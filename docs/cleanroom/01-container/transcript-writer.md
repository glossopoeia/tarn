# Conforming WRITER and APPENDER — implementation walkthrough

Source of truth: `/Users/robertkleffner/Documents/GitHub/tarn/spec/tarn.md` (working draft). All citations below are to that document. Sections 12, 13, 14, 15, 16, 17, 18, 19, 20, 21 are *[Reserved]*; where a byte I must emit is determined only by a Reserved section, I say so explicitly and record it in the consolidated list.

## 0. Preliminary geometry decision that shapes everything

The task says "zero stored tiles (all sentinel)" — but *stored* and *addressed* are distinct (§3.1: every tile is addressed; a tile is stored iff its index entry is not the sentinel). With extent E=100, tile extent T=256: G = ⌈100/256⌉ = 1 (§11.2, [R-GEO-03]; §11.1 permits T > E — "the grid is then a single padded tile"). So N = 1 spatial tile; interleaved layout → addressed-tile count = N = 1. Therefore `entry_count = 1`, and the layer **must** carry a real tile-index region: under index_encoding 1, extent_length = entry_count × 20 + ⌈entry_count/2¹⁶⌉ × 4 = 20 + 4 = **24 bytes** ([R-CNT-17]). The "(0,0) extent slot" shortcut exists only for *zero addressed tiles* (§7.4), which we do not have.

## 1. Creation — complete byte layout

Procedure (§9.2, [R-LIF-02] creation variant): emit front signature block, then perform commit steps 2–6 starting at offset 16, generation 1. Structure order within the generation: step-2 structures first, then directory, pre-trailer pad, trailer last (§5.1, [R-CNT-01]). With A=0, S=0 there is no lawful padding class between structures ([R-CNT-02], [R-CNT-03]; declared padding is only alignment gaps of aligned/slab layers plus the pre-trailer pad), so everything packs exactly.

Field-value justifications:
- layout = 1 (interleaved) — §7.4 table.
- linearization = 1 — the only value writers may emit ([R-GEO-05]).
- filter = 1 = none — §7.4 table gives the value set directly.
- codec — **not determinable**: §7.4 says only "§17 (0 invalid)", and §17 is Reserved; no nonzero codec value is assigned anywhere in the text, yet a reserved/unassigned value is reject-layer ([R-CNT-23]). I emit 1 by pattern (every other enum here assigns 1 as first/none: layout, linearization, filter, index_encoding, metadata encoding §7.1) — recorded as Ambiguity 1. Note codec never touches bytes here (no stored tiles), but the field must still hold an assigned value.
- channel type — **not determinable**: "type per §12" (§7.4) and §12 is Reserved. I emit 1 and assume element size 1 byte — recorded as Ambiguity 2. Fill length must equal the type's element size ([R-CNT-23]) → 1-byte fill; fill *content* is governed by Reserved §13; I emit 0x00 (Ambiguity 6).
- A = 0, S = 0, A_slab = 0 (A_slab MUST be 0 when S = 0, [R-CNT-23]); [R-CNT-16] not triggered.
- index_encoding = 1 = raw-segmented (§7.4).
- Record flags for type 0x0001: exactly MU=1, PE=1 = 0x0003 ([R-CNT-22], §7.3); reserved bits zero ([R-CNT-12]).
- Trailer flags = 0 ([R-CNT-08]); file_id nonzero, SHOULD be cryptographically random (§9.3); generation = 1.

**Byte map (F = 256):**

```
[0,16)    Front signature block (§6.1) [R-CNT-04]
  0:  89 54 41 52 4E 0D 0A 1A
  8:  00 00 00 00 00 00 00 00

[16,40)   Tile-index region, layer "t" (24 bytes; [R-CNT-17])
  16: 20 bytes — one index entry = the sentinel.
      BIT PATTERN UNDETERMINED: entry layout and sentinel encoding are §15 [Reserved].
  36: 4 bytes — segment CRC array (1 segment: ⌈1/2^16⌉=1). Per §8.1 it covers
      "index entries, per segment"; I place it after the entries and compute
      CRC-32C over bytes [16,36). PLACEMENT/COVERAGE DETAIL UNDETERMINED (§15 Reserved).

[40,141)  Directory region, dir_length = 101 (§7.1)
  Layer record header (§7.2, 24 bytes):
  40:  01 00                    u16 type = 0x0001 (layer, §7.3)
  42:  03 00                    u16 flags MU=1,PE=1 [R-CNT-22]
  44:  49 00 00 00              u32 inline_length = 73
  48:  10 00 00 00 00 00 00 00  u64 extent_offset = 16
  56:  18 00 00 00 00 00 00 00  u64 extent_length = 24
  Inline payload (§7.4, 73 bytes):
  64:  01 74                    name "t" (u8 len + bytes, §4.6)
  66:  01                       u8 layout = interleaved
  67:  01 00                    u16 linearization = 1 [R-GEO-05]
  69:  01 00                    u16 codec — UNDETERMINED (§17 Reserved); 1 chosen
  71:  01 00                    u16 filter = 1 none (§7.4)
  73:  00 x8                    u64 A = 0
  81:  00 x8                    u64 S = 0
  89:  00 x8                    u64 A_slab = 0 [R-CNT-23]
  97:  01                       u8 rank = 1
  98:  01 00                    u16 channel count = 1
  100: 01 78                    dim name "x"
  102: 64 00 00 00 00 00 00 00  u64 extent = 100
  110: 00 01 00 00 00 00 00 00  u64 tile extent = 256
  118: 01 76                    channel name "v"
  120: 01 00                    u16 type — UNDETERMINED (§12 Reserved); 1 chosen
  122: 01 00                    fill: len 1 (= element size, [R-CNT-23]); value 0x00
                                — length rule known, content rule §13 Reserved
  124: 01                       u8 index_encoding = 1
  125: 01 00 00 00 00 00 00 00  u64 entry_count = 1 (addressed-tile count, [R-CNT-17])
  133: ?? ?? ?? ??              u32 crc_of_crc_array = CRC-32C over bytes [36,40)
                                — numerically undetermined (depends on sentinel bytes)
  (no sub-records: zero residue, [R-CNT-18])
  137: ?? ?? ?? ??              u32 directory CRC over [40,137) (§7.1 [R-CNT-11])
                                — undetermined (depends on the bytes above)

[141,192) Pre-trailer pad: 51 zero bytes (51 < 64, [R-CNT-05]; zero per [R-CNT-03])

[192,256) Trailer (§6.2):
  192: 8A 4E 52 41 54 0D 0A 1A  magic
  200: 01 00                    u16 version_major = 1
  202: 00 00                    u16 version_minor — UNDETERMINED by the text
                                (valid values "any"; no writer rule); 0 chosen
  204: 00 00 00 00              u32 flags = 0 [R-CNT-08]
  208: 01 00 00 00 00 00 00 00  u64 generation = 1
  216: 28 00 00 00 00 00 00 00  u64 dir_offset = 40
  224: 65 00 00 00 00 00 00 00  u64 dir_length = 101
  232: 00 01 00 00 00 00 00 00  u64 committed_file_length = 256 (multiple of 64)
  240: (nonzero, writer-chosen)  u64 file_id — nondeterministic by design (§9.3)
  248: 00 00 00 00              reserved
  252: ?? ?? ?? ??              u32 CRC-32C over [192,252)
```

Cross-checks: dir_offset 40 ≥ 16; dir_length 101 ≥ 4; 40+101 = 141 ≤ F−64 = 192; extent [16,40) within [16, F−64] ([R-CNT-13]); 16+24+101+51+64 = 256 = F, 256 mod 64 = 0 ([R-CNT-01]); dir_length+pad+64 = 216 ≤ 65,536 (SHOULD, [R-CNT-09]). Undetermined bytes: the 20 sentinel bytes, the segment CRC, crc_of_crc_array, the directory CRC (transitively), codec, channel type, fill (size/content), version_minor, file_id, trailer CRC (transitively).

Durability: barrier after step 3 (front block + index + directory), then pad+trailer, then barrier ([R-LIF-02] steps 4 and 6).

## 2. Append — second layer ("u", same shape as "t"; name must differ, [R-ENC-15])

**Open phase (the appender is a reader first — §4.2, [R-CNT-08]):**
1. Verify the front signature block by byte equality (local reader obligation, [R-CNT-04]).
2. Establish F: validate the trailer in the final 64 bytes of the *physical* file ([R-LIF-04]) in [R-CNT-06]'s order: magic → trailer CRC → version gate (§6.3; major must be 1, no unknown incompat-lane flags) → then committed_file_length = physical size and multiple of 64, dir_offset ≥ 16, dir_length ≥ 4, bounds, generation ≥ 1, file_id ≠ 0, reserved zero. Here F = 256, physical = 256, so no truncate/overwrite branch.
3. Read [40,141); verify the directory CRC before any other use ([R-CNT-11], [R-ENC-10]); parse records. The layer record for "t" will be re-emitted (commit step 3 re-emits every retained record; §9.2). Note the appender need not decode "t"'s tiles or verify its index chain — it acts on no field those links cover ([R-CNT-20]; §3.3 Note makes this independence load-bearing) — see Ambiguity 8.

**Commit phase ([R-LIF-02]), bytes in write order:**

```
Step 1  Begin writing at exactly F = 256.
Step 2  [256,280)  Tile-index region for "u": 20-byte sentinel entry (§15 Reserved,
                   same undetermined pattern) + 4-byte segment CRC over [256,276).
Step 3  [280,478)  New COMPLETE directory (never a delta — §3.1), dir_length = 198:
        [280,377)  layer record "t", re-emitted byte-identical to bytes [40,137)
                   of gen 1 — extent slot still (16,24): retained structures stay
                   where gen 1 put them (§9.7 Note). Byte-identity is my reading of
                   "re-emitting every retained record per §20's preservation rules"
                   + preserve-verbatim (§2.4); §20 is Reserved — Ambiguity 5.
        [377,474)  layer record "u": identical to "t"'s record except
                   name byte 74→75 ("u") at inline offset 0, extent_offset =
                   00 01 00 00 00 00 00 00 (256), crc_of_crc_array over [276,280).
        [474,478)  directory CRC-32C over [280,474).
Step 4  BARRIER #1 (fdatasync or platform equivalent): makes [256,478) durable,
        ordered against power loss.
Step 5  [478,512)  34 zero pad bytes ([R-CNT-03]; 34 < 64 [R-CNT-05]).
        [512,576)  Generation-2 trailer.
Step 6  BARRIER #2: makes the trailer durable. Physical length now 576
        = committed_file_length ([R-LIF-04] end condition).
```

Record order "t" then "u" is a free choice ([R-CNT-14]: order carries no meaning).

**Generation-2 trailer contents:**

| Offset in trailer | Field | Value |
|---|---|---|
| 0 | magic | `8A 4E 52 41 54 0D 0A 1A` |
| 8 | version_major | 1 |
| 10 | version_minor | carried forward (0) — no rule fixes this; Ambiguity 4 |
| 12 | flags | 0 — unknown ignore-lane bits MUST be copied forward, never cleared ([R-CNT-08]); none are set |
| 16 | generation | 2 — exactly prior + 1 ([R-LIF-02] step 5, [R-LIF-03]) |
| 24 | dir_offset | 280 |
| 32 | dir_length | 198 |
| 40 | committed_file_length | 576 (multiple of 64) |
| 48 | file_id | identical to gen 1's — "the file_id chosen at creation" rides in every commit's trailer (§9.3); a new file_id happens only via compaction/rewrite ([R-LIF-01], §20) |
| 56 | reserved | zero |
| 60 | trailer CRC | CRC-32C over trailer bytes [0,60) |

Post-commit coverage: gen 2 claims [256,576) exactly (index, directory, pad, trailer — §9.7(c)); gen 1's tile-index region [16,40) remains live (reachable via "t"'s extent slot), while gen 1's directory, pad, and trailer become superseded structures — dead space readers must not interpret on the default path ([R-CNT-21]), reachable only to verifiers/recovery via §9.6/§9.7.

## 3. Torn-append recovery

Crash mid-gen-2-commit; a new writer process opens to append.

**Obliged steps:**
1. Verify the front block ([R-CNT-04]).
2. Attempt to establish F by validating the final 64 physical bytes per §6.2 ([R-LIF-04]). Because [R-CNT-06] requires committed_file_length = file size, a stale-but-valid trailer that is no longer at EOF can never validate here: if the crash left any partial gen-2 bytes after offset 256, the final 64 bytes are torn garbage and validation fails.
3. On failure the file is torn: the writer **MUST NOT append**, and **MUST NOT** treat backward scanning as an implicit step of opening for append ([R-LIF-04]); on the read side, a reader likewise MUST report torn/invalid and MUST NOT scan backward ([R-LIF-05]).
4. Recovery is a *deliberate* operation (§9.6, [R-LIF-06]): probe backward at 64-aligned offsets o for the trailer magic; a candidate is valid only if its trailer CRC verifies **and** committed_file_length = o + 64. The nearest-to-end valid candidate is the last committed state (here o = 192, F = 256). Truncating to it recovers the file.
5. The recovery output MUST be re-verified as a whole file (§8) before being trusted — a tile payload can deliberately mimic a valid trailer ([R-LIF-06]). (No stored tiles exist in this file, but the rule is unconditional.)
6. Only "once F is established (directly, or by recovery whose output has been re-verified)" may the writer append; if the physical file is still longer than F it MUST either truncate to F before commit step 1, or overwrite from F and truncate to the new committed_file_length no later than step 6 — bytes beyond a committed length never survive into any committed state ([R-LIF-04]). Then re-run the §2 append verbatim; the retried commit again carries generation 2.
7. Edge case: if the crash left a fully written, CRC-valid gen-2 trailer at physical EOF but the step-4 barrier had not completed and directory bytes are torn, trailer validation succeeds but the directory CRC fails → reject-file ([R-CNT-11]); an updater is a reader first and rejects before modifying anything ([R-CNT-08]). Recovery per step 4 then truncates to gen 1. This is exactly §9.2's Note: weak barriers degrade "torn commits are invisible" to "torn commits are detected", never silent corruption.

**Forbidden:** appending past an unvalidated trailer; implicit recovery on the append path ([R-LIF-04]); modifying any byte of [0, F) ([R-LIF-01]); heuristic repair or inferring undefined values ([R-CNF-04]); trusting an un-re-verified recovery result ([R-LIF-06]); acting on any integer before its covering checksum verifies ([R-ENC-05]). Also note: truncation to an earlier commit is in-format indistinguishable from that earlier version — rollback detection needs out-of-band state ([R-LIF-06]) — and single-writer exclusion is the deployment's job (§9.5).

## 4. Legitimate byte divergence between two conforming writers

Licensed globally by [R-CNF-05]: "this specification does not promise canonical bytes." Taking "same logical content" = same reference arrays (§3.2), names, and metadata:

Even with identical declared schema:
1. **file_id** — SHOULD be cryptographically random (§9.3); differs by design.
2. **version_minor** — trailer table says "any"; no writer rule pins it (§6.2/§6.3).
3. **Directory record order** — order carries no meaning ([R-CNT-14]).
4. **Physical placement of step-2 structures** — payloads, index regions, record extents may be appended "in any order" ([R-LIF-02] step 2), changing every extent_offset, dir_offset, pad length, and F.
5. **Commit granularity** — one commit vs. many (including SHOULD-level checkpoint commits, [R-LIF-07]): different generation counts, extra superseded directories/trailers as dead space ([R-CNT-21]).
6. **Codec and filter selection per layer** (§7.4: filter 1 vs 2; codec menu in Reserved §17) — entirely different payload bytes for the same reference array.
7. **Non-canonical compressed output** — same codec value, different byte streams (implied by [R-CNF-05]; detail Reserved §17). Likewise user-metadata encoding 1 = none vs 2 = zstd (§7.1 [R-CNT-25]).
8. **Storing vs. sentineling an all-fill tile** — an addressed-but-unstored tile reads as fill (§3.1, [R-MDL-01]); a stored tile containing exactly the fill pattern yields the identical reference array.
9. **Fill field bytes when every tile carrying the channel is stored** — fill is consulted only where a tile is not stored (§3.2), so the stored fill bit pattern is then inert.
10. **Unicode normalization of names** — NFC is only SHOULD ([R-ENC-14]); with the caveat that byte-distinct names are *different names* under [R-ENC-13], so this is divergence only if "logical content" is defined above the byte level.

If "same logical content" is only the reference array (schema free): additionally tile extents, interleaved vs. planar layout, alignment A, slab declarations (§7.4, §16), and dimension-order conventions (§11.4 Note re column-major ecosystems) — each changes bytes wholesale. Not free: dimension/channel declaration order given a fixed schema (load-bearing, §3.1/§11.4), reserved bits, padding content (zero), registered record flags ([R-CNT-22]), linearization (only 1).

---

## AMBIGUITIES

1. **Codec value** (§7.4 table → §17 *[Reserved]*). No nonzero codec value is assigned anywhere in the present text, yet an unassigned value is reject-layer ([R-CNT-23]) and 0 is invalid. Readings: (a) no conforming layer record can be written yet; (b) 1 will be the "none/raw" codec by the document's uniform enum pattern (layout, linearization, filter, index_encoding, metadata-encoding all assign 1 first). I pick (b), value 1, because every enumerated field in §7 uses 1 as the first/identity assignment — but this is an unresolvable forward reference into a Reserved section.
2. **Channel type and element size** (§7.4 → §12 *[Reserved]*). Same structure as #1: no type value is assigned, and the fill's mandatory length "equals the type's element size" ([R-CNT-23]) is uncomputable without §12. I pick type = 1 with element size 1 to make the layout concrete; unresolvable forward reference.
3. **Tile-index entry layout, sentinel bit pattern, segment structure** (§7.4/§8.1 → §15 *[Reserved]*). The text fixes only: total region length via [R-CNT-17]'s formula; that a per-segment CRC array exists covering "index entries, per segment" (§8.1); that crc_of_crc_array covers that array (§7.4). Readings for region layout: entries then CRC array; CRC array first; CRC adjacent to each segment. I pick entries-then-array (matches the formula's additive form and §8.1's ordering), but the 20 sentinel bytes are simply unwritable from the present text — the single hardest blocker for a cleanroom writer.
4. **version_minor**: §6.2 lists valid values "any"; no rule states what a creating writer emits or whether an appender copies the prior trailer's minor or stamps its own (§6.3 constrains readers only). I emit 0 at creation and carry it forward on append — lowest value consistent with additive-only minors.
5. **"Re-emitting every retained record per §20's preservation rules"** ([R-LIF-02] step 3 → §20 *[Reserved]*). Readings: byte-identical re-emission (header + inline payload verbatim, extent slot unchanged when the extent is not relocated) vs. any semantically equivalent re-encoding. I pick byte-identical, anchored on preserve-verbatim's definition ("bytes carried forward unmodified (relocated only as Part I permits)", §2.4) and PE = 1 on the layer record (§7.3) — but the operative updater rule is Reserved.
6. **Fill content rules** (§13 *[Reserved]*): "fill per the rules" is satisfiable today only for the length rule ([R-CNT-23]); whether §13 constrains the value (e.g., NaN handling, bit-exactness obligations) is unknowable. I emit 0x00.
7. **Per-segment CRC coverage detail** (§8.1 vs §15): I assume each 4-byte CRC covers its segment's entry bytes exactly as stored (≤ 2¹⁶ × 20 bytes). The text's "index entries, per segment" permits this but does not pin segment boundaries' handling of the final partial segment.
8. **Appender verification depth for untouched layers**: [R-CNT-20] orders the chain trailer → directory → … and requires verifying each link "before acting on any field the link covers". Readings: (a) re-emitting a layer record verbatim is not "acting on" the fields its crc_of_crc_array covers, so trailer + directory CRC suffice (supported by §3.3's Note that appenders operate on layers they cannot decode); (b) strict reading requires walking every layer's index chain before any commit. I pick (a).

## CONTRADICTIONS

None found in the text needed for these four tasks. Candidates checked and dismissed: the §5.1 128-byte example is fully consistent with [R-CNT-05]/[R-CNT-06]; the [R-LIF-04] overwrite-beyond-F allowance does not conflict with [R-LIF-01] (immutability binds only [0, F)); [R-CNT-13]'s reject-layer for malformed layer-record extent slots is explicitly harmonized with [R-CNT-17].

## OBSERVATIONS

1. "Zero stored tiles" still yields one **addressed** tile (E=100 < T=256 → G=1, §11.1/§11.2), so the extent slot cannot be (0,0) and a 24-byte index region is mandatory ([R-CNT-17]) — easy to get wrong reading §7.4's "(0,0)" sentence alone.
2. With A = 0 and S = 0 there is no lawful padding class between structures ([R-CNT-02]/[R-CNT-03], §5.2): a writer cannot insert convenience gaps; every structure must pack exactly. Decidable only by enumerating the coverage classes.
3. The §5.1 example (empty directory CRC = 0x00000000) plus §4.5's check vector jointly confirm the CRC-32C parameterization (init 0xFFFFFFFF, final XOR 0xFFFFFFFF ⇒ CRC of zero bytes = 0).
4. On creation, the front signature block is emitted before commit "steps 2–6" (§9.2), so [R-LIF-02] step 4's "make steps 1–3 durable" does not literally name it; any real barrier flushes it, but the wording leaves the front block's durability unowned.
5. A trailer mimic sitting at exact physical EOF passes [R-CNT-06] (committed_file_length = physical size can hold there); §9.6's mimic caution is stated only for the backward scan, not the default open-at-end path — detection falls through to the directory CRC, consistent with §9.2's Note but never said explicitly.
6. §2.4 promises every structure's owning scope is "stated in the section that defines the structure", but §6 never states one for the trailer/front block; it is recoverable (all failures are reject-file per [R-CNT-04]/[R-CNT-06]) yet cost a cross-check.
7. Direct establishment of F ([R-LIF-04]) can never coexist with physical length > F, because [R-CNT-06] ties committed_file_length to the physical size — so the truncate-or-overwrite branch of [R-LIF-04] is reachable only via the deliberate-recovery path. Decidable, but only by composing the two rules.
8. The addressed-tile-count cross-check (entry_count must equal the geometry-derived count, [R-CNT-17]) makes entry_count fully redundant with §11.2 arithmetic — a writer must compute the grid math anyway; harmless but worth noting for implementers.
