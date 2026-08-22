# Cleanroom round 21 — findings

Protocol: ADR-0034, four phases, preceded by the repair audit in
[repair-audit.md](repair-audit.md). Charter: [prompt.md](prompt.md).

## Verdict

**Two byte-level ambiguities. G3 is not met** — and this is the first increase
since round 17.

| | |
|---|---|
| Quiz | **15 agree / 0 diverge / 0 underdetermined** — fifteenth round running |
| Findings | 21 |
| Self-flagged byte-level | 2 |
| Distinct defects | **21** — 2 byte-level, 2 design-decision, 6 register-bookkeeping, 11 editorial |
| **Byte-level after triage and the refute phase** | **2** |
| Harness | clean: 13/13, 0 errors, every `transcript_finding_count` matching, all three passes echoing all 21 ids with no gap, duplicate or extra |

Byte-level history: … → 1 → 1 → 1 → 1 → **2**.

**The reader walk returned zero findings at high confidence** — the first time
any implementer walk has come back empty in this project.

## Survivor 1: the per-tile guarantee over a layer that addresses no tile

Unanimous — all three passes graded it byte-level independently.

The writer's creation walk emitted a schema-first layer: dimension extent 0,
tile extent 2³¹, one uint8 channel, interleaved. §11.2 gives it **zero
addressed tiles**, while its declaration-derived decoded size is
P·Q = 2³¹ = 2048 MiB — **eight times** §21.9's 256 MiB per-tile guarantee. §19.3
obliges a reader to derive that quantity at layer access, and §17.2's Note
confirms it is computed even in an empty layer.

- **Reading A** — the row ranges over *addressed* tiles, as §17.2's Note
  explicitly quantifies `[R-COD-07]`'s lz4 cap. No tile exists, so no quantity
  exceeds the table, and a reader declining on resource grounds "declines on
  that ground a file whose every quantity lies within the table" — and is
  **not a conforming reader**.
- **Reading B** — the declarations do yield 2048 MiB, and `[R-ERR-04]` licenses
  declining "at the narrowest scope whose declarations exceed what it can
  serve".

Same file, opposite answers to whether the reader is conforming.

## Survivor 2: `Frame_Content_Size` — in the passage this session just repaired

Two passes byte-level, one not; the refute phase attacked the split and the
finding survived.

For a **tile**, `[R-COD-06]` pins it: "The frame content-size field MAY be
present; when present it MUST equal the tile's decoded size, a reader MUST treat
a mismatch as a validity error at tile scope" (T22). For a **document**,
`[R-MTA-09]` withdraws that constraint — correctly, there being no declared size
to compare against — **and puts nothing in its place.** The carried-over list is
closed and enumerated, and R4's Instances cell enumerates exactly those six
alternatives plus "bytes remaining after the frame". FCS is in neither.

So for a frame declaring FCS = 999 whose decode produces 100 bytes, the only
rule left is R3, "fails to decode" — and whether the bytes fail to decode is now
**a property of the decoder, not of the bytes**, against `[R-CNF-02]`'s
statement that file conformance "is a pure predicate on bytes". The refuter
built the concrete 20-byte extent.

**This is ADR-0085's passage, and ADR-0085's shape.** That repair pinned the
*window* and left the *content size* unpinned — one quantity named where two
were in play. The round-21 charter had warned, in terms, that §18.2 is "the one
place this document has repeatedly found itself with a rule that names one
quantity where two are in play." The charter predicted its own next defect, and
the repair audit that read that repair did not catch it, because it was auditing
what the repair said rather than what the frame header still left open.

## A harness semantics wrinkle, disclosed by the refuter

The refute trigger fires on split verdicts as well as unanimous downgrades, and
here it fired on a group two passes had **upheld**. The refuter flagged that
there was no downgrade quotation to overturn, read the operative instruction as
"attack the premise", and returned `DOWNGRADE_REFUTED` to record that byte-level
status survived. The verdict vocabulary assumes a downgrade; on the split path
it should say which side the refuter attacked from.

## Disposition

Both survivors need a maintainer decision. Survivor 2's fix is the same move
ADR-0085 made for the window, applied to the quantity it missed. Survivor 1 is
a quantifier question on §21.9's table — whether its per-structure rows range
over structures the file *addresses* or over what its *declarations derive* —
and it may reach more rows than the tile one.

Register and corpus unchanged: 121 conditions over 273 instances, 327 vectors.
