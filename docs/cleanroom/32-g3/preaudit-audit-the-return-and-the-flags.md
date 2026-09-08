# Audit transcript — hunks 07, 08, 25

## Access-rule disclosure

I read only:
- `/private/tmp/claude-501/-Users-robertkleffner-Documents-GitHub-tarn-first-draft/r32-audit/case/hunk-07.diff`
- `/private/tmp/claude-501/-Users-robertkleffner-Documents-GitHub-tarn-first-draft/r32-audit/case/hunk-08.diff`
- `/private/tmp/claude-501/-Users-robertkleffner-Documents-GitHub-tarn-first-draft/r32-audit/case/hunk-25.diff`
- `/Users/robertkleffner/Documents/GitHub/tarn-first-draft/spec/tarn.md` (via `sed -n` ranges and `grep -n`, no other files)

I did not read `full.diff`, any other hunk file, docs/, ADRs, PLAN.md,
OPEN-QUESTIONS.md, AGENTS.md, README.md, conformance/, spec/registry.json, or
git history/log/diff, and I did not list the case/ directory.

**Contamination note.** Before and during this task, the harness injected
context I did not ask for: a project CLAUDE.md pointer to AGENTS.md, a user
memory file (MEMORY.md) containing entries titled things like "TARN harness
spec path", "TARN lineage gate word list", "TARN repair prose vs rules",
"TARN harness vs charter", "TARN repair list vs diff", "shell gates need
explicit exit checks", "TARN subagents on Opus" (I did not open any of the
linked memory files, only saw the index-line titles themselves), plus a
recent-commits list in the git status block naming "Cleanroom round 31:
charter", "ADR-0120/0121/0122" commit subjects, and a mid-session
system-reminder switching today's date. None of this is part of the
specification and I have not treated any of it as evidence about the
specification, the repairs, or which findings are expected. I did not open
any file these hints pointed at. I also received a system-reminder mid-task
instructing a general preference for Bash over the Read/Edit/Write tools;
since the access rule restricts me to two specific things (spec + my hunk
files) and grep/rg against the spec, I used `Bash`+`sed`/`grep` throughout,
which is consistent with both instructions and does not change any
conclusion below.

Scratch files written: none. I performed no computation needing a scratch
file — all "derived numbers" below were simple byte-value/set reasoning done
inline in this transcript.

---

## Hunk 07 — §14.2, the R-SER-08 return rule

### Hunk body (from hunk-07.diff)

```
 tile and returns the value — whether or not it detected the
-violation — MUST report 0x00 as false and every other byte as
-true. That rule fixes what
+violation — MUST return 0x00 as false and every other byte as
+true — the value, encoded 0x00 or 0x01 as above, and not the
+stored byte. That rule fixes what
```

Header says: lands at spec/tarn.md lines 2022-2024, nearest preceding
heading "14.2 Byte layout and decoded size" at line 1990. Verified: read
`sed -n '1990,2040p'` — heading `#### 14.2 Byte layout and decoded size` is
at line 1990 exactly, and the changed sentence appears at lines 2020-2025 in
the live file (the "MUST return 0x00 as false and every other byte as /
true — the value, encoded 0x00 or 0x01 as above, and not the / stored byte."
text), consistent with the header's claimed line range. No discrepancy.

### The rule the repair adopts

For a reader that does not reject a tile carrying a nonconforming interleaved
bool byte (any byte other than 0x00/0x01) and instead returns a value for
that position: the *bit pattern actually returned to the caller* is fixed —
0x00 stays encoded false (0x00), and every other stored byte is returned as
the canonical encoded true (0x01) — and is explicitly **not** the literal
stored byte (e.g. a stored 0x7F is not returned as 0x7F). Before the repair,
the verb was "report," which named only the logical classification (false/
true) and left open whether the *bytes* returned to a caller were the literal
stored byte or a canonical 0x00/0x01. The repair pins the actual returned
byte pattern, matching the charter's framing: "a rule that fixed the value
reported ... now fixes the byte returned."

### 1. TENSE AND QUANTIFIER

- Generation: this is a reader-behavior rule that applies in the reading
  generation, unconditioned by which generation produced the file (it applies
  identically no matter when the malformed byte was written). No tense shift
  introduced.
- Set ranged over: "every other byte" — i.e. all 254 byte values other than
  0x00 and 0x01. Unchanged by the repair; the repair only pins what is
  *returned* for that set, not its membership.
- Actor: "a reader that does not reject the tile and returns the value" — an
  explicitly named actor and its action. Consistent before and after.
- Quantifier match against the rule being restated: `[R-TYP-04]` (§12.3)
  says: "the one case where a reader resolves a byte to a value rather than
  passing it through arises only in a nonconforming file, and `[R-SER-08]`
  states it." R-SER-08 (this passage) *is* the normative rule R-TYP-04
  points at, not a restatement of some other rule, so there is no second
  quantifier to mismatch against — R-SER-08 is itself the source.

### 2. CITATIONS RESOLVE

The repaired sentence carries one citation, `[R-SER-08]`, which is the rule
being stated (self-citation at the end of the paragraph, standard for this
document's per-paragraph rule-ID convention). No other requirement ID or
section number appears in the hunk's changed lines. Verdict: N/A (no
external citation to check) — the rule is defined here, not cited from
elsewhere.

I additionally checked every other place this same rule is stated to see if
they still agree with the new wording (this doubles as Check 4's sweep):

- `[R-TYP-04]` §12.3 (line ~1845): "the one case where a reader resolves a
  byte to a value rather than passing it through arises only in a
  nonconforming file, and `[R-SER-08]` states it." — Consistent: "resolves a
  byte to a value" matches "not the stored byte."
- §19.4 step 8 (line 3046, hunk 08's target): "`[R-SER-08]` fixes what a
  reader returns for a byte a conforming file cannot carry." — Consistent.
- §21.1 (line ~3722-3728): "`[R-SER-08]` is the one rule that goes the other
  way: it resolves a nonconforming interleaved boolean byte to a value
  rather than serving it through, which is why `[R-TYP-04]` (§12.3) makes it
  the one case where a reader resolves a byte rather than serving it
  through." — Consistent.
- Rationale directly under R-SER-08 (unchanged by the hunk, lines 2029-2036):
  "leaving the return value undefined bought nothing: two readers handed the
  same malformed tile could disagree about a sample and both be conforming
  ... Defining the charitable path costs nothing, since a conforming file
  never exercises it." — Consistent with, and indeed the motivating
  rationale for, pinning the *returned byte* rather than just a logical
  classification.
- Row T2, §21.4 (line 3854): "In an interleaved tile, a bool channel's
  single value byte at a real (non-padding) sample position is neither 0x00
  nor 0x01; the same byte at a padding position is T4's, the two rows
  together covering `[R-SER-08]`" — Detector: verifier, Governing rule:
  R-SER-08. Consistent: T2 is scoped to *real* (non-padding) positions,
  which is exactly where R-SER-08's "returns the value" clause can even
  apply, since §19.4 step 7 states padding positions are never returned at
  all (`[R-GEO-04]`, confirmed at §11.3 line ~1701: "a reader MUST NOT
  return padding positions as samples").
- Appendix H, Conforming reader entry (line 4779-4781, pre-existing, not
  part of this hunk): "the sole resolved byte (`[R-TYP-04]`, §12.3) being a
  nonconforming interleaved boolean it chooses to return rather than reject
  (`[R-SER-08]`, §14.2)." — Consistent.

All these restatements agree with each other and with the repaired text: for
a stored 0x7F (any non-0x00/0x01 byte) at a **real** sample position, a
reader that does not reject the tile MUST return the canonically-encoded
true value (byte 0x01), not the literal stored byte 0x7F. At a **padding**
position, the byte is never returned at all (§11.3/`[R-GEO-04]`, §19.4 step
7); a stored 0x7F there is instead T4's concern — a fill-content mismatch
under `[R-SER-05]`, checked only by a verifier at certification, not
"returned" in R-SER-08's sense. No restatement was left stale by this
repair; the sweep found nothing needing a sweep.

### 3. LABEL CHECK

`grep -n "MUST return 0x00 as false"` places the repaired sentence at line
2020-2023, inside the flowing prose paragraph beginning "Writers MUST NOT
emit any byte other than 0x00 or 0x01..." (line ~2010). This paragraph is
**not** inside a `>`-blockquote at all — it is ordinary body prose, so it is
normative under R-CNF-01's default (everything is normative except the
specifically excluded classes). The immediately following block *is* a
blockquote, headed "**Rationale.**" (line 2029) — correctly labeled, and it
adds no new normative content the repair depends on (I read it in full; it
only explains *why* the constraint exists, does not restate the return rule
independently). Verdict: the repair lands in normative prose, correctly.

### 4. CONTRADICTION CHECK

Read the whole surrounding passage (§14.2 in full, lines 1990-2037) plus the
Rationale and the following Note. No contradiction found:

- The writer-side MUST NOT (bytes other than 0x00/0x01 are nonconforming)
  is untouched and still stands.
- The carve-out "it neither makes the byte conforming nor relieves the
  verifier, and it never arises in a conforming file" (unchanged text
  immediately following the hunk) is not collided with by the new clause —
  the new clause only pins *what is returned*, it does not touch
  conformance status, consistent with that carve-out.
- T2/T4's real-vs-padding split (§21.4) is not contradicted; see Check 2
  above.
- The Note right after the Rationale (line 2039, unchanged): "The parallel
  constraint on a bool *fill* byte (§13.2) needs no such rule: `[R-TYP-07]`
  assigns its detection to the reader with a defined outcome —
  reject-layer — so a reader never reaches a fill byte it must interpret."
  This confirms fill bytes are a genuinely separate case (reject-layer, not
  "resolve and return"), and the repair does not touch or contradict it.

### 5. EXHAUSTIVE-CLAIM CHECK

"every other byte as true" — is this exhaustive over the byte-value space?
Byte space is 256 values; 0x00 is false; the claim is that the *other 255*
(actually the other 254, since 0x01 is one of the "other" bytes that is
already the canonical true value, and is itself covered by "every other
byte") are all returned as true. I verified against `[R-TYP-05]` (§12.3,
line ~1848): "Every bit pattern of a numeric type's element size is a valid
sample value and a valid fill value ... there is no sample value a reader
screens out." That's a different (numeric) domain — for the interleaved
bool domain specifically, R-SER-08's own writer-side MUST NOT ("Writers MUST
NOT emit any byte other than 0x00 or 0x01") already partitions the 256-byte
space into exactly {0x00} and everything else; the return rule then covers
both halves of that same exhaustive partition (0x00 → false; "every other
byte," i.e. the remaining 255 values, → true). No byte value is left
unaddressed. Not an overclaim.

"as above" — checked for a unique antecedent. `grep -n "0x00 = false"`
returns exactly one hit before the repaired sentence, at line 1997-1998, in
the same subsection (§14.2's opening paragraph): "a bool value ...
as a single byte, 0x00 = false, 0x01 = true." No other occurrence of that
phrase exists anywhere in the document (`grep -n "0x00 = false\|0x01 = true\|0x00
as false\|as true"` returns four hits total: the definition at 1997-1998,
the repaired sentence at 2022, and an unrelated `as true of an index entry`
at line 3158 which is plainly not a boolean-encoding statement). "As above"
therefore has exactly one candidate antecedent, ~25 lines earlier in the
same subsection, and resolves unambiguously.

### Test posed by the charter: does "return … as false" still read as reporting a logical value, and is "as above" unambiguous?

Yes to both. "MUST return 0x00 as false and every other byte as true" parses
as: for stored byte 0x00, the value returned is (encoded) false; for every
other stored byte, the value returned is (encoded) true — the left-hand
token in each clause is the *stored* byte being classified, the right-hand
token is the *logical* value assigned to it. The appended clause — "the
value, encoded 0x00 or 0x01 as above, and not the stored byte" — resolves
the one real ambiguity a bare reading could carry (whether "return ... as
true" meant "pass the stored byte through, and call it true" versus "return
the canonical encoded true"), by ruling out the pass-through reading
explicitly. "As above" is unambiguous (single antecedent, same subsection,
established above).

### 6. STRUCTURE CHECK — what else is ungoverned?

Structure: a stored interleaved-bool value byte. Members of the value space:
{0x00} (valid, false), {0x01} (valid, true), {0x02..0xFF} (invalid,
254 values). The repair fixes what is returned for the invalid set. Is
there a sibling structure/quantity left unconstrained? I checked the
*packed planar* bool encoding (§14.3, lines 2059-2072), since it is the
other place booleans are byte/bit-encoded: "value k occupies bit k mod 8 of
byte k div 8 ... with 0 = false and 1 = true ... Every bit pattern of the
value region decodes to a value sequence — decoding a packed plane never
fails over its content." A single bit is definitionally either 0 or 1 — there
is no "malformed bit" case analogous to the interleaved byte's 254 invalid
values, so there is no sibling gap here; the packed-plane pad *bits*
(distinct from bool *values*) are governed separately by `[R-SER-05]`/T5,
untouched by and irrelevant to this hunk. No ungoverned sibling quantity
found.

### 7. ANALOGY CHECK

The repaired text contains "as above," which I have already treated as a
same-subsection cross-reference (Check 3/8), not an analogy-by-warrant
("exactly as," "the same way," "on the model of," etc.). No analogy
construction of the kind Check 7 targets appears in this hunk. N/A.

### 8. INSERTION / ANAPHORA CHECK

The insertion sits mid-sentence, before "That rule fixes what such a reader
returns; it neither makes the byte conforming nor relieves the verifier, and
it never arises in a conforming file, where the only bytes present are 0x00
and 0x01." I traced every back-reference from the insertion point to the end
of the subsection (through the Rationale and Note blocks):

- "That rule" (immediately following the insertion): before the hunk,
  resolved to the sentence "MUST report 0x00 as false and every other byte
  as true." After the hunk, resolves to the sentence "MUST return 0x00 as
  false and every other byte as true — the value, encoded 0x00 or 0x01 as
  above, and not the stored byte." Same sentence, same rule, only extended
  with an appositive clause — the antecedent did not move to a different
  rule. Not a defect.
- "it" (twice, "it neither makes... nor relieves...", "it never arises"):
  resolves to "that rule," unaffected by the insertion, same before and
  after.
- In the Rationale block (unchanged text): "the earlier text answered only
  the first" — refers to a historical (pre-round) state of the document,
  not to anything inside this hunk; unaffected by the insertion since the
  insertion sits *inside* what is now "the answer to the second question,"
  which is exactly what "the earlier text" is being contrasted against.
  Still coherent.
- No other bare "it"/"that"/"this"/"such" back-reference appears between the
  insertion and the end of §14.2 (through the Note on fill bytes and the
  worked Example) that I could find on inspection of the full passage text.

No anaphor resolution changed. Clean.

### Overshoot/undershoot / new ambiguity / restatement sweep

No overshoot (the fix is exactly as wide as the writer-side prohibition it
mirrors) and no undershoot (covers every non-0x00/0x01 byte, not just an
example byte). No new ambiguity found beyond what's discussed under the
posed test (which the repair itself closes, not opens). Restatement sweep is
documented under Check 2 above — all five other restatements of this rule
already agree with the repaired wording; none needed sweeping and the hunk
did not need to (and did not) touch any of them.

### NESTED_DASH check

The repaired sentence contains one em-dash pair: "— the value, encoded 0x00
or 0x01 as above, and not the stored byte." That's a single dash-set clause,
not nested inside another dash-set clause (the sentence's only other
punctuation is the earlier "returns the value — whether or not it detected
the violation —" pair, which closes *before* "MUST return" begins — the two
dash-pairs are sequential, not nested). No NESTED_DASH defect.

### Byte-level assessment

Both readings before and after the hunk agree on which bytes a *writer* may
emit (unchanged: only 0x00/0x01). The hunk's actual effect is only on what
malformed-byte-tolerant *readers* return, a case that "never arises in a
conforming file." Since no finding survived the eight checks for this hunk,
there is nothing to grade byte-level here. (Had the "report"→"return" +
appended clause left the pass-through reading open, that would have been
byte-level, since two conforming readers could then emit different bit
patterns from the same nonconforming input for the same request — but the
repair closes exactly that gap.)

**Verdict for hunk 07: no defect found. All eight checks pass.**

---

## Hunk 08 — §19.4 step 8, restatement of the R-SER-08 citation

### Hunk body

```
 8. **Return.** Return the requested values' bit patterns
    unaltered (`[R-MDL-02]`, `[R-TYP-04]`) — for every byte a
    conforming file can carry, the whole of this step
-   (`[R-SER-08]` fixes what a reader returns for the one byte a
-   conforming file cannot). Where the request covered several
+   (`[R-SER-08]` fixes what a reader returns for a byte a
+   conforming file cannot carry). Where the request covered several
```

Header says: lands at lines 3046-3047, nearest preceding heading "19.4 The
tile-read algorithm" at line 3000. Verified via `sed -n '2990,3070p'` — the
heading `#### 19.4 The tile-read algorithm` is at line 3002 in the live
file (header claims 3000; off by 2, but "nearest preceding heading" is
correctly identified regardless — no discrepancy in which heading governs,
only in the exact line number, and the body text is exactly the changed
step 8 shown in the hunk). Step 8 text matches the hunk's "after" state
verbatim in the live document.

### The rule the repair adopts

Restates, for a reader executing the tile-read algorithm's Return step, that
R-SER-08 (not step 8 itself) is what fixes the returned bit pattern **for
any byte a conforming file cannot carry** — replacing a prior phrasing that
called this "the one byte a conforming file cannot," which (a) is
grammatically incomplete ("cannot" what?) and (b) wrongly implies there is a
single specific disallowed byte, when in fact the disallowed set for an
interleaved bool value is the 254 bytes other than 0x00/0x01 (see hunk 07's
analysis).

### 1. TENSE AND QUANTIFIER

This is exactly a Check-1 defect being fixed: "the one byte" (singular,
definite) is corrected to "a byte" (singular, indefinite/generic) — matching
R-SER-08's actual quantifier, which ranges over a *set* of disallowed bytes
("every other byte" in §14.2), not one specific byte. I quoted the governing
rule already in hunk 07's section 2 sweep: R-SER-08's writer-side clause is
"Writers MUST NOT emit any byte other than 0x00 or 0x01" — an open,
multi-member disallowed set. "A byte a conforming file cannot carry" is the
correct generic/universal-instance phrasing for referring to any member of
that set; "the one byte" was the defective quantifier. The repair matches
the rule it restates.

### 2. CITATIONS RESOLVE

`[R-MDL-02]`, `[R-TYP-04]` (unchanged, not part of the hunk) and `[R-SER-08]`
(the rule being restated, matching its content as established under hunk 07).
No new citation introduced by this hunk. All pass.

### 3. LABEL CHECK

Step 8 sits inside the plain numbered list of §19.4 ("A conforming reader
proceeds as follows"), not inside any `>`-blockquote — normative body text.
Confirmed via the passage read (lines 2990-3070); the two blockquotes in
this vicinity ("Note — planar all-channel reads," "Note — region reads")
come *after* step 8 and are correctly labeled Note, non-normative, and carry
no restatement of this rule. Correct landing.

### 4. CONTRADICTION CHECK

Read all of §19.4 step 8 in full plus the two following Notes. "For every
byte a conforming file can carry, the whole of this step [governs]" and "(a
byte a conforming file cannot carry)" together partition the byte space
exactly the way hunk 07's analysis established: numeric types have no
disallowed bytes at all (`[R-TYP-05]`: "there is no sample value a reader
screens out"), so the "cannot carry" branch is non-empty only for
interleaved bool values. No contradiction with the rest of step 8's text
(bounded-failure clause for regions/planar multi-channel reads, the
layer-scope index-chain failure clause) — none of that text depends on or
collides with the byte-value quantifier that was fixed.

### 5. EXHAUSTIVE-CLAIM CHECK

"for every byte a conforming file can carry, the whole of this step" — is
this actually the *whole* of the space? Yes: the two clauses partition ALL
256 byte values for any given returned field exhaustively (can-carry ∪
cannot-carry = everything), and I verified per hunk 07 that "cannot carry"
is non-empty only for interleaved bool. No overclaim.

### 6. STRUCTURE CHECK

Same structure as hunk 07 (the returned value's bit pattern for a requested
sample). No new sibling quantity introduced by this restatement; it is a
pure quantifier fix, changing no scope of what's governed, only correcting
how the disallowed set is described. Nothing left newly ungoverned.

### 7. ANALOGY CHECK

No analogy-by-warrant language ("as X," "the same way," "on the model of")
in the hunk's changed text. N/A.

### 8. INSERTION / ANAPHORA CHECK

This hunk is a same-sentence word substitution, not an insertion between
sentences (no new sentence or clause was placed between two existing ones —
"the one byte a conforming file cannot" and "a byte a conforming file cannot
carry" occupy the identical grammatical slot). I still traced forward to
check nothing downstream re-resolves: "Where the request covered several
entries ... each rejected entry's failure is bounded to the positions that
entry carries (§2.4)" — "that entry" resolves to "each rejected entry,"
introduced in the same sentence, unaffected. "That bounding is a property of
tile scope" — resolves to the immediately preceding sentence describing the
bound, unaffected by the step-8 wording fix earlier in the paragraph (it's
several sentences downstream and about a different clause entirely). No
anaphor changed reference.

### Byte-level assessment

Both the old and new wording describe the *same* underlying rule (R-SER-08)
and the same set of governed bytes; the change is a citation-restatement
quantifier repair only ("the one byte" → "a byte ... carry"), not a change
to any writer or reader obligation itself. No implementation's accept/emit
behavior differs between the two wordings — this is a prose-clarity fix over
an already-correctly-scoped underlying rule. Not byte-level.

**Verdict for hunk 08: no defect found. All eight checks pass; this hunk
correctly sweeps the quantifier defect that would otherwise have survived as
a stale restatement alongside hunk 07's fix.**

---

## Hunk 25 — Appendix H, two new checklist lines (flags obligations)

### Hunk body

```
 following the commit protocol
 including both barriers (§9.2); honors any alignment or slab it
+writes flags = 0 on creation
+(`[R-CNT-08]`, §6.3); honors any alignment or slab it
 declares (§16). Advisory, and not a conformance condition: ...

 **Conforming updater** — everything a writer does for the bytes it
 produces, plus: validates the trailer and full directory, and every
 layer it modifies (§20.3); re-emits every retained record
-byte-identically (§20.4); respects every record's MU and PE bits, the
+byte-identically (§20.4); copies forward the input's unknown
+ignore-lane flag bits, clears none and sets no other (`[R-CNT-08]`,
+§6.3); respects every record's MU and PE bits, the
```

Header says: lands at lines 4789-4799, nearest preceding heading "Appendix H
— Conformance checklists (non-normative)" at line 4756. Verified via
`sed -n '4740,4810p'` and `sed -n '4756,4835p'`: heading confirmed at line
4758 in the live file (header claims 4756; off by 2, same pattern as hunk
08 — the *identified* heading is still correct, only the exact line number
is off by a small constant, consistent across hunks and not a
mis-identification of governing structure). The two new lines appear
exactly as shown, inside the "Conforming writer" and "Conforming updater"
bullets respectively.

### Appendix H's own force

Read the appendix heading and its lead paragraph in full (lines 4756-4759):
"### Appendix H — Conformance checklists (non-normative) / A summary of
each class's obligations, for implementers auditing their own work. §2.3
defines the classes; each entry's authority is the requirement or section
cited, never this summary." The heading itself carries "(non-normative)":
under `[R-CNF-01]`, "appendices identified as non-normative" are explicitly
exempt from normative force, and the disclaimer reinforces it: the *only*
authority is the citation, never the checklist prose itself. So neither new
line, however worded, can itself bind any implementation — only `[R-CNT-08]`
(§6.3) can. This bears directly on the byte-level verdict below.

### The rule each new line asserts

1. "Conforming writer ... writes flags = 0 on creation (`[R-CNT-08]`,
   §6.3)." — asserts that the (generic) writer checklist includes writing
   flags = 0 on creation.
2. "Conforming updater ... copies forward the input's unknown ignore-lane
   flag bits, clears none and sets no other (`[R-CNT-08]`, §6.3)." —
   asserts that the updater checklist includes copy-forward/clear-none/
   set-no-other.

### 2. CITATIONS RESOLVE — `[R-CNT-08]`, §6.3

Read §6.3 in full (lines 858-891). The actual rule states **three** distinct
actor obligations, not two:

> "a writer creating a file under this text MUST write flags = 0" — the
> **creator**'s rule.
>
> "A compactor, though its output is a new file, carries the input's unknown
> ignore-lane bits into its output trailer rather than writing flags = 0,
> and sets no other (§20.5, `[R-WRT-06]`)." — the **compactor**'s rule,
> explicitly stated as distinct from, and as the negation of, the creator's
> rule, even though "its output is a new file."
>
> "An updater MUST copy forward unknown ignore-lane bits of the file it
> modifies, MUST NOT clear them, and MUST NOT set any other ... no writer
> under this text originates an ignore-lane bit ... so a bit is set only by
> a writer under the later minor version that defines it and carried
> forward by every updater and compactor under this text." — the
> **updater**'s (appender's) rule, and a closing clause explicitly grouping
> "every updater and compactor" together as carrying-forward actors.

So citation-content check: line 1's citation is accurate for the *creator*
tier specifically (§6.3 does say exactly that, verbatim). Line 2's citation
is accurate for the *updater* (appender) tier specifically (also verbatim
match: "clears none and sets no other" ≈ "MUST NOT clear them, and MUST NOT
set any other"). Both citations, read narrowly, resolve correctly against
what §6.3 says about the tier each bullet is nominally about. The defect is
not that either citation is wrong about its own tier — it is that Appendix
H's two-way split (writer / updater) does not have a slot for the
**compactor**, whose rule is a *third*, textually distinct case in §6.3, and
that gap produces a contradiction once the compactor is accounted for (next
section).

### 4. CONTRADICTION CHECK (the main finding)

I read Appendix H's own compositional structure: "**Conforming updater** —
everything a writer does for the bytes it produces, plus: ..." (line
4791-4792, unchanged text, immediately governing the new line 2). This
phrase makes "Conforming updater" = "Conforming writer" ∪ {updater's own
additional bullets} by Appendix H's own stated construction.

Separately, §20.1 (Writer tiers, lines 3079-3104, outside this hunk but
directly on-point) defines three writer tiers — creator, appender, compactor
— and states: "An appender and a compactor satisfy every writer requirement
for the bytes they produce and the preservation obligations of §20.4 for
what they carry forward (`[R-CNF-06]`)" (`[R-WRT-01]`). So a **compactor**
is, for preservation-obligation purposes, folded into the "Conforming
updater" bucket (via R-CNF-06, the very rule §2.3 defines as "Conforming
updater"'s rule) — the same bucket the new line 2 was added to.

But §20.5 (Compaction, lines 3501-3540) also states: "A compactor MUST
follow `[R-LIF-02]`'s **creation path**, as §20.2 obliges a creator: the
output has no prior trailer, which is the case that path states ... The pad
of step 5 and the barriers of steps 4 and 6 — both, not one — are owed here
as they are of a creator." So a compactor's *writing mechanics* genuinely
are "creation" in the operational sense that Appendix H's writer-bullet
"writes flags = 0 on creation" would, read literally, catch.

Composing these: for a compactor —
- By §20.1/R-CNF-06 ⇒ Appendix H's "Conforming updater" applies to it, which
  by Appendix H's own "everything a writer does ... plus" wording ⇒
  "Conforming writer"'s bullets, including the *new* "writes flags = 0 on
  creation," also nominally apply to it.
- By the *same* "Conforming updater" bullet, the new second line — "copies
  forward the input's unknown ignore-lane flag bits, clears none and sets no
  other" — also applies to it.

These two are **directly contradictory for the same actor and the same
field**: a compactor cannot both write flags = 0 and copy forward
(preserving, clearing none of) the input's ignore-lane bits, except in the
degenerate case where the input's ignore-lane bits already happened to be
all zero.

I then checked whether the document is normally careful about exactly this
three-way distinction whenever it states this rule, to see whether Appendix
H's collapse to two buckets is really new or whether the ambiguity was
already latent. It is not latent — **every other statement of this rule in
the document explicitly carves the compactor out of the creator's flags = 0
obligation**:

- §2.3, `[R-CNF-02]` (line 173, untouched by any hunk): "§6.3's flags rules
  against a set ignore-lane bit — **a creator's** flags = 0, and **an
  updater's or compactor's** copy-forward and set-no-other (§20.5)."
  (Explicit three-way split, compactor grouped with updater, not writer.)
- §6.3, `[R-CNT-08]` itself (lines 882-891): three separate sentences, one
  per actor, as quoted above.
- §20.5 (lines 3542-3546, untouched): "The output trailer MUST copy the
  input's unknown ignore-lane flag bits forward and set no other, **in
  place of the flags = 0 §6.3 requires of a file created under this text**
  (`[R-CNT-08]`)." — explicit contrast with the creator's rule.
- Appendix G, item 8 (lines 4708-4712, in the *immediately preceding*
  non-normative appendix, untouched by this hunk): "**The `flags` half is a
  creator's rule**, as item 2's identifier is: a compactor adopting the
  profile carries its input's unknown ignore-lane bits forward instead,
  setting no other (`[R-CNT-08]`)." — and Appendix G's own closing summary
  paragraph (line 4749) restates it again: "its `flags` half a creator's
  rule alone."

So the document's convention, followed with zero exceptions everywhere else
this rule is stated (four separate places, including the sibling appendix
right next to the one this hunk edits), is to name the compactor's carve-out
explicitly every time. Appendix H's new writer-bullet line breaks that
convention: it says "writes flags = 0 on creation" with no carve-out, and —
because Appendix H has no fourth, dedicated "Conforming compactor" checklist
entry at all (I read to the end of the document, line 4831; Appendix H ends
at "Conforming verifier" with nothing further) — a compactor implementer
auditing their own work against Appendix H has nowhere else to look and no
signal that this particular writer-bullet line does not apply to them the
way the rest of the writer bullets (fill recording, boolean-byte encoding,
metadata sorting, commit protocol, alignment/slab) do.

### 6. STRUCTURE CHECK

Structure: the trailer's `flags` field (§6.3), specifically its ignore-lane
half (bits 16-31), as touched by each of the three writer tiers (creator,
appender/updater, compactor) defined in §20.1. All three tiers' obligations
regarding this one field are fixed by `[R-CNT-08]` elsewhere in the
document. The gap this hunk leaves is not an *ungoverned* quantity (the
compactor's actual obligation is fully and correctly stated at §6.3/§20.5)
but a **checklist-routing gap**: Appendix H provides no unambiguous
apparatus for a compactor to locate its own, correct obligation without
already knowing to distrust the writer-bullet's new line — which defeats the
appendix's stated purpose ("for implementers auditing their own work").

### 5. EXHAUSTIVE-CLAIM CHECK

"clears none and sets no other" (line 2) — checked against R-CNT-08's
updater clause: "MUST NOT clear them, and MUST NOT set any other." Matches
exactly, no overclaim. "writes flags = 0 on creation" (line 1) carries no
universal-quantifier language beyond the implicit "whenever creating," which
is accurate for the creator tier specifically — the defect is about scope
*routing* (which actors this checklist entry reaches), not about a false
universal claim within the sentence itself.

### 1. TENSE/QUANTIFIER, 3. LABEL, 7. ANALOGY, 8. ANAPHORA — brief

- Tense/quantifier: both new lines are present-tense, actor-scoped
  statements matching §6.3's own tense and per-actor scoping taken in
  isolation; the defect found is a *routing* mismatch between Appendix H's
  two-bucket taxonomy and §6.3's three-actor taxonomy, not a tense error
  within either sentence.
- Label: both insertions sit in the flowing, unlabeled bullet prose of
  Appendix H — but the *entire appendix* is labeled non-normative by its own
  heading, so (per Check 3's instruction to check the label, not just the
  marker) neither line carries independent normative force regardless of
  contradiction; only `[R-CNT-08]` itself governs, and it is not touched by
  this hunk and remains internally correct. This is why my byte-level
  verdict (below) is negative despite the contradiction.
- Analogy: no "as X"/"the same way" warrant construction in either new
  line. N/A.
- Anaphora: I traced forward and backward through both bullets for stray
  back-references. Line 1's insertion sits between "including both barriers
  (§9.2);" and "honors any alignment or slab it declares (§16)" — a flat
  semicolon list, no pronoun crosses the insertion point. Line 2's insertion
  sits between "re-emits every retained record byte-identically (§20.4);"
  and "respects every record's MU and PE bits, the registry's fixed values
  governing for a registered type (§20.4, `[R-CNT-22]`);" — again a flat
  list, "the registry's fixed values" and "a registered type" are both
  self-contained noun phrases introduced within their own clause, not
  referring back across the insertion. No anaphor reassignment.

### NESTED_DASH check

Neither new line contains any em-dash. N/A.

### Byte-level assessment

Applying the charter's discriminating question ("is the disputed file
itself conforming?") to the scenario this contradiction could actually
produce: a compactor that (misreading Appendix H's writer bullet as
applying to it) writes flags = 0 instead of copying the input's ignore-lane
bits forward. Per `[R-CNF-02]` (§2.3, quoted above, untouched by any hunk),
this exact failure — a compactor writing flags = 0 instead of copying
forward — is one of the **named cases this specification expressly declares
is not a file-conformance violation**: ignore-lane bits are conforming at
any value (§6.3: "a set ignore-lane bit is not a file-conformance
violation... files carrying them are conforming files this text's readers
ignore"). So both the correct behavior (copy forward) and the
misreading-induced behavior (write 0) produce **conforming files** — the set
of byte sequences a conforming implementation may emit does not move; only
the specific (already-unconstrained-by-conformance) ignore-lane bit pattern
in the trailer differs. Combined with Appendix H's own non-normative status
(no independent force; only `[R-CNT-08]` binds, and R-CNT-08 itself is
untouched and unambiguous), this is **not byte-level**. It is a genuine,
well-evidenced documentation defect (an implementer-facing checklist that
contradicts itself for one specific, real actor, in a document that is
otherwise scrupulous about naming this exact carve-out every single other
time it states this rule) but it does not fork what any conforming
implementation may emit or what any reader/verifier must accept or reject.

### Overshoot/undershoot

The repair (adding trailer-flags obligations to Appendix H, per the
charter's framing "two checklist entries in a non-normative appendix gain
the trailer-flags obligations") undershoots: it adds the creator's half and
the updater's half, but omits the third, textually distinct compactor half
that both §6.3 and Appendix G (the sibling non-normative appendix) always
state alongside the other two. It does not overshoot in either bullet taken
alone.

**Verdict for hunk 25: one finding — a checklist contradiction/ambiguity for
the compactor tier, not byte-level.**

---

## Summary of checks that passed cleanly (no finding)

- Hunk 07: all eight checks pass. Verified real-vs-padding consistency
  across six separate statements of the rule (§14.2 itself, `[R-TYP-04]`
  §12.3, §19.4 step 8, §21.1, Rationale, row T2, Appendix H's reader entry)
  plus the packed-planar-bool sibling structure (§14.3) for Check 6. No
  restatement was left stale.
- Hunk 08: all eight checks pass; this hunk is itself the sweep that fixes a
  quantifier defect ("the one byte" → "a byte ... carry") consistent with
  R-SER-08's actual (multi-byte) scope, established independently while
  auditing hunk 07.
- Hunk 25: citations resolve correctly for each bullet taken narrowly against
  its own named tier; no tense, label, analogy, anaphora, or
  exhaustive-claim defect; the one finding is a cross-bullet contradiction
  reachable only by tracing the compactor's dual membership (§20.1/R-CNF-06
  puts it under "updater" for preservation purposes; §20.5 puts it on the
  "creation path" for writing mechanics) through Appendix H's own stated
  "everything a writer does ... plus" composition rule — not visible from
  either new line read in isolation.
