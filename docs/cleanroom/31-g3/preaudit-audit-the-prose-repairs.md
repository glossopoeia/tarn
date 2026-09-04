# Audit transcript — lane "the-prose-repairs" (hunks 01, 08, 23)

## Disclosure

Read: /private/tmp/claude-501/.../r31-audit/case/hunk-01.diff, hunk-08.diff, hunk-23.diff
(nothing else in case/; did not list it; did not open full.diff).
Read from spec/tarn.md by `sed -n`: lines 117-151 (§2.2), 152-260 (§2.3 and the reach
paragraph), 806-856 (§6.2), 856-900 (§6.3), 1480-1500 (§9.7), 1530-1602 (§10.2-10.4),
2540-2600 (§17.3 tail, §17.4, §18.1 head), 2604-2780 (§18.2 whole), 2925-2940 (§19.2),
3452-3595 (§20.5 whole), 3597-3683 (§21.1), 3831-3920 (§21.5, §21.6), 4130-4155 (§22.3),
4535-4720 (Appendix G whole, Appendix H head), 4740-4770 (Appendix H tail).
Ran: grep -n on the phrases listed under "Sweeps"; one python3 heredoc that read only
spec/tarn.md and normalised whitespace to count wrap-spanning phrases (no file written).
Wrote: only this file. Nothing written to the scratch directory (no scripts needed;
the python was an inline heredoc that read only the spec).
Context I did not ask for: my runtime placed a project-instruction pointer, a memory
index of four note titles, and an environment block naming recent commit subjects in
my context before I began. I did not act on any of it; none of it is cited below.

## Hunk headers vs bodies

- hunk-01: header says lines 224-228 under heading line 152 "2.3 Conformance classes".
  Body text found verbatim at 224-228 inside the "Conforming verifier" bullet. Match.
- hunk-08: header says 2577-2579 under 2563 "17.4 Certification under codecs". Found
  at 2577-2579. Match.
- hunk-23: header says 4690-4692 under 4535 "Appendix G — Reproducible-writer profile
  (non-normative)". Found at 4690-4692. Match.

## Hunk 01 — §2.3 verifier bullet ([R-CNF-11])

Rule the repair asserts: for a verifier, a user-metadata record whose encoding byte is
in the experimental range (>= 0x80) is not a cannot-establish ground and does not
affect certification; encoding 0 and 3-0x7F are file-conformance violations (R1).
It restates [R-MTA-10] (narrowed) and R1; it is not itself the governing rule.

Check 1 (tense/quantifier): "a conforming file can carry" — generation-free predicate
on bytes. Actor: the verifier. Set: experimental-range encodings (>= 0x80, §18.2 /
§10.2 table). The governing rule [R-MTA-10] ranges over "an unassigned encoding" —
a superset. The repair's narrower claim is consistent with it; the superset's own
over-breadth is F-01 below.
Check 2 (citations): §21.6 row "A user-metadata record declares an experimental-range
(>= 0x80) document encoding | Ignored...; the file is conforming ... a verifier
certifies, reporting the record it ignored" — supports "a conforming file can carry".
PASS. [R-MTA-10] (§18.2 line 2754-2771): "no content rule attaches ... the record is
not among [R-CNF-11]'s cannot-establish grounds, and certification is unaffected" —
PASS. §21.5 preamble + R1 (line 3854): "declares a document encoding of 0, or a
reserved-range value (3-0x7F)" — supports "encoding 0 and a reserved value are
violations". PASS.
Check 3 (label): the sentence sits in the bulleted list of §2.3, closed by
`[R-CNF-11]`; no Note/Example/Rationale label; §2.3 is not an appendix. Normative.
Test applied: label, not marker. PASS.
Check 4 (same-passage contradiction): read the whole verifier bullet and the reader
bullet. Reader bullet line 176-192 uses the same partition (experimental MU=1 record
conforming, reserved MU=1 a violation) — parallel, not contradictory. The listed
cannot-establish ground "declines to decode a user-metadata document ([R-MTA-09])":
[R-MTA-09] line 2688-2690 says the decline presupposes an assigned encoding, so it
does not collide with "experimental ... is not such a ground". No carve-out found.
PASS.
Check 5 (exhaustive words): "encoding 0 and a reserved value are violations" is a
closed partition of the u8 space: 0 | 1,2 assigned | 3-0x7F reserved | >=0x80
experimental = 256 values. Complete. PASS.
Check 6 (siblings): the structure is the encoding byte's value space; all four
partitions now have a stated verifier outcome (assigned: rules attach, [R-MTA-09]
decline possible; experimental: not a ground; 0/reserved: R1). Nothing left open.
Check 7 (analogy): none in the repaired text. n/a.
Check 8 (anaphors): "is not such a ground" -> "a capability or resource ground" two
sentences up; the insertion is inside the same sentence, before the anaphor, so
resolution unchanged. Following sentences: "reports that way" -> cannot establish;
unchanged. Inserted "one this specification does not assign" -> "an experimental-range
encoding", adjacent. PASS.

## Hunk 08 — §17.4 closing sentence (after [R-COD-11])

Rule asserted: an experimental-range metadata encoding is not a violation, attaches no
document rule, and does not affect certification — unlike an experimental codec or
filter value, which is a validity error at layer scope (L43, L45).
Check 1: predicate on bytes, no generation; actor verifier. Governing rule quantifier:
[R-MTA-10] "unassigned"; repair "experimental-range" (narrower, consistent). §21.6 row
uses "experimental-range" exactly. PASS.
Check 2: §21.6 — row quoted above, PASS. [R-MTA-10] — PASS. §18.2 — §18.2 is where
[R-MTA-10] lives and where the value set is given. PASS. [R-CNF-03] / [R-COD-03] /
[R-COD-09] in the surrounding untouched text not re-audited beyond confirming L43/L45
list "experimental >= 0x8000" as violation instances (lines 3786, 3788).
Check 3: sentence follows the `[R-COD-11]` tag with no identifier of its own; it is
prose in §17.4, no Note label, not an appendix — normative restatement. PASS.
Check 4: preceding sentence "that position arises only at a reserved or experimental
value ... it rejects the layer" — for codecs both ranges are violations; the repaired
sentence contrasts only the experimental range, which is the only range that differs.
No contradiction. PASS.
Check 5: "alone" — see F-02. "in a conforming file" — circular-sounding but means "a
file carrying one is not thereby nonconforming"; matches §21.6 row. 
Check 6: the sentence now says nothing about reserved/0 metadata encodings, where the
old (wrong) sentence did; R1 governs them and hunk 01 states it. Not a gap that
changes behaviour.
Check 7: no analogy ("alone differs" is a contrast, not a warrant). n/a.
Check 8: nothing follows the sentence in the subsection; "its extent" -> the record's
extent, pre-existing wording. PASS.

## Hunk 23 — Appendix G closing paragraph, gloss on item 8

Rule asserted (non-normative): item 8's version_minor floor binds a creator and a
compactor adopting the profile, except in §20.5's carried-feature case; item 8's
flags = 0 binds only a creator.
Check 1: three claims vs item 8 (lines 4649-4660):
 (a) "binding creator and compactor alike" vs "The version_minor floor binds a
     compactor too" — PASS.
 (b) "save §20.5's carried-feature case" vs "save where its output carries a feature
     it does not implement, when §20.5's floor governs instead ([R-WRT-06])" and §20.5
     line 3497-3507 "Where the output carries a feature a later minor defines and this
     compactor does not ... version_minor SHOULD be at least the input's ... Otherwise
     version_minor follows [R-CNT-26]'s floor" — PASS.
 (c) "its flags half a creator's rule alone" vs item 8 "The flags half is a creator's
     rule ... a compactor ... carries its input's unknown ignore-lane bits forward
     instead, setting no other ([R-CNT-08])" — PASS.
 The changed flags rule: §6.3 [R-CNT-08] line 883-885 "A compactor, though its output
 is a new file, carries the input's unknown ignore-lane bits into its output trailer
 rather than writing flags = 0, and sets no other (§20.5, [R-WRT-06])"; §20.5 line
 3494-3496 "The output trailer MUST copy the input's unknown ignore-lane flag bits
 forward and set no other, in place of the flags = 0 §6.3 requires". Under that rule
 a compactor's flags are fixed by its input, so the profile's flags = 0 can only be a
 creator's rule. The gloss SURVIVES the flags change.
Check 2: [R-CNT-26] (line 894-898) "A writer SHOULD emit the lowest version_minor..."
— "states as a SHOULD" PASS. §20.5 — PASS as above.
Check 3: Appendix G is headed "(non-normative)"; the gloss carries no force by design.
Not a defect: it is a profile summary, and the paragraph itself says the numbered
items are the list.
Check 4: item 2 "This is a creator's rule: a compactor adopting the profile takes
[R-WRT-06]'s fresh draw instead" and item 8 "as item 2's identifier is" — consistent
with the gloss. Item 8's closing "reproducible only modulo its trailer" — consistent.
PASS.
Check 5: "alone" in "a creator's rule alone" — an updater/appender also may not write
flags = 0 ([R-CNT-08]), but item 4 (one generation) puts appended files outside the
profile, so within the profile the only two actors are creator and compactor. Holds.
Check 6: trailer fields (§6.2 table): magic constant; version_major = 1; version_minor
item 8; flags item 8; dir_offset item 3; dir_length function of content and item 3;
committed_file_length = F; file_id item 2; reserved zero; CRC derived. Every field
pinned. Nothing left open by the profile that the gloss should name.
Check 7: no analogy in the gloss. n/a.
Check 8: "its floor" -> version_minor's; "its flags half" -> item 8's (the only reading
that parses). Rest of paragraph unchanged in resolution. PASS.

## Sweeps (verbatim, with counts)

grep -n "does not assign"            -> 3 hits (1808 sample types; 2620 [R-MTA-03]; 2689 [R-MTA-09])
grep -n "not assign"                 -> 10 hits
grep -n -i "unassigned"              -> 5 hits (1058, 1104, 1492, 2754, 3844, 3856, 4147 — 7 lines actually printed)
grep -n -i "experimental"            -> 46 hits
grep -n "R-MTA-10"                   -> 16 hits
grep -n "R-COD-11"                   -> 4 hits
grep -n "R-CNT-26"                   -> 5 hits
grep -n -F "certification is unaffected" -> 2 (line-oriented; wraps at §17.4)
grep -n -F "carried-feature"         -> 1
grep -n -F "creator's rule"          -> 3
grep -n -F "alone differs"           -> 1
grep -n -F "such a ground"           -> 0  (WRAPPED — see control below)
grep -n -F "is not such a"           -> 1 (line 225)
grep -n -F "binds a compactor"       -> 1
grep -n -F "flags = 0"               -> 4
grep -n -F "reserved value"          -> 5
grep -n -F "reserved-range value"    -> 1
grep -n -F "encoding 0"              -> 4
Whitespace-normalised (python, wraps joined, "> " stripped):
  0  encoding this specification does not assign   (old hunk-01 phrase: gone)
  0  an unassigned document encoding                (old hunk-08 phrase: gone)
  3  unassigned encoding                            (1492, 2754, 4147)
  3  experimental-range encoding
  1  experimental-range document encoding
  0  creator's rule, not a compactor                (old hunk-23 phrase: gone)
  1  binding creator and compactor alike            (control for the line above)
  3  certification is unaffected                    (vs 2 line-oriented: wrap proven)
  1  The metadata-encoding space alone differs
  1  not such a ground                              (vs 0 line-oriented: wrap proven)
  1  Under an unassigned encoding this specification defines no decoding (control)
Controls: every zero above is paired with a normalised search for a phrase present in
the same passage that returned nonzero; the line-oriented zero for "such a ground"
was overturned by the normalised search, which is the wrap effect the brief warns of.

## Derived numbers

- Metadata-encoding u8 partition: 1 (value 0) + 2 (assigned) + 125 (3-0x7F) + 128
  (0x80-0xFF) = 256. Compared with §18.2 "0 is invalid; 1 = none and 2 = zstd ...;
  3 through 0x7F are reserved; values >= 0x80 are the experimental range" and §10.2's
  row. Hunk 01's "encoding 0 and a reserved value" + "experimental-range" + assigned
  therefore covers every value.
- Trailer fields per §6.2: 10 rows; each mapped to a profile item or a constant
  (above). Compared with Appendix G items 2, 3, 8.
- Hunk line ranges: all three headers agree with the bodies (checked by sed).

## Rejected candidates

1. Hunk 23 "save §20.5's carried-feature case" reads as if item 8 does not bind a
   compactor there, whereas item 8 says §20.5's floor governs instead. Dropped: the
   paragraph itself says "Read the numbered items as the list", the appendix is
   non-normative, and §20.5's SHOULD binds the compactor regardless of the gloss.
2. Hunk 23 "a creator's rule alone" vs an updater's [R-CNT-08] duty. Dropped: item 4
   (one generation) excludes appended files from the profile, so no third actor.
3. Hunk 01 "a conforming file can carry" vs §10.3 "Writers MUST NOT emit files carrying
   an experimental value in released software". Dropped: [R-CNF-02] and the §21.6 row
   both say the prohibition binds conduct, not bytes; the file is conforming.
4. Hunk 08's "in a conforming file" as circular. Dropped: pre-existing and matches the
   §21.6 row's "the file is conforming".
5. §17.4's untouched "that position arises only at a reserved or experimental value"
   making [R-CNF-11]'s cannot-execute-codec ground unreachable for a conforming
   verifier. Out of my hunks and pre-existing; noted, not filed.

## Findings

F-01 (UNSWEPT_RESTATEMENT, hunks 01/08, not byte-level). Three sites still state the
rule over "an unassigned encoding" — the exact over-breadth hunks 01 and 08 narrowed:
 - §18.2 [R-MTA-10], line 2762-2766: "A verifier meeting such a record in an otherwise
   conforming file has no requirement it is unable to check — the record is not among
   [R-CNF-11]'s cannot-establish grounds, and certification is unaffected" where "such
   a record" is one "Under an unassigned encoding" (line 2754). For encoding 0 or
   3-0x7F certification is affected: R1 is a violation.
 - §9.7 line 1491-1495: "A user-metadata document under an unassigned encoding asks
   nothing of this walk: no rule attaches to its content ([R-MTA-10]), so there is no
   violation there to look for, and what the verifier reports instead is that rule's
   subject." For a reserved encoding there is a violation to report (R1).
 - §22.3 line 4146-4150: "the extent of a user-metadata record under an unassigned
   encoding is covered by its terminal CRC but constrained by no content rule
   ([R-MTA-10]) ... so a certificate covers those bytes uninspected" — no certificate
   issues for a reserved encoding.
Why not byte-level: a file carrying encoding 0 or 3-0x7F carries R1 under every
reading ([R-MTA-03]; §21.5 preamble "R1 registers both as violations: what [R-MTA-10]
withdraws is the document's content rules, never the encoding byte's own value set");
R1's detector is the reader and every verifier is a reader ([R-CNF-04]), so no
competent verifier certifies it. The set of emittable and accepted files does not
move. Repair: in [R-MTA-10] change "and certification is unaffected" to "and, at an
experimental-range encoding, certification is unaffected"; in §9.7 and §22.3 replace
"under an unassigned encoding" with "under an experimental-range encoding".

F-02 (OVERCLAIM, hunk 08, not byte-level, reading-dependent, pre-existing word carried
through the rewrite). "The metadata-encoding space alone differs: an experimental-range
document encoding in a conforming file is not a violation (§21.6)". Read against the
codec and filter spaces §17.4 is about, "alone" holds. Read across §10.2's eight
spaces, the record-type space also carries a conforming experimental value: §21.6 row
"A record type this specification has not assigned, from the experimental range
(>= 0x8000, §10.2), carries MU = 0 | Ignored" and Appendix H "an experimental-range
MU = 0 record being conforming". Narrowing the clause from "unassigned" to
"experimental-range" is what exposes the word: under the old (false) reading no other
space treated every unassigned value as a non-violation. Not byte-level: no
implementer takes record-type behaviour from §17.4. Repair: "The metadata-encoding
space differs from the codec and filter spaces:" or "Of the spaces a verifier executes
a decoder for, the metadata-encoding space alone differs:".

Distinct findings in this transcript: 2.
