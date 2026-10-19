# Generate a platform proposal

You are drafting an internal proposal for **{PHASE}** of a shared platform, written by the
platform's PM for their VP. The audience is executives: lead with the answer, keep it to roughly
1,500–2,200 words, and use tables wherever they're clearer than prose.

## Inputs

| Name | File | Use it for |
|---|---|---|
| **BRIEF** | `inputs/brief.md` | The structure and the questions the proposal must answer. Where it conflicts with a rule below, the brief wins |
| **COMPANY** | `context/company.md` | Framing. Its constraints are hard rules |
| **HYPOTHESES** | `context/research-goals.md` | The "closes" column and the risks (H-numbers) |
| **NOW** | `context/now.md` | Every fact about teams, consumers, dates, capacity and decisions. Bullets under a heading feed that section first |
| **GAP_REGISTER** | `inputs/gap-register.md` | The candidate scope |
| **COMPETITIVE** | `inputs/competitive.md` (optional) | The competitive "why now", gaps, scope edits, metrics |
| **PREVIOUS** | the latest earlier-phase proposal in `outputs/` (phases after the first) | Starting scope: what it deferred, its open risks, its pending designs |

## Evidence rules

1. **Cite every claim** to an input and section, for example `(GAP_REGISTER row 2b)` or `(NOW: North Star)`. If no input supports a claim, leave it out or list it under "Things to check before sending."
2. **No quotes and no attribution to people.** NOW holds the author's own observations: state them in the author's voice, never "per <name>" or in quotation marks. Teams and roles can be named where the proposal needs an owner ("the engineering lead", "the <product> team"). Only text copied from BRIEF or another input file goes in quotation marks.
3. **Never invent a number, date, name or ownership.** Missing facts become questions or pre-send checks.
4. **When inputs conflict, the newer one wins**, and the conflict goes under "Things to check before sending." NOW → OVERRIDES bullets beat the gap register.
5. **Rival facts come only from COMPETITIVE.** Keep the home company's internal plans out of any claim about what's shipped.
6. **Regulations and standards** named in the proposal must come from an input. If an input flags one as uncertain, hedge it in the text and list it under pre-send checks.

## Decision rules for any phase

Apply these in order, and give the reasoning in one line wherever the proposal states a choice.

1. **Scope.** Group candidate gaps into **at most four shared capabilities**. A gap belongs in scope if any of these is true:
   - it's a gate that blocks shipping (an audit record, data isolation, a trust boundary named in COMPANY);
   - every consuming team would otherwise rebuild it;
   - COMPETITIVE shows rivals ship it, and its absence blocks a "where we could win" play.

   Exclude anything that is one team's feature, cross-product orchestration, or a build the platform team doesn't own. List every exclusion under "Out of {PHASE}".
2. **Fund first:** the capability every consumer's traffic passes through, plus the record it writes, built once, unless NOW records a different decision.
3. **What it enables:** exactly **three** business outcomes, each with a "how we'll know" measure.
4. **Must-haves:** testable checks, phrased "X for every Y", including any the COMPETITIVE edits add.
5. **Not go-dark:** four steps, each ending in something an executive can see (a demo, a report), with who sees it.
6. **Risks, ranked:**
   1. things that block shipping;
   2. adoption (teams not moving onto the platform);
   3. dependencies on other teams;
   4. engineering capacity;
   5. overlapping ownership;
   6. collisions with other launches.

   Each risk gets an early test and a posture for this phase.
7. **North Star.**
   - **Metric:** consumers (agents, workflows) in production on the platform. One counts only with real traffic, 100% of its traffic through the platform, and a complete record for every decision.
   - **Companion metrics:** teams with ≥2 consumers live ("one is a trial; two is behavior"), and platform cost per unit of business value (the unit from NOW → North Star).
   - **Targets:**
     - next period-end = the consumers NOW shows in production by then;
     - the period after = that, plus the consumers NOW shows starting build before it;
     - state the demand count from NOW → North Star, and each target as a share of it.
   - **Doesn't count:** repos, pilots, proofs of concept.
   - **What would change the numbers:** list it.
8. **Competitive edits.** Apply every edit in COMPETITIVE that fits rule 1 and the phase defaults. Say which ones you didn't apply and why. Add one "Why now" point from COMPETITIVE.
9. **Effort.** No estimate unless NOW → Header contains one from the engineering lead. Say so in the header.
10. **Questions** (6–8, to the BRIEF's author). For each, privately list the answers it could get. Keep it only if at least one answer would change the plan.

## Phase defaults

**First phase** (no PREVIOUS):
- **Acting vs. reading:** if NOW doesn't show delegated access solved, the phase is **read-only**, plus a written design for write access. The design gets a target date, flagged "to confirm with the engineering lead." Use the gated-write patterns in COMPETITIVE if it has them.
- **First tenant:** the consumer NOW shows in production or closest to it. Protect its launch: run it in shadow mode through the platform first, and cut over after its launch date.

**Later phases** (PREVIOUS exists):
- **Starting scope:** PREVIOUS's "Out of" list, its pending designs (for example the write-access design), its unresolved risks, plus gap-register rows still open. Re-apply rule 1 to that set.
- **What changed:** open with a short "Since <previous phase>" table: what shipped (from NOW), what moved, what was dropped and why.
- **Targets** continue from PREVIOUS's North Star counts. Explain any reset.

## Output

Write in this shape:

```
# Platform: {PHASE} Proposal (draft)
From / date / status / engineering lead / effort-estimate note / inputs used (with NOW's "as of" date)
## In one paragraph            (capabilities → what they enable → fund first → where the risk is)
## Since <previous phase>      (later phases only)
## Why now                     (3–5 bullets, cited)
## {PHASE}: what it delivers   (table: capability | what it is | closes: gap rows · H-numbers) + Out of {PHASE}
## What it enables for the business   (3 items, each with "how we'll know")
## Must-haves                  (checklist)
## Recommendation: what to fund first (ordered)
## Not a go-dark build         (table: step | what you see | who sees it)
## Highest-risk items          (table: risk | why it matters | how we find out early | posture this phase)
## North Star                  (definition, companions, the count table, demand, why these numbers, input metrics, what would change them)
## My questions                (numbered, each with one line of why)
## Appendix: sources           (input → what it supported)
Things to check before sending (conflicts, unconfirmed dates, regulations or standards to verify)
```

## Before you finish, check

- Every number, date and name traces to an input.
- Nothing is in quotation marks except text copied from an input file.
- Every rule above is visibly applied.
- Every candidate gap is either in scope or listed as out.
- Everything a rule told you to check is under "Things to check before sending."
