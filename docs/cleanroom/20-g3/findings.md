# Cleanroom round 20 — findings

Protocol: ADR-0034, four phases, preceded by a repair audit. **The first round
whose agents read an uncontaminated context** (ADR-0084). Charter:
[prompt.md](prompt.md).

## Verdict

**One byte-level ambiguity. G3 is not met.** Third round running the survivor
is in text no recent round touched — and this one is the constructive
adversary's first survivor in many rounds.

| | |
|---|---|
| Quiz | **15 agree / 0 diverge / 0 underdetermined** — fourteenth round running (Q08's difference was "CRC-32C **of** trailer bytes" against "**over** trailer bytes") |
| Findings | **20** — the lowest raw count of any recent round (44, 26, 20) |
| Self-flagged byte-level | 1 |
| Distinct defects | **16** — 1 byte-level, 6 design-decision, 3 register-bookkeeping, 6 editorial |
| **Byte-level after triage and the refute phase** | **1** |
| Harness | **clean**: 13/13, 0 errors, every `transcript_finding_count` matching, all three passes echoing all 20 ids with no gap, duplicate or extra, every walk `confidence: high` |

Byte-level history: 5 → 4 → 4 → 3 → 3 → 5 → 0 → 2 → 0 → 1 → 1 → 1 → 0 → 1 →
1 → 1 → 1 → 1 → 1 → **1**.

## The access-rule clause worked, and was tested

Two agents disclosed the runtime injection unprompted and said they acted on
none of it. The quiz author went further and volunteered the one place it
brushed its work: it had counted §21's rows and instances from the document,
then recognised afterwards that the injected index carried a similar figure —
and reported the count it computed, noting it is checkable from the document
alone. **That is the clause doing exactly what it was written for**, including
the part that is hardest to get from an instruction: disclosing a near-miss
nobody would have detected.

## The survivor: a metadata zstd window above the guaranteed floor

§18.2 makes encoding 2 "exactly one RFC 8878 compressed frame" but explicitly
withdraws §17.2's window constraint, which is stated "against a tile's declared
decoded size" — a document has no declared size. So a user-metadata frame's
declared `Window_Size` is **unconstrained**, while §21.9 guarantees a conforming
reader only **8 MiB**. Nothing says whether a reader that cannot decode such a
frame has established §21.5's R3 violation or hit its own capability bound.

The adversary built two conforming 128-byte files differing only in the
Window_Descriptor byte. **The refuter then rebuilt it at minimal gap** —
`0x68` is windowLog 23, exactly 8 MiB; `0x69` is 9 MiB — so the answer cannot
turn on the size of the excess. **One bit of a mantissa field separates a file
every conforming reader MUST accept from the disputed one**, and the two
readings give it opposite verdicts: *nonconforming* under R3, *cannot
establish* under the capability reading.

One triage pass upheld it, two did not; the refute phase attacked the split and
returned DOWNGRADE_REFUTED — declining to treat the pass's prose as the target
and instead rebuilding the construction independently.

**This is the constructive adversary role finally paying out.** It has returned
empty or refuted-from-the-text for most of this project's history; PLAN.md
records it trying 23 attacks in round 5 and refuting every one.

## Disposition

The survivor needs a maintainer decision — whether §18.2 gains a window bound
for metadata frames, or §21.5/§21.9 say which side of the
violation/capability line a window above the floor falls on. `[R-MTA-09]`
already settles the *size-bound* decline as a capability, which is the obvious
model. **No repair made this round.**

Register and corpus unchanged: 121 conditions over 273 instances, 327 vectors —
recomputed mechanically by the quiz author (36+49+26+10 rows), along with every
published checksum constant.
