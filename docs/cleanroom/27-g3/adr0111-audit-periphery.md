# Periphery audit transcript — case-adr0111

## Unrequested context disclosure

Before I did anything, my context already contained: a project CLAUDE.md
pointer (to AGENTS.md), an index of the user's auto-memory files (mentioning
"TARN lineage stays private", "TARN working cadence", "spec edits need
propagation checks", "TARN register is the corpus build list", etc.), the
user's email, and today's date. None of this was requested by me, none of it
is part of the specification, and none of it is evidence about the change
under audit. I disregarded all of it and did not open, read, or act on any of
the named memory files, AGENTS.md, or CLAUDE.md. I am naming that it appeared,
per instructions, without repeating its contents further than the topic
labels already unavoidably visible above.

## What I read

1. All six hunk files in full:
   - hunk-23.diff (§22.5)
   - hunk-24.diff (§23.2)
   - hunk-26.diff (Appendix A, hex dump)
   - hunk-27.diff (Appendix A, annotation table)
   - hunk-28.diff (Appendix D)
   - hunk-29.diff (Appendix G)
2. spec/tarn.md, the following ranges (current file, via Read tool):
   - lines 380-399 (§3 definitions: "generation", "trailer")
   - lines 4020-4148 (§22.4 end, §22.5, §23.1, §23.2 through start of §23.3)
   - lines 1222-1352 (§9.1 Committed-prefix immutability, §9.2 Commit
     protocol, §9.3 Generations/file_id/caching)
   - lines 1391-1435 (§9.6 Recovery scan, start of §9.7)
   - lines 3334-3433 (§20.5 Compaction)
   - lines 4200-4300 (end of §21.9/24 lead-in, Appendix A full, start of
     Appendix B)
   - lines 800-889 (§6.2 Trailer layout, §6.3 start)
   - lines 4358-4417 (Appendix D full, Appendix E, start of Appendix F)
   - lines 4423-4540 (Appendix G items 1-9)
   - grep hits for "generation", "reserved", "R-SEC-07", "R-PRV-03",
     "R-PRV-04", "21.6" (context lines around F14-F26 register rows, lines
     3577-3596, to check the F15/F17 citations reached from §9.6's text)
   - wc -l on spec/tarn.md (4641 lines total)

I did not read full.diff, any hunk file outside my charter, docs/, PLAN.md,
OPEN-QUESTIONS.md, AGENTS.md, git history, or the web. I did not list the
case-adr0111 directory.

## Header verification

For each hunk I compared the "lands at lines N-M" claim and "nearest
preceding heading" claim against the current file:

- hunk-23: claimed lines 4067-4070, preceding heading line 4058 "22.5 What
  this format does not provide". Current file lines 4067-4070 are exactly
  the four inserted lines from the hunk body; line 4058 is exactly that
  heading. Match.
- hunk-24: claimed lines 4123-4130, preceding heading line 4112 "23.2 What a
  file discloses". Current file lines 4123-4130 are exactly the eight
  inserted lines from the hunk body; line 4112 is exactly that heading.
  Match.
- hunk-26: claimed lines 4261-4263, preceding heading line 4249 "Appendix A
  — An annotated minimal file (non-normative)". Current file lines
  4261-4263 are exactly the three changed hex-dump rows (0050/0060/0070);
  line 4249 is exactly that heading. Match.
- hunk-27: claimed lines 4276-4281, same preceding heading. Current file
  lines 4276-4281 are exactly the six changed table rows. Match.
- hunk-28: claimed lines 4373-4375, preceding heading line 4358 "Appendix D
  — Design rationale (non-normative)". Current file lines 4373-4375 are
  exactly the three inserted lines; line 4358 is exactly that heading.
  Match.
- hunk-29: claimed lines 4502-4505, preceding heading line 4423 "Appendix G
  — Reproducible-writer profile (non-normative)". Current file lines
  4502-4505 are exactly the four inserted lines; line 4423 is exactly that
  heading. Match.

No header/body mismatches found in any of the six hunks.

## CRC-32C verification (Appendix A, hunks 26 & 27)

Step 1 — validate my own CRC-32C implementation against §4.5/Appendix B's
check vectors before trusting it on anything else:

- Implemented CRC-32C (Castagnoli, poly 0x82F63B78 reflected form, init
  0xFFFFFFFF, final XOR 0xFFFFFFFF) in Python.
- CRC-32C("123456789") -> 0xe3069283. §4.5 states "83 92 06 E3" (i.e.
  0xE3069283 little-endian) and Appendix B restates
  CRC-32C("123456789") = 0xE3069283. Match.
- CRC-32C(b"") -> 0x0. §4.5 and Appendix B both state CRC-32C of zero bytes
  = 0x00000000. Match.

Step 2 — compute the file's own trailer CRC. Trailer bytes [0,60)
(absolute file offset [64,124)) assembled from the new annotation table:

```
8A 4E 52 41 54 0D 0A 1A   magic
01 00                     version_major=1
00 00                     version_minor=0
00 00 00 00               flags=0
10 00 00 00 00 00 00 00   dir_offset=16
04 00 00 00 00 00 00 00   dir_length=4
80 00 00 00 00 00 00 00   committed_file_length=128
EF CD AB 89 67 45 23 01   file_id
00×12                     reserved
```
= 60 bytes exactly (8+2+2+4+8+8+8+8+12=60).

Computed CRC-32C over these 60 bytes = 0x402f157e.

The document (hunk-27, table row [124,128)) claims "trailer CRC-32C =
0x402F157E" and the hex dump (hunk-26, row 0070) stores it little-endian as
`7E 15 2F 40`. Both match my independently computed value exactly. The CRC
is correct for the new layout.

## Byte-by-byte cross-check, hex dump vs. annotation table vs. §6.2

Read §6.2's trailer layout table (lines 805-816) and confirmed every
absolute offset in the new Appendix A table is trailer-relative-offset + 64:

| Trailer-relative (§6.2) | Absolute (Appendix A) | Field |
|---|---|---|
| 0,8 | 64,72 | magic |
| 8,2 | 72,74 | version_major |
| 10,2 | 74,76 | version_minor |
| 12,4 | 76,80 | flags |
| 16,8 | 80,88 | dir_offset |
| 24,8 | 88,96 | dir_length |
| 32,8 | 96,104 | committed_file_length |
| 40,8 | 104,112 | file_id |
| 48,12 | 112,124 | reserved |
| 60,4 | 124,128 | trailer CRC |

Every row of hunk-27's table lands at exactly these absolute offsets. The
new hex dump rows (hunk-26) place the corresponding byte values at exactly
these offsets (checked row-by-row against the table above; see arithmetic
in the CRC section). Total byte accounting for the whole 128-byte file
(front magic 8 + front reserved 8 + directory 4 + pad 44 + trailer's nine
fields 8+2+2+4+8+8+8+8+12+4=64) sums to 128 with no gap or overlap. The
table is exhaustive and internally consistent.

Also checked: F15's register-row description (line 3585, outside my hunks
but reached from context) says "The 12 reserved bytes at trailer offset 48"
— matches the new §6.2 and Appendix A reserved field exactly. F17 (line
3587) is "committed_file_length does not equal the transport-authoritative
file size" — matches its use in §9.6's citation ("the length cross-check")
which itself is cited from a passage adjacent to (but not part of) my
hunks. No contradiction found; not itself a finding since neither §21.2 nor
§9.6's body text was in my charter's hunks.

## §22.5 / hunk-23

Rule the change adopts, in my own words: a detached signature over a TARN
file's committed prefix [0, F) is pinned to two things it can name without
a generation counter — the file_id the trailer carries, and the F value of
the prefix that was signed — and it remains valid across every later append
because bytes below F are never modified, though the signature only attests
to that specific generation, not to whatever the file has grown into by the
time a reader opens it.

1. Restatement check: this passage restates §9.1's committed-prefix
   immutability ("Bytes in [0, F) ... are immutable: a writer MUST NOT
   modify them", `[R-LIF-01]`). The hunk's tense/scope ("stays valid over
   that prefix under every later append") matches the normative "MUST NOT
   modify" — the signature's persistence claim is licensed exactly by the
   MUST NOT, no broader and no narrower.
2. Citations: `[R-SEC-07]` is defined only at this one location (grepped);
   no dangling or mispointed citation.
3. Normative text: this is body prose in §22.5 (Security Considerations),
   not inside a labelled blockquote. Grepped "generation its trailer" and
   confirmed the only hit is this passage.
4. No contradiction elsewhere in §22.5 — read the full subsection (4058-
   4070); nothing else in it mentions generation attribution.
5. No exhaustive claim beyond what's licensed.
6. Left open: nothing new — the concept of "that F" identifying a
   generation is exactly what §9.3 already establishes ("F ... orders that
   file's generations and identifies each of them", not itself part of my
   hunks but confirms the derivation exists rather than being invented
   here).
7. No "exactly as" / "the same way" / analogy language in this hunk.

No finding.

## §23.2 / hunk-24

Rule the change adopts: a file's history (per-commit sizes and slack) stays
disclosed, recoverable by the same backward probe recovery tooling already
uses (§9.6) over the superseded trailers committed-prefix immutability
never lets a later commit erase (§9.1) — but the *count* of commits is no
longer disclosed by any field; it is derivable only by running that probe
to completion, is unavailable from the live trailer alone, and a compacted
file has no superseded trailers left to probe for at all.

1. Restatement check against §9.3's Note (lines 1337-1345): "F counts
   bytes, not commits... how many commits a file has undergone is not
   recoverable from the live trailer, and no field records it." Word for
   word this matches the hunk's "no field carries a count... is
   unavailable to anyone holding just the live trailer." Same quantifier
   ("no field" / "not recoverable ... no field records it"), same scope
   (live trailer). No divergence.
2. Citations: §9.1 and §9.6 both checked and both say what the text
   claims — §9.1 defines committed-prefix immutability and F; §9.6 states
   the backward probe and explicitly extends it to full enumeration ("A
   recovery tool enumerating a file's commit states continues the same
   probe to offset 0"), which is exactly what licenses the "size of each
   commit... recoverable by probing backward" claim. §20.5 checked and
   confirms "nothing in the output's trailer records that it is a first
   committed state — no field counts commits" and that the compactor
   follows the creation path with no prior trailer — matches "retains no
   earlier trailer to find."
3. Normative text: body prose, not in a blockquote; the actual `[R-PRV-03]`
   keyword sentence ("Writers handling sensitive material SHOULD...")
   follows the descriptive material and is unaffected by this hunk.
4. No contradiction: read the whole of §23.2 through its end (through
   `[R-PRV-04]`, line 4145) — the file_id paragraph that follows is
   untouched and consistent (compaction "mints a new [file_id]... not an
   unlinkability measure", no clash with the commit-count claim).
5. No exhaustive claim beyond what §9.6 supports — "the number follows only
   from that probe" is exactly what §9.6 supports (probe to offset 0 to
   enumerate).
6. Left open: nothing new introduced; the paragraph is explicit that no
   field carries a count, so there's no sibling quantity silently left
   unpinned.
7. No analogy language in this hunk.

No finding.

## Appendix A / hunks 26 & 27

Rule the change adopts: the minimal 128-byte file's trailer no longer
carries an 8-byte generation counter at offset 80; dir_offset, dir_length,
committed_file_length, and file_id each shift back 8 bytes to close the
gap; the vacated 8 bytes join the trailer's existing 4 reserved bytes to
form one contiguous 12-byte reserved run at offset 112; and the trailer CRC
is recomputed over the new 60-byte prefix.

Checked (see CRC section and byte-by-byte section above): every offset in
both the hex dump and the annotation table is internally consistent, is
consistent with §6.2's layout table, and the CRC value is independently
verified correct — not merely internally self-consistent but checked
against a CRC-32C implementation itself validated against §4.5/Appendix B's
named check vectors first, as the brief required.

1. Restatement: the table restates §6.2's field list and §4.5's checksum
   definition; both checked and matching.
2. Citations: none inside the table body beyond the field names §6.2
   already defines with those exact names/offsets/widths — checked, match.
3. Normative text: Appendix A is explicitly non-normative (heading says
   so) and the surrounding prose ("A remote reader opens this file in
   §6.4's two requests...") is also unchanged by these two hunks — not
   itself a finding since Appendix A's non-normativity is a labelled
   heading, not a mislabelled blockquote, and none of the seven checks'
   "labelled blockquote" trap applies to a whole non-normative appendix by
   design.
4. No contradiction elsewhere in the surrounding paragraph (lines
   4283-4294, read in full) — describes §6.4's two-request open and
   §19.1's four-step open against this exact file; nothing there depends
   on the removed generation field or a stale offset.
5. No exhaustive claim beyond what's licensed — the table is exhaustive
   over the file's 128 bytes and I verified it actually is exhaustive (see
   byte accounting above): a genuine closed count that is actually closed.
6. Left open: nothing — every byte of the smallest conforming file is
   annotated.
7. No analogy language in either hunk.

No finding.

## Appendix D / hunk-28

Rule the change adopts: the append-only/complete-directory-per-generation
design choice is why there is no generation-attribution machinery, no
trailer chain, *and* (new) no counter in the trailer numbering the commits
— folding the removed field into the existing rationale for why the format
tracks no cross-generation bookkeeping at all.

1. Restatement: consistent with §9.3's Note (no field records commit
   count) and with hunk-24/29's descriptions — same claim, same scope,
   restated as design rationale rather than normative requirement (as
   befits a non-normative appendix).
2. Citations: none added by this hunk.
3. Normative text: Appendix D is explicitly non-normative; this rationale
   sentence carries no requirement keyword and isn't purporting to.
4. No contradiction: read the full "Append-only, with a complete directory
   per generation" paragraph (4367-4375) and the rest of Appendix D
   (4358-4395) — nothing else references generation numbering or a
   trailer chain in a way this conflicts with.
5. No exhaustive claim issue.
6. Left open: nothing — this is a three-item list ("no ... machinery, no
   ... chain, and no counter") and all three items are independently true
   per §9.3/§20.5.
7. No analogy language in this hunk.

No finding.

## Appendix G / hunk-29

Rule the change adopts: within the reproducible-writer profile, "one
generation" (item 4) is refuted the same way it always could be verified —
not by reading a value out of the trailer (there isn't one now, and there
never really was a reliable one for this purpose either), but by running
§9.6's backward probe and finding a superseded trailer sitting in slack
that committed-prefix immutability never let the writer erase.

1. Restatement: matches §9.3's Note and §9.6's probe description precisely
   — "backward probe finding a superseded trailer in the slack" mirrors
   §9.6's "probe backward at 64-aligned offsets... for the trailer magic"
   and its "continues the same probe to offset 0" enumeration language.
2. Citations: §9.6 checked, matches.
3. Normative text: Appendix G is explicitly non-normative (profile items
   are opt-in, "It adds no requirement to any actor"); this is consistent
   with the item's own framing ("nothing refutes this item by reading a
   value") which is explicitly about a voluntary profile's confirmability,
   not a MUST.
4. No contradiction: read the full Appendix G list, items 1 through 9
   (4434-4540) — no other item references a generation counter or commit
   count; item 8's `flags`/`version_minor` discussion and item 9's JSON/
   zstd pinning are unrelated and unaffected.
5. No exhaustive claim: "nothing refutes this item by reading a value" is
   a true universal given no field exists to read — checked against the
   trailer's full field list (§6.2, Appendix A) and confirmed none of the
   nine fields records a commit count.
6. Left open: nothing new.
7. Analogy language: none in this hunk itself. (Items 8 and 9, untouched
   by this hunk, do use "as item 2's identifier is" / "as item 1 pins a
   tile codec" — outside my hunk's changed lines and unrelated to the
   generation-field removal, so not pursued further under my charter.)

No finding.

## Findings considered and rejected

- Considered whether "the size of each commit" (hunk-24) is actually
  recoverable for *every* commit via backward probe, or only some. Checked
  §9.6: since committed-prefix immutability never modifies earlier bytes
  and this is a single (uncompacted) file, every earlier trailer remains
  physically present, and §9.6 explicitly describes continuing the probe
  to offset 0 to enumerate all commit states. Not an overclaim — rejected.
- Considered whether the "absent altogether from a compacted file" claim
  (hunk-24) contradicts §20.5's "indistinguishable by their trailers
  alone" phrasing. Resolved: "trailers alone" in §20.5 means the live
  trailer only (no probing), which is a narrower claim than "no earlier
  trailer to find" (which is about what a full backward probe turns up on
  a freshly compacted file). The two are complementary, not contradictory
  — rejected.
- Considered whether hunk-23's "pinned to the file_id its trailer names and
  to that F" silently drops the ability to name a specific generation now
  that there's no counter. Checked §9.3: F alone (paired with file_id)
  already "identifies each" generation, since F strictly increases per
  commit and no two commits share one. Not a loss of precision — rejected.
- Considered whether the Appendix A table might have a subtle CRC error
  (e.g. an off-by-one in which 60 vs 64 bytes are covered, or an endianness
  slip). Computed independently from a validated CRC-32C implementation
  (checked first against §4.5/Appendix B's two named check vectors) and
  got exact agreement with the document's claimed value and stored bytes
  — rejected.
- Considered whether the reserved-run offset/width in the new table (12
  bytes at [112,124)) might disagree with §6.2 or with register row F15.
  Both checked and match exactly — rejected.

## Result

No findings survive across all six hunks. All six header-derivation checks
passed (no header/body mismatches). The Appendix A CRC and full byte
layout were independently verified correct. The §22.5/§23.2/Appendix D/
Appendix G prose changes are consistent with each other and with §9.1,
§9.2, §9.3, §9.6, §20.5, and §6.2 as read.
