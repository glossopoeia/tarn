# Cross-hunk consistency audit — r32, one commit, 7 hunks

## 0. Disclosure

Read: `/Users/robertkleffner/Documents/GitHub/tarn-first-draft/spec/tarn.md` (whole file, in
sections, by `sed`/`grep`/a normalising Python script), and
`case/hunk-01.diff` … `case/hunk-07.diff`. I did **not** open `full.diff`, `docs/`,
`PLAN.md`, `OPEN-QUESTIONS.md`, `AGENTS.md`, `README.md`, `conformance/`,
`spec/registry.json`, or any git history. I did run `ls -la` on the case directory
before I had read the brief's "do not list that directory" line; the listing showed only
the seven hunk files, `full.diff`, and their sizes. That is a disclosed breach; nothing in
it informed a finding (sizes only).

Context I did not ask for and disregarded: the runtime placed a `CLAUDE.md` pointer, an
index of maintainer memory notes with TARN-specific titles, and an environment block
naming recent commit subjects (ADR numbers and one-line summaries) in my context before I
began. I did not open any of those files and no finding below rests on them.

Files I wrote, all under my own scratch directory
`/private/tmp/claude-501/.../r32-audit2/scratch/cross-hunk/`:
- `norm.txt` — whitespace-normalised, blockquote-marker-stripped copy of the spec
- `idx.json` — character→line map for the above
and the transcript at `.../r32-audit2/out/audit-cross-hunk.md`.

Header check: every hunk's stated "nearest preceding heading" matched the body I found at
those lines. Hunk 1 says §11.1 (line 1618) — the changed text is the §11.1 **Rationale**
block: matches. Hunk 2 says §13.3 (1902) — the changed text is §13.3's **Note — sparse
writing**: matches. Hunks 3 and 4 say §20.3 (3113): matches (step 4, and the Example's
shape (c)). Hunks 5 and 6 say §23.1 (4139): matches. Hunk 7 says Appendix H (4649):
matches. No mismatch to report.

## 1. The grouping (derived from the text, not the headers)

The commit replaces one rule — "what a commit may change in the declarations of a layer
that already stores tiles" — stated as two bars with carve-outs, by a **closed list**.
Grouped by the rule each hunk touches:

**Group A — the list itself (source + five restatements).**
- **Source, normative**: hunk 3, §20.3 step 4, paragraph beginning "A layer that stores a
  tile **in the generation this commit supersedes** keeps its declarations…". Plain
  numbered-list prose: normative by [R-CNF-01].
- R1 hunk 1, §11.1, block opening "> **Rationale.**" → **non-normative** by [R-CNF-01].
- R2 hunk 2, §13.3, block opening "> **Note — sparse writing.**" → **non-normative**.
- R3 hunk 4, §20.3, block opening "> **Example — the three shapes a commit takes.**",
  shape (c) → **non-normative**.
- R4 hunks 5 + 6, §23.1, plain prose ending `[R-PRV-01]` → **normative**.
- R5 hunk 7, "Appendix H — Conformance checklists (**non-normative**)" → non-normative,
  and the appendix says so itself: "each entry's authority is the requirement or section
  cited, never this summary."

Force test applied: the **label**, not the ">" marker. Three of the five restatements sit
in labelled blocks; one sits in a non-normative appendix; only §23.1 carries force. So the
normative surface of this commit is hunk 3 and hunks 5–6, and every disagreement between
those two and the other four resolves against the other four — which is what decides the
byte-level grading below.

**Group B — the principle and the give-up sentence** (hunk 3, second inserted paragraph),
which must line up with the fixed list of Group A.

**Group C — the re-emission clause and what moves an ordinal**: hunk 3's parenthesis "(a
growth renumbers ordinals wherever `[R-GEO-06]` moves them, and nothing else this step
permits moves one)" against hunk 2's "entry_count — the only way its index content moves"
and against the two untouched statements of the same rule (§5.1's Example at line 678, and
step 4's own trigger at line 3161).

**Group D — the slack / growth / de-addressing obligations**: hunk 3's third paragraph,
hunk 1's growth sentences, hunks 5–6's privacy account.

## 2. The list, held item for item

Permitted side, four members, as each of the four statements words them:

| | source (h3, 3181) | §11.1 Rationale (h1, 1641) | App. H (h7, 4691) | §20.3 (c) (h4) |
|---|---|---|---|---|
| names | "its name, and its dimension and channel names, MAY change" | "its names … may change" | "its names" | "renaming a layer" |
| growth | "an extent MAY grow" | "its extents may grow, subject to every rule the grown geometry is under" | "a grown extent" | — |
| planar channels | "MAY be extended at its end, or shortened from its end" | "may be extended or shortened at its end" | "a planar channel at the end" | — |
| slab/alignment | "**is re-established or cleared** as this step provides below" | "its slab and alignment declarations, **may change**" | "a slab or alignment declaration" | "clearing a slab declaration" |

The slab/alignment row does not agree (finding X-08). The planar-channel row agrees in
substance; App. H's wording ("a planar channel at the end") does not say whether removal is
included. The names row agrees. The growth row agrees.

Fixed side (source only, 3185): "the layout, the linearization and the index encoding, the
codec and the filter, the rank and the dimension order, every tile extent, every channel's
type and fill, an interleaved layer's channel list, and the position of every planar
channel but the last."

## 3. The partition claim, checked against §7.4

§7.4's inline-payload table has **16 field rows** (counted: `awk NR 1087-1107 | grep -c '^|'`
= 18, minus header and separator). The claim is: "The two lists partition §7.4's fields, the
derived ones aside — entry_count, crc_of_crc_array and the extent slot follow the commit."
Two of the 16 rows are set aside by name; the "extent slot" is not a table row at all (it
is the record's slot, described in §7.4's opening sentence). So **14 rows** must fall on one
side or the other.

- permitted: name; alignment A; slab S; (dimension **names** and dimension **extents**
  inside "d dimension entries"); (channel **names** inside "C channel entries")
- fixed: layout; linearization; codec; filter; rank d; index_encoding; (tile extents inside
  "d dimension entries"); (channel types and fills inside "C channel entries")
- assignable only by inference: **slab alignment A_slab** (presumably inside "a slab
  declaration"); **channel count C** (presumably inside "channel list")
- **assignable to neither: `sub-records`** — a §7.4 field row, named in no list and not
  among the three set aside. → X-01.
- Two rows (dimension entries, channel entries) are **split** across the two sides, so the
  claim is a partition of sub-fields, not of fields; and the **dimension extent** is split
  by the *direction* of the change (grow permitted, shrink a rewrite), which no partition
  of a field set can express. → X-10.

## 4. Sweeps run (all with controls; the file is hard-wrapped, "> " included)

Line-oriented, on the raw file:
- `grep -n "shrink\|shrunk\|shrinking"` → **2** (3217, 4157). Control: `grep -c "grow"` →
  **23**. So the old shrink vocabulary is genuinely swept everywhere but the two places the
  commit rewrote.
- `grep -n "§14 bar\|the bar\|carve-out\|carve out"` → 5 hits, **none** about this rule
  ("the barrier", "the bar on sizing a buffer", "the bar is prospective"). Control: the
  same grep hits real text at 2643/3049, so the pattern works.
- `grep -n "re-type\|re-tiling\|transposed"` → 2 (2682 unrelated, 3218 the new give-up
  sentence). `grep -n "de-address\|addressed set"` → 3 (3215, 4146, and 3955's unrelated
  §21.9 sentence).
- `grep -n "at once\|several of these\|in one commit\|in the same commit"` → **2**, neither
  about combining permitted changes (3081 "in one commit" = the creator definition; 3834
  unrelated). Control: `grep -c "commit"` → **193**. This proves the zero I rest X-11 on.
- `grep -n "whole-file rewrite"` → 5 (1246, 3190, 3369, 3433, 4693).
- `grep -n "stores a tile\|stored a tile\|stores no tile\|stored no tile\|stores any tile"`
  → 8, all accounted for above.

Whitespace-normalised (script strips "> " and collapses every run of whitespace, so a
phrase that spans a wrap is still found — proved by the 678 hit below, which spans a line
break and which a line-oriented `grep -n "index content"` **misses**, reporting 1 hit
instead of 3):
- `"index content"` → **3**: 678 (§5.1 Example, non-normative), 1945 (hunk 2's Note),
  3161 (step 4, normative). Control in the same run: `"stored-tile set"` → **6**, including
  the same wrapped line 678.
- `"keeps its declarations"` → 1 (3179). `"fixed declaration"` → 2 (3203, 3311).
- `"re-declared"` → 3 (1646, 3199, 3315). `"MAY be re-declared"` → 1 (3198).
- `"channel list"` → 3 (1641, 3181, 3188). `"at its end"` → 2. `"from its end"` → 1.
  `"last channel"` → 1 (4145).
- `"alignment declaration"` → 3 (1642, 3182, 4692). `"slab declaration"` → 8.
- `"turns real positions"` → **0** (the old privacy wording is gone); control
  `"into padding"` → 1, the new sentence at 4156, so the search reaches that passage.
- `"sub-record"` → 86; `"partition"` → 11 (3191 is the claim).
- `"entry_count"` → 42.

## 5. Citations opened and checked

| citation (in repaired text) | verdict |
|---|---|
| §7.4 "fields" (h3) | resolves; 16 field rows; **fails** the partition claim (X-01, X-10) |
| §3.1 defines *stored* against a generation (h3) | §3.1 is "Terms"; the tense clause's use is consistent with §20.3's own usage — pass |
| `[R-LIF-01]`, §20.5 (rewrite escape, h3) | pass — §20.5 is compaction/whole-file rewrite, `[R-LIF-01]` sanctions a fresh file_id rewrite (3369) |
| §11.1 (schema-first creation, h3) | pass — §11.1's [R-GEO-02] and its Rationale are exactly that |
| §14 / §14.5 (h3, h4) | pass — §14.1 value sequence, §14.2 byte layout, §14.5 [R-SER-05] "at every padding position, a writer MUST encode … that channel's fill value" |
| §11.4 "assigns its ordinal and its values' coordinates" (h3) | resolves ([R-GEO-06], s = Σtᵢ·∏Gⱼ; disk ordinal c·N + s) — but see X-03: the grid counts §11.4 uses are derived from the **extents**, which the same paragraph permits to change |
| §8 "every checksum" (h3) | pass |
| **§21.7 (h3, "no check any actor owes able to see it")** | **fails** — X-04; §21.7 defines *unwitnessed*, and T3/T14/T2 witness several of the fixed declarations |
| `[R-COD-07]` L44, "quantified over addressed tiles" (h3) | pass — L44: "any of whose **addressed** tiles' decoded size exceeds 0x7E000000 … in a planar layer the largest channel plane governs" |
| `[R-ENC-04]` 2⁶³−1 (h3) | pass (L1/L2) |
| §5.2 slack, `[R-CNT-21]`, `[R-CNT-17]`, §15.2, `[R-SLB-04]`, `[R-SLB-01]`, `[R-CNF-05]` (h3) | all resolve; `[R-CNT-17]` does tie entry_count to the addressed-tile count and extent_length |
| §20.4 licences the drop (h4) | resolves — MU=0/PE=0 row: "an updater MAY drop the record in any commit it is otherwise free to make"; **collides** with the closed list (X-01) |
| "which is the same step's permission" (h4, untouched context) | **fails** — X-14; the rewritten step attaches the geometry proviso to a growth, not to the empty layer's free re-declaration |
| §20.3 step 4 (h5, h6, h7) | resolve |
| §15.2 sentinel (h5) | pass |
| §11.1, §20.3, `[R-WRT-04]` (h2) | resolve; but the sentence they support no longer matches §20.3 (X-07) |
| `[R-GEO-06]` (h3 re-emission parenthesis) | pass |

## 6. Anaphora (check 8), every back-reference I resolved

- h3, "A commit MUST NOT change one of **these**" → the fixed enumeration. Unchanged
  resolution; correct.
- h3, "**The two lists**" → permitted + fixed. Correct.
- h3, "The permitted changes touch none of **that**" → the §14/§11.4 characterisation.
  Correct as a referent; false as a claim (X-03).
- h3, "as **this step** provides below" → step 4's last paragraph. Correct.
- h3, "**the list** is not offered as exhaustive" → the bounds list ([R-COD-07],
  [R-ENC-04]). Same antecedent as before the rewrite; not disturbed by the new "two lists"
  wording three paragraphs earlier — a reader reaches for the nearer one.
- **h4, "a layer that stored a tile in *that generation*"** → **no antecedent**. Before
  this commit, the preceding clause read "…in any tile the layer stores **in the generation
  the commit supersedes**"; hunk 4 deleted that clause and left the anaphor. The nearest
  naming of a generation is now the *following* sentence. → X-06.
- h4, "any extent **it** owned" → the PE = 0 record. Unchanged; correct.
- h5, "**the same way**" → made unreachable rather than erased. Unchanged; correct.
- h5, "which is **the case** most likely to strand content" → editing a user-metadata
  document. Unchanged; correct.
- h6, "**they** remain in the file as slack" → the bytes. Correct.
- h6, "**That** is every case" → the "Where the structure … leaves the live state" branch.
  Before the rewrite this read "**Those two cases** are exhaustive", naming two bolded
  branches; one branch is gone, and "that" now resolves to the single surviving branch.
  Readable; not a defect on its own.
- h6, "the list of operations **above**" → the three-operation list in §23.1's first
  sentence. Unchanged; correct.
- h1, "**Growth** that leaves entry_count unchanged" → a bare noun, not an anaphor; its
  neighbouring sentences changed but its sense did not.
- h7, "makes any other change to **it**" → the layer. Correct.

## 7. Analogies (check 7), both verbs quoted

- h6: "a channel removal reported as erasure **misleads** exactly as a supersede so
  reported **does**." Same verb, same subject class (a commit that makes sample data
  unreachable). Ranges over the same set. **Passes.**
- h3: "…`[R-COD-07]`'s lz4 decoded-size cap … which an empty layer **escapes** only because
  that cap **is quantified over addressed tiles**." L44's verb: "Codec 4 (lz4) **declared
  on a layer any of whose addressed tiles' decoded size exceeds**…". Same quantifier
  (addressed). **Passes.** (Unchanged text, re-checked.)
- h3: "The fixed declarations **are** the ones §14 **reads a stored tile under** … and the
  ones §11.4 **assigns** its ordinal and its values' coordinates **by**." §14's verb:
  "defines the decoded tile image: the byte sequence a stored tile's payload decodes to";
  §11.4/[R-GEO-06]'s verb: "The **disk tile ordinal**, which **orders** tile-index
  entries … is s for an interleaved layer, and c · N + s for a planar layer". The two
  ranges are **not** the same: §11.4's ordinal is computed from the grid counts Gᵢ =
  ⌈Eᵢ/Tᵢ⌉, i.e. from the **dimension extents**, which this very paragraph's permitted list
  lets a commit change. The analogy is doing work its words do not support. → X-03.
- h3, give-up sentence: "…are rewrites **even where a particular file would survive them in
  place**, because deciding which files would is the edge this list exists to remove." Not
  an analogy; a policy statement. Tested against the fixed list instead (X-02, X-15).

## 8. Em-dash nesting

I read every new sentence in all seven hunks for an em-dash pair inside a clause itself set
off by em-dashes. h3 has three single pairs (3203–3205, 3231, 3245) and two lone dashes;
h1 one lone dash in untouched text; h4 one pair; h5 one lone dash; h6 none; h7 one pair set
off by semicolons, not dashes. **No NESTED_DASH finding.**

## 9. Findings — see the structured return

X-01 … X-16 as returned. Byte-level grading rule applied throughout: a non-normative
restatement that is broader or narrower than the normative rule does not move the emittable
set, because [R-CNF-01] makes the normative statement govern. That knocks X-05, X-06, X-07,
X-08, X-09 and X-14 down to non-byte-level even where the substantive disagreement is
sharp. The two I do grade byte-level (X-01, X-02) are disagreements **inside normative
text** whose disputed file is itself conforming.
