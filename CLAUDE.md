# proposal: project instructions

- **Purpose:** generate a phase's platform proposal with `/generate-proposal <phase>`. Read `README.md` first.
- **Read `context/` and `inputs/`; write only to `outputs/`.** Never edit the user's context or
  input files while generating; if one looks wrong or stale, say so.
- **Never overwrite an output.** `tools/check.py` picks the next free name.
- **Only templates are committed.** `context/*.md`, `inputs/*.md` and `outputs/*` are gitignored;
  never add them to git.
- **Evidence:** every claim cites an input; no quotes and no attribution to people; never invent a
  number, date, name or owner. Missing facts become questions or pre-send checks.
- **Keep the scaffold generic.** Company- or market-specific wording belongs in the user's context
  files, not in `prompts/`, `tools/` or the templates.
- **Tests:** `python3 -m unittest discover -s tests -t .` after changing `tools/`.
