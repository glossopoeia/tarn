# Working notes — quiz-compare-a

Scratch dir: /private/tmp/claude-501/-Users-robertkleffner-Documents-GitHub-tarn-first-draft/fidelity-2/scratch/quiz-compare-a/
Files read: only
  - /Users/robertkleffner/Documents/GitHub/tarn-first-draft/scratch/cleanroom/editions/a/tarn.md (edition A, 4981 lines)
  - /Users/robertkleffner/Documents/GitHub/tarn-first-draft/scratch/cleanroom/editions/c/tarn.md (edition B for this task, 4885 lines)

Method: grep -n for requirement IDs / distinctive phrases in both files, then
targeted `sed -n` prints of the surrounding passage in each edition, and in
several cases a direct `diff` of the aligned line ranges to check for any
byte-level wording difference at all.

## quiza-quiza-04 (trailer torn / recovery scan, §9.4-9.6, R-LIF-05/06)
- grep "R-LIF-05" and "R-LIF-06" in both files: same hit pattern/line offsets
  (edition B's file is 96 lines shorter overall, consistent with a uniform
  shift, not local deletion).
- Printed A lines 1330-1470 and C lines 1227-1367 side by side: §9.2 Note,
  §9.3, §9.4, §9.5, §9.6 text is IDENTICAL word for word, including the
  R-LIF-05 sentence ("The default read path is trailer-at-end-or-fail: a
  reader that finds no valid trailer in the final 64 bytes MUST report the
  file torn or invalid and MUST NOT scan backward.") and the §9.6 heading
  "Recovery scan (not a reader behavior)".
- grep "| F8 |" in both: identical row, same wording, same requirement tag
  R-CNT-06, same actor/phase (reader/open).
- Control search: grep "torn or invalid" - present in both editions (proves
  the search apparatus finds text that is actually there, not a tooling
  false-zero).
- Conclusion: no divergence between the editions on the cited passages. Both
  takers reached the same correct answer via effectively the same text.
  B's citation of `[R-LIF-06]` for "recovery scan is a separate operation" is
  loosely attached (R-LIF-06 is actually the shorten-a-file rule elsewhere;
  the "not a reader behavior" phrase is the §9.6 heading, untagged) but this
  is a citation looseness, not a misreading of decisive text, and not an
  edition difference.

## quiza-quiza-05 (crc_of_crc_array coverage / purpose, §4.5, §7.4, §8.1)
- grep "crc_of_crc_array" in both: same count, same contexts at shifted line
  numbers.
- Printed A 500-560 vs C 400-460 (§4.5 Checksums): identical text.
- Printed A 1225-1262 vs C 1130-1160 (§8.1 Coverage map table, including the
  "Directory region | final 4 bytes of the region | the preceding
  dir_length − 4 bytes (the raw record sequence)" row and the
  "Tile-index region | ... itself covered by the layer record's
  crc_of_crc_array" row): identical text, identical table.
- Conclusion: no divergence. Both takers derive (a) directory region's
  terminal checksum and (b) the segment-CRC array from the same table row
  in both editions.

## quiza-quiza-10 (user-metadata doc content-size mismatch, §18.2 R-MTA-09,
   contrast with §17.2 R-COD-06)
- grep "R-MTA-09" and "R-COD-06": same hit pattern in both files.
- Printed A 2670-2750 vs C 2567-2650 (the §18.2 paragraph on encoding-2
  documents, the content-size-field rule, and the R4/R3 routing): identical
  text, sentence for sentence, including "The frame's content-size field,
  unlike the decoded size and the window, is *not* left to the reader: it
  MAY be present, and when present it MUST equal the byte length of the
  decoded document. A mismatch is one of the frame constraints R4
  registers, not a failure to decode under R3..."
- diff of full §17.2 Codecs section (A 2449-2575 vs C 2346-2472): zero
  output — byte-for-byte identical.
- Conclusion: no divergence. Both (a)/(b)/(c) answers restate the same rule
  and the same tile-vs-document contrast found in identical text in both
  editions.

## quiza-quiza-13 (unimplemented experimental-range sub-record MU=1 blocks
   layer drop, §20.4)
- grep "^#### 20\.4" in both: single match each.
- diff of full §20.4 section (A 3475-3551 vs C 3372-3448): zero output —
  byte-for-byte identical, including the MU=1 table row ("At layer scope an
  unknown critical record blocks modification of that layer, its drop
  included, leaving other layers editable (`[R-CNT-18]`)") and the
  "stored flags are authoritative" sentence tied to R-CNT-15/§7.3.
- Conclusion: no divergence. Both takers answer "no" on the same rule chain
  (unimplemented type -> stored flags authoritative -> MU=1 -> blocks drop
  at layer scope), reached from identical text.

## quiza-quiza-15 (verifier verdict priority + mandatory per-requirement
   report, §2.3 R-CNF-11)
- grep "R-CNF-11": present in both files at a shifted but parallel set of
  contexts.
- Printed A 230-251 (end of §2.3, the Conforming-verifier bullet ending in
  R-CNF-11) vs C 240-265 (aligned bullet as it appears earlier in C's
  restructured §2/§3 ordering): substance identical — "An established
  violation takes priority: a verifier that has established any violation
  reports nonconforming, however many requirements it was unable to check,
  and cannot establish is available only to a traversal that established no
  violation. A verifier MUST report each requirement it was unable to check
  on a capability or resource ground, naming the requirement and the
  ground, whichever of the three verdicts it reports."  Both editions state
  this with only cosmetic rewording (edition C folds two sentences that A
  keeps separate, and reorders the *unexamined* clause slightly), no rule,
  quantifier or scope is added, dropped, narrowed or widened.
- Conclusion: no divergence. Both takers' (a) nonconforming, (b) yes with
  requirement+ground answers restate the same rule.

## Overall
All five mechanically-flagged divergences turn out, on inspection of the
cited (and surrounding) passages in both editions, to rest on textually
identical or substantively identical passages. None is a LOSS, ADDITION,
or REPORTER_ERROR; all five are EQUIVALENT — the takers' answers differ
only in wording/citation style, not in what the two editions decide.
