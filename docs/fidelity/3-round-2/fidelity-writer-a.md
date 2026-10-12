# Writer/Updater fidelity walk — edition A — transcript

## Disclosure

- A harness-relayed "user request" appeared above this brief, consisting of the single word "Go". Per the brief's own instructions, this is the launcher's message to the orchestrator, carried out before I was spawned; it is not a task for me, needs no reconciliation, and does not widen the access rule. I disregarded it as a task instruction.
- My runtime context also contained, before I began: a CLAUDE.md pointer to an AGENTS.md file, a user auto-memory index (MEMORY.md) listing many TARN-process notes (harness spec paths, lineage gates, repair passes, subagent model pins, etc.), a git status/log block showing recent "Readable:" commits on a branch named `readable`, an attribution-footer instruction for commits/PRs, and a list of deferred tool names. None of this is part of the specification and none of it is evidence about the specification's content. I disregarded all of it as a source of fact about TARN; I am not repeating its contents here beyond this one clause, per instruction.
- The access rule said my scratch directory was at a `fidelity-4/scratch/walk-writer-a/` path; when I created it, it was empty — no prior attempt's files were present.
- I read exactly one file: `/Users/robertkleffner/Documents/GitHub/tarn-first-draft/scratch/cleanroom/editions/a/tarn.md` (4,981 lines). I did not list any other directory, did not open any other copy of the specification, did not consult git history, and did not browse the web. The path matches what the brief specified, so no path-mismatch disclosure is needed beyond confirming the match.
- I ran local commands only: `wc -l`, `grep -n` for the table of contents (section headers) and for targeted phrase sweeps (`PE = 0`, `PE=0`, `PRESERVE_ON_EDIT`) against that one file, `sed -n` to print line ranges of that one file in full (never truncated to a single line, so hard-wrap concerns did not bite — I was reading whole paragraphs, not grepping single lines for multi-line phrases), and a short local Python script (no file I/O other than writing its own script) that implements CRC-32C and checks it against the document's own check vectors and against Appendix A's worked trailer, as a computational cross-check (not a new source of facts).

## Working files in my scratch directory

- `/private/tmp/claude-501/-Users-robertkleffner-Documents-GitHub-tarn-first-draft/fidelity-4/scratch/walk-writer-a/crc32c.py` — local CRC-32C implementation and verification script (described below).
- `/private/tmp/claude-501/-Users-robertkleffner-Documents-GitHub-tarn-first-draft/fidelity-4/scratch/walk-writer-a/transcript.md` — this file (copied to the mandated output path).

## Table of contents swept

`grep -n '^#### \|^### \|^## '` against the one file gave the section map I navigated by: Parts 0/I/II/III, §1–§24, Appendices A–H. I read in full: §1–§10 (Preliminaries + Container: conformance classes, outcome classes, encoding, file anatomy, front block/trailer, directory/records, integrity, lifecycle/commit protocol, extension/registry), §15–§17 (tile index, slabs/alignment, codecs — scanned), §19 (reading, scanned for cross-reference), §20 in full (writer tiers, creation, append procedure, re-emission/preservation, rewriting), §21 in full (error register §21.1–§21.9), and Appendices A, B, C, G in full (minimal file, constants, registry snapshot, reproducible-writer profile). I did not read §11–§14, §18, §22–§24, Appendix D–F, H word-for-word; I confirmed via the TOC and targeted greps that the charter's subject matter (byte layout, append procedure, record flags, slack, torn-write recovery, writer byte-divergence) lives in the sections I did read in full, and cross-checked that nothing in §21's rows for those sections contradicted what I found.

## W1 — smallest conforming file

§5.1 (`[R-CNT-27]`): "No conforming file is shorter than 128 bytes: the front signature block, a directory of at least 4 bytes at an offset of at least 16, and the 64-byte trailer at a 64-aligned offset cannot be satisfied in fewer." §5.1's own example states the layout; I derived it independently from §6.1, §6.2, §7.1, §4.5 and cross-checked against Appendix A (non-normative) and a local CRC-32C computation.

Regions, [start, end):
- [0, 8): front signature magic `89 54 41 52 4E 0D 0A 1A` (§6.1).
- [8, 16): front signature reserved, zero (§6.1, structural).
- [16, 20): directory region, dir_length = 4: a record sequence of zero bytes (§7.1 — "zero or more records" permits zero, §9.1/§21.6 "The file contains zero layers" / "a directory carrying no layer record is a conforming generation ... an empty directory included") followed by its CRC-32C over those zero bytes, which §4.5's check vector gives as `0x00000000`.
- [20, 64): pre-trailer pad, 44 bytes — slack (§6.2 `[R-CNT-05]`, §5.2 `[R-CNT-21]`), zeroed by the advice of `[R-CNT-03]`, not required.
- [64, 128): the 64-byte trailer (§6.2), fields below.

Trailer field values (offsets relative to trailer start, i.e. file offset + 64):
- [0,8) trailer magic: `8A 4E 52 41 54 0D 0A 1A`.
- [8,10) version_major = 1 (`01 00`).
- [10,12) version_minor = 0 (`00 00`).
- [12,16) flags = 0 (`00 00 00 00`) — a creator writes flags = 0 (§6.3: "a writer creating a file under this text MUST write flags = 0").
- [16,24) dir_offset = 16 (`10 00 00 00 00 00 00 00`).
- [24,32) dir_length = 4 (`04 00 00 00 00 00 00 00`).
- [32,40) committed_file_length = 128 (`80 00 00 00 00 00 00 00`) = F, and F mod 64 = 0 (`[R-CNT-01]`, `[R-CNT-06]`).
- [40,48) file_id = any nonzero u64, writer's choice, SHOULD be drawn randomly (§9.3). Appendix A's worked value is `EF CD AB 89 67 45 23 01` (0x0123456789ABCDEF LE); any nonzero u64 is equally conforming.
- [48,60) reserved = 12 zero bytes (structural, must be zero — `[R-CNT-06]`).
- [60,64) trailer CRC = CRC-32C over trailer bytes [0,60).

I computed this CRC-32C independently (see `crc32c.py`): building the exact 60-byte trailer prefix with the values above (using Appendix A's file_id for a concrete instance) and running my own reflected-Castagnoli CRC-32C implementation, I got `0x402f157e`, i.e. stored bytes `7E 15 2F 40`. This matches Appendix A's stated value exactly, and the full assembled file is exactly 128 bytes. I also verified my CRC-32C implementation against §4.5's two check vectors before trusting it: CRC-32C("123456789") = `0xe3069283` (matches `[R-ENC-09]`'s stated value) and CRC-32C(zero bytes) = `0x00000000` (matches, and is the value used for the empty directory's CRC above). This is independent confirmation that the normative rules in §4.5, §5.1, §6.1, §6.2, §7.1 compose to exactly Appendix A's (non-normative) worked example — the appendix is consistent with, and does not add to, the normative text.

The file contains zero layers, which §21.6's table records as a conforming, valid, empty file ("A directory carrying no layer record is a conforming generation whether or not it carries other records, an empty directory included" — `[R-CNT-14]`, `[R-CNT-02]`).

## W2 — appending 100,000 bytes superseding one tile of a 32-tile interleaved layer

Directly on point, §20.3's worked example (verbatim): "Superseding one 100,000-byte stored tile of a 32-tile interleaved layer appends: the new payload (100,000 bytes), the layer's full new index region (32 · 20 + 4 = 644 bytes — one entry re-pointed, 31 byte-identical), the new directory (every record byte-identical except the modified layer's), the pad, and the 64-byte trailer. The prior index region and the superseded payload become slack, reclaimable only by a rewrite."

I derived the 644-byte figure independently from §15.1's entry layout (20 bytes/entry) and §15.4's segmentation (segments of 2^16 entries; 32 entries ≤ 65,536 so there is exactly one, partial, segment, contributing one 4-byte CRC): 32 × 20 = 640, + ⌈32/65536⌉ × 4 = 4, total 644 — matching `[R-CNT-17]`'s extent_length formula (entry_count × 20 + ⌈entry_count/2^16⌉ × 4) exactly, and matching the document's own arithmetic.

Regions the commit appends, **in order** (per `[R-LIF-02]` / `[R-WRT-04]`'s step ordering: payloads+indexes, then directory+CRC, then barrier, then pad+trailer, then barrier):
1. New stored-tile payload — 100,000 bytes (the new/superseding tile's bytes).
2. The layer's full new tile-index region — 644 bytes (entry array 32 × 20 = 640 bytes, one entry re-pointed to the new payload's offset/length/crc, 31 byte-identical to the superseded generation's entries at the same disk ordinals; + one 4-byte segment CRC recomputed over the 640-byte entry array as newly emitted). This whole region is re-emitted "necessarily at a new placement" even though only one entry's value changed (§20.3 step 4, `[R-WRT-04]`) — this is the §20.3 note's "a commit's cost is dominated by its index, not its data" point.
3. The new complete directory + its trailing CRC-32C — every record byte-identical except the modified layer's record (whose extent slot now points at the new 644-byte index region, and whose crc_of_crc_array is recomputed over the new segment-CRC array) (§20.4 `[R-WRT-05]`, §7.1 `[R-CNT-11]`).
4. [barrier — makes 1–3 durable, `[R-LIF-02]` step 4; conduct, no bytes]
5. The pre-trailer pad, 0–63 bytes to the next 64-byte boundary (§6.2, `[R-CNT-03]` advice to zero it; size depends on where step 3 ends, not determinable from the probe's given facts).
6. The new 64-byte trailer, committed_file_length = new end (at least 128 bytes above the prior F, per `[R-LIF-02]`'s strict-increase note), unknown ignore-lane bits carried forward, same file_id (`[R-CNT-08]`, `[R-WRT-04]`).
7. [barrier — makes the trailer durable, `[R-LIF-02]` step 6; conduct, no bytes]

Prior bytes that become slack (§5.2, `[R-CNT-21]`):
- The superseded tile's old stored-payload bytes (whatever size the old tile was — not given by the probe, and in general different from 100,000).
- The entire prior tile-index region for this layer (not just the one changed entry's 20 bytes — the whole region moves because it is addressed by one extent slot, so "a single changed entry costs its whole length", per §20.3's own commentary on this exact example).
- The entire prior directory, pre-trailer pad, and prior 64-byte trailer (every commit re-emits a fresh directory/pad/trailer, which supersedes the previous one in full — this is the figure's shape (b): "│front│ tiles │▓index▓│▓▓▓▓▓▓▓▓▓▓▓▓▓│ +tiles │ index′ │ dir₂│pad│tr₂│", where the long ▓ run is "old dir…tr" in full).

No other prior bytes (other tiles/layers untouched) become slack, since placement of untouched structures is undisturbed (`[R-WRT-05]`: "a layer the commit leaves untouched" keeps its extent slot "pointing at the existing region").

## W3 — appender's input carries a top-level record of a type it does not implement with MU = 1

§7.2's record framing + `[R-CNT-15]`: "An unknown record type at file scope: MU = 1 → reject-file." The append procedure's step 2 ("Open") says: "Perform §19.1's open ... A violation the open establishes bars the commits its outcome bars and no others: reject-file bars every commit." §20.4's preservation table, MU = 1 row, states the same scenario in terms directly: "At file scope no commit is available at all: the updater is a reader of the file first (§2.3), and `[R-CNT-15]` makes an unimplemented top-level MU = 1 record reject-file — the same treatment §6.3 gives an unknown incompat-lane bit."

**What the appender may do to the file:** nothing. The file is reject-file at open; no commit of any kind is available — the appender cannot append anything at all, to any layer, because the violation it has met on open bars every commit (not merely a commit touching the offending record's scope — file scope is the whole file).

**What a rewriter may do:** also nothing — it must refuse outright. §20.4's same MU = 1 row, continuing: "At either scope a rewriter MUST refuse to rewrite the file, on `[R-WRT-06]`'s own ground." `[R-WRT-06]` itself: "A rewriter MUST refuse to rewrite a file carrying any record whose type it does not implement with MU = 1: such a type can define references this specification does not (§7.2), so its bytes cannot be safely relocated." So a rewriter facing exactly this input must produce no output file at all.

I checked for disagreement between the "append procedure" framing (step 2, open) and the "preservation" framing (§20.4's table) — they state the identical outcome (reject-file; no commit) via two routes (§7.2/`[R-CNT-15]`'s general rule, and §20.4's table restating it for the updater's specific position), and cross-cite each other ("the same treatment §6.3 gives"). No disagreement found.

## W4 — top-level record, unimplemented type, MU = 0, PE = 0

§20.4's preservation table, MU = 0 / PE = 0 row (verbatim): "Retain byte-identical, or drop it — its extent becoming slack. The licence is the bit's own: whoever fixed PE = 0 for the record, the writer that stored it or the definition that governs it, declined preservation across edits, so an appender MAY drop the record in any commit it is otherwise free to make — **one whose only effect is the drop included** — and a rewriter MAY drop it in any rewrite. An updater that drops such a record SHOULD report the loss; unreported, application state disappears with no diagnostic."

**Appender:** Yes — explicitly "one whose only effect is the drop included." The document anticipates exactly the probe's scenario (a commit whose sole content is dropping the record) and licenses it.

**Rewriter:** Yes — "a rewriter MAY drop it in any rewrite" (and the drop is also one of the three named rewrite shapes in §20.5: "dropping a layer or another record §20.4's table licenses dropping").

**Reporting:** Neither is obliged (MUST) to report; both SHOULD report the loss (keyword: **SHOULD**, not MUST) — "An updater that drops such a record SHOULD report the loss." Since this is a non-layer top-level record (not a layer record, and the probe's type is "it does not implement" so it isn't the registered user-metadata type either — it's an unregistered, unimplemented type for which the stored flags govern per §7.3/`[R-CNT-15]`, giving MU=0/PE=0 as stated), the same SHOULD-report obligation attaches generically to the governing-flags table, not to a type-specific rule.

I checked §21's register for a corresponding row: this SHOULD is not itself file-conformance-checked (§21's register is "MUST-level conditions only", `[R-CNF-12]`), so there is no register row for an unreported drop — consistent, not a gap.

## W5 — input trailer has ignore-lane bit 20 set; output after (a) appender commit, (b) rewrite, (c) creator-from-decoded-input

§6.3 (`[R-CNT-08]`): "An updater MUST copy forward unknown ignore-lane bits of its input file, MUST NOT clear them, and MUST NOT set any other ... no writer under this text originates an ignore-lane bit, this text defining none for it to mean anything by, so a bit is set only by a writer under the later minor version that defines it and carried forward by every updater under this text, appender and rewriter alike."

§20.5 (`[R-WRT-06]`): "The output trailer MUST copy the input's unknown ignore-lane flag bits forward and set no other, in place of the flags = 0 §6.3 requires of a file created under this text."

§20.1: a tool writing a new file from an existing one chooses between the rewriter position (undertakes to preserve, per §20.4 and §20.5 whole, "the unknown ignore-lane bits (`[R-CNT-08]`)" named explicitly among what it preserves) and the creator position ("As a creator it undertakes nothing toward its input, whatever it read: §20.2 binds it, it writes flags = 0 ... bytes it copied from another file included").

**(a) Appender's commit output trailer flags:** bit 20 still set (copied forward unchanged, `[R-CNT-08]`), no other bit set by this commit.

**(b) Rewrite's output trailer flags:** bit 20 still set (copied forward, `[R-WRT-06]`), no other bit set — even though the rewrite's file_id, placement, and every other trailer field are new/fresh, the ignore-lane bits are the one piece of trailer state a rewrite is obliged to carry rather than reset.

**(c) A creator that read the input and writes a new file from what it decoded:** flags = 0 — bit 20 is **not** carried forward. Per §20.1, this tool has chosen the creator position (it "undertakes nothing toward its input"), and §20.2/§6.3 bind a creator to write flags = 0 regardless of what it read. The distinction the probe is testing is exactly §20.1's: the same physical act (reading an existing file, writing a new one) is governed by different, mutually exclusive rule sets depending on which position ("undertaking", in the document's word) the writer adopts, and only the rewriter's undertaking carries the ignore-lane bit forward.

I found no sentence suggesting a decoded-and-rewritten creator inherits any trailer-copying obligation; `[R-CNT-08]`'s and `[R-WRT-06]`'s "updater"/"rewriter" language is consistently distinguished from "creator" throughout §20.1–§20.2 and §6.3.

## W6 — commit that changes only the fill value of a layer that stores a tile

§20.3 step 4 states the closed list of permitted changes to a layer that "stores a tile in the generation this commit supersedes": name changes, dimension-extent growth, planar-channel-list append/truncate (not both), slab/alignment declare/change/clear. Then: "Every other declaration is fixed for as long as the layer stores a tile: ... every channel's type **and fill** ... A commit MUST NOT change one of these; the change is a new layer, or a rewrite that re-declares it under a fresh file_id."

Later in the same step, the "what the line gives up" sentence lists explicitly: "a shrink, **a fill change**, a re-type, a re-tiling, ... are rewrites even where a particular file would survive them in place."

**Is the commit permitted?** No — a fill-only change to a layer that stores a tile is not an appender's operation; §20.3's worked figure (c) says so directly: "A change to any fixed declaration of a layer that stored a tile in the generation the commit supersedes — a fill value, a type, a tile extent — is not an appender's operation at all (step 4): it would reinterpret or invalidate every stored tile it reaches."

**What the document offers instead:** (i) a **rewrite that re-declares the layer** (§20.5 names "re-declaring a layer that stores a tile in the input" as one of its three named rewrite operations, "the rewrite §20.3 step 4 reserves for a change to a fixed declaration"); or (ii) an appender's commit that **drops the layer and adds a new layer under its name** with the new fill value, since §20.3 step 4 states "A commit MAY drop the layer (§20.4) and add a new one under its name and other declarations, the new layer being new whatever bytes its entries address" — this is a commit-level route, not only a rewrite, though it necessarily restores every stored tile (the old layer's tiles become slack; nothing of the old generation's data survives as "the layer").

**Is the file such an impermissible commit would leave nonconforming?** The bar itself is explicitly named a conduct rule, not a file-conformance rule: `[R-CNF-02]` lists "§20.3 step 4's bar on the fixed declarations of a layer that stores a tile" among the stated cases where "a file is never nonconforming by virtue of one: conduct rules bind the actor, the predicate binds the bytes." §20.3 step 4 repeats this: "This bar binds the commit as an actor: no file is nonconforming by virtue of its violation, and no register row records the violation itself ... a file such a commit leaves **can be** nonconforming on its own terms, as the paragraph below sets out." The following paragraph narrows exactly when a resulting file *is* independently witnessed as nonconforming: "but for a stored tile's decoded size, a padding position or pad bit, or a boolean byte the register witnesses (T3, T14, T21, T22, T4, T5, T2) and a decode that fails outright, or a codec's framing check that precedes it, under a changed codec or filter (T17, T24, T25), no check any actor owes able to see it (§21.7)." A pure fill-value change is witnessed only through edge-tile padding content (T4, `[R-SER-05]`) — and only where the layer in fact has edge padding (extent not an exact multiple of tile extent, §11.3). **So: where the layer has no edge padding at all, a fill-only change leaves no file-conformance witness whatsoever** — the resulting byte sequence can satisfy every §21 check and a verifier would certify it, even though the writer that produced it violated a bound conduct rule. This is the document's own, explicit, point (§21.7's "What no check detects" generalizes it: "this format detects corruption of structure, not incorrectness of content"), not an ambiguity I am raising — I flag it below as an OBSERVATION because it is a real byte-level consequence (what a conforming verifier is obliged to certify) that an implementer could easily miss on a first read of the "MUST NOT" bar alone.

## W7 — commit interrupted after directory durable, before trailer durable

§9.2 (`[R-LIF-02]`), steps: "(3) append the new complete directory ... followed by its CRC; (4) make steps 1–3 durable (a storage barrier) ...; (5) append the pad ... and the new trailer ...; (6) make the trailer durable." The probe's crash point is after step 4, before step 6 completes — i.e., the directory (and prior payloads/indexes) are durable, but the trailer is not yet durably in place (whether or not its bytes were physically written at all is exactly what "not yet durable" leaves open).

§9.2's own worked example covers this shape directly ("Example — what a crash sees"): "mid-commit │ … │ dirₙ │pad│ trailₙ │▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓ ... trailₙ intact, but no longer at the file's end" — followed by: "Mid-commit the physical tail is not a trailer, so a reader on the default path reports the file torn and MUST NOT scan backward (`[R-LIF-05]`)."

**What the next reader sees:** The reader validates the trailer at the physical end of file per §6.2/§9.5 (`[R-LIF-05]`: "a reader that finds no valid trailer in the final 64 bytes MUST report the file torn or invalid and MUST NOT scan backward"). Since the new trailer is absent or incomplete at the physical end (the crash happened before step 5/6 completed the new trailer and its barrier), the final 64 bytes fail the magic/CRC gates of §6.2 (register rows F8/F14, possibly F17 if length also mismatches) — reject-file / "torn", at the "open" detection point. The prior generation's trailer (trail_n) is still byte-intact somewhere earlier in the file (committed-prefix immutability, `[R-LIF-01]`), but it is **not** at the physical end, so the default read path does not find or use it (§9.5 forbids scanning backward).

**Whether the file is conforming:** As a byte-sequence whose own physical end fails §6.2's trailer gates, it is **not a conforming file** under the pure byte-predicate of §2.3 (conformance "does not depend on any reader, writer, or environment" but is evaluated against the bytes as they stand, and `[R-CNT-06]`'s gates are part of what every conforming file must satisfy at its own physical end).

**What the next appender does:** `[R-LIF-04]`: "A writer beginning a commit against an existing file MUST establish F by validating the trailer in the final 64 bytes of the physical file. If that validation fails, the file is torn: the writer MUST NOT append, and locating the last committed state is the deliberate recovery operation of §9.6 — never an implicit step of opening for append." So the next appender does not append; it must invoke §9.6's recovery scan (probe backward at 64-aligned offsets for the trailer magic, find trail_n as the nearest surviving candidate, re-verify it as a whole file per §8, then truncate the physical file to that recovered F) before any further commit — and only then does `[R-LIF-04]`'s "truncate to F... or overwrite from F" apply, anchored at the recovered F rather than the (torn) physical end.

## W8 — rewriter carries forward a layer it cannot decode (unimplemented sample type)

§20.5 (`[R-WRT-09]`): "A rewriter's verification depth over what it carries follows reliance (`[R-WRT-03]`): it relies structurally on every structure it copies, so it MUST verify each link of the chain — the open (§19.1), each retained layer's record (§19.3) and full index chain (`[R-IDX-04]`), and the checksum §8.1 states over each extent it copies, **every stored tile's entry crc among them** — before emitting that structure's bytes." And earlier in §20.5: "a violation latent in a structure it carries forward verbatim travels into its output (`[R-WRT-01]`) — its verification depth over what it carries is `[R-WRT-09]`'s and **reaches no decoded content**."

**What it must verify about each stored tile it copies:** the structural chain only — crc_of_crc_array over the fetched segment-CRC array, the segment CRC over the segment containing the tile's entry (`[R-IDX-04]`), and the tile's own stored-bytes CRC (its index entry's `crc` field, per §8.1's coverage map) — **not** the decoded content (which, for an unimplemented sample type, it cannot even produce). This matches §20.1/`[R-CNF-11]`'s general point that an updater is "a reader of every structure it processes" to §20.3's `[R-WRT-03]` depth, which for structures it neither modifies nor decodes is the structural chain, not §14's content obligations.

**What it does when a checksum fails:** `[R-WRT-09]`'s own text: "A rewriter MUST refuse to rewrite when any check `[R-WRT-09]` obliges fails, and MUST NOT emit a file carrying a violation it has detected: it can neither re-emit the structure corrected (`[R-WRT-05]`), nor keep it and call the output clean. **Dropping is the one disposal that answers**, and only where §20.4's table licenses it ... Where the table does not license a drop the rewriter MUST refuse." A layer record's own governing flags are fixed by the registry at MU = 0, PE = 0 (§7.3's table; §20.4 names the layer record as "dropped under the table's last row"), so dropping the whole layer is licensed **unless** some sub-record of that layer is a type the updater does not implement with MU = 1 (which blocks the drop per §20.4's MU = 1 row and W9 below) — in which case the rewriter has no disposal but to refuse the whole rewrite.

**Whether it may instead re-create the layer:** No. Re-creating a layer means writing it as a creator from content the rewriter itself decoded ("A layer the rewrite re-creates is new output: its record, its tile-index region and its stored tiles are written under §20.2's rules from content the rewriter decoded (§19.3, §19.4)" — §20.5). Since the sample type is unimplemented, the rewriter cannot decode it, so re-creation (which presupposes a successful decode) is unavailable to it; its only two dispositions for this layer are carry-forward-verbatim (if every link verifies) or drop (if licensed) — refusal if neither holds.

## W9 — commit would drop a layer whose own record is PE = 0 but which carries a sub-record (MU = 1, unimplemented) of its own

§20.4, directly: "A commit MAY therefore drop a layer record, and the drop takes the layer whole: a sub-record's flags govern it within a layer the updater keeps, so a dropped layer's sub-records and their extents go with it whatever their PE bits. **One sub-record blocks the drop, a sub-record of a type the updater does not implement with MU = 1, the drop being a modification of the scope it governs (the table's first row).**"

This is the single decisive sentence; I cite every other sentence I found bearing on the act and checked them against it:
- §20.4's MU = 1 table row: "At layer scope an unknown critical record blocks modification of that layer, **its drop included**, leaving other layers editable." — agrees; states the same rule generally (not layer-record-specific).
- §7.2 (`[R-CNT-18]`): "an unknown sub-record type with MU = 1 is reject-layer" — states the reader-side consequence of the sub-record's own unimplemented-criticality, consistent with it being untouchable, hence undroppable alongside its layer.
- §20.3 step 2: "MUST NOT drop the record save where §20.4 licenses the drop" — general append-procedure statement, consistent with (and pointing straight at) §20.4's table, which is where this specific block is stated.

**Answer:** No, the commit may **not** drop the layer. Although the layer record's own flags (PE = 0 per the registry) would, in isolation, license dropping the layer (per the MU=0/PE=0 row and the "table's last row" language), the presence of an MU = 1, not-understood sub-record overrides that licence: the drop is "a modification of the scope [the sub-record] governs" (the layer), and the MU = 1 row's "MUST NOT modify the scope the record governs" therefore forbids the drop. I found no sentence disagreeing with this; every passage I located treats the MU = 1 sub-record as the controlling fact once one is present, and the layer record's own PE = 0 as relevant only in a layer that carries no such blocking sub-record.

## W10 — appender carries forward unmodified a top-level record, unimplemented type, MU = 0 / PE = 0, wishes to drop it in this commit

**Append procedure, step 2 ("Open")**: "Against any other structure the appender carries forward, it MUST NOT repair the defect ... and MUST NOT drop the record **save where §20.4 licenses the drop**."

**Preservation section, §20.4, MU = 0/PE = 0 row**: "Retain byte-identical, or drop it — its extent becoming slack. ... an appender MAY drop the record in any commit it is otherwise free to make — one whose only effect is the drop included."

**Agreement check:** Step 2's clause is phrased as a general prohibition with an explicit carve-out pointing at §20.4; §20.4's table is precisely the "licence" that clause refers to, and for this record's governing flags (MU = 0, PE = 0, stored-flags-authoritative since the type is unimplemented per §7.3/`[R-CNT-15]`) that licence says MAY drop. The two sections agree exactly — one states the general rule-with-carve-out, the other fills in the carve-out for this flag combination — and I found no third passage (e.g. in §9.2's commit protocol or §20.3's numbered steps) stating anything different about this case.

## W11 — updater implements an unregistered type from the definition it took the type from; that definition fixes MU = 1, PE = 0; a record of this type it does not modify

§20.4, verbatim, in sequence:
1. "For a type the updater implements that this specification does not register, the definition it implements the type from supplies the flags, and the stored bits never do (`[R-CNT-22]`, §10.3)." — so the governing flags here are the ones the probe states: MU = 1, PE = 0, taken from the definition, not from the record's own stored bits.
2. "The table states what an updater owes a record it does not logically modify, read under whichever flags govern it. **Its MU = 1 row reaches only a type the updater does not implement** — an updater implements both registered types and understands an unregistered type it implements from its definition, modifying their records as §20.3 and that definition provide — **so for an implemented type only the PE bit bites**."

**What the preservation table obliges:** Because the updater *implements* this type (by hypothesis), the table's MU = 1 row does not reach it — that row is reserved for types the updater does not implement. Only the PE bit governs, and PE = 0 here, so the applicable row is the MU = 0/PE = 0 row: "Retain byte-identical, or drop it — its extent becoming slack. ... SHOULD report the loss."

**May the updater drop it?** Yes — the PE = 0 licence applies in full (an appender MAY drop it in any commit it is otherwise free to make; a rewriter MAY drop it in any rewrite), exactly as if the governing flags were plain MU = 0/PE = 0, because the MU bit's preservation force is tied to non-implementation, not to the definition's label of "critical". An implementer who read "MU = 1" literally and assumed unconditional retention would get this wrong.

**Which sentence decides which row governs an implemented type:** "Its MU = 1 row reaches only a type the updater does not implement ... so for an implemented type only the PE bit bites" (§20.4). This is the single decisive sentence; it is a direct continuation of the sentence immediately before it in the same paragraph (quote 1 above), and I found no other passage addressing this specific configuration (implemented + unregistered + definition-fixed MU=1/PE=0) that disagreed with it.

---

## Findings log (also reported structurally)

- **writera-01** (OBSERVATION): §20.3 step 4's bar against changing a stored-tile layer's fixed declarations (e.g., fill value) is explicitly a conduct rule, not a file-conformance rule (`[R-CNF-02]`); the document itself notes the resulting file "can be nonconforming on its own terms" but narrows the independent witnesses to a short, named list of register rows (T2–T5, T14, T17, T21–T25) plus outright decode/framing failure. A fill-value-only change on a layer with **no edge padding** (extent an exact multiple of tile extent, §11.3) triggers none of those — meaning a conforming verifier would certify a file that resulted from a conduct-rule violation, and two conforming implementations can diverge on whether to even attempt such a commit while producing output that is byte-level indistinguishable in conformance status either way. This bears on which bytes a conforming reader/verifier MUST accept, so it meets the byte-level test, even though the document is already explicit about it (so I report it as an observation worth a probe/implementer's attention, not as an unflagged gap).

All other probes (W1–W5, W7–W11) were fully determined by the document, each by a single governing sentence or a short, mutually agreeing set of sentences across the two sections the probe named (append procedure vs. preservation, in W9/W10/W11's case); I found no second passage that spoke to the same act and disagreed with the one I cited. W3 and W9 each turn on sentences that are easy to read past (the "no commit is available at all" scope in W3; the "one sub-record blocks the drop" exception in W9), but neither is itself an ambiguity — each has exactly one controlling sentence I could locate and cite.
