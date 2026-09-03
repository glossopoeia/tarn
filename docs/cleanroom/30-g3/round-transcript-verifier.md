# Cleanroom round 30 — Verifier implementer transcript

## 0. Disclosure

Read: `/Users/robertkleffner/Documents/GitHub/tarn-first-draft/spec/tarn.md`, all 4,743 lines, in
sequential `sed -n` windows, plus targeted `grep`/`sed` re-reads of it. Nothing else in the
repository was opened; no directory was listed; no git command, web fetch or web search was run.

Ran, in my own scratch directory
`/private/tmp/claude-501/-Users-robertkleffner-Documents-GitHub-tarn-first-draft/r30-round/scratch/verifier/`:

- `crc_check.py` — a from-scratch CRC-32C (reflected 0x82F63B78, init/xorout 0xFFFFFFFF) reproducing every checksum constant the document states.
- `count_rows.py` — a regex count of §21.2–§21.5 rows and their Instances cells.
- `build_file.py` — builds a concrete four-generation file (create, append, update, compact), computes every CRC in it, and runs a coverage walk over each generation. It wrote `gen3.tarn` (the third generation's bytes) into the same scratch directory.

One `sed` window's output exceeded the tool's display cap and was saved by the tool runtime to its own tool-results path; I did not open that saved file, and instead re-read the same spec lines in smaller windows.

Context I did not ask for: the runtime placed a project instruction file (pointing at AGENTS.md), an index of the maintainer's memory notes (four titled entries), and a user email address into my context before I began. I did not open any file they name and did not act on their contents; nothing below rests on them.

## 1. Method

The document is hard-wrapped and blockquotes wrap with `> `. Every phrase sweep below was either a short unwrappable fragment, or was run against a whitespace-normalised copy of the text (all `\n` and `> ` collapsed to single spaces). Where a line-oriented grep returned zero for a phrase I expected to exist ("the cases this text states"), the normalised search found it (it wraps at "text / states"), and every zero I rely on was paired with a presence check of a phrase known to be in the same passage.

Label census: the only blockquote opener in the document without a *Note*/*Example*/*Rationale* label is at line 2147, §15.1's `> [ entry array … ] [ segment CRC array … ]` region layout. Under [R-CNF-01] it is normative. Every other `>` block (93 openers) carries a label. The front matter's "How to read this document" block carries a **Note** label and is therefore non-normative.

## 2. Reproduced constants

| Document figure | Where | My computation |
|---|---|---|
| CRC-32C("123456789") = 0xE3069283 | §4.5 | E3069283 ✓ |
| CRC-32C(zero bytes) = 0x00000000 | §4.5, §5.1, App. A | 00000000 ✓ |
| Appendix A trailer CRC 0x402F157E over the 60 bytes listed | App. A | 402F157E ✓ |
| Segment CRC over 4 sentinel entries (80 bytes) = 0x80A34955 | §7.4 example | 80A34955 ✓ |
| crc_of_crc_array over that one u32 = 0xC4EE982E | §7.4 example | C4EE982E ✓ |
| CRC of a full 2¹⁶-sentinel segment = 0xEECB3BB2 | §15.4, App. B | EECB3BB2 ✓ |

All six reproduced. There is no checksum constant in the document I could not compute locally.

Other document figures re-derived: §7.4 example payload 4+34+18+12+13 = 81 bytes, extent 4·20+⌈4/2¹⁶⌉·4 = 84 ✓; §15.4 example — 16 segments, last 16,960 entries, region 20,000,064, entry 999,999 at segment-relative 339,180, segment 15 at [19,660,800, 20,000,000), full segment 1.25 MiB ✓; §11.4 example s = 10, in-tile ordinal 11,452, planar disk ordinal 74, and §15.4's entry 74 at [1,480, 1,500) ✓; §14.2 examples (18/[15,18); 12/10–11; 30/[25,30)) ✓; §14.3 example bytes `55 01` / `55 FD` ✓; §14.5 example 32 bytes ✓; §17.3 shuffle example ✓; §20.3 example 32·20+4 = 644 ✓; §21.9 Note 2³²·4/2¹⁶ = 256 KiB, 4 MiB at 2³⁶ ✓; §9.2 second Note F+68 → F+128 ✓; Appendix A slack 44 bytes and the 112-byte window ✓; §12.1 bfloat16 1.0 = 0x3F80 ✓.

Register arithmetic: rows F = 35 (F1–F36 less struck F11), L = 49, T = 26, R = 10 — total 120, matching §21.2/§21.3/§21.4/§21.5 headings and §21.8. Instances (semicolons + 1 per cell; a `—` cell = 1): F 56, L 116, T 55, R 50 — total 277, matching §21.8. Verifier-detected rows: F7, F25, F26, F27, F28, F33, F36, L18, L25, L40, L41, L42, L46, L47, L48, L49, T2, T4, T5, T26 (20 rows). §20.5's parenthetical list of the "other seven spaces" (L31, L33, L34, L36, L43, L45, R1) is exactly one row per non-record-type space of §10.2's eight-row table ✓. [R-CNF-13]'s "[R-CNT-06] states nine" — rows governed by CNT-06 are F8, F9, F10, F12, F13, F14, F15, F16, F17 = nine ✓, of which F8 and F14 reach ✓. §21.2's "F8, F14, F6 and both of F1's instances … and no other row" — I checked every §21.2 row against [R-CNT-24]'s four fixed invariants (front block constant; magic at F−64; version fields at F−56; CRC at F−4 over [F−64, F−4)) and found no other ✓.

## 3. The certification procedure (as I would implement it)

Verdict vocabulary (§2.3 [R-CNF-11]): **conforming**, **nonconforming**, **cannot establish**. Per-item report vocabulary: a *violation* (row + governing rule + scope), an *unchecked requirement* (requirement id + capability/resource ground), an *unexamined* scope, an *advisory* (SHOULD deviation, §2.4 [R-CNF-12] — reported where observed, not hunted), an *ignored-record report* ([R-MTA-10]: scope, encoding value, stored extent length), the *slack total* (exact or partial, [R-CNT-21]), and where the file is torn, the recovery diagnosis ([R-LIF-06]: candidate settled on and count rejected).

Verdict rule: nonconforming iff at least one violation established (priority over everything, "however many requirements it was unable to check"); else cannot establish iff at least one unchecked requirement on a capability/resource ground; else conforming. A verifier MAY stop at the first violation; then every scope not examined is reported *unexamined*. *Unexamined* and the per-requirement unchecked report never move the verdict.

Ordered checks:

1. **Size and front block.** Obtain transport-authoritative F ([R-CNT-10]). F < 128 → F5 (reject-file) — but only assessed for a file declaring major 1 (§2.3 Note). Read [0,16), compare by equality: F1-front / F6. A verifier holds no residency exemption (§2.3, F6 cell, App. H).
2. **Trailer** in §6.2's fixed order: magic (F8 / F1-trailer) → trailer CRC (F14) → version gate: major = 0 → F18; major ≠ 1 → every *reaching* condition (F1 both instances, F6, F8, F14) is applied and its failure is nonconforming ([R-CNF-13]); if all pass, the file is *cannot establish* and every non-reaching requirement is reported unchecked on the capability ground. Then flags incompat lane (F19), F = file size (F17), F mod 64 (F13), dir_offset ≥ 16 (F9), dir_length ≥ 4 (F16), dir_offset ≤ 2⁶³−1 etc. (F2), sum (F3, F10), file_id ≠ 0 (F12), reserved zero (F15). Any failure → reject-file; no live state established; **no slack total is owed** ([R-CNT-21]).
3. **Directory.** Fetch, verify terminal CRC (F20). Parse records (F29, F24), multiplicity (F34), unknown types: reserved-range → F36 (and F35 if MU=1); experimental MU=1 → *cannot establish* ground (§21.6, [R-CNF-11]); experimental MU=0 → ignored, preserved. Per-record: reserved flag bits (F26/L47), MU=1∧PE=0 (F25/L46), registered-type flag mismatch (F28/L49), extent slot rules (F30–F32, L15–L17), user-metadata framing (F21–F23, L10–L12). Layer names (L3, L5, L6, F4 over raw bytes).
4. **Per layer** (§19.3 in full — every item there is decidable from the directory and F): L1, L2, L4, L7–L9, L13, L14, L19–L36, L39, L43–L45.
5. **Index chain per layer**: fetch region; crc_of_crc_array (L37), every segment CRC (L38) — the all-sentinel constant is never matched, always computed ([R-IDX-05]). Classify every entry per §15.3: T6–T12 (structural), sentinel, or well-formed.
6. **Coverage walk** ([R-LIF-08], see §4 below): claimants = directory, each record's extent, each layer's index region (once, as its record's extent), each well-formed non-sentinel entry's extent; check each within [16, F−64), pairwise disjoint (L18 / F33), none in [dir_end, F−64) (F7).
7. **Per stored tile**: fetch, entry crc (T1); codec-1 length (T14) — decidable before the fetch; decode (T13, T15–T25); size (T3); content: padding fill (T4), pad bits (T5), interleaved bool bytes (T2), which together witness T26. Every stored tile is decoded (§9.7); decline on resource grounds only above the 256 MiB / 8 MiB guarantees → unchecked [R-SER-05]/[R-SER-08] for that tile, *cannot establish* if nothing else fails.
8. **Per user-metadata record**: extent CRC (R2); encoding 0/reserved → R1 (violation); experimental → no content rule, report the record ([R-MTA-10]), certification unaffected; assigned → decode within a bound ≥ 16 MiB and window ≥ 8 MiB (else unchecked [R-MTA-04]/[R-MTA-05] for that document → cannot establish), R3/R4 frame constraints, R5–R10 content, F27/L48 member order.
9. **Alignment and slab invariants** (L40–L42) from the classified entries and F alone.
10. **Report**: verdict, findings, unchecked list, unexamined list, advisories, ignored records, slack total (exact or partial with the stopping scope/violation).

Every step above cites a rule that fixes it; the document sufficed for the ordering except where noted in the findings (the *composition* of a partial total after a file-scope rejection, finding verifier-03).

## 4. The coverage walk — concrete arithmetic

I built a rank-1 layer `sst` from §7.4's example (extent 100, tile extent 32, one interleaved float32 channel `temp`, fill 0x7FC00000, codec 1, filter 1, no alignment or slab), so every tile's decoded size is 32·4 = 128 bytes, grid count 4, entry_count 4, index region 84 bytes, layer record 24+81 = 105 bytes, directory 109 bytes. Tile 3 is an edge tile: 4 real positions and 28 padding positions, each padding position holding the fill bytes `00 00 C0 7F` ([R-SER-05]).

**Generation 1 (creator)** — stores tiles 0 and 3; tiles 1 and 2 sentinel.

| Range | Claimant |
|---|---|
| [0,16) | front block |
| [16,144) | tile 0 (crc F8118D31) |
| [144,272) | tile 3 (crc 1909AA1A) |
| [272,356) | index region (crc_of_crc_array 3F5D9738) |
| [356,465) | directory (dir CRC C4B3C12A) |
| [465,512) | pre-trailer pad — slack, 47 bytes |
| [512,576) | trailer (CRC 9A168B3F), F = 576 |

Live state = 16+128+128+84+109+64 = 529 bytes; slack = 576 − 529 = **47**, exact; every one of the 576 bytes is either claimed by exactly one claimant or slack — there is no third class, which is what §5.2's Note says ("belongs to no class" describes nothing). Verdict on my own bytes: conforming.

**Generation 2 (append tile 1)** — writing begins at 576: tile 1 [576,704), new index [704,788) (crc_of_crc_array DEC9B769), directory [788,897), pad 63, trailer [960,1024), F = 1024. Live: 16 + 3·128 + 84 + 109 + 64 = 657; slack = 1024 − 657 = **367** = old index 84 + old dir 109 + old pad 47 + old trailer 64 + new pad 63 ✓. Verdict: conforming. The old index region and old trailer are inside the file, unclaimed and uninterpreted — a §9.6 probe at o = 512 would find a *candidate* (magic ✓, CRC ✓, committed_file_length = 576 = o+64 ✓) that is not the live state; §9.6 says no verdict turns on it.

**Generation 3 (update: supersede tile 0)** — new tile 0 [1024,1152), index [1152,1236), directory [1236,1345), pad 63, trailer [1408,1472), F = 1472. Live still 657 bytes; slack = **815**. Verdict: conforming.

**Generation 4 (compaction)** — a new file, fresh file_id: front, tiles 0′,1,3 at [16,400), index [400,484), directory [484,593), pad 47, trailer [640,704), F = 704. Slack **47**. Every tile's bytes and entry crc unchanged ([R-WRT-07]); entry offsets re-pointed; segment CRC recomputed (crc_of_crc_array 19ED25D4 ≠ gen 3's F1A6A3BA, as [R-WRT-07] says it may). Verdict: conforming; reference array bit-identical to gen 3's.

**A walk that does not complete.** Two-layer file: layer A as gen 1 (tiles [16,144), [144,272), index [272,356)); layer B with tiles at [356,484) and [420,548) — a 64-byte intra-layer overlap — and index [548,632); directory of two layer records 2·105+4 = 214 bytes at [632,846); pad 50; trailer [896,960); F = 960. The walk establishes L18 on B. Per [R-CNT-21], B's claimants — including the two already enumerated — are discarded with the layer. Partial total = 960 − (16 + 256 + 84 + 214 + 64) = **326**, reported "partial; stopped by L18 in layer B". The file's true unclaimed count, if one took B's union [356,548) ∪ [548,632) = 276 bytes as claimed, would be 50; 326 ≥ 50, so the partial is the upper bound the rule promises. Verdict: nonconforming (L18 established).

Which bytes are certified and which are counted-but-unconstrained: certified = the front block by equality, the trailer/directory/index/tiles/user-metadata extents by their checksums, and the decoded content of every stored tile against §14.5 and [R-SER-08]; counted-but-unconstrained = every slack byte, plus two classes of *live* bytes a certificate covers uninspected — the extent of a record of an unassigned type (no checksum, opaque, §8.1) and the document bytes of a user-metadata record under an experimental encoding (checksummed but content-free, [R-MTA-10]). Can a byte be neither claimed nor slack? No — slack is defined as the complement ([R-LIF-08]).

## 5. Extent overlap, alignment, slab — adversarial layouts

Overlap cases I checked against §7.2/§15.3/§21: two tiles of one layer overlapping → L18 (reject-layer); a tile of A inside A's own index region → L18; A's sub-record extent inside A's index region → L18 ("any intra-layer overlap"); a tile of B inside A's index region → F33; a tile overlapping the directory region → F33 (directory is in F33's instance list); two layer records whose extent slots address the *same* index region → F33 (byte-identical entries do not excuse it); a top-level user-metadata extent overlapping a layer's sub-record extent → F33 ("touching another scope's structures"); a live tile in [dir_end, F−64) overlapping nothing → F7 alone. A tile with a structural defect (T8 offset 5) contributes no extent and cannot overlap; one whose bytes fail crc keeps its extent and can (T1 + L18). All determinate.

Alignment, A = 512: tiles at 512, 1024 pass; a well-formed entry at offset 17 (≥ 16, in bounds) fails L40; an entry at offset 5 is T8 and is *not* L40, since §15.3's verifier rows bind over well-formed entries only.

Slab, S = 2, A_slab = 1024, interleaved N = 4: runs [0,2), [2,4). Run 0: tile 0 at 1024 (len 100), tile 1 at 1124 (len 50) — packed ✓. Run 1: tile 2 at 2048 (len 100), tile 3 at 2200 → gap → L41; at 2100 → overlap → L41 (and L18); tile 2 at 2000 → L42. Tile 0 sentinel → tile 1 is the run's first stored tile and must be 1024-aligned. Tile 1 structurally malformed → transparent, run 0 reduces to tile 0. Tile 1 with a crc failure → not transparent; its offset and length enter the packing relation (§16.2, L41). S = 1 makes every stored tile A_slab-aligned and contiguity vacuous; A_slab = 1 is contiguity-only. A run with no stored tiles imposes nothing. All decidable from the classified entries and F without a payload fetch, as §16.2 claims.

## 6. Checksum obligations

Every live structure and the checksum covering it, from §8.1: front block (equality); trailer (its own [60,64) over [0,60)); directory (terminal 4 over the record sequence, which contains every layer record's inline payload and therefore crc_of_crc_array); index region (segment CRCs over entries, the array covered by crc_of_crc_array); stored tile (entry crc, entry covered by its segment); user-metadata extent (terminal 4). The single live structure covered by no checksum is the extent of a record of a type this specification has not assigned — §4.5, §8.1 and §22.3 all say so. Interior checksum fields are each comparison-verified and covered by exactly one further checksum ✓ (I traced each: segment array ← crc_of_crc_array ← directory CRC; entry crc ← segment CRC; crc_of_crc_array ← directory CRC).

## 7. Decoded-content obligations

Must decode: every stored tile (§9.7), every user-metadata document under an assigned encoding (R3–R10, F27/L48). Must compare against: padding positions vs. recorded fill bytes/byte/bit (T4), pad bits vs. fill bit (T5), interleaved bool real-position bytes ∈ {00, 01} (T2), decoded length vs. declared decoded size (T3), zstd frame header fields vs. declared decoded size (T21, T22), document content-size vs. decoded document length (R4). May skip: sentinel tiles (nothing to decode), the document under an experimental encoding (no rule; report it), SHOULD-level properties (not hunted), the shape/scope of standardized keys (§21.6 non-violations), and slack. Structurally-malformed entries are recorded (T6–T12) and their nominal bytes fall to slack.

## 8. Multi-generation verdict trace

| Generation | Operation | Verdict | Slack | Notes |
|---|---|---|---|---|
| 1 | create (tiles 0, 3) | conforming | 47 exact | — |
| 2 | append tile 1 | conforming | 367 exact | superseded trailer at 512 is a §9.6 candidate; no verdict turns on it |
| 3 | supersede tile 0 | conforming | 815 exact | old tile 0 bytes remain readable in slack (§23.1) |
| 4 | compact | conforming | 47 exact | new file_id; reference array identical |
| 2-layer variant | B's tiles overlap | nonconforming (L18) | partial 326, "stopped by L18 in B" | upper bound on true slack |

## 9. Findings

### verifier-01 — AMBIGUITY (not byte-level). "An encoding this specification does not assign" is used in two senses, and in §2.3's sense the sentence is false for encoding 0 and the reserved range.

Location: §2.3 [R-CNF-11]; §17.4 [R-COD-11]'s closing sentence; §9.7 [R-LIF-08]; §22.3 [R-SEC-04]; against §21.5's intro, R3, and [R-MTA-03].

§2.3 (lines 223–226): "A user-metadata document under an encoding this specification does not assign is not such a ground: no content rule attaches there, so nothing is left unchecked, and certification is unaffected (`[R-MTA-10]`, §21.6)."

§17.4 (lines 2567–2570): "The metadata-encoding space alone differs: an unassigned document encoding in a conforming file is not a violation (§21.6), no document rule attaches to its extent, and certification is unaffected (`[R-MTA-10]`, §18.2)."

§21.5 intro (line 3822): "Encoding 0 and a reserved-range value are unassigned too, and R1 registers both as violations: what `[R-MTA-10]` withdraws is the document's content rules, never the encoding byte's own value set (`[R-MTA-03]`)." §18.2 [R-MTA-03]: "An encoding a reader does not implement is therefore one this specification does not assign, and is ignore-record".

Readings. (a) "does not assign / unassigned" = {0, 3–0x7F, ≥ 0x80}, which is the sense §21.5, R3 and [R-MTA-03] fix expressly. Under it, §2.3's "certification is unaffected" and §17.4's "not a violation" are false for encoding 0 and reserved values, which R1 registers and which bar certification. (b) The four sentences mean the experimental range only — the sense §21.6's row and Appendix H use ("a user-metadata record at an experimental-range encoding is no violation and no bar … encoding 0 and the reserved range stay violations (R1)"). I picked (b) because [R-MTA-03] fixes 0 as invalid and R1 is a register row whose governing rules ([R-CNT-25], [R-MTA-03]) agree, and a verifier inherits every reader obligation, so no competent verifier certifies over encoding 0. What an implementer does wrong without it: reading §2.3 or §17.4 alone, treats a reserved-range encoding byte as a report-and-certify case. The verdict does not fork: [R-MTA-03]'s value set and R1 decide it under both readings. §21.5's sentence was written precisely to close reading (a)'s confusion; §2.3, §9.7, §17.4 and §22.3 are the neighbours still using the word in the other sense.

### verifier-02 — CONTRADICTION (not byte-level). §18.2's Note says a resource decline under [R-ERR-04] for an oversized document is at the whole file only; [R-ERR-04] and §18.2's own body name the record as a scope.

§18.2 Note (lines 2688–2692): "A reader that proceeds takes ignore-record for that record; a reader that instead declines on resource grounds under `[R-ERR-04]` does so at the whole file, a document having no declared size and so no narrower scope whose stated or derived quantities that rule can measure, its decoded size being neither."

§21.9 [R-ERR-04] (lines 3997–4001): "a reader MAY decline it — at the whole file, or at the narrowest scope whose stated or derived quantities exceed what it can serve: a layer, a tile, or the record carrying a user-metadata document, as §18.2 assigns."

§18.2 body, window case: "a frame declaring more than the reader admits is ignore-record on that ground — the reader's capability, not a failure to decode within the meaning of R3, and no violation: the file exceeds a §21.9 guarantee and so remains conforming while the reader MAY decline it (`[R-ERR-04]`)."

The Note is labelled and non-normative, but it glosses [R-ERR-04] and disagrees with it on whether the record is an [R-ERR-04] scope; the normative body treats record-scope ignore-record as the [R-ERR-04] decline for the window bound while the Note denies it for the size bound. Not byte-level: under either text the permitted behaviours are the same two — ignore the record, or refuse the file — and only the label the report carries ("resource limit" vs. "loss") differs. Cost: an implementer of a reader's reporting path cannot tell which label §21.9's "MUST be reported as a resource limit" attaches to the record-scope case.

### verifier-03 — AMBIGUITY (not byte-level). [R-CNT-21] fixes what a partial total contains after a walk-established *layer* rejection, but not after a walk-established *file* rejection (F33, F7) or a post-trailer reject-file (F20, F29 …).

§5.2 [R-CNT-21] (lines 710–724): "a rejected layer's claimants are not enumerated, whether or not the rejection impeded reading them — and where the rejection is one the walk itself established, L18's overlap or L40 through L42's placement among them, the claimants it had already enumerated are discarded with the layer, since the total is a claim about a live state one of whose layers is not usable … A partial total is F less the bytes claimed by the claimants the walk did enumerate — an upper bound on the file's true slack, never an under-count — and a verifier reporting one MUST say which scope or violation stopped the walk."

The rule owes a partial total whenever a live trailer was established and the walk did not complete, and it only exempts the pre-trailer case ("there is no F and no live state to walk"). For F33 (cross-layer overlap the walk itself established) or F7, two readings: (a) by the stated rationale — the total is a claim about a live state that is now wholly unusable — discard every enumerated claimant except the front block and trailer, reporting F − 80; (b) "F less the bytes claimed by the claimants the walk did enumerate" literally, keeping everything enumerated (as a set union, so still an upper bound). I implemented (b), since the discard clause names layers only. The two verifiers report different partial totals for the same file; both satisfy "upper bound … naming what stopped the walk". Not byte-level — a reporting figure, not a verdict or an emitted byte. Rejected sub-candidate: "never an under-count" would fail if a verifier subtracted *lengths* rather than the *union of bytes* after an overlap; "the bytes claimed by" reads naturally as the set, so I did not file that separately.

### verifier-04 — OBSERVATION (not byte-level). [R-CNF-02]'s closed list of "the cases this text states" omits §9.2's barrier declaration, which uses the same express form.

§2.3 (lines 170–176): "A writer obligation whose violation this specification expressly declares not to be a file-conformance violation binds the actor in the same way; §6.3's flags = 0 against a set ignore-lane bit and §6.2's pre-trailer gap longer than `[R-LIF-02]` step 5's pad are the cases this text states, and each is declared where it arises rather than enumerated here."

§9.2: "Steps 4 and 6 bind a writer's **conduct** rather than its output, and are declared so here on the model `[R-CNF-02]` states … A writer that omits a barrier violates this requirement, and the file it produces is not nonconforming on that account."

§9.2 both places the barriers under [R-CNF-02]'s first (conduct) category and, in its last sentence, "expressly declares" the violation not to make the file nonconforming — the second category's defining form — so the count of two is exceeded by the text's own third instance. Both categories "bind the actor in the same way", so nothing turns on it; consequence-free, and filed only because it is a closed count the document itself falsifies.

## 10. Rejected candidates (opened and closed)

- [R-CNF-03]'s acceptance exemption "carrying no record of a type it does not implement with MU = 1" vs [R-CNT-18]'s "MUST NOT reject the file for it" on a sub-record: closed by [R-CNT-18] being a MUST NOT that governs conduct whether or not the acceptance duty runs; §21.6's "the qualifier is load-bearing" confirms.
- §20.3's §14 bar barring "superseding every tile of a layer and re-declaring it" although the resulting bytes are indistinguishable from a conforming file: closed by [R-CNF-02] (pure predicate on bytes) plus §21.7 ("Being unwitnessed bears on detection and not on permission") — a creator with free slack content can emit the identical bytes, so the emittable set does not move.
- A compactor that "detects" F36 (reserved-range MU=0 type) vs one that does not: closed by the disputed output being nonconforming, and by §20.5's express "bounds how far a compactor goes looking, not what it owes on what … has already put in front of it".
- Whether §9.6's "whole-file re-verification" is §8's checksum chain or full certification: closed by the caution's own citation "re-verified as a whole file (§8)" and by "no verdict turns on the probe".
- Whether a user-metadata extent failing R2 remains a claimant: closed by §9.7 naming claimants by reachability ("each record's extent") and treating the checksum as a separate check, the same structure that keeps a T1 tile's extent.
- Whether a verifier meeting an experimental MU=1 top-level record may stop and report *cannot establish* without checking layers: closed by §2.3's "checks every file-level requirement" and §19.3's "All are decidable from the resident directory and F" — layer rows remain checkable, so the verdict is fixed by whether any is violated.
- [R-COD-11]'s cannot-establish ground being vacuous for a conforming major-1 verifier (every assigned codec is core; any other value is L43/L45): true, but dead text, not a defect.
- §21.9's "The first five rows range over declarations" for a zero-layer file: holds (0 ≤ 65,536).
- L40 vs T8 on an entry with offset 5 and A = 512: closed by §15.3's "verifier rows … bind over well-formed entries' extents only".
- Appendix G item 5's "exactly where" for filter identity: verified — the transpose of an s×n byte matrix is the identity iff s = 1 or n = 1.

## 11. Sweeps run (hit counts)

Line-oriented, over spec/tarn.md: "cannot establish" 7; "unexamined" 4; "partial" 11; "slack total" 5; "certif" 44; "verifier MUST" 14; "MUST NOT certify" 3; "conduct" 6; "not nonconforming" 1; "advisory" 5 (3 shown by grep -n, others wrapped); "first stored" 4; "0x7E000000" 4; "16 MiB" 7; "8 MiB" 5; "pre-trailer" 12; "structural ground" 2; "discarded" 1; "upper bound" 3; "never an under-count" 1; "the whole of the test" 1; "does not reach" 5; "declines" 9; "resource ground" 5; "capability" 10; "Detector" 17; "certification" 26; "does not assign|unassigned|certification is unaffected" 15 lines; "narrowest scope|at the whole file|record carrying a user" 3; "sentinel" 54 and "reject-layer" 21 as presence checks. Whitespace-normalised: "are the cases this text states" 1 (line-oriented grep gave 0 — wraps); "certification is unaffected" 3; "does so at the whole file" 1; "never an under-count" 1; "discarded with the layer" 1; "an unassigned document encoding in a conforming file is not a violation" 1; "Encoding 0 and a reserved-range value are unassigned too" 1; "no violation there to look for" 1; "reject-file bars every commit" 1. Blockquote label census: 93 labelled openers, 1 unlabelled (line 2147).

## 12. Confidence

High that an implementation built from this text alone interoperates on every verdict: I could not construct a file on which two competent verifiers reading this document would return different verdicts, and every byte-level suspicion I opened closed on a sentence in the document rather than on reasoning I supplied. The four findings are report-content and wording defects; none moves the emittable set or an accept/reject/certify verdict.
