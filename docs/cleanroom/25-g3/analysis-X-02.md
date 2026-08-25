# Refute pass on X-02 downgrade

## What I read
- /private/tmp/.../r26audit-b/case/case-X-02.md
- /private/tmp/.../r26audit-b/hunk-01.diff, hunk-02.diff
- spec/tarn.md: lines 100-115 (R-CNF-01), 165-200 (R-CNF-03/04/05), 596-616 (§9 figure Rationale),
  1030-1050 (R-CNT-17, R-CNT-16), 1475-1502 (§11.1 shrink Rationale = hunk 01 region),
  2950-3096 (§20.3 steps 1-6 = [R-WRT-04]), 3100-3145 (three-shapes Example),
  3146-3160 (§20.4 / R-WRT-05), 3275-3312 (R-WRT-07 + compaction Example),
  3915-3960 (§23.1 = hunk 02 region).

## Greps run (exact)
- grep -n "R-WRT-05\|R-WRT-07\|R-WRT-04\|R-CNT-21" spec/tarn.md  -> 604,608,611,657,680,1357,1500,1790,2601,2975,2995,2996,3057,3067,3077,3156,3174,3213,3288,3307,3333,3610,3863,3878,3936,3984,4453
- grep -n -i "shrink" spec/tarn.md -> 1487,1493,3036,3037,3046,3051,3056,3932,3939,3942,3948  (ONLY hits; no §21 row mentions shrink)
- grep -n "21.7" spec/tarn.md -> 2385,2477,3053,3249,3352,3366,3560,3650

## Findings

### Fact 1 — [R-WRT-04] is the whole of steps 1-6.
Line 3077 closes step 6 with `[R-WRT-04]`. So BOTH the operative trigger (line ~2981-2996)
and the disputed consequence sentence (3056-3059) sit inside one normative requirement.
The verifier's point (3) framing ("operative rule beats gloss") is therefore weaker than
it stated: there is no rank difference between the two sentences. I had to decide the
case on the sentences' own content, not on their status.

### Fact 2 — the padding-only shrink was licensed in untouched normative text.
Line 3049-3053, untouched by either hunk: "What counts as such an alteration is the bar
above and nothing else, its carve-out included — a new padding position whose stored byte
already holds the fill `[R-SER-05]` fixes is not one, so a shrink producing only those is
permitted here exactly as it is there, and this sentence answers the rescue question
rather than restating the test."
Also, hunk 01's '-' side already read "a new padding position whose stored byte already
holds the fill is the other."
=> The finding's causal claim ("only becomes false once the repairs establish that a
shrink need not de-address anything") is false. Neither repair introduced the case, so
this is not an unswept restatement of a repair. Verifier point (1) is confirmed as text.

### Fact 3 — the consequence sentence's re-emission clause is chained off a premise that
does not exist in the worked case.
Line 3056-3059 verbatim: "Where a shrink is permitted the de-addressed tiles' extents
become slack (`[R-CNT-21]`), `[R-CNT-17]` obliges the smaller entry_count and so a
re-emitted index region, and every surviving stored tile is untouched."
Three coordinated CONSEQUENCE clauses; the outer two are plainly reports ("become slack",
"is untouched"). The only obligation word is attributed to [R-CNT-17], whose own text
(1038-1042) is "extent_length MUST equal entry_count x 20 + ceil(entry_count/2^16) x 4 ...;
a mismatch, or an entry_count that does not equal the geometry-derived addressed-tile
count, is a validity error at layer scope." In the worked case (T0=4, E0 8->5, G0 = 2 both
sides) entry_count = 2 IS the geometry-derived count and extent_length = 44 IS the
formula. There is no "smaller entry_count", so the "and so" has no premise and the
sentence yields no instruction. Reading it as an obligation requires ignoring the noun
phrase the obligation is stated over.

### Fact 4 — the case is decided exactly, in the same requirement.
Trigger (2981-2984): "Every layer whose stored-tile set or index content this commit
changes has its tile-index region re-emitted in full". Neither changes: stored bytes do
not move or change, §15.1 entries are offset/length/crc-of-stored-bytes, so no entry byte
and no segment CRC changes, and G0 unchanged means [R-GEO-06] moves no disk ordinal.
Complement (2994-2996): "A layer whose record alone changes keeps its extent slot,
pointing at the existing region, as does a layer the commit leaves untouched
(`[R-WRT-05]`); relocating a live index region is compaction's operation (§20.5,
`[R-WRT-07]`), not an appender's."

### Constructions I built and what each showed

C1 (the finding's). Rank-1 interleaved, one u8 channel, T0=4, E0 8->5, G0=2 both sides,
entry_count 2, extent_length 44, tile 1's bytes at 5,6,7 already hold fill. Verified
constructible. Writer B = directory+pad+trailer only. Writer A = +44-byte index region at
new placement, old region slack. Both files conforming (no §21 row fires; [R-CNT-21] makes
slack unconstrained). Fork, if real, would be byte-level under the charter's test. But
Fact 3 shows the disputed sentence never reaches Writer A: its own chain breaks.

C2. Writer C takes "obliges the smaller entry_count" literally and emits entry_count = 1.
Then entry_count != geometry-derived addressed-tile count -> [R-CNT-17] validity error at
layer scope -> nonconforming file -> [R-CNF-05] bars it under BOTH readings. Not
byte-level by the charter's own discriminator.

C3. Shrink that de-addresses tiles (E0 8->4, G0 2->1). entry_count falls, index content
changes, trigger fires, consequence sentence agrees. No fork.

C4. Shrink de-addressing a tile that was UNSTORED (sentinel entry). "the de-addressed
tiles' extents become slack" is then false (no extent), but entry_count still falls and
re-emission still fires. Inaccuracy without a byte fork.

C5. Hunted for a shrink that changes index content WITHOUT changing entry_count, which
would put trigger and consequence sentence in genuine conflict. Index entries are
offset/length/crc over stored bytes; a padding-only shrink touches none of them, and any
shrink that DID alter a prior-generation stored tile's §14 obligations is barred outright
by the bar at 3005-3020. No such shape exists.

C6. Actor sweep. Reader/verifier: both files satisfy every checkable rule, so no
accept/reject fork. Updater ([R-CNF-06]): [R-WRT-05] compels byte-identical re-emission
only for records "it retains and does not logically modify"; the layer record IS modified
here (E0 8->5), so [R-WRT-05] neither forces nor forbids moving the extent slot — step 4's
complement is what decides, and it decides for B. Compactor: [R-WRT-07] relocates by
design, but that writes a new file under a fresh file_id, not a generation, so it is not
in the emittable set for this commit. No actor reaches Writer A by a licensed route.

C7. §21 route. grep -i shrink returns no §21 row. §21.7 (3053) "records the consequence"
only that the bar is unwitnessed. §21.1's prose-vs-row precedence is therefore irrelevant;
there is no row to disagree with.

C8. Corroboration for the conditional reading elsewhere. §9's figure Rationale (611):
"A commit never relocates a live index region otherwise; that is compaction's operation".
§11.1 Rationale (1500-1503, untouched by hunk 01): "Growth that leaves every grid count
unchanged touches the directory alone; growth that raises one changes entry_count and with
it extent_length (`[R-CNT-17]`), so the layer's whole tile-index region is re-emitted".
Both non-normative, but both track the conditional rule and neither supports the universal
reading. That is the exact symmetric statement for growth of the rule the finding wants
added for shrink.

## Where the verifier was wrong, and why it does not save the finding
The verifier's stated byte-level reason is bad. It leans on [R-CNF-05] ("two conforming
writers given identical input MAY produce different conforming files") and [R-CNF-02]
("conduct rules bind the actor, the predicate binds the bytes") to say a permission fork is
never a bytes fork. That reasoning, if accepted generally, would make every appender-conduct
ambiguity non-byte-level, which is precisely the framing this pass exists to distrust: the
charter's discriminator says a conforming disputed file that only one reading lets an actor
produce DOES move the emittable set. I reject that limb.
The downgrade survives on its other limb only: the disputed sentence does not admit the
universal reading in the first place, because its re-emission clause is derived "and so"
from "the smaller entry_count", which [R-CNT-17]'s own quantifier denies in this case, and
because the same requirement states the record-only outcome exactly, three sentences
earlier.

## Verdict
DOWNGRADE_STANDS. Byte-level NO. Real-as-text: only as editorial imprecision in a sentence
neither hunk touched, whose antecedent "Where a shrink is permitted" is broader than the
three consequences it reports. Worth the polish the finding proposes; not a defect in the
repairs and not a byte fork.
