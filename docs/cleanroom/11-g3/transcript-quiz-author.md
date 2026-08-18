# Round 11 — quiz author transcript

## Access disclosure

Read exactly one file: `/Users/robertkleffner/Documents/GitHub/tarn/spec/tarn.md`
(all 3,953 lines, in five sequential reads). No other file in the repository
was opened, listed, or grepped. No git history, no ADRs, no conformance
corpus, no registry.json, no PLAN.md/AGENTS.md/README, no web access.

Local computation only, in two throwaway Python scripts I wrote in the
scratchpad (`calc.py`, `calc2.py`), reading no repository files:

- a bit-by-bit CRC-32C implementation (reflected Castagnoli 0x82F63B78,
  init/final 0xFFFFFFFF), validated against the document's own two check
  vectors (`"123456789"` → 0xE3069283, empty → 0x00000000) and against the
  all-sentinel-segment constant 0xEECB3BB2 of §15.4, and cross-checked by
  reproducing Appendix A's trailer CRC 0xE00938D2 from the appendix's own
  trailer bytes;
- grid/ordinal/extent arithmetic for the geometry questions;
- a small parser over §21.2–§21.5's tables that counts Instances cells by
  §21.1's rule (semicolon-separated; a cell reading `—` is one instance),
  which reproduces §21.8's published totals: 36+49+26+10 = 121 conditions,
  53+106+45+44 = 248 instances.

One `grep -n` against that same single file, to confirm which requirement
identifiers appear in the register's *Governing rule* column.

I recorded no answers anywhere; the values I computed were computed only to
confirm that each question has a determinate answer, and are not written
down here.

## How I chose the slate

Weighting went to the sections named as newest, but not as a walk: I picked
questions that force an implementer to *produce* something. Rough shape:

- Three questions demand literal bytes (a stored tile after filtering, a
  tile-index entry including its CRC, index-region offsets under Appendix G's
  emission order, the two CRC fields of an all-sentinel index). Each one is
  wrong-bytes-on-disk if the reader mis-reads a rule.
- Four are verdict questions over a specific malformed or oddly-shaped file:
  a slab-declared layer where one entry is structurally malformed versus one
  whose *bytes* merely fail their CRC (§15.3's new "structural rows are
  transparent" carve-out meeting §16.2's packing invariant); an unimplemented
  format major carried alongside a major-1-only field defect; a readable but
  unsorted user-metadata document carrying a standardized key outside its
  scope; an over-large metadata document against §21.9's minimum guarantee.
- Four are arithmetic: geometry → entry_count → extent_length → disk ordinal
  → entry byte offset; the coverage walk's slack total (which forces the
  §9.7 rules that the index region enters the walk once, that sentinels and
  structurally-malformed entries contribute nothing, and that such an entry
  does *not* make the walk partial); a commit's appended byte count and pad;
  and the instance/vector arithmetic of §21.1/§21.8/§24.
- Two turn on rules whose statement is deliberately spread: which
  requirements §21.7 keeps out of the register versus which own rows; and the
  MU/PE drop-or-retain matrix of §20.4, which only resolves by combining the
  table, its "independently changes the scope" qualifier, and §7.3's fixed
  flags for registered types.

### What I rejected, and why

- **"What class is field X?"** as a bare §4.7 lookup — a table cell read back.
  Folded the taxonomy into a question that also costs a reader/verifier
  verdict, so a taxonomy slip alone does not decide the item.
- **Counting §21.3's instances (106).** Determinate, and I verified it, but 49
  rows of semicolon counting is tedium that would make a transcription slip
  look like a divergence. Used §21.5 (10 rows) instead, where the same rule
  is exercised and a miscount is a real reading error, not a clerical one.
- **A verifier's verdict for a file that declares an unimplemented major
  *and* fails its trailer CRC.** I wanted it — the CRC's coverage is
  permanent across majors (`[R-CNT-24]`) and §6.2 validates it *before* the
  version gate, so it looks establishable — but §2.3's "a file declaring
  another major is neither conforming nor nonconforming under it" pulls the
  other way. No determinate answer; it became finding quiz-03 and the
  question was rewritten to the case where both readings agree.
- **Appendix G's emission order for a multi-layer file with record extents.**
  "then any record extents in ascending record order" leaves it arguable
  whether a layer record's own extent (its index region, already emitted) is
  meant, so I kept the Appendix G question to a single-layer file with no
  other extents, where the order is forced.
- **A question about slack content.** §5.2 puts no requirement on it at all;
  any question would have had "unconstrained" as its answer, which teaches
  nothing about bytes.
- **Appendix H checklist items.** Non-normative and, where I checked them
  against §2.3/§12.1/§17.2/§17.3/§18.2/§21.9, accurate. Enumerating an
  accurate summary is not a question worth one of fifteen slots.

## Slate (question stems only — no answers recorded)

1. Interleaved edge tile: stored bytes after byte-shuffle, plus the full
   20-byte index entry (§11.2, §11.3, §14.2, §14.5, §17.3, §15.1, §4.5).
2. Appendix G emission order: index-region and segment-CRC-array offsets, and
   entry 1's offset/length bytes (App G, §9.2, §14.2, §17.2, §15.1).
3. All-sentinel two-entry index: the segment CRC and crc_of_crc_array bytes
   (§15.2, §15.4, §7.4, §4.5).
4. Geometry chain: entry_count, extent_length, disk ordinal, entry offset,
   in-tile ordinal (§11.2, §11.4, §7.4, §15.1).
5. Coverage walk: slack total, and partial versus exact (§5.2, §9.7, §15.3).
6. One supersede commit: index bytes appended, pad bytes, new
   committed_file_length (§9.2, §20.3, §15.1, §6.2).
7. Slab run with a structurally malformed entry versus a CRC-failing entry:
   rows and outcomes (§15.3, §16.2, §21.3, §21.4).
8. Unimplemented format major plus a major-1-only field defect: reader
   outcome, verifier verdict, register rows (§6.2, §6.3, §2.3, §21.6).
9. Unsorted user-metadata document carrying a standardized key out of scope
   (§18.2, §18.4, §21.2, §21.6).
10. A 20 MiB metadata document against the 16 MiB minimum guarantee (§18.2,
    §21.9, §2.3).
11. MU/PE drop-or-retain across six updater situations (§20.4, §7.3, §20.5).
12. version_minor, an ignore-lane bit, an experimental type and a
    reserved-range type in one file; plus two taxonomy classes (§6.3, §7.2,
    §10.2, §21.6, §4.7).
13. Which of eight requirement identifiers own a register row (§21.2–§21.5,
    §21.7, §16.2).
14. §21.5's instance total, the vectors owed for two rows, and the intact
    sibling rule (§21.1, §21.8, §24).
15. A fill-value change on a layer with edge padding: tiles re-emitted, index
    region re-emitted, its byte length (§11.3, §14.5, §20.3, §15.1).

## Findings raised while authoring

See the structured result, ids quiz-01 … quiz-04:

- quiz-01 — §2.1's exhaustive list of non-normative text does not reach the
  front matter's self-labelled "(non-normative)" reading guide.
- quiz-02 — §20.5's version_minor clause: MUST or a restatement of
  `[R-CNT-26]`'s SHOULD? Two compactors emit different trailer bytes.
- quiz-03 — §2.3 versus §6.2's validation order for an unimplemented major
  whose trailer CRC fails: *nonconforming* or *cannot establish*?
- quiz-04 — §4.7's structural test (acceptance of a tile) captures `fill` via
  `[R-SER-05]`, contradicting the same paragraph's closing assertion that
  `fill` is the only semantic field.
