# Layout audit transcript — generation-counter removal (§2.3, §3.1, §6.2)

## Unsolicited context disclosure

Before starting, my runtime context included a CLAUDE.md pointer, the user's
email, current date, a git status/log block naming five recent commit
subjects (including "ADR-0111: the generation counter is removed, the
trailer reordered, a struck row label retired" and "Q-B9 and Q-B7 priced by
consequence sweep..."), and various tool-availability system reminders. None
of this is part of the specification or evidence about it, and I did not use
any of it as a substitute for reading the spec or the hunks themselves. I
disregarded it per the brief's instruction and do not repeat its contents
further here beyond this disclosure.

## What I read

- `/private/tmp/.../case-final/hunk-01.diff` through `hunk-04.diff` (my
  charter's four files) — read in full via the Read tool.
- `/Users/robertkleffner/Documents/GitHub/tarn-first-draft/spec/tarn.md` —
  read via `sed`/`awk` over these ranges: 140-270 (§2.3), 244-262, 388-400,
  758-900 (§6.1-§6.4), 805-846, 828-848, 858-900, 1222-1350 (§9-§9.3),
  1230-1270, 1300-1350, 4250-4325 (Appendix A/B). Plus targeted `grep -n`
  passes listed below over the whole file.
- I did **not** read `full.diff`, any hunk file outside my charter, docs/,
  ADRs, PLAN.md, OPEN-QUESTIONS.md, AGENTS.md, or git history/diff, per the
  access rule.

## Commands run (disclosure of every search)

```
wc -l spec/tarn.md                                            → 4648
grep -n "R-CNT-06" spec/tarn.md                                → 15 hits (listed below)
grep -n "generation" -i spec/tarn.md                           → ~45 hits, none referencing a removed counter field
grep -n "R-ENC-03\|R-ENC-04" spec/tarn.md                      → 21 hits, all resolve correctly
grep -n "generation number\|numbers it\|number.*generation\|generation.*number" spec/tarn.md → 1 hit (the new §3.1 bullet itself)
grep -n "trailer offset\|offset 16\|offset 24\|offset 32\|offset 40\|offset 48\|offset 56\|offset 60\|F-64\|F − 64\|F-48\|F − 48" spec/tarn.md → 16 hits, all consistent with new layout
grep -n "states ten\|other eight\|states nine\|other seven\|`[R-CNT-06]` states" spec/tarn.md → 3 hits, only the current (correct) text
grep -n "exactly as\|the same way\|likewise\|for the same reason\|on the same discipline" (scoped via awk to §2.3/§3.1/§6.2/§9.3) → 1 hit, in §2.3, unrelated to the generation removal
grep -n "dir_offset\b" spec/tarn.md                            → 12 hits, all consistent
grep -n "56 | 4\|56,4\|\[48,\|\[56,\|56 |" spec/tarn.md         → 1 hit (F15, correctly says [48,60))
grep -n -i "reserved" spec/tarn.md                              → ~55 hits; every trailer-reserved-specific one says "12" / offset 48, none say "4" / offset 56
grep -n "^| F[0-9]" spec/tarn.md | awk -F'|' '{print $2}'      → F1..F10, F12..F21... (F11 absent — the retired row, outside my charter)
grep -n "^#### 6\." spec/tarn.md                                → 758, 800, 850, 891 (confirms §6.3 at 850)
grep -n "^### 9\.\|^#### 9\." spec/tarn.md                      → confirms §9 at 1222, §9.3 at 1304
grep -n "states eight\|states ten\|nine conditions\|seven conditions\|ten conditions\|eight conditions" spec/tarn.md → 0 hits
grep -n "R-CNT-06.*states\|states.*R-CNT-06" spec/tarn.md       → 1 hit, the current text only
```

Plus a Python script (via Bash/python3) that reconstructed Appendix A's
128-byte example file from its own hex dump and independently computed:
- the trailer CRC-32C over bytes [64+0, 64+60) — got `0x402f157e`, matching
  the stored little-endian bytes `7e 15 2f 40` and the table's claimed value
  exactly;
- CRC-32C of zero bytes = `0x00000000`, matching the directory-region claim;
- CRC-32C("123456789") = `0xe3069283`, matching Appendix B's check vector.

## Header-vs-body verification (all four hunks)

For each hunk I computed, from its own `@@ -a,b +c,d @@` line and body, which
current-file line numbers its first and last **changed** (`+`) line should
land on, then checked that against `awk 'NR==...'` on the live file.

| hunk | header claims | independently computed from @@ + body | live file at that line | match |
|---|---|---|---|---|
| 01 | 249-251 | 249 ("`[R-CNT-06]` states nine, of which the") – 251 ("and the other seven do not.") | identical text at 249/251 | yes |
| 02 | 395-398 | 395 ("- **generation** — one committed state...") – 398 ("carry (§9.3).") | identical text at 395/398 | yes |
| 03 | 811-815 | 811 ("| 16 | 8 | u64 | dir_offset ...") – 815 ("| 48 | 12 | bytes | reserved ...") | identical text at 811/815 | yes |
| 04 | 837-843 | 837 ("involved: the flag gates...") – 843 ("trailer is the file. `[R-CNT-06]`") | identical text at 837/843 (verified with `awk 'NR==...'` after an initial manual-count slip on my part, corrected) | yes |

No header/body mismatch in any of the four hunks. (I initially miscounted
hunk-04's mapping by hand and suspected a 1-line offset; re-deriving with
`awk 'NR>=828&&NR<=848{print NR": "$0}'` resolved it — the header is
correct, my manual line-counting was the error, now corrected and shown
above.)

## The rule each hunk adopts, in my own words

- **Hunk 01 (§2.3):** the "reach" argument's illustrative count of how many
  conditions `[R-CNT-06]` states, and how many of those are format-major-
  invariant per `[R-CNT-24]`, is revised down by one in lockstep (10→9,
  8→7) because the generation-range condition that used to be one of
  R-CNT-06's ten no longer exists.
- **Hunk 02 (§3.1):** the term "generation" is redefined to drop any claim
  that a field numbers generations, and states instead that ordering across
  a file_id's generations comes from committed_file_length being strictly
  increasing, sourced to §9.3.
- **Hunk 03 (§6.2 table):** the trailer field table drops the generation row
  entirely, shifts dir_offset/dir_length/committed_file_length/file_id back
  8 bytes each, and widens reserved from 4 to 12 bytes at offset 48 to
  absorb the freed space, keeping the table's total at 64 bytes and the CRC
  window at [0,60) unchanged.
- **Hunk 04 (§6.2 validation gate):** the reader's mandatory-validation list
  drops the generation range check (`1 ≤ generation ≤ 2⁶³ − 1`) from the
  list of gates a reader MUST apply, leaving the other checks (and their
  order) untouched.

## The seven checks, applied

**1. Against the rule it restates.**
- Hunk 01's "nine"/"seven" is not freestanding — it must match what
  `[R-CNT-06]`'s own text (§6.2, hunk 04's paragraph) actually lists, and
  independently what §21 registers as R-CNT-06-primary rows. I counted both:
  - From the validate-gate paragraph itself: trailer magic; trailer CRC;
    committed_file_length = F; multiple of 64; dir_offset ≥ 16; dir_length ≥
    4; dir_offset+dir_length ≤ F−64; file_id ≠ 0; reserved zero = **9**.
  - From §21: rows whose **primary** (non-parenthetical) citation is
    `[R-CNT-06]` are F8, F9, F10, F12, F13, F14, F15, F16, F17 = **9** (F11
    is absent — a struck/retired row, outside my charter, consistent with
    the brief's mention of a second separable change).
  - Of these 9, the ones asserting an invariant `[R-CNT-24]` fixes across
    every major are exactly F8 (trailer magic) and F14 (trailer CRC) — R-
    CNT-24's own text fixes only the trailer-magic bytes, the
    version_major/minor bytes (not part of R-CNT-06's nine — that's R-CNT-
    07's gate), and the CRC computation. So 9 total, 2 fixed, **7** not
    fixed. All three methods agree with the hunk's "nine"/"seven" exactly.
- Hunk 02's ordering claim ("strictly increasing committed file length")
  restates `[R-LIF-02]`'s own text almost verbatim: "A commit's
  committed_file_length is strictly greater than the prior trailer's, by at
  least 128, so the committed file length orders a file's generations
  (§9.3)." Same quantifier (strict), same subject (committed_file_length),
  same scope (per file_id, per commit). `[R-LIF-03]` then uses that same
  ordering for cache-revalidation semantics. No mismatch in tense,
  quantifier, or scope between the §3.1 restatement and its §9.2/§9.3
  sources.

**2. Citations point where claimed.**
- `[R-CNT-24]` (hunks 01, 04) → §6.3, lines 861-869: fixes trailer-magic
  position, version_major/minor position, and the CRC computation across
  every major. Matches both citing uses.
- `[R-CNT-06]` (hunks 01, 03 implicitly, 04) → §6.2, lines 833-843: the
  validate-gate paragraph itself, matches.
- `[R-ENC-04]` (hunk 04) → line 471, "A reader MUST NOT allocate, seek, or
  [use a declaration-derived sum without overflow-checking it]" — matches
  the "declaration-derived quantity under `[R-ENC-04]`" claim about
  dir_offset+dir_length.
- §6.3 (hunk 04, twice: "the version gate" and "the flag gates") → confirmed
  §6.3 (line 850) contains both R-CNT-07 (version gate) and R-CNT-08 (flag
  gates).
- §9 and §9.3 (hunk 02) → confirmed §9 = "Lifecycle and Consistency" (1222)
  and §9.3 = "Generations, file_id, caching" (1304) — both on-topic and
  exactly matching what's cited.
All citations resolve to the content claimed; none point to the wrong
section or an unrelated rule.

**3. The change sits in normative text.**
- All four hunks land in flowing prose (§2.3, §3.1's term list, §6.2's
  table and validate-gate paragraph), none inside a `>` blockquote. Grepped
  the surrounding paragraphs directly (shown in the sed/awk reads above);
  none of the changed lines are prefixed with `>`. The one nearby analogy
  phrase I found in §2.3 ("binds the actor in the same way") sits in
  ordinary prose too, not a blockquote, and is unrelated to this change.
- Hunk 02's restated ordering property does depend for its *force* on
  `[R-LIF-02]`'s bare declarative ("A commit's committed_file_length is
  strictly greater than the prior trailer's..."), which per this document's
  stated convention ("a keyword-free clause is not thereby inert...calls
  them prohibitions elsewhere") carries force as a numbered requirement's
  own text, not as an unlabelled aside.

**4. No contradiction elsewhere in the same passage.**
- Read the whole of §2.3 (140-262), §3.1's term list (341-400), and all of
  §6.2 (800-891) — including text no hunk touched (e.g., the pre-trailer
  pad paragraph, the two Notes bracketing the validate-gate paragraph, the
  "In every format major version, permanently..." R-CNT-24 paragraph
  immediately following in §6.3). None of it restates a stale offset, a
  stale field, or a stale count. Full "generation" grep (45 hits) turned up
  no leftover reference to a generation *field* or *counter* — every hit is
  either the *state* sense (a committed generation of the file, unaffected
  by this change) or, in the new §3.1 bullet, the explicit "No field
  numbers generations" statement.

**5. No exhaustive claim it cannot carry.**
- The "nine"/"seven" claim is a closed count. I derived membership two
  independent ways (the validate-gate paragraph's own list; §21's primary-
  citation rows) and both land on exactly 9/7, cross-checked against
  `[R-CNT-24]`'s own text for which 2 are format-major-fixed. No smallest-
  legal-member case (e.g., a file at the 128-byte minimum, one file_id, one
  commit — Appendix A's own example) contradicts this: Appendix A's worked
  example implements exactly this 9-condition validate list against 128
  bytes, and every field position and the CRC verify by direct computation
  (see CRC check above).
- The trailer table is a complete accounting of 64 bytes: 8+2+2+4+8+8+8+8+12+4
  = 64, matching "the trailer occupies the final 64 bytes" and the CRC
  window [0,60) = 60 bytes = everything but the CRC field itself. No gap,
  no overlap.

**6. What did the change leave open?**
- The structure the change governs is the 64-byte trailer and the notion of
  ordering/identifying a file's generations. Quantities/cases: (a) trailer
  byte layout — fully re-accounted, sums to 64, verified byte-for-byte
  against Appendix A's worked hex example and independently-computed CRC;
  (b) which conditions gate acceptance — the validate-gate paragraph still
  names exactly the fields the new table defines, one gate per structural
  field (9 fields: magic, version_major [via §6.3], flags [via §6.3],
  dir_offset, dir_length, committed_file_length, file_id, reserved, CRC —
  every one gated, none left ungated); (c) how generations are ordered/
  identified — committed_file_length now carries both, and §9.3's existing
  Notes (already in place, not touched by these hunks) already cover the
  edge cases a counter used to seem to promise: no two commits of one
  file_id share an F (Note under R-LIF-03), a lower F under a known file_id
  is treated as a different/corrupted file rather than staleness, and the
  practical ceiling on F is derived from R-ENC-03's 2⁶³−1 bound and R-CNT-
  06's multiple-of-64 requirement. I looked specifically for a quantity the
  old generation counter might have uniquely supplied that's now
  ungoverned (e.g., a monotonic *count* of commits, independent of file
  size) — §9.3's own third Note already discloses this was never claimed:
  "F counts bytes, not commits...it does not number them: how many commits
  a file has undergone is not recoverable from the live trailer, and no
  field records it." That Note is untouched by any of my four hunks and
  predates this claim being retired from the *old* generation-field text
  too (the old field was described as numbering *generations*, i.e. states,
  not commits, so nothing that used to be true became false — the same
  gap existed before). No newly-ungoverned quantity found.

**7. Argument by analogy.**
- Within my four hunks: no "exactly as / the same way / likewise / for the
  same reason / on the same discipline" phrasing appears in any of the
  changed lines.
- Within the surrounding sections I was told to also audit (§2.3's full
  text, §3.1's term list, all of §6.2, §9.3): one hit, in §2.3's conduct-
  rules paragraph (line ~171, untouched by any hunk): "A writer obligation
  whose violation this specification expressly declares not to be a
  file-conformance violation binds the actor **in the same way**; §6.3's
  flags = 0 against a set ignore-lane bit and §6.2's pre-trailer gap longer
  than `[R-LIF-02]` step 5's pad are the cases this text states." Governing
  verb on both sides: "binds the actor" (both cases). Checked both cited
  cases: §6.3 says an ignore-lane bit "is not a file-conformance violation"
  (line ~876); §6.2 says a longer-than-minimum pre-trailer gap "is
  conforming, and no conforming commit produces one" (line ~822). Both
  verbs/claims range over the same set (writer conduct explicitly excepted
  from the file-conformance predicate) — analogy holds, but it is unrelated
  to the generation-removal change and predates it; not a finding.

## Derived numbers (arithmetic, shown in full)

1. Trailer table offset/width sum: 8+2+2+4+8+8+8+8+12+4 = **64**. Matches
   "trailer occupies the final 64 bytes."
2. CRC window: fields at offsets 0 through 59 inclusive (0..(60-1)) = 60
   bytes = **[0,60)**. Matches the CRC row's stated coverage.
3. R-CNT-06 condition count — method A (validate-gate paragraph's own
   list): trailer magic, trailer CRC, committed_file_length=F, multiple-of-
   64, dir_offset≥16, dir_length≥4, dir_offset+dir_length≤F−64, file_id≠0,
   reserved-zero = **9** items.
4. R-CNT-06 condition count — method B (§21 rows whose primary citation is
   `[R-CNT-06]`): F8, F9, F10, F12, F13, F14, F15, F16, F17 = **9** rows.
   Methods A and B agree.
5. Format-major-fixed subset (per `[R-CNT-24]`'s own text: fixes trailer-
   magic bytes and the CRC computation, not the value-domain gate on
   version_major, which is a different requirement, R-CNT-07): F8 and F14
   = **2**. 9 − 2 = **7**, matching "the other seven do not."
6. Appendix A trailer CRC: reconstructed the 128-byte example from its own
   published hex dump and computed CRC-32C (poly 0x82F63B78 reflected,
   init/final 0xFFFFFFFF) over file bytes [64,124) (= trailer [0,60)):
   got `0x402f157e`; stored little-endian bytes are `7e 15 2f 40` = same
   value. Independently computed CRC-32C("123456789") = `0xe3069283`,
   matching Appendix B's stated check vector, and CRC-32C(b"") = 0,
   matching the directory-region entry. All agree with the document; this
   corroborates that the reordered/widened reserved field (12 bytes at
   offset 48) is reflected correctly in the one place the whole 64 bytes
   are laid out byte-for-byte, even though Appendix A is outside my four
   hunks.

## Candidates considered and rejected

1. **Hunk-04 header off-by-something.** My first manual line-count (via a
   `sed -n '830,846p' | cat -n` where I treated the sed output's own 1-based
   line numbering as absolute) suggested the header's claimed 837-843 might
   be off by ~3-4 lines from the actual "involved:..." line. Re-derived with
   `awk 'NR==...'` printing absolute file line numbers directly and this
   was purely my own arithmetic slip translating relative sed output to
   absolute line numbers — the header is correct (verified in the table
   above). Rejected as a finding; recorded as a self-correction per the
   brief's instruction to distrust inputs including my own intermediate
   work.
2. **"12" reserved bytes width vs. the freed 8 bytes.** Considered whether
   widening reserved from 4→12 (an increase of 8, matching exactly the
   8 bytes freed by dropping the u64 `generation` field) was arithmetically
   forced or an independent, possibly-wrong choice. Recomputed the trailer
   layout from scratch assuming only the removal-and-shift (no reserved
   change) and found a 12-byte gap would open between file_id's end (48)
   and the CRC's start (60) if reserved stayed at 4 bytes — so 12 is the
   *only* width that keeps the table contiguous and the trailer at 64
   bytes. Confirmed correct, not a defect.
3. **F11's disappearance from the §21 sequence (F10 → F12).** This is the
   "struck register row" the brief mentions as a second, separable change,
   and squarely inside §21, which is outside my four hunks (§2.3, §3.1,
   §6.2 table, §6.2 validate-gate). I did not audit it further and am not
   reporting on it; noted here only as context that explains an otherwise-
   puzzling gap I found while counting R-CNT-06's primary rows.
4. **Whether dropping the generation field leaves any promise about
   *distinguishing replayed/duplicate commits* ungoverned** (check 6, see
   above) — traced through §9.3's three Notes (untouched by my hunks) and
   found the relevant guarantees (no two commits of one file_id share F;
   a lower F is a different/corrupted file, not staleness; F never counted
   commits even under the old field) already stated independently of the
   generation field's presence. Rejected as a finding — nothing new was
   left ungoverned by this specific removal.

## What I could not check

- I could not read `full.diff` or any hunk outside my charter, so I cannot
  say whether hunks elsewhere in the 31-hunk changeset (e.g., the §21 row-
  retirement, or hunks touching §9.2/§9.4-9.7 for wording I did not
  independently re-derive against source) are individually sound — only
  that nothing in the text those other hunks would have touched, as far as
  I read it while sweeping for staleness (§9.2 commit protocol,
  §9.3's Notes, Appendix A/B), still describes the old generation-field
  layout.
- I did not verify every one of the ~4600 lines of the document; searches
  were targeted at every term the four hunks introduce, remove, or depend
  on (generation, dir_offset, dir_length, committed_file_length, file_id,
  reserved, R-CNT-06, R-CNT-24, R-ENC-03, R-ENC-04, the offset/width
  literals 16/24/32/40/48/56/60/64, "states nine/ten/eight/seven"). A term
  I did not think to search for could in principle still carry a stale
  reference I did not find.

## Conclusion

No finding survives. The four hunks are internally consistent with each
other, with `[R-CNT-24]`/`[R-CNT-06]`'s own governing text, with §9.2's
commit protocol and §9.3's ordering Notes, with §21's F-row register (cross-
checked by two independent counting methods), and with Appendix A's worked
byte-level example (cross-checked by independently recomputing its CRC-32C).
Both hunk headers I most scrutinized (03 and 04, which straddle the actual
table/reorder) match the live file exactly once verified with absolute line
numbers.
