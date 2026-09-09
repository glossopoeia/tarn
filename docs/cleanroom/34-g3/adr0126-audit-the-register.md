# Audit transcript — hunks 13, 14, 15, 16 (§21's conventions, two cells, normative references)

Auditor scope: hunk-13.diff, hunk-14.diff, hunk-15.diff, hunk-16.diff only.
Access used: spec/tarn.md (read + rg), the four hunk files. No other file read.

## Disclosure

I read exactly: the four hunk files named in the charter
(`/private/tmp/.../r34-audit/case/hunk-13.diff` through `hunk-16.diff`), and
`/Users/robertkleffner/Documents/GitHub/tarn-first-draft/spec/tarn.md` (via
`Read`/`sed -n` and `grep`/`awk` over it). I ran only `grep`, `awk`, `sed`,
`wc`, and a small inline `python3` script that reads a scratch file I wrote
myself (never any other repo file). I wrote working files only under
`/private/tmp/.../r34-audit/scratch/the-register/`:
`governing_cells.tsv` (a first, broken extraction attempt — abandoned),
`gov_cells2.txt` (broken — FS='|' off-by-one), `gov_cells3.txt` (the
corrected Governing-rule-column extraction for all 120 register rows),
`instances_raw.txt` / `instances_raw2.tsv` (broken — wrong column) and
`instances_raw3.tsv` (the corrected Instances-column extraction for all 120
rows). No file outside that directory and the two permitted inputs was
written or read.

A system-reminder appeared mid-session (an "Auto Mode Active" notice
instructing me to prefer Bash over the Read/Edit/Write tools generically for
this harness). It is host tooling guidance, not case material — it named no
finding, no verdict, and no position for this round, so I disregarded it as
evidence and used it only to decide which tool to reach for (Bash, which the
access rule explicitly permits for grep/awk/local computation). No other
unrequested context appeared naming a round result or a prior finding.

No path disagreement: all four hunk files were exactly where the charter
said, and each hunk's own header line ("lands in spec/tarn.md at lines
NNNN-NNNN") matched the section I found there once line-drift from other
edits earlier in the file was accounted for (the hunk headers explicitly warn
the numbers are mechanically derived and may drift; I did not rely on the
numbers alone — I located each hunk by its quoted text and confirmed the
surrounding heading named in the hunk file matched).

## Hunk 13 — §21.1, two edits

### The rule each edit adopts

**Edit A** (outcome-assignment sentence): every one of §21.5's ten rows
(R1–R10) has its outcome (ignore-record) assigned *expressly* — overriding
the normal scope-determines-outcome default of §2.4 — by one of exactly two
rules: `[R-CNT-25]`'s quarantine, or `[R-MTA-09]`. Before the repair only
`[R-CNT-25]` was named; the repair adds `[R-MTA-09]` (and fixes the
resulting subject-verb agreement, "does" → "do").

**Edit B** (Governing-rule-cell convention): a Governing rule cell's
parenthetical, after the primary (bracketed) requirement, may hold either
(a) further rule IDs the condition reads, cited without brackets, or (b) —
newly stated — the section defining a value set the condition reads, citing
two examples, L26 and L31.

### Check-by-check

**1. Tense/quantifier.** Edit A's quantifier is "every §21.5 row" — I
enumerated all ten rows (R1–R10) below under Check 5; the quantifier is
exercised in full, not restated loosely. Edit B's quantifier is "any
identifiers following [the primary rule] in parentheses" — ranging over
every Governing-rule cell in the register; I checked this against all 120
cells (Check 6). Both quantifiers are the actual normative extent, not a
subset dressed as the whole.

**2. Citations resolve.**

- `[R-CNT-25]` (line 2621–2623 in spec): "the outcome of every failure to
  read its **document** is ignore-record whatever the scope, because the
  document is **quarantined**." — Confirmed: this is a general "assigns the
  outcome, whatever scope" rule, matching Edit A's framing. PASS.
- `[R-MTA-09]` (line 2721, end of the frame-constraint paragraph): "Any
  violation here is ignore-record, never the tile-scope outcome §17.2
  assigns. `[R-MTA-09]`" — "here" = the immediately preceding paragraph's
  frame-constraint violations (R4's condition). Confirmed this is the
  express, scope-independent outcome assignment for R4. PASS.
- L26's citation `` `[R-CNT-18]` (§7.3 registry table) `` — opened §7.3
  (line 1075–1082): the registry table itself defines "0x0001 = layer,
  scope file." This is the original, sole defining location (confirmed by
  grep: every other mention of type 0x0001, lines 1197/1570/4484, cites
  back to §7.3 rather than redefining it). §7.3 is indeed "the section
  defining [the] value set" L26's condition reads. PASS.
- L31's citation `` `[R-CNT-23]` (§15.1) `` — opened §15.1 (line
  2175–2200). §15.1's *only* statement about index_encoding is: "Under
  index_encoding 1 (the only encoding this format major version defines,
  **§7.4**), the tile-index region ... is, contiguously: ...". §15.1 does
  not itself state the value domain; it uses the value as a precondition
  and explicitly attributes the definition to §7.4. The actual defining
  location is §7.4's layer-record field table (line 1120): "index_encoding
  | u8 | 1 = raw-segmented; any other value — including 0, reserved
  2–0x7F, and the experimental range ≥ 0x80 (§10) — is a validity error at
  layer scope (§15)" — this sentence states exactly the three categories
  L31's Instances column enumerates ("index_encoding 0; reserved 2-0x7F;
  experimental >= 0x80"). **FAIL — this is my C-01 finding**: the section
  the repair's new clause names as "the section defining [L31's] value
  set" is §15.1, which is a restatement that itself credits §7.4; the
  section that actually defines the value set is §7.4. Contrast with L26,
  where the cited section genuinely is the defining location.

**3. Label check.** Both edits sit in plain running prose in §21.1, no ">"
prefix anywhere in the surrounding paragraph (verified lines 3618–3705 have
no blockquote marker). Not a Note/Example/Rationale block. Normative,
lands. PASS.

**4. Contradiction in the passage.** I read the whole of §21.1
(3618–3705). No sentence elsewhere in the passage restates the pre-repair
"quarantine alone" framing in a way that would now conflict with the added
`[R-MTA-09]`; no sentence asserts a different set of assigning rules for
§21.5. No contradiction found for Edit A. For Edit B: I scanned all 120
Governing-rule cells (below) — no cell contradicts the two-branch
description; the only tension is the wrong-section citation captured as
C-01, which is a citation-accuracy defect, not an internal contradiction of
the convention's own words.

**5. Exhaustive claims.** "for every §21.5 row" (Edit A) — checked against
all ten rows individually:

| Row | Governing cell (primary) | Where outcome is textually assigned | Covered by {R-CNT-25, R-MTA-09}? |
|---|---|---|---|
| R1 | `[R-CNT-25]` | "...is ignore-record (`[R-CNT-25]`)" (line ~2635) | yes, R-CNT-25 |
| R2 | `[R-CNT-20]` (R-CNT-25) | §8.2's outcome table (line 1245): "a user-metadata extent's CRC → ignore-record. `[R-CNT-20]`" | R-CNT-20 states it explicitly; R-CNT-25's general "every failure to read the document" clause (line 2621) also textually subsumes a CRC failure — I accept this as covered, but note it is the one row where the *express* per-structure assignment (R-CNT-20) is not one of the two named rules; R-CNT-25 covers it only via its general clause, not a row-specific citation the way it does for R1/R3/R5. Flagged as a considered-and-rejected candidate below (not filed as a defect — see rejected_candidates). |
| R3 | `[R-CNT-25]` | explicit, same clause as R1 | yes |
| R4 | `[R-MTA-09]` (R-COD-06, R-CNT-25) | explicit, line 2721 | yes, R-MTA-09 |
| R5 | `[R-CNT-25]` (R-MTA-04, R-ENC-11) | "a document violating any of them is unreadable — ignore-record, with the report `[R-CNT-25]` asks for" (line 2736) | yes |
| R6 | `[R-MTA-04]` (R-CNT-25, R-ENC-12) | same intro sentence (line 2736) covers the 4-bullet restrictions, of which R6 is one | yes |
| R7 | `[R-MTA-04]` (R-CNT-25) | same | yes |
| R8 | `[R-MTA-04]` (R-CNT-25) | same | yes |
| R9 | `[R-MTA-04]` (R-CNT-25) | same | yes |
| R10 | `[R-MTA-04]` (R-CNT-25, R-ENC-12) | same, plus R-ENC-12's own text (line 562): "...except for a key inside a user-metadata document, where `[R-CNT-25]`'s quarantine governs and the outcome is ignore-record" | yes |

Conclusion: "every §21.5 row" is true after the repair (it was false before,
for R4, which is the defect this edit fixes). R2 is the one row I scrutinized
hardest; I did not file it as a defect (see rejected_candidates) because
R-CNT-25's own general clause is worded broadly enough ("every failure to
read its document") to textually reach a CRC failure, even though R2's table
cell names R-CNT-20 first.

Edit B's "(L26, L31)" — exhaustiveness of the *set of section-cited cells*:
confirmed by full-corpus grep (see Check 6) that L26 and L31 are the only
two of 120 cells with a section-only parenthetical. The *list* L26, L31 is
complete. What is wrong is not the list's membership but L31's own citation
target, per C-01.

**6. What else is left unconstrained (structure: the Governing-rule cell,
all 120 of them).** I extracted the Governing-rule column for all 120 rows
mechanically (script below) and confirmed every cell fits one of exactly two
shapes: `` `[R-XXX-NN]` `` alone, `` `[R-XXX-NN]` (R-YYY-MM[, R-ZZZ-KK...]) ``,
or (only L26, L31) `` `[R-XXX-NN]` (§N.N ...) ``. No third shape exists (no
cell mixes a section and a rule ID in the parenthetical, no cell has a
section as the *primary* citation). The amended convention, as a
*structural* description, covers all 120 cells with no sibling left
unconstrained. The defect is not a missing case in the convention's shape —
it is that one of the two worked examples (L31) points at the wrong
section, a citation-content error rather than a structural gap.

**7. Analogy check.** Neither edit argues by analogy ("exactly as", "the
same way", "transposed from", etc.) — Edit A lists two rules that *do*
something (an enumeration, not an analogy-as-warrant), and Edit B states a
structural convention. No analogy-warrant construction to check side by
side.

**8. Back-reference check (insertion).** Edit A inserts "and `[R-MTA-09]`"
and reflows "does" → "do" inside an em-dash-bounded aside that already sat,
pre-repair, between "each row is one malformed condition" and "the actor
obliged to detect **it**". I traced "it" in "the actor obliged to detect it"
forward from the insertion: nearest preceding singular nouns after the
insertion are "scope" and "row" (both inside the aside, both semantically
impossible antecedents for "detect"), so the reader must reach back past the
aside to "condition" regardless of whether the aside says "quarantine does"
or "quarantine and R-MTA-09 do" — the aside's *length* changed slightly but
its *boundary* (the two em dashes) did not move relative to "condition" and
"it", so the resolution is unchanged before and after. Not a new defect;
this ambiguity (if it is one at all) predates hunk 13 and is out of this
hunk's scope. Edit B's insertion ("or the section defining a value set it
reads (L26, L31)") sits at the end of a clause before a full stop; nothing
after it in the sentence contains a pronoun that could re-resolve.

### Scripts run for hunk 13's Check 5/6

```
cd spec
awk -F'|' '/^\| (F|L|T|R)[0-9]+ \|/ {n=NF; if($n ~ /^[ \t]*$/) n=n-1; gsub(/^ +| +$/,"",$n); print $2, "->", $n}' tarn.md | sed 's/^ *//'
```
→ 120 lines (all register rows), saved to gov_cells3.txt. `grep -E '§'`
on that file returns exactly two lines: `L26  -> `[R-CNT-18]` (§7.3
registry table)` and `L31  -> `[R-CNT-23]` (§15.1)`.

Control search proving the "only L26/L31" zero was not a broken search: the
same grep against a naive full-line extraction (before I fixed the FS
off-by-one) had returned an extra false hit `(§2.3)` that I traced to F6's
*Condition* column, not its Governing-rule column — this is exactly the
"run the control before trusting a zero" case the charter warns about; I
did not accept the corrected zero-elsewhere result until I had diagnosed and
fixed that miscount.

---

## Hunk 14 — R10's Governing rule cell

### The rule the repair adopts

R10 ("A user-metadata document key is longer than 255 bytes") now cites
`` `[R-MTA-04]` (R-CNT-25, R-ENC-12) ``, adding `R-CNT-25` to the existing
`R-ENC-12`.

### Check-by-check

**1. Tense/quantifier.** No quantifier changes; this is a citation-set
addition to one row.

**2. Citations resolve.**
- `[R-ENC-12]` (line 550–566, §4.6 "Names"): "Names ... satisfy three
  further constraints. ... a reader MUST treat such a name as a validity
  error at the owning scope — **except for a key inside a user-metadata
  document, where `[R-CNT-25]`'s quarantine governs and the outcome is
  ignore-record**. `[R-ENC-12]`" — this is a verbatim, explicit pairing of
  R-ENC-12 with R-CNT-25 for exactly the user-metadata-key case R10
  describes. PASS, and it is as strong a citation match as this document
  offers anywhere.
- `[R-MTA-04]` (line 2770, closing the four-restriction list) — the fourth
  bullet's "every key satisfying §4.6's name rules — non-empty, at most
  255 bytes, free of U+0000 through U+001F" is exactly R10's condition
  (255-byte cap). PASS.

**3. Label check.** R10 is a table row inside §21.5's register table, not a
blockquote, not Note/Example/Rationale. Normative. PASS.

**4. Contradiction.** I held R10 against R6–R9 (the charter's instruction):

| Row | Cell |
|---|---|
| R6 | `[R-MTA-04]` (R-CNT-25, R-ENC-12) |
| R7 | `[R-MTA-04]` (R-CNT-25) |
| R8 | `[R-MTA-04]` (R-CNT-25) |
| R9 | `[R-MTA-04]` (R-CNT-25) |
| R10 (after) | `[R-MTA-04]` (R-CNT-25, R-ENC-12) |

R10 now matches R6 exactly (both are name-rule violations governed by
R-ENC-12, both quarantined by R-CNT-25). Before the repair R10 was the odd
one out (R-ENC-12 with no R-CNT-25, unlike R6's identical shape). No
contradiction; this is a straightforward consistency fix. PASS.

**5. Exhaustive claims.** None introduced.

**6. Siblings.** The "structure" is the Governing-rule cell for a
name-length/name-content register row. R6 (empty key / control code) and
R10 (over-length key) are the two "name rule" violations among R5–R10;
both now carry the identical (R-CNT-25, R-ENC-12) pair. No sibling left
unconstrained.

**7. Analogy.** None present.

**8. Back-reference.** This is a same-line cell substitution, not an
insertion between sentences; no back-reference to check.

### §21.8's 277-instance recount

Per the charter, I recomputed the Instances-column total mechanically, per
§21.1's own stated rule (an em-dash cell = 1 instance; otherwise, count of
semicolon-separated items), across all 120 rows:

```
awk -F'|' '/^\| (F|L|T|R)[0-9]+ \|/ {gsub(/^ +| +$/,"",$2); gsub(/^ +| +$/,"",$4); print $2"\t"$4}' tarn.md
```
→ 120 rows extracted (instances_raw3.tsv), summed with a small python
script:
```
ROWS: 120  TOTAL INSTANCES: 277
```
This matches §21.8's stated "120 conditions over 277 instances" exactly.
Hunk 14 only changed R10's *Governing-rule* cell, not its *Instances* cell
(still "top-level document; layer sub-record document" = 2, unchanged), so
the 277 total was never at risk from this edit — the recount is a clean
PASS, confirming no accidental drift.

---

## Hunk 15 — §21.6's closing paragraph

### The rule the repair adopts

Neither of the two "conforming files a reader nevertheless refuses" cases
is a register row, and the repair now gives a *distinct* reason for each:
the first (version_major naming an unimplemented major) is a file this
document declines to judge at all; the second (experimental-range MU=1
type) is a file the document does judge, and finds to carry no violation
("carries none").

### Check-by-check

**1. Tense/quantifier.** "the first"/"the second" — I traced both back to
their sole antecedents earlier in the *same* paragraph: "The first is
**version_major naming a major this reader does not implement**" and "The
second is an **experimental-range top-level record type carrying MU = 1**".
Nothing else in the paragraph or subsection introduces a competing "first"
or "second". Quantifier ("neither is a register row") ranges over exactly
these two named cases, matching the paragraph's own earlier "Two structural
cases are conforming files a reader nevertheless refuses."

**2. Citations resolve.**
- `[R-CNF-13]` (lines 145–162, §2.3): "a file declaring another major is
  **neither conforming nor nonconforming under it save as to the
  conditions that reach it**: a reader refuses such a file on capability
  grounds ..., and that refusal is not a finding about its bytes." This
  matches "the first is a file this document declines to judge" — the
  document does not resolve the general conformance question for that
  file (it resolves only the narrow set of "reaching conditions" F1/F6/
  F8/F14, which is a separate, already-established exception and does not
  contradict "declines to judge" as a description of the *general*
  disposition). PASS, with the caveat noted above that "declines to
  judge" is a summary of the *general* case, not a claim that literally
  nothing about the file is ever checked.
- `[R-CNF-02]` (lines 145–178, and again at 3934): "a file is never
  nonconforming by virtue of [a conduct rule] ... `[R-CNF-02]` makes the
  file conforming all the same." This matches "the second carries none
  [violation]" directly — the file IS judged, and is conforming. PASS.

**3. Label check.** Plain prose in §21.6 (lines 3889–3945), no blockquote
marker anywhere in this paragraph. Normative. PASS.

**4. Contradiction.** I re-read the full paragraph start to finish (Two
structural cases ... through ... F35, F36, L24, L25). "In both the outcome
records a reader's capability, not a defect in the bytes" (unedited,
precedes the hunk) is consistent with both readings post-edit: case 1 is
capability-grounds refusal per R-CNF-13's own words; case 2 is also
capability/conduct-grounds per R-CNF-02. No contradiction. The closing
sentence ("What is registered in each case is the neighbouring condition
that *is* a violation — version_major = 0 ... F18 ...; and a reserved-range
type ... F35, F36, L24, L25") pairs one neighbouring violation with each of
"the first" and "the second" respectively, in the same order, and is
untouched by the diff except for incidental line-rewrap — consistent.

**5. Exhaustive claims.** "Neither is a register row" — verified against
the full register: version_major-unimplemented is not itself any F/L/T/R
row (its *neighbour*, F18, is, for major=0 specifically, a different
condition); experimental-range MU=1 top-level type is explicitly listed in
§21.6's own table above this paragraph ("A user-metadata record declares an
experimental-range... " — no, that's the metadata-encoding case, a
different row; the *type*-level experimental-MU=1 case doesn't appear
anywhere in §21.2–§21.5's F/L/T/R tables — confirmed by grep for
"MU = 1" and "experimental" co-occurring only in this closing paragraph and
in §7.2/§10, never as a numbered F/L/T/R row). PASS — "Neither is a
register row" holds.

**6. Siblings.** Structure: "conforming files a reader nevertheless
refuses." The paragraph asserts exactly "Two structural cases" (a closed
count, not itself part of this hunk's diff). I looked for a third such
case (grep for "reject the file"/"rejects the file"/"reader refuses" across
the whole document — 40 hits, listed in sweeps_run) and found none that is
(a) a conforming file and (b) refused on grounds other than the two named
here — the nearby "unknown record type at file scope: MU=1 → reject-file"
passage (line 1064) is the *same* experimental/reserved distinction already
covered by "the second", not a third case; F19's incompat-bit reject-file
is itself a register row (a violation, not a "conforming file refused"
case), and is unrelated. No unconstrained sibling found; "Two" continues to
hold as exhaustive. (This exhaustiveness claim predates the hunk and was
not itself edited — I checked it anyway per Check 6's instruction to look
at what the repair's *structure* leaves open.)

**7. Analogy.** No analogy-warrant language ("exactly as", "the same way")
in the edited sentence.

**8. Back-reference (insertion).** This is the hunk most directly shaped
like Check 8's target: it replaces "and a file this document declines to
judge is not one" with a longer clause naming "the first" and "the second"
separately, inside the sentence that begins "Neither is a register row:".
I read forward from the insertion to the paragraph's end and listed every
back-reference:
  - "the first" / "the second" (in the new clause) → resolve to the two
    bolded case-definitions two sentences earlier in the *same* paragraph.
    Same resolution before and after the repair (before the repair, the
    old single clause "a file this document declines to judge" collapsed
    both cases into one, incorrectly implying case 2 is *also* undecided —
    see below).
  - "each case" (next sentence, unedited: "What is registered in each case
    is...") → before the repair, "each case" had nothing distinct to point
    at within the *removed* clause (which said only "is not one", singular,
    about a merged case); after the repair, "each case" cleanly resolves to
    "the first" and "the second" just introduced. This is actually an
    *improvement* in resolution, not a break: the repair gives "each case"
    a real antecedent pair it previously had to reach past the collapsed
    clause for.
  - "the two" (earlier, unedited: "the diagnostic ought to distinguish the
    two") → resolves to the same first/second pair; unaffected, still
    correct, since the pair itself was already established two sentences
    before the diagnostic sentence.
No new mis-resolution found. If anything this repair *repairs* a mild
pre-existing anaphora flaw (the old text made two different things — "in
both, the outcome records a reader's capability" and "the file this
document declines to judge" — sound like they described the same single
disposition for both cases, when case 2 is in fact affirmatively judged
conforming, not undecided).

### Rejected candidate: "carries none" — ellipsis

I considered flagging "the second carries none" as a NEW_AMBIGUITY (no
explicit object for "none"). On rereading, the sentence's own list
structure — "the register enumerates file-conformance **violations**
(§21.1), the first is a file this document declines to judge, and the
second carries none" — supplies "violations" as the implied object via
ordinary list-final ellipsis, and the very next sentence ("What is
registered in each case is the neighbouring condition that *is* a
violation") confirms the reading. I closed this candidate as not a defect.

---

## Hunk 16 — Appendix F, [RFC 1950] and [RFC 1952]

### The rule the repair adopts

Two normative references, RFC 1950 (zlib) and RFC 1952 (gzip), are added to
Appendix F, each glossed "the wrapper codec 2 excludes (§17.2, T15)".

### Check-by-check

**1. Tense/quantifier.** No tense/quantifier issue — these are static
bibliography entries.

**2. Citations resolve.**
- `[R-COD-05]` (line 2445–2447, §17.2 "Codec 2 — deflate"): "The stored
  bytes are exactly one DEFLATE compressed data stream as defined by RFC
  1951 — raw, **not a zlib (RFC 1950) or gzip (RFC 1952) wrapper**."
  Confirms both RFC 1950 and RFC 1952 are cited normatively in body text,
  by exactly the "excludes" framing the new appendix entries use. PASS.
- T15 (line 3842, §21.4): condition "Codec 2 (deflate) and the stored
  bytes carry a wrapper rather than a raw RFC 1951 DEFLATE stream", with
  Instances "zlib RFC 1950 (CMF/FLG header + trailing Adler-32); gzip RFC
  1952 member (1F 8B, trailing CRC32+ISIZE)" — both RFCs named explicitly
  as the two instances of this row. PASS.
- §17.2 is confirmed as R-COD-05's home section (heading at line 2426,
  R-COD-05 at line 2447, both inside it). PASS.

**3. Label check.** Appendix F's own heading is "Appendix F — Normative
references" (no "(non-normative)" qualifier), in explicit contrast to
Appendix G's heading, "Appendix G — Reproducible-writer profile
(non-normative)", a few lines below. Per [R-CNF-01]'s "appendices
identified as non-normative" carve-out, F is normative (not so
identified) and G is not. The insertion lands in normative text.

**4. Contradiction.** None found — the two new entries are additive
bullets in a flat list; nothing elsewhere in Appendix F or in the body
disputes RFC 1950/1952's role.

**5. Exhaustive claims / completeness.** I swept the whole document for
every bracket-cited external-reference token and every bare "RFC NNNN"
occurrence (scripts below) and cross-checked against Appendix F's now-11
entries. Result: every external standard cited anywhere in the document
(BCP 14, IEEE 754, LZ4 Block, RFC 1950, RFC 1951, RFC 1952, RFC 2119, RFC
3339, RFC 3720, RFC 8174, RFC 8259, RFC 8878, Unicode) is present in
Appendix F after the repair (RFC 2119/8174 subsumed under the existing
[BCP 14] entry). Before the repair, RFC 1950 and RFC 1952 were the two
gaps. Confirms the charter's "check ... whether any other document cited
in normative text is still absent" — **none is absent now**. PASS, and
this specific check closes clean.

**6. Siblings / structure.** The structure is Appendix F's list of
reference entries. Each entry's established shape (checked across all 11,
pre- and post-repair) is `` - **[TAG]** Title — usage-gloss (§section[,
§section]). `` I checked whether the two new entries deviate: they add a
*register-row label* ("T15") inside the section-citation parenthetical —
`(§17.2, T15)` — which no other entry in Appendix F does (every other
entry's parenthetical holds only §-numbers). This is a minor form
deviation from this specific list's own established pattern (though bare
row-label citations, e.g. "(F35, F36, L24, L25)", are commonplace
elsewhere in the document's *body* prose, just not previously inside
Appendix F). I did not file this as a defect — it does not misstate a
fact and T15 is unambiguously locatable — but I record it as a considered,
rejected candidate (see rejected_candidates) since the charter specifically
asked me to check "the appendix's other entries' form."

**7. Analogy.** No analogy-warrant language in either new entry.

**8. Back-reference.** Pure insertion of two flat bullets with no pronouns;
nothing before or after re-resolves.

**9. Bibliographic accuracy (spot check, not one of the 8 checks but
worth recording).** "ZLIB Compressed Data Format Specification version
3.3" and "GZIP file format specification version 4.3" are RFC 1950's and
RFC 1952's actual titles, matching the citation style (title, then dash,
then usage) used by every neighboring entry (e.g. "[RFC 1951] DEFLATE
Compressed Data Format Specification version 1.3"). No mismatch found.

### Sweeps for hunk 16

```
grep -oE '\[[A-Za-z][A-Za-z0-9 .,'"'"'/-]*\]' tarn.md | sort -u | grep -vE '^\[R-[A-Z]+-[0-9]+\]$'
```
→ BCP 14, IEEE 754, LICENSE-SPEC, LZ4 Block, PLAN.md, RFC 1950, RFC 1951,
RFC 1952, RFC 2119, RFC 3339, RFC 3720, RFC 8174, RFC 8259, RFC 8878,
Unicode, docs/decisions/ — of these, LICENSE-SPEC/PLAN.md/docs/decisions/
are markdown links inside §1 (non-normative, [R-CNF-01]), not standards
citations; the remaining 13 tokens fold to Appendix F's 11 entries (RFC
2119 and RFC 8174 both live under [BCP 14]). Control: I confirmed §1's
non-normative status directly from [R-CNF-01]'s own text (line ~... "All
text in this document is normative except: §1 (Introduction)...") rather
than assuming it.

```
grep -noE 'RFC [0-9]+' tarn.md | sort -t: -k2 -u | awk -F: '{print $2}' | sort -u
```
→ RFC 1950, RFC 1951, RFC 1952, RFC 2119, RFC 3339, RFC 3720, RFC 8174,
RFC 8259, RFC 8878 — exactly nine, all present in Appendix F. Control for
this zero-gap conclusion: I did not simply trust the count; I individually
matched each RFC number against an Appendix F line before concluding
completeness (shown in the entry list above).

---

## Summary of findings

- **C-01** (hunk 13, Edit B): the newly-added claim "the section defining
  a value set it reads (L26, L31)" is wrong for L31 — §15.1 (the section
  actually cited in L31's Governing-rule cell) does not itself define
  index_encoding's value set; it merely uses the value as a precondition
  and explicitly credits §7.4 ("the only encoding this format major
  version defines, §7.4") as the defining section. §7.4's field table
  (line 1120) is where the value domain (1 = raw-segmented; 0, 2–0x7F
  reserved, ≥0x80 experimental) is actually stated, in the same three
  categories L31's own Instances column enumerates. Not byte-level: this
  is a citation/explanatory error about which section is authoritative,
  and does not change the value domain itself or which bytes a conforming
  implementation may emit or must reject (that is still governed by
  R-CNT-23, cited correctly and unaffected).

No other check across any of the four hunks produced a finding I am willing
to stand behind as a defect. Two candidates were opened and closed without
filing (R2's outcome-assignment attribution in hunk 13, and the "(§17.2,
T15)" row-label form deviation in hunk 16) — both are recorded above and in
rejected_candidates with the reasoning that closed each.
