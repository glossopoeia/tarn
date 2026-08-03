# Conforming TARN container reader — implementation plan (cleanroom, from `spec/tarn.md` only)

All citations are to `/Users/robertkleffner/Documents/GitHub/tarn/spec/tarn.md`.

---

## 1. Local open sequence (from a file path)

Notation: `L` = physical file size from the filesystem; trailer-relative offsets are within the 64-byte trailer; all multi-byte fields little-endian [R-ENC-01]; all CRCs are CRC-32C per §4.5 [R-ENC-09], self-tested at startup against the check vector `"123456789"` → `0xE3069283` (§4.5 says a checksum function that fails this "does not implement this specification's checksum").

**Step 0 — stat.** Obtain `L`. If `L < 16` the front-block equality check below necessarily fails → **reject-file** [R-CNT-04]. If `L < 64` no trailer can occupy the final 64 bytes → report torn/invalid, **reject-file**, and MUST NOT scan backward [R-LIF-05].

**Step 1 — front signature block (local readers only, first).** Read bytes `[0, 16)`. Compare all 16 bytes for equality against `89 54 41 52 4E 0D 0A 1A 00 00 00 00 00 00 00 00` (§6.1: 8 magic bytes + 8 reserved-zero bytes; both rows are structural, and the check is "the full block by byte equality before other processing"). Any mismatch → **reject-file** [R-CNT-04]. This is the only structure checked by equality rather than CRC (§4.5, [R-CNT-19]).

**Step 2 — trailer.** Read bytes `[L−64, L)`. Validate **in this exact order** per [R-CNT-06]:

1. **Trailer magic**: bytes `[0,8)` == `8A 4E 52 41 54 0D 0A 1A` (§6.2). Fail → **reject-file** (equivalently, "no valid trailer in the final 64 bytes" → torn-or-invalid, [R-LIF-05]).
2. **Trailer CRC**: CRC-32C over trailer bytes `[0, 60)` must equal the LE u32 at `[60, 64)` (§6.2 row "trailer CRC"; §8.1 row "Trailer"). Fail → **reject-file**.
3. **Version gate**: `version_major` (u16 at 8). `0` → **reject-file** (invalid); any major ≠ 1 → **reject-file** with a diagnostic distinct from "not TARN" and "corrupt", e.g. "TARN format major N; this reader supports major 1" [R-CNT-07]. `version_minor` (u16 at 10) is never grounds for rejection [R-CNT-07]. [R-CNT-06] notes only these three checks may run pre-gate because only these fields are position-fixed across majors [R-CNT-24].

Then, gates passed, validate **all of the following before acting on the fields involved** (no further order imposed by [R-CNT-06]); each failure → **reject-file**:

4. **Flag gates**: `flags` (u32 at 12). Any set bit in the incompat lane (bits 0–15) is unimplemented in major 1 (no flags are defined) → **reject-file**; ignore-lane bits 16–31 are ignored [R-CNT-08], §6.3. Bit numbering: bit 0 = LSB [R-ENC-08].
5. `committed_file_length` (u64 at 40) `== L` and `L mod 64 == 0` [R-CNT-06], [R-CNT-01].
6. `dir_offset` (u64 at 24) `≥ 16`, and ≤ 2⁶³−1 [R-ENC-03].
7. `dir_length` (u64 at 32) `≥ 4`, and ≤ 2⁶³−1 [R-ENC-03].
8. `dir_offset + dir_length ≤ L − 64`, computed with an explicit overflow guard; a mathematical sum exceeding 2⁶³−1 is itself reject-file [R-ENC-04].
9. `generation` (u64 at 16) `≥ 1`.
10. `file_id` (u64 at 48) `≠ 0`.
11. Reserved bytes `[56, 60)` all zero.

Note the reader does **not** check the pre-trailer pad gap or padding zeroness — those are verifier obligations [R-CNT-05], [R-CNT-03] ("readers are not obligated to check the gap bound").

**Step 3 — directory region.** Only now may I seek/read using file-derived integers, because the trailer CRC covering them is verified [R-ENC-05]. Read `[dir_offset, dir_offset + dir_length)`. Compute CRC-32C over the first `dir_length − 4` bytes; compare against the LE u32 in the final 4 bytes. This MUST happen "before any other use of the region"; mismatch → **reject-file** [R-CNT-11], [R-CNT-20]. The region is always raw — "no codec involvement on the open path" [R-CNT-11].

**Step 4 — top-level record parse.** Cursor `p` over the covered bytes `[0, dir_length − 4)`; zero records is valid ([R-CNT-14]; §5.1 Example: empty directory = 4 bytes holding CRC of zero bytes, `0x00000000`). Per record:

- If fewer than 24 bytes remain → header extends past sequence end → **reject-file** [R-CNT-12].
- Parse the 24-byte header (§7.2): `type` u16 @0, `flags` u16 @2 (bit 0 MU, bit 1 PE, bits 2–15 reserved — reader ignores reserved bits), `inline_length` u32 @4, `extent_offset` u64 @8, `extent_length` u64 @16.
- `type == 0` → **reject-file** (top-level scope) [R-CNT-12].
- `p + 24 + inline_length` past sequence end → **reject-file** [R-CNT-12].
- `MU=1, PE=0` → treat as `PE=1` [R-CNT-12] (affects updater behavior; recorded, not rejected).
- Dispatch by type, applying registered semantics **regardless of stored MU/PE bits** for known types [R-CNT-22]; never infer meaning from record position [R-CNT-14]:
  - `0x0001` layer → Step 5.
  - `0x0002` file-scope user metadata: a second one → **reject-file** [R-CNT-14]. Its extent slot is validated per [R-CNT-13] at **file** scope ("the file for other top-level records") → malformed → **reject-file**. The extent contents are not read at open; when read later, its final 4 bytes are a CRC over the preceding stored bytes (§8.1); CRC failure or an unimplemented encoding byte (u8: 0 invalid, 1 none, 2 zstd) → **ignore-record**, SHOULD report [R-CNT-25], [R-CNT-20].
  - Unknown type: `MU=1` → **reject-file**; `MU=0` → **ignore-record** [R-CNT-15]. An MU=0 unknown's payload/extent is opaque and encodes no other file offsets by rule [R-CNT-13], so skipping is safe.
- Advance `p += 24 + inline_length`.

After the loop: **duplicate layer name** check by raw byte equality — no normalization or case folding [R-ENC-13] — duplicate → **reject-file** [R-ENC-15].

**Step 5 — layer record parse** (per type-0x0001 record; owning scope of the inline payload is the layer [R-CNT-23]; every failure below is **reject-layer** unless stated; a rejected layer never aborts the file — other layers are unaffected, §2.4). Cursor `q` over the inline payload; fields are concatenated in table order (§7.4 "Its inline payload is, in order"), and any truncation/overrun of the fixed fields, dimension entries, or channel entries → **reject-layer** [R-CNT-18]:

1. `name`: u8 length prefix + bytes. Non-empty, well-formed UTF-8, no U+0000–U+001F → else **reject-layer** [R-ENC-11], [R-ENC-12] (duplication with another layer is the file-scope exception above).
2. `layout` u8 ∈ {1 interleaved, 2 planar}; 0/reserved → **reject-layer** [R-CNT-23].
3. `linearization` u16 == 1; **any** other value including 0, reserved 2–3, reserved 4–0x7FFF, and experimental ≥ 0x8000 → **reject-layer** [R-GEO-05].
4. `codec` u16; 0 → **reject-layer** (§7.4 table "0 invalid"). Assigned-set validation is blocked on §17 [Reserved] — see AMBIGUITY 2.
5. `filter` u16 ∈ {1 none, 2 byte-shuffle}; 0/others → **reject-layer** (§7.4 table, [R-CNT-23]).
6. `A` u64: 0, or a power of two; else **reject-layer**.
7. `S` u64.
8. `A_slab` u64: must be 0 when `S == 0` (nonzero → **reject-layer** [R-CNT-23]); else a power of two.
9. `A ≠ 0 && S ≠ 0` → **reject-layer** [R-CNT-16].
10. `d` u8 ≥ 1; 0 → **reject-layer** [R-GEO-01].
11. `C` u16 ≥ 1; 0 → **reject-layer** [R-GEO-01].
12. `d` dimension entries, each: name (u8 len + bytes, §4.6 rules; intra-layer duplicate → **reject-layer** [R-ENC-15]) · extent `Eᵢ` u64 (0 is valid [R-GEO-02]; > 2⁶³−1 → **reject-layer** [R-ENC-03]) · tile extent `Tᵢ` u64 (0 → **reject-layer** [R-GEO-01]; may exceed `Eᵢ` [R-GEO-01]).
13. `C` channel entries, each: name (rules as above) · type u16 (validation blocked on §12 [Reserved]) · fill (u8 len + bytes — "parses without type knowledge and validates with it", §7.4; the equals-element-size check is blocked on §12).
14. `index_encoding` u8 == 1 (raw-segmented); anything else → **reject-layer** ([R-CNT-23]; see AMBIGUITY 1 for the experimental range).
15. `entry_count` u64. Compute per §11.2 using the overflow-safe form: `Gᵢ = Eᵢ/Tᵢ + (Eᵢ mod Tᵢ ≠ 0 ? 1 : 0)`; `N = ∏Gᵢ`; addressed-tile count = `N` (interleaved) or `C·N` (planar) — every product overflow-checked, > 2⁶³−1 → **reject-layer** [R-GEO-03], [R-ENC-04]. `entry_count` ≠ addressed count → **reject-layer** [R-CNT-17].
16. `crc_of_crc_array` u32; nonzero with `entry_count == 0` → **reject-layer** [R-CNT-23].
17. **Extent-slot validation** ([R-CNT-13], scope = the layer): `(0,0)` = no extent (required shape when addressed count is 0, §7.4); any other combination with either half zero, `extent_offset < 16`, extent extending past `F − 64`, or an overflowing sum → **reject-layer**. Cross-check [R-CNT-17]: `extent_length == entry_count × 20 + ⌈entry_count / 2¹⁶⌉ × 4` (0 when `entry_count == 0`), the multiplication overflow-checked [R-ENC-04]; mismatch → **reject-layer**.
18. **Sub-records**: remaining payload bytes must parse as zero or more complete §7.2-framed records with no residue → overrun/truncation/residue → **reject-layer** [R-CNT-18]. Sub-record `type 0` → **reject-layer** [R-CNT-12]. Unknown sub-record `MU=1` → **reject-layer** (never reject-file); `MU=0` → **ignore-record** [R-CNT-18]. Second user-metadata sub-record → **reject-layer** [R-CNT-14]. Sub-record extent slots validated per [R-CNT-13] at layer scope.

**Output.** A list of layers; per layer: name, layout, linearization, codec, filter, A, S, A_slab, rank `d`, channel count `C`, ordered dimension triples (name, `Eᵢ`, `Tᵢ`), ordered channel triples (name, type, fill bytes), index_encoding, entry_count, crc_of_crc_array, tile-index extent slot, retained sub-records, plus derived `Gᵢ`, `N`, `P = ∏Tᵢ`, addressed-tile count (§11.2), and a rejected/valid flag. Rejected layers MAY still be listed by name (§2.4). The tile index is **not** read at open — its verification chain (crc_of_crc_array → segment CRC array → segment → entry → stored tile) runs when tiles are first accessed [R-CNT-20], and §15's entry layout is [Reserved] anyway. No heuristic repair ever [R-CNF-04]; no data returned from any rejected scope, and a rejected tile never silently reads as fill [R-CNF-09]. Overlap/coverage checks are explicitly **not** reader obligations ([R-CNT-13] "readers are not obligated to detect overlap"; §5.2 Note "coverage is checked by verifiers, never by readers").

---

## 2. Remote open over HTTP (F = 10,000,000 bytes)

Sanity: 10,000,000 = 156,250 × 64, so the hypothetical size is consistent with [R-CNT-01]. Trailer occupies absolute bytes [9,999,936, 10,000,000). The front block is never fetched: a remote reader MAY defer or omit that check, and §6.4's two-request accounting excludes it [R-CNT-04].

### Baseline (two requests, §6.4 [R-CNT-09])

**Request 1** — "fetch the final 64 bytes":

```
GET /file HTTP/1.1
Range: bytes=-64
```

Expected: `206 Partial Content` with `Content-Range: bytes 9999936-9999999/10000000`. The complete-length field `10000000` is my **transport-authoritative size** ("the complete length of a range response", [R-CNT-10]). Validate the 64 bytes exactly as local Step 2, with one substitution: `committed_file_length` is compared to the transport size, not a stat ("for a remote reader, the size reported by its transport", [R-CNT-06]). So: magic → CRC → version gate → flags, `committed_file_length == 10,000,000` and mod-64 == 0, `dir_offset ≥ 16`, `dir_length ≥ 4`, `dir_offset + dir_length ≤ 9,999,936`, `generation ≥ 1`, `file_id ≠ 0`, reserved zero. Any failure → **reject-file**.

**Request 2** — the directory region, `[dir_offset, dir_offset + dir_length)`:

```
Range: bytes={dir_offset}-{dir_offset + dir_length − 1}
```

Example: `dir_offset = 9,998,000`, `dir_length = 1,600` → `Range: bytes=9998000-9999599`. Then verify the directory CRC and parse exactly as local Steps 3–5.

### Speculative suffix variant ([R-CNT-09])

**Request 1′**:

```
Range: bytes=-65536
```

Expected `206` with `Content-Range: bytes 9934464-9999999/10000000`; buffer `B[0,65536)` maps to absolute [9,934,464, 10,000,000). Trailer = `B[65472, 65536)`; validate as above (transport size from Content-Range). **Containment test**: if `dir_offset ≥ 9,934,464` the whole directory region `[dir_offset, dir_offset+dir_length)` lies in `B` → decode from the buffer, request 2 unnecessary. Otherwise issue baseline request 2. The 64 KiB window matches the writer SHOULD (`dir_length` + pre-trailer pad + 64 ≤ 65,536); a larger directory "is conforming and merely costs the second request" [R-CNT-09].

### Transport edge cases the spec obliges ([R-CNT-10])

1. **200 to a range request**: MUST handle deliberately — either abort, or accept the full 10,000,000-byte body and slice locally; **never** treat the body prefix as the requested range.
2. **No suffix-range support** (416, or 200 to `bytes=-64`): SHOULD fall back to a size probe (e.g. HEAD yielding `Content-Length: 10000000`) plus an absolute range `Range: bytes=9999936-9999999`; the spec states the consequence of omitting the fallback — remote open "fails outright on such transports".
3. **Size must be transport-authoritative**: a full-response content length, the complete length of a range response, or a size probe. If none is obtainable (e.g. `Content-Range: bytes .../\*`), MUST probe separately or fail the open, and MUST NOT substitute the trailer's own `committed_file_length` for the transport size.
4. **Torn/mid-commit remote files**: size ≠ `committed_file_length` → reject-file; §9.5's non-normative Note permits a retry for attribute-cache staleness, and never a backward scan [R-LIF-05].
5. **Caching (optional)**: byte ranges may be cached keyed `(file_id, range)`; revalidation is one 64-byte trailer read — same generation ⇒ cache valid; higher generation ⇒ refetch directory; different file_id or lower generation ⇒ different file [R-LIF-03].

---

## 3. Three degradation walkthroughs

**(a) Trailer validates, directory CRC fails.** Steps 0–2 pass. Step 3 reads `[dir_offset, dir_offset+dir_length)`, computes CRC-32C over the first `dir_length − 4` bytes, mismatch against the final 4. Outcome: **reject-file**, immediately ([R-CNT-11] "mismatch: reject-file"; [R-CNT-20] "trailer or directory → reject-file"). Because verification precedes "any other use of the region" [R-CNT-11] and I may not act on unverified fields [R-ENC-10], **zero records are parsed**: no layer names are available, no partial listing is offered (§2.4 reject-file: "MUST NOT rely on any structure in it"), and no repair or salvage scan is attempted [R-CNF-04], [R-LIF-05]. The whole-file failure is reported; how is implementation technique (§2.4 Note).

**(b) Directory parses; one layer record has a malformed extent slot** (e.g. `extent_offset = 8 < 16`, or one half zero, or `extent_offset + extent_length > F − 64`, or the sum overflows 2⁶³−1). The slot check in Step 5.17 fires: outcome **reject-layer** — [R-CNT-13] states it verbatim: "a malformed slot on a layer record is therefore reject-layer, consistent with [R-CNT-17]". Behavior: that layer is marked unusable — data **and** metadata, including its user-metadata sub-record (§2.4: "the affected layer's data and metadata are not usable"); every other layer parses and is served normally; the rejected layer's name MAY still appear in the listing (§2.4). Any subsequent read addressed to the rejected layer reports failure; it never returns data "as valid" and never silently returns fill [R-CNF-09]. No attempt to guess corrected bounds [R-CNF-04].

**(c) Layer fine, but its codec value is one I do not implement.** Three distinct cases:

- `codec == 0`: invalid → **reject-layer** at parse (§7.4 table, [R-CNT-23]).
- The value is **reserved/unassigned** under §17's value set: **reject-layer** at parse ([R-CNT-23]: "a reserved or unassigned … codec … value … as a validity error at layer scope"). Blocking problem: §17 is [Reserved], so the assigned set is an unresolvable forward reference — today I can decide only the 0 case (AMBIGUITY 2).
- The value is a **core codec I merely didn't implement**: the spec assigns no reader outcome for this, because the state itself is nonconforming software — [R-CNF-03]: "software that declines to support a core codec … is not a conforming reader", "there are no subset profiles". My reader therefore implements every §17 core codec once §17 exists. Note the container open is unaffected either way: the codec field is touched only when decoding tile payloads ("tile payloads use the layer's codec field", [R-CNT-25]), so open, layer listing, and geometry all complete; a hypothetical codec-less reader would fail only at tile decode, outside any conformance class.

---

## 4. Codec-free implementability — CONFIRMED for everything above

Everything in deliverables 1–3 is implementable with zero knowledge of any compression codec. Decided by:

- [R-CNT-11]: the directory's covered bytes "are the record sequence itself — the directory is always raw, with no codec involvement on the open path."
- [R-CNT-25]: "The directory and the tile-index region are always raw (the index so that it can be range-fetched, §15); tile payloads use the layer's codec field (§17)" — codecs exist only behind tile decode, which the open path never performs.
- §7.4 channel-entry row: fill is length-prefixed precisely "so fill parses without type knowledge and validates with it" — the layer record parses fully without §12 or §17.
- §3.3 Note (non-normative but corroborating): "no Part I structure requires decoding sample payloads … verifiers, appenders, and compactors operate on files whose layers they cannot decode."
- The one codec-adjacent surface on the metadata side — a user-metadata document stored with encoding 2 (zstd) — has a **defined lawful outcome** for non-implementation: ignore-record, SHOULD report [R-CNT-25]. So even that requires no codec.

The only caveat, cleanly separable: **full reader-class conformance** (not the container reader above) does require implementing every §17 core codec [R-CNF-03] — for tile decoding, never for open/parse. And §17 is [Reserved], so that obligation is currently unsatisfiable by anyone.

---

## Consolidated list

### AMBIGUITIES

1. **§7.4 `index_encoding` experimental range (≥ 0x80).** (a) Location: §7.4 constraint column "1 = raw-segmented (0 invalid; 2 reserved; ≥ 0x80 experimental; §15)" together with [R-CNT-23]'s "reserved or unassigned … index_encoding" rejection. (b) Readings: (i) any value ≠ 1 is reject-layer in major 1, mirroring how [R-GEO-05] explicitly rejects linearization's experimental range; (ii) experimental values are conditionally legal under §10's mechanism (§10 is [Reserved]). (c) I pick (i): a reader cannot parse an index whose encoding it has no semantics for, [R-CNT-23] gives no experimental carve-out for this field, and §15/§10 provide no text to license one.
2. **Codec (u16) and channel-type (u16) assigned-value sets are unresolvable forward references into [Reserved] §17 and §12.** (a) Location: §7.4 rows "codec" and "type", [R-CNT-23] ("the value sets are §14, §17, §15, and §12's subjects"), [R-CNF-03]. (b) Readings: (i) accept any nonzero value at parse and defer rejection to decode time; (ii) reject every value not positively known assigned — which today is every value, since only "0 invalid" is stated. (c) I pick (i) provisionally (reject only 0), flagging that [R-CNT-23]'s reject-unassigned obligation for these two fields **cannot be implemented** until §17/§12 land; likewise the fill-length-equals-element-size check needs §12's element sizes. For channel type, not even "0 invalid" is stated (unlike layout/codec/filter/index_encoding), so I cannot confidently reject type 0.
3. **Duplicate layer name where one duplicate belongs to an otherwise-rejected layer record.** (a) Location: [R-ENC-15] (duplicate layer name → reject-file) vs §2.4 reject-layer ("all other layers are unaffected"). (b) Readings: (i) the duplicate check ranges over all layer records' names as bytes, regardless of layer validity → reject-file; (ii) rejected layers are excluded from the uniqueness pool. (c) I pick (i): [R-ENC-15] states the file-scope rule without exception, and §2.4 confirms a rejected layer's name remains legible.
4. **Eager vs lazy enforcement timing of layer-scope validity checks.** (a) Location: [R-CNT-23], [R-CNT-13], [R-CNT-17] say a reader "MUST treat" violations as errors at a scope, but no text fixes *when* detection must occur (open vs first access); §19, which would ("normative open and tile-read algorithms"), is [Reserved]. (b) Readings: (i) validate everything decidable from directory bytes eagerly at open; (ii) validate on first access to the layer. (c) I pick (i) for all checks needing only the (already fetched, CRC-verified) directory — same observable outcomes, simplest to prove [R-ENC-10] compliance; extent contents (tile index, metadata documents) stay lazy since fetching them at open is nowhere required.

### CONTRADICTIONS

5. **None found.** Candidate pairs examined and reconciled: [R-CNT-04] front-block-first vs trailer-anchored remote open (explicit remote exemption); [R-CNT-06] size-equality vs §9.4 physically-longer torn files (reader reports torn per [R-LIF-05]; recovery is a tool operation, [R-LIF-06]); [R-CNT-12] type-0 reject-file vs reject-layer (explicitly split by containing sequence); [R-CNT-25] "same outcome as a failed CRC" vs §8.2's table (both say ignore-record).

### OBSERVATIONS

6. **§7.4 gives field order but no offset table.** Packed concatenation (no inter-field alignment) must be inferred from "Its inline payload is, in order", [R-ENC-06] fixed widths, and [R-CNT-18]'s exact-parse/no-residue rule. Decidable, but §4.7's Note promises offset/size layout tables and §7.4 doesn't deliver one — disproportionate effort for a load-bearing conclusion.
7. **Outcome authority is delegated to ADR tables** ([R-CNT-11] "reject-file, ADR-0031"; [R-CNT-20] "the outcome of ADR-0031's table"), which are outside the document and unreadable in cleanroom. The outcomes are restated inline, so nothing blocked, but the normative citation chain dead-ends; the in-spec consolidated register (§21) is [Reserved].
8. **[R-CNF-03]/[R-CNF-10] bind conformance to §21's limits table, which is [Reserved].** The open-path skeleton is unaffected, but no implementation can currently know the minimum guarantees it must accept, so no final "conforming reader" claim is possible yet.
9. **CRC of an empty record sequence = `0x00000000`** is confirmed only by the non-normative §5.1 Example; deriving it from §4.5's parameters (init 0xFFFFFFFF, final XOR 0xFFFFFFFF over zero bytes) is easy but the normative text never states it.
10. **Minimum conforming file size 128** is derivable from normative constraints (`dir_offset ≥ 16`, `dir_length ≥ 4`, `dir_offset + dir_length ≤ F − 64`, F multiple of 64, [R-CNT-06]/[R-CNT-01]) and matches the non-normative §5.1 Example — worth a test vector.
11. **[R-CNT-06]'s post-gate checks are deliberately unordered** ("MUST validate all of the following before acting on the fields involved"); only magic → CRC → version-gate is sequenced. Implementations should not read an ordering into the prose list.
12. **§6.4 does not mandate the form of request 1** (suffix range vs probe-then-absolute); [R-CNT-10]'s fallback SHOULD implies suffix-first is the intended primary. I implement suffix-first with the mandated fallback.
13. **10,000,000 is exactly 156,250 × 64**, so the task's hypothetical size can be a real `committed_file_length`; had it not been a multiple of 64, request 1 would end in reject-file at the mod-64 check regardless of content.
14. **The reader has no fallback path by design**: no backward scan [R-LIF-05], no repair [R-CNF-04], recovery scan explicitly "not a reader behavior" (§9.6 heading, [R-LIF-06]) — this materially simplifies the open path and I implement none of §9.6 in the reader.
