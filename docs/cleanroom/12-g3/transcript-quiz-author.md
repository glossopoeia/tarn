# Round 12 — quiz author transcript

## Access disclosure

Read exactly one file: `/Users/robertkleffner/Documents/GitHub/tarn/spec/tarn.md`
(all 3,982 lines, in five reads). Ran `wc -l` and `grep` against that file only,
and Python that reads no repository files (a CRC-32C implementation plus
arithmetic), from a scratch script I wrote myself at
`scratchpad/round12/crc.py`. No ADRs, no `docs/`, no `conformance/`, no
`registry.json`, no other repo file, no git history, no web.

## Method

I did not walk the six named sections in order and narrate them. I read the
document straight through once, then built things:

1. Reproduced §4.5's check vector (`CRC-32C("123456789") = 0xE3069283`, CRC of
   zero bytes `0x00000000`) — my implementation matches, so every CRC below is
   trustworthy.
2. Reconstructed Appendix A's 128-byte file byte by byte from §6.1/§6.2/§7.1 and
   recomputed the trailer CRC: `0xE00938D2`. Matches the appendix.
3. Recomputed §15.4's all-sentinel constant: CRC-32C of 2^16 copies of
   `FF×16 00×4` = `0xEECB3BB2`. Matches. (One sentinel alone is `0xE5389D3D`,
   which the document does not state and does not need to.)
4. Built a complete single-layer file from §7.4's inline-payload field list,
   §7.2's 24-byte header, §7.1's terminal CRC, §9.2 step 5's pad rule, and
   §6.2's F-mod-64 rule, to see whether the layer record parses to a single
   determinate length. It does (inline 101, record 125, dir_length 129, F 256).
5. Built decoded tile images and stored bytes end to end for three shapes —
   interleaved with edge padding under filter 2, a packed planar bool edge tile
   with both padding positions and pad bits, and a zstd-declared tile — to
   exercise §11.2/§11.3/§14.2/§14.3/§14.5/§17.1/§17.3 together.
6. Ran §9.7's coverage walk by hand over a constructed live state containing one
   structurally-bad index entry and one crc-failing entry, to see whether the
   slack total is determinate. It is.
7. Mechanically counted §21's register: 121 rows and 248 instances under §21.1's
   counting rule (`—` counts as one instance; otherwise semicolon-separated).
   §21.2/§21.3/§21.4/§21.5 declare 36/49/26/10 and §21.8 declares 121 over 248.
   All agree. No register-arithmetic finding this round.

Where the walk forced me to guess, that became a finding rather than a question.

## The slate, and why each earns its place

Weighting: Appendix G (Q05), §9.7 (Q06), §20.3 (Q12, Q15), §13.1 (Q03, Q04,
Q15 all turn on fill authority), §4.7 and the front matter's structural/
descriptive framing (Q13). The remaining nine deliberately land in text no
recent round has had to implement from: §7.4 parsing, §14 byte layout, §15
ordinals and segments, §17.2 codec frame constraints, §18.2/§2.3 verdict
priority, §20.4's drop rule.

- Q01 — trailer CRC over a chosen field set. Concrete bytes at a concrete
  offset; needs §6.2's layout table *and* §4.5's CRC parameters *and* §4.1's
  little-endian storage. Fails only if one of those three is wrong.
- Q02 — dir_length and committed_file_length for a fully pinned one-layer file.
  Needs §7.4's field order and widths, §7.2's 24-byte header, §7.1's terminal
  CRC inside dir_length, §9.2 step 5's pad, §6.2's multiple-of-64.
- Q03 — stored bytes of an interleaved edge tile under byte-shuffle. Needs
  §11.2 grid, §11.3 padding positions, §14.5 fill-encoded padding, §14.2
  sample-major layout and stride Q, §4.1 endianness, §17.1 stage order, §17.3
  stride rule.
- Q04 — stored bytes of a packed planar bool edge tile. Disjoint from Q03: it
  turns on §14.3 LSB-first packing, the pad-bit rule, §13.2's one-byte bool
  fill, and §17.3's "for a packed boolean plane s = 1 and the filter is the
  identity". A reader who gets Q03 right can still get this wrong.
- Q05 — offset of a layer's index region under Appendix G item 3. The two
  user-metadata extents are placed to punish anyone who interleaves record
  extents per layer; item 3 says all of them come after every layer's tiles and
  index region.
- Q06 — slack total from §9.7's walk. Needs §5.2's claimant classes, §9.7's
  "a record is not a claimant of its own" and the layer-record-extent-is-the-
  index-region clause, §15.3's structural-versus-crc distinction, and
  [R-CNT-17]'s region-size formula.
- Q07 — reserved-range record type at MU = 0. Reader outcome and verifier
  verdict diverge; §10.3, §7.2 and §21.6's closing paragraphs must all be
  combined.
- Q08 — verdict priority when a declined user-metadata decode coexists with an
  established violation. §2.3 decides it; §18.2's new text is the bait.
- Q09 — per-channel result of a planar three-channel point read. §13.3, §15.3,
  §19.4 step 8, §2.4's no-fill-for-a-rejected-tile rule.
- Q10 — zstd Window_Size against a decoded size the reader computes itself.
  Arithmetic feeding a verdict.
- Q11 — the lz4 cap in a planar layer. Deliberately constructed so the correct
  planar rule says *conforming* while the wrong (interleaved-stride) reading
  says reject-layer. Asks for the governing plane's size so the reasoning is
  visible in the answer.
- Q12 — the MU = 0 / PE = 0 drop rule against a supersede-only commit versus an
  add-a-layer commit. §20.4's table row and §20.3 step 4 together.
- Q13 — a set ignore-lane bit: conforming file, ignored bit, certifiable.
  §6.3, §2.3, §2.4's SHOULD-deviation clause, §21.6.
- Q14 — planar disk ordinal, entry offset, segment index, segment-CRC offset.
  §11.2, §11.4, §15.1, §15.4 in one chain; four integers make a partial error
  visible rather than silent.
- Q15 — which stored tiles a fill change must re-emit. §11.3 padding, §14.5's
  writer MUST, §20.3's shape (c) note. The trap is answering "all four".

## Rejected candidates

- **Appendix G item 2's derived `file_id`.** I wanted a "what is the file_id"
  question. It has no determinate answer (no hash is named, the input is
  circular, and the 64-bit reduction is unstated). Became finding quiz-02.
- **"Name every descriptive field."** One-cell lookup in §4.7. Folded into Q13
  instead, where the taxonomy has to be applied rather than recited.
- **"How many instances does row L2 enumerate?"** Mechanical table reading, no
  byte consequence.
- **"Which register row does condition X exercise?"** Row-id recall, and §21.1
  already says the rule governs over the row — so a wrong row id costs nothing
  on disk.
- **A question on whether a reject-tile stops §9.7's walk.** §9.7 answers it for
  the structural case and §15.3 for the crc case, so it is decidable — but the
  phrase "a scope-level rejection blocks enumeration" reads as though tile scope
  might qualify. I judged it decided rather than open, and used the case inside
  Q06 rather than asking about it directly.
- **A question on whether an appender may emit a malformed index entry into a
  freshly written index region.** This is exactly the fork I report as finding
  quiz-01, so it cannot be a quiz item: a divergence there would be the
  document's, not the answerer's.

## Findings raised while authoring

1. quiz-01 (CONTRADICTION, byte-level) — §20.3 step 2 orders an appender to
   re-emit a malformed index entry byte-identically into a tile-index region it
   is newly authoring at a new placement, while §2.3 `[R-CNF-06]`, §20.1
   `[R-WRT-01]` and §2.3 `[R-CNF-05]` require an updater to satisfy every writer
   requirement for the bytes it produces. The justification §20.3 offers is
   `[R-WRT-05]`, which is about *records*, not about a re-authored index region.
   §20.5 `[R-WRT-06]` resolves the parallel case for compactors in the opposite
   direction ("MUST NOT emit a file carrying a violation it has detected").
2. quiz-02 (AMBIGUITY, not byte-level) — Appendix G item 2's `file_id`
   derivation names no hash function, includes "the trailer's other fields",
   which contains the trailer CRC that cannot exist before `file_id` is written,
   and does not say how a digest becomes a nonzero 64-bit value.
3. quiz-03 (OBSERVATION, not byte-level) — §4.7's "In format major 1
   `version_minor` is the only descriptive field" sits against `[R-WRT-06]` and
   `[R-CNT-26]`, under which an input file's `version_minor` determines a byte
   an updater (a reader of the file it processes, §2.3) emits.

No answers appear anywhere in this transcript or in the question texts.
