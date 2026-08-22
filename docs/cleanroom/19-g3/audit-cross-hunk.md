# Cross-hunk consistency audit — r19audit2

## 0. Access disclosure

- Charter said ten hunk files. There are **five**. Each file's own header line
  reads "Hunk N of 5". I attempted `hunk-06..10` by name and got
  `No such file or directory` for all five. I did run one glob-ls
  (`ls -la .../hunk-*.diff`) before noticing the charter's "do not list that
  directory"; it returned the same five names and nothing else. Disclosed.
- Read: `/Users/robertkleffner/Documents/GitHub/tarn/spec/tarn.md` (targeted
  `sed -n` ranges, listed below) and `hunk-01..05.diff`.
- Did NOT read: `full.diff`, `docs/`, `PLAN.md`, `OPEN-QUESTIONS.md`,
  `AGENTS.md`, `README.md`, `conformance/`, `spec/registry.json`, git history,
  the web.
- Charter names four rule-families ("what a commit may do to a layer's stored
  tiles", "when a record may be dropped", "what a compactor answers for",
  "which refusals are a file's fault"). Only two of the four are touched by the
  five hunks I have. The record-dropping and capability-refusal families appear
  only as unchanged context. Some of the charter's expected cross-hunk pairs
  therefore cannot exist in this set.

## 1. Spec ranges read

3120–3230 (§20.4 table tail, §20.5), 805–835 (§6.3 [R-CNT-08], [R-CNT-26]),
1368–1392 (§10.1), 3580–3660 (§21.7, §21.8, §21.9), 3270–3320 (§21.1),
4190–4290 (Appendix G items 3–10 + summary paragraph), 4150–4190 (Appendix G
header + items 1–2), 3790–3870 (§22.4–§23.2), 2975–3060 (§20.3 steps 4–6),
2930–2975 (§20.3 steps 2–4), 2165–2180 ([R-SLB-04]), 3520–3580 (§21.6),
2560–2585 (§18.3 [R-MTA-06]), 3258–3270 ([R-WRT-09] + the compaction Note),
405–415 ([R-ENC-06]), 4286–4357 (Appendix H).

## 2. Searches run (all whitespace-aware where the phrase could wrap)

```
grep -n "R-CNT-26" spec/tarn.md
  -> 824, 3026, 3184, 4247, 4252, 4279
grep -n "version_minor" spec/tarn.md
  -> 532, 744, 793, 798, 820, 3026, 3180, 3184, 3542, 3625, 4003, 4247, 4279
grep -n -i "unstor|un-stor|no longer stored|not stored in the live|stored-tile set|which of its tiles are stored"
  -> 606,610,1708,1740,1742,1746,1753,1773,1783,2105,2170,2937,2942,2960,2998,3029,3123,3854,3855,4044
grep -n -i "erasure|erase|deletion|delete"
  -> 2023, 3267, 3673, 3826, 3837, 3843, 3844, 3845
grep -n "reserved" spec/tarn.md          (80 hits; the register rows matter:
  F15, F35, F36, L24, L25, L31, L33, L34, L36, L43, L45, L47, R1)
grep -n "represent"                       -> only 3836 is [R-PRV-01]'s
grep -n "R-MTA-06"                        -> 2579, 3546
grep -n "R-CNF-06"                        -> 188, 2870, 3156
grep -n "R-ENC-06"                        -> 412, 2757, 3627
grep -n "^### Appendix"                   -> G at 4152, "(non-normative)"
tr '\n' ' ' | grep -oE ".{90}creator.s rules?.{110}"   (wrap-proof)
  -> three hits: Appendix G item 2, item 8 (hunk 04), summary para (hunk 05)
tr '\n' ' ' | grep -oE ".{60}compactor adopting the profile.{120}"
  -> item 2 and item 8 only
```

## 3. Grouping (by rule, not by section)

**Group A — what a compactor's trailer must and should carry.**
Hunks 01 (§20.5, the rule), 02 (§21.7, the witness account), 04 (Appendix G
item 8, the profile restatement), 05 (Appendix G summary paragraph, the
second profile restatement). Four of five hunks are one rule seen from four
places. This is the whole cross-hunk surface in this set.

**Group B — deletion is not erasure.**
Hunk 03 alone (§23.1 [R-PRV-01]). No other hunk touches it. Its cross-checks
are against untouched text: §20.3 step 4, §23.2, and the §20.5 Note at 3267.

### Rule each repair adopts, in my words

- **Hunk 01.** A compactor MUST carry the input's unknown ignore-lane bits into
  its output trailer. Separately: if the output carries *any* feature the
  compactor does not implement — by any of §10.1's four extension vehicles —
  its version_minor SHOULD be at least the input's; if it carries none, the
  plain [R-CNT-26] floor applies instead. (Trigger widened from "a carried
  ignore-lane bit is set" to "any unimplemented feature by any vehicle".)
- **Hunk 02.** §21.7 now says the register omits *two* §20.5 trailer
  obligations, and names them: the flags MUST and the version_minor SHOULD.
- **Hunk 03.** The illustration under [R-PRV-01] now says a shrink reported as
  *erasure* misleads, not a shrink reported as *a deletion*. Correct: a shrink
  IS a deletion (that is the subsection's title), and the MUST NOT bars
  representing it as erasure.
- **Hunk 04.** Appendix G item 8's two pins (version_minor at [R-CNT-26]'s
  floor, flags = 0) are creator's rules; a profile-adopting compactor carries
  input bits instead of flags = 0, and takes §20.5's floor *where it carries an
  unimplemented feature*.
- **Hunk 05.** The summary paragraph now says the version_minor pin is
  "item 8's creator's rule, not a compactor's".

## 4. Group A — do 01, 02, 04, 05 agree?

### 4a. Hunk 04 vs hunk 05 — they do not. (X-01)

Hunk 04, item 8:

> Both are creator's rules, as item 2's identifier is: a compactor adopting the
> profile carries its input's unknown ignore-lane bits forward instead, and
> **where it carries any feature it does not implement** takes §20.5's floor
> rather than `[R-CNT-26]`'s (`[R-WRT-06]`).

Hunk 05, summary paragraph:

> `version_minor` at its floor, which `[R-CNT-26]` states as a SHOULD —
> **item 8's creator's rule, not a compactor's** (§20.5)

Hunk 04's rule: item 8's version_minor pin binds a compactor **except** where
it carries an unimplemented feature. Hunk 05's rule: item 8's version_minor pin
does **not** bind a compactor, full stop. The ordinary compactor — one that
implements every feature in its input, which is the common case — is bound
under 04 and unbound under 05. §20.5 settles the direction: "*Otherwise*
version_minor follows `[R-CNT-26]`'s floor." Hunk 04 is right; **hunk 05 is
the side that should change.**

Neither the hunk-04 auditor nor the hunk-05 auditor can see this: each repair
reads correctly against §20.5 in isolation, because 05 elides the condition 04
states and 01 states.

Note also the asymmetry hunk 04 does *not* carry over: for **flags** the
displacement is unconditional (a compactor always carries input bits), for
**version_minor** it is conditional. Hunk 05 collapses both into one flat
"not a compactor's".

### 4b. Hunk 01 vs hunk 02 — "Neither obligation" ≠ "two obligations". (X-02)

§20.5 as repaired, in sequence:

1. "The output trailer MUST copy the input's unknown ignore-lane flag bits
   forward…"
2. "Where the output carries any feature the compactor does not implement …
   the output's version_minor SHOULD be at least the input's…"
3. "Otherwise version_minor follows `[R-CNT-26]`'s floor."
4. "**Neither obligation** has a witness in the output alone (§21.7)."

§21.7 as repaired: "§20.5's **two obligations** on a compacted file's trailer
(`[R-WRT-06]`) — the unknown ignore-lane bits it MUST carry forward, and the
floor its version_minor SHOULD take — are unwitnessed…"

§21.7's pair is {1, 2}. §20.5's "Neither", read by nearest antecedent, is
{2, 3} — sentences 2 and 3 are the two adjacent version_minor branches, and
sentence 1 is two sentences back with an intervening clause. Under the {2, 3}
reading the claim is **false**: the plain [R-CNT-26] floor of sentence 3 *is*
witnessed in the output alone — a verifier holding the compacted file can
enumerate the features present in it and compare. §21.7 knows this; it does not
list [R-CNT-26]'s floor among the unwitnessed, and correctly so.

The repair's own new word "obligation" is what nudges toward the {1, 2}
reading (sentence 3 is a pointer, not an obligation §20.5 imposes). So the two
hunks were plainly *written* to coordinate — and the coordination is one
sentence short of landing, because sentence 3 sits between the antecedent and
the pronoun. This is a coordination near-miss, not a wholesale contradiction,
but the cross-reference §20.5 gives the reader ("(§21.7)") resolves to a
different pair than the pronoun does. **§20.5 is the side to change**: replace
"Neither obligation" with a phrase that names both, e.g. "Neither the
carry-forward nor either floor…" or move sentence 3 after sentence 4.

Original text had the same latent slip ("Neither has a witness"); hunk 02 is
what made the count explicit and therefore checkable.

### 4c. Hunk 01's "four vehicles" — an enumeration it cannot carry. (X-03)

> Where the output carries any feature the compactor does not implement — by
> any of the four vehicles §10.1 enumerates (`[R-EXT-01]`), a carried
> ignore-lane bit and an unrecognized `tarn.` key in a record it never decoded
> being the two it is likeliest to meet — …

§10.1 (verified, lines 1372–1386) enumerates exactly four:
1. new record types (§7.3); 2. new values in reserved ranges (§10.2);
3. new ignore-lane flag bits (§6.3); 4. new standardized user-metadata keys
(§18.4).

Vehicles 3 and 4 are **conforming** under this text — §21.6 rows: "An
ignore-lane flag bit (16–31) is set → Ignored; the file is conforming"; "A
user-metadata document carries an unrecognized `tarn.`-prefixed key →
Conforming" ([R-MTA-06], §18.3 line 2571-2574).

Vehicles 1 and 2 are **violations** under this text. A record type a later
minor registers comes out of the reserved range, and F36/L25 make emitting a
reserved-range type a violation "whatever its MU bit"; F35/L24 make an MU=1 one
reject-file / reject-layer. Every other reserved-value space is likewise a
validity error: L31 (index_encoding), L33 (linearization), L34 (channel type),
L36 (layout), L43 (codec), L45 (filter), R1 (metadata encoding), F15 (trailer
reserved bytes).

So on a **conforming input** — which is the input §20.5 speaks of ("Given a
conforming input the output is a conforming file") — a compactor can meet
exactly two of the four vehicles, and the repair names them. They are not "the
two it is likeliest to meet"; they are **the only two possible**. The
four-vehicle framing widens the trigger over cases whose correct disposition is
refusal, not a version_minor bump, and it directly collides with §20.5's own
earlier MUSTs eleven lines above ("MUST NOT emit a file carrying a violation it
has detected"; "Where the table does not license a drop the compactor MUST
refuse").

### 4d. Hunk 01 — the trigger the compactor cannot evaluate. (X-04)

The repair's own example admits it: "an unrecognized `tarn.` key **in a record
it never decoded**". §20.5, twelve lines above the repair: a compactor's
"verification depth is `[R-WRT-09]`'s and **reaches no decoded content**". And
§20.4: "No commit therefore removes a layer record, or a user-metadata record
at either scope" — so the metadata record is always carried, always undecoded.

The old trigger ("Where any such bit is set") was a trailer inspection. The new
one is a predicate over content the compactor is told not to look at. Two
readings:

- **conservative**: it cannot rule out an unimplemented feature, so it always
  takes the input's minor as a floor — which erases the "Otherwise" branch;
- **literal**: the SHOULD bites only on features it knows of, so a compactor
  that never decodes metadata takes [R-CNT-26]'s floor.

Two compactors, same input, different bytes at trailer offset F−56 (Appendix A
line 4003 shows the field at [74,76) of that file). Both outputs conform
(§21.6: "version_minor is higher than this text defines → Accepted"). This one
does fork the bytes.

### 4e. Restatement hunk 01 should have swept and did not. (X-05)

§6.3 sweeps the *flags* half for compactors, in the [R-CNT-08] paragraph
(lines 812–814):

> A compactor, though its output is a new file, carries the input's unknown
> ignore-lane bits into its output trailer rather than writing flags = 0
> (§20.5, `[R-WRT-06]`).

The very next paragraph, [R-CNT-26] (lines 820–824), states the version_minor
rule and enumerates its actors — **and the compactor is not among them**:

> A writer SHOULD emit the lowest version_minor that defines every feature
> present in the file — for a file expressible under this text, 0 — and **an
> appender** the maximum of that floor and the prior trailer's minor…

A compactor "satisfies every writer requirement for the bytes it produces
(`[R-CNF-06]`)", so [R-CNT-26] reaches it as a writer and gives it the plain
floor unconditionally. §20.5 branch 1 now says otherwise. The parallel
compactor sentence that §6.3 already carries for flags is missing for
version_minor. Hunk 01 changed the rule in §20.5 and left [R-CNT-26]'s own
statement of it un-swept.

(Checked and *not* a defect: hunk 01 deleted "as it does for an appender
(§20.3 step 6)" from the Otherwise branch. Good deletion — an appender's rule
is max(floor, prior minor), not the plain floor, so the old clause equated two
different rules. §20.3 step 6 at line 3026 still reads "version_minor per
`[R-CNT-26]`", which is correct for an appender.)

### 4f. Hunk 05's un-annotated neighbour. (X-07)

Hunk 05 annotates one list entry with a compactor carve-out and leaves the
entry three words later un-annotated, although Appendix G item 2 carries
exactly the same carve-out in exactly the same words:

> `version_minor` at its floor … — item 8's creator's rule, not a compactor's
> (§20.5); **a derived `file_id`, where §9.3 states only advice**; …

Item 2: "This is a creator's rule: a compactor adopting the profile takes
`[R-WRT-06]`'s fresh draw instead". Marking one and not the other, inside one
sentence, tells a reader by contrast that the file_id pin has no compactor
carve-out. It has one, and it is the older of the two.

## 5. Group B — hunk 03

The repair itself is **correct and lands in normative text** (line 3836–3838,
no ">" prefix, governed by [R-PRV-01] at 3839). "a shrink reported as a
deletion" was the wrong illustration for a subsection titled "Deletion is not
erasure" and for a MUST NOT that bars representing a commit "as erasure of it".
The repaired clause now mirrors the MUST NOT's own word. Checked every other
occurrence of erase/erasure/deletion (2023, 3267, 3673, 3843–3845): none
restates this rule with the old word. Line 3267 is a ">" Note ("logical
deletion supersedes bytes but leaves them in the file as slack") — consistent
in terminology, non-normative, nothing to sweep.

**But the sentence three lines above it, untouched, is a false closed count.**
(X-06)

> A commit removes sample data **two ways** — superseding it, and a shrink that
> de-addresses tiles (§20.3 step 4) — and a dropped ancillary record's extent
> (§20.4) goes the same way; no commit removes a layer at all.

There is a third way, and the document states it twice:

- §20.3 step 4 (line 2942): "entries for tiles that **become unstored** written
  as the sentinel" — un-storing an addressed tile, which is neither a supersede
  (no new bytes) nor a shrink (the tile stays addressed).
- §23.2 (lines 3853–3856), the very next subsection, citing §23.1 back:
  "a sentinel entry (§15.2) marks each addressed tile not stored in the live
  generation — **a tile unstored by a later commit leaves its earlier payload in
  the file as slack (§23.1)**".

§23.2 points at §23.1 for a case §23.1's count excludes. [R-PRV-01]'s MUST NOT
itself is safely quantified ("any commit that makes sample data unreachable"),
so no rule is lost — but the enumeration in front of it is wrong, and it is the
enumeration a reader uses to decide which commits the MUST NOT reaches.

## 6. Citation ledger

| Cited in | Target | Verdict |
|---|---|---|
| h01 | §10.1 / [R-EXT-01] "four vehicles" | PASS (1372–1386; exactly four, [R-EXT-01] at 1386) — but see X-03 on what it licenses |
| h01 | [R-CNT-26] "the overstatement it names" | PASS (823–824: "a higher minor than needed … misstates the file's feature floor to tooling") |
| h01 | [R-CNT-26] "'s floor | PASS as to existence (820–822); actor list incomplete, X-05 |
| h01 | [R-CNT-08] / §6.3 flags = 0 | PASS (808–810) |
| h01 | §21.7 for "Neither obligation" | **FAIL** — §21.7 names a different pair, X-02 |
| h01 | [R-WRT-06] (para terminator) | PASS (3190) |
| h01 | §7.2, [R-WRT-09], [R-CNF-06], [R-WRT-01], [R-LIF-01], [R-LIF-03] | context, unchanged; spot-checked [R-CNF-06] at 188/2870/3156 — PASS |
| h02 | [R-WRT-06] | PASS |
| h02 | [R-LIF-01] "for the same reason" | PASS (§21.7 para 2 already classes it as history) |
| h02 | §9.7 | PASS |
| h02 | [R-ENC-06] (unchanged tail) | PASS (412) |
| h02 | [R-ERR-01] (para terminator) | PASS (3632) |
| h03 | [R-PRV-01] | PASS (3839) |
| h03 | §20.3 step 4, §20.4, [R-CNT-21], §9.6 | PASS individually; the *set* is incomplete, X-06 |
| h04 | [R-CNT-26] | PASS |
| h04 | [R-WRT-06] | PASS |
| h04 | §20.5 "'s floor" | PASS |
| h04 | "as item 2's identifier is" | PASS (item 2, 4184–4186, uses the identical "creator's rule" construction) |
| h05 | §20.5 | **FAIL as applied** — §20.5's "Otherwise" branch contradicts "not a compactor's", X-01 |
| h05 | [R-CNT-26] "states as a SHOULD" | PASS |
| h05 | §9.3, [R-ENC-14], [R-CNT-03], [R-SLB-05], [R-CNT-14], [R-TYP-10] | unchanged context, not re-verified |

## 7. Normativity of each landing site

- h01 → §20.5 body prose, no ">". Normative. Governed by [R-WRT-06].
- h02 → §21.7 body prose, no ">". Normative, [R-ERR-01]. (§21.1: §21.7 is
  outside the register's completeness clause, which is what makes an
  enumeration there a description rather than a rule — relevant to X-02's
  severity, not to its existence.)
- h03 → §23.1 body prose, no ">". Normative, [R-PRV-01]. Good — this is the
  one place a repair of this kind has historically gone wrong, and it did not.
- h04, h05 → **Appendix G, headed "(non-normative)"** (line 4152), and the
  appendix says of itself "It adds no requirement to any actor: a writer
  ignoring it is fully conforming". So X-01 and X-07 are defects in a profile
  definition, not in a normative rule — which is exactly why neither is
  byte-level under the discriminator, even though two profile-claiming
  compactors would emit different bytes.

## 8. Byte-level determinations

| # | Byte-level | Why |
|---|---|---|
| X-01 | no | Appendix G is non-normative and adds no requirement to any actor; both version_minor values yield conforming files (§21.6). Two *profile-claiming* compactors fork at F−56, but the conforming-emittable set does not move. |
| X-02 | no | Affects what §20.5 asserts about witnesses, not what any actor emits or any verifier decides. |
| X-03 | no | The disputed files carry register-row violations (F36/L25/L43/…), so [R-CNF-05] bars every conforming writer from emitting them under both readings. The emittable set does not move. |
| X-04 | **yes** | Conservative and literal compactors emit different version_minor at trailer offset F−56 for the same conforming input; both outputs are conforming, and nothing in the document resolves which the SHOULD asks for, because the predicate ranges over content [R-WRT-09] forbids the actor to reach. |
| X-05 | no | §20.5 is the specific rule and [R-CNT-26] the general one, so a careful implementer resolves it; the defect is findability, and its byte exposure is the same F−56 field X-04 already claims. |
| X-06 | no | [R-PRV-01]'s MUST NOT is quantified over "any commit", so no commit escapes it under either reading; the defect is a wrong enumeration, not a changed licence. |
| X-07 | no | Non-normative appendix; item 2 states the carve-out plainly, so no byte is actually at stake. |
