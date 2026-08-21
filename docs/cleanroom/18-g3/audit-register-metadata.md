# Round 18 repair audit — hunks 5 and 6 (§21 register prose)

Auditor scope: hunk-05.diff (§21.5 prose, lands at spec/tarn.md:3486) and
hunk-06.diff (§21.7 prose, lands at spec/tarn.md:3596).

## 0. Disclosure — everything I read and ran

Files opened with Read:
- `/private/tmp/claude-501/-Users-robertkleffner-Documents-GitHub-tarn/2c60df09-4efe-4196-a7da-930efc26640f/scratchpad/round18-audit/hunk-05.diff`
- `/private/tmp/claude-501/-Users-robertkleffner-Documents-GitHub-tarn/2c60df09-4efe-4196-a7da-930efc26640f/scratchpad/round18-audit/hunk-06.diff`
- `/Users/robertkleffner/Documents/GitHub/tarn/spec/tarn.md`, in these windows:
  - 140–159 (`[R-CNF-02]` tail, conforming-reader head)
  - 170–219 (`[R-CNF-04]`, `[R-CNF-05]`, `[R-CNF-06]`, §2.4 verifier verdicts)
  - 258–288 (`[R-CNF-12]`, `[R-CNF-10]` / §2.5)
  - 470–499 (§4.6, `[R-ENC-11]`, `[R-ENC-12]`)
  - 876–901 (§7.1 tail, `[R-CNT-25]`)
  - 1340–1368 (`[R-LIF-08]`)
  - 1418–1437 (`[R-EXT-03]`, §10.4 head)
  - 1908–1925 (`[R-SER-07]`, §14.4 head)
  - 2240–2258 (`[R-COD-03]`, `[R-COD-04]`, `[R-COD-05]`)
  - 2395–2564 (`[R-COD-11]` tail, §18.1, §18.2 entire: `[R-MTA-03]`,
    `[R-MTA-09]`, its Note, `[R-MTA-04]`, `[R-MTA-05]`, `[R-MTA-10]`)
  - 2891–3019 (§20.3 the append procedure, steps 1–4 and the grow/shrink text)
  - 3230–3349 (§20.5 tail, §21.1 entire, §21.2 head)
  - 3400–3679 (§21.3 tail, §21.4 entire, §21.5 entire, §21.6 entire,
    §21.7 entire, §21.8, §21.9 and its Note, §21.9 hard-limits head)
  - 4310–4327 (the verifier checklist near the document's end)

Commands run (all read-only, all against spec/tarn.md only):
```
grep -n "R-MTA-09" spec/tarn.md
grep -n "R-MTA-10\|R-MTA-03\|R-CNT-25\|R-CNF-12" spec/tarn.md
grep -n "20.3 " spec/tarn.md | head -40 ; grep -n "^#### 20\|^### 20" spec/tarn.md
grep -n "T14\|T3\b" spec/tarn.md
grep -n "R-COD-04\|R-SER-07" spec/tarn.md
grep -n "R-CNF-02\|R-CNF-10\|R-CNF-11\b" spec/tarn.md | head -30
tr '\n' ' ' < spec/tarn.md | grep -o -E '.{140}(size bound|the bound|its own choosing|declines to decode|declines the decode).{140}' | head -40
awk 'NR>=3516 && NR<=3565' spec/tarn.md | grep -c "bound\|16 MiB\|size"
awk 'NR>=3521 && NR<=3536' spec/tarn.md | grep -o "^| [^|]*"
tr '\n' ' ' < spec/tarn.md | grep -o -E '.{120}§21\.6 lists.{120}'
tr '\n' ' ' < spec/tarn.md | grep -o -E '.{100}capability refusals.{120}'
```
The `tr '\n' ' ' | grep -o -E` form was used wherever the phrase could span the
hard wrap; the wrap defeated a plain line grep for "declines the decode" and
"§21.6 lists", which is why those searches were run whitespace-normalised.

I did **not** open full.diff, any other hunk file, docs/, PLAN.md,
OPEN-QUESTIONS.md, AGENTS.md, README.md, conformance/, spec/registry.json, git
history, or the web. I did not list the audit directory. No access-rule breach.

---

## 1. Hunk 5 — §21.5 prose, the size-bound carve-out

### 1.1 The current text, verbatim (spec/tarn.md:3485–3501)

```
Outcome: ignore-record — the record is skipped as though absent and
decoding of stored data is unaffected. Readers SHOULD report the
loss; silent metadata loss defeats the record's purpose. User
metadata is quarantined (`[R-CNT-25]`): every way its document can
be unreadable takes this outcome, whatever the containing scope —
as a violation in the rows below, except at an experimental-range
encoding, where no document rule attaches and §21.6 records the
defined non-violation (`[R-MTA-10]`), and except where a reader or
verifier declines the decode on the size bound, which `[R-MTA-09]`
makes that actor's capability and not a fact about the file. Encoding 0 and a reserved-range
value are unassigned too, and R1 registers both as violations: what
`[R-MTA-10]` withdraws is the document's content rules, never the
encoding byte's own value set (`[R-MTA-03]`). Every row
here is a violation all the same: the outcome bounds a reader's
blast radius and never makes the file conforming (`[R-CNF-12]`);
§21.6 lists the ignore-record conditions that are not violations.
10 conditions.
```

### 1.2 The rule the repair adopts, in my own words

For an implementation: *a document that exceeds the size bound the decoding
actor chose (a bound that MUST be at least §21.9's 16 MiB user-metadata
guarantee) is ignore-record for that actor, but the file is not thereby
nonconforming and no §21.5 row is charged against it.* Concretely: a verifier
meeting a 20 MiB user-metadata document may decline the decode, MUST NOT
certify, MUST NOT report *nonconforming* on that ground, and reports *cannot
establish* if it found nothing else; a reader may take ignore-record for that
record and keep serving the file's stored data.

### 1.3 Check 1 — tense and quantifier

Generation: no generational content at all here. The passage speaks about the
file as it stands, not about a superseded state. Nothing to get wrong.

Set ranged over: the carve-out's quantifier is "where a reader **or** verifier
declines" — i.e. it fires for either actor. The requirement it restates,
`[R-MTA-09]` (spec/tarn.md:2454–2478), states the reader arm and the verifier
arm with different consequences:

- reader: "a reader instead decodes with a bound of its own choosing, no
  smaller than §21.9's user-metadata guarantee, and a document exceeding that
  bound is ignore-record like any other it cannot read."
- verifier: "A **verifier** that declines to decode a document on the bound
  above cannot establish that document's conformance and MUST NOT certify the
  file … the bound is that verifier's capability and not a limit on validity
  (`[R-CNF-10]`), so the decline is not a finding that the file is
  nonconforming and a verifier MUST NOT report it as one."

Verifier arm: exact match, word for word ("that verifier's capability" /
"that actor's capability"; "not a limit on validity" / "not a fact about the
file"). Reader arm: `[R-MTA-09]` does not itself say the reader's decline is
"not a fact about the file"; it only assigns the outcome. I chased whether that
makes the repair an overclaim and concluded it does not, because the same
requirement's clause "the bound is that verifier's capability and not a limit on
validity (`[R-CNF-10]`)" is a statement about *the bound* — the bound
introduced one sentence earlier as the reader's "bound of its own choosing" —
and because `[R-CNF-10]` (spec/tarn.md:273–278, restated at §21.9:3623–3631)
is itself general: "Every limit that affects which files are valid or which
files a conforming reader accepts lives in this specification, never only in an
implementation," plus §21.9's "A file exceeding any of these remains
conforming, and a reader MAY decline it." A reader's private bound is therefore
not a validity limit under normative text, not merely under §18.2's Note.
**Not reported.** Recorded here because the reader arm is one step of inference
away from `[R-MTA-09]`'s literal words and a future editor should know it was
looked at.

Scope range: the sentence ranges over "whatever the containing scope" —
top-level record (file scope) and layer sub-record (layer scope). I checked
that `[R-MTA-09]` reaches both. §18.1 `[R-MTA-01]` (3417–3420): "A file MAY
carry one user-metadata document at file scope, and each layer MAY carry one of
its own." §18.2 and `[R-MTA-09]` speak of "a document" and "a user-metadata
record" with no scope restriction, and §21.9's guarantee row reads "decoded
size of one user-metadata document" — also scope-neutral. **The carve-out
applies at every scope the sentence ranges over. Passes.**

### 1.4 Check 2 — citations resolve

| Citation in the repaired sentence | Where I read it | Verdict |
|---|---|---|
| `[R-MTA-09]` | spec/tarn.md:2454–2478 (§18.2) | **Passes.** Contains both the reader bound ("no smaller than §21.9's user-metadata guarantee … ignore-record like any other it cannot read") and the verifier capability framing ("the bound is that verifier's capability and not a limit on validity … a verifier MUST NOT report it as one"). It is the correct governing rule for the carve-out. |
| `[R-CNT-25]` (context, unchanged) | spec/tarn.md:878–897 (§7.1) | Passes as the quarantine cite. Note in §1.7 below about its own enumeration. |
| `[R-MTA-10]` (context, unchanged) | spec/tarn.md:2537–2557 | Passes: withdraws the *document rules* at an unassigned encoding, leaves the structural checks including "the encoding byte's own value set (`[R-MTA-03]`)". |
| `[R-MTA-03]` (context, unchanged) | spec/tarn.md:2437–2452 | Passes: 0 invalid, 1/2 assigned, 3–0x7F reserved, ≥0x80 experimental. |
| `[R-CNF-12]` (context, unchanged) | spec/tarn.md:258–266 | Passes: an outcome class never makes the file conforming; a reader MAY reject on any violation. |
| §21.6 (context, unchanged) | spec/tarn.md:3516–3565 | **Fails as used.** See §1.6. |
| §21.9's guarantee, reached via `[R-MTA-09]` | spec/tarn.md:3633–3654 | Passes: "decoded size of one user-metadata document | 16 MiB", and "A file exceeding any of these remains conforming". |

I also opened §2.4's verifier definition (spec/tarn.md:189–223) because it
independently enumerates the *cannot establish* grounds, and found the
size-bound decline already listed there: "or when it declines to decode a
user-metadata document (`[R-MTA-09]`)". That corroborates the repair's verifier
arm from a second normative site.

### 1.5 Check 3 — the repair sits in normative text

§21.5's prose is plain body text, no `>` prefix on any line of 3485–3501; I
confirmed by reading the raw lines. It is inside the register, which §21.1
(3262–3292) makes normative for completeness. The rule the repair restates is
independently normative at §18.2 `[R-MTA-09]` and at §2.4. So this is a
restatement in normative prose of a normative rule stated elsewhere — the good
case, not the blockquote signature.

I grepped the distinctive words of the rule (whitespace-normalised, because
"declines the decode on the size bound" spans the hard wrap at 3492/3493):
`(size bound|the bound|its own choosing|declines to decode|declines the decode)`
returns exactly three substantive sites — §2.4:202, `[R-MTA-09]`:2461–2474, and
the repaired §21.5 — plus two false hits ("bounds rows", "a vector at the
bound"). **No orphan statement in a `>` block; nothing normative left saying the
old thing. Passes.**

### 1.6 Check 4 — contradiction in the same passage, including untouched text

This is where hunk 5 fails.

The repair adds a second exception, and the exception it adds is *an
ignore-record condition that is not a violation*. Two sentences later, in text
the repair did not touch, §21.5 closes with:

> "§21.6 lists the ignore-record conditions that are not violations."

Definite article, plural: an exhaustive pointer. Before the repair it was true —
§21.5's prose named exactly one non-violation, the experimental-range encoding,
and §21.6 carries a row for it (spec/tarn.md:3532: "A user-metadata record
declares an experimental-range (≥ 0x80) document encoding | Ignored
(ignore-record); the file is conforming …"). After the repair it is not.

I enumerated every §21.6 row to be sure. `awk 'NR>=3521 && NR<=3536' | grep -o
"^| [^|]*"` gives 14 rows: sentinel index entry; coordinate outside extents;
dimension extent 0; zero layers; experimental record type MU=0; ignore-lane flag
bit; higher version_minor; unclaimed bytes/slack; mixed bool and numeric
channels; **experimental-range document encoding**; unrecognized `tarn.` key;
standardized key out of scope; trailer mimic; compressing codec whose decoded
size differs from stored length. A word-frequency check over §21.6 entire
(`grep -c "bound\|16 MiB\|size"`) returns 2 hits, both the "decoded size"
phrases in the last row — **no row and no prose sentence anywhere in §21.6
mentions a size bound, a 16 MiB guarantee, or a declined decode.**

`[R-MTA-09]` makes the size-bound case unambiguously an ignore-record
condition ("a document exceeding that bound is ignore-record like any other it
cannot read"), and the repair makes it unambiguously not a violation ("not a
fact about the file"). So §21.5 now names one that §21.6 does not list, and the
closing sentence is a sentence written to be true only under the old wording —
exactly the shape check 4 is aimed at.

I steelmanned the defence and record it: §21.6's own intro is "These are
defined behaviors, not errors. A reader that treats any of them as a failure is
the nonconforming party" (3518–3519), and that second sentence is *false* of
the size-bound case, because §21.9 expressly lets a reader decline an
over-guarantee file ("a reader MAY decline it — at the whole file"). So the
size-bound case genuinely does not belong in §21.6's table as that table is
written. I also noted the repair itself routes the second exception to
`[R-MTA-09]` rather than to §21.6, unlike the first. That defence establishes
where the fix should go — §21.5's pointer, not §21.6's table — but it does not
rescue the pointer, which still asserts that §21.6 has them all.

I also checked the adjacent exhaustive claim it might have broken and it holds:
§21.9:3646–3649 says "the two capability refusals §21.6 names, a foreign format
major and an unimplemented MU = 1 type, are not this ground". §21.6's paragraph
at 3549–3558 does name exactly two, and it scopes them as "**structural** cases
… conforming files a reader nevertheless refuses". The size-bound decline is a
resource case at record granularity, not a structural whole-file refusal, so
the count "two" survives the repair. **§21.9 passes.**

Other contradictions I looked for in the passage and did **not** find:
- A MUST elsewhere in §21.5 that the carve-out's new licence lets an actor
  violate: none. §21.5 carries no MUST at all; its rows are declarative.
- "Every row here is a violation all the same" (3497–3498): still true. The
  carve-out adds no row. R1–R10 are ten rows and 3501 still says "10
  conditions"; §21.8:3616 still says "121 conditions over 273 instances" and is
  unaffected because no row moved.
- Whether the carve-out lets a writer off. It does not: `[R-CNF-02]`
  (spec/tarn.md:140) — "conformance … is a predicate on bytes: it does not
  depend on any reader, writer, or environment" — forecloses the reading that a
  20 MiB document carrying, say, an R9 duplicate key stops being a violation
  because some actor declined the decode. I specifically tested that misreading
  because the carve-out's trigger is actor-relative while the clause it excepts
  is a file predicate; `[R-CNF-02]` plus the carve-out's own tail ("not a fact
  about the file") close it. **Not reported.**
- §21.1's "where a row and the rule it cites diverge, the rule governs"
  (3277–3278) and its extension to §21.6's entries (3290–3292): applied to
  D-01, the governing rules (`[R-MTA-09]`, §21.9, §2.4) all agree with the
  repair, so the *repair* is right and the untouched pointer sentence is the
  wrong text. That is the answer to the charter's "say which of the two is
  wrong": the closing pointer sentence of §21.5 is wrong, not the carve-out and
  not any §21.6 row.

### 1.7 Check 5 — exhaustive claims

Words promising completeness in and around the repaired text:

- "**every** way its document can be unreadable takes this outcome" — with two
  exceptions carved from the violation clause, I enumerated the ways that
  remain and matched them to rows: failed extent CRC → R2; decode failure under
  an assigned encoding → R3; encoding-2 frame breach → R4; content rules → R5,
  R6, R7, R8, R9, R10; encoding 0 / reserved → R1. Carved out: experimental
  encoding; over-bound decline. I could construct no thirteenth way. A reader
  lacking a zstd decoder is not one: `[R-MTA-03]`:2447–2452 makes both assigned
  encodings core, so such software is not a conforming reader. **Holds.**
- "**whatever** the containing scope" — checked in §1.3. Holds.
- "§21.6 lists **the** ignore-record conditions that are not violations" —
  fails; this is D-01.
- "**Every** row here is a violation all the same" — holds.
- "the **two** capability refusals §21.6 names" (§21.9) — holds; see §1.6.
- "R1 registers **both**" (encoding 0 and reserved) — checked against R1 at
  3505, which covers "a document encoding of 0, or a reserved-range value
  (3-0x7F)". Holds.

### 1.8 Overshoot / undershoot / new ambiguity for hunk 5

- Overshoot: the carve-out is narrow — one named ground, one cited rule, one
  named consequence. It does not widen any licence beyond `[R-MTA-09]`. No.
- Undershoot: it does leave D-01's pointer sentence standing, which is the
  finding.
- New ambiguity: two candidates examined and rejected. (a) Whether the
  exceptions attach to "as a violation in the rows below" or to "takes this
  outcome" — under the second reading the verifier's decline would not take
  ignore-record, which is arguably *more* accurate for a verifier
  (`[R-MTA-09]` gives it a verdict, not an outcome class), so neither reading
  produces a wrong rule. (b) The actor-relative trigger, closed by
  `[R-CNF-02]` as above.
- Restatement the repair should have swept: `[R-CNT-25]` at spec/tarn.md:
  888–894 enumerates "each way a user-metadata record's document can be
  unreadable once its framing has been read — a failed extent CRC, an
  unimplemented or invalid encoding, a decode failure, or content violating the
  document's own rules". That list does not include the size bound. I did
  **not** report it: the gap predates this repair (`[R-MTA-09]` already put the
  bound outside that list), the outcome is ignore-record under both, and no
  reading of either text changes an implementation's behaviour. Recorded so the
  next round knows it was checked.
- Cosmetic, not reported: line 3494 breaks the file's hard wrap (it runs to
  ~86 columns where the surrounding lines wrap near 66), and the inserted
  clause now sits between "at an experimental-range encoding" and the sentence
  whose "unassigned **too**" anaphorically depends on it.

---

## 2. Hunk 6 — §21.7 prose, T3 vs T14

### 2.1 The current text, verbatim (spec/tarn.md:3596–3607)

```
reader parses as a record sequence (§7.4's closing Note);
§20.3 step 4's bar on a declaration change is witnessed only where
the affected tiles remain stored *and* the change reaches a byte §14
structurally constrains — a padding position, a pad bit, or a boolean
byte — where §21.4's content rows fire; a change that reaches the
decoded size or the codec instead is witnessed by T3 or T14, which
test a length rather than the decoded image's content — T14 the
entry's declared length, T3 the decoded payload's own; and a
commit that supersedes every tile it would have damaged leaves the
live state clean, so the bar is unwitnessed there for the same
reason `[R-LIF-01]` is: it is a property of the prior generation,
which §9.7 does not reconstruct;
```

### 2.2 The rule the repair adopts, in my own words

For an implementation: *T14 is a check on the tile-index entry's `length`
field against the declaration-derived decoded size, and is gated on codec 1;
T3 is a check on the byte length the decode actually produced against the same
declaration-derived decoded size. Neither inspects sample content. An
implementer building either check reads a different quantity: T14 needs no
payload fetch, T3 needs a completed decode.*

### 2.3 Check 1 — tense and quantifier

Generation: the passage is generation-sensitive throughout, and the repair
landed inside the one clause that is not. The surrounding sentence is careful —
"where the affected tiles remain stored", "a property of the prior generation"
— and matches §20.3 step 4's own tense, which I read at spec/tarn.md:
2951–2962: "for any tile that layer stores **in the generation this commit
supersedes** … The tense is the prior generation's (§3.1 defines *stored*
against a generation)". The repaired clause introduces no generation of its own
(it describes what two register rows test), so it cannot shift the tense.
**Passes.**

Quantifier: "T14 the entry's declared length, T3 the decoded payload's own" is
a closed two-item mapping. Checked in §2.5.

### 2.4 Check 2 — citations resolve

No requirement identifiers appear in the repaired words; the citations are the
two row labels. I opened both rows and both governing rules.

| Reference | Where | Verdict |
|---|---|---|
| T3 | spec/tarn.md:3458 — "The decoded payload's byte length is not exactly the tile's decoded size derived from the layer's declarations", governing `[R-SER-07]` (R-COD-08); instances all of the form "payload longer / payload shorter" | **Passes.** T3 is the decoded payload's own length. |
| `[R-SER-07]` | spec/tarn.md:1914–1921 — "a reader MUST treat a decoded payload whose byte length is not exactly that decoded size as a validity error at tile scope" | **Passes.** Confirms T3's subject is the decoded payload's length. |
| T14 | spec/tarn.md:3469 — "Codec 1 (none) declared and a non-sentinel index entry's length differs from the tile's decoded size", governing `[R-COD-04]`; instances all "length longer / length shorter" | **Passes.** T14 is the index entry's length field. |
| `[R-COD-04]` | spec/tarn.md:2246–2250 — "The index entry's length therefore MUST equal the tile's decoded size … checkable from the entry and the layer record alone, before any payload fetch" | **Passes.** Confirms T14's subject is the entry's declared length and that it needs no decode. |
| §20.3 step 4 | spec/tarn.md:2934–3004 | Passes: its barred list includes "the decoded size … or the codec and filter that produced the stored bytes", which is what the sentence's "decoded size or the codec" branch refers to. |
| §9.7 / `[R-LIF-01]` (context) | reached at spec/tarn.md:1340–1360 (`[R-LIF-08]`) | Passes as used: the verifier's walk does not reconstruct history. |

**The distinction is real and correctly assigned, not swapped.** The repair
corrects a genuine error in round 16's text, which said both rows "read the
index entry rather than the decoded image" — false of T3, which by `[R-SER-07]`
cannot fire without a completed decode.

### 2.5 Check 3 — normative placement

§21.7 is plain body text (no `>` prefix anywhere in 3567–3612) closing with
`[R-ERR-01]`. It is descriptive of rows that live in §21.4, and §21.1:3277
makes the row the restatement and the rule the governor, so nothing normative
depends on this clause being right — but nothing normative contradicts it
either. I grepped the whole document for other places that characterise these
rows: `grep -n "T14\|T3\b"` returns exactly four lines — 3458 (the T3 row),
3469 (the T14 row), and 3601/3603 (this clause, split across the hard wrap).
`grep -n "R-COD-04\|R-SER-07"` returns nine lines, of which the only other
characterising site is §21.6:3536, "codec 1's equality is `[R-COD-04]`'s
subject", which agrees with the repair. **No restatement anywhere that the
repair should have swept and did not. Passes.**

### 2.6 Check 4 — contradiction in the same passage

The one I found and am reporting is the sentence's own subject clause, which
the repair rewrote the predicate of and left the subject of. The clause says
"a change that reaches the decoded size **or the codec** instead is witnessed
by T3 or T14, which test a length …". Worked through both directions of a
codec re-declaration on a layer with prior-generation stored tiles — the case
§20.3 step 4 bars:

- **codec 2 → codec 1.** Stored bytes are a DEFLATE stream of length L;
  decoded size S. Under codec 1 the reader compares L against S. T14 fires
  (unless L = S by coincidence). The repaired clause is right here.
- **codec 1 → codec 2.** Stored bytes are the raw filtered image. Under codec
  2 the reader attempts a raw RFC 1951 decode of image bytes. T14 cannot fire —
  its row is gated on "Codec 1 (none) declared". T3 cannot fire either — there
  is no decoded payload to measure a length of. What fires is T25 (3480, "The
  stored bytes are a malformed stream that fails to decode", `[R-COD-08]`), or
  T15 (3470) if the image happens to open like a wrapper. Under a 1 → 3 change
  it is T17 (missing zstd magic); under 1 → 4, T23/T25.

So for one of the two directions of the codec branch, and for every
non-deflate target, the named witnesses are the wrong rows, and the repair's
new predicate — "which test a length rather than the decoded image's content" —
is what makes the mismatch legible: the rows that actually witness a codec
change test *stream structure*, not a length. Round 16's wording ("read the
index entry rather than the decoded image") was equally wrong about the codec
branch, so the repair did not create this; it rewrote the clause that carries
it and did not fix it. That is an undershoot, and I report it as D-02.

Other contradictions I looked for in §21.7 and did **not** report:
- The "witnessed **only** where … *and* the change reaches a byte §14
  structurally constrains" that immediately precedes, versus "a change that
  reaches the decoded size or the codec **instead** is witnessed by T3 or
  T14". Read strictly, the second clause falsifies the "only". I judged this
  pre-existing and outside the repair: "instead" plus the semicolon list is
  readable as scoping the "only" to the §21.4 *content*-row way of witnessing,
  and neither the deleted nor the inserted words touch the "only".
- Whether T3 and T14 are a specialization pair §21.1:3283–3286 should list
  (under codec 1 both fire on the same file). Not listed there — F1/F6/F8,
  F35/F36, L24/L25 are the listed pairs. Pre-existing, untouched by the repair,
  and not within this charter.
- The ragged wrap at 3607–3609 ("… fixed field widths are not / a state a /
  file can be in") is context in the hunk, not repaired text.

### 2.7 Check 5 — exhaustive claims in the repaired words

- "**T14** the entry's declared length, **T3** the decoded payload's own" — a
  closed two-item assignment. Falsification attempt: read both rows and both
  governing rules (§2.4 above). Cannot be falsified; the assignment is correct
  in both directions and is not swapped.
- "test **a length** rather than the decoded image's content" — true of both
  rows; T3's instances are all "payload longer/shorter" and T14's all "length
  longer/shorter", i.e. magnitude comparisons of lengths, per §21.1:3307–3311.
  Neither row's condition text mentions a sample value.
- "**the** decoded image's content" — the definite article here is a contrast
  term, not a completeness claim; §21.4's content rows (T2, T4, T5, T26) are
  what it points away from and they are the content rows.
- "witnessed by **T3 or T14**" — this is context, not repaired text, and it is
  what D-02 is about.

---

## 3. Byte-level assessment

**D-01.** The disputed file is a conforming file carrying a well-formed
user-metadata document larger than 16 MiB. §21.9:3644 settles that it is
conforming ("A file exceeding any of these remains conforming"), so a
permissive reading lets a writer emit it and so does the restrictive one —
`[R-CNF-05]` bars nothing extra. On the verdict side, a verifier that read the
closing pointer as exhaustive might be tempted to report *nonconforming*, but
`[R-MTA-09]` says in terms "a verifier MUST NOT report it as one", and
§21.1:3277 makes the rule govern over the register's restatement, so no
competent verifier reaches that verdict. **Not byte-level.** It is a
completeness defect in the register's navigation text.

**D-02.** §21.7 is by construction an account of what has *no* witness; it
assigns no obligation and no outcome. The rows that actually fire on a 1 → 2
codec change (T25, T15, T17, T23) are in the register with their own detectors
and detection points, and a reader implements the rows, not §21.7's summary.
No byte a writer may emit and no accept/reject verdict moves. **Not
byte-level.**

Neither finding is inflated to byte-level and neither is suppressed: I could
not construct two competent implementations differing on a byte or a verdict
from either.

---

## 4. Verdict

Hunk 6's core repair is correct: T3 and T14 are correctly distinguished and
correctly assigned, verified against both rows and both governing rules. Hunk
5's core repair is correct: `[R-MTA-09]` says what is claimed, at both scopes.
Each hunk carries one collision with text it did not touch — D-01 in §21.5's
closing pointer, D-02 in §21.7's subject clause. Both are reported below.
