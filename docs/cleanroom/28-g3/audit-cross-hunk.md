# Cross-hunk consistency audit — ADR-0113 repair set (8 hunks)

## Disclosure

Read: all eight hunk-NN.diff files in the case directory (01..08); `spec/tarn.md`
(§11.1, §11.2, §11.4/[R-GEO-06], §12.1, §14.5, §19.3, §9.7, §20.3 in full,
§20.4 excerpt, §7.4 layer-record field table, §21.2–21.5 rows greppd, §21.7 in
full, §21.9). Did NOT read full.diff, docs/, PLAN.md, OPEN-QUESTIONS.md,
AGENTS.md, README.md, conformance/, registry.json, git history, or the web. Did
not list the case directory beyond globbing `hunk-*.diff`.

Context I did not ask for DID appear before I began: a project instruction file
(CLAUDE.md pointing at AGENTS.md), a user auto-memory index naming two memory
notes, and a git status/recent-commit listing whose subject lines mention
"ADR-0113 audit" runs and defect counts. None of it is the specification and
none of it is evidence about the specification. I did not open any of the named
files and did not use the commit subjects to steer any conclusion; every finding
below is anchored to a line of spec/tarn.md or a hunk file I quote.

## Header verification

Every hunk's stated "nearest preceding heading" was checked against the body:

- hunk 1 → line 1584 "11.1 Geometry and its validity floor" — VERIFIED (the
  changed text is inside the `> **Rationale.**` block at 1602–1628, under 11.1).
- hunks 2,3,4,5,6 → line 3073 "20.3 The append procedure" — VERIFIED. Note that
  hunk 6 lands not in step 4 but in the `> **Example — the three shapes a commit
  takes.**` block at 3283–3338, which is still inside §20.3.
- hunks 7,8 → line 3862 "21.7 What no check detects" — VERIFIED.

No mismatch.

## [R-CNF-01] label test, applied per hunk (marker NOT used)

- hunk 1: block opens `> **Rationale.** Empty layers serve schema-first
  workflows` → labelled *Rationale* → NON-NORMATIVE.
- hunk 6: block opens `> **Example — the three shapes a commit takes.**` →
  labelled *Example* → NON-NORMATIVE.
- hunks 2,3,4,5: numbered step 4 of §20.3, no blockquote, carries `[R-WRT-04]`
  at the end of step 6 → NORMATIVE.
- hunks 7,8: §21.7 running prose, no blockquote, paragraph closes with
  `[R-ERR-01]` → NORMATIVE.

So the two normative bars live in hunks 2/3/4/5 and their consequences in 7/8;
hunks 1 and 6 are unenforceable restatements. That matters for direction: where
1 or 6 disagrees with 3/4/5, the Rationale/Example is the side that must change.

## The grouping (by rule, not by section or commit)

**Group I — the §14 bar (naming + scope).** hunks 2, 4, 5, 8, and the
restatements in 1 and 6. Rule: a commit MUST NOT change a layer's declarations
in a way that alters, for any tile that layer stores *in the generation this
commit supersedes*, what §14 fixes for its stored bytes or how they decode.
Hunk 2 gives it the name. Hunks 4 and 5 replace the anaphors "the bar above" /
"the bar" with the name and re-admit the other obligations a shrink is under.
Hunk 8 does the same swap in §21.7. Hunks 1 and 6 restate it outside §20.3.

**Group II — the §14 bar's reach over a channel's sample type.** hunk 3 (first
inserted paragraph), hunk 1 ("Re-typing a channel is the §14 bar's own
subject"), hunk 7 (the witness claim for a re-typed channel). Rule: re-typing a
channel is a §14-bar change wherever the superseded generation stored a tile
carrying that channel.

**Group III — the new companion bar on planar disk ordinals.** hunk 3 (second
inserted paragraph, the MUST NOT), hunk 1 ("The other bar reaches neither a
shrink nor a growth"), hunk 5 ("The bar beside the §14 bar does not reach a
shrink either"), hunk 7 ("Its companion bar on a planar layer's disk ordinals").
Rule: for a planar layer, a commit MUST NOT change the channel declarations in a
way that alters the disk ordinal [R-GEO-06] assigns any tile stored in the
superseded generation.

**Group IV — the empty-layer re-declaration permission and its tense.** hunk 3
("the tense is both bars'"), hunk 1 ("a layer the commit itself empties does not
qualify"), hunk 6 (same sentence in the Example). Rule: only a layer that stored
no tile in the *superseded* generation may be re-declared freely.

Groups I and III are the ones where two repairs both bound what a rule ranges
over; Group I bounds by *generation of storedness*, Group III bounds by *which
declaration is edited* (channel declarations) plus *layout* (planar). Those are
two different kinds of property, and finding X-04 below is the seam between
them.

## Searches run (hard wrap accounted for: short fragments only)

    grep -n "14 bar" spec/tarn.md                       → 12 hits (1606,1616,
       3140,3175,3214,3231,3236,3240,3896,3911,3935 + none stray)
    grep -n "re-declar\|redeclar"                        → 6 hits (1615,3144,
       3200,3203,3325,3912)
    grep -n "bar above\|the bar is\|the bar has\|this bars\|it bars\|bars it"
                                                         → 11 hits; NO "bar
       above" survives in §20.3 — hunks 4 and 5 swept both anaphors.
    grep -n "disk ordinal\|disk-ordinal"                 → 18 hits
    grep -n "R-GEO-06"                                   → 6 hits
    grep -n "a layer's declarations\|the layer's declarations\|channel declarations\|declaration change\|change a layer"
                                                         → 6 hits
    grep -n "whole-file rewrite\|fresh file_id\|fresh \`file_id\`"  → 12 hits
    grep -n "channel count\|adding a channel\|removing a channel\|channel order\|channel's index"
                                                         → 12 hits (incl. L32 at
       3718, which classifies channel count C as a *layer geometry field*)
    grep -n "supersedes every\|superseding every\|unstoring\|does not escape\|escapes"
                                                         → 6 hits (1541,3143,
       3208,3910,3911,4161)  ← this is the sweep that produced X-01
    grep -n "rows below\|rows above\|table below\|below states\|the rows\b"
                                                         → 7 hits
    grep -n "^| T3 \|^| T14 \|^| T2 \|^| T4 \|^| T5 \|^| T26 "  → 6 rows
    grep -n "R-COD-07"                                   → 6 hits (L44 at 3730)
    grep -n "R-SLB-01\|R-SLB-04"                         → 10 hits (L39, L40)
    grep -n "R-CNT-21\|R-CNT-22"                         → 19 hits
    grep -n "^#### 21\.\|^### 21\."                      → 10 headings; §21.2–21.5
       occupy 3626–3807, §21.7 begins 3862  ← this is the sweep behind X-09
    awk 'NR>=3116 && NR<=3263' | grep "MUST\|SHOULD\|MAY"  → exactly two MUST NOTs
       in step 4 (3133 "A commit MUST NOT change a", 3179 "commit MUST NOT change
       the channel declarations"), plus two MAYs and one SHOULD. Confirms hunk 1's
       count of "two bars".

## Citation ledger

| cited | in hunk | verdict |
|---|---|---|
| [R-GEO-06] "disk ordinal is c·N+s / s" | 3 | PASS — line 1700-1703 says exactly that, c = channel's index |
| §11.2 "addressed-tile count C·N" | 3 | PASS — line 1636-1638 |
| §12.1 element sizes; uint8 = 1, bool = 1 | 7 | PASS — table at 1734-1747; bool row element size 1, uint8 row 1 |
| planar bool plane ⌈P/8⌉ vs numeric P·Bᶜ | 7 | PASS — §12.1 closing para ("a planar bool plane is sized by packing (§14.3)") and T3/T14 instance lists |
| T3 | 7 | PASS — row 3749 tests decoded payload byte length against declarations |
| T14 "under codec 1" | 7 | PASS — row 3760 is codec 1 (none) and tests the entry's declared length |
| §14.5 "for each channel the position carries, that channel's fill" | 3 | PASS — §14.5 uses that exact quantifier verbatim |
| [R-COD-07] cap "quantified over addressed tiles" | 3 | PASS — L44 row 3730 says "any of whose **addressed** tiles' decoded size" |
| [R-ENC-04] 2⁶³−1 ceiling | 3 | PASS |
| [R-SLB-04], [R-SLB-01] "obligations this step states below" | 4 | PASS — both appear at 3254-3258, below hunk 4's insertion at 3214 |
| [R-CNT-17] "the smaller entry_count" | 4 (implied), 5 | PASS — 3110-3115 [R-CNT-17] ties entry_count to the geometry-derived addressed-tile count |
| [R-CNT-21] slack | 4, 5 | PASS |
| [R-LIF-01], §20.5 remedy | 3 | PASS |
| §9.7 "which is all §9.7 walks" | 7 | PASS — §9.7 opens "walks the live state only" |
| §11.1 "what schema-first creation needs" | 3 | PASS as a justification, but §11.1's schema-first material is inside the *Rationale* block → non-normative; the cite is to a motive, not a rule, so it lands |
| "the rows below" | 7 | **FAIL** — §21.2–21.5 are at 3626–3807, above §21.7 at 3862. See X-09 |
| "escapes the §14 bar" implied cite to §20.3 step 4 | 7 | **FAIL** — §20.3 line 3142-3145 says the opposite in the same verb. See X-01 |
| "the same step's permission" | 6 | **FAIL/soft** — step 4 attaches "subject to every rule its new geometry is subject to" to a *growth*, not to re-declaration. See X-10 |

## Derived numbers

- Disk ordinal arithmetic in hunk 3's worked example: N = 2, channels (a,b).
  a → c=0 → ordinals 0·2+0 = 0 and 0·2+1 = 1. b → c=1 → 1·2+0 = 2 and 1·2+1 = 3.
  Appending c → c=2 → 2·2+0 = 4 and 2·2+1 = 5, and a's and b's are unchanged.
  Exchanging a and b swaps c=0 and c=1 → all four move. **Hunk 3's example is
  arithmetically correct.**
- Max disk ordinal (C−1)·N + (N−1) — matches L2's parenthetical at 3688.
- uint8 → bool on a planar plane: P·Bᶜ = P·1 = P bytes → ⌈P/8⌉ bytes. For P ≥ 2
  these differ, so T3/T14 fire. **Hunk 7's example is correct, and it is what
  falsifies hunk 7's own earlier blanket claim (X-07).**
- Count of bars in §20.3 step 4: 2 (see awk sweep). Hunk 1's "Of its two bars"
  and hunk 5's "The bar beside the §14 bar" both check out.
- Count of channel-entry fields per §7.4's table: 3 (name, type u16, fill).
  Type is pinned by hunk 3; fill by the §14 bar via "the content [R-SER-05]
  fixes there"; name is unconstrained and harmlessly so. No gap at that level.

## Check 6 — the structure behind the ordinal bar, member by member

Structure governed: the layer record's inline payload, the subset of it that
[R-GEO-06] and §14 read. Members and their governor:

| member | moves a disk ordinal? | governed by |
|---|---|---|
| channel entry: name | no | nothing (harmless) |
| channel entry: type | no (but changes decoded size) | §14 bar, via hunk 3 |
| channel entry: fill | no | §14 bar ("the content [R-SER-05] fixes there") |
| channel count C / channel order | YES, planar | **hunk 3's new ordinal bar** |
| layout (interleaved↔planar) | YES for C ≥ 2 (s ↔ c·N+s) | §14 bar catches it via decoded size (P·Q vs P·Bᶜ); for C=1 numeric the two coincide and the change is a no-op. NOT a gap. |
| dimension entries: extents Eᵢ | YES (N changes) | licensed: re-emission rule's "(a geometry change renumbers ordinals…)" |
| dimension entries: tile extents Tᵢ | YES | same, plus §14 bar via in-tile offsets |
| dimension ORDER (rank d fixed, T's equal) | YES, both layouts (s = Σtᵢ·∏_{j>i}Gⱼ) | licensed by the same parenthetical — NOT a gap, but see X-05 |
| linearization | only value 1 legal | [R-GEO-05] |
| codec / filter | no | §14 bar names both |
| alignment A / slab S | no | [R-SLB-01], [R-SLB-04] via step 4's tail |

The one member whose *consequence* nothing states is the **de-addressing of a
stored plane by dropping a channel** — see X-04.

## Check 8 — back-reference ledger for the inserting hunks

hunk 3, insertion 1 (the sample-type paragraph, 3153–3165):
- "Where a change does reach **them**" (3165-3166). BEFORE: nearest antecedent
  was "every one of those tiles" ≈ every tile stored in the superseded
  generation. AFTER: nearest plural is "a planar channel none of whose own
  **tiles** are stored". **CHANGED → X-06.**
- "Such a change is a new layer" (3170). BEFORE: any §14-bar-reaching
  declaration change. AFTER: reads as a type change. CHANGED, same finding.
- "`[R-LIF-01]` freezes **them** where they lie" — resolves inside its own
  clause to "the originals". Unaffected.

hunk 3, insertion 2 (the ordinal-bar paragraph, 3174–3199):
- "One effect is barred beside **it**" — "it" = the §14 bar (two sentences and
  one paragraph break away); within the SAME sentence "the §14 bar does not
  reach **it**" uses "it" for the effect. Two referents, one pronoun, one
  sentence. Resolvable only because "§14 bar" is spelled out mid-sentence.
  Noted in rejected candidates (survivable, not a defect I would file alone).
- "exactly as above" (3198) → resolves to "Such a change is a new layer, or a
  whole-file rewrite under a fresh file_id" at 3170. Correct, unaffected.
- "the re-emission rule **above**" → resolves to 3121-3128. Correct. But see
  X-05 for what that rule actually already licenses.

hunk 4 (insertion at 3214–3220):
- "the obligations this step states **below**" → 3244 ([R-CNT-21]), 3244
  ([R-CNT-17]), 3251-3258 ([R-SLB-04], [R-SLB-01]), 3247-3251 (the SHOULD).
  All genuinely below. PASS.
- The insertion converted a colon into a full stop, orphaning "A shrink is
  permitted exactly where…" into a free-standing biconditional. **X-02.**

hunk 5 (insertion at 3236–3242):
- "it bars a change to a planar layer's channel declarations" — "it" = "The bar
  beside the §14 bar", named in the same sentence. PASS.
- "§21.7 records the consequence — that **this** is precisely where the §14 bar
  has no witness" — "this" = the unstore-in-the-same-breath case. Unaffected by
  the insertion. PASS.

hunk 7 (insertion at 3896–3913):
- "only for part of what **it** bars — a re-typed channel among the cases **it**
  does not reach". Same pronoun, two referents (the bar; the witnessing).
  **X-07.**
- "**Its** companion bar" → the §14 bar. PASS.
- "the rows **below**" → §21.2–21.5 are above. **X-09.**
- "escapes **them**" → the rows. PASS grammatically; the trailing "as it escapes
  the §14 bar" is **X-01**.
- "Which case a type change falls in" → the two cases of the preceding sentence
  (touches something §14 fixes / does not). PASS, and it is what falsifies the
  blanket claim earlier in the same paragraph.

hunk 8 (single-token swap at 3935): no insertion, no re-resolution. Its own
sentence is the *correct* statement of the case hunk 7 got wrong 24 lines
earlier — see X-01.

## Check 7 — analogy ledger (both verbs quoted)

1. hunk 7: "a commit that supersedes every tile it would have damaged **escapes
   them** exactly as **it escapes the §14 bar**." Cited warrant, §20.3 step 4:
   "a commit does **not escape** this by unstoring in the same breath".
   Verbs: `escapes` vs `does not escape`. Same verb, opposite polarity, same
   case. **UNSOUND → X-01.**
2. hunk 5: "The bar beside the §14 bar does not reach a shrink either: it **bars
   a change to a planar layer's channel declarations** … and a shrink is not
   one." Cited rule, §20.3: "a commit MUST NOT **change the channel
   declarations** in a way that alters the disk ordinal". Verbs: `bars a change
   to … channel declarations` vs `MUST NOT change the channel declarations`.
   Same set. **SOUND.**
3. hunk 1: "it **bars a change to a planar layer's channel declarations** that
   moves a stored tile's disk ordinal" vs the same source. **SOUND.**
4. hunk 3: "Where this bars a change the operation is a new layer or a
   whole-file rewrite, **exactly as above**." Source: "Such a change **is** a
   new layer, or a whole-file rewrite under a fresh file_id". Verbs: `is` vs
   `the operation is`. Same. **SOUND.**
5. hunk 3: "**the tense is both bars'**". §14 bar: "for any tile that layer
   **stores in the generation this commit supersedes**". Ordinal bar: "any tile
   the layer **stores in the generation this commit supersedes**". Word for
   word identical. **SOUND.**
6. hunk 3: "what it disturbs is instead the re-emission rule above, **whose only
   stated occasion for a renumbering is a geometry change**." Source: "(a
   geometry change renumbers ordinals wherever `[R-GEO-06]` moves them)".
   The claim about the *text* is right; the claim's *force* fails, because
   [R-GEO-01] and register row L32 both classify channel count C as a layer
   geometry field, so the insert/remove half of the bar's own subject IS a
   geometry change and is already licensed there. Sound for a permutation,
   unsound for an insertion or removal — the analogy is doing work for two
   members and only holds for one. **X-05.**
7. hunk 6: "subject to every rule its new geometry is subject to, **which is the
   same step's permission**." Step 4's actual sentence: "**a growth** is
   permitted exactly where the geometry it produces satisfies every rule that
   geometry is subject to" — attached to growth, not to re-declaration, whose
   own permission in step 4 is the bare "MAY be **re-declared freely**".
   Verbs: `is re-declared freely, subject to every rule` vs `MAY be re-declared
   freely` + `a growth is permitted exactly where`. **X-10.**
8. hunk 5: "so a shrink producing only those is permitted here **exactly as it
   is there**" — "there" = the §14 bar's own carve-out at 3148-3151 ("a new
   padding position whose stored byte already holds the fill `[R-SER-05]` fixes
   — is not what this bars"). Same carve-out, same quantifier. **SOUND.**

## Check 5 — exhaustive-claim ledger

- hunk 1 "Of its two bars" → verified 2 by the awk sweep. PASS.
- hunk 1 "The other bar reaches **neither** a shrink **nor** a growth" → the
  ordinal bar's subject is a channel-declaration change; a shrink and a growth
  are extent changes. PASS. (A planar shrink/growth does move stored ordinals
  via N, but the bar does not reach it and the re-emission rule licenses it.)
- hunk 3 "Appending a channel, or removing the last, re-indexes nothing and
  **moves no ordinal at all**" → true of the *surviving* channels. It is silent
  about the removed channel's own stored tiles, which cease to have an ordinal.
  **X-04.**
- hunk 3 "**The test is on the declared types and not on the values a tile
  happens to hold**" → PASS, and the 0x80/int8/uint8 illustration is correct.
- hunk 3 "the list is not offered as exhaustive" → an explicit disclaimer. PASS.
- hunk 4 "**among them**" → explicitly non-exhaustive. PASS.
- hunk 4 "A shrink is permitted **exactly where** it alters nothing §14 fixes"
  → falsified by hunk 4's own preceding clause. **X-02.**
- hunk 5 "What counts as such an alteration is the §14 bar **and nothing else**"
  → correctly scoped to *alteration*, not to permission. PASS.
- hunk 7 "a re-typed channel among the cases it does not reach" → falsified four
  sentences later by the uint8→bool/T3 example in the same hunk. **X-07.**
- hunk 7 "**no** check can know which type a channel carried before" → PASS
  (§9.7 walks the live state only; no field records a prior declaration).
- §11.1 hunk 1 "permitted **wherever** it does not" → **X-03.**

## Byte-level determinations

- X-01: the disputed file is CONFORMING — §21.7 itself says the case leaves the
  live state clean and has no witness, so no register row fires and [R-CNF-05]
  does not bar it. One reading lets an appender emit it; the other forces a
  fresh file_id. Set moves. **BYTE-LEVEL.**
- X-04: the disputed file (planar layer, C reduced, old plane's payloads as
  slack, entry_count = C'·N) is CONFORMING under both readings. One reading
  permits it as an append, the other forces a whole-file rewrite. Set moves.
  **BYTE-LEVEL.**
- X-02 / X-03: the disputed file carries an L40 violation (alignment declared,
  a stored tile's offset not a multiple of A) or the [R-SLB-04] equivalent, so
  [R-CNF-05] bars every conforming writer from emitting it under BOTH readings.
  Set does not move. **NOT byte-level.**
- X-05, X-06, X-07, X-08, X-09, X-10: all leave the operative MUST NOT
  untouched; they change what a reader believes about ground, remedy, or
  detectability, not what may be emitted. **NOT byte-level.**

## Rejected candidates

1. *"§14 bar" is used at line 1606 and 1616, ~1500 lines before hunk 2 coins it
   at 3140.* Dropped: §11.1's Rationale points at §20.3 in the same sentence
   ("§20.3 states normatively, and governs, …"), so the term is findable, and
   the Rationale is non-normative anyway.
2. *A planar↔interleaved layout flip moves every stored ordinal and the ordinal
   bar names only "channel declarations".* Dropped: for C ≥ 2 the §14 bar
   catches it through the decoded size (P·Q vs P·Bᶜ), and for C = 1 numeric the
   two ordinal formulas and the two decoded sizes coincide, so the change is a
   no-op. No case escapes.
3. *A dimension reorder moves every stored ordinal in both layouts and no bar
   names it.* Dropped: it is a geometry change, and the re-emission rule's
   parenthetical at 3127 explicitly licenses renumbering there.
4. *"One effect is barred beside it … the §14 bar does not reach it" reuses one
   pronoun for two referents in one sentence.* Dropped as a filed finding: the
   mid-sentence naming of "the §14 bar" disambiguates it for any reader who
   reaches the comma. Recorded here.
5. *Hunk 3's "MAY be re-declared freely" could let an empty layer be
   re-declared past [R-COD-07]'s L44 cap.* Dropped: re-declaring an empty layer
   with a nonzero extent IS a growth, and the growth clause immediately
   following imposes "every bound the layer's own declarations impose,
   [R-COD-07]'s lz4 decoded-size cap among them (L44)". Only the residue —
   a re-declaration that changes nothing geometric — is unqualified, and there
   nothing is at stake. Related but weaker than X-10, which I did file.
6. *Hunk 7's "a permutation among channels whose planes are the same length
   disturbs nothing a row can see" might miss a CRC row.* Dropped: the entries
   and payloads are unchanged bytes at permuted positions; the segment CRC array
   is re-emitted over the permuted entries by the re-emission rule, so it is
   consistent. No row fires.
