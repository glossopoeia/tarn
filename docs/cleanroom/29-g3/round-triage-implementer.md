# Triage pass — implementer consequence — cleanroom round 29

## What I read

Only `/Users/robertkleffner/Documents/GitHub/tarn-first-draft/spec/tarn.md`, via
`wc`, `grep`, and `sed -n` ranges. Sections opened in full or in part:

- front matter (lines 1–30, incl. the *How to read this document* blockquote)
- §2 Conformance (2.1–2.5), §3.1 Terms
- §4 Encoding Conventions (4.1–4.7)
- §6.3 Version and flag gates, §6.4
- §7.4's nesting Note (lines 1155–1180)
- §9.5, §9.6
- §11.1, §11.2, §11.3
- §12.3
- §14 (14.1–14.5)
- §15.1, §15.2
- §16.2
- §17.2 (codec 3 / `[R-COD-06]`), §17.3, §17.4 (head)
- §18.1, §18.2, §18.3 (head)
- §19.2, §19.3, §19.4
- §20.3, §20.4, §20.5
- §21 in full (21.1–21.9)
- Appendix G in full

I did **not** open any walk transcript, any other triage pass's notes, `docs/`,
`PLAN.md`, `AGENTS.md`, `conformance/`, `spec/registry.json`, git history, or the
web. I did **not** list `/private/tmp/.../r29-round/out/` or any directory under
it — I never referenced that path at all. The one `mkdir -p` I ran was on my own
output directory.

Nothing in the input was left unevaluated. All 34 ids are grouped.

---

## Grouping

26 groups. Reasoning for the non-obvious merges and splits:

**Merged — `sole-resolved-byte-misattribution` (verifier-04, register-06).**
Identical defect, identical repair. Checked: `grep -n "sole resolved"` returns
exactly two hits, line 3630 (§21.1) and line 4649 (Appendix H). §12.3
`[R-TYP-04]` carries the uniqueness claim ("the one case where a reader resolves
a byte to a value rather than passing it through arises only in a nonconforming
file, and `[R-SER-08]` states it"). §14.2 does not.

**Merged — `shuffle-identity-universal-false` (writer-03, diagrams-04).**
Same sentence, same falsifying class (any decoded image the permutation fixes).
I verified both arithmetics. At s=2, n=2 the permutation is the transposition of
offsets 1 and 2, so `01 02 02 03` is fixed and `01 02 03 04` → `01 03 02 04`.
diagrams-04's interleaved uint16 tile: P=4, Q=2, L=8, n=4, permutation
non-trivial, an all-`01` image is fixed. Both correct.

**Merged — `detectability-quantifier-scope` (writer-05, verifier-01,
adversary-03).** One sentence, one repair (a word before "such a check"). All
three give the same two parses; verifier-01 and register-01 both test F35, but
verifier-01's *headline* is the parse and register-01's is F1, so register-01
goes elsewhere.

**Merged — `detectability-test-does-not-match-register` (verifier-02,
register-01, adversary-04, adversary-02).** One defect seen from four angles:
§21.7's `exactly where` biconditional is false of §21 as it stands. F1
(verifier-02, register-01) and T13/T15/T16/T23/T26 (adversary-04) are rows the
formal definition calls unwitnessed; adversary-02 supplies the mechanism —
§21.7 states its test twice, once over "every file that does not" (line 3886–3890)
and once over "a conforming one" (line 3901–3903), and the two complement classes
disagree in *both* directions (the second grants rows to undisclosed-dictionary
and stale-slab, which §18.2 and §16.2 expressly deny). A maintainer cannot repair
one half without deciding the other, so one group. Noted in `notes` that a
maintainer may want two edits.

**Split — the three §14-bar list defects (reader-02, verifier-03,
adversary-05).** Same paragraph, three different, separately-repairable gaps:
the list *over*-reaches on growth (padding positions), *under*-reaches on pad
bits, and *mis-names* the quantity (sample offset, not value offset). Three
edits, three groups.

**Split — diagrams-02 / diagrams-03.** Same blockquote, different defects: the
gloss's content vs `[R-ENC-16]`, and the blockquote's self-declared
non-normativity vs `[R-CNF-01]`'s closed exception list. Different repairs.

**Split — reader-05 / quiz-03.** Both concern the seam between §21.7's two
absence-grounds, but reader-05 is about §20.3/§20.5's labels and quiz-03 is about
`[R-CNF-02]`'s conduct taxonomy for §9.2's barriers. Repairing one does not
repair the other.

---

## The one self-flagged byte-level finding: adversary-01

This is the only finding a reporter flagged byte-level, and the only one where a
verdict fork was constructed on a named file. I spent most of my time here.

The claim: `[R-SER-02]`'s closing sentence ("These products and sums are
declaration-derived quantities under `[R-ENC-04]`") is unqualified, so P·Q is a
designated quantity of a *planar* layer too, and a 256-byte planar file with
P = 2^59 and Q = 16 has P·Q = 2^63, one above the domain. Verifier A rejects the
layer (L2); verifier B certifies.

I re-derived the file's arithmetic and it holds: rank 1, E = 1, T = 2^59, so
G = 1, N = 1, P = 2^59; two float64 channels, so C·N = 2, P·Bᶜ = 2^62,
entry_count = 2, index extent_length = 2·20 + ⌈2/2^16⌉·4 = 44. Every designated
planar quantity is in domain. Only P·Q overflows.

**Why I nonetheless downgrade.** §14.2 does not state two independent quantities;
it states two *quantities* — "the decoded size" and "the offset of value k" —
whose formulas are selected by a column literally headed **Layout**:

> | Layout | Decoded size | Offset of value k |
> |---|---|---|
> | planar, numeric channel c | P · Bᶜ | k · Bᶜ |
> | interleaved | P · Q | (k div C) · Q + F_{k mod C} |

The two rows are mutually exclusive alternatives: they define the *same*
quantity ("Offset of value k") for the same k, and no layer can have both. So
they cannot both be applicable to one layer, and the designating sentence that
follows designates each expression where its row applies. `[R-SER-07]` says so
directly for the size limb — "**Whichever** of §14.2 or §14.3 defines **a
tile's** decoded size" — a tile has one decoded size, not two.

§11.2 `[R-GEO-03]` is the same construction, and settles the reading independently
of §14.2 (this is the premise-test the round-16 warning asks for, since it does
not come from adversary-01's example):

> The layer's **addressed-tile count** — the number of its tile-index entries
> (§15) — is N for an interleaved layer and C · N for a planar layer … These
> products are declaration-derived quantities under `[R-ENC-04]`.

Under adversary-01's reading (a), C·N is designated for an *interleaved* layer
too, and an interleaved layer with N = 2^58, C = 64 would be reject-layer for a
count of tile-index entries it does not have (entry_count·20 = 5.76e18 stays in
domain, so nothing else catches it). Reading (a) therefore forks §11.2 the same
way it forks §14.2 — and §11.2 names one quantity with two layout formulas in a
single sentence, which no one would read as designating both for every layer.
That is the reading that governs §14.2's table as well.

`[R-ENC-04]`'s own limiting clause points the same way: "an expression this
specification writes only inside a comparison, and **names nowhere**, is not a
designated quantity and no reader is obliged to form it." In a planar layer P·Q
names nothing — it is not that layer's decoded size, not a tile length, not an
ordinal. §17.3 confirms the layout keying for Q itself: "The shuffle stride s is
the channel's element size for a planar tile and the sample stride Q for an
**interleaved tile**".

Two supporting (not decisive) observations. First, reading (a) is not coherently
implementable: it would equally oblige a planar layer's reader to form
`(k div C)·Q + F_{k mod C}` as "the offset of value k", contradicting the same
table's planar `k · Bᶜ` for the same k. Second, the disputed file declares a
per-tile decoded size of 2^62 bytes, ten orders of magnitude above §21.9's
256 MiB guarantee, so `[R-ERR-04]` lets *both* verifiers decline the layer
outright; the fork is only reachable between two implementations that both chose
to evaluate a layer far outside the acceptance floor.

**Premise of the downgrade, stated for attack:** I assume §14.2's table states
*one* decoded size and *one* value-offset per tile, with layout selecting the
formula, rather than two expressions each of which every layer possesses. If a
maintainer reads the designating sentence as designating the *expressions*
rather than the *quantities*, adversary-01's fork is real and byte-level, and my
whole downgrade fails. The cheap insurance is one clause on `[R-SER-02]` — "each
row's quantities are those of a layer of that layout" — which I recommend
regardless, because it costs nothing and it is the only place in this round where
a byte-level finding could still land.

---

## Per-group notes and the quotation behind each downgrade

### reader-01 + register-02 — `[R-CNF-12]`'s "runs to the MUST-level conditions §21 inventories"
Real ambiguity (restrictive vs appositive). Not byte-level: the fork requires a
file exhibiting a **detectable, un-rowed, MUST-level file-conformance violation**,
and §21.1 makes the non-existence of one normative —

> Its **completeness is normative** — a *detectable* file-conformance violation
> this specification names and the register omits is a defect in this document

so under both readings the verifier's search space is the same 120 conditions on
every file the document contemplates; where it is not, the repair is to add the
row, not to pick a reading. Both reporters swept and named no such condition; I
did not find one either (the candidates — the §14 bar, `[R-SLB-04]`'s stale
declaration, §7.4's nesting — are each expressly unwitnessed or commit-relative).

### reader-02 — growth vs the §14 bar's "set of padding positions"
The tension on the face of the list is real. But the reporter's claim that the
growth direction is "nowhere in the carve-out" is wrong: the growth paragraph
*is* the carve-out for that direction and states the same reason —

> and an extent MAY **grow**, since a position that becomes real held, for each
> channel the position carries, that channel's fill (§14.5), and fill is a legal
> sample value

together with "the list names where that effect arises rather than standing on
its own". PARTIAL. Not byte-level: the produced file is conforming under both
readings; only the route to it changes.

### reader-03 — "Neither obligation has a witness in the output alone"
REFUTED. The reporter reads "witness" as "observable in the bytes"; §21.7 defines
it over *obliged checks*:

> A condition this specification names is **unwitnessed** where, for every file
> exhibiting it, some file that does not exhibit it cannot be told apart from it
> by any check **this specification obliges a reader or a verifier to perform**.

`[R-CNT-26]` is a SHOULD, and `[R-CNF-12]` says "A verifier owes no search for
one … a SHOULD deviation is reported where the verifier observes it and not
hunted for", so no obliged check has version_minor's value in its failure set.
Take f (minor = 1, no later-minor feature) and g (minor = 0, otherwise
identical, trailer CRC recomputed): every obliged check returns the same result
on both, including F14's CRC comparison. §20.5's sentence is true as written.

### reader-04 — "This is precisely where the §14 bar has no witness"
CONFIRMED: under the sequential reading (the paragraph's declared subject is a
shrink) the claim is false, because a shrink that turns real positions into
padding positions of a tile the new state still stores leaves a T4 violation in
the live state — I checked the geometry (E: 8→5, T = 4; grid count stays 2; the
high tile keeps position 4 real and 5–7 become padding, whose stored bytes are
not fill). Not byte-level: a verifier's duty to look is stated unconditionally by
the governing rule, not by §20.3's prose —

> A conforming reader never returns this content (`[R-GEO-04]`) and is not
> obligated to check it; **a verifier MUST check it**, and a violation is a
> validity error at tile scope. `[R-SER-05]`

— and §21.1 adds "where a row and the rule it cites diverge, the rule governs".

### reader-05 — §21.7's two grounds
PARTIAL. Right for the §14 bar's unwitnessed cases and for §20.5's
output-≥-input obligation (no file exhibits either). Wrong for the `[R-CNT-26]`
floor, which *is* a file condition with no obliged check — ground 1 is apt there.
§21.7 also forecloses whole-requirement classification: "A single requirement
states conditions of both kinds where it states several, and is classified as a
whole by neither." Not byte-level: both grounds keep a condition out of the
register.

### writer-01 — compaction's regeneration trigger
CONFIRMED and reachable (a compactor that reorders tiles into disk-ordinal order
can leave a region's byte offset unchanged while the tiles it names move). Not
byte-level: the literal reading's output is nonconforming (T1 on every re-pointed
entry) and is barred by `[R-CNF-05]`/`[R-CNF-06]` either way. Decided by §20.5's
own text — "Given a conforming input the output is a conforming file" and "The
output's reference arrays MUST equal the live generation's bit for bit
(`[R-MDL-02]`)" — plus the next paragraph's definition, "Regenerating a region
means classifying every entry in it: … every other entry is re-pointed to where
its stored extent now lies", which is the operation the trigger should be keyed
to.

### writer-02 — `[R-ERR-04]`'s "declarations"
PARTIAL. The word is loose, but nothing conflicts: `[R-COD-06]` states the
tile-scope decline expressly — "a wider window is conforming and merely permits a
conforming reader to decline **the tile or the layer** on resource grounds
(`[R-ERR-04]`)" — and `[R-ERR-04]` itself offers "a layer or a tile" as the
narrow scopes. Not byte-level: "A file exceeding any of these remains
conforming", and the whole-file decline is available under every reading, so no
file moves between must-accept and may-reject.

### writer-03 + diagrams-04 — Appendix G item 5
CONFIRMED, non-normative. "It adds no requirement to any actor: a writer
ignoring it is fully conforming."

### writer-04 — Appendix G's completeness claim
CONFIRMED. §11.3's Note ("Tile extents are a writer's choice, and this
specification imposes none") and §14.1/§7.4's free layout field leave two of
item 2's own three named freedoms open. The closing paragraph's disclaimer
("Read the numbered items as the list; this paragraph names what they are for,
not how many there are") covers the inventory paragraph but not the preamble's
"closes the degrees of freedom this format deliberately leaves open".
Non-normative, so not byte-level.

### writer-05 + verifier-01 + adversary-03 — the detectable clause's quantifiers
CONFIRMED. The English is ∃f ∃k ∀g; the asserted duality requires ∃f ∀g ∃k. Not
byte-level: which parse wins decides only whether a condition owes a row, and
§21.1 keeps the governing rule's detection duty in force regardless — "each row
*restates* its governing rule, and where a row and the rule it cites diverge, the
rule governs". Reader duty under `[R-CNF-04]` runs to rows that exist under both
parses (F35's row exists either way).

### writer-06 — recovery with no surviving candidate
CONFIRMED; both states are reachable (a 16-byte file, and a file all of whose
candidates fail re-verification). Not byte-level: §9.6 says "no verdict turns on
the probe", and recovery tools are not one of §2.3's five conformance classes.

### writer-07 — `[R-SLB-04]`'s trigger
CONFIRMED (the trigger names only stored-tile-set / run-partition / placement
changes "of a slab-declared layer", so authoring or re-aligning a declaration is
outside it). Not byte-level: `[R-SLB-03]` binds the new generation regardless —
"When declared, for every run: the run's stored tiles are contiguous and packed
in ordinal order … A verifier MUST check these invariants (violation:
reject-layer)" — so the resulting file is L41/L42-nonconforming under both
readings and `[R-CNF-05]` bars emitting it.

### verifier-02 + register-01 + adversary-04 + adversary-02 — the biconditional
CONFIRMED. I re-ran the F1 construction (byte-reversed trailer magic vs
eight zero bytes, each with its CRC recomputed): both fail `[R-CNT-06]`'s magic
check identically, so no obliged check separates them and F1 is unwitnessed under
the formal definition while carrying a row. `[R-ENC-02]` obliges a *response*
("a reader encountering what appears to be a byte-swapped signature … MUST treat
the file as invalid"), not a search, so it supplies no separating check. Same
shape for T13/T15/T16/T23/T26, whose own Condition cells say the detecting check
is another row's. Not byte-level: the governing rules ( `[R-CNT-04]`,
`[R-CNT-06]`, `[R-COD-08]`, `[R-SER-05]`, `[R-SER-08]`) reject the same files at
the same scopes whichever way the register is repaired, and §21.1's "the rule
governs" makes a row's presence or absence non-dispositive for any reader. What
moves is `[R-VEC-02]` attribution and §21.8's counts.

### verifier-03 — pad bits absent from the §14 bar's list
CONFIRMED. I checked each of the other four list items against a bool-fill change
in a layer with no padding positions and P mod 8 ≠ 0: decoded size ⌈P/8⌉
unchanged, every value's offset unchanged, sample type unchanged, codec and
filter unchanged. Only the general clause reaches it. Not byte-level: the file
the permissive reading produces violates `[R-SER-05]`'s pad-bit sentence and is
T5 at tile scope, so `[R-CNF-05]` bars it under both readings — and shape (c)'s
"no padding position and **no pad bit**" shows the intent even though it is an
*Example*.

### verifier-04 + register-06 — "the sole resolved byte"
CONFIRMED, editorial. Verified by whole-file grep (two hits, neither in §14.2).

### diagrams-01 — R8's Instances cell
CONFIRMED, register bookkeeping. §21.1's criterion is "materially different
shapes", applied by the document to pairs *less* different than these (T15's zlib
vs gzip wrappers). The corpus consequence is concrete: `[R-VEC-03]` obliges one
vector per named instance, R8 names no bare-token instance, and §21.1's
specialization clause attaches "at a given instance of it, where the row
enumerates several" — so the bare-token case, which R7 also catches, gets no
obliged vector. Not byte-level: both alternatives are `[R-MTA-04]` violations
with the same ignore-record outcome either way. The maintainer decision is
enumerate-4 (total 277) or state why "alike" makes them one family.

### diagrams-02 — the front-matter gloss narrows `[R-ENC-16]`
CONFIRMED (the gloss drops "or verifier" and "layer or tile"). Not byte-level;
the taxonomy is decided field-by-field by a single sentence no gloss can move:

> In format major 1 `version_minor` is the only descriptive field, and every
> other field this specification defines is structural. `[R-ENC-16]`

plus §15.1's entry table cell (`| 16 | 4 | u32 | crc | structural |`) and
§19.4 step 5's "verify the entry's crc over the stored bytes before decoding
(`[R-CNT-20]`)". No implementation can conclude from the gloss that the entry crc
need not be checked without contradicting an explicit MUST.

### diagrams-03 — the front-matter block's normative status
CONFIRMED. `[R-CNF-01]`'s exception list is closed and introduced by "except:";
the block is not §1, is not labeled *Note*/*Example*/*Rationale*, and is not an
appendix. Not byte-level for the reason above.

### register-03 — `[R-ENC-06]` in §19.3 vs §21.7
PARTIAL: no contradiction (§19.3's item is a parse convention alongside a real
`[R-ENC-03]` check), but §21.7's supporting clause does overstate — a structure
written at a wrong width can yield values that pass every rowed check and merely
return wrong samples, which is §21.7's own undetectable-content class, so "caught
by the rows for the fields that hold them" is not guaranteed. Not byte-level:

> `[R-ENC-06]`'s fixed field widths are not a state a file can be in — the parse
> is always at the widths this specification fixes

and `[R-CNF-04]` forbids the one resolution that could fork bytes: "A reader MUST
NOT heuristically repair a violating structure or infer values this specification
does not define."

### register-04 — `[R-ERR-05]`'s "Two do not"
PARTIAL. `[R-ERR-05]` nowhere asserts that A is inside `[R-ENC-03]`'s domain, so
there is no contradiction with L1's instance cell; what is unsafe is the closed
count, since the *power-of-two shape* on A and A_slab follows from no field
width, external format, value domain, or structural arithmetic. Not byte-level:
A = 2^63 is reject-layer at layer access under both readings (L39's "A above
2^62" instance, or L1's domain instance) — same scope, same detector, same tier.

### register-05 — F18's cross-major gloss
CONFIRMED as an overstatement. `[R-CNT-24]` fixes the *position* of version_major
in every major and states nothing about its value; `[R-CNT-07]` is a major-1
rule. The argument §21.2 actually needs does not require the cross-major claim:
version_major = 0 does not meet `[R-CNF-13]`'s premise ("a file declaring a
format major other than 1"), so major 1's rules apply and `[R-CNT-07]` rejects.
Not byte-level: every major-1 reader rejects the file under both readings.

### adversary-05 — sample offset vs value offset
CONFIRMED. §3.1: "**sample** — the tuple of one value per channel at one
coordinate", and §14.2's example ("its sample occupies bytes [15, 18)") uses it
that way, so item 3 of the list names an offset a same-type channel permutation
leaves fixed, while what moves is Fᶜ, a value's offset, which the list never
names. I checked the other four items against the permutation and none catches
it. Not byte-level: `[R-SER-01]` ("value k of the sequence is channel
(k mod C)'s value") makes the general clause reach it, and the resulting file is
conforming in isolation either way — the bar leaves no file witness, so no
verifier verdict moves. It is nonetheless the most consequential of the three
list defects for a real updater, because nothing downstream catches the mistake.

### quiz-01 — "the bound above"
CONFIRMED as a local ambiguity in §18.2; decided elsewhere, in normative text:

> except where a reader or verifier declines the decode **on the size bound or
> on the frame's declared window**, which `[R-MTA-09]` makes that actor's
> capability and not a fact about the file [§21.5]

Not byte-level: the document is conforming under both readings and no reader's
accept/reject of any byte sequence moves; what moves is a verifier's report
between *conforming* and *cannot establish*.

### quiz-02 — "last" zero grid count
CONFIRMED (under last-declared, the sentence is false: raising that dimension's
grid count while another extent is still 0 leaves N = 0 and entry_count = 0, so
it is the previous sentence's directory-only case). Not byte-level: the passage
is inside a blockquote labelled *Rationale*, which `[R-CNF-01]` exempts, and it
defers — "§20.3 states normatively, and governs, what a commit may do to a
layer"; L22 catches an implementer who follows the wrong reading.

### quiz-03 — the durability barriers
PARTIAL. The `[R-CNF-02]` half is refuted by the rule's own first principle —
"File conformance is a pure predicate on bytes: it does not depend on any reader,
writer, or environment" — and by the conduct clause being illustrative ("govern
their *conduct* rather than their output — where a value is published, or which
registry version a writer targets"), not a closed enumeration; a barrier is
paradigmatically conduct-not-output. The §21.7 half is a real but inert
looseness: a barrier states no condition a file can exhibit, which is §21.7's
second class, and §21.7 says of that class "Nothing is omitted from the register
on its account, there being no condition to omit."

---

## Byte-level tally

0 groups byte-level. One reporter flag downgraded (adversary-01), with the
premise stated above for attack.
