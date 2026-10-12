# Reader-implementer walk — edition A — transcript

## Disclosure

- A "user request" (`Go`) was relayed above this brief by the harness. Per
  the brief's own instructions, it is the launcher's message to the
  orchestrator, carries no task for me, needs no reconciliation with this
  brief, and does not widen the access rule. Noted and set aside.
- My runtime placed unsolicited material in context before I began: a
  project `CLAUDE.md` pointer to an `AGENTS.md` file, a user memory index
  (`MEMORY.md`) with ~30 one-line titles about a "TARN" project's harness,
  gates, repair passes, etc., a git-status block naming recent commit
  subjects on a branch called `readable`, an attribution-footer policy for
  commits/PRs, a model/environment identification block, and a long list of
  deferred-tool names. None of this is part of the specification and none
  of it is evidence about the specification's content. I did not open
  `AGENTS.md`, did not read any memory file linked from `MEMORY.md`, did not
  run `git log`/`git diff`, and did not treat any commit-subject text (e.g.
  "spruce-up pass", "word-diff preflight") as a fact about this document. I
  disregarded all of it.
- The one file I was told to read is exactly where the brief said it would
  be: `/Users/robertkleffner/Documents/GitHub/tarn-first-draft/scratch/cleanroom/editions/a/tarn.md`.
  I read it in full (5 `Read` calls covering lines 1–4981, the whole file;
  confirmed via `wc -l`/`wc -c` first: 4981 lines, 302,380 bytes). I did not
  list any directory other than my own scratch directory, did not open any
  other copy of this specification, did not read `docs/`, `PLAN.md`,
  `OPEN-QUESTIONS.md`, `AGENTS.md`, `README.md`, `CONTRIBUTING.md`,
  `conformance/`, or `spec/registry.json`, and did not run `git log`/`git
  diff`/web search/web fetch.
- I ran local, file-free computation only: a Python 3 script (run with
  `python3 -I` to disable the script-directory/cwd import shadowing the
  environment warns about, even though this script reads nothing) that
  implements CRC-32C (Castagnoli, reflected, init/final 0xFFFFFFFF) from
  the polynomial alone and checks it against every stated constant/checksum
  in the document, plus the §11.4/§14.2 arithmetic for probe R7. No file
  was read by that script. Scratch files I wrote, all under my own scratch
  directory and nowhere else:
  - `crc_check.py` — check vector, zero-byte CRC, all-sentinel full-segment
    CRC (§4.5, §15.4).
  - `crc_check2.py` — Appendix A's 128-byte minimal file: full hex
    reconstruction and its trailer CRC.
  - `crc_check3.py` — §7.4's worked layer-record example (segment CRC and
    crc_of_crc_array over 4 sentinel entries), the index extent_length
    formula, the bfloat16 example, and probe R7's ordinal/offset
    arithmetic.
  My scratch directory was empty when I started (verified by `ls -la`
  before writing anything), so there is no prior attempt's files to
  disclose.
- I did not read or list the shared output directory
  (`/private/tmp/claude-501/.../fidelity-4/out/`) other than to write my
  own transcript file into it, as instructed.

## 1. The open path — every byte fetched before the trailer and directory validate

Governing text: §19.1 (open algorithm), §6.2 (trailer), §6.4 (remote
accounting), §7.1 (directory region).

Walking it in the order a cold remote reader (ranged transport, complete
length disclosed per response) performs it, against a hypothetical
4,096-byte file (probe R1's setup):

1. **Request 1 — suffix range for the final 64 bytes.** Byte range
   `[F−64, F)`. Before F is known this is naturally expressed as a
   suffix-range request ("last 64 bytes"); the transport's response
   discloses the complete resource length, which *is* F (`[R-CNT-10]`). For
   F = 4096 this is `[4032, 4096)` — exactly 64 bytes. §19.1 step 1 (obtain
   F) and step 2 (fetch and validate the trailer) are "ordered by
   dependency, not by I/O": because the transport discloses the complete
   length in this response, both steps are discharged by this one request
   (§6.4: "so that §19.1's first two steps cost one request between them").
   The reader validates these 64 bytes in §6.2's fixed order: trailer
   magic; trailer CRC (`[R-CNT-06]`, `[R-ENC-09]`); the version gate
   (§6.3); then, those three passed, the remaining field gates as a set —
   flags; `committed_file_length` against the transport-authoritative size
   (here, 4096, matching F already obtained); `dir_offset ≥ 16`;
   `dir_length ≥ 4`; `dir_offset + dir_length ≤ F − 64`; `file_id ≠ 0`;
   reserved bytes zero (`[R-CNT-06]`). Only after `dir_offset` and
   `dir_length` pass their own gates does the reader act on them to form
   the next request (`[R-ENC-10]`: verify before acting on a field, which
   for a non-checksum gate is this ordered-validation discipline instead,
   §6.2).
2. **Request 2 — the directory region.** Byte range
   `[dir_offset, dir_offset + dir_length)`, length `dir_length` bytes. Both
   halves of this range are bounded by trailer fields obtained and
   gate-checked in request 1 and nowhere else: `dir_offset` fixes the
   start, `dir_length` fixes the extent, and the pair's own validity
   (`dir_offset ≥ 16`, `dir_length ≥ 4`, their sum `≤ F − 64`) was
   established in step 2's trailer validation *before* this range is read,
   never after. The reader then verifies the directory CRC over the
   preceding `dir_length − 4` bytes before any other use of the region
   (`[R-CNT-11]`) and only then parses records (§19.1 step 4).

**Total: 2 requests** — `[4032, 4096)` (64 bytes) and
`[dir_offset, dir_offset + dir_length)` (`dir_length` bytes) — **total bytes
fetched = 64 + dir_length**. The probe gives no `dir_offset`/`dir_length`
for this hypothetical file, so the total cannot be reduced to one number;
it is exactly `64 + dir_length`, per §6.4's own accounting ("two requests,
each with an exact target"). §6.4 separately licenses a non-baseline
variant — one speculative suffix fetch plus a containment test, which can
collapse this to one request when the window happens to contain the
directory — but that is a reader option (`MAY`), not the baseline the open
algorithm states, and the probe asks for "every request it makes," which I
read as the deterministic baseline path. The field(s) bounding the second
range: **`dir_offset`** (the range's start) and **`dir_length`** (the
range's extent), both trailer fields, both validated under §6.2's ordered
gates in step 2 before the reader acts on them to compute and issue
request 2.

Note on scope: completing these two requests and the record walk is "the
open" (§19.1, closing sentence) and costs exactly this I/O "at any layer
count and file size" (`[R-RDR-01]`) — no layer record's extent slot, no
tile index, and no payload is touched yet. This is why the open validates
*the directory's record framing and the layer-name namespace* but not any
layer's declarations (§19.2: layer validation is deferred to first access,
§19.3).

## 2. Validation timing by tier (§19.2, `[R-RDR-02]`)

The document states four tiers, each the *latest* point a violation
touching that tier's structures may surface, never a mandate to defer:

- **At open:** front signature block (only if resident, `[R-CNT-04]`);
  trailer; directory region + record walk; layer-name namespace
  uniqueness (§19.1 steps 1–4).
- **At first access to a layer:** full validation of that layer's record —
  extent slot, the whole §7.4 constraint set, sub-record walk and
  multiplicity, name rules, user-metadata sub-record framing, the u64
  domain, every enumerated value set, fill constraints, codec
  declaration bounds, geometry floor/arithmetic, the 2⁶³−1 ceiling on every
  derived quantity, and the index cross-checks computable without I/O
  (§19.3, `[R-RDR-03]`) — all decidable from the resident directory and F,
  with **no fetch**.
- **At use of a tile:** the index chain (crc_of_crc_array, segment CRC),
  the entry's own classification (§15.3), the payload fetch and its CRC,
  decode, extraction (§19.4).
- **At use of a record's extent:** that extent's CRC and the content rules
  its encoding attaches (§18.2), not before — "since the open fetches no
  extent."

A violation's *outcome and scope* always come from the rule that defines
it, never from the tier at which it happens to be caught (§19.2: "Failure
at any point takes the violated rule's own outcome and scope — in
particular, index-chain failures take layer scope [`R-IDX-04`] although
their detection point is tile use"). Earlier detection is always licensed
(`[R-CNF-12]`); a conforming reader simply must not serve data past its
tier's gate.

## 3. Layer access (§19.3, `[R-RDR-03]`)

First access to a layer (the first use of anything beyond its *name*, that
being parsed at open) requires full record validation first, and — this is
the point worth stating plainly — **none of it costs I/O**: extent slot
rules, the §7.4 field-by-field constraint set, sub-record framing and
multiplicity, name well-formedness/uniqueness, the domain and overflow
ceilings, and the index-region cross-check (`entry_count` against the
geometry-derived addressed-tile count, `extent_length` against the
20-byte-entry-plus-segment-CRC formula) are "all decidable from the
resident directory and F." Only after this gate may any of the layer's
declarations (geometry, codec, fill, …) be used for anything, including
forming the tile-index fetch of §19.4.

## 4. The tile-read algorithm (§19.4, `[R-RDR-04]`)

Eight steps, each failing under the rule it cites:

1. Domain check against extents (`[R-MDL-01]`, `[R-GEO-02]`) — not a file
   verdict, a request-level non-match.
2. Compute tile coords, in-tile ordinal, spatial ordinal `s`, disk ordinal
   (`[R-GEO-06]`): `s` for interleaved, `c·N + s` per requested channel for
   planar.
3. Index chain: verify `crc_of_crc_array` over the fetched CRC array and
   the segment CRC over the fetched segment containing the entry
   (`[R-IDX-04]`) — **layer-scope** failure here, though caught at tile
   use.
4. Classify the entry per §15.3 (`[R-IDX-03]`); a valid sentinel
   short-circuits to fill with no payload I/O; a malformed entry is
   **tile-scope** reject, and fill is never substituted for a rejection
   (`[R-CNF-09]`).
5. Fetch `[offset, offset+length)`; verify the entry's `crc` before
   decoding (`[R-CNT-20]`).
6. Decode: codec then filter's inverse (§17.1); exact-decoded-size rule
   (`[R-SER-07]`).
7. Extract requested values by §14's offset arithmetic; never return
   padding positions (`[R-GEO-04]`).
8. Return bit patterns unaltered (`[R-MDL-02]`, `[R-TYP-04]`), the one
   resolved exception being `[R-SER-08]`'s nonconforming-bool-byte rule.
   A region/multi-channel request's tile-scope failures are bounded to
   the positions that tile carries; a layer-scope failure (step 3) bars
   the rest of the request and all further service from the layer, but
   is prospective — values already returned stand.

## 5. Checksum/constant verification (local computation, no file reads)

All computed with a from-scratch CRC-32C (poly 0x1EDC6F41 reflected as
0x82F63B78, init/final XOR 0xFFFFFFFF), run via `python3 -I`:

| Claim (location) | Computed | Match |
|---|---|---|
| CRC-32C(`"123456789"`) = `0xE3069283` (§4.5) | `0xe3069283` | yes |
| CRC-32C(zero bytes) = `0x00000000` (§4.5) | `0x0` | yes |
| CRC-32C of 2¹⁶ sentinel entries = `0xEECB3BB2` (§15.4) | `0xeecb3bb2` | yes |
| Appendix A: trailer CRC over trailer bytes [0,60) of the 128-byte minimal file = `0x402F157E` | `0x402f157e` | yes |
| Appendix A: directory-region CRC = CRC-32C(zero bytes) = `0x00000000`, stored `00 00 00 00` | `0x0` | yes |
| §7.4 example: segment CRC over 4 sentinel entries (80 bytes) = `0x80A34955`, stored `55 49 A3 80` | `0x80a34955` → LE `5549a380` | yes |
| §7.4 example: `crc_of_crc_array` = CRC-32C(`55 49 A3 80`) = `0xC4EE982E` | `0xc4ee982e` | yes |
| §7.4 example: `extent_length` formula, entry_count=4 → 4×20+⌈4/2¹⁶⌉×4 = 84 | `84` | yes |
| §12.1 example: bfloat16(1.0) = high 16 bits of binary32 `0x3F800000` = `0x3F80` | `0x3f80` | yes |

Every stated constant/checksum I could check from the text alone, checked
out; I found no arithmetic or checksum error in edition A.

I additionally re-derived (by hand, cross-checked against the document's
own worked numbers, not independently recomputed by script except where
noted) §11.2's grid/tile-count example (G=(4,8), N=32; with extent 1000
instead of 1024, G_y = ⌈1000/256⌉ = 4, unchanged), §11.4's ordinal example
(tile (1,2) → s = 10; in-tile ordinal 11,452; planar C=4 disk ordinal 74),
and §15.4's large-index example (entry_count = 1,000,000 → 16 segments,
last covering 16,960 entries; tile k=999,999 at segment-relative byte
20×16,959 = 339,180; segment start at region byte 983,040×20 =
19,660,800; CRC array at [20,000,000, 20,000,064)). All of these check out
arithmetically against the document's own stated formulas; I found no
divergence.

## 6. Worked example with real offsets

Using Appendix A's 128-byte minimal conforming file (the only full file
laid out byte-for-byte in this document) plus §7.4's layer-record payload
example (bytes given but not embedded in a full file):

- Front signature block `[0,16)`: magic `89 54 41 52 4E 0D 0A 1A` + 8 zero
  bytes — verified against the §6.1 constant.
- Directory region `[16,20)`: 0 record bytes + CRC `00 00 00 00` =
  CRC-32C(∅), verified above.
- Pre-trailer pad `[20,64)`: 44 zero bytes — slack, zeroed by
  `[R-CNT-03]`'s advice, not required.
- Trailer `[64,128)`: magic `8A 4E 52 41 54 0D 0A 1A`; version_major=1,
  version_minor=0; flags=0; dir_offset=16; dir_length=4;
  committed_file_length=128=F; file_id=`0x0123456789ABCDEF`; 12 reserved
  zero bytes; trailer CRC `0x402F157E`, verified above against trailer
  bytes `[64,124)` (trailer-relative `[0,60)`).
- A remote reader's open: request 1 = `[64,128)` (the whole trailer, which
  for this tiny file also happens to be a "speculative suffix window" that
  reaches offset 0 only if the window is ≥128 bytes, in which case
  `[R-CNT-04]`'s front-block equality check becomes due); request 2 =
  `[16,20)`, 4 bytes. A 112-byte window `[16,128)` also satisfies
  containment (§6.4) and would let a reader skip request 2 while still
  leaving `[0,16)` non-resident (so the front-block check stays optional).
- §7.4's layer record (not placed at a real file offset in the document,
  but every field and its arithmetic are given): the inline payload is 81
  bytes exactly (name 4 + nine scalars 34 + one dimension entry 18 + one
  channel entry 12 + trailing fixed fields 13 = 81, no residue, so the
  sub-record sequence is empty); its extent slot addresses an 84-byte
  tile-index region (4 sentinel entries × 20 + one 4-byte segment CRC),
  whose segment CRC `0x80A34955` and whose `crc_of_crc_array` `0xC4EE982E`
  I verified above.

## 7. Eight degradation walks, end to end

**(1) Unknown top-level record type, no MU bit.** A record with type
0x9000 (experimental range, ≥0x8000 per §10.2), MU=0. At open, step 4:
`[R-CNT-15]` — MU=0 on an unknown type is *ignore-record*; this is a
defined non-violation (§21.6: emitting an experimental-range value with
MU=0 is conforming; only a *reserved*-range value, 0x0003–0x7FFF, would be
a violation, F36, detector *verifier*, since emitting a reserved value at
all — regardless of MU — is itself a violation even though no reader
behavior differs). The reader skips the record as though absent; decoding
of all stored data is unaffected; an updater preserves or drops it per its
PE bit (§20.4).

**(2) Unknown codec — the reserved/experimental value case.** Layer
record's codec field = 5 (reserved, 5–0x7FFF per §10.2). At first layer
access (§19.3), the §7.4 constraint set catches this: `[R-CNT-23]`/`[R-COD-03]`
— any codec value outside 1–4 is a validity error at layer scope, register
row L43. Outcome: **reject-layer**. The reader MAY still list the file's
layers including this one's name (§2.4); it checks no payload CRC for this
layer and performs no tile I/O for it, having rejected at layer-access
time, before any tile is touched.

**(2′) Unknown codec — the assigned-but-unimplemented case (probe R3's
case).** This is different in kind from (2): codec 3 (zstd) is an
*assigned, core* value, not reserved/experimental, so `[R-COD-03]`'s
value-set check *passes* — the layer is not malformed. §17.4 states that
"software unable to execute an assigned codec or filter is not a
conforming reader" (`[R-CNF-03]`), full stop; it does not say what such
software's *behavior* is. See Finding 1 below — I could not find register
text, a resource-limit row, or an §21.6 non-violation entry that assigns
an outcome class to this exact situation for a layer that is otherwise
conforming.

**(3) Unrecognized flag — trailer incompat-lane bit.** `flags =
0x00000004` (bit 2, incompat lane bits 0–15). At open, after magic/CRC/
version gate pass, the flag gate fires: `[R-CNT-08]` — "a reader MUST
reject-file on any set bit it does not implement in the incompat lane";
this text defines none, so every such bit is unimplemented. Outcome:
**reject-file** (register row F19). This is exactly probe R2's case; see
§Probes below. Contrast: `flags = 0x00010000` (bit 16, ignore lane) is
ignored outright — not a violation, not a reader action of any kind
beyond ignoring it (§21.6; `[R-CNT-08]`).

**(4) Truncated tail.** A file whose physical length is, say, 4,090 bytes
where the last committed generation's trailer declared
`committed_file_length = 4,096` (a torn append per §9.2's example). The
reader's open step 1 obtains the *actual* transport size, 4,090; step 2
fetches `[4090−64, 4090)` and validates it as a trailer. Two sub-cases:
(a) if those final 64 physical bytes are not a valid trailer at all (no
magic match, or CRC fails) the reader reports the file torn/invalid per
the *default read path* (`[R-LIF-05]`) and **MUST NOT scan backward** —
this is not a conforming reader's job; recovery (§9.6) is a separate,
deliberate tool operation. (b) If by coincidence those final bytes parse
as *some* valid-looking trailer but its own `committed_file_length` field
does not equal the actual physical size (4,090), that is F17 —
**reject-file** — again under the ordinary open path, with no backward
scan. Either way the outcome is reject-file, and the distinction between
"torn" and "corrupt" is not one the format asks a conforming reader to
make on this path.

**(5) Checksum mismatch — four different scopes depending on which
checksum.** (a) Trailer CRC mismatch → reject-file (F14, `[R-CNT-06]`).
(b) Directory-region CRC mismatch → reject-file (F20, `[R-CNT-11]`); see
probe R5. (c) A layer's `crc_of_crc_array` or a segment CRC mismatch →
**reject-layer** (L37/L38, `[R-IDX-04]`), detected at tile use but
layer-scoped. (d) A stored tile's bytes failing its index entry's `crc`
→ **reject-tile** (T1, `[R-CNT-20]`) — only that tile; "neighbors in the
same layer are unaffected" (§2.4). (e) A user-metadata extent's terminal
CRC failing → **ignore-record** (R2 in §21.5, `[R-CNT-20]`/`[R-CNT-25]`),
SHOULD-reported, and "decoding of all stored data is unaffected."

**(6) Limit exceeded.** A conforming file whose directory region is, say,
20 MiB — above §21.9's 16 MiB minimum guarantee for `dir_length` but not
itself a violation of any rule (the table states *minimum guarantees*, not
caps, `[R-ERR-03]`). A reader MAY decline it, but **only** at the scope the
exceeded quantity is itself scoped to — here the whole file, since
`dir_length` is file-level (`[R-ERR-04]`: "layers per file and dir_length
are" examples of file-scoped quantities) — and **MUST report the refusal
as a resource limit, not as a validity error** ("the two send a user to
opposite remedies"). The file remains conforming throughout; this is not
reject-file in the §2.4 register sense at all, even though the practical
effect (nothing served) can look similar. A reader that declined a file
whose every quantity instead stayed *within* the table on this same
ground would not be a conforming reader (`[R-CNF-03]`).

**(7) Format major the reader does not implement.** `version_major = 7`.
Open step 2: magic passes; trailer CRC passes (it covers raw bytes
regardless of their semantic layout under any major, so it is computable
and meaningful even for an unimplemented major — this is F14's "reach"
argument, `[R-CNF-13]`); the version gate then fires: `[R-CNT-07]` —
reject-file, with the document explicitly recommending a diagnostic
*distinct from both* "not a TARN file" and "corrupt" ("TARN format major
7; this reader supports major 1"). Crucially the file **can be perfectly
conforming** under major 7 — this is one of exactly two "conforming files
a reader nevertheless refuses" cases §21.6 names, and the register records
only the *neighboring* violation (version_major = 0, F18) rather than this
case itself, since this case is not a violation of anything (`[R-CNF-13]`,
§2.3). The reader never reaches `dir_offset`/`dir_length`/`file_id` checks
for this file — the version gate is checked immediately after the two
reaching conditions (magic, trailer CRC) and before "the remaining field
gates," per §6.2's own stated order.

## 8. Findings

### Finding readera-01 — no outcome is assigned to a reader that lacks an assigned, core codec/filter it is obliged to implement

**Kind:** AMBIGUITY (location_b/quotation_b n/a — this is a single-document
finding about edition A).

The charter's walk step and probe R3 both ask what happens when a layer
declares an assigned core codec (zstd, codec 3) that the reader does not
implement. Tracing every place the document discusses codec/filter
capability:

- `[R-CNF-03]` (§2.3): "There are no subset profiles: software that
  declines to support a core codec... is not a conforming reader, even if
  it reads all other conforming files correctly." This disqualifies the
  software from the conforming-reader class. It states nothing about what
  such software's observable behavior is, or what outcome class (if any)
  applies to the layer in its hands.
- §17.4 (`[R-COD-11]`): "For a conforming reader that position [inability
  to execute a codec/filter] arises only at a reserved or experimental
  value, every assigned codec and filter being core: it rejects the layer
  (`[R-COD-03]`, `[R-COD-09]`); software unable to execute an assigned
  codec or filter is not a conforming reader (`[R-CNF-03]`)." This
  sentence's own grammar confines the reject-layer treatment to "a
  conforming reader" meeting a *reserved or experimental* value — i.e. a
  value outside 1–4. It explicitly does *not* say that software lacking
  zstd, meeting the *assigned* value 3, rejects the layer; it only
  restates that such software is non-conforming.
- §21.9 (`[R-ERR-04]`)'s resource-decline mechanism is explicitly scoped to
  quantities the limits table states (rank, channel count, entry_count,
  layer count, dir_length, decoded tile size, metadata document size,
  zstd window) — not to "a codec this reader does not implement." Nothing
  in that table or its surrounding text contemplates codec/filter
  capability as a resource-limit axis.
- §21.6's closing paragraph enumerates, as a closed pair ("Two structural
  cases"), the only "conforming files a reader nevertheless refuses":
  an unimplemented format major, and an experimental-range top-level
  record type with MU=1. Lacking a core codec is neither of these, and
  the paragraph does not gesture at a third case.
- §21.5/§21.6 (the register and its non-violation table) are both scoped
  to *file-conformance violations and defined non-violations* — a layer
  declaring codec 3 is neither: it is a perfectly ordinary, unexceptional
  declaration on a conforming file.

So the document is fully determinate that such software is not a
conforming reader, but — unlike every other capability gap it discusses
(an unimplemented format major, an unimplemented top-level MU=1 type, a
quantity beyond §21.9's guarantees) — it never states what that software's
reject/serve/report behavior *is*, nor under what label (if any) it
reports a refusal. A verifier in the same position is told exactly what to
do (`[R-COD-11]`: "cannot establish that layer's conformance and MUST NOT
certify the file," with the usual `[R-CNF-11]` cannot-establish reporting
duty) — but a *reader* lacking the codec has no analogous instruction at
all, only the one-line disqualification from the conformance class.

**Byte-level test:** yes. Two implementations built from this text alone,
each omitting zstd, can diverge: implementation A refuses the whole file
(treating the gap like a format-major refusal); implementation B serves
every other layer and reports only the zstd layer as unusable (treating
the gap like a reject-layer value violation); implementation C serves the
layer's *declarations* (name, geometry, channel list) while refusing only
its *tile reads*. All three are equally consistent with the text, because
none of them is a "conforming reader" in the first place and the text
supplies no further constraint distinguishing their behavior. A spec
reader implementing this format and asking "what should my code actually
do when a customer's build omits the zstd dependency" gets no answer from
this document beyond "don't call it conforming."

### Finding readera-02 (OBSERVATION) — probe terminology for the tile-index entry's sentinel fields does not match the document's own field names

Not a defect in edition A; a note on probe R4's wording. The document
names a tile-index entry's two 8-byte fields `offset` and `length`
(§15.1's table); `extent_offset`/`extent_length` is the document's name
for a *record's* extent slot (§7.2) — a different structure at a different
scope (file/layer record framing, not a per-tile index entry). Probe R4
asks about "a tile-index entry [with] extent_offset equal to the sentinel
value" — read charitably as referring to the entry's `offset` field (the
only field of a tile-index entry the sentinel value governs in that
position), this maps cleanly onto register row T7 (§15.3,
`[R-IDX-03]`: "offset = S ∧ length ≠ S, or offset ≠ S ∧ length = S" →
*structural*: reject-tile). I answered R4 on that reading and flag the
naming mismatch here rather than as a document finding, since the
document itself is internally consistent and simply uses different field
names for these two structures.

## Evidence

(See `probe_answers` and the structured `evidence` object for the
required sweeps/derivations/rejected-candidates/confidence-empty summary.)
