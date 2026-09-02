# Repair audit — hunks 5 and 6 (§21.7, "What no check detects")

Auditor lane: "§21.7's account of what no check detects, and the register's
relationship to the two new rules."

## 0. Disclosure

Read: `spec/tarn.md` (the whole of §12.1, §14.2, §14.3, §14.5, §15.1 opening,
§16/§16.1/§16.2, §9.6, §9.7, §20.3, §20.4, §21.1–§21.9, §2.2's [R-CNF-05]/
[R-CNF-11], §2.4's [R-CNF-07], and [R-PRV-03] at lines 4180–4200), plus my two
hunk files:
`/private/tmp/.../scratchpad/case-adr0113/hunk-05.diff` and `hunk-06.diff`.

Ran: `grep`/`sed`/`awk` and one `python3` heredoc over `spec/tarn.md` only. No
network. Did not open `full.diff`, other hunk files, `docs/`, `conformance/`,
`OPEN-QUESTIONS.md`, `PLAN.md`, `AGENTS.md`, `spec/registry.json`, or git
history; did not list the case directory.

Unrequested context appeared before I began: a project-instruction file
reference (CLAUDE.md -> AGENTS.md), an auto-memory index with two note titles
about this project's harness, an MCP server instruction block, a skills
listing, and a `git status`/recent-commit-log block naming round numbers and an
ADR filename. I read none of the files they name and drew no conclusion from
them. The commit subjects visible in that block do mention "ADR-0113" and
"round 28"; I did not use them. Disclosed, not acted on.

## 1. The hunks, and where they land

Hunk 5 header claims lines 3889–3900, nearest preceding heading line 3853
"21.7 What no check detects". Verified: `sed -n '3853p'` gives
`#### 21.7 What no check detects`; line 3889 is
`bars, and its two companion bars are witnessed not at all where the`.
Header is accurate.

Hunk 6 header claims line 3919. Verified: line 3919 is
`live state clean, so the §14 bar is unwitnessed there for the same`.
Header is accurate.

Neither hunk sits in a blockquote. §21.7's body is plain paragraphs — no ">"
marker anywhere between lines 3853 and 3934 (checked by eye over the full
`sed -n '3853,3935p'` dump). So the label test of [R-CNF-01] is not even
reached: there is no block, labeled or otherwise. Both repairs land in
normative text. (Test applied: read the opening words of the enclosing
structure; the enclosing structure is a bare paragraph.)

### The rule each repair asserts, in my words

**Hunk 5.** Of the three MUST NOTs §20.3 step 4 imposes on a declaration
change: the §14 bar can be caught by a check only where the tiles it damaged
are still stored, and then only partly; and the other two — the sample-type
bar and the planar disk-ordinal bar — can never be caught in the case where
the change alters nothing §14 fixes for a stored tile, because a file carries
no copy of its previous channel declarations. Where the change does alter
something §14 fixes, the following sentences' rows catch it; and §12.1's
element-size column is not what decides which of the two cases a type change
is in.

**Hunk 6.** The "supersede-everything-you-damaged" escape belongs to the §14
bar specifically, not to the whole family of step-4 bars.

### The three bars, quoted (§20.3 step 4)

- §14 bar, lines 3126–3134: "A commit MUST NOT change a layer's declarations in
  a way that alters, for **any** tile that layer stores **in the generation
  this commit supersedes**, what §14 fixes for its stored bytes or how they
  decode — the **§14 bar** — the set of padding positions (§11.3) and the
  content `[R-SER-05]` fixes there, the decoded size, the byte offset of any
  sample within the decoded tile image, or the codec and filter that produced
  the stored bytes."
- Sample-type bar, lines 3165–3168: "a commit MUST NOT change the declared
  sample type of any channel of a layer that stores a tile **in the generation
  this commit supersedes**, whatever the layer's layout and whether or not the
  element size moves."
- Planar disk-ordinal bar, lines 3174–3179: "the §14 bar does not reach it
  **because it is not an effect on any stored tile's bytes**: for a **planar**
  layer, a commit MUST NOT change the channel declarations in a way that alters
  the disk ordinal `[R-GEO-06]` assigns any tile the layer stores **in the
  generation this commit supersedes**."

"its two companion bars" = exactly these two. Count verified: §20.3 step 4
contains three MUST NOTs on a declaration change and no fourth. §20.3 line
3230 independently says "The two bars beside the §14 bar govern declaration
changes". PASSES check 5 for the numeral "two".

## 2. Check 1 — tense and quantifier

Repair phrase: "everything §14 fixes for **a tile the layer stores**".

- No generation marker. All three bars it summarises are quantified over "the
  generation this commit supersedes" — §20.3 says so three times and adds "The
  tense is the prior generation's (§3.1 defines *stored* against a
  generation)" (line 3135) and "the tense is these bars'" (line 3200).
- The *same sentence's* first clause uses the **other** generation: "witnessed
  only where the affected tiles **remain stored**". So one sentence now carries
  both generations, one of them unmarked, eight words apart.
- Quantifier: §20.3 writes "for **any** tile that layer stores"; the repair
  writes "for **a** tile the layer stores". Under "leaves untouched … for a
  tile", English admits an existential reading ("there is a tile it leaves
  alone"), which is the wrong rule: one damaged tile witnesses regardless of
  how many are untouched.

Honest precedent: §20.3 line 3153 itself writes "any that alters, for a tile
the layer stores, what §14 fixes" without a generation. But there the bare
phrase sits two paragraphs below the bar whose tense is stated in bold and is
not adjacent to a contrary tense. In §21.7 the two tenses are adjacent, and the
two readings give different accounts of what is witnessed. -> C-01.

## 3. Check 2 — citations

Every identifier and section number in the repaired text, opened:

- **§14** ("everything §14 fixes for a tile"): §14.2 fixes decoded size and
  each value's byte offset; §14.3 fixes packed-plane decoded size ⌈P/8⌉ and pad
  bits; §14.5 ([R-SER-05]) fixes padding-position content and pad-bit content;
  §14.2's [R-SER-08] fixes interleaved bool bytes. Matches the §14 bar's own
  list (padding positions and their content, decoded size, sample byte offset,
  codec and filter) except that §14 does not fix "the codec and filter" — that
  member of the §14 bar's list comes from §17, not §14. Pre-existing in §20.3;
  §21.7's "everything §14 fixes" inherits it. Not reported: §21.7 is
  paraphrasing §20.3's own name for the bar, and the following sentences treat
  codec and filter separately anyway. VERDICT: passes as used.
- **§12.1** ("not decided by the element sizes of §12.1"): §12.1's table gives
  bool = 1 and uint8 = 1; the prose adds "except that a planar bool plane is
  sized by packing (§14.3)". The claim is exactly right. VERDICT: passes.
- **P · Bᶜ** and **⌈P/8⌉**: §14.2's table row "planar, numeric channel c |
  P · Bᶜ"; §14.3 "the decoded size is ⌈P/8⌉ bytes". VERDICT: passes.
- **§21.4's content rows**, **T3**, **T14** (context lines, re-wrapped by the
  hunk but not altered): unchanged text, spot-checked only. T3/T14 exist in
  §21.4/§21.3 and test lengths. VERDICT: passes.
- **§14 bar** (hunk 6): the defined term is introduced in bold at line 3129 and
  used at 3152, 3176, 3213, 3225, 3230, 3232. Hunk 6's use is the seventh and
  matches §20.3 line 3232's "§21.7 records the consequence — that this is
  precisely where the §14 bar has no witness, the live state being clean".
  VERDICT: passes, and it repairs a cross-reference that §20.3 was already
  relying on.
- **[R-LIF-01]**, **§9.7**, **§20.5**, **[R-WRT-06]**, **[R-ENC-06]**,
  **[R-ERR-01]** (untouched tail of the paragraph): not re-verified beyond
  confirming §9.7 walks the live state only ("A verifier checking [R-CNT-02]'s
  partition walks the live state only", line 3441).

One citation the repair should have made and did not: the em-dash reason it
gives is a claim about recoverability, and the document's ground for exactly
this proposition is §9.7's live-state-only walk — cited twice elsewhere in the
same paragraph as "which §9.7 does not reconstruct". See C-04.

## 4. Check 3 — normative placement

Applied the LABEL test, not the ">" test. §21.7 lines 3853–3934 contain no
blockquote at all; both hunks land in bare normative paragraphs. Additionally
greped the distinctive terms to see whether the rule the repair states is
stated anywhere else, and whether any of those places is labeled:

    grep -c "companion bar"      -> 1   (only line 3889, the repair itself)
    grep -c "declaration change" -> 2   (3231 in §20.3; 3887 in §21.7)
    grep -c "witness"            -> 17
    grep -c "unwitnessed"        -> 3   (3908, 3919, 3924 — all §21.7 prose)
    grep -c "§21.7"              -> 7

Of the seven "§21.7" hits, two are labeled-block-free normative prose that
point *at* §21.7 (line 3231 in §20.3 step 4; line 3447 in §20.5), one is a
register row cell (T26, line 3763), one is §21.1's completeness clause (3550),
one §21.1's exclusion clause (3569), and two are §17/§18-area prose (2514,
2606). None of the statements the repair makes has its only home in a **Note**,
**Example** or **Rationale** block. No defect on check 3.

## 5. Check 4 — contradiction in the same passage, including untouched text

Read §21.7 entire (lines 3853–3934), §20.3 step 4 entire (3110–3251), §20.4
entire, §9.6, §9.7, §21.1, §21.6.

### 5a. The supersession escape (C-02)

Four sentences after the insertion, in text hunk 6 edited:

  "And a commit that supersedes every tile it would have damaged leaves the
  live state clean, so **the §14 bar** is unwitnessed there for the same reason
  `[R-LIF-01]` is: it is a property of the prior generation, which §9.7 does
  not reconstruct" (lines 3917–3921).

The inserted text says:

  "Where the change does touch one of those the rows below witness it"
  (lines 3894–3896).

Constructed case. Planar layer L, one channel `a: uint8`, N = 4 spatial tiles,
P = 64. Generation G1 stores tile (a, s=0) as a 64-byte plane. Commit C
re-declares `a` as `float32` **and in the same commit supersedes tile (a,0)**
with a fresh, correct 256-byte float32 plane.

- The sample-type bar is violated: the layer stored a tile in the superseded
  generation and the declared type changed. §20.3 forecloses the escape
  expressly — "a commit does not escape this by unstoring in the same breath"
  (line 3136) and "Unstoring that tile in the same commit does not rescue it
  either" (line 3220).
- The §14 bar is violated too (the decoded size for that prior-generation
  stored tile is altered).
- The change *does* touch something §14 fixes.
- The live state is clean: entry length 256, decoded payload 256, T3 and T14
  pass; no §21.4 content row fires; no row anywhere reads a prior generation.

So "the rows below witness it" is false here. The §14-bar half of the sentence
protects itself with "only where the affected tiles remain stored"; the
companion-bar half has no such qualifier, and hunk 6 has just narrowed the one
sentence that would have supplied it to "the §14 bar". The two hunks pull
against each other. -> C-02.

### 5b. Recoverability (C-04)

Inserted: "the prior generation's channel declarations are **not recoverable
from the file**".

Untouched normative text, [R-PRV-03], lines 4188–4196:

  "and the shape of its own history — the size of each commit and the slack it
  left behind, **recoverable by probing backward for the superseded trailers
  that committed-prefix immutability keeps in place** (§9.1, §9.6). … absent
  altogether from a compacted file (§20.5), which retains no earlier trailer to
  find."

And §9.6 [R-LIF-06], line 1404: "A recovery tool enumerating a file's commit
states continues the same probe to offset 0". A superseded trailer locates a
superseded directory, and a superseded directory *is* the prior generation's
channel declarations. §20.3's own diagrams show the superseded directory
becoming slack that only compaction reclaims, and [R-LIF-01] freezes it in
place. So in the ordinary appended file the prior declarations are recoverable;
only a compacted file lacks them.

The paragraph already contains the correct, careful formulation twice — "are
properties of a file's history, **which §9.7 does not reconstruct**" (3875) and
"it is a property of the prior generation, **which §9.7 does not reconstruct**"
(3920). The insertion departs from it and states an absolute the document
elsewhere denies. -> C-04.

### 5c. Contradictions looked for and NOT found

- §21.6's "Two structural cases are conforming files a reader nevertheless
  refuses" — no collision: neither companion bar produces a reader refusal.
- §21.6's carve-out sentences ("Neither is a register row: the register
  enumerates file-conformance violations (§21.1), and a file this document
  declines to judge is not one") — consistent with leaving both bars out of the
  register, see §7 below.
- §20.3's shrink paragraph, "The two bars beside the §14 bar govern declaration
  changes, which a shrink is not" (3230) — consistent with hunk 6 naming the
  §14 bar in the shrink/supersession sentence. Hunk 6 is *correct* here; §20.3
  line 3232 was already pointing at exactly this sentence.
- [R-SLB-01]/[R-SLB-03]/[R-SLB-04]: searched for a slab-based witness of an
  ordinal move; see §6 below. None exists.
- §21.1's "where a row and the rule it cites diverge, the rule governs" — not
  engaged; §21.7 carries no rows.

## 6. Check 5 — exhaustive claims, each attacked

| Claim in repaired text | Attack | Verdict |
|---|---|---|
| "its **two** companion bars" | Counted the MUST NOTs in §20.3 step 4: §14 bar (3126), sample-type (3165), planar ordinal (3177). Exactly two companions. §20.3 line 3230 agrees. | holds |
| "witnessed **not at all** where …" | For the sample-type bar the condition is under-stated (5a). For the ordinal bar it is over-stated: see next row. | fails, C-02/C-03 |
| "the change leaves untouched **everything** §14 fixes" | Correct universal over what §14 fixes; but the tile set it ranges over is unmarked (C-01). | partial |
| "**no** check can know which ordinal a stored tile used to occupy, or which type its channel carried before" | True of every row in §21.2–§21.5: none reads a prior generation. Attempted witnesses: L21 (entry_count vs C·N) — the writer emits the new, correct count; L22 (extent_length formula) — follows entry_count; L2 (declaration-derived overflow) — a property of the new geometry, not of the change; L39/L40 ([R-SLB-01] alignment) — `offset mod A = 0` does not read the ordinal; L-rows for [R-SLB-03] packing — see below. | holds |
| "not decided by the element sizes of §12.1" | uint8 -> bool keeps size 1 and moves the plane size; uint8 -> uint16 moves both. So element size neither settles nor is irrelevant — "not decided by" is the right claim. §20.3 says "do not settle it". | holds |
| "its plane goes from P · Bᶜ bytes to ⌈P/8⌉" | Falsified at P = 1: 1·1 = 1 and ⌈1/8⌉ = 1. §20.3's source sentence says so — "and the two coincide at P = 1" — and §21.7 drops it. | fails, C-05 |
| "Where the change does touch one of those **the rows below witness it**" | Falsified by 5a, and by the P = 1 pad-bit case: at P = 1 a uint8->bool re-declaration newly subjects bits 1–7 to [R-SER-05], i.e. it *does* touch what §14 fixes, yet if the stored byte's high bits already equal the fill bit no row fires. | fails, C-02 |

### The slab, worked out (the only candidate witness I found for the ordinal bar)

[R-SLB-02]: "for a planar layer each channel block [c·N, (c+1)·N) — runs never
span channel blocks … Run r of a block starts at ordinal block_start + r·S."
[R-SLB-03]: within a run, stored tiles contiguous and packed in ordinal order,
first stored tile's offset ≡ 0 mod A_slab. [R-SLB-04] makes a stale declaration
a layer-scope validity error detected as [R-SLB-03]'s failures are.

The run partition inside a block depends only on N and S, never on c. A
channel permutation therefore maps runs onto runs isomorphically, carrying each
block's stored tiles and their offsets with it; packing and first-tile
alignment survive unchanged. A channel insertion or removal shifts block
starts but leaves each surviving channel's block internally identical. Worked
example: C = 2 (a, b), N = 2, S = 2, A_slab = 1; a at 1000/1010, b at
5000/5010. Runs before: {0,1} = a packed, {2,3} = b packed. After exchanging a
and b: {0,1} = b at 5000/5010 packed, {2,3} = a at 1000/1010 packed. Invariant
holds. Conclusion: no slab witness. Combined with §20.3's own reason for the
ordinal bar — "**it is not an effect on any stored tile's bytes**" — the
ordinal bar is unwitnessed *unconditionally*, not conditionally. -> C-03.

## 7. The register question (§21.1's completeness rule applied)

§21.1: "The register — §21.2 through §21.5 ([R-ERR-02]) — enumerates every
**detectable** file-conformance violation this specification names … Its
**completeness is normative** — a *detectable* file-conformance violation this
specification names and the register omits is a defect in this document,
detectability being the gate [R-CNF-07] already applies and §21.7 the account,
by class, of what fails it".

Two gates, both of which the companion bars fail:

1. **Detectable.** No row reads a prior generation; §9.7's walk is live-state
   only. Neither bar's violation is detectable from the file handed over. (The
   §9.6 probe is expressly "diagnosis … not a finding about the file it was
   given", line 1412 — which is why C-04 is a wording defect and not a
   detectability defect.)
2. **File-conformance violation.** In every case where the bars bite without
   also biting the §14 bar, the *resulting file is conforming*: its stored
   tiles all satisfy §14 under the new declarations, its index has the right
   entry_count, its slab invariants hold. The bars constrain a commit, not the
   bytes. §21.6 already states the principle for the parallel case: "Neither is
   a register row: the register enumerates file-conformance violations (§21.1),
   and a file this document declines to judge is not one."

Where a declaration change *is* detectable, the detectable thing is already
registered under its own row (T3, T14, §21.4's content rows) — exactly the
relationship §21.7's following sentences describe, and exactly how the §14 bar
itself is handled.

**Conclusion: no row is owed for either bar.** §21.7 is the right home. The
counts are therefore unchanged, and I verified them anyway:

    F rows 3617–3670: 35   (§21.2 prints "35 conditions")   OK
    L rows 3671–3727: 49   (§21.3 prints "49 conditions")   OK
    T rows 3728–3764: 26   (§21.4 prints "26 conditions")   OK
    R rows 3765–3798: 10   (§21.5 prints "10 conditions")   OK
    total 35+49+26+10 = 120 (§21.8 prints "120 conditions") OK
    instances (semicolon-split per §21.1's rule, "—" = 1):
      F 56, L 116, T 55, R 48; total 275 (§21.8 prints "275 instances") OK

§21.7 states no count of its own obligations. The only numerals in it are "its
two companion bars" (verified, §1 above), "§20.5's three obligations" and "For
the last two" (untouched, and §20.5's trailer obligations are indeed three:
fresh file_id draw, ignore-lane carry-forward, version_minor floor — confirmed
against §20.5 line 3447 "Neither obligation has a witness in the output alone
(§21.7)", which is about the last two).

## 8. Check 6 — what the repair left unconstrained

Structure governed: §20.3 step 4's obligations on a commit, and §21.7's account
of which of them a check can see. Full enumeration of step 4's obligations, and
whether §21.7 now accounts for each:

| Step-4 obligation | Witnessed? | Accounted in §21.7? |
|---|---|---|
| §14 bar | partly | yes (first clause) |
| sample-type bar | partly (C-01/C-02 mis-state the condition) | yes, after this commit |
| planar disk-ordinal bar | never | yes, but mis-conditioned (C-03) |
| "every other entry byte-identical **at its disk-ordinal position**" | never — a file carries no copy of the superseded index region | **no** |
| [R-WRT-05] byte-identical re-emission of retained records (§20.4) | never — §20.4's own Rationale says "it cannot, from the format: … nothing in either says how many commits separate them" | **no** |
| grow permission, shrink permission | permissions, no witness question | n/a |
| [R-SLB-04] stale slab declaration | witnessed, and §16.2's Note says why it has no row of its own | n/a |

The two "no" rows are the siblings the repair left unnamed. I decided not to
file them as findings: §21.1 calls §21.7 "the account, **by class**, of what
fails" the detectability gate, and both are in the class §21.7's first item
already names — "properties of a file's history, which §9.7 does not
reconstruct". Recorded here so the judgement is visible rather than absent.

## 9. Check 7 — analogies, verb against verb

The repaired text carries two "same reason" moves.

**(a) hunk 6's sentence.** "so **the §14 bar is unwitnessed** there for the same
reason **`[R-LIF-01]` is**: it is a property of the prior generation."
- §14 bar's governing verb: "MUST NOT change … in a way that **alters**, for
  any tile that layer **stores** in the generation this commit supersedes".
- [R-LIF-01]'s subject as §21.7 states it: "Committed-prefix immutability …
  **are properties of a file's history**".
Both range over the superseded generation; both are invisible to a live-state
walk. The analogy holds, and hunk 6 makes it hold of the right bar. REPORTED AS
PASSING.

**(b) The inserted joint condition** — an implicit "for the same reason", since
one clause and one reason are supplied for two bars.
- Sample-type bar: "MUST NOT **change the declared sample type** of any channel
  of a layer that **stores a tile** in the generation this commit supersedes".
- Ordinal bar: "MUST NOT change the channel declarations in a way that
  **alters the disk ordinal** [R-GEO-06] **assigns** any tile the layer stores
  …", introduced by "the §14 bar does not reach it because **it is not an
  effect on any stored tile's bytes**".
- The repair's condition: "where the change leaves untouched everything **§14
  fixes** for a tile the layer stores".
The sample-type bar's effects *are* effects on stored tiles' bytes, so keying
its witness to §14 is sound. The ordinal bar's effects are, by §20.3's own
words, *not* effects on any stored tile's bytes, so keying its witness to §14
is unsound for it: the antecedent is satisfied in every case the bar reaches,
and where it is not satisfied (a commit that also changes a type) the row that
fires witnesses the type effect, never the ordinal move. One sentence, two
members, sound for one and unsound for the next. The follow-on clause gives
this away by narrowing to a single member without saying so — "which case **a
type change** falls in". -> C-03.

## 10. Check 8 — what the insertion did to its neighbours

Every back-reference from the insertion point to the end of §21.7, with its
antecedent before and after:

| Reference | Before insertion | After insertion | Changed? |
|---|---|---|---|
| "§20.3 step 4's bar on a declaration change" (subject of the whole passage) | the one bar then under discussion = the §14 bar | §20.3 step 4 now holds three bars on declaration changes, and this very sentence distinguishes them; the subject is no longer self-identifying | YES — see C-06 |
| "its two companion bars" (inserted) | n/a | resolves to the unnamed subject above | inherits the ambiguity |
| "one of those" (inserted) | n/a | "everything §14 fixes" | fine |
| "the rows below" (inserted) | n/a | forward reference to the four following "A change reaching …" sentences | see C-02/C-06 |
| "which case" (inserted) | n/a | the witnessed/unwitnessed pair just drawn | fine |
| "**A change** reaching a byte §14 structurally constrains …" | continued directly from "§20.3 step 4's bar on a declaration change … only for part of what it bars" — so: a declaration change under the §14 bar | now separated from that antecedent by two sentences whose topic is a **type** change and its element sizes | YES — C-06 |
| "**A change** reaching the decoded size …" | same | same | YES — C-06 |
| "**A change** reaching the codec …" | same | same; and a *type* change cannot reach a codec at all, so the re-resolved reading is vacuous | YES — C-06 |
| "**A change** reaching the filter, or moving a sample's byte offset …" | same | same | YES — C-06 |
| "**Neither change** is caught by a length" | the filter change and the offset move, from the sentence immediately before | unchanged | no |
| "so **the bar** is unwitnessed there" | the §14 bar (the only bar named) | would now have three candidates | FIXED by hunk 6 |
| "**it** is a property of the prior generation" | the bar / [R-LIF-01]'s obligation | unchanged by hunk 6's subject edit; still true of the §14 bar | no |
| "**For the last two** there is a second" | §20.5's three trailer obligations | unchanged | no |

Backwards: the inserted text's own back-references ("its", "one of those",
"the rows below") all have antecedents inside or immediately beside the
inserted sentence, except "its", which points at an unnamed subject 3 lines
back — C-06.

## 11. Byte-level test, for every finding

The discriminating question, for each: is the disputed file conforming, and
does one reading permit an actor to produce it while the other forbids?

§21.7 imposes no obligation on any actor. It carries no register rows —
§21.1 says so expressly: "neither this completeness clause nor the instance
arithmetic below reaches … §21.7's account of what no check detects". The
three bars themselves live in §20.3 and are stated there in unambiguous MUST
NOT form with an explicit tense; a writer misled by §21.7 into thinking a
change unwitnessed still violates §20.3, and a verifier misled into thinking a
change witnessed still finds nothing, because no row reads a prior generation.
[R-CNF-11]'s *cannot establish* is reserved for "a capability or resource
ground", which none of these is — §21.7's own first paragraph says so of the
parallel case. So no accept/reject verdict and no emitted byte moves under any
of the six readings. All six findings: **not byte-level**. I state that
plainly rather than inflating; the findings are defects in a normative
paragraph that misdescribes the detection model, and one of them (C-02) sets
two sentences of the same paragraph against each other, but no implementation
pair forks on bytes.

## 12. Candidates opened and closed

- *Should the sample-type bar get a register row?* Closed by §21.1's
  detectability gate plus §21.6's precedent: the resulting file is conforming.
- *Should the ordinal bar get a row?* Same, and reinforced by §20.3's "it is
  not an effect on any stored tile's bytes".
- *Do the counts move?* Recounted mechanically: 35/49/26/10 = 120 rows, 275
  instances. Both printed figures are right and no row is owed. Closed.
- *Is the [R-CNF-11] disclaimer in §21.7's first paragraph missing from the
  second?* It is, but that is pre-existing structure the hunks did not touch,
  and "None of these" plausibly scopes to the first paragraph's items. Closed
  as out of charter.
- *Does a slab declaration witness an ordinal move?* Worked the run arithmetic
  (§6 above). It does not. Closed.
- *Does "everything §14 fixes" wrongly include the codec and filter, which §17
  fixes?* §20.3's §14 bar already names "the codec and filter that produced
  the stored bytes" in its own list under the label "§14 bar". Inherited, not
  introduced. Closed.
- *Does the P = 1 coincidence matter, or is it pedantry?* It matters: P = 1 is
  the one geometry where a uint8->bool re-declaration leaves the decoded size
  alone and moves the witness question onto pad-bit content, which is precisely
  the distinction the sentence is drawn to make. Kept as C-05.
- *Did hunk 6 pick the wrong subject?* No — §20.3 line 3232 was already
  pointing at this sentence with the words "the §14 bar has no witness, the
  live state being clean". Hunk 6 is a correct repair whose fault is only what
  it leaves unsaid (C-02).

## 13. Sweeps run, verbatim, with hit counts

    grep -n "^#\{1,6\} " spec/tarn.md                       (heading index)
    grep -n "^#### 20\.\|^### 20\." spec/tarn.md            -> 6
    grep -n "^## 21\|^### 21\." spec/tarn.md                -> 1
    grep -n "R-SLB-01\|R-SLB-04\|R-GEO-06\|R-CNT-17"        -> 24
    grep -n "R-CNF-11\|R-CNF-05\|R-CNF-07"                  -> 20
    grep -n "§14 bar\|14 bar"                               -> 8
    grep -n "^#### 12\.\|^#### 14\.\|^### 12\.\|^### 14\."  -> 10
    grep -n "^#### 9\."                                     -> 7
    grep -c "§21.7"                                         -> 7
    grep -c "witness"                                       -> 17
    grep -c "unwitnessed"                                   -> 3
    grep -c "companion bar"                                 -> 1
    grep -c "declaration change"                            -> 2
    grep -c "sample type"                                   -> 10
    grep -c "disk ordinal"                                  -> 13
    grep -c "not recoverable"                               -> 0
    grep -c "recoverable"                                   -> 9
    grep -cE '^\| F[0-9]+ \|' (3617–3670)                    -> 35
    grep -cE '^\| L[0-9]+ \|' (3671–3727)                    -> 49
    grep -cE '^\| T[0-9]+ \|' (3728–3764)                    -> 26
    grep -cE '^\| R[0-9]+ \|' (3765–3798)                    -> 10
    python3 instance count over 3617–3798                    -> F56 L116 T55 R48, 275

Note on hard wrap: "not recoverable" returned 0 hits because the phrase spans
the line break at 3891/3892 ("are not\nrecoverable from the file"). I did not
draw any conclusion from that zero; I searched the short fragment
"recoverable" instead, which found line 3892 and, decisively, line 4190.

## 14. Findings

C-01  TENSE_QUANTIFIER   §21.7 lines 3889–3891 — "a tile the layer stores"
                         carries neither generation nor the bars' universal.
C-02  LOCAL_CONTRADICTION §21.7 lines 3894–3896 vs 3917–3920 — "the rows below
                         witness it" against the supersession escape hunk 6 has
                         just narrowed to the §14 bar.
C-03  OVERCLAIM          §21.7 lines 3889–3894 — one §14-keyed condition for two
                         bars; the ordinal bar is unwitnessed unconditionally.
C-04  LOCAL_CONTRADICTION §21.7 lines 3891–3892 — "not recoverable from the
                         file" against [R-PRV-03] and §9.6.
C-05  UNSWEPT_RESTATEMENT §21.7 lines 3896–3898 — the §20.3 example restated
                         without "and the two coincide at P = 1".
C-06  NEW_AMBIGUITY      §21.7 lines 3887–3900 — the insertion re-scopes the
                         four "A change reaching …" sentences and leaves the
                         passage's subject unnamed among three bars.
