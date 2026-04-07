from __future__ import annotations

from pathlib import Path

from src.retrieval import retrieve_top_k


def build_grounded_answer(base_dir: str | Path, query: str, top_k: int = 3) -> dict:
    _, retrieved = retrieve_top_k(base_dir, query=query, top_k=top_k)
    primary = retrieved[0]
    secondary = retrieved[1] if len(retrieved) > 1 else None

    answer_parts = [
        f"Based on {primary.source_label}, {primary.content}",
    ]
    if secondary and secondary.similarity >= 0.15:
        answer_parts.append(
            f"Additional supporting context from {secondary.source_label}: {secondary.content}"
        )

    confidence = round(min(max(primary.similarity * 1.85, 0.0), 0.99), 4)
    limitation_note = (
        "This answer is grounded only in the retrieved educational corpus used by the MVP. "
        "A production system should validate document version, course term, and policy recency."
    )

    return {
        "question": query,
        "answer": " ".join(answer_parts),
        "confidence": confidence,
        "sources": [
            {
                "doc_id": item.doc_id,
                "title": item.title,
                "section_title": item.section_title,
                "source_label": item.source_label,
                "similarity": item.similarity,
            }
            for item in retrieved
        ],
        "limitation_note": limitation_note,
    }
