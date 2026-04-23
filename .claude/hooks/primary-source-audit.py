#!/usr/bin/env python3
"""
Primary-Source-First Stop Hook — audits conversation prose.

Scans all assistant text messages in the session transcript for citation
patterns. For each citation found in prose (not just in tool-call content),
checks whether reading-notes exist and whether they were Read with the Read
tool during this session. If any citation lacks evidence, blocks the Stop
with a warning listing the gaps.

Rationale: the PreToolUse hook only sees tool-call content. A citation made
only in conversation text (e.g., an assistant response summarizing a paper's
claim) would escape enforcement. This hook closes that gap.

Install (in .claude/settings.json, Stop block):
    python3 "$CLAUDE_PROJECT_DIR"/.claude/hooks/primary-source-audit.py

Fail-open on any internal exception.

Stop-loop safety: respects the `stop_hook_active` flag to avoid infinite
loops — if Claude is already continuing from a prior Stop block, this hook
exits without blocking again in the same turn.
"""

from __future__ import annotations

import importlib.util
import json
import os
import sys
from pathlib import Path


def _load_lib():
    lib_path = Path(__file__).resolve().parent / "primary_source_lib.py"
    spec = importlib.util.spec_from_file_location("primary_source_lib", lib_path)
    if spec is None or spec.loader is None:
        raise ImportError(f"Cannot load {lib_path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def main() -> None:
    lib = _load_lib()

    try:
        hook_input = json.load(sys.stdin)
    except (json.JSONDecodeError, EOFError):
        sys.exit(0)

    # Avoid stop-hook loops: if Claude is already continuing from a prior
    # block in this turn, let it stop this time.
    if hook_input.get("stop_hook_active", False):
        sys.exit(0)

    transcript_path_str = hook_input.get("transcript_path", "") or ""
    if not transcript_path_str:
        sys.exit(0)
    transcript_path = Path(transcript_path_str)
    if not transcript_path.is_file():
        sys.exit(0)

    project_dir = os.environ.get("CLAUDE_PROJECT_DIR", hook_input.get("cwd", ""))
    if not project_dir:
        sys.exit(0)
    project_root = Path(project_dir)

    # Gather assistant prose from the session.
    assistant_text = lib.extract_assistant_text(transcript_path)
    if not assistant_text.strip():
        sys.exit(0)

    citations = lib.extract_citations(assistant_text)
    if not citations:
        sys.exit(0)

    # Scan escape hatches from prose AND from tool-use inputs. An escape
    # hatch placed inside a file edit is valid evidence that the citation
    # was intentionally ungrounded; no need to repeat in prose.
    escaped = lib.extract_escaped_stems(assistant_text)
    escaped |= lib.extract_escaped_stems(lib.extract_tool_use_inputs(transcript_path))

    reading_notes_dir = project_root / "master_supporting_docs" / "literature" / "reading_notes"
    papers_dir = project_root / "master_supporting_docs" / "literature" / "papers"

    missing = []
    for stem, display in citations:
        if stem in escaped:
            continue
        status = lib.describe_missing_status(
            stem, reading_notes_dir, papers_dir, transcript_path
        )
        if status is None:
            continue
        missing.append((stem, display, status))

    if not missing:
        sys.exit(0)

    message = lib.build_block_message(
        context_description=(
            "Stop-hook audit: your session prose cites papers that lack "
            "reading-notes evidence. Claims in conversation are subject to the "
            "same primary-source-first rule as claims in files."
        ),
        missing=missing,
    )
    output = {"decision": "block", "reason": message}
    json.dump(output, sys.stdout)
    sys.exit(0)


if __name__ == "__main__":
    try:
        main()
    except Exception:
        sys.exit(0)
