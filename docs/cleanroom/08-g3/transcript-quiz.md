# Cleanroom round 8 — the quiz, adjudicated

Protocol: ADR-0034. Fifteen byte-level questions **authored** by one agent,
**answered** cold by a second, and **keyed** independently by a third, each
blind to the other two and each reading `spec/tarn.md` and nothing else.
A divergence indicts the key's reading as readily as the answer's.

Verbatim transcripts: [author](transcript-quiz-author.md) ·
[answers](transcript-quiz-answers.md) · [key](transcript-quiz-key.md).

## Result

**15 agree / 0 diverge / 0 underdetermined.**

Neither agent marked a single question underdetermined. The two questions
whose answer strings differ (Q01, Q02) differ only in the letter case of hex
digits — `016d…` against `016D…`, `feff` against `FEFF` — the same values,
and the author's answer form did not fix a case. They are scored as agreeing;
the adjudication below shows both strings so the reader can check that
judgement rather than take it.

| # | Verdict | Answer | Key |
|---|---|---|---|
| Q01 | agree (hex case) | `016d010001010262740b0002803f` | `016D010001010262740B0002803F` |
| Q02 | agree (hex case) | `(a) feff; (b) 2; (c) 60` | `(a) FEFF; (b) 2; (c) 60` |
| Q03 | agree | `114433662255` | `114433662255` |
| Q04 | agree | `(a) 10; (b) 559` | `(a) 10; (b) 559` |
| Q05 | agree | `580` | `580` |
| Q06 | agree | `(a) 2621448; (b) [1310720, 2621440); (c) [2621444, 2621448)` | `(a) 2621448; (b) [1310720, 2621440); (c) [2621444, 2621448)` |
| Q07 | agree | `(a) 1; (b) 9; (c) 18` | `(a) 1; (b) 9; (c) 18` |
| Q08 | agree | `(a) ignore-record; (b) nonconforming` | `(a) ignore-record; (b) nonconforming` |
| Q09 | agree | `(a) reject-layer; (b) yes; (c) cannot establish` | `(a) reject-layer; (b) yes; (c) cannot establish` |
| Q10 | agree | `(a) nonconforming; (b) no` | `(a) nonconforming; (b) no` |
| Q11 | agree | `(a) reject-layer; (b) no; (c) no` | `(a) reject-layer; (b) no; (c) no` |
| Q12 | agree | `(a) 4096; (b) 20; (c) 4480; (d) 8; (e) no` | `(a) 4096; (b) 20; (c) 4480; (d) 8; (e) no` |
| Q13 | agree | `(a) 5; (b) 00000300; (c) yes` | `(a) 5; (b) 00000300; (c) yes` |
| Q14 | agree | `(a) reject-tile; (b) T21` | `(a) reject-tile; (b) T21` |
| Q15 | agree | `File 1: reject-file, F6. File 2: reject-layer, L6.` | `File 1: reject-file, F6. File 2: reject-layer, L6.` |

## The slate

Each question was written to stand alone: the answerer and the keyer saw the
question text and the document, nothing else.

### Q01

A conforming TARN file of format major version 1 contains a layer record whose inline payload declares exactly two channels, in this declared order: - channel 0: name `m` (the single ASCII byte 0x6D), sample type bool, fill value true; - channel 1: name `bt` (the two ASCII bytes 0x62 0x74), sample type bfloat16, fill value 1.0. Give the complete byte sequence of these two channel entries as they appear, concatenated in declared order, inside the layer record's inline payload. Answer as a single continuous hex string with no separators and no `0x` prefix (for example `0a1b2c3d`).

*Answer form:* A hex string of 14 bytes (28 hex digits), no separators.

*Sections drawn on (withheld from both takers):* §7.4 (channel entry framing), §12.1 (element sizes, bfloat16 identification and its worked example), §12.2 (type identifiers), §13.1/§13.2 (fill field, bool fill domain), §4.1 (little-endian), §4.6 (name length prefix)

*Byte-level consequence of getting it wrong:* The fill field's length prefix, the u16 type identifier's byte order, and bfloat16's two-byte encoding are each a place a writer can emit a different number of bytes. A layer record whose channel entries are one byte off shifts every later field of the inline payload, so the two implementations disagree about the layer's index_encoding and entry_count as well — the file one writes is a file the other rejects.

### Q02

A conforming TARN file of format major version 1 contains a layer declaring: layout planar; linearization 1; codec 1; filter 1; rank 2; dimension extents (5, 5) in declared order; tile extents (4, 4) in declared order; and exactly one channel, named `m`, of sample type bool, whose recorded fill field is the single byte 0x01. Consider the tile at tile coordinates (1, 1). The one sample of the layer that this tile carries has the value false. Give three things: (a) that tile's complete decoded tile image, as a hex string with no separators and no `0x` prefix; (b) the value stored in the `length` field of that tile's tile-index entry, as a decimal integer; (c) the byte offset of that tile's index entry measured from the first byte of the tile-index region, as a decimal integer.

*Answer form:* (a) a hex string of 2 bytes; (b) a decimal integer; (c) a decimal integer.

*Sections drawn on (withheld from both takers):* §11.2 (grid counts), §11.3 (padding positions), §11.4 (spatial and disk tile ordinals, in-tile ordinal), §13.2 (bool fill), §14.3 (packed boolean planes), §14.5 (padding content), §15.1 (entry size and placement), §17.2 codec 1 (`[R-COD-04]` length equality)

*Byte-level consequence of getting it wrong:* Fifteen of this tile's sixteen positions are padding. A writer that zero-fills padding instead of fill-encoding it emits different bytes for both bytes of the image, and its stored tile fails a verifier's padding check while decoding to the same reference array — two writers producing different bytes for identical logical content, only one of them conforming.

### Q03

A conforming TARN file of format major version 1 contains a layer declaring: layout interleaved; linearization 1; codec 1 (none); filter 2 (byte-shuffle); rank 1; its single dimension has extent 2 and tile extent 2; and exactly two channels in this declared order: `a` of sample type uint8, then `b` of sample type uint16. The layer's single tile carries, at in-tile ordinal 0, a = 0x11 and b = 0x2233, and at in-tile ordinal 1, a = 0x44 and b = 0x5566. Give the exact stored bytes of that tile — the bytes at [offset, offset + length) named by its tile-index entry — as a single hex string with no separators and no `0x` prefix.

*Answer form:* A hex string of 6 bytes (12 hex digits), no separators.

*Sections drawn on (withheld from both takers):* §14.1 (interleaved value sequence, sample-major), §14.2 (byte layout, sample stride Q, decoded size), §17.1 (filter then codec; reader reverses), §17.2 codec 1, §17.3 (byte-shuffle stride and the i·n + j permutation), §4.1 (little-endian)

*Byte-level consequence of getting it wrong:* The shuffle stride for an interleaved tile is the sample stride Q, not a channel's element size. An implementation that shuffles at stride 1 (identity), at stride 2, or that transposes in the inverse direction emits different stored bytes for the same tile; each decodes to different sample values in the other implementation, and every one of them passes the entry CRC because the CRC is computed over whatever the writer wrote.

### Q04

A conforming TARN file of format major version 1 contains a layer declaring: layout interleaved; linearization 1; rank 3; dimension extents (10, 9, 7) in declared order; tile extents (4, 5, 3) in declared order; and exactly three channels in this declared order: `a` of sample type uint8, `b` of sample type float64, `c` of sample type uint16. For the layer coordinate (7, 6, 5), given in declared dimension order, give: (a) the disk tile ordinal of the tile that contains it, as a decimal integer; (b) the byte offset, measured from the first byte of that tile's decoded tile image, of channel `c`'s value at that coordinate, as a decimal integer.

*Answer form:* (a) a decimal integer; (b) a decimal integer.

*Sections drawn on (withheld from both takers):* §11.2 (ceiling division, grid counts, N and P), §11.4 (tile coordinates, in-tile position, in-tile sample ordinal, spatial tile ordinal, disk tile ordinal), §14.2 (interleaved offset formula, sample stride Q, in-sample offset F^c), §12.1 (element sizes)

*Byte-level consequence of getting it wrong:* Both ordinals are sums of products over ∏_{j>i} — reading the products in the other direction (column-major) gives a well-formed but different answer, so two readers fetch different index entries and extract different bytes from the same tile. Nothing detects it: the file is structurally perfect and every checksum verifies. Samples simply come back wrong.

### Q05

A TARN file of format major version 1 has committed_file_length F = 1024, and its live trailer occupies bytes [960, 1024). Its live directory region begins at dir_offset 832 with dir_length 96. That directory contains exactly one record: a layer record whose extent slot is (extent_offset = 16, extent_length = 84), addressing that layer's tile-index region. The layer declares layout interleaved, index_encoding 1, and entry_count 4, and its geometry yields exactly 4 addressed tiles. Its four tile-index entries, in disk-ordinal order, are: - entry 0: offset 100, length 120 — the bytes it addresses match its crc field; - entry 1: offset 0xFFFFFFFFFFFFFFFF, length 0xFFFFFFFFFFFFFFFF, crc 0; - entry 2: offset 256, length 64 — the bytes it addresses do NOT match its crc field; - entry 3: offset 8, length 40, crc nonzero. There are no other records and no other structures. A verifier performs this specification's coverage verification, does not elect to stop at the first violation it finds, and its walk runs to completion. What total number of slack bytes does that verifier report? Answer as a single decimal integer.

*Answer form:* A single decimal integer.

*Sections drawn on (withheld from both takers):* §5.2 (coverage classes, slack, the verifier's slack total), §9.7 (what the walk enumerates and claims), §15.3 (which entries contribute a stored extent; the *structural* rows versus a crc-only failure), §15.2 (sentinel), §7.4/§15.1 (index region sizing and its single claimant), §6.2 (trailer, directory bounds)

*Byte-level consequence of getting it wrong:* Four separate rules each move this number: whether the front block and the live trailer are claimants, whether the tile-index region is claimed once or twice, whether an entry rejected on a structural ground still claims the bytes it nominally names, and whether an entry whose only defect is a failed tile CRC keeps its extent. Two verifiers reporting different slack totals for the same file give an operator opposite answers about whether to compact, and the third rule additionally decides whether an overlap violation is recorded at all — an accept/reject divergence on the same bytes.

### Q06

A conforming TARN file of format major version 1 contains a layer whose layer record declares index_encoding 1 and entry_count 131072. Give: (a) the value the layer record's extent_length field must hold, as a decimal integer; (b) the byte range, measured from the first byte of the tile-index region, of the index segment that contains the entry for disk tile ordinal 100000, expressed as a half-open interval of decimal integers in the form `[start, end)`; (c) the byte range, measured from the first byte of the tile-index region, of the four-byte segment CRC that covers that segment, expressed as a half-open interval of decimal integers in the form `[start, end)`.

*Answer form:* (a) a decimal integer; (b) an interval `[start, end)`; (c) an interval `[start, end)`.

*Sections drawn on (withheld from both takers):* §7.4 (`[R-CNT-17]`'s extent_length formula), §15.1 (region layout: entry array then segment CRC array, entry k at 20·k), §15.4 (segment membership and the s-th u32)

*Byte-level consequence of getting it wrong:* A reader that places the segment CRC array before the entry array, or that computes the segment index or the ceiling term wrong, fetches and verifies the wrong bytes: it will either reject a conforming file because its computed CRC does not match, or verify a segment that does not contain the entry it is about to act on. The extent_length value is also a hard cross-check a reader applies at layer access, so getting it wrong turns conforming layers into reject-layer.

### Q07

A conforming TARN file of format major version 1 contains a layer declaring: layout planar; linearization 1; exactly 3 channels; a spatial-tile count N of 10; a slab run length S of 4; and a slab alignment A_slab of 512. Consider the addressed tile whose disk tile ordinal is 19. Give: (a) the 0-based index of the channel that tile carries, as a decimal integer; (b) the spatial tile ordinal of that tile, as a decimal integer; (c) the disk tile ordinal at which the slab run containing disk tile ordinal 19 begins, as a decimal integer.

*Answer form:* (a) a decimal integer; (b) a decimal integer; (c) a decimal integer.

*Sections drawn on (withheld from both takers):* §11.4 (disk tile ordinal c·N + s for a planar layer, channel-major grouping), §16.2 (runs partition each contiguous block of disk ordinals independently; per-channel blocks [c·N, (c+1)·N); run r starts at block_start + r·S)

*Byte-level consequence of getting it wrong:* A writer that partitions runs globally from ordinal 0 rather than per channel block places a different tile first in this run, and therefore applies the A_slab alignment obligation to a different tile and the packing obligation across a different set of tiles. The two writers emit stored tiles at different byte offsets, and each one's file fails the other's verifier on the slab invariants.

### Q08

A TARN file of format major version 1 is well-formed in every respect except one: its live directory's top-level record sequence contains one record whose type field holds the value 0x0005, with MUST_UNDERSTAND = 0 and PRESERVE_ON_EDIT = 1, a well-formed extent slot addressing bytes that overlap nothing, and an inline payload that lies entirely within the record sequence. No other unusual condition is present anywhere in the file. A conforming reader and a conforming verifier, neither of which implements record type 0x0005, each process the file. Give: (a) the name of the reader outcome class the conforming reader applies to that record, using this specification's own outcome-class vocabulary; (b) the verdict the conforming verifier reports for the file, using this specification's own three-verdict vocabulary.

*Answer form:* (a) one outcome-class name from the document's vocabulary; (b) one verdict name from the document's vocabulary.

*Sections drawn on (withheld from both takers):* §7.2 (unknown record types and the MU rule; reserved-range types), §10.2 (record type space partition), §10.3, §2.3 (verifier verdicts), §2.4 (outcome classes), §21.2 rows F38/F39

*Byte-level consequence of getting it wrong:* 0x0005 sits in the reserved range, which makes emitting it a violation, but a reader's treatment turns only on the MU bit. A reader that conflates 'this specification has not assigned it' with 'reject the file' refuses a file it must instead read past, and a verifier that mirrors the reader's outcome and certifies the file certifies a file it must report otherwise. The two answers must diverge, and an implementation that gives them the same answer is wrong in one direction or the other.

### Q09

A TARN file of format major version 1 contains a layer record whose sub-record sequence includes one sub-record whose type field holds the value 0x8001, with MUST_UNDERSTAND = 1 and PRESERVE_ON_EDIT = 1, a well-formed extent slot addressing bytes that overlap nothing, and an inline payload lying entirely within the layer record's inline payload. Everything else in the file satisfies this specification. Neither the reader nor the verifier described below implements record type 0x8001. Give: (a) the name of the reader outcome class a conforming reader applies, using this specification's own outcome-class vocabulary; (b) whether the file is a conforming TARN file — answer yes or no; (c) the verdict a conforming verifier reports for the file, using this specification's own three-verdict vocabulary.

*Answer form:* (a) one outcome-class name from the document's vocabulary; (b) yes or no; (c) one verdict name from the document's vocabulary.

*Sections drawn on (withheld from both takers):* §7.4 (`[R-CNT-18]`: unknown sub-record with MU = 1), §10.2/§10.3 (experimental range), §2.3 (conforming file predicate; verifier verdicts and their grounds), §21.6 (the two conforming files a reader nevertheless refuses)

*Byte-level consequence of getting it wrong:* The three answers pull apart deliberately: the reader refuses a scope, the bytes are conforming, and the verifier may neither certify nor condemn. An implementation that treats an unknown critical sub-record as a whole-file rejection removes from service a file this specification says must remain readable layer by layer; a verifier that instead condemns the file brands conforming bytes as defective, which sends an operator to delete intact data.

### Q10

A conforming verifier's own bound for decoding a user-metadata document is exactly the smallest value this specification permits that bound to be. It is given a TARN file of format major version 1 whose single top-level user-metadata record carries a document that decodes to 20 MiB; the verifier therefore declines to decode it. Separately, that same file's single layer record declares entry_count = 0 and crc_of_crc_array = 0x00000001. Nothing else in the file is unusual. Give: (a) the verdict the verifier reports for the file, using this specification's own three-verdict vocabulary; (b) whether the verifier's decline to decode the document is itself reported as a finding that the file is nonconforming — answer yes or no.

*Answer form:* (a) one verdict name from the document's vocabulary; (b) yes or no.

*Sections drawn on (withheld from both takers):* §18.2 (`[R-MTA-09]`: the decoding bound, the verifier's decline, and what it is not), §21.9 (the user-metadata minimum guarantee and `[R-ERR-04]`), §2.3 (verdict priority between an established violation and unchecked requirements), §7.4 (`[R-CNT-23]`: nonzero crc_of_crc_array with entry_count = 0)

*Byte-level consequence of getting it wrong:* A verifier that lets an unchecked requirement dominate an established violation reports the file as merely unexaminable when it has already proved it defective, and a downstream tool acts on that. The mirror error — reporting the size decline as nonconformance — condemns a conforming document on the strength of the verifier's own capability rather than the bytes.

### Q11

A conforming reader has opened a TARN file of format major version 1 and has performed its first access to a planar layer, which validated cleanly. It now serves a single region request that needs three of that layer's tile-index entries, which it processes in ascending disk-ordinal order. The first two entries verify, and the reader returns the sample values they carry to the caller. For the third entry, the segment CRC the reader computes over the fetched index segment containing that entry does not equal the stored segment CRC for that segment. Give: (a) the name of the outcome class this failure takes, using this specification's own outcome-class vocabulary; (b) whether the reader is obliged to withdraw or invalidate the sample values it has already returned from the first two entries — answer yes or no; (c) whether the reader may serve a later, separate request for a different tile of the same layer — answer yes or no.

*Answer form:* (a) one outcome-class name from the document's vocabulary; (b) yes or no; (c) yes or no.

*Sections drawn on (withheld from both takers):* §15.4 (`[R-IDX-04]`), §19.2 (validation timing; failure takes the violated rule's own scope though detected at tile use), §19.4 step 8 (a layer-scope failure bars the request's remaining entries and all further service, prospectively), §2.4 (reject-layer is prospective and does not retroactively invalidate)

*Byte-level consequence of getting it wrong:* The natural but wrong reading scopes an index-chain failure to the tile whose entry was being fetched, which lets the reader keep serving other tiles of a layer whose index it can no longer trust — returning data from a scope this specification rejects. The opposite error, retracting already-returned values, makes the served-versus-failed boundary nondeterministic between readers handed the same file.

### Q12

An existing conforming TARN file of format major version 1 has committed_file_length F = 4096, and its live trailer carries generation 7. Its live directory contains four layer records and nothing else. A conforming appender performs exactly one commit against it, whose only logical change is to replace the fill value recorded for one channel of layer A; the new fill value has the same byte length as the old one. The appender writes every structure it appends at the lowest offset the commit protocol permits. The new complete directory region, including its terminal CRC-32C, is 300 bytes long. Give: (a) the byte offset at which the new directory region begins, as a decimal integer; (b) the number of pad bytes the commit writes between the end of the new directory region and the first byte of the new trailer, as a decimal integer; (c) the value the new trailer's committed_file_length field holds, as a decimal integer; (d) the value the new trailer's generation field holds, as a decimal integer; (e) whether layer A's tile-index region is re-emitted by this commit — answer yes or no.

*Answer form:* (a) a decimal integer; (b) a decimal integer; (c) a decimal integer; (d) a decimal integer; (e) yes or no.

*Sections drawn on (withheld from both takers):* §9.2 (`[R-LIF-02]` steps 1, 2, 3, 5), §5.1 (anatomy; what a commit that touches no layer's stored-tile set re-emits), §6.2 (trailer at a 64-aligned offset, F a multiple of 64), §20.3 (`[R-WRT-04]`/`[R-WRT-05]`: when an index region moves and when a layer keeps its extent slot), §9.3 (generation increments by exactly 1)

*Byte-level consequence of getting it wrong:* Every one of these five values is a byte another tool reads back. An appender that re-emits layer A's whole tile-index region because 'the layer changed' appends bytes the specification says it must not move and leaves the previous region as slack; an appender that pads to the wrong boundary places the trailer at a non-64-aligned offset, which every conforming reader must reject at open.

### Q13

An existing TARN file's live trailer has version_major = 1, version_minor = 5, and a flags field in which bits 16 and 17 are set and every other bit is clear. The file is otherwise conforming. An appender that implements only the format described by the current text of this specification — under which no flag bit is defined and no feature beyond version_minor 0 exists — performs one commit against that file. Give: (a) the value this specification directs the appender to write into the new trailer's version_minor field, as a decimal integer; (b) the four bytes the appender writes at offset 12 within the new 64-byte trailer, in the order they appear in the file, as a hex string with no separators and no `0x` prefix; (c) whether the input file is a conforming TARN file — answer yes or no.

*Answer form:* (a) a decimal integer; (b) a hex string of 4 bytes (8 hex digits); (c) yes or no.

*Sections drawn on (withheld from both takers):* §6.2 (trailer layout: flags at offset 12, version_minor at offset 10), §6.3 (`[R-CNT-08]` ignore-lane bits and the flags = 0 obligation; `[R-CNT-26]` the appender's version_minor), §20.3 step 6, §2.3 (`[R-CNF-02]`: a writer obligation this specification declares not to be a file-conformance violation), §4.1 (little-endian)

*Byte-level consequence of getting it wrong:* Part (b) is four literal trailer bytes. An appender that reads 'a writer creating a file under this text MUST write flags = 0' as binding on it writes four zero bytes and silently strips feature bits a later minor version defined, producing a file that misdescribes itself to readers that do implement those bits. An appender that lowers version_minor does the same to tooling that reads the feature floor.

### Q14

A TARN file of format major version 1 has a layer declaring codec 3, and one of its stored tiles has a decoded size, derived from the layer's declarations, of 512 bytes. That tile's stored bytes are exactly one Zstandard compressed frame: it begins with the correct compressed-frame magic, has Single_Segment_Flag clear, carries a Window_Descriptor yielding a Window_Size of 1024 bytes, carries no Dictionary_ID, does not set the content-checksum flag, omits the Frame_Content_Size field, decodes to exactly 512 bytes, and is consumed exactly by the entry's stored length with no trailing bytes. The tile's stored bytes match its index entry's crc field. Give: (a) the name of the outcome class a conforming reader applies to this tile, using this specification's own outcome-class vocabulary; (b) the identifier of the row of this specification's error-handling register against which this condition is recorded, in the form the register uses (for example `F12`, `L34`, `T7`, or `R3`).

*Answer form:* (a) one outcome-class name from the document's vocabulary; (b) one register row identifier.

*Sections drawn on (withheld from both takers):* §17.2 (`[R-COD-06]`: the window-size constraint against the tile's decoded size, and the note on how Window_Size is derived), §14.2/§14.3 (decoded size from declarations), §21.4 (the tile-scope register rows)

*Byte-level consequence of getting it wrong:* The frame decodes correctly to exactly the right length, so a reader that only checks the decoded length accepts this tile while a reader that applies the declared-window check refuses it — the same bytes, opposite verdicts. It also decides what a writer may emit: a tile whose decoded size is under 1 KiB cannot be encoded as anything but a single-segment frame, and a writer that does not know this emits tiles conforming readers must refuse.

### Q15

Consider two separate TARN files, each of format major version 1. File 1: its live directory contains exactly two layer records. The name field of each is the single byte 0x00 — a length prefix of 0 followed by no name bytes — and each name field lies entirely within its record's inline_length. Everything else in the file satisfies this specification. File 2: its live directory contains exactly two layer records. The name field of the first is the single byte 0x00. The name field of the second is the two bytes 0x01 0x61 — a length prefix of 1 followed by the ASCII byte `a`. Everything else in the file satisfies this specification. For each file separately, give the name of the outcome class a conforming reader applies, using this specification's own outcome-class vocabulary, and the identifier of the error-handling register row the condition is recorded against, in the form the register uses (for example `F12` or `L34`). Answer as two labelled pairs, File 1 and File 2.

*Answer form:* Two pairs, each an outcome-class name plus a register row identifier.

*Sections drawn on (withheld from both takers):* §19.1 step 4 (the record walk: the layer-name namespace, and that uniqueness is decided first and over raw name bytes whether or not each name is well-formed), §4.6 (`[R-ENC-12]` name constraints, `[R-ENC-13]` byte comparison, `[R-ENC-15]` scope split), §19.2 (detection at open), §21.2 and §21.3 (the register rows)

*Byte-level consequence of getting it wrong:* The scope split is the whole point: a duplicate layer name condemns the file, while any other name defect condemns only its layer. A reader that validates each name before testing uniqueness keeps serving a layer of a file it must refuse entirely; a reader that treats the single empty name in File 2 as a file-scope defect refuses a file whose second layer it is obliged to serve. Two readers therefore disagree about whether the same bytes are readable at all.

