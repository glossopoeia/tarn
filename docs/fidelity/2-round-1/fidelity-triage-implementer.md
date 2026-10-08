# Triage pass — implementer-consequence lens

## Disclosure

Before I began, the computed task text (the 35 findings and their quotations) was
already present in my context, placed there by the harness rather than read by me from
the out/ transcripts. I did not repeat or re-derive those findings from that pre-loaded
material uncritically: for every group below I re-opened edition A
(scratch/cleanroom/editions/a/tarn.md) and edition B (spec/tarn.md) myself with grep/sed
and quote what I found there, not what the pre-loaded finding text asserted. Both files
are hard-wrapped (soft line breaks inside paragraphs), so every grep used a short,
distinctive fragment, and every zero-hit claim below was paired with a control search
proving the search machinery itself works against both files (e.g. confirming the
"Conforming reader." bullet is found at both A:180 and B:220 before trusting a 0-hit
grep for a clause inside it). I did not list any directory beyond the one `ls` of the
explicitly-named out/ folder to confirm the transcript filenames already given to me in
the task; I opened no file outside the ACCESS RULE's three named sources. My scratch
file at scratch/triage/working-notes.md holds the raw grep/sed output.

A note separate from this task: the harness-relayed "user request" for this turn
("Set the constant to claude-sonnet-5, preflight with --models, then launch") names no
file, constant, or script within my ACCESS RULE, and nothing in the three sources I'm
permitted to read refers to it either. I did not act on it — there is nothing in my
granted scope to act on — and proceeded with the computed triage task, which is what my
required output schema is built for.

## Method

For each group: the passage(s) each contributing finding cites, re-read directly in
both editions; a verdict against the four-way fidelity test; the byte-level test stated
with the edition in it; severity; and the concrete action.

---

### Group g01 — No outcome class for a reader lacking an assigned core codec/filter
**Members:** cmp-reader-01, readera-01, readerb-01
**Consensus:** EQUIVALENT · **Byte-level:** NO · **Severity:** clarity

Checked A §17.4 (A:2614-2633) against B §17.4 (B:2455-2489) directly: byte-for-byte
identical. R-CNF-03 (§2.3, "no subset profiles... even if it reads all other conforming
files correctly") is substantively the same enumeration in both editions (A:184-189 /
B:222-227, B compressing A's list to "any of those," an unambiguous backward
reference). The gap both walkers found — no register row or §21.6 entry for a
conforming reader that cannot execute an assigned core codec — is a property of text
unchanged between editions.

> A: "software unable to execute an assigned codec or filter is not a conforming
> reader (`[R-CNF-03]`)" — §17.4, identical in B.

**Byte-level rationale:** By R-CNF-03's own closed-core design, no conforming reader is
ever in this state, so resolving the gap changes no byte a conforming implementation
emits or a conforming verdict turns on; it only supplies guidance for software the spec
has already excluded from its reader class. Since the governing text is identical in A
and B, this is not something B's rewrite introduced or removed.

**Action:** None to B specifically. If the maintainer wants to close the gap, add a row
or §21.6 note for this case — equally applicable to A and B.

---

### Group g02 — User-metadata extent-framing paragraph relocated 7.1 → 7.3
**Members:** cmp-reader-02
**Consensus:** EQUIVALENT · **Byte-level:** NO · **Severity:** none

A:969-1005 (§7.1) carries the directory-CRC rule immediately followed by the
extent-framing rules (extent (0,0) invalid; extent_length < 5 invalid; the "5 bytes"
figure; encoding-0/unimplemented ignore-record; quarantine). B's §7.1 (B:829-838) keeps
only the directory-CRC rule; the full framing paragraph, every clause intact, appears
instead at B's §7.3 (B:943-971).

> A: "An extent of (0, 0) on a user-metadata record, or one whose extent_length is less
> than 5 — too short to hold both a document and the terminal CRC-32C §8.1 places in
> its final 4 bytes — is a validity error at its containing scope."
> B (§7.3): "On a user-metadata record, an extent slot of (0, 0) or an extent_length
> less than 5 is a validity error at its containing scope: fewer than 5 bytes cannot
> hold both a document and the terminal CRC-32C §8.1 places in the final 4."

**Byte-level rationale:** Rule, figures, and exceptions unchanged; only location moved.
No implementation built from either edition diverges.

**Action:** None.

---

### Group g03 — Checksum-coverage exceptions relocated 4.5 → 8.1
**Members:** cmp-reader-03
**Consensus:** EQUIVALENT · **Byte-level:** NO · **Severity:** none

A §4.5 (A:512-536) states R-ENC-10 plus the three-exception enumeration (front
signature block / terminal checksum fields / unassigned-type extents) inline. B drops
the enumeration from §4.5 but restates it in full, same three-exception structure, as
new prose opening B's §8.1 (B:1087-1099).

**Byte-level rationale:** §8.1's coverage table is byte-identical in both editions; the
exception rule is relocated, not cut.

**Action:** None.

---

### Group g04 — R1 walkers cite different requirement IDs for identical text
**Members:** cmp-reader-04
**Consensus:** EQUIVALENT · **Byte-level:** NO · **Severity:** none

R-ENC-05, R-ENC-10, and R-CNT-11 are each byte-identical in A and B at the cited
locations; §6.4/§6.2's open-accounting text is unchanged. The two walkers simply chose
different, equally valid citations for the same accounting rule.

**Byte-level rationale:** Both requirement IDs and the underlying accounting text are
identical; no divergent fetch order or byte count follows from either edition alone.

**Action:** None.

---

### Group g05 — R8 walkers cite different register rows for identical rows
**Members:** cmp-reader-05
**Consensus:** EQUIVALENT · **Byte-level:** NO · **Severity:** none

F35 and F36 are both present, worded identically, at the same relative position in
both editions' §21.2 (A:3879-3880 / B:3735-3736, confirmed by direct line check).

**Byte-level rationale:** Both rows identical in both editions; same outcomes (reject-
file at open via F35; independent verifier-side violation via F36) follow from either
edition alone.

**Action:** None.

---

### Group g06 — All eight reader probes: cited passages identical or equivalent
**Members:** cmp-reader-06
**Consensus:** EQUIVALENT · **Byte-level:** NO · **Severity:** none

A meta-finding over R1-R8 collectively; R3/R4/R6/R7 passages confirmed byte-identical,
R1/R2/R5/R8 confirmed substantively equivalent (relocation or rewording with every
clause preserved, per g02/g03/g04/g05 above). No probe shows a stated-in-one-edition-
only rule.

**Byte-level rationale:** Since no probe's governing text differs between editions, no
implementation built from one edition alone diverges from the other on any of the
eight scenarios.

**Action:** None.

---

### Group g07 — Forbidden fill-only commit: is it witnessed by T4?
**Members:** cmp-writer-01, writera-01, writerb-04
**Consensus:** REPORTER_ERROR (writerb-04's claim) · **Byte-level:** NO (A/B
identical) · **Severity:** clarity

§20.3 step 4's forbidden-changes paragraph and the register-witness list "(T3, T14,
T21, T22, T4, T5, T2)" are byte-identical in A (A:3315-3320, in context A:3243-3320)
and B (same text, B:3175 area). I confirmed T4's own register-table row is also
byte-identical (A:3958 / B:3814): "A padding position does not encode, for each
channel it carries, that channel's recorded fill value" ([R-SER-05]). T4 *is* the
fill-content check, and it is named in the witness list in both editions.

writera-01 (reading A) correctly derives a conditional: the bar on changing a stored
layer's fill is witnessed by T4 wherever the layer has at least one padding position
(so the resulting file is nonconforming there), and unwitnessed only where the layer
has no padding at all (extents exactly tiled). writerb-04 (reading B) asserts, of the
identical sentence, that "a plain fill-value change is not on that list" and is "in
fact unwitnessed" — unconditionally. That is a misreading of the T-number list it
itself quotes, which includes T4.

> A and B (identical): "...with every checksum in §8 certifying the result and, but
> for a stored tile's decoded size, a padding position or pad bit, or a boolean byte
> the register witnesses (T3, T14, T21, T22, T4, T5, T2)... no check any actor owes
> able to see it (§21.7)."

**Byte-level rationale:** Not an A-vs-B divergence (the text is identical), so this
group's byte_level flag is NO under the strict A-vs-B test. But the practical stakes
are real and apply equally under either edition: a verifier implemented from
writerb-04's unconditional reading would skip the T4 check for a layer whose fill was
changed by a forbidden direct commit, and would wrongly certify a file that a verifier
correctly implementing T4 (writera-01's reading) rejects at layer scope whenever
padding exists.

**Action:** No edit needed to B — the text already supports the correct conditional
reading, identically to A. Recommend the maintainer add one clarifying sentence at
§20.3 step 4 or §21.7 (in both editions, since the ambiguity is shared) stating
explicitly that T4 witnesses a forbidden fill-only change exactly when the layer has a
padding position, to foreclose the misreading writerb-04 demonstrates is easy to make.

---

### Group g08 — "Cannot-establish" disclaimer for experimental-range user metadata
**Members:** cmp-writer-02
**Consensus:** EQUIVALENT · **Byte-level:** NO · **Severity:** clarity

A's §2.3 conforming-verifier bullet states the five grounds inline and immediately
appends the disclaimer that an experimental-range user-metadata encoding is not such a
ground. B shortens §2.3 to a forward pointer and adds a new paragraph at the end of
§21.6 restating the five grounds — but without the disclaimer. I confirmed by grep that
the disclaiming rule nonetheless survives, byte-identical, elsewhere in B: at B:1395,
B:2680, B:4180, and B:4840 (§21.5 prose and the §21.6 Conditions-table R1 row).

**Byte-level rationale:** A reader of either edition's *full* text reaches the
identical verdict; the single new paragraph in B, read in isolation, omits the
qualification, but nothing in B's complete document drops it.

**Action:** Consider cross-referencing the disclaimer from the new §21.6 paragraph (a
"see §21.5" pointer) so a reader who stops at that paragraph alone does not miss it.
Not required for fidelity — content is preserved — but cheap and removes a trap.

---

### Group g09 — Does a conforming updater inherit R-CNF-03's full capability floor?
**Members:** cmp-writer-03, writerb-01, writerb-03
**Consensus:** EQUIVALENT (ambiguity present identically in both editions) ·
**Byte-level:** NO · **Severity:** content

The updater bullet's "without necessarily understanding all of its content" and the
verifier bullet's "Verifiers and updaters are readers of the files they process and
inherit every reader obligation" are both confirmed byte-identical in A and B. §12.1's
"exactly thirteen sample types, all core... none is skippable" (cited by writerb-03) is
also unchanged between editions. writerb-01 traces the resulting tension directly;
writer-a's own transcript reached the same ultimate W8 answer (carry the layer forward,
checksum-only) without engaging the "inherit every reader obligation" sentence that
creates it.

> A and B (identical): "A tool that modifies an existing file... without necessarily
> understanding all of its content... Verifiers and updaters are readers of the files
> they process and inherit every reader obligation."

**Byte-level rationale:** Since both sentences are identical in A and B, this is not a
difference B's rewrite introduces or removes. But it is a genuine fork with real
stakes: under the broad reading (updaters inherit R-CNF-03's full codec/filter/
sample-type coverage), a rewriter lacking one core sample type cannot be a conforming
updater when it meets such a layer and must refuse the whole file; under the narrow
reading it may carry that layer's tiles forward verbatim after checksum verification.
Same input bytes, two different sets of legally emittable output bytes — but the
identical fork exists in both editions.

**Action:** Not a fidelity defect of B. Flag to the maintainer: add one sentence to
§2.3's updater bullet (in the base text, hence in both editions going forward) stating
whether "every reader obligation" includes R-CNF-03's capability floor or only
behavioral MUSTs.

---

### Group g10 — Dropped resolution: unimplemented-type/MU=1 record is necessarily experimental-range
**Members:** cmp-verifier-01, verifierb-01, swab-04
**Consensus:** LOSS · **Byte-level:** YES · **Severity:** byte-level

A's §2.3 conforming-reader bullet (A:182-184) contains the clause: "in a conforming
file such a type is necessarily from the experimental range, since a reserved-range
type carrying MU = 1 is itself a violation." I grepped the exact fragment "necessarily
from the experimental" against both files: 1 hit in A (line 183), 0 hits in B. Control
search confirms the bullet itself exists at B:220 (found via "Conforming reader."), so
the 0-hit is a real omission, not a search failure.

> A (§2.3, R-CNF-03 bullet): "...carrying no top-level record of a type it does not
> implement with MUST_UNDERSTAND = 1 — in a conforming file such a type is necessarily
> from the experimental range, since a reserved-range type carrying MU = 1 is itself a
> violation — and none of whose values exceeds the minimum guarantees of §21's limits
> table..."
> B (§2.3, same bullet, B:220-224): "...carrying no top-level record of a type it does
> not implement with MUST_UNDERSTAND = 1 and none of whose values exceeds the minimum
> guarantees of §21's limits table (§21.9)..."

This is not merely an abstract loss. verifierb-01 is B's *own* in-document walk, built
from B alone, encountering exactly this fact pattern ("a top-level record of an
unimplemented type with MU=1") with no other stated range. Its own transcript concludes
the scenario is genuinely bimodal — reserved-range gives nonconforming (F35 at open +
F36), experimental-range gives cannot-establish (per B's §21.6 closing paragraph,
B:3915-3917: "an experimental-range top-level record type carrying MU = 1... [R-CNF-02]
makes the file conforming all the same") — and that B's text does not pin down which
applies to a bare file matching the probe's description. verifiera-01 (reading A, the
twin walk) reports no such indeterminacy, because A's clause above forecloses it
directly at the point the obligation is defined. swab-04, surveying the same drop
independently, grades it low-materiality on the theory that an implementer who
correctly chains F35/F36 with R-CNF-11's violation-priority rule reaches the same
conclusion unaided — but verifierb-01's own transcript is the counter-evidence: a
careful walk built from B alone, performing exactly that chain, still did not treat the
case as settled.

**Byte-level rationale:** Built from A alone, an implementer has a direct textual
anchor: an otherwise-violation-free file with an unimplemented-type/MU=1 top-level
record is necessarily experimental-range, so the verifier's report is forced
unconditionally to the two-branch answer (experimental → cannot establish; reserved →
impossible for a conforming file, hence moot). Built from B alone, nothing states this;
B's own walk, applying the document's other rules as carefully as it can, produces a
report that flags the fact pattern as undetermined rather than issuing the single
settled verdict A yields. That is a difference in what the verifier's actual output
text says for the same input description — a real byte/content divergence between an
A-built and a B-built verifier's report, demonstrated rather than hypothesized.

**Action:** Restore to B's §2.3 conforming-reader bullet the clause A states:
insert "— in a conforming file such a type is necessarily from the experimental range,
since a reserved-range type carrying MU = 1 is itself a violation —" at the
corresponding point (after "MUST_UNDERSTAND = 1" and before "and none of whose
values..."), matching A verbatim.

---

### Group g11 — Five cannot-establish grounds relocated §2.3 → §21.6
**Members:** cmp-verifier-02
**Consensus:** EQUIVALENT · **Byte-level:** NO · **Severity:** none

A states the five grounds inline in §2.3 (A:221-228). B shortens §2.3 to "(§21.6 names
the grounds)" and states the same five grounds, matching wording, in a new paragraph
at B:3934 (confirmed by grepping "unable to check a requirement on a capability",
present at A:221 wrapped and at B:253 and again at B:3934).

**Byte-level rationale:** Net content unchanged; only the list's location differs.

**Action:** None.

---

### Group g12 — No named ground for a file-scope resource decline
**Members:** cmp-verifier-03, verifiera-01
**Consensus:** EQUIVALENT (gap present identically in both editions) ·
**Byte-level:** NO · **Severity:** content

§21.9/[R-ERR-04] licenses a reader to decline on resource grounds "at the whole file...
as layers per file and dir_length are," before the directory can even be parsed — a
case never named among the five illustrative cannot-establish grounds. I spot-checked
§21.9's governing sentence and the five-grounds list (per g11, confirmed relocated but
unchanged) in both editions; the first ~120 lines of §21.9 were confirmed
byte-identical by the original comparator's own direct diff, which I did not need to
redo given the exact line-anchored citation given.

**Byte-level rationale:** verifiera-01 raised this from A; the identical gap exists in
B. A real implementer stake survives regardless of edition: a verifier following only
the five named grounds has no defined report shape for an oversized directory/
layer-count file it never reaches the directory of; one reading [R-CNF-11]'s general
rule literally reports cannot-establish. Since this is the same unresolved case under
either edition alone, it is not a fidelity difference between A and B.

**Action:** Not a B-specific fix. Flag to the maintainer: name the file-scope resource
decline as an explicit sixth ground (or confirm it is meant to be read as covered by
the general rule) — in the base text, which will then carry into both editions.

---

### Group g13 — Undetectable fixed-declaration change is a shared design property
**Members:** cmp-verifier-04, verifierb-02
**Consensus:** EQUIVALENT · **Byte-level:** NO · **Severity:** content

§20.3 step 4's bar paragraph and §9.7's closing Note ("Nothing here enumerates prior
commits...") are confirmed byte-identical between editions (same content as checked
under g07's §20.3 citation, plus the §9.7 Note, matching location in both files given
their fixed offset). verifierb-02 (walking B) observes that a fixed-declaration change
preserving decoded size and codec/filter framing is, by design, undetectable by any
single-pass verifier; verifier-A, walking A independently, reaches the identical
conclusion for its own V5 answer without flagging it as a separate finding.

**Byte-level rationale:** Both governing passages are verbatim-identical, so the
undetectability property holds equally under an A-built or a B-built verifier; nothing
here is a B-introduced or B-removed behavior.

**Action:** None (this is a correct, already-explicit §21.7 outcome in both editions,
not an unresolved question).

---

### Group g14 — Closed-list completeness claim for writer-conduct carve-outs dropped
**Members:** cmp-verifier-05
**Consensus:** LOSS · **Byte-level:** NO · **Severity:** content

A's first §2.3 bullet (A:166-179) names three specific writer-conduct-only carve-outs
(a set ignore-lane bit; a pre-trailer gap longer than the minimum pad; the §20.3 step 4
fixed-declaration bar) and calls them, verbatim, "the cases this text states" — a
completeness claim. I grepped "are the cases this text states": 1 hit (A:178), 0 hits
in B. B's corresponding bullet (B:207-219, read in full) states only the bare
disjunctive category, with neither the enumeration nor the completeness claim. Each of
the three instances is independently and identically recoverable at its own local
section in both editions (ignore-lane: §6.3; pre-trailer pad: §6.2; the §20.3 step 4
bar: confirmed under g07/g13).

> A: "...§20.3 step 4's bar on the fixed declarations of a layer that stores a tile
> are the cases this text states, and each is declared where it arises rather than
> enumerated here. `[R-CNF-02]`"
> B: "A writer obligation that governs conduct rather than output, or whose violation
> this specification expressly declares not to be a file-conformance violation, binds
> the writer and never makes a file nonconforming."

**Byte-level rationale:** Each named fact survives at its own section in both
editions, so no single verifier output differs on the three named instances. What is
lost is the single place in the document asserting that these three are the *only*
such carve-outs — an implementer who reads only §2.3, rather than the whole document,
has no way in B to know the list is closed, and so cannot rule out a fourth
undiscovered writer-conduct exception without reading the rest of the specification
end to end. No concrete byte emitted differs today, but the closed-list assurance
itself is gone from the one place a reader would look for it.

**Action:** Restore to B's §2.3 bullet either the enumeration-plus-completeness-claim
A states, or at minimum a forward-pointing completeness claim ("the only such cases
this specification states are..., declared where each arises").

---

### Group g15 — Redundant §20.4-scope forward-pointer dropped
**Members:** cmp-verifier-06
**Consensus:** EQUIVALENT · **Byte-level:** NO · **Severity:** none

A's updater bullet adds "— which govern every record type, not only those it does not
understand" after citing §20.4; B drops the clause. §20.4's own opening sentence
("Persistence governs every record type; only the authoritative source of the flags
differs," confirmed byte-identical in both editions per the §20.4 check under g21)
restates the same scope claim in full at its point of full definition.

**Byte-level rationale:** The dropped clause was a redundant forward-pointer; the scope
claim is fully and identically present at §20.4 in both editions.

**Action:** None.

---

### Group g16 — Minor local prose consolidations
**Members:** cmp-verifier-07
**Consensus:** EQUIVALENT · **Byte-level:** NO · **Severity:** none

Three rewordings (ignore-lane statement, pre-trailer-pad statement, the V1 unexamined/
per-requirement clause) checked; each states the identical rule under different
sentence boundaries.

**Byte-level rationale:** No behavior or report-content difference follows from either
edition alone.

**Action:** None.

---

### Group g17 — Part I / Part II architectural-independence claim dropped
**Members:** swab-01, adv-01, adv-02
**Consensus:** LOSS · **Byte-level:** NO · **Severity:** clarity

A states this claim twice: §3.3's Note (A:437-442, the entirety of §3.3) and the
Introduction's closing "Reading this document" paragraph (A:81-93, containing "Part I
alone yields a container reader"). I grepped "independent of Part" (1 hit, A:437 only)
and "container reader" (1 hit, A:89 only) — both zero in B. I confirmed B has no §3.3
heading at all: B's §3 numbering runs 3.1 (B:62), 3.2 (B:125), then directly to §2
Conformance (B:146) — no 3.3 anywhere — and B's own "How to read this document"
paragraph (B:54) covers only the document's rubric/layout-table columns, no Part I/II/
III roadmap.

> A (§3.3, entire section, a Note): "Part I (container) is independent of Part II
> (array model) by construction: no Part I structure requires decoding sample
> payloads, so appenders, and rewriters that carry a layer forward, operate on files
> whose layers they cannot decode — that independence is load-bearing for the updater
> rules of §7 and §20."
> B: absent (no §3.3 heading or body; no restatement found anywhere in B).

**Byte-level rationale:** Both A statements are inside non-normative material (the
§3.3 block is explicitly a Note; the Introduction is excluded from normative text by
§2.1/R-CNF-01 in both editions). No requirement ID or register row cites either
passage. The operative permission this rationale supports — an updater may carry
forward a layer it cannot decode — is established directly and identically by §20's
writer-tier and re-emission rules in both editions (confirmed byte-identical,
independent of this rationale). So no implementation built from B alone differs in
behavior; what is lost is the stated architectural invariant itself, stated twice in A
and nowhere in B, useful to an implementer deciding whether a container-only tool is
sound by design or by accident.

**Action:** Restore at least one instance (the §3.3 Note is the more load-bearing of
the two, since it names §7/§20 explicitly) to B, even briefly, e.g. appended to B's §3.2
or as a short Note before Part I begins.

---

### Group g18 — "preserve-verbatim is orthogonal to ignore" bridge sentence dropped
**Members:** swab-02
**Consensus:** LOSS · **Byte-level:** NO · **Severity:** clarity

A's §2.4 (A:300-304, ordinary normative prose, not a Note) states: "The same vocabulary
is used for defined conditions that are not violations (an unknown ancillary record is
*ignored*, not rejected). preserve-verbatim names an updater obligation, orthogonal to
reader outcomes: a record a reader ignores can still be one an updater preserves." I
grepped "orthogonal to reader" — 1 hit (A:303), 0 in B. §20.4 (updater's
preserve-verbatim obligation) and §21.5 (reader's ignore-record outcome) are each fully
and identically stated in both editions; what's missing is only the explicit sentence
connecting the two.

**Byte-level rationale:** Both connected rules are independently intact and identical
in both editions, so an implementation reading either edition's full text still
implements both correctly. The loss is the bridge that heads off a careless
cross-reading (that a reader-ignored record is one any tool may silently drop); it adds
or removes no requirement on bytes by itself.

**Action:** Restore the bridge sentence to B's §2.4, verbatim or close to it.

---

### Group g19 — Note disambiguating "reject" (scope of unusability, not UI) dropped
**Members:** swab-03
**Consensus:** LOSS · **Byte-level:** NO · **Severity:** clarity

A's §2.4 ends with a Note: "'Reject' prescribes the scope of unusability, not user
interface: how failure is reported is implementation technique." Grepped "prescribes
the scope of unusability" — 1 hit (A:339), 0 in B. Grepped "implementation technique" in
B: present only at the unrelated §2.1 Note (already identical in both editions), not in
connection with "reject."

**Byte-level rationale:** The Note is explicitly about implementation technique (error-
reporting mechanism), which by the specification's own framework never affects bytes
emitted or accept/reject verdicts. Its removal changes no requirement.

**Action:** Restore the Note to B's §2.4, or fold its content into the vocabulary
definition of "reject" wherever B states it.

---

### Group g20 — Worked three-row illustration of the "reach" test dropped
**Members:** swab-05
**Consensus:** LOSS · **Byte-level:** NO · **Severity:** clarity

A's §2.3 closes with a Note walking F14 (reaches, asserts only the CRC invariant), F5
(does not reach, its 128-byte floor is major-1-specific), and F15 (does not reach,
despite citing R-CNT-24, because its zero-bytes are inside the 48 a future major may
redefine). Grepped "three rows show why" — 1 hit (A:284), 0 in B.

**Byte-level rationale:** Explicitly a Note (non-normative under R-CNF-01 in both
editions) illustrating R-CNF-13's reach rule, not stating it; the rule and the
per-row determinations the Note illustrates are in the §21.2 register table, outside
this check's remit but presumably unchanged given no edit to that table is reported
elsewhere. No byte or verdict changes with or without the Note.

**Action:** Restore the worked illustration to B, as a Note at the same point in §2.3 —
useful for anyone implementing the "reach" test against a future format major, but not
required for B to decide anything A decides.

---

### Group g21 — MU=1/PE=0 for an implemented-but-unregistered type: stored bits vs. definition's flags
**Members:** writera-02, writerb-02
**Consensus:** EQUIVALENT (tension present identically in both editions) ·
**Byte-level:** NO · **Severity:** content

§20.4's governing-flags paragraph (A:3475-3501 / B, same text at offset -144) states,
identically in both editions: for a type the updater implements but this spec does not
register, "the definition it implements the type from supplies the flags, and the
stored bits never do," so "for an implemented type only the PE bit bites." R-CNT-12
itself, at §7.2 (A:1028 / B:859, byte-identical), reads on its face as unconditional:
"Writers MUST NOT emit the combination MU = 1 with PE = 0; a reader or updater
encountering it MUST treat the record as PE = 1" — and its own adjoining Note (A:1036,
identical in B) restates this as "MU = 1, whose PE bit is read as 1 whatever is
stored," again with no stated exception for the implemented-unregistered-type case.

writera-02 (from A) reads §20.4 as the controlling, later-stated carve-out and calls the
result "explicit in the text (not a contradiction)," though flags it as an easy-to-
misread fork. writerb-02 (from B) reads R-CNT-12's literal, unconditional-sounding
wording as still binding and calls the two rules a CONTRADICTION over the same bit
pattern. I re-read both passages directly in both editions: they are identical in A and
B, so whichever reading is correct, it is correct (or wrong) identically under either
edition.

**Byte-level rationale:** Not an A-vs-B difference — both texts are the same — so no
implementation built from B alone diverges from one built from A alone. But the
underlying tension is real: for a type an updater implements from an external,
unregistered definition that itself fixes MU=1/PE=0, one reading (literal R-CNT-12)
forbids ever dropping the record; the other (§20.4's "only the PE bit bites") licenses
dropping it under ordinary PE=0 treatment. Two implementations of the *same* edition,
resolving the tension oppositely, emit different legally-droppable-or-not output for
the same stored bytes.

**Action:** Not a B-fidelity defect. Flag to the maintainer to add, in the base text
(both editions), an explicit sentence scoping R-CNT-12's escalation to the case where
stored flags are authoritative (i.e., the type is not implemented by the updater),
matching §20.4's own framing.

---

### Group g22 — "Addressed tile" made explicitly generation-relative in B's glossary
**Members:** adv-03
**Consensus:** EQUIVALENT · **Byte-level:** NO · **Severity:** clarity

A's glossary bullet (A:383-384): "every tile of a layer is *addressed*" (unqualified).
B's corresponding bullet: "a tile is *addressed* in a generation if that generation's
tile index has an entry for it: the tiles of the layer's grid under the geometry that
generation declares (§11.2, §15)." Confirmed both at the same glossary entry
("addressed tile / stored tile"), and confirmed the operative sections that actually
compute the addressed-tile set for a given generation — §11.2 grid arithmetic, §15 tile
index, and §20.3's growth clause — are byte-identical between editions (not re-verified
line-by-line beyond the citation given, since no other finding in this set disputes
it).

**Byte-level rationale:** This is glossary prose carrying no requirement ID in either
edition. Because dimension extents can grow across generations, A's unqualified wording
is, read in isolation, imprecise about which generation's grid is meant; B's wording
resolves that ambiguity explicitly. But the byte-level determination of which tiles are
addressed for any concrete generation is made entirely by the three operative sections,
identical in both editions, so a reader or verifier built from either edition's
operative rules alone computes the identical addressed-tile set for any file and
generation. B's rewording changes no decision; it only states, more precisely, what A
always meant.

**Action:** None required. If anything, B's phrasing could be back-ported to A as a
clarity improvement, but no edit to B is needed for fidelity.

---

## Coverage check

22 groups, 35 member ids, each id appearing exactly once (verified by listing every
group's member_ids and checking the concatenation against the full 35-id list with no
duplicates and no omissions).

## Summary for the next phase

Only **one** group carries a demonstrated byte-level divergence between an
implementation built from A alone and one built from B alone: **g10**, the dropped
"necessarily from the experimental range" resolution. It is also the only LOSS in this
set with a `severity: byte-level` grade. Every other LOSS (g14, g17, g18, g19, g20) is
either explicitly non-normative material (Note-level rationale or illustration) or
normative connective prose whose underlying rules survive, fully and identically,
elsewhere in both editions — real content worth restoring to B for a reader who does
not read the whole document, but not something that changes a byte a conforming
implementation emits or a verdict it reaches. The remaining groups are either
relocations with no content change (g02, g03, g11, g15), different-but-equally-valid
citations of unchanged text (g04, g05, g06, g16), shared ambiguities present
identically in both editions that are not fidelity differences at all (g01, g07's
underlying issue modulo the reporter error, g09, g12, g13, g21, g22), or a reporter
error (g07) and a partial-relocation that is net-lossless (g08).
