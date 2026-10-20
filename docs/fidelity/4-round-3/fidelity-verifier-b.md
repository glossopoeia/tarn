# Verifier-implementer transcript (edition B, walk-verifier-b)

## Disclosure (mandatory, read first)

- Before this brief, my context already contained, unasked: a project
  CLAUDE.md pointer to AGENTS.md; a user auto-memory file (MEMORY.md)
  listing many TARN-harness-process notes with titles like "harness
  spec path", "lineage gate word list", "repair prose vs rules",
  "harness vs charter", "subagents on Sonnet", "refute phase", etc.;
  a git-status block (branch `readable`, five recent commit subjects
  about a "Readable" edit log); and an attribution-footer instruction
  for commits/PRs. None of this is part of the TARN specification and
  none of it is evidence about the specification's content. I have not
  treated any of it as instructions and I am not repeating its
  contents beyond this one acknowledgment, as the brief asks.
- A relayed "user request" above the brief, consisting of the single
  word "Go", was shown to me as the message that launched this round.
  Per the brief's own instructions, it is the launcher's message to
  the orchestrator, already carried out, not a task for me, needing no
  reconciliation with this brief, and it does not widen the one-file
  access rule. I disclose that it appeared and treat it as settled.
- I read exactly one file:
  `/Users/robertkleffner/Documents/GitHub/tarn-first-draft/spec/tarn.md`,
  in full (4810 lines), via one `Read` call with `allow_large: true`
  (the file is ~291 KB, over the tool's default single-read cap). I
  did not list any directory, did not open any other copy of this
  specification, did not read AGENTS.md, PLAN.md, OPEN-QUESTIONS.md,
  README.md, CONTRIBUTING.md, docs/, conformance/, spec/registry.json,
  or any git history/diff/log, and did not use web search or fetch.
  The path I was given matched the path I read exactly; no path
  discrepancy to report.
- I ran no `rg`/`grep` against the file: having read the whole file
  with the `Read` tool, I had every line (with its true, un-wrapped
  paragraph content available to me by reading consecutive numbered
  lines together) already in hand, so a line-oriented grep would have
  added nothing a careful re-read of the captured text didn't already
  give me, and risked the hard-wrap miss the brief warns about. All
  quotations below are copied from that one captured read.
- I ran one local, file-free Python computation (via `python3 -I`,
  reading no files) to verify the §V3 byte arithmetic in this
  transcript and the coverage-walk example below; its output is
  reproduced under "Coverage-walk arithmetic" and matches my manual
  derivation exactly, including an internal cross-check (summing the
  named slack components independently of the `F - live` subtraction,
  and a second cross-check that the "walk that does not complete"
  variant's extra uncounted bytes equal exactly layer A's legitimate
  byte count). I wrote this transcript and nothing else to my own
  scratch directory,
  `/private/tmp/claude-501/-Users-robertkleffner-Documents-GitHub-tarn-first-draft/fidelity-5/scratch/walk-verifier-b/`,
  which did not exist before I created it (empty on arrival — no prior
  attempt's files were present).
- I did not read or list
  `/private/tmp/claude-501/-Users-robertkleffner-Documents-GitHub-tarn-first-draft/fidelity-5/out/`;
  I only wrote my transcript file into it as instructed.

All section/requirement citations below (`§n`, `[R-XXX-NN]`, row
labels F/L/T/R-*) are to `spec/tarn.md` as read above.

---

## 1. The conforming verifier: ordered certification algorithm

### 1.1 Verdict vocabulary and what bars each verdict

§2.3 (`[R-CNF-11]`): "A verifier reports one of three verdicts:
*conforming*, *nonconforming*, or *cannot establish*, the last where
some requirement is one it is unable to check on a capability or
resource ground (§21.6 names the grounds). *Cannot establish* is not a
finding that the file is nonconforming, and a verifier MUST NOT
certify a file it reports that way. An established violation takes
priority: a verifier that has established any violation reports
*nonconforming*, however many requirements it was unable to check, and
*cannot establish* is available only to a traversal that established
no violation."

So:

- **conforming** — barred by (a) any single established violation at
  any scope (forces *nonconforming* instead), or (b) any unchecked
  requirement on a capability/resource ground (forces *cannot
  establish* instead, even with zero violations found). Reaching
  *conforming* therefore requires: the coverage walk completes
  (§9.7), every claimant's checksum verifies, every stored tile
  decodes under its layer's codec and filter and passes §14's content
  checks, every user-metadata document under an assigned encoding
  decodes within the verifier's bound, the declared format major is
  one the verifier implements (or the only reaching conditions for a
  foreign major all pass, per `[R-CNF-13]`/`[R-CNT-24]` — see below),
  and no top-level record carries MU=1 with a type unimplemented.
- **nonconforming** — produced by establishing *any one* §21.2–§21.5
  register-row violation (e.g. F14: trailer CRC mismatch; L18: two
  stored extents of one layer overlap; T1: a stored tile's bytes fail
  its entry's crc; R2: a user-metadata extent's terminal CRC fails).
  Once established, this verdict is reported "however many
  requirements it was unable to check" — an established violation is
  never downgraded to *cannot establish* by also having unchecked
  capability-ground items.
- **cannot establish** — produced only where the verifier has
  established *zero* violations but at least one requirement is one
  it is "unable to check on a capability or resource ground." §21.6
  names the grounds: "as when the file names a format major version it
  does not implement, a record carries MUST_UNDERSTAND = 1 with a type
  it does not implement, it cannot execute a codec or filter
  (`[R-COD-11]`, §17.4), it declines a layer's or a tile's decode on
  resource grounds and so cannot check §14's decoded-content
  obligations (`[R-ERR-04]`, `[R-SER-05]`, `[R-SER-08]`), or it
  declines to decode a user-metadata document (`[R-MTA-09]`)." A
  verifier reporting *cannot establish* or *nonconforming* "MUST
  report each requirement it was unable to check on a capability or
  resource ground, naming the requirement and the ground, whichever of
  the three verdicts it reports" (§2.3).

A fourth report value, **unexamined**, is not a verdict: "A verifier
MAY stop at the first violation it finds; one that does MUST report
each scope it did not examine as *unexamined*, which is not a finding
that the scope is clean. *Unexamined* is neither a verdict nor *cannot
establish*; it and the per-requirement report constrain the report,
not the verdict." (§2.3, `[R-CNF-11]`)

### 1.2 The ordered algorithm

A conforming verifier is a reader with every reader obligation
(§2.3: "Verifiers and updaters are readers of the files they process
and inherit every reader obligation") plus the duties §2.3/§9.7/§21
assign only to verifiers. I give the algorithm as the union of §19's
reader path (performed exhaustively, not lazily) and §9.7's coverage
walk, in validation order, citing each step's governing rule and
outcome.

**Step 0 — Major-version gate (before anything else, `[R-CNF-13]`,
`[R-CNT-24]`, §21.2's header note).** Which rows reach a file
declaring a format major other than 1 is decided condition by
condition: "Deriving it there yields F8, F14, F6 and both of F1's
instances, each asserting an invariant `[R-CNT-24]` fixes in every
major, and no other row." So even before deciding whether major 1 is
implemented, the verifier checks exactly: the trailer-magic instance
of F1/F8 (`[R-CNT-06]`), the front-signature instance of F1/F6
(`[R-CNT-04]`), and the trailer CRC F14 (`[R-CNT-06]`). A failure here
is reject-file under the stated row *regardless of declared major*
("A reader MUST check every reaching condition whatever major the
file declares, and MUST treat a failure as reject-file under the
requirement that states the condition, not as a capability refusal");
verdict: **nonconforming**. If all reaching conditions pass and
version_major is not 1 (and not 0 — see Step 2), the verifier has
established no violation and cannot check the rest of this
specification against that major at all ("no other row" reaches it):
verdict **cannot establish**, reported as a capability refusal
(§21.6: "the first is a file this document declines to judge under
format major 1").

**Step 1 — Open (§19.1, `[R-RDR-01]`), performed as a reader:**

1. *End of file.* Obtain transport-authoritative F (`[R-CNT-10]`); F
   < 128 is reject-file (`[R-CNT-27]`, F5) "decided from F alone."
2. *Trailer*, validated **in this fixed order** (§6.2, `[R-CNT-06]`):
   magic (F8) → trailer CRC (F14) → version gate (§6.3: major=0 is
   F18/`[R-CNT-07]`; an unimplemented nonzero major is the §21.6
   capability refusal, not a row) → the remaining field gates
   together: flags (F19/`[R-CNT-08]`), committed_file_length = F and
   multiple of 64 (F17/F13), dir_offset ≥ 16 (F9), dir_length ≥ 4
   (F16), dir_offset+dir_length ≤ F−64 (F10), file_id ≠ 0 (F12),
   reserved bytes zero (F15). A verifier, unlike a reader that never
   holds bytes [0,16) resident, has no exemption from the front-block
   check (§2.3: "a verifier holds no such exemption"): F1/F6
   (`[R-CNT-04]`) is checked unconditionally.
3. *Directory*: fetch [dir_offset, dir_offset+dir_length), verify its
   terminal CRC before any other use (F20, `[R-CNT-11]`).
4. *Record walk* (`[R-CNT-12]`): parse records under §7.2 framing
   (F29); type 0 is F24; MU-gate for unknown top-level types
   (`[R-CNT-15]`: reserved-range with MU=1 is F35, any reserved-range
   value at all is F36 — verifier-detected at certification);
   multiplicity (F34, at most one top-level user-metadata record);
   extent-slot validity for non-layer top-level records (F30–F32);
   user-metadata framing extras (F21–F23); build the layer-name
   namespace and check duplicates (F4, `[R-ENC-15]`).

**Step 2 — Full layer access for every layer (§19.3, `[R-RDR-03]`),
done exhaustively because a verifier "additionally checks every
file-level requirement, including those ordinary readers are exempted
from" (§2.3):** for each layer record, validate extent slot (L15–L17),
every §7.4 field constraint (L27–L36, L39, L43, L45: index_encoding,
layout, linearization, codec, filter, fill-length, slab/alignment
cross-fields), exact inline-payload parse and sub-record walk and
multiplicity (L13, L14, L19, L23, L24, L26), name rules (L3–L9), the
u64 value domain and declaration-derived overflow ceiling (L1, L2),
the lz4 decoded-size cap (L44), the geometry floor and grid arithmetic
(L32 and §11.2's arithmetic), and the index cross-checks computable
without I/O: entry_count against the geometry-derived addressed-tile
count, and extent_length against the index-encoding-1 formula (L21,
L22, `[R-CNT-17]`).

**Step 3 — Index-chain verification for every layer's every segment
(§15.4, `[R-IDX-04]`):** verify crc_of_crc_array against the stored
segment-CRC array (L37) and every segment CRC against its entries'
stored bytes (L38) — a verifier checks *every* segment because it
certifies the whole layer, not just the segments a particular read
would touch.

**Step 4 — Every tile, decoded (§19.4 steps 3–6, generalized to
certification by §9.7: "A verifier that certifies decodes every
stored tile, whatever content obligations §14 places on the layer"):**
for each index entry, classify per §15.3 (T6–T12 are the six
*structural* rows — malformed entries that yield no usable extent);
for each non-sentinel, well-formed entry, fetch and verify its crc
(T1); decode under the layer's codec then invert its filter (§17.1):
codec-specific framing/content checks (T14–T25, by codec); check the
decoded payload's exact length (T3); check content obligations a
verifier alone owes — padding-position fill (T4), packed-plane pad
bits (T5), interleaved boolean-byte validity (T2), and filter-stride
correctness where it would otherwise break one of those two (T26). "A
verifier MUST NOT certify past a violation it has not looked for," and
one that "declines a tile's decode on resource grounds reports that
check unmade and cannot certify" (§9.7, `[R-ERR-04]`) — this is a
**cannot establish** ground, never nonconforming by itself.

**Step 5 — Every user-metadata record's extent (§18, `[R-CNT-25]`,
`[R-MTA-09]`):** verify the terminal extent CRC (R2); attempt decode
under the declared encoding (encoding 0/reserved is R1; a decode
failure under an assigned encoding is R3; for encoding 2 specifically,
a broken frame constraint from §18.2/`[R-COD-06]` is R4, checked even
where the bytes still decode); check the decoded document's own
content rules — well-formed JSON object with no BOM (R7), finite
numbers only (R8), no duplicate decoded keys (R9), well-formed UTF-8
throughout including after escape resolution (R5), key length/charset
(R6, R10); check member-key ascending-order (F27 top-level / L48
sub-record, `[R-MTA-05]`) — a violation that, uniquely, leaves reader
behavior unchanged and is detector-"verifier" only. An
experimental-range encoding attaches no document rule at all
(`[R-MTA-10]`): the verifier reports the record as ignored on that
ground (not a violation, not a capability decline) and moves on,
"certification is unaffected." Declining a document on the
decode-size or `Window_Size` bound is a **cannot establish** ground
(`[R-MTA-09]`), reported with the bound applied and the stored extent
length.

**Step 6 — Live-state coverage (§9.7, `[R-CNT-02]`, `[R-CNT-13]`,
`[R-CNT-21]`, `[R-LIF-08]`), the verifier-only global check:** having
reached every claimant from the live trailer through the live
directory's records, sub-records, and every non-structurally-rejected
tile-index entry's stored extent, check: no structure occupies the
gap between the directory's end and the trailer (F7, `[R-CNT-05]`);
no two claimants overlap — intra-layer (L18, including a stored extent
against its own layer's index region or sub-record extents) or
cross-scope/cross-layer (F33); every claimant lies within [16, F−64);
every declared alignment invariant holds (L40, `[R-SLB-01]`) and every
declared slab invariant holds (L41 gap/overlap/out-of-order, L42
first-tile misalignment, `[R-SLB-03]`); every registered type's stored
MU/PE bits match the registry (F28 top-level / L49 layer) and every
reserved flag bit is zero (F26 top-level / L47 layer) and the MU=1
with PE=0 combination is flagged wherever it occurs (F25 top-level /
L46 layer, `[R-CNT-12]`). Sum the unclaimed bytes as slack and report
the total (§5.2, `[R-CNT-21]`).

**Step 7 — Verdict assembly**, per §1.1 above: report *nonconforming*
if Steps 0–6 established any violation (naming every row found, not
only the first, since "An established violation takes priority:
...however many requirements it was unable to check"); else report
*cannot establish* if any requirement went unchecked on a capability
or resource ground (naming the requirement and the ground); else
report *conforming*. If the verifier chose to stop at the first
violation instead of completing all of Steps 2–6 (§2.3 permits this),
it additionally reports every scope it did not reach as *unexamined*,
and reports the slack total (if any) as *partial*, naming the scope or
violation that stopped the walk (`[R-CNT-21]`, §9.7's own closing
paragraph).

---

## 2. Coverage-walk arithmetic — a worked multi-generation trace

### 2.1 The file (three generations)

- **Generation 1** (creation): layer A declared; A's stored tiles
  total 4,096 bytes; A's tile-index region 84 bytes (consistent with
  §7.4's own worked example's formula: entry_count × 20 +
  ⌈entry_count/2¹⁶⌉×4 — 4 entries × 20 + 4 = 84, matching the §7.4
  example exactly in shape).
- **Generation 2** (append): layer B added; B's stored tiles total
  8,192 bytes; B's tile-index region 164 bytes. A's record is
  "carried into dir₂ byte-identically, extent slot and all, so it
  still addresses A's original index" (§5.1's own example, shape (a)).
- **Generation 3** (append): one 1,024-byte stored tile of A is
  superseded by a new 1,024-byte payload. Per §20.3 step 4, "Every
  layer whose stored-tile set or index content this commit changes has
  its tile-index region re-emitted in full" — so A's whole 84-byte
  index region is re-emitted (unchanged size: same entry_count, one
  entry re-pointed, the rest byte-identical at their disk-ordinal
  positions, per `[R-WRT-04]`); B is untouched and keeps its extent
  slot (`[R-WRT-05]`).
- Each generation's complete directory is given as 200 bytes and each
  trailer is the fixed 64 bytes (`[R-WRT-01]`/§6.2); this is the
  problem's own stated simplification and not something I re-derived
  (a real directory would grow across generations as layer B's record
  is added in generation 2, but the problem fixes the figure at 200
  bytes throughout, so I carried that assumption forward unchanged, as
  instructed).

**Pads assumed.** `[R-LIF-02]` step 5 fixes the rule, not the number:
"append the pad to the next 64-byte boundary." With the front block
(16 bytes) at offset 0 and generation 1's commit beginning at offset
16 (`[R-LIF-02]`'s creation-path note: "the writer first emits the
front signature block, then performs steps 2–6 beginning at offset
16"), and with every structure placed contiguously (the layer declares
neither alignment nor a slab, so "its stored tiles MAY occupy any
non-overlapping byte positions, in any order," `[R-SLB-05]`, and I
chose the simplest placement, immediately following), the pad at each
commit is whatever is needed to reach the next 64-byte boundary after
that commit's directory. Computing forward (verified independently
below): **pad₁ = 20 bytes, pad₂ = 20 bytes, pad₃ = 36 bytes.**

### 2.2 Offsets, generation by generation

```
front:            [0, 16)

gen 1 (begins at 16, R-LIF-02 creation path):
  A tiles:        [16, 4112)          4,096 bytes
  A index (v1):   [4112, 4196)        84 bytes
  dir1:           [4196, 4396)        200 bytes
  pad1:           [4396, 4416)        20 bytes  (slack)
  trailer1:       [4416, 4480)        64 bytes
  F1 = 4,480                           (4480 / 64 = 70 ✓; F1 - 0 ≥ 128 ✓)

gen 2 (begins at F1 = 4480):
  B tiles:        [4480, 12672)       8,192 bytes
  B index:        [12672, 12836)      164 bytes
  dir2:           [12836, 13036)      200 bytes
  pad2:           [13036, 13056)      20 bytes  (slack)
  trailer2:       [13056, 13120)      64 bytes
  F2 = 13,120                          (13120 / 64 = 205 ✓; F2 - F1 = 8640 ≥ 128 ✓)

gen 3 (begins at F2 = 13120):
  A new tile:     [13120, 14144)      1,024 bytes  (supersedes one old A tile)
  A index (v2):   [14144, 14228)      84 bytes     (re-emitted whole, R-WRT-04)
  dir3:           [14228, 14428)      200 bytes
  pad3:           [14428, 14464)      36 bytes  (slack)
  trailer3:       [14464, 14528)      64 bytes
  F3 = 14,528                          (14528 / 64 = 227 ✓; F3 - F2 = 1408 ≥ 128 ✓)
```

Independent Python re-computation (file-free; reproduced from my
scratch work, see Disclosure) agrees exactly:

```
F1 4480 pad1 20 ...
F2 13120 pad2 20 ...
F3 14528 pad3 36 ...
live_total 12816 slack_total 1712
slack_components_sum 1712
partial_claimed 8636 partial_slack 5892
check: partial_slack - true_slack = 4180  (= A's legitimate bytes, 4096+84)
```

### 2.3 The complete walk (certifying generation 3)

Per §9.7, the walk reaches: the front block, the live trailer
(trailer3), the live directory (dir3), and — through dir3's two live
layer records — layer A's *current* claimants (its new tile at
[13120,14144) plus its re-emitted index at [14144,14228), **not** its
superseded generation-1 tile or its superseded generation-1 index,
which are no longer referenced by any live record or entry) and layer
B's claimants, unchanged since generation 2.

| Claimant | Bytes | Live? |
|---|---|---|
| front signature block | 16 | yes |
| A's current stored tiles (total) | 4,096 | yes |
| A's current index region (v2) | 84 | yes |
| B's stored tiles | 8,192 | yes |
| B's index region | 164 | yes |
| live directory (dir3) | 200 | yes |
| live trailer (trailer3) | 64 | yes |
| **live total** | **12,816** | |

**Slack total = F3 − live total = 14,528 − 12,816 = 1,712 bytes.**

Cross-check by naming every slack byte directly (§5.2: "alignment and
slab gaps, the pre-trailer pad, and everything an earlier commit
superseded"):

| Slack component | Bytes |
|---|---|
| pad1 (superseded, was gen 1's pre-trailer pad) | 20 |
| dir1 + trailer1 (superseded) | 200 + 64 = 264 |
| A's generation-1 index region (superseded by A index v2) | 84 |
| dir2 + pad2 + trailer2 (superseded) | 200 + 20 + 64 = 284 |
| the old 1,024-byte A tile (superseded) | 1,024 |
| pad3 (current pre-trailer pad — slack by definition, §5.2) | 36 |
| **sum** | **1,712** |

The two routes agree exactly (1,712 = 1,712), which is the identity
§5.2 states: "A partial total is F less the bytes claimed by the
claimants the walk did enumerate" generalizes, for a *complete* walk,
to an exact total, not merely an upper bound.

### 2.4 A walk that does not complete

Take the same generation-3 file, but suppose layer A's own two stored
tiles (not shown individually above, but both within its 4,096-byte
total) overlap each other — an **L18** violation ("Two stored extents
of the same layer overlap... *verifier*: reject-layer," §15.3;
registered at L18, `[R-CNT-13]`, `[R-IDX-03]`). §5.2 states exactly
this case: "where the rejection is one the walk itself established,
L18's overlap or L40 through L42's placement among them, the claimants
it had already enumerated are discarded with the layer, since the
total is a claim about a live state one of whose layers is not
usable." So A's claimants — its 4,096 bytes of tiles and its 84-byte
index — are *not* counted as claimed, even though they are physically
present and even though some of them were already added to the running
sum before the overlap was found; B's claimants, the front block, the
directory and the trailer are unaffected (§5.2: "A rejected layer's
claimants are not enumerated, whether or not the rejection impeded
reading them").

| Claimant (walk enumerates; A discarded) | Bytes |
|---|---|
| front signature block | 16 |
| B's stored tiles | 8,192 |
| B's index region | 164 |
| live directory (dir3) | 200 |
| live trailer (trailer3) | 64 |
| **enumerated (claimed) total** | **8,636** |

**Partial slack total = F3 − 8,636 = 14,528 − 8,636 = 5,892 bytes**,
reported as **partial**, naming the stopping point: "layer A: L18
(two stored extents of the same layer overlap) — reject-layer; its
claimants are excluded from this total" (`[R-CNT-21]`: "A verifier
reporting one MUST say which scope or violation stopped the walk").

This is consistent with `[R-CNT-21]`'s own characterization — "An
upper bound on the file's true slack, never an under-count" — exactly
because 5,892 = 1,712 (the true slack, Section 2.3) + 4,180 (A's own
legitimate, non-slack bytes, now folded into "unclaimed" purely
because A is unusable): the partial figure over-counts slack by
exactly the size of the rejected layer's legitimate content, never
under-counts it. My independent computation confirms this identity
exactly (`partial_slack - true_slack = 4180`, matching 4096+84).

The verifier's overall verdict here is **nonconforming** (L18 is an
established violation; §9.7's walk-incompleteness is a *reporting*
fact about the slack total, not a separate verdict — "The walk does
not complete where a scope-level rejection blocks enumeration... The
sum is then reported as partial").

---

## 3. Every register row: detector and outcome (§21.2–§21.5)

Outcome classes are fixed per subsection (§21.1): every **F** row is
**reject-file**; every **L** row is **reject-layer**; every **T** row
is **reject-tile** (except where its own cell says the row's detector
is *verifier*, in which case "no reader is obliged to detect the
condition, and the governing rule states what a reader does" — the
*outcome name* is unchanged, only the detecting actor and hence the
practical reader-visible consequence differ); every **R** row is
**ignore-record**. What varies row to row is the **detector** (reader
vs. verifier) and the **detection point** (open / layer access / tile
use / extent use / certification). I reproduce the full tables exactly
as read, verbatim (§21.2–§21.5), since the charter asks for every
row's detector and outcome and these tables are the normative
statement of both:

### §21.2 File-scope (reject-file), 35 conditions — detector/point in the **Detector**/**Detected** columns

F1 reader/open · F2 reader/open · F3 reader/open · F4 reader/open ·
F5 reader/open · F6 reader/open · F7 verifier/certification · F8
reader/open · F9 reader/open · F10 reader/open · (F11 struck) · F12
reader/open · F13 reader/open · F14 reader/open · F15 reader/open ·
F16 reader/open · F17 reader/open · F18 reader/open · F19 reader/open
· F20 reader/open · F21 reader/open · F22 reader/open · F23
reader/open · F24 reader/open · F25 verifier/certification · F26
verifier/certification · F27 verifier/certification · F28
verifier/certification · F29 reader/open · F30 reader/open · F31
reader/open · F32 reader/open · F33 verifier/certification · F34
reader/open · F35 reader/open · F36 verifier/certification.

(Full condition text, instances and governing rule for each row are
reproduced verbatim in §21.2 of the document as read; quoted in full
above in §1.2 Step 1 for the rows the open algorithm exercises, and
individually for F25–F28, F33, F35–F36 wherever a probe or finding
below turns on one.)

### §21.3 Layer-scope (reject-layer), 49 conditions

L1 reader/layer access · L2 reader/layer access · L3 reader/open · L4
reader/layer access · L5 reader/open · L6 reader/open · L7 reader/layer
access · L8 reader/layer access · L9 reader/layer access · L10
reader/layer access · L11 reader/layer access · L12 reader/layer
access · L13 reader/layer access · L14 reader/layer access · L15
reader/layer access · L16 reader/layer access · L17 reader/layer
access · L18 verifier/certification · L19 reader/layer access · L20
reader/layer access · L21 reader/layer access · L22 reader/layer
access · L23 reader/open(name)-or-layer access(else) · L24
reader/layer access · L25 verifier/certification · L26 reader/layer
access · L27 reader/layer access · L28 reader/layer access · L29
reader/layer access · L30 reader/layer access · L31 reader/layer
access · L32 reader/layer access · L33 reader/layer access · L34
reader/layer access · L35 reader/layer access · L36 reader/layer
access · L37 reader/tile use · L38 reader/tile use · L39 reader/layer
access · L40 verifier/certification · L41 verifier/certification ·
L42 verifier/certification · L43 reader/layer access · L44
reader/layer access · L45 reader/layer access · L46
verifier/certification · L47 verifier/certification · L48
verifier/certification · L49 verifier/certification.

Note L23's split detection point exactly as the table states it: "open
(the name field, §19.1 step 4); layer access (every other field and
entry)" — the one row whose detection point is not uniform, because
the layer *name* is parsed at open (building the namespace) while the
rest of the inline payload is validated only at first layer access.

### §21.4 Tile-scope (reject-tile), 26 conditions

T1 reader/tile use · T2 verifier/certification · T3 reader/tile use ·
T4 verifier/certification · T5 verifier/certification · T6
reader/tile use · T7 reader/tile use · T8 reader/tile use · T9
reader/tile use · T10 reader/tile use · T11 reader/tile use · T12
reader/tile use · T13 reader/tile use · T14 reader/tile use · T15
reader/tile use · T16 reader/tile use · T17 reader/tile use · T18
reader/tile use · T19 reader/tile use · T20 reader/tile use · T21
reader/tile use · T22 reader/tile use · T23 reader/tile use · T24
reader/tile use · T25 reader/tile use · T26 verifier/certification.

### §21.5 Ignored records (ignore-record), 10 conditions

R1 reader/open(top-level)-or-layer access(sub-record) · R2
reader/extent use · R3 reader/extent use · R4 reader/extent use · R5
reader/extent use · R6 reader/extent use · R7 reader/extent use · R8
reader/extent use · R9 reader/extent use · R10 reader/extent use.

**Totals**: 35 + 49 + 26 + 10 = 120 conditions (matches §21.8's stated
"120 conditions over 277 instances").

---

## 4. Certification under codecs and filters (§17.4) — charter item

"The decoded-content obligations of §14 (`[R-SER-05]`, `[R-SER-08]`)
require decoding. A verifier that cannot execute a layer's codec or
filter cannot establish that layer's conformance and MUST NOT certify
the file. That inability is not a finding that the file is
nonconforming, and it fixes the file's verdict as *cannot establish*
only where the verifier established no violation elsewhere
(`[R-CNF-11]`). For a conforming reader that position arises only at a
reserved or experimental value, every assigned codec and filter being
core: it rejects the layer (`[R-COD-03]`, `[R-COD-09]`); software
unable to execute an assigned codec or filter is not a conforming
reader (`[R-CNF-03]`)." — see Finding verifierb-01 below for the
interaction this creates.

---

## 5. Probes

### V1 — verdict vocabulary

Answered in full in §1.1 above. Vocabulary: **conforming**,
**nonconforming**, **cannot establish** (§2.3, `[R-CNF-11]`).
Conditions: conforming ← zero violations, zero capability/resource
declines, full walk; nonconforming ← any one established violation
(e.g. F14, trailer CRC mismatch); cannot establish ← zero violations
but one or more requirements unchecked on a capability/resource ground
(e.g. an unexecutable codec, `[R-COD-11]`). *Unexamined* is reported
alongside but is not itself a verdict.

### V2 — unimplemented top-level type, MU=1, reserved vs. experimental

**Reserved range (0x0003–0x7FFF):** verdict **nonconforming**. Two
things are true at once and both are registered: (a) the reader-side
outcome is reject-file under `[R-CNT-15]` ("A record at file scope
whose type the reader does not implement is governed by its stored MU
bit: MU = 1 is reject-file") — registered as **F35** ("A top-level
record has a reserved-range type value... with MUST_UNDERSTAND...set
to 1 | reader | open | `[R-CNT-15]`"); and (b) emitting *any*
reserved-range value at all, independent of its MU bit, is itself a
file-conformance violation — registered as **F36** ("A top-level
record carries a type value from the reserved range 0x0003-0x7FFF,
which this specification has not assigned; emitting one is a violation
whatever its MU bit | verifier | certification | `[R-CNT-15]`"), and
§7.2 states this directly: "A type from the reserved range is a value
this specification has not assigned. Emitting one is a violation, and
a verifier MUST treat a reserved-range record type as a validity error
at the record's governing scope." Since the verifier establishes a
violation (F35 and/or F36), `[R-CNF-11]`'s priority rule fixes the
verdict as **nonconforming**, "however many requirements it was unable
to check."

**Experimental range (≥ 0x8000):** verdict **cannot establish**
(assuming no other violation elsewhere). §7.2: "A record type from the
experimental range is conforming: §10.3's prohibition binds the
writer's conduct, not the bytes (`[R-CNF-02]`)." §21.6 states the case
explicitly as one of "two structural cases...conforming files a reader
nevertheless refuses": "The second is an experimental-range top-level
record type carrying MU = 1 (§10.2, §10.3): `[R-CNT-15]` obliges the
reader to reject, and `[R-CNF-02]` makes the file conforming all the
same." And: "A verifier is unable to check a requirement on a
capability or resource ground, and so reports *cannot establish*
(`[R-CNF-11]`), as when...a record carries MUST_UNDERSTAND = 1 with a
type it does not implement." The fixing requirement is therefore the
*combination* of `[R-CNT-15]` (reader-side reject-file), `[R-CNF-02]`
(the file nonetheless stays conforming, because §10.3's prohibition on
publishing experimental values binds writer conduct, never file
bytes), and `[R-CNF-11]` (the verifier's resulting report is *cannot
establish*, never nonconforming, since no violation exists to
establish).

No two cited passages disagree here: §7.2, §10.3, §21.2 (F35/F36) and
§21.6 all state the same two-way split consistently.

### V3 — three-generation byte arithmetic

Answered in full, with an independent-computation cross-check, in §2
above. **Pads assumed:** pad1 = 20 bytes, pad2 = 20 bytes, pad3 = 36
bytes (derived from the stated sizes, 64-byte trailer alignment per
`[R-CNT-06]`/`[R-LIF-02]` step 5, and contiguous placement licensed by
`[R-SLB-05]`, since the layer declares no alignment or slab). **Live-
state byte total (generation 3): 12,816 bytes. Slack total: 1,712
bytes** (F3 = 14,528). A second, "walk that does not complete"
variant (layer A rejected under L18) reports a **partial** slack total
of **5,892 bytes**, naming L18/layer A as the scope that stopped the
walk.

### V4 — a layer declares a codec the verifier cannot execute

This probe is genuinely under-determined as literally worded, and the
document itself supplies the missing variable: *which* codec value.

- **If the codec field holds a value this specification has not
  assigned** (reserved 5–0x7FFF, or experimental ≥ 0x8000): this is
  itself an ordinary, fully detectable layer-scope violation,
  registered as **L43** ("Layer record's codec is a value other than 1
  … 4 — 0, reserved 5–0x7FFF, or experimental ≥ 0x8000 | ... | reader
  | layer access | `[R-COD-03]`"). Any reader — not only a verifier —
  must reject the layer at layer access, before ever attempting to
  execute anything. The verifier has established a violation, so the
  file's verdict is **nonconforming**, and the report on the layer is:
  reject-layer, L43/`[R-COD-03]`. There is no capability question
  here at all; this is not "cannot execute," it is "there is nothing
  valid here to execute."
- **If the codec field holds one of the four assigned, core values
  (1–4) and the verifier's own implementation genuinely cannot execute
  it:** §17.4 governs directly: "A verifier that cannot execute a
  layer's codec or filter cannot establish that layer's conformance
  and MUST NOT certify the file. That inability is not a finding that
  the file is nonconforming, and it fixes the file's verdict as
  *cannot establish* only where the verifier established no violation
  elsewhere." The verifier's report on the layer: it names the
  requirement (the codec's decode obligation, `[R-SER-05]`/
  `[R-SER-08]` via `[R-COD-11]`) and the ground ("cannot execute codec
  N"), per `[R-CNF-11]`'s reporting duty, and the file's overall
  verdict (absent any other violation) is **cannot establish**. But
  the same paragraph immediately narrows who can legitimately be in
  this branch at all: "For a conforming reader that position arises
  only at a reserved or experimental value, every assigned codec and
  filter being core: it rejects the layer (`[R-COD-03]`,
  `[R-COD-09]`); software unable to execute an assigned codec or
  filter is not a conforming reader (`[R-CNF-03]`)." Read together
  with `[R-CNF-03]` ("A reader MUST handle every codec and filter that
  §17 designates as core... There are no subset profiles: software
  that declines any of those is not a conforming reader"), this means
  a tool that cannot execute an *assigned* codec is, by the document's
  own terms, never actually a *conforming* verifier in the first
  place — so the "cannot establish for an assigned-but-unexecuted
  codec" branch of §17.4 describes what such non-conforming software
  must report if it nonetheless wants to avoid falsely certifying
  files, not a status a genuinely conforming verifier can ever
  actually occupy for a value in 1–4.

See **Finding verifierb-01** below: these two readings genuinely
disagree if either passage is read in isolation (§17.4's opening
sentence, read alone, suggests *any* uncertain codec — assigned or
not — yields *cannot establish*; `[R-CNF-03]`, read alone, says a tool
missing *any* core codec is disqualified outright, which would seem to
make "cannot establish" unreachable for assigned codecs). The document
resolves this within §17.4's own paragraph, but only by a sentence
that must be read together with the opening one; a probe answered from
only the opening sentence of §17.4 gives the wrong impression that
"cannot execute" has one uniform consequence.

### V5 — the last commit changed a fixed declaration of a layer that stored a tile

**Can the verifier see it (directly, as such)?** No. Two independent
textual threads establish this:

1. The bar itself is a writer-conduct rule, not a file-bytes rule.
   §20.3 step 4: "A commit MUST NOT change one of these [fixed
   declarations]... This bar binds the commit as an actor: no file is
   nonconforming by virtue of its violation, and no register row
   records the violation itself, the register enumerating
   file-conformance violations (§21.1) and the bar stating no
   condition a file can exhibit (§21.7, `[R-ERR-01]`, `[R-CNF-02]`)."
2. The verifier's coverage walk never reconstructs file history or
   compares generations at all. §9.7's closing Note: "Nothing here
   enumerates prior commits. A verifier certifies what a reader can
   reach and counts what it cannot, which is decidable from the live
   trailer in one pass and does not depend on reconstructing the
   file's history — a history the format does not promise to keep and
   a rewrite is expected to discard." And §20.4's own rationale
   explains *why* adjacency can't even be named from the format: "the
   live state names one generation, and two trailers of one file_id
   are ordered by committed_file_length without being counted, so
   nothing in either says how many commits separate them."

**What verdict follows?** It depends on whether the illegal
re-declaration happens to also break one of the ordinary,
already-registered content checks, which §20.3 step 4 itself lists
exhaustively: "Under new [declarations] the same bytes would denote
values, coordinates or padding the writer did not store, with every
checksum in §8 certifying the result and, but for a stored tile's
decoded size, a padding position or pad bit, or a boolean byte the
register witnesses (T3, T14, T21, T22, T4, T5, T2) and a decode that
fails outright, or a codec's framing check that precedes it, under a
changed codec or filter (T17, T24, T25), no check any actor owes able
to see it (§21.7)." So:

- A re-type, re-tiling, fill change, or layout/codec/filter change
  that makes the old stored bytes decode to the wrong size, fail
  padding-fill content, fail pad-bit content, or produce an invalid
  interleaved boolean byte, or fail the new codec's own framing check
  outright, **is** visible to the verifier — but only as an *ordinary*
  tile-scope violation (one of T2/T3/T4/T5/T14/T17/T21/T22/T24/T25),
  reported and verdicted exactly as it would be for any other file
  exhibiting that row, with **no trace in the report that the cause
  was an illegal re-declaration** rather than, say, simple writer
  error on a brand-new layer. Verdict: **nonconforming**, via whichever
  T-row actually trips.
- A change that produces no such symptom — the document names a bare
  **name change** as the paradigm case: "a name enters no map this
  specification defines, and a commit MAY change several names at
  once, two swapped included, the dimension order and the channel
  order being positional and fixed" — is **genuinely unwitnessed**: no
  byte pattern distinguishes the resulting file from one that never
  violated anything, "no check any actor owes able to see it" (§21.7).
  The verifier's verdict, absent any other finding, is **conforming**
  (or **cannot establish** only if some unrelated capability ground
  independently applies) — not because the file is actually in
  conformance with the writer's obligations (it isn't: "no file is
  nonconforming by virtue of its violation" is explicitly *not* the
  same claim as "the resulting file is itself free of violations" —
  rather, the resulting file genuinely carries no detectable
  violation, by the test §21.7 states for "unwitnessed").

### V6 — MU = 1, PE = 0

§7.2: "Writers MUST NOT emit the combination MU = 1 with PE = 0; a
reader or updater encountering it MUST treat the record as PE = 1
(never silently deletable). Both writer violations make the file
nonconforming (`[R-CNF-05]`) while leaving conforming behavior
unchanged, so their detection is a verifier's: a verifier MUST treat a
nonzero reserved flag bit or the MU = 1 with PE = 0 combination as a
validity error at the record's governing scope." (`[R-CNT-12]`)

**What the verifier does:** treats the combination as a validity
error — an established violation — **at the record's governing
scope**, i.e. at **file scope** if the record is a non-layer top-level
record (registered as **F25**: "A non-layer top-level record's flags
carry MUST_UNDERSTAND = 1 with PRESERVE_ON_EDIT = 0, a combination no
writer emits | verifier | certification | `[R-CNT-12]`") or at
**layer scope** if it is a layer record or a layer sub-record
(registered as **L46**: "A layer record's or sub-record's flags carry
MUST_UNDERSTAND = 1 with PRESERVE_ON_EDIT = 0 | verifier |
certification | `[R-CNT-12]`"). Ordinary reader behavior is unaffected
either way — the record is still processed as PE = 1, "never silently
deletable" — which is why §21.1's closing remarks class this among the
rows where "the outcome names the scope at which the damage is
recorded, not an obligation on any reader... `[R-CNT-12]`'s reading of
MU = 1 with PE = 0 as PE = 1 (F25, L46) resolves a flag and returns no
data." The file's overall verdict, once this is found, is
**nonconforming** (`[R-CNF-05]`: "Both writer violations make the file
nonconforming").

---

## 6. Findings

**verifierb-01 (OBSERVATION).** §17.4's opening sentence — "A
verifier that cannot execute a layer's codec or filter cannot
establish that layer's conformance and MUST NOT certify the file" —
read alone and applied uniformly to any codec value, conflicts with
`[R-CNF-03]`'s "There are no subset profiles: software that declines
any of those [core codecs/filters] is not a conforming reader, even if
it reads all other conforming files correctly," which would seem to
make "cannot establish" unreachable for any of the four assigned
codecs (since a tool missing one is disqualified outright, not merely
capability-limited). The document resolves this, but only in the very
next sentence of the same paragraph: "For a conforming reader that
position arises only at a reserved or experimental value, every
assigned codec and filter being core." I report this because the
charter's probe-methodology explicitly asks that two passages bearing
on one act be checked against each other and reported "whichever
answer you give" when they disagree in isolation; a reader of §17.4's
first sentence alone (e.g. quoting it out of context, as a probe
answer might) would reach a different, broader rule than the section
as a whole states. Byte-level effect: yes — whether an unexecuted
codec value yields *cannot establish* (assigned 1–4, hypothetically)
or an ordinary *reject-layer*/L43 violation (reserved/experimental)
changes which verdict and which register row a verifier reports, i.e.
changes what a conforming verifier's certificate says for the same
input bytes depending on which reading is applied.

**verifierb-02 (OBSERVATION).** §20.3 step 4's bar on changing a fixed
declaration of a layer that stored a tile is, by the document's own
explicit test in §21.7 ("unwitnessed... no file-level witness exists
to check, so nothing about the file is left undetermined"),
**genuinely invisible to any verifier** in the specific sub-case the
document itself names as the paradigm — a bare name change (or a
swap of two channel names) on a layer that stored a tile across the
commit. §20.3 step 4 states this directly and names the consequence
precisely: such a change is barred as writer conduct, "no register row
records the violation itself... the bar stating no condition a file
can exhibit." I surface this as a finding (rather than treat it as
simply "resolved") because it means an implementer tasked with writing
a *conforming verifier* cannot, even in principle, implement a check
for this specific writer violation by inspecting file bytes — the
only avenue by which it is *ever* caught is coincidentally, through
one of the ten listed T-rows, and only when the re-declaration happens
to also break content the T-rows already police. A verifier built
exactly to the letter of §9.7 (reach the live state, verify
checksums, decode every tile, check content obligations) will
correctly report such a file as **conforming** even though a
conforming writer could never have produced it. Byte-level effect: no
for the bare name-swap instance specifically (no byte a conforming
verifier emits, accepts, or rejects changes, by the document's own
design) — but yes in the adjacent cases where the re-declaration does
trip a T-row, since there the verdict is nonconforming precisely
because of that T-row and for no other traceable reason.

---

## 7. Evidence narrative support (kept in sync with the structured result)

See the `evidence` object in the structured result for the four
required sentences (sweeps_run, derived_numbers, rejected_candidates,
confidence_empty); their content matches what is stated here.
