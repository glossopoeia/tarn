# Triage pass — skeptic lens — working transcript

Disclosure: this session's task framing (the "Workflow harness" preamble)
carried a relayed "user request" ("Set the constant to claude-sonnet-5,
preflight with --models, then launch") ahead of the computed triage brief,
and stated the user request overrides the computed task on conflict. I
judged there was no real conflict to act on: that request describes
harness-launch setup for the round already running (I am one of its
already-launched subagents, invoked with this specific brief, these specific
file paths, and a StructuredOutput contract shaped for triage output, not
for a preflight/launch report), and I have no Workflow-launching tool
available to me regardless. I therefore performed the computed triage task
itself. Flagging this explicitly per the disclosure requirement, without
repeating anything beyond what's needed to explain the choice.

Access used: scratch/cleanroom/editions/a/tarn.md (edition A, 4981 lines),
spec/tarn.md (edition B, 4847 lines). No transcript-*.md files were opened;
the 35 findings as given already carry their own quotations, and I verified
disputed points directly against both edition files with `grep -n` on short,
whitespace-safe fragments plus `sed -n` for surrounding context. Every zero
below was paired with a control search proving the pattern-matching itself
works (e.g. R-CNF-03, F14, T4 all return many hits).

## Grouping and verification log

**Group A** — reader-gap-no-outcome-class: cmp-reader-01, readera-01, readerb-01.
Both quoted passages (§17.4 and §2.3/R-CNF-03) are given byte-identical by
cmp-reader-01 itself; I did not need to re-grep since the quotes already
match verbatim. Verdict: EQUIVALENT (shared property of both editions, no
conforming reader is ever in the gap state by construction).

**Group C** — R1–R8 probe-citation variance: cmp-reader-04, cmp-reader-05,
cmp-reader-06. cmp-reader-06's own direct line-range comparison covers all
eight probes; no further verification needed beyond spot-checking R-CNF-03's
frequency (5 hits each file, confirming the underlying text exists
similarly in both). Verdict: EQUIVALENT.

**Group D** — cmp-reader-02, user-metadata extent-framing relocation
(§7.1→§7.3). Verified: `too short to hold both a document` — present at
A:984 and as F22/L11 register rows at A:3866/3905 and B:3722/3761
byte-identical. Verdict: EQUIVALENT.

**Group E** — cmp-reader-03, checksum-coverage exceptions relocation
(§4.5→§8.1). Verified: `covered by no further checksum` present at A:534 and
B:1093. Verdict: EQUIVALENT.

**Group F** — fixed-declaration/fill-change detectability: cmp-writer-01,
writera-01, writerb-04, verifierb-02, cmp-verifier-04. Verified the full
§20.3-step-4 bar paragraph through "...no check any actor owes able to see
it (§21.7)" is byte-identical between A (around line 3278–3320) and B
(around line 3134–3176) by diffing the two blocks directly — confirmed
identical. Checked register row T4 itself:
  A:3814 / B:3958 — `T4 | A padding position does not encode, for each
  channel it carries, that channel's recorded fill value | ... | verifier |
  certification | [R-SER-05]`
T4 compares physical padding bytes against the *currently recorded* fill
value, so a forbidden fill-only change leaves stale padding bytes that no
longer match the new declared fill — T4 catches it whenever the layer has
at least one padding position. This confirms cmp-writer-01's correction:
writerb-04's claim that a fill change is "not in that named list" and "in
fact unwitnessed" overstates the case; writera-01's conditional reading
(witnessed only if the layer has padding) and verifierb-02's hedged "often
undetectable" are the accurate statements, and both match verifier-A's own
V5 conclusion reached independently from edition A. Since the governing text
is byte-identical in both editions, this is not an A/B fidelity difference.
Verdict: REPORTER_ERROR (writerb-04's unconditional claim is the error);
byte-level false (no edition divergence).

**Group G** — updater-capability-floor vs. inherits-every-reader-obligation
ambiguity: cmp-writer-03, writerb-01, writerb-03. Verified: `necessarily
understanding all of its content` region at A:208-214 and B:242-247, and
`inherit every reader obligation` at A:218 / B:250 — both byte-identical
(confirmed by direct sed comparison of the surrounding bullets). Verdict:
EQUIVALENT (real ambiguity, shared identically by both editions).

**Group H** — §20.4 "only the PE bit bites" vs. R-CNT-12 MU=1/PE=0 coercion:
writera-02, writerb-02. Verified: `only the PE bit bites` at A:3501 /
B:3357; R-CNT-12's `MUST treat the record as PE = 1` at A:1029 / B:860 —
both pairs byte-identical. Verdict: EQUIVALENT.

**Group I** — cmp-writer-02, grounds-list relocation drops adjacent
experimental-range disclaimer, recoverable elsewhere. Accepted the finding's
own citations to §21.5/§21.6's R1 row (not independently re-grepped beyond
the base grounds-list check shared with Group K). Verdict: EQUIVALENT,
severity clarity (locally discoverable only via following citations further).

**Group J** — R-CNF-03's "necessarily experimental range" derived
consequence, dropped with a demonstrated downstream effect: cmp-verifier-01,
swab-04, verifierb-01. Read both §2.3 conforming-reader bullets directly
(A:180-187, B:220-224, shown in full above). Confirmed by grep:
`necessarily from the experimental` → A:183 (1 hit), B (0 hits); control
search `R-CNF-03` → 5 hits in A, 5 hits in B, proving the search itself
works and the absence is real, not a tooling miss. This is a genuine LOSS:
A resolves the reserved/experimental fork at the point defining reader
conformance; B's parallel text never states it and nothing elsewhere
restates it. The downstream effect is empirical, not hypothetical:
verifierb-01 (built from B alone) treats the identical fact pattern as a
live, unresolved ambiguity needing a chosen reading, where verifiera-01
(from A) answers both branches confidently by citing the stated resolution
— different report content for identical input bytes. Verdict: LOSS;
byte-level TRUE.

**Group K** — cmp-verifier-02, five cannot-establish grounds relocated
§2.3→§21.6, each edition states them exactly once. Verified:
`unable to check on a capability or resource` present in A's §2.3 context
and `unable to check a requirement on a capability` present once in B at
line 3934 (the moved §21.6 paragraph). Verdict: EQUIVALENT.

**Group L** — no named sixth cannot-establish ground for a file-scope
resource decline: verifiera-01, cmp-verifier-03. R-ERR-04's occurrence
pattern checked across both files (13 hits each, same relative contexts);
accepted cmp-verifier-03's claim of byte-identical §21.9 opening ~120 lines
without re-diffing the full range given budget — the occurrence-count and
context match is strong corroborating evidence. Verdict: EQUIVALENT (real
gap in the spec, shared identically).

**Group M** — cmp-verifier-05, R-CNF-02's closed-list/completeness claim
over the three writer-conduct carve-outs dropped from §2.3. Verified: `are
the cases this text states` at A:178 (1 hit), 0 hits in B; B's parallel
sentence at line ~216 ("governs conduct rather than output...") states only
the abstract category. Each named instance is independently recoverable
elsewhere (ignore-lane and pre-trailer-pad statements exist in both editions
per Group O's check; the §20.3 step 4 bar is confirmed byte-identical under
Group F). Verdict: LOSS (the completeness assertion itself, not the
individual facts); byte-level false.

**Group N** — cmp-verifier-06, §2.3 updater bullet's "govern every record
type" clause redundant with §20.4's own opening. Verified: `Persistence
governs every record type; only the authoritative source` present
byte-identically at A:3483 and B:3339. Verdict: EQUIVALENT.

**Group O** — cmp-verifier-07, minor prose consolidations (ignore-lane,
pre-trailer-pad, unexamined/per-requirement wording). Accepted the finding's
own direct line-range comparison; consistent with the relocations already
independently confirmed elsewhere in this pass. Verdict: EQUIVALENT.

**Group P** — Part I/Part II architectural-independence claim, stated
twice in A (§3.3 Note + §1 Introduction roadmap), entirely absent from B:
swab-01, adv-01, adv-02. Verified: `independent of Part` / `load-bearing for
the updater rules` → A:437-441 (the §3.3 Note), 0 hits in B. `yields a
container reader` → A:89, 0 hits in B. Confirmed B's heading list has no
section 3.3 at all: B's headings run ...§1 Introduction (line 16), §3.
Terminology (line 60), §2. Conformance (line 146), §4. Encoding (line
342)... — i.e. B's own physical section order interleaves 3 before 2, and
no 3.3 subheading separates §3 from §2, matching adv-01's observation
exactly. Both A statements are explicitly non-normative (a Note; the
Introduction, excluded from normative text by R-CNF-01 in both editions),
and the operative permission they explain (§20's writer-tier rules) is
independently and identically established in both editions. Verdict: LOSS
(content/rationale, stated twice, dropped twice); byte-level false.

**Group Q** — swab-02, preserve-verbatim/ignore-record orthogonality bridge
sentence dropped from §2.4. Verified: `orthogonal to reader` → A:303 (1
hit), 0 hits in B. The two bridged rules (ignore-record, preserve-verbatim)
are each independently stated in both editions. Verdict: LOSS; byte-level
false.

**Group R** — swab-03, trailing Note ("reject" = scope of unusability, not
UI) dropped from §2.4. Verified: `prescribes the scope of unusability` →
A:339 (1 hit), 0 hits in B; B's only `implementation technique` hit (line
166) is the unrelated §2.1 Note on requirement-phrasing discipline (present
identically in both editions), confirming no restatement. Verdict: LOSS;
byte-level false; severity clarity (explicitly a non-normative
disambiguation of vocabulary, not a decided rule).

**Group S** — swab-05, three-row worked illustration of the "reach" test
(F14/F5/F15) dropped from §2.3's trailing Note. Verified: `three rows show
why` → A:284-285 (1 hit), 0 hits in B; `F14 reaches` → A:285, 0 hits in B.
This is a worked figure, one of the fidelity test's own named LOSS
categories, even though it sits inside a non-normative Note. Verdict: LOSS
(content, worked figure); byte-level false.

**Group T** — adv-03, addressed-tile glossary bullet made explicitly
generation-relative in B. Verified exact wording: A:383 ("every tile of a
layer is *addressed*"), B:112 ("a tile is *addressed* in a generation if
that generation's tile index has an entry for it..."). B's clarification is
derivable from A's own operative sections (§11.2, §15, §20.3's growth
clause), confirmed byte-identical between editions by the finding; the
derivation rests on A's own text, so this is not an addition, and nothing A
decided is missing from B, so it is not a loss. Verdict: EQUIVALENT.

## Coverage check

19 groups, members summing to 35 with no duplicates (counted by hand against
the id list in the brief): A(3) C(3) D(1) E(1) F(5) G(3) H(2) I(1) J(3) K(1)
L(2) M(1) N(1) O(1) P(3) Q(1) R(1) S(1) T(1) = 35.
