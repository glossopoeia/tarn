# Repair audit — hunks 8 and 9 (§21.7, "What no check detects")

Working transcript. Written for someone checking my work, not a summary.

## 0. Disclosure

Files opened:

- `/private/tmp/.../scratchpad/case-adr0113/hunk-08.diff`
- `/private/tmp/.../scratchpad/case-adr0113/hunk-09.diff`
- `/Users/robertkleffner/Documents/GitHub/tarn-first-draft/spec/tarn.md` (many
  ranges, listed below)

Nothing else. I did not open `full.diff`, any other hunk file, `docs/`,
`OPEN-QUESTIONS.md`, `AGENTS.md`, `PLAN.md`, `conformance/`, `spec/registry.json`,
git history, or the web. I did not list the case directory (I addressed the two
hunk files by their charter-given paths). I wrote exactly one file, this one.

Commands run: `wc -l`, `sed -n`, `grep -n`, `grep -c`, and two `python3` heredocs
that read only `spec/tarn.md` and did arithmetic. All exact greps and their hit
counts are in §5 below.

**Context I did not ask for.** Material was present in my context before I began:
a project instruction file pointing at another file in the repo, a memory index
naming two prior-round notes by title, and an environment block containing a
`git status` snapshot with modified-file names and five recent commit subject
lines. That commit-subject material names prior rounds' dispositions and a
document not in my access set. I did not open any of it and I have not used it:
no conclusion below rests on it. Disclosing per the charter.

Spec ranges read in full: §11.1 (1584–1630), §11.2 head, §12.1 head, §14 entire
(1919–2116), §16 entire (2242–2345), §20.3 (3070–3270), §20.5 fragment
(3440–3462), §21.1 (3541–3624), §21.2 head + rows, §21.3/§21.4/§21.5 heads and
rows, §21.6 (3807–3860), §21.7 entire (3861–3944), §21.8 (3946–3951), §21.9
(3952–4000), §9.7 (1440–1496), §2.3/§2.4 fragments (195–215, 280–300).

---

## 1. The hunks, and where they land

### Hunk 8

Header claims: lands at 3897–3911, nearest preceding heading line 3861
`#### 21.7 What no check detects`. **Verified against the body**: line 3861 is
indeed `#### 21.7 What no check detects`, and the changed lines are 3895–3911 in
the current file. No mismatch.

Before → after, the substance:

- BEFORE: `…§20.3 step 4's bar on a declaration change is witnessed only where
  the affected tiles remain stored, and then only for part of what it bars. A
  change reaching a byte §14 structurally constrains — a padding position, a pad
  bit, or a boolean byte — fires §21.4's content rows. A change reaching the
  decoded size is witnessed by T3 or T14, …`
- AFTER: the full stop after "what it bars" becomes a comma, and this is inserted
  before "A change reaching a byte §14…":

  > bars, and its two companion bars are witnessed not at all where the change
  > leaves untouched everything §14 fixes for a tile the layer stores in the
  > generation the commit supersedes — the prior generation's channel
  > declarations are not part of the live state, which is all §9.7 walks, so no
  > check can know which ordinal a stored tile used to occupy, or which type its
  > channel carried before. Where the change does touch one of those, and the
  > tile it touches remains stored, the rows below witness it; a commit that
  > supersedes every tile it would have damaged escapes them here exactly as it
  > does the §14 bar. Which case a type change falls in is not decided by the
  > element sizes of §12.1: a planar `uint8` channel re-declared `bool` keeps its
  > element size of 1 while its plane goes from P · Bᶜ bytes to ⌈P/8⌉.

### Hunk 9

Header claims: lands at 3930, same heading. **Verified**: line 3930 is inside
§21.7 and inside the *same paragraph* as hunk 8 (the paragraph runs 3879–3944 and
closes with `[R-ERR-01]`). One word inserted:

- BEFORE: `so the bar is unwitnessed there for the same reason [R-LIF-01] is`
- AFTER: `so the §14 bar is unwitnessed there for the same reason [R-LIF-01] is`

### The rule each repair adopts, in my own words

**Hunk 8.** For an implementation: the two obligations §20.3 step 4 states beside
the §14 bar — (A) a commit MUST NOT change any channel's declared sample type in
a layer that stored a tile in the superseded generation; (B) for a planar layer,
a commit MUST NOT change the channel declarations so as to move a stored tile's
disk ordinal — leave no trace in a single file whenever the change does not also
alter something §14 fixes for a prior-generation stored tile, because the only
thing a checker walks is the live state and the live state does not carry the
prior generation's channel declarations. Where the change *does* alter such a
thing and the tile survives, hunk 8 asserts the register rows named in the rest
of the paragraph catch it. And it asserts that unstoring every damaged tile puts
the commit beyond those rows the same way it does for the §14 bar.

**Hunk 9.** Of the three bars, it is specifically the §14 bar whose violation is
undetectable when the commit supersedes every tile it damaged. (Before the word
was added, "the bar" had three candidate antecedents; after hunk 8 there are
demonstrably three.)

---

## 2. The two companion bars — located and quoted

`grep -n "§14 bar" spec/tarn.md` → 10 hits (1606, 3137, 3157, 3181, 3218, 3230,
3235, 3239, 3906, 3930).

§20.3 step 4, line 3128–3138, defines the **§14 bar**:

> A commit MUST NOT change a layer's declarations in a way that alters, for any
> tile that layer stores **in the generation this commit supersedes**, what §14
> fixes for its stored bytes or how they decode — the set of padding positions
> (§11.3) and the content `[R-SER-05]` fixes there, the decoded size, the byte
> offset of any sample within the decoded tile image, or the codec and filter
> that produced the stored bytes. Call this the **§14 bar**, the name the rest of
> this step and §21.7 use for it.

**Companion bar A** (line 3169–3173):

> So the change is barred outright rather than by cases: a commit MUST NOT change
> the declared sample type of any channel of a layer that stores a tile in the
> generation this commit supersedes, whatever the layer's layout and whether or
> not the element size moves.

**Companion bar B** (line 3179–3187):

> A further effect is barred on the same tense and for the same reason, and the
> §14 bar does not reach it because it is not an effect on any stored tile's
> bytes: for a **planar** layer, a commit MUST NOT change the channel
> declarations in a way that alters the disk ordinal `[R-GEO-06]` assigns any
> tile the layer stores in the generation this commit supersedes.

Count check for "its two companion bars": §20.3 line 3235–3237 says "Neither of
the **two** bars beside the §14 bar reaches a shrink: one bars a change to a
channel's declared sample type and the other a change to the channel
declarations". §11.1's Rationale (line 1605–1616) says "Of its **three** bars…
The other **two** bars… they bar a change to a channel's declared sample type,
and a change to a planar layer's channel declarations that moves a stored tile's
disk ordinal." **"two companion bars" is correct.** (Check 5 pass.)

Note on §11.1: that block opens `> **Rationale.**` — labelled, therefore
non-normative under `[R-CNF-01]`. It is corroboration of the count, not the
source of it; the normative source is §20.3 step 4.

---

## 3. Check 3 — normative placement (label test, not marker test)

`[R-CNF-01]` sits at line ~100–106 and ends `non-normative. [R-CNF-01]`. I applied
the **label** test, not the `>` test.

The paragraph the repairs land in (3879–3944) has **no `>` marker on any line**
and **no Note/Example/Rationale label**. It closes with the requirement
identifier `[R-ERR-01]` at line 3944. §21.7 is therefore normative text in full,
and both repairs land in normative text. The `[R-CNF-01]` carve-outs (§1, labelled
blocks, non-normative appendices) do not reach it.

The blocks I *did* find carrying restatements of the same rules, and their labels:

- line 1604 `> **Rationale.**` — §11.1's account of the three bars. **Labelled →
  non-normative.** It agrees with §20.3, so no failed-to-land problem.
- line 3269 `> **Note.**` — §20.3's commit-cost note. Not about the bars.
- line 3324 (in a `>` block) — "generation the commit supersedes is re-declared
  freely, subject to…". I checked its label: it is inside a Note in §20.4.
  Non-normative, agrees with §20.3 line 3204.

**No case here of a rule whose only statement is in a labelled block, and no case
of a repair editing a labelled block while the normative statement says the old
thing.** Check 3 passes for both hunks.

---

## 4. Check 2 — every citation in the repaired text, opened

| Citation in repaired text | Claim made about it | Verdict |
|---|---|---|
| `§20.3 step 4` (line 3895) | has a "bar on a declaration change" plus two companion bars | **PASS.** Lines 3128–3138 (§14 bar), 3169–3173 (A), 3179–3187 (B). |
| `§14` (line 3898, "everything §14 fixes") | fixes things for a stored tile's bytes | **PASS.** §14.2 `[R-SER-02]`/`[R-SER-08]`, §14.3 `[R-SER-03]`, §14.3 closing `[R-SER-07]`, §14.5 `[R-SER-05]`. Note `[R-SER-08]` (bool bytes) is at line 1985, *inside* §14.2 — so "everything §14 fixes" does include bool-byte content. I checked this specifically because §21.7 line 3871 writes "§14.5 and `[R-SER-08]`" as if they were siblings; they are not, `[R-SER-08]` is in §14.2 and §14.5 is `[R-SER-05]`. Both are in §14, so the repair's phrase is right. |
| `§9.7` (line 3901, "which is all §9.7 walks") | walks the live state only | **PASS.** §9.7 line 1442: "A verifier checking `[R-CNT-02]`'s partition walks the live state only." Its closing Note: "Nothing here enumerates prior commits." |
| `§12.1` (line 3907, "the element sizes of §12.1") | defines element sizes | **PASS.** §12.1 line 1750: "**element size** is the byte length of one encoded value of that type"; line 1755: "a bool's element size of 1". |
| `` `uint8` → `bool` ``, `P · Bᶜ`, `⌈P/8⌉` (3907–3909) | planar uint8 plane is P·Bᶜ, planar bool plane is ⌈P/8⌉ | **PASS on the formulas.** §14.2 table: planar numeric channel c → `P · Bᶜ`. §14.3: "the decoded size is ⌈P/8⌉ bytes". **FAIL on completeness** — see C-04: §20.3's own version of this sentence (3166–3169) ends "and the two coincide at P = 1", and §14.4's Note says the same; §21.7's restatement drops it. |
| `§21.4` (line 3911, pre-existing) | has content rows | PASS (T2, T4, T5 at 3747–3750). |
| `T3`, `T14` (3911–3913, pre-existing) | test a length | PASS (rows 3748, 3759). |
| `[R-LIF-01]` (hunk 9's sentence, 3931) | is unwitnessed because it is a property of the prior generation | PASS — same paragraph line 3880–3883 states it, and §9.7's Note confirms. |
| `§14 bar` (hunk 9's inserted words, 3930) | is the bar §20.3 says has no witness where the live state is left clean | **PASS.** §20.3 line 3238–3240: "§21.7 records the consequence — that this is precisely where the **§14 bar** has no witness, the live state being clean". Hunk 9's narrowing makes §20.3's forward reference land on the right sentence. |

---

## 5. Sweeps run (verbatim, with hit counts)

All against `/Users/robertkleffner/Documents/GitHub/tarn-first-draft/spec/tarn.md`.
The document is hard-wrapped, so every phrase below was chosen short enough not
to wrap, and I cross-checked the long ones by reading the passage.

```
grep -c "companion bar"        1     (3897 — the repair itself; nowhere else)
grep -c "§14 bar"             10     (1606 3137 3157 3181 3218 3230 3235 3239 3906 3930)
grep -c "escape"              10     (incl. 3140 "does not escape this", 3905 "escapes them here")
grep -c "unwitnessed"          3     (3919 3930 3935)
grep -c "no witness"           3     (2607 3880 3925)
grep -c "witnessed"            9     (3889 3895 3897 3911 3914 3919 3921 3930 3935)
grep -c "declared sample type" 2     (1615 3171)
grep -c "sample type"         11
grep -c "re-declared"          5     (1613 3167 3204 3324 3907)
grep -c "supersedes"          16
grep -c "coincide at P = 1"    1     (3169 — §20.3 only; NOT at 3907)
grep -c "element size"        19
grep -c "rows below"           2     (3780 §21.5; 3904 the repair)
grep -c "one of those"         4     (20 593 3144 3903)
grep -c "does touch"           1     (3903 — the repair)
grep -c "would have damaged"   2     (3905 the repair; 3929 pre-existing)
grep -c "no check can know"    2     (3901 the repair; 3937 pre-existing)
grep -c "not decided by"       1     (3906 — the repair)
grep -c "below witness"        1     (3904 — the repair)
grep -n "§21.7"                9     (2518 2610 3138 3238 3455 3558 3577 3771 + heading)
grep -n "R-SER-08"            10
grep -n "R-CNF-05"             8
grep -n "R-CNF-01"             1     (106)
grep -n "R-ERR-01"             1     (3944)
grep -n "R-GEO-06|R-SER-01|R-LIF-0[0-9]"  (48 hits; used to find §20.3's bars and §9.7)
grep -n "^#### 1[1-7]\.|^### 1[1-7]\."    (section index for §11–§17)
grep -n "^#### 2[01]\.|^### 2[01]"        (section index for §20–§21)
grep -n "| T14 || T3 || T15 || T17 || T23 || T25 || T26 |"  (7 rows read in full)
```

Negative results worth recording: **"coincide at P = 1" appears once, at 3169
(§20.3), and not in §21.7.** That single hit is the whole of finding C-04.
**"companion bar" appears once** — the repair coined the term and nothing else in
the document uses it, so there is no other site to sweep for it.

---

## 6. Derived numbers — the recount

The charter asks me to recount the per-subsection condition counts and the §21.8
totals where these hunks touch them.

First the load-bearing structural fact, from §21.1 line 3573–3578:

> The subsections after §21.5 are not part of the register and carry no rows:
> neither this completeness clause nor the instance arithmetic below reaches
> §21.6's defined non-violations, §21.7's account of what no check detects, or
> §21.9's limits.

So hunks 8 and 9, both wholly inside §21.7, cannot move a count. I recounted
anyway, mechanically, from the tables themselves. Instance counting rule taken
from §21.1: "Instances within a cell are separated by semicolons, and a cell
reading — is one instance; the count is therefore mechanical once the cell is
written."

Script: split each table row on `|`, take field 3 (Instances), count 1 if it is
`—` else count semicolon-separated non-empty parts.

| Subsection | Rows I counted | Printed figure | Instances I counted |
|---|---|---|---|
| §21.2 File-scope | 35 | "35 conditions" (3627) | 56 |
| §21.3 Layer-scope | 49 | "49 conditions" (3682) | 116 |
| §21.4 Tile-scope | 26 | "26 conditions" (3742) | 55 |
| §21.5 Ignored records | 10 | "10 conditions" (3792) | 48 |
| **Total** | **35+49+26+10 = 120** | §21.8: "120 conditions" | **56+116+55+48 = 275** |

§21.8 (line 3947–3949) prints: "Every row of §21.2 through §21.5 — 120 conditions
over 275 instances — has at least one conformance vector (§24) whose expected
outcome is that row's outcome, and one vector per instance."

**120 = 120 ✓. 275 = 275 ✓.** Every per-subsection figure matches. The repairs
owe no recount.

Per-row instance counts for §21.5, printed as a spot check of my method (the
sub-total 48 is the one most sensitive to a miscount, R4 alone carrying 16):
R1 4, R2 2, R3 2, R4 16, R5 8, R6 4, R7 6, R8 2, R9 2, R10 2 = 48.

---

## 7. Is a register row owed for either companion bar?

§21.1's completeness rule, lines 3545–3560:

> The register — §21.2 through §21.5 (`[R-ERR-02]`) — enumerates every
> **detectable** file-conformance violation this specification names … Its
> **completeness is normative** — a *detectable* file-conformance violation this
> specification names and the register omits is a defect in this document,
> detectability being the gate `[R-CNF-07]` already applies and §21.7 the
> account, by class, of what fails it.

Applying it:

**Bar A (sample type).** Is a violation detectable from one file? The only record
of a channel's type in the live state is the current declaration. Nothing in the
file records a previous one — §9.7 walks the live state only, and its Note says
"Nothing here enumerates prior commits". So no. What *is* detectable in the
sub-case where the change also altered a §14 quantity is the resulting structural
condition — a decoded payload whose length is not the derived decoded size (T3,
governed by `[R-SER-07]`), an index entry length disagreeing under codec 1 (T14),
a bool byte that is neither 0x00 nor 0x01 (T2), padding not carrying fill (T4,
T5). Every one of those already has a row. There is no separate file predicate
"the declared type changed". **No row owed.**

**Bar B (planar ordinal).** Same, and stronger: nothing in the resulting file even
differs. I constructed the cases (see §8 below) and none produces a structural
condition at all. **No row owed.**

Consequently §21.2–§21.8's counts stand, which is what my recount in §6 shows
independently.

I also checked the converse direction — whether §21.7's account, now that it
claims *some* of these violations are witnessed, creates a gap. It does not: the
witnessing conditions it names are already rows (T2, T3, T4, T5, T14, T15, T17,
T23, T25, T26). The problem with the claim is that it is too strong, not that it
implies a missing row. That is C-01.

---

## 8. Check 1 (tense and quantifier) and the case construction

Both bars are quantified over **the superseded generation** — "in the generation
this commit supersedes" appears verbatim in both (3172, 3185–3186). The repair
writes "for a tile the layer stores in the generation the commit supersedes"
(3898–3899): same tense, same set, article shifted from "this commit" to "the
commit" because §21.7 is not inside the procedure. **Quantifier match: pass.**

Note the shape difference the repair does *not* reproduce, and does not need to:
Bar A ranges over **any channel of a layer that stores a tile** — the retyped
channel need not itself store anything. Bar B ranges over **any tile the layer
stores** whose ordinal moves. The repair's condition ("where the change leaves
untouched everything §14 fixes for a tile the layer stores…") is a condition on
*witnessing*, not a restatement of either bar's trigger, so the mismatch is not a
defect. I checked the vacuous corner: a planar layer storing tiles for channel
`a` only, commit re-types channel `b`. Bar A is violated; nothing is damaged;
"witnessed not at all" holds. Pass.

### Cases I built, and what each yields

Layout of the test: does a violation of A or B ever leave a witness where §14 is
untouched (which would make "witnessed not at all" too wide), and does a
violation ever leave *no* witness where §14 *is* touched (which would make "the
rows below witness it" too strong)?

**B-1. Planar layer, channels (`a` uint8, `b` uint8), N = 2, both stored.
Exchange `a` and `b`.** Disk ordinal is c·N + s (§11.4, quoted in §20.3 at 3190):
`a` moves 0,1 → 2,3 and `b` 2,3 → 0,1. Bar B violated. §14: each plane's own type,
decoded size, padding, codec, filter unchanged. Witness? entry_count = C·N = 4,
unchanged. The index is re-emitted with each entry at its new disk-ordinal
position. Result is a self-consistent live state. **No witness.** Claim holds.

**B-2. Same, with a slab.** I went looking for a witness in §16, because a slab
invariant is stated over *disk ordinals*, which is exactly what B moves.
`[R-SLB-02]`: "for a planar layer each channel block [c·N, (c+1)·N) — runs never
span channel blocks. Run r of a block starts at ordinal block_start + r·S."
`[R-SLB-03]`: within each run, stored tiles contiguous and packed in ordinal
order, first stored tile's offset ≡ 0 mod A_slab. Under a permutation of channel
blocks every block has the same size N and the same internal ordering, so each
run's membership and internal order are carried over intact and both invariants
survive. Same for inserting or removing a channel: blocks shift wholesale, run
structure inside a block is unchanged. **No witness.** Also checked `[R-SLB-01]`
per-tile alignment: `offset mod A = 0` is ordinal-independent. **No witness.**
This was my best candidate for falsifying "witnessed not at all" and it fails.

**B-3. Planar (`a`,`b`,`c`), remove `b`.** `c` moves from ordinals 4,5 to 2,3.
Bar B violated. entry_count falls 6 → 4, index re-emitted, `b`'s extents become
slack (`[R-CNT-21]`). Self-consistent. **No witness.**

**B-4. Append a channel / remove the last.** §20.3 3187–3193 says these move no
ordinal. Confirmed by the formula c·N + s. **Not a Bar B violation at all.**

**A-1. `int8` → `uint8` (any layout).** §20.3 3161–3164 states this case
explicitly: "moves no stored byte, no decoded size and no sample offset, leaves
every content rule §14 states over those bytes satisfied exactly as before".
§14 untouched. **No witness.** Claim holds.

**A-2. Planar `uint8` → `bool`, P > 1.** Plane P·1 → ⌈P/8⌉. §14 touched (decoded
size). T3 fires on every stored tile that survives. **Witnessed.** This is the
repair's own example.

**A-3. Planar `uint8` → `bool`, P = 1.** ⌈1/8⌉ = 1 = P·1. Decoded size unchanged,
so **T3 and T14 are silent**. §14 is still touched — the byte's bits 1–7 are now
pad bits and `[R-SER-05]` fixes them to the channel's fill bit — so the witness,
if any, is T5, and T5 fires only if those seven bits are not the fill bit. Stored
byte 0x01 with fill false: conforming as a bool plane, **no witness**. This is the
case §20.3 flagged with "the two coincide at P = 1" and §21.7 dropped. → C-04,
and a second instance of C-01.

**A-4. Interleaved, channels (`a` uint8, `b` uint16) re-declared (`a` uint16,
`b` uint8).** Q = ΣBᵢ = 3 both before and after, so decoded size P·Q is unchanged
→ T3 silent, T14 silent. In-sample offsets Fᶜ = ΣBⱼ (j < c) move: F_b goes 1 → 2,
and `a` grows from one byte at offset 0 to two. So "the byte offset of any sample
within the decoded tile image" — an item on the §14 bar's own list at line
3135–3136 — **is** altered. The tiles remain stored. Rows: T2 needs a bool
channel (none); T4/T5 need padding positions or pad bits, and a layer whose
extents are exact multiples of its tile extents has neither (§11.3, §14.3's Note:
"A plane can have many padding positions and no pad bits"); the codec and filter
declarations are untouched so T15/T17/T23/T25/T26 are silent; the stored bytes
still decode. **No row fires.** → C-01's primary counterexample.

I checked the one row that might have caught A-4 by accident: L30, "A channel
entry's fill length prefix differs from the element size of the channel's
declared type" (line 3715). A writer performing A-4 swaps the two fill length
prefixes along with the types in the same commit; nothing forces it to leave them
stale. So L30 is not a witness of the type change — it is a witness of a
separately careless edit. Same reasoning disposes of §13.2's per-type fill
constraints. Recorded as a rejected candidate.

**A-5. Interleaved `uint8` → `bool`.** Element size 1 both ways, Q unchanged,
decoded size unchanged. §14 *is* touched, because `[R-SER-08]` (line 1985, inside
§14.2) now fixes those bytes to 0x00/0x01. If the stored uint8 samples were a
mask already holding only 0 and 1, T2 does not fire, T4 does not fire if the fill
byte likewise coincides, and **no row fires**. Third instance of C-01.

**Conclusion of the case work.** "witnessed not at all where the change leaves
untouched everything §14 fixes" — I could not falsify it; B-1..B-4 and A-1 all
confirm it and B-2 was a serious attempt to break it. **That half of the repair is
sound.** "Where the change does touch one of those, and the tile it touches
remains stored, the rows below witness it" — falsified three separate ways
(A-3, A-4, A-5). **That half is wrong.**

---

## 9. Check 4 — contradiction inside the passage, including untouched text

The repair's new sentence, line 3902–3904:

> Where the change does touch one of those, and the tile it touches remains
> stored, **the rows below witness it**

The same paragraph, lines 3913–3919, **untouched by the repair**:

> A change reaching the codec is *sometimes* witnessed by the rows for the codec
> now declared … or by T14 where the new declaration is codec 1 — **but neither
> is assured**: a writer can choose stored bytes that satisfy the old declaration
> and the new one alike, and **the change is unwitnessed there**.

And lines 3919–3925, **untouched by the repair**:

> A change reaching the filter, or moving a sample's byte offset within the
> decoded image without changing that image's length, is witnessed on the same
> terms T26 states for a wrong stride: where the resulting image breaks §14.5's
> padding content or `[R-SER-08]`'s bool bytes, the check that detects it is T2's
> or T4's, exactly as T26 has it, **and where it breaks neither there is no
> witness**.

The codec and the filter and the sample byte offset are all on the §14 bar's own
list (3133–3137). So the inserted sentence says "the rows below witness it" of
exactly the three quantities the rows below say are not assuredly witnessed. This
is a repair widening a claim into a carve-out that the passage already contained.
Row T26 itself carries the carve-out in the register: "(a wrong stride with no
such structural constraint is undetectable, §21.7)" — the register points *at*
§21.7 for the undetectable case, and §21.7 now says the rows catch it. → **C-01**.

The second contradiction, this one against §20.3 rather than within §21.7. Repair,
3904–3906:

> a commit that supersedes every tile it would have damaged **escapes them here
> exactly as it does the §14 bar**.

§20.3 step 4, 3138–3142, untouched:

> The tense is the prior generation's (§3.1 defines *stored* against a
> generation), so **a commit does not escape this by unstoring in the same
> breath**: superseding every tile of a layer and re-declaring it are one
> operation, and this bars it.

Same subject ("a commit that supersedes every tile"), same verb ("escape"),
opposite polarity, and "this" in §20.3 is the §14 bar. §20.3 says it a second
time at 3204–3207 ("a commit does not earn this permission by emptying the layer
as it re-declares it") and a third at 3222–3226 ("Unstoring that tile in the same
commit does not rescue it either"). → **C-03**.

I looked for, and did not find: a MUST elsewhere in §21.7 that the repair's new
text lets an actor violate (§21.7 states no obligations of its own — it closes
with `[R-ERR-01]` and its content is descriptive of detection); a sentence written
only for the old wording (the old text's flow "…only for part of what it bars. A
change reaching a byte §14…" survives intact as a sentence, though see C-05 for
what happened to its antecedent).

---

## 10. Check 5 — exhaustive claims in the repaired text

| Word/claim | Falsification attempt | Verdict |
|---|---|---|
| "its **two** companion bars" | Counted the bars in §20.3 step 4: §14 bar (3128), sample type (3169), planar ordinal (3179). §20.3 3235 and §11.1's Rationale both say two beside the §14 bar. | **Holds.** |
| "witnessed **not at all**" | B-1..B-4, A-1; slab invariants (§16); per-tile alignment; entry_count. | **Holds** (see §8). |
| "**no check** can know which ordinal … or which type" | Scoped in the same sentence by "the prior generation's channel declarations are not part of the live state, which is all §9.7 walks". §9.7 confirms. A §9.6 recovery scan can reach an earlier trailer, but §9.6 is "not a reader behavior" (its own heading) and produces output that must be re-verified whole; it is not a check on this file. | **Holds**, narrowly. Recorded as a rejected candidate. |
| "the rows below **witness it**" (unqualified) | A-3, A-4, A-5. | **Fails → C-01.** |
| "**Which case** a type change falls in" (a closed two-case split) | The split is witnessed/unwitnessed. A-3 shows a third posture — contingent on stored byte values — which the paragraph's later sentences name ("*sometimes*") but this sentence's binary does not. | Folded into C-01/C-04. |
| "its plane **goes from** P · Bᶜ bytes to ⌈P/8⌉" | P = 1: 1 → 1. §20.3 says so in terms; §14.4's Note says so. | **Fails → C-04.** |
| "exactly as it does the §14 bar" | §20.3 3140. | **Fails → C-03.** |

---

## 11. Check 6 — what the repair left unconstrained in this structure

The structure is §20.3 step 4's set of prohibitions on an in-place declaration
change, and §21.7's account of which of them a single file can witness. I
enumerated every member of that set from §20.3 step 4 and asked, for each,
whether §21.7 now accounts for it:

1. **§14 bar** (3128) — accounted for: 3895–3896 and 3928–3931.
2. **Sample-type bar** (3169) — accounted for by the repair.
3. **Planar-ordinal bar** (3179) — accounted for by the repair.
4. **Index re-emission at disk-ordinal position**, with "(a geometry change
   renumbers ordinals wherever `[R-GEO-06]` moves them)" (3117–3125) — an
   appender that fails to renumber after a geometry grow leaves tiles claimed by
   the wrong channel. Witnessed only if the channels' element sizes differ
   (T3), unwitnessed otherwise. §21.7 does not name this obligation. I judged it
   **covered in class** by the repair's own newly general clause "no check can
   know which ordinal a stored tile used to occupy", which is the whole ground.
   Not reported; recorded as a rejected candidate.
5. **`[R-SLB-04]` re-establish-or-clear a slab declaration** — expressly *not*
   a §21.7 case: its own Note (3282–3288) says "every file exhibiting one
   exhibits a run whose tiles are unpacked or whose first stored tile is
   misaligned, which §21.3 registers". Fully witnessed. Correctly absent.
6. **`[R-CNT-17]` entry_count, `[R-CNT-21]` slack, `[R-SLB-01]` aligned-layer
   invariant on shrink** (3245–3257) — all properties of the new live state,
   fully witnessed. Correctly absent.
7. **Growth permission and its bounds** (3207–3217) — the produced geometry must
   satisfy every rule, and those rules are registered. Correctly absent.
8. **Shrink permission** (3218–3241) — §20.3 itself routes this to §21.7 at 3238,
   and hunk 9's narrowing is what makes that route land. Accounted for.
9. **The layout field** (interleaved ↔ planar) — *not* named by any of the three
   bars. I checked whether it needs one: for C > 1 a layout flip alters the
   decoded size and every sample offset, so the §14 bar reaches it. For C = 1
   numeric, §14.4's Note says the images are byte-identical and the planar
   ordinal c·N+s reduces to s, equal to the interleaved ordinal — nothing moves.
   For C = 1 bool the images differ wherever ⌈P/8⌉ ≠ P, so §14 bar reaches it, and
   at P = 1 §14.4's Note says they coincide when fill is false. **No gap.**
10. **The linearization field** (§11.4) — a change would move every stored tile's
    ordinal in *either* layout, and Bar B is restricted to planar and to *channel*
    declarations. I checked §11.4: only row-major is defined, the rest are
    reserved and a writer MUST NOT emit them under major 1, so the field cannot
    change within this major. **No gap under this text.** Worth a maintainer's
    note when a curve value is assigned, but not a defect now.

So the answer to check 6: the repair pinned the two bars and the set it belongs
to has no unpinned sibling I could find. The one member with a soft edge is item
10, and it is closed by §11.4's reservation rather than by §20.3.

---

## 12. Check 7 — the analogies, verb against verb

Three analogy constructions in the repaired text.

**(a) "escapes them here exactly as it does the §14 bar" (3904–3906).**

- Repair's governing verb: **escapes**, object **them** = "the rows below".
- Cited rule's governing verb, §20.3 3139–3140: **does not escape**, object
  **this** = the §14 bar.

Same verb lemma, opposite polarity, and the objects differ in kind (rows vs a
bar). The elided second clause reads most naturally as "as it escapes the §14
bar", which is what §20.3 denies in terms. The intended reading has to borrow
"escapes *the rows that would witness*" across the analogy, which the words do not
supply. → **C-03**.

I then applied the charter's instruction to test an analogy against *each* member
it carries. This one carries three: the §14 bar, Bar A, Bar B. For the §14 bar the
proposition is stated independently at 3928–3931 and is true. For Bar B, "every
tile it would have damaged" is the empty set — a Bar B violation damages no
bytes — so the clause is vacuously true rather than false. For Bar A it is
vacuously true in the planar unstored-channel case and true otherwise. So the
analogy is not false member-by-member; the defect is the verb, not the range.
The "damaged" framing being vacuous for Bar B I considered and rejected as a
finding — recorded below.

**(b) "for the same reason `[R-LIF-01]` is" (hunk 9's sentence, 3930–3932).**

- Repair's subject and verb: **the §14 bar is unwitnessed**.
- Cited rule's posture, same paragraph 3880–3884: `[R-LIF-01]` is omitted from the
  register because committed-prefix immutability is "a propert[y] of a file's
  history, which §9.7 does not reconstruct".

Both range over *the prior generation*, and the §14 bar's own quantifier is
"any tile that layer stores **in the generation this commit supersedes**". Same
set, same ground. **Analogy sound.** Hunk 9 passes check 7.

**(c) "not decided by the element sizes of §12.1" (3906–3907)** is a denial of an
analogy rather than an analogy; its warrant is the worked example, checked in §4
and C-04.

---

## 13. Check 8 — what the insertion did to the sentences around it

Hunk 8 inserts; hunk 9 replaces one word. Reading forward from the insertion to
the end of §21.7, every back-reference:

| Reference | Line | Resolved BEFORE the insertion | Resolves NOW | Changed? |
|---|---|---|---|---|
| "one of those" | 3903 | *did not exist* | Ambiguous: (i) "everything §14 fixes" (3898), reached back across an em-dash clause; (ii) "which ordinal a stored tile used to occupy, or which type its channel carried before" (3901–3902), which is nearer. | **new ambiguity → C-02** |
| "the rows below" / "them" | 3904, 3905 | *did not exist* | No register rows lie below §21.7 — §21.2–§21.5 are all above; §21.8 has none and §21.9's table is expressly not register rows (§21.1 3573). Must mean "the rows named later in this paragraph". The document's only other "rows below" (§21.5, 3780) means rows that literally follow. | **new ambiguity → C-06** |
| "it" in "witness it" | 3904 | *did not exist* | the violation of the bar under discussion | fine |
| "Which case" | 3906 | *did not exist* | the witnessed / not-witnessed split just drawn | fine |
| "**A** change reaching a byte §14 structurally constrains…" and the three parallel "A change reaching…" sentences | 3909, 3911, 3913–3914, 3919 | The class was set by the immediately preceding sentence: "§20.3 step 4's bar on **a declaration change**…". So "A change" = a declaration change, and the enumeration covered padding, decoded size, codec, filter — all four of the §14 bar's list. | The immediately preceding sentences are now about the **two companion bars** and then specifically about **a type change** ("Which case a **type change** falls in… a planar `uint8` channel re-declared `bool`"). The nearest class-setter is now narrower than the enumeration. Under it, "A change reaching the codec" and "A change reaching the filter" are unreachable — a sample-type change cannot alter the codec or filter declaration, and Bar B changes no declaration outside the channel list. | **changed → C-05** |
| "there" in "the change is unwitnessed there" | 3919 | the codec case | unchanged | fine |
| "Neither change" | 3925 | the filter change and the sample-offset move | unchanged | fine |
| "there" in "unwitnessed there" | 3930 | the supersede-everything case | unchanged | fine |
| "the bar" → "**the §14 bar**" | 3930 | ambiguous among the bars named in §20.3 once §21.7 mentions more than one | pinned to the §14 bar, matching §20.3's forward reference at 3238 ("this is precisely where the §14 bar has no witness") | **fixed — this is hunk 9 doing its job** |
| "it" in "it is a property of the prior generation" | 3931 | the bar | the §14 bar | fine, and improved |
| "all three share", "the last two", "the three" | 3935–3937 | §20.5's three trailer obligations | unchanged — the insertion is 30 lines earlier and §20.5 is re-named at 3932 | fine |

Backwards run: does the inserted text itself lean on an antecedent further away
than a reader will look? Yes, once — "one of those" reaches back over the whole
em-dash clause at 3899–3902 to "everything §14 fixes" at 3898. That is C-02.

Hunk 9 inserts two characters' worth of text and creates no new back-reference.
Its one effect on a neighbour is to disambiguate 3931's "it", favourably.

One redundancy the insertion created, which I considered and did not report as a
defect: 3904–3906 and 3928–3931 now state the same proposition about a commit
that supersedes every damaged tile, twenty-four lines apart, and the second begins
"And a commit that supersedes…" as though introducing it. The first also
forward-references ("exactly as it does the §14 bar") a claim the paragraph does
not make until the second. Editorially poor; not a defect on its own, and the
"escapes" problem in the first is C-03.

---

## 14. Findings

### C-01 — "the rows below witness it" is unconditional and the paragraph refutes it four sentences later

Check: OVERCLAIM (and LOCAL_CONTRADICTION). Hunk 8. Location: §21.7, lines
3902–3904; contradicted at 3913–3919 and 3919–3925.

Quotation: "Where the change does touch one of those, and the tile it touches
remains stored, the rows below witness it".

Contradicting text: "A change reaching the codec is *sometimes* witnessed … but
neither is assured: a writer can choose stored bytes that satisfy the old
declaration and the new one alike, and the change is unwitnessed there." And:
"…where the resulting image breaks §14.5's padding content or `[R-SER-08]`'s bool
bytes, the check that detects it is T2's or T4's, exactly as T26 has it, and
where it breaks neither there is no witness."

Three constructed failures (full working in §8): A-4 (interleaved `uint8`/`uint16`
retyped to `uint16`/`uint8` — Q = 3 unchanged so T3 and T14 silent, sample
offsets move so §14 is touched, no padding positions so T4/T5 silent, codec and
filter untouched so T15/T17/T23/T25/T26 silent — no row fires); A-5 (interleaved
`uint8` → `bool` over a mask holding only 0x00/0x01 — `[R-SER-08]` newly binds
those bytes so §14 is touched, T2 has nothing to fire on); A-3 (planar `uint8` →
`bool` at P = 1 — decoded size 1 both ways, T5 fires only if the seven new pad
bits differ from the fill bit).

Repair: qualify the sentence to the terms the following sentences actually state,
e.g. "Where the change does touch one of those, and the tile it touches remains
stored, the rows below witness it on the terms they state — assured for the
decoded size, contingent on the stored bytes for the codec, the filter and a
moved sample offset."

Byte-level: **no.** Both readings leave the bars in force and leave every row's
detector and detection point exactly as the rows state them; a verifier's
obligations come from the rows and their governing rules, not from §21.7's
description of them. No file becomes emittable or refusable either way.

### C-02 — "one of those" has two live antecedents, and the nearer one makes the sentence flatly false

Check: NEW_AMBIGUITY. Hunk 8. Location: §21.7 line 3903.

Quotation: "Where the change does touch one of those, and the tile it touches
remains stored, the rows below witness it".

Candidate (i), intended: "everything §14 fixes for a tile the layer stores in the
generation the commit supersedes" (3898–3899). Candidate (ii), nearer: "which
ordinal a stored tile used to occupy, or which type its channel carried before"
(3901–3902). Under (ii) the sentence claims that any change touching a stored
tile's ordinal or its channel's type is witnessed — which §20.3 3161–3164 denies
in terms for `int8` → `uint8` ("moves no stored byte, no decoded size and no
sample offset"), and which case B-1 denies for the ordinal.

Repair: name the antecedent — "Where the change does touch something §14 fixes for
such a tile…".

Byte-level: no. Same reasoning as C-01.

### C-03 — "escapes … the §14 bar" says the opposite of the bar's own tense clause

Check: LOCAL_CONTRADICTION. Hunk 8. Location: §21.7 lines 3904–3906 against
§20.3 step 4 lines 3138–3142 (and 3204–3207, 3222–3226).

Quotation: "a commit that supersedes every tile it would have damaged escapes
them here exactly as it does the §14 bar."

Contradicting text, §20.3 step 4: "The tense is the prior generation's (§3.1
defines *stored* against a generation), so a commit does not escape this by
unstoring in the same breath: superseding every tile of a layer and re-declaring
it are one operation, and this bars it."

Why this is not merely infelicitous: §21.7 is normative (no `>` marker, no
Note/Example/Rationale label, closes with `[R-ERR-01]`), and the document supplies
**no precedence rule** for §21.7 against the rule it describes. §21.1 states one
for register rows ("where a row and the rule it cites diverge, the rule governs")
and repeats it for §21.6's entries ("the rule governs there too"), and then says
in terms that §21.7 is *not part of the register* (3573–3578). So the one
mechanism that would resolve this conflict is expressly withheld from §21.7.

Repair: say what the paragraph means — "…is beyond those rows here, exactly as a
§14-bar violation is; the bar is not thereby escaped (§20.3 step 4)." Or reuse
the paragraph's own vocabulary at 3919/3930: *unwitnessed*, never *escapes*.

Byte-level: **yes.** Applying the charter's discriminator: the disputed file is
conforming. §21.7's own claim is that such a commit "leaves the live state clean"
(3928–3930), so the output carries no register-row violation and `[R-CNF-05]`
("A writer MUST emit only conforming files", line 199) does not reach it — the
strict reading forbids the *actor's* conduct under `[R-WRT-04]`, not the bytes.
So exactly one reading permits an actor to produce the file, and the emittable
set moves. Two implementations: appender X reads §20.3 and refuses, writing the
retyped channels as a **new layer** (or a whole-file rewrite under a fresh
file_id, per 3153–3155); appender Y reads §21.7 and appends **one commit** whose
tile-index region for layer L is all sentinel (§15.2) and whose re-emitted layer
record carries the new sample types. Y's file has one layer record where X's has
two, a different `entry_count`/extent layout, and a different
`committed_file_length`. They differ on disk.

### C-04 — the restated `uint8`→`bool` example drops the P = 1 coincidence, in the one place it decides the outcome

Check: UNSWEPT_RESTATEMENT. Hunk 8. Location: §21.7 lines 3906–3909 against
§20.3 lines 3166–3169 and §14.4's Note at 2078–2083.

Quotation: "Which case a type change falls in is not decided by the element sizes
of §12.1: a planar `uint8` channel re-declared `bool` keeps its element size of 1
while its plane goes from P · Bᶜ bytes to ⌈P/8⌉."

Contradicting text, §20.3 3166–3169: "the element sizes of §12.1 do not settle
it — a planar `uint8` channel re-declared `bool` keeps its element size of 1 while
its plane goes from P · Bᶜ bytes to ⌈P/8⌉ (§14.3), **and the two coincide at
P = 1**." Corroborated by §14.4's Note: "At P = 1 the two are the same length and
`[R-SER-05]` fixes the planar pad bits to the channel's fill, so the images
coincide exactly when that fill is false."

`grep -c "coincide at P = 1"` → 1, at 3169. The qualification exists in exactly
one place and the restatement dropped it. It was inert in §20.3 (the bar is
outright there, "barred outright rather than by cases"). It is **not** inert in
§21.7, whose sentence is doing case-assignment: at P = 1 the decoded size does not
move, T3 and T14 are silent, and the change lands in the unwitnessed-or-contingent
case that the example is offered to illustrate the opposite of. The `(§14.3)`
citation was dropped with it.

Repair: restore the clause and the citation — "…goes from P · Bᶜ bytes to ⌈P/8⌉
(§14.3), and the two coincide at P = 1, where the change moves no length and only
`[R-SER-05]`'s pad bits can witness it."

Byte-level: no. It misdescribes detection; it does not change what any writer may
emit or any reader must reject.

### C-05 — the "A change reaching …" enumeration lost its subject to the insertion

Check: NEW_AMBIGUITY (check 8). Hunk 8. Location: §21.7 lines 3909–3925, text the
repair did not touch, following the insertion at 3897–3909.

Quotation (the inserted sentence that re-set the class): "Which case a type change
falls in is not decided by the element sizes of §12.1: a planar `uint8` channel
re-declared `bool` keeps its element size of 1 while its plane goes from P · Bᶜ
bytes to ⌈P/8⌉."

Contradicting/affected text: "A change reaching the codec is *sometimes*
witnessed by the rows for the codec now declared…" (3913–3915).

Before the insertion, the four parallel "A change reaching …" sentences took their
class from the sentence immediately before them — "§20.3 step 4's bar on **a
declaration change** is witnessed only where the affected tiles remain stored, and
then only for part of what it bars." — so "A change" meant a declaration change
and the four members matched the §14 bar's four-item list (padding content,
decoded size, codec, filter/offset). After the insertion the nearest class-setters
are the two companion bars and then, at 3906–3909, a **type** change. A sample-type
change cannot reach the codec or the filter declaration, and a Bar B change alters
no declaration outside the channel list, so two of the four sentences are
unreachable under their new nearest antecedent.

Repair: restore the class explicitly at the head of the enumeration — "Of a
declaration change generally: a change reaching a byte §14 structurally
constrains…" — or move the inserted companion-bar material to a sentence after
the enumeration.

Byte-level: no.

### C-06 — "the rows below", in a subsection with no rows below it

Check: NEW_AMBIGUITY. Hunk 8. Location: §21.7 line 3904 (and "them", 3905).

Quotation: "the rows below witness it; a commit that supersedes every tile it
would have damaged escapes them here".

Contradicting text, §21.1 lines 3573–3578: "The subsections after §21.5 are not
part of the register and carry no rows: neither this completeness clause nor the
instance arithmetic below reaches §21.6's defined non-violations, §21.7's account
of what no check detects, or §21.9's limits."

Every register row is *above* §21.7. Below it are §21.8 (no table) and §21.9
(a limits table §21.1 expressly denies is register rows). The document's only
other use of the phrase — §21.5 line 3780, "as a violation in the rows below" —
means rows that literally follow. A reader who follows this one goes to the wrong
place, and "them" at 3905 inherits the same referent.

Repair: "the rows named below" or, better, name them: "T3 or T14, or §21.4's
content rows, on the terms below".

Byte-level: no.

---

## 15. Candidates I opened and closed

1. **A slab or alignment invariant witnessing a Bar B ordinal move.** Closed by
   reading `[R-SLB-01]`/`[R-SLB-02]`/`[R-SLB-03]` in full: runs partition each
   channel block [c·N, (c+1)·N) identically for every c, all blocks have size N,
   and a permutation or shift of whole blocks preserves each run's membership,
   internal order and first-tile alignment; per-tile alignment is
   `offset mod A = 0`, which no ordinal enters.
2. **L30 (fill length prefix vs element size) witnessing a Bar A type change.**
   Closed: the fill length prefix is a directory field the same commit rewrites
   at no cost, so it is not a witness of the type change but of a separate
   careless edit — the same reasoning §21.7 already applies to the codec case
   ("a writer can choose stored bytes that satisfy the old declaration and the new
   one alike").
3. **§13.2 per-type fill constraints as a witness.** Closed for the same reason.
4. **`entry_count` (`[R-CNT-17]`) witnessing a channel insertion or removal.**
   Closed: entry_count = C·N is derived from the *new* declarations and the
   re-emitted index carries the new value; nothing records the old C.
5. **"no check can know" being too absolute, given §9.6 recovery can reach an
   earlier trailer.** Closed: §9.6 is headed "Recovery scan (**not a reader
   behavior**)", and its output must be re-verified whole before use; it is not a
   check on this file, and the repair scopes its claim to what §9.7 walks.
6. **§21.7 owing a register row for either companion bar.** Closed by §7 above:
   neither is detectable from one file, so `[R-CNF-07]`'s gate excludes them and
   §21.1 routes them to §21.7, which is where the repair put them. Counts
   unaffected, and my recount (120/275) matches the printed figures exactly.
7. **"three obligations" (§21.7, 3932) vs "Neither obligation" (§20.5, 3455).**
   Closed: §20.5's "Neither" covers the two just discussed (ignore-lane carry-
   forward and the version_minor floor); the third, the fresh `file_id` draw, is
   stated earlier in §20.5. §21.7's own "For the last two there is a second"
   confirms the 2-of-3 split. No mismatch, and untouched by these hunks.
8. **"every tile it would have damaged" as a quantifier mismatch for Bar B**
   (Bar B damages no bytes). Closed: the clause comes out vacuously true rather
   than false for Bar B, so it is imprecise, not wrong. The defect in that
   sentence is the verb, reported as C-03.
9. **The index-renumbering obligation (3117–3125) missing from §21.7's account.**
   Closed: the repair's own new ground — "no check can know which ordinal a stored
   tile used to occupy" — states exactly the reason it is undetectable, so the
   class is covered even though the obligation is not named.
10. **Hunk 9 narrowing to the wrong bar.** Closed: §20.3 line 3238–3240 names the
    §14 bar in terms as the one whose consequence §21.7 records, and the
    surrounding sentences (filter changes, sample-offset moves, both §14-bar
    items) are §14-bar material. The narrowing is right.

## 16. Verdict per hunk

**Hunk 9: clean.** All eight checks run. The narrowed subject is the right one,
it matches §20.3's own forward reference word for word, the sentences on either
side stay true, and it improves the resolution of "it" in the clause that follows.

**Hunk 8: five findings.** Its central claim — that the two companion bars are
witnessed not at all where §14 is left untouched — I tried hard to falsify and
could not; that half is sound and correctly placed. The failures are all in the
sentence that handles the *other* branch and in the analogy attached to it.
