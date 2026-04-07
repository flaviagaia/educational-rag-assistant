from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from src.sample_data import ensure_corpus


@dataclass
class RetrievalResult:
    doc_id: str
    title: str
    section_title: str
    source_label: str
    content: str
    similarity: float


def retrieve_top_k(base_dir: str | Path, query: str, top_k: int = 3) -> tuple[pd.DataFrame, list[RetrievalResult]]:
    dataset = ensure_corpus(base_dir)
    corpus = pd.read_csv(dataset["corpus_path"])

    searchable_text = (
        corpus["title"].fillna("")
        + " "
        + corpus["section_title"].fillna("")
        + " "
        + corpus["content"].fillna("")
    )
    vectorizer = TfidfVectorizer(ngram_range=(1, 2), stop_words="english")
    matrix = vectorizer.fit_transform(searchable_text)
    query_vector = vectorizer.transform([query])
    similarities = cosine_similarity(query_vector, matrix).ravel()

    corpus = corpus.copy()
    corpus["similarity"] = similarities
    ranked = corpus.sort_values("similarity", ascending=False).head(top_k)
    results = [
        RetrievalResult(
            doc_id=row.doc_id,
            title=row.title,
            section_title=row.section_title,
            source_label=row.source_label,
            content=row.content,
            similarity=round(float(row.similarity), 4),
        )
        for row in ranked.itertuples(index=False)
    ]
    return corpus, results
