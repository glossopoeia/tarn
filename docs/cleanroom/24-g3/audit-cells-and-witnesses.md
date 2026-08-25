# Repair audit — hunks 3 and 4 (auditor B)

Working transcript. Verbatim record of what was read, what was run, and what
was concluded. Written to be checkable, not readable.

## 0. Disclosure

Read:
- `/private/tmp/.../r24audit-b/hunk-03.diff`
- `/private/tmp/.../r24audit-b/hunk-04.diff`
- `/Users/robertkleffner/Documents/GitHub/tarn/spec/tarn.md` (many passages,
  listed below)

Ran: `wc -l`, `sed -n`, `grep -n`, `awk`, and two `python3 -c` whitespace-
normalising searches, all against `spec/tarn.md` only.

Did NOT read: `full.diff`, hunk-01/02, `docs/`, `PLAN.md`,
`OPEN-QUESTIONS.md`, `AGENTS.md`, `README.md`, `conformance/`,
`spec/registry.json`, git history, the web. Did not list the hunk directory.

**Unrequested context appeared before I began.** A system-reminder block was
placed in my context carrying (a) a pointer from `CLAUDE.md` to `AGENTS.md`
and (b) an index of the maintainer's private memory notes with one-line
descriptions, plus a date and the user's email. I did not open any file it
named and I have not used its contents as evidence; nothing below is reached
because that material suggested it. Disclosing its appearance, not its
contents.

Spec passages read in full:
- §6.2 trailer layout + `[R-CNT-05]`, `[R-CNT-06]` (lines 735–780)
- §6.3 `[R-CNT-07]`, `[R-CNT-08]`, `[R-CNT-26]` (lines 786–830)
- §9.1 `[R-LIF-01]`, §9.2 `[R-LIF-02]`, §9.3 `[R-LIF-03]` (lines 1155–1245)
- §14.2 `[R-SER-02]`, `[R-SER-08]` + its Rationale/Note (lines 1830–1880)
- §14.3 `[R-SER-03]` + Note (lines 1886–1905)
- §14.5 `[R-SER-05]` + Example/Rationale (lines 1952–1975)
- §17.3 `[R-COD-09]`, `[R-COD-10]` + Example/Rationale (lines 2355–2400)
- §18 `[R-MTA-04]`, `[R-MTA-05]`, `[R-MTA-10]` (lines 2530–2600)
- §20.3 step 4 (lines 2960–3040)
- §20.5 `[R-WRT-06]`, `[R-WRT-07]` (lines 3192–3270)
- §21.1 in full (lines 3319–3396)
- §21.3 tail, §21.4 in full, §21.5 in full, §21.6 in full (3480–3630)
- §21.7 in full, §21.8, §21.9 head (3630–3740)
- §24 `[R-VEC-01]`…`[R-VEC-04]` + Note (lines 3972–4060)
- `[R-CNF-04]`, `[R-CNF-05]`, `[R-CNF-06]`, `[R-CNF-11]` (lines 175–200)
- Appendix G fragments surfaced by grep (compaction reproducibility)

---

## 1. Hunk 3 — §21.5 row R8, line 3572

### 1.1 The two sides

Before (one day old):

> the two being one instance because a document carrying a bare token is not
> well-formed JSON either, so no file exhibits this row's predicate alone
> through one (§21.1, R7)

After:

> the two being one instance **not because they share a shape — they do not —
> but** because a document carrying a bare token is not well-formed JSON
> either, so no file exhibits this row's predicate alone through one **and the
> second is exhibitable only as a co-violation of R7, which is `[R-VEC-02]`'s
> limit rather than a judgement under §21.1**

Unchanged around it: Instances `top-level document; layer sub-record document`
(2), Detector `reader`, Detected `extent use`, Governing rule
`[R-MTA-04]` (R-CNT-25).

### 1.2 The rule the repair asserts, in my words

Of an implementation: nothing. Of a corpus builder: R8's two alternatives —
an overflowing magnitude and a bare token — are to be built as **one**
instance per container rather than two, and the ground for that collapse is
*not* §21.1's instance arithmetic but `[R-VEC-02]`, said to impose a "limit"
because a bare-token file necessarily also exercises R7. It also asserts a
negative about the file space: no file exhibits R8's predicate alone through
the bare-token alternative.

### 1.3 Check 2 — citations

**`[R-VEC-02]`** (§24, line 3986–4007). Opened. Full relevant text:

> Each vector is one file plus a manifest entry recording, at minimum: its
> identifier; whether the file is **conforming**; the decoded content a reader
> is to return from every scope it can read … and, for each structure the file
> damages, the outcome class (§2.4), the scope, and the §21 register row it
> exercises together with that row's governing requirement identifier … Naming
> the row is a constraint on how a vector is built, not a claim about the
> file: a vector is constructed so that one row is the one it exercises, and
> **where a condition cannot be isolated — §6.2's field gates are validated
> together, so a file failing two of them attributes to neither alone — the
> entry records every row the file exercises and says which it was built
> for.** A vector whose expectation cannot be stated in those terms is testing
> something this specification has not defined, which makes it a finding
> against this document rather than a vector.

Verdict: **FAILS**. `[R-VEC-02]` contains no limit of the claimed kind. Its
one clause about non-isolable conditions is an *accommodation*: it says such a
vector is still built, and its manifest entry records every row it exercises
and names the one it was built for. A bare-token vector's expectation is
statable in exactly those terms — conforming: no; outcome ignore-record; scope
top-level (or layer sub-record) record; rows R7 and R8 with governing
requirement `[R-MTA-04]`; built for R8. So `[R-VEC-02]` does not bar the
instance; it tells you how to record it. The repair cites the one requirement
in the document that makes the collapsed instance *constructible* as the
authority for not constructing it. → finding **B-01**.

The only sentence in `[R-VEC-02]` that reads as a limit — "A vector whose
expectation cannot be stated in those terms is testing something this
specification has not defined" — does not bite here, since the expectation
*can* be stated in those terms (shown above).

**§21.1** (line 3319 ff). Opened. Relevant text, verbatim:

> The **Instances** column enumerates what a conformance corpus builds for
> that row (§21.8): the row is the rule, and each instance is one file. An
> instance names a field the condition ranges over, a container it can occur
> in, one of several alternatives the condition text states, or any
> combination of the three — **a condition applying to two alternatives in two
> containers has four.**

and

> What a cell enumerates is the condition's own alternatives and containers: a
> row whose check ranges over a family without the condition changing shape
> states that range as a single instance (T24's *any codec*), and **one whose
> members give the condition materially different shapes enumerates them**
> (T15, T25).

and

> One instance is one *distinguishable* file: where a condition is a single
> predicate over several fields — a sum against a bound, a combination of two
> flag bits — the fields it reads are not instances, because no two files
> could differ.

Verdict on the *swap*: the repair is right that §21.1's "distinguishable file"
carve-out does not license the collapse — a `1e400` document and a `NaN`
document are two distinguishable files, so "no two files could differ" is
false here. The previous version's `(§21.1, R7)` was therefore a weak
citation. But the swap did not improve it; it moved it to a requirement that
says the opposite (B-01) and, in doing so, left the cell's count with no
authority at all (B-02, below).

**R7** (line 3571). Opened: "A decoded user-metadata document is not
well-formed JSON, or its top-level value is not an object". Verdict: **PASSES**
as the row a bare-token document co-violates.

**`[R-MTA-04]`** (governing cell, unchanged; line 2544–2551). Opened:

> **Finite numbers only.** A reader interprets every JSON number as an IEEE 754
> binary64 value … A document is unreadable if it contains a number whose
> binary64 interpretation is not finite — which covers a magnitude that
> overflows on conversion, `1e400` being the ordinary case — or any of the bare
> tokens `NaN`, `Infinity`, or `-Infinity`, which RFC 8259 does not admit and
> some parsers accept regardless.

Verdict: **PASSES**. The row's predicate and both alternatives restate the rule
faithfully, and the rule itself supplies the R7 co-violation premise ("which
RFC 8259 does not admit"). Note for check 5: the rule hedges the first
alternative ("which covers … the ordinary case"), so its enumeration is open
where the row's "the two" is closed — see §1.6.

**(R-CNT-25)** parenthetical, unchanged: §21.5's preamble already sources the
quarantine outcome to it. Not disturbed by the repair. **PASSES**.

### 1.4 Check 3 — normative placement

Line 3572 begins with `|`. It is a register table row, not a `>` block. The
whole of §21.5 (3542–3575) contains no `>` lines. §21.1, the rule the
reasoning now repudiates, is plain prose at 3319–3395 with no `>` lines. So
neither side of this repair hides in non-normative text. **PASSES.**

Distinctive-term greps (hard wrap defeated by normalising whitespace first):

```
$ python3 -c "... n.count(p) ..."
'share a shape' 1
'bare token' → lines 2548 (R-MTA-04) and 3572 (R8) only
'co-violation' → line 3572 only
'cannot be isolated' → line 4000 ([R-VEC-02]) only
'1e400' → lines 2547 (R-MTA-04) and 3572 (R8) only
'non-finite' / 'not finite' → 2546, 3572 only
```

So the collapse argument exists in exactly one place (the cell) and the number
rule in exactly two (rule + row). No stale restatement of R8's content rule
elsewhere. Nothing else in the document states the collapse, so there is no
second copy to sweep.

### 1.5 Check 4 — contradiction in the same structure, including untouched text

The structure is the §21.5 table plus §21.1, which governs how its cells are
written, plus §21.8, which totals them.

I counted the register mechanically to see what the collapse is load-bearing
for:

```
$ awk 'NR>=3396 && NR<=3575' spec/tarn.md | awk -F'|' '... split(cell,a,";") ...'
… T26 3
R1 4
R2 2
R3 2
R4 16
R5 8
R6 4
R7 6
R8 2
R9 2
R10 2
ROWS=121 INSTANCES=277
```

§21.8 says "121 conditions over 277 instances". The arithmetic checks out
exactly, **with R8 counted as 2**. So the collapse is not decorative: the
document's own published count depends on it.

Now the collision. §21.1 gives one and only one licence for stating a
multi-member range as a single instance — "a row whose check ranges over a
family **without the condition changing shape**". The repair's new clause says,
in terms, that this licence does not apply: "not because they share a shape —
**they do not**". §21.1's very next clause then governs: "one whose members
give the condition materially different shapes **enumerates them**". And
§21.1's worked example is the exact arity in play: "a condition applying to two
alternatives in two containers has four."

Neighbouring rows confirm §21.1 is applied that way in practice: R1 (2
alternatives × 2 containers) = 4; R6 (2 × 2) = 4; R5 (2 × 2 × 2) = 8; R7 (3 ×
2) = 6. R8 is the sole row in §21.5 whose alternatives are not multiplied out,
and the only thing standing between it and §21.1's arithmetic is the sentence
this repair rewrote — which now (a) asserts the fact that triggers
enumeration, and (b) disclaims §21.1 as the ground for not enumerating. →
finding **B-02**.

Also checked and *not* a contradiction:
- §21.1's specialisation rule ("F1 of F6 and of F8, F35 of F36, L24 of L25")
  does not list R8 of R7, so the bare-token file is not routed to a narrower
  row; it exercises both. That is precisely `[R-VEC-02]`'s recorded case.
- §21.5's preamble (outcome, quarantine, `[R-CNF-12]`) is untouched by, and
  consistent with, the repair.
- `[R-VEC-03]`: "every register row has at least one vector for each instance
  it names" — consistent with 2 or with 4; it follows the cell.

### 1.6 Check 5 — exhaustive claims

- "**the two**" (twice: "the two being one instance", "the two ... alike").
  Tried to falsify: is there a third form of non-finite number? JSON numbers
  are finite decimal literals; binary64 conversion yields a non-finite value
  only on overflow (underflow gives ±0, finite). The bare tokens are the only
  non-numeric spellings `[R-MTA-04]` names. So two forms. **Holds**, though
  `[R-MTA-04]` states the first alternative openly ("which covers … the
  ordinary case") where the row states it closed; a later-registered third form
  would break the row's arithmetic before it broke the rule.
- "**in any form**" — open, matches `[R-MTA-04]`. **Holds.**
- "**no file exhibits this row's predicate alone through one**". Tried to
  falsify by construction. Take a document `{"a":1e400}`: `1e400` is a
  grammatically valid JSON number (RFC 8259 puts no bound on the exponent), the
  document is well-formed JSON with an object at top level, keys are fine, so
  it violates R8 and no other §21.5 row. Take `{"a":NaN}`: `NaN` is not a JSON
  value, so the text is not well-formed JSON → R7 fires too. Take `{"a":"NaN"}`:
  a string, no violation at all. So the negative holds **for the bare-token
  alternative and only for it**. Which is the referent problem in §1.7.
- "**only** as a co-violation of R7" — holds for the bare token; false if read
  of the magnitude alternative. Again §1.7.

### 1.7 Check 6 / new ambiguity — what the cell now leaves open

Structure governed: one register row = five cells (Condition, Instances,
Detector, Detected, Governing rule) plus the outcome §21.5's preamble assigns.
Walked each: Instances 2 (disputed, B-02); Detector `reader` and Detected
`extent use` match every other decoded-document row (R5–R10) and are
untouched; Governing rule `[R-MTA-04]` (R-CNT-25) checked above; outcome
ignore-record from the preamble. Nothing in the row is left unpinned by the
repair itself.

But the sentence introduces a referent that was not there before. The
condition names the alternatives in the order (1) magnitude overflow, (2) bare
tokens. The repaired clause reads "… so no file exhibits this row's predicate
alone through **one** and **the second** is exhibitable only as a co-violation
of R7".

- Reading A: "one" = the bare-token alternative (forced by the preceding
  "because a document carrying a bare token…"). Then "the second" is the same
  alternative named again, and the clause says one thing twice.
- Reading B: "one" = the first-named alternative, "the second" = the bare
  token. Then the clause asserts that neither alternative is exhibitable alone
  — which §1.6 falsifies with `{"a":1e400}`.

Reading B is what the ordinal "the second" invites, and it has a consequence: a
corpus builder taking it would conclude R8 has no isolable vector at all and
build both of its two instances as R7 co-violations, when the `1e400` form is
the clean isolating vector `[R-VEC-02]` prefers ("a vector is constructed so
that one row is the one it exercises"). The pre-repair sentence had no ordinal
and no such reading. → finding **B-03**.

### 1.8 Check 7 — analogy / warrant

The repaired cell contains one warrant-by-pointing: "which is `[R-VEC-02]`'s
limit rather than a judgement under §21.1". Verbs side by side:

| | governing verb | ranges over |
|---|---|---|
| repair | "*is exhibitable* only as a co-violation of R7" | files exhibiting R8's second alternative |
| `[R-VEC-02]` | "the entry *records* every row the file exercises and says which it was built for" | vectors whose condition cannot be isolated |

They do not range over the same thing and they do not do the same work. The
repair's verb is about which files can exist; `[R-VEC-02]`'s is about what a
manifest entry writes down for a file that does exist. Non-isolability is the
shared premise, but `[R-VEC-02]` answers it by *recording more*, never by
*building fewer*. The analogy fails in the direction that matters: it is
offered as the reason an instance disappears, and the cited rule is the reason
it does not have to. Recorded as B-01.

### 1.9 Check 1 — tense and quantifier

R8's condition is present-tense over a decoded document ("A user-metadata
document **contains** a non-finite number"), matching `[R-MTA-04]`'s "A
document is unreadable if it **contains** a number whose binary64
interpretation is not finite". Same generation (there is only one — a document
is a decoded artefact of stored bytes, not a state with an antecedent). Same
quantifier: indefinite "a document", i.e. any. **PASSES.** The repair does not
touch tense or the ranging quantifier; it touches only the instance
arithmetic, which is where the defects are.

---

## 2. Hunk 4 — §21.7, lines ~3674–3696

### 2.1 The two sides

Clause 1, before:

> A change reaching the filter, or moving a sample's byte offset within the
> decoded image without changing that image's length, **has no witness at all
> — both filter values are length-preserving (§17.3), and the content rules
> test only the bytes §14 constrains.**

Clause 1, after:

> … **is witnessed on the same terms T26 states for a wrong stride: where the
> resulting image breaks §14.5's padding content or `[R-SER-08]`'s bool bytes,
> T2, T4 or T5 fires, and where it breaks neither there is no witness. Neither
> change is caught by a length: both filter values are length-preserving
> (§17.3), and moving a sample within an image of unchanged length alters no
> declared quantity.**

Clause 2, before:

> … are unwitnessed for that same reason, **the output carrying no record of
> its input's `file_id`, generation, flags or minor, nor any record that it is
> a compaction output at all;**

Clause 2, after:

> … are unwitnessed for that same reason, **and for one they share: the output
> carries no record that it is a compaction output at all, so no check can know
> that any of the four was owed. The last two are unwitnessed twice over, the
> output also carrying no record of its input's flags or its input's minor;**

### 2.2 The rules the repair asserts, in my words

Clause 1: of an implementation — nothing new is required; of the register's
completeness claim — a §20.3-step-4 declaration change that alters the filter
or moves a sample's offset at constant length is **not** wholly undetectable
(the pre-repair text said "no witness at all", which was wrong); it is detected
exactly when the resulting decoded image breaks a §14 content obligation, by
the same three tile rows that catch a mis-strided filter.

Clause 2: all four of `[R-WRT-06]`'s trailer obligations lack a single-file
witness; the reason common to all four is that nothing in the output marks it
as a compaction output, so no check can know the obligation was owed; and two
of the four have a second, independent reason.

### 2.3 Check 2 — citations in clause 1

**T26** (line 3540). Opened, verbatim:

> Filter 2 applied at a stride other than the mandated one, **where the
> resulting image breaks §14.5's padding content or `[R-SER-08]`'s bool bytes**
> (a wrong stride with no such structural constraint is undetectable, §21.7);
> **the check that detects it is T2's or T4's**, and this row records the cause
> rather than a procedure of its own | planar numeric: channel element size;
> interleaved: sample stride Q; packed planar bool: identity s = 1 | verifier |
> certification | `[R-COD-10]` (R-SER-05)

Verdict: **PARTIAL** — see check 7 in §2.7. The condition half matches word for
word; the consequent half does not (T26: two rows; repair: three).

**§14.5** (line 1952). Opened, verbatim `[R-SER-05]`:

> Padding positions (§11.3) are serialized like any other position, and their
> content is fixed: at every padding position, a writer MUST encode, for each
> channel the position carries, that channel's fill value … **Every pad bit
> (§14.3) MUST carry the plane's channel's fill bit.** A conforming reader
> never returns this content … a verifier MUST check it, and a violation is a
> validity error at tile scope.

Verdict: **PASSES**, and it settles which side of the T26 mismatch is right:
"§14.5's padding content" carries two obligations, padding positions (T4) and
pad bits (T5). §14.3's Note is explicit that these are different things: "Pad
bits are not padding positions (§11.3)."

**`[R-SER-08]`** (line 1846). Opened: "Writers MUST NOT emit any byte other
than 0x00 or 0x01 as an interleaved bool value … its assigned detector is the
verifier". Row T2 is its real-position half and T4's "interleaved bool fill
byte" instance its padding half. **PASSES.**

**T2, T4, T5** (lines 3517–3519). Opened. T2 interleaved bool byte at a real
position; T4 padding position content, four instances including "packed planar
bool plane fill bit"; T5 packed-plane final-byte pad bits. All three are
`verifier`/`certification`, matching T26's detector. **PASSES** as the correct
three-row set for "breaks §14.5's padding content or `[R-SER-08]`'s bool
bytes".

**§17.3** (line 2357). Opened. Filter 1 = none, "the filtered image is the
decoded image"; filter 2 byte-shuffle, "**Length is unchanged.**" Values other
than 1 and 2 are invalid (`[R-COD-09]`, row L45). So "both filter values are
length-preserving" **PASSES**, and "both" is the right count because the
assigned set is exactly {1, 2}.

Also read `[R-COD-10]` in the same paragraph:

> A writer that filters with any other stride violates this rule; where the
> resulting decoded image breaks a stated content obligation (§14.5's padding,
> `[R-SER-08]`'s bool bytes) a verifier detects it as a validity error at tile
> scope, and otherwise the consequence is wrong sample content — undetectable
> by construction (§21.7).

The governing rule names the obligation, not the rows, and its "§14.5's
padding" is the whole of §14.5 — pad bits included. So the rule sides with the
repair and against T26's parenthetical. §21.1: "where a row and the rule it
cites diverge, **the rule governs**."

### 2.4 Check 2 — citations in clause 2

**§20.5 / `[R-WRT-06]`** (lines 3192–3235). Opened. Enumerated every trailer
obligation it states, one by one:

1. "It MUST mint a fresh file_id for the output — **a new draw under §9.3's
   randomness advice, not merely a value compared against the input's**"
2. "and generation 1"
3. "The output trailer MUST copy the input's unknown ignore-lane flag bits
   forward, in place of the flags = 0 §6.3 requires of a file created under
   this text (`[R-CNT-08]`)"
4. "the output's version_minor SHOULD be at least the input's" (conditioned on
   "Where the output carries a feature a later minor defines and this
   compactor does not"), with "Otherwise version_minor follows `[R-CNT-26]`'s
   floor"

So "**four obligations**" **PASSES** — the else-branch in (4) is `[R-CNT-26]`'s
own floor, not a compaction obligation. And the repair's four glosses match:
"its fresh `file_id` draw" (1), "its generation" (2), "the unknown ignore-lane
bits it MUST carry forward" (3, and note it correctly keeps *unknown*), "the
floor its version_minor SHOULD take" (4, and it correctly keeps SHOULD against
the three MUSTs).

§20.5's own witness sentence, immediately after (4): "**Neither obligation** has
a witness in the output alone (§21.7)." That is scoped to (3) and (4). It does
not assert that (1) and (2) *do* have witnesses, so it is narrower than §21.7,
not in conflict with it. Recorded as checked, not a finding.

**§9.7 / `[R-LIF-01]`** — `[R-LIF-01]` at line 1155: "Bytes in [0, F) … are
immutable". §21.7's earlier untouched sentence sources its unwitnessedness to
history not being reconstructed. The repair's "for that same reason" inherits
that. See §2.6 for where it does and does not hold.

**§6.2 trailer table** (line 741). Opened, to enumerate the structure for
check 6. Fields: trailer magic, version_major, version_minor, flags (bits
0–15 incompat / 16–31 ignore), generation, dir_offset, dir_length,
committed_file_length, file_id, reserved, trailer CRC.

**Appendix G**, surfaced by grep: "`[R-WRT-06]`'s fresh file_id is no function
of content" — independent confirmation that obligation (1) is a property of
the *drawing process*, not of the output bytes.

### 2.5 Check 4 — contradiction inside the sentence and the passage

The repaired clause 2 lives inside one long semicoloned sentence. Read whole,
normalised:

> And a commit that supersedes every tile it would have damaged leaves the live
> state clean, so the bar is unwitnessed there for the same reason `[R-LIF-01]`
> is: **it is a property of the prior generation, which §9.7 does not
> reconstruct**; §20.5's four obligations on a compacted file's trailer
> (`[R-WRT-06]`) — its fresh `file_id` draw, its generation, the unknown
> ignore-lane bits it MUST carry forward, and the floor its version_minor
> SHOULD take — **are unwitnessed for that same reason, and for one they
> share**: the output carries no record that it is a compaction output at all,
> so no check can know that any of the four was owed. **The last two are
> unwitnessed twice over**, the output also carrying no record of its input's
> flags or its input's minor; and `[R-ENC-06]`'s fixed field widths are not a
> state a file can be in …

Count the reasons the sentence hands out:
- reason A = "that same reason" = property of the prior generation, §9.7 does
  not reconstruct — asserted of **all four**;
- reason B = "one they share" = no record it is a compaction output — asserted
  of **all four** ("any of the four was owed").

Two reasons × four obligations. Then: "The last two are unwitnessed **twice
over**." If all four already carry two reasons, all four are twice over and the
distinction is empty; if only the last two are twice over, then reason A does
not in fact hold of the first two and the sentence asserting it of all four is
wrong. The clause cannot be read so that both halves are true. → finding
**B-04**.

Working out which horn is real, obligation by obligation, on the repair's own
criterion (does a single-file check fail for want of the *input*, over and
above not knowing compaction happened?):

| obligation | needs the input? | reason A true of it? |
|---|---|---|
| (1) fresh `file_id` draw | **yes** — "not merely a value compared against the input's" presupposes the input's file_id, and Appendix G says the draw is no function of content at all | as an input-relative property, yes |
| (2) generation 1 | **no** — the required value is the absolute constant 1, read straight off the output's own trailer field at offset 16 | **no**: "generation 1" is not a property of the prior generation; given that compaction is known, the check is one field read and no history need be reconstructed |
| (3) ignore-lane carry-forward | yes — needs the input's flags | yes |
| (4) version_minor floor | yes — needs the input's minor | yes |

So the correct partition is (1), (3), (4) twice over and (2) once — the exact
inverse of the repair's split on the first two. The superseded text named all
four inputs ("no record of its input's `file_id`, generation, flags or minor"),
which was loose about generation but true of file_id; the repair drops file_id
from the list and thereby loses a true ground. → finding **B-05**, with the
generation half folded into B-04's detail since it is what resolves the
contradiction.

Other things looked for in the passage and **not** found:
- No carve-out or "is not such a case" sentence anywhere in §21.7 that clause
  1's new breadth collides with. §21.7's opening paragraph in fact agrees with
  it: "The obligations of §14.5 and `[R-SER-08]` narrow this only where content
  is structurally constrained: **padding positions, pad bits, and boolean
  bytes**" — three things, matching T4, T5, T2.
- No MUST elsewhere in §21.7 that the repair's new licence lets an actor
  violate; §21.7 imposes no obligations, it accounts for absent witnesses, and
  it carries `[R-ERR-01]` at its close.
- Duplication check: clause 1's second limb ("moving a sample's byte offset
  within the decoded image") restates, on the same terms, the earlier untouched
  clause "the ordinal mappings of `[R-GEO-06]` and `[R-SER-01]` … a mis-ordered
  image is then witnessed by T2, T4 or T5, exactly as a mis-strided filter is".
  The two are **consistent** — same three rows, same trigger — so this is
  deliberate restatement, not contradiction. Recorded, not a finding.
- §20.3 step 4 read in full: its bar is "the set of padding positions (§11.3)
  and the content `[R-SER-05]` fixes there, the decoded size, the byte offset
  of any sample within the decoded tile image, or the codec and filter that
  produced the stored bytes", explicitly non-exhaustive ("the list names where
  that effect arises rather than standing on its own"). §21.7 hedges to match:
  "and then only **for part of** what it bars". No overclaim there. **PASSES.**

### 2.6 Check 1 — tense and quantifier

- §20.3 step 4's bar is quantified "for any tile that layer stores **in the
  generation this commit supersedes**", and §20.3 belabours the tense ("The
  tense is the prior generation's"). §21.7's framing sentence — untouched —
  says the bar "is witnessed only where the affected tiles **remain stored**",
  i.e. in the *new* state. Those are deliberately different generations and the
  difference is right: the bar ranges over the superseded generation's stored
  tiles; a witness exists only for bytes the live state still claims. The
  repair sits inside that framing and does not disturb it. **PASSES.**
- The repair's own quantifiers: "**both** filter values" (the assigned set is
  exactly {1,2} — passes); "**Neither** change" (the two the clause names —
  passes); "**any** of the four was owed" (universal over the four — passes as
  a quantifier, fails on the reason attached to it, B-04); "**The last two**"
  (a positional count — fails, B-05).
- Clause 2's subject is "a compacted file's trailer" — the *output*, present
  tense. The obligations it names are output-state obligations except (1),
  (3), (4), which are input-relative. The repair does not misstate which
  generation; it misstates which reason. Recorded.

### 2.7 Check 7 — the analogy, word for word

The repaired clause justifies itself by pointing: "**is witnessed on the same
terms T26 states for a wrong stride**".

| | governing verb and object | ranges over |
|---|---|---|
| repair | "where the resulting image **breaks** §14.5's padding content or `[R-SER-08]`'s bool bytes, **T2, T4 or T5 fires**" | any §20.3-step-4 change reaching the filter, or moving a sample's offset at constant length |
| T26 | "where the resulting image **breaks** §14.5's padding content or `[R-SER-08]`'s bool bytes … the check that **detects it is T2's or T4's**" | filter 2 applied at a wrong stride |

The condition clause is identical, character for character, and both verbs are
"breaks" over "the resulting image". That half **passes**. The consequent
diverges: the repair names three rows, T26 names two. The repair says it is
stating "the same terms T26 states" and is not.

The clause carries the analogy for two distinct changes, so I tested each
separately as check 7 requires:
- *a change reaching the filter* — a declaration change from filter 1 to 2 (or
  2 to 1) at constant length. Both witnesses are available: interleaved bool
  bytes (T2), padding-position content (T4), pad bits of a packed plane (T5).
  Analogy sound in substance; row list wrong.
- *moving a sample's byte offset at constant length* — reachable by reordering
  channel entries of equal element size in an interleaved layer (Q unchanged,
  every Fᶜ changes), and independently already covered by the
  `[R-GEO-06]`/`[R-SER-01]` clause above, which names the same three rows.
  Analogy sound in substance; row list wrong the same way.

Which side is stale? §14.5 states two obligations, padding positions and pad
bits; §14.3's Note insists they are different things; `[R-COD-10]` (T26's own
governing rule) names the *obligation* not the rows; §21.7's opening paragraph
names all three structurally constrained kinds. And T26's third instance,
"packed planar bool: identity s = 1", has cases witnessed by **T5 alone** — a
bool plane with P mod 8 ≠ 0 and no padding positions at all, where a wrong
stride permutes bytes and only the final byte's pad bits betray it. So T26's
"the check that detects it is T2's or T4's" is the stale text and the repair is
right about the world and wrong about T26. → finding **B-06** (unswept
restatement).

### 2.8 Check 5 — exhaustive claims in the repaired text

- "**both** filter values are length-preserving" — {1,2} is the whole assigned
  set (§17.3, L45 for the rest). **Holds.**
- "**Neither** change is caught by a length" — checked against the only two
  length rows: T14 (codec 1, entry length vs decoded size) and T3 (decoded
  payload length vs derived decoded size). Filter affects neither, by §17.3's
  "Length is unchanged"; the second change is at constant length by
  construction. **Holds.**
- "**there is no witness**" where the image breaks neither — matches
  `[R-COD-10]`'s "otherwise the consequence is wrong sample content —
  undetectable by construction". **Holds.**
- "**four** obligations" — enumerated §20.5 above, four. **Holds.**
- "**no check** can know that any of the four was owed" — read against §21.7's
  frame sentence, "a single file exhibits no witness of their violation". A
  cross-file tool holding input and output could know for (3) and (4). Within
  the section's declared single-file frame the claim **holds**; I flag that
  "no check" is broader than "no single-file check" only as a note, since the
  frame is set two sentences earlier and the whole subsection reads under it.
- "**The last two**" — a positional count. **Fails**, B-05.
- "**alters no declared quantity**" — a universal negative over declared
  quantities. **Fails**, see §2.9.

### 2.9 Check 6 / new ambiguity — the structures, member by member

**Structure A: §20.3 step 4's bar list**, the thing clause 1 accounts for.
Members and their §21.7 witness accounts:

| member of the bar | §21.7 account | pinned? |
|---|---|---|
| the set of padding positions (§11.3) | "a byte §14 structurally constrains … fires §21.4's content rows" | yes |
| the content `[R-SER-05]` fixes there | same | yes |
| the decoded size | "witnessed by T3 or T14" | yes |
| the byte offset of any sample | repaired clause 1 | yes |
| the codec | "*sometimes* witnessed … but neither is assured" | yes, honestly hedged |
| the filter | repaired clause 1 | yes |

No member is left without an account, and §20.3's own "the list names where
that effect arises rather than standing on its own" is matched by §21.7's "only
for part of what it bars". Check 6 **passes** for clause 1.

But clause 1's closing gloss introduces a false universal. "moving a sample
within an image of unchanged length **alters no declared quantity**". §14.2
says of exactly these quantities: "Q = Σ Bᵢ over all channels (the **sample
stride**), and Fᶜ = Σ Bⱼ over channels j < c (channel c's in-sample offset).
**These products and sums are declaration-derived quantities under
`[R-ENC-04]`**." The only way to move a sample's offset at constant length is
to change a declaration — reorder equal-width channels, and every Fᶜ after the
swap changes; the channel entries themselves are declared. So the sentence
denies, in a passage whose entire subject is declaration changes, that a
declaration change alters a declared quantity. The intended claim is plainly
"alters no quantity any register row tests as a length" — which is what the
preceding half-sentence already says. → finding **B-07**.

**Structure B: the compacted output's trailer**, the thing clause 2 accounts
for. Walked all eleven fields of §6.2's table:

| field | fixed by | witnessed in the output alone? |
|---|---|---|
| trailer magic | `[R-CNT-06]` | yes |
| version_major | `[R-CNT-06]`, §6.3 | yes |
| version_minor | `[R-CNT-26]` floor, §20.5 input floor | floor: no — obligation (4) |
| flags, incompat lane 0–15 | §6.3; no bit is defined in this text, so any set bit is unimplemented → reject-file | yes (vacuously) |
| flags, ignore lane 16–31 | §20.5 carry-forward — obligation (3) | no |
| generation | §20.5 "generation 1" — obligation (2) | value yes, owedness no |
| dir_offset / dir_length | `[R-CNT-06]` bounds | yes |
| committed_file_length | `[R-CNT-06]` = F, multiple of 64 | yes |
| file_id | `[R-CNT-06]` ≠ 0; §20.5 fresh draw — obligation (1) | nonzero yes, freshness no |
| reserved | `[R-CNT-06]` zero | yes |
| trailer CRC | `[R-CNT-06]` | yes |

So the four the repair names are exactly the unwitnessed ones and no sibling
field of the same structure is left ungoverned. One genuine gap sits in §20.5
rather than in the repair: it obliges carrying forward the input's **unknown**
ignore-lane bits and says nothing about ignore-lane bits a later-minor
compactor *does* implement. The repair restates §20.5 faithfully ("the
**unknown** ignore-lane bits it MUST carry forward"), so this is not a defect
in the repair and I am not filing it as one; recorded here because check 6 asks
for it.

### 2.10 Check 3 — normative placement

Lines 3664–3699 contain no `>` lines: §21.7 is plain prose closing with
`[R-ERR-01]`. T26 at line 3540 is a table row. §14.5, §17.3's `[R-COD-10]`
paragraph, and §20.5 are all plain prose. Nothing here is a repair written into
a Rationale. **PASSES.**

Restatement sweep for clause 1's rule (whitespace-normalised, since every one
of these phrases spans a line break in the source):

```
'on the same terms T26'          1   (the repair)
'T2, T4 or T5'                   2   (line 3657 untouched; line 3677 the repair)
"T2's or T4's"                   1   (T26, line 3540)
'length-preserving'              1
'alters no declared quantity'    1
```

Four places state the witness set for a §14-content breakage: §21.7's opening
paragraph ("padding positions, pad bits, and boolean bytes"), §21.7 line 3657
("T2, T4 or T5"), the repair ("T2, T4 or T5"), and T26 ("T2's or T4's"). Three
agree; T26 is the odd one and was not swept. That is B-06.

Restatement sweep for clause 2: §20.5's "Neither obligation has a witness in
the output alone (§21.7)" is the only other statement, checked in §2.4 and
consistent.

---

## 3. Byte-level test, per finding

The discriminating question in every case: is the disputed file conforming?

- **B-01, B-02, B-03** — the disputed file is a user-metadata document
  carrying a bare `NaN`. It violates R7 and R8 under every reading, outcome
  ignore-record either way, so `[R-CNF-05]` bars every conforming writer from
  emitting it under both readings and no reader's verdict moves. What moves is
  the size of the corpus (277 vs 279 instances) and whether §21.8's published
  count is right. **Not byte-level.**
- **B-04, B-05** — these concern why a check cannot see something, not what any
  check does. A compactor's obligations are unchanged; the emittable set is
  unchanged. **Not byte-level.**
- **B-06** — the disputed file is a tile filtered at a wrong stride whose only
  structural breakage is a packed plane's pad bits. It is nonconforming under
  T5 on both readings, and `[R-CNF-04]` obliges a verifier to detect every
  register row, so T5 is checked whether or not T26's parenthetical mentions
  it. No verdict forks. **Not byte-level.** (What forks is which row a vector's
  manifest entry names under `[R-VEC-02]` — a corpus-attribution difference.)
- **B-07** — an explanatory gloss in a subsection that imposes no obligations.
  **Not byte-level.**

I did not find a byte-level defect in either hunk, and I am not inflating one.

---

## 4. Summary of findings

| id | hunk | check | one line |
|---|---|---|---|
| B-01 | 3 | citation | `[R-VEC-02]` states no such limit; its non-isolable clause makes the vector constructible, not barred |
| B-02 | 3 | contradiction | "they do not [share a shape]" is §21.1's trigger to enumerate; cell keeps 2 where §21.1 demands 4, and repudiates the only rule that governs the count |
| B-03 | 3 | new ambiguity | "through one … and the second" — referent forks between redundancy and a false claim about `1e400` |
| B-04 | 4 | contradiction | two reasons given for all four obligations, then "twice over" reserved to two of them |
| B-05 | 4 | overshot | "The last two" drops the `file_id` obligation, which the superseded text named and which needs the input's file_id |
| B-06 | 4 | unswept restatement | T26 still says "T2's or T4's" while the repair claims to state T26's own terms and names T2, T4 or T5 |
| B-07 | 4 | new ambiguity | "alters no declared quantity" is false of the only changes that produce the case |


---

*Editorial substitution for the repository vocabulary gate: one ordinary-English
use of a gate word was replaced with an exact synonym at line 323 ('a state with
an antecedent'). The auditor's reasoning is unchanged. Rounds 19 and 22 each
required the same treatment; the substitution is recorded here rather than made
silently.*
