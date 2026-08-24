# Round 23 — Verifier implementer, working transcript

## 0. Disclosure, up front

I read exactly one file from the repository: `/Users/robertkleffner/Documents/GitHub/tarn/spec/tarn.md`,
in five sequential `Read` calls covering lines 1–4426 (the whole document). I ran
`grep` against that file once (to enumerate every occurrence of "verifier"). All
other computation was local Python over data I typed in myself, in a private
directory I created.

**Context I did not ask for, and did not act on.** Before I began, my runtime
placed in my context: a project instruction file (`CLAUDE.md`, which only
redirects to `AGENTS.md`), and an index of the maintainer's auto-memory listing
six memory-file titles with one-line descriptions. Two of those descriptions
name things adjacent to this exercise. I did not open any of them, and I have
disregarded their contents in reaching every conclusion below. Naming that they
appeared is the disclosure; I am not repeating what they said.

**A second, unexpected disclosure.** My scratchpad is not private. On my second
Bash call, a `crc.py` I had written one call earlier had been replaced by a
*different* `crc.py` (different identifiers, different print strings) — another
agent is writing into the same directory concurrently. Listing the directory to
diagnose that showed me filenames I had not created: `accumulated.diff`,
`checks_block.txt`, `flat.txt`, `rows.txt`, `inst.txt`, `edits*.json`,
`r89*.json`, `r23audit/`, `round23/`, plus some `.zst` fixtures. **I opened none
of them.** The only content I saw from any of them was the first five lines of
the overwritten `crc.py` (a CRC-32C table generator, substantively identical to
my own and carrying no information about TARN). I then moved all my work into
`scratchpad/vfy-priv-r23/` and worked there. I report the filename exposure
because a filename like `accumulated.diff` or `rows.txt` is itself a weak signal
about what changed, and a disclosed brush is usable where a silent one is not. I
did not read the file, and nothing below rests on it.

I did not read any ADR, any conformance vector, `registry.json`, `PLAN.md`,
`AGENTS.md`, `README.md`, `OPEN-QUESTIONS.md`, or any git history. I ran no web
search and no web fetch.

---

## 1. What I built

A conforming verifier, on paper and then in ~330 lines of Python that reads
nothing but a candidate file and reports a verdict. Then a family of files to
run it against: a four-generation lifecycle (create → append → update →
compact), ten adversarial layouts, three degenerate-but-legal files, and one
short foreign-major file. Every checksum constant the document states and every
worked numeric example it gives, recomputed.

I will give the algorithm first, then the walks, then the findings.

---

## 2. The certification procedure, as an ordered algorithm

### 2.1 Verdict vocabulary and what bars certification

§2.3 fixes three verdicts and their availability, and I found it complete once I
had assembled it from four places (§2.3, §2.4's `[R-CNF-12]`, §17.4's
`[R-COD-11]`, §18.2's `[R-MTA-09]`):

| Verdict | When |
|---|---|
| *conforming* | the traversal established no violation and left no requirement unchecked |
| *nonconforming* | **any** established violation, however many requirements went unchecked — "An established violation takes priority" |
| *cannot establish* | no violation established, but ≥1 requirement unchecked on a **capability or resource** ground |

Three report-level channels sit beside the verdict and never change it:

- **per-requirement unchecked report** — owed under all three verdicts:
  "A verifier MUST report each requirement it was unable to check on a
  capability or resource ground, naming the requirement and the ground,
  whichever of the three verdicts it reports; that per-requirement report
  constrains the report and not the verdict".
- **unexamined scopes** — only for a verifier that exercises `[R-CNF-11]`'s
  licence to stop at the first violation. "*Unexamined* is neither a verdict nor
  *cannot establish*."
- **advisories** — SHOULD deviations. `[R-CNF-12]`: "a verifier reports a SHOULD
  deviation as an advisory that does not bar certification. A verifier owes no
  search for one". So my verifier reports SHOULD deviations it happens to
  observe (a non-zeroed gap, a `version_minor` above the floor) and hunts for
  none.

The closed list of cannot-establish grounds, assembled:

1. `version_major` names a major it does not implement (§2.3).
2. A record carries MU = 1 with a type it does not implement (§2.3, §21.6) —
   top-level *or* layer sub-record; §2.3 does not distinguish, and §21.6's
   top-level/sub-record distinction is about a *reader's* refusal scope, not the
   verifier's verdict.
3. It cannot execute a layer's codec or filter (`[R-COD-11]`).
4. It declines a layer's or a tile's decode on resource grounds, and so cannot
   check §14's decoded-content obligations (`[R-ERR-04]`, `[R-SER-05]`,
   `[R-SER-08]`).
5. It declines to decode a user-metadata document (`[R-MTA-09]`).

And one explicit **non**-ground, which I had to read twice: a user-metadata
document under an encoding this specification does not assign. "no content rule
attaches there, so nothing is left unchecked, and certification is unaffected
(`[R-MTA-10]`, §21.6)."

Also a non-ground, and stated so I could not get it wrong: §21.7's undetectable
content errors. "None of these is a requirement a verifier is *unable to check*
within the meaning of `[R-CNF-11]`: no file-level witness exists to check, so
nothing about the file is left undetermined and the verdict is unaffected." That
sentence saved me from a wrong design — my first sketch had the verifier
reporting "cannot establish" for any layer whose codec might have hidden a
dictionary.

### 2.2 The ordered algorithm

```
V0  Physical size Fp.
V1  Trailer, in §6.2's mandated order, no reordering permitted:
      magic at [Fp-64, Fp-56)        -> F8   reject-file, stop
      trailer CRC [60,64) over [0,60)-> F14  reject-file, stop
      version gate:
          version_major == 0         -> F18  reject-file, stop
          version_major != 1         -> CANNOT ESTABLISH, stop
      (only these three touch fields [R-CNT-24] fixes across majors)
    then, gates passed, all of:
      flags incompat lane            -> F19
      F == Fp                        -> F17
      F mod 64 == 0                  -> F13
      dir_offset >= 16               -> F9
      dir_length >= 4                -> F16
      dir_offset+dir_length <= F-64  -> F10 (overflow of the sum -> F3)
      1 <= generation                -> F11
      file_id != 0                   -> F12
      reserved [56,60) zero          -> F15
      any u64 above 2^63-1           -> F2
V2  Front block [0,16) by byte equality       -> F6 / F1
    A verifier has NO residency exemption here; App H says so in terms.
V3  Directory CRC over [dir_offset, dir_offset+dir_length-4) -> F20, stop on fail
V4  Record walk (§7.2 framing, no residue)    -> F29, F24
    per record: multiplicity F34; MU gate F35; reserved-range F36;
      flag bits F25/F26; registry flags F28; extent slot F30/F31/F32
V5  Layer-name uniqueness over raw name bytes -> F4
V6  Per layer, §19.3's full validation, then the index chain,
    then per entry §15.3, then per stored tile: fetch, entry CRC,
    decode, decoded size, padding content, pad bits, interleaved bool bytes
V7  Alignment / slab invariants                -> L40, L41, L42
V8  Coverage walk (§9.7): disjointness, bounds, checksums, slack total
V9  Pre-trailer gap emptiness                  -> F7
V10 Verdict + reports
```

Two ordering decisions I had to make from the text rather than read off it:

- **V2 before or after V3?** `[R-CNT-04]` says a reader holding [0,16) resident
  "MUST verify the full block by byte equality **before other processing**". A
  verifier always holds it (§2.3, App H). So V2 is before V3. But V2 is *after*
  V1, because §6.2's ordering is explicit and mandatory and §21.2's preamble
  confirms the trailer magic and CRC precede everything. I placed V2 between
  them, which satisfies both.
- **V9 after V8**, because F7 ("a structure occupies bytes between the live
  directory's end and the live trailer") is decidable only once every claimant's
  extent is known.

### 2.3 What the verifier reports when a check cannot be run

Four distinct report lines, and I want to record that they are *four*, because
my first draft collapsed two of them:

1. `unchecked(requirement, ground)` — §2.3. Forces *cannot establish* unless a
   violation was established.
2. `unexamined(scope)` — §2.3. Does not force anything.
3. `ignored(scope, encoding, stored extent length)` — `[R-MTA-10]`, for a
   user-metadata record at an **unassigned** encoding. Explicitly **not** an
   unchecked requirement, explicitly **not** a bar to certification.
4. `advisory(SHOULD deviation)` — `[R-CNF-12]`.

(3) is the one that surprised me. `[R-MTA-10]`: "it MUST report each record it
ignored on this ground, naming the owning scope, the encoding value, and the
stored extent length, as it reports the slack total (`[R-CNT-21]`): bytes a
certificate covers without inspecting are counted and named, never silent."
That's a *report* obligation with no verdict consequence. It is the only such
obligation in the document, and finding **verifier-02** below is about the
structurally identical case it does not reach.

---

## 3. Checksums: which structures, and is every live structure covered?

### 3.1 The map, resolved

§8.1's map plus §4.5's carve-outs give three populations, not two:

**(a) Covered by exactly one checksum** — trailer bytes [0,60); the directory
region's record sequence; index entries (per segment); the segment CRC array
(by `crc_of_crc_array`); `crc_of_crc_array` itself (by the directory CRC); each
stored tile's bytes; each user-metadata extent's pre-terminal bytes.

**(b) Verified by comparison, covered by no further checksum** — the front
signature block (equality, not a checksum) and the three *terminal* checksum
fields: trailer [60,64), the directory region's final 4, a user-metadata
extent's final 4.

**(c) Live-state bytes covered by no checksum at all** — exactly one row:
"| Extent of a record of a type this specification has not assigned | none — the
bytes are opaque (§7.2) | — |".

So the answer to my charter's question is **no**: not every live structure is
covered by a checksum. §22.3's `[R-SEC-04]` states the consequence plainly:
"The extent of a record of a type this specification has not assigned is covered
by no checksum either (§8.1), so corruption inside it is equally invisible".

I built a file to make (c) concrete — see §5.4 below.

The chain of trust (§8.2) is strictly ordered and I implemented it in exactly
that order: trailer → directory → `crc_of_crc_array` → segment CRC array →
index segment → index entry → stored tile. `[R-ENC-05]` forbids acting on any
integer before the checksum covering it verifies, and `[R-ENC-10]` carves out
"comparing a field against a constant for validation", which is what makes
§6.2's ordered gate legal at all (you compare the magic before the CRC that
covers it).

### 3.2 Constants I reproduced

CRC-32C implemented from §4.5's parameters (Castagnoli 0x1EDC6F41, reflected in
and out, init 0xFFFFFFFF, final XOR 0xFFFFFFFF), used in its reflected form
0x82F63B78.

| Constant | Stated | Computed | Where |
|---|---|---|---|
| CRC-32C(`"123456789"`) | `0xE3069283` | `0xe3069283` | §4.5, App B |
| CRC-32C(zero bytes) | `0x00000000` | `0x0` | §4.5, App B |
| CRC over 4 sentinel entries (80 B) | `0x80A34955` | `0x80a34955` | §7.4 example |
| `crc_of_crc_array` over `55 49 A3 80` | `0xC4EE982E` | `0xc4ee982e` | §7.4 example |
| CRC of a full 2¹⁶-sentinel segment | `0xEECB3BB2` | `0xeecb3bb2` | `[R-IDX-05]`, App B |
| Appendix A trailer CRC | `0xE00938D2` | `0xe00938d2` | App A |
| Appendix A directory CRC | `00 00 00 00` | `0x0` | App A |

All seven reproduce. I also decoded Appendix A's entire 128-byte hexdump field
by field against its own annotation table: `version_major` 1, `version_minor` 0,
`flags` 0, `generation` 1, `dir_offset` 16, `dir_length` 4,
`committed_file_length` 128, `file_id` 0x0123456789ABCDEF, reserved zero. Every
row of the table is right, and F mod 64 = 0.

The 2¹⁶-sentinel constant is worth a note: `[R-IDX-05]` licenses emitting it
"for any **full** segment — one covering exactly 2¹⁶ entries, final or not"
and requires a partial segment's CRC to be computed. My four-sentinel segment
CRC (`0x80A34955`) is indeed different from `0xEECB3BB2`, which is the fact that
rule turns on, and I confirmed it rather than assumed it.

### 3.3 Constants I could **not** reproduce

- The zstd compressed-frame magic `28 B5 2F FD` (0xFD2FB528) and the LZ4 frame
  magic `04 22 4D 18` are external facts about RFC 8878 and the LZ4 block
  format. I could not check them from this document, and I deliberately did not
  reach for prior knowledge as evidence. Same for gzip's `1F 8B`, zlib's CMF/FLG
  framing, and the `0x7E000000` lz4 cap.
- The CRC-32C polynomial value `0x1EDC6F41` as cited to RFC 3720 §12.1 is
  external. What I *can* say is that the parameter set as a whole is
  self-consistent: taking that polynomial reflected reproduces both stated check
  vectors and all five in-document CRC constants, so the six parameters §4.5
  gives cannot be independently wrong.
- §21.9's minimum guarantees are chosen numbers, not derivable.

---

## 4. The coverage walk

### 4.1 The partition, as the document actually defines it

§5.2's `[R-CNT-02]` names the classes: the front signature block; or a
*structure* — "a stored-tile extent, a record extent (the bytes any record's
extent slot references, whatever the record's type, §7.2), the directory, or the
trailer". §9.7 tells the verifier how to reach them, and adds two members
`[R-CNT-02]` names but §9.7's traversal would otherwise miss: "The front
signature block at [0, 16) and the live trailer at [F − 64, F) are claimed by
the walk as well".

Three traps in §9.7 that I had to implement exactly:

- A record is **not** a claimant of its own header and inline payload — those
  lie inside the directory region, "which is the claimant covering them".
- A layer record's extent slot addresses the tile-index region, "so the region
  enters the walk once, as that record's extent, and is not a second claimant
  beside it."
- An entry `[R-IDX-03]` classifies reject-tile **on a structural ground**
  contributes no stored extent; "one whose stored bytes alone fail its crc keeps
  its extent". So a T1 (bad tile CRC) entry is still a claimant, and a T8/T9/T10
  entry is not. §15.3 marks exactly six rows *structural*, and I counted them:
  sentinel-with-crc≠0, half-sentinel, length 0, offset < 16, out-of-domain,
  and overflow/past-F−64. Six. The seventh row (crc failure) is explicitly not.

**Can a byte be neither claimed nor slack?** No, and the document says so rather
than leaving me to infer it. `[R-LIF-08]`: "Bytes the walk does not reach are
slack". §5.2's Note: "'belongs to no class' describes nothing, and a register
row for it would be a row no file could exhibit." So of `[R-CNT-02]`'s two
halves only disjointness is testable, and that is what my V8 checks.

### 4.2 A concrete file, with the arithmetic

I built layer `sst`: rank 1, dimension `x` with E = 100, T = 32, interleaved,
one float32 channel `temp` with fill `00 00 C0 7F` (the quiet NaN 0x7FC00000),
codec 1, filter 1, no alignment, no slab. This is §7.4's example layer, and I
used it precisely so the document could check my encoder rather than the other
way round: my inline payload came out **81 bytes**, and §7.4's worked example
says 81 with the same field-by-field breakdown (4 + 34 + 18 + 12 + 13). Grid
count ⌈100/32⌉ = 4, so `entry_count` = 4, and `[R-CNT-17]`'s extent length
4 × 20 + ⌈4/2¹⁶⌉ × 4 = **84**, which is what my index region measured.

Decoded size per tile: P = ∏Tᵢ = 32, Q = ΣBᵢ = 4, so P·Q = **128** bytes.

Generation 1, tiles 0 and 1 stored, tiles 2 and 3 sentinel:

```
[     0,    16)   16   front signature block
[    16,   144)  128   stored tile 0
[   144,   272)  128   stored tile 1
[   272,   356)   84   tile-index region  (= layer record's extent)
[   356,   465)  109   directory (105-byte record + 4-byte CRC)
[   465,   512)   47   pre-trailer pad          <- SLACK
[   512,   576)   64   trailer
```

F = 576, F mod 64 = 0. Claimed = 16+128+128+84+109+64 = **529**.
Slack = 576 − 529 = **47**, and the 47 is exactly the pad. Walk complete, so the
total is exact and not partial. Verdict: **conforming**.

I ran the same arithmetic on Appendix A's minimal file as a cross-check:
claimed 16 + 4 + 64 = 84, F = 128, slack = **44** — which is the number §5.1's
example states ("44 bytes of slack, zeroed by advice"). Two independent
constructions, both agreeing with the document.

### 4.3 The three populations, restated as bytes

For the file above: 529 bytes **certified** (every one of them covered by a
checksum or, for [0,16), by byte equality); 47 bytes **counted but
unconstrained**; 0 bytes in neither. For the D2 file of §5.4 the answer is
different and more interesting: 519 claimed, of which **96 are certified as
*placed* but covered by no checksum and inspected by nothing**.

### 4.4 A walk that does not complete

`[R-CNT-21]` is precise about two things I got wrong on my first pass, and I am
recording the corrections because they matter:

**(i) The total is a union, not a sum.** "Every byte the live state does not
claim is slack" is set-theoretic. My first implementation summed claim lengths,
and on an overlapping file it produced a *negative* slack total (−17 bytes on
A1, −202 on D1), which is nonsense and contradicts "an upper bound on the file's
true slack, never an under-count". Taking the union of the claimed intervals
fixes it. The document does not spell "union" out, but "every byte ... does not
claim" can only mean the union, and no other reading is available.

**(ii) A rejected layer's claimants are discarded.** "(a rejected layer's
claimants are not enumerated, whether or not the rejection impeded reading
them — and where the rejection is one the walk itself established, L18's overlap
or L40 through L42's placement among them, the claimants it had already
enumerated are discarded with the layer, since the total is a claim about a live
state one of whose layers is not usable)". So the general rule is *not
enumerated*; the added clause handles the case where you can only establish the
rejection **by** enumerating, and tells you to throw the enumeration away. Both
give the same answer.

Recomputed with both corrections:

| File | Violation | F | claimed (union) | slack | kind |
|---|---|---|---|---|---|
| A1 intra-layer overlap | L18 reject-layer | 512 | 189 | **323** | PARTIAL, stopped by layer `sst` (L18) |
| A3 misaligned tile | L40 reject-layer | 1472 | 189 | **1283** | PARTIAL, stopped by layer `sst` (L40) |
| A2 cross-layer overlap | F33 reject-file | 704 | 650 | 54 | exact |
| A6 bad padding | T4 reject-tile | 448 | 401 | 47 | exact |
| A7 structure in the gap | F7 reject-file | 4288 | 401 | 3887 | exact |

A6 is the case that taught me the rule's shape: T4 is a *content* violation, the
entry is well-formed, "its extent stands and it keeps its place in the *verifier*
rows, in run continuity, and in the coverage walk" — so a reject-tile at T4 does
**not** make the walk partial. §9.7 says the same from the other side: only a
*structural*-ground reject-tile is passed over, and "does not make the walk
incomplete".

Two edge questions I had to settle from the text:

- **Does a codec the verifier cannot execute make the walk partial?** No. The
  claimants are the entries' extents, which are enumerable from the index
  without decoding. §9.7's two partial triggers are "a scope-level rejection
  blocks enumeration" and "the verifier stops at the first violation"; an
  undecodable codec is neither. So: exact slack total, verdict *cannot
  establish*. My verifier does this.
- **Does a directory-CRC failure (F20) owe a slack total?** Yes, as partial.
  §5.2's only carve-out is "Where §6.2's ordered validation rejects the file
  before a live trailer is established there is no F and no live state to walk,
  so the total is not owed at all". A valid trailer with a corrupt directory
  *has* established a live trailer, so F exists; the walk enumerates the front
  block, the directory region and the trailer, and reports
  F − 16 − dir_length − 64 as partial, naming the directory CRC as the stopper.
  My first implementation just bailed; that was my bug, not the document's.

---

## 5. Extent overlap, alignment, and slab invariants, on adversarial layouts

I built ten files. Each is a real byte sequence my verifier read from disk.

### 5.1 Overlap

`[R-CNT-13]` splits overlap three ways, and I checked the split is exhaustive
over the structure kinds {front, trailer, directory, layer-owned (stored tile /
index region / sub-record extent), non-layer top-level record extent}:

- layer A ∩ layer A → reject-layer (L18)
- layer A ∩ layer B, or layer ∩ another scope's structure → reject-file (F33)
- non-layer ∩ non-layer → reject-file (F33)

That covers every pair. F33's row adds the useful note that a claimant reaching
[0,16) or [F−64, F) "is instead caught by the bounds rows F9/F10, F31/F32,
L16/L17 and T8/T9, each at its own tier" — which is why §9.7's `[16, F − 64)`
bound "already keeps every other claimant disjoint from them" and I did not need
a separate front/trailer overlap check.

**A1** — two stored tiles of one layer at [16,144) and [80,208):
L18, reject-layer, partial total 323. Verified.

**A2** — layer `a`'s tile at [16,144), layer `b`'s at [80,208):
F33, reject-file. Verified.

**D1, the one I built to be nasty** — two layer records with byte-identical
geometry whose extent slots point at *the same* index region. Every per-layer
cross-check passes: `entry_count` matches the geometry-derived count for both,
`extent_length` = 84 = the `[R-CNT-17]` formula for both, `crc_of_crc_array`
verifies for both, every segment CRC verifies for both. Nothing in §7.4, §15 or
§19.3 catches it. It is caught only by the coverage walk, twice over: the shared
index region is claimed by two layer records, and the single stored tile is
claimed by both layers' entry 0. Both are cross-layer → F33, reject-file. So
tile-sharing / index-sharing deduplication is barred, and barred *only* by
`[R-CNT-13]`'s "Extents are owned exactly once". Worth knowing: a writer that
tries to be clever about identical layers produces a file that no reader detects
and only a verifier rejects.

### 5.2 Alignment

`[R-SLB-01]`: "When declared: every stored tile's offset satisfies
offset mod A = 0. ... A verifier MUST check the invariant (violation:
reject-layer, §15.3); readers are not obligated to — offsets are always
explicit, so alignment is reader-invisible."

**A3** — A = 512, tiles at 512 (ok) and 1032 (1032 mod 512 = 8): L40,
reject-layer. Verified. The quantifier is over *stored* tiles, so sentinels are
silent, which matters because a sparse aligned layer would otherwise be
undecidable.

### 5.3 Slabs

`[R-SLB-02]` partitions the runs: interleaved → the single block [0, N); planar
→ each channel block [c·N, (c+1)·N), "runs never span channel blocks", run r
starts at block_start + r·S. `[R-SLB-03]` then requires, per run, packing in
ordinal order and A_slab alignment of the first stored tile.

**A4** — S = 2, A_slab = 64, tiles 0 and 1 stored at 64 and 200 (an 8-byte gap
after tile 0's 128 bytes): L41, reject-layer. Verified.

**A5** — the §16.2 example transposed: S = 2, A_slab = 64, tiles 0 and 3 stored,
tiles 1 and 2 sentinel. Run 0 = ordinals [0,2) holds only tile 0; run 1 =
[2,4) holds only tile 3. Each run has a single stored tile at a 64-aligned
offset. **Conforming.** This is "Sentinel tiles are transparent to run
continuity: they occupy no bytes and do not break packing", and I confirmed the
transparency also closes over §15.3's six structural rows — `[R-SLB-03]` says so
in terms — while an entry whose *only* defect is a failed stored-bytes CRC is
**not** transparent. That last clause is what keeps the invariant decidable
without fetching payloads: you never have to know whether a CRC failed, only
whether the entry is structurally sound, and both crc-passing and crc-failing
well-formed entries are treated identically for packing.

`[R-SLB-04]`'s stale-declaration rule has no row of its own, and §16.2's Note
explains why: "every file exhibiting one exhibits a run whose tiles are unpacked
or whose first stored tile is misaligned, which §21.3 registers." That is right —
I could not construct a stale declaration that produced no L41/L42 witness.

### 5.4 The degenerate file that answers the checksum question

**D2** — a conforming file carrying, beside its layer, a top-level record of
**experimental** type 0x8123 with MU = 0, PE = 0, and a 96-byte extent:

```
[     0,    16)   16   front block
[    16,   144)  128   stored tile 0 of layer 'a'
[   144,   240)   96   record extent, type 0x8123     <- NO CHECKSUM
[   240,   324)   84   tile-index region of 'a'
[   324,   455)  131   directory
[   455,   512)   57   pad                            <- SLACK
[   512,   576)   64   trailer
```

Verdict: **conforming**. Slack total: 57. Claimed: 519.

Those 96 bytes are live committed state — `[R-CNT-02]` names them ("a record
extent ... whatever the record's type"), so they are excluded from the slack
total and the certificate covers them. §8.1 gives them no checksum. §7.2 makes
their content opaque. `[R-WRT-05]` carries them forward unread; `[R-WRT-08]`
bars re-encoding them. Nothing in the verifier's report names them. This is
finding **verifier-02**.

**D3** — the same file with a *reserved*-range type 0x0123 instead: F36,
reject-file, verifier-detected. Note the asymmetry the register encodes — F36
fires "whatever its MU bit", while F35 is the narrower specialization for MU = 1.
§21.1 tells me a file exhibiting both is "recorded against the narrower row",
and names F35-of-F36 as one of exactly three specialization pairs.

**A10** — a layer with dimension extent 0: grid count 0, addressed-tile count 0,
extent slot (0,0), `crc_of_crc_array` 0, no index region, no claimants at all
from the layer. Conforming, 1 byte of slack. §21.6 records it as a defined
non-violation and `[R-GEO-02]` requires readers to accept it.

**Over-long pad files** — an empty directory at [16,20) with F = 512 and
F = 65536, so the pre-trailer gap runs to 428 and 65,452 bytes. Both
**conforming**: `[R-CNT-05]` says "a longer gap is conforming, and no conforming
commit produces one", and §2.3 declares this one of exactly two writer
obligations whose violation "this specification expressly declares not to be a
file-conformance violation". The slack totals (428 / 65,452) are what an
operator sees. This is the cheapest way to build a legal file that is almost
entirely waste, and the document handles it by counting rather than forbidding.

---

## 6. Decoded-content obligations

### 6.1 What the verifier must decode

§9.7 is unconditional and I want to quote it because it settled a design
question I would otherwise have got wrong: "A verifier decodes **every stored
tile**, whatever content obligations §14 places on the layer: §21.4's codec rows
are file-conformance violations, and a verifier MUST NOT certify past a
violation it has not looked for."

So a verifier decodes even a planar all-numeric layer with no padding positions
and no bool channels — a layer on which §14 places *no* content obligation —
because T24 (trailing bytes) and T25 (malformed stream) are still live.

### 6.2 What it compares against

Three obligations, and they partition cleanly:

| Where | Obligation | Row |
|---|---|---|
| every padding position, every layout | encodes each carried channel's recorded fill | T4 |
| packed planar bool, P mod 8 ≠ 0 | final-byte bits [P mod 8, 8) carry the fill bit | T5 |
| interleaved bool, **real** positions only | byte is 0x00 or 0x01 | T2 |

T2's row draws the boundary explicitly — "the same byte at a padding position is
T4's, the two rows together covering `[R-SER-08]`" — so no byte is covered
twice and none is missed. Planar bool *value* bits are unconstrained
(`[R-SER-03]`: "Every bit pattern of the value region decodes to a value
sequence"), and planar numeric values are unconstrained (`[R-TYP-05]`: "there is
no sample value a reader screens out").

I implemented the padding test by reconstructing tile coordinates from the disk
ordinal (§11.4: tᵢ from s by row-major division over the Gᵢ; c = k div N for
planar) and then walking in-tile ordinals, marking position u as padding iff
tᵢ·Tᵢ + uᵢ ≥ Eᵢ for some i.

**A6** — the edge tile of `sst` (ordinal 3, covering x = 96..127, so 4 real
positions and 28 padding ones) with one padding float32 zeroed instead of
fill-encoded: **T4, reject-tile**. Verified. The correct version of the same
tile, in generation 2 of my lifecycle trace, certifies.

**A8 / A9** — a planar layer, one bool channel `m` and one uint16 channel `v`,
single tile of P = 10 positions. `m`'s plane is ⌈10/8⌉ = 2 bytes; `v`'s is 20.
A8 has pad bits 2–7 of byte 1 clear (fill = false): **conforming**. A9 sets
bit 5: **T5, reject-tile**. Verified. This is §14.3's worked example structure,
and its stated results (`55 01` with fill false, `55 FD` with fill true)
reproduce exactly under my packing implementation.

### 6.3 What it is permitted to skip

Exactly two things, and neither is discretionary in the sense of being free:

- A decode declined on **resource** grounds (`[R-ERR-04]`) — verdict becomes
  *cannot establish*, and the declined requirement is named.
- A codec or filter it **cannot execute** (`[R-COD-11]`) — same. For a
  *conforming* verifier this can only arise "at a reserved or experimental
  value, every assigned codec and filter being core".

And one thing it must **not** treat as a skip: §21.7's undetectable content. A
mis-strided filter whose image happens to break no structural byte, an
undisclosed compression dictionary, or simply wrong sample data leave nothing
unchecked, so the verdict is unaffected. "Checksums are computed over what the
writer wrote."

I checked §21.7's witness account against `[R-COD-10]`'s own closing sentence
("where the resulting decoded image breaks a stated content obligation ... a
verifier detects it as a validity error at tile scope, and otherwise the
consequence is wrong sample content — undetectable by construction (§21.7)")
and against T26's row, and the three agree.

### 6.4 User-metadata documents

`[R-MTA-09]`, read as a whole passage rather than as a rule list, gives the
verifier this:

- Decode with a bound of its own choosing, no smaller than §21.9's 16 MiB.
  Applies **under either encoding**, and the passage forecloses the objection
  I was about to raise: "§21.9's row is stated over a document's decoded size,
  which a verbatim document has as surely as a compressed one."
- Under encoding 2, check eight frame constraints (magic; no skippable frame;
  no second frame; no nonzero dictionary ID; no content-checksum flag; no bytes
  after the frame; content-size, if present, equal to the decoded document's
  byte length — the last in both directions). I checked this list against
  `[R-COD-06]` clause by clause and it is complete: `[R-COD-06]` states eight
  things, of which two are excepted (window, decoded-size comparisons), two
  carry no witness (undisclosed dictionary use, the buffer-sizing bar), and the
  rest carry over. R4's sixteen instances are exactly those eight conditions ×
  two containers.
- Do **not** check the declared `Window_Size` against anything in the file —
  the bound is the verifier's own, no smaller than 8 MiB, and exceeding it is a
  decline, not a violation.
- On a decline: *cannot establish*, MUST NOT certify, MUST NOT report it as a
  finding of nonconformance, SHOULD report the bound applied and the stored
  extent length.
- Under an **unassigned** encoding: no decline, no unchecked requirement,
  certification unaffected, but a mandatory report line naming scope, encoding
  value and stored extent length.

I spent a while on "A **verifier** that declines to decode a document on **the
bound above**", because the passage introduces two bounds (the size bound and
the window bound) and "the bound above" was used earlier in the same paragraph
to mean the size bound specifically ("which is why the bound above is the
reader's own and not the file's"). §21.5's preamble asserts that both grounds
are a verifier's capability — "except where a reader or verifier declines the
decode on the size bound **or on the frame's declared window**". I concluded
this does not fork: §2.3's cannot-establish list says "or when it declines to
decode a user-metadata document (`[R-MTA-09]`)" without qualifying the ground,
so both declines land on *cannot establish* either way. Not a finding.

I also re-read §21.5's "except at an experimental-range encoding" three times,
because taken bare it would exempt a **failed extent CRC** (R2) at such an
encoding, and §7.1's `[R-CNT-25]` lists "a failed extent CRC" as one of the
"ways a user-metadata record's document can be unreadable". The same sentence
closes it — the exception is qualified "where **no document rule attaches**",
and an extent CRC is not a document rule — and `[R-MTA-10]` says so directly
("the extent's terminal CRC (`[R-CNT-20]`)" is among the structural checks that
still decide conformance), with §22.3 restating it. Three closures; not a
finding, but the reason I had to check three places is that the preamble's
exception is phrased as a *location* while its scope is a *rule class*.

---

## 7. Multi-generation trace

Layer `sst` throughout. Every generation was assembled byte by byte and then
handed to the verifier from disk.

### G1 — creation (`[R-LIF-02]` creation path, generation 1)

Front block, tile 0 at 16, tile 1 at 144, index at 272, directory at 356, pad,
trailer at 512. F = 576. **conforming**, slack **47**.

### G2 — append: store the edge tile (ordinal 3)

Writing begins at exactly F = 576 (`[R-LIF-02]` step 1). New payload at 576;
the layer's *whole* index region re-emitted at 704 (`[R-WRT-04]`: "Every layer
whose stored-tile set or index content this commit changes has its tile-index
region re-emitted in full ... necessarily at a new placement"); entries 0 and 1
byte-identical at their disk-ordinal positions; entry 2 still the sentinel;
entry 3 new. New directory at 788, pad, trailer at 960. F = 1024, generation 2,
same `file_id`.

Superseded to slack: the old index region (84), the old directory (109), the old
pad (47), the old trailer (64) = 304. Plus the new pad, 63. Slack **367**.
**conforming**.

The edge tile is where the padding obligation bites: x = 96..127 against E = 100
means positions 4..31 of that tile are padding and each must hold `00 00 C0 7F`.
My writer encodes them; A6 is the same tile with one of them wrong.

### G3 — update: supersede tile 0

New payload for tile 0 at 1024, whole index region again at 1152, directory at
1236, trailer at 1408. F = 1472, generation 3. The *old* tile 0 payload at
[16,144) drops out of the live state entirely and becomes slack.

Slack **815**. **conforming**. This matches §20.3's Note ("a commit's cost is
dominated by its index, not its data") and its worked example (a 32-tile layer's
index is 32·20 + 4 = 644 bytes; mine is 4·20 + 4 = 84).

### G4 — compaction (`[R-WRT-06]`, `[R-WRT-07]`)

Fresh `file_id` (0x0FEDCBA987654321, a new draw — "not merely a value compared
against the input's"), **generation 1**, and only the live state carried
forward. Tiles 0, 1 and 3 relocated to 16, 144 and 272; the index region
regenerated (entry offsets new; **entry lengths, entry crcs and sentinel entries
unchanged**; segment CRCs recomputed); `crc_of_crc_array` updated; the layer
record's extent slot re-pointed. F = 704.

Slack **47** — back to a single pad. I verified programmatically that all four
entry `crc` fields are byte-identical between G3 and G4, which is
`[R-WRT-07]`'s "every stored tile's bytes verbatim — each index entry's crc is
unchanged", and is also the property §23.2 warns makes a compacted file
"trivially correlatable with its input by content".

Slack trace across the four generations: **47 → 367 → 815 → 47**.
Certification result at each generation: **conforming, conforming, conforming,
conforming**.

One compaction rule I want to record because it is sharper than I expected:
"Regenerating a region means classifying every entry in it... An entry §15.3
classifies reject-tile on a structural ground is neither — `[R-IDX-03]` gives it
no stored extent for a re-pointing to target — so regenerating the region cannot
proceed without meeting it... `[R-WRT-06]` then obliges refusal: the compactor
can neither reproduce the entry nor invent a replacement, and no drop is
available, a tile-index entry being no record §20.4's table licenses dropping."
So a single malformed index entry makes a file permanently uncompactable — an
appender must carry it forward byte-identically (§20.3 step 2), and a compactor
must refuse. The document states this; I did not have to infer it.

---

## 8. Findings

### verifier-01 — AMBIGUITY

**`[R-CNT-27]`'s 128-byte floor has no stated position in §6.2's ordered
validation, and §21.2's preamble asserts one that §6.2's own enumeration does
not contain — so a verifier's verdict on a short foreign-major file is open.**

§21.2's preamble (normative under §2.1):

> "A file declaring a format major other than 1 is neither conforming nor
> nonconforming under this text (§2.3, `[R-CNF-02]`), and the rows below whose
> subject is that file's *geometry* do not reach it: §6.2 puts the version gate
> ahead of every check but the trailer magic and the trailer CRC, so such a file
> is refused on capability grounds first. Four rows are outside that reasoning
> and do reach it, because their subject is a field fixed across every major
> (`[R-CNT-24]`): F8 and F1's trailer-magic instance, F14's trailer CRC — the two
> checks §6.2 places before the gate — and F6 with F1's front-block instance,
> which `[R-CNT-04]` places before other processing."

§5.1's `[R-CNT-27]`:

> "No conforming file is shorter than 128 bytes: the front signature block, a
> directory of at least 4 bytes at an offset of at least 16, and the 64-byte
> trailer at a 64-aligned offset cannot be satisfied in fewer. A reader MUST
> treat a shorter file as a validity error at file scope."

§6.2's `[R-CNT-06]` enumerates its order exhaustively — "the trailer magic; the
trailer CRC; the version gate (§6.3) ... and then, those gates passed, MUST
validate all of the following before acting on the fields involved: the flag
gates (§6.3); committed_file_length equals the file size ...; dir_offset ≥ 16;
dir_length ≥ 4; dir_offset + dir_length ≤ F − 64; 1 ≤ generation ≤ 2⁶³ − 1;
file_id ≠ 0; reserved bytes zero" — and the 128-byte floor appears in neither
list. §19.1's four-step open does not contain it either, though F5's *Detected*
cell says `open` and §19's preamble notes that §19.1's enumerations are not
complete.

**The two readings.** (A) `[R-CNT-27]` is checked before the trailer is even
read — the obvious implementation, since you cannot read a 64-byte trailer from
a 40-byte file, and nothing orders it later. (B) §21.2's blanket claim that
"§6.2 puts the version gate ahead of every check but the trailer magic and the
trailer CRC" reaches `[R-CNT-27]` too, so F5 does not reach a foreign-major
file.

**I picked (B)**, because §21.2's preamble is normative, is directly on point,
and enumerates exactly four exceptions with F5 not among them — and because
`[R-CNT-27]`'s own justification is built from major-1 facts (`dir_offset ≥ 16`,
`dir_length ≥ 4`, and 64-alignment of F are all §6.2 gates, none of them fixed
across majors by `[R-CNT-24]`), so the floor is a major-1 number and should not
judge a file of another major.

**What an implementer does wrong without it.** I built the witness: a 96-byte
file whose front block at [0,16) is correct, whose trailer sits at [32,96) with
a correct magic and a correct CRC, and whose `version_major` is 7. None of
F1, F6, F8 or F14 fires. Under (A) the verifier reports **nonconforming** (F5);
under (B) it reports **cannot establish** and makes no finding about the bytes.
§2.3 makes those two verdicts different assertions — "*Cannot establish* is not a
finding that the file is nonconforming" — and §6.3 asks that the diagnostic for
an unimplemented major be "distinct from both 'not a TARN file' and 'corrupt'",
which is exactly what reading (A) collapses.

**Byte-level: no.** Both paths reject the file, and `[R-CNT-07]` obliges
reject-file for an unimplemented major on either reading, so no reader's
accept/reject changes and no writer's emittable set changes. What differs is
the verifier's verdict token and the class of diagnostic a user sees. The fix is
one clause: either add `[R-CNT-27]` to §6.2's post-gate list, or say in §5.1
that the floor is checked after the version gate.

### verifier-02 — OBSERVATION

**A certificate covers the extent of an unassigned-type record without
inspecting it and without naming it, while the document states the opposite
principle for the structurally identical metadata case.**

§8.1's coverage map, last row:

> "| Extent of a record of a type this specification has not assigned | none —
> the bytes are opaque (§7.2) | — |"

§22.3's `[R-SEC-04]`, on the same bytes:

> "The extent of a record of a type this specification has not assigned is
> covered by no checksum either (§8.1), so corruption inside it is equally
> invisible: §20.4's byte-identical re-emission (`[R-WRT-05]`) carries such an
> extent forward unread, and `[R-WRT-08]` bars re-encoding it, so nothing an
> updater does would surface the damage."

And, for the parallel case, `[R-MTA-10]`:

> "and it MUST report each record it ignored on this ground, naming the owning
> scope, the encoding value, and the stored extent length, as it reports the
> slack total (`[R-CNT-21]`): bytes a certificate covers without inspecting are
> counted and named, never silent."

`[R-SEC-04]` names four residues; the verifier's report reaches three of them.
Slack is counted and totalled (`[R-CNT-21]`). A user-metadata extent under an
unassigned encoding is counted *and named*, on the stated principle above, and
§22.3 spells out the operational point: "an operator who wants no such bytes
rejects on that report line, a policy above conformance." A trailer-mimic in
slack is inert. The fourth — an unassigned-type record's extent — is counted
(it is a `[R-CNT-02]` claimant, so it is excluded from the slack total and the
certificate covers it) but named nowhere, and it is the *weaker* of the two
uninspected cases: the metadata extent at least carries a terminal CRC, and this
one carries no checksum at all.

**Why this is an observation and not an ambiguity.** The text decides it: no
rule obliges the report, `[R-MTA-10]`'s duty is scoped to its own subject, and
§2.3's per-requirement report is for *requirements it was unable to check* —
here there is no requirement to check, exactly as `[R-MTA-10]` says of its own
case. So a verifier that says nothing is conforming. What I am flagging is that
the principle the document articulates ("bytes a certificate covers without
inspecting are counted and named, never silent") is applied to one of two
structurally identical populations, and that a verifier implementer working from
this text alone will produce a report that is silent about the larger hole. I
found it by building the file rather than by reading: my D2 fixture is a
576-byte **conforming** file in which 96 live-state bytes are covered by no
checksum, inspected by nothing, and mentioned in no report line — and the
certificate says so about none of it.

**Byte-level: no.** It changes no byte a writer may emit and no accept/reject
verdict. It changes what a certificate discloses. A triager may reasonably class
it as a deliberate design position rather than a defect; I report it because my
charter is the verifier's report and this is the one place the report contract
has a hole I could not close from the text.

---

## 9. Things I checked and found clean

Recording these so the absence of a finding is legible as work rather than as
silence.

- **§21.8's stated totals.** "Every row of §21.2 through §21.5 — 121 conditions
  over 277 instances". I counted mechanically under §21.1's own rule
  ("Instances within a cell are separated by semicolons, and a cell reading — is
  one instance; the count is therefore mechanical once the cell is written"):
  F 36 rows / 58 instances, L 49 / 116, T 26 / 55, R 10 / 48. **121 rows, 277
  instances.** The per-section counts in each subsection heading (36, 49, 26, 10)
  are also right.
- **Every worked numeric example.** 55 assertions across §7.4, §11.2, §11.4,
  §12.1, §12.3, §14.2, §14.3, §14.5, §15.4, §17.3, §20.3, Appendix A and
  Appendix B. All reproduce, including the §17.3 shuffle
  (`0000803f0000004000004040` → `0000000000008000403f4040`, inverse restores),
  §15.4's 1,000,000-entry layout (16 segments, last covering 16,960 entries,
  region 20,000,064 bytes, tile 999,999 at segment-relative byte 339,180,
  segment 15 at [19,660,800, 20,000,000)), and §14.3's `55 01` / `55 FD`.
- **Field inventory for "one quantity, two in play".** I enumerated every field
  of the trailer, the record header, the layer inline payload, dimension and
  channel entries, the index entry, the directory region and the user-metadata
  record, and looked for one governed by nothing. Every one is governed. The
  cases I checked hardest: `S` (bounded only by the u64 domain, which is
  correct — S = 0 means "not declared" and L28 catches the A_slab pairing);
  `A_slab` (L28 for S = 0, L29 for the value set, together exhaustive over
  S = 0 / S ≠ 0); `inline_length` (u32, so inside `[R-ENC-03]`'s domain by
  construction, and overrun is F29/L14); `version_minor` (descriptive, "any").
- **`[R-CNT-13]`'s three overlap cases** are exhaustive over the five structure
  kinds — I enumerated the pairs.
- **§15.3's six *structural* rows** — I counted them and confirmed the seventh
  (crc failure) is deliberately outside, which is what `[R-SLB-03]`, `[R-LIF-08]`
  and `[R-WRT-06]` all lean on.
- **§21.7's witness account.** §20.3 step 4's bar names four effects (padding
  set and content, decoded size, sample byte offsets, codec and filter). §21.7
  gives witnesses for two of them by other means (decoded size → T3/T14;
  codec → T15/T17/T23/T25/T14) and folds the other two into its opening clause
  ("witnessed only where ... the change reaches a byte §14 structurally
  constrains"). I tried to build a counterexample — an interleaved channel
  reorder that preserves decoded size, codec and filter — and it is witnessed by
  T4 exactly when the two channels' fills differ and unwitnessed otherwise,
  which is what §21.7 claims.
- **§21.9's per-instance paragraph.** 5 declaration rows + 3 per-instance rows
  = the 8 rows in the table. The tile row's quantifier ("a layer's **addressed**
  tiles, stored or not") matches `[R-COD-07]`'s cap, and the two are cited as
  parallel; I checked both governing verbs and they do range over the same set.
  The `Window_Size` row's range ("compressed frames a file actually contains")
  covers both tile frames and metadata frames, which is what `[R-MTA-09]` relies
  on when it says "§21.9's user-metadata row bounds a document's decoded size;
  it does not relieve the frame carrying it of the `Window_Size` row."
- **No addressed tile can be entirely padding.** G_i = ⌈E_i/T_i⌉ implies
  (G_i − 1)·T_i < E_i, so the last tile along every axis has at least one real
  position — which is why §14.5's obligation never degenerates.
- **A conforming reader must accept an arbitrarily large *stored* tile.** No
  §21.9 row bounds a stored length, so `[R-CNF-03]`'s acceptance duty runs to it.
  I decided this is deliberate rather than a gap: `[R-SEC-02]`'s defense is over
  *decoded* size, the stored length is bounded by F (you must physically hand
  the reader the bytes), and a streaming decoder never buffers it.
- **§21.5's "except at an experimental-range encoding"** — settled against R2,
  as recorded in §6.4 above.
- **§18.2's "the bound above"** — settled by §2.3's unqualified decline clause,
  as recorded in §6.4 above.

---

## 10. Confidence

**High** that the document determines the verifier I built. Every question my
charter names has an answer in the text, and where I first thought otherwise
(the slack total on an incomplete walk; whether a T4 tile makes a walk partial;
whether a verifier decodes a layer with no content obligation; whether a
foreign-major file gets a verdict at all) the answer turned out to be stated,
usually in a sentence I had read past. The two places I could not close from the
text are above, and neither forks a byte.

The one thing I would tell the next implementer: build the coverage walk as a
*union over intervals*, not a sum of lengths, and discard a rejected layer's
claims before totalling. Both follow from §5.2, but §5.2 states them in prose
whose arithmetic only becomes obvious when you run it on an overlapping file and
get a negative number back.

**Transcript finding count: 2.**
