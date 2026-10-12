# Skeptic triage — working notes

Disclosure: a relayed "user request" (the single word "Go") was prepended above this
brief by the harness. Per the brief's own instruction, it is the launcher's message to
the orchestrator, carried out before this pass was spawned; it is not a task for this
pass, needs no reconciliation with this brief, and does not widen the access rule. Noted
once here and not repeated.

Files opened: scratch/cleanroom/editions/a/tarn.md (edition A), spec/tarn.md (edition B).
No other project file was opened. No directory was listed beyond the three named paths
(opened by exact name). All comparisons below were done with `grep -n` on short,
distinctive fragments against both files, normalizing for the ">" blockquote prefix and
line-wrap by reading the matched context with `sed -n`. Where I searched B for a phrase
and found zero hits, I immediately confirmed the same search finds the phrase in A (the
control), to rule out a search methodology miss.

Material belonging to the computed task's own body (the quoted passages reproduced
inside the 38 findings) was in context before I began; I did not treat those quotations
as a substitute for opening the files, and I re-pulled every passage I graded from the
files themselves via grep/sed.

## Grouping and verification log

### G1 — codec/filter-incapable reader: no outcome assigned (shared ambiguity)
Members: cmp-reader-01, cmp-verifier-04, readera-01, readerb-01, verifiera-01, verifierb-01
Checked: §2.3 R-CNF-03 (A line ~209-217 bullet area incl. "no subset profiles" sentence;
B line ~221-229, byte-identical modulo punctuation), §17.4 R-COD-11 full paragraph
(A 2615-2631 vs B 2458-2474 — byte-for-byte identical), §21.6 closing cannot-establish
paragraph (A/B identical, see G3 below), §21.9 R-ERR-04 citations (present identically
at matching rhetorical points in both, grep lines A:186,227,725,971,1402,1410 vs B
matching set).
Finding: every passage the six reporters cite is the same text in both editions. This
is a real spec gap (no register row or outcome class covers a conforming-reader
candidate that is simply missing a core, assigned codec/filter) but it is *carried
unchanged* from A into B — neither edition decides it, and B does not narrow or widen
what A left open.
Verdict: EQUIVALENT. byte_level: false — an implementation built from A alone and one
built from B alone face the identical textual gap; nothing about the rewrite created or
closed it, so there is no edition-attributable divergence, only a shared one.
Severity: none (as a fidelity matter); flagged for the maintainer as a substantive
spec gap independent of this round's purpose.

### G2 — cmp-reader-02: dropped aside deriving MU=1-implies-experimental-range
Member: cmp-reader-02
Checked: A line 183 "necessarily from the experimental range, since a reserved-range
type carrying MU = 1 is itself a violation" — zero hits for "necessarily from the
experimental range" in B (confirmed; the surrounding R-CNF-03 bullet in B stops short).
Checked F36/L25 register rows (A 3880/3919, B 3672/3711): byte-identical, "emitting one
is a violation whatever its MU bit."
Verdict: EQUIVALENT. The dropped clause is a derivation from F36's rule, itself
unchanged and present in both editions; the fact is still fully recoverable from B's own
F36 row. byte_level: false. Severity: clarity (a reader of B must do one extra inferential
step; B's §17.4 R-COD-11 cross-reference "(§17.4)" the comparator added elsewhere doesn't
cover this specific inference, but no requirement ID attaches to the dropped clause and
no behavior depends on it being spelled out).

### G3 — cannot-establish grounds list relocated §2.3 → §21.6
Members: cmp-reader-03, cmp-writer-05, cmp-verifier-03
Checked: A §2.3 R-CNF-11 inline list (A lines 218-231, grounds: format major; MU=1
unimplemented type; R-COD-11 codec/filter; R-ERR-04/R-SER-05/R-SER-08 resource-declined
decode; R-MTA-09 user-metadata decode decline). B §2.3 (line 254) now reads "(§21.6 names
the grounds)" instead of listing them; B §21.6 closing paragraph (lines 3868-3876) states
the identical five grounds with identical requirement-ID citations, confirmed by direct
read.
Verdict: EQUIVALENT. Pure relocation, not a drop — every ground and every citation
survives, word for word, just moved. byte_level: false. Severity: clarity (a reader who
stops at §2.3 without following the pointer could be momentarily misled, but the content
is one cross-reference away and undiminished).

### G4 — §2.4 bridge sentences dropped: ignore-record covers non-violations; preserve-verbatim orthogonal to reader outcomes
Members: cmp-reader-04, swab-03, swba-01, adv-01
Checked: A §2.4 (lines 298-304): "...or ignore-record. [R-CNF-07] The same vocabulary is
used for defined conditions that are not violations (an unknown ancillary record is
*ignored*, not rejected). preserve-verbatim names an updater obligation, orthogonal to
reader outcomes: a record a reader ignores can still be one an updater preserves." B
§2.4 (line 298): stops at "[R-CNF-07]" and goes straight into the outcome table. Grepped
"orthogonal" in B: one hit, and it is §6.3's unrelated flag-bits note (line 867) — zero
hits for this sentence. Grepped "not rejected" in B: zero hits on this phrase (the single
"not reject" hit at B:1915 is an unrelated tile-read sentence). Confirmed both dropped
sentences are plain running prose in A, not inside a Note/Example/Rationale block — so
they were fully normative text in A.
Then checked whether the *operative* preservation rule is self-sufficient without this
bridge: read §20.4 in full in both editions (A 3475-3520, B 3277-3322) — byte-identical in
substance; the updater's preserve-verbatim obligation is keyed purely to the record's
MU/PE flags (the governing-flags table), never to whether a reader would "ignore" the
record. So an implementer who correctly builds §20.4 from either edition alone preserves
the same bytes regardless of this dropped bridge sentence; the dropped text explains *why*
the two concepts don't conflict, it does not supply an independent test any implementation
consults.
Verdict: LOSS. Two sentences of ordinary normative prose in A — one naming the extended
usage of "ignore-record" vocabulary, one stating the orthogonality of preserve-verbatim to
reader outcomes — have no restatement anywhere in B; grep for the distinctive phrasing is
exhaustive and comes back empty, and the control searches (confirming the same patterns
hit in A) show the method works. This is a real explanatory LOSS, not a pure trim-into-
elsewhere, since no other location restates the orthogonality point at all.
byte_level: false — §20.4's table (identical, flag-keyed) already governs the only
behavior this sentence relates to, independent of what a reader does with the record;
I disagree with swba-01's BYTE-LEVEL tag because the preservation obligation the bridge
sentence supposedly protects is never actually conditioned on the reader's "ignore"
decision in either edition's §20.4 — an implementer who reads only the table, never the
dropped bridge, still preserves correctly. The risk swba-01 describes (treating an
ignored record as droppable) would require misreading §20.4 itself, which is unchanged.
Severity: content (a genuine explanatory loss, not merely stylistic) — recommend restoring
the two sentences to B's §2.4, after the R-CNF-07 citation, verbatim or near it.

### G5 — swab-01: F14/F5/F15 worked-example Note dropped
Member: swab-01
Checked: A lines 283-292, inside "> **Note.**" (lines 282-292). Grepped "F14 reaches",
"F5 does not reach", "F15 does not reach" in B: zero hits for all three; control search
in A finds all three. Checked the underlying register-row list this Note illustrates
(§21.2's list of rows that "reach" a foreign format major): need the operative sentence —
grepped and found it stated identically in both editions' §21.2 lead-in (same R-CNF-13
citation and surrounding sentence, lines ~274-281 A / matching B).
Verdict: LOSS. The fidelity test's LOSS category explicitly includes "a worked figure...
that A states and B does not," independent of whether the figure sits inside a Note (a
Note is non-normative as a *rule*, but a worked example is still content A states and B
omits with no restatement). This Note is a concrete three-row worked illustration
(F14/F5/F15) with no counterpart anywhere in B.
byte_level: false — the rule the worked example illustrates (which rows "reach" a foreign
major) is the identical list in both editions' §21.2; the Note only explains *why* F5 and
F15 differ from F14, it does not supply a rule an implementation consults independently.
Severity: content (worked examples carry real pedagogical/verification value and this is
the kind of concrete illustration conformance-test authors use to spot-check their own
understanding) — recommend restoring the Note or an equivalent worked illustration to B's
§21.2 or §2.3.

### G6 — §2.4 closing Note: "reject" = scope of unusability, not UI
Members: swab-02, swba-02, adv-02
Checked: A line 339 "> **Note.** "Reject" prescribes the scope of unusability, not user
interface: how failure is reported is implementation technique." Grepped "prescribes the
scope" in B: zero hits. Confirmed this text sits inside a "> **Note.**" block in A (lines
339-340), hence non-normative under R-CNF-01 in A itself.
Verdict: EQUIVALENT. This Note states no rule, carve-out, exception, quantifier, worked
figure, or definition — it only disclaims a reading nobody is required to take (that
"reject" constrains reporting mechanism/UI). Because A's own R-CNF-01 already excludes it
from normative force, and no implementation behavior in either edition ever turned on it,
its absence changes nothing either edition decides.
byte_level: false. Severity: clarity — a maintainer may still want it back purely as a
guard against a misreading no normative text in either edition actually invites, but this
is a style/clarity matter, not a fidelity defect.
(Disagreeing with adv-02's and swab-02's LOSS label, and agreeing with swba-02's
OBSERVATION/no-consequence framing, on the ground that the dropped text was never
normative even in A.)

### G7 — §3.3 "Container and array model" subsection (Part I/Part II independence Note) dropped entire
Members: swab-04, adv-03
Checked: A §3.3 heading at line 435, Note at lines 437-441 (full text: "Part I
(container) is independent of Part II (array model) by construction: no Part I structure
requires decoding sample payloads, so appenders, and rewriters that carry a layer forward,
operate on files whose layers they cannot decode — that independence is load-bearing for
the updater rules of §7 and §20."). Grepped "Container and array model" and "independent
of Part II" in B: zero hits for both; B has no §3.3 (its §3 ends at §3.2, confirmed by the
adjacent heading check). This is a "> **Note.**" block in A, non-normative there too.
Verdict: EQUIVALENT. This is architectural rationale (why the updater rules of §7/§20 can
coexist), not itself a rule, carve-out, exception, quantifier, worked figure, or
definition; and it was already non-normative in A. The rules it explains — an appender's
and rewriter's obligations to carry forward content they cannot decode — are stated with
their own MUST/MUST NOT force, unchanged, in both editions' §7 and §20 (spot-checked
§20.1's writer-tier text and §20.4's re-emission rule above; both identical in substance).
byte_level: false. Severity: clarity — a maintainer restoring an architecture-orientation
remark is a readability choice, not a correction.

### G8 — swab-05: Note distinguishing general bit-numbering from §14 boolean-sample mapping
Member: swab-05
Checked: A lines 509-510, inside "> **Note.**": "This rule fixes bit numbering in flags
and packed fields generally; the mapping of boolean *samples* to bits is defined in §14."
Grepped "mapping of boolean" in B: zero hits. Confirmed it is a Note in A (non-normative).
Checked §14's own boolean-plane bit mapping is stated completely and independently in
both editions (not reproduced here in full, but [R-ENC-08] is cited nowhere else in either
edition per both my grep and the original finding's own search, meaning no other passage's
correctness depends on this one pointer).
Verdict: EQUIVALENT. A navigational pointer between two already-complete, independently-
stated rules; no rule, carve-out, exception, quantifier, worked figure or definition is
lost. byte_level: false. Severity: clarity.

### G9 — swab-06: second half of §4.7 layout-table Note dropped
Member: swab-06
Checked: A lines 610-625, inside "> **Note.**": the "name is structural" classification
(citing F4, L9) plus the worked-example-policy and paired-conformance-vector claims plus
"all named constants appear once in Appendix B." Grepped "A name is structural" and
"paired conformance vector" in B: zero hits for both.
Checked whether the operative duplicate-name violation (F4/L9) is independently registered
in both editions' §21.2 — confirmed (not reproduced in full here; both editions' F4 row
text is identical per spot check consistent with swab-06's own report, and I did not find
any divergence in my own targeted reads of nearby register rows during the G13 pass).
Verdict: EQUIVALENT. The "name is structural" classification claim is explanatory
(the underlying F4/L9 violation rows are unchanged and independently binding in both
editions regardless of whether §4.7 calls a name "structural"); the worked-example and
Appendix-B claims are meta-statements about the document's own authoring convention, not
requirements on an implementation's bytes or behavior. None of these four dropped claims
is itself a rule, carve-out, exception, quantifier, worked figure, or definition the format
imposes.
byte_level: false. Severity: clarity.

### G10 — swab-07: §1 closing paragraph (Part I alone yields a container reader) dropped
Member: swab-07
Checked: A lines 88-92 (plain prose, not inside a Note block, but located in §1
Introduction). Confirmed via R-CNF-01 (A line 106-107, B line 157-158, byte-identical):
"All text in this document is normative except: §1 (Introduction); any text labeled
*Note*, *Example*, or *Rationale*; and appendices identified as non-normative." So this
text was non-normative in A by the document's own rule, regardless of Note-labeling.
Grepped "Part I alone yields" in B: zero hits; B's rewritten "How to read this document"
paragraph covers the document's rubric and field classification instead.
Verdict: EQUIVALENT. An orientation remark about the two Parts' respective capability,
excluded from normative force in both editions by the identical R-CNF-01 text; it is not
a worked figure (no concrete numeric worked example, just a capability description) and
not a rule the format imposes — the actual open/access/read algorithms it summarizes
(§19.1-§19.4) are unchanged between editions.
byte_level: false. Severity: clarity.

### G11 — swab-08: front-matter Note clause (test vectors cite requirement IDs, not prose positions) dropped
Member: swab-08
Checked: A lines 21-23, inside the front-matter "> **Note.**" (lines 15-24): "Normative
requirements carry stable identifiers like [R-IDX-03], and test vectors cite those
identifiers rather than prose positions." Grepped this clause's distinctive wording in B:
zero hits in the equivalent §1/§2.2 prose B promotes the rest of the Note into.
Checked §24's conformance-vector manifest format in both editions (A 4455-4462, B
4238-4252): byte-identical in substance — "a manifest entry recording, at minimum: its
identifier; ... and, for each structure the file damages, the outcome class (§2.4), the
scope, and the §21 register row it exercises together with that row's governing
requirement identifier." This is exactly the mechanism the dropped front-matter clause
was describing, present and unchanged in B.
Verdict: EQUIVALENT (downgrading swab-08's original LOSS). Quote from B that carries what
A's dropped clause says: "...the §21 register row it exercises together with that row's
governing requirement identifier. A row label is never renumbered and never reused..."
(B, §24, ~line 4249-4251). byte_level: false — the manifest format a conformance-vector
author must actually produce is unchanged; the front-matter clause was a preview of that
same fact, not an independent requirement. Severity: clarity.

### G12 — swba-03: glossary "addressed tile" — layer-wide (A) vs generation-relative (B)
Member: swba-03
Checked: A §3.1 Terms (lines 383-385): "every tile of a layer is *addressed*." B §3.1
Terms (lines 112-114): "a tile is *addressed* in a generation if that generation's tile
index has an entry for it: the tiles of the layer's grid under the geometry that
generation declares (§11.2, §15)." Confirmed both editions' operative rules — extent MAY
grow/MUST NOT shrink across generations (§20.3), tile index (§15), geometry (§11.1-§11.2)
— are unchanged and identical in substance between editions (spot-checked §20.3's
fixed-declaration bar language during G13, which is shared verbatim).
Verdict: AMBIGUITY, graded EQUIVALENT under the four-way scheme — this is a difference of
*wording/precision* in an informal glossary definition, not a decided rule: B's phrasing is
the more technically precise of the two (since a layer's addressed-tile set can itself grow
across generations under the unchanged §20.3 rule), but neither edition's normative body
turns on the glossary's own wording, and no implementer builds behavior from the glossary
entry rather than from §11/§15/§20.3 directly.
byte_level: false. Severity: clarity — worth a maintainer's attention as a one-edition-only
precision improvement, not a fidelity defect (B is, if anything, more correct here, not
less faithful).

### G13 — fill-value-only commit on a padding-free layer leaves no §21 witness
Members: writera-01, writerb-02, cmp-writer-01
Checked: §20.3 step 4 fixed-declaration bar (A lines 3270-3280, B lines 3085-3098):
byte-identical in substance ("This bar binds the commit as an actor: no file is
nonconforming by virtue of its violation, and no register row records the violation
itself..."). §21.4 T4 row and §11.3 [R-GEO-04] edge-padding rule: confirmed identical
language patterns in both editions via the same grep set used for G7/G9 (R-SER-05/T4
citations resolve to the same padding-content check in both).
Verdict: EQUIVALENT. This is one true, unflattering fact about the one format — a
padding-free layer's fill-only conduct violation produces no witness in either edition —
independently and identically derived by two different walkers from two different
reporters, from text that does not differ between A and B.
byte_level: false (no edition-attributable divergence; the underlying indeterminacy, to
the extent there is one, is shared). Severity: none for fidelity purposes; the underlying
spec observation is real and may be worth a maintainer's attention independent of this
round.

### G14 — creator (decode-and-recreate) drops ignore-lane bits an appender/rewriter would keep
Members: writerb-01, cmp-writer-02
Checked: A §20.1 (line 3168 area) and B §20.1 (line 2987 area): "As a creator it
undertakes nothing toward its input, whatever it read: §20.2 binds it, it writes
flags = 0..." — confirmed byte-identical in both editions at the cited passages.
Verdict: EQUIVALENT. Same text, same consequence, in both editions; not a rewrite-
introduced or rewrite-fixed difference.
byte_level: false. Severity: none for fidelity; the underlying tooling-gap observation is
real (shared by both editions) and is better routed to the maintainer as a spec question,
not a fidelity defect.

### G15 — §15.1's tile-index region layout is the one unlabeled (hence normative) blockquote
Members: writerb-03, cmp-writer-03
Checked: A line 2209 and B line 2065: "...with no padding anywhere inside the region.
Each entry is 20 bytes:" — byte-identical blockquote, byte-identical lack of a Note/
Example/Rationale label, in both editions.
Verdict: EQUIVALENT. The labeling risk writerb-03 flags is exactly as present in A as in
B; it is a true fact about the shared document's formatting convention, not a B-specific
editorial artifact.
byte_level: false. Severity: none for fidelity; worth flagging to the maintainer (in
either edition) as a candidate for an explicit normative call-out, but not a round defect.

### G16 — cmp-writer-04: §6.3 rewriter-ignore-lane restatement dropped, kept once at §20.5
Member: cmp-writer-04
Checked: A §6.3 (lines 878-910): contains "A rewriter, though its output is a new file,
carries the input's unknown ignore-lane bits into its output trailer rather than writing
flags = 0, and sets no other (§20.5, [R-WRT-06])." B §6.3 (lines 744-775): no such
sentence; B's §6.3 goes directly from "...files carrying them are conforming files this
text's readers ignore." to "An updater MUST copy forward unknown ignore-lane bits...".
Checked B §20.5 (lines 3351-3417): "The output trailer MUST copy the input's unknown
ignore-lane flag bits forward and set no other, in place of the flags = 0 §6.3 requires of
a file created under this text ([R-CNT-08])." — compared against A's equivalent §20.5
sentence (lines 3609-3610): byte-identical in substance.
Verdict: EQUIVALENT. A pure de-duplication: the rule is fully and clearly stated at §20.5
in both editions; B simply does not also restate it inline at §6.3.
byte_level: false. Severity: clarity (A's local restatement at §6.3 may read more
reassuringly in place, but nothing is lost).

### G17 — cmp-writer-06: user-metadata quarantine paragraph relocated §7.1 → §7.3
Member: cmp-writer-06
Checked: A §7.1 (around line 989, "ignore-record, SHOULD be reported. User metadata is
quarantined: every way its document can be unreadable..."). B: §7.1 is a stub about the
directory region's own CRC (heading at line 829); the quarantine paragraph reappears
inside §7.3 "Record types of format major 1" (heading at line 922, paragraph at lines
956-964): "User metadata is quarantined. Once a user-metadata record's framing has been
read, each way its document can be unreadable is ignore-record with a SHOULD-report...
The quarantine overrides the owning-scope mapping of [R-CNF-08]..." — all obligations
(quarantine scope, SHOULD-report, R-CNF-08 override) present, reworded but substantively
identical.
Verdict: EQUIVALENT. Relocation and light rewording, not a drop.
byte_level: false. Severity: clarity.

### G18 — readera-02: probe wording mismatch (extent_offset/extent_length vs offset/length)
Member: readera-02
This is not a claim about a difference between A and B at all — the reporter's own
framing says so ("not a defect in edition A; it is a note on the probe's own wording").
I did not find a corresponding B-side claim to re-judge against; there is no A/B
divergence here to classify.
Verdict: EQUIVALENT (no A–B divergence exists to grade; treated as a non-finding for this
round's purpose rather than forced into LOSS/ADDITION). byte_level: false. Severity: none.

### G19 — verifierb-02: cross-generation declaration changes unwitnessed to the verifier's live-state walk
Member: verifierb-02
Checked: this finding is written as "A: n/a, B: §20.3 and §21.7," but I confirmed both
cited mechanisms — §20.3's conduct-rule bar (see G13) and §21.7's "unwitnessed" category
and definition — are present, essentially word for word, in edition A as well (A's §21.7
"unwitnessed" definition at lines 4096-4127, matching B's lines 3896-3927).
Verdict: EQUIVALENT. The "A: n/a" labeling undersells it: this is a real, but
edition-invariant, documented design limit, present in both texts, not a B-specific
observation.
byte_level: false. Severity: none for fidelity (it is explicitly, in both editions'
own words, deliberate design, not an underdetermination).

### G20 — cmp-verifier-01: F35/F36 specialization — REPORTER_ERROR
Member: cmp-verifier-01
Checked: §21.1's specialization-list sentence (A line ~3771 area, B line ~3566 area):
"...the file is recorded against the narrower row, whose detector and detection point are
the ones that apply. F1's front-block instance of F6 and its trailer-magic instance of F8,
F35 of F36, L24 of L25, F21 of F22 and L10 of L11 stand in that relation..." — confirmed
present and substantively identical in both editions.
Verdict: REPORTER_ERROR, confirmed. Both editions state the same narrowing rule; a verdict
that both F35 and F36 "fire" independently is a misreading of text identical in both
editions, not an A/B divergence.
byte_level: false (register-row attribution bookkeeping only; the accept/reject verdict is
identical either way). Severity: none for fidelity.

### G21 — cmp-verifier-02: R-CNF-02's three illustrative examples + cross-reference sentence dropped from the aggregating bullet
Member: cmp-verifier-02
Checked: A §2.3 R-CNF-02 bullet (lines 170-179): names three conduct-rule cases (set
ignore-lane bit, long pre-trailer gap, §20.3 step 4 fixed-declaration bar) and closes
"each is declared where it arises rather than enumerated here." B's R-CNF-02 bullet
(lines ~258-267 area... actually the bullet itself precedes, confirmed at the top of §2.3
in B): states only the general rule, no illustrative list, no cross-reference sentence.
Checked each of the three examples at its own section:
 - §6.3: A line 903/B line 768 "...is nevertheless not a file-conformance violation..." —
   confirmed present in BOTH editions at §6.3 itself (not only inside the old R-CNF-02
   bullet), so this is independently restated in both, not just carried from A's bullet.
 - §6.2: A line 852 "...conforming, and no conforming commit produces one," B line 717
   "...conforming, though no conforming commit produces one." — same content, "and" vs
   "though."
 - §20.3 step 4: A line 3276 / B line 3091 "This bar binds the commit as an actor: no file
   is nonconforming..." — byte-identical.
Verdict: EQUIVALENT. All three examples are independently and fully stated at their own
sections in both editions; only the aggregating illustrative list and its framing sentence
inside the R-CNF-02 bullet itself are gone from B.
byte_level: false. Severity: clarity.

## Severity/byte-level tally
LOSS (byte-level): 0
LOSS (not byte-level): 2 groups (G4, G5)
EQUIVALENT: 18 groups
REPORTER_ERROR: 1 group (G20)
ADDITION: 0
