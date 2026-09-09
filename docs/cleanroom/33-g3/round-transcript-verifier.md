# Cleanroom round 33 — Verifier implementer — working transcript

## 0. Disclosure

I read exactly one file: `/Users/robertkleffner/Documents/GitHub/tarn-first-draft/spec/tarn.md`
(4,805 lines, 47,853 words per `wc`). I opened no ADR, no `docs/`, no
`conformance/`, no `registry.json`, no `PLAN.md`/`AGENTS.md`/`README.md`, no git
history. I ran no web search or fetch. I did not list any directory other than
creating my own scratch directory. I did not read the output directory.

The path in the brief was correct: the spec was where I was told it would be.

**Context I did not ask for.** My runtime placed a `CLAUDE.md` project-instruction
pointer and a block of the maintainer's auto-memory index in my context before I
began. The memory index carried entries naming this project's round structure, a
harness spec path, a lineage gate, repair-vs-diff discipline, and a note about
subagent models. I disregarded all of it. None of it named a spec section, a
requirement identifier, or a finding, and no conclusion below came from it. I
record its appearance here because the brief requires it.

Files I wrote (all in
`/private/tmp/claude-501/-Users-robertkleffner-Documents-GitHub-tarn-first-draft/r33-round/scratch/verifier/`):

- `crc32c_verify.py` — CRC-32C implementation and reproduction of every checksum
  constant the document states.
- `count_register.py` — mechanical row and instance counts over §21.2–§21.5.
- `build_trace.py` — a four-generation TARN file built byte-by-byte with real
  CRCs, and a paper verifier run over each generation.

Plus this transcript, at the single output path named in the brief.

---

## 1. What I built

I implemented, on paper and then concretely in Python, a **conforming verifier**:
the ordered certification procedure of §2.3/§9.7, the coverage walk of
`[R-LIF-08]`, the overlap/alignment/slab invariants of §7.2 and §16, the checksum
chain of §8, and the decoded-content obligations of §14. I then drove it over a
file I constructed myself across four generations — creation, append, metadata
edit, compaction — and over a fifth run in which the walk deliberately does not
complete.

Everything below that carries a number was derived by me and then compared
against what the document states. I did not take a number from the document and
call it checked.

---

## 2. The certification procedure, as an ordered algorithm

Assembled from §2.3 `[R-CNF-11]`, §2.4 `[R-CNF-12]`, §19.1–§19.4, §9.7
`[R-LIF-08]`, §5.2 `[R-CNT-21]`, `[R-COD-11]`, `[R-MTA-09]`, `[R-MTA-10]`,
`[R-ERR-04]`, and Appendix H's checklist (non-normative, cited only as a
cross-check).

**Verdict vocabulary.** Exactly three verdicts — *conforming*, *nonconforming*,
*cannot establish* — plus two report-only annotations that are not verdicts:
per-requirement *unable to check* (naming requirement and ground) and per-scope
*unexamined*. §2.3 is explicit that both "constrain the report, not the verdict".

**Availability, as the text fixes it.**

| Verdict | Available when |
|---|---|
| nonconforming | any violation established. Takes priority over every unable-to-check ("however many requirements it was unable to check"). |
| cannot establish | no violation established **and** some requirement unable to be checked on a capability or resource ground. Certification barred (`[R-CNF-11]`, `[R-COD-11]`, `[R-MTA-09]` each say MUST NOT certify). |
| conforming | no violation established and nothing unable to be checked. `[R-CNF-12]`: "a verifier certifies only violation-free files"; §9.7: "MUST NOT certify past a violation it has not looked for". |

The cannot-establish grounds in §2.3 are introduced by "**as when**", so the list
is illustrative and the operative test is the general one — "some requirement is
one it is unable to check on a capability or resource ground". This matters: a
verifier that declines a tile's decode on a layer with *no* §14 content
obligation (no padding positions, no bool channels) is not covered by §2.3's
fourth example, whose stated consequence is "and so cannot check §14's
decoded-content obligations" — but §9.7 still requires the decode, for §21.4's
codec rows, and the general test reaches it. **I checked this and it holds only
because of "as when."** Had that phrase been "namely" or "in the following
cases", the ground would have been missing. I record it as a near miss rather
than a finding.

**Ordered algorithm as I implemented it.** Numbering follows §19.1's tiers, with
the verifier-only checks folded in at the tier where the structure they read
becomes available.

0. **Residency / front block.** §19.1 step 1. `[R-CNT-04]` lets an ordinary
   reader that would have to issue a further range request defer or omit the
   byte-equality check. **A verifier holds no such exemption** — §2.3 ("including
   those ordinary readers are exempted from"), F6's Condition cell, and Appendix
   H all say so. So: fetch [0,16) if needed and compare against
   `89 54 41 52 4E 0D 0A 1A` + 8 zero bytes. Failure: F6, or F1's front-block
   instance where the 8 magic bytes are stored reversed. reject-file.
1. **Trailer, in §6.2's fixed order.** magic → trailer CRC → version gate → then
   all remaining gates before acting on the fields: flag gates;
   committed_file_length = transport-authoritative size and ≡ 0 (mod 64);
   dir_offset ≥ 16; dir_length ≥ 4; dir_offset + dir_length ≤ F − 64 (a
   declaration-derived quantity under `[R-ENC-04]`); file_id ≠ 0; reserved [48,60)
   zero. Rows F8, F14, F18, F19, F17, F13, F9, F16, F10, F12, F15. Plus F5's
   128-byte floor (`[R-CNT-27]`).
   *This is the boundary for the slack total.* §5.2: where §6.2's ordered
   validation rejects before a live trailer is established, "there is no F and no
   live state to walk, so the total is not owed at all ... which is not a partial
   total but the absence of one."
2. **Directory region.** Verify the terminal CRC-32C over the preceding
   dir_length − 4 bytes before any other use (F20).
3. **Record walk.** §7.2 framing (F29, F24), MU gate for unknown top-level types
   (F35), multiplicity (F34), extent slots (F30/F31/F32), user-metadata framing
   (F21/F22/F23), layer-name namespace over raw bytes (F4). Verifier-only here:
   reserved flag bits (F26), MU = 1 with PE = 0 (F25), registered type's stored
   MU/PE against §7.3 (F28), reserved-range type value whatever its MU (F36).
4. **Per layer, §19.3's full validation**, all decidable from the resident
   directory and F: L1–L36, L39, L43–L47, L49. Verifier-only: L46, L47, L49,
   L25.
5. **Index chain per layer.** crc_of_crc_array over the fetched CRC array (L37),
   then each segment CRC over its entries as stored (L38). A verifier needs
   *every* segment, since the coverage walk reads every entry.
6. **Per entry, §15.3's classification.** T6, T7, T8, T9, T10, T11, T12; then T1
   over the stored bytes.
7. **Per stored tile, decode.** §9.7: "A verifier that certifies decodes every
   stored tile, whatever content obligations §14 places on the layer." T14 (codec
   1 length), T3 (decoded length), T17–T22 (zstd header), T24 (exact
   consumption), T25 (malformed stream); then the content obligations T2 (real
   interleaved bool bytes), T4 (padding positions), T5 (pad bits), and T26 by way
   of T2/T4.
8. **Per user-metadata extent.** R2 (terminal CRC), R1 (encoding value set), R4
   (frame constraints under encoding 2), R3 (decode failure), R5–R10 (document
   content), F27/L48 (member ordering, verifier-only). At an experimental-range
   encoding: no content rule attaches (`[R-MTA-10]`), certification unaffected,
   but the record MUST be reported — owning scope, encoding value, stored extent
   length.
9. **Coverage walk and slack total.** Below, §3.
10. **Placement invariants.** L40 (alignment), L41/L42 (slab), F7 (structure in
    the pre-trailer gap), F33/L18 (overlap).

**What bars certification, exhaustively:** any established violation (→
nonconforming); any requirement unable to be checked on capability or resource
grounds (→ cannot establish); and — this is easy to miss — a check the verifier
simply *did not look for*, which §9.7 forbids certifying past.

**Cross-check of the verifier-only set.** I extracted every register row whose
Detector cell says *verifier*: 20 rows — F7, F25, F26, F27, F28, F33, F36, L18,
L25, L40, L41, L42, L46, L47, L48, L49, T2, T4, T5, T26. Every one of them is
named in Appendix H's verifier checklist, and Appendix H names nothing that is
not a verifier row (it additionally names F1/F6, correctly, as reader rows from
which the verifier holds no exemption). Detected is *certification* for all 20.
No leaks in either direction.

**A dead branch I checked and closed.** `[R-COD-11]`'s "cannot execute a layer's
codec or filter" ground is unreachable for a *conforming* verifier: all four
codecs and both filters are core (`[R-CNF-03]`), so the only values it cannot
execute are reserved or experimental — and those are themselves layer-scope
violations L43/L45, making the verdict nonconforming, not cannot-establish. The
document says exactly this itself ("For a conforming reader that position arises
only at a reserved or experimental value ... software unable to execute an
assigned codec or filter is not a conforming reader"). Not a finding; the
document already knows.

---

## 3. The coverage walk, with the arithmetic

### 3.1 The partition, derived

§5.2 `[R-CNT-02]` gives the classes; §9.7 `[R-LIF-08]` gives the walk. Deriving
the claimant set myself from the structure the rule governs:

- the front signature block [0, 16) — a class of its own, not a "structure";
- the live trailer [F − 64, F);
- the live directory region [dir_offset, dir_offset + dir_length);
- every record's extent, whatever the record's type — which includes each layer
  record's tile-index region (§9.7 is explicit that the region "enters the walk
  once, as that record's extent, and is not a second claimant beside it") and
  each user-metadata extent, top-level or sub-record;
- the stored extent of each non-sentinel tile-index entry, **excluding** entries
  `[R-IDX-03]` classifies reject-tile on a *structural* ground, which contribute
  none.

A record is **not** a claimant of its own: its header and inline payload lie
inside the directory region. I confirmed this is necessary — without it every
record would double-claim directory bytes and F33 would fire on every conforming
file.

Checks: pairwise disjointness; every claimant other than the front block and
trailer within [16, F − 64); each verifies against the checksum §8.1 maps to it.
Then F7 separately — no claimant in [dir_end, F − 64), which is *inside* the
permitted range and so is not caught by the bound.

### 3.2 Which bytes are certified, which are counted-but-unconstrained

| Class | Content certified by | Status |
|---|---|---|
| front block [0,16) | byte equality against the constant | certified |
| trailer | its own CRC-32C at [60,64) over [0,60) | certified |
| directory region | terminal CRC over dir_length − 4 | certified |
| tile-index region | segment CRCs over the entry array; crc_of_crc_array over the CRC array; that field inside the directory, under the directory CRC | certified, transitively |
| stored tile extent | its entry's crc field | certified |
| user-metadata extent | terminal 4 bytes over the preceding bytes | certified *as bytes*; its **content** is unconstrained under an experimental-range encoding (`[R-MTA-10]`) |
| extent of a record of an unassigned type | **nothing** (§8.1's last row) | in the partition, counted, **wholly uncertified** |
| slack | nothing | counted only |

**Can any byte be neither?** No, and the reason is definitional rather than
empirical: the live committed state *is* what the walk reaches, and `[R-LIF-08]`
makes every byte the walk misses slack. §5.2's Note states this and draws the
right conclusion — "belongs to no class" describes nothing, and a register row
for it would be a row no file could exhibit. I verified against my constructed
files that the sum always closes exactly (§3.3).

The document's own summary of this, in §5.2's Note, is that "of this rule's two
halves, only disjointness is testable." I agree, and my implementation reflects
it: I test disjointness and compute the complement.

### 3.3 A concrete file, and the arithmetic

Layer `sst`: rank 1, dimension `x` with E = 100, T = 32; interleaved; one float32
channel `temp` with fill `0x7FC00000`; codec 1 (none), filter 1 (none); no
alignment, no slab.

Derived by me: G = ⌈100/32⌉ = **4**; N = 4; P = 32; Q = 4; decoded size = P·Q =
**128**; entry_count = N = **4**; index region length = 4·20 + ⌈4/65536⌉·4 =
**84**; layer-record inline payload = **81 bytes**. The document's §7.4 worked
example uses the identical layer and states 4, 4, 84 and 81. All four match, as
do its component sums (name 4, the nine scalars 34, dimension entry 18, channel
entry 12, trailing fixed 13 → 81).

Tiles 0–2 carry only real positions (coordinates 0–95); tile 3 covers 96–127, of
which 96–99 are real and **28 are padding positions**, each of which I encoded as
the recorded fill bytes `00 00 C0 7F` per `[R-SER-05]`. My verifier checks those
28 positions explicitly; T4 is the row.

**Generation 1 (creation).**

```
[0,16)      front signature block
[16,144)    tile 0        128 bytes
[144,272)   tile 1        128
[272,400)   tile 2        128
[400,528)   tile 3        128
[528,612)   tile-index region  84
[612,721)   directory    109  (= 24-byte header + 81 inline + 4 CRC)
[721,768)   pre-trailer pad     47   <- slack
[768,832)   trailer       64
F = 832, F mod 64 = 0
```

Claimed = 16 + 4·128 + 84 + 109 + 64 = **785**. **Slack total = 832 − 785 = 47**,
which is exactly the pre-trailer pad, and 721 padded to the next 64-byte boundary
is 768, so the pad is `[R-LIF-02]` step 5's, not a longer one. Verdict:
**conforming**.

**Generation 2 (supersede tile 1).** Writing begins at exactly F = 832.

```
[832,960)   new tile 1     128
[960,1044)  new index region 84   (one entry re-pointed, three byte-identical)
[1044,1153) directory     109
[1153,1216) pad            63
[1216,1280) trailer        64
F = 1280
```

F increased by 448 ≥ 128 ✓. Claimed = 785 again (the live set has the same
shape). **Slack = 1280 − 785 = 495.** Cross-checked against what commit 1 left
behind: old tile 1 (128) + old index (84) + old directory (109) + old pad (47) +
old trailer (64) = 432, plus the new pad 63 = **495**. The two derivations agree
exactly, which is the check that the walk's complement is the same set as
"everything an earlier commit superseded, plus the gaps".

**Generation 3 (add a file-scope user-metadata record).** Document
`{"tarn.creator":"tarnwrite 0.1","tarn.title":"sst"}` = 51 bytes, extent = 51 + 4
= **55** (≥ 5, so `[R-CNT-25]`'s floor is met; Appendix B's "extent_length ≥ 5"
constant reproduces). Members are in ascending UTF-8 byte order —
`tarn.creator` < `tarn.title` — so `[R-MTA-05]` holds and F27 does not fire.
F = 1536, claimed = 865, **slack = 671**. Verdict: conforming.

**Generation 4 (compaction).** Fresh file_id `0x0FEDCBA987654321`, drawn anew
rather than compared against the input's, per `[R-WRT-06]`. Every stored tile's
bytes carried verbatim, every index entry's crc unchanged. Because the output
relocates the stored extents, the index region is **regenerated** — entry offsets
new, lengths and crcs and sentinels unchanged, segment CRCs recomputed — and
crc_of_crc_array updated: 0x9854EDCE → 0xE93F1270 in my run. F = **896**, claimed
865, **slack = 31** (the output's own pre-trailer pad). 640 bytes reclaimed.

Two things worth stating, because a naive reader gets them wrong:

- A compacted file still has slack. §20.5's "slack is never carried" is about the
  *input's* slack; the output's own pre-trailer pad is new. Both §5.1's and
  §20.5's figures draw a `pad` in the output, so this is consistent.
- The reference arrays are identical bit for bit (`[R-MDL-02]`); I verified the
  four tile payloads compare equal between generations 3 and 4.

### 3.4 A walk that does not complete

I flipped one byte of tile 2's stored payload in generation 3. The entry crc now
fails: **T1, reject-tile**, detector reader, detected at tile use. The verifier
elects under `[R-CNF-11]` to stop at the first violation, having enumerated the
front block, the trailer, the directory, the index region, the metadata extent
and tiles 0 and 1.

Enumerated = 16 + 64 + 134 + 84 + 55 + 2·128 = **609**.
**Partial slack total = F − enumerated = 1536 − 609 = 927.**
True slack (complete walk) = 671. 927 ≥ 671 ✓ — an upper bound, never an
under-count, exactly as §5.2 states.

I proved the bound generally rather than by example: partial = F − |union of
enumerated claimant ranges|, and enumerated ⊆ all, so |union enumerated| ≤ |union
all|, so partial ≥ true. This holds even when the walk stopped *because* of an
overlap, provided "the bytes claimed" is read as a set union and not as a sum of
lengths — which the phrase "F less the bytes claimed by the claimants the walk
did enumerate" supports. It also survives §5.2's discard rule (a rejected layer's
already-enumerated claimants are discarded), since discarding only shrinks the
enumerated set.

The report accompanying that verdict: **nonconforming** (a violation was
established, which takes priority); the slack total reported **as partial**,
naming tile 2's T1 as what stopped the walk; every scope not examined reported as
*unexamined*; and, had any requirement been unable to be checked, that too, with
its ground.

**The three causes of incompleteness** are the same in §5.2 and §9.7 — a
scope-level rejection ending that scope's enumeration; a layer declined on
resource grounds; election to stop at the first violation — and the same two
cases leave the walk complete: a *tile's or a document's* decline (the claimant
having been enumerated from its index entry or extent slot), and an entry
structurally classified reject-tile (which contributes no claimant at all).

I checked whether a fourth cause escapes: a verifier that declines the *whole
file* on resource grounds after establishing the trailer is not in §5.2's
three-case list. It is nonetheless caught, because the operative sentence
immediately before that list is general — "Where the walk of §9.7 does not
enumerate every region's claimants, the verifier MUST report the total as
partial." The enumeration that follows is illustration. Not a finding; the
sentence before the sentence decides it.

---

## 4. Extent overlap, alignment, and slab invariants, on adversarial layouts

### 4.1 Overlap — is the F33/L18 split a partition?

I derived the cases myself from `[R-CNT-13]`'s three clauses and checked
completeness and disjointness over an arbitrary overlapping pair (X, Y):

| X, Y | Row | Outcome |
|---|---|---|
| both belong to layer A | L18 | reject-layer |
| X ∈ layer A, Y ∈ layer B, A ≠ B | F33 | reject-file |
| X ∈ layer A, Y ∈ no layer | F33 ("touching another scope's structures") | reject-file |
| neither belongs to a layer | F33 | reject-file |

Complete and disjoint. F33's Condition cell restates it in the same three
branches. The boundary caveat is also right: a claimant reaching the front block
or trailer is caught by a *bounds* row at its own tier rather than by an overlap
row, and F33 names the exact tiers — F9/F10, F30/F31/F32, L15/L16/L17, T8/T9.
I verified the one non-obvious case it calls out: an extent slot of (0, N) with N
nonzero reaches [0,16) through its zero offset, and it is F30's (exactly one half
zero) rather than F31's, because F31 requires extent_offset in 1–15 and 0 is not
in that range. Correct.

### 4.2 Alignment, adversarially

Layer with A = 512, tiles of 100 bytes. Stored at 512, 1024, 1536, 2048 — all
512-aligned, with 412 bytes of slack between each pair. Conforming
(`[R-SLB-05]`: the bytes alignment leaves between structures are slack, which
writers SHOULD zero and no requirement constrains). A verifier reports the slack
and checks the invariant; L40 is the row; readers are not obliged, since offsets
are always explicit.

Move tile 2 to 1500: 1500 mod 512 = 476 ≠ 0 → **L40**, reject-layer, verifier,
certification. Note the alignment invariant is quantified over *stored tiles*
only — the index region itself is unconstrained by A, which I confirmed against
`[R-SLB-01]`'s wording ("every stored tile's offset").

### 4.3 Slab, adversarially — the case with real teeth

Interleaved layer, N = 6, S = 6, A_slab = 512. One run, ordinals [0,6):

```
entry 0  stored at 512, len 100        -> [512, 612)
entry 1  sentinel                      -> transparent to run continuity
entry 2  stored at 612, len 100        -> [612, 712)   closes over entry 1
entry 3  offset = S, length = 100      -> STRUCTURAL reject-tile (T7); transparent
entry 4  stored at 712, len 100        -> [712, 812)   closes over entry 3
entry 5  stored at 812, len 100, crc mismatched
```

Entry 5's *only* defect is that its stored bytes fail its crc. Under §15.3 it is
**well-formed**: "the defect lies in the bytes it addresses, not in the entry, so
its extent stands and it keeps its place in the *verifier* rows, in run
continuity, and in the coverage walk." So the packing relation reads 812 = 712 +
100 ✓ and L41 does **not** fire. Entry 0's offset 512 mod 512 = 0 ✓ so L42 does
not fire either. What does fire: T7 at entry 3 and T1 at entry 5, both reject-tile.
Verdict: nonconforming. Slack total: entry 3's nominal extent contributes nothing;
entry 5's [812,912) is a claimant.

The three-way distinction — sentinel transparent, structurally-rejected
transparent, crc-failed *not* transparent — is consistent across §15.3, §16.2
`[R-SLB-03]`, §9.7 and §5.2. I checked all four statements against each other and
they agree. This is careful work.

### 4.4 Slab under a permitted commit — where immutability bites

This is the case my charter's "multi-generation" half and the surface's "closed
list" half meet, so I worked it concretely.

Layer d = 2, grid (G₀, G₁) = (2, 2), N = 4, S = 2, A_slab = 512. Ordinals: (0,0)→0,
(0,1)→1, (1,0)→2, (1,1)→3. Runs [0,2) and [2,4). Stored at 512, 612 (run 0) and
1024, 1124 (run 1) — packed, each run's first tile 512-aligned.

Now a **permitted** change: grow E₁ so G₁ = 3, N = 6. New ordinals: (0,0)→0,
(0,1)→1, (0,2)→2, (1,0)→3, (1,1)→4, (1,2)→5. Runs become [0,2), [2,4), [4,6).

- Run 0 = (0,0),(0,1) at 512, 612 — unchanged, invariants hold.
- Run 1 = ordinals 2,3 = new tile (0,2) and existing (1,0) at 1024. If (0,2) is
  stored it must precede (1,0) contiguously — but 1024 is a committed byte and
  `[R-LIF-01]` freezes it. So the writer must leave (0,2) sentinel, re-store
  (1,0) at a fresh offset, or clear the declaration.
- Run 2 = ordinals 4,5, whose first stored tile is (1,1) at **1124**.
  1124 mod 512 = **100 ≠ 0**. The run's first stored tile is misaligned.

So a growth of a *non-leading* dimension of a slab-declared layer forces
re-storing or clearing. `[R-SLB-04]` says precisely that: a commit that changes
"the run partition, the byte placement of any run, the disk ordinal of any tile
the new state stores, or the slab declaration itself" MUST "either re-establish
the invariants for every such run — or clear the declaration in the new
generation; carrying a stale declaration forward is a validity error at layer
scope, detected as the invariant failures of `[R-SLB-03]` are: by a verifier."
And §20.3 step 4 routes to it: "a slab declaration is re-established or cleared
(`[R-SLB-04]`)". The verifier's view is L42 on the carried-forward file, which is
exactly what §16.2's Note predicts ("a stale declaration carries no register row
of its own: every file exhibiting one exhibits a run whose tiles are unpacked or
whose first stored tile is misaligned").

Contrast the rank-1 case: with d = 1, s = t₀, so growth never renumbers, run 0
stays intact, and only new runs need placing. I confirmed the asymmetry is real
and correctly handled by the general rule rather than by a special case.

---

## 5. Checksum obligations — every constant I could reproduce

I wrote CRC-32C from the parameters in `[R-ENC-09]` (Castagnoli 0x1EDC6F41,
reflected in and out, init 0xFFFFFFFF, final XOR 0xFFFFFFFF, stored
little-endian) — reflected polynomial 0x82F63B78 — and reproduced every constant
the document states that is locally computable.

| Constant | Document | I computed | Match |
|---|---|---|---|
| CRC-32C(`"123456789"`) (§4.5) | 0xE3069283, stored `83 92 06 E3` | 0xE3069283, `83 92 06 E3` | yes |
| CRC-32C(zero bytes) (§4.5, §7.1, Appendix A) | 0x00000000 | 0x00000000 | yes |
| CRC of a full all-sentinel segment, 2¹⁶ entries = 1,310,720 bytes (§15.4, Appendix B) | 0xEECB3BB2 | 0xEECB3BB2 | yes |
| CRC of 4 sentinel entries, 80 bytes (§7.4 example) | 0x80A34955, stored `55 49 A3 80` | 0x80A34955, `55 49 A3 80` | yes |
| crc_of_crc_array over that 4-byte array (§7.4 example) | 0xC4EE982E, stored `2E 98 EE C4` | 0xC4EE982E, `2E 98 EE C4` | yes |
| Appendix A trailer CRC over trailer [0,60) | 0x402F157E, stored `7E 15 2F 40` | 0x402F157E, `7E 15 2F 40` | yes |

I additionally rebuilt Appendix A's 128-byte minimal file from the field
descriptions alone and compared it against the hex dump **byte for byte**: all
eight rows identical, including file_id 0x0123456789ABCDEF stored
`EF CD AB 89 67 45 23 01`. The annotation table's byte ranges are also all
correct, and the slack arithmetic closes: 128 − (16 front + 4 directory + 64
trailer) = 44, matching §5.1's "44 bytes of slack, zeroed by advice".

I could **not** reproduce: nothing. Every checksum constant in this document is
locally computable and every one of them is right. There are no external-format
digests (deflate/zstd/lz4 outputs) stated as constants anywhere, so no constant
was out of reach.

### Is every live structure covered by a checksum?

Derived from §8.1's map rather than read off it:

- front block — none, by design; equality is the check.
- trailer — self, [60,64) over [0,60). Terminal, covered by nothing further.
- directory region — terminal 4 bytes. Terminal.
- tile-index region — **fully** covered: segment CRCs cover the entry array,
  crc_of_crc_array covers the segment CRC array, and crc_of_crc_array is a field
  of the layer record inside the directory region, under the directory CRC. No
  byte of the region is uncovered.
- stored tiles — entry crc.
- user-metadata extents — terminal 4 bytes.
- **extent of a record of a type this specification has not assigned — none.**

So the answer is *almost*: one live class carries no checksum at all. §4.5 and
§8.1 both except it explicitly, and §22.3 `[R-SEC-04]` names the consequence
("corruption inside it is equally invisible"). It is nonetheless in the
partition, counted by the walk, and covered by the certificate without being
inspected. See finding **verifier-02**.

At entry_count = 0 the region does not exist, the slot is (0,0), and
crc_of_crc_array must be 0 (`[R-CNT-23]`, L27) — nothing to cover, and §15.4's
closing example says exactly this. Checked.

---

## 6. Decoded-content obligations

**What a verifier must decode.** Every stored tile of every layer it certifies
(§9.7), whatever content obligations §14 places on the layer. The reason given is
not the content rules but the codec rows: "§21.4's codec rows are
file-conformance violations, and a verifier MUST NOT certify past a violation it
has not looked for."

**What it compares against, and where the number comes from.** Always the layer's
declarations, never the payload:

- decoded size — `[R-SER-02]`/`[R-SER-03]`: P·Q interleaved, P·Bᶜ for a planar
  numeric channel, ⌈P/8⌉ for a packed planar bool plane. Row T3; under codec 1
  also T14, checkable from the entry alone before any payload fetch.
- padding positions — each channel's recorded fill bytes, `[R-SER-05]`, T4.
- pad bits in a packed plane — the plane's channel's fill bit, T5.
- interleaved bool bytes at real positions — 0x00 or 0x01, `[R-SER-08]`, T2.
- zstd header — magic, exactly one frame, no skippable frame, no nonzero
  Dictionary_ID, no content-checksum flag, window ≤ decoded size, content size =
  decoded size when present. T17–T22.
- exact consumption and well-formedness — T24, T25.

I verified §14.2's, §14.3's and §14.5's worked examples arithmetically:
interleaved (2,3) with uint8+uint16 → Q = 3, decoded size 18, ordinal 5 at bytes
[15,18); same layer planar, channel `b` 12 bytes, ordinal 5 at 10–11;
float32+bool interleaved → Q = 5, size 30, ordinal 5 at [25,30) with the bool at
byte 29. Packed plane P = 10 alternating → `55 01` with fill false and `55 FD`
with fill true (pad bits 2–7 set). Edge tile at (1,1) of extents (5,5) with tile
extents (4,4) → 16 positions, one real, 15 padding, 32 bytes with values 1–15 all
`CD AB` for fill 0xABCD. §17.3's shuffle: 1.0/2.0/3.0 float32 decode as
`00 00 80 3F 00 00 00 40 00 00 40 40`, and placing byte i of group j at i·n + j
with s = 4, n = 3 gives `00 00 00 00 00 00 80 00 40 3F 40 40`. All six match the
document exactly.

**What it is permitted to skip.** Only on resource grounds, and never silently:

- a tile's decode → the check is reported unmade, the file cannot be certified,
  the walk stays **complete** (the claimant was enumerated from its index entry);
- a layer → its claimants are never enumerated, so the walk is **incomplete** and
  the slack total is partial;
- a user-metadata document, on its decoded-size bound or the frame's declared
  `Window_Size` → `[R-MTA-09]`: cannot establish, MUST NOT certify, MUST NOT
  report as nonconforming, SHOULD report the bound applied and the stored extent
  length. The walk stays complete.

**What carries no content obligation at all.** A user-metadata document under an
experimental-range encoding. `[R-MTA-10]` is careful here and I checked its
reasoning end to end: §10.3 lets two unrelated experiments claim one value with
different meanings, so "the decoded document" names nothing this specification
can test; file conformance is decided by the framing, the extent slot, the
encoding byte's own value set and the terminal CRC alone; the verifier has *no*
requirement it is unable to check, so this is **not** a cannot-establish ground
and certification is unaffected. Encoding 0 and reserved 3–0x7F remain violations
(R1) — what is withdrawn is the document's content rules, never the encoding
byte's value set. I could not fault this.

**A boundary I checked in §18.2.** The finiteness rule now names the rounding
attribute: "the IEEE 754 binary64 value its decimal text converts to under IEEE
754's default rounding-direction attribute, roundTiesToEven". roundTiesToEven is
indeed IEEE 754-2019's default for binary formats, and Appendix F pins it. That
fixes the overflow boundary exactly: a decimal text rounds to +∞ iff its value is
at least the midpoint above the largest finite binary64, so `1e400` is unreadable
and a text one ulp-midpoint below the boundary is readable, with no room for two
implementations to disagree. Underflow to zero or subnormal stays finite and
readable. R8's four instances (overflow / bare token, × two containers) are the
complete alternative set. This repair does what it was meant to do.

---

## 7. The multi-generation trace — certification result at each step

| Generation | Operation | F | Claimed | Slack | Verdict |
|---|---|---|---|---|---|
| 1 | creation, 4 tiles stored | 832 | 785 | **47** | conforming |
| 2 | append: supersede tile 1 | 1280 | 785 | **495** | conforming |
| 3 | append: add file-scope user metadata | 1536 | 865 | **671** | conforming |
| 4 | compaction, fresh file_id | 896 | 865 | **31** | conforming |
| 3′ | generation 3 with one byte of tile 2 corrupted | 1536 | 609 enumerated | **927 partial** | **nonconforming** (T1), walk incomplete |

Each generation's F is a multiple of 64; each append raises F by at least 128
(448, 256); the file_id is constant across 1–3 and freshly drawn for 4.

Things the trace made me check that I would otherwise have taken on trust:

- **Generation 2's index re-emission.** Superseding one tile re-emits the whole
  84-byte region at a new placement — one entry re-pointed, three byte-identical
  at their disk-ordinal positions. §20.3's own worked example gives 32·20 + 4 =
  644 for a 32-tile layer; my 4-tile case gives 4·20 + 4 = 84 by the same
  formula. Both reproduce.
- **The layer record's extent slot follows the region.** A layer whose record
  alone changes keeps its slot; relocating a live index region is compaction's
  operation, not an appender's (`[R-WRT-04]`, `[R-WRT-07]`). Generation 3 changes
  no layer, so the layer record is re-emitted byte-identically, extent slot and
  all, pointing at generation 2's region — which is why generation 3's claimed
  total rises only by the metadata extent.
- **Compaction regenerates rather than copies** exactly when a region's stored
  extents move. Mine moved, so crc_of_crc_array changed. §20.5's figure shows the
  other case (A's extents happen not to move, so A's index is copied and only its
  slot re-pointed). Both are placement-dependent, and the document says so
  ("placement being the compactor's to choose").

---

## 8. The closed list with an exception, taken in pairs

This is the surface's centre, and it intersects my charter wherever a verifier
must decide whether a generation's layer record is consistent with the one it
supersedes. I derived the members myself from §20.3 step 4 rather than reading
them off:

**Permitted, for a layer that stores a tile in the generation the commit
supersedes** — M1 layer name; M2 dimension names; M3 channel names; M4 an extent
grows (never shrinks); M5 a planar channel list extended at its end; M6 a planar
channel list shortened from its end; M7 a slab or alignment declaration declared,
re-established or cleared. Excepted pair: **(M5, M6)** on one channel list.

**Fixed** — layout, linearization, index encoding, codec, filter, rank, dimension
order, every tile extent, every channel's type and fill, an interleaved layer's
channel list but for names, and the position of every planar channel but the last.

I took the pairs. Reported here are the ones that are not trivially independent.

**(M5, M6) — excepted, and I confirmed why it needs to be.** Combining them
replaces the last channel. The fixed side leaves the *position* of the last
planar channel unfixed but fixes "every channel's type and fill" — so a
replacement with a different type would break a fixed declaration by composing
two permitted moves. The exception closes exactly that, and its consequence
clause ("replacing the last channel, or any run of channels at the end, is two
commits or a rewrite") is the right consequence.

**(M4, M6) — growth plus shortening.** This one worried me most, because it is
shape 6 exactly: **a derived quantity holds still while the thing that decides
the outcome moves.** Planar layer, d = 1, T = 8, E = 32 → G = 4, N = 4, C = 2,
addressed = 8. Commit grows E to 64 (N = 8) and shortens to C = 1. New addressed
= 1·8 = **8** — entry_count unchanged, extent_length unchanged at 8·20 + 4 = 164,
and if the right entries were sentinels the region's bytes would be identical
too. Yet ordinals 4–7 have gone from channel 1's spatial 0–3 to channel 0's
spatial 4–7.

The document already closes this, in the sentence that names the very case: "A
channel removed from the end ... changes the layer's index content, the entries
the removed channel held ceasing to denote its tiles, so the region is re-emitted
under the clause above **whether or not entry_count changes with it**
(`[R-CNT-17]`) and whether or not a retained ordinal moves." So re-emission is
triggered semantically, not by entry_count.

I then proved the stronger thing the repair rests on: **a stored tile can never
be misplaced by a composition of permitted changes without the region's bytes
changing.** A retained planar channel c's tile at spatial s moves from c·N_old + s
to c·N_new + s, which differ unless c = 0; so any move shows up in the bytes; so
the re-emission trigger fires under either reading of "index content". And the
step's own claim, "a growth renumbers ordinals wherever `[R-GEO-06]` moves them,
and nothing else this step permits moves one", is true: ordinals depend on the
grid counts and the channel index, M1–M3 touch neither, M5/M6 change only C at
the *end* so retained indices hold, and M7 governs placement, not ordinals.

**(M4, M5) — growth plus extension.** The justification sentence for M5 is "an
appended planar channel adds tiles at ordinals after every existing one, a disk
ordinal being c · N + s with N the spatial-tile count". Taken with a growth, N
changes — so I checked the claim in the *new* numbering: the highest retained
ordinal is (C_old − 1)·N_new + (N_new − 1) = C_old·N_new − 1, and the appended
channel's lowest is C_old·N_new. Still after every existing one. The sentence
survives the pair.

**(M4, M7) and (M6, M7) — worked in §4.4 above.** `[R-SLB-04]`'s trigger list
reaches them, including the case where re-establishing is impossible without
re-storing tiles.

**M7 with itself — may a commit *change* S or A_slab, as opposed to declaring,
re-establishing or clearing?** I opened this as a candidate: §20.3's three verbs
do not obviously cover "change from 4096 to 512", and the resulting file would be
conforming either way, so the fork would be over which files an *updater* may
emit as a later generation — a real emittable-set question. It is closed by
`[R-SLB-04]`'s trigger, which names "**the slab declaration itself**" among the
changes a commit may make and requires only that the invariants be re-established
or the declaration cleared. §20.3's "as this step provides below" points at
exactly that clause, and the alignment half is closed the same way ("an aligned
layer's stored tiles — every one the new state keeps ... satisfy its invariant or
the declaration is cleared"). Candidate closed, and I record it because it took
three sections to close.

**(M3, M6) — renaming into a removed channel's name.** Planar [a, b, c]; shorten
to [a, b] and rename b to `c`. Both permitted, uniqueness holds in the result,
and no structural map is disturbed: "a name enters no map this specification
defines". Benign.

I could not construct a pair that composes into a forbidden operation, or a
justification sentence that a pair falsifies. My conclusion on the surface's
centre is that the round-32 repair holds under pairwise composition.

---

## 9. Mechanical checks of the register

Because a verifier's obligations are enumerated by §21 and by nothing else, I
audited the register's own arithmetic.

**Rows.** §21.2 claims 35, I count 35 (F1–F36 with F11 struck — and §21.2's Note
explains the gap, on §2.2's model). §21.3 claims 49, I count 49. §21.4 claims 26,
I count 26. §21.5 claims 10, I count 10. Total 120, matching §21.8's "120
conditions".

**Instances.** Counting semicolon-separated entries, with a `—` cell counting as
1 per §21.1's own rule: 56 + 116 + 55 + 50 = **277**, matching §21.8's "277
instances" exactly.

**Instance cells against §21.1's counting rules.** I extracted every row whose
condition text uses a two-magnitude comparison and checked that both directions
are enumerated, and every row using a one-directional comparison and checked that
they are not.

- Two directions where required, per layout where the quantity varies by layout:
  T3 (6 = 2 × 3), T14 (6), T22 (6), L21 (4 = 2 × 2), L22 (2 directions + 2 stated
  alternatives), L30 (2), F17 (2), R4 (content-size gets 2 directions × 2
  containers within its 16).
- One direction where the text bounds the comparison: T21 (3 layouts), L44 (3),
  F3, F10, F32, T12, L2 (9 derived quantities), T11, F5, R10.
- No direction where there is no magnitude ordering: F14, L37, L38 (checksum
  against computed), T5, T6 (bit or value against a constant) — each 1 instance,
  exactly as §21.1's "a stored checksum against a computed one ... is equal or it
  is not, and *greater* names nothing" requires.
- No direction for a nonzero value test: L20 (`A ≠ 0` with `S ≠ 0`) — 1 instance,
  and it is also a single predicate over two fields, so rule 7 gives 1 either way.
- L29 (A_slab) enumerates 3 and L39 (A) enumerates 3, correctly asymmetric: A = 0
  is a legal "none declared" so it is not one of A's failure modes, while
  A_slab = 0 with S ≠ 0 is a failure mode.

No cell is inconsistent with the rules §21.1 states. I also derived L2's nine
declaration-derived quantities independently from `[R-ENC-04]`, `[R-GEO-03]`,
`[R-CNT-13]`, `[R-CNT-17]`, `[R-SER-02]` and `[R-SER-07]` and got the same nine,
including the two dominance claims — planar C·N dominates the max disk ordinal
(C−1)·N + (N−1) = C·N − 1, and interleaved P·Q dominates V = P·C since every
Bᵢ ≥ 1 implies Q ≥ C. Both hold.

**`[R-CNT-06]` states nine conditions.** §2.3 asserts this. I derived it: the
rows whose *governing* rule is `[R-CNT-06]` are F8, F9, F10, F12, F13, F14, F15,
F16, F17 — nine, of which two (F8 trailer magic, F14 trailer CRC) assert
invariants `[R-CNT-24]` fixes and seven do not. Matches "the trailer magic and
the trailer CRC ... and the other seven do not" exactly.

**Which rows reach a foreign format major.** §21.2 asserts F8, F14, F6 and both
of F1's instances, and no other. I derived it from `[R-CNT-24]`'s fixed set —
magic at F − 64, versions at F − 56, CRC at F − 4 over [F − 64, F − 4), and the
front block constant — and got the same five, with the arithmetic that a future
major may redefine 64 − (8 + 4 + 4) = **48** bytes, namely [12, 60), which is why
F15 (reserved [48,60)) does *not* reach although its cell cites `[R-CNT-24]`, and
why F13 (64-alignment) and F17 (length cross-check) do not either, `[R-CNT-24]`
fixing neither. §2.3's Note gives the F14/F5/F15 cases and I agree with all
three.

**Specialization pairs.** §21.1 names F1-front/F6, F1-magic/F8, F35/F36, L24/L25,
F21/F22, L10/L11. I checked each: F21 (slot (0,0)) forces extent_length 0 < 5, so
every F21 file exhibits F22 ✓; likewise L10/L11; F35 (reserved type with MU = 1)
implies F36 (reserved type whatever the MU bit) ✓; likewise L24/L25; the front
block magic reversed is `1A 0A 0D 4E 52 41 54 89` ≠ the constant, so F1's
front-block instance implies F6 ✓. All six hold, in the stated direction.

**Other worked numbers I reproduced.** §15.4's 1,000,000-entry example: 16
segments (15 full + 16,960), 64-byte CRC array, region 20,000,064 bytes, entry
999,999 in segment 15 at segment-relative byte 339,180, CRC array at
[20,000,000, 20,000,064), segment 15 at [19,660,800, 20,000,000) = 339,200 bytes,
full segment 1,310,720 = 1.25 MiB. §15.4's planar example: disk ordinal 2·32 + 10
= 74, region bytes [1,480, 1,500), channel 3's entries 96–127. §11.4's example:
tile (1,2) → s = 10, in-tile (44,188) → ordinal 11,452, planar channel 2 → 74.
§21.9's note: 2³² tiles → 2¹⁶ segments × 4 = 256 KiB, and 2³⁶ → 4 MiB; 65,536
layers at 200 bytes → 13,107,200 = 12.5 MiB. §20.3's note: 10⁶ tiles → 20,000,064
≈ 20 MB. §14.4's note at P = 1: interleaved 1 byte, planar ⌈1/8⌉ = 1 byte, and
they coincide exactly when the fill bit is false. Every one matches.

---

## 10. Findings

Three findings, none byte-level. Each is stated with the quotation it complains
about and the section it lives in.

---

### verifier-01 — OBSERVATION

**Two statements of the slack rule drop a qualifier the third states, and the
unqualified form over-counts a MUST-report quantity**

**Location:** §5.2 `[R-CNT-21]`; §9.7 `[R-LIF-08]`; against §15.3 `[R-IDX-03]`.

**Quotation (§5.2):**

> An entry `[R-IDX-03]` classifies reject-tile on a structural ground leaves it
> complete too, and for the opposite reason: it contributes no claimant, the walk
> passes over it, and its bytes fall to slack (§9.7).

**Quotation (§9.7):**

> An entry `[R-IDX-03]` classifies reject-tile on a *structural* ground does not
> make the walk incomplete: the walk passes over it, and the bytes it nominally
> addresses fall to slack (§15.3).

**Quotation (§15.3), which carries the qualifier:**

> and none to `[R-LIF-08]`'s coverage walk, so any bytes it nominally addressed
> that no other claimant claims fall to slack.

**Detail.** "Its bytes" and "the bytes it nominally addresses" have no referent
that survives a structurally-rejected entry. Six of §15.3's rows classify an
entry whose 20 bytes "yield no usable extent", and several of them yield a
*nominal* range that is either enormous or already claimed:

- offset = 10, length = 100 (T8, offset < 16): nominal range [10, 110). Bytes
  [10, 16) belong to the front signature block, a claimant. Bytes [16, 110) may
  belong to another stored tile.
- offset = 200, length = 2⁶⁴ − 1 (T7, exactly one half sentinel): nominal range
  [200, 2⁶⁴ + 199), which exceeds F.
- offset = length = 2⁶⁴ − 1 with crc ≠ 0 (T6): nominal range starts beyond any
  file.

A verifier that follows §5.2's or §9.7's sentence literally adds those nominal
ranges to the slack total. `[R-CNT-21]` makes that total a **MUST report**, and
§22.3 makes it the number "that distinguishes a working file from a padded one",
so two conforming verifiers can report materially different figures for one file
— in the second example above, a figure larger than F.

§15.3's qualifier is the correct statement, and the citation chain resolves to
it: §5.2 cites §9.7, §9.7 cites §15.3, §15.3 carries the qualifier. The operative
definitions also resolve it — §5.2's "Every byte the live state does not claim is
slack" and §9.7's "Bytes the walk does not reach are slack" are both
set-complements, under which a byte claimed by the front block is not slack
however some other entry nominally addresses it. So the question is decidable;
what it costs is that an implementer must follow two citations and prefer a
definition over a consequence clause, and the consequence clause is the one
stated twice.

**Byte-level: no.** The slack total is a report line, not a verdict. The files in
which the divergence arises exhibit T6/T7/T8 and are nonconforming under every
reading, so neither the emittable set nor any accept/reject verdict moves.

**What an implementer does wrong without it:** reports an inflated — occasionally
impossible — slack total on files carrying a structurally malformed index entry,
and an operator reading that total over-estimates what compaction would reclaim.

---

### verifier-02 — OBSERVATION

**The "counted and named, never silent" duty is stated for the checksummed
uninspected extent and not for the unchecksummed one**

**Location:** §18.2 `[R-MTA-10]`; §8.1 `[R-CNT-19]`; §22.3 `[R-SEC-04]`; §2.3
`[R-CNF-11]`; Appendix H.

**Quotation (§18.2, `[R-MTA-10]`):**

> and it MUST report each record it ignored on this ground, naming the owning
> scope, the encoding value, and the stored extent length, as it reports the
> slack total (`[R-CNT-21]`): bytes a certificate covers without inspecting are
> counted and named, never silent.

**Quotation (§8.1's map row):**

> | Extent of a record of a type this specification has not assigned | none — the
> bytes are opaque (§7.2) | — |

**Quotation (§22.3, `[R-SEC-04]`):**

> The extent of a record of a type this specification has not assigned is covered
> by no checksum either (§8.1), so corruption inside it is equally invisible:
> §20.4's byte-identical re-emission (`[R-WRT-05]`) carries such an extent forward
> unread, and `[R-WRT-08]` bars re-encoding it, so nothing an updater does would
> surface the damage.

**Detail.** Two live classes are covered by a verifier's certificate without
their content being inspected:

1. the extent of a user-metadata record under an experimental-range encoding —
   whose bytes **are** covered by the extent's terminal CRC-32C (§8.1), so
   corruption in them is detected, and only the *content rules* are withdrawn;
2. the extent of a record of a type this specification has not assigned — which
   §8.1 covers by **no checksum at all**, so corruption in it is not detected
   either. A conforming file can carry one: §21.6 records an experimental-range
   type with MU = 0 as a defined non-violation, ignored by readers.

`[R-MTA-10]` imposes a naming duty on case (1) and justifies it with a principle
stated in general terms — "bytes a certificate covers without inspecting are
counted and named, never silent." Case (2) satisfies that principle more
strongly, and draws no naming duty anywhere. I searched the whole document for
one: the phrase "counted and named" occurs once, "report each record" occurs
once, both in `[R-MTA-10]`. §2.3's report obligations run to requirements the
verifier was *unable to check* and scopes it did not *examine*; a type this
specification has not assigned imposes no requirement to be unable to check, and
its extent is enumerated by the walk, so neither annotation reaches it. Appendix
H's verifier checklist names the `[R-MTA-10]` report and no counterpart.

So a verifier may certify a file whose bytes include an arbitrarily large,
entirely unchecksummed, entirely uninspected extent, and say nothing about it —
while the same verifier must name a *smaller* uncertainty three lines away.
§22.3's own remedy for case (1), "an operator who wants no such bytes rejects on
that report line, a policy above conformance", has no analogue for case (2), even
though §22.3 states case (2) first and calls it "equally invisible".

**Byte-level: no.** This is a report obligation. No file's conformance changes and
no verdict changes; a verifier that reports such records and one that does not
certify and reject exactly the same files.

**What an implementer does wrong without it:** ships a certificate whose silence
an operator reads as coverage, over precisely the bytes §22.3 identifies as the
format's least-defended residue.

---

### verifier-03 — OBSERVATION

**`[R-CNF-13]` offers `[R-CNT-04]`'s residency exemption as an example of an
exemption that "applies unchanged", for an actor §2.3 grants it to no one**

**Location:** §2.3 `[R-CNF-13]`, against §2.3 `[R-CNF-11]`, §21.2 row F6, and
Appendix H.

**Quotation (§2.3, `[R-CNF-13]`):**

> A reader MUST apply every reaching condition to a file whatever major it
> declares — an exemption the condition's governing requirement grants on a ground
> other than the declared major applies unchanged, `[R-CNT-04]`'s residency
> exemption among them — and MUST treat its failure as reject-file on the ground
> of the requirement stating it rather than on capability grounds

**Quotation (§21.2, row F6):**

> the obligation binds a reader holding those bytes resident, and a reader that
> would have to fetch them MAY defer or omit the check (`[R-CNT-04]`); a verifier
> holds no such exemption (§2.3)

**Detail.** A verifier is a reader — §2.3: "Verifiers and updaters are readers of
the files they process and inherit every reader obligation." So `[R-CNF-13]`'s
sentence addresses it. The conditions that reach a file declaring a format major
other than 1 are exactly F8, F14, F6 and F1's two instances (§21.2), and **two of
those five are the front-block conditions the residency exemption governs.** So
the example clause lands squarely on the verifier's path.

Read as written, a remote verifier faced with a file declaring format major 7,
whose open leaves [0, 16) non-resident, may omit the front-block check and report
*cannot establish*. Read against §2.3's class definition — "checks every
file-level requirement — **including those ordinary readers are exempted from**"
— it must fetch [0, 16), and if the block is wrong it establishes F6 or F1 and
reports **nonconforming**, which `[R-CNF-13]` itself then confirms ("A verifier
that establishes such a failure reports *nonconforming*, whatever major the file
declares"). Those are different verdicts on the same bytes.

The second reading is the right one and I adopted it: §2.3's class definition,
F6's Condition cell, and Appendix H's "which `[R-CNT-04]` lets a reader not
holding it resident defer or omit and §2.3 does not (F1, F6)" all say so, three
times. `[R-CNF-13]`'s clause is preserving exemptions against the reach doctrine,
not granting them, and the example is simply inapt for the one actor the reach
paragraph's next sentence addresses by name.

**Byte-level: no.** The verdict fork is only available on a misreading that three
other passages foreclose, and the file at issue is one this document "declines to
judge" in any case (§21.6): the file may be perfectly conforming under its own
major, so no accept/reject verdict about *conforming bytes* moves.

**What an implementer does wrong without it:** builds a remote verifier that skips
the front-block equality check whenever the block is not already resident, and
reports *cannot establish* where *nonconforming* was owed — for the one class of
file where the front-block check is among the only checks it can make.

---

## 11. Where I found little, and what I did that would have found something

**The certification procedure.** I reconstructed the verdict lattice from
`[R-CNF-11]`, `[R-CNF-12]`, `[R-COD-11]`, `[R-MTA-09]` and `[R-MTA-10]`, checked
that each verdict has a stated availability condition and that the three are
mutually exclusive and jointly exhaustive over (violation established?) ×
(requirement unable to be checked?), and probed for a state with no verdict —
there is none. I probed the boundary between *unexamined*, *unable to check*, and
the partial slack total for double-classification: a resource-declined layer is
reachable through two report channels but neither affects the verdict, so no
fork.

**The coverage walk.** I derived the claimant set independently and closed the
sum exactly on four generations plus one incomplete walk. I proved the
upper-bound property of the partial total rather than sampling it. I searched
specifically for a byte that could be in no class and satisfied myself the
question is definitional, as §5.2's Note says. The one thing I found here is
verifier-01, and it turned up because I ran the walk over a file carrying a
structurally-rejected entry rather than reasoning about the sentence in the
abstract.

**Slab and alignment.** I built four adversarial layouts — sentinels and
structurally-rejected entries inside a run, a crc-failed entry inside a run, a
mid-file misalignment, and a grid growth on a non-leading dimension that forces
re-storing or clearing. The last is the sharpest case in this area and the
document handles it correctly through `[R-SLB-04]`'s "the slab declaration
itself" trigger. Nothing broke.

**Checksums.** Every constant reproduced, including the 1.25 MiB all-sentinel
segment CRC and Appendix A's whole 128-byte file byte for byte. There was
nothing here to find; I say so having computed all six.

**Decoded content.** Six worked examples reproduced arithmetically. I checked the
one place where the verifier's decode duty is broader than §2.3's stated
cannot-establish ground (a layer with no §14 content obligation) and found it
saved by "as when". I checked whether an interleaved bool byte at a *padding*
position falls between T2 and T4 and found T2 routes it to T4 explicitly.

**The closed list.** I derived the seven permitted members and took every
non-trivial pair, including the one that makes entry_count hold still while both
C and N move — the shape the brief names — and proved the general claim the
re-emission trigger needs (no permitted composition moves a stored tile without
changing the region's bytes). I opened the "may a commit change S or A_slab"
question as a genuine emittable-set candidate and closed it on `[R-SLB-04]`. I
found no pair the text leaves open.

**The register.** Rows, instances, direction enumeration, specialization pairs,
`[R-CNT-06]`'s nine, the reach derivation, and L2's nine derived quantities all
checked mechanically or by re-derivation. 120 rows and 277 instances match the
stated figures exactly. The register is in better shape than any other part of
the document I touched, and I say that having counted rather than assumed.

My confidence that a conforming verifier can be built from this document alone is
**high**. The three findings above are report-quality defects; none of them would
stop an implementer, and none of them moves a byte.
