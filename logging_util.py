"""
Capstone (Unit 9): structured run logging.

Every call to `app.py::ask_pipeline` — whether it comes from the command line
or from `serve.py`'s `/ask` route — writes one JSON line to `logs/runs.jsonl`
through `log_run()` below. One line per run, one call site, so the CLI and the
server can never drift out of step with each other.

This is deliberately a thin module: it only knows how to build a record and
append it to a file. It doesn't know what a "run" is — that's `ask_pipeline`'s
job, timing itself and handing the fields in.
"""

import json
import time
import uuid
from pathlib import Path

import config

LOG_DIR = config.ROOT / "logs"
LOG_FILE = LOG_DIR / "runs.jsonl"

_MAX_FIELD_CHARS = 500  # long questions/answers are truncated before logging


def _truncate(text: str | None) -> str | None:
    if text is None:
        return None
    if len(text) <= _MAX_FIELD_CHARS:
        return text
    return text[:_MAX_FIELD_CHARS] + f"...[truncated, {len(text)} chars total]"


def new_run_id() -> str:
    """A short id to tell runs apart in the log without reading timestamps."""
    return uuid.uuid4().hex[:12]


def log_run(
    *,
    run_id: str,
    corpus: str,
    question: str,
    duration_ms: float,
    status: str,
    answer: str | None = None,
    refused: bool | None = None,
    sources: list[str] | None = None,
    best_distance: float | None = None,
    threshold: float | None = None,
    model: str | None = None,
    input_tokens: int | None = None,
    output_tokens: int | None = None,
    error_type: str | None = None,
    error_message: str | None = None,
) -> dict:
    """
    Build one structured record and append it to `logs/runs.jsonl`.

    `status` is "ok" or "error". On "error", `error_type`/`error_message`
    should be set and most of the answer-shaped fields will be None, since the
    pipeline didn't finish. Returns the record that was written, mainly so
    callers/tests can inspect it without re-reading the file.
    """
    record = {
        "timestamp": _now_iso(),
        "run_id": run_id,
        "corpus": corpus,
        "input": _truncate(question),
        "output": _truncate(answer),
        "duration_ms": round(duration_ms, 1),
        "status": status,
        "refused": refused,
        "sources": sources or [],
        "best_distance": round(best_distance, 4) if best_distance is not None else None,
        "threshold": threshold,
        "model": model,
        "input_tokens": input_tokens,
        "output_tokens": output_tokens,
        "error_type": error_type,
        "error_message": _truncate(error_message),
    }

    LOG_DIR.mkdir(parents=True, exist_ok=True)
    with LOG_FILE.open("a", encoding="utf-8") as f:
        f.write(json.dumps(record) + "\n")

    return record


def _now_iso() -> str:
    return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
