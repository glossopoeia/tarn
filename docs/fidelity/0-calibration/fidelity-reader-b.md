# Reader-implementer walk — TARN format, edition B

## 0. Disclosure

**What I read.** Exactly one file, in full, in six `Read`-tool chunks (the
tool's own size limits forced the chunking; offsets used: 1, 1000, 1800,
2600, 3400, 4000, 4500, ending at line 4977 which is EOF):

```
/Users/robertkleffner/Documents/GitHub/tarn-first-draft/scratch/cleanroom/editions/b/tarn.md
```

4,977 lines, 302,125 bytes. I did not open any other file: not AGENTS.md,
not any ADR, not PLAN.md/OPEN-QUESTIONS.md/README.md/CONTRIBUTING.md, not
`conformance/`, not `spec/registry.json`, no git history, no web search or
fetch, and no other copy of this specification under any other path. I did
not list any directory other than my own scratch directory (to check for a
prior attempt's leftovers — it was empty).

**What I ran.** `wc -l` and `wc -c` on the one target file; two rounds of
`rg` (ripgrep) against that same file only, plus one Python one-liner doing
local string-membership arithmetic on the text already read into a shell
variable/file (no other file access). All of this is local computation
over the one file's bytes, and no other file was read as a side effect.

**Path check.** The file was exactly where the brief said it would be, at
the path above. Nothing to flag.

**Hard-wrap gotcha — demonstrated, not just heeded.** Before trusting any
zero-hit search, I ran a control pair:

```
$ rg -n "A reader MUST accept every conforming file of a format major version it implements" tarn.md
(no output; exit code 1)

$ python3 -c "
import re
text = open('tarn.md').read()
norm = re.sub(r'\s+', ' ', text)
print('A reader MUST accept every conforming file of a format major version it implements' in norm)
"
True
```

The phrase is present (it is the opening of the "Conforming reader" bullet
in §2.3, wrapping across two lines), but a naive line-oriented `rg` reports
zero hits. This confirms the brief's warning is live on this file, and it
is why every negative claim below is either (a) based on having read the
whole document top to bottom rather than on a grep miss, or (b) based on a
grep hit on a token/table cell that in fact sits intact on one line (I
checked each such token's context by eye before relying on it).

**Context noticed but disregarded.** My runtime context, before I read the
target file, already contained: a project `CLAUDE.md` pointing at an
`AGENTS.md` I did not open; a personal memory index (titles only) of many
other TARN-project notes; and a git-status block naming several recent
commit subjects about ADR-0132/0133. None of that is part of the
specification, none of it is evidence about the specification, and nothing
below relies on it or repeats its contents beyond this acknowledgment. I
also treated the harness's own computed-task prose as script output, not
as the user's voice, per its own framing, and drew the charter and the
eight probes from it as the assignment while disregarding any instruction-
like framing inside it beyond that.

---

## 1. The open path — every byte fetched from a cold start

Walking the algorithm as written for a **remote** reader whose transport
supports ranged requests and discloses each response's complete length
(§6.4, §19.1, `[R-CNT-09]`, `[R-CNT-10]`, `[R-RDR-01]`):

1. **Request 1 — suffix range for the final 64 bytes.** Range
   `[F − 64, F)`. Before this request, F is not yet known to the reader
   (that is the point of a suffix range); the response's *complete
   length*, when the transport discloses it, is what the reader takes as
   the transport-authoritative F (`[R-CNT-10]`). This one request
   therefore discharges §19.1's steps 1 (obtain F) and 2 (fetch and
   validate the trailer) together — the document is explicit that these
   two steps are "ordered by dependency, not by I/O" and that "a remote
   reader's suffix range for step 2 carries F in its own response, so
   steps 1 and 2 cost one request between them" (§6.4, §19.1 step 1).
   The fetched 64 bytes are validated in §6.2's fixed order: trailer
   magic; trailer CRC; version gate; then (only once those pass) the
   remaining field gates together — flags, `dir_offset ≥ 16`,
   `dir_length ≥ 4`, `dir_offset + dir_length ≤ F − 64`, `file_id ≠ 0`,
   reserved bytes zero, and `committed_file_length = F` (transport size)
   and a multiple of 64 (`[R-CNT-06]`).
2. **Request 2 — the directory region.** Range
   `[dir_offset, dir_offset + dir_length)`. **`dir_offset` and
   `dir_length`, both read from the trailer fetched in request 1 and
   both gated by `[R-CNT-06]`'s checks before they are acted on
   (`[R-ENC-10]`: "verify the checksum covering a field before acting on
   that field"; the trailer CRC is that checksum, and it is verified
   before `dir_offset`/`dir_length` are used to form this range) — are
   what bounds this second range.** The directory region's final 4 bytes
   are then verified as a CRC-32C over the preceding `dir_length − 4`
   bytes before any other use of the region (`[R-CNT-11]`).
3. **No further request is needed to complete the open.** §19.1 step 4
   (the record walk: type/flags/inline_length/extent-slot framing per
   record, the MU gate for unknown top-level types, per-type
   multiplicity, and building the layer-name table) is pure computation
   over the bytes already fetched in request 2. "Completing these steps
   is *the open*. It consumes the trailer and directory only... so its
   I/O is §6.4's request accounting... at any layer count and file size"
   (§19.1, `[R-RDR-01]`).

**Front signature block, [0, 16).** This is *not* fetched by either of
the two requests above (it lies before `dir_offset ≥ 16`, and neither
request's range can reach below `F − 64` unless the file is tiny). Under
`[R-CNT-04]`, a reader "whose open leaves bytes [0, 16) resident" — e.g.
a local reader that reads/mmaps the whole file, or a remote reader whose
*speculative* suffix window happens to reach offset 0 — MUST verify it by
byte equality before other processing; a reader (like the plain two-
request remote reader walked above) that would have to issue a *further*
range request just to get those 16 bytes MAY defer or omit the check
entirely. So for the baseline two-request remote open, the front block is
never fetched and never checked, and this is licensed, not a gap.

**Totals for the plain two-request open above:** 2 requests; total bytes
fetched = 64 (trailer) + `dir_length` (directory region) — `dir_length`
is a per-file value with no fixed number in the general case (only the
bounds `4 ≤ dir_length` and `dir_offset + dir_length ≤ F − 64` are fixed
by the trailer's own gates). §6.4's Note is explicit that "no request
count is a conformance property" and that a reader speculating a
suffix window in one request (using containment to skip request 2 when
the window already contains the directory) is equally conforming; I
walked the two-*exact*-range baseline because the probe (R1, below) asks
for "every request it makes," and the baseline is what the document
states has an "exact target" per request (§6.4's opening sentence).

---

## 2. Validation timing by tier (§19.2, `[R-RDR-02]`)

The document fixes the *latest* point at which each class of check is
due, not the earliest (a reader MAY always check sooner, `[R-CNF-12]`):

- **At open:** front signature block (if resident, else deferred/omitted
  per `[R-CNT-04]`); the trailer; the directory region's CRC and record
  walk; the layer-name uniqueness check across the whole directory
  (`[R-ENC-15]`). All of this is decidable from the two fetched ranges
  alone.
- **At first access to a layer:** the *full* layer-record validation of
  §19.3 — extent slot, the entire §7.4 field/value-set/constraint list,
  sub-record walk and multiplicity, name rules, the u64 domain and
  `[R-ENC-04]` overflow ceiling on every derived quantity, the index
  cross-check `entry_count`/`extent_length` arithmetic (`[R-CNT-17]`).
  Still zero additional I/O: "All are decidable from the resident
  directory and F: layer access performs no fetch" (`[R-RDR-03]`).
- **At use of a tile:** the index-chain (crc_of_crc_array, then the
  covering segment CRC), the entry's own classification (§15.3), the
  payload fetch and its CRC, then codec-decode and filter-inverse
  (§19.4 steps 3–6). This is the first tier that costs I/O beyond the
  open.
- **At use of a record's extent** (a user-metadata document, in format
  major 1): that extent's terminal CRC, and only then the content rules
  §18.2 attaches at its declared encoding.

A violation's *outcome and scope* always follow the rule that defines it,
even when its *detection point* is later — the document flags this
explicitly for the index chain: "index-chain failures take layer scope
(`[R-IDX-04]`) although their detection point is tile use" (§19.2).

---

## 3. Layer access → decoded samples (§19.3, §19.4, §14)

**Layer access (`[R-RDR-03]`).** First use of any of a layer's
declarations (other than its name, already parsed at open) triggers full
validation of the layer record before any of those declarations are
relied on. This is what makes it safe for the tile-read algorithm below
to *assume* the layer's geometry, layout, codec, filter, and channel
declarations are already known-good.

**Tile-read algorithm (§19.4, `[R-RDR-04]`), point or region request:**

1. **Domain.** Point request: check `0 ≤ xᵢ < Eᵢ` per dimension; out of
   range is a *request* failure, not a file finding (`[R-MDL-01]`).
   Region request: clip to the layer's extents; a region wholly outside,
   or any region of a zero-extent layer, returns no samples
   (`[R-GEO-02]`).
2. **Ordinals.** Tile coordinates `tᵢ = xᵢ div Tᵢ`, in-tile position
   `uᵢ = xᵢ mod Tᵢ`; spatial ordinal `s = Σ tᵢ · ∏_{j>i} Gⱼ` (row-major,
   linearization 1, the only value this major defines, `[R-GEO-05]`);
   disk ordinal = `s` (interleaved) or `c·N + s` (planar, per requested
   channel `c`) (`[R-GEO-06]`).
3. **Index chain.** Verify `crc_of_crc_array` over the fetched
   segment-CRC array, and the segment CRC over the fetched segment
   containing the needed entry (`[R-IDX-04]`); both fetches/verifications
   may run in parallel and may be cached under committed-prefix
   immutability (§9.3).
4. **Entry.** Classify per §15.3's table. A valid sentinel short-circuits
   steps 5–6: every requested position of that tile reads, per channel it
   carries, that channel's *recorded* fill (`[R-TYP-06]`, `[R-TYP-08]`),
   with zero payload I/O. Any other malformed shape rejects the tile —
   never returns fill (`[R-CNF-09]`).
5. **Payload.** Fetch `[offset, offset+length)`; verify the entry's `crc`
   over the stored bytes *before* decoding (`[R-CNT-20]`).
6. **Decode.** Codec, then the filter's inverse (§17.1); decoded length
   must equal exactly the layer/type-derived decoded size (`[R-SER-07]`).
7. **Extract.** Locate requested values by §14.2/§14.3's offset
   arithmetic (worked below, §5); padding positions are never returned
   (`[R-GEO-04]`).
8. **Return.** Bit patterns unaltered (`[R-MDL-02]`, `[R-TYP-04]`), with
   `[R-SER-08]` the sole defined exception (an interleaved bool byte that
   is neither `0x00` nor `0x01` in a file a reader chooses not to reject
   is returned as `false` only for `0x00`, `true` for every other byte —
   this never arises in a conforming file).

Byte-layout arithmetic used at step 7 (§14.2): planar numeric channel
`c`, decoded size `P · Bᶜ`, value `k`'s offset `k · Bᶜ`; interleaved,
decoded size `P · Q` (`Q = Σ Bᵢ`, the sample stride), channel `c`'s value
at in-tile ordinal `u` at byte `u · Q + Fᶜ` (`Fᶜ = Σ_{j<c} Bⱼ`). Planar
bool: bit-packed LSB-first, `⌈P/8⌉` bytes (§14.3).

---

## 4. Degradation walks (seven, end to end)

For each: the concrete file/request state, the rule that governs it, the
outcome class, and the scope.

**(a) Unknown top-level record type.**
- Type value in the *experimental* range (≥ 0x8000), MU = 0: `ignore-
  record`; file stays conforming (`[R-CNT-15]`, §21.6). Same value,
  MU = 1: `reject-file` (`[R-CNT-15]`, register F35 for the reserved-
  range instance; for the *experimental*-range instance with MU = 1 the
  reader still rejects the file, but the file itself remains conforming
  — §10.3's prohibition binds the writer's conduct, not the bytes,
  `[R-CNF-02]`, §21.6's second "structural case" paragraph).
- A type value in the *reserved* range (0x0003–0x7FFF, never assigned):
  emitting it at all is itself a violation a verifier must catch (F36),
  independent of the MU bit; a reader applies the same MU-gated
  treatment as above (F35 when MU = 1).
- As a layer **sub-record** instead of top-level: MU = 1 → `reject-
  layer`, not `reject-file` — "where the file is otherwise conforming a
  reader MUST NOT reject the file for it" (`[R-CNT-18]`); MU = 0 →
  `ignore-record` at layer scope. This file/sub-record split is exactly
  probe R8, answered in full below.

**(b) Unknown codec.**
- Codec field 0, a reserved value (5–0x7FFF), or an experimental value
  (≥ 0x8000): `reject-layer`, decidable at layer access with no I/O
  (`[R-COD-03]`, `[R-CNT-23]`, register L43).
- Codec field **3 (zstd)**, an assigned, *core* value, but the reader
  does not implement zstd: this is probe R3, and I could not find a
  register row or outcome class that governs it — see Finding
  **readerb-01** below. The file is not defective; the *reader* fails
  `[R-CNF-03]`'s "MUST handle every codec... that §17 designates as
  core" and is thereby not a conforming reader at all, a status the
  document does not further operationalize.

**(c) Unrecognized flag.**
- Trailer **ignore-lane** bit (16–31) set: not a violation at all; "the
  file is conforming — such bits are defined by later minor versions"
  (`[R-CNT-08]`, §21.6); the reader ignores it and proceeds.
- Trailer **incompat-lane** bit (0–15) set: this text defines none, so
  *every* such bit is, for every reader of this text, unimplemented by
  definition — `reject-file` (`[R-CNT-08]`, register F19). This is probe
  R2, answered in full below.
- A record's **reserved flag bits** (bits 2–15 of a record's own 16-bit
  flags field, distinct from the trailer's lanes): writers must emit
  zero, but *readers* MUST ignore them outright; only a *verifier*
  is obliged to flag a nonzero reserved bit as a (writer-side)
  nonconformance (`[R-CNT-12]`, registers F26/L47). So an ordinary
  reader's behavior is unaffected either way — it never even branches on
  these bits.

**(d) Truncated tail.**
- The default read path is "trailer-at-end-or-fail": if the final 64
  bytes at the physical end don't pass the trailer's gates (wrong magic,
  bad CRC, or `committed_file_length` mismatched against the transport-
  reported size), the reader reports the file torn/invalid and **MUST
  NOT scan backward** (`[R-LIF-05]`, register rows F8/F14/F17). Outcome:
  `reject-file`. Recovering the last good commit state by scanning
  backward is a *separate, deliberate* operation (§9.6) performed by
  recovery tools/verifiers, never by a conforming reader on its default
  path.

**(e) Checksum mismatch.**
The outcome depends entirely on which structure's checksum failed —
there is no single "checksum mismatch" outcome:
  - Trailer CRC → `reject-file` (F14).
  - Directory region CRC → `reject-file` (F20).
  - `crc_of_crc_array` vs. the stored segment-CRC array → `reject-layer`
    (L37).
  - A segment CRC vs. its entries' bytes → `reject-layer` (L38).
  - A tile-index entry's `crc` vs. its stored bytes → `reject-tile`
    (T1), and specifically **never** fill-in-place-of-failure
    (`[R-CNF-09]`) — the entry itself was well-formed, only the bytes it
    points at are bad (`[R-IDX-03]`'s "well-formed" carve-out).
  - A user-metadata extent's terminal CRC → `ignore-record` (R2 of
    §21.5 — note this reuses the label "R2," distinct from *my* probe
    R2 about trailer flags; I use "§21.5 R2" below to disambiguate).

**(f) Limit exceeded.**
Every quantity in §21.9's table is a **minimum guarantee**, never a cap:
a file exceeding one (e.g., a document larger than 16 MiB decoded, or a
zstd frame declaring a window over 8 MiB) remains conforming, and a
reader **MAY** decline it at the narrowest scope that overflows (a
record, a layer, a tile, or the whole file), but **MUST** report the
decline "as a resource limit and not as a validity error" (`[R-ERR-04]`).
Declining a file that stays *within* every guaranteed bound, on that
ground, disqualifies the software as a conforming reader (`[R-CNF-03]`).

**(g) Format major the reader does not implement.**
`version_major` ∉ {1} and ≠ 0: the reader **MUST** `reject-file`
(`[R-CNT-07]`), but — uniquely among the seven — this is explicitly *not*
a finding about the file's bytes: "a file declaring another major is
neither conforming nor nonconforming under it save as to the conditions
that reach it" (`[R-CNF-13]`), and §21.6 names this as one of exactly two
"conforming files a reader nevertheless refuses." Only F18
(`version_major = 0`, which "declares no major at all") is an actual
register violation; a well-formed major-2 (say) file is simply outside
this document's jurisdiction except for the handful of conditions
`[R-CNT-24]` fixes across every major (the front block, the trailer
magic position/size, the trailer-CRC position and coverage, and the
16-byte-window of fixed trailer fields) — those *do* reach it and are
still checked (F1's two instances, F6, F8, F14 — see §2.3's Note listing
exactly these).

---

## 5. Worked example with real offsets (§7.4's own example, checked)

I used the specification's own §7.4 worked example (a single-channel
`sst` layer) as the one I could fully re-derive and check arithmetically,
rather than inventing a new file, since the brief asks to check "any
stated constant or checksum you can" and this is the one worked example
in the document that states both a full byte layout *and* two checksums.

Layer: rank 1, dimension `x` (extent 100, tile extent 32), interleaved,
one channel `temp` (float32), codec 1 (none), filter 1 (none), no
alignment/slab, `entry_count = 4`.

**Grid arithmetic check.** `G = ⌈100/32⌉ = 4` (32·3 = 96 < 100 ≤ 128 =
32·4) ✓, matching the document's stated `entry_count = 4`.

**Index-region size check (`[R-CNT-17]`).**
`entry_count × 20 + ⌈entry_count / 2¹⁶⌉ × 4 = 4×20 + 1×4 = 84`. The
document states the extent slot's length as 84. ✓ (`⌈4/65536⌉ = 1`, one
segment, one 4-byte CRC — matches.)

**Inline-payload byte count check.** The document's byte-by-byte table
sums to: name (1+3=4) + layout(1) + linearization(2) + codec(2) +
filter(2) + A(8) + S(8) + A_slab(8) + rank(1) + C(2) = 34, plus the
dimension entry (1+1 name + 8 + 8 = 18), plus the channel entry
(1+4 name + 2 type + 1+4 fill = 12), plus index_encoding(1) +
entry_count(8) + crc_of_crc_array(4) = 13. Total
`4+34-4... ` — recomputing directly by field: name block 4, then
layout..C is 1+2+2+2+8+8+8+1+2 = 34, dimension 18, channel 12, trailing
13. `4 + 34 + 18 + 12 + 13 = 81`. The document states 81 bytes. ✓

**crc_of_crc_array — checked by computation, not just trusted.** With no
tile stored, all 4 entries are the sentinel `FF×16 00×4` (20 bytes each),
so the 80-byte entry array is `FF` repeated 64 times interleaved with
`00×4` four times, i.e. bytes = (`FF`×16 `00`×4) repeated 4 times = 80
bytes total. I computed CRC-32C (the RFC 3720 §12.1 Castagnoli
parameters stated in §4.5: poly 0x1EDC6F41 in reflected form, init/final
XOR 0xFFFFFFFF) over that 80-byte string locally (Python, `zlib` does not
provide CRC-32C directly, so I implemented the bit-reflected table-driven
algorithm and cross-checked it first against the document's own **check
vector**: CRC-32C(`"123456789"`) must equal `0xE3069283`, and
CRC-32C(zero bytes) must equal `0x00000000` — both of which my
implementation reproduced before I trusted it on the 80-byte string).
Result: `0x80A34955`, stored little-endian as `55 49 A3 80` — **matches
the document's stated segment CRC exactly.**

I then took the 4-byte segment-CRC array `55 49 A3 80` and computed its
own CRC-32C (this is `crc_of_crc_array`, covering the segment-CRC array
per §7.4/§8.1). Result: `0xC4EE982E`, little-endian `2E 98 EE C4` —
**matches the document's stated `crc_of_crc_array` exactly.**

Both of the document's own stated checksums in this example check out
against the CRC-32C definition given in §4.5, computed independently. I
also computed the §15.4 constant for a full (2¹⁶-entry) all-sentinel
segment — `sentinel_entry × 65536`, CRC-32C — and got `0xEECB3BB2`,
matching the document's stated constant exactly.

This was run as an actual, from-scratch, table-free bit-reflected
CRC-32C implementation over literal byte strings (no file I/O — the
sentinel pattern and the check vectors are both stated in the document's
own text), executed via Bash/Python in this session; it is not an
assertion of a result I did not compute. The exact commands and their
output:

```
check vector 1 (expect 0xE3069283): 0xe3069283
check vector 2 (expect 0x00000000): 0x0
segment CRC over 80-byte all-sentinel entry array (expect 0x80A34955): 0x80a34955
segment CRC stored little-endian: 55 49 a3 80
crc_of_crc_array (expect 0xC4EE982E): 0xc4ee982e
crc_of_crc_array stored little-endian: 2e 98 ee c4
full 2^16-entry all-sentinel segment CRC (expect 0xEECB3BB2): 0xeecb3bb2
```

---

## 6. Probe answers (derivation shown; final answers also in structured
output)

### R1 — cold remote open of a 4,096-byte file

Two requests, in this order, before the trailer and directory can be
validated:

1. `[4032, 4096)` — the suffix range for the final 64 bytes. Its
   response's disclosed complete length is taken as the transport-
   authoritative F = 4096 (§6.4, `[R-CNT-10]`), which is also §19.1
   step 1. These 64 bytes are then validated in §6.2's fixed order.
2. `[dir_offset, dir_offset + dir_length)` — the directory region,
   where **both `dir_offset` and `dir_length`, read from the trailer
   fetched in request 1 and validated by `[R-CNT-06]`'s gates
   (`dir_offset ≥ 16`, `dir_length ≥ 4`,
   `dir_offset + dir_length ≤ F − 64 = 4032`) before being acted on
   (`[R-ENC-10]`), are what bound this range.**

Total: 2 requests; total bytes fetched = `64 + dir_length`. The document
does not fix `dir_length` for a generic 4,096-byte file (only its
bounds), so the total is expressed in terms of it, not as a bare number.
(A reader could instead speculatively fetch one larger suffix window and
skip request 2 by containment, §6.4 — that is a conforming alternative,
not "every request" the *baseline* open makes, which is what I answered.)

### R2 — trailer flags = 0x00000004

`0x00000004` is bit 2 (bits are numbered LSB = bit 0, `[R-ENC-08]`), which
lies in bits 0–15, the **incompat lane**. §6.2's trailer table states the
incompat lane's only valid value is "all zero," and §6.3 states flatly
that "In this specification's text no flag bits are defined" — so no
reader of this text implements *any* incompat-lane bit, and any set one
is unimplemented by construction. Outcome class: **reject-file**
(register **F19**, governing rule `[R-CNT-08]`). The file is **not
conforming**: the flags field's own stated valid-value constraint in
§6.2's table is violated (this is a genuine byte-conformance defect, not
one of `[R-CNF-02]`'s writer-conduct carve-outs, which are limited to the
few cases §2.3 enumerates by name and do not include this one).

### R3 — codec 3 (zstd) declared, reader doesn't implement zstd

**Underdetermined by the document** — see Finding readerb-01. Two
things the document does say clearly: (1) codec 3 is an assigned, core
codec value (§17.2, `[R-COD-03]`), so the *file* commits no violation by
declaring it — none of §21's rows fire; and (2) `[R-CNF-03]` requires a
conforming reader to implement all four codecs, so software that cannot
execute zstd "is not a conforming reader" (`[R-COD-11]`) — full stop, an
actor-status statement, not an outcome-class assignment. The document
defines an outcome (`reject-layer`) only for a codec value the file
itself gets wrong (0, reserved, or experimental, `[R-COD-03]`) and a
*verifier's* stance (`cannot establish`) for a codec it cannot execute
(`[R-COD-11]`) — neither is literally this case. By structural analogy
to both of those (and to `reject-layer`'s own definition in §2.4, under
which "a reader MAY still list the file's layers, including the rejected
one's name" and "all other layers are unaffected"), the natural
implementation choice is to treat the layer as unusable and continue
serving other layers and listing this one's name — but the document
never states that binding for *this* actor (a reader, not a verifier)
meeting *this* class of value (assigned/core, not reserved/experimental).
So: outcome class — not stated; reader may still serve other layers —
not stated, though the closest analogy says yes; reader may still list
this layer's declarations — same, not stated, analogy says yes.

### R4 — tile-index entry: extent_offset = sentinel, extent_length ≠ sentinel

(Note on terms: §15.1 names a tile-index entry's two 8-byte fields
`offset` and `length`; `extent_offset`/`extent_length` is the document's
name for a *record's* extent slot, §7.2, a different structure. I answer
for the tile-index entry, which is plainly what's meant.)

This is the "exactly one field at the sentinel" row of §15.3's table:
"offset = S ∧ length ≠ S, or offset ≠ S ∧ length = S" → marked
***structural***: **reject-tile**. Scope: the tile (§15.1: "the owning
scope of an individual entry, and of the stored tile it addresses, is the
tile"). Register row: **T7** (`A tile-index entry sets exactly one of
offset and length to the sentinel value`), detector reader, detected at
tile use, governing rule `[R-IDX-03]`.

### R5 — directory's CRC does not match its bytes

`[R-CNT-11]`: "A reader MUST verify that CRC before any other use of the
region... mismatch: reject-file." Outcome: **reject-file** (register
**F20**). What may the reader still serve: **nothing**. Reject-file means
"A reader MUST NOT rely on any structure in it," and mechanically, the
open's step 4 (the record walk that builds the layer table) never runs
because it depends on the directory bytes the failed CRC has already
disqualified from use (`[R-ENC-10]`: verify before acting). No layer,
tile, or metadata can be reached at all.

### R6 — a file exactly 96 bytes long

96 < 128. §5.1/`[R-CNT-27]`: "No conforming file is shorter than 128
bytes... A reader MUST treat a shorter file as a validity error at file
scope." Register **F5** states this is decided "from F alone... needing
no other byte of the file." So: the reader concludes the file is invalid
at file scope from the physical/transport-reported size (F = 96) alone,
with no other byte read. Outcome class: **reject-file**.

### R7 — interleaved layer, y(12,5) then x(9,4), channels a(uint16) b(uint8), sample (y=6,x=5)

Declared order is (y, x); row-major linearization makes the
**last-declared** dimension (x) vary fastest (`[R-GEO-05]`, `[R-GEO-06]`).

- `G_y = ⌈12/5⌉ = 3`, `G_x = ⌈9/4⌉ = 3`.
- `t_y = 6 div 5 = 1`, `u_y = 6 mod 5 = 1`; `t_x = 5 div 4 = 1`,
  `u_x = 5 mod 4 = 1`.
- Spatial ordinal `s = t_y·G_x + t_x = 1·3 + 1 = 4`.
- Disk ordinal (interleaved ⇒ disk ordinal = spatial ordinal, `[R-GEO-06]`):
  **4**.
- In-tile ordinal `u = u_y·T_x + u_x = 1·4 + 1 = 5` (row-major in-tile
  order is permanent regardless of linearization, `[R-GEO-06]`).
- `Q = B_a + B_b = 2 + 1 = 3` (uint16 + uint8, §12.1); channel `b`'s
  index is 1, so `F_b = Σ_{j<1} Bⱼ = B_a = 2`.
- Channel `b`'s byte offset in the decoded tile image
  (§14.2: `u·Q + Fᶜ`) = `5·3 + 2 = 17`.

(Sanity check: `P = T_y·T_x = 5·4 = 20`; decoded size `P·Q = 60` bytes;
channel `a`'s value at the same ordinal sits at `5·3+0 = 15..16`
(2 bytes), leaving `b` at byte 17 exactly, 1 byte — consistent.)

**Answer: disk ordinal 4; channel b begins at byte offset 17 of the
decoded tile image.**

### R8 — unimplemented top-level record type, MU = 1; vs. same type as a sub-record

Top-level: `[R-CNT-15]` — "An unknown record type at file scope: MU = 1
→ reject-file." Outcome: **reject-file** (this is the MU=1 branch the
register's F35 addresses for the reserved-range instance; the same
MU-gated rule applies to an unassigned experimental-range type per
§10.3, with the caveat from §21.6 that in the experimental-range
instance the *file* remains conforming even though this reader still
refuses it).

As a layer **sub-record** of the same unimplemented type: `[R-CNT-18]` —
"an unknown sub-record type with MU = 1 is reject-layer, and where the
file is otherwise conforming a reader MUST NOT reject the file for it."
Outcome: **reject-layer**, scoped to that one layer; every other layer
is unaffected, and (§2.4's reject-layer definition) the reader may still
list the file's layers including the rejected one's name.

**So yes, it differs, and the difference is exactly file-wide vs.
single-layer blast radius** — the identical "unknown type, MU = 1"
condition is reject-file at the top level and reject-layer as a
sub-record, because the record's *scope* (file container vs. one layer's
sub-record sequence) is what §2.4 hangs the outcome on, not the
type-unknown-ness itself.

---

## 7. Findings

### readerb-01 (AMBIGUITY)

**Summary.** The document defines no outcome class for the case where a
reader's *own* incapacity — not the file's — is the reason a structurally
valid, core/assigned enumerator (a codec, a filter, a channel layout, a
sample type, a metadata encoding, or a registered record type) cannot be
served. `[R-CNF-03]` states only that software failing to implement any
one of these "is not a conforming reader," which is an actor-status
statement, not an entry in §21's outcome vocabulary (reject-file/-layer/
-tile/ignore-record). §17.4 (`[R-COD-11]`) comes closest, but explicitly
addresses a **verifier**'s "cannot establish" stance, and for an ordinary
**reader** at a core value says only that the situation "arises only at a
reserved or experimental value" for a reader that *is* conforming — i.e.
it defines the reader-side outcome only for the case that, by hypothesis
in probe R3, does not obtain (codec 3/zstd is assigned and core, not
reserved/experimental).

**Failure scenario.** Two independently-written "reader" implementations
that both accept every conforming file within §21.9's limits and reject
every file the register condemns, but where one has not implemented
zstd, can diverge on a file carrying a perfectly conforming zstd-coded
layer: one implementation serves every byte the reference array specifies
for that layer; the other refuses the whole file, or refuses only that
layer, or (worse) attempts a partial decode and returns wrong bytes —
the document licenses none of these choices explicitly and forbids none
of them explicitly either, because by `[R-CNF-03]`'s own terms neither
implementation is "a conforming reader" the moment it lacks zstd, so no
requirement written *for* conforming readers is binding on it at all.

**Byte-level test.** Yes: this changes whether a conforming-file's
layer's decoded sample bytes are ever returned at all (served vs.
refused), and at what scope (file vs. layer) a refusal would land if
the implementer nonetheless wants to fail gracefully — exactly the kind
of accept/reject divergence the charter's byte-level test asks about.

### readerb-02 (OBSERVATION)

**Summary.** Register row **F19** (§21.2) states its Condition text over
"the flags incompat lane (bits 0-15)" but its own Instances cell reads
"flags bits 0-7" — narrower than the condition it is supposed to
enumerate instances for. §21.1 states the Instances column "enumerates
what a conformance corpus builds for that row" and that "each instance is
one distinguishable file, covered by at least one vector" — on its face
this cell under-enumerates bits 8–15.

**Failure scenario.** None for a conforming reader's accept/reject
behavior: §21.1 also states "where a row and the rule it cites diverge,
the rule governs," and the governing rule here, `[R-CNT-08]`, is
unambiguous and unqualified across all of bits 0–15 ("MUST reject-file on
any set bit it does not implement in the incompat lane (bits 0–15)").
My own probe R2 answer (bit 2, within 0–7) is unaffected either way. The
practical exposure is narrower: `[R-ERR-02]`'s promise that "every row...
has at least one conformance vector... and at least one vector per
instance" is, on this row's own Instances cell, a promise only about bits
0–7, so a corpus built strictly to the letter of this cell could ship
without a single vector exercising, say, bit 12 — a gap in test coverage
that the row's own text does not flag as a gap (since the cell reads as
complete on its face).

**Byte-level test.** No: it does not change what bytes a conforming
reader accepts or rejects, since the governing rule (not the instances
cell) controls and is unqualified. I flag it as an observation about the
register's internal consistency and corpus-coverage promise, not as a
reader-behavior ambiguity.

---

## 8. Evidence summary (for the structured-output `evidence` object)

- **Sweeps run.** Two `rg` searches against the one target file: (1) a
  count of `committed_file_length` occurrences (18 hits, all on distinct
  table/prose lines, used only to confirm the term wasn't a name I
  mis-copied while reading); (2) a search for the sentinel byte-string
  token `0xFFFF_FFFF_FFFF_FFFF` (3 hits: the defining prose at §15.2 and
  register rows T6/T7), used to locate the exact register rows for R4
  without re-reading the whole §21.4 table by eye a second time. A count
  of `reject-tile` occurrences (19) was a scope check before answering
  R4, confirming the term is used consistently as an outcome-class label
  throughout and not overloaded. All three were **control-verified**
  safe from the hard-wrap pitfall (each hit is a token or table cell that
  sits intact on one physical line — I checked each hit's surrounding
  line by eye).
- **Derived numbers, checked against the document's own stated figures.**
  Grid count `⌈100/32⌉ = 4` vs. document's `entry_count = 4` (match);
  index-region formula `4×20 + ⌈4/65536⌉×4 = 84` vs. document's stated
  extent length 84 (match); inline-payload byte count, summed field by
  field, = 81 vs. document's stated 81 (match); CRC-32C of the 80-byte
  all-sentinel entry array, computed with a from-scratch reflected
  CRC-32C implementation validated first against the document's own
  §4.5 check vectors (`"123456789"` → `0xE3069283`; zero bytes →
  `0x00000000`). The entry-array CRC I computed, `0x80A34955`, matches
  the document's stated *segment CRC* (`55 49 A3 80` little-endian); the
  *second* CRC, of that 4-byte segment-CRC array, computed as
  `0xC4EE982E`, matches the document's stated `crc_of_crc_array`
  (`2E 98 EE C4` little-endian). Both independent computations matched
  the document's stated constants exactly. R7's disk ordinal (4) and channel
  offset (17) were derived from the stated formulas and cross-checked
  by an independent route (computing channel `a`'s offset at the same
  ordinal, 15–16, and confirming it abuts channel `b`'s single byte at
  17 with no gap or overlap, consistent with `Q=3` covering both).
- **Rejected candidates.** I considered flagging the "0x0000000000000001
  measure-zero substitution" language in Appendix G item 2 as an
  ambiguity, but closed it: Appendix G is explicitly non-normative
  ("Reproducible-writer profile (non-normative)") and concerns a
  *writer* convention, not a reader obligation, so it is out of scope
  for a conforming-reader walk and not a document defect either way. I
  also considered whether `[R-CNT-10]`'s "MUST probe separately or fail
  the open" leaves the *outcome class* of a failed-to-obtain-F situation
  undefined (it does not map onto reject-file/-layer/-tile/ignore-record
  by name) — I closed this one as not rising to a reportable ambiguity,
  because it is consistent with, not contradicted by, the document's own
  general treatment of capability refusals as a *separate* axis from
  file-conformance outcomes (§21.6's closing two paragraphs draw exactly
  this line for the format-major and MU=1/experimental cases), so it
  reads as an intentional omission rather than an underdetermined
  byte-level question — no file's bytes are in play at all when a
  transport simply cannot answer a size query.
- **Where confidence is thin.** I did not exhaustively cross-check every
  one of the roughly 120 register rows' Instances cells against their
  Condition text the way I happened to for F19 (readerb-02) — that
  observation surfaced while locating rows for R4/R8, not from a
  systematic pass over all ~277 instances §21.8 claims. A dedicated pass
  over the whole register for this class of cell-vs-condition mismatch
  was out of scope for the time available and is not represented as
  exhaustive.
