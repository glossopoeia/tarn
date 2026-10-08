# Quiz comparator — slate A — working transcript

Scratch dir: /private/tmp/claude-501/-Users-robertkleffner-Documents-GitHub-tarn-first-draft/fidelity-3/scratch/quiz-compare-a/
Files read (only these two, per ACCESS RULE):
- A: /Users/robertkleffner/Documents/GitHub/tarn-first-draft/scratch/cleanroom/editions/a/tarn.md
- B: /Users/robertkleffner/Documents/GitHub/tarn-first-draft/spec/tarn.md

## Divergence quiza-quiza-q14

Question: does index_encoding = 0x50 (reserved 2-0x7F) and index_encoding = 0x90
(experimental >= 0x80) fall under the same register row/outcome, or different ones?

### Searches run

1. `grep -n "index_encoding" scratch/cleanroom/editions/a/tarn.md` -> 7 hits, including:
   - line 1141: field-table row for `index_encoding` in §7.4 (the layer record):
     "1 = raw-segmented; any other value — including 0, reserved 2–0x7F, and the
     experimental range ≥ 0x80 (§10) — is a validity error at layer scope (§15)"
   - line 3925: §21.3 register row:
     "| L31 | Layer record's index_encoding is a value other than 1 — 0, reserved
     2–0x7F, or experimental ≥ 0x80 | index_encoding 0; reserved 2-0x7F; experimental
     >= 0x80 | reader | layer access | `[R-CNT-23]` (§7.4) |"

2. `grep -n "index_encoding" spec/tarn.md` -> 7 hits, same positions shifted:
   - line 993: identical field-table row text (byte-for-byte), in §7.4.
   - line 3781: identical L31 register row text (byte-for-byte), in §21.3.

   Control: both greps returned the same count (7) and the same substantive hits,
   proving the search terms are present verbatim in both files (not hard-wrap
   artifacts) — confirmed further since "index_encoding" never breaks across a
   wrapped line in the matched rows.

3. Section-heading locations confirmed with
   `grep -n "^#.*7\.4"` and `grep -n "^#.*21\.3"` in both files: §7.4 "The layer
   record" and §21.3 "Layer-scope violations" exist in both editions, at
   different absolute line numbers (A is longer overall) but the same content
   at those headings.

4. `diff` of the §21.3 table block (rows L22/L23/L31 and surrounding rows) between
   A (lines 3888-3940) and B (lines 3744-3796): the table rows themselves are
   byte-identical. The only diff found is in the *prose paragraph* right after
   the table (A lines 1145-1155 vs B lines 997-1006), which restates the same
   list of reserved/unassigned-value violations (layout, codec, filter,
   index_encoding, channel-type, A_slab, fill length, crc_of_crc_array) under
   the same outcome ("validity error at layer scope, except where another rule
   assigns a different scope") and the same requirement id `[R-CNT-23]`. A
   phrases it as one sentence with an em-dash aside; B splits it into two
   sentences ("A reader MUST treat... Such violations include..."). No item is
   added, dropped, narrowed, or widened; the exception clause (duplicate layer
   name -> file scope, R-ENC-15) is identical in both.

### Conclusion for q14

Both editions put the reserved range (2-0x7F) and the experimental range
(>= 0x80) under the single register row L31, with the single outcome
"reject-layer" (validity error at layer scope), cited to the same requirement
id `[R-CNT-23]`. This is true identically in A and B: the field-table row
(§7.4) and the register row (§21.3, row L31) are byte-identical between the
two editions. The surrounding prose paragraph is reworded (one sentence split
into two) but states the same list and the same scope/exception, so it carries
no normative change.

Taker A's answer ("L31", single shared row, reject-layer) and taker B's answer
("Same row: L31", single shared row, reject-layer) are the same answer in
different words — B's answer merely prefixes the row id and quotes the row
text with its "L31 |" table-cell marker included, while A quotes the row text
without that marker. Both cite the same two locations (§7.4 and §21.3 row
L31) and reach the same conclusion.

Byte-level test: since the field-table row, the register row, and the outcome
(reject-layer under R-CNT-23) are identical text in A and B, an implementation
built from B alone would emit the same accept/reject verdict and the same
bytes on this question as one built from A alone. No divergence.

Verdict: EQUIVALENT.
