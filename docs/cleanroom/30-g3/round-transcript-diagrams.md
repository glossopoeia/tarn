# Cleanroom round 30 — Diagram auditor transcript

## Disclosure

Read: `/Users/robertkleffner/Documents/GitHub/tarn-first-draft/spec/tarn.md` only, in full, by `sed -n` ranges (1–4743). One `sed` call's output (lines 3200–3600) was truncated by the harness and saved to a tool-results file; I did **not** open that file — I re-read the same spec lines in smaller ranges instead. No other file opened; no directory listed; no git; no web.

Context I did not ask for: the runtime placed a project CLAUDE.md pointer ("See AGENTS.md") and an index of four maintainer memory notes (titles only, naming a harness spec path, a lineage word list, a preflight, and "repair prose vs rules") into my context before I began. I did not open any of them and drew nothing from them. I note their appearance here as the brief requires.

Files written (all in my own scratch dir `/private/tmp/claude-501/-Users-robertkleffner-Documents-GitHub-tarn-first-draft/r30-round/scratch/diagrams/`): `crc_diag.py` (my own CRC-32C, bit-serial, reflected poly 0x82F63B78, init/xorout 0xFFFFFFFF), `count_instances.py` (register row/instance counter — reads only tarn.md), `parse_examples.py` (parses the §7.4 payload dump and the Appendix A dump against the layout tables). Plus this transcript.

## Method

1. Read the whole document once, end to end.
2. Enumerated every table, worked example, code-block figure, appendix and numbered list by grep with line numbers (below).
3. Recomputed every checksum the document prints with my own CRC; parsed every hex dump field-by-field against its layout table; redid every piece of arithmetic in every worked example.
4. For each figure/table/checklist asked: values match prose? narrower/wider than the rule? forbidden or missing case? label (Note/Example/Rationale/non-normative appendix) vs treatment? promised columns/closed lists delivered?
5. Gave extra weight to the changed surface named in the brief (front-matter Note; §2.3, §2.4; §9.2; §9.6; §11.1; §16.2; §18.2; §19.3; §20.3; §20.5; §21.1, §21.2, §21.5, §21.6, §21.7, §21.9; Appendices G, H) and to their restatements elsewhere.

## Inventory (line numbers in spec/tarn.md)

Tables: §2.2 prefixes 127; §2.4 outcomes 298; §6.1 front block 766; §6.2 trailer 809; §7.2 record header 973; §7.3 record types 1048; §7.4 layer payload 1077; §8.1 coverage map 1195; §10.2 identifier spaces 1532; §12.1 sample types 1750; §14.2 decoded size 1982; §15.1 entry 2152; §15.3 entry validity 2200; §18.2 encoding 2598; §18.4 keys 2792; §20.4 stored flags 3391; §21.2 F rows 3671; §21.3 L rows 3720; §21.4 T rows 3780; §21.5 R rows 3830; §21.6 non-violations 3848; §21.9 limits 3973; App A byte table 4355; App B constants 4390; App E changelog 4488.

Worked examples: §4.6 température 582; §5.1 smallest file 646; §5.1 three-commits figure 653–661; §7.4 layer payload dump 1132–1162; §9.2 crash figure 1292–1305; §11.2 grid 1665; §11.4 ordinals 1721; §12.1 bfloat16 1784; §12.3 channel entry 1833; §13.3 fill 1903; §14.2 offsets 2024; §14.3 packed plane 2058; §14.5 padding 2116; §15.4 million-entry 2240; §15.4 planar entries 2255; §16.2 slab runs 2357; §17.3 shuffle 2541; §20.3 supersede cost 3306; §20.3 three shapes 3315–3365; §20.5 compaction figure 3527–3536; App A dump 4344–4353.

Numbered lists: §10.1 vehicles 1512–1516 (4); §19.1 open 2856–2875 (4); §19.4 tile read 2982–3016 (8); §20.3 append 3108–3290 (6); §9.2 commit protocol (1)–(6) inline; App G items 4523–4646 (10).

Checklists/appendices: A 4338; B 4385; C 4420; D 4447; E 4486; F 4497; G 4512; H 4671.

Labels checked: every one of the figures above is inside a block labeled **Example**, **Note** or **Rationale**, or in an appendix headed "(non-normative)", except: the layout tables themselves (normative — §6.1, §6.2, §7.2, §7.3, §7.4, §8.1, §10.2, §12.1, §14.2, §15.1, §15.3, §18.2, §18.4, §20.4, §21.x, §21.9), the §15.1 region layout blockquote at line ~2149 ("> [ entry array … ] [ segment CRC array … ]") which carries **no label and is therefore normative** under [R-CNF-01], and Appendix F (Normative references — no "(non-normative)" in its heading, so it is normative as a reference list). The front-matter block at line 12 is now labeled **Note**, so it is non-normative.

## Computations (all mine, against the document's figures)

CRC-32C (`crc_diag.py`):
- check vector "123456789" → 0xE3069283 (doc §4.5: 0xE3069283, bytes `83 92 06 E3`) ✓; zero bytes → 0x00000000 ✓.
- §7.4 example: 4 sentinel entries = 80 bytes `FF×16 00×4` ×4 → segment CRC 0x80A34955, stored `55 49 A3 80` (doc: same) ✓; crc_of_crc_array = CRC over those 4 bytes → 0xC4EE982E (doc: 0xC4EE982E; dump bytes `2E 98 EE C4`) ✓.
- §15.4 full all-sentinel segment (2¹⁶ × 20 bytes) → 0xEECB3BB2 (doc [R-IDX-05] and App B: 0xEECB3BB2) ✓.
- Appendix A trailer bytes [0,60) → 0x402F157E, stored `7E 15 2F 40` (doc: both) ✓.

§7.4 payload dump (`parse_examples.py`): 81 bytes ✓; field offsets name@0 (len 3 `sst`), layout@4=1, linearization@5=1, codec@7=1, filter@9=1, A@11=0, S@19=0, A_slab@27=0, d@35=1, C@36=1, dim `x` E=100 T=32 ending @56, channel `temp` type 12 fill `00 00 C0 7F` (=0x7FC00000) ending @68, index_encoding@68=1, entry_count@69=4, crc_of_crc_array@77=0xC4EE982E, consumed 81, residue 0 ✓. Sizes: 4 + 34 (1+2+2+2+8+8+8+1+2) + 18 + 12 + 13 = 81 ✓. Grid ⌈100/32⌉ = 4 ✓. Extent length 4×20 + ⌈4/2¹⁶⌉×4 = 84 ✓. Channel entry bytes identical to §12.3's `04 74 65 6D 70 0C 00 04 00 00 C0 7F` ✓ ("byte for byte" claim holds).

Appendix A dump: 128 bytes ✓; front block = §6.1 constant ✓; [16,20) = `00 00 00 00` = CRC of zero bytes ✓; [20,64) 44 zero bytes ✓; trailer magic ✓; version_major 1, minor 0 ✓; flags 0 ✓; dir_offset 16, dir_length 4 ✓ (16+4 = 20 ≤ 128−64 ✓); committed_file_length 128 ✓ (multiple of 64 ✓); file_id LE = 0x0123456789ABCDEF ✓ (bytes `EF CD AB 89 67 45 23 01`); reserved [48,60) zero ✓; stored CRC 0x402F157E = recomputed ✓. Commentary: "112 bytes covering [16,128)" = 128−16 ✓.

Register counts (`count_instances.py`): F rows 35 (F1–F36 less struck F11) ✓ §21.2 "35"; L 49 ✓; T 26 ✓; R 10 ✓; total 120 ✓ §21.8. Instances: F 56, L 116, T 55, R 50 = **277** ✓ §21.8 "277" (rule: semicolon-separated; "—" = 1, exactly as §21.1 says).

Prefix census: identifiers in use have prefixes CNF CNT COD ENC ERR EXT GEO IDX LIF MDL MTA PRV RDR SEC SER SLB TYP VEC WRT = 19, identical to §2.2's 19-row table ✓.

Layout-table widths: §6.2 trailer 8+2+2+4+8+8+8+8+12+4 = 64 ✓; §7.2 header 2+2+4+8+8 = 24 ✓ (App B "24") ✓; §15.1 entry 8+8+4 = 20 ✓ (App B "20") ✓; §6.1 8+8 = 16 ✓.

Other worked arithmetic:
- §5.1 smallest file: 16 + 4 = 20 → next 64-aligned 64 → +64 = 128 ✓; pad 64−20 = 44 ✓ (App A agrees).
- §9.2 Note: prior F + 68 rounded to 64-multiple = F + 128 ✓. §9.3 Note ceiling 2⁶³−64 ✓.
- §11.2: (1024,2048)/(256,256) → G=(4,8), N=32, P=65,536 ✓; ⌈1000/256⌉ = 4 ✓.
- §11.4: (0,1)→1; (1,0)→8 ✓; (300,700) → t=(1,2), s=1·8+2=10 ✓; u=(44,188), 44·256+188 = 11,452 ✓; planar c=2: 2·32+10 = 74 ✓.
- §12.1 bfloat16 1.0 = 0x3F80 (`80 3F`) ✓; 0x7FC0 quiet NaN ✓.
- §4.6: NFC `t e m p C3 A9 r a t u r e` = 12 bytes ✓; NFD `65 CC 81` → 13 ✓.
- §14.2: a(u8)+b(u16): Q=3, P=6, size 18 ✓; ordinal 1·3+2 = 5 ✓ → [15,18) ✓; planar b 12 bytes, ordinal 5 at 10–11 ✓; t(f32)+m(bool): Q=5, size 30, [25,30), t 25–28, m 29 ✓.
- §14.3: P=10 alternating → values 0,2,4,6 true → byte 0 = 0x55 ✓; byte 1 bit0 = value 8 = true → 0x01 ✓; fill true sets pad bits 2–7 → 0xFC|0x01 = 0xFD ✓.
- §14.5: extents (5,5), tiles (4,4) → grid 2×2 ✓; tile (1,1) covers 4–7 both axes; real position (4,4) only → 1 real, 15 padding ✓; uint16 → 32 bytes ✓; fill 0xABCD LE = `CD AB` ✓; (4,4) is in-tile (0,0) = ordinal 0 ✓.
- §15.4: entry_count 1,000,000 → ⌈10⁶/65,536⌉ = 16 segments ✓; last covers 10⁶ − 15·65,536 = 16,960 ✓; CRC array 64 bytes ✓; region 20,000,000 + 64 = 20,000,064 ✓; tile 999,999 → segment 15, index 16,959, byte 339,180 ✓; segment 15 at [19,660,800, 20,000,000) ✓ (~339 KB) ✓; full segment 1,310,720 = 1.25 MiB ✓.
- §15.4 planar example: 74·20 = 1,480 → [1,480, 1,500) ✓; channel 3 → entries 96–127 (32) ✓.
- §16.2: S=8 over N=32 → runs [0,8),[8,16),[16,24),[24,32) ✓; rows 1–2 = ordinals 8–23 = runs 1,2 ✓.
- §17.3 shuffle: groups `00 00 80 3F | 00 00 00 40 | 00 00 40 40` → bytes i=0: 00 00 00; i=1: 00 00 00; i=2: 80 00 40; i=3: 3F 40 40 → `00 00 00 00 00 00 80 00 40 3F 40 40` ✓ matches.
- §20.3 example: 32·20 + 4 = 644 ✓. §20.3 Note: 10⁶-tile index ≈ 20 MB ✓.
- §21.9 Note: 2³² entries → 2¹⁶ segments × 4 B = 256 KiB ✓; 2³⁶ → 4 MiB ✓.
- §2.3 [R-CNF-13] "[R-CNT-06] states nine": F rows governed by R-CNT-06 = F8, F9, F10, F12, F13, F14, F15, F16, F17 = 9 ✓; of which F8 (magic) and F14 (CRC) reach ✓; §21.2 intro's reaching set {F8, F14, F6, F1×2} ✓ consistent with §2.3's Note (F5, F15 do not).
- §15.3 "Six rows are marked structural": rows 2–7 = 6 ✓; each maps to a §21.4 row (T6, T7, T10, T8, T11, T9/T12) ✓; crc row → T1; overlap rows → L18 / F33; alignment/slab → L40–L42 ✓.
- §20.5 [R-WRT-06] "one row for each of the other seven spaces §10.2 tabulates (L31, L33, L34, L36, L43, L45, R1)": §10.2 has 8 spaces; less record type = 7; index-encoding→L31, linearization→L33, sample type→L34, layout→L36, codec→L43, filter→L45, metadata encoding→R1 ✓.
- §21.1 specialization list: F1(front)⊂F6 ✓, F1(trailer)⊂F8 ✓, F35⊂F36 ✓, L24⊂L25 ✓, F21 (slot (0,0)) ⊂ F22 (extent_length < 5) ✓, L10⊂L11 ✓.
- §21.9 table: 8 rows; "last three per-instance" + "first five over declarations" = 8 ✓; App B's guarantees row lists the same 8 in order ✓.
- §10.2 table vs owning sections: record type (§7.3, §21.6) ✓; layout §14.1 (0 invalid; 3–255 reserved; no experimental) ✓; linearization §11.4 ✓; sample type §12.2 (14–19 and 20–0x7FFF both "reserved") ✓; codec §17.2 ✓; filter §17.3 ✓; index encoding §7.4 ✓; metadata encoding §18.2 ✓. App C matches all ✓.
- §12.1 table vs App C (13 types, sizes) ✓; §18.4 six keys vs App C ✓; §7.3 vs App C ✓.
- App B rows against sections: front block, trailer magic, 64/aligned, 128, dir minimums, extent ≥ 5 (§7.1), bool bytes, media type, 24, 20, 2¹⁶/4, sentinel, 0xEECB3BB2, CRC params, check vector, value domain, 255, rank/channel maxima, S range, A range/4096, A_slab range, 64 KiB, 1–16 MiB, zstd magic `28 B5 2F FD` = 0xFD2FB528 LE ✓, 0x7E000000, `tarn.`, guarantees — every cell matches its cited section ✓.
- §8.1 map: 7 rows; §4.5's "terminal fields" (trailer, directory, user-metadata) and "interior fields" (segment CRC array ← crc_of_crc_array; entry crc ← segment CRC; crc_of_crc_array ← directory CRC) both consistent with the map ✓.
- Numbered lists: §10.1 1–4 matches §4.3's four vehicles ✓; §19.1 1–4 ✓ ("four-step open" in App A ✓); §19.4 1–8, step 3's "Steps 3 through 6" ✓; §20.3 1–6, steps 4–6 cite [R-LIF-02] steps 1–2, 3, 4–6 ✓; §9.2 (1)–(6) ✓; App G 1–10 in order, no gaps ✓.
- §21.1's instance discipline applied row by row: two-direction rows (L21 4, L22 4, L30 2, T3 6, T14 6, T22 6, F17 2) ✓; one-direction (L44 3, T21 3, F10 1) ✓; checksum/constant rows "—" (F14, F20, L37, L38, T1, F8) ✓; value tests "—" (L20, L27, L28) ✓.

## Figure-by-figure judgement (beyond the numbers)

- §5.1 three-commits figure: consistent with the prose (two ▓ runs = dir/pad/tr of commits 1 and 2; layer A never moved; commit 3 touched no layer). Its caveat that grouping is illustrative points to §20.5's figure ✓.
- §9.2 crash figure: rows match [R-LIF-05] and §9.6 ✓.
- §20.3 three shapes: (a) new layer ✓; (b) index re-emitted whole, retained payloads not moved ✓ [R-WRT-04]; (c) directory-only list ("clearing a slab declaration, renaming a layer, or changing a channel's fill value where that channel carries no padding position and no pad bit…") consistent with step 4's §14 bar and its carve-out; the extra "layer that stored no tile … re-declared freely — a layer the commit itself empties does not qualify" matches step 4's tense sentences ✓. Editing user metadata routed to shape (b) ✓ consistent with §23.1.
- §20.5 compaction figure: see rejected candidate 3.
- §15.3 table: no row is wider or narrower than [R-IDX-03]'s prose; the "Six rows structural" count holds.
- §20.4 flags table: MU=1 row's compactor refusal restates [R-WRT-06] ✓; MU=0/PE=0 drop conditions consistent with §20.4 prose and §20.5 ✓; the §2.4 preserve-verbatim row correctly names "its MU = 1 and MU = 0 / PE = 1 rows" ✓.
- §21.6 table: each row's rule cell restates its rule; the experimental-encoding row agrees with [R-MTA-03]/[R-MTA-10]/§21.5 intro ✓; the slack row agrees with [R-CNT-21] ✓; closing paragraphs' F18 / F35, F36, L24, L25 citations exist ✓.
- Appendix H: reader list (four codecs, two filters, two layouts, thirteen types, two encodings) ✓ [R-CNF-03]; verifier list's (F1, F6), (F7), (F36, L25), (R1) citations exist and say what the checklist says ✓; updater "never removes a layer record, or a user-metadata record at either scope" ✓ §20.4; writer "both barriers (§9.2)" is a conduct MUST, correctly listed as an obligation and correctly not called a file-conformance condition ✓.
- Appendix A commentary vs [R-CNT-04]: see rejected candidate 4.
- Appendix G: item 2 (see rejected candidate 2), item 3 (first structure at 16 or first aligned position; gaps zero) consistent with [R-CNT-03]/[R-SLB-05]/[R-LIF-02]; item 5's "identity exactly where … stride 1 … or n = 1" verified against [R-COD-10]'s permutation (i·n+j = j·s+i for all i,j iff n=1 or s=1) ✓; item 8 vs closing paragraph — **finding diagrams-01**.

## Findings

### diagrams-01 — CONTRADICTION (non-normative, not byte-level)

Location: Appendix G, item 8 (lines 4625–4636) vs Appendix G closing paragraph (line 4664–4665).

Item 8 says, verbatim:

> "The version_minor floor binds a compactor too, save where its output carries a feature it does not implement, when §20.5's floor governs instead (`[R-WRT-06]`)."

The closing paragraph of the same appendix says, verbatim:

> "`version_minor` at its floor, which `[R-CNT-26]` states as a SHOULD — item 8's creator's rule, not a compactor's (§20.5);"

The two disagree on whether the item-8 version_minor floor binds a compactor. Item 8 says it does (with one carve-out), and the normative text agrees with item 8: §20.5 [R-WRT-06] says "Otherwise version_minor follows `[R-CNT-26]`'s floor", i.e. the compactor is on [R-CNT-26]'s floor except in the carried-feature case. The closing paragraph says the floor is "not a compactor's", which is true of item 8's *flags* half ("The `flags` half is a creator's rule") and of item 2's file_id, but not of its version_minor half. It reads as a neighbour left standing after item 8 was rewritten to split the two halves — the sentence's parenthetical "(§20.5)" even cites the section that says the opposite.

Readings: (a) the closing paragraph is a slip and item 8 governs — a profile-adopting compactor emits the [R-CNT-26] floor unless it carries an unimplemented feature; (b) the closing paragraph governs and a profile-adopting compactor is under no version_minor floor from the profile. I pick (a): item 8 is the enumerated rule, the closing paragraph disclaims being the list ("Read the numbered items as the list"), and §20.5 backs item 8. An implementer of the profile who reads only the closing summary builds (b) and produces a different trailer from one who reads item 8.

Byte-level: **no**. Appendix G is non-normative and "adds no requirement to any actor"; version_minor is descriptive ([R-ENC-16]) and its floor is a SHOULD ([R-CNT-26]), so neither reading moves what a conforming writer may emit or what a reader must accept ([R-CNF-12], [R-CNT-07]). What it costs is the profile's own purpose — byte-identity between two profile-conforming compactors — which is exactly the property the profile exists to deliver.

## Rejected candidates (opened and closed)

1. **§21.8 "120 conditions over 277 instances" stale?** Recounted mechanically: 120 / 277 exactly. Closed by the count.
2. **Appendix G item 2 — hash input includes the trailer CRC field?** "computed over [0, F − 64) together with the trailer's other fields with the `file_id` field taken as zero" could be read as including the CRC field; but the same item restates it precisely — "its input the bytes [0, F − 64) followed by the trailer's first 60 bytes with the `file_id` field zeroed" — and the CRC cannot exist before file_id is "then written in", so the 60-byte reading is the only coherent one. Closed by that sentence. (Non-normative either way.)
3. **§20.5 compaction figure marks `A: index′` regenerated though A's tiles sit in the same place in input and output.** [R-WRT-07] regenerates a region only where a stored extent moved; but the figure is captioned "Regions, not offsets", the "A" box may hide internal gaps, and regenerating an unmoved region yields byte-identical entries anyway, so no byte turns on it. Closed by the caption and by the arithmetic.
4. **Appendix A: "A local reader additionally verifies bytes [0, 16) by equality first" — wider than [R-CNT-04], whose test is residency, not transport.** The same sentence qualifies "which `[R-CNT-04]` requires of any reader holding them", §6.1 states the residency test explicitly, and a file with a bad front block is nonconforming, so a reader rejecting it is within [R-CNF-12] under both readings. Closed; not byte-level, and the appendix's own qualifier limits it.
5. **§11.1 Rationale says growth leaving entry_count unchanged "touches the directory alone" and names only the zero-grid-count case.** The example is introduced "among them", growth within a grid count is also directory-only under §20.3's growth permission, and the block is labeled Rationale. Closed.
6. **Appendix G item 7 "not merely about eight bytes of the layer record"** — a fill field is 1–8 bytes; "eight" is an illustration for an 8-byte type in a non-normative item. Closed as rhetorical.
7. **§7.2 table vs §4.7 Note "folds each field's range into its Field cell"** — only type and flags carry a range in the Field cell; inline_length and the extent fields get theirs in prose. A Note describing presentation, no rule rides on it. Closed.
8. **§20.3 shape (c) list omits a within-grid growth** — the list is dashed, not closed. Closed.
9. **R1's Detected cell (open / layer access) is not restated by §19.1 step 4 or §19.3** — §19's preamble says the register, not §19's enumerations, is the inventory per tier. Closed by that paragraph.
10. **Appendix C names type 19 "opaque" where §12.2's Note says "fixed-size raw-bytes"** — a nickname for a reservation with no semantics; Appendix C is non-normative. Closed.

## Sweeps run (grep over spec/tarn.md only)

- table-header regex `^\| ?(Offset|Prefix|Outcome|…) ` → 25 hits (inventory above).
- `\*\*Example` → 23 hits; code fences → 16 fence lines (8 blocks); `^### Appendix` → 8; numbered bold list items → 38 lines.
- `R-[A-Z]+-[0-9]+` census → 19 distinct prefixes (counts: CNT 298, ENC 94, CNF 77 …).
- `creator's rule|binds a compactor too|version_minor follows|floor governs|SHOULD emit the lowest` → 7 hits (finding 01's citations).
- `other fields|first 60 bytes|eight bytes` → 5 hits; `index′|any of whose stored` → 5; `A local reader additionally|holding them` → 2; `55 FD|0x55` → 2; `touches the directory alone|only remaining` → 2.
- Control for a zero: none of my conclusions rests on a zero-hit search; every phrase I concluded *absent* I instead concluded present-and-consistent. Control phrase "Read the numbered items" → 1 hit as expected.

## Confidence

Every checksum, offset, width, count and worked number in the document that I could recompute recomputes. The one defect I can defend is the Appendix G internal contradiction, which is in a non-normative appendix and cannot move the emittable set. I found no figure, table or checklist that states a rule wider or narrower than its normative source in a way that changes bytes or verdicts.
