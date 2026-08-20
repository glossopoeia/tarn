# Cleanroom round 15 — Register hunter transcript

Charter: audit §21, the error-handling register, against the rules it restates
and against itself.

## 0. Disclosure

I read exactly one file: `/Users/robertkleffner/Documents/GitHub/tarn/spec/tarn.md`,
in four `Read` calls covering lines 1–4227 (the whole document). I opened no
other file. I did not list any directory, did not run `git`, did not fetch
anything, and did not read the round-15 output directory.

I ran three shell commands that touch that file:

- `wc -l spec/tarn.md`
- three `grep`/`sed` invocations over `spec/tarn.md` (row-label citations,
  `R-ERR-` occurrences, `Writers MUST`/`validity error` occurrences)
- one `awk -F'|'` pass over `spec/tarn.md` that counts semicolon-separated
  instance entries per register row. This is mechanised grep over the one
  permitted file; it reads nothing else. I disclose it explicitly because the
  brief licensed "grep/rg", and `awk` is a step beyond the letter of that word
  even though it reads the same single file and nothing more.

I ran two Python scripts that read no files at all (`crc.py`, `crc2.py`),
containing only literal byte strings I typed from the document, to reproduce
the CRC-32C constants and Appendix A's trailer checksum.

I consulted no ADR, no conformance vector, no registry, no prior round's
findings, and no external format specification as evidence. General knowledge
of RFC 1951 / RFC 8878 / the LZ4 block format was used only to *generate*
suspicions about §17.2 and §18.2; every conclusion below is settled from this
document's own text.

---

## 1. What I did first: §21.1, because everything else is held to it

§21.1 is the register's constitution, so I read it before any row.

What it fixes:

1. **Extent.** "The register — §21.2 through §21.5 (`[R-ERR-02]`) — enumerates
   every detectable file-conformance violation this specification names".
2. **Outcome derivation.** "each row is one malformed condition, with the
   outcome class its scope determines (§2.4) — except where a rule assigns one
   expressly, as `[R-CNT-25]`'s quarantine does for every §21.5 row".
3. **Governing rule cell format.** "A Governing rule cell names that
   requirement first; any identifiers following it in parentheses are the
   further rules the condition reads, cited without brackets".
4. **Completeness is normative**, and the tiebreak: "each row *restates* its
   governing rule, and where a row and the rule it cites diverge, **the rule
   governs**." This clause is the reason most of what I found below is *not*
   byte-level: for a row/rule divergence the verdict is already decided, and
   only the table is wrong.
5. **Specialisation rule**: "F1 of F6 and of F8, F35 of F36, L24 of L25 — and a
   file exhibiting a specialization is recorded against the narrower row, whose
   detector and detection point are the ones that apply."
6. **Instance arithmetic**, in six sub-rules I extracted and applied
   mechanically in §3 below.
7. **Detection-point vocabulary**: "open, layer access, tile use, extent use —
   or *certification* for the rows a verifier detects".
8. **§21.6/§21.7/§21.9 are outside the register**, but "§21.6's entries restate
   their governing rules on the same terms a row does, and where such an entry
   and the rule it cites diverge, the rule governs there too."

I note in passing — and am *not* filing it as a finding — that §21.1 carries no
`[R-...]` identifier of its own. It is normative (not a Note/Example/Rationale),
and it is the arbiter of every row-vs-rule dispute in the document, yet a vector
or ADR can only cite it as "§21.1". I checked whether the document tolerates
untagged normative sentences elsewhere before deciding: §8.2's "Verification is
not optional: no in-file flag disables it, and a reader that skips it is not a
conforming reader" is untagged too, as is §6.1's "Writers MUST emit exactly
these 16 bytes." So untagged framing text is this document's settled practice,
and §21.1 is not anomalous. Dropped rather than filed, to keep the list honest.

---

## 2. Row-versus-rule agreement — the full sweep

I resolved the Governing rule cell of all 121 rows and compared the row's
wording, outcome class, scope, and detector against the cited requirement.
Recording only what I checked and where I stopped.

### 2.1 §21.2 against §6.1, §6.2, §6.3, §7.1, §7.2, §7.3, §5.1

`[R-CNT-06]`'s ordered gate list is: "the trailer magic; the trailer CRC; the
version gate (§6.3) … the flag gates (§6.3); committed_file_length equals the
file size … and is a multiple of 64; dir_offset ≥ 16; dir_length ≥ 4;
dir_offset + dir_length ≤ F − 64; 1 ≤ generation ≤ 2⁶³ − 1; file_id ≠ 0;
reserved bytes zero."

Mapping, gate by gate:

| gate | row |
|---|---|
| trailer magic | F8 (and F1's second instance, byte-reversed) |
| trailer CRC | F14 |
| version gate | F18 (version_major = 0); unimplemented major → §21.6, correctly not a row |
| flag gates | F19 (incompat lane); ignore lane → §21.6 |
| committed_file_length = file size | F17 |
| multiple of 64 | F13 |
| dir_offset ≥ 16 | F9 |
| dir_length ≥ 4 | F16 |
| dir_offset + dir_length ≤ F − 64 | F10 |
| 1 ≤ generation | F11 (0) and F2 (> 2⁶³ − 1) |
| file_id ≠ 0 | F12 |
| reserved bytes zero | F15 |

No gate is unregistered and no row registers a gate `[R-CNT-06]` does not state.

F29's bound is right: §7.1 puts the CRC in the region's final 4 bytes, so the
record sequence is `[dir_offset, dir_offset + dir_length − 4)`, which is exactly
what F29's cell says.

F30/F31/F32 are correctly restricted to *non-layer* top-level records, matching
`[R-CNT-13]`'s split ("the layer for a layer record and for sub-records, the
file for other top-level records — a malformed slot on a layer record is
therefore reject-layer"). The layer-side twins are L15/L16/L17. F25, F26 and F28
carry the same "non-layer" restriction, with L46/L47/L49 as their layer-side
twins. F24 (type 0) and F29 (framing) correctly do *not* carry it, because
`[R-CNT-12]` makes the directory's top-level framing file-scope for every
record including layer records. This split is done carefully and I found no
leak in it.

F33's exclusion clause resolves: "a claimant reaching the front signature block
or the live trailer is instead caught by the bounds rows F9/F10, F31/F32,
L16/L17 and T8/T9, each at its own tier". Claimant kinds are: directory
(F9/F10), non-layer top-level record extent (F31/F32), layer record and
sub-record extent — the tile-index region being the layer record's extent
(L16/L17), stored-tile extent (T8/T9). That is every claimant `[R-CNT-02]`
names. Correct.

F33's three alternatives — "across two layers, a layer structure against
another scope's structure, or two structures neither of which belongs to a
layer" — reproduce `[R-CNT-13]`'s three verbatim in substance. Correct.

### 2.2 §21.3 against §4.6, §7.2, §7.4, §11, §12, §13, §14.1, §15, §16, §17

I walked `[R-CNT-23]`'s "including" list and §7.4's constraint table field by
field:

- name rules → L3/L5/L6 (layer record name, at **open**, matching §19.1 step 4),
  L7/L8 (dimension and channel entries, at layer access), L4 (UTF-8), L9
  (duplicates)
- layout → L36 (0; reserved 3–255 — two instances, correctly no experimental
  range, matching §10.2's "channel layout … none")
- linearization → L33 (four instances, following §11.4's finer split 0 / 2–3 /
  4–0x7FFF / ≥0x8000 rather than §10.2's collapsed 2–0x7FFF; §11.4 defines the
  space, so §11.4 governs — correct)
- codec → L43; filter → L45; index_encoding → L31; channel type → L34 (four
  instances following §12.2's 0 / 14–19 / 20–0x7FFF / ≥0x8000)
- alignment A → L39; slab S domain → L1; A_slab → L28 (S = 0 with A_slab ≠ 0)
  and L29 (S ≠ 0 with a bad A_slab, three instances incl. A_slab = 0)
- rank / C / Tᵢ floors → L32
- fill length → L30; bool fill byte → L35
- entry_count vs geometry → L21; extent_length formula → L22
- crc_of_crc_array with entry_count = 0 → L27
- sub-records → L13 (type 0), L14 (framing), L19 (multiplicity), L24/L25
  (reserved-range type), L26 (nested layer record)
- exact parse of the inline payload → L23

Nothing in §7.4's table is unregistered.

L41 restates `[R-SLB-03]`'s transparency rules verbatim in substance —
"sentinels and entries §15.3 classifies reject-tile on a structural ground are
transparent, an entry failing only its stored bytes' crc is not" against
§16.2's "Sentinel tiles are transparent to run continuity … So are the entries
§15.3 classifies reject-tile on a *structural* ground … An entry whose only
defect is that its stored bytes fail its crc is not transparent". Agreement.

I checked §16.2's Note claim that `[R-SLB-04]` needs no row of its own — "every
file exhibiting one exhibits a run whose tiles are unpacked or whose first
stored tile is misaligned". I tried to break it: unstore a tile mid-run (leaves
a gap → L41 fires); unstore the run's *first* stored tile (the new first tile's
offset must be A_slab-aligned → L42 fires, unless A_slab = 1, in which case the
survivors are still packed and the declaration is not in fact stale); unstore
the run's *last* stored tile (survivors still packed, first still aligned — and
the invariants genuinely hold, so nothing is stale). Grow extents so N changes
and the planar channel blocks shift: placements generally break → L41/L42, and
where they accidentally still hold, the declaration is again not stale. The Note
survives. No finding.

### 2.3 §21.4 against §14, §15.3, §17

§15.3's eleven-row classification table maps onto §21.4 and §21.2 exactly:

| §15.3 row | register |
|---|---|
| valid sentinel | §21.6 (not a violation) |
| sentinel offset+length, crc ≠ 0 | T6 |
| exactly one field sentinel | T7 |
| length = 0 non-sentinel | T10 |
| offset < 16 non-sentinel | T8 |
| offset or length > 2⁶³ − 1 | T11 |
| offset+length overflows, or > F − 64 | T12 and T9 respectively |
| stored bytes fail crc | T1 |
| intra-layer overlap | L18 |
| overlap outside the layer | F33 |
| alignment or slab invariant violated | L40, L41, L42 |

§15.3 says "Six rows are marked *structural*"; I counted the marked rows —
rows 2, 3, 4, 5, 6, 7 — and got six. Agreement.

T2's carve-out ("the same byte at a padding position is T4's, the two rows
together covering `[R-SER-08]`") I checked for a hole. A padding position's
interleaved bool byte must equal the recorded fill byte (`[R-SER-05]`), and the
recorded fill byte is constrained to 0x00/0x01 by `[R-TYP-07]`, enforced at
layer scope by L35. So any padding byte outside {0x00, 0x01} differs from fill
and T4 fires; any padding byte equal to fill is in {0x00, 0x01} and satisfies
`[R-SER-08]`. Coverage is exact. No hole.

I also confirmed `[R-SER-08]` does not reach planar bool planes — §14.2 says "a
bool value — interleaved layers only, since §14.3 governs planar bool planes"
and §14.3 says "Every bit pattern of the value region decodes to a value
sequence" — so the absence of a planar analogue of T2 is correct, not a gap.

T13/T15/T16/T23/T26 are "cause" rows that name another row's check. Each
citation resolves and each names a row with the same detector and detection
point (T25 and T24 are reader/tile use, matching T13/T15/T16/T23; T2 and T4 are
verifier/certification, matching T26). No mis-citation.

`[R-COD-06]`'s six tile-scope constraints map to T17 (magic), T18 (extra
frames), T19 (dictionary ID), T20 (content-checksum flag), T21 (window),
T22 (frame content size); the trailing-bytes case is T24 under `[R-COD-08]`.

### 2.4 §21.5 against §7.1, §18.2

`[R-CNT-25]` enumerates the ways a document can be unreadable: "a failed extent
CRC, an unimplemented or invalid encoding, a decode failure, or content
violating the document's own rules (ill-formed UTF-8 included)".

- failed extent CRC → R2
- unimplemented/invalid encoding → R1 (0 and reserved 3–0x7F); experimental
  ≥ 0x80 → §21.6, correctly a non-violation per `[R-MTA-10]` and `[R-CNF-02]`
- decode failure → R3
- document content rules → R5 (UTF-8 / unpaired surrogate), R6 (empty key, C0),
  R7 (JSON / non-object / BOM), R8 (non-finite number), R9 (duplicate key),
  R10 (key > 255 bytes)
- frame constraints of encoding 2 → R4, under `[R-MTA-09]`

`[R-MTA-04]`'s four restrictions map onto R5–R10 with nothing left over, and
`[R-MTA-05]`'s sorted-members MUST is correctly *not* here — an unsorted
document is readable, so the quarantine does not reach it, and the rows sit at
the record's owning scope instead (F27 file-scope, L48 layer-scope), which is
what §18.1's "The owning scope of a user-metadata record is the file when the
record is top-level and the layer when it is a sub-record" requires.

R1's detection points ("open (top-level); layer access (sub-record)") are *not*
listed among §19.1 step 4's enumerated checks — step 4 names the (0,0) slot,
extent_length ≥ 5 and inline_length = 1, but not the encoding byte's value set.
I checked whether this is a defect and concluded it is not: §19's preamble says
"Those enumerations are not the complete inventory of what a reader detects at
that tier: §21's register is, and `[R-CNF-04]` binds a reader to every register
row whose detector is the reader, at the tier that row's *Detected* cell names".
The register governs the tier. No finding.

---

## 3. The counting, recomputed by hand and then mechanically

§21.1's instance criteria, as I extracted them:

- (i) an instance is a field the condition ranges over, a container it can occur
  in, one of several alternatives *the condition text states*, or a combination
- (ii) a family with no shape change is a single instance (T24's "any codec")
- (iii) layout formulas are materially different shapes and are enumerated
- (iv) a *differs from* / *does not equal* enumerates two directions; an
  *exceeds* / *larger than* enumerates one
- (v) a comparison with no magnitude ordering (checksum vs computed, bytes vs a
  constant) enumerates no direction
- (vi) a field tested only for nonzero is not a comparison
- (vii) one instance is one *distinguishable file*; a single predicate over
  several fields does not make its fields instances
- "Instances within a cell are separated by semicolons, and a cell reading — is
  one instance; the count is therefore mechanical once the cell is written."

Because the last clause makes the count mechanical, I counted by hand first and
then reproduced it with an `awk` pass over the Instances column.

Hand count, per subsection:

- §21.2: F1 2, F2 6, F3 2, F4 1, F5 2, F6 2, F7 4, F8 1, F9 1, F10 1, F11 1,
  F12 1, F13 1, F14 1, F15 1, F16 1, F17 2, F18 1, F19 1, F20 1, F21 1, F22 1,
  F23 1, F24 1, F25 1, F26 1, F27 1, F28 2, F29 3, F30 2, F31 1, F32 1, F33 5,
  F34 1, F35 1, F36 1 → **36 rows, 57 instances**
- §21.3: L1 8, L2 9, L3 1, L4 2, L5 1, L6 1, L7 2, L8 2, L9 2, L10 1, L11 1,
  L12 1, L13 1, L14 3, L15 4, L16 2, L17 2, L18 3, L19 1, L20 1, L21 4, L22 4,
  L23 4, L24 1, L25 1, L26 1, L27 1, L28 1, L29 3, L30 2, L31 3, L32 3, L33 4,
  L34 4, L35 1, L36 2, L37 1, L38 1, L39 3, L40 1, L41 3, L42 1, L43 3, L44 3,
  L45 3, L46 2, L47 2, L48 1, L49 4 → **49 rows, 115 instances**
- §21.4: T1 1, T2 1, T3 6, T4 4, T5 1, T6 1, T7 2, T8 1, T9 1, T10 1, T11 2,
  T12 1, T13 2, T14 6, T15 2, T16 1, T17 1, T18 4, T19 1, T20 1, T21 3, T22 6,
  T23 1, T24 1, T25 3, T26 3 → **26 rows, 57 instances**
- §21.5: R1 4, R2 2, R3 2, R4 12, R5 8, R6 4, R7 6, R8 2, R9 2, R10 2 →
  **10 rows, 44 instances**

Mechanical recount agreed exactly: `SECTION F: rows=36 instances=57`,
`SECTION L: rows=49 instances=115`, `SECTION T: rows=26 instances=57`,
`SECTION R: rows=10 instances=44`.

Totals: 36 + 49 + 26 + 10 = **121 conditions**; 57 + 115 + 57 + 44 =
**273 instances**.

Against the document's own stated totals:

- §21.2 "36 conditions" ✔
- §21.3 "49 conditions" ✔
- §21.4 "26 conditions" ✔
- §21.5 "10 conditions" ✔
- §21.8 "121 conditions over 273 instances" ✔

Every total reproduces. I looked specifically for semicolons inside Instances
cells that are not separators and found none (the semicolons in L41's, T2's,
T13's, T15's, T16's, T23's, T26's and R4's *Condition* text sit in a different
column and do not disturb the count).

Spot-checks of the criteria in application:

- (iv) is applied consistently: F17 (2, "does not equal"), L21 (4 = 2 layouts ×
  2 directions), L22 (4 = 2 directions + 2 stated alternatives), L30 (2),
  T3/T14/T22 (6 = 3 layouts × 2 directions) against T21 and L44 (3 = 3 layouts ×
  1 direction, both "exceeds"/"larger than"). The T3-vs-T21 pairing is the exact
  place the criterion could have been applied unevenly and it is not.
- (v) is applied consistently: T1, F14, F20, L37, L38, R2 are all 1.
- (vi) is applied: L20 ("both A ≠ 0 and S ≠ 0") is 1, not 2.
- (vii) is applied: F25/L46 (MU = 1 with PE = 0 — a two-bit combination) give
  one instance per container, while F28/L49 (a *stored bit differing from the
  registry*, which is two independently distinguishable files) give two per
  container. That distinction is right and is the subtlest thing in the column.
- F6 gives 2 (magic half, reserved half) even though the block is one constant;
  correct, because two distinguishable files exist, so (vii)'s "no two files
  could differ" justification does not bite.

L2's derived-quantity list I checked for omissions: Gᵢ ≤ Eᵢ cannot overflow; the
in-tile ordinal is < P; the disk ordinal is < C·N (the cell says so, and
(C−1)·N + (N−1) = C·N − 1, so the domination claim is arithmetically right);
the interleaved value offset is ≤ P·Q; V = P·C ≤ P·Q since every Bᵢ ≥ 1, which
is also stated; ⌈P/8⌉ < P ≤ P·Bᶜ for a planar bool plane, so its absence from
L2 is correct. The list is complete.

---

## 4. Completeness in both directions

### 4.1 Sweep for unregistered violations

I grepped every `Writers MUST`/`Writers MUST NOT`/`MUST NOT emit` and every
`validity error` in the document and walked the hits. Everything that makes a
file nonconforming and has a single-file witness has a row; the mapping is in
§2 above. The rules deliberately *without* rows are each accounted for:

- `[R-ENC-06]` fixed field widths — §21.7: "not a state a file can be in"
- `[R-GEO-06]`, `[R-SER-01]` ordinal mappings — §21.7
- `[R-CNT-13]`'s no-embedded-offsets rule for MU = 0 records — §21.7
- `[R-CNT-18]`'s nesting prohibition — §21.7 and §7.4's closing Note
- `[R-LIF-01]`, `[R-LIF-03]` — §21.7 (history, not reconstructed by §9.7)
- `[R-SLB-04]` stale slab declaration — §16.2's Note, verified in §2.2 above
- `[R-CNT-21]`'s slack-total reporting, `[R-CNF-11]`'s report obligations —
  verifier conduct, not file conditions
- SHOULD-level rules (`[R-CNT-03]`, `[R-CNT-09]`, `[R-CNT-26]`, `[R-TYP-10]`,
  `[R-ENC-14]`, `[R-LIF-07]`) — excluded by `[R-CNF-12]`: "§21's register
  enumerates MUST-level conditions only"
- writer *conduct* rules (`[R-EXT-03]`'s experimental prohibition, `[R-MTA-06]`
  on unregistered `tarn.` keys) — excluded by `[R-CNF-02]`, and both appear in
  §21.6 as non-violations

`[R-COD-02]` is stated declaratively with no MUST yet is registered (T13). I
weighed this against `[R-CNF-12]`'s "MUST-level conditions only" and concluded
it is fine: §2.1's Note says every requirement names the actor it binds, and
`[R-COD-02]` binds the file ("Every stored tile is independently decodable").
Declarative file-level requirements are MUST-level in force. Not filed.

`[R-LIF-02]`, `[R-LIF-04]`, `[R-WRT-05]`, `[R-WRT-06]`, `[R-WRT-07]`,
`[R-WRT-09]` are all history properties with no single-file witness and none is
named in §21.7's second paragraph, whose list reads exhaustive ("… ; and
`[R-ENC-06]`'s fixed field widths …"). I decided this is not a defect: §21.1
calls §21.7 "the account, **by class**, of what fails it", and the paragraph
opens by naming the class ("a single file exhibits no witness of their
violation") before giving examples. Not filed. But see finding register-03,
which is about a member of that list being *wrong*, not missing.

### 4.2 Sweep for over-registration

I checked each row that registers something a reader will not obviously call an
error, and each survived:

- F27/L48 — `[R-MTA-05]` is a writer MUST and says "the file is nonconforming"
- F28/L49 — `[R-CNT-22]`: "writers MUST emit exactly the flag values fixed"
- F26/L47 — `[R-CNT-12]`: "writers MUST emit zero"
- F25/L46 — `[R-CNT-12]`: "Writers MUST NOT emit the combination MU = 1 with
  PE = 0"
- F36/L25 — `[R-CNT-15]`: "emitting it is a violation"; `[R-EXT-03]`: "a value
  from a reserved range MUST NOT be emitted at all"
- R1 — `[R-MTA-03]`: "0 is invalid"; `[R-EXT-03]` for the reserved range; and
  §21.5's preamble is right that `[R-MTA-10]` withdraws only the *document's*
  content rules, never the encoding byte's own value set
- T5 — `[R-SER-05]`: "Every pad bit (§14.3) MUST carry the plane's channel's
  fill bit"
- L26 — `[R-CNT-18]` names this case in terms ("a layer record nested as a
  sub-record, say")

No row registers a non-violation.

---

## 5. Every cross-reference to a row

I grepped every row-label citation outside the four tables and resolved each:

| citation | at | resolves to | verdict |
|---|---|---|---|
| "L18's overlap or L40 through L42's placement" | §5.2 `[R-CNT-21]` | intra-layer overlap; alignment; slab packing; slab first-tile alignment — all verifier/reject-layer/placement | correct |
| "§21.2 rows F8 and F17" | §9.6 `[R-LIF-06]` | trailer magic; committed_file_length vs transport size | correct |
| "(§21.4, T24)" | §17.2 deflate Note | trailing bytes after the stream | correct |
| "(L44)" | §20.3 step 4 | lz4 decoded-size cap | correct |
| "F1 of F6 and of F8, F35 of F36, L24 of L25" | §21.1 | verified each containment by hand | correct |
| "(T24's *any codec*)", "(T15, T25)" | §21.1 | the single-instance family and the two enumerated families | correct |
| "F27 and L48" | §21.1 | the two `[R-MTA-05]` rows | correct as row identities; see finding register-02 for the *claim* made about them |
| "F9/F10, F31/F32, L16/L17 and T8/T9" | F33 | the four claimant tiers' bounds rows | correct |
| "T4's", "T25's", "T24's or T25's", "T24's", "T2's or T4's" | T2, T13, T15, T16, T23, T26 | each names a row with the same detector and detection point | correct |
| "(F36, L25)", "(F18, `[R-CNT-07]`)", "(F35, F36, L24, L25)" | §21.6 | reserved-range rows; version_major = 0 | correct |
| "(F1, F6)", "(`[R-CNT-05]`, F7)", "(F36, L25)", "(R1)" | Appendix H | verifier checklist | correct |

Every citation resolves to a row that says what the citing text claims. I found
no mis-pointed row reference anywhere in the document.

---

## 6. Outcome vocabulary

§2.4 defines five values. Four are reader outcomes — reject-file, reject-layer,
reject-tile, ignore-record — and `[R-CNF-07]` restricts violation assignment to
those four. All four are reachable and each is the outcome of exactly one
register subsection (§21.2/§21.3/§21.4/§21.5). preserve-verbatim is the fifth
and is correctly *not* reachable from any register row: §2.4 says it "names an
updater obligation, orthogonal to reader outcomes", and §20.4's table is where
its cases live. No row carries an outcome outside the vocabulary; no reader
outcome is unreachable.

I also checked the detector/detection-point vocabulary is closed. Twenty rows
carry detector *verifier* (F7, F25, F26, F27, F28, F33, F36; L18, L25, L40,
L41, L42, L46, L47, L48, L49; T2, T4, T5, T26) and every one of them carries
Detected = certification. Every other row carries detector *reader* and a
Detected cell drawn from {open, layer access, tile use, extent use}. §21.5 has
no verifier rows, which is right, since `[R-MTA-05]`'s two verifier rows live
at their records' owning scopes rather than under the quarantine.

---

## 7. Limits, in both directions

### 7.1 §21.9's minimum guarantees against their defining sections

| quantity | §21.9 | defining text | agreement |
|---|---|---|---|
| rank d | 32 | §7.4 u8, ≥ 1 (hard cap 255) | consistent |
| C | 4096 | §7.4 u16, ≥ 1 (hard cap 65,535) | consistent |
| entry_count | 2³² | `[R-ENC-03]` cap 2⁶³ − 1 | consistent |
| layers per file | 65,536 | no other cap | consistent |
| dir_length | 16 MiB | §6.2 ≥ 4, ≤ F − 64 − dir_offset | consistent |
| decoded tile | 256 MiB | `[R-COD-07]` hard cap 0x7E000000 ≈ 2016 MiB for codec 4 only | consistent |
| user-metadata document | 16 MiB | `[R-MTA-09]` "no smaller than §21.9's user-metadata guarantee"; §18.2's Note says "The 16 MiB figure" | consistent |
| zstd Window_Size | 8 MiB | `[R-COD-06]` "within §21.9's 8 MiB `Window_Size` guarantee" | consistent |

Appendix B's summary row reproduces all eight verbatim. §1's "§21.9's
tile-count guarantee" resolves to the entry_count row.

I checked §21.9's Note arithmetic:

- 2³² addressed tiles → ⌈2³²/2¹⁶⌉ = 2¹⁶ segments × 4 bytes = 2¹⁸ = 262,144 =
  **256 KiB** ✔ ("is still 256 KiB")
- 2³⁶ → 2²⁰ segments × 4 = 4,194,304 = **4 MiB** ✔ ("reaches 4 MiB at 2³⁶")
- 65,536 layers × 200 bytes = 13,107,200 = **12.5 MiB** ✔ ("roughly a 12.5 MiB
  directory at the small layer records that figure assumed")
- index region at the guarantee: 2³² × 20 + 2¹⁶ × 4 = 85,899,608,064 bytes,
  which is the "tens of gigabytes" §24's `[R-VEC-03]` says makes the vector
  unconstructible ✔

The composition of the layer-count and dir_length guarantees looked like a
conflict at first (65,536 layers at realistic record sizes exceeds 16 MiB), but
§2.3's acceptance duty is written as "none of whose values exceeds the minimum
guarantees", so a file breaching *either* releases the duty, and §21.9's Note
explicitly reasons about this ("the region's size is the product of the layer
count with each record's channel entries and names rather than the layer count
alone"). Not a defect.

### 7.2 `[R-ERR-05]`'s hard limits against their defining sections

Each of the ten restated hard limits matches its defining text exactly (name
255 / §4.6; metadata key 255 / §18.2's fourth restriction; rank 255 and C
65,535 / §7.4's field widths; 0x7E000000 / `[R-COD-07]`; 2⁶³ − 1 /
`[R-ENC-03]`; A power of two 512…2⁶² and A_slab power of two 1…2⁶² / §7.4 and
§16.1/§16.2; S 1…2⁶³ − 1 / §7.4 and §16.2; dir_offset ≥ 16 and dir_length ≥ 4 /
§6.2; 128 bytes / §5.1). I also verified the closing claim "Two do not [follow
from a field's width, an external format, the value domain, or arithmetic]" by
testing each entry: only the 512 floor on A and the 255-byte metadata-key cap
are chosen numbers, and both are the two the text names. The 2⁶² ceilings follow
from "power of two" plus the 2⁶³ − 1 domain, so they are not a third exception.

### 7.3 Limits stated elsewhere and missing here

`[R-ERR-05]` omits the user-metadata `extent_length ≥ 5` floor (§7.1, and
Appendix B lists it). This is not a defect: §21.9's opening says "The hard
limits it restates are a finding aid rather than an inventory", which licenses
omission.

It also restates the value-domain limit as "every offset, length, extent, and
count at most 2⁶³ − 1", which is not the operative bound for the two byte
lengths this format does not carry in a u64 — `inline_length` (u32) and every
name's length prefix (u8). That took me to §4.2, which claims all byte lengths
are u64, and that is finding **register-06**.

---

## 8. Findings

### register-01 — CONTRADICTION — §21.2's preamble excludes rows it contains

**Location:** §21.2 preamble; rows F1, F5, F6, F18. Requirements `[R-CNT-07]`,
`[R-CNT-04]`, `[R-CNT-27]`, `[R-CNF-02]`.

**Quotation (§21.2 preamble):**

> Every row here presupposes a file this specification judges: one declaring
> format major 1. A file declaring another major is neither conforming nor
> nonconforming under this text (§2.3, `[R-CNF-02]`), and no row below reaches
> it — §6.2's ordered validation puts the version gate ahead of every check but
> the trailer magic and the trailer CRC, so a foreign-major file is refused on
> capability grounds before any geometry row applies.

**Quotation (row F18):**

> | F18 | Trailer version_major is 0, a permanently invalid major in every
> format major version | version_major | reader | open | `[R-CNT-07]` |

The preamble's premise is universal over the subsection ("Every row here"), and
two independent classes of row escape it.

*First, F18 itself.* A file with version_major = 0 does not declare format major
1. §6.3 calls 0 "invalid" rather than a major, and §21.6 says "version_major =
0, permanently invalid in every format major version (F18, `[R-CNT-07]`)". So
F18 is a row about a file that declares no major at all, which by the
preamble's own premise the subsection does not reach — yet F18 is in it, and is
correct to be, because §6.2's trailer table gives version_major "Valid values"
of "1 (0 invalid; others: §6.3)" and `[R-CNT-07]` makes 0 a reader-detected
reject-file. The preamble states the exemption in terms of "another major";
zero is not another major.

*Second, the rows that precede the version gate but are not the two the
preamble carves out.* The preamble exempts only "the trailer magic and the
trailer CRC" — F8 and F14. But F6 (front signature block, `[R-CNT-04]`) is
required "before other processing" for a resident reader, and §19.1 step 1
places it before step 2's trailer fetch, so it fires on a file declaring major
7. F1's front-block instance is the same. And F5 (`[R-CNT-27]`, file shorter
than 128 bytes) is independent of the trailer entirely. Three rows reach a
foreign-major file that the preamble says no row reaches.

**Which governs.** §21.1's tiebreak decides row-versus-rule, and here each row
*agrees* with its rule; the divergence is between the rows and the preamble.
`[R-CNT-07]`, `[R-CNT-04]` and `[R-CNT-27]` are unambiguous, and `[R-CNF-02]`'s
exemption is worded for "another major", which 0 is not. So the rules and the
rows govern and the preamble is the wrong text. It should be narrowed to
something like: no row *below the trailer's magic, CRC, size and front-block
gates* reaches a file declaring a major this text does not define, and
version_major = 0 is not such a declaration.

**What an implementer does wrong without it.** A verifier that takes the
preamble literally reports *cannot establish* (or refuses to judge) for a file
whose version_major is 0, where §21.6 and F18 require *nonconforming*; and it
may decline to run the front-block equality check or the 128-byte floor against
a foreign-major file, which §2.3 ("A reader that additionally checks every
file-level requirement — including those ordinary readers are exempted from")
and Appendix H ("F1, F6") both require of it.

**Byte-level: no.** Every reader rejects a version_major = 0 file either way
(`[R-CNT-07]`), so no accept/reject verdict on bytes forks. The only divergence
is the label a verifier puts on that refusal, and `[R-CNT-07]` plus §6.2's
"Valid values" column settle it: the file is nonconforming. Only the preamble is
wrong.

---

### register-02 — AMBIGUITY — §21.1 re-opens the `[R-SER-08]` divergence §14.2 closed

**Location:** §21.1, final sentence; `[R-SER-08]` (§14.2); Appendix H's
conforming-reader checklist.

**Quotation (§21.1):**

> For a row whose Detector is *verifier*, the outcome names the scope at which
> the damage is recorded, not an obligation on any reader: the governing rule
> states what a reader does, and for several such rows it obliges the reader to
> serve the structure unchanged (`[R-SER-08]`, `[R-CNT-22]`, and `[R-MTA-05]`,
> whose unsorted document readers process as they find it — F27 and L48).

**Quotation (`[R-SER-08]`, §14.2):**

> A reader that neither detects the violation nor rejects the tile, and returns
> the value, MUST report 0x00 as false and every other byte as true.

Two readings of "obliges the reader to serve the structure unchanged" are
available.

*Reading A — "does not oblige the reader to refuse the structure."* On this
reading the sentence is about scope of refusal only, and it is true of all three
cited rules.

*Reading B — "obliges the reader to hand the structure's bytes on as it found
them."* This is what "unchanged" says, it is exactly right for `[R-CNT-22]` ("A
reader MUST apply a known type's specified semantics regardless of its stored MU
and PE bits") and for `[R-MTA-05]` ("readers process the document unchanged" —
and §21.1 spells out that gloss for `[R-MTA-05]` in the same parenthesis), and
it is wrong for `[R-SER-08]`, whose whole subject is a byte a reader must *not*
pass through: 0x02 is reported as true, not returned as 0x02.

I picked Reading A, because §21.1 says in the same clause that "the governing
rule states what a reader does" and `[R-SER-08]`'s own text is explicit. But
Reading B is the natural one — the parenthesis glosses only `[R-MTA-05]`,
leaving the reader to assume `[R-SER-08]` is the same shape — and it is
precisely the divergence §14.2's Rationale says the rule exists to prevent:
"leaving the return value undefined bought nothing: two readers handed the same
malformed tile could disagree about a sample and both be conforming, which is
the divergence this document exists to prevent." Appendix H states the correct
position ("returns sample bit patterns unaltered (§3.2), the sole resolved byte
being a nonconforming interleaved boolean it chooses to return rather than
reject"), and §21.1 now cuts against it.

A second, smaller inaccuracy in the same clause: `[R-SER-08]` does not *oblige*
a reader to serve anything. It is conditioned — "A reader that neither detects
the violation nor rejects the tile, and returns the value" — and `[R-CNF-12]`
expressly licenses a reader that does detect it to reject. So "obliges the
reader to serve" is wrong for `[R-SER-08]` under either reading.

**What an implementer does wrong without it.** A reader built from §21.1 alone
returns the raw 0x02 for a nonconforming interleaved bool sample instead of
reporting it as true, which is what `[R-SER-08]` was written to stop; or it
concludes it may not exercise `[R-CNF-12]`'s licence to reject the tile.

**Byte-level: no.** The divergence arises only in a nonconforming file — §14.2
says so ("it never arises in a conforming file, where the only bytes present are
0x00 and 0x01") — and no accept/reject verdict changes, since both readers
accept. §21.1's own clause defers to the governing rule, and `[R-SER-08]` is
explicit, so the resolution is available in the document. I record that the
*sample value returned* does fork between the two readings, and that §14.2's
Rationale treats exactly that fork as the thing the format must not have; a
triager who counts returned sample values as bytes on the wire may upgrade this.
I am not claiming it, because the file exhibiting it is nonconforming and the
conflict resolves within §21.1's own sentence.

---

### register-03 — CONTRADICTION — §21.7's two paragraphs disagree about §20.3 step 4's filter case

**Location:** §21.7, `[R-ERR-01]`, first and second paragraphs; §20.3 step 4.

**Quotation (§21.7, first paragraph):**

> A writer that emits well-formed structures carrying wrong sample values — a
> mis-strided filter (`[R-COD-10]`), an undisclosed compression dictionary
> (`[R-COD-06]`), or simply wrong data — produces a file that every checksum in
> §8 certifies.

**Quotation (§21.7, second paragraph):**

> §20.3 step 4's bar on a declaration change is witnessed only where the
> affected tiles remain stored — the §21.4 rows then fire — and a commit that
> supersedes every tile it would have damaged leaves the live state clean

The appositive asserts that when the affected tiles remain stored, the §21.4
rows fire. There is a case where the tiles remain stored and no §21.4 row fires,
and it is the case the first paragraph already claims for the undetectable
class.

**Worked counterexample.** Generation *g* carries layer X: interleaved, rank 1,
one float32 channel, extent E = 256, tile extent T = 256. Then G = ⌈256/256⌉ = 1,
N = 1, P = 256, Q = 4, and the decoded size is P·Q = 1024. G·T = 256 = E, so the
layer has **no padding positions**, and it has **no bool channel**, so it has no
pad bits either. Codec 1 (none), filter 1 (none). One tile is stored, 1024 bytes,
with its entry crc over those bytes.

Generation *g+1* changes one field of the layer record: filter 1 → 2
(byte-shuffle). Nothing else changes — the stored-tile set and the index content
are untouched, so §20.3 does not even require the index region to be re-emitted
("A layer whose record alone changes keeps its extent slot").

§20.3 step 4 bars this: the barred list names "the codec and filter that
produced the stored bytes", and the change reaches a tile the layer stores in
the generation this commit supersedes. It is not rescued by the escape clause
("a filter whose mandated stride makes it the identity"), because for an
interleaved float32 layer the mandated stride is Q = 4 and the shuffle is a
non-trivial permutation.

Now read generation *g+1* as a standalone file and run every §21.4 row:

- T1 — the entry crc still matches the unchanged stored bytes. Silent.
- T3 — filter 2's inverse preserves length (`[R-COD-10]`: "Length is
  unchanged"), so the decoded payload is 1024 = P·Q. Silent.
- T14 — codec 1 and the entry length 1024 equals the decoded size. Silent.
- T4, T5 — no padding positions, no pad bits. Silent.
- T2 — no bool channel. Silent.
- T21, T22, T17–T20 — codec 1, not zstd. Silent.
- T24, T25 — codec 1 consumes the extent exactly; there is no stream to
  malform. Silent.
- T26 — requires that "the resulting image breaks §14.5's padding content or
  `[R-SER-08]`'s bool bytes", and there is neither. Silent. (L = 1024 is
  divisible by s = 4, so `[R-COD-10]`'s divisibility precondition holds and the
  unshuffle is well defined on any 1024 bytes.)

No row fires anywhere in §21, at any scope. The file is a conforming file. Yet
every sample of the layer now decodes to a different bit pattern than it did in
generation *g*, and the commit violated §20.3 step 4.

**Which governs.** §20.3 step 4 governs the writer either way — nothing here
weakens the bar. What is wrong is §21.7's classification: this instance of the
bar belongs to the first paragraph's class ("wrong sample values … every
checksum in §8 certifies"), not to the "rows fire" case. The register stays
complete, because the condition is genuinely undetectable and so is outside
`[R-CNF-07]`'s gate.

**What an implementer does wrong without it.** Two things. A corpus builder,
told the §21.4 rows fire whenever the tiles remain stored, tries to build a
vector for a filter-change violation on a padding-free numeric layer and cannot,
and has no text telling it the attempt was misconceived. And a verifier author
concludes that a stored-tile-preserving declaration change is always caught, and
does not report the residual risk that §21.7's first paragraph exists to name.

**Byte-level: no.** No check exists under either reading; no reader or verifier
behaviour changes; the bar is normative in §20.3 regardless. The two
implementations here (one that believes the rows fire and one that does not)
emit the same bytes, accept the same files, and reach the same verdict on this
file — *conforming* — because the condition has no witness. This is a defect in
the account, not in what any implementation does.

---

### register-04 — AMBIGUITY — R4 groups conditions and instances on criteria its §21.4 twins do not use

**Location:** §21.5 row R4; §21.4 rows T17, T18, T19, T20, T24; §21.1's
instance criteria.

**Quotation (R4, Condition and Instances):**

> | R4 | A user-metadata document stored under encoding 2 breaks one of the
> frame constraints §18.2 states or carries over from `[R-COD-06]` — the single
> frame occupying the extent's bytes before its terminal CRC included; unlike
> R3, the constraint is broken whether or not the bytes decode | missing frame
> magic, top-level extent; … a skippable frame, top-level extent; … a second
> frame, top-level extent; … a nonzero dictionary ID, top-level extent; … the
> content-checksum flag set, top-level extent; … bytes remaining after the
> frame, top-level extent; … |

**Quotation (T18, Instances):**

> | a second concatenated compressed frame; a skippable frame before the frame;
> a skippable frame after the frame; a skippable frame between two frames |

**Quotation (§21.1):**

> each row is one malformed condition … What a cell enumerates is the
> condition's own alternatives and containers: a row whose check ranges over a
> family without the condition changing shape states that range as a single
> instance (T24's *any codec*), and one whose members give the condition
> materially different shapes enumerates them (T15, T25).

The same six frame constraints, drawn from the same requirement `[R-COD-06]`,
are laid out two different ways depending on which side of the quarantine they
sit on.

*At tile scope*: five separate rows — T17 (magic), T18 (extra frames), T19
(dictionary ID), T20 (content-checksum flag), plus T24 for the trailing-bytes
case — with T18 additionally enumerating **four** positional alternatives for a
skippable frame.

*At extent scope*: one row, R4, whose Condition is the compound "breaks one of
the frame constraints", with the six constraints demoted to instances and the
skippable-frame case collapsed to **one** instance per container.

Two readings of §21.1 are defensible.

*Reading A — the row is the requirement.* R4 is right: `[R-MTA-09]` states the
constraints as one bundle ("under the frame constraints of `[R-COD-06]` that do
not reference a tile: the frame magic; no skippable frame and no second frame;
no nonzero dictionary ID; no content-checksum flag"), so one requirement gives
one row and the bundle members are alternatives. On this reading §21.4
over-splits, since `[R-COD-06]` is likewise one requirement.

*Reading B — the row is the condition.* §21.1 says "each row is one malformed
condition"; a missing frame magic and a set content-checksum flag are two
different malformed conditions, so §21.4 is right and R4 is five rows collapsed
into one. On this reading R4's "a skippable frame" also under-enumerates,
because §21.1's own criterion — members that "give the condition materially
different shapes" — is what made T18 spend four instances on skippable-frame
placement, and the same three placements exist in a metadata extent.

I picked Reading B, because §21.1's normative sentence is "each row is one
malformed condition" and because T15, T18 and T25 all show the document
splitting a single requirement's alternatives across rows and instances rather
than bundling them. Under Reading B, R4 should be five rows, and the
skippable-frame condition should carry four positional instances per container
rather than one, which would move the totals from 121/273.

**Which governs.** Neither §21.1 sentence resolves it: "each row is one
malformed condition" and "the count is therefore mechanical once the cell is
written" push in opposite directions, the second making the *writing* of the
cell the unconstrained step. Nothing in §21.1 tells a maintainer when a
requirement's alternatives become rows and when they stay instances, and R4 and
T17–T20 are the same requirement's alternatives resolved in both directions.

**What an implementer does wrong without it.** Nobody's reader or writer
changes. Two things do change: the corpus, since `[R-ERR-02]` demands "one
vector per instance" and R4's collapsed skippable-frame instance buys three
fewer metadata vectors than the parallel tile case; and the register's stated
row total, since §21.8's "121 conditions" is a count whose meaning depends on
which reading is in force. A maintainer auditing completeness against §21.1's
normative completeness clause gets a different answer under each reading.

**Byte-level: no.** No file's acceptance or rejection turns on it: under either
grouping the same predicate is checked, by the same actor, at the same tier,
with the same ignore-record outcome. Only the number of rows and vectors moves.

---

### register-05 — AMBIGUITY — F27 and L48 drop `[R-MTA-05]`'s "at every nesting depth"

**Location:** §21.2 row F27; §21.3 row L48; `[R-MTA-05]` (§18.2).

**Quotation (F27):**

> | F27 | A top-level user-metadata document's object members are not in
> ascending order of their keys' UTF-8 bytes; the document stays readable and
> readers process it unchanged | — | verifier | certification | `[R-MTA-05]`
> (R-CNF-05) |

**Quotation (`[R-MTA-05]`):**

> Writers MUST serialize object members, **at every nesting depth**, in
> ascending order of their keys' UTF-8 bytes.

L48 is the same wording for a layer sub-record's document, likewise without the
depth clause.

Two readings of F27's noun phrase.

*Reading A — "[a top-level user-metadata document]'s object members"*, i.e. the
members of every object anywhere in that document. This matches the rule.
"Top-level" attaches to the *record* (it is what distinguishes F27 from L48,
whose row says "A layer sub-record's user-metadata document").

*Reading B — "a top-level [user-metadata document's object] members"*, i.e. only
the members of the document's outermost object. On this reading a document whose
outermost object is sorted but whose nested objects are not is conforming — and
that is wrong, because `[R-MTA-05]` says "at every nesting depth".

I picked Reading A: L48 has no "top-level" at all and must mean every object, so
the two twin rows can only be describing the same predicate, and Reading A is
the only one that makes them twins. But Reading B is available in F27 read
alone, and the word "top-level" is doing double duty in a row whose sibling does
not need it.

**Which governs.** §21.1: "where a row and the rule it cites diverge, **the rule
governs**." `[R-MTA-05]`'s "at every nesting depth" governs, so nested objects
must be sorted and the rows under-state.

**What an implementer does wrong without it.** A verifier built from F27 checks
only the outermost object and certifies a file `[R-MTA-05]` makes nonconforming;
a corpus builder writes a vector with a sorted outer object and an unsorted
nested one and records the wrong expectation.

**Byte-level: no.** `[R-MTA-05]` already says "the file is nonconforming, a
verifier MUST report it, and readers process the document unchanged", so no
reader's accept/reject behaviour is in play, and §21.1's tiebreak decides the
verifier's finding. The row is wrong; the rule is not.

---

### register-06 — CONTRADICTION — §4.2's "all byte lengths are u64" against §7.2 and §4.6, and the limit §21.9 restates over them

**Location:** §4.2 `[R-ENC-03]`; §7.2's record header table; §4.6; §21.9
`[R-ERR-05]`.

**Quotation (§4.2):**

> This specification uses the types `u8`, `u16`, `u32`, and `u64` for unsigned
> little-endian integers of 1, 2, 4, and 8 bytes. All file offsets, byte
> lengths, dimension extents, and tile extents are `u64`.

**Quotation (§7.2, record header):**

> | 4 | 4 | u32 | inline_length | structural |

**Quotation (§4.6):**

> All strings are length-prefixed UTF-8. Each structure's layout table states
> its prefix width, and every length prefix counts bytes — never characters or
> code points.

`inline_length` is a byte length and it is a `u32`. Every name's length prefix
is a byte length and it is a `u8` — §4.6 says so twice ("at most 255 bytes of
UTF-8 (so every name's length prefix is a single byte)"), and §7.4's payload
table spells it "u8 len + bytes" four times. So §4.2's universal is false of at
least two field classes this document defines, and it is stated in the same
requirement (`[R-ENC-03]`) whose next sentence sets the 0…2⁶³ − 1 domain.

The limits consequence, which is how I reached it: `[R-ERR-05]` restates that
domain as a hard limit — "every offset, length, extent, and count at most
2⁶³ − 1 (`[R-ENC-03]`)" — and for `inline_length` the operative hard limit is
2³² − 1, and for a name's length prefix 255. The 255 case is separately listed
in `[R-ERR-05]` ("a layer, dimension or channel name at most 255 bytes … a `u8`
length prefix"), which is why I think the omission of `inline_length` and the
overreach of §4.2 are the same defect seen from two ends: §21.9 restates a
domain that §4.2 states more broadly than the field table supports.

**Which governs.** §7.2's and §7.4's layout tables. `[R-ENC-06]` settles it
directly — "No field's width is ever a writer choice: every field's width is
fixed by this specification, and a structure whose fields appear at any other
width is invalid at its owning scope" — and §4.7's Note says layout tables give
each field's type. §4.2's sentence should be read as naming which *types* this
specification uses and which quantities are u64 *where a table does not say
otherwise*, or narrowed to the fields it is actually true of (offsets, extents,
tile extents, and the u64 lengths: dir_length, extent_length, index entry
length).

**What an implementer does wrong without it.** In practice: parses
`inline_length` at the wrong width. In principle the tables forbid it, and I
could not construct an implementation that actually does this, because §7.2's
row is unambiguous and `[R-ENC-06]` makes the table authoritative. What is more
likely is a validator that applies the 2⁶³ − 1 domain check to `inline_length`
and never applies the real 2³² − 1 ceiling, or a maintainer who reads
`[R-ERR-05]`'s hard-limit list as an account of every length ceiling in the
format when two are missing from it.

**Byte-level: no.** §7.2's layout table and `[R-ENC-06]` decide the width, so no
two implementations can differ on where `inline_length` lies or how wide it is,
and no file's acceptance turns on it.

---

## 9. What I could not determine, and where I guessed

- **§21.1's instance criteria do not close.** I could apply (i)–(vii)
  mechanically to every cell as written, and every total reproduced. What I
  could not derive from §21.1 is *when a requirement's alternatives become rows
  rather than instances*. R4 versus T17–T20 is the case where the answer
  visibly differs, and that is finding register-04; but the same open question
  would let a maintainer legitimately split or merge several other rows (T15
  into two, T25 into three, L33/L34's reserved sub-ranges into one) without
  violating any stated criterion. The stated criteria are complete for counting
  a written cell and silent on writing one.
- **F5's second instance.** "committed_file_length" as a distinguishable file
  from "F (physical file size)" requires a file where the two differ, which also
  trips F17. I concluded it is defensible under `[R-CNT-01]` ("The file size of
  a conforming file equals the live trailer's committed file length F") read
  with `[R-CNT-27]`, and §24's `[R-VEC-02]` anticipates exactly this ("where a
  condition cannot be isolated — §6.2's field gates are validated together"), so
  I did not file it.
- **§21.6's slack row** says a partial total is owed "where its walk did not
  complete", while §5.2 carves out a case where no total is owed at all ("Where
  §6.2's ordered validation rejects the file before a live trailer is
  established … the total is not owed at all … which is not a partial total but
  the absence of one"). I did not file this: §21.6's Condition column reads
  "Bytes the live state does not claim", which presupposes a live state, so the
  carve-out is outside the row's condition rather than contradicting it. I
  record the judgement because a stricter reader could file it.
- **§21.7's second-paragraph list reads exhaustive** but omits `[R-LIF-02]`,
  `[R-LIF-04]`, `[R-WRT-05]`, `[R-WRT-06]`, `[R-WRT-07]` and `[R-WRT-09]`, all
  of which are equally without single-file witnesses. I did not file it, because
  §21.1 characterises §21.7 as "the account, **by class**", and the paragraph
  names its class before giving examples. Judgement call.
- **§21.1 carries no requirement identifier.** Discussed in §1; not filed.
