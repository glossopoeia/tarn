# Writer/Updater walk — edition B — transcript

## Disclosure

**Access.** I read exactly one file: `/Users/robertkleffner/Documents/GitHub/tarn-first-draft/scratch/cleanroom/editions/b/tarn.md`.
It exists at exactly the path the brief named (I checked with `ls`/`wc -l` before reading):
4977 lines, 302,125 bytes. I read it in full, in ~5 chunked `Read` calls (offset/limit) because
a single call exceeded the tool's token ceiling. I did not open any other file, any other copy of
this specification, docs/, PLAN.md, OPEN-QUESTIONS.md, AGENTS.md, README.md, CONTRIBUTING.md,
conformance/, spec/registry.json, git history/diff/log, or the web. I did not list any directory
other than the scratch directory I created for myself and a directory-existence check on the one
file's parent (`ls .../editions/b/`) before reading it — done only to confirm the path and size,
not to see what else exists there.

I ran `grep -n` against the one file (line-number lookups only, e.g. to find the "32 · 20 + 4"
Example and the section headers) and local Python (no file I/O) to recompute CRC-32C values and
simple arithmetic that the document itself states. No other files were read by those scripts.

**Scratch directory.** `/private/tmp/claude-501/-Users-robertkleffner-Documents-GitHub-tarn-first-draft/fidelity-1/scratch/walk-writer-b/`
was empty when I started (verified with `ls -la`) — no prior attempt's files were there. This
transcript is the only file I wrote in it.

**Unsolicited context.** Before I began, my runtime had already placed into context: a project
`CLAUDE.md` pointer file, a list of titles from a user memory index (about "TARN" topics, an ADR
process, a harness/gate wordlist, etc.), a git-status block naming several recent commit subjects
about ADR-0133 and ADR-0132 and a `docs/fidelity/` directory, and standard environment/tool
plumbing (skills list, model identity, date, deferred-tool list). None of that is part of the
specification and I have treated none of it as evidence about the specification's content. I am
disclosing that it appeared, and am not repeating its substantive content beyond this paragraph.
It played no role in any answer or finding below.

**Wrapping caveat I followed.** The source is hard-wrapped prose with `>` block-quote continuation.
Where I needed to confirm a phrase's presence, I searched short fragments unlikely to wrap (e.g.
`"32 · 20 + 4"`, `"### 15. Tile Index"`) rather than long line-anchored strings, and where I relied
on a `grep` returning zero hits for anything, I did not — every conclusion below rests on text I
actually read in a `Read` call, not on a grep miss.

**R-CNF-01 labelling.** Per the document's own §2.1, `[R-CNF-01]`: "All text in this document is
normative except: §1 (Introduction); any text labeled *Note*, *Example*, or *Rationale*; and
appendices identified as non-normative." I have checked the bold label on every block-quote I rely
on for a normative claim (e.g. the §5.1 "smallest conforming file" passage is labelled
"**Example.**", so I treat its *arithmetic* as illustrative and controlled by the normative
formula in `[R-CNT-17]` rather than as itself binding — this matters for finding writerb-01 below).
Unlabelled block-quotes (e.g. the "Note. How to read this document" block right after the title,
which is *not* one of the three labels — wait, checked again: it is in fact labelled "**Note.**"
in the source) I have treated as non-normative only when the bold label says so, never from the `>`
marker alone.

---

## Sections read closely (by line range, this file)

- §1–§4 (Preliminaries, conformance, terminology, encoding): lines 1–630.
- §5–§10 (Part I, container): lines 631–1651. Front block/trailer §6 read in full (lines 782–965).
  Directory/records §7 in full (966–1231). Integrity §8 in full (1232–1274). Lifecycle §9 in full
  (1275–1560), including the crash-example block (1342–1365) and recovery scan §9.6 (1459–1505)
  and coverage verification §9.7 (1506–1560). Extension points §10 in full (1561–1650).
- §11–§14 (Part II, array model): lines 1653–2193, including grid arithmetic §11.2, linearization
  §11.4, fill §13, tile serialization §14 (byte layout §14.2, packed bool §14.3, padding content
  §14.5).
- §15–§16 (tile index, slabs): lines 2194–2424, in full.
- §19 (Reading): lines 2906–3125, in full — open algorithm, validation timing, layer access,
  tile-read algorithm.
- §20 (Writing and Updating): lines 3125–3728, in full — writer tiers, creation, the append
  procedure (`[R-WRT-04]`) with its worked examples, re-emission/preservation (`[R-WRT-05]`
  through `[R-WRT-08]`), and rewriting (`[R-WRT-06]`, `[R-WRT-07]`, `[R-WRT-09]`).
- §21 (Error register and limits): lines 3729–4236, in full — reading-the-register rules, F/L/T/R
  tables, §21.6 non-violations, §21.7 unwitnessed-condition test, §21.9 limits.

Not read closely (skimmed headers/grep only, judged not load-bearing for this charter): §12.1–12.3
sample-type catalogue beyond what §14 needs, §17 (codecs/filters) beyond the register rows already
quoted, §18 (user metadata) beyond the register rows and `[R-CNT-25]` quarantine already needed for
record-preservation reasoning, §22–§24 (security, privacy, conformance vectors).

---

## Verified computations (local, no file I/O)

1. **CRC-32C check vector** (§4.5): implemented CRC-32C (Castagnoli, poly 0x1EDC6F41 / reflected
   0x82F63B78, init 0xFFFFFFFF, final XOR 0xFFFFFFFF) from scratch and checked:
   - `crc32c(b"123456789")` = `0xE3069283` — matches the document's stated check vector exactly.
   - `crc32c(b"")` = `0x00000000` — matches.
2. **§7.4 worked layer-record example** (rank-1 `sst` layer, entry_count = 4, all-sentinel index):
   - region = 4 × (`FF`×16 `00`×4) = 80 bytes; computed `crc32c(region)` = `0x80A34955` → matches
     the document's stated segment CRC and its little-endian byte form `55 49 A3 80`.
   - `crc32c(bytes.fromhex("5549a380"))` = `0xC4EE982E` → matches the document's stated
     `crc_of_crc_array`.
   - Both check out; this example is internally consistent.
3. **§15.4 full-sentinel-segment constant** (`[R-IDX-05]`): built one segment of 2¹⁶ sentinel
   entries (20 × 65,536 = 1,310,720 bytes) and computed its CRC-32C: `0xEECB3BB2` — matches the
   document's stated constant exactly.
4. **§15.4 entry_count = 1,000,000 example**: 16 segments (15 full + one of 16,960), CRC array
   64 bytes, index region 20,000,064 bytes, tile 999,999 at segment-relative byte 339,180, CRC
   array at region bytes [20,000,000, 20,000,064), segment 15 at [19,660,800, 20,000,000) — all
   arithmetic re-derived and matches the document's stated numbers exactly.
5. **§20.3 append-cost example** ("Superseding one 100,000-byte stored tile of a 32-tile
   interleaved layer..."): the document states the new index region is "32 · 20 + 4 = 664 bytes".
   Recomputed: 32 × 20 = 640; ⌈32/2¹⁶⌉ × 4 = 1 × 4 = 4; **640 + 4 = 644, not 664.** The document's
   own stated formula (`[R-CNT-17]`: `entry_count × 20 + ⌈entry_count/2¹⁶⌉ × 4`) is correct; the
   worked arithmetic in this Example is wrong by 20. This is finding **writerb-01** below.

---

## The byte-layout walk (creation)

A creator follows `[R-LIF-02]`'s creation path as `[R-WRT-02]` restates it: front signature block
first, then each layer's stored tiles / tile-index regions / record extents (order free, subject to
§5.2 coverage and any declared alignment/slab invariant), then the complete directory + its CRC,
then a barrier, the pad, the trailer (fresh nonzero `file_id`), then a second barrier.

### W1 — smallest conforming file

The document gives this as a worked Example at §5.1 (line 656):

> "The smallest conforming file is exactly 128 bytes: front block [0, 16); an empty directory —
> zero records, so 4 bytes holding the CRC-32C of zero bytes, `0x00000000` — at [16, 20); 44 bytes
> of slack, zeroed by advice; trailer at [64, 128). It contains no layers (a valid, empty file)."

This is consistent with the hard floor `[R-CNT-27]` states independently (front block + a
≥4-byte directory at an offset ≥16 + a 64-byte trailer at a 64-aligned offset "cannot be satisfied
in fewer" than 128 bytes) and with `[R-CNT-06]`'s field-by-field trailer gate. Full layout:

| Region | Offset range | Size | Content |
|---|---|---|---|
| Front signature block | [0, 16) | 16 | `89 54 41 52 4E 0D 0A 1A` then 8 zero bytes (§6.1) |
| Directory region | [16, 20) | 4 | CRC-32C of zero preceding bytes = `00 00 00 00` (§7.1) |
| Pre-trailer pad (slack) | [20, 64) | 44 | unconstrained content; zeroed by advice (`[R-CNT-03]`) |
| Trailer | [64, 128) | 64 | see below |

Trailer field values (§6.2's table, filled in for this minimal file):

| Offset (in trailer) | Field | Value |
|---|---|---|
| 0 | trailer magic | `8A 4E 52 41 54 0D 0A 1A` |
| 8 | version_major | `1` |
| 10 | version_minor | `0` — the lowest minor "that defines every feature present in the file", which for an empty file is 0 (`[R-CNT-26]`) |
| 12 | flags | `0x00000000` — a creator "MUST write flags = 0" (§6.3) |
| 16 | dir_offset | `16` |
| 24 | dir_length | `4` |
| 32 | committed_file_length | `128` |
| 40 | file_id | nonzero; writer's choice, SHOULD be drawn cryptographically at random (§9.3) — not fixed by the document |
| 48 | reserved | 12 zero bytes |
| 60 | trailer CRC | CRC-32C of trailer bytes [0,60) — a function of `file_id`, so not a fixed numeral; formula is fixed |

`dir_offset = 16` satisfies "≥16"; `dir_length = 4` satisfies "≥4"; `dir_offset+dir_length = 20 ≤
F−64 = 64`; `committed_file_length = 128 = F`, a multiple of 64; `file_id ≠ 0`; reserved bytes zero
— every `[R-CNT-06]` gate is satisfied with no slack besides the 44-byte pad. The document does not
fully determine `file_id` or the trailer CRC numerically (both depend on the writer's random draw),
which I report as such in the probe answer rather than inventing a number.

---

## W2 — appending one superseded tile in a 32-tile interleaved layer

This is also a worked Example, at §20.3 (right after `[R-WRT-04]`, lines 3396–3403):

> "Superseding one 100,000-byte stored tile of a 32-tile interleaved layer appends: the new payload
> (100,000 bytes), the layer's full new index region (32 · 20 + 4 = 664 bytes — one entry
> re-pointed, 31 byte-identical), the new directory (every record byte-identical except the
> modified layer's), the pad, and the 64-byte trailer. The prior index region and the superseded
> payload become slack, reclaimable only by a rewrite (§20.5)."

I recomputed the index-region arithmetic (see "Verified computations" #5): **644 bytes, not 664**
— the document's own normative formula, `[R-CNT-17]`, is `entry_count × 20 + ⌈entry_count/2¹⁶⌉ × 4`;
for entry_count = 32 that is 32×20 + 1×4 = 644. This is finding **writerb-01**.

Regions appended, in commit order (`[R-LIF-02]` steps 2, 3, 5 as `[R-WRT-04]` details them):

1. **New stored-tile payload** — 100,000 bytes (the new tile content; §5.2 stored-tile extent).
2. **New tile-index region for the touched layer** — entry_count × 20 + ⌈entry_count/2¹⁶⌉×4 =
   32×20+4 = **644 bytes** (corrected). Per `[R-WRT-04]` step 4: "every layer whose stored-tile set
   or index content this commit changes has its tile-index region re-emitted in full... with
   entries for tiles this commit stores or supersedes written to their new state... and every other
   entry byte-identical at its disk-ordinal position" — one of the 32 twenty-byte entries is
   re-pointed to the new payload's offset/length/crc; the other 31 are byte-identical to before;
   the trailing 4-byte segment-CRC array is recomputed over the (now 32-entry) segment.
3. **New complete directory + its CRC** (`[R-LIF-02]` step 3 / `[R-WRT-04]` step 5) — same total
   size as before, since only the touched layer record's extent slot (fixed-width u64 pair) changes
   value, not width; "every record byte-identical except the modified layer's."
4. **Pre-trailer pad** — zero or more bytes to the next 64-byte boundary (`[R-LIF-02]` step 5).
5. **Trailer** — 64 bytes, same `file_id`, `committed_file_length` = new end, ignore-lane bits
   copied forward and no other set (`[R-CNT-08]`), `version_minor` per `[R-CNT-26]`.

**Prior bytes that become slack:** the superseded tile's previous stored bytes (size not given by
this scenario — it is whatever the previously-stored tile's length was, not necessarily 100,000);
the layer's *prior* tile-index region (also 644 bytes, since entry_count is unchanged by a pure
supersede); the prior directory; the prior pad; and the prior trailer. All five are explicit in the
document: "The prior index region and the superseded payload become slack" plus the general rule
(`[R-LIF-02]` step 3's Note, §5.1's three-commit example) that a commit's directory, pad and
trailer are always freshly emitted and the previous ones become slack.

---

## W3 — appender's input carries an unimplemented-type top-level record with MU = 1

First, what such a record can be in a *conforming* input at all. `[R-CNF-03]`'s own parenthetical
(§2.3) states it directly: a conforming reader must carry "no top-level record of a type it does
not implement with MUST_UNDERSTAND = 1 — **in a conforming file such a type is necessarily from the
experimental range, since a reserved-range type carrying MU = 1 is itself a violation**." So the
scenario, restricted to a conforming input, is an experimental-range (≥0x8000) top-level type with
MU=1.

`[R-CNT-15]` (§7.2): "An unknown record type at file scope: MU = 1 → reject-file". This binds every
reader, and `[R-WRT-01]`/§20.1 makes an appender a reader of the file it extends first (`[R-CNF-11]`).
§20.4's table states it explicitly for updaters: "At file scope no commit is available at all: the
updater is a reader of the file first (§2.3), and `[R-CNT-15]` makes an unimplemented top-level
MU = 1 record reject-file — the same treatment §6.3 gives an unknown incompat-lane bit."

**What the appender may do to the file:** nothing. It must reject the file as a reader before any
commit step, exactly as it would an unknown incompat-lane flag bit (§20.1: "An updater encountering
an unknown incompat-lane bit is a reader first, and therefore rejects the file before modifying
anything.") No append is available — not even one that avoids the unknown record's scope, because
the violation is at file scope, not layer scope (contrast `[R-CNT-18]`'s layer-scope version, which
"blocks modification of that layer... leaving other layers editable" — that is not this case).

**What a rewriter may do:** the same refusal, stated as its own rule at §20.5, `[R-WRT-06]`: "A
rewriter MUST refuse to rewrite a file carrying any record whose type it does not implement with
MU = 1: such a type can define references this specification does not (§7.2), so its bytes cannot
be safely relocated." So a rewriter also may do nothing — it must refuse to produce any output file.

Note for the record: this is one of the document's two named "conforming files a reader
nevertheless refuses" cases (§21.6, closing paragraphs): the *file* is not nonconforming (an
experimental-range MU=1 top-level record is licensed by `[R-CNF-02]`), yet every reader — ordinary,
appender, or rewriter — is obliged to reject it outright. `[R-CNF-13]`/§21.6 flag this as a
capability refusal, not a validity finding, and instruct the diagnostic to say so distinctly from
"corrupt".

---

## W4 — unimplemented top-level type, MU = 0, PE = 0

§20.4's table, MU=0/PE=0 row:

> "Retain byte-identical, or drop it — its extent becoming slack. The licence is the bit's own:
> whoever fixed PE = 0 for the record, the writer that stored it or the definition that governs it,
> declined preservation across edits, so **an appender MAY drop the record in any commit it is
> otherwise free to make — one whose only effect is the drop included** — and **a rewriter MAY drop
> it in any rewrite**. An updater that drops such a record **SHOULD report** the loss; unreported,
> application state disappears with no diagnostic."

Answers:
- **May an appender drop it in a commit whose only effect is the drop?** Yes — explicitly licensed
  ("one whose only effect is the drop included").
- **May a rewriter drop it?** Yes — "a rewriter MAY drop it in any rewrite."
- **Must either report the loss? Under which keyword?** Not MUST — **SHOULD** ("An updater that
  drops such a record SHOULD report the loss"). This is a deviation-permitted recommendation, not a
  hard requirement; failing to report does not itself make the output file nonconforming (SHOULD
  deviations are advisory per `[R-CNF-12]`), but the document is explicit about the cost: "unreported,
  application state disappears with no diagnostic."

---

## W5 — ignore-lane bit 20 set in the input trailer

§6.3, `[R-CNT-08]`, distinguishes creator / appender / rewriter conduct precisely:

> "a writer creating a file under this text MUST write flags = 0, but a set ignore-lane bit is not
> a file-conformance violation... A rewriter, though its output is a new file, carries the input's
> unknown ignore-lane bits into its output trailer rather than writing flags = 0, and sets no other
> (§20.5, `[R-WRT-06]`). An updater MUST copy forward unknown ignore-lane bits of its input file,
> MUST NOT set any other."

And §20.1, `[R-WRT-01]`, states the same split from the writer-tier side: "As a **creator** it
undertakes nothing toward its input, whatever it read: §20.2 binds it, it writes flags = 0..."

Taking bit 20 (an ignore-lane bit, since bits 16–31 are the ignore lane) as the *only* set bit of
the input trailer's flags field (value `0x00100000`):

- **(a) Appender's commit output trailer flags:** `0x00100000` — copied forward unchanged, no other
  bit set (`[R-CNT-08]`, `[R-WRT-04]` step 6: "unknown ignore-lane flag bits copied forward and no
  other set").
- **(b) Rewrite output trailer flags:** `0x00100000` — same rule, stated again at §20.5: "The
  output trailer MUST copy the input's unknown ignore-lane flag bits forward and set no other, in
  place of the flags = 0 §6.3 requires of a file created under this text."
- **(c) A creator that read the input and writes a new file from what it decoded:** `0x00000000`.
  A creator "undertakes nothing toward its input" (§20.1) and "MUST write flags = 0" under this
  text (§6.3) regardless of what it read — the ignore-lane bit is *not* carried forward, because
  writing flags=0 is what makes it a creator rather than a rewriter in this document's taxonomy;
  carrying the bit forward is specifically the rewriter's (and appender's) obligation, not a
  creator's option.

This is a clean three-way split the document draws deliberately (it says so: "in place of the
flags = 0 §6.3 requires of a file created under this text" — an explicit contrast).

---

## W6 — commit changes only a layer's fill value, on a layer that stored a tile in the superseded generation

**Not permitted as an appender's operation.** §20.3 step 4 states the closed list of what a commit
*may* change on a layer that "stores a tile in the generation this commit supersedes" (name,
dimension/channel names, extent growth, planar-channel-list extension/shortening at the end, slab/
alignment declare-or-clear) and then states explicitly what is excluded: "a shrink, **a fill
change**, a re-type, a re-tiling, a change to the dimension order, a change of rank, layout,
linearization, index encoding, codec or filter... are rewrites even where a particular file would
survive them in place, because deciding which files would is the edge this list exists to remove."

**What the document offers instead:** "The change is a new layer, or a rewrite that re-declares it
under a fresh file_id (`[R-LIF-01]`, §20.5)" (§20.3 step 4, main paragraph). I.e. either (i) drop
this layer under its old declarations via a new layer under the same or a different name with the
new fill, or (ii) a whole-file rewrite performing a `[R-WRT-06]`/§20.5 "re-declaring" of the layer.

**Is the bar itself a file-conformance rule, or actor conduct?** The document is explicit that this
specific bar is *conduct*, not a predicate on bytes: "This bar binds the commit as an actor: no file
is nonconforming by virtue of its violation, and no register row records the violation itself... a
file such a commit leaves **can be** nonconforming on its own terms, as the paragraph below sets
out" (§20.3 step 4). The very next paragraph names the actual witnesses: "...but for a stored
tile's decoded size, a padding position or pad bit, or a boolean byte the register witnesses (T3,
T14, T21, T22, T4, T5, T2)... no check any actor owes able to see it (§21.7)."

Applied to a **pure fill-value change with nothing else touched**: fill only governs (i) unstored
(sentinel) tiles' reference-array values (`[R-TYP-08]`) and (ii) the content of *padding positions*
inside already-stored tiles (`[R-SER-05]`, §14.5: "at every padding position, a writer MUST encode,
for each channel the position carries, that channel's fill value"). So:

- If any tile of this layer that is **stored** in the surviving generation has **padding
  positions** (i.e. some dimension's extent is not a multiple of its tile extent, §11.3), those
  positions' bytes were written under the *old* fill and now mismatch the *newly declared* fill.
  That is exactly condition **T4** ("A padding position does not encode... that channel's recorded
  fill value"), a *verifier*-detected, tile-scope violation. A verifier that checks it will find the
  resulting file **nonconforming** at those tiles.
- If the layer has **no padding positions** at all (every dimension's extent divides its tile
  extent evenly) and every currently-addressed tile is already stored (no sentinel tiles remain to
  newly read as the changed fill), then nothing in the register is positioned to witness the
  change: fill is otherwise never compared against stored bytes. In that narrow case the resulting
  file is not shown nonconforming by any check this document defines — matching `[R-CNF-02]`'s
  general point that a conduct violation need not leave a byte-level trace, and §21.7's framework
  for "unwitnessed" conditions.

So the honest answer to "is the file such a commit would leave nonconforming?" is: **it depends on
whether the layer has any stored tile with padding positions** (then yes, via T4) **or any sentinel
(unstored) tile whose reference-array reading would silently change** (then the byte-level content
is unaffected, but the *values* a reader returns for that tile change between generations with no
new stored bytes — a real, if not independently registered, consequence) — **otherwise the
document does not make the resulting bytes fail any stated check**, even though the commit itself
is barred as an actor obligation regardless. I record this precisely because it is the kind of place
the charter asks me to flag: whether resolving it changes what a conforming implementation may
emit is genuinely conditional on the layer's own geometry, and the document says so itself rather
than leaving it silently undetermined.

---

## W7 — crash after the directory is durable, before the trailer is durable

Commit protocol, `[R-LIF-02]`: "...(3) append the new complete directory... followed by its CRC;
(4) make steps 1–3 durable (a storage barrier...); (5) append the pad... and the new trailer...;
(6) make the trailer durable." The described crash point is *after* step 4's barrier returns but
*before* step 6's barrier is confirmed — i.e., somewhere during or immediately after step 5.

**What the next reader sees.** §9.5, `[R-LIF-05]`: "The default read path is
trailer-at-end-or-fail: a reader that finds no valid trailer in the final 64 bytes MUST report the
file torn or invalid and MUST NOT scan backward." Because the physical file was already extended
past the old trailer during step 5 (pad + trailer bytes appended, even if not confirmed durable),
the *old* trailer is no longer at the physical end of file, and the *new* trailer's bytes are, by
hypothesis, not reliably present/complete at that end (that is what "before its trailer is durable"
means operationally — the crash may have left them partially written, fully written but unflushed
from a volatile cache, or entirely absent depending on the storage stack). A default-path reader's
final-64-byte validation therefore fails one of `[R-CNT-06]`'s gates (magic F8, or CRC F14, or
committed_file_length-vs-size F17, depending on exactly what landed) and it reports the file torn —
it "MUST NOT scan backward" to find the still-intact prior trailer itself (`[R-LIF-05]`).

**Is the (whole, current-length) file conforming?** No. §5.1/`[R-CNT-01]`: "The file size of a
conforming file equals the live trailer's committed file length F" — for the physical byte string
as it now stands (with the aborted trailer, or no trailer, at its very end) there is no valid
trailer *at the physical end*, so it fails `[R-CNT-06]`'s trailer gates and is not a conforming
TARN file under the definition of conformance as "a byte sequence satisfying every file-level
requirement" (§2.3). This is exactly the "torn" state §9.2's worked example (lines 1342–1365)
depicts: "Mid-commit the physical tail is not a trailer, so a reader on the default path reports
the file torn... What makes that recoverable rather than fatal is that trail_n and everything it
reaches are still byte-intact."

**What the next appender does.** It may not simply resume: `[R-LIF-04]`, §9.4: "A writer beginning
a commit against an existing file MUST establish F by validating the trailer in the final 64 bytes
of the physical file... If that validation fails, the file is torn: the writer MUST NOT append, and
locating the last committed state is the deliberate recovery operation of §9.6 — never an implicit
step of opening for append." So the appender must invoke the §9.6 recovery scan: probe backward at
64-aligned offsets for the trailer magic, and for the nearest-to-end candidate that survives
*whole-file re-verification* (§9.6, `[R-LIF-06]`), accept that as the last committed state — which,
because the crash happened after the prior generation's trailer and before this one's is durable,
will be the *prior* generation's trailer (the one at the old F). The recovery tool then truncates
the physical file back to that old F (or the appender, per `[R-LIF-04]`, "truncate[s] to F before
step 1... or overwrite[s] from F and truncate[s] the physical file to the new
committed_file_length no later than step 6"), and only then proceeds with a fresh commit attempt
from that re-established F. The half-written directory, pad and any partial trailer bytes past the
recovered F become the new commit's overwritten/discarded region — nothing about them is
"repaired"; they are simply never part of any live state again.

One qualification the document itself is careful about (`[R-CNF-02]`, §9.2's second discussion,
lines 1304–1311): if, by the storage stack's own behavior, the new trailer's bytes actually *did*
reach stable media completely and correctly before the crash — the crash only interrupted the
writer's *confirmation* of durability (step 6 is "conduct... rather than... output") — then a
reader opening the file afterward would in fact find a fully valid new trailer at the physical end,
and would accept the file as a normal, later generation with no torn-file symptoms at all: "a
barrier orders writes against power loss and leaves no trace in the bytes, so a file committed
without one can be byte-identical to a file committed with it." I treat this as the fourth of my
four crash points (below), since it is the one place the document explicitly says the writer's own
belief about whether it committed successfully can diverge from what a reader actually observes.

### The four crash points (charter requirement)

1. **Mid-payload/mid-index (during step 2), before the directory CRC exists.** No new candidate
   trailer can exist. Default reader: unaffected if it doesn't re-stat; a reader opening fresh sees
   whatever the *current* physical end is — if untruncated leftover bytes from the aborted write
   sit past the old trailer, the default path still reports torn (`[R-LIF-05]`), even though
   nothing of substance was lost. Appender: `[R-LIF-04]` truncate-to-F (the old F) before retrying.
2. **Mid-directory (during step 3), directory CRC not yet complete/durable.** Same reader-facing
   outcome as (1): no new trailer exists, default path reports torn if the physical file was
   extended past the old trailer; recovery scan (§9.6) finds only the old trailer as a candidate.
3. **After step 4's barrier (payload+directory durable) but during/after step 5, before step 6's
   barrier is confirmed** — the scenario W7 asks about directly. New trailer bytes may be present,
   absent, or partial; default reader reports torn per `[R-LIF-05]`; deliberate recovery (§9.6) is
   required and lands on the *old* trailer as the last committed state, per the reasoning above.
4. **After step 5's bytes are actually complete and stable on the medium, but before/without the
   writer ever confirming step 6's barrier.** This is `[R-CNF-02]`'s named edge: a "conduct" gap
   with no byte-level trace. A reader opening the file afterward sees a fully valid new trailer and
   accepts it as an ordinary next generation — indistinguishable from a "successful" commit, even
   though the writer that performed it never received confirmation and, strictly, violated its own
   step-6 obligation as an actor. The document is explicit that this does not make the file
   nonconforming (`[R-CNF-02]`'s conduct/output distinction).

---

## W8 — rewriter carrying forward a layer with an "unimplemented sample type"

I flag first that the premise does not fit this document's model of sample types, and I answer
accordingly rather than silently assuming a different model.

**Why the premise is foreclosed for a conforming rewriter.** `[R-TYP-01]` (§12.1): "This
specification defines exactly thirteen sample types, all **core**: a conforming reader MUST decode
every one of them, and none is skippable (`[R-CNF-03]`)." `[R-CNF-06]` makes an updater (appender or
rewriter) a class that "MUST satisfy every writer requirement for the bytes it produces," and
`[R-WRT-01]`/`[R-CNF-11]` make it "a reader of every structure it processes" — so a tool that cannot
decode one of the 13 core sample types is not a conforming reader in the first place (`[R-CNF-03]`:
"software that declines to support a core... sample type... is not a conforming reader, even if it
reads all other conforming files correctly"), and therefore not a conforming rewriter either. There
is no scenario, in this document's vocabulary, in which a *conforming* rewriter legitimately "does
not implement" one of the 13 assigned sample types the way it might legitimately not implement an
experimental-range *record* type.

The only way a channel's declared sample type can be one the rewriter "does not implement" is if
its numeric value lies **outside 1–13** — reserved (14–19, 20–0x7FFF) or experimental (≥0x8000).
But that is not an "undecodable but otherwise fine" tile: it is `[R-TYP-03]`'s value-set violation,
registered as **L34** ("A channel entry's type is outside 1…13"), a **layer-scope, reader-detected**
violation whose detection point is **layer access** (§19.3, `[R-RDR-03]`) — *before* any tile is
ever read. A rewriter meets this exactly as any reader does, at the mandatory full validation of
the layer record that precedes "any use of the layer's declarations" (`[R-RDR-03]`).

So, answering the probe's three sub-questions against that corrected premise:

- **What must it verify about each stored tile it copies?** Nothing tile-specific gets that far:
  the layer record itself fails full validation (`[R-RDR-03]`) at layer access, before the rewriter
  ever reaches an index entry or a stored tile's bytes. (If instead the scenario is read as "the
  entries and record are all structurally valid, only the rewriter personally lacks a decoder" —
  which, per the paragraph above, cannot happen for a conforming updater — the general rule would
  still apply: `[R-WRT-09]` obliges it to "verify each link of the chain — the open (§19.1), each
  retained layer's record (§19.3) and full index chain (`[R-IDX-04]`), and the checksum §8.1 states
  over each extent it copies, every stored tile's entry crc among them — before emitting that
  structure's bytes," "whatever it decodes" (§20.1) — i.e. checksum verification of copied bytes is
  never conditioned on being able to decode them.)
- **What does it do when a checksum fails?** `[R-WRT-09]`/§20.5: "A rewriter MUST refuse to rewrite
  when any check `[R-WRT-09]` obliges fails, and MUST NOT emit a file carrying a violation it has
  detected: it can neither re-emit the structure corrected (`[R-WRT-05]`), nor keep it and call the
  output clean. Dropping is the one disposal that answers, and **only where §20.4's table licenses
  it**... Where the table does not license a drop the rewriter MUST refuse." The layer record's
  registry-fixed flags are MU=0, PE=0 (§7.3), which §20.4's table licenses for dropping — "the layer
  record carries PE = 0 and is dropped under the table's last row" — and "a commit MAY therefore
  drop a layer record, and the drop takes the layer whole." So the rewriter's two disposals are:
  **drop the whole layer** (SHOULD report the loss, per §20.4's table) or **refuse to rewrite the
  file at all**. There is no documented per-tile partial remedy inside a rewrite (contrast an
  appender's live commit, which may legitimately choose to *unstore* one bad tile going forward,
  §20.3 step 4: "Unstoring a tile... is how a commit discards data in place; discarding is the
  caller's operation and this specification does not bar it" — that option belongs to a fresh
  commit changing the stored-tile set, not to a rewrite's carry-forward-verbatim path).
- **May it instead re-create the layer?** Only if it *can* decode the layer as a reader — §20.5:
  "A layer the rewrite re-creates is new output: its record, its tile-index region and its stored
  tiles are written under §20.2's rules from content the rewriter decoded (§19.3, §19.4)." By the
  scenario's own premise (an unimplemented type, or, corrected, a value the type field forbids
  outright) the rewriter cannot decode this layer, so re-creation is not available to it — the
  document's re-creation path is explicitly gated on decoding capability, not an alternative to it.

I record the type/record asymmetry above (all sample types mandatory-core vs. record types having a
genuine open/registry-based unimplemented tier) as an **OBSERVATION** rather than a document defect:
the document is internally consistent about it (`[R-TYP-01]`, `[R-CNF-03]`, `[R-TYP-03]`/L34 all
agree), it is simply a place where the probe's premise ("an unimplemented sample type") does not
describe a state this document allows a conforming implementation to be in.

---

## Findings

### writerb-01 (OBSERVATION, non-normative arithmetic slip)

**Location:** §20.3, the worked Example immediately following `[R-WRT-04]` ("Superseding one
100,000-byte stored tile of a 32-tile interleaved layer appends...").

**Quotation:** "the layer's full new index region (32 · 20 + 4 = 664 bytes — one entry re-pointed,
31 byte-identical)"

**Detail:** 32 × 20 + 4 = 644, not 664 (verified by direct computation). The document's own
normative formula for this quantity, `[R-CNT-17]`, is `entry_count × 20 + ⌈entry_count / 2¹⁶⌉ × 4`,
which for entry_count = 32 gives 640 + 4 = 644 — the same number I compute independently. This
Example is labelled "**Example.**", so under `[R-CNF-01]` it is non-normative, and the normative
formula controls what a conforming implementation actually emits or accepts: no conforming writer's
output bytes, and no conforming reader's acceptance decision, is determined by this Example's
arithmetic. An implementer who followed the Example's number instead of the formula (e.g. hand-
verifying a test vector against "664" rather than computing from `[R-CNT-17]`) would be led to a
wrong self-check, though not to nonconforming *output*, since real output is sized by the formula
applied to real data, not by copying this example's stated total. I therefore mark
`byte_level: false` — the defect is in the illustration's arithmetic, not in a place where two
readings of a normative rule would produce different bytes.

---

## Probe answers summary

See W1–W8 sections above for full derivations and citations; `probe_answers` restates each
concisely per the schema, citing the same requirement IDs.
