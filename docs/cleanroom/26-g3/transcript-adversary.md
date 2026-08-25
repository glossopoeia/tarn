# Cleanroom round 26 — Adversary transcript

> *Editorial substitution for the repository's vocabulary gate: an ordinary-English
> use of a gate word has been replaced with an exact synonym. The substitution is
> recorded here and changes no finding, quotation or verdict.*

## 0. Access and disclosure

I read exactly one file: `/Users/robertkleffner/Documents/GitHub/tarn/spec/tarn.md`
(4,484 lines by `wc -l`; the brief says 4,485 — off-by-one on a trailing
newline, not a discrepancy worth anything). I read it whole, in eight
`sed -n` slices, plus targeted `grep`/`sed` re-reads of eleven passages.

I opened no other file. I ran no `git` command. I listed no directory
other than `ls -la` on the single spec path itself, to confirm the brief's
path was where the brief said it was — it was. I ran three Python scripts
of my own authoring, in the scratchpad, which read no project file.

**Context I did not ask for, and disclose.** Before I began, my runtime
placed in my context: (a) a project instruction file pointer
(`CLAUDE.md` → `AGENTS.md`), (b) an index of the maintainer's persistent
memory notes with one-line descriptions, and (c) a `gitStatus` block
carrying the five most recent commit subject lines. (c) is the material
breach: those subject lines name the round before this one, and two
of them describe, in outline, what two of the seven changed passages were
changed *to*. I read them before I read the spec and cannot unsee them.

I have not used them to settle anything. Concretely: I derived my §11.1
finding by censusing the document's own thirteen uses of "last" and
constructing two layers whose entry_count behaves oppositely under the two
readings — not from the commit line — and I checked afterwards that the
commit line does not in fact say which reading is right, only that the
passage was rewritten. My §17.2 finding is in a passage none of those
lines mentions. I flag the exposure because a disclosed breach is usable
and a silent one poisons the round.

## 1. What I did first: verify that the document's own numbers are real

Before attacking semantics I checked every constant and every worked
arithmetic example the document commits to, because a document whose
worked examples are wrong is a document whose prose I should trust less.

CRC-32C implemented from §4.5's parameters (reflected, poly 0x1EDC6F41 →
reflected 0x82F63B78, init 0xFFFFFFFF, final XOR 0xFFFFFFFF):

| Claim | Section | Computed | Verdict |
|---|---|---|---|
| CRC32C("123456789") = 0xE3069283 | §4.5 | 0xE3069283 | ok |
| CRC32C(zero bytes) = 0x00000000 | §4.5 | 0x00000000 | ok |
| 80 bytes = 4 sentinels → 0x80A34955 | §7.4 example | 0x80A34955 | ok |
| crc_of_crc_array over that 4-byte array = 0xC4EE982E | §7.4 example | 0xC4EE982E | ok |
| full 2^16-sentinel segment → 0xEECB3BB2 | §15.4, App. B | 0xEECB3BB2 | ok |
| Appendix A trailer CRC = 0xE00938D2 over [0,60) | App. A | 0xE00938D2 | ok |

Non-CRC arithmetic I re-derived by hand and confirmed: §7.4's 81-byte
layer payload (4 + 34 + 18 + 12 + 13 = 81, and every listed field offset
lands); §11.2's G=(4,8), N=32, P=65536, and ⌈1000/256⌉=4; §11.4's
s=1·8+2=10, in-tile ordinal 44·256+188=11,452, planar disk ordinal
2·32+10=74; §15.4's 1,000,000-entry layer (16 segments, last covers
16,960, region 20,000,064 bytes, entry 999,999 at segment-relative byte
339,180, segment 15 at [19,660,800, 20,000,000), array at
[20,000,000, 20,000,064), full segment = 1.25 MiB); §15.4's second
example (entry 74 at region bytes [1480,1500); channel-3 entries 96–127);
§14.2's three worked layouts (Q=3/size 18/bytes [15,18); planar b 12 bytes
at 10–11; Q=5/size 30/bytes [25,30)); §14.3's `55 01` and `55 FD`;
§14.5's 2×2 grid with 15 padding positions and 32 bytes of `CD AB`;
§17.3's byte-shuffle of three float32s, which I recomputed offset by
offset and which matches `00 00 00 00 00 00 80 00 40 3F 40 40`; §16.2's
four runs and ordinals 8–23; §21.9's note arithmetic (2^32/2^16·4 = 256
KiB, 2^36 → 4 MiB, 65,536 layers ≈ 12.5 MiB).

**Everything checks.** I found no arithmetic error anywhere in the
document. That is worth stating because it means the defects, if any, are
in quantifiers and words, not in numbers.

## 2. Mechanical audit of the register's closed counts (brief hint 5)

§21.8 asserts "121 conditions over 277 instances". §21.1 makes the count
mechanical: instances within a cell are semicolon-separated, and a cell
reading `—` is one instance. I extracted the four tables with a script and
counted:

- §21.2: 36 rows, 58 instances (§21.2 claims "36 conditions") — ok
- §21.3: 49 rows, 116 instances (claims 49) — ok
- §21.4: 26 rows, 55 instances (claims 26) — ok
- §21.5: 10 rows, 48 instances (claims 10) — ok
- Total: 121 rows, 277 instances — **exactly as claimed**

I then audited individual cells against §21.1's own individuation rules
rather than against the cell text, which is the failure mode the brief
warns about:

- **T21** ("window size *larger than* decoded size"): one-directional
  comparison → 1 direction; layout-varying derived quantity → 3 layout
  formulas → 3. Cell says 3. ok.
- **T22** (content-size "does not equal"): two directions × 3 layouts = 6.
  Cell says 6. ok.
- **T3**, **T14**: same shape, 6 each. ok.
- **L21** (entry_count ≠ addressed-tile count): 2 layouts × 2 directions
  = 4. ok.
- **L44** (lz4 "exceeds"): 1 direction × 3 layouts = 3. ok.
- **L30** (fill prefix "differs"): 2 directions, no layout axis = 2. ok.
- **F26 / L47** (reserved flag bits): "any bit set" is a single predicate
  over several fields, so the bits are *not* instances; only the container
  axis is enumerated — F26 gets 1, L47 gets 2 (layer record, sub-record).
  Correct per §21.1's "one *distinguishable* file" rule.
- **R4** (encoding-2 frame constraints): I derived the constraint list
  independently from §18.2 — magic; skippable frame; second frame; nonzero
  dictionary ID; content-checksum flag; bytes after the frame; content-size
  larger; content-size smaller = 8 alternatives, minus the two §18.2 says
  carry no witness (undisclosed dictionary use, and the reader-binding
  buffer-sizing bar), × 2 containers = 16. Cell says 16. ok.

I then tested two lists for *completeness* by deriving the members from
the rule rather than reading the cell:

- **L1** ("a u64 offset, length, extent, or count field of a layer
  record"). The layer record's u64 fields are: extent_offset,
  extent_length (record and sub-record), Eᵢ, Tᵢ, entry_count, S, **A**,
  **A_slab**. L1 lists eight and omits A and A_slab. That is correct, not
  short: [R-ENC-03]'s domain runs over "every offset, length, extent, and
  count", and an alignment modulus is none of those; §21.9 lists A and
  A_slab separately among the *hard* limits, capped at 2^62 by L39 and
  L29 respectively, which subsume any 2^63-crossing value. No gap.
- **L2** ("a declaration-derived sum or product"). I enumerated every
  product the document defines over layer declarations and checked each
  against the cell's nine. The interesting one is **Gᵢ·Tᵢ**, which §11.3
  defines ("Where Gᵢ · Tᵢ > Eᵢ …") and L2 does not list. It cannot be a
  gap: N·P = ∏(Gⱼ·Tⱼ) and every factor is ≥ 1, so N·P ≥ Gᵢ·Tᵢ for every
  i — any file that overflows Gᵢ·Tᵢ overflows N·P, and the two are not
  distinguishable files at d = 1. Also checked and correctly subsumed:
  Q and Fᶜ (bounded by 65535·8), V = P·C (dominated by P·Q, since Q ≥ C),
  the max disk ordinal (dominated by C·N, as the cell itself says),
  ⌈P/8⌉ (< P), 20·k (< entry_count·20), and slab run starts (< C·N).
  No gap.
- **F2**: file-scope u64s are dir_offset, dir_length,
  committed_file_length, generation, file_id, and a non-layer top-level
  record's extent slot. F2 lists six and omits file_id — correctly, since
  file_id is an identifier, not an offset/length/count, and §6.2
  constrains it only by ≠ 0. No gap.
- **F7 / F33**: I derived the claimant classes from §5.2 (front block;
  stored-tile extent; record extent; directory; trailer) and confirmed
  both instance lists are exactly the reachable members, with front block
  and trailer correctly excluded by F33's own bounds-row argument.

I could not break the register's arithmetic or its completeness. This is
the fifth thing in a row I attacked and failed to break, and I record it
because "empty is a real result only if the attacks were good."

## 3. The §21.2 preamble's four-row exception (hint 5 again, and hint 4)

§21.2 claims exactly four rows reach a file declaring a foreign format
major: F8, F1's trailer-magic instance, F14, and F6 with F1's front-block
instance. I tested this against §6.2's stated validation order and
[R-CNT-24]'s cross-major invariants.

[R-CNT-24] fixes permanently: trailer magic at F−64, version_major and
version_minor at F−56, a CRC at F−4 over [F−64, F−4), and the front block.
§6.2 orders magic → CRC → version gate → everything else, and [R-CNT-04]
puts the front-block equality check "before other processing" for a reader
holding those bytes.

I tried to find a fifth row. Candidates and why each fails:

- **F13** (committed_file_length not a multiple of 64). Tempting, because
  64-alignment sounds structural. But committed_file_length sits at
  trailer offset 40, inside the 48 bytes [R-CNT-24] lets a future major
  redefine, and §6.2 puts it after the gate. Does not reach. Correct.
- **F5** (file under 128 bytes). Constructed: a 64-byte file whose whole
  content is a valid-magic, valid-CRC trailer declaring version_major = 2.
  §6.2's order refuses it on capability grounds before F5's
  committed_file_length instance runs, and the physical-size instance is
  §19.1 step 1's, which is not a §6.2 gate. Does not reach. Correct.
  (A file under 64 bytes declares no major at all, so the preamble's
  premise never applies to it — the document says as much of F18.)
- **F17** (length cross-check). §6.2 puts it after the gate. Does not
  reach. Correct.

I also checked the verifier consequence: a verifier holding [0,16)
resident on a major-2 file whose front block is wrong establishes F6, and
§2.3's "an established violation takes priority" makes the verdict
*nonconforming* rather than *cannot establish* — which is exactly what the
preamble's inclusion of F6 implies. The two texts agree. No finding.

## 4. Attack surface: the seam between a rule and the sentinel

This is where I found the one thing I believe forks bytes.

### 4.1 The construction

Layer L: rank 1, dimension `x`, E₀ = 100, T₀ = 32 → G₀ = 4, N = 4,
interleaved, C = 1, one uint8 channel `v` with fill `0x00`, linearization
1, **codec 1 (none)**, filter 1 (none), no alignment, no slab,
index_encoding 1, entry_count = 4. Decoded size = P·Q = 32·1 = 32 bytes.

Index region = 4 × 20 + ⌈4/2^16⌉ × 4 = 84 bytes. Entries 0, 1, 2 are
genuine stored tiles of length 32 each; **entry 3 is the sentinel**,
`FF ×16 00 ×4`. Everything else in the file is well formed: front block,
one layer record in the directory, directory CRC correct, trailer correct,
no overlaps, index region and the three payloads disjoint and inside
[16, F−64), segment CRC and crc_of_crc_array correct.

This is the most ordinary sparse file the format admits: three tiles
written, one absent, no compression. It is the file the §13 "Note — sparse
writing" describes a writer producing.

### 4.2 The two verdicts

**Verifier A certifies it.** Its argument: entry 3 is a valid sentinel,
which §15.3's first row obliges it to classify as "valid sentinel — reads
as fill"; §19.4 step 4 short-circuits steps 5 and 6 for that entry;
§21.6 records "an index entry is the sentinel" as a defined
non-violation; and T14, the register row for [R-COD-04], states the
condition as "a **non-sentinel** index entry's length differs from the
tile's decoded size", which entry 3 is not.

**Verifier B reports nonconforming, at tile scope, for tile 3.** Its
argument is [R-COD-04] read as written:

> "**Codec 1 — none.** The stored bytes are the filtered image
> verbatim. The index entry's length therefore MUST equal the tile's
> decoded size (§14.2, §14.3); a reader MUST treat a mismatch as a
> validity error at tile scope — checkable from the entry and the
> layer record alone, before any payload fetch. `[R-COD-04]`"

Entry 3's length field holds 2^64 − 1. The tile's decoded size is 32.
2^64 − 1 ≠ 32. The rule says a reader MUST treat a mismatch as a validity
error at tile scope, and it carries **no non-sentinel qualifier**, unlike
every one of §15.3's six structural rows and unlike T1, T8, T9, T10, T11,
T12 and T14, all of which spell "(non-sentinel)" out. B further cites
§21.1 against A's best card:

> "each row *restates* its governing rule, and where a row and the rule
> it cites diverge, **the rule governs**."

So T14's qualifier, on the document's own precedence rule, does not bind;
[R-COD-04] does. And B cites §15.2, which is the *only* place the document
exempts sentinels from a rule that reads their fields, and which names a
closed pair:

> "Sentinel entries are a reserved pattern, not offsets or lengths:
> `[R-ENC-03]`'s value-domain rule and `[R-ENC-04]`'s sum rule apply to
> the fields of non-sentinel entries only."

[R-COD-04] is not in that pair. B's position is that the document knows how
to exempt a rule from sentinel entries, has done so exactly twice by name,
and did not do so here.

### 4.3 Where the bytes diverge

The reader-side consequence is not a diagnostic difference. Under B,
reading tile 3 of layer L "reports failure" ([R-CNF-09]: a rejected tile's
read MUST NOT silently return fill). Under A, reading tile 3 returns 32
samples of `0x00`. Same 20 bytes on disk; opposite observable behavior for
a read of the same coordinate; opposite conformance verdicts on the same
file. That is the byte-level test answered yes on both of its clauses.

The blast radius is not exotic. Codec 1 with a sparse index is the
combination §13's sparse-writing note, Appendix G item 6 (which *requires*
"the sentinel for every all-fill tile"), and Appendix G item 1 (which
recommends codec 1 as "reproducible by anyone") all push a writer toward.
Under B's reading, the reproducible-writer profile's item 6 and codec 1
cannot be combined at all: item 6 mandates sentinels, and B rejects every
sentinel a codec-1 layer carries.

### 4.4 Honest weighing

A's counter-text is real and I want it recorded fairly:

1. "The stored bytes are the filtered image verbatim. The index entry's
   length **therefore** MUST equal…" — the "therefore" chains from a
   premise about *stored bytes*, and §3.1 makes "stored" mean "entry is
   not the sentinel", so an unstored tile has no stored bytes for the
   premise to be about. This is the strongest defence and I think it is
   what the author meant.
2. §15.3's table is a MUST-classify table, and its first row gives the
   sentinel a positive verdict, not merely an absence of one.
3. §19.4 step 4's short-circuit.
4. T14 and §21.6, both of which get it right.

What keeps this a finding rather than a non-defect is that A's argument is
entirely *inferential* — it turns on reading a premise clause as scoping a
MUST that does not repeat the scope — while B's is textual, and the
document's own precedence rule (§21.1) hands B the tiebreak against the one
place that states the exemption plainly. The brief's closing question
applies squarely: "for any rule you can only defend by reasoning you supply
yourself, ask whether the document supplies it." Here the document supplies
the exemption for [R-ENC-03] and [R-ENC-04] by name and does not supply it
for [R-COD-04].

The repair is two words in §17.2. I record that only to say the cost of
being wrong about this is asymmetric.

Plausibility that a real implementation lands on B: **moderate**, and the
rule's own last clause is what raises it. "checkable from the entry and
the layer record alone, before any payload fetch" actively invites an
implementer to lift this check out of the per-tile read path and run it as
a cheap sweep over the whole entry array at layer-validation time — which
is precisely the loop in which sentinels are not yet classified. An
implementer who instead follows §19.4's step order classifies first and
never reaches the check for a sentinel. Both are natural code shapes.

I also checked whether §19.4 itself decides it: it does not. §19.4's eight
steps cite [R-IDX-03], [R-CNT-20], [R-COD-08], [R-SER-07], [R-GEO-04],
[R-MDL-02], [R-TYP-04], [R-TYP-06], [R-TYP-08], [R-IDX-04], [R-CNF-09] and
[R-GEO-06] — **[R-COD-04] appears nowhere in the tile-read algorithm.**
T14 places its detection at "tile use", so it is due there, but §19.4 never
says where in the eight steps it happens, and that silence is what leaves
room for the sweep.

## 5. Attack surface: the word "last" in §11.1 (brief hint 7)

§11.1's Rationale closes:

> "Growth that changes entry_count changes extent_length with it
> (`[R-CNT-17]`), so the layer's whole tile-index region is re-emitted
> and disk ordinals renumber wherever `[R-GEO-06]` moves them (§20.3,
> `[R-WRT-04]`) — the growth that raises a zero-extent layer's **last**
> zero grid count included."

I did not settle "last" by what sounded natural. I censused all thirteen
occurrences in the document:

| line | phrase | sense |
|---|---|---|
| 163, 194 | "on that last ground", "the last where…" | last of an enumeration just given |
| 504 | "the last two are separate namespaces" | last two of a list |
| 566, 614 | "trailer last, in that order", "the last ones in the file" | positional in file order |
| 1249, 1294 | "the last committed state" | most recent |
| **1502** | **"a zero-extent layer's last zero grid count"** | **at issue** |
| 1527 | "the last row of tiles is padded" | positional, high edge |
| 1553 | "**the last-declared dimension** varies fastest" | declaration order |
| 1900 | "beyond the last value" | positional in a sequence |
| 2096 | "the last covering 16,960 entries" | positional, final segment |
| 2202 | "a band along the **last-declared dimension**" | declaration order |
| 3468 | "after the last complete record" | positional |
| 3719, 3757 | "the last two", "the last three rows" | positional in a list |
| 4299 | "the eight a named hash emits last" | positional in output order |

Every single other use is **positional within an ordering the document has
already fixed**, and the two uses that index a dimension — §11.4 and
§16.2's note — both mean *last-declared*. The house sense for a
dimension-indexed quantity is unambiguous: last = last-declared.

Now the two readings and their opposite truth values, worked as files.

**Reading (ii), the house sense — "the last-declared dimension whose grid
count is zero."** Construct layer M: rank 2, extents (0, 0), tile extents
(4, 4). G = (0, 0), N = ∏Gᵢ = 0, entry_count = 0, extent slot (0,0),
crc_of_crc_array = 0. A commit grows E₁ (the last-declared dimension, and
the last-declared zero grid count) from 0 to 8. Now G = (0, 2). N = 0·2 =
0 still. entry_count is **unchanged at 0**. extent_length is unchanged at 0.
No index region is emitted, no ordinal renumbers, and the commit touches
the directory alone. So under reading (ii) the sentence asserts that a
growth which does **not** change entry_count is "included" among growths
that **do** — the sentence is false.

**Reading (i) — "the zero grid count that is the last one remaining,"**
i.e. the growth after which no grid count is zero. Construct layer M′:
rank 2, extents (0, 5), tile extents (4, 4). G = (0, 2), N = 0. Grow E₀
from 0 to 4: G = (1, 2), N = 2, entry_count 0 → 2 (interleaved). extent_length
0 → 2·20 + 4 = 44, the region is emitted for the first time, ordinals
appear. entry_count changed, so the growth is indeed included — the
sentence is true, and it is a useful clarification, since this is the
growth that adds tiles without raising any *already-nonzero* grid count.

So the sentence's truth value turns entirely on which sense of "last" the
reader supplies, and the sense the document's own thirteen-use practice
teaches is the one under which it is false.

I am confident (i) is intended: it is what makes the sentence say something,
it parallels the em-dash clause two sentences earlier (which likewise names
the non-obvious member of *its* class rather than defining the class), and
the bolding of **last** signals that a specific one of several zeros is
meant. But "the last zero grid count" of a rank-3 layer with two zero
extents is not a phrase that picks out a unique dimension under reading (i)
either — if two grid counts are zero, neither is "the last remaining" until
one has already been raised, so reading (i) is really "the growth that
raises the final zero grid count," which the words do not say.

**Grading.** Not byte-level. [R-CNF-01] puts Rationale outside normative
text, and every byte-relevant consequence is fixed elsewhere and correctly:
[R-GEO-03] fixes N = ∏Gᵢ; [R-CNT-17] fixes extent_length from entry_count;
[R-WRT-04] fixes when a region is re-emitted; [R-GEO-06] fixes ordinals. An
implementer who computes rather than reads gets it right whichever way they
read the word. What it costs is that this is the passage §11.1 exists to
explain, aimed at exactly the reader who is trying to understand
schema-first growth without deriving it, and half of them will read a false
statement and believe it.

I checked the neighbouring sentence for the same defect and cleared it:

> "Growth that leaves **entry_count** unchanged touches the directory
> alone — a growth raising one grid count ⌈Eᵢ / Tᵢ⌉ (§11.2) while another
> stays 0 among them, the product holding at 0."

If the em-dash clause is read as *defining* the class it is wrong, since
E 100 → 128 at T = 32 also leaves entry_count unchanged and involves no
zero. But read as naming the class's non-obvious member — which is what the
parallel closing em-dash does — it is fine, and I verified the general claim
holds: with N > 0 and every Gᵢ non-decreasing under growth, an unchanged
product forces every Gᵢ unchanged, so entries, segment CRCs and
crc_of_crc_array are all untouched and only the layer record's extents
change. Not a finding.

## 6. Attacks I built and that the document foreclosed

These are the attacks that failed. I list them because the charter asks
for the sentence that forecloses each.

**6.1 Codec 4 on a layer that addresses no tile.** Built: rank 2, extents
(0, 8), tile extents (2^20, 2^20), codec 4, interleaved uint64. P·Q =
2^40·8 = 2^43, far above the 0x7E000000 cap. Foreclosed *as conforming*:
[R-COD-07] is quantified over "addressed tiles", of which there are none,
and §17.2's Note states the escape and its exact end ("takes every
dimension's extent nonzero"). I then tried the obvious follow-up — does
the same emptiness excuse P·Q from the overflow rule? — and it does not:
"[R-ENC-04]'s overflow rule carries no such quantifier — it binds any sum
or product a file yields — so P·Q and P·Bᶜ are checked in an empty layer
even though this cap is not," and L2 lists P·Q. Decided in both directions.

**6.2 A commit that grows extents *and* changes a channel's fill.** The
interesting compound: grow so that Gᵢ·Tᵢ = Eᵢ on every axis (no padding
positions remain) and change fill in the same commit. §20.3 step 4's bar
lists "the set of padding positions … and the content [R-SER-05] fixes
there", and with no padding left there is nothing for the new fill to
contradict — so this is permitted, and correctly so. I then tried the
version that ought to break it: a **planar bool** layer with P mod 8 ≠ 0,
where pad bits (§14.3) depend on P, not on Eᵢ, and so survive any amount of
growth. Foreclosed: [R-SER-05]'s "Every pad bit MUST carry the plane's
channel's fill bit" makes the fill change alter a stored tile's fixed
content, the bar fires, and §20.3's own example (c) says it in words — "a
layer with no padding position **and no pad bit**". The document had
already found this compound.

**6.3 Permuting channel order on a layer with stored tiles.** Interleaved
with channels of unequal size: barred, since Fᶜ moves and the bar names
"the byte offset of any sample within the decoded tile image". Interleaved
with two same-size channels swapped: the *set* of offsets is unchanged, so
I hoped the list would miss it — but the bar's preamble is "alters … what
§14 fixes for its stored bytes **or how they decode**", and the list
"names where that effect arises rather than standing on its own." Channel
a's own offset moved, so it is caught. Planar with a channel appended at
the end: permitted, and harmlessly — each existing plane's ordinal c·N+s,
decoded size, offsets, codec and filter are all untouched; entry_count
rises, [R-CNT-17] forces a re-emitted region, and §20.3 step 4 covers that
path. Not a defect; a correct permission I could not turn into damage.

**6.4 A 128-byte conforming file carrying a record.** §5.1's Example says
the smallest conforming file "contains no layers", which is true but not
the same as "contains no records". I built one: front block [0,16);
user-metadata extent [16, 22) holding the two document bytes `{}` and its
4-byte CRC; directory [22, 51) = one 24-byte record header + 1 inline
encoding byte + 4-byte CRC; slack [51, 64); trailer [64, 128). Every
[R-CNT-06] gate passes, dir_offset 22 ≥ 16, dir_length 29 ≥ 4,
22 + 29 = 51 ≤ 64 = F − 64, extents disjoint and inside [16, 64),
extent_length 6 ≥ 5, inline_length exactly 1, `{}` is a JSON object with
vacuously sorted members and no numbers or keys to violate. Conforming, and
the document's own text supports it — I could not turn it into a
disagreement. §5.1's Example is explicitly non-normative and its "smallest"
claim is about size, which 128 still is.

**6.5 A run all of whose entries are structurally reject-tile.** §3.1 says
a tile is stored iff its entry is not the sentinel, so a malformed
non-sentinel entry names a *stored* tile — which ought to make it "the
first stored tile" of its run and drag L42's alignment check onto an offset
that does not exist. Foreclosed by §16.2's third sentence: "So are the
entries §15.3 classifies reject-tile on a *structural* ground: they address
no usable extent, and the run's stored tiles close over them," reinforced by
§15.3's "Such an entry contributes no stored extent to the *verifier* rows,
which bind over well-formed entries' extents only". L40 and L42 are verifier
rows, so both are covered, and the crc-failing case is explicitly carved
back in on both sides. This is tight.

**6.6 A user-metadata document decoding to 20 MiB.** Verifier A (16 MiB
bound) declines and MUST NOT certify; verifier B (32 MiB bound) certifies.
That *is* two verifiers reaching different results on one file — but not
the charter's fork, because §18.2 and §2.3 make A's result *cannot
establish*, which "is not a finding that the file is nonconforming," and
§21.9 makes the file conforming either way. Designed divergence, stated
three times. Not a defect.

**6.7 Residue past a completed commit, and the "three rows" list.** §9.5's
Note and §9.6 both say a bad tail is met as "the magic, the CRC, or
committed_file_length against the transport size" — three rows, F8/F14/F17
— and I spent a while trying to show that list short, since arbitrary
residue can pass all three and then fail F9 or F16 or F20. It is not short:
§9.6 defines "a valid trailer" two sentences earlier *as the probe's three
criteria* — "require the trailer CRC to verify and committed_file_length =
o + 64", plus the magic match — so "not a valid trailer" is exactly those
three by construction. Withdrawn.

**6.8 A later minor version's record type.** A file at version_minor 1
carrying record type 0x0003 is conforming under minor 1's text and, under
this text, a reserved-range type that F36 makes a violation — so the same
file is conforming and nonconforming depending on which minor's text you
hold, while §2.3 says conformance is to a *major*. I decided this is the
brief's "unresolvable forward reference into a reserved range … reportable
and expected" and not a defect: §12.2's Note and §20.5's F36/L25 sentence
both state the consequence deliberately, and §6.3's "readers MUST NOT
reject a file for its version_minor" is about the minor field, not about
reserved values.

**6.9 [R-EXT-02]'s "every numeric identifier space is partitioned
identically."** The trailer's flag lanes are then named as a *space* with
no experimental range, and they are not partitioned into
assigned/reserved/experimental at all — they are two lanes. A literal
counterexample to the rule's first sentence, inside the same rule. I am not
reporting it: the sentence names the exception in the same breath ("which
§6.3 partitions instead"), the flag lanes are not in §10.2's table of eight
spaces, and no implementer could be misled about a field §6.3 governs
directly. Reporting it would be padding.

**6.10 [R-CNF-03]'s MU = 1 carve-out and layer sub-records.** [R-CNF-03]
removes the acceptance duty for any file "carrying no record of a type it
does not implement with MUST_UNDERSTAND = 1", unqualified by scope, which
would let a reader refuse a conforming file over an experimental MU = 1
*sub-record*. Foreclosed twice, and decisively: [R-CNT-18] — "where the
file is otherwise conforming a reader MUST NOT reject the file for it" —
and §21.6's closing paragraph, "The qualifier is load-bearing — the same
type as a layer sub-record is reject-layer and never a ground to refuse the
file". Removing a duty is not granting a permission. Not a defect.

**6.11 [R-SER-08]'s coverage by T2 and T4.** T2 is restricted to real
positions and T4 to fill mismatch, so I checked whether a padding byte can
violate [R-SER-08] without violating [R-SER-05]: it would need to be
neither 0x00 nor 0x01 *and* equal to the recorded fill, which [R-TYP-07]
makes impossible by constraining a bool fill byte to 0x00 or 0x01. T2 and
T4 do jointly cover [R-SER-08], exactly as T2's cell claims.

**6.12 §8.1's coverage map.** I walked every field of every structure and
asked what checksum covers it: trailer → its own [60,64); directory and
every record header, inline payload, extent slot and crc_of_crc_array →
the directory CRC; segment CRC array → crc_of_crc_array; entry crc fields →
their segment CRC; stored tile bytes → the entry crc; user-metadata
document bytes → the extent's terminal CRC; unassigned-type extents →
nothing, stated; slack → nothing, stated; front block → equality, stated.
Exactly one each, no field uncovered and none doubly covered. Clean.

**6.13 §23.1's "Those two cases are exhaustive."** I tried the third case:
a shrink that turns real positions into padding of a tile the superseded
generation stored but the new state unstores. Foreclosed — §20.3's "the
quantifier is the superseded generation's, so a shrink that alters what
§14 fixes for a tile stored there is barred whether or not the new state
still stores it" bars it unless the newly-padding bytes already hold fill,
in which case nothing is disclosed and case two applies; if the tile's
extent leaves the live state, case one applies. The dichotomy holds on the
stated ground ("the bytes either travel out of the live state or stay in the
structure that carried them").

## 7. Findings

### adversary-01 — AMBIGUITY — byte-level

**Location.** §17.2, `[R-COD-04]`; cross-read against §15.2 (`[R-IDX-02]`),
§15.3 (`[R-IDX-03]`), §21.1, §21.4 row T14.

**Title.** [R-COD-04]'s codec-1 length equality carries no non-sentinel
qualifier, so a sparse codec-1 layer's sentinel entries are readable two
ways.

**Quotation.**

> "**Codec 1 — none.** The stored bytes are the filtered image
> verbatim. The index entry's length therefore MUST equal the tile's
> decoded size (§14.2, §14.3); a reader MUST treat a mismatch as a
> validity error at tile scope — checkable from the entry and the
> layer record alone, before any payload fetch. `[R-COD-04]`"

and, for the exemption the document does state and this rule is absent
from:

> "Sentinel entries are a reserved pattern, not offsets or lengths:
> `[R-ENC-03]`'s value-domain rule and `[R-ENC-04]`'s sum rule apply to
> the fields of non-sentinel entries only." (§15.2, `[R-IDX-02]`)

**Detail.** See §4 above for the file, the two verdicts and their
citations. Permitted readings: (a) the equality ranges over every entry of
a codec-1 layer, so a sentinel's length field of 2^64 − 1 is a mismatch and
the tile is reject-tile; (b) it ranges over non-sentinel entries only. I
pick (b) — the premise clause "The stored bytes are the filtered image
verbatim" presupposes storedness, §15.3's first row obliges a positive
"valid sentinel" classification, §19.4 step 4 short-circuits, and T14 and
§21.6 both read it that way. What an implementer does wrong without the
qualifier: lifts a check the rule itself calls "checkable from the entry
and the layer record alone, before any payload fetch" out of the per-tile
path into a sweep over the entry array, where sentinels have not yet been
classified, and rejects every unstored tile of every uncompressed sparse
layer.

**Byte-level: yes.** Verifier B reports *nonconforming* on the §4.1 file
and verifier A certifies it; reader B fails the read of tile 3 while
reader A returns 32 bytes of `0x00`. §21.1's "where a row and the rule it
cites diverge, the rule governs" hands B the only textual tiebreak, since
the "non-sentinel" qualifier lives in T14 (a row) and not in [R-COD-04]
(the rule).

### adversary-02 — AMBIGUITY — not byte-level

**Location.** §11.1, Rationale block following `[R-GEO-02]`.

**Title.** "a zero-extent layer's **last** zero grid count" reads two ways,
and the document's own house sense of "last" is the one that makes the
sentence false.

**Quotation.**

> "Growth that changes entry_count changes extent_length with it
> (`[R-CNT-17]`), so the layer's whole tile-index region is re-emitted
> and disk ordinals renumber wherever `[R-GEO-06]` moves them (§20.3,
> `[R-WRT-04]`) — the growth that raises a zero-extent layer's **last**
> zero grid count included."

**Detail.** See §5 above for the census and the two worked layers.
Permitted readings: (i) "the final remaining zero grid count", under which
the growth takes N from 0 to positive, entry_count changes, and the
sentence is true; (ii) "the last-declared dimension whose grid count is
zero", under which a rank-2 layer at extents (0,0) growing E₁ to 8 leaves
N = 0 and entry_count unchanged, so the growth is *not* among those the
sentence claims include it, and the sentence is false. I pick (i). But all
twelve other uses of "last" in the document are positional within an
already-fixed ordering, and the two that index a dimension — §11.4's "the
last-declared dimension varies fastest" and §16.2's "a band along the
last-declared dimension" — both mean last-declared, so a reader applying
the house sense reads a false claim in the passage that exists to teach
schema-first growth.

**Byte-level: no.** `[R-CNF-01]` puts Rationale outside normative text, and
every consequence is independently fixed and correct: `[R-GEO-03]` derives
N, `[R-CNT-17]` derives extent_length from entry_count, `[R-WRT-04]` fixes
re-emission, `[R-GEO-06]` fixes ordinals. An implementer who computes gets
the same bytes under either reading. The cost is comprehension, not
emission.

## 8. Confidence

**Medium.** I would expect two independent implementations built from this
text alone to interoperate on every file I could construct except the
sparse-codec-1 one, and I could not manufacture a second fork despite
sustained attempts at boundary values, degenerate files, reserved values in
every position, the reader/verifier seam, and two-feature interactions. The
document's arithmetic is exact everywhere I checked it, its register's
counts are mechanically correct, and its two largest recent worry-areas —
§20.3's tense-quantified bar and §16.2's transparency rules — survived
every compound commit I built against them. What holds confidence below
high is that the one surviving fork sits on a very common file shape, and
that the mechanism producing it — a MUST stated over a field without
repeating which instances of that field it ranges over — is the same
mechanism the brief reports as four of the last six byte-level defects,
which suggests the class is not yet exhausted.
