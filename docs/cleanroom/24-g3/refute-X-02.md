# Refute pass on X-02 (downgrade attacked: REFUTED / not-byte-level)

## What I read
- /private/tmp/.../r24audit/finish/finding-X-02.md
- /private/tmp/.../r24audit/hunk-01.diff, hunk-04.diff
- spec/tarn.md: lines 200-235 ([R-CNF-11]), 805-830 ([R-CNT-08], [R-CNT-26]),
  2375-2390 ([R-COD-10]), 2468-2480 (R4/zstd witness discussion),
  3038-3050 (§20.3 step 4 note pointing at §21.7), 3195-3250 (§20.5),
  3319-3396 (§21.1), 3396-3580 (register rows, grepped), 3634-3710 (§21.7, §21.8),
  4015-4040 ([R-VEC-03]/[R-VEC-04]), 4318-4370 (reproducibility profile items 8+).

## Greps run (exact)
1. `grep -n "21.7\|R-ERR-01\|R-ERR-02\|R-ERR-03" spec/tarn.md`
   -> 2382, 2474, 3045, 3231, 3321, 3334, 3348, 3544, 3634, 3697, 3704, 3716, 4027.
   These are every cross-reference to §21.7 and every [R-ERR-*] site.
2. `grep -n "^#### 21\.\|^#### 20\.\|^### 21\|^### 20" spec/tarn.md` -> section map.
3. `grep -n "R-CNT-26" spec/tarn.md` -> 824, 3069, 3230, 4325, 4363. No register row cites it.
4. `awk 'NR>=3396 && NR<=3580' spec/tarn.md | grep -in "file_id\|generation\|version_minor\|minor"`
   -> F2 (u64 above 2^63-1, incl. generation), F11 (generation is 0), F12 (file_id is 0).
   Nothing else. No row tests generation == 1, and no row tests file_id freshness.
5. Whitespace-normalised (`tr '\n' ' ' | tr -s ' '`) window greps for
   `(Neither obligation|two obligations|four obligations|three obligations)` and for
   `(witness in the output|no witness|has no witness|unwitnessed)`.
   Exactly two count sites survive: §20.5 "Neither obligation has a witness in the
   output alone (§21.7)." and §21.7 "§20.5's four obligations on a compacted file's
   trailer". No leftover "two obligations" anywhere.

## Question 1 — is the finding real as text?

Partly, and weaker than reported.

The finding's own headline word is "contradicts". It does not contradict.
"Neither obligation has a witness in the output alone" is a two-place quantifier
scoped over the two obligations immediately preceding it (the ignore-lane
carry-forward MUST and the version_minor SHOULD). Both of those are, per hunk 4's
new §21.7, unwitnessed. The sentence is TRUE under the repaired §21.7. It asserts
no exhaustiveness — "neither of these two" is not "only these two". §21.7 saying
four are unwitnessed and §20.5 saying two of them are unwitnessed is a superset
relation, not a conflict.

What is real: hunk 4 desynchronised a counted cross-reference pair. Before the
commit the two sites matched ("two" / "Neither"); after it §21.7 attributes four
obligations to §20.5 while §20.5's own pointer sentence still covers half of them.
That is an editorial asymmetry a re-read around the landing site would have caught.
It introduces no false statement.

I also checked whether "Neither" could be mis-scoped onto {SHOULD >= input's minor,
[R-CNT-26]'s fallback floor}. Under that strained reading the second conjunct would
be false, since the [R-CNT-26] floor ("lowest version_minor that defines every
feature present in the file") is computable from the output alone. But [R-CNT-26]
is a SHOULD with no register row (grep 3), so even that reading produces no
violation, no outcome class, and no reject. And §21.7's own gloss "the floor its
version_minor SHOULD take" resolves the referent to §20.5's floor.

## Question 2 — is it byte-level?

No. I could not move the emittable set or any accept/reject verdict under any
construction I built.

The disputed sentences are both *descriptive claims about witnesses*, not
obligations on any actor. Under BOTH readings (two unwitnessed, four unwitnessed):

- §20.5's four obligations bind unchanged and verbatim: "It MUST mint a fresh
  file_id for the output ... and generation 1", "The output trailer MUST copy the
  input's unknown ignore-lane flag bits forward", "the output's version_minor
  SHOULD be at least the input's". Nothing in either sentence relaxes a MUST.
  A compactor's emitted bytes are identical under both readings.

- No corpus obligation flows from §21.7. §21.1 line ~3346 is decisive:
  "The subsections after §21.5 are not part of the register and carry no rows:
  neither this completeness clause nor the instance arithmetic below reaches
  §21.6's defined non-violations, §21.7's account of what no check detects, or
  §21.9's limits." [R-ERR-02] (§21.8) and [R-VEC-03] (§24, line ~4027) both key
  on *register rows*. §21.7 has none. So the finding's stated consequence — a
  corpus author hunting for rows that witness file_id/generation — produces no
  vector, no file, no byte either way. §21.8's "121 conditions over 277 instances"
  is untouched by the two->four change for the same reason.

- No reader/verifier behaviour moves. [R-CNF-11]'s per-requirement "unable to
  check" report is confined to "a capability or resource ground"; reusing a
  file_id is neither, and §21.7 ¶1 already states in terms that these are not
  [R-CNF-11] cases and "the verdict is unaffected".

## Constructions tried against the downgrade's premise

The downgrade's premise is "which obligations are excused from carrying a
register row changes no byte". I attacked it five ways.

1. **Actor enumeration for the antecedent.** Who can ever observe that a file is
   a compaction output? Reader: no. Verifier: no. Appender/updater: no. A second
   compactor compacting the output: no. §21.7's own new clause states the ground —
   "nor any record that it is a compaction output at all". Unlike the charter's
   template, this antecedent genuinely never obtains for any actor but the
   compactor itself, whose MUSTs are unchanged. Dead end for me.

2. **Is the disputed file conforming?** Yes — and this is the one place the
   finding could have become byte-level, so I pushed it. A compaction output with
   a reused (nonzero) file_id or generation 7 exhibits NO register row: grep 4
   shows only F11 (generation == 0) and F12 (file_id == 0), and a conforming input
   cannot supply file_id 0. So [R-CNF-05] does not bar it, and the file is
   single-file conforming. But the permissive reading does not exist: §20.5's
   MUSTs bar the compactor from emitting it under both readings. The set does not
   move because no reading relaxes the MUST, not because the file is
   nonconforming. The downgrade reaches the right answer by a different route
   than the one the discriminating test names, and the answer survives.

3. **Register-completeness back-door.** §21.1's completeness clause IS normative.
   Could a reader inferring from §20.5 that file_id/generation ARE witnessed then
   demand rows, and reject a file when none fire? No: the clause makes a missing
   row "a defect in this document", not a licence or a bar, and detectability is
   the gate — these are undetectable, so no row is owed.

4. **Verifier report / verdict.** Could the count change what a verifier reports
   or certifies? §21.7 ¶1 forecloses it ("nothing about the file is left
   undetermined and the verdict is unaffected"), and [R-CNF-11] limits
   unable-to-check to capability/resource grounds.

5. **Reproducibility profile (item 8, ~line 4325).** It already carves the
   compactor out explicitly — "A compactor's output is therefore reproducible only
   modulo its trailer: [R-WRT-06]'s fresh file_id is no function of content".
   Byte-identity across compactors is pinned by pinning the compactor, under both
   readings alike.

## Verdict
DOWNGRADE_STANDS. The finding is at most an editorial desynchronisation of a
counted cross-reference; its central claim of contradiction is false; and no
construction moves an emitted byte or an accept/reject verdict.

## Missing sentence
n/a — the refutation is grounded in text present in the document (§21.1's
carve-out of §21.7 from the completeness clause and instance arithmetic; §20.5's
unrelaxed MUSTs; §21.7 ¶1's [R-CNF-11] disclaimer).
