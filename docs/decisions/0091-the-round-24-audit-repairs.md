# 0091. ADR-0090's F5 addition is reverted, and three of its claims are corrected

- Status: Accepted (resolves the round-24 repair audit's confirmed findings)
- Date: 2026-08-24
- Covers: §21.2's preamble; §20.5's reserved-range parenthetical; §21.7's filter
  clause and its `[R-WRT-06]` reason; R8's instance-collapse ground
- Revises: four claims ADR-0090 wrote, one of which is reverted outright
- Confirm: none

## Context

The repair audit that precedes round 24 read ADR-0090's four hunks — 35
insertions, 20 deletions, all written in one sitting. Three auditors returned
**15 findings, none self-flagged byte-level.** Verification returned 7
CONFIRMED, 4 PARTIAL, 4 REFUTED; a refute pass over the three downgrades
overturned two of them. **No finding at any stage was byte-level.**

**Every confirmed defect is in text ADR-0090 wrote the previous day**, which is
this project's measured base rate rather than a surprise: rounds 8, 10 and 14
each found the next defect in a clean round's repairs. The audit found these
before a round did, which is what it is for.

The F5 addition is the instructive one. Round 23's `verifier-01` reported that
`[R-CNT-27]`'s 128-byte floor has no position in §6.2's validation order, and
offered two readings. ADR-0090 chose one and wrote a warrant for it. **The
audit falsified that warrant three independent ways:**

- `[R-CNT-27]` contains no ordering language at all — no "before", no "first",
  no "in order". It was cited for a proposition it does not carry.
- The physical claim — that a file shorter than 128 bytes "has no trailer to
  read a magic, a CRC or a version from" — **is false for every file of 64 to
  127 bytes.** §6.2 puts the trailer in the final **64** bytes and §19.1 step 2
  fetches `[F − 64, F)`. At F = 100 the magic, version and CRC sit at offsets
  36, 44 and 96, all inside the file.
- `[R-RDR-02]` fixes only the *latest* detection point and then says "A reader
  MAY detect any violation earlier". Detection order is therefore a reader's
  option, so **no row's reach can be established by procedural priority at
  all** — which reaches the preamble's existing four rows as well.

That last point is why the answer is a revert and a ledger entry rather than a
better warrant. A repair slot is not where a question with two defensible
readings gets decided, and ADR-0090 decided one there.

## Decision

**The F5 addition is reverted.** §21.2's preamble returns to four rows, exactly
as it stood. The question round 23 raised is genuinely open, is now wider than
round 23 knew, and becomes **Q-H4**: which register rows reach a file declaring
a foreign major, and can detection order settle it at all given `[R-RDR-02]`'s
permission? Three options are priced there, including one that decides reach by
a rule's *subject* rather than by when it is checked.

**§20.5's parenthetical says "the other seven".** §10.2 tabulates **eight**
identifier spaces — record type, channel layout, linearization, sample type,
codec, filter, index encoding, metadata encoding. ADR-0090 wrote "one row for
each identifier space §10.2 tabulates" and then listed seven, having already
covered the eighth (record type) by F36 and L25 in the preceding clause. The
count is now stated correctly; the seven rows and their spaces map one for one.

**§21.7's filter clause takes T26's terms.** ADR-0090 wrote that a change
reaching the filter "has no witness at all". T26 registers exactly this: "Filter
2 applied at a stride other than the mandated one, **where the resulting image
breaks §14.5's padding content or `[R-SER-08]`'s bool bytes** (a wrong stride
with no such structural constraint is undetectable, §21.7)". The claim is
replaced by T26's own formulation — witnessed where the image breaks a byte §14
constrains, unwitnessed where it breaks neither — which is also what §21.7
already says twenty lines above for a mis-ordered image, "witnessed by T2, T4 or
T5, exactly as a mis-strided filter is". Two auditors reported this
independently, a verifier refuted it, and the refute pass overturned that
refutation.

**`[R-WRT-06]`'s four obligations share one reason.** ADR-0090 gave the reason
as "the output carrying no record of its input's `file_id`, generation, flags or
minor" — which is the wrong reason for two of the four, since the obligations on
`file_id` and generation are about the *output's* values, not the input's. The
shared reason is stated instead: **the output carries no record that it is a
compaction output at all**, so no check can know that any of the four was owed.
The ignore-lane bits and the version_minor floor are unwitnessed twice over, the
input's flags and minor being unrecorded as well.

**R8's instance-collapse cites the right limit.** ADR-0090 justified holding R8
at one instance by "§21.1's distinguishability test". §21.1 states no such test;
its criterion is whether members give the condition **materially different
shapes**, and by that criterion `1e400` and a bare `NaN` token *are* different —
the reporter was right about the shape. The real ground is that a bare-token
document is not well-formed JSON either, so the second is exhibitable only as a
co-violation of R7. That is `[R-VEC-02]`'s co-attribution limit, where L50's
fourth instance already sits, and the cell now says so — including that the two
do **not** share a shape.

## Consequences

The register does not move: 121 conditions, 277 instances, 331 vectors. No
vector changes.

`B-02` — that R6 and R5 now name opposite governing rules — was **refuted**, and
R5 is left as it stands. `X-02`/`B-04` — that §20.5's "Neither obligation" now
disagrees with §21.7's four — was downgraded and the refute pass upheld the
downgrade: "Neither" is a two-place quantifier scoped over the two obligations
immediately preceding it, so there is no contradiction. Neither is repaired.

Two propagation acknowledgements recorded.

**What this cycle demonstrates about repair slots.** Four of ADR-0090's eight
repairs were correct; three were wrong in ways a careful reader catches, and one
decided a design question that should have gone to the ledger. The audit caught
all four before a round read them. The rule this yields is narrower than "be
careful": **a repair that must invent a warrant is a decision, not a repair**, and
it belongs in OPEN-QUESTIONS.

## Precedent

- `[R-RDR-02]`'s "A reader MAY detect any violation earlier", which is why
  procedural priority cannot settle a row's reach and why Q-H4 is wider than the
  finding that prompted it.
- T26, which already stated the filter's witness condition in the terms §21.7
  now adopts.
- `[R-VEC-02]`'s co-attribution limit and L50's held fourth instance, which is
  the actual ground for R8's collapse.
- AGENTS.md rule 3 — a question with options belongs in the ledger before it
  belongs in the text.
