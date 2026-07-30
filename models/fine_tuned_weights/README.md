# Fine-Tuned Model Weights Directory

This directory stores your fine-tuned small LLM weights (e.g. `careermarg_0.5b.gguf`).

---

## 📌 How to Place Your Fine-Tuned Weights Here:

1. Open and run [notebooks/Fine_Tune_CareerGPT.ipynb](file:///d:/MS_AI_ML/Trimester%204/LLM/CIA%203/notebooks/Fine_Tune_CareerGPT.ipynb) in **Google Colab** (with free T4 GPU).
2. After fine-tuning completes, Colab will automatically prompt you to download `careermarg_0.5b_weights-Q4_K_M.gguf`.
3. Rename the downloaded `.gguf` file to:
   ```text
   careermarg_0.5b.gguf
   ```
4. Move/paste `careermarg_0.5b.gguf` into this exact directory:
   ```text
   CIA 3/models/fine_tuned_weights/careermarg_0.5b.gguf
   ```

Once placed here, **Career मार्ग** (`services/llm_service.py`) will automatically detect and load your fine-tuned weights for local offline execution!
