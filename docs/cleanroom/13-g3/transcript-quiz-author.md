# Cleanroom round 13 — quiz author transcript

## Disclosure

Read exactly one file: `/Users/robertkleffner/Documents/GitHub/tarn/spec/tarn.md`
(all 4,128 lines, in five Read calls plus one `wc -l` and one `rg` over that
same file). No ADRs, no docs/, no conformance/, no registry.json, no git
history, no web. Ran local Python (no file input) to recompute CRC-32C
constants and to check the arithmetic behind every question I authored.
Nothing else was read or listed.

## Method

I read the document end to end once, then went back and built things from it:

1. Recomputed every CRC constant the document states, from the CRC-32C
   parameters in §4.5 alone (polynomial 0x1EDC6F41 → reflected 0x82F63B78,
   init 0xFFFFFFFF, reflected in/out, final XOR).
2. Constructed several complete layer records byte by byte from §7.4's
   field table, sized their inline payloads, and sized the smallest whole
   file that could carry one.
3. Walked the reader algorithm (§19.1–§19.4) against several malformed
   files I invented, and the verifier's verdict machinery (§2.3, §9.7,
   §17.4, §18.2, §21.6) against several conforming-but-refused ones.
4. Counted §21's register mechanically against §21.1's instance criterion.

### Constants recomputed and confirmed

| Claim | Section | Recomputed |
|---|---|---|
| CRC-32C("123456789") = 0xE3069283 | §4.5 | matches |
| CRC-32C(zero bytes) = 0x00000000 | §4.5 | matches |
| 80-byte array of 4 sentinel entries → 0x80A34955, stored `55 49 A3 80` | §7.4 example | matches |
| crc_of_crc_array over `55 49 A3 80` = 0xC4EE982E | §7.4 example | matches |
| full all-sentinel segment (2^16 entries) → 0xEECB3BB2 | §15.4, App B | matches |
| Appendix A trailer CRC = 0xE00938D2, stored `D2 38 09 E0` | App A | matches |

The §7.4 worked example is internally exact in every other respect too:
inline payload 4 + 34 + 18 + 12 + 13 = 81, offsets in the hex dump land where
the field table puts them, extent length 4·20 + ⌈4/2^16⌉·4 = 84.

### Register arithmetic recomputed

§21.2 = 36 rows, §21.3 = 49, §21.4 = 26, §21.5 = 10 → 121 conditions, which
is what §21.8 states. Counting instances by §21.1's rule (semicolon
separators; a cell reading `—` is one instance): 56 + 110 + 54 + 44 = 264,
which is also what §21.8 states. No defect here.

### Where I had to guess

Three places, all written up as findings. None of them forks bytes:

- §21.1's instance criterion is applied in two different ways inside §21.4
  (T3/T14 enumerate longer/shorter; T22, the same "does not equal the
  decoded size" shape, does not). Decided only because §21.1 concedes the
  cell is authored, not derived.
- The detection tier for a layer record whose name field overruns its
  inline_length: §19.1 step 4 puts the discovery at the open, §21.3 L23's
  *Detected* cell says layer access.
- Whether a pre-trailer pad longer than the pad to the next 64-byte
  boundary makes a file nonconforming: `[R-LIF-02]` step 5 is a MUST,
  §6.2 says a longer gap is conforming, and `[R-CNF-02]` names exactly one
  conduct carve-out and it is not this one.

I looked hard for a propagation-class defect (a rule changed in one place
and left standing in another) and did not find one. The places I checked
that came out consistent: the "cannot establish" ground lists in §2.3,
§17.4 and §18.2; the metadata-encoding value partition across §10.2,
§18.2, §21.5 R1 and §21.6; the A / A_slab / S bounds across §7.4, §16.1,
§16.2, §21.3 L29/L39, §21.9 and Appendix B; the coverage-walk claimant
list across §5.2, §9.7 and §22.3; the decoded-size formulas across §14.2,
§14.3, §17.2's lz4 cap and §21.3 L44 / §21.4 T3/T14/T21/T22; the reader
capability list across §2.3, §12.1, §17.2, §17.3, §18.2 and Appendix H.

## The slate, and why each question earns its place

**Q01 — extent growth across a stored edge tile.** §11.1's rationale, §11.2's
grid arithmetic, §14.5's padding content and §20.3's step-4 prohibition all
have to be held at once. The prohibition bars changes that alter "the set of
padding positions", and growth does exactly that — the carve-out
("an extent MAY always grow") is what resolves it, and the grid-count test is
what decides whether the index is re-emitted. Three yes/no answers.

**Q02 — byte offset of one channel's value inside a decoded interleaved
tile.** Rank 3, four channels of four different element sizes. Needs
§11.4's in-tile ordinal (Σ uᵢ·∏_{j>i} Tⱼ), §14.2's offset table, and §12.1's
element sizes. Wrong answer = wrong bytes read from a valid file.

**Q03 — decoded bytes of a packed planar bool tile with padding positions
and pad bits.** §14.3's LSB-first packing, §14.5's fill-encoded padding
*and* fill-carrying pad bits, §11.3's padding positions, §11.4's in-tile
ordinal. Two bytes of hex; getting any of the four rules wrong changes them.

**Q04 — stored bytes of a filtered tile.** §14.2 (sample stride Q, decoded
image), §17.3 (shuffle at stride Q for interleaved, i·n + j placement),
§17.1 (filter then codec), §4.1 (little-endian). Twelve bytes of hex.

**Q05 — a trailer CRC.** §6.2's field table and §4.5's CRC parameters. The
one question that is pure byte production at fixed offsets; different values
from Appendix A's so it cannot be copied.

**Q06 — the smallest conforming file carrying one layer.** §7.4's field
list (including the fill field's own length prefix, which is the easy miss),
§7.2's 24-byte header, §7.1's terminal CRC, §11.1/§11.2's zero-extent
geometry, §7.4 + `[R-CNT-17]` + `[R-CNT-23]`'s forced (0,0) slot and zero
crc_of_crc_array, and §6.2's 64-alignment of the trailer.

**Q07 — a slab run containing a structurally malformed entry.** §15.3's
row for offset = S with length ≠ S, and §16.2's rule that such entries are
transparent to run continuity while a crc-failing one is not. Two
implementations that read this differently disagree about whether the file
is nonconforming.

**Q08 — reserved vs experimental metadata encoding.** §10.2's partition,
§18.2, §21.5 R1, §21.6's non-violation row, `[R-MTA-10]`. Same outcome class
for a reader (ignore-record), opposite verdicts for a verifier. Asked as a
pair so the question cannot be passed by conflating the two ranges.

**Q09 — verdict priority.** §2.3's "an established violation takes
priority", §17.4's cannot-establish ground, `[R-TYP-07]`'s reader-detected
bool fill. A verifier that reports *cannot establish* here has certified
nothing and mislabeled a broken file.

**Q10 — the two ranges a reader fetches to use one index entry.** §15.1's
region layout, §15.4's segment definition, `[R-CNT-17]`'s length formula.
Four integers. Deliberately does not reuse the linearization arithmetic of
Q02, so the two cannot fail together.

**Q11 — an oversize user-metadata document.** §21.9's minimum guarantee,
`[R-ERR-04]`'s scope rule, §18.2's note on where a resource decline lands,
`[R-MTA-09]`'s verifier consequence. Three tokens.

**Q12 — the lz4 decoded-size cap under two layouts.** §17.2's cap and its
"largest plane governs" clause, §14.2's P·Q, §14.3's ⌈P/8⌉. Numbers chosen
so that planar passes and interleaved fails — a layer one implementation
accepts and another rejects.

**Q13 — dropping an MU = 0 / PE = 0 record.** §20.4's table row, read
against §20.3's account of what a supersede changes. Three candidate
commits, one letter of answer.

**Q14 — the slack total.** §5.2's coverage classes, §9.7's claimant walk
(including that the front block and live trailer are claimed, and that a
record is not a claimant of its own header), §15.1's region size. A verifier
that double-counts the layer record inside the directory gets a different
number.

**Q15 — which register row a file is recorded against.** §21.1's
specialization paragraph, §21.2's F35/F36 pair, §10.2's reserved range.

## Questions I drafted and rejected

- **Total instance count of §21.5 (44).** Mechanical semicolon counting;
  combines two places but decides nothing about bytes, and a miscount by one
  would read as a divergence about the document rather than about a file.
- **"Is a 128-byte pre-trailer pad conforming?"** — this is my third
  finding, and asking it as a question would score a real indeterminacy as
  an answerer's error.
- **"At what tier is an overrunning layer-record name field detected?"** —
  my second finding; same problem.
- **A second CRC question over a directory region.** Would fail together
  with Q05 for any answerer whose CRC-32C is wrong (reflection or final XOR).
  One CRC question is enough.
- **"Give extent_length for entry_count = 131,072."** Shares the
  ⌈entry_count/2^16⌉ term with Q10; dropped in favour of Q11.
- **"Give inline_length for a planar two-channel layer record."** Shares
  the §7.4 payload-sizing failure mode with Q06 (specifically, forgetting
  the fill field's length prefix). Kept the richer of the two.
- **Anything turning on the §7.4 or Appendix A worked examples.** Both are
  correct, so such a question tests transcription rather than the document.

## Note on what I did not put in the questions

No answers are recorded anywhere in this transcript or in the question text.
The arithmetic above is stated as *what I checked*, not as *what the answer
is*, except for the register counts, which are the document's own published
figures (§21.8) and are not the subject of any question on the slate.
