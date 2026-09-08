# Audit transcript — lane "the-scopes"

Charter: hunk-01.diff, hunk-03.diff, hunk-04.diff, hunk-16.diff
(directory: /private/tmp/claude-501/-Users-robertkleffner-Documents-GitHub-tarn-first-draft/r33-audit/case/)

## Disclosure

Files read: the four named hunk files in full (cat'd together in one
command); spec/tarn.md, in the ranges quoted below, via `sed -n` and
one `grep -n` / `python3 -re` pass for whitespace-normalized search
(the doc is hard-wrapped, per the brief's warning, so line-oriented
grep alone would under-count). No other files were opened. I did not
list the case/ directory beyond the four names given, did not open
full.diff, did not open any other hunk file, and did not read docs/,
AGENTS.md, PLAN.md, registry.json, or git history.

Context I did not ask for: my system prompt's task preamble ("What
this is") describes a prior ADR (ADR-0124, "the closed list of
permitted layer-declaration changes") and a "pre-round-32 audit" with
specific defect counts, plus a MEMORY.md digest of prior-session
lessons and a git status block naming recent commit subjects
("Cleanroom round 32: charter", "ADR-0124...", etc.). None of that
material is part of the specification or evidence about it. I did not
use it to reach any conclusion below — my four hunks concern reader
conformance / metadata quarantine / coverage-walk text, not the
layer-declaration edit-permission list that ADR-0124's narrative
describes, so there was no live risk of transplanting its named
defect shapes onto unrelated text, but I flag the exposure per the
charter's instruction. Working files: none written (no CRC
recomputation or scratch table was needed for these four hunks).

## Hunk 01 — [R-CNF-03], §2.3 Conformance classes (lines ~185-193)

### The rule adopted
A conforming reader MUST implement/decode both registered record
types (0x0001 layer, 0x0002 user metadata — §7.3's exact and only two
rows), on par with core codecs/filters, both channel layouts, core
sample types, and assigned user-metadata encodings; software that
declines any one of these — including "a registered record type" —
is not a conforming reader, "even if it reads all other conforming
files correctly."

### Passage read in full
Lines 152-260 (§2.3, all five conformance-class bullets) and the
paragraph after them (the "reaches" definition, unaffected by this
hunk).

### Check 1 — tense/quantifier
The sentence is present-tense, format-major-1-scoped ("§7.3" is
literally headed "Record types of format major 1"), matching the
tense of every other item in the same list ("§17 designates as
core", "§12 designates as core"). "Both record types" is a correct
count: §7.3's table (line 1068-1070) has exactly two rows, 0x0001 and
0x0002. No other row exists in that table ("All other type values
are unassigned"). Quantifier is exact.

### Check 2 — citations resolve
- §7.3 registers exactly two record types → verified (table has two
  rows only). PASS.
- The unchanged citation "§21.6's closing paragraph names the other
  two" (context around this bullet, untouched by the hunk) → verified
  against §21.6's actual last paragraph (lines ~3899-3910, "Two
  structural cases are conforming files a reader nevertheless
  refuses"), which names exactly two cases (unimplemented
  version_major; experimental-range top-level MU=1 type). This is a
  *different* paragraph from the one hunk-16 edits (hunk-16 touches
  the paragraph immediately before this one). PASS, and confirms
  hunk-16's edit does not disturb this citation.
- §12.1 ("core sample types" — R-TYP-01: "a conforming reader MUST
  decode every one of them") and §17.2 ("core" codecs — R-COD-03:
  "MUST implement every one of them") were opened to compare what
  "handle" is doing double duty for. PASS (both resolve as claimed by
  the pre-existing, unedited part of the sentence).

### Check 3 — normative placement
The bullet lives in plain (unlabeled, ">"-free) prose under §2.3,
which is normative body text, not §1 (which R-CNF-01 exempts). The
parallel sentence in §1 ("There are no subset profiles, no subset
readers, and no feature a conforming reader can decline," line 40-41)
is *inside* the exempted §1 and is consistent with, but not the
normative source for, this rule. Confirmed by opening §1's text and
checking it precedes the "#### 2.3" heading. PASS — the normative
statement is where it needs to be, and the §1 echo is correctly
non-normative background, not a second (and only) statement of the
rule.

### Check 4 — local contradiction
Checked against §20.4 (lines 3373-3399, Re-emission and preservation),
which contains, unedited: "an updater implements both registered
types and understands an unregistered type it implements from its
definition" (line 3394-95) — an assumption §20.4 already relied on
without any normative backing elsewhere in the document prior to this
hunk. Since updaters inherit "every reader obligation" (§2.3), hunk-01
supplies exactly the missing justification for that §20.4 sentence
rather than conflicting with it. No contradiction found.

Also checked the surrounding em-dash gloss in the same sentence:
"carrying no top-level record of a type it does not implement with
MUST_UNDERSTAND = 1 — in a conforming file such a type is necessarily
from the experimental range, since a reserved-range type carrying
MU = 1 is itself a violation —". Before this hunk, nothing forced a
conforming reader to implement the *layer* record type (0x0001,
MU=1), so in principle an unimplemented top-level MU=1 type could have
been 0x0001 itself, which is neither reserved nor experimental —
falsifying the gloss's "necessarily from the experimental range"
claim. After the hunk, since a conforming reader MUST implement both
registered types, an unimplemented top-level MU=1 type can no longer
be 0x0001, and the gloss's claim becomes true as stated. The hunk
*repairs* a latent gap in this gloss; it does not break it. (Reported
as a positive, not a finding.)

### Check 5 — exhaustive claims
"both record types" (2, verified against §7.3's table) and the list
overall ("a core codec, a core filter, either channel layout, a core
sample type, an assigned user-metadata encoding, or a registered
record type") is closed and, on inspection, exhaustive of §7.3's
table plus the pre-existing items. No falsifying third record type
found (§7.3: "All other type values are unassigned").

### Check 6 — unconstrained siblings
Considered other layer-record fields with a similar "value set, some
subset mandatory" shape (linearization: only value 1 is defined at
all — §11.4, R-GEO-05, L33 — so it is trivially "core" with no
sibling to omit) and confirmed no comparable un-enumerated sibling
quantity was left out of this list by the hunk.

### Check 7 — analogy
Not applicable; this hunk does not argue by pointing at another rule
as its warrant (no "exactly as", "the same way", etc. in the diff).

### Check 8 — anaphora after insertion
The insertion is mid-sentence (extends an existing list), not between
two sentences, so there is no back-reference in the *following*
sentence ("There are no subset profiles: ...") whose antecedent moved
— that sentence's own list was edited in the same hunk, in lockstep.
Checked forward through the rest of the bullet (into "A reader MUST
detect every violation...") for stray anaphora: none point back to
the newly-added list items specifically.

### Verdict
No confirmed defect. Sound restatement; if anything, it closes a
previously-unstated dependency of §20.4 on reader-level record-type
coverage.

## Hunk 03 — §5.2 Byte coverage (lines ~718-728)

### The rule adopted
Extends the enumeration of what keeps the §9.7 coverage walk
"complete" (as opposed to "incomplete/partial"): alongside a tile's
or document's declined *decode* (extent still enumerated as a
claimant), an index entry that `[R-IDX-03]` classifies reject-tile on
a *structural* ground likewise does not make the walk incomplete —
"the walk passes over" it (§9.7).

### Passage read in full
§5.2 in its entirety (lines 692-745) and §9.7 in its entirety (lines
1476-1518, through the Note), plus §15.3's Entry validity table and
its lead-in (lines 2206-2225) and R-IDX-03's own definition (lines
2213-2219).

### Sweeps run
```
grep -n "licence to reject on any detected violation is untouched"  -> 0 hits (hard-wrap defeats line grep; used as a control, see hunk-16 below)
python3 whitespace-normalized search for "licence to reject" -> 2 hits (R-CNT-18's own text; hunk-16's edit) — used to confirm the normalizer works before trusting any zero-count elsewhere.
```

### Check 1 — tense/quantifier
"an entry `[R-IDX-03]` classifies reject-tile on a structural ground"
is the *exact* subject noun phrase §9.7's closing sentence uses ("An
entry `[R-IDX-03]` classifies reject-tile on a *structural* ground
does not make the walk incomplete"). Same generic/universal "an
entry" quantifier in both places — a faithful, word-for-word
restatement of the *subject*, not a widened or narrowed set.

### Check 2 — citations resolve
- `[R-IDX-03]` — opened at line ~2213-2219 (§15.3's lead-in) and its
  own six-row "structural" list (lines 2226-2232, confirmed: exactly
  six rows marked *structural*, matching the text's own "Six rows are
  marked *structural*"). The cited text there states: "Such an entry
  contributes no stored extent to the *verifier* rows... and none to
  `[R-LIF-08]`'s coverage walk, so any bytes it nominally addressed
  that no other claimant claims fall to slack." This is the
  controlling statement. PASS as a citation (R-IDX-03 does classify
  reject-tile on a structural ground, and does say the walk does not
  count it) but see Check 4/8 for how the *host* sentence's phrasing
  interacts with it.
- (§9.7) — opened; its closing sentence (line ~1514-1518) reads: "An
  entry `[R-IDX-03]` classifies reject-tile on a *structural* ground
  does not make the walk incomplete: the walk passes over it, and the
  bytes it nominally addresses fall to slack (§15.3). `[R-LIF-08]`."
  This is word-for-word the source of both the subject noun phrase and
  the "the walk passes over" clause the hunk borrows. PASS.

### Check 3 — normative placement
Plain prose, no ">" block, §5.2 proper. Normative. PASS.

### Check 4 / Check 8 — local contradiction and anaphor scope of "so does"
This is where I spent the most effort. The full resulting sentence:

> "...a tile's or a document's decode declined leaves the walk
> complete, that claimant being enumerated from its index entry or
> extent slot, and so does an entry `[R-IDX-03]` classifies
> reject-tile on a structural ground, which the walk passes over
> (§9.7)."

Two readings are available for the elided predicate of "so does":

(a) *Narrow* — "so does" substitutes only for the finite verb phrase
"leaves the walk complete" (matching subject-verb agreement: "X
leaves the walk complete" / "so does Y"). Under this reading each
subject gets its *own* appositive: the decode-declined claimant is
"enumerated from its index entry or extent slot"; the
structurally-rejected entry is, separately, "passed over." Under (a)
the sentence says only that *both* keep the walk complete, by two
different and each individually correct mechanisms — this matches
§9.7/R-IDX-03 exactly (Check 1's word-for-word match) and is not a
contradiction.

(b) *Wide* — because "so does" immediately follows "...being
enumerated from its index entry or extent slot," a reader could take
the absolute-construction appositive as carried over too, i.e. read
the sentence as also claiming the structurally-rejected entry is
"enumerated ... as a claimant." That reading is flatly false: R-IDX-03
says such an entry "contributes no stored extent to the... coverage
walk" and its bytes "fall to slack" — the opposite of being an
enumerated claimant. Under (b) the added clause contradicts the very
citation it carries.

I could not fully rule out reading (b) as the one many readers would
take on a first pass, precisely because of the placement chosen (the
new clause was appended immediately after the word "enumerated"
rather than, say, restructured as its own sentence). English
"so does X" constructions can go either way depending on how tightly
the first clause's appositive is felt to bind; I do not have a way to
force disambiguation from the text alone. Reading (a) is the
grammatically defensible one and is fully consistent with every
citation checked; reading (b) is the one the placement invites and is
false.

### Check 5 — exhaustive claims
The three grounds of incompleteness listed just before the edited
sentence ("a scope-level rejection ends that scope's enumeration...",
"the verifier declined a layer on resource grounds...", "the verifier
elected under `[R-CNF-11]` to stop at the first violation") are
untouched by this hunk. Cross-checked against §9.7's own parallel list
("Where the walk does not complete — a scope-level rejection blocks
enumeration, the verifier declines a layer on resource grounds... or
it stops at the first violation") — same three grounds, unchanged, and
consistent between the two sections. PASS, no drift introduced.

### Check 6 — unconstrained siblings
Considered whether the hunk should also have addressed the CRC-only
failure case ("stored bytes fail the entry's crc" — §15.3's row
"reject-tile (§8.2) — the entry itself is well-formed; its extent
stands"). It should not: that case is explicitly *not* structural
(R-IDX-03: "one whose stored bytes alone fail its crc keeps its
extent... and none to `[R-LIF-08]`'s coverage walk" is the
*structural*-only clause; the CRC-only case is already covered by "a
tile's ... decode declined leaves the walk complete, that claimant
being enumerated" — a CRC failure is exactly a case where the extent
is known/enumerated but content is bad). No sibling left unconstrained.

### Check 7 — analogy
N/A (no "exactly as" / "on the model of" construction here — the added
clause cites §9.7 for identity of wording, not as an analogy to a
different rule).

### Verdict
PLAUSIBLE, not CONFIRMED. The grammatically correct reading of the
sentence is consistent with R-IDX-03/§9.7 (I verified this formally,
subject phrase for subject phrase). But the insertion's placement,
immediately after "...being enumerated from its index entry or extent
slot, and so does...", invites the false reading that a
structurally-rejected entry is *also* enumerated as a claimant, which
directly contradicts R-IDX-03's "contributes no stored extent... fall
to slack." This is a NEW_AMBIGUITY from the insertion's placement
relative to an existing phrase, not a proven change in the normative
rule (R-IDX-03 itself is untouched and controls regardless of which
way a reader parses this restatement).

Byte-level: **No.** R-IDX-03 (unedited) is the controlling rule for
what a verifier must count as a claimant vs. slack, and it is
unambiguous on its own. Two verifiers reading only the controlling
rule would agree; the ambiguity is confined to this one restatement
in §5.2, and even a verifier that misread it as claiming "enumerated"
would still be bound by R-IDX-03 directly. This does not fork
emittable bytes or accept/reject verdicts on its own.

## Hunk 04 — [R-CNT-25], §7.1 Directory region (lines ~971-982)

### The rule adopted
"Application metadata never makes the structural data it annotates
unusable" (replacing "never invalidates the structural data it
annotates"): a defect *in the user-metadata document* can never cause
reject-file/-layer/-tile of the structural data it describes. Adds an
explicit carve-in: a rule *outside* the quarantine (currently just
R-MTA-05, rows F27/L48) can still record "a document's defect" at file
or layer scope — i.e. make the *file* nonconforming — but even then
"the verifier records it there and a reader owes nothing for it."

### Passage read in full
§7.1 in full (lines 952-982) and §7.2's opening (983-1010, for the
"owning scope" and record-framing context); §18.1/§18.2 in full (lines
2600-2660, the quarantine's home section) for the encoding-core
requirement and R-MTA-02/03; §21.5's lead-in (lines 3821-3833) and
§21.6's "Two conditions that once sat in this table..." paragraph
(3878-3890, shared with hunk-16) for the F27/L48/R-CNT-22 lineage
claim; R-MTA-05's own text (lines 2757-2768).

### Sweeps run
```
python3 whitespace-normalized: "never invalidates" -> 0 hits (confirms the old phrase was fully replaced, not left standing elsewhere)
python3 whitespace-normalized: "makes the structural data" -> 1 hit (the hunk's own sentence, only)
python3 whitespace-normalized: "structural data it annotates" -> 1 hit (same)
python3 whitespace-normalized: "quarantined" -> 4 hits (walked each: §7.1's own two uses, §21.5's lead-in restatement, and §22's privacy-surface mention) — none restate the old "never invalidates" wording, so no unswept restatement survives.
```
Control for the zero-count: same normalizer, searched "quarantined"
(known to occur) and got 4 hits, confirming the script is not
silently failing on wrapped text.

### Check 2 — citations resolve
- `[R-MTA-05]` — opened at lines 2757-2768: "unsorted members do not
  make a document unreadable: the file is nonconforming, a verifier
  MUST report it, and readers process the document unchanged." Exact
  match for "a document's defect... at the file" and for "a reader
  owes nothing" (readers process it *unchanged*). PASS.
- F27 — opened at line 3708: file-scope row, detector *verifier*,
  outcome *certification*, rule `[R-MTA-05]` (R-CNF-05); row text
  itself says "the document stays readable and readers process it
  unchanged." PASS, matches "the verifier records it there."
- L48 — opened at line 3779: identical shape, layer scope. PASS.
- (§21.6) for "a reader owes nothing for it" — opened the paragraph
  hunk-16 also edits (lines 3878-3890): "neither obliges a reader to
  reject anything" (post-hunk-16 wording) / "neither is a reason for a
  reader to reject anything" (pre-hunk-16 wording) — either version
  supports "owes nothing." PASS under both orderings.

### Check 4 — "owes nothing" against R-CNF-12's licence
Opened R-CNF-12 (lines 318-333): "a reader MAY reject it upon
detecting any violation, including violations whose assigned detector
is the verifier." "Owes nothing" is an absence of a MUST, which
coexists with R-CNF-12's MAY without tension — the sentence does not
say "and a reader MUST NOT reject for it," so there is no collision
with R-CNF-12's blanket permissive licence. PASS, no contradiction.

### Check 4 (continued) — is "a rule outside this quarantine" a set the document defines?
The quarantine's covered causes are enumerated two sentences earlier,
closed: "a failed extent CRC, an unimplemented or invalid encoding, a
decode failure, or content violating the document's own rules." R-
MTA-05 (member ordering) is not one of these four — it does not affect
readability at all — so "outside this quarantine" is a well-defined
residual class, and I could not find a second member of that residual
class besides R-MTA-05/F27/L48 (checked R-CNT-22/F28/L49 — about
record *flags*, not "a document's defect," correctly excluded; checked
R1/R-MTA-03 — encoding value violations, but these fall *inside* the
quarantine's own "invalid encoding" clause, correctly not double-
counted here). PASS — the closed citation list is, as far as I can
verify, exhaustive for "a document's defect."

### Check 5 — exhaustive claims
"at the file or the layer" — checked against §7.3's scope column for
user-metadata (0x0002): "file when top-level; layer as sub-record."
No third scope exists for this record type (no tile-scope variant), so
"at the file or the layer" is exhaustive, not an overclaim.

### Check 6 — unconstrained siblings
Checked whether an updater/compactor owes something extra for a
record carrying an R-MTA-05 defect it retains unmodified — no such
obligation is stated or implied; §20.4's ordinary re-emission rule
(byte-identical retention, unaffected by this hunk) already covers it,
and R-MTA-05 only binds *new* output under R-CNF-05 if an updater
chooses to modify the record. No gap found.

### Check 3 — normative placement
Plain prose in §7.1, no ">" block. Normative. PASS.

### Verdict
No confirmed defect. The rewrite ties the rule to the document's own
term of art ("not usable," matching the Outcome-class table's
"reject-*: ... not usable" language at line 304-306) instead of the
vaguer "invalidates," and the added carve-in is citation-accurate and
closed.

## Hunk 16 — §21.6 closing paragraphs (lines ~3883-3889)

### The rule adopted
For the two conditions that were moved out of the "not violations"
table into the register (R-MTA-05 unsorted keys; R-CNT-22 stored-flag
mismatch on a registered type): neither *obliges* a reader to reject
the file, and separately, R-CNF-12's general licence to reject a
nonconforming file on any detected violation remains available
regardless — "as `[R-CNT-18]` says of its own case."

### Passage read in full
§21.6 in its entirety (lines 3853-3910, table through both closing
paragraphs and into the §21.7 heading); §7.4's full text (lines
1090-1160) for R-CNT-18's own clause; R-CNF-12's full text (lines
318-333).

### Sweeps run
```
python3 whitespace-normalized: "licence to reject on any detected violation is untouched" -> 2 hits total in the document: R-CNT-18's own clause (§7.4) and hunk-16's new clause (§21.6). Nowhere else. This confirms the analogy's target exists and is singular (no third copy to reconcile).
python3 whitespace-normalized: "reason for a reader" / "never a reason" / "is not a reason" -> 0 hits each. Control: same normalizer found "obliges a reader" 4 times (including this hunk's own new text) and "obliges no reader" 0 times, so the zero counts are not a normalizer failure.
```
Conclusion of the sweep: the pre-repair phrase ("is not a reason for a
reader to reject anything") has been fully replaced everywhere in the
document — no orphaned restatement of the old wording survives
elsewhere (the brief's specific concern under "Also report").

### Check 2 — citations resolve
- `[R-CNF-12]` — opened, quoted above under hunk-04. PASS, matches
  "licence to reject a nonconforming file on any detected violation."
- `[R-CNT-18]` — opened at §7.4 (lines ~1144-1148): "...an unknown
  sub-record type with MU = 1 is reject-layer, and where the file is
  otherwise conforming a reader MUST NOT reject the file for it — on a
  nonconforming file `[R-CNF-12]`'s licence to reject on any detected
  violation is untouched; with MU = 0 it is ignore-record." The exact
  clause hunk-16 echoes is present verbatim. PASS as a citation of
  wording.

### Check 7 — analogy, verbs side by side
Repair's governing verb (for its own two conditions): **"neither
obliges** a reader to reject anything" — i.e. no MUST; a reader MAY
reject only via R-CNF-12's separate general licence.

R-CNT-18's governing verb for *its own case* (the file-otherwise-
conforming branch): a reader **"MUST NOT reject** the file for it" —
an affirmative prohibition, not merely an absence of obligation. Only
the *second* half of R-CNT-18's sentence (the nonconforming-file
branch) uses the shared "licence... is untouched" language hunk-16
quotes.

These verbs do not match: "not obliged" (permissive-neutral) is
weaker than "MUST NOT" (prohibitive). The phrase "as `[R-CNT-18]` says
of its own case" is textually accurate only if read narrowly, as
citing R-CNT-18 solely for the shared closing clause ("CNF-12's
licence... untouched") — which is the one piece of R-CNT-18 that is
genuinely parallel, since R-CNT-18's *file-otherwise-conforming*
branch (with its "MUST NOT reject" bar) has no analogue at all for
R-MTA-05/R-CNT-22: those two conditions are never "otherwise
conforming" — the violation itself is what makes the file
nonconforming, so there is no "MUST NOT reject the file for it, if
file is otherwise conforming" case here to parallel. A reader who
takes the analogy at its broader, more natural word (R-CNT-18's
"case" = its whole two-branch rule, prohibition included) could
wrongly conclude that a reader is similarly *barred* from rejecting a
file solely for an R-MTA-05/R-CNT-22 violation — which is false; no
such prohibition exists anywhere for these two conditions, and R-CNF-
12's full MAY-reject licence applies to them unconditionally (they are
always-nonconforming, never "otherwise conforming" edge cases the way
R-CNT-18's sub-record scenario can be).

### Check 4 — local contradiction
Checked whether "neither obliges... to reject" collides with any MUST
elsewhere that would force rejection for these two conditions — none
found; F27/L48/F28/L49 are all "detector: verifier, outcome:
certification," meaning no reader-scope obligation attaches by
definition (§21.1's own reader/verifier split, referenced generally).
No contradiction.

### Check 6 — unconstrained siblings
Checked the full "verifier | certification" row list in §21 (F7, F25,
F26, F33, F36, L18, L25, L40-L42, L46, L47, T2, T4, T5, T26 — see grep
output) to see whether "Two conditions that once sat in this table are
violations" over-claims completeness against this larger set. It does
not: that sentence is a historical claim ("once sat in this table,"
i.e. §21.6's earlier "not violations" list), not a claim that R-MTA-05
and R-CNT-22 are the only verifier/certification-only violations in
the document — the other rows listed above were never in the "not
violations" table to begin with, so they are out of this paragraph's
scope and the paragraph does not claim otherwise.

### Check 3 — normative placement
Plain prose (no ">" block), §21.6. Normative. PASS.

### Check 8 — anaphora after insertion
Read forward into the next paragraph ("Two structural cases are
**conforming files a reader nevertheless refuses**...", through to the
§21.7 heading). That paragraph independently cites `[R-CNT-18]` again
("the same type as a layer sub-record is reject-layer and never a
ground to refuse the file (`[R-CNT-18]`)") — a separate, explicit
citation, not a pronoun, so the insertion does not change what any
bare "it"/"this"/"that" resolves to there. No anaphor shift found.

### Verdict
PLAUSIBLE. The citation of R-CNT-18 is textually accurate for the one
clause it literally shares, but the analogy as phrased ("as
`[R-CNT-18]` says of its own case") invites reading in the stronger,
prohibitive sense R-CNT-18 actually carries for its own scenario,
which has no counterpart for R-MTA-05/R-CNT-22. This is an ANALOGY-
check mismatch: the two "own case[s]" differ in whether a prohibition
on rejection exists at all, and the shared sentence fragment obscures
that difference rather than stating it.

Byte-level: **No.** The explicitly stated rule ("neither obliges... to
reject," "CNF-12's licence... is untouched") is itself correct and
unambiguous taken on its own; R-CNF-12 only ever grants a MAY, never a
MUST, so even a reader who over-read the analogy and became more
lenient (declined to exercise a reject it was never obliged to make)
would remain fully conforming. No accept/reject verdict or emittable
byte set forks on this reading.

## Summary of checks that passed cleanly (no finding)

- Hunk 01: checks 1-6, 8 all passed; check 7 not applicable. The
  em-dash gloss check specifically requested by the brief passed, and
  in fact the hunk repairs a previously-unstated gap in that gloss
  (documented above, not filed as a finding since it is not a
  defect).
- Hunk 04: checks 1-6, 8 all passed; check 7 not applicable (no
  analogy construction in this hunk's own text).
- Hunk 03: checks 1, 2, 3, 5, 6 passed; check 7 not applicable; checks
  4/8 produced the one PLAUSIBLE finding above.
- Hunk 16: checks 1 (n/a, no restated normative rule to compare
  tense/quantifier against — this is itself close to normative
  source), 2, 3, 4, 6, 8 passed; check 7 produced the one PLAUSIBLE
  finding above.
- NESTED_DASH: none of the four hunks introduce any new em-dash into
  the repaired text (checked each diff's added lines directly); no
  finding under this check.

## Rejected candidates

1. Hunk-01, "handle" as an umbrella verb across codec/filter (=
   implement), sample type (= decode), and now record type: I
   considered this a possible TENSE_QUANTIFIER/ambiguity finding, but
   confirmed "handle" was already polysemous across these categories
   *before* the hunk (the verb governs the whole pre-existing list),
   so this is not something the repair introduced. Closed: pre-
   existing usage, not a new defect.
2. Hunk-01, whether requiring "both record types" changes any byte a
   conforming *writer* may emit: closed — this is a reader-conformance
   clause; §21.6/R-MTA-03 already required user-metadata encoding
   support, and the layer-record case is not one any real
   implementation could omit and still function as a reader at all
   (it could not process any tile without the layer record). No
   byte-level fork identified.
3. Hunk-03, whether the "so does" sentence is a flat contradiction
   (not just an ambiguity): closed to PLAUSIBLE rather than CONFIRMED
   after the formal subject/predicate parse (Check 1) showed the
   narrow reading matches R-IDX-03/§9.7 exactly; I could not force the
   wide (contradictory) reading as the *only* available parse, so I
   did not report it as CONFIRMED.
4. Hunk-04, whether "at the file or the layer" needed a third scope
   for tile-level metadata defects: closed — user-metadata records
   have no tile-scope variant (§7.3's own scope column), so no third
   case is missing.
5. Hunk-16, whether the "two conditions" framing under-counts the
   verifier/certification rows in §21 (F7, F25/26, F33, F36, L18, L25,
   L40-42, L46/47, T2, T4, T5, T26): closed — that framing is an
   explicit historical claim ("once sat in this table") not a general
   completeness claim, and I confirmed none of those other rows are
   or were ever part of the "not violations" table.

## Confidence / where an empty result would have needed more

Both findings filed are PLAUSIBLE, not CONFIRMED, and neither is
byte-level. I want to be explicit about what would have raised my
confidence to CONFIRMED and what I could not do to get there: for
hunk-03, a second, independent sentence elsewhere restating "an entry
classified reject-tile structurally is [not] enumerated as a
claimant" in the *same* terms as this passage would have let me test
which reading the document's own usage favors; no such second
restatement exists (the only other places R-IDX-03's structural class
is discussed are §9.7 and §15.3 themselves, both of which I already
used to fix the *controlling* rule, not this restatement's phrasing).
For hunk-16, direct testimony from a hypothetical implementer's
reading would settle it; absent that, I relied on the verb-for-verb
comparison the brief's check 7 specifies and reported the mismatch I
found rather than asserting a verdict beyond what the text supports.
