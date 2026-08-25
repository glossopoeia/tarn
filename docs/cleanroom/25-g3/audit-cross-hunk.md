# Cross-hunk consistency audit — round 26 (2 hunks)

## 0. Disclosure

Read: `/Users/robertkleffner/Documents/GitHub/tarn/spec/tarn.md` (targeted ranges, listed
below); `.../r26audit/hunk-01.diff`; `.../r26audit/hunk-02.diff`. Did NOT read full.diff,
did not list the r26audit directory, read no docs/, no conformance/, no git history, no web.

Unrequested context appeared before I began: a project instruction file pointing at
AGENTS.md, and an index of the maintainer's memory notes naming a register/corpus
relationship and a "gate board". I did not open any of it and drew no conclusion from it.
Note: the memory index line about §21 being the corpus build list is thematically adjacent
to §21.8, which I did examine — but I reached §21.8 from §21.1's own text ("Instances
column enumerates what a conformance corpus builds for that row (§21.8)"), not from that
index.

Spec ranges opened: 335 (glossary), 370-382 (§4.1), 900-975 (§7.2, [R-CNT-12]/[R-CNT-13]/
[R-CNT-14]/[R-CNT-15]), 2425-2440 ([R-MTA-02]), 2515-2600 ([R-MTA-09] note, [R-MTA-04],
[R-MTA-05], [R-MTA-10]), 2694-2816 (§19.1-§19.3), 3318-3400 (§21 head, §21.1), 3433-3470
(§21.2 rows), 3468-3500 (§21.3 head + rows), 3530-3560 (§21.4 rows), 3562-3596 (§21.5 head
+ rows), 3596-3650 (§21.6), 3650-3722 (§21.7), 3721-3760 (§21.8, §21.9), 3816-3860 (§22.2,
§22.3), 4135-4165 (Appendix B), 4355-4385 (byte-identity profile items 8-10).

## 1. The two repairs, and the rule each adopts

### Hunk 1 — §21.3 row L16 (spec line 3493), Condition cell

- old: `A layer record's or sub-record's nonzero extent slot has extent_offset < 16,
  pointing into the front signature block`
- new: `A layer record's or sub-record's nonzero extent slot has extent_offset in 1-15,
  placing the extent inside the front signature block`

Rule adopted: for a layer record or a layer sub-record, a slot other than (0,0) whose
extent_offset is one of 1..15 is a reject-layer validity error. Offset 0 is no longer named
by this row; the (0, length>0) case is left to L15.

### Hunk 2 — §21.5 row R7 (spec line 3591), Condition cell

- old: `A decoded user-metadata document is not well-formed JSON, or its top-level value is
  not an object`
- new: `A decoded user-metadata document is not well-formed JSON, its top-level value is not
  an object, or it carries a leading U+FEFF byte-order mark`

Rule adopted: a decoded user-metadata document that begins with U+FEFF is unreadable —
ignore-record — on the same footing as one that is not well-formed JSON or whose top-level
value is not an object. Instances cell unchanged (it already listed the two U+FEFF files).

## 2. Grouping (worked out from the text, not from section numbers)

Section numbers put these in different subsections and different outcome classes
(reject-layer vs ignore-record). By *rule touched* they are one group and one group only:

**Group A — "a register row's Condition cell must state exactly the set its Instances cell
enumerates and its governing rule licenses."** Both hunks edit only a Condition cell; both
leave the Instances cell alone; both are corrections of the row-to-rule / row-to-instances
correspondence that §21.1 makes normative ("its **completeness is normative**"; "each row
*restates* its governing rule"; "the count is therefore mechanical once the cell is
written").

They pull in opposite directions inside that one group:

- hunk 2 **widens** its Condition until it licenses every instance already listed (4
  licensed, 6 listed → 6 licensed, 6 listed);
- hunk 1 **narrows** its Condition away from the literal predicate of its governing rule
  ([R-CNT-13] says `extent_offset < 16`), handing the remainder to a neighbouring row.

That divergence is the cross-hunk question, and §3.3 below is where it bites.

Secondary grouping I tested and discarded: "front-signature-block bounds rows" (F9, F31,
L16, T8) — only hunk 1 is in it, but it supplies the sibling evidence for X-01.

## 3. Checks

### 3.1 Citations (check 2) — every identifier and section number in the repaired text

The repaired cells carry no inline citations of their own; the Governing rule cells are
unchanged. Checked anyway, since a row's Governing rule cell is part of the repaired row:

- **L16 → `[R-CNT-13]`** (line 928-931): "The **extent slot** (extent_offset,
  extent_length): (0, 0) means no extent. Any other combination with either half zero, an
  extent_offset < 16, an extent extending past F − 64, or an overflowing sum is a validity
  error at the scope the record governs (§7.3): the layer for a layer record and for
  sub-records". PASS on scope (reject-layer for layer records and sub-records — matches
  §21.3). PASS on existence of a `< 16` bound. See §3.3/§3.4 for the quantifier.
- **L16 → "front signature block"** (glossary line 335): "the constant 16 bytes at offset 0
  (§6.1)". So the block is bytes [0,16) and offsets 1..15 do lie in it. PASS as to which
  bytes; FAIL as to "placing the extent inside" — see X-01.
- **R7 → `[R-MTA-04]`** (lines 2537-2571): "The decoded document is a JSON text as defined
  by RFC 8259, encoded in UTF-8. Four restrictions apply, and a document violating any of
  them is unreadable — ignore-record …  - **A JSON object, unmarked.** The top-level value
  is an object, and the encoding carries no byte-order mark: a leading U+FEFF makes the
  document unreadable." PASS. The clause is normative prose, not a ">" block, and it says
  precisely what R7 now claims, including the word "leading".
- **R7 → `(R-CNT-25)`** — the quarantine, restated at §21.5's head ("User metadata is
  quarantined (`[R-CNT-25]`): every way its document can be unreadable takes this outcome").
  PASS: ignore-record is the outcome R7 carries.
- **§21.5 head's carve-out for experimental-range encodings** — R7 needs no encoding
  qualifier of its own because the head carries it for every row. PASS.

### 3.2 The repair sits in normative text (check 3)

grep for the rules' own terms, hard-wrap-safe short fragments:

```
$ grep -n "signature block" spec/tarn.md        # 335, 454, 560, 621, 624, 693, 778, 799,
                                                # 1116, 1125, 1183, 1341, 2705, 2755, 2925,
                                                # 3434, 3439, 3442, 3464, 3466, 3493, 3542,
                                                # 4144, 4331, 4456
$ grep -n "FEFF" spec/tarn.md                   # 376, 2543, 3591
$ grep -n "unmarked" spec/tarn.md               # 2542
$ grep -n "top-level value" spec/tarn.md        # 2542, 3591
$ grep -n "well-formed JSON" spec/tarn.md       # 3591 only
$ grep -n "placing the extent" spec/tarn.md     # 3464 (F31), 3493 (L16)
$ grep -n "nonzero extent slot\|nonzero slot" spec/tarn.md   # 3464, 3493, 3499 (L22)
```

Neither repair lives only in a ">" block, and neither leaves a normative statement of the
old rule standing:

- L16's rule is [R-CNT-13] at line 928-931 — bare prose, normative, unchanged and still
  saying `extent_offset < 16`. The register row is a restatement; §21.1 says "where a row
  and the rule it cites diverge, **the rule governs**". So the repair cannot weaken the
  requirement, only mis-describe it. PASS on force, with the divergence noted in X-01/X-03.
- R7's rule is [R-MTA-04]'s first bullet — normative prose. Line 2605-2610 is a ">" Note
  about why JSON was chosen; it restates nothing about the BOM. PASS.
- Line 376 ("There is no byte-order mark and no big-endian variant") is [R-ENC-02] about
  numeric byte order, a different subject; it does not contradict R7 and needed no sweep.

### 3.3 Instance arithmetic and the §21.8 totals (checks 1, 5) — both hunks

§21.1: "An instance names a field the condition ranges over, a container it can occur in,
one of several alternatives the condition text states, or any combination of the three — a
condition applying to two alternatives in two containers has four."
§21.8: "Every row of §21.2 through §21.5 — 121 conditions over 277 instances".

Mechanical recount of the live document (rows starting `| F#|L#|T#|R# |`, instances =
semicolon-separated items in field 4):

```
$ awk -F'|' '/^\| [FLTR][0-9]+ \|/{n=split($4,a,";"); t+=n; c++} END{print c, t}' spec/tarn.md
121 277
$ ... per-subsection row counts:  F 36, L 49, T 26, R 10   (§21.2 "36", §21.3 "49",
                                  §21.4 "26", §21.5 "10" — all four heads agree)
```

- **R7 post-repair**: 3 alternatives × 2 containers = 6; cell lists 6. PASS, and this is
  exactly what the repair restores — the old Condition stated 2 alternatives, licensing 4,
  against 6 listed. Hunk 2 fixes the row in the direction that preserves 277.
- **L16 post-repair**: 1 predicate × 2 containers = 2; cell lists 2. PASS. I checked whether
  rewriting a one-sided bound (`< 16`) as a two-sided range (`in 1-15`) forces a second
  direction under §21.1's direction rule: it does not. That rule runs on "a condition
  [that] compares two **magnitudes** either of which can be the greater — a *differs from*
  or *does not equal*"; membership in a fixed value range is on the other side of §21.1's
  own line ("a field tested only for being nonzero … is a value test and not a comparison of
  two quantities at all"). Count unchanged either way. PASS.
- Neighbours: L15 = 2 alternatives × 2 containers = 4, listed 4. F30 = 2 × 1 = 2, listed 2.
  F31 = 1 × 1 = 1, listed 1. All PASS.

So both repairs are arithmetically consistent with each other and with §21.8's 277. **The
two repairs agree on the convention** at the level of counting. They disagree at the level
of *what the Condition is allowed to leave to a neighbouring row* — see X-03.

### 3.4 Reading the whole structure the repair landed in (check 4)

**L16's neighbourhood.** L15 (line 3492): "A layer record's or sub-record's extent slot has
exactly one of extent_offset and extent_length zero". F30 (line 3463) is the file-tier twin
and is explicit about both halves: "extent slot has exactly one half zero (offset 0 with
length != 0, or **offset != 0 with length 0**)". F31 (line 3464) already carried, before
this commit, the identical wording hunk 1 gave L16 — the commit has two hunks and neither
touches 3464, so hunk 1 is harmonising L16 *to* F31.

"Nonzero extent slot" is not defined, but the document's own usage settles it: [R-CNT-13]
"(0, 0) means no extent. Any other combination …", and L22 (line 3499) "including slot (0,0)
with entry_count > 0, or **a nonzero slot** with entry_count = 0", where the contrast is
plainly (0,0) vs anything else. So a slot (7, 0) is a "nonzero extent slot" with
extent_offset in 1-15 → L16 fires, and it is a slot with exactly one half zero → L15 fires
too. The repair removed the (0, length>0) half of the L15/L16 overlap and left the
(1..15, 0) half. Same on the file tier for F30/F31. §21.1's specialization list is closed —
"Some rows are strict specializations of others — F1 of F6 and of F8, F35 of F36, L24 of
L25 — and a file exhibiting a specialization is recorded against the narrower row" — and
neither L15/L16 nor F30/F31 is in it, nor is either pair a specialization (neither
condition contains the other). → **X-03**.

**F33 (line 3466), untouched, in the same table as F31 and cross-referencing L16:** "…a
claimant reaching the front signature block or the live trailer is instead caught by the
bounds rows F9/F10, F31/F32, L16/L17 and T8/T9, each at its own tier". A slot (0, 100)
reaches the front signature block and, after this repair, is caught by L15 (or F30) — rows
that sentence does not name. Before the repair L16's `< 16` did catch it, so hunk 1 falsified
the L-tier half of that enumeration. → **X-02**.

**R7's neighbourhood.** §21.5 head: "every way its document can be unreadable takes this
outcome … as a violation in the rows below, except at an experimental-range encoding …
and except where a reader or verifier declines the decode on the size bound or on the
frame's declared window". No carve-out collides with the BOM alternative. R1 (encoding
value), R3 (decode failure — "decode" is the *storage* decode, i.e. decompression, per R4's
encoding-2 framing), R4 (zstd frame constraints), R5 (UTF-8 / surrogates), R6 (key
charset), R8 (non-finite numbers), R9 (duplicate keys), R10 (key length): none of them
states or contradicts a BOM rule. §21.6 has two user-metadata entries (unrecognized
`tarn.` key; standardized key out of scope) — neither touches the document's framing.
No contradiction found. PASS.

### 3.5 Exhaustive claims (check 5)

- L16 "in 1-15" — a closed range. Falsification attempt: is 0 handled elsewhere? Yes, L15/
  F30. Is 16 harmless? Yes — [R-CNT-13] bounds only below 16, the glossary puts the block at
  [0,16), Appendix B repeats "Front signature block … (16 bytes)" and "Directory minimums |
  dir_offset ≥ 16". PASS.
- L16 "placing the extent inside the front signature block" — a containment claim.
  Falsified by extent_offset = 15, extent_length = 8: the extent is [15,23), one byte of it
  inside the block. → **X-01**.
- R7 "or it carries a leading U+FEFF byte-order mark" — "leading" is the only quantifier and
  it matches [R-MTA-04]'s "a leading U+FEFF". A U+FEFF elsewhere in a string value is a
  legal ZWNBSP and neither text bars it. PASS.
- §21.5 "10 conditions", §21.3 "49 conditions", §21.8 "121 conditions over 277 instances" —
  all recomputed above, all still true after both repairs. PASS.
- §21.1's specialization list, read as closed — see X-03.
- F33's "the bounds rows F9/F10, F31/F32, L16/L17 and T8/T9" — see X-02.

### 3.6 What the repairs left unconstrained (check 6)

**Structure L16 governs: the extent slot (extent_offset, extent_length) of a layer record or
sub-record.** Every quantity it can carry, and the rule that fixes it:
u64 domain → L1/[R-ENC-03]; the (0,0)/half-zero combination → L15; the lower offset bound →
L16; offset+length upper bound (F − 64) → L17; the sum's overflow → L2/[R-ENC-04];
ownership/overlap → L18 and F33; for a user-metadata sub-record, extent_length ≥ 5 → L11;
for the layer record's own index extent, the length formula → L22. Nothing in the slot is
left unpinned by the repair. The only sibling that moved is L15's share of the half-zero
cases, which is X-03.

**Structure R7 governs: the decoded user-metadata document's framing.** Quantities: the
top-level value's type (pinned, R7); a leading BOM (pinned by this repair); leading
whitespace (permitted by RFC 8259, correctly unmentioned); a BOM *after* leading whitespace
(caught by "not well-formed JSON" — U+FEFF is not JSON ws); trailing bytes after the
top-level value (same); zero-length document (same, and L11's extent_length ≥ 5); the
document's byte size ([R-MTA-09] + §21.9's 16 MiB guarantee); member order ([R-MTA-05] →
F27/L48). I examined **nesting depth**, which §21.9's table does not guarantee and no row
constrains, as a candidate second defect in this row: it is not one the repair created or
should have carried, it is symmetric before and after, and [R-ERR-04] plus the §18.2 Note
("a reader that instead declines on resource grounds under `[R-ERR-04]` does so at the whole
file") already assign a defined behaviour. Not filed.

### 3.7 Analogy / warrant comparison (check 7)

Neither repaired cell contains "exactly as", "the same way", "as X is", "following",
"transposed from", "for the same reason", or "likewise". Reported verb-for-verb anyway,
since both cells justify themselves implicitly against a named rule:

- **L16.** Repair's governing verb: "*has* extent_offset in 1-15, *placing the extent
  inside* the front signature block". Cited rule's governing verb ([R-CNT-13]): "Any other
  combination with … *an extent_offset < 16* … *is* a validity error". The operative half
  ("has extent_offset in 1-15" vs "an extent_offset < 16") ranges over the same set once
  L15's (0, length>0) case is subtracted — same set, and I checked the subtraction is
  exact. The gloss half is the mismatch: "placing the extent inside" ranges over extents
  *contained in* [0,16); "extent_offset < 16" ranges over extents that *begin* in [0,16).
  Different sets. FAIL → X-01.
- **L16 vs its three sibling bounds rows** (the analogy hunk 1 is really making, since it
  copies F31's wording): F9 "dir_offset is less than 16, *pointing the directory into or
  before* the front signature block"; T8 "has offset < 16, *addressing bytes of* the front
  signature block"; old L16 "*pointing into* the front signature block". Three
  offset-based verbs, one containment verb. I tested the analogy separately against each of
  the other two structures, as required: F9's `< 16` is right because dir_offset is
  unconditionally ≥ 16 (line 747-748, 775; Appendix B "Directory minimums") so 0 needs no
  separate row; T8's `< 16` is right because a tile-index entry's absence marker is the
  all-ones sentinel (Appendix B "Unstored-tile sentinel `FF ×16 00 ×4`", T6/T7), not (0,0),
  so offset 0 on a non-sentinel entry is T8's own business and no T-row twin claims it.
  Neither is an unswept restatement of L16's rule — the structures individuate differently.
  PASS on those two.
- **R7.** Repair's verb: "*carries* a leading U+FEFF byte-order mark", subject "A decoded
  user-metadata document". Cited rule's verb ([R-MTA-04]): "the encoding *carries* no
  byte-order mark: a leading U+FEFF makes the document unreadable", subject "The decoded
  document". Same verb, same subject, same "leading" qualifier, same set. Tested against
  each of R7's three alternatives separately: alternative 1 ("not well-formed JSON") ←
  "The decoded document is a JSON text as defined by RFC 8259"; alternative 2 ("top-level
  value is not an object") ← "The top-level value is an object"; alternative 3 ← the BOM
  clause. All three PASS.

### 3.8 Cross-hunk verdict

The two repairs do not contradict each other on any byte, any outcome, any count. They are
consistent where a checker could see it (both preserve 121/277; both leave their Governing
rule cells alone; neither touches a rule the other restates). Where they disagree is the
convention in §2 above, and the disagreement has one concrete residue, X-03: hunk 2 finished
the job of making a Condition cell coextensive with what its row must carry, and hunk 1 did
the same job halfway, leaving L16 (and F31, which it copied) overlapping L15 (and F30) on
slots (1..15, 0). Neither of the two auditors looking at a single hunk has both halves of
that comparison in front of them.

## 4. Byte-level test for each finding

The discriminating question in all three: is the disputed file conforming? In every case it
is **not** — [R-CNT-13] independently makes the slot a validity error, and §21.1 says the
rule governs where a row and its rule diverge. So no conforming writer may emit any of the
disputed files ([R-CNF-05]) and every conforming reader rejects at the same scope
(reject-layer for L15/L16, reject-file for F30/F31), only recording the damage against a
different row. The emittable set does not move and no accept/reject verdict flips. All three
findings: **not byte-level**. I record this plainly rather than inflating: X-01 is the one
that comes closest, because a reader that implements the register cell literally and never
opens [R-CNT-13] would accept a layer whose sub-record extent starts at offset 8 and runs
1000 bytes — but that reader is already non-conforming under §21.1's precedence clause, so
the divergence is resolvable inside the document.
