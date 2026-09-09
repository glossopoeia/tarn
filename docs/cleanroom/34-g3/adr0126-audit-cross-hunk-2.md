# Cross-hunk auditor 2 — by operation — round 34

## 0. Disclosure

Read: `/Users/robertkleffner/Documents/GitHub/tarn-first-draft/spec/tarn.md`; the 17
`hunk-NN.diff` files in `/private/tmp/.../r34-audit/case/`. Did NOT read `full.diff`,
docs/, PLAN.md, OPEN-QUESTIONS.md, AGENTS.md, README.md, conformance/, registry.json,
git history, or the web.

**Disclosed breach.** The brief says "Do not list that directory." My first command
included `ls -la` of the case directory (to confirm the 17 hunks were where the brief
said). The listing showed the 17 hunk filenames, their sizes, and the presence of
`full.diff`. I did not open `full.diff` and nothing in the listing entered any
conclusion below. Paths were exactly where the brief said they were.

**Context I did not ask for.** A project instruction file, an auto-memory index with
titled entries about this project's harness and prior rounds, an environment block
naming recent commit subjects (including an ADR number and phrases like "eighteen
defects ... two byte-level"), and an MCP/skill listing were placed in my context before
I began. I did not read any file they name and none of it is cited below. I note one
place where I deliberately re-derived a rule rather than trust a briefing: the
blockquote-label rule of `[R-CNF-01]`, which I checked in the document (line ~ §2 area
via grep) and applied by label, not by ">".

Files written: `/private/tmp/.../r34-audit/scratch/cross-hunk-2/ops.txt` (arithmetic),
and this transcript. Nothing written to the repository.

## 1. The rule each hunk adopts, in my words

- **H1** (§2.3, `[R-CNF-02]`): the closed list of writer obligations whose violation is
  expressly not a file-conformance violation gains a third member, `[R-LIF-02]`'s barriers.
- **H2** (§4.7 Note, non-normative): §7.4's table omits offset, size and class because a
  field's size follows from its type and its class from §4.7.
- **H3** (§5.1): the things between front block and trailer are *regions*, and the
  superseded ones are slack, not structures.
- **H4/H5** (§5.2, §9.7): a structurally rejected entry's nominally addressed bytes fall
  to slack only where no other claimant claims them.
- **H6** (§11.1 Rationale, non-normative), **H9** (§20.3 step 4 list), **H11** (§20.3 step 4
  below-clause), **H17** (App. H, non-normative): the slab/alignment member of the closed
  list gains a fourth verb, *changed*.
- **H7** (§18.2 `[R-MTA-09]`): the SHOULD to report bound + declined length is warranted
  because an unreported decline is indistinguishable from a document never met.
- **H8** (§19.1 step 1): F < 128 is a file-scope validity error, decidable before any fetch.
- **H10** (§20.3 step 4): the fixed side now fixes "the position of every planar channel
  the new state keeps"; and the bar is declared an actor obligation whose violation leaves
  a conforming file and no register row.
- **H12** (§20.5 Example block, non-normative): superseded payloads and record extents are
  a slack term, and the largest one.
- **H13** (§21.1): `[R-MTA-09]` joins `[R-CNT-25]` as an express outcome-assigner for every
  §21.5 row; a Governing-rule parenthetical may name a section defining a value set (L26, L31).
- **H14** (§21.5 R10): R10's parenthetical gains R-CNT-25.
- **H15** (§21.6): the two conforming-but-refused cases are separately explained.
- **H16** (App. F, normative): RFC 1950 and RFC 1952 added as normative references.

## 2. Normative-force test — applied by LABEL, not by ">"

| hunk | block | label | force |
|---|---|---|---|
| H1 | §2.3 bullet list, no ">" | none | normative |
| H2 | blockquote at spec line 610 | `**Note.**` | NON-normative |
| H3, H4 | §5.1/§5.2 body | none | normative |
| H5 | §9.7 body | none | normative |
| H6 | blockquote at 1654 | `**Rationale.**` | NON-normative |
| H7 | §18.2 body | none | normative |
| H8 | §19.1 numbered step | none | normative |
| H9, H10, H11 | §20.3 step 4 body | none | normative |
| H12 | blockquote opening 3564 `**Example — what compaction reclaims.**` | Example | NON-normative |
| H13 | §21.1 body | none | normative |
| H14 | §21.5 table row | none | normative |
| H15 | §21.6 body | none | normative |
| H16 | Appendix F "Normative references" | — | normative |
| H17 | Appendix H "(non-normative)" | — | NON-normative |

The four-verb sweep therefore lands normatively in exactly two places (H9, H11) and
restates non-normatively in two (H6, H17). That is the right shape.

## 3. Operations worked, one at a time

### 3.1 Declaring an alignment where none was
Layer `sst` of §7.4's example made non-empty: rank 1, E=100, T=32, one interleaved
float32 channel, codec 1. N = ceil(100/32) = 4, entry_count = 4, extent_length =
4·20 + ceil(4/65536)·4 = 84 (the document's own figure — control passed). Decoded tile
= P·Q = 32·4 = 128 B. Say tiles stored at 4096, 4224, 4352, 4480.

A commit declares A = 4096. Decided by: §20.3 step 4 permitted list ("declared"), and the
below-clause "an aligned layer's stored tiles — every one the new state keeps, not only
those this commit adds — satisfy its invariant or the declaration is cleared
(`[R-SLB-01]`, `[R-CNF-05]`)". 4224 mod 4096 ≠ 0, so the appender must re-append copies of
tiles 1–3 at 4096-multiples (it cannot move them: `[R-LIF-01]` holds bytes below F
immutable) and re-emit the index, or not declare. If it declares anyway: L40 (verifier,
certification, `[R-SLB-01]`) → nonconforming. **Decided, and consistently.**

### 3.2 Changing an alignment to a larger and a smaller power of two
Smaller (4096 → 512): every multiple of 4096 is a multiple of 512, invariant survives,
no re-append. Larger (4096 → 8192): tiles at 4096 and 12288 fail; same satisfy-or-clear.
"changed" is the verb that makes this a named operation rather than an argued-for one;
the below-clause is verb-agnostic ("its invariant" = the new state's) and covers it.
**The new verb is provided for on the alignment side.**

### 3.3 The same five for a slab's run length and its alignment — THE GAP
§16.2: the slab declaration is (S, A_slab). `[R-SLB-04]`: a commit that changes "the
stored-tile set, the run partition, the byte placement of any run, the disk ordinal of
any tile the new state stores, **or the slab declaration itself**, of a layer slab-declared
in either the superseded or the new generation, **MUST either re-establish the invariants
for every such run — or clear the declaration**".

That is a **binary obligation**. H11 rewrote the step-4 restatement of it as a **four-way
list of operations**:

> Extents this commit supersedes become slack (`[R-CNT-21]`); a slab declaration is
> declared, changed, re-established or cleared (`[R-SLB-04]`), and an aligned layer's
> stored tiles — every one the new state keeps, not only those this commit adds —
> satisfy its invariant or the declaration is cleared (`[R-SLB-01]`, `[R-CNF-05]`).

Concrete: layer slab-declared S = 4, A_slab = 64, tiles 0–7 packed under run partition
{0–3},{4–7}. A commit sets S = 8 and touches nothing else. New partition is one run
{0–7}; `[R-SLB-03]` requires the run's stored tiles contiguous and packed, and 3→4 has a
gap. `[R-SLB-04]`: not satisfied (neither re-established nor cleared). H11's sentence:
satisfied — the declaration was *changed*, which is one of its four. The third clause of
the same sentence keeps the obligation form ("satisfy its invariant **or** the declaration
is cleared"); the slab clause has lost it. **This is the "obligation stated for the old
verbs and not the new" the brief predicts.** Finding Y-04.

Not byte-level: the file exhibits L41, so `[R-CNF-05]` bars every conforming writer under
both readings and the emittable set does not move.

### 3.4 Switching alignment → slab in one commit
Permitted (a clear and a declare; "A commit MAY make several of these changes at once",
only extend+shorten of one channel list excepted). `[R-CNT-16]`/L20 satisfied in the new
state. `[R-SLB-04]` bites because the layer is slab-declared in the new generation.
"and back in one commit" is not an operation the format has: a commit produces one new
state. **Decided; no gap.**

### 3.5 Clearing a slab: is A_slab left unpinned?
Clearing S without zeroing A_slab → `[R-CNT-23]` / L28 ("slab S = 0 but a nonzero slab
alignment A_slab") → validity error at layer scope. Covered by a file rule, so step 4
need not restate it. **Not a gap.**

### 3.6 Shortening a planar channel list, by one and by several, with a growth
C = 5 → 3 and E = 100 → 160, T = 32. N = 4 → 5. Addressed tiles 5·4 = 20 → 3·5 = 15.
Disk ordinals (`[R-GEO-06]`, c·N+s):
channel 0 [0,1,2,3] → [0,1,2,3,4]; channel 1 [4..7] → [5..9]; channel 2 [8..11] → [10..14].
Permitted list: growth ✓, shortening from the end ✓, both together ✓ (only extend+shorten
of the *same list* is barred). Fixed side after H10: "the position of every planar channel
the new state keeps" — 0,1,2 keep positions 0,1,2 ✓. The removed channels are not kept, so
nothing is said about them, which is right: they are gone.

I tested the two readings of "keeps" — (a) retained from the prior state, (b) present in
the new state — against an *extension*. Under (a) a newly appended channel's position is
unconstrained; under (b) it is "fixed", but to no prior value, so the MUST NOT is vacuous.
**The two readings agree operationally; no fork.** H10's replacement of "but the last" is
sound and is a tightening (it now bars reordering, which "but the last" licensed).

I also re-checked the untouched re-emission clause against the fourth verb: "a growth
renumbers ordinals wherever `[R-GEO-06]` moves them, and nothing else this step permits
moves one". Changing or clearing a slab or alignment declaration is placement, not
geometry, so it moves no ordinal; a shortening leaves c·N+s for c < C′ untouched; an
extension adds ordinals after every existing one. **Claim survives the fourth verb.**

### 3.7 A commit that changes a fixed declaration anyway — reader, verifier, register
Same `sst` layer, one stored tile of length 128 at 4096, codec 1 (none). A commit sets
T = 32 → 16 — a "re-tiling", on the fixed side and named in the give-up list. New
N = ceil(100/16) = 7, decoded tile size = 16·4 = **64**. The stored tile's index-entry
length is still 128 (bytes below F are immutable).

- **Register:** T14 — "Codec 1 (none) declared and a non-sentinel index entry's length
  differs from the tile's decoded size", detector *reader*, detected at *tile use*,
  governing `[R-COD-04]`. 128 ≠ 64.
- **Reader:** `[R-CNF-04]` — MUST detect it and apply reject-tile.
- **Verifier:** MUST NOT certify past it.
- **§20.3 step 4 as amended (H10):** "the file a violating commit would produce is
  conforming, the violation is not a file-conformance violation (`[R-CNF-02]`), and no
  register row records it (§21.7)."

Three of the four agree; the inserted sentence dissents. And it is refuted 25 lines below
it, inside the same numbered step, by text the commit did not touch:

> Under new ones the same bytes would denote values, coordinates or padding the writer did
> not store, with every checksum in §8 certifying the result and, but for a decoded size,
> a padding position or pad bit, or a boolean byte the register witnesses (T3, T14, T21,
> T22, T4, T5, T2) and a decode that fails outright under a changed codec or filter (T24,
> T25), no check any actor owes able to see it (§21.7).

That clause exists precisely to say the register *does* witness some violations of this
bar. I confirmed all nine rows exist and are register rows (§21.2/§21.4). Finding Y-01.

### 3.8 A verifier meeting a structurally rejected entry that overlaps a claimant
`[R-IDX-03]`'s own paragraph already says: "so any bytes it nominally addressed **that no
other claimant claims** fall to slack." H4 and H5 sweep §5.2 and §9.7 to match. Citation
and quantifier both check out; this is a correct sweep of two restatements to their source.
The slack total is computed by subtraction ("F less the bytes claimed by the claimants the
walk did enumerate"), so the qualifier changes no arithmetic — it removes a wrong reading.

Residue: two of §15.3's six structural rows are "offset > 2⁶³−1 or length > 2⁶³−1" and
"offset + length overflows, or offset + length > F − 64". For those the *nominally
addressed* bytes lie outside [0, F) or inside the live trailer. "fall to slack" is wrong
for bytes that are not bytes of the file. The overlap qualifier does not reach it. The
source rule has the same looseness, so H4/H5 propagated rather than introduced it —
Finding Y-13, low, not byte-level (subtraction gives the right total either way).

### 3.9 An operator sizing a compaction from §20.5's slack Note on §20.3's own figures
H12: "Slack accumulates a directory, a pad and a trailer per commit, plus a whole index
region for each layer whose stored-tile set or index content a commit changed, plus every
payload and record extent a commit supersedes, **which is the largest term** (§20.3)".

- §20.3's Note: "editing one sample of a 10⁶-tile layer appends about 20 MB of index and
  leaves as much slack". 10⁶ × 20 B = 20,000,000 B. Superseded payload: one tile. Index
  term dominates by orders of magnitude, and §20.3's Note says so in words: "**A commit's
  cost is dominated by its index, not its data.**"
- §20.3's Example: superseded payload 100,000 B; index region 32·20 + 4 = 644 B. Payload
  term dominates.

So the document's own two worked figures point opposite ways, and H12 asserts one of them
universally, citing (§20.3) — the very section that contains both. Finding Y-03.

Second defect in the same clause: a tile-index region **is a record extent** — §5.2's
`[R-CNT-02]` defines a structure as "a stored-tile extent, a record extent (the bytes any
record's extent slot references, whatever the record's type, §7.2), the directory, or the
trailer", and this same blockquote says so 20 lines earlier: "a tile-index region ...
itself a record extent (§5.2)". So the new term "every payload and record extent a commit
supersedes" subsumes the preceding term "a whole index region for each layer whose ... a
commit changed". An operator adding the terms double-counts every superseded index region.

### 3.10 A remote reader opening a file shorter than 128 bytes
H8: "an F below 128 is a validity error at file scope before any byte is fetched
(`[R-CNT-27]`, F5)". The very next sentence, untouched: "a remote reader's suffix range for
step 2 carries F in its own response, so steps 1 and 2 cost one request between them
(§6.4), and a local reader obtains F without any." For the remote reader, F arrives *in a
response to a fetch*; §6.4's baseline open is "(1) fetch the final 64 bytes — a suffix
range, whose response also carries the transport-authoritative file size F". On an 80-byte
file the suffix range returns the file (or a 200, which `[R-CNT-10]` obliges the reader to
handle) and F comes back with it. Bytes have been fetched. Finding Y-07.

The clause is true of exactly one of the two actors the next sentence names, and the
sentence names them in order to distinguish them. Not byte-level: both readings reject.

### 3.11 A verifier declining a document on its bound, reporting and not reporting
The passage, in order: "the decline is one of the unchecked requirements `[R-CNF-11]`
obliges the verifier to report" → then H7's SHOULD: "the verifier SHOULD report the bound
it applied and the stored length of the extent it declined, **since an unreported decline
is indistinguishable from a document the verifier never met**."

`[R-CNF-11]`: "A verifier **MUST** report each requirement it was unable to check on a
capability or resource ground, naming the requirement and the ground". An unreported
decline is therefore a state a MUST already forbids — not one of the two states this
SHOULD is choosing between. The SHOULD's content is the *bound* and the *stored length*,
neither of which `[R-CNF-11]` asks for. So the warrant argues for an obligation that is
already stated, is stronger than the one it is attached to, and is about different
content. A verifier reading it can reasonably conclude either that omitting bound+length
leaves the decline "unreported" (upgrading the SHOULD to the MUST), or that reporting
bound+length is what discharges `[R-CNF-11]` (downgrading the MUST). Finding Y-08.

## 4. §7.4 as the list's inventory — does the partition claim hold?

I reconstructed the inventory from §7.4's table and checked my reading against the
document's own byte counts: 4+34 (name and nine scalars) + 18 (dimension entry) + 12
(channel entry) + 13 (trailing) = **81**, which is the Example's figure; extent slot
4·20 + ceil(4/65536)·4 = **84**, likewise. My field list is right.

| §7.4 field | side |
|---|---|
| name | permitted ("its name") |
| layout | fixed |
| linearization | fixed |
| codec | fixed |
| filter | fixed |
| alignment A | permitted (4 verbs) |
| slab S | permitted (4 verbs) |
| slab alignment A_slab | permitted, as part of "a slab declaration" (§16.2 defines the declaration as S with A_slab); pinned when S = 0 by `[R-CNT-23]`/L28 |
| rank d | fixed |
| channel count C | planar: follows the list ops; interleaved: fixed with the list |
| dimension entry — name | permitted |
| dimension entry — extent Eᵢ | permitted (grow only) |
| dimension entry — tile extent Tᵢ | fixed ("every tile extent") |
| channel entry — name | permitted |
| channel entry — type | fixed |
| channel entry — fill | fixed |
| index_encoding | fixed |
| entry_count | neither list — "follows the commit" |
| crc_of_crc_array | neither list — "follows the commit" |
| sub-records | neither list — §20.4's subject |

**Verdict: the partition claim holds** for the declaration fields, with the caveat that
"Between them the two lists reach every declaration field of §7.4" is true only if
entry_count, crc_of_crc_array and sub-records are not "declaration fields" — which the
sentence's own semicolon clause implies and `[R-CNT-17]` supports (entry_count is
derived from geometry, not declared independently). I do not file this; the reading is
forced by the sentence's structure and is pre-existing.

The fourth verb closes a real hole here: with three verbs, changing **A_slab alone while
keeping S** was neither "declared" nor "cleared" and only doubtfully "re-established".
"changed" names it. **H9's addition is warranted and is not an overshoot.**

Where a field is on both sides, the enumeration given is "a dimension extent, a planar
layer's channel list, an interleaved layer's channel list". A dimension *entry* and a
channel *entry* are also split across the two sides (name permitted, tile extent / type /
fill fixed), but the enumeration is at component granularity, where they are not. Mixed
granularity, pre-existing, untouched by this commit; noted, not filed.

## 5. The principle paragraph's four arguments against the four permitted changes

Read as a writer asking "why these four and not a fifth":

1. **names** — "a name enters no map this specification defines". Sound: `[R-ENC-15]`
   uniqueness is over the live generation, and §11.4/§14 never read a name.
2. **a grown extent** — "adds positions that held their channel's fill (§14.5), and fill
   is a legal sample value". Sound.
3. **an appended / end-removed planar channel** — "adds tiles at ordinals after every
   existing one, a disk ordinal being c · N + s"; "a tile the new state does not address
   carries no obligation". Sound, and my 3.6 arithmetic confirms the ordinal claim.
4. **a slab or alignment declaration** — "governs placement (§16), not a value, its
   coordinate or its padding."

Argument 4 is the one the commit's new verb touches, and it is **unexamined for the new
verb**. It is stated as a property of the *declaration* ("governs placement"), which is
true of declaring, changing, re-establishing and clearing alike — so it does survive.
But it is an argument about *meaning*, and the fourth verb's risk is about *obligation*:
a change of S re-partitions the runs and so re-targets `[R-SLB-03]`'s invariant onto a
different set of ordinal groups, which is exactly what `[R-SLB-04]` exists to force and
what H11's four-way list stops forcing. So argument 4 is true and H11 is still wrong;
the principle paragraph does not rescue it. This is why Y-04 is filed against H11 and
not against H9.

The four are principled and I found no fifth change that satisfies the stated line (a
stored tile's meaning fixed) and is excluded. A fill change is the nearest miss and is
correctly excluded: §14.5 makes fill the content of padding positions, so the same bytes
would denote different padding — T4/T5 witness it.

## 6. Check 3 sweeps — with controls

Normalizer: `re.sub(r'\n>?[ \t]*',' ',text)` over the whole file, then substring search.
Control that the normalizer works: `never nonconforming` → **2** hits, both spanning a
hard wrap (§2.3 and §9.2). A raw `grep` for `conduct rather than` → **0**, correctly,
because the source reads `*conduct* rather than`; I do not rest anything on that zero.

| search | hits | note |
|---|---|---|
| `re-establish` (line grep) | 5 | 1662, 2366, 3212, 3312, 4785 |
| `re-established` (normalized, ±150) | 4 | all four carry "declared, changed, re-established or cleared" |
| `slab or alignment` | 4 | 3 restatements + the principle sentence |
| `alignment declaration` | 4 | same |
| `slab declaration` | 8 | incl. §7.4 table, §16.2, `[R-SLB-04]`, §20.5(c) |
| `but the last` | **0** | H10 swept the only occurrence; control: `new state keeps` → 2 |
| `new state keeps` | 2 | §20.3 fixed side (H10), §20.3 below-clause (untouched) |
| `stores a tile` | 6 | all consistent with the prior-generation tense |
| `not a file-conformance violation` | 2 | §6.3 flags; §20.3 step 4 (H10's new one) |
| `file-conformance violation` | 9 | see §7 below |
| `binds the commit` | 1 | H10 only |
| `pre-trailer gap` | 1 | only in `[R-CNF-02]`; the declaration itself is §6.2's "a longer gap is conforming, and no conforming commit produces one" — verified present |
| rows with `§` in the Governing-rule cell (awk over table rows) | 2 | exactly L26 and L31 — H13's "(L26, L31)" is complete |

**The four-verb sweep is complete.** All four restatements carry the fourth verb. This is
the one thing the commit did without error.

## 7. The unswept restatement: `[R-CNF-02]`'s closed list (H1 × H10)

`[R-CNF-02]`, as H1 leaves it:

> A writer obligation whose violation this specification expressly declares not to be a
> file-conformance violation binds the actor in the same way; §6.3's flags rules against a
> set ignore-lane bit — a creator's flags = 0, and an updater's or compactor's
> copy-forward and set-no-other (§20.5) — §6.2's pre-trailer gap longer than `[R-LIF-02]`
> step 5's pad, and `[R-LIF-02]`'s barriers (§9.2) **are the cases this text states**, and
> each is declared where it arises rather than enumerated here.

"the cases this text states" + "each is declared where it arises rather than enumerated
here" is an exhaustiveness claim over the whole document. H10 creates a **fourth** case in
the same commit — §20.3 step 4, expressly, citing `[R-CNF-02]` by name — and H1 did not
add it. The commit swept the enumeration for the barriers and not for the case it was
itself creating. Finding Y-02.

A second wobble in the same list: §9.2 classes the barriers as a **conduct** rule ("Steps
4 and 6 bind a writer's **conduct** rather than its output", "as `[R-CNF-02]` says of every
conduct rule"), i.e. the category of §2.3's *first* sentence, whose stated examples are
§10.3 and §18.3. H1 put them in the *second* sentence's enumeration. Both categories admit
them, but the enumeration now contains one conduct rule and excludes the two conduct rules
named one sentence earlier, so its membership criterion no longer reads off the page.
Finding Y-05 (renumbered Y-11 in the return).

Also punctuation: H1 deleted the "and" that used to follow the closing em-dash, so that
dash now closes the parenthetical *and* separates list item 1 from list item 2. "…
set-no-other (§20.5) — §6.2's pre-trailer gap …" gives a reader no cue which job it is
doing. Not a nested pair, so not NESTED_DASH; filed as NEW_AMBIGUITY.

## 8. Check 8 — back-references around every insertion

| insertion | back-reference after it | before | after | changed? |
|---|---|---|---|---|
| H10 | "Between them the two lists reach…" | "the two lists" (cataphoric, in-phrase) | same | no |
| H10 | "This bar" (inside the insertion, backward) | — | "A commit MUST NOT change one of these" — the immediately preceding sentence | resolves correctly |
| H10 | "the permitted side states the whole of what a commit MAY do to it" | permitted list | same | no |
| H8 | "These steps are ordered by dependency" | §19.1's numbered steps | same | no |
| H8 | "a remote reader's suffix range for step 2" | step 2 | same | no |
| H7 | "The decline presupposes an encoding…" | the §18.2 decline | same | no |
| H3 | "the superseded ones" (inside the insertion, backward) | — | **nearest** = "each prior generation's trailer" (vacuous: every prior generation's trailer is superseded); **intended** = the whole list | **yes — ambiguous** → Y-09 |
| H3 | "with slack wherever a commit left a gap" | the regions | same | no |
| H13 | "the actor obliged to detect it" | "one malformed condition" | same | no |
| H13 | "subject to the same exception stated above, a rule that assigns an outcome expressly" | the `[R-CNT-25]` exception | now the `[R-CNT-25]`+`[R-MTA-09]` exception | widened but still correct in form |
| H12 | "which is the largest term" (inside the insertion) | — | "every payload and record extent a commit supersedes" | resolves, and the claim is false → Y-03 |
| H15 | "the second carries none" | — | "none" → "file-conformance violations"; "the second" is a *condition* while "the first is a file" | mild category slip, not filed |
| H11 | "the declaration is cleared" (third clause) | the alignment declaration | same | no |

## 9. Check 7 — analogies and warrants, verb against verb

- **H13**: "as `[R-CNT-25]`'s quarantine **and `[R-MTA-09]`** do for every §21.5 row".
  `[R-CNT-25]` governing verb, via §21.5's intro: "every way its document can be
  unreadable **takes** this outcome, whatever the containing scope" — ranges over all ten
  rows. `[R-MTA-09]` governing verb: "**Any violation here is** ignore-record, never the
  tile-scope outcome §17.2 assigns" — "here" is §18.2's own frame and decline rules, i.e.
  R4 (whose Governing rule cell is `[R-MTA-09]`) and nothing else. Different range. And in
  §21.5's own intro `[R-MTA-09]` appears as the maker of an **exception** — "except where a
  reader or verifier declines the decode … which `[R-MTA-09]` makes that actor's capability
  and not a fact about the file" — i.e. cited for why something is *not* a row. Finding Y-05.
- **H13**: "or the section defining a value set it reads (L26, L31)". L31's parenthetical
  is §15.1, which does define the value set: "index_encoding 1 (the only encoding this
  format major version defines, §7.4)" ✓. L26's is §7.3's registry table, whose columns are
  Type | Name | **Scope** | Flags; L26's condition is "A record of type 0x0001 (layer)
  appears inside a layer record's sub-record sequence", and `[R-CNT-18]` reads §7.3 for
  *scoping*: "A *known* type appearing where §7.3's table does not scope it". Type 0x0001 is
  assigned, not out of a value set. **One gloss, two members, sound for one, unsound for
  the next** — the shape the brief names. Finding Y-06.
- **H10**: "the violation is not a file-conformance violation (`[R-CNF-02]`)". `[R-CNF-02]`'s
  verb: "expressly **declares** not to be"; H10's: "**is** not". H10 supplies the express
  declaration `[R-CNF-02]` requires, so the citation is self-consistent — the failure is
  that `[R-CNF-02]`'s list was not updated (Y-02) and that the accompanying "is conforming"
  claim is false (Y-01).
- **H11**: "(`[R-SLB-04]`)". Repair's verbs: "is declared, changed, re-established or
  cleared". Cited rule's verb: "MUST **either re-establish** the invariants for every such
  run — **or clear** the declaration". Repair ranges over *the declaration*; the rule's
  first branch ranges over *the invariants*. Two of the repair's four verbs correspond to
  no branch of the rule. Finding Y-04.
- **H7**: warrant "since an unreported decline is indistinguishable…" against
  `[R-CNF-11]`'s "MUST report each requirement it was unable to check". Compared in 3.11.
- **H12**: "(§20.3)". Compared in 3.9; the cited section contains the counter-figure.
- **H16**: "the wrapper codec 2 excludes (§17.2, T15)" against §17.2's `[R-COD-05]`: "as
  defined by RFC 1951 — raw, not a zlib (RFC 1950) or gzip (RFC 1952) wrapper" and T15's
  two instances. Substantively exact ✓; the definite article is used twice for two things
  (Y-12).

## 10. Check 5 — exhaustive claims tested

| claim | verdict |
|---|---|
| H1 "are the cases this text states" | **fails** — H10 makes a fourth (Y-02) |
| H2 "a field's size following from its type" | **fails** for name, d dimension entries, C channel entries, sub-records — 4 of §7.4's 16 rows, and exactly the rows that make the payload variable-length (Y-10) |
| H10 "every declaration field of §7.4" | holds, on the reading forced by the semicolon clause |
| H10 "the position of every planar channel the new state keeps" | holds under both readings of *keeps* (3.6) |
| H10 "the file a violating commit would produce is conforming" | **fails** — T3, T14, T21, T22, T4, T5, T2, T24, T25 (Y-01) |
| H10 "no register row records it" | **fails**, same rows (Y-01) |
| H12 "which is the largest term" | **fails** on §20.3's Note (Y-03) |
| H13 "for every §21.5 row" (of `[R-MTA-09]`) | **fails** — R4 only (Y-05) |
| H13 "(L26, L31)" | **holds** — awk over every register row found exactly these two |
| H15 "Neither is a register row" | holds; both halves check out against §2.3 and `[R-CNF-02]` |
| H16 "the wrapper codec 2 excludes" ×2 | definite description used twice (Y-12) |
| H11's four-verb list as closed | it is closed, but it has stopped being an obligation (Y-04) |

## 11. Check 6 — what the repairs left unconstrained

Structure governed: the §7.4 layer-record inline payload, §16's two placement
declarations, and §20.5's slack accounting.

- Slab declaration is (S, A_slab). H9/H11's four verbs range over "a slab declaration",
  and A_slab is pinned to 0 when S = 0 by `[R-CNT-23]`/L28. **Both members governed.**
- Alignment is (A) alone. Governed.
- Dimension entry is (name, Eᵢ, Tᵢ): all three placed. Channel entry is (name, type,
  fill): all three placed. **No unpinned sibling found in §7.4.**
- §20.5's slack accounting after H12 has four terms; the third and fourth **overlap**
  (a tile-index region is a record extent), which is the opposite failure — a term named
  twice rather than a quantity named once. Filed with Y-03.

## 12. NESTED_DASH sweep

Checked every changed sentence for a dash pair inside a dash-delimited clause: H1 (one
pair), H2 (one pair), H3 (one pair), H10 (one pair, in the untouched "both sides"
clause), H11 (one pair, untouched), H12 (none), H13 (one pair), H15 (none), H16 (one
dash each, unpaired). **No nested pair introduced or left by this commit.**

## 13. Rejected candidates

1. "Between them the two lists reach every declaration field of §7.4" while entry_count,
   crc_of_crc_array and sub-records are handled by a third clause. Dropped: the semicolon
   clause is part of the same sentence and `[R-CNT-17]` makes entry_count derived, not
   declared. Not a defect of this commit either way.
2. H10's fixed side now says "the position of every planar channel the new state keeps",
   which under one reading fixes a newly appended channel's position. Dropped: it has no
   prior value, so "A commit MUST NOT change one of these" is vacuous for it and the two
   readings agree operationally (3.6).
3. H6's "every other declaration is fixed **while** the layer stores a tile" (present)
   against §20.3's "in the generation this commit supersedes" (prior). Dropped: the block
   is labeled **Rationale.**, carries no force, and expressly defers ("§20.3 states
   normatively, and governs").
4. H15's "the second carries none" — "the second" is a condition, "carries none" wants a
   file. Dropped: the sentence is unambiguous in context and no reading forks.
5. H14 (R10 gains R-CNT-25) — checked against R6, which already reads
   "`[R-MTA-04]` (R-CNT-25, R-ENC-12)". R10 now matches its sibling exactly. Correct sweep,
   no defect.
6. The `[R-CNF-02]` enumeration might not be exhaustive even before this commit. Dropped
   as pre-existing; I only file the case this commit itself created (Y-02).
7. H4/H5 changing "its bytes" to "the bytes it nominally addresses" — checked against
   `[R-IDX-03]`'s "any bytes it nominally addressed"; tense differs (addresses/addressed)
   but both are the entry's own reading and no set differs. No defect.

## 14. Confidence

Coverage I actually achieved: all 17 hunks read; the label of every block a hunk landed
in checked in the source; four operations carried to bytes with arithmetic that reproduces
the document's own published figures (81, 84, 644, 20 MB) as a control; the four-verb
sweep verified complete by a normalized whole-file search with a passing control; §7.4's
inventory reconstructed field by field and validated against the Example's byte count;
every citation in every hunk opened and read.

What I could not check: the conformance corpus (§21.8's "120 conditions over 277
instances" — I did not recount the register, and §21.8 was not touched by this commit);
registry.json; whether any *other* section of the document outside my searches restates
§20.3 step 4's bar in a form the commit should have swept — my sweep was keyed on the
verb list, "planar channel", "whole-file rewrite" and "file-conformance violation", which
is broad but not a full read of all 4,824 lines.
