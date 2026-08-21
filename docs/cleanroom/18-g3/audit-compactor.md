# Round 18 repair audit — hunk-04 (§20.5, structurally-invalid tile-index entry)

Auditor scope: hunk-04.diff only. Working transcript of record.

## 0. Access disclosure

Files opened:

- `/private/tmp/claude-501/-Users-robertkleffner-Documents-GitHub-tarn/2c60df09-4efe-4196-a7da-930efc26640f/scratchpad/round18-audit/hunk-04.diff` (my charter hunk, in full)
- `/Users/robertkleffner/Documents/GitHub/tarn/spec/tarn.md` — read in ranges:
  170–199, 1310–1369, 2030–2079, 2145–2174, 2648-heading-scan, 2744–2770,
  2770–2824, 2840–2949, 3085–3109, 3120–3259, plus `sed` extracts of
  3151–3160 and 2916–2932 unwrapped.

Nothing else was read. I did **not** open `full.diff`, any other hunk file,
`docs/`, `PLAN.md`, `OPEN-QUESTIONS.md`, `AGENTS.md`, `README.md`,
`conformance/`, `spec/registry.json`, git history, or the web. I did not list
the audit directory. No breach to disclose.

Commands run (all against `spec/tarn.md` only):

```
grep -n 'R-WRT-06' spec/tarn.md
grep -n 'R-WRT-01\b' spec/tarn.md
grep -n 'reject-tile' spec/tarn.md
grep -n 'R-IDX-03\|R-WRT-09\|R-CNF-05\|R-CNF-06' spec/tarn.md
grep -n 'compactor\|compaction' spec/tarn.md
grep -n 'travels\|travel ' spec/tarn.md
grep -n 'carried forward byte-identical\|byte-identically at its disk-ordinal' spec/tarn.md
grep -n 'need not have looked\|has detected\|it has detected' spec/tarn.md
grep -n 'refus' spec/tarn.md
grep -n '#### 19\.' spec/tarn.md
sed -n '3260,3300p' spec/tarn.md            (§21.1)
sed -n '3151,3160p' spec/tarn.md | tr '\n' ' '   (unwrap)
sed -n '2916,2932p' spec/tarn.md | tr '\n' ' '   (unwrap)
```

Hard-wrap note: `grep -n 'it has detected'` returned **nothing**, and that is a
wrap artifact, not evidence — line 3160 ends `...carrying a violation it has`
and line 3161 begins `detected:`. I recovered the sentence with the `sed | tr`
unwrap above and by reading 3151–3182 directly. Every negative conclusion below
rests on a read of the passage, not on a failed line-oriented grep.

## 1. The rule the repair adopts, in my words

Before: a tile-index entry that §15.3 classifies reject-tile on a *structural*
ground is copied into the regenerated index region with its offset and length
byte-for-byte as they stood, the violation travels into the compactor's output,
and this is **not** a case where `[R-WRT-06]` obliges the compactor to refuse.

After: the presence of such an entry in a region the compactor would regenerate
**obliges the compactor to refuse to compact at all**. The output file is never
produced. The stated ground is: (a) the regenerated region is bytes the
compactor *produces*, and §20.1 makes it answer for produced bytes in full;
(b) it cannot reproduce the entry and cannot invent a replacement; (c)
`[R-WRT-01]`'s travel licence "reaches only" structures the commit neither
modifies nor relies on, and a regenerated region is not one; (d) `[R-WRT-09]`'s
shallower reach means only that the compactor *need not have looked*, and
"where it has, this is the disposal."

Operationally, for an implementation: a compactor that classifies index entries
per §15.3 and finds a structural one must emit no file. A compactor that never
classifies has — after the repair — no stated behaviour for such an entry at
all, because the sentence that told it what to emit was deleted.

## 2. Check 1 — tense and quantifier

Generation: correct. The repair speaks about the input's live committed state
(the entry as it stands in the file being compacted) and about the output the
compactor would produce. No tense slippage found.

Set: **this is where the repair moves the goalposts.** `[R-WRT-01]` quantifies
over "a structure they neither modify nor rely on". The document elsewhere
applies that quantifier at **entry** granularity; the repair applies it at
**region** granularity. §20.3 step 2 is explicit that the individual entry is
the structure:

> "a violation latent in a structure it neither modifies nor relies on travels
> with that structure (§20.1, `[R-WRT-01]`) — which is as true of an index
> entry copied to its disk-ordinal position as of a record re-emitted
> byte-identically (`[R-WRT-05]`)."  (lines 2925–2929)

The repair instead reasons over the containing region: "which a regenerated
region is not." Same requirement, two granularities, opposite outcomes. The
granularity shift is silent — nothing in the repaired text acknowledges that
the document had already fixed the granularity at the entry. This is the root
of findings C-01 and C-02.

## 3. Check 2 — citations resolve

Every identifier and section number in the repaired text, opened and read.

| Cited | Where it lives | Verdict |
|---|---|---|
| §15.3 ("classifies reject-tile on a structural ground") | 2030–2059, tagged `[R-IDX-03]` | **PASS.** "Six rows are marked *structural*" (2035); all six outcome cells read "*structural*: reject-tile" (2050–2055). The phrase resolves exactly. |
| `[R-WRT-06]` ("obliges the compactor to refuse") | paragraph 3151–3182, tag at 3182 | **PARTIAL PASS.** The paragraph does contain "MUST NOT emit a file carrying a violation it has detected" and "Where the table does not license a drop the compactor MUST refuse." An index entry is not a record, so §20.4's table licenses no drop for it, and refusal follows. But the paragraph's obligation is expressly conditioned on the violation being **detected**; the repaired sentence states the obligation unconditionally. See C-04. |
| §20.1 ("makes it answer for those in full") | 2857–2874 | **PASS as to bytes produced.** "An appender and a compactor satisfy every writer requirement for the bytes they produce ... (`[R-CNF-06]`)" (2867–2870). §20.1 says nothing about whether *reproducing* bytes counts as producing them — the document answers that elsewhere, and answers it the other way (see C-02). |
| `[R-WRT-01]` ("licence ... reaches only a structure the commit neither modifies nor relies on") | tag at 2874, text 2867–2873 | **FAIL on the exhaustive half.** The cited text is: "a violation latent in a structure they neither modify nor rely on travels with it". That is a sufficient condition. There is no "only", no "and no other structure", no exclusion clause anywhere in §20.1. The limit the repair attributes to `[R-WRT-01]` is an inference, not the cited text. See C-03. Also: `[R-WRT-01]` quantifies over the actors ("they" = an appender and a compactor); the repair substitutes the operation ("the commit"), which sweeps appenders in — see C-02. |
| `[R-WRT-09]` ("checks reach the index chain and each stored tile's entry crc rather than an entry's own value domain") | paragraph 3246–3252 | **PASS.** `[R-WRT-09]` names: the open (§19.1), each retained layer's record (§19.3), the full index chain (`[R-IDX-04]`), and each relocated extent's checksum including every stored tile's entry crc. I opened §19.3 (2744–2768): it is a list of directory-resident checks and contains **no** §15.3 per-entry classification. I opened `[R-IDX-04]` / §15.4 (2061–2072): crc_of_crc_array and segment CRCs only. So `[R-WRT-09]` genuinely does not reach an entry's own value domain. The characterisation is accurate. |
| `[R-SLB-01]`, `[R-SLB-03]` in the line-3184 lead-in | 2149–2168 and elsewhere | Not part of the repair (unchanged context), but read: `[R-SLB-03]` at 2155–2158 says structural entries "are transparent to run continuity". Consistent with the repair; no collision. |

Citation the repair **deleted**: `[R-IDX-03]` ("gives such an entry no stored
extent and no claimant in the coverage walk"). I checked that the deleted claim
was true — §15.3 lines 2036–2041 ("Such an entry contributes no stored extent
to the *verifier* rows ... and none to `[R-LIF-08]`'s coverage walk") and §9.7
lines 1325–1327 and 1356–1359 both say it. It was a correct citation; its
removal is what leaves C-04's gap.

## 4. Check 3 — the repair sits in normative text

Lines 3184–3211 are ordinary paragraph prose. No line in the repaired range
begins with ">". The paragraph carries the tag `[R-WRT-07]` at line 3211. The
Example block at 3213–3244 is a ">" block and was **not** the landing site.
So: the repair has normative force. **Check 3 passes.**

Distinctive-terms grep for the rule as stated (remembering the wrap):
`grep -n 'refus'` returns 3159, 3167, 3179, 3190 — all in §20.5, all in
running prose, none in a ">" block. `grep -n 'need not have looked'` returns
only 3198, the repair itself. No competing statement of the new rule sits in a
blockquote, and the repair did not edit a blockquote.

One structural note: the new MUST-refuse obligation is stated inside the
paragraph tagged `[R-WRT-07]` while being attributed to `[R-WRT-06]`. That is
tolerable — §20.5 does this elsewhere (line 3204 cites `[R-WRT-06]` from inside
the same `[R-WRT-07]` paragraph) — but it means `[R-WRT-06]`'s own paragraph
never mentions index entries, so anyone reading `[R-WRT-06]` alone will not
find this disposal.

## 5. Check 4 — contradiction in the same passage, including untouched text

I read the whole of §20.5 (3149–3256), the whole of §20.4 (3099–3147), and the
whole of §20.3 (2891–3097 in the parts that bear). Two collisions, both with
text the repair did not touch.

### 5a. Same subsection, two paragraphs up — `[R-WRT-01]`'s licence stated the other way

§20.5 first paragraph, lines 3155–3158 (unwrapped):

> "A compactor satisfies every writer requirement for the bytes it produces
> (`[R-CNF-06]`), and a violation latent in a structure **it carries forward
> verbatim** travels into its output (`[R-WRT-01]`)"

The repair, lines 3193–3195:

> "`[R-WRT-01]`'s licence for a latent violation to travel **reaches only a
> structure the commit neither modifies nor relies on**, which a regenerated
> region is not."

These are two different statements of the same licence's scope, 35 lines apart,
in the same subsection, both normative, both citing `[R-WRT-01]`. Under the
first, the test is *carried forward verbatim* — and a structurally invalid
entry whose offset and length are reproduced exactly as they stand is carried
forward verbatim, so the licence reaches it and the violation travels into the
output. Under the second, the test is *neither modified nor relied on at region
granularity* — and it does not reach the entry, so the compactor must refuse.
The first paragraph still says the old thing. This is the "restatement the
repair should have swept" pattern, and it sits inside the very subsection the
repair edited. → **C-01**.

### 5b. §20.3 step 2 — the appender is told to do exactly what the compactor is now forbidden to do

Lines 2917–2929 (unwrapped), inside the numbered steps of "An appender MUST, in
order:", i.e. normative, not a blockquote:

> "a malformed index entry an appender meets **while re-emitting a region** is
> carried forward byte-identically at its disk-ordinal position under step 4,
> not repaired to a sentinel. ... **Reproducing a structure's bytes unchanged
> is not authoring them**: an appender satisfies its writer obligations for the
> bytes it produces, and a violation latent in a structure it neither modifies
> nor relies on travels with that structure (§20.1, `[R-WRT-01]`) — which is as
> true of an index entry copied to its disk-ordinal position as of a record
> re-emitted byte-identically (`[R-WRT-05]`)."

And step 4, lines 2937–2945: the appender's index region is "re-emitted in full
— entry_count entries plus the segment CRC array — necessarily at a new
placement", with "every other entry byte-identical at its disk-ordinal
position". That is a regenerated region by any reading of the word.

So the document already holds, normatively, that (i) an index entry inside a
freshly re-emitted region **is** a structure the writer neither modifies nor
relies on, and (ii) producing a region's bytes does not make a reproduced
entry's violation the writer's own. The repair asserts the negation of both, as
a general proposition about `[R-WRT-01]` and §20.1 — requirements §20.1 states
jointly for "an appender **and** a compactor" (2867–2870). And the repair's
subject is "**the commit**", not "the compactor": an appender's operation is a
commit; compaction, per line 3170 and `[R-LIF-01]`, is a whole-file rewrite. So
the repaired sentence, read as written, most naturally binds the appender —
where §20.3 says the opposite. → **C-02**.

I looked for a sentence anywhere that distinguishes appender from compactor on
this ground and would license the divergence. The nearest is §20.5's
compactor-only "MUST NOT emit a file carrying a violation it has detected"
(3160–3161). That *is* a defensible ground for the reversal — but it is not the
ground the repair gives, and the ground the repair gives contradicts §20.3.

### 5c. Contradictions I looked for and did **not** find

- **A carve-out in §20.5 that the new breadth collides with.** None. §20.5's
  disposal ladder at 3159–3167 (refuse on failed `[R-WRT-09]` check; MUST NOT
  emit a detected violation; drop only where §20.4's table licenses; otherwise
  MUST refuse) is consistent with the new obligation, since §20.4's table
  governs records only and licenses nothing for an index entry.
- **Does anything describe what a refusing compactor does?** Yes: "MUST refuse
  to compact" appears at 3159, 3167 (implicitly), 3179 and now 3190. Refusal is
  an established, defined outcome in this subsection; no output file is
  produced. `grep -n 'refus'` shows nothing in §21 that describes compactor
  refusal, and none is needed — §21 rows are file conditions, not actor
  procedures, and §21.1's completeness clause is scoped to "detectable
  file-conformance violations". **No inconsistency here.**
- **Does the surrounding enumeration still hold?** Yes, and it is arguably
  tightened. Post-repair, an entry in a successfully compacted region is either
  a valid sentinel (unchanged) or a well-formed stored-tile entry (offset new;
  length and crc unchanged) — the entry whose stored bytes fail its crc is
  caught by `[R-WRT-09]`'s "every stored tile's entry crc" (3251) and refused
  under 3159. So "entry offsets new; entry lengths, entry crcs, and sentinel
  entries unchanged" is now exhaustive over the entries that reach the output.
  No defect.
- **Register rows that presuppose survival.** L41 (3439) and `[R-SLB-03]`
  (2155–2158) both treat structural entries as transparent, and §9.7 /
  `[R-LIF-08]` (1325–1327, 1356–1359) says the coverage walk passes over one.
  All three describe files in general — corrupted files a verifier meets — not
  compactor outputs. None of them says a compactor may emit one. **Not a
  collision.**
- **§20.4 table.** No row bears on index entries. No collision.
- **The Example block 3213–3244.** Says nothing about invalid entries. No
  collision.

## 6. Check 5 — exhaustive claims

Words in the repaired text promising completeness, each tested:

- **"reaches only a structure the commit neither modifies nor relies on"** —
  the exhaustive claim the charter flagged. Falsified twice from the document:
  by §20.5's own line 3157 ("a structure it carries forward verbatim") and by
  §20.3's line 2927 ("as true of an index entry copied to its disk-ordinal
  position"). And the limit is not present in the cited requirement's text at
  all. → **C-03**.
- **"in full"** ("§20.1 makes it answer for those in full") — §20.1 says "every
  writer requirement for the bytes they produce". "In full" is fair as to the
  requirement set; the load-bearing and unverified word is "produces", not
  "in full". No separate finding.
- **"neither reproduce the entry nor invent a replacement"** — a closed
  two-element disposal set. I tested for a third: repair to a sentinel (barred,
  §20.3 line 2919 and `[R-CNF-04]` line 177); drop the entry (impossible —
  entry_count is fixed by geometry); drop the containing record (§20.4 never
  licenses dropping a layer record, line 3125). The pair is genuinely
  exhaustive. **Passes.**
- **"this is the disposal"** — definite article, exhaustive. True only in the
  detected branch; see C-04.
- **"No other record payload carries a file offset"** (line 3201–3202) —
  unchanged context, not this repair's claim.

## 7. Check on grammatical and logical fit inside the host sentence

The host sentence runs 3184–3211: "A compactor preserves content but not
placement ... : every stored tile's bytes verbatim ... and every retained record
per §20.4, except that relocation re-points extent slots, regenerates each
relocated tile-index region (**entry offsets new; entry lengths, entry crcs,
and sentinel entries unchanged; an entry ... [repair] ...; segment CRCs
recomputed over the entries as re-emitted**), and updates the layer-record
fields covering a regenerated region (crc_of_crc_array)."

The parenthetical is a semicolon-delimited list of properties of the produced
region. The repair inserts, as the third list item, a **full sentence boundary**
— "... which a regenerated region is not. That `[R-WRT-09]`'s checks ..." — and
the trailing item "segment CRCs recomputed over the entries as re-emitted" now
hangs off the far side of that period, reading as a third clause of the new
sentence rather than as a sibling of "entry offsets new". The old text had a
long aside here too, but no sentence boundary; the period is new.

Logically, the item is also a category mismatch with its siblings: the other
items state what a field of the produced region contains, while this one states
that no region and no file are produced at all. → **C-05** (minor).

## 8. Byte-level determination

Applying the charter's discriminating test rather than my own intuition.

In every finding below, the disputed file is a compactor (or appender) output
that carries an entry §15.3 classifies reject-tile on a structural ground.
That condition is a register row — T6, T7, T8, T9, T10, T11 or T12 (lines
3461–3467), detector "reader", detection point "tile use". So the disputed file
carries a register-row violation and is nonconforming. Under `[R-CNF-05]` (line
180, "A writer MUST emit only conforming files") that file is barred to a
conforming writer under **both** readings, so the emittable set does not move.

**Every finding here is therefore non-byte-level.** I record, for the
maintainer's benefit and without inflating the classification, that the
readings do diverge on an operational *verdict* — one implementation emits a
(nonconforming) extended or compacted file, the other emits nothing — but that
divergence is over files no conforming writer may emit either way, which is
exactly the case the charter's test excludes.

## 9. Findings

### C-01 — §20.5's first paragraph still states `[R-WRT-01]`'s licence the old way

Location: §20.5, lines 3155–3158 (untouched) against the repair at 3193–3195.
Repair: sweep 3157. Either restate it as "a structure it neither modifies nor
relies on" to match, or — better, since it is the true ground — replace the
repair's `[R-WRT-01]`-scope argument with `[R-WRT-06]`'s own
"MUST NOT emit a file carrying a violation it has detected", which needs no
claim about the licence's outer boundary.

### C-02 — §20.3 step 2 is the unswept restatement, and the repair's reason contradicts it

Location: §20.3 step 2, lines 2917–2929 (untouched) against the repair at
3191–3195. Repair: distinguish the compactor expressly, on the detected-
violation ground, and drop the general propositions about `[R-WRT-01]` and
about produced bytes — or, if the maintainer intends the general rule, §20.3
step 2 must be reversed too and the consequences for appenders worked through.
Also replace "the commit" with "the compactor": compaction is a whole-file
rewrite, not a commit (line 3170, `[R-LIF-01]`), and "the commit" reads onto
the appender.

### C-03 — "reaches only" is a limit not present in the cited requirement

Location: repair line 3193–3194 citing `[R-WRT-01]` at §20.1 lines 2867–2874.
Repair: delete "reaches only ... which a regenerated region is not", or
demote the exhaustive form to the sufficient form the cited text actually
supports.

### C-04 — unconditional obligation, conditional detection, and a hole where the deleted sentence was

Location: repair lines 3189–3198. "obliges the compactor to refuse" is
unconditional; three clauses later, "a compactor need not have looked; where it
has, this is the disposal" makes the obligation conditional on detection —
which is also what `[R-WRT-06]` at 3160–3161 actually says. Worse, the repair
deleted the sentence that told a *non-detecting* compactor what to emit ("is
reproduced with its offset and length exactly as they stand"), so the
non-detecting branch — which the repair itself says exists — now has no defined
behaviour for an entry that names no relocatable extent. Repair: state the
obligation as conditional ("a compactor that detects such an entry MUST
refuse") and restore a disposal for the branch where it has not looked.

### C-05 — the reversal does not fit the list it landed in

Location: repair lines 3189–3199 inside the parenthetical opened at 3187.
Repair: lift the refusal out of the parenthetical into its own sentence after
the host sentence closes, leaving the parenthetical as the four-item list of
what the regenerated region contains.

## 10. Verdict

Five findings. Check 3 (normative placement) passes cleanly. Check 2 passes on
§15.3, `[R-WRT-09]`, §20.1-as-to-produced-bytes and `[R-WRT-06]`-as-to-detected-
violations, and fails on `[R-WRT-01]`'s "only". Checks 1, 4 and 5 each fail on
the same underlying move: the repair silently shifts `[R-WRT-01]`'s quantifier
from the entry to the containing region, and neither of the two places where
the document states the entry-granularity rule was swept. The repair's
*conclusion* (refuse) is defensible and is well supported by `[R-WRT-06]`'s own
paragraph; the repair's *argument* is not, and the argument is the part that
proves too much.
