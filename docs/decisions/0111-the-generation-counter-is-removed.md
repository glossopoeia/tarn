# 0111. The generation counter is removed, the trailer is reordered, and a struck row label is retired

- Status: Accepted
- Date: 2026-08-31
- Covers: §6.2's trailer layout and `[R-CNT-06]`; §3.1's *generation* term;
  §9.2, §9.3 and §9.6; §20.1–§20.5; §21.2, §21.7 and §21.8; §22.5; §23.2;
  §24's `[R-VEC-02]`; Appendices A, D, G and H;
  `conformance/tools/tarn_build.py` and the vector corpus
- Confirm: none

## Context

The trailer has carried a u64 `generation` at offset 16 since the format was
drafted: 1 ≤ g ≤ 2⁶³ − 1, increasing by exactly 1 per commit, paired with a
nonzero `file_id` drawn at creation. The maintainer asked what removing it would
cost. Six spec-only analyses priced three readings of the question and three
cross-cutting specialists took all three; a seventh synthesised them.

**The counter has exactly one consumer.** A census of every comparative use of
the value found ten. Nine are the counter maintaining or naming itself — §9.2
step 5 and §20.3 step 6 incrementing it, §9.3 defining its increment, §20.5
stamping a compacted file, Appendix G item 4. The tenth is `[R-LIF-03]`'s
revalidation: "same generation, everything cached remains valid; higher
generation, refetch the directory; different file_id or lower generation, treat
as a different file." §6.4's remote-open accounting never mentions it; §9.6's
recovery scan keys on position and `committed_file_length = o + 64`; §9.5's
snapshot consistency rests on `[R-LIF-01]`'s immutability, not on the number.

**What the counter is load-bearing for is narrower still**: deciding, from a
fixed-size tail read, whether a previously fetched *directory* is still live.
That is `[R-LIF-03]`'s middle arm. The claim that cached *ranges* stay
byte-correct is carried by `[R-LIF-01]` and never depended on the counter.

**`committed_file_length` already does the job.** F is strictly increasing per
commit within one `file_id`, and the derivation is the document's own:
`[R-LIF-02]` step 1 begins writing at exactly F; §9.2's first Note forbids
discharging step 3 with an earlier generation's directory; `[R-CNT-06]` gives
`dir_length ≥ 4` and `dir_offset + dir_length ≤ F − 64`; step 5 pads to the next
64-byte boundary and appends the 64-byte trailer; §6.2 makes F a multiple of 64.
Hence **F_new ≥ F_old + 128**. F sits at trailer offset 40, inside the same
64-byte read revalidation already costs, inside the trailer CRC, and gated
harder than `generation` ever was — by `[R-CNT-06]`, `[R-CNT-10]`, F5, F13 and
F17. So `(file_id, F)` names a generation exactly, which is what the counter
supplied.

**The claim was entailed and nowhere stated.** `grep -ci "monoton"` returns 0
and "increasing" occurs once, at §9.3, bound to the counter. Re-keying a rule
onto a quantity the document does not fix is this project's most repeated defect
(ADR-0099), so the monotonicity is now **stated normatively** in `[R-LIF-02]`,
where the steps that force it live, and derived in a Note beneath the Note it
depends on.

### Why the trailer stays 64 bytes

The maintainer asked, correctly, whether anything *substantively* requires 64 —
"because the trailer is defined to be 64 bytes" being no reason. Nothing does:
Appendix D argues for a **tail-anchored** trailer and is silent on its size, and
a 56-byte trailer keeping its 64-aligned start (F ≡ 56 mod 64) is coherent.

It stays 64 because shrinking converts a reusable resource into nothing.
`[R-CNT-24]` makes the trailer the only fixed-position structure in the format
and caps what any future major may put there: "A future major MAY redefine only
the remaining 48 trailer bytes and MUST NOT grow the trailer." Deleting the
counter and keeping 64 leaves 48 redefinable bytes with **8 of them now
unspent** — banked. Shrinking to 56 leaves 40, spending a sixth of the format's
permanent fixed-position budget to save 8 bytes per file, against a format whose
smallest conforming file is 128 bytes and whose stated target is O(1) remote
open. The saving is unmeasurable; the loss is permanent.

That 64 is a power of two is a secondary virtue and was not the reason.

## Decision

**The `generation` field is removed and the trailer is reordered so its reserved
bytes are contiguous.** `dir_offset`, `dir_length`, `committed_file_length` and
`file_id` each shift back by 8; the reserved run becomes 12 bytes at offset 48;
the CRC stays at offset 60 over [0, 60). `[R-CNT-24]`'s permanent anchors are
untouched — magic at F − 64, version at F − 56, CRC at F − 4 — so nothing about
cross-major identification changes, and "every byte is assigned" stays true,
*reserved, MUST be zero* being an assignment the table already used at offset 56.

The reorder also keeps `[R-CNT-06]`'s "reserved bytes zero" a **single** clause
covering one contiguous run. `[R-CNT-06]` therefore states **nine** conditions
where it stated ten, and §2.3's reach argument, which cites that count, follows.

**`[R-LIF-03]` is re-keyed onto `committed_file_length`**, with the three arms
unchanged in form: same F, everything cached remains valid; higher F, refetch the
directory; different `file_id` or lower F, treat as a different file.

**Two capabilities are lost, and the document says so rather than hiding it.**

- **The commit count.** F counts bytes, never commits. §23.2 disclosed
  "generation count" as part of the shape of a file's history; it no longer can.
  That is a privacy improvement, and §23.2 now states what is and is not
  disclosed.
- **§9.6's rollback token.** "Rollback detection requires out-of-band state (an
  expected generation or a detached hash)" named the counter as the cheap
  anchor. An expected-F check is **not** a substitute: placement within a commit
  is free (`[R-SLB-05]`) and slack is unconstrained (`[R-CNT-21]`), so a party
  that truncates to an earlier commit and re-appends can return the file to any F
  at or above the expected one while serving rolled-back content. §9.6 now says
  no field of the format supplies the anchor, and names what does — a detached
  hash over the committed prefix, a signed `(file_id, committed_file_length)`
  pair held elsewhere, or an append-only transport that refuses a shortened
  object.

**A struck register row's label is permanently retired, not renumbered.** F11
("Trailer generation is 0") is struck. §24's `[R-VEC-02]` said "row labels are
positional and renumber when a row is struck"; that is the only site in the
document making the claim, and it is reversed. A label now names the same
condition for the life of the major, exactly as §2.2 fixes a requirement
identifier — "a withdrawn requirement leaves its identifier permanently retired"
— and as §14.4's Note records for the withdrawn `[R-SER-04]`.

This was decided on its own merits and is separable from the rest. Renumbering
would have moved 25 labels and 13 cross-references at 11 sites for no design
benefit, and would recur on every future strike. It also repairs a defect the
analysis exposed: `[R-VEC-02]` offered the (label, identifier) pair as what
survives a renumbering, but F8 through F17 all cite `[R-CNT-06]`, so after this
strike the pair would not have disambiguated across six rows.

## Consequences

**The register moves**, for the first time in this project's history by removal:
121 conditions over 277 instances becomes **120 over 275** — F11's row and its
single instance, and one instance from F2, whose cell enumerated `generation`
among six u64 fields. §21.2's preamble reads 35 conditions. F15's cell changes
from "The 4 reserved bytes at trailer offset 56" to the 12 at offset 48. The
counting method was validated by reproducing the current totals exactly before
the new ones were computed.

**Appendix A changes byte for byte.** The file stays 128 bytes; the trailer's
interior moves and its CRC-32C becomes **0x402F157E**, from 0xE00938D2. The value
was computed with an implementation first validated against Appendix B's
CRC-32C("123456789") = 0xE3069283 *and* against the current printed trailer.

**The corpus rebuilds rather than being edited**, and shrinks from 331 vectors
to **329**: TV-0123 (F11) and TV-0930 (F2's `generation` instance) retire, their
only content patch having been to a field that no longer exists. `tarn_build.py`
generates every vector, so the trailer emitter, its offset map and its
`generation` parameter change once and the corpus follows. Coverage holds at
120/120 rows and 275/275 instances.

**Two things the plan did not anticipate, both found by checks rather than by
reading.**

The first is a policy collision. `tarn_check.py`'s REG-01 required §21 row ids to
be contiguous — it encoded the very positional-label rule this ADR reverses — so
retiring F11 made the build fail on the decision it implements, and the obvious
way to "fix" the failure would have been to renumber. REG-01 now consults a
`RETIRED_ROWS` set, which sits beside the `WITHDRAWN_IDS` that has always done
the same job for requirement identifiers; it still forbids reuse of a retired
label, a repeat, or a hole anywhere else. **A decision recorded only in the spec
and not in the checker that enforces the old one is not yet made.**

The second is a gap. Three files hand-build a trailer rather than calling the
builder, and only two were in any group's scope; `sub_records.py`'s
`_with_residue` was owned by nobody and kept emitting the old layout. Nothing
caught it by reading — `tarn_vectors --verify` caught it, because the file it
produced broke a trailer gate the vector did not declare, which is exactly the
isolation property `[R-VEC-02]` exists to assert. A sweep for `TRAILER_MAGIC`
afterwards confirmed the other two were correct.

Three propagation acknowledgements were recorded, all shared phrasing rather
than restatement: §20.2's creation-path enumeration, and §2.3's and §21.9's
reuse of the 128-byte-floor wording that the new monotonicity derivation
borrows from `[R-CNT-27]`.

**§21.7's account shortens.** It listed "immutability and the generation
sequence" among the obligations a single file exhibits no witness of. The
generation sequence is no longer an obligation; F's monotonicity replaces it and
is equally unwitnessed, being a property of the prior generation that §9.7 does
not reconstruct.

**What does not change**, and this is most of the document: the *concept* of a
generation. §3.1 defines a generation as one committed state, and roughly forty
passages — §3.1's *stored*, *directory* and *trailer*, §5.1's anatomy, §9.5's
snapshot, §9.7's walk, the whole of §20.3 step 4's declaration-change bar —
quantify over committed states and are untouched. Only the counter goes.

## Alternatives rejected

- **Remove multiple committed states entirely.** A different format. It fails on
  a sentence this document already wrote (§20.4: a producer wanting a file
  without a layer "writes one: a whole-file rewrite under a fresh file_id …
  That is not compaction"), and `[R-EXT-01]` would make it a new major.
- **Keep the field, drop the monotonic guarantee.** Unsound. `[R-LIF-03]`'s
  "same generation, everything cached remains valid" would stay binding and
  become false: a reader that believes it has revalidated has not, serves a
  superseded directory, and every checksum verifies. Silent.
- **Keep the field and strict monotonicity, drop only the "+1".** The cheapest
  option — zero rows, zero instances, zero bytes — and it deletes precisely the
  clause §21.7 books as unwitnessed. Rejected in favour of removing the field
  outright, which the maintainer chose knowing this was available.
- **Shrink the trailer to 56 bytes.** Coherent, and rejected above.

## Precedent

- §2.2's treatment of withdrawn requirement identifiers, extended to register
  row labels: the retirement rule is the document's own, applied where it had
  not been.
- ADR-0099's re-keying defect, which is why F's monotonicity is derived and
  stated rather than assumed.
- Appendix D's own rationale, which says the format "certifies the live state and
  counts the rest … which is why this document has no generation-attribution
  machinery and no trailer chain" — an argument this decision completes.
