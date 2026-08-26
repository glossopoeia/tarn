# 0107. `[R-CNF-02]`'s stale quantifier, `[R-CNF-13]`'s swallowed exemption, and a tooling defect an auditor found

- Status: Accepted (resolves the ADR-0106 audit)
- Date: 2026-08-25
- Covers: §2.3's `[R-CNF-02]` and `[R-CNF-13]`; `conformance/tools/tarn_editorial.py`;
  the audit harness's briefing; Q-I6
- Revises: two repairs ADR-0106 wrote
- Confirm: none

## Context

The ADR-0106 repairs were audited by three auditors over seven hunks, run
**findings-only with no verification cap** — the fix ADR-0106 recorded after a
cap sized for a three-hunk diff starved thirteen of twenty-five findings on a
twelve-hunk one. Eighteen findings came back; they grouped into eleven distinct
defects, each verified, and the four reporter-flagged byte-level findings that
were downgraded each went to a refuter. Two confirmations, one overturn.

## Decision

**`[R-CNF-02]` loses the quantifier ADR-0106 superseded next door.** ADR-0106
re-quantified `[R-CNF-13]` from requirements to conditions and left `[R-CNF-02]`,
eighty lines above in the same subsection, still reading "the requirements that
reach it" and "the failure of a reaching requirement" — citing `[R-CNF-13]` as
its authority for a predicate `[R-CNF-13]` expressly says is not a predicate of
requirements. **All three auditors found it independently, and it is byte-level.**
The discriminator: a verifier implementing only major 1, given a major-2 file
with valid magic, valid trailer CRC and `file_id` = 0. Per condition, F12's
invariant is not one `[R-CNT-24]` fixes, so nothing is established and the verdict
is *cannot establish*; read existentially over requirements, `[R-CNT-06]` reaches,
F12 becomes a finding about the file's bytes, and `[R-CNF-11]`'s priority clause
forces *nonconforming*. Same bytes, opposite verdicts, and §2.3 makes the verdict
an obligation rather than a presentation choice.

The repair is two phrases. A whitespace-normalised census confirms these were the
only requirement-level uses of the predicate in the document; `[R-CNF-13]`'s own
two uses were already condition-level.

**`[R-CNF-13]` stops swallowing exemptions granted on other grounds.** A refuter
overturned the downgrade on this one, and the finding is that **ADR-0106's own
repair created the collision.** Defining the rule's object as "a **condition** …
and **not the requirement that defines it**" severed the MUST from `[R-CNT-04]`'s
residency exemption, which lives in the requirement. F6's condition — the front
signature block not matching the constant — is a reaching condition, so a reader
that would have to fetch bytes [0, 16) became obliged to check them, which
`[R-CNT-04]` says it MAY decline. F6's own Condition cell carries that exemption
inline and so escapes `[R-CNF-04]`; `[R-CNF-13]` as written had no such route,
because the definitional clause closed it.

The MUST now says that an exemption the condition's governing requirement grants
**on a ground other than the declared major** applies unchanged. Stated as a
property, with `[R-CNT-04]` named as an instance rather than as the list — the
refuter's proposed sentence called it "the only such exemption in this text", and
a closed claim of that shape is what three of this week's defects have been.

**Appendix G item 5 goes to Q-I6 rather than take a fourth patch.** Three
auditors reported that ADR-0106's replacement is *still* a false universal: the
sentence has now said "changes the stored bytes of every tile it touches" (false
at stride 1), "any tile whose shuffle stride exceeds 1" (false at n = 1), and
"elsewhere it changes the stored bytes of every tile it touches" (false for a
tile whose decoded image is invariant under the permutation). The sweep found the
question already owned: **Q-I6** asks why the profile pins what it pins, and its
premise is that each pinned freedom "changes bytes and no content implies it" —
which is false for the filter, a member already on the list. Q-I6 is amended
rather than duplicated, and its option (c) becomes the leading one: the item keeps
asserting a universal because the criterion demands one, and the criterion is what
is wrong.

**A tooling defect, found by an auditor reading its own briefing.** The harness
told every auditor this session that text in a Markdown blockquote is
non-normative. `[R-CNF-01]` exempts "any text **labeled** *Note*, *Example*, or
*Rationale*" — by label, not by the ">" marker. Of ninety blockquote blocks, one
carries no label and is not an identified non-normative appendix: §15.1's
region-layout block, which is therefore **normative**.

That briefing error was also in `tarn_editorial.py`, which excluded every ">"
line — so an edit to §15.1's normative block would have graded **EDITORIAL**. A
false negative, the one direction that check must never fail in, and the *second*
time this tool has had that shape. The parser now excludes a blockquote only when
it is labelled, a self-test case mutates an unlabelled block and asserts CONTENT,
and the harness briefing is corrected. The "18.5% of the document is
non-normative" figure in ADR-0104 is correspondingly a shade high; that ADR is not
rewritten, and this records the correction.

## Consequences

The register does not move: 121 conditions, 277 instances, 331 vectors. No cell
changes and no propagation acknowledgement was needed.

**On what caught what.** Nine of the eleven grouped defects were refuted or
partial, so the audit was not a sweep. The two that survived were both reported by
all three auditors independently — convergence remains this project's most
reliable signal. The overturn came from the refute phase doing its stated job:
the verifier had shown the reporter's quotation was truncated, which is not the
same as showing the repaired text is correct, and the charter's insistence on that
distinction is what produced the finding.

**And the instrument that keeps earning its keep is the disclosure field.** It has
now surfaced an injected notes index, a path-name leak, a commit-subject channel,
a mislabelled hunk header, and — this cycle — a briefing that contradicted the
document, which no mechanical check in this project could see because the briefing
is not in the repository.

## Precedent

- ADR-0106's own lesson about the verification cap, applied here rather than
  merely recorded: this audit ran findings-first and sized verification to the
  count, and two of the confirmed defects came from groups a cap of four would
  have starved.
- ADR-0095's rule about closed claims, applied to the refuter's own proposed
  sentence: a fix offered with "the only such exemption in this text" is a list,
  and the property form is what landed.
- ADR-0084's disclosure paragraph, whose fifth distinct channel this is.
