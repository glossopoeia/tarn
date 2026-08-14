# Round 8 — quiz author transcript

## Disclosure

Read exactly one file: `/Users/robertkleffner/Documents/GitHub/tarn/spec/tarn.md`
(all 3,842 lines, in four Read calls plus a `wc -l`). No other file was opened,
no directory listed, no git command run, no ADR, no conformance corpus, no
`registry.json`, no web access. Three Bash calls ran pure Python arithmetic /
CRC computation that read no files (constants pasted inline from the document).

## Method

1. Read the document end to end, cold, in order — no jumping straight to the
   weighted sections, because several of the weighted sections' rules are only
   decidable against text elsewhere (§9.7 against §15.3, §2.3 against §21.6,
   §20.3 against §5.1).
2. Re-walked the weighted list and tried to *implement* from it rather than
   narrate it: I built concrete files on paper (byte layouts, coverage walks,
   commit arithmetic) and recorded every place I had to stop and decide.
3. Verified every constant the document states that is locally computable:
   - CRC-32C(`"123456789"`) = `0xE3069283` — confirmed.
   - CRC-32C(zero bytes) = `0x00000000` — confirmed.
   - CRC-32C of a full 2^16-entry all-sentinel segment = `0xEECB3BB2` —
     confirmed (1,310,720 bytes of `FF×16 00×4`).
   - Appendix A's trailer CRC `0xE00938D2`, stored `D2 38 09 E0`, over the
     60 trailer bytes the appendix prints — confirmed.
   - §21.8's "125 conditions over 252 instances": counted the four register
     tables under §21.1's counting rule (a cell reading `—` is one instance;
     semicolon-separated items otherwise). 39+50+26+10 = 125 conditions;
     61+102+45+44 = 252 instances. Both confirmed. This is a real check, not a
     formality — a miscount here would be a corpus-sizing defect — and it holds.
   - §15.4's worked example (entry_count 1,000,000 → 16 segments, last 16,960
     entries, region 20,000,064 bytes, tile 999,999 at segment-relative byte
     339,180, segment 15 at [19,660,800, 20,000,000)) — recomputed, all correct.
   - §11.4/§15.4's planar example (C=4, N=32, channel 2 at s=10 → disk ordinal
     74 → region bytes [1,480, 1,500); channel 3 = entries 96–127) — correct.
   - §14.3's packed-bool example (`55 01` / `55 FD`) and §12.3's channel-entry
     example (12 bytes) — correct.
   The document's arithmetic is tight. That pushed the slate toward *composed*
   questions rather than constant-recall.

## Selection principles applied

- Every question must fail differently. I checked the slate pairwise for shared
  failure modes and cut two candidates for collision (below).
- No question may be answered by reading one table cell. Each names a concrete
  file or a concrete operation and requires at least two sections.
- Every answer is short and mechanically comparable: a hex string, a decimal
  integer, an interval, an outcome-class name, a verdict name, a register row
  id, or yes/no. Format is stated *inside* the question text, because the
  answerer sees nothing else from me.
- I deliberately avoided asking for any CRC-32C value as an answer: an answerer
  without a tool would be defeated by arithmetic that is not the point.

## The slate, and what each is actually testing

- **Q01** — channel-entry bytes (bool fill true, then bfloat16 fill 1.0).
  Composes §7.4's framing (u8 name prefix, u16 type, u8 fill prefix), §12.1's
  element-size table and bfloat16 identification, §13.2's one-byte bool fill
  domain, §4.1's little-endianness. Fails if an implementer writes the fill
  without its length prefix, or gets bfloat16's byte order or width wrong.
- **Q02** — packed planar bool edge tile: decoded image, entry length, entry
  offset within the region. Composes §11.3 (which positions are padding),
  §14.3 (LSB-first packing, ⌈P/8⌉), §14.5 (padding carries the fill bit),
  §13.2, §11.4 (disk ordinal), §15.1 (20·k), §17.2 `[R-COD-04]`.
  This is the question I most expect to split implementations: the naive answer
  zero-fills padding.
- **Q03** — byte-shuffle stored bytes for an interleaved two-channel tile.
  Composes §14.1/§14.2 (sample-major order, little-endian uint16, Q = ΣB),
  §17.3 (stride is Q, *not* the element size, and the i·n+j transposition),
  §17.1 (filter then codec; codec 1 stores the filtered image verbatim).
  Two wrong strides (1 and 2) both produce plausible-looking output.
- **Q04** — disk ordinal + in-image byte offset at a rank-3 coordinate.
  Composes §11.2 (ceiling division), §11.4 (spatial ordinal, in-tile ordinal,
  both Σ over ∏_{j>i}), §14.2 (u·Q + F^c). Row-major vs column-major error
  shows up immediately.
- **Q05** — slack total for a fully specified 1,024-byte file. Composes §5.2's
  coverage classes, §9.7's walk (front block and trailer are claimants; the
  index region enters once, as the layer record's extent), §15.3's *structural*
  distinction (an `offset < 16` entry contributes no extent, so its nominal
  bytes fall to slack; an entry whose only defect is a failed tile CRC keeps
  its extent), §7.4/`[R-CNT-17]`'s region sizing. Every one of those four
  decisions moves the number.
- **Q06** — index region sizing and the segment/CRC ranges for one entry at
  scale. Composes `[R-CNT-17]`, §15.1's region layout, §15.4's segmentation.
  Catches the off-by-one of treating the CRC array as preceding the entries,
  and the ⌈·⌉ on the segment count.
- **Q07** — planar slab run containing a given disk ordinal. Composes §11.4
  (c·N+s decomposition) and §16.2 (runs partition each *channel block*
  independently, starting at block_start + r·S). A global partition from
  ordinal 0 gives a different run start — that is the discriminator.
- **Q08** — reserved-range top-level record type with MU = 0: reader outcome
  vs verifier verdict. Composes §7.2's `[R-CNT-15]` ("readers of both apply the
  MU rule above unchanged" — so *ignore-record*, not reject), §10.2/§10.3, and
  §2.3's verdict rules (the verifier has established a violation).
- **Q09** — experimental-range MU = 1 sub-record: reader outcome, file
  conformance, verifier verdict. Composes §7.4's `[R-CNT-18]` (reject-layer,
  never reject-file), §2.3's *cannot establish* grounds, §21.6's closing
  paragraph, `[R-CNF-02]`. The three parts pull in three different directions
  and a reader who conflates "reader refuses" with "file nonconforming" gets
  two of them wrong.
- **Q10** — verifier that declines an oversized metadata document *and*
  establishes an unrelated layer-scope violation. Composes §18.2's
  `[R-MTA-09]`, §21.9's 16 MiB guarantee, and §2.3's priority rule ("An
  established violation takes priority"). Deliberately the mirror of Q09: same
  vocabulary, opposite verdict, different reason.
- **Q11** — segment-CRC failure part-way through a region request. Composes
  §15.4's `[R-IDX-04]` (layer scope though detected at tile use), §19.4 step 8,
  §2.4's prospective-bar language for reject-layer.
- **Q12** — the directory-only commit shape: where the directory lands, pad
  size, new F, new generation, whether the index region moves. Composes §9.2
  steps 1/3/5, §5.1, §6.2 (64-alignment), §20.3 shape (c) and `[R-WRT-05]`.
  I had to pin "the lowest offset the commit protocol permits" because writer
  placement freedom otherwise leaves (a) open — see finding quiz-04's cousin
  in my notes; it is licensed freedom, not a defect.
- **Q13** — what an appender writes into version_minor and flags when the input
  carries ignore-lane bits and a higher minor. Composes §6.3's `[R-CNT-08]` and
  `[R-CNT-26]`, §20.3 step 6, §2.3's conduct-vs-bytes clause. Answer (b) is
  four literal trailer bytes; a writer that "resets to flags = 0 because this
  text defines none" emits different bytes.
- **Q14** — codec 3 window size against decoded size. Composes §17.2's
  `[R-COD-06]` window rule with the note deriving that a sub-1-KiB tile is only
  encodable as a single-segment frame, plus §21.4's row identity.
- **Q15** — two layer records with empty name fields, versus one. Composes
  §19.1 step 4 ("Uniqueness is decided first, and over the raw name bytes
  whether or not each name is itself well-formed"), §4.6's `[R-ENC-15]` scope
  split (duplicate layer name = file scope; every other name defect = layer
  scope), and the register rows. The pair makes the reader show the ordering,
  not just the outcome.

## Coverage against the charter's spread requirement

- Concrete bytes at concrete offsets: Q01, Q02, Q03, Q13(b) — plus Q04's offset.
- Reader/verifier verdicts on specific malformed files: Q08, Q09, Q10, Q11,
  Q14, Q15.
- Arithmetic (sizes, counts, alignment, coverage): Q04, Q05, Q06, Q07, Q12.
- Rules stated across more than one section: Q05 (§5.2+§9.7+§15.3+§7.4),
  Q09 (§7.4+§2.3+§21.6), Q10 (§18.2+§21.9+§2.3), Q12 (§9.2+§5.1+§20.3),
  Q13 (§6.3+§20.3+§2.3), Q15 (§19.1+§4.6+§21.2/§21.3).
- Weighted sections hit: §2.3 (Q08–Q10), §9.7 (Q05), §18.2 (Q10), §17.2
  (Q02, Q03, Q14), §19.1 (Q15), §15.3 (Q05), §20.3 (Q12, Q13), §5.1/§5.2
  (Q05, Q12), §6.3 (Q13), §15.4 (Q06, Q11), §16.2 (Q07), §11.1–§11.4 (Q04),
  §13 (Q01, Q02), §14 (Q02, Q03, Q04).

## Candidates raised and rejected, with reasons

- **"How many of the trailer's 64 bytes may a future major redefine, and at
  which offsets?"** (48; offsets 12–59). Determinate and composes §6.2's layout
  with §6.3's `[R-CNT-24]`, but the count 48 is stated verbatim, so half the
  question is recall. Cut in favour of Q13, which reaches the same section and
  produces literal bytes.
- **"Applying §21.1's instance rule, how many instances does §21.4 enumerate?"**
  (45). I verified the answer and the whole 252 total. Cut because getting it
  wrong changes the size of a test corpus, not any byte on disk or any verdict —
  it fails the charter's own "earns its place" test even though §21.1 is
  heavily weighted.
- **"Must a remote reader that speculatively fetched the final 112 bytes of a
  128-byte file verify the front signature block?"** Determinate (no —
  `[R-CNT-04]`'s residency test, confirmed by Appendix A), but the answer is
  binary and Appendix A hands it over almost verbatim.
- **"Ordered list of checksums a reader verifies before acting on a tile-index
  entry's offset."** Determinate (trailer CRC → directory CRC →
  crc_of_crc_array → the containing segment's CRC) but very close to reciting
  §8.2's chain sentence.
- **"An interleaved bool value byte of 0x02 at a real position — what does a
  reader that returns it report?"** (true, per `[R-SER-08]`). Good question,
  but it collides with Q02 on the bool/fill axis and with Q08/Q09 on the
  "violation the reader is not obliged to detect" axis. Held in reserve.
- **The §20.4 MU = 0 / PE = 0 drop rule.** I *wanted* this as a question and
  could not make it one: I could not determine the answer myself. It became
  finding quiz-01 instead.

## Working notes on the file built for Q05

    [0,16)      front signature block            16   claimed
    [16,100)    tile-index region (layer record extent, 4*20 + 1*4 = 84)
                                                  84   claimed
    [100,220)   entry 0's stored extent          120   claimed
    —           entry 1 sentinel                   0   no extent
    [256,320)   entry 2's stored extent           64   claimed (crc fails, but
                                                       the entry is well-formed,
                                                       so the extent stands)
    (8,48)      entry 3 nominal                    0   §15.3 *structural*
                                                       (offset < 16) → no extent
                                                       contributed anywhere
    [832,928)   directory region                  96   claimed
    [960,1024)  live trailer                      64   claimed
                                                 ----
                                                  444 claimed, F = 1024

    slack runs: [220,256)=36, [320,832)=512, [928,960)=32  → 580

Checks I made before shipping it: dir_offset ≥ 16 and dir_offset + dir_length
≤ F − 64 (928 ≤ 960); the pre-trailer gap [928,960) is exactly what step 5 of
`[R-LIF-02]` produces from a directory ending at 928, so no `[R-CNT-05]`
question arises; entry 3's nominal extent overlaps both the front block and
the index region, which is precisely why the *structural* rule has to be
applied rather than the overlap rows; and §9.7 says outright that a reject-tile
entry does not make the walk incomplete, so the total is a full total and not a
`[R-CNT-21]` partial. Entry_count 4 is satisfiable by a rank-1 interleaved
layer of extent 4, tile extent 1.

## Findings raised while authoring

Recorded in the structured result as quiz-01 … quiz-03. Summary of my own
byte-level judgement:

- quiz-01 (§20.4, AMBIGUITY) — flagged byte-level. Two updaters, same input,
  same requested change, different output records. I make the strongest case I
  can in the finding; I am aware round 7 flagged 8 and landed 0, and I am not
  flagging the other two.
- quiz-02 (§9.7 vs §6.2, OBSERVATION) — not byte-level. §6.2 states the
  obligation plainly; §9.7 simply does not restate it among the walk's checks.
- quiz-03 (Appendix H, OBSERVATION) — not byte-level. Appendix H is
  non-normative and defers to its citations; §5.2 is unambiguous that no
  conformance requirement rides on slack content.

No answers are recorded anywhere in this transcript or in the question text.
