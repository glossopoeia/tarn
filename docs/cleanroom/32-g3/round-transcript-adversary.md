# Adversary — cleanroom round 32 — working transcript

## 0. Access and disclosure

I read exactly one file: `/Users/robertkleffner/Documents/GitHub/tarn-first-draft/spec/tarn.md`
(4,754 lines, 47,314 words — both figures match the brief). It was at the path the
brief named. I read the whole document in eight `sed` slices, then re-read §5.2,
§6.2, §7.2, §7.4, §11.1, §13.3, §14.2, §15.3, §17.2, §18.2, §19.4, §20.3, §20.4,
§20.5, §21.1, §21.6, §21.7, §21.9, §22.3, §23.1 and Appendix H several times each.

I opened no ADR, no plan, no registry, no conformance directory, no git history,
no web page. I did not list any directory. I did not read the output directory.

**Context I did not ask for.** Material appeared in my context before I began: a
project instruction file pointing at an `AGENTS.md`, and an index of the
maintainer's memory notes whose titles concern this project's harness, its gates,
and its repair habits. I am naming that it appeared and not repeating its
contents; none of it is part of the specification, and no conclusion below rests
on it. Nothing in it named a finding or a section, so far as I can tell from the
titles, and I did not open any of the files it indexed.

Files I wrote, all inside my own scratch directory
`/private/tmp/claude-501/-Users-robertkleffner-Documents-GitHub-tarn-first-draft/r32-round/scratch/adversary/`:

- `adv_crc32c_check.py` — a CRC-32C implementation built from the polynomial the
  document states, plus the document's own check vectors.
- `adv_appA.py` — reconstructs Appendix A's 128-byte file from the field values
  and compares the hexdump.
- `adv_count_instances.py` — parses §21.2–§21.5's tables and counts rows and
  semicolon-separated instances.
- `adv_construct.py` — the byte-level attack construction for finding
  adversary-01.
- `adv_norm.txt` — a whitespace-normalised copy of the document (blockquote `> `
  markers stripped, all runs of whitespace collapsed to one space) so that
  phrase searches cannot be defeated by the hard wrap.
- `adv_f1.txt` — a slice of §21.2 held for width-truncated printing.

I wrote nothing else anywhere. This transcript is the only file I wrote outside
that directory.

---

## 1. Method

### 1.1 The wrap defence

The brief warns that a line-oriented `grep` will miss any phrase that spans the
hard wrap, and that a blockquote inserts `> ` at every wrap point. So before any
search I built `adv_norm.txt`: strip `\n> ` and `\n>` to a single space, then
collapse all whitespace. Every phrase search below ran against that file with
`grep -o -E ".{N}phrase.{N}"` so I saw the surrounding context rather than a
line.

I ran the brief's own control: before resting anything on a zero I searched a
phrase I knew was present in the same passage. Two examples of the control
firing:

- `grep -c "index content"` on the raw file returns 3; on `adv_norm.txt` it
  returns 3 as well, but the *context* around the §13.3 occurrence is only
  legible in the normalised copy — the parenthetical that carries the defect
  ("which, among the declaration changes §20.3 permits …") spans four wrapped
  lines inside a `>` block and no line-oriented search would have shown it as a
  clause.
- `grep "and no other"` on the raw file: 1 hit. On `adv_norm.txt`: 5 hits,
  including the one that matters — "keeps its declarations, with these
  exceptions and no other". The raw-file zero-ish result is exactly the failure
  mode the brief describes, and it would have hidden the closure marker on the
  list this round is about.

### 1.2 The label check

[R-CNF-01] exempts text *labeled* Note, Example or Rationale, and appendices
identified as non-normative — not every `>` block. I checked the label on every
blockquote I relied on. The two that matter below:

- §13.3's sparse-writing block opens `> **Note — sparse writing.**` (line 1941).
  Labelled — non-normative.
- §11.1's block opens `> **Rationale.**` Labelled — non-normative.

I also confirmed the brief's claim that at least one unlabelled blockquote is
normative: §15.1's region diagram is a `>` block carrying no label, and it is the
normative statement of the tile-index region's layout ("[ entry array:
entry_count × 20 bytes ] [ segment CRC array: ⌈entry_count / 2¹⁶⌉ × 4 bytes ]").
Nothing I found lives there, but I checked it rather than assuming it.

### 1.3 Independent arithmetic

Before trusting any of the document's worked examples as a reading aid I
re-derived them. All of the following were computed by me and compared against
the figure the document states; every one matched.

| Quantity | I computed | Document states |
|---|---|---|
| CRC-32C(`"123456789"`) | 0xE3069283 | 0xE3069283 (§4.5) |
| CRC-32C(zero bytes) | 0x00000000 | 0x00000000 (§4.5) |
| CRC-32C of 4 sentinel entries (80 bytes) | 0x80A34955 | 0x80A34955 (§7.4 example) |
| crc_of_crc_array over that 4-byte array | 0xC4EE982E | 0xC4EE982E (§7.4 example) |
| CRC-32C of a full 2¹⁶-sentinel segment | 0xEECB3BB2 | 0xEECB3BB2 (§15.4, App. B) |
| Appendix A trailer CRC over [0,60) | 0x402F157E | 0x402F157E (App. A) |
| Appendix A full 128-byte hexdump | reproduced byte for byte | App. A's dump |
| §7.4 payload size 4+34+18+12+13 | 81 | 81 |
| §7.4 index extent 4×20+⌈4/2¹⁶⌉×4 | 84 | 84 |
| §15.4 index region at entry_count 10⁶ | 20,000,064 B; 16 segments; k=999,999 at segment-relative byte 339,180; segment 15 at [19,660,800, 20,000,000) | same |
| one full segment | 65,536×20 = 1,310,720 = 1.25 MiB | 1.25 MiB |
| §11.4 (300,700) in T=(256,256), G=(4,8) | s=10, in-tile ordinal 11,452, planar c=2 → 74 | same |
| §15.4 entry for disk ordinal 74 | region bytes [1,480, 1,500) | same |
| §14.2 interleaved (a:u8,b:u16), T=(2,3) | Q=3, decoded 18, ordinal 5 at [15,18) | same |
| §14.2 (t:f32,m:bool) | Q=5, decoded 30, ordinal 5 at [25,30) | same |
| §14.3 P=10 alternating, fill false / true | `55 01` / `55 FD` | same |
| §14.5 (5,5)/(4,4) edge tile | 1 real + 15 padding, 32 bytes, values 1–15 = `CD AB` | same |
| §17.3 shuffle of 1.0,2.0,3.0 | `00 00 00 00 00 00 80 00 40 3F 40 40` | same |
| §20.3 example index region for 32 tiles | 32·20+4 = 644 | 644 |
| minimum conforming file from dir_offset≥16, dir_length≥4, F≡0 mod 64 | 128 | 128 (§5.1, [R-CNT-27]) |
| §9.3's ceiling: largest multiple of 64 ≤ 2⁶³−1 | 2⁶³−64 | 2⁶³−64 |
| [R-CNT-06]'s conditions (magic, CRC, F=size, F mod 64, dir_offset≥16, dir_length≥4, sum≤F−64, file_id≠0, reserved zero) | 9 | "states nine" (§2.3) |
| §22.3's residues (slack; unassigned-type extent; trailer mimic; experimental-encoding metadata extent) | 4 | "Four residues" |
| §21.2/3/4/5 row counts | 35 / 49 / 26 / 10 = 120 | 35 / 49 / 26 / 10; §21.8 "120 conditions" |
| §21.2–§21.5 instance count (semicolon rule of §21.1) | 56+116+55+50 = 277 | §21.8 "277 instances" |
| L2's dominance claims: C·N > (C−1)N+(N−1)=C·N−1; P·Q ≥ P·C since Q=ΣBᵢ≥C | both hold | both asserted |
| §20.5's "one row for each of the other seven spaces" | layout L36, linearization L33, type L34, codec L43, filter L45, index enc. L31, metadata enc. R1 = 7 | L31, L33, L34, L36, L43, L45, R1 |
| §10.1's four vehicles, two made conforming by §21.6 | ignore-lane bit; unrecognised `tarn.` key | "the two of §10.1's four vehicles" |

Nothing in that table is a finding. I record it because a reporter that finds
little in an area should be able to say what it did there, and because the
register's own closed counts — 120 and 277 — are exactly the shape the brief
tells me to derive rather than accept, and they hold.

I also checked §21.1's declared specialization pairs by the property it states
("every file exhibiting one row's condition necessarily exhibits another's"):
F1-front ⊂ F6 (a byte-reversed magic is not byte-identical); F1-trailer ⊂ F8;
F35 ⊂ F36; L24 ⊂ L25; F21 ⊂ F22 (extent_length 0 < 5); L10 ⊂ L11. All six hold.
The list says it is not closed, so T14 ⊂ T3 (under codec 1 a length mismatch is
a decoded-length mismatch) being unlisted is not a defect.

---

## 2. The walk: attacks tried, in the order I tried them

My charter is constructive: build a file two conforming verifiers judge
differently, or show which sentence forecloses each attack. I worked outward
from the changed surface (§20.3 first, as the brief directs) and then over the
boundary/degenerate space.

### 2.1 Deriving §20.3's closed list myself

The brief tells me to derive the members from the structure the list governs
rather than accept the document's partition claim. §7.4's layer-record inline
payload has these declaration fields, in table order:

name; layout; linearization; codec; filter; alignment A; slab S; slab alignment
A_slab; rank d; channel count C; d dimension entries (name, extent, tile
extent); C channel entries (name, type, fill); index_encoding; entry_count;
crc_of_crc_array; sub-records.

§20.3's permitted side: layer name, dimension names, channel names; an extent
MAY grow and MUST NOT shrink; a planar layer's channel list MAY be extended at
its end or shortened from its end; a slab or alignment declaration MAY be
declared, re-established or cleared.

§20.3's fixed side: layout, linearization, index encoding, codec, filter, rank,
dimension order, every tile extent, every channel's type and fill, an
interleaved layer's channel list, and the position of every planar channel but
the last.

Placing each derived field on one side:

- name → permitted. layout, linearization, codec, filter, index_encoding, rank →
  fixed. A, S, A_slab → permitted (as the slab/alignment declaration). C → via
  "channel list", planar side permitted, interleaved side fixed. Dimension
  name → permitted; extent → permitted (grow); tile extent → fixed. Channel
  name → permitted; type → fixed; fill → fixed. entry_count,
  crc_of_crc_array → "follow the commit". Sub-records → §20.4.

So the partition does reach every field of §7.4. That claim survives. What does
not survive is the *composition* question, which is §2.2.

I also checked the degenerate instances the brief asks for. A planar layer at
C = 1: "the position of every planar channel but the last" quantifies over the
empty set, which is harmless; shortening from the end would take C to 0 and is
foreclosed by the bounds paragraph's citation of "[R-GEO-01]'s floor of one
channel". A layer with any extent 0 addresses no tile (N = ∏Gᵢ = 0), so it can
never *store* a tile, so the closed list never binds it — which is why the
"re-declared freely" branch and the closed list do not overlap on that case.
Every addressed tile has at least one real position, since tᵢ < Gᵢ = ⌈Eᵢ/Tᵢ⌉
implies tᵢ·Tᵢ < Eᵢ; there are no all-padding tiles, which closes a family of
attacks on §14.5 I had intended to try.

### 2.2 The composition attack — my headline

The two sentences in question sit adjacent:

> "a planar layer's channel list MAY be extended at its end, or shortened from
> its end; and a slab or alignment declaration MAY be declared, re-established or
> cleared as this step provides below. **A commit MAY make several of these
> changes at once.** Every other declaration is fixed for as long as the layer
> stores a tile: … every channel's type and fill …"

and the reconciliation sentence:

> "where a field is on both sides — a dimension extent, a planar layer's channel
> list — the permitted side states the whole of what a commit MAY do to it"

Take a planar layer that stores tiles and, in one commit, shorten the channel
list from its end by one and extend it at its end by one. Each half is on the
permitted side; "several of these changes at once" appears to license the pair;
and the reconciliation sentence hands the channel list wholly to the permitted
side. The net effect on the record is that the last channel's *type* and *fill*
are different — which the fixed side names as fixed.

**Concrete construction.** Planar layer `L`, d = 1, dimension `x`, E = 1, T = 1,
so G = 1, N = 1, P = 1. layout = 2, linearization = 1, codec = 1 (none),
filter = 1 (none), A = S = A_slab = 0. C = 2: channel `a` type 12 (float32) fill
`00 00 00 00`, channel `b` type 12 (float32) fill `00 00 00 00`.
entry_count = C·N = 2; index extent_length = 2×20 + ⌈2/2¹⁶⌉×4 = 44
([R-CNT-17], which I recomputed). Each plane's decoded size is P·Bᶜ = 4, and
under codec 1 [R-COD-04] pins each non-sentinel entry's length to 4.

Generation 1 stores tile ordinal 0 (channel `a`, s = 0) at [16, 20) holding
`00 00 00 00`, and tile ordinal 1 (channel `b`) at [20, 24) holding
`00 00 80 3F` — float32 1.0. I computed the entry crcs: CRC-32C(`00 00 00 00`) =
0x48674BC7, CRC-32C(`00 00 80 3F`) = 0xDD54C4AB. The 40-byte entry array is

```
10 00 00 00 00 00 00 00  04 00 00 00 00 00 00 00  C7 4B 67 48
14 00 00 00 00 00 00 00  04 00 00 00 00 00 00 00  AB C4 54 DD
```

whose single segment CRC I computed as 0x7ED66646, and crc_of_crc_array over
those four bytes as 0x5F2AFCEC. Region length 44 = 40 + 4 ✓.

Generation 2, one commit: shorten the channel list from its end (C: 2 → 1), then
extend it at its end with channel `q`, type 4 (int32), fill `00 00 00 00`. Net
C = 2, entry_count = 2, region length 44. The re-emitted index region carries
entry 0 byte-identical and entry 1 = (20, 4, 0xDD54C4AB) — pointing at the same
four bytes, with the same crc.

Every check I can find passes on the result. Decoded size of channel 1's plane
is still P·Bᶜ = 1·4 = 4, so [R-COD-04]'s codec-1 equality holds and T14/T3
cannot fire. E = T = 1 means there are no padding positions, so [R-SER-05]/T4
and T5 are vacuous. The fill is 4 bytes, matching int32's element size
([R-CNT-23]/L30). entry_count matches C·N ([R-CNT-17]/L21). extent_length
matches the formula (L22). Coverage partitions: [16,20) and [20,24) are each
claimed exactly once, by the new entries; generation 1's index region becomes
slack. Two conforming verifiers handed generation 2 both certify it — the file
carries no register-row condition.

**The four stored bytes `00 00 80 3F` now denote int32 1,065,353,216 where they
denoted float32 1.0, with every checksum in §8 certifying the result.** That is,
word for word, the harm §20.3 says its fixed list exists to prevent:

> "Under new ones the same bytes would denote values, coordinates or padding the
> writer did not store, with every checksum in §8 certifying the result and, but
> for a decoded size or a boolean byte the register witnesses (T3, T14, T2), no
> check any actor owes able to see it (§21.7)."

**Two implementations, and the bytes they differ on.** Updater A reads
"several of these changes at once" as reaching the two alternatives inside the
channel-list bullet and appends generation 2's tail — the 44-byte index region,
the new directory, the pad, the trailer — at F. Updater B reads the alternatives
as exclusive, treats the operation as a change to a fixed declaration, and must
instead perform a whole-file rewrite under a fresh file_id, which is a different
byte sequence (different file_id, and none of generation 1's superseded
structures). The file A emits is conforming; only one reading permits A to
produce it from that input. That is the discriminating test as the brief states
it, so I grade this byte-level.

**The case against, stated honestly.** The same final content is reachable in
*two* commits with no ambiguity at all: commit n shortens the planar channel
list from its end (its stored extents "leave … as slack", §20.3); commit n+1
extends at its end with `q` and emits the appended channel's entry — an entry
"new to this generation", which §20.3 says is "emitted per §15" and which §15
lets point at any legal extent, including the bytes commit n stranded. Both
commits are individually and unambiguously permitted, and the result is
byte-equivalent in content. So a triager may conclude the permissive reading is
the intended one and that the defect is really in the fixed side's unqualified
"every channel's type and fill". I think that is the right repair, but it is a
repair either way: as written, one sentence permits what another forbids, and an
implementer cannot tell which governs. I have left the wording to human
disposition, as the brief's shape 11 asks.

**A second edge the same composition opens.** The bounds paragraph closes with
"a change is permitted exactly where the declarations it produces satisfy every
rule they are subject to" — a test keyed to *declarations and geometry*. It does
not reach the stored-content rules. Take the same construction with old channel
`b` of type 6 (uint8), fill `0x00`, its stored tile the single byte `0x02`
(decoded size P·Bᶜ = 1, conforming), replaced by `q` of type 1 (bool), fill
`0x00`. Decoded size of a packed planar bool plane is ⌈P/8⌉ = ⌈1/8⌉ = 1 — the
same 1 byte, so the size checks still pass. But bit 0 is the only value bit and
bits 1–7 are pad bits, which [R-SER-05] fixes to the channel's fill bit; `0x02`
sets bit 1, so the tile now exhibits T5. The declarations the change produces
satisfy every rule they are subject to, and the file is nonconforming all the
same. Because that output is nonconforming, [R-CNF-05] bars it under both
readings, so this variant does not move the emittable set — but it shows the
bounds paragraph's generalisation is quantified over the wrong thing.

### 2.3 The §13.3 Note against §20.3

The sparse-writing Note in §13.3 reads (normalised):

> "each commit that changes a layer's stored-tile set or its index content —
> **which, among the declaration changes §20.3 permits a layer that stores a
> tile, only a change to entry_count does** — re-emits that layer's whole
> tile-index region (§11.1, §20.3, `[R-WRT-04]`)."

I built two counterexamples.

*(i) Declaring an alignment.* "a slab or alignment declaration MAY be declared"
is on the permitted side. §20.3's own step-4 close says "an aligned layer's
stored tiles — every one the new state keeps, not only those this commit adds —
satisfy its invariant or the declaration is cleared ([R-SLB-01], [R-CNF-05])".
So a commit that declares A = 4096 on a layer whose stored tiles sit at
arbitrary offsets must re-store every kept tile at a 4096-aligned offset. That
changes the index content — every entry's offset — while entry_count is
untouched. [R-SLB-04] states the same obligation for a slab declaration in its
own words ("MUST either re-establish the invariants for every such run — or
clear the declaration").

*(ii) A shorten and a growth that cancel.* Planar layer, d = 1, T = 1, C = 3,
E = 4, so N = 4 and entry_count = C·N = 12. One commit shortens the channel list
from its end (C → 2) and grows E to 6 (N → 6). New entry_count = 2·6 = 12 —
unchanged. Every retained tile's disk ordinal changes: channel 1's tile at s = 0
moves from ordinal 4 to ordinal 6, since the ordinal is c·N + s ([R-GEO-06]).
The index content changes completely while entry_count does not.

There is a third, purely textual counterexample: §20.3 does not classify
entry_count as a permitted declaration change at all. It says "entry_count and
crc_of_crc_array **follow** the commit, the record's extent slot with them" —
they are consequences, not permissions. So the Note names as the sole
index-changing member of a set something that is not a member of that set.

Grading. The block is labelled *Note* and is therefore non-normative under
[R-CNF-01]; the normative criterion in §20.3 step 4 is "Every layer whose
stored-tile set or index content this commit changes has its tile-index region
re-emitted in full", which is keyed to the right quantity. So a writer that
follows §20.3 is safe, and the emittable set does not move. But a
non-normative block that misdescribes the rule it glosses still tells an
implementer what to build, and this one tells a writer that a slab or alignment
declaration is index-free. §11.1's Rationale, by contrast, states the same
territory correctly — "Growth that leaves entry_count unchanged touches the
directory alone", which I checked and which holds, since a grid count can only
rise while N is constant if some other grid count is 0.

### 2.4 The registered record types and the no-subset list

[R-CNF-03] reads:

> "A reader MUST accept every conforming file of a format major version it
> implements, carrying no top-level record of a type it does not implement with
> MUST_UNDERSTAND = 1 — **in a conforming file such a type is necessarily from
> the experimental range**, since a reserved-range type carrying MU = 1 is itself
> a violation — …
> There are no subset profiles: software that declines to support a core codec, a
> core filter, either channel layout, a core sample type, or an assigned
> user-metadata encoding is not a conforming reader, even if it reads all other
> conforming files correctly."

That second sentence is a closed list of what cannot be declined, and the
registered record types are on neither side of it. Type 0x0001 (layer) carries
MU = 1 by registry (§7.3). A reader that does not implement type 0x0001 is,
by the letter of the first sentence, excused from accepting any file that
carries a layer record — and the em-dash gloss "in a conforming file such a type
is necessarily from the experimental range" is then false, because the type in
question is 0x0001. The gloss silently presupposes what the rule never states.

§20.4 relies on the same unstated premise and says so out loud: "Its MU = 1 row
reaches only a type the updater does not implement — **an updater implements both
registered types** — so for an implemented type only the PE bit bites." Nothing
requires that.

There is a reachable consequence, though it needs a nonconforming input.
[R-CNT-22] makes the registry's flags govern "only for record types the consuming
tool does not implement"; for a tool that does *not* implement the type, the
stored flags are authoritative (§20.4's third case). Give such a tool a file
whose layer record carries stored MU = 0 / PE = 0 — an L49 violation, whose
detector is the verifier, so an updater-as-reader is not obliged to detect it.
§20.4's table then hands it the MU = 0, PE = 0 row: "Retain byte-identical, or
drop it". The categorical sentence two paragraphs later — "No commit therefore
removes a layer record … Both registered types carry PE = 1" — is false for that
tool, because for it the registry's PE = 1 is not what governs.

I do not think this moves the emittable set. "a format major version it
implements" is fairly read to require implementing that major's defined
structures; §1 says "no feature a conforming reader can decline" (though §1 is
non-normative); and Appendix H's reader checklist repeats the same list without
record types. So the document supplies an answer, weakly, in three places that
each stop short of stating it. I grade it not byte-level and rank it below the
first two.

### 2.5 The JSON overflow boundary

§18.2's second document restriction:

> "**Finite numbers only.** A reader interprets every JSON number as an IEEE 754
> binary64 value and MAY use a wider representation. A document is unreadable if
> it contains a number whose binary64 interpretation is not finite — which covers
> a magnitude that overflows on conversion, `1e400` being the ordinary case …"

I first tested the obvious reading fork — does "MAY use a wider representation"
let a binary128 reader find `1e400` finite? No: the test is stated over "the
binary64 interpretation" explicitly. Foreclosed.

What is not foreclosed is the rounding direction of the decimal-to-binary64
conversion. IEEE 754 conversion is correctly rounded *under a rounding-direction
attribute*, and the document names none. I computed the exact boundary: DBL_MAX
is (2⁵³−1)·2⁹⁷¹ and the midpoint to 2¹⁰²⁴ is 2¹⁰²⁴ − 2⁹⁷⁰, a 309-digit integer
beginning `17976931348623158079372897140530341507993413271003…`. I verified with
`Decimal` that this is exactly (DBL_MAX + 2¹⁰²⁴)/2, and that a default
round-to-nearest-even conversion (Python's `float()`, i.e. `strtod`) yields
`inf`. Under roundTowardZero the same digits yield DBL_MAX, a finite value.

So a user-metadata document whose only unusual content is that integer literal
is, to verifier A (default rounding), an R8 violation and therefore a
nonconforming file; to verifier B (roundTowardZero, or a parser that clamps on
overflow, which several fast JSON parsers do), a conforming file. Both can
defend the verdict from this text, which says only "IEEE 754 binary64" and
"overflows on conversion".

That is a genuine two-verifier verdict fork on a specific byte sequence, so I
grade it byte-level. I rank it last for plausibility: the window is half an ULP
wide at the top of the binary64 range, and most implementations use `strtod`
under the default rounding attribute and would agree. It is the only clean
two-verifier fork I found.

### 2.6 The compactor's regeneration trigger

§20.5's regeneration paragraph:

> "An entry §15.3 classifies reject-tile on a structural ground is neither —
> `[R-IDX-03]` gives it no stored extent for a re-pointing to target — so
> regenerating the region cannot proceed without meeting it, and the violation is
> thereafter one the compactor has detected. `[R-WRT-06]` then obliges refusal"

and [R-WRT-07] fixes when regeneration happens: the compactor "regenerates each
tile-index region **any of whose stored extents the output relocates**". A
compactor is free to place structures anywhere ("A compactor MUST preserve
content, and preserves no placement"). So whether a compactor is obliged to
refuse a given input turns on a placement choice it is free to make.

I constructed the case. Input: front [0,16); layer A's tiles [16,100); A's index
[100,200); the superseded dir₁/pad/trail₁ run [200,384) as slack; a file-scope
user-metadata extent [384,400); dir₂ and trail₂ after it. A's index contains one
entry with offset = 5 — a T8 condition, verifier-invisible to the index chain
because [R-IDX-04] verifies crc_of_crc_array and the segment CRCs, not the
entries' value domains. A compactor that packs the output as front, A's tiles at
[16,100), A's index at [100,200), the metadata extent at [200,216), then the
directory, relocates none of A's stored extents, so it never regenerates A's
index and never classifies that entry — and emits an output carrying it. A
compactor that chooses any other placement for A's tiles must regenerate, meets
the entry, and MUST refuse.

Whether the first compactor is conforming turns on how [R-WRT-09]'s list reads:
"each relocated extent's checksum, **including every stored tile's entry crc**".
Restrictively, "including" is appositive to "relocated extent" and only the
relocated tiles' crcs are owed — and to verify a tile's crc a compactor must use
its entry, which under §19.4 step 4 means classifying it under §15.3, so a
universal reading closes the hole and a restrictive one does not. The same
paragraph's opening — "it relies structurally on every structure it copies, so it
MUST verify each link of the chain" — points to the universal reading. I grade
this an OBSERVATION rather than a fork: it is decidable from the sentence's
opening clause, but only after reading a compound list against a governing clause
two lines above it, which is disproportionately expensive for the size of the
consequence, and the document's own remark that the bound is on "how far a
compactor goes looking" does not mention that the *trigger* is a free choice.

---

## 3. Attacks I opened and closed

These are the suspicions I formed and the sentence that killed each. I record
them because the brief asks a clean lane to prove it looked.

**Front-block overlap falls through [R-CNT-13]'s partition.** §5.2 says the front
signature block is not a *structure* ("belongs to exactly one of: the front
signature block; or a structure"), and [R-CNT-13]'s three overlap clauses are
all stated over structures — so a structure overlapping [0,16) seemed to be
classified by none of them. Closed: no such overlap is reachable, because every
extent-bearing rule floors the offset at 16 (F31/L16/T8), and F33's own condition
cell says so: "a claimant reaching the front signature block or the live trailer
is instead caught by the bounds rows F9/F10, F30/F31/F32, L15/L16/L17 and T8/T9,
each at its own tier".

**A tile extent ending exactly at F − 64.** [R-CNT-13] and §15.3 both bar
"past"/">" F − 64, so equality is legal. But [R-CNT-05] requires the directory to
be the last structure, so a tile ending at F − 64 would have to sit after the
directory or overlap it. Closed by [R-CNT-05] plus F7; the looser bound in
[R-CNT-13] is simply not the binding one.

**F5 against a foreign-major file.** [R-CNT-27] states its 128-byte floor
unconditionally ("A reader MUST treat a shorter file as a validity error at file
scope"), which looked like it would fire against a 64-byte file declaring
version_major = 2 and turn a *cannot establish* into a *nonconforming*. Closed by
[R-CNF-13] and §2.3's Note, which name F5 by number as a row that does not reach:
"the 128-byte floor it asserts is derived from a directory of at least 4 bytes at
an offset of at least 16 and a 64-aligned F ([R-CNT-27]), and those are format
major 1's."

**§23.1's "That is every case".** I enumerated every way a commit can make sample
data unreachable under the new closed list — superseding a tile, unstoring a
tile, shortening a planar channel list, dropping a PE = 0 record, and growing an
extent — and checked whether the carrying structure always leaves the live state.
It does: §20.3 says a removed channel "leaves its stored tiles' extents as slack",
superseded extents "become slack", and a growth can only turn padding into real
positions, never the reverse, since tile extents are fixed, rank and dimension
order are fixed, and a shrink is a rewrite. I also checked whether a growth can
increase a stored tile's padding: padding at tile coordinate tᵢ exists iff
(tᵢ+1)·Tᵢ > Eᵢ, and growth only raises Eᵢ, so padding only shrinks. §23.1's claim
holds.

**The two-commit re-declaration escape.** A commit may not re-declare a layer it
itself empties ("unstoring or superseding every tile of a layer and re-declaring
it is one operation, and it is a rewrite"), but commit n may empty it and commit
n+1 re-declare it freely and re-address the stranded bytes. I first read this as
a hole in the bar. Closed: in generation n the layer stores no tile, so the bar's
subject does not exist, and commit n+1's writer is authoring a new channel's data
rather than reinterpreting a stored tile. The document's premise — "The line is
drawn where a stored tile's meaning is fixed" — is about a tile stored in the
superseded generation, and it is intact. I do report this as the reason a triager
might treat §2.2's permissive reading as intended.

**Channel names as a third "both sides" field.** "an interleaved layer's channel
list" is fixed, and "its dimension and channel names MAY change" is permitted, so
channel names on an interleaved layer looked like a third field on both sides —
which would falsify the reconciliation sentence's list of exactly two. Closed by
the principle paragraph ("a name enters no map") and Appendix H's updater
checklist ("its names"), which together fix "channel list" as membership and
order rather than the entries' names. Weak but sufficient; I did not file it.

**[R-CNF-02]'s "are the cases this text states".** I suspected a missing member —
[R-WRT-06]'s fresh-file_id obligation, whose violation is invisible in the output
bytes, and [R-WRT-05]'s byte-identical re-emission, which §20.4's own Rationale
admits no observer can check ("It cannot, from the format"). Closed: the class
[R-CNF-02] closes is defined by *express declaration* — "a writer obligation whose
violation this specification **expressly declares** not to be a file-conformance
violation" — and neither is expressly declared, so neither is a member. The
general principle "File conformance is a pure predicate on bytes" settles what
happens to those files without needing the carve-out. I spent real time here and
it came out clean.

**A verifier fork on the slack total, the *cannot establish* grounds, or the
experimental-encoding metadata record.** All three are stated to be capability
facts about the verifier rather than facts about the file ([R-CNF-11],
[R-MTA-10], [R-ERR-04]), and each explicitly says certification is unaffected or
that the verifier reports rather than judges. Two verifiers with different
resource budgets legitimately return *conforming* and *cannot establish* on the
same file, and the document says so. Not a defect.

**R8's bare tokens as a specialization of R7.** `NaN`, `Infinity`, `-Infinity` are
not admitted by RFC 8259, so a document containing them is also not well-formed
JSON (R7). §21.1's specialization list does not name the pair, but it says the
list is not closed and that the property decides. Closed.

**Ill-formed UTF-8 outside a key or string value.** R5's instances cover keys and
string values only. I checked whether an ill-formed byte elsewhere in a document
has a row: numbers and literals are ASCII-only and JSON whitespace is ASCII, so
any such byte produces a parse failure and lands on R7. Complete.

**[R-COD-06]'s Window_Size derivations at small tiles.** The Note claims "no
conforming file turns on which derivation a reader implements". I checked: with
Single_Segment_Flag set, RFC 8878 makes Window_Size the frame content size, which
[R-COD-06] already pins to the decoded size; without it, the Window_Descriptor
cannot express less than 1 KiB, so a sub-1-KiB tile must be single-segment. The
claim holds.

**§10.2's "Two spaces carry no experimental range".** One of the two (the trailer
flag lanes) is not a row of §10.2's table, so "Value 0 is invalid in every space
above" does not reach it — and flags = 0 is of course valid. Closed: the flag
lanes are named as *not* being in the table ("which §6.3 partitions instead").

**The point-vs-region request asymmetry** (§19.4 step 1: a point request outside
the extents fails, while "a range whose every interval holds a single position is
a region request" and succeeds returning nothing). Deliberate and stated; it is
an API distinction, not a byte or verdict distinction.

**Degenerate and boundary files I built and could not break.** The 128-byte
minimal file (reproduced byte for byte, §3 above). A file whose directory ends
exactly at F − 64 with a zero-length pre-trailer pad (dir_offset 16,
dir_length 48, F 128) — legal. A conforming file carrying a 100-byte extent of an
experimental-range record type, covered by no checksum and inspected by nobody,
which §22.3 names as a stated residue. A user-metadata extent of exactly 6 bytes
holding `{}` plus its CRC — a conforming, vacuously sorted, key-free document. A
1-byte stored tile (planar bool, P ≤ 8, codec 1). A layer with a huge P and one
extent 0, which escapes both [R-COD-07]'s lz4 cap and §21.9's decoded-tile row
because both are quantified over *addressed* tiles, and which a conforming reader
must therefore accept — the document states this in [R-COD-07]'s Note and
§21.9's per-instance paragraph, and the two agree.

---

## 4. Findings

Five. Each is stated with its location, its quotation, the readings, and the
byte-level answer.

### adversary-01 — AMBIGUITY — byte-level

**§20.3 step 4, [R-WRT-04].** "a planar layer's channel list MAY be extended at
its end, or shortened from its end; … A commit MAY make several of these changes
at once. Every other declaration is fixed for as long as the layer stores a tile:
… every channel's type and fill …"

Reading 1: the two channel-list alternatives compose, so one commit may shorten
from the end and extend at the end, and the resulting record's last channel
carries a different type and fill. Reading 2: they are exclusive, and the net
effect on the channel list must be one or the other, so the composite is a
rewrite. The reconciliation sentence ("the permitted side states the whole of
what a commit MAY do to it") points to reading 1; the fixed side's "every
channel's type and fill" points to reading 2, and the section's own statement of
purpose is that under changed declarations "the same bytes would denote values …
the writer did not store". Construction and both verdicts in §2.2 above. I pick
reading 2 as the one the section's principle requires, and I flag that the
wording as it stands admits reading 1.

Byte-level: yes. Given the same input file, updater A appends generation 2's tail
and updater B may not; A's output is a conforming file, and only one reading
permits an updater to produce it.

### adversary-02 — CONTRADICTION — not byte-level

**§13.3's *Note — sparse writing* against §20.3 step 4, [R-WRT-04].**

Note: "each commit that changes a layer's stored-tile set or its index content —
which, among the declaration changes §20.3 permits a layer that stores a tile,
only a change to entry_count does — re-emits that layer's whole tile-index
region".

§20.3: "a slab or alignment declaration MAY be declared, re-established or
cleared"; "an aligned layer's stored tiles — every one the new state keeps, not
only those this commit adds — satisfy its invariant or the declaration is
cleared"; and "entry_count and crc_of_crc_array follow the commit".

Counterexamples in §2.3 above. The Note is labelled and therefore non-normative,
and the normative criterion in §20.3 is keyed to index content rather than to
entry_count, so a writer following §20.3 emits nothing wrong. It is still a gloss
that tells an implementer the opposite of the rule it cites, and it names as the
sole member of a set a field §20.3 classifies as a consequence rather than a
permission.

### adversary-03 — AMBIGUITY — not byte-level

**§2.3 [R-CNF-03], with §20.4.** "in a conforming file such a type is necessarily
from the experimental range"; "There are no subset profiles: software that
declines to support a core codec, a core filter, either channel layout, a core
sample type, or an assigned user-metadata encoding is not a conforming reader";
and §20.4's "an updater implements both registered types".

Nothing requires a conforming reader or updater to implement record types 0x0001
and 0x0002. The no-subset list omits them, and two passages assert the premise
rather than stating it. Consequences in §2.4 above, including §20.4's categorical
"No commit therefore removes a layer record" failing for a tool that does not
implement type 0x0001 and meets a nonconforming input whose layer record stores
MU = 0 / PE = 0.

Byte-level: no. "a format major version it implements", §1, and Appendix H each
supply the missing premise, weakly but consistently, and no implementation would
land on the other side.

### adversary-04 — AMBIGUITY — byte-level

**§18.2, [R-MTA-04], and §21.5 row R8.** "A reader interprets every JSON number as
an IEEE 754 binary64 value and MAY use a wider representation. A document is
unreadable if it contains a number whose binary64 interpretation is not finite —
which covers a magnitude that overflows on conversion, `1e400` being the ordinary
case".

The conversion's rounding direction is unnamed. Under roundTiesToEven the exact
midpoint 2¹⁰²⁴ − 2⁹⁷⁰ (the 309-digit integer I computed and verified) overflows
to infinity and the document is R8-nonconforming; under roundTowardZero, or under
a parser that clamps to DBL_MAX, it is finite and the file is conforming. Two
verifiers, two verdicts, both defensible from this text. Detail in §2.5.

Byte-level: yes — it decides accept/reject on a specific byte sequence. Ranked
last for plausibility: the window is half an ULP at the top of the range and the
default rounding attribute is what most implementations use.

### adversary-05 — OBSERVATION — not byte-level

**§20.5, [R-WRT-07] with [R-WRT-09] and [R-WRT-06].** "regenerates each
tile-index region any of whose stored extents the output relocates"; "regenerating
the region cannot proceed without meeting it, and the violation is thereafter one
the compactor has detected. `[R-WRT-06]` then obliges refusal"; "each relocated
extent's checksum, including every stored tile's entry crc".

Whether a compactor must refuse an input carrying a structurally malformed index
entry turns on whether it regenerates that layer's index region, which
[R-WRT-07] keys to whether any of that layer's stored extents relocate — a
placement choice §20.5 leaves free ("preserves no placement"). Construction in
§2.6. The question is decided by [R-WRT-09]'s opening clause ("it relies
structurally on every structure it copies, so it MUST verify each link of the
chain"), which forces the universal reading of the "including" and closes the
hole — but only after reading a compound list against a governing clause two
lines above it, which is why I file it as decidable-but-expensive rather than as
a fork.

---

## 5. Where I found little, and what I did there

My charter's core ask — a file two conforming *verifiers* judge differently — I
met once, and thinly (adversary-04). I want to be explicit about what I did that
would have found more.

I walked every §21.2–§21.5 row against a constructed file or a boundary value,
and I derived the register's own closed counts (120 rows, 277 instances) rather
than accepting them; both matched, which is evidence the register is tight rather
than evidence I did not look. I checked the completeness of each scope's row set
by enumerating conditions from the rules rather than from the table — the
trailer's nine, the extent-slot family, the index-entry family, the codec family,
the document family — and found no unregistered detectable condition. I built the
boundary files the charter names: the smallest conforming file (reproduced byte
for byte), a zero-length pad, a one-byte tile, a zero-member document, a
zero-extent layer under an lz4 declaration that would otherwise blow the cap, an
unassigned-type extent covered by no checksum, and the degenerate C = 1 and
d = 1 and P = 1 cases the closed list's members bottom out at. I tried every
reserved and experimental value in every position I could find for it, and every
combination of the two record flag bits at both scopes. The document answered all
of them, usually in a sentence that names the case by number.

The structural core is genuinely tight, and the seams the charter points at —
reader versus verifier, ordering versus content, one rule stated twice — are
each closed by an explicit sentence, most of which name the row or the requirement
they are closing. What is not tight is the newest prose: the composition of a
closed list's members (adversary-01), and a Note written for the rule the list
replaced (adversary-02). That is the pattern the brief predicted, and it is where
both of my substantive findings landed.
