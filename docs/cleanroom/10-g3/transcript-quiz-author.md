# Round 10 — quiz author transcript

## Disclosure of what I read and ran

Read exactly one file: `/Users/robertkleffner/Documents/GitHub/tarn/spec/tarn.md`
(3,919 lines, read in full across five `Read` calls, plus one `wc -l`).

No other file in the repository was opened, listed, grepped, or otherwise
inspected. No `docs/`, no `conformance/`, no `spec/registry.json`, no
`PLAN.md`/`AGENTS.md`/`README.md`, no git history, no `git log`/`git diff`,
no web search, no web fetch, no directory listings.

Local computation run (reads no repository file except the spec, and only
through `awk`/`grep` on that one path):

- `python3` script in my own scratchpad implementing CRC-32C (Castagnoli,
  reflected, init 0xFFFFFFFF, final XOR 0xFFFFFFFF) — self-tested against
  the document's own check vectors `CRC32C("123456789") = 0xE3069283` and
  `CRC32C(<empty>) = 0x00000000`, and cross-checked against Appendix A's
  trailer CRC `0xE00938D2` and §15.4's full all-sentinel segment constant
  `0xEECB3BB2`. Both reproduced exactly, which validates both the checksum
  implementation and my reading of the trailer field layout and the
  20-byte sentinel entry.
- `awk`/`python3` over lines 3062–3215 of the spec to count the Instances
  column of §21.2–§21.5 mechanically under §21.1's counting rule.
- `grep -oE` over the spec alone to enumerate every citation of a register
  row label (`F<n>`, `L<n>`, `T<n>`, `R<n>`) outside the register tables.

Wrote only into my scratchpad: `round10/calc.py`, this transcript.

I did not record answers anywhere.

## How I read the document

Full cold read, front to back, then targeted re-reads of the sections the
brief weighted: §21.3, §21.2, §20.5, §4.7, Appendix G, §20.4, Appendix H,
§21.6, front matter, §21.9, then §21.4, §23.1, §2.3, §21.1, §6.2, §9.6,
§19.1, §21.5, §21.8, Appendix B.

Because the brief warned that a wholesale re-labelling of register rows had
happened, my first mechanical pass was to enumerate every cross-reference to
a row label anywhere outside the register tables and check each against the
row it now lands on:

- §9.6 → F8, F17 (trailer magic; committed_file_length vs transport size) — correct
- §17.2 note → T24 (decode does not consume the extent exactly) — correct
- §21.1 specializations → F1⊂F6, F1⊂F8, F35⊂F36, L24⊂L25 — all four hold
- §21.1 instance examples → T24 "any codec", T15, T25 — all three match
- §21.2 F33 → F9/F10, F31/F32, L16/L17, T8/T9 — all four bounds pairs correct,
  and together they do cover every claimant class F33 excludes
- §21.4 T2 → T4; T13 → T25; T26 → T2/T4 — all correct
- §21.6 → F36/L25, F18, F35/F36/L24/L25 — correct
- Appendix H → F7, F36, L25 — correct

So the re-labelling appears to have been propagated. I found no stale row
citation. That is a null result, not a question, so it does not appear in
the slate; it is why I spent the rest of my effort on arithmetic and on
implementing things rather than on further label auditing.

Second mechanical pass: the register's own arithmetic. Counting the
Instances column under §21.1's rules (semicolons separate; a cell reading
`—` is one instance; a family stated as one range is one instance):

    §21.2  36 rows   53 instances
    §21.3  49 rows  106 instances
    §21.4  26 rows   45 instances
    §21.5  10 rows   44 instances
    total 121 rows  248 instances

which is exactly §21.8's "121 conditions over 248 instances". The register
is internally consistent on this axis. That gave me confidence the counting
rule itself is determinate enough to ask about (Q12).

Third pass: I re-derived every worked numeric example in the document
(§11.2, §11.4, §12.3, §14.2, §14.3, §14.5, §15.4 ×2, §17.3, §20.3,
Appendix A, §21.9's note on 2^32 → 256 KiB and 2^36 → 4 MiB). All of them
reproduce. So I built my byte questions on *different* shapes than the ones
the document already works out, so that an answerer cannot pattern-match a
printed example.

## The slate, and why each question is there

Byte-production questions (4 of 15 — the brief asked for at least three):

- **Q01 trailer bytes at [304, 320)**. Requires laying out §6.2's table
  correctly (including that `flags` is the u32 at offset 12 and that the
  ignore-lane bit set here does not change anything), then computing
  CRC-32C over trailer bytes [0, 60) with §4.5's exact parameters. A
  wrong field order or a CRC-32 (Ethernet polynomial) instead of CRC-32C
  produces four wrong bytes at the file's very end. Deliberately *not*
  Appendix A's file: different F, generation, minor, flags, file_id.
- **Q02 packed planar bool tile**. Combines §11.2's grid arithmetic,
  §11.3's padding positions, §14.3's LSB-first packing and ⌈P/8⌉ size,
  §14.5's rule that padding positions carry the fill *bit* and that pad
  bits carry it too, and §13.2's one-byte bool fill. Two bytes of answer,
  and both bytes are wrong if either the padding rule or the pad-bit rule
  is missed. Chose extents (3, 2) against tile extents (3, 3) so that
  padding positions and pad bits are *both* present and distinguishable —
  §14.3's note insists they are different mechanisms.
- **Q03 interleaved decoded image**. Same padding rule but through §14.2's
  stride arithmetic instead: the answerer has to find which in-tile
  ordinal falls at byte offset 6 and notice it is a padding position, then
  emit both channels' recorded fill in declared channel order, with the
  int16 fill bytes passed through verbatim (§12.3, §13.1).
- **Q05 all-sentinel partial segment**. §15.4's constant `0xEECB3BB2` is a
  trap: it is licensed only for a *full* segment, and "a partial segment's
  CRC MUST be computed". Three entries is a partial segment, so the answer
  is a computed CRC over 60 bytes, then a second CRC over the 4 stored
  bytes for `crc_of_crc_array`, plus §7.4/`[R-CNT-17]`'s extent_length
  formula. A reader who reaches for the constant emits four wrong bytes
  and a wrong layer record field.

Verdict questions (the brief asked for at least two; I have four):

- **Q06** two verifier verdicts. Tests §2.3's priority rule ("An
  established violation takes priority") against `[R-COD-11]`'s
  cannot-establish ground, and separately `[R-MTA-09]`'s decline. The two
  halves fail for different reasons, so they do not collapse.
- **Q07** two layer records with byte-identical *ill-formed* name fields.
  §19.1 step 4 fixes the order — uniqueness first, over raw bytes, "even
  when neither name is valid" — so the outcome is reject-file, not the
  reject-layer that L3 would give. Getting this wrong wrongly *serves* a
  file this specification rejects entire.
- **Q11** experimental-range MU = 1 sub-record. Three answers that pull
  apart deliberately: reject-*layer* (not file, `[R-CNT-18]`), compaction
  barred outright (`[R-WRT-06]`, whole file, not just that layer), and the
  file nevertheless *conforming* (§21.6's closing, `[R-CNF-02]`).
- **Q15** file_id at 2^64 − 1 versus generation at 2^63. §4.2's value
  domain covers "every offset, length, extent, and count"; file_id is a
  semantic identifier and none of those, and §6.2's table constrains it
  only to ≠ 0, and §21.2's F2 instance list pointedly omits it. A reader
  that applies the domain rule to file_id rejects conforming files.

Arithmetic:

- **Q04** five integers from one layer declaration: addressed-tile count
  under planar (C·N, §11.2), `[R-CNT-17]`'s extent_length, the
  channel-major disk ordinal (§11.4), the entry's region byte offset
  (§15.1), and the permanent row-major in-tile ordinal (§11.4). Every one
  of the five is a different rule; a wrong grid count poisons only some.
- **Q09** §9.6's probe start on a 1,000-byte physical file. The largest
  64-aligned o with o + 64 ≤ 1000 is 896, not 960 and not 936. Plus the
  candidate's required committed_file_length.
- **Q12** the Instances total of §21.4 under §21.1's counting rule.
- **Q14** slack accounting on a file with an over-long pre-trailer gap,
  which doubles as a conformance verdict.

Multi-section rules:

- **Q08** front-block residency across §6.1, §6.4 and §19.1 step 1, with
  the three cases the document distinguishes: local/mapped, a suffix
  window that does not reach 0, and a suffix window that swallows the
  whole file. Appendix A discusses the third case for its own 128-byte
  file; I used a 40,000-byte file so it cannot be answered by recall.
- **Q10** the compactor's output trailer: version_minor from §6.3's
  `[R-CNT-26]` floor maxed with the input's, generation 1 and a fresh
  file_id from §9.3/§20.5, ignore-lane bits copied forward from §6.3.
  Four fields, four different sections.
- **Q13** the checksum chain over a tile-index entry's own crc field.
  §4.5 classifies it as an *interior* checksum field; §8.1's map gives
  each covering relation; §7.4 places crc_of_crc_array inside the layer
  record's inline payload, which is what makes the directory CRC the
  terminal link. Three items, ordered.

## What I rejected, and why

- **Anything answerable from one cell.** Dropped several drafts that were
  really "what does row L33 say".
- **A question on Appendix G's emission order.** I wanted one, because the
  appendix is heavily weighted and is the only place claiming byte
  determinism. But item 3 does not give a total order over the several
  type-0x0002 record extents a file can carry (see finding quiz-05), so no
  determinate answer exists. Became a finding instead.
- **A question on Appendix G item 2's file_id.** Same reason: no hash is
  named, no truncation rule is given, and the input set is circular with
  respect to the trailer CRC field. Finding quiz-06.
- **"Which taxonomy class does a layer record's `name` field carry?"**
  §4.7 says every field is classified and §4.7's note says the layer
  record's payload table omits the class column because "each field's
  class follows from the definitions above" — but for a name it does not
  follow. Finding quiz-04.
- **A question on whether a compactor may clear a slab declaration.** I
  believe the answer is "no, and it must therefore re-establish the run
  invariants", but §20.5's "free to place structures anywhere §5.2 admits"
  cuts the other way and never cites `[R-SLB-03]`. Too close to call, so
  it is finding quiz-02 rather than a question.
- **A question on dropping an MU = 0 / PE = 0 layer sub-record in a
  tiles-only commit.** Same treatment — finding quiz-01.
- **A question built on §21.8/§24 vector construction for a
  verifier-detected reject-layer row.** `[R-VEC-04]` demands a "scope no
  reader is permitted to serve", which for those rows does not exist.
  Finding quiz-03.
- **A second duplicate-layer-name question** (name field overrunning
  inline_length, so it yields no name to compare). Cut because it shares
  §19.1 step 4 with Q07 and would fail together with it.
- **Two register-counting questions.** One is enough; a second would fail
  for the same reason as the first.

## Where I had to guess while implementing

Writing Q02 and Q03 meant deciding, from the text alone, that a padding
position in an interleaved tile carries each channel's recorded fill bytes
in declared channel order at that position's stride slot, and that in a
packed plane a padding position carries the fill *bit* while the final
byte's unused high bits carry it as well. §14.5 states both explicitly, so
that was not a guess. Writing Q14 I had to decide whether an over-long
pre-trailer gap makes a file nonconforming; §6.2 says outright that a
longer gap is conforming, and §21.1's normative completeness clause means
the absence of a register row settles it — but §9.2 step 5 states the pad
as a MUST, and that pairing is finding quiz-07.
