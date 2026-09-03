# Cross-hunk consistency audit — r29, six hunks

## 0. Disclosure

Read: `/Users/robertkleffner/Documents/GitHub/tarn-first-draft/spec/tarn.md` (whole file, via
sed ranges and a whitespace-normalised copy), and the six files
`hunk-01.diff` … `hunk-06.diff` in
`/private/tmp/.../r29-driverfull/case/`. I did NOT open `full.diff`, did not
`ls` beyond one `ls -la` of the case directory (which listed full.diff's name and
size; I did not read it), and did not open docs/, PLAN.md, OPEN-QUESTIONS.md,
AGENTS.md, README.md, conformance/, spec/registry.json, or git history.

Working files written, all under my own scratch dir
`/private/tmp/.../r29-driverfull/scratch/cross-hunk/`:
- `flat.txt` — whitespace-normalised single-line copy of tarn.md (285,781 → 283,149 chars),
  built to defeat the hard wrap. All phrase searches ran against this.

Unrequested context that appeared before I began: a project instruction file
(CLAUDE.md pointing at AGENTS.md) and an index of the maintainer's auto-memory
naming several memory documents. I did not open any of them and drew no
conclusion from their contents; they are named here only as disclosure.

## 1. Grouping (by rule touched, not by section)

**Group A — the detectability test and register membership.** Hunks 3 (§21.1)
and 4 (§21.7). Hunk 3 edits §21.1's *report* of a definition; hunk 4 edits the
*definition's* meta-statement and the register-membership rule in §21.7. This is
the definition/report pair.

**Group B — the two grounds for a condition's absence from the register,
applied.** Hunk 1 (§18.2) applies Group A's grounds to two carried-over frame
constraints. Depends on Group A.

**Group C — §20.3 step 4's two bars and their witnesses.** Hunk 2 (§20.3, the
§14 bar's slack consequence) and hunk 6 (§21.7 Rationale, the companion ordinal
bar's witness analysis). Hunk 6's block is the walk-through §20.3 normatively
cites.

**Group D — the Rationale block's own status.** Hunks 5 and 6, the two edits
that land inside `> **Rationale.**`. Under [R-CNF-01] both are non-normative;
the other four are normative (none sits in a block whose first word is *Note*,
*Example* or *Rationale*; hunks 1–4 sit in ordinary paragraph text with no ">"
marker at all).

## 2. Force test applied — by label, not by marker

[R-CNF-01] verbatim: "All text in this document is normative except: §1
(Introduction); any text labeled *Note*, *Example*, or *Rationale*; and
appendices identified as non-normative."

| hunk | lands in | block label | force |
|---|---|---|---|
| 1 | §18.2 body paragraph | none (no ">") | normative |
| 2 | §20.3 numbered step 4 | none | normative |
| 3 | §21.1 body paragraph | none | normative |
| 4 | §21.7 body paragraph | none | normative |
| 5 | §21.7 blockquote, first word **Rationale.** | Rationale | NON-normative |
| 6 | same blockquote | Rationale | NON-normative |

## 3. Per-hunk: the rule the repair adopts

- **H1.** Of §18.2's carried-over [R-COD-06] frame constraints, exactly two are
  outside the register, and for two *different* reasons: undisclosed dictionary
  use is an unwitnessed condition; the buffer-sizing bar states no condition a
  file can exhibit.
- **H2.** A §14-bar-violating re-declaration strands, as slack, the originals of
  every tile the change reaches — not the whole layer's stored tiles.
- **H3.** §21.1's own statement of detectability is the check-based one: a
  condition is detectable iff some file exhibiting it is separated, by an
  obliged reader/verifier check, from every file that does not. (Previously: iff
  some file exhibiting it *differs, in its live state*, from every file that does
  not.)
- **H4.** unwitnessed and detectable are exact negations because their
  quantifiers are duals (not because they "match"); and a register row exists for
  a condition exactly where the condition is a detectable *file-conformance
  violation*.
- **H5.** The §21.7 Rationale walk-through's list is not closed, and both a stale
  item and an omitted obligation are defects in the block rather than in the
  register.
- **H6.** A planar channel permutation is witnessed by T4/T5 only where the fills
  differ *and* the permuted channels carry a padding position or a pad bit;
  otherwise unwitnessed regardless of the fills.

## 4. Check 1 — tense and quantifier

**H2.** Tense: "the generation this commit supersedes" — the prior generation.
Governing normative rule, §20.3 step 4: "A commit MUST NOT change a layer's
declarations in a way that alters, for any tile that layer stores **in the
generation this commit supersedes**, what §14 fixes…". H2's "every tile the
change reaches" sits under "Where a change does reach them", whose "them" is
"a tile that carries that channel" stored in the superseded generation. Tense and
set match. The old "the whole layer's worth" contradicted the carve-out two
sentences earlier ("a planar channel none of whose own tiles are stored, is a
declaration edit like any other"), so the repair is in the right direction.
Matching restatement in the Example block: "it would invalidate every stored tile
it reaches". PASS.

**H3 vs H4 (the definition/report pair), word for word:**

- §21.7 (definition, untouched by H4): "It is **detectable** in the contrary
  case: where some file exhibiting it is separated by such a check from every
  file that does not."
- §21.1 (H3): "a condition is detectable exactly where some file exhibiting it is
  separated, by a check this specification obliges a reader or a verifier to
  perform, from every file that does not"

Identical modulo the expansion of "such a check" (whose antecedent in §21.7 is
"any check this specification obliges a reader or a verifier to perform").
Subject in both: "a condition". Quantifier order in both: ∃(file exhibiting) …
∀(file not exhibiting). PASS on the comparison the pair was made for.

H4's duality claim, checked formally:
- unwitnessed = ∀F∈E ∃G∉E ∀c ¬sep(F,G,c)
- ¬unwitnessed = ∃F∈E ∀G∉E ∃c sep(F,G,c)
- detectable as worded = ∃F∈E ∃c ∀G∉E sep(F,G,c)  ← "by such a check" precedes
  "from every file that does not"

Quantifier-by-quantifier the duals are right (∀↔∃ three times), so H4 correctly
replaces the old, plainly false "with matching quantifiers". But the *check*
quantifier's scope position moves from innermost (unwitnessed) to second
(detectable as worded), and exact negation requires the reversal to be
order-preserving. See finding X-03.

**H6.** Ranges over "the permuted channels". Its normative counterpart, §20.3:
"a commit MUST NOT change the channel declarations in a way that alters the disk
ordinal [R-GEO-06] assigns **any tile the layer stores in the generation this
commit supersedes**". H6 is a witness claim, not a restatement of the bar, so no
quantifier mismatch with the bar; the mismatch is internal (X-01).

## 5. Check 2 — citations resolved, one by one

| citation | in | claim | verdict |
|---|---|---|---|
| `[R-COD-06]` (§18.2, H1) | "dictionary use the header does not disclose … an unwitnessed condition, exactly as [R-COD-06] has it for a tile" | [R-COD-06]: "Dictionary use the header does not disclose is not detectable by inspection and need not decode to an error: it is a writer violation whose consequence is wrong decoded content, the same undetectable class as any other writer that emits wrong bytes (§21)." | **PASS** |
| §21.7 (§18.2, H1, "the two distinct grounds §21.7 separates") | §21.7 separates (a) unwitnessed, (b) "a requirement that states **no condition a file can exhibit**" ([R-ENC-06] example) | both are in §21.7's *normative* paragraphs, not in the Rationale | **PASS** (see rejected candidate RC-2 for a phrasing quibble) |
| R4 (§18.2, H1, "R4 registers neither") | R4's Instances cell enumerates: missing frame magic ×2, skippable frame ×2, second frame ×2, nonzero dictionary ID ×2, content-checksum flag ×2, bytes remaining after the frame ×2, content-size larger ×2, content-size smaller ×2 = 16 instances. Undisclosed dictionary use and the buffer-sizing bar appear nowhere in it. | **PASS** |
| `[R-LIF-01]` (§20.3, H2) | "freezes them where they lie" — [R-LIF-01] is cited across the document for committed-prefix immutability ("[R-LIF-01] freezes the committed prefix", §20.3 elsewhere) | **PASS** |
| `[R-CNF-07]` (§21.1, H3) | "detectability being the gate [R-CNF-07] already applies" — [R-CNF-07]/§2.4: "Every detectable file-conformance violation named by this specification is assigned exactly one **reader outcome**." | **PASS** |
| §21.7 (§21.1, H3) | "§21.7 states the test for" — §21.7 does state it | **PASS** |
| `[R-CNF-07]` (§21.7, H4) | "the gate [R-CNF-07] applies in assigning an outcome" | **PASS** (same text as above) |
| §21.1 (§21.7, H4) | "§21.1's completeness clause" — §21.1: "Its **completeness is normative** — a *detectable* file-conformance violation … and the register omits is a defect in this document" | **PASS** |
| §14.5 (§21.7 Rationale, H6) | "§14.5's padding positions" — §14.5 "Padding content": "at every padding position, a writer MUST encode … that channel's fill value" | **PASS** |
| §14.3 (§21.7 Rationale, H6) | "§14.3's pad bits" — §14.3: "…are the tile's **pad bits**; their content is fixed by [R-SER-05]" | **PASS** |
| T4 (H6) | "A padding position does not encode, for each channel it carries, that channel's recorded fill value"; instances include "planar numeric plane fill bytes; packed planar bool plane fill bit" | **PASS** |
| T5 (H6) | "In a packed planar bool plane with P mod 8 ≠ 0, a final-byte pad bit … is not the channel's fill bit" | **PASS** |
| T3 / T14 (H6, in the untouched clause H6's tail collides with) | T3 "The decoded payload's byte length is not exactly the tile's decoded size derived from the layer's declarations"; T14 "Codec 1 (none) declared and a non-sentinel index entry's length differs from the tile's decoded size" | **PASS as cited — and they are what falsifies H6's tail** |
| "the test above" (H5) | resolves to §21.7's normative "That is the whole of the test…" | **PASS** |

T2 is *not* cited by H6, correctly: T2 is interleaved-only and H6's subject is a
planar layer. (The same block's earlier sentence names "T2, T4 or T5" because it
covers all layouts.)

## 6. Check 3 — where the rule's own words land

Terms grepped in `flat.txt` (whitespace-normalised; hit counts):

```
"detectab"                   → 10 hits, listed and located
"unwitnessed"                → 8 hits
"cannot be told apart"       → 1 hit  (§21.7 definition, normative)
"obliges a reader or a verifier" → 2 hits (§21.1 H3, §21.7 definition) — both normative
"differs, in its live state" → 0 hits  (H3's deletion swept clean)
"live state"                 → 18 hits, all inspected
"carry no witness"           → 0 hits  (H1's deletion swept clean)
"no witness"                 → 3 hits
"told apart"                 → 1 hit
"separated by"               → 2 hits
"no register row"            → 3 hits ([R-CNT-18] Note, [R-LIF-05] Note, [R-SLB-04] Note)
"no row"                     → 1 hit  (§21.1)
"not registered"             → 0 hits
"not offered as closed"      → 3 hits (§21.1, §21.7 Rationale [H5], §23)
"not offered as exhaustive"  → 1 hit  (§20.3)
"not as a closed list"       → 1 hit  (§18.2)
"strand"                     → 5 hits
"whole layer"                → 0 hits  (H2's deletion swept clean)
"disk ordinal"               → 14 hits
"permutation"                → 3 hits
"re-typing"                  → 4 hits
"re-declar"                  → 5 hits
"ignore-lane"                → 14 hits
"copied forward" / "carry forward" / "carried forward" → 1 / 2 / 2
"R-CNT-26"                   → 6 hits
"invalidate every"           → 1 hit  (Example block (c))
```

Findings from the label test:
- H1, H2, H3, H4 all state their rules in unlabeled paragraph text. Each landed.
- H5 and H6 state theirs inside `> **Rationale.**`. Neither has force. For H6
  that is fine (it is a witness walk-through, and the bar itself is normative in
  §20.3). For H5 it is not fine: "is a defect in this block" is the same kind of
  maintenance obligation §21.1 states normatively and marks "**completeness is
  normative**" — H5's has no normative counterpart anywhere. See X-02.
- Two *normative* sentences cite §21.7 for content that exists only inside the
  Rationale block: §20.3's "§21.7 records the consequence — that this is
  precisely where the §14 bar has no witness, the live state being clean — which
  is why the rule is stated here and not left to the rows"; and §20.5's "Neither
  obligation has a witness in the output alone (§21.7)." See X-04.

## 7. Check 4 — contradiction inside the passage, including untouched text

**H6 — CONFIRMED contradiction.** The full sentence chain, in one place:

> "…a permutation among channels whose planes are the same length **and whose
> recorded fills agree** disturbs nothing a row can see, while one that leaves a
> plane of one length at an ordinal the new declarations size differently is
> caught by T3, or by T14 under codec 1. Where the fills differ and the permuted
> channels themselves carry a padding position or a pad bit, §14.5's padding
> positions and §14.3's pad bits carry the wrong channel's fill and T4 or T5 sees
> it; **where neither does, the permutation is unwitnessed whether the fills
> agree or not.**"

The old text carried its equal-length condition on the only clause that claimed
unwitnessedness. H6's new tail claims unwitnessedness under a condition stated
purely in terms of padding, with no length condition, and then explicitly widens
past its own antecedent ("whether the fills agree or not"). Falsifying instance,
built from the document: a planar layer, C = 2, channel `a` `uint8` (Bᵃ = 1),
channel `b` `uint16` (Bᵇ = 2), extents an exact multiple of the tile extents so
no tile carries a padding position, and no bool channel so no plane carries a
pad bit. Exchanging `a` and `b` in the channel declarations moves all of both
channels' disk ordinals (§20.3's own worked example: "exchanging `a` and `b`
moves all four"). Neither permuted channel carries a padding position or a pad
bit, so H6's tail says the permutation is unwitnessed — while the clause 30 words
earlier says a plane "of one length at an ordinal the new declarations size
differently is caught by T3". T3's cell confirms it: "planar numeric P·Bᶜ,
payload longer; planar numeric P·Bᶜ, payload shorter".

**H5 — contradiction inside one inserted clause.** "…its list is not offered as
closed; where an item here and the test above disagree, the test governs, and an
item found stale — or **an obligation the list omits** — is a defect in this
block…". A list that is expressly not closed cannot make its own omissions
defects. Every other non-closure construction in this document pairs
non-closure with a *deciding property* and asserts no defect on omission:
- §21.1: "the property decides any pair and this list is not offered as closed."
- §20.3: "the list is not offered as exhaustive: a growth is permitted exactly
  where the geometry it produces satisfies every rule that geometry is subject to."
- §18.2: "Carried over — named for convenience, not as a closed list —"
- §23: "Those two cases are exhaustive because … the list of operations above is
  not offered as closed."
H5 is the only one that adds defect-on-omission, and it is the only one that
does so inside a labeled block.

The clause also bites: the list demonstrably omits at least two obligations of
exactly the kind it collects. §20.3 step 6 obliges an ordinary appender to emit
"unknown ignore-lane flag bits copied forward (`[R-CNT-08]`), and version_minor
per `[R-CNT-26]`". Both are unwitnessed for precisely the reason the list gives
for §20.5's versions of them: the prior trailer is slack (§21.6: "Bytes the live
state does not claim — … superseded structures"), §9.7 walks the live state only,
and no obliged check compares the new trailer's flags or minor to the old. The
list names only "§20.5's three obligations on a compacted file's trailer".

**H1 — no contradiction found in §18.2.** The paragraphs either side were read
whole. "The first exception holds because a document has no declared size" and
"The frame's declared `Window_Size` is unconstrained here for the same reason"
remain true; the ignore-record-on-window-grounds sentence ("no violation: the
file exceeds a §21.9 guarantee and so remains conforming") is about one of the
two constraints §18.2 *replaces*, not one it carries over, so H1's "Two of those"
does not reach it.

**H2 — no contradiction.** The step's carve-outs ("a change that leaves every one
of those tiles' stored bytes meaning exactly what they meant … is not what this
bars"; "a planar channel none of whose own tiles are stored") are now *supported*
by the repair rather than collided with.

**H3/H4 — no contradiction with the surrounding §21.1/§21.7 text.** In
particular §21.1's "The subsections after §21.5 are not part of the register and
carry no rows: neither this completeness clause nor the instance arithmetic below
reaches … §21.7's test" still holds after H3 inlined the test into §21.1; the
clause is about what the completeness clause *reaches*, not about where the test
is stated.

## 8. Check 5 — exhaustive claims

- H1 "**Two** of those" — verified against the carried-over list (frame magic;
  no skippable frame and no second frame; no dictionary use, disclosed or not,
  and no nonzero dictionary ID; no content-checksum flag; the buffer-sizing bar)
  and against R4's 16 instances. Exactly two are unregistered. **HOLDS.**
- H1 "the **two** distinct grounds §21.7 separates" — §21.7 separates exactly
  two. **HOLDS** as a claim about §21.7 (§21.6 supplies a third ground for
  register absence, but H1 does not attribute the count to the document at
  large). See RC-2.
- H1 "states **no** condition a file can exhibit **at all**" — [R-COD-06]: "a
  reader MUST NOT allocate or size any buffer from it". Binds a reader. §2.3: a
  conforming file is "A byte sequence satisfying every file-level requirement".
  **HOLDS.**
- H2 "**every** tile the change reaches" — matches Example (c)'s "it would
  invalidate every stored tile it reaches". **HOLDS.**
- H3 "**exactly where**" — biconditional over the check-based test. Tested
  against [R-SLB-04]'s and [R-LIF-05]'s "no register row" Notes; both survive
  because staleness / residue are conflated by the obliged checks with plain
  violations, so neither is detectable under the new test. (Both would have
  *failed* under the deleted "differs, in its live state" test — the repair
  rescues them.) **HOLDS.**
- H4 "**exactly where** it is a detectable file-conformance violation" — the
  converse half is not stated in §21.1, which says only "enumerates every
  detectable file-conformance violation this specification names". Weak
  overreach; see RC-1, not raised as a finding.
- H4 "each quantifier is the other's dual, **so each is exactly the negation of
  the other**" — the inference needs quantifier *order* preserved under
  reversal, which the check quantifier's stated position does not give. See X-03.
- H5 "its list is not offered as closed" — this is a *disclaimer* of
  exhaustiveness, and it is the right one; it is the clause bolted onto it that
  fails. See X-02.
- H6 "**T4 or T5**" — correct and complete for a planar layer; T2 is
  interleaved-only. **HOLDS.**
- H6 "unwitnessed **whether the fills agree or not**" — falsified. See X-01.

## 9. Check 6 — what the repair left unconstrained

**H2. Structure governed: the slack accounting of a §14-bar-violating
re-declaration that is nevertheless carried out by re-emitting tiles.** Quantities
the structure carries: (i) the superseded tile payloads; (ii) the layer's
tile-index region; (iii) the directory; (iv) the pad and trailer. H2 pins (i)
precisely — "every tile the change reaches". (ii) is governed but not by this
sentence: §20.3's own Note says "any change to a layer's stored-tile set
re-emits that layer's whole tile-index region, so editing one sample of a
10⁶-tile layer appends about 20 MB of index and leaves as much slack", and
[R-CNT-17] obliges a re-emitted region wherever entry_count changes. The
sentence's conclusion — "leaving the file larger for a change that reads like a
directory edit" — turns on the *total*, and after the repair the total's largest
term for a large layer is the one term the sentence does not name. See X-06.

**H6. Structure governed: a planar layer's per-channel plane.** Quantities it
carries: plane byte length (P·Bᶜ, or ⌈P/8⌉ packed); padding-position fill bytes;
final-byte pad bits; the recorded fill value; the codec/filter the bytes were
produced under. H6 names padding positions, pad bits and fills; it drops plane
length — the very quantity the preceding clause pinned to T3/T14. That is not a
sibling left unconstrained, it is a sibling constrained by the neighbouring
sentence and dropped by this one — which is why it reads as X-01 rather than as a
gap.

**H1. Structure governed: §18.2's carried-over frame-constraint list.** Members:
magic, skippable frame, second frame, dictionary use (disclosed / undisclosed),
dictionary ID, content-checksum flag, buffer-sizing bar. Every member is either
an R4 instance or one of the two H1 places outside. No member left unaccounted.

**H3/H4. Structure governed: the register-membership predicate.** Discriminators
in play: (a) unwitnessed vs detectable; (b) file-conformance violation vs not;
(c) a condition vs "no condition a file can exhibit"; (d) named by this
specification vs not; (e) reaching a file of another format major ([R-CNF-13]).
H4 pins (a) and (b) in one sentence. (c) is pinned by the next paragraph. (d) is
carried by §21.1 ("this specification names") and by §21.7's own subject
sentence, but *not* by H4's biconditional itself. (e) is pinned by [R-CNF-13].
Nothing is orphaned.

## 10. Check 7 — analogies, verb against verb

**H1.** "…is a writer violation nothing in the extent shows — an unwitnessed
condition, **exactly as** `[R-COD-06]` has it for a tile (§21.7)".
- repair's verb: "nothing in the extent **shows**"
- cited rule's verb: "is not **detectable by inspection** and need not **decode**
  to an error"
- §21.7's own gloss of the same rule: "produces a file that every checksum in §8
  **certifies**".
Ranges: the repair speaks of a user-metadata document's extent; [R-COD-06]
speaks of a tile. §21.7 anticipates that transposition and supplies its own
document analogue: "an undisclosed compression dictionary (`[R-COD-06]`, and
`[R-MTA-09]` for a user-metadata document, whose wrong content is the document's
rather than a tile's samples)". The analogy therefore holds *for this member*.
I pressure-tested the one place it could fail: a user-metadata document, unlike a
tile's samples, has content rules a verifier must check (R5–R10), so an
undisclosed dictionary usually produces bytes that fail R7 or R3 — which looks
like a witness. It is not one under §21.7's test, because such a file is not
separated by any obliged check from a file whose document is simply not
well-formed JSON and used no dictionary; the checks conflate them. **PASS, and
the near-miss is worth recording.**

**H1's second half is not an analogy** — it asserts ground (b) directly, no "as"
clause. Nothing to compare.

**H4.** "each quantifier is the other's dual, **so** each is exactly the negation
of the other". This is the analogy-shaped move in this commit, and it carries the
weight for *both* halves of a definition.
- unwitnessed's verbs: "**cannot be told apart** from it by **any** check"
- detectable's verbs: "**is separated by such a check** from **every** file"
Compared member by member: file-exhibiting quantifier ∀ ↔ ∃ (dual, order
reversed — correct); file-not-exhibiting quantifier ∃ ↔ ∀ (dual, order reversed —
correct); check quantifier "any … " under negation ↔ "such a check" (dual, but
its scope position is innermost in one and second in the other — **not**
order-reversing). The analogy is sound for two of the three and unsound for the
third. That is exactly the shape the charter names: one sentence carrying an
analogy for several members, sound for some and not the next. See X-03.

**H6.** "…for the same reason no check knows which ordinal a stored tile used to
occupy" (untouched). Verb: "no check **knows**". H6's inserted claim's verb:
"T4 or T5 **sees** it" / "is **unwitnessed**". The "same reason" is the
prior-generation-is-not-live-state reason, which is a reason *some* permutations
escape, not all — and the untouched T3 clause already says so. The repair did not
disturb this analogy; it disturbed the enumeration it introduces.

**H2, H3, H5.** No "exactly as"/"the same way"/"for the same reason"
constructions in the repaired text. Nothing to compare.

## 11. Check 8 — what the insertions did to their neighbours

Every back-reference from each insertion to the end of its structure:

**H1 (§18.2).**
- "**The first exception** holds because a document has no declared size" — before
  the insertion the nearest preceding pair was "save two: what it states against
  a tile's declared decoded size, and what it states about the frame's declared
  `Window_Size`". H1 inserts a *second* numbered pair between them — "the two
  distinct grounds §21.7 separates" — and it is now the nearest. Resolution
  changed for a first-pass reader; the trailing clause ("because a document has no
  declared size") lets a careful one recover. See X-05.
- "**for the same reason**" (in "The frame's declared `Window_Size` is
  unconstrained here for the same reason") — resolves to "a document has no
  declared size", unchanged by the insertion. **UNAFFECTED.**
- "**both**" in "This section replaces both" — precedes the insertion.
  **UNAFFECTED.**
- H1's own backward reference: "**Two of those**" → the carried-over list.
  **RESOLVES.**

**H2 (§20.3 step 4).**
- "**Such a change** is a new layer, or a whole-file rewrite" — nearest antecedent
  is "a change that reads like a directory edit", which sits *after* the
  insertion point. **UNAFFECTED.**
- H2's own backward reference: "every tile **the change** reaches" → "a change
  [that] does reach them", four words earlier. **RESOLVES.**

**H3 (§21.1).**
- "— but each row *restates* its governing rule, and where a row and the rule
  **it** cites diverge" — "it" = the row. **UNAFFECTED.**
- "subject to **the same exception stated above**" → "[R-CNT-25]'s quarantine".
  H3 inserted no exception. **UNAFFECTED.**
- "neither **this completeness clause** nor the instance arithmetic below reaches
  … §21.7's test" → the clause H3 edited. Still the only completeness clause.
  **UNAFFECTED.**

**H4 (§21.7).**
- "so an unwitnessed condition is absent from it by **that clause's** own terms" →
  "§21.1's completeness clause", named in the preceding clause. H4 inserted no
  competing "clause" noun. **UNAFFECTED.**
- "**That is the whole of the test**" (next paragraph) → the unwitnessed/detectable
  definition. H4 inserted no second test between them. **UNAFFECTED.**

**H5 (§21.7 Rationale).**
- "where an item here and **the test above** disagree" → §21.7's normative test.
  **UNAFFECTED.**
- "**these obligations** are omitted from the register" (next paragraph) →
  "Obligations this test places outside the register", H5's own first words.
  **UNAFFECTED** (H5 dropped only the leading "The").
- H5's own backward reference: "an obligation **the list** omits" → "its list",
  inserted six words earlier. **RESOLVES** — and see X-02 for what it resolves to.

**H6 (§21.7 Rationale).**
- "Where **the change** does touch something §14 fixes, the register's rows reach
  **it**" — before H6 the nearest antecedent was "…T4 or T5 sees it"; now it is
  "the permutation is unwitnessed whether the fills agree or not". Both resolve to
  the same referent (the ordinal-moving re-declaration), so the resolution did not
  change — but the juxtaposition now reads "the permutation is unwitnessed …
  Where the change does touch something §14 fixes, the register's rows reach it",
  which sharpens X-01 rather than creating a new defect. **RESOLUTION UNCHANGED.**

## 12. Direction of each disagreement

- X-01: the **repair** (H6's tail) is the side that should change. The T3/T14
  clause is correct and matches T3's Instances cell.
- X-02: the **repair**'s added defect-on-omission clause should go; the
  non-closure disclaimer it accompanies should stay.
- X-03: the **definition sentence in §21.7** should be reworded ("separated from
  every file that does not by some such check"), and §21.1's H3 copy with it;
  H4's assertion is what the pair should be made to satisfy, not what should go.
- X-04: the **normative citations** in §20.3 and §20.5 are the wrong side to
  leave standing; the statements they rely on should be lifted out of the
  Rationale block, not the citations weakened.
- X-05: the **repair** should name the exceptions, or the following sentence
  should.
- X-06: the **repair** should either name the index region or drop the
  "leaving the file larger" conclusion's reliance on the total.

## 13. Derived numbers

- R4 Instances cell, counted by hand from the cell text: 8 distinct conditions ×
  2 containers (top-level extent; layer sub-record extent) = **16 instances**.
  Compared against §18.2's carried-over list (5 named groups) to establish H1's
  "Two of those … R4 registers neither". The document states no per-row count for
  R4, so there is no published figure to compare against; §21.8's aggregate is
  "120 conditions over 275 instances", which I did not recount.
- H1's "Two of those": counted = 2 (undisclosed dictionary use; the buffer-sizing
  bar). Matches.
- H1's "the two distinct grounds §21.7 separates": counted = 2 in §21.7
  (unwitnessed; states no condition a file can exhibit). Matches.
- H6's "T4 or T5": for a planar layer the applicable content rows are T4
  (padding positions, both the planar-numeric and packed-bool instances) and T5
  (packed-bool pad bits); T2 is interleaved-only. Count = 2. Matches.
- Falsifying-instance arithmetic for X-01: channel `a` `uint8` → plane P·1 bytes;
  channel `b` `uint16` → plane P·2 bytes; P·1 ≠ P·2 for any P ≥ 1, so the
  permutation leaves a P-byte payload at an ordinal the new declarations size at
  2P — T3's "planar numeric P·Bᶜ, payload shorter".

## 14. Findings

### X-01 — hunk 6 (with 5): the unwitnessed tail drops the plane-length condition and collides with the T3 clause beside it
Check: LOCAL_CONTRADICTION. Location: §21.7, `> **Rationale.**` block, the planar
ordinal-permutation sentence. Quotation (repaired text): "where neither does, the
permutation is unwitnessed whether the fills agree or not". Contradicting text
(untouched, 30 words earlier, same sentence chain): "while one that leaves a plane
of one length at an ordinal the new declarations size differently is caught by T3,
or by T14 under codec 1."
The old wording carried "whose planes are the same length" on every clause that
claimed unwitnessedness. H6's replacement states its unwitnessedness condition
purely in terms of padding positions and pad bits and then explicitly widens past
its own "Where the fills differ" antecedent, so it now covers cases the T3 clause
has already disposed of. Instance: planar layer, C = 2, `a` `uint8`, `b` `uint16`,
extents an exact multiple of tile extents (no padding positions), no bool channel
(no pad bits); exchanging `a` and `b` moves every ordinal (§20.3's own example) and
T3 catches it ("planar numeric P·Bᶜ, payload shorter"). Repair: "where neither
does, a permutation among planes of the same length is unwitnessed whether the
fills agree or not." Byte-level: **no** — the block is labeled *Rationale* and so
non-normative under [R-CNF-01]; T3 and §20.3's bar govern regardless, and no
writer's emittable set moves. Hunk 5 is named because its new clause ("an item
found stale … is a defect in this block") is what classifies this.

### X-02 — hunk 5: the list is declared not closed and its omissions declared defects in the same breath, in a block that cannot make either stick
Check: LOCAL_CONTRADICTION (also OVERSHOT and NORMATIVE_PLACEMENT). Location:
§21.7, opening sentence of the `> **Rationale.**` block. Quotation: "This
walk-through illustrates the test and does not extend it, and its list is not
offered as closed; where an item here and the test above disagree, the test
governs, and an item found stale — or an obligation the list omits — is a defect
in this block and not in the register."
Three problems, one edit. (a) A list expressly not closed cannot make its own
omissions defects; the two added clauses cancel. (b) Every other non-closure
construction in the document pairs non-closure with a deciding property and
asserts no defect on omission — §21.1 "the property decides any pair and this list
is not offered as closed"; §20.3 "the list is not offered as exhaustive: a growth
is permitted exactly where…"; §18.2 "named for convenience, not as a closed list";
§23 "the list of operations above is not offered as closed". H5 is the only
departure. (c) "is a defect in this block" is the same species of maintenance
obligation §21.1 states and marks "**completeness is normative**" — but H5's sits
inside a *Rationale*-labeled block and therefore carries no force under
[R-CNF-01], and it has no normative counterpart anywhere. The clause also bites in
fact: §20.3 step 6 obliges an ordinary appender to copy unknown ignore-lane bits
forward ([R-CNT-08]) and to set version_minor per [R-CNT-26]; both are unwitnessed
for exactly the reason the block gives for §20.5's versions of them (the prior
trailer is slack, §9.7 walks the live state only), and the list names only §20.5's
three. Repair: keep "its list is not offered as closed"; delete "or an obligation
the list omits". Byte-level: **no**.

### X-03 — hunks 3 and 4: one repair asserts an exact negation the other's wording does not deliver
Check: NEW_AMBIGUITY. Locations: §21.7 (H4) and §21.1 (H3). Quotation (H4): "The
two are stated over the same subject, and each quantifier is the other's dual, so
each is exactly the negation of the other". Quotation (H3, §21.1): "a condition is
detectable exactly where some file exhibiting it is separated, by a check this
specification obliges a reader or a verifier to perform, from every file that does
not". The definition H4 speaks about: "for every file exhibiting it, some file
that does not exhibit it cannot be told apart from it by **any** check…" /
"…separated **by such a check** from every file that does not."
Formally: unwitnessed = ∀F∃G∀c ¬sep; its negation = ∃F∀G∃c sep; the detectable
clause as worded = ∃F∃c∀G sep, because "by such a check" precedes "from every file
that does not". H4 replaced a plainly false claim ("with matching quantifiers")
with a true one about each quantifier individually, but the inference it draws
("so each is exactly the negation of the other") also needs the reversal to
preserve quantifier *order*, and the check quantifier's stated position breaks
that. H3, editing the same test in the same commit, chose a phrasing that sets the
check off with commas immediately after "separated", which if anything strengthens
the one-fixed-check reading. Consequence: a condition separated from different
non-exhibiting files by different obliged checks — plausible here, where T3, T4,
T5 and T14 each separate different neighbours — is detectable under one reading
and unwitnessed under the other, which decides whether §21.1's completeness clause
owes it a row. Repair: in §21.7 write "separated from every file that does not by
some such check", and mirror it in §21.1. Byte-level: **no** — the test decides
whether a register omission is a document defect; readers' accept/reject
obligations come from the rules and rows as written, which do not move.

### X-04 — hunks 5 and 6: two normative sentences depend on statements that exist only inside a Rationale block
Check: NORMATIVE_PLACEMENT. Locations: §20.3 (normative), §20.5 (normative), and
the §21.7 `> **Rationale.**` block both cite. Quotations: §20.3 — "§21.7 records
the consequence — that this is precisely where the §14 bar has no witness, the
live state being clean — which is why the rule is stated here and not left to the
rows."; §20.5 — "Neither obligation has a witness in the output alone (§21.7)."
The only text in §21.7 recording either is inside the Rationale block: "a commit
that supersedes every tile it would have damaged leaves the live state clean, so
the §14 bar is unwitnessed there for the same reason [R-LIF-01] is" and "§20.5's
three obligations on a compacted file's trailer ([R-WRT-06]) … are unwitnessed for
a reason all three share". Under [R-CNF-01] that block is non-normative, so two
normative sentences — one of which justifies *where a rule is stated* — rest on
text with no force. This commit edited that block twice and H5 deepened the
mismatch by adding an express non-closure disclaimer, making the block's own text
decline to warrant the record §20.3 and §20.5 cite it for. Repair: move the two
cited consequences into §21.7's unlabeled prose, leaving the walk-through to
illustrate them. Byte-level: **no**.

### X-05 — hunk 1: the insertion puts a nearer numbered pair between "save two" and "The first exception"
Check: LOCAL_CONTRADICTION / anaphor. Location: §18.2. Quotation: "Two of those
fall outside the register, on the two distinct grounds §21.7 separates". Following
untouched sentence: "The first exception holds because a document has no declared
size". "The first exception" resolves to the first of "save two: what it states
against a tile's declared decoded size, and what it states about the frame's
declared `Window_Size`"; the insertion places "the two distinct grounds §21.7
separates" between them, and it is now the nearest ordered pair. A reader who
takes it recovers only from the trailing "because a document has no declared
size". Repair: "The first of the two exceptions above — the tile's declared
decoded size — holds because…". Byte-level: **no**.

### X-06 — hunk 2: the slack accounting is made precise over tiles and leaves the index region, the larger term, unnamed
Check: UNDERSHOT. Location: §20.3 step 4. Quotation: "re-emitting those tiles would
strand the originals as slack — every tile the change reaches, since `[R-LIF-01]`
freezes them where they lie — leaving the file larger for a change that reads like
a directory edit." The repair correctly narrows the tile term from "the whole
layer's worth". But the sentence's conclusion turns on the total stranded, and the
same section's Note states the other term: "any change to a layer's stored-tile set
re-emits that layer's whole tile-index region, so editing one sample of a 10⁶-tile
layer appends about 20 MB of index and leaves as much slack" ([R-CNT-17] obliges
the re-emitted region). Having made one quantity of the accounting exact, the
repair leaves its sibling — which for a large layer dominates — unnamed. Repair:
"…strand the originals as slack — every tile the change reaches, together with the
layer's whole re-emitted index region ([R-CNT-17]) — since [R-LIF-01] freezes them
where they lie". Byte-level: **no**.

## 15. Rejected candidates

**RC-1. H4's "exactly where" is stronger than §21.1's completeness clause.**
§21.1 gives only one direction ("enumerates every detectable file-conformance
violation this specification names"; omission = defect); H4 asserts a
biconditional, which additionally says no row exists for anything else. Dropped:
§21.1's opening ("each row is one malformed condition") together with [R-CNF-07]
("Every detectable file-conformance violation … is assigned exactly one reader
outcome") and §21.6's "Neither is a register row: the register enumerates
file-conformance violations (§21.1)" jointly support the converse, and I found no
row that is not a detectable file-conformance violation.

**RC-2. H1's "fall outside the register" mischaracterises §21.7's second ground.**
§21.7's ground (b) does not say such a requirement falls outside the register; it
says "Nothing is omitted from the register on its account, there being no
condition to omit". Dropped: the two formulations differ in emphasis, not in
consequence, and H1's own following words ("states no condition a file can exhibit
at all") state ground (b) exactly.

**RC-3. [R-SLB-04]'s and [R-LIF-05]'s "no register row" Notes contradict H4's
biconditional.** [R-SLB-04] calls a stale slab declaration "a validity error at
layer scope, detected as the invariant failures of [R-SLB-03] are: by a verifier"
— apparently a detected file-conformance violation with no row. Dropped: under
§21.7's test the staleness is not *separated* by any obliged check from a
fresh-but-violated declaration, so it is unwitnessed and no row is owed. Worth
recording that this case *would* have failed §21.1's deleted "differs, in its live
state" test, so H3 is the repair that rescues it.

**RC-4. [R-CNT-18]'s Note says "reader-detectable" where the test says "a reader
or a verifier".** Dropped: pre-existing (§21.7 already said "a reader or a
verifier" before this commit), the Note is non-normative, and §7.4's closing Note
establishes that no verifier parses sub-record payloads as records either, so the
conclusion holds under the wider instrument.

**RC-5. H1's analogy to [R-COD-06] fails for a user-metadata document, because a
verifier must check the decoded document's content rules (R5–R10) whereas a tile's
samples are unconstrained.** Dropped: an undisclosed-dictionary file that fails R7
is not separated by any obliged check from a file whose document is simply
ill-formed JSON, so the condition is still unwitnessed under §21.7's test. This
was the closest call in the audit.

**RC-6. §21.1's "One instance is one *distinguishable* file" and §21.7's "cannot
be told apart" state two different notions of distinguishability in one section.**
Dropped: they govern different objects (instance individuation for the corpus vs
detectability of a condition) and no passage applies one where the other is meant.
