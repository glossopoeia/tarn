# 0067. Conformance is per-major, and four register repairs

- Status: Accepted
- Date: 2026-08-14
- Covers: the scope of *conforming*; F21's removal and the F-row renumbering;
  L2's instance arithmetic; `[R-ENC-06]` at tile scope; `[R-ERR-05]`'s
  hard-limit list; Appendix G's open degrees of freedom
- Confirm: none

## Context

Cleanroom round 8 escalated three register decisions and deferred two more
([docs/cleanroom/08-g3/findings.md](../cleanroom/08-g3/findings.md)). None
was byte-level — ADR-0066 carries those — but each turned on a claim the
document makes about itself, and three of them move the corpus.

## Decision

**Conformance is always conformance to a stated format major version, and
F21 is dropped.** §2.3 supported both readings, two bullets apart: *"A byte
sequence satisfying every file-level requirement of this specification"*
(absolute) against *"every conforming file of a format major version it
implements"* (relative). The relative reading governs. §2.3 now says so: a
file declaring another major is neither conforming nor nonconforming under
this document, and a reader's refusal of it is a capability finding, not a
finding about its bytes.

F21 — *"version_major is a nonzero major the reader does not implement"* —
therefore leaves the register, which §21.1 makes an enumeration of
detectable *file-conformance* violations. §21.6 had already said as much
and then offered a non-reason for treating the two capability cases
differently: it called both *"a reader's capability, not a defect in the
bytes"* and gave that likeness as why one was registered and the other was
not. Both are now unregistered, and §21.6 names what *is* registered in
each case instead.

The rule loses nothing. **F20 carries `[R-CNT-07]`'s real violation** —
version_major = 0, permanently invalid in every major — so the requirement
keeps a row, and `[R-VEC-04]`'s *"every vector built from §21's register is
nonconforming"* becomes true again rather than being qualified.

**L2's sum instance ranges over two containers.** §21.1's *"a sum against a
bound … the fields it reads are not instances"* is why L2 does not split
`extent_offset` from `extent_length`, and it speaks only to the field axis.
The container axis is separate, and L1, L16, L17 and L18 all spell it out —
layer record and sub-record. L2 did not. This is the same repair round 7
applied to five other cells and missed here.

**`[R-ENC-06]` gains its third owning scope.** F5 records the cause at file
scope and L3 at layer scope; the tile-index entry had none, though it is a
fixed-layout structure whose fields are constructible at unchanged 20-byte
size (offset as u32, length and crc each as u64). T27 is added on F5's and
L3's model, and like them records the cause rather than a check of its own.
The known cost, priced in ADR-0065 for two rows, is now paid for three.

**`[R-ERR-05]`'s hard-limit list is completed and its closing claim
dropped.** The list omitted the alignment bounds, A_slab, the slab run
length, the directory's floors and `[R-CNT-27]`'s 128-byte file minimum,
and closed *"never a number chosen here"* — which §16.1 falsifies in its own
text, since the 512 floor on A is the legacy sector size, chosen. The
document now names it as the one chosen number. This is not tidying:
`[R-VEC-03]` binds corpus construction to this enumeration, so a short list
was a short corpus.

**Appendix G closes three degrees of freedom it claimed not to have.** Its
closing paragraph said gap *content* was the sole residue. Gap *extent*,
sub-record order, and the fill a writer records when its caller chooses
none were all open. All three are now profile requirements. The fill one
reaches furthest: item 6 stores no tile whose samples all equal fill, so
two writers defaulting fill differently disagree about which tiles exist.

## Consequences

The register moves to **125 conditions over 253 instances**, and the corpus
to **306 vectors** at 100% row and per-instance coverage: −1 condition and
−1 instance from F21, +1 instance from L2's split, +1 condition and +1
instance from T27. TV-0130 is retired; TV-0952 and TV-0953 are new.

**F22–F39 renumber to F21–F38.** REG-01 makes row ids positional, so
removing a row shifts every later one — 148 references across `spec/tarn.md`
and five vector-definition files, shifted in a single pass so no
intermediate state could collide. Earlier ADRs and the round 1–8 cleanroom
findings keep the old numbers: they record what the document said when they
were written, and ADR-0002's rule is to supersede rather than rewrite. A
reader comparing them against §21 after this ADR must add one to any F-row
above F20.

Priced knowingly. The renumbering is a real cost to anyone holding a
citation to an F-row, paid once, and the alternative was a register whose
completeness clause had a standing counterexample. Adding T27 makes three
cause rows a verifier built from §21 alone cannot turn into a check of its
own, which leans §21.8's coverage further on `[R-VEC-02]`'s co-attribution
clause — a gap that remains open and is not this ADR's subject. Completing
the hard-limit list adds bounds the corpus now owes vectors at under
`[R-VEC-03]`; the alignment bounds already have them, the rest do not, and
that debt is recorded rather than discharged here.

## Precedent

- ADR-0043's method for the limits table, applied to the rows it had not
  reached.
- ADR-0049 and ADR-0056, which established that a register defect found by
  recounting is repaired in the table rather than absorbed by the prose.
- ADR-0064, whose per-instance measurement is what made L2's collapsed cell
  visible at all: under row-level counting the shortfall was invisible.
- ADR-0046, under which the specification governs and a disagreeing vector
  is corrected — the authority for retiring TV-0130.
