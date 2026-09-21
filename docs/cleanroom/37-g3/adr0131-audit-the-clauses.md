# Round 37 audit — "the-clauses" lane

## Disclosure

**What I read:**
- `/Users/robertkleffner/Documents/GitHub/tarn-first-draft/spec/tarn.md` in full (4981 lines), plus targeted re-reads of: §2.1, §2.2, §2.3, §2.4, §3.2, §3.3, §5.1/§5.2's example figure (lines 655-694), §7.2, §9.1, §9.2, §9.3, §9.7, §17.4, §18 (skimmed), §19.1, §19.3, §19.4, §20.1–§20.5 in full, §21.6, §23.1, Appendix H (Conformance checklists).
- My three charter hunk files: `hunk-01.diff`, `hunk-02.diff`, `hunk-03.diff` under `/private/tmp/claude-501/-Users-robertkleffner-Documents-GitHub-tarn-first-draft/r37-audit/case/`. I did not open `full.diff` or any other lane's hunk file, and did not list the `case/` directory (I only opened the three named files directly).

**What I ran:** a series of `grep -n` searches against `spec/tarn.md` (listed verbatim under "Sweeps run" below), and one Python script (via Bash, no file writes) to index character columns of the ASCII-art figures for hunk 2, run twice (once with a filtered character set, once dumping a raw column range) to double check my own column arithmetic.

**Files I wrote:** only under my scratch directory — `/private/tmp/claude-501/-Users-robertkleffner-Documents-GitHub-tarn-first-draft/r37-audit/scratch/the-clauses/transcript-draft.md` (an empty placeholder, superseded by this file) — and this transcript itself at the required output path. I wrote nothing else, anywhere.

**Disclosed breach:** while locating the output path, I ran `ls -la` on `/private/tmp/claude-501/-Users-robertkleffner-Documents-GitHub-tarn-first-draft/r37-audit/out/` to confirm the directory existed before writing into it. That listing showed one other filename, `audit-cross-hunk.md`, evidently another lane's output. I did not open, read, or otherwise use that file's contents anywhere in this audit; I mention it only because the charter says not to list the case directory, and out/ is close enough in spirit that I want the breach on the record rather than silently sitting on it. Nothing in this transcript or in my findings rests on anything from that filename or from having seen it.

**Contamination check:** my invocation context (system reminders) contained a project `CLAUDE.md` pointing at `AGENTS.md`, a user memory file listing prior "TARN" round titles (e.g. "TARN repair prose vs rules", "TARN closed-list exceptions compose", "TARN class lines are undertakings"), and a git log of recent commit subjects for this repo, including the exact commit subjects for round 36's repair and the charter that preceded it. None of this was requested by me; it arrived as ambient context before I did anything. I did not read `AGENTS.md`, `PLAN.md`, `docs/`, or any of the files the memory titles allude to, and I did not use any of those memory-file titles or commit subjects as evidence about the specification's content or about where a defect is likely to be. All conclusions below are derived solely from the two files the charter permits (the spec and my own hunks) and from the reasoning shown in this transcript. Where the ambient context happened to match something I independently verified from the spec (e.g., the round summary's claim about a citation), I re-derived it from the primary text rather than trusting the summary, and I say so explicitly at each such point.

---

## Hunk headers vs. body — verification

All three hunk files' headers claim the landing line numbers and preceding heading match the *current* file. I verified this directly:

- hunk-01.diff claims lines 439-440, heading "3.3 Container and array model" at line 435. Reading `tarn.md` lines 400-460: §3.3's heading is at line 435, and the Note text at lines 437-441 matches the hunk's "+" (post-repair) lines exactly, character for character. **Header and body agree.**
- hunk-02.diff claims line 3433, heading "20.3 The append procedure" at line 3188. Reading `tarn.md` lines 3407-3474 (the whole "three shapes" Example): the annotation line at 3433 matches the hunk's "+" line exactly. **Header and body agree.**
- hunk-03.diff claims line 3507, heading "20.4 Re-emission and preservation" at line 3475. Reading `tarn.md` lines 3475-3527: the table row at 3507 matches the hunk's "+" line exactly. **Header and body agree.**

No discrepancy to report on any of the three.

---

## HUNK 1 — §3.3's Note

### The rule the repair adopts

Before: "no Part I structure requires decoding sample payloads, so **verifiers, appenders, and rewriters carrying a layer forward** operate on files whose layers they cannot decode."
After: "no Part I structure requires decoding sample payloads, so **appenders, and rewriters carrying a layer forward,** operate on files whose layers they cannot decode."

The repair drops "verifiers" from the actor list and adds a comma after "forward" (so the modifier clause is now bracketed by commas on both sides). The rule it asserts: of the actors this specification defines, exactly appenders (always) and rewriters (when carrying a layer forward, i.e. not when re-creating it) can legitimately process a file containing a layer whose codec they cannot execute, without that being a nonconformity or a failure — and this fact is what lets §7 and §20's updater rules avoid requiring codec support.

### Check 1 — tense/quantifier, and the comma pair

**Which actors, and what does "carrying a layer forward" attach to?** Grammatically, "carrying a layer forward" sits immediately adjacent to "rewriters" with no intervening comma ("rewriters carrying a layer forward" is one noun phrase), while "appenders" is separated from it by "and". A modifier can only float back to attach to a non-adjacent noun across "and X" if the sentence sets it off on both sides of the *whole* compound subject (e.g. "appenders and rewriters, carrying a layer forward, operate..."). That is not the punctuation used. So the natural, and I think the only defensible, reading is: **"carrying a layer forward" modifies "rewriters" alone**; "appenders" is unqualified.

Is that reading true of the document? Yes, and importantly the *asymmetry* is required, not accidental:
- An appender never decodes anything it doesn't itself write, in any of its operations (§19.1's open touches only trailer+directory; §19.3's layer-access validation, which R-WRT-03 requires for a layer the commit modifies, is purely structural — "All are decidable from the resident directory and F: layer access performs no fetch" — no sample payload is ever fetched or decoded). So "appenders" needs no qualifier — it's unconditionally true of every appender operation.
- A rewriter, by contrast, sometimes *does* decode: "what it re-creates it decodes as a reader" (§20.5). Only the rewriter's *carrying-forward* disposition (as opposed to re-creation) is decode-free. So the qualifier is load-bearing specifically for the rewriter, and its absence for the appender is correct, not an oversight.

I could not construct a reading in which "carrying a layer forward" attaching to both actors would be *false* of the document (since it's true of appenders vacuously — they always carry forward without decoding), but that reading is not the one the punctuation supports, so this is a non-finding: the comma structure is a little unusual stylistically (see below) but not semantically wrong.

**The leftover comma.** Before the edit, "verifiers, appenders, and rewriters carrying a layer forward" was a normal three-item Oxford-comma list. After striking "verifiers," the text kept a comma after "appenders" ("appenders, and rewriters...") — a comma before "and" in what is now a two-item list, which is non-standard usage (normally "appenders and rewriters carrying a layer forward operate..." with no comma). This is a minor prose artifact of the edit, not a substantive ambiguity — I read it as a vestige of the three-item list rather than as evidence of a different parse — but note it below as a rejected candidate rather than a finding, since it does not change what the sentence claims or admit a false reading.

### Hold "appenders ... operate on files whose layers they cannot decode" to §20.3 and R-WRT-03

Two scenarios per the charter:

1. **An appender adds a new layer to a file whose *other* layer uses a codec it lacks.** R-WRT-03: "An updater's verification depth follows reliance ... plus §19.3's layer validation for every layer whose record, index, or extents the commit modifies ... Structures the commit neither modifies nor relies on impose no further obligation." The untouched layer is neither modified nor relied on, so it imposes zero obligation — the appender never touches its codec. **True, no qualifier needed.**

2. **An appender stores a tile into a layer whose codec it lacks.** This is not a scenario the Note's claim needs to cover, and on inspection it cannot arise for a conforming appender: storing a new tile into a layer requires *encoding* with that layer's fixed codec (§20.3 step 4: the codec is one of the declarations "fixed for as long as the layer stores a tile"), and this specification does not split "implements a codec" into separate encode/decode capabilities anywhere I found (§17.4/R-COD-11 and §2.3's "cannot execute a codec" language always speak of executing the codec as a unit). An appender that "lacks" a layer's codec entirely cannot perform this operation at all — so the scenario is vacuous, not a counterexample. The Note's claim is about a *file* containing a layer the appender doesn't decode; it never claims an appender can write into a layer whose codec it lacks. I looked for, and did not find, any sentence claiming otherwise.

### Hold "rewriters carrying a layer forward" to §20.5 and R-WRT-09

§20.5: "A rewriter satisfies every writer requirement for the bytes it produces (`[R-CNF-06]`), and a violation latent in a structure it carries forward verbatim travels into its output (`[R-WRT-01]`) — its verification depth over what it carries is `[R-WRT-09]`'s and reaches no decoded content, and what it re-creates it decodes as a reader (`[R-CNF-11]`) and writes as a creator (§20.2)." This sentence draws exactly the line the Note's qualifier draws: carrying forward reaches no decoded content; re-creating does decode. **Citation resolves; claim is true as scoped.**

### The verifier the repair struck — check 3/5

§2.3's verifier paragraph: a verifier reports *cannot establish* "when it cannot execute a codec or filter (`[R-COD-11]`)" among other capability/resource grounds. §17.4 (R-COD-11): "A verifier that cannot execute a layer's codec or filter cannot establish that layer's conformance and MUST NOT certify the file." §9.7 (R-LIF-08): "A verifier that certifies decodes every stored tile, whatever content obligations §14 places on the layer... a verifier MUST NOT certify past a violation it has not looked for; one that declines a tile's decode on resource grounds reports that check unmade and cannot certify."

So: a verifier that *certifies* has necessarily decoded every stored tile of every layer it certifies — for that verifier, at the moment of certifying, the "operates on files whose layers it cannot decode" claim is **false**. A verifier that does *not* certify (reports *cannot establish*) can and does process — "operate on" — a file containing a layer it cannot decode. The pre-repair Note's blanket "verifiers ... operate on files whose layers they cannot decode" was therefore an overclaim: true of a non-certifying verifier, false of a certifying one, asserted without qualification. That is exactly the finding the round summary attributes to this hunk (verifier certification requires decode, §9.7), and I independently re-derived it from R-LIF-08 and R-COD-11 rather than taking the summary's word for it.

**Did striking the verifier make anything false, or leave the "so" claiming too much/little?** The Note's payoff clause is explicit about its scope: "that independence is load-bearing for **the updater rules of §7 and §20**." Verifiers are not updaters (§2.3: "Its tiers, the appender and the rewriter, are §20.1's" — the updater class has exactly two tiers, neither of which is verifier). So the clause the Note exists to support never needed verifiers in the first place; removing them narrows the *subject* of the "so" to exactly the actors the "load-bearing" clause is about, and I could not find any place where the document needs the Note to say something about verifiers not decoding. The "so" now claims exactly what it needs for its own stated purpose — not more, not less. Whether it *should* also have kept a properly-qualified statement about non-certifying verifiers is a matter of completeness, not correctness (see "rejected candidates").

### Check 5 — the whole actor list

| Actor (§2.3/§20.1) | Operates on a file whose layers it cannot decode? | Where the document says so |
|---|---|---|
| Conforming reader | No — R-CNF-03 requires implementing every core codec/filter/sample type; the codec/filter menus are closed and both are core, so a conforming reader is never in the "cannot decode a core codec" position for a valid layer. |
| Creator | N/A — never has pre-existing undecoded content; writes flags = 0, nothing carried forward (§20.1). |
| Appender | Yes, unconditionally — R-WRT-03 + §19.1 (open touches only trailer/directory) + §19.3 (layer-access validation is purely structural, no fetch). |
| Rewriter | Yes, but only for what it *carries forward* — §20.5 ("reaches no decoded content" for carried structures; re-creation "decodes as a reader"). |
| Verifier | Conditionally — yes while it has not yet certified / is reporting *cannot establish* (§17.4, R-COD-11); no at the moment it certifies (§9.7, R-LIF-08 — certifying decodes every stored tile). |
| Updater (generic) | Union of appender + rewriter rows above — §2.3 defines it as exactly those two tiers. |

This table is exactly what motivates the repair: appender and rewriter are the two actors for which the claim is *unconditionally* true (modulo the rewriter's own internal carry/re-create split, which the sentence already encodes), which is why they are the two named in the "so" clause that feeds "load-bearing for the updater rules."

### Sweep — other sentences about decoding independence

```
grep -n "cannot decode" tarn.md       -> 1 hit: line 440 (the Note itself)
grep -n "undecod" tarn.md             -> 0 hits
grep -n "without decoding" tarn.md    -> 2 hits: lines 83, 90 (both in §1, non-normative Introduction, describing a hypothetical "container reader" — not part of the §2.3 conformance vocabulary, not in tension with the Note)
grep -n "does not decode" tarn.md     -> 0 hits
grep -n "opaque" tarn.md              -> 4 hits: lines 1230, 1241, 1253 (unknown/unregistered record payload opacity, §7.2 territory — a different, non-codec sense of "not decoded") and 4624 (a sample type named "opaque", unrelated)
```

**Control for the zeros** (to rule out hard-wrap or normalization artifacts per the brief's warning): I re-ran all five searches against whitespace-normalized text (all runs of whitespace collapsed to one space) with a Python script:
```
cannot decode           => 1
undecod                 => 0
without decoding        => 2
does not decode         => 0
opaque                  => 4
carrying a layer forward => 1
every entry, re-emitted => 1
an appender MAY drop    => 1
```
Identical counts before and after normalization. Since the "decode" stem itself is common (`grep -c "decode" tarn.md` → 142 hits, confirming the tool and file are being read correctly), I'm confident the zeros for "undecod" and "does not decode" are genuine, not artifacts of a broken search.

I also swept for anything leaning on this Note by citation or restatement:
```
grep -n "Part I\|Part II" tarn.md
```
→ only the definitional/introductory uses at lines 82-92 (§1, non-normative) and the Note's own line 437-438, plus incidental mentions of "Part I permits" (line 312, the preserve-verbatim outcome-class definition — about relocation, not decoding) and "Part II's rules/value sets" (lines 420, 92 — about what decoding does, not about who is exempt from it). Nothing else restates or depends on the Note's specific actor list.

**Conclusion on hunk 1:** the repair is correct as far as I can establish. It resolves the round-36 finding (a certifying verifier decodes everything, so "verifiers operate without decoding" was an overclaim) without introducing a false claim, without breaking the "so...load-bearing" clause's own scope, and without leaving any other passage in the document out of step with the new wording. The comma-before-"and" left over from the three-item list is a cosmetic wrinkle, not a substantive defect — see rejected candidates.

---

## HUNK 2 — figure (b) of the three-shapes Example, §20.3

### The rule the repair adopts

Before (raw): `└ old ─┘                      └ every entry, re-emitted` — an *opening* corner with no matching close, running to the end of the line with its caption directly attached, inside the still-open bracket.
After: `└ old ─┘                      └────────┘ every entry, re-emitted` — the second bracket is now closed, and the caption "every entry, re-emitted" sits *after* the closing corner, outside the bracket.

The rule the figure now (attempts to) express: the caption "every entry, re-emitted" describes only the field the closed bracket spans (the new index region, `index′`), not everything to the right of it (`dir₂│pad│tr₂`).

### Establishing the Example's force

This whole passage is inside `> **Example — the three shapes a commit takes.**` — a labeled blockquote, non-normative under R-CNF-01 ("any text labeled *Note*, *Example*, or *Rationale*"). I confirmed the label by reading the block's own opening line (3407) rather than assuming from the ">" marker alone. The actual normative rule this figure illustrates is stated in unlabeled, non-blockquote prose: §20.3 step 4 (lines 3233-3253, "An appender MUST, in order: ... 4. Write payloads and indexes ... Every layer whose stored-tile set or index content this commit changes has its tile-index region re-emitted in full... with entries for tiles this commit stores or supersedes written to their new state, entries for tiles that become unstored written as the sentinel, entries new to this generation ... emitted per §15, and every other entry byte-identical at its disk-ordinal position") and R-WRT-04. That prose is unaffected by this hunk and is unambiguous on its own. So whatever the figure's defect, **it cannot be byte-level**: nothing here changes what bytes any conforming appender may emit or what a reader must accept/reject, only whether a reader of the *diagram* understands it correctly.

### Character-column analysis (worked by script, not by eye)

I dumped exact character indices (Unicode codepoints, one column each — I counted the hatching `▓`, the prime `′`, and subscript digits as one column apiece, as instructed) for every `│`, `▓`, `└`, `┘`, `─` in:

**Figure (a)** (lines 3413-3415, "after" row + annotation row):
```
after row │ positions: 9, 15, 32, 46, 63, 69, 73, 77
  field "A: tiles+index" (labelled "untouched"): between │15 and │32
  hatched field (labelled "was dir₁…tr₁"): between │32 and │46
annotation row:
  bracket 1: └ at col 16, ┘ at col 32  (label "untouched" INSIDE, cols 19-29)
  bracket 2: └ at col 33, ┘ at col 46  (label "was dir₁…tr₁" INSIDE, cols 34-45)
```
Bracket 1's field spans │15..│32 (content cols 16-31); its open corner sits at col 16 = leftSep+1 (one column *inside* the field, past the separator), and its close corner sits at col 32 = rightSep+0 (exactly on top of the field's own right-hand separator). Bracket 2 shows the identical pattern relative to its field (│32..│46): open at 33 = leftSep+1, close at 46 = rightSep+0. **Both brackets in figure (a) follow the same convention: open one column inside the field (never on the separator), close exactly on the following separator. Both captions sit inside the bracket, between the corners.**

**Figure (b)**, "old" bracket (unchanged by the hunk), lines 3431-3433:
```
after row │ positions: 9, 15, 23, 31, 45, 54, 63, 69, 73, 77
  field "▓index▓" (labelled "old"): between │23 and │31
annotation row:
  bracket "old": └ at col 24, ┘ at col 31  (label "old" INSIDE, cols 26-28)
```
Same convention exactly: open at 24 = leftSep(23)+1, close at 31 = rightSep+0, caption inside.

**Figure (b), the repaired bracket** (line 3433, cols verified with a raw per-column dump of 3432/3433):
```
row 3432 (after) fields: "+tiles" between │45 and │54; "index′" between │54 and │63
row 3433 (annotation): └ at col 54, ── at 55-62, ┘ at col 63
  caption "every entry, re-emitted" begins at col 65, i.e. AFTER the ┘ at 63 (one space, then text)
```
The dash-fill (cols 55-62, 8 columns) exactly matches the "index′" field's own content width (│54..│63 ⇒ content cols 55-62, 8 columns) — so the bracket's *width* is right. But:

- **Left corner:** placed at col 54 = leftSep+0 (exactly on top of the separator that divides "+tiles" from "index′"), not leftSep+1 like every other bracket in this document (both brackets of figure (a), the "old" bracket of this same figure). This is a **one-column departure from the figure's own established convention**, confirmed against three independent prior examples, not just one.
- **Caption placement:** placed *outside*, after the closing corner, rather than *inside* the bracket like all three prior examples ("untouched", "was dir₁…tr₁", "old" are all written between their brackets' corners). This is a second, and to my eye more visible, departure from the same convention.

**Right corner** is correctly placed at col 63 = rightSep+0, consistent with every other bracket. So the close end is fine; both defects are on the presentation of the *open* side and the caption.

### Held against the §5.1 figure (the other place corner characters appear)

I grepped the whole document for box-drawing corner characters:
```
grep -n "└\|┘\|┌\|┐" tarn.md
```
→ 5 lines: 667, 669 (the box's own top/bottom borders — ┌┬┐ / └┴┘, not annotation brackets), 670 (the annotation row under it), 3415, 3433 (the two lines already examined above). The charter's framing text ("four lines... carry them") does not match what I found (5 lines) — I flag this discrepancy rather than picking a side, but it doesn't change any of the analysis above, since lines 667/669 are table borders, not annotation brackets, and are not the kind of mark the charter or I am comparing against.

The §5.1 figure's annotation row (line 670), against its box row (line 668):
```
box row │ positions: 2, 10, 22, 30, 42, 50, 57, 62, 71
annotation row: └ at 10, ┘ at 22 (layer A, "tiles+index"); └ at 30, ┘ at 42 (layer B); └ at 50, ── ..., ┘ at 71 (re-emitted)
```
Here **both** corners sit exactly on top of the box row's own │ characters (leftSep+0, rightSep+0) — a different, symmetric convention from the §20.3 figures' asymmetric one (leftSep+1, rightSep+0). This is a real inconsistency *between figures*, but it predates this hunk (§5.1's figure is untouched by any of my three hunks) and is not something the repair could have introduced or fixed. I report it for completeness since the charter asked me to characterize every figure's convention, but it is not a finding against this commit.

**What this means for the repaired bracket:** held against its *own* figure's other bracket (the standard the charter asks me to apply first), the new bracket is wrong on the left corner and on caption placement. Held against the *different* convention used in §5.1 (a different figure, not cited or referenced by this Example), the new bracket's left-corner placement would actually be *correct* — but that is not the convention this figure itself uses, and a reader working only from figure (b)'s own "old" bracket (the nearest, most obviously comparable mark, three lines above) will see an inconsistency.

### Does the fix over- or under-shoot the original defect?

**Before:** the bracket was unclosed and ran to the end of the line, with the caption inside it. This meant a strict character-by-character reading had no defined right edge at all — the annotation could be (mis)read as reaching over `dir₂│pad│tr₂` as well as `index′`, which would be false (the directory/pad/trailer are not "entries" and are not "re-emitted" in the sense this caption means — they're freshly written every commit regardless, not a whole-region-rewrite-of-existing-entries claim). That was the defect the repair targets.

**After:** the close corner correctly stops at col 63, immediately before ` dir₂` begins (col 64) — so the overreach to the right is fixed and the bracket no longer claims anything about the directory/pad/trailer fields. Good.

On the left side, the new bracket's corner sits exactly on the boundary shared with "+tiles," rather than one column inside "index′" like every sibling bracket. Because the caption's own wording is unambiguous ("every **entry**, re-emitted" — "entry" is specifically an index-entry, §15's vocabulary, never used for tile payloads), I don't think this misalignment actually causes a false reading of *what* is being claimed (a careful reader still knows "entry" can't mean "+tiles," which are payloads, not entries). But it is a genuine, checkable **inconsistency in the figure's own drawing convention**, and a reader who checks column-for-column (as this audit was asked to do) will find the new bracket doesn't line up the way its neighbor does. This is exactly the shape of defect named in the charter's own list of prior-round failure shapes: "a figure's mark drawn to a convention the figure's other marks do not follow." I am filing this as a finding (non-byte-level, since it sits inside a labeled, non-normative Example, and the underlying normative rule in §20.3 step 4 is untouched and correct).

### Caption vs. the paragraph above the figure and step 4's index sentence

The paragraph immediately above the figure says three commit shapes "take the same shape" as (b): tiles added; stored tiles superseded; and an empty layer re-declared with no tile written (with index content changed). Step 4's own text says the re-emitted region always contains four categories of entry: newly-stored/superseded tiles' entries (new state), newly-unstored tiles' entries (sentinel), entries new to the generation (freshly emitted per §15), and "every other entry byte-identical at its disk-ordinal position." Crucially, that last category is *copied unchanged*, not re-encoded — yet it is still physically written into the new region, because "the whole region moves... a single changed entry costs its whole length" (the sentence immediately below the figure). So "every entry, re-emitted" is true in exactly the sense this document's own vocabulary gives "re-emit" — R-WRT-05 already establishes that "re-emit" applies even to byte-identical, unmodified content ("an updater MUST re-emit byte-identically ... every record it retains and does not logically modify"). Under that established sense, the caption is accurate for all three of the shape-(b) sub-cases, since in each of them the whole tile-index region — including its unchanged entries — is physically rewritten at a new placement. I checked this is true uniformly for all three (tiles added, tiles superseded, empty-layer re-declaration with index-content change) by re-reading step 4's own text, which does not carve out any of the three as an exception to "has its tile-index region re-emitted in full." No defect here.

### Sweeps for hunk 2

```
grep -n "└\|┘\|┌\|┐" tarn.md              -> 5 lines (667, 669, 670, 3415, 3433) — see above
grep -n "every entry" tarn.md              -> 1 hit (the caption itself, line 3433)
grep -n "re-emitted in full" tarn.md       -> 1 hit (line 3236, §20.3 step 4's own governing sentence)
```
Control: `grep -c "re-emit" tarn.md` → non-zero (many hits across §20.4/R-WRT-05/Appendix H), confirming the tool is working; the single-hit counts above for the more specific phrases are genuine, not search failures.

**Conclusion on hunk 2:** one confirmed, non-byte-level finding — the new bracket's left corner and its caption placement each depart from the convention every other bracket in this same figure (and the "old" bracket three columns to its left, in the very same annotation row) uses. The substantive claim the caption makes ("every entry, re-emitted") is accurate under the document's own defined sense of "re-emit," and the closing of the bracket correctly fixes the original overreach into the directory/pad/trailer fields.

---

## HUNK 3 — last row of §20.4's table

### The rule the repair adopts

Before: "...so **an updater** MAY drop the record in any commit it is otherwise free to make ... and a rewriter MAY drop it in any rewrite."
After: "...so **an appender** MAY drop the record in any commit it is otherwise free to make ... and a rewriter MAY drop it in any rewrite."

Only the first clause's actor noun changes; "and a rewriter MAY drop it in any rewrite" and the trailing "An updater that drops such a record SHOULD report the loss" sentence are untouched.

### Establishing the table's normative force

The table (`| Governing flags | Updater obligation |` at line 3503) is **not** inside a blockquote — no line in this table or its surrounding paragraph (lines 3475-3526) begins with ">". I confirmed this with a direct dump of the raw lines. Per R-CNF-01 this table is normative by default, since it carries no *Note*/*Example*/*Rationale* label and there is no such label anywhere nearby. This is, in fact, the specific "normative table in a '>'-free block" the charter's own framing material describes — I verified it directly rather than trusting that description. So this repair, unlike hunks 1 and 2, edits genuinely normative text, and I hold it to the byte-level test seriously.

### Check 1 — actors, sentence by sentence

I read §2.3's conformance-class definitions, §20.1 (writer tiers), and R-LIF-01/R-LIF-02/§9.2 (the commit protocol) to pin down exactly what each noun means:

- **"an appender"** — §20.1: "extends an existing file by commits (§9.2)." An appender's operation is, definitionally, a commit.
- **"a rewriter"** — §20.1: "writes a new file from an existing one under a new identity (§20.5)." §20.5, explicitly: *"That a rewrite is not a commit (`[R-LIF-01]`) fixes what the output* is*, not which rules govern the writing of it."* This is the single most load-bearing citation in this hunk, and it says exactly what the repair's premise needs: a rewrite and a commit are mutually exclusive operations.
- **"An updater"** — §2.3: "Its tiers, the appender and the rewriter, are §20.1's." So *updater* = {appender, rewriter}, no third tier, and a creator is explicitly *not* an updater (§2.3's "Conforming updater" is defined as "A tool that modifies an existing file, or as a rewriter writes a new one from it" — a creator does neither).
- **§9.1/R-LIF-01, verbatim:** "A TARN file changes only by commit... and every conforming mutation of a file is either a commit (§9.2) or a whole-file rewrite under a new file_id (a rewrite, §20.5)." Disjoint, exhaustive (over *mutations*; creation is a third, non-mutation case handled separately by §9.2's own "on creation there is no prior trailer" clause and by §20.1 calling a creator's output "one commit" — but a creator is never an updater, so this doesn't matter for who is licensed to drop a *pre-existing* PE=0 record, since a creator never has one).

**Is every updater an appender or a rewriter?** Yes, exhaustively, per §2.3's own sentence quoted above — there is no third updater tier.

**Is anything that commits not an appender?** A creator's first-generation write is also called "one commit" (§20.1's creator bullet, and §9.2's "on creation there is no prior trailer... performs steps 2–6"). So strictly, "commit" as a term covers both appenders' and creators' writes. But a creator never inherits a pre-existing PE=0 record to preserve or drop (§20.1: "As a creator it undertakes nothing toward its input... it writes flags = 0" — nothing is carried forward at all), so the drop question this table row exists to answer is vacuous for a creator; "an appender MAY drop the record in any commit" is not narrower in *effect* than "an updater/anyone MAY drop the record in any commit" would have been, since the only actor other than the appender who ever commits (the creator) never faces this choice. I could not find a scenario in which a creator holds a PE=0 record inherited from an existing generation — by definition it has no existing generation.

**Is a rewriter's output produced by a commit?** No — R-LIF-01 and the explicit §20.5 sentence quoted above settle this without ambiguity. This is exactly the premise the round-36 finding (quoted in my charter) states, and I verified it independently rather than accepting it on the charter's word.

### Did the narrowing take a drop from any actor, or give one to any?

- **Appender:** explicitly still licensed ("an appender MAY drop the record in any commit..."). No change.
- **Rewriter:** its licence is stated in the untouched second clause ("and a rewriter MAY drop it in any rewrite"), corroborated independently by §20.5's own prose ("dropping a layer or another record §20.4's table licenses dropping, which a commit does by omitting the record and stranding what it addressed (§20.4) and a rewrite does reclaiming it") and by §20.3 shape (c) ("dropping a layer or another PE = 0 record where §20.4 licenses the drop..."), and by §7.2's own step-2 language ("MUST NOT drop the record save where §20.4 licenses the drop" — this whole procedure is captioned "An appender MUST, in order:", confirming §20.3's drop language was always about the appender specifically). No change.
- **Creator:** never had this licence and still doesn't (irrelevant, as above). No change.
- **"An updater that drops such a record SHOULD report the loss"** — untouched, still names "An updater" (the union of both tiers), which is exactly right since both routes (commit-drop and rewrite-drop) are covered by "updater."

So: **no actor gains or loses a drop by this edit**, exactly as the repair's own rationale (per my charter) claims. I verified this by tracing every actor through §2.3, §20.1, §20.3, §20.5, and R-LIF-01 rather than taking the claim at face value.

### Check 4 — contradiction across the whole passage

I read the MU=1 row, the flags paragraph above the table, and the paragraph below the table in full (quoted below), specifically hunting for a MUST the new MAY now lets someone violate, or a carve-out the new breadth collides with.

- **MU=1 row** (unaffected by this hunk, but read for contradiction): "The updater MUST NOT modify the scope the record governs... At either scope a rewriter MUST refuse to rewrite the file, on `[R-WRT-06]`'s own ground." This row *already* used the same generic-updater / specific-rewriter mixed style the repaired row now also uses — so the repaired row's style is consistent with its sibling row, not a new pattern.
- **Flags paragraph above the table** ("the layer record carries PE = 0 and is dropped under the table's last row... the permission to drop it is the bit's alone") — names no actor, so it cannot conflict with the more specific actor-splitting done in the row itself.
- **Paragraph below the table** (lines 3509-3526), read in full:
  > "A commit MAY therefore drop a layer record, and the drop takes the layer whole... One sub-record blocks the drop, a sub-record of a type the updater does not implement with MU = 1, the drop being a modification of the scope it governs (the table's first row). A commit never removes a user-metadata record from a scope it keeps... Dropping a layer by commit strands its stored tiles... which only a rewrite reclaims, so the file is no smaller than before... a writer SHOULD instead rewrite where a drop would strand a large share of the file's stored bytes, a rewrite that drops the layer (§20.5) reclaiming what the commit would strand, and an updater that drops a layer SHOULD report the loss, as the table says of any record dropped."

  This paragraph explicitly discusses *both* the commit-route drop (stranding) and the rewrite-route drop (reclaiming) as two parallel mechanisms, exactly matching the table row's own two-clause structure post-repair. **Check 8 (the "therefore"):** before the edit, "A commit MAY therefore drop a layer record" followed from "an updater MAY drop the record in any commit"; after the edit, it follows from "an appender MAY drop the record in any commit." Since "commit" was already, in effect, exclusively the appender's operation (a rewriter never commits, established above), the antecedent this "therefore" needs is unchanged in substance — only made more precise. I don't find the "therefore" now claiming anything different than it did before the edit.
  **The closing SHOULD-sentence, held word for word:** the row's own SHOULD sentence, untouched by the repair, reads "An updater that drops such a record SHOULD report the loss." The paragraph below reads "an updater that drops a layer SHOULD report the loss, as the table says of any record dropped." Actor ("An/an updater") matches, keyword (SHOULD report the loss) matches. No drift between the two.
- No MUST elsewhere in this passage is now violable by the new MAY, and no carve-out narrows what the new MAY grants: I specifically checked whether the MU=1 row's "blocks modification of that layer, its drop included" (an MU=1 sub-record blocking a PE=0 sibling's drop) still holds against the new wording, and it does — "an appender MAY drop the record in any commit **it is otherwise free to make**" is exactly the qualifier that defers to the MU=1 block; this qualifier is untouched by the repair.

### Check 5 — exhaustive-claim words

The repaired sentence contains "any commit," "any rewrite," and "otherwise free to make." I tried to falsify "any": is there a commit the appender is "otherwise free to make" in which it nonetheless may *not* drop this record? Only if the MU=1 carve-out or some other rule blocks that specific commit — but that's exactly what "otherwise free to make" excludes by its own wording, so it's not a counterexample, it's the qualifier doing its job. I found no commit that is "otherwise free" (i.e., not independently blocked) in which the drop is nonetheless barred. Same check for "any rewrite" against §20.5's refusal conditions (an MU=1 unimplemented type forces refusal of the *whole rewrite*, not a partial one — so again, not a counterexample to "any rewrite [that the rewriter undertakes at all] MAY include this drop"). No overclaim found.

### Check 6 — what else in this structure is left unconstrained

The structure here is the table row itself, which fixes: (a) who may drop a PE=0 record and under which operation, and (b) who should report a drop. I looked for a sibling quantity in the same row or table that the repair should have addressed but didn't:
- The **MU=0, PE=1 row** ("Retain byte-identical, extent content unmodified") states an unconditional retention duty with no drop-licence at all, so it has no commit/rewrite split to make in the first place — nothing left unconstrained there.
- The **asymmetric parenthetical** — the appender's clause carries an aside, "one whose only effect is the drop included," clarifying that a drop-only commit is still a legitimate commit; the rewriter's clause carries no analogous aside. I checked whether this needs one: §20.5 already establishes that a rewrite is inherently a whole-file operation that can combine drops, re-creations, and carries in any combination ("A rewrite MAY do several of these at once, dropping one layer, re-declaring another and carrying the rest forward, and is compaction only where it does nothing but carry") — so there is no analogous doubt for a rewrite that a drop-only rewrite is legitimate; the appender's aside answers a question (is dropping enough, on its own, to justify a commit?) that doesn't arise for a rewrite. Not a defect.
- I checked whether "creator" being silently absent from this row leaves anything about *creators* unconstrained — it doesn't, since a creator can't hold a PE=0 record it inherited (established above).

### Check 7 — analogy comparison

No "exactly as," "the same way," or similar analogy marker appears in this hunk's own new text; the sentence states the rule directly rather than deriving it from another rule by analogy. N/A for this check.

### Check 8 — anaphora after the insertion

This repair replaces one word ("updater" → "appender") inside an existing sentence; it does not insert a new sentence or clause between two existing ones, so there is no new "insertion point" whose forward back-references could silently re-resolve. I nonetheless walked forward through the rest of the row and the paragraph below for every back-reference:
- "**one** whose only effect is the drop included" → resolves to "commit," unchanged before/after.
- "A commit MAY **therefore**..." → resolves to the appender's MAY-clause, discussed above; unchanged in substance.
- "**as the table says** of any record dropped" → resolves to the row's own SHOULD sentence, which the repair did not touch; still matches actor-for-actor and keyword-for-keyword (see Check 4 above).

No back-reference silently changed its target.

### Restatement sweep (who may drop what, who reports it)

I read every location my charter named and quote the actor noun used in each:

- **§7.2's Note** (line 1040): "An updater that does not implement an MU = 1 record's type never drops the record" — about MU=1, not this hunk's MU=0/PE=0 row; "updater" here is correct and untouched territory.
- **§20.1's rewriter bullet** (line 3141-3146): "rewriter — writes a new file from an existing one... carrying structures forward, re-creating some, or dropping some." Generic "dropping," no conflict with the row.
- **§20.3 step 2** (line 3219-3220): "MUST NOT drop the record save where §20.4 licenses the drop." This whole procedure is introduced as "An appender MUST, in order:" (line 3200) — so this "MUST NOT drop... save where licensed" is *already*, and always was, about the appender specifically, matching the row's post-repair "appender" language precisely.
- **§20.3 step 4** (lines 3294-3299): "a commit MAY drop the layer (§20.4)" — again inside the appender's own procedure; "commit" is the appender's operation throughout this section. Consistent.
- **Shape (c) of the three-shapes Example** (lines 3441-3459): "dropping a layer or another PE = 0 record where §20.4 licenses the drop" — again within the (non-normative, labeled) Example illustrating the appender's procedure. Consistent, no actor-noun conflict.
- **§20.5's opening** (line 3561-3563): "dropping a layer or another record §20.4's table licenses dropping, which **a commit** does by omitting the record and stranding what it addressed (§20.4) and **a rewrite** does reclaiming it" — this is the single clearest independent corroboration of the row's post-repair split: commit-drop vs. rewrite-drop, named exactly the way the row now names them.
- **§20.5's disposal sentence** (lines 3652-3655): "`[R-WRT-06]` then leaves it two disposals... drop the layer, which §20.4's table licenses and whose loss **the rewriter** SHOULD report as that table says, or refuse." Actor "the rewriter," matches "An updater... SHOULD report" (rewriter ⊂ updater) with no drift.
- **§20.5's regeneration paragraph** (lines 3628-3644): no drop language relevant to this row (about relocation/regeneration of index regions for content it carries forward, a different topic).
- **§21.6's row for an experimental-range record with MU = 0** (line 4029): "Ignored, and preserved or dropped per its PE bit" — no actor named; not in tension with either wording.
- **§23.1** (lines 4356-4382): "a record's extent goes the same way whether **a commit** drops the record (§20.4) or supersedes it," and "**a commit** that drops a layer (§20.4) strands every tile it stored." Both use "a commit" as the drop mechanism, consistent with (and arguably anticipating) the row's post-repair "appender ... in any commit" wording, since only an appender's operation is ever called a "commit" in this drop context.
- **Appendix G** — I searched it; it does not discuss record-drop licensing at all (it's the reproducible-writer profile, about canonical placement/byte determinism), so it is not a restatement site for this rule.
- **Appendix H's updater entry** (lines 4924-4954): "drops a layer record only under §20.4's PE = 0 licence, its sub-records with it... (§20.4)" appears in the shared (appender-applicable) part of the updater checklist, immediately followed by a separately-labeled rewriter-specific clause: "A rewriter, in addition,... drops a layer or a PE = 0 record by omitting it, **reclaiming** what it addressed... (§20.5)." This is an independent, pre-existing restatement of exactly the same commit(strand)/rewrite(reclaim) split the table row's repair encodes — further corroboration, not a conflict. The advisory sentence closing that entry — "an updater that drops a record SHOULD report the loss (§20.4)" — again uses "updater" (both tiers), matching the row's untouched SHOULD sentence.

I found no site where "updater" is used in a way that, read together with the repaired row's "appender," leaves some actor's licence or duty undecided or stated two conflicting ways. Every site either (a) is not about this MU=0/PE=0 drop rule at all, (b) already used the commit/appender vs. rewrite/rewriter split independently, or (c) uses "updater" correctly to cover both tiers together (the SHOULD-report duty, which both tiers share).

### BCP 14 casing and NESTED_DASH

- Casing: "MAY" (×2) and "SHOULD" (×1) in the repaired row are all-caps, correctly. No casing defect.
- Em-dashes: the row's touched sentence contains exactly one em-dash *pair* — "— one whose only effect is the drop included —" — and it is not nested inside another dash-delimited clause (there is no outer dash pair enclosing the whole "so an appender ... any rewrite" clause). NESTED_DASH: not applicable, no nesting found.

### Byte-level test

Since a rewrite can never be a commit (R-LIF-01, and the explicit "that a rewrite is not a commit... fixes what the output *is*" sentence in §20.5), "an updater MAY drop the record in any commit" and "an appender MAY drop the record in any commit" describe **exactly the same set of permitted operations** — the rewriter branch of "updater" was always vacuous against the predicate "in any commit," since no rewriter ever satisfies it. The rewriter's actual drop permission is, and remains, stated in the untouched second clause. So the set of files a conforming appender or a conforming rewriter may produce is identical before and after this edit; a verifier's or reader's accept/reject verdicts are likewise unaffected, since nothing about detection, outcome class, or scope changed. **Not byte-level.**

**Conclusion on hunk 3:** I did not find a defect. The repair's own claim ("no actor gains or loses a drop by it") holds up under all eight checks and the full restatement sweep I ran, and is independently corroborated (not merely asserted) by §20.5's own prose, §20.3's procedure header, §23.1, and Appendix H's pre-existing appender/rewriter split. This is the hunk the charter itself flags as highest-risk ("the hunk to read hardest... whose table and the paragraphs either side of it this cycle's commits rewrote again and again"), so I gave it the most exhaustive treatment of the three; I record that thoroughness here rather than asserting confidence without showing the work.

---

## Rejected candidates

1. **Hunk 1 — comma before "and" in a two-item list.** After striking "verifiers," "appenders, and rewriters carrying a layer forward," retains a comma that made sense in the original three-item list but is non-standard for two items. Closed: I could not construct a parse in which this comma changes what the sentence claims (see Check 1 above) — it's a stylistic leftover, not a semantic fork.
2. **Hunk 1 — should "verifiers" have been kept, reworded, in the Note?** A non-certifying verifier genuinely does "operate on a file whose layers it cannot decode" (§17.4/R-COD-11). Closed: the Note's own payoff clause is scoped to "the updater rules of §7 and §20," and verifiers are not updaters (§2.3), so the Note never needed to make a claim about verifiers to do its stated job. This is a completeness question, not a correctness defect — I looked for, and did not find, any place downstream that needs the Note to say something about verifiers that it no longer says.
3. **Hunk 2 — does the misaligned left corner cause the bracket to be read over "+tiles"?** Closed: the caption's own word "entry" (§15's vocabulary) cannot refer to "+tiles" (raw tile payloads, not index entries), so even with the one-column shift, no reader is misled about *what* the annotation refers to — only that the drawing itself doesn't match its sibling bracket's convention. Filed as a (non-byte-level) finding on the drawing-convention grounds alone, not on a "wrong field labeled" grounds.
4. **Hunk 2 — does "every entry, re-emitted" contradict "every other entry byte-identical at its disk-ordinal position" (step 4)?** Closed: no contradiction, because "re-emit" in this document's defined usage (R-WRT-05) means "write out again," not "change the value of" — byte-identical content can still be, and per step 4's own text is, physically re-emitted when its containing region is rewritten at a new placement.
5. **Hunk 3 — does "an appender MAY drop... in any commit" wrongly exclude a creator's first-generation "commit"?** Closed: a creator never inherits a PE=0 record from a prior generation (§20.1: "writes flags = 0," nothing carried forward), so the drop question this row answers cannot arise for a creator; the narrowing removes no real permission from anyone.
6. **Hunk 3 — asymmetric parenthetical ("one whose only effect is the drop included") only on the appender's clause, not the rewriter's.** Closed: §20.5 already establishes that a rewrite may combine any mix of drop/re-create/carry, so there's no analogous doubt to resolve for the rewriter; the asymmetry answers a question that only arises for commits.

## Confidence for the near-empty result (hunks 1 and 3)

For hunks 1 and 3, where I am reporting no confirmed defect, this is what I did that *would* have caught one if it were there: I traced every actor noun used in the repaired sentence through its formal definition in §2.3 and §20.1 rather than relying on intuition about what "appender," "rewriter," or "updater" mean; for hunk 1 I built the full six-actor table (Check 5) rather than checking only the actors the repair mentions; for hunk 3 I ran the full restatement sweep across every site my charter named (§7.2, §20.1, §20.3 steps 2/4 and shape (c), §20.5 ×3, §21.6, §23.1, Appendix G, Appendix H) and quoted each site's actor noun rather than summarizing whether it "seemed consistent"; and I specifically hunted for the failure shapes the charter warned are this project's actual record (a scope corrected and a tense broken, a list widened and its partition claim broken, a rider added to one row and its sibling left saying the old thing, a class line drawn on a test that turns with input) against both hunks and did not find an instance of any of them. What I could not fully rule out, and say so rather than silently passing over: whether some document location outside the ones my charter named (§7.2, §20.1, §9.2, §20.3 shape (c), §20.5, §21.6, §23.1, Appendix G/H for hunk 3; the whole-document greps for hunk 1) restates either rule in a way I didn't find by grepping for the specific phrases I chose — my sweeps are as exhaustive as the phrase choices I made, not a proof that no other phrasing exists anywhere in a 4981-line document.

## Sweeps run (verbatim, with hit counts and controls)

```
grep -n "cannot decode" tarn.md                    -> 1  (line 440)
grep -n "undecod" tarn.md                          -> 0
grep -n "without decoding" tarn.md                 -> 2  (lines 83, 90)
grep -n "does not decode" tarn.md                  -> 0
grep -n "opaque" tarn.md                           -> 4  (lines 1230, 1241, 1253, 4624)
grep -n "cannot execute" tarn.md                   -> 2  (lines 225, 2617)
grep -n "decodes every" tarn.md                    -> 0
grep -n "carrying a layer forward" tarn.md         -> 1  (line 439)
grep -n "load-bearing for the updater" tarn.md     -> 1  (line 441)
grep -n "load-bearing" tarn.md                     -> 5  (lines 366, 370, 441, 1796, 4062)
grep -n "Part I\|Part II" tarn.md                  -> 9 lines (82,84,89,91,92,312,420,437,438 + Part headers)
grep -n "└\|┘\|┌\|┐" tarn.md                       -> 5  (lines 667, 669, 670, 3415, 3433)
grep -n "every entry" tarn.md                      -> 1  (line 3433)
grep -n "re-emitted in full" tarn.md                -> 1  (line 3236)
grep -n "MAY drop\|MAY therefore drop\|drop it in any\|drop the record in any" tarn.md -> 3 (lines 3294, 3507, 3509)
grep -n "SHOULD report the loss\|report the loss" tarn.md -> 4 (lines 1265, 3507, 3524, 4954)
grep -n "R-LIF-01" tarn.md                          -> 10 hits (1285, 1328, 1393, 3129, 3158, 3218, 3239, 3276, 3588, 3604)
grep -n "R-WRT-09" tarn.md                          -> 7 hits (3167, 3572, 3577, 3655, 3727, 4926, 4950)
grep -c "decode" tarn.md   (control)                -> 142
grep -c "re-emit" tarn.md  (control)                -> non-zero, many hits
python3 whitespace-normalized re-check of all zero/low-count searches above -> identical counts (see hunk 1 section)
```

## Derived numbers

- Character-column indices for every box-drawing character in lines 3413-3415, 3431-3433, 3467-3468, 667-670, computed via a Python script reading the raw file bytes as UTF-8 codepoints (not bytes), cross-checked twice (once via a filtered-character dump, once via a raw per-column dump of the specific range in question) — see the "Character-column analysis" section above for the values and their comparison against the field boundaries in each figure's own "after" or box row.
- Dash-fill width of the repaired bracket: 8 columns (cols 55-62), compared against the "index′" field's own content width, also 8 columns (│54..│63 ⇒ 63-54-1 = 8) — these match, confirming the bracket's *width* is correct even though its *left edge* is shifted by one column relative to the figure's convention.
- Count of box-drawing corner-character lines in the whole document: 5 (667, 669, 670, 3415, 3433), against the charter's stated expectation of 4 — a discrepancy I report above rather than silently reconciling.
