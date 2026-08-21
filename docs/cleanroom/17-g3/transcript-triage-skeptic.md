# Round 17 triage — skeptic pass

## Disclosure

Read: `spec/tarn.md` only — §2.1–§2.5, §3.1–§3.2, §5.2, §6.1–§6.4, §7.2–§7.3,
§9.1–§9.7, §11.1–§11.2, §13.3, §15.3–§15.4, §18.2, §19.1–§19.4, §20.1–§20.5,
§21.1–§21.9, §24, Appendix G, Appendix H. Also `wc -l` and a heading listing
and three greps (`R-CNT-10`, `R-TYP-09|R-MDL-02|R-LIF-08`,
`logically modif|independently|attaches to`).

Read no walk transcripts (I did not need a reporter's fuller reasoning; every
finding quoted enough to locate). Read no `transcript-triage-*.md`; I did not
list `round17/`. Read no `docs/`, `PLAN.md`, `AGENTS.md`, `conformance/`,
`spec/registry.json`, git history, or web.

Nothing was left unevaluated.

## Grouping

17 groups over 34 ids.

| group | members |
|---|---|
| shrink-quantifier-in-11-1 | reader-01, writer-03, verifier-01, diagrams-01, register-01, adversary-03, quiz-01 |
| drop-licence-modifying-a-layer-record | writer-01, verifier-03, adversary-02, quiz-02 |
| compactor-refuse-vs-reproduce-entry | reader-02, writer-02, verifier-02, register-03, adversary-01 |
| removing-a-layer-dead-branch | reader-04, diagrams-03, register-05 |
| quarantine-preamble-vs-r2-at-experimental | reader-03 |
| quarantine-preamble-omits-bound-decline | writer-05, adversary-04 |
| t3-described-as-entry-level | register-02, quiz-04 |
| durability-barriers-unaccounted | writer-04 |
| structural-entry-not-stable-under-new-F | verifier-04 |
| appendix-g-file-id-fallback | writer-06 |
| appendix-h-omits-pad-bits | diagrams-02 |
| shrink-sentence-vs-fill-carve-out | diagrams-04 |
| shape-c-whatever-its-geometry | diagrams-05 |
| 21-1-carries-no-identifier | register-04 |
| err-04-decline-unqualified | register-06 |
| local-remote-and-nothing-else | quiz-03 |
| appendix-g-item-3-record-extents | quiz-05 |

Merges worth defending:

- The seven §11.1 findings are one sentence and one repair. diagrams-01 and
  register-01 add a second clause of the same sentence ("permitted where it
  drops tiles out of the addressed set"); that is the same defect, repaired by
  restating the same sentence, so it stays in the group and is named in the
  action.
- writer-01/quiz-02 (supersede framing) and verifier-03/adversary-02 (store
  framing) are one defect: the undefined sense of "modifying any layer's
  record" in §20.4's MU=0/PE=0 row. One insertion of "logically" repairs both
  framings. Splitting would hide that the supersede half is expressly decided
  and the store half is not — which is exactly the fact that makes the group
  byte-level.
- reader-03 and writer-05/adversary-04 both attack §21.5's preamble but on
  different axes (whether the experimental-encoding exception withdraws R2 vs
  whether the disjunction omits the §18.2 bound-decline). Different questions,
  different repairs, two groups.

## Groups I tried hardest to kill and failed

**drop-licence-modifying-a-layer-record.** I hunted for a sentence that names
the store case. Candidates and why each fails:

- §20.4 opening — "every record it retains and does not **logically** modify"
  — "logically" is load-bearing, but the drop licence three lines later says
  "modifying any layer's record", unqualified, and nothing ties the two words
  together.
- The carve-out — "Superseding a stored tile's bytes is not such a change for
  either kind — it re-places that layer's index region (§20.3, `[R-WRT-04]`)
  without altering the scope any record attaches to". Its *reason* is general
  and would cover a store; its *terms* name superseding alone. Naming one
  operation and not its twin cuts toward the store being inside the licence.
- §20.3 step 4 — "A layer whose record alone changes keeps its extent slot" —
  distinguishes the categories but defines no sense of "modify".
- `grep 'logically modif|independently|attaches to'` returns nothing else in
  the document.

Both readings are internally coherent. Under (a) the carve-out is a special
exemption for supersede and the store is unexempted; under (b) the carve-out
is clarifying and the store is excluded by parity. Two conforming updaters,
one input, one instruction ("store layer A's tile at disk ordinal 1"), two
directories differing by a 24-byte record, dir_length, directory CRC,
committed_file_length and trailer CRC — both outputs conforming files, so one
of the two updaters is nonconforming under `[R-CNF-06]` and the document does
not say which. That is squarely "which byte sequences a conforming
implementation may emit". Upheld byte-level. Sole byte-level of this pass.

Note the sub-case that is *not* in doubt: for a **layer sub-record**, storing a
previously-unstored tile changes "which of its tiles are stored", which the
row lists expressly. The fork exists only for a **top-level** MU=0/PE=0
record, whose branch reads "the file's layer set — which a commit changes by
adding or removing a layer and equally by modifying any layer's record".

**durability-barriers-unaccounted** (writer-04). I looked for an accounting of
`[R-LIF-02]` steps 4 and 6 and found none: §21.7 ¶2 names six classes and the
barriers are in none of them by citation. The rescue I did find is that
"properties of a file's history, which §9.7 does not reconstruct" plausibly
*covers* the barriers as a class even though the parenthetical cites only
`[R-LIF-01]`/`[R-LIF-03]` — and §21.1 calls §21.7 "the account, **by class**,
of what fails it", which licenses reading the citations as exemplary. That is
why this is PARTIAL rather than CONFIRMED. It cannot be byte-level: the two
files a barrier distinguishes are byte-identical by construction, which is the
reporter's own premise and §21.7 ¶2's stated criterion.

## Downgrades, with the deciding text

### shrink-quantifier-in-11-1 (7 reporters, all self-downgraded; I concur)

`[R-CNF-01]`, §2.1: "All text in this document is normative except: §1
(Introduction); any text labeled *Note*, *Example*, or *Rationale*; and
appendices identified as non-normative."

The §11.1 block opens `> **Rationale.**` (line 1481) and says of itself
"§20.3 states normatively, and governs".

Tested against a construction none of the seven leaned on: could §11.1's
weaker guard ever *license* bytes? No — a permission stated in Rationale text
licenses nothing, so the set of commits a conforming appender may perform is
single-valued and fixed by §20.3 step 4. The disputed commit (shrink that
turns real positions into padding of a superseded-generation stored tile, that
tile unstored in the same commit) yields a *conforming file* whose emission
`[R-WRT-04]` nonetheless bars; that is the one direction where a normative
fork would have been byte-level, and it is closed by `[R-CNF-01]`. The defect
is real and worth repairing — §11.1 is where a schema-first writer meets the
question — but it is a paraphrase, not a rule.

Second clause, same sentence: §11.1's "permitted where it drops tiles out of
the addressed set" states as sufficient what §20.3 states as "not itself such
an alteration — but neither does it rescue a commit that damages a
prior-generation stored tile." Same repair.

### compactor-refuse-vs-reproduce-entry (5 reporters; 3 flagged byte-level)

Deciding text, `[R-WRT-07]`, §20.5:

> "`[R-WRT-09]`'s checks reach the index chain and each stored tile's entry
> crc, not an entry's own value domain, so such an entry is not one
> `[R-WRT-06]` obliges a compactor to refuse"

Premise of my downgrade, stated so it can be attacked: **that clause is an
express disposition of the whole of `[R-WRT-06]` for this entry class, and the
"so" that introduces it does not narrow its scope to the limb the preceding
clause argues about.** `[R-WRT-06]`'s second limb reaches a refusal only
through its own closer ("Where the table does not license a drop the compactor
MUST refuse"), so an entry that is "not one `[R-WRT-06]` obliges a compactor
to refuse" is outside that closer too.

Two supporting readings:

- `[R-WRT-06]`'s disposal apparatus is framed over *records*: "Dropping is the
  one disposal that answers, and only where §20.4's table licenses it: **a
  record dropped is not in the output**". §20.4's table licenses drops of
  records; an index entry is not a record and is not a structure that table
  reaches at all.
- §20.5's opening already contemplates violations reaching the output: "a
  violation latent in a structure it carries forward verbatim travels into its
  output (`[R-WRT-01]`) — its verification depth is `[R-WRT-09]`'s and reaches
  no decoded content."

What survives: the *justification* is false. `[R-WRT-09]` says the compactor
"relies structurally on every structure it copies", §2.3 makes updaters
readers inheriting every reader obligation, `[R-CNF-04]` binds a reader to
every reader-detected row, and `[R-WRT-07]` itself directs classification per
§15.3 — so the compactor has detected T6–T12 in fact. A stated conclusion
resting on a premise its neighbours refute is what pushed two of five
reporters to the opposite implementation. Repair is required; the ground
should be "no disposal exists and `[R-WRT-05]` bars correction", per
register-03's suggestion, not `[R-WRT-09]`'s reach.

This is the group most likely to be overturned by the refute pass. If the
maintainer reads the "so" as narrowing, the fork is real and byte-level: A
emits nothing, B emits a file whose index region carries the malformed entry
verbatim. I flag it as design-decision so the repair happens either way.

### structural-entry-not-stable-under-new-F (verifier-04)

The mechanism claim does fail: §15.3's row "offset + length overflows, or
offset + length > F − 64 (non-sentinel)" is F-relative, and no rule bounds a
compactor's output length ("free to place structures anywhere §5.2 admits").
For F_out ≥ offset+length+64 the reproduced entry is well-formed in the output
and the promised violation does not travel.

Why not byte-level:

- §3.2 `[R-MDL-01]`: "Each layer of a **conforming file** denotes exactly one
  reference array". The input here is nonconforming, so `[R-WRT-07]`'s "The
  output's reference arrays MUST equal the live generation's bit for bit" has
  no defined referent and cannot be the second horn of a dilemma.
- §20.5: "**Given a conforming input** the output is a conforming file." The
  output-conformance promise is conditioned and is not breached.

So the compactor's mandate ("reproduced with its offset and length exactly as
they stand") is single-valued, and every implementation reading §20.5 emits
the same class of bytes; what is defective is a factual claim in normative
prose, plus a real hole (a tile-scope violation can become a file-scope
overlap). Reachability requires F_out > F_in, which compaction does not
normally produce but nothing forbids.

### quarantine-preamble-vs-r2-at-experimental (reader-03) — REFUTED

Reader-03's reading (a) requires the exception to range over the whole failure
set. The preamble's own next sentence forecloses it:

> "Encoding 0 and a reserved-range value are unassigned too, and R1 registers
> both as violations: **what `[R-MTA-10]` withdraws is the document's content
> rules**, never the encoding byte's own value set (`[R-MTA-03]`)."

and the exception clause is itself qualified — "except at an
experimental-range encoding, **where no document rule attaches**". A failed
extent CRC is `[R-CNT-20]`, not a document rule. `[R-MTA-10]` says the same
from outside: conformance under an unassigned encoding "is decided by the
structural checks that precede the document alone: the record's framing and
extent slot (`[R-CNT-13]`), the encoding byte's own value set
(`[R-MTA-03]`), and the extent's terminal CRC (`[R-CNT-20]`)."

The reporter quoted the exception without its own relative clause and without
the sentence after it. Refuted; no repair owed.

### err-04-decline-unqualified (register-06) — REFUTED

§2.3, inside `[R-CNF-03]` itself: "(§21.9's `[R-ERR-04]` governs a refusal on
that last ground; §21.6's closing paragraph names the other two)". The scoping
is express, in the rule `[R-ERR-04]` cites. The next sentence of §21.9 is
"Either way, a refusal **on resource grounds** MUST be reported as a resource
limit". A two-word clarification is cheap and I recommend it, but nothing is
undecided.

### shrink-sentence-vs-fill-carve-out (diagrams-04) — REFUTED

Same paragraph, four lines above the sentence complained of: "An extent MAY
also **shrink**, and **the bar above is the whole of the test**, **in the
bar's own tense**". The "bar above" is the sentence that contains the
carve-out ("a new padding position whose stored byte already holds the fill
`[R-SER-05]` fixes — is not what this bars"). Reading (ii) — an independent
second bar with no carve-out — is foreclosed by the clause that opens the
sentence's own paragraph.

### local-remote-and-nothing-else (quiz-03) — PARTIAL

`[R-CNT-10]` — the rule the §6.2 parenthetical points at — lives in §6.4, and
§19.1 step 1 obliges *every* reader to "Obtain the transport-authoritative
file size F (`[R-CNT-10]`)". No obligation in §6.2 turns on the
classification: the parenthetical names where a remote transport's F comes
from, and §6.4 is where the MUST sits ("The size a remote reader compares
against committed_file_length MUST be transport-authoritative"). §6.1's
purpose — "the obligation over the front block turns on residency instead" —
is served either way. Loose, not false.

### 21-1-carries-no-identifier (register-04) — PARTIAL

§2.1's Note states the drafting discipline: "every requirement names the actor
it binds (writer, reader, updater, verifier, or file)". §21.1's statements
bind no actor — they are interpretive rules about this document — so §2.2's
"Normative requirements carry identifiers" does not obviously reach them.
The cited cost also does not materialize: `[R-VEC-02]` requires a vector to
record "the §21 register **row** it exercises together with that row's
governing requirement identifier"; §21.1's precedence rule is not a row and no
vector exercises it.

### appendix-g-file-id-fallback (writer-06) — PARTIAL

The profile's convention throughout is an adopter-supplied pin, not a value
this appendix names: item 1 "a named codec implementation at a named version",
item 2's own hash "a named function at a named version", item 9 "a named JSON
writer at a named version". "Any other fixed nonzero value" is the same shape.
Naming a constant is still the better drafting and costs six words; two
adopters who have agreed on a hash function have to agree on one more thing.
Non-normative either way: "It adds no requirement to any actor: a writer
ignoring it is fully conforming."

### The remaining editorial confirmations

- **removing-a-layer-dead-branch** — the table cell says a commit changes the
  layer set "by adding or **removing** a layer"; the paragraph 2 lines below
  says "No commit therefore removes a layer record, or a user-metadata record
  at either scope." Unreachable trigger, so no file's bytes turn on it. Strike
  "or removing".
- **t3-described-as-entry-level** — §21.7: "witnessed by T3 or T14, which read
  the index entry rather than the decoded image". True of T14
  (`[R-COD-04]`, checkable before any payload fetch); false of T3, whose
  condition is "The decoded payload's byte length is not exactly the tile's
  decoded size". Both rows still fire on the same files, so nothing forks.
- **appendix-h-omits-pad-bits** — verifier block: "decoded-content obligations
  — padding samples and interleaved boolean bytes (§14.5, §14.2)"; the writer
  block four paragraphs above: "fill-encodes edge padding **and pad bits**".
  T5 matches no clause. Non-normative and self-disclaiming: "each entry's
  authority is the requirement or section cited, never this summary."
- **shape-c-whatever-its-geometry** — the Example's "whatever its geometry"
  has no counterpart in step 4, whose own text says "a growth is permitted
  exactly where the geometry it produces satisfies every rule that geometry is
  subject to" and distinguishes an *empty* layer ("which an empty layer
  escapes only because that cap is quantified over addressed tiles") from one
  that merely stores no tile. `[R-CNF-05]` closes it independently.
- **appendix-g-item-3-record-extents** — §5.2 does make a tile-index region a
  record extent ("a record extent (the bytes any record's extent slot
  references, whatever the record's type, §7.2)"), and §20.5 says so in terms
  ("itself a record extent (§5.2)"). Reading (2) is unsatisfiable for a
  two-layer file, so only reading (1) is available. One word: "any
  *remaining* record extents".
- **quarantine-preamble-omits-bound-decline** — the harmful outcome is
  foreclosed by `[R-MTA-09]`: "the decline is not a finding that the file is
  nonconforming and a verifier **MUST NOT** report it as one." And the
  document reserves "unreadable" for the document's own defects (§18.2: "a
  document violating any of them is unreadable") while phrasing the bound case
  reader-relatively ("ignore-record like any other **it cannot read**"), which
  is a rescuing reading of the preamble. Loose, decided.

## Coverage check

Counted by hand from the group table: 7+4+5+3+1+2+2+1+1+1+1+1+1+1+1+1+1 = 34.
Each of the 34 input ids appears in exactly one group; no duplicates.

Byte-level groups: 1 (drop-licence-modifying-a-layer-record).
