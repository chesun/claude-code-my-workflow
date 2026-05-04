# Destructive-Action Guardrails — Plan
**Date:** 2026-05-03
**Status:** Proposed (awaiting approval)
**Supersedes:** —

## Goal

Install hook-level enforcement against destructive operations on shared infrastructure, motivated by the 2026-04-25 incident where `git filter-repo --invert-paths` rewrote a Dropbox-shared repo's working tree, deleted `output/dta/most_recent/`, and force-pushed — all while the session log claimed "working tree unchanged" without verification.

Existing rules (`adversarial-default.md`, the system-prompt "executing actions with care" section) cover this at the prose level but no hook fires. This plan closes that gap with two hooks (one blocking, one warning), one rule, and a test suite.

## Files to create / modify

| File | Type | Purpose |
|---|---|---|
| `.claude/hooks/destructive-action-guard.py` | new | PreToolUse Bash hook — blocks history rewrites unconditionally and `rm -rf` / `find -delete` on shared-storage paths |
| `.claude/hooks/post-rewrite-verify.py` | new | PostToolUse Bash hook — injects verification reminder into the next agent turn after a history rewrite |
| `.claude/hooks/test_destructive_action_guard.py` | new | regression tests; same pattern as `test_primary_source_lib.py` |
| `.claude/rules/destructive-actions.md` | new | rule doc explaining triggers, protected paths, bypass mechanism, post-action verification protocol |
| `.claude/settings.json` | edit | wire both hooks into PreToolUse / PostToolUse Bash matchers |

**Naming note vs spec:** spec said `hooks/destructive-on-shared-block.py`; project convention is `.claude/hooks/<descriptive-name>.py`. The hook handles two classes (always-blocked + path-conditional), so I'd name it `destructive-action-guard.py` rather than `destructive-on-shared-block.py` (the latter implies path-conditional only). Easy to rename if you prefer.

## Detection logic

### Always-blocked commands (regardless of cwd or repo)

Match on shlex-tokenized command string:

| Pattern | Match condition |
|---|---|
| `git filter-repo` | first two tokens are `git filter-repo` |
| `git filter-branch` | first two tokens are `git filter-branch` |
| `git push --force` / `git push -f` / `git push --force-with-lease` | `git push` followed by any force flag in tokens |
| `git push +<refspec>` | `git push` with a refspec arg starting with `+` |
| `git rebase ...` (non-resumption) | `git rebase` *without* any of `--continue`, `--abort`, `--skip`, `--quit` |
| `git update-ref -d` | tokens contain `update-ref` and `-d` |
| `git reset --hard` | tokens contain `reset` and `--hard` |
| `git clean -fd` / `-fdx` / `-fx` | `git clean` with `-f` and `-d` (any combination) |

Rationale: history rewrites and force-pushes are always destructive enough to warrant explicit re-authorization, regardless of whether the repo is shared. The 2026-04-25 incident hit `git filter-repo` specifically.

### Path-conditional commands (block only when target resolves into shared infrastructure)

| Pattern | Path-extraction approach |
|---|---|
| `rm -rf <path>` / `rm -fr` | shlex-tokenize, walk for tokens after `rm` that don't start with `-` |
| `rm -r <path>` / `rm -R` | same |
| `find <path> ... -delete` | `find` + first non-flag arg as starting path |
| `mv <src> <dst>` where `<dst>` would overwrite | path-conditional only on `<dst>` resolving into shared path AND existing |

For each extracted path: resolve relative to effective cwd (see below), call `os.path.realpath()` to follow symlinks, then check prefix against shared-storage list.

### Effective-cwd resolution (handles the `cd X && Y` case)

The hook receives `cwd` from `tool_input` (or `hook_input["cwd"]`). But Bash invocations of form `cd /some/path && rm -rf foo` change the effective cwd mid-command. Need to parse leading `cd <path>` directives:

```python
# Pseudocode
tokens = shlex.split(command)
effective_cwd = hook_input["cwd"]
i = 0
while i < len(tokens) - 2 and tokens[i] == "cd" and tokens[i+2] in ("&&", ";"):
    target = tokens[i+1]
    effective_cwd = os.path.realpath(os.path.join(effective_cwd, target))
    i += 3
# remaining tokens evaluated against effective_cwd
```

This handles `cd dropbox-repo && rm -rf foo` and `cd ~/foo && find . -delete` where `~/foo` is a symlink into Dropbox.

### Shared-storage prefix list

```
~/Library/CloudStorage/Dropbox-*/
~/Library/CloudStorage/Dropbox
~/Library/CloudStorage/GoogleDrive-*/
~/Library/CloudStorage/OneDrive-*/
~/Library/CloudStorage/Box-*/
~/Library/Mobile Documents/com~apple~CloudDocs/   (iCloud Drive)
~/Dropbox/                                        (legacy direct-mount Dropbox)
```

**Spec deviation flagged:** spec said "any path containing `/Dropbox/`". Too broad — would block `rm -rf /tmp/dropbox-repo-clone/foo`. I'd limit to the canonical macOS mount points above. Override flag in the rule for users with non-standard mounts.

After realpath resolution, check whether the path starts with any prefix (after expanding `~` and globs).

### Bypass mechanism

Two paths:

1. **Env-var prefix in command:** `BYPASS_SHARED_GUARD=1 git filter-repo --invert-paths --path output/`. Hook detects the `BYPASS_SHARED_GUARD=1` token at command start and exits 0. Audit trail visible in shell history and the session log.
2. **Conversational re-auth:** the block message instructs the user to re-issue the command with the bypass prefix or explicitly tell Claude to retry with the env-var. No silent bypass.

## Hook 1: `destructive-action-guard.py` (PreToolUse)

Skeleton matching `primary-source-check.py` conventions:

- Shebang `#!/usr/bin/env python3`
- Read JSON from stdin; `json.load(sys.stdin)` with fail-open on `JSONDecodeError`
- `tool_name` filter: only run for `Bash`; exit 0 otherwise
- Extract `command`, `cwd` from `tool_input`
- Run detection: always-blocked first (cheaper), then path-conditional
- On block: write descriptive message to stderr, exit 2
- On allow: exit 0

Block message format:

```
DESTRUCTIVE-ACTION-GUARD: blocking.

Matched: <pattern>
Reason: <"history rewrite — always requires explicit re-authorization" | "destructive command on shared-storage path: <prefix>">
Effective cwd: <resolved>
Resolved path(s): <list>

Why this exists: 2026-04-25 incident — `git filter-repo --invert-paths`
silently rewrote a Dropbox-shared repo's working tree, deleted analysis
output, and force-pushed. The session log falsely claimed "working tree
unchanged" without verification. See .claude/rules/destructive-actions.md.

Bypass:
  - Re-run with: BYPASS_SHARED_GUARD=1 <original command>
  - Or get explicit user re-authorization in the conversation, then re-run
    with the env-var prefix.

Audit trail: any bypass is visible in shell history and session logs.
```

## Hook 2: `post-rewrite-verify.py` (PostToolUse)

- Triggers on PostToolUse for Bash
- Inspects `tool_input.command` for the same history-rewrite patterns as Hook 1's always-blocked class
- If matched: outputs JSON with `decision: "approve"` plus a `reason` field that injects a reminder into the next turn
- Soft injection only — never blocks

Reminder text:

```
HISTORY-REWRITE VERIFICATION REQUIRED.

You ran `<command>`. Before claiming the working tree is unchanged or
the operation succeeded as intended, run BOTH:

  1. ls -la <affected paths>      (compare to expected file list)
  2. du -sh <repo root>           (compare to pre-rewrite size)

The 2026-04-25 incident: a session ran `git filter-repo --invert-paths`,
claimed "Working tree = 8.8 GB unchanged (all .dta files still present)"
without verification, and the deletion only surfaced 8 days later when
a coauthor noticed missing files.

Adversarial-default rule applies: compliance is a positive claim that
requires positive evidence. Without `ls`/`du` output, you have not
verified — do not narrate success.
```

Per Claude Code hook spec, PostToolUse can return JSON with a `hookSpecificOutput.additionalContext` field that gets injected. (Will verify exact field name from current Claude Code docs in implementation.)

## Settings.json wiring

Diff:

```jsonc
{
  "hooks": {
    "PreToolUse": [
      // existing Edit|Write block stays
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "python3 \"$CLAUDE_PROJECT_DIR\"/.claude/hooks/destructive-action-guard.py",
            "timeout": 10
          }
        ]
      }
    ],
    "PostToolUse": [
      // append to existing PostToolUse block
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "python3 \"$CLAUDE_PROJECT_DIR\"/.claude/hooks/post-rewrite-verify.py",
            "timeout": 5
          }
        ]
      }
    ]
  }
}
```

## Rule: `.claude/rules/destructive-actions.md`

Sections:

1. **Why this exists** — one paragraph on the 2026-04-25 incident; cross-reference to `adversarial-default.md`
2. **Always-blocked commands** — table from this plan
3. **Path-conditional commands** — table + the shared-storage prefix list
4. **Effective-cwd resolution** — explanation of the `cd X && Y` parsing
5. **Bypass mechanism** — env-var + conversational re-auth; auditability
6. **Required post-action verification protocol** — `ls`/`du` after history rewrites; pre-snapshot when feasible
7. **What this rule does NOT cover** — non-shared local repos for path-conditional ops; tools other than Bash; signal that future hooks can extend

## Test cases (`test_destructive_action_guard.py`)

Following `test_primary_source_lib.py` pattern: import the hook's library functions via `importlib`, run assertions, print PASS/FAIL, exit 1 on failure.

| # | Case | Expected |
|---|---|---|
| 1 | `git filter-repo --invert-paths` in `/tmp/foo` | BLOCK (always-blocked class) |
| 2 | `git filter-repo --invert-paths` in `~/Library/CloudStorage/Dropbox/repo` | BLOCK |
| 3 | `BYPASS_SHARED_GUARD=1 git filter-repo --invert-paths` in same | ALLOW |
| 4 | `git push --force origin main` in Dropbox repo | BLOCK |
| 5 | `git push -f origin main` (short form) | BLOCK |
| 6 | `git push origin main` in Dropbox repo | ALLOW |
| 7 | `git push origin +main:main` (refspec force) | BLOCK |
| 8 | `git rebase -i HEAD~3` in Dropbox repo | BLOCK |
| 9 | `git rebase --continue` (resumption) | ALLOW |
| 10 | `git reset --hard HEAD~1` | BLOCK |
| 11 | `git reset --soft HEAD~1` | ALLOW |
| 12 | `git clean -fd` | BLOCK |
| 13 | `git clean -n` (dry-run) | ALLOW |
| 14 | `rm -rf foo/` in `/tmp/scratch` | ALLOW (not shared) |
| 15 | `rm -rf foo/` in `~/Library/CloudStorage/Dropbox/...` | BLOCK |
| 16 | `cd ~/foo && rm -rf bar` where `~/foo` symlinks into Dropbox | BLOCK (symlink resolution) |
| 17 | `find ~/Library/CloudStorage/Dropbox/repo -name '*.tmp' -delete` | BLOCK |
| 18 | `find /tmp/scratch -delete` | ALLOW |
| 19 | `rm -rf /tmp/dropbox-test/foo` (substring "dropbox" in path but not in shared mount) | ALLOW (anchor on canonical mount points) |
| 20 | `rm file.txt` (no -r/-f) | ALLOW (not destructive enough to gate) |

Tests 16, 17, 19 require setting up real symlinks / paths in tempdir to validate the realpath resolution.

## Verification steps (post-implementation)

1. All 20 test cases pass (`python3 .claude/hooks/test_destructive_action_guard.py`)
2. Manual smoke test: `git push origin main` (no force) on workflow repo → not blocked
3. Manual smoke test: `git filter-repo --help` (still always blocked, even with `--help`?) — document expected behavior
4. PostToolUse reminder fires after `git rebase HEAD~2 --no-edit` on a test branch
5. Hook errors fail-open (don't break the agent if Python crashes)
6. Settings.json validates: `python3 -c "import json; json.load(open('.claude/settings.json'))"`
7. Cherry-pick to applied-micro and behavioral; sync to 7 downstream repos (same protocol as the all-caps filter ship)

## Open questions / risks

1. **Subagent / Task-tool Bash invocations.** When Claude dispatches a subagent via `Task`, that subagent's Bash calls also pass through PreToolUse hooks (in current Claude Code semantics). Confirm hook fires for sub-agent Bash; if not, the guard has a hole. *Mitigation:* if subagent Bash bypasses hooks, document the gap in the rule and flag as a v2 concern.

2. **`shlex.split()` vs shell metachar handling.** Commands with subshells, command substitution, or unusual quoting may parse oddly. *Mitigation:* on shlex.split failure, conservatively block any always-blocked-class command (fail-closed for the dangerous classes); allow path-conditional commands (fail-open for the lower-stakes class). Document.

3. **`git rebase` — broad blocking may produce friction.** Even an interactive rebase on a personal branch is blocked under spec. Bypass works but feels heavy. *Alternative:* block only `--root` and `--onto`; allow plain `git rebase HEAD~N`. *Recommend:* keep spec-strict for v1; loosen if friction is real. Easier to relax than tighten.

4. **PostToolUse reminder format.** The exact `additionalContext` field name in Claude Code's hook JSON spec needs verification at implementation time (current docs reference is at https://docs.claude.com/en/docs/claude-code/hooks ; field naming has changed across versions).

5. **Path resolution for non-existent targets.** If the user runs `rm -rf foo/` and `foo/` doesn't exist (or never did), `os.path.realpath()` returns the would-be path. Check that anyway — intent matters, even if no-op. *Decision:* yes, check intent.

6. **False-positive cost.** Each block adds friction even when the operation is legitimate. The bypass mechanism is the safety valve, but if the user hits blocks 3+ times on a routine workflow, the rule needs tuning. *Plan:* one-week shakeout window; track bypass invocations in a session log; revisit thresholds if friction is real.

## Sequencing

1. Get approval on this plan
2. Implement hook 1 (destructive-action-guard.py) + tests; run all 20 cases
3. Implement hook 2 (post-rewrite-verify.py); manual smoke test
4. Write rule doc
5. Wire settings.json
6. Single atomic commit on workflow main
7. Cherry-pick to applied-micro + behavioral
8. Sync to 7 downstream repos
9. Update CHANGELOG with v0.2.x line item
