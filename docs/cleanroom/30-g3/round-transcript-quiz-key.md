# Round 30 — quiz keyer transcript

## Disclosure

Read: `/Users/robertkleffner/Documents/GitHub/tarn-first-draft/spec/tarn.md`, in full
(lines 1–4743), via the Read tool in chunks, plus `wc -l` and several `grep -n`
calls against that one file (each grep paired with a positive control that hit).
Nothing else was read: no `docs/`, no ADRs, no `conformance/`, no `registry.json`,
no PLAN/OPEN-QUESTIONS/AGENTS/README, no git commands, no web.

Unrequested context: my runtime placed a project-instruction pointer (CLAUDE.md →
AGENTS.md) and an index of four auto-memory note titles in my context before I
began. I did not open any of those files and did not use their titles as evidence.
One of the memory titles mentions a phrase-search tool defect — the brief itself
already says this. I disregarded all of it.

One Bash `sed -n 1,700p` call's output was too large and was persisted by the
harness to a tool-results file under `~/.claude/projects/...`; I did not open that
file and instead re-read the spec with the Read tool.

Working files (mine alone):
`/private/tmp/claude-501/-Users-robertkleffner-Documents-GitHub-tarn-first-draft/r30-round/scratch/quiz-keyer/qk_crc.py`

CRC self-checks all reproduced the document's own vectors before any answer:
`"123456789"` → 0xE3069283 (§4.5); zero bytes → 0; Appendix A trailer [0,60) →
0x402F157E; §7.4's 80-byte all-sentinel array → 0x80A34955 and its
crc_of_crc_array → 0xC4EE982E; §15.4's full sentinel segment → 0xEECB3BB2.

## Q01 — trailer CRC with file_id = 1

Trailer bytes [0,60) from Appendix A, with bytes [40,48) replaced by
`01 00 00 00 00 00 00 00`. §6.2 table: "60 | 4 | u32 | trailer CRC | structural |
CRC-32C over trailer bytes [0, 60)". §4.5 `[R-ENC-09]`: CRC-32C stored
little-endian.

Computed: 0x1C5CFD35 → stored `35 fd 5c 1c`.

Answer: `35 fd 5c 1c`. Confidence high.

## Q02 — sst layer with tile 2 stored

Layer per §7.4 example: entry_count = 4, one segment (§15.4: segment 0 covers
entries [0, min(65536, 4))). Entry layout §15.1: offset u64 @0, length u64 @8,
crc u32 @16 — "CRC-32C of the stored tile's bytes". Sentinel §15.2:
`FF ×16 00 ×4`. Codec 1: stored bytes = filtered image = decoded image (filter 1).
Decoded size = P·Q = 32·4 = 128, matches `[R-COD-04]`.

(a) CRC-32C of 32 × `00 00 80 3F` = 0x433391F6 → stored `f6 91 33 43`.
(b) Entry array: sentinel, sentinel, `E8 03 00 00 00 00 00 00 | 80 00 00 00 00
00 00 00 | F6 91 33 43`, sentinel. CRC-32C over those 80 bytes = 0xC171A492 →
stored `92 a4 71 c1`.
(c) CRC-32C over the 4-byte array `92 A4 71 C1` = 0x2564D13E → stored
`3e d1 64 25`.

§15.4 `[R-IDX-04]`: "the s-th u32 of the segment CRC array is the CRC-32C over
exactly those entries' bytes as stored"; §7.4 table: crc_of_crc_array "CRC-32C over
the index's segment-CRC array".

Confidence high.

## Q03 — byte-shuffle at s = Q = 3

§17.3 `[R-COD-10]`: "Viewing the image as n = L/s consecutive groups of s bytes,
the filtered image places byte i of group j at offset i · n + j — all first bytes
in image order, then all second bytes, and so on." L = 18, s = 3, n = 6.

Groups: [01 02 03][04 05 06][07 08 09][0A 0B 0C][0D 0E 0F][10 11 12].
Filtered: `01 04 07 0a 0d 10 02 05 08 0b 0e 11 03 06 09 0c 0f 12`.
CRC-32C = 0x4356370B → stored `0b 37 56 43`.

Cross-check against the §17.3 example (s=4, n=3) shape: consistent.
Confidence high.

## Q04

`[R-CNT-17]`: extent_length = entry_count × 20 + ⌈entry_count / 2¹⁶⌉ × 4.
131,073 × 20 = 2,621,460; ⌈131,073 / 65,536⌉ = 3 (131,072 = 2·65,536, one more
entry starts a third segment); 3 × 4 = 12. Total 2,621,472.
Confidence high.

## Q05

§11.2: Gᵢ = ⌈Eᵢ/Tᵢ⌉ → G = (3, 4, 5), N = 60. §11.4 `[R-GEO-06]`:
s = Σ tᵢ · ∏_{j>i} Gⱼ = 2·(4·5) + 3·5 + 1 = 40 + 15 + 1 = 56. Planar disk ordinal =
c · N + s with c the channel index; `mask` is index 1 → 1·60 + 56 = 116.
Confidence high.

## Q06

§16.2 `[R-SLB-02]`: runs partition each channel block [c·N, (c+1)·N)
independently; run r starts at block_start + r·S; final run may be partial.
Per block: ⌈100/30⌉ = 4 runs (30, 30, 30, 10). Three blocks → 12 runs.
Block 1 = [100, 200); last run r = 3 starts at 100 + 90 = 190 → [190, 200).
Confidence high.

## Q07

`[R-CNT-21]`: where the verifier "elected under [R-CNF-11] to stop at the first
violation — the verifier MUST report the total as partial. A partial total is F
less the bytes claimed by the claimants the walk did enumerate". §9.7
`[R-LIF-08]`: "The front signature block at [0, 16) and the live trailer at
[F − 64, F) are claimed by the walk as well". Layer B's claimants were never
enumerated (and a rejected layer's are not enumerated anyway).

100,000 − 16 − 64 − 500 − 40,000 = 59,420, reported as partial (an upper bound,
naming layer B / L1 as what stopped the walk).
Confidence high.

## Q08

§6.2 `[R-CNT-06]`: "A reader MUST validate, in order: the trailer magic; the
trailer CRC; the version gate (§6.3)". The CRC fails before the version gate is
reached. `[R-CNF-13]` confirms the trailer CRC is a reaching condition: a reader
"MUST treat its failure as reject-file on the ground of the requirement stating it
rather than on capability grounds; the distinct diagnostic [R-CNT-07] asks for is
owed where every reaching condition is satisfied". Register row F14, governing
rule `[R-CNT-06]`.

Answer: reject-file (trailer CRC), `[R-CNT-06]`. Confidence high.

## Q09

(a) Yes. §21.6: "an experimental-range top-level record type carrying MU = 1 …
[R-CNT-15] obliges the reader to reject, and [R-CNF-02] makes the file conforming
all the same." §7.2 `[R-CNT-15]`: "a record type from the experimental range is
conforming". (b) cannot establish. `[R-CNF-11]`: *cannot establish* applies "when a
record carries MUST_UNDERSTAND = 1 with a type it does not implement (§21.6)", and
"is available only to a traversal that established no violation" — which is the
premise. Confidence high.

## Q10

§9.6 `[R-LIF-06]`: candidate = magic match with verifying CRC and
committed_file_length = o + 64; "The nearest-to-end candidate that survives the
whole-file re-verification below is the last committed state"; "a candidate whose
whole-file re-verification fails was not a commit state, so the tool continues the
probe past it, and MUST report the candidate it settled on and how many candidates
it rejected on that re-verification".

Surviving candidate at o = 100 → committed_file_length = 164; rejected = 2.

Oddity: the question's offsets 500, 300, 100 are not 64-aligned (500 mod 64 = 52,
300 mod 64 = 44, 100 mod 64 = 36), so under the document's probe no candidate can
sit there, and 164 is not a multiple of 64 as `[R-CNT-06]` requires. The premise
is impossible as stated; I answer the arithmetic the document fixes (o + 64) on the
hypothetical given. Confidence medium (arithmetic certain; premise inconsistent).

## Q11

§18.2 `[R-MTA-09]`: the content-size field "MAY be present, and when present it
MUST equal the byte length of the decoded document. A mismatch is one of the frame
constraints R4 registers, not a failure to decode under R3". §21.5 R4 instances
include "the content-size field declared larger than the decoded length, top-level
extent". §21.5 preamble: "Every row here is a violation all the same".
(a) No. (b) R4. (c) ignore-record. Confidence high.

## Q12

§20.3 step 4: "For a planar layer, a commit MUST NOT change the channel
declarations in a way that alters the disk ordinal [R-GEO-06] assigns any tile the
layer stores in the generation this commit supersedes. A channel's tiles move
exactly when its index does: reordering moves those channels the reorder
re-indexes … Either is such a change wherever the layer stores a tile for a channel
that moved." Swapping re-indexes both; `b` (stored, ordinals 5–9 → 0–4) moved.
The worked example "exchanging a and b moves all four" matches.
Answer: barred; channel `b`. Confidence high.

## Q13

`[R-CNF-01]`: "All text in this document is normative except: §1 (Introduction);
any text labeled Note, Example, or Rationale; and appendices identified as
non-normative." The blockquote begins "**Note.**" and sits before the §1 heading,
so it is not in §1 and is not an appendix; the applicable exemption is the
Note/Example/Rationale label. Answer: no; category "text labeled Note, Example, or
Rationale". Confidence high.

## Q14

No. §2.4 outcome table, reject-layer row: "The outcome is prospective: it bars
further service from the layer, and does not retroactively invalidate content
already returned under §19.2's validation timing ([R-RDR-02])." §19.4 step 8
restates: "the bar is prospective, so values the reader has already returned under
§19.2's timing stand (§2.4)". Confidence high.

## Q15

No. §19.3 `[R-RDR-03]`: "A reader's **first access** to a layer — the first
operation using any of the layer's declarations other than its name, whose parse
§19.1 step 4 places at the open — MUST be preceded by full validation". The name
parse is expressly carved out. Confidence high.

## Underdetermined count

None strictly underdetermined. Q10's premise is internally inconsistent with the
document (offsets not 64-aligned), noted above.
