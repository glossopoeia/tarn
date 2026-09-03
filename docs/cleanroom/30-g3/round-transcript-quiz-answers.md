# Cleanroom round 30 — quiz answerer transcript

## Access disclosure

Read: `/Users/robertkleffner/Documents/GitHub/tarn-first-draft/spec/tarn.md` only, in full
(lines 1–4743), via the Read tool in chunks; one initial `sed -n '1,700p'` whose output the
harness persisted to a tool-results file (I saw a 2 KB preview of spec text; I did not open
that file). Ran `grep -n` against the same one file only, with positive controls. Ran one
local script that reads no files:
`/private/tmp/claude-501/-Users-robertkleffner-Documents-GitHub-tarn-first-draft/r30-round/scratch/quiz-answerer/qa_crc.py`
(pure-Python CRC-32C, shuffle, and arithmetic). Nothing else read: no docs/, no ADRs, no
conformance/, no registry.json, no git, no web, no directory listings.

Unrequested context: the runtime placed in my context a project instruction pointer
("See AGENTS.md"), an auto-memory index listing four note titles about the TARN harness, an
MCP server-instructions block, and the user's email. I did not open AGENTS.md or any memory
file and did not act on any of it. The spec's own status paragraph references PLAN.md and
docs/decisions/; I did not follow those links.

CRC implementation self-checks (all reproduce the document's own values):
CRC32C("123456789") = 0xE3069283; CRC32C(empty) = 0; Appendix A trailer CRC = 0x402F157E
(stored `7E 15 2F 40`); §7.4 example 80-sentinel-byte segment CRC = 0x80A34955 and
crc_of_crc_array = 0xC4EE982E; §15.4 full all-sentinel segment = 0xEECB3BB2.

## Q01 — `35 fd 5c 1c`

Trailer bytes [0,60) exactly as Appendix A (§Appendix A hex dump, lines 4349–4352) except
[40,48) = `01 00 00 00 00 00 00 00`:
`8a4e5241540d0a1a 0100 0000 00000000 1000000000000000 0400000000000000 8000000000000000
0100000000000000 000000000000000000000000`.
§4.5 [R-ENC-09]: CRC-32C "stored as a little-endian u32". §6.2 table: trailer CRC at offset
60 "CRC-32C over trailer bytes [0, 60)". Computed CRC = 0x1C5CFD35 → stored `35 fd 5c 1c`.
Confidence high.

## Q02 — (a) `f6 91 33 43` (b) `92 a4 71 c1` (c) `3e d1 64 25`

Payload = 32 × `00 00 80 3F` (128 bytes). §15.1 entry: offset u64, length u64, crc u32
"CRC-32C of the stored tile's bytes (§8.1)". (a) CRC32C(payload) = 0x433391F6 → `f6 91 33 43`.
Entry 2 as stored: `e8 03 00 00 00 00 00 00 | 80 00 00 00 00 00 00 00 | f6 91 33 43`
(offset 1000, length 128; codec 1 requires length = decoded size P·Q = 32·4 = 128, [R-COD-04]).
Sentinel = `FF ×16 00 ×4` ([R-IDX-02]). Array = sentinel, sentinel, entry2, sentinel (80 bytes);
§15.4 [R-IDX-04]: segment CRC is "the CRC-32C over exactly those entries' bytes as stored".
(b) 0xC171A492 → `92 a4 71 c1`. §7.4: crc_of_crc_array "CRC-32C over the index's segment-CRC
array"; array is the 4 stored bytes `92 a4 71 c1`. (c) 0x2564D13E → `3e d1 64 25`.
Confidence high.

## Q03 — `01 04 07 0a 0d 10 02 05 08 0b 0e 11 03 06 09 0c 0f 12`; CRC `0b 37 56 43`

§17.3 [R-COD-10]: stride s = Q for an interleaved tile; "Viewing the image as n = L/s
consecutive groups of s bytes, the filtered image places byte i of group j at offset i · n + j".
s = 3, n = 6. First bytes of groups: 01 04 07 0a 0d 10; second: 02 05 08 0b 0e 11; third:
03 06 09 0c 0f 12. Inverse verified to restore the input. Codec 1 (§17.2 [R-COD-04]): stored
bytes are the filtered image verbatim. CRC32C(filtered) = 0x4356370B → `0b 37 56 43`.
Confidence high.

## Q04 — 2,621,472

[R-CNT-17]: extent_length = entry_count × 20 + ⌈entry_count / 2¹⁶⌉ × 4.
131,073 × 20 = 2,621,460; ⌈131,073 / 65,536⌉ = 3 (131,073 = 2·65,536 + 1); 3 × 4 = 12.
Total 2,621,472. Confidence high.

## Q05 — 116

§11.2: Gᵢ = ⌈Eᵢ/Tᵢ⌉ → G = (⌈10/4⌉, ⌈20/5⌉, ⌈30/6⌉) = (3, 4, 5); N = 60.
§11.4 [R-GEO-06]: s = Σᵢ tᵢ · ∏_{j>i} Gⱼ = 2·(4·5) + 3·5 + 1 = 40 + 15 + 1 = 56.
Disk ordinal planar = c · N + s with c = channel index; `mask` is index 1 → 60 + 56 = 116.
Confidence high.

## Q06 — 12 runs; block 1's last run is [190, 200)

§16.2 [R-SLB-02]: runs partition each channel block [c·N, (c+1)·N) independently; "Run r of a
block starts at ordinal block_start + r·S"; "the final run of a block can cover fewer than S".
Per block: ⌈100/30⌉ = 4 runs (30, 30, 30, 10). Total 3 × 4 = 12. Block 1 = [100, 200);
run r = 3 starts at 100 + 90 = 190, ends at block end 200 → [190, 200). Confidence high.

## Q07 — 59,420; partial

[R-CNT-21]: "because the verifier elected under [R-CNF-11] to stop at the first violation —
the verifier MUST report the total as partial. A partial total is F less the bytes claimed by
the claimants the walk did enumerate — an upper bound on the file's true slack". Enumerated
claimants: 16 + 64 + 500 + 40,000 = 40,580. 100,000 − 40,580 = 59,420. The discard clause
("where the rejection is one the walk itself established, L18's overlap or L40 through L42's
placement among them, the claimants it had already enumerated are discarded with the layer")
does not apply: the rejection is an L1 layer-record validation failure, not one the walk
established, and B's claimants were never enumerated. Layer A's claimants stand. Verifier must
also name the violation that stopped the walk. Confidence high.

## Q08 — reject-file (trailer CRC); [R-CNT-06]

§6.2 [R-CNT-06]: "A reader MUST validate, in order: the trailer magic; the trailer CRC; the
version gate (§6.3)". CRC fails before the version gate is reached → reject-file, F14.
Independently, [R-CNF-13]: the trailer CRC is a reaching condition; "MUST treat its failure
as reject-file on the ground of the requirement stating it rather than on capability grounds;
the distinct diagnostic [R-CNT-07] asks for is owed where every reaching condition is
satisfied". Both routes agree. Confidence high.

## Q09 — (a) yes; (b) cannot establish

(a) §21.6: "an experimental-range top-level record type carrying MU = 1 ... [R-CNT-15]
obliges the reader to reject, and [R-CNF-02] makes the file conforming all the same."
[R-CNT-15]: "a record type from the experimental range is conforming (§10.3's prohibition
binds the writer's conduct, not the bytes)". (b) §2.3 [R-CNF-11]: "cannot establish — the
last where some requirement is one it is unable to check on a capability or resource ground,
as when ... a record carries MUST_UNDERSTAND = 1 with a type it does not implement (§21.6)";
and "cannot establish is available only to a traversal that established no violation" — given.
Confidence high.

## Q10 — 164; 2

§9.6 [R-LIF-06]: "The nearest-to-end candidate that survives the whole-file re-verification
below is the last committed state"; "a candidate whose whole-file re-verification fails was not
a commit state, so the tool continues the probe past it, and MUST report the candidate it
settled on and how many candidates it rejected on that re-verification". Settled candidate at
o = 100 → committed_file_length = o + 64 = 164; rejected = 2 (500 and 300).
Oddity: none of 500, 300, 100 is 64-aligned, so under the document's actual probe none could be
a candidate, and 164 would fail [R-CNT-06]'s multiple-of-64 gate on re-verification. Answer is
on the question's own hypothetical terms. Confidence medium (arithmetic certain; premise
inconsistent with the spec).

## Q11 — (a) no; (b) R4; (c) ignore-record

§18.2 [R-MTA-09]: content-size field "MAY be present, and when present it MUST equal the byte
length of the decoded document. A mismatch is one of the frame constraints R4 registers, not a
failure to decode under R3". R4 instance: "the content-size field declared larger than the
decoded length, top-level extent". §21.5: "Every row here is a violation all the same: the
outcome bounds a reader's blast radius and never makes the file conforming" → not conforming.
Outcome ignore-record ([R-MTA-09]: "Any violation here is ignore-record"). Confidence high.

## Q12 — barred; channel `b`

§20.3 step 4: "For a planar layer, a commit MUST NOT change the channel declarations in a way
that alters the disk ordinal [R-GEO-06] assigns any tile the layer stores in the generation
this commit supersedes. A channel's tiles move exactly when its index does: reordering moves
those channels the reorder re-indexes ... Either is such a change wherever the layer stores a
tile for a channel that moved." `b` goes from index 1 (ordinals 5–9) to 0 (ordinals 0–4) and
all its tiles are stored → barred. `a` also moves but stores nothing, so it contributes no
witness. Confidence high.

## Q13 — no; text labeled Note, Example, or Rationale

[R-CNF-01]: "All text in this document is normative except: §1 (Introduction); any text
labeled *Note*, *Example*, or *Rationale*; and appendices identified as non-normative." The
blockquote begins "**Note.**" → labeled Note. It precedes §1's heading, so the §1 category does
not apply, and it is not an appendix. Confidence high.

## Q14 — no

§2.4 outcome table, reject-layer row: "The outcome is prospective: it bars further service from
the layer, and does not retroactively invalidate content already returned under §19.2's
validation timing ([R-RDR-02])." Echoed in §19.4 step 8. Confidence high.

## Q15 — no

§19.3 [R-RDR-03]: "A reader's first access to a layer — the first operation using any of the
layer's declarations other than its name, whose parse §19.1 step 4 places at the open — MUST be
preceded by full validation of the layer record". Confidence high.
