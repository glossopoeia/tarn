# Verifier-comparator working transcript

## Disclosure
- A relayed "user request" above the brief, consisting of the single word "Go", was shown to me as
  the message that launched this round. Per the brief, it is the launcher's message to the
  orchestrator, carried out before I was spawned, not a task for me, needing no reconciliation with
  this brief, and it does not widen the access rule. I disclose that it appeared and treat it as
  settled; I did not act on it as an instruction.
- My context also carried, unasked, a project CLAUDE.md pointer to AGENTS.md, a long user
  auto-memory index (TARN-harness-process notes: "harness spec path", "lineage gate word list",
  "repair prose vs rules", "harness vs charter", "subagents on Sonnet", "refute phase", etc.), a
  git-status block (branch `readable`, recent "Readable" edit-log commits), and a commit/PR
  attribution-footer instruction. None of this is part of the TARN specification or evidence about
  it. I have not opened, searched, or relied on anything it names, and record only that it appeared.
- Per the access rule I read exactly four files: edition A
  (`scratch/cleanroom/editions/a/tarn.md`, 5004 lines), edition B (`spec/tarn.md`, 4810 lines), and
  the two walk transcripts (`transcript-verifier-a.md`, 456 lines; `transcript-verifier-b.md`, 834
  lines), all at the paths the brief names — no discrepancy. Both editions were too large for a
  single default `Read` and were read via targeted `sed -n` line-range extraction plus `grep -n`
  searches run with the Bash tool (not `rg`) against the files above only. I opened no other file,
  listed no directory other than creating/confirming my own scratch directory, and ran no git
  history, web search, or fetch.
- Because both editions are hard-wrapped (`> ` not present here — these are plain paragraphs
  reflowed at some column), I searched short, low-frequency fragments (5-10 words, no wrapped
  phrase) rather than full sentences, and proved every "not found" result with a positive control
  search run against the same file immediately before or after, confirming the search mechanism
  itself was working (e.g. the "necessarily from the experimental range" search returned 1 hit in A
  and 0 in B; I then ran a broader control, "necessarily", against B and got 5 unrelated hits,
  confirming grep was not silently failing against B's file).
- My scratch directory,
  `/private/tmp/claude-501/-Users-robertkleffner-Documents-GitHub-tarn-first-draft/fidelity-5/scratch/compare-verifier/`,
  was empty on arrival (confirmed via `ls -la` before writing). This file is the only file I wrote
  there. I did not list the sibling `out/` directory beyond writing my required output file into it.

## Sweeps run (see evidence object for the summary sentence)
1. `grep -n "reader" A | grep -i outcome` vs same on B → both hit at line ~301/302 ("reader
   outcome"), confirming §2.4's unqualified label exists byte-identically in both editions.
2. `grep -n "outcome names the scope"` on both → 0 hits in either (the phrase is wrapped across
   lines), so I widened to `grep -n "obligation on any reader"` → 1 hit each (A:3838, B:3663);
   `sed -n` around each hit showed the full §21.1 "Detection points name §19.2's reader tiers..."
   paragraph is byte-identical in substance between editions (only em-dash/comma/parenthesis
   punctuation differs, consistent with the project's "spruce-up pass" / readable-edition
   re-wrapping, per the user's own memory notes about that process — noted only as context for why
   punctuation differs, not acted on as instruction).
3. `grep -n "cannot execute a layer's codec"` → 1 hit in B only (wrapped differently in A); `sed -n`
   around §17.4 in both (A:2630-2652, B:2509-2525) showed the full paragraph byte-identical in
   substance.
4. `grep -n "The line is drawn"` / `"bar binds the commit as an actor"` → both present in both
   editions; `sed -n` around §20.3 step 4 in both (A:3260-3340, B:3100-3195) showed the
   fixed-declaration bar, its exception list, and its symptom list (T3, T14, T21, T22, T4, T5, T2,
   T17, T24, T25) byte-identical in substance.
5. `grep -n "structural cases"` / `"Nothing here enumerates"` → both present in both editions;
   `sed -n` around §21.6's two-structural-cases paragraph (A:4074-4095, B:3894-3915) and §9.7's
   closing note (A:1572-1575, B:1446-1449) showed byte-identical substance.
6. `grep -n "^#### 2.3"` then `sed -n` over the full §2.3 Conformance-classes section in both
   (A:152-280, B:206-335) — this is where the one confirmed LOSS was found (see cmp-verifier-01).
7. Control searches proving the zero: `grep -n "necessarily from the experimental"` (A: 1 hit,
   B: 0), `grep -n "is itself a violation"` (A: 1 hit, B: 0), `grep -n "governs a refusal on that
   last ground"` / `"closing paragraph names the other two"` (A: 1 hit, B: 0), each followed by a
   positive control (`grep -n "necessarily"`, `grep -n "is a violation"`-style broader searches)
   against B returning multiple unrelated hits, proving the search itself works against B's file
   and the zero is a real absence, not a wrapping miss.
8. `grep -n "unable to check a requirement on a capability"` → 0 in A, 1 in B (§21.6's closing
   paragraph) — confirming B *relocated* (not dropped) the full grounds-list sentence from §2.3 to
   the end of §21.6, with §2.3 left as a forward cross-reference "(§21.6 names the grounds)"; this
   is a reorganization, not a loss, since the content exists exactly once in each edition.
9. `grep -n "detectable"` across both editions as a broad control, confirming line-number
   correspondence throughout §2.4/§21.1 stays close (within a handful of lines) and the two
   documents track each other section-for-section.

## Derived numbers
- Register totals: 35 (F) + 49 (L) + 26 (T) + 10 (R) = 120, matching both walks' independent counts
  and §21.8's stated total; I did not recompute the full register from scratch (out of scope given
  the charter's focus on the cited passages) but spot-checked the F-row table in both editions
  (A:3850-3900ish, via the §21.2 header region) and found row text and rule-ID citations
  byte-identical where compared.
- V3 arithmetic: both walks independently derive F1=4,480, F2=13,120, F3=14,528, live-total=12,816,
  slack-total=1,712, and the "walk that does not complete" variant's partial-slack figures (A:
  10,068 against a different stopping assumption — intra-layer overlap discovered while walking A
  first, B's A tiles not yet summed; B: 5,892 against layer A's *own* two tiles overlapping, with
  A's claimants discarded wholesale). These are two *different* probe scenarios (A's walker assumed
  the overlap is between A's tile and something outside A triggering a mid-walk stop before B is
  reached; B's walker assumed A's two own tiles overlap each other, so all of A's claimants are
  discarded per §5.2's rule for a rejected layer) — not a text disagreement: both are consistent,
  separate illustrations of the identical slack-accounting rule in §5.2/[R-CNT-21], and both check
  out arithmetically against the same underlying F3/live-total figures. I did not find the document
  text itself differs at the cited sections (§5.2, §9.7, §20.3, [R-SLB-05], [R-LIF-02]).

## Rejected candidates
- I suspected the V1 "cannot establish" grounds-list might differ in content (not just location)
  between editions, since B's §2.3 compresses it to a forward reference. Closed by finding the full
  list verbatim at the end of B's §21.6 (line 3920), word-for-word matching A's inline §2.3 list
  (format major, MU=1 unimplemented type, codec/filter execution, layer/tile resource decline,
  user-metadata decode decline) — a relocation, not a content change. Not a finding.
- I suspected A's and B's V3 "walk that does not complete" worked examples might reflect a document
  difference in how a rejected layer's already-enumerated claimants are treated (A's figure,
  10,068, differs enormously from B's, 5,892). Closed by reading both scenarios' own stated setups
  (§3.2 in A's transcript vs. §2.4 in B's transcript): they are different starting assumptions about
  *which* violation stops the walk and when, not different rules. [R-CNT-21]'s "upper bound, never
  an under-count" property holds in both, confirmed by each walk's own internal arithmetic check.
- I suspected the register's Instances/count column might have been altered somewhere in B's
  rewrite (a readability pass is exactly where a maintainer might accidentally trim a clause). Spot
  checks at §21.1's instance-counting paragraph (A:3803-3833, B:3629-3663) found it byte-identical
  in substance; I did not exhaustively diff all 120 register rows given the charter's direction to
  prioritize the cited passages and the sections the verifier depends on most, within the effort
  available.
- I considered classifying verifiera-01 (the §2.4/§21.1 "reader outcome" ambiguity) as a
  REPORTER_ERROR against walker B for not raising it. Rejected: B's own Section 3 preamble
  ("the outcome name is unchanged, only the detecting actor... differ") shows B's walker read and
  understood the same distinction; it simply didn't package it as a formal "finding." Since the
  text is identical in both editions and B's walker wasn't wrong, not REPORTER_ERROR — recorded
  as an EQUIVALENT confirmation instead.

## Confidence / where I found little
- I did not find any case where the two editions' texts actually disagreed on a normative
  requirement, exception, quantifier, or worked figure at any of the six probes' cited passages, or
  at either walk's own two findings' cited passages. Everywhere I compared side-by-side sections
  (§2.3, §2.4, §9.7's closing note, §17.4, §20.3 step 4, §21.1, §21.6), the prose was byte-identical
  in substance, differing only in wrapping and minor punctuation (em-dash vs. comma/parenthesis),
  consistent with a careful, non-lossy rewrite. The one confirmed textual absence (cmp-verifier-01)
  is a dropped explanatory/derivational clause, not a dropped rule — the underlying rule (F35/F36)
  that licenses the derivation is present, identical, and independently sufficient in both editions,
  which is why neither walk's probe *answers* actually diverged because of it. I verified this
  confidence directly (not by absence of effort) by running the positive-control searches listed in
  "Sweeps run" item 7 above specifically to rule out a wrapping-induced false negative before
  concluding the clause was genuinely, not just apparently, absent from B.

## Findings (see structured result for full fields)
- cmp-verifier-01 — LOSS (not byte-level): §2.3's Conforming-reader bullet in A carries an explicit
  derivational clause and a citation breakdown that B's edition omits without restating elsewhere.
- cmp-verifier-02 — EQUIVALENT: verifiera-01's §2.4/§21.1 "reader outcome" ambiguity is present,
  byte-identically, in both editions; not a fidelity divergence between A and B.
- cmp-verifier-03 — EQUIVALENT: verifierb-01's §17.4/R-CNF-03 potential-conflict-if-read-in-isolation
  is present, byte-identically, in both editions.
- cmp-verifier-04 — EQUIVALENT: verifiera-02/verifierb-02's fixed-declaration-change-unwitnessed
  finding rests on byte-identical text (§20.3 step 4, §9.7, §21.7) in both editions.
- cmp-verifier-05 — OBSERVATION: probe V2's two citation routes (A: §2.3 inline + §21.1
  specialization; B: §7.2 + §21.2 rows + §21.6) reach identical verdicts; the only textual asymmetry
  behind the different routes is cmp-verifier-01's dropped clause.
- cmp-verifier-06 — OBSERVATION: probe V4's answers differ in walker thoroughness (B works out the
  unassigned-codec/L43 branch explicitly; A does not), not in document text — §17.4 and the L43 row
  are identical in both editions as far as checked.
