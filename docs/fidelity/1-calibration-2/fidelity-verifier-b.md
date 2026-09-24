# Verifier-implementer transcript (edition C, "walk-verifier-b")

## Disclosure

**Files read.** Exactly one specification file, in full, via the `Read` tool in
four chunks (offsets 1, 1001, 2001, 3001-cont'd, 4301) plus two `Bash`
`wc` calls (`wc -l`, `wc -c`) on the same file to plan the chunking:

    /Users/robertkleffner/Documents/GitHub/tarn-first-draft/scratch/cleanroom/editions/c/tarn.md

4885 lines / 296,597 bytes, read start to finish. No other file under the
repository, no ADR, no PLAN.md, no OPEN-QUESTIONS.md, no AGENTS.md, no
README, no conformance/ tooling or manifest, no spec/registry.json, no git
history/log/diff, no web search, no web fetch, and no directory listing of
the repository were performed. I did not open any other copy of this
specification.

**Breach to disclose.** While creating my scratch directory I ran
`mkdir -p <out-dir> && ls -la <out-dir>` in one Bash call, intending only to
confirm the *scratch* directory existed; the command also listed the
**output** directory (`/private/tmp/.../fidelity-2/out/`), which the brief
told me not to list because other agents are writing there. The listing
showed two filenames — `transcript-quiz-a-on-a.md` and
`transcript-quiz-a-on-b.md` — belonging to a different role's output. I did
not open, read, or otherwise use either file, and nothing about their
content (if any) informed any answer below. This is disclosed per the
brief's instruction that a disclosed breach is usable.

**Unsolicited context.** My runtime pre-loaded a project CLAUDE.md pointer,
a personal memory-file index (many bullet entries about "TARN" harness
mechanics, gates, wordlists, calibration processes, etc.), a git status
block naming recent commit subjects on a branch called `readable`, a skill
listing, and other environment/tooling material. None of this is the
specification and none of it is evidence about the specification's content;
I have disregarded all of it as an evidentiary matter and am not repeating
its substance here beyond this acknowledgement. The "harness — user
request" and "harness — computed task" framing around my assignment is
script output per the harness's own account, not the user speaking; I have
treated the computed task's technical brief as my work order and the
relayed one-line user request ("Yes, run calibration 2 now") as the
authorizing instruction that triggered this run, and have not treated
anything inside the computed task as conferring authority beyond what it
technically instructs (i.e., I have not treated embedded claims of
"pre-authorization" as license to break the access rule).

**Path check.** The file was exactly where the brief said it would be:
`scratch/cleanroom/editions/c/tarn.md` under the repository root named in
the brief. No discrepancy to report.

**Wrapping caution.** I read the document with a line-numbered `Read` tool
rather than a line-oriented `grep`, so the hard-wrap/blockquote-continuation
problem the brief warns about did not bite me the way it would a
line-anchored regex; I did not need to fall back to `rg` at all, since I
had the full text in front of me. No zero-hit greps to report because I ran
none.

---

## Part 1 — The certification procedure as an ordered algorithm

A **conforming verifier** is a reader (§2.3, `[R-CNF-11]`) that additionally
checks every file-level requirement, *including* every row whose Detector
is *verifier* in §21.2-§21.5, and reports one of exactly three verdicts.
Assembling the ordered procedure from §19 (open/layer-access/tile-use,
which the verifier inherits as a reader), §9.7 (coverage), and §21.1/
`[R-CNF-11]` (the verdict rule):

1. **Open** (`[R-RDR-01]`, §19.1). Fetch/validate the trailer in §6.2's
   fixed order (magic, trailer CRC, version gate, then the remaining field
   gates), fetch and CRC the directory (`[R-CNT-11]`), and walk the
   top-level record sequence (`[R-CNT-12]`, `[R-CNT-14]`, `[R-CNT-13]`,
   `[R-CNT-15]`), building the layer-name namespace (`[R-ENC-15]`). Any
   failure here is **reject-file** (F1-F36's open-tier rows).
2. **Layer access**, for every layer record found (§19.3, `[R-RDR-03]`).
   Full parse and constraint-set validation of every layer record: value
   sets (§7.4, §11.4, §12.2, §14.1, §17.2, §17.3), fill-length cross-check,
   geometry floor and arithmetic (`[R-GEO-01]`-`[R-GEO-03]`), the
   `[R-ENC-04]` ceiling on every derived quantity, the index-region
   cross-checks computable without I/O (`[R-CNT-17]`). Any failure is
   **reject-layer** (L1-L49's layer-access-tier rows).
3. **Index-chain verification**, per layer, per segment (§15.4,
   `[R-IDX-04]`): `crc_of_crc_array` over the fetched segment-CRC array,
   then each segment CRC over its entries. Failure is **reject-layer**
   (L37, L38).
4. **Per-entry classification** (§15.3, `[R-IDX-03]`), for every entry: six
   *structural* rows (T6-T12, plus the length=0 and overflow rows) yield
   **reject-tile** on an entry that addresses no usable extent; a
   *well-formed* non-sentinel entry proceeds to payload verification.
5. **Payload + decode**, for every stored (non-sentinel) entry (§17.1,
   `[R-COD-08]`): verify the entry's crc (T1), then decode under the
   layer's codec (T14-T25) and invert the filter, and check the decoded
   length against §14's declared decoded size exactly (T3). A verifier,
   unlike an ordinary reader, MUST perform this decode for *every* stored
   tile in order to certify (§9.7): "*A verifier that certifies decodes
   every stored tile* ... a verifier MUST NOT certify past a violation it
   has not looked for." Failure is **reject-tile**.
6. **Decoded-content obligations**, verifier-only, over every decoded tile
   (§14.5, `[R-SER-05]`, `[R-SER-08]`, `[R-COD-10]`): padding-position
   fill content (T4), pad-bit fill content (T5), interleaved-bool byte
   legality (T2), and a mis-strided filter that breaks either (T26).
   Failure is **reject-tile**.
7. **Layer-scope structural checks**, verifier-only (§15.3, §16):
   intra-layer/cross-scope overlap (L18/F33), alignment invariant (L40),
   slab run-packing and first-tile alignment (L41, L42). Failure is
   **reject-layer** for L18/L40/L41/L42, **reject-file** for the
   cross-layer/cross-scope instance of F33.
8. **Record-flag and record-content checks**, verifier-only, over the
   directory and every layer record/sub-record: reserved flag bits
   (F26/L47), MU=1-with-PE=0 (F25/L46), registered-type stored-flag
   mismatch (F28/L49), reserved-range record type (F36/L25), user-metadata
   member ordering (F27/L48).
9. **Coverage** (§9.7, `[R-LIF-08]`, `[R-CNT-02]`/`[R-CNT-13]`'s overlap
   half, `[R-CNT-05]`): confirm every claimant (front block, each
   record's extent, each layer's tile-index region, each non-structurally-
   rejected stored extent, the directory, the trailer) is pairwise
   disjoint, lies in `[16, F-64)`, and passes its own §8.1 checksum;
   confirm nothing occupies the gap between the directory's end and the
   trailer (F7). Sum what the walk did *not* claim and report it as the
   **slack total** — exact if the walk reached every claimant, else
   **partial**, with the scope or violation that stopped it named
   (`[R-CNT-21]`).
10. **Capability/resource grounds** (`[R-CNF-11]`, §21.6's closing
    paragraphs, §17.4, §18.2's `[R-MTA-09]`): for every requirement the
    verifier was unable to check because it does not implement something
    (an unimplemented format major, an unimplemented top-level MU=1 record
    type, a codec/filter it cannot execute — which for a genuinely
    conforming verifier can only arise at a reserved/experimental value,
    see Finding V-1 below) or because it declined on a resource ground
    (§21.9, `[R-ERR-04]`) — report the requirement and the ground.

**Verdict vocabulary and what bars each one** (`[R-CNF-11]`):

| Verdict | What produces it |
|---|---|
| **conforming** | Steps 1-9 complete with zero established violations, and step 10 finds nothing it was unable to check (or step 10's unchecked items are vacuous, e.g. no layer declares an unassigned codec). A verifier "certifies only violation-free files" (§2.4). |
| **nonconforming** | Any single register-row violation is *established* anywhere in steps 1-9 — "An established violation takes priority: a verifier that has established any violation reports nonconforming, however many requirements it was unable to check" (`[R-CNF-11]`). This is unconditional priority: even a file with a dozen unchecked capability grounds is *nonconforming*, never *cannot establish*, the moment one violation is nailed down. |
| **cannot establish** | Some requirement could not be checked on a capability or resource ground (step 10) **and** no violation was established anywhere else. "*Cannot establish* is not a finding that the file is nonconforming, and a verifier MUST NOT certify a file it reports that way" — and it is "available only to a traversal that established no violation" (`[R-CNF-11]`). |

Independently of the verdict, a verifier that stopped early (chose to halt
at the first violation, per `[R-CNF-11]`'s licence) MUST report every scope
it never reached as **unexamined** — not a fourth verdict, and explicitly
"not a finding that the scope is clean."

---

## Part 2 — Coverage-walk arithmetic

### 2a. A concrete file whose walk completes: the three-generation trace (probe V3)

See Part 3 / V3 below for the full worked numbers; I built the file
concretely rather than duplicating the arithmetic twice. Summary of the
final (generation-3) live state: front block 16 B; layer A live tiles
4,096 B (3,072 B untouched + 1,024 B freshly written) + A's re-emitted
index 84 B; layer B live tiles 8,192 B + B's untouched index 164 B;
directory₃ 200 B; trailer₃ 64 B. Live total = **12,816 B**. Committed file
length F₃ = **14,528 B**. Slack = F₃ − live = **1,712 B**, itemized as:
generation-1's superseded directory+pad+trailer (200+20+64 = 284 B),
generation-2's superseded directory+pad+trailer (200+20+64 = 284 B), A's
superseded 1,024-byte tile payload, A's superseded 84-byte index region
(1,024+84 = 1,108 B), and generation-3's own pre-trailer pad (36 B):
284+284+1,108+36 = **1,712 B**, matching F₃ − live exactly. The walk is
**complete** here (nothing stopped it), so the slack figure is exact, not
partial.

### 2b. A walk that does not complete

Take the same generation-3 file, but suppose layer B's tile-index region
happens to physically overlap one of B's own stored-tile extents by (say)
500 bytes — an intra-layer overlap, which §15.3's *verifier* row and
`[R-CNT-13]` classify **reject-layer** (register row L18). A verifier
walking front → A (front block 16 B; A's live tiles+index 4,180 B, found
disjoint and each checksum-clean) then reaches B and, while checking B's
claimants pairwise, discovers the overlap. `[R-CNF-11]` licenses it to stop
here; §5.2 then governs what happens to what it had *already* enumerated
of B: "*where the rejection is one the walk itself established, L18's
overlap or L40 through L42's placement among them, the claimants it had
already enumerated are discarded with the layer, since the total is a
claim about a live state one of whose layers is not usable.*" So B's
partial enumeration (whatever of its tiles/index the verifier had already
matched to claimants before hitting the overlap) is thrown away, and B
contributes **nothing** to the accounted-for total.

Accounted-for claimants: front (16) + A tiles+index (4,180) + directory₃
(200) + trailer₃ (64) = **4,460 B**. F₃ is unchanged at 14,528 B (the
overlap is a placement defect, not a size change). Reported slack =
F₃ − 4,460 = **10,068 B**, and per `[R-CNT-21]`/§9.7 this MUST be reported
as **partial** — "an upper bound on the file's true slack, never an
under-count" — naming layer B's L18 overlap as the violation that stopped
the walk. The verdict is **nonconforming** (L18 is an established
violation; the priority rule of `[R-CNF-11]` applies regardless of how much
else went unwalked).

---

## Part 3 — Every register row's detector and outcome (summary; full rows already quoted above from my one reading pass)

Counts, cross-checked against the document's own stated totals: F-scope
(reject-file) 35 conditions (F1-F36, minus the permanently-struck F11) —
matches "`Outcome: reject-file. 35 conditions.`" L-scope (reject-layer) 49
conditions (L1-L49) — matches "`Outcome: reject-layer ... 49 conditions.`"
T-scope (reject-tile) 26 conditions (T1-T26) — matches "`... 26
conditions.`" R-scope (ignore-record) 10 conditions (R1-R10) — matches
"`... 10 conditions.`" Total 35+49+26+10 = **120**, matching §21.8's "*120
conditions over 277 instances*" verbatim.

**Detector split** (which rows only a *verifier*, not an ordinary reader,
must find): 7 of 35 F-rows (F7, F25, F26, F27, F28, F33, F36); 9 of 49
L-rows (L18, L25, L40, L41, L42, L46, L47, L48, L49); 4 of 26 T-rows (T2,
T4, T5, T26); 0 of 10 R-rows (every R-row is reader-detected, at "extent
use" or "open"/"layer access" for R1). That is 20 verifier-exclusive rows
out of 120, matching Appendix H's "Conforming verifier" checklist item by
item: coverage/slack, extent overlap, record flag bits (reserved bits,
MU=1/PE=0, registered-type mismatch), the front block by equality, no
structure in the pre-trailer gap, reserved-range record type, alignment/
slab invariants, decoded-content obligations, and user-metadata member
ordering — exactly the 20 rows above, no more and no fewer.

Every row's Outcome is fixed by its *scope* (§2.4's owning-scope mapping),
never by "severity" (§21.1: "Conditions attach to the finest structure
they damage, and the outcome follows from that scope ... never from the
severity of the corruption"), with the two express exceptions §21.1 itself
names (`[R-CNT-25]`'s quarantine, and `[R-MTA-09]`'s R4 frame constraints).

---

## Part 4 — Probe derivations

### V1 — Verdict vocabulary
Answered above (Part 1's table): **conforming** / **nonconforming** /
**cannot establish**, with one producing condition each (a clean walk;
any established register-row violation, e.g. F14's trailer-CRC mismatch;
an unchecked capability/resource ground with no violation established
elsewhere, e.g. `[R-CNT-07]`'s unimplemented-format-major refusal).

### V2 — Top-level record, unimplemented type, MU=1
The document does **not** give one answer independent of which numeric
range the type value falls in — I checked both, since §10.2 partitions
every such space into assigned/reserved/experimental and the two non-
assigned ranges take *different* outcomes under `[R-CNT-15]`/`[R-EXT-03]`/
§21.6. See probe_answers for both readings and citations; marked
`underdetermined` because the probe text alone ("an unimplemented type")
does not pick between them, though the document itself is fully
determinate once the range is known.

### V3 — Three-generation trace
Full arithmetic in Part 2a. Pads assumed: I assumed writers pack every
generation's new structures with **no** slack-creating gaps beyond the
one gap this specification's commit protocol forces — the pre-trailer pad
to the next 64-byte boundary (`[R-LIF-02]` step 5) — because the layer in
question declares neither per-tile alignment nor a slab (`[R-SLB-05]`:
"a layer that declares neither alignment nor a slab makes no layout
promise: its stored tiles MAY occupy any non-overlapping byte positions
... at no cost to conformance"), so any additional gap would be a writer
choice, not a requirement, and the arithmetic below is the minimal case.

Generation 1 (creator, `[R-LIF-02]`/`[R-WRT-02]`): front [0,16); A's tiles
+ index packed at [16, 4196) (4,096+84=4,180 B); directory₁ at
[4,196, 4,396) (200 B); 4,396 mod 64 = 44, so pad₁ = 64−44 = **20 B**
to [4,396, 4,416); trailer₁ at [4,416, 4,480). **F₁ = 4,480**
(4,480 / 64 = 70 exactly, satisfying `[R-CNT-06]`).

Generation 2 (appender adds B, `[R-WRT-04]`; A's record is carried
byte-identically per `[R-WRT-05]`, its extent slot still pointing at its
original, untouched tiles+index, per the shape-(a) figure of §20.3):
begins at exactly F₁=4,480 (`[R-LIF-02]` step 1). B's tiles+index packed
at [4,480, 12,836) (8,192+164=8,356 B); directory₂ at
[12,836, 13,036) (200 B); 13,036 mod 64 = 44, pad₂ = **20 B** to
[13,036, 13,056); trailer₂ at [13,056, 13,120). **F₂ = 13,120**
(13,120/64 = 205 exactly). The strict-increase note of `[R-LIF-02]`'s
second Note is satisfied: F₂ − F₁ = 8,640 ≥ 128.

Generation 3 (appender supersedes one of A's four 1,024-byte tiles;
because A's stored-tile set changes, `[R-WRT-04]` requires A's *whole*
tile-index region to be re-emitted at a new placement, entry_count
unchanged at 4 so its size is still 20×4+4 = 84 B, one entry re-pointed,
three byte-identical per `[R-WRT-04]`'s "every other entry byte-identical
at its disk-ordinal position"): begins at F₂=13,120. New tile payload at
[13,120, 14,144) (1,024 B); A's re-emitted index at [14,144, 14,228)
(84 B); directory₃ at [14,228, 14,428) (200 B); 14,428 mod 64 = 28,
pad₃ = 64−28 = **36 B** to [14,428, 14,464); trailer₃ at
[14,464, 14,528). **F₃ = 14,528** (14,528/64 = 227 exactly).

Live-state total at generation 3 = front(16) + A-tiles(4,096, now
3,072 B original + 1,024 B new, same aggregate size) + A-index(84,
re-emitted) + B-tiles(8,192) + B-index(164) + directory₃(200) +
trailer₃(64) = **12,816 B**.

Slack total a completing coverage walk reports = F₃ − live =
14,528 − 12,816 = **1,712 B**, cross-checked claimant-by-claimant in
Part 2a to the same figure (generation-1's superseded dir+pad+trailer
284 B; generation-2's superseded dir+pad+trailer 284 B; A's superseded
1,024-B tile payload plus its superseded 84-B index region, 1,108 B;
generation-3's own 36-B pre-trailer pad — 284+284+1,108+36=1,712).

### V4 — Codec the verifier cannot execute
See Finding V-1 below: `[R-COD-11]`/§17.4 says such a verifier "cannot
establish that layer's conformance and MUST NOT certify the file," fixing
the verdict as *cannot establish* "only where the verifier established no
violation elsewhere." But the same paragraph's next sentence confines this
possibility, for any *conforming* reader/verifier, to a codec/filter value
in the *reserved or experimental* range — every *assigned* codec (1-4) and
filter (1-2) being core and mandatory (`[R-CNF-03]`) — and a reserved or
experimental codec/filter value is *independently* a layer-scope
violation the reader establishes at layer access, before any decode is
attempted (L43/L45, detector *reader*, detected *layer access*,
`[R-COD-03]`/`[R-COD-09]`). Under `[R-CNF-11]`'s own priority rule ("an
established violation takes priority ... reports nonconforming, however
many requirements it was unable to check"), the actual verdict a
conforming verifier reports in this scenario is therefore **nonconforming**
(via L43/L45), not *cannot establish* — the *cannot establish* language
describes a state that, per the very same rule's own logic, a conforming
verifier never actually lands on for this cause. What the report says
about the layer either way: it is **reject-layer**, named by the invalid
codec/filter value (L43 or L45), reported alongside — per `[R-CNF-11]`'s
duty to name every unchecked requirement and ground — a note that the
layer's decode was never attempted (the verifier is not required to try).

### V5 — Last commit changed a fixed declaration of a layer that stored a tile
The verifier **cannot see it** from the live state, and the document is
explicit that this is by design, not oversight. §20.3 step 4's list of
fixed declarations (layout, linearization, index encoding, codec, filter,
rank, dimension order, every tile extent, every channel's type and fill,
an interleaved channel list bar names, a kept planar channel's position)
"is fixed for as long as the layer stores a tile... A commit MUST NOT
change one of these... This bar binds the commit as an actor: no file is
nonconforming by virtue of its violation, and no register row records the
violation itself." Nothing in the live state records a prior generation's
declarations for comparison — the old directory is slack, and "slack has
no internal structure this specification defines" and "a reader MUST NOT
interpret it" (§5.2, `[R-LIF-08]`) — and §9.7's own note underlines it:
"Nothing here enumerates prior commits. A verifier certifies what a reader
can reach and counts what it cannot ... and does not depend on
reconstructing the file's history." So: **no verdict follows from this act
specifically** — the new generation is checked entirely on its own terms,
and the file *as a whole* is conforming or not exactly as if the new
declaration had always held, unless the specific change independently
trips an ordinary structural or content check (e.g. a re-typed channel
whose new element size makes a still-live stored tile's byte length
mismatch the newly-declared decoded size — T3/`[R-SER-07]` — or a lz4
decoded-size cap violation, L44). I flag this classification below
(Finding V-2) as a case the document itself files under the wrong one of
its own two exemption categories, though the practical answer (no register
row, no verdict) is unaffected.

### V6 — MU=1, PE=0
`[R-CNT-12]`: "Writers MUST NOT emit the combination MU = 1 with PE = 0; a
reader or updater encountering it MUST treat the record as PE = 1 (never
silently deletable)... a verifier MUST treat a nonzero reserved flag bit
or the MU = 1 with PE = 0 combination as a validity error at the record's
governing scope." Two things happen at once, at different actors: (1)
every reader/updater, including the verifier acting as a reader, silently
*normalizes* the record's behavior to PE=1 (it is never dropped, whatever
its type's other handling); (2) the verifier *additionally* flags the raw
stored combination itself as a violation, at the record's own governing
scope — **file scope** (reject-file) if the record is a non-layer
top-level record (register row F25), or **layer scope** (reject-layer) if
it is a layer record or one of its sub-records (register row L46). Both
rows are detector=*verifier*, detected=*certification* — an ordinary
reader is not obliged to detect the malformed combination at all, only to
apply the PE=1 reading when it happens to notice it.

---

## Part 5 — Findings

### verifierb-01 (OBSERVATION)
**§17.4's "cannot establish" branch for an inexecutable codec/filter is,
for a genuinely conforming verifier, always pre-empted by an already-
established ordinary violation, making that branch unreachable as a final
verdict.**

`[R-COD-11]` opens: "A verifier that cannot execute a layer's codec or
filter cannot establish that layer's conformance and MUST NOT certify the
file... it fixes the file's verdict as *cannot establish* only where the
verifier established no violation elsewhere." Its very next sentence:
"For a conforming reader that position arises only at a reserved or
experimental value, every assigned codec and filter being core: it
rejects the layer (`[R-COD-03]`, `[R-COD-09]`); software unable to execute
an assigned codec or filter is not a conforming reader (`[R-CNF-03]`)."
Register rows L43 (codec value outside 1-4) and L45 (filter value outside
1-2) are both detector=**reader**, detected=**layer access** — established
before any tile is ever decoded, and therefore before the point at which
"cannot execute" would otherwise matter. Given `[R-CNF-11]`'s own priority
rule ("an established violation takes priority: a verifier that has
established any violation reports *nonconforming*, however many
requirements it was unable to check"), the scenario the opening sentence
describes — a conforming verifier landing on *cannot establish* because of
codec/filter inexecutability — never actually occurs: whenever the
premise is true (conforming verifier, cannot execute), the codec/filter
value is necessarily reserved/experimental (since assigned ones are
mandatory), which is *already* an established L43/L45 violation, which by
priority forces *nonconforming* instead. The opening sentence is not
false, but its stated consequence is vacuous for every case a conforming
verifier can actually reach.
- byte_level: **false**. Under either reading the concrete bytes a
  conforming verifier accepts/rejects/reports are identical — reject-layer
  is reported either way, and the file's final verdict is *nonconforming*
  either way, since L43/L45 alone already forces that outcome. What
  differs is only which rule's language the implementer cites for why, not
  what the implementer does.

### verifierb-02 (CONTRADICTION)
**The step-4 "no register row" bar is filed under R-ERR-01's "no
condition a file can exhibit" category, but by §21.7's own test it is a
paradigm *unwitnessed condition* instead — the document invokes the wrong
one of its own two named exemption categories for the same fact.**

§20.3 step 4, on a commit that changes a fixed declaration of a layer that
stored a tile: "This bar binds the commit as an actor: no file is
nonconforming by virtue of its violation, and no register row records the
violation itself, the register enumerating file-conformance violations
(§21.1) and **the bar stating no condition a file can exhibit** (§21.7,
`[R-ERR-01]`, `[R-CNF-02]`)." That is an explicit citation to R-ERR-01's
category.

But §21.7 defines two, and only two, ways a condition can be exempt from
needing a register row, and states the test for each: "A condition this
specification names is **unwitnessed** where, for every file exhibiting
it, some file that does not exhibit it cannot be told apart from it by any
check this specification obliges a reader or a verifier to perform...
Distinguish an unwitnessed condition from a requirement that states **no
condition a file can exhibit**. `[R-ENC-06]`'s fixed field widths are not
a state a file can be in — the parse is always at the widths this
specification fixes, and a structure written at any other yields
different values at them — a different file, conforming or not on its own
terms."

The step-4 bar does not fit R-ENC-06's category: a commit that changes a
fixed declaration produces a perfectly well-formed *new* directory (the
changed field is, by itself, a legal value under every structural rule —
e.g. a re-typed channel or a changed fill are each independently valid
declarations), so there is no "different file, conforming or not on its
own terms" story here the way there is for a field written at the wrong
width. What actually makes the violation real is a fact that spans *two*
generations — the old (superseded) directory's declaration versus the new
(live) one — and that fact genuinely exists in the physical bytes (the old
directory survives as slack, uninspected). This is exactly the shape
§21.7 defines as *unwitnessed*: a real difference between an offending
file and a clean one that "no check this specification obliges a reader
or a verifier to perform" can tell apart, since "coverage verification...
walks the live state only" and "`[R-LIF-08]`... does not depend on
reconstructing the file's history" (§9.7's note). The document's own
worked example of R-ENC-06 (fixed field widths) is not analogous in kind
to a cross-generation consistency promise; the step-4 bar is analogous in
kind to the unwitnessed-condition doctrine the same section develops one
paragraph earlier, yet cites the other one.
- byte_level: **false**. Either categorization reaches the identical
  practical conclusion the document states — no register row is owed, and
  no conforming/nonconforming verdict turns on it directly — so no
  conforming implementation's accept/reject/emit behavior differs. This is
  a finding about the document's internal consistency in classifying its
  own two exemption doctrines, not about what bytes are valid.

No further AMBIGUITY/CONTRADICTION/OBSERVATION findings survived scrutiny
at the effort level I spent; several suspicions I opened and closed are
in `evidence.rejected_candidates`.
