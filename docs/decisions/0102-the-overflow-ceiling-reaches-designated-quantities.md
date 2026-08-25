# 0102. The overflow ceiling reaches designated quantities, and §11.3 stops forming a product

- Status: Accepted (resolves round 26's byte-level ambiguity)
- Date: 2026-08-25
- Covers: `[R-ENC-04]`'s reach; §11.2's `[R-GEO-03]`; §11.3's `[R-GEO-04]`;
  §17.2's Note; §20.3's growth bound list; §22.2's `[R-SEC-02]`
- Confirm: none

## Context

Round 26 returned one byte-level ambiguity, and it was in text no recent round
had touched.

`[R-ENC-04]` binds "any quantity **this specification defines** as a sum or
product of integers obtained from a file (offsets plus lengths, grid counts, tile
counts, sample-position counts, ordinals)". §11.3 wrote Gᵢ · Tᵢ — once, as the
left operand of a comparison, with no name, no gloss and no cross-reference to
§4.2. The bold term §11.3 defines is *padding positions*, not the product.

**The two readings agree wherever every extent is nonzero**, because
N · P = ∏(Gⱼ · Tⱼ) with every factor ≥ 1, so N · P ≥ Gᵢ · Tᵢ and L2's `N·P`
instance already catches any overflow. They diverge only when some dimension has
extent 0, since then N · P = 0 however large another axis's product.

The file that separates them, verified three times independently: rank 2;
dimension a with E₀ = 0 and T₀ = 1, so G₀ = 0; dimension b with E₁ = 2⁶³ − 1 and
T₁ = 2, so G₁ = 2⁶². **G₁ · T₁ = 2⁶³, over the ceiling by exactly one**, while N,
N · P, C · N and `entry_count` are all 0 — every quantity L2 names and every
quantity §19.3 sends a reader to check is in domain. `[R-GEO-02]` says such a
layer MUST be accepted. One conforming reader serves it and returns no samples;
another reports a validity error at layer scope, and `[R-CNF-05]` then bars a
conforming writer from emitting those bytes.

Put plainly: **the array fits and the grid that covers it does not.** Rounding an
extent up to a whole number of tiles can land one position past the ceiling, and
only an empty layer hides that from every check the document names.

## Decision

**The ceiling reaches the quantities the specification designates, and a
designation is express.** `[R-ENC-04]` now says so, and says what follows: an
expression this specification writes only inside a comparison, and names nowhere,
is not a designated quantity and no reader is obliged to form it. The document
already had the pattern — §14.2's `[R-SER-02]` ("These products and sums are
declaration-derived quantities under `[R-ENC-04]`") and §14.3's `[R-SER-07]` both
designate expressly. §11.2's `[R-GEO-03]` now uses the same words in place of
"like all geometry arithmetic", which was the broad hook.

**§11.3 states its condition in a form that forms no product.** Padding exists on
an axis exactly where Eᵢ mod Tᵢ ≠ 0. That is the same condition —
Gᵢ = ⌈Eᵢ / Tᵢ⌉, so Gᵢ · Tᵢ > Eᵢ exactly when Tᵢ does not divide Eᵢ, at Eᵢ = 0
included — and it is the move §11.2 had already made one subsection earlier,
where its Note rejects the idiom (Eᵢ + Tᵢ − 1)/Tᵢ because "whose intermediate sum
can exceed 2⁶³ − 1 … for large extents, even though it fits an unsigned 64-bit
integer" and prescribes ceiling division instead. **Same hazard, same fix, and
the document had already chosen this side of the question without saying so.**

Two restatements are narrowed to match, because each stated the broad reading
outright: §22.2's `[R-SEC-02]` said "Every sum and product taken from a file is
overflow-checked before use", and §17.2's Note said the rule "binds any sum or
product a file yields". §20.3's growth bound takes the same vocabulary. Those
three were what made the broad reading defensible; without them it rests on
"geometry arithmetic" alone, and that phrase is gone.

**The alternatives, and what they cost.** Reading the ceiling broadly would have
made the file nonconforming — rejecting an empty layer `[R-GEO-02]` says a reader
MUST accept, and moving the register from 277 instances to 278 with vectors to
match. Bounding the extent in `[R-GEO-01]` would have made the question moot by
construction, at the price of a normative bound on extents that nothing else in
the format needs, plus a row and vectors. Both reject a file the format was
designed to accept; the decision taken does not.

## Consequences

**The register does not move: 121 conditions, 277 instances, 331 vectors.** L2's
condition cell already read "A declaration-derived sum or product of a layer
exceeds 2⁶³ − 1", so the row and the rule now share vocabulary exactly, and its
nine-instance cell — which never listed Gᵢ · Tᵢ — is correct rather than short.
That the register was already right on this is the strongest evidence for the
reading taken.

One propagation acknowledgement. §14.5's `[R-SER-05]` states what padding content
must *be* and never states when padding exists; it shares only the serialization
idiom that §11.3's unchanged second half also carries.

**On the finding's shape.** The charter told this round that four of the last six
byte-level defects had been quantifier or scope questions; this one is another,
so the run continues rather than breaking. It is not a rule that says the wrong
thing — it is a rule whose subject was left to inference in a document that
elsewhere designates that subject expressly twice. The lesson generalises the way
ADR-0095's did — **where a rule ranges over a class, the class needs a membership
test, not an illustrative list** — and `[R-ENC-04]`'s parenthetical gloss was
being read as one.

## Precedent

- §11.2's Note, which rejected an overflowing idiom for a non-overflowing one
  rather than declaring the layer invalid. It is the same choice, made earlier in
  the same section, and it is why the narrow reading is the document's own.
- §14.2's `[R-SER-02]` and §14.3's `[R-SER-07]`, the express-designation pattern
  this decision makes the rule.
- ADR-0091's rule that a repair which must decide a rule's reach is a decision:
  the options were priced for the maintainer and the reach was chosen, not
  inferred in a repair slot.
