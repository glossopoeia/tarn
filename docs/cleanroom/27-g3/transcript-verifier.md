# Cleanroom round 27 — Verifier implementer, working transcript

## 0. Disclosure of what I read and ran

I read exactly one file: `/Users/robertkleffner/Documents/GitHub/tarn/spec/tarn.md`
(4,549 lines — the brief says 4,550; `wc -l` reports 4,549, which is the same
document if the file lacks a terminal newline count or the brief rounded. I did
not investigate further, and I note it only because "paths and counts are context
too").

I ran, against that file only:

- `wc -l`, `grep`, `rg`-style `grep -o`, and two small `awk`/`python3` scripts
  that read that file and nothing else, to (a) enumerate every register row and
  count its instances, (b) enumerate every `[R-...]` identifier and look for
  numbering gaps, (c) find every blockquote that carries no *Note* / *Example* /
  *Rationale* label.
- Two `python3` scripts that read **no** files: a CRC-32C implementation, and an
  Appendix A hexdump transcribed by hand into the script from what I had read.

I opened no ADR, no `docs/`, no `PLAN.md`, no `AGENTS.md`, no `conformance/`, no
`spec/registry.json`, no git history. I ran no web search or fetch. I did not
list the output directory.

**Context I did not ask for.** Material was placed in my context before I began:
a project instruction file (`CLAUDE.md`, pointing at `AGENTS.md`), an index of
the maintainer's memory notes with descriptive titles, a `gitStatus` block naming
the current branch and the subject lines of the five most recent commits, and a
user email address. The commit subjects in particular name this round's number
and describe some of the edits. **I disregarded all of it**: I did not open any
file it named, and every conclusion below is derived from `spec/tarn.md` and my
own arithmetic. I flag it here because a disclosed breach is usable and a silent
one is not. Nothing in that material is quoted or relied on below.

---

## 1. What I built

I implemented, on paper, a conforming verifier: the certification procedure as an
ordered algorithm; the coverage walk with worked arithmetic on a file of my own
construction and again on a walk that does not complete; the extent-overlap,
alignment and slab checks on concrete adversarial layouts; the checksum
obligations with every stated constant recomputed locally; the decoded-content
obligations; and a four-generation trace (create → append → update → compact)
with the certification result at each step.

Two findings survived. One I grade byte-level.

---

## 2. Reading order and the conformance convention

I checked `[R-CNF-01]` against the document rather than assuming it. The
exemption is by **label**, not by the `>` marker:

> All text in this document is normative except: §1 (Introduction); any text
> labeled *Note*, *Example*, or *Rationale*; and appendices identified as
> non-normative. `[R-CNF-01]`

I ran an `awk` pass over every blockquote in the file, printing any whose body
carries neither a `**Note**` / `**Example**` / `**Rationale**` label nor the
words "non-normative". Exactly one came back — §15.1's index-region layout:

```
=== unlabeled blockquote at line 2071
> [ entry array: entry_count × 20 bytes ] [ segment CRC array:
> ⌈entry_count / 2¹⁶⌉ × 4 bytes ]
```

That block is normative. It agrees with `[R-CNT-17]`'s
`entry_count × 20 + ⌈entry_count / 2¹⁶⌉ × 4`, so I have no finding there, but I
recorded it because the brief warned that an earlier briefing in this project had
the rule backwards.

Also checked: the §2.2 prefix table (a presentation change the brief flags as
"asserted to carry the same content"). I extracted every `R-XXX` prefix actually
used in the document — CNF, CNT, COD, ENC, ERR, EXT, GEO, IDX, LIF, MDL, MTA,
PRV, RDR, SEC, SER, SLB, TYP, VEC, WRT: nineteen — and the table lists exactly
those nineteen. No prefix in the table is unused; no used prefix is missing. The
table's assertion of content-preservation holds on the only axis I can test from
the document alone.

Identifier hygiene: every prefix's numbering runs 1..max with no gaps
(`R-ENC-100` appears only as §2.2's own illustration of numbers above 99).
`[R-SER-04]` appears only in §14.4's withdrawal Note, not as a live assignment —
consistent with §2.2's retirement rule.

---

## 3. Checksum constants — every one I could compute

I wrote a CRC-32C (reflected Castagnoli, poly 0x82F63B78 reflected form,
init 0xFFFFFFFF, final XOR 0xFFFFFFFF) and checked it against §4.5's own check
vector before using it for anything.

| Constant | Stated where | Computed | Match |
|---|---|---|---|
| CRC-32C(`"123456789"`) = `0xE3069283` | §4.5, Appendix B | `0xe3069283` | ✅ |
| CRC-32C(zero bytes) = `0x00000000` | §4.5, §7.1, §5.1's Example, Appendix A | `0x0` | ✅ |
| §7.4's example: CRC over 80 bytes = 4 sentinel entries → `0x80A34955`, stored `55 49 A3 80` | §7.4 | `0x80a34955` → `55 49 a3 80` | ✅ |
| §7.4's example: `crc_of_crc_array` over that 4-byte array → `0xC4EE982E` | §7.4 | `0xc4ee982e` | ✅ |
| CRC of a full all-sentinel segment (2¹⁶ entries, 1,310,720 bytes) → `0xEECB3BB2` | §15.4, §21.3 L38, Appendix B | `0xeecb3bb2` | ✅ |
| Appendix A's trailer CRC over trailer bytes [0,60) → `0xE00938D2`, stored `D2 38 09 E0` | Appendix A | `0xe00938d2` → `d2 38 09 e0` | ✅ |
| Appendix A's directory region `00 00 00 00` = CRC of zero bytes | Appendix A | `0x0` | ✅ |

**Reproduced: all seven. Could not reproduce: none.** There is no stated checksum
constant in this document that I was unable to check locally.

Sentinel byte pattern used: `FF ×16 00 ×4` (`[R-IDX-02]`, Appendix B), 20 bytes,
matching §15.1's entry layout (offset u64, length u64, crc u32).

I also re-derived the non-checksum arithmetic in the same examples, since a
verifier has to do it anyway:

- §7.4's layer-record payload. Field-by-field offsets: name 0..3 (`03 73 73 74`
  = `sst`), layout 4, linearization 5..6, codec 7..8, filter 9..10, A 11..18,
  S 19..26, A_slab 27..34, d 35, C 36..37, dimension entry 38..55
  (`01 78` = `x`, extent 100 at 40, tile extent 32 at 48), channel entry 56..67
  (`04 74 65 6D 70 0C 00` then `04 00 00 C0 7F`), index_encoding 68,
  entry_count 69..76, crc_of_crc_array 77..80. **81 bytes exactly**, matching the
  document's "4 + 34 bytes ... the dimension entry 18, the channel entry 12, and
  the trailing fixed fields 13 — 81 exactly". The nine scalars from layout
  through channel count are 1+2+2+2+8+8+8+1+2 = 34 ✅. Extent slot length
  4×20 + ⌈4/2¹⁶⌉×4 = 84 ✅. The channel entry is byte-identical to §12.3's ✅.
- §15.4's worked example: entry_count 1,000,000 → 16 segments (15 full of 65,536
  = 983,040 entries, last covering 16,960), CRC array 64 bytes, region
  20,000,064 bytes ✅. Tile 999,999 → segment 15, segment-relative entry 16,959,
  byte 339,180 ✅; CRC array at [20,000,000, 20,000,064) ✅; segment 15 at
  [19,660,800, 20,000,000) = 339,200 bytes ✅; a full segment is 1,310,720 bytes
  = 1.25 MiB ✅.
- §15.4's planar example: C=4, N=32, channel 2 at spatial 10 → disk ordinal
  2·32+10 = 74, entry at region bytes [1,480, 1,500) ✅; channel 3's entries are
  96..127 ✅.
- §11.4's example: (300,700) with T=(256,256) → tile (1,2), s = 1·8+2 = 10;
  in-tile (44,188) → 44·256+188 = 11,452 ✅; planar C=4 → 2·32+10 = 74 ✅.
- §17.3's shuffle example: 1.0/2.0/3.0 float32 LE with s=4, n=3 gives
  `00 00 00 | 00 00 00 | 80 00 40 | 3F 40 40` ✅.
- §14.2's examples: Q=3, P=6 → 18 bytes, ordinal 5 at [15,18) ✅; planar `b`
  12 bytes, ordinal 5 at [10,12) ✅; float32+bool → Q=5, 30 bytes, ordinal 5 at
  [25,30) ✅.
- §14.3's example: P=10 → ⌈10/8⌉ = 2 bytes; alternating from true gives byte 0 =
  `0x55`, byte 1 = `0x01`, and with fill true the six pad bits set → `55 FD` ✅.
- §14.5's example: extents (5,5), tiles (4,4) → grid 2×2, edge tile (1,1) has one
  real position and 15 padding; uint16 → 32 bytes ✅.
- §20.3's example: 32-tile index region = 32·20 + 4 = 644 ✅.
- §5.1/Appendix A's 128-byte floor: front block ends at 16, dir_offset ≥ 16 and
  dir_length ≥ 4 put the directory end ≥ 20; `dir_offset + dir_length ≤ F − 64`
  gives F ≥ 84; F ≡ 0 (mod 64) gives F ≥ 128 ✅.

Everything the document states as a number, I could reproduce. That is a real
result about this document and I want it on the record: the arithmetic is clean.

---

## 4. The certification procedure, as an ordered algorithm

Assembled from §2.3 (`[R-CNF-11]`), §2.4 (`[R-CNF-12]`), §19.1–§19.4, §9.7
(`[R-LIF-08]`), §5.2 (`[R-CNT-21]`), §6.2 (`[R-CNT-05]`, `[R-CNT-06]`), §7.2,
§8.2, §15.3, §16, §17.4, §18.2 and §21.

A verifier is first a conforming reader: "Verifiers and updaters are readers of
the files they process and inherit every reader obligation." It additionally
"checks every file-level requirement — including those ordinary readers are
exempted from". So the algorithm is the reader's path with the verifier-only
checks spliced in, plus the coverage walk, plus the report.

**Verdict vocabulary.** Exactly three: *conforming*, *nonconforming*,
*cannot establish*. Two report-only labels ride alongside and are explicitly
**not** verdicts: the per-requirement "unable to check" report, and *unexamined*.

Availability rules I extracted:

1. Any **established violation** → *nonconforming*, "however many requirements it
   was unable to check". This dominates everything.
2. *cannot establish* "is available only to a traversal that established no
   violation", and applies "where some requirement is one it is unable to check
   on a **capability or resource** ground". Five grounds are named:
   - the file declares a format major the verifier does not implement;
   - a record carries MU = 1 with a type the verifier does not implement;
   - it cannot execute a codec or filter (`[R-COD-11]`);
   - it declines a layer's or a tile's decode on resource grounds and so cannot
     check §14's decoded-content obligations (`[R-ERR-04]`, `[R-SER-05]`,
     `[R-SER-08]`);
   - it declines to decode a user-metadata document (`[R-MTA-09]`).
   Two of the five carry their own explicit `MUST NOT certify` (`[R-COD-11]`,
   `[R-MTA-09]`); the other three are barred by "a verifier MUST NOT certify a
   file it reports that way" once the verdict is reported.
3. *conforming* (i.e. certification) requires no established violation **and**
   nothing left unchecked on a capability/resource ground: §2.4 has "a verifier
   certifies only violation-free files", §2.3 has the definitional "checks every
   file-level requirement".

I noted, and checked, one thing that could have been a defect and is not: an
unassigned **document encoding** is expressly *not* a cannot-establish ground —
"no content rule attaches there, so nothing is left unchecked, and certification
is unaffected (`[R-MTA-10]`, §21.6)". §17.4 says the same from the other side.
That is coherent: the rules that would need checking are withdrawn, so nothing is
unchecked.

I also checked that `[R-COD-11]`'s ground is not vacuous in a way that breaks
anything. A conforming verifier is a conforming reader, and `[R-CNF-03]` makes
all four codecs and both filters core, so a conforming verifier can always
execute an assigned codec. §17.4 says exactly this: "For a conforming reader that
position arises only at a reserved or experimental value ... it rejects the
layer". At a reserved/experimental value there **is** an established violation
(L43 / L45), so rule 1 dominates and the verdict is *nonconforming*, not
*cannot establish*. The text anticipates this with "only where the verifier
established no violation elsewhere". No finding.

**Things a verifier is permitted to skip.** Exactly three, all express:
SHOULD deviations ("A verifier owes no search for one ... reported where the
verifier observes it and not hunted for", `[R-CNF-12]`); the content of a
user-metadata document under an unassigned encoding (`[R-MTA-10]`, §9.7: "asks
nothing of this walk"); and slack content ("its content is not its concern",
§9.7). Everything else is owed.

**Things a verifier may not skip that a reader may.** The front signature block
by byte equality even when non-resident — §21.2's F6 spells it out: "a reader
that would have to fetch them MAY defer or omit the check (`[R-CNT-04]`); a
verifier holds no such exemption (§2.3)". Extent overlap. The pre-trailer-gap
emptiness. Record flag bits. Alignment and slab invariants. Decoded content.
Reserved-range type values. Member ordering.

The ordered algorithm I would implement:

```
V0.  Obtain the transport-authoritative size ([R-CNT-10]). If < 128 → F5, reject-file.
V1.  Fetch [0,16). Byte-equality against the constant. Mismatch → F1/F6, reject-file.
     (The verifier fetches; it has no residency exemption.)
V2.  Fetch [F-64, F). Validate in §6.2's MANDATED order:
       a. trailer magic          → F8/F1
       b. trailer CRC over [0,60) → F14
       c. version gate (§6.3)     → F18 (major 0); unimplemented major → cannot establish
     Then, "those gates passed", all of the following as one group (§24 says
     they are "validated together", so a file failing two attributes to neither
     alone): flag gates (F19); cfl == size and cfl mod 64 == 0 (F17, F13);
     dir_offset ≥ 16 (F9); dir_length ≥ 4 (F16); dir_offset+dir_length ≤ F-64
     (F10, and F3 for the designated sum); 1 ≤ generation ≤ 2^63-1 (F11, F2);
     file_id ≠ 0 (F12); reserved zero (F15).
     ANY failure here → reject-file, AND [R-CNT-21] exempts the verifier from the
     slack total entirely: "there is no F and no live state to walk, so the total
     is not owed at all ... which is not a partial total but the absence of one."
V3.  Fetch [dir_offset, dir_offset+dir_length). Verify the terminal CRC BEFORE any
     other use (F20). Failure → reject-file, live trailer already established, so
     a PARTIAL slack total is owed.
V4.  Parse the record sequence (F29, F24). Per-type multiplicity (F34). MU gate for
     unknown top-level types (F35; unimplemented MU=1 → cannot-establish ground).
     Extent slots of non-layer top-level records (F30/F31/F32/F2/F3).
     User-metadata framing: no (0,0) slot (F21), extent_length ≥ 5 (F22),
     inline_length == 1 (F23).
     Layer-name namespace over RAW bytes, uniqueness decided FIRST (F4), then
     per-name validity (L3/L5/L6). A record whose name field does not fit its
     inline_length contributes no name and is L23 instead.
     VERIFIER-ONLY here: reserved flag bits (F26), MU=1/PE=0 (F25), registered
     type's stored flags vs §7.3 (F28), reserved-range type value whatever its MU
     (F36).
V5.  Per layer: §19.3's full layer validation (L1..L36, L39, L43..L47, L49), all
     "decidable from the resident directory and F: layer access performs no fetch".
V6.  Per layer: fetch the segment-CRC array, verify crc_of_crc_array (L37); fetch
     each segment, verify its CRC (L38). NOTE: a verifier must fetch EVERY segment,
     not just the ones covering tiles it wants — it is certifying, not reading.
V7.  Per entry: classify per §15.3 (T6..T12). Six rows are *structural*: such an
     entry yields no usable extent, is transparent to slab run continuity, and
     contributes nothing to the coverage walk. An entry that fails only its stored
     bytes' crc is well-formed and keeps its extent everywhere.
V8.  Per stored tile: fetch, verify entry crc (T1), then DECODE. §9.7: "A verifier
     decodes every stored tile, whatever content obligations §14 places on the
     layer". Codec rows T13..T25. Then the decoded-content checks: padding
     positions carry fill (T4), pad bits carry the fill bit (T5), interleaved
     boolean bytes are 0x00/0x01 at real positions (T2), and T26's wrong-stride
     cause, whose "check that detects it is T2's or T4's".
V9.  Per user-metadata extent under an ASSIGNED encoding: terminal CRC (R2), frame
     constraints (R4), decode (R3), document content rules (R5..R10), and member
     ordering at every nesting depth (F27/L48 — verifier-only). Under an UNASSIGNED
     encoding: nothing but the framing, and MUST report the record it ignored
     (scope, encoding value, stored extent length).
V10. VERIFIER-ONLY structural pass: alignment (L40) and slab (L41, L42) invariants;
     nothing occupying the pre-trailer gap (F7); extent overlap (L18 intra-layer,
     F33 otherwise).
V11. The coverage walk of §9.7: partition, bounds, checksums, slack total.
V12. Report: verdict; every requirement unable to check with its ground; every
     *unexamined* scope if it stopped early; the slack total, marked partial if the
     walk did not complete, naming what stopped it; every ignored unassigned-encoding
     metadata record; SHOULD deviations observed, as advisories.
```

One ordering question I checked against shape 4 of the brief ("a claim about
*when* rather than *what*"): §6.2's three-step order is a **MUST**
("A reader MUST validate, in order: the trailer magic; the trailer CRC; the
version gate"), not a MAY, and the reason is given — "only these touch fields
whose positions are fixed across all majors (`[R-CNT-24]`)". The remaining gates
are explicitly a group, not a sequence, and §24 confirms the consequence for
vector construction. No finding.

---

## 5. §21.2's reach derivation — re-derived independently

The brief lists §21.2 as changed and warns not to grant a preamble's assertion.
§21.2 asserts:

> Deriving it there yields F8, F14, F6 and both of F1's instances — each
> asserting an invariant `[R-CNT-24]` fixes in every major — and no other row.

`[R-CNT-24]` fixes exactly four things across all majors: the trailer magic at
F−64; version_major/version_minor **positions** at F−56; a CRC-32C at F−4 over
[F−64, F−4); and the constancy of the front signature block. Everything else in
the trailer — "the remaining 48 trailer bytes" — a future major may redefine.

Walking §21.2 row by row against that:

- F1 — both instances. Front-block bytes [0,8) byte-reversed asserts front-block
  constancy ✅ reaches. Trailer magic byte-reversed asserts the magic ✅ reaches.
- F6 — front block not byte-identical, instances `[0,8)` and `[8,16)`. §6.1's
  table makes both halves constant, and `[R-CNT-24]` says "the front signature
  block (§6.1) is constant" without qualification ✅ reaches.
- F8 — magic at F−64 ✅ reaches.
- F14 — u32 at trailer offset 60 vs CRC of [0,60) ✅ reaches (and §2.3's Note
  gives the right reason: the check *consumes* redefinable bytes as CRC input
  but *asserts* only the fixed invariant).
- F15 — trailer bytes [56,60): inside the redefinable 48 ✗.
- F13, F17 — committed_file_length lives at trailer offset 40, inside the 48 ✗.
  (And 64-alignment of F is derived from format-major-1 facts, as §2.3's Note
  says for F5.)
- F2, F3, F9, F10, F11, F12, F16 — trailer offsets 24/32/40/48 and major-1
  record structures ✗.
- F19 — flags at trailer offset 12 ✗.
- F5 — the 128-byte floor is derived from major-1's directory minimums and
  64-aligned F ✗ (§2.3's Note states this).
- F4, F7, F20–F36 — all major-1 structures ✗.
- F18 — version_major = 0. Outside the premise, as §21.2 says: it "declares no
  major at all".

**The preamble's derivation is exactly right.** No finding.

I also independently re-derived §2.3's other closed count:

> Reach is per condition because a single requirement can state several:
> `[R-CNT-06]` states ten, of which the trailer magic and the trailer CRC assert
> invariants `[R-CNT-24]` fixes and the other eight do not.

Counting §21's rows whose Governing rule cell names `[R-CNT-06]` first: F8, F9,
F10, F11, F12, F13, F14, F15, F16, F17. **Ten.** Of them F8 (magic) and F14
(CRC) reach; the other eight do not. Exactly as stated — and note that the count
only works because conditions are individuated as §21.1 does (the version gate
and flag gates belong to `[R-CNT-07]` / `[R-CNT-08]`, not `[R-CNT-06]`), which
is precisely what `[R-CNF-13]` says. That is a tight, correct piece of writing.

---

## 6. Register arithmetic — re-derived

The brief's shape 5 says to derive a closed count myself. I parsed every register
row mechanically and counted instances by §21.1's own rule (a cell reading `—`
is one instance; otherwise semicolon-separated members):

| Section | Rows | Rows claimed | Instances |
|---|---|---|---|
| §21.2 file scope | 36 | "36 conditions" ✅ | 58 |
| §21.3 layer scope | 49 | "49 conditions" ✅ | 116 |
| §21.4 tile scope | 26 | "26 conditions" ✅ | 55 |
| §21.5 ignored records | 10 | "10 conditions" ✅ | 48 |
| **Total** | **121** | §21.8: "121 conditions over 277 instances" ✅ | **277** ✅ |

Both numbers reproduce exactly. I spot-checked the individuation rules on the
rows where they bite hardest and all hold: T21 ("larger than" = one direction ×
three layout formulas = 3), T22 and T14 and T3 (a "does not equal" / "differs
from" / "not exactly" = two directions × three layouts = 6 each), L44 ("exceeds"
= one direction × three = 3), L21 (two directions × two layouts = 4), L30
("differs from" = 2), R4 (eight frame constraints × two containers = 16), T24
("any codec" stated as one instance, exactly as §21.1 licenses).

I also checked L1's field list for a missing sibling — shape 2 of the brief.
A layer record carries eight u64 fields beyond `A` and `A_slab`, and L1 lists
exactly those eight. `A` and `A_slab` are **not** "offset, length, extent, or
count" fields, so L1 correctly excludes them; a value above 2⁶³−1 in either is
caught by L39 ("A above 2^62") and L29 ("A_slab above 2^62"). No gap.

F2's list is likewise complete for file scope: `file_id` is a u64 but is neither
an offset, a length, nor a count, and has no upper bound beyond ≠ 0.

`[R-ENC-04]`'s "designation is express" rule (§4.2, changed) checked against L2's
nine instances. Every one is expressly designated in the section that defines it:
`[R-CNT-13]` for record extent sums, `[R-GEO-03]` for N / P / C·N / N·P,
`[R-SER-02]` for P·Q and P·Bᶜ, `[R-CNT-17]` for the index-length expression.
Those last three designation clauses live in §6.2, §7.2 and §7.4 — three of the
sections the brief flags as changed, and they read to me exactly like "one-clause
designations added to existing rules". They close a real hole: without them a
reader could compare a *wrapped* `entry_count × 20 + …` against `extent_length`
and accept.

I checked the two kinds `[R-ENC-04]` names that have **no** expressly designated
member — "grid counts" and "ordinals" — and neither can overflow undetected:
Gᵢ = ⌈Eᵢ/Tᵢ⌉ ≤ Eᵢ ≤ 2⁶³−1 by construction, and the maximum disk ordinal
(C−1)·N + (N−1) = C·N − 1 is dominated by C·N, which L2 checks and says so in
the cell itself. Not a defect; I record it as checked and clean.

---

## 7. The coverage walk, with arithmetic

### 7.1 What the walk claims

From §9.7 and `[R-CNT-02]` the claimants are: the front signature block [0,16);
the live trailer [F−64, F); the directory region; **each record's extent**
(including each layer record's tile-index region — "the region enters the walk
once, as that record's extent, and is not a second claimant beside it"); and the
stored extent of each non-sentinel tile-index entry, minus the entries §15.3
classifies reject-tile on a *structural* ground.

A record is **not** a claimant of its own — its header and inline payload lie
inside the directory region, "which is the claimant covering them".

Checks: pairwise disjointness; each claimant within [16, F − 64) (the front block
and trailer being exempt, since "the [16, F − 64) bound above already keeps every
other claimant disjoint from them"); each verifying against its checksum "where
§8.1's map states one".

### 7.2 A concrete file, generation 1

Layer `sst`, rank 1, dimension `x` with E=100 and T=32, so G=4, N=4,
entry_count=4. Interleaved, C=1, channel `temp` float32, fill `0x7FC00000`.
Codec 1 (none), filter 1 (none), A=0, S=0, A_slab=0. Decoded size per tile =
P·Q = 32·4 = **128 bytes**. One tile stored (tile 0); tiles 1–3 sentinel.

```
[0,   16)  front signature block                 16
[16, 144)  tile 0 payload (codec 1 → len==128)  128
[144,228)  tile-index region: 4×20 + 4           84
[228,337)  directory: 24 + 81 + 4               109
[337,384)  pre-trailer pad                       47   ← slack
[384,448)  trailer                               64
F = 448 = 7 × 64  ✅   dir_offset+dir_length = 337 ≤ 448-64 = 384  ✅
```

Coverage: 16 + 128 + 84 + 109 + 64 = **401 claimed**. F − claimed = 448 − 401 =
**47 bytes of slack**, and [337,384) is 47 bytes. The two agree, which is the
whole point of the partition.

**Which bytes are certified.** All 401:

- [0,16) — no checksum; certified by **byte equality** (§8.1's first row, §6.1).
- [16,144) — covered by entry 0's `crc` field.
- [144,228) — the 80 entry bytes covered by the one segment CRC; the 4-byte
  segment CRC array covered by `crc_of_crc_array`; `crc_of_crc_array` itself a
  field of the layer record, inside the directory, covered by the directory CRC.
- [228,337) — the first 105 bytes covered by the terminal 4; the terminal 4
  comparison-verified and covered by nothing further (§4.5's express exception).
- [384,448) — bytes [0,60) covered by [60,64); [60,64) comparison-verified.

**Which bytes are counted but unconstrained.** The 47 pad bytes. "Slack has no
internal structure this specification defines, its content is unconstrained, and
no conformance requirement applies to it", and the verifier "MUST report the
total number of slack bytes".

**Can a byte be neither?** §5.2's Note says no, and gives the reason: the live
committed state is *defined* as what a complete walk reaches, and `[R-LIF-08]`
makes every byte the walk misses slack, so "'belongs to no class' describes
nothing". For *counted vs certified*, the answer is different, and it is
finding 2 below: yes, a byte can be claimed by the walk (hence not slack, hence
not counted) and covered by no checksum (hence not certified). §8.1's last row:

> | Extent of a record of a type this specification has not assigned | none — the bytes are opaque (§7.2) | — |

### 7.3 A walk that does not complete

Same layer, now with A = 4096 declared, two tiles stored, and the second one
misplaced:

```
[0,     16)  front block                     16
[16,  4096)  alignment gap                 4080   ← slack
[4096,4196)  tile 0, len 100                100   4096 mod 4096 = 0  ✅
[4196,4200)  gap                               4   ← slack
[4200,4300)  tile 1, len 100                 100   4200 mod 4096 = 104 ✗  → L40
[4300,4384)  tile-index region                84
[4384,4493)  directory                       109
[4493,4544)  pre-trailer pad                  51   ← slack
[4544,4608)  trailer                          64
F = 4608 = 72 × 64  ✅
```

Had the walk completed: claimed = 16+100+100+84+109+64 = 473; true slack =
4608 − 473 = **4135**, and 4080 + 4 + 51 = 4135 ✅.

But the walk itself establishes L40 — one of the rejections `[R-CNT-21]` names
explicitly ("L18's overlap or L40 through L42's placement among them"). So:

> the claimants it had already enumerated are discarded with the layer, since
> the total is a claim about a live state one of whose layers is not usable

Enumerated claimants that survive: front block 16, directory 109, trailer 64 =
189. **Partial total = 4608 − 189 = 4419.** That is an upper bound on 4135, never
an under-count ✅, exactly as `[R-CNT-21]` promises. The verifier "MUST say which
scope or violation stopped the walk" — here: layer `sst`, L40, `[R-SLB-01]`.

Verdict: **nonconforming** (L40 is established; rule 1 dominates).

Note that the *layer record's own bytes* stay counted, because they live inside
the directory region, which is a claimant that does not belong to a layer and is
therefore not discarded. That falls out of §9.7's "a record is not a claimant of
its own" and is the right answer.

I checked the upper-bound claim for soundness in general: partial = F − |union of
enumerated claimants|, true = F − |union of all claimants|; enumerated ⊆ all, so
partial ≥ true. The text says "F less the bytes claimed by", i.e. the union, not
the sum, so overlapping claimants cannot make it an under-count. Clean.

One residual question I resolved rather than reported: when the walk itself
establishes a **file-scope** violation (say F33), does the layer-style
"claimants already enumerated are discarded" clause apply, giving partial = F?
No — that clause is worded for layers ("discarded with the layer"), and the
definition is flat: "A partial total is F less the bytes claimed by the claimants
the walk did enumerate". Absent an analogous discard clause at file scope, the
enumerated claimants stand. Decidable; no finding.

---

## 8. Extent overlap, alignment and slab, on adversarial layouts

### 8.1 Overlap classification

`[R-CNT-13]`'s three arms are exhaustive over the pairs. I enumerated:

| Adversarial layout | Rule | Outcome | Row |
|---|---|---|---|
| Layer A's stored tiles [512,1112) and [1024,1124), both 512-aligned | intra-layer | reject-layer | L18 |
| Layer A's index region [1000,1084) vs layer B's tile [1050,1200) | across layers | reject-file | F33 |
| Layer A's sub-record extent vs layer A's index region | intra-layer | reject-layer | L18 |
| Top-level metadata extent vs the directory region | two non-layer structures | reject-file | F33 |
| A layer record's extent slot pointing *into* the directory | layer structure vs another scope's | reject-file | F33 |
| A record extent at offset 8 | not overlap — a bounds row | reject-* | F31/L16/T8 |
| A stored tile ending past F−64 | not overlap — a bounds row | reject-tile | T9 |

The first two cases are the ones that matter for a verifier, and note the first:
**both offsets satisfy the alignment invariant and the tiles still overlap**.
Alignment does not imply disjointness, and the document does not pretend it does
— `[R-SLB-01]` states only `offset mod A = 0`. Two separate checks, correctly
separated.

F33's parenthetical about the front block and trailer is doing real work and I
verified it closes: a claimant reaching [0,16) or [F−64,F) is caught by a bounds
row rather than an overlap row, and the list F9/F10, F30/F31/F32, L15/L16/L17,
T8/T9 covers every claimant kind (directory, non-layer top-level extents, layer
and sub-record extents, stored tiles). No claimant kind is missing.

### 8.2 Alignment

`[R-SLB-01]`: "every stored tile's offset satisfies offset mod A = 0", verifier
checks, violation reject-layer.

Degenerate cases I built:

- **Sentinel entries.** A sentinel's offset is `0xFFFF_FFFF_FFFF_FFFF`, which is
  not a multiple of any A ≥ 512. Does L40 fire? No: §3.1 makes a sentinel tile
  *not stored*, so the invariant does not range over it. Clean.
- **Structurally-rejected entries.** Here §3.1's definition and `[R-SLB-01]`'s
  wording pull apart: §3.1 says "A tile is *stored in a generation* if and only
  if that generation's tile-index entry for it is not the sentinel", so an entry
  with `length = 0` and a non-sentinel offset describes a *stored* tile by that
  definition, and its offset need not be A-aligned. This is exactly the brief's
  shape 9 — a definition that could sever a rule from its carve-out. It does not,
  because `[R-IDX-03]` says so in general: such an entry "contributes no stored
  extent to the *verifier* rows, which bind over well-formed entries' extents
  only", and §15.3's table routes the alignment check through a *verifier* row.
  `[R-SLB-03]` then repeats it for slabs in its own words. I looked hard for a
  gap here and did not find one.
- **A layer with entry_count = 0 declaring A = 4096.** Vacuous; conforming.

### 8.3 Slabs

`[R-SLB-02]`/`[R-SLB-03]` on a concrete layout: interleaved, N = 8, S = 4,
A_slab = 1024, runs [0,4) and [4,8).

```
run 0: ordinals 0,1,2,3   stored: 0, 1, 3     (2 = sentinel)
run 1: ordinals 4,5,6,7   stored: 5, 6        (4, 7 = sentinel)

tile 0 @ 1024 len 200   1024 mod 1024 = 0            ✅ L42
tile 1 @ 1224 len 100   = 1024+200                   ✅ L41
tile 3 @ 1324 len 150   = 1224+100  (2 transparent)  ✅ L41
--- gap, placement free between runs, slack ---
tile 5 @ 4096 len 300   4096 mod 1024 = 0            ✅ L42 (run 1's FIRST stored tile)
tile 6 @ 4396 len 50    = 4096+300                   ✅ L41
```

Variants I checked:

- Make tile 3's entry `length = 0`: structurally rejected → **transparent**, so
  run 0's packing relation is only 0→1 and still holds. T10 fires (reject-tile,
  reader), and the walk contributes no extent for it. §9.7: "An entry
  `[R-IDX-03]` classifies reject-tile on a *structural* ground does not make the
  walk incomplete: the walk passes over it, and the bytes it nominally addresses
  fall to slack (§15.3)."
- Make tile 3's entry fail only its stored bytes' crc: **not** transparent — "its
  offset and length stand, and the packing relation reads them as it does any
  other stored tile's". So if the writer had placed it elsewhere, L41 fires too,
  and the walk keeps its extent. Both T1 and L41 are then live.
- Make tile 0 a sentinel: run 0's first stored tile becomes tile 1, and *its*
  offset must be A_slab-aligned. `[R-SLB-03]` says "the **first stored** tile's
  offset", not "the run's first ordinal", so this is determined.
- A run with no stored tiles: "A run with no stored tiles imposes nothing."
- S = 1: every stored tile is its own run's first, so every stored tile must be
  A_slab-aligned. Determined.
- A_slab = 1: every offset satisfies `mod 1 = 0`; contiguity only. The §16.2 Note
  says exactly this.
- Planar: runs "never span channel blocks", block c is [c·N, (c+1)·N), run r
  starts at `block_start + r·S`, and "the final run of a block can cover fewer
  than S ordinals". I checked C=4, N=8, S=3 → blocks [0,8),[8,16),[16,24),[24,32),
  each partitioned as [0,3),[3,6),[6,8) relative to its block. Determined.

`[R-SLB-03]`'s closing claim — "this invariant stays decidable from the index
entries alone, given the committed file length §15.3 already requires to classify
any entry" — is true: every input is `offset`, `length`, the entry's §15.3 class,
and F.

One thing worth recording for the charter: `[R-SLB-04]` (stale slab declarations)
binds "a writer or updater whose **commit** changes …", and compaction is a
whole-file rewrite, not a commit (`[R-LIF-01]`). So `[R-SLB-04]` does not reach a
compactor by its own words — but it does not need to, because `[R-WRT-07]` binds
the compactor directly to "every declared layout invariant permits
(`[R-SLB-01]`, `[R-SLB-03]`)". I checked this specifically because it looked like
a scope hole and it is not one.

---

## 9. Checksum obligations — is every live structure covered?

**No, and the document says so, twice.** The honest answer to my charter's
question:

| Live structure | Covering checksum | Verified how |
|---|---|---|
| Front signature block | none | byte equality (§6.1) |
| Trailer | its own bytes [60,64) | comparison; covered by nothing further |
| Directory region | its own final 4 bytes | comparison; covered by nothing further |
| Tile-index region | segment CRC array (entries) + `crc_of_crc_array` (the array) | chained to the directory CRC |
| Stored tile | its index entry's `crc` field | that field covered by its segment CRC |
| User-metadata extent | its own final 4 bytes | comparison; covered by nothing further |
| **Extent of a record of an unassigned type** | **none** | **nothing** |

§4.5 enumerates the exceptions and they match §8.1's map exactly: the front
block; "the terminal checksum fields of §8.1's map — the trailer,
directory-region, and user-metadata checksum fields"; and "the extent of a record
of a type this specification has not assigned". The interior checksum fields —
each segment CRC array, each entry's `crc`, each `crc_of_crc_array` — are "both
comparison-verified and covered by exactly one further checksum". I traced every
one of those chains and they close.

`[R-SEC-04]` says the same from the security side: "The extent of a record of a
type this specification has not assigned is covered by no checksum either (§8.1),
so corruption inside it is equally invisible".

That last row is where finding 2 lives. A **conforming** file may carry such a
record — §21.6 registers "A record type this specification has not assigned, from
the experimental range (≥ 0x8000, §10.2), carries MU = 0 | Ignored, and preserved
or dropped per its PE bit". Its extent is a claimant of the coverage walk (it is
"a record extent (the bytes any record's extent slot references, **whatever the
record's type**, §7.2)"), so those bytes are *not* slack and are *not* in the
slack total; and no checksum covers them, so they are not certified either. Take
my §7.2 file and add a top-level record of type 0x8001, MU=0, PE=0,
inline_length 0, extent (X, 4096): 4096 bytes that a certificate covers, that no
check inspects, and that no rule requires the verifier to count or name.

The document states the contrary principle, in `[R-MTA-10]`:

> bytes a certificate covers without inspecting are counted and named, never
> silent.

For the metadata sibling — which is *better* off, having a verified terminal CRC
— `[R-MTA-10]` imposes a naming duty. For the strictly worse case it imposes
none. That is finding 2.

---

## 10. Decoded-content obligations

**What a verifier must decode.** Every stored tile, unconditionally: §9.7 —
"A verifier decodes every stored tile, whatever content obligations §14 places on
the layer: §21.4's codec rows are file-conformance violations, and a verifier
MUST NOT certify past a violation it has not looked for." Plus every
user-metadata document under an assigned encoding.

**What it compares against.**

- Decoded length vs the declared decoded size, from `[R-SER-02]`/`[R-SER-03]`
  (T3). The declared size is P·Q interleaved, P·Bᶜ for a planar numeric channel,
  ⌈P/8⌉ for a packed planar bool plane.
- Every padding position's content vs the channel's **recorded** fill
  (`[R-SER-05]`, T4) — "the recorded fill bytes for a numeric channel, the
  recorded fill byte for an interleaved bool channel, the fill bit in a packed
  plane".
- Every pad bit vs the plane's channel's fill bit (T5).
- Every interleaved bool byte at a real position vs {0x00, 0x01}
  (`[R-SER-08]`, T2). T2's own text explains the division of labour: "the same
  byte at a padding position is T4's, the two rows together covering
  `[R-SER-08]`". I checked that this really is complete: a padding position's
  bool byte must equal the fill byte, which `[R-TYP-07]` constrains to 0x00 or
  0x01, so any other byte at a padding position is a T4 violation. Covered.
- Codec-specific header and stream facts (T13, T15–T25).

**What it is permitted to skip.** Sample *values* — §21.7 is blunt: "this format
detects *corruption of structure*, not *incorrectness of content*". And the
document's own narrowing is exact: "The obligations of §14.5 and `[R-SER-08]`
narrow this only where content is structurally constrained: padding positions,
pad bits, and boolean bytes."

I checked T26 (a mis-strided filter) against shape 3, because it argues by
analogy: "the check that detects it is T2's or T4's". §21.7 elsewhere writes
"witnessed by T2, T4 or T5, exactly as a mis-strided filter is". Is T5 ever a
witness for a wrong stride? I proved not: the shuffle places byte *i* of group
*j* at `i·n + j`, so the byte landing at the final offset `L − 1` is byte
`s − 1` of group `n − 1`, whose original offset is `(n−1)·s + (s−1) = L − 1`.
**The last byte of the image is a fixed point of every byte-shuffle stride.** Pad
bits live only in the final byte (`[R-SER-03]`), so no stride, right or wrong,
can move them. T26 is right to say "T2's or T4's"; §21.7's earlier "T2, T4 or T5"
attaches to a *mis-ordered image*, which genuinely can move a pad bit. I decided
this is an editorial imprecision in a Note-adjacent clause that the same section
later states correctly ("the check that detects it is T2's or T4's, exactly as
T26 has it"), and did **not** report it. Recording the proof because it took real
work and is reusable.

I also checked `[R-COD-10]`'s universal "The decoded image's length L is
divisible by s in every case (§14)": planar numeric L = P·Bᶜ with s = Bᶜ ✅;
interleaved L = P·Q with s = Q ✅; packed bool L = ⌈P/8⌉ with s = 1 ✅. True, no
degenerate counterexample.

And §17.2's zstd Note, against the 1 KiB window floor: with
`Single_Segment_Flag` set, RFC 8878 has no Window_Descriptor and Window_Size is
the frame content size, which `[R-COD-06]` already pins to the decoded size;
without it the Window_Descriptor's minimum windowBase is 2¹⁰ = 1024. So a tile
below 1 KiB decoded is encodable under codec 3 only as a single-segment frame.
The Note's worked figures (18, 30 from §14.2; 2 from §14.3) are all values I
recomputed above. Correct. (§14.2's example also yields 12 for the planar `b`
plane, which the Note does not list, but it does not claim to enumerate.)

---

## 11. The multi-generation trace

Same layer as §7.2. Four steps, verified after each.

### Generation 1 — creation

As laid out in §7.2. F = 448. Claimed 401, slack 47.
**Verdict: conforming.** Every claimant within [16, 384) ✅, disjoint ✅, every
checksum verifies ✅, no structure in the pre-trailer gap ✅ (F7 clean), tile 0
covers x = 0..31, all < E = 100, so it has **no padding positions** and
`[R-SER-05]` is vacuous for it ✅. No bool channel, so `[R-SER-08]` is vacuous ✅.
Codec 1, so `[R-COD-04]` requires `length == 128` ✅. Slack total reported: 47.

### Generation 2 — append (store tile 1)

Writing begins at exactly F = 448 (`[R-LIF-02]` step 1). Tile 1's payload, then
the whole tile-index region re-emitted — `[R-WRT-04]`: "Every layer whose
stored-tile set or index content this commit changes has its tile-index region
re-emitted in full — entry_count entries plus the segment CRC array — necessarily
at a new placement" — then the complete directory, then pad and trailer.

```
[448, 576)  tile 1                   128
[576, 660)  index region (new)        84
[660, 769)  directory (new)          109
[769, 832)  pad                       63   ← slack
[832, 896)  trailer                   64
F = 896 = 14 × 64 ✅   660+109 = 769 ≤ 832 ✅
```

Claimants now: front 16, tile 0 [16,144) 128 (still live — its entry is in the
new index, byte-identical at its disk-ordinal position), tile 1 128, index 84,
directory 109, trailer 64 = **529**. Slack = 896 − 529 = **367**.

Cross-check against what was superseded: old index 84 + old directory 109 + old
pad 47 + old trailer 64 + new pad 63 = **367** ✅.

**Verdict: conforming.** Slack total 367.

### Generation 3 — update (supersede tile 0's bytes)

```
[896, 1024)  tile 0'                 128
[1024,1108)  index region (new)       84   (entry 0 re-pointed to 896)
[1108,1217)  directory (new)         109
[1217,1280)  pad                      63   ← slack
[1280,1344)  trailer                  64
F = 1344 = 21 × 64 ✅
```

Claimed: 16 + 128 (tile 0') + 128 (tile 1, unmoved) + 84 + 109 + 64 = **529**.
Slack = 1344 − 529 = **815**.

Cross-check: old tile 0 128 + gen-1 index 84 + gen-1 dir 109 + gen-1 pad 47 +
gen-1 trailer 64 + gen-2 index 84 + gen-2 dir 109 + gen-2 pad 63 + gen-2 trailer
64 + gen-3 pad 63 = **815** ✅.

**Verdict: conforming.** Slack total 815 — 61% of the file. This is the number
§5.2 says "tells an operator to compact", and it does.

### Generation 4 — compaction

`[R-WRT-06]`/`[R-WRT-07]`: fresh `file_id` (a new draw, "not merely a value
compared against the input's"), generation 1, the **creation** path of
`[R-LIF-02]` including both barriers and the step-5 pad, every stored tile's
bytes verbatim, each index entry's `crc` unchanged, entry offsets new, segment
CRCs recomputed, `crc_of_crc_array` updated, extent slots re-pointed.

```
[0,   16)  front block                16
[16, 144)  tile 0' (bytes verbatim)  128
[144,272)  tile 1  (bytes verbatim)  128
[272,356)  index region (regenerated) 84
[356,465)  directory                 109
[465,512)  pad                        47   ← slack
[512,576)  trailer (file_id Y, gen 1) 64
F = 576 = 9 × 64 ✅   356+109 = 465 ≤ 512 ✅
```

Claimed 529, slack **47**. The file shrank 1344 → 576 and slack 815 → 47; the
47 that remain are the new pad, which no operation removes. `[R-CNT-21]`'s
"Only compaction (§20.5) reclaims it" is about *which operation*, not about
reclaiming to zero, and the arithmetic bears that out.

Regeneration check: `[R-WRT-07]` says regenerating means "classifying every entry
in it: a sentinel is re-emitted unchanged, and every other entry is re-pointed".
Entries 1 and 3 here are sentinels, re-emitted as `FF ×16 00 ×4`; entries 0 and 2
— wait, in my layer tiles 0 and 1 are stored, 2 and 3 sentinel — entries 0 and 1
re-pointed to 16 and 144, entries 2 and 3 unchanged. The segment CRC changes
(offsets changed), so `crc_of_crc_array` changes, so the layer record's inline
payload changes at that field — but its **length** does not, so `dir_length`
stays 109. The directory's terminal CRC changes. All consistent.

**Verdict: conforming.** Slack total 47.

`[R-WRT-07]`'s reference-array guarantee holds trivially: the decoded tile bytes
are byte-identical, so every sample is bit-identical, `[R-MDL-02]` satisfied.

§21.7 correctly records that none of `[R-WRT-06]`'s four trailer obligations has
a witness in the output — "the output carries no record that it is a compaction
output at all" — so a verifier certifying gen 4 has no way to know the `file_id`
was freshly drawn. I checked whether that ought to make the verdict *cannot
establish*: it should not, because §2.3 limits that verdict to grounds that are
"capability or resource", and a no-witness obligation is neither. Determinate;
no finding.

---

## 12. Findings

### verifier-01 — §22.2 `[R-SEC-02]`'s new allocation rule forbids the decode-buffer sizing that §14, §17 and §21.9 require

**Kind: CONTRADICTION. Byte-level: yes.**

§22.2 (`[R-SEC-02]`) reads, in one requirement, in this order:

> Decoded tile size is a function of the layer's declarations alone (§14.2,
> §14.3), so a reader allocates from geometry and never from a length embedded
> in a payload

and then, four sentences later:

> A reader MUST NOT size an allocation, fetch, or index walk in proportion to a
> declared magnitude it has not corroborated against the file's actual length: a
> layer can declare 2⁶³ − 1 addressed tiles, and the declaration alone costs
> nothing to state.

A tile's decoded size **is** a declared magnitude — P·Q, or P·Bᶜ, or ⌈P/8⌉,
derived from the layer's declarations. And under codecs 2–4 it is **expressly
uncorroborated** against anything in the file. §17.2's Note:

> For the compressing codecs (2–4), no bound relates a stored length to its
> decoded size in either direction — codec 1's equality is `[R-COD-04]`'s
> subject.

`[R-SER-07]` is unambiguous that a reader must nevertheless size from it:

> decoded size is a function of the layer's declarations alone — geometry,
> layout, and channel types — never of payload content, and readers allocate
> from those declarations, not from stored data.

**A concrete conforming file.** Rank-1 interleaved layer, dimension `x` with
E = T = 2²⁸, one `uint8` channel with fill 0x00, codec 3 (zstd), filter 1.
Then G = 1, N = 1, P = 2²⁸, Q = 1, entry_count = 1, and the decoded size is
2²⁸ = 268,435,456 bytes = **exactly 256 MiB** — §21.9's guaranteed minimum, not
above it. E mod T = 0, so there are no padding positions; no bool channel, so no
`[R-SER-08]` obligation. One tile is stored: 2²⁸ zero bytes as a single zstd
frame with an 8 MiB declared window (within §21.9's `Window_Size` row), which
compresses to on the order of 1 KiB. Layout:

```
[0,     16)  front block                16
[16,  1040)  the one stored tile      1024
[1040,1064)  index region (1×20 + 4)    24
[1064,1165)  directory (24 + 73 + 4)   101
[1165,1216)  pad                        51
[1216,1280)  trailer                    64
F = 1280 = 20 × 64  ✅
```

Every quantity of this ~1.3 KB file lies inside §21.9's table: rank 1 ≤ 32,
C = 1 ≤ 4096, entry_count = 1 ≤ 2³², layers 1 ≤ 65,536, dir_length 101 ≤ 16 MiB,
decoded tile 256 MiB ≤ 256 MiB, no metadata document, window 8 MiB ≤ 8 MiB.

Now the two readings, and what each implementation does with this file:

- **Narrow reading** — "declared magnitude" means a magnitude that declares how
  much *of the file* to touch (entry_count, region lengths, offsets), and
  "an allocation" means a buffer for file bytes. The rule is about I/O
  amplification, which is what the following clause and §22.2's Note illustrate
  ("The index is the cheapest hostile amplifier"). **Implementation B** allocates
  268,435,456 bytes, decodes, serves the samples. Conforming.
- **Broad reading** — the sentence says "an allocation", the decode buffer is an
  allocation, its size is proportional to a declared magnitude, and that
  magnitude is corroborated against nothing. **Implementation A** refuses to
  allocate 209,715× the file's length and declines the tile.

`[R-ERR-04]` then makes them disagree about conformance itself:

> Software that declines **on that ground** a file whose every quantity lies
> within the table is not a conforming reader (`[R-CNF-03]`) — the two capability
> refusals §21.6 names, a foreign format major and an unimplemented MU = 1 type,
> are not this ground

So under the narrow reading, A is not a conforming reader; under the broad
reading, B violates a MUST NOT. For a verifier the fork is sharper still: a
verifier that declines the decode cannot check §14's decoded-content obligations
and reports *cannot establish*, while one that proceeds reports *conforming*.
Same bytes, two verdicts, and the disputed file is itself conforming.

**Why I grade it byte-level.** The test is "must accept or reject". Here two
competent implementations reading this text reach opposite accept/reject
positions on a file I have laid out byte-region by byte-region, and each can cite
a MUST for its position. This is not a dispute about a SHOULD — `[R-SEC-02]`'s
clause is a MUST NOT in capitals, and `[R-ERR-04]`'s acceptance duty is a MUST
that `[R-CNF-03]` carries.

**What I picked, and what an implementer does wrong without it.** I implemented
the narrow reading, because §22.2's own first property and `[R-SER-07]` both say
in terms that decoded-size allocation comes from declarations, and because the
broad reading would make §21.9's 256 MiB tile guarantee unsatisfiable by any
reader with a proportionality guard. But I had to supply that reasoning myself —
the document never restricts "an allocation" to file-byte buffers, never defines
"declared magnitude", and never says the decoded size is exempt from the rule.
An implementer who reads §22.2 in order and applies its last sentence literally
builds a reader that refuses conforming files, and reports the refusal as a
resource limit — which §21.9 says makes it a non-conforming reader.

The narrowing this rule appears to want is available and cheap: name the
magnitudes it governs (those that determine how many of the file's own bytes a
reader fetches, walks or buffers), or exempt the decoded size by name.

---

### verifier-02 — `[R-MTA-10]`'s "counted and named, never silent" is falsified by the extent of a record of an unassigned type, and no rule reaches it

**Kind: AMBIGUITY. Byte-level: no.**

`[R-MTA-10]` closes with a general principle, stated as the reason for the
reporting duty it imposes:

> and it MUST report each record it ignored on this ground, naming the owning
> scope, the encoding value, and the stored extent length, as it reports the
> slack total (`[R-CNT-21]`): bytes a certificate covers without inspecting are
> counted and named, never silent.

There is a strictly worse class of such bytes, and nothing counts or names it.
§8.1's map:

> | Extent of a record of a type this specification has not assigned | none — the
> bytes are opaque (§7.2) | — |

§21.6 makes a file carrying one **conforming**: "A record type this specification
has not assigned, from the experimental range (≥ 0x8000, §10.2), carries MU = 0 |
Ignored, and preserved or dropped per its PE bit". And `[R-CNT-02]` makes the
extent a **claimant** of the coverage walk — "a record extent (the bytes any
record's extent slot references, **whatever the record's type**, §7.2)" — so
those bytes are not slack and do not enter the slack total.

Concretely: take my §7.2 file (F = 448, 401 claimed, 47 slack) and add a
top-level record of type 0x8001 with MU = 0, PE = 0, inline_length 0, and extent
(X, 4096). The verifier certifies. Its report contains a slack total that
excludes those 4096 bytes, and — on the reading I could not rule out — nothing
else about them. §22.3 confirms the exposure and declines to close it:

> The extent of a record of a type this specification has not assigned is covered
> by no checksum either (§8.1), so corruption inside it is equally invisible:
> §20.4's byte-identical re-emission (`[R-WRT-05]`) carries such an extent
> forward unread, and `[R-WRT-08]` bars re-encoding it, so nothing an updater
> does would surface the damage.

The two readings of `[R-MTA-10]`'s closing clause:

1. **A general duty.** "Bytes a certificate covers without inspecting are counted
   and named" states what a certificate owes, and the metadata case is one
   application of it; a verifier must likewise name each unassigned-type record
   extent it certified without inspecting.
2. **A local justification.** The clause explains why *this* duty exists and
   imposes nothing beyond it; unassigned-type extents are covered silently.

I implemented reading 2, because the duty's operative words ("it MUST report each
record it ignored **on this ground**") are scoped to the encoding case, and
because §21.6's row for the unassigned record type conspicuously does *not*
mention a report where §21.6's row for the unassigned metadata encoding does
("so a verifier certifies, reporting the record it ignored"). But reading 1 is
what the sentence says, and it is the reading that makes the principle true; an
operator following §22.3's advice — "an operator who wants no such bytes rejects
on that report line, a policy above conformance" — has no report line to reject
on for the class that carries **no checksum at all**, only for the class that
carries a verified one.

**What an implementer does wrong without it.** Two verifiers emit different
certificates for the same conforming file: one names the opaque extent, one does
not. An operator building an ingest policy on "reject if the certificate names
uninspected bytes" gets no protection against precisely the unchecksummed case.
No verdict and no byte on disk changes, which is why I do not grade this
byte-level.

---

## 13. Things I checked and did not report

Recording these so the next round does not repeat the work, and so the ratio of
searching to reporting is visible.

- **§21.2's reach derivation** and **§2.3's "`[R-CNT-06]` states ten"** — both
  re-derived independently, both exactly right (§5 above).
- **§21.8's 121 conditions over 277 instances** — reproduced mechanically (§6).
- **§2.2's prefix table** — complete and minimal against the prefixes actually
  used (§2).
- **§10.2's "Two spaces carry no experimental range"** — one is tabulated
  (channel layout), one is not (the flag lanes); loose but explicitly named.
- **§20.5's "one row for each of the other seven spaces §10.2 tabulates (L31,
  L33, L34, L36, L43, L45, R1)"** — I checked the mapping space by space: index
  encoding, linearization, sample type, channel layout, codec, filter, metadata
  encoding. Seven spaces, seven rows, each row really registering that space's
  reserved range. Correct.
- **§2.3's closed list of expressly-declared non-violations** ("§6.3's flags = 0
  against a set ignore-lane bit and §6.2's pre-trailer gap longer than
  `[R-LIF-02]` step 5's pad are the cases this text states"). I grepped every
  "is conforming" / "remains conforming" / "not a violation" in the document and
  classified each: §10.3's publishing ban and §18.3's registry targeting are
  category-one conduct rules, already named; §6.4, §17.2, §18.4 and §21.9's cases
  are SHOULDs. The list of two is complete.
- **`[R-CNF-08]`'s "exactly one owning scope"** against §18.1's user-metadata
  record, which has file scope top-level and layer scope as a sub-record. Reads
  correctly per instance, not per type.
- **§15.3's entry-state table** — enumerated the (offset, length, crc) space and
  found it total: sentinel/sentinel with crc 0 and with crc ≠ 0, either-one-
  sentinel, and for non-sentinels length 0, offset < 16, either field > 2⁶³−1,
  sum overflow or sum > F−64, then the crc row, then the three verifier rows.
  Exactly six *structural* rows, as `[R-IDX-03]` claims.
- **`[R-COD-07]`'s "addressed tiles" quantifier and its Note** — "The escape ends
  exactly when the layer's addressed-tile count rises above 0, which takes every
  dimension's extent nonzero". True: N = ∏⌈Eᵢ/Tᵢ⌉ is zero iff some Eᵢ is zero,
  and C ≥ 1.
- **§11.1's growth Rationale** against §20.3's normative bar — I tried to build a
  growth that leaves entry_count unchanged while renumbering disk ordinals. For
  N > 0 it is impossible (growth strictly raises any Gᵢ it touches, hence N); for
  N = 0 there are no entries. The planar variant (raise N while lowering C to
  hold C·N) requires dropping a channel, which §20.3 step 4 bars for any layer
  with a stored tile in the superseded generation, and which for a layer storing
  nothing leaves an all-sentinel index byte-identical anyway. Clean.
- **The final-byte fixed point of byte-shuffle** (§10), which vindicates T26's
  "T2's or T4's" against a looser sentence in §21.7.
- **`[R-CNT-21]`'s partial-total definition at file scope** — resolved by the
  flat definition ("F less the bytes claimed by the claimants the walk did
  enumerate"); the discard clause is worded for layers and does not generalize.
- **Whether the unwitnessed obligations of §21.7 force *cannot establish***.
  They do not: §2.3 limits that verdict to "capability or resource" grounds, and
  a no-witness obligation is neither. If they did, no file could ever be
  certified.
- **§21.9's tile-decoded-size row being per-addressed-tile** and the interaction
  with a planar layer's per-channel plane sizes. Determined.
- **Appendix H's verifier checklist** against the actual set of verifier-detected
  rows (F1/F6, F7, F25, F26, F27, F28, F33, F36, L18, L25, L40, L41, L42, L46,
  L47, L48, L49, T2, T4, T5, T26). Every one is reachable from the checklist's
  items; T26 via the decoded-content item, which is where its detection actually
  lives. Non-normative anyway, but correct.
- **Appendix G item 5's "elsewhere it changes the stored bytes of every tile it
  touches"** — false as a universal (a tile whose decoded image is constant is
  invariant under any permutation of its bytes), but the brief states that one
  Appendix G sentence has been given three false universals in three cycles and
  has been sent to the maintainer's ledger rather than repaired again. I judged
  this to be that sentence, and did not report it as new.

## 14. Confidence

**Medium.** I could build a conforming verifier from this document alone and I
believe two implementers doing so would produce the same verdicts on every file
I constructed except the one in verifier-01. The arithmetic is exact everywhere I
could check it, the register is internally consistent to the instance count, the
coverage walk closes, and the multi-generation trace is fully determined. The one
place I would expect real divergence is the allocation rule, and the one place a
certificate's contents are underdetermined is the opaque record extent.

Transcript finding count: **2**.
