# Cleanroom round 37 — triage-correctness pass — working transcript

## Access disclosure

- Read `/Users/robertkleffner/Documents/GitHub/tarn-first-draft/spec/tarn.md` in full via targeted offsets (verified: total 4981 lines; read the front-matter conformance sections §2.1–§2.3, §5.1, §6.2, §6.3, §7.3, §7.4, and §20.1–§20.5, plus §14.4's Note, matching every location cited by the six findings).
- Did **not** read AGENTS.md, docs/, PLAN.md, conformance/, spec/registry.json, git history, or the web, per the brief's restriction (this overrides CLAUDE.md's generic "see AGENTS.md" pointer for this task).
- Did **not** open any walk transcript in `r37-round/out/` — I confirmed the six named transcripts exist there (`transcript-adversary.md`, `transcript-diagrams.md`, `transcript-quiz-answers.md`, `transcript-quiz-author.md`, `transcript-quiz-key.md`, `transcript-reader.md`, `transcript-register.md`, `transcript-verifier.md`, `transcript-writer.md`) via a directory listing but did not need to open any of them — every claim below was checked directly against the spec text quoted in the findings.
- **Incidental disclosure:** before listing `r37-round/out/`, I ran `ls` on its parent `r37-round/` to locate the `out` directory. That parent listing incidentally showed the names of the other two triage passes' own working directories (`triage-implementer`, `triage-skeptic`) alongside my own (`triage-correctness`). I did not open, list, or read anything inside those two directories — only their bare directory names were visible in that one listing. Flagging this per the brief's instruction to disclose any accidental exposure to the other passes' locations.

## Method

For each finding: locate the cited section/lines in `spec/tarn.md`, verify the quotation is accurate and in context, verify any requirement IDs cited actually say what the reporter claims, and independently re-derive the byte-level verdict rather than accepting the reporter's self-rating.

---

### diagrams-01 — bracket overrun in §20.3 diagrams (a) and (b)

Indexed the literal characters of lines 3413–3415 and 3431–3433 by hand (python one-liner) against the divider (`│`) column positions. Confirmed exactly as reported:
- Diagram (a): cell "A: tiles+index" occupies content columns 16–31 (dividers at 15 and 32); the "untouched" bracket runs 16→32, i.e. its closing `┘` sits on column 32, the divider — one past the cell's last content column (31). Same overshoot on the second bracket (33→46 against slack content 33–45, divider at 46).
- Diagram (b): `▓index▓` cell occupies content columns 24–30 (7 chars, dividers at 23/31); bracket `└ old ─┘` runs 24→31 = 8 characters. ` index′ ` cell occupies content columns 55–62 (8 chars, dividers at 54/63); bracket `└───────┘` runs 55→63 = 9 characters. Reporter's character counts are exact.
- Compared against §5.1's diagram (lines 667–670): there, brackets run divider-to-divider inclusive (e.g. columns 10→22 for an 11-char content cell, width = content+2), landing on *both* bounding dividers symmetrically — a different, self-consistent convention from §20.3's (content-start to far-divider only).

So there is a real, verifiable rendering inconsistency, and it's internally consistent within §20.3 (both examples do it the same way) but differs from §5.1. Checked `[R-CNF-01]` (line 105–107): "All text in this document is normative except: ... any text labeled *Note*, *Example*, or *Rationale*." Both diagrams sit inside blocks headed "**Example.**" — confirmed non-normative. Checked the governing rule is stated in prose independent of the figure: §20.3 step 4 (`[R-WRT-04]`, line 3388) and §5.1 (`[R-WRT-05]`, line 683/688) state the tile-index re-emission and untouched-extent-slot rules in ordinary sentences, not by reference to the diagram's pixel geometry.

**Verdict: CONFIRMED** (the rendering slip is real, matching reading (i) over (ii) — §5.1's brackets are symmetric, §20.3's asymmetric ones are inconsistent with that pattern and with their own cells' content width). **Not byte-level**: resolving it changes a diagram's decoration, not any byte a writer emits or a verifier checks, since the actual rule is carried entirely by prose elsewhere and the diagrams are non-normative. **Severity: figure.**

---

### diagrams-02 — trailer table's flags cell lists "updater, appender or rewriter"

Confirmed the quotation at line 838 exactly. Confirmed §20.1's closed two-tier taxonomy (line 214, `[R-CNF-06]`: "Its tiers, the appender and the rewriter, are §20.1's") — no third kind of updater exists. Confirmed §6.3's parallel, better-built sentence at lines 907–914 ("...carried forward by every updater under this text, appender and rewriter alike"), which sets off the class noun before the appositive rather than folding it into an "X, Y or Z" list. Confirmed `[R-CNT-08]` (same paragraph, tag at line 914) states the substantive obligation directly and unconditionally, binding "an updater" without tier-splitting.

**Verdict: CONFIRMED** as a real imprecision (the cell's "X, Y or Z" phrasing is more easily misread as three coordinate actors than §6.3's "X, Y and Z alike" idiom is). **Not byte-level**: `[R-CNT-08]` already governs the substance unconditionally elsewhere, and §20.1 forecloses any third updater kind, so no verifier or writer behavior turns on how this cell is parsed. **Severity: editorial.**

---

### adversary-01 — R-WRT-06 lacks R-CNF-02's conduct-only disclaimer

Confirmed `[R-CNF-02]`'s three named conduct-only exceptions verbatim (lines 166–179): §6.3's ignore-lane flag rules, §6.2's pre-trailer gap rule, and §20.3 step 4's fixed-declaration bar — "each is declared where it arises rather than enumerated here." Searched the whole document for every `[R-WRT-06]` occurrence (10 hits) and confirmed the defining text (lines 3623–3626: "A rewriter MUST refuse to rewrite a file carrying any record whose type it does not implement with MU = 1..."). Nowhere at that site, or elsewhere, is R-WRT-06 given the same "does not bear on file-conformance" disclaimer the three named siblings get.

Checked the reporter's own resolution against §2.3's conforming-file definition (line 156–158): "File conformance is a pure predicate on bytes: it does not depend on any reader, writer, or environment." This is exactly the general principle that already forecloses any actor-identity-keyed rule (rewriter vs. creator, refused vs. not-refused) from ever producing two different conformance verdicts on the *same* resulting byte sequence — a verifier examining output bytes has no way to know which actor role produced them. This independently confirms the reporter's own conclusion.

**Verdict: CONFIRMED** as a real documentation-completeness gap: R-WRT-06's status (conduct-only vs. an unwitnessed file-conformance requirement) has to be derived from §2.3's general definition rather than stated at its own site, unlike its three named peers. **Not byte-level**: §2.3's pure-predicate definition already settles that no actor-identity rule can fork a verdict on fixed output bytes, regardless of which label applies to R-WRT-06. **Severity: editorial.** Repair: add an explicit conduct-only (or "does not bear on file-conformance") disclaimer at R-WRT-06's site, matching the treatment §6.3/§20.3 give their three examples, or fold R-WRT-06 into `[R-CNF-02]`'s enumerated list.

---

### adversary-02 — layer-drop paragraph's blocking condition and implemented MU=1 sub-records

Confirmed the quoted lead-in ("Its MU = 1 row reaches only a type the updater does not implement... so for an implemented type only the PE bit bites") immediately precedes the table (§20.4), and the quoted layer-drop paragraph ("One sub-record blocks the drop, a sub-record of a type the updater does not implement with MU = 1...") follows the table, explicitly citing "(the table's first row)" as its basis. Confirmed `[R-CNT-12]`'s general statement (line 1038, in the Note under §7.4) that MU=1 records read PE as 1 "whatever is stored" — this is stated as a general encoding fact, not restricted to unimplemented types, which is what makes the reporter's fork worth taking seriously.

However, tracing the table's own scoping sentence through to the layer-drop paragraph: the paragraph's blocking clause is not an independently-drafted rule but an explicit citation back to "the table's first row," and that row is scoped, one sentence earlier, to apply "only [to] a type the updater does not implement." Read together (not in isolation from the table lead-in), the blocking condition is exhaustively and unambiguously restricted to unimplemented MU=1 sub-records; an implemented one — registered or not — is governed by the PE-only rows, and is swept away by the layer-drop's "whatever their PE bits" clause with no contradiction. Also confirmed via §7.3 (lines 39–47 of that block) that format major 1's registry currently assigns MU=0 to both registered types, so no registered type can hit this today; the scenario is reachable today only through an updater implementing an unregistered/experimental type under its own external definition (§20.4's "the definition it implements the type from supplies the flags" clause) — a case this specification's own checks cannot examine, since such a definition is by construction outside its registry.

**Verdict: CONFIRMED** as an accurately identified misreading risk (the table's MU=1 row *label* alone, without the qualifying sentence above it, invites exactly the wrong generalization the reporter names), but **not a genuine two-reading ambiguity** in the combined text — the qualifying sentence is dispositive and the layer-drop paragraph explicitly inherits it. So I'd grade this **PARTIAL** relative to the reporter's own "AMBIGUITY" framing: the real defect is a *presentation* risk (row label omits the qualifier it needs when read out of the immediate context), not an unresolved fork of readings. **Not byte-level**, on two independent grounds: the qualifying sentence forecloses the naive reading for a reader who reads the whole subsection, and no MU=1 type is registered today for the scenario to bite on regardless. **Severity: editorial.** Repair: add "(unimplemented only)" (or equivalent) directly to the table's MU=1 row label, so the constraint survives being read in isolation from its lead-in sentence.

---

### adversary-03 — table's appender/rewriter narrowing is exhaustive (self-reported non-defect)

Confirmed §20.1's closed two-tier taxonomy again (line 214, `[R-CNF-06]`) and the quoted table row (PE=0 row, in §20.4's table) narrowing "an updater" to "an appender... and a rewriter..." Confirmed this is a complete restatement, not an omission — there is no third updater tier anywhere in the document. Checked the phrasing asymmetry the reporter flagged (appender's licence qualified, rewriter's not) against §20.5's own rewrite-obligations text (lines 3600–3606: pad and barriers "both, not one — are owed here as they are of a creator") and found no basis for a stricter reading on the rewriter's clause; rewrites indeed carry fewer independent per-commit constraints than a commit does, matching the reporter's explanation.

**Verdict: CONFIRMED** — the reporter's own conclusion (this is a confirmation, not a defect) is correct on this text; I found nothing that reopens it. **Not byte-level.** **Severity: none** — no repair needed.

---

### adversary-04 — single-numeric-channel `layout` field is a confirmed unwitnessed fixed declaration (self-reported non-defect)

Confirmed the quoted "changed passage" verbatim against lines 3305–3319 of §20.3 step 4 (word-for-word match, including the register-row list T3/T14/T21/T22/T4/T5/T2 and T17/T24/T25). Confirmed §14.4's Note verbatim (lines 2146–2148): "A single-channel numeric layer produces byte-identical tile images under either layout." This is exactly the document's own independent statement of the fact the reporter re-derived by hand. Reconfirmed `[R-CNF-02]` names this exact bar (§20.3 step 4's fixed-declaration bar) as one of its three conduct-only exceptions (line 178), so it does not bear on file-conformance regardless of the arithmetic.

**Verdict: CONFIRMED** — an accurate, independently-verifiable confirmation of a fact the spec already states about itself. **Not byte-level** (the bar is conduct-only per `[R-CNF-02]`, and the worked arithmetic only reinforces a documented equivalence, it does not expose any new fork). **Severity: none** — no repair needed; this is a positive check, not a defect.

---

## Coverage

Six input ids: diagrams-01, diagrams-02, adversary-01, adversary-02, adversary-03, adversary-04. Each forms its own group (no duplicates found across the six; each is textually distinct in location and content). All six accounted for, one group per id, zero left over.

## Notes

No coverage gaps. No group in this pass was judged byte-level. All six items were checked against the primary spec text directly (not merely against the reporters' own quoted excerpts), including cross-references (`[R-CNF-01]`, `[R-CNF-02]`, `[R-CNF-06]`, `[R-CNT-08]`, `[R-CNT-12]`, `[R-CNT-22]`, §5.1, §7.3, §7.4, §20.1, §20.5) that the reporters cited but did not always quote in full.
