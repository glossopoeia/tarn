# Reader-implementer walk — edition A — transcript (readera)

## 0. Disclosure

**Files read.** Exactly one specification file:
`/Users/robertkleffner/Documents/GitHub/tarn-first-draft/scratch/cleanroom/editions/a/tarn.md`
(4,981 lines / 302,380 bytes). It exceeded the Read tool's single-call size
cap, so I read it in eight sequential offset/limit chunks covering lines
1–4981 with no gaps and no overlap skipped (1–700, 700–1400, 1400–2100,
2100–2800, 2800–3500, 3500–4050, 4050–4600, 4600–4981), i.e. the entire
file, once, top to bottom. I did not open any other copy of this
specification, and I have no visibility into any other path in this
repository — I did not list any directory.

**Commands run.** `mkdir -p` and `ls -la` on my own scratch directory
(`/private/tmp/.../fidelity-1/scratch/walk-reader-a/`) before starting —
it was empty, no prior attempt's files were present. `wc -l` and `wc -c`
on the one target file only (line/byte count, to plan chunked reads — this
reads no *content*, just size, of the one permitted file). A local Python
script, `crc_check.py`, written to my scratch directory and run to verify
CRC-32C constants the document states, using only byte literals I
transcribed from the document text (no file I/O of any kind — see §7
below). No grep was needed in the end because the Read tool's chunking
gave complete, gap-free coverage; I did not need to hunt for a
hard-wrapped phrase via line-oriented search.

**Unsolicited context.** Before this task began, my context already
contained: a `CLAUDE.md` pointer to an `AGENTS.md` file; a user
auto-memory file listing many past-session notes with titles like "TARN
harness vs charter", "TARN repair prose vs rules", "TARN lineage gate word
list", etc.; a git-status block naming recent commit subjects (ADR-0133,
ADR-0132, round 37's repair, etc.); and various tool/skill inventories. I
have not opened, searched for, or relied on any of it. None of it is part
of the specification and none of it is evidence about the specification's
content. I mention only that it appeared, not its contents, per the
brief's instruction, and everything below is drawn solely from the one
file named above.

**Paths.** The file was exactly where the brief said it would be; no
discrepancy to report.

---

## 1. The open path — every byte fetched from a cold start, in order

Implementing `open()` in the order I'd write it:

1. **Obtain F.** For a remote reader, issue a suffix-range request for
   "the final 64 bytes" (§6.4, §19.1 step 1). A transport that discloses
   a range response's complete length hands back F in the same response
   (`[R-CNT-10]`), so this one request also answers "how big is the
   file" — steps 1 and 2 of §19.1 cost one request between them. If the
   transport can't disclose complete length, the reader must probe
   separately (a second request) or fail the open (`[R-CNT-10]`).
   Byte range: **[F−64, F)** — except that at the very first instant F
   is unknown, so this is physically a suffix request ("last 64 bytes"),
   not an absolute range; F becomes known from the response.
   - Gate before anything else: **F < 128 → reject-file**, decided from
     F alone, no other byte needed (`[R-CNT-27]`, register row F5). This
     is checkable before the suffix response's *body* is even
     inspected, from the disclosed length alone.
2. **Front signature block, conditionally.** If this reader's open
   leaves bytes [0,16) resident (e.g. a local whole-file read, an mmap,
   or — for a remote reader — only if it chose to speculate a suffix
   window large enough to reach offset 0), verify those 16 bytes by
   equality now (`[R-CNT-04]`, F1/F6). A reader that would need a
   further request for [0,16) MAY defer or omit this check entirely —
   the two-request baseline accounting of §6.4 never includes it.
3. **Validate the trailer**, in the *fixed* order §6.2 states:
   1. trailer magic bytes [0,8) of the fetched 64 == `8A 4E 52 41 54 0D 0A 1A` (F8);
   2. trailer CRC: bytes[60,64) == CRC32C(bytes[0,60)) (F14);
   3. version gate: version_major ≠ 0 and is a major this reader
      implements (F18; else `[R-CNT-07]`'s distinct-diagnostic capability
      refusal, not a register row, for major ≥ 1 the reader doesn't know);
   — only these three touch fields fixed across every major
   (`[R-CNT-24]`) —
   4. **then**, as a bundle with no stated sub-order among its members
      (§24 explicitly treats these as validated "together", so a file
      failing two attributes to neither alone): flags gates (F19 for any
      incompat-lane bit; ignore-lane bits are never a failure);
      committed_file_length == the transport-authoritative F and is a
      multiple of 64 (F13, F17); dir_offset ≥ 16 (F9); dir_length ≥ 4
      (F16); dir_offset + dir_length ≤ F − 64 (F10, and this sum is
      itself a `[R-ENC-04]` declaration-derived quantity, so its own
      overflow is a distinct check); file_id ≠ 0 (F12); reserved
      bytes [48,60) all zero (F15).
   Any failure here is reject-file; this is **step 2** of §19.1, and it
   consumes only the 64 bytes already fetched — no new I/O.
4. **Fetch the directory region.** Byte range **[dir_offset,
   dir_offset + dir_length)**. The field that bounds this range —
   dir_offset for its start, dir_length for its length — is available
   only because step 3 already validated both against the trailer CRC
   and the domain/bounds gates above; per `[R-ENC-05]`/`[R-ENC-10]` a
   reader must not seek or fetch using a field before the checksum
   covering it (the trailer CRC) has verified. This is the **second
   request** for a remote reader with no prior residency (§6.4); a
   reader may instead have spent one larger speculative request in step
   1 and use containment to skip this one if the directory fell inside
   what it already has.
5. **Verify the directory CRC** before any other use of the region:
   last 4 bytes of the region == CRC32C(preceding dir_length−4 bytes)
   (`[R-CNT-11]`, F20). This is the directory's *raw* record-sequence
   bytes — the directory is never codec-compressed (§7.1).
6. **Walk the record sequence** (§7.2 framing) over the CRC-verified
   bytes only, no further I/O:
   - Parse records back-to-back; each is a 24-byte header
     (type, flags, inline_length, extent_offset, extent_length) plus
     inline_length bytes of payload. Header or payload running past the
     sequence end, or residue after the last complete record, is
     reject-file (F29).
   - type == 0 is always a validity error, never "unknown" (F24).
   - For a non-layer top-level record: apply the MU gate for unknown
     types — MU=1 → reject-file (F35 if from the reserved range,
     otherwise just `[R-CNT-15]`'s MU rule biting on any type this
     reader doesn't implement); MU=0 → ignore-record. Apply per-type
     multiplicity: at most one top-level user-metadata record (F34).
     Apply extent-slot structural validity to *every* top-level record's
     slot regardless of whether its type is understood — (0,0) is
     "none"; any other half-zero is F30; offset in [1,16) is F31;
     offset+length > F−64 is F32; offset+length overflow is F3. This
     applies even to a record of an unassigned type, because the slot
     itself is a fixed-position structural field (§7.2) even though the
     *bytes it addresses* are left opaque and uncovered by any checksum
     (§8.1's map) once the type is unknown.
   - For a user-metadata top-level record specifically, on top of the
     generic extent rule: extent ≠ (0,0) is required (F21), extent_length
     ≥ 5 (F22), inline_length == exactly 1 (F23).
   - For each layer record (type 0x0001): parse only its **name**
     field now (nothing else of the layer record — layout, geometry,
     etc. — is touched until first access, §19.3). Build the layer-name
     table; a name that doesn't parse within inline_length contributes
     no name (and is instead flagged reject-layer under `[R-CNT-18]`,
     deferred to layer access, L23); duplicate raw name bytes among
     layer records is reject-file (F4, `[R-ENC-15]`), decided by raw
     byte comparison with no normalization (`[R-ENC-13]`), so even two
     invalid names that are byte-identical collide.

**Completing step 6 is "the open."** Its I/O is exactly: one 64-byte
fetch (or shared with F-discovery) + one dir_length-byte fetch — nothing
about tile indices, tile payloads, or non-name layer-record fields is
ever touched (`[R-RDR-01]`). This is the invariant §6.4's "two requests"
accounting exists to make legible; it holds at any file size and any
layer count.

---

## 2. Validation timing by tier (§19.2)

I implement this as four deferred-validation tiers, each gating the
narrowest possible read:

| Tier | What must pass before this tier's first reliance | Failure scope |
|---|---|---|
| **open** | front block (if resident), trailer, directory CRC + record walk, layer-name uniqueness | reject-file |
| **first layer access** | the *whole* layer record — extent slot, exact inline-payload parse, sub-record walk + multiplicity, name rules, u64 domain, every enum value set (layout/linearization/type/codec/filter/index_encoding), fill-length-vs-type-size, geometry floor + arithmetic ceiling, index-count/length cross-check (`[R-CNT-17]`) — all decidable from the already-resident directory bytes and F, **no fetch** (`[R-RDR-03]`) | reject-layer |
| **tile use** | crc_of_crc_array over the fetched segment-CRC array; the segment CRC over the fetched segment containing the needed entry; entry classification (§15.3); (if not sentinel) the stored bytes' own crc; decode exact-size | reject-layer (index-chain link) *or* reject-tile (entry/payload/decode) — see note below |
| **extent use** (a record's extent, e.g. user metadata) | that extent's terminal CRC, then (if an assigned encoding) the document's own content rules | ignore-record |

The one sharp edge worth flagging in code: **an index-chain failure
(crc_of_crc_array or a segment CRC) is detected at tile-use time but
takes *layer* scope** (`[R-IDX-04]`), not tile scope — so a single
malformed segment fails every tile whose entry lives in it, and bars
"further service from the layer" prospectively, while **already-returned
values from that layer under earlier successful tile reads stand**
(§19.2's closing paragraph, `[R-RDR-04]` step 8's last sentence). This
means my tile-read function's error type has to carry a scope tag
(layer vs tile), and a batched multi-tile request has to keep serving
already-validated tiles even after a later one in the same batch trips a
layer-scope failure retroactively-for-the-future but not retroactively-in-the-past.

A reader MAY detect any of this earlier than its tier — never later. So
a strict/eager implementation (validate every layer fully at open) is
still conforming; a lazy one is required to be *at least* this eager.

---

## 3. Layer access (§19.3) → tile-read algorithm to decoded samples (§19.4)

**First access to layer L** (triggered by anything beyond reading its
name) runs, purely against resident bytes:

1. Re-parse L's inline payload exactly per §7.4's field order — no gaps,
   no padding, sub-records framed per §7.2 to the end of inline_length
   with no residue.
2. Validate every enumerated field's value set: layout ∈ {1,2}; codec ∈
   {1,2,3,4}; filter ∈ {1,2}; index_encoding == 1; every channel type ∈
   {1..13}; linearization == 1.
3. Validate geometry floor: d ≥ 1, every Tᵢ ≥ 1, C ≥ 1 (Eᵢ = 0 is
   allowed, §11.1).
4. Compute, with overflow checking at 2⁶³−1 at every step
   (`[R-ENC-04]`): Gᵢ = ⌈Eᵢ/Tᵢ⌉ for each i; N = ∏Gᵢ; P = ∏Tᵢ;
   addressed-tile count = N (interleaved) or C·N (planar); decoded
   tile size(s) per §14.2/§14.3.
5. Cross-check entry_count == the geometry-derived addressed-tile count
   (`[R-CNT-17]`), and extent_length == entry_count×20 +
   ⌈entry_count/2¹⁶⌉×4.
6. Validate each channel's fill-field length == its type's element
   size, and (bool only) the fill byte ∈ {0x00, 0x01}.
7. Validate mutual exclusion of alignment vs slab declarations
   (`[R-CNT-16]`), and codec-4's decoded-size cap if codec==4
   (`[R-COD-07]`).

None of this issues I/O. Only after all of it passes is the layer
"accessed," and its declarations (dimension order, channel order,
fills, codec, filter, index shape) become load-bearing for reads.

**Tile-read algorithm**, for a request against an already-accessed
layer L (§19.4, implemented per-tile even for a region):

1. **Domain clip.** Point request: 0 ≤ xᵢ < Eᵢ or the request fails (no
   file verdict). Region request: intersect with extents; empty
   intersection or any request against a zero-extent layer returns no
   samples, successfully.
2. **Ordinal math.** tᵢ = xᵢ div Tᵢ, uᵢ = xᵢ mod Tᵢ; s = Σtᵢ·∏_{j>i}Gⱼ;
   in-tile ordinal = Σuᵢ·∏_{j>i}Tⱼ; disk ordinal = s (interleaved) or
   c·N+s per requested channel c (planar).
3. **Index-chain verify** (once per distinct segment touched, cacheable
   under committed-prefix immutability, §15.4's note): fetch+verify the
   segment-CRC array against crc_of_crc_array; fetch+verify the specific
   2¹⁶-entry segment against its stored CRC (the two fetches are
   independent of each other and MAY run in parallel — both are
   computable from the layer record alone with no dependency on the
   entry itself). Failure here → reject-layer, bars the rest of this
   request and all further service from this layer.
4. **Classify the entry** (§15.3's table, in the order that table
   states it — sentinel-first, then the two "exactly one half is
   sentinel" cases, then length==0, offset<16, domain, sum-overflow).
   A valid sentinel short-circuits — no payload I/O, return each
   carried channel's recorded fill at every requested position in this
   tile. Anything else malformed → reject-tile, no payload I/O either.
5. **Fetch payload** [offset, offset+length); verify entry.crc over
   those bytes *before* touching them further (`[R-CNT-20]`).
6. **Decode**: codec's decode, then the filter's inverse. Enforce: for
   codec 1, length == decoded size exactly, checkable pre-fetch
   (`[R-COD-04]`); for 2/3/4, decode must consume the extent exactly and
   produce exactly the decoded size, with codec 3 and 4's extra
   framing constraints (§17.2) checked from the header/stream itself,
   never used to size a buffer.
7. **Extract** requested values by §14.2/§14.3's offset arithmetic;
   never surface a padding position.
8. **Return** bit patterns verbatim (no NaN quieting, no −0/+0
   collapse) — except the one resolved case, `[R-SER-08]`'s treatment of
   a nonconforming interleaved-bool byte (0x00→false, anything
   else→true) if I choose to serve rather than reject a file exhibiting
   that specific writer defect.

For a multi-tile request, tile-scope failures are bounded to their own
tile's positions (I MAY partial-succeed and report per-entry, or fail
the whole request, but MUST NOT substitute fill for a rejected tile);
a layer-scope failure inside the same request (step 3) is not
so bounded — it bars the request's remaining entries.

---

## 4. Degradation walks (seven, end to end)

### D1 — Unknown top-level record type
A top-level record type 0x0050 (unassigned, reserved range) appears.
- **MU=1**: reject-file at open, register row F35 (with F36 additionally
  registering the mere *emission* of a reserved-range type as a
  verifier-detected violation regardless of MU). The reader never
  reaches the record's payload; nothing about the file otherwise being
  fine saves it, because `[R-CNT-15]` makes this file-scope.
- **MU=0**: ignore-record, SHOULD report the loss. The record's extent
  slot is still structurally validated (offset/length domain, no
  overlap) — F30/F31/F32/F3 still apply to *it*, since extent-slot
  framing is a fixed §7.2 structure independent of whether the type is
  known — but its extent's *contents* are covered by no checksum at all
  (§8.1's map: "the extent of a record of a type this specification has
  not assigned... none — the bytes are opaque"). So an unknown ignored
  record's payload can be silently corrupted with no detection anywhere
  in this format — this is one of §22.3's four named "residues."
- As a **layer sub-record** instead: same MU split, but scoped to
  reject-layer, not reject-file (`[R-CNT-18]`), and "where the file is
  otherwise conforming a reader MUST NOT reject the file for it."

### D2 — Unknown/invalid codec value
Layer declares codec = 7 (reserved, 5–0x7FFF). At **layer access**,
`[R-COD-03]` fires: validity error at layer scope (register L43). The
whole layer is unusable — no tile of it is ever attempted — but this is
purely a layer-access-time, zero-I/O check (codec value is read straight
out of the already-resident, already-CRC'd layer record), so it never
gets as far as fetching an index segment or a payload. Compare/contrast
with the probe R3 case below, which is a *different* failure mode
(reader capability, not file validity).

### D3 — Unrecognized flag
Two distinct mechanisms, both worth walking:
- **Trailer incompat-lane bit** (bits 0–15) set, e.g. flags =
  0x00000004: this text defines no bits at all in that lane, so *any*
  set bit there is "unimplemented" by definition → reject-file at open
  (F19, `[R-CNT-08]`). (This is exactly probe R2, below.)
- **Trailer ignore-lane bit** (bits 16–31) set: not a violation at all
  — ignored, file stays conforming (§21.6's table). An appender/rewriter
  must carry it forward unchanged and set no other such bit
  (`[R-CNT-08]`).
- **Record reserved flag bits** (bits 2–15 of a record's own flags):
  readers ignore them outright; only a *verifier* treats a set one as a
  nonconformance (F26/L47) — an ordinary reader never even looks.

### D4 — Truncated tail
Physical file is shorter than any committed_file_length it could ever
have validly declared, or simply lacks a valid trailer in its final 64
bytes altogether (e.g. write was interrupted mid-commit). The **default
read path is trailer-at-end-or-fail**: report torn/invalid; **MUST NOT
scan backward** (`[R-LIF-05]`). This is deliberately not "corrupt" in
the sense of a checksum mismatch — it may be a perfectly intact earlier
generation with a dangling partial commit appended — but a conforming
reader treats it identically to corruption at the file level: reject,
full stop. Recovery (probing backward for the nearest 64-aligned trailer
magic, re-verifying the *whole* candidate state before trusting it,
§9.6) is explicitly **not a reader behavior** — it's a separate
recovery-tool/verifier operation the spec is careful to keep out of the
default path, because a payload can deliberately contain bytes that
mimic a trailer (§21.6's table; §22.3's third named residue) and only
whole-state re-verification, never bare magic+CRC+length matching,
tells a mimic from a real one.

### D5 — Checksum mismatch
Three worked instances, at three different scopes, same underlying
mechanism (compare stored CRC-32C against computed):
- Directory region CRC fails → reject-**file** (F20) — nothing in the
  directory can be trusted, so no layer table, no records, nothing.
- A layer's segment CRC (or crc_of_crc_array) fails → reject-**layer**
  (L37/L38) at tile-use time (detection point), but the *scope* is the
  whole layer, retroactively for every tile whose entry lives in the
  bad segment/array, prospectively only (already-served tiles from this
  layer, if any, stand).
- A single stored tile's own crc fails → reject-**tile** only (T1); its
  entry is otherwise well-formed (`[R-IDX-03]`'s point that a bad
  payload-checksum, unlike a malformed entry, doesn't erase the entry's
  place in run-continuity/coverage bookkeeping — only its serve-ability).

### D6 — A limit exceeded
Two genuinely different things hide under this one phrase, and getting
them confused is exactly the trap `[R-ERR-04]`'s closing sentence warns
about ("a reader that reports 'too large' as 'corrupt' invites the
deletion of intact data"):
- **Hard domain limit** (2⁶³−1) on a `u64` field, or on a
  declaration-derived sum/product (`[R-ENC-03]`/`[R-ENC-04]`) — e.g. a
  layer's entry_count field itself holds 2⁶⁴−2 (in-domain-adjacent to
  the sentinel but over 2⁶³−1): this **is** a validity error at the
  owning scope (F2/F3 at file scope, L1/L2 at layer scope) — the file is
  nonconforming, full stop, no capability framing.
- **§21.9 minimum-guarantee exceeded** — e.g. a layer with 2⁴⁰ channels,
  or a document whose decoded size is 40 MiB: the file **remains
  conforming** (these are floors a reader must accept, not caps a
  writer can't exceed); a reader MAY decline at the narrowest scope its
  resources allow (or any containing scope), but **MUST report the
  refusal as a resource limit, never as corruption** (`[R-ERR-04]`), and
  software that declines something *within* the table on this ground is
  simply not a conforming reader at all.

### D7 — Format major the reader does not implement
version_major = 2 (this text defines major 1 only). Reject-file
(`[R-CNT-07]`), **but** this is explicitly *not* a finding about the
file's bytes — the file can be a perfectly conforming major-2 file for
all this reader knows. `[R-CNF-13]` narrows what this reader must still
check regardless of major: only the conditions that assert an invariant
`[R-CNT-24]` fixes in every major — trailer magic (F8), trailer CRC
(F14), and the front-signature-block instance of F1/F6 — reach this
file at all; every other file-scope/layer-scope row (F2–F36 apart from
those three, all of L*, T*, R*) is "not assessed against a file
declaring another major" and produces no register-row finding here.
Diagnostically, this SHOULD read "TARN format major 2; this reader
supports major 1," not "corrupt" (§6.3) — contrast with version_major=0
(F18), which is a real violation because 0 "declares no major at all"
and so isn't a not-yet-implemented-major case at all.

---

## 5. Worked example with real offsets

I use Appendix A's 128-byte minimal file (no layers) as my base case,
because it lets me verify every stated constant independently rather
than trusting the prose, and then extend it with §7.4's worked layer
record to get a worked *tile*-bearing example, per the arithmetic the
document itself gives.

**5a. The 128-byte file, byte-by-byte.**

```
0000  89 54 41 52 4E 0D 0A 1A  00 00 00 00 00 00 00 00   front block [0,16)
0010  00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00   directory region [16,20) = 4-byte CRC of zero bytes = 00000000
0020  00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00   pre-trailer pad [20,64), slack, zeroed
0030  00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00
0040  8A 4E 52 41 54 0D 0A 1A  01 00 00 00 00 00 00 00   trailer [64,128): magic, ver_major=1, ver_minor=0, flags=0
0050  10 00 00 00 00 00 00 00  04 00 00 00 00 00 00 00   dir_offset=16, dir_length=4
0060  80 00 00 00 00 00 00 00  EF CD AB 89 67 45 23 01   committed_file_length=128, file_id=0x0123456789ABCDEF
0070  00 00 00 00 00 00 00 00  00 00 00 00 7E 15 2F 40   reserved(12)=0, trailer CRC=0x402F157E
```

**Open, remote, containing 2 requests (or 1, by containment):**
- Request 1: [64, 128) — the final 64 bytes. F is disclosed as 128 by
  the transport in the same response.
  - F=128 ≥ 128: passes F5's floor.
  - magic == `8A 4E 52 41 54 0D 0A 1A`: pass (F8).
  - trailer CRC: I computed CRC-32C over bytes[0,60) of this trailer
    with a from-scratch CRC-32C implementation (polynomial 0x1EDC6F41
    reflected as 0x82F63B78, init/final-xor 0xFFFFFFFF) and got
    **0x402F157E** — matches the stated value exactly. ✓ (script output
    below)
  - version_major=1: implemented, pass.
  - flags=0: no incompat bit, pass.
  - committed_file_length=128 == F: pass. Multiple of 64: pass.
  - dir_offset=16 ≥ 16: pass. dir_length=4 ≥ 4: pass.
    dir_offset+dir_length=20 ≤ F−64=64: pass.
  - file_id=0x0123456789ABCDEF ≠ 0: pass.
  - reserved[48,60) all zero: pass.
- Request 2: [16, 20) — the directory region (dir_offset=16,
  dir_length=4). Its last 4 bytes (the whole region, since dir_length=4
  and the CRC occupies the final 4) must equal CRC-32C of the preceding
  dir_length−4 = 0 bytes. I verified: **CRC-32C(empty) = 0x00000000**,
  matching bytes [16,20) exactly. ✓
- Record walk over zero bytes: zero records, no residue, trivially
  valid. Layer table: empty (§21.6: "the file contains zero layers" is
  explicitly a conforming, valid generation).

A local reader (or a remote one whose speculative window reached offset
0 — on this exact 128-byte file, any window ≥ 128 bytes does) also
checks [0,16) by equality against the front-block constant: matches. A
remote reader fetching only [16,128) (112 bytes) instead of the whole
file still gets the directory by containment and can skip request 2,
while correctly leaving the front-block check to `[R-CNT-04]`'s
licensed deferral, exactly as Appendix A's own closing paragraph
describes.

**5b. Extending to a stored tile — §7.4's `sst` layer, computed
independently.**

Layer `sst`: rank 1, dimension `x` (extent 100, tile extent 32),
one interleaved float32 channel `temp`, fill = quiet NaN
0x7FC00000, codec 1 (none), filter 1 (none), no alignment/slab.

- Grid: G₀ = ⌈100/32⌉ = 4. N = 4 (interleaved, C=1 so addressed count
  = N = 4). P = 32. Decoded tile size (interleaved, single float32
  channel): P·Q = 32·4 = 128 bytes per tile.
- With no tile stored, index region = 4 sentinel entries (80 bytes) +
  1 segment CRC (4 bytes) = 84 bytes total, matching
  `[R-CNT-17]`'s formula: 4×20 + ⌈4/2¹⁶⌉×4 = 80+4 = 84. ✓ (matches the
  document's own stated extent-slot length for this record.)
- I independently computed the segment CRC over the 80 bytes of
  `FF×16 00×4` repeated four times: **0x80A34955**, stored little-endian
  as `55 49 A3 80` — matches the document's stated value exactly.
- I then computed crc_of_crc_array = CRC-32C over those same 4 stored
  bytes (`55 49 A3 80`): **0xC4EE982E** — matches the document's stated
  value exactly.
- I additionally computed the CRC-32C of a *full* 2¹⁶-entry all-sentinel
  segment (1,310,720 bytes of the sentinel pattern) independently:
  **0xEECB3BB2** — matches §15.4's stated constant exactly, confirming
  it (this is the constant `[R-IDX-05]` licenses writers to emit without
  computing, for any full all-sentinel segment).

All computed values matched the document's stated values exactly; no
discrepancy found in any constant I was able to check independently.
(Script: `crc_check.py` in my scratch directory; output captured
verbatim below.)

```
check vector 123456789: 0xe3069283 expect 0xe3069283
zero bytes: 0x0 expect 0x00000000
trailer bytes[0,60) length: 60
Appendix A trailer CRC: 0x402f157e expect 0x402f157e
segment CRC over 80 sentinel bytes: 0x80a34955 expect 0x80a34955
segment CRC stored bytes: 5549a380 expect 55 49 a3 80
crc_of_crc_array: 0xc4ee982e expect 0xc4ee982e
full 2^16-sentinel segment CRC: 0xeecb3bb2 expect 0xeecb3bb2
```

---

## 6. Probe derivations

**R1.** Remote reader, transport supports ranged requests and discloses
complete length on every response, 4,096-byte file. Requests before
trailer+directory can be validated:

1. **Suffix request for the final 64 bytes.** Physically this is a
   suffix-range request (the reader does not know F yet); the response
   both delivers bytes and discloses the transport-authoritative
   complete length, which *is* F = 4096 in this scenario. So this
   request resolves to byte range **[4032, 4096)**, 64 bytes, and
   simultaneously answers §19.1 step 1 (F) and delivers the bytes for
   step 2 (trailer). This matches §6.4: "steps 1 and 2 cost one request
   between them" whenever the transport discloses complete length,
   which the probe stipulates.
2. **Directory fetch**, byte range **[dir_offset, dir_offset +
   dir_length)** — read out of the now-validated trailer. This is
   request 2.

Total requests: **2**. Total bytes fetched: **64 + dir_length** (I
cannot give a single number for dir_length; it isn't stipulated by the
probe, only F=4096 is — the document doesn't let me derive dir_length
from F alone, since dir_length is a writer choice bounded only by
dir_offset+dir_length ≤ F−64 = 4032). The field that bounds the second
range, before it is read, is **dir_offset (its start) and dir_length
(its length)**, both trailer fields — and per `[R-ENC-05]`/`[R-ENC-10]`
they may only be acted on (used to seek/fetch) once the trailer CRC
covering them has verified, which happens as part of validating request
1's response before request 2 is ever issued. (§6.4 also licenses an
alternative one-request strategy — speculatively fetch a suffix window
and use containment — which for a 4,096-byte file could plausibly
capture the whole file in one shot; the document explicitly treats
request-count as a "theory of operation, not a budget" and states no
conformance requirement pinning it to exactly two, so which of the two
strategies "it" uses is genuinely up to the implementation. I give the
document's own stated baseline above as the canonical answer.)

**R2.** flags = 0x00000004 = binary …0000_0100 → bit index 2 is set (bit
0 = LSB, `[R-ENC-08]`). Bits 0–15 are the incompat lane (§6.3). Bit 2 ∈
[0,15]. This text defines *no* flag bits at all, so every incompat-lane
bit is "unimplemented" by construction (§6.3's own wording; register row
F19: "this text defines no flag bits, so every such bit is
unimplemented"). Outcome class: **reject-file** (`[R-CNT-08]`, register
F19). The file is **not conforming** — F19 is a listed file-conformance
violation (§21.2), not one of §21.6's defined non-violations (only the
*ignore*-lane, bits 16–31, is a non-violation).

**R3.** Codec value 3 (zstd) is a validly *assigned*, core codec
(`[R-COD-03]`: "all four are core — a conforming reader MUST implement
every one of them"). The document's answer is not "reject-layer" here —
that outcome is reserved for an *invalid* codec value (0, reserved
5–0x7FFF, or experimental ≥0x8000, register row L43). For an assigned
value the reader simply can't execute, `[R-COD-11]` is explicit and
narrow: "software unable to execute an assigned codec or filter is not
a conforming reader (`[R-CNF-03]`)" — full stop. The same sentence's
first half ("for a conforming reader that position arises only at a
reserved or experimental value... it rejects the layer") is stated to
apply *only* to reserved/experimental values, precisely because a
conforming reader by definition never lacks a core codec. So: **the
document does not name an outcome class for this scenario** — it
disqualifies the software from "conforming reader" status instead of
prescribing degraded behavior for it. Consequently it also does not say
whether such (non-conforming) software may serve other layers or list
this layer's declarations — that's outside anything the conformance
vocabulary of §2.4/§21 governs, since the vocabulary is defined in terms
of what a *conforming* reader does. (I flag this as a finding below —
readera-01.) If I answer as if the closest analogous, better-specified
mechanism applied (§21.9's resource-decline path, `[R-ERR-04]`), it
would say: decline at the narrowest scope (the layer), report it as a
resource/capability limit and not as corruption, and other layers are
explicitly unaffected by any reject-layer outcome (§2.4's table) — but
`[R-ERR-04]`'s own closing paragraph excludes exactly this ground from
its licence ("the two capability refusals §21.6's closing paragraph
names... are not this ground" — and lacking a core codec isn't even one
of *those* two), so this extrapolation is mine, not the document's.

**R4.** extent_offset == sentinel (2⁶⁴−1), extent_length ≠ sentinel.
§15.3's table, row for "offset = S ∧ length ≠ S, or offset ≠ S ∧
length = S": **structural, reject-tile**. Register row **T7** ("A
tile-index entry sets exactly one of offset and length to the sentinel
value"). Scope: tile — this entry alone fails; every other tile of the
same layer, including its neighbors, is unaffected (§2.4's reject-tile
definition). Being classified *structural* under `[R-IDX-03]`, this
entry contributes no stored extent to any verifier-side check (overlap,
run-continuity, coverage walk) — any bytes it nominally addressed fall
to slack if no other claimant claims them.

**R5.** Directory CRC mismatch → **reject-file** (`[R-CNT-11]`, register
F20). A reader "MUST NOT rely on any structure in it" (§2.4's
reject-file definition) — nothing is served: no layer table (never
built, since building it requires the record walk, which requires the
CRC-verified region), no layer, no tile, nothing. This is checked
*before any other use of the region* — earlier than the record walk
itself — so a corrupt directory never even gets as far as producing a
(possibly-wrong) layer list.

**R6.** File is exactly 96 bytes. The reader concludes reject-file
**from F alone** (the transport-reported/physical size), needing no
other byte of the file at all: §19.1 step 1 states this explicitly ("An
F below 128 is a validity error at file scope decided from F alone and
needing no other byte of the file"), and `[R-CNT-27]` derives the
128-byte floor arithmetically (front block 16 + directory minimum 4 at
offset ≥16 + 64-byte trailer, can't fit below 128). Outcome class:
**reject-file** (register row **F5**). Not even a range request for the
trailer is issued in an implementation that checks this first — 96 < 128
is decidable the instant the size is known.

**R7.** Interleaved layer, dims declared (y: E=12,T=5) then (x: E=9,
T=4); channels declared (a: uint16) then (b: uint8). Sample (y=6, x=5).

- Gy=⌈12/5⌉=3, Gx=⌈9/4⌉=3.
- ty=6 div 5=1, uy=6 mod 5=1; tx=5 div 4=1, ux=5 mod 4=1.
- Spatial tile ordinal s = Σtᵢ·∏_{j>i}Gⱼ = ty·Gx + tx·1 = 1·3+1 = **4**.
- Disk ordinal (interleaved, = s): **4**.
- In-tile ordinal u = Σuᵢ·∏_{j>i}Tⱼ = uy·Tx + ux·1 = 1·4+1 = **5**.
- Q (sample stride) = size(a)+size(b) = 2+1 = 3 bytes. F_b (channel b's
  in-sample offset) = size(a) = 2 bytes (sum of sizes of channels
  declared before b).
- Channel c's value at in-tile ordinal u sits at byte **u·Q + F_c**
  (§14.2's example note, general form): 5·3 + 2 = **17**.
- Cross-check via the table's own k-indexed form: k = u·C + c_b =
  5·2+1 = 11; offset = (k div C)·Q + F_{k mod C} = (11 div 2)·3 +
  F_{11 mod 2 = 1} = 5·3 + 2 = 17. Same answer.

**Answer: disk ordinal 4; channel b begins at byte offset 17 of the
decoded tile image.** (Verified by an independent Python re-derivation,
transcript §3/script above — script also double-checked Gy, Gx, ty, uy,
tx, ux, s, u arithmetic.)

**R8.** A top-level record of an unimplemented type carries MU=1: per
`[R-CNT-15]`, outcome is **reject-file** — the whole file is unusable,
regardless of how well-formed everything else is (this is the same
"reader is a reader before it can commit" logic §6.3 applies to an
unknown incompat-lane bit). **It differs for the same type value as a
sub-record inside a layer record**: `[R-CNT-18]` scopes an unimplemented
MU=1 sub-record to **reject-layer** only — "where the file is otherwise
conforming a reader MUST NOT reject the file for it" — so every other
layer, and the rest of the file's top-level records, remain fully
usable. The difference is exactly the nesting: a top-level MU=1 unknown
type has no scope narrower than the whole file to fail at (nothing else
"owns" a top-level record), while a layer sub-record's governing scope
is that one layer.

---

## 7. Findings

Listed with the byte-level test applied per the charter: does resolving
the gap change which bytes a conforming implementation may emit, or
must accept or reject?

### readera-01 — OBSERVATION — no outcome class for a reader that cannot execute a mandatory (core) codec or filter

**Where.** §17.2 (`[R-COD-03]`), §17.3 (`[R-COD-09]`), §17.4
(`[R-COD-11]`), §21.6's closing paragraph, §21.9 (`[R-ERR-04]`).

**What.** Every assigned codec value (1–4) and every assigned filter
value (1–2) is declared **core**: "a conforming reader MUST implement
every one of them" (`[R-CNF-03]`, restated at `[R-COD-03]`/`[R-COD-09]`).
The document has clean, register-backed treatment for the *adjacent*
cases — an invalid/reserved/experimental codec or filter *value* is
reject-layer (L43/L45); a verifier that cannot *execute* a codec is
told exactly what to do (`[R-COD-11]`: "cannot establish," MUST NOT
certify); and there are exactly **two** named "conforming file, reader
nevertheless refuses" capability escapes, enumerated by §21.6's closing
paragraph itself: an unimplemented format major (`[R-CNT-07]`), and an
experimental-range top-level record type carrying MU=1 (`[R-CNT-15]`).
For a *reader* (not a verifier) that lacks an assigned, core codec or
filter, `[R-COD-11]`'s only statement is: "software unable to execute
an assigned codec or filter is not a conforming reader." That sentence
disqualifies the software from the conformance class entirely; it does
not say what such software's behavior *is* — not "reject-layer," not
one of §21.6's licensed declines, not covered by `[R-ERR-04]`'s
resource-decline machinery (whose own text limits the "MAY decline
within the guarantee table" licence to declines made *on a resource
ground*, and separately says the two named capability refusals "are not
this ground" — implying, but never stating, where a codec-support gap
sits). A reader vendor who wants to ship software supporting, say,
three of the four core codecs (and knows this makes it non-conforming)
has no textual answer for what a spec-following *degraded* behavior
would look like — reject the layer? reject the file? the document
simply never reaches that question, because by its own construction the
question can't arise for a conforming reader.

**Byte-level test.** Does resolving this change which bytes a
conforming implementation may emit, or must accept or reject? **No.**
A conforming reader is required, unconditionally, to implement all four
codecs and both filters (`[R-CNF-03]`), so this scenario is definitionally
impossible for any implementation the specification's acceptance
obligations ever apply to; resolving the gap would only add guidance
for software that has already, by the document's own terms, left the
conformance class. It changes no accept/reject/emit boundary for a
conforming file or a conforming reader. `byte_level: false`.

**Verified via probe R3** above, independently of hunting for this as a
"finding" — the probe forced the question and the document's answer
turned out to be "this case is defined out of existence for conforming
software," which is worth surfacing explicitly since another
implementer working from a different edition might describe reject-layer
behavior here if their edition's §17.4/§21.9 differs even slightly in
wording (e.g. if it extended `[R-ERR-04]`'s licence to cover this
ground, or scoped `[R-COD-11]`'s "cannot establish" language to readers
as well as verifiers).
