# Audit transcript — the register repairs (hunks 05, 07, 09, 18, 19, 20)

## 0. Disclosure

Read: the six hunk files named in my charter under
/private/tmp/claude-501/-Users-robertkleffner-Documents-GitHub-tarn-first-draft/r31-audit/case/
(hunk-05.diff, hunk-07.diff, hunk-09.diff, hunk-18.diff, hunk-19.diff, hunk-20.diff), and
/Users/robertkleffner/Documents/GitHub/tarn-first-draft/spec/tarn.md (4770 lines) — the passages
named below via sed/grep. I did not read full.diff, any other hunk, docs/, conformance/,
registry.json, git history, or the web. I did not list the case directory.

Wrote: /private/tmp/.../r31-audit/scratch/the-register-repairs/count_instances.py (instance
counter) and this file.

Path discrepancy: the brief says my scratch directory "already exists". It did not
(`MISSING .../scratch/the-register-repairs`; `.../scratch`, `.../out`, `.../case` existed).
I created it with mkdir -p and used it. The first attempt to write the counter script failed
on the missing directory; no other lane's file was present or executed.

Unrequested context: my runtime placed a project-instruction pointer (CLAUDE.md → AGENTS.md),
an index of four auto-memory notes about this project (their titles only), a git status block
naming five recent commit subjects, and a date. None was used as evidence; I did not open
AGENTS.md or the memory files. The commit subjects mention ADR numbers and prior audit
outcomes; I disregarded them.

Header/body check: every hunk header's landing line matches the body in the current file
(1998–1999, 2502–2503, 2698–2701, 3745, 3766, 3884 — verified by sed).

## 1. Passages read (by line)

- §2.3 [R-CNF-02]/[R-CNF-03]/[R-CNF-11] 152–260; §2.4 [R-CNF-07..12] 290–336; §2.5 336–345
- §4.2 [R-ENC-03], [R-ENC-04] 440–500
- §7.2 [R-CNT-12]/[R-CNT-13] 990–1035; §7.4 layer record table 1076–1100; [R-CNT-23],
  [R-CNT-16], [R-CNT-17], [R-CNT-18] 1100–1140
- §11.2 [R-GEO-03] 1640–1670; §11.4 [R-GEO-06] 1697–1744; §12.1 1752–1797
- §14.1 tail / §14.2 whole / §14.3 / [R-SER-07] / §14.4 1960–2113; §17.2 2440–2530;
  §17.3 stride 2530–2545
- §18.1 2584–2604; §18.2 whole 2604–2740
- §19.1–19.3 2862–2983; §20.3 excerpts 3220–3230, 3245–3265
- §21.1 3597–3683; §21.2 3683–3737; §21.3 3737–3794; §21.4 3794–3831; §21.5 3831–3865;
  §21.6 3865–3920; §21.7 3920–3977; §21.8 3977–3984; §21.9 3984–4076; §24 Note 4340–4350

## 2. Sweeps run (verbatim grep, hit counts)

- `grep -n 'P·Q\|P · Q'` → 9 hits: 1993 (table), 1999 (hunk 5), 2502 (hunk 7), 3745 (L2),
  3787 (L44), 3806 (T3), 3817 (T14), 3824 (T21), 3825 (T22). No hit states P·Q for a planar layer.
- `grep -n 'C·N\|C · N'` → 4: 1661 (R-GEO-03), 3226 (§20.3), 3745 (L2), 3764 (L21).
- `grep -n 'P·Bᶜ\|P · Bᶜ'` → 8: 1992, 2502, 3745, 3787, 3806, 3817, 3824, 3825.
- `grep -n '⌈P/8⌉'` → 7: 2051 (§14.3), 2099 (§14.4 Note), 3787 (L44), 3806 (T3), 3817 (T14),
  3824 (T21), 3825 (T22). NOT in L2 (3745) and NOT in hunk 7's Note (2502).
- `grep -n 'capability refusal'` → 1: 4026 ("capability refusals §21.6 names").
- `grep -n 'narrowest'` → 4: 2699 (hunk 9), 3884 (hunk 20), 4021 (R-ERR-04), 4343 (§24 Note).
- `grep -n 'whole file'` → 10; relevant: 2700 (hunk 9), 3884 (hunk 20), 4021 (R-ERR-04).
- `grep -n 'sample stride\|stride Q'` → 3: 1996, 2537, 3829 — Q used only for interleaved.
- `grep -n 'the two capability\|names the other two\|Two structural'` → 184, 3899 (and 4026
  found by the previous sweep; "the two\ncapability" wraps at 4025/4026).
- `grep -c 'ignore-record'` → 20 hits, listed in transcript above; every ignore-record
  non-violation now has a §21.6 row (experimental encoding 3881; unassigned type MU=0 row;
  decline-on-bound 3884). No other ignore-record non-violation found.
- `grep -n 'resource limit'` → 4: 340, 2701 (hunk 9), 3884 (hunk 20), 4029 (R-ERR-04).
- `grep -n 'Window_Size'` → 10 (2457, 2462, 2464, 2633, 2648, 2657, 2660, 2667, 3884, 4005).
- `grep -n 'proceeds'` → 2: 2698 (hunk 9), 2989 (§19.4, unrelated).
- `grep -n 'declin'` → 20 hits; relevant 2459 (R-COD-06 "the tile or the layer"), 2655, 2677–2690
  (verifier), 2699–2700, 3841, 3884, 3913, 4021–4024.
- `grep -n 'stated or derived'` → 1: 4022.
- `grep -n 'treats any of them'` → 0. CONTROL: `grep -n 'treats any'` → 3867 and
  `grep -n 'of them as a failure'` → 3868: the phrase wraps at "any\nof". Zero was a wrap
  artefact; the sentence exists at 3867–3868.
- `grep -n 'every quantity it designates'` → 1: 2501 (hunk 7 Note).
- Controls proving the grep instrument: `grep -c 'sample-position count per tile'` → 2;
  `grep -c 'no such quantifier'` → 1; `grep -c '1 for bool'` → 1.

## 3. Derived numbers

- Register totals via count_instances.py (rows matching `^| [FLTR]\d+ |`, instances =
  semicolons+1, "—" = 1): F 35 conditions / 56 instances; L 49 / 116; T 26 / 55; R 10 / 50.
  Total 120 conditions / 277 instances. §21.8 states "120 conditions over 277 instances" — match.
  §21.2 says 35, §21.3 says 49, §21.4 says 26, §21.5 says 10 — all match.
- L2 instance count after hunk 18: 9 (extent sum; sub-record extent sum; N; P; N·P; planar C·N;
  interleaved P·Q; planar numeric P·Bᶜ; entry_count formula). Before (from the hunk's "-" line):
  9. Unchanged.
- L23 instance count: 4 before and after (hunk 19 edits only the Detected cell).
- Dominance arithmetic in L2: (C−1)·N + (N−1) = C·N − 1 < C·N ✓. V = P·C ≤ P·Q since
  Q = ΣBᵢ with every Bᵢ ≥ 1 ✓. Planar V = P (§14.1), listed as P ✓. Interleaved max disk
  ordinal = N−1 < N ✓. Packed planar bool ⌈P/8⌉ ≤ P — cannot exceed 2⁶³−1 unless P does,
  so it is not a distinguishable L2 file (§21.1 "no two files could differ").
- §21.6 capability refusals now named: foreign format major (prose), unimplemented MU = 1
  top-level type (prose), resource decline on a document (new row 3884) = 3. R-ERR-04 says "the
  two capability refusals §21.6 names".
- Planar-bool worked case for hunk 5/7/18: P = 2⁵⁹, channels 4 × float64 planar → each
  P·Bᶜ = 2⁶² (in domain), P·Q = 2⁶⁴ (would overflow). After hunk 5 the layer forms no P·Q
  (conforming on this ground); before, a reader could have read L2's untagged P·Q as reaching it.

## 4. Per-hunk audit

### Hunk 05 — §14.2, [R-SER-02] sentence (normative prose, not in any blockquote)
Rule adopted: the designated declaration-derived quantities of §14.2's table are per layout —
an interleaved layer designates P·Q (and the sums Q, Fᶜ); a planar layer designates P·Bᶜ per
numeric channel and nothing called P·Q. A reader checks only the quantity its layer's row states.
1. Tense/quantifier: layer-level, present declarations; matches [R-ENC-04] ("any quantity this
   specification designates … A designation is express, made by the section that defines the
   quantity") and [R-SER-07] ("Every decoded size … under [R-ENC-04]"). This sentence IS the
   express designation. PASS.
2. Citations: [R-ENC-04] (line 477) — states the designation model the sentence invokes. PASS.
   [R-SER-02] is the sentence's own id.
3. Label: the sentence sits in ordinary prose after the table; not in a blockquote. Normative. PASS.
4. Contradiction in passage: §14.2's opening restricts the section to numeric planar tiles and
   every interleaved tile, so the planar-bool plane (§14.3, ⌈P/8⌉) is outside "these products";
   [R-SER-07] designates it separately. §17.3 uses Q only for interleaved (line 2537). §19.3
   cites "the decoded sizes §14 derives ([R-SER-02], [R-SER-07])". No collision. PASS.
5. Exhaustive claims: "a planar layer has no P·Q to form" — grep shows no rule designating P·Q
   for a planar layer. PASS.
6. Unconstrained siblings: table quantities are P·Bᶜ, P·Q, k·Bᶜ, (k div C)·Q + F. The offset
   expressions are ≤ the decoded size and never exceed it; the sums Q ≤ 65535·8. Nothing left
   reachable-and-unpinned. PASS.
7. Analogy: none. N/A.
8. Insertion effects: following sentence "That rule fixes what such a reader returns" refers to
   the [R-SER-08] sentence in its own paragraph; unaffected. "its row" in the inserted text: Q and
   Fᶜ have no row of their own, but appear only in the interleaved row's cells — resolvable.
Byte-level: the repair moves one class of file (planar, P·Q overflows, no P·Bᶜ overflows) firmly
to "no L2 violation"; both readings now agree because this sentence is the normative
designation. No finding.

### Hunk 07 — §17.2 Note under [R-COD-07] (block labeled "> **Note.**", non-normative)
Rule restated: [R-ENC-04] binds designated quantities of a layer whether or not it addresses a
tile, so the layout's decoded-size quantity is overflow-checked even in an empty layer.
1. Quantifier "every quantity it designates, whether or not the layer addresses a tile" matches
   [R-ENC-04] ("any quantity this specification designates") and §20.3 line 3257 ("[R-ENC-04]'s
   2⁶³ − 1 ceiling on every quantity it designates … which an empty layer escapes only because
   that cap is quantified over addressed tiles"). PASS.
2. Citations: [R-ENC-04] ✓, [R-GEO-02] ✓ (extent 0 = valid empty layer), §11.2 ✓, §21.6 row
   "A dimension has extent 0" ✓. PASS.
3. Label: "> **Note.**" at 2490 — non-normative; the normative statements are [R-SER-02]
   (hunk 5), [R-SER-07], [R-ENC-04]. Consistent with them. PASS.
4. Contradiction: §21.9 "A layer addressing no tile therefore has no tile whose decoded size the
   table bounds" — about the guarantee row, which the Note explicitly contrasts. No collision.
5. Exhaustive claim: "the decoded size the layout gives, P·Q or P·Bᶜ" — presented as the closed
   pair of decoded sizes the layout gives. §14.3 gives a third, ⌈P/8⌉ for a planar bool channel,
   and [R-SER-07] designates "every decoded size". Also a planar layer gives one decoded size
   per channel, not "the decoded size". → FINDING D-01 (OVERCLAIM, Note, not byte-level:
   ⌈P/8⌉ ≤ P and P is checked, so no file's verdict turns on it).
6. Siblings: decoded sizes per layout: interleaved P·Q; planar numeric P·Bᶜ; planar bool ⌈P/8⌉.
   The Note names two of three (see D-01). L2 names two of three but ⌈P/8⌉ is dominated by P.
7. Analogy: "no such quantifier" contrasts [R-ENC-04] against [R-COD-07]'s "any of whose
   addressed tiles". Verbs: [R-COD-07] "a layer any of whose addressed tiles' decoded size
   exceeds" vs [R-ENC-04] "any quantity this specification designates … whose mathematical value
   would exceed". Different sets by design; the Note's point is exactly that. PASS.
8. Insertion effects: next paragraph "the stored bytes MUST decode to exactly the decoded size"
   — "the decoded size" is generic; unchanged.

### Hunk 09 — §18.2 Note after [R-MTA-09] (block labeled "> **Note.**", non-normative)
Rule restated: a document exceeding the reader's (≥ 16 MiB) bound → the reader that stays with
the file takes ignore-record for that record, which is the narrowest scope [R-ERR-04] allows;
it may instead decline the whole file; either is reported as a resource limit.
1. Actor: reader; set: that record / the whole file. Matches [R-ERR-04] "a reader MAY decline it
   — at the whole file, or at the narrowest scope … the record carrying a user-metadata document,
   as §18.2 assigns" (4020–4023). PASS.
2. Citations: [R-ERR-04] ✓ names the record (4022–4023). [R-CNF-03] ✓ "none of whose values
   exceeds the minimum guarantees" (181–183). PASS.
3. Label: Note — non-normative; body [R-MTA-09] states "a document exceeding that bound is
   ignore-record" (2626), "the reader MAY decline it ([R-ERR-04])" (2655), and R-ERR-04 states
   the whole-file option and the reporting rule (4028–4032). Repair lands nowhere normative and
   need not: every claim has a normative home. PASS.
4. Contradiction: body speaks of both proceeding (ignore-record) and declining (MAY decline it);
   the verifier passage (2677–2690) says the decline is not a finding of nonconformity — matches
   "not as corruption". §24 Note (4343) speaks of [R-CNF-12]'s licence for nonconforming files;
   here the file is conforming and the licence is [R-ERR-04]'s — the Note cites the right one.
   PASS.
5. Exhaustive: "the narrowest scope" — R-ERR-04's list has no scope narrower than the record for
   a document. "Either refusal" — two options, R-ERR-04 states exactly two. PASS.
6. Siblings: the two grounds are decoded size and Window_Size; the Note names the 16 MiB figure
   only, but §21.6's new row and the body cover both. Acceptable for a Note.
7. Analogy: "compose here as they do elsewhere" — unchanged text. N/A.
8. Anaphors: "that record" → the record whose document decodes to more than the guarantee
   (previous sentence, unchanged); "which" → that record; "it" → the reader. Following paragraph
   has no back-reference into the Note. "A reader that proceeds": previously contrasted with
   "declines … at the whole file"; now still contrasted with "decline the whole file". Considered
   as a new ambiguity (could "proceeds" mean proceeds to decode past its bound?) — rejected: the
   body defines the bound as the reader's own, so a reader that decodes has no excess; the
   only reading that leaves "takes ignore-record" true is "proceeds with the file".
No finding.

### Hunk 18 — §21.3 L2 Instances cell (register row, normative but "the rule governs")
Rule restated: the L2 overflow instances are layout-tagged — C·N is the planar addressed-tile
count, P·Q the interleaved decoded size, P·Bᶜ the planar numeric decoded size.
1. Quantifier: "A declaration-derived sum or product of a layer" — layer-level, no addressed-tile
   quantifier; matches [R-ENC-04] and hunk 7's Note. PASS.
2. Citations: [R-ENC-04] ✓; R-GEO-03 ✓ designates N, P, N·P, addressed count (N interleaved,
   C·N planar); R-CNT-13 ✓ (extent sums); R-SER-02 ✓ (P·Q, P·Bᶜ); R-SER-07 ✓ (every decoded size,
   V). PASS.
3. Label: table row in §21.3; normative restatement, rule governs (§21.1). PASS.
4. Contradiction: tags agree with L21 ("N interleaved, C·N planar"), L44/T3/T14/T21/T22
   ("interleaved P·Q; planar numeric P·Bᶜ; packed planar bool ⌈P/8⌉"), §11.2, §14.2. PASS.
5. Exhaustive: the cell is a closed enumeration; instance count 9 unchanged (derived above).
   ⌈P/8⌉ absent but dominated by P (no distinguishable file). PASS.
6. Siblings: every quantity §11.2/§14.2/§14.3/§7.4/§15.1 designates is either listed or
   dominated by a listed one (disk ordinal by C·N or N; V by P·Q or P; ⌈P/8⌉ by P). PASS.
7. Analogy: "which dominates" twice — both verified arithmetically above. PASS.
8. Insertion effects: cell-internal; no anaphors. PASS.
No finding.

### Hunk 19 — §21.3 L23 Detected cell
Rule restated: a truncated name is detected at open (§19.1 step 4); every other region at layer
access.
1. Actor: reader; tiers per §19.2. §19.1 step 4 (2887–2893): "a layer record whose name field
   does not lie entirely within that record's inline_length yields no name field … is instead a
   validity error at layer scope ([R-CNT-18])" — at open ✓. §19.3: first access is "the first
   operation using any of the layer's declarations other than its name, whose parse §19.1 step 4
   places at the open" and requires "the exact parse" — layer access for the rest ✓. PASS.
2. Citations: §19.1 step 4 ✓ says exactly that. [R-CNT-18] ✓ (1120–1135). PASS.
3. Label: table row; rule governs. PASS.
4. Contradiction: none with §19.2's tier list ("the layer-name namespace" at open; "full
   validation of that layer's record" at first access). R1 uses the same two-part cell form.
5/6. Partition: the cell's two parts are "the name" and "every other region". The row's own
   Condition and Instances individuate four *regions*: leading fixed fields (name … C), d
   dimension entries, C channel entries, trailing fixed fields. "The name" is not one of those
   four; it is a field inside the first. Read with the row's own vocabulary, "every other region"
   = the three regions other than the one containing the name, and the leading fixed fields
   layout … C fall in neither part. → FINDING D-02 (NEW_AMBIGUITY; not byte-level: §19.3 fixes
   layer access unambiguously and earlier detection is always licensed by [R-RDR-02]).
7. Analogy: none.
8. No anaphors.

### Hunk 20 — §21.6 new row (table entry; §21.1: restates its rule, rule governs)
Rule restated: a document whose decoded size or frame Window_Size exceeds the reader's own bound
(≥ §21.9's guarantee) is ignore-record on capability grounds, reported as a resource limit, the
file conforming, and the reader may instead decline the whole file.
1. Actor: the reader (verifier included, §2.3). Bound: "the reader's own … no smaller than
   §21.9's guarantee" matches 2624–2626 and 2650–2653. PASS.
2. Citations: [R-MTA-09] ✓ (both bounds, ignore-record, file conforming, verifier cannot-establish);
   [R-ERR-04] ✓ (record scope named, whole-file option, resource-limit reporting). §21.9 ✓ rows
   "decoded size of one user-metadata document 16 MiB" and "zstd frame Window_Size 8 MiB". PASS.
3. Label: table entry in §21.6, not a Note. The normative statements live in [R-MTA-09] and
   [R-ERR-04]; the row is a restatement. PASS.
4. Contradiction in the same section: §21.6's preamble "These are defined behaviors, not errors.
   A reader that treats any of them as a failure is the nonconforming party." (3867–3868). The
   new row's defined behavior includes "the reader MAY instead decline the whole file" — a
   whole-file refusal that the preamble, read literally, brands nonconforming. Every earlier table
   entry is a condition a reader serves through; the two refusal cases were kept out of the table
   and put in prose. → FINDING D-04 (LOCAL_CONTRADICTION; not byte-level: R-ERR-04 governs and
   its MAY is unambiguous).
5. Exhaustive: "the narrowest-scope decline" ✓ (R-ERR-04 names the record). "§21.9's guarantee"
   singular over two quantities — read distributively; body is explicit per quantity; rejected.
6. Siblings: the verifier's side (cannot establish, MUST NOT certify) is not stated in the row
   while the experimental-encoding row does state its verifier outcome — rejected as a finding
   since [R-MTA-09] governs and §21.5's preamble already says "a reader or verifier declines".
7. Analogy: none in the row.
8. Insertion effects, forward to end of subsection: "exactly as for an unrecognized key above"
   (row before; backward, unaffected). "Two conditions that once sat in this table … registered
   above" (unaffected). "Two structural cases are conforming files a reader nevertheless refuses"
   — count unchanged because "structural" excludes the resource ground, and [R-CNF-03] (184)
   already separates them. "Neither is a register row" — still true (§21.6 is not the register).
   Restatement sweep outside the section: [R-ERR-04] (4025–4027) "the two capability refusals
   §21.6 names, a foreign format major and an unimplemented MU = 1 type, are not this ground" —
   §21.6 now names a third capability refusal, and it IS this ground. → FINDING D-03
   (UNSWEPT_RESTATEMENT; not byte-level).
   §21.5 preamble sentence "§21.6 lists the ignore-record conditions that are not violations"
   (3849): before this row §21.6 omitted the decline-on-bound condition that §21.5's own
   preamble (3840–3843) carves out; now listed. The sentence is now true (ignore-record sweep
   found no other unlisted ignore-record non-violation). PASS.

## 5. Findings (4)

D-01 hunk 07 OVERCLAIM — Note's "the decoded size the layout gives, P·Q or P·Bᶜ" omits the
     planar bool plane's ⌈P/8⌉ (§14.3, designated by [R-SER-07]) and treats a planar layer's
     per-channel sizes as one. Not byte-level.
D-02 hunk 19 NEW_AMBIGUITY — "layer access (every other region)" leaves the non-name leading
     fixed fields (layout … C) in neither part when "region" is read as the row's four regions.
     Not byte-level.
D-03 hunk 20 UNSWEPT_RESTATEMENT — [R-ERR-04]'s "the two capability refusals §21.6 names …
     are not this ground" is false once §21.6 names a third that is this ground. Not byte-level.
D-04 hunk 20 LOCAL_CONTRADICTION — §21.6 preamble "A reader that treats any of them as a
     failure is the nonconforming party" vs the row's licensed whole-file decline. Not byte-level.

## 6. Rejected candidates

- L2 omits packed planar bool ⌈P/8⌉ while L44/T3/T14/T21/T22 list it — dropped: ⌈P/8⌉ ≤ P and P
  is an L2 instance, so no distinguishable overflow file exists (§21.1's instance rule).
- Hunk 5 "its row" for the sums Q and Fᶜ, which have no table row — dropped: both appear only in
  the interleaved row's cells, and §17.3 confirms Q is interleaved-only.
- Hunk 9 "A reader that proceeds" — dropped: the only reading under which "takes ignore-record"
  is true is "proceeds with the file", the same contrast the old text drew.
- Hunk 20 "§21.9's guarantee" singular over two quantities — dropped: [R-MTA-09] is explicit per
  quantity and §21.1 makes the rule govern; a reader applying one bound of 16 MiB to both is
  merely more permissive, and one applying 8 MiB to documents is already nonconforming under
  R-ERR-04's own words.
- Hunk 20 row silent on the verifier's cannot-establish — dropped: [R-MTA-09] states it;
  §21.5's preamble names "a reader or verifier"; the §21.6 preamble's "reader" includes verifiers.
- Hunk 20 row "the file is conforming" as an absolute — dropped: same idiom as the ignore-lane
  and experimental-encoding rows; read as "conforming on this ground".
- R-ERR-04's own wording "narrowest scope whose stated or derived quantities exceed" against a
  document's decoded size, which is neither stated nor derived — R-ERR-04 delegates "as §18.2
  assigns"; not in my hunks; noted only.
- [R-COD-06] (2459) "decline the tile or the layer" vs R-ERR-04's "whole file, or narrowest" —
  pre-existing, tile-side, outside these six hunks; noted only.
- Hunk 7 vs §21.9 "no tile whose decoded size the table bounds" — dropped: the Note's whole point
  is that [R-ENC-04] carries no addressed-tile quantifier, and [R-SER-02]/§19.3/§20.3 agree.
