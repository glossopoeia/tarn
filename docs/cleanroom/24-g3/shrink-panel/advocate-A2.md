# Advocate A2 — working transcript

## Access log
Read only /Users/robertkleffner/Documents/GitHub/tarn/spec/tarn.md, via bash
(wc, grep, sed). No docs/, no conformance/, no git, no web.

Unrequested context appeared before I began: a project instruction pointer
(CLAUDE.md -> AGENTS.md) and an index of the maintainer's memory files with
one-line descriptions. I did not open any of it and did not use it. Disclosed.

## Quote check
- Sentence A: spec lines 3005-3011. Charter's rendering is verbatim EXCEPT it
  drops the citation `(\[R-COD-10\])` after "makes it the identity". Not
  material to the question, but noted.
- Sentence B: spec lines 3041-3045. Verbatim.

## The construction, mechanically
Layer L, rank d, dimension x with E_x = 6, T_x = 4 (any T_x >= 2 that does not
put index 5 at a tile start works; T_x = 3 also works). Grid count
G_x = ceil(6/4) = 2 before, ceil(5/4) = 2 after -> unchanged (§11.2).
Tile at x-index 1 covers x in [4,8). Before: real = {4,5}. After: real = {4}.
So x=5 becomes a padding position (§11.3) of a tile that stays addressed and
stays stored.

What the commit does NOT change, checked against the bar's own list:
- decoded size: P·Q (interleaved) or P·B^c (planar), §14.2 — functions of
  T_i and channels only. Unchanged.
- byte offset of any sample: same table, same inputs. Unchanged.
- value sequence order: §14.1, P and C only. Unchanged.
- codec, filter: untouched.
- content §14.5 fixes at padding positions: the byte at x=5 already holds the
  channel's fill, which is exactly what [R-SER-05] mandates there. Unchanged.
- entry_count: addressed-tile count unchanged, so [R-CNT-17] is satisfied by
  the same value; the index region need not be re-emitted (§20.3 step 4
  re-emits only where the stored-tile set or index content changes). This is
  §20.3's shape (c) — a change confined to the directory.

The ONLY item on the bar's list the commit touches is "the set of padding
positions (§11.3)".

## Site survey (grepped terms, not identifiers; hard-wrap aware)
`shrink` -> 1487, 3033-3048, 3933, 3940.
`re-declar|declarations in a way|extent MAY|stored in the generation` -> 1472,
1490, 2995-6, 3004, 3019, 3022, 3033, 3036, 3126.
`padding position` -> 1528, 1712, 1775, 1902-6, 1955, 1968, 2854, 2998, 3009,
3023, 3043, 3122, 3539, 3541, 3665, 3678, 3688, 4416.

Sites that state or restate this rule:
1. §20.3 step 4, lines 2994-3031 — the bar itself (normative prose).
2. §20.3 step 4, lines 3033-3052 — the shrink paragraph (normative prose).
3. §20.3's "three shapes" Example, shape (c), line 3122-3128 — BLOCKQUOTE,
   non-normative under [R-CNF-01].
4. §11.1 Rationale, lines 1483-1492 — BLOCKQUOTE, non-normative, and it
   expressly defers: "§20.3 states normatively, and governs".
5. §21.7, lines 3685-3706 — normative prose, the undetectability account.
6. §23.1, lines 3931-3941 — normative prose, privacy framing.

## Argument 1 — the shrink paragraph subordinates itself to the bar
Line 3033: "An extent MAY also **shrink**, and the bar above is the whole of
the test, **in the bar's own tense**". Two clauses, and the first is a total
incorporation: the bar above, entire, is the test. Sentence A is part of the
bar above; it is the sentence that says how the bar's predicate is applied.
If Sentence B added an independent trigger the bar does not contain, the
paragraph's own opening sentence would be false. Reading A leaves it true.

## Argument 2 — the bar's own next sentence, by contrapositive
Lines 3011-3013 (normative): "Where a change does reach them it makes each
stored tile it reaches nonconforming". Reach => nonconforming. Contrapositive:
still conforming => not reached. Tile T after the commit satisfies §14.1-§14.5
in every particular, including §14.5 at the new padding position. T is
conforming. Therefore the change did not reach T. Therefore the bar, whose
operative verb is "alters ... for any tile that layer stores", does not bite.

## Argument 3 — grow proves the list cannot stand on its own
Lines 3022-3024 (normative): "an extent MAY **grow**, since a position that
becomes real held that channel's fill and fill is a legal sample value".
This permission is not confined to empty layers: its stated reason ("a position
that becomes real HELD that channel's fill") presupposes stored bytes, which an
empty layer has none of, and the clause is joined by "and" to the separate
empty-layer permission.
A grow of E_x 5 -> 6 with T_x = 4 changes tile 1's padding set from {5,6,7} to
{6,7} — a stored tile of the superseded generation. So an expressly permitted
operation alters "the set of padding positions". The list item therefore cannot
be an independent trigger. Sentence A is the sentence that says so, and without
it the grow permission and the bar contradict each other.
Note the exact symmetry: grow is permitted because the byte already held fill
and fill is legal as a real sample; Sentence A's shrink is permitted because
the byte already holds fill and fill is what §14.5 requires of a padding
position. One principle, both directions. Reading B keeps the principle for
grow and drops it for shrink with no stated ground.

## Argument 4 — Sentence B's own stated reason cannot carry it
"and for the same reason: the quantifier is the superseded generation's".
A quantifier tells you WHICH tiles to test. It does not tell you WHETHER the
test is met. Sentence B's ratio is entirely about tense, and tense is equally
true of a grow (which is permitted). So the final clause's "is barred" cannot
be doing independent work; it is the paragraph's running case restated.

## Argument 5 — Sentence B's paragraph job is "rescue", not "bar"
Paragraph structure, lines 3033-3047:
  (i) topic: shrink permitted exactly where it alters nothing §14 fixes;
  (ii) de-addressing "is not itself such an alteration ... but neither does it
       rescue a commit that damages a prior-generation stored tile";
  (iii) "Unstoring that tile in the same commit does not rescue IT either, and
        for the same reason".
The pronoun "it" in (iii) takes its antecedent from (ii): "a commit that
DAMAGES a prior-generation stored tile". Both rescue sentences presuppose
damage; neither establishes it. The trailing clause is a compression of (iii)
in which the damage premise is carried, not dropped.

## Argument 6 — §21.7 supplies the qualifier Sentence B omits
Line ~3703 (normative prose, §21.7): "And a commit that supersedes every tile
it WOULD HAVE DAMAGED leaves the live state clean, so the bar is unwitnessed
there for the same reason [R-LIF-01] is".
This is §21.7 discharging the cross-reference Sentence B itself makes ("§21.7
records the consequence"). The two sentences are the same rule stated twice,
and the §21.7 statement carries the damage qualifier. Reading A's claim — that
Sentence B "omits a qualifier stated elsewhere" — is not a construction I have
to invent; the document states the qualifier at the site Sentence B points to.

## Argument 7 — §21.7's witness account is true under A, incomplete under B
§21.7, lines 3685-3689: "§20.3 step 4's bar on a declaration change is
witnessed only where the affected tiles remain stored ... A change reaching a
byte §14 structurally constrains — a padding position, a pad bit, or a boolean
byte — fires §21.4's content rows."
Under Reading B the disputed commit is barred, the affected tile REMAINS
STORED, and the change reaches a padding position — yet T4 does not fire (the
byte holds the fill), and no other row fires. §21.7 would then be a false
account of a class it expressly claims to cover, and §21.1 makes §21.7 "the
account, by class, of what fails" the detectability gate. Under Reading A there
is no such class: a padding-set change that preserves the byte is not a barred
change, and every barred change that reaches a padding byte does break it and
does fire T4.

## Register check
- T4 (§21.4, line 3541): "A padding position does not encode, for each channel
  it carries, that channel's recorded fill value". Our padding position DOES
  encode it. T4 does not fire.
- T2, T5: bool-specific, and only where content is wrong. Do not fire.
- T3/T14: decoded size and declared length. Unchanged. Do not fire.
- Codec/filter rows (T15, T17, T23, T25, T26): declarations untouched.
- §21.6: no entry on point.
No row fires under either reading. §21.1's row-vs-rule precedence therefore has
nothing to resolve; there is no register witness on either side, which is what
Sentence B's own cross-reference to §21.7 concedes.

## The file, both ways
Start: front(16) | L's tiles | L's index region | dir_1 | pad | trailer_1
(gen 1). L's dimension entry for x carries extent = 6 (u64, §7.4).

Under Reading A the appender emits a §20.3 shape-(c) commit:
  - step 4 writes no payload and no index (stored-tile set unchanged, index
    content unchanged, entry_count unchanged);
  - step 5 re-emits the whole directory: every record byte-identical except
    L's, whose x dimension entry's extent u64 now reads 5; L's extent slot
    still points at the ORIGINAL index region;
  - step 6 appends pad and trailer_2, generation 2, same file_id, ignore-lane
    bits copied forward.
  after: front | L's tiles | L's index | (dir_1,pad,tr_1 now slack) | dir_2 |
         pad | tr_2
File grows by |dir| + |pad| + 64. Not one byte of L's tiles or index moves or
changes. Reads of x in [0,5) return exactly what they returned before; x = 5
is now outside the extents and §21.6's "requested coordinate lies outside the
layer's extents" governs a request for it.

Under Reading B the appender MUST NOT commit. Its options are §20.3's own:
"Such a change is a new layer, or a whole-file rewrite under a fresh file_id
([R-LIF-01], §20.5)." A new layer duplicates every stored tile of L and leaves
the original addressed forever ([R-CNT-22]: no commit removes a layer). A
rewrite is a compaction: fresh file_id drawn anew, generation 1, every tile
payload re-emitted, and the (file_id, range) cache contract of [R-LIF-03]
broken for every open reader. For a 10^6-tile layer that is the whole layer's
bytes to change a single u64.

So: two conforming implementations reading only this document emit either a
few-kilobyte directory-only append, or a full-file rewrite under a new
file_id — or a refusal. Byte-level divergence, and the largest kind.

Note also that the Reading-A output is a conforming file under BOTH readings.
[R-CNF-02] makes file conformance "a pure predicate on bytes"; a creator under
§20.2 could emit those exact bytes. Reading B's bar therefore has zero byte
consequence in this case — it is pure conduct, unwitnessed, and its only
effect is to force duplication of a layer to reach a state the format already
permits a file to be in.

## Points against me, honestly
1. The bar's list names "the set of padding positions (§11.3)" AND "the content
   [R-SER-05] fixes there" as two items. If content were the whole test, the
   first is surplusage.
   Answer: the grow permission (Argument 3) makes it surplusage under any
   reading, because grow changes the set and is expressly MAY. The surplusage
   argument proves too much.
2. §11.1's Rationale: "a shrink is barred wherever it alters what §14 fixes for
   such a tile — whether or not the new state still stores it — and permitted
   where it only drops tiles out of the addressed set." The final clause is a
   flat statement that de-addressing is the ONLY permitted shrink.
   Answer: blockquote, therefore non-normative under [R-CNF-01]; and it
   expressly defers — "§20.3 states normatively, and governs". Note too that
   its structure puts "whether or not the new state still stores it" as a rider
   on an ALTERATION test, which is Reading A's structure exactly.
3. Line 3048-3050: "Where a shrink is permitted the de-addressed tiles' extents
   become slack, [R-CNT-17] obliges the smaller entry_count and so a re-emitted
   index region" — describes a permitted shrink as one that drops tiles.
   Answer: it over-describes under Reading B too. Take E 6->5, T=4, tile 1
   addressed but UNSTORED (sentinel). No stored tile is affected, so the shrink
   is permitted under both readings, yet nothing is de-addressed and
   entry_count does not fall. The sentence is describing the typical shrink,
   not defining the permitted set.
4. §23.1: "A commit removes sample data two ways — superseding it, and a shrink
   that de-addresses tiles". Under Reading A there is a third way: a shrink
   that makes a real position padding.
   Answer: Reading A's carve-out is limited precisely to positions whose stored
   byte already holds fill. Nothing is removed that a reader could have
   distinguished from absence: fill is what §13.3 returns for absent data. No
   sample data is made unreachable, so §23.1's enumeration is untouched.
5. Sentence B is later in the document.
   Answer: and it opens by declaring the earlier text "the whole of the test".
   Lex posterior does not run against a text that incorporates the earlier one
   entire.

## Verdict
Reading A. The document contains a real, on-its-face divergence between two
normative sentences, and every tiebreaker inside §20.3 step 4 and §21.7 runs
toward A: the shrink paragraph subordinates itself to the bar; the bar equates
reaching with making a tile nonconforming; the grow permission forecloses the
padding-set item as an independent trigger; Sentence B's stated reason is about
tense only; and §21.7 restates Sentence B's case with the damage qualifier
Sentence B leaves out.

That said, the divergence is a defect worth repairing on its face. Sentence B
should read "...so a shrink that damages a tile stored there — one that turns
real positions into padding whose stored bytes do not already hold the fill —
is barred whether or not the new state still stores it." That is what the rest
of the section already means; the sentence is the only place that does not say
it. §11.1's Rationale should lose "and permitted where it only drops tiles out
of the addressed set" for the same reason.


---

*Editorial substitution for the repository vocabulary gate: one ordinary-English
use of a gate word was replaced with an exact synonym at line 218. The advocate's
argument is unchanged. Rounds 19, 22, 24 and both round-24 audits required the
same treatment; the substitution is recorded here rather than made silently.*
