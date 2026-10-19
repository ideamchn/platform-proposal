# proposal

A scaffold for writing a platform proposal from scratch, one phase at a time, with Claude Code.
You keep a small set of context files current; the `/generate-proposal` command turns them into a
draft for the phase you name.

```
/generate-proposal phase-1
/generate-proposal phase-2      # starts from what phase 1 deferred
```

The proposal follows a fixed shape: what the phase delivers, what it enables, must-haves, what to
fund first, a step-by-step plan that ends each step in a demo, the highest risks, a North Star
with targets and the reasons for them, and your open questions. The rules behind each choice are
in `prompts/generate-proposal.md`, so a fresh session makes the same calls from the same inputs.

## Layout

```
context/                     your frame and current state (you write these)
  company.template.md        mandate, workstreams, thesis, constraints     → company.md
  research-goals.template.md hypotheses H1… tied to gaps                   → research-goals.md
  now.template.md            dated current state, by proposal section      → now.md
inputs/                      documents you drop in for a run
  brief.template.md          the ask, verbatim                             → brief.md
  gap-register.template.md   what the platform doesn't do yet              → gap-register.md
  competitive.template.md    optional competitive and gap report           → competitive.md
prompts/generate-proposal.md the rules and the output shape
.claude/commands/            /generate-proposal
tools/check.py               pre-flight: files present and filled in, now.md not stale, output path
outputs/                     proposal-<phase>-<date>.md
tests/                       unittest suite for the pre-flight (standard library only)
```

Your real files (`context/*.md`, `inputs/*.md`, `outputs/*`) are gitignored. The repo ships
templates only, so it's safe to share or push anywhere.

## Getting started

1. **Copy each template** to its real name (drop `.template`) and fill it in:
   ```bash
   for f in context/*.template.md inputs/*.template.md; do cp -n "$f" "${f/.template/}"; done
   ```
2. **Fill in `context/now.md`** last, and keep it current. It's the file that changes most:
   - your own observations, as bullets, under the proposal section each one feeds;
   - no quotes and no "per <name>": the proposal states them in your voice;
   - an **As of** and a **Review by** date. The command refuses to run once the review date has
     passed, so a proposal is never built on stale state.
3. **Check:** `python3 tools/check.py phase-1`. It reports missing files, files still holding
   template placeholders, a stale `now.md`, and the output path it will use.
4. **Generate:** open Claude Code in this folder and run `/generate-proposal phase-1`.

## How phases work

- **Phase 1** starts from the gap register. Its defaults:
  - read-only first, plus a dated design for write access;
  - the consumer closest to production as the first tenant, protected by a shadow-mode cutover.
- **Phase 2 and later** read the latest earlier-phase proposal in `outputs/`. They start from what
  it deferred, its pending designs and its open risks, plus gap rows still open. They open with a
  "Since Phase N" table: what shipped, what moved, what was dropped.
- **The brief can override any default**, since it's what's being asked.
- **Runs never overwrite:** a second run on the same day gets a `-2` suffix.

## What the inputs are for

| File | Changes | What the proposal uses it for |
|---|---|---|
| `company.md` | rarely | framing; its constraints are hard rules |
| `research-goals.md` | per round | the H-numbers each capability closes; risks |
| `gap-register.md` | as gaps close | the candidate scope |
| `now.md` | weekly | every fact about teams, consumers, dates, capacity and decisions |
| `brief.md` | per proposal | the structure and the questions to answer |
| `competitive.md` | per competitive run | a "why now" point, gaps rivals have closed, proposed scope edits |

Anything not in these files won't appear in the proposal, and nothing will warn you it's missing.
If a fact matters, put it in `now.md`.
