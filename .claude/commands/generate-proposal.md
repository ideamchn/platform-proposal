---
description: Generate a platform proposal for a phase from context/, inputs/ and (for later phases) the previous proposal
argument-hint: "<phase> (e.g. phase-1, phase-2)"
---

Generate the **$ARGUMENTS** proposal.

1. Run `python3 tools/check.py $ARGUMENTS`. If it prints any ERROR, stop and show the errors; don't
   draft anything. Show NOTE lines and carry on.
2. Read `prompts/generate-proposal.md`, replacing `{PHASE}` with a readable form of the phase
   (`phase-2` → "Phase 2"). Follow it exactly.
3. Read every input it lists. Read the `previous` file the check printed, if any.
4. Write the proposal to the `output` path the check printed. Never overwrite an existing file.
5. Show me:
   - the "In one paragraph" summary;
   - the North Star targets;
   - the "Things to check before sending" list;
   - the output path.
