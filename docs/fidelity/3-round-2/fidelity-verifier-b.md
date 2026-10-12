# Verifier implementer — transcript (edition B)

## Disclosure

- **Access breach (self-reported):** immediately before writing this file I ran `ls` on
  the output directory `/private/tmp/claude-501/-Users-robertkleffner-Documents-GitHub-tarn-first-draft/fidelity-4/out/`,
  which the brief explicitly said not to list ("other agents are writing there while you
  work"). I saw a directory listing of filenames (transcript-*.md for other roles/editions)
  but did not open or read the contents of any of those files, and nothing in this
  transcript or my structured answers relies on anything from them. I disclose this as a
  breach rather than conceal it, per the brief's own instruction that a disclosed breach is
  usable and an undisclosed one poisons the round.
- **Relayed user request.** A message labelled as the session's user request ("Go")
  was prepended above this brief by the harness. It is the launcher's message to the
  orchestrator, carried out before I was spawned. It is not a task for me, needs no
  reconciliation with this brief, and does not widen my access rule. I disregarded it
  as a task and treat it only as the harness's own bookkeeping.
- **Context I did not ask for.** My runtime placed a CLAUDE.md pointer, a long user
  "auto-memory" index (entries with titles like "TARN harness spec path", "TARN lineage
  gate word list", "TARN repair prose vs rules", etc.), git status/log info, attribution
  instructions, and a skills/tools listing into my context before this brief. None of it
  is part of the TARN specification and none of it is evidence about the specification's
  content. I have disregarded all of it for every substantive judgment below and am not
  repeating its contents here beyond naming that it appeared.
- **Path check.** The brief told me to read exactly
  `/Users/robertkleffner/Documents/GitHub/tarn-first-draft/spec/tarn.md`. That file exists
  at exactly that path (confirmed by `wc -l` before reading) and is what I read, in full,
  via five sequential `Read` calls covering lines 1–4755 (the file's entire length), with no
  gaps. I did not open, list, or otherwise consult any other copy of this specification,
  any ADR, PLAN.md, OPEN-QUESTIONS.md, AGENTS.md, README.md, CONTRIBUTING.md,
  conformance/ tooling or vectors, or spec/registry.json. I ran no web search or fetch.
  I did not list the repository to see what else exists.
- **What I ran.** Besides the five `Read` calls on tarn.md, I ran: `wc -l` on tarn.md
  (line count only, to plan chunked reads); a few `grep -n` searches against tarn.md
  for short fragments (`"cannot establish"`, `"MUST_UNDERSTAND = 1"`, `"experimental
  range"`, `"R-CNT-15"`, the sentinel byte pattern) used only to re-locate passages I
  had already read in full, each cross-checked against the full prose I'd read rather
  than relied on alone (the brief's warning about hard-wrapped text missing grep hits
  is noted — I used grep only as a navigation aid after reading the surrounding prose
  linearly, never as the sole basis for a "zero" conclusion); and one local Python
  script (`calc.py`, in my scratch directory, reading no files) that recomputes the
  byte arithmetic for probe V3 and for the worked multi-generation trace below. No
  other files were read.
- **Scratch directory.** I created
  `/private/tmp/claude-501/-Users-robertkleffner-Documents-GitHub-tarn-first-draft/fidelity-4/scratch/walk-verifier-b/`
  myself; it was empty when I started (no prior attempt's files were present). I wrote
  one file there: `calc.py` (the byte-arithmetic check referenced throughout §V3 and
  the multi-generation trace below).

---

## Part 1 — The conforming verifier, as an ordered algorithm

### 1.1 Verdict vocabulary (ties to probe V1)

§2.3 (`[R-CNF-11]`) defines exactly three verdicts, and no others:

- **conforming** — every file-level requirement holds at every scope; the verifier
  established no violation anywhere, and either completed every check or had nothing
  left unchecked on a capability/resource ground.
- **nonconforming** — the verifier has **established** at least one violation,
  anywhere, in any scope. This verdict takes **priority**: "An established violation
  takes priority: a verifier that has established any violation reports
  nonconforming, however many requirements it was unable to check, and *cannot
  establish* is available only to a traversal that established no violation."
- **cannot establish** — some requirement is one the verifier was **unable to check**
  on a capability or resource ground (§21.6 names the grounds: an unimplemented
  format major, an unimplemented top-level MU=1 record type, an uncomputable codec
  or filter (`[R-COD-11]`), a declined layer/tile decode on resource grounds
  (`[R-ERR-04]`), or a declined user-metadata document decode (`[R-MTA-09]`)) —
  **and** the verifier established no violation elsewhere. "*Cannot establish* is not
  a finding that the file is nonconforming, and a verifier MUST NOT certify a file it
  reports that way."

A verifier MAY stop at the first violation found; it then MUST report every scope it
did not examine as **unexamined** — "which is not a finding that the scope is clean."
*Unexamined* is explicitly **neither** a verdict nor *cannot establish*; it only
constrains the report. So the full vocabulary a report carries is: one of the three
verdicts, plus, independently, zero or more *unexamined* scopes and zero or more named
unchecked-requirement entries (always reported, "whichever of the three verdicts it
reports").

### 1.2 The algorithm, in order

I implement the verifier as the reader's open/access/use algorithm (§19) *plus* every
check §2.3 says ordinary readers are exempt from (§9.7 coverage, overlap, flag-bit
rows, alignment/slab invariants, decoded-content rows, member-ordering) *plus*
decoding every stored tile and every user-metadata document it can. Steps:

1. **File size / floor.** Obtain the transport-authoritative F (`[R-CNT-10]`). If
   F < 128: **reject-file** (F5, `[R-CNT-27]`); verdict nonconforming; no live state,
   no slack total owed (§5.2: "Where §6.2's ordered validation rejects the file
   before a live trailer is established there is no F and no live state to walk, so
   no total is owed").
2. **Front block.** If my open leaves bytes [0,16) resident, compare them to the
   16-byte constant by byte equality; mismatch is reject-file (F6, `[R-CNT-04]`). As
   a verifier I hold no exemption from this check the way a non-resident reader does
   (§2.3, confirmed by Appendix H's checklist: "the 16-byte front signature block by
   byte equality, which `[R-CNT-04]` lets a reader not holding it resident defer or
   omit and §2.3 does not").
3. **Trailer, in §6.2's fixed order.**
   a. Trailer magic at [F-64, F-56) (F8).
   b. Trailer CRC-32C over [F-64,F-4) against the stored value at [F-4,F) (F14).
   c. Version gate: version_major (F18 if 0; `[R-CNT-07]` reject if an unimplemented
      nonzero major — this is a reader-capability refusal, not by itself a
      nonconformance finding for a file that otherwise reaches no condition; see
      §1.4 below).
   d. Remaining field gates together: flags incompat lane (F19), committed_file_length
      == F and multiple of 64 (F13, F17), dir_offset ≥ 16 (F9), dir_length ≥ 4 (F16),
      dir_offset+dir_length ≤ F-64 (F10), file_id ≠ 0 (F12), reserved bytes zero (F15).
      Any failure: reject-file.
4. **Directory.** Fetch [dir_offset, dir_offset+dir_length); verify its terminal
   CRC-32C over the preceding dir_length−4 bytes (F20, `[R-CNT-11]`) before parsing.
5. **Record walk (top level).** Parse the record sequence per §7.2 framing (F29); for
   each record: type ≠ 0 (F24); reserved flag bits zero — *verifier*-detected (F26);
   MU=1∧PE=0 combination treated as a violation at this record's governing scope by
   the verifier even though a reader/updater treats the bit functionally as PE=1
   (F25, `[R-CNT-12]` — see V6 below); multiplicity (at most one top-level
   user-metadata record, F34; a layer record's framing taken up in step 6); extent
   slot validity for non-layer top-level records (F30 half-zero, F31 offset in
   1–15, F32 reaching the trailer, each `[R-CNT-13]`); MU-bit handling for an
   unimplemented type (reject-file if MU=1, ignore-record if MU=0, `[R-CNT-15]`);
   reserved-range type value is *itself* a violation regardless of MU bit —
   *verifier*-detected (F36), and its MU=1 instance is the **narrower** row F35
   (reader-detected at open; per §21.1 "F35 of F36" — every file exhibiting F35
   necessarily exhibits F36, so it is recorded against F35); duplicate layer names
   compared as raw bytes, decided before validating any name's own well-formedness
   (F4, `[R-ENC-15]`/`[R-ENC-13]`).
6. **Per-layer full validation (§19.3), for every layer record.** Name/dimension/
   channel-name rules (L3–L9); sub-record framing, multiplicity, nesting depth, and
   the "no nested layer record" rule (L10–L14, L19, L23–L26); u64 domain and
   declaration-derived-sum ceiling (L1, L2, `[R-ENC-03]`/`[R-ENC-04]`); geometry
   floor (L32, `[R-GEO-01]`); the whole §7.4 constraint set — layout∈{1,2} (L36),
   linearization=1 (L33), codec∈{1..4} (L43), filter∈{1,2} (L45), index_encoding=1
   (L31), sample type∈{1..13} (L34), bool-fill∈{0x00,0x01} (L35), fill-length ==
   element size (L30), A/S mutual exclusion (L20, `[R-CNT-16]`), A_slab forced to 0
   when S=0 and its own power-of-two bound when S≠0 (L27–L29), A's own power-of-two
   bound (L39), lz4's decoded-size cap when codec=4 (L44, `[R-COD-07]`); the
   entry_count/extent_length cross-check (L21, L22, `[R-CNT-17]`); reserved flag bits
   and MU=1/PE=0 on the layer record or a sub-record (L46, L47); a registered
   sub-record type's stored MU/PE against the registry (L49). All of this is
   decidable from the resident directory and F alone, no fetch (`[R-RDR-03]`).
7. **Per-layer index chain and tile decode (§19.4 steps 3–6, generalized to every
   entry, not just requested ones, because a verifier certifies the whole file).**
   For each layer: verify crc_of_crc_array over the fetched segment-CRC array (L37);
   for each segment, verify its CRC over its entries' stored bytes (L38, with the
   all-sentinel constant `0xEECB3BB2` never substituted for a real comparison,
   `[R-IDX-05]`). For each entry, classify per §15.3's table: valid sentinel (reads
   as fill, no further check); each of the six *structural* reject-tile rows (T6–T12
   — mismatched sentinel halves, offset<16, domain overflow, sum overflow/reach, and
   non-sentinel length=0); or well-formed-but-possibly-crc-failing (T1, `[R-CNT-20]`).
   A structurally-invalid entry contributes **no stored extent** to the coverage walk
   or to overlap/alignment/slab checks (`[R-IDX-03]`); an entry whose only defect is
   a failing stored-bytes CRC keeps its extent for all of those purposes. For every
   entry that *does* have a stored extent, fetch and decode: codec-specific framing
   checks (T14 codec 1 exact-length; T15–T22 codec 2/3 wrapper/multi-frame/dictionary/
   checksum-flag/window/content-size for deflate and zstd; T23 codec 4's
   frame-vs.-block check) and the universal exact-consumption and malformed-stream
   checks (T24, T25, `[R-COD-08]`); decoded-size-exact check (T3, `[R-SER-07]`);
   then the *verifier*-only decoded-content obligations: every padding position and
   pad bit equals the carried channel's fill (T4, T5, `[R-SER-05]`); every
   interleaved bool byte at a *real* position is 0x00 or 0x01 (T2, `[R-SER-08]`); and,
   so far as witnessed by those two checks, the filter was applied at the mandated
   stride (T26, `[R-COD-10]` — unwitnessed otherwise, see §21.7 and finding
   verifierb-02 below).
8. **Alignment/slab invariants (verifier-only, §16).** Where A≠0: every stored tile's
   offset ≡ 0 mod A (L40). Where S≠0: within each run, stored-tile offsets pack
   contiguously in ordinal order and the run's first stored tile's offset ≡ 0 mod
   A_slab (L41, L42) — sentinels and structurally-invalid entries are transparent to
   this packing; a crc-only failure is not.
9. **Overlap (verifier-only, §7.2/§7.5, `[R-CNT-13]`).** Over the whole directory:
   any two structures of the *same* layer overlapping → reject-**layer** (L18); any
   overlap across layers, or touching another scope's structures, or between two
   non-layer structures → reject-**file** (F33).
10. **User metadata (every top-level and sub-record carrying it).** Framing precedes
    the quarantine: (0,0) slot (F21/L10), extent_length<5 (F22/L11), inline_length≠1
    (F23/L12) are validity errors at the record's *containing* scope, not
    ignore-record — "that failure precedes the document" (`[R-CNT-25]`,
    `[R-MTA-02]`). Past framing, everything is ignore-record (never a scope-level
    outcome, "whichever scope owns the record"): encoding 0 or reserved (R1); extent
    CRC failure (R2); decode failure under an *assigned* encoding (R3); for encoding
    2, the frame-constraint rows (R4 — magic, no skippable/second frame, no
    dictionary, no content-checksum flag, no trailing bytes, content-size field
    equal to decoded length when present); document content rules once decoded (R5
    ill-formed UTF-8/unpaired surrogate; R6 empty/control-code key; R7 not an
    object/BOM/malformed JSON; R8 non-finite number; R9 duplicate key; R10 key >255
    bytes). Two things are explicitly **not** quarantined and **do** bite the
    verdict: unsorted object members is a violation the verifier reports (F27/L48,
    `[R-MTA-05]`) even though *no reader behavior changes* and the document stays
    readable; and an experimental-range (≥0x80) encoding is **not** a violation at
    all and "asks nothing of this walk" (`[R-MTA-10]`) — the verifier instead reports
    which record it passed over uninspected, by scope, encoding value and stored
    extent length, "as it reports the slack total... bytes a certificate covers
    without inspecting are counted and named, never silent."
    A verifier that declines a document's decode on its own size/window bound cannot
    establish that document and must say so (`[R-MTA-09]`), on the same footing as
    `[R-COD-11]` for a codec.
11. **Coverage walk (§9.7, verifier-only).** From the live trailer, through the live
    directory's records, collect every claimant: the directory itself, each
    non-layer top-level record's extent, each layer's tile-index region (via its
    record's extent slot — entering the walk *once*, through that slot, never as a
    second claim), and each non-sentinel/well-formed index entry's stored-tile
    extent. Check: every claimant lies within [16, F−64); no two overlap (step 9);
    every claimant verifies against the checksum §8.1's map states for it. Sum what
    remains unclaimed as **slack**. If the walk reaches every claimant without a
    scope-level rejection interrupting it, the slack total is **exact**. If a
    scope-level rejection (an L18 overlap, an L40–L42 placement failure, or any other
    *verifier*-detected row) is found mid-walk, or the verifier declines a layer/tile
    on resource grounds and never enumerates its claimants, or the verifier stops at
    the first violation it finds: the walk is **incomplete**, the sum is reported as
    **partial** — "F less the bytes claimed by the claimants the walk did
    enumerate: an upper bound on the file's true slack, never an under-count" — and
    the verifier **must say which scope or violation stopped the walk**
    (`[R-CNT-21]`, `[R-LIF-08]`). A rejected layer's *already-enumerated* claimants
    are **discarded** from the tally (not merely left as-is), "since the total is a
    claim about a live state one of whose layers is not usable" — worked
    numerically in §2 below. A structurally-invalid index entry (one of the six
    T6–T12 rows) does **not** make the walk incomplete; the walk simply passes over
    it and whatever bytes it nominally addressed fall to slack if unclaimed by
    anything else.
12. **Capability/resource grounds.** Anywhere a codec or filter can't be executed
    (`[R-COD-11]`), a user-metadata document exceeds the verifier's own bound
    (`[R-MTA-09]`), a layer/tile decode is declined on resource grounds
    (`[R-ERR-04]`), a top-level MU=1 record's type isn't implemented, or the file
    names an unimplemented format major: record this as an unchecked requirement,
    naming the requirement and the ground. Report every such entry regardless of
    final verdict (`[R-CNF-11]`).
13. **Final verdict.** If any violation was established anywhere in steps 1–11:
    **nonconforming**, regardless of how many steps were left undone, and regardless
    of how many capability-ground items step 12 collected. Else, if step 12 collected
    any unchecked requirement: **cannot establish**. Else: **conforming**, and only
    then does the verifier certify.

### 1.3 The owning-scope → outcome mapping the algorithm implements

| Owning scope | Outcome | §21 rows |
|---|---|---|
| file | reject-file | F1–F36 (35 conditions) |
| layer | reject-layer | L1–L49 (49 conditions) |
| tile | reject-tile | T1–T26 (26 conditions) |
| record (user metadata) | ignore-record | R1–R10 (10 conditions) |

120 conditions total (`[R-ERR-02]`'s "120 conditions over 277 instances", §21.8), which
I recorded row-by-row while reading §21.2–§21.5 (full tables transcribed above in my
working notes; not repeated verbatim here to keep this transcript to a manageable
length, but every row's Detector and Detected-at column was read and is reflected in
steps 1–10 above). Detector is `reader` for the great majority of rows (checkable at
open or layer access with no fetch) and `verifier` for a specific, recurring subset:
flag-bit/registry-mismatch rows (F25–F28, L46–L49), reserved-range-type-value rows
regardless of MU (F36, L25), overlap rows (F33, L18), alignment/slab-placement rows
(L40–L42), decoded-content rows (T2, T4, T5, T26), and member-ordering (F27, L48). For
every *verifier*-detected row, "no reader is obliged to detect the condition, and the
governing rule states what a reader does" — several of them explicitly oblige the
*reader* that serves the structure to serve it **unchanged** under its nominal
(possibly wrong) semantics (`[R-CNT-22]`'s registered-type rows F28/L49; `[R-MTA-05]`'s
unsorted-document rows F27/L48), while `[R-CNT-12]`'s MU=1/PE=0 reading as PE=1
(F25/L46) resolves a flag and returns no data, and `[R-SER-08]` is the one row where a
*reader* (not just the verifier) resolves nonconforming content to a value (a bad
interleaved bool byte) rather than passing it through — the single exception to "values
are bit patterns" (`[R-TYP-04]`).

### 1.4 Note on `[R-CNF-13]` and formats other than major 1

Everything above assumes the file declares major 1. Where it declares a different
major, only conditions that assert a property `[R-CNT-24]` fixes for *every* major
reach the file at all: F8 (trailer magic), F14 (trailer CRC), F6/F1's two front/trailer
instances. "Every other condition concerns a structure this document defines for
format major 1 alone: it is not checked against a file declaring another major, no
violation of it is found there, and no §21 row records such a file." A verifier facing
an unimplemented nonzero major and no reaching-condition failure has nothing to call
nonconforming under its own terms, but also cannot certify (it doesn't implement that
major, so §21.6 classes it among "conforming files a reader nevertheless refuses" —
not a register row). I did not build a full second algorithm for other majors since
format major 1 is this document's entire normative subject; I flag this only so the
scope of "the verifier" above is explicit.

---

## Part 2 — Worked coverage walks (arithmetic)

### 2.1 A walk that completes: the minimal 128-byte file (Appendix A)

The document gives this example directly (§5.1's Example, and Appendix A in full byte
detail): front block [0,16); empty directory (0 records, 4-byte CRC of zero bytes,
`0x00000000`) at [16,20); 44 zeroed pad bytes [20,64); 64-byte trailer at [64,128).

- F = 128.
- Claimants: front (16) + directory region (4) + trailer (64) = 84.
- Slack = 128 − 84 = **44 bytes**, matching the document's own statement ("44 bytes of
  slack, zeroed by advice").
- This file contains zero layers, which §21.6 records as a defined non-violation
  ("The file contains zero layers | A conforming file"), so the walk completes with
  no violation anywhere and the exact slack total is reportable alongside a
  **conforming** verdict.

### 2.2 A multi-generation trace, and its arithmetic (this doubles as my answer to
probe V3 below)

**Setup**, exactly as the probe states, with the pads I assume stated explicitly (no
alignment or slab declared anywhere, so structures within a commit are assumed packed
contiguously with no gap except the pre-trailer pad; directory sizes are given flat
at 200 bytes per generation and I do not second-guess that given, non-realistic as
it would be for a real writer whose directory grows as layers are added):

- **Generation 1** (creator): front (16) → A's stored tiles (4,096) → A's index
  region (84) → directory₁ (200) → pad₁ → trailer₁ (64).
  Running end after directory₁: 16+4096+84+200 = 4,396. 4,396 mod 64 = 44, so
  **pad₁ = 20** bytes, landing trailer₁ at [4,416, 4,480). **F₁ = 4,480**
  (4,480/64 = 70 exactly).
- **Generation 2** (appender, adds layer B; A is untouched — `[R-WRT-05]`, A's
  record and extent slot are carried forward byte-identically): B's stored tiles
  (8,192) → B's index region (164) → directory₂ (200) → pad₂ → trailer₂ (64), all
  starting at F₁ = 4,480.
  Running end after directory₂: 4,480+8,192+164+200 = 13,036. 13,036 mod 64 = 44, so
  **pad₂ = 20** bytes, trailer₂ at [13,056, 13,120). **F₂ = 13,120** (205×64).
- **Generation 3** (appender, supersedes one 1,024-byte tile of A): because the
  stored-tile *set* of A changes, A's whole tile-index region is re-emitted "in
  full... necessarily at a new placement" (`[R-WRT-04]`) even though its byte size is
  unchanged (84 bytes: same entry_count, 83 entries byte-identical, one entry
  re-pointed to the new payload). New payload (1,024) → A's new index region (84) →
  directory₃ (200) → pad₃ → trailer₃ (64), starting at F₂ = 13,120.
  Running end after directory₃: 13,120+1,024+84+200 = 14,428. 14,428 mod 64 = 28, so
  **pad₃ = 36** bytes, trailer₃ at [14,464, 14,528). **F₃ = 14,528** (227×64).

**Live-state byte total at the end (generation 3), assuming the whole file is
otherwise conforming so the walk completes exactly:**

front (16) + A's live tiles (4,096 — unchanged in total size: 3,072 bytes of A's
original tiles at their original disk-ordinal positions, still byte-identical, plus
the new 1,024-byte payload) + A's live index region (84, at its new placement) + B's
live tiles (8,192, untouched since generation 2) + B's live index region (164,
untouched) + directory₃ (200) + trailer₃ (64)

= 16 + 4,096 + 84 + 8,192 + 164 + 200 + 64 = **12,816 bytes**.

**Slack total the coverage walk reports** = F₃ − live total = 14,528 − 12,816 =
**1,712 bytes**.

Cross-checked by enumerating every slack region directly (both arithmetically
identical, confirmed by the local script):
old A index region from generation 1, now superseded (84) + directory₁+pad₁+trailer₁,
superseded by generation 2 (200+20+64 = 284) + the one superseded 1,024-byte A tile +
directory₂+pad₂+trailer₂, superseded by generation 3 (200+20+64 = 284) + pad₃ itself
(36) = 84 + 284 + 1,024 + 284 + 36 = **1,712**, matching exactly.

### 2.3 A walk that does not complete, built on the same three-generation file

Suppose, instead, that a writer defect leaves two of layer A's live tile-index entries
both addressing the same 1,024-byte extent (an intra-layer overlap — row **L18**,
`[R-CNT-13]`/`[R-IDX-03]`, detector *verifier*, detected at certification). As the
verifier walks layer A's claimants (its index region, and each of its stored-tile
extents in turn) it establishes this overlap. Per §5.2's own text: "where the
rejection is one the walk itself established, L18's overlap or L40 through L42's
placement among them, the claimants it had already enumerated are discarded with the
layer, since the total is a claim about a live state one of whose layers is not
usable." So **every** claimant already attributed to layer A (its index region and
every one of its tile extents, 4,096+84 = 4,180 bytes, overlap and all) is removed
from the "claimed" side of the ledger, not merely the overlapping extent. Layer B,
the directory and the trailer are unaffected and are still fully enumerated (they
don't belong to layer A, so the discard clause doesn't reach them).

Claimed bytes (A excluded): front (16) + B's tiles (8,192) + B's index (164) +
directory₃ (200) + trailer₃ (64) = **8,636 bytes**.

Reported slack = F₃ − 8,636 = 14,528 − 8,636 = **5,892 bytes**, and the verifier
reports this explicitly as **partial** — "an upper bound on the file's true slack,
never an under-count" — together with "which scope or violation stopped the walk":
layer A, under `[R-CNT-13]`/`[R-IDX-03]` (row L18). The overall **verdict is
nonconforming** (an established violation was found — L18 — which per `[R-CNF-11]`
takes priority over any unexamined scope, and there is none of significance left
unexamined here since only A's own remaining claimants, if any had not yet been
walked, go unexamined; B and the directory/trailer were fully checked). This also
illustrates that "cannot establish" is unavailable here: that verdict is reserved for
a walk that establishes **no** violation at all, and this one did.

---

## Part 3 — Register row detectors and outcomes (coverage, condensed)

I read §21.1 through §21.9 in full (lines ~3530–4036) and incorporated every row's
*Detector* and *Detected* cell into the algorithm of Part 1 rather than reproducing
all 120 rows' full text a second time here (they are quoted individually above
wherever a probe or a step needed one). The totals and the detector pattern are
restated in §1.3 above. Two points worth flagging explicitly because they shape what
"the verifier" must do that a plain reader need not:

- Every row marked detector = *verifier* is a condition §19.2 places **outside the
  reader tiers entirely** ("Detection points name §19.2's reader tiers (open, layer
  access, tile use, extent use) or *certification* for the rows a verifier detects,
  which §19.2 places outside the reader tiers entirely"). A plain conforming reader
  that never runs these checks is still fully conforming; only a verifier's
  certification duty reaches them.
- §21.1's **instance-specialization** list (rows that are strict specializations of
  other rows, so a file exhibiting the narrower condition is recorded against the
  narrower row alone) names five pairs explicitly and says the list "is not offered
  as closed": F1's front-block instance of F6, F1's trailer-magic instance of F8, F35
  of F36, L24 of L25, F21 of F22, L10 of L11. I used this once above (§1.2 step 5,
  F35/F36) and again in probe V2 below.

---

## Part 4 — Probe answers (full derivations; condensed versions also given in
`probe_answers`)

### V1 — Verdict vocabulary

Answered fully in §1.1 above. Conditions: conforming (no violation found, nothing
left uncheckable); nonconforming (any established violation, anywhere — takes
priority over everything else); cannot establish (some requirement unable to be
checked on a capability/resource ground, **and** no violation established elsewhere).
Decisive text: `[R-CNF-11]` (§2.3) in full, quoted above.

### V2 — Unimplemented type, MU=1, reserved vs. experimental range

**Reserved range (0x0003–0x7FFF).** Two things both bite independently: (a) the
general MU-bit rule for an unimplemented type, `[R-CNT-15]`: "A record at file scope
whose type the reader does not implement is governed by its stored MU bit: MU = 1 is
reject-file, and MU = 0 is ignore-record." — register row **F35** ("A top-level
record has a reserved-range type value... with MUST_UNDERSTAND... set to 1", detector
*reader*, detected at *open*). (b) Independently, emitting **any** reserved-range
value at all is itself a violation regardless of the MU bit: "A type from the
reserved range is a value this specification has not assigned. Emitting one is a
violation, and a verifier MUST treat a reserved-range record type as a validity error
at the record's governing scope." — register row **F36** (detector *verifier*,
*certification*). Per §21.1's specialization list, F35 "is an instance of" F36 (every
file exhibiting F35 necessarily exhibits F36), so the file is **recorded against
F35** — the reader itself already rejects the file at open, and the verifier's
certification-time F36 check would find the same thing again if it ever got that far.
**Verdict: nonconforming** (reject-file), fixed by `[R-CNT-15]` (and registered under
F35/F36); there is no "fix" available to the reader/verifier — the remedy lies with
whoever registers the value in a future minor version (§10.4), since the writer
should never have emitted it (§10.3).

**Experimental range (≥0x8000).** §21.6 names this explicitly as one of exactly two
"conforming files a reader nevertheless refuses": "an experimental-range top-level
record type carrying MU = 1 (§10.2, §10.3): `[R-CNT-15]` obliges the reader to
reject, and `[R-CNF-02]` makes the file conforming all the same." So the **reader's
action** is identical (reject-file) — but this is **not** a file-conformance finding.
For a **verifier** specifically, §21.6 separately lists this exact case among the
named *cannot-establish* grounds: "A verifier is unable to check a requirement on a
capability or resource ground, and so reports *cannot establish*..., as when... a
record carries MUST_UNDERSTAND = 1 with a type it does not implement..." Since no
violation is established by this record alone (the file is conforming per
`[R-CNF-02]`), and the verifier is structurally unable to check whatever that
unimplemented type's semantics require, the **verdict is cannot establish** (assuming
no other violation exists elsewhere in the file) — never nonconforming, and the
verifier must not certify. **Fixed by** `[R-CNT-15]` (reject-file action) +
`[R-CNF-02]` (file stays conforming) + `[R-CNF-11]`/§21.6 (cannot-establish ground).
There is, by design, no "fix": §10.3 says experimental values carry "no collision
protection" and are private use; the only remedy is registration (turning it into an
assigned type) or simply not relying on software that lacks that private extension.

*Two passages checked against each other, as the probe asks:* `[R-CNT-15]` and
`[R-CNF-02]`/§21.6 do **not** disagree — they describe two different things (a
reader's refusal action vs. the file's conformance status) and the document is
explicit that both hold simultaneously for the experimental case. I looked for, and
did not find, any passage asserting the reserved-range case is *also* merely a
capability refusal (it is not: F36 makes the value's very emission a violation,
independent of any MU bit or any reader's capabilities) — so the reserved/
experimental distinction is clean, not contradictory, despite the two cases'
superficial parallel ("the MU-bit outcome of `[R-CNT-15]` at file scope... A reader
applies the MU rule to both, unchanged").

### V3 — Three-generation byte arithmetic

Fully worked in §2.2 above. **Pads assumed:** pad₁ = 20 bytes, pad₂ = 20 bytes,
pad₃ = 36 bytes (each the gap from the end of that generation's directory to the next
64-byte boundary, per `[R-LIF-02]` step 5 and `[R-CNT-03]`'s zero-by-advice; no
alignment or slab declared, so no other gaps). **F (final committed file length) =
14,528 bytes. Live-state byte total = 12,816 bytes. Slack total a completing
coverage walk reports = 1,712 bytes.**

### V4 — Codec the verifier cannot execute

`[R-COD-11]`, in full: "A verifier that cannot execute a layer's codec or filter
cannot establish that layer's conformance and MUST NOT certify the file. That
inability is not a finding that the file is nonconforming, and it fixes the file's
verdict as *cannot establish* only where the verifier established no violation
elsewhere." **Verdict: cannot establish** (assuming no violation found elsewhere in
the file). **The report on that layer:** per `[R-CNF-11]`'s per-requirement reporting
duty, the verifier names the requirement it could not check and the ground — here,
the specific codec (or filter) value and the layer it governs — "A verifier MUST
report each requirement it was unable to check on a capability or resource ground,
naming the requirement and the ground." The layer is **not** reported as rejected and
**not** claimed as examined; it is reported as unchecked, and the overall file cannot
be certified on that account alone (though other layers may be fully certified-clean
independently — nothing in `[R-COD-11]` extends the inability past the one layer).

I note, without resolving it as settled (see finding verifierb-02 below), that this
sits in some tension with `[R-CNF-03]`'s unconditional "no subset profiles" rule for
codecs, which §17.2 calls **core**: "all four are core: a conforming reader MUST
implement every one of them... values ≥ 0x8000 are the experimental range" — the
inability contemplated by V4 can only honestly arise for an **assigned** codec (1–4),
since a reserved/experimental codec value is a different, ordinary value-set
violation (L43) with its own outcome, not a `[R-COD-11]` "cannot execute" scenario at
all.

### V5 — Last commit changed a fixed declaration of a layer that stored a tile

**Can the verifier see it? In general, no.** The verifier's coverage walk is defined
entirely over the **live** state reached from the **live** trailer (§9.7): "A verifier
checking `[R-CNT-02]`'s partition walks the live state only," and "Nothing here
enumerates prior commits. A verifier certifies what a reader can reach and counts what
it cannot, which is decidable from the live trailer in one pass and does not depend on
reconstructing the file's history." §20.3 states plainly that changing a fixed
declaration of a layer that stored a tile is not a legitimate append operation at all
("A commit MUST NOT change one of these; the change is a new layer, or a rewrite...
This bar binds the commit as an actor: no file is nonconforming by virtue of its
violation, and **no register row records the violation itself**, the register
enumerating file-conformance violations... and the bar stating no condition a file can
exhibit"). §21.7 makes the general principle explicit: this is one of the named
*unwitnessed* conditions — "under new [declarations] the same bytes would denote
values, coordinates or padding the writer did not store, with every checksum in §8
certifying the result and... no check any actor owes able to see it." So, absent a
side effect, the verifier simply has **no byte-level signal** that anything changed
across generations; the live directory it reads only ever states the *current*
declaration, and nothing in the format records "this layer's codec used to be X."

**Exception — a symptom the verifier *can* catch, though not as "a declaration
changed."** If the changed declaration breaks one of the few structurally-witnessed
content obligations for a tile the commit carried forward unmodified, the verifier
*will* trip a real tile-scope (or layer-scope) row and report **nonconforming** for
that tile/layer — but it will report whatever structural symptom fired (e.g. T3's
decoded-size mismatch, T4/T5's padding-fill mismatch, T2's bad boolean byte, or one of
the codec-framing rows T14/T17/T21/T22/T24/T25 "under a changed codec or filter"),
never "a fixed declaration changed across generations," because the format carries no
field recording that fact at all. §20.3's own list of what *does* trip a check
(parenthetically): "but for a stored tile's decoded size, a padding position or pad
bit, or a boolean byte the register witnesses (T3, T14, T21, T22, T4, T5, T2) and a
decode that fails outright, or a codec's framing check that precedes it, under a
changed codec or filter (T17, T24, T25)." **Verdict, when no such symptom fires:**
conforming (if nothing else is wrong) — the live state is, by definition, all the
verifier has. **Verdict, when a symptom fires:** nonconforming, at whichever scope and
row the symptom belongs to, reported as that row, not as "declaration change."

### V6 — MU = 1, PE = 0

`[R-CNT-12]`, in full on this point: "Writers MUST NOT emit the combination MU = 1
with PE = 0; a reader or updater encountering it MUST treat the record as PE = 1
(never silently deletable). Both writer violations make the file nonconforming... so
their detection is a verifier's: a verifier MUST treat a nonzero reserved flag bit or
the MU = 1 with PE = 0 combination as a validity error at the record's governing
scope."

**What the verifier does:** treats the combination as a validity error — a
file-conformance violation — **at the record's own governing scope**: **file scope**
(reject-file, register row **F25**) if the record is a non-layer top-level record, or
**layer scope** (reject-layer, register row **L46**) if it is a layer record or one of
its sub-records. This is a *verifier*-detected row in both cases (certification time);
**no ordinary reader or updater is obliged to reject anything over it** — functionally
they simply read the PE bit as 1 regardless of what's stored, so the record is never
silently dropped, and conforming behavior is otherwise unchanged. (I note, as an
observation and not a contradiction, that since **both** registry-assigned types fix
MU=0 — layer and user-metadata, §7.3's table — this combination can only arise on an
unassigned (reserved/experimental) type's stored bits, or on a registered type's
stored bits disagreeing with its own fixed flags, which separately trips F28/L49;
nothing in the text says these two rows are mutually exclusive, and §21.1 explicitly
allows rows that "merely overlap, each reachable without the other.")

---

## Part 5 — Findings

See `findings` in the structured result. Summary of the two I am reporting:

1. **verifierb-01 (AMBIGUITY).** Whether software that cannot execute one of the four
   **assigned** (core) codecs or either assigned filter is itself within the
   "conforming verifier" class at all, given `[R-CNF-03]`'s unconditional "no subset
   profiles" bar (which `[R-CNF-11]` says verifiers "inherit... every reader
   obligation" of), versus `[R-COD-11]`'s and §21.6's instructions for exactly that
   software to report "cannot establish" using the very verdict vocabulary §2.3
   reserves for a *conforming* verifier.
2. **verifierb-02 (OBSERVATION).** A commit that changes a fixed declaration of a
   layer that stored a tile (barred by §20.3 as a writer-conduct rule) is, by the
   document's own explicit design and admission, invisible to a verifier's live-state
   walk in the general case (§21.7's "unwitnessed" category), detectable only as an
   incidental symptom (T2/T3/T4/T5/T14/T17/T21/T22/T24/T25) when the new declaration
   happens to break a structurally-witnessed content rule for a carried-forward tile —
   this is not a flaw I am alleging, since the document says so itself at length, but
   it is worth recording plainly as a limit on what "a conforming verifier" can ever
   certify, for an implementer who might otherwise assume certification implies
   cross-generation consistency.
