# Verifier-implementer transcript — edition A

## Disclosure

- A line above this brief, labelled by the harness as the relayed user
  request, read only "Go." I note its appearance and treat it as the
  launcher's own message, carrying no task content and no widening of the
  access rule below.
- My context also carried, unasked, a project CLAUDE.md pointer, a long
  auto-memory index (entries about a "TARN harness", gate word lists,
  preflight checks, repair passes, etc.), a git status block, and an
  attribution/model-identity reminder. None of this is part of the
  specification and none of it is evidence about the specification; I have
  disregarded its contents entirely (I have not opened, searched, or relied
  on anything it names) and record only that it appeared, per the brief's
  instruction.
- Per the access rule, I read exactly one file:
  `/Users/robertkleffner/Documents/GitHub/tarn-first-draft/scratch/cleanroom/editions/a/tarn.md`
  (5004 lines, 303,815 bytes). It is at the path the brief names — no
  discrepancy to report. I opened no other file, ran no `ls` on sibling
  directories, consulted no ADR, no PLAN.md, no registry, no git history,
  and did no web search or fetch.
- Tools used: the `Read` tool, in sequential chunks, to read the entirety of
  `tarn.md` (I did not use line-oriented `grep` for prose search, given the
  brief's warning about hard-wrapped text; I did use `grep -n` once, purely
  to list section headers by `^#` markers, which do not wrap, and once more
  as a sanity check that single-word greps — e.g. `verifier` — are safe
  against wrapping, confirmed against a known multi-line phrase
  ("Conforming verifier") that *did* wrap across the lines it spans in the
  Read output). All arithmetic for V3 (byte totals, offsets, pad sizes) was
  done by hand/in my own working notes file, reading no other file.
- My scratch directory, `/private/tmp/claude-501/-Users-robertkleffner-Documents-GitHub-tarn-first-draft/fidelity-5/scratch/walk-verifier-a/`,
  was empty when I started (I `ls -la`'d it to create it and confirm). I
  wrote one working file there, `arithmetic-notes.md`, holding the V3 byte
  arithmetic; nothing else lives there. I did not read or list the output
  directory `/private/tmp/claude-501/-Users-robertkleffner-Documents-GitHub-tarn-first-draft/fidelity-5/out/` beyond writing this one file to it.
- Confidence: high on the register, the verifier's defined obligations, and
  the worked arithmetic, all of which the document states explicitly and
  in detail. Lower (medium) on the few places I flag as document gaps,
  since those turn on reading the whole of a long, cross-referencing text
  correctly rather than on any one clean quotation.

---

## 1. The verifier's certification procedure, as an ordered algorithm

### 1.1 Verdict vocabulary

Exactly three verdicts exist (§2.3's Conforming-verifier definition):

- **conforming** — every file-level requirement is satisfied; the verifier
  "certifies only violation-free files" (§2.4) and "MUST NOT certify a file
  it reports [cannot establish]" otherwise.
- **nonconforming** — the verifier has established at least one violation.
  "An established violation takes priority: a verifier that has established
  any violation reports *nonconforming*, however many requirements it was
  unable to check" (§2.3).
- **cannot establish** — "the last where some requirement is one it is
  unable to check on a capability or resource ground" — named examples: an
  unimplemented format major, a record with MUST_UNDERSTAND = 1 at a type
  the verifier does not implement (§21.6), an unexecutable codec or filter
  (`[R-COD-11]`), a declined tile/layer decode on resource grounds
  (`[R-ERR-04]`, `[R-SER-05]`, `[R-SER-08]`), or a declined user-metadata
  decode (`[R-MTA-09]`). "*Cannot establish* is not a finding that the file
  is nonconforming... and is available only to a traversal that established
  no violation" (§2.3).

A fourth label, **unexamined**, is *not* a verdict: "*Unexamined* is
neither a verdict nor *cannot establish* — it constrains the report, not
the verdict" (§2.3). It marks a scope a verifier chose not to examine after
stopping at a first violation (`[R-CNF-11]`).

Whichever of the three verdicts is reported, the verifier additionally
"MUST report each requirement it was unable to check on a capability or
resource ground, naming the requirement and the ground" (§2.3) — this is
unconditional, not only for *cannot establish*.

### 1.2 The algorithm

A conforming verifier is a reader first (§2.3: "Verifiers and updaters are
readers of the files they process and inherit every reader obligation"),
so it runs the full reader path (§19) and *additionally* performs the
checks §19.2 exempts ordinary readers from. In order:

1. **Front signature block.** Unlike an ordinary reader, a verifier holds
   no residency exemption: "a verifier holds no such exemption" (F6's row;
   Appendix H's checklist: "`[R-CNT-04]` lets a reader not holding it
   resident defer or omit and §2.3 does not"). Verify bytes [0,16) by byte
   equality against the constant (§6.1). Mismatch → **nonconforming**
   (F1's front-block instance / F6, `[R-CNT-04]`).
2. **Trailer** (§6.2, step order fixed): magic, then trailer CRC, then the
   version gate (§6.3), then the remaining field gates (dir_offset,
   dir_length, the dir-bounds sum, committed_file_length vs. transport size
   and vs. a multiple of 64, file_id ≠ 0, reserved bytes zero). Any failure
   → **nonconforming**, scope file (F8–F19 as applicable); an
   unimplemented format major → **cannot establish** on that ground alone
   if nothing else is wrong (§2.3, §21.6).
3. **Directory.** Verify the directory-region CRC before parsing (F20,
   `[R-CNT-11]`). Parse the record sequence under §7.2's exact-parse rule
   (F29); apply the MU gate to unknown top-level types (F24, F35, F36);
   apply per-type multiplicity (F34); apply extent-slot validity to
   non-layer top-level records (F2, F3, F30–F33); build and uniqueness-check
   the layer-name namespace (F4, raw bytes, `[R-ENC-13]`); check the
   top-level user-metadata record's framing (F21–F23). Any failure →
   **nonconforming**, scope file.
4. **Reserved-flag and flag-mismatch sweep (verifier-only).** Over every
   top-level record: reserved bits 2–15 zero (F26); not MU=1∧PE=0 (F25);
   for a §7.3-registered type, stored MU/PE bits match the registry (F28).
   Any failure → **nonconforming**, scope file, *without* any reader-facing
   rejection (§21.1: "the outcome names the scope... not an obligation on
   any reader" for a verifier-detected row) — the verifier still processes
   the record under its fixed semantics while recording the finding.
5. **Pre-trailer gap.** No structure may occupy the bytes between the
   directory's end and the live trailer (F7, `[R-CNT-05]`); a failure here
   → **nonconforming**, file scope.
6. **Per layer, full layer-access validation** (§19.3, the reader tier),
   for every layer in the directory (a verifier does not get to skip layers
   a "request" never touches — it certifies the whole file): extent-slot
   validity (L1, L2, L15–L17), name well-formedness and uniqueness (L3,
   L4, L5–L9), sub-record framing and multiplicity (L10–L14, L19, L23,
   L24, L26), the §7.4 constraint set in full — layout, linearization,
   codec, filter, alignment/slab mutual exclusion, rank/channel-count
   floors, channel type and fill-length, index_encoding (L20, L27–L36,
   L39, L43, L45), the entry_count/extent_length cross-check (L21, L22).
   Any failure → **nonconforming**, scope layer (that layer only; other
   layers are unaffected per §2.4's reject-layer semantics, even though
   the *verdict* on the whole file is nonconforming).
7. **Verifier-only layer sweep.** Reserved sub-record type emitted at all,
   regardless of MU (L25); reserved/MU=1∧PE=0 and registry-mismatch flag
   checks on the layer record and its sub-records (L46, L47, L49);
   user-metadata member-ordering (L48, `[R-MTA-05]`).
8. **Index chain, per layer** (§15.4, `[R-IDX-04]`): crc_of_crc_array over
   the segment-CRC array (L37); each segment CRC over its entries as
   stored (L38). Failure → **nonconforming**, scope layer.
9. **Per-entry classification, every entry of every layer** (§15.3,
   `[R-IDX-03]`): the six *structural* rows (T6–T12 as instanced) and the
   stored-bytes-CRC row (T1). A structural defect contributes no stored
   extent to later steps; a CRC-only defect keeps its extent. Failure →
   **nonconforming**, scope tile (that tile only).
10. **Decode, every stored (non-sentinel, non-structurally-rejected) tile**
    (because certifying is defined to require it: "A verifier that
    certifies decodes every stored tile, whatever content obligations §14
    places on the layer... a verifier MUST NOT certify past a violation it
    has not looked for", §9.7). Apply codec then filter inverse; check
    exact length consumption (T3, T24); apply the codec-specific framing
    constraints (T14–T23, T25, depending on declared codec); check padding
    content, pad bits, and interleaved boolean bytes (T2, T4, T5, T26).
    Failure → **nonconforming**, scope tile. Inability to execute a
    declared codec or filter → **cannot establish**, scope that layer, if
    no violation has yet been established elsewhere (`[R-COD-11]`,
    §17.4) — "it fixes the file's verdict as *cannot establish* only
    where the verifier established no violation elsewhere."
11. **Extent-ownership (coverage) walk** (§9.7, `[R-CNT-02]`,
    `[R-CNT-13]`): from the live trailer, through the live directory, its
    records' extents, its sub-records' extents, and each non-structurally-
    rejected entry's stored extent, confirm every claimant lies in
    [16, F−64), no two overlap, and each verifies against the checksum
    §8.1 assigns it. An intra-layer overlap → **nonconforming**, scope
    layer (L18); any other overlap → **nonconforming**, scope file (F33).
    Sum the unclaimed bytes as the slack total; report it, or, if the walk
    did not complete, report it as **partial** (an upper bound) together
    with naming what stopped the walk, and report every scope not reached
    as **unexamined** (§5.2, §9.7, `[R-CNT-21]`, `[R-CNF-11]`).
12. **User-metadata content, every readable document** (file-scope and per
    layer): member ordering (F27, L48); for an *assigned* encoding, the
    document's own content rules (§18's R1–R10 family, reported as
    ignore-record, not as a bar to certification per se — "application
    metadata never obliges a reader to treat the structural data it
    annotates as unusable", §7.1); for an *experimental-range* encoding, no
    content rule attaches at all — the verifier instead *reports* the
    record (owning scope, encoding value, stored extent length,
    `[R-MTA-10]`) without that being a violation or a bar; a decline to
    decode on the size/window bound → **cannot establish**, scope the
    narrowest declining one (`[R-MTA-09]`), if no violation has been
    established elsewhere.
13. **Final verdict.** If any step above established a violation →
    **nonconforming**, regardless of how many other requirements remain
    unchecked. Else, if some requirement was left unchecked on a
    capability/resource ground → **cannot establish**. Else →
    **conforming**. In every case, report per-requirement the ones left
    unchecked and why, and (if the walk stopped early) which scopes are
    unexamined and that the slack figure is partial.

---

## 2. The register, by detector and outcome

The register (§21.2–§21.5) is, per §21.1, complete by construction: "a
*detectable* file-conformance violation this specification names and the
register omits is a defect in this document" — and I found none omitted in
my reading (120 rows: F1–F36 less struck F11 = 35; L1–L49 = 49; T1–T26 =
26; R1–R10 = 10; 35+49+26+10 = 120, matching §21.8's stated count exactly).

### 2.1 File scope — outcome reject-file (35 conditions, §21.2)

| Row | Condition (short) | Detector | Governing rule |
|---|---|---|---|
| F1 | signature byte-reversed (front block / trailer magic instances) | reader | `[R-ENC-02]` |
| F2 | u64 field > 2^63−1 | reader | `[R-ENC-03]` |
| F3 | declaration-derived sum overflows 2^63−1 | reader | `[R-ENC-04]` |
| F4 | duplicate layer name | reader | `[R-ENC-15]` |
| F5 | file below 128 bytes | reader | `[R-CNT-27]` |
| F6 | front block not byte-identical | reader | `[R-CNT-04]` |
| F7 | structure in the pre-trailer gap | verifier | `[R-CNT-05]` |
| F8 | trailer magic wrong | reader | `[R-CNT-06]` |
| F9 | dir_offset < 16 | reader | `[R-CNT-06]` |
| F10 | dir region runs past F−64 | reader | `[R-CNT-06]` |
| F12 | file_id = 0 | reader | `[R-CNT-06]` |
| F13 | committed_file_length not a multiple of 64 | reader | `[R-CNT-06]` |
| F14 | trailer CRC mismatch | reader | `[R-CNT-06]` |
| F15 | trailer reserved bytes nonzero | reader | `[R-CNT-06]` |
| F16 | dir_length < 4 | reader | `[R-CNT-06]` |
| F17 | committed_file_length ≠ transport size | reader | `[R-CNT-06]` |
| F18 | version_major = 0 | reader | `[R-CNT-07]` |
| F19 | an incompat-lane bit set | reader | `[R-CNT-08]` |
| F20 | directory CRC mismatch | reader | `[R-CNT-11]` |
| F21 | top-level user-metadata extent slot (0,0) | reader | `[R-CNT-25]` |
| F22 | top-level user-metadata extent_length < 5 | reader | `[R-CNT-25]` |
| F23 | top-level user-metadata inline_length ≠ 1 | reader | `[R-MTA-03]` |
| F24 | top-level record type = 0 | reader | `[R-CNT-12]` |
| F25 | non-layer top-level record MU=1∧PE=0 | verifier | `[R-CNT-12]` |
| F26 | non-layer top-level reserved flag bits set | verifier | `[R-CNT-12]` |
| F27 | file-scope user-metadata members unsorted | verifier | `[R-MTA-05]` |
| F28 | registered non-layer top-level record's stored flags ≠ registry | verifier | `[R-CNT-22]` |
| F29 | record header/payload overrun or residue | reader | `[R-CNT-12]` |
| F30 | extent slot half-zero | reader | `[R-CNT-13]` |
| F31 | extent_offset in 1–15 | reader | `[R-CNT-13]` |
| F32 | extent runs past F−64 | reader | `[R-CNT-13]` |
| F33 | cross-scope / cross-layer overlap | verifier | `[R-CNT-13]` |
| F34 | two top-level user-metadata records | reader | `[R-CNT-14]` |
| F35 | reserved-range top-level type, MU=1 | reader | `[R-CNT-15]` |
| F36 | reserved-range top-level type emitted (any MU) | verifier | `[R-CNT-15]` |

(F11 is struck — a permanently retired label, never reused, §21.2's note.)

### 2.2 Layer scope — outcome reject-layer (49 conditions, §21.3)

Reader-detected (at layer access, unless noted): L1–L17, L19–L24, L26–L36,
L39, L43, L45 (the full §7.4/§11/§12/§13/§16/§17 constraint sweep, name
rules, sub-record framing, entry_count/extent_length cross-check).
Reader-detected at tile use: L37, L38 (index-chain CRCs).
Verifier-only (at certification): L18 (intra-layer overlap), L25
(reserved-range sub-record type, any MU), L40 (alignment multiple), L41
(slab-run contiguity), L42 (slab-run first-offset alignment), L46
(MU=1∧PE=0 on a layer record/sub-record), L47 (reserved flag bits), L48
(user-metadata member order), L49 (registered type's stored flags ≠
registry).

### 2.3 Tile scope — outcome reject-tile (26 conditions, §21.4)

Reader-detected (at tile use): T1 (stored-bytes CRC), T3 (decoded length
mismatch), T6–T12 (sentinel/structural entry malformations), T13–T25
(codec framing: wrapper/multi-stream/dictionary/checksum/window/
content-size/consumed-length/malformed-stream, per codec 1–4).
Verifier-only (at certification): T2 (interleaved bool byte at a real
position), T4 (padding content), T5 (packed-bool final-byte pad bits), T26
(wrong filter stride surfaced through T2/T4).

### 2.4 Ignore-record — user metadata (10 conditions, §21.5)

All reader-detected: R1 (encoding 0 or reserved), at open (top-level) or
layer access (sub-record); R2 (extent CRC), R3 (decode failure), R4 (zstd
frame-constraint breaks under encoding 2), R5–R10 (document content rules
— UTF-8/surrogates, empty/control-code keys, non-object/non-JSON/BOM,
non-finite numbers, duplicate keys, key length) — all at extent use.

---

## 3. The coverage walk — concrete arithmetic

### 3.1 A complete walk: the three-generation file of probe V3

See full byte-by-byte derivation in my working notes
(`arithmetic-notes.md`, this run's scratch directory). Stated assumptions:
neither layer declares per-tile alignment (A=0) nor a slab (S=0) — nothing
in the probe's description says otherwise, and `[R-SLB-05]` leaves
placement otherwise unconstrained — so I assume tiles/index/directory are
written back-to-back with no internal gap, and the only gap per commit is
the pre-trailer pad rounding the directory's end up to the next 64-byte
boundary (`[R-LIF-02]` step 5, `[R-CNT-05]`), zeroed by advisory
(`[R-CNT-03]`), without affecting the totals either way. The front block is
16 bytes (§6.1); a layer's index-region size is
`entry_count × 20 + ⌈entry_count/2¹⁶⌉ × 4` (§7.4, `[R-CNT-17]`), which
backs out entry_count = 4 for layer A (84 bytes) and entry_count = 8 for
layer B (164 bytes), both single-segment. Per `[R-LIF-02]`, the first
commit begins writing at offset 16 and every later commit begins writing
at the prior F; per `[R-WRT-05]`, a layer the commit does not touch keeps
its extent slot pointing at its unmoved region; per `[R-WRT-04]`, a commit
that supersedes a stored tile re-emits that layer's *whole* index region
at a new placement.

- Gen 1 (creates A): F1 = 4,480 (pad 20).
- Gen 2 (adds B, A untouched): F2 = 13,120 (pad 20).
- Gen 3 (supersedes one 1,024-byte tile of A; A's index re-emitted whole;
  B untouched): F3 = 14,528 (pad 36).

**Live-state total: 12,816 bytes** = front(16) + A's live tiles(4,096,
3 at their original gen-1 offsets plus 1 new) + A's live index(84, gen-3's)
+ B's live tiles(8,192) + B's live index(164) + the live directory(200) +
the live trailer(64).

**Slack total: 1,712 bytes** = gen-1's directory+pad+trailer(284) + gen-2's
directory+pad+trailer(284) + gen-3's pad(36) + the one superseded
1,024-byte A tile + A's superseded gen-1 index region(84).

Check: 12,816 + 1,712 = 14,528 = F3. ✓ (also cross-checked by computing
slack as the itemized sum independently of F3 minus live-total, and getting
the same figure both ways — see working notes).

### 3.2 A walk that does not complete

Take the same gen-3 file, but suppose layer A's tile-index now exhibits an
intra-layer extent overlap (condition L18: "Two structures of one and the
same layer claim overlapping bytes in the live committed state" — verifier-
detected, reject-layer, `[R-CNT-13]`/`[R-IDX-03]`). A verifier walking the
directory reaches layer A first (directories carry records in whatever
order the writer chose; order carries no meaning, `[R-CNT-14]`, but a
depth-first per-record walk meets A before B here), establishes L18, and —
per `[R-CNF-11]` — MAY stop at this first violation rather than continuing
to walk layer B's claimants.

Enumerated before stopping: front(16) + A's tiles(4,096) + A's index(84) +
the live directory(200) + the live trailer(64) = **4,460 bytes**.
Reported slack = F3 − 4,460 = 14,528 − 4,460 = **10,068 bytes, reported as
partial** (`[R-CNT-21]`: "an upper bound on the file's true slack, never an
under-count"), naming layer A's L18 finding as what stopped the walk, and
reporting layer B's region as **unexamined** (distinct from "slack": B was
never looked at, not found empty). Note that this partial figure
(10,068) overstates the complete walk's true slack (1,712, from §3.1 on the
undamaged file) by exactly B's un-subtracted live bytes
(8,192 + 164 = 8,356): 10,068 − 8,356 = 1,712 — a concrete illustration of
`[R-CNT-21]`'s "never an under-count" property, since B's bytes are in
fact claimed (live), not slack, but the halted walk cannot know that and
so counts them toward the unclaimed figure.

---

## 4. Findings

### verifiera-01 — kind AMBIGUITY — §2.4 vs. §21.1 on what "reader outcome" means for verifier-only rows

**Location A:** §2.4, `[R-CNF-07]`: "Every detectable file-conformance
violation named by this specification is assigned exactly one **reader
outcome**: reject-file, reject-layer, reject-tile, or ignore-record."

**Quotation A:** "Every detectable file-conformance violation named by
this specification is assigned exactly one **reader outcome**:
reject-file, reject-layer, reject-tile, or ignore-record."

**Location B:** §21.1 (register-reading rules), the paragraph beginning
"For a row whose Detector is *verifier*..."

**Quotation B:** "For a row whose Detector is *verifier*, the outcome
names the scope at which the damage is recorded, not an obligation on any
reader."

**Detail.** §2.4 calls the four-way classification a "reader outcome" for
*every* register row without qualification. Read in isolation — which an
implementer skimming the conformance-vocabulary section first plausibly
would, since §2.4 precedes the register by over 3,000 lines — this says
every reject-file/reject-layer/reject-tile-labelled condition binds a
*reader* to refuse that scope. §21.1 then narrows this for the ~20 rows
whose Detector is *verifier* (F7, F25–F28, F33, F36, L18, L25, L40–L42,
L46–L49, T2, T4, T5, T26, R-family rows have no verifier rows): for those,
"the outcome names the scope... not an obligation on any reader" — a
reader that serves the data unchanged is still conforming (§21.1 cites
`[R-CNT-22]` and `[R-MTA-05]` by name as cases where the reader "serves it
unchanged"). An implementer building a reader from §2.4's definition and
the register's Outcome column alone — without reaching and correctly
applying §21.1's Detector-keyed carve-out — would wrongly reject scopes
(e.g. refuse to serve a layer whose stored MU/PE bits merely differ from
the registry, L49) that this document requires be served.

**Byte-level test.** Does this change what a conforming implementation
does? For a *reader*, yes if the ambiguity is resolved the wrong way: a
reader that treats every Outcome-column entry as its own obligation (not
reading §21.1's carve-out) would refuse scopes the specification requires
it to serve, and conversely one that reads §21.1 correctly would serve
them — a real difference in which bytes get returned for, e.g., a layer
whose only defect is a stored-flags/registry mismatch (L49). For a
*verifier*, no: both readings converge once §21.1 and the Detector column
are consulted, since the verifier's own obligations are stated
unambiguously per-row. So the ambiguity is byte-level for an implementation
that reads §2.4 and the bare register table as sufficient and never
reaches §21.1's own qualifying paragraph — which, given §21.1 is the
register's own preface, a careful implementer would read, but §2.4's
unqualified phrasing is still a document-structure trap for a partial
reading.

byte_level: true
byte_level_rationale: A reader is genuinely required by this document to
serve data (not reject) for a verifier-only-detected condition (§21.1, and
Appendix H's checklist: certain rows "oblige the reader that serves the
structure to serve it unchanged"), yet §2.4's unqualified "reader outcome"
label, read alone, implies the opposite for the same rows. Whether an
implementation built strictly from §2.4 serves or refuses those scopes is
exactly the byte difference at stake.

---

### verifiera-02 — kind OBSERVATION — a changed fixed declaration over a stored tile is, by the document's own account, mostly unwitnessed

**Location A:** §20.3, the paragraph beginning "The line is drawn where a
stored tile's meaning is fixed."

**Quotation A:** "Under new [declarations] the same bytes would denote
values, coordinates or padding the writer did not store, with every
checksum in §8 certifying the result and, but for a stored tile's decoded
size, a padding position or pad bit, or a boolean byte the register
witnesses (T3, T14, T21, T22, T4, T5, T2) and a decode that fails
outright, or a codec's framing check that precedes it, under a changed
codec or filter (T17, T24, T25), no check any actor owes able to see it
(§21.7)."

**Location B:** §9.7, note: "Nothing here enumerates prior commits. A
verifier certifies what a reader can reach and counts what it cannot,
which is decidable from the live trailer in one pass and does not depend
on reconstructing the file's history."

**Detail.** Probe V5 asks whether a verifier can see that *the last
commit* changed a fixed declaration of a layer that stored a tile (a
conduct rule bound on the appender, §20.3, not itself a register row —
"no file is nonconforming by virtue of its violation, and no register row
records the violation itself... the bar stating no condition a file can
exhibit"). The document is explicit and internally consistent that (a) a
verifier never sees commit history at all — only the live state — so "the
last commit did X" is not a question a verifier's walk can even ask; and
(b) even confined to the one generation it does see, the *effects* of such
a change are undetectable except where they happen to also trip one of a
named, closed list of other rows (decoded-size mismatch T3/T14, window/
content-size T21/T22, padding/pad-bit/bool-byte T4/T5/T2, or a codec framing
check T17/T24/T25 under a changed codec/filter). This is not a
contradiction — the document says so of itself, twice, in different
sections that agree — but it is worth recording as a load-bearing fact for
a verifier implementation: there is no register row, and no walk step, that
targets this condition directly, and an implementer tasked with "detect
when an update changed fixed declarations" would be building something
this specification affirmatively does not provide and says it does not
provide.

byte_level: false
byte_level_rationale: Resolving this does not change what bytes a
conforming implementation may emit, accept, or reject — the document
already fixes the answer (no check sees it, except incidentally via the
named rows) and both of my candidate implementers reading this file would
reach the same conclusion. I report it as an observation because it is the
decisive fact behind probe V5's answer, not as an unresolved question.

---

## 5. Note on V1–V6 overlap with §1–4 above

Each probe answer below cites the specific rule text directly rather than
only cross-referencing §1–4; the two sections are built from the same
reading and agree with each other and with this transcript's register
table and arithmetic.
