# Repair audit — case adr0109, hunks 01–08

## 0. Disclosure of what I read and ran

Read: the eight hunk files named in my charter
(hunk-01.diff … hunk-08.diff) in
/private/tmp/.../scratchpad/case-adr0109/, and
/Users/robertkleffner/Documents/GitHub/tarn/spec/tarn.md (many passages,
listed below). I did not read full.diff, did not list the case directory,
and read no other hunk files. I read no docs/, no PLAN.md, no
OPEN-QUESTIONS.md, no AGENTS.md, no conformance/, no registry.json, no git
history, no web.

Unrequested context appeared in my context before I began: a project
instruction file pointer and an index of the maintainer's memory notes
(titles only). I did not open any of it and no conclusion below derives
from it; I name that it appeared, not its contents.

Commands run (all against spec/tarn.md only):
- `wc -l spec/tarn.md` → 4559
- `sed -n` reads of: 283–302, 545–590, 623 area, 915–962, 960–1050,
  1755–1775, 1815–1850, 1900–1992, 1990–2045, 2080–2100, 2440–2470,
  2525–2575, 2570–2610, 2915–2950, 3228–3275, 3300–3375, 3400–3500,
  3496–3552, 3552–3602, 3602–3680, 3680–3800, 4344–4360, 4425–4500,
  and the §6.1 block.
- `grep -n "tile extent"`, `grep -n "R-WRT-06"`, `grep -n "sub-record"`,
  `grep -n -i "specializ\|narrower\|strict special"`,
  `grep -n "R-ENC-13\|R-ENC-14\|R-IDX-02\|R-TYP-08\|R-CNF-09\|R-COD-10\|R-MTA-09\|R-MTA-10"`,
  `grep -n "front signature block"`, `grep -n "sparse layers first-class"`.
- One python3 pass that read spec/tarn.md, collapsed all whitespace to
  single spaces (defeating the hard wrap) and printed every occurrence with
  160 chars of context for: "reads as fill", "read as fill",
  "channel's fill", "addressed but not stored", "never returns fill",
  "return fill", "in place of data", "not usable". This is the sweep I
  relied on for the hard-wrap problem; line-oriented greps for those
  phrases would have missed wrapped instances.

Hunk-header heading claims verified against the body: hunk 1 → §14.4 (line
2000) OK; hunk 2 → §20.4 (3228) OK; hunk 3 → §21.1 (3415) OK; hunk 4 →
§21.2 (3496) OK; hunk 5 → §21.4 (3602) OK; hunk 6 → §21.5 (3639) OK;
hunk 7 → §21.6 (3673) OK; hunk 8 → Appendix G (4344) OK. No mismatch.

---

## Hunk 1 — §14.4 Note, single-channel bool layouts

### Rule the repair asserts
For a single-channel bool layer, the planar and interleaved tile images
differ in length whenever ceil(P/8) != P; at P = 1 they are the same length,
and there the two images are byte-identical if and only if the channel's
fill is false.

### Check 1 (tense/quantifier)
No generation is in play. The quantifier is over P, a per-layer
declaration-derived quantity (P = prod Ti). "wherever ceil(P/8) != P" and
"At P = 1" partition the space only if P >= 1 always. Verified: L32 ("A layer
geometry field whose floor is 1 is 0 | rank d; channel count C; tile extent
Ti"), and line 1539 "extent Ei >= 0, and a tile extent Ti >= 1 ... a reader
MUST reject ... layer with rank 0, any tile extent 0". So d >= 1 and every
Ti >= 1, hence P >= 1 and P = 0 is unreachable. ceil(P/8) = P holds only at
P = 1. Partition is exact.

### Check 2 (citations)
- `[R-SER-05]` (§14.5, line ~2036): "Every pad bit (§14.3) MUST carry the
  plane's channel's fill bit." The repair says it "fixes the planar pad bits
  to the channel's fill". VERDICT: resolves, exact.
- §14.3 `[R-SER-03]` (not cited but relied on): packing is LSB-first, "value
  k occupies bit k mod 8 of byte k div 8 ... 0 = false and 1 = true",
  decoded size ceil(P/8); pad bits are "bit positions P mod 8 through 7,
  when P mod 8 != 0". At P = 1 that is bits 1–7.
- §14.2 `[R-SER-02]`: interleaved bool "as a single byte, 0x00 = false,
  0x01 = true, with element size 1"; interleaved decoded size P·Q, and with
  C = 1 bool, Q = 1, so 1 byte at P = 1. Same length as ceil(1/8) = 1. OK.

### Smallest legal instance (as charter requires)
rank 1, T0 = 1, E0 = 1, one bool channel. One addressed tile, P = 1.
- fill false: planar byte = value in bit 0, bits 1–7 = 0 → 0x00 or 0x01.
  Interleaved byte = 0x00 or 0x01 for the same value. Identical. OK
- fill true: planar = 0xFE (value false) or 0xFF (value true); interleaved
  = 0x00 or 0x01. Never identical. OK
- edge/padding case: if the single position is a padding position it carries
  the fill in both layouts (`[R-SER-05]`); with fill true planar = 0xFF,
  interleaved = 0x01 — still different. So "exactly when that fill is false"
  is an iff, and it holds. VERDICT: the new sentence is correct.
- Bool fill is constrained to 0x00/0x01 by L35 / `[R-TYP-07]`, so no third
  fill state exists to break the iff.

### Check 3 (normative siting)
The repair edits a blockquote **labelled "Note."** — non-normative by
`[R-CNF-01]`. It states no rule; the rules it depends on (R-SER-02,
R-SER-03, R-SER-05, R-SER-09) all sit in normative prose (§14.2, §14.3,
§14.5, §14.4). Nothing normative elsewhere says the old (wrong) thing that
needed correcting, because the Note asserted no rule. Grading: an error
here would be editorial, not a conformance defect; but I found no error.

### Check 4 (contradiction in the passage)
Read all of §14.4 (2000–2035) and §14.3, §14.5. The untouched first clause
"A single-channel numeric layer produces byte-identical tile images under
either layout" is true: planar offset k·Bc; interleaved with C = 1 gives
(k div 1)·Q + F0 = k·B. No collision with the new sentence. The §14.3
Example ("with fill true, `55 FD`") is consistent with pad bits = fill.
`[R-SER-09]`'s "both forms are valid" is untouched and still true.

### Check 5 (exhaustive claims)
- "the two are the same length" — a count of 2 (planar, interleaved): correct,
  §14.4 lists exactly two layouts (L36: layout is 1 or 2).
- "wherever ceil(P/8) != P" — verified above to be exactly "P >= 2".
- "exactly when that fill is false" — an iff; verified both directions.

### Check 6 (what the structure still leaves open)
Structure: a single-channel bool tile image. Members: (a) value bits/bytes —
fixed by R-SER-03 (planar) / R-SER-02 (interleaved); (b) pad bits — fixed by
R-SER-05; (c) padding positions — fixed by R-SER-05; (d) image length —
fixed by R-SER-02/03. All four pinned; no sibling left unconstrained.

### Check 7 (analogy)
No "exactly as / the same way" construction. The one warrant is R-SER-05:
repair verb "fixes the planar pad bits to the channel's fill" vs rule verb
"Every pad bit MUST carry the plane's channel's fill bit". Same set (every
pad bit of that plane), same direction. Comparison passes.

**Hunk 1 verdict: no finding.**

---

## Hunk 2 — §20.4 MU = 1 row, compaction clause

### Rule the repair asserts
For a record whose type the updater does not implement and whose stored MU
bit is 1, a compactor MUST refuse the whole file — whether the record is
top-level or a layer sub-record — because such a type may carry references
this document does not define, so its bytes cannot be relocated.

### Check 1 (quantifier)
The row's premise (line 3241–3246) is "For a type the updater does not
implement, the stored flags are authoritative". The repair's added sentence
ranges over "either scope" = the two scopes the row's two prior sentences
name (layer, file). Not a generation claim.

### Check 2 (citations)
- `[R-WRT-06]` (line 3329–3331, §20.5, normative prose): "A compactor MUST
  refuse to compact a file carrying **any record** whose type it does not
  implement with MU = 1: such a type can define references this
  specification does not (§7.2), so its bytes cannot be safely relocated."
  The repair's gloss is that rule's own words, verbatim from "such a type"
  onward. VERDICT: resolves, and supports the claim.
- The scope claim: does "any record" reach a layer sub-record? §7.4's layer
  record layout (line 1089): "| sub-records | zero or more **records**
  (§7.2 framing) to the end of the inline payload | layer scope by
  containment |". A sub-record is a record. §7.2 line 998 assigns governing
  scope "the layer for a layer record and for sub-records, the file for
  other top-level records" — two scopes, no third. VERDICT: "at either
  scope" is supported by "any record".
- §7.2: "Records with MU = 1 carry further references only where this
  specification or registry review (§10) defines them". VERDICT: resolves —
  it is exactly the ground R-WRT-06 states.
- §2.3, `[R-CNT-18]`, `[R-CNT-15]`, §6.3, `[R-WRT-06]` in the untouched
  parts of the cell: unchanged by this hunk; R-CNT-15 does make an
  unimplemented top-level MU = 1 record reject-file (§7.2 line 1030-ish),
  and R-CNT-18 governs the layer-scope case. Both check out.

### Check 3 (normative siting)
The repair is a cell of a table in §20.4's normative body, not a blockquote.
The rule it restates (R-WRT-06) is in §20.5's normative prose, unchanged.
Grep of "R-WRT-06" gave 9 hits: 878, 3250 (this cell), 3331 (the rule),
3348, 3359, 3785, 4064, 4377, 4448/4449. Line 3359 ("an MU = 1 type the
compactor does not implement never reaches this step (`[R-WRT-06]`)") and
line 3348 ("`[R-WRT-06]` then obliges refusal") are consistent with the
repair. No surviving statement of the old, weaker "compaction is barred on
the same ground" formulation anywhere.

### Check 4 (contradiction in the passage)
Read all of §20.4 (3228–3298) and §20.5 (3300–3375). Candidate collisions
examined:
- "At layer scope an unknown critical record blocks modification of that
  layer, leaving other layers editable" vs "At either scope a compactor MUST
  refuse the file". Not a contradiction: the first governs an appender's
  in-place commit, the second a compactor's whole-file rewrite. §20.5
  line 3359 says the same thing from the other side.
- MU = 0/PE = 0 row: "A compactor MAY drop it whenever it rewrites the
  file." Different flag combination; no collision.
- §20.5 "An MU = 1 type it *does* implement is the remaining case, and §7.2
  admits it" — complementary, not contradictory (this row is only about
  types the updater does **not** implement).

### Check 5 (exhaustive claims)
"At either scope" — a closed count of two. Verified against §7.2 line 998:
records govern either layer scope (layer record and sub-records) or file
scope. Nesting beyond two is a validity error (`[R-CNT-18]`, line 1118), so
there is no third scope a record can sit at. Holds.

### Check 6 (what the structure leaves open)
Structure: the obligations table for an unimplemented record's stored flags.
Members: MU = 1; MU = 0/PE = 1; MU = 0/PE = 0 (MU = 1/PE = 0 is folded into
MU = 1 by R-CNT-12). All three rows carry obligations. Within the MU = 1
row, the actors in play: appender (covered — MUST NOT modify the scope),
compactor (now covered at both scopes), whole-file rewriter under a fresh
file_id (not an updater; and it is a reader first, so R-CNT-15/R-CNT-18
reject the file or the layer for it anyway). Reserved flag bits 2–15 are not
this row's business (F26/L47). Nothing left dangling.

### Check 7 (analogy)
"on `[R-WRT-06]`'s own ground". Repair verb: "a compactor MUST refuse the
file". Cited rule verb: "A compactor MUST refuse to compact a file carrying
any record ...". Same modal, same actor, same object; the repair's "at
either scope" is narrower than "any record", not wider. The other analogy in
the cell ("the same treatment §6.3 gives an unknown incompat-lane bit") is
untouched pre-existing text and F19/`[R-CNT-08]` bear it out. Comparison
passes.

**Hunk 2 verdict: no finding.**

---

## Hunk 3 — §21.1, closed list replaced by a property  (THE BIG ONE)

### Rule the repair asserts
Row X is a strict specialization of row Y iff every file exhibiting X's
condition necessarily exhibits Y's. A file exhibiting both is recorded
against the narrower row, and that row's Detector and Detected cells are the
ones that apply. Rows that merely overlap — each reachable without the
other — are not in the relation. The named list is illustrative, not closed.

### Derivation, then attack

**(a) Is the relation the register needs?** For each named pair I checked
the outcome the clause dictates against both rows' Detector/Detected cells:
- F35 (reader, open) of F36 (verifier, certification): F35 = reserved-range
  top-level type with MU = 1; F36 = reserved-range top-level type whatever
  the MU bit. Every F35 file is an F36 file. OK. Narrower = F35, so
  reader/open applies — the stronger obligation. Coherent.
- L24 (reader, layer access) of L25 (verifier, certification): identical
  shape at layer scope. OK.
- F21 (reader, open) of F22 (reader, open): F21 = top-level user-metadata
  record carries slot (0, 0); F22 = its extent_length < 5. Slot (0,0) has
  extent_length = 0 < 5, so every F21 file is an F22 file. F22 is reachable
  without F21 (offset 100, length 3). Strict. Both cells identical, so the
  recording rule changes nothing operationally. OK. (Note this containment
  is exactly what hunk 4's deletion makes clean — see hunk 4.)
- L10 (reader, layer access) of L11 (reader, layer access): same at layer
  scope. OK.
- **F1 of F6, and F1 of F8: FAIL.** See finding A-01 below.

**(b) A pair the clause catches that the old list did not name** (charter
asks for at least one beyond the two new ones, or a sweep report). I swept
by reading every row of §21.2 (F1–F36), §21.3 (L1–L49), §21.4 (T1–T26) and
§21.5 (R1–R10) and, for each row, asking whether its condition forces
another row's condition. Method: for rows whose Condition text already names
another row's check ("the check that detects it is Tn's"), test containment
directly; for value-domain and bounds rows, test whether the field values
one row admits are a subset of another's.
- **T16 of T24** — clean, unnamed. T16: "Codec 2 (deflate) and the stored
  extent holds more than one DEFLATE stream — a second stream begins after
  the BFINAL block; the check that detects it is T24's". T24: "The decode
  does not consume the entry's length exactly — bytes remain in the stored
  extent after the stream, frame, or block ends | any codec". Every T16 file
  has bytes after the first stream ends, so every T16 file is a T24 file.
  T24 is reachable without T16 (trailing garbage under codec 1 or 3).
  Detector/Detected identical (reader, tile use), so the recording rule is
  coherent here.
- T13 of T25 and T23 of T25 — same shape; both rows say "the check that
  detects it is T25's", and both conditions force a standalone decode
  failure.
- T11 of T9 — probable: an entry offset or length above 2^63 − 1 puts the
  extent's end past F − 64 for any F <= 2^63 − 1 (F2 bounds
  committed_file_length). Listed as probable, not asserted, because it turns
  on how the sum is evaluated when a field is already out of domain (T12
  carves that out for the sum row but T9 does not).
- Union-shaped, therefore NOT caught by the row-level property: T15 (its
  check is "T24's or T25's") and T26 (its check is "T2's or T4's"). These
  fail the property for exactly the same reason F1 does — see A-01.
So: the property does real work beyond the list, and the "not offered as
closed" hedge is warranted.

**(c) The negative, tested on an overlapping pair.** T8 ("A non-sentinel
tile-index entry has offset < 16") and T10 ("A non-sentinel tile-index entry
has length = 0"). Each is reachable without the other (offset 8/length 100;
offset 1000/length 0) and they overlap (offset 8/length 0). Per the clause
they do not stand in the relation, so the file is recorded against both;
both cells read reader/tile use and both outcomes are reject-tile, so
nothing clashes. Second test with different tiers: L21 (reader, layer
access) and L37 (reader, tile use) overlap and each is reachable without the
other; recorded against both, each cell stands on its own and the earlier
tier simply fires first. The negative holds in both cases, and I found no
overlapping pair where recording against both produces an incoherent
detector or detection point — **except** the pair the clause itself
mis-classifies (A-01).

### Check 2 (citations)
The repaired sentence cites no requirement IDs and no section numbers. The
surrounding untouched text cites `[R-CNT-25]`, `[R-CNF-07]`, `[R-CNF-04]`,
`[R-CNF-11]`, §2.4, §19.2, §21.6, §21.7, §21.9 — none touched by this hunk.
I opened `[R-CNT-25]` (§7.1, line ~941) for the F21/F22 and L10/L11 pairs:
"An extent of (0, 0) on a user-metadata record, or one whose extent_length
is less than 5 — too short to hold both a document and the terminal CRC-32C
§8.1 places in its final 4 bytes — is a validity error at its containing
scope." The two disjuncts are not exclusive, and F22/L11 are stated over the
*field* ("a record's extent_length is less than 5"), which a (0,0) record
has with value 0. So the containment survives §21.1's own "where a row and
the rule it cites diverge, the rule governs". VERDICT: consistent.

### Check 3 (normative siting)
§21.1 is normative prose, not a blockquote. `grep -n -i
"specializ\|narrower\|strict special"` returns only 2612 (unrelated:
"narrower scope whose declarations that rule can measure") and 3438/3440 —
the repair itself. So there is no second statement of the old closed list
left standing anywhere. Sweep clean on that axis.

### Check 4 (contradiction in the passage)
The contradiction is inside the repair itself: see A-01. Elsewhere in §21.1
I checked the sentence "Conditions attach to the finest structure they
damage, and the outcome follows from that scope" — compatible with
"recorded against the narrower row". And F33's own carve-out ("a claimant
reaching the front signature block or the live trailer is instead caught by
the bounds rows F9/F10, F30/F31/F32, L15/L16/L17 and T8/T9, each at its own
tier") is a hand-written overlap resolution that the new property does not
disturb, because those pairs merely overlap.

### Check 5 (exhaustive claims)
- "this list is not offered as closed" — correctly disclaims closure; my
  sweep found T16/T24 etc., which the hedge accommodates.
- "the property decides any pair" — a totality claim. For disjoint pairs and
  overlapping pairs it decides "no"; for containment it decides "yes". The
  one case it cannot decide is mutual implication (two rows with equivalent
  conditions), and I found none. But the claim is false in the direction
  that matters: it does **not** decide the F1 pairs the same way the
  sentence next to it does (A-01).
- "F1 of F6 and of F8, F35 of F36, L24 of L25, F21 of F22 and L10 of L11" —
  five assertions; three of the pairings (F35/F36, L24/L25, F21/F22,
  L10/L11 — four) verified true, two (F1/F6, F1/F8) verified false at the
  granularity the property uses.

### Check 6 (what the structure leaves open)
Structure governed: the register as a set of rows, each with cells
Condition / Instances / Detector / Detected / Governing rule, plus the
subsection-level Outcome. The clause fixes, for a specialized pair, the
Detector and the Detected cells. It does **not** say which row's
**Outcome** applies, nor which row's **Instances** the corpus builds. For
every pair it names, both rows sit in the same subsection and so share an
outcome, so nothing bites today; but the property is open-ended ("decides
any pair"), and a future cross-subsection containment would leave the
outcome unassigned by this clause — §21.1's "the outcome follows from that
scope" would then be the only guide and would point at the narrower row's
scope, i.e. the *weaker* outcome. I swept for such a pair and found none:
the F/L/T/R rows are scoped disjointly by construction, and F33's carve-out
explicitly routes cross-tier claimants to their own tier. Recorded as a
sweep result, not a finding.

### Check 7 (analogy)
The repair argues from no other rule; it defines a property outright. No
"exactly as / the same way / following" construction to compare. Not
applicable.

### FINDING A-01 (see structured output)

---

## Hunk 4 — §21.2 row F21, deleted clause

### Rule the repair asserts
F21's condition is exactly the field-value condition "a top-level
user-metadata record carries extent slot (0, 0)"; the reason that is a
violation is not part of the row.

### What the deleted clause was carrying, and what carries it now
Deleted: ", placing its document inline". It was (i) a rationale for the
violation and (ii) inaccurate: §7.2 says "(0, 0) means **no** extent", not
"the document moves inline", and F23 fixes a user-metadata record's
inline_length at 1 (the encoding byte alone), so no document can be inline.
The normative statement that carries the real content is `[R-CNT-25]`
(§7.1): "Each user-metadata record carries its document in its extent —
**never inline** — and declares the document's encoding in its own inline
payload". That is the row's Governing rule cell, unchanged. So the clause's
freight is carried, and carried more accurately than the deleted words did.

### Check 1
Field-value quantifier, no generation. Matches R-CNT-25's "An extent of
(0, 0) on a user-metadata record ... is a validity error at its containing
scope", split by scope into F21 (file) and L10 (layer).

### Check 2
`[R-CNT-25]` opened and read (§7.1, lines 941–961). VERDICT: says what the
row now claims.

### Check 3
Register row in a normative table. The rule it restates is normative prose.
No blockquote involved.

### Check 4
Neighbouring rows F22 (extent_length < 5) and F23 (inline_length != 1) —
after the deletion, F21 no longer says anything about the inline payload,
which is F23's subject, so a small pre-existing overlap of subject matter is
removed rather than created. L10 (the layer-scope twin) never carried the
gloss, so the deletion makes the two rows parallel — which the hunk-3
property needs, since F21 of F22 and L10 of L11 must read the same way.

### Check 5
Nothing exhaustive left in the cell.

### Check 6
Structure: the F21 row's five cells. Condition — now a bare field test.
Instances "—" = one file, correct (there is exactly one distinguishable
(0,0) file for this row). Detector reader / Detected open — unchanged and
still right, since the slot is in the record header read at open. Governing
rule R-CNT-25 — unchanged. Nothing in the row is now unpinned. The sibling
condition on the same record that the row does not cover (inline_length,
encoding byte value) is covered by F23 and R1 respectively.

### Check 7
No analogy.

**Hunk 4 verdict: no finding.** The deletion removed a false gloss and lost
nothing the governing rule does not carry.

---

## Hunk 5 — §21.4 preamble

### Rule the repair asserts
The "never returns fill" half of the reject-tile outcome binds a reader only
for a rejection that reader is obliged to detect; for a row whose Detector
is *verifier*, no reader is obliged to detect the condition, and what a
reader does is stated by the governing rule.

### Check 1 (quantifier)
`[R-CNF-09]` (line 309–311): "A reader MUST NOT return data as valid from a
scope this specification rejects **and whose rejection this reader is
obliged to detect** (`[R-RDR-02]`); in particular, a read of a rejected tile
MUST NOT silently return fill." The repair's added qualifier "for a
rejection the reader is obliged to detect" is that rule's own qualifier,
word for word in substance. The dropped qualifier is now restored. PASS.

### Check 2 (citations)
- `[R-CNF-09]`: opened, quoted above. VERDICT: says what the preamble claims.
- The §21.4 rows whose Detector is *verifier*: T2, T4, T5, T26 (read the
  whole table, 3610–3637). Their governing rules: R-SER-08 (T2), R-SER-05
  (T4, T5), R-COD-10 (T26).
  - R-SER-08 (§14.2, lines 1911–1930): "A reader that neither detects the
    violation nor rejects the tile, and returns the value, MUST report 0x00
    as false and every other byte as true." — states what a reader does. OK
  - R-SER-05 (§14.5, lines 2036–2042): "A conforming reader never returns
    this content (`[R-GEO-04]`) and is not obligated to check it" — states
    what a reader does. OK
  - R-COD-10 (§17.3, lines 2450–2463): "A writer that filters with any other
    stride violates this rule; where the resulting decoded image breaks a
    stated content obligation (§14.5's padding, `[R-SER-08]`'s bool bytes) a
    verifier detects it as a validity error at tile scope, and otherwise the
    consequence is wrong sample content — undetectable by construction
    (§21.7)." — says nothing about what a reader does. FAILS the claim.
    See finding A-02.

### Check 3 (normative siting)
§21.4's preamble is normative prose introducing a normative table. Not a
blockquote. The parallel statement in §21.1 ("For a row whose Detector is
*verifier*, the outcome names the scope at which the damage is recorded, not
an obligation on any reader: the governing rule states what a reader does")
is also normative and now agrees with §21.4. No blockquote-only siting.

### Check 4 (contradiction in the passage)
- §2.4's outcome table, reject-tile row: "The affected tile's data is not
  usable; a read of that tile reports failure." Unqualified, but that table
  *defines* the class rather than restating a detection obligation, and
  §21.1 carries the verifier nuance. Not scored.
- `[R-TYP-09]` (line 1837–1841): "A reader MUST NOT return fill for a tile
  whose entry is malformed (§15.3), whose index CRC array or segment failed
  verification, or whose stored bytes failed their checksum". Unqualified —
  but every condition it names is a reader-detected row (T1, T6–T12, L37,
  L38), so it never reaches a verifier row and does not collide.
- §19's read path, step 4 and step 8 (lines 2925, 2947): "a rejected tile's
  read reports failure, and fill is never a failure fallback
  (`[R-CNF-09]`)"; "MUST NOT stand fill in for a rejected tile's positions
  (`[R-CNF-09]`)". Both cite R-CNF-09 and so inherit its qualifier. No
  collision.
- Appendix H's reader checklist: "never returns fill for a rejected tile
  (§2.4)". Non-normative summary that disclaims its own authority ("each
  entry's authority is the requirement or section cited, never this
  summary"). Not scored.
- **§21.3's preamble**: "Outcome: reject-layer — the named layer is
  unusable, every other layer unaffected. 49 conditions." Unqualified, and
  §21.3 contains verifier rows (L18, L40, L41, L42, L46, L47, L48, L49) for
  which §21.1 says the opposite. See finding A-03.

### Check 5 (exhaustive claims)
- "never returns fill in place of data" — now bounded by the obliged-to-
  detect clause; holds.
- "no reader is obliged to detect the condition" — true for verifier rows by
  `[R-CNF-04]`/`[R-CNF-11]` and §21.1's own statement; a reader that does
  detect one MAY reject under the §2.4 paragraph. Holds.
- "the governing rule states what a reader does" — a universal over the four
  verifier rows of §21.4. Fails on T26. A-02.
- "26 conditions" — unchanged by the hunk; §21.2+§21.3+§21.4+§21.5 =
  36+49+26+10 = 121, matching §21.8's "121 conditions". Arithmetic intact.

### Check 6 (what the structure leaves open)
Structure: a §21.4 row's five cells plus the subsection Outcome. The
preamble now pins: the outcome (reject-tile), the fill prohibition and its
scope, and the meaning of a verifier Detector. Left unpinned by the
preamble but pinned elsewhere: the Detected column (§19.2's tiers, named in
§21.1), the Instances column (§21.1's instance rules), and the blast-radius
bounding for multi-entry requests (§19 step 8). Nothing in the structure is
governed by nothing.

### Check 7 (analogy)
Warrant is `[R-CNF-09]`. Repair verb: "never returns fill in place of data,
for a rejection the reader is obliged to detect". Rule verb: "MUST NOT
return data as valid from a scope this specification rejects and whose
rejection this reader is obliged to detect ... a read of a rejected tile
MUST NOT silently return fill." Same set (rejections this reader must
detect), same object (fill for a rejected tile). Comparison passes.

### FINDINGS A-02, A-03

---

## Hunk 6 — §21.5 rows R3 and R4 (the pair that must agree)

### Rules the repairs assert
R3: a decode failure under an assigned encoding is R3's, **except** where
the encoding is 2 and what fails is a frame constraint R4 registers, in
which case the row is R4 even if the bytes also fail to decode.
R4: every constraint R4 registers is checkable from the extent's bytes
without depending on how tolerant a decoder is; a reader that only attempts
a decode cannot tell which constraint is broken; and several of them —
content-size among them — are broken by the frame's declarations while the
bytes still decode.

### Do they agree with each other?
- Double registration: a missing frame magic under encoding 2 satisfies both
  R3's literal text and R4's. R3's new carve-out routes it to R4. Exactly
  one row. No condition is registered by both.
- Gap: encoding 2 with a well-formed, constraint-satisfying frame whose
  compressed data is corrupt → decode fails → R3 (the carve-out does not
  fire, since no R4 constraint is broken). Encoding 1 verbatim → nothing to
  fail. Encoding 0 / reserved → R1. Experimental → §21.6. No condition is
  registered by neither.
- Claim collision: R4 says its constraints are checkable without a decoder's
  tolerance; R3's carve-out says routing holds "whether or not the bytes
  also fail to decode". These are compatible: R4's ground is checkability,
  not decodability. Neither denies the other.
- The set "the frame constraints R4 registers" is well defined by §18.2
  (lines 2536–2556): magic; no skippable frame; no second frame; no dictionary
  use and no nonzero dictionary ID; no content-checksum flag; the bar on
  sizing a buffer from a declared length; **"Two of those carry no witness a
  file exhibits, and R4 registers neither"** (undisclosed dictionary use;
  the buffer-sizing bar). R4's Instances cell enumerates exactly the
  witnessed set plus "bytes remaining after the frame" and the two
  content-size directions. R3's carve-out is carefully worded as "the frame
  constraints **R4 registers**", not "§18.2 states", so it does not sweep in
  the two witnessless ones. The pair agrees exactly.

### Check 1 (quantifier)
"where the encoding is 2 and what fails is one of the frame constraints R4
registers" — ranges over the registered constraint set, not over §18.2's
full list. Correct and deliberately narrower.

### Check 2 (citations)
- `[R-MTA-10]`, `[R-CNT-25]`, `[R-COD-06]`, `[R-MTA-09]` in the cells:
  unchanged by the hunk. I opened `[R-MTA-09]` (§18.2, lines 2565–2602):
  "The frame's content-size field ... MAY be present, and when present it
  MUST equal the byte length of the decoded document. **A mismatch is one of
  the frame constraints R4 registers, not a failure to decode under R3: the
  bytes decode, and what is wrong is what the header said about them.
  Routing it to R4 keeps the condition checkable from the bytes alone rather
  than turning on a decoder's tolerance (`[R-CNF-02]`)**". VERDICT: this is
  the normative statement the two repaired cells restate, and both now match
  it — R3's carve-out generalizes the routing from the content-size case to
  the whole registered set, which §18.2's constraint list supports, and R4's
  "checkable ... without relying on a decoder's tolerance" is §18.2's own
  phrase.
- §18.2 as cited in R4's condition: opened, quoted above. VERDICT: resolves.

### Check 3 (normative siting)
Both cells are in a normative table; the governing statement is in §18.2's
normative prose (`[R-MTA-09]`), not in a blockquote. The §18.2 Note that
follows ("The 16 MiB figure is a §21.9 minimum guarantee...") is labelled
and carries nothing the repair depends on.

### Check 4 (contradiction in the passage)
Read the whole of §21.5's preamble (3639–3660) and all ten rows.
- Preamble: "except where a reader or verifier declines the decode on the
  size bound or on the frame's declared window, which `[R-MTA-09]` makes
  that actor's capability and not a fact about the file" — consistent with
  R4 not registering a window constraint (its Instances cell has no window
  entry) and with §18.2's two exceptions.
- Preamble: "Encoding 0 and a reserved-range value are unassigned too, and
  R1 registers both" — matches R3's untouched clause.
- R1/R2 vs R3/R4: R2 (extent CRC) precedes any decode; no collision.
- The one pre-existing wrinkle I checked and did not score: §18.2 says
  undisclosed dictionary use "carries no witness a file exhibits", yet a
  zstd frame compressed against an undisclosed dictionary can fail to
  decode, in which case R3 does witness it. That tension is in untouched
  text (§18.2 and R3's first clause), the hunk neither creates nor worsens
  it, and R3's new carve-out deliberately does not reach it.

### Check 5 (exhaustive claims)
- "one of the frame constraints R4 registers" — a closed set; verified
  against §18.2's list and R4's Instances cell; they agree.
- "a constraint of this row is checkable from the extent's bytes without
  relying on a decoder's tolerance" — universal over R4's seven constraint
  families. Magic, skippable frame, second frame, dictionary ID,
  content-checksum flag and bytes-remaining are header/structure tests. The
  content-size test needs the decoded length, i.e. a decode — but the claim
  is about a decoder's *tolerance*, not about avoiding a decoder, and §18.2
  itself calls that same test "checkable from the bytes alone". Holds as
  worded.
- "several, the content-size field among them, are broken by what the frame
  declares while the bytes decode" — "several" needs >= 2: content-size
  mismatch, content-checksum flag set, and bytes remaining after the frame
  all decode. Holds. This is the claim the old wording overshot on
  ("broken by what the frame declares **rather than** by whether the bytes
  decode ... a reader that only tries decoding establishes **none** of
  them"), which was false for the magic instance; the new wording is
  correctly weakened to "does not establish **which** of them is broken".
  No residue of the old absolute survives in either cell.

### Check 6 (what the structure leaves open)
Structure: the encoding-2 user-metadata frame, and the R-row set that
registers its failures. Quantities the frame carries: magic (R4), frame
type — skippable vs compressed (R4), frame count (R4), dictionary ID (R4),
content-checksum flag (R4), content-size field (R4), Window_Size /
Window_Descriptor (**deliberately unregistered** — §18.2 replaces
`[R-COD-06]`'s window constraint with a reader-capability rule, and §21.5's
preamble and `[R-MTA-09]` both say so), trailing bytes (R4), the compressed
payload itself (R3), and the extent's terminal CRC (R2). Every quantity is
governed by something, and the one that is not registered as a violation is
explicitly accounted for in three places. No unpinned sibling.

### Check 7 (analogy)
"unlike R3" is a contrast, not a warrant. The warrant is §18.2: repair verb
"is checkable from the extent's bytes without relying on a decoder's
tolerance" vs §18.2's "keeps the condition checkable from the bytes alone
rather than turning on a decoder's tolerance". Same verb, same ranging.
Tested separately against each of R4's seven constraint families above; the
only one that needed care (content-size) is the very one §18.2 states it
for. Comparison passes.

**Hunk 6 verdict: no finding. The two cells agree; nothing is registered by
both rows or by neither.**

---

## Hunk 7 — §21.6 sentinel row

### Rule the repair asserts
For a sentinel index entry, every sample position the tile carries **inside
the layer's extents** reads as fill, and the fill is taken **per channel the
tile carries** rather than from a single channel.

### Check 1 and Check 7 — side-by-side quantifier comparison
Repair: "The tile is addressed but not stored; every sample position it
carries **inside the layer's extents** reads, **for each channel the tile
carries**, as that channel's fill".
`[R-TYP-08]` (§13.3, lines 1819–1827): "For every addressed tile that is not
stored in the live generation — its index entry is the sentinel (§15.2) — a
reader that returns any of the tile's sample positions **inside the layer's
extents** MUST return, **for each channel the tile carries**, that channel's
fill value at every such position."
Both qualifiers now match word for word. The old cell said "every sample
position it carries reads as **the channel's** fill" — dropping the extents
qualifier (so it appeared to promise fill for padding positions, which
`[R-GEO-04]` says a reader never returns) and collapsing "each channel the
tile carries" to a single channel (right for planar, wrong for interleaved,
where one tile carries every channel). Both drops are repaired.
Governing verbs: repair "reads ... as that channel's fill" vs rule "MUST
return ... that channel's fill value". The repair is in a Defined-behavior
column and states the outcome rather than the obligation; the ranging is
identical. Comparison passes.

### Check 2 (citations)
- `[R-IDX-02]` (§15.2, lines 2090–2096): "An addressed tile that is not
  stored has the **sentinel entry**: offset and length both
  0xFFFF_FFFF_FFFF_FFFF and crc 0 ... A sentinel tile contributes fill to
  the reference array (§3.2, §13)." VERDICT: supports "addressed but not
  stored" and the fill contribution.
- `[R-TYP-08]`: quoted above. VERDICT: supports the rest, exactly.

### Check 3 (normative siting)
§21.6's table is not a blockquote, and §21.1 says "§21.6's entries restate
their governing rules on the same terms a row does, and where such an entry
and the rule it cites diverge, the rule governs there too" — so the cell is
a restatement whose authority is `[R-TYP-08]`, which is normative prose in
§13.3 and unchanged. The repair therefore lands correctly: it moves the
restatement onto the rule rather than moving the rule.

### Check 4 (contradiction in the passage)
Read all of §21.6 (3673–3717). The next row, "A requested coordinate lies
outside the layer's extents | The request fails as a request, with no
verdict on the file", is what makes the new "inside the layer's extents"
qualifier coherent rather than redundant — a position outside the extents is
not a read at all. §15.3's entry-state table ("valid sentinel — reads as
fill") and §19 step 4 ("every requested sample position of its tile reads as
fill — the entry's channel's recorded fill in a planar layer; each carried
channel's, in declared order, in an interleaved layer") both agree with the
repaired cell. `[R-TYP-09]` ("Fill is produced by exactly one condition: a
sentinel entry read from a verified index chain") is not contradicted: an
unverified chain rejects at layer or tile scope, so nothing reads.

### Check 5 (exhaustive claims)
"every sample position it carries inside the layer's extents" — bounded,
and matches the rule. "for each channel the tile carries" — a count that
varies by layout (1 for a planar entry, C for an interleaved tile), which is
exactly right and is what the old singular got wrong.

### Check 6 (what the structure leaves open)
Structure: a sentinel index entry (offset, length, crc) and the read of its
tile. offset/length — fixed to all-ones by `[R-IDX-02]`; crc — fixed to 0 by
`[R-IDX-02]`, with T6 registering crc != 0; the returned values — now fixed
by this cell + `[R-TYP-08]`; padding positions of that tile — governed by
`[R-GEO-04]` (never returned) and `[R-SER-05]` (content, though a sentinel
tile stores no bytes at all). No member of the structure is ungoverned.

### Sweep for unswept restatements (whitespace-normalized, hard wrap defeated)
Six other statements of "unstored reads as fill" exist:
1. §3 glossary: "An addressed tile that is not stored reads as fill (§13)."
   — pointer only, no detail to be wrong about.
2. §13 lead-in (line 1768–1771): "each channel it carries reads as fill at
   **every sample position** (§13.3)" — carries the per-channel half but not
   the extents half. See finding A-04.
3. §13.3 itself — the rule. Correct.
4. §15.3 entry-state table: "valid sentinel — reads as fill" — pointer only.
5. §19 read path step 4 — correct, and distinguishes the layouts.
6. §21.6 — the repaired cell.

### FINDING A-04

---

## Hunk 8 — Appendix G item 10

### Rule the repair asserts
A caller-supplied decomposed name is a different name because its **bytes**
differ, independently of whether its **length** differs; so a writer that
does not normalize emits a different layer record. (The old text asserted
the length always differs, and drew the further consequences "a different
inline_length, and a different dir_length" from it.)

### Check 1 (quantifier)
Old: "is a different name under `[R-ENC-13]` **and a different length**" — a
universal over decomposed names, falsified by any name whose NFD form
differs from its NFC form only by canonical reordering of combining marks
(same bytes, permuted; same length). New: "because its bytes differ —
whether or not its length differs with them", plus "a name differing only by
canonical reordering is the same length in both forms". The quantifier now
matches `[R-ENC-13]`'s, which is stated over bytes, not lengths.

### Check 2 (citations)
- `[R-ENC-13]` (§4.6, line 558–560): "Name comparison is raw bytes: two
  names are the same name if and only if their encoded byte sequences are
  identical. Readers MUST NOT normalize, case-fold, or otherwise transform
  names for comparison." VERDICT: supports "a different name ... because its
  bytes differ" exactly; and it is byte identity, never length, so the old
  "and a different length" was never this rule's ground.
- `[R-ENC-14]` (line 561–563): "Writers SHOULD emit names in Unicode
  Normalization Form C". VERDICT: "which `[R-ENC-14]` states as a SHOULD" is
  right.
- §4.6 (the `température` Example, lines 576–581): 12 bytes NFC, 13 bytes
  NFD. VERDICT: the figures match. Note the Example is a labelled blockquote
  (non-normative), which is fine — item 10 is itself non-normative and only
  borrows the illustration.

### Check 3 (normative siting)
Appendix G is headed "Reproducible-writer profile (**non-normative**)" and
says outright "It adds no requirement to any actor". The repair therefore
imposes nothing; the rules it leans on (`[R-ENC-13]`, `[R-ENC-14]`) are in
§4.6's normative prose and unchanged. Nothing normative restated the old
false "and a different length" claim: `grep` of "R-ENC-13"/"R-ENC-14" gives
560, 563, 579, 2646, 2814, 3276, 3511, 4465, 4483 — line 2646 (§18: "two
keys differing only in Unicode ..."), 2814, 3276 and 3511 (F4: "comparison
is raw bytes, no normalization") are all byte-based and none asserts a
length consequence. Sweep clean on the corrected claim.

### Check 4 (contradiction in the passage)
Read items 8, 9, 10 and the closing paragraph (4425–4495). The closing
paragraph lists "NFC-normalized names, which `[R-ENC-14]` states as a
SHOULD" — consistent. Item 9 pins user-metadata serialization by pinning a
JSON writer and (for encoding 2) a zstd build; it does not pin key
normalization, which is item 10's job — see check 6.

### Check 5 (exhaustive claims)
- "whether or not its length differs with them" — correctly refuses to make
  a universal claim about length.
- "a name differing only by canonical reordering is the same length in both
  forms" — true: canonical ordering permutes combining marks without adding
  or removing code points; only composition/decomposition changes length.
- "So a writer that does not normalize emits a different layer record." —
  true for a layer, dimension or channel name, all of which live in the
  layer record's inline payload (§7.4 layout, line 1084). See check 6 for
  the fourth kind of name.

### Check 6 (what the structure leaves open)
Structure: item 10 governs **names**. §4.6 defines names as "the strings
that identify layers, dimensions, channels, **and user-metadata keys**", and
`[R-ENC-14]`'s SHOULD is stated over names, so item 10 reaches all four
kinds. The repaired consequence names one carrier — the layer record —
which covers three of the four. A caller-supplied non-NFC user-metadata key
changes the metadata document's bytes, hence the record's extent, not the
layer record; item 9 does not close it (pinning a JSON writer does not
normalize the caller's key bytes). See finding A-05.

### Check 7 (analogy)
Warrant is `[R-ENC-13]`. Repair verb: "is a different name ... because its
bytes differ". Rule verb: "two names are the same name if and only if their
encoded byte sequences are identical." Same relation, contrapositive, same
set (names). Comparison passes. The old text's implicit warrant — that a
length difference is what makes it a different name — is exactly the
mismatched quantifier this hunk removes.

### FINDING A-05

---

## Findings

### A-01 — hunk 3 — §21.1: "F1 of F6 and of F8" contradicts the property the same sentence states, and the negative sentence next to it

Repaired text, verbatim:
"Some rows are strict specializations of others: where every file exhibiting
one row's condition necessarily exhibits another's, the file is recorded
against the narrower row, whose detector and detection point are the ones
that apply. F1 of F6 and of F8, F35 of F36, L24 of L25, F21 of F22 and L10
of L11 stand in that relation; the property decides any pair and this list
is not offered as closed. Rows that merely overlap, each reachable without
the other, do not stand in it."

F1 (line 3511): "A signature constant is stored byte-reversed — never to be
adapted as a foreign-endian TARN file; the front-block instance binds only a
reader holding bytes [0, 16) resident (`[R-CNT-04]`), the trailer-magic
instance every reader (`[R-CNT-06]`) | front signature block bytes [0,8);
trailer magic at F-64 | reader | open | `[R-ENC-02]` (R-CNT-04, R-CNT-06)".
F6: "The 16-byte front signature block is not byte-identical to the
constant..."  F8: "The 8 bytes at F-64 are not exactly the trailer magic
8A 4E 52 41 54 0D 0A 1A".

F1 is one row with two independent instances. Take a file whose trailer
magic at F − 64 holds `1A 0A 0D 54 52 41 4E 8A` (the constant reversed) and
whose front block is the correct `89 54 41 52 4E 0D 0A 1A` + eight zero
bytes. It exhibits F1 (trailer-magic instance) and does **not** exhibit F6.
So it is false that every file exhibiting F1's condition necessarily
exhibits F6's. Symmetrically, a file with the front block reversed and a
correct trailer exhibits F1 but not F8. And F6 is reachable without F1 (any
non-zero byte in [8,16)); F8 is reachable without F1 (trailer magic replaced
by arbitrary bytes). So F1/F6 and F1/F8 are precisely the case the third
sentence excludes — "rows that merely overlap, each reachable without the
other" — while the second sentence asserts they stand in the relation.
Neither magic is a palindrome (checked: §6.1's `89 54 41 52 4E 0D 0A 1A`
reversed is `1A 0A 0D 4E 52 41 54 89`; F8's `8A 4E 52 41 54 0D 0A 1A`
reversed is `1A 0A 0D 54 52 41 4E 8A`), so the per-instance containments do
hold — the relation the old closed list encoded was instance-level, and the
property that replaced it is row-level.
The old text ("Some rows are strict specializations of others — F1 of F6 and
of F8, F35 of F36, L24 of L25 — and a file exhibiting a specialization is
recorded against the narrower row") asserted the list without deriving it,
so no contradiction existed. Deriving the property created one.
Repair: quantify over (row, instance) pairs, or restate the F1 entries as
"F1's front-block instance of F6 and its trailer-magic instance of F8". The
same fix covers the two union-shaped rows my sweep found (T15, whose check
is "T24's or T25's", and T26, whose check is "T2's or T4's"), which the
row-level property likewise cannot express.
Byte-level: NO. Under either reading the file is nonconforming and is
rejected at open; F1's front-block instance and F6 carry the same residency
exemption (`[R-CNT-04]`) and F1's trailer instance and F8 both bind every
reader at open, so no detector, detection point, outcome or emittable byte
sequence moves. It is a defect in the register's bookkeeping and in the
clause's internal consistency, not in the bytes.

### A-02 — hunk 5 — §21.4: "the governing rule states what a reader does" is false for T26

Repaired text: "...where a row's Detector is *verifier* no reader is obliged
to detect the condition, and the governing rule states what a reader does."
§21.4's verifier rows are T2, T4, T5, T26. T26's Governing rule cell names
`[R-COD-10]` first (R-SER-05 follows in parentheses, which §21.1 defines as
"the further rules the condition reads", not the governing one).
`[R-COD-10]` in full (§17.3): "A writer that filters with any other stride
violates this rule; where the resulting decoded image breaks a stated
content obligation (§14.5's padding, `[R-SER-08]`'s bool bytes) a verifier
detects it as a validity error at tile scope, and otherwise the consequence
is wrong sample content — undetectable by construction (§21.7)." It says
what a writer does and what a verifier does; it says nothing about a
reader. T2's rule (R-SER-08) and T4/T5's rule (R-SER-05) both do.
The claim is inherited from §21.1's identically-worded sentence, so the
repair replicated an existing overclaim into the subsection where its one
counterexample lives rather than introducing a new one.
Repair: "...and where it does, the governing rule states what a reader does
(T2, T4, T5); for T26 the reader's behaviour follows from the rows whose
checks detect it, T2's and T4's." Or drop the second conjunct and rely on
§21.1.
Byte-level: NO. A reader is not obliged to detect T26 under either reading,
and `[R-CNF-12]`/§2.4 already permit a reader that does detect a verifier
row to reject. No accept/reject verdict and no emittable byte changes.

### A-03 — hunk 5 — §21.3's preamble carries the same unqualified claim the repair removed from §21.4, and §21.1 contradicts it

The repair qualified §21.4's outcome sentence for verifier rows. The
parallel sentence one subsection earlier was not swept. §21.3 (line
3604-ish, unchanged): "Outcome: reject-layer — **the named layer is
unusable**, every other layer unaffected. 49 conditions."
§21.3 contains eight verifier rows: L18, L40, L41, L42, L46, L47, L48, L49.
§21.1 says of them: "For a row whose Detector is *verifier*, the outcome
names the scope at which the damage is recorded, not an obligation on any
reader: the governing rule states what a reader does, and for several such
rows it obliges the reader to serve the structure unchanged (`[R-CNT-22]`,
whose registered type keeps its fixed semantics; and `[R-MTA-05]`, whose
unsorted document readers process as they find it — **F27 and L48**)."
L48 is a §21.3 row, and L49 (`[R-CNT-22]`) another. For a file exhibiting
L48, §21.3's preamble says the named layer is unusable; §21.1 and
`[R-MTA-05]` say readers process the document as they find it and nothing
about the layer is refused. §21.2's preamble ("Outcome: reject-file. 36
conditions.") carries no gloss and so has no equivalent problem; §21.5's was
already carefully qualified. §21.3 is the one left standing.
Repair: give §21.3 the same clause §21.4 now has — "...for a rejection the
reader is obliged to detect; where a row's Detector is *verifier* no reader
is obliged to detect the condition, and the governing rule states what a
reader does."
Byte-level: NO. A file exhibiting L48 or L49 is nonconforming, so
`[R-CNF-05]` bars every conforming writer from emitting it under both
readings; and §2.4's "For a nonconforming file no acceptance obligation
exists — a reader MAY reject it upon detecting any violation, including
violations whose assigned detector is the verifier" already licenses both
reader behaviours. The emittable set and the verdict set do not move.

### A-04 — hunk 7 — §13's lead-in restates the sentinel rule without the extents qualifier the repair just added

§13 lead-in (line 1768–1771, normative prose, not a blockquote): "Fill is
what makes sparse layers first-class: an addressed tile that is not stored
(§3.1) occupies no payload bytes, and reading it is defined behavior — each
channel it carries reads as fill **at every sample position** (§13.3) —
rather than an error."
`[R-TYP-08]` bounds this to positions "inside the layer's extents", and
`[R-GEO-04]` bars returning padding positions at all. The §21.6 cell was
repaired for exactly this omission; §13's lead-in still carries it. It does
carry the per-channel half correctly ("each channel it carries"), so it is
the weaker half of the same drop, and it cross-references §13.3, which is
mitigating.
Repair: "...reads as fill at every sample position inside the layer's
extents (§13.3)".
Byte-level: NO. `[R-GEO-04]` and §19 step 7 bar returning padding positions
for stored and unstored tiles alike, so no reader that follows the rest of
the document returns a different byte under either reading.

### A-05 — hunk 8 — item 10 governs four kinds of name; the repaired consequence covers three

Repaired text: "A caller-supplied decomposed name is a different name under
`[R-ENC-13]`, because its bytes differ — whether or not its length differs
with them. §4.6's `température` is 12 bytes in NFC and 13 in NFD, while a
name differing only by canonical reordering is the same length in both
forms. So a writer that does not normalize emits **a different layer
record**."
§4.6: "**Names** — the strings that identify layers, dimensions, channels,
**and user-metadata keys** — satisfy three further constraints", and
`[R-ENC-14]`'s SHOULD-NFC is stated over names. Item 10's heading is
"Names normalized to Unicode Normalization Form C". Layer, dimension and
channel names all sit in the layer record, so "a different layer record"
covers three of the four. A non-NFC user-metadata key changes the
document's bytes and hence the record's extent, not the layer record; item 9
pins the JSON writer and the zstd build but cannot normalize a caller's key
bytes, so nothing else in the profile closes it. The old wording had the
same gap, but the repair rewrote this sentence and narrowed the consequence
to a single carrier without widening the coverage.
Repair: "...emits a different layer record — or, for a user-metadata key, a
different document and so a different extent."
Byte-level: NO. Appendix G is non-normative and "adds no requirement to any
actor"; a writer ignoring it is fully conforming under both readings.

---

## Checks that passed, stated per check

1. TENSE AND QUANTIFIER — passed on hunks 1, 2, 4, 6, 7, 8; on hunk 5 the
   dropped `[R-CNF-09]` qualifier is correctly restored word for word; on
   hunk 3 it fails (A-01), because the property is quantified over rows
   while two of its own examples hold only over instances.
2. CITATIONS RESOLVE — every identifier and section number in the repaired
   text opened and read; all resolve (list in the structured output). No
   citation points at a rule that only nearly says the claimed thing.
3. NORMATIVE SITING — hunks 2–7 sit in normative prose or normative tables
   and the rules they restate are normative and unchanged. Hunk 1 edits a
   labelled Note and hunk 8 a non-normative appendix; neither states a rule,
   and in both cases the normative statement elsewhere already says the
   corrected thing, so nothing was repaired into a place with no force.
4. NO CONTRADICTION IN THE SAME PASSAGE — read each whole structure. Two
   failures: A-01 (inside the repaired sentence itself) and A-03 (§21.3
   untouched but now out of step with §21.4 and already out of step with
   §21.1).
5. NO EXHAUSTIVE CLAIM IT CANNOT CARRY — every completeness word tested.
   One failure: A-02 ("the governing rule states what a reader does").
   "At either scope", "the two are the same length", "exactly when that fill
   is false", "one of the frame constraints R4 registers", "several", "not
   offered as closed", and the 26/121 counts all hold.
6. WHAT ELSE IS STILL UNCONSTRAINED — structures enumerated member by member
   for all eight hunks. One gap: A-05 (item 10's fourth kind of name).
7. ANALOGY QUANTIFIERS — four hunks argue from a warrant (1: R-SER-05;
   2: R-WRT-06; 5: R-CNF-09; 6: §18.2/R-MTA-09; 7: R-TYP-08). Verbs quoted
   side by side above; all five comparisons pass, including hunk 6's tested
   separately against each of R4's seven constraint families.
