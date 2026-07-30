# ==============================================================================
# Fine-Tune Career मार्ग Small LLM (Qwen2.5-0.5B-Instruct) in Google Colab
# ==============================================================================
# Instructions:
# 1. Open Google Colab (https://colab.research.google.com/)
# 2. Set Runtime to T4 GPU (Runtime -> Change runtime type -> T4 GPU)
# 3. Paste and run this script in a code cell.
# ==============================================================================

# Step 1: Install Unsloth & Dependencies
!pip install --no-deps "unsloth[colab-new] @ git+https://github.com/unslothai/unsloth.git"
!pip install --no-deps unsloth_zoo
!pip install --no-deps "xformers" "peft" "accelerate" "bitsandbytes" "trl" "datasets"

import torch
from unsloth import FastLanguageModel
from datasets import Dataset
from trl import SFTTrainer
from transformers import TrainingArguments

# Step 2: Load 4-bit Quantized Base Model (Qwen2.5-0.5B)
max_seq_length = 2048
model_name = "unsloth/Qwen2.5-0.5B-Instruct-bnb-4bit"

model, tokenizer = FastLanguageModel.from_pretrained(
    model_name = model_name,
    max_seq_length = max_seq_length,
    load_in_4bit = True,
)

model = FastLanguageModel.get_peft_model(
    model,
    r = 16,
    target_modules = ["q_proj", "k_proj", "v_proj", "o_proj", "gate_proj", "up_proj", "down_proj"],
    lora_alpha = 16,
    lora_dropout = 0,
    bias = "none",
    use_gradient_checkpointing = "unsloth",
)
print("✓ Model and LoRA adapters loaded successfully!")

# Step 3: Prepare Training Dataset
training_samples = [
    {
        "instruction": "Synthesize an executive professional summary from raw candidate experience.",
        "input": "Candidate with 2 years in Python, FastAPI, Docker, and PostgreSQL. Built microservices.",
        "output": "Results-driven Software Engineer with 2 years of experience building scalable microservices using Python, FastAPI, Docker, and PostgreSQL."
    },
    {
        "instruction": "Transform weak bullet point into quantifiable achievement bullet.",
        "input": "Worked on machine learning model for customer sentiment.",
        "output": "Engineered and deployed an NLP sentiment classification model using PyTorch, improving prediction accuracy by [X%] and reducing inference latency by [Y ms]."
    },
    {
        "instruction": "Generate 30-day skill gap action plan summary.",
        "input": "Target Role: MLOps Engineer. Missing Skills: Docker, Kubernetes, MLflow.",
        "output": "30-Day Strategy for MLOps Engineer: Focus Days 1–10 on Docker containerization, Days 11–20 on Kubernetes orchestration, and Days 21–30 on deploying a full MLflow tracking pipeline."
    }
]

formatted_data = []
for sample in training_samples:
    text = f"<|im_start|>system\n{sample['instruction']}<|im_end|>\n<|im_start|>user\n{sample['input']}<|im_end|>\n<|im_start|>assistant\n{sample['output']}<|im_end|>"
    formatted_data.append({"text": text})

dataset = Dataset.from_list(formatted_data)

from trl import SFTTrainer, SFTConfig

# Step 4: Fine-Tune with SFTTrainer (with Packing Enabled)
trainer = SFTTrainer(
    model = model,
    tokenizer = tokenizer,
    train_dataset = dataset,
    dataset_text_field = "text",
    max_seq_length = max_seq_length,
    packing = True,
    args = SFTConfig(
        per_device_train_batch_size = 2,
        gradient_accumulation_steps = 4,
        warmup_steps = 5,
        max_steps = 60,
        learning_rate = 2e-4,
        fp16 = not torch.cuda.is_bf16_supported(),
        bf16 = torch.cuda.is_bf16_supported(),
        logging_steps = 10,
        output_dir = "outputs",
    ),
)
trainer.train()
print("🎉 Fine-tuning complete!")

# Step 5: Export to GGUF and Download
model.save_pretrained_gguf("careermarg_0.5b_weights", tokenizer, quantization_method = "q4_k_m")

from google.colab import files
files.download("careermarg_0.5b_weights_gguf/Qwen2.5-0.5B-Instruct.Q4_K_M.gguf")
