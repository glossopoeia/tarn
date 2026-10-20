# Writer/Updater fidelity walk — Edition A — working transcript

## Disclosure (mandatory, read first)

- **Access taken.** I read exactly one file:
  `/Users/robertkleffner/Documents/GitHub/tarn-first-draft/scratch/cleanroom/editions/a/tarn.md`
  (5,004 lines / 303,815 bytes), in eight sequential `Read` calls (offsets
  1, 651, 1301, 1951, 2601, 3251, 3901, 4550) covering the entire file with
  small overlaps, start to finish, including all appendices (A–H). I ran
  `wc -l` and `wc -c` against that same file (nothing else) to size my read
  plan, and `mkdir -p` to create my own scratch directory. No other file was
  opened, no directory was listed for content, no git history/diff, no web
  search/fetch. I did not encounter or open any other copy of this
  specification.
- **Unsolicited context.** Before this task text, my runtime surfaced a
  project `CLAUDE.md` pointer, a user memory-index file (a bulleted list of
  prior-round note titles), a git-status/environment block, model identity,
  and a list of available skills/deferred tools. None of this is part of
  the specification and none of it is evidence about the specification; I
  disregarded its content entirely and am not repeating it here beyond
  this one acknowledgment.
- **Relayed "user request".** A message "Go" was prepended above the
  computed brief, labelled as the user's request to the orchestrator. It
  predates my spawning, is not a task for me, and does not widen the
  access rule. Noted and set aside.
- **Path check.** The file exists at exactly the path the brief named;
  no discrepancy to report.
- **Wrapping caveat applied.** The document is hard-wrapped prose with
  `> ` blockquote continuations. I did not rely on line-oriented `grep`
  for prose claims in this transcript; all quotations below are taken
  from my own sequential read of the full file (rendered, unwrapped, in
  my context), not from a line-grep. Where I state "no other sentence
  speaks to X", that is based on having read every section of the
  document once, start to finish, not on a single zero-hit grep.

## Document map (for my own orientation)

Part 0 (§1–§4): intro, conformance vocabulary, terminology, encoding
conventions. Part I (§5–§10): container — file anatomy, front block/trailer,
directory & records, integrity, lifecycle/commit protocol, extension
registry. Part II (§11–§18): array model — layers/tiling, channels/types,
fill, tile serialization, tile index, slabs/alignment, codecs/filters, user
metadata. Part III (§19–§24): reading algorithm, writing/updating
(creator/appender/rewriter), error register (§21, rows F*/L*/T*/R*),
security/privacy, conformance vectors. Appendices A–H: worked minimal file,
constants, registry snapshot, design rationale, changelog, references,
reproducible-writer profile, conformance checklists.

My charter is the **writer/updater byte-layout walk**: creation layout,
append procedure (incl. preservation/MU/PE), slack per commit shape,
torn-write recovery at four crash points, and the legitimate
byte-divergence catalogue between two conforming writers — plus the 11
probes below.

---

## PART A — The byte-layout walk

### A.1 Creation: smallest conforming file (ties to Probe W1)

`[R-CNT-27]`/§5.1: "No conforming file is shorter than 128 bytes: the
front signature block, a directory of at least 4 bytes at an offset of at
least 16, and the 64-byte trailer at a 64-aligned offset cannot be
satisfied in fewer."

§5.1's own worked example and Appendix A give the exact byte-for-byte
minimal file (file size F = 128):

```
[0,8)     89 54 41 52 4E 0D 0A 1A      front signature magic           (§6.1)
[8,16)    00*8                         front signature reserved        (§6.1)
[16,20)   00 00 00 00                  directory region: 0-byte record
                                        sequence + CRC-32C(empty)=0     (§7.1)
[20,64)   00*44                        pre-trailer pad — SLACK          (§6.2, R-CNT-03)
[64,72)   8A 4E 52 41 54 0D 0A 1A      trailer magic                    (§6.2)
[72,74)   01 00                       version_major = 1
[74,76)   00 00                       version_minor = 0
[76,80)   00 00 00 00                 flags = 0 (incompat & ignore lanes clear)
[80,88)   10 00 00 00 00 00 00 00      dir_offset = 16
[88,96)   04 00 00 00 00 00 00 00      dir_length = 4
[96,104)  80 00 00 00 00 00 00 00      committed_file_length = 128 = F
[104,112) EF CD AB 89 67 45 23 01      file_id (nonzero, writer-chosen; here 0x0123456789ABCDEF)
[112,124) 00*12                       trailer reserved = 0
[124,128) 7E 15 2F 40                 trailer CRC-32C over trailer[0,60) = 0x402F157E
```

Cross-check against the §6.2 trailer layout table (relative offsets 0, 8,
10, 12, 16, 24, 32, 40, 48, 60; sizes 8,2,2,4,8,8,8,8,12,4) plus the
trailer base at absolute 64: every field above lands exactly where
`0x40 + relative_offset` puts it — I verified this arithmetically field by
field (e.g. relative 16 → dir_offset at absolute 80, matching Appendix A's
`[80,88)`). No layer records: "a directory carrying no layer record is a
conforming generation, an empty directory included" (`[R-CNT-14]`, and
restated as a non-violation in §21.6: "The file contains zero layers").

Region/trailer values, exactly per the ask: front block [0,16); directory
[16,20) with 0 records and directory CRC = CRC-32C(∅) = `0x00000000`
(given in §4.5's check vector: "The CRC-32C of zero bytes is
`0x00000000`"); pad [20,64) = 44 bytes of slack; trailer [64,128) with the
ten field values listed above.

### A.2 The append procedure, including a record of an unimplemented type (ties to W2–W4, W9–W11)

**Order of operations** (`[R-WRT-04]`, restating `[R-LIF-02]`):
1. Establish F from the existing trailer (`[R-LIF-04]`); if that fails the
   file is torn and the appender **MUST NOT** append (§9.4) — recovery
   (§9.6) is a separate, deliberate operation.
2. Open the file as a reader (§19.1) — a reject-file violation bars every
   commit; a reject-layer violation bars only a commit touching that layer.
3. Validate what the commit touches, to `[R-WRT-03]`'s depth (trailer +
   full directory always; §19.3 layer validation for every layer the
   commit modifies; §19.4 index-chain verification for every segment whose
   entries the commit reuses).
4. **Write payloads and indexes**, beginning at exactly F: new stored
   tiles and record extents, in any order satisfying §5.2's coverage
   classes (placement between structures is free per `[R-SLB-05]` except
   where an alignment/slab declaration constrains it); every layer whose
   stored-tile set or index content changes gets its **whole** tile-index
   region re-emitted at a new placement; untouched layers' extent slots
   are carried byte-identically, still pointing at their existing region
   (`[R-WRT-05]`).
5. Re-emit the complete directory + its CRC (`[R-LIF-02]` step 3).
6. Commit: barrier; pad to the next 64-byte boundary; new trailer (same
   file_id, committed_file_length ≥ prior + 128, ignore-lane bits copied
   forward and no other set); barrier.

**A record of a type the appender does not implement, with MU = 1, at
top level** — this is Probe W3's subject, worked through here because it
gates everything else in the append: §20.4's table, MU = 1 row: *"At file
scope no commit is available at all: the updater is a reader of the file
first (§2.3), and `[R-CNT-15]` makes an unimplemented top-level MU = 1
record reject-file — the same treatment §6.3 gives an unknown incompat-lane
bit."* So before step 4 can even begin, step 2's open already rejects the
file; no bytes are written at all. (By contrast, the **same** condition on
a layer **sub**-record only blocks modification of *that* layer — §7.2:
*"an unknown sub-record type with MU = 1 is reject-layer, and where the
file is otherwise conforming a reader MUST NOT reject the file for it."*)

**The 32-tile interleaved supersede, 100,000-byte new payload** (Probe
W2's worked numbers, taken verbatim from §20.3's own example, then
decomposed into an ordered byte-region list): *"Superseding one
100,000-byte stored tile of a 32-tile interleaved layer appends: the new
payload (100,000 bytes), the layer's full new index region (32 · 20 + 4 =
644 bytes — one entry re-pointed, 31 byte-identical), the new directory
(every record byte-identical except the modified layer's), the pad, and
the 64-byte trailer. The prior index region and the superseded payload
become slack, reclaimable only by a rewrite (§20.5)."*

Ordered list of appended regions, in commit order:
1. New stored-tile payload — **100,000 bytes** (step 4). Index-encoding
   note: entry_count = 32 ≤ 2¹⁶, so there is exactly **one** segment
   (§15.4: "Segment s covers entries [s·2¹⁶, min((s+1)·2¹⁶, entry_count))"),
   and the new index region's size follows `[R-CNT-17]`'s formula
   `entry_count × 20 + ⌈entry_count/2¹⁶⌉ × 4` = 32×20 + 1×4 = **644 bytes**
   exactly as the example states (step 4).
2. New tile-index region — **644 bytes**: 32 × 20-byte entries (31
   byte-identical to the superseded generation's entries at their
   disk-ordinal positions, `[R-WRT-05]`; 1 re-pointed to the new payload's
   offset/length/crc) + a 4-byte segment CRC recomputed over all 640 entry
   bytes as now stored (§15.4) — this single segment CRC necessarily
   changes value even though only one entry's bytes changed, because it
   covers the whole (sole) segment.
3. New directory + its 4-byte CRC (step 5) — "every record byte-identical
   except the modified layer's." I note precisely *what* changes in that
   one layer record, since the example's prose is a summary: the record's
   **extent slot** (`extent_offset`, in the 24-byte header, §7.2) changes
   to the new index region's placement, and the record's inline-payload
   field **`crc_of_crc_array`** (§7.4) changes value because the segment
   CRC array it covers changed (§8.1's map: "Tile-index region |
   the per-segment CRC array, itself covered by the layer record's
   crc_of_crc_array"). `entry_count` (32) and `extent_length` (644) are
   unchanged, since the addressed-tile count didn't change
   (`[R-CNT-17]`).
4. Pre-trailer pad (step 6) — size = `(64 − (running length mod 64)) mod
   64` bytes; not a fixed number, since the running length depends on
   writer-chosen placement (`[R-SLB-05]`) and on whatever earlier slack the
   writer did or did not leave; the document gives no fixed count for this
   case and I do not manufacture one.
5. New 64-byte trailer (step 6).

**Which prior bytes become slack**, combining the example's own sentence
with the general commit mechanics stated elsewhere (§5.2, §20.3's Note,
and the "three shapes" example): the superseded tile's old payload bytes
and the prior tile-index region (both named in the example); **and**, as
is true of every commit (not restated in this specific example but
established generally): the prior directory, the prior pre-trailer pad,
and the prior trailer — "The ▓ runs are the directories, pads and
trailers of commits 1 and 2, superseded when commit 3 wrote its own"
(§5.1); "Extents this commit supersedes become slack" (§20.3 step 4). The
example explicitly says the *new* directory is "every record
byte-identical except the modified layer's" — it does not need to restate
that the *old* directory/pad/trailer fall to slack, because that is true
of literally every commit and is established once, generally, elsewhere.

### A.3 Slack under each commit shape (§20.3's own taxonomy)

Direct quotation, since this is exactly what the charter asks for and the
document states it as a closed three-way taxonomy:

- **(a) A new layer.** "Nothing existing is rewritten... the slack is the
  old directory, pad and trailer — sized by the file's *layer count*,
  never by any layer's data."
- **(b) Tiles added to an existing layer** (supersede, growth that moves
  ordinals, or a re-declaration of an empty layer that changes index
  content). "The whole region moves because it is addressed by one extent
  slot, so a single changed entry costs its whole length... Superseded
  payloads become slack too; retained ones do not move." (This is the
  shape of §20.3's worked 100k-byte example above.)
- **(c) A change confined to the directory** — clearing a slab
  declaration, renaming a layer, or dropping a layer or another PE = 0
  record where §20.4 licenses it (the dropped layer's tiles, index region
  and sub-records' extents becoming slack); or a re-declaration of an
  empty layer that leaves index content unchanged. "Only the directory is
  re-emitted." Explicitly **excluded** from shape (c): "Editing user
  metadata is not shape (c): its document lives in an extent
  (`[R-CNT-25]`), so a new extent is appended and the old one becomes
  slack, as in (b)." And excluded in the other direction: "A change to
  any fixed declaration of a layer that **stored** a tile in the
  generation the commit supersedes... is not an appender's operation at
  all" — it is a new layer or a whole-file rewrite (ties to Probe W6).

### A.4 Torn-write recovery at four distinct crash points (ties to Probe W7)

I derive four crash points from the six ordered steps of `[R-LIF-02]`/
`[R-WRT-04]` (steps 1–3 "write"; step 4 barrier; step 5 "pad+trailer";
step 6 barrier), each with what the next reader sees, conformance status,
and what the next appender/recovery tool does.

**Point 1 — crash during step 2/3 (payload/index/directory bytes being
written, before step 4's barrier).** The physical file is longer than the
prior F but its tail is not a valid trailer region in any useful state
(whatever bytes happen to be there are mid-write and, per the barrier's
purpose, not guaranteed ordered or complete). On the default read path, a
reader fetches `[physical_size − 64, physical_size)` and finds that the
last 64 bytes fail `[R-CNT-06]`'s magic/CRC gates (F8/F14, overwhelmingly
likely since the bytes there are leftover mid-write content, not a
trailer). *"A reader that finds no valid trailer in the final 64 bytes
MUST report the file torn or invalid and MUST NOT scan backward"*
(`[R-LIF-05]`). As **bytes**, this longer byte sequence is **not a
conforming file** (it fails the trailer gate). The prior generation's
committed prefix `[0, F_prior)` remains byte-intact (`[R-LIF-01]`). Next
appender: per §9.4 (`[R-LIF-04]`), validating the physical tail fails, so
"the writer MUST NOT append"; it must run the deliberate recovery scan of
§9.6, which probes backward for the trailer magic, requires the trailer
CRC to verify and `committed_file_length = o + 64`, re-verifies the
candidate as a *whole file* (§8), and then truncates the physical file to
that recovered F (or overwrites from F and truncates by step 6,
`[R-LIF-04]`) before beginning any new commit.

**Point 2 — crash immediately after step 4's barrier (new
payload/index/directory durable) but before step 5 has appended anything
(no pad, no new trailer bytes yet).** Same analysis as Point 1 from the
reader's perspective: the physical tail still isn't a trailer (there is
none yet), so the default path reports torn, `[R-LIF-05]` forbids
scanning back, and §9.6 recovery is required exactly as above. The only
difference from Point 1 is which of the *new* generation's structures
happen to be byte-intact already (all of them, by construction, since the
barrier at step 4 covers exactly steps 1–3) — but that fact is invisible
and irrelevant to the default reader, which never scans for a non-tail
trailer (`[R-LIF-05]`), and is relevant only to a future rewriter/recovery
tool that might (per §9.6) eventually enumerate commit states from the
physical file, which is explicitly *not* the default read path.

**Point 3 — crash after step 5 (new pad and new trailer bytes appended)
but before step 6's barrier makes the trailer durable. This is exactly
Probe W7's scenario; worked in full under Probe W7 below.**

**Point 4 — crash after step 6's barrier completes.** The commit
succeeded; trailₙ₊₁ is durable, at the new physical end. The next reader's
default open succeeds against the new generation; `[R-LIF-03]`'s caching
contract holds. (Not a torn write at all — included for completeness of
the four-point walk, since steps 4 and 6 are the two barrier points that
divide the commit into exactly these four observable epochs.)

The document's own worked example (§9.2, "what a crash sees") pictures
exactly the Point-1/2-type case in its "mid-commit" row: *"│ … │ dirₙ │pad│
trailₙ │▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓ ↑ trailₙ intact, but no longer at the file's
end"* — i.e. the **default reader's 64-byte window has moved past trailₙ
into the garbage tail**, so trailₙ being byte-intact further back in the
file does the default reader no good at all; only the deliberate §9.6 scan
(never the default path) can find it. This is the same structural picture
underlying all of Points 1–3; what moves between points 1/2 and point 3 is
only which bytes of the doomed new generation happen to be on disk when
the crash lands — never whether the default reader accepts the file
(it never does, at any of points 1–3).

### A.5 Legitimate byte-divergence between two conforming writers (same logical input)

`[R-CNF-05]`: *"Writer conformance is semantic: this specification does
not promise canonical bytes, and two conforming writers given identical
input MAY produce different conforming files."* Enumerating the axes I
found stated as writer choices, each confirmed not to bear on conformance:

1. **Relative placement of every structure** between the front block and
   the directory, whenever no alignment/slab is declared (`[R-SLB-05]`) —
   affects every structure's offsets.
2. **Compressed bytes under codecs 2–4** for identical logical content —
   "two conforming encoders emit different, equally valid streams for the
   same input" (Appendix G item 1); codec 1 (none) is the only
   byte-reproducible one across implementations.
3. **`file_id`** — any nonzero value; "the creating writer SHOULD draw it
   from a cryptographically random source" (§9.3, a SHOULD, not a MUST).
4. **Gap/slack content** — "writers SHOULD zero the gaps they create"
   (`[R-CNT-03]`, a SHOULD); unzeroed slack is still conforming.
5. **Alignment/slab declaration itself** — declare neither, declare
   alignment, or declare a slab; all conforming, all producing different
   byte layouts (§16).
6. **Filter choice** (none vs. byte-shuffle, §17.3) and **tile
   extents/layout** (interleaved vs. planar, §11.3/§14.1) — all a
   writer's choice, each producing entirely different stored bytes for
   the same logical array.
7. **Record/sub-record order** in the directory — "Record semantics MUST
   NOT depend on record order" (`[R-CNT-14]`); multiplicity is the only
   constraint.
8. **Sentinel vs. explicitly-stored all-fill tile** — the base
   specification (outside Appendix G's optional profile) never requires a
   writer to sentinel an all-fill tile; two conforming writers may differ
   on this for logically identical arrays.
9. **`version_minor`** — writers SHOULD emit the lowest value that
   expresses the file's features (`[R-CNT-26]`, a SHOULD); a higher value
   is still conforming.
10. **NFC normalization of names** — SHOULD, not MUST (`[R-ENC-14]`); an
    NFD name is a *different* name under `[R-ENC-13]`'s raw-byte
    comparison, yet both are conforming names.
11. **Default fill value when the caller chooses none** — SHOULD be
    all-zero (`[R-TYP-10]`); a writer defaulting differently is still
    conforming.
12. **User-metadata encoding** (1 = none vs. 2 = zstd, §18.2) and its
    encoder settings (under encoding 2) — writer's choice.

Conduct rules (barrier timing, §9.2 steps 4/6) are explicitly *not* part
of this catalogue: they "leave no trace in the bytes" (§9.2's own
language) and so cannot be a source of *byte* divergence at all — only of
differing crash-safety, which is orthogonal to conformance (`[R-CNF-02]`).

---

## PART B — The 11 probes

Each probe below: the document's answer, the governing citation(s), and
(per the charter) every sentence elsewhere that bears on the same act,
noting agreement or disagreement.

### W1 — Smallest conforming file: byte layout + trailer field values

**Answer:** See §A.1 above for the full region table (offsets and values).
Summary of trailer fields: version_major=1, version_minor=0, flags=0,
dir_offset=16, dir_length=4, committed_file_length=128, file_id=nonzero
(writer's choice), reserved=0, trailer CRC=CRC-32C over trailer[0,60).
Governing: `[R-CNT-27]`, §6.2's table, §5.1 Example, Appendix A (which
gives the exact byte dump I cross-checked arithmetically field-by-field
against §6.2's offset/size columns — no disagreement; Appendix A is
explicitly non-normative but I verified it against the normative table
myself rather than trusting it blindly).

### W2 — 32-tile interleaved supersede, 100,000-byte payload

**Answer:** Ordered regions: (1) new 100,000-byte payload; (2) new 644-byte
index region (32×20 entries + 4-byte segment CRC, one entry re-pointed,
31 byte-identical, segment CRC recomputed); (3) new directory + CRC (the
touched layer record's extent_offset and crc_of_crc_array change; nothing
else in that record changes; every other record byte-identical); (4) pad
to 64-byte boundary (size not fixed by the document — depends on running
offset); (5) 64-byte trailer. Slack: the superseded payload, the prior
index region (both named by §20.3's example), plus — by the general rule,
not restated in that specific example — the prior directory, prior pad,
and prior trailer (§5.1 Example; §20.3's "Extents this commit supersedes
become slack"). Governing: `[R-WRT-04]`, §20.3's own worked example,
`[R-CNT-17]` (index-region size formula), §15.4 (segment definition and
why there is exactly one segment here), §8.1 (crc_of_crc_array's coverage
of the segment-CRC array).

### W3 — Appender's input carries an unimplemented top-level type, MU = 1

**Answer:** The appender **may do nothing to the file at all**: per
§20.4's table (MU = 1 row), *"At file scope no commit is available at
all: the updater is a reader of the file first (§2.3), and `[R-CNT-15]`
makes an unimplemented top-level MU = 1 record reject-file — the same
treatment §6.3 gives an unknown incompat-lane bit."* The appender's own
open step (§19.1/§20.3 step 2) establishes this reject-file violation
before step 4 ever runs, and §20.3 step 2 itself says: *"A violation the
open establishes bars the commits its outcome bars and no others:
reject-file bars every commit."* So it cannot append anything, touch any
other layer, or do a drop — the file is simply unusable to it as a
writer, exactly as it would be to a plain reader.
A **rewriter** faces the identical bar but stated as its own rule:
`[R-WRT-06]`: *"A rewriter MUST refuse to rewrite a file carrying any
record whose type it does not implement with MU = 1: such a type can
define references this specification does not (§7.2), so its bytes
cannot be safely relocated."* — restated in §20.4's table: *"At either
scope a rewriter MUST refuse to rewrite the file, on `[R-WRT-06]`'s own
ground."* Both tiers converge on total refusal; no disagreement between
the two statements (§20.4's table cites `[R-CNT-15]` for the appender and
`[R-WRT-06]` for the rewriter, consistently).

### W4 — Unimplemented top-level type, MU = 0, PE = 0 — drop with no other effect?

**Answer:** Yes, an appender **MAY** drop it in a commit whose only effect
is the drop, and so **MAY** a rewriter, in any rewrite. §20.4's table,
last row (MU = 0, PE = 0): *"Retain byte-identical, or drop it — its
extent becoming slack. The licence is the bit's own... an appender MAY
drop the record in any commit it is otherwise free to make — one whose
only effect is the drop included — and a rewriter MAY drop it in any
rewrite."* Neither is **required** to report the loss: *"An updater that
drops such a record **SHOULD** report the loss; unreported, application
state disappears with no diagnostic."* The keyword is **SHOULD**, not
MUST — this is advisory, not a conformance condition (confirmed by
Appendix H's checklist, which lists it separately under "Advisory, and
not a conformance condition").

### W5 — Input trailer has ignore-lane bit 20 set; three writer tiers' output flags

**Answer:**
- **(a) Appender's commit:** output flags = **input flags, unchanged**
  (bit 20 still set, no other bit set). `[R-CNT-08]`: *"An updater MUST
  copy forward unknown ignore-lane bits of its input file, MUST NOT clear
  them, and MUST NOT set any other."*
- **(b) Rewrite:** output flags = **input flags, unchanged** — same
  value as (a). `[R-WRT-06]`: *"The output trailer MUST copy the input's
  unknown ignore-lane flag bits forward and set no other, in place of the
  flags = 0 §6.3 requires of a file created under this text."*
- **(c) A creator that read the input and writes a new file from what it
  decoded:** output flags = **0** (bit 20 cleared). §20.1: *"As a creator
  it undertakes nothing toward its input, whatever it read: §20.2 binds
  it, it writes flags = 0, and it answers for every byte of its output
  (`[R-CNF-05]`), bytes it copied from another file included."* This
  scenario is the document's own phrase ("a creator that read the input
  and writes a new file from what it decoded" is lifted almost verbatim
  from §20.1's own description) — the *position* a tool occupies (creator
  vs. rewriter) is a declared choice (*"the choice is its own"*), not a
  function of what it actually did with the bytes; see my OBSERVATION
  finding writera-02 below.
No disagreement among (a)/(b)/(c)'s governing sentences — they describe
three genuinely different, explicitly named writer positions, each with
its own explicit rule, not three readings of one rule.

### W6 — Supersede a stored tile's own layer, changing only its fill value

**Answer:** **Not permitted as a commit.** Fill is one of the "fixed
declarations" for as long as the layer stores a tile: §20.3 step 4: *"Every
other declaration is fixed for as long as the layer stores a tile: the
layout, the linearization and the index encoding, the codec and the
filter, the rank and the dimension order, every tile extent, **every
channel's type and fill**... A commit MUST NOT change one of these; the
change is a new layer, or a rewrite that re-declares it under a fresh
file_id."* **Operations the document offers instead:** (i) drop the layer
(§20.4-licensed, since layer records are PE = 0) and add a new layer under
the same name with the new fill — "the new layer being new whatever bytes
its entries address, the dropped layer's former extents included"; or
(ii) a whole-file rewrite that **re-declares** the layer (§20.5's
"re-declaring" rewrite kind, exactly the case "§20.3 step 4 reserves for a
change to a fixed declaration").
**Is the resulting file nonconforming?** Not *by virtue of* this bar
alone — it is explicitly a **conduct** rule, parallel to `[R-CNF-02]`'s
conduct rules: *"This bar binds the commit as an actor: no file is
nonconforming by virtue of its violation, and no register row records the
violation itself, the register enumerating file-conformance violations
(§21.1) and the bar stating no condition a file can exhibit (§21.7,
`[R-ERR-01]`, `[R-CNF-02]`); a file such a commit leaves can be
nonconforming on its own terms, as the paragraph below sets out."* The
live file (one generation, as a pure byte-sequence predicate) carries no
trace of "what the fill used to be" — the superseded generation's
directory is not part of the live committed state (`[R-LIF-08]`) — so
this particular violation is, by the document's own §21.7 test,
structurally unwitnessed from the resulting bytes alone. (The file *can*
still be independently nonconforming for unrelated, ordinary reasons —
nothing here immunizes it generally.)

### W7 — Crash after directory durable, before trailer durable

**Answer:** This is my walk's Point 3 (§A.4). What the next reader sees:
on the default open, it fetches the **final 64 bytes of the now-longer
physical file** — which is *not* trailₙ (that sits further back, now
mid-file) but whatever bytes the interrupted step 5 did or did not manage
to lay down (partial/garbage trailer bytes, or nothing at that position
at all if the physical length only grew as far as the pad). These almost
certainly fail `[R-CNT-06]`'s magic or CRC gate. *"A reader that finds no
valid trailer in the final 64 bytes MUST report the file torn or invalid
and MUST NOT scan backward"* (`[R-LIF-05]`); *"the physical tail is not a
trailer, so a reader on the default path reports the file torn and MUST
NOT scan backward... What makes that recoverable rather than fatal is
that trailₙ and everything it reaches are still byte-intact"* (§9.2
Example). **Is the file conforming?** As the physical byte sequence
currently stands, **no** — its final 64 bytes do not satisfy
`[R-CNT-06]`'s trailer gates, so by the pure bytes predicate this is not a
conforming file (it is, however, one generation — the one ending at
trailₙ — away from a conforming prefix that remains fully intact and
checksum-verifiable). **What the next appender does:** per §9.4
(`[R-LIF-04]`), its attempt to validate the trailer at the physical end
fails, so *"the writer MUST NOT append"*; it must invoke §9.6's
deliberate recovery scan (probe backward for the trailer magic; require
the candidate's CRC to verify and `committed_file_length = o + 64`;
re-verify the surviving candidate as a whole file before trusting it), and
then either truncate the physical file to that recovered F before
resuming, or overwrite from F and truncate by its own step 6
(`[R-LIF-04]`) — only after which can it begin a fresh commit anchored at
the recovered F (= trailₙ's committed_file_length).

### W8 — Rewriter carries forward a layer with an unimplemented sample type

**Answer:** The rewriter's duty over what it carries forward is purely
**structural**, never a decode: `[R-WRT-09]`: *"A rewriter's verification
depth over what it carries follows reliance... it relies structurally on
every structure it copies, so it MUST verify each link of the chain — the
open (§19.1), each retained layer's record (§19.3) and full index chain
(`[R-IDX-04]`), and the checksum §8.1 states over each extent it copies,
every stored tile's entry crc among them — before emitting that
structure's bytes."* And explicitly: *"its verification depth over what
it carries is `[R-WRT-09]`'s and reaches no decoded content"* (§20.5). So
for each stored tile it copies verbatim it must verify: the layer
record's full §19.3 validation, the crc_of_crc_array over the fetched
segment-CRC array, the segment CRC over the segment containing that
tile's entry, and the tile's own **entry crc** over its stored bytes
(§8.2's chain) — **never** a decode, since it neither can (unimplemented
type) nor is obliged to for carried-forward content.
**When a checksum fails** (the tile's stored bytes fail the entry crc,
T1): this is a violation the rewriter has now **detected**, and §20.5's
central rule bars it from shipping it: *"A rewriter MUST refuse to
rewrite when any check `[R-WRT-09]` obliges fails, and MUST NOT emit a
file carrying a violation it has detected: it can neither re-emit the
structure corrected (`[R-WRT-05]`), nor keep it and call the output
clean. Dropping is the one disposal that answers, and only where §20.4's
table licenses it."* §20.4's table licenses dropping the whole **layer**
(its own record is PE = 0 per the registry: *"the layer record carries
PE = 0 and is dropped under the table's last row"*) — not the single
corrupt tile in isolation, since the preservation table operates at
record (not tile) granularity. So the rewriter's two disposals are: drop
the entire layer (reporting the loss, SHOULD), or refuse to rewrite the
file outright. **May it instead re-create the layer?** No — re-creating a
layer means decoding it as a reader first and re-emitting it as a creator
(§20.2, §19.3/§19.4): *"What it re-creates it decodes as a reader
(`[R-CNF-11]`) and writes as a creator (§20.2)."* Since it does not
implement the sample type, it cannot decode the layer, so re-creation is
not available to it here — only carry-forward-verbatim (blocked by the
detected checksum failure) or drop.

### W9 — Drop a layer (PE = 0) that carries an MU = 1 unimplemented sub-record

**Answer: No, the commit may not drop the layer.** Every sentence
bearing on this act:
- §20.4's table, MU = 1 row: *"Retain byte-identical. The updater MUST
  NOT modify the scope the record governs. At layer scope an unknown
  critical record blocks modification of that layer, its drop included,
  leaving other layers editable (`[R-CNT-18]`)."*
- §20.4, the paragraph directly addressing layer drops: *"A commit MAY
  therefore drop a layer record, and the drop takes the layer whole: a
  sub-record's flags govern it within a layer the updater keeps, so a
  dropped layer's sub-records and their extents go with it whatever their
  PE bits. **One sub-record blocks the drop, a sub-record of a type the
  updater does not implement with MU = 1**, the drop being a modification
  of the scope it governs (the table's first row)."*
These two passages **agree exactly** — the second is explicitly derived
from the first ("the table's first row"). The general rule ("a commit MAY
drop a layer record... sub-records... go with it whatever their PE bits")
is explicitly and consistently qualified by the MU = 1 exception in the
very same paragraph; there is no tension, let alone a contradiction,
between them. (The layer record's own PE = 0 would, alone, license the
drop — §20.4's table, last row, "the layer record carries PE = 0" — but
the blocking sub-record overrides that specifically, per both quotations
above.)

### W10 — Appender drops a carried-forward MU = 0/PE = 0 top-level record it doesn't implement

**Answer: Yes, it may, in a commit whose only effect is the drop — and the
append procedure and the preservation section agree completely.**
- §20.3 step 2 (the append procedure): *"Against any other structure the
  appender carries forward, it MUST NOT repair the defect...and **MUST
  NOT drop the record save where §20.4 licenses the drop**."*
- §20.4's table, last row (MU = 0, PE = 0): *"Retain byte-identical, or
  drop it — its extent becoming slack. The licence is the bit's own...
  **an appender MAY drop the record in any commit it is otherwise free to
  make — one whose only effect is the drop included**."*
These are not two independent rules that happen to coincide — the first
explicitly defers to the second ("save where §20.4 licenses the drop"),
and the second explicitly answers exactly the "only effect is the drop"
case the probe poses. No disagreement.

### W11 — Updater implements an unregistered type from a definition fixing MU = 1, PE = 0

**Answer.** The deciding sentence, verbatim, from §20.4 (just before the
preservation table): *"Its MU = 1 row reaches **only a type the updater
does not implement** — an updater implements both registered types and
understands an unregistered type it implements from its definition,
modifying their records as §20.3 and that definition provide — **so for
an implemented type only the PE bit bites**."* Because this type is
implemented, the table's MU = 1 row (retain-only, modification blocked)
simply does not reach it, regardless of what MU value the external
definition assigns; governance reduces to the PE bit alone. The
definition fixes PE = 0, so the governing row for an **unmodified**
instance of such a record is the table's **last row** (MU = 0, PE = 0, in
effect): *"Retain byte-identical, or drop it — its extent becoming
slack... an appender MAY drop the record in any commit it is otherwise
free to make... and a rewriter MAY drop it in any rewrite... An updater
that drops such a record SHOULD report the loss."* So: the updater **MAY
drop** such a record even though its definition's own MU bit says 1 —
because, per the deciding sentence above, the MU bit only "bites" for
types the updater does *not* implement. (Separately, this type's own
instance flags, as literally stored in the 24-byte record header
per §7.2, remain subject to `[R-CNT-12]`'s universal combination rule for
the file-conformance predicate itself — a stored MU=1/PE=0 combination is
still something *"writers MUST NOT emit"* and is a verifier-detected
nonconformance on its own terms — but that is orthogonal to what
*governs the updater's persistence obligation*, which the quoted sentence
routes entirely through the external definition's fixed values, not the
stored instance bits: "the definition it implements the type from
supplies the flags, and the stored bits never do.")

---

## Findings

Two OBSERVATIONs, both about explicitly-licensed degrees of freedom that
bear directly on byte-level output (not defects — the document is
internally consistent on every point I probed, including the two
"do these disagree" probes W9/W10, which I found to agree exactly).

**writera-01** (OBSERVATION): The exact relative order/placement of a
layer's new stored-tile payload versus its new tile-index region, and —
in a multi-layer commit — the interleaving of different layers'
appended structures, is left entirely to the writer (`[R-SLB-05]`'s
placement freedom), constrained only by the high-level step order
(payloads+indexes, then directory, then pad+trailer). This means Probe
W2's answer is complete as to which regions appear and their sizes, but
the *exact byte offsets* of each region (and therefore the exact
pre-trailer pad length) are not determined by the document for this or
any other append — two conforming appenders doing the identical logical
edit will legitimately diverge in exact offsets. This is intentional
(ties into the Part A.5 divergence catalogue), not a gap, but it is the
reason I could not give W2 a single fixed offset table the way I could
for W1.

**writera-02** (OBSERVATION): Whether a tool that reads an existing file
and produces a new one is a "creator" (flags=0, no preservation duty,
answers for every byte including copied ones) or a "rewriter" (must
preserve per §20.4/§20.5, carries ignore-lane bits forward) is stated as
a **declared choice** of the tool itself — "the choice is its own" (§20.1)
— rather than a function of how much of the input it actually reproduces.
Probe W5(c) depends entirely on this: the same tool, doing what might
look externally identical to a compaction rewrite, gets flags=0 (cleared
ignore-lane bit) if it self-identifies as a creator and the full
preserve-or-refuse discipline of §20.4/§20.5 if it self-identifies as a
rewriter. This is explicit and intentional in the text, not a gap I am
flagging as wrong — but it is worth recording because it means
"ignore-lane bit 20 survives" is not a fact about *what the tool did*
(read input, wrote output) but about *which position it declared*, and an
implementer could get W5 "wrong" relative to another implementer simply
by labelling the same code path differently.

No CONTRADICTION or AMBIGUITY findings survived scrutiny for the 11
probes or the byte-layout walk items the charter asked for; everywhere I
expected tension (W6's conduct-vs-bytes split, W9's drop-blocking,
W10's append-vs-preservation cross-reference, W11's MU/PE routing for
implemented-unregistered types) the document resolves it with an explicit
sentence, which I have quoted above rather than asserting from memory.
