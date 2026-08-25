# Round 24 — Adversary transcript

## 0. Disclosure

I read exactly one file: `/Users/robertkleffner/Documents/GitHub/tarn/spec/tarn.md`
(4,445 lines), in full, in chunks. I opened no other file in the repository —
no `docs/`, no `PLAN.md`, no `AGENTS.md`, no `conformance/`, no
`spec/registry.json`, no git history, no web.

I ran local computation only, in a scratch directory I created
(`.../scratchpad/work/`): a CRC-32C implementation, an instance-counting script
over the register tables extracted from the spec text, a file builder, and a
self-written verifier. Those scripts read the spec file and files I wrote
myself, nothing else.

Context I did not ask for **did** appear before I began: a project
instruction file pointing at `AGENTS.md`, and an index of the maintainer's
auto-memory naming several memory documents (a wording rule, a working
cadence, a decision-style note, a workflow-failure note, a propagation-check
note, and a note about the §21 register). I did not open any of them and I
have not used their contents. I name their appearance here as the brief
requires; I have not repeated what they said.

## 1. Method

I read the document once end to end before touching the four named passages,
because I wanted my own model of the container before anyone's account of
what changed. Then:

1. Mechanically checked the register's own arithmetic (row counts, instance
   counts) against §21.1's stated instance rules and §21.8's totals.
2. Recomputed every constant and every worked byte example the document gives.
3. Built three complete files end to end — the minimal file, a
   sentinel-heavy layer, and a two-generation append — and wrote an
   independent verifier for them.
4. Walked the four named passages (§20.5, §21.2, §21.5, §21.7) word by word
   against the rules they cite.
5. Ran the four shapes the brief names (quantifier/scope, one-quantity-of-two,
   argument by analogy, claims about *when*) across the whole document.

## 2. Mechanical checks — all pass

### 2.1 Checksum and constants

My CRC-32C (reflected, poly 0x82F63B78, init 0xFFFFFFFF, final XOR) reproduces
§4.5's check vector: `CRC-32C("123456789") = 0xE3069283`, `CRC-32C(<empty>) =
0x00000000`. I then recomputed, and confirmed, every derived constant the
document publishes:

| Constant | Document | Computed |
|---|---|---|
| Appendix A trailer CRC | `D2 38 09 E0` (0xE00938D2) | 0xE00938D2 |
| §7.4 four-sentinel segment CRC | `55 49 A3 80` (0x80A34955) | 0x80A34955 |
| §7.4 crc_of_crc_array | `2E 98 EE C4` (0xC4EE982E) | 0xC4EE982E |
| §15.4 full all-sentinel segment | 0xEECB3BB2 | 0xEECB3BB2 |

I also re-derived by hand: §11.2's grid example; §11.4's ordinals (tile (1,0)
→ 8; (300,700) → s = 10, in-tile ordinal 11,452; planar channel 2 → disk
ordinal 74); §14.2's three layouts (18 / 12 / 30 bytes, offsets 15, 10, 25);
§14.3's `55 01` and `55 FD` (byte 1 = bit0 set, bit1 clear, pad bits 2–7 =
fill); §17.3's shuffle (`00 00 00 00 00 00 80 00 40 3F 40 40` — I re-derived
each of the twelve destinations from `i·n + j`); §15.4's 1,000,000-entry
layout (16 segments, last covering 16,960; entry at region byte 339,180;
segment 15 at [19,660,800, 20,000,000)); §20.3's 644-byte index; §21.9's
note-arithmetic (256 KiB at 2³², 4 MiB at 2³⁶); and §6.3's "remaining 48
trailer bytes" (64 − 8 magic − 2 major − 2 minor − 4 CRC = 48). Every one is
correct.

I also checked `[R-CNT-27]`'s 128-byte floor by construction: F ≡ 0 mod 64,
trailer at F−64, dir_offset ≥ 16, dir_length ≥ 4 forces F−64 ≥ 20 hence
F ≥ 128. Exact.

### 2.2 Register self-consistency

I extracted every row of §21.2–§21.5 and counted instances by §21.1's own
rule ("Instances within a cell are separated by semicolons, and a cell reading
— is one instance"):

```
F rows=36 instances=58
L rows=49 instances=116
T rows=26 instances=55
R rows=10 instances=48
TOTAL rows 121  TOTAL instances 277
```

§21.2 says 36, §21.3 says 49, §21.4 says 26, §21.5 says 10; §21.8 says "121
conditions over 277 instances". All four subsection counts and both totals
agree exactly. I then audited a sample of cells against §21.1's two stated
axes and found no cell that disobeys them:

- *does not equal* between two magnitudes → two directions: L21 (4 = 2 dirs ×
  2 layouts), L22 (4), L30 (2), T3 (6 = 2 × 3 layout shapes), T14 (6), T22 (6),
  R4's content-size pair (2 dirs × 2 containers). ✔
- *exceeds* / *larger than* → one direction: T21 (3 layout shapes, one
  direction), L44 (3, one direction). ✔
- pattern-against-constant → one: F8, F15, F24, L37, L38, T1. ✔
- nonzero test → one: L27, L28. ✔
- F23/L12's split into "inline_length 0" and "inline_length ≥ 2" is a
  two-magnitude *does not equal* against 1, so two is right under the same
  axis. ✔

### 2.3 §20.5's cross-reference arithmetic

§20.5 claims a compactor's output can carry a later-minor feature only as "a
carried ignore-lane bit … or an unrecognized `tarn.` key", the other two of
§10.1's four vehicles reaching such a file "only as values this text still
registers as reserved-range violations — F36 and L25 for a record type, and
one row for each of the other seven spaces §10.2 tabulates (L31, L33, L34,
L36, L43, L45, R1)".

Checked: §10.2 tabulates eight spaces. Minus record type, seven remain —
channel layout (L36), linearization (L33), sample type (L34), codec (L43),
filter (L45), index encoding (L31), metadata encoding (R1). Seven spaces,
seven rows, exactly the seven named. ✔ §10.1's four vehicles, two of which
§21.6 makes conforming (ignore-lane bit; unrecognized `tarn.` key). ✔

### 2.4 §21.2's "four rows"

"Four rows are outside that reasoning and do reach it": F8, F1 (trailer-magic
instance), F14, F6 (with F1's front-block instance). That is four rows, and
each names a field `[R-CNT-24]` fixes across every major. I checked the
complement: F5 (128-byte floor), F13 (F mod 64), F19 (incompat lane) are all
major-1-specific — `[R-CNT-24]` fixes only bytes [0,8), [8,12) and [60,64) of
the trailer, so flags at offset 12 is redefinable and F19 correctly does not
reach a foreign major; and a foreign-major file's minimum length is 80 bytes
(front + trailer), not 128, so F5 correctly does not reach it either. ✔

## 3. Files I built

All three were built from the document alone and checked by a verifier I
wrote from §6.2, §7.1, §7.2, §7.4, §8.1, §11.2, §15.1, §15.3, §15.4 and
`[R-COD-04]`.

**(a) The minimal file (Appendix A).** 128 bytes. Reproduced byte for byte
including the trailer CRC. No guesses.

**(b) `good.tarn`** — 448 bytes. Layer `sst`, rank 1, x extent 100 tile
extent 32, one interleaved float32 channel `temp` with fill 0x7FC00000, codec
1, filter 1. My independently constructed inline payload came out at 81 bytes,
matching §7.4's worked example exactly, and the index region at 84 bytes
(4×20 + ⌈4/2¹⁶⌉×4). One tile stored (128 bytes = P·Q = 32·4), three sentinels.
Layout: front [0,16), tile [16,144), index [144,228), directory [228,337),
pad [337,384), trailer [384,448).

**(c) `gen1.tarn` / `gen2.tarn`** — the two-generation witness for finding 1,
described in §5 below.

### Places I had to guess while building

Very few. Recording them honestly:

- **"the next 64-byte boundary" when the directory already ends on one.**
  `[R-LIF-02]` step 5 says "append the pad to the next 64-byte boundary". Read
  alone this is ambiguous between "the smallest boundary ≥ end" and "the
  smallest boundary > end". §6.2 settles it — "a writer that ends its
  directory on a 64-byte boundary leaves none" — so the pad may be zero. Not
  a defect; I record it because I had to leave `[R-LIF-02]` to resolve it.
- **crc_of_crc_array at entry_count = 0.** `[R-CNT-23]` forces 0. I checked
  that this coincides with the computed value: the CRC array is zero bytes and
  CRC-32C(∅) = 0x00000000, so the forced constant and the computed one agree.
  Nothing to guess after that.
- **Whether a layer whose record alone changes may keep its extent slot
  pointing at the prior generation's index region.** §20.3 step 4 states it
  outright ("A layer whose record alone changes keeps its extent slot,
  pointing at the existing region"), and §20.3's shape (c) figure confirms.
  No guess needed, but it is the one place where an implementer might expect
  re-emission and the document has to say so explicitly.

Nothing else in three complete builds required me to supply a fact the
document does not state.

## 4. Attacks tried and foreclosed

I list these because "empty is a real result, but only if the attacks were
good". For each I give the construction and the sentence that closes it.

**A1 — Codec 1 length equality against a sentinel entry.** `[R-COD-04]` says
"The index entry's length therefore MUST equal the tile's decoded size … a
reader MUST treat a mismatch as a validity error at tile scope", with no
sentinel qualifier. A sentinel's length field is 0xFFFF_FFFF_FFFF_FFFF, which
is never the decoded size. Build: any codec-1 layer with one sentinel. Verdict
fork attempted: reject-tile vs. valid sentinel. **Foreclosed** by three
sentences: `[R-IDX-02]` ("Sentinel entries are a reserved pattern, not offsets
or lengths"); §19.4 step 4 ("A valid sentinel short-circuits steps 5 and 6 for
that entry"); and T14's own text, which says "a **non-sentinel** index
entry's length". The rule's unqualified phrasing survives only because
`[R-IDX-02]` withdraws the field's status as a length.

**A2 — Structural entry that "is stored".** §3.1 defines *stored* as "its
tile-index entry for it is not the sentinel", so an entry with offset = 8 is
"stored" by that definition while §15.3 makes it structurally reject-tile. I
tried to make `[R-WRT-09]`'s "every stored tile's entry crc" and
`[R-LIF-08]`'s walk disagree. **Foreclosed**: §15.3 says such an entry
"contributes no stored extent to the *verifier* rows … and none to
`[R-LIF-08]`'s coverage walk"; §16.2 closes run continuity over it; §20.5
requires refusal on meeting it during regeneration. Every consumer of the
word "stored" that could have been damaged is separately qualified.

**A3 — Compactor that relocates nothing.** §20.5 makes regeneration the
mechanism by which a structurally-bad entry is forced in front of the
compactor. A compactor that places a region at the offset it already occupied
never "relocates" it and so never regenerates it. **Not foreclosed as a
question, but not a defect either**: §20.5 already says "a violation latent in
a structure it carries forward verbatim travels into its output", and
`[R-WRT-06]` bites only on a violation "it has detected". The output is a
different file (fresh file_id, generation 1) either way and remains as
nonconforming as its input, which the document permits. No fork.

**A4 — Stored-tile extent inside the directory region.** Entry offset inside
[dir_offset, dir_offset+dir_length), length ≤ region. Passes every reader row
of §15.3 (offset ≥ 16, length ≠ 0, offset+length ≤ F−64) and the tile's CRC
can be made to verify over directory bytes. A reader serves it.
**Foreclosed**: F33 registers it (verifier, reject-file), `[R-CNT-13]` routes
"another scope's structures" to reject-file, and §22.3 states outright that
"a reader that skips them is still conforming". Deliberate, stated seam.

**A5 — Byte-shuffle where L is not divisible by s.** `[R-COD-10]` asserts
"The decoded image's length L is divisible by s in every case (§14)". I
checked all three shapes: interleaved L = P·Q, s = Q → n = P; planar numeric
L = P·Bᶜ, s = Bᶜ → n = P; planar bool s = 1. Including an interleaved layer
mixing bool (B = 1) and float64. The assertion holds; no residue case exists.
**Foreclosed.**

**A6 — Codec 3 on a sub-1-KiB tile.** The smallest Window_Descriptor value is
1 KiB, and `[R-COD-06]` forbids a window exceeding the decoded size, so an
18-byte tile appears unencodable. **Foreclosed** by §17.2's own Note: the
tile "is therefore encodable under codec 3 only as a single-segment frame",
where Window_Size *is* the content size, which `[R-COD-06]` already pins to
the decoded size. I checked the descriptor's expressible set (1024 + m·128 for
exponent 0) to confirm the 1 KiB floor.

**A7 — file_id above 2⁶³ − 1.** `[R-ENC-03]` bounds "every offset, length,
extent, and count"; file_id is none of those, and §6.2's valid-values cell
says only "≠ 0". So file_id = 0xFFFFFFFFFFFFFFFF is conforming, and F2's
instance list correctly omits it. I confirmed F2's six instances are the
complete set of file-scope u64 offset/length/count fields a reader reads at
open. **Foreclosed — and correctly so.**

**A8 — L2's derived-quantity list.** I enumerated every product or sum a
layer's declarations yield and checked each is covered or dominated: Q ≤
65535·8 = 524,280 (cannot overflow); Fᶜ ≤ Q; ⌈P/8⌉ ≤ P; V = P·C dominated by
P·Q since Q ≥ C; max disk ordinal (C−1)·N + (N−1) = C·N − 1 dominated by C·N;
segment base s·2¹⁶ ≤ entry_count; region byte 20·k covered by the entry_count
formula. L2's nine instances are complete. **Foreclosed.**

**A9 — Empty layer escapes.** E₀ = 0 gives N = 0, addressed count 0, extent
slot (0,0), crc_of_crc_array 0, and escapes L44's lz4 cap and §21.9's tile
guarantee. I built it and it verifies. **Foreclosed and deliberate** — §17.2's
Note and §21.9's per-instance paragraph both state it, and both are careful to
say `[R-ENC-04]` carries *no* such quantifier so P·Q is still checked in an
empty layer.

**A10 — Interleaved bool byte at a padding position.** `[R-SER-08]` (T2) and
`[R-SER-05]` (T4) both reach that byte. **Foreclosed**: T2's own text carves
padding positions out and hands them to T4 — "the same byte at a padding
position is T4's, the two rows together covering `[R-SER-08]`" — and since
`[R-TYP-07]` constrains the fill byte to 0x00/0x01, T4 subsumes T2's
constraint there exactly.

**A11 — `[R-CNT-05]`'s pre-trailer gap vs. F7.** A gap longer than step 5's
pad is conforming (§2.3 names it as one of exactly two declared
writer-conduct-only obligations); a *structure* in it is F7. I checked the
two declared cases against every other writer MUST in the document and found
no third case that the text expressly declares not to be a file-conformance
violation. **Foreclosed.**

**A12 — F33's exclusion list.** "a claimant reaching the front signature block
or the live trailer is instead caught by the bounds rows F9/F10, F31/F32,
L16/L17 and T8/T9". I enumerated claimant kinds from `[R-CNT-02]` — directory,
non-layer top-level record extent, layer-record extent (= the tile-index
region, per §9.7), sub-record extent, stored-tile extent — and each has both a
low bound and a high bound row in that list. Complete. **Foreclosed.**

**A13 — `[R-CNT-21]`'s partial total under-counting.** partial = F less the
enumerated claimants' bytes; discarding a rejected layer's already-enumerated
claimants only raises it. It is an upper bound in every path I could
construct. **Foreclosed.**

**A14 — `[R-SLB-03]`'s dangling "its".** "each stored tile's offset equals the
previous stored tile's offset plus its length" — "its" could bind to either
tile. **Foreclosed** by L41's restatement ("plus **that tile's** length"), by
the word "packed", and by §16.2's worked example ("run 1's stored tiles are 8,
9, 11…15, packed with no gap where 10 would have been").

**A15 — Two verifiers disagreeing over a large user-metadata document.** A
20 MiB verbatim document: a verifier with a 16 MiB bound declines, one with a
32 MiB bound certifies. **Not a fork**: §2.3 makes the decline *cannot
establish*, which "is not a finding that the file is nonconforming". The two
verifiers do not contradict; one simply reports less.

## 5. Finding 1 — `[R-WRT-04]` step 4 bars and permits the same shrink

**AMBIGUITY/CONTRADICTION. §20.3 step 4, `[R-WRT-04]`.** Two sentences of one
rule give opposite answers for a shrink whose newly-created padding positions
already hold fill.

The bar first lists what a commit must not alter for a prior-generation stored
tile — "the set of padding positions (§11.3) and the content `[R-SER-05]`
fixes there, the decoded size, the byte offset of any sample within the
decoded tile image, or the codec and filter that produced the stored bytes" —
and then withdraws the list as a standalone test:

> The test is the effect on such a tile, and the list names where that effect
> arises rather than standing on its own: a change that leaves every one of
> those tiles' stored bytes meaning exactly what they meant — a filter whose
> mandated stride makes it the identity (`[R-COD-10]`), or a new padding
> position whose stored byte already holds the fill `[R-SER-05]` fixes — is
> not what this bars.

Call that **(A)**. Two paragraphs later:

> Unstoring that tile in the same commit does not rescue it either, and for
> the same reason: the quantifier is the superseded generation's, so a shrink
> that turns real positions into padding of a tile stored there is barred
> whether or not the new state still stores it.

Call that **(B)**.

### Why the conflict is real and not an ellipsis

A **new padding position in a tile the layer already stores can arise from a
shrink and from nothing else.** I checked every other declaration change:

- growing Eᵢ removes padding positions from an existing tile and adds new
  tiles (not tiles "stored in the generation this commit supersedes");
- changing any Tᵢ changes P, hence the decoded size — barred outright;
- changing Tᵢ while holding P constant (e.g. (2,6) → (3,4)) moves sample byte
  offsets — barred outright;
- changing rank, channel count or channel order changes Q or the offsets —
  barred outright;
- changing a fill value alters the content at *existing* padding positions,
  not the set of them (§20.3's shape (c) treats it separately).

So (A)'s carve-out has exactly one referent: the shrink (B) forbids.

The carve-out is also load-bearing for a permission the same rule grants three
lines earlier — "an extent MAY **grow**". A grow *does* alter "the set of
padding positions" of a stored tile, which the bar's list names. Only (A)'s
"the list names where that effect arises rather than standing on its own"
rescues the grow. So (A) cannot be read as decorative; and once (A) governs,
(B)'s unconditional final clause is the outlier.

§21.7 independently favours (A). It says of the bar: "A change reaching a byte
§14 structurally constrains — a padding position, a pad bit, or a boolean byte
— fires §21.4's content rows." Under (B) there would exist a *barred* change
that reaches a padding position and fires no content row (T4 passes, because
the byte already holds the fill). That is a state §21.7's account says does
not occur.

### The concrete construction

Layer `a`: rank 1, dimension `x`, tile extent T = 4, one interleaved uint8
channel `v` with fill `0x00`, codec 1 (none), filter 1 (none), no alignment,
no slab.

Generation 1, E = 6. G = ⌈6/4⌉ = 2, N = entry_count = 2, P = 4, Q = 1,
decoded size 4.

```
tile 0  [16, 20)  01 02 03 04      x = 0..3, all real
tile 1  [20, 24)  07 00 00 00      x = 4 -> 0x07 (real)
                                   x = 5 -> 0x00 (real, and equal to fill)
                                   x = 6,7 padding -> 0x00 = fill  [R-SER-05]
index   [24, 68)  2 entries + 1 segment CRC = 2*20 + 4 = 44 bytes
dir     [68, 169) one layer record, inline_length 73, extent slot (24, 44)
pad     [169, 192)
trailer [192, 256)   generation 1, F = 256
```

Generation 2 commits one change: dimension extent 6 → 5. G = ⌈5/4⌉ = 2 is
unchanged, so entry_count stays 2, no disk ordinal moves, the stored-tile set
is unchanged and the index region's *content* is unchanged — this is §20.3's
shape (c), "a change confined to the directory", and `[R-WRT-05]` keeps the
layer record's extent slot pointing at (24, 44). The commit appends only a new
directory (101 bytes at 256), a pad, and a trailer; F = 448.

In generation 2 tile 1 carries one real position (x = 4) and three padding
positions (x = 5, 6, 7), each of which must encode the fill `0x00` — and each
already does. I wrote a verifier from §6.2/§7/§8.1/§15/§17.2 and ran it over
both files: both pass every reader-detectable and every verifier-detectable
row I implemented, including T4's padding-content check.

### The two verdicts

- **Appender P (reading A).** The change leaves tile 1's stored bytes meaning
  exactly what they meant; the newly-padding byte at x = 5 already holds the
  fill `[R-SER-05]` fixes. Permitted. P emits the 448-byte generation-2 file.
- **Appender Q (reading B).** "a shrink that turns real positions into padding
  of a tile stored there is barred whether or not the new state still stores
  it." Tile 1 is stored in the superseded generation and x = 5 goes real →
  padding. Barred. Q must refuse and tell its caller to rewrite the file whole
  under a fresh file_id.

Both defend from the same rule. I picked **(A)**: it is the paragraph the
shrink paragraph itself defers to ("the bar above is the whole of the test"),
it is required to make the sibling grow permission coherent, and §21.7's
witness account presupposes it.

### Byte-level

Yes, on the emit half. The generation-2 byte sequence — file_id unchanged,
generation 2, the generation-1 bytes as an intact committed prefix, extent 5 —
is emittable by a conforming appender under (A) and by no conforming writer
at all under (B): a creator emits generation 1, and a compactor emits
generation 1 under a *fresh* file_id (`[R-WRT-06]`), so neither can produce
those 448 bytes. The two implementations are appenders P and Q; the artefact
they differ on is `gen2.tarn` in full.

It is **not** byte-level on the accept/reject half. §21.7 is explicit that the
bar has no file-level witness where the live state stays clean, and here it
does stay clean, so every verifier certifies `gen2.tarn` under either reading.
I grade it byte-level on the emit half alone and say so.

### What an implementer does wrong without a resolution

An appender author writing the "amend a layer's extents" path must decide
whether a shrink that only de-realises fill-valued positions is a commit or a
rewrite. Reading (B) costs a full duplication of the layer's stored bytes for
a change that touches one `u64` in the directory — precisely the outcome
§20.3's own prose warns against ("leaving the file larger for a change that
reads like a directory edit"). Reading (A) costs 192 bytes. A library that
picks (B) and a library that picks (A) will diverge on real workloads —
trimming a time axis after a partial ingest is the ordinary case — and the
files they produce are not interconvertible, since the (A) file's prefix is
the (B) library's refusal.

### Narrowest repair

Either strike (B)'s final clause back to the quantifier point it is making —
"…so a shrink that damages a tile stored there is barred whether or not the
new state still stores it" — or, if (B) is the intended rule, delete (A)'s
"or a new padding position whose stored byte already holds the fill
`[R-SER-05]` fixes" and supply a different rescue for the grow permission.

## 6. Finding 2 — `[R-CNF-03]`'s MU = 1 exclusion is unqualified where §21.6 says the qualifier is load-bearing

**AMBIGUITY. §2.3 (`[R-CNF-03]`), against §21.6's closing paragraph and
`[R-CNT-18]`.**

§2.3's conforming-reader definition scopes the acceptance duty:

> A reader MUST accept every conforming file of a format major version it
> implements, carrying no record of a type it does not implement with
> MUST_UNDERSTAND = 1 — in a conforming file such a type is necessarily from
> the experimental range, since a reserved-range type carrying MU = 1 is
> itself a violation — and none of whose values exceeds the minimum
> guarantees of §21's limits table (§21.9's `[R-ERR-04]` governs a refusal on
> that last ground; §21.6's closing paragraph names the other two)

The forward reference is to §21.6, which names the second ground as an
**experimental-range top-level record type carrying MU = 1**, and then says:

> The qualifier is load-bearing — the same type as a layer sub-record is
> reject-layer and never a ground to refuse the file (`[R-CNT-18]`), so only
> the top-level case is a file a reader refuses

§2.3's own clause carries no "top-level" qualifier. So the two texts describe
different exclusion sets.

**Construction.** A conforming file with two layers. Layer L1's record carries
a sub-record of type 0x8001 (experimental range, §10.2) with MU = 1, PE = 1,
inline_length 0, extent slot (0,0). Layer L2 is clean and stores tiles. Nothing
else in the file is irregular. The file is conforming: §10.3's prohibition on
publishing experimental values "binds the writer's conduct, not the bytes"
(`[R-CNT-15]`, `[R-CNF-02]`), and F35/F36/L24/L25 register only the
*reserved* range.

**Reading 1.** §2.3 excludes any file "carrying … a record of a type it does
not implement with MUST_UNDERSTAND = 1" from the acceptance duty. This file
carries one. The reader owes nothing, and refuses the file, serving neither
layer.

**Reading 2.** The exclusion removes an obligation and grants no permission,
and `[R-CNT-18]` supplies the missing prohibition: "an unknown sub-record type
with MU = 1 is reject-layer, and where the file is otherwise conforming a
reader MUST NOT reject the file for it". The reader rejects L1 and serves L2.

I picked **Reading 2**. `[R-CNT-18]`'s MUST NOT is in capitals and directly on
point; `[R-CNF-12]`'s licence to reject runs only "For a nonconforming file";
and §21.6 says the top-level qualifier is load-bearing, which it can only be
if the sub-record case is *not* excluded.

**Byte-level: no.** The verdict is decided — `[R-CNT-18]` forecloses Reading 1
— so no two *conforming* implementations differ. The cost is that §2.3's
clause, read at its own site, states an exclusion set two sections wider than
the one §21.6 says it names, and a reader author who implements the
conformance-class definition literally will build the wrong refusal and only
discover it at §7.4. I report it because it is a scope defect in the sentence
the brief's shape 1 describes — a permission-shaped clause over a structure
that does not say which instances of that structure it ranges over — and
because the same unqualified phrasing in the *verifier* bullet three
paragraphs later is correct there, which is what makes the reader bullet easy
to read as deliberate.

**Narrowest repair.** Insert the qualifier: "carrying no *top-level* record of
a type it does not implement with MUST_UNDERSTAND = 1".

## 7. Things I looked at and decided not to report

Recorded so the next round need not re-tread them.

- **`[R-ENC-02]`'s big-endian prohibition is not itemised in §21.7.** A
  big-endian-written field is simply a different little-endian value and has
  no witness, the same argument §21.7 gives verbatim for `[R-ENC-06]`. §21.7
  says it is "the account, **by class**", and the class is present. Not a
  defect.
- **§20.4's preservation obligations (`[R-WRT-05]`, the drop rules) are not
  itemised in §21.7 either.** Same disposition: they are history properties,
  and §21.7 names that class via `[R-LIF-01]`/`[R-LIF-03]`.
- **§21.7's "(T15, T17, T23, T25)" under-enumerates the codec rows** that may
  witness a codec change (T16, T18–T22, T24 can also fire). The sentence is
  hedged twice — "*sometimes*", "neither is assured" — and under-enumeration
  here is conservative, so no implementer concludes a witness exists where
  none does.
- **§2.3's "since a reserved-range type carrying MU = 1 is itself a
  violation"** gives a weaker reason than the document has: a reserved-range
  type is a violation whatever its MU bit (F36, L25). The conclusion drawn is
  correct. Prose imprecision, not a rule defect.
- **F7 and F33 enumerate "tile-index regions", "record extents" and
  "sub-record extents" as separate instances** although §9.7 says the
  tile-index region "enters the walk once, as that record's extent, and is not
  a second claimant beside it". Under §21.1's instance rules these are
  distinguishable containers, so the enumeration is defensible; it affects
  corpus size, not any verdict.
- **§5.2's "a scope-level rejection ends that scope's enumeration"** reads as
  though a tile-scope rejection could truncate the walk, which §9.7 contradicts
  for content-ground reject-tile entries (their extents stand). §9.7 is the
  operative procedure and is unambiguous; §5.2's parenthetical only
  illustrates the layer case.
- **A 20 MiB user-metadata document splits reader behaviour** between
  ignore-record and a whole-file resource decline. §18.2's Note licenses both
  explicitly. Divergent but stated.

## 8. Confidence

Medium-high that an implementation built from this text alone would
interoperate on the *file* predicate: I built three files end to end and the
document determined every field, every derived quantity, and every constant.
The gap is on the *transition* predicate — §20.3 step 4 — where finding 1
leaves two appenders producing different files from the same input and the
same caller request.
