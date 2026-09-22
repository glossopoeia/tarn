# 0133. The readable edition, and the fidelity process that guards it

- Status: Proposed (drafted 2026-09-22 at the maintainer's request; in force
  on the maintainer's acceptance, and nothing here touches spec text)
- Covers: how the specification is edited after G3; the two editions and
  which governs; the equivalence contract between them; the fidelity round;
  how the readable edition is accepted and what becomes of the reference;
  what the repair-audit convention (ADR-0081) and the chain invariant
  (ADR-0097) become
- Date: 2026-09-22
- Confirm: the maintainer's acceptance; the branch and tag names; whether
  sections are renumbered at the end (decision 3); the calibration threshold
  (decision 4)

## Context

G3 is met (ADR-0132) and G1, afternoon-readable, is the gate still reserved to
the maintainer. The document is 4,981 lines and about 49,800 words, 162
requirement IDs, a register of 120 rows and 277 instances cited by 331
vectors, 94 labelled Note, Example and Rationale blocks and 125 headings, and
it reads as what it is: thirty-seven rounds of repair. The maintainer will
read it through and direct agent sessions to make it readable: reorder,
reword, cut restatements, shorten. Those edits must not change what the
document decides.

Two facts from the record shape the process. First, across every repair audit
the normative rules held and the explanatory prose around them produced every
confirmed defect (ADR-0113 through ADR-0115's audits; the pre-round-37 audit;
the audit of ADR-0132): the prose is where the length is and where the risk
of a rewrite is, and the two are not the same risk. Second, the repair-audit
convention does not converge on wording: the one-clause repair of ADR-0132
drew a one-clause finding in nine minutes, and its repair went unaudited by
decision. A rewrite of the whole document under that convention would audit
itself forever. What replaces it is a different instrument: not "does this
text stand alone" (the cleanroom rounds settled that) but "does this text say
what that text says".

## Decision

1. **Two editions, one of them normative.** Edition A is `spec/tarn.md` at
   `81e2ad2`, tagged `edition-a` and never edited; it remains the normative
   text until decision 5 replaces it. Edition B is `spec/tarn.md` on the
   branch `readable`, edited in place so that every tool that reads
   `spec/tarn.md` works unchanged; the reference is exported for the tools
   that need both at `scratch/cleanroom/editions/a/tarn.md`. **No normative
   change lands in either edition while B is open**: a decision the ledger
   or a round forces is taken by ADR against A on `main`, under the old
   gates, and ported to B as a listed edit. The two editions never carry
   different rules on purpose.

2. **The equivalence contract**, checked by `conformance/tools/tarn_inventory.py`
   before every commit to B, is the part of "no content change" a script can
   see. HARD, and a commit fails on any of them: the requirement-ID inventory
   is identical; every ID's governing paragraph is verbatim, or the ID is
   listed in `conformance/tools/reworded-ids.txt` with a one-line
   justification; the register §21.2–§21.5 is row for row identical by label;
   every §3.1 term stays defined. SOFT, reported for the reader and for the
   fidelity round: table rows and fenced blocks present in one edition only;
   numbers inside labelled Examples; BCP 14 keyword counts; headings; the
   count of labelled blocks. The tool's selftest is the list of what it
   catches and, deliberately, what it cannot: a sentence cut from a paragraph
   carrying no ID is invisible to it.

3. **Editing rules for B.** Explanatory prose is free: Notes, Examples and
   Rationales may be cut, merged, moved or rewritten, and a restatement of a
   rule may be removed where the rule's statement remains and the removal is
   logged with the ADR that added it. A normative sentence is rewritten only
   one at a time, by the listed-ID mechanism above, and never moved into a
   labelled block. No new normative content: B may say what A implies only
   where the derivation is A's own text, and a fidelity round grades anything
   else as an addition for the maintainer. Requirement IDs, register labels
   and section numbers stay fixed while B is open, so that every citation in
   the ADRs, the vectors and the tools keeps resolving; any renumbering is
   one mechanical step at the end, with a mapping table, if the maintainer
   wants it at all. The maintainer's standing rules for prose hold: no
   lowercase BCP 14 keyword in any line added, no dash pair nested in a
   dash-delimited clause.

4. **The fidelity round** (`scratch/cleanroom/wf-fidelity.js`) replaces the
   repair audit and the cleanroom round for B. Its instruments, every agent
   on Sonnet under the policy of 2026-09-21:
   - **the quiz, cross-answered**: two authors, one blind to each edition,
     write fifteen byte-level questions each, weighted to rules stated in
     prose; four takers answer each slate from A and from B; a divergence
     between the editions' takers is a finding with a location;
   - **six blind walks**, a reader, a writer and a verifier built from each
     edition, each answering the same fixed probes (concrete open sequences,
     verdicts, byte layouts, preservation decisions) and reporting its own
     edition's ambiguities;
   - **three comparators**, one per role, reading both editions and both
     walks, grading every divergence LOSS, ADDITION, REPORTER_ERROR or
     EQUIVALENT with both texts quoted;
   - **two completeness sweeps**, A into B and B into A, over what no script
     sees: the sentences without an ID, the carve-outs, the quantifiers and
     the labelled blocks;
   - **a diff-adversary** that builds the file, commit or verdict on which
     the editions disagree;
   - **three blind triage passes** and **a refute phase** in both directions,
     with a verdict enum per call and a round-wide attacker on a zero.
   The discriminating question, everywhere: *would an implementation built
   from B alone emit different bytes, or reach a different verdict on some
   file, than one built from A alone?* Blind agents read one edition; the
   path they are given names it and nothing else. Every gate-clearing
   verdict is provisional on the driver's hand-check, as in the cleanroom
   rounds. **Before the first real round, the instruments are calibrated**:
   `fidelity-seed.py` plants six known content changes in a copy of A, three
   the inventory tool catches and three only a reader can, the round runs
   over the seeded copy, and the findings file records which instrument
   caught each seed. A round whose instruments missed a seed is not trusted
   on a zero until the brief that missed it is changed and the seed is caught.

5. **Acceptance and the end state.** B replaces A on `main` when a fidelity
   round over the final B returns no LOSS and no unreviewed ADDITION after
   the hand-check, `tarn_inventory.py` is clean, `tarn_check` and the vector
   build pass on B, and the maintainer has read it. A is archived as
   `docs/archive/tarn-edition-a.md` beside its tag. ADRs 0001 through 0133
   quote edition A; `tarn_adr_quotes.py` gains an edition boundary so that an
   ADR numbered at or below this one is checked against the archive and a
   later ADR against the live text. G1's verdict is then given on B.

6. **The audit chain after G3.** ADR-0081's repair audit and ADR-0097's
   chain invariant were built for the drafting cycle and end with it. On
   `main` a normative change still lands by ADR behind `gate.sh --spec`; it
   is read by the next fidelity round through its port to B rather than by
   an audit of its own, and `tarn_chain` is retired from the commit gate,
   its last PASS at `508e052` and its last decided FAIL at `81e2ad2`. A
   wording commit to B needs no audit; the fidelity round is what reads it.

## Consequences

The document can be made readable without the ratchet that made it long: a
cut restatement is checked by the sweep and the quiz, not by an audit of the
cut. What is foreclosed is silent normative change: a reworded rule is a
listed edit, a decided question is an ADR against A, and an addition B makes
is the maintainer's to keep or strike. The cost is a second reading
instrument whose sensitivity is unmeasured until the seeded run, on a model
that returns a third of what the rounds' earlier model did; the calibration
exists so that a zero from it means what it says. Two editions exist for the
length of the rewrite and one afterwards.

## Alternatives rejected

- **Edit `spec/tarn.md` in place under the existing gates.** Every wording
  commit would open the chain and want an audit; the record says this does
  not converge, and the audits test the wrong property.
- **Two normative editions maintained side by side.** The document's own
  §21.1 exists because two statements of one rule drift; two documents would.
- **Agents only, no mechanical contract.** The instrument's sensitivity is
  the open question; the contract makes the checkable part certain and
  leaves the instrument the part that needs judgement.
- **A fresh rewrite from an outline, in the manner of a shorter format's
  specification.** The rules and their carve-outs are the product of
  thirty-seven rounds; a rewrite that does not start from them would have to
  rediscover them.

## Precedent

- **ADR-0034**: the cleanroom protocol; the fidelity round keeps its access
  rule, its blindness, its triage and its refute phase.
- **ADR-0081** and **ADR-0097**: the repair audit and the chain invariant,
  which this ADR retires for the readable edition.
- **ADR-0055**: a gate declared on evidence a tool can reproduce; the
  contract is that shape.
- **ADR-0003**: stable requirement IDs and the register, which are what make
  the contract mechanical.
- **ADR-0132**: G3, and the last repair made unaudited by decision.
