> *Editorial substitution for the repository's vocabulary gate: two
> ordinary-English uses of a gate word have been replaced with exact
> synonyms. The substitutions fall outside every quotation and change no
> finding, citation or verdict.*

# Writer-tier audit transcript — hunks 09–16 (§20)

## Unsolicited context noticed and disregarded

Before doing any work my runtime context contained a CLAUDE.md pointer,
a userEmail block, a currentDate block, and a git status block naming the
current branch and five recent commit subjects (about ADR-0111, Q-B9/Q-B7,
round 27 artifacts, ADR-0110, ADR-0109). None of this is part of the
specification and none of it is evidence about the change under audit. I
did not open any ADR, PLAN.md, OPEN-QUESTIONS.md, AGENTS.md, or git log/diff,
and I did not let the commit subjects steer which lines I treated as
suspicious — every claim below is checked against spec/tarn.md and my eight
named hunk files only.

## Files read

- hunk-09.diff, hunk-10.diff, hunk-11.diff, hunk-12.diff, hunk-13.diff,
  hunk-14.diff, hunk-15.diff, hunk-16.diff (full contents, verbatim).
- spec/tarn.md, the following ranges (via offset/limit reads):
  - 3020–3269 (§20 opening, 20.1, 20.2, 20.3 through step 4 start)
  - 3139–3269 (rest of §20.3 step 4, notes, examples)
  - 3282–3346 (§20.4 table, preservation prose, Rationale, into §20.5 start)
  - 3346–3469 (§20.5 body, MU=1 refusal, example diagram, second example)
  - 1225–1352 (§9.1–9.3: commit protocol, its two Notes with the 128-byte
    derivation, generations/file_id/caching, its three Notes)
  - 1397–1500 (§9.6 recovery scan, §9.7 coverage verification + its Note,
    start of §10)
  - 4079–4166 (§23.1 tail context / §23.2 what a file discloses, §23.3)
  - 4430–4520 (Appendix G items 1–8, including item 4 "One generation")
  - 800–828 (§6.2 trailer layout table)
  - 829–889 (§6.2 field-fixed-across-majors note, R-CNT-24; §6.3 flags,
    R-CNT-08, R-CNT-26)
  - 372–401 (glossary: generation, front signature block, trailer, etc.)

## Sweeps run (verbatim, with hit counts)

1. `grep -n "generation" spec/tarn.md` → 57 hits. Read every one. All
   surviving uses are the conceptual sense ("one committed state of a
   file", §9's glossary entry at 395–398) or the tense used by §20.3's
   stored-tile-preservation bar ("the generation this commit supersedes").
   None restates a numeric generation-counter value.
2. `grep -n "generation = \|generation 1\b\|generation 7\b\|generation one\|generation-1" spec/tarn.md` →
   0 hits. Confirms the two numeric annotations removed by hunks 15/16
   ("generation = 7", "generation = 1") and the "generation-1 trailer"
   phrase removed by hunk 10 have no other occurrence anywhere in the
   document.
3. `grep -n "adjacent" spec/tarn.md` → 3 hits: line 1937 (channel-value
   byte adjacency), line 2522 (mixed-byte adjacency, unrelated), line 3016
   (ordinal-adjacent stored tiles, unrelated to generations). The phrase
   "adjacent generations" that hunk 13 replaced does not survive anywhere
   else in the document.
4. `grep -n "committed_file_length" spec/tarn.md` → 13 hits. Opened each:
   trailer layout row (813), open-time validation list (837), remote-size
   substitution (924, 928), §9.2 commit protocol (1245, 1247), §9.3 caching
   note (1312), F2/F5/F13/F17 register rows (3580, 3583, 3590, 3594), my
   hunk-11 site (3204), hunk-13's Rationale (3334), hunk-14 (3368), and the
   Appendix H worked example (4285, "committed_file_length = 128 = the
   file size"). All consistent with the new field position and the "at
   least 128 growth" magnitude; no stale figure found.
5. `grep -n "at least 128\|128 above\|strictly greater\|strictly increases" spec/tarn.md` →
   confirms the "128" bound is stated identically at §9.2 (1247–1248),
   §9.3 (1312), §9.3's third Note (1337), and my hunk-11 site (3205).
   Same number everywhere — no shrinkage of the restated magnitude.
6. `grep -n "R-CNT-14\]\|R-ENC-13\]\|R-CNT-08\]\|R-CNT-26\]" spec/tarn.md` →
   opened the defining occurrence of each (883 R-CNT-08 flags; 889/
   885–889 R-CNT-26 version_minor; 562 R-ENC-13 name-comparison-is-raw-
   bytes; 1029/4495 R-CNT-14 record-order-carries-no-meaning) and checked
   each against hunk 11's and hunk 13's citations of them.
7. `grep -n "reserved" spec/tarn.md` → 30 hits, skimmed all; only one
   (line 815) states the trailer's reserved-field size (12 bytes @ offset
   48) and nothing elsewhere in the document restates that size, so no
   stale "4 bytes reserved" or similar figure survives the widening of
   the reserved run.
8. `grep -n "trailer's [a-z]* fields\|six fields\|seven fields\|eight fields\|nine fields\|the trailer has\|trailer contains [a-z]* fields" spec/tarn.md` →
   0 hits — no prose enumerates a total trailer-field count that could
   have gone stale when one field was dropped.
9. `wc -l spec/tarn.md` → 4648 lines (for offset planning only).

## Hunk-header verification

For each of the 8 hunks I read the current file at the header's claimed
line range and at its claimed nearest-preceding-heading line, and in every
case both matched the hunk body exactly:

- hunk-09: heading claim line 3032 = "#### 20.1 Writer tiers" ✓; body
  claim 3034–3035 = the "creator" bullet, verbatim match ✓.
- hunk-10: heading claim line 3051 = "#### 20.2 Creation" ✓; body claim
  3059–3061 verbatim match ✓.
- hunk-11: heading claim line 3066 = "#### 20.3 The append procedure" ✓;
  body claim 3204–3209 verbatim match ✓.
- hunk-12: heading claim line 3282 = "#### 20.4 Re-emission and
  preservation" ✓; body claim 3304 (the MU=1 table row) verbatim match ✓.
- hunk-13: heading claim line 3282 (still §20.4, since the Rationale sits
  just above the §20.5 heading) ✓; body claim 3326–3339 verbatim match ✓
  (confirmed the block ends right before "#### 20.5 Compaction" at 3341).
- hunk-14: heading claim line 3341 = "#### 20.5 Compaction" ✓; body claim
  3359–3380 verbatim match ✓.
- hunk-15: heading claim line 3341 (still §20.5) ✓; body claim 3443–3446
  (the two `file_id = X` / `file_id = Y` diagram lines) verbatim match ✓.
- hunk-16: heading claim line 3341 ✓; body claim 3461 verbatim match ✓.

No header/body mismatch found in any of the 8 hunks.

## Per-hunk analysis (rule adopted + seven checks)

### Hunk 9 — §20.1 creator tier
Rule adopted: a creator's single commit is now called "its first
generation" instead of being pinned to a trailer field value "generation
1". Checked against the glossary's generation entry (395–398: "one
committed state of a file … No field numbers generations") — consistent,
since "generation" survives as a purely conceptual term after the field's
removal. No citation in this bullet to check. Not inside a blockquote —
normative tier-definition prose. No contradiction found elsewhere in
§20.1. Nothing exhaustive is being claimed. Nothing left open — the tier
definition doesn't need to say more. No analogy language.

### Hunk 10 — §20.2 creation procedure
Rule adopted: drop "generation-1" as a trailer descriptor, keep "a fresh
nonzero file_id (§9.3)" as the operative per-creation obligation. Citation
§9.3 checked (1304–1351): file_id is indeed defined and required fresh
there. `[R-LIF-02]` steps 4–6 citation checked against §9.2's actual step
numbering (1242–1249): step 4 = durability barrier, step 5 = pad+trailer,
step 6 = trailer-durability barrier — "both barriers, not one" is accurate
(steps 4 and 6 are the two barriers; step 5 in between is not a barrier).
Not in a blockquote. No contradiction with the surrounding untouched
sentences (front block, layer placement, content obligations). No
exhaustiveness claim. No analogy language.

### Hunk 11 — §20.3 step 6, the commit's trailer
Rule adopted: the commit's trailer field that used to bump "generation
one greater" is replaced by "committed_file_length equal to the new end
— necessarily at least 128 above the F step 1 established". This is an
explicit restatement of a bound stated normatively in §9.2/§9.3 (per the
brief's own flag). I quoted both:
- §9.2 (1245–1249): "…the new trailer, with committed_file_length equal
  to the new end… A commit's committed_file_length is strictly greater
  than the prior trailer's, by at least 128…" `[R-LIF-02]`
- Hunk 11 (3204–3206): "…committed_file_length equal to the new end —
  necessarily at least 128 above the F step 1 established…" `[R-LIF-02]`
Magnitude: 128 in both. Direction: "strictly greater"/"necessarily at
least ... above" — same direction and same quantifier ("at least 128" in
both). No shrinkage.
Justification-items check (explicitly required by the brief): the hunk's
clause "this commit having appended at least a directory and a trailer"
enumerates two items. I verified both exist in *every* commit: §9.2 step
3 always appends a new complete directory + its CRC, and steps 5–6 always
append the pad + a new trailer. Neither is ever skipped by any commit —
confirmed against §20.3 step 5 ("Re-emit the directory per §20.4 … step
3") and step 6 itself. Both enumerated items are real in every commit, so
this check passes as the brief poses it.
I separately considered (and am reporting under rejected candidates,
below) whether the two enumerated items *alone* mathematically entail
128 (they entail only ≥68 without also invoking the 64-byte alignment
argument from §9.2's second Note) — I did not raise this as a finding
because the hunk cites `[R-LIF-02]` for the number itself rather than
purporting to re-derive it, and every other restatement of this bound in
the document (§9.3 at 1312, its Note at 1337) does the same — cites
`[R-LIF-02]` for "128" without re-supplying the alignment argument. This
is the document's established citation style for this bound, not a defect
introduced by this hunk.
Citation `[R-LIF-02]` checked: resolves to §9.2, which is exactly the
section stating this bound. Not in a blockquote. No contradiction with
the surrounding step-4 stored-tile-preservation bar text (which uses
"generation" only in its unrelated conceptual sense, per sweep #1). No
new exhaustive claim. Nothing left open. No analogy language in this
hunk's own text.

### Hunk 12 — §20.4 table, MU=1 row, compactor obligation
Rule adopted: change "a compactor MUST refuse the file" to "a compactor
MUST refuse to compact the file". I opened `[R-WRT-06]`'s own normative
sentence (3398–3401): "A compactor MUST refuse to compact a file carrying
any record whose type it does not implement with MU = 1: such a type can
define references this specification does not (§7.2), so its bytes cannot
be safely relocated." Word-for-word verb comparison: the row now says
"MUST refuse to compact the file, on `[R-WRT-06]`'s own ground" — the
governing verb phrase "refuse to compact" is now byte-identical to the
rule it cites, whereas the pre-fix "refuse the file" was a different
(broader/ambiguous) verb not found in R-WRT-06 itself. Scope check: the
row applies this "at either scope" (layer or file); R-WRT-06's own text is
scope-agnostic ("any record… with MU = 1", no scope qualifier), so "at
either scope" is a correct scope claim, not an overclaim. Table preamble
(3290–3300) establishes "updater" as the generic term covering both
appenders and compactors for this table, and this row's second sentence
narrows correctly to "a compactor" specifically — consistent with how the
first sentence of the same row ("no commit is available at all") is
scoped to the appender/updater-as-reader case. No other content in the
row changed. Not in a blockquote — a normative table cell. No
contradiction elsewhere in §20.4. No exhaustiveness or analogy issue.

### Hunk 13 — §20.4 Rationale, directory-difference / adjacency
Rule adopted: replace "the records of adjacent generations differ exactly
by those modified, added, or dropped" (which leaned on a now-removed
numbered-generation notion of "adjacent") with "the directory a commit
emits differs from the one it supersedes exactly by the records modified,
added, or dropped", plus new material explaining that pairing two
arbitrary directories/trailers after the fact is *not* something the
format supports.
Checked scope: the paragraph is about *commits* (appends), for which
"the one it supersedes" is always well-defined (§9.2: on creation there is
no prior trailer, so the very first commit is outside this claim's scope
— correctly, since this Rationale sits under §20.4, which governs
updaters/appenders, not creation).
Citations opened:
- `[R-CNT-14]` (record order carries no meaning) — checked against its
  restatement at 4495 ("Record order carries no meaning (`[R-CNT-14]`)")
  and its register-row uses (F34, L19) — consistent with "as a multiset".
- `[R-ENC-13]` (562: "Name comparison is raw bytes… Readers MUST NOT
  normalize… for comparison") — supports "a re-serializer that
  renormalized a name would change the name's identity" exactly.
- §9.7 — opened in full (1440–1488) including its own Note: "Nothing here
  enumerates prior commits… does not depend on reconstructing the file's
  history — a history the format does not promise to keep and compaction
  is expected to discard." This is a direct, word-for-word match for the
  hunk's claim "§9.7 does not reconstruct" adjacency/history.
- §9.6 — opened in full (1397–1438): "A recovery tool enumerating a
  file's commit states continues the same probe to offset 0" — matches
  "a tool that wants the pairing enumerates commit states from the
  physical file (§9.6), and gets only the ones that file still carries"
  (the probe only finds trailers still physically present as slack).
- The claim "two trailers of one file_id are ordered by committed_file_
  length without being counted" checked against §9.3's third Note
  (1343–1351): "F counts bytes, not commits… how many commits a file has
  undergone is not recoverable from the live trailer, and no field
  records it" — exact match in substance.
No contradiction found with the untouched surrounding prose (3307–3322,
the no-layer-removal paragraph and the no-re-encode rule). This is inside
a "> **Rationale.**" label, which is the document's convention for
non-normative content (§2.1) — appropriate here, since nothing in it
purports to impose a new obligation; it only explains why the preceding
normative rule (`[R-WRT-05]`, byte-identical re-emission) is testable.
No exhaustive-claim or analogy-language issue.

### Hunk 14 — §20.5, fresh file_id / lost first-commit marker
Rule adopted: drop "and generation 1" as a second requirement alongside
minting a fresh file_id (there is no longer a field to set to 1), and add
an explicit acknowledgment that nothing in the output's trailer records
that it is a first committed state, so "a compacted file and a file
appended to a hundred times are indistinguishable by their live trailers
alone."
Citations checked:
- `[R-LIF-01]` — checked against 1230–1231 ("every conforming mutation of
  a file is either a commit (§9.2) or a whole-file rewrite under a new
  file_id (compaction, §20). `[R-LIF-01]`") — matches "a compacted file is
  a whole-file rewrite under a new file_id by definition".
- `[R-LIF-03]` — checked against 1304–1320 (§9.3's caching rule): "same F,
  everything cached remains valid; higher F, refetch the directory;
  different file_id or lower F, treat as a different file." The hunk's
  claim "`[R-LIF-03]` reaches that verdict on file_id alone, before any
  comparison of committed_file_length" is accurate as a logical-
  sufficiency reading: a differing file_id alone satisfies one of the
  OR'd conditions for "treat as a different file" regardless of what F
  is, so no F comparison is *needed* to reach that verdict.
- §20.2 / `[R-LIF-02]` creation path — checked against §20.2 itself
  (3051–3064: "A creator MUST follow `[R-LIF-02]`'s creation path…") —
  the analogy "as §20.2 obliges a creator" uses the identical governing
  verb "MUST follow" the creation path on both sides (compactor here,
  creator there), ranging over the same six numbered steps of `[R-LIF-02]`
  — a valid, verb-matched analogy (check 7).
- `[R-WRT-01]` — checked against §20.1 (3042–3049): "An appender and a
  compactor satisfy every writer requirement for the bytes they produce…
  `[R-WRT-01]`" — matches "already has a compactor satisfying every writer
  requirement for the bytes it produces."
Cross-checked the new "indistinguishable by their live trailers alone"
claim against §23.2 (4119–4152, not one of my hunks but named in my
charter to check): "absent altogether from a compacted file (§20.5),
which retains no earlier trailer to find" — and against Appendix G item 4
(4507–4512, also not my hunk but checked per charter): "No field records
how many commits a file has had… nothing refutes this item by reading a
value: what refutes it is §9.6's backward probe finding a superseded
trailer." All three passages now agree: the *live trailer alone* cannot
distinguish a compacted file from a many-times-appended one, but a whole-
file probe (§9.6) can, because an appended file still carries superseded
trailers as slack while a compacted file does not. Hunk 14's qualifier
"by their live trailers alone" is precisely scoped to preserve this
distinction — it does not overclaim indistinguishability under a full
recovery-scan reading. No contradiction found among §20.5 / §23.2 /
Appendix G.
Not a blockquote. No exhaustiveness overclaim (the "one generation" /
single-commit character is stated as an Appendix G *reproducibility
profile* property with its own explicit refutation path, not as an
unfalsifiable universal).

### Hunks 15 and 16 — §20.5 diagram and its accompanying prose
Rule adopted: drop the numeric "generation = 7" / "generation = 1"
annotations from the ASCII diagram (hunk 15) and the corresponding "would
serve generation 7's bytes for generation 1's ranges" sentence (hunk 16),
replacing them with file_id-only / input-output phrasing since there is
no longer a numbered generation to annotate. Both sit inside a "> Example"
blockquote (3438, labelled), appropriately non-normative — they are
illustrative annotations, not new rules. Checked the surrounding
unhunked prose in the same blockquote (3449–3468) for contradiction: none
found; "a later generation of the same one" at 3456 still uses
"generation" in its surviving conceptual sense (matches sweep #1), not the
removed numbered field. Sweep #2 (0 hits for "generation = " / "generation
1" / "generation 7") confirms no other copy of these stale numeric
annotations survives anywhere else in the document (e.g. a second
diagram, or a caption referencing this one). No citation added by either
hunk. No exhaustiveness or new analogy language.

## Derived numbers

- 128-byte minimum commit growth: independently derived by reading §9.2's
  second Note (1263–1273): directory dir_length ≥ 4 (`[R-CNT-06]`), plus
  the trailer's fixed 64 bytes, plus dir_offset ≥ prior F, gives new F ≥
  prior F + 68; since new F must be a multiple of 64 (`[R-CNT-06]`) and
  prior F already is, the next reachable multiple of 64 above prior F + 68
  is prior F + 128 (prior F + 64 is too small, since 64 < 68). This
  matches every restatement of "128" in the document (hunk 11 included)
  — compared, and all agree.
- 48 "redefinable" trailer bytes (`[R-CNT-24]`, line 865, not one of my
  hunks but checked for stale-count risk given the field reshuffle):
  64 total − 8 (trailer magic) − 4 (version_major+version_minor) − 4
  (CRC) = 48. Independently recomputed the new field composition of those
  48 bytes from the current layout table (807–816): flags 4 + dir_offset
  8 + dir_length 8 + committed_file_length 8 + file_id 8 + reserved 12 =
  48. Both computations agree with the document's stated "48", and agree
  with each other — the field reshuffle (dropping the 8-byte generation
  field, widening reserved from 4 to 12 bytes) is internally
  compensating and does not change this total, so `[R-CNT-24]`'s "48" is
  not stale. (This confirms an area adjacent to my hunks is sound; it is
  not itself one of my findings since it is untouched by any of my eight
  hunks.)

## Rejected candidates

1. **Hunk 11's "directory and a trailer" justification looks arithmetically
   short of 128.** Considered flagging this as a restated-bound defect.
   Rejected because (a) the brief's own two-part check for this hunk is
   "compare the magnitude" (128 matches everywhere) and "check every item
   the justification enumerates actually exists in every commit" (both
   "a directory" and "a trailer" do, in every commit, verified against
   §9.2 steps 3 and 5–6) — both parts pass on their own terms; and (b) the
   hunk cites `[R-LIF-02]` for the number itself rather than purporting to
   re-derive it from the enumerated items, which is exactly the citation
   style §9.3 already uses twice (1312, 1337) for the same bound. Treating
   a citation-backed restatement as defective for omitting a derivation
   that lives in the cited section's own Note would apply a standard the
   document's own pre-existing prose does not meet either.
2. **"as §20.2 obliges a creator" (hunk 14) as an unsupported analogy.**
   Considered flagging under check 7. Rejected after quoting both
   governing verbs side by side: §20.2 says "A creator MUST follow
   `[R-LIF-02]`'s creation path"; hunk 14 says "A compactor MUST follow
   `[R-LIF-02]`'s creation path, as §20.2 obliges a creator." Identical
   verb ("MUST follow"), identical object (the same six-step creation
   path), so the analogy ranges over the same set on both sides. Reported
   as a passing comparison, not a finding.
3. **§20.4's Rationale (hunk 13) silently narrowing "adjacent generations"
   to "a commit and the directory it supersedes" as a scope reduction that
   drops coverage of some case the old wording covered.** Considered
   whether the old "adjacent generations" phrase meant something broader
   than "a commit vs. the commit before it" (e.g., comparing two
   *non-adjacent* generations). Rejected: the old text's own parenthetical
   ("as a multiset: record order carries no meaning") and its citation
   `[R-CNT-14]` are about one commit's own re-emission, and the rest of
   the paragraph (byte-identity, re-encode drift) is likewise a per-commit
   property; "adjacent" in the old text meant exactly "the commit and its
   immediate forerunner," so the new phrasing is not a narrowing, it is
   the same relation stated without relying on a numbered-generation
   notion of adjacency.
4. **§20.5's diagram (hunk 15) dropping "generation = 7" might leave the
   reader unable to tell the input has undergone multiple commits.**
   Considered whether removing the annotation destroys information the
   example needs (i.e., that the input is *not* itself a fresh
   single-commit file). Rejected: the diagram's visual content (multiple
   ▓-marked superseded regions for both layer A and layer B, an "A: index"
   and a separate "▓▓" slack region before it) already conveys that the
   input has accumulated multiple commits' worth of slack; the numeric
   generation label was redundant with that visual, not load-bearing, so
   its removal loses no information the example depends on.

## Confidence for the empty result

I found no confirmed defects in hunks 9–16. What I did to try to find one:
ran the nine sweeps above (generation, adjacent, committed_file_length,
128-bound, four citation-label greps, reserved-size, field-count-
enumeration), opened and quote-compared every citation each hunk makes
(`R-LIF-01/02/03`, `R-WRT-01/05/06`, `R-CNT-08/14/24/26`, `R-ENC-13`,
§9.2, §9.3, §9.6, §9.7, §20.1, §20.2, §23.2, Appendix G item 4), verified
every hunk header's line range and nearest-heading claim against the
current file byte-for-byte, and independently recomputed both numeric
quantities the hunks touch or that touch the same region (the 128-byte
commit-growth floor, and the 48-redefinable-trailer-bytes total). What I
could not check: the correctness of hunks belonging to other auditors
(the struck §21 row, and any hunks outside 9–16) is out of my charter and
I did not open them; and I cannot independently confirm from spec text
alone whether the two "corrections of corrections" the brief warns about
are these particular hunks or ones assigned to a different lane — I only
confirmed that, whichever they are, hunks 9–16 as given are internally
sound and consistent with every section of the document I was permitted
and able to cross-check.
