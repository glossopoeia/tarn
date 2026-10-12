# Working notes — quiz-compare-b, slate B, divergence quizb-quizb-q3

## Disclosure
A relayed user request ("Go") appeared above this brief, labelled as the message that
launched this round; per the brief it is the launcher's message to the orchestrator,
carried out before I was spawned, needs no reconciliation with this brief, and does not
widen the access rule. I disclose it appeared and have not treated it as a task for me.
Nothing else was placed in my context before I began other than the computed task itself.

## Files opened (and only these)
- A: /Users/robertkleffner/Documents/GitHub/tarn-first-draft/scratch/cleanroom/editions/a/tarn.md
- B: /Users/robertkleffner/Documents/GitHub/tarn-first-draft/spec/tarn.md

## Sweeps run

1. `wc -l` on both files — A = 4981 lines, B = 4755 lines (established file sizes, no content claim).
2. `grep -n "14\.2\|14\.3"` on both files — located every occurrence of the section
   cross-references in both editions, to find §14.2/§14.3's body and every place that
   cites it. A: ~19 hits. B: ~18 hits (one fewer purely because B's §14.2 body merges
   two sentences A splits with an em dash — see EQUIVALENT reasoning below). Control:
   both files produced nonzero hits, so the grep works on the hard-wrapped text; a zero
   here would have meant the fragment needed splitting across a line wrap, which did not
   happen for "14.2"/"14.3" since those tokens never straddle a wrap point in either file.
3. `sed -n` ranges around the codec-4 clause (A line 2526-2542, B line 2381-2387) to read
   `[R-COD-07]`'s full prose in both editions verbatim.
4. `sed -n` on §14.2's full body in both editions (A 2026-2100, B 1887-1960) to read the
   P·Bᶜ decoded-size formula and the element-size table pointer verbatim.
5. `grep -n "^#### 12\.1\|^### 12"` on both files, then `sed -n` on the §12.1 body
   (A 1798-1826, B 1660-1690) to read the element-size table (uint8=1, uint64=8) verbatim
   in both editions.
6. `grep -n "^### 17\|^#### 17\."` and `grep -n "^#### 21\.3\|^### 21"` on both files to
   confirm §17.2 ("Codecs") and §21.3 ("Layer-scope violations") carry the same section
   numbers and titles in A and B — ruling out a renumbering-induced false citation
   mismatch between the two takers.
7. `grep -n "| L44 "` on both files to pull the §21.3 table row taker B cited by exact
   row id, and confirm it is byte-identical in A and B.

## Derived numbers

- Channel a (uint64, element size 8 per §12.1's table in both editions): P · Bᶜ =
  2,000,000 × 8 = 16,000,000 bytes. Matches both takers' figure.
- Channel b (uint8, element size 1): P · Bᶜ = 2,000,000 × 1 = 2,000,000 bytes. Matches
  both takers' figure.
- 0x7E000000 in decimal: 0x7E = 126; 126 × 16^6 = 126 × 16,777,216 = 2,113,929,216.
  Both takers state this figure; it checks out by direct hex-to-decimal conversion.
- 16,000,000 < 2,113,929,216, so the declaration is within the codec-4 cap: conforming.
  Both takers' verdict is arithmetically correct under both editions' stated rule, since
  both editions state the identical rule (same formula, same cap, same "largest governs"
  clause — see quotations in the finding).

## Rejected candidates

- Considered whether A's §21.3 table (taker A's "L44" citation) might differ from B's in
  wording or in which rule it cites, since the takers used different citation vocabulary
  (taker A: "§17.2 R-COD-07/L44"; taker B: "§17.2 ... [R-COD-07]; §21.3 rows L2/L44").
  Closed by the direct `grep` pull of the L44 row from both files (sweep 7): the row text
  is byte-identical between A (line 3938) and B (line 3730), including the "largest
  channel plane governs" clause and the `[R-COD-07]` tag, so the different citation
  phrasing is cosmetic, not a divergence in what either edition states.
- Considered whether B's row-L2 citation (overflow of a declaration-derived product)
  signals a different, stricter check that A lacks. Closed by reading L2 in B (sweep 6/7
  context): L2 is the generic 2^63-1 overflow guard restated for several products
  including "planar numeric P·Bᶜ" — a reader-side overflow check, not a different cap on
  codec-4's decoded-size ceiling, and the brief's question is well below any 2^63 bound,
  so L2 does not change the verdict in either edition. B citing it is additional context
  taker A did not quote, not a different rule.
- Considered whether A's and B's §14.2 differ substantively given the differing grep hit
  counts in sweep 2. Closed by reading both bodies in full (sweep 4): the one-hit
  difference is B's §14.2 collapsing two of A's em-dash-joined clauses into comma-joined
  clauses ("each for the layout its row states — a planar layer has no P · Q to form" in
  A vs "each for the layout its row states: a planar layer has no P · Q to form" in B, and
  similarly for the bool-value clause) — wording only, identical content, identical
  formula and table.

## Confidence / where little was found

I found no divergence between A and B on any passage this question turns on: the P·Bᶜ
formula (§14.2), the element-size table (§12.1), and the codec-4 cap plus "largest
channel plane governs" clause (§17.2 `[R-COD-07]`, and the §21.3 L44 table row) are
byte-identical in substance between the two editions (differing only in connective
punctuation that changes nothing decided). I treated this as a real finding rather than a
missed search by locating and quoting the exact sentence in both editions rather than
relying on either taker's paraphrase, and by independently recomputing both channel sizes
and the hex cap rather than trusting either taker's arithmetic.
