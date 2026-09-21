# Reader implementer — cleanroom round 36 — working transcript

## 0. Disclosure

**What I read.** Exactly one file: `/Users/robertkleffner/Documents/GitHub/tarn-first-draft/spec/tarn.md`,
in full (4,981 lines, read in five `Read` calls due to tool size limits:
offsets 1–600, 600–1200, 1200–1800, 1800–2400, ... through 4600–4981 — the
tool's own pagination, not a choice to skip anything). I did not open
`AGENTS.md`, any ADR, `PLAN.md`, `OPEN-QUESTIONS.md`, `conformance/`,
`spec/registry.json`, or any other file in the repository. I ran no git
commands and did no web access. I ran only local, file-reading-free Python
arithmetic in my own scratch directory (below).

**Context that appeared unasked.** Before I did anything, my system prompt
already contained: (a) the contents of this project's `CLAUDE.md`, which
just points to `AGENTS.md` (I did not follow that pointer); (b) the
contents of a user memory file (`MEMORY.md`) with about 19 one-line entries
about this TARN project's history, gate wordlist, harness paths, prior
rounds' repair defects, and similar; and (c) a git status block naming the
current branch, a clean working tree, and five recent commit subject
lines, including `"ADR-0129's erratum E3: a writer of a new file takes one
of two positions, rewriter or creator, and the choice is its own"` and
`"§7.2 notes that MU and PE are not orthogonal"`.

I treated none of this as evidence about the specification's content. In
one place below (§20.1's writer-tiers analysis) I noticed that the
in-document text I was independently reading ("A writer of a new file from
an existing one takes one of two positions, and the choice is its own")
lines up with the commit-message text quoted above. I flag that
correspondence here for transparency, but my analysis of that passage
rests only on the document text and its own cross-references (§2.3, §9.1,
§20.2, §20.4, §20.5), not on the commit message. I did not use the
memory file's per-round claims (e.g. about wordlists, gates, or prior
repair locations) to steer where I looked or what I concluded; the section
list and heuristics in the task brief did that steering, and I additionally
read outside the listed 31 passages per the brief's own instruction not to
stop there.

**Scratch directory.** `/private/tmp/claude-501/-Users-robertkleffner-Documents-GitHub-tarn-first-draft/r36-round/scratch/reader/`
was empty when I started (I listed it before writing anything, per the
brief's instruction to check). I created and used exactly one file there,
`crc_check.py` (and re-ran equivalent code inline in later Bash calls
rather than editing it repeatedly) — a from-scratch CRC-32C implementation
(bit-at-a-time, then a table-driven variant for speed) used only to verify
arithmetic already stated in the document. I read no file from that
directory that I had not just written myself, and I did not read or list
the shared round output directory at any point.

## 1. Method

I read the whole document once, start to finish, then went back over the
31 listed changed passages a second time against the six "what shape
carries" bullets and the twelve numbered heuristics, then spent the
remaining effort on arithmetic verification (the worked-example charter
item) and on stress-testing a handful of passages that looked like
recent, dense rewrites (§20.1, §20.3 step 4, §20.4, §20.5, §5.2, §9.7,
§21.1, §21.6) against the "quantifier/scope" and "sentence rewritten to
close a reading" heuristics, since those are the two the calibration
history credits with the most real defects.

## 2. The open path, byte-exact

### 2.1 Steps, in order (§19.1)

1. **End of file.** Obtain the transport-authoritative file size F
   (`[R-CNT-10]`). F < 128 is reject-file (`[R-CNT-27]`, F5) and needs no
   other byte.
2. **Trailer.** Fetch `[F−64, F)` — exactly 64 bytes — and validate in
   §6.2's fixed order: trailer magic, trailer CRC, version gate (§6.3),
   then the remaining field gates (dir_offset ≥ 16; dir_length ≥ 4;
   dir_offset + dir_length ≤ F−64; committed_file_length = F and a
   multiple of 64; file_id ≠ 0; reserved bytes zero).
3. **Directory.** Fetch `[dir_offset, dir_offset+dir_length)` — exactly
   dir_length bytes — verify the trailing CRC-32C over the first
   `dir_length−4` bytes before any other use.
4. **Record walk.** Parse the record sequence (§7.2), apply the
   MUST_UNDERSTAND gate for unknown top-level types, per-type
   multiplicity, extent-slot validity for non-layer records, the
   top-level user-metadata framing checks, and build the layer table
   (name-uniqueness decided over raw bytes, `[R-ENC-13]`, `[R-ENC-15]`).

Step 1's front-signature-block check (§6.1) is folded in only where bytes
`[0,16)` happen to already be resident (a local file read whole, a memory
mapping, or a suffix speculation that reached offset 0); otherwise it is
deferred or omitted (`[R-CNT-04]`) and is **not** part of the open's
required I/O.

### 2.2 Byte-exact cost, remote reader, ranged-request server

**Baseline (§6.4, `[R-CNT-09]`):** exactly two requests.

- Request 1: a suffix range for the final 64 bytes. On a transport that
  discloses a range response's complete length (e.g. HTTP's
  `Content-Range: bytes X-Y/TOTAL`), this single response both supplies
  the 64 trailer bytes and discloses F, so steps 1 and 2 cost this one
  request together. **64 bytes downloaded.**
- Request 2: `[dir_offset, dir_offset+dir_length)`. **dir_length bytes
  downloaded.**

**Total: 2 requests, 64 + dir_length bytes.** No tile index, no record
extent, and no tile payload is fetched by the open at any file size or
layer count (`[R-RDR-01]`) — this is the invariant the accounting exists
to make legible, not a request-count promise (the section's own Note says
so explicitly: "no request count is a conformance property").

A reader MAY instead speculate a suffix window (commonly bounded near
64 KiB, per the writer guidance that dir_length + pad + 64 ≤ 65,536) in
one request and use containment to skip request 2 if the window happens
to contain `[dir_offset, dir_offset+dir_length)`. That collapses cost to
**1 request, up to the window size**, but is not required.

**Worked instance — Appendix A's 128-byte minimal file.** dir_offset=16,
dir_length=4, F=128.
- Request 1: `[64,128)`, 64 bytes; discloses F=128 (matches
  committed_file_length, satisfying F17's negative test).
- Request 2: `[16,20)`, 4 bytes; the CRC of those 4 bytes over 0
  preceding bytes is `0x00000000` — the layer table is empty (zero
  records).
- **Total: 2 requests, 68 bytes**, or in the speculative-suffix variant,
  a single 112-byte-or-larger suffix window (any window ⊇ `[16,128)`)
  containing both trailer and directory in 1 request — and if that
  window also reaches offset 0 (i.e. is the whole 128-byte file), the
  front block equality check becomes mandatory rather than deferred
  (`[R-CNT-04]`), which I verified: bytes `[0,16)` are exactly
  `89 54 41 52 4E 0D 0A 1A` + 8 zero bytes, matching §6.1's constant.

I hand-verified the trailer CRC given in Appendix A by implementing
CRC-32C myself (bit-at-a-time, polynomial 0x1EDC6F41 reflected =
0x82F63B78 forward-reflected form, init/final XOR 0xFFFFFFFF) and running
it over the 60 trailer bytes `[0,60)` as spelled out in the file: I get
`0x402F157E`, matching the document's stored bytes `7E 15 2F 40`
little-endian. I also reproduced the two check vectors
`[R-ENC-09]`/§4.5 states (`CRC32C("123456789") = 0xE3069283`,
`CRC32C("") = 0x00000000`) before trusting my implementation on anything
else.

## 3. Validation timing by tier

§19.2 fixes the *latest* point, not a schedule an implementation must
literally follow at run time:

| Tier | What must be checked no later than this point |
|---|---|
| **At open** | front block (if resident), trailer, directory region CRC, record-sequence framing, per-type multiplicity, non-layer extent-slot validity, layer-name uniqueness |
| **At first access to a layer** | the entirety of §19.3's list: layer record's extent slot, the full §7.4 field-constraint set, exact parse + sub-record walk + sub-record multiplicity, name rules, u64 domain and declaration-derived-sum ceilings, value sets for layout/linearization/type/codec/filter, per-type fill constraints, the lz4 decoded-size cap, geometry floor and grid arithmetic, and the index cross-checks computable without I/O (`[R-CNT-17]`) |
| **At use of a tile** | the index chain (crc_of_crc_array, segment CRC, entry classification), the payload's own CRC, the codec/filter decode and its exact-size obligation |
| **At use of a record's extent** | that extent's own CRC, and (for user metadata) the content rules the assigned encoding attaches |

A reader MAY detect any of these earlier (`[R-CNF-12]`); it MUST NOT serve
data from a structure that has not yet passed the check due at its tier.
Two things worth flagging for an implementer: (1) an index-chain failure
is *detected* at tile-use time but its *outcome* is layer scope
(`[R-IDX-04]`) — I built my tile-read code path to bail the whole layer,
not just the one requested tile, on that failure; (2) "structures a
request never relies on impose no detection obligation beyond the open
steps" (§19.2's closing sentence) means an implementation that never
touches layer B need not ever validate layer B's record at all — I
verified this against `[R-RDR-02]`'s own wording and it is stated exactly
that way, not something I inferred.

What a reader is **permitted never to check**: every verifier-only row of
§21 (coverage/overlap, `[R-CNT-05]`'s pre-trailer-gap-structure check,
alignment/slab invariants, registered-type flag mismatches, user-metadata
member ordering, padding/pad-bit/interleaved-bool content). A conforming
reader that never runs these is still conforming; only a conforming
*verifier* must run them.

## 4. Layer access and the tile-read algorithm

### 4.1 Layer access (§19.3)

First access to a layer performs **no fetch** — everything is decidable
from the already-resident directory and F. I built this as one pass over
the layer record's inline payload that (a) parses the fixed leading
fields, (b) parses d dimension entries and C channel entries, checking
name well-formedness/non-emptiness/C0-freedom/uniqueness as it goes, (c)
parses the trailing fixed fields, (d) parses the sub-record sequence
under §7.2 framing with a nesting-depth check, and (e) only after a
clean parse, runs the cross-arithmetic: Gᵢ = ⌈Eᵢ/Tᵢ⌉ per dimension, N =
∏Gᵢ, P = ∏Tᵢ, addressed-tile count (N or C·N), and `entry_count ×20 +
⌈entry_count/2¹⁶⌉×4` against extent_length (`[R-CNT-17]`) — each product
checked against 2⁶³−1 before use (`[R-ENC-04]`).

### 4.2 Tile read, layer name + coordinate → decoded bytes (§19.4)

1. **Domain check.** Point request: 0 ≤ xᵢ < Eᵢ for every i, else the
   *request* fails with no verdict on the file (`[R-MDL-01]`). Region
   request: clip to the layer's extents; a region wholly outside, or any
   region of a zero-extent layer, returns no samples.
2. **Ordinals.** tᵢ = xᵢ div Tᵢ, uᵢ = xᵢ mod Tᵢ; in-tile ordinal =
   Σ uᵢ·∏_{j>i}Tⱼ; spatial ordinal s = Σ tᵢ·∏_{j>i}Gⱼ; disk ordinal = s
   (interleaved) or c·N+s (planar, per requested channel c).
3. **Index chain.** Fetch/verify crc_of_crc_array over the (whole)
   segment-CRC array, and the one segment CRC covering the needed
   entry's segment; both fetches are independent of each other and MAY
   run in parallel; both MAY be cached once verified under
   committed-prefix immutability.
4. **Entry classification** (§15.3, exactly the table given): sentinel →
   short-circuit to fill, no payload I/O; any of the six *structural*
   malformed shapes → reject-tile with no further I/O for that tile;
   well-formed but not yet checksum-checked → proceed.
5. **Payload fetch + verify.** Fetch `[offset, offset+length)`, verify
   against the entry's crc field before decoding.
6. **Decode.** Codec first (reversing §17.1's writer order: writer
   applies filter then codec, so reader applies codec's inverse then
   filter's inverse), verify exact decode-size match to the
   declaration-derived decoded size (`[R-SER-07]`).
7. **Extract.** Byte offset of value k: planar numeric k·Bᶜ; interleaved
   (k div C)·Q + F_{k mod C}; planar bool bit k mod 8 of byte k div 8.
   Padding positions are never surfaced (`[R-GEO-04]`).
8. **Return** bit-for-bit, no alteration — except the one resolved case,
   an out-of-domain interleaved bool byte in a nonconforming file, which
   `[R-SER-08]` fixes to (0x00→false, anything else→true) rather than
   leaving reader behavior free.

For a region or multi-channel (planar) request spanning several tile-index
entries, a rejected entry's failure is bounded to the positions *that
entry* carries; the reader MAY return the good entries' values with a
per-entry failure report, or fail the whole request, but MUST NOT
substitute fill for a rejected tile's positions. A step-3 (index-chain)
failure is different in kind: it is layer-scope, so it bars the rest of
the request and all further service from that layer — but does not
retract values already returned earlier in the same session
(`[R-CNF-08]`'s "prospective" language, restated at `[R-RDR-04]`'s last
sentence).

## 5. Five degradation walks, end to end

**(a) Unknown ancillary record type, file scope, MU=0 (e.g. type 0x9000,
experimental range).** At open, step 4: type is not 0x0001/0x0002, MU=0 →
ignore-record (`[R-CNT-15]`). File stays otherwise usable; the layer
table is built exactly as if the record were absent. If an appender
later edits the file: it MUST NOT re-encode this record's payload
(`[R-WRT-08]`), and re-emits it byte-identically in the new directory
unless its PE bit (from the *definition it implements the type from*, if
it implements the type — otherwise from the stored bits, since it's
unimplemented) licenses a drop.

**(b) Unknown/reserved codec on a layer (e.g. codec value 7).** Not
caught at open (codec lives inside a layer record, not the directory
proper — wait, codec *is* a field of the layer record's inline payload,
which the directory does carry — so it is in fact checked at **layer
access**, not tile use: `[R-COD-03]` folds into §7.4's §19.3-cited
constraint set). Result: reject-layer, before any tile of that layer is
ever touched, whether or not the caller asked to read a tile. Other
layers are unaffected and still listed and readable.

**(c) Malformed enum value discovered only at tile use — codec 3 (zstd)
frame missing its magic on one specific tile (T17).** This is *not* a
layer-scope condition (the codec value itself, 3, is valid) — it is
per-tile, discovered only when that one tile is fetched and decoded.
Outcome: reject-tile for that one tile; sibling tiles of the same layer,
even ones compressed with the same codec, are unaffected, since each
tile is independently decodable from its own extent and the layer record
alone (`[R-COD-02]`).

**(d) Truncated tail (torn file — the physical file is longer than any
completed commit, e.g. because a writer crashed mid-append).** The
reader's step-2 fetch of the *physical* final 64 bytes lands on whatever
partial garbage the interrupted write left there (very likely failing
the trailer-magic or trailer-CRC test, F8/F14, or a plausible-looking-but-
wrong committed_file_length failing F17 against the transport size). The
default read path (`[R-LIF-05]`) reports the file torn/invalid and — this
is explicit and important — **MUST NOT scan backward** to find the last
good commit, even though that commit is still byte-intact on disk
untouched by the crash (`[R-LIF-01]`'s immutability guarantee is exactly
why it's still there). Recovering it is a *separate, deliberate* tool
operation (§9.6: probe 64-aligned offsets backward for the trailer magic,
require trailer-CRC + committed_file_length = offset+64 for a
"candidate," take the nearest-to-end candidate that survives a full
whole-file re-verification, and report how many rejected candidates it
skipped). A conforming reader never does this on its own.

**(e) Checksum mismatch on one stored tile (T1).** Detected at tile use,
step 5, before decode is attempted. Outcome: reject-tile, that tile only.
Neighboring tiles of the same layer — including ones physically adjacent
in a declared slab run — are unaffected; a region read spanning this
tile and others returns the others' values (optionally) alongside a
failure report for this one, but must never report fill for it
(`[R-CNF-09]`, `[R-TYP-09]`'s explicit statement that fill arises from
exactly one condition — a verified sentinel — and never from a failed
checksum).

**(f, bonus) Resource limit exceeded — entry_count declares 2⁴⁰ tiles and
the implementation cannot afford a segment-CRC-array-sized allocation at
that scale (well within `[R-ENC-04]`'s domain, and 2⁴⁰ ≥ §21.9's 2³²
guarantee floor, so a reader IS obliged to accept it if it can).** A
reader that cannot serve this MAY decline — at the narrowest scope that
exceeds what it can serve, here the layer — but MUST report the decline
as a resource limit, never as corruption (`[R-ERR-04]`); declining
*within* the guaranteed floor for any other reason disqualifies it from
being a conforming reader at all. I traced this specifically because
§21.9's guarantee table states minimums, not caps, and it is easy for an
implementer to conflate "big" with "invalid" — the document is explicit
that these are different failure modes with different required user-
facing language.

## 6. Worked example and arithmetic checks

I did not need to construct my own file: the document's own two worked
examples (Appendix A's 128-byte minimal file, and §7.4's rank-1 `sst`
layer with a 4-entry all-sentinel index) are fully specified byte-for-
byte, so I re-derived every checksum and count in them independently
rather than trusting the prose. All of the following were computed with
a from-scratch CRC-32C (verified first against the document's own two
check vectors) run with no file I/O, in my scratch directory:

- CRC-32C(`"123456789"`) = `0xE3069283` ✓ (matches §4.5's check vector)
- CRC-32C(``) = `0x00000000` ✓
- Appendix A trailer CRC over bytes `[0,60)`: I get `0x402F157E`,
  stored little-endian `7E 15 2F 40` — **matches** the document exactly.
- §7.4's `sst` example: the 80-byte all-sentinel entry array (4 ×
  `FF×16 00×4`) CRCs to `0x80A34955` (stored `55 49 A3 80`) — **matches**;
  CRC-32C of that one 4-byte segment-CRC array (crc_of_crc_array) is
  `0xC4EE982E` (stored `2E 98 EE C4`) — **matches**; entry_count×20 +
  ⌈entry_count/2¹⁶⌉×4 at entry_count=4 is 84 — **matches** the stated
  extent length.
- The full-all-sentinel-segment constant `[R-IDX-05]` states,
  `0xEECB3BB2`: I built the actual 1,310,720-byte buffer (65,536 ×
  20-byte sentinel entries) and ran my table-driven CRC-32C over it —
  **matches** exactly.
- §15.4's entry_count = 1,000,000 example: 16 segments (15 full +
  16,960), 64-byte CRC array, 20,000,064-byte index region, entry
  999,999 at segment-relative byte 339,180, CRC-array fetch
  `[20,000,000, 20,000,064)`, segment-15 fetch `[19,660,800,
  20,000,000)`, one full segment = 1,310,720 bytes = exactly 1.25 MiB,
  segment-CRC array at 2³² entries = 262,144 bytes = exactly 256 KiB,
  and at 2³⁶ entries = 4,194,304 bytes = exactly 4 MiB — **all
  recomputed and matching**.
- §11.4's linearization example (grid 4×8, coordinate (300,700)): tile
  (1,2), s=10, in-tile position (44,188), in-tile ordinal 11,452, planar
  channel-2 disk ordinal 74 — **all recomputed and matching**.
- Register-row completeness counts: I mechanically parsed every `| F#
  |`, `| L# |`, `| T# |`, `| R# |` row of §21.2–§21.5 and its Instances
  cell (splitting on `;`, treating a bare `—` as one instance). Result:
  **35 F-rows, 49 L-rows, 26 T-rows, 10 R-rows = 120 rows**, and **277
  total instances** — matching §21.1/§21.3/§21.4/§21.5's own stated
  counts ("35 conditions", "49 conditions", "26 conditions", "10
  conditions") and §21.8's "120 conditions over 277 instances" exactly.
  I did not find a single miscount here, which is itself worth recording
  as a clean result rather than an unchecked one.

## 7. Close reading of the changed surface — reasoning trail

I give the reasoning trail for the passages where I spent real time,
including the ones that turned out clean, because a clean passage I
checked is not the same as one I skipped.

**§20.1 writer tiers ("the choice is its own").** A tool producing a
brand-new file whose content derives from reading an existing one may
present itself as either a *rewriter* (an updater, carrying §20.4's and
§20.5's full preservation apparatus) or a *creator* (a plain writer,
bound only by §20.2, answering for every output byte with no
preservation undertaking at all, "bytes it copied from another file
included"). I checked this against `[R-LIF-01]`'s dichotomy ("every
conforming mutation of a file is either a commit or a whole-file
rewrite") for a contradiction — does declaring yourself a "creator"
let you escape being classified as "rewriting" the input file? I
concluded no genuine tension: `[R-LIF-01]` binds *mutation of a file*,
which is a relationship an updater stands in to the specific file whose
generation it extends or supersedes; a creator's input is read only as a
data source, not as a file it is mutating — nothing in the file it reads
changes state, gets a new generation, or is claimed by the creator's
output at all. This reading is internally consistent (§20.2 requires the
creator to follow the full creation path with a fresh nonzero file_id,
exactly `[R-LIF-02]`'s zero-prior-generation case), and I could not
construct a file whose bytes or accept/reject verdict this choice would
change — it is a classification of the *actor's undertaking*, not of the
bytes, exactly as `[R-CNF-02]` already establishes for every conduct
rule. Not byte-level. I list it as a rejected candidate rather than a
finding.

**§20.3 step 4, "the two lists reach every declaration field of §7.4,
and where a field is on both sides — a planar layer's channel list, an
interleaved layer's channel list — the permitted side states the whole
of what a commit MAY do to it."** On first reading this looks like it
claims each named item is literally written into *both* enumerations
above it — but the permitted list only ever names "a planar layer's
channel list" (extend/shorten at the end) and the fixed list only ever
names "an interleaved layer's channel list" (membership/order fixed,
names aside). Taken that literally, neither named item is actually
present in both lists, which would make the sentence false on its face.
I resolved this by finding the fields that genuinely do straddle both
lists: (1) the *permitted* list's blanket "its dimension and channel
names, MAY change" reaches an interleaved layer's channel list too (only
its names, not membership/order — consistent with the fixed list's own
parenthetical "(its names aside)"); and (2) the *fixed* list's "the
position of every planar channel the new state keeps" reaches a planar
layer's channel list (positions of retained channels are frozen even
though the list's length is not). Under that reading the sentence is
true — each layout's channel-list field really does have one component
in each list — but the sentence's compressed phrasing ("a field is on
both sides — [name], [name]") reads at first pass as naming the two list
items directly, and only resolves correctly once a reader goes back and
re-derives which specific clause in the *other* list secretly reaches
each one. This is the "sentence rewritten to close a reading" shape
(heuristic #11): it is very likely correct, but it is not free-standing —
an implementer who trusts the parenthetical's face-value pairing without
doing this cross-check could misjudge what a commit may do to an
interleaved layer's channel names, or to a planar layer's retained
channel order. I flag this below as an AMBIGUITY (resolved by me, but
worth a human read) rather than a CONTRADICTION, since I could not
construct two conforming implementations that would actually diverge on
bytes once each has done the same cross-check — the four component
clauses concerned agree in all four combinations. Not byte-level.

**§20.4's MU=1 row ("the updater MUST NOT modify the scope the record
governs") versus the appender's actual behavior on an unknown critical
sub-record ("blocks modification of that layer... leaving other layers
editable") versus the rewriter's behavior on the same condition ("MUST
refuse to rewrite the file, on `[R-WRT-06]`'s own ground").** I checked
whether these three statements are mutually consistent for an appender
versus total for a rewriter given the *same* triggering condition
(unimplemented MU=1 sub-record). They are, and the document does supply
the reasoning, distributed rather than stated in one place: an appender
never moves or rewrites any existing byte outside the layer it is
actively modifying (`[R-LIF-01]`'s immutable-prefix guarantee), so an
unknown record's undocumented internal references — wherever they point
— stay valid as long as the appender leaves that record's own containing
layer untouched; a rewriter, by definition, reproduces the *entire* file
from scratch into new byte positions (§20.5: "carrying no slack," "MAY
add what a creator could"), so no byte position anywhere in the output is
guaranteed to match the input, and an unknown record's internal
references cannot be guaranteed valid at any placement the rewriter
might choose. I could not find this specific comparative argument spelled
out in one sentence — it has to be assembled from `[R-LIF-01]`, R-WRT-04's
"relocating a live index region is a rewriter's operation, not an
appender's," and R-WRT-06's "cannot be safely relocated" — so this is a
case where "for any rule you can only defend by reasoning you supply
yourself, ask whether the document supplies it" bites: the document
supplies the pieces but not the assembled argument. I record this as an
OBSERVATION (decidable, but expensive to decide) rather than a finding
against the rule itself, since I could not find any way the two rules
actually disagree on bytes.

**§18.2's transposition of `[R-COD-06]`'s tile-window rule onto a
document's window ("the tile rule of `[R-COD-06]` transposed to the
quantity a document does have, its decoded length, in place of the
declared size it does not").** I checked whether the document's own
"decoded length" is well-defined at the point R4's content-size check
runs, given decoding could itself fail for other reasons first (frame
constraint violations independent of content-size). R3's note ("where
the encoding is 2 and what fails is one of the frame constraints R4
registers, R4 is the row, whether or not the bytes also fail to decode")
answers this directly and correctly resolves the ordering question I had
— R4 is checkable from the frame's own header fields and the decoded
byte count without needing the *rest* of decode to succeed, so there is
no circularity. Rejected candidate, not a finding.

**§22.3's four "residues... stated rather than defended."** I checked
this list (slack; the extent of an unassigned-type record; a trailer-
mimicking payload; an experimental-encoding metadata extent) against
§21's register and §21.6's non-violation table for a fifth undefended
residue the list might have missed — specifically, a stored tile's
*decoded content* under a wrong-stride filter or a mis-declared fill,
which §21.7 already separately and explicitly calls out as "unwitnessed."
I confirmed §21.7 is a *different* subsection addressing a *different*
question (content correctness generally, not byte-coverage residues
specifically) and that §22.3's four-item list is scoped to structural/
coverage residues, so it is not actually incomplete relative to its own
stated scope. Rejected candidate.

## 8. Findings

### reader-01 — AMBIGUITY

**Location.** §20.3, step 4, the paragraph beginning "Between them the
two lists reach every declaration field of §7.4..."

**Quotation.** "Between them the two lists reach every declaration field
of §7.4, and where a field is on both sides — a planar layer's channel
list, an interleaved layer's channel list — the permitted side states
the whole of what a commit MAY do to it; entry_count and crc_of_crc_array
follow the commit, the record's extent slot with them (§7.2), and a
layer's sub-records are §20.4's subject whether or not the layer stores
a tile."

**Every permitted reading, which I picked, and why.** Reading A (face
value): "a planar layer's channel list" and "an interleaved layer's
channel list" are each claimed to literally appear as line items in
*both* the permitted-changes enumeration and the fixed-declarations
enumeration a few paragraphs earlier. Textually false: the permitted
list names only "a planar layer's channel list" (extend/shorten at the
end); the fixed list names only "an interleaved layer's channel list
(its names aside)." Neither layout's channel list, read as a whole
undivided item, is named in both places.

Reading B (the one I adopted): "a field" here means the abstract
"channel list" declaration of §7.4, and the sentence is asserting that
*each layout's version of it* has one governing clause sitting in each
list — not that the exact phrase recurs. Under Reading B: a planar
layer's channel list is governed by the permitted list's "extend/shorten
at the end" clause *and* by the fixed list's "the position of every
planar channel the new state keeps"; an interleaved layer's channel list
is governed by the fixed list's "(its names aside)" parenthetical
*and* by the permitted list's blanket "its dimension and channel names,
MAY change." I verified all four component clauses are mutually
consistent under Reading B and could not construct a file or a commit
that two implementations following Reading B would classify differently.

**Why it matters even though I resolved it.** An implementer working
from a single pass over this sentence, without independently re-deriving
which clause in the *other* enumeration secretly reaches "the interleaved
case" or "the planar case," is likely to read Reading A, notice it looks
false against the two enumerations as literally written, and either (a)
conclude the document contradicts itself, or (b) silently patch their own
understanding without checking it against the fixed list's "position of
every planar channel" clause and the permitted list's names-only clause,
which are the two pieces that actually make Reading B — and hence the
sentence — true. This is exactly a "sentence rewritten to close a
reading" case (task heuristic #11): the sentence is very likely correct
under the intended reading, but the reading has to be reconstructed, not
read off the page, and I could not find independent textual signal
inside this sentence disambiguating which of the two it means.

**Byte-level?** No. `byte_level: false`. Once resolved (either by me or
by any other careful reader doing the same cross-check I did), both
readings converge on the same set of permitted/forbidden commits — I
could not find a commit that Reading A and Reading B would classify
differently, because Reading A is simply false as a literal claim rather
than a live alternative rule. This is a clarity/ambiguity finding about
how expensive the sentence is to parse correctly, not a fork in what
bytes a conforming implementation may emit or accept.

### reader-02 — OBSERVATION

**Location.** §20.4 (the governing-flags table's MU=1 row and its
lead-in paragraph) together with §20.5's rewriter-refusal sentence in
`[R-WRT-06]`.

**Quotation.** §20.4: "MU = 1 | Retain byte-identical. The updater MUST
NOT modify the scope the record governs. At layer scope an unknown
critical record blocks modification of that layer, its drop included,
leaving other layers editable... At either scope a rewriter MUST refuse
to rewrite the file, on `[R-WRT-06]`'s own ground: such a type can define
references this specification does not (§7.2), so its bytes cannot be
safely relocated." §20.5, `[R-WRT-06]`: "A rewriter MUST refuse to
rewrite a file carrying any record whose type it does not implement with
MU = 1: such a type can define references this specification does not
(§7.2), so its bytes cannot be safely relocated."

**What is decidable but expensive.** The document states, correctly and
without contradiction, that an appender facing an unimplemented MU=1
sub-record is confined to *that one layer* (other layers stay editable,
and the appender can still commit changes elsewhere), while a rewriter
facing the identical condition anywhere in the file must refuse the
*entire* rewrite, including layers wholly unrelated to the one carrying
the record. Both rules are individually stated plainly. What is not
stated in one place is *why* the scope of the block differs so sharply
between the two actor types for the same triggering condition — an
implementer has to assemble the justification from `[R-LIF-01]`'s
committed-prefix immutability (an appender never relocates any existing
byte outside the layer it is actively touching, so an opaque record's
undisclosed internal references, wherever they point, remain valid
regardless of what else the appender's commit does) together with
§20.5's "carrying no slack" / whole-file-reconstruction character of a
rewrite (no byte position anywhere in a rewritten output is guaranteed to
match the input, so an opaque record's references cannot be guaranteed
valid at any rewriter-chosen placement). I was able to reconstruct this
and found no case where it fails, but the document does not spell out
the comparison; it states each actor's rule on its own terms in a
different section, and the "why they differ" step is left to the reader.

**Byte-level?** No. `byte_level: false`. I could not find a file or a
commit sequence where the appender-rule and the rewriter-rule, both
correctly applied, would produce or accept different bytes than intended
— they operate over disjoint actor types performing disjoint operations,
and each rule is unambiguous once isolated. This is reported because the
task brief explicitly asks, for every rule defended only by
reader-supplied reasoning, whether the document supplies it — here it
does not, in one place, though it is fully reconstructible from three
separate rules taken together.

## 9. Confidence and residual uncertainty

I read the entire document once end to end and re-read the 31 named
changed passages a second time against the twelve heuristics, and spent
targeted extra effort on the passages that read as the freshest and
least-reviewed text per the brief's own framing (§20.1, §20.3 step 4,
§20.4, §20.5, §7.2's MU/PE-not-orthogonal note, §5.2, §9.7, §21.1,
§21.6). I did not find a byte-level fork despite specifically constructing
adversarial readings of the two most heavily rewritten paragraphs I
found (§20.3 step 4's "both sides" sentence, and the appender/rewriter
MU=1 asymmetry). I do not have visibility into what the two prior audits
in this cycle already found and fixed, so I cannot rule out that a
narrower, more surgical defect survives somewhere I read past too
quickly — the document is 4,981 lines and I could not give every sentence
the same depth of adversarial construction I gave the two flagged above.
Where I found little (Part II's channel/type/fill machinery, §16's slab
arithmetic, §22–§23's security/privacy sections, the appendices other
than the arithmetic I re-derived), I did read every sentence and checked
it against the twelve heuristics in the single pass, but did not
separately attempt to hand-build adversarial files for each one the way
I did for the two findings above; a genuinely well-hidden defect in those
areas could have survived a single careful read without a dedicated
construction attempt.
