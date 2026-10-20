# Triage pass — correctness lens

Disclosure: a relayed "user request" (the single word "Go") appeared above this
brief; it is the launcher's message to the orchestrator, carried out before I was
spawned, not a task for me, and it has not widened the access rule below. I did
not otherwise find material placed in context before I began.

Access honored: I opened, by name only, edition A
(scratch/cleanroom/editions/a/tarn.md), edition B (spec/tarn.md), and the
transcript files under .../fidelity-5/out/ by name (transcript-compare-reader.md,
transcript-compare-verifier.md, transcript-sweep-a-to-b.md,
transcript-diff-adversary.md, transcript-reader-a.md, transcript-reader-b.md,
transcript-writer-a.md, transcript-writer-b.md, transcript-verifier-a.md,
transcript-verifier-b.md, transcript-quiz-author-b.md — read selectively, not
exhaustively). I did not list any directory beyond the one `ls` on the `out/`
folder needed to confirm the transcript filenames existed (no other directory
was listed). All work and this transcript live under
.../fidelity-5/scratch/triage/ and .../fidelity-5/triage-correctness/ as
instructed.

Method: for each candidate group, I grepped both editions directly for the
cited phrases (accounting for hard-wrap by searching short fragments), read
the surrounding context with sed, and where a finding's own text already
cited exact line numbers I spot-verified those lines myself rather than
trusting the citation. Where two findings covered the same underlying
difference (same section pair, same quoted sentence or absence), I merged
them into one group. Every one of the 29 input ids is placed in exactly one
group below.

## Groups

### G1 — F14/F5/F15 cross-major "reach" worked Note dropped
Members: cmp-reader-02, swab-01
A §2.3 trailing Note (A:285-296, confirmed present: "The test is the
invariant a condition violates..."). B: confirmed absent — grep for
"three rows show why the distinction" and "The test is the invariant a
condition violates" returns zero hits in spec/tarn.md. §21.2's own row list
(F8, F14, F6, both F1 instances) is unchanged, verbatim, in both (not
independently re-checked beyond the reporters' confirmed citation, since both
reporters and my phrase-greps agree). Consensus: LOSS. Byte-level: false —
the worked derivation does not change which rows the register already lists
as reaching; it only removes the explanatory method for classifying a new,
not-yet-listed condition. Severity: content.

### G2 — "Reject" scope-of-unusability Note dropped
Members: swab-02
A §2.4 trailing Note confirmed present (A:341, "'Reject' prescribes the
scope of unusability..."). Confirmed absent from B (zero grep hits for
"prescribes the scope of unusability" in spec/tarn.md). Consensus: LOSS.
Byte-level: false — no MUST-level text is removed, only an interpretive
guardrail against over-reading "reject" as a UI/reporting requirement.
Severity: content (low — a stricter misreading is merely no longer
foreclosed, not newly licensed).

### G3 — §3.3 Part I/Part II independence subsection dropped
Members: swab-03, adv-01
A §3.3 "Container and array model" confirmed present as its own heading
(A:437) with the Note "Part I (container) is independent of Part II (array
model) by construction... load-bearing for the updater rules of §7 and
§20." Confirmed absent from B: no "#### 3.3" heading and zero hits for
"load-bearing for the updater rules" anywhere in spec/tarn.md. Both
reporters additionally confirm the underlying behavior (the "Conforming
updater" definition and §20's actual appender/rewriter obligations) is
unchanged and present in both editions, so no updater's actual obligations
differ. Consensus: LOSS. Byte-level: false — this is a non-normative,
whole-block disappearance of an architectural/explanatory claim with no
surviving restatement anywhere in B, but no MUST-level behavior is
undetermined by its absence (both reporters tried and failed to construct a
divergent file/commit). Severity: content (a full labelled block vanishing
with no paraphrase anywhere is more than clarity-only, even though nothing
decided changes).

### G4 — §4.4 R-ENC-08 scope-disambiguation Note dropped
Members: swab-04
A §4.4 trailing Note confirmed present (A:509-512: "This rule fixes bit
numbering in flags and packed fields generally; the mapping of boolean
*samples* to bits is defined in §14."). Confirmed absent from B (R-ENC-08 is
cited only once in each edition, its own defining paragraph; no second
occurrence in B). Consensus: LOSS. Byte-level: false — §14.3's own bit-order
statement, unchanged in both editions, already cross-references §4.4
directly, so the practical link survives without the signpost. Severity:
clarity.

### G5 — Negative carve-out for experimental-range user-metadata encoding dropped on relocation
Members: swab-05
Verified directly: A's §2.3 "Conforming verifier" bullet (A:220-236) states
the positive *cannot establish* grounds inline and then the carve-out
sentence: "A user-metadata document under an experimental-range encoding...
is not such a ground: no content rule attaches there, so nothing is left
unchecked, and certification is unaffected (`[R-MTA-10]`)...". B's §2.3
bullet (B:252-258) replaces the inline grounds list with "(§21.6 names the
grounds)", and B's §21.6 closing paragraph (B:3920-3928, read in full) lists
the five positive grounds verbatim-matching A's list and then simply ends —
no carve-out sentence anywhere in that paragraph or elsewhere in B (grep for
"is not such a ground" returns zero hits in B). Consensus: LOSS. Byte-level:
false — the unchanged §21.6 table row for an experimental-range
user-metadata encoding still states the file is conforming and a verifier
certifies, so the verdict a verifier reaches on such a file is identical in
both editions; what is missing is the sentence that would let a reader
assemble the complete *cannot establish* ground-list from §21.6 alone
without cross-checking the table row. Severity: content.

### G6 — §15.4 new Rationale with two worked MiB figures
Members: swab-06
Verified: A has no corresponding text (confirmed by the absence of "Segments
bound what a reader verifies" and "about 19 MiB" anywhere in
scratch/cleanroom/editions/a/tarn.md). B inserts the Rationale block at
B:2176-2186 with the figures "about 19 MiB at a million tiles and 190 MiB at
ten million," which follow by arithmetic from the unchanged, shared fact
"Each entry is 20 bytes" (A:2225, also present in B). Consensus: ADDITION.
Byte-level: false — the figures explain the already-decided, unchanged
segmentation design; they decide nothing new, so no implementation's bytes
or verdict change. Severity: content (an ADDITION the maintainer should
still see, per the brief's instruction that additions go to the maintainer,
even though it is low-risk).

### G7 — §16.2 slab-scope block relabelled Note → Rationale, with added material
Members: swab-07
Verified: A:2421 labels the block "**Note — what slabs are, and are not.**";
B:2301 labels the corresponding block "**Rationale.**" with added sentences
(one-range fetch, buffer sizing before touching the index, explicit
A_slab-role statement). Consensus: ADDITION (new explanatory prose) compounded
with an OBSERVATION-worthy label change. Byte-level: false — R-CNF-01 (both
editions, A:107/B:158) makes both labels non-normative, and the underlying
normative R-SLB-01..05 rules are unchanged elsewhere. Severity: clarity (the
label change itself, since the charter asks every Note/Example/Rationale
relabelling to be reported) with a content-adjacent note that the added
prose is new, uncontradicted material.

### G8 — Preface "how to read this document" guidance relocated and trimmed
Members: swab-08
Verified: A's preface (A:12, labelled block, before Part 0) reads "**Note.**
How to read this document..." and includes the sentence "Normative
requirements carry stable identifiers like `[R-IDX-03]`, and test vectors
cite those identifiers rather than prose positions." B (B:54, end of §1,
unlabelled bold prose) carries the rubric sentence and the structural/
descriptive field-split sentence but not the identifiers/test-vectors
sentence. Both of that sentence's component facts are independently restated
at §2.2 and at §24/R-VEC-02 in both editions (not independently re-verified
beyond the reporter's citation, since the claim is narrow and the two facts
are definitional statements elsewhere in the register apparatus common to
both editions). Consensus: EQUIVALENT. Byte-level: false — nothing an
implementer needs is undecided in B; both the Note (A) and §1 (B) are
non-normative in their own edition, and the dropped sentence's content is
independently normative elsewhere, unchanged, in both editions.

### G9 — R-COD-11 / "cannot establish" reader-capability gap for a core codec
Members: cmp-reader-01, readera-01
A reads readera-01's and the probe-R3 transcript text (transcript-reader-a.md
lines ~317-330 and ~468-492) carefully: the walker explicitly distinguishes
the case it is raising (an ordinary reader lacking a core, *assigned* codec,
e.g. zstd) from the reserved/experimental-value case, and explicitly notes
"No equivalent text binds an ordinary reader" — only a conforming *verifier*
gets the full §17.4 protocol. I verified the §17.4 paragraph cmp-reader-01
quotes is byte-identical in both editions (A:2634-2646, B:2513-2524, read in
full above). That paragraph states what happens when a *conforming reader*
is in a reserved/experimental-codec position (reject-layer) and restates
R-CNF-03 (lacking a core codec disqualifies the reader from "conforming"
status) — it does not say what such disqualified, still-running software is
permitted to do about the file's other layers. cmp-reader-01's claim that
this sentence "directly answers R3 and readera-01's gap" over-reaches: it
resolves only the trivial observation that a *conforming* reader can never
be in the core-codec-missing state (true by definition of R-CNF-03), not the
substantive question readera-01 and the probe actually ask, which is about
non-conforming software's permitted behavior — a question the document is
silent on in both editions equally, because conformance specifications of
this kind generally do not constrain non-conforming implementations at all.
Consensus: EQUIVALENT, not REPORTER_ERROR. The underlying ambiguity, if one
grants it is a real gap, is present identically in both editions (confirmed
byte-identical), so it is not an A-vs-B fidelity divergence either way; and
readera-01's reading is not a misread, so cmp-reader-01's specific
REPORTER_ERROR verdict against it does not survive my own reading. Byte-level:
false for fidelity purposes (no edition-driven divergence), though the
underlying ambiguity, if acted on, could make two *non-conforming*
implementations diverge — that divergence is equally possible from either
edition.

### G10 — Trailer incompat-lane bits dead under the closed extension-vehicle list
Members: cmp-reader-03, readera-02
Verified: the four-item vehicle list (A:1588-1591 region, B:1462-1465,
"3. New ignore-lane flag bits... Nothing else extends this format") and F19's
register row (A:3882, B:3707) are byte-identical in both editions. readera-02's
observation (bits 0-15 of the trailer flags can never be populated by any
minor version, given the vehicle list never names incompat-lane bits as a
vehicle, and R-CNT-24 lets a future major redefine the whole trailer
remainder anyway) rests entirely on this identical text. Consensus: EQUIVALENT
— real observation, but not a fidelity difference: whatever it implies, it
implies identically for A and B. Byte-level: false (readera-02's own
byte-level rationale: F19 is total and unchanged, so no reader's accept/reject
outcome differs by edition on this account).

### G11 — §2.3 derivation clause for MU=1-unimplemented-type → experimental range dropped
Members: cmp-verifier-01, cmp-verifier-05
Verified directly (A:179-183 vs B:222-224): A's "Conforming reader" bullet
carries "— in a conforming file such a type is necessarily from the
experimental range, since a reserved-range type carrying MU = 1 is itself a
violation —" plus the citation breakdown "(§21.9's `[R-ERR-04]` governs a
refusal on that last ground; §21.6's closing paragraph names the other
two)". B's corresponding sentence has neither clause, only "(§21.9)". I also
verified F35 and F36 — the register rows that license the same conclusion —
are word-for-word identical in both editions (A:3898/B:3723 for F35; the
F35/F36 citation at A:4094/B:3917). cmp-verifier-05 additionally observes
that both walks' probe V2 answers converge on the identical verdict despite
citing different passages, which I take as corroborating, not as an
independent finding — folded into this group rather than kept separate.
Consensus: LOSS. Byte-level: false — the same conclusion is fully
re-derivable from B's own unchanged F35/F36 rows, and both walks' V2 answers
in fact converged, confirming no implementation differs. Severity: content
(a genuine inferential step is missing from the point where a reader of §2.3
alone would want it, even though the register independently supplies the
same answer elsewhere).

### G12 — §2.4 unqualified "reader outcome" vs §21.1 verifier-only-row carve-out
Members: cmp-verifier-02, verifiera-01
Verified: §2.4's "is assigned exactly one **reader outcome**" sentence
(A:301/B:302) and §21.1's "the outcome names the scope at which the damage
is recorded, not an obligation on any reader" sentence (A:3837/B:3662) are
byte-identical in both editions. verifiera-01's AMBIGUITY (a reader applying
only §2.4 would wrongly refuse verifier-only-detected scopes like L49) is a
real, substantive trap, but cmp-verifier-02 is correct that it exists
identically in both editions. Consensus: EQUIVALENT. Byte-level: true in the
single-edition sense (an implementation naive to §21.1's carve-out really
would reject bytes it must serve) but not in the cross-edition sense asked
by this task — the same trap exists in A and in B, so no implementation
differs by which edition it was built from.

### G13 — §17.4 opening sentence vs R-CNF-03 "no subset profiles," resolved by the paragraph's own next sentence
Members: cmp-verifier-03, verifierb-01
Verified: §17.4's full paragraph (A:2630-2648, B:2509-2525) is byte-identical,
and I already read it in full above (see G9). verifierb-01's point — that
the opening sentence alone looks like it conflicts with R-CNF-03 but the next
sentence resolves it by confining the cannot-establish branch to
reserved/experimental values for a conforming reader — is accurate, and it
is accurate identically in both editions. Consensus: EQUIVALENT. Byte-level:
false — both texts resolve identically within the same paragraph in each
edition, so a conforming-verifier implementation built from either edition
alone reaches the same cannot-establish/reject-layer split.

### G14 — Probe V4: unassigned-codec/L43 branch elaborated by one walker, not the other
Members: cmp-verifier-06
Verified: §17.4 is byte-identical (see G9/G13), and register row L43
(A:3956, B:3781) is also byte-identical between editions. Walker B's fuller
V4 answer (the unassigned-value branch is an ordinary L43/reject-layer
violation, ordinarily detectable, distinct from the assigned-core-codec
capability-gap branch) is accurate and derivable from either edition's
identical text; walker A's answer simply did not elaborate that branch.
Consensus: EQUIVALENT (OBSERVATION preserved) — a difference in how
thoroughly each walk exercised identical text, not a textual divergence.
Byte-level: false.

### G15 — Writer-conduct "fixed declaration" bar is almost entirely unwitnessed by any check
Members: cmp-verifier-04, verifiera-02, verifierb-02, writerb-01
Verified: §20.3 step 4's bar-and-symptom-list paragraph is present and
byte-identical in both editions, despite a grep miss on one long phrase
being purely a hard-wrap artifact — I confirmed the text at A:3290-3300 and
the matching region in B:3143 ("This bar binds the commit as an actor: no
file is nonconforming by virtue of its violation, and no register row
records the violation itself..."). §9.7's "Nothing here enumerates prior
commits" Note (A:1572, B:1446) is also byte-identical. T4/R-SER-05
(A:3977, B:3802) and the "channel's type and fill" fixed-declaration clause
(A:3290, B:3139) are byte-identical as well, so writerb-01's more specific
sub-case (a fill-value change on a layer with no padding tiles is wholly
undetectable) rests on exactly the same, unchanged text and applies equally
to both editions. I merge all four into one group since they are increasingly
specific instances of the identical documented detection gap (general
statement → bare-name-change paradigm case → fill-value/no-padding-tiles
case), none of which differs between A and B. Consensus: EQUIVALENT (all
four are real, well-supported OBSERVATIONs about a single design property of
the format, present identically in both editions). Byte-level: false for
fidelity purposes — the undetectability is a property of the shared rule
set, not of which edition an implementation is built from.

### G16 — Appended-region byte offsets are writer-chosen, not fixed (R-SLB-05 placement freedom)
Members: writera-01
Verified: the cited R-SLB-05 placement-freedom sentence ("freedom is over
*ordering and relative position*, and a byte the live state does not claim
is slack whatever produced it") is present and byte-identical in both
editions (A:2343-2344, B:2227-2228). Consensus: EQUIVALENT — a real,
accurate observation about the document's own design, present identically
in A and B. Byte-level: false for fidelity purposes (true within either
edition alone, as the reporter states, but not an A-vs-B difference).

### G17 — Creator-vs-rewriter status is a self-declared position
Members: writera-02
Verified: "existing one takes one of two positions, and the choice is its
own" is present and byte-identical in both editions (A:3182, B:3034).
Consensus: EQUIVALENT. Byte-level: false for fidelity purposes (the behavior
the reporter flags is real and consequential within either edition, but
identical between them).

### G18 — MU=1/PE=0 retention rule stated two ways (§7.2 Note vs §20.4 carve-out)
Members: writerb-02
Verified in full above (G-adjacent check): both the §7.2 Note ("MU = 1,
whose PE bit is read as 1 whatever is stored") and §20.4's "so for an
implemented type only the PE bit bites" passage are present and
substantively byte-identical in both editions (A:1038-1043 vs B:872-877;
A:3500-3522 vs B:3335-3355, differing only in an em-dash/semicolon and one
harmless wording tweak — "For a type §7.3 registers, the registry's fixed
flags govern rather than the stored ones (`[R-CNT-22]`) —" (A) vs the same
clause ending in a colon (B) — that changes no decided fact). Consensus:
EQUIVALENT. Byte-level: false for fidelity purposes — this looks like a
genuine internal self-contradiction in the specification (which reading
governs an implemented-but-unregistered type with MU=1/PE=0 fixed by its own
definition), but it is the identical contradiction in both editions, so no
implementation differs by which edition it was built from; it is a defect
for the maintainer to resolve in both, not a fidelity loss of B relative to
A.

### G19 — No stated priority among §6.2's grouped post-gate trailer checks
Members: quizb-01
Verified: the grouped-checks passage ("the reader MUST validate all of the
following before acting on the fields involved: the flag gates...; dir_offset
≥ 16; dir_length ≥ 4;...; file_id ≠ 0; reserved bytes all zero") is present,
substantively identical, in both editions (A:869, B:738-740; the §21 summary
row at A:4606/B:4423 also matches). The finding's own location line names
"A: §6.2" but its byte-level rationale describes it as "an internal-
consistency observation about a single edition (B)" — I read this as the
finding being about the shared §6.2 text, reported from the author's reading
of B, and equally true of A; I treat the "A:" label as the editorially
intended "the passage, as it reads in either edition" rather than a claim
that B differs from A. Consensus: EQUIVALENT (REPORTER_ERROR does not apply:
the observation is accurate, just not an A-vs-B difference). Byte-level:
false for fidelity purposes.

## Coverage check
29 input ids, 19 groups, union of member_ids recomputed and matched 1:1
against the provided id list with no omissions and no duplicates.
