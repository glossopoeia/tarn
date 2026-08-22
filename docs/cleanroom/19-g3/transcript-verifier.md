# Round 19 — Verifier implementer, working transcript

**Disclosure.** I opened exactly one file: `/Users/robertkleffner/Documents/GitHub/tarn/spec/tarn.md`,
read end to end (4,364 lines) in five passes. I ran `wc`, `grep`, and Python
scripts of my own authorship in the scratchpad (`crclib.py`, `appa.py`,
`build.py`, `adv.py`, `count.py`, `ids.py`); every one of those reads either
nothing or only `spec/tarn.md`. I did not open `docs/`, `PLAN.md`,
`OPEN-QUESTIONS.md`, `AGENTS.md`, `README.md`, `conformance/`,
`spec/registry.json`, or any ADR; I ran no git command; I made no web request;
I did not list or read the round19 output directory. Prior knowledge of other
array/image formats was used only to generate suspicions (e.g. "is the zstd
window-descriptor floor really 1 KiB?"), and every such suspicion was settled
against this document's own text or by local computation, never by appeal to
another format.

---

## 0. How I worked

I built the verifier as an ordered algorithm first, then ran it, on paper and
in Python, against files I constructed byte-for-byte. Where the algorithm
reached a step the document did not determine, I wrote the guess down at that
moment rather than at the end. That is where the findings come from: eight of
the nine below are places I actually stopped and could not proceed without
choosing.

I began by reproducing every constant the document states, because a verifier
that cannot reproduce them is not implementing this specification (§4.5), and
because a constant that does not reproduce is the cheapest possible finding.

### 0.1 Checksum constants — what I reproduced

CRC-32C implemented from §4.5's parameters alone (reflected Castagnoli
0x1EDC6F41 → reflected table constant 0x82F63B78, init 0xFFFFFFFF, final XOR
0xFFFFFFFF, stored little-endian).

| Constant | Stated | Computed | Where |
|---|---|---|---|
| CRC-32C(`"123456789"`) | `0xE3069283` / `83 92 06 E3` | `0xE3069283` | §4.5, App. B |
| CRC-32C(zero bytes) | `0x00000000` | `0x00000000` | §4.5, App. A |
| CRC-32C of 2¹⁶ sentinel entries | `0xEECB3BB2` | `0xEECB3BB2` | §15.4 `[R-IDX-05]`, App. B |
| CRC-32C of 4 sentinel entries (80 B) | `0x80A34955` / `55 49 A3 80` | `0x80A34955` | §7.4 example |
| crc_of_crc_array over `55 49 A3 80` | `0xC4EE982E` | `0xC4EE982E` | §7.4 example |
| Appendix A trailer CRC over `[0,60)` | `0xE00938D2` / `D2 38 09 E0` | `0xE00938D2` | App. A |

**All six reproduce.** I could not reproduce anything a codec produces
(no deflate/zstd/lz4 constant is stated as a literal, so there was nothing to
reproduce there), and there are no other stated checksum literals in the
document. I also re-derived Appendix A's whole 128-byte file: every trailer
field decodes to the value the annotation table claims (version_major 1,
version_minor 0, flags 0, generation 1, dir_offset 16, dir_length 4,
committed_file_length 128, file_id 0x0123456789ABCDEF, reserved zero), the
directory region `[16,20)` is `00 00 00 00` = CRC-32C of zero bytes, and
F = 128 ≡ 0 (mod 64).

### 0.2 Worked examples I checked arithmetically

Not findings — recorded because a verifier's arithmetic has to agree with the
document's, and disagreement would have been a finding.

- §7.4's 81-byte layer-record payload: name 4 + nine scalars 34 + dimension
  entry 18 + channel entry 12 + trailing fixed 13 = 81, no residue, so the
  sub-record sequence is empty. `⌈100/32⌉ = 4`; extent_length
  `4·20 + ⌈4/2¹⁶⌉·4 = 84`. ✓
- §12.3's channel entry `04 74 65 6D 70 0C 00 04 00 00 C0 7F` is byte-identical
  to bytes 56–68 of §7.4's dump. ✓
- §11.4: (300,700) → tile (1,2), s = 10, in-tile (44,188), ordinal 11,452;
  planar channel 2 → 2·32 + 10 = 74. ✓
- §14.2: interleaved (2,3), a:uint8 b:uint16 → Q = 3, decoded 18, ordinal 5 at
  [15,18); planar b = 12 bytes, ordinal 5 at 10–11; t:float32 m:bool → Q = 5,
  decoded 30, ordinal 5 at [25,30). ✓
- §14.3: P = 10 alternating → `55 01` (fill false) / `55 FD` (fill true, pad
  bits 2–7 set). ✓
- §14.5: extents (5,5) tile (4,4) → 2×2 grid, edge tile (1,1) has 1 real and 15
  padding positions, decoded 32 bytes, values 1–15 each `CD AB`. ✓
- §17.3 shuffle: `00 00 80 3F 00 00 00 40 00 00 40 40` (s=4, n=3) →
  `00 00 00 00 00 00 80 00 40 3F 40 40`. ✓ (I re-derived it from
  `i·n + j`, not by pattern-matching the stated answer.)
- §15.4: entry_count 1,000,000 → 16 segments (15 full + 16,960), 64-byte CRC
  array, region 20,000,064 B; tile 999,999 in segment 15 at segment-relative
  339,180; array `[20,000,000, 20,000,064)`; segment 15
  `[19,660,800, 20,000,000)` = 339,200 B ≈ 339 KB; one full segment =
  65,536·20 = 1,310,720 = 1.25 MiB. ✓
- §21.9's note: 2³² entries → 65,536 segment CRCs → 256 KiB; 2³⁶ → 4 MiB. ✓
- §17.2's zstd note: RFC 8878's Window_Descriptor minimum is
  windowLog 10 → 1024 B, so a sub-1-KiB tile is encodable only single-segment,
  where Window_Size = Frame_Content_Size = the decoded size. The two
  derivations agree exactly as the note claims. ✓
- lz4 cap `0x7E000000` = 2,113,929,216. ✓

### 0.3 Register arithmetic

I parsed §21.2–§21.5 mechanically and applied §21.1's counting rule
("Instances within a cell are separated by semicolons, and a cell reading — is
one instance"):

```
rows:      F 36, L 49, T 26, R 10  = 121
instances: F 58, L 116, T 55, R 44 = 273
```

§21.2 says 36, §21.3 says 49, §21.4 says 26, §21.5 says 10, and §21.8 says
"121 conditions over 273 instances". **All five numbers agree.** I also
enumerated every `[R-…]` identifier: none is cited without being defined, none
is defined twice, `[R-SER-04]` appears exactly once (its withdrawal note,
§14.4), and `[R-ENC-100]` appears only as §2.2's illustration. No identifier
hygiene defect.

---

## 1. The certification procedure

### 1.1 Verdict vocabulary and its availability

Three verdicts (§2.3 `[R-CNF-11]`): *conforming*, *nonconforming*,
*cannot establish*. The availability rules, assembled:

- **nonconforming** — the verifier established at least one violation. This
  dominates: "An established violation takes priority: a verifier that has
  established any violation reports *nonconforming*, however many requirements
  it was unable to check".
- **cannot establish** — no violation established, and at least one requirement
  could not be checked *on a capability or resource ground*. §2.3's list is
  introduced with "as when", so it is illustrative, not closed: foreign format
  major; MU = 1 record of an unimplemented type; codec/filter it cannot execute
  (`[R-COD-11]`); a layer's or tile's decode declined on resource grounds
  (`[R-ERR-04]`, `[R-SER-05]`, `[R-SER-08]`); a user-metadata document declined
  on the size bound (`[R-MTA-09]`). Certification is barred here explicitly:
  "a verifier MUST NOT certify a file it reports that way".
- **conforming** — everything checked, nothing violated.

Two grounds that look like cannot-establish and are not:

1. A user-metadata record at an **unassigned** encoding. `[R-MTA-10]`: "A
   verifier meeting such a record in an otherwise conforming file has no
   requirement it is unable to check". Certification proceeds; the record is
   *reported*, not held against the file.
2. Anything in §21.7. "no file-level witness exists to check, so nothing about
   the file is left undetermined and the verdict is unaffected." — but see
   **verifier-02**: that disclaimer sits in §21.7's first paragraph and the
   larger list is in its second.

I checked whether `[R-COD-11]`'s branch is ever live for a *conforming*
verifier and concluded it is not: §17.4 says so itself ("For a conforming
reader that position arises only at a reserved or experimental value ...
software unable to execute an assigned codec or filter is not a conforming
reader"), and a reserved/experimental codec value is L43, a violation, which
§2.3's priority rule sends to *nonconforming*. I nearly reported this as a
trap — a naive implementer reading §2.3's list in isolation would answer
"cannot establish" for codec = 7 — but §2.3 resolves it in its own next
sentence. Not a defect.

### 1.2 The ordered algorithm I built

Ordering is free except where §6.2 fixes it, where §8.2's chain of trust fixes
it, and where `[R-CNT-04]` places the front block "before other processing".
§21.1 puts verifier rows at detection point *certification*, "which §19.2
places outside the reader tiers entirely", so those carry no ordering
obligation. Reader rows carry §19.2's *latest* points, which a verifier
satisfies trivially since it checks everything.

**Phase 0 — size.** Obtain the transport-authoritative F_phys (`[R-CNT-10]`).
A verifier MUST NOT substitute committed_file_length for it.

**Phase 1 — front block.** Compare `[0,16)` to the constant. A verifier holds
no `[R-CNT-04]` exemption (§2.3 "including those ordinary readers are exempted
from"; F6's row; Appendix H). Mismatch → **F6**, or **F1**'s front-block
instance if byte-reversed. Nonconforming, *and this survives a foreign format
major* — §21.2's preamble makes F6/F1 one of the four rows that reach such a
file. If F_phys < 128 → **F5** (`[R-CNT-27]`).

I noted here that F5 and F6 are not isolable on a 12-byte file; §24
`[R-VEC-02]` anticipates exactly that ("the entry records every row the file
exercises and says which it was built for").

**Phase 2 — trailer, in §6.2's fixed order.**
1. magic at F−64 → F8 / F1;
2. CRC over `[0,60)` → F14;
3. version gate → F18 if version_major = 0 (**violation**); if
   version_major ≠ 1 and unimplemented → **cannot establish**, *not* a
   violation, and — see §5.2 — **no slack total is owed at all**, because no
   live trailer was established;
4. then, together: flag gates (F19 for any incompat bit; ignore-lane bits
   ignored, and a set one is expressly **not** a violation, §6.3);
   committed_file_length = F_phys (F17) and ≡ 0 mod 64 (F13); dir_offset ≥ 16
   (F9); dir_length ≥ 4 (F16); dir_offset + dir_length ≤ F − 64 (F10);
   1 ≤ generation ≤ 2⁶³−1 (F11, and F2/F3 for domain and sum); file_id ≠ 0
   (F12); reserved zero (F15).

Any failure in phase 2 → nonconforming **and** no live trailer, hence §5.2's
"the total is not owed at all, ... which is not a partial total but the absence
of one". That is a clean, decided answer and I used it.

**Phase 3 — directory region.** CRC over the first dir_length − 4 bytes → F20.
This is the first place the walk can be blocked with a live trailer already
established; see **verifier-01**.

**Phase 4 — top-level record walk.** F29 (framing/residue), F24 (type 0),
F34 (second user-metadata), F35/F36 (reserved-range type, with/without MU),
F30/F31/F32 (extent slot), F21/F22/F23 (user-metadata framing), F25/F26/F28
(flag bits — verifier-only rows), F4 (duplicate layer name), and the layer-name
rows L3/L5/L6 which §19.1 step 4 and §21.3 both place at **open**, not layer
access. §19.1's step 4 is precise about the namespace: a record whose name
field does not lie within its inline_length "contributes no name to the
namespace and is instead a validity error at layer scope", and uniqueness is
decided over raw bytes "whether or not each name is itself well-formed".

**Phase 5 — per-layer record validation (§19.3).** I walked §19.3's enumeration
against §21.3 row by row and found it complete over every reader-detected
layer row: L1, L2, L4, L7, L8, L9, L10–L17, L19–L23, L24, L26–L36, L39, L43,
L44, L45 are each reachable from a rule §19.3 names, and the rows §19.3 omits
are exactly the verifier rows (L18, L25, L40–L42, L46–L49) and the tile-use
rows (L37, L38). §19's preamble already disclaims exhaustiveness
("§21's register is"), so nothing turns on it — but the enumeration holds up.

**Phase 6 — index chain, per layer.** `[R-CNT-17]`'s cross-checks (L21, L22),
then crc_of_crc_array (L37), then each segment CRC (L38), then per-entry
classification under §15.3 (T6–T12), then each stored tile's crc (T1).

**Phase 7 — decode every stored tile.** §9.7 is explicit and I leaned on it
hard: "A verifier decodes every stored tile, whatever content obligations §14
places on the layer: §21.4's codec rows are file-conformance violations, and a
verifier MUST NOT certify past a violation it has not looked for." Note the
drafting: the decode sentence carries no BCP 14 keyword, so under §2.1 it has
no force of its own — but the following MUST NOT does all the work, since you
cannot have looked for T15/T17/T21–T25 without decoding. This composes
correctly with the resource-decline (which yields *cannot establish*, not
certification). Checks here: T3, T14, T24, T25, and the codec-specific rows;
then the content rows T2, T4, T5, and T26's cause.

**Phase 8 — coverage walk (§9.7 `[R-LIF-08]`).** Below, §2.

**Phase 9 — alignment and slab invariants.** L40, L41, L42. Below, §3.

**Phase 10 — record extents.** R2 (terminal CRC), R1 (encoding value), R3–R10
(document), F27/L48 (member ordering). A verifier must decode every
user-metadata document under an **assigned** encoding: §2.3 makes it a
file-level requirement, `[R-MTA-09]` makes declining it a cannot-establish
ground, and R3–R10 are reader rows only at *extent use* — a tier an ordinary
reader may never reach, but a verifier always does.

**Phase 11 — verdict**, per §1.1 above.

### 1.3 What the verifier reports

Assembled from every reporting clause I could find:

| Owed | Rule | Modal |
|---|---|---|
| the verdict | §2.3 | declarative |
| slack total (partial + what stopped the walk) | §5.2 `[R-CNT-21]` | MUST |
| each requirement unchecked on a capability/resource ground, naming requirement and ground | §2.3 `[R-CNF-11]` | MUST |
| each scope not examined, as *unexamined*, if it stopped at the first violation | §2.3 `[R-CNF-11]` | MUST |
| each record ignored at an unassigned metadata encoding — scope, encoding value, stored extent length | `[R-MTA-10]` | MUST |
| an unsorted metadata document | `[R-MTA-05]` | MUST |
| a resource refusal, as a resource limit and not a validity error | `[R-ERR-04]` | MUST |
| the bound applied and the extent length, on a declined document | `[R-MTA-09]` | SHOULD |
| a SHOULD deviation, as an advisory, where observed (no search owed) | §2.4 `[R-CNF-12]` | declarative |

Building this table is where **verifier-05** came from: nothing here obliges a
verifier reporting *nonconforming* to say *what* it found. And **verifier-06**
came from noticing that the one class of live bytes a certificate covers
without any checksum at all — an unassigned record type's extent — is the one
class with no naming duty, while the metadata analogue has one.

---

## 2. The coverage walk, done on files I built

### 2.1 The partition

`[R-CNT-02]` partitions the live committed state into: the front signature
block; or one structure — a stored-tile extent, a record extent (whatever the
record's type), the directory, the trailer. §9.7 adds the traversal rules I
needed:

- a record is **not** a claimant of its own header/payload — the directory
  covers them;
- a layer record's extent slot addresses its index region, so the region enters
  once, as that record's extent, not twice;
- an entry §15.3 classifies reject-tile **on a structural ground** contributes
  no stored extent; one whose stored bytes alone fail its crc **keeps** its
  extent;
- front block `[0,16)` and trailer `[F−64,F)` are claimed; every other claimant
  must lie within `[16, F−64)`.

**Certified / counted-but-unconstrained / neither.** My answer:

- **Certified** (placed *and* content-checked): the trailer, the directory, each
  tile-index region, each stored-tile extent, each user-metadata extent under an
  assigned encoding, and the front block (by equality rather than checksum).
- **Counted but unconstrained** — two classes, and the document names both:
  (a) the extent of a record of a type this specification has not assigned —
  §8.1's last row gives it *no checksum*, and no content rule reaches it; it is
  a claimant, so it is *placed*, and that is all;
  (b) a user-metadata extent under an unassigned encoding — checksummed by
  `[R-CNT-20]`, but "no content rule attaches to the extent's bytes"
  (`[R-MTA-10]`).
- **Slack** — everything the walk does not reach. Unconstrained, uncovered,
  counted.
- **Neither?** No. §5.2's Note settles it: "The live committed state is
  *defined* as the front block plus what a complete coverage walk reaches, and
  `[R-LIF-08]` makes every byte that walk misses slack — so 'belongs to no
  class' describes nothing". Bytes at or past F are not a fourth class either:
  `[R-CNT-06]` requires committed_file_length = the transport size (F17).

**Is every live structure covered by a checksum?** No — and the exception is
exactly class (a). Everything else is covered exactly once: index entries by
segment CRCs, the segment CRC array by crc_of_crc_array, crc_of_crc_array and
every record byte by the directory CRC, stored tiles by their entry crc, and
the three terminal fields (trailer CRC, directory CRC, user-metadata extent
CRC) verified by comparison and covered by nothing further, per §4.5's explicit
carve-out. I checked for double coverage and found none: the index region's
entry bytes and its CRC-array bytes are covered by different checksums, never
both.

### 2.2 A concrete file, and its slack

I constructed file **W**, generation 1, one layer, and computed every number.

Layer `sst`: rank 1, dimension `x`, E = 100, T = 32 → G = 4, N = 4;
interleaved; C = 1; channel `temp` float32, fill `0x7FC00000`; codec 1, filter
1; A = 0, S = 0, A_slab = 0; index_encoding 1; entry_count 4. Inline payload is
81 bytes — I emitted it field by field and got 81, matching §7.4. Decoded size
per tile = P·Q = 32·4 = **128**, and codec 1 forces every stored entry's length
to 128 (`[R-COD-04]`). Index region = 4·20 + 4 = **84**. Tile 3 covers
x ∈ [96,128), of which 96–99 are real and **28 are padding positions**;
generation 1 leaves it a sentinel.

Layout and the walk:

```
 [0,16)      16  front signature block   (equality)
 [16,144)   128  stored tile 0           (entry crc 0xF8118D31)
 [144,272)  128  stored tile 1           (entry crc 0xFDF96FE9)
 [272,400)  128  stored tile 2           (entry crc 0x99870149)
 [400,484)   84  tile-index region       (= layer record's extent)
 [484,593)  109  directory (105 B record sequence + 4 B CRC)
 [593,640)   47  pre-trailer pad          <- slack
 [640,704)   64  live trailer
                 F = 704, 704 mod 64 = 0
```

crc_of_crc_array for this index = `0x809B053C`.
Claimed = 16 + 128·3 + 84 + 109 + 64 = **657**. **Slack = 704 − 657 = 47**, and
those 47 bytes are exactly the pre-trailer pad. Walk complete → the total is
exact, not partial. No structure lies in `[593,640)`, so **F7** does not fire.
Verdict: **conforming**.

### 2.3 A walk that does not complete

Same file, tile 2 moved to `[270,398)` so it overlaps tile 1's `[144,272)` on
`[270,272)` — two bytes, both extents belonging to layer `sst`. §7.2: "a
verifier MUST treat an intra-layer overlap ... as reject-layer" → **L18**.
Verdict: **nonconforming**.

`[R-CNT-21]`: because the walk itself established the rejection, "the claimants
it had already enumerated are discarded with the layer". Surviving claimants:
front (16), directory (109), trailer (64) = 189.

**Partial total = 704 − 189 = 515**, reported as partial, naming layer `sst` /
L18 as what stopped the walk. The file's true slack, if one counted the
rejected layer's bytes, is 704 − 655 = 49 (the two-byte overlap plus
`[398,400)`). 515 ≥ 49, so the "upper bound, never an under-count" promise
holds. I verified the direction rather than assuming it.

That promise is also what settles a smaller question I stopped on: is "F less
the bytes claimed by the claimants the walk did enumerate" a **sum of lengths**
or a **union of ranges**? On overlapping claimants the sum reading gives
704 − 751 = **−47** for the cross-layer file below — an under-count, and a
negative one. `[R-CNT-21]`'s own "never an under-count" forbids it, so the
union reading is forced. Decided by the text; not reported.

### 2.4 The case I could not decide — file-scope rejection

Two layers, A and B. A's tile 2 at `[272,400)`, B's single tile at `[390,518)`;
overlap `[390,400)`, ten bytes, **across layers** → §7.2's "any overlap across
layers ... as reject-file" → **F33**. Verdict: nonconforming, easily. The slack
total is where I stalled — three defensible answers, spread across the whole
file:

| reading | partial total |
|---|---|
| a file-scope rejection ends *the file's* enumeration, as a layer's ends the layer's | **704** (= F; everything discarded) |
| the walk completed (overlap detection needs whole-directory knowledge), so report the exact complement | **47** |
| sum-of-lengths | −47 (barred, §2.3 above) |

The same fork appears, with different numbers, on **F20**: the directory CRC
fails, the live trailer *is* established (so §5.2's "not owed at all" escape
does not apply), and the walk cannot enumerate a single record extent. Is the
total F − (16 + dir_length + 64), or F? This is **verifier-01**.

### 2.5 Multi-generation trace

Same layer, four generations. Every number below is computed, not estimated.

**g1 — creation.** As §2.2. F = 704, claimed 785 − 128 = 657, **slack 47
(6.7%)**. Verdict **conforming**.

**g2 — append: store tile 3.** Tile 3's 28 padding positions must each encode
the recorded fill `00 00 C0 7F` (`[R-SER-05]`); I built it that way and the
verifier's T4 check passes. New payload `[704,832)`, new index region
`[832,916)` (`[R-LIF-01]` forbids overwriting the old one), new directory
`[916,1025)`, pad `[1025,1088)`, trailer `[1088,1152)`. F = 1152.
Claimed = 16 + 4·128 + 84 + 109 + 64 = 785. **Slack 367 (31.9%)** — the old
index (84), old directory (109), old pad (47), old trailer (64), new pad (63).
Verdict **conforming**.

**g3 — update: supersede tile 1.** New payload `[1152,1280)`, index
`[1280,1364)`, directory `[1364,1473)`, pad `[1473,1536)`, trailer
`[1536,1600)`. F = 1600, claimed still 785. **Slack 815 (50.9%)**. Verdict
**conforming** — and this is the number §5.2 says is "what tells an operator to
compact", now past half the file.

I checked g3 against §20.3 step 4's bar: the commit changes no declaration, so
nothing §14 fixes for a tile stored in the superseded generation moves. Also
against §20.4: the single layer record is *modified* (its extent slot moves),
so it is new output, not a byte-identical re-emission — and nothing is dropped.

**g4 — compaction.** Fresh file_id, generation 1, every stored tile's bytes
verbatim, index region regenerated with new offsets and unchanged
lengths/crcs, crc_of_crc_array updated (`[R-WRT-07]`).

```
[0,16) front | [16,144) t0 | [144,272) t1' | [272,400) t2 | [400,528) t3
             | [528,612) index | [612,721) directory | [721,768) pad
             | [768,832) trailer      F = 832
```

Claimed 785, **slack 47 (5.6%)** — the pre-trailer pad again, so "slack is
never carried" holds in the sense §20.5 means it (the *input's* slack is not
carried; the output still has its own pad, as §20.5's own figure shows).
Verdict **conforming**.

Slack ratio by generation: 6.7% → 31.9% → 50.9% → 5.6%.

I also confirmed the compactor's regeneration dichotomy is exhaustive over
§15.3: every entry is a sentinel (re-emitted unchanged), a structural
reject-tile (no stored extent to re-point → `[R-WRT-06]` obliges refusal), or
well-formed (re-pointed). A crc-failing entry falls in the third class, is
re-pointed — and is caught anyway, because `[R-WRT-09]` obliges verifying
"every stored tile's entry crc" before emitting its bytes. The pieces fit.

---

## 3. Extent overlap, alignment, and slab, on adversarial layouts

### 3.1 Overlap trichotomy

§7.2 gives three outcomes and I exercised each:

- both structures in one layer → **reject-layer, L18**. §2.3 above.
- one in a layer, the other elsewhere (other layer, other scope) →
  **reject-file, F33**. §2.4 above.
- neither in a layer (e.g. the directory against a top-level record's extent) →
  **reject-file, F33**.

I checked the boundary cases F33's row itself flags: a claimant reaching the
front block or the trailer is *not* F33 but the bounds rows — F9/F10 for the
directory, F31/F32 for a top-level extent, L16/L17 for a layer or sub-record
extent, T8/T9 for a stored tile. So an extent at offset 8 is T8, not "overlaps
the front block". That is a genuinely useful disambiguation and it is stated.

I also checked an intra-layer overlap that involves no stored tile — a layer's
index region against its own user-metadata sub-record extent. §7.2's "an
intra-layer overlap" is general, and L18's instance list names "tile-index
region; layer sub-record extents", so it is covered.

### 3.2 Alignment, isolated

A = 512 declared; stored-tile offsets 512, 1024, **1600**. 1600 mod 512 = 64 →
**L40** (verifier, reject-layer). Nothing else fires: `[R-SLB-01]` constrains
only stored tiles' offsets, so the index region and record extents may sit
anywhere. The gap `[640,1024)` between tile 1's end and tile 2's start is
slack, and no rule constrains it.

### 3.3 Slab, isolated, and the three transparency rules

To get a vector exercising exactly one row I had to pick A_slab deliberately:

- **L41 only**: S = 3, **A_slab = 1** (so L42 can never fire — every offset is
  1-aligned). Run `[0,3)` at offsets 1024 (len 100), **1200**, 1300. Packing
  requires 1124; 1200 ≠ 1124 → L41's *gap* instance, alone.
- **L42 only**: S = 3, A_slab = 1024. Run `[0,3)` at 1500 (len 100), 1600,
  1700. Packing holds; 1500 mod 1024 = 476 → L42, alone.

Then the interesting one — §16.2's three transparency rules on one run
partition. Interleaved, N = 8, S = 3, A_slab = 64; runs `[0,3)`, `[3,6)`,
`[6,8)`:

| ord | state | off | len |
|---|---|---|---|
| 0 | stored | 64 | 20 |
| 1 | **sentinel** | — | — |
| 2 | stored | 84 | 20 |
| 3 | **length = 0, non-sentinel** (T10, *structural*) | — | — |
| 4 | stored | 128 | 20 |
| 5 | stored | 148 | 20 |
| 6 | stored, **bytes fail crc** (T1) | 200 | 20 |
| 7 | stored | 220 | 20 |

- Run 0: ordinal 1 is a sentinel — "transparent to run continuity: they occupy
  no bytes and do not break packing". First stored = 64, 64 mod 64 = 0 ✓;
  84 = 64 + 20 ✓. Clean.
- Run 1: ordinal 3 is structurally rejected — "So are the entries §15.3
  classifies reject-tile on a *structural* ground: they address no usable
  extent, and the run's stored tiles close over them." First stored = ordinal 4
  at 128, 128 mod 64 = 0 ✓; 148 = 128 + 20 ✓. Clean.
- Run 2: ordinal 6's only defect is its stored bytes' crc, and §16.2 is
  explicit that this one is **not** transparent — "its offset and length stand,
  and the packing relation reads them as it does any other stored tile's". So
  the run's first stored tile is ordinal 6 at 200, and 200 mod 64 = 8 →
  **L42**. Packing 220 = 200 + 20 holds, so L41 does not fire.

Result: layer → reject-layer (L42); tile 6 → reject-tile (T1); verdict
nonconforming; the layer's claimants are discarded from the walk
(`[R-CNT-21]` names "L40 through L42's placement" as walk-established
rejections), so the slack total is partial.

That distinction — structural-reject entries transparent, crc-failing entries
not — is stated three times (§15.3's closing paragraph, §16.2, §9.7) and each
statement agrees. It is the single sharpest piece of drafting I met, and it
resolves a question I would otherwise have had to guess: whether a crc-failing
tile makes the coverage walk incomplete. It does not — its extent is
enumerated. I note that `[R-CNT-21]`'s general clause, "a scope-level rejection
ends that scope's enumeration", read at *tile* scope, would say the opposite;
but the specific text wins three-to-one and the parenthetical that follows it
speaks only of layers. Not reported as a defect — reported instead as the
*absence* of that specific text at file scope, which is verifier-01.

### 3.4 Other slab checks I ran

- S > N: N = 5, S = 8 → block `[0,5)`, one run covering all five. "the final run
  of a block can cover fewer than S ordinals" ✓.
- Planar blocks: C = 3, N = 5, S = 2 → runs `[0,2) [2,4) [4,5)` per block, never
  spanning `[5,10)` or `[10,15)` ✓.
- Runs need not be mutually ordered in byte space; between them
  `[R-SLB-05]`'s freedom governs, and `[R-CNT-13]`'s no-overlap still catches
  a run placed inside another.
- A run with no stored tiles imposes nothing; a layer with E = 0 has no runs.
- `[R-CNT-16]` bars A ≠ 0 with S ≠ 0 (L20); `[R-CNT-23]` bars A_slab ≠ 0 with
  S = 0 (L28).
- A compactor **cannot** clear a slab declaration the way `[R-SLB-04]` lets a
  committing writer: `[R-WRT-07]` re-emits every retained record and changes
  only extent slots and crc_of_crc_array, so it must re-establish the
  invariants. It always can, since it controls placement. Consistent.

---

## 4. Decoded-content obligations

**Must decode.** Every stored tile (§9.7, and the MUST NOT that backs it).
Every user-metadata document under an assigned encoding (§2.3 + `[R-MTA-09]`).

**Must compare against.**

| Decoded thing | Compared against | Row |
|---|---|---|
| decoded payload length | the layer's declaration-derived decoded size | T3 |
| every padding position, each channel | that channel's recorded fill bytes / byte / bit | T4 |
| pad bits of a packed bool plane (P mod 8 ≠ 0) | the plane's channel's fill bit | T5 |
| every interleaved bool byte at a real position | `0x00` or `0x01` | T2 |
| stored-byte consumption | exactly the entry's length | T24 |
| stream/frame/block well-formedness | the declared codec | T25, T15–T23 |
| codec 1 entry length | the decoded size | T14 |
| metadata object members | ascending decoded-key UTF-8 byte order | F27, L48 |
| decoded document | §18.2's four restrictions | R5–R10 |

**Permitted to skip.** The *values* at real sample positions — §21.7 ¶1 is
unambiguous that a well-formed tile carrying wrong data "every checksum in §8
certifies". The content of an unassigned-encoding metadata document
(`[R-MTA-10]`). The content of an unassigned-type record extent (§8.1, §22.3).
Slack content (§5.2). `[R-MTA-07]`'s standardized-key placement and value
shapes — and §18.4 says why, in terms: "enforcing them would put a verifier to
work on the content of metadata, which §21.6 declares a non-violation rather
than a check any actor owes."

I confirmed T2 and T4 jointly cover every interleaved bool byte (T2's row says
so; T4 catches a bad byte at a padding position because a bool fill byte is
constrained to `0x00`/`0x01` by `[R-TYP-07]`), and that the byte-shuffle stride
rule composes: L = P·Q, P·Bᶜ, or ⌈P/8⌉, each divisible by its stride, with the
packed-bool case degenerating to the identity at s = 1.

---

## 5. Findings

Nine. Two are in text nobody flagged (verifier-01, verifier-05); four are in
the four named sections; three sit across the two. None is byte-level, and I
say for each why not — a verdict fork I could construct would have been the
most valuable thing I could return, and I did not find one that survives a
competent reading.

---

### verifier-01 — AMBIGUITY. A file-scope rejection's effect on the coverage walk is unstated, and the three readings differ by the whole file.

**Location.** §5.2 `[R-CNT-21]`; §9.7 `[R-LIF-08]`.

**Quotation.** §5.2:

> Where the walk of §9.7 does not enumerate every region's claimants — whether
> because a scope-level rejection ends that scope's enumeration (a rejected
> layer's claimants are not enumerated, whether or not the rejection impeded
> reading them — and where the rejection is one the walk itself established,
> L18's overlap or L40 through L42's placement among them, the claimants it had
> already enumerated are discarded with the layer, since the total is a claim
> about a live state one of whose layers is not usable), or because the verifier
> elected under `[R-CNF-11]` to stop at the first violation — the verifier MUST
> report the total as partial.

**Detail.** The governing clause is stated at *scope* generality — "a
scope-level rejection ends that scope's enumeration" — and §2.4 fixes three
scopes: file, layer, tile. The parenthetical then works out the **layer** case
in full, including the discard rule. §9.7 works out the **tile** case in full,
twice ("an entry `[R-IDX-03]` classifies reject-tile on a *structural* ground
contributes no stored extent to the walk; one whose stored bytes alone fail its
crc keeps its extent"; "does not make the walk incomplete"). The **file** case
is worked out nowhere, and §5.2's only file-scope carve-out is the pre-trailer
one — "Where §6.2's ordered validation rejects the file before a live trailer
is established there is no F and no live state to walk" — which by construction
covers only failures *before* the trailer is established.

So for a reject-file established after the trailer, three readings are open:

1. **Uniform.** Apply the general clause at file scope: the file's enumeration
   ends and, since the walk itself established the rejection, "the claimants it
   had already enumerated are discarded" — with the file, now, rather than with
   a layer. Partial total = F − 0 = **F**. The stated justification supports
   this ("the total is a claim about a live state one of whose layers is not
   usable" generalises to *whose file is not usable"), and it keeps the
   upper-bound promise trivially.
2. **Complete-walk.** The parenthetical's discard rule is written for layers
   only; F33 in particular cannot be established until the walk has enumerated
   everything, so the walk *did* "enumerate every region's claimants" and the
   antecedent is false. Total is **exact**: F − |union of claimants|.
3. **Keep-and-flag.** Retain what was enumerated, report the total as partial,
   and name F33 as what stopped the walk.

On the two-layer file I built (A's tile 2 at `[272,400)`, B's tile at
`[390,518)`, ten bytes of cross-layer overlap, F = 704), reading 1 reports
**704**, readings 2 and 3 report **47**. The same fork with different numbers
appears on F20: a directory whose CRC fails leaves the live trailer established
(so the "not owed at all" escape is unavailable) and no record extent
enumerable; reading 1 gives F, readings 2/3 give F − (16 + dir_length + 64).
It also appears on F4 (duplicate layer name, established at open) and F7
(structure in the pre-trailer gap).

**I picked reading 3** for my verifier: it is the only one that is both never
an under-count and never vacuous, it preserves §5.2's "tightening to the exact
total when the walk completes" as a meaningful statement, and it satisfies the
MUST to "say which scope or violation stopped the walk" — a clause that has
nothing to name under reading 2 and everything to name under reading 1.

**What an implementer does wrong without it.** Reports F as the slack total for
any file with a post-trailer file-scope violation, which §22.3 leans on as "the
number that distinguishes a working file from a padded one" — and which an
operator reads as "this file is entirely waste". Or reports an exact total on a
walk whose completeness the document never granted.

**Byte-level?** No. Every reading yields the same verdict (*nonconforming*),
because the rejection that raises the question is itself an established
violation. The divergence is confined to a mandatory report field, so no byte
sequence changes its emittability and no file changes its accept/reject
outcome.

---

### verifier-02 — AMBIGUITY. §21.7's "None of these" disclaimer sits in the first paragraph; the list that needs it is in the second. Read narrowly, no file is ever certifiable.

**Location.** §21.7, `[R-ERR-01]`.

**Quotation.** End of ¶1:

> None of these is a requirement a verifier is *unable to check* within the
> meaning of `[R-CNF-11]`: no file-level witness exists to check, so nothing
> about the file is left undetermined and the verdict is unaffected.

Opening of ¶2:

> A second set of obligations is omitted from the register because a single file
> exhibits no witness of their violation.

**Detail.** ¶1's subject is content-incorrectness: a mis-strided filter, an
undisclosed dictionary, "or simply wrong data". "None of these" takes that as
its antecedent. ¶2 then introduces a *different* and much larger set —
`[R-LIF-01]`, `[R-LIF-03]`, `[R-GEO-06]`, `[R-SER-01]`, `[R-CNT-13]`'s
no-embedded-offsets prohibition, `[R-CNT-18]`'s nesting prohibition, §20.3
step 4's bar, `[R-WRT-06]`'s two trailer obligations, `[R-ENC-06]` — and
carries no disclaimer of its own. Two readings:

- **Broad** (disclaimer covers §21.7 entire): none of ¶2's obligations is an
  "unable to check" ground; the verdict is unaffected; certification proceeds.
- **Narrow** (disclaimer covers ¶1 only): each of ¶2's obligations is a
  file-level requirement (§2.3 obliges a verifier to check "every file-level
  requirement") that the verifier cannot check. `[R-CNF-11]` then makes each an
  unchecked requirement, which must be reported and — absent an established
  violation — fixes the verdict as *cannot establish*.

The narrow reading is catastrophic, and that is what makes it worth reporting
rather than shrugging at. `[R-GEO-06]` and `[R-SER-01]`'s ordinal mappings are
"satisfied by a structurally valid tile whatever values it carries" — so every
file with a stored tile has an unverifiable requirement. `[R-CNT-13]`'s
prohibition is "opaque by construction" — so every file with an MU = 0 record
does. `[R-CNT-18]`'s nesting prohibition — every file with a sub-record. Under
the narrow reading the verdict *conforming* is unreachable for any file richer
than Appendix A's empty one, which contradicts §21.1 ("a verifier certifies
only violation-free files"), §24's corpus of conforming vectors, and Appendix
H's checklist.

**I picked the broad reading.** But the placement is the wrong way round: the
sentence that disclaims is attached to the shorter, more obvious list, and the
longer list that actually needs it follows it.

**What an implementer does wrong without it.** Builds a verifier that returns
*cannot establish* for every nontrivial file, with a report naming six
requirements it cannot check — and, reading `[R-CNF-11]`, believes it is right.

**Byte-level?** No, on the discriminator this project uses. The narrow reading
is not a *competent* reading: it is refuted within the document by three
independent statements that certification of a conforming file is expected.
Two competent implementations do not diverge here. It costs an implementer
reading time, not bytes.

---

### verifier-03 — AMBIGUITY. Appendix G item 6 is not marked a creator's rule, and a compactor cannot obey it; the new concession's "only modulo its trailer" depends on which way that goes.

**Location.** Appendix G, items 2, 6 and 8; §20.5 `[R-WRT-07]`.

**Quotation.** Appendix G item 6:

> 6. **The sentinel for every all-fill tile**, so that a tile whose samples all
> equal fill is never stored; otherwise two writers agreeing on content still
> disagree on bytes.

§20.5 `[R-WRT-07]`:

> A compactor preserves content but not placement — ... : every stored
> tile's bytes verbatim — each index entry's crc is unchanged — and every
> retained record per §20.4, except that relocation re-points extent slots,
> regenerates each relocated tile-index region (entry offsets new; entry
> lengths, entry crcs, and sentinel entries unchanged; segment CRCs recomputed
> over the entries as re-emitted) ...

Appendix G item 8's concession:

> A compactor's output is therefore reproducible only modulo its trailer:
> `[R-WRT-06]`'s fresh file_id is no function of content, and this item's floor
> turns on which features the compactor implements.

**Detail.** The appendix contemplates compactors adopting the profile and
carves items out for them where they cannot comply: item 2 ("This is a
creator's rule: a compactor adopting the profile takes `[R-WRT-06]`'s fresh
draw instead"), item 8 ("The `flags` half is a creator's rule, as item 2's
identifier is"). Item 6 gets no such marking, and a compactor cannot obey it.
Given an input storing a tile whose samples all equal fill, `[R-WRT-07]`
requires that tile's bytes verbatim with its entry length and crc unchanged;
converting it to a sentinel would change both. Nor is dropping available —
§20.5 licenses dropping only *records* §20.4's table names, and a stored tile
is no record. So:

- **Reading A** (item 6 is a creator's rule, unmarked): a profile-adopting
  compactor inherits its input's stored-tile set, item 6 is vacuous for it, and
  the concession's "only modulo its trailer" is exactly right — two
  profile-adopting compactors given the same input file agree outside the
  trailer.
- **Reading B** (item 6 binds every adopter, as its unmarked text says): a
  compactor whose input stores an all-fill tile cannot adopt the profile at
  all, and the concession understates the gap — the divergence is not confined
  to the trailer, since a profile-conformant creator and a profile-adopting
  compactor produce different index regions and different stored-tile sets from
  the same logical content.

**I picked A**, on the strength of items 2 and 8 establishing that the appendix
marks creator-only items when it means them, plus `[R-WRT-07]`'s normative MUST
outranking a non-normative appendix under §2.1. But the marking is exactly what
is missing, and the concession that was added to bound the compactor's
irreproducibility is the sentence that makes the gap visible.

**What an implementer does wrong without it.** Writes a profile-adopting
compactor that sentinels all-fill tiles, violating `[R-WRT-07]` — a normative
MUST — in pursuit of a non-normative appendix. Or, more likely, wastes an
afternoon deciding it cannot.

**Byte-level?** No. §2.1 makes Appendix G non-normative and the appendix says
so itself ("It adds no requirement to any actor: a writer ignoring it is fully
conforming"), so `[R-WRT-07]` governs and no conforming compactor's output
bytes are in doubt. The cost is to the profile's own claim, not to the format's.

---

### verifier-04 — OBSERVATION. `[R-CNF-02]` claims to enumerate the conduct cases; §21.7 ¶2 lists obligations that cannot be byte predicates and are not in that enumeration.

**Location.** §2.3 `[R-CNF-02]`; §21.7 `[R-ERR-01]`; §6.3 `[R-CNT-08]`;
§20.5 `[R-WRT-06]`.

**Quotation.** §2.3:

> A writer obligation whose violation this specification expressly declares not
> to be a file-conformance violation binds the actor in the same way; §6.3's
> flags = 0 against a set ignore-lane bit and §6.2's pre-trailer gap longer than
> `[R-LIF-02]` step 5's pad are the cases this text states, and each is declared
> where it arises rather than enumerated here.

§20.5:

> The output trailer MUST copy the input's unknown ignore-lane flag bits
> forward, in place of the flags = 0 §6.3 requires of a file created under this
> text (`[R-CNT-08]`).

**Detail.** Take bytes **B**: a well-formed file, generation 1, `flags = 0`.
A creator emitting B is conforming — §6.3: "a writer creating a file under this
text MUST write flags = 0". A compactor that produced B from an input carrying
ignore-lane bit 16 has violated `[R-WRT-06]`'s MUST. §2.3 says file conformance
"is a pure predicate on bytes: it does not depend on any reader, writer, or
environment", so B cannot be both conforming and nonconforming; B is
conforming, and therefore `[R-WRT-06]`'s carry-forward obligation is not a
file-conformance requirement at all. It is a conduct rule — and it lacks the
"express declaration" `[R-CNF-02]` requires of one, and is absent from the list
that says "are the cases this text states".

§21.7 instead files it under the no-witness class, whose opening frames its
members as violations that happen to be unwitnessed: "A second set of
obligations is omitted from the register because a single file exhibits no
witness of their violation." The same argument applies to `[R-LIF-01]`
(committed-prefix immutability: a file mutated in place can be byte-identical
to one built by a legal commit) and `[R-LIF-03]` (the generation sequence).
§21.7's ¶2 therefore mixes two kinds — byte predicates with no practical
witness (`[R-CNT-13]`'s embedded offsets, `[R-CNT-18]`'s nesting) and conduct
obligations that are not byte predicates at all — and `[R-CNF-02]`'s enumeration
does not admit the second kind.

**I picked**: treat `[R-WRT-06]`'s two trailer obligations, `[R-LIF-01]` and
`[R-LIF-03]` as conduct, so that B stays conforming and the pure-predicate
clause survives. My verifier therefore does not list them among the file-level
requirements it owes a check on.

**What an implementer does wrong without it.** A verifier that takes §21.7 ¶2
at its word — these are violations, merely unwitnessed — has, combined with
verifier-02's narrow reading, a reason to never certify. Separately, a
`[R-CNF-05]` audit of a compactor gets the count of violations wrong, which
matters only to a tool that counts them.

**Byte-level?** No. No verifier can distinguish B's two provenances, so no
accept/reject verdict moves; and the compactor is bound by the MUST under
either classification, so no emitted byte moves either.

---

### verifier-05 — OBSERVATION. A verifier must name every requirement it could not check, and is nowhere obliged to name a violation it did establish.

**Location.** §2.3 `[R-CNF-11]`; §2.4; §21.1.

**Quotation.** §2.3:

> A verifier MUST report each requirement it was unable to check on a capability
> or resource ground, naming the requirement and the ground, whichever of the
> three verdicts it reports

and, for the other half of the report:

> A verifier MAY stop at the first violation it finds; one that does MUST report
> each scope it did not examine as *unexamined*, which is not a finding that the
> scope is clean.

**Detail.** I assembled every verifier reporting duty in the document (the
table in §1.3 of this transcript). The document is precise about what the
verifier could **not** do: unchecked requirements by name and ground, unexamined
scopes, the slack total with what stopped the walk, each metadata record
ignored at an unassigned encoding with its scope/encoding/extent length, a
resource refusal distinguished from corruption, the bound applied to a declined
document. It requires naming a violation in exactly one place — `[R-MTA-05]`'s
unsorted document, "the file is nonconforming, a verifier MUST report it" —
and nowhere generally. A verifier whose entire output for my adversarial file
is the single token `nonconforming` satisfies every requirement I can find,
while a verifier that reports only `cannot establish` does not.

The counter-argument, which I weighed and did not find sufficient, is §2.4's
Note: "'Reject' prescribes the scope of unusability, not user interface: how
failure is reported is implementation technique." That Note is about the
outcome classes and readers' handling of them. It sits oddly against a section
that then mandates the *content* of a verifier's report in six other respects,
and against §24 `[R-VEC-02]`, which requires a corpus manifest to record "the
outcome class (§2.4), the scope, and the §21 register row it exercises together
with that row's governing requirement identifier" — precisely the pair a
verifier is not obliged to emit, so a corpus runner cannot check a verifier's
finding against a vector's expectation using anything the verifier owes it.

**I picked**: report the row identifier, the governing requirement identifier,
the scope, and the byte range for every established violation, on the model of
`[R-VEC-02]`'s manifest pair — but I recorded that I was choosing, not
following.

**What an implementer does wrong without it.** Ships a conforming verifier that
is useless for the job §22.3 assigns it ("a pipeline accepting files from
untrusted sources SHOULD verify rather than merely read"), and a corpus harness
that cannot tell whether a verifier found the row the vector was built for or a
different one.

**Byte-level?** No — report content only, and no file's verdict changes.

---

### verifier-06 — OBSERVATION. `[R-MTA-10]`'s "counted and named, never silent" is not carried to the one live-byte class covered by no checksum at all.

**Location.** §8.1 `[R-CNT-19]` (final table row); §18.2 `[R-MTA-10]`;
§22.3 `[R-SEC-04]`; Appendix H's verifier checklist.

**Quotation.** `[R-MTA-10]`, on the metadata case:

> it MUST report each record it ignored on this ground, naming the owning scope,
> the encoding value, and the stored extent length, as it reports the slack
> total (`[R-CNT-21]`): bytes a certificate covers without inspecting are
> counted and named, never silent.

§22.3, on the parallel case:

> The extent of a record of a type this specification has not assigned is
> covered by no checksum either (§8.1), so corruption inside it is equally
> invisible: §20.4's byte-identical re-emission (`[R-WRT-05]`) carries such an
> extent forward unread, and `[R-WRT-08]` bars re-encoding it, so nothing an
> updater does would surface the damage.

**Detail.** Partitioning the certified file's bytes (this transcript, §2.1) I
found exactly two live classes a certificate covers without inspecting their
content: an unassigned-encoding metadata extent, and an unassigned record
type's extent. The second is strictly *weaker* — §8.1's last row gives it
"none — the bytes are opaque", so it carries no checksum either, where the
metadata extent at least has its terminal CRC (`[R-CNT-20]`). The document
states the principle in `[R-MTA-10]`, applies it to the stronger case, notices
the weaker case in §22.3, and imposes no naming duty there; Appendix H's
verifier checklist likewise names the metadata report and not this one. So the
class of live bytes a verifier certifies with the least evidence is the class it
need never mention.

I could construct no reading on which a naming duty exists, so this is not an
ambiguity: it is decidable, and the answer is that no duty exists. It is
expensive to *notice*, which is why I record it — reaching it required
partitioning the coverage classes by evidence rather than by structure kind,
and §22.3's own framing ("Four residues are stated rather than defended") is
the closest the document comes to acknowledging it.

**I picked**: report unassigned-type record extents on the same three fields
(owning scope, type value, stored extent length) as `[R-MTA-10]` requires for
metadata, as an extension beyond what is owed.

**What an implementer does wrong without it.** Emits a certificate over a file
in which an arbitrary, unchecksummed, uninspected, unmentioned byte range of
any size rides along — precisely the smuggling channel §22.3's last sentence
tells an operator to police "on that report line", for the residue that has one.

**Byte-level?** No. The file is conforming either way and the verdict is the
same; only the report differs.

---

### verifier-07 — AMBIGUITY. §23.1's new two-way enumeration turns on whether "superseding" is broad, and §20.3 step 4 uses it narrowly.

**Location.** §23.1 `[R-PRV-01]`; §20.3 step 4 `[R-WRT-04]`; §23.2 `[R-PRV-03]`.

**Quotation.** §23.1:

> A commit removes sample data two ways — superseding it, and a shrink that
> de-addresses tiles (§20.3 step 4) — and a dropped ancillary record's extent
> (§20.4) goes the same way; no commit removes a layer at all.

§20.3 step 4, distinguishing the two in its own vocabulary:

> with entries for tiles this commit stores or supersedes written to their new
> state, entries for tiles that become unstored written as the sentinel

**Detail.** A commit can make a stored tile's payload unreachable in a third
way: writing the sentinel for a previously-stored entry without shrinking any
extent. §20.3 step 4 names that operation separately from superseding, in a
list where the contrast is doing work. §23.2 then names it as its own case and
cites §23.1 for the consequence — "a tile unstored by a later commit leaves its
earlier payload in the file as slack (§23.1)" — pointing at a section whose
enumeration does not use that word.

- **Broad reading** of "superseding it": any commit whose new generation no
  longer reaches the old payload, unstoring included. Supported by §5.2's
  "everything an earlier commit superseded" and by step 4's own closing
  "Extents this commit supersedes become slack".
- **Narrow reading**: replacement of a stored tile's bytes at one disk ordinal.
  Supported by step 4's contrast above and by §3.1's "Superseded payload bytes
  from earlier generations do not make a tile stored".

Under the narrow reading the enumeration is short one item, in a passage whose
whole point is to enumerate exhaustively.

**I picked the broad reading**, and note that nothing normative is lost either
way: the requirement `[R-PRV-01]` carries is quantified over the general case,
not over the enumeration — "Writers and the tools built on them MUST NOT
represent **any commit that makes sample data unreachable** as erasure of it" —
so an unstoring commit is bound whichever reading of the enumeration one takes.

**What an implementer does wrong without it.** A tool author auditing its own
UI against §23.1 checks its supersede path and its shrink path, and leaves an
"unstore" or "clear tile" operation reporting erasure — the exact
misrepresentation `[R-PRV-01]` exists to bar, missed because the enumeration
that preceded the rule read as complete.

**Byte-level?** No, twice over: `[R-PRV-01]` constrains what a tool *says*, not
what it writes, and the requirement's own scope already covers the case the
enumeration may not.

---

### verifier-08 — OBSERVATION. §20.5's closure argument miscounts against §21.6 unless silently restricted to minor-defined values.

**Location.** §20.5 `[R-WRT-06]`; §21.6's table; §10.1, §10.3.

**Quotation.** §20.5:

> Where the output carries a feature a later minor defines and this compactor
> does not — on a conforming input a carried ignore-lane bit (§6.3) or an
> unrecognized `tarn.` key in a record it never decoded (§18.3), the two of
> §10.1's four vehicles §21.6 makes conforming, the other two reaching such a
> file only as values this text still registers as reserved-range violations
> (F36, L25, R1) — the output's version_minor SHOULD be at least the input's

**Detail.** I checked the closure argument rather than the enumeration, since
the enumeration is only as good as the argument. §10.1's four vehicles are new
record types, new reserved-range values, new ignore-lane bits, new standardized
metadata keys. §21.6's table makes instances of **all four** conforming, not
two:

- vehicle 1 — "A record type this specification has not assigned, from the
  experimental range (≥ 0x8000, §10.2), carries MU = 0 | Ignored ...";
- vehicle 2 — "A user-metadata record declares an experimental-range (≥ 0x80)
  document encoding | Ignored (ignore-record); the file is conforming";
- vehicle 3 — "An ignore-lane flag bit (16–31) is set | Ignored; the file is
  conforming";
- vehicle 4 — "A user-metadata document carries an unrecognized
  `tarn.`-prefixed key | Conforming".

So "the two of §10.1's four vehicles §21.6 makes conforming" is wrong as
written, and "the other two reaching such a file only as values this text still
registers as reserved-range violations" is wrong as written too — vehicles 1
and 2 also reach a conforming file, as experimental values.

The conclusion nevertheless holds, by a step the passage does not take: §10.3
makes experimental values private use, so they are never "a feature a later
minor defines", and the antecedent excludes them. Read with that restriction
silently applied to the parenthetical as well as to the antecedent, both counts
become correct. The parenthetical's row citation is also partial on its own
terms: a later minor's new reserved-range value reaches a file under this text
as L31, L33, L34, L36, L43 or L45 as well as F36, L25 and R1, six rows the
citation omits.

**I picked**: the scoped reading, and confirmed the enumeration is closed —
on a conforming input the only later-minor features a compactor may not
implement are a carried ignore-lane bit and an unrecognized `tarn.` key. My
compactor therefore takes the input's version_minor as its floor unless it can
show neither is present, which for the key it cannot, since `[R-WRT-09]`'s
depth "reaches no decoded content".

**What an implementer does wrong without it.** Checks the closure claim against
§21.6's table, finds four conforming vehicle-instances where the text says two,
and either concludes the enumeration is unsound (it is not) or that experimental
values must be carried into the version_minor floor (they must not — a minor
never defined them, so there is no floor for them to raise).

**Byte-level?** No, on this project's own SHOULD discriminator: the obligation
the enumeration serves is `[R-WRT-06]`'s "the output's version_minor **SHOULD**
be at least the input's". `[R-CNF-12]` places SHOULD deviation outside the
register, so however the closure question resolves, the emittable set is
unchanged. The cost is one implementer's afternoon.

---

### verifier-09 — CONTRADICTION. §21.7 says the §20.3-step-4 bar is witnessed "only where" content is constrained, then names two other witnesses in the same sentence.

**Location.** §21.7 `[R-ERR-01]`.

**Quotation.** One sentence, two clauses:

> §20.3 step 4's bar on a declaration change is witnessed only where the
> affected tiles remain stored *and* the change reaches a byte §14 structurally
> constrains — a padding position, a pad bit, or a boolean byte — where §21.4's
> content rows fire;

> a change that reaches the decoded size instead is witnessed by T3 or T14,
> which test a length rather than the decoded image's content — T14 the entry's
> declared length, T3 the decoded payload's own; a change that reaches the codec
> is witnessed by the rows for the codec now declared, which test the stored
> bytes as a stream of it (T15, T17, T23, T25), or by T14 where the new
> declaration is codec 1

**Detail.** The first clause states two jointly necessary conditions for the bar
to be witnessed, the second of which is that the change reach a byte §14
structurally constrains. The clauses that follow describe witnesses that meet
neither half of that second condition — T3 and T14 "test a length rather than
the decoded image's content", and T15/T17/T23/T25 test stream framing. So a
commit that, say, re-declares codec 1 as codec 3 over an unchanged stored tile
is witnessed (T17, missing frame magic) without reaching any padding position,
pad bit or boolean byte, and the "only where" is false on the sentence's own
next clause.

A charitable parse exists: read the "only where" as scoped to the content-row
witness — "witnessed [by §21.4's content rows] only where ..." — with the
trailing "where §21.4's content rows fire" supplying that scope retroactively.
Under that parse the sentence is consistent. Nothing marks the scope, and the
word "instead" opening the next clause reads as contrasting with the whole
preceding claim rather than with one unstated bracket of it.

**I picked** the scoped parse, since it is the only one on which the sentence is
true. I verified the account it gives is otherwise complete against §20.3
step 4's own list of four effects (padding set/content → T4, T5; decoded size →
T3, T14; sample byte offset within the image → content rows only; codec and
filter → the codec rows, with a *filter*-only change falling back to the content
rows, which §21.7 does not say but which clause 1 covers).

**What an implementer does wrong without it.** Builds the conformance corpus
from §21.7 and omits vectors for declaration changes that move the decoded size
or the codec, believing them unwitnessed — though §21.7 then tells them
otherwise three clauses later, which is why I grade this low.

**Byte-level?** No. §21.7 is an account of what no check detects; it imposes no
check and licenses no emission. Every row it names (T3, T4, T5, T14, T15, T17,
T23, T25) is checked by my verifier regardless of how the "only" is read.

---

## 6. Where the document did determine things, and it mattered

Recorded because a walk that only lists complaints misreports the document.
These are places I expected to have to guess and did not:

- Whether a verifier decodes tiles in a layer with no padding and no bool
  channels. §9.7 answers directly, and the MUST NOT that carries it is exactly
  strong enough.
- Whether a crc-failing entry is transparent to slab run continuity, and
  whether it drops out of the coverage walk. Stated three times, consistently
  (§15.3, §16.2, §9.7), and the *structural*/crc distinction is drawn in the
  same words each time.
- Whether the overlap outcome is layer- or file-scope, in all three
  configurations, and how it interacts with the bounds rows. §7.2, §15.3 and
  F33's own row agree.
- Whether the slack total is owed after a trailer-gate failure. §5.2's "not a
  partial total but the absence of one" is unusually careful and I used it.
- Whether an unassigned metadata encoding bars certification. `[R-MTA-10]`,
  §17.4's closing sentence, §21.5's preamble and §21.6's row all say no, and
  all say it the same way, while R1 keeps encoding 0 and the reserved range as
  violations.
- Whether §2.3's cannot-establish list is closed. "as when" settles it.
- Whether the register's completeness claim reaches §21.6/§21.7/§21.9. §21.1
  excludes them explicitly, and the instance arithmetic confirms the excluded
  sections contribute no rows.

## 7. Confidence

**Medium.** I could implement the certification procedure, the coverage walk,
the invariant checks, the checksum chain and the decoded-content checks from
this document alone, and I did — every number in §2 and §3 above is computed,
not estimated. The one place two implementations of *my* verifier would
disagree on an emitted number rather than a verdict is verifier-01, and it is a
mandatory report field on a file the document otherwise decides completely.
Nothing I found moves a byte or a verdict.
