# Cross-hunk consistency audit — round 34 (lane: cross-hunk auditor #1)

## Disclosure

Read: spec/tarn.md (via grep/sed, targeted sections — §2.3, §5.1, §5.2, §9.2,
§9.7, §11.1, §15.3, §16.1, §16.2, §18.2, §19.1, §20.3, §20.5, §21.1, §21.5,
§21.6, §21.7, Appendix F, Appendix H) and all 17 hunk-NN.diff files in
r34-audit/case/. Ran only grep/sed against spec/tarn.md; wrote no scratch
files beyond this transcript (no CRC/count computation was needed for this
audit's checks). Did not read full.diff, other lanes' hunk files, or any
docs/ material.

No contamination observed: nothing in the system prompt or tool preamble
supplied findings, verdicts, or hints about this round's defect beyond the
charter text itself, which I treated as the assignment, not as evidence.

## Grouping (by rule touched, not by section)

1. **The fifth member and its restatements** — the closed list's "declared,
   changed, re-established or cleared" verb-set for a slab/alignment
   declaration: hunk-09 (§20.3 step 4 top, source), hunk-11 (§20.3 step 4
   closing paragraph), hunk-06 (§11.1 Rationale), hunk-17 (Appendix H,
   non-normative checklist).
2. **The bar's category sentence vs. R-CNF-02 and §21.7** — hunk-10 (§20.3,
   the "position of every planar channel" bar) and hunk-01 (§2.3's R-CNF-02
   enumeration, widened to 3 cases this round).
3. **Slack disposal / slack inventory** — hunk-04 (§5.2), hunk-05 (§9.7),
   both citing §15.3; hunk-12 (§20.5's slack-accumulation sentence, Example
   block) against hunk-11's "Extents this commit supersedes become slack"
   and hunk-03's §5.1 anatomy list.
4. **Register conventions** — hunk-13 (§21.1's two amended conventions) and
   hunk-14 (§21.5 R10's Governing rule cell, an instance of one of those
   conventions).
5. **Reader's open path** — hunk-08 (§19.1 step 1, F<128 check).
6. **Independent, single-site edits** — hunk-02 (§4.7 taxonomy, packed
   payload table columns), hunk-07 (§18.2, SHOULD-report rationale),
   hunk-15 (§21.6, splitting "first"/"second" for the two structural cases),
   hunk-16 (Appendix F, RFC 1950/1952 additions).

## Group 1 — the fourth verb, word for word

Quoted exactly as they land:

- hunk-09 (source, §20.3 step 4 top): "a slab or alignment declaration MAY
  be declared, changed, re-established or cleared as this step provides
  below."
- hunk-11 (§20.3 step 4, later in the same step, the "below" the source
  sentence points to): "a slab declaration is declared, changed,
  re-established or cleared (`[R-SLB-04]`), and an aligned layer's stored
  tiles — every one the new state keeps, not only those this commit adds —
  satisfy its invariant or the declaration is cleared (`[R-SLB-01]`,
  `[R-CNF-05]`)."
- hunk-06 (§11.1 Rationale — labeled Rationale, so non-normative per
  R-CNF-01, and it says so of itself: "§20.3 states normatively, and
  governs, what a commit may do..."): "a slab or alignment declaration may
  be declared, changed, re-established or cleared".
- hunk-17 (Appendix H — labeled non-normative in its own heading, and its
  preamble disclaims authority: "each entry's authority is the requirement
  or section cited, never this summary"): "a slab or alignment declaration
  declared, changed, re-established or cleared".

All four use the same four verbs in the same order. Both non-normative
restatements (§11.1, Appendix H) explicitly point back to §20.3 as the
authority rather than asserting independent force, so R-CNF-01's label test
is satisfied and there's no orphaned normative claim sitting in a labeled
block.

Checked whether the "below" clause (hunk-11) actually **provides** the
"changed" transition for both slab and alignment, since the source sentence
promises "as this step provides below" for both nouns jointly:

- For slab: explicit, same four verbs, citing `[R-SLB-04]`. Read
  `[R-SLB-04]` (§16.2): "A writer or updater whose commit changes the
  stored-tile set, the run partition, the byte placement of any run, the
  disk ordinal of any tile the new state stores, **or the slab declaration
  itself**, of a layer slab-declared in either the superseded or the new
  generation, MUST either re-establish the invariants for every such run —
  or clear the declaration". This already covered a value-change of S/A_slab
  before this round (the "or the slab declaration itself" clause is
  untouched by any hunk), so the new "changed" verb at the top of §20.3 is
  simply naming a transition `[R-SLB-04]` already obliged. Consistent.
- For alignment: the "below" clause never uses the word "changed" (or
  "declared" or "re-established") for alignment at all — it states a
  conditional ("stored tiles satisfy its invariant or the declaration is
  cleared") that implicitly covers all three "declaration ends up set"
  cases without naming them. I checked `[R-SLB-01]` (§16.1) for an explicit
  transition rule analogous to `[R-SLB-04]`'s "commit changes ... the ...
  declaration itself" clause, and found none — §16.1 states only the
  invariant and who checks it, with no per-generation transition language.
  The §20.3 sentence is therefore doing double duty as both the citation
  and the only place this transition is stated for alignment. I did not
  find a contradiction here (the conditional does cover "changed" as one
  of the ways a layer ends up "aligned"), so I'm not filing this as a
  defect — flagging it in rejected_candidates since it's a plausible
  candidate I checked hard and could not stand up.

## Group 2 — the bar's category sentence (hunk-10) vs. R-CNF-02 (hunk-01)
## and §21.7 — CONFIRMED finding X-01

hunk-10 inserts, at the end of the "fixed declarations" MUST NOT bar in
§20.3 step 4:

> "This bar binds the commit as an actor: the file a violating commit would
> produce is conforming, the violation is not a file-conformance violation
> (`[R-CNF-02]`), and no register row records it (§21.7)."

I checked the `[R-CNF-02]` citation: it resolves correctly. §2.3's R-CNF-02
bullet (as amended by hunk-01, in the same commit) states the general
principle: "A writer obligation whose violation this specification
expressly declares not to be a file-conformance violation binds the actor
in the same way [as a conduct rule]" and gives three worked examples ending
"...and each is declared where it arises rather than enumerated here" — an
explicit disclaimer that R-CNF-02's own list isn't exhaustive, so hunk-10's
new fourth case not appearing in R-CNF-02's list is fine by R-CNF-02's own
terms.

The `(§21.7)` citation does **not** resolve. §21.7 ("What no check
detects") states exactly one test, twice framed as *the* test: "That is the
whole of the test, and it decides any condition put to it without appeal to
a list." The test is witnessed/unwitnessed — i.e., is a genuine
file-conformance violation *detectable*. §21.7 never once discusses
conduct rules or violations excluded from the register because they are
**not file-conformance violations in the first place**; its whole subject
is conditions that *are* violations but may or may not be checkable
("Distinguish an unwitnessed condition from a requirement that states no
condition a file can exhibit" — both of §21.7's two categories still
presuppose a would-be file-conformance violation).

The document already has the right citation, used for the exact parallel
case, immediately upstream of this round's changes (§21.6, untouched by any
hunk except hunk-15's local wording): describing the experimental-range
MU=1 top-level-record case — also "the prohibition ... binds a writer's
conduct and not the bytes" — it says: "**Neither is a register row: the
register enumerates file-conformance violations (§21.1)**, the first is a
file this document declines to judge, and the second carries none." That
passage cites **§21.1** (the register's domain statement: "enumerates
every detectable file-conformance violation this specification names"),
not §21.7, for exactly the reasoning hunk-10 needs.

So hunk-10's "(§21.7)" points at a real section that says something
related but not what the sentence claims — the "citation that points at a
rule which almost says the claimed thing" failure mode the charter warns is
the most expensive kind here. The repair should cite §21.1 (the register's
declared domain), not §21.7 (detectability of things already inside that
domain). Byte-level: no — this is a cross-reference/exposition defect; it
does not change what bytes a conforming implementation may emit or must
accept/reject, since the substantive claim (no register row for this bar)
is true either way and rests on `[R-CNF-02]` regardless of which section
number backs it.

## Group 4 — §21.1's two amended conventions (hunk-13) — CONFIRMED finding X-02

hunk-13 changes the "except" clause of §21.1's opening paragraph from

> "...except where a rule assigns one expressly, as `[R-CNT-25]`'s
> quarantine ... are the cases this text states..."

to

> "...except where a rule assigns one expressly, as `[R-CNT-25]`'s
> quarantine **and `[R-MTA-09]`** do for every §21.5 row, whatever the
> containing scope..."

I checked this against every §21.5 row (R1–R10) and against `[R-MTA-09]`'s
own text (§18.2, the block ending "Any violation here is ignore-record,
never the tile-scope outcome §17.2 assigns. `[R-MTA-09]`").

- `[R-CNT-25]` does hold for every §21.5 row: §21.5's own intro states
  "User metadata is quarantined (`[R-CNT-25]`): every way its document can
  be unreadable takes this outcome, whatever the containing scope — as a
  violation in the rows below" — an express, row-spanning claim, matching
  "whatever the containing scope" verbatim.
- `[R-MTA-09]` does **not** hold for every §21.5 row. Its "Any violation
  here is ignore-record" sentence is scoped to *its own* subject — the
  frame constraints of an encoding-2 document (window size, content-size
  field) — which is exactly R4's condition (R4's Governing rule cell is
  `[R-MTA-09]` (R-COD-06, R-CNT-25)) and nothing else. `[R-MTA-09]` says
  nothing about R1, R2, R3, R5–R10 (whose outcomes are governed by
  `[R-CNT-25]`/`[R-MTA-04]`, unrelated to `[R-MTA-09]`'s subject matter).
  `[R-MTA-09]`'s only other appearance is the §21.6 resource-decline case,
  which is not a §21.5 row at all (it's the neighbouring
  "conditions that are not violations" table).

So "as ... `[R-MTA-09]` do for every §21.5 row" is an overclaim: true of
`[R-CNT-25]`, false of `[R-MTA-09]` (true only of one row, R4). This is
exactly the shape check 5 asks for — a completeness word ("every") attached
to two rules conjunctively where it only holds for one. The fix is either
to drop `[R-MTA-09]` from this joint clause and let it be picked up
implicitly by "the requirement that defines it" per-row, or to rephrase as
two separate clauses ("...as `[R-CNT-25]`'s quarantine does for every
§21.5 row, and `[R-MTA-09]` does for R4..."). Not byte-level — an
exposition-scope error about which rule the convention-statement credits,
not a behavioral rule.

The register's *second* amended convention in the same hunk-13 — "or the
section defining a value set it reads (L26, L31)" — I checked against
every row's Governing rule cell across §21.2–§21.5 by grepping every
`(§...)` parenthetical inside a Governing-rule cell (not inside a Condition
column, which also uses "§" incidentally, e.g. F6). Only L26
(`[R-CNT-18]` (§7.3 registry table)) and L31 (`[R-CNT-23]` (§15.1)) fit the
pattern; the naming "(L26, L31)" is exhaustive and correct. No defect in
this half of the hunk.

Cross-checked hunk-14 (R10's Governing cell gains "R-CNT-25" in its
parenthetical) against this same §21.1 convention machinery: R10 was the
one §21.5 row whose parenthetical had *not* cited `[R-CNT-25]`, unlike its
siblings R2, R5–R9 (each cites `[R-CNT-25]` either as governing rule or in
parens) and R1/R3/R4 (which cite it as the governing identifier itself or
via `[R-MTA-09]`). After the fix, all ten rows are consistent with the
"every §21.5 row" claim about `[R-CNT-25]` specifically. This hunk itself
is sound; it's hunk-13's `[R-MTA-09]` addition next to it that overreaches.

## Group 3 — slack disposal and inventory

hunk-04 (§5.2) and hunk-05 (§9.7) both land the identical phrase "the bytes
it nominally addresses fall to slack where no other claimant claims them",
citing §15.3 (hunk-04 also cites §9.7, appropriately, since hunk-04's own
site is §5.2 and hunk-05's site *is* §9.7). Checked against §15.3's own
text (`[R-IDX-03]`, unmodified by any hunk): "any bytes it nominally
addressed that no other claimant claims fall to slack." Same claim, same
quantifier ("no other claimant"), consistent tense treatment (§15.3 uses
"addressed" for the classification rule in the abstract; §5.2/§9.7 use
"addresses" describing the live walk) — no defect.

hunk-12 (§20.5, inside the labeled "**Example** — what compaction
reclaims." block — confirmed non-normative by checking every line in the
enclosing range carries the ">" blockquote prefix) adds a third term to the
slack-accumulation sentence:

> "Slack accumulates a directory, a pad and a trailer per commit, plus a
> whole index region for each layer whose stored-tile set or index content
> a commit changed, plus **every payload and record extent a commit
> supersedes, which is the largest term** (§20.3)..."

Checked "record extent" against §5.2's formal definition: "a **structure**
— a stored-tile extent, **a record extent** (the bytes any record's extent
slot references, whatever the record's type, §7.2), the directory, or the
trailer." A layer record's extent slot addresses its tile-index region
(§7.4, confirmed at line 1102: "A layer record's extent slot addresses the
layer's tile-index region"). So, read against §5.2's own definition, "record
extent" formally *includes* a layer's tile-index region — which the same
sentence, two clauses earlier, already counts separately as "a whole index
region for each layer whose ... index content a commit changed." That's a
literal overlap between two terms of what reads as an additive inventory.

I checked whether this is resolved by the document's own habitual idiom:
the untouched §5.1 anatomy sentence (only its neighboring wording is
touched by hunk-03) lists "stored-tile payloads, tile-index regions, record
extents (§5.2)" as three parallel, sibling terms — i.e., elsewhere in this
document "record extent," when placed beside "tile-index region," is used
to mean the *other* record-extent content (non-layer documents), not the
formal §5.2 superset. Under that reading hunk-12's "payload and record
extent" is non-overlapping with its own "index region" clause (payload =
stored-tile extent, record extent = non-index record documents, e.g. a
superseded user-metadata document). Both readings are available from the
text as written, and the sentence gives the reader no local signal for
which one is meant here — unlike §5.1, hunk-12's clause doesn't say "record
extent" alongside "tile-index region" in the same breath, it says it right
after a separate clause about index regions, so the sibling-idiom reading
requires the reader to reach back across a "plus" boundary. This is a
genuine ambiguity, not a confirmed contradiction (since one reading is
consistent), so I'm filing it at PLAUSIBLE confidence, and noting it as
non-normative (Example block, so not byte-level under any reading — this
doesn't move what bytes a writer may emit or a reader must accept, only
whether the illustrative slack-inventory explanation double-counts what it
tells an operator).

## Group 5 — reader's open path (hunk-08)

Checked `[R-CNT-27]` and F5 against the inserted clause "an F below 128 is
a validity error at file scope before any byte is fetched
(`[R-CNT-27]`, F5)": `[R-CNT-27]`'s text ("No conforming file is shorter
than 128 bytes ... A reader MUST treat a shorter file as a validity error
at file scope") and F5's row ("File size is below the 128-byte minimum...
| reader | open | `[R-CNT-27]` (R-CNT-01, R-CNT-06)") both resolve exactly
as claimed.

Considered, and rejected, a possible contradiction with the very next
sentence: "a remote reader's suffix range for step 2 carries F in its own
response, so steps 1 and 2 cost one request between them" — which seems in
tension with "before any byte is fetched" if a single combined request
already carries trailer bytes by the time F is known. I judged this
resolved by "These steps are ordered by dependency, not by I/O," which
explicitly anticipates and licenses the combined-request case as a
dependency ordering rather than a strict I/O ordering, and by HTTP
semantics (headers, which is where Content-Range/F would appear, arrive
before the body). Filing as a rejected candidate, not a finding.

## Group 6 — single-site edits

- hunk-02 (§4.7): adds "size" to the columns a packed payload's table
  omits, and supplies the reason ("a field's size following from its
  type"). Checked this doesn't collide with §6.1's or §7.2's per-field
  size statements — consistent, no defect found.
- hunk-07 (§18.2): adds a rationale clause to an existing SHOULD. No
  citation, no quantifier, no exhaustive claim — checked for contradiction
  with the surrounding paragraph (the *cannot establish* / MUST NOT
  certify language) and found none.
- hunk-15 (§21.6): splits an ambiguous "and a file this document declines
  to judge is not one" into "the first is ... declines to judge, and the
  second carries none," correctly mapping to the two structural cases
  (version_major mismatch; experimental MU=1 top-level record) stated two
  paragraphs earlier in the same passage. Checked against both cases'
  earlier wording — matches; strictly clarifies, doesn't change the claim.
- hunk-16 (Appendix F): adds RFC 1950 (zlib) and RFC 1952 (gzip) entries,
  "the wrapper codec 2 excludes (§17.2, T15)". Checked against T15's row
  text verbatim: "zlib RFC 1950 (CMF/FLG header + trailing Adler-32); gzip
  RFC 1952 member (1F 8B, trailing CRC32+ISIZE)" — exact match, both
  wrappers, no defect.

## Searches run (with hit counts) and their controls

- `grep -n "R-SLB-0[0-9]"` → 15 hits (used to locate §16.1/§16.2 and every
  citing site). Control: same search also surfaces R-SLB-04's own
  definition at line 2369, proving the search reaches defining prose, not
  only citations.
- `grep -n "R-CNF-02\b"` → 6 hits. Control: hit at line 178 is R-CNF-02's
  own defining bullet (proves the search finds definitions, not just uses).
- `grep -n "R-MTA-09"` → 7 hits, spanning its own definition (line 2721),
  its two citing sites in this round's hunks (3624, one is the finding),
  and its citation in §21.6/§21.7 elsewhere. Control: found at both a
  defining site and multiple citing sites, so the zero-risk case (a search
  that could not have matched the defining prose) doesn't apply here.
- `grep -n "record extent\|payload extent\|extent slot"` → 40 hits,
  including the formal §5.2 definition (line 702) and the §5.1 sibling
  listing (line 638) — both readings' textual basis confirmed present.
- `grep -n "^| L26 \|| L31 "` and a full-table sweep for `(§` inside
  Governing-rule cells (`grep "^| [A-Z][0-9]* |.*\`\[R-" | grep "(§"`) → 3
  hits total (F6, L26, L31); F6's is inside its Condition column, not its
  Governing-rule cell, ruled out by inspection, leaving exactly {L26, L31}
  as the pattern hunk-13 names. This is the control for hunk-13's second
  convention: had the search returned a fourth row, "(L26, L31)" would be
  an incomplete enumeration; it returned exactly the two named.
- Confirmed the hard-wrap risk directly: `grep -n "aligned layer's stored
  tiles"` (a phrase that spans a line break in the file) returns 0 on a
  naive single-line grep, so I re-verified with `sed -n` printing the raw
  paragraph and reading across the wrap by eye, rather than trusting a
  grep zero, per the brief's warning.

## Rejected candidates

1. Whether `[R-SLB-01]` needs its own explicit "changed" transition
   language parallel to `[R-SLB-04]`'s "or the slab declaration itself"
   clause — checked hard, concluded the §20.3 conditional ("stored tiles
   satisfy its invariant or the declaration is cleared") already covers
   the "changed" transition for alignment without needing to name it,
   because the invariant is stated over the *new* declared A regardless of
   how it got there. Not filed.
2. hunk-08's "before any byte is fetched" vs. the combined-request
   sentence immediately following — resolved by the "ordered by
   dependency, not by I/O" framing and HTTP header/body ordering. Not
   filed.

## Confidence / what an empty result would have meant

Not applicable — two CONFIRMED findings and one PLAUSIBLE survive. Where I
found nothing (groups 5 and 6, and half of group 4), I've stated what
checks I ran and their controls above rather than leaving a bare absence.
