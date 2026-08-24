# 0090. §21.7's enumerations stop overclaiming, and three register cells name what defines them

- Status: Accepted (dispositions cleanroom round 23)
- Date: 2026-08-24
- Covers: §21.7's account of §20.3 step 4 and of `[R-WRT-06]`; §20.5's
  reserved-range parenthetical; §21.2's preamble and F5; R6's governing-rule
  cell; R8's condition cell
- Revises: nothing; every change here completes or corrects an enumeration
- Confirm: none

## Context

Round 23 returned **zero byte-level ambiguities** — the fourth zero in
twenty-three rounds and the first since round 13 — over 19 findings from seven
reporters, 17 distinct defects after union-find, quiz 15/0/0. The one
self-flagged byte-level finding was downgraded by all three triage passes and
the refute phase upheld the downgrade.

Five of the seventeen land on **§21.7**, and that is the round's signal. §21.7
is the section that accounts, by class, for what no check detects. An
enumeration there is not a convenience: it is a claim that the listed cases are
the cases, and a reader who trusts it will conclude a witness exists where none
does. Three of the five are exactly that — an "only where" that the same
sentence falsifies two clauses later, a bar whose four items are accounted for
in three, and a witness asserted unconditionally that a writer can construct
around.

Three more are register bookkeeping, and one of those turned out to be a finding
about this project's own habit rather than about the register.

## Decision

**§21.7's account of §20.3 step 4 is restructured.** The old sentence read
"witnessed only where the affected tiles remain stored *and* the change reaches
a byte §14 structurally constrains", then named witnesses for two changes that
reach no such byte. Only the first conjunct is exclusive, and it now says so:
witnessed only where the affected tiles remain stored, **and then only for part
of what the step bars.** The three witnessed cases are stated as separate
sentences rather than semicolon clauses, so no "only" reaches across them.

**The codec witness is no longer asserted unconditionally.** A change reaching
the codec is *sometimes* witnessed by the rows for the codec now declared, or by
T14 where the new declaration is codec 1 — "but neither is assured: a writer can
choose stored bytes that satisfy the old declaration and the new one alike."
Both halves are constructible around. Raw DEFLATE of tuned data lands exactly on
the decoded size, so a codec 2 → 1 re-declaration exhibits no T14; and under
codec 1 the stored bytes are an arbitrary tile image, so a writer can make them
a valid zstd frame decoding to exactly the decoded size and re-declare codec 3
with nothing firing.

**The filter and the sample offset are named as unwitnessed.** §20.3 step 4 bars
four things and §21.7 accounted for three, carrying the codec across from "the
codec and filter that produced the stored bytes" and dropping the filter — the
analogy shape check 7 exists for. Neither filter value can fail: filter 1 is the
identity and filter 2 is a permutation defined for every input whose length is
divisible by the mandated stride, which §17.3 makes always the case. A change
moving a sample's byte offset without changing the image's length is likewise
unwitnessed.

**`[R-WRT-06]` has four trailer obligations, not two.** §21.7 named the
ignore-lane bits and the version_minor floor and called them "two obligations on
a compacted file's trailer". The fresh `file_id` draw and the generation are the
other two, and both are unwitnessed for the same reason — a compacted file
standing at generation 7 carrying its input's `file_id` passes every check §6.2
states, because **the output carries no record that it is a compaction output at
all.** That last clause is added, since it is the fact all four rest on.

**§20.5's reserved-range parenthetical is completed.** "(F36, L25, R1)" named
one of the seven identifier spaces §10.2 tabulates. It now reads: F36 and L25
for a record type, and one row for each of those spaces — L31, L33, L34, L36,
L43, L45, R1. The omission was not idle: §12.2's Note pins sample types 14
through 19 to named future assignments, which makes a reserved sample type the
most concrete instance of "a feature a later minor defines" in the document, and
its row is L34.

**F5 is a fifth row reaching a foreign-major file.** §21.2's preamble named four
rows outside its version-gate reasoning, on the ground that their subject is a
field fixed across every major. `[R-CNT-27]`'s 128-byte floor is outside that
order for a different reason, now stated: **it precedes the order rather than
sitting in it** — a file shorter than 128 bytes has no trailer to read a magic, a
CRC or a version from, so the floor is established before any field the gate
consults exists.

**R6's governing-rule cell names the rule that defines it.** §21.1 fixes what
the cell is for — "the requirement that defines it" — and R6 cited `[R-CNT-25]`,
which assigns an outcome and states no key rule, with `[R-ENC-12]`, which
expressly excludes document keys from its own scope. R6 and R10 come from one
clause of `[R-MTA-04]`; R10 already cited it and R6 now does too, as
`[R-MTA-04]` (R-CNT-25, R-ENC-12). Its four vectors are re-emitted against the
new rule.

**R8 keeps one instance, and the register now says why.** The reporter argued
that `1e400` and the bare `NaN` token have materially different shapes and
should be enumerated separately under §21.1's criterion. The counter-argument
already existed and was correct — but it lived in a comment in
`conformance/tools/vectordefs/r_rows.py`, which no reader of the specification
can see. **That is the same failure ADR-0089 closed in three other places**: a
document that cannot show its own reasoning. R8's condition cell now carries it:
the two are one instance because a document carrying a bare token is not
well-formed JSON either, so no file exhibits R8's predicate alone through one
(§21.1's distinguishability test, R7).

## Consequences

The register does not move: 121 conditions, 277 instances, 331 vectors. Four
vectors are re-emitted under R6's corrected rule; no vector is added or removed.

Nine editorial findings and five design-decision findings are **deferred, not
fixed**, each with a named owning section — the disposition ADR-0034 permits.
The five design decisions become ledger entries rather than spec text, per
AGENTS.md rule 3: a format capability question gets an entry with options before
it gets a decision.

Three propagation acknowledgements recorded, covering five flagged sites.

**What this cycle is a test of.** G3 requires a round to return zero *and* the
next round, reading that round's repairs, to return zero too. Rounds 7, 9 and 13
each hit zero; rounds 8, 10 and 14 each found the next defect in the repairs the
zero produced. These are those repairs, and round 24 is the fourth attempt at
the second half of the criterion. They were deliberately kept narrow — the §21.7
cluster and the register cells — with everything else deferred, so that the
surface round 24 reads is the smallest one that still fixes what round 23
actually found.

## Precedent

- `[R-CNF-01]`, which is why a reason living in a Note carries no force — and,
  by extension, why a reason living in a build script carries none either.
- §21.1's distinguishability test, which is what holds R8 at one instance and
  what the register now cites for it.
- ADR-0089's finding that a repair can be correct while the document cannot show
  why, of which R8 is the fourth instance and the first found by a round rather
  than by an audit.
