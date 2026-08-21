# Round 18 triage — implementer-consequence lens

## Disclosure of access

Read: `/Users/robertkleffner/Documents/GitHub/tarn/spec/tarn.md` only — §2.1–§2.5,
§4.7, §5.1, §5.2, §6.1–§6.4, §7.1, §9.1–§9.7, §14.3, §14.5, §17.3, §17.4,
§18.2, §20.1–§20.5, §21.1–§21.9, §23.1–§23.3, §24, Appendix G, Appendix H,
plus a `grep -n "^#"` for the section map and a `grep -n version_minor`.

Read NO transcript of any kind — not the six walk transcripts, not the quiz
transcripts, and no `transcript-triage-*`.

**Protocol deviation to disclose:** my first command paired `wc -l` on the spec
with `ls | head -20` on the round18 scratchpad directory, which the charter told
me not to do. The listing returned 15 entries (build/calc/crc/reader py files,
`sst.tarn`, `__pycache__`, and the nine `transcript-<role>` / quiz files). No
`transcript-triage-*` name appeared in it — alphabetically such names would have
sorted between `transcript-register.md` and `transcript-verifier.md`, and nothing
sat there — so at that instant none existed. I opened none of the listed files.
The deviation gave me no information about the other two passes.

No web, no `docs/`, no `PLAN.md`, no `AGENTS.md`, no `conformance/`, no
`spec/registry.json`, no git history.

---

## The byte-level test I applied

> Does resolving this change which byte sequences a conforming implementation
> may emit, or must accept or reject?

Two refinements I had to make explicit before I could use it consistently, both
stated here so they can be attacked:

**(A) "May emit" is per-operation, not per-file-set.** Almost every candidate
here produces two outputs that are *both* conforming files. That alone does not
kill a byte-level flag: the question is whether, *given the same input and the
same operation*, the set of outputs a conforming implementation may produce
differs between the readings. If it does, two teams ship compactors that emit
different bytes for the same file and each believes the other is wrong. That is
a fork.

**(B) A conduct rule can still fork bytes.** §2.3 puts some writer obligations
outside file conformance (`[R-CNF-02]`). A rule being conduct-level does not make
it inert: it still determines what the writer writes. What *does* make a
divergence inert is when the document forecloses one reading, or when the
divergent bytes are ones the document expressly places outside every
requirement (slack, `[R-CNT-21]`).

Refinement (B) is what separates group 16 (upheld) from group 4 (downgraded), and
I say so in each.

---

## Grouping

17 groups over 26 ids. Every id in exactly one group; union checked by hand and
by count (4+1+4+1+1+1+1+3+1+1+1+1+2+1+1+1+1 = 26).

### G1 `sec21-7-only-vs-its-own-witnesses` — reader-01, verifier-01, diagrams-01, register-03

Four reporters, one sentence, §21.7. All four read it the same way (the "only"
governs "the affected tiles remain stored" alone). Trivially one group.

Verified in the text: the sentence really does say "witnessed only where the
affected tiles remain stored *and* the change reaches a byte §14 structurally
constrains", then names T3/T14 for a decoded-size change and T15/T17/T23/T25 for
a codec change. T3, T14, T15, T17, T23, T25 all exist in §21.4 with detector
*reader* and their own governing rules. So reading (a) makes §21.7 assert
something false about the register.

**Implementer consequence:** none that reaches a byte. §21.7 imposes no check on
anybody, and it is expressly outside the register's machinery:

> "The subsections after §21.5 are not part of the register and carry no rows:
> neither this completeness clause nor the instance arithmetic below reaches
> §21.6's defined non-violations, §21.7's account of what no check detects, or
> §21.9's limits." (§21.1)

and

> "where a row and the rule it cites diverge, **the rule governs**." (§21.1)

A reader implements T3/T14 because `[R-CNF-04]` and §21.4 say so; a corpus
builder builds vectors because §21.8 quantifies over §21.2–§21.5 rows, which
§21.7 is not. Nothing an implementation does changes. Editorial.

Premise of my downgrade, stated for attack: *§21.7 assigns no obligation and
carries no rows, so the only thing at stake is which of two accounts a reader of
§21.7 believes.* The way to attack it would be to find an obligation that runs
*from* §21.7 — §21.1's "§21.7 the account, by class, of what fails it" is the
closest, and it is a pointer, not a delegation.

### G2 `sec21-7-t5-mis-strided-filter` — register-01

Different sentence of §21.7, different claim. Not the "only" defect. Own group.

I checked the mechanics rather than the reporter's account. §17.3: filtered image
places byte i of group j at offset i·n + j, n = L/s; inverse restores i·n + j to
j·s + i. Solve i·n + j = L − 1 with 0 ≤ j < n, 0 ≤ i < s: i = s − 1, j = n − 1,
source offset (n − 1)s + s − 1 = ns − 1 = L − 1. So the final byte is a fixed
point of the shuffle at every stride. §14.3 puts a packed planar bool plane's pad
bits in the final byte and nowhere else; §17.3 mandates s = 1 (identity) for such
a plane, so the reader's inverse is the identity and the writer's own final byte
survives into the decoded image. T5 cannot fire from a stride error. T26's cell
("the check that detects it is T2's or T4's") is right; §21.7's "exactly as a
mis-strided filter is" over-extends the analogy by one row.

Note the analogy's *subject* — a mis-ordered image — genuinely can exhibit T5
(swap two planar planes whose channels' fill bits differ). So only the "exactly
as" half is wrong.

**Implementer consequence:** a corpus builder who took §21.7 literally would try
to construct a T5-witnessed vector for T26's "packed planar bool: identity s = 1"
instance and fail — no such file exists. But T26's own cell tells him T2 or T4,
and §21.1 makes the rule (`[R-COD-10]`) govern over any restatement. No byte, no
verdict. Editorial.

### G3 `compactor-duties-keyed-to-relocation` — reader-02, writer-04, adversary-02, quiz-03

The merge that took the most thought. Four findings, three sentences, one word.

- `[R-WRT-09]`: "each **relocated** extent's checksum" — against its own premise
  "it relies structurally on every structure it **copies**" (reader-02).
- `[R-WRT-07]`: "regenerates each **relocated** tile-index region" — under-inclusive
  when the region stays and its tiles move (writer-04).
- the same clause — over-permissive when the region stays and an entry in it is
  structurally malformed, so the refusal duty is never triggered
  (adversary-02, quiz-03, which are the same finding in different words).

All three turn on `relocated` being the trigger while §20.5 leaves placement free:

> "A compactor preserves content but not placement — placement is not among the
> things it carries forward, and it is free to place structures anywhere §5.2
> admits and every declared layout invariant permits"

and §20.5's own figure confirms a structure can keep its input offset: input
`│front│ A │▓▓▓▓│ B │…`, output `│front│ A │ B │…` — layer A's tiles sit at the
same offset in both rows. So the coincidence case is not hypothetical; it is the
figure. One repair (re-key the three duties to emission/carriage, or state that a
compactor relocates every structure) fixes all four findings. Merged.

**Implementer consequence, concretely, in both directions:**

- Compactor A relocates everything, regenerates every region, verifies every
  extent it emits. On a damaged input it refuses.
- Compactor B keeps the first structure at offset 16, never regenerates that
  layer's region, never verifies that extent. On the same damaged input it emits
  a file.

**Byte-level? No — but two different sentences decide it, and I nearly missed
that.** My first premise was "the divergence only arises on a nonconforming
input", which is true for reader-02 and for adversary-02/quiz-03 (a conforming
input has no failing CRC and no structurally malformed entry), and there:

> "a violation latent in a structure it carries forward verbatim travels into its
> output (`[R-WRT-01]`)" and "Given a conforming input the output is a conforming
> file." (§20.5) — plus `[R-CNF-12]`: "For a nonconforming file no acceptance
> obligation exists".

But that premise is **false for writer-04**, whose case arises on a perfectly
conforming input: region stays, tiles move, literal reading copies the region
verbatim, output entries point at slack. So writer-04 needs its own deciding
sentence, and it has one in the same requirement:

> "The output's reference arrays MUST equal the live generation's bit for bit
> (`[R-MDL-02]`): compaction changes where bytes live, never what a layer
> denotes." `[R-WRT-07]`

A conforming compactor may not emit that output whichever way the trigger clause
is read. So: not byte-level, but design-decision rather than editorial, because
the maintainer has to *choose* the trigger.

### G4 `lif04-residue-survives-into-a-committed-state` — writer-01

Checked the scenario. `[R-LIF-04]`'s second option is "overwrite from F and
truncate the physical file to the new committed_file_length no later than step 6";
with F = 704, residue to 900, a first structure at [704,750) and a 4096-aligned
second, F' = 8192, the truncate is a no-op and [750,900) survives as slack of the
new live state. The trailing "bytes beyond a committed length never survive into
any committed state" is therefore false under the narrow reading of "overwrite
from F".

**Byte-level? No, and the sentence that decides it is `[R-CNT-21]`:**

> "Slack has no internal structure this specification defines, its content is
> **unconstrained**, and **no conformance requirement applies to it**."

Reading (a) — "overwrite from F" means overwrite all of [F, old physical end) —
would impose a conformance requirement on the content of particular slack bytes,
which that sentence forbids in terms. §5.2's Rationale adds that the obligation
would not even be testable: "Certifying its content would mean deciding which
slack bytes *this* commit wrote, which is not decidable from the live state."
And §9.7 puts it outside a verifier's concern: "Bytes the walk does not reach are
slack: the verifier sums them and reports the total, and their content is not its
concern."

So the two implementations — truncate-first and write-from-F — produce files no
checker can tell apart, and `[R-CNT-03]`'s zeroing is SHOULD-level either way.
This is the case where refinement (B) above *does* bite: the divergent bytes are
the ones the document expressly places outside every requirement.

The residue does have a real consequence the reporter names and I confirm: §23.1
accounts only for *superseded* bytes, and an abandoned commit's bytes republished
into a live file are neither superseded nor described. §9.6's backward probe
would find an abandoned trailer sitting in that residue on a later torn state.
That is a privacy-disclosure gap, not a byte fork. Design-decision: narrow the
clause, or strengthen the requirement to cover the whole old tail and say so.

### G5 `appendix-g-item-8-no-compactor-carve-out` — writer-02

Confirmed against the text. Item 2 carries "This is a creator's rule: a compactor
adopting the profile takes `[R-WRT-06]`'s fresh draw instead"; item 8 carries no
such clause, and item 4's "One generation" is satisfied by a compacted file
(generation 1 by definition). So item 8 reaches compactors, and it tells them
`flags` = 0 — against §6.3's "A compactor, though its output is a new file,
carries the input's unknown ignore-lane bits into its output trailer rather than
writing flags = 0" and `[R-CNT-08]`'s "MUST NOT clear them" — and version_minor
at the floor, against §20.5's max.

**Byte-level? No, and this is the quotation that decides it:**

> "**Appendix G — Reproducible-writer profile (non-normative)**" … "It adds no
> requirement to any actor: a writer ignoring it is fully conforming"

together with `[R-CNF-01]`'s exclusion of "appendices identified as
non-normative". §2.3 defines five conformance classes and profile-adoption is
none of them. A conforming compactor is bound by §6.3 and §20.5 whatever the
profile says, so the profile cannot widen or narrow the set of byte sequences a
*conforming* implementation may emit. What it can and does break is the profile's
own promise: two profile-adopting compactors emit different trailers and both
claim reproducibility. That is a defect worth fixing and it is not the gate's
subject.

Entangled with G16: item 8's version_minor half cannot be written correctly until
G16 decides §20.5's modality. Design-decision, and sequenced after G16.

### G6 `one-failed-extent-crc-forecloses-compaction` — writer-03

Walked the four hops myself. `[R-WRT-09]` obliges "each relocated extent's
checksum, including every stored tile's entry crc". `[R-WRT-06]`: "A compactor
MUST refuse to compact when any check `[R-WRT-09]` obliges fails, and MUST NOT
emit a file carrying a violation it has detected". §20.5: "Where the table does
not license a drop the compactor MUST refuse." §20.4: "both registered types
carry PE = 1, so neither can be dropped" and "No commit therefore removes a layer
record, or a user-metadata record at either scope." So a single bit flip in one
user-metadata extent (R2, ignore-record for every reader) or in one stored tile
(T1, reject-tile) makes the whole file permanently uncompactable, and compaction
is "the only operation that reclaims slack".

**Implementer consequence:** the tool refuses; the operator whose verifier just
told them to compact has no in-format remedy and the document never says so. The
escape §20.4 names — "a whole-file rewrite under a fresh file_id" — is expressly
not compaction. Nothing forks: the input keeps the verdict it had, and a refusing
compactor emits nothing at all. Not byte-level. Design-decision: either say it
out loud in §20.5 or Appendix H, or license a disposal.

### G7 `prv01-supersede-is-not-the-only-removal` — writer-05

Verified both halves. §23.1 says superseding is "the only removal of sample data
a commit performs". §20.3 step 4 describes a second and uses a different word for
it in the same passage: "Where a shrink is permitted the **de-addressed** tiles'
extents become slack (`[R-CNT-21]`)" … "Extents this commit **supersedes** become
slack (`[R-CNT-21]`)". §3.1's term list distinguishes stored/addressed and says
only "Superseded payload bytes from earlier generations do not make a tile
stored" — it never defines superseding broadly enough to absorb de-addressing.
§23.2 adds a third shape: "a tile unstored by a later commit leaves its earlier
payload in the file as slack".

The bite is that `[R-PRV-01]`'s MUST NOT is scoped by the same word: "Writers and
the tools built on them MUST NOT represent a commit that supersedes data as
erasure of it." A shrink-as-delete tool reporting "rows 900–1000 deleted" is the
case the rule most needs and, on §20.3's own vocabulary, does not reach.

Not byte-level: `[R-PRV-01]` binds how a tool describes an operation to its user.
No structure is emitted or withheld either way. Design-decision — the maintainer
must decide the scope of a MUST NOT, and I would broaden it to any commit that
makes sample data unreachable.

### G8 `sec20-4-table-scope` — writer-06, adversary-01, diagrams-06

Three reporters, one question: does §20.4's table reach beyond "a type the
updater does not implement", and if so, do the MU = 1 cell's modification
sentences come with it? diagrams-06 comes at it from §2.4's preserve-verbatim
pointer, but that is the same defect seen from the other end — §2.4 sends the
reader to a table whose lead-in excludes both registered types. Merged.

The generalization is stated twice: §20.4's "Persistence governs every record
type; only the authoritative source of the flags differs" and `[R-CNF-06]`'s
"the preservation obligations of §20.4 — which govern every record type, not only
those it does not understand". If the MU = 1 cell's second sentence generalized,
§7.3's registry-fixed MU = 1 on type 0x0001 would bar every layer edit and §20.3
would be dead letter.

**Byte-level? No. Two sentences inside the cell itself decide it:**

> "At layer scope an **unknown** critical record blocks modification of that
> layer" and "`[R-CNT-15]` makes an **unimplemented** top-level MU = 1 record
> reject-file"

— the cell is written about records the updater does not implement, exactly as
its lead-in says, while the retain/drop column is what "Persistence governs every
record type" generalizes. §2.4 confirms the narrow scope of what travels:
"**preserve-verbatim** | Binds updaters: the bytes are carried forward
unmodified". And §20.3's step-by-step permission to modify layers is
unqualified.

I checked adversary-01's residue too — an implemented, unregistered MU = 1 type,
where the cell says "Compaction is barred on the same ground (`[R-WRT-06]`)" and
§20.5 says "a compactor implementing one relocates whatever that registration
defines". `[R-WRT-06]`'s own text bars only "any record whose type it does not
implement with MU = 1", so the cell's cited ground does not reach an implemented
type and §20.5's permission stands unopposed. Determined, at the cost of three
sections.

I also checked the drop question for an implemented unregistered PE = 0 record:
the generalization sentence plus "the definition it implements the type from
supplies the flags" settles it — the MU = 0 / PE = 0 row's drop licence applies.
No fork there either.

Editorial: restate the scope so the cell's first sentence and its remainder are
visibly different in reach.

### G9 `foreign-major-verdict` — verifier-02

Confirmed the collision. §2.3: "a file declaring another major is neither
conforming nor nonconforming under it". §21.2's preamble: "Four rows are outside
that reasoning and **do reach it**, because their subject is a field fixed across
every major (`[R-CNT-24]`): F8 and F1's trailer-magic instance, F14's trailer
CRC … and F6 with F1's front-block instance". If a row reaches such a file the
file exhibits a file-conformance violation, and §2.3's own priority sentence then
fires: "An established violation takes priority: a verifier that has established
any violation reports *nonconforming*."

I could find nothing that reconciles them. Specific-governs-general favours §21.2;
`[R-CNF-02]` is the more fundamental statement. Genuinely open.

**Implementer consequence, both sides concretely:** verifier A prints
*nonconforming*; verifier B prints *cannot establish* naming `[R-CNT-07]`. As
readers both reject-file, on the same two grounds, in the same order. Neither
certifies — §2.3: "a verifier MUST NOT certify a file it reports that way".

Not byte-level: no byte a writer may emit and no acceptance moves; the divergence
is a verdict label. I also tested the reporter's corpus argument and it is weaker
than claimed: F6's instances are "magic bytes [0,8); reserved bytes [8,16)", and
those vectors are naturally built as format-major-1 files, so §24 is not forced
into the foreign-major case. Design-decision: §2.3 needs the carve-out §21.2
already wrote.

### G10 `partial-slack-enumeration-boundary` — verifier-03

The scenario is right — a directory whose terminal CRC fails after the trailer
validated leaves a total owed (§5.2's "no F and no live state to walk" exemption
does not apply) and `[R-ENC-10]` blocks every field the failed CRC covers.

**Byte-level? No. And the text answers the enumeration question by a parallel it
states outright, in §9.7:**

> "an entry `[R-IDX-03]` classifies reject-tile on a *structural* ground
> contributes no stored extent to the walk; **one whose stored bytes alone fail
> its crc keeps its extent**."

A claimant whose covering checksum failed keeps its claim; only structural
invalidity removes it. §9.7 also separates reaching from checking — the walk
"reaches the claimants `[R-CNT-02]` names: the directory itself, each record's
extent…" and then "checks … that each verifies against the checksum covering it".
Both point to the reporter's reading (i), 387, not 496. Add to that `[R-CNT-21]`'s
own "It is not the file's slack total but a bound on it", and the file's status
(F20, nonconforming) is identical under either figure.

Editorial: §5.2 should state the boundary rather than leave it to §9.7's
tile-entry parallel.

### G11 `sec21-6-cites-wrt08-for-a-rule-it-does-not-state` — diagrams-02

Confirmed by reading both. §21.6's experimental-MU = 0 row: behaviour "Ignored,
and preserved or dropped per its PE bit", rule cell "`[R-CNT-15]`, `[R-WRT-08]`".
`[R-WRT-08]`'s sentence is entirely about not re-encoding and not modifying
except by relocation; it says nothing about dropping or about PE. The rule that
does state it is §20.4's table block, which carries no identifier of its own —
`[R-WRT-05]` terminates the paragraph above it and `[R-WRT-08]` a separate
paragraph below. §22.3 uses `[R-WRT-08]` narrowly ("bars re-encoding it"),
which is evidence the label does not stretch over the table.

Not byte-level: §21.1 makes the rule govern over any §21.6 entry too ("where such
an entry and the rule it cites diverge, the rule governs there too"), and the
obligations in §20.4's table are the same words binding the same actors under
either label. Register-bookkeeping: repoint the citation, and mint an identifier
for the table block (which §2.2's "Normative requirements carry identifiers" and
`[R-VEC-02]`'s permanence argument both want).

### G12 `r5-r6-governing-rule-attribution` — diagrams-03

Checked R6 against R10. Both come from one bullet of `[R-MTA-04]`: "every key
satisfying §4.6's name rules — non-empty, at most 255 bytes, free of U+0000
through U+001F". R6's cell reads `[R-CNT-25]` (R-ENC-12); R10's reads
`[R-MTA-04]` (R-ENC-12). §21.1 says the cell "names that requirement first" —
"the requirement that defines it" — and `[R-CNT-25]` is what assigns the
ignore-record outcome to all ten rows, an outcome the subsection heading already
carries. So R6 is misattributed.

One correction to the reporter: R5 is defensible where he calls it wrong, because
`[R-CNT-25]` names its subject expressly — "content violating the document's own
rules (**ill-formed UTF-8 included**, `[R-ENC-11]`)". R6's subject is not named
there.

Not byte-level: both rules agree on ignore-record and are satisfied by the same
reader behaviour. Register-bookkeeping — it matters only to `[R-VEC-02]`'s
manifest identifier, which is exactly the thing §24 says must survive
renumbering.

### G13 `r7-condition-omits-the-bom-alternative` — diagrams-04, register-02

Same defect from two angles: R7's Instances cell enumerates six across three
alternatives, its Condition cell states two. §21.1 licenses an instance to name
"one of several alternatives the condition text states", and "leading U+FEFF" is
not one the Condition states. §18.2's bullet does state it: "The top-level value
is an object, and the encoding carries no byte-order mark: a leading U+FEFF makes
the document unreadable."

Not byte-level. §21.1: "where a row and the rule it cites diverge, the rule
governs", and `[R-MTA-04]` is unambiguous, so every reader takes ignore-record
and every verifier reports nonconforming for a BOM-led document. Register-
bookkeeping, and the arithmetic is safe either way: repairing the Condition to
three alternatives × two containers reproduces the cell's existing six, so §21.8's
273 does not move.

### G14 `sec20-3-note-narrows-the-reemission-trigger` — diagrams-05

Confirmed. Step 4: "Every layer whose stored-tile set **or index content** this
commit changes has its tile-index region re-emitted in full". The Note: "any
change to a layer's stored-tile set re-emits that layer's whole tile-index
region", then reasons about editing one sample — which supersedes a tile, changing
every entry field but not the set of stored ordinals. §5.1's caption states it in
full, so the Note is an isolated stale restatement.

Not byte-level, and the deciding text is `[R-CNF-01]`: "All text in this document
is normative except: §1 (Introduction); **any text labeled *Note*, *Example*, or
*Rationale***". Step 4's own words are normative and complete, and the Note's
arithmetic conclusion is correct under them. Editorial.

### G15 `sec21-1-carries-no-identifier` — register-04

Verified: neither §21.1 paragraph terminates in an identifier, the parenthetical
`[R-ERR-02]` belongs to §21.8, and §21.7/§21.9 carry `[R-ERR-01]` and
`[R-ERR-03]`–`[R-ERR-05]`. §21.1 states two normative rules — completeness, and
rule-over-row precedence — against §2.2's "Normative requirements carry
identifiers … Identifiers are stable".

Not byte-level: the rules are in force as normative text under `[R-CNF-01]`
regardless, and every citation of them resolves by section number today.
Design-decision, because minting an identifier is permanent (§2.2) and someone
has to choose whether "How to read the register" is requirement-bearing — a
position §21.1's own bolded "**completeness is normative**" makes hard to duck.

### G16 `compactor-version-minor-has-no-modal` — quiz-01 — **UPHELD BYTE-LEVEL**

The one I am flagging, so here is the whole chain.

The clause, in §20.5's `[R-WRT-06]` paragraph:

> "The output trailer copies the input's unknown ignore-lane flag bits forward
> (`[R-CNT-08]`) and **carries** the greater of `[R-CNT-26]`'s floor and the
> input's version_minor — a compactor cannot know which minor version defined an
> ignore-lane bit it does not implement, so it does not lower the floor beneath
> one."

Bare declarative. The cited rule is SHOULD-level in full:

> "A writer SHOULD emit the lowest version_minor that defines every feature
> present in the file — for a file expressible under this text, 0 — and an
> appender the maximum of that floor and the prior trailer's minor" `[R-CNT-26]`

The same paragraph is dense with explicit MUSTs on the same actor — "A compactor
MUST refuse to compact when any check `[R-WRT-09]` obliges fails", "MUST NOT emit
a file carrying a violation it has detected", "It MUST mint a fresh file_id" —
so the absence of one here reads as contrast; §2.1's Note ("every requirement
names the actor it binds") points the same way, and this clause's actor is "the
output trailer". Against that: §2.1 makes the clause normative text, the first
half of the same sentence is unquestionably binding (`[R-CNT-08]` backs it with
"MUST NOT clear them"), and the trailing rationale reads like a rule's rationale.

I searched for anything that decides it — `grep -n version_minor` over the whole
file gives §4.7, §6.2's table, §6.3 (`[R-CNT-07]`, `[R-CNT-26]`), §20.3 step 6,
§20.5, §21.6, Appendix A's byte table, Appendix G items 8 and the closing
paragraph. Nothing resolves the modality. §20.3 step 6 goes the *other* way for
the neighbouring actor — "version_minor per `[R-CNT-26]`", i.e. the appender's
identical max(floor, prior minor) construction is explicitly SHOULD-governed —
and Appendix G's closing paragraph calls the whole subject "`version_minor` at
its floor, which `[R-CNT-26]` states as a SHOULD". Appendix H's updater checklist
does not mention the field at all.

**Why I did not downgrade it.** The sharpest case is not even the reporter's.
Take an input with version_minor = 3 and **no** set ignore-lane bit, whose
content is fully expressible under this text.

- Reading (1), mandatory: the output carries max(0, 3) = 3.
- Reading (2), advisory gloss on `[R-CNT-26]`: `[R-CNT-26]`'s own floor for the
  output is 0, and its own consequence clause says a higher minor "misstates the
  file's feature floor to tooling" — so a compactor optimising for that advice
  writes 0.

Here §20.5's max and `[R-CNT-26]`'s floor point in **opposite** directions, and
§20.5's rationale ("a compactor cannot know which minor version defined an
ignore-lane bit it does not implement") does not cover the case, because there is
no unknown bit. Two compactors, same input, same operation: trailer bytes
[10, 12) are `03 00` against `00 00` and the trailer CRC at [60, 64) differs with
them. Both authors read the whole document; both believe the other is wrong.

What I concede, and it is what a downgrade would be built on: both outputs are
conforming files. §6.2 admits any version_minor; `[R-CNT-07]`: "A reader MUST NOT
reject a file for its version_minor"; §4.7 makes it the format's sole descriptive
field. So no reader's decoding, no verifier's verdict, and no acceptance moves,
and no verifier could ever detect the deviation, having no access to the input.

I judged that insufficient. Under refinement (A) the test is what a conforming
implementation may emit *for this operation*, and that set differs. Under
refinement (B) a conduct rule still determines bytes, and — unlike G4 — nothing
here places these bytes outside every requirement: version_minor is a live-state,
CRC-covered trailer field with a stated purpose (communicating the feature floor
to tooling), and §2.3's list of expressly-not-a-file-violation writer obligations
names "§6.3's flags = 0 against a set ignore-lane bit and §6.2's pre-trailer gap"
and **not** this. If I am wrong, the way to show it is to produce the sentence
that fixes the modality; I could not find one, and I looked at all nine
occurrences of the field name.

Repair is a one-word edit and a maintainer's choice of which word: either "MUST
carry the greater of …", or "SHOULD carry …, on `[R-CNT-26]`'s terms". Fixing it
also settles the version_minor half of G5.

### G17 `dead-cannot-establish-ground` — quiz-02

Confirmed by chasing it back. §2.3 lists "when it cannot execute a codec or
filter (`[R-COD-11]`)" among the cannot-establish grounds. §17.3 makes both
filters core; §17.2 does the same for all four codecs; `[R-CNF-03]`: "software
that declines to support a core codec, a core filter … is not a conforming
reader"; §2.3: "Verifiers and updaters are readers of the files they process".
§17.4 closes it: "For a conforming reader that position arises only at a reserved
or experimental value, every assigned codec and filter being core: it rejects the
layer (`[R-COD-03]`, `[R-COD-09]`)" — and that is a violation (L43, L45), so the
verdict is *nonconforming*, not *cannot establish*. The other three grounds
(foreign major, unimplemented MU = 1 type, declined user-metadata decode under
`[R-MTA-09]`) are all reachable.

Not byte-level: an enumeration member with no instance changes nothing any
implementation does; the resource-decline ground is listed separately and remains
live. Editorial at most — §17.4 already says this without drawing the conclusion,
and a Note in §2.3 would save the next reader the chase.

---

## Tally

byte-level: 1 (G16). design-decision: 8 (G3, G4, G5, G6, G7, G9, G15, and — no,
7: G3, G4, G5, G6, G7, G9, G15). editorial: 6 (G1, G2, G8, G10, G14, G17).
register-bookkeeping: 3 (G11, G12, G13). Total 17 groups, 26 ids.
