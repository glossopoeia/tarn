# 0109. Round 27's eight checkable repairs, and a closed list restated as a property

- Status: Accepted (resolves round 27's non-byte-level confirmed defects)
- Date: 2026-08-26
- Covers: §21.1's specialization clause; §21.6's sentinel entry; §21.5's R3 and
  R4; §21.2's F21; §21.4's preamble; §20.4's MU = 1 cell; §14.4's layout Note;
  Appendix G item 10
- Confirm: none

## Context

Cleanroom round 27 returned 23 findings over 16 distinct defects. Two were
byte-level and both are questions about a rule's reach, so ADR-0091 sends them
to the ledger (Q-B9, and Q-B7 whose standing changed) rather than to a repair
slot. A third — `[R-SEC-02]`'s unscoped allocation prohibition, reported by four
readers — goes to the ledger too, as Q-C9, because bounding it is a claim about
the whole passage and this week produced two repairs that replaced a false
universal with a narrower false one (ADR-0106).

The eight below are the remainder that are **checkable against a named rule**.
Each is a restatement that lost something the rule it cites still says, or a
claim the rule it cites falsifies. None decides anything.

## Decision

**§21.1's specialization clause stops being a list.** It named F1 of F6 and of
F8, F35 of F36, L24 of L25 — and round 27 found two more it did not name. F21's
condition is an extent slot of (0, 0), so `extent_length` is 0; F22's is an
`extent_length` less than 5. Every file exhibiting F21 exhibits F22, and L10 and
L11 stand in the same relation for a layer sub-record. **Adding two members to a
list just found short is the move ADR-0095 recorded as having failed three
times**, so the clause is restated as the property that decides any pair — where
every file exhibiting one row's condition necessarily exhibits another's, the
narrower row is the one it is recorded against — with the five pairs named as
instances and the list expressly not offered as closed. A closing sentence says
that rows which merely overlap, each reachable without the other, are not in the
relation: F30 and F22 overlap in one of F30's two branches and neither contains
the other, and a reporter proposed them as a pair.

ADR-0106's limit on ADR-0095 applies and was tested: **a property beats a list
only if it is true.** This one is a definition rather than an empirical claim —
it is the meaning of *strict specialization* — which is why it can be stated
without a pairwise sweep of all 121 rows. What a sweep would settle is whether
any pair standing in the relation has a detector or detection point that makes
the narrower row the wrong place to record it. That is left to the repair audit.

**§21.6's sentinel entry regains both of `[R-TYP-08]`'s qualifications.** It read
"every sample position it carries reads as the channel's fill". `[R-TYP-08]`
says a reader returning "any of the tile's sample positions **inside the layer's
extents**" MUST return "**for each channel the tile carries**, that channel's
fill value". The entry dropped the extents restriction and collapsed the channel
quantifier to a singular. It now carries the rule's own words.

**§21.5's R3 and R4 stop registering the same condition.** R4's ground clause
claimed, of all sixteen of its instances, that "a constraint of this row is
broken by what the frame declares rather than by whether the bytes decode".
False of missing frame magic, of a second frame, and of bytes remaining after
the frame — each of which also fails to decode, which is R3's condition. R4 now
states the property true of all sixteen (checkable from the extent's bytes
without relying on a decoder's tolerance) and confines the
declares-while-decoding claim to the instances it holds for. R3 gains the
carve-out it already grants three other encodings, naming R4 as the row for a
frame-constraint failure under encoding 2 whether or not the bytes also fail to
decode. **No instance moves**: R4's Instances column already enumerated missing
frame magic, so the assignment is the one the register had made and failed to
state.

§18.2 is not changed. Its parallel sentence — "A mismatch is one of the frame
constraints R4 registers, not a failure to decode under R3: the bytes decode" —
has its subject fixed by the preceding sentence as the content-size field's
mismatch, one of the instances for which the claim is true. R4's row had
generalised a correctly scoped sentence, which is a row diverging from its rule
and so §21.1's case.

**§21.2's F21 loses a gloss describing an unrepresentable state.** It read
"carries extent slot (0, 0), placing its document inline". §7.1 `[R-CNT-25]` says
a user-metadata record "carries its document in its extent — **never inline** —
and declares the document's encoding in its own inline payload", and `[R-MTA-03]`
fixes that payload at exactly one byte. A record with slot (0, 0) has no document
anywhere, not an inline one. The clause is deleted, which also makes F21 read
exactly as L10 does.

**§21.4's preamble regains `[R-CNF-09]`'s qualifier.** It stated the reject-tile
outcome flatly. `[R-CNF-09]` qualifies it to a rejection the reader is obliged to
detect, and four of §21.4's rows — T2, T4, T5, T26 — carry Detector *verifier*,
where `[R-SER-08]` licenses a reader to return the data. The header now carries
the qualifier and says what governs a verifier-detected row.

**§20.4's MU = 1 cell stops borrowing an anaphor.** "Compaction is barred on the
same ground (`[R-WRT-06]`)" pointed at the nearest antecedent, `[R-CNT-15]`'s
reject-file treatment of a top-level unimplemented MU = 1 record. `[R-WRT-06]`'s
ground is neither that nor file-scope: "such a type can define references this
specification does not (§7.2), so its bytes cannot be safely relocated", and it
reaches a record at **either** scope. The cell now states both.

**§14.4's layout Note is qualified for P = 1.** It said a single-channel bool
layer never produces byte-identical images under both layouts. `[R-GEO-01]`
permits every tile extent to be 1, giving P = 1 and ⌈P/8⌉ = 1 = P, and
`[R-SER-05]` fixes the planar pad bits to the channel's fill — so the two images
are identical when that fill is false and differ when it is true. The Note now
says where the claim holds and what decides the degenerate case.

**Appendix G item 10 drops a false universal.** It said a decomposed name is "a
different name under `[R-ENC-13]` and a different length", and drew a different
`inline_length` and `dir_length` from the length claim. NFD and NFC forms are
frequently the same length — U+1E00 is three bytes in both — and canonical
reordering alone never changes length at all. The item now rests on the bytes
differing, which is what `[R-ENC-13]` actually turns on, keeps `température` as
one worked case rather than the ground of a universal, and drops the two
consequences that followed only from the length.

## Consequences

The register does not move: 121 conditions, 277 instances, 331 vectors, and
`tarn_vectors --verify` reports isolation clean. No cell changes which condition
it registers; F21 and R3/R4 change what they say about conditions they already
registered.

**Thirteen propagation acknowledgements**, which is the largest set this project
has recorded at once and is an artifact of the edit touching §21 in four places.
Every one is a shared row label or a deliberate agreement with a source: the
§21.6 sentinel entry and the §20.4 cell now quote `[R-TYP-08]` and `[R-WRT-06]`
almost word for word, which is the repair rather than a divergence.

**Three of the eight were the same defect in different clothes** — a restatement
that dropped a qualifier its rule still carried (§21.6's sentinel entry, §21.4's
header, §20.4's cell). That is the class ADR-0073 built `tarn_propagate` for, and
the tool cannot see any of them, because none of the three passages changed when
the rule did: they were written short. **A propagation check finds a rule that
moved and left a restatement behind; it cannot find a restatement that was never
right.** Only a reader comparing the two word for word finds those, which is what
the register hunter and the diagram auditor are for, and both found one each this
round.

## Precedent

- ADR-0095's rule that a partition stated by a property beats a list, applied to
  §21.1 — and ADR-0106's limit on it, which is why the property here is a
  definition rather than a claim needing a sweep.
- §21.1's own "where a row and the rule it cites diverge, the rule governs",
  which is the warrant for five of the eight: the row was wrong, not the rule.
- ADR-0091's boundary, which this ADR does not cross — the three defects that
  would have required deciding a rule's reach went to Q-B9, Q-B7 and Q-C9
  instead.
