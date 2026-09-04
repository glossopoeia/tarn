# Audit transcript — lane "the-rule-repairs" (hunks 03, 06, 10, 12, 21)

## 0. Disclosure

Read:
- /private/tmp/claude-501/-Users-robertkleffner-Documents-GitHub-tarn-first-draft/r31-audit/case/hunk-03.diff
- .../case/hunk-06.diff, hunk-10.diff, hunk-12.diff, hunk-21.diff (my five only; no other hunk, no full.diff, no directory listing)
- /Users/robertkleffner/Documents/GitHub/tarn-first-draft/spec/tarn.md, by `sed -n` ranges:
  headings list (`grep -n '^#'`); 1243-1300 (§9.2); 1978-2040 (§14.2); 2700-2775 (§18.2 tail);
  3104-3240 and 3240-3330 (§20.3); 4535-4620 and 4620-4770 (App. G, App. H); 95-345 (§2 whole);
  3597-3683 (§21.1); 3794-3831 (§21.4); 3920-3984 (§21.7, §21.8); 544-590 (§4.6); 1821-1848 (§12.3);
  1885-1899 (§13.2); 2046-2084 (§14.3); 2983-3062 (§19.4); 806-900 (§6.2, §6.3); 973-1051 (§7.2);
  3062-3104 (§20 intro, §20.1, §20.2); 3393-3452 (§20.4); 3865-3920 (§21.6); 4155-4170 (§22.4);
  2604-2700 (§18.2 head); 2524-2582 (§17.3, §17.4); 1625-1654 (§11.1 note); 1752-1800 (§12.1);
  2113-2146 (§14.5); 1480-1500 (§9.7 excerpt); 3478-3495 (§20.5 excerpt); 2915-2958 (§19.2);
  1036-1050; 4190-4200.
Wrote: this file only. Nothing written to the scratch directory
(/private/tmp/.../r31-audit/scratch/the-rule-repairs/) — no scripts were needed; the arithmetic
below was done by hand and is shown.

Unrequested context that appeared before I began: a project-instruction pointer (CLAUDE.md -> AGENTS.md,
whose body I did not open), an index of the user's memory notes naming four TARN-related note titles,
an environment block listing recent commit subjects, and a tool-use system reminder. None of it was
used as evidence; no conclusion below rests on it. Hunk headers: every hunk's stated landing lines
(03: 1265-1267; 06: 2008-2011; 10: 2740-2749; 12: 3202-3205; 21: 4578-4579) match the changed lines I
found in the current file; nearest headings match. No header/body mismatch.

## 1. Hunk 03 (§9.2, lines 1260-1267)

Repaired text (verbatim, current file):
"Steps 4 and 6 bind a writer's **conduct** rather than its output, and are declared so here on the
model `[R-CNF-02]` states: a barrier orders writes against power loss and leaves no trace in the
bytes, so a file committed without one can be byte-identical to a file committed with it. A writer
that omits a barrier violates this requirement as an actor, and the file it produces is never
nonconforming by virtue of it, as `[R-CNF-02]` says of every conduct rule."

Rule adopted: omitting a step-4 or step-6 barrier is a violation by the writer (actor) of
[R-LIF-02]; it never makes the resulting file nonconforming.

The §2.3 sentence it is re-grounded on (lines 166-170, verbatim): "A few obligations this
specification places on writers govern their *conduct* rather than their output — where a value is
published, or which registry version a writer targets (§10.3, §18.3) — and a file is never
nonconforming by virtue of one: conduct rules bind the actor, the predicate binds the bytes."

Check 1 (tense/quantifier): "the file it produces" = the new state the commit produces; "never" matches
§2.3's "never nonconforming by virtue of one"; "every conduct rule" matches §2.3's general "conduct rules
bind the actor" (quantified over the class, not the two examples). PASS.
Check 2 (citations): [R-CNF-02] at line 176 — says exactly the claimed thing. "this requirement" =
[R-LIF-02] (line 1258), whose steps 4 and 6 are the barriers. PASS.
Check 3 (label): body paragraph, not a blockquote; normative under [R-CNF-01]. The three Notes and the
Example after it are labeled and non-normative; the rule's statement is not inside them. PASS.
Check 4 (same passage): §9.2's first Note ("A writer that re-points a new trailer ... has left step 3
unperformed") is about step 3, not 4/6. Third Note ("Where barriers are weaker than assumed ...") is
consistent. No carve-out collides. PASS.
Check 5 (exhaustive claims): "never", "every conduct rule". §2.3 asserts the same "never"; "every" is
§2.3's own generality. The §2.3 count for its OTHER category — "A writer obligation whose violation this
specification expressly declares not to be a file-conformance violation ... §6.3's flags = 0 against a
set ignore-lane bit and §6.2's pre-trailer gap longer than [R-LIF-02] step 5's pad are the cases this
text states" — verified: §6.3 line 883-885 "a set ignore-lane bit is not a file-conformance violation";
§6.2 line 830 "a longer gap is conforming, and no conforming commit produces one". Count = 2, matches.
The OLD §9.2 wording ("is not nonconforming on that account") read as a bare express declaration and so
as a third member of that category; the repair's "declared so here on the model [R-CNF-02] states"
places the barrier steps in the conduct category, so the count of two stands. Sweep for further express
declarations (§1 below, "on that account|file-conformance violation|not nonconforming|conforming all the
same|not thereby nonconforming"): hits 172, 292, 1490, 2007, 3600, 3610, 3905, 3949 — 172 is §2.3
itself, 3905 is §21.6's experimental-type case (conduct, cites [R-CNF-02]), 2007 is [R-SER-08]'s reader
(not a writer obligation), the rest are register/§21.1 phrasing. No third case. PASS.
Check 6 (siblings): structure = [R-LIF-02]'s six steps. Steps 1,2,3,5 bind output (bytes); 4 and 6 are
the only two barrier steps and both are named. Nothing left ungoverned. PASS.
Check 7 (analogy): "on the model [R-CNF-02] states" / "as [R-CNF-02] says of every conduct rule".
Repair's verb: "the file it produces is never nonconforming by virtue of it"; cited: "a file is never
nonconforming by virtue of one". Same verb, same set (a conduct-rule violation). PASS.
Check 8 (anaphors): substitution within one sentence, nothing inserted between sentences. Forward:
"the strict increase above" (line 1272) -> step 5's strict increase in the [R-LIF-02] paragraph, before
and after; "the barriers of steps 4 and 6" explicit; "the Note above" (2nd Note) -> 1st Note. Backward:
"this requirement" -> [R-LIF-02]; "by virtue of it" -> the omission (or the requirement; both readings
give the same proposition). PASS.
Restatements swept: "barrier" (13 hits) — §20.2 line 3099 "(steps 4–6 — both barriers, not one)",
§20.3 step 6 (3311-3318), §20.5 (3488 "both, not one — are owed here"), App. H 4731 "including both
barriers (§9.2)". None characterises conformance consequence; nothing left inconsistent.
Verdict: no finding.

## 2. Hunk 06 (§14.2, lines 2001-2014)

Repaired text: "A reader that does not reject the tile and returns the value — whether or not it
detected the violation — MUST report 0x00 as false and every other byte as true."
Old: "A reader that neither detects the violation nor rejects the tile, and returns the value, MUST
report 0x00 as false and every other byte as true."

Rule adopted: every reader that returns an interleaved bool value from a tile it has not rejected
resolves 0x00 -> false and any other byte -> true, detection irrelevant.

Reach before: readers with (not detected) AND (not rejected tile) AND (returns). Reach after: (not
rejected tile) AND (returns). Newly bound: a reader that detected the byte, did not reject the tile (or
file) and returns the value. Not bound: a reader that rejects the tile (T-scope failure), a reader that
rejects the file under [R-CNF-12], a verifier that reports and returns nothing, an updater copying the
tile's bytes (it produces bytes, it does not "return the value"; [R-WRT-05]/[R-LIF-01] keep the stored
tile byte-identical).

Check 1: actor = reader (verifiers/updaters inherit, §2.3). Set: as above. Tense: the byte as stored.
The normative rule IS this sentence ([R-SER-08], line 2014). PASS.
Check 2: [R-CNF-12] (line 331): "For a nonconforming file no acceptance obligation exists — a reader MAY
reject it upon detecting any violation, including violations whose assigned detector is the verifier"
— it governs the detecting reader's licence to reject; the repaired sentence governs what it returns if
it does not. Complementary. [R-SER-08] cross-cites checked: §12.3 [R-TYP-04] line 1831 "the one case
where a reader resolves a byte to a value rather than passing it through arises only in a nonconforming
file, and [R-SER-08] states it" — consistent; §19.4 step 8 line 3029 "[R-SER-08] fixes what a reader
returns for the one byte a conforming file cannot" — consistent; §21.1 line 3677-3680 "[R-SER-08] is the
one rule that goes the other way: it resolves a nonconforming interleaved boolean byte to a value rather
than serving it through" — consistent with the widened form; §21.4 T2 (line 3805) — writer-side
condition, detector verifier, "the two rows together covering [R-SER-08]" — still describes the rule;
App. H reader entry (4721-4723) "the sole resolved byte ... being a nonconforming interleaved boolean it
chooses to return rather than reject" — already phrased in the widened form. PASS.
Check 3: body paragraph; normative. The **Rationale.** block after it ("two readers handed the same
malformed tile could disagree about a sample and both be conforming ... Defining the charitable path
costs nothing") still describes the rule, more strongly than before. The **Note.** block ("Only the
in-tile byte, whose detector is the verifier, could be met by a reader with no obligation to act on
it") still true. PASS.
Check 4: preceding sentence "[R-CNF-12] governs a reader that does detect it" sits beside the new
"whether or not it detected" — not a contradiction: [R-CNF-12] governs rejection, [R-SER-08] governs the
return; the parenthetical exists to say so. §19.4 step 7 keeps padding-position bytes from ever being
returned; step 8 defers to [R-SER-08]. [R-CNF-04] "MUST NOT ... infer values this specification does not
define" — the value is defined here, and [R-TYP-04] carves the case expressly. [R-CNF-09] does not
reach: T2's detector is the verifier. No rule tells a newly-bound reader to do anything else with that
byte. PASS.
Check 5: "every other byte as true", "never arises in a conforming file, where the only bytes present
are 0x00 and 0x01" — pre-existing; in a conforming file real-position bool bytes are 0x00/0x01
([R-SER-08]) and padding-position bool bytes carry the fill byte, itself 0x00/0x01 ([R-TYP-07],
[R-SER-05]). Holds. PASS.
Check 6: structure = a bool value byte. Real position, interleaved: writer [R-SER-08], verifier T2,
reader return [R-SER-08]. Padding position: [R-SER-05]/T4, never returned ([R-GEO-04]). Fill byte:
[R-TYP-07]/L35, reader reject-layer. Packed-plane bit: every pattern decodes ([R-SER-03]); pad bits
T5. Nothing ungoverned. PASS.
Check 7: no analogy in the repaired text. N/A.
Check 8: substitution; forward "That rule fixes what such a reader returns" — "such a reader" -> the
reader of the previous sentence, now the widened set (intended). "it neither makes the byte conforming
nor relieves the verifier, and it never arises in a conforming file" — "it" -> the rule / the case;
unchanged. PASS.
Verdict: no finding. Rejected candidates recorded in §7.

## 3. Hunk 10 (§18.2, lines 2739-2749) and Hunk 21 (App. G item 3, lines 4577-4579)

Hunk 10 repaired text: "Writers MUST serialize object members, at every nesting depth, in ascending
order of their keys' UTF-8 bytes, compared lexicographically as unsigned bytes with a proper prefix
ordering first."
Rule adopted: member order is the bytewise unsigned lexicographic order of decoded keys' UTF-8 bytes; a
proper prefix precedes the string it prefixes.

Literal application, three keys: "a" = 61; "ab" = 61 62; "b" = 62.
- "a" vs "ab": "a" is a proper prefix -> "a" < "ab".
- "ab" vs "b": first byte 61 < 62 -> "ab" < "b".
- "a" vs "b": 61 < 62 -> "a" < "b".
Order: a, ab, b. Total, and both readings of "with a proper prefix ordering first" (a prefix sorts
first / the prefix test is applied first) give the same order, since bytewise lexicographic order
already places a prefix first. Unsigned pin matters: "z" = 7A vs "é" = C3 A9: unsigned 7A < C3 -> z, é;
signed C3 = -61 would put é first. The repair closes that fork.
Register rows: F27 (line 3720) and L48 (line 3791) both say "not in ascending order of their keys' UTF-8
bytes; the document stays readable and readers process it unchanged" — restate the rule at lower
precision; §21.1: the rule governs. Line 2726 "[R-MTA-05]'s sort order is likewise over decoded keys'
UTF-8 bytes" — consistent (fixes the subject as decoded keys). App. G item 9 (4665) and App. H (4728)
"sorts user-metadata object members by their keys' UTF-8 bytes" — consistent. §21.6 line 3890 — reader
side unchanged. PASS on all restatements.
Check 3: body paragraph, normative. Check 4: "No duplicate keys" bullet makes equal keys unreadable, so
the sort never meets a tie; "[R-ENC-13] raw bytes" consistent with byte comparison. Check 5: "at every
nesting depth" pre-existing. Check 6: siblings of member order — whitespace, number formatting, string
escaping — are named as deliberately free ("does not make two writers' output identical"; App. G item 9
pins the producer). Check 7: no analogy. Check 8: "This makes one writer's output reproducible" — "This"
-> the ordering; unchanged.
Hunk 10 verdict: no finding.

Hunk 21 repaired text: "For each layer in ascending layer-name byte order, compared as `[R-MTA-05]`
compares keys: its stored tiles in disk-ordinal order, ..."
Rule adopted (profile item, non-normative): layers are emitted in the unsigned bytewise lexicographic,
prefix-first order of their name bytes.
Check 2: [R-MTA-05] now states that comparison. Layer names: UTF-8, non-empty, <= 255 bytes (§4.6),
raw-byte identity ([R-ENC-13]), unique among a file's layers ([R-ENC-15], F4) -> a total order over
layers. PASS.
Check 7 (analogy, word for word): repair: "layer-name byte order, compared as [R-MTA-05] compares keys";
cited: "compared lexicographically as unsigned bytes with a proper prefix ordering first". Same verb
("compared"), same kind of set (byte strings of a name); the "decoded" qualifier on keys has no
counterpart for layer names, which are stored raw, and the borrowed part is the comparison only. PASS.
Check 3: Appendix G is identified non-normative; the item binds nobody ([R-CNF-01]); the repair intends
no force. Correctly placed.
Check 8: forward back-references in item 3: "That order runs over top-level records first" -> the total
emission order, before and after (the insertion is a parenthetical inside the first clause);
"this very order is what fixes it" -> the record order; "this key" -> the record key; "the writer
chooses" — unaffected. PASS.
Check 6 (siblings in the same item): the item defines FOUR orderings: (i) layer order — now pinned;
(ii) tile order within a layer — disk-ordinal, pinned; (iii) record order by type — u16 field value,
"ascending record order", pinned; (iv) within a type: "type 0x0001 ties by layer name, and every other
type by the record's header with extent_offset masked to zero, then its inline payload, then the
contents of its extent, compared lexicographically" (line 4590-4593). (iv)'s "compared lexicographically"
carries neither "as unsigned bytes" nor a prefix rule — exactly the two things the repair added for
(i). Prefix: cannot arise — the 24-byte header (§7.2) includes inline_length at offset 4 and
extent_length at offset 16, so equal headers imply equal key lengths. Signedness: open. A Java/JVM
adopter comparing byte[] arithmetically (signed) and a C/Rust adopter (unsigned) place two records of
one type whose first differing byte is >= 0x80 in opposite orders, so the profile — whose only purpose
is byte-identity — yields two files. And "ties by layer name" in (iv) does not say it uses the
comparison (i) borrows, though a reader would probably assume so. FINDING E-02 (non-byte-level: App. G
binds no conforming actor; no accept/reject verdict or emittable set moves).
Hunk 21 verdict: one finding, E-02.

## 4. Hunk 12 (§20.3 step 4, lines 3199-3208)

Repaired text: "Where a change does reach them it makes the stored bytes of each tile it reaches
denote values the writer did not store — wrong content, of the kind §21.7 leaves unwitnessed — and
re-emitting those tiles would strand the originals as slack — every tile the change reaches, since
[R-LIF-01] freezes them where they lie — leaving the file larger for a change that reads like a
directory edit."
Old: "it makes each stored tile it reaches nonconforming, and re-emitting those tiles would strand the
originals as slack".

Rule asserted: a re-type reaching a stored tile yields wrong content that the register does not
witness (so the file stays conforming and only the updater is in violation).

Two re-types, checked against the register:
(A) int8 -> uint8 (element size 1 -> 1, table §12.1). Planar: decoded size P·1 unchanged (T3 no; T14 no
for codec 1; T21/T22 no). Interleaved: Q unchanged. Padding positions: fill field stays one byte with the
same bytes -> T4 no. Bytes decode and are returned as bit patterns ([R-TYP-04]); 0x80 now reads 128
instead of -128. No row fires: unwitnessed, file conforming. The repaired sentence is TRUE here (and the
old "nonconforming" was false here).
(B) uint8 -> uint16 (element size 1 -> 2). Planar: decoded size P·1 -> P·2; the stored tile decodes to
P bytes != 2P -> T3 ("The decoded payload's byte length is not exactly the tile's decoded size", reader,
tile use, reject-tile); under codec 1 also T14; under zstd T21/T22 can fire. Interleaved: Q = sum of
sizes changes, P·Q changes -> T3. The bytes do not "denote values" at all — the decode fails on length
and the tile is rejected; the condition is witnessed by a reader-detected row. The repaired sentence is
FALSE here (and the old "nonconforming" was true here).
(A') uint8 -> bool. Interleaved (size 1 -> 1): any stored real-position byte >= 0x02 becomes T2
(verifier), a padding byte != fill becomes T4, and a fill byte >= 0x02 becomes L35 (reader,
reject-layer) — witnessed; §21.7's own text says so: "The obligations of §14.5 and [R-SER-08] narrow
this only where content is structurally constrained: padding positions, pad bits, and boolean bytes."
Planar: decoded size P -> ceil(P/8), T3 for every P >= 2. FALSE here too.
The sentence ranges over every re-type ("changing it is such a change wherever the layer stores a tile
that carries that channel"), and the §14 bar's own list two lines above names "the decoded size" among
the effects a re-type can have, which is precisely the witnessed case. So the repair swapped which half
of the population the sentence is wrong about rather than covering both. FINDING E-01 (OVERCLAIM;
not byte-level — the MUST NOT is unchanged and bars A, A' and B alike; in B the resulting file is
T3-nonconforming under both readings, in A it is conforming and the commit barred under both readings,
so no emittable set or verdict moves).

Other checks on hunk 12:
Check 1: tense — "each tile it reaches" is a tile the superseded generation stores (set by "in the
generation this commit supersedes" and "Where the superseded generation stored no tile carrying that
channel"); "values the writer did not store" — "the writer" has no antecedent in step 4 (subjects are
"a commit", "an updater", "the layer"); nearest earlier "writer" is step 2's "writer obligations". Either
reading (the storing writer / the committing updater) yields the same proposition. Not filed.
Check 2: §21.7 — its unwitnessed test (line 3938) and its "wrong sample values ... simply wrong data"
paragraph exist and say what is claimed for case A; [R-LIF-01] freezes the prefix — PASS for the
citation's content, FAIL for the range (E-01).
Check 3: numbered step in body text, normative. PASS.
Check 4: same passage — the bar's list "the decoded size, the byte offset ... the sample type each value
in the image is read under" is the contradicting text for case B (quoted in E-01).
Check 5: "of the kind §21.7 leaves unwitnessed" — falsified (E-01). "each tile"/"every tile the change
reaches" pre-existing and unchanged.
Check 6: structure = a channel entry's declarations reachable by a re-type: type (this paragraph), fill
(L35 for bool; T4 if padding no longer matches a changed fill — governed by the §14 bar's "content
[R-SER-05] fixes"), element size (bar's "decoded size"/"byte offset"). All named by the bar. PASS.
Check 7: no analogy phrase. N/A.
Check 8: forward: "those tiles" -> "each tile it reaches" (same set as old "each stored tile it
reaches"); "the originals" -> those tiles' stored extents; "Such a change is a new layer" -> a change
reaching stored tiles; next paragraph "One effect is barred beside it" -> the §14 bar. Backward: "them"
in "Where a change does reach them" -> tiles carrying that channel that the superseded generation
stored. All unchanged. PASS.
Restatements: "re-typ|retyp|reinterpret" -> 1525 (§10, unrelated), 1640 (§11.1 Note: "Re-typing a
channel is the §14 bar's own subject, barred wherever the layer stores a tile that carries that channel,
and free where it does not" — consistent, non-normative), 3199 (this passage). No other place describes
the consequence, so nothing was left unswept.

## 5. Sweeps run (verbatim, with hit counts)

All `grep -n` on spec/tarn.md:
- `grep -n -i 'conduct'` -> 7 (167,169,1043,1260,1266,3881,3909)
- `grep -n 'as an actor'` -> 1 (1265)
- `grep -n -i 'lexicograph'` -> 2 (2740, 4593)
- `grep -n -i 'proper prefix\|prefix ordering'` -> 1 (2741)
- `grep -n -i 'name byte order\|byte order of\|ascending order\|ascending layer'` -> 4 (2740,3720,3791,4578)
- `grep -n -i 'unwitnessed'` -> 6 (2641,3204,3938,3950,3963,3969)
- `grep -n '0x00 as false\|every other byte'` -> 1 (2010)
- `grep -n -i 'wrong content'` -> 2 (3203, 3927)
- `grep -n -i 'barrier'` -> 13 (854,1251,1261,1264,1270,1293,3097,3098,3099,3311,3318,3488,4731)
- `grep -n -i 're-typ\|retyp\|reinterpret'` -> 3 (1525,1640,3199)
- `grep -n -i 'on that account\|file-conformance violation\|not nonconforming\|conforming all the same\|not thereby nonconforming'` -> 8 (172,292,1490,2007,3600,3610,3905,3949); 'on that account' alone -> 0 (old text gone); control 'not thereby nonconforming' -> 1 (2007)
- `grep -n -i 'transcod\|re-encod\|recompress\|re-compress'` -> 3 (3429,3440,4139)
- `grep -n 'neither detects\|whether or not it detected\|does not detect the'` -> 2 (2006, 2009); 'neither detects' alone -> 0 (old text gone); control 'whether or not it detected' -> 1
- `grep -n -i 'sample type'` -> 13 shown (capped at 60 lines)
- `grep -n 'R-MTA-05\|R-SER-08\|R-LIF-02\|R-CNF-02\|R-ENC-13\|R-TYP-07\|R-CNF-12'` -> 66 hits, all opened where they bear on a hunk (listed in §1-§4)
- `grep -n -i 'sorted\|sort order\|sorts '` -> 5 (2726,2747,3676,3890,4665)
- `grep -n -i 'layer-name\|layer name order\|by layer name'` -> 4 (2896,2925,4578,4591)
- `grep -n -i 'strand'` -> 8; `grep -n -i 'denote'` -> 11; `grep -n -i 'resolves a byte\|resolved byte\|resolves rather'` -> 3 (1831,3680,4721); `grep -n 'one byte a'` -> 3 (1889,3029,3680)
- Controls for wrap-sensitivity: `grep -n 'A few obligations'` -> 1 (166); `grep -n 'proper prefix'` -> 1 (2741). Every zero above is for a phrase the repair deleted, and its replacement phrase was found by the paired control.

## 6. Derived numbers

- §2.3 second-category cases: counted 2 (§6.3 line 883-885; §6.2 line 830) vs §2.3's two named -> equal.
- Key order a < ab < b (bytes 61; 61 62; 62); z (7A) < é (C3 A9) unsigned, reversed if signed.
- Element sizes (§12.1 table): bool 1, int8 1, uint8 1, uint16 2. Planar decoded sizes: int8->uint8 P->P;
  uint8->uint16 P->2P; uint8->bool P->ceil(P/8) (differs for P >= 2).
- Record header 24 bytes; inline_length at offset 4, extent_length at 16 -> equal headers imply equal
  (header+payload+extent) lengths -> no proper-prefix case in App. G item 3's record key.
- §21.4 header says 26 conditions; rows T1..T26 counted = 26.

## 7. Rejected candidates

- Hunk 03: "never nonconforming by virtue of it" vs a crash after an omitted barrier leaving a torn
  file — dropped: the torn bytes are nonconforming by virtue of the bytes, which is §2.3's own
  formulation ("the predicate binds the bytes"), and the sentence restates §2.3 verbatim in force.
- Hunk 03: does §9.2's own express declaration make the barrier a third member of §2.3's "expressly
  declares" category? Dropped: the repair's "bind a writer's conduct ... declared so here on the model
  [R-CNF-02] states" self-classifies it as a conduct rule, the category §2.3 leaves open-ended.
- Hunk 06: "does not reject the tile" while [R-CNF-12] says "a reader MAY reject it" (the file) —
  dropped: pre-existing phrase; "no acceptance obligation exists" licenses the narrower refusal, and
  App. H already reads "chooses to return rather than reject".
- Hunk 06: "[R-CNF-12] governs a reader that does detect it" read as exclusive, colliding with the new
  MUST — dropped: the "whether or not it detected" parenthetical exists to deny the exclusive reading,
  and the two rules answer different questions (reject? / return what?).
- Hunk 10: "with a proper prefix ordering first" misread as "apply a prefix ordering before the
  lexicographic one" — dropped: both readings give the same total order, so no implementation forks.
- Hunk 12: "the writer" without antecedent — dropped: both candidate antecedents make the clause true
  and neither changes what is barred.

## 8. Findings

E-01 (hunk 12, OVERCLAIM, not byte-level) — see §4.
E-02 (hunk 21, UNCONSTRAINED_SIBLING, not byte-level) — see §3.
