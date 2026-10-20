# Quiz comparator — slate B — working transcript

Disclosure: a relayed "user request" (the single word "Go") was prepended above
the computed brief by the harness; per the brief's own instructions this is
the launcher's message to the orchestrator, carried out before this session
was spawned, is not a task for this session, needs no reconciliation with
this brief, and never widens the access rule. It is noted here and not acted
on further.

Access actually used: only the two permitted files were opened, by absolute
path, with `sed -n` line ranges located via `grep -n` for section headings and
rule IDs within those same two files. No directory was listed. No other file,
registry, docs/, or web source was read.

Files:
- A = /Users/robertkleffner/Documents/GitHub/tarn-first-draft/scratch/cleanroom/editions/a/tarn.md (5004 lines)
- B = /Users/robertkleffner/Documents/GitHub/tarn-first-draft/spec/tarn.md (4810 lines)

## Method

For each of the six divergences, located the cited sections in both A and B
by `grep -n` on the section heading and the rule ID, then read the full
section(s) with `sed -n`, then diffed by eye (and once with `diff` on an
exact line range, §15.3) to find any substantive difference, as opposed to
pure rewording/re-ordering. Classified per the charter's four kinds, applying
the byte-level test, and noted any taker citation that looked like a slip.

## q02 — §6.2 trailer layout, §6.4 R-CNT-09 (suffix-window containment)

Read A §6.2 (lines 830-925), A §6.4 (925-969); B §6.2 (698-792), B §6.4
(792-832).

dir_offset=1,998,900, dir_length=120 in both editions' trailer layout table
is quiz-supplied data, not spec text; the region formula dir_offset,
dir_offset+dir_length) and the containment test ("if the fetched buffer
contains the directory region, request 2 is unnecessary") are byte-identical
in R-CNT-09 across A and B (only wording/paragraph-break differences
elsewhere in §6.4, e.g. A: "A remote reader MUST handle a 200 response to a
range request (HTTP's terms, RFC 9110 ... abort or accept the full body
deliberately" vs B's reordered "A remote reader MUST handle a 200 response to
a range request: it aborts, or accepts ... The terms are HTTP's (RFC 9110)").
No numeric constant, no quantifier, no outcome differs.

Both takers: region = [1998900, 1999020); window [1999000, 2000000) does not
contain it (1998900 < 1999000) so containment fails and request 2 is
required. Same answer, same arithmetic, different phrasing of the inequality
direction (A: "begins after 1,998,900"; B: "begins 100 bytes earlier"/
"region_start >= window_start fails"). No misreading either side.

Verdict: EQUIVALENT.

## q03 — §10.2/§10.3 numeric spaces, §7.2 R-CNT-15, §2.3 class list

Read A §10.2 (1597-1623), A §10.3 (1623-1641), A §7.2 (1009-1098), A §2.3
(179-200ish, R-CNF-02 vs R-CNF-03 definitions). B §10.2 (1470-1496), B §10.3
(1496-1513), B §7.2 (843-927).

Numeric-space table, experimental-range rule, and R-CNT-15's MU-gate text
("An unknown record type at file scope: MU=1 -> reject-file; MU=0 ->
ignore-record ... a record type from the experimental range is conforming
(S10.3's prohibition binds the writer's conduct, not the bytes, [R-CNF-02])
... one from the reserved range ... emitting it is a violation") are
byte-for-byte identical in content between A and B (B's §7.2 sentence order
is split into shorter sentences, no content change).

One wrinkle: the A-taker's citation reads "§2.3 [R-CNF-03]" for the
"conforming TARN file is a pure predicate on bytes" point; checking A's own
§2.3 (and the identical text in B's §2.3, not separately re-quoted here since
both editions define R-CNF-02 and R-CNF-03 in the same roles at the same
place), R-CNF-02 is the file-conformance-is-a-pure-predicate rule the A
taker's reasoning actually uses, while R-CNF-03 is the adjacent "conforming
reader" rule (no subset profiles, core codecs/types) a few lines below it in
the same subsection. This is a citation slip within the A taker's own
apparatus, not a difference between what A and B say — both editions place
R-CNF-02 and R-CNF-03 identically, and the taker's stated reasoning and final
answer track R-CNF-02's content regardless of the label used. It does not
change the answer to (a)-(d) and is not a text divergence between editions.

Both takers agree on all four sub-answers: (a) experimental, (b) reject-file/
not nonconforming, (c) ignore-record/not nonconforming, (d) no.

Verdict: EQUIVALENT.

## q04 — §6.1 front signature block, R-CNT-04 residency

Read A §6.1 (786-830) and B §6.1 (655-698) in full.

Identical content: local/remote reader definitions, the residency test,
"MUST verify the full block by byte equality ... MUST treat any mismatch as
reject-file", "MAY defer or omit the check" when the bytes are not resident,
same Rationale and Note blocks. Only prose-level differences (B spells out
"bytes are resident when the reader already holds them after its open" where
A leaves that as implicit from the local/remote-reader definitions above it;
B's Note says "no further prefix" where A says "no other prefix" of a
conforming file being constant — same meaning).

Both takers: (a) must detect, reject-file, decided by residency (bytes
resident in a whole-file mmap); (b) no obligation, decided by residency (the
remote reader anchored at the trailer never makes [0,16) resident). Same
answer, same concept named.

Verdict: EQUIVALENT.

## q11 — §19.1 step 4 (duplicate layer name), §4.6 R-ENC-15/R-ENC-13

Read A §19.1 (2938-2995) and B §19.1 (2810-2863) in full; spot-checked A
§4.6 (552-598) against B §4.6 (436-482) with `diff` on the matching line
ranges.

§19.1 step 4's duplicate-name text is identical in substance between A and
B, down to "Uniqueness is decided first, and over the raw name bytes whether
or not each name is itself well-formed[,] ... [R-ENC-13] makes name
comparison a byte comparison, which needs no valid name; so two layers whose
name fields are byte-identical are a duplicate even when neither name is
valid" (B adds the connective "because" where A uses an em dash — a
punctuation-only difference). The one `diff` hit in §4.6 was purely
sentence-boundary rewording ("as a validity error at the owning scope —
except for a key inside a user-metadata document, where [R-CNT-25]'s
quarantine governs and the outcome is ignore-record" vs "... with the same
exception for a key inside a user-metadata document ([R-CNT-25])"); no rule,
scope or outcome changed.

Both takers: yes; reject-file; invalidity does not defer the duplicate
determination (raw-byte comparison decides it first, independent of the
name's own well-formedness). Same answer.

Verdict: EQUIVALENT.

## q12 — §20.3 step 4 (appender vs rewrite: extent growth, fixed declarations)

Read A §20.3 (3207-3330, through the fixed-declarations paragraph) and B
§20.3 (3059-3180) in full.

The permitted-changes list ("a dimension extent MAY grow, and MUST NOT
shrink ...") and the fixed-declarations list ("the layout, the
linearization and the index encoding, the codec and the filter, the rank
and the dimension order ...") with the "A commit MUST NOT change one of
these; the change is a new layer, or a rewrite that re-declares it under a
fresh file_id" sentence are identical in both editions, word for word except
for paragraph breaks (A runs the whole step 4 as one block; B breaks the
permitted/fixed-declarations material into its own paragraph after the
numbered list item). No change to what MAY grow, what MUST NOT change, or
what the only alternative to an appender commit is.

Both takers: (a) yes (extent growth permitted); (b) no (codec fixed while a
tile is stored); must do a new layer or a rewrite under a fresh file_id.
Same answer.

Verdict: EQUIVALENT.

## q13 — §15.3 entry validity, §20.5 R-WRT-06 (regenerating a region)

Read A §15.3 (2257-2290) and B §15.3 (2125-2158) with `diff`; read A's
R-WRT-06 regeneration passage (3640-3690) and B's (3475-3520) in full.

`diff` on §15.3 showed only one line changed: A "govern notwithstanding the
general owning-scope mapping of [R-ENC-03]/[R-ENC-04]" vs B "override the
general owning-scope mapping of [R-ENC-03] and [R-ENC-04]" — synonym
substitution, no table row, class or outcome changed. Table rows (structural
reject-tile for offset=sentinel/length-not-sentinel, etc.) are identical.

The §20.5 passage is identical in substance between editions, including the
operative sentence: "[R-WRT-06] then leaves it two disposals, since it can
neither reproduce the entry nor invent a replacement: drop the layer, which
§20.4's table licenses and whose loss the rewriter SHOULD report as that
table says, or refuse." Both editions state exactly two dispositions and
foreclose "carry forward unchanged" by the same "can neither reproduce ...
nor invent a replacement" clause.

Both takers: [drop the layer, refuse (to rewrite)]; No (third option is not
available). Same answer, same two named dispositions.

Verdict: EQUIVALENT.

## Overall

All six divergences the mechanical matcher flagged turned out, on reading
both editions at the cited passages, to be cases where A and B say the same
thing in different words (occasionally different sentence breaks or a
synonym swap, e.g. "govern notwithstanding" / "override"), and the two takers
gave the same answer in different words. No LOSS, ADDITION, or genuine
REPORTER_ERROR (a misreading that changed an answer) was found; one taker
citation slip (A/q03, "§2.3 [R-CNF-03]" where the content matches R-CNF-02)
is noted but did not change that taker's answer and is not a divergence
between the two editions, so it is reported as a sub-note under q03's
EQUIVALENT finding rather than as its own REPORTER_ERROR finding, since the
charter asks for one finding per divergence id.
