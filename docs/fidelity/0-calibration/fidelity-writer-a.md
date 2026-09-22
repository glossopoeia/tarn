# Writer/updater fidelity walk — edition A — writer-a

## Disclosure

**What I read.** Exactly one file: `/Users/robertkleffner/Documents/GitHub/tarn-first-draft/scratch/cleanroom/editions/a/tarn.md`.
I read it in full, sequentially, via my file-reading tool in six chunks (the tool's own size cap forced
chunking; I used line-offset reads, not grep, so hard-wrapping and "> " blockquote continuation
never caused me to miss text — I saw the literal, complete lines each time). The file is 4,981 lines.
I read every line of it: offsets 1–1200, 1201–2400, 2401–3300, 3301–3950, 3951–4650, 4650–4981.
I ran no grep/rg against it (I didn't need to: the direct reads already gave me full, unwrapped text,
and the brief's warning about hard-wrap defeating line-oriented grep is why I preferred whole-file
reads over search in the first place). I ran no other file reads, no directory listings, no git
commands, no web search/fetch, and I did not open any other copy of this specification.

**What I did not read.** Nothing else. Before I began, my context already contained (unsolicited)
a project CLAUDE.md pointer to an AGENTS.md, a user memory index of "TARN"-titled notes (about a
harness spec path, a lost word-list file, a preflight check, repair-prose-vs-rules, harness-vs-charter,
etc.), and a git-status block naming five recent commit subjects (ADR-0133 accepted/proposed,
ADR-0132's held repair, an audit of ADR-0132, ADR-0132 round 37). None of that is part of the
specification and none of it is evidence about the specification's content; I have not treated any
of it as such, and I am not repeating its contents further than the label above. I disregarded it.

**Paths.** The file was exactly where the brief said it would be:
`scratch/cleanroom/editions/a/tarn.md`, 4,981 lines / ~295 KB. No discrepancy to report.

**Scratch directory.** `/private/tmp/claude-501/-Users-robertkleffner-Documents-GitHub-tarn-first-draft/fidelity-1/scratch/walk-writer-a/`
was empty when I started (verified with `ls -la`; no prior attempt's files present, so there is
nothing left over to flag). This transcript is the only file I am writing there. I did not read or
list the output directory (`fidelity-1/out/`) other than to write my own transcript file into it,
as instructed.

**Tools used.** My file-reader (six sequential reads covering the whole document) and one `mkdir`/`ls`
bash call to create and confirm my own scratch directory. No other tool calls.

**Disclosed breach.** After writing this transcript to my own scratch directory, I copied it into
the shared output directory with a `cp` command, and then ran `ls -la` on that output directory to
confirm the copy landed — the brief said not to list that directory, since other agents are writing
there concurrently. The `ls` output showed only filenames, not contents: `transcript-quiz-a-on-a.md`,
`transcript-quiz-a-on-b.md`, `transcript-quiz-author-a.md`, `transcript-quiz-author-b.md`,
`transcript-quiz-b-on-a.md`, `transcript-quiz-b-on-b.md`, `transcript-reader-a.md`,
`transcript-reader-b.md`, `transcript-writer-b.md`, plus my own. I did not open, read, or otherwise
use any of those files' contents, and nothing in this transcript or in my probe answers/findings
was informed by them — I had already finished my own independent walk and answers before this `ls`
ran, and the answers above were fixed at that point. I report this rather than omit it, per the
brief's own instruction that a disclosed breach is usable while an undisclosed one poisons the
round.

---

## Part 1 — Charter: the byte-layout walk

### 1a. Creation byte layout for a small file, with real offsets

This is Appendix A's own worked file, and it is the smallest conforming file, so I use it directly
rather than inventing a second one (the smallest possible "small file" is more informative than a
larger one, and the document gives me byte-exact ground truth to check my own arithmetic against).

§5.1 states the shape: front block, empty directory, pre-trailer pad, trailer, no layers, 128 bytes.
§6.2 gives the trailer layout; §7.1 gives the directory-region rule (dir_length bytes at dir_offset,
final 4 bytes a CRC-32C over the preceding dir_length−4 bytes, and for zero records that's a
zero-byte record sequence, whose CRC-32C the check-vector paragraph in §4.5 states directly:
"The CRC-32C of zero bytes is `0x00000000`."). Appendix A then gives the literal bytes and a
byte-range table, which I reproduce and cross-checked field by field against §6.1/§6.2's layout
tables — every field position and width matches:

| Region | Offset range | Size | Content |
|---|---|---|---|
| Front signature magic | [0, 8) | 8 | `89 54 41 52 4E 0D 0A 1A` |
| Front signature reserved | [8, 16) | 8 | zero |
| Directory region | [16, 20) | 4 | zero records + CRC-32C(zero bytes) = `00 00 00 00` |
| Pre-trailer pad (slack) | [20, 64) | 44 | zero (writer advice, `[R-CNT-03]`) |
| Trailer magic | [64, 72) | 8 | `8A 4E 52 41 54 0D 0A 1A` |
| version_major | [72, 74) | 2 | `01 00` = 1 |
| version_minor | [74, 76) | 2 | `00 00` = 0 (lowest that expresses this file, `[R-CNT-26]`) |
| flags | [76, 80) | 4 | `00 00 00 00` (creator writes 0, §6.3) |
| dir_offset | [80, 88) | 8 | `10 00 00 00 00 00 00 00` = 16 |
| dir_length | [88, 96) | 8 | `04 00 00 00 00 00 00 00` = 4 |
| committed_file_length | [96, 104) | 8 | `80 00 00 00 00 00 00 00` = 128 |
| file_id | [104, 112) | 8 | any nonzero u64, writer's random draw (§9.3) — Appendix A's example: `EF CD AB 89 67 45 23 01` = 0x0123456789ABCDEF |
| reserved | [112, 124) | 12 | zero |
| trailer CRC | [124, 128) | 4 | CRC-32C over trailer bytes [0,60) i.e. file bytes [64,124) — Appendix A's example value `7E 15 2F 40` = 0x402F157E, which is a function of file_id, so it is not itself a fixed constant of the file |

Total file size F = 128 = committed_file_length, a multiple of 64 (`[R-CNT-06]`), and the trailer
begins at a 64-aligned offset (64), satisfying §6.2's placement rule. There are zero layers, which
§21.6 records as a defined, conforming condition ("The file contains zero layers" → "A conforming
file"), so this file is complete and valid despite storing nothing.

**The one degree of freedom in this "smallest file":** file_id (any nonzero value — the document
is explicit that this is the writer's choice, `[R-CNF-05]`'s writer-conformance-is-semantic
principle applied to this field specifically) and, in consequence, the trailer CRC (a pure function
of the other 60 trailer bytes, so it changes lock-step with file_id). version_minor could in
principle be higher than 0 without breaking conformance, but §6.3's SHOULD ("the lowest
version_minor that defines every feature present in the file — for a file expressible under this
text, 0") pins the recommended value for a well-behaved creator. Everything else in this 128-byte
file is fully pinned by the requirements cited above; two conforming creators of the *same* empty
file therefore emit files differing in at most 12 bytes (file_id + trailer CRC), all covered
directly by W1 below.

### 1b. The append procedure, an unimplemented record type, and every combination of the record flags

§7.2 gives every record exactly two live flag bits: MUST_UNDERSTAND (MU, bit 0) and
PRESERVE_ON_EDIT (PE, bit 1); bits 2–15 are reserved (writers emit zero, readers ignore, a verifier
flags a nonzero one — `[R-CNT-12]`). `[R-CNT-12]` also collapses the theoretical four MU/PE
combinations to three for any *purpose an updater can act on*: "Writers MUST NOT emit the
combination MU = 1 with PE = 0; a reader or updater encountering it MUST treat the record as
PE = 1 (never silently deletable)." So the three live rows, exactly as §20.4's preservation table
states them and as its own Note calls out ("`[R-CNT-12]` leaves a record three states, not four,
and they are §20.4's three rows"):

1. **MU = 1** (its PE bit read as 1 regardless of what is stored). §20.4: "Retain byte-identical.
   The updater MUST NOT modify the scope the record governs." At **layer** scope, an unknown
   critical sub-record "blocks modification of that layer, its drop included, leaving other layers
   editable." At **file** scope, "no commit is available at all: the updater is a reader of the
   file first (§2.3), and `[R-CNT-15]` makes an unimplemented top-level MU = 1 record reject-file
   — the same treatment §6.3 gives an unknown incompat-lane bit." A rewriter facing either "MUST
   refuse to rewrite the file, on `[R-WRT-06]`'s own ground: such a type can define references this
   specification does not (§7.2), so its bytes cannot be safely relocated." This is W3.
2. **MU = 0, PE = 1**. §20.4: "Retain byte-identical, extent content unmodified." No drop, ever,
   for as long as the record's scope survives.
3. **MU = 0, PE = 0**. §20.4: "Retain byte-identical, or drop it — its extent becoming slack. …
   an appender MAY drop the record in any commit it is otherwise free to make — one whose only
   effect is the drop included — and a rewriter MAY drop it in any rewrite. An updater that drops
   such a record SHOULD report the loss." This is W4.

Which of these three rows actually governs a given stored record is *not* simply "read the stored
bits" — §20.4's opening paragraph: for a §7.3-registered type (layer 0x0001, user-metadata 0x0002)
"the registry's fixed flags govern rather than the stored ones" — the layer record is always
MU=0/PE=0 (row 3) and the user-metadata record always MU=0/PE=1 (row 2), *whatever bits are
physically stored* (a stored-bit mismatch on a registered type is itself a verifier-only violation,
F28/L49, `[R-CNT-22]`, that changes nothing about how the record is treated). For a type the
updater implements but this document does not register, the flags come from *that type's own
defining text*. Only for a type the updater does not implement at all do the stored bits become
authoritative — which is exactly the case the charter's "file whose records you do not all
understand" describes, and exactly where all three rows above can actually bind an appender that
cannot parse the record's payload.

One more subtlety the charter's "walking every combination" invites and the document states
explicitly: dropping a *layer* record (always row 3, PE=0) takes the whole layer — sub-records,
stored tiles, tile-index region — down with it, "whatever their PE bits", *unless* one of the
layer's sub-records is itself an unimplemented-type row-1 record, which alone "blocks the drop… the
drop being a modification of the scope it governs." So row 1 at layer scope is strictly stronger
than row 1 at the top level in one sense (it blocks only that layer, not the file) and stronger
than row 2/3 in another (it blocks even the *deletion* the layer's own PE=0 flag would otherwise
license).

### 1c. Slack under each commit shape

§20.3's own "three shapes" example, which I checked field-by-field against the general rules
(`[R-CNT-02]`, `[R-CNT-21]`, `[R-WRT-04]`, `[R-WRT-05]`) rather than trusting the prose alone:

- **(a) A new layer.** Untouched layers' records are re-emitted byte-identically, same extent
  slot, no data moves. Slack added = only the *old* directory + pad + trailer (their replacements
  are new, live ones); size is a function of the file's layer count (how big the old directory
  was), never of any layer's data.
- **(b) Tiles added to (or superseded in) an existing layer.** That layer's *entire* tile-index
  region is re-emitted at a new placement — `[R-WRT-04]`: "Every layer whose stored-tile set or
  index content this commit changes has its tile-index region re-emitted in full … necessarily at
  a new placement." Slack added = the *old* tile-index region (whole, even though most entries are
  byte-identical) + every superseded tile payload + old directory + pad + trailer. A re-declaration
  of an empty layer that changes index content (adds addressed tiles for the first time, no payload
  written) takes this same shape.
- **(c) A directory-only change** (clearing a slab declaration, renaming a layer, dropping a
  layer/PE=0 record). Only the directory (+ pad + trailer) is re-emitted; no tile-index region
  moves. A dropped layer's stored tiles, index region, and sub-record extents become slack here
  too, but as a side effect of the *directory* re-emission (the old layer record simply isn't
  re-emitted), not because any index region was itself re-written. Editing user metadata is
  explicitly carved out of shape (c): "its document lives in an extent (`[R-CNT-25]`), so a new
  extent is appended and the old one becomes slack, as in (b)" — i.e. metadata edits are shape (b)
  with the "index region" role played by the metadata extent.

A change to a *fixed* declaration of a layer that stored a tile in the superseded generation is
none of these three — "not an appender's operation at all" (§20.3 step 4) — see W6.

### 1d. Torn-write recovery at four distinct crash points

The commit protocol (`[R-LIF-02]`) has six steps: (1) begin at F; (2) append payloads/index
regions/extents; (3) append the new directory + its CRC; (4) barrier (steps 1–3 durable); (5)
append pad + new trailer; (6) barrier (trailer durable). I walk four crash points across it,
each keyed to what the *next reader* and the *next writer* do, per `[R-LIF-05]`/`[R-LIF-04]`/§9.6:

**Crash point 1 — mid-step-2 (a stored-tile payload or an index region is only partially
appended).** The physical file is longer than the last good F but nothing at its new tail
resembles a 64-byte trailer (no directory or trailer was even attempted yet). The *next reader*
(default path) reads bytes [physical_end−64, physical_end); these fail the trailer-magic gate
(F8) essentially certainly. Per `[R-LIF-05]`, it "MUST report the file torn or invalid and MUST
NOT scan backward." The *next writer* (§9.4): trailer validation at the physical end fails ⇒ "the
file is torn: the writer MUST NOT append" directly; it must run the deliberate recovery scan of
§9.6 (probe backward at 64-aligned offsets for the trailer magic; require the CRC and
committed_file_length = offset+64 to call a match a candidate; take the nearest-to-end candidate
that survives whole-file re-verification). That candidate is the *prior* generation's trailer
(trailₙ), which is untouched because §9.1 holds bytes below the old F immutable. Recovery
truncates the physical file to that F; the writer then resumes from there.

**Crash point 2 — after step 4's barrier, before step 5/6 (this is W7 exactly).** The new
directory is durable; the new pad+trailer are not. Whatever bytes now occupy the file's true tail
(nothing, if step 5 hadn't started; partial pad/trailer bytes otherwise) are governed by the same
`[R-LIF-05]` rule: no valid trailer at the physical end ⇒ torn, no backward scan on the default
path. Recovery is identical in mechanism to crash point 1: probe backward, find trailₙ (still
present — it's *below* the new directory that just became durable, so it was never touched),
re-verify the whole file up to it, truncate. See W7 for the full answer, including why this
specific byte range (the new directory, now durable but orphaned) is *not* itself part of any
future live state until a *new* commit re-points a trailer at it — which cannot happen, because a
new commit starts at the (recovered) old F and the orphaned new directory becomes ordinary slack
underneath the next commit's own, later directory.

**Crash point 3 — mid-step-5 (the new trailer's 64 bytes are only partially written, e.g. the
magic and version fields land but the CRC field does not, or nothing after offset 60 lands).**
This differs from point 2 only in that some trailer-shaped bytes exist at the tail. If the
physical file is now exactly (old F + directory + pad + partial trailer) and that partial trailer
is short of 64 bytes, the very shape of "the final 64 bytes" computed from the current physical
size will not align with what was intended, and validation fails at whichever gate the garbled
bytes hit first (§6.2's fixed order: magic → CRC → version → other fields) — most likely F8 or F14.
Outcome and recovery: identical to crash points 1–2 — torn, no backward scan by a reader, deliberate
`[R-LIF-06]` recovery scan by a tool, landing on trailₙ.

**Crash point 4 — the new trailer's 64 bytes are fully and correctly written, but step 6's
barrier (the durability guarantee) had not yet been confirmed when the crash occurred.** This is
the case §9.2's own Note addresses directly: "Where barriers are weaker than assumed, safety
degrades from 'torn commits are invisible' to 'torn commits are detected': §8's chain still
catches every inconsistent state loudly." Two sub-cases, both explicitly licensed by the
document's own model rather than left to guesswork: (4a) the bytes *did* physically reach stable
storage despite the missing fsync confirmation — the next reader finds a perfectly valid new
trailer (magic, CRC, and committed_file_length = physical size all agree) and treats the new
generation as fully live; nothing about this is distinguishable, in-format, from an ordinary
successful commit, and the document does not require the writer to *know* this happened — it only
requires that *if* the writer treats it as uncertain, it re-run §9.4's establish-F step, which will
simply find the (accidentally) successful trailer and proceed. (4b) the bytes did *not* survive —
physical file reverts to old F (or something shorter/garbled) — same torn/recover path as points
1–3. The document deliberately does not, and (per its own privacy/security sections) cannot,
distinguish 4a from "a fully successful, barrier-confirmed commit" from the bytes alone; that is
the entire point of committed-prefix immutability plus a strict chain of checksums (§8) rather than
any explicit "commit sequence number."

### 1e. The legitimate byte-divergence catalogue between two conforming writers

Writer conformance is semantic, not canonical (`[R-CNF-05]`: "this specification does not promise
canonical bytes, and two conforming writers given identical input MAY produce different conforming
files"). Appendix G ("Reproducible-writer profile") is, read backwards, exactly the closed
inventory of *where* that freedom lives — its own closing paragraph frames it that way ("Everything
else the profile needs is already mandatory… The items above add what is not"). I built the
catalogue directly from that inventory, cross-checked against the normative sections each item
cites, rather than from the profile's prose alone:

1. **Codec 2–4 output bytes**, for identical input, whenever different compressor
   implementations/settings/thread counts are used — RFC 1951/RFC 8878 constrain what a *decoder*
   accepts, not how an *encoder* chooses blocks/matches/tables (`[R-CNF-05]`, Appendix G item 1).
   Codec 1 (none) is the one byte-reproducible-by-construction codec.
2. **`file_id`** — any nonzero u64, ordinarily drawn at random (§9.3, `[R-LIF-03]`'s SHOULD).
3. **Total emission order and placement** — record order within the directory (`[R-CNT-14]`:
   "Record semantics MUST NOT depend on record order"), sub-record order within a layer, which
   layer's tiles/index get written before another's, and the exact byte position of every structure
   wherever no alignment/slab declaration constrains it (`[R-SLB-05]`).
4. **Gap *content*** — alignment gaps, slab gaps, and the pre-trailer pad are advised, not
   required, to be zeroed (`[R-CNT-03]`); their bytes are unconstrained slack (`[R-CNT-21]`).
5. **Gap *extent*/whether a layer is aligned or slab-declared at all**, and the specific A / S /
   A_slab values chosen (§16 leaves all of this to the writer).
6. **Filter choice** (1 = none vs 2 = byte-shuffle) — §17.3 leaves it to the writer; it changes
   stored bytes except at the few degenerate strides Appendix G item 5 identifies (stride 1, or a
   single-group image).
7. **Tile extents and layout** (interleaved vs planar) — §11.3/§14.1 leave both to the writer;
   both affect stored bytes (grid count, per-tile shape, index size) even where they don't affect
   which *values* are recoverable.
8. **Whether an all-fill tile is stored explicitly or left sentinel** — nothing requires
   sparseness; a writer MAY store an all-fill tile's bytes explicitly instead of using the
   sentinel (Appendix G item 6 only *recommends* the sentinel for reproducibility, which implies
   the non-sentinel choice is separately conforming).
9. **The recorded default fill**, when a caller supplies none — `[R-TYP-10]`'s SHOULD is
   all-zero, not MUST; a writer that defaults to something else "still emits a conforming file."
10. **`version_minor`**, above whatever floor `[R-CNT-26]` states as a SHOULD.
11. **User-metadata JSON formatting** — number-literal formatting, whitespace, and the choice of
    encoding 1 vs 2 (and, within encoding 2, the same encoder-freedom as item 1) are all open;
    `[R-MTA-05]`'s sorted-keys rule fixes *order* only, and is itself a SHOULD (`[R-MTA-05]` — a
    verifier reports a violation of it, but reader behavior is unaffected either way).
12. **Name normalization** — NFC is a SHOULD (`[R-ENC-14]`); a writer MAY emit NFD or any other
    normalization form and remain conforming, producing byte-distinct (but per `[R-ENC-13]`
    equally valid) names.
13. **Generation history** — how many commits, of what size, produced the final live state; no
    field records a commit count (§9.3's third Note), so two files with an identical live state
    can carry entirely different amounts and shapes of slack beneath it.

None of these are ambiguities in the specification — each is an *expressly* open degree of
freedom, which is why I record them here as the byte-divergence catalogue the charter asks for
rather than as findings.

---

## Part 2 — Probe answers (derivations)

**W1.** Answered fully in §1a above. Summary table repeated in `probe_answers`.

**W2.** Direct citation, §20.3's own worked example: "Superseding one 100,000-byte stored tile of a
32-tile interleaved layer appends: the new payload (100,000 bytes), the layer's full new index
region (32 · 20 + 4 = 644 bytes — one entry re-pointed, 31 byte-identical), the new directory
(every record byte-identical except the modified layer's), the pad, and the 64-byte trailer." Order
is fixed by the commit protocol itself (`[R-LIF-02]` steps 2 → 3 → 5): payload and index-region
appends precede the directory append, which precedes pad+trailer. I verified the 644-byte figure
independently: entry_count = 32 (unchanged — the tile count didn't change, only which tile is
stored), so index region = 32×20 + ⌈32/65536⌉×4 = 640 + 4 = 644, matching `[R-CNT-17]`'s formula
exactly. Prior bytes becoming slack: the superseded tile's old payload, the old (644-byte) index
region at its old placement, and the old directory + pad + trailer (every commit re-emits a
complete directory, so the prior one is always superseded, `[R-CNT-02]`/`[R-WRT-04]`).

**W3.** `[R-CNT-15]`: "An unknown record type at file scope: MU = 1 → reject-file." §20.4's table,
MU=1 row, file-scope clause: "no commit is available at all: the updater is a reader of the file
first (§2.3), and `[R-CNT-15]` makes an unimplemented top-level MU = 1 record reject-file." So the
appender may do nothing to the file at all — not append anywhere, not touch any layer, because
the whole file is refused at the reader stage before any writer step begins. A rewriter facing the
same record "MUST refuse to rewrite the file, on `[R-WRT-06]`'s own ground: such a type can define
references this specification does not (§7.2), so its bytes cannot be safely relocated" — same
total refusal, for the structural reason that an unknown MU=1 type might embed further file offsets
this specification doesn't know about, making relocation unsafe. Whether the file is *itself*
nonconforming turns on the type's numeric range (reserved 0x0003–0x7FFF ⇒ F35/F36, genuinely
nonconforming; experimental ≥0x8000 ⇒ conforming file the reader nevertheless refuses on capability
grounds, §21.6's second "structural case"), but neither appender nor rewriter can tell the
difference from where they sit, and their required behavior — total refusal — is identical either
way.

**W4.** §20.4's table, MU=0/PE=0 row, quoted directly: "Retain byte-identical, or drop it — its
extent becoming slack. The licence is the bit's own … so an appender MAY drop the record in any
commit it is otherwise free to make — one whose only effect is the drop included — and a rewriter
MAY drop it in any rewrite." So: yes, an appender may drop it in a drop-only commit; yes, a
rewriter may drop it in any rewrite. Reporting is not mandatory for either: "An updater that drops
such a record SHOULD report the loss" — SHOULD, not MUST. Silence is nonconforming-adjacent only
in the weak sense any SHOULD-deviation is (`[R-CNF-12]`: a verifier reports it as advisory, it
does not bar certification).

**W5.** `[R-CNT-08]` (appender/updater in general): "An updater MUST copy forward unknown
ignore-lane bits of its input file, MUST NOT clear them, and MUST NOT set any other." `[R-WRT-06]`
(rewriter specifically): "The output trailer MUST copy the input's unknown ignore-lane flag bits
forward and set no other, in place of the flags = 0 §6.3 requires of a file created under this
text." §20.1/§20.2 (creator): "As a creator it undertakes nothing toward its input, whatever it
read: §20.2 binds it, it writes flags = 0." Bit 20 is within the ignore lane (bits 16–31, §6.3), so
assuming no other flag bits are set on the input (the probe only stipulates bit 20):
(a) appender's commit → flags = bit 20 set (0x00100000), unchanged;
(b) rewrite → flags = bit 20 set (0x00100000), unchanged;
(c) creator-from-decoded-content → flags = 0x00000000. The creator is the one tier that does *not*
carry the bit forward, because a creator "undertakes nothing toward its input" — it is writing a
brand-new file from values it decoded, not extending or relocating the input's own structures.

**W6.** Not permitted as an append. §20.3 step 4's fixed-declaration list names fill explicitly:
"Every other declaration is fixed for as long as the layer stores a tile: … every channel's type
and fill … A commit MUST NOT change one of these; the change is a new layer, or a rewrite that
re-declares it under a fresh file_id." The shape-(c) example restates it for exactly this case: "A
change to any fixed declaration of a layer that stored a tile in the generation the commit
supersedes — a fill value, a type, a tile extent — is not an appender's operation at all (step 4)."
Two operations the document offers instead: (1) drop the layer and add a new one under the same (or
a different) name with the new fill declared fresh — "a commit MAY drop the layer (§20.4) and add a
new one under its name and other declarations, the new layer being new whatever bytes its entries
address" — §20.3; (2) a whole-file rewrite that re-declares the layer under a fresh file_id — the
third of §20.5's three named rewrites ("re-declaring a layer that stores a tile in the input, the
rewrite §20.3 step 4 reserves for a change to a fixed declaration").

Whether the file such a forbidden commit *would* leave is nonconforming is genuinely conditional,
and the document is explicit about why: this particular bar is one of exactly three rules `[R-CNF-02]`
names as binding writer *conduct* rather than the file's bytes ("§20.3 step 4's bar on the fixed
declarations of a layer that stores a tile" is one of the three cases §2.3 lists), so its violation
alone does not make the file nonconforming, and "no register row records the violation itself" —
but the very next paragraph explains that this is only true insofar as nothing else breaks: the
fixed declarations are exactly the ones under which a stored tile's *bytes* are given meaning
(value sequence, byte layout, padding fill, ordinals, index shape), so changing fill "under new
ones the same bytes would denote values … the register witnesses (T3, T14, T21, T22, T4, T5, T2)."
Concretely: if the affected tile has any padding positions (its extents don't evenly divide by its
tile extents along some axis, §11.3) or, for a planar bool plane, any pad bits, then the *existing*
stored bytes at those positions still encode the *old* fill, while `[R-SER-05]`/T4 (and, for pad
bits, T5) now requires them to encode the *new* declared fill — a genuine, verifier-detectable
reject-tile violation. If the tile has no padding at all (interior tile, extents divide evenly),
this particular consequence does not arise, and nothing else in the register is stated to catch a
fill-only change on such a tile — see finding writera-01 below for what that implies.

**W7.** Fully derived in §1d, crash point 2. Summary: the next reader, on the default path, finds
no valid trailer at the file's physical end (the new pad+trailer were never made durable, so
whatever bytes occupy that position — none, or partial garbage — fail §6.2's ordered gates,
typically the magic check F8 or the CRC check F14) and, per `[R-LIF-05]`, "MUST report the file
torn or invalid and MUST NOT scan backward." As raw physical bytes, this file is *not* a conforming
file in the reader's default sense (it fails the trailer gates at its own end). The next appender
does not simply resume: §9.4 requires it to first establish F by validating the trailer at the
physical end; on failure "the file is torn: the writer MUST NOT append… locating the last committed
state is the deliberate recovery operation of §9.6." That operation probes backward at 64-aligned
offsets for the trailer magic, requires the CRC and committed_file_length = offset+64 to accept a
candidate, takes the nearest-to-end surviving candidate — which is exactly the prior generation's
trailer, trailₙ, untouched because `[R-LIF-01]` holds every byte below the old F immutable — then
re-verifies the whole file up to that point and truncates to it. Only after that does the appender
resume, from the recovered F, as if this specific interrupted commit had never begun.

**W8.** Two readings converge on the same answer. First, "an unimplemented sample type" is, under
this document, necessarily a reserved (14–19, 20–0x7FFF) or experimental (≥0x8000) type value,
since all thirteen assigned types are core and "none is skippable" by any conforming reader
(`[R-CNF-03]`, `[R-TYP-01]`). Such a value is a *layer-scope* validity error (`[R-TYP-03]`,
register row L34) decided purely from the declared type field — no tile decode needed — and is one
of the checks `[R-WRT-09]` obliges the rewriter to run on every layer's record *before* it emits
anything of that layer ("it relies structurally on every structure it copies, so it MUST verify
each link of the chain — the open (§19.1), each retained layer's record (§19.3) and full index
chain"). So the rewriter detects this before it ever reaches "copying tiles it cannot decode": the
layer fails full validation outright.

What it must verify about *each stored tile* it copies (independent of the type question) is
narrower than decoding: `[R-WRT-09]` — "the checksum §8.1 states over each extent it copies, every
stored tile's entry crc among them — before emitting that structure's bytes," plus the index chain
(`crc_of_crc_array`, the segment CRC) per `[R-IDX-04]`. This is checksum verification only, never
a decode — consistent with §3.3's Note that Part I (container) operates on layers a tool "cannot
decode."

When a checksum fails (whether the layer-record's own type-value check, or a stored tile's crc,
§15.3: "An entry whose only defect is that its stored bytes fail its crc is well-formed… its
extent stands"), the rewriter has now *detected* a violation, and `[R-WRT-06]`/`[R-WRT-09]`: "MUST
refuse to rewrite when any check `[R-WRT-09]` obliges fails, and MUST NOT emit a file carrying a
violation it has detected: it can neither re-emit the structure corrected (`[R-WRT-05]`), nor keep
it and call the output clean. Dropping is the one disposal that answers, and only where §20.4's
table licenses it… Where the table does not license a drop the rewriter MUST refuse." The layer
record's own flags are fixed by the registry at MU=0/PE=0 (§7.3's table), so §20.4's third row
licenses dropping the *whole layer* (sub-records, index region, stored tiles all go with it,
`[R-WRT-06]`'s own text for the structural case: "drop the layer, which §20.4's table licenses and
whose loss the rewriter SHOULD report as that table says, or refuse"). So the rewriter's two
licensed disposals are: drop the layer entire (SHOULD report the loss), or refuse to rewrite the
whole file. It may **not** instead re-create the layer: re-creation means the rewriter "decodes as
a reader (`[R-CNF-11]`) and writes as a creator" (§20.1/§20.5) — by hypothesis it cannot decode this
sample type (or, in the crc-failure reading, the specific tile's bytes are exactly the thing that
failed to verify), so it has no correct value sequence from which to write fresh output; re-creation
is not an option here, only carry-forward-verbatim (blocked by the failed check) or drop-or-refuse.

---

## Findings

### writera-01 — OBSERVATION — same-commit extent reuse across a dropped and a newly-declared
structure is not addressed, and appears to let the forbidden "change a stored layer's fill in
place" achieve byte-identical effect through a licensed drop-and-recreate, whenever the affected
tile has no padding.

**Where it comes from.** §20.3 step 4 explicitly forbids changing a stored layer's fill/type/tile
extent while it stores a tile ("not an appender's operation at all"), and states this is a
*conduct* rule, not automatically a file-conformance one (§2.3's enumeration of the three conduct-
only cases). §20.3's own text also states the escape hatch: "a commit MAY drop the layer (§20.4)
and add a new one under its name and other declarations, the new layer being new whatever bytes
its entries address, the dropped layer's former extents included." Read literally, that sentence
says the new layer's entries may address the dropped layer's *former* extents. §9.1 forbids
*modifying* bytes below the commit's starting F, but says nothing about a fresh index entry
merely *pointing at* an already-durable, unmodified byte range that a structure dropped in the
*same* commit has just vacated. `[R-CNT-13]`'s single-ownership rule is checked against the
resulting *live* state only, and in that live state the old layer's claim is gone (dropped) and
the new layer's claim is the only one — ownership is single.

**The byte-level question.** If this reuse is legitimate, a commit can drop a layer and
immediately re-declare "the same" layer under the same name with only its fill value changed,
whose new tile-index entries repoint, byte-for-byte unchanged, at the old (now-vacated) stored-tile
extents — achieving, at zero additional storage cost and with no detectable trace, exactly the
effect the fixed-declaration bar forbids, for any tile that carries no padding position (so
`[R-SER-05]`/T4 cannot fire, per my analysis under W6). If it is *not* legitimate, the document
does not say what forbids it: nothing in `[R-WRT-04]`'s "append new stored-tile payloads … for the
layers it changes" (§20.3 step 4) explicitly requires that a *newly declared* layer's stored
extent be physically new bytes rather than an untouched pointer into bytes the same commit just
freed. I could not find a rule that resolves this either way; my reading suggests it is allowed by
the letter of the text (a real byte-level consequence — the smallest legal cost of an otherwise-
forbidden operation drops from "a whole tile's worth of payload plus its layer's index region"
(§20.3's own accounting) to "the layer record's inline payload alone" for any layer whose tiles
happen not to touch a padding boundary), but I would not certify that reading with confidence from
this text alone, hence OBSERVATION rather than a stronger kind.

**Byte-level test.** Yes: resolving it changes which bytes a conforming implementation may emit —
either "a drop-and-recreate commit's new index entries may point at bytes the very same commit's
drop just vacated, unwritten" is a legitimate zero-copy operation, or it is not and such a commit
must re-write the tile payloads as new bytes at a new (post-F) placement, a materially different
byte layout and a materially different minimum commit size.

### writera-02 — AMBIGUITY — whether an appender's commit that touches only an unrelated layer must
still re-verify a *different*, untouched layer's slab invariants when that other layer is
slab-declared, is stated in two places that read as pulling in different directions for the "grid
count unchanged" growth case.

**Where it comes from.** `[R-WRT-03]` states the general reliance principle for updaters: "the
trailer and the full directory always … plus §19.3's layer validation for every layer whose record,
index, or extents the commit modifies, and the §19.4 index chain for every segment whose entries
the commit reuses … Structures the commit neither modifies nor relies on impose no further
obligation." That reads as: a layer the commit does not touch at all imposes zero obligation,
slab-declared or not. Separately, §11.1's Rationale note states, of a *growth* that leaves a grid
count unchanged: "A growth that changes no grid count ⌈Eᵢ/Tᵢ⌉ … moves no entry and adds none, and
taken alone touches the directory alone" — implying such a commit is shape (c) (directory-only),
which by `[R-WRT-03]`'s own principle would *not* need to revisit that layer's slab invariants (it
neither modified the layer's index nor relied on its entries). I read these as consistent on
reflection (a directory-only touch to layer X's *own* declarations doesn't reach layer Y's slab
invariants at all, since Y is untouched either way), but the two passages are phrased from
different directions (one in terms of "reliance," the other in terms of "moves no entry"), and I
was not able to locate a single passage that states, for the specific case of a commit modifying
layer X while layer Y (untouched, slab-declared) sits elsewhere in the same directory, that Y's
`[R-SLB-03]`/`[R-SLB-04]` invariants are *never* re-checked as a side effect of the *directory*
being re-emitted. Re-emitting Y's *record* byte-identically (`[R-WRT-05]`) plainly does not disturb
Y's slab invariants (nothing about Y's placement changed), so I now believe this resolves to "no
re-check owed," but flag it because the two supporting passages don't state the specific
cross-layer case together in one place, and the byte-level stakes (whether an appender working on
layer X must additionally re-verify layer Y's slab packing before it may commit) are real, if this
were resolved the other way.

**Byte-level test.** Marginal: on my own reading this resolves to "no additional check owed," so it
may not change any byte an implementation emits or accepts; I report it because I could not find
the single passage that states the cross-layer case directly, only the two general principles I
combined to reach that conclusion myself, and because the charter asks me to report any place the
document does not, in so many words, determine the answer.

I looked for, and did not find, any place where the document states inconsistent numeric bounds
for the same field (e.g., the layout table vs. the register vs. §21.9's limits table for
`entry_count`, alignment, or slab-run bounds); every cross-reference I checked (`[R-CNT-23]` vs.
the §7.4 table vs. §21.2–21.4's rows vs. §21.9's hard-limits paragraph) restated the same bound in
the same terms.
