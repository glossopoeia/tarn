# Cleanroom round 29 — Reader implementer transcript

## 0. Access and disclosure

I read exactly one file: `/Users/robertkleffner/Documents/GitHub/tarn-first-draft/spec/tarn.md`
(4,697 lines, 46,880 words by `wc`). I opened no other file in the repository — no
`docs/`, no `conformance/`, no `spec/registry.json`, no `PLAN.md`, no `OPEN-QUESTIONS.md`,
no git history. I ran no web search or fetch. I did not list or read the output directory.

The file was where the brief said it would be.

**Context I did not ask for.** My runtime placed material in my context before I began:
a project instruction file pointing at an `AGENTS.md`, and an index of the maintainer's
private memory notes with several titled entries, one of which names §21 and the vector
corpus. I did not open any of those files, and I have not used any of that material as
evidence about the specification. I note one path detail because the brief asks me to:
the injected instruction file is rooted at a directory named `tarn`, while the spec I was
told to read lives under `tarn-first-draft`. I did not go looking at the other directory.

**Files I wrote** (all in my own scratch directory
`/private/tmp/claude-501/-Users-robertkleffner-Documents-GitHub-tarn-first-draft/r29-round/scratch/reader/`):
`rdr_crc.py` (CRC-32C implementation and constant checks), `rdr_appA.py` (Appendix A
verification), `rdr_reg.py` (register row/instance census), `rdr_build.py` (constructs a
complete one-layer TARN file), `rdr_read.py` (my paper reader, executed against it),
`worked.tarn` (the constructed file). Plus this transcript, at the single path the brief names.

---

## 1. The open path, walked

### 1.1 Cold remote open — byte-exact

I implemented §19.1 as written and ran it. From a cold start against a ranged server:

| # | Range | Bytes | What bounds it before I have read it |
|---|---|---|---|
| 1 | suffix `bytes=-64` | 64 | The constant 64 — §6.2 fixes the trailer size, and `[R-CNT-24]` fixes it in **every** format major ("MUST NOT grow the trailer"), so this range needs nothing from the file. The response's `Content-Range` total supplies the transport-authoritative F (`[R-CNT-10]`), which is why §19.1's steps 1 and 2 cost one request between them. |
| 2 | `[dir_offset, dir_offset + dir_length)` | dir_length | `dir_offset ≥ 16`, `dir_length ≥ 4`, `dir_offset + dir_length ≤ F − 64` — all validated in §6.2's stated order *after* the trailer CRC verifies, so `[R-ENC-05]`'s "no I/O on an unverified integer" is satisfied. |

Total: **2 requests, 64 + dir_length bytes.** No third request is ever needed for the
open: §19.1 says the open "consumes the trailer and directory only — no extent slot's
content, no tile index, no payload".

For Appendix A that is 2 requests / 68 bytes. For the file I built below it is
2 requests / 173 bytes. Both match §6.4.

The front signature block is **not** part of that accounting. `[R-CNT-04]` keys the
obligation to *residency*, not transport: my two-exact-range reader never holds
[0, 16), so it may defer or omit the check. My local reader holds the whole file and
must check it by equality first. This is stated three times consistently (§6.1, §19.1
step 1, F6's Condition cell) and Appendix H confirms a verifier holds no exemption. I
found no gap here.

### 1.2 Validation order, as I coded it

§6.2 fixes the order and I followed it literally:
magic → trailer CRC → version gate → {flag gates, committed_file_length vs transport
size, CFL mod 64, dir_offset ≥ 16, dir_length ≥ 4, dir_offset+dir_length ≤ F−64,
file_id ≠ 0, reserved zero}.

I derived `[R-CNT-06]`'s condition count myself, because §2.3 asserts it: stripping the
version gate (`[R-CNT-07]`'s) and the flag gates (`[R-CNT-08]`'s) leaves exactly **nine**
conditions, and the register carries exactly nine rows citing `[R-CNT-06]` as governing
rule: F8, F9, F10, F12, F13, F14, F15, F16, F17. §2.3 says nine. Confirmed.

Of those nine, the two that assert an invariant `[R-CNT-24]` fixes in every major are the
magic (F8) and the trailer CRC (F14) — the other seven read fields a future major may
redefine or derive a floor from format-major-1 structure. §2.3 says "the other seven do
not". Confirmed. §21.2's reaching set (F8, F14, F6, both F1 instances) follows and I
could re-derive it without help.

---

## 2. Validation timing by tier

I built the tier table from the register mechanically (`rdr_reg.py`) rather than from
prose, then checked it against §19.2.

- **at open** — every reader-detected F row except none; plus L3, L5, L6 (the layer
  *record's name*, which §19.1 step 4 parses at open to build the namespace); plus R1's
  top-level instance.
- **at layer access** — L1, L2, L4, L7–L36, L39, L43, L44, L45 (the whole §7.4/§11/§12/
  §14/§15/§17 declaration set); plus R1's sub-record instance.
- **at tile use** — L37, L38 (index chain — layer *outcome*, tile-use *detection point*,
  which §19.2 calls out explicitly) and every reader-detected T row.
- **at extent use** — R2 … R10.
- **certification** — every verifier-detected row, and only those.

Every reader row's Detected cell is one of §19.2's four tiers; every verifier row's is
"certification". §21.1 claims exactly this and it holds row for row.

What a reader is permitted never to check: everything whose Detector cell reads
*verifier* — F7, F25, F26, F27, F28, F33, F36; L18, L25, L40, L41, L42, L46, L47, L48,
L49; T2, T4, T5, T26. `[R-RDR-02]` makes that explicit ("a violation whose assigned
detector is the verifier imposes no reader obligation") and `[R-CNF-12]` still licenses a
reader that notices one to reject. That is coherent; I had no decision to guess at.

---

## 3. Layer access and the tile-read algorithm — executed

I did not want to walk this on paper only, so I built a complete conforming file from
the document alone and ran a reader over it.

### 3.1 The file I built (`worked.tarn`, 256 bytes)

Rank-1 interleaved layer `sst`; dimension `x` with E = 4, T = 2; one float32 channel
`temp` with fill `0x7FC00000`; codec 1, filter 1; no alignment, no slab. Tile 0 stored
(values 1.0, 2.0), tile 1 sentinel.

Derived from §11.2/§14.2: G = ⌈4/2⌉ = 2, N = 2, P = 2, Q = 4, decoded size P·Q = 8,
addressed-tile count = N = 2 (interleaved), so entry_count = 2 and, by `[R-CNT-17]`,
extent_length = 2 × 20 + ⌈2/2¹⁶⌉ × 4 = **44**.

```
[   0,  16)   16  front signature block
[  16,  24)    8  tile 0 stored extent (codec 1: length == decoded size, [R-COD-04])
[  24,  68)   44  tile-index region: 2 entries + one 4-byte segment CRC
[  68, 177)  109  directory: one 24-byte layer-record header + 81-byte inline + 4-byte CRC
[ 177, 192)   15  pre-trailer pad — slack
[ 192, 256)   64  trailer
```

The inline payload came out at **81 bytes**, the same figure §7.4's worked example
gives for its own rank-1/1-channel layer, and for the same reason: name (4) + nine
scalars (34) + one dimension entry (18) + one channel entry (12) + trailing fixed
fields (13). I recomputed each of those four sub-totals independently against §7.4's
field table before trusting the example.

Claimed bytes: 16 + 8 + 44 + 109 + 64 = 241. F = 256. **Slack = 15**, exactly the
pre-trailer pad. §9.7's walk reproduces it.

### 3.2 The read

`rdr_read.py` implements §19.1 → §19.3 → §19.4 with no reference to anything but the
spec text, and asserts a register row label at each check. Output:

```
[19.1.1] transport size F=256; front block resident -> verify by equality
[19.1.2] trailer fetched [F-64,F) = 64 bytes  (remote request #1: suffix -64)
[19.1.2] trailer OK: dir=(68,109) F=256 file_id=0x0123456789ABCDEF
[19.1.3] directory 109 bytes fetched+CRC-verified (request #2). cold open = 173 bytes / 2 requests
[19.1.4] 1 record(s); types=['0x1']
[19.3] layer 'sst' layout=1 lin=1 codec=1 filter=1 rank=1 C=1 dims=[('x',4,2)]
       chans=[('temp',12,'0000c07f')] idx_enc=1 entry_count=2
[19.3] G=[2] N=2 P=2 Q=4 addressed=2 decoded_size=8 index extent=(24,44)
[19.4.1-2] x=3 -> tile 1, in-tile 1, spatial ordinal s=1, disk ordinal 1
[19.4.3] crc_of_crc_array OK; segment 0 CRC OK over entries [0,2)
[19.4.4] entry 1 is the SENTINEL -> 'temp' reads fill 0000c07f at x=3 (no payload I/O)
[19.4.8] RETURN x=3: 0000c07f
[reference array] [('stored',1.0), ('stored',2.0), ('fill',nan), ('fill',nan)]
```

Everything §19.4 needs is in the document. The one thing I had to pin myself was the
*returned representation* of a boolean sample (a bit in a planar plane, a byte
interleaved); §12.1's "logical value: false or true" plus `[R-SER-08]`'s "MUST report
0x00 as false and every other byte as true" settle it — the returned value is the
logical value, and `[R-MDL-02]`'s "bit-for-bit" is aimed at the numeric types it
parenthesises. I do not report that as a defect.

### 3.3 Arithmetic I re-derived rather than trusted

Every one of these I computed before comparing with the document's stated figure.

| Quantity | I computed | Document says | § |
|---|---|---|---|
| CRC-32C("123456789") | `0xE3069283` | `0xE3069283` | §4.5 |
| CRC-32C(zero bytes) | `0x00000000` | `0x00000000` | §4.5 |
| CRC of 80 bytes = 4 sentinel entries | `0x80A34955` (`55 49 A3 80`) | `0x80A34955`, `55 49 A3 80` | §7.4 example |
| crc_of_crc_array over that 4-byte array | `0xC4EE982E` (`2E 98 EE C4`) | `0xC4EE982E`, `2E 98 EE C4` | §7.4 example |
| CRC of 2¹⁶ sentinel entries (1,310,720 B) | `0xEECB3BB2` | `0xEECB3BB2` | §15.4, App. B |
| Appendix A trailer CRC over [0,60) | `0x402F157E` | `7E 15 2F 40` = `0x402F157E` | App. A |
| Appendix A: file length / dir / pad / slack | 128 / (16,4) / 44 B / 44 B | 128 / (16,4) / 44 B | App. A, §5.1 |
| §7.4 example inline payload | 4+34+18+12+13 = 81 | 81 | §7.4 |
| §7.4 example index extent_length | 4×20 + ⌈4/2¹⁶⌉×4 = 84 | 84 | §7.4 |
| §11.4 example: (300,700) T=256 G=(4,8) | s=10, u=(44,188), ordinal 11,452, planar disk 74 | same | §11.4 |
| §15.4 example: entry_count 1,000,000 | 16 segments (15 full + 16,960); array 64 B; region 20,000,064; tile 999,999 at seg-rel 339,180; ranges [19,660,800, 20,000,000) and [20,000,000, 20,000,064) | same | §15.4 |
| §15.4 example: planar C=4 N=32 chan 2 s=10 | disk 74, entry bytes [1480,1500); chan 3 = entries 96–127 | same | §15.4 |
| §14.2 example: (2,3) uint8+uint16 | Q=3, size 18, ordinal 5 at [15,18); planar b 12 B, ordinal 5 at 10–11; float32+bool Q=5, size 30, [25,30) | same | §14.2 |
| §14.3 example: P=10 alternating | `55 01` (fill false) / `55 FD` (fill true) | same | §14.3 |
| §14.5 example: (5,5)/(4,4) uint16 | 1 real + 15 padding, tile 32 B | same | §14.5 |
| §17.3 shuffle example, s=4 n=3 | `00 00 00 00 00 00 80 00 40 3F 40 40` | same | §17.3 |
| Full segment size | 2¹⁶ × 20 = 1,310,720 = 1.25 MiB | 1.25 MiB | §15.4 |
| Seg-CRC array at 2³² / 2³⁶ entries | 256 KiB / 4 MiB | 256 KiB / 4 MiB | §21.9 note |
| §9.2 Note: minimum commit growth | ≥ prior F + 68 → ≥ prior F + 128 | 68 → 128 | §9.2 |
| §9.3 Note: reachable F ceiling | largest multiple of 64 ≤ 2⁶³−1 = 2⁶³ − 64 | 2⁶³ − 64 | §9.3 |
| `[R-CNT-27]` floor | dir end ≥ 20, F−64 ≥ 20, F mult of 64 → F ≥ 128 | 128 | §5.1 |
| Register rows | F 35 / L 49 / T 26 / R 10 = **120**; F11 struck | 35 / 49 / 26 / 10; "120 conditions" | §21.2–§21.8 |
| Register instances (semicolon census) | **275** | "275 instances" | §21.8 |
| §20.3 example: 32-tile index re-emission | 32×20 + 4 = 644 | 644 | §20.3 |
| Requirement-ID inventory | 19 prefixes, all tabulated in §2.2, no gaps in any prefix's numbering (SER-04 present only as its withdrawal note) | — | §2.2 |
| §14.4 Note, P=1 bool | planar byte = `0xFE|v` when fill true, = v when fill false → coincide iff fill false | "coincide exactly when that fill is false" | §14.4 |
| §21.9 note: 65,536 layers ≈ 12.5 MiB | 65,536 × 200 B = 12.5 MiB | 12.5 MiB | §21.9 |

**Not one stated constant, offset or checksum in this document is wrong.** That is the
cleanest result I have from the arithmetic side, and I checked more than I expected to
have to.

### 3.4 The register's own instance rules, applied

§21.1 states the rules for the Instances column and I applied them to every row rather
than reading the totals:

- Layout-varying quantities enumerate their formulas (3: interleaved P·Q, planar
  numeric P·Bᶜ, packed bool ⌈P/8⌉). T3, T14, T22 = 3 layouts × 2 magnitude directions
  = 6 each. T21 ("larger than"), L44 ("exceeds") = 3 × 1. Every one matches.
- Magnitude comparisons enumerate two directions where either can be greater (L21 = 2
  layouts × 2 = 4; L22 = 2 + 2 alternatives = 4; L30 = 2; F17 = 2; F23 = 2). Checksum-
  against-computed and pattern-against-constant enumerate none (T1, F6, F14, F20, L37,
  L38 — all 1 or field-split only). Nonzero tests enumerate none (L20, L28). All match.
- R4's 16 = 8 frame constraints × 2 containers. I derived the 8 from §18.2's own
  carried-over list independently: magic, skippable frame, second frame, dictionary ID,
  content-checksum flag, bytes remaining after the frame, content-size larger,
  content-size smaller. Matches.
- L2's nine designated quantities: I derived them from `[R-ENC-04]` + §11.2 + §14.2 +
  §7.4 and got the same nine. The two domination claims in the cell check out —
  P·Q ≥ P·C because Q = ΣBᵢ ≥ C, and C·N > (C−1)·N + (N−1) = C·N − 1.
- The strict-specialization pairs §21.1 lists all hold: F1-front ⟹ F6, F1-magic ⟹ F8,
  F35 ⟹ F36, L24 ⟹ L25, F21 ⟹ F22 (extent_length 0 < 5), L10 ⟹ L11.

### 3.5 Closed counts I derived rather than trusted

"exactly thirteen sample types" — 13 table rows. "Three frame features are excluded"
(`[R-COD-06]`) — dictionary, content-checksum, oversized window: 3. "Four
restrictions apply" (§18.2) — 4 bullets. "exactly four vehicles" (§10.1) — 4. "Three
properties bound what a hostile file can make a reader spend" (§22.2) — 3. "Four
residues are stated rather than defended" (§22.3) — 4. "Conformance is defined for five
classes" — 5. "Six choices shape everything else" (App. D) — 6. §20.5's "one row for
each of the other seven spaces §10.2 tabulates (L31, L33, L34, L36, L43, L45, R1)" —
§10.2 tabulates 8 spaces, minus record type = 7, and the seven named rows map one-to-one
onto channel layout, linearization, sample type, codec, filter, index encoding, metadata
encoding. Every closed count in this document is correct.

### 3.6 The `[R-CNF-01]` convention, checked rather than assumed

I enumerated all 94 blockquote blocks and tested each for a leading *Note* / *Example* /
*Rationale* label. Exactly two are unlabelled: §1's "How to read this document", which
carries its own explicit *(non-normative)*, and **§15.1's tile-index region layout
block** —

> [ entry array: entry_count × 20 bytes ] [ segment CRC array: ⌈entry_count / 2¹⁶⌉ × 4 bytes ]

— which is normative and load-bearing (it is the only statement of the region's
composition and order). The briefing's claim holds; I verified it against the document
rather than accepting it. I graded nothing on the ">" marker.

---

## 4. Degradation walks — five traced end to end

**(1) Unknown top-level record type, MU = 1.** §19.1 step 4 → `[R-CNT-15]` →
reject-file. In a conforming file that type is necessarily experimental-range, since a
reserved-range type is F35/F36 whatever its MU bit — so §21.6's second "conforming file
a reader nevertheless refuses" is the right box. **Still served:** nothing; but §21.6
says the diagnostic must distinguish capability from corruption. The same type as a
*sub-record* is reject-layer and never a ground to refuse the file (`[R-CNT-18]`, and
§21.6 calls the qualifier load-bearing). I confirmed both branches are reachable and
disjoint.

**(2) Unknown codec.** A reader never meets one it must decline: all four assigned
codecs are core (`[R-COD-03]`, `[R-CNF-03]`), so any other value is 0/reserved/
experimental and is L43 — **reject-layer, at layer access, from declarations alone, with
no fetch.** **Still served:** every other layer, and the file's layer list. Same shape
for filter (L45), layout (L36), linearization (L33), sample type (L34), index encoding
(L31).

**(3) Truncated tail.** Physical file longer or shorter than committed_file_length →
F17 at open → reject-file, reported as *torn*. `[R-LIF-05]` forbids scanning backward,
so the reader cannot distinguish residue from corruption and §9.5's Note says it is not
asked to. **Still served:** nothing. Recovery (§9.6) is a separate, deliberate
operation, and its output must be re-verified whole before trust.

**(4) Checksum mismatch, by scope.** trailer → F14 reject-file; directory → F20
reject-file; crc_of_crc_array → L37 reject-layer; segment CRC → L38 reject-layer;
stored-tile crc → T1 reject-tile; user-metadata extent CRC → R2 **ignore-record** with a
SHOULD-report. I traced the last one specifically because it crosses the quarantine:
`[R-CNT-25]` overrides `[R-CNF-08]`'s owning-scope mapping, so a file-scope metadata
record whose extent CRC fails costs the record and nothing else. **Still served:** in
the tile case, every other tile including neighbours in the same layer; in the metadata
case, everything.

**(5) Limit exceeded.** `[R-ERR-04]`: the file stays conforming, the reader MAY decline
"at the whole file, or at the narrowest scope whose declarations exceed what it can
serve, a layer or a tile", and MUST report a resource limit, never a validity error. The
user-metadata document is the interesting case: it has no declared size, so §18.2's Note
routes an `[R-ERR-04]` decline to the *whole file*, while the ordinary path is
ignore-record for that record. Both are available and the document says so.

**(6) Foreign format major.** §2.3's `[R-CNF-13]` machinery: apply every *reaching*
condition first (F8, F14, F6, both F1 instances — the ones asserting invariants
`[R-CNT-24]` fixes in every major), treating a failure as reject-file **on the
requirement's ground**; only if all of them pass is the distinct capability diagnostic
`[R-CNT-07]` asks for owed. A verifier that establishes a reaching failure reports
*nonconforming* whatever the declared major. I could implement this from the text
without guessing; the §2.3 Note's three worked rows (F14 reaches, F5 does not, F15 does
not) are each independently correct on the reasoning they give.

---

## 5. Putting §21.7's test to requirements

The brief asks for this explicitly, so I wrote the quantifiers out and then ran a dozen
requirements through them.

### 5.1 Do the quantifiers do what the sentence claims?

Let X = the files exhibiting condition c; Sep(f,g) = "some check this specification
obliges a reader or a verifier to perform tells f from g".

- **Unwitnessed** ("for every file exhibiting it, some file that does not exhibit it
  cannot be told apart from it by any check…"): ∀f ∈ X · ∃g ∉ X · ¬Sep(f,g).
- **Detectable** ("some file exhibiting it is separated by such a check from every file
  that does not"): ∃f ∈ X · ∀g ∉ X · Sep(f,g).

¬(∀f ∃g ¬Sep) = ∃f ∀g Sep. **The two are exactly each other's negation, as claimed.**
The sentence "each quantifier is the other's dual" is true and I could not break it.
§21.1's restatement ("a condition is detectable exactly where some file exhibiting it is
separated, by a check this specification obliges a reader or a verifier to perform, from
every file that does not") is quantifier-for-quantifier identical to §21.7's. That is
the restatement the brief warned me to check word for word, and it does not drift.

### 5.2 A dozen requirements put to it

Worked in order; ✔ = the test decides it, and decides it the way the document does.

1. **`[R-COD-06]`, undisclosed dictionary.** Take f = a tile compressed with a private
   dictionary, dict_id 0. Take g = the byte-identical file emitted without one. No check
   separates them because there is nothing to separate. **Unwitnessed ✔** — and §21.7
   names it. The test shows *why*: the condition is about provenance, not bytes.
2. **`[R-COD-10]`, mis-strided filter.** Where the resulting image breaks §14.5 or
   `[R-SER-08]`, a verifier check separates it → **detectable**, registered as T26.
   Where it breaks neither, the image is just other bytes → **unwitnessed**. One
   requirement, conditions of both kinds. §21.7 anticipates exactly this ("A single
   requirement states conditions of both kinds where it states several"). ✔
3. **`[R-CNT-18]`'s nesting prohibition.** A sub-record of an unknown type whose payload
   happens to parse as records is byte-identical to one that does not "contain" records,
   because `[R-CNT-15]` makes the payload opaque; a user-metadata sub-record's payload is
   one byte (`[R-MTA-03]`); a nested *layer* record is L26. **Unwitnessed ✔** — §7.4's
   Note reaches the same conclusion by the same route.
4. **`[R-WRT-05]`, byte-identical re-emission.** The output does not record the prior
   directory, §9.7's walk reads only the live state, and §9.6's backward probe is not a
   check any actor is *obliged* to perform (it is "diagnosis — … not a finding about the
   file it was given"). **Unwitnessed ✔**, and §20.4's Rationale says so independently.
5. **`[R-SLB-04]`, stale slab declaration.** The rule's disjunct is satisfied whenever
   the invariants in fact hold, so every file exhibiting it exhibits L41 or L42.
   **Detectable, and a strict specialization** — §16.2's Note is right that it needs no
   row of its own. ✔
6. **`[R-CNT-03]`, zeroed gaps.** Non-zero gaps are plainly visible — *detectable* — but
   it is a SHOULD, so `[R-CNF-12]` keeps it out of a register that "enumerates MUST-level
   conditions only". The test correctly says nothing, because detectability is not the
   gate for SHOULDs. ✔
7. **§6.2's over-long pre-trailer gap.** F − 64 − (dir_offset+dir_length) > 63 is
   visible in the live state, so the condition is *detectable* — yet `[R-CNF-02]`
   expressly declares it not a file-conformance violation. Correctly absent from the
   register on the **conduct** ground rather than the detectability ground, and
   `[R-CNF-02]` names it as one of the two cases. ✔
8. **§6.3's flags = 0 against a set ignore-lane bit.** Same shape; §21.6 records it. ✔
9. **§10.3's "not in released software".** Visible value, invisible predicate ("released
   software or published data"). **Unwitnessed**, and the prohibition binds conduct. ✔
10. **`[R-ENC-06]`, fixed field widths.** §21.7's *second* ground: no condition a file
    can exhibit, because the parse is always at the fixed widths. ✔
11. **`[R-CNT-02]`'s "belongs to no class" half.** §5.2's Note: `[R-LIF-08]` makes every
    unreached byte slack, so the condition describes nothing. Second ground again; only
    disjointness is registered (F33, L18). ✔
12. **`[R-WRT-07]`, "the output's reference arrays MUST equal the live generation's".**
    Relates two files; the output alone carries no witness. Absent from the register,
    correctly. ✔ — but see finding reader-05: this and the §20.3 bars belong to §21.7's
    *second* ground, not its first, and the document files them under the first.
13. **The §14 bar itself** (§20.3). Take f produced by a bar-violating commit and g a
    byte-identical file produced by a creator in one commit. No check separates them —
    the bar's subject is a *commit*, and no file records the generation it superseded.
    So the bar is never witnessed, anywhere. §20.3 says it has no witness only "where …
    the live state being clean". See findings reader-04 and reader-05.

**Where the test works, and it mostly does.** For every condition whose subject is a
*file*, the test decided it cleanly and agreed with the register. I could not find a
detectable, un-rowed, MUST-level file-conformance violation: I swept §6.1, §6.2, §7.1,
§7.2, §7.4, §8.1, §14, §15.1, §15.4, §17.2, §17.3, §18.2 requirement by requirement,
and every byte-visible MUST landed on a row. The register looks complete to me.

**Where it stops working** is at the two places the document applies it to conditions no
file exhibits — the §20.3 bars and §20.5's version_minor obligations. That is findings
reader-03, reader-04 and reader-05.

**Where the instrument itself is not fixed** is finding reader-01, which is the one I
think matters most.

---

## 6. Findings

### reader-01 — CONTRADICTION — §2.4 `[R-CNF-12]` scopes a verifier's checking duty to the register's own rows, which is precisely the instrument §21.7 says its test does not use

**Location:** §2.4 `[R-CNF-12]`; §21.7 `[R-ERR-01]`; §21.1's completeness clause.

**Quotation (§2.4, `[R-CNF-12]`):**

> A verifier owes no search for one: §2.3's duty to check every file-level requirement
> runs to the MUST-level conditions §21 inventories, and a SHOULD deviation is reported
> where the verifier observes it and not hunted for.

**Quotation (§21.7, `[R-ERR-01]`):**

> The instrument is the checks this specification obliges an actor to perform, and
> deliberately not the register's own rows — a test keyed to the rows would make §21.1's
> completeness clause vacuous, every omitted condition being undetectable by construction.

**The problem.** §21.7's test is defined over "any check this specification obliges a
reader or a verifier to perform". The reader's obliged checks are, by §19.2 and §21.1,
exactly the register rows whose Detector cell reads *reader* — so the reader half of the
instrument is already row-keyed. The whole force of §21.7's disclaimer therefore rests
on the **verifier's** obliged checks being *broader* than the rows. §2.3 supplies that
breadth ("checks every file-level requirement — including those ordinary readers are
exempted from"). `[R-CNF-12]` then narrows it, and the natural restrictive reading of
"the MUST-level conditions §21 inventories" is *the conditions the register inventories* —
the rows.

Under that reading the instrument is rows ∪ rows = rows, §21.7's "deliberately not the
register's own rows" is false of its own test, and §21.1's completeness clause becomes
exactly the vacuity §21.7 says it was built to avoid: any condition the register omits
is, by construction, one no obliged check separates, hence unwitnessed, hence properly
omitted. The clause could then never be violated and could never be used to find a gap.

**Permitted readings.**

(A) *Restrictive* — the duty runs to precisely those MUST-level conditions §21
inventories. Grammatically the default (no comma before "§21 inventories"); it also
makes `[R-CNF-12]`'s "owes no search" bite hardest, which is the sentence's rhetorical
job. Contradicts §21.7.

(B) *Non-restrictive* — the duty runs to MUST-level conditions (of which §21 is the
inventory), as against SHOULD deviations, which is all the sentence is arguing about.
Compatible with §21.7, with §2.3's "every file-level requirement", and with §9.7's "a
verifier MUST NOT certify past a violation it has not looked for".

**I picked (B)**, because it is the only reading under which §21.7's test, §21.1's
completeness clause and `[R-CNF-07]`'s outcome gate are all non-vacuous, and because
§2.3 states the duty in unqualified terms that `[R-CNF-12]` is not obviously trying to
amend. But a careful implementer reading `[R-CNF-12]` on its own will take (A) — it is
the plainer English — and will then build a verifier whose search space is the 120 rows
and nothing more.

**What an implementer does wrong without it.** Two verifier implementations diverge in
scope: one checks 120 enumerated conditions, the other checks every MUST-level
file-level requirement in the document. On a file exhibiting a byte-visible MUST-level
violation the register happens to omit, the first certifies and the second reports
*nonconforming*, and both believe themselves conforming. More seriously, reading (A)
disarms the only mechanism this document has for detecting its own register gaps: an
auditor applying §21.7's test under reading (A) can never find one.

**Byte-level: no.** The disputed file is nonconforming under both readings (it violates
a MUST-level file-level requirement), so `[R-CNF-05]` bars every conforming writer from
emitting it either way and the emittable set does not move. A verifier-verdict fork
exists in principle — a certify-vs-nonconforming disagreement — but exhibiting it
requires a detectable, un-rowed MUST-level file-conformance violation, and my sweep of
§6–§18 found none; §21.1's completeness clause asserts none exists. I will not claim a
fork I cannot name a file for.

---

### reader-02 — AMBIGUITY — §20.3's §14 bar lists "the set of padding positions" among what a commit may not alter, and every growth over a stored edge tile alters it

**Location:** §20.3 step 4, `[R-WRT-04]` (the §14 bar, and the growth permission in the
same step); §11.1's Rationale.

**Quotation (the bar):**

> A commit MUST NOT change a layer's declarations in a way that alters, for any tile that
> layer stores **in the generation this commit supersedes**, what §14 fixes for its stored
> bytes or how they decode — the set of padding positions (§11.3) and the content
> `[R-SER-05]` fixes there, the decoded size, the byte offset of any sample within the
> decoded tile image, the sample type each value in the image is read under, or the codec
> and filter that produced the stored bytes. Call this the **§14 bar**.

**Quotation (the permission, same step):**

> and an extent MAY **grow**, since a position that becomes real held, for each channel
> the position carries, that channel's fill (§14.5), and fill is a legal sample value …
> a growth is permitted exactly where the geometry it produces satisfies every rule that
> geometry is subject to.

**The problem.** Growing Eᵢ where Eᵢ mod Tᵢ ≠ 0 converts padding positions of the
existing high-edge tile into real positions. That tile is one the layer stored in the
generation the commit supersedes, and the growth **alters its set of padding positions** —
the first item on the bar's own list. Read against the list, every such growth is barred.
Read against the express MAY two paragraphs later, every such growth is permitted.

The document supplies a reconciliation, but only obliquely: "the list names where that
effect arises rather than standing on its own: a change that leaves every one of those
tiles' stored bytes meaning exactly what they meant … is not what this bars." The two
carve-out examples it then gives are an identity-stride filter and "**a new** padding
position whose stored byte already holds the fill" — both *shrink*-direction cases. The
growth direction (padding → real) is nowhere in the carve-out, and it is not obviously
covered by "meaning exactly what they meant": a byte that meant "padding, never returned
(`[R-GEO-04]`)" now means "a fill-valued sample of the reference array". The reference
array demonstrably changes — that is the point of a growth.

**Permitted readings.** (i) The list is a definition of what "alters" means, so growth
over a stored edge tile is barred and must instead be a new layer or a whole-file
rewrite. (ii) The list is illustrative, the effect test governs, and the express MAY
settles growth. **I picked (ii)** — the MAY is specific, states its own reason, and
§11.1's Rationale agrees ("Of its two bars the one reaching a shrink or a growth is the
§14 bar", then permits growth). But (i) is what a careful implementer gets from reading
the bar's own words, and the bar is the normative sentence.

**What an implementer does wrong without it.** An appender built on (i) refuses the
central schema-first workflow §11.1 exists to support — declare a layer, store tiles,
then grow extents as data arrives — for any layer whose extents are not an exact
multiple of its tile extents, and forces a whole-file rewrite instead.

**Byte-level: no.** The file a permitted growth produces is itself conforming under both
readings — its padding set, decoded sizes, entry_count and `[R-SER-05]` content all check
out — and a creator can emit byte-identical bytes in one commit (slack content is
unconstrained, §5.2). So the set of conforming files does not move; only the route to
one does. Reading (i) costs an updater a rewrite; it does not change a byte or a verdict.

---

### reader-03 — OBSERVATION — §20.5's "Neither obligation has a witness in the output alone" is false for the `[R-CNT-26]`-floor branch on an ordinary compacted output

**Location:** §20.5, `[R-WRT-06]`.

**Quotation:**

> Otherwise version_minor follows `[R-CNT-26]`'s floor. Neither obligation has a witness
> in the output alone (§21.7).

**The problem.** The two obligations are (i) "the output's version_minor SHOULD be at
least the input's", which applies where the output carries a later-minor feature the
compactor does not implement, and (ii) the `[R-CNT-26]` floor otherwise. (i) is indeed
unwitnessed: the output does not record the input's minor.

(ii) is not, in the ordinary case. §20.5 itself enumerates exhaustively how a *conforming*
file can carry a later-minor feature — "a carried ignore-lane bit (§6.3) or an
unrecognized `tarn.` key in a record it never decoded (§18.3), the two of §10.1's four
vehicles §21.6 makes conforming, the other two reaching such a file only as values this
text still registers as reserved-range violations". So on an output with `flags` = 0 and
no unrecognized `tarn.` key, there is no later-minor feature at all, `[R-CNT-26]`'s floor
is the stated "for a file expressible under this text, 0", and a `version_minor` other
than 0 is visible in the trailer's own bytes at F − 54. That is a witness in the output
alone. Appendix G item 8's defence ("this item's floor turns on which features the
compactor implements") does not rescue it, because in this branch the output carries no
feature for the compactor to have failed to implement.

**Byte-level: no.** Both obligations are SHOULDs, and `[R-CNF-12]` places SHOULD
deviation outside the register entirely, so nothing here can move the emittable set. The
cost is to a verifier's report: told there is no witness, it will not report an advisory
it could in fact observe on every ordinary compacted file.

---

### reader-04 — AMBIGUITY — §20.3's "This is precisely where the §14 bar has no witness, the live state being clean" has an undetermined antecedent, and is false under the wider reading

**Location:** §20.3 step 4, `[R-WRT-04]` (the shrink paragraph).

**Quotation:**

> The bar beside the §14 bar does not reach a shrink either: it bars a change to a planar
> layer's channel declarations that moves a stored tile's disk ordinal, and a shrink is
> not one. This is precisely where the §14 bar has no witness, the live state being clean,
> which is why the rule is stated here and not left to the rows.

**The problem.** "This" has at least two available antecedents, and they give different
truth values.

(a) *The shrink case generally.* Then the claim "the live state being clean" is false. A
shrink that turns real positions into padding positions of a tile the **new state still
stores**, where those positions do not already hold fill, leaves a stored tile whose
padding content violates `[R-SER-05]` — which is T4, sitting in the live state, and
registered. The live state is not clean, and the bar is witnessed there in the only sense
the sentence can mean.

(b) *The narrow sub-case the two preceding sentences build up to* — a shrink that
unstores or de-addresses the very tile it damages. Then the live state is clean and the
claim is true, but "precisely where" is doing a lot of work to pick out a sub-case that
the sentence does not name.

**I picked (b)**, because the two sentences immediately before it are about exactly the
unstore/de-address rescue ("Unstoring that tile in the same commit does not rescue it
either … whether or not the new state still stores it"). But (a) is the reading a
sequential reader gets, since the paragraph's declared subject is "a shrink".

There is a further wrinkle that neither reading fixes, and it is finding reader-05: on
§21.7's own test the §14 bar has no witness **anywhere**, because its subject is a commit
and no file records the generation it superseded — a file produced by a bar-violating
commit is byte-identical to one a creator emitted in a single commit.

**What an implementer does wrong without it.** Under (a) a verifier concludes that a
still-stored tile damaged by a shrink is unregistrable and does not look for it; under
(b) it looks, finds T4, and reports *nonconforming*. The file is nonconforming either
way — T4 is registered and its detection is a verifier's — so this costs a report line,
not a verdict.

**Byte-level: no.** Under both readings the file with wrong padding content is
nonconforming (T4, `[R-SER-05]`), so `[R-CNF-05]` bars a conforming writer from emitting
it either way and the emittable set does not move.

---

### reader-05 — OBSERVATION — §21.7's two grounds are stated over files, and §20.3 and §20.5 apply the wrong one to conditions no file can exhibit

**Location:** §21.7 `[R-ERR-01]`; §20.3 step 4 `[R-WRT-04]`; §20.5 `[R-WRT-06]`;
compare §18.2 `[R-MTA-09]`, which gets it right.

**Quotation (§21.7):**

> Distinguish an unwitnessed condition from a requirement that states **no condition a
> file can exhibit**. `[R-ENC-06]`'s fixed field widths are not a state a file can be in …
> Nothing is omitted from the register on its account, there being no condition to omit.

**The problem.** §21.7 defines *unwitnessed* over "every file exhibiting it" and
*detectable* over "some file exhibiting it" — both quantify over **files** — and then
expressly tells the reader to distinguish those from requirements stating no file
condition at all.

The §14 bar and the planar-ordinal bar of §20.3 bind a **commit**: their subject is a
relation between the generation a commit supersedes and the one it writes. No file is in
that state. §20.5's version_minor obligations bind an **input/output pair**. Both
passages nonetheless reach for §21.7's first ground — "This is precisely where the §14
bar has no witness"; "Neither obligation has a witness in the output alone (§21.7)" —
when the second ground is the one that applies. §18.2 shows the document knows the
difference and can apply both cleanly in one sentence: "dictionary use the header does
not disclose is a writer violation nothing in the extent shows — an unwitnessed condition
… — while the bar on sizing a buffer binds a reader rather than the document, and so
states no condition a file can exhibit at all."

**Why it matters to a reader trying to apply the test.** §21.1's completeness clause and
`[R-CNF-07]`'s outcome gate both turn on §21.7's test, and the test's subject is a file.
An implementer or auditor asked to run the test over the §20.3 bars has nothing to run it
on: there is no f ∈ X to quantify over, because X is empty as a set of files. The
document's own words for that situation are the second ground, and neither §20.3 nor
§20.5 uses them. §21.7's "That is the whole of the test, and it decides any condition put
to it without appeal to a list" is therefore overstated for the class of conditions §20.3
and §20.5 put to it — those are decided by observing they are not file conditions at all,
which is the *other* ground.

**Byte-level: no.** Both grounds keep a condition out of the register, so the register is
unchanged and no reader or writer behaviour turns on which label applies.

---

## 7. What I could not determine, and what I checked that found nothing

- **Whether the register is complete.** I could not find a detectable, un-rowed,
  MUST-level file-conformance violation, and I looked requirement by requirement through
  §4, §5, §6, §7, §8, §9, §11–§18. I also checked that every one of the 19 requirement
  prefixes used appears in §2.2's table and that no prefix's numbering has a gap.
  Everything byte-visible landed on a row. But finding reader-01 means the document's own
  instrument for answering this question is not fixed, so my "I found none" is an
  empirical result and not a derivation.
- **Slab and alignment.** §16's invariants, the run partition (⌈N/S⌉ runs per block, never
  spanning channel blocks), sentinel and structural-reject transparency, and §16.2's
  worked example (four runs of a 4×8 row-major grid = four tile rows; ordinal 10 a
  sentinel closes the packing) all check out. `[R-SLB-04]`'s no-row justification survives
  the §21.7 test. I found nothing.
- **Codec constraints.** `[R-COD-06]`'s Note about the 1 KiB Window_Descriptor floor is
  correct — RFC 8878's minimum expressible window is 2¹⁰, so a sub-1-KiB tile is encodable
  under codec 3 only single-segment, and there Window_Size *is* the content size, which
  the same rule pins to the decoded size. §18.2's transposition of that reasoning to
  documents (where the decoded-size and Window_Size constraints are both replaced) is
  internally consistent and its R3/R4 routing is complete against §18.2's own carried-over
  list. I found nothing.
- **The filter.** L divisible by s in all three cases; the permutation is the identity
  exactly when s = 1 or n = 1, which is what Appendix G item 5 claims. I found nothing.
- **Degenerate legal files.** I checked the extent-0 layer (N = 0, entry_count 0, extent
  slot (0,0), crc_of_crc_array 0, `[R-COD-07]`'s cap escaped, `[R-ENC-04]`'s ceiling still
  binding on P·Q and P·Bᶜ), the 128-byte empty file, P = 1 single-channel bool in both
  layouts, and a layer whose every entry is the sentinel. All consistent; §21.9's
  per-instance individuation ("A layer addressing no tile therefore has no tile whose
  decoded size the table bounds") is right.

