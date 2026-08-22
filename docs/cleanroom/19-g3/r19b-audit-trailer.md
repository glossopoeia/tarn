# Repair audit trailer — r19, second-pass repairs, hunks 01 and 02

Auditor scope: hunk-01.diff (§20.5, line 3170) and hunk-02.diff (§21.7, line 3617).

## 0. Access disclosure

Read, in full or in the ranges named:

- `/private/tmp/.../r19audit2/hunk-01.diff` (my charter hunk)
- `/private/tmp/.../r19audit2/hunk-02.diff` (my charter hunk)
- `/Users/robertkleffner/Documents/GitHub/tarn/spec/tarn.md`, ranges:
  100–110 (`[R-CNF-01]`), 145–160 (`[R-CNF-02]`), 170–230 (`[R-CNF-05]`,
  `[R-CNF-06]`, `[R-CNF-11]`), 415–432 (§4.3, `[R-ENC-07]`), 785–830 (§6.3,
  `[R-CNT-07]`/`[R-CNT-08]`/`[R-CNT-24]`/`[R-CNT-26]`), 1368–1435 (§10.1–§10.4),
  2415–2470 (§18.2), 2566–2620 (§18.3, §18.4), 2744–2775 (§19.3, §19.4 open),
  3120–3230 (end of §20.4 table, §20.5 through the relocation paragraph),
  3240–3270 (`[R-WRT-09]`, the Note, §18.3 header), 3271–3352 (§21.1),
  3350–3405 grepped for F18/F19/F34/F35/F36, 3405–3462 grepped for L24/L25,
  3496–3560 (§21.5 and §21.6 in full), 3560–3640 (§21.6 tail, §21.7, §21.8),
  4235–4290 (Appendix G items 6–10 and its closing paragraph, Appendix H head).

Ran (all against spec/tarn.md only):

```
grep -n "R-EXT-01" spec/tarn.md
  1385:`[R-EXT-01]`
  3178:enumerates (`[R-EXT-01]`), a carried ignore-lane bit and an

grep -n "^#### 10\.\|^### 10\|^#### 21\.7\|^#### 20\.5" spec/tarn.md
  1368:### 10. Extension Points and Registry
  1370:#### 10.1 The extension surface
  1387:#### 10.2 Numeric identifier spaces
  1412:#### 10.3 The experimental range
  1430:#### 10.4 Registration
  3149:#### 20.5 Compaction
  3580:#### 21.7 What no check detects

grep -n "R-WRT-09\|R-CNT-26\|R-CNT-08\b" spec/tarn.md
  818, 824, 2666, 3025, 3026, 3158, 3159, 3176, 3184, 3209, 3265, 3386, 3541,
  4247, 4252, 4279

grep -n "R-CNF-11\|R-CNF-05\|R-CNF-01\b" spec/tarn.md
  106, 181, 223, 649, 922, 994, 1354, 2262, 2402, 2470, 2531, 2551, 2867,
  2871, 2895, 3020, 3105, 3280, 3394, 3395, 3459, 3460, 3593, 4155, 4357

grep -n "version_minor\|ignore-lane" spec/tarn.md
  153, 424, 532, 744, 793, 798, 809, 813, 815, 820, 1378, 2574, 3025, 3026,
  3174, 3178, 3180, 3184, 3541, 3542, 3624, 3625, 4003, 4004, 4247, 4250, 4279

grep -n "four vehicles" spec/tarn.md
  423:four vehicles: new record types (§7), new enum values in ranges this
  1372:This format grows through exactly four vehicles (`[R-ENC-07]`), and
  3177:compactor does not implement — by any of the four vehicles §10.1

awk 'NR>=3151 && NR<=3189 && /^>/'   -> no output (no blockquote lines)
awk 'NR>=3580 && NR<=3633 && /^>/'   -> no output (no blockquote lines)
awk paragraph-boundary scan 3149–3196 -> blanks only at 3150 and 3190, so
  3151–3189 is ONE paragraph terminated by `[R-WRT-06]` at 3189.

Unwrapped (whole-file `tr '\n' ' ' | tr -s ' '`) exact-phrase confirmations:
  "the two it is likeliest to meet"                                    -> found
  "A second set of obligations is omitted from the register because a
   single file exhibits no witness of their violation"                 -> found
  "§21.7 the account, by class, of what fails it"                      -> found
  "A writer obligation whose violation this specification expressly
   declares not to be a file-conformance violation binds the actor in
   the same way"                                                       -> found
```

Nothing outside spec/tarn.md and my two hunk files was read. I did not read
full.diff, did not list the scratchpad directory, did not touch docs/,
conformance/, registry.json, or git history.

---

## 1. The rule each repair adopts, in my own words

**Hunk 1 (§20.5).** For a compactor: (a) it MUST copy the input's unknown
ignore-lane flag bits into the output trailer instead of writing flags = 0;
(b) if the output carries *any* feature the compactor does not implement,
where "feature" is anything arriving by one of §10.1's four extension
vehicles, then it SHOULD set the output's version_minor to at least the
input's; (c) otherwise it SHOULD set version_minor to `[R-CNT-26]`'s floor —
the lowest minor that defines every feature present in the file. Sentence (d)
then asserts that "neither obligation" can be checked from the output alone.

**Hunk 2 (§21.7).** Both (a) and (b) above belong on §21.7's second list —
the obligations left out of the error register — and they are there for the
same reason the other members are: the output file exhibits no witness of
their violation, since it records neither its input's flags nor its input's
minor.

---

## 2. Check 2 — every citation, opened, with verdict

| Cited in | Target | What the repair claims | Verdict |
|---|---|---|---|
| H1 | §10.1 | enumerates four vehicles, closed | **PASS.** L1372 "This format grows through exactly **four** vehicles"; L1374–1381 four numbered items; L1383 "**Nothing else** extends this format." Count = 4, list closed. |
| H1 | `[R-EXT-01]` | the requirement for that list | **PASS with caveat.** L1385 `[R-EXT-01]` terminates the paragraph asserting closure, so it is the right ID for *closure*. Caveat: §10.1 itself attributes the count parenthetically to `[R-ENC-07]` (L1372), and §4.3's "All format growth happens through four vehicles…" sentence (L422–425) sits *after* the `[R-ENC-07]` marker, so `[R-ENC-07]`'s own governed text is about fixed structure sizes. `[R-EXT-01]` is nonetheless the only identifier whose governed text says the list is exhaustive. Citation resolves. |
| H1 | `[R-CNT-08]` | flags = 0 is what §6.3 requires of a file created under this text | **PASS.** L807–809: "a writer creating a file under this text MUST write flags = 0". L811–814 even states the compactor carve-out from §6.3's side and cross-cites §20.5/`[R-WRT-06]`. Consistent both directions. |
| H1 | `[R-CNT-26]` | names an *overstatement*; states a *floor* | **PASS.** L820–824: "A writer SHOULD emit the **lowest** version_minor that defines every feature present in the file" (a floor) … "a **higher** minor than needed … misstates the file's feature floor to tooling" (the overstatement). The repair's "the mirror of the overstatement `[R-CNT-26]` names" is exactly right, and repairs the previous version's "as `[R-CNT-26]` describes", which `[R-CNT-26]` did not describe. |
| H1 | `[R-WRT-06]` | governs the paragraph | **PASS.** Paragraph-boundary scan: 3151–3189 is one paragraph, terminated `[R-WRT-06]` at 3189. Both obligations are inside it. |
| H1 | §21.7 | says neither is witnessed | **PASS as a pointer** (hunk 2 puts them there), but see A-05 for whether §21.7 is the right home. |
| H1 | §20.3 step 6 | *(removed by the repair)* | n/a. L3025–3026 still reads "ignore-lane flag bits copied forward (`[R-CNT-08]`), and version_minor per `[R-CNT-26]`", which remains correct for an appender. Dropping the cross-reference loses nothing. |
| H2 | §20.5 / `[R-WRT-06]` | two obligations on a compacted file's trailer | **PASS on identity.** Both sentences are in the `[R-WRT-06]` paragraph, both are about trailer fields (flags, version_minor). Modal labels are accurate: MUST for the bits, SHOULD for the floor. |
| H2 | `[R-LIF-01]`, §9.7, `[R-ENC-06]`, `[R-ERR-01]` | unchanged context | **PASS**, untouched by the repair. |

**Check 2 verdict: every identifier and section number resolves and says what
the repaired text claims.** The `[R-CNT-26]` mirror-of-the-overstatement fix
is a genuine improvement over the text it replaced.

---

## 3. Check 3 — normative placement

`awk` over 3151–3189 and 3580–3633 finds no line beginning `>`. Both repairs
land in plain prose carrying requirement identifiers (`[R-WRT-06]` at 3189,
`[R-ERR-01]` at 3633). Neither is a Note/Example/Rationale block.
**Check 3 passes for both hunks.** No rule stated only inside a `>` block; no
blockquote edited while a normative statement elsewhere kept the old wording.

---

## 4. Check 5 / Check 1 on hunk 1 — the deferral, counted and falsified

The repair defers to "any of the four vehicles §10.1 enumerates". §10.1:

1. New record types (§7.3)
2. New values in the ranges this specification reserves (§10.2)
3. New ignore-lane flag bits in the trailer (§6.3)
4. New standardized user-metadata keys (§18.4)

Closed: "Nothing else extends this format." Count 4, corroborated at §4.3
L422–425. So the *count* and the *closure* both hold.

Now the charter's real test: can a compactor **carry** each member without
implementing it, in an output that is a conforming file?

**Vehicle 3 — set ignore-lane bit.** Yes. §21.6 row: "An ignore-lane flag bit
(16–31) is set | Ignored; the file is **conforming** — such bits are defined
by later minor versions". And §20.5 MUSTs the carry-forward. ✔

**Vehicle 4 — unrecognized `tarn.` key.** Yes. §21.6 row: "A user-metadata
document carries an unrecognized `tarn.`-prefixed key | **Conforming**: later
minor versions register keys". §18.3 `[R-MTA-06]` says the same. ✔

**Vehicle 2 — a value from a reserved range.** No, not in a conforming file
under this text, and mostly not at all:

- §10.2 partitions every space into assigned / **reserved** / experimental.
  §10.3: "a value from a reserved range MUST NOT be emitted at all before
  this specification assigns it."
- For the value sets of §11.4, §12.2, §14.1, §15.1, §17.2, §17.3, §10.3 makes
  a reserved value "a validity error at the owning scope". §19.3 (`[R-RDR-03]`)
  puts exactly "the value sets of §11.4, §12.2, §14.1, §15.1, §17.2, and
  §17.3" inside full layer-record validation, and `[R-WRT-09]` (L3260–3265)
  obliges a compactor to verify "each retained layer's record (§19.3)". So the
  compactor **detects** it, and `[R-WRT-06]` L3159–3160: "A compactor MUST
  refuse to compact when any check `[R-WRT-09]` obliges fails". The compaction
  never happens.
- For the metadata-encoding space (§18.2), §21.5 row **R1** registers
  "encoding 0, or a reserved-range value (3-0x7F)" as a violation, detector
  *reader*, detected *open (top-level); layer access (sub-record)*. A compactor
  is a reader of its input (§2.3, `[R-CNF-06]`), so it detects it, and
  `[R-WRT-06]` bars emitting a file carrying a violation it has detected.
- For record types, §21.2 **F36** / §21.3 **L25**: a reserved-range type value
  "which this specification has not assigned; **emitting one is a violation
  whatever its MU bit**". Detector *verifier*, so a compactor need not detect
  it — but the output is then a **nonconforming** file.

**Vehicle 1 — new record types.** A "new record type" is drawn from the
record-type reserved range 0x0003–0x7FFF (§10.2 table), so it is F36/L25:
emitting one is a violation whatever its MU bit. §21.6 makes this explicit:
"a *reserved*-range type is read the same way, but emitting one is a violation
(F36, L25)". So vehicle 1 also cannot appear in a conforming compactor output.

**Conclusion.** Of the four vehicles, exactly **two** can appear in a
conforming file this text's compactor carries forward — and they are precisely
the two §21.6 blesses, which are precisely the two the repair demotes to
"likeliest to meet". The deferral therefore over-reaches on two members. This
is finding **A-01**. And it means the phrase "the two it is likeliest to meet"
is not smuggling the old enumeration back in — it is *understating* an
enumeration that is in fact exhaustive for conforming outputs; the repair's
own hedge is weaker than the document supports. Both named members are
genuine members of §10.1's list (3 and 4), so that half of the charter's
question is clean.

The case the four-vehicle frame **misses**: §21.6 also makes conforming (i) "A
record type this specification has not assigned, from the **experimental**
range (≥ 0x8000, §10.2), carries MU = 0 | Ignored, and preserved or dropped
per its PE bit" and (ii) "A user-metadata record declares an
experimental-range (≥ 0x80) document encoding | Ignored; the file is
conforming". These are real, conforming, carried-forward things the compactor
does not implement — and they are *not* extension vehicles (§10.1's vehicle 2
is the reserved range; §10.2 keeps experimental separate; §10.3 calls
experimental values private use with no collision protection). An
implementer who reads "New record types (§7.3)" loosely enough to cover an
experimental type will raise version_minor for a value **no minor version
defines**, producing exactly the overstatement `[R-CNT-26]` warns of. Finding
**A-03**.

---

## 5. Check 1 on hunk 1 — quantifier and knowability

Quantifier/generation: the repair speaks about "the output" ("Where the
**output** carries any feature the compactor does not implement"), and
compares against "the **input's**" minor. Two generations, both named, no
tense slip. The MUST is over "the input's unknown ignore-lane flag bits" —
correct set. `[R-CNT-26]`'s floor is over "every feature present in the file"
— the output. All three quantifiers are right for the rule intended.

But the antecedent is not evaluable by the actor bound. §20.5 L3157–3158: the
compactor's "verification depth is `[R-WRT-09]`'s and **reaches no decoded
content**". `[R-WRT-09]` L3260–3265 lists the whole depth: the open (§19.1),
each retained layer's record (§19.3), the full index chain, and each
relocated extent's checksum. A user-metadata extent's terminal CRC is checked
(§21.5 R2); the document is never decoded (R5–R10 are detected at *extent
use*, which a compactor does not perform). So the compactor cannot see the
keys — and the repair's own words concede it: "in a record **it never
decoded**".

A conditional SHOULD whose antecedent the obligated actor cannot evaluate
collapses one of two ways: it never fires (nothing observable is ever
established), or it always fires (the compactor can never exclude an
unrecognized `tarn.` key in a record it did not decode, so the safe reading is
to raise the minor unconditionally). The two readings put different bytes at
F−56+2. Finding **A-02**.

I checked the previous wording for contrast: "Where any such bit is set" was
fully observable. The repair widened the trigger past the actor's own
verification depth. That is an overshoot as well as an ambiguity.

---

## 6. Check 4 on hunk 1 — contradiction in the passage it landed in

Read all of 3151–3230 plus the §20.4 table row above it and the Note/Example
below. Looked for, and did **not** find:

- a carve-out the new breadth collides with. The nearest candidate is the
  next sentence, "A compactor MUST refuse to compact a file carrying any
  record whose type it does not implement with MU = 1" — it *narrows* what
  can be carried but does not contradict the SHOULD, since it removes cases
  rather than licensing them.
- a MUST the new SHOULD lets an actor violate. The MUST-carry-forward and the
  SHOULD interlock correctly: whenever a bit is carried (the MUST bites), the
  bit is a vehicle-3 feature, so the SHOULD fires; the "Otherwise" branch is
  reachable only when no bit is set and nothing else unimplemented is carried.
  Coherent.
- a sentence true only under the old wording. The removed "as it does for an
  appender (§20.3 step 6)" was the one such, and it was removed.

One real problem in the passage: **the antecedent of "Neither obligation"**.
Sentence order is (a) MUST-carry-forward, (b) SHOULD floor, (c) "Otherwise
version_minor follows `[R-CNT-26]`'s floor.", (d) "**Neither obligation** has
a witness in the output alone (§21.7)." The two nearest obligations are (b)
and (c). Hunk 2 fixes the referent as (a)+(b), but §20.5 must read correctly
on its own, and the (b)+(c) reading is **false**: `[R-CNT-26]`'s floor is
"the lowest version_minor that defines every feature present in the file" —
a property of the output alone, and §21.6 registers the observable case
("version_minor is higher than this text defines | Accepted; minors never
gate", `[R-CNT-07]`). So one available reading of the new sentence asserts an
untruth. Finding **A-04**.

Cross-hunk agreement: hunk 1 asserts §21.7 covers two obligations; hunk 2
names two obligations in §21.7 and they are the same two ((a) and (b)). The
hunks **do** agree with each other on the referent. The defect is that §20.5
alone does not force that referent.

---

## 7. Check 4 / Check 3 on hunk 2 — is §21.7 the right list?

§21.7's second-list ground, verbatim (unwrapped grep confirms the phrase):

> A second set of obligations is omitted from the register because a single
> file exhibits no witness of their violation.

§21.1 fixes what §21.7 is for (unwrapped grep confirms):

> The register — §21.2 through §21.5 (`[R-ERR-02]`) — enumerates every
> **detectable file-conformance violation** this specification names … Its
> completeness is normative — a *detectable* file-conformance violation this
> specification names and the register omits is a defect in this document,
> detectability being the gate `[R-CNF-07]` already applies and **§21.7 the
> account, by class, of what fails it**.

So §21.7 is the account of what fails the **detectability** gate. Membership
presupposes there is a *file-conformance violation* to be undetectable.

Every other member of the second list clears that bar: `[R-LIF-01]`,
`[R-LIF-03]` (history), `[R-GEO-06]`, `[R-SER-01]` (ordinal mappings),
`[R-CNT-13]` ("opaque by construction"), `[R-CNT-18]`, §20.3 step 4's bar,
`[R-ENC-06]`. Each is a real nonconformity that no single file witnesses.

Hunk 2's two do not:

- **The SHOULD.** A SHOULD is not a MUST; deviating leaves the file
  conforming. `[R-CNT-07]`: "A reader MUST NOT reject a file for its
  version_minor." §21.6: "version_minor is higher than this text defines |
  Accepted; minors never gate." There is no violation for a witness to be
  missing *of*. The charter's suspicion is confirmed: **§21.7's ground does
  not cover a SHOULD's deviation.**
- **The MUST too.** A compactor that writes flags = 0 instead of carrying the
  bits forward emits a file with flags = 0 — the canonical, unimpeachable
  value. §6.3 itself: "a set ignore-lane bit is not a file-conformance
  violation". §21.6: "An ignore-lane flag bit (16–31) is set | Ignored; the
  file is conforming". Whichever way the bits go, the output is conforming.
  And `[R-CNF-02]` (L146–156) already classifies this exact subject matter:
  "A writer obligation whose violation this specification expressly declares
  not to be a file-conformance violation binds the actor in the same way;
  **§6.3's flags = 0 against a set ignore-lane bit** … are the cases this
  text states."

So both are **conduct** rules in `[R-CNF-02]`'s sense, not undetectable
violations, and neither belongs on §21.7's second list as its opening frames
it. The reason the repair gives — "the output carrying no record of its
input's flags or its input's minor" — is *factually true* of both, but it is
the wrong ground: it implies that with a witness these would be register rows,
which §21.1's own subject matter denies. Finding **A-05**.

Note for whoever repairs A-05: `[R-CNF-02]`'s "are the cases this text states"
is a closed two-item claim. If §20.5's two trailer obligations are relocated
there, that claim goes short by two and must be swept. I am not filing that as
a separate finding, because as the document currently stands `[R-CNF-02]` is
scoped to obligations the text "**expressly declares**" non-violations, and it
does not so declare for §20.5's two — so `[R-CNF-02]` is accurate today.

Contradictions I looked for in §21.7 and did **not** find: the added clause
does not collide with the first paragraph's `[R-CNF-11]` disclaimer (that
paragraph is about content-correctness, a different class); it does not
disturb the `[R-ERR-01]` terminator; the "for that same reason" chain back to
`[R-LIF-01]` still parses; §21.8's counts (121 conditions over 273 instances)
are untouched, correctly, since §21.7 carries no rows and §21.1 says so
expressly ("The subsections after §21.5 are not part of the register and carry
no rows").

---

## 8. Restatements swept / not swept

- **Appendix G item 8** (L4247–4252, non-normative): "a compactor adopting the
  profile carries its input's unknown ignore-lane bits forward instead, and
  where it carries **any feature it does not implement** takes §20.5's floor
  rather than `[R-CNT-26]`'s (`[R-WRT-06]`)." Already in the new broad form —
  **swept, consistent.** (It does not repeat the four-vehicle gloss, so if
  A-01 is fixed by narrowing §20.5, this line needs no change; if A-01 is
  fixed by keeping the breadth, it still needs none.)
- **Appendix G closing paragraph** (L4279): "`version_minor` at its floor,
  which `[R-CNT-26]` states as a SHOULD — item 8's creator's rule, not a
  compactor's (§20.5)". Consistent.
- **§20.3 step 6** (L3025–3026), appender: unchanged and still correct.
- **§6.3 `[R-CNT-08]`** (L811–814): states the compactor carve-out from the
  other side and cross-cites §20.5/`[R-WRT-06]`. Consistent with hunk 1's MUST.
- **§21.6 rows** L3541–3542: the non-violation homes for both trailer fields
  already exist. Not swept, and A-05 argues they are where hunk 2's material
  actually belongs.
- **§4.3** L422–425: the other statement of the four vehicles. Matches §10.1.
  (Pre-existing oddity, outside my hunks: that sentence trails *after* the
  `[R-ENC-07]` identifier.)

Searched the whole document for the compactor version_minor / ignore-lane rule
with the unwrapped grep above; the sites listed are all of them.

---

## 9. Byte-level determination, per finding

The discriminator: does the disputed *file* carry a register-row violation?

- **A-01.** The files a permissive reading admits (vehicle 1 or 2 carried
  forward) carry F36 / L25 / R1 rows. `[R-CNF-05]` bars every conforming
  writer from emitting them under both readings. Emittable set does not move.
  **Not byte-level.**
- **A-02, A-03, A-04.** The disputed files are conforming, and the two
  readings differ in the value of a trailer u16. But the rule at stake is a
  **SHOULD**: a conforming implementation may emit either value under either
  reading, and `[R-CNT-07]` forbids any reader rejecting on version_minor, so
  no accept/reject verdict moves either. The set of emittable byte sequences
  is identical under both readings. **Not byte-level** — though A-02 will
  cause two good-faith compactors to write different trailers in practice,
  which is an interoperability cost even where it is not a conformance one.
- **A-05.** Editorial placement of a non-normative-in-effect classification
  inside normative prose. No bytes, no verdicts. **Not byte-level.**

None of my five findings is byte-level. I considered inflating A-02 on the
strength of "two implementations disagree about actual bytes on disk" and
decided against it: the governing modal is lowercase-equivalent in force
(SHOULD), so both bytes are emittable by a conforming writer under both
readings and the conforming set does not move.

---

## 10. Five checks, verdict per check

1. **Tense and quantifier.** Generations are correctly distinguished in both
   hunks; the sets ("the input's unknown ignore-lane bits", "the output",
   "every feature present in the file") match the rules restated. No tense
   slip. **Passes**, except that the *evaluability* of the quantifier fails
   (A-02) and the "Neither" quantifier has a false reading (A-04).
2. **Citations resolve.** All nine checked; all pass. §10.1's count of four is
   correct and the list is closed. **Passes.**
3. **Repair sits in normative text.** Both hunks in plain prose under
   `[R-WRT-06]` and `[R-ERR-01]`. **Passes.**
4. **No contradiction in the same passage.** §20.5 clean (A-04 is an
   ambiguity, not a contradiction). §21.7 **fails**: A-05, against §21.1's
   statement of what §21.7 accounts for, §21.6's two rows, and `[R-CNF-02]`.
5. **No exhaustive claim it cannot carry.** "the four vehicles" — count and
   closure hold, membership-carriability **fails** on two of four (A-01);
   "the two it is likeliest to meet" — both are members, but the pair is in
   fact exhaustive for conforming outputs, so the hedge understates (A-01);
   "Neither obligation" — one reading false (A-04).

Findings: A-01 … A-05, below in the structured result.
