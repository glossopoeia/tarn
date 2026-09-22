# Transcript — verifier implementer, edition A

## Disclosure

**Access.** I read exactly one file, in full, via the Read tool in eight
sequential chunks (offsets 1, 700, 1400, 1900, 2400, 2900, 3399, 3898, 4397,
4696), covering all 4,981 lines of
`/Users/robertkleffner/Documents/GitHub/tarn-first-draft/scratch/cleanroom/editions/a/tarn.md`.
I read no other file in this repository: not docs/, not PLAN.md, not
AGENTS.md, not conformance/, not spec/registry.json, no git history. I did
not list any directory other than my own scratch directory (to confirm it
was empty at the start) and the output directory's parent (to create it with
`mkdir -p`; I did not list its contents). I ran two `grep` searches against
the target file itself (`cannot establish`, `does not implement`) to check
for passages I might have paraphrased imprecisely, and one local Python
script (arithmetic only, no file I/O beyond writing its own source and
reading nothing) to check the multi-generation byte arithmetic for probe V3.
No web search, no web fetch.

**Context that arrived unrequested.** My context contained, before I began:
a project file naming another document by reference; an auto-memory index of
notes with editorialized titles about a "TARN" project (gates, harnesses,
repairs, ADRs, subagents, refute phases, etc.); a git status block naming
five recent commit subjects (mentioning "ADR-0133", "ADR-0132", ADR audits,
repairs, and inventory/equivalence tooling); and an attribution/formatting
instruction block. None of this is part of the specification and I have
treated none of it as evidence about the specification's content. I am not
repeating its contents beyond this generic description, and I have not acted
on anything it might imply. The harness's own framing (a "user request" to
"Accept ADR-0133 and run the calibration round") is a request to run this
fidelity-round exercise; it says nothing about the spec's content either,
and I have not treated it as such.

**Path check.** The file I was told to read was present at exactly the path
given, and nothing about the path (`scratch/cleanroom/editions/a/tarn.md`)
tells me anything about the content beyond what I read there.

**Scratch directory.** `/private/tmp/claude-501/-Users-robertkleffner-Documents-GitHub-tarn-first-draft/fidelity-1/scratch/walk-verifier-a/`
was empty when I created it (verified with `ls -la`, no prior-attempt files
found). I wrote `v3_arithmetic.py` there for the V3 computation, and this
draft transcript before copying it to the final output path.

**Hard-wrap caution.** I read the file with a tool that returned full lines
(not re-wrapped my own way), and cross-checked several load-bearing phrases
that I quote below by locating them in the sequential reads rather than by
line-oriented grep, per the brief's warning. Where I did grep (the two
searches above), both were short fragments (`cannot establish`,
`does not implement`) chosen because neither is likely to straddle a
hard-wrap line break in ordinary prose, and both returned multiple hits
consistent with what I'd already read, so I treat them as confirmatory
rather than as my primary evidence.

---

## Part 1 — The certification procedure as an ordered algorithm

### 1.1 Verdict vocabulary (§2.3, `[R-CNF-11]`)

A verifier is "a reader that additionally checks every file-level
requirement — including those ordinary readers are exempted from — and
certifies conformance." It reports exactly one of three verdicts:

- **conforming** — issued only when the verifier has checked everything it
  is obliged to check, has established no violation anywhere, and has no
  outstanding capability/resource ground it could not check. ("A file is
  conforming only if it satisfies every requirement at every scope... a
  verifier certifies only violation-free files", §2.4/`[R-CNF-12]`.)
- **nonconforming** — issued whenever the verifier has established *any*
  violation, "however many requirements it was unable to check" — an
  established violation takes absolute priority over unresolved
  capability/resource grounds.
- **cannot establish** — available *only* to "a traversal that established
  no violation" and that nonetheless has some requirement "it is unable to
  check on a capability or resource ground" — named examples: an
  unimplemented format major, an unimplemented top-level MU=1 record type,
  an unexecutable codec/filter (`[R-COD-11]`), a tile or layer decode
  declined on resource grounds (`[R-ERR-04]`, `[R-SER-05]`, `[R-SER-08]`),
  or a declined user-metadata document decode (`[R-MTA-09]`). "*Cannot
  establish* is not a finding that the file is nonconforming, and a
  verifier MUST NOT certify a file it reports that way."

A fourth word, **unexamined**, appears in the report but is explicitly *not*
part of the verdict vocabulary: "*Unexamined* is neither a verdict nor
*cannot establish* — it constrains the report, not the verdict." It marks a
scope the verifier chose not to visit after stopping at a first violation
(licensed by `[R-CNF-11]`'s "MAY stop at the first violation it finds").

Independently of the verdict, the verifier's *report* (not its verdict) must
separately carry: (a) every requirement it was unable to check, naming the
requirement and the ground, "whichever of the three verdicts it reports";
(b) if it stopped early, every scope marked unexamined; (c) the live-state
slack total, exact if the walk completed, or explicitly marked *partial*
(an upper bound) naming the scope/violation that stopped the walk, if it did
not (`[R-CNT-21]`, `[R-LIF-08]`); (d) each user-metadata record it ignored
under an experimental-range encoding, naming owning scope, encoding value,
and stored extent length (`[R-MTA-10]`).

### 1.2 The algorithm

Consolidating §6.2, §7.1, §9.7, §19.1–19.4, §17.4/§18.2 (decode declines),
and Appendix H's "Conforming verifier" checklist, a verifier's ordered
procedure is:

1. **Obtain F** (transport-authoritative file size). F < 128 → reject-file,
   established violation (F5, `[R-CNT-27]`) — **stop, verdict nonconforming**
   (no live state, no slack total owed at all — `[R-CNT-21]`: "there is no F
   and no live state to walk... the total is not owed at all").
2. **Trailer**, in §6.2's fixed order: magic (F8) → trailer CRC (F14) →
   version gate (F18/`[R-CNT-07]`'s capability refusal) → remaining field
   gates (flags F19, dir_offset F9, dir_length F16, dir bounds F10, F17
   length check, F12 file_id, F15 reserved). Any failure among F8/F9/F10/
   F12/F14/F15/F16/F17/F19 → established violation, reject-file →
   **nonconforming**. version_major = 0 → F18, likewise nonconforming
   (`[R-CNT-07]` on the "declares no major at all" branch). version_major
   naming an *unimplemented nonzero* major is a **capability** refusal, not
   itself an established violation, *except* that `[R-CNF-13]`'s
   "reaching" conditions (the ones `[R-CNT-24]` fixes across every major —
   F1's trailer-magic instance, F6/F8, F14) still apply and can themselves
   be established violations regardless of major. If only the
   unimplemented-major refusal applies (no reaching condition failed): this
   is a capability ground → contributes to **cannot establish** if nothing
   else is wrong. Also unlike a reader, the front-signature-block check
   (F1/F6, `[R-CNT-04]`'s residency exemption) is **not** available to a
   verifier: "a verifier holds no such exemption" — it always checks bytes
   [0,16) by equality.
3. **Directory.** Fetch [dir_offset, dir_offset+dir_length), verify its CRC
   (F20) before any other use, then parse the record sequence under §7.2
   framing (F24 type=0, F29 overrun/residue, F2/F3 domain/sum overflow on
   non-layer records, F30/F31/F32 extent-slot validity, F34 duplicate
   top-level user-metadata, F21/F22/F23 user-metadata framing, F35/F36
   reserved-range MU handling). Any failure → **nonconforming**.
4. **Layer-name namespace** (F4, `[R-ENC-15]`/`[R-ENC-13]`): duplicate
   byte-identical layer-record names → **nonconforming**, decided on raw
   bytes regardless of each name's own validity.
5. **Per non-layer top-level record, verifier-only checks**: reserved flag
   bits (F26), MU=1/PE=0 (F25), registered-type flag mismatch (F28),
   unsorted user-metadata document members (F27) — each **verifier**-
   detected, at *certification*, each an established violation if present.
6. **Per layer record, full §19.3 validation** (extent slot L15/L16/L17;
   §7.4 constraint set L1/L2/L27–L45; exact parse and sub-record walk
   L13/L14/L23/L24/L26; sub-record multiplicity L19; name rules L3–L9;
   user-metadata sub-record framing L10–L12; index cross-check L21/L22).
   Any failure → that layer **rejected** (reject-layer) — the *file* is
   still nonconforming (a verifier "certifies only violation-free files"),
   but the blast radius recorded is the layer, and the verifier does not
   enumerate that layer's claimants for the coverage walk (§9.7).
7. **Per layer, verifier-only structural checks**: extent-slot overlap
   inside the layer (L18); reserved-range sub-record type (L25); layer/
   sub-record reserved flag bits (L47), MU=1/PE=0 (L46), registered-type
   flag mismatch (L49); unsorted layer-scope user-metadata (L48); alignment
   invariant (L40, `[R-SLB-01]`); slab run-continuity and first-tile
   alignment invariants (L41/L42, `[R-SLB-03]`). Any failure → reject-layer,
   file **nonconforming**.
8. **Per layer, index-chain verification** (`[R-IDX-04]`): crc_of_crc_array
   over the fetched segment-CRC array (L37); each segment CRC over its
   entries as stored (L38). Failure → reject-layer.
9. **Per tile-index entry, classify per §15.3** (`[R-IDX-03]`): sentinel
   valid; T6/T7 malformed sentinel-adjacent; T8/T9/T10/T11/T12 structural
   bounds. A *structural* failure contributes no stored extent to anything
   downstream (walk, run-continuity, verifier rows) — "the walk passes over
   it." An entry whose *only* defect is a failed stored-bytes CRC (T1) is
   still well-formed for these purposes; its extent stands.
10. **Per stored (non-sentinel, well-formed) tile: decode it** (this is a
    verifier-only obligation beyond ordinary reading — "A verifier that
    certifies decodes every stored tile"): verify entry CRC (T1) →
    codec-specific framing checks (T14–T24, per §17.2's codec) → decode →
    exact-size check (T3, `[R-SER-07]`) → filter inverse. If the layer's
    codec/filter cannot be executed by this verifier at all: **cannot
    check** §14's decoded-content obligations for that layer → contributes
    to *cannot establish* if nothing else in the file is wrong
    (`[R-COD-11]`). Decoded-content checks only reachable by decoding:
    padding-position fill content (T4, `[R-SER-05]`), packed-bool pad-bit
    fill content (T5), interleaved-bool byte domain (T2, `[R-SER-08]`),
    mis-strided filter with a structural symptom (T26, routed through T2/
    T4). Any positive finding here → reject-tile, file **nonconforming**.
11. **Coverage walk** (§9.7, `[R-CNT-02]`/`[R-LIF-08]`): from the live
    trailer, through the live directory's records/sub-records/tile-index
    entries, enumerate every claimant (front block; each record's extent;
    each stored, well-formed tile-index entry's stored extent; the
    directory; the trailer). Check pairwise disjointness (F33 across
    scopes/layers, L18 within one layer) and that each claimant's checksum
    (per §8.1's map) verifies. Check nothing occupies the pre-trailer gap
    outside the directory (F7, `[R-CNT-05]`). Sum unclaimed bytes as slack.
    If the walk enumerated every layer's claimants (no scope-level
    rejection, no resource-based decline, no early stop): slack total is
    **exact**. Otherwise: report it **partial**, naming what stopped it.
12. **User-metadata documents actually decoded** (only if a request/the
    certification path reaches them — §19.2's "at use of a record's
    extent" timing applies to the verifier too, since it is a reader):
    extent CRC (R2); encoding value set (R1); encoding-2 frame constraints
    (R4); JSON well-formedness/object/BOM (R7); finite numbers (R8);
    duplicate keys (R9); UTF-8/surrogate well-formedness (R5); key length/
    charset (R6, R10); member ordering (F27/L48, verifier-only, makes the
    *file* nonconforming even though the outcome for the record itself is
    ignore-record and readers process it unchanged). An
    experimental-range encoding is *not* a violation and attaches no
    content rule at all (`[R-MTA-10]`) — report it (scope, encoding value,
    extent length) but do not treat it as unchecked or as a violation. A
    decline on the size/window bound is a **cannot establish** ground
    (`[R-MTA-09]`), not a violation.
13. **Aggregate.** If step 2–12 established any violation at any point:
    verdict **nonconforming**, report every capability/resource ground
    encountered regardless, report slack (exact or partial), report any
    unexamined scopes if the verifier stopped early. Else, if any
    capability/resource ground was encountered (unexecutable codec/filter,
    unimplemented format major with no reaching-condition failure,
    unimplemented top-level MU=1 experimental-range type, declined
    document/tile/layer decode): verdict **cannot establish**, report the
    ground(s), report slack (partial, since at least one thing was not
    checked — unless the decline was of a kind §9.7 says leaves the walk
    complete, e.g. a tile decode declined still leaves its extent
    enumerated). Else: verdict **conforming**, report the exact slack
    total and any experimental-range records ignored (not violations, just
    reported).

---

## Part 2 — Coverage-walk arithmetic

### 2.1 A concrete file: the smallest conforming file (Appendix A, cross-check)

F = 128. Live state = front(16) + directory region(4, an empty record
sequence's CRC alone) + trailer(64) = 84 bytes. Slack = 128 − 84 = 44 bytes
(the pre-trailer pad, bytes [20,64)). This matches Appendix A's own account
("44 bytes of slack, zeroed by advice") and gives me a sanity-checked
baseline before the three-generation trace below.

### 2.2 V3's three-generation trace — the walk that completes

See Part 4, V3, for the full derivation. Result: F3 = 14,528 bytes;
live-state total = 12,816 bytes; slack = 1,712 bytes (verified two
independent ways: F3 − live_total, and direct enumeration of the nine slack
sources, both giving 1,712 — see `v3_arithmetic.py` in my scratch
directory).

### 2.3 The same file, but the walk does not complete

Take generation 3 exactly as built in V3, but suppose layer B's
crc_of_crc_array no longer matches the segment-CRC array actually stored at
the tail of B's tile-index region (an L37 violation, `[R-IDX-04]`). This is
a **verifier**-independent condition — actually detector *reader*, at *tile
use* per the register (L37's Detector cell is "reader"; but a verifier
performing coverage discovers it during its own attempt to walk B's
entries, since it cannot classify any of B's 8,192/… tile-index entries as
sentinel-vs-stored without first trusting the segment CRC that
`crc_of_crc_array` covers). The result: `[R-CNT-20]` in §8.2 makes this
outcome reject-layer for B. Per §9.7 (`[R-LIF-08]`): "a scope-level
rejection blocks enumeration" — B's tile-index entries and stored-tile
extents are never added to the claimant set (the verifier cannot determine
which of B's disk ordinals are stored versus sentinel without a verified
index, so it cannot even attempt to enumerate B's stored extents).

Consequences for the walk:
- The file's verdict is **nonconforming** (L37 is an established violation),
  regardless of the slack question — established violation takes priority
  over everything (`[R-CNF-11]`).
- The live-state total the verifier *can* still establish is only: front
  (16) + layer A's live tiles (4,096) + layer A's live index (84) +
  directory (200) + trailer (64) = 4,460 bytes. Layer B's 8,192+164 = 8,356
  bytes are **not** claimed (B's whole region — tiles and index alike —
  falls outside what the walk enumerated).
- F3 is still 14,528 (the trailer/committed_file_length gate is independent
  of B's index-chain failure and was validated earlier in the algorithm).
- Reported slack = F3 − 4,460 = 10,068 bytes, but the verifier MUST report
  this as **partial**, "naming the scope or violation that stopped the
  walk" (`[R-CNT-21]`) — here, layer B, L37/`[R-IDX-04]`. It is explicitly
  "an upper bound on the file's true slack, never an under-count": the
  8,356 bytes B *would* have claimed if its index had verified are counted
  as slack in this partial total even though they are almost certainly not
  actually slack (they are B's live tiles and index, just unreachable to
  this verifier's walk because of the corrupted checksum chain).

This exercises §9.7's and `[R-CNT-21]`'s distinction cleanly: a walk that
does not complete still yields a definite (partial) number, but that number
overstates true slack, and the report must say so and say why.

---

## Part 3 — Register rows: detector and outcome, by scope

I read all four register tables (§21.2–§21.5) in full, verbatim, from the
one file. Rather than re-transcribe all 120 rows a third time here (once in
my sequential read, once in my working notes), I summarize the structure
and detector/outcome split, which is what the charter asks me to "cover":

**File scope — reject-file (§21.2), 35 conditions, rows F1–F36 (F11
retired/struck, never reused, §2.2/§21.1's note).**
- Detector = **reader**, at **open**: F1 (front block/trailer-magic byte
  reversal), F2 (u64 domain overflow on dir/extent fields), F3 (sum
  overflow), F4 (duplicate layer name), F5 (file < 128 bytes), F6 (front
  block mismatch, resident-reader only), F8–F10, F12–F19 (trailer field
  gates in §6.2's fixed order, including the version/flag gates), F20
  (directory CRC), F21–F23 (top-level user-metadata framing), F24 (type 0),
  F29–F32 (record framing/extent-slot bounds), F34 (duplicate top-level
  user-metadata record), F35 (reserved-range type with MU=1).
- Detector = **verifier**, at **certification**: F7 (structure in the
  pre-trailer gap), F25 (MU=1/PE=0 on a non-layer record), F26 (reserved
  flag bits 2–15), F27 (unsorted file-scope metadata document), F28
  (registered-type flag mismatch), F33 (cross-scope/cross-layer extent
  overlap), F36 (reserved-range type emitted at all, any MU bit).

**Layer scope — reject-layer (§21.3), 49 conditions, L1–L49.**
- Detector = **reader**, mostly at **layer access** (a few name-field
  checks at **open**, per L23's split cell): L1–L17 (domain/sum overflow,
  UTF-8, name emptiness/control-chars, name uniqueness, user-metadata
  sub-record framing, sub-record type-0/framing, extent-slot bounds),
  L19–L36 (sub-record multiplicity, alignment/slab mutual exclusion,
  entry_count/extent_length cross-checks §7.4/`[R-CNT-17]`, inline-payload
  parse bounds, reserved-range sub-record type with MU=1, layer-as-
  sub-record nesting, entry_count/crc_of_crc_array zero-consistency, slab
  alignment consistency, fill-length/type consistency, index_encoding
  value set, geometry floors, linearization value set, channel-type value
  set, bool-fill byte domain, layout value set), L39 (alignment value
  domain), L43–L45 (codec/lz4-cap/filter value sets).
- Detector = **reader**, at **tile use**: L37, L38 (crc_of_crc_array and
  segment CRC verification — `[R-IDX-04]`).
- Detector = **verifier**, at **certification**: L18 (intra-layer extent
  overlap), L25 (reserved-range sub-record type emitted at all), L40
  (alignment invariant), L41/L42 (slab run continuity / first-tile
  alignment), L46 (MU=1/PE=0 on layer record or sub-record), L47 (reserved
  flag bits), L48 (unsorted layer-scope metadata document), L49
  (registered-type flag mismatch).

**Tile scope — reject-tile (§21.4), 26 conditions, T1–T26.**
- Detector = **reader**, at **tile use**: T1 (stored-bytes CRC), T3
  (decoded-size mismatch), T6–T12 (sentinel/structural entry-validity
  rows), T14 (codec-1 length≠decoded-size), T15–T24 (per-codec framing:
  deflate wrapper/second-stream, zstd magic/second-frame/dict-ID/
  content-checksum/window/content-size, lz4 frame-vs-block, trailing
  bytes any codec), T13 (recorded for state/side-data dependence — same
  underlying check as T25), T25 (malformed stream fails to decode).
- Detector = **verifier**, at **certification**: T2 (interleaved bool byte
  domain at a real position), T4 (padding-position fill content), T5
  (packed-bool pad-bit fill content), T26 (mis-strided filter with a
  structural symptom, routed through T2/T4's own checks).

**Ignore-record (§21.5), 10 conditions, R1–R10 — all detector = reader, at
open (top-level R1) or layer access (sub-record R1) or extent use
(R2–R10).** These are all violations (the file is nonconforming) even
though the reader-visible consequence is bounded to ignoring one record;
§21.6 is the separate, non-normative table of conditions that are *not*
violations at all.

Two rows are explicitly called out (§21.1) as *specializations* of others —
recorded against the narrower row only: F1's front-block instance is an
instance of F6; F1's trailer-magic instance is an instance of F8; F35 is an
instance of F36; L24 is an instance of L25; F21 is an instance of F22; L10
is an instance of L11. (The document states this list is illustrative, "not
offered as closed" — a genuinely open point I address as a finding below,
§21.1's completeness claim notwithstanding.)

Cross-cutting count check: 35 (F, minus the struck F11 slot, i.e. labels
F1–F36 with F11 absent) + 49 (L1–L49) + 26 (T1–T26) + 10 (R1–R10) = 120,
matching §21.1's own stated total ("120 conditions over 277 instances") and
§21.8's restatement (`[R-ERR-02]`). This cross-check gave me confidence I
had not mis-copied a row while reading.

---

## Part 4 — The probes

### V1 — Verdict vocabulary

Answered in full in Part 1.1 above. Three verdicts — conforming,
nonconforming, cannot establish — plus the report-only, non-verdict marker
*unexamined*. One triggering condition each:
- conforming: the verifier walks the whole live state, verifies every
  checksum and decodes every tile, and finds nothing wrong anywhere
  (§2.4, `[R-CNF-12]`: "a verifier certifies only violation-free files").
- nonconforming: the verifier finds even one established violation, e.g. a
  trailer-CRC mismatch (F14) — "an established violation takes priority...
  however many requirements it was unable to check" (§2.3, `[R-CNF-11]`).
- cannot establish: the verifier finds zero violations but cannot execute
  one layer's declared codec (`[R-COD-11]`) — "not a finding that the file
  is nonconforming... available only to a traversal that established no
  violation" (§2.3, `[R-CNF-11]`).

### V2 — Top-level record, unimplemented type, MU=1

The document's answer branches on the type's numeric range (§10.2's record-
type space: assigned 0x0001–0x0002, reserved 0x0003–0x7FFF, experimental
≥0x8000), and the probe does not say which range applies, so I answer both
readings and flag this as underdetermined **by the probe, not by the
document** — the document itself decides fully once the range is known.

- **If the type is in the reserved range (0x0003–0x7FFF):** emitting it at
  all is itself the violation, whatever its MU bit — register row **F36**
  (`[R-CNT-15]`: "a reserved-range record type carrying MU = 1 is itself a
  violation", §2.3). Additionally, MU=1 specifically on a reserved-range
  type is its own, narrower row **F35** ("A top-level record has a
  reserved-range type value... with MUST_UNDERSTAND... set to 1"), which
  §21.1 calls out as an instance of F36 ("F35 of F36... stand in that
  relation"). F35's detector is *reader*, at *open* — so an ordinary
  reader already rejects the file, and a verifier reports **nonconforming**
  (an established violation), citing F35 (and F36).
- **If the type is in the experimental range (≥0x8000):** this is *not* a
  file-conformance violation at all — §21.6's closing paragraph names
  exactly this as one of "two structural cases [that are] conforming files
  a reader nevertheless refuses": "`[R-CNT-15]` obliges the reader to
  reject, and `[R-CNF-02]` makes the file conforming all the same." A
  verifier, being a reader first, must also reject on this ground — but
  since the underlying byte pattern is not itself irregular, the fixing
  requirement is `[R-CNF-11]`, which lists exactly this scenario among its
  named cannot-establish grounds ("when a record carries MUST_UNDERSTAND
  = 1 with a type it does not implement (§21.6)"). If the verifier finds
  no other violation anywhere in the file, its verdict is **cannot
  establish**, and it must report this specific ground and requirement.

I flag as a document-level finding (verifiera-01, below) that this second
branch produces a genuine tension worth a verifier-implementer's attention:
§21.6 independently states "the file in the second carries no violation at
all," while `[R-CNF-11]` unconditionally requires *cannot establish* (never
*conforming*) whenever this pattern is present. Both are true, but only
because "conforming file" (a byte-predicate) and "verifier certifies
conforming" (an epistemic verdict) are not the same claim — see the
finding.

### V3 — Three-generation byte arithmetic

**Assumptions stated up front** (the scenario underdetermines these, and the
probe explicitly asks me to state them):
1. Neither layer declares per-tile alignment (A) nor a slab (S), so within
   one commit a writer places the stored-tile payload(s) and the tile-index
   region contiguously with no gap between them or before the directory,
   per `[R-SLB-05]`'s placement freedom ("MAY occupy any non-overlapping
   byte positions, in any order"). Only the pre-trailer pad (`[R-LIF-02]`
   step 5, "append the pad to the next 64-byte boundary") produces slack
   within a commit.
2. Each commit follows the ordinary appender procedure of §20.3
   (`[R-WRT-04]`) exactly, producing the *minimal* pad each time (§6.2:
   "a longer gap is conforming, and no conforming commit produces one").
3. Generation 3's supersede of one 1,024-byte tile of layer A forces a
   **whole re-emission of layer A's tile-index region** (84 bytes) at a new
   placement, because the stored-tile set's *content* changes (the
   superseded entry's offset and crc change even though its length does
   not) — `[R-WRT-04]`: "Every layer whose stored-tile set or index content
   this commit changes has its tile-index region re-emitted in full." I
   assume the new payload and the re-emitted index are the only bytes
   generation 3 appends before its directory (layer B is untouched).
4. Each generation's directory is exactly 200 bytes, as given, regardless
   of which/how many layer records it must re-emit byte-identically
   (`[R-WRT-05]`) — taken at face value from the problem statement.

**Derivation** (see `v3_arithmetic.py` in my scratch directory for the
executable check; the two computations below — F − live_total, and direct
enumeration of slack sources — agree exactly):

| Generation | Appended before directory | Directory | Pre-dir end | Pad (to next ×64) | Trailer | New F |
|---|---|---|---|---|---|---|
| 1 | front(16)+A tiles(4,096)+A index(84) = 4,196 | 200 | 4,396 | 20 | 64 | **4,480** |
| 2 | F1(4,480)+B tiles(8,192)+B index(164) = 12,836 | 200 | 13,036 | 20 | 64 | **13,120** |
| 3 | F2(13,120)+new tile(1,024)+A index re-emit(84) = 14,228 | 200 | 14,428 | 36 | 64 | **14,528** |

Live state at generation 3 = front(16) + A's live tiles(4,096, unchanged
total: 3,072 original + 1,024 new, 1-for-1 supersede) + A's live index(84,
only the generation-3 copy) + B's tiles(8,192, untouched) + B's index(164,
untouched) + directory(200) + trailer(64) = **12,816 bytes**.

**Live-state byte total: 12,816 bytes.**
**Slack total: F3 − live_total = 14,528 − 12,816 = 1,712 bytes.**

Cross-check by direct enumeration of every slack source: generation 1's
superseded A-index copy (84) + the superseded 1,024-byte tile payload
(1,024) + generation 1's directory (200) + generation 1's pad (20) +
generation 1's trailer (64) + generation 2's directory (200) + generation
2's pad (20) + generation 2's trailer (64) + generation 3's pad (36) =
**1,712 bytes**, exactly matching. (Generation 2's tiles/index and
generation 3's new tile are never superseded, so they are not slack
sources; front and the live trailer are claimed, not slack.)

### V4 — Codec the verifier cannot execute

The governing rule is §17.4, `[R-COD-11]`: "A verifier that cannot execute
a layer's codec or filter cannot establish that layer's conformance and
MUST NOT certify the file. That inability is not a finding that the file is
nonconforming, and it fixes the file's verdict as *cannot establish* only
where the verifier established no violation elsewhere."

**Verdict on the file:** *cannot establish* — provided the verifier
establishes no other violation anywhere in the file. (If it does find some
other, unrelated violation, the priority rule of `[R-CNF-11]` makes the
verdict *nonconforming* regardless, and the codec inability is then just
one more unchecked requirement to report alongside that.) The verifier
"MUST NOT certify the file" in either case where the codec was not
executed.

**What the report says about that layer:** the requirement it could not
check — the decoded-content obligations of §14 that require decoding
(cited by number: `[R-SER-05]` padding-fill content, `[R-SER-08]` boolean
byte resolution, and implicitly the exact-decoded-size check `[R-SER-07]`
and every codec-framing row T14–T25 that a verifier "that certifies decodes
every stored tile" would otherwise have checked) — and the ground (it could
not execute the layer's declared codec). `[R-CNF-11]` requires the verifier
to "report each requirement it was unable to check on a capability or
resource ground, naming the requirement and the ground."

**A document-determined branch worth flagging (not an ambiguity, but easy
to miss when implementing):** `[R-COD-11]`'s own third sentence narrows
when this can happen to a genuinely *conforming* verifier at all: "For a
conforming reader that position arises only at a reserved or experimental
value, every assigned codec and filter being core: it rejects the layer
(`[R-COD-03]`, `[R-COD-09]`); software unable to execute an assigned codec
or filter is not a conforming reader (`[R-CNF-03]`)." So:
- If the layer's codec value is **outside 1–4** (reserved or experimental):
  this is independently register row **L43** (reserved/experimental codec
  value), detector *reader*, at *layer access* — a conforming reader
  rejects the layer purely from the declared value, without needing to
  attempt execution at all, and the file is already **nonconforming** on
  that ground alone (priority rule), independent of anything about
  execution capability.
- If the codec value is **assigned (1–4, "core")** and the verifier still
  cannot execute it: the verifier itself is not, by `[R-CNF-03]`'s own
  terms, a conforming verifier — yet `[R-COD-11]`'s first two sentences are
  written generally ("a verifier," not "a conforming verifier") and still
  tell that non-conforming verifier what to report: cannot establish, do
  not certify. I read this as the document knowingly describing best-effort
  behavior for real, imperfect verifier software (which will not always
  implement every core codec) rather than a gap — but it means "the
  verdict is cannot establish" is really only the fully-correct answer when
  the codec value is 1–4; when it's outside that range, the true, fully-
  determined answer is nonconforming via L43, and a verifier that reports
  cannot establish there instead (because it also happens not to be able to
  execute the reserved/experimental value) would be under-reporting a
  violation it should have caught from the declared value alone, with no
  execution needed.

I mark this probe **underdetermined by the probe's own wording** (which
codec-value range applies is not stated) and give both readings; the
document decides fully once the value is known.

### V5 — Last commit changed a fixed declaration of a layer that stored a tile

**Can the verifier see it: no, not as such.** Two independent reasons, both
textual:

1. **The coverage walk never reconstructs history.** §9.7's closing note:
   "Nothing here enumerates prior commits. A verifier certifies what a
   reader can reach and counts what it cannot, which is decidable from the
   live trailer in one pass and does not depend on reconstructing the
   file's history." The verifier only ever examines the *live* generation's
   directory and structures; it has no access to, and no obligation to
   recover, generation n−1's layer record to compare fixed fields against
   generation n's. Even the Rationale to §20.4 confirms this from the
   writer side: "the live state names one generation, and two trailers of
   one file_id are ordered by committed_file_length without being counted,
   so nothing in either says how many commits separate them... A tool that
   wants the pairing enumerates commit states from the physical file
   (§9.6), and gets only the ones that file still carries" — and §9.6's
   backward probe is explicitly "not a reader behavior," and not part of
   §9.7's coverage verification either ("coverage verification does not
   [continue the probe to offset 0]," `[R-LIF-08]`).

2. **The prohibition itself is a writer-conduct rule, not a file-
   conformance predicate.** §20.3 step 4's own text: "This bar binds the
   commit as an actor: no file is nonconforming by virtue of its violation,
   and no register row records the violation itself, the register
   enumerating file-conformance violations (§21.1) and the bar stating no
   condition a file can exhibit (§21.7, `[R-ERR-01]`, `[R-CNF-02]`)." This
   places it in the same class as `[R-CNF-02]`'s other conduct rules (a set
   ignore-lane bit on a creator, the commit-durability barriers) — binding
   the actor, never the bytes.

**What verdict follows: it depends on whether the change left an incidental
byte-level trace**, and the document is explicit and (I believe) exhaustive
about which changes do:

> "Under new ones the same bytes would denote values, coordinates or
> padding the writer did not store, with every checksum in §8 certifying
> the result and, but for a stored tile's decoded size, a padding position
> or pad bit, or a boolean byte the register witnesses (T3, T14, T21, T22,
> T4, T5, T2) and a decode that fails outright, or a codec's framing check
> that precedes it, under a changed codec or filter (T17, T24, T25), no
> check any actor owes able to see it (§21.7)."

So:
- A change to **tile extent, channel type/count, or layout** that alters
  the tile's decoded size, where the old stored bytes no longer match the
  new declared decoded size: **T3** (or the codec-1-specific **T14**), or
  the zstd frame's now-mismatched declared size/window (**T21**, **T22**)
  — reject-tile, verdict **nonconforming**, but discovered purely as an
  ordinary size/framing mismatch, never as "a fixed declaration changed."
- A change to **fill** that leaves old padding-position bytes no longer
  matching the new fill: **T4** (or **T5** for a packed bool plane's pad
  bits), or **T2** if the change somehow produces a byte other than
  0x00/0x01 at a real interleaved-bool position — reject-tile, verdict
  **nonconforming**, again incidentally.
- A change to **codec or filter** that makes the old stored bytes fail to
  parse under the new declaration's framing rules: **T17** (zstd magic),
  **T24** (trailing bytes), **T25** (malformed stream) — reject-tile,
  verdict **nonconforming**.
- A change to anything else the fixed-declaration list covers but that
  produces none of the above symptoms — for example, **renaming a
  dimension or channel** (names "enter no map this specification defines"),
  reordering names, or a change whose old and new decoded images happen to
  coincide bit-for-bit (the document's own example: a filter change where
  the permutation is the identity at n=1, or a layout change on a
  single-channel numeric layer, per §14.4's Note) — is **entirely
  invisible**: no register row fires, the verifier finds nothing wrong, and
  (assuming nothing else in the file is broken) the verdict is
  **conforming**, despite the writer having violated §20.3 step 4 as an
  actor.

I treat this probe as **underdetermined by its own wording** (it does not
say *which* fixed declaration changed) and give the full, document-
determined case split above rather than a single answer, since the
document's answer is genuinely conditional on that fact and states so
explicitly (the "but for..." clause is, on its face, meant as an exhaustive
list of the witnessed exceptions).

### V6 — MU = 1, PE = 0 on a record

`[R-CNT-12]`: "Writers MUST NOT emit the combination MU = 1 with PE = 0; a
reader or updater encountering it MUST treat the record as PE = 1 (never
silently deletable)... a verifier MUST treat a nonzero reserved flag bit or
the MU = 1 with PE = 0 combination as a validity error at the record's
governing scope." This is one of the two writer defects §7.2 explicitly
assigns to the verifier alone: "Both writer violations make the file
nonconforming (`[R-CNF-05]`) while leaving conforming behavior unchanged, so
their detection is a verifier's."

**What the verifier does with the combination:** treats it as a validity
error at the record's own **governing scope** (§2.4's mapping: file →
reject-file, layer → reject-layer), which makes the file nonconforming.
Ordinary readers and updaters are unaffected in their own behavior — per
`[R-CNT-12]`, they resolve the flag combination to PE=1 and carry on; the
verifier's finding does not change what a plain reader returns, only
whether the file certifies.

**At which scope**, concretely — this is where the register splits by
which kind of record carries the combination:
- **Non-layer top-level record** (e.g., the file-scope user-metadata
  record): register row **F25** — Detector *verifier*, Detected
  *certification*, outcome reject-**file** (`[R-CNT-12]`).
- **Layer record, or a layer's sub-record**: register row **L46** —
  Detector *verifier*, Detected *certification*, outcome reject-**layer**
  (`[R-CNT-12]`, `[R-CNT-13]`).

Both rows are explicitly grouped in §21.1's own discussion of rows "for
which the governing rule states what a reader does" while the outcome is
recorded at certification: "`[R-CNT-12]`'s reading of MU = 1 with PE = 0 as
PE = 1 (F25, L46) resolves a flag and returns no data" — i.e. the reader-
visible effect (treat as PE=1) is uniform, and F25 vs. L46 is purely a
function of which scope the record belongs to.

---

## Findings

### verifiera-01 — OBSERVATION: "conforming file" and "verifier certifies conforming" are provably non-coextensive for at least one structural pattern

**Location A:** §2.3 (`[R-CNF-11]`), the sentence "as when the file names a
format major version it does not implement, when a record carries
MUST_UNDERSTAND = 1 with a type it does not implement (§21.6)..." — this is
one of the named triggers for the *cannot establish* verdict, listed
unconditionally (not qualified by the type's numeric range).

**Location B (same edition, no B text — this is a single-document
finding):** §21.6's closing paragraph, discussing the identical structural
pattern (an experimental-range top-level record type carrying MU=1):
"`[R-CNT-15]` obliges the reader to reject, and `[R-CNF-02]` makes the file
conforming all the same... the file in the second carries no violation at
all."

**Detail.** Take a byte sequence that is a conforming TARN file by every
file-level requirement (§2.3's byte-predicate sense, `[R-CNF-02]`), except
that it carries one top-level record whose type is in the experimental
range (≥0x8000) with MUST_UNDERSTAND=1. §21.6 states flatly that this
exact file "carries no violation at all" — i.e., under the specification's
own predicate, it *is* a conforming file. Yet `[R-CNF-11]` requires every
verifier that does not itself implement that specific (necessarily private,
per §10.3: "two unrelated experiments MAY select the same value") type to
report this file as *cannot establish*, never *conforming* — and
`[R-CNF-11]` is explicit that "a verifier MUST NOT certify a file it
reports [cannot establish]." Because experimental values by definition
carry "no collision protection" and are "private use," no general-purpose
verifier can ever implement all of them; so for at least this one class of
genuinely-conforming, byte-predicate-conforming files, **no verifier
implementation can ever emit the verdict *conforming*** — the best any
verifier can do is *cannot establish* (or worse, *nonconforming*, if
something else is also wrong). "Conforming file" (the predicate on bytes)
and "the verdict a verifier may report as *conforming*" are therefore
provably different classes: the former is not a subset of what can ever be
certified as the latter.

I do not believe this is a drafting error — the two passages are individually
consistent with the rest of the document's careful "capability, not defect"
framing (§21.6's own next paragraph: "In both the outcome records a
reader's capability, not a defect in the bytes"). But it is a real
consequence a verifier *implementer* should know going in: encountering
this pattern must never be treated as license to report *conforming* just
because §21.6 says the file "carries no violation," and a test suite that
expects "some conforming file, verifier says conforming" to be exhaustive
over all conforming files will need to special-case this one structural
family.

**Byte-level test:** yes. It determines that a verifier must never emit the
byte-level verdict "conforming" for an entire class of otherwise
byte-identical-to-conforming files (anything carrying a top-level
experimental-range MU=1 record), regardless of how thoroughly it checks
everything else — a concrete constraint on what output a conforming
verifier implementation may ever produce for such an input.

### verifiera-02 — OBSERVATION: the §21.1 "narrower row" list is declared open, which leaves the corpus's completeness claim to a property rather than an enumeration

**Location:** §21.1: "Some rows are strict specializations of others: where
every file exhibiting one row's condition... necessarily exhibits another's,
the file is recorded against the narrower row... F1's front-block instance
of F6 and its trailer-magic instance of F8, F35 of F36, L24 of L25, F21 of
F22 and L10 of L11 stand in that relation; the property decides any pair
and this list is not offered as closed."

**Detail.** This is not a contradiction or a gap in the register itself
(§21.1 gives the general test — "the property decides any pair" — so the
document is not silent on how to resolve an unlisted pair). But it does
mean that whether some *other* pair of rows I have not been asked about
also stands in a subsumption relation is left to applying the stated
property fresh each time, not to a closed list I could check a candidate
pair against. For a verifier or a conformance-vector author, this matters
operationally: attributing a file to the wrong one of two rows in such a
relation (recording a narrower-row file against the broader row, or vice
versa) is exactly the kind of mistake this document's own vector-
completeness machinery (`[R-VEC-02]`, `[R-VEC-03]`) is designed to catch,
but only if the implementer re-derives subsumption pairs the document
chose not to enumerate exhaustively.

**Byte-level test:** marginal. It does not change which bytes are accepted
or rejected — the outcome (reject-file/layer/tile) for a file exhibiting
one of these conditions is the same whichever of the two rows in a pair it
is attributed to, since both rows always carry the same scope and outcome
by construction (that is what "necessarily exhibits another's" requires).
What it can change is only which row identifier a verifier's *report*
cites for a given violation — relevant to test-vector bookkeeping
(`[R-VEC-02]`'s "recording both ties the vector to the rule as well as to
the row") but not to any byte a conforming implementation may emit, accept,
or reject. I include it as a lower-confidence OBSERVATION rather than a
stronger AMBIGUITY finding for that reason.

---

## Evidence notes (for the structured result's `evidence` object)

- I did not use `rg`/`grep` as my primary method (the file is small enough,
  and the brief's own caution about hard-wrapped blockquotes made we wary of
  relying on line-oriented search for anything I hadn't already read in
  full context); I used two confirmatory greps only, both returning
  multiple non-zero hits consistent with my sequential reading (`cannot
  establish`: 5 hits; `does not implement`: 21 hits).
- Every quantity in V3 was independently derived twice (by hand while
  reading, and by an executable Python script) and the two agree exactly;
  I also cross-checked the general coverage-walk machinery against the
  independent, simpler Appendix A minimal-file example (44 bytes of slack
  out of 128) before trusting the three-generation trace.
- I considered and rejected treating "F35 is an instance of F36" and
  similar as an ambiguity — the document supplies a general test ("the
  property decides any pair") and is explicit the enumerated list is
  illustrative, not exhaustive, so this is a documented open point rather
  than a silence.
- I looked for, and did not find, any place where the register's
  completeness claim (§21.1: "a *detectable* file-conformance violation
  this specification names and the register omits is a defect in this
  document") is itself falsified by something I read — the cross-check of
  35+49+26+10=120 against the document's own stated total (120 conditions,
  277 instances) came out exact, which is some evidence (not proof) that I
  did not mis-transcribe a row while reading sequentially.
