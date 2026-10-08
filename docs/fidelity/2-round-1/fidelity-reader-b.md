# Reader-implementer walk — edition B — working transcript source

## Disclosure

I read exactly one file: `/Users/robertkleffner/Documents/GitHub/tarn-first-draft/spec/tarn.md`
(4,847 lines). I read it with `sed -n` in ~300-line windows, in order, start to
finish, plus one `grep -n` call to locate section headers (`^### `, `^#### `,
`^## Part`) so I could navigate accurately. I opened no other file under any
path, ran no `git` command, did no web search or fetch, and did not list any
directory other than my own scratch directory (to check for a prior attempt's
leftovers — it was empty).

I ran local Python (no file I/O save writing my own scratch outputs) to:
implement and self-check CRC-32C against the document's own check vector
(`"123456789"` → `0xE3069283`, zero bytes → `0x00000000`) and its all-sentinel
segment constant (`0xEECB3BB2`); reproduce the §7.4 worked example's stated
segment CRC (`0x80A34955`) and `crc_of_crc_array` (`0xC4EE982E`) from the raw
bytes the document specifies; compute the grid/ordinal/byte-offset arithmetic
for probe R7; and assemble a complete, byte-exact 320-byte conforming file
around the §7.4 "sst" layer example, computing its directory CRC and trailer
CRC. All of that is in `/private/tmp/.../scratch/walk-reader-b/` — none of it
read anything besides values I typed in from the spec text.

**Context that arrived unasked.** Before I did anything, my context already
contained a project `CLAUDE.md` pointer, a user memory index with many
TARN-related note titles, a git-status block naming recent commit subjects on
a branch called `readable`, and assorted session/environment boilerplate.
None of that is the specification and none of it is evidence about the
specification; I have not opened, searched for, or relied on any of it, and I
am not repeating its contents here. The one file named in the brief is the
only text this walk is built from.

**Path check.** The brief told me to read
`/Users/robertkleffner/Documents/GitHub/tarn-first-draft/spec/tarn.md`. That
file exists at exactly that path, and I read it from there. I did not check
whether other copies of this specification exist elsewhere, as instructed.

## Stance

Per `[R-CNF-01]`, I have treated as non-normative: §1 (Introduction), and
every passage explicitly labeled **Note**, **Example**, or **Rationale**
(by its bold marker, not by content shape — an unlabelled blockquote is
normative, e.g. the §2.1 "Note" box is labeled, but ordinary indented
quotation-style running text that carries a bracketed `[R-...]` tag is a
normative requirement wherever it appears, including inside list items and
table rows). Appendices are not reached by this walk at all (out of scope:
only one file was read, and no appendix content was needed by the probes or
the charter).

---

## PART A — The open path (every byte fetched from cold, in order)

Scenario: remote reader, ranged-request transport that discloses each
response's complete length.

**Step 0 — nothing fetched yet.** No byte is read before the reader decides
how to obtain F. §19.1 step 1 and §6.4 govern.

**Request 1 — suffix range for the final 64 bytes.**
Issued as a byte-range request for the *last* 64 bytes (a suffix spec; the
client need not know F to issue it). The transport's response discloses the
complete resource length, which becomes the transport-authoritative file
size F (`[R-CNT-10]`, §6.4: "(1) Fetch the final 64 bytes, a suffix range,
and validate per §6.2–§6.3. Where the transport discloses a range response's
complete length, that response also carries the transport-authoritative file
size F, so §19.1's first two steps cost one request between them"). Range:
`[F−64, F)`. Bytes: 64.

Over those 64 bytes, before anything else, the reader validates in the fixed
order §6.2 states and §19.1 step 2 restates: trailer magic → trailer CRC →
version gate → the remaining field gates (flags, `committed_file_length`
against the just-obtained F, `dir_offset ≥ 16`, `dir_length ≥ 4`,
`dir_offset + dir_length ≤ F − 64`, `file_id ≠ 0`, reserved bytes zero)
(`[R-CNT-06]`, `[R-CNT-07]`, `[R-CNT-08]`). This is also where `F < 128`
would have been caught even before fetching anything (`[R-CNT-27]`), and
it is moot here since the suffix fetch already presupposes F ≥ 64; the
real floor check is against the F the response disclosed.

The front signature block, bytes `[0, 16)`, is **not** fetched by this path:
nothing above required it, the reader's open is anchored at the trailer, and
the front block is excluded from §6.4's two-request accounting unless the
reader's open otherwise left those bytes resident (`[R-CNT-04]`, `[R-RDR-01]`:
"its I/O is §6.4's request accounting... at any layer count and file size").
A reader is free to also speculatively fetch `[0,16)` as a third request and
check it (`[R-CNT-04]`'s byte-equality obligation then binds), but nothing in
the brief's scenario requires it, so I do not count it among the requests
"it makes."

**Request 2 — the directory region.**
Bounded by two trailer fields obtained and validated in request 1:
`dir_offset` gives the range's start, `dir_length` gives its length. Range:
`[dir_offset, dir_offset + dir_length)`. Bytes: `dir_length`
(`dir_length ≥ 4`, and `dir_offset + dir_length ≤ F − 64`, so
`dir_length ≤ F − 64 − dir_offset ≤ F − 80`; for F = 4,096 that bounds
`dir_length ≤ 4,016`). §6.4 step 2: "Fetch
`[dir_offset, dir_offset + dir_length)`; verify and decode per §7.1." The
directory's terminal 4-byte CRC-32C is verified over the preceding
`dir_length − 4` bytes before any record is parsed (`[R-CNT-11]`); only then
does record-walk/layer-table construction (§19.1 step 4) proceed, which is
the last step of "the open" (`[R-RDR-01]`).

**Which field bounds the second range before it is read:** `dir_length`
(together with `dir_offset`, which sets the start) — both are trailer fields,
obtained and validated in request 1, strictly before request 2 is issued.
`dir_length` is the one that fixes how many bytes request 2 asks for.

**Totals, this scenario:**
- 2 requests.
- Request 1: `[F−64, F)`, 64 bytes.
- Request 2: `[dir_offset, dir_offset+dir_length)`, `dir_length` bytes
  (≥ 4, and bounded above by `F − 64 − dir_offset`).
- Total bytes fetched: `64 + dir_length`.

This matches §6.4's own framing exactly: "The baseline remote open is two
requests" — consistent whether or not the file in question happens to have a
small enough directory to fit a 64 KiB suffix window (`[R-CNT-09]`); the
brief's scenario (complete-length disclosure, no probe needed) is precisely
the case the text calls out as merging steps 1–2 into one request.

**Cross-check for disagreement.** §6.4's opening sentence, §19.1 step 1's
restatement, and `[R-RDR-01]`'s summary all describe the same two-request
accounting with no daylight between them; the only textual nuance is that
§6.4 states the *theory* ("a theory of operation, not a budget... nothing
here bounds what a reader fetches") while §19.1/`[R-RDR-01]` state the
*obligation* ("MUST" validate in this order; "its I/O is §6.4's request
accounting"). These are complementary, not contradictory — no finding.

---

## PART B — Validation timing by tier (§19.2, consolidated)

- **At open:** front signature block (only if resident, `[R-CNT-04]`);
  trailer (magic, CRC, version gate, remaining field gates, `[R-CNT-06]`
  through `[R-CNT-08]`); directory region CRC (`[R-CNT-11]`); the record
  walk's framing/multiplicity/extent-slot rules for non-layer top-level
  records and the user-metadata top-level framing floor (`[R-CNT-12]`
  through `[R-CNT-15]`, `[R-CNT-25]`, `[R-MTA-03]`); the layer-name
  namespace, built from name fields obtainable within each layer record's
  own `inline_length` (`[R-ENC-12]`, `[R-ENC-15]`).
- **At first access to a layer:** the *whole* layer record — extent slot,
  every `[R-CNT-23]` constraint, exact parse, sub-record walk and
  multiplicity, name rules for dimensions/channels, user-metadata sub-record
  framing floor, u64 domain and declaration-derived-sum ceilings, the §7.4
  value sets, fill constraints, the lz4 cap, the geometry floor and its
  arithmetic, and the index cross-checks computable without I/O
  (`[R-RDR-03]`) — all before any use of the layer's declarations. No fetch
  happens here; it is all decidable from the already-resident directory and
  F.
- **At use of a tile:** the index-chain (`crc_of_crc_array`, segment CRC),
  the entry's own classification (§15.3), the payload CRC, and the decode's
  exact-size obligation — all before any sample of that tile is returned
  (`[R-RDR-04]`, §19.4 steps 3–6).
- **At use of a record's extent:** that extent's terminal CRC and — only for
  an assigned metadata encoding — the document's own content rules, before
  anything the extent holds is returned. The open fetches no extent, so this
  is strictly later than open (`[R-MTA-10]`, `[R-RDR-02]`).

The rule binds the *latest* point, never a requirement to front-load
everything: "A reader MAY detect any violation earlier... it MUST NOT return
data whose governing structure has not passed the validation this rule
requires at its tier" (`[R-RDR-02]`). A violation in a layer never accessed
imposes no obligation beyond the open steps.

---

## PART C — Layer access (§19.3) and the tile-read algorithm to decoded samples (§19.4)

Layer access is pure computation over already-fetched bytes (directory +
trailer); it performs **no I/O** (`[R-RDR-03]`). It validates, in whatever
order an implementation likes (the rule does not sequence sub-checks, only
"full validation... before any use"): the extent slot; every `[R-CNT-23]`
field constraint (layout, codec, filter, alignment, slab, index_encoding,
fill-length-vs-element-size, `crc_of_crc_array`-vs-`entry_count=0`); the
mutual exclusion of alignment and slab (`[R-CNT-16]`); the exact-parse and
sub-record walk (`[R-CNT-18]`) and multiplicity (`[R-CNT-14]`); name
validity and uniqueness for dimensions/channels (`[R-ENC-11]`, `[R-ENC-12]`,
`[R-ENC-15]`); the index-formula cross-check
(`extent_length = entry_count×20 + ⌈entry_count/2¹⁶⌉×4`, `[R-CNT-17]`); the
geometry floor (`[R-GEO-01]`) and its arithmetic ceiling (`[R-GEO-03]`,
`[R-ENC-04]`); the lz4 decoded-size cap where codec = 4 (`[R-COD-07]`); the
2⁶³−1 domain on every u64 field (`[R-ENC-03]`). Only after *all* of this
passes does the reader treat the layer as open for tile-read.

**Tile-read algorithm (§19.4), point or region request, per needed tile:**

1. **Domain.** Point: `0 ≤ xᵢ < Eᵢ` for every dimension, or the request
   fails as a request (no file verdict) (`[R-MDL-01]`). Region: clip to the
   extents' intersection; wholly-outside or any zero-extent-layer region
   succeeds with no samples (`[R-GEO-02]`).
2. **Ordinals.** Tile coords `tᵢ = xᵢ div Tᵢ`, in-tile position
   `uᵢ = xᵢ mod Tᵢ`; in-tile ordinal `Σ uᵢ·∏_{j>i}Tⱼ`; spatial ordinal
   `s = Σ tᵢ·∏_{j>i}Gⱼ`; disk ordinal `s` (interleaved) or `c·N+s` (planar,
   per requested channel `c`) (`[R-GEO-06]`).
3. **Index chain.** Verify `crc_of_crc_array` over the fetched CRC array and
   the segment CRC over the fetched segment containing the entry — fetches
   may run in parallel, verifications may be cached (`[R-IDX-04]`,
   §15.4's note).
4. **Entry.** Classify per §15.3. A valid sentinel short-circuits steps 5–6:
   every requested position of that tile reads as fill, bit-exact, with no
   payload I/O (`[R-TYP-06]`, `[R-TYP-08]`). A malformed entry rejects the
   tile; fill is never substituted for a rejection (`[R-CNF-09]`).
5. **Payload.** Fetch `[offset, offset+length)`; verify the entry's `crc`
   over the stored bytes before decoding (`[R-CNT-20]`).
6. **Decode.** Codec, then the filter's inverse; decoded length must equal
   the declared decoded size exactly (`[R-SER-07]`, `[R-COD-08]`).
7. **Extract.** Locate each requested value by §14's offset arithmetic;
   never return a padding position (`[R-GEO-04]`).
8. **Return.** Bit-exact values, unaltered (`[R-MDL-02]`, `[R-TYP-04]`).
   Multi-entry requests: a tile-scope failure bounds to that tile's
   positions (reader MAY partial-return with a per-entry failure report, or
   fail the whole request, but MUST NOT fill in for it); a layer-scope
   failure inside the same request (an index-chain failure) bars the rest of
   the request and all further service from the layer, prospectively only —
   already-returned values stand (`[R-RDR-04]`).

---

## PART D — Degradation walks (seven, end to end)

### D1. Unknown top-level record type, MU = 1
Open's record walk hits a type the reader does not implement, stored
MU = 1. Outcome: **reject-file** (`[R-CNT-15]`: "A record at file scope
whose type the reader does not implement is governed by its stored MU bit:
MU = 1 is reject-file"). The file may still be fully conforming on its own
terms if the type is from the *experimental* range (§10.3, §21.6's closing
paragraph) — the reader's refusal is then a capability refusal, not a
finding about the bytes — but if the type is from the *reserved* range, the
file itself is nonconforming on a second, independent ground (`[R-CNT-15]`,
register row F36, detector verifier). Either way, this reader rejects the
whole file at open, before any layer table is built, so it serves nothing
and lists nothing.

### D2. Unknown codec on a layer
Layer access reads a codec field outside 1–4 (reserved or experimental):
**reject-layer** (`[R-COD-03]`, `[R-CNT-23]`), checkable at layer access
with no fetch — all other layers are unaffected (§2.4's reject-layer
meaning), and the reader MAY still list the rejected layer's name (it is
already in the open-time layer-name namespace, §19.1 step 4) though not its
declarations (full validation of those never passed). **Sharper case, and
the one the brief actually poses** — the codec value is *assigned* (e.g.
codec 3, zstd) but *this reader* does not implement it: per `[R-COD-11]`,
"software unable to execute an assigned codec or filter is not a conforming
reader" at all; §17.4 says the reject-layer position "arises only at a
reserved or experimental value" *for a conforming reader*. There is no
register row and no licensed outcome class for "conforming reader meets an
assigned codec it lacks," because the specification's design (§1: "a closed
core with an open edge... there is no subset of the core a conforming reader
can decline," restated at `[R-CNF-03]`) forecloses that software from being
a conforming reader in the first place — see Finding readerb-01.

### D3. Unrecognized flag bit
Two sub-cases, opposite outcomes, both at open, both from the trailer:
- Incompat lane (bits 0–15) bit set that this text does not define: every
  bit in that lane is "unimplemented" to this text's readers, so
  **reject-file** (`[R-CNT-08]`, F19).
- Ignore lane (bits 16–31) bit set: **not a violation** — ignored, file
  conforming (§21.6, `[R-CNT-08]`).
A reserved layer-record or sub-record flag bit (bits 2–15 of the 16-bit
record-flags field) is a different case again: not a reader-detectable
violation at all — "readers MUST ignore them" (`[R-CNT-12]`) — but it *does*
make the file nonconforming, detected only by a **verifier** at
certification (F26/L47). Three distinct bit-spaces, three distinct outcomes;
I checked this for disagreement and found none — each is scoped to its own
field and the text is internally consistent.

### D4. Truncated tail
"Truncated" bottoms out at whichever structure the truncation lands in:
- Truncated below 128 bytes total: **reject-file**, decided from F alone,
  no byte of the file read (`[R-CNT-27]`, F5) — this is R6 below.
- Physical file longer than F but the final 64 bytes are not a valid
  trailer (a torn mid-commit write, §9.2's crash example): the reader's
  default path is "trailer-at-end-or-fail... MUST NOT scan backward"
  (`[R-LIF-05]`) — reported as torn/invalid, not silently repaired; recovery
  is a separate, deliberate tool operation (§9.6), never an implicit reader
  behavior.
- A record's inline payload or a sub-record sequence truncated before its
  declared end: reject-file (top-level, F29) or reject-layer (sub-record,
  L14), per `[R-CNT-12]`/`[R-CNT-18]`.
- A codec stream truncated inside a tile's stored extent: decode fails to
  produce the exact decoded size or fails outright → **reject-tile**
  (`[R-SER-07]`, `[R-COD-08]`, T25).

### D5. Checksum mismatch
Also bottoms out by structure, and the chain is strictly ordered
(`[R-CNT-19]`, `[R-CNT-20]`, §8.2): trailer CRC mismatch → reject-file (F14);
directory CRC mismatch → reject-file, and nothing else may be served, since
the reader "MUST verify that CRC before any other use of the region"
(`[R-CNT-11]`) — this is R5 below; `crc_of_crc_array` or a segment CRC
mismatch → reject-layer (`[R-IDX-04]`, L37/L38); a stored tile's `crc`
mismatch → reject-tile, all other tiles (same layer or not) unaffected
(`[R-CNT-20]`, T1); a user-metadata extent's terminal CRC mismatch →
ignore-record, SHOULD-report (`[R-CNT-20]`, R2) — the one case in this list
where a checksum failure does **not** reject a structural scope, because the
document is quarantined (`[R-CNT-25]`).

### D6. Limit exceeded
Governed entirely by `[R-ERR-04]` and §21.9's minimum-guarantee table: a
file whose quantities exceed a guaranteed minimum (e.g. a tile whose decoded
size is above 256 MiB, a directory above 16 MiB, more than 65,536 layers) is
**still conforming**. A reader MAY decline it — at the narrowest scope whose
quantity it cannot serve (tile, layer, the metadata record, or the whole
file for a file-wide quantity like layer count or `dir_length`) — but MUST
report the decline as a **resource limit**, never as a validity error
("the two send a user to opposite remedies"). A reader that declines on this
ground a file whose every quantity is *within* the table is simply not a
conforming reader (`[R-CNF-03]`) — the guarantees are a floor. Contrast:
declining on a capability ground (unimplemented format major, or an
unimplemented top-level MU = 1 type) is licensed differently and is not
"this ground" (§21.6's closing paragraph draws the line explicitly).

### D7. Format major the reader does not implement
Reader rejects the file (`[R-CNT-07]`): "A reader MUST reject-file when
`version_major`... is a major it does not implement, and the diagnostic...
SHOULD be distinct from both 'not a TARN file' and 'corrupt'." Crucially,
the *file itself* may be a perfectly conforming file under that other major
— "neither conforming nor nonconforming under it [format major 1] save as
to the conditions that reach it" (`[R-CNF-02]`, `[R-CNF-13]`) — so this is
named explicitly as a reader capability refusal, not a file-conformance
finding (§21.6's closing paragraph, first of its two listed cases). The
*only* conditions a reader must still check regardless of the declared major
are the ones `[R-CNT-24]` fixes across every major: trailer magic (F8),
trailer CRC (F14), front block (F6), and both of F1's byte-reversal
instances — nothing else in the trailer or directory is checked against a
foreign-major file, and no §21 row records a foreign-major file's content as
a violation.

---

## PART E — Worked example with real offsets

I built this by taking the document's own §7.4 worked example (the `sst`
layer: rank 1, dimension `x` extent 100 / tile extent 32, one interleaved
`temp` float32 channel, fill quiet-NaN `0x7FC00000`, codec 1 / filter 1, no
alignment or slab, `entry_count = 4`, all four tiles sentinel) and placing it
inside a complete, byte-exact minimal file, computing every offset and
re-deriving the document's own stated constants from raw bytes with my own
CRC-32C implementation (verified first against the spec's check vector and
its all-sentinel-segment constant — both matched exactly, see disclosure).

**Layout (all offsets verified by local computation, not asserted):**

| Region | Byte range | Length | Notes |
|---|---|---|---|
| Front signature block | [0, 16) | 16 | constant |
| Tile-index region (layer `sst`) | [16, 100) | 84 | 4 sentinel entries (80) + 1 segment CRC (4) |
| Directory region | [100, 209) | 109 | one layer record (105) + directory CRC (4) |
| Pre-trailer pad (slack) | [209, 256) | 47 | zeroed by advice, `[R-CNT-03]` |
| Trailer | [256, 320) | 64 | |
| **F (committed_file_length)** | | **320** | multiple of 64 ✓ |

**Checksums reproduced exactly:**
- Segment CRC over the 80-byte all-sentinel entry array: `0x80A34955`
  (stored LE `55 49 A3 80`) — **matches the document's own stated value**.
- `crc_of_crc_array` = CRC-32C of those 4 bytes: `0xC4EE982E` — **matches**.
- Directory CRC (over the 105-byte record sequence, my own construction,
  not stated in the document): `0x44D52258`.
- Trailer CRC (over trailer bytes [0,60), my own construction):
  `0x1F83EF68`.

**Record header, byte-exact (24 bytes):** type `01 00`; flags `00 00`
(MU=0, PE=0, per §7.3's registry-fixed values for type 0x0001); inline_length
`51 00 00 00` (81); extent_offset `10 00 00 00 00 00 00 00` (16);
extent_length `54 00 00 00 00 00 00 00` (84).

**Validity floor check:** this file is 320 bytes, well above the 128-byte
minimum (`[R-CNT-27]`); `dir_offset` (100) ≥ 16; `dir_length` (109) ≥ 4;
`dir_offset+dir_length` (209) ≤ F−64 (256) — 47 bytes of headroom, which is
exactly the pre-trailer pad computed above and nothing else, consistent with
`[R-CNT-05]` ("Writers MUST place the directory so that no structure lies
between its end and the trailer").

Source: `/private/tmp/.../scratch/walk-reader-b/*.py` (inline heredocs,
not saved as separate files — the arithmetic is reproduced in full above).

---

## PART F — Probe derivations

(See structured probe_answers for the final answers; derivations for R7 and
the CRC-based probes are above. R2's bit math: `0x00000004` = bit 2 set,
which lies in bits 0–15, the incompat lane, and this text defines zero flag
bits of any kind, incompat or ignore — so the bit is unconditionally
unimplemented and `[R-CNT-08]` fires regardless of which specific bit it is.)

---

## PART G — Findings

**readerb-01 (OBSERVATION).** The specification gives a conforming reader no
licensed outcome — no register row, no §21.6 non-violation entry — for the
case where the software itself cannot execute an *assigned* core codec or
filter (e.g. zstd). `[R-CNF-03]` requires every conforming reader to
implement all four codecs and both filters with "no subset profiles... even
if it reads all other conforming files correctly." `[R-COD-11]`/§17.4 then
states that for a conforming reader, "cannot execute this codec" only
legitimately arises at a reserved or experimental value — i.e. the document
treats "conforming reader lacking a core codec" as a contradiction in terms
rather than a case to define behavior for. This is evidently deliberate
(§1's "closed core... no subset... can decline" is a named design goal, not
an oversight), so I record it as an OBSERVATION rather than an AMBIGUITY:
the document is internally consistent, but it leaves the very common
real-world situation — an implementation that supports most of the format
but not, say, zstd — entirely outside its conformance vocabulary. Such
software's behavior toward a zstd layer (reject that layer only? refuse the
whole file? silently misdecode?) is unconstrained by this text, because the
text's position is that such software does not qualify for discussion.
Byte-level test: does resolving this change what bytes *a conforming
implementation* may emit or must accept/reject? No — by the document's own
terms no conforming implementation is ever in this state, so nothing about
conforming behavior is left undetermined. I report it because a real
implementer asking "what do I do if I haven't finished my zstd decoder yet"
gets no answer from this document, only a disqualification.

I found no CONTRADICTION in the sections this walk exercised: every
cross-reference I followed (the CRC coverage map vs. the verification-order
rule, §19's tier-by-tier restatement vs. §21's per-row Detector/Detected
cells, the three disjoint flag-bit outcome spaces of D3 above, the §6.4
request accounting vs. its §19.1 restatement) was self-consistent on
inspection, and the constants I could check computationally (the CRC check
vector, the all-sentinel-segment constant, the §7.4 worked example's segment
CRC and `crc_of_crc_array`) all reproduced exactly.
