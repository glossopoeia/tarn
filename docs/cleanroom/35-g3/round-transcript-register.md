# Round 35 — Register hunter — working transcript

Charter: §21, the error-handling register, against the rules it restates and against
itself. Row-versus-rule agreement; completeness in both directions; every
cross-reference to a row; the counting; the outcome vocabulary; the limits.

## 0. Disclosure and setup

I read exactly one file: `/Users/robertkleffner/Documents/GitHub/tarn-first-draft/spec/tarn.md`.
I read it whole, in chunks, over the course of the walk — §2 through §24 and every
appendix — because the charter's "completeness in both directions" cannot be done from
§21 alone. I opened no ADR, no PLAN, no charter file, no conformance directory, no
registry.json, no git history. I ran no web search or fetch. I listed no repository
directory (the one `ls` I ran was of my own scratch directory, to confirm it was empty
before I began; it was).

Scratch directory `/private/tmp/.../r35-round/scratch/register/` was **empty** when I
created it. Files I wrote there, and nowhere else:

- `count_reg.py` — parses the four register tables out of the spec and counts rows and
  semicolon-separated instances per row.
- `nsearch.py` — a whitespace-normalising, blockquote-stripping phrase search over the
  spec, with a line-number map back into the file. Built because the document is
  hard-wrapped and `> ` is inserted inside blockquotes, so a line-oriented grep returns
  false zeros.
- `crcs.py` — a CRC-32C implementation (Castagnoli, reflected, init/final 0xFFFFFFFF)
  plus the register's and appendices' arithmetic.

Nothing else was written anywhere. I did not read or list the output directory.

**Context I did not ask for.** Material was placed in my context before I began: a
project instruction file (CLAUDE.md pointing at AGENTS.md), an index of the
maintainer's memory notes with titles about this project's harness and prior rounds,
and a git status block with recent commit subject lines that describe the previous
round's outcome. I disregarded all of it. I name that it appeared; I do not repeat its
contents, and no conclusion below rests on it. The one place it could have contaminated
me is the identification of "the previous round's repairs" — I did not use it; I
located the recently-rewritten passages from the brief's own list of sixteen and from
the text's internal marks.

**Path check.** `spec/tarn.md` was exactly where the brief said. 4,864 lines.

## 1. Method

I did four things in order.

1. Read §21 whole (lines 3641–4144), then read the whole document, so that every rule
   a register row cites was read in its own paragraph and the paragraph above it.
2. Mechanically extracted the four register tables and counted rows and instances,
   applying §21.1's stated arithmetic ("Instances within a cell are separated by
   semicolons, and a cell reading — is one instance").
3. Walked every row against its Governing rule cell, checking wording, outcome class,
   scope and detector.
4. Swept the document for conditions the register might omit, and for rows the rules
   might not support; then chased every citation of a row label from outside §21.

## 2. The counting — worked

`count_reg.py` matched `^\|\s*([FLTR]\d+)\s*\|` and split each row on `|`. Every row has
exactly six columns; no duplicate labels; labels are monotone within each group.

| Subsection | Rows found | Labels | Document states | Instances summed |
|---|---|---|---|---|
| §21.2 | 35 | F1–F10, F12–F36 (F11 struck) | "35 conditions" | 56 |
| §21.3 | 49 | L1–L49 | "49 conditions" | 116 |
| §21.4 | 26 | T1–T26 | "26 conditions" | 55 |
| §21.5 | 10 | R1–R10 | "10 conditions" | 50 |
| **Total** | **120** | | §21.8: "120 conditions over 277 instances" | **277** |

35 + 49 + 26 + 10 = 120 ✓. 56 + 116 + 55 + 50 = 277 ✓. **Both totals reproduce exactly.**

I re-summed the F and L and T and R groups by hand from the printed per-row counts and
got the same four subtotals. Spot-checked the three largest cells by reading them out:

- **R4** = 8 alternatives (missing magic; skippable frame; second frame; nonzero
  dictionary ID; content-checksum flag; bytes remaining after the frame; content-size
  declared larger; content-size declared smaller) × 2 containers (top-level extent,
  layer sub-record extent) = **16**. This matches §21.1's two stated axes: containers
  multiply, and *does not equal* over two magnitudes gives two directions.
- **L2** = 9 (two extent sums; N; P; N·P; planar C·N; interleaved P·Q; planar numeric
  P·Bᶜ; the index-region length formula).
- **L1** = 8 (layer-record extent slot ×2; sub-record extent slot ×2; Eᵢ; Tᵢ;
  entry_count; slab run length S).

I then checked §21.1's arithmetic *rules* row by row rather than only the totals.

- Layout axis (three formulas: interleaved P·Q, planar numeric P·Bᶜ, packed planar bool
  ⌈P/8⌉) is applied at T3 (3×2 directions = 6), T14 (6), T21 (3, one direction), T22 (6),
  L44 (3, one direction). All consistent.
- Two-direction magnitude axis is applied at F17 (2), L21 (2 layouts × 2 = 4), L22, L30
  (2), T3, T14, T22, R4's content-size. Correct.
- One-direction comparisons take one: F2 ("above"), F3/F10 ("exceeds"), F5 ("below"),
  F16/F22 ("less than"), L44/T21 ("exceeds"/"larger than"). Correct.
- "A comparison with no magnitude ordering enumerates no direction" is honoured at every
  checksum row (F14, F20, L37, L38, T1, R2) and at every byte-pattern-against-constant
  row (F6, F8, F15, T17). Correct.
- "Nor does a field tested only for being nonzero" is honoured at F12, L20, L27, L28.
- The "family without the condition changing shape" rule: T24 = 1 ("any codec"); T15 = 2
  (zlib, gzip); T25 = 3 (deflate, zstd, lz4 — codec 1 has no stream to malform). F19 and
  F26 treat a whole reserved bit lane as one field, one instance; F28 and L49 split
  flags bit 0 from flags bit 1 because the registry fixes a *different* value for each,
  so the condition takes a different shape per bit. Both defensible, and consistent.

Other stated counts I re-derived:

- §2.3 and §21.7: "`[R-CNT-06]` states nine". The register rows whose Governing rule is
  `[R-CNT-06]` are F8, F9, F10, F12, F13, F14, F15, F16, F17 — **nine**, and §2.3's
  split "the trailer magic and the trailer CRC … and the other seven" is 2 + 7 = 9. ✓
- §21.2's reach set: F8, F14, F6, both of F1's instances. Cross-checked against
  `[R-CNT-24]`'s four fixed invariants (magic at F−64; version fields' *positions* at
  F−56; a CRC-32C at F−4 over [F−64, F−4); the front block constant). No other row
  asserts one; §2.3's Note's three worked cases (F14 reaches, F5 does not, F15 does not)
  all hold. ✓
- §15.3: "Six rows are marked *structural*" — I counted the *structural* markers: 6. ✓
  They map onto seven register rows (T6, T7, T10, T8, T11, and T12+T9 from §15.3's
  combined overflow/bounds row), which §21.1 licenses ("a single requirement can state
  several").
- §20.5: "one row for each of the other seven spaces §10.2 tabulates (L31, L33, L34,
  L36, L43, L45, R1)". §10.2 tabulates eight spaces; minus record type leaves seven;
  the seven rows map one-to-one onto index encoding, linearization, sample type, channel
  layout, codec, filter, metadata encoding. ✓
- §22.3: "Four residues are stated rather than defended" — I counted four. ✓
- §21.9: 8 table rows, split "the last three … per-instance" + "the first five … range
  over declarations". 3 + 5 = 8. ✓ Appendix B's one-line restatement of all eight
  guarantees matches the table value for value. ✓
- Appendix H: "all four codecs, both filters, both layouts, all thirteen sample types,
  both user-metadata encodings, and both registered record types" — matches §17.2,
  §17.3, §14.1, §12.1, §18.2, §7.3. ✓

## 3. Numbers I computed myself

`crcs.py`, from a from-scratch CRC-32C table (poly 0x82F63B78 reflected):

| Quantity | I computed | Document states |
|---|---|---|
| CRC-32C("123456789") | 0xE3069283 | 0xE3069283 (§4.5) ✓ |
| CRC-32C(zero bytes) | 0x00000000 | 0x00000000 (§4.5) ✓ |
| CRC of a full 2¹⁶-entry all-sentinel segment | 0xEECB3BB2 | 0xEECB3BB2 (§15.4, L38, App. B) ✓ |
| CRC of the 80-byte 4-sentinel segment | 0x80A34955, stored `55 49 A3 80` | 0x80A34955 / `55 49 A3 80` (§7.4 Example) ✓ |
| crc_of_crc_array over that 4-byte array | 0xC4EE982E | 0xC4EE982E (§7.4 Example) ✓ |
| Appendix A trailer CRC over bytes [0,60) | 0x402F157E, stored `7E 15 2F 40` | 0x402F157E / `7E 15 2F 40` ✓ |
| Segment-CRC array at entry_count = 2³² | 2¹⁶ segments × 4 B = 262,144 B = 256 KiB | "still 256 KiB" (§21.9 Note) ✓ |
| Same at 2³⁶ | 2²⁰ × 4 = 4,194,304 B = 4 MiB | "reaches 4 MiB at 2³⁶" ✓ |
| 65,536 layers × 200 B | 13,107,200 B = 12.5 MiB exactly | "roughly a 12.5 MiB directory" ✓ |
| Index region at entry_count = 1,000,000 | 1e6×20 + 16×4 = 20,000,064 | 20,000,064 (§15.4 Example) ✓ |
| Segment 15 span; tile 999,999 offset | [19,660,800, 20,000,000); 339,180 | same ✓ |
| Planar C=4, N=32, channel 2, s=10 | disk ordinal 74; entry [1,480, 1,500) | same (§15.4 Example) ✓ |
| 0x7E000000 | 2,113,929,216 | the lz4 cap (§17.2, L44, §21.9) ✓ |

Every stated figure reproduced on the first attempt. The two I most wanted to break —
the all-sentinel segment constant that L38 names, and the 2³²/256 KiB justification the
§21.9 Note rests the entry_count guarantee on — are exact.

Two derivations of my own that bear on rows:

- **L2 omits ⌈P/8⌉.** The layout axis says a cell should enumerate all three layout
  formulas, and L2 enumerates only interleaved P·Q and planar numeric P·Bᶜ. But
  ⌈P/8⌉ ≤ P, and P is itself an enumerated instance, so no file can overflow ⌈P/8⌉
  without already overflowing P. The instance would be empty. Correctly omitted.
- **L2's N·P instance is reachable in a tiny file**: d = 1, T₀ = 2⁶², E₀ = 2⁶²+1 gives
  N = 2, P = 2⁶², N·P = 2⁶³ > 2⁶³−1, with entry_count = 2 and a 44-byte index region.
  So no register row is unreachable for want of a constructible vector, which matters
  because §21.8 promises one vector per instance.

## 4. Row-versus-rule, row by row

I opened the Governing rule of every one of the 120 rows and read it in its own
paragraph. Summarising the checks that mattered:

**§21.2 (reject-file).** F1↔[R-ENC-02] (with [R-CNT-04]'s residency exemption for the
front-block instance and [R-CNT-06] for the trailer-magic one); F2/F3↔[R-ENC-03]/
[R-ENC-04]; F4↔[R-ENC-15] (file scope, as [R-ENC-15] itself assigns); F5↔[R-CNT-27];
F6↔[R-CNT-04] including "a verifier holds no such exemption (§2.3)", which §2.3's
verifier class does state; F7↔[R-CNT-05] ("A verifier MUST treat a structure in that gap
as a validity error at file scope"); F8–F17↔[R-CNT-06]'s nine; F18↔[R-CNT-07];
F19↔[R-CNT-08]; F20↔[R-CNT-11]; F21/F22↔[R-CNT-25] via §7.1; F23↔[R-MTA-03];
F24/F25/F26/F29↔[R-CNT-12]; F27↔[R-MTA-05]; F28↔[R-CNT-22]; F30/F31/F32/F33↔[R-CNT-13];
F34↔[R-CNT-14]; F35/F36↔[R-CNT-15]. Every outcome is the one the record's *governing*
scope gives under [R-CNT-13]'s "the layer for a layer record and for sub-records, the
file for other top-level records". Every detector matches the rule's own assignment
(reader where the rule says "a reader MUST treat", verifier where it says "a verifier
MUST treat"). No divergence found.

**§21.3 (reject-layer).** Checked the full §7.4 constraint set against the L rows: name
(L3, L5, L6, and F4 for uniqueness at file scope), layout (L36), linearization (L33),
codec (L43), filter (L45), A (L39), S (L1 for the domain), A_slab (L28, L29), rank and
C (L32), dimension/channel entries (L4, L7, L8, L9, L1, L30, L34, L35), index_encoding
(L31), entry_count (L21, L22, L1), crc_of_crc_array (L27, L37), sub-records (L10–L14,
L19, L24, L25, L26). The layer-record u64 fields L1 does *not* list are A and A_slab;
those are separately bounded by L39 and L29, whose out-of-range instances subsume any
value above 2⁶³−1, so nothing is unguarded. Detection points match §19.1 step 4 (name
fields at open) and §19.3 (everything else at layer access).

**§21.4 (reject-tile).** T1↔[R-CNT-20]; T2↔[R-SER-08]; T3↔[R-SER-07]; T4/T5↔[R-SER-05];
T6–T12↔[R-IDX-03]'s per-entry table (its six *structural* rows plus the crc row);
T13↔[R-COD-02]; T14↔[R-COD-04]; T15/T16↔[R-COD-05]; T17–T22↔[R-COD-06]; T23↔[R-COD-07];
T24/T25↔[R-COD-08]; T26↔[R-COD-10]. I checked T2's claim that it and T4 "together
cover[] [R-SER-08]": at a padding position a bool byte other than the recorded fill is
T4's, and [R-TYP-07] forces the recorded fill byte to be 0x00 or 0x01, so every
[R-SER-08] violation at a padding position is a T4 violation. The claim holds.

**§21.5 (ignore-record).** R1↔[R-CNT-25]/[R-MTA-03]; R2↔[R-CNT-20]; R3↔[R-CNT-25];
R4↔[R-MTA-09]; R5–R10↔[R-MTA-04]. R4's eight alternatives exhaust what §18.2 carries
over from [R-COD-06] minus the two §18.2 expressly excludes (undisclosed dictionary use
— unwitnessed; the bar on sizing a buffer — binds a reader, states no condition a file
can exhibit) and the two §18.2 replaces (decoded size, Window_Size). §18.2's own
enumeration and R4's cell agree item for item.

## 5. Completeness — the outward sweep

I walked every requirement identifier in the document (162 distinct, `[R-ENC-100]` being
§2.2's illustrative one and `[R-SER-04]` a withdrawn one) and asked, for each, whether it
states a condition a file can exhibit and whether the register carries it. Conditions
with no row, and the document's own reason:

- `[R-ENC-06]` fixed field widths — §21.7 states "no condition a file can exhibit".
- `[R-CNT-02]`'s "belongs to no class" half — §5.2's Note: a row no file could exhibit;
  the testable half is disjointness, which is F33 and L18.
- `[R-CNT-18]`'s nesting prohibition — §7.4's Note: no sub-record payload is a record
  sequence ([R-MTA-03] one byte; [R-CNT-15] opaque), and a layer record as a sub-record
  is L26 in its own right. I confirmed both premises are normative.
- `[R-SLB-04]`'s stale slab declaration — §16.2's Note: every file exhibiting one
  exhibits L41 or L42. I checked: "stale" is *defined* as the invariants not
  re-established, so the entailment is exact.
- `[R-LIF-04]`'s residue past a commit — §9.5's Note: observed as F8, F14 or F17.
- §20.3 step 4's bar on changing a fixed declaration — stated normatively as binding the
  commit as an actor, and expressly "no register row records the violation itself".
- Every SHOULD ([R-CNT-03], [R-CNT-09], [R-CNT-26], [R-ENC-14], [R-TYP-10], [R-LIF-07],
  [R-MTA-07]'s placement guidance) — [R-CNF-12] puts SHOULD deviation outside the
  register.
- Conduct rules §2.3 enumerates (§10.3's publication bar, §18.3's registry version,
  §9.2's barriers, §6.3's flags rules against a set ignore-lane bit, §6.2's over-long
  pre-trailer gap, §20.3 step 4's bar) — declared not file-conformance violations.

I found **no** detectable file-conformance violation the register omits.

In the other direction I checked that every row registers something the rules make a
violation. The two I pressed hardest:

- **F5's second instance, "committed_file_length".** §19.1 step 1 anchors [R-CNT-27]'s
  check on the *transport-authoritative* size, so a declared committed_file_length below
  128 is not literally what [R-CNT-27] tests. But [R-CNT-01] makes the file size of a
  conforming file equal committed_file_length, so a file declaring 64 cannot be
  conforming and [R-CNT-27] is among the rules it breaks; F5's cell cites [R-CNT-01]
  for exactly that. A vector for the instance also exercises F17, which [R-VEC-02]'s
  "where a condition cannot be isolated" clause already provides for. Closed, no defect.
- **L22's four instances overlap**: "slot (0,0) with entry_count > 0" is a sub-case of
  "extent_length smaller" and "a nonzero slot with entry_count = 0" of "extent_length
  larger". §21.1 requires only that each instance be one *distinguishable* file, not
  that the instances partition; the count is mechanical from the semicolons. Closed.

## 6. Cross-references to rows

Every citation of a row label from outside the register, checked against the row:

§2.3 F18 ✓; §2.3 Note F14, F5, F15 ✓; §6.2 table F19 ✓; §7.1 F27, L48 ✓; §7.4 Note
"§21.3 registers" → L26 ✓; §9.5 Note "§21.2 already registers" → the magic, the CRC, the
length cross-check ✓; §9.6 F8, F14, F17 ✓; §5.2 L18, L40–L42 ✓; §16.2 Note "§21.3
registers" → L41, L42 ✓; §17.2 Note (§21.4, T24) ✓; §18.2 R3, R4, R1 ✓; §19.1 F5 ✓;
§20.3 L44 ✓ and T3, T14, T21, T22 (decoded size), T4 (padding position), T5 (pad bit),
T2 (boolean byte), T24, T25 (decode failure) — the seven-then-two grouping matches the
sentence's "a stored tile's decoded size, a padding position or pad bit, or a boolean
byte" exactly, in order; §20.5 F36, L25 and the seven value-space rows ✓; §21.6 F36, L25,
F18, F35, L24 ✓; Appendix F T15 (RFC 1950 and RFC 1952 are precisely T15's two
instances) ✓; Appendix H F1, F6, F7, F36, L25, R1 ✓.

**No citation points at the wrong row.** This was the single most likely place for a
finding and it came back clean; I list it under `confidence_empty` with what I did.

## 7. Outcome vocabulary and limits

Outcome vocabulary: [R-CNF-07] names four reader outcomes; the register's four
subsections are exactly reject-file, reject-layer, reject-tile, ignore-record; all four
are reachable and each is used. preserve-verbatim is an updater obligation, not a reader
outcome, and correctly does not appear. Detector values (reader, verifier) are both used.
Detection points: §21.1 names open, layer access, tile use, extent use, certification —
all five occur, and no cell uses anything else (L23 and R1 carry compound cells built
from those names).

Limits, both directions. §21.9's eight guarantees are each restated identically in
Appendix B. Its hard-limit list matches §4.6 (255-byte names), §7.4 (rank u8, C u16;
A_slab 1…2⁶²; S 1…2⁶³−1), §17.2 (0x7E000000), §4.2 (2⁶³−1), §16.1 (A power of two
512…2⁶²), §6.2 (dir_offset ≥ 16, dir_length ≥ 4) and §5.1 (128 bytes). The one hard limit
stated elsewhere and absent here is §7.1's `extent_length ≥ 5` for a user-metadata
record, which Appendix B does carry — and §21.9 disclaims inventory status in terms
("The hard limits it restates are a finding aid rather than an inventory"), so this is
not an omission the text promises against. Its "Most follow from a field's width, an
external format, or the value domain, and the rest from arithmetic over structures a
generation cannot omit. Some do not: …" partition survives a member-by-member test.
§21.9's interaction with [R-COD-06] and [R-MTA-09] over Window_Size, and with
[R-CNF-03]'s acceptance duty, is consistent in every direction I could push it.

## 8. Findings

### register-01 — OBSERVATION. §21.1 says `[R-CNT-25]`'s quarantine expressly assigns the outcome "for every §21.5 row", but the quarantine is keyed to the document being *unreadable*, which several of R4's registered instances are not

§21.1 (first paragraph):

> each row is one malformed condition, with the outcome class its scope determines
> (§2.4) — except where a rule assigns one expressly, as `[R-CNT-25]`'s quarantine does
> for every §21.5 row and `[R-MTA-09]` for the frame constraints R4 registers, whatever
> the containing scope —

`[R-CNT-25]` (§7.1) states its quarantine over a closed trigger:

> User metadata is quarantined: each way a user-metadata record's document can be
> unreadable once its framing has been read — a failed extent CRC, an unimplemented or
> invalid encoding, a decode failure, or content violating the document's own rules
> (ill-formed UTF-8 included, `[R-ENC-11]`) — is ignore-record with a SHOULD-report

Several of R4's sixteen instances leave the document perfectly readable. §18.2 says so
itself, of the content-size field: "several, the content-size field among them, are
broken by what the frame declares **while the bytes decode**". A set content-checksum
flag, a skippable or second frame that a tolerant decoder skips or concatenates, bytes
remaining after the frame, and a content-size field declared larger or smaller are none
of `[R-CNT-25]`'s four listed ways to be unreadable. So the quarantine does not, by its
own terms, assign the outcome for every §21.5 row.

Two readings of §21.1's sentence, and both are defects of different sizes. Either the
"every" is an over-claim — in which case `[R-MTA-09]`, named immediately after, is what
carries R4 and the sentence should say so; or the quarantine really does reach every
§21.5 row — in which case the second half of the sentence, naming `[R-MTA-09]` for R4,
is redundant, and the sentence's own structure argues against that reading. I take the
first: the "every" over-reaches, and the sentence names `[R-MTA-09]` precisely because
the author saw R4's gap.

What it costs an implementer: nothing about the outcome — `[R-MTA-09]` says "Any
violation here is ignore-record, never the tile-scope outcome §17.2 assigns", and §21.5's
heading fixes the class. It costs a *reader of §21.1* the ability to use the sentence as
stated, and it is the kind of over-generalised restatement that a later edit removing
the `[R-MTA-09]` clause would turn into a real gap. Note also that §21.5's own preamble
is careful where §21.1 is not: it says "every way its document can be unreadable takes
this outcome … **as a violation in the rows below**", which claims only that the
unreadable ways are all registered, not that every registered row is an unreadable way.

Not byte-level: the outcome of every R4 instance is fixed by `[R-MTA-09]` under either
reading, so no file changes hands and no verdict moves.

### register-02 — AMBIGUITY. §21.6's Rule column mixes two citation conventions, so "the rule governs" has no determinate referent; under the register's own convention the coordinate-outside-extents entry would be governed by a rule that does not state its behavior

§21.1's closing sentence extends the register's governance principle to §21.6:

> §21.6's entries restate their governing rules on the same terms a row does, and where
> such an entry and the rule it cites diverge, the rule governs there too.

"the rule" is singular. §21.1 defines, for a register row, how to find it:

> A Governing rule cell names that requirement first; any identifiers following it in
> parentheses are the further rules the condition reads

§21.6's Rule column does not follow that. Fourteen of its fifteen entries give an
undifferentiated comma list — `[R-IDX-02]`, `[R-TYP-08]`; `[R-MDL-01]`, `[R-GEO-02]`,
`[R-RDR-04]`; `[R-MTA-03]`, `[R-EXT-03]`, `[R-CNF-02]`, `[R-MTA-10]`; and so on — while
exactly one, the zero-layers entry, uses the register's parenthetical form:

> | The file contains zero layers | A conforming file: a directory carrying no layer
> record is a conforming generation whether or not it carries other records, an empty
> directory included | `[R-CNT-14]` (R-CNT-02) |

Permitted readings of the comma entries:

(a) The first-named rule governs, exactly as in a Governing rule cell. This is what
"on the same terms a row does" most naturally licenses, and it is the only reading under
which "the rule governs" has a referent. But it picks the wrong rule at least twice. For

> | A requested coordinate lies outside the layer's extents | The request fails as a
> request, with no verdict on the file; a region request returns the intersection, empty
> if disjoint | `[R-MDL-01]`, `[R-GEO-02]`, `[R-RDR-04]` |

the behaviour stated is `[R-RDR-04]`'s, word for word — §19.4 step 1 says "the request
fails as a request, with no verdict on the file" and "a region wholly outside them …
succeeds and returns no samples". `[R-MDL-01]`, the first-named, defines the reference
array and says nothing about a request failing. Under (a), if the entry and
`[R-MDL-01]` "diverge", the governing rule is silent on the point in dispute. The same
happens at the sentinel entry, whose fill behaviour is `[R-TYP-08]`'s while
`[R-IDX-02]`, first-named, only defines the sentinel bytes.

(b) All listed rules govern jointly, the entry being a composite. Then "the rule
governs" (singular) is a category error for six of the fifteen entries, and there is no
stated way to resolve a conflict *between* two of an entry's own rules.

I pick (b) as the one the text actually means and (a) as the one it says, which is the
defect: the extension of the register's governance principle to §21.6 was made without
extending the register's citation convention with it, and one entry was converted while
fourteen were not.

Not byte-level. §21.6's entries are defined non-violations; nothing here changes whether
a file is conforming, only which rule an implementer is sent to when the gloss and the
rule disagree.

### register-03 — OBSERVATION. The Governing rule cell's parenthetical is defined as "the further rules the condition reads", and is applied inconsistently across rows that read the same rules

§21.1:

> any identifiers following it in parentheses are the further rules the condition reads,
> or the section stating what it reads where no requirement identifier does

The definite article makes this a description of the whole set, not a sample. It is not
kept. Four concrete divergences, all decidable by inspection:

1. **L2 omits `[R-CNT-17]`.** L2's cell is "`[R-ENC-04]` (R-GEO-03, R-CNT-13, R-SER-02,
   R-SER-07)". Its last instance is "entry_count × 20 + ⌈entry_count/2¹⁶⌉ × 4", and the
   rule that makes that expression a designated declaration-derived quantity — which
   `[R-ENC-04]` requires ("A designation is express, made by the section that defines the
   quantity") — is `[R-CNT-17]`: "that expression being a declaration-derived quantity
   under `[R-ENC-04]`". Without `[R-CNT-17]` the instance has no designating rule among
   the ones cited, and `[R-ENC-04]` expressly says "an expression this specification
   writes only inside a comparison, and names nowhere, is not a designated quantity".

2. **L21 omits `[R-GEO-03]`.** L21's condition is "entry_count does not equal the
   geometry-derived addressed-tile count (N interleaved, C·N planar)"; the rule defining
   that count is `[R-GEO-03]`. The cell reads "`[R-CNT-17]` (R-CNT-20)".

3. **F27 and L48 omit `[R-CNT-25]`.** Both cells read "`[R-MTA-05]` (R-CNF-05)".
   `[R-MTA-05]` states that unsorted members make the file nonconforming and that a
   verifier must report it, but it assigns no scope. The rule that places the defect at
   the file or the layer is `[R-CNT-25]`, and it names these very rows: "where a rule
   outside this quarantine records a document's defect at the file or the layer
   (`[R-MTA-05]`, F27, L48), the verifier records it there".

4. **The six checksum rows disagree about `[R-ENC-09]`.** F14 cites "(R-CNT-20,
   R-ENC-09)". F20, L37, L38 and T1 cite R-ENC-10 and not R-ENC-09. R2 cites
   "(R-CNT-25)" — neither. Every one of the six reads `[R-ENC-09]`, which is the sole
   definition of the CRC-32C the row compares against.

Either the parenthetical is exhaustive, in which case these four are omissions, or it is
illustrative, in which case §21.1's "are the further rules the condition reads" says
more than the column delivers. I record it as one finding rather than four because the
fix is one decision about the column.

Not byte-level: §21.1 makes the rule govern in every case, and every rule involved is
reachable from the row's condition text.

### register-04 — AMBIGUITY. The individuation of a "condition" is defined by a three-hop chain that ends at the register's own rows, which is exactly what §21.7 forbids for the sibling question of detectability

§21.1's completeness clause is normative and quantifies over conditions:

> Its **completeness is normative** — a *detectable* file-conformance violation this
> specification names and the register omits is a defect in this document

To apply it one must be able to individuate a condition the register does *not* carry.
The chain the document offers:

- §21.7: "**The subject is the condition and not the requirement**, as `[R-CNF-13]`
  individuates them and as `[R-CNT-06]` shows by stating nine."
- `[R-CNF-13]` (§2.3): "A **condition** this specification names — one malformed state,
  as §21.1 individuates them, and not the requirement that defines it"
- §21.1: "each row is one malformed condition"

So §21.7 defers to `[R-CNF-13]`, `[R-CNF-13]` defers to §21.1, and §21.1's only explicit
individuation is one-row-one-condition. The illustration §21.7 offers — "`[R-CNT-06]`
shows by stating nine" — is itself read off the nine rows carrying that identifier, as I
did in §2 above.

§21.7 sees this hazard for detectability and closes it deliberately:

> The instrument is the checks this specification obliges an actor to perform, and
> deliberately not the register's own rows — a test keyed to the rows would make §21.1's
> completeness clause vacuous, every omitted condition being undetectable by
> construction.

The same argument applies verbatim to individuation, and is not made. Permitted readings:

(a) "One malformed state" in `[R-CNF-13]` is the substantive criterion and §21.1's rows
are only an illustration of it. Then §21.1's further principles — "Conditions attach to
the finest structure they damage", and the strict-specialization rule that records a
file against the narrower row — are the operative guidance, and an auditor applies them
by analogy to a condition with no row. This is the reading I pick: it is the only one
under which the completeness clause does any work.

(b) Individuation is genuinely keyed to the rows. Then the completeness clause is
vacuous in the way §21.7 warns against, for a different reason than the one it guards:
an omitted condition is not a condition at all until someone writes its row, so the
register can never be found incomplete.

The cost of leaving it open is borne by an auditor of this document rather than an
implementer: under (b) no §21 finding of the "missing row" kind is ever available, which
would silently retire half of §21.1's completeness clause. Under (a) — mine — the clause
works but the count of missing rows for a given gap is unfixed: nothing says whether a
single omitted requirement stating two malformed states owes one row or two.

Not byte-level: nothing an implementation emits or accepts turns on how conditions are
counted. It turns on whether this document can be audited against its own clause.

### register-05 — OBSERVATION. §21.1's sentence about `[R-SER-08]` explains a claim by restating it

§21.1, second paragraph, verbatim:

> `[R-SER-08]` is the one rule that goes the other way for a value a reader returns: it
> resolves a nonconforming interleaved boolean byte to a sample value rather than serving
> it through, which is why `[R-TYP-04]` (§12.3) makes it the one case where a reader
> resolves a byte to a sample value rather than serving it through

The clause after "which is why" repeats the predicate before it word for word: *it
resolves X rather than serving it through, which is why `[R-TYP-04]` makes it the one
case where a reader resolves X rather than serving it through*. Nothing is explained;
the sentence is a tautology dressed as a derivation, and the second half's only real
content — that `[R-SER-08]` is the *sole* such case — is asserted, not connected to the
first half.

The substance underneath is sound. `[R-TYP-04]` says "the one case where a reader
resolves a byte to a value rather than passing it through arises only in a nonconforming
file, and `[R-SER-08]` states it", and I checked that the two rival candidates —
`[R-CNT-12]`'s reading of MU = 1 / PE = 0 as PE = 1, and `[R-CNT-22]`'s registered-type
semantics — resolve flags and not sample values, which is exactly what the next clause
of §21.1 says. So the sentence is true; it just does not say anything.

This is a sentence in the surface the round before this one rewrote, in normative text
(§21.1 carries no *Note*, *Example* or *Rationale* label, so [R-CNF-01] leaves it
normative). I report it under the standing instruction that where a passage has plainly
been rewritten more than once, the readings it still admits are named and the wording
left to human disposition: as written, a reader cannot tell whether the "which is why"
clause was meant to derive `[R-TYP-04]`'s uniqueness claim from something, or merely to
cite it.

Not byte-level.

### register-06 — OBSERVATION. The index-encoding value set is attributed to §15.1 by two rules, while §15.1 states no value set and the register's own row correctly cites §7.4

§21.1 tells a reader that a bracketless parenthetical names "the section stating what it
reads where no requirement identifier does, **a value set (L31)** or a registered type's
scope (L26)". L31's cell is "`[R-CNT-23]` (§7.4)", and §7.4's table row does state the
whole set:

> | index_encoding | u8 | 1 = raw-segmented; any other value — including 0, reserved
> 2–0x7F, and the experimental range ≥ 0x80 (§10) — is a validity error at layer scope
> (§15) |

Two rules elsewhere send a reader to §15.1 for the same value set, in identical lists of
six sections:

> a validity error at the owning scope for the value sets of §11.4, §12.2, §14.1, §15.1,
> §17.2, and §17.3  — `[R-EXT-03]`, §10.3

> the value sets of §11.4, §12.2, §14.1, §15.1, §17.2, and §17.3  — `[R-RDR-03]`, §19.3

Of the six, five do state their value set in the named section (§11.4 linearization,
§12.2 sample type, §14.1 layout via `[R-SER-06]`, §17.2 codec, §17.3 filter). §15.1 does
not. Its only mention of the field is parenthetical and points back the other way:
"Under index_encoding 1 (the only encoding this format major version defines, §7.4)". It
gives no reserved range, no experimental range, and no outcome. §10.2's table hedges by
citing both ("index encoding (§7.4, §15.1)"), and the register cites only §7.4.

Permitted readings: (a) "the value sets of … §15.1" means the value set governing the
structure §15.1 defines, wherever stated — harmless but then the list is not parallel
with its other five members; (b) it means the value set §15.1 states, in which case
`[R-EXT-03]` and `[R-RDR-03]` both point a reader at a section that has none. I pick (b)
as what the sentence says and (a) as what it means; the cost is a reader who follows
either rule's reference for the index-encoding value set and finds nothing there.

Not byte-level: the value set is unambiguous once found, and L31 enumerates its three
alternatives explicitly.

## 9. Suspicions I opened and closed

- **A row registering something the rules do not make a violation.** Pressed F5's
  committed_file_length instance and L22's overlapping instances (see §5). Both closed.
- **A missing row for `[R-IDX-05]`'s "a partial segment's CRC MUST be computed".** Closed
  by L38's own condition text, which spells it out: "a partial segment covers only its
  actual bytes, and the all-sentinel constant 0xEECB3BB2 never substitutes for
  comparison".
- **A missing row for `[R-CNT-19]`/§8.1's coverage map.** Closed: the map states which
  checksum covers what; each individual failure is F14, F20, L37, L38, T1 or R2, and
  §8.1's two "none" rows (front block, unassigned-type extent) are covered by F6/F1 and
  by §22.3's fourth residue respectively.
- **A missing §21.6 entry for an experimental-range sub-record type carrying MU = 1** (a
  conforming file whose *layer* a reader must refuse). Closed by §21.1: "neither this
  completeness clause nor the instance arithmetic below reaches §21.6's defined
  non-violations", and §21.6's closing paragraph names the case in passing anyway.
- **A third "conforming file a reader nevertheless refuses"** beyond §21.6's closed
  count of two. Closed: the resource-decline case is the third ground, and §2.3 routes it
  explicitly — "§21.9's `[R-ERR-04]` governs a refusal on that last ground; §21.6's
  closing paragraph names the other two" — with §21.9 reciprocating.
- **F19 as a capability refusal rather than a violation.** Closed by `[R-CNT-08]`: "a
  writer creating a file under this text MUST write flags = 0, but a set *ignore-lane*
  bit is not a file-conformance violation" — the exemption is the ignore lane's alone,
  so a set incompat bit is a writer violation and F19 is properly registered.
- **§21.4's preamble claiming of every verifier row that "the governing rule states what
  a reader does".** T26's `[R-COD-10]` states what a *verifier* does and what the
  undetectable consequence is, but no reader clause. Closed because `[R-COD-10]`'s first
  half does tell a reader what to do — it fixes the mandated stride the reader inverts at
  — so the rule does state a reader's behaviour, just not in a sentence about violation.
- **`[R-ENC-07]` fixed-size structures without a row.** Closed: every fixed structure's
  size violation lands somewhere (F16/F20 directory, F29/L14 record header, L22 index
  entry and segment array, F23/L12 the one-byte user-metadata payload), and the trailer's
  64 bytes are definitional.
- **§21.9's hard-limit list omitting `extent_length ≥ 5`.** Closed by "The hard limits it
  restates are a finding aid rather than an inventory".
- **The instance definition's three kinds versus the two mandated axes.** §21.1 says an
  instance names "a field the condition ranges over, a container it can occur in, one of
  several alternatives the condition text states, or any combination of the three", and
  a layout formula or a magnitude direction is none of the three where the condition text
  does not state them (T3's text does not). Closed because two sentences later the same
  paragraph loosens it to "the condition's own alternatives and containers" and then
  mandates both axes outright — "Two axes recur often enough to be stated rather than
  judged each time" — so no cell's count is left open, and the stated total of 277
  reproduces under the mandated reading and only under it.
- **`[R-ERR-02]` cited in §21.1 for the register's extent.** §21.1 carries no requirement
  identifier of its own, and the identifier it cites is stated in §21.8 and is about
  conformance-vector coverage. Closed as not a defect: the document carries un-identified
  normative prose elsewhere (§4.5's check-vector and coverage paragraphs, §8.2's
  "Verification is not optional"), and `[R-VEC-02]`'s requirement that a manifest record
  "that row's governing requirement identifier" is satisfied by every row's own cell.
- **The reach set citing `[R-CNT-24]`.** None of the four reaching rows (F1, F6, F8, F14)
  cites `[R-CNT-24]` in its cell, and the one row that does (F15) does not reach. Closed
  by §2.3, which states the test as the invariant asserted and not the rule cited, and by
  its Note, which works F15 through by name.
- **Every cross-reference to a row.** 78 F-label hits and 156 L/T/R-label hits over the
  normalised text; all resolve to a row that says what the citing text claims. Nothing
  found.

## 10. What I could not determine

Nothing in the charter was left undecidable. The two places I would most want a human
eye are register-02 (whether §21.6's Rule column was meant to inherit the register's
governing/further-rules convention) and register-04 (whether "one malformed state" is
meant to do individuation work independent of the rows) — both are questions about
authorial intent that the text underdetermines, and I have said which reading I picked
and why in each.

## 11. Byte-level verdict

**None of the six findings is byte-level.** Applying the discriminating question — is the
disputed file itself conforming, and does only one reading permit an actor to produce it?
— every finding above sits either in §21.1's or §21.6's *gloss* on rules that govern
regardless (§21.1: "where a row and the rule it cites diverge, the rule governs"), or in
a citation that changes which paragraph an implementer reads and not what that paragraph
says. In no case can two competent implementations reading this text disagree about a
byte on disk or an accept/reject verdict.

I looked hard for one. The places I thought most likely — R4's outcome, F19's status as
violation versus capability refusal, F5's second instance, the §21.6 closed count of two,
and the reach set of §21.2 — each turned out to be decided by a rule I found above the
sentence I was reading. I record that rather than reaching.
