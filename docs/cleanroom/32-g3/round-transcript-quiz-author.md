# Cleanroom round 32 — quiz author transcript

**No answers appear in this file.** I am the author only; two blind agents
answer and key the slate.

## 0. Access and method

Read exactly one file: `/Users/robertkleffner/Documents/GitHub/tarn-first-draft/spec/tarn.md`
(4,754 lines), in five sequential `Read` calls covering lines 1–4754 with no
gaps. No other repository file was opened, listed, or grepped. No git history,
no web, no ADRs, no conformance corpus, no registry.

Local computation only, all of it in my own scratch directory
`/private/tmp/claude-501/-Users-robertkleffner-Documents-GitHub-tarn-first-draft/r32-round/scratch/quiz-author/`:

- `crc_check.py` — a CRC-32C (Castagnoli, reflected, init/final 0xFFFFFFFF)
  implementation, used to reproduce the document's own published constants
  before trusting my own derived values.
- `count_inst.py` — parses the §21.2–§21.5 register tables out of the one file
  I am allowed to read and counts rows and Instances-cell members under
  §21.1's stated rule.
- `q_calcs.py` — the arithmetic behind each numeric question.

I wrote no other files anywhere, and I did not read this output directory.

### Self-checks run before authoring

I refused to build any numeric question until the document's own published
numbers reproduced under my own CRC implementation, so that a divergence
between the two answerers cannot be blamed on my arithmetic:

- CRC-32C of `"123456789"` and of zero bytes — both reproduce §4.5's check
  vector.
- §7.4's worked layer record: the segment CRC over 80 bytes of sentinel
  entries, and the crc_of_crc_array over that 4-byte array — both reproduce.
- §15.4's all-sentinel full-segment constant — reproduces.
- Appendix A's trailer CRC over trailer bytes [0, 60) — reproduces.
- §21.8's "120 conditions over 277 instances": 35 + 49 + 26 + 10 = 120 rows,
  and applying §21.1's rule ("Instances within a cell are separated by
  semicolons, and a cell reading — is one instance") mechanically over all
  four tables yields exactly 277. Internally consistent; no finding.

A note on searching. The document is hard-wrapped and blockquotes wrap with
`> ` inserted, so I did not rest any conclusion on a line-oriented zero result.
Every claim below is grounded in text I read in full sequence, not in a grep
miss.

## 1. How I chose the slate

The brief weights the slate toward nineteen recently changed passages and asks
for a spread: ≥3 questions producing or validating concrete bytes at concrete
offsets, ≥2 reader/verifier verdicts on a specific malformed file, ≥2
arithmetic, ≥2 on rules stated across more than one section, and no two
questions that fail together for the same reason.

The governing constraint on a *good* question here is that the document must
determine one answer. So I built every question by first deriving the answer
from the text myself, then asking whether a second careful reader could reach
a different one for a reason I would call defensible. Where the answer was
defensible-but-arguable, I moved the matter out of the slate and into the
findings list rather than manufacturing a divergence that indicts nobody.

Design rules I applied to every item:

1. **Answer shape stated in the question.** Every hex request names its case
   and its byte order; every integer request names its origin ("measured from
   the first byte of the inline payload", "from the start of the tile-index
   region"); every verdict request names which vocabulary to use (§2.4's
   outcome names, §19.2's tier names, §2.3's verdict names, a §21 row label).
   A case difference or an origin difference must not be able to masquerade
   as a divergence.
2. **At least two places, always.** No question is answerable from one table
   cell. The cheapest one (Q03) still requires §6.2's layout table, §4.2's
   widths, §4.1's endianness and §4.5's CRC parameters.
3. **Distinct failure modes.** I checked the slate pairwise for shared
   dependence. Q04 and Q05 both touch §11.4, but on different formulas — Q04
   on the in-tile ordinal Σ uᵢ·∏_{j>i}Tⱼ and §14.2's offset arithmetic, Q05 on
   the spatial ordinal Σ tᵢ·∏_{j>i}Gⱼ, the planar disk ordinal c·N+s and
   §15.4's segment arithmetic. Getting one wrong does not entail getting the
   other wrong.
4. **Degenerate and legal instances preferred over round ones.** Q14 is built
   on a zero-extent layer; Q02 on a tile whose padding positions outnumber its
   real ones; Q13 on a commit whose derived quantity holds still while the
   thing that decides the outcome moves.

### Coverage of the mandated spread

| Requirement | Items |
|---|---|
| Concrete bytes at concrete offsets (≥3) | Q01, Q02, Q03, Q04, Q11 |
| Reader/verifier verdict on a malformed file (≥2) | Q08, Q09, Q10, Q11, Q15 |
| Arithmetic — sizes, counts, alignment, coverage (≥2) | Q01, Q04, Q05, Q06, Q07, Q13 |
| Rule stated across more than one section (≥2) | Q07, Q09, Q10, Q12, Q13, Q14, Q15 |

### Coverage of the changed surface

Weighted, but not exclusively: §2.3 (Q09), §5.2 (Q07), §6.2 (Q03, Q09),
§7.2 (Q10, Q15), §9.7 (Q07), §11.1 (Q13, Q14), §13.3 (Q13), §14.2 (Q04, Q11),
§18.2 (Q10), §19.4 (Q11), §20.3 (Q12, Q13), §20.4/§20.5 (Q15), §21.1 (Q08,
Q10, Q11), §21.6 (Q14), §21.9 (Q14). Untouched-surface items — where four
prior rounds found their survivors — are Q01, Q02, Q05, Q06: §7.4's packed
inline payload, §14.3's packed boolean planes with §14.5's padding content,
§15.4's segment arithmetic, and §17.2's codec-1 length equality.

## 2. The slate

Each question is written to stand entirely alone: the answerer sees the
question text and the document, nothing else.

**Q01 — layer record inline payload.** A rank-2 planar layer, two channels of
different element sizes, no sub-records. Asks for the byte offset of
index_encoding within the inline payload, the record's inline_length,
entry_count, and the extent slot's extent_length. Draws on §7.4's field table
and packing rule, §4.2's widths, §4.6's single-byte name prefixes, §12.1's
element sizes, §11.2's ceiling division and planar C·N, and [R-CNT-17]'s
extent_length formula.

**Q02 — a packed boolean plane whose padding dominates it.** Extents (3, 3),
tile extents (2, 4), one planar bool channel with fill true, every real sample
false. Asks for the complete decoded tile image of each of the two tiles as
uppercase hex. Draws on §11.2, §11.3's padding positions, §11.4's in-tile
ordinal, §14.3's LSB-first packing and ⌈P/8⌉ size, and §14.5's rule that a
padding position carries its channel's fill — here, the fill *bit*. Also
exercises §14.3's Note distinguishing pad bits from padding positions: this
tile has many padding positions and no pad bits.

**Q03 — a trailer's CRC bytes.** All ten trailer fields given by value; asks
for the four bytes of the trailer CRC field in file order, lowercase hex.
Draws on §6.2's layout table, §4.1, §4.2 and §4.5.

**Q04 — a value's byte offset inside an interleaved decoded tile image.**
Three channels of element sizes 1, 8 and 2; rank 3. Asks for the decoded size
and the byte offset of the third channel's value at a named in-tile position.
Draws on §11.4's in-tile ordinal, §14.2's table with Q and Fᶜ, and §12.1's
element sizes — including bool's element size of 1 in an interleaved layer.

**Q05 — planar disk ordinal, index-region offset, segment index,
extent_length.** A layer with 80,000 entries, so the answer crosses a segment
boundary. Draws on §11.2, §11.4's spatial and disk ordinals, §15.1's 20-byte
entries and region layout, §15.4's segment covering, and [R-CNT-17].

**Q06 — codec 1's length equality across a mixed-type planar layer.** Channels
`m` (bool) and `v` (uint8); asks what the length field of the entry at two
named disk ordinals must carry, and the region's extent_length. Draws on
§11.4's channel-major grouping to decide *which channel* each ordinal carries,
then §14.3 versus §14.2 for the decoded size, then [R-COD-04].

**Q07 — the slack total, and whether it is partial.** A fully specified 1024-
byte file with one layer, one stored tile, and one index entry that §15.3
classifies reject-tile on a *structural* ground. Draws on §5.2's claimant
classes, §9.7's walk (including its closing sentence about structural
entries), and §15.3's paragraph on entries that yield no usable extent.

**Q08 — entry_count against the geometry.** A planar layer whose declared
entry_count is self-consistent with its extent_length but not with its
geometry. Asks for the row label, outcome, detector and detection tier. Draws
on §11.2, [R-CNT-17], §21.3 and §19.2's tiers. Built so that exactly one row
fires: the extent_length matches the formula for the *declared* entry_count,
so L22 is not exercised.

**Q09 — a file declaring a format major the reader does not implement.** Two
trailer fields are wrong by format-major-1's standards, and neither condition
reaches under [R-CNF-13]. Asks how many §21.2 rows record the file, the
requirement under which a reader refuses it, and the verifier's verdict by
§2.3's exact name. Draws on §2.3, §6.3, §21.2's opening paragraph and §21.6's
closing paragraphs.

**Q10 — a user-metadata frame whose declared content size is wrong.** Encoding
2, extent CRC verifies, frame decodes, but Frame_Content_Size disagrees with
the decoded document's byte length by one. Asks for the row, the reader's
outcome, the detection tier and whether a verifier may certify. Draws on
§18.2's replacement of two of [R-COD-06]'s constraints and its explicit
routing of this case, §21.5's R3/R4 boundary, and §21.5's closing statement
that every row there is a violation all the same.

**Q11 — a nonconforming interleaved boolean byte.** Asks what byte a reader
that chooses to return the value returns, the row label, its detector, and
whether the file is conforming. Draws on §14.2's [R-SER-08], §12.3's statement
that this is the one resolved case, §21.4's T2, and §21.1's paragraph on
verifier-detected rows.

**Q12 — six operations against §20.3's closed list.** Six yes/no answers:
a growth, a shrink, a filter change, two permitted changes taken at once, a
mid-list planar channel removal, and an append combined with a growth. Draws
on §20.3 step 4's permitted list, its fixed list, its "several of these changes
at once" clause, and its "what the line gives up" paragraph.

**Q13 — a commit under which entry_count holds still.** A planar layer whose
single commit both grows an extent and shortens the channel list, leaving C·N
unchanged while every disk ordinal moves. Asks for both entry_counts, one new
disk ordinal, and whether the tile-index region must be re-emitted in full.
Draws on §11.2, §11.4, §20.3 step 4's permitted list and re-emission clause,
and [R-WRT-04]. This is the question I am least confident every reader will
answer alike, and the reason is recorded as finding quiz-01.

**Q14 — a zero-extent layer declaring lz4 with a 2 GiB nominal tile.** Asks
whether the file is conforming, whether L44 records it, and whether a reader
declining it on §21.9's tile-size guarantee is still conforming. Draws on
§11.2, §17.2's [R-COD-07] and its Note on the addressed-tile quantifier,
§21.3's L44, §21.9's per-instance paragraph, and [R-ERR-04]'s "on that ground"
clause.

**Q15 — a compactor meeting an entry that yields no extent.** Scenario A asks
what §20.5 obliges; scenario B removes the defect and asks which of six values
the compactor carries into its output unchanged. Draws on §15.3's structural
rows, §20.5's regeneration paragraph, [R-WRT-06], [R-WRT-07] and [R-WRT-09].

## 3. What I rejected, and why

- **"How many instances does §21.4 enumerate?"** Determinate — §21.1 states
  the counting rule and I verified the whole-register total mechanically — but
  the failure mode is a miscount over 26 cells, not a misreading of a rule. A
  divergence there would indict an adding machine, not a reading.
- **Anything turning on a SHOULD.** [R-CNF-12] places SHOULD deviation outside
  the register and [R-CNT-26], [R-CNT-03], [R-CNT-09], [R-TYP-10] and
  [R-ENC-14] are all SHOULDs. A question whose answer is "the writer ought to"
  cannot fork bytes, and Appendix G's profile is non-normative besides.
- **"May a commit rename a channel of an *interleaved* layer that stores a
  tile?"** I believe the answer is yes — the fixed list names "an interleaved
  layer's channel list", lists "every channel's type and fill" separately, and
  the principle paragraph says "a name enters no map" — but "channel list" is
  doing work an implementer could read either way, and the tie-break sentence
  enumerates only two fields as standing on both sides. Recorded as finding
  quiz-02 instead of asked.
- **"Does a commit that shortens a planar channel list and appends a new
  channel in the same commit carry the removed channel's index entries
  forward?"** The re-emission clause's parenthetical "(added tiles, grown
  extents, an appended channel)" decides it, so it is not the open question it
  first looks like; but the principle offered to justify the append does not
  reach the combination. Recorded as finding quiz-03.
- **Recovery-scan questions (§9.6).** The probe is explicitly not a reader
  behavior and no verdict turns on it, so a wrong answer costs no bytes.
- **Anything requiring me to execute zstd, deflate or lz4.** I cannot fetch a
  codec implementation and would not be able to check my own question. Q10 is
  framed over what a frame *declares* rather than over what it decodes to, so
  it needs no codec.
- **A question about the front-block residency exemption alone.** [R-CNT-04],
  F1 and F6 restate each other closely enough that the question would be a
  lookup; the residency point instead appears as one clause of Q09's setup.

## 4. Findings raised while authoring

Four, reported in the structured result as quiz-01 through quiz-04. In brief:

- **quiz-01** — §13.3's `Note — sparse writing` claims that among §20.3's
  permitted declaration changes "only a change to entry_count" changes a
  layer's index content. A single commit may grow an extent and shorten a
  planar channel list at once, holding C·N constant while every disk ordinal
  moves. Non-normative text, so not byte-level, but an implementer following
  it omits a re-emission no check would catch.
- **quiz-02** — §20.3's fixed list names "an interleaved layer's channel list"
  while its permitted list lets "channel names" change without qualifying by
  layout, and the tie-break sentence enumerates only two fields as standing on
  both sides.
- **quiz-03** — the principle paragraph's "an appended planar channel adds
  tiles at ordinals after every existing one" is false of the shorten-then-
  append combination the list expressly permits.
- **quiz-04** — §5.2's three grounds for an incomplete walk include "a
  scope-level rejection ends that scope's enumeration"; tile is a scope, and
  only §9.7's closing sentence says a structural reject-tile entry leaves the
  walk complete. Decidable, but only from the other section.

I hold none of these to be byte-level, and I say so with the reasons rather
than reaching for the grade. The base rate the brief quotes is neither zero
nor high, and an over-claimed flag costs this round more than a graded one.
