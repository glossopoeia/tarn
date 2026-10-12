# Quiz author B — working transcript

## Disclosure

A message labelled as the user's request ("Go") was relayed above my brief by the
harness. Per the brief's own instructions, it is the launcher's message to the
orchestrator, carried out before I was spawned, needs no reconciliation with my
brief, and does not widen my access rule; I disregarded it as a task for me.

My runtime also placed context ahead of my brief that I did not ask for: a
project-instruction file pointing at another file, and a list of the user's
own memory-note titles (topics about this same TARN fidelity project and its
harness, named but not read by me). None of that is part of the specification
and none of it is evidence about the specification; I disregarded its content
entirely and did not use it to form or settle any suspicion about the document
below. I am not repeating its contents here.

**What I read:** exactly one file, at exactly the path my brief named:
`/Users/robertkleffner/Documents/GitHub/tarn-first-draft/spec/tarn.md`. The
path matched my brief; I did not find it anywhere else and did not need to
say otherwise. I read it in full (4,755 lines) via five sequential reads, start
to end, including the front matter, Parts I–III (§§1–21), §22 Security, §23
Privacy, §24 Conformance Test Vectors, and Appendices A–H. I did not open any
other file: not AGENTS.md, PLAN.md, OPEN-QUESTIONS.md, README.md,
CONTRIBUTING.md, anything under docs/ or conformance/, spec/registry.json, nor
any other copy of this specification. I did not run `git log`/`git diff`, did
not web-search or web-fetch, and did not list the repository to see what else
exists.

**What I ran:** `mkdir -p` to create my own scratch directory and the shared
output directory (`out/`, creating it only — I did not list its contents, and
do not know what other agents have placed there); `ls -la` once on my own
scratch directory to confirm it was empty before I started (it was — no prior
attempt's files to report); `wc -l` on the one allowed file to see its length
before reading it in chunks. No other command was run, and no file outside my
own scratch directory and this output file was written.

**Method note on the hard wrap.** Rather than grep, I read the document
directly with an offset/limit reader that returns raw lines, so I was not
exposed to the line-break-mid-phrase failure mode the brief warns about; I did
not need to fall back to a short-fragment search or a zero-result sanity
check, since nothing I looked for returned a zero I had to interpret.

## The slate (15 questions, no answers recorded)

1. For a conforming TARN file whose trailer declares `dir_offset = 16` and
   `dir_length = 20`, what is the minimum value `committed_file_length` (F) can
   take, consistent with every trailer field constraint and the file-size
   floor? Answer as an integer (bytes).

2. A layer uses `index_encoding` 1 and has `entry_count = 70,000`. What is the
   exact byte length of its tile-index region (entry array plus segment-CRC
   array)? Answer as an integer (bytes).

3. A planar layer declares codec 4 (lz4). Its tile extents give P = 2,000,000
   sample positions per tile. It has two channels: channel `a`, type uint64,
   and channel `b`, type uint8. Is this layer's codec declaration conforming?
   State the exact decoded byte size of whichever channel's plane governs the
   lz4 size check, and say which channel that is.

4. A layer record declares per-tile alignment A = 4096 and slab run length
   S = 8 (both nonzero) in the same layer record. Name the exact outcome
   class this produces and the register row (an "Lxx" label) it violates.

5. A layer has dimension extents (7, 7) and tile extents (4, 4), one int16
   channel whose fill value is `0x2A2B`. For the tile at tile coordinates
   (1, 1): how many of its sample positions are padding positions, and what
   two bytes, in storage order, does each padding position's channel value
   encode? Give the byte count and the two hex bytes in the order stored.

6. A top-level user-metadata record (type 0x0002) is stored with flags
   MUST_UNDERSTAND = 1, PRESERVE_ON_EDIT = 0. Name the exact file-scope
   register row ("Fxx") that this stored-flag combination violates.

7. A planar layer is read for channels r, g, b at one spatial position in a
   single request. Channel r's tile fails its stored-bytes CRC; channel g's
   tile is a valid sentinel; channel b's tile decodes cleanly. Must the
   reader fail the whole request, or may it return g's and b's values while
   reporting r's failure separately? Name the outcome class that governs r's
   failure.

8. True or false: an appender that extends a planar layer's channel list by
   one channel at the end (the layer having stored tiles in the generation
   the commit supersedes) may satisfy its re-emission obligation by appending
   only the new channel's tile-index entries, leaving the existing entries'
   bytes and position untouched. Answer true or false.

9. A channel entry declares type uint32 and a fill field with length prefix
   3. Name the exact register row ("Lxx") this violates.

10. A layer's tile index has `entry_count = 131,072`, and every entry is the
    sentinel. How many segments does the index have, and what CRC-32C value
    (hex, upper-case) does the segment-CRC array hold for each of them?

11. A file's trailer has version_major = 1, version_minor = 5, no incompat-lane
    bits set, and ignore-lane bit 20 set. A reader implements only through
    version_minor 2 of major 1. Is the file accepted by this reader? Answer
    yes or no, and name any file-scope register row that would otherwise
    apply, or state that none does.

12. A rewriter's input has a layer whose tile index contains an entry that
    §15.3 classifies reject-tile on a structural ground (not a stored-bytes
    CRC failure). Name the rewriter's two possible courses of action with
    respect to that layer.

13. A remote reader's transport does not disclose a range response's complete
    length, so the reader must probe the file size separately. What is the
    minimum number of round-trip requests this reader needs to complete the
    open (trailer validation plus directory fetch)? Answer as an integer.

14. A layer record declares rank 2, dimension extents (1000, 2000), tile
    extents (300, 500), layout = interleaved, and `entry_count = 21`. Name
    the exact register row ("Lxx") this layer violates.

15. Partway through servicing a multi-tile request against one layer, step 3
    of the tile-read algorithm detects an index-chain failure (a
    `crc_of_crc_array` or segment-CRC mismatch). (a) Name the outcome class
    and scope this failure takes. (b) May the reader still service the
    request's remaining tile entries from that same layer afterward? Answer
    yes or no.

## Notable rejections

- A question asking only for the front signature block's constant bytes, or
  only for the lz4 decoded-size cap as a bare table value, was rejected as a
  lazy table-quote with no combination; the lz4 question (slate #3) was
  rebuilt around a two-channel planar layer so the answerer has to compute
  which channel's plane governs before comparing it to the cap.
- A question asking only "by how much must `committed_file_length` increase
  per commit" was rejected as too close to one directly stated sentence
  ("strictly greater... by at least 128"); folded instead into slate #1,
  which forces combining the directory-bounds inequality with the 64-byte
  alignment rule and the 128-byte file-size floor for a specific
  `dir_offset`/`dir_length` pair, so the "at least 128" number is not simply
  copied out.
- No question in this slate was abandoned for lack of a determinate answer;
  I found no ambiguity in this text worth reporting against the quiz-authoring
  charter.

No answers to any of the above are recorded in this transcript or anywhere
else I wrote to.
