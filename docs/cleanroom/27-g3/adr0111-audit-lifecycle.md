# Lifecycle auditor transcript — case-adr0111

## Unsolicited context notice

Before I began, my context already contained material I did not request:
a project-instructions block (pointing at AGENTS.md), a user memory-file
index, a userEmail value, and a currentDate value, plus harness/tool-usage
reminders (bash-preference, auto-mode, browser-tool notes). None of this is
part of the specification and none of it is evidence about the change under
audit. I disregarded all of it and did not use any of its contents (repo
history, prior TARN working notes, etc.) in forming the findings below.

## What I read

1. My four hunk files, in full:
   - hunk-05.diff (claims: lands spec/tarn.md 1245-1255, nearest heading
     "9.2 The commit protocol" @1234)
   - hunk-06.diff (claims: lands 1263-1274, same nearest heading @1234)
   - hunk-07.diff (claims: lands 1306-1345, nearest heading
     "9.3 Generations, file_id, caching" @1304)
   - hunk-08.diff (claims: lands 1412-1421, nearest heading
     "9.6 Recovery scan (not a reader behavior)" @1391)
2. spec/tarn.md, the following ranges, via the Read tool:
   - lines 1190-1439 (§8.2 tail, all of §9.1-9.7 through the coverage-
     verification opening) — the post-change text of all four hunks plus
     surrounding untouched prose.
   - lines 800-900 (§6.2 Trailer, §6.3 Version and flag gates, start of
     §6.4) — the trailer's post-change field table and validation order.
   - lines 610-749 (§5.1 Anatomy, §5.2 Byte coverage) — R-CNT-01,
     R-CNT-27, R-CNT-21, R-CNT-03, R-CNT-05 definitions and the worked
     128-byte-minimum-file example.
   - lines 360-401 (§3.1 glossary) — the *generation* glossary entry, to
     confirm it already reads "No field numbers generations..." consistent
     with my hunks (this entry itself is not in my charter; I only read it
     to check for a contradiction against my hunks' claims).
   - lines 430-470 (§4.2 Integer types) — R-ENC-03's exact text.
   - lines 2225-2290 (§16 Slabs and Alignment) — R-SLB-05's definition and
     a second, broader use of it at line ~3012.
   - lines 2995-3060 (§20.1-20.2) — a third use of R-SLB-05
     ("placement is otherwise free") confirming it is the document's
     general placement-freedom citation, not narrowly scoped to per-layer
     tile ordinal placement — this resolved a candidate finding (see
     "Rejected" below).
   - lines 3334-3430 (§20.5 Compaction) — checked the "fresh file_id...
     starts F over" claim in hunk-07 against compaction's actual creation-
     path obligations, and checked the "no field counts commits" claim
     against §20.5's own (already-updated, not-mine) prose making the
     identical point.
   - lines 3560-3613 (§21.2 File-scope violations, tail) — located the
     struck-row Note (F11) mentioned in my brief as a sanity check that it
     exists and is coherent; this table is not in my charter and I did not
     audit it.
   - lines 4095-4145 (§23.1 end / §23.2 What a file discloses) — checked
     the "how many commits... not recoverable... deployment... keeps it
     out of band or in user metadata" claim in hunk-07 against this
     section's fuller treatment of the same fact (the count *is* forensically
     recoverable pre-compaction via the §9.6 probe). Resolved as consistent,
     not a contradiction — see "Rejected" below.
   - `grep -n` sweeps for: `generation` (whole file, to check for any
     stale reference to the removed field left behind by text bordering my
     hunks); `\[R-CNT-03\]` through `\[R-CNF-05\]` (to locate every rule
     cited by my hunks); `rollback|truncat` (to check the register has no
     now-stale rollback-specific row); `#### 21\.` (to see the register's
     per-scope condition-count lines, for context only — not audited,
     outside my charter).
3. `wc -l spec/tarn.md` to get the file's total line count (4641) before
   reading, purely to plan Read offsets.

I read no other file. I did not read full.diff, any other hunk file, any
file under docs/, PLAN.md, OPEN-QUESTIONS.md, AGENTS.md, or any git history.
I ran no git commands.

## Hunk-header verification

All four hunk headers check out against the current file:

- hunk-05: post-change text at spec/tarn.md 1244-1249 (dir/pad/trailer
  step 5, "by at least 128") plus 1251-1255 (creation-path exemption)
  matches the file exactly; nearest heading claim (9.2 @1234) correct.
- hunk-06: the added Note appears at 1263-1273, matching (off by one on
  the closing line count, which includes the trailing blank line — not a
  real mismatch).
- hunk-07: post-change §9.3 body (1306-1345) matches the file exactly;
  nearest-heading claim (9.3 @1304) correct.
- hunk-08: post-change §9.6 span (1412-1421) matches the file exactly;
  nearest-heading claim (9.6 @1391) correct.

No header/body mismatches found.

## Rule each hunk adopts, in my own words

- **hunk-05**: A commit's committed_file_length (F) is required to be
  strictly greater than the prior trailer's F, by at least 128 bytes; this
  is what lets F serve as the ordering key for a file's generations
  (previously the generation counter's job). The very first commit
  (creation) is exempted since there is no prior F to compare against.
- **hunk-06**: A proof (non-normative Note) that the "≥128" floor in
  hunk-05 is *forced*, not an extra writer obligation — re-deriving it
  from R-LIF-01 (immutability), the no-directory-reuse rule, and
  R-CNT-06's dir_length/dir_offset+dir_length bounds, explicitly framed as
  R-CNT-27's minimum-file-size argument re-run from the prior F instead of
  from offset 0.
- **hunk-07**: Rewrites §9.3 to key the caching/revalidation rule
  (R-LIF-03) on F instead of the removed generation counter: within one
  file_id, F strictly increases (cites R-LIF-02), so a matching
  (file_id, F) pair identifies one committed prefix, giving the same
  three-way cache revalidation (same F valid / higher F refetch directory
  / different file_id or lower F treat as different file). Three added
  Notes: (a) why the revalidation is sound and checkable, given hunk-06's
  proof; (b) F's upper bound and what happens at it; (c) F counts bytes
  not commits, the count is not recoverable from the live trailer alone,
  and the whole contract assumes a conforming writer — a truncate-and-
  reappend can replay an already-seen F, which is the rollback case
  hunk-08 names.
- **hunk-08**: Rewrites §9.6's rollback caution: no field of the format
  supplies out-of-band rollback detection, and specifically an "expected
  F" is not a substitute, because placement freedom (R-SLB-05) and
  unconstrained slack (R-CNT-21) let an attacker who truncates and
  re-appends pad the file back to any F at or above the one a client
  expects, while serving the rolled-back content. Names what does still
  work: a detached hash, a signed (file_id, F) pair held elsewhere, or an
  append-only transport.

## Re-derivations I actually built

**Strict-increase floor, general case.** Per step 1 the commit begins
writing at exactly the prior F. R-LIF-01 holds every byte below the prior
F immutable, so every new byte — including this commit's directory — lies
at an offset ≥ the prior F. R-CNT-06 requires dir_length ≥ 4 and
dir_offset + dir_length ≤ new_F − 64. Combining: new_F ≥ prior_F + 4 + 64
= prior_F + 68. Both prior_F and new_F must be multiples of 64
(R-CNT-06's "= F; multiple of 64" on committed_file_length), so their
difference must be a multiple of 64; the smallest multiple of 64 that is
≥ 68 is 128. So new_F ≥ prior_F + 128, tight and achievable (dir_offset =
prior_F exactly, dir_length = 4 exactly, pad = 60 bytes to the next
64-boundary: delta = 4 + 60 + 64 = 128). This matches hunk-05's "by at
least 128" and hunk-06's derivation exactly. I checked the three edge
cases the brief calls out:
- *Smallest legal commit* (no new tiles/records, dir_offset = prior_F):
  covered above, gives exactly 128 — the bound is tight, not merely an
  upper estimate.
- *Commit that changes nothing* (re-emits only an unchanged, possibly
  large, retained directory): still forced through the same dir+pad+
  trailer append, still strictly increasing (delta ≥ 128, generally much
  more since a real directory re-emits every retained record — §9.2 "(3)
  append the new complete directory — re-emitting every retained record").
- *First commit of a file (creation)*: explicitly exempted by hunk-05's
  own added sentence ("There being no prior committed file length, the
  strict increase above binds from the second commit onward"), and
  confirmed against §9.2's creation-path paragraph, which has no "prior
  trailer" to compare against. Correct scoping.

**Compaction does not break the "within one file_id" scoping.** §20.5
(read, not in my charter, only for cross-check) confirms a compactor
"MUST mint a fresh file_id" and "MUST follow [R-LIF-02]'s creation path:
the output has no prior trailer" — so compaction is exempt from the
strict-increase-vs-prior-F comparison for the same reason file creation
is, and hunk-07's "Within one file_id" qualifier correctly fences off
this case.

**Three-way cache revalidation, exhaustiveness.** Given (file_id match?,
F comparison) the four raw combinations are: same-id&same-F, same-id&
higher-F, same-id&lower-F, different-id (any F). hunk-07's text merges
same-id&lower-F with different-id into a single "different file" arm.
Under strict monotonicity, same-id&lower-F cannot occur for a conforming
writer (checked below); merging it with different-id is a correct
(defensive) choice, not a gap, and I confirmed all four raw combinations
are covered by exactly one of the text's three named arms.

**Upper bound arithmetic (this is where I found the defect — see
Findings).** R-ENC-03 bounds every u64 offset/length/count field,
committed_file_length included (confirmed against the F2 register row at
§21.2, which lists committed_file_length among the fields R-ENC-03
governs), at 0 ≤ value ≤ 2⁶³ − 1. Separately, §6.2's trailer field table
requires committed_file_length to be "= F; multiple of 64," and §6.2's
prose validation list repeats "is a multiple of 64." 2⁶³ − 1 is odd (2⁶³
is even, so 2⁶³ − 1 is odd), and no multiple of 64 is odd, so no
conforming trailer can ever carry committed_file_length = 2⁶³ − 1. The
true reachable ceiling is the largest multiple of 64 not exceeding
2⁶³ − 1, i.e. 2⁶³ − 64 (since 2⁶³ = 64 × 2⁵⁷ is itself a multiple of 64).
hunk-07's added Note states "F ≤ 2⁶³ − 1 ... a file at that ceiling
admits no further commit" — describing a state (F literally equal to
2⁶³ − 1) that can never arise in a conforming file. See Finding B-01.

I checked whether this was already true of the *removed* generation
Note it replaces, to make sure I wasn't flagging a pre-existing,
unrelated imprecision: the old text (visible in hunk-07's `-` lines) read
"1 ≤ generation ≤ 2⁶³ − 1 ... and each commit adds exactly 1, so a file
standing at 2⁶³ − 1 admits no further commit." Generation had no
multiple-of-64 (or any other) side constraint beyond R-CNT-06's raw
range, so 2⁶³ − 1 *was* exactly reachable for generation, and that Note
was tight. The imprecision is new, introduced by re-keying the same
sentence shape onto a field that carries an extra domain constraint the
old field didn't have — exactly the failure mode the brief names ("a new
claim introduced to replace the old one that is asserted rather than
derived").

## Citations opened and checked

- `[R-CNT-03]` (hunk-05) — §5.2 line ~725-729: "Writers SHOULD zero the
  gaps they create... the pre-trailer pad." Matches "zeroed by advice."
- `[R-LIF-02]` (hunk-05, 06, 07) — the commit-protocol rule itself
  (§9.2), correctly the rule under which the "by at least 128" claim is
  filed in both places it appears.
- `[R-CNT-06]` (hunk-06) — §6.2 table: dir_length ≥ 4; dir_offset +
  dir_length ≤ F − 64. Matches exactly.
- `[R-CNT-27]` (hunk-06) — §5.1 line ~636-640: the 128-byte
  minimum-file derivation (front 16 + dir ≥4 at offset ≥16 + trailer 64,
  64-aligned). Confirmed hunk-06's re-derivation from the prior F is the
  same argument shape with "prior F" standing in for "offset 0" (checked
  side by side, see re-derivation above) — a correctly labeled analogy,
  not an overclaimed identity.
- `[R-LIF-01]` (hunk-06, 07) — §9.1: committed-prefix immutability.
  Correctly cited both places.
- `[R-LIF-03]` (hunk-07) — the caching rule itself; this is the rule
  hunk-07 rewrites, correctly tagged.
- `[R-ENC-03]` (hunk-07) — §4.2: 0 to 2⁶³ − 1 valid range for u64
  offset/length/count fields. Correctly cited for the raw bound; see
  Finding B-01 for the composition problem with the separate
  multiple-of-64 rule.
- `[R-SLB-05]` (hunk-08) — checked its home definition (§16, "A layer
  that declares neither alignment nor a slab makes no layout promise")
  *and* its broader reuse at §20.2 ("placement is otherwise free
  (`[R-SLB-05]`)") to confirm the document already uses this citation as
  the general "structures need not be tightly packed" rule, not narrowly
  for per-layer tile ordinal freedom alone. hunk-08's "placement within a
  commit is free (`[R-SLB-05]`)" matches this established usage.
- `[R-CNT-21]` (hunk-08) — §5.2: slack is unconstrained in content, no
  conformance requirement on it. Matches "slack is unconstrained."
- The unchanged register-row citation just above hunk-08's span (§21.2
  rows F8, F14, F17 — "the magic, the trailer CRC and the length
  cross-check") — checked against the §21.2 table: F8 = trailer magic,
  F14 = trailer CRC, F17 = committed_file_length vs transport size.
  Matches exactly (this text is untouched by my hunks; checked only
  because it borders hunk-08 and check #4 asks for the whole passage).

All citations resolve to text that says what the citing sentence claims,
except the composition issue in Finding B-01 (which is not a
misattributed citation — R-ENC-03 says exactly what's claimed — but a
failure to also apply the multiple-of-64 constraint from the same
section's field table when computing the practical ceiling).

## Findings considered and rejected

1. **R-SLB-05 might be the wrong citation for "placement within a
   commit is free" in hunk-08**, since its home section (§16) is phrased
   around per-layer tile ordinal placement. Rejected after finding the
   identical phrase "placement is otherwise free (`[R-SLB-05]`)" already
   used generically at §20.2 for the same kind of claim (any structure's
   placement within a commit, subject to declared invariants) — this is
   the document's established general usage, not a hunk-08-specific
   stretch.
2. **Possible contradiction between §9.3's "no two commits... share a
   committed file length" (hunk-07, main text + Note 1) and its own
   Note 3 admitting a truncate-and-reappend can produce an already-seen
   F.** Rejected: Note 3 explicitly scopes the stronger claim ("The
   contract above also assumes a conforming writer"), so the caveat is
   disclosed in the same subsection rather than silently contradicting
   the main claim. This is the brief's "LEFT OPEN" check being properly
   answered by the hunk itself, not a gap.
3. **hunk-07's Note 3 ("a deployment needing that count keeps it out of
   band or in user metadata") vs §23.2's fuller statement that commit
   count *is* forensically recoverable via the §9.6 probe until
   compaction.** Rejected as a genuine contradiction after reading §23.2
   in full: §23.2 frames the probe-based recoverability as a *privacy
   leak* to be closed by compacting before publication, not as a
   reliable mechanism a deployment should lean on; hunk-07's Note is
   giving functional advice for a deployment that *needs* a durable
   count (the probe disappears on compaction, so it can't be relied on).
   The two statements answer different questions and don't conflict on
   the facts (both agree: not recoverable from the live trailer alone;
   both agree the probe is the other avenue, one flagging it as a leak,
   the other silently declining to recommend it as a solution). Not
   reported.
4. **Symbol overload of "F"**: §9.1 defines F as "the live trailer's
   committed file length," while hunks 5-7 use "F" for the committed
   length of arbitrary (not necessarily live) trailers, qualified as
   "prior F" / "new F" / "the generation whose committed file length is
   F." Considered as a possible NORMATIVE_FORCE/OTHER finding but
   rejected: every instance outside §9.1 is qualified in context, this
   is standard technical-writing symbol reuse, and I found no sentence
   where the ambiguity could change a reader's conclusion.
5. **Register condition-count sweep (§21.2's "35 conditions" against the
   struck F11 row)**: noticed while sanity-checking the struck-row Note,
   but this table, its row count, and the struck-row mechanics are
   outside my four hunks and my charter (a different auditor's
   assignment per the brief's structure). Not investigated further and
   not reported here.

## Findings

One finding, B-01 — see structured output. It is graded byte_level =
false: it sits inside a labelled, non-normative Note (§9.3's second added
Note in hunk-07), the document's own convention exempts labelled
blockquotes from normative force, and the actual conformance-relevant
bounds (R-ENC-03's raw range, §6.2's multiple-of-64 requirement) are
untouched and correctly stated elsewhere — resolving the imprecision
would not change which byte sequences any conforming reader or writer
must accept or emit, only the accuracy of an explanatory aside.
