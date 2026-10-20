# Quiz author B — transcript (summary)

## Disclosure

I read exactly one file: `/Users/robertkleffner/Documents/GitHub/tarn-first-draft/spec/tarn.md`,
in full, offset/limit chunks of roughly 600-1200 lines at a time (the
tool's size cap forced chunking; nothing was skipped — the whole 4810
lines were covered, including all appendices through Appendix H). I
also ran `ls` and `wc -l` on that same file's directory/file to confirm
its size before reading, and `sed -n` on that same single file to pull
its tail in place of a Read call for the last chunk. I read and ran
nothing else: no ADRs, no `docs/`, no `PLAN.md`, `OPEN-QUESTIONS.md`,
`AGENTS.md`, `README.md`, `CONTRIBUTING.md`, no `conformance/`, no
`spec/registry.json`, no git history/log/diff, no web search or fetch,
and I did not list any directory to see what else exists. I did not
open any other copy of this specification. The path I was given
matched exactly where the file actually was.

Before this brief, my context already contained material I did not
ask for: a project instruction file pointing elsewhere, an index of
the user's own memory notes about an unrelated harness/process, a git
status block, an environment/email block, and a relayed one-word
"user request" ("Go") that the harness says launched this round. None
of that is part of the specification and none of it is evidence about
the specification; I disregarded all of it and am not repeating its
contents here beyond naming that it appeared. The relayed request
needed no reconciliation with this brief and widened nothing.

I did not record any of my own answers anywhere, in this file or in
scratch. Per-question working arithmetic lived only in my own
reasoning, never written to disk.

## The slate (15 questions, no answers)

1. **(Part I — §6.2 ordered trailer validation)** A file's trailer has
   a correct magic and a correct CRC-32C, declares `version_major = 5`
   (a major this reader does not implement), and — in the same
   trailer — has an incompat-lane flag bit set and a nonzero reserved
   byte. Validating strictly in the order the specification mandates:
   (a) what outcome class results; (b) what must the rejection
   diagnostic avoid implying, in the specification's own terms; and
   (c) are the flag-bit and reserved-byte conditions separately
   evaluated and reported for this file, or not reached at all? Answer
   as a short verdict for each of (a), (b), (c).

2. **(Part I — §6.4 remote-open containment test)** A file's total
   size is 2,000,000 bytes. Its trailer gives `dir_offset = 1,998,900`
   and `dir_length = 120`. A remote reader's first request
   speculatively fetches the suffix window `[1,999,000, 2,000,000)`
   (1000 bytes). State the directory region's exact byte range, and
   say whether this window satisfies the containment test that would
   make a second request unnecessary (yes/no), with the one-sentence
   arithmetic reason.

3. **(Part I — §10.2/§10.3/§21.6 record-type ranges)** A writer emits
   a top-level record with type value `0x8123`. (a) Classify this
   value as assigned, reserved, or experimental. (b) If a reader does
   not implement this type and the record's stored MUST_UNDERSTAND bit
   is 1, what must the reader do, and does the file count as
   nonconforming on account of this record? (c) Give the same two
   answers for MUST_UNDERSTAND = 0. (d) Would either emission — MU=1
   or MU=0 — itself register as a file-conformance violation in the
   way an unassigned *reserved*-range type value would?

4. **(Part I — §6.1 residency)** A local reader memory-maps the whole
   file, so every byte is resident at open. Bytes [0,8) of the file
   read as the correct magic, but one byte inside [8,16) is `0x01`
   instead of `0x00`. (a) Must this reader detect the defect, and what
   outcome follows? (b) Would a remote reader whose open path never
   fetches bytes [0,16) (anchored at the trailer instead) have the
   same obligation? Answer (a) and (b) each as a short verdict with
   the governing concept (residency) named.

5. **(Part II — §11.2/§7.4 grid and index arithmetic)** A layer
   declares rank 2 with dimensions, in declared order, `y` (extent
   300, tile extent 64) and `x` (extent 500, tile extent 128); channel
   count C = 5; layout = planar; `index_encoding` = 1. Compute, in
   order: the grid counts G_y and G_x; the spatial-tile count N; the
   addressed-tile count (`entry_count`); and the tile-index region's
   `extent_length` in bytes. Give all five as integers.

6. **(Part II — §11.4 disk-ordinal arithmetic)** Using the same layer
   as the previous question (G_y = 5, G_x = 4, N = 20, C = 5, planar,
   dimensions declared in order (y, x)), find the disk ordinal of the
   tile that carries channel index 3 at tile coordinates
   (t_y = 2, t_x = 1). Show the spatial ordinal s and the final disk
   ordinal as two integers.

7. **(Part II — §17.2/§11.1/§20.3 lz4 cap and the empty-layer escape)**
   A layer declares codec 4 (lz4), rank 1, one dimension with extent 0
   and tile extent 2,200,000,000, one channel of type uint8. (a) Is
   this declaration, as stated, conforming? Name the rule that
   decides it. (b) If a later commit grows that dimension's extent
   from 0 to 1 (and nothing else about the layer changes), is the
   resulting generation's declaration for this layer still
   conforming? Give a yes/no for (a) and (b), each with the one
   governing requirement.

8. **(Part II — §15.1/§15.4 segment arithmetic)** A layer is planar
   with channel count C = 4 and spatial-tile count N = 20,000 (so
   `entry_count` = 80,000). Using the channel-major disk-ordinal rule
   and a segment size of 2^16 entries, find: the disk ordinal of the
   tile-index entry addressing channel index 3 at spatial ordinal
   19,999; which segment index (0-based) contains that entry; and that
   segment's entry range (as a half-open interval of entry indices).

9. **(Part II — §14.3/§14.5 packed-bool pad bits)** A planar bool
   channel has P = 20 sample positions per tile and a declared fill
   value of true (`0x01`). Suppose the four real (non-padding) values
   at in-tile ordinals 16, 17, 18, 19 are, respectively, false, true,
   false, false. Give the exact value, as a single hex byte, of the
   tile's third decoded byte (byte index 2, zero-based), including its
   pad bits.

10. **(Part II — §17.3/§14.3 shuffle-stride carve-out)** For a planar
    bool channel (a packed boolean plane), what shuffle stride does
    the byte-shuffle filter use, and — independent of whether the
    layer's declared filter value is "none" or "byte-shuffle" — is the
    filtered image for such a plane ever different from its unfiltered
    decoded image? Answer with the stride value and a yes/no.

11. **(Part III — §19.1 open-time duplicate-name priority)** Two layer
    records in one directory have name fields whose raw bytes are both
    the 3-byte sequence `61 00 62` (which contains the C0 control byte
    `0x00`, itself independently invalid as a name). At open, does the
    reader treat these two layer records as a duplicate-name
    violation? If so, state the outcome class, and state whether the
    name field's own invalidity changes or defers that determination.

12. **(Part III — §20.3 fixed-vs-permitted declarations under a
    two-part commit)** A layer currently stores at least one tile,
    under codec = zstd (3), tile extents (128, 128). A single appender
    commit attempts, at once: (a) growing one dimension's extent from
    1000 to 1200, and (b) changing the layer's codec from zstd (3) to
    lz4 (4). Taking each change on its own merits as an appender
    operation (not a rewrite): is change (a) alone permitted? Is
    change (b) alone permitted? What must a writer that wants change
    (b) do instead?

13. **(Part III — §20.5 rewriter disposal of a structurally
    malformed index entry)** A rewriter is compacting a file and
    relocating one layer's stored tiles, which requires regenerating
    that layer's whole tile-index region. One index entry in that
    region is `offset = sentinel, length ≠ sentinel, crc = 0` — a
    malformed entry that §15.3 classifies reject-tile on a structural
    ground. Name the two, and only two, dispositions available to the
    rewriter for this situation, and say whether "carry this one entry
    forward unchanged while regenerating the rest of the region" is a
    third option.

14. **(Part III — §21.2-§21.5 vs §21.8 totals)** Summing the stated
    condition counts given at the head of each of §21.2 ("35
    conditions"), §21.3 ("49 conditions"), §21.4 ("26 conditions"),
    and §21.5 ("10 conditions"), what total do you get, and does it
    match the total the specification states for the whole register in
    §21.8? Give the sum and a yes/no.

15. **(Part III — §20.4/§7.3 registry-flags-govern rule)** An appender
    is re-emitting the directory and meets a top-level record of type
    `0x0002` (user metadata) whose *stored* flag bits are
    `MUST_UNDERSTAND = 1, PRESERVE_ON_EDIT = 0` — not the value the
    registry fixes for this type. For the purpose of deciding this
    record's persistence treatment in the commit (not its reader
    semantics), do the stored bits or the registry's fixed values
    govern? Name the applicable persistence-table row (by its MU/PE
    values) and what the appender must therefore do with the record's
    bytes.

## Notable rejections

- A direct lookup of the CRC-32C check vector, or of what bytes a
  checksum covers from the §8.1 table alone — rejected as a
  single-location table-quote with no combination required.
- A question asking which of §6.2's un-ordered "following" checks
  (flag gates, length equality, the four offset/length bounds,
  file_id, reserved bytes) is reported first when several fail at
  once — the text orders only the first three gates (magic, CRC,
  version) explicitly, and states the remainder as a set validated
  together ("MUST validate all of the following") with no stated
  priority among its members. I could not derive a single determinate
  answer to "which one is reported first" and dropped the question
  rather than force one; see the finding below.
- A question built only from §11.2's own worked example numbers
  (1024×2048 at 256×256 tiles) — rejected as restating the document's
  example rather than posing an independent case.
- A question turning on a single channel-type or codec value-set
  table row alone, with no second rule applied to a concrete case —
  rejected as a lazy table-quote in each case it was tried.

## Finding carried from a rejected question

While testing the discarded §6.2 question above, I confirmed the
underlying condition is a genuine property of the text and not a
misreading: the specification states a strict sequence for exactly
three trailer gates (magic, CRC, version) and then groups a distinct,
larger set of checks ("the flag gates; committed_file_length …;
dir_offset ≥ 16; dir_length ≥ 4; … file_id ≠ 0; reserved bytes all
zero") under "MUST validate all of the following," with no ordering
language among that group's members. Every member of that group
independently yields reject-file, so the outcome class is unaffected,
but which diagnostic a reader surfaces first when two or more of that
group's conditions fail on the same file is not fixed by the text.
This is reported as a finding, not used as a quiz question, since it
has no single determinate answer for the answerer to converge on.
