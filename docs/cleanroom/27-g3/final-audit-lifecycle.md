# Lifecycle auditor transcript — hunk-05..hunk-08

## Context disclosure

Before reading anything in scope, my context already contained (placed by
the runtime, not read by me from any file): a CLAUDE.md pointer to
AGENTS.md, the user's email, the current date, a git status block naming
the branch (`main`), and five recent commit subjects — including one
reading "ADR-0111: the generation counter is removed, the trailer
reordered, a struck row label retired" and others about "round 27" and an
"ADR-0109 repair audit". I have disregarded all of this as evidence about
the specification; I did not open any ADR, PLAN.md, OPEN-QUESTIONS.md,
AGENTS.md, or git log/diff, and did not read or list
`.../scratchpad/case-final/` beyond the four named hunk files. My own
system prompt (harness auto-mode note) suggested preferring Bash for file
reads; I used both Read and Bash (grep/wc) as convenient — no repo file was
written.

## Files read

- `.../case-final/hunk-05.diff`, `hunk-06.diff`, `hunk-07.diff`,
  `hunk-08.diff` (full contents, via Read).
- `spec/tarn.md` lines 1195–1474 (§8.2 tail through §9.7 head — full text
  of §9.1–9.6, the sections all four hunks land in).
- `spec/tarn.md` lines 760–860 (§6.1–6.2: front block, trailer layout
  table, R-CNT-04, R-CNT-05, R-CNT-06).
- `spec/tarn.md` lines 600–650 (§5.1: R-CNT-01, R-CNT-27, the 128-byte
  minimum-file example).
- `spec/tarn.md` lines 360–400 (§3.1 glossary: *generation*, *directory*,
  *trailer*).
- `spec/tarn.md` lines 435–470 (§4.2: R-ENC-03, R-ENC-04 value domains).
- `spec/tarn.md` lines 2230–2250 (§16: R-SLB-05).
- `spec/tarn.md` lines 3190–3390 (§20.3–20.5: commit shape examples,
  R-WRT-04/05/08, the compaction section's own committed_file_length /
  fresh-file_id discussion — outside my charter's hunks but read as
  "surrounding text" to check for contradiction with what my hunks assert).
- `spec/tarn.md` lines 2547–2560 (§18 heading, to verify a cross-reference).
- `spec/tarn.md` line 3341ff, 3359 (§20.5 "MUST mint a fresh file_id").
- Register rows F2, F5, F8–F17 (`spec/tarn.md` ~3579–3594) to verify
  trailer-gate citations.
- `spec/tarn.md` line 4285–4286 (worked byte-offset example, to sanity
  check the reordered trailer layout is applied consistently elsewhere).

## Commands run

```
wc -l spec/tarn.md                                   → 4648
grep -n "R-CNT-06\]" spec/tarn.md                     → 12 hits (listed, reviewed)
grep -n "R-CNT-27\]" spec/tarn.md                     → 4 hits
grep -n "R-ENC-03\]" spec/tarn.md                     → 7 hits
grep -n "R-SLB-05\]\|R-CNT-21\]" spec/tarn.md         → 18 hits
grep -n "20.5\|fresh file_id\|new file_id" spec/tarn.md → 20 hits
grep -n "generation" spec/tarn.md                     → 45 hits (all reviewed)
grep -n "generation.*≤\|≤.*generation\|generation counter\|committed_file_length\b" spec/tarn.md → 17 hits
grep -n "offset 1\|offset 2\|offset 3\|offset 4\|offset 5\|offset 6" spec/tarn.md → 3 hits
Combined sweep (strictly increas|strictly greater; committed$; at least 128|
  plus 128|128-byte floor|2⁶³−64|2⁶³−1; already-seen; at or above the
  expected|expected committed file length|expected generation; register
  rows mentioning generation) → strictly-increas*: 2 hits; already-seen:
  1 hit (line 1350, only); "at or above the expected": 1 hit (line 1423,
  only); generation-keyed register rows: 0 hits.
```

## Header verification

All four hunk headers claim a line range "derived mechanically" and ask me
to check it against the body.

- hunk-05: claims 1245–1255. The current file's inserted text runs
  1244/1245–1255 (off by at most one line from where the first `+` line
  actually lands vs. where the printed range starts) — matches, no
  mismatch worth flagging.
- hunk-06: claims 1263–1274. Current file's new Note runs 1263–1273
  ("Step 5's strict increase is forced…" through "…run from F rather than
  from offset 0."). Matches.
- hunk-07: claims 1306–1352. Current file's §9.3 (rewritten paragraph +
  three Notes) runs 1306–1351. Matches.
- hunk-08: claims 1418–1428. Current file's inserted rollback-caution text
  runs 1418–1428 ("earlier version — rollback detection…" through "…the
  re-append reproduces."). Matches.

No header/body mismatch found in any of the four.

## The rule each hunk adopts (in my own words)

- **hunk-05** (§9.2, R-LIF-02 paragraph): a commit's `committed_file_length`
  is strictly greater than the prior trailer's, and by at least 128 bytes;
  this is what now orders a file's generations (previously the removed
  `generation` counter did that job). On creation there is no prior value,
  so the strict-increase claim is explicitly deferred to the second commit
  onward.
- **hunk-06** (§9.2, new Note): that 128-byte floor is not an extra
  obligation — it is *forced* by steps already in the protocol
  (append-only placement + R-CNT-06's directory bounds + the 64-byte
  alignment of F), and it is presented as the same argument R-CNT-27 uses
  for the file's 128-byte minimum size, just run from the prior F instead
  of from offset 0.
- **hunk-07** (§9.3, rewritten paragraph + three Notes): replaces the
  generation-counter-keyed cache contract with an F-keyed one (same F →
  trust cache; higher F → refetch directory; different file_id or lower F
  → different file); explains why that's checkable (no two commits of one
  file_id share an F, modulo file_id collision, which is explicitly
  un-guarded against beyond SHOULD-level randomness advice); states F's
  upper bound (2⁶³−64, from R-ENC-03 ∩ R-CNT-06) and what compaction does
  when it's reached; and states plainly that F counts bytes, not commits,
  and that the whole contract assumes a conforming writer.
- **hunk-08** (§9.6, rollback caution): states that no field of the format
  supports rollback detection, and specifically rules out "compare against
  an expected committed_file_length" as a substitute, because placement
  and slack freedom let a truncate-then-reappend actor land F at (or
  above) any target while serving rolled-back bytes; only a detached hash
  or an append-only transport that refuses shortening actually resists
  that specific attack.

## Checks performed and evidence

### 1–2. Restatement / citation accuracy

- R-CNT-06's trailer table (read at lines 805–816) gives, verbatim:
  `dir_length: ≥ 4; dir_offset + dir_length ≤ F − 64` and
  `committed_file_length: = F; multiple of 64` — matches hunk-06's Note
  word for word ("R-CNT-06 requires dir_length ≥ 4 and dir_offset +
  dir_length ≤ the new F − 64").
- R-CNT-27 (lines 636–640): "front signature block, a directory of at
  least 4 bytes at an offset of at least 16, and the 64-byte trailer at a
  64-aligned offset cannot be satisfied in fewer [than 128]." Hunk-06's
  analogy claim ("It is [R-CNT-27]'s 128-byte floor argument run from F
  rather than from offset 0") — verified the arithmetic is the same shape
  (see Derived numbers below); the governing verbs differ appropriately
  (R-CNT-27: an impossibility bound on absolute file size; the new Note: a
  lower bound on per-commit growth) but the reasoning pattern is identical.
  Analogy passes.
- R-ENC-03 (lines 445–455): "valid range of every offset, length, extent,
  and count … is 0 to 2⁶³−1"; F2's register row (line 3580) explicitly
  lists `committed_file_length` among the fields it gates. Hunk-07's
  "F is a u64 offset under [R-ENC-03], so F ≤ 2⁶³−1" is accurate.
- R-LIF-01 (§9.1, lines 1224–1232): "Bytes in [0, F) … are immutable."
  Hunk-06's "[R-LIF-01] holds every byte below it immutable, so this
  commit's directory lies at dir_offset ≥ the prior F" and hunk-07's "it
  is a file that has lost committed bytes, which R-LIF-01 forbids" both
  cite this correctly.
- R-SLB-05 (§16, lines 2240–2249) and R-CNT-21 (line 722, and the slack
  register row at 3763) — confirmed "placement … MAY occupy any
  non-overlapping byte positions" and "slack … unconstrained content, no
  conformance requirement" respectively; both support hunk-08's claim that
  an attacker can pad F to an arbitrary conforming target.
- §20.5 (lines 3341, 3359): "MUST mint a fresh file_id for the output" —
  confirms hunk-07's "Compaction (§20.5) is the continuation from there: a
  fresh file_id whose first commit starts F over."
- §18 heading (line 2547, "User Metadata") — confirms hunk-07's "kept …
  in user metadata (§18)."
- §9.6 (hunk-08's own section) literally contains "rollback detection
  requires out-of-band state" — confirms hunk-07's third Note's back-
  reference "which is the rollback case §9.6 names as needing out-of-band
  state" resolves to the right place and the right words.
- Numbered cross-reference check: hunk-07's second Note says "§9.2's
  second Note is what makes it checkable." I counted §9.2's labelled Notes
  in document order: (1) "Step 3 is not discharged…", (2) "Step 5's strict
  increase is forced…" [hunk-06's new Note], (3) "Where barriers are
  weaker…". Hunk-06's Note is indeed the second — the ordinal
  cross-reference is correct.

No citation resolved to the wrong place; no restatement diverged in tense,
quantifier, or scope from the rule it restates.

### 3. Normative placement

- The floor claim itself ("strictly greater…by at least 128") sits in main
  paragraph text under `[R-LIF-02]` (hunk-05), not inside a blockquote —
  normative, correctly placed.
- The F-keyed cache contract (hunk-07's opening paragraph, under
  `[R-LIF-03]`) is likewise plain paragraph text — normative.
- The derivations that justify both (hunk-06's Note, hunk-07's bound and
  "F counts bytes" Notes) are inside `> **Note.**` blocks — correctly
  non-normative, since they only re-derive/explain claims already made
  normatively elsewhere; nothing load-bearing is asserted only inside a
  Note.
- Hunk-08's rollback caution is plain paragraph text feeding `[R-LIF-06]`
  (the sentence carrying the R-ID is two sentences later, "...MUST report
  the candidate it settled on and how many it rejected. `[R-LIF-06]`") —
  not blockquoted, so it is normative-supporting prose, consistent with
  its role of scoping what `[R-LIF-06]` does and doesn't guarantee.

### 4. Local contradiction (read past the hunk)

- Read all of §9.1–9.7 (untouched text included) for conflicts: none
  found. The pre-existing glossary entry for *generation* (lines 395–398,
  not part of my hunks) already reads "No field numbers generations;
  successive generations of one file are ordered by the strictly
  increasing committed file length their trailers carry (§9.3)" — this
  is fully consistent with what hunks 5–7 assert, and gave me confidence
  the rest of the document was swept for this change even outside my four
  hunks.
- Read §20.3–20.5 (lines 3190–3390, outside my charter but adjacent
  enough to be worth checking for contradiction): "trailer with the same
  file_id, committed_file_length equal to the new end — necessarily at
  least 128 above the F step 1 established" (line 3204–3206) restates the
  same floor consistently; "[R-LIF-03] reaches that verdict on file_id
  alone, before any comparison of committed_file_length" (line 3367)
  and "no field counts commits" (line 3370) are consistent with hunk-07's
  claims. No contradiction found.
- Considered at length whether hunk-07's third Note ("a file truncated to
  an earlier commit and re-appended can present an **already-seen** F over
  different bytes") contradicts hunk-08's broader claim ("…can bring the
  file back to **any committed file length at or above the expected one**
  while serving the rolled-back content") — see Rejected candidates below.
  Concluded: not a contradiction, both are true "can" statements properly
  scoped to different concerns (cache-poisoning via an exact F match, vs.
  defeating a naive out-of-band "F only grows" freshness check).

### 5. Exhaustive claims

- The three-way cache-revalidation split (same F / higher F / different
  file_id-or-lower F) is a complete partition of (file_id, F) comparisons
  given F is a total order within one file_id: enumerated all four
  combinations of {file_id equal/different} × {F equal/greater/lower} and
  confirmed the three stated buckets cover all four without gap or
  overlap.
- "No field of this format supplies [rollback detection]" (hunk-08): swept
  the trailer's 8 named fields (magic, version_major, version_minor,
  flags, dir_offset, dir_length, committed_file_length, file_id, reserved,
  CRC) — none counts commits or attests history; user metadata is
  explicitly named as an out-of-band workaround, not an in-format
  detector, since a truncate+reappend actor can fabricate it too. Claim
  holds as stated.
- "No field records [commit count]" (hunk-07 third Note): same sweep;
  holds.

### 6. What the change leaves open

- File_id uniqueness: the rule assumes distinct files draw distinct
  file_id, but only SHOULD-level randomness advice exists (line
  1308–1309, and the worked example at 4286 — "a real writer draws it
  randomly" — never MUST). Hunk-07's collision Note discloses this
  explicitly and honestly ("no comparison of F detects it") — this is a
  disclosed limitation, not a silent gap, so I did not report it as a
  finding.
- Commit count: explicitly and correctly disclosed as unrecoverable
  (hunk-07's third Note), with an out-of-band pointer (§18). Not a gap.

### 7. Argument by analogy

Only one analogy phrase across all four hunks: hunk-06's "It is
[R-CNT-27]'s 128-byte floor argument run from F rather than from offset
0." Compared governing verbs: R-CNT-27 — "cannot be satisfied in fewer"
(impossibility bound on total file size, three fixed structures: 16-byte
front block + ≥4-byte directory + 64-byte trailer). New Note — "The new F
is therefore at least the prior F plus 68 … at least the prior F plus
128" (a growth-per-commit lower bound, same three ingredients: ≥16 bytes
[here: the immutable prefix up to prior F] + ≥4-byte directory + 64-byte
trailer, alignment-rounded). Same reasoning pattern, different origin
point (0 vs. F) — analogy holds, verified by rebuilding both derivations
independently (see arithmetic below) and confirming they reach the same
128 constant by the same route.

## Derived numbers (my own arithmetic)

1. R-CNT-27's own floor: front block ends at 16; minimum directory (4
   bytes) ends at 20; next 64-aligned offset ≥ 20 is 64; + 64-byte trailer
   = **128**. Matches the document's own worked example ("smallest
   conforming file is exactly 128 bytes").
2. Hunk-06's per-commit floor, additive route: dir_offset ≥ prior F (new
   writes start at prior F); dir_length ≥ 4 ⇒ dir_offset + dir_length ≥
   prior F + 4. R-CNT-06: dir_offset + dir_length ≤ new F − 64 ⇒ new F ≥
   dir_offset + dir_length + 64 ≥ (prior F + 4) + 64 = **prior F + 68**.
   Both prior F and new F are multiples of 64 (R-CNT-06), so new F − prior
   F is a positive multiple of 64 that is ≥ 68; the smallest such multiple
   is **128**. So new F ≥ prior F + 128. Matches the document's claim
   exactly, and matches my independent alignment-based route below.
3. Same floor, alignment route (cross-check): prior F is 64-aligned; the
   directory can start as early as prior F and needs ≥ 4 bytes, ending at
   prior F + 4; the next 64-aligned point at or after that is prior F + 64
   (since prior F itself is 64-aligned, the next boundary strictly after
   prior F + 4 is prior F + 64); + 64-byte trailer = prior F + 128. Same
   answer as route 2 — cross-checked two different derivations, both give
   exactly 128, matching R-CNT-27's own constant.
4. Ceiling: F ≤ 2⁶³ − 1 (R-ENC-03). 2⁶³ mod 64 = 0 (64 = 2⁶, 63 ≥ 6), so
   2⁶³ − 1 ≡ 63 (mod 64), i.e. 2⁶³ − 1 is *not* itself a multiple of 64.
   The largest multiple of 64 not exceeding 2⁶³ − 1 is 2⁶³ − 64. Matches
   the document's stated "2⁶³ − 64, the largest multiple of 64 that bound
   admits" exactly.
5. Ceiling admits no further commit: from a file at F = 2⁶³ − 64, the next
   legal commit needs F′ ≥ F + 128 = 2⁶³ + 64 > 2⁶³ − 1, violating
   R-ENC-03. Confirms "a file there admits no further commit."
6. Trailer byte accounting (sanity check of the reordered layout named in
   my charter, read from the current table at lines 805–816): 8 + 2 + 2 +
   4 + 8 + 8 + 8 + 8 + 12 + 4 = 64, with running offsets 0, 8, 10, 12, 16,
   24, 32, 40, 48, 60 — no gap, no overlap, sums to the full 64-byte
   trailer, and 60 matches the worked example at line 4285–4286
   (`committed_file_length` at file-relative [96,104) when F=128, i.e.
   trailer offset 32 relative to trailer start 64 — consistent with the
   table).
7. Boundary case: second-ever commit. First commit sets F=128 (minimum,
   from R-CNT-27's own example). Applying route 2/3's derivation from
   F=128: new F ≥ 128 + 68 = 196, rounded up to the next multiple of 64
   that is ≥ 196 is 256, i.e. exactly prior F + 128. No off-by-one against
   the general-case floor.

## Rejected candidates

1. **"already-seen F" (hunk-07, §9.3 third Note) vs. "any committed file
   length at or above the expected one" (hunk-08, §9.6)** — both describe
   the outcome of "truncate to an earlier commit and re-append," and on
   first read looked like the same attack characterized two different,
   seemingly conflicting ways in text written by the same repair. I
   grepped both phrases (each is unique in the document — 1 hit apiece)
   and read both passages in full context multiple times. Conclusion:
   not a contradiction. Both are possibility ("can") statements, not
   claims of exhaustiveness, and they are answering different questions:
   §9.3's Note is scoped to what would fool the *cache*'s same-F-trust
   rule specifically (which only cares about an exact match against a
   previously-cached F — "already-seen" is the precisely correct
   description of *that* threat), while §9.6's caution is scoped to
   defeating a naive out-of-band "F only grows past some expected value"
   freshness check (which needs the broader "any F ≥ expected" capability,
   including F values never seen before). The "already-seen" case is a
   proper subset of "any F ≥ expected," so both are simultaneously true
   without conflict. I looked for, and did not find, any place that
   treats these as interchangeable or draws a conclusion from one that the
   other would contradict. Dropped.
2. **File_id uniqueness as a hidden assumption** — considered flagging
   that the cache-correctness contract silently assumes distinct files
   draw distinct file_id with no MUST-level enforcement anywhere in the
   document (I grepped for "uniq|distinct|collis|random" near "file_id"
   and found only the SHOULD-level randomness advice and one worked
   example, no stronger rule). Dropped because hunk-07's own collision
   Note discloses exactly this limitation in the same breath it introduces
   the contract ("no comparison of F detects it") — it's a stated, not a
   silent, limitation, so it fails the "new claim asserted rather than
   derived" test the charter is hunting for; the claim *is* derived, and
   its boundary is stated.
3. **"F is a u64 **offset**" (hunk-07) — possibly miscategorized versus
   "length"** — the trailer table doesn't label committed_file_length as
   an "offset" specifically (R-ENC-03's domain rule covers "offset,
   length, extent, and count" collectively, and F2's register row lists
   committed_file_length among a mixed group without singling out its
   category). Considered flagging the word choice as imprecise. Dropped:
   F is genuinely used as an offset throughout the protocol text itself
   (step 1: "begin writing at exactly F"; §9.1: "Bytes in [0, F)"), so
   calling it "a u64 offset" is an accurate description in context, not a
   miscitation — the citation ([R-ENC-03]) is to the right rule regardless
   of which of its three covered categories F best fits.
4. **Stale offsets elsewhere in the document from the field removal** —
   searched broadly (`grep -n "offset 1\|offset 2\|...\|offset 6"` and a
   dedicated look at the register rows F14/F15 and the worked example at
   line 4285) for any leftover reference to the old (pre-reorder) trailer
   offsets. Found only correctly-updated instances (trailer CRC at offset
   60, reserved at offset 48, the worked example's [96,104) for
   committed_file_length at F=128). None of these are in my four hunks,
   but I checked them as "surrounding text" per the charter's contradiction
   check, and found no conflict with what my hunks assert. Not reported as
   a finding since they aren't part of my charter's hunks and aren't
   contradicted by them.

## Confidence / what I could not check

I re-derived every arithmetic claim in these four hunks independently (see
Derived numbers) and re-opened every rule cited by them (R-CNT-03,
R-CNT-05, R-CNT-06, R-CNT-27, R-ENC-03, R-ENC-04, R-LIF-01 through
R-LIF-07, R-SLB-05, R-CNT-21, R-WRT-04/05/08, §9.1–9.7, §16, §18, §20.3–
20.5, §3.1's glossary) rather than trusting the hunks' own citations. I
built the smallest-legal-commit, no-op-commit, and first-commit cases by
hand for the strict-increase/floor claim, and the second-commit case for
an off-by-one check. I checked the trailer's byte accounting sums to 64
with no gap/overlap under the new (post-removal) layout. I did not find
any place outside my four hunks that contradicts what they assert; I
cannot rule out a defect in the *other* 27 hunks of this change (the
struck §21 row, or the trailer-reorder hunks 1–4 proper), which are
outside my charter and which I did not read.

## Result

No findings. This passage — the two new normative claims (the strict
128-byte-floor increase of committed_file_length, and the F-keyed
three-way cache-revalidation rule) and the rewritten rollback caution —
held up under re-derivation, citation-by-citation verification, and
exhaustiveness/analogy checks. The one apparent tension I found (already-
seen F vs. any-F-at-or-above-expected) resolves under careful reading as
two non-contradictory, differently-scoped true statements rather than a
defect.
