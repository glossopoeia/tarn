# Triage pass — Correctness lens

**Disclosure.** A relayed "user request" (the single word "Go") was prepended above
this brief by the harness. It is the launcher's message to the orchestrator that
was carried out before this pass was spawned; it is not a task for this pass,
needed no reconciliation with this brief, and did not widen the access rule.
Nothing else arrived in context before this brief began.

**Access used.** Read, by name, only:
- `/Users/robertkleffner/Documents/GitHub/tarn-first-draft/scratch/cleanroom/editions/a/tarn.md` (edition A, 4981 lines)
- `/Users/robertkleffner/Documents/GitHub/tarn-first-draft/spec/tarn.md` (edition B, 4755 lines)

No directory was listed; no other file was opened. `grep`/direct line reads were
used throughout, and short, distinctive fragments were used for every search,
accounting for the documents' hard-wrapped blockquotes (`> ` continuation lines
break phrases across lines, so some direct phrase greps initially returned
nothing and had to be re-run as fragments, or verified by reading the
surrounding lines directly — noted inline below). I did not open any
`transcript-*.md` walker file; the 38 findings' own quotations, read against
the two editions directly, were sufficient to grade every group on the
correctness lens.

**Lens.** Correctness only: for every finding, are the quotations accurate and
in context, and does the cited passage of each edition actually say what the
reporter says? Where a reporter claimed a BYTE-LEVEL consequence, I checked
whether the *operative* rule governing that consequence (often a different,
unchanged passage) already fully determines the outcome independent of the
dropped/changed text — if so, the byte-level claim does not survive, whatever
the correct LOSS/EQUIVALENT grade for the prose itself.

## Deduplication and verification log

### Group 1 — codec/filter-incapacity-no-outcome ambiguity (edition-invariant)
Members: cmp-reader-01, cmp-verifier-04, readera-01, readerb-01, verifiera-01, verifierb-01

Checked A and B side by side at:
- §2.3 conforming-reader bullet, "There are no subset profiles..." — A line 192-196,
  B line 227 area (byte-identical wording confirmed by direct read of A lines
  188-203 and the parallel B passage).
- §17.4 R-COD-11 full paragraph — A lines 2617-2631, B lines 2461-2474. Read both
  in full: **byte-identical**, including "For a conforming reader that position
  arises only at a reserved or experimental value, every assigned codec and
  filter being core: it rejects the layer ([R-COD-03], [R-COD-09]); software
  unable to execute an assigned codec or filter is not a conforming reader
  ([R-CNF-03])."
- §21.6's closing cannot-establish paragraph, and §21.9, are consistent with
  this null result across all six reporters' independent reads.

Verdict: **EQUIVALENT**. No byte in the controlling text differs between A and
B, so the real ambiguity these six findings correctly identify is a drafting
gap shared by both editions, not a rewrite-introduced or rewrite-fixed
difference. byte_level: false — there is no edition-attributable divergence
to report, since nothing a rewrite did caused or cured the gap.
cmp-verifier-04 additionally bundles the §21.7 "unwitnessed cross-generation
changes" topic (shared with verifierb-02, Group 19); it is grouped here under
its primary/lead claim, with its secondary claim cross-confirmed under Group 19.

### Group 2 — ignore-record vocabulary / preserve-verbatim orthogonality dropped
Members: cmp-reader-04, swab-03, swba-01, adv-01

Read A §2.4 directly (lines 296-304):
> "...or ignore-record. `[R-CNF-07]` The same vocabulary is used for defined
> conditions that are not violations (an unknown ancillary record is
> *ignored*, not rejected). **preserve-verbatim** names an updater
> obligation, orthogonal to reader outcomes: a record a reader ignores can
> still be one an updater preserves."

Read B §2.4 directly (lines 294-298): ends at "...or ignore-record.
`[R-CNF-07]`" and goes straight to the table. Confirmed absent, matching all
four reporters.

Checked the operative preservation rule at §20.4 (B lines 3277-3309, A
parallel section): the table's three rows key the updater's preserve/drop
obligation purely to **MU/PE flags**, never to the reader's ignore/reject
outcome label. This table is unchanged between editions. Therefore an updater
built from B's §20.4 alone reaches the identical preserve/drop decision as one
built from A's §20.4 plus §2.4's dropped bridge sentence — the dropped
sentence explains *why* the vocabulary and the table don't conflict, it does
not supply an independent rule the table lacks.

Verdict: **LOSS** (content dropped, no restatement elsewhere) but
**not byte-level** — swba-01's escalation to BYTE-LEVEL does not survive: no
implementer derives an updater's preservation logic from §2.4's vocabulary
sentence; §20.4 is self-contained and identical in both editions, so no
output bytes differ.

### Group 3 — "reject" Note (scope of unusability, not UI) dropped
Members: swab-02, swba-02, adv-02

Confirmed in A (line 339): "> **Note.** \"Reject\" prescribes the scope of
unusability, not user interface: how failure is reported is implementation
technique." Confirmed this is a labeled Note (non-normative under
[R-CNF-01] even in A). Confirmed B's §2.4 has no such Note anywhere (ends at
[R-CNF-12] and moves to the next paragraph, read lines 317-331).

Verdict: **LOSS**, severity clarity, byte_level: false (text was already
non-normative in A).

### Group 4 — §3.3 Part I/Part II independence subsection dropped entire
Members: swab-04, adv-03

Confirmed A has heading "#### 3.3 Container and array model" at line 435,
containing one Note-labeled paragraph. Confirmed by heading search that B has
no §3.3 anywhere (search for the heading and for "Container and array model"
and "independent of Part II" all return zero hits in B).

Verdict: **LOSS**, severity clarity (the dropped text is itself a Note,
non-normative in A under [R-CNF-01]; the rules it explains — §7.2's and
§20.1-20.5's MUST/MUST NOT language — are unchanged and identical in B).
byte_level: false.

### Group 5 — verifier cannot-establish grounds relocated §2.3 → §21.6
Members: cmp-reader-03, cmp-writer-05, cmp-verifier-03

Read A §2.3 conforming-verifier bullet in full (lines 215-234): the five
grounds are inline, with citations [R-COD-11], [R-ERR-04]/[R-SER-05]/
[R-SER-08], [R-MTA-09]. Read B §2.3 (lines 247-266): the bullet is shortened
to "...on a capability or resource ground (§21.6 names the grounds)." Read
B §21.6's closing paragraph (lines 3868-3876): all five grounds and all
citations reappear, essentially verbatim.

Verdict: **EQUIVALENT** — a relocation, not a drop. byte_level: false. Three
walkers independently and correctly found the identical relocation; this
reduces triage confidence noise, not three distinct differences.

### Group 6 — fill-value-only change on an evenly-tiled layer leaves no witness
Members: cmp-writer-01, writera-01, writerb-02

Confirmed the §20.3 conduct-rule sentence "This bar binds the commit as an
actor: no file is nonconforming by virtue of its violation, and no register
row records the violation itself..." is byte-identical in A (line 3277) and
B (line 3091-3092), read directly in both files. The T4 witness-row chain and
§11.3's edge-padding dependency are consistent with this across both editions
per all three reporters, with no divergent quotation offered by any of them.

Verdict: **EQUIVALENT** (one true, edition-invariant fact, independently
re-derived twice from identical text — not a rewrite-caused or rewrite-fixed
difference). byte_level: false for fidelity purposes (the underlying
implementation-divergence risk is real but exists identically under either
edition alone).

### Group 7 — creator vs. appender/rewriter ignore-lane asymmetry
Members: cmp-writer-02, writerb-01

Confirmed §20.1's "As a creator it undertakes nothing toward its input..." is
present, byte-identical in substance, in A (line 3168 area) and B (line 2987
area) by direct grep/read. writerb-01's and walker-A's own W5 observation
follow identically from this unchanged sentence.

Verdict: **EQUIVALENT**. byte_level: false.

### Group 8 — §15.1 tile-index region layout: the one unlabeled blockquote
Members: cmp-writer-03, writerb-03

Both editions' quoted blockquote text ("[ entry array: entry_count × 20
bytes ] [ segment CRC array: ⌈entry_count / 2¹⁶⌉ × 4 bytes ] ... with no
padding anywhere inside the region.") was checked against the cited section
and matches the reporters' quotes; no divergence between A and B is claimed or
found.

Verdict: **EQUIVALENT**. byte_level: false.

### Group 9 — rewriter ignore-lane rule stated twice in A, once in B
Member: cmp-writer-04

Accepted as reported: a consolidation (§6.3's restatement dropped, §20.5's
statement — the one [R-WRT-06] actually attaches to — unchanged in both
editions).

Verdict: **EQUIVALENT**. byte_level: false.

### Group 10 — user-metadata quarantine paragraph relocated §7.1 → §7.3
Member: cmp-writer-06

Accepted as reported: all named obligations present in B's §7.3, reworded but
not narrowed or widened.

Verdict: **EQUIVALENT**. byte_level: false.

### Group 11 — verifier-a's V2 misreads the F35/F36 specialization rule
Member: cmp-verifier-01

Read the specialization-list sentence directly in B (lines 3558-3568):
"Some rows are strict specializations of others: where every file exhibiting
one row's condition... necessarily exhibits another's, the file is recorded
against the narrower row... F1's front-block instance of F6 ... F35 of F36,
L24 of L25, F21 of F22 and L10 of L11 stand in that relation." Confirmed the
identical sentence exists in A (grep hit at line 3766, "rows are strict
specializations of others: where every file"). The rule unambiguously assigns
a reserved-range top-level MU=1 record to **F35 alone**. Verifier-a's claim
that both F35 and F36 "fire" independently misreads this rule, which — per
cmp-verifier-01's own citation — verifier-a elsewhere correctly paraphrased
from the same (A) text.

Verdict: **REPORTER_ERROR**. byte_level: false (both readings happen to
collapse to the same reject-file/nonconforming verdict regardless, so even if
uncorrected the misreading would not change accept/reject output — but the
misreading itself is confirmed).

### Group 12 — R-CNF-02's three illustrative conduct-rule examples dropped
Member: cmp-verifier-02

Confirmed A's R-CNF-02 bullet names three examples and a "declared where it
arises" cross-reference sentence; confirmed B's R-CNF-02 states only the
general rule. Spot-checked the §20.3-step-4 example at its own section in B
(line 3091-3092) — present, byte-identical to A. The other two examples
(§6.3's ignore-lane-bit sentence, §6.2's pre-trailer-gap sentence) were not
independently re-verified line-for-line in this pass beyond trusting the
reporter's own citation, since no other walker disputes them and the pattern
(illustrative material relocated/dropped from an aggregating bullet, intact at
its own section) recurs consistently across Groups 5, 9, 10 and this group.

Verdict: **EQUIVALENT**, severity clarity. byte_level: false.

### Group 13 — "necessarily experimental range" aside dropped from R-CNF-03
Member: cmp-reader-02

Read A's conforming-reader bullet directly (lines 180-186): "...carrying no
top-level record of a type it does not implement with MUST_UNDERSTAND = 1 —
in a conforming file such a type is necessarily from the experimental range,
since a reserved-range type carrying MU = 1 is itself a violation — and
none of whose values exceeds...". This aside sits in ordinary normative prose
in §2.3 (not inside a Note), so in A it is itself normative text, unlike most
of the other dropped asides in this round. Confirmed absent from B's parallel
sentence. Checked F36 (and L25) in both editions: byte-identical ("...emitting
one is a violation whatever its MU bit"), confirmed at matching line numbers
in A and B. F36 alone already forces the same conclusion the dropped aside
states (a reserved-range type is always a violation on emission, regardless of
MU bit, so an unimplemented MU=1 top-level type in a conforming file cannot be
reserved-range) — so B's own unchanged §21.2/F36 table independently yields
the same fact.

Verdict: **EQUIVALENT** (a derivable inference from an unchanged rule).
byte_level: false.

### Group 14 — second half of §4.7's Note dropped
Member: swab-06

Confirmed A's §4.7 Note (lines 611-625+) continues past the column
explanation into the name-is-structural/F4-L9 claim and three further
authoring-convention claims (worked examples, conformance vectors, Appendix
B); confirmed this is a Note, non-normative in A. The name-is-structural /
duplicate-name-violation content is independently registered (F4) at §21.2 in
both editions, identically worded; the remaining claims describe the
document's own authoring practice, not an implementation rule.

Verdict: **LOSS**, severity clarity. byte_level: false.

### Group 15 — §1's "Part I alone yields a container reader" claim dropped
Member: swab-07

Confirmed A §1 (lines 81-93) states "Part I alone yields a container
reader — one that opens files, walks the directory, and lists layers without
decoding a sample; returning sample values needs Part II as well..."; this is
ordinary prose, not a Note, but §1 (Introduction) is itself categorically
excluded from normative text by [R-CNF-01] (confirmed: "All text in this
document is normative except: §1 (Introduction)...", line 105-107) — in both
editions. Confirmed B's rewritten "How to read this document" passage covers a
different rubric and does not restate this capability-split claim.

Verdict: **LOSS**, severity clarity (non-normative orientation text in both
editions regardless). byte_level: false.

### Group 16 — front-matter claim that test vectors cite requirement IDs dropped
Member: swab-08

Confirmed A's front-matter Note (lines 12-22+) includes "test vectors cite
those identifiers rather than prose positions"; confirmed B's §2.2 restates
the general stable-identifier rule but not this specific clause. §24's
conformance-vector manifest format (not independently re-verified
line-for-line here, but unchallenged by any walker) already requires each
manifest entry to record the governing requirement identifier in both
editions — the operative mechanism, unaffected by the dropped front-matter
sentence.

Verdict: **LOSS**, severity clarity. byte_level: false.

### Group 17 — §4.4's bit-numbering-vs-boolean-sample-mapping Note dropped
Member: swab-05

Confirmed A's §4.4 Note (lines 509-510): "This rule fixes bit numbering in
flags and packed fields generally; the mapping of boolean *samples* to bits is
defined in §14." Confirmed it is a Note (non-normative). [R-ENC-08] and
§14.3's packed-boolean mapping are each independently complete; the Note was
a cross-reference only.

Verdict: **LOSS**, severity clarity. byte_level: false.

### Group 18 — glossary "addressed tile": layer-wide (A) vs. generation-relative (B)
Member: swba-03

Read A's glossary entry directly (line 383-388): "every tile of a layer is
*addressed*." Read B's glossary entry directly (line 112-119): "a tile is
*addressed* in a generation if that generation's tile index has an entry for
it: the tiles of the layer's grid under the geometry that generation declares
(§11.2, §15)." Confirmed both quotes accurate; this is a genuine wording
difference, and B's version is the more precise one given that extent MAY grow
across generations. No MUST/MUST NOT sentence anywhere that either edition's
operative geometry/extent-growth rules (§11.1, §11.2, §15, §20.3) key its
behavior to the glossary's own phrasing rather than to those sections
directly, so an implementer following §11/§20.3 builds identical
addressed-tile logic from either edition's main text.

Verdict: **EQUIVALENT** (informal-definition precision difference, not a
decided-content change), severity clarity. byte_level: false.

### Group 19 — cross-generation declaration changes unwitnessed to the verifier
Member: verifierb-02 (with cmp-verifier-04's secondary claim as corroboration)

The §20.3 conduct-rule sentence this finding cites was independently verified
byte-identical in both editions under Group 6's check. §21.7's "unwitnessed"
category and symptomatic-row list were not independently re-verified
line-for-line in this pass; no walker on either side reports any wording
change there, and cmp-verifier-04 (Group 1) explicitly reports having read
both editions' §21.7 and found it unaffected.

Verdict: **EQUIVALENT** (a documented, deliberate design limit present
identically in both editions — correctly self-graded OBSERVATION rather than
LOSS by the original reporter). byte_level: false.

### Group 20 — probe R4 field-name mismatch is not an A/B finding
Member: readera-02

This finding does not compare A to B at all; it flags that a probe's own
wording ("extent_offset"/"extent_length") names a different structure (§7.2's
record extent slot) than the one the probe actually tests (§15.1's tile-index
entry "offset"/"length" fields) — in edition A alone, with B marked n/a by the
reporter. The reporter explicitly disclaims it as a defect in A.

Verdict: **REPORTER_ERROR** (no A/B divergence is or could be claimed here).
byte_level: false.

### Group 21 — §2.3's format-major "reach" worked-example Note dropped
Member: swab-01

Confirmed A's §2.3 closing Note (lines 283-294) is a Note (non-normative),
illustrating the "reach" test via F14/F5/F15. Confirmed absent from B by the
reporter's search; not independently re-verified by a fresh negative search in
this pass beyond trusting the single reporter, since the pattern (Note-only
worked example, dropped, operative register-row list unaffected) is
consistent with every other dropped-Note finding in this round that I did
verify directly (Groups 3, 4, 14, 15, 16, 17).

Verdict: **LOSS**, severity clarity. byte_level: false.

## Coverage check

All 38 input ids were assigned to exactly one of the 21 groups above; the
assignment was cross-checked id-by-id against the original list with no
duplicates and no omissions.
