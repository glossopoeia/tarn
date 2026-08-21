# Round 18 — cross-hunk consistency audit (working transcript)

## Access disclosure

Read: all ten `hunk-NN.diff` (01–10) in the audit dir; `spec/tarn.md` only.
Did NOT read: `full.diff`, `docs/`, `PLAN.md`, `OPEN-QUESTIONS.md`, `AGENTS.md`,
`README.md`, `conformance/`, `spec/registry.json`, git history, the web. Did not
list the audit directory (globbed `hunk-*.diff` for a count/size check only).

Spec passages read in full (line ranges): 155–230 (§2.3 conformance classes,
[R-CNF-03]/[R-CNF-04]/[R-CNF-05]/[R-CNF-06]/[R-CNF-11]), 596–662 (§5.1 note, §5.2),
735–784 headings, 900–960 (§7.2), 1220–1240 (§9.3), 1315–1366 (§9.7), 1466–1510
(§11.1–11.2), 1885–1930 (§14.3, §14.4 head), 1950–1982 (§14.5), 2009–2107
(§15.2–15.4), 2440–2564 (§18.2), 2849–3258 (§20 whole), 3258–3336 (§21.1),
3449–3565 (§21.4–21.6), 3567–3654 (§21.7–21.9), 3804–3853 (§23), 4128–4255
(Appendix G), 4256–4327 (Appendix H).

Computation run: python over `spec/tarn.md` only — a whitespace-normalising
scan that strips `>` prefixes and collapses newlines so hard-wrapped phrases
match, then regex search with line attribution. Plus line-oriented `grep -n`
for requirement IDs and single tokens that cannot wrap.

## Searches run (normalised, wrap-safe) and their output

```
're-declared freely'   -> line~1488 (§11.1 Rationale, HUNK 1)
                          line~2976 (§20.3 step 4, NORMATIVE)
                          line~3083 (§20.3 Example (c), HUNK 2)
'storing no tile'      -> line~3083 only
'stored nothing'       -> line~1488 only
'pad bit'              -> 1893,1900,1902,1904,1910,1911 (§14.3)
                          1957 (§14.5, [R-SER-05] "Every pad bit (§14.3) MUST carry ...")
                          3079 (§20.3 Example (c)), 3460 (T5),
                          3577 (§21.7), 3590 (§21.7), 3599 (§21.7, HUNK 6 context)
                          4284 (App. H writer: "pad bits ([R-SER-05], §14.5)")
                          4316 (App. H verifier: "pad bits ... (§14.5, §14.3, §14.2)", HUNK 10)
'capability refusal'   -> 3648 only (HUNK 7)
'lists the ignore-record' -> 3500 ("§21.6 lists the ignore-record conditions that
                          are not violations.") — UNTOUCHED, same paragraph as HUNK 5
'narrowest scope'      -> 3645 ("a layer or a tile") — HUNK 7's own sentence
'MUST NOT drop the record' -> 2922 (§20.3 step 2) — UNTOUCHED
'relies structurally'  -> 3247 ("it relies structurally on every structure it copies")
'either.{0,20}so a commit whose only' -> 3123 (HUNK 3's own cell)
grep 'drop'            -> 1487,2922,2993,3012,3110,3112,3123,3144,3153,3162,3164,3166,3527
grep 'supersed'        -> 61,315,602,632,657,1198,1484,2862,2941,2953,2960,2976,2993,
                          2999,3015,3036,3042,3063,3064,3074,3123,3255,3530,3604,
                          3808,3810,3814
grep 'regenerat|relocat|latent|structural ground' -> 241,610,938,2871,2872,2925,2926,
                          2949,3136,3156,3157,3173,3182,3186,3187,3191,3193,3195,
                          3201,3207,3225,3226,3229,3250,3439,1326,1356,3190
grep 'file_id'         -> 750,776 (§6.2 "file_id ≠ 0") confirms HUNK 8's citation
grep 'R-MTA-09'        -> 2464–2478 (§18.2), 3493 (HUNK 5), 3508 (R4), 203 (§2.3)
grep 'R-CNF-03'        -> 172 and 160–171 (§2.3): "§21.9's [R-ERR-04] governs a
                          refusal on that last ground; §21.6's closing paragraph
                          names the other two" — confirms HUNK 7's count of two
```

## The grouping (by rule, not by section)

**Group A — the generation a re-declaration/shrink is measured over.**
Hunks 1, 2, 6. Governing normative text: §20.3 step 4, lines 2951–3020, esp.
2951–2959 (the bar, "in the generation this commit supersedes"), 2975–2979
(empty-layer permission, "the tense is the bar's"), 2990–3004 (shrink).
Hunks 1 and 2 are both `>` blocks; hunk 6 (§21.7) is normative prose.

**Group B — when a record may be dropped / what counts as changing its scope.**
Hunk 3 (§20.4 table). Untouched neighbours that state the same rule:
§20.3 step 2 line 2922, §20.5 lines 3153/3162–3166, §2 line 241, §23.1 line 3809,
Appendix H line 4292–4300.

**Group C — what a compactor answers for in bytes it regenerates.**
Hunk 4, and by shared rule §20.3 step 2 (2917–2929, the appender's identical
situation), §20.5 opening (3151–3166) and §20.5 closing (3246–3252). Hunk 9
touches the same "a tile-index region is itself a record extent" fact.

**Group D — file's fault vs actor's capability.**
Hunks 5, 7, 10. Governing: [R-CNF-11] §2.3 (189–224), [R-MTA-09] §18.2
(2454–2489), [R-MTA-10] §18.2 (2537–2557), §21.6 (3516–3565), §21.9 (3644–3654).

**Ungrouped / profile-local.** Hunk 8 (Appendix G file_id substitution),
hunk 9 (Appendix G emission order).

## Group-by-group verdicts

### Group A

Normative rule, quoted (2975–2979):
> "A layer that stores no tile **in the generation this commit supersedes** MAY
> be re-declared freely, which is what schema-first creation needs (§11.1) — the
> tense is the bar's, so a commit does not earn this permission by emptying the
> layer as it re-declares it"

Hunk 1 (1488): "A layer that **stored nothing** may be re-declared **freely**."
— tensed to the superseded generation ✓, unqualified.

Hunk 2 (3083): "A layer **storing no tile** is re-declared **freely, subject to
every rule its new geometry is subject to**, which is the same step's permission."
— untensed ✗, qualified.

Same commit, same rule, two restatements, disagreeing on both axes. → finding X-06.
Note the "every rule its new geometry is subject to" clause is step 4's proviso on
**growth** (2986–2988), not on the empty-layer re-declaration, which step 4 states
as a bare "freely". Attributing the qualified form to "the same step's permission"
is a small overreach; it is nonetheless substantively right (a nonconforming
geometry is barred by [R-CNF-05] anyway), so the direction is to sweep hunk 1, not
to undo hunk 2.

Hunk 1's shrink clause vs 2990–3004: "barred wherever it alters what §14 fixes for
such a tile — whether or not the new state still stores it" matches 3000–3002 ✓.
"permitted where it **only** drops tiles out of the addressed set" — the new "only"
is what makes it match 2992–2997; without it the round-16 sentence was wrong. ✓

Hunk 6 vs 2960–2962/2998–3004: "a commit that supersedes every tile it would have
damaged leaves the live state clean" — matches; §20.3 line 3002 forward-cites §21.7
for exactly this. ✓ Hunks 1 and 6 agree. Hunk 2 is the odd one out.

Hunk 6's new gloss on T3/T14 checked against the rows: T14 (3469) "a non-sentinel
index entry's length differs from the tile's decoded size" = the entry's declared
length ✓; T3 (3458) "The decoded payload's byte length is not exactly the tile's
decoded size" = the decoded payload's own ✓. Round 16's "read the index entry
rather than the decoded image" was wrong for T3; the repair fixes it. But the
sentence it now underwrites says a change reaching **the codec** is witnessed by
T3 or T14 — falsified by a codec 1→3 change on raw tiles, which is witnessed by
T17, and by 2→4, witnessed by T23/T25; none is a length test. → finding X-08.

### Group B

Hunk 3 reverses round 16. Old: "Superseding a stored tile's bytes **is not** such a
change for either kind ... so a commit whose only change is a supersede MUST retain
the record." New: "Superseding a stored tile's bytes re-places that layer's index
region (§20.3, [R-WRT-04]) and so modifies that layer's record, which **is** such a
change: an appender superseding a tile MAY drop the record."

Citation check: §20.3 step 4 lines 2937–2940 confirm the whole index region is
re-emitted "necessarily at a new placement"; line 2947–2949 confirm the layer
record's extent slot is what addresses the region; §20.5 line 3200–3201 confirms
crc_of_crc_array is a layer-record field over the region. So "modifies that layer's
record" resolves ✓. "an appender never removes one (§20.4)" resolves to §20.4's own
line 3125 ("No commit therefore removes a layer record") ✓ — a self-citation two
lines below the table, but accurate.

Sweep check. §20.3 step 2, line 2920–2923 (untouched):
> "Against any other structure the appender carries forward, it MUST NOT repair the
> defect — `[R-LIF-01]` freezes the committed prefix — and **MUST NOT drop the
> record (§20.4)**."
That flat MUST NOT, cited to §20.4, now collides with §20.4's widened MAY in
precisely the commit shape the surrounding sentences describe (an appender
re-emitting an index region it met a malformed entry in). → finding X-03.

Residue check inside the cell: the next sentence still reads "Dropping the record,
or dropping another record in the same commit, is not itself such a change
**either**". "either" was an anaphor to the deleted "is not such a change"
sentence; with that sentence reversed, "either" points at a clause of the opposite
polarity. → finding X-07.

§23.1 line 3808–3810 ("a commit that supersedes data — the only removal a commit
performs") is an exhaustive claim that a record drop already falsified before this
commit; hunk 3 makes supersede-plus-drop the ordinary case. Noted, not raised as a
separate finding — pre-existing and non-byte-level.

Hunks 3 and 4 agree in direction (both widen "what the commit modifies"). Checked
and passed.

### Group C

Hunk 4's rule: a compactor meeting an index entry §15.3 classifies reject-tile on a
structural ground MUST refuse; it may neither reproduce the entry nor invent a
replacement.

Three collisions:

1. Same passage, three paragraphs up (3159–3162, untouched):
   "A compactor MUST refuse to compact when any check `[R-WRT-09]` obliges fails,
   and MUST NOT emit a file carrying a violation **it has detected**."
   Hunk 4 states the obligation unconditionally, then ends conditionally: "a
   compactor **need not have looked**; where it has, this is the disposal."
   → finding X-01.

2. The deleted clause was the only guidance for the case hunk 4 still admits (a
   compactor that has not looked). Round 16: "reproduced with its offset and length
   exactly as they stand, there being no live extent for a re-pointing to target —
   `[R-IDX-03]` gives such an entry no stored extent and no claimant in the coverage
   walk". §9.7 lines 1325–1328 and §15.3 lines 2035–2041 confirm that fact is true
   and is stated nowhere else in a form that tells a compactor what bytes to write.
   Hunk 4 now forbids both available actions. → finding X-01.

3. The discriminator. Hunk 4: "`[R-WRT-01]`'s licence for a latent violation to
   travel reaches only a structure the commit neither modifies nor relies on, which
   a regenerated region is not." Against §20.3 step 2 (2923–2929, untouched):
   "Reproducing a structure's bytes unchanged is not authoring them ... a violation
   latent in a structure it neither modifies nor relies on travels with that
   structure (§20.1, `[R-WRT-01]`) — which is as true of **an index entry copied to
   its disk-ordinal position** as of a record re-emitted byte-identically" — i.e.
   §20.3 applies the licence at *entry* granularity inside a wholly re-emitted
   region. And against §20.5's own closing paragraph (3246–3248, untouched): "it
   **relies structurally on every structure it copies**", which if read into
   [R-WRT-01]'s "rely on" empties the licence for a compactor entirely and
   contradicts §20.5's opening (3156–3157). → finding X-02.

[R-WRT-06] citation check: the tag at 3182 closes a block whose refusal triggers
are (i) a [R-WRT-09] check failing, (ii) a violation **detected**, (iii) the §20.4
table not licensing a drop, (iv) an unimplemented MU = 1 type. A structural
reject-tile entry is (i) by hunk 4's own concession *not* a [R-WRT-09] check, is
not a record-drop question, and is (ii) only once detected. So [R-WRT-06] almost
says the claimed thing. Recorded in X-01.

§20.1 citation check: §20.1 (2867–2874) says a compactor "satisfies every writer
requirement for the bytes they produce" — and in the same breath carves out "a
violation latent in a structure they neither modify nor rely on". So §20.1 does not
make a compactor "answer for those **in full**" without qualification; the "in
full" is hunk 4's gloss, and the qualification it omits is the very clause the next
sentence deploys. Recorded in X-02.

### Group D

Hunk 5's substance is well grounded: §2.3 [R-CNF-11] (lines 200–206) already names
"when it declines to decode a user-metadata document (`[R-MTA-09]`)" as a
cannot-establish ground and, in the same list, says the unassigned-encoding case
"is not such a ground". §18.2 [R-MTA-09] (2461–2478) supplies both halves. Both
citations in hunk 5 resolve. ✓

The failure is the pointer three sentences later, untouched, in the same §21.5
preamble (3500): "§21.6 lists the ignore-record conditions that are not
violations." §21.6's table (3521–3536) and its two closing blocks (3538–3565) list
neither the size-bound decline nor anything like it. → finding X-04.

Hunk 7's count: §2.3 line 164 (untouched) independently says "§21.6's closing
paragraph names the other **two**". Count ✓. But §2.3 phrases the second as "a
record carries MUST_UNDERSTAND = 1 with a type it does not implement — **in a
conforming file such a type is necessarily from the experimental range, since a
reserved-range type carrying MU = 1 is itself a violation**". §21.6 itself (3552–
3554) states it as "an **experimental-range** record type carrying MU = 1". Hunk 7
drops the qualifier and writes the bare "an unimplemented MU = 1 type", which
sweeps in the reserved-range case §21.6's own closing sentence (3562–3565) puts on
the violation side. → finding X-05.

Hunk 7's "a layer or a tile": checked against [R-CNF-11] line 199–201 ("when it
declines a **layer's or a tile's** decode on resource grounds") and §18.2's Note
(2485–2489: a document "having no declared size and so no narrower scope whose
declarations that rule can measure" — the decline is at the whole file). The
enumeration is deliberate and correct, and does **not** conflict with hunk 5.
Checked and passed — this was my leading hypothesis and it is wrong.

Hunk 10: adding pad bits to the verifier's decoded-content obligations is right —
T5 (3460) is a verifier row for pad bits and round 16's checklist omitted it. The
citation is wrong. §14.3 (1893–1894) defines pad bits and expressly delegates:
"their content is fixed by `[R-SER-05]`", and its Note (1904) "§14.5 gives both
their content". §14.5 [R-SER-05] (1957) carries the obligation: "Every pad bit
(§14.3) MUST carry the plane's channel's fill bit." Two untouched restatements
cite §14.5 for pad bits — Appendix H's own writer entry 32 lines above (4284) and
§21.7 (3575–3577). → finding X-09.

### Hunks 8 and 9

Hunk 8: "(§6.2 forbids `file_id` = 0)" resolves — §6.2 spans 735–784 and states
`file_id ≠ 0` at lines 750 and 776. ✓ Fixing the substitute at
0x0000000000000001 removes round 16's under-determination ("Any other fixed nonzero
value" pinned nothing, which defeats a reproducibility profile). No collision with
§9.3's randomness advice: the case has probability 2⁻⁶⁴ and the following sentence
("Deterministic, and high-entropy") is about the derivation, not the fallback.
Checked and passed.

Hunk 9: "any **remaining** record extents". §5.2 (624–626) defines a record extent
as "the bytes any record's extent slot references, whatever the record's type", and
§9.7 (1332–1334) confirms a layer record's extent slot addresses its tile-index
region — so without "remaining" the item ordered every index region twice. §20.5's
own figure text (3225–3226) states the same fact ("a relocated tile-index region —
itself a record extent (§5.2)"). Coverage after the repair is complete against
§5.2's four structure classes. Checked and passed.

## Byte-level reasoning, case by case

- X-01: input carries a structural reject-tile entry, so the input is
  nonconforming — but [R-WRT-01]/§20.5's opening expressly license a compactor to
  carry a latent violation into its output, so emitting is not barred by
  [R-CNF-05]. Compactor C (verifies the entry's value domain) emits nothing;
  compactor D (does not) emits a compacted file whose regenerated region carries
  the entry's original offset/length. Different bytes on disk. BYTE-LEVEL.
- X-02: same file; appender A (per §20.3 step 2) emits a new generation carrying
  the entry forward; appender B (per hunk 4's generalised ground) refuses.
  §20.3 step 2 is explicit, so B is a misreading — but hunk 4 supplies the ground
  for it and §20.5's 3247 reinforces it. BYTE-LEVEL, verdict PLAUSIBLE.
- X-03: conforming file, MU = 0 / PE = 0 record with a latent defect, commit
  supersedes a tile. Appender A retains (step 2's MUST NOT); appender B drops
  (§20.4's MAY). Directory bytes differ and an extent becomes slack. BYTE-LEVEL.
- X-04, X-05, X-06, X-07, X-08, X-09: in every case the governing normative rule
  ([R-MTA-09]/[R-CNF-11]; §21.6's closing block; §20.3 step 4 at 2975; §14.5
  [R-SER-05]; §21.4's rows) is explicit and §21.1's "where a row and the rule it
  cites diverge, the rule governs" resolves the divergence, so no two competent
  implementations end up on different bytes or different verdicts. NOT byte-level.
  Hunks 1, 2 additionally sit in `>` blocks ([R-CNF-01]) and hunks 8–10 in
  appendices whose headings say non-normative.
