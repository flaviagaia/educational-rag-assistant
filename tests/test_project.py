from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from src.generation import build_grounded_answer
from src.pipeline import run_pipeline


class EducationalRagAssistantTestCase(unittest.TestCase):
    def test_pipeline_contract(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            summary = run_pipeline(temp_dir)
            self.assertEqual(summary["dataset_source"], "educational_corpus_local_sample")
            self.assertEqual(summary["document_count"], 8)
            self.assertGreaterEqual(summary["top_similarity"], 0.15)
            self.assertGreaterEqual(summary["confidence"], 0.25)

            report = json.loads(Path(summary["report_artifact"]).read_text(encoding="utf-8"))
            self.assertIn("answer", report)
            self.assertGreaterEqual(len(report["sources"]), 2)

    def test_grounded_answer_mentions_source_content(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            response = build_grounded_answer(
                temp_dir,
                query="When are office hours and how should students ask conceptual questions?",
                top_k=3,
            )
            self.assertIn("Tuesdays from 6 PM to 7 PM Eastern Time", response["answer"])
            self.assertEqual(response["sources"][0]["doc_id"], "EDU-1004")


if __name__ == "__main__":
    unittest.main()
