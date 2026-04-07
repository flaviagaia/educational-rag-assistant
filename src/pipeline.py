from __future__ import annotations

import json
from pathlib import Path

from src.generation import build_grounded_answer
from src.sample_data import ensure_corpus


DEFAULT_QUESTION = "What is the late submission policy and what should students submit for the project?"


def run_pipeline(base_dir: str | Path, question: str = DEFAULT_QUESTION) -> dict:
    base_path = Path(base_dir)
    dataset = ensure_corpus(base_path)
    response = build_grounded_answer(base_path, query=question, top_k=3)

    processed_dir = base_path / "data" / "processed"
    processed_dir.mkdir(parents=True, exist_ok=True)
    report_path = processed_dir / "educational_rag_report.json"
    report_path.write_text(json.dumps(response, ensure_ascii=False, indent=2), encoding="utf-8")

    summary = {
        "dataset_source": "educational_corpus_local_sample",
        "public_dataset_reference": dataset["reference_path"],
        "document_count": 8,
        "question": question,
        "top_source": response["sources"][0]["doc_id"],
        "top_similarity": response["sources"][0]["similarity"],
        "confidence": response["confidence"],
        "report_artifact": str(report_path),
    }
    return summary
