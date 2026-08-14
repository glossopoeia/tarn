# Round 8 — Register hunter — working transcript

**Access disclosure.** I read exactly one file: `/Users/robertkleffner/Documents/GitHub/tarn/spec/tarn.md`,
in four `Read` calls covering lines 1–3843 (the whole document). I ran `grep`
against that same file only, four times (phrase sweeps for "validity error",
line-wrapped variants of it, the four outcome-class names, and the writer
prohibitions). I ran two local Python computations: one that generates CRC-32C
inputs from literals in the script and reads no files, and one that consumes
`grep` output over the spec on stdin to count register rows and semicolons in
the Instances column. I read no ADR, no `docs/`, no `PLAN.md`, no
`AGENTS.md`, no `conformance/`, no `registry.json`, no git history, and I ran no
web search or fetch. I listed no directories except creating my own output
directory. Nothing outside `spec/tarn.md` informed any conclusion below.

---

## 0. How I worked

My charter is §21, the error-handling register, audited against the rules it
restates and against itself. I did the work in this order:

1. Read §21.1 first and wrote down its governing rules, because everything else
   in §21 is held to them.
2. Read the whole document end to end, because the register cites forty-odd
   requirements and a register audit that does not read those requirements is
   an audit of a table's internal prettiness.
3. Built the row inventory mechanically and recounted conditions and instances
   by hand and then by script.
4. Swept the document for every condition that makes a file nonconforming or
   that a reader/verifier must detect, and matched each to a row (or to an
   explicit no-row note).
5. Swept the register in the other direction, asking of each row: does the rule
   it cites actually make this a violation?
6. Checked the outcome vocabulary for definedness and reachability.
7. Checked §21.9's limits against every other limit statement in the document.
8. Verified, by local computation, every CRC constant the register or its
   neighbourhood depends on.

### §21.1's rules, as I recorded them

- The register is §21.2–§21.5. Its completeness is normative in one direction:
  "a *detectable* violation this specification names and the register omits is
  a defect in this document".
- "each row *restates* its governing rule, and where a row and the rule it
  cites diverge, **the rule governs**." — This is the clause that decides most
  row/rule mismatches, and it is why I have flagged almost nothing byte-level.
- "Conditions attach to the finest structure they damage, and the outcome
  follows from that scope".
- Specializations: F2 of F8 and of F10, F38 of F39, L25 of L26; "a file
  exhibiting a specialization is recorded against the narrower row, whose
  detector and detection point are the ones that apply."
- §21.6–§21.9 are *not* register subsections and are reached by neither the
  completeness clause nor the instance arithmetic — but "§21.6's entries
  restate their governing rules on the same terms a row does, and where such
  an entry and the rule it cites diverge, the rule governs there too."
- Instance rule: an instance is "a field the condition ranges over, a container
  it can occur in, one of several alternatives the condition text states, or
  any combination of the three"; a family over which the condition does not
  change shape is one instance (T24's *any codec*); materially different shapes
  are enumerated (T15, T25); "Instances within a cell are separated by
  semicolons, and a cell reading — is one instance; the count is therefore
  mechanical once the cell is written"; "One instance is one *distinguishable*
  file", and the fields read by a single predicate (a sum against a bound, a
  combination of two flag bits) are not separate instances.
- Detection points are §19.2's tiers — open, layer access, tile use, extent
  use — or *certification*.
- For verifier rows the Outcome column "names the scope at which the damage is
  recorded, not an obligation on any reader".

---

## 1. The counting

### 1.1 Conditions

Rows present, in order, with no gaps and no duplicate identifiers:
F1–F39 (39), L1–L50 (50), T1–T26 (26), R1–R10 (10). Total 125.

Stated: §21.2 "39 conditions"; §21.3 "50 conditions"; §21.4 "26 conditions";
§21.5 "10 conditions"; §21.8 "125 conditions over 252 instances".
All four subsection totals reproduce, and 39 + 50 + 26 + 10 = 125 reproduces.

### 1.2 Instances

I applied §21.1's own arithmetic — semicolon count plus one, with "—" counting
one — by hand first, then mechanically. Hand totals per subsection:

- §21.2: F1 5, F2 2, F3 6, F4 2, F5 2, F6 1, F7 2, F8 2, F9 1, F10 1 → 24;
  F11–F30 all 1 → 20, running 44; F31 2, F32 3, F33 2, F34 1, F35 1, F36 5,
  F37 1, F38 1, F39 1 → **61**.
- §21.3: L1 8, L2 8, L3 1, L4 1, L5 2, L6 1, L7 1, L8 2, L9 2, L10 2 → 28;
  L11 1, L12 1, L13 1, L14 1, L15 3, L16 4, L17 2, L18 2, L19 3, L20 1 → 19,
  running 47; L21 1, L22 1, L23 3, L24 4, L25 1, L26 1, L27 1, L28 1, L29 1,
  L30 3 → 17, running 64; L31 1, L32 3, L33 3, L34 4, L35 4, L36 1, L37 2,
  L38 1, L39 1, L40 3 → 23, running 87; L41 1, L42 1, L43 1, L44 3, L45 1,
  L46 3, L47 1, L48 1, L49 1, L50 2 → 15 → **102**.
- §21.4: T1 1, T2 1, T3 6, T4 4, T5 1, T6 1, T7 2, T8 1, T9 1, T10 1 → 19;
  T11 2, T12 1, T13 2, T14 1, T15 2, T16 1, T17 1, T18 4, T19 1, T20 1 → 16,
  running 35; T21 1, T22 1, T23 1, T24 1, T25 3, T26 3 → 10 → **45**.
- §21.5: R1 4, R2 2, R3 2, R4 12, R5 8, R6 4, R7 6, R8 2, R9 2, R10 2 → **44**.

61 + 102 + 45 + 44 = **252**, exactly the figure §21.8 states.

I then re-derived the same numbers with a script that split each row on `|`,
took the third cell, and counted `;` + 1. It returned
`{'F': 61, 'L': 102, 'T': 45, 'R': 44} rows=125 instances=252`. The two agree.

**Result: every total the document states about the register reproduces.**
No arithmetic finding. That is the single most useful negative result in this
walk, and I want it recorded plainly, because the previous rounds' register
findings clustered here.

### 1.3 Where the arithmetic is mechanical but the cell-writing is not

§21.1 concedes this itself ("mechanical once the cell is written"), so the
following is not an arithmetic defect. But the *criteria* for writing a cell
are stated, and they are not applied uniformly:

- **Container axis, used and unused.** L1 splits the layer-record and
  sub-record containers into four instances
  ("layer record extent_offset; layer record extent_length; sub-record
  extent_offset; sub-record extent_length"). L16 does the same (4), L17 and L18
  each do it as two ("layer record extent slot; sub-record extent slot").
  L2, whose first instance is the sum over the very same two slots, writes a
  single "extent_offset + extent_length". Collapsing the *fields* of the sum is
  correct — §21.1 says so explicitly. Collapsing the *containers* is what L1,
  L16, L17 and L18 do not do. Two distinguishable files exist (an overflowing
  sum on a layer record's own extent slot; an overflowing sum on a sub-record's
  slot), both layer-scope by `[R-CNT-13]`, and under `[R-ERR-02]`'s
  "one vector per instance" only one of them gets built. See finding
  register-04.
- **Sub-alternatives, enumerated and not.** T3's condition text is one
  equality ("The decoded payload's byte length is not exactly the tile's
  decoded size"), and its cell nonetheless enumerates
  longer/shorter for each of three formulas — six instances for alternatives
  the condition text does not state. L42's condition text *does* state three
  alternatives ("gap, overlap, or out-of-ordinal placement") and its cell is
  "—", one instance. Each is individually defensible: L42's three alternatives
  are one predicate (`offset ≠ prev_offset + prev_length`) that does not change
  shape, and T3's longer/shorter arguably do give a corpus builder materially
  different files. I record the asymmetry and do not raise it as a separate
  finding; the cells are given, so no builder has to derive them.

### 1.4 Constants the register leans on, verified by computation

I implemented CRC-32C from §4.5's parameters (reflected Castagnoli 0x82F63B78,
init 0xFFFFFFFF, final XOR 0xFFFFFFFF) in a script that reads no files, and
checked:

| Quantity | Document | Computed |
|---|---|---|
| CRC-32C("123456789") (§4.5) | `0xE3069283` | `0xe3069283` |
| CRC-32C(zero bytes) (§4.5, Appendix A) | `0x00000000` | `0x0` |
| CRC-32C of a full all-sentinel segment (§15.4, cited by L39, Appendix B) | `0xEECB3BB2` | `0xeecb3bb2` |
| Appendix A trailer CRC over [0, 60) | `0xE00938D2`, stored `D2 38 09 E0` | `0xe00938d2` |

The segment computation used 65,536 × (`FF`×16 + `00`×4) = 1,310,720 bytes,
which is what §15.4's "full segment — one covering exactly 2¹⁶ entries" means
under §15.1's 20-byte entry. All four match. L39's parenthetical that the
constant "never substitutes for comparison" matches `[R-IDX-05]`'s
"Equality with the constant licenses nothing for readers".

Arithmetic I also re-derived while I was at it, all consistent:
2³² entries ÷ 2¹⁶ per segment × 4 bytes = 256 KiB (§21.9's note);
2³⁶ ÷ 2¹⁶ × 4 = 4 MiB (same note); 2³² × 20 bytes ≈ 85.9 GB, which is §24's
"tens of gigabytes of incompressible entries"; §15.4's worked example
(1,000,000 entries → 16 segments, last covering 16,960; region 20,000,064
bytes; entry 999,999 at region byte 19,999,980, i.e. segment-relative
20 × 16,959 = 339,180) checks out; the 128-byte minimum of §5.1/F7 is forced
(F must be a multiple of 64 and dir_offset + dir_length ≤ F − 64 with
dir_offset ≥ 16 and dir_length ≥ 4, so F = 64 is impossible and F = 128 is
achievable).

---

## 2. Completeness, document → register

I swept for every condition the document makes a violation or obliges a reader
or verifier to detect, using `grep` for the phrase "validity error" (including
its line-wrapped occurrences — line 2200 breaks "validity / error" across the
line boundary and the naive grep missed it, which is exactly the trap the brief
warned about), for each of the four outcome names, and for the writer
prohibitions. Then I walked §4 through §20 requirement by requirement.

Matched and covered (abbreviated; the full list is in my notes and every entry
below was checked against the row's wording, outcome, scope and detector):

- `[R-ENC-01]`/`[R-ENC-02]` → F1, F2. `[R-ENC-03]` → F3, L1, T11.
  `[R-ENC-04]` → F4, L2, T12. `[R-ENC-06]` → F5, L3 (**and nothing at tile
  scope — see register-03**). `[R-ENC-11]` → L4, L5, R5. `[R-ENC-12]` → L6,
  L7, L8, L9, R6, R10. `[R-ENC-15]` → F6, L10, and R9 by way of `[R-MTA-04]`.
- `[R-CNT-27]` → F7. `[R-CNT-04]` → F8. `[R-CNT-05]` → F9. `[R-CNT-06]` →
  F10–F19 (magic, CRC, length equality, 64-multiple, dir_offset floor,
  dir_length floor, dir bound, generation floor, file_id, reserved bytes),
  with generation's ceiling at F3. I checked each of `[R-CNT-06]`'s enumerated
  gates against a row and found all ten present.
- `[R-CNT-07]` → F20, F21 (**F21 is not a violation — see register-01**);
  version_minor's non-gating → §21.6. `[R-CNT-08]` → F22, and the ignore lane
  → §21.6.
- `[R-CNT-11]` → F23. `[R-CNT-25]` framing → F24, F25, L11, L12;
  `[R-MTA-03]` → F26, L13; quarantine ways → R1–R10.
- `[R-CNT-12]` → F27, F28, F29, F32, L14, L15, L47, L48. `[R-CNT-13]` → F4,
  F33, F34, F35, F36, L2, L16, L17, L18, L19. `[R-CNT-14]` → F37, L20, and
  zero layers → §21.6. `[R-CNT-15]` → F38, F39, L25, L26, with experimental
  MU = 0 → §21.6. `[R-CNT-16]` → L21. `[R-CNT-17]` → L22, L23.
  `[R-CNT-18]` → L24, L25, L27, and the nesting prohibition explicitly
  disclaimed as unwitnessable by §7.4's note. `[R-CNT-22]` → F31, L50.
  `[R-CNT-23]` → L28–L37, L40, L44, L46 in combination with the value-set
  rules. `[R-CNT-20]` → T1, L38, L39, R2, F16, F23.
- `[R-GEO-01]` → L33; `[R-GEO-02]` → §21.6; `[R-GEO-03]` → L2;
  `[R-GEO-05]` → L34; `[R-GEO-06]` → §21.7.
- `[R-TYP-03]` → L35; `[R-TYP-07]` → L36; `[R-TYP-06]`'s length cross-check →
  L31.
- `[R-SER-05]` → T4, T5; `[R-SER-06]` → L37; `[R-SER-07]` → T3;
  `[R-SER-08]` → T2; `[R-SER-01]` → §21.7; `[R-SER-09]` → §21.6.
- `[R-IDX-03]` — I mapped §15.3's eleven table rows one by one: sentinel →
  §21.6; crc ≠ 0 sentinel → T6; half-sentinel → T7; length 0 → T10;
  offset < 16 → T8; field over 2⁶³−1 → T11; sum overflow → T12 and
  sum > F − 64 → T9; stored bytes fail crc → T1; intra-layer overlap → L19;
  cross-scope overlap → F36; alignment/slab invariant → L41, L42, L43.
  All eleven land. `[R-IDX-04]` → L38, L39. `[R-IDX-05]` → no violation.
- `[R-SLB-01]` → L40, L41; `[R-SLB-03]` → L42, L43; `[R-SLB-04]` → no row,
  and §16.2's note says why in terms I checked and accept ("every file
  exhibiting one exhibits a run whose tiles are unpacked or whose first stored
  tile is misaligned, which §21.3 registers").
- `[R-COD-02]` → T13; `[R-COD-03]` → L44; `[R-COD-04]` → T14;
  `[R-COD-05]` → T15, T16; `[R-COD-06]` → T17–T22; `[R-COD-07]` → L45, T23;
  `[R-COD-08]` → T24, T25; `[R-COD-09]` → L46; `[R-COD-10]` → T26.
- `[R-MTA-04]` → R5–R10; `[R-MTA-05]` → F30, L49; `[R-MTA-09]` → R4;
  `[R-MTA-06]`, `[R-MTA-07]` → §21.6.
- History-dependent obligations (`[R-LIF-01]`, `[R-LIF-03]`, `[R-LIF-04]`,
  `[R-WRT-05]`–`[R-WRT-09]`, `[R-CNT-08]`'s updater copy-forward) → §21.7's
  second paragraph, which §21.1 calls "the account, by class". §21.7's own
  enumeration names only `[R-LIF-01]`, `[R-LIF-03]`, `[R-GEO-06]`,
  `[R-SER-01]` and `[R-CNT-13]`'s embedded-offset prohibition, but its stated
  ground — "properties of a file's history, which §9.7 does not reconstruct" —
  is a class, and every unnamed obligation I listed falls in it. I do not raise
  this: §21.1 describes §21.7 as an account by class, not by requirement.
- `[R-LIF-05]` residue past a completed commit → §9.5's note says it carries no
  row of its own, and gives a reason I checked and accept (the observable state
  is a trailer failing its gates, already F10/F16/F19).

**One gap.** `[R-ENC-06]` ("a structure whose fields appear at any other width
is invalid at its owning scope") has a cause row at file scope (F5) and at
layer scope (L3), and none at tile scope, although §15.1 fixes the tile-index
entry's field widths and offsets and makes the entry's owning scope the tile.
A 20-byte entry with compensating wrong widths (offset as u32 at [0,4), length
as u64 at [4,12), crc as u64 at [12,20)) keeps the region length that
`[R-CNT-17]` cross-checks and is detected only through whichever of
T8/T9/T11/T12/T1 the misparsed values trip — precisely the situation F5 and L3
describe of themselves ("the checks that fire are those values' own value and
bounds gates, and this row records the cause rather than a procedure of its
own"). See finding register-03.

**Two things I checked and found correctly absent.** (a) A row for "a byte
belongs to no coverage class": §5.2's note argues it "would be a row no file
could exhibit" because the live state is *defined* as what the walk reaches; I
followed that argument through `[R-LIF-08]` and it holds. (b) A row for a
pre-trailer pad longer than 64 bytes: §6.2 says "a longer gap is conforming",
so it is not a violation and belongs in no register subsection.

---

## 3. Completeness, register → document

Asking of each row whether the rule it cites actually makes the condition a
violation. Every row survived this except one.

- **F21** — "Trailer version_major is a nonzero major the reader does not
  implement (e.g. 2); magic and CRC still validate". Its rule, `[R-CNT-07]`,
  obliges a reader to reject-file. It does not make the file nonconforming, and
  §21.6 says in as many words that the file "can be perfectly conforming under
  that major" and that F21's "condition records only the reader's outcome and
  not a defect in the bytes". Finding register-01.
- Everything else: F22's incompat-lane bit is a violation, because §6.3 excuses
  only the *ignore* lane ("a set ignore-lane bit is not a file-conformance
  violation") and `[R-CNF-02]` picks up exactly that exception by name. The
  reserved-range rows (F39, L26, R1's reserved half) are violations because
  §10.3 says a reserved value "MUST NOT be emitted at all", a prohibition on
  bytes and not on conduct — unlike the experimental prohibition, which
  §21.6 and `[R-CNF-02]` classify as conduct. The experimental-value rows in
  the layer-scope value sets (L32, L34, L35, L37, L44, L46) are violations not
  because of §10.3 but because each space's own rule (`[R-GEO-05]`,
  `[R-TYP-03]`, `[R-SER-06]`, `[R-COD-03]`, `[R-COD-09]`, §7.4/§15.1) makes any
  unassigned value a validity error; `[R-EXT-03]` routes each space
  individually and the register matches it space by space, including the two
  spaces where the experimental value is *not* a violation (record type,
  metadata encoding — both in §21.6). This is the most carefully constructed
  part of §21 and I could not fault it.
- The F/L partition of the shared rules is exact and deliberate: F28/F29 and
  F31 and F33/F34/F35 say "non-layer top-level record" while L47/L48, L50 and
  L16/L17/L18 say "layer record's or sub-record's", because `[R-CNT-13]` maps
  "the scope the record governs" to the layer for a layer record. But F32
  correctly says "A top-level record's" without the non-layer qualifier,
  because `[R-CNT-12]` scopes a framing overrun to the *sequence's* owning
  scope — file, even for a layer record. I checked that this distinction is
  right in both directions and it is.

---

## 4. Row-versus-rule: outcome, scope, detector, tier

### 4.1 Outcomes and scopes

Every row's outcome is the one its subsection header assigns, and I checked
each against the cited rule's stated scope. All agree. Notable ones I expected
to be wrong and were not:

- L47 (MU = 1 with PE = 0 on a layer record) is reject-layer, not reject-file,
  even though §7.3's table gives the layer record's Scope as "file (container
  for layer scope)". `[R-CNT-12]` says "the record's governing scope" and
  `[R-CNT-13]` defines that phrase as "the layer for a layer record". The row
  even cites (R-CNT-13) for exactly that. Correct.
- R2 is ignore-record though the containing scope may be the file, because
  `[R-CNT-25]`'s quarantine is stated to govern "notwithstanding the
  owning-scope mapping of `[R-CNF-08]`". Correct.
- F36/L19 record overlap at file/layer rather than at the tile, against
  §21.1's "finest structure they damage" principle — but `[R-CNT-13]` states
  the two scopes explicitly, and §21.1 says the rule governs. Correct.
- L38/L39 are reject-layer while detected at tile use, which §19.2 anticipates
  in terms ("index-chain failures take layer scope (`[R-IDX-04]`) although
  their detection point is tile use"). Correct.

### 4.2 Detectors

Every "verifier" row traces to a rule that assigns detection to a verifier:
F9 (`[R-CNT-05]`), F28/F29/L47/L48 (`[R-CNT-12]` "their detection is a
verifier's"), F30/L49 (`[R-MTA-05]` "a verifier MUST report it"), F31/L50
(`[R-CNT-22]`), F36/L19 (`[R-CNT-13]` "readers are not obligated to detect
overlap"), F39/L26 (`[R-CNT-15]`), L41 (`[R-SLB-01]`), L42/L43 (`[R-SLB-03]`),
T2 (`[R-SER-08]` "its assigned detector is the verifier"), T4/T5
(`[R-SER-05]` "a verifier MUST check it"), T26 (`[R-COD-10]`). No row assigns
verifier detection where the rule assigns it to a reader, or the reverse.

### 4.3 Detection tiers

Every Detected cell holds one of §21.1's five permitted values. One is wrong:

**L24 says "layer access"**, but one of its four instances — a name-field
overrun inside "leading fixed fields (name … C)" — is due at open. §19.1 step 4
makes the layer-name namespace part of the open and says of exactly this
condition that such a record "yields no name field to compare, so it
contributes no name to the namespace and is instead a validity error at layer
scope (`[R-CNT-18]`)"; §19.2's tier list puts "the layer-name namespace
(§19.1's steps)" at open. A reader cannot defer this to layer access, because
it must decide at open whether the record contributes a name — that decision
*is* the detection, and F6's duplicate-name check at open depends on it.
Finding register-02.

I checked R1's tier ("open (top-level); layer access (sub-record)") against
§19.2 and accept it: the encoding byte is inline and resident, and although
§19.2's reliance rule would permit deferring to extent use, §19's preamble
makes the Detected cell binding, and detecting earlier is harmless
(`[R-CNF-12]`, §19.2's "MAY detect any violation earlier"). L4/L6/L7 at open
are right for the same reason L24 is wrong: §19.1 step 4 checks layer names
"per §4.6", which is `[R-ENC-11]` through `[R-ENC-15]`.

---

## 5. The outcome vocabulary

§2.4 defines five values: reject-file, reject-layer, reject-tile,
ignore-record, preserve-verbatim. `[R-CNF-07]` names the first four as the
reader outcomes and preserve-verbatim as an updater obligation.

- Every register row's outcome is one of the four reader outcomes, assigned by
  its subsection header. No row carries an undefined outcome.
- All four reader outcomes are reachable: §21.2/§21.3/§21.4/§21.5 respectively,
  and ignore-record is additionally reachable for non-violations (§21.6's
  unknown MU = 0 record, its experimental metadata encoding).
- **preserve-verbatim is defined and then never used.** `grep` finds the string
  exactly twice, both in §2.4 (its definition and its table row). §20.4 states
  the same obligation in prose — "Retain byte-identical" in all three rows of
  its table, and `[R-WRT-05]`'s "MUST re-emit byte-identically" — without
  binding the defined term to any record class. Nothing behavioural turns on
  it; the updater's obligations are fully determined by §20.4 and the PE bit.
  Finding register-06, at the lowest severity I have.

---

## 6. Limits

I checked §21.9 against every other statement of a limit.

`[R-ERR-03]`'s eight minimum guarantees are internally consistent and
consistent with everywhere they are cited: §2.3's acceptance duty, §2.5's
`[R-CNF-10]`, §17.2's zstd-window SHOULD ("within §21.9's 8 MiB `Window_Size`
guarantee"), §18.2's "no smaller than §21.9's user-metadata guarantee",
§1's "§21.9's tile-count guarantee", Appendix B's collected row (which restates
all eight identically), and Appendix H's reader checklist. The §21.9 note's
arithmetic reproduces (256 KiB at 2³², 4 MiB at 2³⁶). The apparent tension
between "65,536 layers" and "16 MiB directory" is handled explicitly in the
note, which says the two rows state the same budget from different ends; a file
whose 65,536 layers push the directory past 16 MiB exceeds the dir_length
guarantee and is declinable, so `[R-CNF-03]`'s acceptance duty stays
satisfiable. No contradiction.

The interaction of the 256 MiB tile guarantee with `[R-COD-06]`'s
window ≤ decoded-size rule and the 8 MiB window guarantee also composes: a
256 MiB tile with a 256 MiB window is conforming and declinable, which is why
§17.2 carries the SHOULD.

`[R-ERR-05]`'s hard-limit inventory does not hold up as stated. It claims
"Each is a consequence of a field's width, an external format, or the value
domain — never a number chosen here", and its list is a name at most 255 bytes,
rank at most 255 and channel count at most 65,535, codec 4's 0x7E000000, and
the 2⁶³−1 value domain. Two problems:

1. §16.1's per-tile alignment floor — "a power of two with 512 ≤ A ≤ 2⁶²" —
   is a hard limit (a layer declaring A = 256 is invalid at layer scope; L40
   registers "A below 512" as an instance) and 512 is a number chosen here,
   which §16.1's own note concedes ("512 is the legacy sector floor"). It is
   absent from the inventory. A_slab's power-of-two constraint is likewise
   absent.
2. The 255-byte cap is attributed to "a `u8` length prefix". That holds for
   layer, dimension and channel names. It does not hold for user-metadata keys,
   which §18.2 subjects to the same cap ("every key satisfying §4.6's name
   rules — non-empty, at most 255 bytes") and which carry no length prefix at
   all; R10 registers a longer key, and §21.5's preamble makes every row there
   a violation, so the cap is hard and is a number chosen here.

Finding register-05. Neither costs an implementer anything — §16.1 and L40
fully determine A, and §18.2 and R10 fully determine keys — so this is an
inventory defect, not a behavioural one.

---

## 7. Findings

Each finding states the byte-level test's answer. I have flagged **none** of
them byte-level, and I want to be explicit that this is a conclusion and not a
reflex: I looked hardest at register-01, which comes closest, and talked myself
out of it below for a reason I can state.

---

### register-01 — CONTRADICTION — F21 registers a condition the document elsewhere says is not a violation, and `[R-VEC-04]`'s universal claim about register vectors is false because of it

**Location.** §21.2 row F21; §21.1's completeness clause; §21.6's closing
paragraph; §24, `[R-VEC-04]`.

**Quotations.**

§21.2, F21, under the heading "#### 21.2 File-scope violations / Outcome:
reject-file. 39 conditions.":

> | F21 | Trailer version_major is a nonzero major the reader does not implement (e.g. 2); magic and CRC still validate | version_major | reader | open | `[R-CNT-07]` (R-CNT-24) |

§21.1:

> The register — §21.2 through §21.5 (`[R-ERR-02]`) — enumerates every
> detectable violation this specification names: each row is one malformed
> condition

§21.6:

> Two structural cases are **conforming files a reader nevertheless refuses**.
> The first is **version_major naming a major this reader does not
> implement**: the reader rejects the file (`[R-CNT-07]`), but the file can be
> perfectly conforming under that major. … In both the outcome records a
> reader's capability, not a defect in the bytes, and the diagnostic ought to
> distinguish the two. That is why the second is not a register row, while the
> first is registered as F21, whose condition records only the reader's outcome
> and not a defect in the bytes

§24, `[R-VEC-04]`:

> because `[R-CNF-12]` permits the latter for any nonconforming file and every
> vector built from §21's register is nonconforming.

**What is wrong.** Three things, all following from the same root.

(a) §21.1 defines a register row as a malformed condition and a detectable
violation, and §21.2's heading calls its rows file-scope violations. F21 is
neither, by §21.6's own account.

(b) §21.6's justification is self-defeating as written. It says the two cases
are alike ("In both the outcome records a reader's capability, not a defect in
the bytes"), and then offers that likeness as the reason the second is excluded
while the first is included. The sentence gives no ground on which the two are
treated differently.

(c) `[R-VEC-04]`'s "every vector built from §21's register is nonconforming" is
false, and F21 is the counterexample. Worse, `[R-VEC-02]` requires each
vector's manifest to record "whether the file is **conforming**", a binary, and
for F21's vector — a file whose version_major is 2 — the answer is neither
"yes" (this document's file-level requirements are major-1 requirements) nor
"no" (§21.6 says it "can be perfectly conforming under that major"). A corpus
builder has no defensible entry to write.

**Permitted readings, and which I picked.** Reading 1: F21 is a violation row
like every other, so a verifier that establishes it reports *nonconforming*.
Reading 2: F21 is a reader-capability row that records a refusal, not a defect,
so a verifier handed a major-2 file reports *cannot establish* and F21 has no
bearing on the file's conformance. I picked reading 2, and I think it is
forced rather than merely preferable: §2.3 names this exact case as a
*cannot establish* ground —

> A verifier reports one of three verdicts: *conforming*, *nonconforming*, or
> *cannot establish* — the last where some requirement is one it is unable to
> check, as when the file names a format major version it does not implement

— and §21.1's tie-breaker ("where a row and the rule it cites diverge, **the
rule governs**") points at `[R-CNT-07]`, which obliges rejection and says
nothing about conformance, and §21.6 says the same in plain words. Three
independent places decide it.

**What an implementer does wrong without it.** A verifier author who builds
from the register table alone reports *nonconforming* for a well-formed major-2
file, which §2.3 forbids ("*Cannot establish* is not a finding that the file is
nonconforming"). A corpus author writes a manifest entry that `[R-VEC-02]`
cannot accommodate.

**Byte-level: no.** This is exactly the shape the round-8 brief calls out. The
row contradicts material elsewhere, but §21.1 has already decided which
governs, §2.3 states the correct verdict independently, and §21.6 states the
correct classification independently. Two competent implementations reading the
whole document reach the same verdict on the same bytes: reject the file at
open, report *cannot establish*, do not report nonconforming. What is wrong is
the table's placement of the row and `[R-VEC-04]`'s universal, not any file's
fate. The cheapest fix is to move F21's substance into §21.6 beside the
experimental MU = 1 case, or to keep it and qualify `[R-VEC-04]` and §21.1.

---

### register-02 — CONTRADICTION — L24's detection tier is "layer access", but §19.1 makes the name-field overrun instance due at open

**Location.** §21.3 row L24; §19.1 step 4; §19.2's tier list.

**Quotations.**

§21.3:

> | L24 | A declared region of the layer record's inline payload does not lie entirely within inline_length (overrun or truncation) | leading fixed fields (name … C); d dimension entries; C channel entries; trailing fixed fields (index_encoding, entry_count, crc_of_crc_array) | reader | layer access | `[R-CNT-18]` |

§19.1, step 4:

> The layer-name namespace is built from the name fields a reader can obtain
> under §7.4's framing: a layer record whose name field does not lie entirely
> within that record's inline_length yields no name field to compare, so it
> contributes no name to the namespace and is instead a validity error at layer
> scope (`[R-CNT-18]`).

§19.2:

> - **at open:** the front signature block, for a reader whose open leaves it
>   resident (`[R-CNT-04]`), the trailer, the directory region and its record
>   walk, and the layer-name namespace (§19.1's steps);

**What is wrong.** L24's first instance covers the leading fixed fields, of
which the name is the first. §19.1 places the discovery of a name-field overrun
inside the open, and §19.2 places the layer-name namespace at the open tier.
The row's Detected cell says the whole row is due at layer access. Since §19's
preamble makes the cell binding — "`[R-CNF-04]` binds a reader to every
register row whose detector is the reader, at the tier that row's *Detected*
cell names (§21.1)" — the two texts state different tiers for the same
condition.

**Permitted readings, and which I picked.** Reading 1: L24 is due at layer
access throughout, and a reader may open a file containing such a record
successfully. Reading 2: the instance touching the name is due at open, the
other three at layer access. I picked reading 2, on §21.1's "the rule governs"
and because reading 1 is not implementable: the open must decide whether each
layer record contributes a name to the namespace before it can apply F6, and
that decision is the overrun check. A reader cannot both perform §19.1 step 4
and defer L24's first instance.

**What an implementer does wrong without it.** A reader built from the table
reports a successful open, lists a layer whose record it has not parsed far
enough to name, and discovers the defect only if the caller touches that layer.
No wrong data is returned in either reading — the layer is rejected before
service in both — so the divergence is in when the open fails, not in what is
served.

**Byte-level: no.** No byte sequence changes hands, and no accept/reject verdict
on any scope differs: the layer is reject-layer under both readings, the file
is nonconforming under both, and §19.2 licenses earlier detection anyway ("A
reader MAY detect any violation earlier"). Only the timing of the diagnostic
moves.

---

### register-03 — OBSERVATION — `[R-ENC-06]` has cause rows at file and layer scope and none at tile scope, though the tile-index entry is a fixed-layout tile-scope structure

**Location.** §21.4 (absence); §21.2 F5; §21.3 L3; §4.2 `[R-ENC-06]`; §15.1;
§21.1's completeness clause.

**Quotations.**

§4.2:

> No field's width is ever a writer choice: every field's width is fixed by
> this specification, and a structure whose fields appear at any other width is
> invalid at its owning scope. `[R-ENC-06]`

§15.1:

> The owning scope of a layer's tile index is the layer; the owning scope of an
> individual entry, and of the stored tile it addresses, is the tile.

§21.2, F5 (the file-scope analogue that does exist):

> | F5 | A fixed file-scope structure places its fields at widths other than those the spec fixes, with total size unchanged, detectable only through the values the fixed-width parse then reads at the shifted offsets; the checks that fire are those values' own value and bounds gates, and this row records the cause rather than a procedure of its own | trailer (e.g. version_major and version_minor each written as u32); top-level record header | reader | open | `[R-ENC-06]` (R-CNT-06) |

§21.1:

> Its **completeness is normative** — a *detectable* violation this
> specification names and the register omits is a defect in this document

**What is wrong.** The register carries a "records the cause" row for
`[R-ENC-06]` at file scope (F5) and at layer scope (L3, "A field of a
layer-scope structure is written at a width other than the one this
specification fixes (e.g. rank d as u16)"), and none at tile scope. §15.1
fixes the tile-index entry's three fields at u64/u64/u32 and makes the entry's
owning scope the tile, so `[R-ENC-06]` names a tile-scope condition. It is
reachable with the entry's total size preserved — offset written as u32 at
[0,4), length as u64 at [4,12), crc as u64 at [12,20) keeps 20 bytes and so
keeps `[R-CNT-17]`'s region-length cross-check satisfied — and is then
detectable exactly as F5 and L3 concede of themselves, through whichever of
T8, T9, T11, T12 or T1 the misparsed values trip.

**Why I filed it as an observation rather than an ambiguity.** Nothing is
underdetermined: every instance of the condition is caught, with the right
outcome and scope, by a row that already exists. What is missing is the cause
row, and the register's own practice (F5, L3, and also T13 and T26, both of
which say "the check that detects it is …'s, and this row records the cause
rather than a procedure of its own") establishes that the document wants such
rows. Deciding whether the gap matters costs more than the gap does.

**Byte-level: no.** Adding the row changes no outcome, no scope, no detector
and no tier for any file; every affected file is already rejected at the tile,
by the existing rows, on the existing grounds. It changes the corpus by one
condition and one instance, and it changes §21.8's totals from 125/252 to
126/253.

---

### register-04 — OBSERVATION — L2 collapses the layer-record and sub-record containers that L1, L16, L17 and L18 enumerate, so one distinguishable file has no corpus instance

**Location.** §21.3 rows L1, L2, L16, L17, L18; §21.1's instance rule; §21.8
`[R-ERR-02]`; §7.2 `[R-CNT-13]`.

**Quotations.**

§21.3, L1 and L2 (Instances columns):

> | L1 | A u64 offset, length, extent, or count field of a layer record holds a value above 2^63 - 1 | layer record extent_offset; layer record extent_length; sub-record extent_offset; sub-record extent_length; dimension extent Eᵢ; tile extent Tᵢ; entry_count; slab run length S | … |
> | L2 | A declaration-derived sum or product of a layer exceeds 2^63 - 1 although every contributing field is in domain | extent_offset + extent_length; N = ∏⌈Eᵢ/Tᵢ⌉; P = ∏Tᵢ; N·P; C·N (which dominates the max disk ordinal (C−1)·N + (N−1)); P·Q (which dominates V = P·C); P·Bᶜ; entry_count × 20 + ⌈entry_count/2¹⁶⌉ × 4 | … |

§21.1:

> An instance names a field the condition ranges over, a container it can occur
> in, one of several alternatives the condition text states, or any combination
> of the three … One instance is one *distinguishable* file

§21.8:

> Every row of §21.2 through §21.5 — 125 conditions over 252 instances — has at
> least one conformance vector (§24) whose expected verdict is that row's
> outcome, and one vector per instance.

**What is wrong.** `[R-CNT-13]` makes an overflowing extent-slot sum a layer-
scope error for both a layer record's own slot and a sub-record's slot ("a
validity error at the scope the record governs (§7.3): the layer for a layer
record and for sub-records"). L1, L16, L17 and L18 all treat those two
containers as separate instances. L2 does not: its "extent_offset +
extent_length" is one instance. Collapsing the two *fields* of the sum is
correct and §21.1 says so; collapsing the two *containers* is the axis L1 uses
four times in the very next-door cell. Two distinguishable files exist, and
under `[R-ERR-02]`'s "one vector per instance" only one gets built.

The register is not uniform on the alternatives axis either, in the opposite
direction: T3's cell enumerates longer/shorter for each of three decoded-size
formulas although its condition text states one equality, while L42's cell is
"—" although its condition text explicitly states three alternatives ("gap,
overlap, or out-of-ordinal placement"). Both are individually defensible under
§21.1's "without the condition changing shape" clause; I note them only to show
that the instance criteria are being applied by judgement rather than
mechanically, which §21.1 half-concedes ("mechanical once the cell is
written").

**Which governs.** §21.1's instance rule governs the cell, so the cell is the
thing to fix; the stated totals are correct arithmetic over the cells as
written, and I verified that they reproduce exactly. Correcting L2 would move
§21.3 to 103 instances and the document total to 253.

**Byte-level: no.** Instance counts drive corpus construction, not file
validity or reader behaviour. Both files are reject-layer either way; only one
of them gets a vector.

---

### register-05 — CONTRADICTION — `[R-ERR-05]`'s hard-limit inventory omits §16.1's alignment floor and mis-attributes the 255-byte cap on user-metadata keys

**Location.** §21.9 `[R-ERR-05]`; §16.1 `[R-SLB-01]`; §7.4's layer-record
table; §18.2 `[R-MTA-04]`; §21.5 R10.

**Quotations.**

§21.9:

> Some limits are instead **hard**: a file violating one is invalid, not merely
> large. They are stated where the structures forcing them are defined — a name
> at most 255 bytes (`[R-ENC-12]`, a `u8` length prefix); rank at most 255 and
> channel count at most 65,535 (§7.4's `u8` and `u16` fields); a layer
> declaring codec 4 at decoded tile size at most `0x7E000000` (`[R-COD-07]`);
> and every offset, length, extent, and count at most 2⁶³ − 1 (`[R-ENC-03]`).
> Each is a consequence of a field's width, an external format, or the value
> domain — never a number chosen here. `[R-ERR-05]`

§16.1:

> A layer MAY declare alignment A (§7.4): a power of two with
> 512 ≤ A ≤ 2⁶². Writers MUST NOT emit any other nonzero value; a reader MUST
> treat one as a validity error at layer scope (`[R-CNT-23]`).

§18.2, fourth restriction:

> and every key satisfying §4.6's name rules — non-empty, at most 255 bytes,
> free of U+0000 through U+001F.

**What is wrong.** Two counterexamples to the closing sentence, and two
omissions from the list it closes.

1. The 512 floor on per-tile alignment is a hard limit — a layer declaring
   A = 256 is invalid at layer scope, and L40 registers "A below 512" as one of
   its three instances — and it is a number chosen in this document, as §16.1's
   own note says ("512 is the legacy sector floor"). No field width, external
   format or value domain forces it. It is absent from the inventory, as is
   A_slab's power-of-two-in-1…2⁶² constraint.
2. The 255-byte cap is attributed to "a `u8` length prefix". That derivation
   holds for layer, dimension and channel names, whose §7.4 encodings are
   `u8 len + bytes`. It does not hold for user-metadata keys, which §18.2
   subjects to the same cap and which are JSON strings with no length prefix.
   R10 registers a longer key, and §21.5's preamble makes every row there a
   violation ("Every row here is a violation all the same"), so the cap is hard
   there too — and chosen here.

**Which governs.** §16.1, §7.4 and §18.2 define the limits; §21.9's inventory
restates them, and by §21.1's principle — which §10.4's `[R-EXT-05]` states in
the same terms for the registry, "the section that defines the space governs" —
the defining section wins. So the limits themselves are not in doubt; the
inventory and its closing generalisation are wrong.

**What an implementer does wrong without it.** Nothing at validation time:
§16.1 and L40 fully determine A, and §18.2 and R10 fully determine keys. The
cost is to anyone using §21.9 as the promised single index of limits —
`[R-ERR-03]` opens with "Every limit affecting which files are valid, or which
files a conforming reader accepts, lives here" — who will not find the
alignment floor there and will conclude from the closing sentence that no such
chosen number exists.

**Byte-level: no.** Every file's fate is already fixed by the defining
sections and by L40 and R10.

---

### register-06 — OBSERVATION — `preserve-verbatim` is defined in §2.4's outcome vocabulary and never used anywhere else in the document

**Location.** §2.4; §20.4 (where it would be used).

**Quotations.**

§2.4:

> **preserve-verbatim** names an updater obligation, orthogonal to reader
> outcomes: a record a reader ignores can still be one an updater preserves.

and, in the same table:

> | **preserve-verbatim** | Binds updaters: the bytes are carried forward unmodified (relocated only as Part I permits). |

§20.4, the place the term would attach, states the obligation without it:

> | MU = 0, PE = 1 | Retain byte-identical, extent content unmodified. |

**What is wrong.** `grep` over the document finds the string `preserve-verbatim`
exactly twice, both inside §2.4. The document defines a fifth member of its
outcome vocabulary, states that it binds updaters, and then never assigns it to
any record, record class, flag combination or rule. §20.4 carries the whole
substance in prose and via `[R-WRT-05]`'s "MUST re-emit byte-identically".
Checking that every defined outcome value is reachable is part of my charter;
this is the one that is not.

**Which governs.** Nothing is in tension — §20.4's table and `[R-WRT-05]`
determine the updater's obligations completely, and §21 correctly carries no
preserve-verbatim rows, since §21's outcomes are reader outcomes. This is
vocabulary hygiene: either bind the term in §20.4 (the PE = 1 and MU = 1 rows
*are* preserve-verbatim) or drop it from §2.4's table.

**Byte-level: no.** No behaviour depends on the term existing.

---

## 8. Things I checked and did not report

Recorded so a reader can see the shape of the negative space.

- **All stated totals reproduce.** 39/50/26/10 conditions, 125 conditions,
  252 instances. Verified by hand and by script; the two agree.
- **All four CRC constants verify** against §4.5's parameters, including the
  all-sentinel segment constant L39 names.
- **§15.3's eleven-row entry-validity table maps one-to-one onto the register**
  (T6, T7, T10, T8, T11, T12/T9, T1, L19, F36, L41–L43, with the sentinel row
  in §21.6). No row of that table is unregistered, and no T row invents a
  condition it does not contain.
- **`[R-CNT-06]`'s ten trailer gates each have a row** (F10, F16, F19, F15,
  F11, F18, F12, F13, F14, F17), with generation's upper bound at F3.
- **The value-space rows match `[R-EXT-03]`'s per-space routing exactly**,
  including the two spaces where an experimental value is not a violation.
- **The F/L partition of shared rules is correct**, including the deliberate
  exception at F32 (framing overrun is file scope even for a layer record,
  because `[R-CNT-12]` scopes it to the sequence, not to the record).
- **The three explicit "no register row" notes each hold**: §7.4's on
  sub-record nesting, §16.2's on a stale slab declaration, §9.5's on residue
  past a completed commit. I followed each argument and could not break it.
- **§5.2's note that "belongs to no coverage class" is unexhibitable** holds:
  the live state is defined as what the walk reaches, and `[R-LIF-08]` makes
  everything else slack.
- **F36's claim that out-of-bounds claimants are caught at open by
  F11/F12, F34/F35, L17/L18 and T8/T9** is complete: I enumerated the claimant
  kinds (directory, top-level record extents, layer-record and sub-record
  extents including the index region, stored-tile extents) and each has a
  bounds row on both sides.
- **T17/T18 overlap** on the instance "a skippable frame before the frame",
  which necessarily also fails the first-four-bytes magic test. §21.1 does not
  list it as a specialization pair, but `[R-VEC-02]` already provides for
  conditions that cannot be isolated ("the entry records every row the file
  exercises and says which it was built for"), so I did not raise it.
- **§21.1's note that verifier rows' outcomes are not reader obligations**
  names `[R-SER-08]` and `[R-CNT-22]` as the rows where the reader must serve
  the structure unchanged. `[R-MTA-05]` (F30, L49) is a third such row and is
  not named, but the sentence reads as illustrative ("for several such rows"),
  so I did not raise it.
- **§21.7's second paragraph enumerates five undetectable obligations by
  identifier** while several others (`[R-CNT-08]`'s updater copy-forward,
  `[R-WRT-05]`–`[R-WRT-09]`) fall in the same class. §21.1 describes §21.7 as
  "the account, by class", and every unnamed one falls in the stated class
  ("properties of a file's history"), so I did not raise it.
- **Appendix H's verifier checklist omits `[R-CNT-05]`'s "no structure between
  the directory's end and the trailer" check** (F9's rule). Appendix H is
  explicitly non-normative and explicitly a summary whose "authority is the
  requirement or section cited, never this summary", and Appendix H is not my
  charter, so I did not raise it.

## 9. Confidence

High that §21's arithmetic is sound and that its coverage of the document's
detectable violations is essentially complete: I found one omission
(register-03), and it is a cause row whose every instance is already caught.
High that no register row would send a conforming implementation to the wrong
bytes or the wrong accept/reject verdict — §21.1's "the rule governs" clause is
doing real work, and every mismatch I found is resolved by it plus one other
place in the document. Lower on the F21 question only in the sense that it is
the one place where a hasty implementer could reach a wrong *verifier verdict*;
I judged it decided by §2.3 and §21.6, and said so.
