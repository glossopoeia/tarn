# Working notes, quiz-compare-a

Disclosure: a relayed "user request" (the literal text "Go") was prepended above the
computed task by the harness; it is the launcher's message to the orchestrator, not a
task for me, and it is disclosed here without being treated as evidence or as widening
the access rule below.

Access rule followed: only read
scratch/cleanroom/editions/a/tarn.md (edition A) and spec/tarn.md (edition B), both
under /Users/robertkleffner/Documents/GitHub/tarn-first-draft. No other file, no
directory listing (`wc -l` and the scratch/out mkdir are not directory listings of
content; only line counts were taken), no git history, no web.

## Method

For each of the 7 divergences, grepped the cited requirement ID in both editions,
located the cited section, and read the full paragraph(s)/table rows the question and
both takers' quotes turn on, in both editions, side by side. Where a quote spans a
table row, confirmed the row text byte-for-byte (modulo known hard-wrap and em-dash-
vs-comma rewrite artifacts). Judged each by the four-way test (LOSS / ADDITION /
REPORTER_ERROR / EQUIVALENT) and the byte-level test, not by taker confidence.

## quiza-quiza-03 — §21.2 reach rule / R-CNF-13

Grep: `R-CNF-13` in both files; `21.2` in both. Opened A lines 3853-3860 and
B lines 3678-3686 (§21.2 lead-in paragraph) plus the F1/F6/F8/F14 table rows (A
3870-3891 region, B equivalent). Text is word-for-word identical between editions
except B turns two em-dashes into commas ("Deriving it there yields F8, F14, F6 and
both of F1's instances, each asserting..." vs "...instances — each asserting..."),
a purely typographic rewrap with no content change. Both takers derive F1 (2
instances), F6, F8, F14 (1 each) = 5. Verdict: EQUIVALENT. No byte-level difference:
an implementation built from either text derives the identical row set and instance
count.

## quiza-quiza-07 — packed bool tile, fill=true, P=20, all real values false

Grep: `R-SER-03`, `R-SER-05`. Opened A §14.3 (lines ~2112-2147) and §14.5 (lines
~2165-2189); B §14.3 (lines ~1992-2027) and §14.5 (lines ~2045-2058). Both state:
decoded size = ceil(P/8); "every pad bit (§14.3) MUST carry the plane's channel's
fill bit" (R-SER-05), identical sentence in both editions. P=20: real positions
0-19 occupy bytes 0 (0-7), 1 (8-15), and bits 0-3 of byte 2 (16-19); pad bits are
bits 4-7 of byte 2 (P mod 8 = 4). All 20 real values false -> bytes 0,1 = 0x00,
0x00; byte 2 low nibble 0, high nibble = fill bit repeated = since fill=true,
0b1111 -> byte2 = 0xF0. Both takers: 00 00 F0. Verdict: EQUIVALENT.

## quiza-quiza-08 — codec 4 (lz4) decoded-size cap, R-COD-07

Grep: `R-COD-07`. Opened A lines ~2546-2560 ("Codec 4 — lz4" paragraph) and
B lines ~2432-2441; identical content, B only moves the "in a planar layer... the
largest governs" clause to its own sentence at the paragraph's end instead of an
em-dash aside mid-sentence (reordering, not a content change — both state the same
rule, same cap 0x7E000000, same "checkable from declarations alone", same
reject-layer-by-declaration framing). Checked the outcome-class heading at §21.3
("Outcome: reject-layer; the named layer is unusable...") identical in both (A uses
em-dash, B uses semicolon) and L44's row (detector reader, detected "layer access")
identical in both. Computation: 300,000,000 * 8 bytes = 2,400,000,000 >
0x7E000000 (2,113,929,216) in both editions' terms. Both takers: nonconforming /
reject-layer / layer / yes-detectable-from-declarations. Verdict: EQUIVALENT
("Nonconforming" vs "No" is the same verdict in different words).

## quiza-quiza-09 — dimension and channel sharing name "z", R-ENC-15

Grep: `R-ENC-15`. The cited sentence ("The last two are separate namespaces, so a
dimension and a channel of one layer are permitted to share a name — the ordinary
way to name a channel after the axis it samples.") is byte-identical in both
editions at their respective §4.6 locations. Verdict: EQUIVALENT.

## quiza-quiza-12 — §20.3 step 4, shrinking a dimension extent, the two legitimate routes

Grep: `20.3`, opened A's full §20.3 step 4 paragraph (lines 3207-3320) and B's
counterpart (lines 3059-3105+; the "A commit MUST NOT change one of these; the
change is a new layer, or a rewrite that re-declares it under a fresh file_id" clause
is byte-identical across editions). Also checked the following sentences in both
("a commit MAY drop the layer (§20.4) and add a new one under its name and other
declarations, the new layer being new whatever bytes its entries address") —
identical in both, which backs B's gloss "new layer under the same name" as the
same thing A's answer calls "a new layer (drop the old layer and declare a new
one)". Both name the same two routes. Verdict: EQUIVALENT.

## quiza-quiza-13 — unregistered record type, external definition flags govern, §20.4

Grep: `R-CNT-22`. Opened A §20.4 lines ~3493-3511 and B lines ~3330-3349. The
sentence "For a type the updater implements that this specification does not
register, the definition it implements the type from supplies the flags, and the
stored bits never do" is byte-identical in both. Checked the MU/PE table's
MU=0,PE=1 row text ("Retain byte-identical, extent content unmodified") — present
and identical in both editions, immediately following the quoted paragraph in each.
Both takers: type's own definition governs (MU=0,PE=1); may not drop. Verdict:
EQUIVALENT.

## quiza-quiza-14 — R-VEC-04, intact sibling requirement

Grep: `R-VEC-04`. Opened A lines ~4499-4516 and B lines ~4318-4335; the "Every
vector whose recorded outcome is reject-layer or reject-tile is built inside a file
that also carries an intact sibling..." paragraph is identical in substance between
editions, B again replacing em-dash-set asides with commas/semicolons (no content
change: "another layer, or another tile of the same layer where that layer is one a
reader is still permitted to serve" appears verbatim in both). Both takers: intact
sibling; manifest records its decoded content. Verdict: EQUIVALENT.

## quiza-quiza-15 — R-RDR-04, segment CRC failure mid-request on an interleaved layer

Grep: `R-RDR-04`. Opened A §19.4 full numbered procedure (lines 3066-3124) and B's
counterpart (lines 2934-2980). Step 3 ("Index chain") and step 8 ("Return") are
identical in content and order in both editions. The governing sentence — "A failure
inside the same request that takes layer scope instead — step 3's index-chain
failure ([R-IDX-04]) — bars the request's remaining entries and all further service
from the layer; the bar is prospective, so values the reader has already returned
under §19.2's timing stand" — is byte-identical in both editions (only the dash
punctuation style differs), and in both editions this sentence, and the `[R-RDR-04]`
tag, sit inside step 8's paragraph, not step 3's. Taker A cites "§19.4 step 8
(R-RDR-04)" (where the rule-tagged text actually sits); taker B cites "§19.4 step 3
(R-RDR-04)" (the step whose *failure condition* — the index-chain check — the
sentence is about). This is an imprecision of citation on B's part (the R-RDR-04 tag
is not on step 3), but it does not change B's answer: both takers give the identical
two verdicts, (a) earlier-returned values stand, (b) the layer is barred from all
further service for the rest of the session. The question asks only for the two
verdicts, not for the step number, so the citation variance does not bear on
correctness of the answer itself. Verdict: EQUIVALENT (same answer; B's citation of
"step 3" rather than "step 8" is an internal cross-reference imprecision in the
taker's working, not a divergence between what A and B *say*, since both editions
place the identical sentence in the identical place).

## Overall

All seven divergences are EQUIVALENT: in every case the cited passages are the same
text in both editions (allowing for the editions' consistent em-dash-to-comma/
semicolon rewrap, which is cosmetic), and both quiz takers reached the same
substantive answer in different words (or, for quiza-15, with one taker's citation
slightly less precise without affecting the answer). No LOSS, ADDITION, or
REPORTER_ERROR found: neither taker misread a passage that decides its question —
each taker's quoted text does appear, and does decide the question, in both
editions.
