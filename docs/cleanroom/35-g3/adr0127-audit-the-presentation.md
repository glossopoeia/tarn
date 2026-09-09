# Audit transcript — lane "the-presentation"
Hunks audited: hunk-01, hunk-02, hunk-05, hunk-16, hunk-17
Spec file: /Users/robertkleffner/Documents/GitHub/tarn-first-draft/spec/tarn.md

## Disclosure of what was read/run

Files read (only these, per the access rule):
- /Users/robertkleffner/Documents/GitHub/tarn-first-draft/spec/tarn.md (many ranges, listed below)
- /private/tmp/claude-501/-Users-robertkleffner-Documents-GitHub-tarn-first-draft/r35-audit/case/hunk-01.diff
- /private/tmp/claude-501/-Users-robertkleffner-Documents-GitHub-tarn-first-draft/r35-audit/case/hunk-02.diff
- /private/tmp/claude-501/-Users-robertkleffner-Documents-GitHub-tarn-first-draft/r35-audit/case/hunk-05.diff
- /private/tmp/claude-501/-Users-robertkleffner-Documents-GitHub-tarn-first-draft/r35-audit/case/hunk-16.diff
- /private/tmp/claude-501/-Users-robertkleffner-Documents-GitHub-tarn-first-draft/r35-audit/case/hunk-17.diff

Did NOT read: full.diff, other hunk files, docs/, PLAN.md, AGENTS.md, README.md,
conformance/, spec/registry.json, git log/diff, the web. Did not list the case/ directory
(only read the five named files directly).

**Contamination disclosure.** Before this task began, my context already contained (via
system-reminders I did not request): the contents of /Users/robertkleffner/.../CLAUDE.md
(which just points to AGENTS.md — not read), the user's MEMORY.md index (a list of memory
note titles about this TARN project, e.g. "TARN harness spec path", "TARN repair prose vs
rules", "No nested em-dash phrases", etc.), and a git-status block naming five recent commit
subjects ("Cleanroom round 34: charter", "The pre-round-34 audit of ADR-0126: seventeen
defects...", "ADR-0126: decision 1 confirmed", "ADR-0126: round 33's repairs...", "Cleanroom
round 33: one byte-level flag..."). None of this was solicited by me, none of it is part of
the specification, and I did not use it to shape any conclusion below — every finding (or
non-finding) below is backed by a direct read of spec/tarn.md and the hunk files, with
quotations and grep output. I did note that the memory titles and commit subjects broadly
corroborate the charter's own framing (this is a many-round audit project with a history of
subtle repair defects), but I treated that only as atmosphere, not evidence, and drew no
conclusion from it about whether *these particular* five hunks contain a defect.

Scratch files written: none needed — all verification was done via Read/grep against the
spec directly; no local computation file was necessary. (No file written under
r35-audit/scratch/the-presentation/.)

## Hunk headers vs. body — verification

For every hunk, I read the claimed landing line range in the *current* spec file and diffed
it by eye against the hunk's "+" lines, and checked the claimed "nearest preceding heading."
All five matched exactly, no discrepancy:

- hunk-01: lines 604-606 == hunk's "+" lines verbatim. Preceding heading confirmed: line 594,
  "#### 4.7 Field taxonomy and presentation".
- hunk-02: lines 619-622 == hunk's "+" lines verbatim. Same preceding heading (594).
- hunk-05: line 2642 == hunk's "+" line verbatim. Preceding heading confirmed: line 2636,
  "#### 18.2 Encoding".
- hunk-16: line 4587 == hunk's "+" line verbatim. Preceding heading confirmed: line 4573,
  "### Appendix F — Normative references".
- hunk-17: lines 4717-4722 == hunk's "+" lines verbatim. Preceding heading confirmed: line
  4593, "### Appendix G — Reproducible-writer profile (non-normative)".

## Force under R-CNF-01 (label, not marker)

R-CNF-01 (quoted from doc, line ~110-ish region and restated in the charter): normative
except §1, text labeled Note/Example/Rationale, and appendices identified non-normative.

- Hunk-01 lands in the main run of §4.7 (lines 596-609), which is plain text, NOT inside a
  blockquote at all. **Normative.**
- Hunk-02 lands inside the blockquote at lines 611-627, which opens "> **Note.** Layout
  tables...". **Labeled Note — non-normative.**
- Hunk-05 lands in a table cell (line 2642) inside plain running prose of §18.2 (no
  blockquote, no label). **Normative** (it is a normative table, "under a Class column" that
  already assigns "structural" — this is exactly the case the charter warns about: a table
  in unlabeled text binds).
- Hunk-16 lands in Appendix F, "Normative references" — the heading carries no
  "(non-normative)" qualifier (contrast Appendix E "(non-normative)" and Appendix G
  "(non-normative)", which DO carry it). **Normative appendix.**
- Hunk-17 lands in Appendix G, whose heading is explicitly
  "Reproducible-writer profile (non-normative)". **Non-normative appendix**, and the text
  itself says "It adds no requirement to any actor."

This matches the charter's own claim ("one normative prose, one labelled Note, one table
cell in normative text, one normative appendix, one non-normative appendix") exactly, and I
verified it independently rather than taking the charter's word.

---

## HUNK 01 — [R-ENC-16]'s descriptive test

### The rule the repair adopts
Before: a field is descriptive only if "its value determines nothing a conforming reader
does." After: "...nothing a conforming reader **or verifier** does." The rule this makes
true: the actor-set the descriptive test ranges over is widened from {reader} to
{reader, verifier} — matching the actor-set the STRUCTURAL test already used one sentence
earlier (unchanged context, line 598-599: "anything a conforming reader or verifier does with
the bytes it reads").

### Check 1 — tense/quantifier/actor
The generation in question is present-tense/atemporal (a classification rule, not a
commit-state rule) — no tense issue. The actor-set changed as described. Crucially, I
confirmed the *structural* test's actor-set ("reader or verifier") was **already present
before this hunk**, as unchanged context on line 599 (visible in the hunk file itself, which
shows it as a context line, not a "+"/"-" line). So the repair is not inventing a new
actor-set; it is porting the pre-existing actor-set from the structural half of the
definition into the descriptive half, which is defined explicitly as the complement of the
structural one ("descriptive if it determines **none of those**" — line 603, unchanged). A
descriptive-vs-structural pair whose two halves quantify over different actor-sets is
internally inconsistent; the repair removes that inconsistency. This is a repair I can defend
as *required by the document's own definition*, not merely stylistically nicer.

### Check 2 — citations
- `[R-ENC-16]` — this is the requirement being defined by this very paragraph (grep shows it
  appears nowhere else: `grep -n "R-ENC-16" tarn.md` → only line 609). Self-defining, not a
  forward reference. PASS (nothing to mis-cite).
- `[R-CNT-07]`, `[R-MTA-02]`, `[R-SEC-06]` — untouched context citations, cited as already
  using "the sense" of the structural test. Checked each:
  - `[R-CNT-07]` (line 884): "A reader MUST NOT reject a file for its version_minor... all
    feature gating is structural." Consistent with "whether ... is accepted at all" sense.
    PASS.
  - `[R-MTA-02]` (line 2634): "A reader MUST NOT let any part of a user-metadata document
    affect how a byte is located, decoded, or returned." Matches "where a byte lies, how it
    decodes, what a decoded value is" sense exactly. PASS.
  - `[R-SEC-06]` (line 4223, context: "...is located or decoded.") Matches the same sense.
    PASS.

### Check 3 — normative placement
Confirmed above: plain prose, not inside any Note/Example/Rationale block. The repair lands
in force. PASS.

### Check 4 — contradiction in the same passage
Re-read the whole of §4.7's first paragraph (596-609) and the Note (611-627). No carve-out
elsewhere in this passage collides with the widened test. The Note (unaffected by hunk-01)
doesn't restate the reader-only phrasing.

### Check 5 — exhaustive claims
"version_minor is the only descriptive field" (unchanged sentence, immediately after the
touched text) is the live exhaustive claim to stress. See the dedicated sweep below — it
survives.

### Check 6 — what else is unconstrained
The structure here is the binary taxonomy itself (every field of the format is either
structural or descriptive, per line 597 "each class being what the one before it is not").
Every layout table's Class column instantiates this partition. I did not find any field
whose Class-column entry is missing (spot-checked §6.1, §6.2, §7.2, §15.1, §18.2 — full grep
of `^| Offset` below; every row I looked at carries a Class value). Not a defect site for
this hunk.

### Check 7 — analogy
No "exactly as," "the same way," etc. construction is introduced by this hunk's own text.
(The surrounding sentence *cites* three requirements as already using "the sense" the
definition states, which I checked under Check 2, but that's citation, not an analogy
argument of the kind Check 7 targets.)

### Check 8 — anaphor / back-reference
Read forward through the rest of §4.7 (through line 627). No bare "it"/"this"/"that" in the
text following the insertion resolves to something the insertion changed. The one "it" in
"a reader MUST NOT alter decoding based on it" resolves to "its value" (the field's value) —
unaffected, same referent before and after. The later "it" in "when the field contradicts the
data it describes" resolves to "the field" — unaffected. PASS.

### The targeted sweep: does "version_minor is the only descriptive field" survive?

I grepped every place version_minor's *value* could drive a reader-or-verifier action:

```
grep -n "version_minor" tarn.md
607: ...version_minor is the only descriptive field...
834: | 10 | 2 | u16 | version_minor | descriptive | any (see §6.3) |
883: A reader MUST NOT reject a file for its version_minor: minor releases are
     additive-only, and all feature gating is structural... [R-CNT-07]
914-918: A writer SHOULD emit the lowest version_minor... [R-CNT-26] (writer-side SHOULD)
3334-3335: (compactor context, writer-side)
3532-3535: the output's version_minor SHOULD be at least the input's... [R-CNT-26] (compactor,
     writer-side SHOULD)
3921: | version_minor is higher than this text defines | Accepted; minors never gate |
     [R-CNT-07] |
4439: (conformance-vector byte listing, not a behavior)
4709-4715: Appendix G item 8 (profile-only, non-normative, writer-side)
4752: (Appendix G item 8 restated in intro list, non-normative)
```

None of these is a *verifier* action keyed to version_minor's value that falls inside the
structural test's four criteria ("where a byte lies, how it decodes, what a decoded value is,
or whether the file/layer/tile is accepted at all"). The only place a verifier's behavior
could depend on version_minor at all is the SHOULD-deviation advisory mechanism at lines
329-335 (`[R-CNF-12]`): "a verifier reports a SHOULD deviation as an advisory that does not
bar certification... reported where the verifier observes it and not hunted for." Even if a
verifier happens to notice `[R-CNT-26]`'s floor SHOULD is unmet and reports it, that reporting
does not change "whether the file... is accepted at all" (SHOULD deviations never bar
certification, per the same rule) — so it is not one of the four listed structural
consequences. Control check: I confirmed `[R-CNT-07]`'s MUST NOT-reject rule at line 882-884
is unconditional and not qualified by version — a reader/verifier's *rejection* behavior never
turns on version_minor's value. Conclusion: the closing sentence survives the widening. No
defect found here.

### A further stress-test the charter asked for: reserved flag bits and a registered type's
### stored MU/PE bits, through both tests + §7.2's Class column

Read §7.2 (lines 1000-1102) in full.

- Record flags field (line 1008): "flags: bit 0 MUST_UNDERSTAND, bit 1 PRESERVE_ON_EDIT,
  bits 2-15 reserved | structural" — the whole field is classed structural in the Class
  column, as a unit.
- Reserved bits specifically: "Reserved flag bits: writers MUST emit zero; readers MUST
  ignore them" (line 1019-1020) — a plain *reader* does nothing different based on a reserved
  bit's value (this is exactly the shape the OLD, narrower test would have missed: under the
  old wording "nothing a conforming reader does," reserved bits' effect *would have* satisfied
  the descriptive test in isolation). But: "a verifier MUST treat a nonzero reserved flag bit
  ... as a validity error at the record's governing scope" (line 1025-1026, `[R-CNT-12]`) — a
  verifier's accept/reject behavior DOES depend on the reserved bits' value. Under the NEW
  (widened) test this correctly keeps the whole flags field out of "descriptive," consistent
  with its Class-column value. Under the OLD test, taken bit-by-bit rather than field-by-field,
  there would have been a latent inconsistency (a sub-behavior of the field visible only to a
  verifier, which the old descriptive wording's actor-set didn't cover) between the taxonomy's
  own definition and the Class-column answer — the repair removes exactly this class of
  inconsistency at the field level, even though the taxonomy is defined over whole fields, not
  bits, so this was never a live contradiction in the Class column itself, just a latent one in
  the definition's own actor-completeness.
- Registered-type stored MU/PE bits (§7.3, lines 1089-1102): "A reader MUST apply a known
  type's specified semantics regardless of its stored MU and PE bits — a flipped stored bit
  never changes conforming behavior — and a verifier MUST treat the mismatch as a validity
  error" (`[R-CNT-22]`). Same shape: a plain reader's behavior is invariant to the stored bits
  (fixed registry semantics apply regardless), but a verifier's behavior (reject on mismatch)
  is not. Again, this is already captured because the bits live inside the (already
  structural) "flags" field of §7.2's Class column — not a second, hidden descriptive field —
  but it is exactly the kind of case that motivates widening the descriptive test's actor set,
  and it is consistent with, not contradicted by, the repair.

Conclusion for hunk-01: the repair is correct, required by the document's own definitions, and
survives every downstream check I could run. No finding.

---

## HUNK 02 — §4.7's Note

### The rule the repair adopts
Extends the Note's account of which layout tables depart from the "canonical six columns"
(offset, size, type, name, class, valid range): (a) §6.1's Value column replaces THREE
things — type, name, and range (previously the Note said it replaced only type and range,
omitting that §6.1 also has no Field/name column); (b) §7.2's table folds a field's *range*
into its Field cell **only where it states one**, and for the fields where it doesn't (length
and extent fields), the bound is stated in the prose rules below the table, not omitted.

### Check 2 — citations / table audit
I opened all five tables the charter named plus cross-checked for any other layout table in
the document:

```
grep -n "^| Offset" tarn.md
787:  | Offset | Size | Value | Class |                              (§6.1, 4 cols)
830:  | Offset | Size | Type | Field | Class | Valid values |         (§6.2, 6 cols — full)
1005: | Offset | Size | Type | Field | Class |                       (§7.2, 5 cols — no VV)
2193: | Offset | Size | Type | Field | Class | Valid values |         (§15.1, 6 cols — full)
2640: | Offset | Size | Type | Field | Class | Valid values |         (§18.2, 6 cols — full)
```//
This is every "| Offset"-headed table in the document — no sixth table exists that the Note's
generalization would need to but doesn't cover.

- **§6.1** (lines 783-792): columns are Offset|Size|**Value**|Class. No Type column, no
  Field/name column, no Valid-values column — three columns (type, name, range) are indeed
  absent, replaced by the single Value column. The repaired Note text ("a Value column
  replaces type, name and range") is now accurate; the PRE-repair text ("replaces type and
  range") was wrong by omission (it never accounted for the missing Field/name column). This
  is exactly the kind of fix the charter describes. PASS — repair is correct and necessary.
- **§7.2** (lines 1000-1011): columns are Offset|Size|Type|Field|Class — no Valid-values
  column at all. Five fields: type, flags, inline_length, extent_offset, extent_length.
  - "type (0 invalid)" (line 1007) — range folded into the Field cell. ✓.
  - "flags: bit 0 MUST_UNDERSTAND, bit 1 PRESERVE_ON_EDIT, bits 2-15 reserved" (line 1008) —
    range/meaning folded into the Field cell. ✓.
  - inline_length (line 1009): Field cell says only "inline_length" — no range in-cell. Bound
    is stated below the table: "The sequence MUST parse as zero or more complete records with
    no residue. A record whose header or inline payload would extend past the end of its
    containing record sequence is a validity error..." (lines 1013-1017), and register row F29
    (line 3763) confirms this rule is what governs inline_length overrun. ✓ "stated in the
    rules below the table."
  - extent_offset / extent_length (lines 1010-1011): Field cells give no range. Bounds stated
    below: "an extent_offset < 16, an extent extending past F − 64, or an overflowing sum...
    is a validity error" (lines 1029-1037). ✓.
  - So the five fields divide exactly as the repaired sentence claims: 2 fields with range
    folded into the Field cell (type, flags), 3 fields ("its length and extent fields") whose
    bounds are in the prose below (inline_length, extent_offset, extent_length). 2+3=5, all
    accounted for, none double-counted, none omitted. PASS.
- **§6.2** (trailer, lines 825-841): full six columns, no departure to describe; consistent
  with "each table giving the columns its structure needs." Not mentioned by the Note and
  needs no mention (nothing anomalous). version_major's cell ("1 (0 invalid; others: §6.3)")
  is a useful precedent for hunk-05, see below.
- **§15.1** (lines 2179-2201): full six columns, no departure. Same as above.
- **§18.2** (lines 2636-2642): full six columns (before AND after hunk-05's edit — hunk-05
  only changes the *content* of the Valid-values cell, not which columns exist). No departure
  for the Note to describe.
- **§7.4** (the layer record's inline payload, lines 1104-1127): NOT an "| Offset"-headed
  table at all — its header is "| Field | Type | Constraint |" (line 1110), confirmed by
  `grep -n "^| Field | Type"` returning exactly one hit, at 1110. This is the "packed
  variable-length payload" case the Note describes separately and which the hunk does not
  touch: "its table omits the offset, size and class columns... and each field's class from
  the definitions above." I verified §7.4 is the *only* such table in the document (no sibling
  "Field|Type|..." table exists), so the Note's singular treatment ("the layer record's inline
  payload (§7.4)") is not under- or over-inclusive.

### Check 3 — normative placement
Confirmed: this lands inside "> **Note.**" (line 611) — non-normative by R-CNF-01's own label
rule. The repair therefore adds descriptive/explanatory color but creates no new obligation on
any actor — consistent with a Note's role. Nothing here is a normative statement that needed
to land in unlabeled text; it's genuinely explanatory of table structure, so the Note is the
right home for it. Not a defect (I checked deliberately for the inverse failure mode the
charter warns about — "if the rule's only statement is inside a Note, the repair has no
force" — but this text isn't imposing a new rule; it's cataloguing existing table shapes that
are independently normative in their own sections (§6.1, §7.2 themselves are normative), so
there's no orphaned obligation here).

### Check 4 — contradiction
Re-read the whole Note (611-627) and the surrounding sections named. No contradiction found:
the claim that §7.2 "folds a field's range into its Field cell where it states one" does not
collide with anything in §7.2's actual prose or table.

### Check 5 — exhaustive claims
"where it states one" is a deliberate hedge, not a "for every field" claim — checked and it is
honest (3 of 5 fields do NOT have an inline range). "its length and extent fields' bounds
being stated in the rules below the table" — verified true for all three (inline_length,
extent_offset, extent_length) via the citations above.

### Check 6 — unconstrained siblings
Structure: the set of all layout tables in the document. I enumerated all of them (five
"Offset"-headed plus the one "Field|Type|Constraint" table) and found none left unaccounted
for by the Note's generalization + its two named exceptions (§6.1, §7.2) + its one separate
exception (§7.4). No sibling table silently left in an unconstrained state.

### Check 7 — analogy
No "exactly as X" construction introduced by this hunk.

### Check 8 — anaphor
Read forward through the rest of the Note (through line 627). The sentence immediately after
the insertion — "A variable-length field's value includes its length prefix, so a name is
structural: it determines where the field after it begins" — is unchanged context. Its "it"s
resolve to "a name" (a specific field of §7.4's table) both before and after the insertion;
the insertion doesn't sit between this sentence and its antecedent (the antecedent, "a name,"
is self-contained within the same sentence). No drift.

Conclusion for hunk-02: repair is accurate, matches the actual table structures exactly, and
introduces no new problem. No finding.

---

## HUNK 05 — §18.2's cell

### The rule the repair adopts
The Valid-values cell for the `encoding` field now states the full value-domain partition
inline (1,2 assigned; 0 invalid; 3-0x7F reserved; ≥0x80 experimental) rather than just "1 or
2; see below."

### Check 2 — citations / cross-references
- **Paragraph below the table** (lines 2644-2653): "0 is invalid; 1 = none and 2 = zstd are
  assigned; 3 through 0x7F are reserved; values ≥ 0x80 are the experimental range (§10)."
  Matches the new cell text term for term. PASS.
- **§10.2** (lines 1564-1587), the "metadata encoding (§18.2)" row of its space-partition
  table (line 1581): "u8 | 1, 2 | 3–0x7F | ≥ 0x80" for Assigned/Reserved/Experimental. Exact
  match to the new cell. PASS.
- **R1** (§21, line 3895): "A user-metadata record declares a document encoding of 0, or a
  reserved-range value (3-0x7F)" — confirms 0 and 3-0x7F are violations, and (by omission)
  confirms experimental (≥0x80) is NOT a violation under R1 — consistent with the cell not
  listing ≥0x80 as invalid. PASS.
- **§21.6's experimental-encoding entry** (line 3924): "A user-metadata record declares an
  experimental-range (≥ 0x80) document encoding | Ignored (ignore-record); the file is
  conforming..." — confirms ≥0x80 is not a violation, consistent with the cell's "experimental"
  label (not "invalid"). PASS.

### Check 5 — exhaustive claim / "valid values" heading tension
The charter specifically asks: can a cell under a "Valid values" heading carry values that
are not valid? I checked the precedent directly. §6.2's trailer table, version_major row
(line 833): "1 (0 invalid; others: §6.3)" — under the SAME "Valid values" header (line 830),
this row already states an explicitly-invalid value (0) and defers others to prose. The
`flags` row (line 835) does the same for the full incompat/ignore-lane partition, invalid bits
included. So there is direct, pre-existing precedent in this very document for a
"Valid values" cell describing the whole value-domain partition, invalid/reserved entries
included, not literally only the valid ones. Hunk-05's cell is consistent with this
established convention, not a new departure. Not a defect.

I also checked how §6.2 and §7.4 handle their OWN reserved/experimental ranges (as the
charter asked):
- §6.2's version_major row: "1 (0 invalid; others: §6.3)" — defers detail to §6.3's prose
  (which itself covers major, not reserved/experimental numeric spaces the way §10.2 does,
  since format-major isn't one of §10.2's eight spaces).
- §7.4's index_encoding row (line 1124), under the "Constraint" column (§7.4 has no
  "Valid values" header — it has Field|Type|Constraint): "1 = raw-segmented; any other
  value — including 0, reserved 2–0x7F, and the experimental range ≥ 0x80 (§10) — is a
  validity error at layer scope (§15)." This is the SAME style hunk-05 now uses (full
  partition spelled out in the cell) but under a differently-named column ("Constraint" vs
  "Valid values"). So hunk-05 brings §18.2's cell into the same *style* §7.4 already uses for
  an analogous reserved/experimental partition, even though the column header name differs.
  Consistent, not contradictory.

### Check 3 — normative placement
This is a table cell in unlabeled running text (§18.2, no blockquote) — normative, and I
confirmed it lands in force (there is no competing statement of the same rule sitting only in
a Note/Example/Rationale elsewhere that would make this the "orphaned" edit).

### Check 4 — contradiction
Checked the whole of §18.2 (lines 2636-2732, read in full) for a carve-out that collides with
the widened cell. None found: the paragraph immediately below (2644-2653) restates the same
partition without conflict, and the later discussion of encoding 2 / RFC 8878 frame
constraints doesn't touch the encoding-byte value-domain at all.

### Check 6 — unconstrained siblings
Structure: the numeric-identifier-space partition (assigned / reserved / experimental) that
every one of §10.2's eight spaces carries. I checked whether the *other seven* spaces have
their own reserved/experimental ranges pinned somewhere (they do — §10.2's table lists all
eight uniformly, and L31/L33/L34/L36/L43/L45/F36/L25/R1 in §21 register violations for each).
This hunk only touches the metadata-encoding cell in §18.2; the other seven spaces' own
layout-table cells are outside this hunk's charter and I did not find hunk-05 claiming
anything about them. Not a defect of this hunk.

### Check 7 — analogy
No "exactly as" construction in the new cell text itself.

### Check 8 — anaphor
The paragraph immediately following the table (lines 2644-2653) is unchanged; no pronoun in
it changed referent because of the cell-only edit.

Conclusion for hunk-05: repair matches §10.2, R1, §21.6 and the paragraph below the table
exactly, and is stylistically consistent with existing "Valid values"/"Constraint" cell
practice elsewhere (§6.2, §7.4). No finding.

---

## HUNK 16 — Appendix F's [RFC 9110] entry

### The rule the repair adopts
Adds a normative-reference entry for RFC 9110 (HTTP Semantics), attributing to it the terms
"range requests, status codes and content length," and citing §6.4 / `[R-CNT-10]` as where
those terms are used.

### Check 2 — citations, word for word against §6.4 and R-CNT-10
Read §6.4 in full (lines 920-958). Terms actually present in §6.4's body:
- "a suffix range" / "range request" (lines 923, 948, 950-951) — matches "range requests."
- "200 response" (line 948) — a specific HTTP status code; matches "status codes" as a
  category (the entry doesn't claim §6.4 uses *multiple* distinct codes — I checked and only
  200 is named there — but "status codes" as RFC 9110's defined concept is what's being cited,
  not a count of how many the spec text itself enumerates, so this is not an overclaim).
- "content length" (line 954, verbatim: "a full-response content length, the complete length
  of a range response, or a size probe") — matches "content length" exactly.
`[R-CNT-10]` is the label at the end of the paragraph containing both the 200-response
handling and the content-length-comparison MUST (lines 948-958) — so the citation's claim
that these terms are "in which... `[R-CNT-10]`" is stated is accurate. PASS on substance.

### Check 3 — normative placement / does the entry's *form* match its siblings — deeper check
Appendix F carries no "(non-normative)" qualifier (contrast Appendices E and G, which do) —
confirmed normative appendix, and the entry lands in force.

Bullet-list *syntactic* form matches every sibling entry: `**[ID]** Title — description
(§ref).` Checked against RFC 3720, RFC 8878, LZ4 Block, RFC 3339 entries — same shape. PASS on
syntax.

However, I went one level deeper (the charter's own phrase "does the entry's form match the
appendix's other entries" invites this) and checked whether every OTHER entry in Appendix F
corresponds to an explicit **inline naming** of that standard somewhere in the document body
(not just a matching *concept*):

```
grep -n "RFC 8878\|RFC 3720\|RFC 3339" tarn.md   -> named inline at lines 514, 2465, 2847, etc.
grep -n "IEEE 754\|LZ4 Block\|BCP 14\|RFC 2119\|RFC 8174" tarn.md -> all named inline
  (lines 101-102, 1797-1816, 2512)
grep -n "RFC 1950\|RFC 1951\|RFC 1952" tarn.md -> all named inline (lines 2450-2451, 3859)
grep -n "RFC 9110\|9110" tarn.md -> ONLY the Appendix F entry itself (line 4587)
```
Every other one of the eight Appendix F entries has its standard's name or number spelled out
somewhere in the normative body text that uses it (e.g. "RFC 3720 §12.1," "as defined by RFC
1951," "IEEE 754 binary32," "RFC 3339 date-time"). RFC 9110 is the only entry where the body
section it's attributed to (§6.4) never once writes "RFC 9110" or "HTTP" — it uses only the
generic terms (range request, 200 response, content length) that happen to be HTTP concepts,
without an inline citation pointing back to the standard. This is a genuine asymmetry in
citation practice versus every sibling entry, even though the *substance* of the attribution
(that these are RFC-9110-defined terms) checks out and the syntactic list-item form matches.

I considered elevating this to a full finding, but decided against treating it as a defect:
Appendix F carries no stated rule that every entry must correspond to an inline-named
citation (there is no sentence anywhere requiring that), and the entry's content is accurate
about what RFC 9110 covers and where those concepts are used. I report the asymmetry as an
observation (see `rejected_candidates`) rather than a finding, because I could not locate a
rule this asymmetry actually violates — it's a difference in the *document's habits*, not a
misstatement, and it does not fork any byte.

### Check 5 — exhaustive claim: "any other document a MUST is stated in still absent?"
I cross-referenced every bracketed external-standard citation used anywhere in the running
text against Appendix F's list:
```
grep -noE "\[(RFC|IEEE|BCP|Unicode|LZ4 Block)[^]]*\]" tarn.md | sort -u
-> [BCP 14] [IEEE 754] [LZ4 Block] [RFC 1950] [RFC 1951] [RFC 1952] [RFC 2119] [RFC 3339]
   [RFC 3720] [RFC 8174] [RFC 8259] [RFC 8878] [RFC 9110] [Unicode]
```
Every one of these is present in Appendix F (BCP 14 subsumes RFC 2119 + RFC 8174 in one
entry, as the body itself does at lines 101-102). I also swept for other external-standard
smells not caught by the bracket convention (HTTP, media type, MIME, URI, URL):
```
grep -n "HTTP\|media type\|MIME\|URI\|URL\b" tarn.md
-> line 819 ("media type" — inside a Note, non-normative, no MUST attaches) and line 4587
   (the entry itself)
```
No other MUST-bearing external document is absent from Appendix F. PASS.

### Check 4 — contradiction
No competing statement anywhere else attributes these HTTP terms to a different or no
standard.

### Check 8 — anaphor
This hunk only inserts a new bullet list item; it doesn't sit between two sentences of running
prose with a pronoun that could re-resolve. Checked the entries immediately before and after
(RFC 3339, then Unicode) — neither refers back to "the previous entry" or similar, so no
anaphor is affected by the insertion's position in the list.

Conclusion for hunk-16: substantively accurate, syntactically consistent with siblings, no
missing MUST-bearing reference found. One genuine (but rule-less, non-byte-level) asymmetry
noted and explicitly not elevated to a finding — see rejected_candidates.

---

## HUNK 17 — Appendix G item 8

### The rule the repair adopts
Before: "A compactor's output is therefore reproducible only modulo its trailer: [file_id
reason], and [version_minor-floor reason]." After: adds a second reproducibility gap —
"...modulo its trailer AND the records §20.4 lets it drop... and a record whose governing
flags are MU = 0 and PE = 0 is retained or dropped at the compactor's choice (§20.4), which no
item here pins."

### Check 2 — citations, word for word
Read §20.4 in full (lines 3415-3479) and §20.5 in full (lines 3480-3560+).
- "governing flags" — the EXACT header of §20.4's table (line 3441: "| Governing flags |
  Updater obligation |"). Verbatim match, not a paraphrase.
- MU=0/PE=0 row (line 3445): "Retain byte-identical, or drop it — its extent becoming slack.
  ...an updater MAY drop the record in any commit it is otherwise free to make... and a
  compactor MAY drop it whenever it rewrites the file." This is exactly "retained or dropped
  at the compactor's choice." PASS, word for word.
- `[R-WRT-06]` — the label governing §20.5's compaction rules (confirmed at line 3539), whose
  "fresh file_id" language is confirmed at line 3498-3502 ("It MUST mint a fresh file_id for
  the output — a new draw..."). PASS.
- §20.5's floor language (lines 3524-3535): "the output's version_minor SHOULD be at least the
  input's: a compactor cannot know which minor version defined a feature it does not
  implement..." — matches "this item's floor turns on which features the compactor
  implements." PASS.

### Check 6 — unconstrained siblings / is the new list of exceptions now complete?
Structure: everything a "byte-identical, reproducible-under-the-profile" compactor output
could vary in, across two different conforming compactors given the same input, all nine
profile items applied. I went through the full list of degrees of freedom the base format
(§20.5) leaves a compactor and checked whether each is closed by SOME item in Appendix G, or
is a genuine remaining gap the sentence should (and does, or doesn't) name:

| Degree of freedom in §20.5 | Closed by | Left open, and named by item 8? |
|---|---|---|
| file_id (fresh draw, `[R-WRT-06]`) | NOT closed — item 2 explicitly excepts it | Yes, named ("R-WRT-06's fresh file_id is no function of content") |
| structure placement / order ("preserves no placement," line 3541) | Item 3 (total emission order, fixed extents/layout/alignment via item 5) | Closed by another item — correctly NOT named in item 8 |
| tile-index relocation / entry offsets | Deterministic once placement is fixed (item 3+5) | Correctly not named |
| version_minor floor when output carries an unimplemented feature | NOT closed — §20.5's SHOULD is implementation-dependent | Yes, named ("this item's floor turns on which features the compactor implements") |
| flags (ignore-lane bits) | Closed — deterministic function of input (copy forward, §20.4/`[R-CNT-08]`) | Correctly not treated as a further gap |
| MU=0/PE=0 record retain-vs-drop (§20.4's table) | NOT closed by any of the 9 items (checked each: 1-codec, 2-file_id, 3-order, 4-one generation, 5-alignment/slab/filter/extents/layout, 6-sentinel, 7-fill default, 8-itself, 9-user metadata — none pins this) | Yes — this is the hunk's own addition, and it's accurate |

I did not find a further, still-unmentioned gap. The sentence's list (trailer + dropped
records) appears complete against the structure it governs.

### Check 5 — exhaustive claim
"which no item here pins" — I verified this by checking all nine items individually (table
above); none of items 1-7 or 9 touches whether an unregistered MU=0/PE=0 record is retained.
Confirmed true, not an overclaim.

"reproducible only modulo its trailer and the records §20.4 lets it drop" — checked this is
not an undercount (see table above — I could not find a third gap) nor an overcount (both
named gaps are real, verified against §20.4/§20.5 above).

### Check 4 — contradiction
Read the whole of item 8 (4709-4724) and adjoining items 7 and 9. No collision: item 9's
"as item 1 pins a tile codec" analogy for user-metadata reproducibility doesn't touch record
dropping; item 7's fill-default discussion is unrelated to record retention.

### Check 7 — analogy
"An adopter needing byte-identity across compactors pins the compactor, as items 1 and 9 pin
their producers." Compared side by side:
- Item 1's verb: "pins" a **named codec implementation at a named version with fixed encoder
  settings** (an implementation-and-version pin).
- Item 9's verb: "pins" the **producer** — "a named JSON writer at a named version... a named
  zstd implementation at a named version" (same shape).
- Item 8's closing verb: "pins the compactor" — pins the **whole writer program** at a
  specific implementation, which is the same kind of fix (name a specific piece of software)
  applied to a different piece of software (the compactor rather than a codec/JSON-library).
Both sides range over "a specific implementation, held fixed" — the quantifier match holds. I
checked one further wrinkle: does "pinning the compactor" actually resolve file_id's
freshness? No — file_id is drawn fresh **per run** regardless of which compactor binary is
used (item 2: "a compactor adopting the profile takes [R-WRT-06]'s fresh draw instead"), so
pinning the compactor implementation does not make two RUNS of it byte-identical in file_id.
This looks at first glance like the closing sentence overclaims. But re-reading item 2 and the
appendix's own framing (para. before item 1: "conformance to the profile can be refuted
cheaply but confirmed only by reproducing the file"), file_id's unreproducibility-by-design is
already flagged as a standing, acknowledged exception at item 2 itself, independent of item 8;
item 8's closing sentence about "pinning the compactor" is doing the same job item 9's
closing sentence does for its own item (closing the *implementation-choice* degrees of
freedom: version_minor-floor policy and MU=0/PE=0 drop policy), not claiming to also cure
file_id's inherent freshness, which was never in dispute and is separately excepted. This
wrinkle **predates the repair** — the pre-repair text already paired the fresh-file_id
sentence with the same closing "pins the compactor" sentence, so nothing about hunk-17's
insertion changes this reading. Not a new defect introduced by this repair.

### Check 8 — anaphor
Read forward from the insertion to the end of item 8 and into item 9. Back-references
checked:
- "this item's floor" (unchanged context) — resolves to item 8's own version_minor floor,
  unaffected by the insertion (the insertion sits after this phrase in the sentence, not
  between it and its antecedent).
- "which no item here pins" (new text) — resolves to the immediately preceding clause (the
  MU=0/PE=0 drop-or-retain choice), a same-sentence, local antecedent. Correct both before
  (didn't exist) and after.
- "An adopter needing byte-identity across compactors pins the compactor" — "the compactor"
  is a fresh noun phrase, not a pronoun; no resolution issue.
- "as items 1 and 9 pin their producers" — "their" resolves to items 1 and 9's respective
  writer components (codec implementation; JSON/zstd implementation) — unaffected by the
  insertion, which sits entirely before this final sentence and doesn't alter what "items 1
  and 9" refers to.
No anaphor whose resolution changed as a result of the insertion.

Conclusion for hunk-17: repair correctly identifies and names a genuine, previously-omitted
reproducibility gap (MU=0/PE=0 record retention choice), verified word-for-word against
§20.4's table and cross-checked against all nine profile items for completeness. No finding.

---

## Sweep for other statements of the same two subjects (descriptive test; compactor
## reproducibility), per the charter's blanket instruction

Descriptive-field test restatements:
```
grep -n "descriptive" tarn.md
21, 603, 605, 607, 834
```
Line 21 (the front-matter Note, lines 12-23) restates structural/descriptive WITHOUT naming
an actor at all ("its value affects where a byte lies..."/"none of those") — actor-agnostic,
so it cannot conflict with either the old or new actor-set at line 604-605. Not something the
repair needed to (or should) sweep.

Compactor-reproducibility restatements:
```
grep -n "reproducib" tarn.md
4596 (intro, "byte-identical output"), 4611 (item1, "unattainable for codecs 2-4"),
4674 (item4, "reproducible only in the weaker sense"), 4716-4717 (item 8, the hunk itself),
4729 (item 9, "reproducible but explicitly do not make two writers' output identical")
```
Each of these is a *different item's own* reproducibility caveat (codec choice, one
generation, user metadata) — none of them restates item 8's specific compactor-trailer claim,
so there is no sibling restatement of item 8's claim elsewhere that the repair should have
swept and didn't.

## Byte-level assessment, all five hunks

None of the five repairs moves the set of bytes a conforming writer may emit or that a
conforming reader/verifier must accept or reject:
- Hunk-01/02 are classification/explanatory text (Note, and a definitional actor-set clarify)
  that doesn't change any MUST/MUST NOT on bytes — verified no reader/verifier behavior
  actually changes (the "gap" it closes was already latent/consistent at the field level).
- Hunk-05's cell restates, in a table cell, exactly what the prose below the table and §10.2
  already require — no writer behavior or reader/verifier verdict changes; two implementations
  reading old-cell vs new-cell text would reach the same accept/reject decisions because the
  governing prose (unchanged) already fully specifies the partition.
- Hunk-16 adds a reference-list entry; it creates no new MUST and changes no accept/reject
  behavior.
- Hunk-17 is in a non-normative appendix that "adds no requirement to any actor" by its own
  stated terms (line 4599-4600) — by construction nothing here can be byte-level, since the
  appendix itself is opt-in guidance for adopters wanting byte-identity, not a conformance
  requirement on core writers/readers/verifiers.

I found no byte-level fork in any of the five hunks.
