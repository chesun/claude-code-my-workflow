#!/usr/bin/env python3
"""
Primary-Source-First PreToolUse Hook.

Blocks Edit/Write to load-bearing files when the delta cites papers that
lack reading-notes evidence. Three failure modes caught:

  1. Notes don't exist AND the PDF is in the repo — read the PDF, write notes.
  2. Notes don't exist AND the PDF is NOT in the repo — add the PDF first.
  3. Notes exist but were not Read with the Read tool in this session —
     session-scoped verification that cached context is not being substituted
     for actual paper consultation.

Shared logic lives in primary_source_lib.py. This file is the PreToolUse
entry point.

Install (in .claude/settings.json, PreToolUse block with matcher "Edit|Write"):
    python3 "$CLAUDE_PROJECT_DIR"/.claude/hooks/primary-source-check.py

Fail-open on any internal exception.
"""

from __future__ import annotations

import importlib.util
import json
import os
import sys
from pathlib import Path


def _load_lib():
    """Load primary_source_lib from the same directory as this script."""
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

    tool_name = hook_input.get("tool_name", "")
    if tool_name not in {"Edit", "Write"}:
        sys.exit(0)

    tool_input = hook_input.get("tool_input", {}) or {}
    file_path = tool_input.get("file_path", "") or ""
    if not file_path:
        sys.exit(0)

    project_dir = os.environ.get("CLAUDE_PROJECT_DIR", hook_input.get("cwd", ""))
    if not project_dir:
        sys.exit(0)

    project_root = Path(project_dir)
    try:
        rel_path = str(Path(file_path).resolve().relative_to(project_root.resolve()))
    except (ValueError, OSError):
        sys.exit(0)

    if not lib.is_enforceable(rel_path):
        sys.exit(0)

    # Extract the delta.
    if tool_name == "Write":
        delta = tool_input.get("content", "") or ""
    else:  # Edit
        delta = tool_input.get("new_string", "") or ""
    if not delta.strip():
        sys.exit(0)

    citations = lib.extract_citations(delta)
    if not citations:
        sys.exit(0)

    escaped = lib.extract_escaped_stems(delta)

    reading_notes_dir = project_root / "master_supporting_docs" / "literature" / "reading_notes"
    papers_dir = project_root / "master_supporting_docs" / "literature" / "papers"

    transcript_path_str = hook_input.get("transcript_path", "") or ""
    transcript_path = Path(transcript_path_str) if transcript_path_str else None

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
            f"You are writing to a load-bearing file: {rel_path}\n"
            "The new content makes claims about cited papers that lack the "
            "required reading-notes evidence."
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
