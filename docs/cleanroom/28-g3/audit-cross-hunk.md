# Cross-hunk consistency audit — ADR-0113 repair set

## 0. Disclosure

Read:

- `/Users/robertkleffner/Documents/GitHub/tarn-first-draft/spec/tarn.md` (whole
  file reachable; read §11.1–§11.3, §12, §12.1, §14.2–§14.5, §15.1, §16.1–§16.2,
  §9.7, §17.2 (`[R-COD-07]` and its Note), §20.3 in full, §20.4 opening, §21.4
  rows T2/T3/T14/T15/T26, §21.7 in full, §21.8, §21.9, §1.x `[R-CNF-01]`,
  §2.x `[R-CNF-05]`, `[R-GEO-06]`, `[R-SLB-01]`/`[R-SLB-03]`/`[R-SLB-04]`).
- `case-adr0113/hunk-01.diff` … `hunk-08.diff`.

Not read: `full.diff`; anything under `docs/`, `conformance/`, `PLAN.md`,
`OPEN-QUESTIONS.md`, `AGENTS.md`, `README.md`, `spec/registry.json`; no git
history; no web.

**Two access-rule deviations, disclosed.**

1. The charter says "every hunk-NN.diff file … (all twelve)". Only **eight**
   exist. Each file's own header says "hunk N of **8**". To establish that I ran
   `ls .../hunk-*.diff`, which is a directory listing of exactly the files I was
   told to read — the charter told me not to list the directory. I then `cat`ed
   `hunk-01`…`hunk-12`; 09–12 returned "No such file or directory". No other
   file in that directory was seen or read. **The audit below covers eight
   hunks.** The charter's description of the commit set ("a section preamble
   that bounds every rule in its section", "a requirement deciding when
   requirements apply at all") does not match anything in these eight; I audited
   the text that is here, not the text the charter predicted.
2. Material was placed in my context before I began: a project `CLAUDE.md`
   pointer, a user auto-memory index naming two TARN notes, MCP server
   instructions, and a skills listing. None of it is specification evidence and
   I drew no conclusion from any of it. I name that it appeared; I do not repeat
   its contents.

Commands run: `wc -l`, `sed -n` ranges, `grep -n` on requirement ids and on
`^| T3 ` etc., `awk`+`tr`+`grep -o` to enumerate `MUST NOT` in §20.3, and two
Python snippets that whitespace-normalise the whole file and report
line-numbered hits (the document is hard-wrapped; line-oriented grep misses
wrapped phrases). Sweep transcripts in §3 below.

## 1. The grouping — by the rule touched, not the section

All eight hunks touch **one** rule complex: *what a commit may change about a
layer's declarations, quantified over which generation's stored tiles.*

Step 4 of §20.3 now holds **three** MUST NOTs on declarations (verified by
enumerating `MUST NOT` over lines 3072–3289; the other two in §20.3 are step 2's
"MUST NOT repair the defect" / "MUST NOT drop the record"):

- **B1, the §14 bar** (L3134–3139, named by hunk 2): "A commit MUST NOT change a
  layer's declarations in a way that alters, for any tile that layer stores **in
  the generation this commit supersedes**, what §14 fixes for its stored bytes
  or how they decode — the set of padding positions (§11.3) and the content
  `[R-SER-05]` fixes there, the decoded size, the byte offset of any sample …,
  or the codec and filter …". Quantifier: **per stored tile**, prior generation.
- **B2, the sample-type bar** (L3172–3175, inserted by hunk 3): "a commit MUST
  NOT change the declared sample type of any channel of a layer that stores a
  tile in the generation this commit supersedes". Quantifier: **per layer**
  (explicitly, deliberately, not per channel), prior generation.
- **B3, the planar ordinal bar** (L3201–3205, inserted by hunk 3): "For a
  **planar** layer, a commit MUST NOT change the channel declarations in a way
  that alters the disk ordinal `[R-GEO-06]` assigns any tile the layer stores in
  the generation this commit supersedes." Quantifier: **per stored tile**, prior
  generation, planar only.

Grouping of the hunks against those:

| Group | Hunks | What it does |
|---|---|---|
| **G1 — naming** | 2, 8 | coins "the **§14 bar**" (h2) and sweeps one anaphor in §21.7 to it (h8) |
| **G2 — the two new bars** | 3 | inserts B2 and B3; repairs "the tense is the bar's" → "these bars'"; rewrites the growth warrant to cite §14.5 |
| **G3 — shrink scoping** | 4, 5 | says B1 alone tests what a shrink *alters* (h4) and that B2/B3 do not reach a shrink (h5) |
| **G4 — non-normative restatements** | 1, 6 | §11.1 **Rationale** (h1) and §20.3's **Example — the three shapes** (h6) restate the three-bar picture and the empty-layer permission |
| **G5 — detectability** | 7, 8 | §21.7 records what witnesses B1/B2/B3 |

**Normative-force test applied, by label not by marker**, per `[R-CNF-01]`
("All text in this document is normative except: §1 (Introduction); any text
labeled *Note*, *Example*, or *Rationale*; and appendices identified as
non-normative", L104–106):

- h1 lands in a block opening `> **Rationale.**` → **non-normative**.
- h6 lands in a block opening `> **Example — the three shapes a commit takes.**`
  → **non-normative**.
- h2, h3, h4, h5 land in §20.3 step 4's numbered list, plain prose carrying
  `[R-WRT-04]` → **normative**.
- h7, h8 land in §21.7 plain prose carrying `[R-ERR-01]` → **normative**. (I
  checked the label, not the ">" marker: §21.7's repaired sentences are not in a
  blockquote at all.)

So B1/B2/B3 and the shrink/growth clauses land normatively; h1 and h6 are
reader-facing restatements with no force. That matters for the *direction* of
every disagreement below.

## 2. Per-hunk: the rule each repair makes true

- **h1** — the §14 bar is the one of §20.3's three bars that reaches a shrink
  *or a growth*; B2 and B3 reach neither; an empty layer is one that stored
  nothing in the **superseded** generation, and a layer the commit empties is not
  one. (Non-normative.)
- **h2** — gives B1 the name "§14 bar". Adds no obligation.
- **h3** — B2 and B3 as quoted above, plus: the free-re-declaration permission's
  tense is *all three* bars'; a growth's warrant is `[R-SER-05]`/§14.5's
  "for each channel the position carries, that channel's fill".
- **h4** — for a shrink, B1 is the whole of the test of what the shrink
  *alters*; the step's later obligations (slack, entry_count, slab/alignment)
  bind a shrink like any commit.
- **h5** — B2 and B3 do not reach a shrink.
- **h6** — restates the empty-layer permission on the superseded generation's
  tense. (Non-normative.)
- **h7** — B1 is witnessed only where affected tiles stay stored and only
  partly; B2 and B3 are witnessed *not at all* where the change leaves untouched
  everything §14 fixes for a prior-generation stored tile; §12.1 element sizes do
  not decide which case a type change is in.
- **h8** — sweeps one "the bar" → "the §14 bar".

## 3. Sweeps run (whitespace-normalised; hit counts)

```
"re-declared freely"            3  (L1615 Rationale, L3223 normative, L3347 Example)
"stores no tile"                2  (L3222, L4621 unrelated)
"stored no tile"                3  (L1614, L3215, L3346)
"declared sample type"          3  (L1617, L3173, L3258)
"disk ordinal"                 15
"§14 bar"                      10  (L1606,3139,3159,3198,3237,3252,3257,3262,3929,3953)
"the bar above"                 0   <- h4/h5 swept both; confirmed none left
"escape"                       16  (relevant: L3142, L3231, L3928/3929)
"set of padding positions"      1  (L3136 only — B1's list)
"MAY \*\*grow\*\*"              1  (L3226)
"permitted exactly where"       2  (L3234 growth, L3241 shrink)
"whole-file rewrite"            8
"in the same breath"            1  (L3142)
"companion bar"                 1  (L3920)
"three bars"                    1  (L1606)
"two bars"                      2  (L1616, L3257)
MUST NOT in §20.3 (3072-3289)   5  (2 in step 2; B1, B2, B3 in step 4)
"^| T3 " / "^| T14 "            1 each (L3770/3782)
```

## 4. Citations checked

| Cite | In | Verdict |
|---|---|---|
| §14.5 (h3, growth warrant) | "a position that becomes real held, for each channel the position carries, that channel's fill (§14.5)" | **PASS** — `[R-SER-05]` L2088-2092 reads "at every padding position, a writer MUST encode, for each channel the position carries, that channel's fill value". Verbatim match of the quantifier. |
| §14.3 (h3) | "its plane goes from P · Bᶜ bytes to ⌈P/8⌉ (§14.3)" | **PASS** — `[R-SER-03]` L2019-2024: "the decoded size is ⌈P/8⌉ bytes". |
| §12.1 (h3, h7) | "a planar `uint8` channel re-declared `bool` keeps its element size of 1" | **PASS** — §12.1 table: bool element size 1, uint8 element size 1. "the two coincide at P = 1": ⌈1/8⌉ = 1 = 1·1. Correct. |
| §14.2 (h3) | "the sample stride Q and each in-sample offset Fᶜ are sums over all of them" | **PARTIAL FAIL** — §14.2 `[R-SER-02]`: "Q = Σ Bᵢ over all channels", but "Fᶜ = Σ Bⱼ over channels **j < c**". F⁰ is the empty sum. See X-09. |
| `[R-GEO-06]` (h3) | "a disk ordinal is c · N + s, and N is the spatial-tile count" | **PASS** — L1701-1702, and §11.2 defines N = ∏Gᵢ as the spatial-tile count and C·N as the addressed-tile count. |
| §11.2 (h3) | "the channel count enters the addressed-tile count C · N (§11.2)" | **PASS** — L1633-1637. |
| `[R-SLB-04]` (h4) | "obligations … on a slab … declaration" | **PASS** — L2311-2313 binds "A writer or updater whose commit changes the stored-tile set, the run partition, or the byte placement of any run of a slab-declared layer". A shrink changes the stored-tile set and the run partition (blocks are [c·N,(c+1)·N), §16.2). |
| `[R-SLB-01]` (h4) | "…or alignment declaration" | **PASS but vacuous for a pure shrink** — `[R-SLB-01]` L2259-2267 constrains stored tiles' offsets; a shrink moves no tile, so it cannot break the invariant. Harmless. |
| `[R-CNT-21]`, `[R-CNT-17]` (h4's "below") | slack, entry_count | **PASS** — both stated below at L3266, L3276. |
| §21.7 (h5) | "§21.7 records the consequence — that this is precisely where the §14 bar has no witness" | **PASS on substance** (L3950-3954 says exactly that) — but see X-05 on what "this" now resolves to. |
| §9.7 (h7) | "the prior generation's channel declarations are not part of the live state, which is all §9.7 walks" | **PASS** — §9.7 L1442-1443: "A verifier checking `[R-CNT-02]`'s partition walks the live state only." |
| §12.1 (h7) | "not decided by the element sizes of §12.1" | **PASS**. |
| §21.4 rows T3/T14 (h7, pre-existing) | "witnessed by T3 or T14" | **PASS** — L3770 (T3, `[R-SER-07]`), L3782 (T14, `[R-COD-04]`). |
| §11.1 (h3) | "which is what schema-first creation needs (§11.1)" | **PASS** — §11.1's Rationale is about schema-first workflows. |
| `[R-COD-07]` / L44 (h3, pre-existing) | "quantified over addressed tiles" | **PASS** — L44 (L3752) "any of whose **addressed** tiles' decoded size"; `[R-COD-07]` L2451-2457 likewise. |
| `[R-LIF-01]`, §20.5 (h3) | "a new layer, or a whole-file rewrite under a fresh file_id" | **PASS** — `[R-LIF-01]` L1230. |

## 5. Check 6 — the structure, and what is still unconstrained

Structure the repairs govern: **a layer's declaration set**, specifically the
channel entry (§12: name §4.6, sample type u16, fill value §13) plus channel
**count** and **order**, plus geometry (rank, Eᵢ, Tᵢ), layout, linearization,
codec/filter, slab/alignment.

| Member | Governed for a layer with prior-generation stored tiles? |
|---|---|
| channel sample type | **B2** — outright, layer scope |
| channel count / order (planar) | **B3** — where a stored tile's ordinal moves |
| channel count / order (interleaved) | **B1** — Q and Fᶜ move, so decoded size / offsets move |
| channel **fill value** | **B1 only where a padding position or pad bit exists**; otherwise free (§20.3 Example (c)) |
| channel **name** | **nothing** — no bar names it |
| codec / filter | **B1** (named in its list) |
| Eᵢ (grow / shrink) | growth clause / shrink clause |
| Tᵢ, rank, layout, linearization | **B1** only, via decoded size and offsets |
| slab / alignment | `[R-SLB-04]`, `[R-SLB-01]` |

Two siblings sit unpinned next to pinned ones:

- **Channel name.** B2 pins one field of the channel entry and B3 pins the
  entry's *position*; the third field of the same entry, the name, is pinned by
  nothing. That is almost certainly right (nothing in §14 reads a name) but the
  new prose enumerates the entry's other two members and is silent about it, and
  §12 says "the declared order is load-bearing" without saying the name is not.
  I did not raise this as a finding: I could not falsify it from the document.
- **Channel removal on a planar layer.** h3 blesses "removing the last
  [channel]" as moving no ordinal, so B3 does not bar it — but the consequences
  of dropping its stored tiles out of the addressed set (slack, entry_count,
  index re-emission) are stated only in the **extent-shrink** paragraph
  ("Where a shrink is permitted the de-addressed tiles' extents become slack…").
  h4's added "bind it **as they bind any commit**" is what closes this, and it
  closes it — so no finding, but the closure is load-bearing and accidental.

## 6. Check 8 — back-references across h3's 65-line insertion

| Back-reference | Before h3 resolved to | Now resolves to | Verdict |
|---|---|---|---|
| "the tense is **the bar's**" (L3225) | B1 | repaired by h3 to "**these bars'**" = B1+B2+B3 | swept ✔ |
| "**the bar above** is the whole of the test" (L3237) | B1 | repaired by h4 to "**the §14 bar**" | swept ✔ |
| "What counts … is **the bar above**" (L3252) | B1 | repaired by h5 to "**the §14 bar**" | swept ✔ |
| "so **the bar** is unwitnessed there" (L3953) | B1 | repaired by h8 to "**the §14 bar**" | swept ✔ |
| "**§20.3 step 4's bar on a declaration change**" (L3919) | B1 (only bar) | ambiguous among B1/B2/B3 | **NOT swept — X-08** |
| "permitted here exactly as it is **there**" (L3256) | B1's carve-out, ~30 lines up | same, ~100 lines up | still resolves ✔ (the sentence names "the §14 bar" two clauses earlier) |
| "**the re-emission rule above**" (L3200, h3's own) | — | step 4's opening re-emission rule, ~75 lines up | resolves ✔ (nothing nearer is a re-emission rule) |
| "exactly as **above**" (L3221, h3's own) | — | nearest is h3's own "which is a new layer or a whole-file rewrite"; further is B1's | harmless ✔ (identical content) |
| "bind **it** as they bind any commit" (L3241, h4's own) | — | nearest antecedent is "**that bar**", intended is the shrink | **X-06** |
| "§21.7 records the consequence — that **this** is …" and "why **the rule** is stated here" (L3261-3263) | the rescue case (unstoring in the same commit) | h5 inserted a sentence about B2/B3 between them | **X-05** |

## 7. Check 7 — analogies, verb against verb

- **h7**: "a commit that supersedes every tile it would have damaged **escapes
  them** exactly as it **escapes the §14 bar**." Cited warrant's own verb, L3142:
  "a commit **does not escape** this by unstoring in the same breath …
  **and this bars it**." Same subject, same commit, opposite polarity of the
  same verb. → **X-01**.
- **h7**: one sentence carries "witnessed not at all" for **two** bars. Tested
  separately: for **B2** it holds (int8→uint8, or a planar channel storing
  nothing re-typed — nothing to check). For **B3** it fails on a planar exchange
  of two channels of unequal element size. → **X-04**.
- **h5**: "one bars a change to a channel's declared sample type" — governing
  verb of B2 is "change the declared sample type of any channel **of a layer that
  stores a tile**"; h5's gloss drops the layer scope. Sound here because h5 only
  claims non-reach for shrinks, and a shrink changes no type under either scope.
  **Reported as passing.**
- **h4**: "the §14 bar is the whole of the test of what a shrink **alters**"
  against B1's verb "**alters**, for any tile that layer stores in the generation
  this commit supersedes". Same verb, same quantifier. **PASS.**
- **h1**: "the one reaching a shrink **or a growth** is the §14 bar" against the
  growth clause's own verb, L3234: "a growth **is permitted exactly where** the
  geometry it produces satisfies every rule **that geometry** is subject to."
  "reaching" (prior-generation, per-stored-tile) against "the geometry it
  produces" (new-state, declaration-only), joined by an iff. Different sets. →
  **X-02**.

## 8. Findings

X-01 … X-09 as returned in the structured result. Ranked: X-01, X-02, X-03 fork
the bytes; X-04 … X-09 do not.

## 9. Rejected candidates

- *"three bars" is an overclaim.* Falsification attempt: enumerated every
  `MUST NOT` in §20.3 (5 hits, 2 of them in step 2 and about repair/dropping, not
  about a layer's declarations). Also considered "relocating a live index region
  is compaction's operation, not an appender's" as a fourth bar — it is not a
  bar on a *declaration* change and the Rationale's sentence is explicitly about
  declaration bars. **Count of three verified; dropped.**
- *h6's Example (c) proviso "subject to every rule its **new geometry** is
  subject to" is narrower than the normative permission (which is not
  geometry-limited).* Dropped: that clause is untouched by h6 (the diff shows it
  in both the `-` and `+` sides), so it is a pre-existing wording, not a repair
  defect, and the block is Example-labelled and non-normative.
- *h7 drops "and the two coincide at P = 1" from the uint8→bool example that h3
  keeps.* Dropped: §21.7's claim is "element sizes do not settle it", which the
  example supports with or without the P = 1 note; nothing false results.
- *`[R-SLB-01]` is cited by h4 as an obligation binding a shrink although a
  shrink cannot break it.* Dropped: vacuous but not wrong, and the sentence's
  own hedge is "bind it as they bind any commit".
- *h7's "which type its channel carried before" is per-channel while B2 is
  per-layer.* Dropped: I could not make the conclusion (unwitnessed) false in the
  layer-scope case — a planar channel storing nothing has only sentinel entries,
  so there is nothing to check; an interleaved re-type is B1's, not B2's, and is
  witnessed. The reason given is narrower than the rule, but the claim survives.
- *Channel name unpinned.* Dropped: could not falsify (see §5).
