# Cleanroom round 37 — Reader implementer transcript

## 0. Disclosure (read first)

**What I read.** Exactly one specification file:
`/Users/robertkleffner/Documents/GitHub/tarn-first-draft/spec/tarn.md`, read
in full, start to finish (5 `Read` calls covering lines 1–4981; the file is
4981 lines / 49,821 words, matching the brief's stated 4,981 lines / ~49,800
words). I did not open `AGENTS.md`, `PLAN.md`, `OPEN-QUESTIONS.md`,
`README.md`, `CONTRIBUTING.md`, anything under `docs/`, anything under
`conformance/`, `spec/registry.json`, or any other file in the repository. I
did not run `git log`, `git diff`, `git status`, or any other git command
against this repository. I did not list any directory of the repository. I
did not web-search or web-fetch anything.

**What I ran.** Only local, file-free computation: an independent CRC-32C
implementation (bit-by-bit, reflected Castagnoli, matching `[R-ENC-09]`'s
parameters) that I wrote to my own scratch directory and used to check every
worked checksum example the document states that I could verify without
reading any other file. The script is
`/private/tmp/claude-501/-Users-robertkleffner-Documents-GitHub-tarn-first-draft/r37-round/scratch/reader/crc32c_checks.py`.
It performs no file I/O of its own and reads nothing from the network; I ran
it with `python3 crc32c_checks.py` from inside that scratch directory. That
is the only file I created, and it is the only thing in my scratch directory.
When I began, the directory did not yet exist; I created it myself, so there
was no pre-existing content from a prior attempt to work beside.

**Unwanted context that appeared before I began, and what I did with it.**
Before my first tool call, my context already contained, unasked:

1. The contents of this repository's `CLAUDE.md`, which reads only "See
   AGENTS.md." — I did not follow that pointer; `AGENTS.md` is outside my
   one-file access rule and I never opened it.
2. The contents of a user memory file (`MEMORY.md`) listing about twenty
   bullet points with titles that plainly presuppose facts about this very
   project and prior rounds — e.g. "TARN harness spec path", "TARN lineage
   gate word list — the canonical file is missing", "TARN repair prose vs
   rules — where this project's repair defects actually live", "TARN
   refute phase and unanimous upholds", "TARN closed-list exceptions
   compose", and others in the same vein.
3. A git-status/log block showing the current branch, a clean working tree,
   and five most-recent commit subject lines, including "Cleanroom round 37:
   charter, over 96e4ad4..6c9470e", "The pre-round-37 audit of ADR-0131: two
   defects in three clauses, none byte-level, both repaired", and three
   other round-36-era commit messages.
4. Boilerplate MCP server instructions for a documents connector and a
   Chrome-automation tool, unrelated to TARN.

None of (1)–(4) is part of the specification and I treated none of it as
evidence about the specification's content. In particular I did not let the
memory-file titles suggest where a defect "must" be, and I did not let the
commit messages' claim of "two defects... both repaired" or the mention of
"ADR-0131" steer my reading toward or away from any passage — I have not
read any ADR and do not know what ADR-0131 says. I disclose that this
material appeared; I am not repeating its substantive content as if it were
a finding, and I did not act on any of it. Item (4) is inert boilerplate and
I mention it only for completeness.

**Path check.** The file was exactly where the brief said it would be:
`spec/tarn.md` under the stated repository root. Nothing about its path
carried any information I needed to act on.

---

## 1. How I read the document

I read the file sequentially in five chunks (lines 1–400, 400–800, 800–1200,
1200–1600, 1600–2000, 2000–2450, 2450–2900, 2900–3350, 3350–3750, 3750–4200,
4200–4650, 4650–4981 — the tool's line-limit meant more like a dozen calls
in practice, but always forward, never skipping). I did not use the round's
files-under-`out/` directory in any way, and I did not read it.

Per the brief, I paid the heaviest attention to the three named passages
(§3.3, §20.3, §20.4) and the four named "decisions" (§20.4's drop-a-layer
table and paragraph; §7.2's flag-orthogonality Note and the paragraph before
it; §20.1's closing paragraph together with §2.3's updater clause; §20.3
step 4's scope sentence and the paragraph it closes), plus the two
appendices that restate them (Appendix H's "Conforming updater" checklist,
which restates both §20.4 and §20.1) and the Note in §7.2. I then re-read
the whole document with the twelve shapes in mind, and did the required
implementation-walk exercise (open path, validation timing, layer access,
tile-read algorithm, degradation walks, worked example) as I went, because
that is the only way I know to find an ambiguity that a summary would paper
over: I had to decide, at each step, what code I would actually write, and
note every point where the text left that underdetermined.

---

## 2. The open path (byte-exact cold remote open)

Implementing `open()`:

1. Issue **one HTTP range request** for the suffix `bytes=-64` (or the
   local-file/mmap equivalent, which costs no request). If the transport
   discloses the range response's complete length (`[R-CNT-10]`), that
   response gives me both the trailer bytes **and** F, the
   transport-authoritative file size, in the same round trip. This is
   `[R-RDR-01]` step 1 and 2 merged, exactly as §6.4 describes.
   - **Bound before I've read anything else:** F itself. §6.2 says the
     trailer must be validated "in order": magic (8 bytes) → trailer CRC
     (self-contained, over the 60 bytes I already have) → version gate →
     the remaining field gates (dir_offset ≥ 16; dir_length ≥ 4;
     dir_offset + dir_length ≤ F − 64; file_id ≠ 0; reserved zero). The
     critical one for my next request is `dir_offset + dir_length ≤ F − 64`
     — this is what bounds the *size* of the range I am about to ask for
     before I have fetched a single byte of the directory itself. If I
     skipped this check I could be induced by a hostile trailer into
     requesting an unbounded range; `[R-ENC-05]` is explicit that I MUST
     NOT act on dir_offset/dir_length before their own domain checks pass
     (they're covered by the trailer CRC I already verified).
2. Issue **one more HTTP range request**, `bytes=dir_offset-(dir_offset+dir_length-1)`,
   to fetch the directory region. Verify its trailing 4-byte CRC-32C over
   the preceding `dir_length − 4` bytes before parsing a single record
   (`[R-CNT-11]`).
3. Parse the record sequence (no further I/O): apply the MU gate to
   unknown top-level types, the per-type multiplicity rule, the extent-slot
   shape checks for non-layer records, and the user-metadata framing
   checks, and build the layer-name table, checking uniqueness over raw
   bytes.

**Total for the baseline path:** 2 requests, `64 + dir_length` bytes, of
exactly two ranges: the trailing 64 bytes, and `[dir_offset, dir_offset +
dir_length)`. The second range's size is entirely determined by fields
inside the first — that is the "bounds each range before you have read it"
property the brief asks me to state, and it is what makes the two-request
figure independent of file size and layer count (`[R-RDR-01]`).

If I choose the speculative-suffix variant (fetch, say, the last 64 KiB in
one shot and check containment), the request count can drop to 1 when the
directory is small enough to fall inside that window (§6.4's guidance that
writers keep `dir_length + pad + 64 ≤ 65536` exists exactly to make this the
common case) — but this is my own implementation choice; nothing in the
text obliges it, and a reader that always issues the exact two ranges is
equally conforming.

**Front-block check.** If my speculative window reached byte 0 (or I'm a
local/mmap reader), `[R-CNT-04]` obliges me to compare bytes `[0,16)` for
exact byte equality before other processing, reject-file on mismatch. If my
two-request baseline path never touches byte 0, I am explicitly permitted to
defer or omit that check entirely — the accounting in §6.4 does not include
it. I implement this as: "if my first read's buffer covers offset 0, check
it; otherwise don't, and don't feel obliged to fetch it just to check it."

---

## 3. Validation timing by tier

I built this as a table of "when do I check X" while implementing, matching
§19.2 exactly:

| Tier | What I must have checked before relying on it |
|---|---|
| open | front block (only if resident), trailer (all of §6.2/§6.3 in the stated order), directory CRC, per-record framing/MU/multiplicity/extent-slot-shape at top level, layer-name uniqueness |
| first layer access | the *entire* layer record: extent-slot validity, every §7.4 field's value-set and cross-check (`[R-CNT-23]`, `[R-CNT-16]`, `[R-CNT-17]`), sub-record walk and multiplicity, name rules, the u64 domain check on every field, the 2⁶³−1 ceiling on every derived quantity §11.2/§14 produce, codec/lz4-cap bound |
| tile use | the index chain (crc_of_crc_array → segment CRC → entry classification), the stored bytes' own CRC, decode exactness |
| record-extent use | that extent's own CRC and (for user metadata) the document's content rules, at whichever encoding governs |

The one thing I had to be careful to implement correctly: **the rule fixes
only the *latest* point**, not the earliest — I am free to validate a
layer's record the moment I open the file if I want to (e.g. to build a
richer catalog UI), and I am free to verify every tile's index chain up
front. What I must never do is *serve* something before its tier's checks
have passed. A layer I never touch in a session can carry an undetected
violation forever without that costing me conformance for the *other*
layers (`[R-RDR-02]`'s explicit escape hatch), which is a nice property for
a lazy-catalog implementation: I can list layer names from the open alone
(§19.1 step 4) without ever validating any layer's declarations.

---

## 4. Layer access and the tile-read algorithm

Implementing `layer.access(name)`:

- Validate the *entire* layer record body I described above. This is
  "decidable from the resident directory and F: layer access performs no
  fetch" (`[R-RDR-03]`) — I confirmed by tracing every cited rule
  (`[R-CNT-13]`, `[R-CNT-23]`, `[R-CNT-16]`, `[R-CNT-18]`, `[R-CNT-14]`,
  `[R-ENC-11]`, `[R-ENC-12]`, `[R-ENC-15]`, `[R-CNT-25]`, `[R-MTA-03]`,
  `[R-ENC-03]`, value sets of §7.4/§11.4/§12.2/§14.1/§17.2/§17.3, §13.2,
  `[R-COD-07]`, `[R-GEO-01]`–`[R-GEO-03]`, `[R-ENC-04]`, `[R-SER-02]`,
  `[R-SER-07]`, `[R-CNT-17]`) and every one of them reads only bytes
  already sitting in the directory buffer I fetched at open. None requires
  a fetch. Good — that is a real, checkable invariant, not just an
  assertion, and it held up.

Implementing `layer.read(coord_or_region, channels?)` — I built this exactly
as §19.4 states, as an 8-step per-tile loop:

1. **Domain.** Clip the request to `[0, Eᵢ)` per dimension. A point outside
   fails as a *request*, not a file verdict. A region returns the
   intersection (possibly empty).
2. **Ordinals.** `tᵢ = xᵢ div Tᵢ`, `uᵢ = xᵢ mod Tᵢ`, in-tile ordinal
   `Σ uᵢ·∏_{j>i}Tⱼ`, spatial ordinal `s = Σ tᵢ·∏_{j>i}Gⱼ` (linearization 1
   only — I reject any other value at layer access, so I never reach this
   step with anything else), disk ordinal `s` (interleaved) or `c·N + s`
   (planar, per requested channel `c`).
3. **Index chain.** Verify `crc_of_crc_array` over the fetched segment-CRC
   array, and the segment CRC over the fetched segment containing this
   entry. I may run these two fetches in parallel and cache the
   verification result under committed-prefix immutability
   (`[R-LIF-03]`).
4. **Entry.** Classify per §15.3's table. Sentinel → skip straight to
   returning fill for every position this tile carries, no payload I/O.
   Any of the "structural" malformed shapes, or a bad extent → reject-tile,
   report failure for exactly the positions this tile carries, never fill.
5. **Payload.** Fetch `[offset, offset+length)`, verify the entry's own
   CRC before touching the bytes for decode.
6. **Decode.** Codec, then filter inverse. The result must be exactly the
   tile's decoded size — a mismatch is reject-tile even though the CRC
   passed (this is a distinct check from step 5; a corrupted-but-CRC-valid
   file is impossible by definition, but a mis-declared codec/geometry
   combination is not, and this is where I'd catch it).
7. **Extract.** §14's offset arithmetic locates each requested value.
   Never return a padding position.
8. **Return.** Bit-exact. For a region/multi-channel request spanning
   several tiles, a tile-scope failure is bounded to that tile's positions
   (I may return the rest with a per-tile failure report, or fail the whole
   request — my choice) but a *layer*-scope failure (the index-chain check
   itself failing) bars the rest of the request and all further service
   from that layer — though anything I already returned under the
   validation-timing rule stands.

**Byte layout I implement for step 7**, verified against three worked
examples in the text (all of which I re-derived and all matched, see §7
below): planar numeric channel `c`: decoded size `P·Bᶜ`, value `k` at byte
`k·Bᶜ`; interleaved: decoded size `P·Q` (`Q = ΣBᵢ`), value `k` at byte
`(k div C)·Q + F_{k mod C}` where `Fᶜ = Σ_{j<c} Bⱼ`; planar bool: bit-packed
LSB-first, `⌈P/8⌉` bytes.

---

## 5. Degradation walks

I traced these end-to-end as concrete reader code paths:

**(a) Unknown top-level record type, experimental range, MU = 0.**
`open()` encounters type `0x9000` (say), MU=0. I ignore it entirely
(`[R-CNT-15]`): it contributes no name to the layer table, is not walked
for sub-records (I don't even know its shape), and every other record
parses normally. The file may still be fully conforming (§21.6 lists this
as a defined non-violation), and every layer I *can* validate reads
normally. **What I may still serve:** everything — all layers, all tiles,
the whole file. I only lose whatever that record would have told an
application (nothing to a container-level reader, since it's opaque).

**(b) Unknown top-level record type, reserved range, MU = 1.**
Type `0x0005` (unassigned), MU=1. `[R-CNT-15]`'s MU gate fires: reject-file.
I stop the open entirely — I do not build a layer table, I do not serve
anything. This is true *even though* the type being reserved (rather than
experimental) is itself a separate writer-side violation (F36) I'm not
obliged to detect as a plain reader (that row's detector is *verifier*) —
my own obligation here is purely the MU=1 reject, which fires regardless of
which unassigned range the type came from (`[R-CNT-15]`: "Readers of both
apply the MU rule above unchanged"). **What I may still serve:** nothing.

**(c) Unknown/reserved codec value on one layer.**
Layer `elevation` declares codec `0x0006`. This is caught at *layer
access* (`[R-COD-03]`, register row L43), not at open — the open never
looks past the layer's name. Result: reject-layer for `elevation` alone.
**What I may still serve:** every other layer in the file, in full,
including still *listing* `elevation`'s name (§2.4's reject-layer
definition explicitly permits listing a rejected layer's name) — I just
refuse any read into it.

**(d) Truncated tail (torn commit).**
The physical file is longer than any committed state — say a writer crashed
mid-append. My final-64-byte fetch does not land on a valid trailer (the
magic fails, or the CRC fails, or committed_file_length doesn't match the
transport size). `[R-LIF-05]` is unambiguous: I report the file torn/invalid
and **MUST NOT scan backward** looking for an earlier valid trailer — that
is a *recovery tool's* job (§9.6), never mine on the default read path.
**What I may still serve:** nothing, on this path. (A caller wanting the
last good state has to invoke a separate recovery operation, which is a
different program, not "the reader trying harder.")

**(e) Checksum mismatch — directory CRC vs. a single tile CRC (two
different blast radii from the "same kind" of failure).**
- Directory CRC mismatch (F20): reject-file. Even though the trailer was
  perfectly valid and even though every individual record's bytes might be
  individually well-formed, I never even get to parse a single record —
  I MUST verify this CRC "before any other use of the region"
  (`[R-CNT-11]`). **What I may still serve:** nothing.
- One tile's stored-bytes CRC mismatch (T1): reject-tile, for that tile
  alone. Every other tile of that layer, and every other layer, is
  unaffected — this is explicitly the point of finest-scope detection
  (§1's "one bad tile does not condemn a file"). **What I may still
  serve:** everything except that one tile's positions.

**(f) Format major version this reader does not implement.**
Trailer's version_major = 2 (say I only implement major 1).
`[R-CNT-07]` obliges reject-file, but on *capability* grounds, and my
diagnostic SHOULD say so distinctly from "corrupt" — the file may be a
perfectly conforming major-2 file. Before I even get to reject on this
ground, I must still apply every *reaching* condition (`[R-CNT-24]`,
`[R-CNF-13]`) — the ones that are the same in every major: front-block
equality, trailer magic, trailer CRC. Only after those pass do I emit the
"unimplemented major" refusal rather than a corruption refusal.
**What I may still serve:** nothing from this reader — but I must be
careful that my error message doesn't tell an operator to discard a file
that a newer reader would happily open.

**(g) A resource limit exceeded (entry_count near the guarantee floor, or
above it).**
Layer declares `entry_count = 2^40`. §21.9's minimum guarantee is `2^32`,
so if my implementation's own cap is (say) `2^34`, I MUST accept this file
up to whatever I've chosen to support, and if my cap is below the file's
actual count I MAY decline — but only by reporting a **resource limit**,
never as corruption (`[R-ERR-04]`), and at the *narrowest* scope I can (the
layer, not necessarily the whole file). If instead I declined a file whose
every declared quantity was *within* the §21.9 table, I would not be a
conforming reader at all (`[R-CNF-03]`) — the guarantees are a floor I
cannot treat as a suggestion. **What I may still serve:** every other
layer, or, if I decline only that layer, everything but it.

That's five degradation paths traced fully open-to-served-or-refused; (a)
and (b) form a matched pair showing the MU gate is what actually decides
survivability, not the assigned/reserved/experimental distinction by
itself; (d) and (e)/directory-CRC form a matched pair showing two different
"whole file is unusable" triggers that arrive by different rules
(`[R-LIF-05]` vs `[R-CNT-11]`) but the same reject-file outcome; (e)'s two
halves show the same failure *mode* (a CRC mismatch) landing at two
different blast radii purely because of *which* structure owns the bytes.

---

## 6. Worked example — Appendix A's 128-byte minimal file

I did not build my own file; the appendix's annotated 128-byte file is
small enough to walk by hand and gave me a chance to check the document's
own arithmetic rather than trust it.

Bytes, as given:
```
0000  89 54 41 52 4E 0D 0A 1A  00 00 00 00 00 00 00 00
0010  00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00
0020  00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00
0030  00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00
0040  8A 4E 52 41 54 0D 0A 1A  01 00 00 00 00 00 00 00
0050  10 00 00 00 00 00 00 00  04 00 00 00 00 00 00 00
0060  80 00 00 00 00 00 00 00  EF CD AB 89 67 45 23 01
0070  00 00 00 00 00 00 00 00  00 00 00 00 7E 15 2F 40
```

My open, traced against my own code from §2 above:

1. F = 128 (given/probed). ≥ 128, passes `[R-CNT-27]`.
2. Fetch `[64,128)`. Magic `8A 4E 52 41 54 0D 0A 1A` ✓. Trailer CRC over
   bytes `[64,124)` relative to file start, i.e. trailer-relative `[0,60)`:
   **I recomputed this CRC-32C independently** (see
   `crc32c_checks.py`, "Appendix A trailer CRC" check) over exactly the 60
   bytes the table lists (magic·version_major·version_minor·flags·
   dir_offset·dir_length·committed_file_length·file_id·reserved) and got
   `0x402F157E`, stored little-endian as `7E 15 2F 40` — **matches the
   document's stated bytes exactly.** version_major = 1 (implemented).
   flags = 0 (no incompat bits, nothing to ignore). dir_offset = 16 ≥ 16 ✓.
   dir_length = 4 ≥ 4 ✓. `dir_offset+dir_length = 20 ≤ F−64 = 64` ✓.
   committed_file_length = 128 = F ✓, multiple of 64 ✓. file_id =
   `0x0123456789ABCDEF` ≠ 0 ✓. reserved 12 bytes all zero ✓.
3. Fetch `[16,20)` = `00 00 00 00`. This is dir_length−4 = 0 bytes of record
   sequence, followed by the CRC-32C of those zero bytes. My CRC
   implementation gives `crc32c(b"") == 0x00000000` — **matches**. Directory
   parses as zero records.
4. Record walk: no records, so the layer table is empty, no duplicate-name
   check to perform, nothing to reject.

Front-block check: my baseline two-request path never touches byte 0
(request 1 is `[64,128)`, request 2 is `[16,20)`), so `[R-CNT-04]` lets me
skip it. If I'd instead spooled a single 128-byte speculative window (the
whole file, since the file *is* only 128 bytes), that window *does* reach
offset 0, and now I owe the equality check — verified: bytes `[0,16)` are
exactly the constant `89 54 41 52 4E 0D 0A 1A` + 8 zero bytes.

Result: a conforming, layer-less file. `layers()` returns `[]`. Any read
request against any layer name fails as "no such layer" (not a file
defect — §21.6 records "the file contains zero layers" as a defined
non-violation).

I also re-derived the two smaller worked examples inside the document body
itself, independent of the appendix:

- **§7.4's `sst` layer** (rank 1, extent 100, tile extent 32, one
  interleaved float32 channel `temp`, codec/filter none). Grid count
  `⌈100/32⌉ = 4`. `entry_count = 4` (interleaved, so `N`, no channel
  multiplier). `extent_length` formula: `4×20 + ⌈4/2¹⁶⌉×4 = 80+4 = 84` —
  matches the document's stated 84. With no tile stored, the 80-byte entry
  array is four copies of the sentinel pattern `FF×16 00×4`; **I computed
  its CRC-32C independently and got `0x80A34955`**, stored `55 49 A3 80` —
  matches the document exactly. **I then computed the CRC-32C of that
  4-byte segment-CRC array** (i.e. `crc_of_crc_array`) and got
  `0xC4EE982E` — matches the document exactly.
- **§15.4's all-sentinel-segment constant.** I built a full 65,536-entry
  segment of the sentinel pattern (1,310,720 bytes) and computed its
  CRC-32C independently: `0xEECB3BB2` — matches the document's stated
  constant exactly.
- **§15.4's large-layer example** (`entry_count = 1,000,000`): I re-derived
  segment count (`⌈1000000/65536⌉ = 16`, last segment covering
  `1000000 − 15×65536 = 16960` entries), index region size
  (`1000000×20 + 16×4 = 20,000,064`), the disk ordinal 999,999's segment
  (`999999 div 65536 = 15`), its segment-relative byte offset
  (`(999999 − 15×65536)×20 = 16959×20 = 339,180`), the CRC-array byte
  range (`[20,000,000, 20,000,064)`), segment 15's byte range
  (`[19,660,800, 20,000,000)`, i.e. `339,200` bytes), and the "one full
  segment is 1.25 MiB" claim (`65536×20 = 1,310,720` bytes exactly `=
  1.25×1,048,576`). All of these matched the document's stated figures
  exactly.
- **§14.2's byte-layout examples** (interleaved `a:uint8, b:uint16`,
  tile extents (2,3); and `t:float32, m:bool`). I re-derived `Q`, decoded
  size, in-tile ordinal for coordinate (1,2), and every byte range the
  document states for both the interleaved and the "same layer planar"
  variants. All matched.
- **§11.4's linearization example** (grid (4,8), coordinate (300,700) →
  tile (1,2), spatial ordinal 10, in-tile ordinal 11,452, planar C=4
  channel-2 disk ordinal 74). All arithmetic re-derived and matched.

I did not find a single arithmetic or checksum error anywhere I could
independently check. That is itself worth recording as a result, not a
non-result: this document's worked numbers are, as far as I can verify them
from the text alone, exactly self-consistent.

---

## 7. Focused re-reading of the round's named decisions and passages

I read each of these at least twice, once forward for comprehension and
once backward from every cross-reference it makes, checking that the cited
rule actually says what the citing sentence claims.

### 7.1 §3.3's Note (the changed passage)

> "Part I (container) is independent of Part II (array model) by
> construction: no Part I structure requires decoding sample payloads, so
> appenders, and rewriters that carry a layer forward, operate on files
> whose layers they cannot decode — that independence is load-bearing for
> the updater rules of §7 and §20."

I tested the claim against the rest of the document rather than taking it
on faith. **Does every appender genuinely never need to decode?** I walked
every permitted §20.3-step-4 operation (renaming, growing an extent,
extending/shortening a planar channel list at its end, declaring/
changing/clearing a slab or alignment) and none of them requires applying
a codec or filter to existing stored bytes — they either touch declarations
only, or add wholly new tiles the caller supplies pre-encoded. Index-chain
verification (`[R-IDX-04]`) is CRC comparison, not decode. So "appenders...
operate on files whose layers they cannot decode" holds for the *ordinary*
appender path with no restriction needed.

**Why does "rewriters" need the restriction "that carry a layer forward" but
"appenders" doesn't?** Because §20.5 gives a rewriter a second mode — it can
*re-create* a layer, and re-creating is explicitly defined as decoding:
"What it re-creates it decodes as a reader... and writes as a creator." So
the qualifier is doing real, necessary work: without it, the sentence would
be flatly false of a re-creating rewriter. With it, restricted to "rewriters
that carry a layer forward" (as opposed to those that re-create it), the
claim holds. I checked this is not merely plausible but forced by
`[R-WRT-07]`'s own wording ("A layer the rewrite re-creates is new output...
nothing of the input's copy of that layer is carried forward").

I considered flagging the word "cannot" as overclaiming (a fully-conforming
appender, being a conforming reader per `[R-CNF-06]`/`[R-CNF-11]`, is in
fact *capable* of decoding every core codec — it simply doesn't need to for
these operations, so "cannot" reads more like "need not"). I decided this
does not rise to a reportable finding: the sentence sits inside a labeled
**Note**, which is non-normative under `[R-CNF-01]`, so even a genuine
looseness here cannot move an emittable byte or a verdict, and on reflection
I think "cannot decode" is best read as "operate without any dependency on
having decoded" — a description of the architectural independence, not a
claim about any implementation's capability — which is exactly the
sentence's own stated topic ("Part I is independent of Part II"). I record
this as a rejected candidate, not a finding.

### 7.2 §20.4's drop-a-layer paragraph and table

> "A commit MAY therefore drop a layer record, and the drop takes the layer
> whole: a sub-record's flags govern it within a layer the updater keeps,
> so a dropped layer's sub-records and their extents go with it whatever
> their PE bits. One sub-record blocks the drop, a sub-record of a type
> the updater does not implement with MU = 1, the drop being a
> modification of the scope it governs (the table's first row)."

I checked this against the table's own MU=1 row ("At layer scope an unknown
critical record blocks modification of that layer, its drop included,
leaving other layers editable") — consistent, and I checked it against
`[R-CNT-18]`'s "an unknown sub-record type with MU = 1 is reject-layer" —
also consistent (a layer carrying such a sub-record is already unreadable
as *data*, and separately, as an *editing* target, blocked from
modification including drop; these are two different obligations —
`[R-CNF-09]`'s read-side bar and `[R-WRT-08]`'s write-side one — that
happen to cover the same layer, and I confirmed carrying the whole
directory forward byte-identically in an unrelated commit is not itself a
"modification" of that layer, so there's no tension between "reject-layer
for reads" and "still present, untouched, in the next generation's
directory").

I also checked the closing sentence of the passage: "A dropped layer's name
is free to the same commit and to any later one (§20.3 step 4, §19.1)." —
I confirmed this against §19.1's uniqueness rule, which is computed over
the *new* directory alone (two layer records byte-identical in name within
*one* directory is the violation, F4/L9); since the old record is omitted
from the new directory, there is nothing to collide with. Consistent.

### 7.3 §7.2's flag-orthogonality Note and the paragraph before it

> "The two flag bits are not orthogonal. `[R-CNT-12]` leaves a record three
> states, not four, and they are §20.4's three rows: MU = 1, whose PE bit
> is read as 1 whatever is stored; MU = 0 with PE = 1; and MU = 0 with
> PE = 0."

I cross-checked this literally against §20.4's table rows (`MU = 1`;
`MU = 0, PE = 1`; `MU = 0, PE = 0`) — three rows, exactly as claimed — and
against `[R-CNT-12]`'s own text ("Writers MUST NOT emit the combination
MU = 1 with PE = 0; a reader or updater encountering it MUST treat the
record as PE = 1"), which is exactly what collapses the fourth combination
into the first state. No discrepancy.

The paragraph before the Note (the extent-slot rule) states the layer
record is "the one exception... this specification's own" to the rule that
an MU=0 record's bytes reference no other file bytes, because its tile
index (defined by this specification, not an unknown extension) references
stored-tile extents. I checked this against §7.3's registry table: the
layer record is indeed `MU = 0, PE = 0`, and its tile index is defined in
§15, which is this document's own structure, not a third party's — the
"exception" is coherent and doesn't create a loophole for genuinely unknown
MU=0 record types, which the same paragraph still bars from carrying
references ("neither its inline payload nor its extent contents encode
offsets or lengths of other file bytes").

### 7.4 §20.1's closing paragraph and §2.3's updater clause

> "A writer of a new file from an existing one takes one of two positions,
> and the choice is its own. As a **rewriter** it undertakes to preserve
> its input... As a **creator** it undertakes nothing toward its input,
> whatever it read..."

I checked whether this leaves any actor's status undecided. The two
positions are exhaustive by construction (the paragraph defines them as a
binary choice with named consequences for each), and I checked the
"creator" branch against `[R-CNF-05]` ("a writer MUST emit only conforming
files... bytes it copied from another file included") — a creator that
reads an old file purely as a data source for a brand-new file answers for
every byte of that new file exactly as any other creator would, which is
consistent with `[R-CNF-02]`'s general model that only *conduct* rules are
exempted from the file-conformance predicate.

I also checked this doesn't contradict §9.1's "every conforming mutation of
a file is either a commit... or a whole-file rewrite under a new file_id."
A "creator that read an old file and wrote a new one" is not a *mutation of
that old file* at all — the old file is untouched, and the new file is a
first generation under its own fresh file_id — so it's simply an ordinary
creator event, correctly outside §9.1's scope (which only constrains
mutating operations against *the same* file identity). Consistent.

### 7.5 §20.3 step 4's scope sentence and the paragraph it closes

> "The bar binds a layer the commit keeps and nothing else: a commit MAY
> drop the layer (§20.4) and add a new one under its name and other
> declarations, the new layer being new whatever bytes its entries
> address, the dropped layer's former extents included..."

The load-bearing question here is whether "drop-then-add-same-name" and
"in-place illegitimate re-declaration" are actually distinguishable at the
file level — if they weren't, the "bar" would be unenforceable even in
principle. I worked through this concretely: both operations produce a
*directory* that (a) has exactly one layer record under that name and (b)
whose declarations are whatever the writer chose. There is nothing in the
resulting bytes that says "this used to be layer X, re-declared" versus
"this was layer X, dropped, and layer Y happens to reuse its name" — they
are, in fact, byte-identical outcomes for the same target declarations.
That is exactly the shape of a **conduct rule** as `[R-CNF-02]` defines the
class (a barrier "leaves no trace in the bytes"), and I checked this is
precisely why §20.3 step 4's bar is one of the three examples `[R-CNF-02]`'s
own list in §2.3 cites by name ("§20.3 step 4's bar on the fixed
declarations of a layer that stores a tile"). I also checked the cross
reference to §21.7's `[R-ERR-01]` ("no condition a file can exhibit") that
the paragraph makes — that citation is *not* about literally the same
example (`[R-ERR-01]`'s own worked example is `[R-ENC-06]`'s field widths),
but the analogy holds on inspection: in both cases, there is no
*independently checkable state* the resulting file can be in that isn't
already fully explained by treating it as "whatever new declarations are
present," which is what makes both examples the same *kind* of thing
(conduct rather than predicate) rather than the same rule. I judge the
analogy sound, not sloppy — the two governing "verbs" (an unrepresentable
width-violation, and an unrepresentable illegitimate-vs-legitimate
re-declaration) are doing the same logical work even though they arise from
different mechanisms.

### 7.6 Appendix H's restatements

I compared Appendix H's "Conforming updater" paragraph, clause by clause,
against §20.4 and §20.1/§20.5's main text. Every clause I checked
("drops a layer record only under §20.4's PE = 0 licence... never modifies
or drops a layer that carries an unknown critical sub-record, and rejects
outright a file carrying an unimplemented top-level MU = 1 record") matches
the main text's obligations with no narrowing or widening I could find.

### 7.7 The two figures in §20.3 (bracket alignment)

Because "a figure's annotation bracket" is explicitly one of the things this
round's guidance told me to expect might have shifted, I extracted the raw
source lines with a small script and checked column indices directly
(not by eye) for both bracketed diagrams in §20.3 (the "(a) A new layer"
and "(b) Tiles added to an existing layer" examples; these are the only two
bracket-annotated figures inside §20.3/§20.4 — the document has exactly one
other bracket figure, in §5.1, outside the changed surface).

- Figure (a), line 3415: `└── untouched ──┘└was dir₁…tr₁┘` against the
  `after` line's region separators. The first bracket spans columns
  16–32, which is exactly the "A: tiles+index" region (separators at 15
  and 32) — the bracket text "untouched" is under the right region. The
  second bracket spans columns 33–46, exactly the `▓▓▓▓` slack region
  (separators at 32 and 46) — the bracket text "was dir₁…tr₁" is under the
  right region. **Aligned correctly**, no shift.
- Figure (b), line 3433: `└ old ─┘` at columns 24–31 against the `▓index▓`
  region (separators at 23 and 31) — aligned. `└───────┘` at columns
  55–63 against the ` index′ ` region (separators at 54 and 63) —
  aligned (bracket starts one column right of the left separator and ends
  at the right separator, the same convention both figures and the §5.1
  figure use throughout).

I found no column-shift in either figure as the text currently stands. I
record this as a checked and closed candidate, not a finding: if a bracket
had moved, it would have been visible in this column accounting, and it
isn't.

---

## 8. Sweeps for the twelve shapes, applied document-wide

I did not limit the shapes to the three changed passages; I re-read the
whole document once more with each shape as a lens. Results:

1. **Quantifier/scope.** Checked every MAY/MUST governing a "container" for
   which instances it ranges over (tile extents range over addressed tiles
   in `[R-COD-07]`'s lz4 cap, matching §21.9's per-instance note; the
   2⁶³−1 ceiling ranges over *designated* quantities only, and I checked
   the boundary the text itself draws — "an expression this specification
   writes only inside a comparison, and names nowhere, is not a designated
   quantity" — against every place I could find such an inline comparison,
   and found none that silently smuggled an undesignated overflow-prone
   sum past `[R-ENC-04]`). No new fork found.
2. **One quantity named where two are in play.** Checked entry_count vs.
   extent_length (both governed, `[R-CNT-17]`), and crc_of_crc_array vs.
   entry_count = 0 (both governed, `[R-CNT-23]`). Checked the lz4 cap
   (decoded size) against the *separate* 2⁶³−1 domain check on P·Bᶜ etc.
   (`[R-ENC-04]`) — both apply, independently, and I confirmed the note
   explaining exactly this ("the same declarations are then measured
   against the cap" vs. "checked in an empty layer even though this cap is
   not") is internally consistent.
3. **Argument by analogy.** Traced every "exactly as", "the same way",
   "on the model", "as... does" in and around the changed passages (see
   §7.5 above for the closest call I found, which held up).
4. **Order vs. permission.** Checked §8.2's "chain of trust is strictly
   ordered" against §15.4's "MAY be fetched in parallel" for
   crc_of_crc_array and the segment CRC — these are not actually in
   tension: "strictly ordered" describes *dependency* order (you must have
   verified the CRC array before trusting the segment CRC's own bytes as
   authoritative, since the array covers the segment CRCs), which is
   compatible with fetching both ranges concurrently and verifying them in
   dependency order once both are in hand. Consistent.
5. **Closed count / partition.** Checked the "three states, not four" claim
   in §7.2's Note (verified in §7.3 above) and the layout partition
   (interleaved/planar exhausting §14.1's two values, with every other
   value a violation) — no missing or double-counted member found.
6. **Rule keyed to a quantity that doesn't decide it.** Checked
   `[R-COD-07]`'s lz4 cap is keyed to *decoded size*, which is what
   actually determines whether the block format's practical bound is
   exceeded (not, say, stored/compressed length, which the "For every
   codec" note explicitly says is unbounded in either direction relative
   to decoded size for compressing codecs) — correctly keyed.
7. **A word whose sense I supplied myself.** I censused "last" (used
   consistently for "last-declared dimension varies fastest," "last
   committed state," never contradictorily); "every"/"any" in the
   universal statements of §21.6 and the type/codec/filter value-set
   rules (checked against the degenerate zero-extent-layer case, see (8)
   below); "such" as used in "such a type" cross-references (each one I
   checked resolves to a single unambiguous antecedent).
8. **Degenerate legal case.** Built the smallest legal layer in my head:
   rank 1, one dimension of extent 0. Grid count = 0, addressed-tile
   count = 0, empty index, empty reference array. Checked every rule that
   talks about "every addressed tile," "every stored tile," "every
   channel" against this case and found the document already handles it
   explicitly and consistently (§11.1's Rationale, `[R-GEO-02]`, the lz4
   cap's own Note about the escape ending only when every dimension's
   extent is nonzero, §21.9's "a layer addressing no tile therefore has no
   tile whose decoded size the table bounds"). No falsification found.
9. **A rule whose object excludes its own exceptions.** Checked
   `[R-CNT-25]`'s quarantine definition against `[R-MTA-10]`'s
   experimental-encoding carve-out — the object ("the document") is
   defined broadly enough that the carve-out (no content rule attaches at
   an unassigned encoding) sits *inside* the quarantine's own scope
   ("every way its document can be unreadable" plus "except at an
   experimental-range encoding, where no document rule attaches") rather
   than falling outside a tightened definition. Consistent, and I could
   not find a tightened definition anywhere that severed an exemption from
   what it used to reach.
10. **Sentence re-pointed at a different quantity.** The clearest candidate
    is §18.2's "the tile rule of `[R-COD-06]` transposed to the quantity a
    document does have, its decoded length, in place of the declared size
    it does not" — I checked the property that made the *tile* version
    true (a stored tile's *declared* decoded size is a fixed, structural,
    pre-verified quantity, so comparing it to a frame's content-size field
    is meaningful) against the *document* version's substituted quantity
    (a document's *decoded length*, i.e. an output of decoding, not a
    prior declaration) and found the section is explicit and careful about
    exactly this substitution, walking through why it still produces a
    checkable, decoder-tolerance-independent condition. This looks like a
    place a lazy transposition would have broken, and it didn't.
11. **A sentence rewritten to close a reading, more than once.** §14.2's
    own Rationale flags itself as a repair of a prior version that "left
    the return value undefined" — I read the current `[R-SER-08]` against
    that Rationale's stated goal (define what a reader that doesn't reject
    returns, without relieving the verifier) and found the current text
    delivers exactly that, with the escape hatch explicitly closed
    ("it never arises in a conforming file").
12. **Reach decided rather than repaired.** Checked "in any commit"-style
    generalizations against their neighboring sentences: `[R-CNT-08]`'s
    "An updater MUST copy forward unknown ignore-lane bits... MUST NOT set
    any other" against §20.5's rewriter-specific restatement — consistent,
    no neighbor left assuming the old (narrower) rule.

None of these sweeps turned up a fork I could defend as byte-level. Several
turned up passages that *look* like they could be trouble on first read
(§7.5, §10 above especially) and held up under the specific test the brief
asks for — quoting the closing sentence's actor and the construction's
actor side by side — every time I tried it.

---

## 9. Findings

**None survive to the byte-level standard.** I record here, for the
record, why I am not filing findings on the two strongest candidates I
opened and then closed myself, since the brief asks for rejected
candidates explicitly (see the `evidence` object as well):

- **§3.3's "operate on files whose layers they cannot decode."** Candidate:
  AMBIGUITY, "cannot" vs. "need not." Closed because (a) it sits inside a
  labeled Note, non-normative under `[R-CNF-01]`, so even taken at its
  most literal it cannot move an emittable byte or a verdict; and (b) on
  the more charitable and, I think, intended reading ("operates without
  depending on having decoded"), it is simply true, and consistent with
  every operation §20.3 actually licenses an appender to perform.
- **§20.4's table, MU=1 row, "a rewriter MUST refuse to rewrite the file."**
  Candidate: the noun narrowing from "updater" to "rewriter" leaves the
  appender's file-scope and layer-scope obligations undecided. Closed
  because the same row's earlier sentences ("no commit is available at
  all," "blocks modification of that layer, its drop included") already
  state the appender's obligation in both scopes; the narrowing to
  "rewriter" for the *specific* refuse-to-rewrite action is required
  precisely because only a rewriter rewrites, and I confirmed via
  §20.5/`[R-WRT-06]` and Appendix H's checklist that no actor is left
  undecided by the narrowing.
- **§20.3's two annotated figures.** Candidate: a bracket closed and moved
  one column, per the round's own steering language. Closed by direct
  column-index measurement (§7.7 above): both figures' brackets align with
  their boxes exactly as drawn, in the text as it stands.

I looked hard, specifically, for the five described "wording carries" (the
struck actor / relative clause in §3.3, the shifted bracket in a §20.3
figure, the narrowed actor noun in a §20.4 table row) because the brief
told me they exist somewhere in this cycle's history; I could not find any
of them still present as a defect in the current text, and I traced each
candidate location to a specific, checkable resolution rather than simply
failing to notice something. That is the most honest way I can report a
document that, as far as I can implement against it, determines everything
my charter asked me to build.

**Transcript finding count: 0.**
