# Round 8 triage — skeptic pass — working transcript

## What I read

- `/Users/robertkleffner/Documents/GitHub/tarn/spec/tarn.md` in full (all 3842 lines,
  read in six contiguous chunks: 1–400, 400–800, 800–1200, 1200–1600, 1600–2019,
  2019–2439, 2439–2858, 2858–3255, 3255–3654, 3654–3843).
- Directory listing of `scratchpad/round8/` only. I did **not** open any reporter
  transcript: the brief tells me to verify claims against the document rather than
  the reporter's account, and reading their reasoning would contaminate the
  independent check. Every quotation below I pulled from `spec/tarn.md` myself.
- Greps run against `spec/tarn.md` only:
  - `grep -n "updater\|appender\|compactor"` — to hunt for an updater carve-out
    from reader obligations (writer-01). None exists.
  - `grep -n "preserve-verbatim"` — 2 hits, both §2.4 (register-06 confirmed).
  - `grep -c "| verifier |"` — 20 (verifier-05's row count confirmed).
  - `grep -n "top-level"` — to test whether a layer record is a "top-level record"
    (writer-02 / quiz-01).
  - `grep -n "R-ENC-06"` — F5 and L3 only, no T row (register-03 confirmed).
  - heading counts 39 / 50 / 26 / 10 = 125, and §21.8's "125 conditions over 252
    instances".

I did not read `docs/`, `PLAN.md`, `AGENTS.md`, `conformance/`, `spec/registry.json`,
git history, or the web.

## Method

For each finding I first tried to find the sentence that forecloses it. Where I
found one I quote it and downgrade. Where I looked and found nothing, I say so
explicitly and grade the finding up.

---

## Group 1 — F36's "at open" (reader-01, diagrams-04)

Checked F36 (line 3061) against L17/L18 (3089–3090) and T8/T9 (3138–3139).
The Detected cells read `layer access` and `tile use`. §21.1 (3011): "Detection
points name §19.2's reader tiers — open, layer access, tile use, extent use — or
*certification*." So 'open' is a defined term and four of the eight rows F36 cites
are misstated.

Tried to kill it: §19.1 step 4 (2519–2523) applies the extent-slot rules for
**non-layer** top-level records only, so a layer record's slot is not checked at
open; §19.1's closing (2543) says the open "consumes the trailer and directory
only — no extent slot's content, no tile index, no payload". Both confirm the
reporters rather than refute them.

Downgrade quote (byte-level → no): §19.2 [R-RDR-02] — "A reader MAY detect any
violation earlier (`[R-CNF-12]`)" — and §21.1 — "where a row and the rule it cites
diverge, **the rule governs**." Outcomes are identical either way (reject-layer,
reject-tile), and §6.4's note says "nothing here bounds what a reader fetches", so
an over-eager open is not nonconforming, only expensive.

CONFIRMED / register-bookkeeping / not byte-level.

## Group 2 — §9.7's closing sentence (reader-02)

The closing sentence (3248–3250) drops "on a *structural* ground". Two sentences
decide it: §9.7's own opening parenthetical (1228–1231) — "an entry `[R-IDX-03]`
classifies reject-tile on a *structural* ground contributes no stored extent to the
walk; one whose stored bytes alone fail its crc keeps its extent" — and §15.3
(1921–1925) — "An entry whose only defect is that its stored bytes fail its crc is
well-formed … its extent stands and it keeps its place in the *verifier* rows, in
run continuity, and in the coverage walk." The closing sentence cites §15.3 in its
own parenthesis.

No ambiguity survives. PARTIAL (locally under-qualified, not two-valued) /
editorial / not byte-level. Also §5.2's note: "Coverage is checked by verifiers,
never by readers."

## Group 3 — [R-ENC-12] and the quarantine (reader-03)

Hunted for the foreclosure and found it in [R-CNT-25] (839–841): the quarantine
covers "content violating the document's own rules" and is ignore-record
"**notwithstanding the owning-scope mapping of `[R-CNF-08]`**". [R-ENC-12]'s
disputed phrase — "a validity error at the owning scope" — *is* [R-CNF-08]'s
mapping, so [R-CNT-25] overrides it by name. Reinforced three times: [R-MTA-02]
(2297–2299) "the outcome of every failure to read its **document** is
ignore-record whatever the scope"; §18.2's fourth restriction (2387–2394) folds
§4.6's name rules into the document's own rules under a list whose members are
"unreadable — ignore-record"; and rows R6 and R10.

REFUTED / editorial / not byte-level.

## Group 4 — sub-record extents in the coverage walk (reader-04)

The reporter's three cross-references are real but there is a shorter one they did
not cite. §5.2 [R-CNT-02] (584–587) defines the coverage classes as "a structure —
a stored-tile extent, **a record extent (the bytes any record's extent slot
references, whatever the record's type, §7.2)**, the directory, or the trailer",
and defines the live state as what is reachable "through the live directory's
records, extent slots, and tile-index entries". "Any record's … whatever the
record's type" settles it; §7.4 (995) "Sub-records are layer-scope records" closes
the last gap.

REFUTED / editorial / not byte-level (§5.2: "Coverage is checked by verifiers,
never by readers").

## Group 5 — §20.4's MU = 1 row vs [R-CNT-15] (writer-01) — **BYTE-LEVEL**

This is the one I tried hardest to kill and could not.

The chain for reading (i): §2.3 — "Verifiers and updaters are readers of the files
they process and inherit every reader obligation." §20.3 step 2 (2755) — "**Open.**
Perform §19.1's open (`[R-RDR-01]`) — the appender is a reader here." §19.1 step 4
(2519–2521) — the record walk applies "the MUST_UNDERSTAND gate for unknown
top-level types (`[R-CNT-15]`)". [R-CNT-15] (909) — "An unknown record type at
file scope: MU = 1 → reject-file". §2.4 — reject-file means "A reader MUST NOT rely
on any structure in it." §21.6 (3221) — "`[R-CNT-15]` obliges the reader to reject".
So the appender's own mandated step 2 fails, and every later step relies on the
trailer and directory of a file it must not rely on.

§20.4's MU = 1 row (2869) says the opposite for the file-scope half: "at file scope
it blocks any modification of file-scope structure — adding, removing, or
reordering top-level records — while a commit that only changes a layer's own
tiles, index, or record **remains permitted**."

Searches for a carve-out, all negative:
- `grep -n "updater\|appender\|compactor"` over the whole document: no sentence
  exempts an updater from a reader outcome. The one place the document handles the
  analogous case it goes the *other* way — §6.3 (762–765): "an updater encountering
  an unknown incompat-lane bit is a reader first, and therefore rejects the file
  before modifying anything."
- The redundancy argument for reading (ii) — that [R-WRT-06]'s compactor refusal
  would be redundant — is weaker than it looks: [R-WRT-06] says "**any** record
  whose type it does not implement with MU = 1", which reaches layer *sub-records*
  too, and those are reject-*layer* ([R-CNT-18]), not reject-file. So [R-WRT-06]
  does independent work under reading (i).
- The row's layer-scope half is fully coherent under reading (i) — reject-layer
  bars that layer and leaves others editable, exactly as the row says. Only the
  file-scope half is dead. That is a contradiction, not a redundancy.

Byte-level: under (i) a conforming updater given this input emits nothing; under
(ii) it emits a whole new generation. The test asks whether resolution changes
"which byte sequences a conforming implementation may emit" — it does. Both
resulting files are conforming, so nothing downstream corrects the fork, and the
implementer cannot determine whether their own updater is conforming.

CONTRADICTION CONFIRMED / byte-level / repair: either carve updaters out of
[R-CNT-15] in §20.4's row (name it there) or delete the row's file-scope half and
say a file-scope unknown MU = 1 record bars every commit.

## Group 6 — "another top-level record" (writer-02, quiz-01) — **BYTE-LEVEL**

Two reporters, same clause (2871), same two readings, both picked B.

Testing reading A textually: [R-CNT-13] (879–881) — "the layer for a layer record
and for sub-records, the file for **other** top-level records" — the word "other"
establishes that a layer record *is* a top-level record in this document's usage.
§7.3 scopes 0x0001 as "file". Appendix G item 3 orders "Records … by type, and
within type 0x0001 by layer name", treating layer records as directory records.
Where the document means to exclude them it says so: §19.1 step 4 and F3/F4/F28/
F29/F31/F33–F35 all say "**non-layer** top-level record". §20.4's clause is
unqualified, so reading A is the literal one.

Testing reading B: the MU = 1 row of the same table glosses file-scope structural
modification as "adding, removing, or reordering top-level records" and contrasts
it with "a commit that only changes a layer's own tiles, index, or record". Under
A, "the file's layer set" in the drop clause is near-redundant, and a routine tile
supersede licenses destroying application state — which is what the clause's last
sentence ("Dropping the record is not itself such a change") exists to prevent.

I could find no sentence that decides between the literal reading and the
purposive one. The clause governs a MUST-level preservation obligation
([R-CNF-06]) and the two readings emit different directories — different record
count, different dir_length, different terminal CRC, different
committed_file_length — from the same input and the same instruction.

AMBIGUITY CONFIRMED / byte-level / repair (one word): write "another *non-layer*
top-level record" if B is meant, or "another top-level record, a layer record
included" if A is.

## Group 7 — creation at offset 16 (writer-03) — REFUTED

Found the foreclosing sentence in §20.2 [R-WRT-02] (2721–2726), which restates the
creation path in full and never restates "beginning at offset 16":

> "A creator MUST follow `[R-LIF-02]`'s creation path: the front signature block;
> each layer's stored tiles, tile-index region, and any record extents, in any
> order satisfying §5.2's coverage classes … and every declared layout invariant
> … — **placement is otherwise free (`[R-SLB-05]`)**; then the complete directory
> and its CRC; then the barrier, the pad, the generation-1 trailer…"

"Placement is otherwise free" cannot coexist with a mandatory first-structure
offset. Backed by [R-SLB-05] (1990–1993) — "its stored tiles MAY occupy any
non-overlapping byte positions, in any order" — and by §5.2's note (622–630): "a
register row for it would be a row no file could exhibit."

REFUTED / editorial / not byte-level. The reporter's design worry (a streaming
creator with A = 4096) evaporates under reading (ii), which §20.2 states.

## Group 8 — over-long pre-trailer pad (writer-04, verifier-01)

Same site, two consequences. verifier-01's certify/refuse fork is closed outright
by [R-CNT-05] (706–707): "**a longer gap is conforming**, and no conforming commit
produces one." And the writer's obligation is closed outright by [R-LIF-02] step 5:
"append the pad to the next 64-byte boundary". No emit-set fork, no verdict fork.

What survives is writer-04's accounting point, which I could not dismiss:
[R-CNF-07] "Every detectable violation named by this specification is assigned
exactly one **reader outcome**"; §21.1 "Its **completeness is normative**"; §21.7's
second class enumerates [R-LIF-01], [R-LIF-03], [R-GEO-06], [R-SER-01], [R-CNT-13]
and not this. [R-CNF-02]'s general clause — "A writer obligation whose violation
this specification expressly declares not to be a file-conformance violation —
§6.3's flags = 0 against a set ignore-lane bit — binds the actor in the same way" —
reads as a general rule with one named instance, and [R-CNT-05] expressly makes
that declaration, so it does cover the pad. But as a closed enumeration it is
short by one.

CONFIRMED (accounting), verifier-01's fork REFUTED / register-bookkeeping /
not byte-level.

## Group 9 — Appendix G's profile gaps (writer-05)

Appendix G is non-normative and self-disclaiming: "It adds no requirement to any
actor: a writer ignoring it is fully conforming." So not byte-level. The gaps are
real: item 3 fixes order and not extent (nothing in G forbids padding between
structures, and §16 [R-SLB-05] permits it); sub-record order inside a layer record
is unordered by item 3 and meaningless under [R-CNT-14]; and the closing paragraph
cites [R-TYP-06] (fill is *recorded*) rather than [R-TYP-10] (what it defaults to),
which is a SHOULD the profile never promotes. The closing paragraph
("Everything else the profile needs is already mandatory except gap content") is
false as written, because non-gap placement is not mandatory.

CONFIRMED / editorial / not byte-level.

## Group 10 — §20.3 example (c) (verifier-02, diagrams-01)

Confirmed against [R-SER-05] (1832–1841): "at every padding position, a writer MUST
encode, for each channel the position carries, that channel's fill value … Every
pad bit (§14.3) MUST carry the plane's channel's fill bit … a verifier MUST check
it, and a violation is a validity error at tile scope." Row T4 and row T5 register
it, verifier-detected, reject-tile. Conformance is over the live bytes ([R-CNF-02]:
"File conformance is a pure predicate on bytes"), so the live recorded fill and the
carried-forward stored tiles must agree. The example's other two operations
(clearing a slab declaration, renaming a layer) genuinely are directory-only —
[R-SLB-04] expressly offers "clear the declaration" as the alternative.

Not byte-level: §2.1 — "All text in this document is normative except: §1
(Introduction); **any text labeled *Note*, *Example*, or *Rationale***" — and the
block is labelled "> **Example — the three shapes a commit takes.**", so it cannot
license an emission [R-SER-05] forbids.

CONFIRMED / figure / not byte-level. Repair: qualify the fill case ("on a layer
with no padding positions and no pad bits") or drop it from the example.

## Group 11 — §15.3's slack gloss (verifier-03)

The gloss (1920–1921): "none to `[R-LIF-08]`'s coverage walk, whose slack total
therefore includes whatever bytes such an entry nominally addresses."

Enumerated the six *structural* rows of §15.3's table against it:
sentinel-with-crc and half-sentinel → nominal offset 2⁶⁴−1, outside the file;
`offset < 16` → nominal bytes are inside the front block, which §9.7 expressly
claims for the walk; `offset + length > F − 64` → runs into the trailer or past
end of file; `offset` or `length > 2⁶³−1` and overflowing sum → not representable.
Only `length = 0` makes the gloss true, and trivially. So it is false for five of
six shapes.

Decided by §9.7: "Bytes the walk does not reach are slack: the verifier sums them
and reports the total, and their content is not its concern." A set complement
cannot exceed F − claimed.

CONFIRMED / editorial / not byte-level (the slack total is a report figure under
[R-CNT-21], not an accept/reject verdict).

## Group 12 — "unable to check" (verifier-04, adversary-01) — REFUTED as a fork

Both reporters quote [R-CNF-11] and both stop one clause short. The full sentence
(198–202):

> "A verifier MUST report each requirement it was unable to check, naming the
> requirement and the ground, **whichever of the three verdicts it reports; that
> per-requirement report constrains the report and not the verdict**, as
> *unexamined* does below."

"Whichever of the three verdicts it reports" explicitly contemplates a *conforming*
verdict alongside a non-empty unchecked list, and the following clause severs the
report from the verdict. adversary-01's V-B chain ("unable to check → therefore
cannot establish → therefore MUST NOT certify") breaks at the second arrow, and
verifier-04's reductio (certification unreachable, verifier class empty) dissolves
with it.

Second, independent foreclosure: §2.3 defines the verifier as "A reader that
additionally checks every **file-level** requirement". [R-COD-10]'s stride clause
and [R-COD-06]'s undisclosed-dictionary clause are not file-level requirements —
[R-CNF-02]'s first sentence, "File conformance is a pure predicate on bytes: it
does not depend on any reader, writer, or environment", forces that, since
adversary-02's W1 and W2 emit byte-identical files. So there is nothing there for a
verifier to be unable to check.

Third: every MUST-level instantiation of the verdict in the document is a
*capability* ground — §17.4 [R-COD-11] "A verifier that cannot execute a layer's
codec or filter cannot establish that layer's conformance and MUST NOT certify the
file", and §18.2 [R-MTA-09]'s declined metadata decode. Neither reaches a
format-inherent undetectability.

PARTIAL (the verdict-definition sentence reads as a sufficient condition and
invited two independent reporters into the same misreading — worth tightening) /
editorial / **not** byte-level. Note the interlock: repairing group 23
([R-CNF-02]'s enumeration) closes this one completely.

## Group 13 — F9 orphaned from the verifier build sheets (verifier-05, quiz-02)

Verified the construction. F9 is "A structure occupies bytes between the live
directory's end and the live trailer", detector verifier, governing rule
[R-CNT-05]. Such a structure is a live claimant, is disjoint, lies inside
[16, F − 64), and verifies against its own checksum — so it passes all three of
§9.7's stated checks and the walk reports clean. Only §6.2's sentence catches it:
"A verifier MUST treat a structure in that gap as a validity error at file scope,
and counts the rest as slack." Neither §9.7 nor Appendix H's verifier entry names
it.

verifier-05 additionally shows F39 and L26 (reserved-range record *type*,
verifier-detected) are absent from Appendix H, whose "record flag bits" line covers
only the flag rows; the MU = 1 specialisations F38/L25 are reader rows. Confirmed
by counting: `grep -c "| verifier |"` = 20; Appendix H's list reaches F36, L19,
F28, F29, F31, L47, L48, L50, L41, L42, L43, T2, T4, T5, T26, F30, L49 = 17.

verifier-05's third point (T3, T24, T25) I refute: Appendix H's verifier entry
opens "**every reader obligation**, plus the checks readers are exempt from", and
T3/T24/T25 carry detector *reader*, so they are inside "every reader obligation".

Not byte-level: Appendix H is non-normative — "each entry's authority is the
requirement or section cited, never this summary."

CONFIRMED / editorial / not byte-level.

## Group 14 — §7.4's missing taxonomy column (diagrams-02)

Verified: §6.1, §6.2, §7.2, §15.1 and §18.2 layout tables carry a Class column;
§7.4's carries `| Field | Type | Constraint |`. Prose classifies three of its
fields elsewhere (§11.4 linearization "structural", §12 sample type "structural",
§13.1 "The fill value is semantic"); the rest are unclassified. §4.7's promise of
the column is inside a **Note**, hence non-normative under §2.1, but [R-ENC-16]
itself is normative and asserts "Every field this specification defines is
classified".

Not byte-level: [R-ENC-16] attaches behaviour to exactly one class — "A field
classified informative MUST NOT affect how any byte is located or decoded" — and
none of the fifteen is a candidate, each having a normative role in locating or
decoding bytes.

CONFIRMED / editorial / not byte-level.

## Group 15 — Appendix H's writer checklist (diagrams-03, adversary-04, quiz-03)

Three reporters, one defect. [R-CNT-03] is a SHOULD closing "no conformance
requirement rides on slack content either way"; §5.2 repeats "its content is
unconstrained, and no conformance requirement applies to it"; §21.6 registers
"Slack: unconstrained content, no conformance requirement" as a defined
non-violation; Appendix G draws the line explicitly ("which `[R-CNT-03]` only
advises and this profile requires"). Appendix H lists it undifferentiated among
seven MUSTs.

Not byte-level: both writers emit conforming files; §5.2 decides. Appendix H
disclaims itself.

adversary-04 also carries the reader-checklist omission that diagrams-06 files
separately; it is judged in group 16 and the repair there covers it.

CONFIRMED / figure / not byte-level. Repair: mark the item "(SHOULD)".

## Group 16 — Appendix H's reader checklist (diagrams-06)

§2.3 [R-CNF-03] names five capabilities, the fifth being "every user-metadata
encoding §18.2 assigns"; Appendix H lists four. Not byte-level, because §18.2
supplies the entailment: "a conforming reader MUST be able to decode encoding 2,
whose decoder `[R-COD-11]` already requires of it for codec 3", and encoding 1 is
verbatim storage.

CONFIRMED / figure / not byte-level.

## Group 17 — §21.9's limits inventory (diagrams-05, register-05)

Two halves.

*Refuted half* — "§21.9 is the complete inventory". [R-ERR-05]'s own next clause
says hard limits "are stated where the structures forcing them are defined", and
[R-ERR-03] cites [R-CNF-10], whose text is "lives in **this specification**, never
only in an implementation" — not "in §21.9".

*Confirmed half* — [R-ERR-05]'s closing generalization, "Each is a consequence of a
field's width, an external format, or the value domain — never a number chosen
here", is false twice over. §16.1 [R-SLB-01]: "a power of two with 512 ≤ A ≤ 2⁶².
Writers MUST NOT emit any other nonzero value; a reader MUST treat one as a
validity error at layer scope" — a file declaring A = 256 is invalid, so it is a
hard limit by [R-ERR-05]'s own definition, and §16.1's note concedes "512 is the
legacy sector floor", a number chosen here. And the 255-byte cap is attributed to
"a `u8` length prefix", a derivation that does not hold for user-metadata keys,
which are JSON strings; §18.2's fourth restriction imposes the cap on them anyway
and R10 registers it. diagrams-05's further examples (the 128-byte floor, dir_offset
≥ 16, dir_length ≥ 4) are weaker — the floor is derived in §5.1 and is a floor, not
a cap.

Not byte-level: §7.4's constraint column, §16.1, §16.2 and row L40 fix the values a
reader rejects.

CONFIRMED / editorial / not byte-level.

## Group 18 — F21 (register-01, adversary-03)

The document contradicts itself by name. §21.2's heading: "File-scope violations."
§21.1: "each row is one malformed condition". §21.6 (3226–3228): "the first is
registered as F21, **whose condition records only the reader's outcome and not a
defect in the bytes**."

Consequences I verified: [R-VEC-04] (3523–3524) asserts "every vector built from
§21's register is nonconforming", which F21 falsifies, §21.6 saying such a file
"can be perfectly conforming under that major"; and [R-VEC-02] requires each
manifest to record "whether the file is **conforming**", a boolean this text does
not fix for F21's vector.

Not byte-level: [R-CNT-07] — "A reader MUST reject-file when version_major is 0
(invalid) or is a major it does not implement" — reserves "invalid" for 0 and
obliges every reader to reject either way; §2.3 names this exact case as a
cannot-establish ground; §21.1's tie-breaker sends one to the rule.

CONFIRMED / register-bookkeeping / not byte-level. Note the count consequence: if
F21 moves to §21.6, §21.2 goes 39 → 38, the register 125 → 124, instances 252 → 251.

## Group 19 — L24's Detected cell (register-02)

L24's first instance is the leading fixed fields, "name … C". §19.1 step 4
(2531–2535): "a layer record whose name field does not lie entirely within that
record's inline_length yields no name field to compare, so it contributes no name
to the namespace and is instead a validity error at layer scope (`[R-CNT-18]`)" —
inside the open. §19.2's open tier lists "the layer-name namespace (§19.1's steps)".
The register already agrees for the neighbouring name rows: L4, L6 and L7 all carry
Detected = `open`. L24 carries `layer access`.

Not byte-level: outcome is reject-layer either way and §19.2 licenses earlier
detection outright ("A reader MAY detect any violation earlier").

CONFIRMED / register-bookkeeping / not byte-level.

## Group 20 — no tile-scope cause row for [R-ENC-06] (register-03)

`grep -n "R-ENC-06"` in the register returns F5 (file scope) and L3 (layer scope)
only. §15.1: "the owning scope of an individual entry, and of the stored tile it
addresses, is the tile", and its 20-byte entry has three fixed-width fields, so
[R-ENC-06] names a tile-scope condition. Detectability is the same class F5 and L3
concede of themselves ("detectable only through the values the fixed-width parse
then reads at the shifted offsets"). §21.1's completeness is normative.

Not byte-level: every instance is already caught with the right outcome by T1, T8,
T9, T11 or T12.

CONFIRMED / register-bookkeeping / not byte-level. Count consequence: §21.4 26 → 27,
register 125 → 126, instances 252 → 253.

## Group 21 — L2's collapsed containers (register-04)

Tried to kill it with §21.1's own competing principle: "a row whose check ranges
over a family without the condition changing shape states that range as a single
instance (T24's *any codec*)". The overflowing-sum predicate does not change shape
between a layer record's slot and a sub-record's slot, so L2's single instance is
defensible under that clause. But §21.1 also says an instance names "a container it
can occur in" and "One instance is one *distinguishable* file", and L1, L16, L17
and L18 all split the same two containers — L17 and L18 split *only* on that axis.
So the register applies two of its own principles inconsistently. The reporter's
opposite-direction examples (T3 enumerating six from one equality; L42 reading "—"
despite three stated alternatives) are part of the same finding.

Not byte-level: [R-ERR-02]'s "one vector per instance" drives corpus construction,
not file validity.

CONFIRMED (as a non-uniformity) / register-bookkeeping / not byte-level. Which way
to fix is a maintainer's call, and it collides with group 20's +1.

## Group 22 — preserve-verbatim (register-06)

`grep -n "preserve-verbatim"` returns exactly two hits, both in §2.4 (the
definition and the table row). §20.4 carries the substance in prose without ever
binding the term.

Not byte-level: §20.4's table and [R-WRT-05] fully determine what an updater
carries forward.

CONFIRMED / editorial / not byte-level.

## Group 23 — [R-CNF-02]'s conduct enumeration (adversary-02)

The conclusion the reporter reaches is forced by the document, in the same
requirement's first sentence: [R-CNF-02] — "File conformance is a pure predicate on
bytes: it does not depend on any reader, writer, or environment." Two byte-identical
files must get the same answer, so a stride the bytes cannot witness cannot bear on
the predicate, and [R-COD-10]'s stride clause and [R-COD-06]'s undisclosed-dictionary
clause are conduct rules. §21.7's first paragraph already treats them that way,
naming both by identifier and assimilating them to "simply wrong data".

What is defective is only the enumeration that follows: "A few obligations this
specification places on writers govern their *conduct* rather than their output —
where a value is published, or which registry version a writer targets (§10.3,
§18.3)". Neither §17.2's nor §17.3's clause is about where a value is published or
which registry version is targeted, and neither appears in the "expressly declares
not to be a file-conformance violation" clause either (nothing expressly declares
them conforming).

Not byte-level: no reader, writer or verifier behaves differently on account of the
enumeration; adversary-01's downstream fork is closed independently (group 12).

CONFIRMED / editorial / not byte-level. Repair: replace the enumeration with the
general rule the reporter drafts — "a writer obligation with no witness in the
emitted bytes binds the actor, not the predicate" — which also subsumes group 8's
pad case.

---

## Which groups I tried hardest to kill and failed

1. **Group 5 (writer-01).** Greped the whole document for an updater carve-out from
   reader outcomes. There is none, and §6.3's parallel case goes the other way
   ("is a reader first, and therefore rejects the file before modifying anything").
   The redundancy defence for the other reading collapses once you notice
   [R-WRT-06] reaches sub-records. Flagged byte-level.
2. **Group 6 (writer-02 / quiz-01).** Established from [R-CNT-13]'s "other
   top-level records" that the literal reading is A, then could not find anything
   foreclosing B, which the same table's MU = 1 row and the clause's stated purpose
   both support. Two independent reporters chose B against the literal text.
   Flagged byte-level.
3. **Group 8 (writer-04).** Tried to make [R-CNF-02]'s general clause absorb the
   over-long pad. It probably does, but only if the em-dash is read as
   illustrative rather than identifying, and §21.7's second class names five
   obligations and not this one.

## Groups where the search paid off (downgrades with the sentence)

- Group 7: §20.2's "placement is otherwise free" — the reporter did not look at
  §20.2 at all.
- Group 12: [R-CNF-11]'s "that per-requirement report constrains the report and not
  the verdict" — both reporters quoted the sentence and stopped one clause short.
  This is the only self-flagged byte-level finding I downgraded.
- Group 3: [R-CNT-25]'s "notwithstanding the owning-scope mapping of `[R-CNF-08]`".
- Group 4: §5.2's "any record's extent slot … whatever the record's type".

## Coverage

33 input ids; 23 groups; union of member_ids = the input list exactly, no
duplicates. Counted twice by hand and by tally per reporter
(reader 4, writer 5, verifier 5, diagrams 6, register 6, adversary 4, quiz 3 = 33).

Byte-level groups: 2 (groups 5 and 6), both inside §20.4's persistence table.
