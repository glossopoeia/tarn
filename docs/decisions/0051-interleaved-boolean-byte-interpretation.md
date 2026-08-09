# 0051. Define what a reader returns for a nonconforming boolean byte

- Status: Accepted
- Date: 2026-08-09
- Covers: `[R-SER-08]`'s interleaved boolean byte — whether the writer
  constraint binds as MUST NOT or SHOULD NOT, and what a reader returns
  for a byte outside `{0x00, 0x01}`
- Confirm: none

## Context

§14.2 constrains an interleaved boolean value to `0x00` or `0x01`,
binds writers with MUST NOT, and assigns detection to the verifier.
It then said that such a byte belongs to a nonconforming file "for
which no acceptance obligation and no defined return value exist."

That left a hole. A reader is explicitly not obliged to screen decoded
content, so it can meet the byte without detecting anything — and the
document then said nothing about what it returns. Two conforming
readers handed the same malformed tile could disagree about a sample
value, which is the divergence this format exists to prevent.

The natural-looking fix is to relax the constraint to SHOULD NOT and
let readers read `0x00` as false and any nonzero byte as true. It was
considered and rejected; the reasons are recorded below because the
proposal is an attractive one that will recur.

## Decision

- **The writer constraint stays MUST NOT.** One value, one encoding.
- **The reader's return is now defined.** A reader that neither detects
  the violation nor rejects the tile, and returns the value, MUST
  report `0x00` as false and every other byte as true. This fixes what
  such a reader returns; it does not make the byte conforming, does not
  relieve the verifier, and never arises in a conforming file.
- **Nothing else moves.** The register keeps the violation as a
  verifier row at tile scope. §14.5's padding positions still carry the
  recorded fill byte exactly. `[R-TYP-04]` admits no exception in a
  conforming file, and points at `[R-SER-08]` for the one case that
  arises outside one.

Why the relaxation was rejected, in the order the arguments bite:

1. **The saving is not where the cost is.** §14.2 places an
   interleaved boolean at `u·Q + Fᶜ` — every `Q` bytes. A writer
   building such a tile performs strided stores, so normalising folds
   into a store it already makes. The one case where a bulk copy of a
   raw comparison mask would work is `C = 1, Q = 1`, and §14.4 already
   steers that case to planar, where the plane is bit-packed and gains
   nothing.
2. **Writers must canonicalise anyway.** §14.5 requires the recorded
   fill byte at every padding position of an interleaved boolean
   channel, so any edge-padded tile forces exact bytes already. The
   relaxation would free real positions but not padding ones — a
   stranger rule than the one it replaced.
3. **It is not a local edit.** `[R-TYP-04]` fixes that two values are
   the same value exactly when their bytes are identical. Admitting 255
   encodings of true carves into that, and §13.2 already rejected the
   identical argument for fill, in terms that transfer unchanged.
4. **It buys a two-encodings trap.** Consumers write `== 1` when a
   format promises two encodings, and that test silently reads true as
   false. The burden lands on every consumer of every reader, not on
   the writer that had the information.
5. **It costs detection the document counts on.** §21.7 names three
   places where content is structurally constrained — padding
   positions, pad bits, boolean bytes. `[R-COD-10]`'s mis-strided
   filter is detectable only where the resulting image breaks one of
   them, so removing boolean bytes shrinks what a verifier can catch
   and grows §21.7's undetectable set.
6. **It could not be deferred.** Widening validity is not additive:
   minors never gate (`[R-CNT-07]`), so a reader of this text would
   accept a later file, decline to screen it, and hand a `0x7F` to a
   consumer written against `{0x00, 0x01}`. The change had to land in
   format major 1 or not at all.

## Consequences

An undefined-behavior pocket closes, and the reader's obligation costs
nothing: a conforming file never exercises the rule. The determinism
the relaxation was reaching for is obtained without paying for it —
readers now agree on malformed input, and the canonical encoding, the
padding check, the stride detection and byte reproducibility all stay
as they were.

Priced knowingly: a reader that resolves such a byte does technically
return something other than the stored bit pattern, which is why
`[R-TYP-04]` and §19.4's return step both point at `[R-SER-08]` rather
than leaving a reader to infer the interaction. The rule is stated in
one place and referenced from the others.

Note the asymmetry this exposes, now recorded in §14.2: the parallel
constraint on a boolean *fill* byte (§13.2) needs no such rule, because
`[R-TYP-07]` assigns its detection to the reader with a defined
outcome. Only a violation whose detector is the verifier can be met by
a reader carrying no obligation to act on it, which is the general
shape of this defect and worth checking for elsewhere.

## Precedent

- §13.2's own rationale, which rejected "any nonzero byte is true" for
  fill on the two-encodings ground, and §4.6, which closed the same
  trap for names by making comparison raw bytes with no normalization.
- PNG's approach to values a decoder may meet but not trust: the
  encoder constraint stays absolute and the decoder's behaviour is
  written down, rather than being left to implementations that will
  each choose differently.
- The undefined-behavior worklist in PLAN.md §5, whose whole method is
  that "behaviour undefined" is a defect to be discharged rather than a
  neutral outcome.
