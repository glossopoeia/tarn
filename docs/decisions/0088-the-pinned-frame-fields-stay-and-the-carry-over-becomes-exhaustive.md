# 0088. The pinned frame fields stay enforced, and §18.2's carry-over becomes exhaustive

- Status: Accepted (resolves Q-E4; re-closes Q-E1's zstd half)
- Date: 2026-08-24
- Covers: the enforcement mode of `[R-COD-06]`'s four pinned frame-header
  fields and their rows T19–T22; §18.2's carry-over of `[R-COD-06]`
- Confirm: none

## Context

Q-E4 asked whether zstd's pinned frame-header fields should stay normative
reader checks, become **ignored** fields, or move to a recommended verifier
appendix. It priced four options and gave a per-field triage. Two measurements
and one survey settle it, and all three point the same way.

**What a decoder does.** Each violating frame was built with the corpus's own
`codec_streams.zstd_frame()` and decoded with libzstd. A lying
`Frame_Content_Size` fails (*data corruption detected*); a nonzero
`Dictionary_ID` with no dictionary fails (*dictionary mismatch*); a set
`Content_Checksum_flag` over a wrong checksum fails (*restored data doesn't
match checksum*). An oversized `Window_Size` **decodes cleanly**. So the only
one of the four that a decoder does not already reject is the one every option
agreed to keep. Enforcing the other three therefore costs a reader nothing —
the decode fails either way — while *declaring them ignored* would make a file
conforming that no `ZSTD_decompress()` reader can serve, leaving the tile's
readability a property of the decoder's tolerance. That is `[R-CNF-02]`'s
failure relocated, not removed. Q-E4's triage was wrong on two of the three: the
content-checksum flag does not "break nothing", and the content-size field is
not "safe to ignore".

**What an encoder emits.** Q-E4's adoption premise — that a writer "cannot use
a stock `ZSTD_compress()`" — does not survive measurement. One-shot libzstd
emits a fully conforming tile frame at 28 B, 4 KiB, 300 KB, 4 MiB and 40 MiB
with no configuration: it sets `Single_Segment_Flag`, which makes `Window_Size`
equal `Frame_Content_Size` equal the decoded size, satisfying all four rows at
once. A tile writer always knows its decoded size (§14.2 derives it from
declarations), so this is the API it uses. The measured friction is elsewhere
and is small: the `zstd` CLI sets the checksum flag by default (one flag), and a
streaming encoder given no pledged size declares the level's window — 2 MiB —
on every tile below it, which breaks **T21 alone**, the row every option keeps.
Option (b) would have dropped the three rows that cost a writer nothing and kept
the one that costs it everything.

**What the cohort did.** The record does not split on how much a container knows
about a codec; it splits on *what kind* of knowledge. Containers that hoisted a
codec's **parameters** into container fields failed — TIFF 6.0 §22 broke JPEG's
tables out into tags, and TIFF Technical Note #2 replaced the whole design,
naming the cause: those parameters were "separate fields which the TIFF control
logic must manage, which is bad software engineering". Containers that carry
only an **identifier** pay `[R-CNF-02]`'s price directly: PMTiles v3's
compression byte has a `0x00 Unknown`, and Zarr v3's core specification
constrains no codec's internal byte format at all. Containers that pin a
codec's header fields *softly* fail in production: the AV1 ISOBMFF binding says
`av1C`'s fields "shall match" the Sequence Header OBU while making the OBU
authoritative on conflict, and browsers then had to decide independently whether
to reject a file whose `seq_level_idx_0` disagreed.

The one container that does what TARN does has no such record. PNG §10.1 pins
the zlib datastream's header against what the container already fixes: the
method code "shall specify method code 8", the window is "not more than 32768
bytes", and "the additional flags shall not specify a preset dictionary" —
three of TARN's four rows, present verbatim in role, checked in the header
rather than awaited as a decode failure.

## Decision

**All four fields stay normative reader checks.** T19, T20, T21 and T22 are
unchanged, R4's sixteen instances are unchanged, and the register keeps its 121
conditions over 277 instances and 331 vectors. Q-E4 resolves to no change in
enforcement, and Q-E1's zstd half re-closes on ADR-0039's terms.

The reason is the cross-codec symmetry, which Q-E4 did not weigh: **T19, T20 and
T22 are zstd's T15 and T23.** The rule governing the whole codec column is
*strike any declaration the container already carries; where the format will not
let it be struck, pin it.* For deflate the wrapper is separable, so one row —
T15 — removes a redundant window, checksum and length together. For lz4 the
frame is separable, so T23 does the same. zstd's frame is **not** separable
(`ZSTD_decompressBlock` needs caller-managed window and dictionary state), so
the four fields survive and TARN pins each to what the container already fixes.
Dropping them would make zstd the only codec of the three whose stored bytes may
carry a redundant checksum and a redundant length that nothing checks — the
exact two things T15 rejects in a gzip-wrapped tile.

Nothing here is codec *configuration*: TARN records no level, strategy, table or
window setting. The four rows are two prohibitions and two equalities against
quantities the container derives on its own, which is the side of TIFF's line
that TIFF itself arrived at.

**§18.2's carry-over becomes exhaustive.** The defect class Q-E4 correctly
identifies is real, and it is not the enforcement mode. §18.2 transposes
`[R-COD-06]` to a document through a **closed enumeration** — "the frame
constraints of `[R-COD-06]` that do not reference a tile", followed by a list —
so any constraint §17.2 states and §18.2 omits falls through to nothing. That is
the mechanism behind both recent defects on this surface: the declared window
(round 20, ADR-0085) and the content-size field (round 21, ADR-0087). Round 21's
findings named it in terms: "the carried-over list is closed and enumerated".

The enumeration is therefore inverted. **Every constraint `[R-COD-06]` places on
the frame carries over, named in §18.2 or not, save two: what `[R-COD-06]`
states against a tile's declared decoded size, and what it states about the
declared `Window_Size`.** §18.2 replaces both, as ADR-0085 and ADR-0087 decided.
The remaining list is illustrative, and is marked as such.

## Consequences

The register does not move, and no vector changes. A future constraint added to
`[R-COD-06]` now reaches a document without a second edit, which is what the two
recent defects cost.

Two constraints reach a document that the closed list did not carry, neither of
which adds a row. `[R-COD-06]`'s prohibition on compressing "using a dictionary
— whether or not the header discloses one" now binds a document's writer as it
binds a tile's; the undisclosed case stays undetectable and §21.7 already says
so, so there is nothing new to register. And `[R-COD-06]`'s bar on sizing any
buffer from a length the frame declares now binds a document's reader
explicitly, where §18.2 had only implied it by giving the reader a bound of its
own choosing; that bar constrains a reader, not a file, and the register
registers conditions on files.

What is foreclosed: the adoption argument for unpinning cannot be re-run without
new measurements, since the ones here show the friction lies in `Window_Size`
and nowhere else. If that friction is ever worth paying for, the honest lever is
`Window_Size`'s bound — relaxing it from the tile's decoded size to the larger
of that and §21.9's 8 MiB guarantee — and the cost is an exception in §22.2's
statement that a reader allocates from geometry and never from a payload. That
is a separate question and is not opened here.

## Precedent

- PNG §10.1's constraints on the zlib datastream — method code, window ceiling,
  and the preset-dictionary prohibition — which are three of these four rows in
  the most widely deployed container that carries a codec it did not define.
- TIFF Technical Note #2's replacement of TIFF 6.0 §22, and its statement of
  what went wrong: a container managing a codec's broken-out parameters. The
  replacement carries the codec's tables as one uninterpreted block instead.
- PMTiles v3's `0x00 Unknown` compression value and Zarr v3's unconstrained
  codec byte formats, as the cost of an identifier-only container.
- The AV1 ISOBMFF binding's `av1C` "shall match" with the OBU authoritative on
  conflict, as the cost of pinning a field without making the mismatch fatal.
- `[R-CNF-02]`, which is what all three of those costs are denominated in.
