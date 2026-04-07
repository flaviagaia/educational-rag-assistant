from __future__ import annotations

import json
from pathlib import Path
from tempfile import NamedTemporaryFile

import pandas as pd


PUBLIC_DATASET_REFERENCE = {
    "dataset_name": "Syllabus-style educational corpus",
    "dataset_reference": "Locally curated education-tech sample inspired by course materials, policies, and study guides.",
    "dataset_note": (
        "This repository uses a compact local academic corpus so the RAG workflow remains deterministic, "
        "testable, and production-oriented without external network dependencies."
    ),
}


def _atomic_write_csv(df: pd.DataFrame, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with NamedTemporaryFile("w", suffix=".csv", delete=False, dir=path.parent, encoding="utf-8") as tmp_file:
        temp_path = Path(tmp_file.name)
    try:
        df.to_csv(temp_path, index=False)
        temp_path.replace(path)
    finally:
        if temp_path.exists():
            temp_path.unlink()


def _atomic_write_json(payload: dict, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with NamedTemporaryFile("w", suffix=".json", delete=False, dir=path.parent, encoding="utf-8") as tmp_file:
        temp_path = Path(tmp_file.name)
    try:
        temp_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
        temp_path.replace(path)
    finally:
        if temp_path.exists():
            temp_path.unlink()


def _build_corpus() -> pd.DataFrame:
    rows = [
        {
            "doc_id": "EDU-1001",
            "document_type": "syllabus",
            "title": "Introduction to Data Science - Syllabus",
            "section_title": "Late Work and Submission Policy",
            "source_label": "Syllabus / Submission Policy",
            "content": (
                "Assignments are due on Sundays at 11:59 PM Eastern Time. "
                "Late submissions made within 48 hours receive up to 80 percent of the original grade. "
                "After 48 hours, the assignment receives zero unless the instructor approved an extension in advance."
            ),
        },
        {
            "doc_id": "EDU-1002",
            "document_type": "study_guide",
            "title": "Machine Learning Study Guide",
            "section_title": "Bias, Variance, and Generalization",
            "source_label": "Study Guide / Model Evaluation",
            "content": (
                "High bias usually means the model is too simple and underfits the data. "
                "High variance means the model is too sensitive to the training set and may overfit. "
                "Cross-validation helps estimate generalization performance before deployment."
            ),
        },
        {
            "doc_id": "EDU-1003",
            "document_type": "assignment_brief",
            "title": "Assignment 2 - Educational RAG Prototype",
            "section_title": "Deliverables",
            "source_label": "Assignment Brief / Deliverables",
            "content": (
                "Students must submit a GitHub repository, a short architecture note, and a demo video under five minutes. "
                "The repository should include reproducible instructions, dependency definitions, and automated tests."
            ),
        },
        {
            "doc_id": "EDU-1004",
            "document_type": "course_faq",
            "title": "Course FAQ",
            "section_title": "Office Hours and Instructor Support",
            "source_label": "FAQ / Instructor Support",
            "content": (
                "Office hours are held on Tuesdays from 6 PM to 7 PM Eastern Time. "
                "Students should post conceptual questions in the discussion board before requesting private support, "
                "unless the issue involves grades or personal accommodations."
            ),
        },
        {
            "doc_id": "EDU-1005",
            "document_type": "reading_notes",
            "title": "Reading Notes - Retrieval Augmented Generation",
            "section_title": "Chunking and Retrieval Quality",
            "source_label": "Reading Notes / RAG Foundations",
            "content": (
                "Chunking controls the retrieval unit sent to the model. "
                "Chunks that are too large dilute the relevant context, while chunks that are too small may lose coherence. "
                "A strong RAG system balances semantic completeness with retrieval precision."
            ),
        },
        {
            "doc_id": "EDU-1006",
            "document_type": "student_handbook",
            "title": "Online Learning Handbook",
            "section_title": "Academic Integrity",
            "source_label": "Handbook / Academic Integrity",
            "content": (
                "Students may use AI tools for brainstorming and language support when the assignment explicitly allows it. "
                "Any AI assistance must be disclosed. Submitting generated content as original work without disclosure violates academic integrity rules."
            ),
        },
        {
            "doc_id": "EDU-1007",
            "document_type": "rubric",
            "title": "Project Rubric",
            "section_title": "Evaluation Criteria",
            "source_label": "Rubric / Evaluation Criteria",
            "content": (
                "Projects are evaluated on technical correctness, clarity of explanation, reproducibility, and evidence of testing. "
                "Strong submissions also explain trade-offs and document known limitations."
            ),
        },
        {
            "doc_id": "EDU-1008",
            "document_type": "course_calendar",
            "title": "Course Calendar",
            "section_title": "Assessment Schedule",
            "source_label": "Calendar / Assessments",
            "content": (
                "Quiz 1 is scheduled for September 12, the midterm for October 3, and the final project presentation for November 21. "
                "Any schedule update is announced in the learning platform and in the weekly digest."
            ),
        },
    ]
    return pd.DataFrame(rows)


def ensure_corpus(base_dir: str | Path) -> dict[str, str]:
    base_path = Path(base_dir)
    corpus_path = base_path / "data" / "raw" / "educational_corpus.csv"
    reference_path = base_path / "data" / "raw" / "public_dataset_reference.json"

    corpus_df = _build_corpus()
    _atomic_write_csv(corpus_df, corpus_path)
    _atomic_write_json(PUBLIC_DATASET_REFERENCE, reference_path)

    return {
        "corpus_path": str(corpus_path),
        "reference_path": str(reference_path),
    }
