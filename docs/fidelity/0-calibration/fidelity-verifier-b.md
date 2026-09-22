# Verifier-implementer walk — edition B — transcript

## Disclosure

**What I read.** Exactly and only the file named in the brief:
`/Users/robertkleffner/Documents/GitHub/tarn-first-draft/scratch/cleanroom/editions/b/tarn.md`
(4,977 lines, ~295 KB). I confirmed its path and size with `wc -l` (a
command over that one file, not a read of any other file), then read
its full contents through the Read tool in five sequential chunks
(offsets 1, 1000, 2194 region reread, 2425, 2904, 3187, 3473, 3731,
4030 — precise ranges: 1–1000, 1000–1700 [via the 2194 offset for
§15–16], 2194–2413, 2425–2634, 2904–3183, 3187–3476, 3473–3732,
3731–4030, 4030–4279), until I had read the entire body of the
document end to end, plus a `grep -n "^### \|^#### \|^## "` over that
same file to get the section-heading map (a fixed, non-wrapped line
pattern — headings do not hard-wrap — so this grep is not subject to
the wrapping caution). I did not run any other grep. I did not open
any other file, any other copy of this or any other TARN document, any
ADR, PLAN.md, AGENTS.md, or any directory listing beyond `wc -l` and
the one `grep` above (neither of which lists a directory or reads a
second file). I did not use git, web search, or web fetch.

**Context that arrived unasked.** My runtime placed into context,
before I began: a CLAUDE.md pointer file, a user memory index
(titled entries about "TARN" topics — harness spec paths, gate word
lists, repair defects, subagent models, and similar), a git-status
block naming five recent commit subjects (about ADR-0133 and
ADR-0132), and a "user email" field. None of this is part of the
specification and none of it is evidence about the specification. I
have not treated any of it as such, and beyond naming its categories
here (as the brief requires), I have not repeated its contents or
let it steer any judgment below. Everything in the analysis that
follows is drawn from the one file read above and from my own
arithmetic.

**Path check.** The file was exactly where the brief said it would
be; no discrepancy to report.

**Scratch directory.** `/private/tmp/claude-501/-Users-robertkleffner-Documents-GitHub-tarn-first-draft/fidelity-1/scratch/walk-verifier-b/`
was empty when I started (checked with `ls -la`; only `.` and `..`).
This transcript is the only file I have written there. I did not
read or list the output directory `/private/tmp/claude-501/.../fidelity-1/out/` beyond writing my
own transcript file to it by its given path.

---

## Part A — The conforming-verifier algorithm

### A.1 Verdict vocabulary (§2.3, `[R-CNF-11]`)

> "A verifier reports one of three verdicts: *conforming*,
> *nonconforming*, or *cannot establish* — the last where some
> requirement is one it is unable to check on a capability or
> resource ground..."

- **conforming** — every file-level requirement is checked and none
  is violated. "A verifier certifies only violation-free files"
  (§2.4).
- **nonconforming** — the verifier has *established* at least one
  violation. This wins regardless of how much else went unchecked:
  "An established violation takes priority: a verifier that has
  established any violation reports *nonconforming*, however many
  requirements it was unable to check" (§2.3).
- **cannot establish** — the verifier established no violation, but
  some requirement was one it could not check on a capability or
  resource ground (unimplemented format major, an unimplemented
  MU=1 record type, an inexecutable codec/filter (`[R-COD-11]`), a
  declined layer/tile decode on resource grounds (`[R-ERR-04]`,
  `[R-SER-05]`, `[R-SER-08]`), or a declined user-metadata decode
  (`[R-MTA-09]`)). "*Cannot establish* is not a finding that the
  file is nonconforming, and a verifier MUST NOT certify a file it
  reports that way" — and it "is available only to a traversal that
  established no violation" (§2.3).

Two things are explicitly **not** part of this three-way vocabulary,
and I keep them distinct because the register (§21.1) and §2.3 do:

- **unexamined** — reported per-scope by a verifier that stopped at
  the first violation it found (`[R-CNF-11]` permits this). "*Unexamined*
  is neither a verdict nor *cannot establish* — it constrains the
  report, not the verdict."
- A **per-requirement capability/resource report** — "A verifier
  MUST report each requirement it was unable to check on a capability
  or resource ground, naming the requirement and the ground,
  **whichever of the three verdicts it reports**" (§2.3, emphasis
  mine). So a *nonconforming* verdict can still carry capability-ground
  notes; they just don't change the verdict once a violation is
  established.

### A.2 The algorithm, as an ordered procedure

Consolidating §19 (open/access/read), §9.6–9.7 (recovery diagnosis,
coverage), §8 (chain of trust), and §21 (register) into the single
ordered walk a verifier actually runs:

1. **End of file / trailer (§19.1 steps 1–2, §6.2, §6.3).**
   Obtain F. F < 128 → reject-file (`[R-CNT-27]`, F5) — decided from
   F alone, no other byte needed. Otherwise fetch [F−64, F) and
   validate, in the fixed order §6.2 states: trailer magic (F8),
   trailer CRC (F14), version gate (F18, `[R-CNT-07]`; and for a
   different-but-implemented major nothing more is owed under this
   text, `[R-CNF-13]`), then flag gates (F19, `[R-CNT-08]`),
   `committed_file_length` = transport size and multiple of 64
   (F13, F17), `dir_offset` ≥ 16 (F9), `dir_length` ≥ 4 (F16),
   `dir_offset + dir_length` ≤ F−64 (F10, and F3's overflow variant),
   `file_id` ≠ 0 (F12), reserved bytes zero (F15). Any failure →
   reject-file, verdict *nonconforming* (unless the file also fails
   to name an implemented major, in which case — for version_major
   itself an *implemented* major — F18 is the only reject-file case
   still inside the register; an unimplemented-but-nonzero major is
   the `[R-CNT-07]` capability refusal discussed in A.3 below, not a
   register row, and not itself evidence of nonconformance).
2. **Directory (§19.1 step 3, §7.1).** Fetch [dir_offset,
   dir_offset+dir_length), verify its terminal CRC-32C before any
   other use (F20). Failure → reject-file.
3. **Record walk (§19.1 step 4, §7.2–§7.4).** Parse records under
   the fixed 24-byte-header framing; F2 (u64 domain), F29 (overrun/
   residue), F24 (type 0), F34 (second top-level user-metadata),
   F30–F32 (extent-slot rules for non-layer records), F21–F23
   (user-metadata framing), F35/F36 (reserved-range type,
   MU-bit and bare emission), F25/F26/F28 (flag-combination and
   registry-mismatch — verifier-only, at certification) all attach
   here. Build the layer-name namespace; F4 catches a byte-identical
   duplicate. An unimplemented top-level MU=1 type is a capability
   refusal, not this step's business as a violation (§21.6, A.3
   below) — *unless* the type is in the reserved range, in which
   case F35/F36 make it a violation regardless of MU.
4. **Per-layer validation (§19.3, on every layer, since a verifier
   "checks every file-level requirement" §2.3 — not only the
   layers a reader would access).** Full inline-payload parse and
   every §7.4 constraint (L1–L36, L39, L43, L45 — value domains,
   name rules, index-encoding, slab/alignment declarations, codec/
   filter/type/layout enumerations, geometry floor, the
   `entry_count`/`extent_length` cross-check L21/L22). L46–L49 are
   verifier-only (flag-combination, reserved-flag, registry
   mismatch, unsorted metadata). Any hit → reject-layer,
   *nonconforming*.
5. **Per-layer index chain (§15.4, `[R-IDX-04]`, on every segment of
   every layer — again, not merely the segments a request would
   touch).** `crc_of_crc_array` over the fetched CRC array (L37),
   each segment CRC over its entries (L38). Failure → reject-layer.
6. **Per-entry classification (§15.3, `[R-IDX-03]`, T6–T12).**
   Sentinel vs. well-formed vs. structurally-invalid, for every
   entry. A structurally-invalid entry → reject-tile, and — this is
   the point §5.2/§9.7 lean on hardest — contributes **no stored
   extent** to the coverage walk or to run-continuity (§16); its
   nominal bytes fall to slack if no other claimant claims them.
7. **Per-tile payload and decode, for every stored (non-sentinel,
   structurally-valid) entry (§17, §19.4 steps 5–6, T1, T3, T13–T26,
   T2/T4/T5/T26 verifier-only content obligations).** Entry crc over
   stored bytes (T1) before decoding; codec-specific framing (T14–
   T25); decoded size exactly right (T3); content obligations —
   padding positions and pad bits equal fill (T4, T5), interleaved
   bool bytes in {0,1} at real positions (T2), byte-shuffle stride
   correctness so far as it is witnessed (T26). **This is where
   `[R-COD-11]` bites**: if the verifier cannot execute the layer's
   declared codec or filter, it cannot check T2/T3/T4/T5/T13–T26 for
   that layer's tiles, so it cannot certify (§17.4) — see A.4 below.
8. **User-metadata extents, for every one present (§18.2, R1–R10,
   `[R-CNT-25]` quarantine).** Framing (F21–F23/L10–L12), extent CRC
   (R2), decode under the declared encoding (R3), and — only for
   encoding 2 — R4's frame constraints, then the decoded document's
   own rules (R5–R10, F27/L48 for sort order). Every one of these is
   ignore-record: it never blocks certification of the containing
   file/layer, though F27/L48 (unsorted keys) and F28/L49 (registry-
   flag mismatch) *do* make the file nonconforming even though no
   reader behavior changes (§21.6's closing paragraph, `[R-CNF-05]`).
9. **Coverage walk (§9.7, `[R-LIF-08]`, §5.2, `[R-CNT-02]`,
   `[R-CNT-13]`, F7/F33/L18/L40–L42).** From the validated live
   trailer and directory, enumerate every claimant — front block,
   trailer, directory, every record's extent, every layer's
   tile-index region (once, via its layer record's extent slot),
   and every well-formed entry's stored-tile extent (structurally-
   invalid entries contribute none) — check pairwise disjointness
   (F33 across scopes, L18 within one layer), containment in
   [16, F−64) (F9/F10, L15–L17, T8/T9), and each checksum §8.1 maps.
   Sum unclaimed bytes as slack; report the total, or a partial
   bound plus the scope/violation that stopped the walk, per
   `[R-CNT-21]`.
10. **Verdict.** No violation anywhere and every requirement checked
    → *conforming*. Any established violation → *nonconforming*
    (report it; report every capability/resource ground hit along
    the way, but the verdict stands). No violation but some
    requirement uncheckable on capability/resource grounds →
    *cannot establish* (report each such requirement and its
    ground).

### A.3 What bars *nonconforming* without being a violation

Two "conforming files a reader nevertheless refuses" exist (§21.6's
closing paragraphs), and a verifier must not mistake either for
nonconformance:

- **version_major names an unimplemented major.** `[R-CNT-07]`
  rejects the file, but "the file can be perfectly conforming under
  that major" — this reader/verifier simply does not implement it,
  which under `[R-CNF-13]` is a *reach* question decided condition by
  condition (only F8, F14, F6's two instances, and F1's two
  instances — the ones asserting an `[R-CNT-24]`-fixed invariant —
  apply to a file of another major at all).
- **an experimental-range top-level record type carries MU=1.**
  `[R-CNT-15]` obliges reject-file, yet `[R-CNF-02]` "makes the file
  conforming all the same" — the prohibition on emitting experimental
  values in released software binds the writer's conduct, not the
  file's bytes. This is **probe V2**'s scenario when the type is
  experimental-range (see below).

### A.4 §17.4's codec-execution rule in detail (feeds probe V4)

> "A verifier that cannot execute a layer's codec or filter cannot
> establish that layer's conformance and MUST NOT certify the file.
> That inability is not a finding that the file is nonconforming, and
> it fixes the file's verdict as *cannot establish* only where the
> verifier established no violation elsewhere (`[R-CNF-11]`)."
> (`[R-COD-11]`)

And immediately after: "For a conforming reader that position arises
only at a reserved or experimental value, every assigned codec and
filter being core" — i.e. a genuinely conforming verifier can only
ever be in this position at codec/filter values 5–0x7FFF or ≥0x8000
(reserved/experimental), because it is obliged to implement all of
1–4 and 1–2 (`[R-CNF-03]`). But those same reserved/experimental
values are *already* an independent layer-scope violation the moment
they are read off the layer record (L43 for codec, L45 for filter) —
no decode needed to see it. So the "cannot execute" branch of
`[R-COD-11]` is not, for a genuinely conforming verifier, a
*separate* path to *cannot establish*: the L43/L45 violation is
already established by the time execution would even be attempted,
and per §2.3 "an established violation takes priority" — the verdict
is *nonconforming*, not *cannot establish*, and the report is a
straight L43/L45 row, not a capability note.

Where `[R-COD-11]`'s *cannot establish* branch genuinely applies is
software that is *not* a conforming verifier in the first place (it
does not implement one of the four core codecs or two core filters)
encountering an otherwise-valid declared value it cannot run. That
software is not a conforming verifier by `[R-CNF-03]`'s own terms —
but the rule is still worth having, because such software is exactly
what will exist in practice, and the rule tells it what to say
instead of falsely certifying or falsely condemning: report *cannot
establish*, name the codec/filter and `[R-COD-11]` as the ground, and
do not certify.

**What the report says about that layer (§2.3, §9.7):** the
per-requirement capability report names the unchecked requirement
(`[R-SER-05]` padding-content, `[R-SER-08]` bool-byte, `[R-SER-07]`
decoded-size-exactness, or the specific T-row family for that codec)
and the ground ("cannot execute codec N" / "cannot execute filter
N", `[R-COD-11]`) — *for that layer*. It does **not** need to make
the coverage walk (§9) partial for that layer: decoding is not
required to enumerate the layer's claimants. The walk needs only the
layer record's extent slot, the index region's checksums
(`[R-IDX-04]`), and each entry's crc over its *stored* bytes (T1,
which is a checksum comparison, not a decode) — none of which
invokes the codec or filter. So a verifier stuck on `[R-COD-11]` for
one layer can still report an **exact** slack total across the whole
file; only its *certification* is blocked, not its *coverage
accounting*. I did not find this stated in so many words anywhere in
§5.2/§9.7/§17.4 — it is a consequence I derived from what each
section separately requires the walk to check versus what
`[R-COD-11]` says decoding is needed for. I flag it as finding
**verifierb-01** below because the three sections could easily be
read (wrongly, I believe) as coupling the two.

---

## Part B — Coverage walk arithmetic on a concrete file (probe V3)

### B.1 Setup and stated assumptions

Three generations of one file. Given: generation 1 creates layer A
(stored tiles 4,096 B total, index region 84 B); generation 2 adds
layer B (stored tiles 8,192 B, index region 164 B); generation 3
supersedes one 1,024 B tile of A with a 1,024 B payload. Each
generation's directory is 200 B, trailer 64 B (given, for every
generation).

**Assumptions I made, stated per the brief's requirement:**

1. **No alignment or slab declared** on either layer (not stated
   otherwise), so `[R-SLB-05]` applies: tiles and index regions are
   packed with no gap between them beyond what the commit protocol
   itself forces. I place each generation's new content
   contiguously: tiles then index (order is immaterial to the
   totals; `[R-SLB-05]` licenses either).
2. **The pre-trailer pad (`[R-LIF-02]` step 5)** is the only gap: it
   brings the position immediately after the directory up to the
   next 64-byte-aligned offset, where the 64-byte trailer begins.
   This is the pad I compute per generation below; writers are
   advised, not required, to zero it (`[R-CNT-03]`), and it is
   slack regardless of content (§5.2).
3. **Generation 3's re-emitted index region for layer A is again 84
   bytes.** Superseding one existing tile with a same-size payload
   changes no addressed-tile count, so `entry_count` is unchanged and
   `[R-CNT-17]`'s formula (`entry_count × 20 + ⌈entry_count/2¹⁶⌉ × 4`)
   yields the same 84 bytes as generation 1 — only the one entry's
   offset/crc changes, at a new placement (`[R-WRT-04]`: "Every layer
   whose stored-tile set or index content this commit changes has its
   tile-index region re-emitted in full ... necessarily at a new
   placement").
4. **Layer B is untouched in generation 3** and so keeps its extent
   slot pointing at its generation-2 placement unmoved (`[R-WRT-05]`).
5. Front signature block is the constant 16 bytes at offset 0,
   emitted once, never re-emitted (§6.1, §9.2's creation note).

### B.2 Byte-by-byte construction

**Generation 1** (creation path, `[R-LIF-02]`, offsets from 0):
- front block: [0, 16)
- A's tiles + index (4,096 + 84 = 4,180 B): [16, 4,196)
- directory₁ (200 B): [4,196, 4,396)
- pad to next 64-aligned offset: 4,396 → next multiple of 64 is
  4,416 (4,396 / 64 = 68.6875) → pad₁ = **20 B**: [4,396, 4,416)
- trailer₁ (64 B): [4,416, 4,480)
- **F₁ = 4,480** (= 70 × 64 ✓)

**Generation 2** (append, starts at F₁ = 4,480):
- B's tiles + index (8,192 + 164 = 8,356 B): [4,480, 12,836)
- directory₂ (200 B): [12,836, 13,036)
- pad: 13,036 → next multiple of 64 is 13,056 (13,036/64 = 203.6875)
  → pad₂ = **20 B**: [13,036, 13,056)
- trailer₂ (64 B): [13,056, 13,120)
- **F₂ = 13,120** (= 205 × 64 ✓)

**Generation 3** (append, starts at F₂ = 13,120): supersedes one
1,024 B tile of A.
- new payload (1,024 B): [13,120, 14,144)
- A's re-emitted index region (84 B, assumption 3 above):
  [14,144, 14,228)
- directory₃ (200 B): [14,228, 14,428)
- pad: 14,428 → next multiple of 64 is 14,464 (14,428/64 = 225.4375)
  → pad₃ = **36 B**: [14,428, 14,464)
- trailer₃ (64 B): [14,464, 14,528)
- **F₃ = 14,528** (= 227 × 64 ✓) — this is the file's total size.

### B.3 Live-state total (§5.2, `[R-CNT-02]`, §9.7)

The live state at F₃ is what the live trailer/directory reach:

| Claimant | Bytes |
|---|---|
| front signature block | 16 |
| layer A's live stored tiles (4,096 total: 3,072 untouched, from gen 1's placement, + the 1,024 new one from gen 3) | 4,096 |
| layer A's live index region (gen 3's re-emitted 84 B) | 84 |
| layer B's live stored tiles (untouched since gen 2) | 8,192 |
| layer B's live index region (untouched since gen 2) | 164 |
| directory₃ | 200 |
| trailer₃ | 64 |
| **Live total** | **12,816** |

### B.4 Slack total

Everything else in the 14,528-byte file is slack (§5.2, `[R-CNT-21]`):

| Slack item | Bytes |
|---|---|
| pad₁ (always slack, even while gen 1 was live) | 20 |
| directory₁ (superseded by directory₂) | 200 |
| trailer₁ (superseded by trailer₂) | 64 |
| A's generation-1 index region (superseded by gen 3's re-emission) | 84 |
| the superseded 1,024 B tile of A | 1,024 |
| pad₂ | 20 |
| directory₂ (superseded by directory₃) | 200 |
| trailer₂ (superseded by trailer₃) | 64 |
| pad₃ (live generation's own pre-trailer pad — slack by definition, §5.2) | 36 |
| **Slack total** | **1,712** |

**Check:** 12,816 (live) + 1,712 (slack) = 14,528 = F₃. ✓

**A verifier whose walk completes reports: live-state total 12,816
bytes; slack total 1,712 bytes; file size 14,528 bytes.**

### B.5 The same file, walk that does not complete

Vary generation 3: suppose layer B's tile-index region (unchanged
placement from generation 2, still live) contains two entries whose
stored-tile extents overlap one another — an `[R-CNT-13]` violation
the walk itself establishes, condition **L18** ("Two structures of
one and the same layer claim overlapping bytes in the live committed
state" — verifier, certification). Per §5.2:

> "A rejected layer's claimants are not enumerated ... and where the
> rejection is one the walk itself established, L18's overlap or
> L40 through L42's placement among them, the claimants it had
> already enumerated are discarded with the layer, since the total
> is a claim about a live state one of whose layers is not usable."

So layer B's already-enumerated claimants — its 8,192 B of tiles and
164 B index region, 8,356 B total — are discarded from the live
total, and the walk is reported **partial**:

- Claimants the walk *did* enumerate and keep: front block (16) +
  layer A's tiles (4,096) + A's index (84) + directory₃ (200) +
  trailer₃ (64) = **4,460 B** (the exact live total, restricted to
  what survives).
- Reported (partial) unclaimed total = F₃ − 4,460 = 14,528 − 4,460 =
  **10,068 B**.

Per `[R-CNT-21]`: "A partial total is F less the bytes claimed by
the claimants the walk did enumerate — an upper bound on the file's
true slack, never an under-count — and a verifier reporting one MUST
say which scope or violation stopped the walk." So the verifier's
report here is: **verdict nonconforming (L18, layer B); partial
unclaimed-byte total 10,068 B, stopped by layer B's L18 overlap; the
true slack is some subset of that 10,068 (in fact 1,712 + 8,356 =
10,068 exactly, since B's bytes are not truly slack, merely
un-enumerated because B is unusable) — the report must not claim
10,068 as the slack figure outright, only as the bound, and must
name L18/layer B as the reason.**

---

## Part C — Every register row's detector and outcome

The full register (§21.2–§21.5) as read, verbatim from the document
(I am not re-deriving these; I quote/paraphrase the tables exactly as
printed, since the charter asks me to "cover... every register row's
detector and outcome").

### §21.2 File-scope (outcome: reject-file). 35 conditions, rows F1–F36 (F11 struck).

F1 signature byte-reversed (reader/open, `[R-ENC-02]`); F2 u64 field
>2⁶³−1 (reader/open, `[R-ENC-03]`); F3 declared sum overflow
(reader/open, `[R-ENC-04]`); F4 duplicate layer name (reader/open,
`[R-ENC-15]`); F5 file <128 B (reader/open, `[R-CNT-27]`); F6 front
block byte mismatch (reader/open, `[R-CNT-04]`); F7 structure in
pre-trailer gap (verifier/certification, `[R-CNT-05]`); F8 trailer
magic mismatch (reader/open, `[R-CNT-06]`); F9 dir_offset<16
(reader/open, `[R-CNT-06]`); F10 dir region runs into trailer
(reader/open, `[R-CNT-06]`); F12 file_id=0 (reader/open,
`[R-CNT-06]`); F13 committed_file_length not ×64 (reader/open,
`[R-CNT-06]`); F14 trailer CRC mismatch (reader/open, `[R-CNT-06]`);
F15 reserved trailer bytes nonzero (reader/open, `[R-CNT-06]`); F16
dir_length<4 (reader/open, `[R-CNT-06]`); F17 committed length ≠
transport size (reader/open, `[R-CNT-06]`); F18 version_major=0
(reader/open, `[R-CNT-07]`); F19 incompat-lane bit set (reader/open,
`[R-CNT-08]`); F20 directory CRC mismatch (reader/open,
`[R-CNT-11]`); F21 top-level metadata record (0,0) slot (reader/open,
`[R-CNT-25]`); F22 top-level metadata extent_length<5 (reader/open,
`[R-CNT-25]`); F23 top-level metadata inline_length≠1 (reader/open,
`[R-MTA-03]`); F24 type=0 (reader/open, `[R-CNT-12]`); F25 non-layer
MU=1/PE=0 (verifier/certification, `[R-CNT-12]`); F26 reserved flag
bits 2–15 set (verifier/certification, `[R-CNT-12]`); F27 file-scope
metadata document unsorted keys (verifier/certification,
`[R-MTA-05]`); F28 registered type's stored MU/PE differs from
registry (verifier/certification, `[R-CNT-22]`); F29 record
header/payload overrun or residue (reader/open, `[R-CNT-12]`); F30
non-layer extent slot half-zero (reader/open, `[R-CNT-13]`); F31
non-layer extent_offset in [1,15] (reader/open, `[R-CNT-13]`); F32
non-layer extent past F−64 (reader/open, `[R-CNT-13]`); F33
cross-scope/cross-layer overlap (verifier/certification,
`[R-CNT-13]`); F34 two top-level metadata records (reader/open,
`[R-CNT-14]`); F35 reserved-range type with MU=1 (reader/open,
`[R-CNT-15]`); F36 reserved-range type emitted at all (verifier/
certification, `[R-CNT-15]`).

### §21.3 Layer-scope (outcome: reject-layer). 49 conditions, L1–L49.

L1 u64 field >2⁶³−1 in a layer (reader/layer access, `[R-ENC-03]`);
L2 declaration-derived product/sum overflow (reader/layer access,
`[R-ENC-04]`); L3 layer name ill-formed UTF-8 (reader/open,
`[R-ENC-11]`); L4 dim/channel name ill-formed UTF-8 (reader/layer
access, `[R-ENC-11]`); L5 empty layer name (reader/open,
`[R-ENC-12]`); L6 layer name control code point (reader/open,
`[R-ENC-12]`); L7 empty dim/channel name (reader/layer access,
`[R-ENC-12]`); L8 dim/channel name control code point (reader/layer
access, `[R-ENC-12]`); L9 duplicate dim or channel name (reader/layer
access, `[R-ENC-15]`); L10 sub-record metadata (0,0) slot (reader/
layer access, `[R-CNT-25]`); L11 sub-record metadata extent_length<5
(reader/layer access, `[R-CNT-25]`); L12 sub-record metadata
inline_length≠1 (reader/layer access, `[R-MTA-03]`); L13 sub-record
type=0 (reader/layer access, `[R-CNT-12]`); L14 sub-record
header/payload overrun/residue (reader/layer access, `[R-CNT-12]`);
L15 layer/sub-record extent slot half-zero (reader/layer access,
`[R-CNT-13]`); L16 extent_offset in [1,15] (reader/layer access,
`[R-CNT-13]`); L17 extent past F−64 (reader/layer access,
`[R-CNT-13]`); L18 intra-layer overlap (verifier/certification,
`[R-CNT-13]`); L19 two metadata sub-records (reader/layer access,
`[R-CNT-14]`); L20 both A≠0 and S≠0 (reader/layer access,
`[R-CNT-16]`); L21 entry_count ≠ geometry-derived count (reader/
layer access, `[R-CNT-17]`); L22 extent_length ≠ formula (reader/
layer access, `[R-CNT-17]`); L23 inline-payload field overrun/
truncation (reader/open for the name; reader/layer access for
everything else, `[R-CNT-18]`); L24 sub-record reserved-range MU=1
(reader/layer access, `[R-CNT-18]`); L25 sub-record reserved-range
type emitted (verifier/certification, `[R-CNT-15]`); L26 nested
layer-type sub-record (reader/layer access, `[R-CNT-18]`); L27
entry_count=0 with nonzero crc_of_crc_array (reader/layer access,
`[R-CNT-23]`); L28 S=0 with nonzero A_slab (reader/layer access,
`[R-CNT-23]`); L29 S≠0 with invalid A_slab (reader/layer access,
`[R-CNT-23]`); L30 fill length ≠ type element size (reader/layer
access, `[R-CNT-23]`); L31 index_encoding≠1 (reader/layer access,
`[R-CNT-23]`); L32 geometry field with floor 1 is 0 (reader/layer
access, `[R-GEO-01]`); L33 linearization≠1 (reader/layer access,
`[R-GEO-05]`); L34 channel type outside 1–13 (reader/layer access,
`[R-TYP-03]`); L35 bool fill not 0x00/0x01 (reader/layer access,
`[R-TYP-07]`); L36 layout≠1,2 (reader/layer access, `[R-SER-06]`);
L37 crc_of_crc_array mismatch (reader/tile use, `[R-IDX-04]`); L38
segment CRC mismatch (reader/tile use, `[R-IDX-04]`); L39 invalid
alignment A (reader/layer access, `[R-SLB-01]`); L40 misaligned
tile offset (verifier/certification, `[R-SLB-01]`); L41 slab-run gap/
overlap/misorder (verifier/certification, `[R-SLB-03]`); L42 slab
run's first tile misaligned to A_slab (verifier/certification,
`[R-SLB-03]`); L43 codec≠1–4 (reader/layer access, `[R-COD-03]`); L44
lz4 with oversize decoded tile (reader/layer access, `[R-COD-07]`);
L45 filter≠1,2 (reader/layer access, `[R-COD-09]`); L46 layer/
sub-record MU=1/PE=0 (verifier/certification, `[R-CNT-12]`); L47
reserved flag bits 2–15 (verifier/certification, `[R-CNT-12]`); L48
layer-sub-record metadata document unsorted keys (verifier/
certification, `[R-MTA-05]`); L49 registered type's stored MU/PE
mismatch (verifier/certification, `[R-CNT-22]`).

### §21.4 Tile-scope (outcome: reject-tile). 26 conditions, T1–T26.

T1 stored bytes fail entry crc (reader/tile use, `[R-CNT-20]`); T2
interleaved bool byte ∉{0,1} at real position (verifier/
certification, `[R-SER-08]`); T3 decoded length ≠ decoded size
(reader/tile use, `[R-SER-07]`); T4 padding position ≠ fill
(verifier/certification, `[R-SER-05]`); T5 packed-bool final-byte pad
bit ≠ fill bit (verifier/certification, `[R-SER-05]`); T6 sentinel
offset/length with crc≠0 (reader/tile use, `[R-IDX-03]`); T7 exactly
one field at sentinel value (reader/tile use, `[R-IDX-03]`); T8
non-sentinel offset<16 (reader/tile use, `[R-IDX-03]`); T9
non-sentinel extent past F−64 (reader/tile use, `[R-IDX-03]`); T10
non-sentinel length=0 (reader/tile use, `[R-IDX-03]`); T11
non-sentinel field >2⁶³−1 (reader/tile use, `[R-IDX-03]`); T12
non-sentinel offset+length overflow (reader/tile use, `[R-IDX-03]`);
T13 tile not independently decodable (reader/tile use, `[R-COD-02]`
— detected via T25); T14 codec-1 length≠decoded size (reader/tile
use, `[R-COD-04]`); T15 deflate wrapper present (reader/tile use,
`[R-COD-05]` — detected via T24/T25); T16 second deflate stream
(reader/tile use, `[R-COD-05]` — via T24); T17 zstd missing magic
(reader/tile use, `[R-COD-06]`); T18 zstd extra frame (reader/tile
use, `[R-COD-06]`); T19 zstd nonzero dictionary ID (reader/tile use,
`[R-COD-06]`); T20 zstd content-checksum flag set (reader/tile use,
`[R-COD-06]`); T21 zstd window > decoded size (reader/tile use,
`[R-COD-06]`); T22 zstd content-size ≠ decoded size (reader/tile use,
`[R-COD-06]`); T23 lz4 frame instead of block (reader/tile use,
`[R-COD-07]` — via T25); T24 decode doesn't consume extent exactly
(reader/tile use, `[R-COD-08]`); T25 malformed stream fails to decode
(reader/tile use, `[R-COD-08]`); T26 filter applied at wrong stride,
witnessed via T2/T4 (verifier/certification, `[R-COD-10]`).

### §21.5 Ignored (outcome: ignore-record). 10 conditions, R1–R10.

R1 metadata encoding 0 or reserved (reader/open for top-level, layer
access for sub-record, `[R-CNT-25]`); R2 metadata extent CRC mismatch
(reader/extent use, `[R-CNT-20]`); R3 document fails to decode under
declared encoding (reader/extent use, `[R-CNT-25]`); R4 encoding-2
frame-constraint violation (reader/extent use, `[R-MTA-09]`); R5
ill-formed UTF-8 or unpaired surrogate in decoded document (reader/
extent use, `[R-CNT-25]`); R6 empty/control-code-point key (reader/
extent use, `[R-MTA-04]`); R7 not well-formed JSON / not an object /
leading BOM (reader/extent use, `[R-MTA-04]`); R8 non-finite number
(reader/extent use, `[R-MTA-04]`); R9 duplicate decoded key (reader/
extent use, `[R-MTA-04]`); R10 key >255 bytes (reader/extent use,
`[R-MTA-04]`).

**Totals as the document states them:** 35 + 49 + 26 + 10 = 120
conditions (§21.8 confirms: "120 conditions over 277 instances").

---

## Part D — Probe derivations

### V1 — see Part A.1 above (verdict vocabulary + one condition each).

### V2 — top-level record, unimplemented type, MU=1

The document's answer is conditional on the type's numeric range
(§10.2's partition), and it fully determines both branches:

- **If the type is in the reserved range (0x0003–0x7FFF):**
  emitting it at all is itself the violation **F36**
  (`[R-CNT-15]`: "a value from a reserved range MUST NOT be emitted
  at all before this specification assigns it"), and carrying MU=1
  on it is the further violation **F35** ("A top-level record has a
  reserved-range type value ... with MUST_UNDERSTAND ... set to 1").
  Verdict: **nonconforming**. The reader's mechanical action is
  still reject-file (`[R-CNT-15]`: "An unknown record type at file
  scope: MU=1 → reject-file"), but this is now also a genuine
  file-conformance defect.
- **If the type is in the experimental range (≥0x8000):** this is
  explicitly one of the two "conforming files a reader nevertheless
  refuses" (§21.6's closing paragraphs): "`[R-CNT-15]` obliges the
  reader to reject, and `[R-CNF-02]` makes the file conforming all
  the same." A verifier here has established no violation; it just
  cannot check what that type's record does or governs, so per
  §2.3's list of *cannot establish* grounds ("when a record carries
  MUST_UNDERSTAND = 1 with a type it does not implement (§21.6)"),
  verdict: **cannot establish** (report: the record's type value and
  scope, and that MU=1 makes it capability-blocking).

**The requirement that "fixes" the reader-visible reject-file outcome
in both cases is `[R-CNT-15]`**; which *verdict* a verifier reports
for the file as a whole forks on whether the type is also
reserved-range (adding F35/F36 as established violations) or
experimental-range (no violation, `[R-CNF-02]`, `[R-CNF-13]`
inapplicable since this isn't a version-major question).
`underdetermined`: the probe's own wording doesn't say which range,
so I give both readings; the document itself is not ambiguous once
the range is known.

### V3 — see Part B above in full.

### V4 — see Part A.4 above in full.

### V5 — last commit changed a fixed declaration of a layer that stored a tile

**Can the verifier see it? No, not as a distinct condition.** §20.3
step 4 states which declarations are fixed once a layer stores a
tile (layout, linearization, index encoding, codec, filter, rank,
dimension order, every tile extent, every channel's type and fill,
an interleaved layer's channel list bar names, the position of every
kept planar channel) and says of a commit that changes one:

> "This bar binds the commit as an actor: no file is nonconforming by
> virtue of its violation, and no register row records the violation
> itself, the register enumerating file-conformance violations
> (§21.1) and the bar stating no condition a file can exhibit (§21.7,
> `[R-ERR-01]`, `[R-CNF-02]`)."

This is a writer-*conduct* rule (`[R-CNF-02]`'s category), not a
file-bytes predicate. A verifier, per §9.7's own note, "certifies
what a reader can reach [the live state] and counts what it cannot
... does not depend on reconstructing the file's history — a
history the format does not promise to keep." There is no field
anywhere that records how many commits preceded the live one (§9.3's
third note: "how many commits a file has undergone is not
recoverable from the live trailer") — so a verifier examining only
the live generation has no vantage point from which "the last commit
changed X" is even a meaningful question; it sees one directory, one
set of declarations, one tile index.

**Verdict: no violation is established by this fact alone — the
verifier has nothing to check it against.** It is not "cannot
establish" either (that vocabulary is reserved for a requirement the
verifier knows it needs to check but lacks the capability/resource
to); this is a condition the format's own certification model
structurally cannot see, by design (§9.7's Note: "which is decidable
from the live trailer in one pass and does not depend on
reconstructing the file's history").

**The one exception, which the document names explicitly:** if the
new declaration happens to make the *old* stored bytes fail some
*other*, ordinary structural or content check under the new reading
— a decoded-size mismatch (T3), a padding/fill mismatch (T4/T5), an
interleaved-bool-byte violation (T2), or an outright decode failure
under a changed codec/filter (T17/T24/T25) — then *that* row fires,
reject-tile or reject-layer, exactly as it would for any other file
exhibiting the same bytes-vs-declarations mismatch. But this is
incidental: the document itself says the permitted-vs-forbidden
split "removes the edge" of trying to decide "which files would"
survive a reinterpretation in place, and that "no check any actor
owes [is] able to see it" in the general case (§20.3 step 4's long
paragraph; §21.7). A verifier does not detect "the fixed declaration
changed"; it only detects, coincidentally and only sometimes,
"the stored bytes don't parse under the currently declared reading."

### V6 — a record with MU=1, PE=0

`[R-CNT-12]`: "Writers MUST NOT emit the combination MU = 1 with
PE = 0; a reader or updater encountering it MUST treat the record as
PE = 1 (never silently deletable)... a verifier MUST treat a nonzero
reserved flag bit or the MU = 1 with PE = 0 combination as a validity
error at the record's governing scope."

So there are two separate things the document does with this
combination, at two different actors:

1. **Every reader/updater** (not just the verifier) functionally
   treats the record as if PE were 1 — it is preserved, never
   silently dropped, regardless of what the verifier concludes. This
   is unconditional and has nothing to do with certification.
2. **The verifier** additionally treats the *combination itself* as a
   file-conformance violation, at **the record's governing scope**
   (§7.2: "the layer for a layer record and for sub-records, the file
   for other top-level records"):
   - **Top-level, non-layer record:** file scope → **reject-file**,
     register row **F25** ("A non-layer top-level record's flags
     carry MUST_UNDERSTAND = 1 with PRESERVE_ON_EDIT = 0, a
     combination no writer emits" — detector *verifier*, detected at
     *certification*).
   - **Layer record or one of its sub-records:** layer scope →
     **reject-layer**, register row **L46** ("A layer record's or
     sub-record's flags carry MUST_UNDERSTAND = 1 with
     PRESERVE_ON_EDIT = 0" — detector *verifier*, detected at
     *certification*).

The verdict for the file is **nonconforming** either way (an
established violation), but the reject-file vs reject-layer split —
i.e. how much of the file the verifier's report condemns — follows
the record's own governing scope, exactly as `[R-CNF-08]`'s general
mapping states, with F25/L46 as the two concrete instances of it for
this particular combination.

---

## Part E — Findings surfaced during this walk

See structured findings (verifierb-01, verifierb-02) in the returned
result; both are OBSERVATIONs about edition B alone (no edition-A
comparison was possible or attempted, per the access rule), each with
its byte-level assessment stated inline.
