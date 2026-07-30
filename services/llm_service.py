"""
Provider-Independent LLM Service for Career मार्ग.
Supports Mistral API, OpenAI API, Ollama (Local), and Heuristic NLP Fallbacks.
"""

import os
import json
import requests
from typing import Dict, Any, Optional
from dotenv import load_dotenv

load_dotenv()


class LLMService:
    def __init__(self):
        self.provider = os.getenv("LLM_PROVIDER", "mistral").lower()
        self.mistral_key = os.getenv("MISTRAL_API_KEY", "").strip()
        self.openai_key = os.getenv("OPENAI_API_KEY", os.getenv("LLM_API_KEY", "")).strip()

        # Path to local fine-tuned GGUF weights
        self.fine_tuned_path = os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            "models", "fine_tuned_weights", "careermarg_0.5b.gguf"
        )
        self.has_fine_tuned_weights = os.path.exists(self.fine_tuned_path)

    def generate_json(self, prompt: str, system_prompt: str = "") -> Optional[Dict[str, Any]]:
        """
        Generates structured JSON response from configured LLM provider.
        """
        raw_text = self.generate_text(prompt, system_prompt)
        if not raw_text:
            return None
            
        return self._extract_json(raw_text)

    def generate_text(self, prompt: str, system_prompt: str = "") -> str:
        """
        Generates text completion using Local Fine-Tuned Weights, Mistral, OpenAI, Ollama, or fallback logic.
        """
        # 0. Local Fine-Tuned Weights (if careermarg_0.5b.gguf exists)
        if self.has_fine_tuned_weights:
            try:
                res = self._call_local_gguf(prompt, system_prompt)
                if res:
                    return res
            except Exception:
                pass

        # 1. Mistral API
        if self.provider == "mistral" and self.mistral_key and self.mistral_key != "your_mistral_api_key_here":
            try:
                res = self._call_mistral_chat(prompt, system_prompt)
                if res:
                    return res
            except Exception:
                pass

        # 2. OpenAI API
        if self.openai_key and self.openai_key != "your_openai_api_key_here":
            try:
                res = self._call_openai_chat(prompt, system_prompt)
                if res:
                    return res
            except Exception:
                pass

        # 3. Ollama (Local)
        if self.provider == "ollama":
            try:
                res = self._call_ollama_chat(prompt, system_prompt)
                if res:
                    return res
            except Exception:
                pass

        # Return empty string to trigger domain service fallbacks
        return ""

    def _call_local_gguf(self, prompt: str, system_prompt: str) -> Optional[str]:
        """
        Loads and executes local fine-tuned GGUF weights via llama-cpp-python if installed.
        """
        try:
            from llama_cpp import Llama
            llm = Llama(model_path=self.fine_tuned_path, n_ctx=2048, verbose=False)
            formatted = f"<|im_start|>system\n{system_prompt}<|im_end|>\n<|im_start|>user\n{prompt}<|im_end|>\n<|im_start|>assistant\n"
            output = llm(formatted, max_tokens=512, stop=["<|im_end|>"])
            return output["choices"][0]["text"].strip()
        except Exception:
            return None

    def _call_mistral_chat(self, prompt: str, system_prompt: str) -> Optional[str]:
        url = "https://api.mistral.ai/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {self.mistral_key}",
            "Content-Type": "application/json"
        }
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})

        payload = {
            "model": "mistral-large-latest",
            "messages": messages,
            "temperature": 0.2
        }

        resp = requests.post(url, json=payload, headers=headers, timeout=25)
        if resp.status_code == 200:
            data = resp.json()
            return data["choices"][0]["message"]["content"]
        return None

    def _call_openai_chat(self, prompt: str, system_prompt: str) -> Optional[str]:
        url = "https://api.openai.com/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {self.openai_key}",
            "Content-Type": "application/json"
        }
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})

        payload = {
            "model": "gpt-4o-mini",
            "messages": messages,
            "temperature": 0.2
        }

        resp = requests.post(url, json=payload, headers=headers, timeout=25)
        if resp.status_code == 200:
            data = resp.json()
            return data["choices"][0]["message"]["content"]
        return None

    def _call_ollama_chat(self, prompt: str, system_prompt: str) -> Optional[str]:
        url = "http://localhost:11434/api/generate"
        full_prompt = f"{system_prompt}\n\n{prompt}" if system_prompt else prompt
        payload = {
            "model": "llama3",
            "prompt": full_prompt,
            "stream": False
        }
        resp = requests.post(url, json=payload, timeout=20)
        if resp.status_code == 200:
            return resp.json().get("response")
        return None

    def _extract_json(self, text: str) -> Optional[Dict[str, Any]]:
        """
        Parses JSON object from markdown code block or raw string.
        """
        try:
            # Check for ```json ... ``` blocks
            if "```json" in text:
                text = text.split("```json")[1].split("```")[0]
            elif "```" in text:
                text = text.split("```")[1].split("```")[0]
                
            return json.loads(text.strip())
        except Exception:
            return None
