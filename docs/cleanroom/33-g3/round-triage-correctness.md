# Round 33 — triage pass: CORRECTNESS lens — working transcript

## What I read

- `/Users/robertkleffner/Documents/GitHub/tarn-first-draft/spec/tarn.md` — the whole
  file, lines 1–4805, in eight sequential `sed -n` reads. No section skipped.
- No walk transcript. No other triage pass's notes. No directory listing anywhere
  under `r33-round/out/`. I did not open `docs/`, `PLAN.md`, `AGENTS.md`,
  `conformance/`, `spec/registry.json`, git history, or the web.

## Mechanical checks run (all against spec/tarn.md)

```
grep -n "re-established"                        -> 4 hits: 1656, 3203, 3299, 4766
grep -c "RFC 1950"                              -> 2   (2442 = [R-COD-05]; 3825 = T15)
grep -c "RFC 1952"                              -> 2   (2442 = [R-COD-05]; 3825 = T15)
grep -c "RFC 1951"                              -> 5
grep -n "counted and named"                     -> 1 hit: 2798 ([R-MTA-10])
grep -n "report each record"                    -> 1 hit: 2794 ([R-MTA-10])
grep -in "size column"                          -> 0 hits
grep -n '(§[0-9]' | (register rows only)        -> L26 (3776), L31 (3781) only
grep -n 'slab or alignment'                     -> 1656, 3202, 4765 (three sites)
grep -n 'alignment' | grep -i 'chang|lower|raise|differ' -> 0 hits
grep -n 'declaration itself'                    -> 1 hit: 2358 ([R-SLB-04])
```

Column headers read off the tables directly:

- §6.1  `| Offset | Size | Value | Class |`
- §6.2  `| Offset | Size | Type | Field | Class | Valid values |`
- §7.2  `| Offset | Size | Type | Field | Class |`
- §7.4  `| Field | Type | Constraint |`
- §15.1 `| Offset | Size | Type | Field | Class | Valid values |`
- §18.2 `| Offset | Size | Type | Field | Class | Valid values |`

Register row counts: F 35 (F11 struck), L 49, T 26, R 10 = 120. Matches §21.8.

---

## Grouping

Only one merge: **verifier-01 + quiz-02**. Both report the same defect — §5.2's
and §9.7's restatements of where a structurally-rejected index entry's nominal
bytes go drop §15.3's "that no other claimant claims". Identical location,
identical quotation set, identical repair.

Everything else stands alone. Three near-merges I considered and rejected:

- **writer-02 vs adversary-03.** Both circle §20.3 step 4's uncategorized
  prohibition. But adversary-03's stated defect is that §2.1's *Note* asserts two
  phrasing invariants the body does not satisfy — a different location, a
  different repair (fix the Note or the four requirements), and a second limb
  ([R-MTA-09]'s bare SHOULD) that writer-02 never touches. Kept apart.
  Worth flagging for the reconciler: the two reporters reach **opposite**
  conclusions on whether a step-4-violating commit's output is a conforming
  file (writer-02: conforming; adversary-03: "nonconforming-but-invisible").
  I resolve that against adversary-03 below.
- **diagrams-04 vs register-04.** Both are Governing-rule-cell defects, but
  L26/L31 (section reference where §21.1 says identifier) and R10 (missing
  R-CNT-25) are two different cells with two different repairs. diagrams-04
  mentions the R6/R10 asymmetry in passing; that content is register-04's group.
- **writer-01 vs quiz-01 vs adversary-04.** All three are §20.3 step 4, but they
  are three different clauses: the slab/alignment member's reach, the
  "position of every planar channel but the last" clause, and the
  channel-replacement gloss. Distinct defects, distinct repairs.

---

## Finding-by-finding

### reader-01 — §19.1 omits the 128-byte floor before computing F − 64

Checked. §19.1 step 1 reads "Obtain the transport-authoritative file size F
(`[R-CNT-10]`)" and step 2 "Fetch bytes [F − 64, F)". No mention of 128 anywhere
in §19. The reporter's claim that §19.1 restates many §21-carried checks is
accurate — step 4 restates the MU gate, per-type multiplicity, extent-slot
validity, the user-metadata framing trio and duplicate layer names.

Decided by §19's own preamble, which the reporter quotes correctly:

> A row this section does not restate is due at its own tier all the same, with
> its governing rule's own outcome.

F5's Detected cell is *open*. So the floor is owed at the open whether or not
§19.1 restates it. Reading (b) is not needed and reading (a) is what the
document states. Real but editorial: the sequencing of §19.1's ordered steps
leaves step 2's range arithmetic momentarily undefined for F < 64.

CONFIRMED / editorial / not byte-level. The document decides it.

### reader-02 — §2.3's closed list omits §9.2's barriers

Quotations verified verbatim at §2.3 and §9.2. The barriers are not on §2.3's
two-item list. §9.2 routes itself to the *preceding* sentence's category:

> A writer that omits a barrier violates this requirement as an actor, and the
> file it produces is never nonconforming by virtue of it, as `[R-CNF-02]` says
> of every **conduct rule**.

and the preceding §2.3 sentence is where conduct rules live ("A few obligations
this specification places on writers govern their *conduct* rather than their
output"). So §9.2 self-classifies and the outcome is decided. What is genuinely
loose is that §2.3's second sentence states its class in terms
("expressly declares not to be a file-conformance violation") that the barriers
also satisfy, then closes it — "are the cases this text states" — and §9.2 says
it is "declared so here on the model `[R-CNF-02]` states", which is the second
sentence's convention, not the first's. A checklist built from §2.3 alone files
the barriers wrong.

CONFIRMED / editorial / not byte-level (the actor is bound and the file is
conforming under both).

### reader-03 — §18.2's "Valid values: 1 or 2; see below"

The reporter's supporting premise does not survive checking. The claim is that
"every comparable cell elsewhere spells that out — §7.4 … §6.2 … §15.1". Against
the tables:

- §15.1's `offset` and `length` rows read **"see §15.3"** — pure deferral, no
  value set stated at all.
- §6.2's `version_major` row reads **"1 (0 invalid; others: §6.3)"** — the
  assigned value plus a pointer, exactly §18.2's shape, and it likewise does not
  say in the cell that a foreign major may be a conforming file under its own
  major.
- §7.4 is not the same column: its header is `Constraint`, and §4.7 accounts for
  §7.4's table being shaped differently.

So the cell's "see below" is the document's own established practice, not a
departure from it, and the next sentence partitions the space correctly
("values ≥ 0x80 are the experimental range (§10)"). The claimed inconsistency
is not there.

REFUTED / none / not byte-level. The reporter misread the comparison cells.

### writer-01 — may an already-declared alignment or slab take a different value?

**This is the one I uphold as byte-level.**

Texts checked, all verbatim:

- Closed list: "keeps its declarations, with these exceptions and no other: …
  and a slab or alignment declaration MAY be declared, re-established or cleared
  as this step provides below."
- Fixed side: "Every other declaration is fixed … the layout, the linearization
  and the index encoding, the codec and the filter, the rank and the dimension
  order, every tile extent, every channel's type and fill, an interleaved layer's
  channel list (its names aside), and the position of every planar channel but
  the last. A commit MUST NOT change one of these". **A, S and A_slab are not on
  this list.**
- Below-clause: "a slab declaration is re-established or cleared (`[R-SLB-04]`),
  and an aligned layer's stored tiles — every one the new state keeps … satisfy
  its invariant or the declaration is cleared".
- [R-SLB-04] triggers include "or **the slab declaration itself**".
- The three-verb phrase occurs at exactly three sites (1656 §11.1 Rationale,
  3203 §20.3 step 4, 4766 Appendix H) plus the two-verb below-clause at 3299.
  The reporter's sweep is accurate.

**The sentence I looked for and did not find.** Anywhere in §20.3 step 4, §16.1,
§16.2, §11.1's Rationale or Appendix H, a statement that an alignment or slab
declaration already carried by a layer that stores a tile may (or may not) take a
*different nonzero value* in one commit — a "may be changed", a "raised or
lowered", or "a change of alignment" appearing among the rewrites in the
"gives up" list. `grep -n 'alignment' | grep -i 'chang|lower|raise|differ'`
returns **zero hits across the whole document**. "declaration itself" occurs once,
in [R-SLB-04]'s trigger list, and that trigger is satisfiable by declare/clear
alone, so it does not presuppose a value change as strongly as the reporter says.

**Where I correct the reporter.**

- The (R-b) consequence is overstated. Under (R-b) an updater is *not* driven to
  a whole-file rewrite: clear A in commit n (permitted: "cleared"), declare
  A = 512 in commit n+1 (permitted: "declared"). Two commits, every intermediate
  file conforming. The reporter's cache-invalidation and tile-duplication costs
  do not follow.
- The claim that S = 8 → S = 16 "has no in-place path at all under (R-b)" is
  **wrong** for the same reason: clear S (S = 0 forces A_slab = 0, [R-CNT-23]),
  then declare S = 16. The reporter's "sharper" case is not sharper.

**Why it is byte-level anyway.** The test is "which byte sequences a conforming
implementation may emit". Under (R-a) a conforming updater may append, to
generation n, a commit whose directory carries L with the alignment field holding
512; under (R-b) no conforming actor may produce that byte sequence at all — the
two-commit path produces a *different* file (a third generation, more slack).
The disputed file is itself conforming under both readings — [R-SLB-01]'s
invariant holds over every kept stored tile (every multiple of 4096 is a multiple
of 512), [R-CNT-16] is satisfied with S = 0, [R-CNT-23]'s 512 ≤ A ≤ 2⁶² holds —
so [R-CNF-05] does not bar it under both readings alike. One reading permits an
actor to emit it and the other does not.

**The premise my uphold rests on, stated so it can be attacked:** that
"declared, re-established or cleared" does not unambiguously reach a
nonzero → different-nonzero transition. The best argument the other way is that
the "gives up" list introduces itself as complete — "What the line gives up is
stated rather than carved around" — and does not name a change of alignment or
slab, so under (R-b) that list is incomplete on its own terms while under (R-a)
both lists are complete. That is a real argument and it is why a refuter should
be pointed at it. It is not decisive: the "gives up" sentence states a method,
not a closure, whereas the permitted list says "and no other" outright.

CONFIRMED / **byte-level** / repair below.

### writer-02 — step 4's MUST NOT binds an actor while leaving a conforming file

The categorisation gap is real: §20.3 step 4's prohibition is neither a §10.3/§18.3
conduct rule, nor one of [R-CNF-02]'s two expressly-declared cases, nor
[R-ENC-06]'s "no condition a file can exhibit" instance.

But the *outcome* the reporter leaves open is decided, and against adversary-03's
opposite answer. §2.3: "File conformance is a pure predicate on bytes: it does
not depend on any reader, writer, or environment." The only witness of a step-4
breach lies in the superseded generation, and §5.2 says of those bytes:

> Slack has no internal structure this specification defines, its content is
> unconstrained, and **no conformance requirement applies to it**.

reinforced by §9.6's "no verdict turns on the probe" and §9.7's live-state-only
walk. So the file a violating commit produces **is** conforming, the actor is
bound, and adversary-03's "nonconforming-but-invisible" reading is foreclosed.

What is left is only which of three defined categories the prohibition sits in —
four cross-references to settle and nothing turning on the answer.

CONFIRMED / editorial / not byte-level (no verdict and no emittable set moves
once the file's conformance is settled as above).

### verifier-01 + quiz-02 — the dropped "no other claimant claims" qualifier

Three passages verified verbatim:

- §15.3 [R-IDX-03]: "…and none to `[R-LIF-08]`'s coverage walk, so any bytes it
  nominally addressed **that no other claimant claims** fall to slack."
- §9.7 [R-LIF-08]: "the walk passes over it, and the bytes it nominally addresses
  fall to slack (§15.3)."  — qualifier absent.
- §5.2 [R-CNT-21]: "it contributes no claimant, the walk passes over it, and its
  bytes fall to slack (§9.7)." — qualifier absent.

Both restatements are in normative bodies ([R-LIF-08], [R-CNT-21]) and neither
sits in a *Note*/*Example*/*Rationale* block, so [R-CNF-01] does not excuse them.
§21.1's "the rule governs" tiebreak does not apply — none of the three is a
register row.

The two governing definitions decide it: §5.2's "Every byte the live state does
not claim is slack" and §9.7's "Bytes the walk does not reach are slack" are
set-complements, under which a byte the front block claims is not slack however
some malformed entry nominally addresses it. Both reporters' worked examples
(T8 offset 10 length 100 reaching into [0,16); T7 offset 200 length 2⁶⁴−1
exceeding F) are correct and show the unqualified form can yield a reported total
larger than F.

CONFIRMED / editorial / not byte-level. The slack total is a MUST-level *report*,
not a verdict and not a file byte; §21.4/§21.2 reject every file exhibiting the
divergence under both readings.

### verifier-02 — the unchecksummed uninspected extent draws no naming duty

Verified. §8.1's map row is exactly "| Extent of a record of a type this
specification has not assigned | none — the bytes are opaque (§7.2) | — |".
§22.3 states that case **first** and calls corruption in it "equally invisible",
then supplies the operator remedy ("rejects on that report line, a policy above
conformance") for the *other* case only. "counted and named" and "report each
record" each occur exactly once, both inside [R-MTA-10] (lines 2798, 2794) —
the reporter's grep result reproduces.

The asymmetry is real and correctly described: the extent of an unassigned-type
record is enumerated by §9.7's walk (so it is not slack and not covered by
[R-CNT-21]'s total either), imposes no requirement a verifier is "unable to
check" (so [R-CNF-11]'s report does not reach it), and Appendix H's verifier
checklist names the [R-MTA-10] report with no counterpart.

CONFIRMED / design-decision / not byte-level. Whether to extend the naming duty
is a maintainer's call, not a mechanical edit; a verifier that names such records
and one that does not certify and reject the same files.

### verifier-03 — [R-CNF-13]'s residency-exemption example

The reporter's reading (a) — that the clause *grants* a verifier the residency
exemption — is not permitted by the words. The clause reads:

> an exemption the condition's governing requirement **grants** on a ground other
> than the declared major **applies unchanged**

"Applies unchanged" preserves; it cannot create. [R-CNT-04] grants the exemption
to "A reader that would have to issue a further range request"; §2.3 puts a
verifier outside it ("checks every file-level requirement — including those
ordinary readers are exempted from"), F6's cell says so in the row
("a verifier holds no such exemption (§2.3)"), and Appendix H says so a third
time. For an ordinary reader the example is apt; for a verifier "unchanged"
means "still none".

REFUTED / none / not byte-level.

### diagrams-01 — §4.7's Note mis-describes §7.4's column set

Verified against the tables. §4.7's Note names six per-field columns
(offset, size, type, name, class, valid range) and says of §7.4 "its table omits
the offset and class columns". §7.4's header is `| Field | Type | Constraint |` —
offset, **size** and class are all absent, and no reason is given for size.
`grep -in "size column"` returns 0 across the document, so the omission is
nowhere acknowledged. The Note's accounts of §6.1 ("a Value column replaces type
and range") and §7.2 ("folds each field's range into its Field cell") are both
exactly right, which is the register the sentence keeps; §7.4 is the one table it
gets wrong. The secondary drift is real too: the Note calls the sixth column
"valid range", three tables head it "Valid values", §7.4 heads it "Constraint".

CONFIRMED / editorial / not byte-level (the block is a *Note*, [R-CNF-01]).

### diagrams-02 — §20.5's slack inventory omits superseded payloads

Verified. The closing sentence of the "Example — what compaction reclaims" block
enumerates a per-commit directory/pad/trailer term plus a per-layer index term
and stops. §20.3's own Example says "The prior index region and the superseded
payload become slack"; step 4 adds "Extents this commit supersedes become slack
(`[R-CNT-21]`)" and, for a shortened planar channel list, "leaves its stored
tiles' extents as slack". The arithmetic checks: §20.3's worked figure gives
32·20 + 4 = 644 index bytes against a 100,000-byte superseded payload.

CONFIRMED / editorial / not byte-level (an *Example*; [R-CNT-21] and §9.7 define
the total normatively and are unqualified by this sentence).

### diagrams-03 — Appendix F omits RFC 1950 and RFC 1952

Verified. Appendix F is the only appendix whose heading carries no
"(non-normative)" marker (A, B, C, D, E, G, H all do), so [R-CNF-01] makes it
normative. `grep -c` gives RFC 1950 → 2 and RFC 1952 → 2, both occurrences in
[R-COD-05] (§17.2) and T15 (§21.4), and neither appears in Appendix F. Every
other RFC the document cites is listed there. T15's Instances cell names both
wrappers, and [R-ERR-02]/[R-VEC-03]'s one-vector-per-instance rule obliges a
corpus file for each.

CONFIRMED / editorial / not byte-level — [R-COD-05]'s "exactly one DEFLATE
compressed data stream" plus [R-COD-08]'s exact-consumption rule reject a
wrapped payload without any reader consulting either RFC.

### diagrams-04 — L26 and L31 put section references in the Governing-rule parenthetical

Verified mechanically: filtering register rows for a parenthesised section sign
returns exactly L26 (`[R-CNT-18]` (§7.3 registry table)) and L31
(`[R-CNT-23]` (§15.1)) and nothing else. §21.1 states the column's grammar:
"any **identifiers** following it in parentheses are the further rules the
condition reads, cited without brackets to keep them distinct from the governing
one" — a § citation is not an identifier, and the stated purpose of the
no-brackets convention has no application to it. 118 of 120 cells comply.

CONFIRMED / register-bookkeeping / not byte-level (§21.1's "the rule governs"
already settles any divergence, and neither row's outcome, detector or detection
point turns on the parenthetical).

### register-01 — §21.6's reason for excluding both capability refusals

Verified verbatim. The paragraph says of the second case "`[R-CNF-02]` makes the
file conforming all the same", then three lines later gives one reason for
excluding both: "a file this document declines to judge is not one". A file the
document declares conforming is not one it declines to judge. The relative clause
is offered of "a file" and reads as covering both. Reading (b) would contradict
that flat statement, [R-CNF-02], and §2.3's [R-CNF-03] clause, so (a) is right
and the second case is left with the *other* conjunct as its reason — the
register enumerates violations and a conforming file exhibits none.

CONFIRMED / editorial / not byte-level. The defect is in the reason, not in any
outcome the reason supports.

### register-02 — §21.1 attributes every §21.5 row's outcome to [R-CNT-25]

Verified. §21.1: "except where a rule assigns one expressly, as `[R-CNT-25]`'s
quarantine does for **every §21.5 row**". [R-CNT-25]'s quarantine is keyed to
unreadability and enumerates four ways — failed extent CRC, unimplemented or
invalid encoding, decode failure, content violating the document's own rules.
R4's frame-constraint instances are none of the four, and both §18.2 and R4's
own cell say so in terms:

- §18.2: "the bytes decode, and what is wrong is what the header said about them"
- R4's cell: "several, the content-size field among them, are broken by what the
  frame declares while the bytes decode"

So R4's outcome rests on [R-MTA-09]'s "Any violation here is ignore-record, never
the tile-scope outcome §17.2 assigns", not on the quarantine. §21.1's "every
§21.5 row" over-reaches. (Small misattribution by the reporter: the second
quotation above is R4's register cell, not §18.2. Immaterial.)

CONFIRMED / editorial / not byte-level. Outcome fixed twice over by §21.5's
header and [R-MTA-09].

### register-03 — F33 and L18 individuate a symmetric relation by single kinds

Half right. For **L18** the document does determine the pairs, and the reporter
missed the sentence that does it. §15.3's verifier row states three alternatives:

> two stored extents of the same layer overlap, or a stored extent overlaps its
> own layer's index region or sub-record extents

and [R-CNT-13] repeats it ("including a stored extent overlapping its own layer's
index region or sub-record extents"). L18's Governing rule cell is
`[R-CNT-13]` (R-IDX-03) — R-IDX-03 *is* §15.3 — so the three instances map one to
one onto those three alternatives: (tile ∩ tile), (tile ∩ index),
(tile ∩ sub-record). The reporter's worry that (index ∩ sub-record) goes untested
is a consequence of that enumeration, not of an under-determined cell.

For **F33** the residual is real: five claimant kinds against a condition that is
a relation, with §21.1's "An instance names a field the condition ranges over, a
container it can occur in, one of several alternatives the condition text states"
supplying no rule for which side of a symmetric pair an instance names. Two
corpus builders can produce different pairings and both satisfy §21.8's letter.
The reporter's own arithmetic objection (three stated alternatives not yielding
five) is correctly set aside by them.

PARTIAL / register-bookkeeping / not byte-level ([R-CNT-13] fixes reject-file for
cross-scope and reject-layer for intra-layer whichever pair a vector exercises).

### register-04 — R10 alone among the [R-MTA-04] rows omits (R-CNT-25)

Verified against the table: R6 `(R-CNT-25, R-ENC-12)`, R7 `(R-CNT-25)`,
R8 `(R-CNT-25)`, R9 `(R-CNT-25)`, R10 `(R-ENC-12)`. The R6/R10 pair is the same
folding of §4.6's name rules onto keys (R6 takes non-empty and C0-free, R10 takes
the 255-byte cap) and nothing distinguishes what they read. §21.1 asserts the
quarantine assigns the outcome "for every §21.5 row", so a tool harvesting the
cells to check that claim finds one row that does not cite it.

CONFIRMED / register-bookkeeping / not byte-level.

### register-05 — §21.1's governing rules carry no identifier

Verified. §21.1 states, in normative text under [R-CNF-01], the rule-governs
tiebreak, "Its **completeness is normative**", the specialization rule and the
whole Instances arithmetic, and carries no `[R-<PREFIX>-<NN>]` of its own; the
same is true of the §21.2–§21.6 header paragraphs. The first ERR identifier is
[R-ERR-01] at the end of §21.7. §2.2 states the convention: "Normative
requirements carry identifiers of the form `[R-<PREFIX>-<NN>]`."

One supporting argument of the reporter's fails. [R-VEC-02] requires a vector to
record "the §21 register row it exercises together with **that row's** governing
requirement identifier" — every row has one; it does not ask for an identifier
for §21.1's tiebreak. The reporter's counter-argument against itself (§2.2's own
sentence is unidentified, so the convention is not universal) is sound and worth
keeping.

CONFIRMED / design-decision / not byte-level. Whether §21.1's decision procedures
get identifiers is a maintainer's call; the register binds through [R-CNF-04] and
[R-CNF-07] either way.

### register-06 — F5's second instance names committed_file_length

Refuted on §21.1's own conventions. §21.1 says:

> any identifiers following it in parentheses are the further rules the condition
> reads

F5's cell is `[R-CNT-27]` (R-CNT-01, R-CNT-06), and [R-CNT-01] is precisely the
rule that ties the two quantities: "The file size of a conforming file equals the
live trailer's committed file length F". A trailer declaring
committed_file_length below 128 declares a file size below the minimum, so the
condition — "File size is below the 128-byte minimum" — ranges over it, and the
parenthetical supplies the rule the condition reads to know that. There is no
row/rule divergence for §21.1's tiebreak to resolve. The two instances are
distinguishable files (a 64-byte file; a 192-byte file declaring 64), which is
all §21.1 asks, and §24's [R-VEC-02] already provides for the second
co-exercising F17.

REFUTED / none / not byte-level.

### adversary-01 — "structure" in §5.1 against §5.2's definition

The competing reading (B) is not permitted. §5.2 supplies the express definition —
"a **structure** — a stored-tile extent, a record extent …, the directory, or the
trailer" — as a class of *the live committed state's* partition; [R-CNT-05] uses
the term over the pre-trailer gap while citing §5.2 for the pad's status; F7's
Governing rule is `[R-CNT-05]` (R-CNT-02), pointing at that definition; and F7's
Instances cell enumerates live-state claimant kinds only. §5.1's sentence is
descriptive anatomy inside [R-CNT-01], whose operative clause is its last one.
Reading (B) would also require an actor to identify opaque bytes as a superseded
region, which §9.6 forecloses ("no verdict turns on the probe") and would reject
files §21.6 declares conforming ("A payload contains a byte string that mimics a
trailer | Inert").

What *is* real is the narrower thing the reporter's title states: §5.1 applies an
expressly-defined term to superseded directories and prior trailers, which the
definition excludes. That is an editorial defect worth a word change, not an
ambiguity.

PARTIAL / editorial / not byte-level.

### adversary-02 — does R2 survive at an experimental-range encoding?

Reading (B) dies on the preamble's own next clause and on [R-MTA-10]. §21.5:

> what `[R-MTA-10]` withdraws is **the document's content rules**, never the
> encoding byte's own value set (`[R-MTA-03]`)

An extent's terminal CRC over stored bytes is not a document content rule. And
[R-MTA-10] names it inside a closed three-item list of what decides conformance
there:

> file conformance … is decided by the structural checks that precede the
> document alone: the record's framing and extent slot (`[R-CNT-13]`), the
> encoding byte's own value set (`[R-MTA-03]`), and **the extent's terminal CRC**
> (`[R-CNT-20]`)

§22.3 says it a third time ("covered by its terminal CRC but constrained by no
content rule … the CRC detects corruption"), and §21.6's "a verifier certifies"
entry is qualified by [R-MTA-10]'s "in an otherwise conforming file". §21.1
makes the rule govern both the row and the §21.6 entry.

REFUTED / editorial / not byte-level. The only residue is a symmetry point: the
preamble takes the trouble to name R1 as surviving and could name R2 beside it.

### adversary-03 — §2.1's Note asserts two invariants the document does not satisfy

Both limbs check out.

*Limb 2* I re-swept independently. Every normative SHOULD I could find states a
consequence — [R-CNT-03] ("forfeits byte reproducibility"), [R-ENC-14] ("risks
visually identical but byte-distinct names"), [R-CNT-07] ("misleads users"),
[R-CNT-09] ("merely costs the second request"), [R-CNT-10] ("remote open fails
outright"), [R-CNT-26] ("misstates the file's feature floor"), [R-LIF-03]
("lets two distinct files collide"), [R-LIF-07] ("recoverable only by scanning
back"), [R-CNT-20] ("silent metadata loss defeats the record's purpose"),
[R-TYP-10] ("read back as a value consumers … will not expect"), [R-MTA-04]
("belongs in a structural field"), [R-MTA-06] ("another application can mean
something else by it"), [R-COD-06] ("merely permits a conforming reader to
decline"), [R-SEC-03] ("smuggled bytes travel unexamined"), [R-PRV-05] ("visible
to anyone on the path"), §20.3 step 2, §20.4's drop, §20.5's minor floor — except
[R-MTA-09]'s closing "the verifier SHOULD report the bound it applied and the
stored length of the extent it declined", which states none. Accurate.

*Limb 1*: §20.3 step 4's "A commit MUST NOT change one of these" carries no
reader-side clause and no §21 row, and none exists elsewhere because the
condition is unwitnessed. Two of the reporter's other three exceptions are
softer than presented — [R-LIF-01]'s reader side is [R-LIF-05]'s
trailer-at-end-or-fail, and §9.5's Note expressly supplies [R-LIF-04]'s
("What the residue violates is `[R-LIF-04]`'s writer obligation … and the state a
reader can observe is already named") — but the Note's claim is falsified by step
4 alone.

Where the reporter is wrong is the inference: "That leaves the file
nonconforming-but-invisible." §2.3 makes file conformance "a pure predicate on
bytes", and §5.2 says of the only bytes that witness a step-4 breach that "no
conformance requirement applies to it". The file is conforming; the actor is
bound. That is the coherent position, and it is not "never stated" — it is
stated, just not at step 4.

CONFIRMED / editorial / not byte-level (a *Note*, [R-CNF-01]).

### adversary-04 — the channel-replacement gloss

Reading (2) is not permitted. The gloss's own "so" ties it to the composition it
glosses: "a commit that shortens a planar layer's channel list appends no channel
to it and one that extends it removes none, whatever the counts, **so** replacing
the last channel … is two commits or a rewrite." A rename extends nothing and
shortens nothing; the channel count is unchanged. Against it stand the closed
list's unqualified first member ("its name, and its dimension and channel names,
MAY change") and the justification paragraph ("a name enters no map this
specification defines, and a commit MAY change several names at once, two swapped
included"), plus Appendix H's unqualified rename permission.

The reporter's real point survives and is worth an edit: the gloss is phrased over
a *result* (the last channel differs) while the ban is over an *operation*
(extend and shorten in one commit). Harmless in fact — a replacement that changes
type or fill is separately forbidden by the fixed side, and one that changes
neither is a rename — but loose.

PARTIAL / editorial / not byte-level.

### quiz-01 — "the position of every planar channel but the last"

The step supplies its own tiebreak and the reporter found it:

> where a field is on both sides — a dimension extent, **a planar layer's channel
> list**, an interleaved layer's channel list — the permitted side states the
> whole of what a commit MAY do to it

The planar channel list is named there expressly, so Reading 2 is foreclosed and
a trailing run of any length may go in one commit. The "gives up" list agrees:
"a planar channel inserted or removed anywhere **but the end of the list**".

The phrasing defect is nevertheless real: "but the last" says one channel where
"but those at the end" is meant, and the deciding sentence sits several sentences
below, in a paragraph about entry_count and sub-records.

CONFIRMED / editorial / not byte-level. §9.3's Note ("how many commits a file has
undergone is not recoverable from the live trailer, and no field records it")
makes the one-commit and two-commit outputs equally conforming and
indistinguishable in the live state.

### quiz-03 — compactor refusal turns on a free placement choice

Every link verified. [R-WRT-07] regenerates "each tile-index region any of whose
stored extents the output relocates"; the §20.5 figure calls placement "the
compactor's to choose"; regeneration then "cannot proceed without meeting"
a structurally-rejected entry and [R-WRT-06] "then obliges refusal"; and
[R-WRT-09]'s depth "reach[es] the index chain and each stored tile's entry crc
rather than an entry's own value domain". [R-WRT-01] sanctions the other branch:
"a violation latent in a structure it carries forward verbatim travels into its
output". The reporter's example (offset 4096, length 0, crc 0) is structurally
reject-tile under §15.3's "length = 0 (non-sentinel)" row (T10).

So both compactor behaviours are licensed by stated text, on an input that is
already nonconforming and that every conforming reader rejects at tile scope
under either branch. Accurately reported, and reported as an observation rather
than a defect, which is the right call.

CONFIRMED / design-decision / not byte-level.

---

## Byte-level tally

One: **writer-01**. Reporters flagged one; I uphold that one and downgrade none,
so no downgrade quotation is owed. The uphold's refuter should be told to look for
a sentence — anywhere — stating whether an alignment or slab declaration already
carried by a layer that stores a tile may take a different nonzero value in one
commit, and to attack the premise recorded above (that the "What the line gives
up is stated rather than carved around" list's silence does not decide it).

## Coverage

25 input ids, 24 groups, one merge (verifier-01 + quiz-02). Every id counted once;
union of member_ids equals the input list exactly. No id dropped, no id doubled.
No gaps: I reached a judgement on all 25.
