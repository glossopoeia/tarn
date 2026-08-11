# Cleanroom round 6 — quiz adjudication

I read only `/Users/robertkleffner/Documents/GitHub/tarn/spec/tarn.md`, plus one `python3` one-liner that re-parsed that same file's §21.2–§21.5 tables (result: 125 rows, 244 instances — both agents' claim confirmed independently).

# ADJUDICATION — cleanroom round 6

## Per-question verdicts

| Q | Topic | Verdict |
|---|---|---|
| 1 | §5.2/§9.7 unclaimed live byte | **agree** — correct |
| 2 | interleaved bool 0x7F | **agree** — correct |
| 3 | remote open, Appendix A | **agree** — correct |
| 4 | em-dash Instances cell | **agree** — correct |
| 5 | layer C appended: what becomes slack | **DIVERGE** — answer correct |
| 6 | stale slab declaration | **agree** — correct |
| 7 | sub-record type 0x0003, MU = 0 | **agree** — correct |
| 8 | sentinel offsets with crc ≠ 0 | **agree** — correct |
| 9 | physical length = F + 64 | **agree** — correct |
| 10 | codec 3 Content_Checksum_flag | **agree** — correct |
| 11 | planar bool P = 10, fill true | **agree** — correct |
| 12 | planar disk ordinal / decoded size | **agree** — correct |
| 13 | reject-layer vector's intact sibling | **agree** — correct, but see flag |
| 14 | float32 fill 0x7FC00001 | **agree** — correct |
| 15 | directory ends at 235 | **agree** — correct |

**Score: 14 agree / 1 diverge / 0 underdetermined.** No byte-level ambiguity: the single divergence changes no byte of any file.

## The divergence — Q5

**The claims.** The key names three structures that become slack: the prior generation's directory region, its **pre-trailer pad**, and its trailer. The answer names two — directory and trailer — and separates the pad explicitly: it "was *already* slack before this commit… it stays slack; it does not become slack."

**Adjudication: the answer is right.**

- §6.2 `[R-CNT-05]`, unconditionally and in the present tense: "Writers MUST place the directory so that no structure lies between its end and the trailer. Those bytes — the pre-trailer pad — are slack (§5.2)." The pad is slack in the generation that writes it, while that generation is live.
- §5.2 `[R-CNT-21]` enumerates slack as "alignment and slab gaps, the pre-trailer pad, and everything an earlier commit superseded" — the pad is listed *alongside*, not *within*, the superseded category.
- §21.6's table repeats the same three-way split: "alignment gaps, the pre-trailer pad, superseded structures."
- The question asks for **structures**. §5.2's class list defines a structure as "a stored-tile extent, a record extent…, the directory, or the trailer." The pre-trailer pad is not a structure at all — `[R-CNT-05]` makes a structure in that gap a file-scope validity error (row F9). So the pad cannot be an answer to "name every structure that becomes slack" on either count.

**Why the key went the other way, and the spec wart it exposes.** §20.3's "three shapes a commit takes" example is headed "▓ marks what the commit turned to slack", and its shape (a) prose reads "The slack is the old directory, pad and trailer." The ▓ run in the diagram spans `dir₁│pad│tr₁`. The key reproduced that list verbatim. But §2.1 `[R-CNF-01]` is explicit: "All text in this document is normative except: §1; any text labeled *Note*, *Example*, or *Rationale*." §20.3's example is non-normative and loses to `[R-CNT-05]`/`[R-CNT-21]`.

The sentence "The slack is the old directory, pad and trailer" is true as a statement of *what the slack is* — both agents agree on the identical byte set. It is the framing sentence "▓ marks what the commit **turned to** slack" that is loose, since the pad was never live. **Recommend a one-word fix in §20.3** ("▓ marks the bytes the live state no longer claims") so the example stops contradicting `[R-CNT-05]`; nothing else in the document depends on it, and no register row is affected.

Neither agent's answer is defective on the substance that matters: both correctly excluded everything of layers A and B (`[R-WRT-05]` byte-identical re-emission), and both correctly added the new generation's own pad and any gaps around C as slack-from-birth.

## Agreement-is-not-correctness flags

**Q13 — both agents asserted a pairing the text does not state.** `[R-VEC-04]` is one flat disjunction applied to both outcomes at once: "Every vector whose recorded outcome is reject-layer or reject-tile is built inside a file that also carries an intact sibling — **another layer, or another tile of the same layer** — whose decoded content the manifest records." Read literally, a *reject-layer* vector may satisfy the obligation with another tile of the rejected layer. Both agents concluded "another layer"; neither branch is assigned to an outcome anywhere in §24.

I hold the conclusion is nonetheless **entailed**, not merely preferred: §2.4 defines reject-layer as "the affected layer's data and metadata are not usable", and `[R-VEC-02]` requires the manifest to record "the decoded content a reader is to return from **every scope it can read**" — a reader can read no scope inside the rejected layer, so the intra-layer branch names a sibling whose content the manifest cannot record. The rule's own justification clause ("the content a reader that serves anything at all owes") closes it. So: correct, but derived rather than read off. **The key handled this better** — it disclosed the inference as an AMBIGUITY with both permitted readings; the answer stated the pairing as fact with the reasoning in a parenthesis. The text is worth tightening ("another layer for a reject-layer vector, another tile of the same layer for a reject-tile vector").

**Q4 — both agents agreed, both flagged the same real defect, and both are right about the number.** §21.1 does contain two incompatible sentences ("An instance names… one of several alternatives the condition text states" vs. "a cell reading — is one instance; the count is therefore mechanical"). The question asks how many instances the row *has*, and the counting rule answers that: **one**. I verified the mechanical rule independently — it reproduces §21.8's published "125 conditions over 244 named instances" exactly (F 39/61, L 50/100, T 26/45, R 10/38). The live case is **L42**, whose condition reads "gap, overlap, or out-of-ordinal placement" against an Instances cell of "—", so the row under-covers itself by two files under `[R-ERR-02]` and `[R-VEC-03]`, with nothing to distinguish it from a correct single-predicate row. Real finding, correctly reached by both.

**Q2 — the key's extra AMBIGUITY is overstated.** The key reports that `[R-SER-08]` fixes the logical value but not the byte a byte-oriented API returns. §19.4 step 8 `[R-RDR-04]` closes this: "Return the requested values' bit patterns unaltered… for every byte a conforming file can carry, the whole of this step (`[R-SER-08]` fixes what a reader returns for the one byte a conforming file cannot)." The specification does name `[R-SER-08]` as fixing the *return*, not merely the interpretation. Both agents answered the question identically and correctly (nonconforming; reader reports **true**; verifier: tile scope, reject-tile, at certification, row T2, and MUST NOT certify) — the divergence is only in the finding, and the answer's silence is the better reading here.

**Q3 — the key's OBSERVATION about suffix-range capability is sound** and the answer makes the same point inline: `[R-CNT-10]`'s SHOULD fallback ("a size probe plus an absolute range") makes the open three requests on a transport without suffix ranges, and §6.4 states "the baseline remote open is two requests" without naming that precondition. Appendix A's walkthrough confirms the two-request figure for the 128-byte file, ranges [64, 128) then [16, 20). Both agents correct.

## Spot-checks of the agreed answers against the text

- **Q7** — reserved-range emission genuinely makes the file nonconforming, not merely bad conduct: §21.6 draws the line explicitly ("a *reserved*-range type, whose emission `[R-CNT-15]` does make a violation") against the experimental range, which `[R-CNF-02]` leaves conforming. Reader ignore-record via `[R-CNT-18]`, verifier reject-layer at certification, row L26 (detector *verifier*). Both correct.
- **Q10** — row T20's Detector column reads *reader*, Detected *tile use*. Both correct; the key's contrast with `[R-MTA-09]`/row R4 (ignore-record for the identical constraint on a metadata frame) checks out.
- **Q11** — §14.3's own worked example gives `55 FD` for alternating values with fill true; zeroing the value region leaves `00 FC`. Both correct.
- **Q12** — `[R-GEO-06]`: s = 1·G₁ + 0 = 2, c = 1, N = 4, disk ordinal 6; `[R-SER-02]` planar numeric P·Bᶜ = 4·4 = 16. Both correct, including the entry landing at region byte 120 under `[R-IDX-01]`.
- **Q15** — `dir_offset + dir_length ≤ F − 64` gives F ≥ 299; §6.2's valid-values column and `[R-CNT-01]` force F mod 64 = 0; least such F is 320, trailer at [256, 320), 21 pad bytes at [235, 256). Both correct, and both correctly clear `[R-CNT-27]`'s 128-byte floor.
- **Q9** — §9.5's Note confirms the three-way F10/F16/F19 split and that residue carries no row of its own; §19.1 step 2 and `[R-LIF-05]` confirm the step and the no-backward-scan. Both correct.