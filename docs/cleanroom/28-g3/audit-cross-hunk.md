# Cross-hunk consistency audit — case-adr0113

## 0. Disclosure

Read: `/Users/robertkleffner/Documents/GitHub/tarn-first-draft/spec/tarn.md` (§§3.1, 9.7, 10.4, 11.1–11.4, 12, 12.1–12.3, 14.1–14.4, 16.1–16.2, 20.3, 21.1, 21.7, register rows L2/L39/L40/L44/T23/T26, [R-CNF-01], [R-CNF-05]) and
`.../scratchpad/case-adr0113/hunk-01.diff` … `hunk-09.diff`.

**The charter says twelve hunk files. The directory contains nine** (`hunk-01` … `hunk-09`), and each file's own header line reads "hunk N of 9". I audited the nine that exist. I did not read `full.diff`, `docs/`, `conformance/`, `OPEN-QUESTIONS.md`, `PLAN.md`, `AGENTS.md`, `spec/registry.json`, or any git history, and did not list the case directory beyond globbing `hunk-*.diff`.

**Context I did not ask for appeared before I began**: a project instruction file (CLAUDE.md → AGENTS.md pointer), a user auto-memory index naming two memory notes about this project, an environment/git-status block naming the current branch, modified files and five recent commit subject lines, and an MCP/skills listing. I did not open any of it, and no finding below derives from it. I note only that the git-status block named an untracked ADR filename; I did not read that file and no finding is keyed to its name.

The charter also describes the twelve hunks as "one cycle narrowed a rule's reach; a later one added a scope statement bounding a whole section; a later one still added a requirement deciding when requirements apply at all." **The nine hunks that exist do not match that description**: none adds a section preamble and none adds a requirement about which requirements apply to a class of file. All nine concern one thing — what §20.3 step 4's declaration-change bar(s) range over. I audited what is there, not what the charter describes.

## 1. Grouping (by rule touched, not by section or commit)

**Group A — naming of the incumbent bar.** h3 (coins "**§14 bar**" at §20.3 step 4), h5, h6, h9 (replace anaphors with the coined name), h1 (uses the name in §11.1's Rationale).

**Group B — the two NEW bars.** h4 (§20.3 step 4: the sample-type bar and the planar disk-ordinal bar), h2 (§11.1 Rationale's summary of them), h6 (their non-reach into a shrink), h8 (§21.7's witness account of them).

**Group C — the tense of the empty-layer permission.** h4 ("the tense is these bars'"), h7 (§20.3's Example: "a layer the commit itself empties does not qualify"), h2 (§11.1 Rationale's untouched-in-substance "A layer that stored nothing may be re-declared freely").

Groups A and B share hunks 5/6; B and C share hunk 4 and hunk 2. That overlap is where the cross-hunk defects sit.

## 2. The rule each repair adopts

- **h1** (Rationale, §11.1): of §20.3's three bars, only the §14 bar reaches a shrink or a growth. Non-normative.
- **h2** (Rationale, §11.1): the other two bars are (i) a change to a channel's declared sample type and (ii) a change to a **planar** layer's channel declarations **that moves a stored tile's disk ordinal**. Non-normative.
- **h3** (§20.3 step 4, normative): names the incumbent bar "§14 bar", and asserts that name is used by "the rest of this step and §21.7".
- **h4** (§20.3 step 4, normative): adds two MUST NOTs. (i) *Sample-type bar*: a commit MUST NOT change the declared sample type of **any channel** of a layer that **stores a tile** in the superseded generation — layout-blind, element-size-blind. (ii) *Ordinal bar*: for a **planar** layer, a commit MUST NOT change the channel declarations in a way that **alters the disk ordinal [R-GEO-06] assigns any tile the layer stores** in the superseded generation. Also re-tenses the empty-layer permission to "these bars'".
- **h5** (normative): a shrink's test is the §14 bar, in that bar's own tense.
- **h6** (normative): a shrink is tested by the §14 bar "and nothing else"; neither companion bar reaches a shrink.
- **h7** (Example, non-normative): the free-re-declaration permission is anchored to the superseded generation and a commit that empties the layer does not earn it.
- **h8** (§21.7, normative): the two companion bars are unwitnessed where the change leaves §14-fixed things untouched; where it does touch one and the tile stays stored, "the rows below witness it".
- **h9** (§21.7, normative): renames one anaphor to "the §14 bar".

## 3. Normativity — label test, not ">" marker

[R-CNF-01] (line 106): "All text in this document is normative except: §1 (Introduction); any text labeled *Note*, *Example*, or *Rationale*; and appendices identified as non-normative."

- h1, h2 land in the block opening `> **Rationale.** Empty layers serve schema-first workflows` (line 1604). Label = **Rationale** → **non-normative**.
- h7 lands in the block opening `> **Example — the three shapes a commit takes.**` (line 3286). Label = **Example** → **non-normative**.
- h3, h4, h5, h6 land in §20.3's numbered step 4 under "An appender MUST, in order:" — unlabeled, no ">" — **normative**.
- h8, h9 land in §21.7 running prose ending `[R-ERR-01]` — unlabeled, no ">" — **normative**. §21.1 adds: "The subsections after §21.5 are not part of the register and carry no rows … neither this completeness clause nor the instance arithmetic below reaches … §21.7's account of what no check detects." So §21.7 is normative but row-free; verdicts still follow the rows.

Consequence for Group B: **the growth-side exemption for the two companion bars exists only in the Rationale (h2).** h6 gave the shrink side a normative statement; nothing normative states it for a growth. (Reported as X-08's companion, below; the reach is in fact absent for a pure growth, so this is asymmetry rather than a hole.)

## 4. Searches run (whitespace-normalised over the whole file, so hard wraps cannot hide a hit)

Python `re.sub(r'\s+',' ',text)` then `finditer` for each literal:

| phrase | hits |
|---|---|
| `§14 bar` (line grep) | 10 — 1606, 3137, 3157, 3181, 3218, 3230, 3235, 3239, 3906, 3930 |
| `re-declared freely` | 2 — §20.3 step 4 (normative), §20.3 Example (h7) |
| `stored nothing` | 1 — §11.1 Rationale, line 1613 |
| `stored no tile` | 2 — §20.3 step 4 (h4), §20.3 Example (h7) |
| `stores no tile` | 2 — §20.3 step 4 (h4); one unrelated hit in an appendix item |
| `storing no tile` | 0 (h7 removed it) |
| `declared sample type` | 3 — 1615 (h2), 3171 (h4), 3236 (h6) |
| `channel declarations` | 4 — 1616 (h2), 3183 (h4), 3237 (h6), 3898 (h8) |
| `disk ordinal` | 14 |
| `the bar above` | 0 (h5/h6 swept both) |
| `whole of the test` | 1 — 3218 (h5) |
| `and nothing else` | 4 — one is 3230 (h6) |
| `the rows below` | 2 — one is 3904 (h8) |
| `one of those` | 4 — one is 3903 (h8) |
| `exchanging` | 1 — 3198 (h4) |
| `renumber` / `re-index` | 3124, 1623, 3187, 3190 |
| `R-SLB-01` / `R-SLB-04` | 2265, 2311, 3061, 3254, 3257, 3461, 3724, 3725, 4029 |
| `R-GEO-06` | 1623, 1700, 2968, 3124, 3184, 3885 |
| `R-COD-07` | 2459, 2939, 3210, 3729 (L44), 3768 (T23) |

## 5. Citations checked

| citation (in repaired text) | verdict |
|---|---|
| h1/h2 "§20.3 states normatively" | PASS — §20.3 step 4 is normative (§3 above). |
| h2 "§11.2" grid/addressed-tile count | n/a in h2; used in h4 — PASS, §11.2 line 1630: addressed-tile count "is N for an interleaved layer and C · N for a planar layer". |
| h2 "[R-CNT-17]" (untouched context) | PASS — line 1088/1110, entry_count equals the addressed-tile count. |
| h2/h1 "[R-GEO-06]" | PASS — line 1697-1700: disk ordinal is s interleaved, c·N+s planar, c the channel's index. |
| h3 "§3.1 defines *stored* against a generation" | PASS — §3.1: "A tile is *stored in a generation* if and only if that generation's tile-index entry for it is not the sentinel". |
| h3 "the name the rest of this step **and §21.7** use for it" | **FAIL** — the name is also used at line 1606, in §11.1's Rationale, by h1. See X-05. |
| h4 "§12.1" element sizes | PASS — §12.1 table: bool 1, uint8 1, int8 1, int32 4, float32 4. |
| h4 "(§14.3)" packed plane ⌈P/8⌉ | PASS — §14.3: "the decoded size is ⌈P/8⌉ bytes". |
| h4 "P · Bᶜ" planar numeric plane size | PASS — §14.2 table row "planar, numeric channel c | P · Bᶜ". |
| h4 "[R-GEO-06]" assigns the disk ordinal | PASS. |
| h4 "§11.2" for C · N | PASS. |
| h4 "(§11.1)" schema-first creation | PASS — §11.1's Rationale opens "Empty layers serve schema-first workflows". Note the cite is to a non-normative block; it is offered as motivation, which is legitimate. |
| h4 "[R-LIF-01], §20.5" | PASS — [R-LIF-01] committed-prefix immutability; §20.5 compaction/whole-file rewrite. |
| h6 "§21.7 records the consequence" | PASS — §21.7 line 3929-3931 does record it (and h9 renamed the anaphor there). |
| h8 "§9.7 walks the live state" | PASS — §9.7 line 3863: "A verifier checking [R-CNT-02]'s partition walks the live state only." |
| h8 "the element sizes of §12.1" / "P · Bᶜ → ⌈P/8⌉" | PASS — as above. |
| h8 "§21.4's content rows" | PASS — §21.4 holds the tile-content rows (T2/T4/T5 cited nearby). |
| h8 "T3 or T14" for decoded size | PASS in kind (T14 declared length, T3 decoded payload length), consistent with the untouched gloss. |
| h9 "[R-LIF-01]" / "§20.5's three obligations ([R-WRT-06])" | PASS — untouched context, three obligations enumerated in the same sentence. |

## 6. Derived numbers

- h4's ordinal example, N=2, channels (a,b,c): a → 0·2+0 = 0 and 0·2+1 = 1; b → 1·2+0 = 2 and 1·2+1 = 3; appending c → 2·2+0 = 4 and 2·2+1 = 5. Document says "`a` at ordinals 0 and 1 and `b` at 2 and 3 … adds 4 and 5". **Matches.**
- Exchange of a and b: a → 2,3; b → 0,1 — all four ordinals differ from before. Document: "moves all four". **Matches, under name-individuation only** (see X-01).
- ⌈P/8⌉ vs P·Bᶜ at Bᶜ = 1: P=1 → 1 vs 1 (coincide); P=2 → 1 vs 2; P=8 → 1 vs 8. Document: "the two coincide at P = 1". **Matches** (and P=1 is the only coincidence).
- §11.4's worked example, C=4, N=32, channel 2, s=10: 2·32+10 = 74. Document: 74. **Matches.**
- L2's "C·N (which dominates the max disk ordinal (C−1)·N + (N−1))": (C−1)N + N − 1 = CN − 1 < CN. **Matches.**

## 7. Back-reference resolution (check 8) — every one I traced

Insertions: h3 (one sentence), h4 (three paragraphs, ~44 lines), h6 (one sentence), h8 (one long clause + two sentences).

| back-reference | before | after | verdict |
|---|---|---|---|
| "the tense is **the bar's**" (3206, pre-h4) | §14 bar | h4 inserted two bars between → would have re-resolved to the ordinal bar | **FIXED** by h4 → "these bars'" |
| "**the bar above** is the whole of the test" (3218, pre-h4) | §14 bar | would have re-resolved to the ordinal bar | **FIXED** by h5 → "the §14 bar" |
| "**in the bar's own tense**" (3219) | §14 bar | same risk | **FIXED** by h5 → "in that bar's own tense" |
| "What counts … is **the bar above**" (3230) | §14 bar | same risk | **FIXED** by h6 → "the §14 bar" |
| "where **the bar** has no witness" (3239) | §14 bar | same risk | **FIXED** by h6 |
| "so **the bar** is unwitnessed there" (3930, §21.7) | §14 bar | h8 inserted "its two companion bars" upstream → would re-resolve | **FIXED** by h9 |
| "§20.3 step 4's **bar on a declaration change**" (3895, §21.7, untouched) | the single bar | step 4 now holds three bars, one of which is literally a bar on *changing the channel declarations* | **NOT fixed** — see X-05 |
| "the change does touch **one of those**" (3903, h8's own text) | n/a (new) | nearest antecedent is "which ordinal a stored tile used to occupy, or which type its channel carried before"; intended antecedent "everything §14 fixes" is 4 lines back | **NEW DEFECT** — X-04 |
| "exactly as **above**" (3201, h4's own text) | n/a | resolves to the §14 bar paragraph's tail, "a new layer, or a whole-file rewrite" | OK |
| "permitted here exactly as it is **there**" (3234) | §14 bar's carve-out | h6 pinned it by naming "the §14 bar" in the same sentence | OK |
| "**that cap** is quantified over addressed tiles" (3211) | [R-COD-07]'s lz4 cap, named in the prior clause | unchanged by any insertion | OK |
| "**such an alteration**" (3222, 3230) | "alters nothing §14 fixes" | unchanged | OK |
| "which is **the same step's permission**" (h7) | §20.3 step 4's empty-layer MAY | unchanged | OK |
| "**Of its** three bars" (h1) | "§20.3" in the prior sentence | new, resolves correctly | OK |

## 8. Check 6 — the structure, and what is left unconstrained

Structure governed by the two new bars: **a layer's channel declarations**. §12 (line 1719): "A channel is declared by its layer record's channel entry (§7.4): a **name** (§4.6), a **sample type** (`u16`, structural), and a **fill value** (§13)"; plus the **count** and the **declared order**.

| member | constrained by | verdict |
|---|---|---|
| sample type | h4's sample-type bar (layer-quantified) + §14 bar | constrained — but see X-02 |
| order / count (planar) | h4's ordinal bar | constrained — but see X-01 |
| order / count (interleaved) | §14 bar via "the byte offset of any sample within the decoded tile image" (Fᶜ = Σ Bⱼ, §14.2) and via decoded size P·Q | constrained |
| fill value | §14 bar only where the layer has padding positions or pad bits (§14.5); otherwise expressly permitted by §20.3's Example (c) | deliberate |
| **name** | **nothing** | **UNCONSTRAINED — X-01** |

Channel name is the sibling the repair left unpinned, and it is the sibling that decides *which channel a stored plane belongs to*. A commit whose new layer record lists `(b:uint8, a:uint8)` where the old listed `(a:uint8, b:uint8)` is **byte-identical** whether the writer performed "exchange a and b" (h4 says barred) or "rename a→b and b→a" (no bar reaches a rename). The bar therefore turns on the writer's intent rather than on the two generations' bytes.

Same gap on the dimension side: dimension **names** are equally unconstrained, and §3.1 makes dimension order load-bearing exactly as it does channel order. A dimension rename-permutation of a square-tiled layer is byte-identical to a dimension reorder, and reordering dimensions changes Gᵢ ordering and so the spatial ordinal s = Σ tᵢ·∏_{j>i} Gⱼ — but only the *channel* side got a bar.

## 9. Check 7 — analogy verbs, side by side

| repair's warrant phrase | repair's governing verb | cited rule's governing verb | same set? |
|---|---|---|---|
| h4: "A further effect is barred **on the same tense and for the same reason**" (ordinal bar ← §14 bar) | ordinal bar: "**alters the disk ordinal** [R-GEO-06] **assigns any tile the layer stores**" | §14 bar: "**alters** … **for any tile that layer stores** … **what §14 fixes for its stored bytes or how they decode**" | tense matches; **reason does not** — the §14 bar's reason is stated in the text as "it makes each stored tile it reaches **nonconforming**", but a channel reorder with the index region re-emitted at the new ordinals leaves every stored tile conforming. The harm is misattribution, not nonconformance. The analogy transfers the tense correctly and the rationale incorrectly. |
| h4: "**exactly as above**" (remedy ← §14 bar's remedy) | "the operation is a new layer or a whole-file rewrite" | "Such a change is a new layer, or a whole-file rewrite under a fresh file_id" | PASS — same set. |
| h4: "**for the same reason**" and "**on the same tense**", applied to *both* new bars at once? | sample-type bar: "**of any channel of a layer that stores a tile**" | §14 bar: "**for any tile that layer stores**" | **FAIL for the sample-type bar** — one is quantified over the *layer* (∃ a stored tile anywhere in it), the other over *each tile*. See X-02. |
| h6: "one bars a change to a channel's declared sample type and **the other a change to the channel declarations**" | flat "a change to the channel declarations" | h4: "change the channel declarations **in a way that alters the disk ordinal** … assigns any tile the layer stores" | **FAIL** — h6 drops both the planar restriction and the ordinal-moving restriction. See X-09. |
| h8: "its two companion bars are witnessed not at all **where the change leaves untouched everything §14 fixes for a tile the layer stores**" — one quantifier for two bars | ordinal bar: per stored tile | sample-type bar: per layer | tested separately: sound for the ordinal bar; for the sample-type bar the sentence presupposes there is a tile the change touches, which need not exist (a re-typed channel with no stored tiles). Harmless in outcome (still unwitnessed) but the quantifier does not fit both. |
| h8: "**exactly as it does** the §14 bar" (companion bars' escape ← §14 bar's escape) | "a commit that supersedes every tile it would have damaged escapes them here" | "a commit that supersedes every tile it would have damaged leaves the live state clean" (3928) | PASS — same verb, same set. |
| h1: "the one reaching a shrink or a growth **is** the §14 bar" | "reaching" | h6: "Neither of the two bars beside the §14 bar **reaches** a shrink" | shrink: PASS. **Growth: h6 states nothing**; only the Rationale carries it. |

## 10. Findings

X-01 h4 (with h2, h8) — ordinal bar: channel identity undefined; rename-permutation is byte-identical to the barred reorder. BYTE-LEVEL.
X-02 h4 (with h1, h2, h8) — sample-type bar is layer-quantified where every neighbouring rule is stored-tile-quantified; contradicts the step's own bolded test; delete-then-append reaches the same file. BYTE-LEVEL.
X-03 h8 — "the rows below witness it" contradicts its own sentence's head and the untouched rows six lines later. Not byte-level.
X-04 h8 — "one of those" resolves to the wrong antecedent, making the sentence self-contradicting. Not byte-level.
X-05 h3 (with h1, h8) — "the name the rest of this step and §21.7 use for it" is false (§11.1 uses it); and §21.7's own head sentence, now that step 4 holds three declaration-change bars, was left unnamed. Not byte-level.
X-06 h5+h6 — "the whole of the test" / "and nothing else" for a shrink is falsified by [R-SLB-04] in the same step. Not byte-level.
X-07 h2 (with h7) — §11.1's "A layer that stored nothing may be re-declared freely" left unswept on the very line h2 edited, while h7 swept the identical sentence in §20.3's Example. Not byte-level (Rationale).
X-08 h4 (with h2) — ordinal bar's counterfactual baseline unstated: a commit that both grows a planar extent and appends a channel. BYTE-LEVEL.
X-09 h6 (with h4, h2) — h6 restates the ordinal bar as barring "a change to the channel declarations" flat, which h4 expressly permits for an append. Normative-vs-normative.

## 11. Rejected candidates

- *h4's `int8`→`uint8` / `float32`→`int32` claim* ("moves no stored byte, no decoded size and no sample offset, leaves every content rule §14 states over those bytes satisfied"). Checked: element sizes 1/1 and 4/4 (§12.1); §14.5 fixes padding content to the channel's *fill*, and the fill field's length is the element size ([R-CNT-23]), so the fill bytes are unchanged and padding content stays satisfied; §12.3 makes a value its bit pattern, so nothing is renormalised. Dropped — the claim holds.
- *h4's arithmetic example and h8's ⌈P/8⌉ claim.* Recomputed both (§6 above). Dropped — both correct.
- *"the two coincide at P = 1" as an exhaustive claim.* It is an existence claim, and P=1 is in fact the only coincidence for Bᶜ = 1. Dropped.
- *h6's "a shrink is neither" as false because a shrink of a planar layer changes N and so moves disk ordinals.* The ordinal bar's trigger is a change to the **channel declarations**, which a pure extent shrink is not. Dropped as stated — but it is the seed of X-08, where a commit does both.
- *h7 landing in a non-normative Example, therefore inert.* Checked the normative counterpart: §20.3 step 4 line 3206-3207 carries the same rule ("the tense is these bars', so a commit does not earn this permission by emptying the layer as it re-declares it"). h7 is a faithful non-normative echo. Dropped.
- *h9 as a no-op rename.* Checked: without it, "the bar" at 3930 would re-resolve to "its two companion bars" introduced by h8 at 3897. Dropped — the repair is correct and necessary.
- *§21.7's "the rows below witness it" as byte-level.* §21.1 confines verdict-setting to the rows themselves; §21.7 carries no rows. A verifier's accept/reject on any given file is unchanged. Kept as X-03, marked not byte-level.
