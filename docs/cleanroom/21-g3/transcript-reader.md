# Cleanroom round 21 — Reader implementer transcript

Working transcript of an implementation walk: build a conforming TARN reader on paper
and in code, from `spec/tarn.md` alone, stopping wherever the text failed to tell me
what to do.

---

## 0. Disclosure, up front

**What I read.** `/Users/robertkleffner/Documents/GitHub/tarn/spec/tarn.md`, in five
passes covering all 4,377 lines. Nothing else in the repository. No `docs/`, no ADRs,
no `PLAN.md`, no `AGENTS.md`, no `conformance/`, no `spec/registry.json`, no git
history, no web.

**What I ran.** Local Python only, reading no repository file: a CRC-32C
implementation built from §4.5's stated parameters; a file builder that emits a
conforming two-layer TARN file; a reader that opens and decodes it; and a mutator that
authors ~30 damaged variants and runs the reader over each.

**Two contamination events, both disclosed rather than hidden.**

1. *Shared scratchpad collision.* The scratchpad path this session was given is shared
   with the other agents of this round, and they were writing into it concurrently
   under colliding filenames. Partway through my walk my `crc.py`, `reader.py` and
   `walk.tarn` were overwritten by another agent's files of the same name. One
   invocation of my `run.py` therefore executed a `reader.py` and a `walk.tarn` that
   were not mine. What I saw from that run was program output only: a layer-name list
   (`empty`, `grid`, `mask`), a file length of 1088, and a directory range — i.e.
   another agent's test fixture, not specification text and not a conclusion about the
   specification. I did not open any transcript, and I did not list or read the
   `round21/` output directory. I did list the *parent* scratchpad directory (which is
   how I discovered the collision), and in doing so saw the names of other agents'
   scratch files. On discovering this I moved to a private, uniquely-named
   subdirectory (`rdr21-private-9f3a/`) and **redid the entire walk from scratch**
   — CRC library, file builder, reader, and every degradation case. Every number in
   this transcript comes from the redone run.
2. *Unrequested context.* Before I began, my runtime placed in context a project
   instruction file pointing at `AGENTS.md`, an index of the maintainer's memory notes
   (with titles referring to a working cadence, a naming rule, a register/corpus
   relationship, and prior workflow failures), and a task list naming prior rounds and
   ADR numbers. I did not open any of the files named, and no finding or non-finding
   below rests on any of it. I name that it appeared; I do not repeat its contents.

---

## 1. Where I started, and the order I built in

I built in the order a reader actually executes: open → validation timing → layer
access → tile read → degradation. I did not read Part III first; I read §2 (as §1
advises), then Part I, then Part II, then Part III, then §21, then the appendices,
and only then started writing code. The code is the check on the reading.

Two decisions up front, because everything else hangs on them:

- **§2.1 binds BCP 14 keywords only in all capitals.** So every time I met a
  declarative outcome sentence with no modal — and there are many — I had to find the
  MUST that binds it. The document has a consistent architecture for this, which I did
  not appreciate until late: `[R-CNF-04]` ("A reader MUST detect every violation the
  error register (§21) assigns to the reader as its detector, and apply the outcome
  class this specification assigns to each") is the engine for every registered
  condition, and §2.4's outcome table supplies the modal for the outcome itself
  ("reject-file … A reader MUST NOT rely on any structure in it"). For the *decode*
  path — where §14, §17.1, §17.3 and §11.4 are all purely declarative, with no reader
  modal anywhere — the binding MUST is `[R-MDL-02]`: "a conforming reader that reads
  any portion of a layer MUST return exactly the corresponding portion of the
  reference array, bit-for-bit". A reader that skipped the inverse filter, or got
  `[R-GEO-06]`'s ordinal arithmetic wrong, would violate `[R-MDL-02]` even though
  neither §17.3 nor §11.4 contains a keyword. That is a clean architecture and I want
  to record that I checked it rather than assumed it.
- **§21.1's precedence.** "each row *restates* its governing rule, and where a row and
  the rule it cites diverge, the rule governs." So a wrong register row is a table
  defect, not an open verdict. I used the register as an inventory to check my
  implementation against, never as authority.

---

## 2. The open path, byte-exact

### 2.1 What §19.1 obliges

Four steps, in order.

**Step 1 — end of file.** Obtain the *transport-authoritative* size F (`[R-CNT-10]`).
The rule is emphatic that this may not be the trailer's own
`committed_file_length`: "a reader that cannot obtain one MUST probe separately or
fail the open, and MUST NOT substitute the trailer's committed_file_length for the
transport size." Steps 1 and 2 cost one request between them because the suffix
range's response carries F.

Residency, not transport, decides the front-block obligation (`[R-CNT-04]`): a reader
whose open leaves [0,16) resident MUST verify all 16 bytes by equality *before other
processing*; one that would have to issue a further range request MAY defer or omit.
I built a remote reader that fetches exactly two ranges, so [0,16) is never resident
and the check is deferred — legitimately, and §6.4's accounting explicitly excludes
the front block.

**Step 2 — trailer.** Fetch [F−64, F). §6.2 fixes the validation order and it is not
optional: magic, then trailer CRC, then the version gate — "only these touch fields
whose positions are fixed across all majors (`[R-CNT-24]`)" — and only then the
remaining field gates, which §6.2 enumerates as a set with no order among them.

I implemented exactly that split, and it matters: §21.2's preamble turns on it. A file
declaring format major 7 is "neither conforming nor nonconforming under this text", so
most rows do not reach it — but F8 (trailer magic), F14 (trailer CRC) and F1's
trailer-magic instance do, because §6.2 puts those two checks *ahead* of the gate; and
F6 plus F1's front-block instance reach it because `[R-CNT-04]` places the front-block
check "before other processing". I verified §6.3's permanence claim arithmetically:
magic at F−64 (8 bytes), version_major/minor at F−56 (4 bytes), CRC at F−4 covering
[F−64, F−4) = trailer offsets [0,60). 64 − 8 − 4 − 4 = 48, which is exactly "the
remaining 48 trailer bytes" a future major MAY redefine. And the trailer's field
offsets sum: 8+2+2+4+8+8+8+8+8+4+4 = 64, so §6.3's "the format-major-1 trailer has
zero slack" is true.

One detail I had to decide and the text decides for me: `file_id` is **not** subject to
`[R-ENC-03]`'s 2⁶³−1 domain. §4.2 binds "every offset, length, extent, and count";
file_id is none of those, and §6.2's Valid-values cell says only "≠ 0". F2's instance
list confirms it by omission (`dir_offset; dir_length; committed_file_length;
generation; non-layer top-level record extent_offset; extent_length` — six, no
file_id). Appendix G item 2 corroborates: a file_id derived from "the digest's last
eight bytes in output order, read little-endian" routinely exceeds 2⁶³−1. So a
conforming file may carry file_id = 0xFFFFFFFFFFFFFFFF. `generation`, by contrast, *is*
a count and is capped (F11 covers 0, F2 covers > 2⁶³−1).

**Step 3 — directory.** Fetch [dir_offset, dir_offset + dir_length) and verify the
terminal CRC "before any other use of the region". What bounds that range before I have
read it: dir_offset ≥ 16, dir_length ≥ 4, dir_offset + dir_length ≤ F − 64, and the
non-overflow of that sum — every one of them a field of the trailer whose CRC I have
already verified. So `[R-ENC-05]` ("MUST NOT allocate, seek, or issue I/O based on any
integer obtained from a file before the checksum covering it has been verified") is
satisfiable at every link of the chain, which I checked exhaustively: trailer suffix
range is bounded by the transport size, not by a file integer; the directory range by
CRC-verified trailer fields; the index CRC-array and segment ranges by CRC-verified
directory fields; the tile payload range by a segment-CRC-verified entry. No gap.

**Step 4 — record walk.** Parse under §7.2's framing, apply the MU gate for unknown
top-level types, the multiplicity rules, the extent-slot rules for *non-layer*
top-level records, the user-metadata framing rules (no (0,0) slot, extent_length ≥ 5,
inline_length exactly 1), and build the layer-name table.

### 2.2 A place I had to reason hard: are an *ignored* record's bytes still checked?

This is the first place I stopped. A top-level record of experimental type 0x8001 with
MU = 0 is ignore-record, and §2.4 defines ignore-record as "The record is skipped as
though absent." If it is absent, does its extent slot exist to be malformed? Suppose
its slot is (0, 100) — offset zero, length nonzero.

Reading A: skipped as absent → no slot → file accepted.
Reading B: §19.1 step 4 says the record walk applies "the extent-slot validity rules
for non-layer top-level records (`[R-CNT-13]`)", unqualified; F30 ("A non-layer
top-level record's extent slot has exactly one half zero") is reader/open/reject-file;
`[R-CNF-04]` makes that a MUST → reject-file.

I picked B, and the document says so in four places, not one:

- §19.1 step 4's enumeration carries no carve-out for ignored records.
- §5.2 `[R-CNT-02]` defines a structure as "a record extent (the bytes any record's
  extent slot references, **whatever the record's type**, §7.2)" — the emphasis is the
  document's own point, not mine.
- §9.7 `[R-LIF-08]`'s walk reaches "each record's extent", unqualified.
- §7.2 explains *why* the slot must be well formed for an unknown record: "this is what
  lets a compactor relocate an unknown ancillary's extent without parsing it".

So ignore-record bounds what the reader *serves*, not which of the record's own framing
fields it validates. My reader validates the slot of every top-level record and rejects
the file on F30/F31/F32 regardless of type. Determined; not a finding.

### 2.3 The layer-name namespace, which is subtler than it looks

§19.1 step 4 puts duplicate-name detection at the open and makes it file scope
(`[R-ENC-15]`, F4). Three sub-rules I had to get right:

- Uniqueness is decided **first**, and **over raw bytes**, "whether or not each name is
  itself well-formed — `[R-ENC-13]` makes name comparison a byte comparison, which
  needs no valid name". So two layers with byte-identical *ill-formed* names are a
  duplicate → reject-file, and the reject-layer rows for the malformed names never get
  a chance to fire.
- A layer record whose name field does not lie within its own `inline_length` "yields
  no name field to compare, so it contributes no name to the namespace and is instead a
  validity error at layer scope". My reader emits `None` for such a record and excludes
  it from the namespace.
- L3/L5/L6 (the layer record's own name: ill-formed UTF-8, empty, C0 control) carry
  **Detected: open** and outcome **reject-layer** — a layer-scope verdict established at
  the open, before any layer access. L4/L7/L8 (dimension and channel names) are at layer
  access. My reader parses the layer name at open and defers everything else.

### 2.4 Byte-exact cold remote open

Built and measured against my own conforming file (details in §6 below):

```
request 1   suffix range, final 64 bytes      [576, 640)      64 bytes
request 2   directory                          [270, 528)     258 bytes
                                              ---------------------------
                                               2 requests     322 bytes
```

Generally: **2 requests, 64 + dir_length bytes.** The front block is not fetched. No
extent slot's content, no tile index, no payload (`[R-RDR-01]`). The alternative §6.4
licenses — one speculative suffix window, containment-tested — collapses this to
**1 request**; on Appendix A's 128-byte file a window that reaches offset 0 also makes
the front block resident and so *arms* `[R-CNT-04]`'s MUST, which is exactly the point
of the residency-not-transport test.

What bounds request 2 before it is read: dir_offset ≥ 16, dir_length ≥ 4,
dir_offset + dir_length ≤ F − 64, sum non-overflowing — all from the CRC-verified
trailer. Nothing else is fetchable at the open, at any file size or layer count. I
confirmed §21.9's Note is consistent with this: the 16 MiB `dir_length` guarantee is
sized against the fact that §19.1 "fetches and CRCs it whole before any other use".

---

## 3. Validation timing by tier

I built this as a table before writing code, because `[R-RDR-02]` fixes the *latest*
detection point and `[R-CNF-12]` licenses any earlier one — so the only thing an
implementation can get wrong is being late.

**At open:** front block (if resident); trailer magic/CRC/version gate/flag gates and
every trailer field gate; directory CRC; record framing and residue; type 0; top-level
multiplicity; extent slots of non-layer top-level records; top-level user-metadata
framing (slot, extent_length ≥ 5, inline_length = 1) *and its encoding byte's value set*
(R1's Detected cell says "open (top-level)"); layer-name parse and namespace.

Note that §19.1 step 4 does **not** restate the encoding-byte value-set check, and I
briefly took that for a gap. §19's preamble closes it explicitly: "Those enumerations
are not the complete inventory of what a reader detects at that tier: §21's register
is, and `[R-CNF-04]` binds a reader to every register row whose detector is the reader,
at the tier that row's *Detected* cell names." So the register is the inventory and
§19 is the narrative. I checked every §21 row's Detected cell against my tier table on
that basis.

**At first access to a layer** — "the first operation using any of the layer's
declarations *other than its name*", so listing layers does not arm it — the whole of
§19.3: extent slot; the §7.4 constraint set; exact parse, sub-record walk and sub-record
multiplicity; dimension/channel name rules; field widths and the u64 domain; the value
sets of §11.4, §12.2, §14.1, §15.1, §17.2, §17.3; bool fill; the lz4 declaration cap;
the geometry floor and its arithmetic; the 2⁶³−1 ceiling on every derived product
including §14's decoded sizes; and the index cross-checks computable without I/O
(`[R-CNT-17]`). **"layer access performs no fetch"** — I verified this is achievable:
every one of those is decidable from the resident directory and F.

**At use of a tile:** index chain (`[R-IDX-04]`), entry classification (`[R-IDX-03]`),
payload CRC, codec/filter/decode-size checks. Note the scope inversion §19.2 calls out
explicitly: L37/L38 are detected at *tile use* but take *layer* scope.

**At use of a record's extent:** that extent's CRC (R2) and the document content rules
(R3–R10) — "no earlier, since the open fetches no extent". A reader that never reads
user metadata never detects R2–R10, and §19.2 says so: "Structures a request never
relies on impose no detection obligation beyond the open steps."

**What a reader is permitted never to check.** I extracted this mechanically from the
register's Detector column: 20 of the 121 rows carry Detector *verifier* —
F7, F25, F26, F27, F28, F33, F36; L18, L25, L40, L41, L42, L46, L47, L48, L49;
T2, T4, T5, T26 — and 101 carry *reader*. So a conforming reader never owes: the
live-state coverage partition; any overlap check; alignment and slab invariants;
padding-position content; pad bits; interleaved boolean byte values; reserved flag
bits; MU = 1 with PE = 0; a registered type's stored flag bits; user-metadata member
ordering; a reserved-range record or sub-record type value as such; a structure sitting
in the pre-trailer gap; slack content; and the front block when not resident. §2.4's
`[R-CNF-09]` still binds it not to *serve* from a scope it is obliged to reject — the
"and whose rejection this reader is obliged to detect" clause is what keeps that from
over-reaching onto verifier-only rows.

---

## 4. Layer access and the tile-read algorithm

### 4.1 Parsing the layer record

§7.4's table is packed with no alignment or padding, and `[R-CNT-18]` demands it "parse
exactly … with no residue". The fill field's length prefix is what makes the payload
parseable without type knowledge and then cross-checkable with it (`[R-CNT-23]`): fill
length must equal the type's element size, so L30 is a reader-detected layer-scope
error at layer access.

I derived the geometry per §11.2 in the stated ceiling-division form — Eᵢ/Tᵢ plus 1 if
Eᵢ mod Tᵢ ≠ 0, *not* (Eᵢ+Tᵢ−1)/Tᵢ, whose intermediate sum the Note correctly points
out can leave the declared domain — and checked every product against `[R-ENC-04]`:
N, P, N·P, C·N, P·Q, P·Bᶜ, and entry_count × 20 + ⌈entry_count/2¹⁶⌉ × 4. L2's instance
list is exactly these nine.

One case I checked deliberately because §17.2's Note is non-normative and I could not
rely on it: **does a layer with zero addressed tiles still have its decoded size
overflow-checked?** The Note says yes for `[R-ENC-04]` and no for the lz4 cap. I
confirmed both from normative text alone: `[R-COD-07]` is quantified over the layer's
*addressed* tiles ("any of whose addressed tiles' decoded size exceeds"), so an
E=0 layer escapes it; whereas `[R-SER-02]` ("These products and sums are
declaration-derived quantities under `[R-ENC-04]`") and `[R-SER-07]` ("Every decoded
size, and the value count V, is a declaration-derived quantity under `[R-ENC-04]`") are
normative and carry no such quantifier, and §11.2 defines P = ∏Tᵢ unconditionally.
So a rank-2 layer with T = (2⁴⁰, 2⁴⁰) and E = (0, 0) is reject-layer on L2 even though
it addresses no tile. My reader implements exactly that split.

### 4.2 The index chain

Both ranges are computable from the layer record alone, which I verified:

- CRC array: [extent_offset + entry_count·20, extent_offset + entry_count·20 +
  ⌈entry_count/2¹⁶⌉·4)
- segment s: [extent_offset + s·2¹⁶·20, extent_offset + min((s+1)·2¹⁶, entry_count)·20)

`[R-IDX-04]` says both MAY be fetched in parallel, and §15.4's Note licenses caching the
verification under committed-prefix immutability. The array is fetched **whole** — the
CRC covering it is crc_of_crc_array, which covers the whole array, and §21.9's Note
confirms ("the segment-CRC array a reader fetches whole before using any entry").

I reproduced §15.4's big example exactly: entry_count = 1,000,000 → 16 segments (15
full, last covering 16,960), 64-byte array, region 20,000,064 bytes; k = 999,999 in
segment 15 at segment-relative byte 339,180; array at region [20,000,000, 20,000,064),
segment 15 at [19,660,800, 20,000,000) = 339,200 bytes. A full segment is 65,536·20 =
1,310,720 = 1.25 MiB. At the 2³² entry_count guarantee the array is 256 KiB; at 2³⁶ it
is 4 MiB. Every figure the document states.

### 4.3 Entry classification, and a property worth recording

`[R-IDX-03]`'s eight reader rows partition cleanly, which I checked case by case. The
one that needed care: an entry with offset = length = 2⁶⁴−1 and crc ≠ 0 is **not** a
sentinel (`[R-IDX-02]` makes the sentinel the full three-field pattern), so it is
"non-sentinel" for the domain rows too and matches both T6 and T11-by-value. Both give
reject-tile on a structural ground, so no divergence. T11's instance text closes the
overlap explicitly — "the value being distinct from the all-ones sentinel".

Six rows are marked *structural* (I counted: rows 2–7 of the table = 6, matching the
prose). The consequence is stated in three places and they agree: such an entry
contributes no stored extent to the verifier overlap rows, none to `[R-SLB-03]`'s run
continuity, and none to `[R-LIF-08]`'s coverage walk; whereas an entry whose *only*
defect is that its stored bytes fail its crc is well-formed, keeps its extent, and
stays in all three.

**A property my degradation runs surfaced that is worth writing down:** T6–T12 are
unreachable by *corruption*. Flipping any byte of an index entry breaks its segment CRC,
so the reader takes L38 (reject-layer) and never reaches the entry classification at
all. To exercise T6–T12 I had to *author* the malformation and recompute the segment
CRC and crc_of_crc_array. So `[R-IDX-03]`'s structural rows are rows about
writer-produced files, never about damaged ones — which is precisely what §15.2's
Rationale claims ("a damaged entry rejects the tile rather than filling it" is the
weaker statement; in fact a damaged entry rejects the *layer*). I record it because a
corpus builder needs to know that these vectors cannot be produced by bit-flipping a
good file.

### 4.4 The decode pipeline, in order

`[R-COD-01]`: writer applies filter then codec; reader reverses — codec decode, then
filter inverse, then `[R-SER-07]`'s exact-size check. I confirmed the length algebra
holds so the order can never be observed through a length: `[R-COD-10]` says "Length is
unchanged", and the divisibility claim ("The decoded image's length L is divisible by s
in every case") checks out for all three shapes — interleaved L = P·Q with s = Q;
planar numeric L = P·Bᶜ with s = Bᶜ; packed bool plane L = ⌈P/8⌉ with s = 1 and the
filter the identity.

For a planar tile the shuffle stride is "the channel's element size", so the reader
needs c — which it has from `[R-GEO-06]`'s inverse, c = k div N, s = k mod N. The one
place where the two statements in §17.3 could have conflicted (a planar *bool* channel:
"the channel's element size" = 1 by §12.1, versus "for a packed boolean plane s = 1")
they agree.

### 4.5 Exact decoded byte layout

I derived it and then checked it against every worked example in §14:

- **interleaved**: decoded size P·Q; channel c at in-tile ordinal u sits at
  byte u·Q + Fᶜ where Q = ΣBᵢ and Fᶜ = Σ_{j<c} Bⱼ. Verified against §14.2's example
  (P = 6, uint8 + uint16: Q = 3, size 18, ordinal 5 at [15,18)); the float32+bool case
  (Q = 5, size 30, ordinal 5 at [25,30) with the bool the single byte at 29).
- **planar numeric**: size P·Bᶜ, value k at k·Bᶜ. Verified (channel `b`'s tile 12
  bytes, ordinal 5 at bytes 10–11).
- **planar bool**: bit-packed LSB-first, size ⌈P/8⌉, value k at bit k mod 8 of byte
  k div 8. Reproduced §14.3's example exactly: P = 10, alternating → `55 01` with fill
  false, `55 FD` with fill true (pad bits 2–7 carrying the fill bit).

### 4.6 Sparse and fill

`[R-TYP-08]` and §19.4 step 4: a valid sentinel short-circuits the payload fetch, and
every requested position *inside the extents* reads as fill — each carried channel's
in declared order (interleaved), or exactly the entry's channel's (planar), bit-exactly.
`[R-TYP-09]` is the hard edge: fill is produced by **exactly one** condition, a sentinel
entry read from a verified chain. A malformed entry, a failed segment or array CRC, or
failed stored bytes reject their scope, and "a rejection is never satisfied by returning
fill". My degradation runs confirm my reader honours this: in the T6 case, entry 1 is
reject-tile while entry 2 (a genuine sentinel in the same segment) still reads as fill
and entries 0 and 3 still decode — tile-scope blast radius, exactly as §2.4 promises.

---

## 5. Degradation walks

Twenty-seven traced end to end against constructed files. All determined; no guesses.

| # | Injected condition | Reader outcome | Still served |
|---|---|---|---|
| 1 | unknown top-level type 0x8001, MU = 0, PE = 1, valid extent | ignore-record; file **conforming** (§21.6) | everything |
| 2 | same, MU = 1 | reject-file — a *capability* refusal, file still conforming (§21.6, `[R-CNF-02]`) | nothing |
| 2b | reserved-range type 0x0003, MU = 1 | reject-file (F35) | nothing |
| 2c | reserved-range type 0x0003, MU = 0 | ignore-record for the reader; F36 is the verifier's row | everything |
| 3 | unknown MU = 0 record, extent slot (0, 100) | reject-file (F30) — §2.2 above | nothing |
| 4 | layer `img` codec = 5 (reserved) | reject-layer (L43) at layer access | layer `sst` |
| 5 | layer `img` linearization = 0x8001 (experimental) | reject-layer (L33) | layer `sst` |
| 6 | duplicate layer name | reject-file (F4) at open | nothing |
| 7 | physical file truncated by 8 bytes | reject-file (F8); MUST NOT scan backward (`[R-LIF-05]`) | nothing |
| 8 | physical file extended by 64 zero bytes | reject-file (F8) — §9.5's Note: residue is met as a failed trailer gate, and the reader "cannot tell residue from corruption and is not asked to" | nothing |
| 9 | version_major = 2 | refuse on **capability** grounds, diagnostic distinct from "not a TARN file" and from "corrupt" (`[R-CNT-07]`) | nothing |
| 10 | incompat-lane bit 0 set | reject-file (F19) | nothing |
| 11 | ignore-lane bit 16 set | ignored; file conforming | everything |
| 12 | metadata encoding 0x85 (experimental) | ignore-record; **non-violation**; verifier certifies and reports scope/encoding/extent length (`[R-MTA-10]`) | everything |
| 13 | metadata encoding 0 | ignore-record; **violation** (R1) | everything |
| 14 | one byte of stored tile 0 flipped | reject-tile (T1) | tiles 1,2 as fill; tile 3 decoded; layer `sst` |
| 15 | one byte inside an index segment flipped | reject-**layer** (L38) — note the scope escalation | layer `sst` |
| 16 | segment-CRC-array byte flipped | reject-layer (L37) | layer `sst` |
| 17 | *authored* sentinel with crc ≠ 0 | reject-tile (T6) | the other three tiles, sentinels included |
| 18 | *authored* entry with offset = S, length = 123 | reject-tile (T7) | the rest |
| 19 | *authored* non-sentinel length 0 | reject-tile (T10) | the rest |
| 20 | *authored* offset 15 | reject-tile (T8) | the rest |
| 21 | *authored* extent past F − 64 | reject-tile (T9) | the rest |
| 22 | *authored* offset with bit 63 set | reject-tile (T11) | the rest |
| 23 | *authored* codec-1 length 13 ≠ decoded size 12 | reject-tile (T14), **before any payload fetch** (`[R-COD-04]`) | the rest |
| 24 | layer sub-record type 0x8002 MU = 1 | reject-**layer**; `[R-CNT-18]`: "where the file is otherwise conforming a reader MUST NOT reject the file for it" | layer `sst` |
| 25 | layer sub-record type 0x8002 MU = 0 | ignored | everything |
| 26 | user-metadata extent CRC broken | ignore-record (R2), SHOULD report | everything structural |
| 27 | metadata top-level value `[` not `{` | ignore-record (R7) | everything structural |

Five of these deserve a note on *why* they were determined rather than guessed:

- **#2 vs #24.** The asymmetry is real and load-bearing, and it took me two readings.
  `[R-CNF-03]`'s acceptance duty is carved out for any file "carrying no record of a
  type it does not implement with MUST_UNDERSTAND = 1" — unqualified as to scope, so on
  its own it would exempt a reader from accepting *either* file. What forbids rejecting
  the file in the sub-record case is `[R-CNT-18]`'s explicit "a reader MUST NOT reject
  the file for it", conditioned on the file being otherwise conforming. §21.6's closing
  paragraph says the same thing in prose ("The qualifier is load-bearing"). So the
  capability refusal is top-level only, and a reader that rejects a whole conforming
  file over an unknown MU = 1 *sub-record* is nonconforming.
- **#2's binding modal.** Neither the top-level MU = 1 experimental case nor the
  sub-record case is a register row (§21.6: "Neither is a register row"), so
  `[R-CNF-04]` does not supply the MUST. I traced it instead to `[R-CNT-15]`'s "**This
  governs a reader's treatment**, not the file's validity" plus §2.4's reject-file row
  ("A reader MUST NOT rely on any structure in it"). That chain — declarative outcome
  assignment plus §2.4's modal — is how the document binds every unregistered outcome,
  and it is used consistently. I checked it rather than assumed it because §2.1's
  all-capitals rule makes the chain load-bearing.
- **#9 and #12** are the two "conforming files an actor nevertheless refuses / ignores"
  and both are required to be reported as capability, not corruption — #9 by
  `[R-CNT-07]`'s SHOULD-distinct diagnostic, #12 by `[R-MTA-10]`'s naming duty.
- **#14 vs #15** is the clearest demonstration of the chain-of-trust scope ladder in
  §8.2: identical single-bit damage, one byte apart in the file's *structure*, gives
  reject-tile in one case and reject-layer in the other. That is a design property, not
  a defect, and it is exactly what §8.2's ordering states.
- **#23** is checkable "from the entry and the layer record alone, before any payload
  fetch". §19.4 does not place it among its numbered steps; I put it before step 5.
  A reader that instead fetched, verified the crc, and *then* failed on length reaches
  the same outcome (reject-tile) at the cost of one range request. No fork.

Resource-limit walks (not corruption, and required to be reported as limits per
`[R-ERR-04]`): `dir_length` above the reader's bound → decline at whole file, since
§19.1 must CRC the region whole before any other use; `entry_count` or a decoded tile
size above the reader's bound → decline at the narrowest scope whose declarations
exceed what it can serve, a layer or a tile; a zstd tile frame declaring a window above
8 MiB → decline the tile or the layer (§17.2 says so in terms); a user-metadata
document above 16 MiB, or a metadata frame declaring a window above the reader's bound
→ ignore-record for that record (`[R-MTA-09]`), or a whole-file decline under
`[R-ERR-04]`, which the §18.2 Note explicitly offers as the alternative. My reader
implements the first branch in each case.

---

## 6. Worked examples — every constant, offset and checksum I could check

This is where I expected to find something, and did not. Everything reproduces.

### 6.1 Appendix A's 128-byte file, byte for byte

Parsed the hex dump, re-derived every field, recomputed both checksums:

```
magic 8A 4E 52 41 54 0D 0A 1A   version_major 1   version_minor 0   flags 0
generation 1   dir_offset 16    dir_length 4      committed_file_length 128
file_id 0x0123456789ABCDEF      reserved 00000000
trailer CRC computed = 0xE00938D2   stored = 0xE00938D2      MATCH
directory region = 00 00 00 00; covered bytes = <empty>; CRC-32C(<empty>) = 0  MATCH
```

Appendix A's closing narrative also checks out: F − 64 = 64, 64 mod 64 = 0; the
112-byte window [16,128) contains the directory so §6.4's containment test spares the
second request while leaving [0,16) non-resident.

### 6.2 §4.5's check vectors and the three derived CRC constants

Built CRC-32C from §4.5's stated parameters alone (Castagnoli, reflected in/out, init
0xFFFFFFFF, final XOR 0xFFFFFFFF):

```
CRC-32C("123456789")                        = 0xE3069283   ✓ §4.5
CRC-32C(<zero bytes>)                       = 0x00000000   ✓ §4.5
CRC-32C(4 sentinel entries, 80 bytes)       = 0x80A34955   ✓ §7.4 example
CRC-32C(that 4-byte array, LE 55 49 A3 80)  = 0xC4EE982E   ✓ §7.4 example
CRC-32C(2¹⁶ sentinel entries, 1,310,720 B)  = 0xEECB3BB2   ✓ §15.4, Appendix B
```

### 6.3 §7.4's layer-record payload, re-derived independently

I did **not** transcribe the document's hex. I built the payload from §7.4's field
table and §12.3's channel entry, and compared afterwards. Byte-identical, 81 bytes:

```
03 73 73 74 01 01 00 01 00 01 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
00 00 00 00 00 00 00 00 00 00 01 01 00 01 78 64 00 00 00 00 00 00 00 20 00
00 00 00 00 00 00 04 74 65 6D 70 0C 00 04 00 00 C0 7F 01 04 00 00 00 00 00
00 00 2E 98 EE C4
```

and the size accounting the example gives is right: name 4 + nine scalars 34 +
dimension entry 18 + channel entry 12 + trailing fixed 13 = 81, no residue, empty
sub-record sequence. `[R-CNT-17]`'s extent_length = 4×20 + ⌈4/2¹⁶⌉×4 = 84.

### 6.4 Every other numeric example in the document

- §11.2: G = (4,8), N = 32, P = 65,536; with E_y = 1000, G_y = 4 still. ✓
- §11.4: (300,700) → tile (1,2), s = 10, in-tile (44,188), ordinal 11,452; planar
  channel 2 → disk ordinal 74. ✓
- §12.1: bfloat16 1.0 = 0x3F80 (high half of binary32 0x3F800000), stored `80 3F`. ✓
- §12.3: channel entry `04 74 65 6D 70 0C 00 04 00 00 C0 7F`, 12 bytes. ✓
- §14.2: Q = 3 → size 18, ordinal 5 at [15,18); planar `b` 12 bytes, ordinal 5 at
  10–11; float32+bool Q = 5 → size 30, ordinal 5 at [25,30). ✓
- §14.3: `55 01` / `55 FD`. ✓
- §14.5: extents (5,5) tiles (4,4) → grid 2×2; edge tile (1,1) is 32 bytes, value 0 the
  real sample and values 1–15 each `CD AB`. ✓
- §15.4: both examples, digit for digit (above); and the second — planar C = 4, N = 32,
  channel 2 at s = 10 → ordinal 74 → region bytes [1480,1500); channel 3's entries
  96–127. ✓
- §16.2: N = 32, S = 8 → runs [0,8),[8,16),[16,24),[24,32). ✓
- §17.3: three float32s `00 00 80 3F 00 00 00 40 00 00 40 40` shuffle at s = 4, n = 3
  to `00 00 00 00 00 00 80 00 40 3F 40 40`. ✓
- §20.3: 32·20 + 4 = 644. ✓
- §4.6: `température` NFC = 12 bytes `74 65 6D 70 C3 A9 72 61 74 75 72 65`; NFD = 13. ✓
- §5.1: the 128-byte floor is forced — with F = 64, F − 64 = 0 and dir_offset ≥ 16 with
  dir_length ≥ 4 cannot satisfy dir_offset + dir_length ≤ 0. ✓
- §21.9's Note: 2³² entries → 256 KiB array, 2³⁶ → 4 MiB; 65,536 layers × ~200 bytes ≈
  12.5 MiB. ✓
- §6.4: 64 KiB = 65,536. ✓  §17.2: 0x7E000000 = 2,113,929,216. ✓  zstd magic
  0xFD2FB528 → `28 B5 2F FD` little-endian. ✓

### 6.5 The register's own arithmetic

§21.8 asserts "121 conditions over 273 instances", and §21.1 makes the instance count
mechanical ("Instances within a cell are separated by semicolons, and a cell reading —
is one instance"). I extracted all 121 rows and applied that rule literally:

```
F rows 36, instances  58
L rows 49, instances 116
T rows 26, instances  55
R rows 10, instances  44
      121 rows,      273 instances    — exactly as stated
```

and the per-subsection counts (§21.2 "36", §21.3 "49", §21.4 "26", §21.5 "10") all
match. I also spot-checked §21.1's two stated instance axes against the cells that use
them: layout variation (T3, T14, T21, T22, L44 — three layout formulas each) and
magnitude direction (T3, T14, T22, L21, L22, L30 enumerate both directions; T21, L44,
which say *exceeds*, enumerate one). Consistent throughout.

### 6.6 Cross-authority checks

§21.1, `[R-EXT-05]`, §21.9 and Appendix B all designate a defining section as
authoritative over a restatement, so I checked the restatements:

- §10.2's eight-row identifier-space table against §7.3, §14.1, §11.4, §12.2, §17.2,
  §17.3, §7.4/§15.1, §18.2 — all eight agree, including the two spaces with no
  experimental range.
- Appendix C's snapshot against §10.2 — agrees.
- Appendix B's 26 constants against their defining sections — all agree.
- §21.9's hard-limit restatements (nine of them) against `[R-ENC-12]`, §7.4, §18.2,
  `[R-COD-07]`, `[R-ENC-03]`, §16.1, §16.2, §6.2, §5.1 — all agree.
- Appendix H's four checklists against §2.3, §17, §12, §18.2, §21 — agree, including
  the counts ("all four codecs, both filters, both layouts, all thirteen sample types,
  and both user-metadata encodings").

### 6.7 Register completeness against the rules

§21.1 makes completeness normative, so I walked every requirement identifier and asked
whether its detectable violations are registered. I checked all of `[R-ENC-01..16]`,
`[R-CNT-01..27]`, `[R-GEO-01..06]`, `[R-TYP-01..10]`, `[R-SER-01..09]`,
`[R-IDX-01..05]`, `[R-SLB-01..05]`, `[R-COD-01..11]`, `[R-MTA-01..10]`,
`[R-LIF-01..08]`. Every detectable condition I could construct maps to a row; every
undetectable one is accounted for by §21.7 (`[R-ERR-01]`) or by an explicit Note
(§7.4's nesting Note, §16.2's stale-declaration Note, §5.2's "belongs to no class"
Note). §7.4's table constraints in particular map one-to-one onto
L27–L36, L39, L43, L45 plus L1/L2 for the domains — I enumerated all sixteen fields.
I found no unregistered detectable violation.

### 6.8 My own conforming file, opened and read

Two layers, a file-scope user-metadata record, a stored edge tile with real padding,
codec 1, filter 2 (byte-shuffle at stride Q), two sentinel tiles. F = 640.

```
layer img  layout=1 codec=1 filter=2 G=[2,2] N=4 P=4 Q=3 ec=4 extent=[40,124) dsz=12
layer sst  layout=1 codec=1 filter=1 G=[4]   N=4 P=32 Q=4 ec=4 extent=[124,208) dsz=128

tile 0 stored, filtered  00 01 0A 0B 00 64 E8 4C 00 00 03 04
       unfiltered        00 00 00 01 64 00 0A E8 03 0B 4C 04
tile 1, 2 sentinel
tile 3 stored (edge)     16 98 08 07 CD AB 07 CD AB 07 CD AB
                         └ real (4,4) ┘└──── 3 padding positions at fill ────┘

read (0,0) → tile(0,0) u=0  a=00      b=0000     stored
read (0,1) → tile(0,0) u=1  a=01      b=6400     stored
read (1,0) → tile(0,0) u=2  a=0A      b=E803     stored
read (2,2) → tile(1,1) u=0  a=16 (22) b=9808 (2200)  stored   ← the edge tile's one real position
read (0,2) → tile(0,1) sentinel → a=07 b=CDAB   FILL
read (3,0) → request-failed (outside extents; no verdict on the file)
sst  (7,)  → sentinel → temp = 00 00 C0 7F (the recorded quiet NaN, bit-exact)
```

Total I/O to open and read all four tiles of `img` plus one of `sst`:
10 requests, 538 bytes — of which the open is 2 requests / 322 bytes, and each cold
layer costs its CRC array (4 bytes) + one segment (80 bytes) once, then payloads.

---

## 7. The two changed passages, checked as asked

I read these first, then went elsewhere, then came back after the rest of the walk.

### 7.1 §18.2 / `[R-MTA-09]` — the `Window_Size` treatment

> "The frame's declared `Window_Size` is unconstrained here for the same reason, and
> takes the same treatment: a reader's window bound is its own, no smaller than §21.9's
> guarantee for that quantity, and a frame declaring more than the reader admits is
> ignore-record on that ground — the reader's capability, not a failure to decode
> within the meaning of R3, and no violation: the file exceeds a §21.9 guarantee and so
> remains conforming while the reader MAY decline it (`[R-ERR-04]`)."

Four things I checked and one I nearly reported.

- **"§21.9's guarantee for that quantity"** resolves: §21.9's table row is
  "zstd frame `Window_Size` | 8 MiB", generic, not qualified to tiles. §21.9's Note
  ("8 MiB is the decoder window support RFC 8878 itself recommends") is likewise
  generic. So the reader's floor is 8 MiB, determinate.
- **The modal.** "a reader's window bound is its own, no smaller than …" carries no
  keyword. Under §2.1 that clause has no force of its own — so I looked for the MUST
  and found it in `[R-ERR-03]`: "a conforming reader MUST accept any conforming file
  whose quantities lie within these bounds", reinforced by `[R-ERR-04]`'s "Software
  that declines **on that ground** a file whose every quantity lies within the table is
  not a conforming reader". Bound.
- **The R4/R3 boundary.** R4's twelve instances are exactly the six frame constraints
  §18.2 enumerates (magic, skippable frame, second frame, dictionary ID, content-
  checksum flag, trailing bytes) across two containers. `Window_Size` is deliberately
  not among them, matching §18.2's "unconstrained here". And the new clause explicitly
  removes a window decline from R3. Consistent.
- **The thing I nearly reported, and why I did not.** `[R-ERR-04]` licenses declining
  "at the whole file, or at the narrowest scope whose declarations exceed what it can
  serve, **a layer or a tile**" — record scope is not in that list, yet `[R-MTA-09]`
  assigns ignore-record. And §18.2's own Note argues that a document decline under
  `[R-ERR-04]` "does so at the whole file, a document having no declared size and so no
  narrower scope whose declarations that rule can measure" — reasoning that does not
  transfer to the window, which *is* declared. I built the divergence: two conforming
  readers at the 8 MiB floor meet a conforming file whose metadata frame declares a
  32 MiB window; reader A ignore-records the record and serves the layers, reader B
  declines the whole file. But both are licensed by the text as written — `[R-MTA-09]`
  grants the first and its own closing clause ("while the reader MAY decline it
  (`[R-ERR-04]`)") grants the second, exactly as the size-bound Note grants both there.
  A licensed MAY is not a fork. Not a finding.

### 7.2 §21.5's preamble clause

> "…and except where a reader or verifier declines the decode on the size bound or on
> the frame's declared window, which `[R-MTA-09]` makes that actor's capability and not
> a fact about the file."

This clause is doing real work, and I can name the defect it closes. R3's row text is
"A user-metadata document's stored bytes fail to decode under its declared assigned
encoding", and its Governing rule cell is `[R-CNT-25]` — which lists "a decode failure"
among the ways a document is unreadable and makes every one of them a *violation*.
Neither R3's cell nor `[R-CNT-25]` carries the decline exclusion; only `[R-MTA-09]`
(which R3 does not cite) and this preamble clause do. Without the clause, a verifier
built from R3 plus its cited rule — following §21.1's own "the rule governs"
instruction — would report *nonconforming* for a conforming file whose 20 MiB document
it declined at its 16 MiB bound, where `[R-MTA-09]` says "a verifier MUST NOT report it
as one". That is a verdict fork, and the clause forecloses it. I checked the closure
holds from the register side (§21.5 preamble), the rule side (`[R-MTA-09]`), and the
class side (§2.3's cannot-establish list, which names "when it declines to decode a
user-metadata document (`[R-MTA-09]`)" generically). All three agree.

I also traced the boundary the two edits jointly draw — file defect versus actor limit
— across all nine cases the document distinguishes, and found them mutually consistent:

| case | reader | verifier | file |
|---|---|---|---|
| format major not implemented | reject-file (capability) | cannot establish | conforming or not — undecidable by this text |
| top-level experimental MU = 1 type | reject-file (capability) | cannot establish | conforming |
| layer sub-record experimental MU = 1 | reject-layer; MUST NOT reject file | cannot establish | conforming |
| codec/filter unexecutable | n/a — all core (`[R-CNF-03]`) | cannot establish | conforming |
| decode declined on resource grounds | decline, reported as limit | cannot establish | conforming |
| metadata document above the size bound | ignore-record, or whole-file decline | cannot establish | conforming |
| metadata frame window above the bound | ignore-record, or whole-file decline | cannot establish | conforming |
| metadata encoding experimental | ignore-record | **certifies**, reporting the record | conforming |
| metadata encoding 0 or reserved | ignore-record | nonconforming (R1) | **violation** |

The one that could have gone wrong — the split between the last two rows — is stated
three times and consistently: §21.5's preamble ("what `[R-MTA-10]` withdraws is the
document's content rules, never the encoding byte's own value set"), `[R-MTA-10]`
itself, and §21.6's row. My reader implements the split and my degradation cases 12 and
13 exercise both sides.

---

## 8. Places I had to reason rather than read, listed honestly

Every one of these resolved. I list them because "resolved after two readings" is
information a maintainer can use even when it is not a defect.

1. **Is an ignored record's extent slot validated?** Yes — §2.2 above; four
   independent statements.
2. **Does a *point* request one position outside the extents differ from a
   *single-position region* request there?** Yes, deliberately: §19.4 defines "a range
   whose every interval holds a single position is a region request", and the point
   fails as a request while the region succeeds returning nothing. Explicitly
   disambiguated; I would have guessed otherwise.
3. **Which of §19.3's checks come first?** Unordered. I confirmed order cannot change
   the outcome: every §19.3 condition is reject-layer, and the one file-scope condition
   in the neighbourhood (duplicate layer name) is decided at the open, before any layer
   access. Only the register row a *vector* attributes to could differ, and §24 handles
   that ("the entry records every row the file exercises and says which it was built
   for").
4. **Whether the whole CRC array or one u32 must be fetched.** Whole — crc_of_crc_array
   covers the array, and §21.9's Note says "fetches whole" in terms.
5. **What the "decoded payload" of `[R-SER-07]` is — post-codec or post-filter.** Moot:
   `[R-COD-10]` fixes length invariance. §17.1 nonetheless says post-filter ("the
   result is the decoded tile image, subject to `[R-SER-07]`'s exact-size rule").
6. **What a reader returns for a bool sample.** false/true, per §14.2's byte encoding,
   §14.3's bit encoding, and `[R-SER-08]`'s "MUST report 0x00 as false and every other
   byte as true". §14.4's Note confirms the two layouts denote the same reference array
   despite different tile images.
7. **Whether P·Q is checked in a layer that addresses no tile.** Yes — §4.1 above; the
   normative route is `[R-SER-02]`/`[R-SER-07]` + `[R-ENC-04]`, not the non-normative
   Note that says the same thing.
8. **Whether `file_id` is domain-capped.** No — §2.1 above.
9. **Which modal binds `[R-CNT-15]`'s reject-file for an experimental MU = 1 type,**
   given §21.6 says it is not a register row. "This governs a reader's treatment" plus
   §2.4's reject-file row.
10. **Whether `[R-CNF-03]`'s acceptance carve-out lets a reader reject a conforming file
    over an unknown MU = 1 *sub-record*.** No — `[R-CNT-18]`'s MUST NOT.
11. **Whether a metadata frame's Frame_Content_Size may size a reader's buffer.**
    §18.2 removes §17.2's decoded-size constraints, but `[R-SEC-02]` independently bars
    sizing "in proportion to a declared magnitude it has not corroborated against the
    file's actual length"; a bound of min(FCS, own bound) is safe either way, and RFC
    8878 makes a present FCS honest so no divergence in outcome arises.
12. **Whether `[R-MTA-04]`'s "MAY use a wider representation" lets a reader accept
    `1e400`.** No: the readability test is stated over "the binary64 interpretation",
    and R8 is reader-detected, so `[R-CNF-04]` binds. The MAY governs the reader's
    internal representation, not the test. This is the exact shape §2.1's
    capitals rule makes dangerous, and it resolves cleanly.

---

## 9. Findings

**None.**

I want to be explicit that this is a result and not a shrug. I built the reader end to
end, decoded real samples through the full codec/filter/extract path, exercised
twenty-seven degradations including seven that required authoring index entries with
recomputed checksums, reproduced every constant, offset, checksum and worked example in
the document, re-derived the register's 121 rows and 273 instances mechanically, and
walked every requirement identifier for register completeness. I found nothing that two
competent implementations reading this text could disagree about on bytes or verdicts,
and nothing decidable-but-expensive that I would ask a maintainer to spend a revision
on.

The three candidates I took furthest before rejecting them, so the next round does not
have to redo the work:

- **`[R-ERR-04]`'s scope list versus `[R-MTA-09]`'s ignore-record** (§7.1 above).
  Rejected: both outcomes are licensed by the text as written, so the divergence is a
  MAY, not an ambiguity.
- **"the bound above" in `[R-MTA-09]`'s verifier sentence**, whose antecedent became
  double when the window paragraph was inserted between it and the size-bound sentence.
  Rejected: both permitted readings converge on the same verdict (*cannot establish*,
  MUST NOT certify, MUST NOT report nonconforming), because §2.3 lists the ground
  generically and §21.5's preamble names both bounds. Editorial at most.
- **§18.2 has no writer guidance paralleling §17.2's "Writers SHOULD keep the declared
  window within §21.9's 8 MiB `Window_Size` guarantee"**, so a writer may emit a
  conforming file whose metadata document no reader at the guarantee floor will read.
  Rejected: §18.2 says the window is "unconstrained here" deliberately, and the §21.9
  guarantee mechanism already assigns the consequence. An absence of advice is not a
  defect in a document that has decided the question.

Confidence that an implementation built from this text alone would interoperate:
**high** for the reader's contract — the open, the tiers, the index chain, the decode
pipeline, the byte layout, fill, and every degradation I could construct. The one
residual risk I would name is not an ambiguity but a reading hazard: the decode path
(§11.4, §14, §17.1, §17.3) contains no reader modal at all and is bound entirely by
`[R-MDL-02]`'s bit-exactness requirement several sections away. An implementer who
never makes that connection has no local text telling them they must invert the filter.
Nothing is underdetermined; it is simply the one obligation the document states farthest
from where it is needed.
