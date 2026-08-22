# Repair audit — hunk-01, §18.2 `Window_Size` (round 21)

## 0. Disclosure

Files read: `/private/tmp/claude-501/.../r21audit/hunk-01.diff` (my charter's hunk,
the only file in that directory I opened — I did not list the directory, did
not open `full.diff`, did not open any other hunk), and
`/Users/robertkleffner/Documents/GitHub/tarn/spec/tarn.md`.

Nothing else was read. No `docs/`, no `PLAN.md`, no `OPEN-QUESTIONS.md`, no
`AGENTS.md`, no `README.md`, no `conformance/`, no `spec/registry.json`, no git
history/log/diff, no web.

**Unrequested context.** Before I began, my runtime placed in context: (a) a
project instruction file pointer (`CLAUDE.md` → `AGENTS.md`), (b) an index of
the maintainer's auto-memory notes with several entry titles and one-line
descriptions, (c) a stale task list naming prior rounds, (d) an MCP/skill
listing. I did not open any of those files. I have not used their contents as
evidence; every conclusion below is sourced to a line of `spec/tarn.md` quoted
in place. Disclosing as instructed.

Commands run (all read-only, all against `spec/tarn.md` only):

```
wc -l spec/tarn.md                                   -> 4375
sed -n '2380,2520p' spec/tarn.md
grep -n "Window_Size\|Window Size\|window size\|window bound\|window log" spec/tarn.md
grep -n "R-COD-06\|R-ERR-03\|R-MTA-09\|R-MTA-10\|R-CNF-10\|R-CNF-11" spec/tarn.md
sed -n '2255,2330p' spec/tarn.md
sed -n '3640,3690p' spec/tarn.md
sed -n '3500,3535p' spec/tarn.md
sed -n '190,300p' spec/tarn.md
sed -n '3536,3600p' spec/tarn.md
sed -n '3380,3420p' spec/tarn.md
grep -n "^#### 21\|^### 21\|^#### 22\|^### 22" spec/tarn.md
sed -n '3282,3360p' spec/tarn.md
sed -n '3728,3810p' spec/tarn.md
grep -n "\`\[R-CNT-25\]\`" spec/tarn.md
sed -n '470,495p;1420,1435p;2545,2575p;4350,4375p' spec/tarn.md
grep -n "^#### 17\|^### 17\|^#### 18\|^### 18\|^#### 19.2" spec/tarn.md
tr '\n' ' ' < spec/tarn.md | grep -o -E ".{200}on the size bound.{200}"
tr '\n' ' ' < spec/tarn.md | grep -o -E ".{160}(bound of its own|its own choosing|user-metadata guarantee|declines to decode a user).{160}"
grep -n "16 MiB\|8 MiB" spec/tarn.md
sed -n '4290,4350p' spec/tarn.md
sed -n '3688,3728p' spec/tarn.md
grep -n "R-CNF-05" spec/tarn.md
sed -n '150,190p' spec/tarn.md
```

Because the document is hard-wrapped, every phrase search that mattered was run
through `tr '\n' ' '` first (the two `tr | grep -o -E` lines above). Line-based
greps were used only for tokens that cannot wrap (`Window_Size`, requirement
IDs, `8 MiB`).

---

## 1. The repair, quoted from the current file (spec/tarn.md 2466–2472)

```
cannot read. The frame's declared `Window_Size` is unconstrained
here for the same reason, and takes the same treatment: a reader's
window bound is its own, no smaller than §21.9's guarantee for that
quantity, and a frame declaring more than the reader admits is
ignore-record on that ground — the reader's capability, not a
failure to decode within the meaning of R3, and no violation
(`[R-MTA-09]`, `[R-ERR-03]`). A **verifier** that declines to decode a document on
```

It sits in plain prose in §18.2 (no `>` prefix on any of the seven lines), in
the paragraph that terminates at line 2486 with `` `[R-MTA-09]` ``. Check 3 (the
repair must sit in normative text) therefore **passes on its face**; see §5
below for the converse half of check 3, the unswept restatement.

### The rule the repair adopts, in my own words

For a user-metadata document stored under encoding 2, no rule of this
specification limits the value the frame header declares for `Window_Size`. Any
value is conforming, and a writer may emit any of them. Each reader picks its
own maximum admissible window, which must be at least 8 MiB. If the frame
declares more than that reader's maximum, the reader skips the record
(ignore-record); the file is not thereby nonconforming, no register row is
violated, and register row R3 ("stored bytes fail to decode") does not apply
because the situation is a property of the reader, not of the file.

---

## 2. Check 1 — tense and quantifier

- Generation: not in play. Nothing here is stated over a superseded vs. live
  state; §18.2 speaks of the record as read.
- Set ranged over: "a frame declaring more than the reader admits" — indefinite
  singular over encoding-2 user-metadata frames, at **either** scope. §18.1
  establishes both scopes ("A file MAY carry one user-metadata document at file
  scope, and each layer MAY carry one of its own"), and R3/R4's Instances
  columns list "top-level extent; layer sub-record extent". The repair's
  quantifier is scope-neutral, matching §18.1's "whatever the scope". No
  mismatch.
- "a reader's window bound is its own, no smaller than §21.9's guarantee for
  that quantity" — universally quantified over conforming readers, reader-
  relative rather than file-relative. This matches the quantifier of the
  sentence it copies ("a reader instead decodes with a bound of its own
  choosing, no smaller than §21.9's user-metadata guarantee").
- The normative rule being restated for the floor is §21.9 / `[R-ERR-03]`:
  "The table below states **minimum guarantees**, not caps: a conforming reader
  MUST accept any conforming file whose quantities lie within these bounds, and
  a writer MAY rely on that." Quantifier match: `[R-ERR-03]` is over conforming
  readers and conforming files; the repair's floor clause is over readers. OK.
- Neither new clause carries a BCP 14 keyword ("is its own", "is
  ignore-record"). The sentence it is modelled on has the same property, and the
  paragraph is `[R-MTA-09]`, so the force comes from the requirement label.
  Consistent with house style (cf. "Encoding 1 stores the document verbatim.").
  Not flagged.

**Verdict: check 1 passes.**

---

## 3. Check 2 — citations resolve

Every identifier and section number appearing in the repaired text, opened and
read.

| Citation | Where it lives | What the repair needs it to say | Verdict |
|---|---|---|---|
| `` `Window_Size` `` as a §21.9 quantity | 3674: `\| zstd frame `Window_Size` \| 8 MiB \|` | its own table row, with a value | **PASS** — row exists, value 8 MiB, under the column head "A conforming reader MUST accept at least", i.e. a floor on the reader's admissible window, exactly the sense the repair needs |
| §21.9 (as a section) | 3653–3727 | contains the guarantee table | **PASS** |
| R3 (register row) | 3529 | is the row the repair disclaims | **PASS as a pointer**; see §4 for whether the disclaimer is sound |
| `` `[R-MTA-09]` `` | the label of the very paragraph the repair sits in (2486) | authority for "no violation" | **CIRCULAR** — the sentence cites the requirement it is part of. Adds nothing; not itself a defect, but it means the only outward-facing support for "no violation" is `[R-ERR-03]` |
| `` `[R-ERR-03]` `` | 3655–3663 | authority for "no violation" and for the reader's licence to decline | **PARTIAL — see A-03.** `[R-ERR-03]` says only: limits live in this specification; the section is a finding aid; "The table below states **minimum guarantees**, not caps: a conforming reader MUST accept any conforming file whose quantities lie within these bounds, and a writer MAY rely on that." It does **not** say a file exceeding a guarantee remains conforming, and it does **not** license a decline. Both of those are the *next* paragraph, `[R-ERR-04]` (3676–3686): "A file exceeding any of these remains conforming, and a reader MAY decline it — at the whole file, or at the narrowest scope whose declarations exceed what it can serve, a layer or a tile." |

Citations elsewhere in the same paragraph that the repair did not add but that
its placement bears on, also opened: `` `[R-COD-06]` `` (§17.2, 2269–2296),
`` `[R-COD-11]` `` (§17.4, 2396–2413), `` `[R-CNF-10]` `` (§2.5, 273–278),
`` `[R-CNF-11]` `` (§2.3, 190–223), `` `[R-MTA-10]` `` (2545–2566). All resolve
as their host sentences claim. §17.2 confirmed as the home of `[R-COD-06]` by
heading scan (`#### 17.2 Codecs` at 2235, `#### 17.3` at 2357), so the
neighbouring sentence's "The constraints §17.2 states against a tile's declared
decoded size" is correctly addressed.

**Verdict: check 2 fails on one citation — finding A-03.** The document's own
practice is against the repair here, twice:

- §2.3 `[R-CNF-03]` (161–165): "none of whose values exceeds the minimum
  guarantees of §21's limits table (§21.9's `[R-ERR-04]` governs a refusal on
  that last ground; §21.6's closing paragraph names the other two)".
- §18.2's own pre-existing Note (2488–2497), for the *sibling* bound: "a reader
  that instead declines on resource grounds under `[R-ERR-04]` does so at the
  whole file".

Both route an exceeds-the-guarantee refusal to `[R-ERR-04]`. The repair routes
it to `[R-ERR-03]`.

---

## 4. Check 4 — contradiction in the same passage, and the R3 disclaimer

### 4a. The R3 disclaimer itself is sound

R3, verbatim (3529): "A user-metadata document's stored bytes fail to decode
under its declared assigned encoding — under an experimental-range one this
specification defines no decoding and §21.6 governs (`[R-MTA-10]`); encoding 0
and a reserved value are unassigned too and R1 registers both".

§21.1 (3284–3290) frames what a row can be: "each row is one malformed
condition"; the register "enumerates every detectable **file-conformance**
violation this specification names". A condition that obtains for a reader with
an 8 MiB window and not for a reader with a 64 MiB window is not a malformed
condition and not a file-conformance violation. So R3, read against §21.1,
cannot reach a reader-relative decline, and the repair's denial is consistent
with R3's own words *as §21.1 constrains them*.

Note the asymmetry the charter flagged, and it does cut: `Window_Size` is in the
frame header, so the reader learns it **without decoding** and never enters a
decode that could "fail". That is if anything a *stronger* case for the denial
than the decoded-size case, where a streaming reader genuinely begins decoding
and abandons. I looked for a way R3 still catches the case and did not find one.
**No finding here.**

### 4b. §21.5's preamble is the contradiction — finding A-01

The repair's new proposition is "no violation". §21.5's preamble, in normative
prose (not a `>` block), 3510–3516, whitespace-normalised:

> "User metadata is quarantined (`[R-CNT-25]`): every way its document can be
> unreadable takes this outcome, whatever the containing scope — as a violation
> in the rows below, except at an experimental-range encoding, where no document
> rule attaches and §21.6 records the defined non-violation (`[R-MTA-10]`), and
> except **where a reader or verifier declines the decode on the size bound**,
> which `[R-MTA-09]` makes that actor's capability and not a fact about the
> file."

and, four sentences later (3521–3523):

> "Every row here is a violation all the same: the outcome bounds a reader's
> blast radius and never makes the file conforming (`[R-CNF-12]`); §21.6 lists
> the ignore-record conditions that are not violations."

This is a closed three-way classification of *every* way a user-metadata
document can be unreadable: (i) a violation in R1–R10; (ii) the
experimental-encoding non-violation; (iii) a decline **on the size bound**. The
repair manufactures a fourth way — a decline on the **window** bound — and
§21.5's carve-out does not reach it. By §21.5's own words that case falls into
bucket (i), "as a violation in the rows below", while §18.2 says "no violation".

The precedent is decisive against the repair: the size-bound carve-out is
recorded in §21.5 *as well as* in §18.2. Whoever added it swept the register.
This repair did not.

§21.1's tiebreaker does not rescue it. Its words are: "each row *restates* its
governing rule, and where **a row** and the rule it cites diverge, **the rule
governs**." The colliding text is §21.5's **preamble**, not a row, so no stated
tiebreaker applies. §21.1 also makes register completeness normative — "a
*detectable* file-conformance violation this specification names and the
register omits is a defect in this document" — so a reader who follows §21.5's
prose into bucket (i) finds no row and concludes the document is defective,
rather than concluding the case is benign.

I checked whether a row nonetheless convicts, so the classification could be
harmless:

- R4 (3530): "breaks one of the frame constraints §18.2 states **or carries
  over from `[R-COD-06]`**". §18.2's carry-over set is defined at 2458–2460 as
  "the frame constraints of `[R-COD-06]` that do not reference a tile: the
  frame magic; no skippable frame and no second frame; no nonzero dictionary
  ID; no content-checksum flag." `[R-COD-06]`'s window rule is "MUST NOT declare
  a window size exceeding **the tile's decoded size**" — it references a tile,
  so it does not carry over. R4's Instances list confirms: twelve instances,
  none about a window. **R4 does not bite.**
- R3: disposed of in 4a. **Does not bite.**

So no row convicts, which is exactly why §21.5's prose and §18.2's prose fork
rather than merely overlap.

### 4c. The rest of the passage, read for collisions

I read §18.2 whole (2437–2572), §18.1 (2417–2436), §17.2's codec-3 paragraph
(2269–2296) and both of its Notes, §17.4 (2396–2413), §2.3–§2.5 (190–278),
§21.1 (3282–3357), §21.5 (3505–3535), §21.6 (3538–3590), §21.9 (3653–3727),
§22.2–§22.4 (3739–3822), and Appendix H's reader/writer/verifier checklists
(4304–4375). Collisions I looked for and did **not** find:

- §18.2's closing "Any violation here is ignore-record, never the tile-scope
  outcome §17.2 assigns." — not engaged; the repair says it is not a violation.
- §18.1's quarantine "the outcome of every failure to read its **document** is
  ignore-record whatever the scope" — agrees with ignore-record.
- §21.9's exhaustive count "the two capability refusals §21.6 names, a foreign
  format major and an unimplemented MU = 1 type, are not this ground" — I
  checked whether the repair's new use of the word "capability" falsifies the
  count. It does not: §21.6's closing paragraph and §21.9's clause are about
  **conforming files a reader refuses at file scope**, and the repair's case is
  an ignored record in a file the reader otherwise reads fully.
- §2.3 `[R-CNF-11]`'s cannot-establish list already contains, unqualified, "when
  it declines to decode a user-metadata document (`[R-MTA-09]`)" — this covers
  the window decline as well as the size decline, and is what keeps A-02 below
  from forking a verdict.
- §22.2 `[R-SEC-02]`: "A reader MUST NOT size an allocation, fetch, or index
  walk in proportion to a declared magnitude it has not corroborated against the
  file's actual length." I considered whether this constrains `Window_Size` and
  concluded it does not — it binds the reader's allocation, not the frame's
  declared value, so it does not falsify "unconstrained".
- §21.9's hard-limits paragraph `[R-ERR-05]` (3704–3727): I read the whole
  enumeration of hard limits. `Window_Size` is not among them. Confirms
  "unconstrained".
- Appendix G/H (4290–4375) and the quick-reference row at 4071 ("8 MiB zstd
  window"): nothing restates the metadata window rule, so nothing there is now
  stale.

### 4d. A sentence written to be true only under the old wording — finding A-05

§18.2's Note, immediately after the repaired paragraph (2488–2497), non-normative:

> "**Note.** The 16 MiB figure is a §21.9 minimum guarantee, so the two rules
> compose here as they do elsewhere. ... A reader that proceeds takes
> ignore-record for that record; a reader that instead declines on resource
> grounds under `[R-ERR-04]` does so at the whole file, **a document having no
> declared size and so no narrower scope whose declarations that rule can
> measure**. A refusal on that ground is reported as a resource limit, not as
> corruption."

This Note is the only text in the document that resolves how `[R-ERR-04]`
composes with a user-metadata document, and its whole inference rests on the
premise that the passage contains **no declaration** for `[R-ERR-04]`'s
"narrowest scope whose declarations exceed what it can serve" to measure. The
repair drops into the same passage a quantity that is *declared in the frame
header* and that §21.9 lists as its own guaranteed row. The premise no longer
holds for the window ground.

Consequence, for a layer sub-record's document: `[R-ERR-04]` now has a
declaration to measure and offers "a layer or a tile" as narrower scopes, which
would give reject-layer — colliding with §18.1's quarantine ("ignore-record
whatever the scope") and with the repair's own "is ignore-record". For a
top-level document, `[R-ERR-04]`'s enumerated narrower scopes ("a layer or a
tile") do not include a record, so the resource-decline route has no scope to
land on at all. Neither the repair nor the Note says which route governs, and
the Note's stated reason for preferring the whole file is now false for the new
quantity.

This is a `>` block, so it is non-normative and cannot itself be the rule. That
is why I rate it a real but non-byte-level defect: the repair introduced a
declared quantity into a passage whose only `[R-ERR-04]` composition rule was
argued from the absence of declarations, and left the composition unstated.

---

## 5. Check 3, second half — did the repair leave an old statement standing?

Distinctive terms greped across the whole file, whitespace-normalised where a
wrap was possible:

- `Window_Size` / `window size` / `window bound` / `window log` (line grep;
  these tokens cannot wrap): hits at 2285, 2293, 2298, 2300, 2313, **2466,
  2468** (the repair), 3498 (T21), 3674 (§21.9 row). Every hit outside the
  repair is tile-scoped or the §21.9 row. No stale document-scoped window rule
  is left standing. **Passes.**
- `on the size bound` (normalised phrase search): one hit, §21.5's preamble.
  That is the restatement the repair should have swept — finding A-01, above.
- `bound of its own` / `its own choosing` / `user-metadata guarantee`
  (normalised): one hit each, all inside the §18.2 sentence the repair is
  modelled on. No second home for the reader-bound rule elsewhere. **Passes.**
- `declines to decode a user` (normalised): one hit, §2.3 `[R-CNF-11]`, phrased
  generally enough to cover both bounds. **Passes** (and see A-02).
- `8 MiB` (line grep): 2293, 3674, 3700, 4071. 3700 is §21.9's rationale Note
  ("8 MiB is the decoder window support RFC 8878 itself recommends"); 4071 is
  Appendix's quick-reference row. Neither is falsified.

So the repair **landed** in normative text and left no contradicting normative
window rule for documents. Its failure is the omitted sweep of §21.5.

---

## 6. Check 5 — exhaustive claims in the repaired text

Word by word:

| Claim | Falsification attempt | Result |
|---|---|---|
| "unconstrained **here**" | `[R-COD-06]`'s MUST NOT (tile-relative — does not reach a document); `[R-COD-06]`'s SHOULD (also tile-relative, "even for a larger tile"); §18.2's own enumerated carry-over set (window not in it); R4's twelve instances (no window instance); T21 (tile use); §21.9's guarantee table (a floor, not a cap); §21.9's hard-limits list `[R-ERR-05]` (window absent); §22.2 `[R-SEC-02]` (binds the reader, not the value); §21.9's `[R-ERR-04]` (declines, does not invalidate) | **Survives.** No rule binds the value. But see A-04: it survives *too* completely |
| "for the same reason" | The prior sentence's reason is "because a document has no declared size". `[R-COD-06]`'s window rule is relative to "the tile's decoded size", so the absence of a declared decoded size does disable it | **Survives** |
| "takes the same treatment" | The treatment of the *sibling* bound (§18.2) is: reader's own bound, floor at §21.9, ignore-record above it. Imported faithfully. The treatment of the *same quantity for a tile* (`[R-COD-06]`) has a third component the repair does not import — the writer SHOULD | **A-04** |
| "no smaller than §21.9's guarantee for that quantity" | Row exists, own row, value 8 MiB, and the column heading gives it the right direction | **Survives** |
| "not a failure to decode within the meaning of R3" | R3's words + §21.1's framing of a row as a file-conformance condition | **Survives** (§4a) |
| "no violation" | §21.5's preamble classification | **A-01** |
| "the reader's capability" | §21.9's "the two capability refusals §21.6 names" — checked; different subject (file-scope refusals), so no count is broken | **Survives** |

### A-04, stated

`[R-COD-06]` treats an oversized declared window in three moves:

> "Writers SHOULD keep the declared window within §21.9's 8 MiB `Window_Size`
> guarantee even for a larger tile; a wider window is conforming and merely
> permits a conforming reader to decline the tile or the layer on resource
> grounds (`[R-ERR-04]`)."

(i) a writer SHOULD; (ii) wider is conforming; (iii) a reader may decline. The
repair imports (ii) and (iii) and drops (i). Because §18.2 carries over only the
`[R-COD-06]` constraints "that do not reference a tile" and the SHOULD says
"even for a larger tile", the SHOULD does **not** reach documents, so §18.2 now
gives a writer no guidance at all. A writer may emit a 500-byte JSON document in
a frame declaring a 2 GiB window; every reader whose bound is the guaranteed
8 MiB will ignore that record; the file stays conforming and the verifier cannot
certify it. §21.5 opens by deprecating precisely this: "Readers SHOULD report
the loss; silent metadata loss defeats the record's purpose."

Not byte-level (a SHOULD deviation is not a violation, `[R-CNF-12]`), but the
repair's own phrase "takes the same treatment" is what makes the omission a
defect rather than a choice.

---

## 7. New ambiguity — finding A-02

The repair is inserted **between** the decoded-size bound sentence and the
verifier sentences, which then read:

> "A **verifier** that declines to decode a document on **the bound above**
> cannot establish that document's conformance and MUST NOT certify the file …
> the verifier SHOULD report **the bound** it applied and the stored length of
> the extent it declined. **The decline** presupposes an encoding this
> specification assigns …"

Before the repair, "the bound above" had exactly one antecedent. It now has two,
and the nearest is the window bound. Three readings, all defensible:

1. the size bound only → the window decline gets no verifier rule;
2. the window bound only (nearest antecedent) → the size decline loses the rule
   the sentence was written for;
3. either bound above → both preserved.

Only (3) is coherent, and the singular definite "the bound" does not say it.
Same for "the bound it applied" and "The decline".

I judged this **not** byte-level, because §2.3 `[R-CNF-11]` states the
cannot-establish ground without qualification — "when it declines to decode a
user-metadata document (`[R-MTA-09]`)" — so a verifier cannot certify on either
reading. The residue is a report obligation stated as a SHOULD and a genuinely
ambiguous antecedent. Fix is a two-word edit: "on either bound above".

(Also noted, not separately reported: "more than the reader **admits**"
introduces a new verb for a relation the document elsewhere calls *accept*
(§21.9's column head, `[R-CNF-03]`). Cosmetic; folded into A-02's repair.)

---

## 8. Byte-level test, per finding

- **A-01.** Verifier V1 follows §18.2 `[R-MTA-09]` and certifies (or reports
  cannot-establish) a file whose top-level metadata frame declares
  `Window_Size` = 64 MiB. Verifier V2 follows §21.5's preamble, which places
  that case in "a violation in the rows below", and reports *nonconforming*.
  §21.1's row-vs-rule tiebreaker does not reach preamble prose, so nothing in
  the document settles it. On the writer side, `[R-CNF-05]` ("A writer MUST emit
  only conforming files") bars the emission under V2's reading and permits it
  under V1's. Applying the charter's discriminator: no register row actually
  states the condition (R3 and R4 both checked and both fail to reach it), so
  the file does **not** carry a row violation, and `[R-CNF-05]` does not bar it
  under both readings — the emittable set moves. **Byte-level: yes.** The
  disputed byte is the `Window_Descriptor` byte of the encoding-2 frame in a
  user-metadata extent.
- **A-02.** Resolved by §2.3 for the verdict that matters; residue is a SHOULD
  and an antecedent. **Byte-level: no.**
- **A-03.** Both `[R-ERR-03]` and `[R-ERR-04]` land the reader in the same
  place; the mis-citation misdirects a reader looking for authority rather than
  changing an outcome. **Byte-level: no.**
- **A-04.** SHOULD-level; `[R-CNF-12]` makes a SHOULD deviation not a violation,
  so the conforming set is identical either way. **Byte-level: no.**
- **A-05.** The colliding text is a `>` block and therefore non-normative
  (`[R-CNF-01]`); what is missing is a statement, not a conflicting rule.
  **Byte-level: no.**

---

## 9. Summary of the five checks

1. Tense and quantifier — **pass**, no finding.
2. Citations resolve — **fail**, A-03 (`[R-ERR-03]` cited for `[R-ERR-04]`'s
   propositions; `[R-MTA-09]` self-cited).
3. Repair sits in normative text — **pass** (plain prose in §18.2, no `>`), and
   no stale normative window rule for documents survives elsewhere.
4. No contradiction in the same passage — **fail**, A-01 (§21.5's preamble) and
   A-05 (§18.2's Note reasoning).
5. No exhaustive claim it cannot carry — **pass on every literal claim**, but
   the asserted analogy "takes the same treatment" is incomplete: A-04.
