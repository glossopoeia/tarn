# Cleanroom round 9 — findings

Protocol: ADR-0034. Charters and access rule: [prompt.md](prompt.md).
Six fresh-context implementer walks, a three-way blind quiz, and three
independent triage passes, all against `spec/tarn.md` alone. Every agent
disclosed its access; none reported a breach.

## Verdict

**Zero byte-level ambiguities. The quiz came back 15 agree / 0 diverge /
0 underdetermined.**

| | |
|---|---|
| Quiz | **15 agree / 0 diverge / 0 underdetermined** |
| Findings reaching triage | 41 — reader 5, writer 10, verifier 6, register 9, adversary 6, diagrams 1, quiz author 4 |
| Findings recovered afterwards from a transcript | **7** (see below) |
| Flagged byte-level by their reporter | 3 |
| Distinct defects | **35** (29 from triage + 6 new on recovery) |
| **Byte-level, after triage and hand-check** | **0** |
| Severity (majority) | 26 editorial · 4 register bookkeeping · 4 design decision · 1 none |

G3's byte-level criterion is met for the second time in three rounds. The
gate is not closed: ADR-0034 also requires every finding dispositioned, and
five want a maintainer decision.

## The trend

| Round | Byte-level defects | Quiz |
|---|---|---|
| 6 | 5 | 14 / 1 diverge |
| 7 | 0 | 15 / 0 / 0 |
| 8 | **2** | 15 / 0 / 0 |
| **9** | **0** | **15 / 0 / 0** |

Round 8's two survivors were both in §20.4's `[R-WRT-08]` table. That table
was rewritten by ADR-0066 and read cold here by all six walks; no reporter
raised it. Reporters self-flagged 3 findings byte-level and none survived.

## The one that needed the hardest look

**F1 registered a condition ADR-0067 had just stopped being a violation.**
Three reporters found it independently — the reader, the register hunter and
the adversary — and two flagged it byte-level.

F1's Instances cell listed `trailer version_major` as an instance of a
reject-file violation of `[R-ENC-01]`. But ADR-0067 had rewritten §2.3 to
say a file declaring another major *"is neither conforming nor nonconforming
under it"*, and §21.6 to say *"Neither is a register row … What is
registered in each case is the neighbouring condition that is a violation —
version_major = 0 … (F20)"*. So the register kept enumerating, as a
file-conformance violation, the exact case two other sections had just
declared unjudgeable. **This is a propagation failure of ADR-0067**, one
commit old, and it is the third round running in which a repair made in one
round is the defect found in the next.

The adversary's construction is what makes it airtight: `version_major` is a
u16 whose only invalid value is 0, and **0 is a byte-swap fixed point** — BE(0)
and LE(0) are both `00 00`. So the one value with a validity gate is
invisible under byte reversal, and every other swapped value reads as a major
the reader does not implement. There is no byte sequence that witnesses a
byte-swapped `version_major` at all.

**It is not byte-level, and the reason corrects two of the three reporters.**
Both the register hunter and the adversary argued that §21.1's *"where a row
and the rule it cites diverge, the rule governs"* cannot reach F1, because
F1 cites `[R-ENC-01]` while the conflicting text is §21.6, which F1 does not
cite. That premise is false: F1's governing-rule cell reads **`[R-ENC-01]`
(R-CNT-07)**. It does cite `[R-CNT-07]`, which §2.3 and §21.6 gloss as a
capability refusal — so §21.1's tiebreak applies directly and both
implementations land in the same place. The skeptic pass caught this; the
implementer pass upheld the finding partly on the false premise.

The adversary was right about a sub-claim the reader got wrong: F1's
`generation` instance *is* constructible, since a big-endian `0x80` reads
2⁶³ and trips `[R-CNT-06]`. Only `version_major` has no witness.

## A process failure worth more than any single finding

**One walk returned 1 finding out of the 8 it had written.** The diagram
auditor's structured result carried `disclosure: "test"`,
`walk_summary: "test"`, and a single finding — while its 610-line transcript
of record contained a full, properly-disclosed audit and **eight** findings,
`diagrams-01` through `diagrams-08`. Seven never reached triage.

No agent errored. The workflow reported 12 of 12 complete. Nothing in the
structured pipeline could have caught it: the schema was satisfied, and the
one finding that came through was real. It was caught by diffing the
transcript against the structured return — the same discipline that caught a
false coverage claim in round 7 and a truncated reconciler input in round 6,
applied one layer further out.

Of the seven recovered, one duplicated a defect two other reporters found
(the L47/L48/L50 instance arithmetic) and **six were new**, including two
more propagation failures of ADR-0067 and a miscited requirement ID that had
survived nine rounds. None is byte-level; all are dispositioned below.

The rule this round adds: **check every agent's transcript against its own
structured return, not only its coverage claims against the input.**

## What else the round caught

**Appendix G, four defects, all in text ADR-0067 wrote.** Its closing
paragraph now names gap *content* among the four freedoms "the items above"
close — and after ADR-0067's rewrite no item closed it. Item 3 ordered a
layer record's sub-records "by their order of creation", which is producer
history and not derivable from bytes, in a profile whose entire purpose is
byte-identity. Item 2 asserts a deterministic `file_id` while naming no hash,
no digest-to-u64 rule and no preimage serialization. And the closing
paragraph's "Four things are not" undercounts its own residue.

**`[R-ENC-12]` cited where `[R-ENC-13]` is the rule.** §19.1 step 4 says
*"`[R-ENC-12]` makes name comparison a byte comparison"*. `[R-ENC-12]` is the
name-constraint rule; `[R-ENC-13]` is *"Name comparison is raw bytes"*.
Nine rounds of cold reading had not caught it.

**Appendix B omitted a constant ADR-0067 added.** §4.7's Note promises *"All
named constants appear once in Appendix B"*, and ADR-0067 added the directory
minimums to `[R-ERR-05]`'s hard-limit list without adding them there.

**T14 condemned every sparse codec-1 layer, read literally.** *"Codec 1
(none) declared and the index entry's length differs from the tile's decoded
size"* — with no `non-sentinel` qualifier, where six neighbouring T-rows carry
one. A sentinel entry's length is the all-ones sentinel, which differs from
any decoded size.

**The register's container axis, again.** L47, L48 and L50 each cover *"a
layer record's or sub-record's"* flags while enumerating instances for one
container, where L16–L18 and F27/F28/F30 apply the cross product. Same defect
class as L2 in round 8.

## Disposition

**Fixed — 15 edits, zero anchor misses**, applied one at a time.

| Defect | Repair |
|---|---|
| `f1-registers-an-unjudgeable-case` | `trailer version_major` struck from F1's Instances cell, with the reason stated in the cell; TV-0100 retired |
| `l47-l48-container-axis` | both rows enumerate layer record and sub-record; TV-0954 added for L47's sub-record instance |
| `t14-missing-non-sentinel` | the qualifier its six neighbours carry |
| `enc12-cited-for-enc13` | §19.1 step 4 repointed |
| `appendix-b-omits-directory-minimums` | row added |
| `r1-uncited-governing-rules` | `[R-MTA-03]`, `[R-EXT-03]` added beside `[R-CNT-25]` |
| `name-cap-two-derivations` | §21.9 splits the u8-prefix names from user-metadata keys, which have no prefix |
| `profile-gap-content-unclosed` | item 3 requires gap bytes be zero |
| `profile-subrecord-order-unreproducible` | ordered by encoded bytes, not creation order |

The register is **125 conditions over 254 instances**, the corpus **306
vectors** at 100% row and per-instance coverage.

**Escalated — five maintainer decisions.**

1. **Can a layer ever be deleted?** §20.4's *"both registered types carry
   PE = 1, so neither can be dropped"* means no defined operation removes a
   layer record: §20.5 lets a compactor drop only the MU = 0 / PE = 0 row.
   All three passes agree §20.4 decides it and that the consequence is
   nowhere stated, while §23.1 and §20.4's own rationale read as though
   deletion were available. §2.3 also mislocates the obligations in "Part I"
   when §20.4 is in Part III.
2. **L50's instance split.** L47 and L48 are done; L50's four-way split is
   held back because one of the four — a layer record whose PE bit differs
   from the registry — is *only* exhibitable as a co-violation of L47, since
   type 0x0001 is fixed at MU = 1 / PE = 1 so "PE differs" is necessarily
   MU = 1 / PE = 0. That is the `[R-VEC-02]` co-attribution gap, and forcing
   a vector through it would encode a claim the manifest cannot yet make.
3. **The endianness cause at layer and tile scope.** F1/F2 register it at
   file scope only, where the parallel field-width cause now sits at all
   three (F5, L3, T27).
4. **`[R-WRT-06]`'s compactor obligation** to "emit a new conforming file" is
   unsatisfiable for an input carrying a content violation `[R-WRT-09]`'s
   verification depth cannot reach.
5. **The `informative` field class** has no member anywhere in the document
   and its definition is not disjoint from `semantic`.

**Deferred, with owners.** The remaining editorial defects — §21.7's
witness-list omissions, `[R-CNT-04]`'s residency dash-list, `[R-WRT-07]`'s
regeneration trigger, `[R-SLB-04]`'s omitted commit shape, the 256 MiB /
8 MiB zstd interaction, §21.3/§21.4's header glosses, §21.1's missing
requirement identifier, §20.4's unidentified table, Appendix H's three
checklist drifts, §2.4's "skipped as though absent", `[R-MTA-04]`'s wider
representation, and the compactor's unnamed refusal — are recorded here
against their owning sections and carried to round 10.

## Artifacts

- [prompt.md](prompt.md) — charters, access rule, taxonomy, pass criteria
- `transcript-reader.md`, `transcript-writer.md`, `transcript-verifier.md`
- `transcript-diagrams.md` — **the eight-finding audit whose structured
  return carried one**
- `transcript-register.md`, `transcript-adversary.md`
- `transcript-quiz-author.md`, `transcript-quiz-answers.md`,
  `transcript-quiz-key.md`
- `transcript-triage-correctness.md`, `transcript-triage-implementer.md`,
  `transcript-triage-skeptic.md`
