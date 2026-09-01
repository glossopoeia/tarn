# Periphery audit transcript

## Disclosure

Before I did anything, my context contained material I did not ask for:
a project instruction file (CLAUDE.md pointing at AGENTS.md), the user's
email, today's date, and an environment/git-status block naming the
repository, branch, and five recent commit subject lines describing this
very change. Per my brief, none of that is part of the specification or
evidence about it. I disregarded all of it and did not use any of it —
in particular I did not use the commit subjects to decide what to look
for; every claim below is derived from reading spec/tarn.md and my six
hunk files only. I am not repeating the commit-subject text here.

I read exactly: my six hunk files (hunk-25, hunk-26, hunk-28, hunk-29,
hunk-30, hunk-31, all in the case-final directory named in my charter),
and spec/tarn.md (current file), at the locations the hunks land plus
their cited sections (§9.1–§9.7, §6.2, §6.3, §20.5, §3.1, §22, §23,
Appendix B, Appendix D, Appendix G). I did not read full.diff, any hunk
file outside my charter, any docs/ file, PLAN.md, OPEN-QUESTIONS.md,
AGENTS.md, or git history, and I did not list the case-final directory.

## Hunks read (verbatim headers checked against body)

- hunk-25: §22.5, claimed lines 4074-4077.
- hunk-26: §23.2, claimed lines 4130-4137.
- hunk-28: Appendix A hex dump, claimed lines 4268-4270.
- hunk-29: Appendix A annotation table, claimed lines 4283-4288.
- hunk-30: Appendix D, claimed lines 4380-4382.
- hunk-31: Appendix G item 4, claimed lines 4509-4512.

For each I read the current file at the claimed range and counted the
`+` lines in the hunk against the line span claimed. All six matched
exactly — no header/body mismatch in any of my six hunks.

## §22.5 (hunk-25)

Rule the change adopts: a detached signature over a committed prefix
[0, F) is pinned to (file_id, F) rather than (file_id, generation) —
same mechanism, re-keyed off the surviving ordering quantity.

- Read §22.5 in full (lines 4065-4077): one paragraph, ends
  `[R-SEC-07]`, only definition site of that ID (`grep -n "R-SEC-07"` →
  1 hit, at 4077). Not inside any blockquote — normative text.
- §9.1 (lines 1224-1232), cited by name in this passage, defines F as
  "the live trailer's committed file length" and states bytes [0,F)
  are immutable (`[R-LIF-01]`) — supports "stays valid ... under every
  later append."
- §3.1's glossary entry for *generation* (lines 395-398, read for
  contradiction-check even though not in my hunk set): "No field
  numbers generations; successive generations of one file are ordered
  by the strictly increasing committed file length" — matches this
  hunk's move from generation to F exactly, word for word in effect.
- Checked for stale use of the removed field: the word "generation" is
  retained twice in the sentence, but both are the general noun
  ("one generation" / "that generation" = one committed state, §3.1's
  definition), not the removed field name. This dual use pre-dates the
  change (compare "-" and "+" lines: both keep these two occurrences)
  and is consistent with how "generation" is used as ordinary English
  throughout the document (`grep -c generation` → 53 hits, spanning
  glossary, §9, §20, Appendix D/G — none of the other 51 uses are the
  removed field name either).

No finding.

## §23.2 (hunk-26)

Rule the change adopts: a file discloses per-commit sizes and slack,
recoverable only by the §9.6 backward probe (never from a field); no
field counts commits; a compacted file's probe finds nothing since
compaction carries no earlier trailer forward.

- Read §23.2 in full (4119-4152) and §23.1 (4081-4117) for
  contradiction-check. §23.1 already says slack is "recoverable by any
  tool that scans backward for an earlier trailer (§9.6)" — same
  mechanism, same citation, no conflict.
- §9.3's fourth Note (lines 1343-1351): "F counts bytes, not commits
  ... it does not number them: how many commits a file has undergone
  is not recoverable from the live trailer, and no field records it."
  This is the normative rule the hunk restates; compared word for
  word: "no field records it" vs. hunk's "No field carries a count of
  the commits that produced a file" — same claim, same scope (all
  fields, not just the removed one).
- §9.6 (1397-1432): confirms the backward-probe mechanism, that it is
  a recovery-tool/verifier operation (not a default-path reader
  operation), and that a tool "MUST report the candidate it settled on
  and how many it rejected" — supports "recoverable ... by probing
  backward."
- §20.5 (3341-3410): "A compactor's output contains only the
  structures reachable from the input's live trailer ... so slack is
  never carried" and "nothing in the output's trailer records that it
  is a first committed state — no field counts commits." Supports the
  hunk's "absent altogether from a compacted file ... which retains no
  earlier trailer to find" — a freshly compacted file's probe finds
  zero prior trailers, matching "absent altogether."
- Checked whether "a compacted file" could be misread as "any file
  that was ever compacted, even after further appends" (which would
  make the claim false, since a probe would then find the
  post-compaction commits' trailers back to the compaction boundary).
  Read the sentence again in context: it names §20.5 specifically,
  which is the compactor's *output*, so the referent is the immediate
  compaction product, not an arbitrarily-far-future descendant.
  Considered this a candidate finding and rejected it: the citation
  and context both anchor the claim to the compactor's own output,
  and nothing in the sentence claims more.
- Citation check: `[R-PRV-03]` — `grep -n "R-PRV-03"` → 1 hit, only at
  the tag itself (4140), consistent sole-definition site.

No finding.

## Appendix A hex dump + annotation table (hunk-28, hunk-29)

Rule the change adopts: the trailer's byte layout after removing the
8-byte generation field and widening reserved to 12 bytes at offset
48, with a recomputed CRC — restated in the worked minimal-file
example.

### CRC-32C validation (§4.5 params, Appendix B vector)

Implemented CRC-32C (poly 0x82F63B78 reflected, init/final XOR
0xFFFFFFFF) and validated against both of Appendix B's check vectors
before touching the file's own bytes:
- CRC-32C("123456789") → computed `0xe3069283`, matches Appendix B's
  `0xE3069283`. Pass.
- CRC-32C(zero bytes) → computed `0x0`, matches Appendix B's
  `0x00000000`. Pass.

Then computed the trailer CRC over the claimed 60 bytes [64,124) of
the dump (magic + version_major + version_minor + flags + dir_offset
+ dir_length + committed_file_length + file_id + 12 reserved zero
bytes, taken directly from the hex dump text):

```
input (60 bytes, hex): 8A 4E 52 41 54 0D 0A 1A 01 00 00 00 00 00 00 00
10 00 00 00 00 00 00 00 04 00 00 00 00 00 00 00 80 00 00 00 00 00 00 00
EF CD AB 89 67 45 23 01 00 00 00 00 00 00 00 00 00 00 00 00
result: 0x402f157e -> little-endian bytes 7e 15 2f 40
```

Matches the hunk's claimed CRC `0x402F157E` / bytes `7E 15 2F 40`
exactly. Pass.

### Byte-by-byte check against the annotation table and §6.2

Read §6.2's trailer layout table (800-816): offsets 0/8/10/12/16/24/
32/40/48/60 for magic/version_major/version_minor/flags/dir_offset/
dir_length/committed_file_length/file_id/reserved/CRC, reserved size
12, sizes summing to 64. Mapped to absolute file offsets (trailer
starts at 64): 64/72/74/76/80/88/96/104/112/124 through 128.

Checked every byte of the dump rows 0x40-0x70 against this and against
the annotation table:
- [64,72) `8A 4E 52 41 54 0D 0A 1A` = trailer magic — matches §6.2's
  fixed magic value and §6.3's F−64 invariant.
- [72,74) `01 00`, [74,76) `00 00` = version_major=1, version_minor=0.
- [76,80) `00 00 00 00` = flags=0.
- [80,88) `10 00 00 00 00 00 00 00` = dir_offset=16 (LE) — matches
  annotation and the directory's actual location at [16,20).
- [88,96) `04 00 00 00 00 00 00 00` = dir_length=4 — matches directory
  content (zero-byte record sequence + 4-byte CRC = 4 bytes).
- [96,104) `80 00 00 00 00 00 00 00` = committed_file_length=128 —
  matches stated file size and the 128-byte total (16+4+44+64).
- [104,112) `EF CD AB 89 67 45 23 01` — decoded LE as
  0x0123456789ABCDEF, matches annotation text exactly.
- [112,124) 12 zero bytes = reserved — matches §6.2's 12-byte reserved
  field at relative offset 48 (64+48=112) and matches §21's register
  row F15 ("The 12 reserved bytes at trailer offset 48 ...", line
  3592 — found by `grep -n reserved | grep -i trailer`, 2 hits total:
  this row and the Appendix A row, consistent with each other).
- [124,128) `7E 15 2F 40` = CRC — verified by independent computation
  above.

Field order in the annotation table (magic, version_major,
version_minor, flags, dir_offset, dir_length, committed_file_length,
file_id, reserved, CRC) matches §6.2's table order exactly — the
reorder was applied consistently to both the hex dump and its prose
annotation, not just one of the two.

### Diff-body sanity check (old vs. new)

Compared hunk-28's `-` lines (old dump) against `+` lines: old had
generation(8B)+dir_offset(8B) in row 0x50, dir_length+committed_file_
length in row 0x60, file_id+4-byte-reserved+old-CRC in row 0x70. New
has dir_offset+dir_length in 0x50, committed_file_length+file_id in
0x60, 12-byte-reserved+new-CRC in 0x70 — exactly an 8-byte
back-shift of every field after flags, with reserved absorbing the
freed 8 bytes (4→12), matching the charter's description of the
change. Total file size unchanged (128 bytes, confirmed by
committed_file_length=128 and by the dump's fixed length: still 4
rows × 16 bytes = 64-byte trailer, still 0x40 trailer start).

### Sweep for stale leftovers

- `grep -n "D2 38 09 E0\|E00938D2\|0xE00938D2"` (old CRC value) → 0
  hits. No stale old-CRC reference survives anywhere in the document.
- `grep -n "7E 15 2F 40\|402F157E\|0x402F157E"` → 2 hits, both inside
  this same Appendix A passage (the dump line and the table row) —
  the new CRC is not referenced or duplicated incorrectly anywhere
  else.
- `grep -n "\[80, 88)\|\[88, 96)\|\[96, 104)\|\[104, 112)\|\[112, 120)\|\[120, 124)\|\[112, 124)\|\[124, 128)"`
  → 6 hits, all six inside this one table (hunk-29's rows) — no
  duplicate or conflicting offset table elsewhere in the document
  citing the old (pre-reorder) offsets.
- `grep -n "generation = \|generation counter\|generation field\|8-byte generation\|reserved, 4 bytes\|reserved.*4 bytes.*zero"` →
  0 hits. No leftover mention of the old 4-byte reserved field or an
  "generation = N" annotation anywhere.
- `grep -n "offset 80\|offset 88\|offset 96\|offset 104\|offset 112\|offset 120"` →
  0 hits.

No finding.

## Appendix D (hunk-30)

Rule the change adopts: the document's no-generation-attribution
design choice is now stated to include "no counter in the trailer
numbering the commits" as a third named consequence, alongside the two
that were already there.

- Read the whole rationale bullet (4374-4382) and its neighbors
  (4369-4402) for contradiction — none found; the other five bullets
  don't touch generation/commit-counting.
- Cross-checked against §9.3's Note (the counter never existed as a
  commit-numbering field even conceptually — F counts bytes) and
  against the old Appendix A row `generation = 1` visible in hunk-29's
  `-` lines, which is the concrete artifact this bullet is now
  disclaiming. The addition is accurate: the removed field was
  literally a per-file commit counter (value 1 for the one-commit
  minimal file), so "no counter in the trailer numbering the commits"
  correctly describes what was removed, phrased as a design property
  rather than as a change note (no "before/after" language, no
  reference to the removal itself — reads as a plain description of
  the shipped format, matching the brief's caution about a spec having
  no "before").

No finding.

## Appendix G item 4 (hunk-31)

Rule the change adopts: an implementation of the "one generation"
reproducibility item cannot be refuted by reading a trailer field
(none exists), only by the §9.6 backward-probe procedure actually
finding a superseded trailer.

- Read the whole numbered list (4441-4529) for contradiction with
  neighboring items — none; items 1,2,3,5,6,7 are independent
  (codec/file_id/emission-order/alignment/sentinel/fill), none
  reference commit counting.
- §9.6 (already read for hunk-26) supports "backward probe finding a
  superseded trailer" verbatim — same mechanism, correctly cited.
- Checked the phrase "the slack that committed-prefix immutability
  leaves in place" against §9.1 (`[R-LIF-01]`: committed bytes MUST
  NOT be modified) and against §5.2's definition of slack (line 695:
  "Every byte the live state does not claim is slack") — a superseded
  trailer is, by definition, not claimed by the live state, so it is
  slack, and §9.1 is exactly what keeps it byte-intact rather than
  overwritten. Terminology is used correctly and consistently with
  hunk-26's parallel phrase in §23.2 ("superseded trailers that
  committed-prefix immutability keeps in place").
- Checked this isn't self-contradicting item 4's own claim: item 4
  says a file *is* the output of a single commit (a property the
  writer asserts by construction, not something the format enforces),
  and the new sentences only describe how a claimant *would* be
  caught lying — they don't weaken or restate the "one generation"
  requirement itself into something the format checks automatically.
  Consistent with Appendix G's own framing ("adds no requirement to
  any actor ... conformance to the profile can be refuted cheaply but
  confirmed only by reproducing the file").

No finding.

## Check 7 (argument by analogy) across all six hunks

Searched the six hunks' changed text for "exactly as", "the same way",
"as X is", "for the same reason", "likewise", "on the same discipline"
— none of the six hunks contain any such construction. This check
returns no candidates to test, by direct inspection of the changed
text (not a grep miss — the six hunks are short enough to read in
full, ~35 lines of `+` text total).

## Rejected candidates (beyond the compaction-scope one above)

1. Considered whether hunk-25's retained double use of "generation" as
   plain English (not the removed field) might read as a stale
   reference to the removed field. Rejected: §3.1's glossary explicitly
   defines *generation* as "one committed state of a file," independent
   of any trailer field, and this usage is document-wide (53 hits of
   the word, only one of which — the historical value in hunk-29's `-`
   side — was ever the field name).
2. Considered whether "the size of each commit and the slack it left
   behind" (hunk-26) is itself a new, underivable claim now that the
   generation counter is gone. Rejected after tracing the derivation
   through §9.2 (commits append monotonically, trailer records F) and
   §9.6 (backward probe enumerates trailers): commit size = difference
   of consecutive recovered F values, which needs only
   committed_file_length, never the removed field — so the claim's
   truth doesn't depend on the field that was removed and the repair
   didn't need to (and didn't) change this part of the claim.
3. Considered whether Appendix A's dump could have a swapped byte pair
   somewhere (e.g. dir_offset/dir_length swapped) that would still
   "look right" at a glance. Rejected by computing the CRC over the
   exact claimed byte sequence and getting an exact match — a
   transposition of any two non-identical bytes in the 60-byte input
   would have changed the CRC, and it didn't.

## Confidence / what I could not check

I could not check the §21 register-row-label change (retiring a struck
row's label) described in my brief as riding along with this removal,
since none of my six hunks touch §21 and my charter forbids reading
outside them — I did not open §21's table beyond the single F15 row I
looked up by grep to confirm the reserved-bytes register row is
undisturbed. I also did not audit §6.2, §9.1-§9.3, §20.5, or §3.1
themselves as changes-under-review (they are outside my hunk set) —
I read them only as citation targets to check my six hunks against,
and note anything I read there only as supporting or contradicting
evidence for my own hunks, not as a certification that those sections
are themselves defect-free. A full sweep for every other place the
word "generation" or "reserved" appears (53 and several dozen hits
respectively) was run and inspected only for the specific stale-value
and stale-offset patterns listed under "Sweep for stale leftovers"
above, not read in full — a defect phrased in language my greps didn't
anticipate could exist outside those patterns.
