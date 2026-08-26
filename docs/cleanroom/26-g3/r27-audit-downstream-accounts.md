# R27 downstream-dependency audit — working transcript

Role: repair auditor, "what elsewhere depended on what those passages used to say".
Access: spec/tarn.md and hunk-01..12.diff only.

## 0. Disclosure

Read: the twelve hunk files named in my charter (hunk-01.diff … hunk-12.diff), and
/Users/robertkleffner/Documents/GitHub/tarn/spec/tarn.md (many passages, listed below).
Ran: grep/rg over spec/tarn.md only (commands and output quoted below), plus one `awk|grep -c`
row count. Did NOT read: full.diff, other auditors' hunks, docs/, conformance/, registry.json,
git history, PLAN.md, OPEN-QUESTIONS.md, AGENTS.md, README.md. Did not list the case directory.

Unrequested context appeared in my context window before I began: a project instruction file
pointer (CLAUDE.md -> AGENTS.md) and an index of the maintainer's memory notes naming files about
project cadence, naming rules, register/corpus relationships and prior workflow failures. I did not
open any of them and did not use their contents; I name their appearance here per the charter.
No conclusion below rests on them — every claim is quoted from spec/tarn.md or from a hunk file.

## 1. What the twelve repairs change (my restatement of each rule adopted)

- H1 (§2.3 R-CNF-02): a foreign-major file is undecided under this text EXCEPT as to requirements
  that "reach" it (new [R-CNF-13]); failure of a reaching requirement IS a finding about its bytes.
- H2 (§2.3, new [R-CNF-13] + a Note): a requirement reaches a foreign-major file iff the invariant
  its condition violates is one [R-CNT-24] fixes in every major. Reader MUST apply reaching
  requirements whatever the declared major, and reject on that requirement's own ground; [R-CNT-07]'s
  distinct diagnostic is owed only when every reaching requirement passes. Verifier reports
  nonconforming on such a failure. All other requirements are not assessed there.
- H3 (§4.2 R-ENC-04): the 2^63-1 overflow rule is narrowed from "any quantity this specification
  defines as a sum or product … obtained from a file" to "any quantity this specification
  DESIGNATES a declaration-derived sum or product"; designation must be express, by the defining
  section; an expression written only inside a comparison and named nowhere is not designated and
  "no reader is obliged to form it".
- H4 (§11.2 R-GEO-03): §11.2's products are expressly designated (replaces "like all geometry
  arithmetic, are subject to [R-ENC-04]").
- H5 (§11.3 R-GEO-04): padding condition restated Gi·Ti > Ei  ->  Ei mod Ti != 0 (forms no product).
- H6 (§17 preamble): "Every rule in this section ranges over **stored** tiles"; a sentinel tile
  "satisfies these rules vacuously".
- H7 (§17.2 R-COD-04): codec-1 length equality restricted to a **non-sentinel** index entry.
- H8 (§17.2 Note): R-ENC-04 "binds every quantity it designates, whether or not the layer addresses
  a tile".
- H9 (§20.3 step 4): "every derived product" -> "every quantity it designates".
- H10 (§21.2 preamble): the four-rows-reach argument is replaced by "derive it from [R-CNF-13]",
  yielding F8, F14, F6 and both F1 instances, "and no other row".
- H11 (§22.2 R-SEC-02): "Every sum and product taken from a file is overflow-checked" -> "Every
  declaration-derived sum and product [R-ENC-04] designates is overflow-checked before use".
- H12 (Appendix G item 5): a fixed filter value "changes the stored bytes of any tile whose shuffle
  stride exceeds 1 — §17.3 makes it the identity where the stride is 1, as for a packed boolean plane".

Three narrowings and one new requirement, i.e. exactly the four shapes my charter names:
(a) [R-ENC-04]'s reach narrowed to designated quantities;
(b) §17's rules bounded to stored tiles by a new preamble scope statement;
(c) §11.3's condition restated in different terms;
(d) [R-CNF-13] added, deciding when other requirements apply.

## 2. Greps run (verbatim commands, hard-wrap-safe short fragments)

    grep -n "R-ENC-04" spec/tarn.md
      446, 1555, 1889, 1971, 2066, 2085, 2388, 2861, 3083, 3481, 3524, 3591, 3882
    grep -n "R-CNT-24\|R-CNF-13\|R-COD-07\|R-IDX-02" spec/tarn.md
      144,229,241,246,252,258 (2.3); 811,843 (6.2/6.3); 1426; 2067; 2267; 2378; 2858; 3080;
      3469,3471,3493; 3566 (L44); 3602 (T23); 3648; 3798; 3845
    grep -n "declaration-derived\|designates\|designated\|designation" spec/tarn.md
      167,168 (unrelated "designates as core"); 438,442,444 (R-ENC-04 itself);
      1554 (§11.2), 1889 (§14.2), 1970 (§14.x R-SER-07)  <-- the ONLY three express designations
      2389 (§17.2 Note), 3084 (§20.3), 3524 (L2 row text), 3881-3882 (§22.2)
    grep -n "entry_count" spec/tarn.md            -> 1061,1072,1079-80,2044-45,2113,3524,3544,...
    grep -n "overflow\|wrap\|2⁶³ − 1\|2^63" spec/tarn.md
      -> 428-442, 816, 971 ("overflowing sum", R-CNT-13), 1556, 2104-2105 (§15.3 rows),
         2388, 2860, 3083, 3481 (F3), 3591 (T12), 3846, 3882, 3887
    grep -n "padding position\|overhang\|Gᵢ · Tᵢ\|Gᵢ·Tᵢ\|G_i\|mod Tᵢ\|pad bit" spec/tarn.md
      -> no surviving statement of the old product form anywhere; 1548 and 1573 both use "mod"
    grep -n "0x7E000000\|7E000000" spec/tarn.md  -> 2374 (R-COD-07), 3566 (L44), 3845 (R-ERR-05),
         4217 (Appendix B constants)
    grep -n "format major\|foreign major\|another major\|major it does not implement" spec/tarn.md
    grep -n "neither conforming\|declines to judge\|capability grounds" spec/tarn.md -> 143,145,3688
    grep -n "R-COD-04\|R-COD-08\|sentinel" spec/tarn.md   (80 lines reviewed)
    awk 'NR>=3477 && NR<=3520' spec/tarn.md | grep -c "^| F"   -> 36  (matches "36 conditions")

## 3. Passages read in full

§2.2 prefixes (120-133); §2.3 (134-246) and the new Note (248-259); §2.4 (261-270);
§4.2 (420-452); §6.1 (735-765); §6.2 (777-822); §6.3 + R-CNT-24 + R-CNT-08 (824-866);
§7.2 R-CNT-12/13/14 (955-1000); §7.4 table + R-CNT-23/16/17/18 (1055-1100);
§11.1-11.4 (1500-1660); §12.1 head; §14.2 (1870-1900); §14.3/14.4 (1955-1985);
§15.1/15.2/15.3 (2035-2100); §17 preamble .. §17.4 (2261-2470); §18.1/18.2 (2455-2520);
§19.1 (2746-2800); §19.2 (2800-2845); §19.3 (2845-2870); §19.4 (2886-2950);
§20.3 step 4 (3030-3115); §21.1 (3410-3462); §21.2 preamble + all 36 rows (3465-3514);
§21.3 rows L33-L49 (3555-3575); §21.4 rows T1-T25 (3580-3605); §21.6 (3641-3695);
§21.7 (3697-3760); §21.9 (3776-3856); §22.1-22.3 (3862-3910); Appendix B constants (4195-4220);
Appendix G items 5-6 and its closing paragraph (4392-4452); Appendix H (4454-4524).

## 4. The dependency hunt, hunk group by hunk group

### 4.1 H6 — §17 bounded to "stored" tiles. What depended on the unbounded reading?

The preamble now reads (lines 2262-2268, normative, not a blockquote):

  "The owning scope of a layer's codec and filter declarations is the layer; the owning scope of one
   stored tile's payload under them is the tile (§2.4). Every rule in this section ranges over
   **stored** tiles — a tile whose index entry is the sentinel is not stored (§3.1, `[R-IDX-02]`),
   carries no payload under any codec, and satisfies these rules vacuously."

Inventory of every rule in §17 and what it actually ranges over:

  R-COD-01  pipeline           — a stored tile's bytes.                       stored. OK.
  R-COD-02  independence       — "Every stored tile".                         stored. OK.
  R-COD-03  codec value set    — the LAYER RECORD's codec field. No tile.     NOT stored-ranging.
  R-COD-04  codec-1 equality   — a non-sentinel index entry (H7).             stored. OK.
  R-COD-05/06/08 stream rules  — the stored bytes.                            stored. OK.
  R-COD-07  lz4 cap            — "a layer any of whose ADDRESSED tiles'
                                 decoded size exceeds 0x7E000000 …
                                 checkable from declarations alone".          NOT stored-ranging.
  R-COD-09  filter value set   — the LAYER RECORD's filter field. No tile.    NOT stored-ranging.
  R-COD-10  byte-shuffle       — the decoded/filtered image of a tile.        stored. OK.
  R-COD-11  certification      — a verifier's ability, per layer/file.        NOT stored-ranging.

R-COD-03 and R-COD-09 are rescued from the vacuity by an independent rule OUTSIDE §17: §7.4's
[R-CNT-23] ("a reader MUST treat any such violation — including a reserved or unassigned layout,
codec, filter, index_encoding, or channel-type value … as a validity error at layer scope"), and
rows L43 and L45 both carry "(R-CNT-23)" in their Governing rule cell. R-COD-11 concerns a verifier's
capability, not a file predicate.

**R-COD-07 has no such rescue.** Row L44's Governing rule cell is bare `[R-COD-07]`, and §19.3's
layer-access list cites only "the codec declaration bounds (`[R-COD-07]`)". Four unchanged passages
state the wide (addressed-tile) form:

 (i)  §17.2 R-COD-07 itself, line 2373-2378: "Writers MUST NOT declare this codec for a layer any of
      whose addressed tiles' decoded size exceeds 0x7E000000 bytes … and a reader MUST treat such a
      declaration as a validity error at layer scope, checkable from declarations alone."
 (ii) §17.2's Note, line 2380-2386 (immediately above hunk 8's edit, unchanged): "The cap is
      quantified over the layer's *addressed* tiles, so a layer that addresses none … satisfies it
      whatever its tile shape declares … The escape ends exactly when the layer's addressed-tile
      count rises above 0".
 (iii) §20.3 step 4, line 3080-3083 (hunk 9 edited the NEXT sentence and left this one): "`[R-COD-07]`'s
      lz4 decoded-size cap among them (L44), which an empty layer escapes only because that cap is
      quantified over addressed tiles."
 (iv) §21.3 row L44, line 3566: "Codec 4 (lz4) declared on a layer any of whose addressed tiles'
      decoded size exceeds 0x7E000000 bytes … | reader | layer access | `[R-COD-07]`".
 (v)  §21.9 R-ERR-05's hard-limit list, line 3844-3845: "a layer declaring codec 4 at decoded tile
      size at most `0x7E000000` (`[R-COD-07]`)" — unqualified.
 (vi) §21.9's per-instance paragraph, line 3796-3802: "*Decoded size of one tile* ranges over a
      layer's **addressed** tiles, stored or not, exactly as `[R-COD-07]`'s cap is".

That is the fourth (and fifth, and sixth) passage my charter asks for. Only (vi) was touched in the
previous cycle; none of (i)-(v) was swept by hunk 6.

Structural corroboration (check 6 — what the structure can carry): storedness is a property of the
INDEX REGION, which §19.2 places at the "tile use" tier ("at use of a tile: the index-chain, payload,
and decode checks"), while L44's Detected cell says "layer access" and §19.3 says of the whole
layer-access list "All are decidable from the resident directory and F: layer access performs no
fetch". Under the preamble's stored-tile scope, R-COD-07 becomes undecidable at the tier both its own
text and its row assign to it. That is independent proof the preamble's quantifier is the wrong one.

Falsifying file (byte-level): a ~1 KB file, one layer, codec 4, extents nonzero so tiles are
addressed, tile extents chosen so a tile's decoded size is 0x7F000000, every index entry the sentinel
(permitted: §21.6 "An index entry is the sentinel | The tile is addressed but not stored"). Under
R-COD-07's own words + L44: reject-layer, and [R-CNF-05] bars a conforming writer from emitting it.
Under the new preamble: no stored tile, so "satisfies these rules vacuously", the file is conforming,
a writer may emit it and a conforming reader must serve the layer (every position reads as fill).
§21.1's tiebreak ("where such an entry and the rule it cites diverge, the rule governs") does not
settle it, because the divergence is now INSIDE the rule's own section: preamble vs R-COD-07.
=> FINDING B-01. Byte-level: yes.

And (vi) separately: its warrant sentence is now false. "exactly as [R-COD-07]'s cap is" — the cap's
verb is "declared on a layer any of whose ADDRESSED tiles' decoded size exceeds"; under the preamble
the section's rules "range over STORED tiles". Word for word: "addressed … stored or not" against
"stored". Different sets. §21.9's row is a minimum ACCEPTANCE guarantee, so the two readings give
opposite reader obligations for a fully sparse layer declaring a 300 MiB tile: wide reading — the
file exceeds the row, a reader MAY decline; narrow reading — no instance exists, the file is within
the table and a reader that declines on that ground "is not a conforming reader" (R-ERR-04).
=> FINDING B-02. Byte-level: yes (accept vs. refuse on the same conforming file).

Also noted (reported inside B-01 rather than separately): "Every rule in this section" is an
exhaustive claim falsified by R-COD-03, R-COD-09 and R-COD-11 in the same section, and §18.2 borrows
R-COD-06's constraints for a user-metadata frame ("under every frame constraint `[R-COD-06]` places
on a frame, named here or not, save two"), which is not a tile at all.

### 4.2 H3 — [R-ENC-04] narrowed to designated quantities. Who relied on the wide form?

Express designations, exhaustively (grep "declaration-derived|designat"):
  §11.2 line 1554  "These products are declaration-derived quantities under `[R-ENC-04]`"  — N, P, C·N, N·P
  §14.2 line 1889  "These products and sums are declaration-derived quantities under `[R-ENC-04]`" — P·Bᶜ, P·Q, Q, Fᶜ, value offsets
  §14 (R-SER-07) line 1970 "Every decoded size, and the value count V, is a declaration-derived quantity under `[R-ENC-04]`"
Nothing else in the document expressly designates anything.

Register instances that cite [R-ENC-04] and what now supports them:
  F3 "dir_offset + dir_length"                      -> §6.2 writes it ONLY as "dir_offset +
       dir_length ≤ F − 64" (trailer table cell and R-CNT-06's ordered list) and names it nowhere.
       R-CNT-06 has no "overflowing sum" clause. NOT designated. ORPHANED.
  F3 "non-layer top-level record extent_offset + extent_length" -> rescued: R-CNT-13 line 971 states
       its own rule, "or an overflowing sum is a validity error at the scope the record governs".
  L2 "layer record / sub-record extent_offset + extent_length"  -> same rescue (R-CNT-13).
  L2 "N = ∏⌈Eᵢ/Tᵢ⌉; P = ∏Tᵢ; N·P; C·N"              -> designated, §11.2 (hunk 4).
  L2 "P·Q (which dominates V = P·C); P·Bᶜ"          -> designated, §14.2 / R-SER-07.
  L2 "max disk ordinal (C−1)·N + (N−1)"             -> dominated by C·N, designated.
  L2 "entry_count × 20 + ⌈entry_count/2¹⁶⌉ × 4"     -> §15.1 writes the region layout only inside a
       BLOCKQUOTE (lines 2044-2045, non-normative per [R-CNF-01]); the only normative appearance is
       R-CNT-17 line 1078-1080, "Under index_encoding 1, extent_length MUST equal entry_count × 20 +
       ⌈entry_count / 2¹⁶⌉ × 4 (and 0 when entry_count is 0)" — inside a comparison, named nowhere.
       NOT designated. ORPHANED — and expressly excluded by R-ENC-04's own new carve-out.
  T12 "non-sentinel entry offset + length"          -> rescued: §15.3's own row, line 2105,
       "offset + length overflows, or offset + length > F − 64 (non-sentinel) | *structural*: reject-tile".
=> FINDING B-03 (two orphaned register instances; §21.1 sends the reader to a rule that no longer
   states their condition).

The carve-out sentence itself: "an expression this specification writes only inside a comparison, and
names nowhere, is not a designated quantity and no reader is obliged to form it." The three
expressions that fit that description exactly are the left-hand sides of three MUST comparisons:
  R-CNT-06: "MUST validate … dir_offset + dir_length ≤ F − 64"   (rows F10)
  R-CNT-13: "an extent extending past F − 64"                     (rows F32, L17)
  R-CNT-17: "extent_length MUST equal entry_count × 20 + …"       (row L22)
so the licence "no reader is obliged to form it" is granted over precisely the expressions three
MUSTs oblige a reader to form. §22.2's Note relies on the third: "`[R-CNT-17]`'s cross-check ties it
to the region's declared length while `[R-CNT-13]` ties that length to the file's actual size — a
reader that validates both before fetching cannot be induced to read more than the file contains."
That claim holds only if the region-size expression is formed in exact arithmetic; it is now the one
expression R-ENC-04 expressly declines to cover. (Worked case: entry_count ≈ 4.6e17 is in domain
[R-ENC-03], is a legal addressed-tile count, and entry_count × 20 exceeds 2⁶⁴ — a u64 computation
wraps to a small value that a small declared extent_length can match.)
=> FINDING B-04. Not byte-level under the charter's discriminator (the file violates R-CNT-17
   mathematically either way, so no conforming writer may emit it under either reading), but it forks
   reader obligations and undercuts the stated §22.2 defense.

Unswept restatement of the wide form in normative text: §19.3 line 2859-2861, "the 2⁶³ − 1 ceiling on
every quantity that arithmetic derives (`[R-ENC-04]`) and on the decoded sizes §14 derives from it".
"every quantity that arithmetic derives" is the old quantifier; the cited rule now binds only
designated ones. Compare hunks 9 and 11, which swept exactly this phrasing elsewhere ("every derived
product" -> "every quantity it designates"; "Every sum and product taken from a file" -> "Every
declaration-derived sum and product `[R-ENC-04]` designates"). §19.3 was missed.
=> FINDING B-05.

Checked and found sound: R-ENC-04's class list still names "ordinals" though no section designates an
ordinal — but every ordinal §11.4 defines is dominated by a designated quantity (max in-tile ordinal
< P; max spatial ordinal < N; max disk ordinal = C·N − 1), and L2 says so in its own cell. No defect.
Hunk 8's claim that "P·Q and P·Bᶜ are checked in an empty layer" is sound: both are functions of
declarations (P from §11.2, Q/Bᶜ from §12.1/§14.2) and §14.2's designation is not conditioned on a
tile existing. §21.9's contrary individuation ("A layer addressing no tile therefore has no tile whose
decoded size the table bounds") governs a different rule (the limits table), not R-ENC-04. No defect.

### 4.3 H5 — §11.3's condition restated. Who computes with the old form?

Equivalence check: Gᵢ = ⌈Eᵢ/Tᵢ⌉, Tᵢ ≥ 1, Eᵢ ≥ 0. Gᵢ·Tᵢ > Eᵢ  <=>  Eᵢ mod Tᵢ ≠ 0, including at
Eᵢ = 0 (both false: Gᵢ = 0) and at 0 < Eᵢ < Tᵢ (both true). Sound.
Searched for any other statement of the old product form: grep over "Gᵢ", "G_i", "overhang",
"padding position", "high edge" finds no other occurrence of Gᵢ·Tᵢ anywhere in the document. §11.2
line 1548 already used the mod form ("equal to Eᵢ/Tᵢ plus 1 if Eᵢ mod Tᵢ ≠ 0"), §11.1's "where
0 < Eᵢ < Tᵢ the grid is then a single padded tile along that axis" still holds, and §14.5, §19.4
step 7, §21.4 rows T4/T5 and Appendix H all define padding by coordinate ≥ Eᵢ, which hunk 5 did not
touch. No dependent passage broken. No finding.

### 4.4 H1/H2/H10 — [R-CNF-13]. What already said something about foreign-major files?

Passages checked:
  §2.3 R-CNF-11 "cannot establish … when the file names a format major version it does not
    implement" + "An established violation takes priority" — consistent with R-CNF-13's
    nonconforming verdict. OK.
  §6.2 R-CNT-06's fixed order ("the trailer magic; the trailer CRC; the version gate … — only these
    touch fields whose positions are fixed across all majors ([R-CNT-24]) — and then, those gates
    passed, MUST validate all of the following") — consistent: F9-F17 do not reach.
  §6.1 R-CNT-04 / §19.1 step 1 — the front-block obligation is conditional on residency; hunk 10
    dropped that caveat from the §21.2 preamble but rows F1 and F6 still carry it, and Appendix H's
    verifier entry restates it ("which `[R-CNT-04]` lets a reader not holding it resident defer or
    omit and §2.3 does not (F1, F6)"). No contradiction: applying a conditional requirement means
    honouring its condition.
  §6.3 R-CNT-07 — "the diagnostic … SHOULD be distinct"; R-CNF-13's "the distinct diagnostic
    [R-CNT-07] asks for" is a faithful description of a SHOULD. Citation passes.
  §6.3 R-CNT-24 — fixes trailer magic at F−64, version_major/minor at F−56, CRC-32C at F−4 over
    [F−64, F−4), and "the front signature block (§6.1) is constant"; "A future major MAY redefine
    only the remaining 48 trailer bytes". This supports F8, F14, F6, F1-both and refutes F15 and F13.
    Hunk 10's list and hunk 2's Note check out against it. Citation passes.
  §21.9 R-ERR-04 "the two capability refusals §21.6 names, a foreign format major and an
    unimplemented MU = 1 type" — still two; count survives. OK.
  §21.2 row count "36 conditions" — counted 36 F rows. OK.
  §21.6 lines 3684-3690 — DOES rely on the old wide reading:
      "In both the outcome records a reader's capability, not a defect in the bytes … Neither is a
       register row: the register enumerates file-conformance violations (§21.1), and a file this
       document declines to judge is not one. What is registered in each case is the neighbouring
       condition that *is* a violation — version_major = 0 … (F18)".
    Under R-CNF-13 this document no longer wholly declines to judge such a file, and hunk 10 says in
    terms that F8, F14, F6 and both F1 instances DO record it. The stated reason is now false and the
    "what is registered in each case" enumeration is now incomplete for the foreign-major case.
    Also "the outcome records a reader's capability, not a defect in the bytes" is now true only
    where every reaching requirement passes — which is exactly the qualification hunk 1 added to
    R-CNF-02 and hunk 2 to R-CNT-07's diagnostic, and which was not carried here.
=> FINDING B-07. Not byte-level (the entry's conclusion — that declaring a foreign major is not
   itself a row — still holds).

### 4.5 H12 — Appendix G item 5. Reverse check against §17.3.

New text: a fixed filter value "changes the stored bytes of any tile whose shuffle stride exceeds 1
— §17.3 makes it the identity where the stride is 1, as for a packed boolean plane".
§17.3 R-COD-10: "Viewing the image as n = L/s consecutive groups of s bytes, the filtered image
places byte i of group j at offset i · n + j". At n = 1 the map is i·1 + 0 = i — the identity — for
ANY stride s. n = 1 whenever L = s: a planar numeric tile with P = 1, or an interleaved tile with
P = 1 (all tile extents 1, permitted by [R-GEO-01]'s Tᵢ ≥ 1). So "any tile whose shuffle stride
exceeds 1" overclaims; the true condition is stride > 1 AND more than one group.
=> FINDING B-06. Non-normative appendix; not byte-level.

## 5. Reverse check — do the corrections duplicate or contradict existing text?

  H1/H2 vs §2.3 R-CNF-11: no duplication, priority already stated. OK.
  H7 vs row T14 ("Codec 1 (none) declared and a NON-SENTINEL index entry's length differs …"):
    the row already said non-sentinel; hunk 7 brings the rule into line with it. Correct sweep.
  H4 vs L2: L2's instance list is unchanged and every product it names is now designated. OK.
  H9/H11 vs L2/F3: swept phrasing, but see B-03/B-05 for what the phrasing now excludes.
  H6 vs R-COD-07 / L44 / §20.3 / §21.9: contradiction — B-01, B-02.
  H3 vs R-CNT-06 / R-CNT-13 / R-CNT-17 / §22.2: contradiction — B-04.
  H12 vs R-COD-10: overclaim — B-06.
  H10 vs §21.6: stale premise — B-07.

## 6. Checks that passed with nothing to report

- Tense/quantifier (check 1) for H6: "stored" is defined against a generation (§3.1, "unqualified
  *stored* means stored in the live generation"); §17's rules are reader-facing and live-generation,
  and §20.3's superseded-generation tense is stated locally there. No tense fault.
- Citation resolution: §4.2 (H5's "(§4.2)"), [R-IDX-02] (H6), [R-CNT-24] (H2, H10), [R-CNT-27]
  (H2's Note re F5), [R-CNT-07] (H1, H2), [R-CNF-13] (H1, H10), [R-COD-07] (H9), [R-ENC-04] (H4, H8,
  H9, H11), §17.3 (H12), §14.2/§14.3 (H7), §3.1 (H6), §21.1 (H10) — all open to text that says what
  the citing sentence claims. The one citation whose claim I could NOT confirm is H6's implicit claim
  over "every rule in this section" (B-01).
- H2's Note re F14/F5/F15: F14 asserts the CRC-32C at F−4 over [F−64, F−4) — fixed by R-CNT-24, so it
  reaches; F5's floor derives from dir_length ≥ 4, dir_offset ≥ 16 and 64-alignment, none in
  R-CNT-24, so it does not; F15's reserved bytes at trailer offset 56 are inside the 48 a future
  major may redefine, so it does not. All three verified against R-CNT-24 and §5.1/§6.2. Sound.
