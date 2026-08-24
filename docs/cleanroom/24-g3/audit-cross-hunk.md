# Cross-hunk consistency audit — r24, four hunks

## Disclosure

Read: the four hunk files hunk-01.diff … hunk-04.diff (via one `cat` loop, no
directory listing beyond the explicit glob), and `spec/tarn.md` (sections read
in full: §5.1, §6.2, §6.3, §9.1, §9.3, §10 entire, §17.1–§17.4, §18.1–§18.2,
§19.2–§19.3, §20.3 step 4, §20.5 entire, §21.1–§21.9, Appendix G items 2 and 8
and its closing paragraph, Appendix H).
Ran: `wc -l`, `grep -n` over spec/tarn.md only, and one python3 script that reads
only spec/tarn.md and counts register rows/instances.
Did NOT read: full.diff, docs/, PLAN.md, OPEN-QUESTIONS.md, AGENTS.md, README.md,
conformance/, spec/registry.json, git history, the web.

Unrequested context appeared before I began: a project-instruction file pointer
and an index of the maintainer's memory notes naming prior-round themes. I did
not open any of the named notes and drew no conclusion from the index.

## Grouping (worked from the text, not the section numbers)

- **Group A — the compacted file's trailer obligations.** Hunks 1 and 4.
  Hunk 1 edits the §20.5 sentence two lines above `Neither obligation has a
  witness in the output alone (§21.7)`; hunk 4 rewrites the §21.7 sentence that
  that cross-reference lands on, changing *two* to *four*.
- **Group B — completeness claims about register rows.** Hunks 1 and 2.
  Hunk 1: `one row for each identifier space §10.2 tabulates (L31, L33, L34,
  L36, L43, L45, R1)`. Hunk 2: `Five rows are outside that reasoning`.
- **Group C — where a rule is established rather than what it says.** Hunks 2
  and 3. Hunk 2: F5's floor `precedes that order`. Hunk 3: R6's Governing rule
  moves from `[R-CNT-25]` to `[R-MTA-04]`.
- **Group D — what witnesses a §20.3-step-4 declaration change.** Hunk 4 alone
  states it; hunk 1's row list (L43 codec, L45 filter) is the same commit's own
  falsifier.

## Rule each repair adopts

1. **Hunk 1.** The two extension vehicles §21.6 does *not* make conforming reach a
   file only as values registered as reserved-range violations, and the register
   carries F36 + L25 for a record type plus one row per identifier space of §10.2.
2. **Hunk 2.** F5 (the 128-byte floor) reaches a file declaring a format major
   other than 1, because the floor is established before any field §6.2's gate
   consults exists.
3. **Hunk 3.** (a) R6's governing rule is `[R-MTA-04]`, not `[R-CNT-25]`.
   (b) R8 covers both the overflowing magnitude and the bare tokens, and they are
   one instance, not two.
4. **Hunk 4.** §20.3 step 4's bar is witnessed only in part; codec changes are
   *sometimes* witnessed; filter changes and length-preserving sample-offset moves
   are never witnessed; §20.5 imposes four unwitnessed trailer obligations.

## Searches run

    grep -n "^#\{2,4\} " spec/tarn.md              -> outline
    grep -n "witness" spec/tarn.md
      1103, 2471, 3046, 3231, 3649, 3653, 3660, 3666, 3670, 3673, 3678, 3680,
      3684, 3689
    grep -n "Neither obligation" spec/tarn.md      -> 3231 (single hit)
    grep -n "mis-strided" spec/tarn.md             -> 3639, 3661
    grep -n -i "compact" spec/tarn.md              -> 61,63,366,611,636,656,669,
      812,938,1163,1239,1368,1941,2198,2907,2911,2993,3075,3086,3305,3313,3594,
      3687,3692,3919,3941,3949,3953,4179,4262,4265,4327,4329,4331,4334,4335,4364
    grep -n "R-MTA-04\|R-ENC-12\|R-MTA-03\b"       -> 488, 2454, 2568, 2591, 2721,
      2724, 2797, 2799, 3440, 3466-3469, 3473, 3561, 3569, 3573-3578, 3774, 3876
    grep -n "R-CNT-27\|R-CNT-24\|R-CNT-01\b"       -> 569, 575, 771, 803, 1385,
      3405, 3408, 3422, 3430, 3432, 3785

    python3 (reads spec/tarn.md only): rows 121, instances 277
      R4=16 R6=4 R7=6 R8=2 F5=2 F1=2 L45=3 L43=3
    -> §21.8's "121 conditions over 277 instances" still holds after hunk 3.

## Group A — the contradiction between hunks 1 and 4

spec/tarn.md:3231 (untouched by hunk 1, three lines below hunk 1's insertion):

> floor. Neither obligation has a witness in the output alone (§21.7).

spec/tarn.md:3686-3691 (hunk 4's new text):

> §20.5's four obligations on a compacted file's trailer (`[R-WRT-06]`) — its
> fresh `file_id` draw, its generation, the unknown ignore-lane bits it MUST
> carry forward, and the floor its version_minor SHOULD take — are unwitnessed
> for that same reason

§20.5 enumerated: (a) `It MUST mint a fresh file_id … and generation 1`;
(b) `The output trailer MUST copy the input's unknown ignore-lane flag bits
forward`; (c) `the output's version_minor SHOULD be at least the input's`.
Four obligations, so hunk 4's count is right and §20.5's `Neither` is the side
that should move. Neither of the two-hunk auditors can see this: the `Neither`
sentence is unchanged context in hunk 1 and absent from hunk 4.

## Group B — hunk 1's row enumeration against §10.2

§10.2 tabulates eight spaces: record type, channel layout, linearization,
sample type, codec, filter, index encoding, metadata encoding. Hunk 1 lists
seven rows (L31 index encoding, L33 linearization, L34 sample type, L36 channel
layout, L43 codec, L45 filter, R1 metadata encoding) under the quantifier
`one row for each identifier space §10.2 tabulates`. Record type is handled
separately by F36/L25 in the same sentence — but it is one of the eight the
table tabulates, so the quantifier as written demands an eighth row.

Verified `the two of §10.1's four vehicles §21.6 makes conforming`: §10.1 names
exactly four vehicles; §21.6 rows `An ignore-lane flag bit (16–31) is set` and
`A user-metadata document carries an unrecognized tarn.-prefixed key` are the two.
PASSES.
Verified F36/L25 rather than F35/L24: §21.1's specialization rule (`F35 of F36`,
`L24 of L25`) plus §20.5's own bar on carrying an unimplemented MU = 1 type make
the MU-agnostic rows the right ones. PASSES.

## Group B/C — hunk 2's F5

§6.2's mandated order, verbatim:

> A reader MUST validate, in order: the trailer magic; the trailer CRC; the
> version gate (§6.3) … and then, those gates passed, MUST validate all of the
> following …: the flag gates (§6.3); committed_file_length equals the file size …

The 128-byte floor is indeed absent from that order — hunk 2's premise passes.
But its *reason* does not:

> a file shorter than 128 bytes has no trailer to read a magic, a CRC or a
> version from, so the floor is established before any field the gate consults
> exists

A 64-byte file has a final 64 bytes at a 64-aligned offset — a trailer by §6.2's
own definition — carrying magic at 0, version_major at 8 and the CRC at 60. Any
file of 64 bytes or more (up to 127) has bytes at F−64 that F8's and F14's checks
read. The fields the gate consults exist. Only files below 64 bytes lack them.

And F5's Instances cell is `F (physical file size); committed_file_length` — two
instances. The second is a value *read out of the trailer*, i.e. after the magic,
the CRC and the gate. The passage's own convention is to split a row by instance
where only some qualify (`F1's trailer-magic instance`, `F6 with F1's front-block
instance`); F5 was admitted whole.

## Group C — hunk 3's R6

`[R-MTA-04]` (spec/tarn.md:2561-2568) states:

> every key satisfying §4.6's name rules — non-empty, at most 255 bytes, free of
> U+0000 through U+001F

so `[R-MTA-04]` is where the empty-key and control-code-point bar is established
for a document key. R10 (255-byte key) already carried `[R-MTA-04]` (R-ENC-12);
R7, R8, R9 likewise. §21.9 attributes the key length cap to `§18.2's folding of
§4.6's name rules onto keys`, not to `[R-ENC-12]` directly. R6 was the outlier.
Repair CORRECT; no restatement elsewhere carries the old attribution (checked
§19.2, §19.3, Appendix H, §21.9).

## Group C — hunk 3's R8 instance argument

New text: `the two being one instance because a document carrying a bare token is
not well-formed JSON either, so no file exhibits this row's predicate alone
through one (§21.1, R7)`.

§21.1's applicable rules, verbatim:
- `An instance names a field the condition ranges over, a container it can occur
  in, one of several alternatives the condition text states, or any combination
  of the three — a condition applying to two alternatives in two containers has
  four.`
- `One instance is one *distinguishable* file: where a condition is a single
  predicate over several fields — a sum against a bound, a combination of two
  flag bits — the fields it reads are not instances, because no two files could
  differ.`
- `Some rows are strict specializations of others — F1 of F6 and of F8, F35 of
  F36, L24 of L25 — and a file exhibiting a specialization is recorded against
  the narrower row.`

The repair has just put two alternatives into R8's condition text, which by the
first rule yields 2 × 2 = 4. The second rule does not rescue it: a `1e400`
document and a `NaN` document ARE two distinguishable files. The third rule
arbitrates only *specializations*, and R7/R8 nest in neither direction (R8 fires
on `1e400`, which is well-formed JSON; R7 fires on much that carries no number).
So the cited warrant does not carry the claim, and which row records a bare-token
file is left unarbitrated.

## Group D — hunk 4's filter branch

New text (3678-3682):

> A change reaching the filter, or moving a sample's byte offset within the
> decoded image without changing that image's length, has no witness at all —
> both filter values are length-preserving (§17.3), and the content rows test
> only the bytes §14 constrains.

Untouched text 18 lines above, in the same paragraph (3658-3661):

> the ordinal mappings of `[R-GEO-06]` and `[R-SER-01]` are satisfied by a
> structurally valid tile whatever values it carries, except where §14 constrains
> a byte's content — a padding position, a pad bit, or an interleaved boolean —
> and a mis-ordered image is then witnessed by T2, T4 or T5, exactly as a
> mis-strided filter is

T26, verbatim:

> Filter 2 applied at a stride other than the mandated one, where the resulting
> image breaks §14.5's padding content or `[R-SER-08]`'s bool bytes (a wrong
> stride with no such structural constraint is undetectable, §21.7); the check
> that detects it is T2's or T4's

`[R-COD-10]` (§17.3), verbatim:

> A writer that filters with any other stride violates this rule; where the
> resulting decoded image breaks a stated content obligation (§14.5's padding,
> `[R-SER-08]`'s bool bytes) a verifier detects it as a validity error at tile
> scope, and otherwise the consequence is wrong sample content

Changing the declared filter from 1 to 2 (or 2 to 1) over already-stored bytes
produces exactly the state T26 registers: the reader's decoded image is a
permutation of the intended one. Where the tile carries padding positions or
boolean bytes, T2/T4/T5 fire. So the filter branch needs the same hedge the
repair correctly gave the codec branch (`*sometimes* … but neither is assured`).
The repair's own trailing reason — `the content rows test only the bytes §14
constrains` — is what makes it witnessed, not unwitnessed, whenever the
permutation reaches such a byte.

Additional falsifier from this same commit: hunk 1's list registers L43 (codec
value other than 1…4) and L45 (filter value other than 1 or 2). A step-4
declaration change into a reserved or experimental filter value is witnessed at
layer access by L45; hunk 4 says `no witness at all`.

Check-7 comparison of governing verbs, hunk 4:
- repair: `A change reaching the filter … has no witness at all`
- warrant §17.3: `both filter values are length-preserving` — §17.3's own words
  are `1 = none — the filtered image is the decoded image` and `Length is
  unchanged.` Both assigned values, both length-preserving. The analogy PASSES on
  length, and supplies nothing about *content*, which is what the sentence
  concludes about.
- repair: `§20.5's four obligations` vs §20.5's own `Neither obligation` — see
  Group A.
- repair: `unwitnessed for that same reason` vs `[R-LIF-01]`'s reason `it is a
  property of the prior generation, which §9.7 does not reconstruct`. A
  compaction input is a *different file*, not a prior generation of the output
  (the output stands at generation 1 and has no prior generation). The repair's
  own appositive rescues three of the four but mis-names the datum for the
  generation obligation: the missing fact is not the input's generation but that
  the output is a compaction output at all.

## Check 6 — what each repair left unconstrained

- Hunk 4's structure, the compacted trailer (§6.2's eleven fields): magic,
  version_major, dir_offset, dir_length, committed_file_length, reserved and CRC
  are fixed by `[R-CNT-06]`/`[R-CNT-24]`; the incompat lane by F19; the ignore
  lane, file_id, generation and version_minor by the four named obligations.
  No sibling left unpinned. PASSES.
- Hunk 4's structure, §20.3 step 4's bar. The bar names five things: `the set of
  padding positions (§11.3) and the content [R-SER-05] fixes there, the decoded
  size, the byte offset of any sample within the decoded tile image, or the codec
  and filter that produced the stored bytes`. The repair's five branches map onto
  all five. Enumeration COMPLETE.
- Hunk 2's structure, §21.2's 36 rows: the four `[R-CNT-24]` rows plus F5 are the
  only candidates; F11, F12, F13, F15, F16, F17 all read trailer bytes a future
  major MAY redefine, so they cannot reach. No missing sibling. PASSES on
  membership; fails on F5's instance split (above).
- Hunk 1's structure, §10.2's spaces: seven listed against eight tabulated. The
  verb `tabulates` correctly excludes the trailer flag lanes, which §10.2 names
  in prose only.

## Counts checked
36 (F1–F36) ✓ · 49 (L1–L49) ✓ · 26 (T1–T26) ✓ · 10 (R1–R10) ✓ · 121 total ✓ ·
277 instances ✓ · §10.1 four vehicles ✓ · §17.3 two filter values ✓ ·
§20.5 four trailer obligations ✓ · §10.2 eight spaces vs seven rows ✗
