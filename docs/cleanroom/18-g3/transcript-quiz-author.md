# Round 18 — quiz author transcript

## Disclosure

Read exactly one file: `spec/tarn.md` (4,339 lines), in full, in five sequential
reads. No other file in the repository was opened, listed, or grepped. No git
history, no ADRs, no conformance corpus, no registry.json, no web access. Local
computation only: a Python CRC-32C implementation and integer arithmetic, plus
one regex pass over the *contents already read* to count register instances.
Scratch files written under the session scratchpad: `work.py`, `work2.py`, and
this transcript. The output directory was not read or listed.

## Method

1. Read the document end to end before authoring anything.
2. Built a CRC-32C implementation and validated it against every checksum
   constant the document publishes, so that any byte-producing question I ask
   has an answer I know to be determinate:
   - §4.5 check vector `CRC-32C("123456789") = 0xE3069283` — matched
   - §4.5 `CRC-32C(zero bytes) = 0x00000000` — matched
   - §15.4 full all-sentinel segment `0xEECB3BB2` — matched
   - §7.4 example, 4 sentinel entries → `0x80A34955` — matched
   - §7.4 example, crc_of_crc_array → `0xC4EE982E` — matched
   - Appendix A trailer CRC `0xE00938D2`, rebuilt field by field from §6.2's
     layout table rather than copied — matched
   That last one matters: it means my trailer serializer agrees with the
   document's own worked example, so a trailer I construct from §6.2 alone has
   a determinate CRC.
3. Then actually built things, rather than re-reading the newest paragraphs:
   a complete single-layer file (front block, index region, directory, pad,
   trailer) sized end to end; a packed boolean edge tile; a byte-shuffled
   interleaved tile; an Appendix G emission layout; a slab run.
4. Checked the register's own instance arithmetic mechanically, since §21.1
   makes it mechanical ("Instances within a cell are separated by semicolons,
   and a cell reading — is one instance"). Result: 36 + 49 + 26 + 10 = 121
   rows over 58 + 116 + 55 + 44 = 273 instances, which is exactly what §21.8
   claims. No finding there. I record it because it is the kind of claim a
   reader is invited to take on trust.

## Where I spent attention

The brief named §20.4, §20.5, §21.7, §23.1 and Appendix G as the changed
surface. Six of fifteen questions land there (Q07 Appendix G, Q12 §20.4 with
§23.1, Q13 and Q14 §20.5, Q15 §21.7). The other nine are on text no recent
round has had to implement from: §6.2's trailer layout, §15.1/§15.4's region
arithmetic, §14.2/§14.3's byte layout, §17.3's shuffle, §16.2's run
continuity, §6.2's validation order, §18.2/§21.5/§21.6's metadata-encoding
split, and §2.3's verdict-priority rule.

Two of my three findings came out of authoring, not out of reading: one
question had to be rewritten because its premise (a verifier that cannot
execute a core codec) turns out to be unreachable for a *conforming* verifier,
and one had to be re-scoped because §20.5's compactor obligation is contingent
on a placement choice the same section leaves free.

## The slate

Q01 — trailer bytes. Serialize a 64-byte trailer from stated field values;
     answer is 128 lowercase hex chars. Forces §6.2's offsets and widths,
     §4.1's little-endianness, §6.3's flag lanes (bit 18 is ignore-lane),
     §6.2's reserved-zero row, and §4.5's CRC parameters over [0, 60).
     Wrong anywhere → a trailer no reader accepts.

Q02 — all-sentinel index region, entry_count = 3. Region length, segment CRC,
     crc_of_crc_array. Combines §15.1's region shape, §15.2's 20 sentinel
     bytes, §15.4's segment/CRC-array relation, §7.4's field, §4.5. Chose 3
     rather than 4 so the §7.4 worked example cannot be copied, and rather
     than 65,536 so §15.4's published constant cannot be copied — the answer
     must be computed.

Q03 — packed planar bool edge tile. Two bytes. Combines §11.3 (which
     positions are padding), §14.3 (LSB-first packing, ⌈P/8⌉), §14.5 (padding
     positions carry the fill bit), §13.2 (bool fill encoding). Deliberately
     chose extents/tile extents making P mod 8 = 0, so pad bits do not exist
     and only padding *positions* do — §14.3's Note says these are different
     mechanisms, and an implementer who conflates them gets a different byte.

Q04 — byte-shuffle over an interleaved tile. Eighteen bytes. Combines §12.1
     element sizes, §14.2's interleaved sample-major layout and stride Q,
     §4.1 little-endian, §17.3's i·n + j placement, and §17.3's rule that the
     stride for an interleaved tile is Q and not the element size. Getting
     the stride wrong is exactly `[R-COD-10]`'s undetectable failure, so this
     is a question whose wrong answer ships silently.

Q05 — entry_count = 65,537. extent_length, the offset of segment 1's CRC
     within the region, and how many entries segment 1 covers. Sits one entry
     past the segment boundary so the ⌈⌉ term goes from 1 to 2. `[R-CNT-17]`'s
     formula is a field a reader cross-checks; an off-by-one here is a
     reject-layer verdict two implementations disagree about (L22).

Q06 — end-to-end file sizing. dir_offset, dir_length, committed_file_length
     for a one-layer file built on §7.4's 81-byte example payload. Requires
     §7.2's 24-byte header, §7.1's terminal CRC inside dir_length,
     `[R-CNT-17]`'s 84-byte region, §9.2 step 5's pad to the next 64-byte
     boundary, and §6.2's F mod 64 = 0. Placement is pinned in the question
     so the answer does not depend on writer freedom.

Q07 — Appendix G emission order. Two file offsets. Item 3 orders layers by
     ascending name bytes, tiles then index region per layer, *then* remaining
     record extents, then the directory, first structure at 16. The zero-extent
     layer contributes no structure at all (§7.4 extent (0,0), §15.4's closing
     example), which is the trap.

Q08 — slab run continuity, two cases. §16.2 makes sentinels and §15.3's
     *structural* reject-tile entries transparent to packing, and makes an
     entry that fails only its stored bytes' crc **not** transparent. The two
     cases differ only in which kind of defective entry sits at ordinal 2, and
     the required offset for the next stored tile differs accordingly. This is
     a verifier's L41 verdict.

Q09 — validation order. §6.2 fixes magic → trailer CRC → version gate, and
     §21.2's preamble names the trailer CRC as one of the two checks placed
     before the gate. A file with both a bad trailer CRC and an unimplemented
     major is recorded against one row, not the other. Two readers that order
     these differently report different things about the same bytes.

Q10 — metadata encoding, reserved vs experimental. One byte apart. §21.5's R1
     makes a reserved-range encoding a violation; §21.6 makes an
     experimental-range one a defined non-violation the verifier certifies past
     while reporting it (`[R-MTA-10]`). Same reader outcome (ignore-record),
     opposite verdicts. This is the sharpest verdict fork in the document.

Q11 — verdict priority. A declined metadata decode (`[R-MTA-09]`, a legitimate
     cannot-establish ground) co-occurring with an established violation
     (F36, reserved-range record type, verifier-detected). §2.3: "An
     established violation takes priority." Chose `[R-MTA-09]`'s ground
     deliberately — see finding quiz-02 for why the codec ground would not
     have worked.

Q12 — §20.4's MU = 0 / PE = 0 drop licence. Three records, one commit that
     supersedes one tile of layer A. The table licenses a drop only in a
     commit that *independently* changes the scope the record attaches to, and
     spells out that superseding a tile modifies that layer's record. A
     sub-record of a *different* layer is not licensed; a registered PE = 1
     type is never droppable (and §23.1 names the ancillary drop as the one
     other removal a commit has). Three distinct ways to get it wrong.

Q13 — §20.5's regeneration rule. A structural reject-tile entry meets a
     compactor that relocates the region. `[R-IDX-03]` gives the entry no
     stored extent to re-point, so regeneration cannot proceed past it, and
     `[R-WRT-06]` obliges refusal — no drop is available, a tile-index entry
     being no record §20.4's table licenses dropping. Question pins the
     relocation because the obligation is contingent on it (finding quiz-03).

Q14 — §20.5's output trailer. flags, generation, version_minor. §6.3 makes the
     compactor carry unknown ignore-lane bits forward rather than writing
     flags = 0; §20.5 fixes generation 1 and names the version_minor value.
     Asked for the value §20.5 *states* rather than what a compactor MUST
     write, because the modal strength of that clause is itself a finding
     (quiz-01) while the value it names is not in doubt.

Q15 — §21.7's account of what nothing witnesses. A commit changes only a
     layer's filter field on a layer whose tiles stay stored. §20.3 step 4 bars
     it; §21.7 says the bar is witnessed only through §14-constrained content,
     the decoded size, or the codec. Chose a geometry with no padding positions
     (16/8 = 2 exactly), no bool channel, an unchanged decoded size and an
     unchanged codec, so every listed witness is closed off. The answer is a
     word, and the wrong answer is a row label.

## Coverage against the charter

- Concrete bytes at concrete offsets: Q01, Q02, Q03, Q04, Q06, Q07 (six).
- Reader/verifier verdicts on a specific malformed file: Q09, Q10, Q11, Q13
  (four).
- Arithmetic — sizes, counts, alignment, coverage: Q05, Q06, Q07, Q08 (four).
- Rules whose statement is spread across more than one section: Q06
  (§6.2/§7.1/§7.2/§7.4/§9.2), Q08 (§15.3/§16.2/§21.3), Q10
  (§18.2/§21.5/§21.6), Q11 (§2.3/§18.2/§21.2), Q12 (§20.3/§20.4/§23.1),
  Q15 (§20.3/§21.7/§21.4).
- Changed surface: Q07, Q12, Q13, Q14, Q15 — plus Q14's §6.3 half.

No two questions fail for the same reason. The two §20.5 questions test
disjoint clauses (entry regeneration vs. trailer field carry-forward). The two
verifier-verdict questions test disjoint mechanisms (violation vs.
non-violation classification; priority of an established violation over an
unchecked requirement). Q02 and Q05 are both index arithmetic but one is a
CRC over bytes and the other a ⌈⌉ boundary.

## Questions I considered and rejected

- **"How many instances does §21.3 enumerate?"** Mechanically determinate
  under §21.1's counting rules, and I verified the whole register comes to
  273. Rejected as tedious rather than pointed: it tests semicolon counting,
  not the format.

- **A verifier that cannot execute codec 3.** Drafted, then discarded: no
  *conforming* verifier can be in that position, because all four codecs are
  core. Recorded as finding quiz-02 and the question re-based on
  `[R-MTA-09]`'s size bound, which is a reachable ground.

- **"Smallest F admitting dir_length = 100 at dir_offset = 16."** Determinate
  (the ≤ F − 64 bound plus F mod 64 = 0), but it exercises one table row's
  constraints and nothing else. Q06 does the same arithmetic inside a file
  that has to be built.

- **Interleaved value offset with a bool channel mid-stride.** A good
  question (u·Q + Fᶜ with Bᶜ = 1 for bool), dropped for space because Q04
  already forces the interleaved layout arithmetic, and I preferred to spend
  the slot on §21.7.

- **"Which register row does an experimental-range type with MU = 1 fall
  under?"** Rejected: §21.6 answers it directly — it is not a register row at
  all — so the question quotes a paragraph back.

- **A question turning on the compactor's file_id.** The value is a fresh
  random draw and so not a checkable answer; the only checkable part
  (Appendix G item 2 sends a profile-adopting compactor to `[R-WRT-06]`'s
  draw rather than the derived hash) is a yes/no I could not phrase without
  telegraphing it.

- **A question on §5.2's partial slack total.** The rule is clear and the
  arithmetic (F less the claimed bytes) is determinate, but constructing a
  scenario in which the walk provably stops at a stated point took more
  premise than the answer was worth.

## Findings

Three, reported in the structured result as quiz-01 through quiz-03. One
AMBIGUITY (§20.5's version_minor clause carries no BCP 14 modal where every
neighbouring compactor obligation in the same paragraph is an explicit MUST)
and two OBSERVATIONs (§2.3's codec/filter cannot-establish ground is
unreachable for a conforming verifier; §20.5's compactor-refusal obligation is
contingent on a placement choice §20.5 itself leaves free).

No answers appear anywhere in this transcript or in any question text.
