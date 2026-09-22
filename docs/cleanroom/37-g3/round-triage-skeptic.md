# Cleanroom round 37 — triage pass: skeptic

## Access disclosure

Read: `/Users/robertkleffner/Documents/GitHub/tarn-first-draft/spec/tarn.md` in full for the
sections cited below (§2.1, §2.3, §5.1, §6.2, §6.3, §14.4, §20.1, §20.2 (partial),
§20.3, §20.4, §20.5), using `grep`/`sed`/Python to locate section headers and to do an
exact character-column analysis of the two ASCII diagrams under review (diagrams-01).

I did **not** open any walk transcript (`transcript-<role>.md` or a quiz transcript) — the
findings' own quotations plus the spec were sufficient to check every claim.

I ran one directory listing early on: `ls /private/tmp/.../r37-round/` (the round's parent
directory, one level above my own `out`/`triage-*` folders), to confirm my own output path
existed before writing to it. This showed only sibling directory *names*
(`out`, `scratch`, `triage-correctness`, `triage-implementer`, `triage-skeptic`) — it did not
list or open `out/`'s contents, so no other pass's transcript names or content were seen.
Disclosing it per the brief's instruction, out of caution, even though it is not a listing of
`out/` itself and happened after I had already read the brief.

I did not read `docs/`, `PLAN.md`, `AGENTS.md`, `conformance/`, `spec/registry.json`, git
history, or the web, per the brief's restriction (this overrides CLAUDE.md's pointer to
AGENTS.md for this task).

## diagrams-01 — commit-shape diagram brackets overrun by one column

Verified by exact column count (Python, treating each Unicode code point as one column,
consistent with monospace rendering):

- Diagram (a), line 3414: the `A: tiles+index` cell's content occupies columns 16–31
  (bounded by `│` at 15 and 32). The annotation bracket on line 3415 is `└`(16)…`┘`(32) —
  its closing `┘` lands on column 32, the divider that opens the *next* (▓) cell, one column
  past the cell's own last content column (31).
- The second bracket on line 3415 spans `└`(33)…`┘`(46): content of the ▓ cell is columns
  33–45; the closing bracket again lands on column 46, the divider opening the next
  (`B: tiles+index`) cell.
- Diagram (b), line 3432/3433: identical pattern — `└ old ─┘` spans 23→31 against a
  ▓-cell content of 24–30 (divider at 31 begins the next cell); `└───────┘` spans 31→45
  against content 32–44 (divider at 45 begins the next cell).
- By contrast, §5.1's diagram (lines 667–670) uses an explicit box (`┌┬┐└┴┘`) and its
  brackets land exactly on the box's own `┬`/`┴` column positions at *both* ends (e.g.
  `└tiles+index┘` at columns 10 and 22, matching the `┬`/`┴` at 10 and 22 exactly) — divider
  to divider, content-width + 2, with no overrun into an adjacent cell.

So the reporter's factual claim about the two diagrams is confirmed exactly: both examples in
§20.3 draw their brackets one column wider than their own cell's content, with the extra
column landing on the divider that begins the differently-labelled neighboring cell, and this
differs from §5.1's own convention.

**Byte-level test.** `[R-CNF-01]` (§2.1, line 105-107): "All text in this document is
normative except: §1 (Introduction); any text labeled *Note*, *Example*, or *Rationale*; and
appendices identified as non-normative." This entire figure sits inside a block headed
"**Example** — the three shapes a commit takes." The actual rule governing which bytes a
tile-index re-emission touches is stated in normative prose at §20.3 step 4 (`[R-WRT-04]`,
`[R-WRT-05]`), independent of how the illustration is drawn. Resolving the bracket's exact
column changes no byte a conforming writer emits or a conforming reader/verifier checks.

**Consensus: CONFIRMED** (the rendering slip is real, verified by direct column count).
**Severity: figure.** Not byte-level.
**Repair:** cosmetic — shorten each closing bracket by one column (or lengthen the opening
side to match) so the bracket's span equals its own cell's content width, matching §5.1's
convention; optional, since the block is non-normative.

## diagrams-02 — trailer table flags cell lists three actors

Verified line 838 (trailer table) reads: "carried forward unchanged by an updater, appender
or rewriter alike." Verified §20.1 (lines 208-214, `[R-CNF-06]`): "Conforming updater. A tool
that modifies an existing file... Its tiers, the appender and the rewriter, are §20.1's,"
and again at §20.1's own text (line 3148-3151): "The tiers are shapes of operation... An
appender and a rewriter are updaters." So "updater" is exhaustively the two named tiers, no
third kind exists anywhere in the document — the class is closed.

Verified the "correctly built" comparison the reporter cites: §6.3 line 911-913: "...so a bit
is set only by a writer under the later minor version that defines it and carried forward by
every updater under this text, appender and rewriter alike" — the idiomatic construction,
with "updater" as the class noun and "appender and rewriter alike" as the appositive, versus
line 838's flatter three-item list joined by commas/"or."

**Byte-level test.** `[R-CNT-08]` (§6.3, lines 907-915) states the substantive rule directly
and without qualification: "An updater MUST copy forward unknown ignore-lane bits of its
input file, MUST NOT clear them, and MUST NOT set any other." This binds every updater
(no third tier exists to be omitted or duplicated), so no verifier or reader behavior changes
under either reading of the table cell's prose. The cell is a restatement, not the rule.

**Consensus: CONFIRMED** (imprecise wording, not idiomatic, genuinely defensible as a
three-coordinate misread by a reader consulting only this table). **Severity: editorial.**
Not byte-level.
**Repair:** reword to match §6.3's own construction, e.g. "carried forward unchanged by every
updater under this text, appender and rewriter alike."

## adversary-01 — R-WRT-06's refusal duty lacks the express conduct-only disclaimer

Verified `[R-CNF-02]`'s full text (§2.3, lines 166-179). It has two tiers, not one:

1. A **general** sentence: "A few obligations this specification places on writers govern
   their *conduct* rather than their output — where a value is published, which registry
   version a writer targets (§10.3, §18.3), or the barriers a commit performs (§9.2) — and a
   file is never nonconforming by virtue of one: conduct rules bind the actor, the predicate
   binds the bytes." The three examples given ("where a value is published," etc.) are
   illustrative ("a few obligations"), not an exhaustive enumeration of the whole category.
2. A **named** sub-list of three cases "this specification expressly declares" not to be
   file-conformance violations (ignore-lane bits, pre-trailer gap, step 4's bar) — "each is
   declared where it arises rather than enumerated here."

I tested, rather than assumed, which tier R-WRT-06 (§20.5, line 3623-3626: "A rewriter MUST
refuse to rewrite a file carrying any record whose type it does not implement with MU = 1...")
falls into, by checking whether a *violation* of it leaves any distinguishable trace in output
bytes. The three named cases in tier 2 all leave a literal trace in the file (a set ignore-lane
bit, a longer pre-trailer gap, a changed fixed declaration) that could naively look like a
conformance question, which is presumably *why* they need an express carve-out. R-WRT-06's
violation leaves no such trace: if honored, no output exists to examine; if violated, the
reporter's own point stands — the resulting bytes are indistinguishable from what a
self-declared *creator* could legitimately emit under §20.2 (which imposes no equivalent
duty and explicitly allows "bytes it copied from another file," §20.1 line 3170). So R-WRT-06
matches tier 1's description exactly and needs no individual enumeration to be conduct-only;
the general sentence already covers it.

**Byte-level test.** The general sentence already quoted, plus §2.3's opening definition:
"Conforming TARN file... is a pure predicate on bytes: it does not depend on any reader,
writer, or environment" (line 156-158). Together these foreclose any reading under which an
actor-identity label (rewriter vs. creator) changes a verifier's verdict on fixed output
bytes — matching the reporter's own conclusion.

**Consensus: CONFIRMED** as a real, if narrow, textual asymmetry: R-WRT-06 is not named
alongside its three siblings even though it is the same kind of rule, so a reader checking
only the tier-2 list (rather than reading tier 1's general sentence) could wonder about its
status. **Severity: editorial.** Not byte-level — I looked for, and found, the sentence that
forecloses the fork (quoted above), and additionally confirmed the underlying premise
(bit-for-bit indistinguishability from a legitimate creator's output) rather than taking the
reporter's word for it.
**Repair:** optional — cross-reference `[R-WRT-06]` from `[R-CNF-02]`'s list, or add a short
parenthetical at §20.5's own site, for reader convenience; not required by the rule as
written.

## adversary-02 — layer-drop paragraph and an implemented MU=1 sub-record

Verified §20.4 in full (lines 3475-3532). The paragraph immediately before the table
(lines 3497-3501) explicitly scopes the table's own MU=1 row: "Its MU = 1 row reaches only a
type the updater does not implement... so for an implemented type only the PE bit bites."
This is stated *before* the table and *before* the layer-drop paragraph the finding quotes.

The layer-drop paragraph (lines 3509-3514) then says: "...a sub-record's flags govern it
within a layer the updater keeps, so a dropped layer's sub-records and their extents go with
it whatever their PE bits. One sub-record blocks the drop, a sub-record of a type the updater
does not implement with MU = 1... **(the table's first row)**." That parenthetical explicitly
ties the blocking condition back to "the table's first row" — i.e., to the row whose scope
was *just* restricted, two paragraphs earlier, to unimplemented types only. This is not a
silent gap the reader must independently notice; the text names its own referent.

I tested the specific boundary case the finding raises: an *implemented*, MU=1, PE=1
sub-record. Per line 3501, being implemented routes it to a PE-only lookup, i.e., the PE=1
row. The layer-drop paragraph's "go with it whatever their PE bits" clause explicitly voids
PE-based protection once the *whole layer* (not an individual record within a kept layer) is
dropped, and the sole named exception is the unimplemented-MU=1 case cross-referenced to row
1. So an implemented, critical sub-record disappearing along with its dropped layer is not an
oversight or a gap in the blocking sentence — it is the stated, cross-referenced consequence
of reading the section as a whole, and it is also the coherent design the reporter itself
describes (understanding licenses judging safety; not understanding forecloses it).

**Byte-level test.** No MU=1 record type is registered under format major 1 (§7.3, §10.2) —
both registered types are MU=0 — so this cannot presently be exercised by any real
conforming file, independent of the reading question. But more directly: the reading question
itself is closed by the text, as shown above, so there is no live fork to test bytes against
in the first place.

**Consensus: REFUTED.** The document decides it: the paragraph directly above the table
restricts the MU=1 row's scope to unimplemented types, and the layer-drop paragraph
explicitly cites "the table's first row" as its blocking condition — the two sentences read
together leave no room for the "MU=1 always blocks drop" misreading the finding worries a
reader might form. **Severity: none.** Not byte-level.
**Repair:** none required; optionally, the table's row *label* itself ("MU = 1") could carry
an inline "(unimplemented)" qualifier for a reader who reaches the table without the
preceding paragraph's context, but this is a convenience, not a correction of an error.

## adversary-03 — updater→{appender, rewriter} narrowing is exhaustive

Verified independently (see diagrams-02 above): §20.1 and §2.3's `[R-CNF-06]` both state the
updater class has exactly two tiers, appender and rewriter, with no third. The PE=0 row's
narrowing ("an appender MAY drop... and a rewriter MAY drop...") is therefore a complete
restatement of "an updater MAY drop," not an omission.

I also checked the phrasing asymmetry the reporter flags (the appender's license is qualified
"in any commit it is otherwise free to make," the rewriter's is bare "in any rewrite") against
§20.5's text: a rewrite carries far fewer independent per-operation constraints than a commit
(§20.3's step 4 fixed-declaration bar, its permitted-change list, and its numeric bounds have
no rewrite-side analogue of the same shape), so the qualifying clause has no rewrite-side
counterpart to state. This matches the reporter's own explanation.

**Byte-level test.** No fork: the narrowing exactly reconstitutes the closed two-tier class.

**Consensus: CONFIRMED** (the observation is accurate: no gap here). **Severity: none.**
Not byte-level, not a defect. **Repair:** none.

## adversary-04 — single-numeric-channel layout field, worked confirmation

Verified §14.4's Note (line 2146-2148): "A single-channel numeric layer produces
byte-identical tile images under either layout." Verified the quoted §20.3 step 4 passage
(lines 3457-3465, ending "...no check any actor owes able to see it (§21.7)") is present
verbatim and is normative body text of step 4 (not inside a Note/Example/Rationale block) —
but is itself declared conduct-only two paragraphs earlier at the same step: "This bar binds
the commit as an actor: no file is nonconforming by virtue of its violation... (§21.7,
`[R-ERR-01]`, `[R-CNF-02]`)" (lines 3277-3280 in the step-4 text), which matches `[R-CNF-02]`'s
own named list at §2.3 ("§20.3 step 4's bar on the fixed declarations of a layer that stores a
tile").

I did not redo the reporter's per-quantity arithmetic (disk ordinal, entry_count, decoded
size, per-value offset, filter stride at C=1) by hand, but the claimed conclusion is exactly
what §14.4's Note already asserts independently, in normative text, as a general statement
about single-channel numeric layers — the worked example is a specific instance of a general
rule the document already states elsewhere, not a novel claim resting only on the reporter's
own arithmetic.

**Byte-level test.** No fork: `[R-CNF-02]` already declares this whole bar conduct-only,
independent of whether the C=1 case is witnessed or not.

**Consensus: CONFIRMED** (accurate observation, corroborated by §14.4's Note independent of
the reporter's own derivation). **Severity: none.** Not byte-level, not a defect.
**Repair:** none.

## Coverage

All 6 input ids grouped 1:1 (no duplicates found across the two reporters' findings — each
finding is a genuinely distinct claim in a distinct location). `all_input_ids_seen` lists all
six; every group's `member_ids` is a singleton; the union is exactly the six ids with no
duplicates.

## Groups I tried hardest to overturn and could not

- **adversary-01**: tried to find a case where actor-identity (rewriter vs. creator) could
  make two conforming verifiers disagree on the same output bytes. Could not — the
  bit-for-bit indistinguishability check (rewriter-violation output vs. legitimate
  creator output) holds.
- **adversary-02**: tried to find a live reading under which an implemented, PE=1, MU=1
  sub-record is NOT swept away by a layer drop. Could not — "whatever their PE bits" is
  explicit and the only stated exception is cross-referenced to the unimplemented-MU=1 row.
- **diagrams-01**: tried to find a normative dependency on the diagram's own bracket
  placement (e.g., a cross-reference elsewhere in the spec that treats the figure as
  authoritative for the byte boundary). Found none; step 4's prose is self-contained.
