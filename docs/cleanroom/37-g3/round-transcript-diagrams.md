# Round 37 — Diagram auditor transcript

## Access and disclosure

I read exactly one file: `/Users/robertkleffner/Documents/GitHub/tarn-first-draft/spec/tarn.md`, in full (4,981 lines), in six sequential `Read` calls (offsets 1–1000, 1001–1700, 1701–2400, 2401–3100, 3101–3800, 3801–4500, 4501–4981 — the tool's line/size limits forced this chunking; no other file was opened at any point).

I did not read `docs/`, any ADR, `PLAN.md`, `OPEN-QUESTIONS.md`, `AGENTS.md`, `README.md`, `CONTRIBUTING.md`, `conformance/`, `spec/registry.json`, or any git history. I ran no `git` command. I did not list the round's shared `out/` directory (I only created it with `mkdir -p` because it did not yet exist, and then wrote my one transcript file into it — I never enumerated its contents). I did not list the repository root or any other directory beyond checking that my private scratch directory was empty before I started (it was — no leftover files from a prior attempt).

**Contamination disclosure.** Before this task's content arrived, my context already contained: a `CLAUDE.md` pointer to `AGENTS.md` (unread), a user memory file (`MEMORY.md`) with roughly twenty bullet titles about this project's harness, gates, and prior-round findings (e.g. "TARN lineage gate word list — canonical file is missing", "TARN repair prose vs rules", "TARN subagents on Sonnet", "TARN refute phase and unanimous upholds"), and the git status/log of the outer repository showing recent commit subjects including "Cleanroom round 37: charter, over 96e4ad4..6c9470e" and "The pre-round-37 audit of ADR-0131: two defects in three clauses, none byte-level, both repaired". None of this is part of the specification, and I have not treated any of it as evidence about the specification's content. I did not open any of the linked memory files. I note this exists in my context per the brief's disclosure instruction; I did not act on it — my findings below rest solely on arithmetic and cross-references I performed against `spec/tarn.md`'s own text.

**Scratch files.** My scratch directory `/private/tmp/claude-501/-Users-robertkleffner-Documents-GitHub-tarn-first-draft/r37-round/scratch/diagrams/` was empty when I began (verified with `ls -la`; nothing to disclose from a prior attempt). I wrote and ran, in that directory only:
- `crc_check.py` — my own CRC-32C (Castagnoli, reflected, init/final 0xFFFFFFFF) implementation, self-tested against the spec's own two check vectors (§4.5: `CRC32C("123456789") = 0xE3069283`, `CRC32C(b"") = 0x00000000`) before using it for anything else.
- `appendixA_check.py` — recomputes the directory-region CRC and the trailer CRC for Appendix A's 128-byte worked example from the printed hex dump.
- `sst_check.py` — recomputes the segment CRC and `crc_of_crc_array` for §7.4's worked layer-record example (the `sst` layer).
All other computation (table-row counts, instance counts, bracket/column position analysis) was done with inline `python3 -c` / heredoc scripts run directly from the repository working directory, reading only `spec/tarn.md`; none of that scratch state was persisted to disk beyond the three files above.

## Method

Per the charter I first enumerated every figure/diagram/byte-layout table/worked example/checklist in the document with its line range, then (a) recomputed every checksum and every derived arithmetic quantity a worked example states, by hand-coded computation rather than eyeballing, and (b) checked every fixed-layout table's offset/size columns for internal consistency (no gaps, no overlaps, totals matching the stated structure size), and (c) checked each diagram's annotations (labelled spans, brackets) against the columns they are drawn under, treating the ASCII art as literal fixed-width text. I gave the three changed passages named in the brief (§3.3, §20.3, §20.4) and the four "decisions" (the §20.4 table and the paragraph below it; §7.2's Note and the paragraph before it; §20.1's closing paragraph with §2.3's updater clause; §20.3 step 4's scope sentence and the paragraph it closes) the most scrutiny, followed by the two appendices the brief says restate §20.4 and §20.1 (Appendix H's "Conforming updater" entry, and Appendix G's item 8).

## Inventory of figures/diagrams/tables/examples (with line numbers)

- §2.2 prefix table (127–147) — reference table, not byte-layout; skimmed only.
- §5.1 Example — smallest conforming file (656–662); Example — file after three commits, ASCII diagram with annotation brackets (663–697).
- §6.1 front signature block byte-layout table (788–792).
- §6.2 trailer byte-layout table (833–844).
- §7.2 record header byte-layout table (1012–1018).
- §7.3 record types table (1098–1102).
- §7.4 layer record inline-payload table (1127–1144); worked Example — complete layer record payload, byte-by-byte hex dump (1182–1221).
- §8.1 coverage-map table (1245–1253).
- §9.2 Example — what a crash sees, ASCII diagram with arrows (1343–1365).
- §10.2 numeric identifier spaces table (1589–1599).
- §11.2 worked Example — grid arithmetic (1719–1723).
- §11.4 worked Example — tile/spatial ordinals (1775–1781).
- §12.1 core sample types table (1804–1818); §12.3 worked Example — channel entry bytes (1887–1892); bfloat16 Example (1838–1841).
- §13.3 worked Example — fill values (1957–1962).
- §14.2 byte-layout/offset table (2038–2042); worked Example (2083–2093).
- §14.3 worked Example — packed bool tile (2117–2122).
- §14.5 worked Example — padding content (2175–2180).
- §15.1 tile-index region diagram (2206–2207) and entry byte-layout table (2211–2215).
- §15.3 entry-validity table (2260–2272) — dense, central table.
- §15.4 worked Examples — segment arithmetic at scale, ×2 (2300–2313, 2315–2319).
- §16.2 worked Example — slab runs (2417–2424).
- §18.2 encoding byte-layout table (2659–2661).
- §18.4 standardized keys table (2862–2870).
- §20.3 worked Example — superseding one tile (3398–3405); Example — the three shapes a commit takes, three ASCII diagrams (a)/(b)/(c) with annotation brackets (3407–3473). **In the changed surface.**
- §20.4 updater-obligation table, unlabelled/normative (3503–3507) and the paragraph below it (3509–3526). **In the changed surface / a named decision.**
- §20.5 worked Example — what compaction reclaims, ASCII diagram (3674–3714).
- §21.2–21.5 the error register: F-rows (35), L-rows (49), T-rows (26), R-rows (10) — each row is itself a table restating a governing rule.
- §21.9 implementation-limits table (4154–4163).
- Appendix A — annotated minimal file, full hex dump plus byte-range table (4529–4574).
- Appendix B — constants table (4576–4609).
- Appendix C — registry snapshot (4611–4636).
- Appendix G — reproducible-writer profile, a 10-item checklist (4708–4881); item 8 restates part of §20.1.
- Appendix H — conformance checklists, one paragraph per class (4883–4981); "Conforming updater" restates §20.4 and §20.1.

## Arithmetic verified (all matched; shown in full so a reader can re-run them)

1. **CRC-32C self-check vectors (§4.5).** My implementation reproduces `CRC32C("123456789") = 0xE3069283` and `CRC32C(b"") = 0x00000000` exactly. I would not trust any of the checks below without this passing first.

2. **Appendix A's 128-byte file.** From the printed hex dump:
   - Directory region `[16,20)` = `00 00 00 00`. Document says this is the CRC-32C of a zero-byte record sequence = `0x00000000`. Computed: `crc32c(b"") = 0x00000000`. Match.
   - Trailer bytes `[0,60)` relative to the trailer (global `[64,124)`) hashed with my CRC-32C give `0x402F157E`. The document's stored trailer CRC bytes are `7E 15 2F 40`, little-endian = `0x402F157E`. Match, exactly.
   - `file_id` bytes `EF CD AB 89 67 45 23 01`, little-endian, decode to `0x0123456789ABCDEF` — matches the annotation. Match.
   - `committed_file_length` bytes at `[96,104)` = `80 00 00 00 00 00 00 00` = 128 = the stated file size. Match.

3. **§7.4's worked layer-record example (the `sst` layer).**
   - entry_count = 4 (⌈100/32⌉ = 4). The index region is 4 sentinel entries (`FF×16 00×4` each) = 80 bytes, followed by one segment CRC (single segment, since 4 ≤ 2¹⁶).
   - I computed `crc32c` over 80 bytes of 4 concatenated sentinel entries: got `0x80A34955`, little-endian bytes `55 49 A3 80` — matches the document's stated `0x80A34955` / `55 49 A3 80` exactly.
   - `crc_of_crc_array` = `crc32c(55 49 A3 80)` = `0xC4EE982E` — matches the document's stated value exactly.
   - Inline-payload byte offsets: I walked every field in table order (name 4B @0; layout 1B @4; linearization 2B @5; codec 2B @7; filter 2B @9; alignment 8B @11; slab 8B @19; slab-alignment 8B @27; rank 1B @35; channel-count 2B @36; dimension entry 2+8+8=18B @38; channel entry 5+2+5=12B @56; index_encoding 1B @68; entry_count 8B @69; crc_of_crc_array 4B @77) and every offset in the worked hex dump matches the field that should be there, with zero gap and zero overlap, terminating at byte 81 exactly as stated. The document's own subtotal check ("name and the nine scalars … occupy 4 + 34 bytes, the dimension entry 18, the channel entry 12, and the trailing fixed fields 13 — 81 exactly") also checks out: 4+34+18+12+13 = 81.
   - The record's extent-slot length, per `[R-CNT-17]`'s formula 20·entry_count + 4·⌈entry_count/2¹⁶⌉ = 20·4 + 4·1 = 84 — matches the document's stated 84.

4. **§11.2's grid example.** Extents (1024,2048), tile extents (256,256): G=(4,8) exactly (both divide evenly); N=32; P=65,536. With extents (1000,2048): G_y=⌈1000/256⌉=⌈3.906…⌉=4 — matches "G_y = 4 still."

5. **§11.4's tile-ordinal example.** Grid (G_y,G_x)=(4,8). Tile (1,0): s=1·8+0=8 — wait, the document states s=8 for a *different* claim (tile (0,1)→1, and separately states tile (1,0)→1·8+0=8); I re-derived s=Σtᵢ·∏_{j>i}Gⱼ for d=2 as s=t_y·G_x+t_x and got tile(0,0)=0, tile(0,1)=1, tile(1,0)=8 — all three match. For coordinate (300,700): t_y=300÷256=1, t_x=700÷256=2 (floor), u_y=300 mod 256=44, u_x=700 mod 256=188; s=1·8+2=10 (matches "tile (1,2) → s=10"); in-tile ordinal = 44·256+188 = 11,264+188 = 11,452 (matches). Planar C=4 disk ordinal = 2·32+10 = 74 (matches).

6. **§14.2's byte-layout example.** Interleaved, tile extents (2,3) ⇒ P=6, channels `a`(uint8,B=1), `b`(uint16,B=2) ⇒ Q=3, decoded size=18. Position (1,2): in-tile ordinal u=1·3+2=5. Using the table's offset formula (k div C)·Q+F_{k mod C}: for k=u·C+c, offset = u·Q+F_c. `a`: F_a=0 → byte 15. `b`: F_b=B_a=1 → byte 16, occupying [16,18) i.e. bytes 16–17 — matches "`a` at byte 15, `b` at bytes 16–17" exactly. Planar recheck: channel `b`'s plane is P·B_b=6·2=12 bytes; ordinal 5 → offset 5·2=10, bytes [10,12) — matches "bytes 10–11." Third variant (t float32, m bool): Q=5, decoded size=30, u=5 → offset 25; `t` at [25,29); `m` at F_m=B_t=4 → byte 29 — matches exactly.

7. **§14.3's packed-bool example.** P=10, alternating true/false starting true: byte0 bits0–7 = values0–7 = 1,0,1,0,1,0,1,0 (LSB-first) = `0b01010101` = `0x55` — matches. byte1: bit0=value8=true(1), bit1=value9=false(0), bits2–7=pad. With fill=false, pad bits=0 → byte1=`0x01` → tile `55 01` — matches. With fill=true, pad bits2–7=1 → byte1 = binary `11111101` = `0xFD` → tile `55 FD` — matches exactly, including which bits are "pad bits 2–7 set."

8. **§14.5's padding example.** Extents (5,5), tile extents (4,4): grid 2×2; edge tile at (1,1) covers coordinates 4–7 both axes inside a 5×5 array ⇒ exactly one real position (4,4) and 15 padding positions (16 cell positions − 1). One uint16 channel, fill `0xABCD`; decoded tile 32 bytes (P=16·B=2). Fill bytes little-endian = `CD AB` — matches "values 1–15 are each the bytes `CD AB`."

9. **§15.4's two segment-arithmetic examples.**
   - entry_count=1,000,000: segments=⌈1,000,000/65,536⌉=16 (65,536·15=983,040 < 1,000,000 ≤ 65,536·16=1,048,576); last segment covers 1,000,000−983,040=16,960 entries — matches "16 segments (15 full, the last covering 16,960 entries)." Segment-CRC array = 16·4=64 bytes — matches. Index region = 1,000,000·20+64 = 20,000,064 bytes — matches, and also matches `[R-CNT-17]`'s formula independently. Tile k=999,999: segment = ⌊999,999/65,536⌋=15 (999,999−983,040=16,959<65,536); segment-relative byte = 16,959·20=339,180 — matches. CRC-array fetch range [20,000,000, 20,000,064) — matches (immediately after the entry array). Segment 15's byte range: start=983,040·20=19,660,800; end=1,000,000·20=20,000,000 — matches "[19,660,800, 20,000,000)" exactly; width=339,200 bytes ≈ "~339 KB." One full segment = 65,536·20=1,310,720 bytes = 1.25 MiB exactly — matches.
   - Planar C=4,N=32 example: channel 2, spatial ordinal 10 → disk ordinal = 2·32+10=74; entry byte range [74·20, 75·20) = [1,480,1,500) — matches. Channel 3's 32 tiles → disk ordinals 3·32+s for s=0..31 = 96..127 — matches "entries 96–127."

10. **§16.2's slab example.** N=32, S=8, A_slab=4096: runs = 32/8 = 4 runs exactly, each 8 ordinals wide = one tile-row (G_x=8) — matches. Viewport spanning tile-rows 1–2 = ordinals [8,24) = runs 1 and 2 exactly (0-indexed run0=[0,8), run1=[8,16), run2=[16,24), run3=[24,32)) — matches "two range requests."

11. **§21.9's rationale-note arithmetic.** entry_count=2³²: segments=2³²/2¹⁶=2¹⁶=65,536; CRC array=65,536·4=262,144 bytes=256 KiB — matches. At entry_count=2³⁶: segments=2³⁶/2¹⁶=2²⁰=1,048,576; CRC array=1,048,576·4=4,194,304 bytes=4 MiB — matches "it reaches 4 MiB at 2³⁶."

12. **Register completeness accounting (§21.1, §21.8).** I counted table rows programmatically by section: F=35, L=49, T=26, R=10; sum=120 — matches "120 conditions" in §21.8 exactly, and matches the per-section counts stated in each subsection's lead sentence (35, 49, 26, 10). I additionally parsed every row's "Instances" column (splitting on `;`, treating a lone `—` cell as one instance per the document's own stated convention in §21.1) and summed to **277** — matches "over 277 instances" in §21.8 exactly. This is a strong, mechanically-checked confirmation that the register's own completeness bookkeeping is internally consistent; I found no row miscount and no instance-count drift.

13. **Fixed-layout table self-consistency.** I walked the trailer table (§6.2: 8+2+2+4+8+8+8+8+12+4 = 64, no gaps) and the record-header table (§7.2: 2+2+4+8+8=24, no gaps) and the tile-index-entry table (§15.1: 8+8+4=20, no gaps) field by field against their stated offsets; all three sum exactly to their declared structure sizes (64, 24, 20) with every field's offset equal to the running total — no gap, no overlap, in any of the three.

None of the above turned up a numeric or offset defect. Every worked example's printed bytes, checksums, and derived quantities are correct given the document's own rules, and every fixed-layout table I checked partitions its structure exactly.

## Diagram/table findings

### Finding 1 — §20.3's two annotated commit diagrams draw brackets that overrun their own cell by one column (AMBIGUITY, non-byte-level)

This is inside the "Example — the three shapes a commit takes" figure, which is squarely in the changed surface (§20.3).

Diagram (b) ("Tiles added to an existing layer," lines 3430–3434):

```
before │front│ tiles │ index │ dir₁│pad│tr₁│
after  │front│ tiles │▓index▓│▓▓▓▓▓▓▓▓▓▓▓▓▓│ +tiles │ index′ │ dir₂│pad│tr₂│
                      └ old ─┘                       └───────┘ every entry, re-emitted
```

I located the `│` divider positions in the `after` row and the `└`/`┘` positions in the annotation row by exact character index (script in evidence). Result:

- The `▓index▓` cell occupies content columns 22–28 (7 characters), bounded by dividers at 21 and 29. The bracket `└ old ─┘` is 8 characters wide (`└`, ` `, `o`, `l`, `d`, ` `, `─`, `┘`) — one character too wide for a 7-character cell — so its `└` lands one column to the right of the left divider (at content-start, 22, not at the divider, 21) while its `┘` lands *on* the right divider itself (29), one column past the cell's last content character (28).
- The ` index′ ` cell occupies content columns 53–60 (8 characters), bounded by dividers at 52 and 61. The bracket `└───────┘` is 9 characters wide (7 dashes) — again one character too wide for an 8-character cell — landing `┘` on the right divider (61) instead of the cell's last content column (60).

Both brackets are elongated by exactly one character on the closing side, and in both cases the closing bracket comes to rest exactly on top of the divider that begins the *next* cell, rather than on the last character of the cell it is labelling. I checked whether this is simply this diagram's convention (in which case it would not be a defect) against §5.1's "file after three commits" diagram (lines 667–670), which uses the same `└label┘`-under-a-bordered-cell idiom: there, every bracket's `└` and `┘` land *exactly on* both dividers of the cell they label (verified: dividers at 8/20 for "layer A," bracket at 8/20 exactly; dividers at 28/40 for "layer B," bracket at 28/40 exactly; dividers at 48/69 for the combined dir₃+pad+trail₃ span, bracket at 48/69 exactly) — a different, but internally consistent, convention (bracket width = divider-to-divider span inclusive, not content width). Diagram (a) in the same §20.3 example (lines 3413–3415) uses the same "one column too wide, closing bracket lands on the following divider" pattern as diagram (b), consistently on *both* of its brackets.

I cannot, from the text alone, establish which of the two conventions is the intended one, or whether the §20.3 diagrams were drawn independently of §5.1's and are simply uneven in style rather than wrong. What I can establish is that within §20.3, the pattern is applied uniformly (all four brackets across diagrams (a) and (b) show the identical one-column overrun), which weighs against this being a single freshly-introduced slip (a slip would more plausibly show up as one bracket disagreeing with its neighbor, not four agreeing with each other) and toward it being this example's original, if imprecise, house style. I report it because the charter asks me to check every figure's annotation against the structure it labels, and because a reader who takes the bracket boundary literally would be told that the label "old" (or the "re-emitted" label) extends one byte-column into the neighboring, differently-described region — which is not what the prose means. This is not a byte-level finding: the figure is inside a block explicitly labelled "**Example**," which `[R-CNF-01]` exempts from normative force, and the actual rule governing re-emission (§20.3 step 4's own prose, `[R-WRT-04]`, `[R-WRT-05]`) is unambiguous and does not depend on where a bracket is drawn in this illustration.

### Finding 2 — §6.2's trailer layout table names "an updater, appender or rewriter" as three coordinate alternatives, when the second two are the first's only tiers (AMBIGUITY, non-byte-level)

§6.2's trailer byte-layout table, the `flags` field's "Valid values" cell (line 838):

> bits 16–31 (ignore lane) 0 from a creator, carried forward unchanged by an updater, appender or rewriter alike, a set bit ignored (§6.3)

"Updater" is defined at §2.3 and named again at §20.1 as having *exactly two tiers*, "appender" and "rewriter" (`[R-CNF-06]`: "Its tiers, the appender and the rewriter, are §20.1's"). Listing "an updater, appender or rewriter" as three parallel items joined by commas and "or" reads as three coordinate alternatives at the same level — a class alongside its own two members — rather than as an appositive clarifying that "updater" here means "in either of its two tiers." Compare the document's own, differently-built version of the identical claim at §6.3 (lines 912–913): "carried forward by every updater under this text, **appender and rewriter alike**" — there the class noun ("every updater") is followed by an appositive using "and … alike," the idiomatic English pairing ("young and old alike," "rich and poor alike"); "alike" does not idiomatically pair with "or." The table cell's "an updater, appender or rewriter alike" mixes the class noun into the same list as its tiers and uses "or" where the parallel, correctly-built sentence elsewhere in this document uses "and."

I traced whether this creates any actual coverage gap or double-count: it does not. `[R-CNT-08]` states the substantive rule directly and unconditionally ("An updater MUST copy forward unknown ignore-lane bits of its input file, MUST NOT clear them, and MUST NOT set any other") and does not depend on this table cell's wording, which is a restatement (per §4.7's Note, this layout table's cells are "the rules below the table" restated in summary, and per §21.1's principle for restatements elsewhere in this document, the prose rule governs where a restatement and the rule could be read to diverge). I am reporting this as a table-content finding — a "class beside one of its own tiers" listing inside a byte-layout table's Valid-values cell, which is exactly the shape of defect the round's brief calls out to check for ("a site naming the class beside one naming the tier is a finding only where the two together leave some actor undecided or decide it twice") — but on inspection the two together do **not** leave any actor undecided or decide any actor's obligation twice, since every updater is, without remainder, either an appender or a rewriter, and `[R-CNT-08]` already binds "every updater" unconditionally regardless of tier. So this is a wording defect in a table cell, not a scope defect: it does not change which bytes a conforming updater may emit. Not byte-level.

## Rejected candidates (checked and closed)

- **§9.2's "what a crash sees" diagram arrows** (lines 1348–1355): checked `↑` marker column against the preceding row's final `│` position in both the "committed" and "mid-commit" rows. Both arrows sit exactly one column past their row's closing `│`, consistently between the two rows — this is the correct place to mark "F," which denotes the byte position *immediately after* the trailer's last byte, not a byte inside it. No defect.
- **§20.5's compaction diagram** (lines 3678–3682): no annotation brackets to check (only free-floating `file_id = X` / `file_id = Y` captions beneath the whole diagram, not tied to a specific column); the input/output regions I could check (front, A, B, A-index, B-index′, dir, pad, tr) match the accompanying prose's claims about what moves and what doesn't (A's extents don't move in this placement so its index is "copied," B's index is regenerated and marked with a prime, matching `[R-WRT-07]`'s text). No defect.
- **§10.2's numeric-identifier-spaces table** vs. the finer reserved-subrange language in §11.4 (linearization: "2 and 3 reserved without semantics; 4 through 0x7FFF reserved for future assignment") and §12.2 (sample type: "14–19 reserved without semantics; 20–0x7FFF reserved for future assignment"): the §10.2 table merges these into one "Reserved" column value per space (e.g. "2–0x7FFF," "14–0x7FFF"). I considered this a possible table/prose mismatch, but §10.4's own text (`[R-EXT-05]`) states plainly that where "the registry, §10.2's table, and Appendix C diverge, the section that defines the space governs — the registry is machine-readable convenience, never a second authority," so a coarser summary table that omits a finer sub-partition the defining section draws is exactly the documented relationship, not a defect. Closed.
- **Appendix H's "Conforming updater" paragraph** against current §20.4 and §20.1 prose: checked every clause (drops a layer record only under the PE=0 licence with sub-records going with it; an unknown critical sub-record blocks both modification and drop of that layer; an unimplemented top-level MU=1 record is rejected outright; a rewriter mints a fresh file_id, preserves content, regenerates relocated index regions, refuses on an unimplemented MU=1 record) against §20.4's table, its surrounding paragraph, and §20.5's text word for word. All matched. Closed.
- **Appendix G item 8** ("`version_minor` at the floor … and `flags` = 0 … The `flags` half is a creator's rule … a rewriter adopting the profile carries its input's unknown ignore-lane bits forward instead") against §20.1's closing paragraph and §20.5: matched (creator writes flags=0 per §6.3/§20.2; rewriter instead copies forward per §20.5/`[R-WRT-06]`). Closed.
- **§15.3's entry-validity table**, "six rows marked *structural*" claim: counted the literal occurrences of the word "structural" in the table body — got 6, matching the prose's count exactly. Closed.
- **§14.1/§14.2/§13.2 core-type and layout value-set tables** against the type-count claim in §12.1 ("exactly thirteen sample types") and the codec/filter/layout "core, all N of them" claims in §17.2/§17.3/§14.1: 13 sample types (§12.1's table has 13 rows, IDs 1–13, no gaps), 4 codecs (§17.2, IDs 1–4), 2 filters (§17.3, IDs 1–2), 2 layouts (§14.1, IDs 1–2), 2 metadata encodings (§18.2, IDs 1–2), 2 record types (§7.3). All match the "Conforming reader" checklist entry in Appendix H, which restates all six counts in one sentence. Closed.
- **§20.3 diagram (c)'s missing annotation row**: the prose explicitly says "a run the figure below does not draw," so the absence of a bracket/annotation line under diagram (c) is licensed by the prose itself, not an omission. Closed.

## What I did not, and could not, verify from the document alone

- I cannot compare this round's figures against round 36's or any earlier round's versions of the same figures (no git diff, no ADRs), so I cannot say with certainty which of my two findings, if either, is a change introduced in this round versus a longstanding trait of the document. I have reported both on their present-tense merits, as the brief asks, and flagged in Finding 1 specifically why the *uniformity* of the pattern across two diagrams argues against it being a single fresh slip.
- I could not exercise the §21.9 tile-count guarantee vector "arithmetically" beyond what §21.9's own Note already gives (the document itself says the full vector "is not [constructible]... and is exercised instead by a scaled vector," which I have no way to build or check further without the conformance corpus, which I was told not to read).

## Evidence summary (for the structured result)

- Sweeps run: CRC-32C self-test (2/2 match); Appendix A full byte-level re-derivation (3/3 checks match: dir CRC, trailer CRC, file_id decode); §7.4 `sst` example full field-offset walk (14/14 fields land at the stated offset, 0 gaps) plus 3/3 checksum re-derivations match; 6 further worked-example arithmetic re-derivations (§11.2, §11.4, §14.2, §14.3, §14.5, §16.2) — 100% match; register row-count sweep (grep-based table row counts) — F=35, L=49, T=26, R=10, sum=120, matches; register instance-count sweep (semicolon-split parse of all 120 Instances cells) — sum=277, matches; fixed-table gap/overlap sweep on 3 structures (trailer, record header, tile-index entry) — 0 gaps, 0 overlaps in all 3; bracket-to-divider column-position sweep on all 7 annotation brackets in the document (3 in §5.1, 4 in §20.3) — found the §20.3 group's uniform 1-column overrun (Finding 1); actor-noun sweep (`grep -n "appender\|rewriter\|updater\b"`, 70 hits) read in full for class/tier mixing inside tables specifically — found one instance (Finding 2, §6.2 trailer table).
- Derived numbers computed myself, each checked against the document's own stated figure: segment CRC of 80 sentinel-entry bytes (`0x80A34955`, matches); `crc_of_crc_array` of that segment array (`0xC4EE982E`, matches); extent-slot length via `[R-CNT-17]`'s formula (84, matches); grid counts and ordinals for §11.2/§11.4's examples (all match); byte offsets and decoded sizes for §14.2/§14.3/§14.5's examples (all match); segment/entry arithmetic for both §15.4 examples at scale (all match, including the 256 KiB / 4 MiB figures in §21.9's Note); slab run count and viewport range for §16.2's example (match); register row and instance totals (35/49/26/10/120 and 277, both match).
- Rejected candidates: listed above with the sentence or rule that closed each (§9.2 diagram arrows; §20.5 compaction diagram; §10.2 table vs. finer subrange prose, closed by `[R-EXT-05]`; Appendix H and Appendix G item 8 against §20.4/§20.1/§20.5, closed by word-for-word match; §15.3's structural-row count, closed by literal count; core-type/codec/filter/layout counts, closed by literal count).
- Confidence where I found little: the vast majority of this document's figures and worked examples are byte-for-byte, arithmetically correct given the document's own rules — I verified this by recomputation, not by reading the prose next to the numbers and eyeballing agreement, so a genuine off-by-one in a checksum, an offset, or a count would have surfaced in one of the sweeps above (all of which are exhaustive over their target, not sampled). The two findings I do report are both wording/rendering issues in figures (a diagram's bracket width, a table cell's actor list), neither of which I can show moves a byte a conforming implementation emits or a verdict it reaches — I have said so plainly in each finding rather than reaching for byte-level status they cannot support.
