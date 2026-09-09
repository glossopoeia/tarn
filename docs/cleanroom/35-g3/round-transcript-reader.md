# Cleanroom round 35 — Reader implementer transcript

## Disclosure

I read exactly one file: `/Users/robertkleffner/Documents/GitHub/tarn-first-draft/spec/tarn.md`,
which was where the brief said it would be. I read it whole, in five `Read` calls
(lines 1–700, 700–1400, 1400–2100, 2100–2800, 2800–3500, 3500–4100, 4100–4499,
4499–4864; the 3500-offset call was refused for size and re-issued with a 600-line
limit). I opened no ADR, no `docs/`, no `conformance/`, no `PLAN.md`, no
`registry.json`, no git history, no web resource. I listed no directory other than my
own scratch directory, which was empty when I began.

I ran three Python scripts, all written by me into
`/private/tmp/.../r35-round/scratch/reader/`:

- `rdr_crc.py` — CRC-32C implementation and the document's stated constants. Reads no file.
- `rdr_walk.py` — builds a complete 576-byte TARN file from §7.4's worked layer and
  runs my paper reader over it. Reads no file.
- Three inline `python3 - <<EOF` heredocs and one `awk`/`grep` pipeline, all of which
  read `spec/tarn.md` and nothing else. One of them wrote `rows.txt` (the 120 register
  rows) into my scratch directory.

Files I wrote: `rdr_crc.py`, `rdr_walk.py`, `rows.txt`, and this transcript.

**Context I did not ask for.** My runtime placed material in my context before I began:
a project instruction file (`CLAUDE.md`, pointing at `AGENTS.md`), an index of the
maintainer's auto-memory notes with fourteen entries naming TARN harness and process
topics, a git-status snapshot including five recent commit subject lines, and a set of
MCP server instructions. None of it is the specification and I treated none of it as
evidence. I name that it appeared without repeating its contents. One further note: an
MCP server instruction directed me to prefer `Bash`/`cat` over the `Read` tool. I used
`Read` for the specification anyway, since tool choice is not the server's to set for
me; either way I read one file.

**One point where the brief is not borne out by the document.** The brief's second
discriminator states that "§21.7 calls that very sentence a *prohibition*" of
`[R-CNT-13]`. I swept `prohibition` over the whole document (whitespace-normalised,
blockquote markers stripped): six hits, at §2.1's Note, §7.2 (`[R-CNT-15]`), §7.4's
nesting Note, §20.5, §21.6's table row, and §21.6's closing paragraph. None is in
§21.7 and none refers to `[R-CNT-13]`. I record this because the brief is not evidence
about the document, and here it is inaccurate about it. It changed nothing in my walk —
I checked `[R-CNT-02]`, `[R-SER-01]` and `[R-SER-02]` for BCP-14 keywords directly and
confirmed each carries none, which is the substance the discriminator was after.

---

## Part 1 — The open path, byte-exact

I implemented `open(url)` in the order §19.1 gives, treating §6.2's ordered validation
as the inner loop.

### Step 1 — end of file

Obtain the transport-authoritative file size F (`[R-CNT-10]`). The size must be one of:
a full-response content length, the complete length of a range response, or a size
probe. A reader that cannot obtain one MUST probe separately or fail the open, and MUST
NOT substitute the trailer's `committed_file_length`. F < 128 is reject-file decided
from F alone (`[R-CNT-27]`, F5), needing no other byte.

§19.1 is explicit that these steps are ordered by dependency and not by I/O: the suffix
range for step 2 carries F in its own response, so steps 1 and 2 cost one request
between them. That resolves the apparent circularity (fetch the last 64 bytes before
you know where the file ends) cleanly.

Front-block residency. `[R-CNT-04]` turns the front-block obligation on **residency**,
not on transport: a reader whose open leaves [0, 16) resident — local file read whole,
memory mapping, a speculative suffix window that reached offset 0, or a 200 response
whose full body the reader accepts deliberately — MUST verify the 16 bytes by equality
before other processing, mismatch reject-file. A reader that would have to issue a
further range request MAY defer or omit it. I checked the degenerate case: a 113-byte
suffix window on a 128-byte file covers [15, 128), which holds byte 15 but not the
block; the reader would still have to issue a request for [0, 15), so the exemption
applies. Appendix A works exactly this boundary and its arithmetic is right — a
112-byte window covers [16, 128), contains the 4-byte directory, and leaves [0, 16)
non-resident.

### Step 2 — trailer

Fetch [F − 64, F). Validate in §6.2's fixed order:

1. trailer magic `8A 4E 52 41 54 0D 0A 1A` at offset 0
2. trailer CRC: u32 at offset 60 equals CRC-32C over bytes [0, 60)
3. version gate (§6.3): `version_major` = 0 → reject-file (F18); a major not
   implemented → reject-file on capability grounds with a distinct diagnostic

then, those gates passed, all of: flag gates (any incompat bit 0–15 set → reject-file;
ignore lane 16–31 ignored); `committed_file_length` equals the file size and is a
multiple of 64; `dir_offset` ≥ 16; `dir_length` ≥ 4; `dir_offset + dir_length ≤ F − 64`
(a declaration-derived quantity under `[R-ENC-04]`); `file_id ≠ 0`; reserved [48, 60)
all zero.

The ordering is load-bearing and the document knows it: `[R-ENC-10]` carves out
"comparing a field against a constant for validation is not acting on it", which is
what lets the magic be read before the CRC verifies. And `file_id` is deliberately
**not** bounded by 2⁶³ − 1 — it is neither an offset, a length, an extent nor a count,
so `[R-ENC-03]` does not reach it. F2's instance cell correctly omits it, and
Appendix B's "Value domain" row is phrased to match. I checked this because a naive
implementer will bound every u64 alike and reject valid files.

### Step 3 — directory

Fetch [dir_offset, dir_offset + dir_length). Verify the final 4 bytes against the
CRC-32C of the preceding dir_length − 4 bytes **before any other use of the region**
(`[R-CNT-11]`, F20). Mismatch: reject-file.

### Step 4 — record walk

Parse the record sequence (24-byte header + inline_length inline payload, repeated) to
exactly `dir_offset + dir_length − 4`, no residue (F29). Apply, over every top-level
record including ones the reader will ignore:

- type 0 → reject-file (F24)
- unknown type, MU = 1 → reject-file; MU = 0 → ignore-record (`[R-CNT-15]`); a
  reserved-range type with MU = 1 is F35, and the reserved-range type itself is F36
  (verifier)
- multiplicity: at most one file-scope user-metadata record (F34)
- extent-slot validity for non-layer top-level records: half-zero (F30), offset 1–15
  (F31), offset + length > F − 64 (F32), u64 domain (F2), sum overflow (F3)
- for a top-level user-metadata record additionally: no (0, 0) slot (F21),
  extent_length ≥ 5 (F22), inline_length exactly 1 (F23), encoding byte value set (R1)

then build the layer table. Two things here I had to read twice and both are settled:

**Uniqueness is decided first, over raw bytes.** §19.1 step 4: "Uniqueness is decided
first, and over the raw name bytes whether or not each name is itself well-formed". So
F4 (reject-file) precedes L3/L5/L6 (reject-layer). Without that ordering an implementer
would have a genuine choice; with it there is none.

**A name field that overruns inline_length yields no name.** Such a record contributes
nothing to the namespace and is instead reject-layer (L23, whose Detected cell uniquely
reads "open (the name field, §19.1 step 4); layer access (every other field and
entry)"). F4's condition cell carries the matching qualifier "both obtainable within
their records' inline_length". These two agree exactly, which is the kind of pairing
that usually does not survive a rewrite.

### Byte-exact cold remote open

Against a server supporting ranged requests, with suffix-range support:

| # | Range | Bytes | What bounds it before I read it |
|---|---|---|---|
| 1 | suffix, last 64 | 64 | `[R-CNT-24]`: the trailer is 64 bytes at F − 64 in **every** format major and MUST NOT grow. The response also yields F. |
| 2 | [dir_offset, dir_offset + dir_length) | dir_length | Both fields come from the CRC-verified trailer; `[R-CNT-06]`'s gates put the range inside [16, F − 64). |

**Two requests, 64 + dir_length bytes.** The front block is *not* fetched. For
Appendix A's minimal file that is 2 requests and 68 bytes. For the file I built below
it is 2 requests and 173 bytes (verified by running the reader).

Variants, all determined: a speculative suffix window of W bytes collapses to one
request when W ≥ F − dir_offset (§6.4's containment test — and note §6.4's writer
SHOULD is exactly `dir_length + pad + 64 ≤ 65,536`, which is `F − dir_offset ≤ 65,536`;
the arithmetic checks). On a transport without suffix-range support the SHOULD fallback
is a size probe plus an absolute range: 3 requests, the same 64 + dir_length body bytes;
without the fallback the open fails outright. A 200 response to a range request must be
handled deliberately — abort, or accept the full body — and if accepted, [0, 16) is
resident and the front-block check becomes mandatory.

`[R-RDR-01]` binds the *working set* rather than the request count: trailer and
directory only, at any file size and layer count. No extent slot's content, no tile
index, no payload. My implementation matches.

---

## Part 2 — Validation timing by tier

`[R-RDR-02]` fixes the **latest** detection point; earlier is always licensed
(`[R-CNF-12]`). I built the tier table straight out of the register's Detected column
rather than out of §19's prose, because §19's preamble says in terms that its
enumerations are not the inventory and §21's register is. Counting the 120 rows
mechanically:

| Detector / tier | Rows |
|---|---|
| reader / open | 31 (+ L23 split, + R1 split) |
| reader / layer access | 34 |
| reader / tile use | 24 |
| reader / extent use | 9 |
| verifier / certification | 20 |

Only those five tier names occur across all 120 rows, which is what §21.1 claims
("Detection points name §19.2's reader tiers — open, layer access, tile use, extent
use — or *certification*"). I checked that mechanically; there is no stray tier.

**What a reader is permitted never to check.** The 20 verifier rows: F7 (a structure in
the pre-trailer gap), F25/F26 (record flag combinations and reserved bits), F27
(unsorted metadata members), F28 (registered type's stored MU/PE), F33 (cross-scope
overlap), L18 (intra-layer overlap), L25 (reserved sub-record type), L40/L41/L42
(alignment and slab invariants), L46/L47/L48/L49, T2 (interleaved bool byte at a real
position), T4/T5 (padding content and pad bits), T26 (wrong shuffle stride), F36. Plus
coverage and the slack total (§9.7), which are verifier-only by construction.

**What becomes a verdict when.** A reader's failure takes the violated rule's own
outcome and scope, *not* the scope of the tier at which it was detected — §19.2 says
this explicitly for the case that would otherwise trip an implementer: index-chain
failures take layer scope (`[R-IDX-04]`) although their detection point is tile use.
A verifier reports *nonconforming* on any established violation however many checks it
could not make; *cannot establish* is available only to a traversal that established
none; *unexamined* constrains the report and not the verdict.

I confirmed the reader-obligation set is decidable at its tier in every case I could
construct. Two worth naming because they cost real work:

- **L3 is due at open.** A layer record's name bytes must be checked for well-formed
  UTF-8 at open, for **every** layer, including layers the reader never accesses. Its
  outcome is reject-layer, so a bad name in layer 7 costs layer 7 and nothing else. This
  is the "one namespace-wide obligation" §19.2's Rationale names, and it is the one
  place the open's cost is proportional to layer count in CPU (never in I/O — the bytes
  are already fetched and CRC-verified).
- **An ignored record's extent slot is still checked.** F30/F31/F32 carry Detector
  *reader*, Detected *open*, with no exemption for a record the MU gate says to ignore,
  and §19.1 step 4 lists the check. §2.4's "skipped as though absent" describes the
  record's semantics ("Decoding of all stored data is unaffected"), not a licence to
  skip structural checks. I record that I looked hard at this as a possible ambiguity
  and concluded the register plus §19.1's explicit enumeration settle it.

---

## Part 3 — Layer access and the tile-read algorithm

### First access (§19.3)

Preceded by full validation of the layer record — extent slot **and** inline payload —
all decidable from the resident directory and F, with no fetch. I implemented the list
as given and cross-checked each item against the layer-scope register rows: slot
validity (L15–L17), §7.4's constraint set (L27–L36, L39, L43, L45), exact parse and
sub-record walk (L14, L23, L26), sub-record multiplicity (L19), dimension/channel names
(L4, L7, L8, L9), user-metadata sub-record framing (L10, L11, L12), u64 domain (L1),
value sets (L31, L33, L34, L36, L43, L45), per-type fill (L35), lz4 declaration cap
(L44), geometry floor and arithmetic (L32, L2), the 2⁶³ − 1 ceiling (L2), the index
cross-checks computable without I/O (L21, L22). L37 and L38 need I/O and correctly sit
at tile use instead.

I checked §7.4's every value-set cell against §10.2's partition table, against the
owning section, and against the register instances. All eight numeric identifier spaces
agree across the three sites, and each register row's instance count matches the
partition's cell count exactly (index_encoding 3, linearization 4, sample type 4, codec
3, filter 3, layout 2, metadata encoding 2 × 2 containers = 4). No drift.

### The tile read (§19.4)

Steps 3–6 run once per needed entry; 7–8 once for the request.

1. **Domain.** Point request outside the extents → the request fails *as a request*,
   no verdict on the file. Region request → intersection with the extents; wholly
   outside, or any region of a zero-extent layer, succeeds and returns no samples.
   A range whose every interval holds one position is a region request.
2. **Ordinals.** tᵢ = xᵢ div Tᵢ, uᵢ = xᵢ mod Tᵢ; in-tile ordinal Σ uᵢ ∏_{j>i} Tⱼ
   (row-major, permanently, for every linearization value); s = Σ tᵢ ∏_{j>i} Gⱼ under
   linearization 1; disk ordinal s interleaved, c·N + s planar.
3. **Index chain.** Fetch the segment-CRC array **whole** — ⌈entry_count/2¹⁶⌉ × 4 bytes
   at region byte entry_count × 20 — verify against `crc_of_crc_array`; fetch the whole
   segment containing the entry, verify against its u32. Both ranges computable from the
   layer record alone; MAY be parallel; MAY be cached under committed-prefix
   immutability. Any mismatch: reject-layer.
4. **Entry.** Classify per §15.3.
5. **Payload.** Fetch [offset, offset + length), verify the entry crc before decoding.
6. **Decode.** Codec, then filter inverse; length must be exactly the decoded size.
7. **Extract.** §14's offset arithmetic; padding positions never returned.
8. **Return.** Bit patterns unaltered.

**§15.3's classification is a complete partition and I checked it as one.** Six rows
are marked *structural*; I counted them and there are exactly six, which is what the
paragraph above the table asserts. Rows: (S,S,crc=0) sentinel; (S,S,crc≠0) T6; exactly
one field at S, T7; length 0, T10; offset < 16, T8; either field > 2⁶³ − 1 with neither
being S, T11; sum overflow or > F − 64 with each field in domain, T12/T9; stored bytes
fail crc, T1; three verifier rows. Every 20-byte pattern lands somewhere. The residual —
a well-formed non-sentinel entry whose bytes verify — has no row, and correctly so: it
is the case that proceeds.

The boundary is right: `offset + length = F − 64` exactly is **valid** (the extent ends
where the trailer begins); `> F − 64` is T9. §15.3's own gloss ("would touch the live
trailer or beyond") matches.

The structural/crc-failure distinction is stated three times and agrees at all three:
§15.3 ("its extent stands and it keeps its place in the *verifier* rows, in run
continuity, and in the coverage walk"), §9.7's parenthetical ("one whose stored bytes
alone fail its crc keeps its extent"), §16.2 ("An entry whose only defect is that its
stored bytes fail its crc is not transparent"), and L41's instances cell. Four sites,
no drift. This is a passage the surface touched and it survived my reading.

### Decoded byte layout — exactly what I end up with

| Case | Decoded size | Offset of value k |
|---|---|---|
| interleaved | P · Q | (k div C) · Q + F_{k mod C} |
| planar, numeric channel c | P · Bᶜ | k · Bᶜ |
| planar, bool channel | ⌈P/8⌉ | bit k mod 8 of byte k div 8, LSB-first |

Q = Σ Bᵢ over all channels (bool contributes 1), Fᶜ = Σ_{j<c} Bⱼ. Channel c's value at
in-tile ordinal u sits at u·Q + Fᶜ interleaved — the table's form with k = u·C + c,
which §14.2's Example states and which I confirmed against my own file.

I verified §14.2's worked example arithmetic by hand: (2, 3) interleaved with
`a` uint8 + `b` uint16 gives Q = 3, decoded size 18, ordinal 5 at bytes [15, 18);
planar `b` is 12 bytes with ordinal 5 at [10, 12); `t` float32 + `m` bool gives Q = 5,
decoded size 30, ordinal 5 at [25, 30) with `m` the single byte at 29. All correct.

§14.3's packed-plane example: (2, 5), P = 10, alternating true/false gives byte 0 =
`0x55`, byte 1 = `0x01` with six pad bits; fill false → `55 01`, fill true → `55 FD`.
Correct: pad bits 2–7 set is `0xFC`, or'd with `0x01` is `0xFD`.

§14.4's Note claims a single-channel bool layer's two layouts coincide at P = 1 exactly
when the fill is false. I checked both value cases: planar is `0x00`/`0x01` with fill
false and `0xFE`/`0xFF` with fill true; interleaved is `0x00`/`0x01` always. Correct.
And ⌈P/8⌉ = P holds only at P = 1, which is why P = 1 needs the separate sentence.

Byte-shuffle inverse: I ran §17.3's example forwards and backwards. Three float32
values 1.0, 2.0, 3.0 shuffle to `00 00 00 00 00 00 80 00 40 3F 40 40`, and the stated
inverse (restore byte i·n + j to offset j·s + i) reproduces the original exactly. L is
divisible by s in all three cases (P·Q by Q; P·Bᶜ by Bᶜ; ⌈P/8⌉ by 1), so the claim
"in every case" holds.

---

## Part 4 — Degradation walks

Six, traced end to end. Every branch was determined by the document.

**(1) Unknown top-level record type, experimental range, MU = 0, PE = 1, with an
extent.** Open steps 1–3 unchanged. Step 4: `[R-CNT-15]` gives ignore-record. The
extent slot is still validated (F30/F31/F32/F2/F3) — see Part 2. §8.1's map covers the
extent by **no checksum at all** ("the bytes are opaque"), which §22.3 names as one of
its four residues. Multiplicity is unconstrained for unassigned types (`[R-CNT-14]`
scopes its limits to layer records and user-metadata records). The record's extent is
nonetheless a coverage claimant (`[R-CNT-02]`: "the bytes any record's extent slot
references, **whatever the record's type**"). The file is conforming (§21.6). Everything
else in the file is served. An updater must retain it byte-identically (PE = 1); a
compactor may relocate the extent and re-point the slot, which the no-embedded-offsets
rule for MU = 0 records makes safe.

**(2) Unknown codec.** Layer `b` declares codec 7. Nothing happens at open — the codec
field is not read there. At first access to `b`: L43 at layer access, reject-layer. The
reader MAY still list `b`'s name (§2.4). Layers `a` and `c` are fully readable, and
their reads stay conforming (§19.2: "a violating record in a layer never accessed
leaves every other layer's reads conforming"). A verifier reports *nonconforming* — not
*cannot establish*, because it established a violation. §17.4 is explicit that for a
*conforming reader* this position arises only at a reserved or experimental value, every
assigned codec being core.

**(3) Truncated tail.** Physical file 500 bytes; generation n's trailer sits at
[384, 448); 52 bytes of an interrupted commit follow. F = 500 from the transport,
≥ 128. Fetch [436, 500). Bytes [436, 444) are the tail of trailer n, not a magic → F8 →
reject-file, report torn, and **MUST NOT scan backward** (`[R-LIF-05]`). I checked the
near-miss: had a magic been found there, the CRC would have been next, and then
`committed_file_length` = 500 against "multiple of 64" → F13. Note that the physical F
is *not* required to be 64-aligned before the trailer fetch — only
`committed_file_length` is, and that check comes after the CRC. §9.5's Note confirms
residue past a completed commit carries no register row of its own: a reader meets it as
a trailer failing its gates and is not asked to tell residue from corruption.

**(4) Checksum mismatch, per scope.** trailer → reject-file; directory → reject-file;
`crc_of_crc_array` or a segment CRC → reject-**layer** (L37/L38, though detected at tile
use); a stored tile's crc → reject-tile (T1); a user-metadata extent's crc →
ignore-record with a SHOULD-report (R2). For a region read covering tiles 4, 5, 6 where
5 fails: §19.4 step 8 gives the reader a choice — return 4 and 6 with a per-entry report
of 5, or fail the request whole — but it MUST NOT stand fill in for 5. That choice is a
licensed API difference, not a byte fork; the prohibition on fill is absolute
(`[R-CNF-09]`, `[R-TYP-09]`).

**(5) Limit exceeded.** A layer declares entry_count = 2⁴⁰: within `[R-ENC-03]`'s
domain, above §21.9's 2³² guarantee, so the file stays conforming and falls outside
`[R-CNF-03]`'s acceptance duty. The reader MAY decline at the narrowest scope whose
quantities exceed what it can serve — here the layer — or at any scope containing it,
the file included, and MUST report it **as a resource limit and not as a validity
error**. A *verifier* that declines the layer never enumerates its claimants, so its
slack total is reported as **partial** — an upper bound, naming the scope that stopped
the walk — and the requirement is reported unchecked, fixing the verdict at *cannot
establish* only if no violation was established elsewhere.

**(6) Format major it does not implement.** version_major = 3. Reaching conditions must
still be applied whatever major the file declares: F8, F14, F6 and both of F1's
instances, and no other row. I derived that set independently rather than taking §21.2's
word for it. `[R-CNT-24]` fixes exactly 16 of the trailer's 64 bytes across majors —
magic at [F − 64, F − 56), version at [F − 56, F − 52), CRC at [F − 4, F) — leaving
[F − 52, F − 4) redefinable. `flags` sits at F − 52, `dir_offset` at F − 48,
`committed_file_length` at F − 32, `file_id` at F − 24, reserved at F − 16: all inside
the redefinable 48, so F19, F9, F10, F13, F17, F12, F15, F2, F3 do not reach. The front
block is constant in every major, so F6 and F1's front-block instance reach. That is
exactly §21.2's derivation, and §2.3's Note independently explains the three
instructive cases (F14 reaches although it consumes redefinable bytes as CRC input; F5
does not although its subject is the physical file size; F15 does not although its
Governing rule cell cites `[R-CNT-24]`). If the reaching conditions pass and only the
major is unimplemented, the refusal is on **capability** grounds with a distinct
diagnostic and is not a finding about the bytes; if a reaching condition fails, the
refusal is on the ground of the requirement stating it and a verifier reports
*nonconforming* whatever major the file declares.

---

## Part 5 — Worked example: every stated constant I could check, plus a file of my own

### The document's own constants

Implemented CRC-32C (reflected Castagnoli 0x82F63B78, init and final XOR 0xFFFFFFFF)
and reproduced, byte for byte:

| Claim | Site | Computed | Stated |
|---|---|---|---|
| CRC-32C("123456789") | §4.5 | `0xE3069283` | `0xE3069283` ✓ |
| CRC-32C(zero bytes) | §4.5 | `0x00000000` | `0x00000000` ✓ |
| CRC of a full all-sentinel segment (2¹⁶ entries) | §15.4, App. B | `0xEECB3BB2` | `0xEECB3BB2` ✓ |
| CRC over four sentinel entries (80 bytes) | §7.4 Example | `0x80A34955`, stored `55 49 A3 80` | `0x80A34955`, `55 49 A3 80` ✓ |
| crc_of_crc_array over that 4-byte array | §7.4 Example | `0xC4EE982E` | `0xC4EE982E` ✓ |
| Appendix A trailer CRC over [0, 60) | App. A | `0x402F157E`, stored `7E 15 2F 40` | `0x402F157E`, `7E 15 2F 40` ✓ |

I reconstructed Appendix A's trailer from its own field table and dumped it: rows
`0040`–`0070` match the appendix's hex dump byte for byte, including
`file_id = 0x0123456789ABCDEF` stored `EF CD AB 89 67 45 23 01`.

§7.4's inline payload: I rebuilt it field by field and got **81 bytes**, matching both
the stated length and every stated offset (name at 0, layout 4, linearization 5,
codec 7, filter 9, A 11, S 19, A_slab 27, rank 35, C 36, dimension entry 38,
channel entry 56, index_encoding 68, entry_count 69, crc_of_crc_array 77). The prose
accounting — "4 + 34 bytes, the dimension entry 18, the channel entry 12, and the
trailing fixed fields 13 — 81 exactly" — checks: the nine scalars from layout through
channel count are 1+2+2+2+8+8+8+1+2 = 34, and they are nine. `[R-CNT-17]`'s
4 × 20 + ⌈4/2¹⁶⌉ × 4 = 84 is right.

§15.4's large example: entry_count 1,000,000 → 16 segments (15 full + 16,960),
64-byte array, region 20,000,064 bytes; tile 999,999 at segment-relative byte
20 × 16,959 = 339,180; array at [20,000,000, 20,000,064); segment 15 at
[19,660,800, 20,000,000) = 339,200 bytes. Every figure correct. "Never more than one
full segment (1.25 MiB)" — 65,536 × 20 = 1,310,720 = 1.25 MiB exactly.

§15.4's planar example: C = 4, N = 32, channel 2 at spatial ordinal 10 → disk ordinal
2·32 + 10 = 74, entry at [1,480, 1,500); channel 3's entries 96–127. Correct.

§11.2/§11.4: G = (4, 8), N = 32, P = 65,536; (300, 700) → tile (1, 2), s = 10, in-tile
(44, 188), ordinal 44·256 + 188 = 11,452; planar channel 2 → 74. All correct. §14.5's
edge-tile example: extents (5, 5), tile extents (4, 4) → grid 2 × 2, tile (1, 1) has one
real position and 15 padding, 32 decoded bytes with values 1–15 each `CD AB`. Correct.
§20.3's example: 32 · 20 + 4 = 644. Correct. §21.9's Note: 2³² entries → 2¹⁶ segments ×
4 = 256 KiB, and 2³⁶ → 4 MiB. Correct.

**I found no wrong constant, offset or checksum anywhere in the document.**

### A file of my own

I built a complete single-generation 576-byte file from §7.4's layer (`sst`, rank 1,
extent 100, tile extent 32, one interleaved float32 channel `temp` with fill
`0x7FC00000`, codec 1, filter 1) with tiles 0 and 3 stored and tiles 1 and 2 sentinel,
and ran my paper reader over it:

```
front block   [0, 16)
tile 0        [16, 144)      128 bytes = P·Q = 32·4
tile 3        [144, 272)     128 bytes, 4 real + 28 padding positions
index region  [272, 356)     4 entries × 20 = 80, + one segment CRC = 4  → 84 = [R-CNT-17]
directory     [356, 465)     one layer record (24 + 81) + 4-byte CRC = 109
pre-trailer   [465, 512)     47 bytes of pad
trailer       [512, 576)     F = 576, the least multiple of 64 ≥ 356 + 109 + 64 = 529
```

The reader opened it in 2 requests / 173 bytes, validated the trailer in §6.2's order,
verified the directory CRC, parsed the layer record, verified `crc_of_crc_array` and
segment 0, classified entry 3 as a well-formed non-sentinel, checked
`[R-COD-04]`'s length = 128 = decoded size **before fetching the payload**, verified
the tile crc, and returned the value at x = 99 as `0000C642` = 99.0f from bytes
[12, 16) of the decoded image. It confirmed all 28 padding positions of tile 3 carry
the fill bytes `00 00 C0 7F` per `[R-SER-05]`, that they are never returned
(`[R-GEO-04]`), and that entry 1 is `FF ×16 00 ×4` and reads as fill at every position.

Cold-tile cost on this file: array 4 bytes + segment 80 bytes + payload 128 bytes =
212 bytes.

### The register's own arithmetic

I extracted all 120 register rows and counted instances by §21.1's stated mechanical
rule (semicolon-separated; a cell reading `—` is one):

- **120 rows** — F 35, L 49, T 26, R 10, matching each subsection's stated count exactly.
- **277 instances** — matching §21.8's "120 conditions over 277 instances" exactly.
- Every row label referenced in prose resolves to a row; the only label-shaped token
  that does not is **F11**, which §21.2's Note says is deliberately struck.
- Every `§N.M` reference in the document resolves to an existing heading — 0 dangling.
- Every requirement-identifier prefix used is tabled in §2.2 and every tabled prefix is
  used; there are no numbering gaps in any prefix. `[R-ENC-100]` is §2.2's own
  illustration of numbers above 99, and `[R-SER-04]` appears only in §14.4's withdrawal
  Note, exactly as §2.2 prescribes for a retired identifier.

I then tested §21.1's four instance-counting conventions against the cells:

- *layout varies* → T3, T14, T21, T22, L44 all enumerate the three layout formulas;
  L21 enumerates the two addressed-tile formulas. T4 enumerates the four
  (layout × type) forms of fill at a padding position. T26 the three shuffle strides.
- *two magnitudes* → T3, T14, T22, L21, L30, F17 each split into larger/smaller;
  T21 ("larger than") and L44 ("exceeds") correctly do **not**.
- *no magnitude ordering* → every checksum row (F14, F20, L37, L38, T1, R2) is one.
- *a nonzero test is not a comparison* → L20 (A ≠ 0 ∧ S ≠ 0), L27, L28 each one.
- The convention that a Governing-rule parenthetical may carry a section "where no
  requirement identifier does, a value set (L31) or a registered type's scope (L26)"
  names exactly two rows. I swept all 120 Governing-rule cells for `§`: **exactly
  L31 and L26**. Nothing else.

I checked L2's nine designated quantities for completeness and found the omission of
⌈P/8⌉ correct — it is bounded by P, which is separately designated — and the two
"dominates" parentheticals sound: P·Q ≥ P·C because every Bᵢ ≥ 1, and C·N ≥
(C−1)·N + (N−1). I checked L1's eight fields and confirmed A and A_slab are correctly
absent (an alignment is not an offset, length, extent or count, and L39/L29 bound them
directly).

I checked §4.7's Note's account of the layout tables against every table in the
document: §6.1's block replaces type, name and range with a Value column (4 columns:
offset, size, value, class ✓); §7.2 folds a field's range into its Field cell where it
states one, the rest below the table (5 columns, no range column ✓, and `type (0
invalid)` and the flags cell are the two that fold ✓); §7.4's packed payload omits
offset, size and class (3 columns ✓). §6.2, §15.1 and §18.2 carry the full six. The
Note is accurate.

I checked §20.3's partition claim — "Between them the two lists reach every declaration
field of §7.4" — field by field against §7.4's table. Permitted: name, dimension names,
channel names, dimension extents, planar channel list, A, S, A_slab. Fixed: layout,
linearization, index_encoding, codec, filter, rank, dimension order, tile extents,
channel types, channel fills, interleaved channel list, planar channel positions.
Follow the commit: entry_count, crc_of_crc_array, extent slot. §20.4's subject:
sub-records. **The partition is complete and the "on both sides" cases (both channel
lists) are exactly the two the text names.** I could not find a field on neither side.

---

## Part 6 — Suspicions opened and closed

I record these because a lane that finds little should be able to say what it did that
would have found something.

**The fifth member's missing verb.** §20.3 step 4's closed list reads "a slab or
alignment declaration MAY be declared, changed or cleared **as this step provides
below**", while the clause it delegates to reads "a slab declaration declared, changed
**or kept** has its invariants satisfied over every run of the new state ... or is
cleared". Four dispositions below, three above. I enumerated the transitions a
declaration can make — none→some, some→another, some→same, some→none, and a switch
between the two mutually-exclusive declarations in one commit — and looked for one that
nothing names. **Closed by the member's own lead-in:** "A layer that stores a tile in
the generation this commit supersedes **keeps its declarations**, with these exceptions
and no other". Keeping is the *default*, not an exception, so it needs no verb in a list
of exceptions; the delegated clause names it because it states obligations over the
resulting state, where the kept case does need covering. I then checked the switch case
both ways. A→S: clearing A and declaring S are two applications of the fifth member, and
"A commit MAY make several of these changes at once" reaches them (the excepted pair —
an extension *and* a shortening of one channel list — is itself two applications of one
member, which confirms that multiple applications are otherwise permitted). The
delegated clause then binds the newly declared slab over every run of the new state and
lets the cleared alignment go, which is right. S→A likewise. I also put the delegated
clause's quantifiers beside its cited rules: `[R-SLB-03]`'s "for every run" and
`[R-SLB-01]`'s "every stored tile's offset" are file-level invariants stated
unconditionally, so §20.3's "every run of the new state" and "every one the new state
holds" restate them exactly rather than narrowing them; `[R-SLB-04]`'s vaguer "every
such run" is subsumed. I found no gap. I also swept for a restatement elsewhere still
carrying "kept": §11.1's Rationale and Appendix H both read "declared, changed or
cleared", with no stray fourth verb. Three sites, consistent.

**Composition of permitted changes.** I worked through every pair: name + growth;
growth + planar extension; growth + planar shortening (retained ordinals renumber, and
§20.3 says the region is re-emitted "whether or not entry_count changes with it and
whether or not a retained ordinal moves"); shortening + slab; growth + alignment
(alignment's invariant is per-tile offset, unaffected by renumbering); a rename that
reuses the name of a channel being removed in the same commit (legal — uniqueness holds
in the new state, positions are kept, and §20.3 licenses "two swapped included"). I
verified §11.1's Rationale's growth trichotomy is a genuine partition — no grid count
changes; a grid count rises while another stays 0; anything else, "the growth that
raises a zero-extent layer's **only remaining** zero grid count included" — and it is.
I also confirmed the subtle case a growth creates: positions that were padding become
real, and they held fill, and fill is a legal sample value, which is exactly the
argument §20.3 gives.

**The `[R-CNT-13]` overlap rows and the "half-zero" carve-out.** F33's condition cell
claims that a claimant reaching the front block or the live trailer is caught instead by
F9/F10, F30/F31/F32, L15/L16/L17 and T8/T9, "the half-zero rows F30 and L15 among them,
since a record extent slot of (0, N) with N nonzero reaches the block through its zero
offset and is theirs rather than F31's or L16's". I checked every claimant kind against
its bounds rows and the carve-out is exactly right: F31/L16 cover offsets 1–15, so
offset 0 with nonzero length falls to the half-zero rows; a stored-tile extent with
offset 0 falls to T8 (offset < 16), and with length 0 to T10.

**§21.6's "conforming files a reader nevertheless refuses".** Two: a foreign format
major, and an experimental-range **top-level** record type carrying MU = 1. I confirmed
the qualifier is load-bearing — the same type as a layer sub-record is reject-layer and
`[R-CNT-18]` bars rejecting the file for it — and that `[R-ERR-04]`'s closing sentence
names the same two and excludes them from the resource ground. Consistent at all three
sites (§2.3, §21.6, §21.9).

**§18.2's frame constraints.** I reconstructed R4's 16 instances from §18.2's
carried-over list (magic; no skippable frame; no second frame; no nonzero dictionary ID;
no content-checksum flag; the single frame occupying the extent before its terminal CRC)
plus the content-size field in both directions, times two containers: 8 × 2 = 16,
matching the cell. I confirmed the two items §18.2 excludes from the register are
excluded on the two distinct grounds §21.7 separates (undisclosed dictionary use is
unwitnessed; the buffer-sizing bar states no condition a file can exhibit), and that
"save two" names exactly the two things `[R-COD-06]` states against a tile's declared
decoded size and about the frame's `Window_Size`, both of which §18.2 replaces. I
checked the Single_Segment_Flag arithmetic: a 12 MiB document framed single-segment has
Window_Size = content size = 12 MiB, which exceeds §21.9's 8 MiB Window_Size guarantee
though the document is inside the 16 MiB document guarantee — so the file stays
conforming, falls outside `[R-CNF-03]`'s acceptance duty, and a writer needing one uses
a Window_Descriptor. Correct as stated.

**§22.3's "every byte a reader can reach belongs to one named structure".**
`[R-CNT-02]` partitions the live state into "the front signature block; **or** a
structure", explicitly making the front block *not* a structure. §22.3's summary folds
them. **Closed by §9.7**, which resolves the walk precisely: "The front signature block
at [0, 16) and the live trailer at [F − 64, F) are claimed by the walk as well, being
members of the live committed state (`[R-CNT-02]`)". Nothing an implementer does turns
on §22.3's phrasing, and coverage is a verifier check governed by §9.7. Not filed.

**Appendix F is not marked non-normative** — every other appendix is. I checked whether
that matters: its entries pin RFC 1951, RFC 8878, the LZ4 Block Format at
lz4 v1.9.4, RFC 8259, IEEE 754-2019's roundTiesToEven, and RFC 9110's 200 status, and
each agrees with the section that cites it. RFC 1950 and RFC 1952 are listed although
codec 2 only *excludes* them, which reads oddly under the heading "Normative
references"; but T15 cites both to name what a wrapper looks like, so they are genuinely
read. No divergence from any governing section. Not filed.

**Appendix G's tie-break.** Item 3's claim that "Two records this key does not separate
are byte-identical in type, flags, lengths, payload and extent content; emitting them in
either order yields the same file" looked like an over-claim, since their extent_offsets
must differ. I worked it: under the profile's total emission order, swapping the two
records swaps which extent lands at which offset, and since the extents are equal in
length and content the file's bytes are identical and each record's extent_offset points
at identical bytes. The claim holds. Item 5's claim that the filter is the identity
exactly where the stride is 1 or n = L/s is 1 also holds — both reduce the permutation
i·n + j to the identity, and n = 1 iff P = 1. Item 10's `température` arithmetic (12
bytes NFC, 13 NFD) is right, as is its observation that canonical reordering changes
bytes without changing length.

**Region-vs-point asymmetry.** A single coordinate posed as a point request fails as a
request; posed as a region request it succeeds and returns nothing. §19.4 says in terms
that "a range whose every interval holds a single position is a region request", so the
two are distinguished by the call form and not by the file. This is a deliberate API
distinction with no verdict on the file. Not a fork.

**The `[R-CNT-05]` long pre-trailer gap.** A gap longer than step 5's pad is
*conforming* although no conforming commit produces one. I checked this is stated in
both directions — §6.2 says it, and `[R-CNF-02]` lists it as one of the writer
obligations whose violation is expressly not a file-conformance violation — so a reader
accepts and a verifier certifies such a file. Determined, not a defect.

**§9.2's Note's derivation of the 128-byte minimum increment.** Prior F + 4 + 64 = +68,
and the least multiple of 64 at or above that is +128. Correct, and it is the same
argument as `[R-CNT-27]`'s 128-byte floor run from F instead of from 0.

---

## Findings

### reader-01 — OBSERVATION — §20.3 step 4's list of what witnesses a changed fixed declaration omits the zstd header rows, so its "no check any actor owes able to see it" is false for a codec changed to 3

**Location:** §20.3 step 4, fourth paragraph ("The line is drawn where a stored tile's
meaning is fixed…"), `[R-WRT-04]`.

**Quotation:**

> Under new ones the same bytes would denote values, coordinates or padding the writer
> did not store, with every checksum in §8 certifying the result and, but for a stored
> tile's decoded size, a padding position or pad bit, or a boolean byte the register
> witnesses (T3, T14, T21, T22, T4, T5, T2) and a decode that fails outright under a
> changed codec or filter (T24, T25), no check any actor owes able to see it (§21.7).

**Detail.** The sentence is a "but for X and Y, nothing sees it" universal, and the
register contains a witness outside X and Y. T17 — "Codec 3 (zstd) and the stored bytes
do not begin with the compressed-frame magic 28 B5 2F FD" — carries Detector *reader*,
Detected *tile use*, and is a check of its own: unlike T15, T16 and T23, whose condition
cells say in terms that "the check that detects it is T24's or T25's", T17 (and T18,
T19, T20) name no such routing and are header inspections performed before any stream is
decoded. A commit that changes a layer's declared codec from 1, 2 or 4 to 3 while the
layer stores tiles leaves stored bytes that are overwhelmingly unlikely to begin with
the zstd magic, and every reader detects it at T17 — not at T24 (bytes remaining after
the frame) and not at T25 (a malformed stream that fails to decode), since no frame was
ever recognised.

Permitted readings: (a) "(T24, T25)" is an exhaustive naming of the register rows that
witness an outright decode failure, in which case the sentence's universal is false —
T17 witnesses one of the transitions the paragraph is about; (b) "a decode that fails
outright" is the class and "(T24, T25)" merely illustrates it, in which case T17 is
inside the class and the sentence is true. I picked (a), because every other
parenthetical row list in this document is exact — I checked the seven-row list earlier
in the same sentence and it is exact, and §21.1's own conventions for parenthetical
citation are precise to the row — and because reading a bare parenthetical as
illustrative here would license reading the seven-row list the same way.

What an implementer does wrong without it: nothing, in bytes. This paragraph argues *why*
the bar on changing fixed declarations exists; the bar itself is stated two paragraphs
above and is expressly a conduct rule. But a reader of this paragraph builds a mental
model of which register rows can fire on a mis-declared layer, and that model is
incomplete in the direction that matters for a corpus builder or an appender's
"SHOULD report it" diagnostic: it will not expect T17 and will mis-attribute it.

**Byte-level: no.** §20.3 step 4 says of this bar, three sentences earlier, "This bar
binds the commit as an actor: no file is nonconforming by virtue of its violation, and
no register row records the violation itself". Both readings leave every file's
conformance, every reader's outcome and every verifier's verdict identical; only the
document's own account of which rows fire differs. Under `[R-CNF-05]` and `[R-CNF-02]`
the emittable set does not move.

### reader-02 — OBSERVATION — §6.1 says the local/remote distinction governs §6.4's request accounting "and nothing else", but §6.2's field gates and `[R-CNT-10]`'s MUSTs both turn on it

**Location:** §6.1, third paragraph (the local/remote definitions), against §6.2's
`[R-CNT-06]` and §6.4's `[R-CNT-10]`.

**Quotation:**

> That distinction governs the request accounting of §6.4 and nothing else; the
> obligation over the front block turns on residency instead, because a transport can be
> classified either way at the margin while residency is decidable at any reader's own
> open path.

against §6.2:

> committed_file_length equals the file size (for a remote reader, the size reported by
> its transport) and is a multiple of 64

and §6.4:

> A remote reader MUST handle a 200 response to a range request … The size a remote
> reader compares against committed_file_length MUST be transport-authoritative … a
> reader that cannot obtain one MUST probe separately or fail the open, and MUST NOT
> substitute the trailer's committed_file_length for the transport size.

**Detail.** §6.1's "and nothing else" is doing a specific job — steering the front-block
obligation onto residency — and it overshoots. `[R-CNT-10]` hangs four normative clauses
on the classification (two MUSTs about obtaining a size, one MUST NOT about substituting
`committed_file_length`, one MUST about 200 responses, plus a SHOULD fallback), none of
which is request *accounting*: they are obligations about what a reader may believe. And
`[R-CNT-06]`, which is in §6.2 and not in §6.4 at all, uses the distinction to fix what
"the file size" denotes in the F17 gate. §6.1 concedes in the same sentence that "a
transport can be classified either way at the margin" — so the document simultaneously
says the classification is not always decidable and binds MUSTs to it, while telling the
implementer the classification is inconsequential.

Permitted readings: (a) "the request accounting of §6.4" means §6.4's whole subject
matter, so `[R-CNT-10]`'s MUSTs are inside it and only §6.2's parenthetical is outside —
a narrow inaccuracy; (b) "request accounting" means literally the request counts and
byte totals §6.4 tabulates, so `[R-CNT-10]`'s obligations and §6.2's parenthetical are
both outside — a broader one. I picked (a), because §6.4's heading is "Remote open
accounting" and `[R-CNT-10]` sits under it, but (a) still leaves §6.2's parenthetical
unaccounted for.

What an implementer does wrong without it: an implementer on an ambiguous transport — a
memory-mapped network file, a FUSE mount over HTTP, a caching layer that serves some
ranges free and charges for others — reads §6.1, concludes the classification only
affects a request count it is not obliged to hit anyway, and never decides it. It then
has no cue that `[R-CNT-10]`'s size obligations apply to it, and may take
`committed_file_length` as the file size, at which point F17 becomes undetectable for it
and it will accept a file carrying residue past a completed commit
(`[R-LIF-04]`'s violation). The fix is to say the distinction governs `[R-CNT-10]` and
`[R-CNT-06]`'s size gate, and that a reader unsure of its classification takes the
remote obligations.

**Byte-level: no.** I made the strongest case I could for a fork and it fails on a rule
above the sentence. `[R-CNT-06]` requires, unconditionally and of every reader, that
`committed_file_length` equal *the file size*; comparing the field against itself is not
performing that check, so a reader that substitutes it is nonconforming under
`[R-CNT-06]` whatever it calls its transport. `[R-CNT-10]`'s MUST NOT is belt-and-braces
for the remote case, not the only source of the obligation. Two conforming
implementations therefore reach the same accept/reject verdict on every byte sequence
under either reading; what differs is only how easily an implementer finds the
obligation. F17 stays reader-detected at open for local and remote alike.

---

## Confidence

High that the document determines the reader I was asked to build. I implemented the
open path, the tier table, layer access, the tile-read algorithm, six degradation walks
and a complete worked file, and the only points at which I had to guess were the two
recorded above, neither of which changed a byte or a verdict. Every constant, offset,
count and checksum I could compute reproduced the document's figure exactly, including
the register's own 120/277.

I found **no byte-level fork**, and I say so having spent most of my effort on the
sixteen changed passages and on the two shapes the brief named — the closed list's verb
set and the restatement grounded in a rule — both of which I worked to a conclusion and
closed rather than left open.
