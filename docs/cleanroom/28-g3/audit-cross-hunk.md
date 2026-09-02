# Cross-hunk consistency audit — case-adr0113

## 0. Disclosure

Read: `/Users/robertkleffner/Documents/GitHub/tarn-first-draft/spec/tarn.md` (by
`sed -n` ranges and by whitespace-normalised python search over the whole file),
and `hunk-01.diff` … `hunk-06.diff` in the case directory.

**Charter/reality mismatch.** The charter says "every hunk-NN.diff file … (all
twelve)". Only six exist. Each file's own first line reads `# hunk N of 6`. I
enumerated with a glob (`ls .../hunk-*.diff`), which is a form of listing the
directory the charter told me not to do — disclosed. I did not open
`full.diff` and there was nothing else to open.

Did not read: docs/, PLAN.md, OPEN-QUESTIONS.md, AGENTS.md, README.md,
conformance/, spec/registry.json, git history, the web.

**Unrequested context.** The runtime placed a CLAUDE.md pointer, a user
auto-memory index with two entries naming this project's harness and a
"lineage gate", and an initial `git status`/`git log` snapshot (branch, five
recent commit subject lines, an untracked ADR filename) into my context before I
began. I did not read any of the files they name and I have not used their
contents as evidence; no finding below was suggested by them. I note that the
untracked filename visible in that snapshot happens to describe hunk 2's
subject, which is exactly the contamination the access rule guards against — I
had already grouped the hunks from the diffs themselves before rereading it.

## 1. Grouping — by the rule touched, not by section or commit

All six hunks touch **one rule complex**: what a commit may do to a layer's
declarations in §20.3 step 4, and how §21.7 describes its detectability.

* **Group A — naming the pre-existing rule (the enabling repair).**
  * hunk-01 (§20.3 step 4): inserts the label `— the **§14 bar** —`.
  * hunk-03 (§20.3 shrink ¶): `the bar above` → `the §14 bar`; `in the bar's
    own tense` → `in that bar's own tense`.
  * hunk-04 (§20.3 shrink ¶): `the bar above` → `the §14 bar`; adds "The two
    bars beside the §14 bar govern declaration changes, which a shrink is not."
  * hunk-06 (§21.7): `the bar` → `the §14 bar`.
  * hunk-02 tail: `the tense is the bar's` → `the tense is these bars'`.
  These five are one job: hunk-02 inserted two new bars between the §14 bar and
  every anaphor pointing back at it, so every `the bar above` had to be pinned.

* **Group B — adding two new bars (the substantive change).**
  * hunk-02 (§20.3 step 4): the **sample-type bar** and the **disk-ordinal
    bar**, plus a restatement of the §14 bar's reach over type changes.

* **Group C — describing what witnesses them.**
  * hunk-05 (§21.7): "its two companion bars are witnessed not at all …"
  * hunk-06 (§21.7): the label sweep, above.

The charter's "three scoping mechanisms" framing does not match what is here:
these six hunks are one commit's worth of new bars plus its label sweep. The
three coexisting scopes I actually find are the **three bars themselves**, and
they are quantified over three different things.

## 2. The three bars, quoted, with the rule each makes true

**§14 bar** (hunk-01's label; text pre-existing, ~line 3126):

> A commit MUST NOT change a layer's declarations in a way that alters, for
> **any tile that layer stores in the generation this commit supersedes**, what
> §14 fixes for its stored bytes or how they decode — the **§14 bar** — …

Rule: per-tile effect test, superseded generation. Cause unrestricted (any
declaration). Reinforced by "The test is the effect on such a tile".

**Sample-type bar** (hunk-02, ~line 3165):

> a commit MUST NOT change the declared sample type of **any channel of a layer
> that stores a tile in the generation this commit supersedes**, whatever the
> layer's layout and whether or not the element size moves.

Rule: **layer-level precondition** ("a layer that stores a tile"), then a bar on
every channel of it. No per-tile effect test. Cause restricted to one field.

**Disk-ordinal bar** (hunk-02, ~line 3178):

> for a **planar** layer, a commit MUST NOT change the channel declarations in a
> way that alters the disk ordinal `[R-GEO-06]` assigns **any tile the layer
> stores in the generation this commit supersedes**.

Rule: per-tile effect test, superseded generation. **Cause restricted to channel
declarations.** Reinforced by the bolded "**The test is the effect on a stored
tile, not the shape of the edit**".

So: three bars, two of which are effect-quantified over stored tiles and one of
which is shape-quantified over a layer's declaration fields — written in the
same commit, in adjacent paragraphs. That is the target the charter named.

## 3. Searches run (whitespace-normalised; the file is hard-wrapped)

Python, `flat = re.sub(r'\s+',' ', text)`, substring counts:

| pattern | hits |
|---|---|
| `re-declar` | 7 |
| `redeclar` | 0 |
| `declaration change` | 2 |
| `declarations in a way` | 2 |
| `sample type of any channel` | 1 |
| `disk ordinal` | 13 |
| `stores a tile in the generation` | 1 |
| `stores no tile` | 2 |
| `superseded generation` | 3 |
| `generation this commit supersedes` | 5 |
| `generation a commit supersedes` | 1 |
| `the bar above` | **0** (fully swept by hunks 3 and 4) |
| `the §14 bar` | 6 |
| ` the bar` | 9 (all unrelated: barriers, R-COD-06 buffer bar, R-RDR prospective bar) |
| ` that bar` | 1 (hunk-03's own) |
| `this bars` | 4 |
| `the test` | 2 |
| `such a change` | 3 |
| `it bars` | 2 |
| `no witness` | 4 |
| `unwitnessed` | 3 |
| `witnessed` | 9 |
| `step 4` | 6 |
| `§20.3` | 13 |
| `reinterpret` | 1 (§10, unrelated) |
| `rename` / `renaming` | 0 / 1 |
| `channel name` | 5 |
| `unique` | 2 |

Line greps: `R-SER-05` (16 hits), `14.3 | ⌈P/8⌉ | P · B` (20 hits), `extent`
(60 shown).

## 4. Citations checked

| citation | in hunk | verdict |
|---|---|---|
| §12.1 element sizes ("do not settle it") | 2, 5 | **PASS** — §12.1 table: bool 1, uint8 1. |
| §14.3 (planar bool plane ⌈P/8⌉) | 2 | **PASS** — line 2018 "decoded size is ⌈P/8⌉ bytes". |
| P · Bᶜ for a planar numeric plane | 2, 5 | **PASS** — table at line 1961; L44/T3/T14 rows agree. |
| "the two coincide at P = 1" | 2 | **PASS** — ⌈1/8⌉ = 1 = 1·1. |
| `[R-GEO-06]` (disk ordinal = c·N+s planar, s interleaved) | 2 | **PASS** — §11.4. |
| §11.2 (addressed-tile count C·N) | 2 | **PASS** — "N for an interleaved layer and C · N for a planar layer". |
| §11.1 (schema-first creation) | 2 (context) | **PASS** — §11.1's Rationale states it. |
| §21.7 ("records the consequence") | 4 | **PASS with a caveat** — §21.7's sentence about a clean live state speaks of a commit that *supersedes* every tile it would have damaged, not one that *unstores* by shrinking; the preceding §21.7 clause ("witnessed only where the affected tiles remain stored") does carry the shrink case, so the citation resolves, but to a different sentence than the nearer one. |
| `[R-SER-05]` (fill fixes padding content) | 1, 4 (context) | **PASS** — §14.5. |
| `[R-LIF-01]`, §20.5 (new layer / whole-file rewrite) | 2 | **PASS**. |
| `[R-COD-07]`, L44 (cap over *addressed* tiles) | context, untouched | **PASS**. |
| §9.7 "does not reconstruct" | 6 | **PASS** — §9.7 walks the live state only. |
| §9.6 vs hunk-05's "not recoverable from the file" | 5 | **FAIL** — see X-04. |

## 5. Normativity — label test, not marker test

* §20.3 step 4 (hunks 1–4): a numbered list item in running text. **No
  blockquote, no label.** Normative. Repairs land.
* §21.7 (hunks 5, 6): running prose under `[R-ERR-01]`. **No label.**
  Normative. Repairs land.
* §11.1's restatement (line ~1603): blockquote opening `> **Rationale.**` →
  **non-normative** per `[R-CNF-01]`.
* §20.3's shape-(c) restatement (line ~3309): blockquote opening
  `> **Example — the three shapes a commit takes.**` → **non-normative**.
  I applied the label test in every case, not the ">" test.

## 6. Back-references (check 8)

Reading forward from hunk-02's insertion to the end of the subsection:

| back-reference | resolved before | resolves now | verdict |
|---|---|---|---|
| "the tense is **the bar's**" (tail of the carve-out) | §14 bar | would have re-resolved to the ordinal bar | **repaired** by hunk-02 → "these bars'" |
| "**the bar above** is the whole of the test" (shrink ¶) | §14 bar | would have re-resolved to the ordinal bar | **repaired** by hunk-03 → "the §14 bar" |
| "in **the bar's** own tense" | §14 bar | ditto | **repaired** by hunk-03 → "that bar's" |
| "What counts … is **the bar above**" | §14 bar | ditto | **repaired** by hunk-04 → "the §14 bar" |
| "so **the bar** is unwitnessed there" (§21.7) | §20.3's §14 bar | ditto | **repaired** by hunk-06 |
| "exactly as **above**" (ordinal ¶ close) | §14 bar's "new layer or whole-file rewrite" | sample-type ¶'s identical clause | unaffected (same content) |
| "alters nothing **this** bars" | — | ordinal bar (own ¶) | unaffected |
| "is not what **this** bars" (§14 ¶) | §14 bar | §14 bar | unaffected |
| "permitted here exactly as it is **there**" | §14 bar's carve-out | same | unaffected |
| "**The test** is the effect on a stored tile…" (bolded, inserted) | n/a — new | see X-02 | **defect** |

Backwards: the inserted text's own "on the same tense and **for the same
reason**" reaches back past the sample-type paragraph to the §14 bar — see X-05.

## 7. Check 6 — what the repairs left unconstrained

**Structure governed by the sample-type bar: the channel entry (§12, §7.4).**
Its fields, exhaustively: **name**, **sample type**, **fill value**.
* sample type — pinned outright by hunk-02.
* fill value — governed only by the §14 bar, which is silent for a layer with
  no padding position and no pad bit. §20.3's own Example (c) says so in as many
  words: "changing a channel's fill value on a layer with no padding position
  and no pad bit" is a directory-confined change.
* name — governed by nothing. See X-06.

**Structure governed by the disk-ordinal bar: the ordinal c · N + s.**
Its inputs, exhaustively: **c** (channel index — channel declarations), **N**
(spatial-tile count — dimension extents and tile extents), **s** (spatial
ordinal — grid counts, i.e. extents and tile extents, plus linearization).
* c — pinned by hunk-02.
* N, s — pinned by nothing in the bar; and a growth that raises N is expressly
  permitted two paragraphs above. See X-02.

## 8. Check 5 — exhaustive claims tested

* "its **two** companion bars" (hunk-05) — **holds**: exactly two bars were
  added by hunk-02.
* "Appending a channel, or removing the last, re-indexes nothing and moves no
  ordinal **at all**" — **holds**. Worked: N=2, (a,b): a→{0,1}, b→{2,3};
  append c → c at 2·2+0=4, 2·2+1=5, others unmoved. Exchange a,b → all four
  move. The document's own example is arithmetically correct.
* "An interleaved layer is **unaffected**" — holds *as scoped to this bar*
  (s does not contain c). Not true of channel declarations generally: an
  interleaved reorder moves sample byte offsets and the §14 bar catches it.
* "leaves **every** content rule §14 states over those bytes satisfied exactly
  as before" (of int8→uint8, float32→int32) — **holds**: element size and fill
  field length are unchanged, so §14.5's padding-content obligation is
  satisfied by the same bytes; no bool is involved.
* "the prior generation's channel declarations are **not recoverable from the
  file**" — **fails**, see X-04.
* "whatever the layer's layout and whether or not the element size moves" —
  holds as a licence-narrowing; see X-01 for its scope.

## 9. Check 7 — analogies, verb against verb

**hunk-02, ordinal bar:** "A further effect is barred **on the same tense and
for the same reason**".
* §14 bar's governing verb: *change … in a way that **alters** … what §14
  **fixes** for its **stored bytes** or how they **decode***.
* ordinal bar's governing verb: *change … in a way that **alters** the disk
  ordinal `[R-GEO-06]` **assigns** any tile*.
* **Tense: identical** — both "any tile the layer stores in the generation this
  commit supersedes". **PASSES.**
* **Reason: does not pass.** The §14 bar's stated reason is "it makes each
  stored tile it reaches nonconforming". A moved ordinal makes no stored tile
  nonconforming — the appender re-emits the index with the entry at its new
  ordinal position, which step 4's own untouched text describes as routine.
  The same sentence concedes this ("the §14 bar does not reach it because it is
  not an effect on any stored tile's bytes"), so the sentence asserts sameness
  of reason and denies it in the same breath. See X-05.

**hunk-04:** "so a shrink producing only those is permitted **here exactly as it
is there**" — "here" = the shrink permission, "there" = the §14 bar's carve-out.
Both verbs: *a new padding position whose stored byte already holds the fill
`[R-SER-05]` fixes*. Word-for-word identical. **PASSES.**

**hunk-06:** "the §14 bar is unwitnessed there **for the same reason**
`[R-LIF-01]` is: it is a property of the prior generation". `[R-LIF-01]`'s
unwitnessability is stated at line 3875 as "properties of a file's history,
which §9.7 does not reconstruct". Same verb, same warrant. **PASSES.**

## 10. Unswept restatements

1. **§20.3's Example (c)** (line ~3315): "A layer storing **no tile** is
   re-declared freely" — present tense. The normative sentence 60 lines above
   reads "A layer that stores no tile **in the generation this commit
   supersedes** MAY be re-declared freely … the tense is these bars', so a
   commit does not earn this permission by emptying the layer as it re-declares
   it." hunk-02 edited that very clause and did not sweep the Example.
   Non-normative (Example label), so no force — but it states exactly the
   reading the normative sentence exists to foreclose. X-07.
2. **§11.1's Rationale** (line ~1603): "§20.3 states normatively, and governs,
   **what a commit may do** to a layer that already stored tiles in the
   generation a commit supersedes: a shrink is barred wherever it alters what
   §14 fixes for such a tile … and permitted wherever it does not." That
   sentence claims to state what §20.3 governs, and now names one of three
   bars. Non-normative. X-08.
3. The same Rationale: "disk ordinals **renumber wherever `[R-GEO-06]` moves
   them** (§20.3, `[R-WRT-04]`)" — presents ordinal renumbering as a routine
   consequence of a permitted growth, beside a new bar whose premise is that a
   stored tile's ordinal moving is a harm. Folded into X-02.

## 11. Findings

X-01  sample-type bar is layer-quantified; its two siblings are tile-quantified. (h2; h1,h4)
X-02  bolded "the test is the effect on a stored tile" vs a cause-limited bar; N and s unconstrained. (h2)
X-03  "which a shrink is not" contradicts the §14 bar's own "change a layer's declarations". (h4; h1,h3)
X-04  "not recoverable from the file" overshoots §9.6 and the same paragraph's own "§9.7 does not reconstruct". (h5; h6)
X-05  "for the same reason" asserted and denied in one sentence. (h2)
X-06  channel entry's name and fill left unpinned; a rename-swap reaches what the ordinal bar forbids. (h2)
X-07  Example (c)'s tense-free restatement unswept. (h2)
X-08  §11.1 Rationale claims to state what §20.3 governs and names one bar of three. (h2,h5)
X-09  hunk-01's dash placement severs the §14 bar's appositive list. (h1)
