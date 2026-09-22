# Cleanroom round 37 — triage pass: implementer consequence lens

## Disclosure of access

- Read `/Users/robertkleffner/Documents/GitHub/tarn-first-draft/spec/tarn.md` in full via targeted
  section reads: §2.1–2.5 (Conformance, lines 95–351), §5.1–5.2 (File Anatomy, 631–966
  overlap), §6.1–6.4 (Front block/Trailer, 782–966), §7.2–7.3 (Record framing/types,
  1007–1233 area), §10.2/Appendix C (registry snapshot, 4611–4637), §14.4 (Layout–type
  validity + Note, 2100–2170), §20.1–20.5 (Writing and Updating, 3126–3733), §21.6–21.7
  (Conditions that are not violations / What no check detects, 4016–4135).
- Did **not** read `docs/`, `PLAN.md`, `AGENTS.md`, `conformance/`, `spec/registry.json`,
  git history, or the web, per the brief's restriction — even though this project's own
  CLAUDE.md points to AGENTS.md, the brief's explicit access list overrides it for this task.
- Did **not** open any `transcript-<role>.md` walk transcript or quiz transcript; the spec
  text itself was sufficient to verify every claim, so I did not need a reporter's full
  reasoning trail.
- **Accidental listing disclosure:** I ran `mkdir -p .../triage-implementer && ls -la
  .../r37-round/` to confirm my own output directory existed before writing this file. The
  `ls -la` was scoped to the round directory (not to another pass's directory), but its
  output incidentally showed the *names* of two sibling directories, `triage-correctness/`
  and `triage-skeptic/` (empty at the time, per the listing's sizes). I did not open, list,
  or read anything inside either directory, and did not act on their names beyond noting
  this disclosure. This mirrors the prior-round pattern the brief warned about (an orienting
  listing run before finishing the brief), so I'm flagging it explicitly here rather than
  treating it as nothing.

## Method

For each finding: locate the exact quoted text in the spec, verify it says what the
reporter says it says, find the specific sentence(s) that either create or foreclose a
byte-level fork, and apply the test: *does resolving this change which byte sequences a
conforming implementation may emit, or must accept or reject?*

## Findings, one group each (no duplicates found across the six)

### diagrams-01 — bracket width off-by-one in §20.3 Example diagrams

Hand-verified against the raw text (lines 3407–3470). Diagram (b):

```
after  │front│ tiles │▓index▓│▓▓▓▓▓▓▓▓▓▓▓▓▓│ +tiles │ index′ │ dir₂│pad│tr₂│
                      └ old ─┘                       └───────┘ every entry, re-emitted
```

- Cell `▓index▓` = 7 chars; bracket `└ old ─┘` = 8 chars. One too many, confirmed by
  character count.
- Cell ` index′ ` = 8 chars; bracket `└───────┘` = 9 chars. One too many, confirmed.

Both this Example and §5.1's are inside blocks headed `> **Example.**`. Per §2.1,
`[R-CNF-01]`: "All text in this document is normative except: §1 (Introduction); any text
labeled *Note*, *Example*, or *Rationale*." This block is squarely inside that carve-out.
The governing normative rule for what a commit actually re-emits is §20.3 step 4's prose
(`[R-WRT-04]`, `[R-WRT-05]`), stated in words, not diagram geometry.

**Verdict:** CONFIRMED (the rendering slip is real, exactly as measured). Not byte-level —
no conforming implementation's output bytes depend on where an ASCII bracket is drawn in a
non-normative illustration. Severity: **figure**. Repair: widen each bracket's span by one
column removed (or lengthen the neighboring cell by one), whichever restores content-width
= bracket-width parity with §5.1's convention; purely cosmetic.

### diagrams-02 — trailer table's flags cell listing "updater, appender or rewriter"

Table cell (§6.2, line 838, normative — this is the main byte-layout table, not an
Example/Note/Rationale): "bits 16–31 (ignore lane) 0 from a creator, carried forward
unchanged by an updater, appender or rewriter alike, a set bit ignored."

Checked against the substantive rule, §6.3 `[R-CNT-08]`: "An updater MUST copy forward
unknown ignore-lane bits of its input file, MUST NOT clear them, and MUST NOT set any
other." That sentence binds every updater, unconditionally, with no tier carve-out. And
`[R-CNF-06]` (§2.3) closes the class: "Its tiers, the appender and the rewriter, are
§20.1's" — there is no third kind of updater anywhere in the document.

The reporter is right that the cell's list-of-three phrasing is imprecise compared to
§6.3's own idiomatic restatement two pages later ("carried forward by every updater under
this text, appender and rewriter alike," lines 912–913) — but the *rule itself* is stated
unconditionally at its normative site (§6.3), so resolving this cell's wording either way
changes no byte a conforming updater emits.

**Verdict:** CONFIRMED as a real (if minor) imprecision in normative-table prose. Not
byte-level — the document decides the substantive behavior directly and unconditionally at
`[R-CNT-08]`, independent of this cell's wording. Quote deciding it: *"An updater MUST copy
forward unknown ignore-lane bits of its input file, MUST NOT clear them, and MUST NOT set
any other."* Severity: **editorial**. Repair: reword the cell to the §6.3 idiom ("...
carried forward by every updater, appender and rewriter alike, ...") for internal
consistency; no normative effect.

### adversary-01 — R-WRT-06's refusal duty lacks the conduct-only disclaimer its siblings get

Verified §2.3 `[R-CNF-02]`'s exception list is exactly three items (ignore-lane bits,
pre-trailer gap, §20.3 step 4's fixed-declaration bar), each with its own citation, closed
by "and each is declared where it arises rather than enumerated here." `[R-WRT-06]` (§20.5,
also restated at §20.4's table first row) — "A rewriter MUST refuse to rewrite a file
carrying any record whose type it does not implement with MU = 1" — is not among them and
gets no equivalent disclaimer at its own site.

Checked whether this can actually fork bytes: `[R-CNF-02]`'s (and §2.3's opening
"Conforming TARN file" bullet's) own definition is load-bearing: *"Conforming TARN file...
File conformance is a pure predicate on bytes: it does not depend on any reader, writer, or
environment."* Because a verifier examining an output file G has no way to know which
self-declared role (rewriter vs. creator) produced it, a violation of R-WRT-06 cannot, by
itself, make otherwise-identical output bytes conforming under one label and nonconforming
under another — both a rule-abiding creator and a rule-breaking self-declared rewriter that
perform the byte-identical operation converge on the same verdict for G. So the actual
byte behavior is settled by that pure-predicate clause, even though the document never
says so explicitly at R-WRT-06's own site the way it does for its three named peers.

**Verdict:** CONFIRMED as a genuine documentation-completeness gap — the rule's status
(conduct-only vs. a permanently-unwitnessed-but-real file-conformance requirement) has to
be *derived* from the pure-predicate clause rather than read at the rule's own site, unlike
its three structural siblings. Not byte-level, for the reason above (quoted). Severity:
**register-bookkeeping** (this is precisely a completeness gap in the `[R-CNF-02]`-style
enumeration of conduct-only writer obligations, not a substantive rule change). Repair:
either add R-WRT-06 to `[R-CNF-02]`'s list, or add a one-line cross-reference at R-WRT-06's
own site noting it is conduct-only for the same reason (a self-declared role cannot affect
a pure byte-predicate).

### adversary-02 — layer-drop paragraph's MU=1 blocking condition and an implemented MU=1 sub-record

Checked the passage immediately before the table (§20.4): *"Its MU = 1 row reaches only a
type the updater does not implement — an updater implements both registered types and
understands an unregistered type it implements from its definition, modifying their
records as §20.3 and that definition provide — **so for an implemented type only the PE bit
bites.**"* This sentence directly and explicitly assigns an implemented MU=1 sub-record to
be governed by its PE bit, not by the MU=1 row's blocking language — which is exactly what
the later "one sub-record blocks the drop... a type the updater does not implement with
MU = 1" sentence restates, consistently, not in tension with it.

I also checked the reporter's own byte-level rationale, which claims this can't fork bytes
"today" because format major 1's registry assigns no MU=1 type. That premise is narrower
than the document actually allows: §20.4 explicitly contemplates an updater implementing an
*unregistered* (experimental-range) type "from its definition," and §21.6 confirms "an
experimental-range top-level record type carrying MU = 1" is a legal, conforming state
(`[R-CNT-15]`, `[R-CNT-12]`) — so an implemented, effectively-PE-governed MU=1 sub-record is
not merely a future-registry hypothetical; it is constructible under the current text via
the experimental range. That correction doesn't change the ultimate verdict, though: the
document's own governing sentence quoted above already resolves which row applies, for any
such record, registered or not.

**Verdict:** REFUTED — the document decides this directly, at the sentence quoted above,
which precedes and governs the very passage the reporter quotes. Not byte-level. Severity:
**editorial** (the table's own MU=1 row heading could still usefully carry the
implemented/unimplemented qualifier inline, since a reader consulting only the table row —
not the lead-in paragraph — could still misapply it operationally, even though the
prescriptive text is unambiguous when read as a whole).

### adversary-03 — "updater" narrowed to "appender"/"rewriter" in the PE=0 row is exhaustive

Reporter's own claim is that this is *not* a gap. Verified against §20.1: "Its tiers, the
appender and the rewriter, are §20.1's" (`[R-CNF-06]`) — updater is defined as exactly these
two tiers, no third. Also checked the asymmetric qualification the reporter flagged
("appender... in any commit it is otherwise free to make" vs. "rewriter... in any
rewrite," unqualified) against §20.5: a rewrite indeed carries far fewer independent
structural constraints than a commit (no analogous per-declaration bar), so the missing
qualifier on the rewriter clause is not an omission, it's simply that a rewrite has no
narrower "free to make" boundary to state.

**Verdict:** CONFIRMED (the reporter's own no-gap conclusion is correct). Not byte-level —
this is a positive check with no proposed change. Severity: **none**.

### adversary-04 — single-numeric-channel `layout` field change is a confirmed unwitnessed case

Reporter hand-derived that for C=1, every byte-layout quantity that could differ between
`layout=1` and `layout=2` reduces to the same formula, so a commit that changes only the
`layout` byte of such a layer is bit-for-bit indistinguishable from a correctly-declared
one at every register check. Checked this against §14.4's Note directly: *"A single-channel
numeric layer produces byte-identical tile images under either layout."* That is an
independent, directly-stated confirmation of the same claim from a different section, and
§2.3 `[R-CNF-02]` already lists "§20.3 step 4's bar on the fixed declarations of a layer
that stores a tile" as one of the three named conduct-only obligations, so this finding
does not even reach a live question about `[R-CNF-02]`'s completeness the way adversary-01
does — it's squarely inside the named, already-declared exception.

**Verdict:** CONFIRMED (matches both the changed-passage's self-description and §14.4's
independent Note; the reporter's hand derivation is sound and adds real, if unnecessary,
rigor). Not byte-level — the bar is already named as conduct-only at `[R-CNF-02]`, no
verifier accepts or rejects different bytes under either reading, and no proposed change
follows. Severity: **none**.

## Coverage

Input ids: diagrams-01, diagrams-02, adversary-01, adversary-02, adversary-03, adversary-04
(6 total). Each forms its own group (no two describe the same defect at the same site);
union of member_ids = the complete input list, no duplicates, no omissions.

## Byte-level count

0 of 6 groups fork emitted/accepted bytes. Every finding either sits inside a non-normative
Example (diagrams-01), is resolved unconditionally elsewhere in normative text
(diagrams-02, adversary-02), rests on a definitional closure that forecloses any
actor-identity-based byte fork (adversary-01), or is itself a confirmation that no
ambiguity exists (adversary-03, adversary-04).
