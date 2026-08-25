# Cleanroom round 26 — findings

Protocol: ADR-0034, four phases, preceded by the ADR-0099 repair audit in this
directory. Charter: [prompt.md](prompt.md).

## Verdict

**One byte-level ambiguity. G3 is not met.**

| | |
|---|---|
| Quiz | **15 agree / 0 diverge / 0 underdetermined** — twentieth round running |
| Findings | **25**, from 7 reporters |
| Distinct defects | **17** by union-find; all three passes independently said 17 |
| Self-flagged byte-level | 2 |
| Surviving refute **and** an independent check | **1** |
| Harness | 14 agents, **14 returned, 0 errors, 0 empty** |

Byte-level history: … → 0 → 2 → 0 → **1**.

**G3's criterion resets.** Round 25 returned zero; this round, reading its
repairs, returns one. Rounds 8, 10, 14, 24 and now 26 have each found the next
defect in the repairs a zero produced. **Five attempts at the second half, none
successful.**

## The survivor — `verifier-01`

**`[R-ENC-04]`'s ceiling does not say whether it reaches Gᵢ · Tᵢ, and a
zero-extent layer forks accept against reject on it.**

`[R-ENC-04]` binds "any quantity **this specification defines** as a sum or
product of integers obtained from a file (offsets plus lengths, grid counts, tile
counts, sample-position counts, ordinals)". §11.3 writes Gᵢ · Tᵢ — once, as the
left operand of a comparison, with no name, no gloss and no cross-reference to
§4.2. The bold term §11.3 defines is *padding positions*, not the product.

The two readings agree wherever every extent is nonzero, because
N · P = ∏(Gⱼ · Tⱼ) with every factor ≥ 1, so N · P ≥ Gᵢ · Tᵢ and L2's `N·P`
instance already catches any overflow. **They diverge only when some dimension
has extent 0**, since then N · P = 0 however large another axis's product.

The constructed file, verified independently three times: rank 2; dimension a
with E₀ = 0, T₀ = 1, so G₀ = 0; dimension b with E₁ = 2⁶³ − 1, T₁ = 2, so
G₁ = 2⁶². **G₁ · T₁ = 2⁶³, over the ceiling by exactly 1**, while N = 0,
N · P = 0, C · N = 0 and `entry_count` = 0 — every quantity L2 names and every
quantity §19.3 sends a reader to check is in domain. `[R-GEO-02]` says such a
layer MUST be accepted. One implementation serves it; the other reports a
validity error at layer scope and the file nonconforming, and `[R-CNF-05]` then
forbids a conforming writer from emitting those bytes. **The emittable set
moves.**

**For the narrow reading:** §4.2's own parenthetical gloss omits it; L2's
instance cell enumerates nine derived quantities and omits it; §19.3's cited
range is `[R-GEO-01]`–`[R-GEO-03]`, stopping short of §11.3's `[R-GEO-04]`; and
the document has an explicit-designation pattern it does not follow here —
§14.2's `[R-SER-02]` ("These products and sums are declaration-derived quantities
under `[R-ENC-04]`") and §14.3's `[R-SER-07]` both designate expressly.

**For the broad reading:** §11.2's `[R-GEO-03]` says "These products, **like all
geometry arithmetic**, are subject to `[R-ENC-04]`"; §20.3 says "the list is not
offered as exhaustive"; §22.2's `[R-SEC-02]` says flatly "Every sum and product
taken from a file is overflow-checked before use"; and §17.2's Note says it
"binds any sum or product a file yields".

**This is a decision about a rule's reach, and ADR-0091 governs**: it goes to the
ledger with options priced before any normative text moves.

## The one that did not survive — `adversary-01`

**`[R-COD-04]` carries no "(non-sentinel)" qualifier where T14 and seven other
rows do.** Read alone, and with §21.1's "where a row and the rule it cites
diverge, **the rule governs**", that would make a sentinel entry's length field
(2⁶⁴ − 1) unequal to the tile's decoded size and reject every sparse codec-1
layer.

All three triage passes downgraded it; the refute phase overturned them; **two
independent checkers then graded it not byte-level**, and between them they
reached texts no earlier reader had quoted:

- `[R-COD-04]`'s MUST is **derived**, not free-standing: "The stored bytes are
  the filtered image verbatim. The index entry's length **therefore** MUST
  equal…". §3.1 defines *stored* as precisely "not the sentinel", so the premise
  has no instance for a sentinel entry and the derived obligation has none.
- The reading proves too much. `[R-COD-06]` and `[R-COD-08]` have the identical
  shape, so the same reading would reject every sentinel under **all four**
  codecs, abolishing sparse layers — against §13.3, §15.2 and §21.6.
- §15.2's `[R-IDX-02]`: "Sentinel entries are a reserved pattern, **not offsets
  or lengths**." §15.3's table classifies the entry "valid sentinel — reads as
  fill", and §21.6 adds that "A reader that treats any of them as a failure is
  the nonconforming party."

**Both checkers nonetheless stated the counter-case at its strongest**, and it is
not weak: §21.1 assigns the loser in advance, and §21.9 says an addressed tile
has a decoded size "whether or not its index entry is the sentinel", so both
operands of the equality do exist. The finding is **a real drafting gap and not a
fork** — the qualifier should be written, since the document writes it in seven
register rows and four §15.3 rows and carries it here only by inference.

**The instrument's own lesson.** The refute phase overturned a downgrade that was
correct. It has now changed a headline verdict three times in this project, twice
rightly; this is the first time it went the other way, and it went that way
because it argued from §21.1 alone and never opened §15.2 or §3.1. A refuter is
as exposed to a narrow reading as the pass it attacks.

## What the round says about this week's ledger entries

**Q-B8 was corroborated by the widest convergence in this project's history**,
by readers who had never seen it:

| Defect | Reporters | Triage |
|---|---|---|
| §11.1's "last" reads positionally, which is the document's house sense | `reader-02`, `writer-01`, `verifier-03`, `adversary-02`, `quiz-02` — **five** | CONFIRMED ×3 |
| §13.3's Note states the re-emission trigger short of §20.3 step 4's | `reader-01`, `writer-02`, `diagrams-03`, `quiz-03` — **four** | CONFIRMED ×3 |

Both were ledgered as **Q-B8** before this round launched, so neither is a
finding without a disposition. The census argument a single refuter made against
three verifiers now has five cold readers behind it.

## Harness integrity

- **14 agents started, 14 returned, no error line.**
- **Every walk's transcript matches its structured return exactly**, by
  independent id-scrape: reader 3, writer 6, verifier 3, diagrams 4, register 4,
  adversary 2.
- **All three triage passes CLEAN on mechanical coverage** — 25 of 25 ids, exact,
  checked by set difference against the reporters' ids rather than by any pass's
  `all_input_ids_seen`.
- **Union-find gives 17** against pass counts of 17, 17 and 17.
- The reconciler flagged both byte-level groups **HAND-CHECK REQUIRED**; both
  were hand-checked against the document, and the survivor's arithmetic was
  recomputed independently three times.

## Disclosures

All nine spec-reading agents disclosed injected context: a project instruction
pointer, an index of the maintainer's notes, and an environment block naming the
branch and recent commit subjects, several of which name section numbers and
requirement identifiers.

**The adversary put that channel more sharply than any agent has.** It called the
commit-subject block "the material breach", said the subjects "describe, in
outline, what two of the seven changed passages were changed *to*", and added: "I
read them before I read the spec and **cannot unsee them**." It then set out,
passage by passage, how it had derived its findings from the document instead.
Its two findings are §11.1's "last" — which four other agents reached
independently — and `[R-COD-04]`, which no commit subject touches. Nothing in the
round turns on the leak, and the round cannot prove that; only the disclosure
makes it assessable at all. This is the fifth distinct form the channel has
taken, and no mechanical check in this project can see any of them.

**A disclosed breach, by all three triage passes.** Each ran `ls` on the round's
output directory before internalising the charter's prohibition on listing it,
and each said so unprompted, named what the listing showed, and stated it opened
nothing. Two confirmed no `transcript-triage-*.md` existed at that moment; the
third saw a single scratch `.py`. **Independence holds** — the passes are barred
from each other's transcripts by name and none existed to see. The fix is to the
harness, not the charter: an agent runs an orienting `ls` before it has finished
reading its brief, so the round's transcripts should be written somewhere the
agent has no reason to look.

Both parts of the lineage gate return clean.

## Disposition

The document and the ledger were swept before any repair was proposed.
**Six defects needed no new entry:**

| Defect | Sweep result |
|---|---|
| §11.1's "last" (5 reporters) | **Already Q-B8**, opened hours earlier |
| §13.3's re-emission trigger (4 reporters) | **Already Q-B8** |
| §21.7's account of unwitnessed obligations | **Already Q-I5** (§21.7 whole) |
| §21.2's "geometry" carve-out | **Already Q-H6**, which quotes that very property |
| Appendix G's closing enumeration; "the same input" | **Already Q-I6** (what the profile pins and why) |
| §21.2's two senses of F | **Q-H6 territory** — held with it rather than split off |

**To the ledger.** `verifier-01` becomes a new entry: `[R-ENC-04]`'s reach, with
the narrow and broad readings, the constructed file, and the cost of each option.
It is byte-level, so it gates G3, and it is a rule's reach, so ADR-0091 forbids
settling it in a repair slot.

**Repaired, as checkable against a named rule.** `[R-COD-04]` gains the
"(non-sentinel)" qualifier its seven sibling register rows carry. Appendix G item
5's claim that byte-shuffle changes every tile it touches is corrected against
§17.3, which makes it the identity in the cases §17.3 names.

**Deferred with named owning sections:** `reader-03` (§16.1's alignment
invariant and structurally rejected entries — §16.1); `verifier-02` (§5.2's
partial slack formula against the "never an under-count" promise — §5.2, held
near Q-C7); `diagrams-01` (Appendix A's "a local reader" against §6.1's residency
test — Appendix A); `diagrams-02` (§20.3's cost Note keys re-emission to the
stored-tile set then instances it with a supersede — §20.3); `register-03`
(L23's Detected cell against §19.1 step 4 — §21.3); `quiz-01` (§9.6's "how many
it rejected" — §9.6); `writer-06` (whether a commit may change a layer's channel
count or layout — §20.3, checked against Q-B6 and distinct from it).
