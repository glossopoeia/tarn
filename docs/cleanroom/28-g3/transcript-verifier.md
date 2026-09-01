# Round 28 — Verifier implementer — working transcript

## 0. Disclosure, up front

I read exactly one file from the repository: `/Users/robertkleffner/Documents/GitHub/tarn-first-draft/spec/tarn.md`.
I opened no ADR, no `docs/`, no `conformance/`, no `PLAN.md`, no `AGENTS.md`, no
`registry.json`, and I ran no `git` command. I did not list the repository or the
output directory. Everything below that is not the specification's own text is
either arithmetic I ran locally or reasoning I did myself.

Two things arrived in my context that were not the specification and that I have
not used as evidence:

1. A project-instruction preamble (`CLAUDE.md` pointing at `AGENTS.md`) and a
   `gitStatus` block listing recent commit subject lines. The commit subjects name
   round numbers, ADR numbers, and — in one case — a phrase describing a change to
   the format and a struck row label. **I did not open any of those files, and I
   have not treated any of that text as telling me what is true of the
   specification.** It did tell me a change existed before I read the document; the
   round brief told me the same thing in more detail, so nothing in my walk turns
   on it. I flag it because an undisclosed contamination poisons the round.
2. A tooling notice about scratch directories.

**One more disclosure, and it is a real one.** My first scratch script was written
to the session scratchpad root as `crc.py`. On my second command, `exec`-ing that
same path produced output with labels I had never written — a *different* script's
output ("trailer len 60", "4-sentinel-entry 80B crc") — and then a `TypeError`,
because the file on disk was no longer mine. Another agent in this round is using
the same scratchpad root and overwrote my file between my two calls. I did not read
that file's contents deliberately, but its *stdout* was printed into my context: it
showed a trailer CRC of `0x402f157e`, a 4-sentinel CRC of `0x80a34955`, a
`crc_of_crc_array` of `0xc4ee982e`, and a full-segment constant of `0xeecb3bb2`.
Those are values I had already computed myself in the immediately preceding call
(and recomputed afterwards in an isolated directory,
`.../scratchpad/verifier-lane-priv/`), so no conclusion of mine rests on another
lane's output — but I saw four numbers from another lane's arithmetic, and I am
saying so. Everything after that call was run from my own private directory with
uniquely named files.

Paths: the spec was exactly where the brief said it was. Nothing was misplaced.

---

## 1. How I worked

I read the document straight through, front to back, in ten chunks, then went back
over the passages my charter touches (§2.3, §2.4, §4.5, §5.1, §5.2, §6.2, §7.1,
§7.2, §7.4, §8, §9.6, §9.7, §14.5, §15.1–§15.4, §16, §17.4, §18.2, §19.2, §20.5,
§21 entire, §22.3, Appendices A, B, G, H) at least twice.

I then ran mechanical sweeps over the file (grep/rg and small Python scripts that
parse the register tables), and I recomputed every CRC-32C constant the document
states, plus every worked byte layout I could reconstruct from declarations alone.

I built a conforming file of my own on paper and walked it through four
generations — create, append, update-with-metadata, compact — doing the coverage
arithmetic at each step, and then broke it deliberately to exercise the
incomplete-walk path, the overlap rules, and the slab and alignment invariants.

---

## 2. The verifier, as I would build it

### 2.1 Verdict vocabulary and the gate on each

§2.3's `[R-CNF-11]` gives three verdicts and a strict priority. Written as an
algorithm:

```
V := set of violations established        (initially empty)
U := set of requirements unable to be checked, each with its ground
X := set of scopes not examined            (only populated if we stop early)

run the ordered procedure below
if V ≠ ∅          -> report NONCONFORMING          (whatever |U| is)
elif U ≠ ∅        -> report CANNOT ESTABLISH       (and MUST NOT certify)
else              -> report CONFORMING             (certify)
always            -> report every element of U, naming requirement and ground
always            -> report every element of X as "unexamined"
```

The priority is express: *"An established violation takes priority: a verifier that
has established any violation reports* nonconforming*, however many requirements it
was unable to check, and* cannot establish *is available only to a traversal that
established no violation."* And *"a verifier MUST NOT certify a file it reports
that way"* — so *cannot establish* is a non-certification, not a soft pass.

`U` is populated only *"on a capability or resource ground"*. §2.3 gives five
illustrative grounds ("as when …", so the list is open): a foreign format major;
an MU = 1 record of a type it does not implement; inability to execute a codec or
filter (`[R-COD-11]`); declining a layer's or a tile's decode on resource grounds
(`[R-ERR-04]`); declining to decode a user-metadata document (`[R-MTA-09]`).

Two things are expressly *not* grounds:

- A user-metadata record under an encoding this specification does not assign.
  `[R-MTA-10]`: *"A verifier meeting such a record in an otherwise conforming file
  has no requirement it is unable to check … and certification is unaffected"* —
  but it MUST report the record, naming owning scope, encoding value, and stored
  extent length. Note the trap: this withdraws only the *document's content rules*.
  Encoding 0 and the reserved range 3–0x7F are unassigned too and are violations
  (R1), so those go to `V`, not to the report line. §21.5's preamble says this in
  terms.
- Anything in §21.7's "what no check detects": *"None of these is a requirement a
  verifier is* unable to check *within the meaning of `[R-CNF-11]`: no file-level
  witness exists to check, so nothing about the file is left undetermined and the
  verdict is unaffected."*

And a SHOULD deviation is neither a violation nor an unchecked requirement:
`[R-CNF-12]` makes it *"an advisory that does not bar certification"*, and *"A
verifier owes no search for one"*.

`X` — *unexamined* — is available only after a stop-at-first-violation, so a report
carrying `X` always carries verdict NONCONFORMING. That is worth noticing, because
it means *unexamined* never coexists with a certificate.

### 2.2 The ordered procedure

Tier 0 — **trailer**, in `[R-CNT-06]`'s fixed order, on the final 64 physical
bytes:

1. magic at F−64 (F8)
2. CRC-32C at F−4 over [F−64, F−4) (F14)
3. version gate: `version_major` ≠ 0 (F18) and implemented (else `U`, ground:
   capability, §6.3)
4. then, unordered: flag gates (F19); `committed_file_length` = transport size
   (F17) and ≡ 0 mod 64 (F13); `dir_offset` ≥ 16 (F9); `dir_length` ≥ 4 (F16);
   `dir_offset + dir_length` ≤ F − 64 (F10); `file_id` ≠ 0 (F12); reserved [48,60)
   all zero (F15).

I counted `[R-CNT-06]`'s register rows mechanically: **exactly nine** —
F8, F9, F10, F12, F13, F14, F15, F16, F17. That is the number `[R-CNF-13]` asserts
(*"`[R-CNT-06]` states nine, of which the trailer magic and the trailer CRC assert
invariants `[R-CNT-24]` fixes and the other seven do not"*), and 9 − 2 = 7. Both
halves check out. F11 is struck; §21.2's Note says so and the table's row count
(35) is F1…F36 minus one.

A verifier holds no residency exemption on the front block: F6's own cell says
*"a verifier holds no such exemption (§2.3)"*, and §2.3's verifier bullet — *"A
reader that additionally checks every file-level requirement — including those
ordinary readers are exempted from"* — is what makes that true. So the front block
is a Tier-0 check for me, not an optional one.

Tier 1 — **directory**: CRC over `dir_length − 4` bytes (F20), then the record
walk (F24, F29, F30–F32, F34, F35, and the verifier-only F25, F26, F28, F36),
then the layer-name namespace (F4, L3, L5, L6).

Tier 2 — **per layer**: §19.3's full validation (L1, L2, L4, L7–L17, L19–L24,
L26–L36, L39, L43, L44, L45, plus verifier-only L46, L47, L49).

Tier 3 — **index chain per layer**: `crc_of_crc_array` (L37), every segment CRC
(L38), and every entry classified under §15.3 (T6–T12).

Tier 4 — **per stored tile**: entry crc (T1), decode (T13, T15–T25), decoded size
(T3, T14), and the content rows a verifier owns (T2, T4, T5, T26).

Tier 5 — **coverage walk** (§9.7): disjointness (F33, L18), bounds, checksum
coverage, the pre-trailer gap (F7), the alignment/slab invariants (L40, L41, L42),
and the slack total.

Tier 6 — **extents**: user-metadata documents (R1–R10), and the `[R-MTA-10]`
report line for unassigned encodings.

I cross-checked that partition mechanically. Every register row's Detector/Detected
pair is one of: reader × {open, layer access, tile use, extent use} or verifier ×
certification. There is no verifier row detected at a reader tier and no reader row
detected at certification. 20 rows carry Detector = verifier: F7, F25, F26, F27,
F28, F33, F36; L18, L25, L40, L41, L42, L46, L47, L48, L49; T2, T4, T5, T26.
Appendix H's verifier checklist names all twenty (T26 by way of "the check that
detects it is T2's or T4's"), so the checklist and the register agree.

### 2.3 What a verifier must decode

§9.7 is unambiguous and stronger than §17.4's framing: *"A verifier decodes every
stored tile, whatever content obligations §14 places on the layer: §21.4's codec
rows are file-conformance violations, and a verifier MUST NOT certify past a
violation it has not looked for."* So the trigger is not "does this layer have
padding positions or bool channels" — it is "is this tile stored in the live
generation".

It compares the decode against: the decoded size derived from declarations alone
(§14.2/§14.3, `[R-SER-07]`); codec-1's length equality (`[R-COD-04]`); exact
consumption of the stored extent (`[R-COD-08]`); the zstd header constraints
(`[R-COD-06]`); `[R-SER-05]`'s fill at every padding position and every pad bit;
and `[R-SER-08]`'s 0x00/0x01 on every interleaved bool byte at a real position.

It is permitted to skip: nothing, on capability grounds, if it is a conforming
verifier (every assigned codec and filter is core, `[R-CNF-03]`); a tile's or a
layer's decode on **resource** grounds (`[R-ERR-04]`), which moves the file to
`U`; and a user-metadata document decode on its own size bound or the frame's
declared window (`[R-MTA-09]`), which likewise moves it to `U`. It skips a
user-metadata document under an unassigned encoding without cost (`[R-MTA-10]`).

Worth writing down because I had to re-read it three times: §17.4's *"A verifier
that cannot execute a layer's codec or filter cannot establish that layer's
conformance"* names a state a **conforming** verifier can never be in. Every
assigned codec and filter is core (`[R-CNF-03]`); a non-assigned value is itself a
violation at layer scope (L43/L45); and a resource inability is a different ground
(`[R-ERR-04]`), listed separately in §2.3. §17.4 says as much for readers in its
own next sentence. It is surplus, not a defect, and I am not reporting it.

---

## 3. The coverage walk, worked

### 3.1 The partition, restated

`[R-CNT-02]`: every byte of the live committed state belongs to exactly one of the
front signature block; or a **structure** — a stored-tile extent, a record extent,
the directory, or the trailer. §9.7 names the walk's claimants: the directory
itself; each record's extent (reached through the directory's records *and their
sub-records*); the stored extent of each non-sentinel tile-index entry; plus the
front block at [0, 16) and the live trailer at [F − 64, F).

Two traps the document closes explicitly, and I checked both:

- A record is not a claimant of its own header/payload — those lie inside the
  directory region, *"so reaching a record through the directory is traversal, not
  a second claim on those bytes."*
- A layer's tile-index region is not a second claimant beside the layer record's
  extent — *"the region enters the walk once, as that record's extent."* If it
  were double-claimed, every file with a layer would fail disjointness.

**Can a byte be neither certified nor slack?** No. §5.2's Note settles it: the live
committed state is *defined* as the front block plus what a complete walk reaches,
and `[R-LIF-08]` makes every byte the walk misses slack, *"so 'belongs to no class'
describes nothing, and a register row for it would be a row no file could
exhibit."* Bytes at or beyond F cannot exist in a conforming file (F17). So the
only testable half of `[R-CNT-02]` is disjointness, which is what F33 and L18
register.

**Certified vs counted-but-unconstrained.** Certified: front block (equality),
trailer, directory, each layer's index region (via `crc_of_crc_array` + segment
CRCs), each stored tile (via its entry crc), each user-metadata extent (terminal
CRC). Counted but not certified: (a) slack — claimed by nothing, covered by no
checksum, content unconstrained; (b) the extent of a record of a type this
specification has not assigned — a *claimant*, inside the partition, disjointness-
checked and bounds-checked, but covered by **no** checksum (§8.1's last row) and
constrained by no content rule; (c) the *content* of a user-metadata document under
an unassigned encoding — its extent is CRC-covered, so corruption is detected, but
no content rule attaches (`[R-MTA-10]`), which is why the verifier must name each
such record in its report. §22.3's "four residues" paragraph is the security
statement of exactly this, and it matches.

So: every live *structure* is covered by a checksum **except** the front block
(equality-checked) and the extent of a record of an unassigned type. §4.5 and
`[R-CNT-19]` both say so, and §8.1's seven-row map is the enumeration. I checked
the terminal/interior split: terminal (comparison-verified, covered by nothing
further) = the trailer CRC field, the directory-region CRC, the user-metadata
extent CRC. Interior (comparison-verified *and* covered by exactly one further
checksum) = each segment CRC array (→ `crc_of_crc_array`), each entry's crc field
(→ its segment CRC), each `crc_of_crc_array` (→ the directory CRC). The chain
`[R-CNT-20]` states — trailer → directory → `crc_of_crc_array` → segment CRC array
→ index segment → index entry → stored tile — closes over all of it.

### 3.2 A concrete file, four generations

I built this by hand from declarations only.

Layer `a`: rank 1; dimension `x`, extent 4, tile extent 2; interleaved; one
channel `v`, uint8, fill 0x00; codec 1, filter 1; no alignment, no slab.
G = ⌈4/2⌉ = 2, N = 2, P = 2, Q = 1, decoded size per tile = P·Q = 2 bytes.
Addressed-tile count = N = 2, so `entry_count` = 2.
Index region length by `[R-CNT-17]`: 2 × 20 + ⌈2/2¹⁶⌉ × 4 = 40 + 4 = **44**.

Layer-record inline payload, summed the way §7.4's own worked example sums:
name 1+1 = 2; the nine scalars layout…C = 1+2+2+2+8+8+8+1+2 = 34; one dimension
entry 1+1+8+8 = 18; one channel entry 1+1+2+1+1 = 6; trailing fixed 1+8+4 = 13.
2 + 34 + 18 + 6 + 13 = **73**. Record = 24 + 73 = **97**. Directory = 97 + 4 = **101**.

**Generation 1 (creation).**

```
[0,16)    front block
[16,18)   tile 0 payload   (2 bytes)
[18,20)   tile 1 payload   (2 bytes)
[20,64)   tile-index region (44 bytes) — the layer record's extent
[64,165)  directory (101 bytes)
[165,192) pre-trailer pad  (27 bytes)
[192,256) trailer          F = 256
```
`dir_offset + dir_length = 165 ≤ F − 64 = 192` ✓. F ≡ 0 mod 64 ✓.

Walk: 16 + 4 + 44 + 101 + 64 = **229** claimed. Slack = 256 − 229 = **27**,
which is exactly [165, 192). Verdict: CONFORMING, slack total 27, U empty.

**Generation 2 (append: supersede tile 0).**

```
[256,258) tile 0' ;  [258,302) index'  ;  [302,403) dir₂ ; [403,448) pad ; [448,512) trail₂
```
Claimed: 16 (front) + 2 (tile 0') + 2 (tile 1, unmoved) + 44 + 101 + 64 = **229**.
Slack = 512 − 229 = **283**. Decomposed: old tile 0 (2) + old index (44) + dir₁
(101) + pad₁ (27) + trail₁ (64) + pad₂ (45) = 283 ✓. The two figures agree, which
is the check that the "F less claimed" formula and the "sum the unreached runs"
formula are the same number.

**Generation 3 (update: add a file-scope user-metadata record).**
Document `{"tarn.title":"a"}` = 18 bytes, encoding 1; extent = 18 + 4 = 22 ≥ 5 ✓.
Directory now 97 + 25 + 4 = 126.

```
[512,534) umd extent ; [534,660) dir₃ ; [660,704) pad ; [704,768) trail₃   F = 768
```
Claimed: 16 + 2 + 2 + 44 + 22 + 126 + 64 = **276**. Slack = 768 − 276 = **492**.

**Generation 4 (compaction, fresh `file_id`).** Placement is free
(`[R-SLB-05]`); entry lengths, entry crcs and sentinels are unchanged, offsets are
new, segment CRCs and `crc_of_crc_array` are recomputed (`[R-WRT-07]`).

```
[0,16) front ; [16,18) t0 ; [18,20) t1 ; [20,64) index′ ; [64,86) umd ;
[86,212) dir ; [212,256) pad ; [256,320) trailer      F = 320
```
Claimed: 16 + 2 + 2 + 44 + 22 + 126 + 64 = **276**. Slack = 320 − 276 = **44**.
492 → 44 is what compaction reclaimed. Verdict at every generation: CONFORMING.

Sanity check against the document's own smallest file: zero records, directory
[16,20), pad [20,64), trailer [64,128), F = 128. Claimed = 16 + 4 + 64 = 84,
slack = 44 — exactly Appendix A's *"pre-trailer pad, 44 bytes"*. And a
touch-nothing second commit on it: claimed 84, F = 256, slack = 172 =
[16,128) (112: old dir 4 + old pad 44 + old trailer 64) + [132,192) (60). ✓

### 3.3 A walk that does not complete

Same generation-3 file, with tile 1's extent moved to overlap the layer's own index
region. That is L18 (verifier, reject-layer). `[R-CNT-21]`: the layer's claimants
*"are discarded with the layer, since the total is a claim about a live state one
of whose layers is not usable."*

Partial total = F − (front 16 + umd 22 + dir 126 + trailer 64) = 768 − 228 = **540**.
540 > 492, so it is an upper bound, as required. The verifier reports:
NONCONFORMING (L18 established), partial slack total 540, naming L18/layer `a` as
what stopped the walk. If instead it had elected to stop at the first violation, it
would additionally report every unexamined scope.

I checked the upper-bound claim for soundness: *"A partial total is F less the
bytes claimed by the claimants the walk did enumerate."* Read as a set difference
(F minus the *union* of enumerated claimants' ranges), it is monotone — fewer
claimants, larger residue — so it is always ≥ the true slack. Read as a *sum* of
lengths it could under-count when two enumerated claimants overlap; but overlap is
precisely what triggers discarding, and the natural reading is the set one, so I
took the set reading and I do not think the sum reading is defensible.

### 3.4 Overlap, alignment, slab — on adversarial layouts

**Overlap.** `[R-CNT-13]` partitions the cases exactly: intra-layer → reject-layer
(L18); across layers, or a layer structure against another scope's, or two
non-layer structures → reject-file (F33). Every pair of live structures falls in
exactly one bucket ("same layer or not"), so the partition is complete. F33's cell
routes claimants that reach the front block or the live trailer away to the bounds
rows instead — F9/F10 for the directory, F30/F31/F32 and L15/L16/L17 for record
extents, T8/T9 for stored-tile extents — and it notices the case I would have got
wrong: a slot of (0, N) with N ≠ 0 reaches the front block through a *zero* offset,
which F31/L16 (offsets 1–15) do not catch, so it is F30/L15's. I checked: offset 0
is not in 1–15, so without that sentence there would be a hole.

**Alignment.** Layer declares A = 512. Stored tiles at 512, 1024, 1536: clean. One
at 520: L40 (verifier, reject-layer). Degenerate cases: a layer with A declared and
no stored tile satisfies the invariant vacuously (*"every stored tile's offset"*);
a layer with A declared whose only tile sits at 16 fails, which is why Appendix G
item 3 says the first structure goes *"at the least position above it the
declaration admits."*

**Slabs.** Planar, C = 2, N = 3, S = 2, A_slab = 4096. `[R-SLB-02]` partitions each
channel block independently: block 0 = [0,3), block 1 = [3,6); runs start at
block_start + r·S, so runs are [0,2), [2,3), [3,5), [5,6) — four runs, two of them
short finals. A clean layout: t0@4096 len 100, t1@4196 (packed); t2@8192; t3@12288
len 100, t4@12388; t5@16384. Adversarial variants I checked against the rows:

- t4@12389 → gap → L41.
- t3@12290 → first stored tile of run [3,5) not 4096-aligned → L42.
- t2@4296 (contiguous with t1 but not aligned) → L42, because runs are *"not
  mutually ordered or joined"* — cross-run contiguity buys nothing.
- t1's entry given `length = 0` (T10, a *structural* ground) → transparent to run
  continuity, so run [0,2) has one stored tile and no L41 fires; the file is still
  nonconforming on T10.
- t1's entry given `offset = 8` (T8, structural) → also transparent, and it
  contributes no extent to the walk. This is the case that produced finding
  **verifier-01** below.
- t1's entry left well-formed but its stored bytes made to fail their crc → *not*
  transparent; §16.2 says so in terms, and its offset/length still participate in
  packing. So T1 alone does not perturb L41's arithmetic.

An overlap inside a run fires both L41 (overlap instance) and L18. §21.1's
strict-specialization rule covers this — every file exhibiting L41's overlap
instance exhibits L18 — and the list of such pairs is expressly *"not offered as
closed"*, so this is fine.

---

## 4. Checksum constants — what I reproduced

I implemented CRC-32C from the parameters `[R-ENC-09]` states (Castagnoli
0x1EDC6F41, reflected in/out — reflected table constant 0x82F63B78 — init
0xFFFFFFFF, final XOR 0xFFFFFFFF, stored little-endian) and reproduced:

| Constant | Document | Computed | Where |
|---|---|---|---|
| CRC-32C("123456789") | 0xE3069283 | 0xE3069283 | §4.5, App. B |
| CRC-32C(zero bytes) | 0x00000000 | 0x00000000 | §4.5, §7.1, App. A |
| 4 sentinel entries, 80 bytes | 0x80A34955 (`55 49 A3 80`) | 0x80A34955 | §7.4 example |
| `crc_of_crc_array` over `55 49 A3 80` | 0xC4EE982E (`2E 98 EE C4`) | 0xC4EE982E | §7.4 example |
| full all-sentinel segment (2¹⁶ × 20 B) | 0xEECB3BB2 | 0xEECB3BB2 | §15.4, App. B |
| Appendix A trailer CRC over [0,60) | 0x402F157E (`7E 15 2F 40`) | 0x402F157E | App. A |

**Every stated CRC constant reproduced. None was beyond local computation.**

Appendix A byte-for-byte, decoded from the hex dump and checked field by field
against §6.2's layout **as it now reads** (this is the annotation table the brief
flagged): file length 128 ✓; front magic ✓; front reserved [8,16) zero ✓;
directory [16,20) = `00 00 00 00` = CRC of zero bytes ✓; pad [20,64) 44 bytes ✓;
trailer magic at 64 ✓; `version_major` = 1 at trailer offset 8 = file [72,74) ✓;
`version_minor` = 0 at 10 = [74,76) ✓; `flags` = 0 at 12 = [76,80) ✓;
`dir_offset` = 16 at 16 = [80,88) ✓; `dir_length` = 4 at 24 = [88,96) ✓;
`committed_file_length` = 128 at **32** = [96,104) ✓; `file_id` =
0x0123456789ABCDEF at **40** = [104,112) ✓; reserved **12 bytes** at **48** =
[112,124) all zero ✓; CRC at 60 = [124,128) ✓. Every offset in the annotation
table is consistent with the post-change layout; nothing is stale. Sums:
16 + 4 + 44 + 64 = 128 ✓. The prose's *"112 bytes covering [16, 128)"* is
128 − 16 = 112 ✓.

Other worked examples I reproduced or re-derived by hand:

- §7.4's layer record: 81-byte payload, field-by-field offsets 0/4/5/7/9/11/19/27/
  35/36/38/40/48/56/63/68/69/77 all correct; `sst` = `73 73 74`; `x` = `78`;
  `temp` = `74 65 6D 70`; type 12 = `0C 00`; fill `00 00 C0 7F` = 0x7FC00000;
  4 + 34 + 18 + 12 + 13 = 81 ✓; extent length 4×20 + ⌈4/2¹⁶⌉×4 = 84 ✓;
  ⌈100/32⌉ = 4 ✓.
- §11.2 / §11.4: G = (4,8), N = 32, P = 65,536; (300,700) → tile (1,2), s = 10,
  in-tile (44,188), ordinal 44·256 + 188 = 11,452; planar c = 2 → 2·32 + 10 = 74 ✓.
- §15.4: 1,000,000 entries → 16 segments (15 full + 16,960), 64-byte array, region
  20,000,064; segment 15 at [19,660,800, 20,000,000) = 339,200 B ≈ 339 KB; full
  segment 1,310,720 B = 1.25 MiB ✓. Disk ordinal 74 → entry bytes [1480,1500) ✓;
  channel 3 unstored → entries 96–127 ✓.
- §14.2: (2,3), P = 6, uint8+uint16 → Q = 3, size 18, ordinal 5 at [15,18);
  planar `b` 12 bytes, ordinal 5 at 10–11; float32+bool → Q = 5, size 30, ordinal 5
  at [25,30) ✓.
- §14.3: P = 10 alternating → `55 01` with fill false, `55 FD` with fill true —
  computed both ✓.
- §14.5: (5,5) tiles (4,4) → grid 2×2, edge tile (1,1) has 1 real + 15 padding
  positions, uint16 fill 0xABCD → 32-byte tile, values 1–15 each `CD AB` ✓.
- §17.3 byte-shuffle: 1.0/2.0/3.0 float32 → `00 00 80 3F 00 00 00 40 00 00 40 40`,
  shuffled `00 00 00 00 00 00 80 00 40 3F 40 40` — computed, matches ✓.
- §14.4's P = 1 claim: planar bool pad bits 1–7 take the fill bit, so the planar and
  interleaved images coincide exactly when the fill is false — verified by
  construction (fill false → 0x00/0x01 both ways; fill true → planar 0xFE/0xFF).
  And ⌈P/8⌉ = P only at P = 1, so the "wherever ⌈P/8⌉ ≠ P" qualifier is exact.
- §20.3's example: 32·20 + 4 = 644 ✓.
- §9.2's Note: prior F + 4 + 64 = prior F + 68; both multiples of 64 ⇒ ≥ prior F +
  128 ✓. §9.3's ceiling: 2⁶³ − 64 is the largest multiple of 64 ≤ 2⁶³ − 1, and
  2⁶³ = 64·2⁵⁷ so it is one ✓.
- §21.9's note: 2³² entries → 2¹⁶ segments → 256 KiB array; 2³⁶ → 4 MiB ✓.
  65,536 layers × ~200 B ≈ 12.5 MiB ✓ (and the minimum layer record is 97 bytes,
  so "small layer records" at 200 B is a sane assumption).
- §19.4's Note: entries c·N+s and (c+1)·N+s differ by N; if N ≥ 2¹⁶ then
  ⌊(k+N)/2¹⁶⌋ ≥ ⌊k/2¹⁶⌋ + 1, so *"guaranteed to fall in different segments"* is
  exactly right ✓.

Register arithmetic, computed by parsing the tables:

- §21.2 "35 conditions" → 35 rows (F1…F36, F11 struck) ✓
- §21.3 "49" → 49 ✓; §21.4 "26" → 26 ✓; §21.5 "10" → 10 ✓
- §21.8 "120 conditions over 275 instances" → 120 rows; instance count by §21.1's
  own rule (semicolon-separated, a `—` cell counting 1) = **275** exactly ✓.
  Per-prefix: F 56, L 116, T 55, R 48.
- `[R-CNT-06]` governs exactly 9 rows ✓ (see §2.2 above).
- §20.5's "one row for each of the other seven spaces §10.2 tabulates
  (L31, L33, L34, L36, L43, L45, R1)" → 7 listed, and §10.2 tabulates 8 spaces
  with record type accounted separately (F36, L25) ✓.
- Requirement-identifier sweep: no gaps and no reuse in any prefix. ENC runs 1–16
  plus the deliberate `[R-ENC-100]` illustration in §2.2; SER-04 appears only in
  §14.4's withdrawal Note.
- Unlabelled blockquotes: exactly two in the document. One is the "How to read this
  document" block, explicitly marked *(non-normative)*. The other is §15.1's
  tile-index region layout — `[ entry array: entry_count × 20 bytes ] [ segment CRC
  array: ⌈entry_count / 2¹⁶⌉ × 4 bytes ]` — which carries no Note/Example/Rationale
  label and is therefore **normative** under `[R-CNF-01]`. I treated it as
  normative and my index arithmetic depends on it.

---

## 5. Sweeping the format change

The trailer no longer carries a field between `dir_length` and `file_id`. I swept
for staleness rather than assuming it had been done:

- `grep` for `offset 40|offset 48|offset 56|offset 32|trailer offset|F − 5`: three
  hits, all correct — §6.3's `F − 56` for version_major/minor (trailer offset 8 →
  F−56 ✓), F14's "trailer offset 60", F15's "trailer offset 48".
- `[R-CNT-24]`'s arithmetic: fixed bytes are 0–7 (magic), 8–11 (major+minor), 60–63
  (CRC) = 16; *"the remaining 48 trailer bytes"* = 12–59 ✓; 64 − 16 = 48 ✓. §2.3's
  Note that F15 does not reach because *"the trailer bytes it requires be zero are
  inside the 48"* — reserved is [48,60) ⊂ [12,60) ✓.
- *"The format-major-1 trailer has zero slack: every byte is assigned"* — 8+2+2+4+
  8+8+8+8+12+4 = 64 ✓.
- Every place the ordering quantity is named: §3.1, §9.2, §9.3 (three Notes),
  §9.6, §20.4's Rationale, §20.5, §21.7, §22.5, §23.2, Appendix D, Appendix G item
  4. All of them now say *committed file length*, and each of them separately
  disclaims the property the old field had and the new one does not (*"F counts
  bytes, not commits"*; *"no field records how many commits"*; *"nothing refutes
  this item by reading a value"*). §22.5's signature advice is pinned to the
  *prefix bytes* [0, F), not to the length, which is exactly what §9.6's *"A signed
  committed file length is not among them — the value is exactly what the re-append
  reproduces"* requires. I looked hard for a sentence that still leans on a
  counter's properties and did not find one.

---

## 6. Suspicions I opened and closed

- **Is `[R-CNT-06]`'s "nine" wrong now?** No — nine register rows govern under it,
  and 2 reach / 7 do not. Counted mechanically.
- **Does F11's striking leave a `[R-CNT-06]` condition unregistered?** No — all
  nine of `[R-CNT-06]`'s conditions have rows, and F5, F18, F19 are governed
  elsewhere as their cells say.
- **Does the reach set in §21.2 (F8, F14, F6, both F1 instances) miss anything?**
  I derived it independently from `[R-CNT-24]`'s three permanent facts (magic
  position, major/minor position, CRC at F−4) plus the front block's constancy.
  F5's floor derives from major-1 numbers, F13/F17 read redefinable bytes, F15's
  bytes are inside the redefinable 48. Same answer as the document's.
- **Could the walk double-claim a tile-index region?** No — §9.7 forecloses it in
  terms.
- **Could a partial total under-count?** Only under a "sum of lengths" reading with
  overlapping enumerated claimants; the set reading is the natural one and is
  monotone. Closed.
- **Could a superseded directory/trailer sit in the live pre-trailer gap and be
  mistaken for F7's "structure"?** No: a commit begins at the prior F, so every
  prior generation's bytes lie below the new `dir_offset`. And F7's "structure" is
  `[R-CNT-02]`'s defined term — a live-state member — with `[R-CNT-05]` saying it
  *"counts the rest as slack"*. (§5.1 uses the word loosely — *"the structures the
  file's commits appended … and each prior generation's trailer"* — but nothing
  normative turns on that sentence.)
- **Is T23 (lz4 frame instead of a block) actually detectable, given its cell says
  the detecting check is T25's?** Yes, deterministically: the frame magic's first
  byte 0x04 is an LZ4 token with literal length 0 and a match, whose offset comes
  from `22 4D` = 19,746, reaching back past zero produced output — T25's third
  instance exactly. Closed.
- **T15 (zlib wrapper) — always caught?** zlib's CM = 8 fixes the low nibble of
  CMF to 1000b, so as raw DEFLATE it always opens a non-final *stored* block; the
  4-byte Adler-32 trailer then makes T24 near-certain, and a bad LEN/NLEN makes
  T25 certain in the ordinary case. Not airtight in every hypothetical, but the
  cell says "T24's or T25's" and I could not construct a counterexample. Closed as
  not-my-lane and not demonstrable.
- **Is `[R-COD-11]`'s verifier clause reachable for a conforming verifier?** No,
  as argued in §2.3 above. Surplus, not a defect. Closed without reporting.
- **Do the durability barriers of `[R-LIF-02]` steps 4 and 6 belong in `[R-CNF-02]`'s
  conduct list or §21.7's account?** They are MUST-level writer obligations with no
  byte witness, and neither passage names them. But `[R-CNF-02]`'s conduct examples
  are introduced illustratively, and `[R-CNF-11]` restricts *cannot establish* to a
  *"capability or resource ground"*, which a barrier is not — so a verifier must
  certify past them and no verdict forks. Closed without reporting.
- **Does `[R-CNT-21]` leave the file-scope analogue of the layer-discard rule
  open?** It states the formula (*"F less the bytes claimed by the claimants the
  walk did enumerate"*) and carves out discarding only for layers, so the formula
  governs at file scope: do not discard. Resolvable; closed without reporting.
- **§21.9's per-instance rows** — I checked that *"decoded size of one tile"*
  ranging over **addressed** tiles makes an empty layer exempt, matching
  `[R-COD-07]`'s cap and §17.2's Note, while `[R-ENC-04]`'s ceiling still binds
  P·Q there. Consistent.
- **L2's nine designated quantities** — I re-derived them and checked the
  domination arguments: P·Q dominates V = P·C because every Bᵢ ≥ 1 so Q ≥ C;
  C·N dominates the maximum disk ordinal (C−1)·N + (N−1) = C·N − 1; ⌈P/8⌉ ≤ P;
  Fᶜ ≤ Q. Nothing is missing from the cell.
- **Appendix H's verifier checklist vs the 20 verifier rows** — complete, checked
  row by row.

---

## 7. Findings

### verifier-01 — CONTRADICTION

**Location.** §9.7, `[R-LIF-08]`, against §15.3 `[R-IDX-03]` and §5.2 `[R-CNT-02]`.

**Quotation (§9.7, `[R-LIF-08]`):**

> An entry `[R-IDX-03]` classifies reject-tile on a *structural* ground does not
> make the walk incomplete: the walk passes over it, and the bytes it nominally
> addresses fall to slack (§15.3).

**Against (§15.3, `[R-IDX-03]`):**

> Such an entry contributes no stored extent to the *verifier* rows, which bind
> over well-formed entries' extents only … and none to `[R-LIF-08]`'s coverage
> walk, so any bytes it nominally addressed that no other claimant claims fall to
> slack.

**And (§5.2, `[R-CNT-02]`):**

> Every byte of the live committed state belongs to exactly one of: the front
> signature block; or a **structure** …

**The defect.** §15.3 carries the qualifier *"that no other claimant claims"*;
§9.7's restatement drops it. Three of §15.3's six *structural* rows produce
entries whose nominal extent reaches bytes that **are** claimed, or that lie
outside the file:

- `offset < 16` (T8): the nominal extent starts inside the front signature block,
  which `[R-CNT-02]` makes a member of the live committed state and §9.7 itself
  says is *"claimed by the walk as well"*.
- `offset + length > F − 64` (T9): the nominal extent reaches into the live
  trailer, likewise claimed.
- `offset = S ∧ length ≠ S` and the sentinel-crc row (T6, T7): the nominal offset
  is 2⁶⁴ − 1, addressing bytes that do not exist in the file at all.

Applied literally, §9.7 puts bytes [0,16) or [F−64,F) into *two* classes at once —
the front block or trailer **and** slack — which is exactly what `[R-CNT-02]`'s
"exactly one" forbids, and would make the smallest legal file carrying a T8 entry
self-contradictory on its face. §15.3's sentence is the correct one.

**Which reading I picked, and why.** §15.3's. It is the passage that defines entry
classification, `[R-CNT-02]` is the partition rule, and §9.7's sentence is a gloss
citing §15.3 for its authority — so under §21.1's own principle (*"where a row and
the rule it cites diverge, the rule governs"*, applied here between a gloss and the
rule it cites), the qualified form controls.

**What an implementer does wrong without it.** A verifier that implements §9.7
literally computes its slack total as "unreached bytes **plus** the bytes nominally
addressed by structurally invalid entries", which double-counts front-block or
trailer bytes and reports a total exceeding F − 80 for a file where the true
residue is smaller. The safe implementation — slack = F minus the union of
enumerated claimants' ranges — gives the same answer under both readings, which is
why I grade this below byte level.

**Byte level?** No. Any file that can exhibit it already carries a T6–T12 violation
and is therefore nonconforming under both readings, so no verdict and no emittable
byte sequence moves; what diverges is the number on a report line.

---

### verifier-02 — AMBIGUITY

**Location.** §5.2, `[R-CNT-21]`.

**Quotation:**

> a verifier that reaches a live state MUST report the total number of slack
> bytes, since that number is what tells an operator to compact. Where §6.2's
> ordered validation rejects the file before a live trailer is established there
> is no F and no live state to walk, so the total is not owed at all: the verifier
> reports the trailer failure and nothing about slack, which is not a partial
> total but the absence of one.

**The defect.** The duty and its exemption are keyed to two different, non-
complementary conditions: the duty triggers on *"reaches a live state"*, the
exemption on *"rejects the file before a live trailer is established"*. Between
them sits a real and common case — a file whose trailer passes every §6.2 gate but
whose **directory** cannot be used: F20 (directory-region CRC mismatch) or F29
(record-sequence framing failure). There, a live trailer **is** established, so the
exemption does not apply; but no live state is reached, because §5.2 defines the
live committed state as the front block plus *"every structure reachable from the
live trailer **through the live directory's records**"* — and nothing is reachable
through a directory that will not parse.

**Permitted readings.**

1. *No total is owed.* "Reaches a live state" is the trigger, and it was not met;
   the verifier reports the directory failure and nothing about slack, exactly as
   the exemption's second sentence describes for the trailer case.
2. *A partial total is owed.* The exemption is expressly limited to pre-trailer
   rejections, so everything past it falls to the general rule, and the case is a
   *"scope-level rejection ends that scope's enumeration"* — file scope's
   enumeration — giving a partial total of F less the front block, the directory
   region and the trailer, with the directory CRC named as what stopped the walk.

**Which I picked, and why.** Reading 2. The exemption is drawn narrowly and given a
reason that does not transfer (*"there is no F"* — here there is an F, validated
and CRC-covered), and `[R-CNT-21]`'s own machinery for incomplete walks exists
precisely for rejections that end an enumeration. Reading 1 would also make the
duty unreachable in a second case I could not otherwise dispose of: F33 between two
non-layer structures likewise leaves no usable live state.

**What an implementer does wrong without it.** Two conforming verifiers hand an
operator materially different reports for the same corrupt file: one says "trailer
good, directory CRC failed, slack ≥ N bytes, walk stopped at the directory", the
other says nothing at all about slack. §22.3 makes the slack total the number that
*"distinguishes a working file from a padded one"*, so the difference is not
cosmetic for the operator deciding whether a file has been padded with smuggled
bytes.

**Byte level?** No. The verdict is NONCONFORMING under both readings and no
writer's emittable set moves; the divergence is confined to the contents of the
report.

---

### verifier-03 — OBSERVATION

**Location.** Appendix G (non-normative), item 5, against §17.3 `[R-COD-10]`.

**Quotation:**

> The filter is the identity exactly where its permutation is — where the stride
> is 1, as for a packed boolean plane, and equally where the decoded image is a
> single group, n = L/s being 1 (`[R-COD-10]`); elsewhere it changes the stored
> bytes of every tile it touches.

**The defect.** The first half is exactly right — I verified it: the shuffle sends
source offset j·s + i to i·n + j, and that is the identity map iff s = 1 or n = 1
(take i = 1, j = 0 to force n = 1; take i = 0, j = 1 to force s = 1). The final
clause overreaches. A permutation that is not the identity still fixes any image
that is invariant under it, and such images are legal and unremarkable: any decoded
tile image whose bytes are all equal is fixed by every byte permutation. So for
s ≥ 2 and n ≥ 2 the filter changes the stored bytes of every tile it touches
*except* the constant ones. Profile item 6 removes the all-*fill* case (an all-fill
tile is not stored) but not the general one — a tile of a uint16 channel whose every
byte is 0xAB, with fill 0x0000, is stored and is fixed by the shuffle.

**What an implementer does wrong without it.** Nothing, in bytes. The argument the
item needs — that two writers disagreeing on the filter value can produce different
files, so the profile must pin it — survives intact; only the universal quantifier
is wrong. I report it because Appendix G is the one place the document tells an
implementer how to obtain byte-identity, and a reader checking the profile against
a constant-image tile will find the sentence false of it.

**Byte level?** No. Appendix G is identified as non-normative, adds no requirement
to any actor (*"It adds no requirement to any actor: a writer ignoring it is fully
conforming"*), and the sentence is an aside inside an item whose operative content
— pin the filter value — is unaffected.

---

## 8. Confidence

**High** that a verifier built from this document alone would interoperate on the
things that decide a certificate: the three verdicts and their priority, the
capability/resource grounds, the coverage partition and its arithmetic, the
checksum map, the overlap/alignment/slab invariants, and the decode obligations.
Every constant reproduced; every closed count I could derive matched; the register
is internally consistent with its own instance-individuation rules; and the
format change has been swept thoroughly enough that I could not find a stale
offset, width, or example anywhere.

The three findings I do report all sit in the verifier's *report*, not its
*verdict*, and I have graded them accordingly rather than reaching for byte level.

**Where I found little.** My charter's "multi-generation trace" and "checksum
obligations" sections produced no findings, and I want to be explicit about what I
did there that would have found one. For the trace I computed the coverage total
four times by two independent methods (F minus claimed, and the sum of unreached
runs) and got agreement each time, including on the document's own smallest file,
where my 44 matched Appendix A's stated pad; a stale figure or an off-by-one in
`[R-CNT-17]`'s index-length formula, in `[R-LIF-02]`'s 128-byte floor, or in the
"F less claimed" definition would have shown up as a mismatch between the two
methods. For checksums I enumerated §8.1's seven rows against every live structure
class §5.2 names, checked the terminal/interior split in §4.5 against
`[R-CNT-20]`'s seven-link chain, and recomputed every stated constant; an
uncovered structure or a wrong constant would have surfaced. Both areas came back
clean, and I believe they are.
