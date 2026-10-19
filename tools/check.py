"""Pre-flight for /generate-proposal.

    python3 tools/check.py <phase>          e.g. phase-1, phase-2

Checks that the real (non-template) files exist and aren't still templates, that now.md is within
its review date, finds the previous phase's latest proposal, and prints the output path for this
run. Exits 1 on any blocking problem. Standard library only.
"""
from __future__ import annotations

import re
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
REQUIRED = ["context/company.md", "context/research-goals.md", "context/now.md",
            "inputs/brief.md", "inputs/gap-register.md"]
OPTIONAL = ["inputs/competitive.md"]
PHASE_RE = re.compile(r"^phase-(\d+)$")


def is_template(text: str) -> bool:
    """Still the template if its angle-bracket placeholders were never filled in."""
    return len(re.findall(r"<[a-zA-Z][^<>\n]{2,}>", text)) >= 3


def dates_from_now(text: str) -> tuple[date | None, date | None]:
    def find(label):
        m = re.search(rf"\*\*{label}:\*\*\s*(\d{{4}}-\d{{2}}-\d{{2}})", text)
        return date.fromisoformat(m.group(1)) if m else None
    return find("As of"), find("Review by")


def previous_proposal(outputs: Path, n: int) -> Path | None:
    if n <= 1:
        return None
    for k in range(n - 1, 0, -1):
        found = sorted(outputs.glob(f"proposal-phase-{k}-*.md"))
        if found:
            return found[-1]
    return None


def next_output(outputs: Path, phase: str, today: date) -> Path:
    base = outputs / f"proposal-{phase}-{today.isoformat()}.md"
    i = 2
    out = base
    while out.exists():
        out = base.with_name(f"{base.stem}-{i}.md")
        i += 1
    return out


def check(root: Path, phase: str, today: date) -> tuple[list[str], list[str], dict]:
    errors, notes, info = [], [], {}
    m = PHASE_RE.match(phase)
    if not m:
        return [f"phase must look like 'phase-1', 'phase-2'… (got {phase!r})"], notes, info
    n = int(m.group(1))
    for rel in REQUIRED:
        p = root / rel
        tpl = p.with_name(p.stem + ".template.md")
        if not p.exists():
            errors.append(f"{rel} is missing: copy {tpl.relative_to(root)} and fill it in")
        elif is_template(p.read_text(encoding="utf-8")):
            errors.append(f"{rel} still looks like the template (unfilled <placeholders>)")
    for rel in OPTIONAL:
        if not (root / rel).exists():
            notes.append(f"{rel} not found: the proposal will skip competitive evidence")
    now = root / "context/now.md"
    if now.exists():
        as_of, review_by = dates_from_now(now.read_text(encoding="utf-8"))
        info["now_as_of"] = as_of.isoformat() if as_of else None
        if not as_of or not review_by:
            errors.append("context/now.md needs '**As of:** YYYY-MM-DD' and '**Review by:** YYYY-MM-DD' in its header")
        elif review_by < today:
            errors.append(f"context/now.md was due for review on {review_by}: update its bullets, then move the date")
    outputs = root / "outputs"
    prev = previous_proposal(outputs, n)
    if n > 1 and prev is None:
        notes.append(f"no earlier-phase proposal in outputs/: {phase} will be drafted without PREVIOUS")
    info["previous"] = str(prev.relative_to(root)) if prev else None
    info["output"] = str(next_output(outputs, phase, today).relative_to(root))
    return errors, notes, info


def main() -> int:
    if len(sys.argv) != 2:
        print(__doc__)
        return 1
    errors, notes, info = check(ROOT, sys.argv[1], date.today())
    for e in errors:
        print(f"ERROR  {e}")
    for n in notes:
        print(f"NOTE   {n}")
    for k, v in info.items():
        print(f"{k}: {v}")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
