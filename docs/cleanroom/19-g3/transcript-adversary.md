# Cleanroom round 19 — Adversary transcript

## Disclosure

I read exactly one file: `/Users/robertkleffner/Documents/GitHub/tarn/spec/tarn.md`
(4,364 lines), in five `Read` calls covering lines 1–4364 with no gaps. I ran
`grep`/`python3` against that file only (a modal-casing scan and a mechanical
extraction of the §21 register tables). Everything else I ran was local Python
in my own scratchpad: a CRC-32C implementation, a TARN encoder, a
document-derived verifier, and eleven constructed `.tarn` files. I did not open
`docs/`, `PLAN.md`, `AGENTS.md`, `README.md`, `conformance/`, `spec/registry.json`,
`OPEN-QUESTIONS.md`, or any ADR. I ran no `git` command. I did not list or read
the round-19 output directory. I used no web search or fetch. No prior knowledge
of another array format was used to settle any question; where it generated a
suspicion I chased the suspicion back into this document's text.

---

## 0. Method

The charter is constructive, so I spent the walk building rather than narrating.
The sequence was:

1. Read the document end to end, cold, in order.
2. Reproduce every numeric constant it states, from its own definitions.
3. Build an encoder and a verifier from the document alone, and note every point
   where I had to guess.
4. Emit eleven files: the minimal file, a full one-layer file with a stored edge
   tile, and nine boundary/degenerate/adversarial constructions.
5. Attack: for each surface the charter names, write the concrete bytes, work out
   the two candidate verdicts, and find the sentence that decides between them —
   or report that none does.

I did not treat §20.5 / §21.7 / §23.1 / Appendix G as a checklist. I read them
first, then implemented, then came back to them with the implementation in hand.

---

## 1. Reproducing the document's own arithmetic

Everything checkable is correct. I list this not as padding but because it is the
evidence that the document's *numeric* surface is closed, which is where I
stopped looking.

CRC-32C implementation validated against §4.5's check vector:

```
CRC-32C("123456789") = 0xE3069283   ✓ (§4.5)
CRC-32C("")          = 0x00000000   ✓ (§4.5)
```

Then, computed from the document's field definitions with nothing else:

| Claim | Section | Computed | Match |
|---|---|---|---|
| Trailer CRC of Appendix A's file | App. A | `0xE00938D2` | ✓ |
| Whole 128-byte minimal file | App. A | byte-identical to the hex dump | ✓ |
| CRC of 4 sentinel entries (80 bytes) | §7.4 | `0x80A34955` | ✓ |
| `crc_of_crc_array` over `55 49 A3 80` | §7.4 | `0xC4EE982E` | ✓ |
| CRC of a full 2¹⁶-sentinel segment | §15.4, App. B | `0xEECB3BB2` | ✓ |
| The 81-byte `sst` layer payload | §7.4 | byte-identical | ✓ |
| Byte-shuffle of 1.0/2.0/3.0 float32 | §17.3 | `00 00 00 00 00 00 80 00 40 3F 40 40` | ✓ |

Appendix A reproduced **byte for byte** from §6.1, §6.2, §7.1 and §4.5 alone —
I wrote the encoder before looking at the dump. Same for §7.4's worked layer
payload: `4 + 34 + 18 + 12 + 13 = 81`, no residue, sub-record sequence empty.

Worked examples I re-derived and confirmed: §11.2's grid arithmetic; §11.4's
ordinals (spatial 10, in-tile 11,452, planar disk ordinal 74); §14.2's three
interleaved layouts (18/12/30 bytes, offsets 15, 10, 25); §14.3's packed plane
(`55 01` / `55 FD`); §14.5's edge tile (32 bytes, 15 padding positions);
§15.4's million-entry layer (16 segments, region 20,000,064 bytes, segment 15 at
`[19,660,800, 20,000,000)`, ~339 KB, one full segment = 1.25 MiB); §15.4's planar
entry at region bytes `[1480, 1500)` and entries 96–127; §20.3's `32·20 + 4 = 644`;
§21.9's note (2³² tiles → 256 KiB CRC array; 2³⁶ → 4 MiB).

**Register arithmetic.** I extracted §21.2–§21.5 mechanically and applied §21.1's
counting rule ("Instances within a cell are separated by semicolons, and a cell
reading — is one instance"):

```
F rows 36  instances  58
L rows 49  instances 116
T rows 26  instances  55
R rows 10  instances  44
TOTAL 121 rows, 273 instances
```

§21.8 says "121 conditions over 273 instances". Exact. The subsection headers
("36 conditions", "49", "26", "10") also match.

I then audited the instance *method* against a sample of rows and it holds:
one-directional comparisons get one instance (L44 "exceeds", T21 "larger than");
two-directional get two (T22, T3, T14, L21, L30, F17); layout-varying quantities
get three (L44, T21, T26) or six when crossed with direction (T3, T14, T22);
checksum comparisons get one with no direction (T1, L37, L38, F14). L2's nine
derived quantities are complete — I checked that the in-tile ordinal (≤ P−1),
the spatial ordinal (≤ N−1), `F_c` (≤ Q), the value offset (≤ P·Q), `G_i`
(≤ E_i) and `20·k` are each dominated by a listed term, and that `⌈P/8⌉ ≤ P`
cannot overflow, so its correct omission is not an oversight. L1's eight fields
correctly exclude `A` and `A_slab`, which are not "offset, length, extent, or
count" under §4.2 and are bounded instead by L39/L29; and F2 correctly excludes
`file_id`, which is an identifier and not a count.

**Identifier hygiene.** Every prefix is gap-free (`ENC` shows 17–99 "missing"
only because `[R-ENC-100]` is §2.2's illustration; `SER-04` is present as the
withdrawn identifier §14.4 retires). No register row cites an identifier that
does not exist. I spot-checked ~20 rows against their governing rules' text and
found no row whose governing rule fails to say what the row says.

**Modal casing.** I scanned every non-blockquote line for lowercase BCP 14 words.
The only hits outside notes and non-normative appendices are §8.2's "Verification
is not optional" (a statement of fact plus a definitional consequence, not a
permission) and §18.4's table cells "optional `unit`" (descriptive). The
lowercase-vs-ALLCAPS trap that took rounds 17 and 18 is not present in normative
prose that I could find. §21.7's one sentence carrying `MUST` and `SHOULD` in two
clauses of `[R-WRT-06]` is discussed at finding 04 — it is deliberate and the
two modals attach to genuinely different obligations.

---

## 2. Building it

### 2.1 The encoder and the eleven files

`tarn.py` implements front block, trailer, record framing, layer inline payload,
index region + segment CRC array, and sentinel. `verify.py` implements the checks
of §19.1 (open), §19.3 (layer access), §19.4 steps 3–7 (index chain, entry
classification, payload CRC, codec-1 decode, filter-2 inverse), §14.5's padding
content and §14.3's pad bits, §9.7's coverage walk and slack total, and §15.3's
full entry table. Roughly 60 register rows are implemented.

| file | construction | my verifier's verdict |
|---|---|---|
| `min.tarn` | Appendix A's 128 bytes | conforming, slack 44 |
| `full.tarn` | 1 layer, rank 1, E=100 T=32, one float32 channel, tiles 0 and 3 stored under codec 1, tile 3 carrying 28 fill-encoded padding positions | conforming, slack 47 |
| `zeroslack.tarn` | 128 bytes, **zero slack**: dir `[16,64)` = one experimental type-0x8000 MU=0/PE=0 record with a 20-byte inline payload, ending exactly at F−64 | conforming, slack 0 |
| `emptylayer.tarn` | layer with E=0, entry_count 0, extent slot (0,0), `crc_of_crc_array` 0 | conforming |
| `lz4empty.tarn` | codec 4 declared on an E=0 layer with T=2⁴⁰ (decoded size would be 2⁴⁰ ≫ 0x7E000000) | conforming — §17.2's Note is exactly right |
| `overflow.tarn` | E=0 layer, two dims with T=2³² each, so P = 2⁶⁴ | L2 reject-layer — §17.2's Note again: the cap is quantified over addressed tiles, `[R-ENC-04]` is not |
| `dirfirst.tarn` | directory at offset 16, tiles and index placed *after* it | F7 ×2, reject-file |
| `erased.tarn` | index region overwritten with 0xFF (erased flash) | L37 reject-layer |
| `erased_repaired.tarn` | 0xFF entries with the whole CRC chain recomputed | T6 ×4 — §15.2's rationale holds |
| `zeroed_repaired.tarn` | zeroed entries with the chain recomputed | T10 ×4 — the other half of §15.2's rationale holds |
| `mimic.tarn` | a stored tile whose first 64 bytes are a byte-perfect valid trailer | conforming — inert, exactly as §21.6 records |

The `zeroslack.tarn` construction is worth stating explicitly because the
charter asks for degenerate-but-legal files: a conforming TARN file can have a
slack total of **zero**, and the only way to reach it at 128 bytes is with an
experimental-range record. `[R-CNT-21]`'s "a verifier that reaches a live state
MUST report the total number of slack bytes" is satisfiable with 0. Compacting
that file would *increase* its slack to 44, since §20.4 lets a compactor drop
the MU=0/PE=0 record. That is not a defect, but it is a case worth a vector.

### 2.2 Where I had to guess while implementing

Seven places. All but two resolved cleanly out of the document.

1. **Inverting §11.4's spatial ordinal.** `[R-GEO-06]` gives `s = Σ tᵢ·∏_{j>i}Gⱼ`
   forward only. To classify padding positions I need `tᵢ` from `s`. Derivable
   (`tᵢ = (s div ∏_{j>i}Gⱼ) mod Gᵢ`) and unique because `0 ≤ tᵢ < Gᵢ`. No guess.
2. **Which channel a planar entry carries.** `c = k div N` from `k = c·N + s`.
   Derivable. No guess.
3. **Check ordering inside layer validation.** `[R-RDR-03]` lists checks without
   ordering them. If `layout` is 3, the addressed-tile count is undefined — is it
   `N` or `C·N`? I guessed `C·N`. It cannot matter: L36 already rejects the layer,
   and the outcome is reject-layer either way. Not reportable.
4. **Decoded size for a planar bool plane.** §14.2's table has no row for it;
   §14.3 supplies `⌈P/8⌉` and §14.3's closing sentence ("Whichever of §14.2 or
   §14.3 defines a tile's decoded size") stitches them. No guess.
5. **Byte-shuffle stride for a planar bool plane.** §17.3 says `s = 1`, identity.
   No guess. I also confirmed `L` is divisible by `s` in all four cases
   (`P·Q / Q`, `P·Bᶜ / Bᶜ`, `⌈P/8⌉ / 1`, and the interleaved-bool case where
   `Bᶜ = 1` folds into `Q`).
6. **Whether §20.3 step 4 permits changing a channel's type at equal element
   size.** Genuine guess. Finding 05.
7. **Whether a planar layer may drop a channel while it stores tiles.** Genuine
   guess; the answer bears on §23.1's enumeration. Finding 02.

---

## 3. Attacks

Below: the concrete construction, both verdicts, and the sentence that decides.
Attacks that were foreclosed are reported as foreclosed, with the sentence.

### 3.1 Front-block residency — the reader/reader divergence

**Construction.** `full.tarn` with byte 0 changed from `0x89` to `0x88`.

**Two verdicts.** Reader A memory-maps the file, so `[0,16)` is resident: it
*MUST* verify by equality and reject-file (F6). Reader B `pread`s only
`[F−64, F)` and then the directory: `[0,16)` is not resident, so it MAY omit the
check, accepts, and serves tiles. Both are conforming readers and both can defend
the verdict.

**Foreclosed.** Deliberately, and twice. `[R-CNT-04]`: *"A reader that would have
to issue a further range request to obtain those bytes MAY defer or omit the
check … The test is residency, not transport, so an implementation decides it at
its own open path without having to classify the network underneath it."* And the
charter's target is two *verifiers*, which this is not: §2.3 makes a verifier
*"A reader that additionally checks every file-level requirement — including
those ordinary readers are exempted from"*, and F6's own row says *"a verifier
holds no such exemption (§2.3)"*. Both verifiers reject. No fork.

### 3.2 A structure in the pre-trailer gap

**Construction.** `dirfirst.tarn`: directory at 16, a 4-byte stored tile at 128,
index region at 132, trailer at 256. Every reader-tier check passes; the tile
reads correctly.

**Two verdicts.** A reader serves it. A verifier reports reject-file.

**Foreclosed.** `[R-CNT-05]`: *"A verifier MUST treat a structure in that gap as
a validity error at file scope … (readers check neither, their check being the
dir-bounds rule of `[R-CNT-06]`)."* F7 registers it, detector *verifier*. This is
the reader/verifier seam working as designed, not a fork between verifiers.

### 3.3 A longer-than-necessary pre-trailer pad

**Construction.** `min.tarn` grown to F = 4096 with dir still at `[16,20)`.

**Two verdicts.** Verifier A: `[R-LIF-02]` step 5 pads *to the next 64-byte
boundary*, so a 4,032-byte gap is not what any conforming commit produces →
nonconforming. Verifier B: conforming.

**Foreclosed, in two places.** `[R-CNT-05]`: *"a longer gap is conforming, and no
conforming commit produces one."* And `[R-CNF-02]` names it explicitly among the
writer obligations that are not file-conformance violations: *"§6.3's flags = 0
against a set ignore-lane bit and §6.2's pre-trailer gap longer than
`[R-LIF-02]` step 5's pad are the cases this text states."* B is right. There is
correctly no register row.

### 3.4 Overlap taxonomy

I built the four overlap shapes and checked each against `[R-CNT-13]` and §15.3:

- two stored extents of one layer → reject-layer (§15.3 row, L18);
- a stored extent over its own layer's index region → reject-layer (named
  explicitly in both `[R-CNT-13]` and the §15.3 row);
- a stored extent over another layer's anything, or over the directory →
  reject-file (§15.3 row, F33);
- two layer records whose extent slots address the *same* index region (legal
  names, different layers) → two extent slots overlapping across layers →
  reject-file, F33 instance "tile-index regions".

All four decided. The last is the interesting one because a reader will happily
serve both layers off one index; `[R-CNT-13]`'s parenthetical *"(readers are not
obligated to detect overlap, which requires whole-directory knowledge)"* covers
it. Not a fork.

### 3.5 Non-isolable rows

**Construction.** `dir_offset = 2⁶²`, `dir_length = 2⁶²`. The sum is 2⁶³, which
exceeds 2⁶³−1 (F3) — but since `F ≤ 2⁶³−1`, the sum also exceeds `F−64` (F10).
F3's dir instance can never fire alone. Same for F3's record-extent instance
(always co-fires with F32), and for T12 (always co-fires with T9).

**Foreclosed.** `[R-VEC-02]`: *"where a condition cannot be isolated — §6.2's
field gates are validated together, so a file failing two of them attributes to
neither alone — the entry records every row the file exercises and says which it
was built for."* And both rows carry the same outcome, so `[R-ERR-02]`'s
"expected outcome is that row's outcome" is satisfiable. Not a defect; worth a
note to whoever builds the corpus.

### 3.6 The malformed interleaved boolean byte

**Construction.** Interleaved layer, one bool channel, stored tile carrying
`0x02` at a real position.

**Two verdicts.** Reader A returns the raw byte `0x02`. Reader B returns `0x01`
(true). Both claim `[R-SER-08]` compliance — A because §3.2 says *"sample values
are bit patterns"*, B because `[R-SER-08]` says *"MUST report 0x00 as false and
every other byte as true."*

**Foreclosed.** `[R-TYP-04]`: *"the one case where a reader resolves a byte to a
value rather than passing it through arises only in a nonconforming file, and
`[R-SER-08]` states it."* "Resolves … rather than passing it through" forecloses
A. Reader B is right. This one took me two passes; the deciding phrase is in
§12.3, four sections away from the rule it decides, but it is there and it is
unambiguous.

I also checked the T2/T4 partition: the same `0x02` at a *padding* position is
T4's (fill mismatch), not T2's, and T2's row says so — *"the same byte at a
padding position is T4's, the two rows together covering `[R-SER-08]`"*. Clean.

### 3.7 Codec-4 on an empty layer, and P·Q on an empty layer

**Constructions.** `lz4empty.tarn` (codec 4, E=0, T=2⁴⁰) and `overflow.tarn`
(E=0, P = 2⁶⁴).

**Two verdicts** for each, and both decided by one Note in §17.2: *"The cap is
quantified over the layer's *addressed* tiles, so a layer that addresses none …
satisfies it whatever its tile shape declares … `[R-ENC-04]`'s overflow rule
carries no such quantifier — it binds any sum or product a file yields — so P·Q
and P·Bᶜ are checked in an empty layer even though this cap is not."* Exactly the
distinction my two files probe, stated in one sentence. Foreclosed.

### 3.8 Verifier verdict divergences that are anticipated

Three constructions where two verifiers report different *verdicts* and the
document says so on purpose, so none is a defect:

- **Experimental-range MU=1 record** (`expmu1.tarn`). A verifier implementing the
  private type certifies *conforming*; one that does not reports *cannot
  establish*. §2.3 lists exactly this ground; §21.6 says *"`[R-CNF-02]` makes the
  file conforming all the same."*
- **A 20 MiB user-metadata document.** A verifier with a 16 MiB bound declines →
  *cannot establish*; one with a larger bound certifies. `[R-MTA-09]`: *"the
  bound is that verifier's capability and not a limit on validity
  (`[R-CNF-10]`), so the decline is not a finding that the file is nonconforming
  and a verifier MUST NOT report it as one."*
- **A zstd window above 8 MiB.** `[R-COD-06]`: *"a wider window is conforming and
  merely permits a conforming reader to decline the tile or the layer on resource
  grounds (`[R-ERR-04]`)."*

In all three, neither verifier says *nonconforming*, which is what the charter's
target requires.

### 3.9 Sentinel and index degeneracies

Confirmed against `[R-IDX-02]`/§15.3 with `erased_repaired.tarn` and
`zeroed_repaired.tarn`. The all-0xFF region with a repaired CRC chain gives T6 on
every entry (a sentinel's crc must be 0); the zeroed region with a repaired chain
gives T10 (`length = 0`, non-sentinel). §15.2's rationale predicts both by name.
I also confirmed that `[R-IDX-02]`'s carve-out ("`[R-ENC-03]`'s value-domain rule
… apply to the fields of non-sentinel entries only") does not create a hole: an
entry with `offset = length = S` but `crc ≠ 0` is *not* a sentinel entry by
§15.2's definition, so it is non-sentinel, so both T6 and T11 could be argued —
and both give reject-tile. No fork.

### 3.10 Slab run continuity across a damaged entry

**Construction.** Slab layer, S = 8, A_slab = 4096; run 1 holds ordinals 8–15
with ordinal 10 structurally invalid (`offset = 12`, below 16) and ordinal 12
well-formed but with a wrong `crc`.

**Two verdicts.** Verifier A closes the run over *both* damaged entries and finds
packing intact. Verifier B closes over neither and reports L41.

**Foreclosed.** `[R-SLB-03]` decides both cases in adjacent sentences: *"So are
the entries §15.3 classifies reject-tile on a *structural* ground: they address
no usable extent, and the run's stored tiles close over them. An entry whose only
defect is that its stored bytes fail its crc is not transparent — its offset and
length stand, and the packing relation reads them as it does any other stored
tile's."* The correct behaviour is: close over ordinal 10, do not close over
ordinal 12. My verifier does that. This is the tightest piece of the document I
tested and it is right.

I also checked the claim that follows — *"so this invariant stays decidable from
the index entries alone"* — and it holds: whether an entry is transparent depends
only on its own 20 bytes plus `F`, never on fetching the payload.

### 3.11 Zero-length structures

Systematically: `(0,0)` extent slot = no extent, legal; any other half-zero
combination invalid (F30/L15); stored tile length 0 → T10; directory of exactly 4
bytes = zero records, legal (§7.1, Appendix A); index region of 0 bytes at
entry_count 0, legal (`[R-CNT-17]`'s "and 0 when entry_count is 0");
user-metadata extent below 5 → F22/L11; layer inline payload of 0 → L23; and a
24-byte record with `inline_length = 0` and no extent, which is legal for an
experimental type. `[R-COD-08]`'s Note closes the loop: *"Decoded output is never
empty … the index rule that a zero-length non-sentinel entry is invalid (§15.3)
rests on both facts."*

Minimum viable user-metadata extent is 6 bytes (`{}` + CRC) under encoding 1;
extent_length 5 is *structurally* legal but always ends in ignore-record (R7),
which is consistent and not a defect.

### 3.12 Register completeness

I walked every "validity error" / "reject-*" sentence in §1–§20 (49 of them) and
matched each to a row. Tile scope: `[R-CNT-20]`→T1, `[R-SER-07]`→T3,
`[R-SER-05]`→T4/T5, `[R-SER-08]`→T2, `[R-IDX-03]`'s six structural rows→T6–T12,
`[R-COD-02]`→T13, `[R-COD-04]`→T14, `[R-COD-05]`→T15/T16,
`[R-COD-06]`→T17–T22, `[R-COD-07]`→T23 (with the cap at L44),
`[R-COD-08]`→T24/T25, `[R-COD-10]`→T26. Complete. Layer scope and file scope
likewise; I found no MUST-level, file-detectable condition without a row. §4.5's
checksum-coverage exception list matches §8.1's map exactly (three terminal
fields, three interior fields, front block, unassigned-type extent).

This is why my findings below are all in explanatory and enumerative text rather
than in the rules: the rule surface, as far as I could reach it in one walk, is
closed.

---

## 4. Findings

Six. None is byte-level, and I say so for each rather than reaching.

---

### adversary-01 — AMBIGUITY

**§20.5, `[R-WRT-06]`** — the parenthetical `(F36, L25, R1)` reads as the set of
reserved-range violation rows and is not that set under either available reading.

> Where the output carries a feature a later minor defines and this compactor
> does not — on a conforming input a carried ignore-lane bit (§6.3) or an
> unrecognized `tarn.` key in a record it never decoded (§18.3), the two of
> §10.1's four vehicles §21.6 makes conforming, the other two reaching such a
> file only as values this text still registers as reserved-range violations
> (F36, L25, R1) — the output's version_minor SHOULD be at least the input's

The substantive argument is sound and I checked it: of §10.1's four growth
vehicles, exactly two — new ignore-lane flag bits and new standardized `tarn.`
keys — appear in §21.6 as conforming, and vehicles 1 and 2 (new record types, new
reserved-range values) can only reach a file as reserved-range values. That part
survives.

The row citation does not. Two readings of "such a file":

*Reading A — "such a file" is the compactor's **output**.* Then the cited rows
should be the reserved-range violations that can survive into an output the
compactor emitted. F36 and L25 qualify: their detector is *verifier*, so a
compactor performing §19.1's open and §19.3's layer validation does not detect
them and carries the record forward under `[R-WRT-01]`. **R1 does not qualify.**
R1's Detector cell is *reader* and its Detected cell is *"open (top-level); layer
access (sub-record)"*, so a compactor — which is a reader of every structure it
processes — detects it, and `[R-WRT-06]`'s own *"MUST NOT emit a file carrying a
violation it has detected"* plus §20.4's PE = 1 on type 0x0002 (no drop
available) force refusal. Under reading A, R1 is cited wrongly.

*Reading B — "such a file" is the **conforming input**.* Then the citation is
missing six rows. Vehicle 2 spans all eight spaces of §10.2's table, and a
reserved-range value in any of them is registered: L31 (index encoding), L33
(linearization), L34 (sample type), L36 (channel layout 3–255), L43 (codec),
L45 (filter) — in addition to F36/L25 (record type) and R1 (metadata encoding).

**Which I picked and why.** Reading A, because the surrounding sentence is about
what the output carries ("Where the output carries a feature…"), and because the
two conforming vehicles named just before are both described from the output's
side ("a carried ignore-lane bit", "a record it never decoded"). Under that
reading the sentence should cite F36 and L25 and not R1.

**What an implementer does wrong without it.** Reads the parenthetical as the
inventory of reserved-range violation rows and concludes that a reserved-range
*codec* or *sample type* is not a registered violation — it is (L43, L34) — or,
under reading A, builds a compactor that emits an output carrying an
encoding-0x40 user-metadata record, believing R1 is a survivable class. It is
not: R1 is reader-detected at open, and `[R-WRT-06]` obliges refusal.

**Byte-level: no.** L31/L33/L34/L36/L43/L45 and R1 each state their own condition
in their own section and their own row; §21.1 already fixes that *"where a row
and the rule it cites diverge, the rule governs"*, and no verifier's verdict
turns on this parenthetical. The cost is to a reader of §20.5, not to a file.

---

### adversary-02 — AMBIGUITY

**§23.1, `[R-PRV-01]`** — a closed two-item enumeration of how a commit removes
sample data, with a third way available under §20.3 step 4.

> A commit removes sample data two ways — superseding it, and a shrink that
> de-addresses tiles (§20.3 step 4) — and a dropped ancillary record's extent
> (§20.4) goes the same way; no commit removes a layer at all.

The third way is **dropping a channel from a planar layer**. §20.3 step 4's bar
is stated in full generality — *"A commit MUST NOT change a layer's declarations
in a way that alters, for any tile that layer stores in the generation this
commit supersedes, what §14 fixes for its stored bytes or how they decode"* —
and a trailing-channel drop on a planar layer alters nothing it names:

- disk ordinals of the surviving channels are `c·N + s` with `N` unchanged, so
  no surviving stored tile moves in the entry array;
- each surviving plane's decoded size (`P·Bᶜ`, or `⌈P/8⌉` for bool) is unchanged;
- padding-position set and `[R-SER-05]` content unchanged;
- codec and filter unchanged; the filter's mandated stride for a planar plane is
  that channel's element size, also unchanged.

The dropped channel's tiles simply leave the addressed set, which step 4 itself
declares is not an alteration: *"Dropping a tile out of the addressed set … is
not itself such an alteration — a tile the new state does not address carries no
§14 obligation and its extent becomes slack."* `[R-CNT-17]` then obliges the
smaller `entry_count` and a re-emitted index region — for C = 4 → 3 at N = 32,
128 → 96 entries and 2,564 → 1,924 region bytes. Nothing in §7.4, §11, §12, §20.3
or §20.4 bars a change to the channel count of a layer that stores tiles. Every
byte of the dropped channel's payloads becomes slack.

**Permitted readings.** (a) The enumeration is closed and exhaustive, so a planar
channel drop must be barred somewhere — but no sentence bars it. (b) The
enumeration is closed and *wrong by one*, and the MUST that follows is
nevertheless correct because it is scoped to *"any commit that makes sample data
unreachable"*, which reaches the channel drop.

**Which I picked and why.** (b). The requirement's own scope is general — that is
the widening the sentence carries — so the rule holds; it is the count "two ways"
that is short. Reading (a) would require inventing a prohibition the document
does not state, which `[R-CNF-04]` forbids a reader to do and which I will not do
on a writer's behalf.

**What an implementer does wrong without it.** Two things. An appender author
reads §20.3 step 4, sees growth and shrink discussed at length and channel-count
change nowhere, and either (i) refuses a legal operation, or (ii) performs it and
reports it to the caller as "removing channel 3", which is exactly the
representation `[R-PRV-01]` forbids — because §23.1's enumeration told them
erasure-misreporting was a concern for supersedes and extent shrinks only.

**Byte-level: no.** `[R-PRV-01]` binds how a tool *describes* a commit, not what
it writes; the resulting file is conforming under either reading, and §21.7
already places §20.3 step 4's bar among the obligations with no live-state
witness. Resolving this moves no byte and no verdict.

---

### adversary-03 — OBSERVATION

**Appendix G, item 8 and the closing paragraph** — the concession understates what
the profile leaves unpinned for a compactor.

> A compactor's output is therefore reproducible only modulo its trailer:
> `[R-WRT-06]`'s fresh file_id is no function of content, and this item's floor
> turns on which features the compactor implements.

"Only modulo its trailer" is accurate for the two causes it names — `file_id` and
`version_minor` both live in the trailer, and `flags` does not vary because item 8
sends a profile-adopting compactor to `[R-CNT-08]`'s carry-forward. But a third
cause sits outside the trailer entirely: §20.4's table gives a compactor an
**unconditional** drop licence that the appender does not have —

> A compactor MAY drop it whenever it rewrites the file.

— for any MU = 0, PE = 0 record. Such a record can occur in a conforming input:
the reserved range is barred by F36/L25 and both registered types carry PE = 1,
so the type must be experimental-range, which §21.6 records as conforming
(*"A record type this specification has not assigned, from the experimental range
(≥ 0x8000, §10.2), carries MU = 0 | Ignored, and preserved or dropped per its PE
bit"*). My `zeroslack.tarn` is exactly such an input.

Nothing in items 1–10 pins the decision. Item 3 pins record *order*, not the
record *set*; item 9 pins user-metadata serialization; the closing paragraph's
inventory of what the profile adds — gap content, gap extent, record order, the
default fill, the all-fill sentinel, one generation, alignment/slab, the
`version_minor` floor, the derived `file_id`, NFC names, producer pinning — does
not mention the drop licence. So two compactors both adopting the profile, given
the same conforming input, can emit directories that differ by a whole record and
files that differ in length, order and every offset after the drop point. That is
not "modulo its trailer".

**What an implementer does wrong without it.** Builds a content-addressed pipeline
on the promise that pinning the compactor's *identity* (as the concession's last
sentence advises: *"An adopter needing byte-identity across compactors pins the
compactor"*) is unnecessary for anything but the trailer — and then finds two runs
of the *same* pinned compactor version disagree if the drop decision is
configurable, or two pinned compactors disagree structurally rather than in eight
bytes. The correct advice is either "the profile also requires a fixed drop
policy" or "pin the compactor", and the text gives the second only as a remedy for
the trailer.

**Byte-level: no.** Appendix G is labelled non-normative and adds no requirement
to any actor (*"It adds no requirement to any actor: a writer ignoring it is fully
conforming"*). Both compactors' outputs are conforming files that a conforming
writer may emit, so the emittable set is unchanged. The cost is to the profile's
own stated purpose, not to conformance.

---

### adversary-04 — AMBIGUITY

**§21.7, `[R-ERR-01]`** — "witnessed only where A *and* B", followed immediately by
two witness classes in which B is false.

> §20.3 step 4's bar on a declaration change is witnessed only where the affected
> tiles remain stored *and* the change reaches a byte §14 structurally
> constrains — a padding position, a pad bit, or a boolean byte — where §21.4's
> content rows fire; a change that reaches the decoded size instead is witnessed
> by T3 or T14, which test a length rather than the decoded image's content

The word *instead* marks the second conjunct as false in the second clause, and
the clause then asserts a witness. Read literally the sentence contradicts itself
within twenty words.

**Permitted readings.** (a) "only where A and B" is the necessary condition for
being witnessed *at all*, and the semicolon clauses are exceptions to it — a
contradiction. (b) The trailing "where §21.4's content rows fire" scopes the
"only": the bar is witnessed *by the content rows* only where A and B, and the
semicolon clauses list the other witnesses (T3/T14 for a decoded-size change;
T15/T17/T23/T25 or T14 for a codec change; nothing for the
supersede-everything case). (c) "only where the affected tiles remain stored" is
the sole necessary condition and the "and" opens the first case of a case list.

**Which I picked and why.** (b), reinforced by (c) — they agree on every
consequence. Both are supported by the sentence's own tail, which ends with the
one genuinely unwitnessed case and by §20.3 step 4's forward reference to it:
*"§21.7 records the consequence — that this is precisely where the bar has no
witness, the live state being clean."* If reading (a) were intended, that forward
reference would be false, since step 4 says the unwitnessed case is
supersede-everything and not "any change that misses a structurally constrained
byte". I verified reading (b) constructively: a `float32 → float64` change on a
layer with a stored codec-1 tile leaves the entry length at 128 while the derived
decoded size becomes 256 → T14 fires, with no structurally constrained byte
involved.

**What an implementer does wrong without it.** Builds a verifier that skips T3 and
T14 on layers whose channels are all numeric and whose tiles have no padding
positions, on the theory that §21.7 has told them a declaration change is
unwitnessed there. It is not — T14 fires from the index entry alone, before any
payload fetch.

**Byte-level: no.** §21.7 carries no rows (§21.1: *"The subsections after §21.5
are not part of the register and carry no rows"*), and T3/T14 are stated
independently in §21.4 with their own governing rules. A verifier built from
§21.4 rather than from §21.7's prose is unaffected.

---

### adversary-05 — AMBIGUITY

**§20.3 step 4, `[R-WRT-04]`** — the bar's criterion and the bar's gloss disagree
about a channel type change at equal element size.

> The test is the effect on such a tile, and the list names where that effect
> arises rather than standing on its own: a change that leaves every one of those
> tiles' stored bytes meaning exactly what they meant — a filter whose mandated
> stride makes it the identity (`[R-COD-10]`), or a new padding position whose
> stored byte already holds the fill `[R-SER-05]` fixes — is not what this bars.

**Construction.** A layer with one `int32` channel, interleaved, codec 1, filter
1, no padding positions, storing tiles. A commit re-declares the channel type as
`float32`. Element size 4 either way, so: `Q` unchanged, decoded size `P·Q`
unchanged, every sample's byte offset unchanged, padding-position set unchanged
(empty), `[R-SER-05]`'s content vacuous, codec and filter unchanged, and the
byte-shuffle stride (if filter 2) unchanged. `[R-CNT-23]` requires the fill length
to equal the element size — 4 either way — so the recorded fill bytes can stay
byte-identical.

**Permitted readings.** (a) The criterion governs: the change alters nothing *§14*
fixes for the stored bytes or how they decode — §14 fixes the value sequence's
identity and each value's *encoding width and endianness*, while §12 assigns the
bit pattern its meaning — so the commit is **permitted**, and every stored sample
is silently reinterpreted. (b) The gloss governs: the bytes no longer "mean
exactly what they meant", so the commit is **barred** and the caller must write a
new layer or a new file.

**Which I picked and why.** (a). The gloss is introduced as a *narrowing* device —
its two examples are both cases where an item on the list is touched but the
effect is nil, and its verb phrase is "is not what this bars". A device that only
subtracts cannot add one. Reading (b) also creates a violation class with no live
witness that §21.7's account does not cover: §21.7 says the bar is unwitnessed
only where "a commit that supersedes every tile it would have damaged leaves the
live state clean", whereas a barred-under-(b) type swap leaves the live state
clean without superseding anything. §21.7 therefore argues for (a).

That is an inference across three sections, and I had to make it to write an
appender. The document nowhere says whether a channel's *type* is among the
declarations a commit may change over stored tiles.

Note that the neighbouring case *is* decided, and decided the other way:
`uint8 → bool` on an interleaved layer passes every item on the list — same
element size 1, same `Q`, same decoded size, same offsets, and a `0x00` fill
stays `0x00` — but it retroactively subjects every stored value byte to
`[R-SER-08]`, so previously legal bytes like `0x7F` become T2 violations. The
general criterion catches it ("what §14 fixes for its stored bytes"), and §21.7
names "a boolean byte" as one of the witnesses. That the bool case is decided and
the numeric case is not is what makes this reportable rather than pedantic: an
implementer who works out the bool case from the criterion has no reason to think
the criterion stops short of the numeric one.

**What an implementer does wrong without it.** Under (b) an appender refuses a
legal in-place reinterpretation and forces a whole-file rewrite of a large layer;
under (a) it performs a commit that silently changes every sample value a
consumer sees, with no diagnostic and no witness in the file. Two appenders given
the same input and the same caller request emit different bytes.

**Byte-level: no.** Both outcomes are conforming files — the permissive one is a
file a *creator* could have written from scratch — so the conforming set is
unchanged and no verifier's verdict moves. This is the same class §21.7 already
concedes for §20.3 step 4: an obligation on a commit, not on a file.

---

### adversary-06 — OBSERVATION

**§21.7, `[R-ERR-01]`** — the new `[R-WRT-06]` entry names one of two identical
unwitnessed obligations.

> §20.5's two obligations on a compacted file's trailer (`[R-WRT-06]`) — the
> unknown ignore-lane bits it MUST carry forward, and the floor its version_minor
> SHOULD take — are unwitnessed for that same reason, the output carrying no
> record of its input's flags or its input's minor

`[R-CNT-08]` places the *same* obligation on an appender, in the same terms:

> An updater MUST copy forward unknown ignore-lane bits of the file it modifies
> and MUST NOT clear them

It is unwitnessed for precisely the reason §21.7 gives for the compactor's: the
new generation's trailer carries no record of the prior trailer's flags, and §9.7
does not reconstruct history. `[R-CNT-26]`'s appender floor (*"an appender the
maximum of that floor and the prior trailer's minor"*) is the SHOULD-side twin,
also unwitnessed and also unnamed. §21.7 names neither.

Both are arguably covered by the paragraph's opening class — *"Committed-prefix
immutability and the generation sequence (`[R-LIF-01]`, `[R-LIF-03]`) are
properties of a file's history, which §9.7 does not reconstruct"* — but that
sentence names two specific identifiers rather than describing a class open to
membership, and §21.1 calls §21.7 *"the account, by class, of what fails"*
detectability. Once the compactor's twin is named explicitly, an implementer
auditing §21.7 for "which of my writer obligations have no test" will find the
compactor case listed and the appender case absent, and may reasonably infer the
appender case is testable. It is not.

**What an implementer does wrong without it.** Writes a conformance vector for
"appender clears an ignore-lane bit" and cannot state its expected outcome,
because the output file is conforming — which `[R-VEC-02]` then classifies as
*"a finding against this document rather than a vector"*.

**Byte-level: no.** `[R-CNT-08]`'s obligation is stated in §6.3 and binds the
appender whether or not §21.7 lists it; nothing about which files are conforming
changes.

---

## 5. Honest ranking

By the likelihood a real implementation lands on the wrong side:

1. **adversary-05** (§20.3 step 4, type change at equal element size) — highest.
   Anyone writing an appender that supports schema edits must decide this on day
   one, and the two readings sit one sentence apart. It is also the finding
   furthest from anything this round changed, which is where the brief says the
   marginal value is.
2. **adversary-02** (§23.1's "two ways") — a planar channel drop is a plausible
   product feature ("drop the alpha plane"), and the enumeration is what an
   implementer will consult for the privacy obligation.
3. **adversary-01** (§20.5's row citation) — a compactor author reads exactly this
   paragraph when deciding what to refuse on.
4. **adversary-03** (Appendix G's concession) — only bites an adopter of a
   non-normative profile, but bites hard when it does.
5. **adversary-04** (§21.7's "only where") — recoverable by careful parsing; the
   forward reference from §20.3 disambiguates it.
6. **adversary-06** (§21.7's omitted twin) — an asymmetry, not an error.

## 6. What I could not determine

- Whether §20.5's `(F36, L25, R1)` was meant as an exhaustive citation or an
  illustrative one. Both readings leave it wrong in a different way, which is why
  I reported it; but I cannot tell which repair the authors want.
- Whether the compactor drop licence in §20.4 is deliberately left unpinned by
  Appendix G (on the theory that "pin the compactor" already covers it) or was
  overlooked when the concession sentence was written.
- Whether §20.3 step 4's silence on channel-type changes is intentional
  permission or an unconsidered case. The gloss's wording suggests the authors
  had "meaning" in mind; the criterion's wording says §14, and §14 does not fix
  meaning.

## 7. Empty result claims

I found no attack that produces two conforming verifiers reporting *conforming*
and *nonconforming* on the same bytes. Every candidate I built was decided, and
in eight cases the deciding sentence was placed exactly where the attack lands —
§17.2's Note for the lz4-cap-on-an-empty-layer pair, `[R-SLB-03]` for the
run-continuity-across-damage pair, `[R-CNT-04]` for the residency pair,
`[R-CNF-02]` for the long-pad pair. The three verdict divergences I did find
(§3.8) are all *conforming* against *cannot establish*, which §2.3 explicitly
constructs and explicitly declares not to be a finding about the bytes.
