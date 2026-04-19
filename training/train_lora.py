"""LoRA fine-tuning template for legal instruction model.

This script is a template. Install: transformers, datasets, peft, trl, accelerate.
"""

# NOTE: keep imports in function scope so this file can exist without heavy deps.


def main() -> None:
    from datasets import load_dataset
    from transformers import AutoTokenizer, AutoModelForCausalLM, TrainingArguments
    from peft import LoraConfig
    from trl import SFTTrainer

    model_name = "meta-llama/Meta-Llama-3-8B-Instruct"
    data_path = "data/sft_legal_instructions.jsonl"

    dataset = load_dataset("json", data_files=data_path, split="train")
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForCausalLM.from_pretrained(model_name)

    def fmt(row: dict) -> str:
        return (
            f"<|system|>\n{row['system']}\n"
            f"<|user|>\n{row['user']}\n"
            f"<|assistant|>\n{row['assistant']}"
        )

    dataset = dataset.map(lambda x: {"text": fmt(x)})

    peft_config = LoraConfig(
        r=16,
        lora_alpha=32,
        lora_dropout=0.05,
        bias="none",
        task_type="CAUSAL_LM",
    )

    args = TrainingArguments(
        output_dir="outputs/legal-lora",
        per_device_train_batch_size=2,
        gradient_accumulation_steps=8,
        num_train_epochs=2,
        learning_rate=2e-4,
        fp16=True,
        logging_steps=10,
        save_steps=200,
    )

    trainer = SFTTrainer(
        model=model,
        train_dataset=dataset,
        args=args,
        peft_config=peft_config,
        formatting_func=lambda ex: ex["text"],
    )
    trainer.train()
    trainer.save_model("outputs/legal-lora/final")


if __name__ == "__main__":
    main()
