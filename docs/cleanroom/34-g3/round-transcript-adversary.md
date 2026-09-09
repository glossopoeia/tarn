# Cleanroom round 34 — Adversary transcript

## 0. Access and disclosure

I opened exactly one file: `/Users/robertkleffner/Documents/GitHub/tarn-first-draft/spec/tarn.md`
(4,838 lines, 48,163 words by `wc`). I read it end to end in ten `sed -n` slices. I opened no
ADR, no `PLAN.md`, no `AGENTS.md`, no conformance directory, no registry, no git history, and I
ran no web search or fetch. I did not list any directory. I did not read the output directory.

The spec was where the brief said it was: `spec/tarn.md`.

**Context I did not ask for.** My runtime placed material in my context before I began: a project
instruction file pointing at `AGENTS.md`, a git-status block naming the recent commit subjects,
and an index of the maintainer's memory notes. Some of those lines name this round's position and
gesture at where this project's defects have historically lived. I did not open any of the files
they name, and I have not used any of their content to reach or to close any conclusion below —
every finding here is anchored to a quotation I pulled out of `spec/tarn.md` with a search I ran
myself. I disclose their appearance rather than their contents, as instructed.

Files I wrote, all inside my own scratch directory
`/private/tmp/.../r34-round/scratch/adversary/`:

- `flat.txt` — a whitespace-normalised, blockquote-stripped copy of the spec, so that hard-wrapped
  and `> `-prefixed phrases could be matched. Every phrase count below was taken against this, not
  against a line-oriented grep.
- `crc32c_adv.py` — my own CRC-32C implementation and the constant checks.

I chose those two names deliberately (`_adv` suffix, own directory) rather than the obvious
`crc.py` in a shared place.

---

## 1. Method

The document is hard-wrapped and blockquotes carry `> `. A line-oriented `grep` for
"slab or alignment declaration" returns 0 in this file because the phrase wraps. I therefore built
`flat.txt` first and ran every phrase search against it. Before resting anything on a zero I ran a
control search for a phrase I already knew was in the same passage (e.g. `re-establish`, 5 hits,
against `slab or alignment`, 4 hits — both in the same paragraphs).

I then did four things:

1. Re-derived every number and checksum the document states that I could compute without a file.
2. Enumerated the register mechanically (rows, instances) and compared against §21.8's totals.
3. Built concrete files on paper — the minimal 128-byte file, a minimal one-empty-layer file, a
   planar slab-declared layer through a growth that reshuffles ordinals — and walked each rule.
4. Ran the twelve shapes over the sixteen changed passages, and then over the untouched text the
   changed passages depend on.

---

## 2. Derived numbers

I wrote my own CRC-32C (Castagnoli reflected, poly 0x82F63B78 reflected form, init 0xFFFFFFFF,
final XOR 0xFFFFFFFF) and checked it against §4.5's check vector before using it.

| Quantity | Document | My value |
|---|---|---|
| CRC-32C("123456789") (§4.5) | `0xE3069283` | `0xe3069283` ✓ |
| CRC-32C(zero bytes) (§4.5) | `0x00000000` | `0x0` ✓ |
| §7.4 example: CRC over 80 bytes of 4 sentinel entries | `0x80A34955` | `0x80a34955` ✓ |
| §7.4 example: crc_of_crc_array over that 4-byte array | `0xC4EE982E` | `0xc4ee982e` ✓ |
| §15.4 / Appendix B: CRC of a full 2^16-sentinel segment | `0xEECB3BB2` | `0xeecb3bb2` ✓ |
| Appendix A: trailer CRC over trailer bytes [0,60) | `0x402F157E` | `0x402f157e` ✓ |

I reconstructed Appendix A's trailer byte for byte from §6.2's layout (magic; major 1; minor 0;
flags 0; dir_offset 16; dir_length 4; committed_file_length 128; file_id 0x0123456789ABCDEF;
12 zero reserved bytes) and got the stated CRC. Appendix A's hex dump is internally consistent
with its annotation table at every offset I checked.

Register arithmetic, derived by parsing every `| Fn |`/`| Ln |`/`| Tn |`/`| Rn |` row and applying
§21.1's counting rule ("Instances within a cell are separated by semicolons, and a cell reading —
is one instance"):

| | rows | instances |
|---|---|---|
| §21.2 file scope | 35 (F1–F36, F11 struck) | 56 |
| §21.3 layer scope | 49 (L1–L49) | 116 |
| §21.4 tile scope | 26 (T1–T26) | 55 |
| §21.5 ignored records | 10 (R1–R10) | 50 |
| **total** | **120** | **277** |

§21.2 states 35, §21.3 states 49, §21.4 states 26, §21.5 states 10, and §21.8 states
"120 conditions over 277 instances". All six figures reproduce exactly. I also spot-checked
§21.1's two stated instance axes (layout formulas enumerated; magnitude comparisons enumerated in
both directions, one-directional comparisons in one) against L21, L22, L30, T3, T14, T21, T22,
L44, L39, L29, F17, F13, F23, R4, R5, R7 — every cell counts as the rule says it should.

I extracted the Detector column: **20 rows carry `verifier`** — F7, F25, F26, F27, F28, F33, F36,
L18, L25, L40, L41, L42, L46, L47, L48, L49, T2, T4, T5, T26 — and 100 carry `reader`. I checked
all twenty against Appendix H's "Conforming verifier" checklist and every one is named there,
directly or by its rule (F7; extent overlap = F33/L18; flag bits = F25/F26/L46/L47 and
F28/L49; reserved-range type = F36/L25; alignment and slab = L40/L41/L42; decoded-content =
T2/T4/T5 and T26 by way of them; member ordering = F27/L48). No verifier-detected row is missing
from Appendix H.

Other derivations I checked and found correct:

- §11.2 example: G=(4,8), N=32, P=65,536; ⌈1000/256⌉ = 4.
- §11.4 example: (300,700) → tile (1,2), s = 10; in-tile (44,188) → 44·256+188 = 11,452;
  planar channel 2 → 2·32+10 = 74.
- §15.4 example at entry_count = 1,000,000: 16 segments (15 full + 16,960), 64-byte CRC array,
  region 20,000,064 bytes, k=999,999 at segment-relative 339,180, segment 15 at
  [19,660,800, 20,000,000), array at [20,000,000, 20,000,064), full segment 1,310,720 = 1.25 MiB.
- §15.4 second example: disk ordinal 74 → entry bytes [1,480, 1,500); channel 3 unstored →
  entries 96–127.
- §7.4 example: G = ⌈100/32⌉ = 4; index region 4·20 + 1·4 = 84; inline payload offsets
  0/4/5/7/9/11/19/27/35/36/38/40/48/56/63/68/69/77 summing to exactly 81, with 4+34 for name and
  the nine scalars, 18 for the dimension entry, 12 for the channel entry, 13 trailing.
- §14.2 examples: Q=3 → 18 bytes, ordinal 5 at [15,18); planar b-plane 12 bytes, ordinal 5 at
  10–11; float32+bool → Q=5, 30 bytes, ordinal 5 at [25,30).
- §14.3 example: alternating values give `55 01`, and with fill true `55 FD` (pad bits 2–7 set).
- §14.5 example: extents (5,5) / tiles (4,4) → the (1,1) edge tile has 1 real and 15 padding
  positions, 32 bytes at uint16.
- §17.3 example: s=4, n=3 shuffle of `00 00 80 3F 00 00 00 40 00 00 40 40` gives
  `00 00 00 00 00 00 80 00 40 3F 40 40`.
- §20.3 example: 32·20 + 4 = 644.
- §9.3's ceiling note: F ≤ 2^63 − 1 and 64 | F gives 2^63 − 64 as the largest reachable F.
- §2.3's reach derivation: I re-derived which §21.2 rows assert an invariant `[R-CNT-24]` fixes
  (magic at F−64, major/minor at F−56, CRC at F−4 over [F−64,F−4), constant front block) and got
  exactly F1 (both instances), F6, F8, F14 — the four §21.2's preamble names, and no others. F13
  (64-alignment of F) and F15 (reserved bytes) sit in the 48 redefinable bytes and correctly do
  not reach; F5's 128-byte floor is derived from format-major-1 minimums and correctly does not.
- §20.5's vehicle accounting: §10.1 has four vehicles; §21.6 makes two of them conforming
  (ignore-lane bit; unrecognized `tarn.` key); the other two land as reserved-range violations,
  and the cited rows are F36/L25 for record type plus exactly one row for each of §10.2's other
  seven spaces — layout L36, linearization L33, sample type L34, codec L43, filter L45, index
  encoding L31, metadata encoding R1. Seven cited, seven spaces. Correct.

---

## 3. Constructions

### 3.1 The minimal conforming file (128 bytes)

Reproduced from §5.1's example and Appendix A, checked against [R-CNT-01], [R-CNT-27],
[R-CNT-06], [R-CNT-05], [R-LIF-02]. Directory at [16,20) holding CRC-32C(∅) = 0; 44 bytes of pad
(step 5 pads to the next 64-boundary: 20 → 64); trailer at [64,128); F = 128, a multiple of 64;
dir_offset + dir_length = 20 ≤ F − 64 = 64. Verified trailer CRC. Slack total a verifier owes:
128 − 16 − 4 − 64 = 44. No fork.

### 3.2 A minimal file with one empty layer

Built to exercise the whole zero-addressed-tile path at once. Layer `e`, interleaved, rank 1,
dimension `x` with E₀ = 0 and T₀ = 1, one uint8 channel `c` with fill `00`, codec 1, filter 1,
A = S = A_slab = 0, index_encoding 1, entry_count 0, crc_of_crc_array 0, extent slot (0,0), no
sub-records. Inline payload lengths: 2 + 1 + 2 + 2 + 2 + 8 + 8 + 8 + 1 + 2 = 36, plus an 18-byte
dimension entry, plus a 6-byte channel entry, plus 1 + 8 + 4 trailing = **73 bytes**, parsing
exactly with no residue. Record header 24 → record sequence 97 → dir_length 101 at dir_offset 16,
ending at 117; pad to 128; trailer [128,192); F = 192.

Checks walked: [R-GEO-01] (d ≥ 1, T₀ ≥ 1, C ≥ 1) ✓; [R-GEO-02] (E₀ = 0 valid) ✓; G₀ = 0, N = 0,
addressed-tile count 0 = entry_count ✓ [R-CNT-17]; extent_length 0 matches the formula's
"0 when entry_count is 0" ✓; crc_of_crc_array 0 ✓ [R-CNT-23]; A_slab 0 with S 0 ✓; fill length 1 =
uint8 element size ✓; P = 1 and P·Q = 1, both in domain ✓. Conforming, and both verifiers certify.

### 3.3 Codec 4 on a layer that addresses no tile

E₀ = 0, T₀ = 2^63 − 1, one uint8 channel, interleaved, codec 4. Decoded size P·Q = 2^63 − 1 —
exactly at [R-ENC-03]'s ceiling, so in domain — and vastly over `[R-COD-07]`'s 0x7E000000 cap. The
layer addresses no tile, so the cap's quantifier does not bite. §17.2's Note settles it in terms
("a layer that addresses none … satisfies it whatever its tile shape declares, and codec 4 is
conforming there"), and further settles the neighbouring case ("`[R-ENC-04]`'s overflow rule
carries no such quantifier"). Variant with d = 2, T = (2^62, 4) gives P = 2^64 → L2, reject-layer,
even though the layer is empty. Both verdicts are determined; no fork.

### 3.4 A planar slab-declared layer through a growth that reshuffles ordinals

This was my best hope for a fork, because growing an *inner* dimension renumbers spatial ordinals
rather than merely extending them, and §20.3 step 4 permits growth on a layer that stores a tile.

Layer: planar, d = 2, G = (2,2), N = 4, C = 1, slab S = 2, A_slab = 128. Generation 1 stores all
four tiles, length 100 each, at 128, 228 (run [0,2)) and 384, 484 (run [2,4)). Run 0: first offset
128 mod 128 = 0 ✓, packed 128 + 100 = 228 ✓. Run 1: 384 mod 128 = 0 ✓, packed ✓.

Generation 2 grows E₁ so G₁ = 2 → 3, N = 6. Under [R-GEO-06] the old tiles renumber:
(0,0)→0, (0,1)→1, (1,0)→3, (1,1)→4; new ordinals 2 and 5 are sentinels. New runs are [0,2), [2,4),
[4,6). Run [2,4) has one stored tile at 384, 384 mod 128 = 0 ✓. Run [4,6) has one stored tile at
**484**, and 484 mod 128 = 100 ≠ 0 → **L42**.

So the growth breaks the slab invariant for a tile the commit never touched. The document decides
this cleanly and in two places: `[R-SLB-04]`'s trigger list expressly includes "the disk ordinal of
any tile the new state stores", so the writer must "either re-establish the invariants for every
such run — or clear the declaration in the new generation", and §20.3 step 4 restates it. A writer
that neither re-places the tile (by superseding it at an aligned offset) nor clears the declaration
emits a file that a verifier rejects at L42. Both verifiers reject; a reader is not obliged to
check and serves the layer. That is the designed reader/verifier seam, not a fork.

I ran the same construction over a *shortening* of a planar channel list combined with a growth
(C 3→2, N 4→6): retained ordinals renumber, runs repartition, and every invariant is decidable
from the entries alone. §20.3's "A commit MAY make several of these changes at once, an extension
and a shortening of one channel list excepted" licenses the combination. Determined.

### 3.5 A record extent inside the pre-trailer pad

front [0,16); tile [16,116); index [116,140); directory [140,200); pad [200,256); trailer
[256,320); F = 320. Now place a record extent at [210,240). Every reader-tier check passes:
extent_offset 210 ≥ 16, 210 + 30 = 240 ≤ F − 64 = 256, dir bounds fine. `[R-CNT-05]` assigns the
condition to the verifier — F7 — and says so explicitly ("readers check neither, their check being
the dir-bounds rule of `[R-CNT-06]`"). Reader accepts, verifier reports nonconforming: an assigned
detector split, not a divergence between two verifiers.

### 3.6 Structurally-rejected index entries under a slab and under the coverage walk

Layer with entry_count 3, slab S = 3, A_slab = 8. Entry 0 stored at [1000,1100); entry 1 has
offset = S and length = 100 (one half sentinel, the other not) → §15.3 *structural*: reject-tile;
entry 2 stored at [1100,1200). Run continuity closes over entry 1 ("So are the entries §15.3
classifies reject-tile on a *structural* ground: they address no usable extent, and the run's
stored tiles close over them"), so 1100 = 1000 + 100 holds and L41 does not fire; L42 needs
1000 mod 8 = 0 ✓. §9.7's walk gets no claimant from entry 1, and §5.2 says the walk stays complete
and the nominally addressed bytes fall to slack. The file is nonconforming on T7 alone. Every one
of §5.2, §9.7, §15.3, §16.2, L41 and §20.5 states the structural-entry carve-out in the same terms,
including the counter-case ("An entry whose only defect is that its stored bytes fail its crc is
not transparent"). I could not separate two readings here.

### 3.7 The metadata window/size seam

A 10 MiB user-metadata document framed with Single_Segment_Flag: RFC 8878 makes Window_Size the
content size, which §18.2 pins to the decoded length, so Window_Size = 10 MiB > §21.9's 8 MiB
guarantee even though the document is inside the 16 MiB guarantee. §18.2 states exactly this case
and its consequence ("a document larger than that guarantee, framed that way, exceeds a §21.9 row
and so falls outside `[R-CNF-03]`'s acceptance duty, and a writer that needs one frames it with a
Window_Descriptor instead"). Two readers can differ on whether they serve the record; the file's
conformance does not move, and §21.6 registers the decline as a non-violation. A verifier with a
smaller bound reports *cannot establish* rather than *nonconforming* — which is expressly not a
rejection ("a verifier MUST NOT report it as one"). So this is not "one certifies, the other
rejects".

I also checked R4's instance list against the frame constraints §18.2 carries over: magic,
skippable/second frame, dictionary ID, content-checksum flag, trailing bytes, content-size in both
directions — eight conditions across two containers = 16, which is what the cell enumerates; and
the two constraints §18.2 excludes from the register (undisclosed dictionary use, and the
reader-binding buffer-sizing bar) are excluded on the two distinct grounds §21.7 separates. This
passage is tight.

---

## 4. Register completeness audit

§21.1's completeness clause is normative, so I walked every requirement identifier looking for a
detectable file-conformance violation with no row. I went through R-ENC-01…16, R-CNT-01…27,
R-LIF-01…08, R-EXT-01…05, R-GEO-01…06, R-TYP-01…10, R-SER-01…09, R-IDX-01…05, R-SLB-01…05,
R-COD-01…11, R-MTA-01…10, R-RDR-01…04, R-WRT-01…09, R-ERR-01…05, R-SEC/PRV/VEC. Every one either
has rows, states a reader/writer/updater/verifier *conduct* obligation with no file witness, or is
covered by §21.7's unwitnessed / no-condition test with the document saying so.

Two boundaries I checked in particular because they are easy to double-count or to drop:

- `[R-CNT-12]`'s MU = 1 / PE = 0 and reserved-flag conditions: F25/F26 say "non-layer top-level
  record"; L46/L47 say "layer record's or sub-record's". A *top-level layer record* therefore
  lands in L46/L47 at layer scope, which is what §7.2's governing-scope rule ("the layer for a
  layer record") requires. No gap and no overlap.
- `[R-CNT-22]`'s stored-flag mismatch: F28 covers the registered non-layer top-level type (0x0002
  only); L49 covers the layer record and a registered sub-record. Again exhaustive and disjoint.

I found no missing row.

---

## 5. Findings

### adversary-01 — the closed verb list and the clause it delegates to use different words for the same member (§20.3 step 4)

**AMBIGUITY.** §20.3 step 4's permitted-change list ends:

> and a slab or alignment declaration MAY be declared, changed, re-established or cleared as this
> step provides below.

and the clause below, in the same step, reads:

> a slab declaration declared, changed or kept has its invariants re-established over every run the
> new state keeps, or is cleared (`[R-SLB-04]`)

The member names four verbs; the clause it expressly delegates to names *declared, changed, kept*
and *cleared*. "Re-established" appears nowhere in the delegation, and "kept" appears nowhere in
the member. Everywhere else this document uses "re-establish" it is of *invariants*, never of a
declaration: `[R-SLB-04]` ("MUST either re-establish the invariants for every such run"), and the
delegating clause itself ("has its invariants re-established"). Five occurrences of the stem in the
whole document, and the member's is the only one whose object is a declaration.

Permitted readings of "a declaration MAY be re-established":

1. *Some → same value.* The declaration is carried forward unchanged. But this is the step's own
   baseline — the paragraph opens "A layer that stores a tile **in the generation this commit
   supersedes** keeps its declarations, with these exceptions and no other" — so a verb naming
   "keeping" is not an exception to anything, and the member is then redundant.
2. *Some → same value, over moved geometry.* The declaration is kept while the commit moves the
   run partition or a stored tile's disk ordinal, and the writer re-lays the tiles so the
   invariants hold again. This is the transition §3.4's construction exercises, it is the case
   `[R-SLB-04]` was written for, and it is the only reading on which the member does work the
   baseline does not already do.

I pick reading 2, because it is the only one that makes the member non-redundant and because the
delegation's "declared, changed or **kept** has its invariants re-established" reads as the
member's expansion. But nothing in the text says so, and an implementer who picks reading 1 gets a
list whose third member is noise while the transition reading 2 names — keep the declaration,
re-place the tiles — is named by no verb at all.

I could not turn this into a fork over bytes. `[R-SLB-03]` states the run invariants
unconditionally over the live state, and `[R-SLB-04]` states the writer's obligation with its own
trigger list, so a file is judged the same way under either reading: a stale declaration is L41 or
L42 to any verifier. The defect is in the exception list's own wording, not in what any file is
worth.

### adversary-02 — "the two lists reach every declaration field of §7.4" over-claims, and the "both sides" example is on one side (§20.3 step 4)

**OBSERVATION.** The step says:

> Between them the two lists reach every declaration field of §7.4, and where a field is on both
> sides — a dimension extent, a planar layer's channel list, an interleaved layer's channel list —
> the permitted side states the whole of what a commit MAY do to it

Two problems, both mechanical.

*The "both sides" list.* The fixed list is introduced as "**Every other declaration** is fixed for
as long as the layer stores a tile", i.e. it is by construction the complement of the permitted
list, and it then enumerates: layout, linearization, index encoding, codec, filter, rank, dimension
order, every tile extent, every channel's type and fill, an interleaved layer's channel list (its
names aside), and the position of every planar channel the new state keeps. A **dimension extent**
appears nowhere in it. It appears only on the permitted side ("an extent MAY grow, and MUST NOT
shrink"). The other two examples do sit on both sides — a planar channel list is permitted
(extend/shorten at the end) and fixed (the position of every retained channel), an interleaved
channel list is permitted for names and fixed for everything else — so the pattern the sentence
generalises is real for two of its three members and not for the third. The reading that saves it
is "a field on which both a permission and a prohibition bear", but under that reading the fixed
list is not the second "side" and the sentence's own vocabulary breaks.

*The reach claim.* Four §7.4 fields are reached by neither list but by the clause that follows:
"entry_count and crc_of_crc_array follow the commit, the record's extent slot with them (§7.2),
and a layer's sub-records are §20.4's subject whether or not the layer stores a tile." So "between
them the two lists reach every declaration field of §7.4" is true only if "declaration field"
silently excludes entry_count, crc_of_crc_array, the extent slot and the sub-record sequence — a
narrowing the document nowhere makes. §7.4's table presents all of them as rows of the layer
record's inline payload alongside codec and fill.

Not byte-level: this is a claim *about* the two lists, and the lists themselves decide every field
one way or the other. But a reader auditing the partition — which is the only way to be sure a
commit's permitted set is closed — is told to check a property that two of the named cases do not
have.

### adversary-03 — "keeps" carries two senses inside one numbered step, and the slab clause inherits the narrower one (§20.3 step 4)

**AMBIGUITY.** Three uses of "the new state keeps" in step 4:

> the position of every planar channel the new state keeps

> an aligned layer's stored tiles — every one the new state keeps, not only those this commit
> adds — satisfy its invariant or the declaration is cleared

> a slab declaration declared, changed or kept has its invariants re-established over every run the
> new state keeps, or is cleared

In the first, "keeps" must mean *retains from the superseded generation*: it is contrasted with the
channels a shortening removes, and an appended channel has no prior position to fix. In the second,
"keeps" must mean *stores in the new state, retained and added alike* — the appositive "not only
those this commit adds" only makes sense if added tiles are inside the range. The two senses are
mutually exclusive and sit four lines apart.

The third use is the one that matters, and it is unqualified. Under the first sense, "every run the
new state keeps" is the runs carried over, and the runs a growth *adds* — which a growth reaching a
new grid count always adds — owe nothing. Under the second sense it is every run of the new state.
`[R-SLB-03]` is unconditional ("When declared, for every run: …"), so the second sense is the one
that agrees with the governing rule; I pick it. But the alignment half of the very same sentence
was evidently written to close exactly this quantifier question ("every one the new state keeps,
**not only those this commit adds**") and the slab half was not given the same clause, so the two
halves of one sentence now read at different widths.

Not byte-level. `[R-SLB-03]` governs, and a file with an unpacked or misaligned new run is L41 or
L42 to any verifier under either reading of §20.3. The cost is to the writer, who is told less than
the rule requires in the place the document sends writers to read.

### adversary-04 — §4.7's structural test admits the verifier and its descriptive restatement does not

**OBSERVATION.** §4.7:

> A field is **structural** if its value determines anything a conforming reader or verifier does
> with the bytes it reads — where a byte lies, how it decodes, what a decoded value is, or whether
> the file, layer or tile is accepted at all … It is **descriptive** if it determines none of
> those: its value determines nothing a conforming reader does, and a reader MUST NOT alter
> decoding based on it

The structural half ranges over "a conforming reader **or verifier**". The descriptive half, one
clause later, restates the same test as "nothing a conforming **reader** does". The two are not
the same test, and the difference is populated: the stored MU and PE bits of a record of a
registered type determine nothing a conforming reader does — §7.3 says "A reader MUST apply a known
type's specified semantics regardless of its stored MU and PE bits" — while determining what a
verifier does, F28 and L49 being validity errors. Same for a record's reserved flag bits 2–15,
which "readers MUST ignore" and F26/L47 make verifier-detected.

The governing phrase is "it determines none of **those**", whose antecedent is the four-alternative
gloss, one of which is "whether the file, layer or tile is accepted at all" — and a verifier's
certification is acceptance. So the definition survives, and the closing sentence ("In format major
1 `version_minor` is the only descriptive field") settles every actual field. But the restatement,
read on its own, classifies a verifier-only field as descriptive, which would then attach to it a
consequence the document means for version_minor alone ("each descriptive field's definition states
what a reader does when the field contradicts the data it describes"). Not byte-level: no field is
actually reclassified, because the enumeration is closed by name.

### adversary-05 — the "no check any actor owes able to see it" enumeration omits a decoded-size row that a re-tiled codec-4 layer exhibits (§20.3 step 4)

**OBSERVATION.** Justifying the bar on changing a fixed declaration:

> Under new ones the same bytes would denote values, coordinates or padding the writer did not
> store, with every checksum in §8 certifying the result and, but for a decoded size, a padding
> position or pad bit, or a boolean byte the register witnesses (T3, T14, T21, T22, T4, T5, T2) and
> a decode that fails outright under a changed codec or filter (T24, T25), no check any actor owes
> able to see it (§21.7).

"a decoded size … the register witnesses" is cited to T3, T14, T21, T22 — all tile-scope. The
register carries another decoded-size row: **L44**, "Codec 4 (lz4) declared on a layer any of whose
addressed tiles' decoded size exceeds 0x7E000000 bytes", detector reader, detected at layer access,
"checkable from declarations alone".

Concretely: an interleaved layer with one uint8 channel and tile extents (10000, 10000) has decoded
size 10^8, under `[R-COD-07]`'s cap of 0x7E000000 = 2,113,929,216. A commit that re-tiles it to
(50000, 50000) — a change to a tile extent, exactly what the bar forbids — gives 2.5 × 10^9, over
the cap, and the file exhibits L44 even after the writer has consistently updated entry_count,
extent_length and crc_of_crc_array. So there is a check an actor owes that sees a violating commit's
output, and the sentence says there is not. (L2's `[R-ENC-04]` ceiling does the same for a re-tiling
to T = (2^40, 2^40).)

Thin, and I say so: L44 sees the *new declarations* being out of bounds rather than the tile
denoting wrongly, which is arguably a different thing from what the sentence claims. But the
sentence's own grouping is "a decoded size … the register witnesses", and L44 is a decoded-size row
the register witnesses. Not byte-level either way — the file's verdict is L44's, identically under
both readings.

### adversary-06 — Appendix F carries no reference for the transport vocabulary a MUST-level rule uses

**OBSERVATION.** `[R-CNT-10]` (§6.4) is normative and states:

> A remote reader MUST handle a 200 response to a range request (abort or accept the full body
> deliberately — never treat the body prefix as the requested range) and SHOULD fall back to a size
> probe plus an absolute range on transports without suffix-range support

"a 200 response", "range request", "suffix-range support" and (in §6.4's opening) "a suffix range,
whose response also carries the transport-authoritative file size" are HTTP terms of art. Appendix
F — titled "Normative references", and, unlike Appendices A–E and G–H, *not* marked non-normative,
so normative under `[R-CNF-01]` — lists BCP 14, RFC 3720, IEEE 754, RFC 1950, RFC 1951, RFC 1952,
RFC 8878, LZ4 Block, RFC 8259, RFC 3339 and Unicode, and no HTTP specification. Every other
external vocabulary the document imposes a MUST on is pinned there, down to the lz4 block format's
release tag ("as published with lz4 release v1.9.4").

An implementer taking the document alone must supply from outside it what a 200 means in this
context, what a suffix range is, and what "transport-authoritative" length a range response
carries. Not byte-level: the rule constrains a reader's transport conduct and no on-disk byte, and
the substantive requirement ("never treat the body prefix as the requested range") is stated in
plain terms in the parenthesis.

---

## 6. Attacks I ran that the document forecloses

Recorded because an empty lane has to show what it did.

- **§21.7 category of §20.3's bar.** The bar says of itself: "no register row records the violation
  itself, the register enumerating file-conformance violations (§21.1) and **the bar stating no
  condition a file can exhibit** (§21.7, `[R-ERR-01]`, `[R-CNF-02]`)". I suspected misclassification:
  §21.7's "no condition a file can exhibit" category names only `[R-ENC-06]`'s field widths, and a
  file produced by a violating commit *does* physically carry the superseded generation's directory
  — §23.2 says the history is "recoverable by probing backward for the superseded trailers that
  committed-prefix immutability keeps in place", and Appendix G item 4 says the probe is what
  refutes single-generation reproducibility. So the byte pattern exists, which looked like
  *unwitnessed* rather than *no condition*. What closes it: §5.2's "Slack has no internal structure
  this specification defines, its content is unconstrained, and no conformance requirement applies
  to it". A creator may emit that byte pattern in slack without any commit having violated the bar,
  so the two files are byte-identical and the condition is not a predicate on bytes at all. The
  self-classification stands.
- **A fourth conduct case for `[R-CNF-02]`.** §2.3 closes a list: "§6.3's flags rules against a set
  ignore-lane bit …, §6.2's pre-trailer gap longer than `[R-LIF-02]` step 5's pad, and §20.3 step
  4's bar … **are the cases this text states**". I searched `flat.txt` for every phrasing that could
  mark a fourth ("not a file-conformance violation" 1, "no file is nonconforming" 1, "the file is
  conforming" 3, "stays conforming" 2, "remains conforming" 2, "conduct" 7) and read each hit.
  §10.3's bar on publishing experimental values and §9.2's barriers are both already inside
  `[R-CNF-02]`'s *first* category, which the sentence names separately ("where a value is published,
  which registry version a writer targets (§10.3, §18.3), or the barriers a commit performs (§9.2)").
  `[R-WRT-05]`'s byte-identical re-emission and `[R-WRT-06]`'s fresh file_id are unwitnessed rather
  than expressly non-violations, and §20.4's Rationale says so of the first in terms. I found no
  fourth case.
- **Instance and row arithmetic.** 35/49/26/10 rows, 56/116/55/50 instances, 120 and 277 totals —
  all six figures reproduce. Every CRC constant reproduces. Nothing to report.
- **Verifier-row coverage of Appendix H.** All twenty verifier-detected rows are named in Appendix
  H's verifier checklist. Nothing to report.
- **§21.1's strict-specialization pairs.** F21⊂F22 (a (0,0) slot has extent_length 0 < 5), L10⊂L11,
  F35⊂F36, L24⊂L25, F1's front-block instance ⊂ F6, F1's magic instance ⊂ F8. Each holds under the
  stated test, and the list is expressly not offered as closed.
- **Zero/one/max boundaries.** entry_count 0 (slot (0,0), crc_of_crc_array 0, no region, nothing
  fetched); entry_count at 2^63 − 1 (L2 via the region-length formula); P = 1 and decoded size 1
  under all three layout formulas; ⌈P/8⌉ with P = 1; a full final segment of exactly 2^16 sentinels
  ("full … final or not"); A_slab = 1 (contiguity-only); S > N (one short run); dir_length exactly 4
  at dir_offset 60 on a 128-byte file (legal, the intervening bytes slack). Every one is decided.
- **The decoded-size overflow set.** I derived which declaration-derived quantities can independently
  exceed 2^63 − 1 and compared against L2's nine instances. ⌈P/8⌉, Q, Fᶜ, k·Bᶜ, (k div C)·Q + Fᶜ,
  20·k and s·2^16 are each dominated by a listed quantity or by P itself, so their absence from L2 is
  correct, and the two the cell explicitly marks as dominated (the max disk ordinal, V = P·C) are the
  two that need saying.
- **The experimental sub-record with MU = 1.** A conforming file (`[R-CNF-02]`, §21.6) from which one
  reader serves a layer and another must refuse it (`[R-CNT-18]`). Two conforming readers, different
  returned data, same file. Closed by §21.6's closing paragraph: "the same type as a layer sub-record
  is reject-layer and never a ground to refuse the file", and the outcome "records a reader's
  capability, not a defect in the bytes". No verdict on the bytes moves.
- **The verifier size-bound seam.** Two verifiers with different metadata-document bounds return
  *conforming* and *cannot establish* on the same file. §18.2 forecloses it as a fork: "the decline
  is not a finding that the file is nonconforming and a verifier MUST NOT report it as one".
  *Cannot establish* is not rejection.
- **§5.2's slack-total exemption.** "Where §6.2's ordered validation rejects the file before a live
  trailer is established there is no F and no live state to walk, so the total is not owed at all".
  I looked for a rejection path that bypasses §6.2's ordered validation and would therefore fall
  outside the exemption while still reaching no live state — F5 (`[R-CNT-27]`, decided at §19.1 step
  1 from F alone) and F6/F1 (the front block, checked "before other processing") are both such
  paths. Closed by `[R-CNT-21]`'s own antecedent: the duty is on "a verifier that **reaches a live
  state**", which neither path does, so the §6.2 sentence is an elaboration and not the only
  exemption.
- **§11.1's growth taxonomy.** "A growth that changes no grid count … moves no entry and adds none";
  "so does one that raises a grid count while another stays 0, the product holding at 0"; "Any other
  growth changes the index content — entry_count and extent_length with it". I checked the partition:
  a growth either leaves every Gᵢ unchanged (N fixed), or raises some Gᵢ while another stays 0
  (N = 0 before and after), or raises some Gᵢ with no remaining zero (N strictly increases, and
  entry_count × 20 + ⌈entry_count/2^16⌉ × 4 is strictly monotone with it). No fourth case, and the
  monotonicity claim holds.

## 7. Verdict

I could not construct a file two conforming verifiers judge differently, and I could not find a
byte-level defect. The six findings above are all reading defects in text the document itself
decides elsewhere — five of the six in §20.3 step 4 and §4.7, which is where the round's repairs
land, and one in Appendix F. My confidence that the changed surface is *byte-level* clean is
medium, not high: the passages are dense, several sentences are third or fourth repairs, and the
one place I most expected a survivor — the four-verb closed list and the clause it delegates to —
does have a lexical seam (adversary-01) that I could not turn into a file. What I can say is what
I did that would have found one: I derived every stated number, walked every requirement identifier
against the register, enumerated the verifier rows against Appendix H, and built the slab-growth
case that reshuffles disk ordinals, which is the sharpest interaction the permitted-change list
admits.
