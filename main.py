from __future__ import annotations

import json
from pathlib import Path

from src.pipeline import DEFAULT_QUESTION, run_pipeline


def main() -> None:
    summary = run_pipeline(Path(__file__).resolve().parent, question=DEFAULT_QUESTION)
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
