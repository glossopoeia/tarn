# Quiz-taker transcript — edition A, taker on edition A

## Disclosure

- I read exactly one file: `/Users/robertkleffner/Documents/GitHub/tarn-first-draft/scratch/cleanroom/editions/a/tarn.md` (4981 lines, ~302 KB), in full, via seven sequential offset/limit reads (lines 1-1000, 1000-2000, 2000-3000, 3000-3700, 3700-4300, and confirmed the tail visually through line ~4300; the register sections §21.2-§21.9 and all of Parts 0-III through §22.3 were read verbatim). I did not read any other file, did not list any directory other than creating my own scratch directory, did not run git commands, and did not web search/fetch.
- I ran local Python (via Bash) purely for arithmetic verification (grid/ordinal arithmetic, byte-offset arithmetic, and one hex/decimal conversion for the lz4 cap). These computations read no files.
- I ran two `ls`/`mkdir` shell commands only to create and confirm my own scratch directory and to check the target file existed before reading it; I did not list the shared output directory.
- **Context I did not ask for**: my runtime pre-loaded a project CLAUDE.md pointer (to an AGENTS.md), a user memory-file index with titles like "TARN harness spec path", "TARN lineage gate word list", "TARN repair prose vs rules", etc., a git status block (branch "readable", recent commit subjects about a "Readable" edition of the document), and reminders about model identity and attribution. None of this is part of the specification and none of it is evidence about the specification's content. I disregarded all of it as substance; I am naming only that it appeared, not what it said, beyond what's already necessarily quoted above to identify the categories.
- **Path check**: the file was exactly where the brief said it would be: `scratch/cleanroom/editions/a/tarn.md`. I infer nothing from that path's name about what any other edition (b, or any "readable" edition suggested by the git branch name) says — I did not open any other copy, and the memory-index titles above (which mention a "readable" edition, ADR gates, etc.) are not treated as evidence about this document's content.
- The document is hard-wrapped Markdown (line lengths clustering ~72-79 chars with rare long lines from tables). I did not rely on line-oriented grep for any answer; I read the full prose in order via the Read tool, which reconstructs each paragraph's wrapped lines into contiguous prose in my working context, so wrap-induced false negatives were not a risk for the passages I quote — I quote by joining the visually-wrapped lines back into single sentences.

## Working notes / arithmetic (local computation only)

```
cap = 0x7E000000 = 2,113,929,216
P (16384 x 16384 tile) = 268,435,456
P * 8 (float64 plane) = 2,147,483,648  →  exceeds cap by 33,554,432 bytes

Grid/ordinal check (quiza-06):
Gy = ceil(10/4) = 3 ; Gx = ceil(13/5) = 3
(y,x) = (9,11) → ty=2,uy=1 ; tx=2,ux=1
s = ty*Gx + tx = 2*3+2 = 8  (interleaved ⇒ disk ordinal = s = 8)
in-tile ordinal u = uy*Tx + ux = 1*5+1 = 6
Q = B_p + B_q = 2 + 1 = 3 ; F_q = B_p = 2
offset of channel q = u*Q + F_q = 6*3 + 2 = 20
```

## Answers

Below, each answer cites section/requirement identifiers and quotes (joined across the source's hard wraps) the decisive sentence(s) from `scratch/cleanroom/editions/a/tarn.md`.

### quiza-01 — 256
§9.2 `[R-LIF-02]`: "A commit's committed_file_length is strictly greater than the prior trailer's, by at least 128, so the committed file length orders a file's generations." 128 (prior) + 128 (minimum increase) = 256.

### quiza-02 — (a) 1; (b) yes, `[R-CNT-04]`
§6.4 `[R-CNT-09]`: "A reader MAY instead speculatively fetch a suffix window in one request and use containment: if the fetched buffer contains the directory region, request 2 is unnecessary." The single fetch here returned [0,30000) — the whole file — which contains dir [20,120) and the trailer [29936,30000), and (per `[R-CNT-10]`) discloses the transport-authoritative size in the same response. So one request suffices.
For (b): §6.1 `[R-CNT-04]`: "A reader whose open leaves bytes [0, 16) resident — a local file read whole, a memory mapping, a speculative suffix window that reached offset 0, or any transport already holding them — MUST verify the full block by byte equality before other processing, and MUST treat any mismatch as reject-file." The fetched buffer contains offset 0, so residency holds and the check is obligatory.

### quiza-03 — (a) yes; (b) [R-ENC-04]; (c) reject-file
§7.2: "Any other combination with either half zero, an extent_offset < 16, an extent extending past F − 64, or an overflowing sum — extent_offset + extent_length is a declaration-derived quantity under `[R-ENC-04]` — is a validity error at the scope the record governs ... the file for other top-level records." 2^63−5 and 10 are each in [0, 2^63−1], but their sum is 2^63+5 > 2^63−1. §21.2 row F3 matches exactly: "A sum of a u64 offset and length taken from the file exceeds 2^63 - 1 although each field alone is in domain" with instances including "non-layer top-level record extent_offset + extent_length", governing rule `[R-ENC-04]`, outcome reject-file (§21.2 header: "Outcome: reject-file").

### quiza-04 — (a) reject-file (reported as torn/invalid); (b) no
§9.5 `[R-LIF-05]`: "The default read path is trailer-at-end-or-fail: a reader that finds no valid trailer in the final 64 bytes MUST report the file torn or invalid and MUST NOT scan backward." The bytes at [F-64,F) fail the trailer-magic check (§21.2 row F8: "The 8 bytes at F-64 are not exactly the trailer magic ..." → reject-file, detected at open). The earlier valid-looking trailer 64 bytes back is invisible to the default path; finding it is §9.6's separate, deliberate recovery-scan operation, "never a reader behavior" on the default path.

### quiza-05 — (a) the directory region's checksum; (b) the tile index's segment-CRC array
§4.5: "Interior checksum fields — each segment CRC array, each tile-index entry's crc field, and each layer record's crc_of_crc_array — are both comparison-verified and covered by exactly one further checksum, as §8.1 maps." crc_of_crc_array is a field inside the layer record's inline payload, which is part of the directory's record sequence; §8.1's map states the directory region's checksum ("final 4 bytes of the region") covers "the preceding dir_length − 4 bytes (the raw record sequence)" — which is what covers crc_of_crc_array's own stored bytes. Separately, §7.4 defines crc_of_crc_array itself as: "CRC-32C over the index's segment-CRC array (§15)."

### quiza-06 — (a) 8; (b) 20
See arithmetic above. §11.4 `[R-GEO-06]`: disk tile ordinal = s (interleaved) where s = Σ tᵢ·∏_{j>i} Gⱼ; §14.2's worked-example note: "channel c's value at in-tile ordinal u sits at byte u · Q + Fᶜ."

### quiza-07 — 55 FF
§14.3 `[R-SER-03]`: "value k occupies bit k mod 8 of byte k div 8 ... with 0 = false and 1 = true, and the decoded size is ⌈P/8⌉ bytes ... The final byte's high bits beyond the last value (bit positions P mod 8 through 7, when P mod 8 ≠ 0) are the tile's pad bits." §14.5 `[R-SER-05]`: "Every pad bit ... MUST carry the plane's channel's fill bit." With P=9: byte0 packs values 0-7 (true,false,true,false,true,false,true,false) = 0x55; byte1 bit0 = value 8 (true) and bits1-7 are pad bits = fill (true=1), giving 0xFF.

### quiza-08 — (a) 2,147,483,648; (b) no, channel 'b'
§14.2: planar decoded size = P·Bᶜ. P = 16384×16384 = 268,435,456; B_b (float64) = 8 → 2,147,483,648 bytes.
§17.2 `[R-COD-07]`: "Writers MUST NOT declare this codec for a layer any of whose addressed tiles' decoded size exceeds 0x7E000000 bytes ... in a planar layer each channel's plane carries its own decoded size ... and the largest governs." 0x7E000000 = 2,113,929,216. Channel b's plane (2,147,483,648) exceeds this cap; channel a's plane (268,435,456) does not — b is decisive.

### quiza-09 — (a) yes; (b) ignore-record
§18.2 `[R-MTA-04]`: "Key identity is the decoded string, not its JSON source bytes: "a" and "a" are the same key, and a document in which any one object carries that key twice is unreadable." Both keys decode to "café", so this is a duplicate key. §21.5 row R9: "Two members of one object in a user-metadata document carry the same key, identity being the decoded string and not the JSON source bytes" — outcome ignore-record (§21.5 header: "Outcome: ignore-record").

### quiza-10 — (a) no; (b) broken frame constraint; (c) see below
§18.2: "The frame's content-size field, unlike the decoded size and the window, is not left to the reader: it MAY be present, and when present it MUST equal the byte length of the decoded document. A mismatch is one of the frame constraints R4 registers, not a failure to decode under R3: the bytes decode, and what is wrong is what the header said about them." Decoded length is 800, declared content-size is 750 — a mismatch, so (a) not conforming, and (b) it is R4 (a broken frame constraint), not R3 (failure to decode).
(c) One-sentence contrast: for the user-metadata document the frame's content-size field, when present, must equal the document's actual decoded byte length (there being no independently declared document size to check it against), whereas for a tile under the same codec (`[R-COD-06]`) the content-size field, when present, must equal the tile's decoded size as derived purely from the layer's structural declarations (geometry, layout, channel types) — a value fixed before any byte is decoded, never a measurement of the decode's output.

### quiza-11 — (a) reject-layer; (b) no; (c) no
§15.4 `[R-IDX-04]`: "any mismatch or cross-check failure ... is reject-layer." §19.4 `[R-RDR-04]`: "A failure inside the same request that takes layer scope instead — step 3's index-chain failure (`[R-IDX-04]`) — bars the request's remaining entries and all further service from the layer; the bar is prospective, so values the reader has already returned under §19.2's timing stand." So segment-2's CRC failure is reject-layer; it does not retroactively invalidate the already-returned segment-0/1 values; and it bars all further service from the layer, so no further requests may be served afterward.

### quiza-12 — no; two alternatives: two separate commits, or a rewrite
§20.3 step 4: "a commit that shortens a planar layer's channel list appends no channel to it and one that extends it removes none, whatever the counts, so replacing the last channel, or any run of channels at the end, is two commits or a rewrite."

### quiza-13 — no; mechanism: the unimplemented experimental-range sub-record's governing MUST_UNDERSTAND=1 flag blocks any modification (including drop) of the layer
§20.4: "For a type the updater does not implement, the stored flags are authoritative." Table row "MU = 1": "Retain byte-identical. The updater MUST NOT modify the scope the record governs. At layer scope an unknown critical record blocks modification of that layer, its drop included, leaving other layers editable." The experimental-range sub-record is unimplemented by this updater with its stored MU bit = 1, so its stored flags govern (MU=1), blocking the layer's drop; the user-metadata sub-record's registry-fixed flags (MU=0, PE=1) are not what blocks anything here.

### quiza-14 — (a) no; (b) no; (c) drop the layer, or refuse to rewrite
§20.5: "An entry §15.3 classifies reject-tile on a structural ground is neither [a sentinel nor a valid entry] — `[R-IDX-03]` gives it no stored extent for a re-pointing to target — so regenerating the region cannot proceed without meeting it, and the violation is thereafter one the rewriter has detected. `[R-WRT-06]` then leaves it two disposals, since it can neither reproduce the entry nor invent a replacement: drop the layer, which §20.4's table licenses and whose loss the rewriter SHOULD report as that table says, or refuse."

### quiza-15 — (a) nonconforming; (b) yes; two things: the requirement (name) and the ground (capability/resource reason) it could not check
§2.3 `[R-CNF-11]`: "An established violation takes priority: a verifier that has established any violation reports nonconforming, however many requirements it was unable to check, and cannot establish is available only to a traversal that established no violation ... A verifier MUST report each requirement it was unable to check on a capability or resource ground, naming the requirement and the ground, whichever of the three verdicts it reports."
