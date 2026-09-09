# Triage pass — implementer consequence — round 33

## Disclosure

Read only `/Users/robertkleffner/Documents/GitHub/tarn-first-draft/spec/tarn.md`,
in chunks covering §2, §4, §5, §6, §7, §8, §9, §10, §11.1–11.2, §15, §16, §18,
§19, §20, §21, §22, §24, Appendix F and Appendix H's checklists. Ran targeted
`grep` over that one file (`re-establish`, `^| L18 …`, section headings, RFC
tallies). Opened **no** walk transcript, no other triage pass's notes, no
directory listing of the round output directory, no `docs/`, `PLAN.md`,
`AGENTS.md`, `conformance/`, `registry.json`, git history or web.

Every one of the 25 input findings was evaluated. No gaps.

## Grouping

22 groups over 25 ids. Two merges:

- **verifier-01 + quiz-02** — identical defect: §5.2 `[R-CNT-21]` and §9.7
  `[R-LIF-08]` restate §15.3's slack disposal without its
  "that no other claimant claims" qualifier.
- **writer-02 + adversary-03** — both land on §20.3 step 4's
  `A commit MUST NOT change one of these`: no reader-side clause (which §2.1's
  Note claims every writer prohibition has) and no statement of which
  `[R-CNF-02]` category it occupies. adversary-03's SHOULD limb ([R-MTA-09])
  is the same Note's second claim and travels with it.
- **diagrams-04 + register-04** — both report cells departing from §21.1's
  Governing-rule parenthetical convention; diagrams-04 raises L26/L31 and the
  R6/R10 asymmetry, register-04 raises R10 alone. One defect class, one group.

## Text checked, verbatim

§7.4 layer-record inline-payload table header: `| Field | Type | Constraint |`
— three columns. §4.7's Note: "its table omits the offset and class columns".
Size is omitted and unaccounted. **diagrams-01 confirmed**, and the Note is
labelled *Note*, non-normative under `[R-CNF-01]`.

§15.3 `[R-IDX-03]`: "and none to `[R-LIF-08]`'s coverage walk, so any bytes it
nominally addressed **that no other claimant claims** fall to slack."
§9.7: "the walk passes over it, and the bytes it nominally addresses fall to
slack (§15.3)." §5.2: "it contributes no claimant, the walk passes over it, and
its bytes fall to slack (§9.7)." **verifier-01/quiz-02 confirmed as written.**
Decided against the literal reading by each passage's own operative definition —
§5.2: "Every byte the live state does not claim is **slack**"; §9.7: "Bytes the
walk does not reach are slack". Both are set-complements; a byte the front block
claims is not slack however some malformed entry nominally addresses it.

§19 preamble: "A row this section does not restate is due at its own tier all
the same, with its governing rule's own outcome." §21.2 F5's Detected cell:
*open*. **reader-01 decided by the document.**

§9.2: "A writer that omits a barrier violates this requirement as an actor, and
the file it produces is never nonconforming by virtue of it, as `[R-CNF-02]`
says of every **conduct rule**." §2.3's preceding sentence is where conduct rules
live and its "(§10.3, §18.3)" is an em-dash gloss, not a closed list.
**reader-02 decided.**

§18.2 prose immediately under the table: "1 = none and 2 = zstd are assigned;
3 through 0x7F are reserved; values ≥ 0x80 are the experimental range (§10)."
§15.1's own Valid-values cells read "see §15.3" — the deferring cell is the
document's practice, not an anomaly. **reader-03 decided; the cell is not out of
line with §15.1.**

§20.3 step 4 permitted side: "a slab or alignment declaration MAY be **declared,
re-established or cleared** as this step provides below."
Fixed side: "the layout, the linearization and the index encoding, the codec and
the filter, the rank and the dimension order, every tile extent, every channel's
type and fill, an interleaved layer's channel list (its names aside), and the
position of every planar channel but the last. A commit MUST NOT change one of
these" — **A, S and A_slab are absent from the fixed list**, so no MUST NOT
reaches them; the only bar on a value change is the permitted list's "and no
other".
Gives-up list: "a shrink, a fill change, a re-type, a re-tiling, a change to the
dimension order, a change of rank, layout, linearization, index encoding, codec
or filter, any change to an interleaved layer's channel list but a channel's
name, a planar channel inserted or removed anywhere but the end of the list, and
a planar channel list both extended and shortened in one commit are rewrites" —
**no alignment or slab change named**.
Below-clause: "a slab declaration is re-established or cleared (`[R-SLB-04]`),
and an aligned layer's stored tiles — every one the new state keeps, not only
those this commit adds — satisfy its invariant or the declaration is cleared".
Whitespace-normalised sweep of "declared, re-established or cleared": five hits —
§11.1 Rationale (non-normative), §20.3 step 4, Appendix H's updater checklist,
plus the below-clause's two-verb form and `[R-SLB-04]`'s own two dispositions.
**No sentence anywhere says whether writing a different nonzero value into an
already-nonzero A, S or A_slab is a "declaration" within the fifth member's
meaning.** writer-01 upheld.

Correction against the reporter: writer-01 asserts a slab value change "has no
in-place path at all under (R-b)". False — clear S in commit n, declare S = 16 in
commit n+1 is available under R-b exactly as it is for A, and the reporter's own
two-commit argument establishes it. The cost of R-b is therefore one extra
commit (a directory, a pad, a trailer and, for a slab, a re-emitted index
region), not necessarily a whole-file rewrite. The single-commit fork stands.

§20.3 step 4 tiebreak: "where a field is on both sides — a dimension extent, a
planar layer's channel list, an interleaved layer's channel list — **the
permitted side states the whole of what a commit MAY do to it**."
**quiz-01 decided** — the planar channel list is named expressly.

§20.3 step 4 first member: "its name, and its dimension and channel names, MAY
change"; justification: "a name enters no map this specification defines, and a
commit MAY change several names at once, two swapped included". Appendix H
carries the same unqualified rename permission. **adversary-04 decided.**

§5.2 `[R-CNT-21]`: "Every byte the live state does not claim is **slack**:
alignment and slab gaps, the pre-trailer pad, and **everything an earlier commit
superseded**." §5.2 `[R-CNT-02]` defines "structure" as a class of the live
committed state's partition. §6.2 `[R-CNT-05]`: "Those bytes — the pre-trailer
pad — are slack (§5.2)". **adversary-01 decided**: a superseded trailer in the
gap is slack by name.

§18.2 `[R-MTA-10]`: file conformance "is decided by the structural checks that
precede the document alone: the record's framing and extent slot
(`[R-CNT-13]`), the encoding byte's own value set (`[R-MTA-03]`), and **the
extent's terminal CRC** (`[R-CNT-20]`)." §21.5's exception is stated as "where
no **document rule** attaches". **adversary-02 decided**: R2 survives at an
experimental encoding.

§2.3: verifier "checks every file-level requirement — including those ordinary
readers are exempted from". §21.2 F6: "a verifier holds no such exemption
(§2.3)". Appendix H: "which `[R-CNT-04]` lets a reader not holding it resident
defer or omit and §2.3 does not (F1, F6)". **verifier-03 decided, three times.**

§20.5 `[R-WRT-07]`: "regenerates each tile-index region **any of whose stored
extents the output relocates**" and "placement being the compactor's to choose";
§20.1 `[R-WRT-01]`: "a violation latent in a structure they carry forward
unmodified travels with it, seen or unseen". **quiz-03's divergence is real and
expressly licensed** — a design decision, not an ambiguity.

Appendix F heading carries no "(non-normative)" marker; A, B, C, D, E, G, H all
do. RFC 1950 and RFC 1952 appear in `[R-COD-05]` and T15 and nowhere in
Appendix F. **diagrams-03 confirmed.** `[R-COD-05]` decides the bytes without
either: "exactly one DEFLATE compressed data stream as defined by RFC 1951".

§21.3: `| L26 | … | [R-CNT-18] (§7.3 registry table) |`,
`| L31 | … | [R-CNT-23] (§15.1) |`. §21.5: R6 `[R-MTA-04]` (R-CNT-25, R-ENC-12),
R7–R9 `[R-MTA-04]` (R-CNT-25), **R10 `[R-MTA-04]` (R-ENC-12)**. §21.1: "any
identifiers following it in parentheses are the further rules the condition
reads". **diagrams-04 + register-04 confirmed.**

§21.1: "as `[R-CNT-25]`'s quarantine does for **every** §21.5 row". `[R-CNT-25]`
quarantines "each way a user-metadata record's document can be **unreadable**";
§18.2 of R4's content-size instance: "**the bytes decode**, and what is wrong is
what the header said about them". `[R-MTA-09]`: "Any violation here is
ignore-record". **register-02 confirmed as an over-statement; outcome fixed
elsewhere.**

§21.1 states the rule-governs tiebreak, normative completeness, the
specialization rule and the Instances arithmetic, and carries no
`[R-<PREFIX>-<NN>]`. Confirmed by reading §21.1 in full. **register-05
confirmed** — a maintainer's decision whether to assign one.

§21.6 closing: "Neither is a register row: the register enumerates
file-conformance violations (§21.1), and a file this document declines to judge
is not one." Two limbs; limb (i) disposes of the experimental-MU=1 case
(conforming, so no violation), limb (ii) of the foreign-major case.
**register-01 is PARTIAL** — the compound reason reads as offered of both, but
each limb does work for one case.

§22.3 `[R-SEC-04]` states the unassigned-type extent residue first and supplies
the operator remedy only for the experimental-encoding case. "counted and named"
occurs once in the document, in `[R-MTA-10]`. **verifier-02 confirmed as an
asymmetry**; report-only.

§20.5's Example closing sentence omits superseded payloads and superseded
record extents; §20.3's own Example names them ("The prior index region and the
superseded payload become slack"). Inside a block labelled *Example*.
**diagrams-02 confirmed, non-normative.**

## Byte-level judgement

One: **writer-01**.

Premise stated so it can be attacked: I evaluate "which byte sequences a
conforming implementation may emit" **per actor class and per input** — the set
of outputs a conforming *updater* may produce for a given input file and a given
edit. Under R-a it may append one commit; under R-b it may not, and must emit
either two commits or a whole-file rewrite. If the maintainer instead evaluates
the test as the union over all conforming implementations of all byte sequences
producible, the flag falls — because slack content is unconstrained
(`[R-CNT-21]`: "its content is unconstrained, and no conformance requirement
applies to it"), so a conforming **creator** can emit a file byte-identical to
updater X's output under either reading, with the superseded generation sitting
in it as slack. That union reading would also make §20.3 step 4's entire closed
list byte-level-inert, which I do not think is the intent.

Sentence I looked for and did not find: any statement that "declared" in "a slab
or alignment declaration MAY be declared, re-established or cleared" does or does
not reach writing a different nonzero value over an existing one. Not in §20.3
step 4, not in its below-clause, not in `[R-SLB-04]`, not in §11.1's Rationale,
not in Appendix H.

## Downgrades, and on what ground

- **Document decides it**: reader-01, reader-02, reader-03, verifier-01/quiz-02,
  verifier-03, adversary-01, adversary-02, adversary-04, quiz-01, quiz-03,
  writer-02/adversary-03 (the conformance status of the resulting file is
  decided by `[R-CNF-02]`'s "File conformance is a pure predicate on bytes",
  which cannot distinguish bytes a creator could lawfully have emitted).
- **Ledger already asks it / bookkeeping**: register-03, register-06,
  diagrams-04 + register-04, register-02, register-01.
- **Maintainer's call, no reading forks**: verifier-02, register-05,
  diagrams-03, quiz-03.
- **Non-normative text**: diagrams-01, diagrams-02, adversary-03's Note limb.
