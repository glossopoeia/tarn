# Writer/updater fidelity walk — edition A — writer-a

## Disclosure

- Directory `/private/tmp/claude-501/-Users-robertkleffner-Documents-GitHub-tarn-first-draft/fidelity-2/scratch/walk-writer-a/` was created empty by me (`mkdir -p`); it held no prior files when I began.
- I read exactly one file: `/Users/robertkleffner/Documents/GitHub/tarn-first-draft/scratch/cleanroom/editions/a/tarn.md` (4,981 lines, 302,380 bytes), confirmed present at exactly that path. I read it via the `Read` tool in sequential chunks (offsets 1, 700, 1400, 2100, 2907, 3207, 3486, 3755, and 4529) covering: the full front matter and §§1–4 (conventions, conformance vocabulary), §§5–10 (container: file anatomy, front block/trailer, directory/records, integrity, lifecycle/commit protocol/recovery, extension points), §§11–18 (array model: geometry, sample types, fill, serialization, tile index, slabs, codecs/filters, user metadata — skimmed for cross-references only, not separately walked since the charter is container/updater-focused), §§19–21 in full (reading algorithm, writing/updating — §20.1–20.5 in full, the error-handling register §21.1–21.9), and Appendix A (the annotated minimal 128-byte file) and the start of Appendix C (registry snapshot). I did not read Appendices D–H, §22 (security), or §23 (privacy) in this pass; nothing in the charter or probes turned on them.
- I ran one `grep` (actually a `Bash`/`Read`-tool navigational pass, not a content grep) to list all `### `/`#### ` section headers, purely to build a line-number map for navigation; this searched only the single permitted file and matched no prose content, so the hard-wrap warning about line-oriented searches missing wrapped phrases does not apply to it. I ran no other `grep`/`rg` against the document's prose.
- I ran no Python/arithmetic scripts (the probes' arithmetic — index region sizes, entry counts, byte offsets — is small enough to check by hand against the document's own worked examples, and I quote the document's own arithmetic rather than recomputing independently where it is given).
- **Context I did not ask for, and disregarded as evidence about the specification:** before this task began, my context already contained a `CLAUDE.md` project-instructions file (pointing to an `AGENTS.md`), a user memory file with an index of prior-round notes (filenames suggesting things like a "harness spec path," a "lost word list," "repair prose vs rules," etc.), a git-status block naming five recent commit subjects on a branch called `readable`, and various environment/tool-listing boilerplate. None of that is part of the specification and none of it is evidence about the specification's content; I have not treated any of it as such, and I am not repeating its contents beyond this notice. I did not open `AGENTS.md`, any ADR, `PLAN.md`, `OPEN-QUESTIONS.md`, `spec/registry.json`, `conformance/`, or any other copy of the specification, and I did not run `git log`/`git diff`/web search/web fetch.
- **Path check:** the file handed to me was at exactly the path the brief named, no substitution or redirection observed.

## The walk

### W1 — smallest conforming file

§5.1's own worked example and Appendix A's byte-exact worked example agree: the smallest conforming file is exactly 128 bytes.

Regions:
- `[0, 16)` — front signature block: `[0,8)` = `89 54 41 52 4E 0D 0A 1A`; `[8,16)` = zero. (§6.1, R-CNT-04 governs residency of the check, not the content.)
- `[16, 20)` — directory region: dir_length = 4, a zero-record sequence (0 bytes) followed by its CRC-32C, which is `0x00000000` for zero bytes per the checksum's own check-vector rule (§4.5: "The CRC-32C of zero bytes is `0x00000000`.").
- `[20, 64)` — pre-trailer pad / slack, 44 bytes, zeroed by advice (R-CNT-03), not required to be zero.
- `[64, 128)` — the 64-byte trailer (§6.2 layout, offsets below relative to trailer start, i.e. + 64 in absolute file offset):
  - `[64,72)` trailer magic = `8A 4E 52 41 54 0D 0A 1A`
  - `[72,74)` version_major = `01 00` (1)
  - `[74,76)` version_minor = `00 00` (0 — R-CNT-26: writers SHOULD emit the lowest minor defining every feature present; for a file expressible under this text, 0)
  - `[76,80)` flags = `00 00 00 00` (a creator MUST write flags = 0, §6.3)
  - `[80,88)` dir_offset = `10 00 00 00 00 00 00 00` (16)
  - `[88,96)` dir_length = `04 00 00 00 00 00 00 00` (4)
  - `[96,104)` committed_file_length = `80 00 00 00 00 00 00 00` (128 = F)
  - `[104,112)` file_id — **not a fixed value**: any nonzero u64; Appendix A's own worked example uses `EF CD AB 89 67 45 23 01` (0x0123456789ABCDEF) purely as an illustration and says explicitly "any nonzero value; a real writer draws it randomly, §9.3."
  - `[112,124)` reserved, 12 bytes, zero
  - `[124,128)` trailer CRC-32C over trailer bytes `[0,60)` (i.e. absolute `[64,124)`) — a function of file_id, so not a fixed value either; Appendix A's worked example computes `0x402F157E` for its chosen file_id.

So every trailer field's value is fixed by the document **except** file_id (writer's free, SHOULD-random choice, R-CNT-06 requires only ≠ 0) and the trailer CRC (deterministic function of the other 60 bytes, hence of file_id). This is not a document gap — §9.3 states the freedom expressly — but it means "the value of every trailer field" has exactly one degree of freedom by design, worth flagging in probe_answers as intentional underdetermination rather than a defect.

The file contains no layers (§21.6: "The file contains zero layers" is a listed non-violation, R-CNT-14/R-CNT-02).

### W2 — appending one superseded tile, 32-tile interleaved layer, 100,000-byte payload

This is the document's own worked example, verbatim (§20.3, the paragraph right after `[R-WRT-04]`):

> "Superseding one 100,000-byte stored tile of a 32-tile interleaved layer appends: the new payload (100,000 bytes), the layer's full new index region (32 · 20 + 4 = 644 bytes — one entry re-pointed, 31 byte-identical), the new directory (every record byte-identical except the modified layer's), the pad, and the 64-byte trailer. The prior index region and the superseded payload become slack, reclaimable only by a rewrite (§20.5)."

Cross-checking the index-region arithmetic against §7.4's general formula for index_encoding 1 (R-CNT-17): extent_length = entry_count × 20 + ⌈entry_count / 2¹⁶⌉ × 4. With entry_count = 32 (interleaved, N = 32, addressed-tile count = N): 32×20 = 640, ⌈32/65536⌉ = 1, +4 = 644. Matches.

Ordered list of regions the commit appends (per `[R-LIF-02]`/`[R-WRT-04]`'s fixed step order — payloads+indexes, then directory+CRC, then barrier, then pad+trailer, then barrier):
1. The new tile payload extent, 100,000 bytes (step 2/4).
2. The layer's full new tile-index region, 644 bytes (32 entries × 20 + one 4-byte segment CRC) — one entry re-pointed to the new payload's offset/length/crc, the other 31 entries byte-identical to their prior values at the same disk ordinals (step 4, R-WRT-04: "every other entry byte-identical at its disk-ordinal position").
3. The new complete directory + its CRC-32C — every record byte-identical except the modified layer's record (whose extent slot now points at the new 644-byte index region) (step 5, §20.4).
4. The pre-trailer pad to the next 64-byte boundary (step 6/`[R-LIF-02]` step 5).
5. The new 64-byte trailer, same file_id, committed_file_length = new F (step 6).

Prior bytes that become slack: the superseded tile's old stored payload (whatever its size was) and the layer's *entire* prior 644-byte index region (not just the one changed entry — the whole region is superseded because a layer's index is addressed by one extent slot and any change to the stored-tile set or index content re-emits the whole region at a new placement, R-WRT-04). The old directory, its pad, and its trailer from the commit being superseded also become slack (§5.1's three-commit example shows this as the general shape).

### W3 — appender's input carries an unimplemented top-level record, MU = 1

§20.4's preservation table, MU = 1 row, and its own cross-reference to R-CNT-15/§2.3:

> "At file scope no commit is available at all: the updater is a reader of the file first (§2.3), and `[R-CNT-15]` makes an unimplemented top-level MU = 1 record reject-file — the same treatment §6.3 gives an unknown incompat-lane bit."

So an appender facing such a record MUST reject the file outright — it may not commit at all, whatever the commit's target layer or scope, because R-CNT-15 makes the whole file unusable to any reader (which the appender is, first, per R-CNF-11/§2.3).

For a rewriter, the same MU = 1 row states, for either scope (file or layer):

> "At either scope a rewriter MUST refuse to rewrite the file, on `[R-WRT-06]`'s own ground: such a type can define references this specification does not (§7.2), so its bytes cannot be safely relocated."

§20.5 confirms independently: "A rewriter MUST refuse to rewrite a file carrying any record whose type it does not implement with MU = 1" (`[R-WRT-06]`).

Both actors: refuse entirely. Neither may drop the unknown record and proceed (the MU=1 row's own text: "the updater MUST NOT modify the scope the record governs" — and at file scope, "the scope the record governs" is the whole file, so no commit or rewrite is available).

### W4 — unimplemented top-level record, MU = 0, PE = 0

§20.4's table, third row:

> "MU = 0, PE = 0 | Retain byte-identical, or drop it — its extent becoming slack. The licence is the bit's own: whoever fixed PE = 0 for the record, the writer that stored it or the definition that governs it, declined preservation across edits, so an appender MAY drop the record in any commit it is otherwise free to make — one whose only effect is the drop included — and a rewriter MAY drop it in any rewrite. An updater that drops such a record SHOULD report the loss; unreported, application state disappears with no diagnostic."

- May an appender drop it in a commit whose only effect is the drop? **Yes** — explicitly licensed ("one whose only effect is the drop included").
- May a rewriter drop it? **Yes** — "in any rewrite."
- Must either report the loss? **No — SHOULD, not MUST.** The keyword is **SHOULD** (both here and in §20.4's separate statement about dropping a layer: "an updater that drops a layer SHOULD report the loss, as the table says of any record dropped").

### W5 — ignore-lane bit 20 set in the input trailer

Governing rule R-CNT-08 (§6.3): "An updater MUST copy forward unknown ignore-lane bits of its input file, MUST NOT clear them, and MUST NOT set any other... A rewriter, though its output is a new file, carries the input's unknown ignore-lane bits into its output trailer rather than writing flags = 0, and sets no other." §20.5 restates this for rewriters verbatim: "The output trailer MUST copy the input's unknown ignore-lane flag bits forward and set no other, in place of the flags = 0 §6.3 requires of a file created under this text."

- (a) Appender's commit: flags value is **unchanged from the input** — bit 20 remains set, no incompat-lane bit is touched (the appender would have rejected the file at open if one were set and unimplemented), and no other ignore-lane bit is set by this text (which defines none).
- (b) A rewrite: **same as (a)** — bit 20 copied forward, no other bit set (§20.5, quoted above).
- (c) A creator that read the input and writes a new file from what it decoded: this is the third position §20.1 names — "As a **creator** it undertakes nothing toward its input, whatever it read: §20.2 binds it, it writes flags = 0." §6.3: "a writer creating a file under this text MUST write flags = 0." So **flags = 0** — bit 20 is *not* carried over, because a plain creator (as opposed to an appender or a rewriter) owes the input nothing and this text defines no semantics for that bit to reproduce. This is a meaningful three-way divergence worth flagging: the same starting bit survives identically under (a) and (b) but is silently dropped under (c), and the document's own taxonomy (§20.1) is explicit that reading an existing file does not make a tool an updater — only extending it (appender) or undertaking §20.4/§20.5's preservation duties (rewriter) does.

### W6 — commit changes only a stored layer's fill value

§20.3 step 4's fixed-declarations list is explicit that a channel's fill is one of the "Every other declaration ... fixed for as long as the layer stores a tile," naming "every channel's type and fill" among them, and: "A commit MUST NOT change one of these; the change is a new layer, or a rewrite that re-declares it under a fresh file_id (`[R-LIF-01]`, §20.5)."

So: **not permitted** as an appender operation. The document offers exactly two operations instead: (1) create a **new layer** (under a different name, or the same name after this commit or a later one drops the old layer, §20.3 step 4 / §19.1) carrying the desired fill from the start; or (2) a **rewrite that re-declares the layer** under a fresh file_id — this is one of the three named rewrite operations in §20.5 ("re-declaring a layer that stores a tile in the input, the rewrite §20.3 step 4 reserves for a change to a fixed declaration").

Whether the file such an (impermissible) appender commit would leave is nonconforming: the bar is stated as binding "the commit as an actor" — "no file is nonconforming by virtue of its violation... a file such a commit leaves can be nonconforming **on its own terms**" (§20.3 step 4, citing R-ERR-01/R-CNF-02's conduct-rule model). The very next paragraph supplies the "own terms" test: whether a fill change is *witnessed* turns on whether the layer's tiles have padding. Padding-position content is fixed to the channel's fill by `[R-SER-05]` (§14.5), and a verifier checks it (T4, §21.4: "A padding position does not encode, for each channel it carries, that channel's recorded fill value"). §20.3 step 4 names T4 explicitly among the register rows a changed fixed-declaration *can* trigger ("but for a stored tile's decoded size, a padding position or pad bit, or a boolean byte the register witnesses (T3, T14, T21, T22, T4, T5, T2)... no check any actor owes able to see it"). So:
- If the layer has any tile with padding positions (i.e., some dimension's extent is not a multiple of its tile extent), the previously-stored tile's padding bytes still encode the *old* fill, which now mismatches the newly declared fill — a **T4 violation, reject-tile, detected by a verifier at certification** — making the resulting file nonconforming.
- If the layer has no padding at all (every extent evenly divides its tile extent), a fill-only change is unwitnessed by any check this specification obliges (§21.7's test), and the resulting file is not made nonconforming by it — only future unstored tiles would read differently, harmlessly.

### W7 — crash after directory durable, before trailer durable

This is exactly the scenario §9.2's own worked example depicts ("Example — what a crash sees," row 2, "mid-commit"):

> "mid-commit │ … │ dirₙ │pad│ trailₙ │▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓ ↑ trailₙ intact, but no longer at the file's end"

i.e. the *old* generation's directory/pad/trailer (dirₙ/pad/trailₙ) remain byte-intact, and the new commit's payloads/index/new-directory (the ▓ region) were appended and made durable (step 4's barrier), but the new pad+trailer (step 5) never became durable — so at the crash instant it is unknown, and immaterial, whether any prefix of the new pad+trailer bytes physically landed on disk; what matters is what the *next reader* finds at the physical end of file.

**What the next reader sees:** on the default read path (trailer-at-end-or-fail), the reader fetches the final 64 physical bytes and validates them per §6.2. Because trailₙ is "no longer at the file's end," those final 64 bytes are either garbage (if nothing of the new trailer landed) or an incomplete/torn new trailer (if some but not all of it landed) — in either case they fail one of the trailer's ordered gates (magic F8, CRC F14, or the length cross-check F17). Per R-LIF-05: "a reader that finds no valid trailer in the final 64 bytes MUST report the file torn or invalid and MUST NOT scan backward." So the reader reports the file torn/invalid and stops; it does not fall back to trailₙ on its own.

**Is the file conforming?** As a raw byte sequence at its current physical length, **no** — it fails `[R-CNT-06]`'s trailer gates at file scope, so the whole physical byte string is not a conforming file. But the *committed prefix* ending at the old F (front block through trailₙ) is fully intact and immutable (`[R-LIF-01]`) and is itself a conforming file once truncated to it — this is precisely "the window ... in which the old state is *recoverable*" that §9.2's example note describes.

**What the next appender does:** per R-LIF-04/§9.4, it must first establish F by validating the trailer at the *physical* end; that fails, so "the file is torn: the writer MUST NOT append, and locating the last committed state is the deliberate recovery operation of §9.6 — never an implicit step of opening for append." §9.6's probe scans backward at 64-aligned offsets for the trailer magic; it will find trailₙ as a candidate, verify its CRC and its committed_file_length = o + 64 — both hold since trailₙ is byte-intact — making it "the nearest-to-end candidate that survives whole-file re-verification," hence "the last committed state." The recovery tool truncates to that old F (or the appender, per R-LIF-04, truncates to F before its own step 1, or overwrites from F and truncates no later than its own step 6). The appender then proceeds with a fresh commit from that recovered F. §9.6 also obliges the tool to "report the candidate it settled on and how many candidates it rejected on [whole-file] re-verification."

### W8 — rewriter carrying forward a layer with an unimplemented sample type

Part I/Part II independence is stated explicitly (§3.3's Note): "appenders, and rewriters that carry a layer forward, operate on files whose layers they cannot decode." R-WRT-09 states the rewriter's verification depth precisely:

> "A rewriter's verification depth over what it carries follows reliance (`[R-WRT-03]`): it relies structurally on every structure it copies, so it MUST verify each link of the chain — the open (§19.1), each retained layer's record (§19.3) and full index chain (`[R-IDX-04]`), and the checksum §8.1 states over each extent it copies, every stored tile's entry crc among them — before emitting that structure's bytes."

So for each stored tile it copies it MUST verify: crc_of_crc_array over the fetched segment-CRC array, the segment CRC over the segment containing the entry, entry classification (R-IDX-03), and the entry's own crc field against the tile's stored bytes (R-CNT-20/§8.1) — **all structural**, never a decode of the sample content, which R-WRT-09 itself notes "reaches no decoded content."

**When a checksum fails:** this is a violation the rewriter has, by its own obligatory verification, detected. §20.5's general rule governs: "A rewriter MUST refuse to rewrite when any check `[R-WRT-09]` obliges fails, and MUST NOT emit a file carrying a violation it has detected: it can neither re-emit the structure corrected (`[R-WRT-05]`), nor keep it and call the output clean. Dropping is the one disposal that answers, and only where §20.4's table licenses it... Where the table does not license a drop the rewriter MUST refuse." The layer record's own registry-fixed flags are MU = 0, PE = 0 (§7.3: "0x0001 layer ... MU = 0, PE = 0"), so §20.4's last row licenses dropping the *whole layer* (there is no finer-grained "drop just this one tile" disposal in the document's three-way carry/re-create/drop framework — the only dispositions named for "each structure of the input" are carry-forward-verbatim, re-create, or drop, §20.5 opening paragraph). So on a checksum failure the rewriter's only two options are: **refuse the whole rewrite**, or **drop the entire layer** (SHOULD report the loss, §20.4).

**May it instead re-create the layer?** **No.** Re-creation is defined as: "A layer the rewrite re-creates is new output: its record, its tile-index region and its stored tiles are written under §20.2's rules from content the rewriter **decoded** (§19.3, §19.4)." Since the sample type is by hypothesis unimplemented, the rewriter cannot decode this layer's tiles at all — re-creation is exactly the operation Part I/Part II independence exists to make *unnecessary* for such a tool, and it is unavailable to it here.

### W9 — layer PE = 0, but carries an unimplemented MU = 1 sub-record

The layer record's own top-level flags are registry-fixed at MU = 0, PE = 0 (§7.3), which alone would license dropping the layer under §20.4's last table row. But §20.4 addresses exactly this compound case, in the paragraph immediately following the table:

> "A commit MAY therefore drop a layer record, and the drop takes the layer whole: a sub-record's flags govern it within a layer the updater keeps, so a dropped layer's sub-records and their extents go with it whatever their PE bits. **One sub-record blocks the drop, a sub-record of a type the updater does not implement with MU = 1, the drop being a modification of the scope it governs** (the table's first row)."

And the table's MU = 1 row itself: "Retain byte-identical. The updater MUST NOT modify the scope the record governs. At layer scope an unknown critical record blocks modification of that layer, its drop included, leaving other layers editable."

§7.2's Note states the same conclusion independently: "An updater that does not implement an MU = 1 record's type never drops the record, **alone or with the scope it governs** (§20.4)."

**All three sentences agree, with no disagreement found:** the commit **may not** drop the layer. The layer's own PE = 0 licenses dropping *it as a bare layer*, but that license is overridden the instant it carries an unimplemented MU = 1 sub-record, because dropping the layer would necessarily drop (modify away) that sub-record's governed scope, which the MU = 1 row forbids outright. Other layers remain editable/droppable normally ("leaving other layers editable").

### W10 — appender wants to drop a carried, unimplemented top-level record, MU = 0 / PE = 0

Two passages bear on this, one in the append procedure and one in the preservation section, and a third that ties them together by explicit cross-reference:

- §20.3 step 2 (Open): "Against any other structure the appender carries forward, it MUST NOT repair the defect... and **MUST NOT drop the record save where §20.4 licenses the drop**."
- §20.3 step 5: "**Re-emit the directory per §20.4**, followed by its CRC" — the append procedure does not restate a separate drop rule at step 5; it delegates to §20.4 wholesale.
- §20.4's table, MU = 0 / PE = 0 row (quoted in full at W4): licenses exactly this — "an appender MAY drop the record in any commit it is otherwise free to make — one whose only effect is the drop included."

**They agree; there is no tension.** §20.3's own text is written as an explicit pointer to §20.4 ("save where §20.4 licenses the drop" / "per §20.4"), not an independent rule that could diverge from it — the two sections state one rule, split across "when in the procedure" (§20.3) and "which records" (§20.4). Under PE = 0, the drop is licensed, so an appender MAY drop this record, in a commit whose only effect is the drop, and SHOULD report the loss (W4).

### W11 — updater implements an unregistered type whose (private) definition fixes MU = 1, PE = 0

§20.4's opening paragraphs distinguish three flag-authority regimes: (i) a type §7.3 registers — the registry's fixed flags govern, never the stored bits; (ii) a type the updater implements that is *not* registered — "the definition it implements the type from supplies the flags, and the stored bits never do"; (iii) a type the updater does not implement — the stored bits govern (with the MU=1-w/-PE=0-stored-as-PE=1 coercion of R-CNT-12).

The deciding sentence for which row of the three-row table governs an *implemented* (but unregistered) type is this one, immediately after the table:

> "The table states what an updater owes a record it does not logically modify, read under whichever flags govern it. **Its MU = 1 row reaches only a type the updater does not implement** — an updater implements both registered types and understands an unregistered type it implements from its definition, modifying their records as §20.3 and that definition provide — **so for an implemented type only the PE bit bites**."

For this record — implemented, definition-fixed PE = 0 — the MU = 1 row is stated to be *inapplicable regardless of the definition's MU value*, because the MU = 1 row is scoped to "a type the updater does not implement." Only the PE bit selects the governing row for an implemented type, and PE = 0 selects the table's third row (MU = 0, PE = 0 in the table's own labelling, though the *stored*/defined MU here is 1): "Retain byte-identical, or drop it." So: **the preservation table obliges only retain-or-drop treatment; the updater MAY drop this unmodified record** (in any commit/rewrite it is otherwise free to make, SHOULD report the loss), exactly as if it were an ordinary ancillary record — the definition's MU = 1 has no preservation consequence once the type is implemented.

This is a genuinely easy point to get backwards from a first read of the table alone (the table's own row labels read "MU = 1" as an unconditional "retain, never drop" case), and I flag it as an OBSERVATION below since another implementer answering only from the table's row labels, without this connecting sentence, could reasonably reach the opposite conclusion — the divergence is not in what the document says (it is unambiguous once this sentence is read) but in what a reader might miss.

## Findings

See structured findings; summarized here:

1. **writera-01 (OBSERVATION).** §20.4's connecting sentence ("so for an implemented type only the PE bit bites") is the sole textual link that resolves W11; a reader who stops at the three-row table (whose rows are captioned by MU/PE combinations) can easily conclude MU = 1 always means "never drop," which is wrong for a type the updater implements. Byte-level: this changes whether a conforming updater may emit a file with the record dropped versus must retain it — directly bears on which bytes a conforming appender/rewriter may emit.
2. **writera-02 (OBSERVATION).** W5's three-way divergence: an ignore-lane bit is preserved identically by an appender and by a rewriter, but is silently zeroed by a plain creator that happens to have read the same input and decoded its content — a consequence of §20.1's tier taxonomy (reading is not, by itself, updating) rather than any special rule for that bit. Byte-level: same starting trailer flags value, three different legitimate output values depending solely on which of the three writer tiers is producing the output, with no requirement that the tool disclose which tier it acted as.
3. **writera-03 (OBSERVATION).** W6's "nonconforming on its own terms" test is conditional on the layer's own geometry (whether it has any padding tiles) — an appender conduct-rule violation (changing fill on a layer that stored a tile) produces a file that is byte-level nonconforming (via T4) only in the padding case, and produces a file with no detectable defect in the no-padding case, even though the *conduct* violates R-WRT-04/§20.3 step 4 identically in both cases. Byte-level: whether a conforming verifier must reject the resulting file depends on the layer's tile-extent-vs-dimension-extent arithmetic, not on anything about the fill change itself.

No CONTRADICTION was found among the sentences cited for W9, W10, or W11 — in each case multiple passages were checked and found to state one consistent rule (via explicit cross-reference in W10's case, and via directly reinforcing sentences in W9's and W11's).
