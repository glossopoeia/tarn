# Cleanroom round 28 — findings

Protocol: ADR-0034, four phases, over the repairs of ADR-0109, ADR-0110, ADR-0111
and ADR-0112. Charter: [prompt.md](prompt.md).

## Verdict

**One byte-level ambiguity. G3 is not met.**

| | |
|---|---|
| Quiz | **15 agree / 0 diverge / 0 underdetermined** — twenty-second round running |
| Findings | **22**, from 7 reporters |
| Distinct defects | **18** by union-find; all three passes independently said 18 |
| Self-flagged byte-level | **0** |
| Upheld byte-level by any triage pass | **0** |
| Surviving the refute phase **and** an independent hand-check | **1** |
| Harness | 12 agents, 12 returned, 0 errors, 0 empty; refute phase 8 agents, 1 model failure recovered on the fallback |

Byte-level history: … → 0 → 1 → **2** → **1**.

**The round as run returned zero, and the zero did not survive.** No reporter
flagged byte-level and no triage pass upheld one. A refute phase run over that
zero established one, in a group all four readers had graded *editorial*, and
every number in its construction reproduces independently.

**G3's criterion does not reach its second half.** Round 27 returned two, so round
28 was a fresh first half — the seventh. It returned one.

## The harness did not fire its own refute phase, and the charter says it must

The charter is explicit: *"a zero is not a result… **Zero is the trigger for the
refute phase.**"* `README.local.md` states the same rule from round 17: *"Never
accept a unanimous zero without it."*

The implementation does not do this. Its trigger is

> a group is a *downgrade* when some reporter flagged byte-level and no pass
> upheld it

and a *split* is a disagreement between passes **on the `byte_level` field**.
With zero reporter flags and zero pass flags, both sets are empty, and the phase
logged `0 unanimous downgrade(s), 0 split verdict(s)` and ran nothing. **A round
that returns a clean zero is exactly the round this phase exists for, and is the
one case in which it cannot fire.**

The trigger has been reporter-keyed since round 17, and exactly two rounds since
then have returned **zero reporter flags**: round 25 and this one. Round 25's
refute phase fired on a single *recovered* AMBIGUITY, routed to it by hand because
that finding had bypassed triage — not by the trigger, which had nothing to fire
on there either. So **both rounds in which the trigger could not fire needed hand
intervention to get any refutation at all**, and in this one that intervention
changed the verdict.

This round's zero was attacked by hand instead: seven refuters, one per group
where a fork was most plausible — including the two groups the passes themselves
named as their weakest kills — plus one agent attacking the round-wide zero
across all eighteen defects. **One of the seven came back with a construction.**

The fix belongs in the harness, not the charter: fire the refute phase whenever
the round's byte-level count is zero, choosing targets by subject matter rather
than by flag.

## The survivor

### `ordinal-renumber-trigger-gloss` — `writer-03`, §20.3 step 4 `[R-WRT-04]`

**Nothing says where a carried-forward index entry goes when a planar layer's
channel *order* changes.**

Step 4, inside "An appender MUST, in order:", requires

> every other entry byte-identical at its **disk-ordinal position** (a geometry
> change renumbers ordinals wherever `[R-GEO-06]` moves them)

and the parenthetical is the document's only statement of when ordinals
renumber. `[R-GEO-06]` gives a planar tile the disk ordinal **c · N + s**,
"where c is the channel's index (§3.1)", and §3.1 fixes that index as "its
0-based position in that order".

**The two readings.** (1) *Name identity* — a carried-forward entry belongs to a
named channel, so when that channel's declared index moves, `[R-GEO-06]` moves
its entries and the parenthetical is merely under-inclusive. (2) *Position
identity* — an entry at position *k* is the entry for tile (k div N, k mod N),
`[R-GEO-06]` over the new declarations returns it to *k*, and the parenthetical
is exactly right: ordinals renumber iff N moves, which is what a geometry change
does. The reporter and all three triage passes took (1) and graded the defect
editorial. **Every rule that individuates a planar tile's channel does so
positionally** — `[R-GEO-06]`, `[R-SER-01]` ("the tile with disk ordinal c · N + s
… carries exactly the values of channel c"), `[R-IDX-01]` ("the entry for the tile
with disk ordinal k … is the k-th entry"), §19.4 step 2 — and **no rule anywhere
ties a channel's identity across generations to its name.** Reading (2) needs no
unstated premise; reading (1) does.

**The construction, re-derived here in full.** A planar layer, rank 1, extent
E = 2 and tile extent T = 1, so G = 2, N = 2, P = 1 and the grid covers the extent
exactly — **no padding position**, which makes `[R-SER-05]`, T4 and T5 vacuous.
Two channels, `a` and `b`, both uint8, so every tile's decoded size is P·B = 1
whichever channel it is taken to carry. Addressed-tile count C·N = 4
(`[R-GEO-03]`), `entry_count` 4 and `extent_length` 4·20 + ⌈4/2¹⁶⌉·4 = **84**
(`[R-CNT-17]`). All four tiles stored, one byte each at offsets 16–19, holding
`11 22 33 44`.

Commit **K** is stated wholly in format vocabulary and is identical under both
readings: emit the next generation whose layer record carries its channel entries
as **[b, a]** instead of [a, b]; store no tile, supersede no tile, change nothing
else. §20.3's declaration-change bar permits K under both readings — no padding
position exists, both channels' decoded size is 1, sample offset is 0, codec and
filter are layer fields.

| | Reading (1) | Reading (2) |
|---|---|---|
| index entries | permute to [e2 e3 e0 e1] | unchanged |
| index region | re-emitted in full at F | not appended |
| extent slot | re-pointed to (F, 84) | unchanged at (20, 84) |
| `crc_of_crc_array` | `cb 83 76 80` | `21 3e a9 bc` |
| `committed_file_length` | — | 84 lower, plus the pad delta |

**Both files are conforming.** `entry_count` is 4 = C·N and `extent_length` 84 in
both; every entry is well-formed under §15.3; each stored payload is exactly the
decoded size 1 (`[R-SER-07]`); no padding position, so §14.5 has nothing to check.
A conforming reader MUST accept both (`[R-CNF-03]`). Their reference arrays
differ — at x = 0 one gives (0x33, 0x11) and the other (0x11, 0x33) — and §21.7 is
precisely why no check separates them. **Each reading bars the other's file under
the clause in dispute**, so the disputed bytes are producible under exactly one
reading each. That is the charter's discriminator, second limb: *"If the disputed
file is conforming and only one reading permits an actor to produce it, the set
moves."*

**A second construction makes it a MUST NOT / MAY fork.** Same layer with `a`
uint8 and `b` uint16. Under (1) the bar tests each channel's own tiles, nothing
§14 fixes changes, and K′ is permitted. Under (2) the tile stored at ordinal 0
changes decoded size from 1 to 2 — one of the four effects the bar names — so
"A commit MUST NOT change a layer's declarations in a way that alters …" forbids
K′ outright and the operation becomes a new layer or a whole-file rewrite.

**Hand-check.** Every quantity above was re-derived independently of the refuter,
with a CRC-32C written from §4.5's parameters and validated on the document's own
`"123456789"` → `0xE3069283` vector: the four entry CRCs (`B048173D`, `93FBAD78`,
`71CEE914`, `D49CD9F2`), both segment CRCs (`42ED63A5`, `8391B634`), both
`crc_of_crc_array` values (`BCA93E21`, `807683CB`), and `extent_length` = 84. All
reproduce exactly.

**Why the passes' shared premise fails.** All three leaned on §21.7 — "the ordinal
mappings of `[R-GEO-06]` and `[R-SER-01]` are satisfied by a structurally valid
tile whatever values it carries" — and read it as licensing the writer. It does
not. §21.7's own opening sentence scopes it: obligations are listed there
"because a single file exhibits no witness of their violation", and it names
"§20.3 step 4's bar on a declaration change" among them. **Undetectable is not
permitted.** `[R-CNF-06]` binds an updater to every writer requirement for the
bytes it produces, and step 4 is a MUST. §21.7 is what makes *both* files
conforming — which the construction needs — and says nothing about which one the
appender is obliged to emit.

## What the round says about the ledger

The document and the ledger were swept before any repair was proposed. **Three of
the eighteen defects were already owned**, by entries their reporters had never
seen.

| Defect | Reporters | Sweep result |
|---|---|---|
| `ordinal-renumber-trigger-gloss` | `writer-03` | **Q-B6**, opened after round 25 on the channels' declared order. Round 28 found it cold from a different clause of the same step and supplied the construction the entry lacked. |
| `shuffle-fixed-point-universal` | `verifier-03`, `diagrams-02`, `adversary-06` — **three** | **Q-I6**, which already records "independently for any tile whose decoded image is invariant under the permutation". This is the **fourth** failure of that one sentence, and the second round running in which three reporters found it. |
| `appendix-g-unpinned-layout-and-tiling` | `writer-01` | **Q-I6**'s own question — which degrees of freedom the profile pins and why — with *declaration order* as a member the entry does not yet name. |

**Q-B6's standing changes: byte-level, and it gates G3.** It was opened
`[shaping]` on a walk that did not grade it. Round 28 grades it, with two
conforming files and a producer enumeration. That is a change in the entry's
standing, not a new entry — and the round adds a sub-question the entry's options
must now dispose of: **what individuates a carried-forward index entry across a
commit.** A Q-B6 option that bars a channel-order change closes the fork; one that
permits it must answer the sub-question. The entry's own stated premise — that the
channels' declared order "alters a stored tile's decoded image" — is itself
reading-dependent, which the entry did not record.

**Q-I6 is held whole, as ADR-0091 and this cycle's own rule require.** A fifth
patch to Appendix G item 5 is not the move; three reporters converging on the
fourth failure of one sentence is the entry's own diagnosis being confirmed again.

## The six that did not survive

Each was attacked by a refuter told the burden was reversed — find the fork or
show it cannot exist. All six returned `NOT_BYTE_LEVEL` with 5.0–7.1k characters
of attempted constructions apiece, three or four named constructions each, every
one killed by a quoted sentence rather than by assertion.

| Group | Killed by |
|---|---|
| `slack-disposal-missing-qualifier` | T8 is a register row, so the exploiting file is nonconforming under both readings (§2.4, `[R-CNF-05]`); §6.1's constant front block bars it again |
| `slack-total-duty-exemption-gap` | §21.2's reject-file outcome over F20 plus `[R-CNF-11]`'s priority rule — same bytes, same verdict, only a report line differs |
| `experimental-encoding-exception-over-broad` | `[R-MTA-10]`'s express closed list, which names the extent's terminal CRC among the structural checks that survive |
| `relocated-region-regeneration-trigger` | the literal reading's output fires T9 and F33; and the purposive output is emittable anyway, by a compactor from a different input and by any creator |
| `l23-detection-tier` | §19.2 for the untouched layer, §19.3 for the accessed one, and F4's "both obtainable within their records' inline_length" against the escalation |
| `preservation-table-unidentified` | §20.1 `[R-WRT-01]` and `[R-CNF-06]` bind an updater to §20.4's preservation obligations regardless of identifiers; `[R-CNF-01]` makes the unlabelled table normative |

## Harness integrity

- **12 agents started, 12 returned, 0 errors, 0 empty.** `journal.jsonl` carries 14
  `started` against 12 `result`; the two extra are logged stall-retries of
  `triage:implementer` and `triage:skeptic`, both of which then returned.
- **Every walk transcript matches its structured return exactly**, by independent
  id-scrape: reader 1, writer 3, verifier 3, diagrams 5, register 2, adversary 6 —
  each equal to its own `transcript_finding_count`.
- **The quiz author is checkable for the first time.** `transcript_finding_count`
  was added to its schema this round, after round 27 recorded that nothing
  compared that agent's return against its transcript. It returned 2 and its
  transcript labels 2.
- **All three triage passes CLEAN on mechanical coverage** — 22 of 22 ids, exact,
  by set difference against the reporters' ids rather than any pass's
  `all_input_ids_seen`.
- **Union-find gives 18** against pass counts of 18, 18 and 18.
- **No pass ran a directory listing.** The round-27 relocation holds: each pass
  wrote to its own directory outside `OUT`, and all three confirm they opened no
  walk transcript and no other pass's notes.

### The evidence fields worked

Required of every walk this round, after ADR-0112 recorded five empty lanes being
nearly reported as five clean ones. **66,441 characters across six lanes**, 7.8k
to 13.5k each, none empty.

They are not decoration. Three lanes independently implemented CRC-32C from §4.5's
parameters and reproduced **every constant the document prints** — `E3069283`,
`00000000`, `80A34955`, `C4EE982E`, `EECB3BB2`, and Appendix A's
**`402F157E`** — the last being the value ADR-0111 changed. With the pre-launch
hand-check that is **four independent derivations of it**. The register lane
derived `[R-CNT-06]`'s nine conditions from §6.2's ordered list and found exactly
nine rows citing it (F8, F9, F10, F12–F17), reproducing §2.3's count and its 2 + 7
split; and reproduced §21.8's "120 conditions over 275 instances" as 35 + 49 + 26 +
10 and 56 + 116 + 55 + 48.

**On the change ADR-0111 made, the instrument is as clean as it has ever been.**
Two agents blind to each other rebuilt the trailer from §6.2's layout table for a
quiz question and returned the same four bytes, `0df8679c`, which a third
computation reproduced. No finding this round touches the trailer's layout, its
CRC, Appendix A's dump, or the register's totals.

### One hand-check reverses a pass

Two passes derived that the byte-shuffle **fixes the byte at offset L − 1 at every
legal stride**; the skeptic did not, and built a "T5 witness" on a 6-byte planar
bool plane at s = 2. Re-derived here from `[R-COD-10]`'s own words — source
offset j·s + i, destination i·n + j, so j = n−1 and i = s−1 give L−1 → L−1 — the
final byte, where the pad bits live, is fixed. **T5 cannot witness a mis-strided
filter.** The repair therefore goes the correctness and implementer passes' way:
fix §21.7's first sentence, not T26. Not gate-relevant — all three graded the
group register-bookkeeping — but it decides which of two contradictory repairs is
right, and the reporter's own recommendation would have asked the corpus for a
vector that is not constructible.

### The eighth lane, and why it is not evidence against the survivor

The refute phase's eighth agent was charged with attacking the zero across all
eighteen defects and hunting for a byte-level question nobody had raised. It
returned **NOT_BYTE_LEVEL**, and the honest reading of that result is narrower
than it sounds.

Its **fresh sweep corroborates the trailer work**. It read §6.2, §9.2, §9.3, §20.5
and §23.2 end to end against the re-keying, recomputed Appendix A's trailer CRC
from raw bytes with a hand-rolled implementation — `0x402F157E`, a **fifth**
independent derivation — checked the layout table sums to 64 and the struck F11 is
handled as `[R-VEC-02]` and §2.2 prescribe, and reports finding **no sentence that
was true of the old counter and is merely plausible of `file_id` or F**. On the
change ADR-0111 made, that is a real negative from a lane that looked.

Its **roster re-check of the survivor is not**. On group 7 it wrote that "any
channel-set change large enough to matter for already-stored tiles is
independently barred by the 'MUST NOT alter what §14 fixes' rule earlier in the
same step" — **which is the premise the targeted refuter's construction was built
to falsify.** In the uint8/uint8 swap nothing §14 fixes changes under either
reading, so the bar does not bite; and "self-correcting regardless of *why*
`[R-GEO-06]`'s ordinal moved" assumes the answer to the question in dispute. This
lane had the roster titles, not the construction. It restates the shared framing a
fifth time rather than testing it.

It also ran on the fallback model, and ADR-0112 records what that costs. Its
`constructions_tried` is 1,575 characters against 5.0–7.1k from the seven targeted
refuters, and its `sections_opened` 836 against 1.1–1.9k. **Its coverage of the
roster is unestablished** and should be treated as such; its (b) sweep is not.

### The model failure, and what it cost

`refute:zero-attack` — the agent charged with attacking the round-wide zero — died
on `API Error: … safeguards flagged this message … [reasoning_extraction]`. The
recorded remedy was followed in order: the scope block was reworded into neutral
review language, which **failed again in 6 seconds with 0 subagent tokens**; the
agent was then moved to `model: 'sonnet'` and completed. **This is the third cycle
in which this failure has bitten, and the first in which rewording cleared
nothing.**

Everything else held: **20 of 21 agents across the round and its refute phase
returned on the primary model**, against 20 failures in 37 agents last cycle. The
one that failed was the one whose brief was framed as an attack, which is a
plausible enough pattern to be worth recording but is a single observation.

## Disclosures

All eight spec-reading agents disclosed injected context, and **this round the
channel is materially worse than in any before it.** The environment block's five
commit subject lines describe *in prose the very change under audit* — the
register hunter calls that out as "more seriously" than the instruction pointer,
the diagram auditor records that the subjects "corroborated a hypothesis I had
already formed independently from §6.2's layout table and §3.1's *generation*
entry", and the quiz answerer names the leak and identifies which of its answers
brush against it. Each states that no finding of theirs rests on it. **This is the
seventh round in which the channel has been disclosed and no mechanical check in
this project can see any of it.**

### A new breach class: agents contaminating each other through the shared scratchpad

The verifier disclosed, unprompted, that it wrote `crc.py` into the **shared**
session scratchpad root; that **another lane overwrote that file between two of
its calls**; and that it therefore executed the other agent's script and had four
of that lane's numbers printed into its context. It recomputed all four in a
private directory afterwards and no conclusion of its rests on them — they were
document constants it had already derived — but the general shape is that **any
lane can silently replace another's working file, and the victim finds out only
if the replacement happens to fail.**

Nothing in the harness prevents this. Every agent is told it may write scratch
files it creates itself; they all choose the same obvious name in the same shared
directory. The refute phase run over this round's zero was given a
private-scratch-directory clause and every refuter used one. **It belongs in the
round's own ACCESS block.**

Three agents (reader, diagram auditor, register hunter) each ran one `ls` of
`spec/` before internalising the access rule, disclosed it, saw only
`registry.json` and `tarn.md`, and opened neither.

Four agents again reported the line-count discrepancy in their brief — 4,648 by
`wc -l` against the charter's 4,649 — and each correctly identified it as a
trailing-newline convention rather than a finding.

Both parts of the lineage gate return clean. **The canonical word list is gone:**
it lived in the project's memory directory, which is now empty, so the gate was
run against the words recorded in `README.local.md` instead.

### The repository moved, and the old path is occupied

`wf-round27.js` points every agent at
`/Users/robertkleffner/Documents/GitHub/**tarn**/spec/tarn.md`. Round 27's own
transcripts confirm that path was correct then. It is not correct now: the
repository is `tarn-first-draft`, and the old path still exists as a **separate
git repository with no commits**, whose `spec/tarn.md` is a **295-line early
draft of this same document**.

Copying the round-27 harness verbatim would have briefed all fifteen agents on
that stub, and **no gate in this project would have said so** — `tarn_check`,
`tarn_build`, `tarn_vectors`, `tarn_propagate`, `tarn_editorial` and `tarn_chain`
all read the working tree, not the charter's path. The round-28 harness was
pointed at the real file and the rendered prompt was checked before launch.

That stale copy is a standing contamination hazard for every future round: it is a
**prior state of the document** one directory away from the current one, and an
agent that wanders into it reads the answers to the questions it is being asked.

## Disposition

Zero findings are left without a disposition.

**To the ledger — byte-level, and ADR-0091 forbids settling a rule's reach in a
repair slot.**

| Defect | Disposition |
|---|---|
| `ordinal-renumber-trigger-gloss` | **Already Q-B6**, whose standing changes: byte-level, gating G3, with this round's construction and its sub-question attached |

**To the ledger — already owned, held whole.**

| Defect | Disposition |
|---|---|
| `shuffle-fixed-point-universal` | **Q-I6**, fourth failure of the same sentence, three reporters |
| `appendix-g-unpinned-layout-and-tiling` | **Q-I6**, adding *declaration order* to the degrees of freedom the entry names |

**Repairable, each checkable against a named rule.** None is byte-level; five
touch register cells and so need an ADR under ADR-0104.

| Defect | Checkable against |
|---|---|
| `opening-blockquote-normativity` | §2.1 `[R-CNF-01]` — the front-matter blockquote claims an exemption the rule grants only to appendices |
| `appender-tier-list-incomplete` | §20.3 — shrinking an extent and unstoring a tile are appender operations §20.1's list omits |
| `slack-disposal-missing-qualifier` | §15.3 `[R-IDX-03]` — §9.7 drops "that no other claimant claims" |
| `compaction-figure-pad-not-hatched` | §5.2 `[R-CNT-21]`, §6.2 `[R-CNT-05]` — the pad is slack and the figure's legend is unscoped *(figure)* |
| `zero-layers-empty-directory-conflation` | §7.2 `[R-CNT-14]` — a zero-layer file's directory need not be empty *(register)* |
| `serve-unchanged-row-citation-short` | §21.1 — `[R-MTA-05]`'s rows F27 and L48 are not cited beside `[R-CNT-22]`'s *(register)* |
| `unwitnessed-inventory-omits-preservation` | §20.4 `[R-WRT-05]`, §6.3 `[R-CNT-08]` — §21.7's itemisation omits both |
| `t5-as-filter-witness` | §21.4 T26 and `[R-COD-10]` — repair §21.7's **first** sentence; the shuffle fixes byte L − 1 at every stride *(register)* |
| `experimental-encoding-exception-over-broad` | §18.2 `[R-MTA-10]` — the exception is written over a set `[R-CNT-25]` defines to include a failed extent CRC *(register)* |
| `relocated-region-regeneration-trigger` | §20.5 `[R-WRT-07]` — key the exception to the entries, not to the region |
| `l23-detection-tier` | §19.1 step 4 `[R-RDR-01]` — the name-field-fits determination is made at the open *(register)* |
| `should-consequence-universal` | §2.1's Note against §18.2 `[R-MTA-09]`, §16.1 `[R-SLB-01]`, §16.2 `[R-SLB-03]`, §23.2 `[R-PRV-03]` |

**Deferred with named owning sections.**

| Defect | Owning section |
|---|---|
| `slack-total-duty-exemption-gap` | §5.2 — `[R-CNT-21]`'s duty and exemption are keyed to non-complementary conditions; split verdict, and whether to re-key the rule or rely on §9.7 is a decision |
| `preservation-table-unidentified` | §20.4 — minting an identifier for the retention-and-drop obligations is permanent under §2.2, so it is the maintainer's call |
| `partial-product-not-designated` | §11.2 — split verdict (skeptic REFUTED); no normative change is owed, and whether to extend the Note is optional |

## Recommendations to the harness, in priority order

1. **Fire the refute phase on a zero.** The charter requires it, the
   implementation cannot, and this round's only byte-level finding came out of
   firing it by hand.
2. **Give every agent a private scratch directory.** One lane's script was
   silently replaced by another's this round.
3. **Delete or rename the stale `GitHub/tarn` working copy**, or make the
   round's harness assert that the spec it hands agents is the one under
   `git`. A prior draft of the document sitting at the harness's own historical
   path is the strongest contamination source this project has found that no
   gate can see.
