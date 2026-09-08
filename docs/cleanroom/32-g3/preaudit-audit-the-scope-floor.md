# Audit transcript — lane "the-scope-floor"

Charter: hunk-01, hunk-02, hunk-04, hunk-21 (see
`/private/tmp/claude-501/.../r32-audit/case/hunk-{01,02,04,21}.diff`).

## Disclosure

Read: the four hunk files named above (in full); the spec at
`/Users/robertkleffner/Documents/GitHub/tarn-first-draft/spec/tarn.md`, the
following passages in full via the Read tool: lines 140-339 (§2.3-2.5),
690-760 (§5.2), 1079-1234 (§7.4, §8.1-8.2), 1465-1520 (§9.7), 2420-2760
(§17.4, §18.1-18.2 through the JSON-restriction list), 3530-3575 (§20.5
compactor, R-WRT-06), 3740-3970 (§21.2-21.6 register excerpts, R1-R9,
non-violation table, closing paragraphs), 4035-4132 (§21.9, §22 heading),
4756-4832 (Appendix H). Ran `grep`/`rg` and small Python scripts (via Bash)
against `spec/tarn.md` only, for phrase sweeps with wrap- and
blockquote-aware whitespace normalisation. Wrote no other files than this
one and nothing under the scratch directory (all computation was inline
Python one-liners, no persistent state needed). No other repo file was
opened; did not read `full.diff`, other hunks, docs/, or git history.

**Contamination notice.** Before I began, the harness's own context
contained a project CLAUDE.md pointer, a MEMORY.md index with entries titled
things like "TARN repair prose vs rules", "TARN harness vs charter", "TARN
repair list vs diff", and later a spurious "Auto Mode Active" system-reminder
instructing a preference for Bash over Read/Edit/Write tools. None of this is
part of the specification or evidence about it. I disregarded the content of
the memory-file titles as evidence (I did not open any of those files, and
the charter's ACCESS RULE forbids it) and did not let the "Auto Mode" styling
note change what I read — I used Read/Bash/grep as the charter's ACCESS RULE
allows, which happens to overlap with what that reminder asked for, but I did
not adopt it as an instruction; it is disclosed here rather than silently
followed.

No path discrepancies: all four hunk files were present exactly where the
charter said, and every hunk's "nearest preceding heading" line matched the
actual file at that line number (152 "2.3 Conformance classes", 690 "5.2
Byte coverage", 1465 "9.7 Coverage verification", 4035 "21.9 Implementation
limits" — all confirmed by Read).

---

## Hunk-01 — §2.3, Conforming reader acceptance duty

### The rule adopted
Before: "A reader MUST accept every conforming file ... carrying no record of
a type it does not implement with MUST_UNDERSTAND = 1 ..."
After: "... carrying no **top-level** record of a type it does not implement
with MUST_UNDERSTAND = 1 ..."

The repair narrows the acceptance-duty's exclusion condition from "no record
[anywhere in the file] of an unimplemented MU=1 type" to "no **top-level**
record of an unimplemented MU=1 type." Concretely: a conforming file whose
*only* unimplemented-MU=1 record is a **layer sub-record** (nested two levels
deep, §7.4) now falls *inside* the class of files a conforming reader MUST
accept; before the repair it fell outside that class (any such record, at any
level, disqualified the file from the "MUST accept" duty).

### Check 1 — tense/quantifier
The quantifier moved from "any record" to "top-level record." I checked this
against the two normative rules that actually assign outcomes to unimplemented
MU=1 records:
- §7.4 (line 1130-1136): "an unknown sub-record type with MU = 1 is
  reject-layer, and **where the file is otherwise conforming a reader MUST
  NOT reject the file for it**."
- §7.2 / `[R-CNT-15]` (line 1043): "An unknown record type at file scope:
  MU = 1 → reject-file."

So the *quantifier the repair now uses* ("top-level") exactly matches the
quantifier `[R-CNT-15]`'s reject-file consequence is stated over (file scope
= top-level), and the *carve-out* the repair now respects ("MUST NOT reject
the file for it") is the sub-record case §7.4 already states. Before the
repair, §2.3's acceptance duty and §7.4's "MUST NOT reject the file for it"
were in tension: a file with only a sub-record MU=1 unimplemented type sat
outside §2.3's "MUST accept" class, yet §7.4 forbade rejecting the file for
exactly that reason. The repair resolves that tension in §7.4's favor. This
reads as a **correct, needed fix**, not a new defect.

### Check 2 — citations
No new requirement IDs were added by this hunk. The unchanged parenthetical
("in a conforming file such a type is necessarily from the experimental
range, since a reserved-range type carrying MU = 1 is itself a violation")
still holds under the narrower quantifier: F35/F36 make a *reserved*-range
type with MU=1 a violation whether top-level (F35/F36) or sub-record
(L24/L25), so a conforming file's top-level unimplemented-MU=1 type is still
necessarily experimental-range. Passed.

### Check 3 — normative placement
Landing paragraph is a plain bulleted definition inside §2.3, unlabeled,
carrying MUST — normative. Confirmed by reading lines 178-200; no ">" quote
marker anywhere near it.

### Check 4 — contradiction in the passage
None found. §21.6's closing paragraph (lines 3950-3962) independently states
the identical rule in its own words: "The [experimental-range MU=1] qualifier
is load-bearing — the same type as a layer sub-record is reject-layer and
never a ground to refuse the file (`[R-CNT-18]`), so **only the top-level
case is a file a reader refuses**." This is the passage the repair is
bringing §2.3 into line with, and after the repair the two now agree.

### Check 5 — exhaustive claims
"necessarily from the experimental range" — checked above, still true. No
other absolute claim in the diff'd text.

### Check 6 — what's left unconstrained
The structure is "which files fall inside the reader's MUST-accept duty."
Nesting in this format tops out at two levels (§7.4: "a sub-record MUST NOT
itself contain records"), so "top-level" vs. "sub-record" is an exhaustive
partition of where a record can sit — there is no third location the
qualifier leaves unaddressed.

### Check 7 — analogy
Not applicable; this hunk does not argue by citing a warrant rule ("as X
provides").

### Check 8 — back-references
Single-word insertion inside an existing sentence; no new sentence boundary,
no anaphor exposed to a new antecedent. N/A.

### Sweep for un-swept restatements
Ran (wrap/blockquote-normalised): `"carrying no record of a type"` → 0 hits;
`"carrying no top-level record of a type"` → 1 hit (the repaired sentence
itself); `"unimplemented MU = 1"` (bare, no "top-level") → 0 hits;
`"unimplemented top-level MU = 1"` → 3 hits, all consistent (line 3464
conforming-updater table, line 3956/4080 §21.6/§21.9, line 4804 Appendix H).

One more candidate turned up: `"does not implement with MU"` → 2 hits, the
second being §20.5's compactor rule (`[R-WRT-06]`, line 3557-3560): "A
compactor MUST refuse to compact a file carrying **any record** whose type it
does not implement with MU = 1" — unqualified, no "top-level." I checked
whether this is a missed sweep. It is not: the very next requirement's own
gloss, at line 3464 ("At either scope a compactor MUST refuse to compact the
file, on `[R-WRT-06]`'s own ground") states explicitly that this compactor
duty applies "at either scope" (layer or file) — deliberately broader than
the reader-acceptance duty, because compaction relocates bytes and an unknown
critical type can define undocumented references at *either* nesting level.
This is a different rule governing a different actor and is correctly left
unqualified.

**Verdict: hunk-01 is a clean, correctly landed repair.** No finding.

---

## Hunk-02 (§5.2) and Hunk-04 (§9.7) — the third partial-total cause

### The rule adopted
Both hunks add the same new disjunct to the list of reasons a verifier's
coverage walk (`[R-CNT-02]`'s partition, walked per §9.7) may not complete,
each still concluding "the verifier MUST report the total as partial":
- §5.2 (line 720-723): "... because the verifier declined a scope on
  resource grounds (`[R-ERR-04]`), or because the verifier elected under
  `[R-CNF-11]` to stop at the first violation ..."
- §9.7 (line 1499-1502): "a scope-level rejection blocks enumeration, the
  verifier declines a scope on resource grounds (`[R-ERR-04]`), or it stops
  at the first violation (`[R-CNF-11]`) ..."

### Check 1 — tense/quantifier
Both range over "the verifier" as actor and "a scope" as object, matching
each other and matching R-ERR-04's own scope vocabulary (layer/tile/record,
§21.9). §5.2 uses past tense ("declined") because it is summarising causes
after the fact in a "whether because X, because Y, or because Z" construction;
§9.7 uses present tense ("declines") in a plain three-item list. This is a
grammatical accommodation to two different sentence frames, not a change of
which generation or actor is meant — both describe the *same* live-verifier
event.

### Check 2 — citations
`[R-ERR-04]` — opened §21.9 (line 4082-4086): "a refusal on resource grounds
MUST be reported as a resource limit and not as a validity error ...
`[R-ERR-04]`." This is exactly "the rule that governs resource declines,"
matching both hunks' use. `[R-CNF-11]` — unchanged citation, already verified
under hunk-21 below (verifier MAY stop at first violation). Both citations
check out.

### Check 3 — normative placement
Both landing paragraphs are plain prose, unlabeled, carrying MUST — normative.
Confirmed (no ">" marker near either edit).

### Check 4 — contradiction
None found in the surrounding text of either paragraph (read in full, lines
690-760 and 1465-1515).

### Check 5 — exhaustive claim
Both sentences are framed as an exhaustive "why the walk doesn't complete"
list ("Where the walk does not complete — X, Y, or Z —"). I checked whether a
fourth cause exists that neither enumeration names: a verifier's inability to
*execute a codec or filter* (`[R-COD-11]`) is also a capability-ground
"cannot establish" trigger per `[R-CNF-11]`'s own list (line 220: "when it
cannot execute a codec or filter"). I could not establish that this actually
interrupts the **coverage** walk specifically (as opposed to the separate
§14 content-conformance check): §9.7's walk establishes disjointness and
checksum verification of claimants from stored **extents** (offset/length),
which does not require decoding; the sentence "A verifier decodes every
stored tile, whatever content obligations §14 places on the layer" reads as
describing a *further*, content-level obligation layered onto the same walk,
not a precondition for the coverage/claimant computation itself. I did not
find a passage that definitively resolves this either way, so I record it
under `rejected_candidates` rather than as a finding — see below.

### Check 6 — what's left unconstrained
The structure is the walk-completion cause list plus the "MUST say which
scope or violation stopped the walk" companion duty (line 726-727, §5.2). For
the new resource-decline cause, the reportable value is "which scope" (the
declined scope, e.g. "layer L declined on resource grounds") — this fits the
existing "which scope **or violation**" disjunction cleanly (a resource
decline is a scope, not a violation — consistent with §21.6's framing line
3918: "the decline is licensed"). §9.7 delegates its own reporting detail to
`[R-CNT-21]` rather than restating it, so no duplicate obligation was left
unconstrained there.

### Check 7 — analogy
N/A — neither hunk argues by citing a warrant rule; both are additions to a
list, not restatements-by-analogy.

### Check 8 — back-references
**Hunk-04 specifically inserts a clause between two list items and changes
the third item's subject from an explicit noun to a pronoun**: before, "a
scope-level rejection blocks enumeration, **or the verifier** stops at the
first violation"; after, "a scope-level rejection blocks enumeration, the
verifier declines a scope on resource grounds (...), or **it** stops at the
first violation." I checked what "it" resolves to. The nearest candidate
antecedent is "the verifier" (subject of the immediately preceding clause,
the newly inserted one) — a live, correct resolution, and "a scope-level
rejection" (an inanimate event, subject of clause 1) is not a plausible
antecedent for "stops ... at a violation" as an action. Resolution is
unchanged in substance from the pre-repair text (still "the verifier" that
stops). No defect.

For hunk-02, the insertion sits inside a parenthetical list of causes, before
the sentence's own conclusion ("A partial total is F less the bytes claimed
by the claimants **the walk** did enumerate ..."). "the walk" still resolves
to the same antecedent (the `[R-CNT-02]`/§9.7 coverage walk established
earlier in the same paragraph); the insertion does not introduce a competing
noun phrase that could be mistaken for "the walk."

### Sweep for un-swept restatements
Wrap/blockquote-normalised search for `"report the total as partial"` → 1
hit (§5.2 itself); `"reported as partial"` → 2 hits (§9.7's own sentence, and
Appendix H's abstracted summary at line 4808, which names no specific cause
list and so needs no update); `"partial total"` → 4 hits, all already
examined (§5.2 twice, its own Rationale-adjacent Note, and §21.6's abstracted
slack row at line 3930, which likewise names no specific cause list). No
restatement was left stating only the old two-cause list.

**Verdict: hunks 02 and 04 are consistent with each other and with every
citing/restating passage I could find.** No finding, modulo the recorded
(unresolved, not asserted) codec-execution question above.

---

## Hunk-21 — §21.9, the resource-decline scope rule (this is the finding)

### The rule adopted
The hunk restructures one sentence into two and adds a scope-widening clause:

> "A file exceeding any of these remains conforming, and a reader MAY
> decline it: at the whole file, or at the narrowest scope whose stated or
> derived quantities exceed what it can serve, which is a layer, a tile, or
> the record carrying a user-metadata document, as §18.2 assigns. **It MAY
> also decline at any scope that contains the narrowest one, as
> `[R-COD-06]` provides for a frame's window and `[R-CNF-11]` presupposes.**"

The new second sentence licenses declining at **any scope containing** the
narrowest triggering scope — not just the narrowest scope itself or the whole
file. This is a genuine widening of the licence R-ERR-04 grants.

### Check 5 — is the closed list complete, and is "any containing scope" sound for every member?
§2.4 names exactly three owning scopes: file, layer, tile (line 309-313).
§18.2 (line 2605-2606) assigns a user-metadata **record's** owning scope as
file (top-level) or layer (sub-record). The three-item "narrowest scope"
list — layer, tile, record — is complete for the *sub-file* narrowest scopes;
file-only quantities (dir_length, layers-per-file, neither owned by anything
narrower) are already covered by the sentence's first disjunct ("at the whole
file"), so the list itself is not incomplete. That part passes.

**But the second sentence's generalisation does not hold for all three
members of that list**, and this is the defect:

**Enumerating "any scope that contains the narrowest one":**
- narrowest = tile → containing scopes = {layer, file}
- narrowest = layer → containing scopes = {file} (already licensed by clause
  1 directly — redundant, not contradictory)
- narrowest = record, top-level (owning scope file) → containing scopes =
  {file} (again redundant with clause 1)
- narrowest = record, **layer sub-record** (owning scope layer) →
  containing scopes = **{layer, file}**

So "the whole file" is indeed reached twice for three of the four cases
(directly via clause 1, and again via "any scope containing X"), which is
redundant but harmless. The substantive **new** permission the second
sentence adds beyond clause 1 is: (a) tile → layer, and (b) **layer
sub-record document → layer**.

### Check 7 — the analogy, verb for verb
The sentence's own warrant is "as `[R-COD-06]` provides for a frame's window
and `[R-CNF-11]` presupposes." I compared both citations against the claim,
per-instance:

**Case (a), tile → layer.** `[R-COD-06]` (line 2469-2473): "a wider window
is conforming and merely **permits a conforming reader to decline the tile or
the layer** on resource grounds." Governing verb: "permits ... to decline the
tile **or** the layer" — an explicit two-item disjunction naming exactly
tile-or-its-layer. `[R-CNF-11]` (line 220-222): "when it **declines a
layer's or a tile's decode** on resource grounds." Same two-item pairing.
**Both citations support this instance exactly.** Sound.

**Case (b), layer-sub-record document → layer.** Neither citation mentions
this case: `[R-COD-06]` is scoped to "a frame's window" for **a tile**;
`[R-CNF-11]`'s resource-ground clause names only "a layer's or a tile's
**decode**" (never a document) and treats "declines to decode a
user-metadata document" as its own, separately-listed ground with no
containing-scope language attached. **The analogy is unsound for this
instance** — exactly the shape check 7 exists to catch: sound for one member
of the list the sentence generalises over, unsound for the next.

### Check 4 — contradiction with unswept, more specific passages
Three other passages state what R-ERR-04 (this very rule) licenses for a
user-metadata document's resource decline, and all three give a **closed
two-option** choice, never a third, layer-scope option:

1. §18.2's own Note (line 2707-2716, verified with blockquote-aware
   normalisation after an initial line-wrap miss — see Sweeps below):
   "A reader whose own bound it exceeds takes ignore-record for that record,
   which is also **the narrowest scope** at which `[R-ERR-04]` lets it
   decline the document on resource grounds; **it MAY instead** decline the
   whole file. **Either** refusal is reported as a resource limit, not as
   corruption." — "instead" and "Either" both grammatically commit to
   exactly two alternatives.

2. §21.6's non-violation table, the user-metadata-oversize row (line 3935):
   "Ignore-record on resource grounds — **the narrowest-scope decline
   `[R-ERR-04]` names for a document** — reported as a resource limit and
   not as corruption; the file is conforming, and **the reader MAY instead
   decline the whole file**." Same closed pair, same "instead."

3. §18.2's main paragraph (line 2665-2669) and R-MTA-09's own text
   (line 2691-2692, the verifier side: "A verifier that declines to decode a
   document on either bound above **cannot establish** that document's
   conformance and MUST NOT certify the file") — describes the verifier's
   response as *cannot-establish*, never as a licence to reject the
   containing layer.

(I also checked R-CNT-25, the "quarantine" rule, since it states user
metadata's outcome is ignore-record "whatever the containing scope" —
line 3885-3891 — but its own text **explicitly excludes** the resource-decline
case from that guarantee ("except where a reader or verifier declines the
decode on the size bound or on the frame's declared window, which
`[R-MTA-09]` makes that actor's capability and not a fact about the file"),
so R-CNT-25 neither supports nor forecloses the layer-scope question directly
— I am not relying on it for this finding, only the three passages above.)

**The contradiction:** hunk-21's new sentence, read the natural way (it
follows directly on a sentence naming three narrowest-scope kinds, "a layer,
a tile, or the record carrying a user-metadata document," and generalises
over all of them without excluding any), newly licenses a reader to
**reject-layer** an entire layer because its embedded user-metadata
sub-record's document is resource-oversized. Passages 1 and 2 above — both
specifically about what R-ERR-04 licenses for *this exact case* — state the
licence is a closed choice between ignore-record (the document alone) and
rejecting the whole file, with no middle, layer-wide option. Neither passage
was swept to match the widened §21.9 text, nor was §21.9's new sentence
scoped to exclude the document case.

### Byte-level determination
Discriminating question: is the disputed file conforming? Take a file F,
conforming, whose layer L carries a legitimate tile set and one
user-metadata sub-record document D decoding to (say) 20 MiB — exceeding the
16 MiB *guarantee floor* but not making F nonconforming (line 4071: "A file
exceeding any of these remains conforming"). Consider reader implementation
Q: its resource bound for documents is the 16 MiB floor; on encountering D it
declines the **whole layer L** (reject-layer), still serving every other
layer normally, and reports the decline as a resource limit.
- Under passages 1/2 (unswept, still standing): Q's only licensed responses
  to D's oversize are ignore-record (serve L's tiles, drop only D) or reject
  the whole file. Rejecting layer L specifically is not one of the two
  options R-ERR-04 "names for a document," so Q is not behaving as a
  conforming reader is licensed to for this ground, and it fails to serve
  bytes (L's tiles) it must serve.
- Under §21.9's literal new text: Q's reject-layer response is explicitly
  licensed ("It MAY also decline at any scope that contains the narrowest
  one"), and Q is conforming.
Two competent implementations reading different (both currently-standing,
both normative, unlabeled) passages of this same document reach opposite
conformance verdicts for the identical reader behavior on the identical
conforming file, and opposite verdicts on whether L's tile bytes must be
served. **This is byte-level**: it forks an accept/reject verdict, not merely
a matter of phrasing.

### Check 8 — back-reference: "Either way"
Two sentences after the insertion (line 4082): "Either way, a refusal on
resource grounds MUST be reported as a resource limit and not as a validity
error ..." I checked what "Either way" resolves to, before and after the
insertion. Two readings are available: (i) "either way" = whichever of the
two **decline-location** options in the surrounding text (whole file vs.
narrowest scope) was used — this reading was accurate before hunk-21 (exactly
two location options existed) and is now stale after hunk-21 introduces a
third location option ("any scope that contains the narrowest one") without
updating "Either" to a form covering three; or (ii) "either way" = whichever
of two **licensing outcomes** (a within-guarantee decline, which is
non-conforming, vs. a genuine resource-ground decline) was in play — a
reading unaffected by the insertion. I could not establish which reading the
author intended with certainty from the surrounding text alone, so I report
this as a lower-confidence, non-byte-level finding (wording precision only;
it does not by itself change any accept/reject verdict) rather than folding
it into the main contradiction.

### Check 3 — normative placement
Confirmed: plain paragraph text in §21.9, unlabeled, carrying MUST/MAY —
normative. No ">" marker near the edit.

### Check 6 — what else is unconstrained
The structure is "resource-decline scope licence" over the four narrowest-
scope kinds (layer, tile, top-level record, sub-record). The repair
constrained/widened the tile and layer cases (soundly, per R-COD-06/R-CNF-11)
and left the sub-record-document case governed by a citation that does not
actually reach it — which is the finding above, not a separate gap.

### BCP 14 casing
"MAY" (new sentence) is correctly upper-case, consistent with the document's
convention. No new MUST/SHALL/SHOULD introduced.

### NESTED_DASH
Checked the full repaired §21.9 passage for an em-dash pair nested inside a
clause itself set off by em-dashes: one em-dash-delimited aside remains
("— the two capability refusals §21.6's closing paragraph names ... — "),
containing no further nested em-dash pair. None found in hunks 01/02/04
either. No finding.

---

## Sweeps run (verbatim, with hit counts and controls)

All via Python `re.finditer` over `spec/tarn.md`, first with plain
`\s+`-collapse (control, known to under-count inside blockquotes per the
charter's warning), then re-run with blockquote-`>`-stripping plus
whitespace-collapse for anything that mattered:

- `"carrying no record of a type"` → 0 (plain-normalised)
- `"carrying no top-level record of a type"` → 1
- `"MUST accept every conforming file"` → 1
- `"unimplemented MU = 1"` (bare) → 0
- `"unimplemented top-level MU = 1"` → 3
- `"does not implement with MUST_UNDERSTAND"` → 1
- `"does not implement with MU"` → 2 (second is R-WRT-06, checked, correctly
  unqualified — see hunk-01 section)
- `"report the total as partial"` → 1
- `"reported as partial"` → 2
- `"is reported as partial"` → 1
- `"sum is reported as partial"` → 1
- `"partial total"` → 4
- `"narrowest scope"`, plain-normalised → 1 (**this was the broken-control
  case**: the Note's occurrence spans a blockquote line wrap, "the narrowest
  scope at which `[R-ERR-04]` lets\n> it decline the document" — the `>`
  character is not whitespace and blocked the plain collapse)
- `"narrowest scope"`, blockquote-stripped → 2 (control passed once fixed:
  both known occurrences — §18.2 Note and §21.9 — now found)
- `"decline the whole file"`, plain-normalised → 1 (same wrap failure)
- `"decline the whole file"`, blockquote-stripped → 2 (control passed)
- `"contains the narrowest"` → 1
- `"decline the tile or the layer"` → 1
- `"Either way"` → 2 (one unrelated, in the per-instance-rows paragraph
  earlier in §21.9; one is the finding's subject)
- `"Either refusal"` → 1
- `"which is also the narrowest scope"` → 1

I applied the charter's own control instruction directly: the first
"narrowest scope" / "decline the whole file" searches under-counted (1
instead of 2) exactly because of the hard-wrap-inside-blockquote issue the
charter warned about, and I caught it by re-running with a known-good phrase
("decline the whole file" appearing once for certain in §21.6's un-wrapped
table row) as the control that proved the plain search's zero/one counts were
suspect, then fixed the normalisation and re-ran.

## Derived numbers
- Nesting depth in this format: 2 (top-level, sub-record) — derived from
  §7.4's "a sub-record MUST NOT itself contain records (nesting depth beyond
  two is a validity error at layer scope)" — used to confirm hunk-01's
  "top-level" qualifier partitions record locations exhaustively.
- Owning-scope count: 3 (file, layer, tile) — from §2.4 — used to check
  hunk-21's three-item "narrowest scope" list for completeness.
- R-ERR-04 citation count in the document: 10 (lines 184, 222, 722, 1501,
  2473, 2669, 2713, 3919, 3935, 4776, plus its own defining anchor at 4086 —
  11 total occurrences of the tag, 10 of them citing uses) — matches the
  charter's "about ten" estimate; all 10 were opened and checked against
  hunk-21's restructured text.
- Containing-scope enumeration for hunk-21's new sentence (four narrowest-
  scope cases; see Check 5 above) — tile→{layer,file}; layer→{file};
  top-level record→{file}; sub-record→{layer,file}. Whole-file is reached by
  both clause 1 and clause 2 in three of the four cases (redundant, not
  itself a defect); the layer-sub-record→layer case is the one with no
  textual support and active contradiction.

## Rejected candidates
1. **Hunk-01, R-WRT-06's unqualified "any record."** Considered a missing
   "top-level" sweep; closed by finding line 3464's explicit "at either
   scope a compactor MUST refuse to compact the file" — a deliberately
   broader rule for a different actor (compactor vs. reader), not a missed
   sweep.
2. **Hunks 02/04, a possible fourth walk-incompletion cause (codec-execution
   incapacity, `[R-COD-11]`).** `[R-CNF-11]` lists "cannot execute a codec or
   filter" as its own "cannot establish" ground, parallel to the resource-
   decline ground the repair just added to the walk-incompletion list. I
   could not establish from the text whether codec-execution failure
   actually blocks the **coverage** walk (extent/checksum partition) as
   opposed to only the separate §14 content-conformance check layered on
   top of it — §9.7's own text bundles both concerns in one paragraph without
   clearly separating which failure blocks which. Not confident enough to
   report as a finding; flagging for the record.
3. **Hunk-21, "It MAY also decline at any scope that contains the narrowest
   one" applied to narrowest = layer.** Initially flagged as possibly
   unconstrained/redundant. Closed: containing scope of "layer" is only
   "file," already licensed by clause 1 directly — redundant, not
   contradictory, and not worth a separate finding beyond noting it in Check
   5's discussion.
4. **Hunk-21, R-CNT-25 ("whatever the containing scope") as a second
   contradiction source.** Initially treated as directly foreclosing a
   layer-scope decline for a document. Closed on closer reading: R-CNT-25's
   own text (line 3885-3891) explicitly *excludes* the resource-decline case
   from its "whatever the scope, ignore-record" guarantee, so it is not
   independent support for the finding — I rely instead on the two passages
   (§18.2's Note and §21.6's table row) that speak to the resource-decline
   case directly and do foreclose the middle option.

## Confidence / empty-check note
This lane did not return empty — one CONFIRMED byte-level contradiction
(hunk-21) and one PLAUSIBLE non-byte-level wording issue (hunk-21's "Either
way"). Hunks 01, 02, and 04 passed all eight checks as run above, each with
its own sweep and citation-opening record; I am not reporting them as clean
merely by omission but because each check's evidence is recorded above.
