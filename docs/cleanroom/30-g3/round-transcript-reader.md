# Round 30 — Reader implementer transcript

## Disclosure

I read exactly one file: `/Users/robertkleffner/Documents/GitHub/tarn-first-draft/spec/tarn.md`,
in full (4,743 lines, 47,313 words), in eight `sed -n` chunks. I ran `grep`, `awk`, `tr`, `sed`
against that one file only, and one Python script that reads no files:
`/private/tmp/claude-501/-Users-robertkleffner-Documents-GitHub-tarn-first-draft/r30-round/scratch/reader/r30_reader_crc.py`
(CRC-32C and arithmetic checks). I wrote this transcript and nothing else to the output directory,
and did not list or read that directory.

Context I did not ask for: my runtime placed a project-instruction pointer (`CLAUDE.md` → `AGENTS.md`)
and an index of four auto-memory notes about this project into my context before I began. I did not
open any of those files and I did not act on the index entries; I disregard them as evidence. No
ADR, finding, plan, registry, conformance vector, or git history was consulted. The spec was where the
brief said it was.

## 1. The open path (a cold remote open, ranged transport)

Written in the order I would code it.

**Request 1 — suffix range `bytes=-64`.** The response carries the transport-authoritative size F
(`[R-CNT-10]`; a 200 response must be handled deliberately, never treated as the range). Cost: 64
bytes. Before this request I know nothing; after it I know F and hold the trailer.

Validation in `[R-CNT-06]`'s fixed order:

1. Trailer magic at [F−64, F−56) == `8A 4E 52 41 54 0D 0A 1A` (F8; byte-reversed = F1). Reaches every
   major.
2. Trailer CRC: u32 at [F−4, F) == CRC-32C over [F−64, F−4) (F14). Reaches every major.
3. Version gate: version_major (u16 at F−56) == 1; 0 → reject-file (F18); other → reject-file on
   capability grounds with the distinct diagnostic `[R-CNT-07]` asks for. Note the front block
   check, if the bytes are resident, precedes all of this (`[R-CNT-04]`, F6 — reaching).
4. Then, only for major 1: incompat lane bits 0–15 all clear (F19); ignore lane ignored;
   committed_file_length == F (F17) and F mod 64 == 0 (F13); dir_offset ≥ 16 (F9); dir_length ≥ 4
   (F16); dir_offset + dir_length checked for the 2⁶³−1 domain (F2) and overflow (F3) and ≤ F−64
   (F10); file_id ≠ 0 (F12); reserved [48,60) zero (F15). F < 128 → F5 (`[R-CNT-27]`; not in the
   §6.2 order but reject-file either way for major 1; for a foreign major it does not reach and no
   violation is established — §2.3's Note explains why: the 128 floor is major 1's).

**Request 2 — `bytes=dir_offset-(dir_offset+dir_length−1)`.** Cost: dir_length bytes. Before I read
it, dir_length is bounded by 4 ≤ dir_length ≤ F − 80 (from dir_offset ≥ 16 and the sum bound), and by
§21.9 I must accept up to 16 MiB; above that I MAY decline on resource grounds, reported as a limit.
Verify the final 4 bytes == CRC-32C of the first dir_length − 4 (F20) before any other use.

**Total: 2 requests, 64 + dir_length bytes.** A speculative suffix window of W bytes makes it one
request whenever dir_offset ≥ F − W; if W reaches offset 0 the front block becomes resident and must
then be verified by equality (Appendix A walks this for the 128-byte file: a 112-byte window spares
the second request and leaves [0,16) non-resident).

**Record walk (still at open, no further I/O).** Parse 24-byte headers with no residue (F29). type 0 →
reject-file (F24). Known types get fixed semantics regardless of stored MU/PE (`[R-CNT-22]`). Unknown
type MU=1 → reject-file (experimental → conforming file I refuse; reserved → F35); MU=0 → ignore-record.
For every non-layer top-level record, check the extent slot (F30–F32, F2/F3 instances). For a
user-metadata record: at most one (F34), inline_length == 1 (F23), slot not (0,0) (F21), extent_length
≥ 5 (F22), encoding byte 0 or 3–0x7F → R1 ignore-record here at open; ≥ 0x80 → ignore-record, not a
violation. For each layer record, parse only the name field; if it does not fit inline_length, no
name enters the namespace and the layer is reject-layer (`[R-CNT-18]`). Duplicate raw name bytes →
reject-file (F4), decided before validity; ill-formed / empty / control-char name → reject-layer at
open (L3, L5, L6). Completing this is "the open" (`[R-RDR-01]`).

## 2. Validation timing by tier

I reproduced the register's detector/tier census mechanically (see §6): open 31 rows + R1's top-level
half; layer access 35 rows + R1's sub-record half; tile use 24 rows (L37, L38, T1, T3, T6–T25); extent
use 9 rows (R2–R10); verifier-only 20 rows (F7, F25–F28, F33, F36, L18, L25, L40–L42, L46–L49, T2,
T4, T5, T26) which a reader is permitted never to check, though `[R-CNF-12]` lets it reject a
nonconforming file if it happens to notice one. Earlier detection is always licensed; the tier is the
latest point (`[R-RDR-02]`). Reject-layer is prospective; values already returned stand (§2.4, §19.4
step 8).

**Layer access** (first use of any declaration other than the name; no I/O): slot rules (L15–L17,
L1/L2 sums), exact parse and sub-record walk (L13, L14, L23, L24, L26, L19, L10–L12, R1), §7.4
constraint set (L27–L31, L34–L36, L39, L43, L45, L20), names (L4, L7–L9), geometry floor (L32),
grid arithmetic and every designated product ≤ 2⁶³−1 (L2), bool fill (L35), lz4 cap (L44),
`[R-CNT-17]` cross-checks (L21, L22).

**Tile use**: the index chain (L37 crc_of_crc_array over the fetched CRC array; L38 the segment CRC),
entry classification (T6–T12), codec-1 length equality (T14, before any fetch), payload CRC (T1),
decode (T13, T15–T25), size (T3). **Extent use**: R2 CRC, then the document rules R3–R10 under an
assigned encoding only.

## 3. Layer access and the tile-read algorithm

From (layer name, coordinate x, channel set):

1. Domain: 0 ≤ xᵢ < Eᵢ, else the request fails as a request. Zero-extent layer → no samples.
2. tᵢ = xᵢ div Tᵢ, uᵢ = xᵢ mod Tᵢ; s = Σ tᵢ ∏_{j>i} Gⱼ; in-tile ordinal u = Σ uᵢ ∏_{j>i} Tⱼ; disk
   ordinal k = s (interleaved) or c·N + s (planar, per requested channel).
3. Segment σ = k div 2¹⁶. Fetch the CRC array at region bytes [entry_count·20, extent_length) —
   ⌈entry_count/2¹⁶⌉·4 bytes — and segment σ at [σ·2¹⁶·20, min((σ+1)·2¹⁶, entry_count)·20);
   verify crc_of_crc_array over the array, then the σ-th u32 over the segment. Both ranges are
   computable from the layer record; may be one coalesced fetch when the layer has one segment.
4. Entry at segment-relative 20·(k − σ·2¹⁶). Classify per §15.3: `FF×16 00×4` → fill, bit-exactly
   from the channel entry; six structural rows → reject-tile (never fill).
5. Fetch [offset, offset+length); verify crc.
6. Codec inverse (1 verbatim with length == decoded size; 2 raw DEFLATE; 3 one zstd frame with the
   header gates; 4 one LZ4 block with decoded size as capacity) — output must be exactly the decoded
   size and consume the extent exactly; then the filter inverse (byte-shuffle with s = Q interleaved,
   Bᶜ planar numeric, identity for packed bool: restore byte i·n + j to j·s + i).
7. Decoded layout: interleaved — value of channel c at ordinal u is at byte u·Q + Fᶜ, Bᶜ bytes
   little-endian (bool one byte 00/01, resolved 00→false else true only on a nonconforming byte);
   planar numeric — u·Bᶜ; planar bool — bit u mod 8 of byte u div 8. Never return a padding
   position (uᵢ + tᵢTᵢ ≥ Eᵢ).
8. Return bit patterns unaltered.

Worked (from §11.4/§15.4): grid (4,8), T (256,256); (y,x) = (300,700) → tile (1,2), s = 10, in-tile
(44,188), u = 44·256 + 188 = 11,452; planar c = 2, N = 32 → k = 74 → region bytes [1,480, 1,500).
All of these I recomputed and they match.

## 4. Degradation walks (five traced end to end, plus three)

1. **Unknown top-level record type 0x9000, MU=0, PE=0, slot (4096, 100).** Open: slot checked
   (F30–F32 pass), then ignore-record. Every layer serves normally. An updater carries it forward or
   drops it only in a commit that independently changes the file's layer set / a layer record /
   another non-layer record. Same type with MU=1: reject-file; the file is conforming (§21.6) and I
   refuse it on capability grounds; I may serve nothing.
2. **Codec value 7 on layer B.** Layer access: L43 → reject-layer; I may still list B's name; layer
   A's reads are unaffected; a region request touching only A succeeds.
3. **Trailer flags bit 3 set.** Open: F19 → reject-file, nothing served. Bit 20 set: ignored, file
   conforming, served fully; a compactor copies bit 20 into its output.
4. **Truncated tail (crash mid-commit).** Suffix request returns 64 bytes of payload/index residue:
   F8 (or F14, or F17) fails → reject-file, report torn; I MUST NOT scan backward (`[R-LIF-05]`).
   Nothing served. Recovery is §9.6, a separate tool.
5. **Payload CRC mismatch on tile k.** Tile use: T1 → reject-tile; the read of that tile reports
   failure and never returns fill; neighbours unaffected; a region request may return the other
   tiles' values plus a per-tile failure report or fail whole (`[R-RDR-04]` step 8).
6. **Segment CRC mismatch.** L38 → reject-layer although detected at tile use; values already
   returned stand; no further service from the layer.
7. **Directory of 20 MiB.** Conforming; exceeds the 16 MiB guarantee; I MAY decline the whole file,
   reported as a resource limit, never as corruption (`[R-ERR-04]`).
8. **version_major = 2.** Front block (if resident), magic, CRC checked and passed; then reject with
   "TARN format major 2; this reader supports major 1". Not a finding about its bytes. If the magic
   were wrong the failure is F8, on `[R-CNT-06]`'s ground, whatever the major says.

## 5. Worked example — Appendix A and §7.4, checked

Everything I could compute reproduced (script output in §6): CRC-32C("123456789") = 0xE3069283;
Appendix A trailer CRC over the 60 bytes = 0x402F157E; file_id bytes `EF CD AB 89 67 45 23 01`;
§7.4's 80-byte all-sentinel segment CRC = 0x80A34955, crc_of_crc_array over `55 49 A3 80` =
0xC4EE982E, payload 81 bytes with the offsets as printed (4 + 34 + 18 + 12 + 13), extent 84;
§15.4's full-segment constant 0xEECB3BB2 and its 1,000,000-entry example (16 segments, last 16,960;
region 20,000,064; k = 999,999 at segment-relative 339,180; segment 15 at 19,660,800);
§17.3's shuffle bytes; §14.3's `55 01` / `55 FD`; §20.3's 644; §9.2's Note's +68 → +128;
[R-CNT-06] governs exactly nine register rows (F8, F9, F10, F12, F13, F14, F15, F16, F17) as §2.3
and §21.7 say; §21.8's 120 conditions (35 + 49 + 26 + 10) over 277 instances.

## 6. Sweeps and derived numbers

Line-oriented `grep -c`: "declaration-derived" 9; "P·Q" 7; "P·Bᶜ" 7; "conduct" 6; "nonconforming" 28;
"no earlier" 2; "MAY detect any violation earlier" 1; "every such run" 1; "strict specialization" 1;
"makes each stored tile it reaches" 1; "resident" 9; "reaching condition" 2; "Note.**" 56;
"Rationale.**" 13; "Example" 21; lines beginning "> " 686. Zero hits line-oriented — then confirmed
present with whitespace normalised (`tr '\n' ' '`, `> ` stripped): "These products and sums are
declaration-derived" 1; "are the cases this text states" 1; "not nonconforming on that account" 1;
"makes each stored tile it reaches nonconforming" 1; "declared so here on the model" 1; "no earlier,
since the open fetches no extent" 1; "the decoded sizes §14 derives from it" 1; "P·Q and P·Bᶜ are
checked in an empty layer" 1; "for every such run" 1. Positive controls: "sample stride" 3, "MUST
classify as follows" 1, "pre-trailer pad" 11. Unlabelled-blockquote census: the only genuinely
unlabelled `>` block is §15.1's region layout line (line 2147) — normative; all other flagged lines
are continuation paragraphs inside labelled Examples. Register census by (detector, tier): reader/open
31, reader/layer access 35, reader/tile use 24, reader/extent use 9, reader/open+layer-access (R1) 1,
verifier/certification 20 → 120.

## 7. Findings

### reader-01 — AMBIGUITY, byte-level — §14.2 `[R-SER-02]`, §21.3 L2, §19.3 `[R-RDR-03]`: is P·Q a designated quantity of a *planar* layer?

Quotation (§14.2): "| planar, numeric channel c | P · Bᶜ | k · Bᶜ | / | interleaved | P · Q |
(k div C) · Q + F_{k mod C} | where Bᶜ is channel c's element size (§12.1; 1 for bool), Q = Σ Bᵢ over
all channels (the **sample stride**), and Fᶜ = Σ Bⱼ over channels j < c (channel c's in-sample
offset). These products and sums are declaration-derived quantities under `[R-ENC-04]`."
L2's Instances cell: "… N·P; C·N (which dominates the max disk ordinal (C−1)·N + (N−1)); P·Q (which
dominates V = P·C); P·Bᶜ; …" §19.3: "the 2⁶³ − 1 ceiling on every quantity that arithmetic derives
(`[R-ENC-04]`) and on the decoded sizes §14 derives from it (`[R-SER-02]`, `[R-SER-07]`)". §17.2's
Note: "so P·Q and P·Bᶜ are checked in an empty layer even though this cap is not."

Readings. (i) "These products and sums" designates every product written in the table and the
where-clause, for every layer: P·Q is formed and ceiling-checked whatever the layout. L2's cell lists
P·Q and P·Bᶜ untagged, whereas every other layout-varying cell (L44, T3, T14, T21, T22) tags
"interleaved P·Q; planar numeric P·Bᶜ", which suggests L2's author meant both to be checked
unconditionally; the §17.2 Note reads the same way. (ii) The table is layout-keyed: the designated
quantity is *the decoded size*, which is P·Q under interleaved and P·Bᶜ under planar, so a planar layer
has no quantity P·Q; §21.1's convention ("Where the quantity a condition derives varies by layout, the
layout formulas are materially different shapes and the cell enumerates them") makes L2's two entries
the two layout shapes of one quantity, and §19.3's "the decoded sizes §14 derives" says the same.
`[R-ENC-04]` itself says a designation is "express, made by the section that defines the quantity",
and §14.2 defines the interleaved decoded size, not a planar P·Q.

I picked (ii): it is the reading the table's structure supports and the one a reader that only ever
forms P·Q to allocate an interleaved image would naturally implement. The fork: a planar layer with
one dimension of extent 0 (legal, `[R-GEO-02]`), tile extent 2⁵² (legal, `[R-GEO-01]`), and 4,096
uint8 channels. P = 2⁵², Bᶜ = 1, Q = 4,096: P·Bᶜ = 2⁵² and V = P are in domain; P·Q = 2⁶⁴ is not.
N = 0, entry_count = 0, no tile is addressed, so every §21.9 row is satisfied (the tile row ranges
over addressed tiles; rank 1; C = 4,096 is exactly the guarantee). Reader/verifier A under (i)
rejects the layer (L2) and reports *nonconforming*; reader/verifier B under (ii) accepts and
certifies. Under (ii) the file is conforming and within the guarantees, so `[R-CNF-03]` obliges
acceptance and A is nonconforming; under (i) B has missed a reader-detected row. The emittable set
moves with the reading. I flag it byte-level with the honest caveat that only a degenerate (empty)
layer reaches it: with an addressed tile the same declarations exceed the 256 MiB tile guarantee and
a refusal is licensed either way.

### reader-02 — CONTRADICTION, not byte-level — §2.3 `[R-CNF-02]` vs §9.2 `[R-LIF-02]`'s conduct paragraph

`[R-CNF-02]`: "A writer obligation whose violation this specification expressly declares not to be a
file-conformance violation binds the actor in the same way; §6.3's flags = 0 against a set ignore-lane
bit and §6.2's pre-trailer gap longer than `[R-LIF-02]` step 5's pad are the cases this text states,
and each is declared where it arises rather than enumerated here."
§9.2: "Steps 4 and 6 bind a writer's **conduct** rather than its output, and are declared so here on
the model `[R-CNF-02]` states: … A writer that omits a barrier violates this requirement, and the
file it produces is not nonconforming on that account."

§9.2 is a third express declaration of exactly the kind the first sentence describes, made "on the
model `[R-CNF-02]` states", yet `[R-CNF-02]` presents two as "the cases this text states". An
implementer deriving the closed list gets three where the text says two (shape 5: a list presented as
complete). Nothing about bytes turns on it — all three are conduct rules and all three files are
conforming — so it is not byte-level; but the sentence that closes the count is normative and now
false.

### reader-03 — CONTRADICTION, not byte-level — §20.3 step 4's re-typing paragraph vs `[R-CNF-02]`

§20.3: "Where a change does reach them it makes each stored tile it reaches nonconforming, and
re-emitting those tiles would strand the originals as slack". `[R-CNF-02]`: "File conformance is a
pure predicate on bytes: it does not depend on any reader, writer, or environment."

Take an int8 channel re-typed to uint8 by a directory-only commit, on a layer whose stored tiles carry
no padding position (extents multiples of tile extents). Every byte of the result is a valid uint8
sample (`[R-TYP-05]`), no §21 row applies, and §21.7 classes wrong content as unwitnessed. The
resulting byte sequence is one a conforming *creator* can emit directly — a uint8 layer with those
tiles, and the superseded int8 directory reproduced as slack, whose content is unconstrained
(`[R-CNT-21]`, `[R-CNT-03]` only advises zeroing). A pure predicate on bytes cannot call the tiles
nonconforming in one file and conforming in the byte-identical other. The bar itself is clear and I
do not dispute it; the sentence characterising its consequence is what is wrong, and it was
plainly written to close a reading (shape 11). No verifier can establish it and no reader's
behaviour changes, so not byte-level.

### reader-04 — OBSERVATION, not byte-level — §21.3 L23's Detected cell vs §19.1 step 4

§19.1: "a layer record whose name field does not lie entirely within that record's inline_length
yields no name field to compare, so it contributes no name to the namespace and is instead a validity
error at layer scope (`[R-CNT-18]`)." L23: "A declared region of the layer record's inline payload
does not lie entirely within inline_length (overrun or truncation) | leading fixed fields (name … C);
… | reader | layer access | `[R-CNT-18]`". §19.2 puts "the layer-name namespace" at open, and
`[R-RDR-02]` makes detection due no later than first reliance, which for the name is the open; the
row's tier for the name instance is therefore one tier late, and the rule governs (§21.1). Only
reporting timing differs; nothing served changes.

## 8. Rejected candidates

- `[R-CNF-03]`'s acceptance exemption "carrying no record of a type it does not implement with
  MUST_UNDERSTAND = 1" reaches a sub-record, but `[R-CNT-18]` closes it: "where the file is
  otherwise conforming a reader MUST NOT reject the file for it". Settled.
- §19.2's "no earlier, since the open fetches no extent" against "A reader MAY detect any violation
  earlier": the bullet states where the obligation attaches (the Rationale: "The rule fixes the
  *latest* detection point"); and ignore-record served data is identical either way.
- §18.2's Note "a reader that instead declines on resource grounds under `[R-ERR-04]` does so at the
  whole file" against `[R-ERR-04]`'s "or the record carrying a user-metadata document, as §18.2
  assigns": the record-scope decline *is* the ignore-record §18.2 assigns; both are licensed on a file
  that exceeds a guarantee. Reconciled.
- `[R-SLB-04]`'s "for every such run" (which runs?): `[R-SLB-03]` already requires the invariants of
  every run when declared, so the antecedent question cannot move a verdict.
- Local vs remote readers giving different verdicts on a bad front block: by design, the file is
  nonconforming (F6), `[R-CNF-12]` licenses either verdict.
- Unknown MU=0 record with a malformed slot: "skipped as though absent" vs F30–F32: §19.1 step 4
  expressly applies the slot rules to non-layer top-level records and `[R-CNF-04]` binds the reader
  to the row. Settled.
- F5's absence from §6.2's order: reject-file either way for major 1; `[R-CNF-13]` fixes that it is
  not established on a foreign major regardless of order.
- §21.1's strict-specialisation list (F1⊂F6/F8, F35⊂F36, L24⊂L25, F21⊂F22, L10⊂L11): each checked and
  holds; F5 is not a specialisation of a single row (F10 or F13 or F17), and the list says it is not
  closed.
- Stored (compressed) extent length has no §21.9 row: `[R-SEC-02]` corroborates the extent against F,
  so the attacker ships every byte the reader reads; not amplification.
- §11.1's Rationale restating §20.3's two bars: read side by side, quantifier for quantifier (tense,
  carve-out, "a layer the commit itself empties does not qualify"); they agree.
- §2.3's "nine" conditions under `[R-CNT-06]`: derived nine rows; matches.
