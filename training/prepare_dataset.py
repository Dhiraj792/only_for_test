"""Prepare instruction-style dataset for legal chatbot SFT.

Input format (JSONL):
{"question": "...", "answer": "...", "jurisdiction": "US", "source": "..."}
"""
from pathlib import Path
import json

def to_instruction(record: dict) -> dict:
    system = (
        "You are a legal information assistant. Provide general information only, "
        "do not provide legal advice, and cite jurisdiction context when available."
    )
    user = f"Jurisdiction: {record.get('jurisdiction', 'US')}\nQuestion: {record['question']}"
    assistant = (
        f"{record['answer']}\n\n"
        "Disclaimer: This is general legal information, not legal advice."
    )
    return {"system": system, "user": user, "assistant": assistant}


def main() -> None:
    src = Path("data/raw_legal_qa.jsonl")
    out = Path("data/sft_legal_instructions.jsonl")
    out.parent.mkdir(parents=True, exist_ok=True)

    if not src.exists():
        print(f"Missing {src}. Add raw Q/A data first.")
        return

    count = 0
    with src.open("r", encoding="utf-8") as fin, out.open("w", encoding="utf-8") as fout:
        for line in fin:
            record = json.loads(line)
            converted = to_instruction(record)
            fout.write(json.dumps(converted, ensure_ascii=False) + "\n")
            count += 1

    print(f"Wrote {count} rows to {out}")


if __name__ == "__main__":
    main()
