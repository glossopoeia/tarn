# Cleanroom round 29 — triage pass, Skeptic lens — working transcript

## Disclosure of what I read

Read, in full or in the ranges named:

- `/Users/robertkleffner/Documents/GitHub/tarn-first-draft/spec/tarn.md` — front matter
  (lines 1–120), §2.3–§2.5 (151–340), §4.1 (433–443), §4.2 (443–500), §4.7 (584–620),
  §6.1–§6.4 (756–932), §7.2–§7.4 (964–1180), §9.5–§9.7 (1369–1445), §10 (1491–1580),
  §11 (1584–1720), §12.3 (1797–1830), §14 (1922–2120), §15.1–§15.2 (2122–2200),
  §16 (2245–2350), §17.2–§17.4 (2371–2576), §18.2 (2576–2760), §19.2–§19.4 (2886–3035),
  §20.3 (3076–3345), §20.5 (3404–3546), §21.1–§21.9 (3546–4020), Appendix G and
  Appendix H (4479–4700). Plus targeted greps (`P·Q`, `sample stride`, section headers).

Did **not** read: any other triage pass's notes; the walk transcripts in the r29 `out/`
directory (I opened none of them, and ran no directory listing anywhere under
`/private/tmp/claude-501/...`); `docs/`, `PLAN.md`, `AGENTS.md`, `conformance/`,
`spec/registry.json`, git history, the web. No accidental opens to report.

Ran: `wc`, `grep -n`, `sed -n` over the spec only. No writes to the repo.

Coverage: 34 input ids, 28 groups, every id in exactly one group. Counted by hand
against the id list in the brief and re-counted per reporter prefix
(reader 5 + writer 7 + verifier 4 + diagrams 4 + register 6 + adversary 5 + quiz 3 = 34).

---

## Method

Skeptic default: for each finding, hunt for the sentence that forecloses it. Where I
found one, I quote it and downgrade. Where I searched and found none, I say so and
grade the finding up. One finding survived every kill attempt at byte level:
**adversary-01**.

---

## The one I could not kill: adversary-01 (P·Q in a planar layer)

The claim: `[R-SER-02]`'s designation sentence is unqualified, so a verifier may be
obliged to form P·Q for a **planar** layer and reject it under L2 when P·Q > 2⁶³ − 1,
while another verifier, reading the table as layout-keyed, certifies the same bytes.

### Kill attempts (all failed)

1. **The table is layout-keyed.** §14.2's table rows read
   `| planar, numeric channel c | P · Bᶜ | k · Bᶜ |` and `| interleaved | P · Q | … |`.
   Strong for reading (b) — but the designation sentence that follows is
   *"These products and sums are declaration-derived quantities under `[R-ENC-04]`."*
   It carries no layout qualifier, and §21.1 says "where a row and the rule it cites
   diverge, **the rule governs**".
2. **`[R-SER-07]`'s "whichever".** *"Whichever of §14.2 or §14.3 defines a tile's decoded
   size … Every decoded size, and the value count V, is a declaration-derived quantity."*
   This designates *decoded sizes*, per tile, which for a planar float64 layer is P·Bᶜ.
   It does not say anything about P·Q not being designated; `[R-SER-02]`'s own sentence
   is a separate designation.
3. **§19.3's checklist.** *"the 2⁶³ − 1 ceiling on every quantity that arithmetic derives
   (`[R-ENC-04]`) and on the decoded sizes §14 derives from it (`[R-SER-02]`,
   `[R-SER-07]`)"*. The second limb is layout-keyed in effect; the first limb is
   designation-keyed and routes straight back to `[R-SER-02]`. Circular; settles nothing.
4. **`[R-ENC-04]`'s escape clause.** *"an expression this specification writes only inside
   a comparison, and names nowhere, is not a designated quantity and no reader is obliged
   to form it."* Does not apply: P·Q is named in a table cell, not written only inside a
   comparison.
5. **The register's own layout keying.** L44, T3, T14, T21, T22 all write
   "interleaved P·Q; planar numeric P·Bᶜ; packed planar bool ⌈P/8⌉". L2 alone writes
   "P·Q (which dominates V = P·C); P·Bᶜ" with **no** layout labels — the one place in the
   document where P·Q appears unkeyed. That is evidence for (a), not against it.
6. **§17.2's Note after `[R-COD-07]`** — and this is the sentence that finished the kill
   attempt off: *"`[R-ENC-04]`'s overflow rule carries no such quantifier — it binds every
   quantity it designates, whether or not the layer addresses a tile — **so P·Q and P·Bᶜ
   are checked in an empty layer** even though this cap is not."* Read with a single layer
   as its subject, that sentence says both quantities are formed for one layer, which is
   exactly reading (a). It is a *Note* (non-normative under `[R-CNF-01]`), and it can be
   read distributively across layouts — but nothing in the document contradicts the
   single-layer reading, and I could not find a sentence that does.

### The premise my *non*-downgrade rests on, stated for attack

That the attack file is conforming under reading (b) in every other respect. I
re-derived it: rank 1, E=1, T=2⁵⁹ → G=1, N=1, P=2⁵⁹; C=2 float64 → Q=16, Bᶜ=8;
N·P = 2⁵⁹; C·N = 2 = entry_count; extent_length = 2·20 + ⌈2/2¹⁶⌉·4 = 44; P·Bᶜ = 2⁶².
All in domain. Both entries sentinel, so no `[R-SER-05]`, `[R-COD-04]`, `[R-CNT-20]`
obligation bites. A=S=A_slab=0. Codec 1, filter 1 — no `[R-COD-07]` cap. P·Q = 2⁶³,
over by one.

Two loose ends I checked and did not find fatal:

- The tile's decoded size (2⁶² bytes) massively exceeds §21.9's 256 MiB row. But
  `[R-ERR-03]` says the table states **minimum guarantees, not caps**, and `[R-ERR-04]`
  says *"A file exceeding any of these remains conforming, and a reader MAY decline it"*.
  A verifier that declines reports *cannot establish*, not *conforming* — so the fork
  needs a verifier that does not decline. That is a permitted verifier. The fork stands.
- I checked whether a smaller witness exists that stays inside §21.9's guarantees.
  It does not: P·Bᶜ ≤ 2²⁸ with P·Q > 2⁶³ − 1 would need C > 2³⁵, and C ≤ 65,535. So
  every witness is a giant-tile file. That makes the fork exotic; it does not make it
  unreachable, and `[R-CNF-03]`'s acceptance duty is not what decides conformance.

**Verdict: byte-level.** Under (a) the named byte sequence is nonconforming
(L2, reject-layer at layer access) and `[R-CNF-05]` bars a conforming writer from
emitting it; under (b) it is conforming and a reader must accept it. Opposite
accept/reject on one named file, and the emittable set moves with it.

**Repair (needs a maintainer decision, not just an edit):** decide whether the
designation is layout-keyed, then say so in `[R-SER-02]`. If layout-keyed, add the
qualifier ("for the layout the row above names") and align §17.2's Note. If not, say
that expressly and key L2's instance cell the way L44/T3/T14/T21/T22 already are — and
check whether P·Bᶜ is then designated for interleaved layers too, which the same
sentence would make it.

---

## Groups I tried hardest to kill and succeeded

### reader-03 — the `[R-CNT-26]` floor "has no witness"

The reporter argues that on an ordinary compacted output (flags = 0, no unrecognized
`tarn.` key) version_minor ≠ 0 "sits in the trailer's own bytes at F − 54. That is a
witness in the output alone."

That conflates byte-visibility with §21.7's technical term. §21.7 defines the term
against **obliged checks**, not against visibility:

> "A condition this specification names is **unwitnessed** where, for every file
> exhibiting it, some file that does not exhibit it cannot be told apart from it **by any
> check this specification obliges a reader or a verifier to perform**."

And there is no obliged check over version_minor at all:

> `[R-CNT-07]`: "A reader MUST NOT reject a file for its version_minor: minor releases
> are additive-only, and all feature gating is structural."

> §21.6: "version_minor is higher than this text defines | Accepted; minors never gate"

> `[R-CNF-12]`: "A verifier owes no search for one … a SHOULD deviation is reported where
> the verifier observes it and not hunted for."

So no obliged check separates a file at version_minor 0 from the same file at
version_minor 7, and §20.5's sentence is correct in the sense §21.7 gives the word.
**REFUTED.** Severity: none.

### quiz-03 — durability barriers

Decided in the first sentence of `[R-CNF-02]`'s bullet:

> §2.3: "File conformance is a pure predicate on bytes: it does not depend on any reader,
> writer, or environment."

and by the operative clause of the conduct sentence itself:

> "conduct rules bind the actor, the predicate binds the bytes."

Two byte-identical files cannot differ in conformance, so the barrier-less commit's
output is conforming whatever the enumeration does or does not list. And §21.7's
taxonomy is not owed a placement, because §21.1's register and §21.7's test are stated
over "**file-conformance violation**"s and a conduct-rule breach is not one. Reporter's
practical residue (an implementer wants a stated home) is real but small. **PARTIAL.**

### writer-02 — resource decline scope

`[R-ERR-04]` names its own scope list, and it includes the tile:

> "at the whole file, or at the narrowest scope whose declarations exceed what it can
> serve, **a layer or a tile**."

and §2.3 repeats it:

> "when it declines a layer's or a tile's decode on resource grounds (`[R-ERR-04]`,
> `[R-SER-05]`)"

So reading (b) — under which `[R-COD-06]`'s tile-scope decline is unlicensed — is
foreclosed by the rule's own enumeration. §18.2's whole-file result follows from the
same enumeration without needing the "declarations" premise: a user-metadata document is
neither a layer nor a tile. **PARTIAL** (the word "declarations" is doing loose work; no
fork). Editorial.

### writer-01 — compaction regeneration trigger

Foreclosed twice in §20.5:

> "Given a conforming input the output is a conforming file."

> "The output's reference arrays MUST equal the live generation's bit for bit
> (`[R-MDL-02]`): compaction changes where bytes live, never what a layer denotes."

A compactor that left a region in place while relocating its tiles would emit entries
pointing at other structures' bytes — the entry crc (T1) fails, or the coverage partition
(F7/F33) breaks. Both sentences bar it. **PARTIAL** (wording, no fork). Editorial.

### writer-07 — `[R-SLB-04]`'s trigger

The trigger really is under-inclusive as observed. But the harm is foreclosed by the
file-level invariant, which is unconditional on how the declaration got there:

> `[R-SLB-03]`: "When declared, for every run: the run's stored tiles are contiguous and
> packed in ordinal order … and the first stored tile's offset satisfies
> offset mod A_slab = 0."

plus `[R-CNF-05]` ("A writer MUST emit only conforming files") and `[R-CNF-06]`. So an
updater cannot author a declaration its frozen tiles do not satisfy; the resulting file
is L41/L42. **PARTIAL.** Repair is still worth making (broaden the trigger).

### reader-04 — "This is precisely where the §14 bar has no witness"

The antecedent is genuinely loose. But the harm the reporter names under reading (a) —
"a verifier concludes that a still-stored tile damaged by a shrink is unregistrable and
does not look for it" — is foreclosed by the independent verifier duty:

> `[R-SER-05]`: "A conforming reader never returns this content (`[R-GEO-04]`) and is not
> obligated to check it; **a verifier MUST check it**, and a violation is a validity error
> at tile scope."

and T4/T5 carry rows regardless. Note also that the *bar's own* condition is unwitnessed
under either reading (the reporter's own "further wrinkle", and adversary-05 agrees) —
what is witnessed in the reader's case (a) is `[R-SER-05]`'s condition, a different one.
**PARTIAL.** Editorial.

### quiz-01 — "the bound above"

Decided outside §18.2, by two texts the reporter also cites:

> §21.5 intro: "except where a reader or verifier declines the decode **on the size bound
> or on the frame's declared window**, which `[R-MTA-09]` makes that actor's capability
> and not a fact about the file."

> §2.3 `[R-CNF-11]`: "when it declines to decode a user-metadata document
> (`[R-MTA-09]`)" — unqualified as to ground.

Reading 1 is foreclosed. **PARTIAL** (one-word clarification in §18.2 is still the right
repair). Not byte-level: the file is conforming under both readings and the reader
outcome is ignore-record either way.

### quiz-02 — "last" zero grid count

The immediately preceding clause fixes the contrast:

> §11.1 Rationale: "Growth that leaves **entry_count** unchanged touches the directory
> alone — a growth raising one grid count ⌈Eᵢ / Tᵢ⌉ (§11.2) while another stays 0 among
> them, the product holding at 0."

Reading 1 (last-*declared*) would make the "included" clause describe the case the
previous sentence has just placed on the other side of the contrast, which the sentence
structure forbids. Also inside a *Rationale* blockquote, non-normative under
`[R-CNF-01]`, and the passage defers ("§20.3 states normatively, and governs"). **PARTIAL.**

### reader-02 — growth over a stored edge tile

The §14 bar's list is expressly not the test:

> §20.3 step 4: "The test is the effect on such a tile, and **the list names where that
> effect arises rather than standing on its own**"

and growth carries its own express permission with its own stated reason in the same
numbered step:

> "an extent MAY **grow**, since a position that becomes real held, for each channel the
> position carries, that channel's fill (§14.5), and fill is a legal sample value …
> a growth is permitted exactly where the geometry it produces satisfies every rule that
> geometry is subject to."

§11.1's Rationale says the same. Reading (i) is foreclosed. **REFUTED** as a live
ambiguity; the underlying weakness (the em-dash list reads closed) is real and is what
verifier-03 and adversary-05 attack at other list items. Severity: editorial.

### diagrams-02 / diagrams-03 — the front-matter blockquote

Both are real. diagrams-02: the gloss says "whether **the file** is accepted" where
`[R-ENC-16]` says "anything a conforming reader **or verifier** does … whether the file,
**layer or tile** is accepted at all". The gloss would reclassify the tile-index entry
crc as descriptive; that is foreclosed twice —

> `[R-ENC-16]`: "In format major 1 `version_minor` is the only descriptive field, and
> every other field this specification defines is structural."

> §15.1's entry table: "| 16 | 4 | u32 | crc | structural | …"

so no implementation forks; the gloss is what is wrong. diagrams-03: `[R-CNF-01]`'s list
is closed by its own "except:" and the block is not §1, not a labelled
Note/Example/Rationale, and not an appendix. I looked for a foreclosing sentence and
found none — the nearest thing is a *reductio* the document does not state: read
literally, the Status paragraph and the licence line above §1 are normative too, which
nobody intends. Both **CONFIRMED**, editorial.

### register-03 — `[R-ENC-06]` widths vs §19.3's checklist

§21.7 supplies its own argument and it is sound:

> "`[R-ENC-06]`'s fixed field widths are not a state a file can be in — the parse is
> always at the widths this specification fixes, and a structure written at any other
> yields different values at them, caught by the rows for the fields that hold them."

So §19.3's list item is a parsing convention, and there is nothing statable to check.
`[R-CNF-04]`'s bar on inferring values the specification does not define blocks the one
way an implementer could turn this into behaviour. **PARTIAL** (§19.3's phrasing invites
the wrong reading; the reporter's own note that "caught by the rows" overstates is fair).
Editorial.

### register-05 — F18's cross-major gloss

§21.2 states the operative argument in the same breath as the gloss:

> "F18 is not an exception but a case **outside the premise**: version_major = 0 declares
> no major at all"

and `[R-CNF-13]`'s premise is "a file declaring a format major other than 1". So the
cross-major flourish is not load-bearing; `[R-CNT-07]` decides every file. **PARTIAL**,
editorial. `[R-CNT-24]` does indeed fix only the *position* of version_major, so the
reporter is right that the gloss is ungrounded — but nothing turns on it.

---

## The §21.7 cluster

Nine findings attack §21.7. I split them into four defects by repair:

**(A) Quantifier scope in the detectable clause** — writer-05, verifier-01, adversary-03.
The unwitnessed clause fixes ∀f ∃g ∀check. The detectable clause's English
("separated by such a check from every file that does not") admits ∃f ∃k ∀g as readily as
∃f ∀g ∃k, and only the latter is the negation. §21.1's restatement carries the same
ambiguity in commas. I searched for a disambiguating sentence and found only the duality
*assertion* itself — which is the thing in question, not evidence for a parse.
**CONFIRMED.** Also inside this group: writer-05's second point, that "separated" must
mean "some individual check's result differs" and not "different verdicts", which the
document nowhere says. Same repair site.

**(B) The complement class** — adversary-02. The formal definition quantifies over
"every file that does not [exhibit it]"; the gloss three sentences later quantifies over
conforming files: *"ask whether a breach can be made to leave behind a file no obliged
check separates from **a conforming one**."* The two differ, and I confirmed the direction
matters by working T13: pair a history-window deflate stream with a differently-malformed
one of the same length; both fail T25 identically, and the second does not exhibit T13, so
under the formal definition T13 is unwitnessed — while under the gloss it is detectable,
because every *conforming* file passes T25. **CONFIRMED.** Note the gloss also swaps the
outer quantifier ("can be made to leave behind" is existential where the definition is
universal over exhibiting files), which the finding does not name but the repair must fix.

**(C) "Exactly where" vs F1** — verifier-02, register-01. I tried to kill this by making
`[R-ENC-02]` an obliged check. It is not one: its text is

> "a reader encountering what appears to be a byte-swapped signature (§6) MUST treat the
> file as invalid (reject-file), never as a foreign-endian file to be adapted"

— a constraint on the *response* to an encounter, satisfied vacuously by a reader that
never recognises the swap. The obliged check over those bytes is `[R-CNT-04]`'s byte
equality, which fails identically on a byte-reversed block and an all-zero block. So F1
is unwitnessed under §21.7's own definition while the register carries it and §21.1 names
it as a specialization. **CONFIRMED.** Repair is a maintainer decision: weaken the
biconditional to the forward direction §21.1 already states, or fix the complement class
per (B) — under "a conforming one" F1 becomes detectable and the biconditional survives,
which is the cheaper of the two and fixes (C) and adversary-02's five rows at once.

**(D) Cause-rows vs declined rows** — adversary-04. §21.4's T13/T15/T16/T23/T26 take a
row while saying in their own Condition cells that "the check that detects it is T25's"
(etc.); §16.2, §7.4 and §9.5 decline rows on materially the same ground:

> §16.2: "Because this rule's detection *is* `[R-SLB-03]`'s, a stale declaration carries
> no register row of its own"

> §7.4: "in format major 1 it has no reader-detectable witness, and so no register row"

> §9.5: "Residue past a completed commit carries no register row of its own."

That inconsistency is independent of (B) — even under the "conforming file" complement,
a stale slab declaration is detectable and would owe a row. **CONFIRMED**, register-
bookkeeping (it moves §21.8's 120/275 and §24's corpus, not a verdict).

### Why none of (A)–(D) is byte-level

The premise, stated for attack: **a reader's and verifier's obligations flow from the
governing rules, and the presence or absence of a row never displaces them.** The text:

> §21.1: "each row *restates* its governing rule, and where a row and the rule it cites
> diverge, **the rule governs**."

> §21.1: "a *detectable* file-conformance violation this specification names and the
> register omits is **a defect in this document**" — not a licence.

> §21.7: "Being unwitnessed bears on detection and not on permission: the requirement
> binds its actor as any other does."

I then checked, row by row, that every disputed row has an independent duty in its rule:
F1 → `[R-CNT-04]`/`[R-CNT-06]` (F6, F8) reject-file; F35 → `[R-CNT-15]` states the reader
duty in its own words ("An unknown record type at file scope: MU = 1 → reject-file");
T13/T15/T16/T23 → `[R-COD-08]`'s "a reader MUST treat a malformed stream and either
inexactness as a validity error at tile scope"; T26 → `[R-COD-10]`'s "a verifier detects
it as a validity error at tile scope"; stale slab → `[R-SLB-03]`'s "A verifier MUST check
these invariants". No disputed row is the sole source of any duty. What moves is §21.8's
counts and §24's corpus attribution under `[R-VEC-02]`.

---

## Remaining singletons

- **reader-01 / register-02** (`[R-CNF-12]`'s "runs to the MUST-level conditions §21
  inventories"). Restrictive vs appositive. The circularity is real, and I could not find
  a sentence resolving the grammar. What kills the *byte* claim is the completeness
  clause: "Its **completeness is normative**". Given it, the two search spaces coincide
  on every conforming-file question, and both reporters' sweeps found no un-rowed
  detectable MUST-level condition. **CONFIRMED**, editorial; repair is a comma or "of
  which".

- **verifier-03** (§14 bar omits pad bits). Verified against §14.3's Note ("Pad bits are
  not padding positions"), `[R-SER-05]`'s two sentences, and the bar's list, whose
  "there" is the padding positions. The list genuinely does not reach pad bits; the
  general clause does; shape (c) confirms intent but is an *Example*. **CONFIRMED**,
  editorial. Not byte-level: the permissive reading yields a file exhibiting T5 in every
  such tile, so `[R-CNF-05]` bars it under both readings, and the general clause bars a
  superset of the list, so the divergence cannot run the other way.

- **adversary-05** (the list says "byte offset of any sample", §3.1 defines *sample* as
  the whole tuple, so an interleaved same-type channel permutation passes every item).
  Verified: §14.1 fixes "value k of the sequence is channel (k mod C)'s value", §14.2
  distinguishes Fᶜ (a value's in-sample offset) from the sample's offset, and the bar
  beside the §14 bar exempts interleaved layers outright. **CONFIRMED**, editorial.
  Downgrade rests on the same sentence as reader-02: "the list names where that effect
  arises rather than standing on its own".

- **writer-03 / diagrams-04** (Appendix G item 5's "elsewhere it changes the stored bytes
  of every tile it touches"). A permutation fixes every constant string; `[R-COD-10]`'s
  map is a permutation; §14.5 forces padding to fill, so all-fill-valued regions are
  common. Falsified by an all-zero float32 plane at s = 4 and by diagrams' uint16
  P = 4 / s = 2 / n = 4 tile. Appendix G "adds no requirement to any actor".
  **CONFIRMED**, figure/editorial.

- **writer-04** (the profile's completeness claim leaves tiling and layout open). Item 2's
  own words: "two files carrying the same arrays can legitimately differ in tiling,
  layout, and codec". Item 1 closes the codec; nothing closes the other two. §11.3's Note
  — "Tile extents are a writer's choice, and this specification imposes none" — makes
  them a writer freedom, not a caller input. The closing paragraph's disclaimer ("Read the
  numbered items as the list; this paragraph names what they are for, not how many there
  are") defends the closing paragraph, not the preamble. I looked for a sentence saying
  tiling and layout are profile inputs and found none. **CONFIRMED**, editorial.

- **writer-06** (recovery tool with no candidate). Two reachable states leave no referent
  for "the candidate it settled on": a physical file under 64 bytes (no 64-aligned o with
  o + 64 ≤ length) and a file all of whose candidates fail whole-file re-verification,
  which the same sentence contemplates. Nothing in §9.6 or §9.4 supplies the report for
  that case. **CONFIRMED**, editorial. Not byte-level: recovery tools are not among
  §2.3's five conformance classes, and "no verdict turns on the probe".

- **verifier-04 / register-06** (§21.1 attributes "the sole resolved byte" to §14.2).
  Verified by reading §14.2 whole: `[R-SER-08]`, its Rationale and its Note carry no
  uniqueness claim. §12.3 `[R-TYP-04]` does: "the one case where a reader resolves a byte
  to a value rather than passing it through arises only in a nonconforming file, and
  `[R-SER-08]` states it." Appendix H (non-normative) carries the phrase.
  **CONFIRMED**, editorial. Clean duplicate pair.

- **diagrams-01** (R8's Instances cell). The row's own text elects the single-family
  treatment: "in any form — a magnitude whose binary64 interpretation overflows (`1e400`)
  and the bare tokens `NaN`, `Infinity` and `-Infinity` **alike**". §21.1's escape ("a row
  whose check ranges over a family without the condition changing shape states that range
  as a single instance") is the clause it is invoking. "Materially different" is left to
  judgement, as the reporter concedes. **PARTIAL**, register-bookkeeping. The corpus
  observation — that `[R-VEC-03]` then owes no bare-token vector for the case `[R-MTA-04]`
  singles out as "some parsers accept regardless" — is worth acting on in §24 even if the
  cell stands.

- **register-04** (`[R-ERR-05]`'s "Two do not"). §7.4's table and §16.1 state
  "a power of two, 512 ≤ A ≤ 2⁶²" and "a power of two, 1 ≤ A_slab ≤ 2⁶²" directly.
  `[R-ENC-03]` reads "every offset, length, extent, and count this specification defines —
  entry counts and slab run lengths included" — it names S, sitting right beside A in the
  same table, and does **not** name A or A_slab; L1's instance cell likewise lists S and
  omits both. That is the strongest evidence, and it points to (a): the 2⁶² ceilings are
  chosen numbers, so "Two do not" undercounts. **CONFIRMED**, register-bookkeeping.
  Not byte-level: an A of 2⁶³ is L39 and an A_slab of 2⁶³ is L29 under either reading.

---

## Byte-level tally

1 group: `planar-pq-designation` (adversary-01). Every other group downgraded with a
quoted deciding sentence, or graded non-byte-level on the register-does-not-create-duty
premise stated above, which I have written out so it can be attacked.
