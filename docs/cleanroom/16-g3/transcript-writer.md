# Cleanroom round 16 — Writer implementer transcript

## 0. Disclosure

I read exactly one file: `/Users/robertkleffner/Documents/GitHub/tarn/spec/tarn.md`,
in five `Read` calls covering lines 1–4283 (the whole document). I opened no
other file. I did not read `docs/`, `PLAN.md`, `OPEN-QUESTIONS.md`, `AGENTS.md`,
`README.md`, `CONTRIBUTING.md`, `conformance/`, or `spec/registry.json`. I ran no
`git` command and issued no web request. I did not list or read the output
directory.

One thing I must disclose because it arrived unbidden: the harness's environment
preamble included a `gitStatus` block carrying five recent commit subject lines
(ADR numbers and short titles). I did not seek it, and I did not use it to settle
any question — every conclusion below is anchored to a quotation from
`spec/tarn.md`. It did shape one *suspicion* (that §20.3's declaration-freeze rule
was recently reworked), which I then investigated against the document alone and
concluded was correct.

Everything else I ran was local computation over files I created myself, in
`…/scratchpad/`: `crc.py` (a CRC-32C implementation), `checkdoc.py`, `build.py`,
`read.py`, `append.py`, `torn.py`, `compact.py`, `count.py`. These read no project
file. I wrote four binary artifacts (`gen1.tarn`, `gen2.tarn`,
`gen3-compacted.tarn`) and this transcript.

---

## 1. Instrument check — do the document's own constants reproduce?

Before trusting my own bytes I made the document check itself. `[R-ENC-09]` fixes
CRC-32C (Castagnoli 0x1EDC6F41, reflected in and out, init 0xFFFFFFFF, final XOR
0xFFFFFFFF, stored little-endian) and §4.5 gives a check vector. I implemented it
from that paragraph alone and got:

| Claim | Where | Computed | Verdict |
|---|---|---|---|
| CRC-32C(`"123456789"`) = 0xE3069283 | §4.5 | `0xe3069283` | ✓ |
| CRC-32C(zero bytes) = 0x00000000 | §4.5 | `0x0` | ✓ |
| CRC of 2¹⁶ sentinel entries = 0xEECB3BB2 | `[R-IDX-05]`, App. B | `0xeecb3bb2` | ✓ |
| §7.4 example: CRC of 4 sentinel entries (80 B) = 0x80A34955 | §7.4 | `0x80a34955` | ✓ |
| §7.4 example: crc_of_crc_array = 0xC4EE982E | §7.4 | `0xc4ee982e` | ✓ |
| Appendix A trailer CRC = 0xE00938D2, bytes `D2 38 09 E0` | App. A | `0xe00938d2` | ✓ |

I also rebuilt §7.4's worked layer-record payload field by field. It is 81 bytes,
every offset in the annotated listing lands where the table says, and bytes
[56,68) are `04 74 65 6d 70 0c 00 04 00 00 c0 7f` and [77,81) are `2e 98 ee c4`
— byte-for-byte what §7.4 prints. The arithmetic prose ("4 + 34 bytes, the
dimension entry 18, the channel entry 12, and the trailing fixed fields 13 — 81
exactly") also checks: 1+2+2+2+8+8+8+1+2 = 34.

This example is new-ish surface and it is clean. It is also load-bearing for a
first implementer: it is the only place the packed inline payload is shown as
bytes, and getting the nine-scalar block right (34 bytes, no padding) is the
single easiest thing to get wrong in this format.

I separately reproduced §14.2's three offset examples (Q = 3 → bytes [15,18);
planar `b` → bytes 10–11; float32 + bool → Q = 5, bytes [25,30)), §14.3's packed
plane (`55 01` with fill false, `55 FD` with fill true), §14.5's edge-tile example
(extents (5,5), tiles (4,4), one uint16 channel, fill 0xABCD → 32 bytes, value 0
real, values 1–15 each `CD AB`), §17.3's shuffle example (`00 00 00 00 00 00 80 00
40 3F 40 40`), §11.4's ordinal examples (s = 10; in-tile ordinal 11,452; planar
disk ordinal 74), and §15.4's two examples (16 segments, region 20,000,064 bytes,
segment 15 at [19,660,800, 20,000,000), CRC array at [20,000,000, 20,000,064);
and entry 74 at region bytes [1,480, 1,500)). All correct.

Nothing in this section is a finding. I record it because it is what licensed me
to trust the arithmetic in the rest of the walk.

---

## 2. Creation — a file end to end

### 2.1 What I chose to build, and why

I wanted a file that exercises the writer decisions that actually differ from
each other: both layouts, both alignment mechanisms (they are mutually exclusive
per layer, `[R-CNT-16]`, so I needed two layers), a sentinel run, an edge tile
with padding positions, a packed bool plane with pad bits, and a file-scope
user-metadata record.

- **Layer `sst`** — rank 2, dims `y`(E=5, T=4) and `x`(E=5, T=4), **interleaved**,
  one `uint16` channel `v` with fill `0xABCD`, codec 1, filter 1, **alignment
  A = 512**, no slab. G = (2, 2), N = 4, P = 16, Q = 2, decoded size 32.
  entry_count = 4 (interleaved → N, `[R-GEO-03]`). Tiles 0 and 3 stored, 1 and 2
  sentinel.
- **Layer `mask`** — rank 1, dim `i`(E=10, T=10), **planar**, one `bool` channel
  `m` with fill `0x00`, codec 1, filter 1, **slab S = 1, A_slab = 64**.
  G = (1), N = 1, C·N = 1 addressed tile (planar → C·N). P = 10, decoded size
  ⌈10/8⌉ = 2. One stored tile.
- **File-scope user metadata**, encoding 1 (none), document
  `{"tarn.created":"2026-08-20T00:00:00Z","tarn.title":"demo"}` — 58 bytes,
  members sorted by decoded-key UTF-8 bytes as `[R-MTA-05]` requires
  (`tarn.c…` < `tarn.t…`).

Tile 3 of `sst` is deliberately §14.5's worked example: tile coordinates (1,1)
covering y,x ∈ [4,8), one real position (4,4) and 15 padding positions each
carrying the fill bytes `CD AB`. My emitted tile 3 is
`92 10` followed by 15 × `cd ab` — the document's own example, arrived at
independently.

The `mask` tile is §14.3's example: values alternating true/false from ordinal 0,
so byte 0 = `0x55`, byte 1 = `0x01` with pad bits 2–7 carrying the fill bit
(false = 0), per `[R-SER-05]`'s "Every pad bit (§14.3) MUST carry the plane's
channel's fill bit."

### 2.2 Emission order and the actual byte map

`[R-LIF-02]`'s creation path is: front signature block; then steps 2–6 writing
from offset 16, generation 1. Step 2's ordering is explicitly free ("in any order
satisfying §5.2's coverage classes"). I nevertheless emitted in Appendix G item
3's total order, so that the same file would double as a reproducible-profile
test: layers in ascending layer-name byte order (`mask` = `6D 61 73 6B` <
`sst` = `73 73 74`), each layer's stored tiles in disk-ordinal order then its
tile-index region, then non-layer record extents, then the directory.

```
  start     end    len  what                                fixed by
      0      16     16  front signature block               §6.1 [R-CNT-04]
     16      64     48  SLACK (A_slab=64 forces mask's       §16.2 [R-SLB-03]
                        first stored tile to 64)
     64      66      2  mask tile, disk ordinal 0           writer choice of place
     66      90     24  mask index region (1×20 + 1×4)      §15.1 [R-IDX-01]
     90     512    422  SLACK (A=512 forces sst tile 0)     §16.1 [R-SLB-01]
    512     544     32  sst tile 0                          A=512
    544    1024    480  SLACK (A=512 forces sst tile 3)     §16.1
   1024    1056     32  sst tile 3 (edge tile, 15 padding)  A=512
   1056    1140     84  sst index region (4×20 + 1×4)       [R-CNT-17]
   1140    1203     63  user-metadata extent (58 + 4 CRC)   §7.1 [R-CNT-25]
   1203    1450    247  directory region (243 + 4 CRC)      §7.1 [R-CNT-11]
   1450    1472     22  SLACK — pre-trailer pad             [R-LIF-02] step 5
   1472    1536     64  trailer, generation 1               §6.2
```

F = 1536, F mod 64 = 0 ✓ (`[R-CNT-01]`). dir_offset = 1203 ≥ 16 ✓, dir_length =
247 ≥ 4 ✓, dir_offset + dir_length = 1450 ≤ F − 64 = 1472 ✓ (`[R-CNT-06]`).
`[R-CNT-09]`'s discovery-window advice: 247 + 22 + 64 = 333 ≤ 65,536 ✓.

**Field-by-field, was the value fixed by the document or left to me?**

| Field | Value | Who decided |
|---|---|---|
| front block [0,16) | `89 54 41 52 4E 0D 0A 1A` + 8 zeros | **document**, §6.1 |
| first structure offset | 16 (here pushed to 64 by A_slab) | **document** floor `[R-CNT-13]`; placement mine `[R-SLB-05]` |
| tile placement | 64, 512, 1024 | **document** constrains mod A / mod A_slab; the rest mine |
| index region placement | immediately after each layer's tiles | **mine** — `[R-SLB-05]` |
| index region internal layout | entries then CRC array, no padding | **document**, §15.1 |
| entry order | disk-ordinal order | **document**, `[R-IDX-01]`, `[R-GEO-06]` |
| sentinel bytes | `FF ×16 00 ×4` | **document**, `[R-IDX-02]` |
| record flags | layer 0x0003, usermeta 0x0002 | **document**, §7.3 + §7.2 bit map |
| record order in directory | layer, layer, usermeta | **mine** — `[R-CNT-14]` |
| dir_offset | 1203 | **mine**, subject to §6.2's "no structure between its end and the trailer" |
| pre-trailer pad length | 22 | **document**, `[R-LIF-02]` step 5 |
| pad content | zeros | **advisory**, `[R-CNT-03]` SHOULD |
| generation | 1 | **document**, `[R-LIF-02]` creation path |
| file_id | 0x5A17C0FFEE00D15E | **mine**; `[R-LIF-03]` SHOULD draw randomly |
| version_minor | 0 | **advisory**, `[R-CNT-26]` SHOULD |
| flags | 0 | **document**, `[R-CNT-08]` |
| trailer reserved [56,60) | zeros | **document**, §6.2 |

Two things I checked and want to record because they are easy to get wrong and
the document does fix them:

1. **`file_id` is not subject to `[R-ENC-03]`'s 2⁶³−1 domain.** §4.2 bounds "every
   offset, length, extent, and count"; a file identifier is none of those, §6.2's
   only constraint is "≠ 0", and F2's Instances cell lists `dir_offset;
   dir_length; committed_file_length; generation; …extent_offset; extent_length`
   and pointedly not `file_id`. This matters because Appendix G item 2 derives
   `file_id` from a hash's last eight bytes read little-endian, which sets bit 63
   half the time. The document is consistent here.

2. **crc_of_crc_array at entry_count = 0.** §7.4 says "0 when entry_count = 0";
   the general rule would say CRC-32C over a zero-byte array, which §4.5 fixes at
   0x00000000. The special case agrees with the general rule rather than
   overriding it. Good.

### 2.3 Reading it back

I wrote an independent reader (`read.py`) that follows §19.1's four open steps,
§19.3's layer validation list, and §19.4's tile-read algorithm, and never reuses a
value from `build.py`. It re-derives G, N, P, Q, addressed-tile counts,
`[R-CNT-17]`'s extent_length formula, every segment CRC, crc_of_crc_array, every
entry classification per §15.3's table, `[R-COD-04]`'s codec-1 length equality,
and both `[R-SLB-01]` and `[R-SLB-03]` invariants. It accepts the file and returns
the expected samples, with entries 1 and 2 of `sst` short-circuiting to fill per
§19.4 step 4.

I record one thing the walk surfaced: for a **planar** layer the reader must map
entry index k back to a channel as `c = k div N` in order to know whether the
plane is bit-packed (§14.3) or byte-laid-out (§14.2), because decoded size depends
on the channel's *type*. §14.1 gives the mapping ("the tile with disk ordinal
c · N + s … carries exactly the values of channel c") and §12.1 says "a planar
bool plane is sized by packing (§14.3)". Both are present; a reader that does not
join them will size every plane at P·Bᶜ and mis-size every bool plane. This is
correctly specified, just spread across three sections.

---

## 3. The append procedure

### 3.1 What I appended

Against `gen1.tarn` I performed one commit that does two things at once, because
that is where the interesting interactions live: **add a new layer `aux`** (rank 1,
E=3, T=3, interleaved, one float32 channel `f` with fill 0x7FC00000, one stored
tile) **and supersede `sst`'s tile 0**.

`[R-WRT-04]`'s ordered procedure, as I executed it:

1. **Establish F.** Validate the trailer in the physical file's final 64 bytes
   (`[R-LIF-04]`). Passed → F = 1536.
2. **Open** (§19.1). The appender is a reader here. Four top-level… three
   top-level records parse; no violation.
3. **Validate what the commit touches** (`[R-WRT-03]`): trailer and full directory
   always, plus §19.3 for `sst` (whose index I re-emit) and the §19.4 index chain
   for every segment whose entries I reuse. `mask` is neither modified nor relied
   on, so no §19.3 for it — I only copy its record image.
4. **Write payloads and indexes**, beginning at exactly F = 1536.
5. **Re-emit the directory** per §20.4, then its CRC.
6. **Commit**: barrier; pad; trailer with generation 2, the same file_id, ignore-
   lane bits copied forward, `version_minor` per `[R-CNT-26]`; barrier.

```
   1536    1568     32  sst tile 0 (new payload)      512-aligned: A=512 still declared
   1568    1580     12  aux tile, disk ordinal 0      no alignment declared
   1580    1604     24  aux index region
   1604    1688     84  sst index region, re-emitted in full at a new placement
   1688    2037    349  directory (gen 2)
   2037    2048     11  pre-trailer pad
   2048    2112     64  trailer, generation 2
```

576 bytes appended. Newly created slack: old `sst` tile 0 [512,544) = 32; old
`sst` index [1056,1140) = 84; gen-1 directory [1203,1450) = 247; gen-1 pad
[1450,1472) = 22; gen-1 trailer [1472,1536) = 64. Total new slack 449.

### 3.2 The thing that bit me, and the document was right

My first append attempt asserted that `sst`'s layer-record inline payload would
re-emit byte-identically with only its **extent slot** re-pointed. That assertion
failed, correctly. Superseding one tile changes entry 0, which changes the
segment CRC, which changes **`crc_of_crc_array`** — a field inside the inline
payload. So a supersede touches the layer record's payload as well as its slot.

The document says this without saying it in one place: §7.4 puts
`crc_of_crc_array` in the inline payload; `[R-WRT-07]` names it as the field a
compactor updates when it regenerates a region; §20.3 step 4 distinguishes "a
layer whose record alone changes" from one whose index content changes. Joining
them gives the right answer. I record it because it is the one place my
first-pass writer was wrong and the specification was not.

### 3.3 The full record-flag matrix for an updater

My charter is to walk every combination of the flags §7.2 defines — bit 0
MUST_UNDERSTAND, bit 1 PRESERVE_ON_EDIT, bits 2–15 reserved — and say exactly
what my updater may do. §20.4's opening sentence is the key that makes the table
usable: "Persistence governs every record type; only the authoritative source of
the flags differs."

**Which flags govern:**

- **Type §7.3 registers (0x0001, 0x0002).** The *registry's* fixed values govern,
  not the stored bits (`[R-CNT-22]`). Both registered types carry PE = 1.
- **Type the updater implements that this specification does not register.** The
  definition the updater implements the type from supplies the flags; the stored
  bits never do. (In practice this is an experimental-range type, since a
  reserved-range type in the file is itself a violation, F36/L25.)
- **Type the updater does not implement.** The stored flags are authoritative,
  with MU = 1 / PE = 0 read as PE = 1 (`[R-CNT-12]`).

**What my updater is permitted to do, per combination:**

| Stored flags | Top-level record | Layer sub-record |
|---|---|---|
| **MU=1, PE=1** (unimplemented type) | **No commit at all.** The updater is a reader first; `[R-CNT-15]` makes an unimplemented top-level MU=1 record reject-file. Compaction barred on the same ground (`[R-WRT-06]`). | Retain byte-identical; **must not modify that layer**; other layers stay editable (`[R-CNT-18]` makes it reject-layer, never reject-file). |
| **MU=1, PE=0** (unimplemented) | Read as PE = 1 (`[R-CNT-12]`), then exactly the row above. Additionally F25/L46: a verifier records the combination as a violation; my updater is not obliged to detect it and re-emits the bytes as found. | Same, at layer scope (L46). |
| **MU=0, PE=1** (unimplemented) | Retain byte-identical, extent content unmodified. Commits to other scopes unrestricted. | Same. |
| **MU=0, PE=0** (unimplemented) | Retain byte-identical, **or** drop it — but only in a commit that *independently* changes the file's layer set or another non-layer top-level record. A supersede is explicitly not such a change; nor is the drop itself. SHOULD report the loss. | Retain, or drop only in a commit that independently changes that layer's record, the entry set of its index, or which of its tiles are stored. |
| **any reserved bit 2–15 set** | Ignore the bits (`[R-CNT-12]`); re-emit byte-identically. If I *modify* the record it becomes new output under `[R-CNF-05]`, so I must then emit the reserved bits as zero — there is no preservation rule for record reserved bits, unlike the trailer's ignore-lane bits (`[R-CNT-08]`). | Same. |
| **registered type, stored bits ≠ registry** | Process under the type's *fixed* semantics regardless (`[R-CNT-22]`); re-emit byte-identically if retained, carrying the F28/L49 violation forward. | Same (L49). |

Two points where a naive updater goes wrong and the document is explicit:

- **Re-emitting a violating record is not authoring it.** §20.3 step 2: "Reproducing
  a structure's bytes unchanged is not authoring them: an appender satisfies its
  writer obligations for the bytes it produces, and a violation latent in a
  structure it neither modifies nor relies on travels with that structure … which
  is as true of an index entry copied to its disk-ordinal position as of a record
  re-emitted byte-identically". Without this my updater would face an impossible
  conflict between `[R-WRT-05]` (re-emit byte-identically) and `[R-CNF-05]` (emit
  only conforming files). It is well handled, and `[R-CNF-06]` is what actually
  binds an updater — "every writer requirement **for the bytes it produces**".
- **A malformed index entry is carried forward, not repaired.** §20.3 step 2 again:
  "a malformed index entry an appender meets while re-emitting a region is carried
  forward byte-identically at its disk-ordinal position under step 4, not repaired
  to a sentinel." I implemented this; it is the only sane answer given
  `[R-CNF-04]`'s ban on heuristic repair.

**Where I had to guess:** the MU=0/PE=0 drop condition's phrase "the file's layer
set". See finding **writer-05**.

### 3.4 Durability, and the commit point

`[R-LIF-02]` fixes it exactly and I have nothing to add except to state it as a
writer executes it:

- Steps 1–3 (payloads, indexes, record extents, complete directory + CRC) are made
  durable by the **step 4 barrier**.
- Step 5 writes the pad and the trailer. Step 6's barrier makes the trailer durable.
- **The commit point is the moment the 64 trailer bytes become durable.** Before
  that, a reader sees the previous generation (if nothing past F was written) or a
  torn file (if it was). After it, the new generation is live and its bytes are
  immutable forever (`[R-LIF-01]`).
- On creation the front block is written first and "whose durability the barriers
  of steps 4 and 6 cover" — `[R-WRT-02]` is emphatic that it is "both barriers,
  not one".

The only ordering that is *observable* is 3 → 4 → 5 → 6. The order of writes
*within* steps 1–3 is unobservable, since the step-4 barrier makes them all
durable together and a crash before it leaves no trailer either way; `[R-LIF-02]`
nonetheless says "MUST, in order: (1) … (2) … (3)". I noted this as a mild tension
with §2.1's Note ("requirements constrain bytes and observable behavior, never
implementation technique") but it is not a defect: no byte and no verdict turns on
it, and the sequence is a legible way to state the layout dependency. Not filed.

---

## 4. Slack, per shape of commit

§5.2 defines slack as everything the live committed state does not claim, and
`[R-CNT-21]` gives its content ("no internal structure this specification defines,
its content is unconstrained, and no conformance requirement applies to it") and
its counter (the verifier, `[R-LIF-08]`, reporting a **partial** total naming what
stopped the walk where its walk does not complete). Readers never count it and
`[R-CNT-21]` bars them from interpreting it.

**(a) Creation.** Only alignment gaps and the pre-trailer pad. My gen 1: 48 + 422
+ 480 + 22 = 972 bytes of slack in a 1536-byte file — 63%, all of it forced by
`A = 512` on a layer with 32-byte tiles. Content: whatever the writer left;
`[R-CNT-03]` advises zeros and Appendix G item 3 makes zeroing a requirement of
the profile.

**(b) Append.** Everything the commit superseded, plus the new commit's own
alignment gaps and pad: the previous directory, its pad, its trailer (always —
"a commit that touches no layer re-emits the directory, the pad and the trailer
alone", §5.1's example); plus, for each layer whose stored-tile set or index
content changed, that layer's **whole previous index region**; plus every
superseded stored-tile payload; plus every superseded record extent. Measured on
my gen 2: 449 new bytes of slack for a 32-byte data change. §20.3's note quantifies
the general case ("editing one sample of a 10⁶-tile layer appends about 20 MB of
index and leaves as much slack").

**(c) In-place update.** There is none. `[R-LIF-01]` freezes [0, F). The only
bytes a writer may overwrite are those beyond a committed F after a torn write
(`[R-LIF-04]`), and those were never in any live committed state, so they were
never slack.

**(d) Rewrite (whole-file, fresh file_id).** The output's slack is only its own
alignment gaps and pad. The *input* persists unmodified until something outside
this specification deletes it (`[R-PRV-02]`); it is not slack, it is a second file.

**(e) Compaction.** `[R-WRT-06]`: the output "contains only the structures
reachable from the input's live trailer … so slack is never carried". Measured:
compacting my gen 2 took F from 2112 to 1664 and slack from 1410 to **962**. The
962 is not a defect — `[R-WRT-07]` frees the compactor to place structures anywhere
"§5.2 admits and every declared layout invariant permits (`[R-SLB-01]`,
`[R-SLB-03]`)", and `A = 512` on `sst` forces 422 + 480 bytes of gap plus a 48-byte
pad no matter where it puts things. Worth stating plainly because §20.5's figure
draws a slack-free output: **compaction does not drive slack to zero on an
alignment-declaring layer.** Only clearing the declaration would, and that is a
declaration change the compactor is not licensed to make.

**(f) Abandoned partial write.** It contributes **no** slack, and this is a
pleasingly clean consequence. `[R-LIF-04]` gives the writer two paths and both
erase it: truncate to F before step 1, or overwrite from F and truncate to the new
committed_file_length no later than step 6. Either way "bytes beyond a committed
length never survive into any committed state." The one residue is indirect: if
the *next* commit's first structure is alignment-forced above F, the gap between F
and it is slack **containing the abandoned write's stale bytes**, which is exactly
the hazard `[R-CNT-03]` names ("A writer that does not [zero] leaves bytes
indistinguishable from stale data"). I now regard zeroing gaps as mandatory
practice for any writer that ever resumes after a tear, and the specification's
SHOULD is well-judged.

Who counts, in one line: **the verifier and nobody else** (§9.7, `[R-LIF-08]`);
a reader must not interpret slack; a writer has no counting obligation; and
§5.2 is careful that a verifier which never establishes a live trailer owes no
total at all, "which is not a partial total but the absence of one."

I checked `[R-CNT-21]`'s claim that a partial total is "an upper bound … never an
under-count": partial = F − (bytes claimed by enumerated claimants), true =
F − (bytes claimed by all claimants), and enumerated ⊆ all, so partial ≥ true. It
holds, and the double-counting worry (overlapping claimants would make the sum too
big and the difference too small) is closed by the rule that a walk-established
overlap discards that layer's claimants. Correct.

---

## 5. Torn-write recovery

I built seven physical files and ran both a §6.2/§19.1 reader and a §9.6 recovery
probe against each.

| Crash point | Physical len | Next reader sees | Next updater does | Recovery lands on |
|---|---|---|---|---|
| **A** mid step 2 — 40 of 576 payload bytes durable | 1576 | reject-file: trailer magic (F8, `[R-CNT-06]`) | `[R-LIF-04]`: **must not append**; recovery is separate | trailer at 1472 → truncate to 1536 → gen 1 |
| **B** after step 3 — directory durable, no trailer | 2037 | reject-file: trailer magic (F8) | must not append | 1472 → gen 1 |
| **C** mid step 5 — pad + 40 of 64 trailer bytes | 2088 | reject-file: trailer magic (F8) | must not append | 1472 → gen 1 |
| **D** after step 5, before step 6's barrier, all bytes present | 2112 | **OK, generation 2** | appends normally from F = 2112 | 2048 → gen 2 |
| **E** weak barrier — trailer durable, directory bytes not | 2112 | reject-file: **directory CRC** (F20, `[R-CNT-11]`) | must not append | see below |
| **F** step-6 truncation skipped — residue past new F | 3136 | reject-file: trailer magic (F8) | must not append | 2048 → truncate to 2112 → gen 2 |

**Is the file conforming in the meantime?** No, in every torn case. §5.1
`[R-CNT-01]` requires "The file size of a conforming file equals the live
trailer's committed file length F", and in A/B/C/F the final 64 bytes are not a
trailer, so no live trailer is established at all. The *previous* state is not
readable, only **recoverable** — §9.2's example says exactly this and the
distinction is the whole return on append-only ("The window is not one in which
the old state is *readable* — it is one in which the old state is *recoverable*").
A reader must not scan backward (`[R-LIF-05]`), so it cannot tell A from
corruption and is not asked to.

**Scenario E is the one that tests §9.6 properly.** The naive probe settles on the
trailer at 2048: magic matches, CRC verifies, committed_file_length = 2112 =
o + 64. All three of §9.6's conditions pass. But truncating there yields a file
whose directory CRC fails. §9.6 covers this: "a candidate whose whole-file
re-verification fails was not a commit state, so the tool continues the probe past
it, and MUST report the candidate it settled on and how many it rejected." So the
tool continues to 1472 and recovers generation 1, reporting one rejected
candidate. Without that clause a recovery tool would hand back a file that does
not open. It is present and it is normative. Good.

**Scenario F** is `[R-LIF-04]`'s truncation obligation being violated. §9.5's Note
covers exactly this and declines to give it a register row of its own, correctly:
"A reader meets it as a trailer that fails its gates … and `[R-LIF-05]` forbids it
to scan backward, so it cannot tell residue from corruption and is not asked to."

One state I looked for and could not construct: a torn file whose physical tail
*accidentally* passes all of §6.2's gates. §9.6's first caution names it ("a tile
payload can deliberately contain a byte string that mimics a valid trailer") and
§21.6 records it as inert; the defense is that committed_file_length must equal
the physical size, so the mimic must sit at exactly the physical end, and the
directory CRC then catches it (§6.2's Note). I could not find a hole here.

---

## 6. Byte-divergence catalogue

Given identical input arrays and identical stated options, here is every way I
found for two conforming writers to differ, and whether Appendix G closes it.

| # | Degree of freedom | Rule that leaves it open | Closed by |
|---|---|---|---|
| 1 | Structure placement and order | `[R-SLB-05]`, `[R-LIF-02]` step 2 | item 3 |
| 2 | Content of alignment gaps and the pre-trailer pad | `[R-CNT-03]` (SHOULD only) | item 3 |
| 3 | Extent of gaps (packing vs scattering) | `[R-SLB-05]` | item 3 |
| 4 | Record order in the directory; sub-record order | `[R-CNT-14]` | item 3 |
| 5 | `file_id` | `[R-LIF-03]` (SHOULD random) | item 2 |
| 6 | Number of commits / generation reached | §9 nowhere constrains | item 4 |
| 7 | `version_minor`; `flags` | `[R-CNT-26]` (SHOULD) | item 8 |
| 8 | Fill recorded when the caller chooses none | `[R-TYP-10]` (SHOULD) | item 7 |
| 9 | Whether an all-fill tile is stored or sentinel | no rule requires either | item 6 |
| 10 | Declared alignment A / slab S / A_slab | §16 leaves to the writer | item 5 |
| 11 | Name normalization (NFC vs NFD) | `[R-ENC-14]` (SHOULD) | item 10 |
| 12 | Codec **encoder** output for a fixed codec value | `[R-CNF-05]`; §17.2's Note on DEFLATE's final-byte bits | item 1 |
| 13 | zstd Frame_Content_Size present/absent; declared window | `[R-COD-06]` ("MAY be present") | item 1 (encoder settings) |
| 14 | User-metadata JSON number formatting, whitespace | `[R-MTA-05]` explicitly does not close it | item 9 |
| 15 | Metadata storage encoding 1 vs 2, and the zstd producer | §18.2 | item 9 |
| 16 | **Filter value 1 vs 2** | `[R-COD-09]` assigns both; nothing prefers either | **nothing — see writer-03** |

Non-divergences I checked and can classify as **forbidden**, so no writer freedom
exists:

- **De-duplicating two byte-identical stored tiles onto one extent.** Forbidden:
  `[R-CNT-13]` — "no two extent slots and no two structures overlap" — with L18
  registering the intra-layer case as reject-layer. Two writers cannot differ here.
- **Placing the directory anywhere but last.** Forbidden by §6.2's
  "no structure lies between its end and the trailer" (F7).
- **Emitting an all-padding tile.** Unconstructible: G = ⌈E/T⌉ guarantees
  (G−1)·T < E, so every addressed tile of a nonempty layer contains at least one
  real position along every axis.
- **Choosing linearization or index_encoding.** Only value 1 is emittable
  (`[R-GEO-05]`, §7.4), so no freedom.
- **Using `[R-IDX-05]`'s all-sentinel constant instead of computing.** A
  computation shortcut yielding identical bytes; no divergence.
- **The pre-trailer pad's length.** Determined once dir_offset and dir_length are:
  §6.2 plus `[R-LIF-02]` step 5, with §6.2 settling the boundary case explicitly
  ("a writer that ends its directory on a 64-byte boundary leaves none").

Every divergence in my catalogue is classified as legitimate-and-closed,
legitimate-and-open (#16), or forbidden. I found none I could not classify.

**Item-by-item pass over Appendix G's numbered list.**

1. Codec — closes #12, and §17.2's Note explicitly hands DEFLATE's final-byte
   unused bits to it. Sound. The item is honest that byte-identity across
   *implementations* is unattainable for codecs 2–4.
2. `file_id` — closes #5. I checked the derivation for internal consistency: the
   input is "[0, F − 64) followed by the trailer's first 60 bytes with the
   `file_id` field zeroed", which is well founded because those 60 bytes contain
   dir_offset, dir_length and committed_file_length, all fixed by item 3 before
   the hash is taken, and the trailer CRC is not in the input (it is bytes
   [60,64), computed after). No circularity. The "last eight bytes in output
   order" wording, and its explicit refusal of the word "low", is a good call. The
   compactor carve-out is right: `[R-WRT-06]` demands "a new draw … not merely a
   value compared against the input's", and re-deriving on an already-compact
   input would reproduce the input's identifier.
3. Emission order — closes #1, #2, #3, #4. I executed it and it is
   implementable. The ordering key ("the record's header with **extent_offset
   masked to zero**, then its inline payload, then the contents of its extent") is
   non-circular, and I verified its closing claim: two records the key does not
   separate agree in type, flags, inline_length, extent_length, inline payload and
   extent content, so swapping them permutes only which identical extent sits at
   which offset — the file's bytes are unchanged. The claim holds.
4. One generation — closes #6. Mild unremarked tension with `[R-LIF-07]`'s SHOULD
   to emit checkpoint commits during very large writes; since the profile "adds no
   requirement to any actor" this is a choice, not a conflict. Not filed.
5. Alignment and slab — closes #10, with the stated reason "both change placement
   and neither is implied by content."
6. Sentinel for every all-fill tile — closes #9.
7. All-zero fill default — closes #8, and item 7 correctly notes it reaches
   further than eight bytes of layer record, because item 6 makes fill decide
   *which tiles exist*.
8. `version_minor` and flags — closes #7.
9. User metadata — closes #14, #15.
10. NFC names — closes #11, with the correct observation that it changes
    `inline_length` and `dir_length`, not just the name.

**The gap:** the **filter** is a layer declaration that changes the stored bytes of
every tile and the two bytes of the filter field, is not implied by content, and
is fixed by no item. Concretely, my `sst` tile 0 stores
`00 00 01 00 02 00 03 00 04 00 05 00 06 00 07 00 08 00 09 00 0a 00 0b 00 0c 00 0d
00 0e 00 0f 00` under filter 1 and
`00 01 02 03 04 05 06 07 08 09 0a 0b 0c 0d 0e 0f 00 ×16` under filter 2, with
entry crcs 0xF3108B26 and 0xA3A2B9CF. Same decoded image, same reference array,
same decoded size, both conforming, and both satisfy every one of items 1–10.
That falsifies the closing paragraph's "Everything else the profile needs is
already mandatory." Filed as **writer-03**.

I also considered and did **not** file: a writer that stamps `tarn.created` or
`tarn.creator` from the clock defeats reproducibility, and item 9 pins the
serializer but not the content. I classify document *content* as caller input
rather than a writer degree of freedom, which makes this legitimate and outside
the profile's remit — though `tarn.created` is by nature writer-generated and an
implementer adopting the profile should be told to take it from the caller.

---

## 7. Findings

### writer-01 — CONTRADICTION — §21.7 vs §20.3 step 4 and §21.4's T14/T17

**Location:** §21.7 `[R-ERR-01]`; §20.3 step 4 `[R-WRT-04]`; §21.4 rows T14, T17, T3.

§21.7 states:

> §20.3 step 4's bar on a declaration change is witnessed only where
> the affected tiles remain stored *and* the change reaches a byte §14
> structurally constrains — a padding position, a pad bit, or a boolean
> byte — the §21.4 rows firing there and nowhere else

But §20.3 step 4 lists, among what the bar covers:

> the set of padding positions (§11.3) and the content `[R-SER-05]` fixes
> there, the decoded size, the byte offset of any sample within the decoded
> tile image, or the codec and filter that produced the stored bytes.

Two of those four — the decoded size and the codec — are witnessed by §21.4 rows
that have nothing to do with a structurally constrained byte.

*Counterexample 1 (codec).* Layer: rank 1, dim `x` with E = 8, T = 4,
interleaved, one uint16 channel, codec 1, filter 1. G = ⌈8/4⌉ = 2, G·T = 8 = E,
so **zero padding positions**, no bool channel, hence no pad bits. Both tiles
stored, 8 bytes each; tile 0's stored bytes are `00 00 01 00 02 00 03 00`. A
commit changes only the codec field, 1 → 3. entry_count, the index bytes and the
geometry are untouched, so this is §20.3's shape (c), a change confined to the
directory. §20.3 step 4 bars it ("the codec … that produced the stored bytes").
The witness is **T17** — "Codec 3 (zstd) and the stored bytes do not begin with
the compressed-frame magic 28 B5 2F FD" — detector *reader*, at tile use.
T2, T4 and T5 cannot fire: there is no padding position, no pad bit, and no
boolean byte anywhere in the layer.

*Counterexample 2 (decoded size).* Same layer; a commit changes T from 4 to 8.
New G = ⌈8/8⌉ = 1, still no padding. entry_count 2 → 1, so the index is re-emitted;
the new entry 0 carries the old tile 0's extent, length 8. The layer passes §19.3
(entry_count 1 = N 1; extent_length 24 = 1×20 + ⌈1/2¹⁶⌉×4). Under codec 1,
**T14** fires — "Codec 1 (none) declared and a non-sentinel index entry's length
differs from the tile's decoded size" — 8 ≠ P·Q = 16, again reader, tile use,
again with no structurally constrained byte in sight. Under a compressing codec
the same change is witnessed by **T3** instead.

The clause that *is* accurate is the one about the **filter**: a mis-strided or
changed filter over a tile with no padding, no pad bit and no bool leaves the
decoded size intact and is genuinely undetectable, which §21.7 says correctly
elsewhere and §21.4's T26 registers on the same terms. The sentence generalises
that filter-only truth over "codec and filter" and over the decoded size.

**What an implementer does wrong without it:** nothing to a byte — see below. The
cost is to the register's own audit. §21.1 makes §21.2–§21.5's completeness
normative and §21.7 is the account of what fails detectability; a reviewer
checking that §20.3 step 4 needs no row of its own is told the answer is
"T2/T4/T5 and nothing else", and will not look for the codec and decoded-size
witnesses that actually carry it. It also understates the bar's detectability,
which is the opposite of the safe direction for a document that elsewhere works
hard to say exactly what no check catches.

**Byte-level: no.** T14, T17 and T3 are registered, unchanged, and reader-detected
either way; every reader and verifier behaves identically before and after the
correction. No byte a writer may emit and no verdict a reader must return moves.

---

### writer-02 — AMBIGUITY — §20.3 step 4's shrink clause states a permission whose premise can be false

**Location:** §20.3 step 4, `[R-WRT-04]`.

> An extent MAY also **shrink**. Where the shrink leaves a stored tile addressed
> it is the case above — barred wherever it alters what §14 fixes for that
> tile — but where it drops a tile out of the addressed set entirely (§11.2's
> grid count falls), nothing is altered for a tile the new state stores, and the
> commit is permitted

A single shrink can satisfy both clauses at once, and when it does the second
clause's premise is false.

Take my `sst` layer: dims (y, x), E = (5, 5), T = (4, 4), G = (2, 2), interleaved,
one uint16 channel with fill 0xABCD. Shrink E_x from 5 to 3. Then G_x = ⌈3/4⌉ = 1,
so the two tiles at t_x = 1 **drop out of the addressed set** — the second clause's
antecedent holds. But the surviving tiles at t_x = 0 still span x ∈ [0,4), and
x = 3 is now ≥ E_x = 3, so **x = 3 becomes a padding position in a tile the new
state stores**. `[R-SER-05]` requires that position to hold the recorded fill
`CD AB`; my stored tile 0 holds `06 00` there. So the assertion "nothing is
altered for a tile the new state stores" is false for this shrink, and the flat
"the commit is permitted" that rests on it is unsafe.

**Permitted readings.**

(a) *Per-commit.* The two clauses classify commits. A shrink that drops any tile
falls in the second and is permitted. Under this reading my example commits, and
the resulting file exhibits T4 at tile 0 (reject-tile at certification).

(b) *Per-tile.* The clauses classify *tiles*: for each tile the shrink leaves
addressed, the general test governs; for each tile it drops, nothing is owed. The
commit is permitted iff no surviving stored tile is altered. Under this reading my
example is barred and belongs to "a new layer, or a whole-file rewrite under a
fresh file_id".

**I picked (b).** It is the only reading that survives contact with the general
test stated three sentences earlier — "The test is the effect on such a tile, and
the list names where that effect arises rather than standing on its own" — and it
is the only one under which the emitted file is conforming. Reading (a) is
available only because the sentence asserts its conclusion flatly rather than
conditioning it on the surviving tiles.

**What an implementer does wrong without it:** builds a shrink path that checks
only "did a grid count fall?" and commits a file with a non-fill byte at a
newly-created padding position. It will pass every reader (T4's detector is the
verifier) and fail certification.

**Byte-level: no.** The two readings differ over whether a commit may be emitted,
but reading (a)'s output is unambiguously nonconforming under `[R-SER-05]`/T4, and
`[R-CNF-06]` binds an updater to "every writer requirement for the bytes it
produces". A competent implementation that checks its own output against T4
converges on (b) regardless of how it read this sentence, so no verdict and no
permissible byte sequence is actually in dispute — the defect is that the text
points a careful implementer at the wrong test, not that it leaves the bytes open.

---

### writer-03 — CONTRADICTION — Appendix G leaves the filter open while claiming everything else is mandatory

**Location:** Appendix G, closing paragraph and item 5; §17.3 `[R-COD-09]`.

Appendix G's closing paragraph:

> Everything else the profile needs is already mandatory — fill-encoded
> edge padding (`[R-SER-05]`) and explicitly recorded fill (`[R-TYP-06]`) among
> them. The items above add what is not

and item 5, which is the profile's own statement of the test it applies to a layer
declaration:

> 5. **No declared alignment and no slab**, or fixed declared values —
>    both change placement and neither is implied by content.

The filter meets item 5's test exactly — it changes bytes and is not implied by
content — and is fixed by no item. The word *filter* does not occur in Appendix G
at all. §17.3 assigns both values and prefers neither: "1 = none — the filtered
image is the decoded image — and 2 = byte-shuffle, defined below, are assigned,
and both are **core**".

Demonstration, using my `sst` tile 0 (16 uint16 values 0…15, interleaved, C = 1,
so shuffle stride s = Q = 2, n = 16):

```
filter 1 stored: 00 00 01 00 02 00 … 0e 00 0f 00      entry crc F3108B26
filter 2 stored: 00 01 02 … 0e 0f 00 00 … 00 00       entry crc A3A2B9CF
layer record filter field:  01 00   vs   02 00
```

Identical input array, identical stated options, identical decoded image,
identical reference array, both conforming, both satisfying items 1–10 — and
different bytes in every stored tile, every index entry crc, the layer record, and
therefore the directory CRC and the trailer CRC. Two writers that both claim the
profile produce different files.

**Which reading I picked, and why it does not rescue the item.** One could argue
the filter is a *stated option* supplied by the caller, so the profile need not
close it. But item 5 forecloses that: alignment and slab are equally layer
declarations a caller may not have specified, and the profile pins them anyway on
exactly the "not implied by content" ground the filter also meets. Item 1's
alternative form — "**Codec 1 (none), or** a named codec implementation…" — also
treats the choice of codec *value* as within the profile's scope. The filter is
the one such declaration left out.

The fix is one clause in item 1 or a new item; the point of reporting it is that
the closing paragraph claims completeness the list does not have.

**Byte-level: no.** Appendix G is "non-normative" by its own heading and "adds no
requirement to any actor: a writer ignoring it is fully conforming". Both filter
values are conforming with or without the repair, so no conforming implementation's
permitted output changes. It is a falsifiable claim in the reproducible-writer
material, which is what makes it reportable.

---

### writer-04 — OBSERVATION — `[R-WRT-06]` lists the same alternative twice

**Location:** §20.5, `[R-WRT-06]`.

> A compactor MUST refuse to compact when any check `[R-WRT-09]`
> obliges fails, and MUST NOT emit a file carrying a violation it has
> detected: it can neither re-emit the structure corrected
> (`[R-WRT-05]`), nor keep it and call the output clean — and a record
> §20.4 does let it drop is no exception, dropping being available
> only where that table licenses it —
> nor re-emit it corrected (`[R-WRT-05]`).

The "neither … nor … nor" list has three limbs and the first and third are the
same proposition with the same citation: *re-emit the structure corrected*
(`[R-WRT-05]`) and *re-emit it corrected* (`[R-WRT-05]`). This is the signature of
an em-dash aside being inserted mid-sentence without the trailing clause being
deleted. Under every antecedent I can assign to "it" — the structure, or the
droppable record the aside just named — the third limb is subsumed by the first.

I report it because §20.5 is normative text and this is the sentence that tells a
compactor implementer the exhaustive set of things it may not do with a detected
violation; a reader counting the alternatives will look for a distinction that is
not there.

**Byte-level: no.** Purely editorial. The rule's content — refuse, do not correct,
do not launder, do not drop your way out — is unchanged under any reading, and no
byte or verdict depends on it.

---

### writer-05 — AMBIGUITY — §20.4: does modifying a layer record change "the file's layer set"?

**Location:** §20.4, `[R-WRT-05]`'s table, the MU = 0 / PE = 0 row.

> An appender may drop it only in a commit that *independently* changes the
> scope the record attaches to: for a layer sub-record, that layer's record,
> the entry set of its index, or which of its tiles are stored; for a
> top-level record, the file's layer set or another *non-layer* top-level
> record.

Building the updater, I had to decide whether a commit that **renames a layer** —
or otherwise modifies an existing layer record without adding or removing a
layer — licenses dropping a top-level MU = 0 / PE = 0 ancillary record.

**Permitted readings.**

(a) "the file's layer set" = which layers the file has. A rename does not change
it, so the ancillary must be retained.

(b) "the file's layer set" = the set of layers *as declared*, names included. A
rename changes it, so the ancillary may be dropped.

**I picked (a),** on the parallel construction. The sub-record list distinguishes
"that layer's record" from "the entry set of its index" from "which of its tiles
are stored" — three separate triggers, one of which is precisely "the layer record
changed". For the top-level list the drafters wrote "the file's layer set" and
*not* "any layer record", which reads as a deliberate contrast: a top-level
ancillary attaches to the file, and only a change to which layers exist (or to
another non-layer top-level record) is a change to that scope.

Two neighbouring cases the same phrase leaves me deciding: whether **adding** a new
non-layer top-level record counts as changing "another non-layer top-level record"
(singular, so I read: no — only modifying an existing one), and whether the
one-way anti-bootstrap clause covers it (it covers dropping, explicitly: "a commit
whose only effect would be the drop MUST retain it").

**What an implementer does wrong without it:** drops an application's ancillary
record in a rename-only commit, silently losing application state that
`[R-WRT-08]` and the row's own SHOULD-report exist to protect. The loss is
undetectable afterwards — no single file witnesses whether a record was dropped or
was never there, which is why this cannot be a register row.

**Byte-level: no.** The two readings do produce different directory bytes, and both
outputs are conforming with no witness, so nothing downstream corrects the choice.
But I judge that a competent implementer reading the two lists side by side lands
on (a): the contrast between "that layer's record" in one list and "the file's
layer set" in the other is doing deliberate work, and reading (b) makes the
sub-record list's first trigger redundant with the top-level list's first. I flag
it because it is the single place in the flag matrix where I had to reason rather
than read, not because I think the bytes are genuinely open.

---

### writer-06 — OBSERVATION — §11.1's Rationale overstates disk-ordinal renumbering on growth

**Location:** §11.1, the Rationale following `[R-GEO-02]`.

> growth that raises one changes entry_count and with it
> extent_length (`[R-CNT-17]`), so the layer's whole tile-index region
> is re-emitted and disk ordinals renumber (§20.3, `[R-WRT-04]`,
> `[R-GEO-06]`)

For an interleaved layer, growth that raises the grid count of any dimension
**other than the last-declared** renumbers nothing. `[R-GEO-06]` gives
s = Σᵢ tᵢ · ∏_{j>i} Gⱼ, and G_y does not appear in its own coefficient. Concretely,
with dims (y, x), E = (5,5), T = (4,4), G = (2,2): s = t_y·2 + t_x. Grow E_y to 9;
G becomes (3,2), entry_count 4 → 6, the region is re-emitted — and tile (0,0)→0,
(0,1)→1, (1,0)→2, (1,1)→3 exactly as before, with the two new tiles appended at
ordinals 4 and 5. No existing entry moves.

The claim is true for a **planar** layer (disk ordinal c·N + s, and N changes, so
every channel block above c = 0 shifts) and true for growth along the last-declared
dimension. It is false in general, which is why §20.3 step 4's own parenthetical is
correctly hedged — "(a geometry change renumbers ordinals wherever `[R-GEO-06]`
moves them)" — and the Rationale is not.

**What an implementer does wrong without it:** nothing, if they compute
`[R-GEO-06]`. The risk is an appender that treats "entry_count grew" as "rebuild
the ordinal mapping from scratch" and gets the coefficient order wrong; the
Rationale encourages exactly that framing.

**Byte-level: no.** §2.1 excludes text "labeled *Note*, *Example*, or *Rationale*"
from the normative document, so this sentence binds nobody, and `[R-GEO-06]`'s
formula decides every ordinal unambiguously. A charitable reading of "renumber" as
"the mapping is recomputed" also survives; I report it because in a section the
repair pass touched, a hedge that the normative text got right was dropped in the
Rationale that summarises it.

---

## 8. Things I checked and did not file

Recorded so the next round need not redo them.

- **§21.8's arithmetic.** I parsed all 121 register rows and counted their
  Instances cells under §21.1's stated criterion (a cell reading `—` is one
  instance, otherwise semicolon-separated). F: 36 rows / 58; L: 49 / 116;
  T: 26 / 57; R: 10 / 44. **121 rows, 275 instances** — exactly what §21.8 claims.
  I also spot-checked the criterion's application on ~40 rows: the
  magnitude-direction rule (T3, T14, T22, L21, L22, L30, F17, F23 all enumerate
  two directions; T21, L44, F5, F16, F9 enumerate one, matching *exceeds* /
  *larger than* / *below*), the no-ordering rule (every checksum and constant
  comparison at 1 — L37, L38, T1, F14, F20, F8), the nonzero-value-test rule
  (L20, L28 at 1), the single-predicate rule (F25, F26 at 1, against L46, L47 at
  2 on the container axis), and the family rule (T24 *any codec* at 1 vs T25 at
  3, both blessed by name in §21.1). I found no cell that misapplies it.
- **Requirement identifiers.** No numbering gaps in any prefix; every prefix
  declared in §2.2 is used and none is used undeclared; `[R-SER-04]` occurs once,
  in its own withdrawal Note, as §2.2 requires; `[R-ENC-100]` is §2.2's own
  illustration, not a live requirement.
- **§21.2's preamble** on which rows reach a foreign-major file. The reasoning is
  sound: §6.2 orders magic → CRC → version gate → everything else, so F5, F9–F13,
  F15–F17 and the rest are unreachable, while F8, F14 (before the gate) and F6
  with F1's front-block instance (`[R-CNT-04]`, "before other processing") are.
  Four rows named, four rows counted. `[R-CNT-27]`'s 128-byte floor is
  format-major-1 reasoning and correctly does not reach such a file, which is why
  F5 is on the unreachable side.
- **`[R-COD-06]`'s zstd window rule** and its Note about RFC 8878's two
  derivations. I worked it: Single_Segment_Flag ⇒ no Window_Descriptor ⇒
  Window_Size = Frame_Content_Size, which the rule already pins to the decoded
  size; without it, the Window_Descriptor's floor is 1 KiB, so a sub-1-KiB tile is
  encodable only single-segment. The Note is correct and the small-tile
  consequence is real — §14.2's own examples (18 and 30 bytes) and §14.3's (2
  bytes) all fall under it.
- **`[R-SER-08]`'s "sole resolved byte" claim.** Asserted in four places (§12.3,
  §14.2, §21.1, Appendix H) and consistent in all four.
- **§16.2's packing invariant** is decidable from index entries alone given F, as
  it claims: sentinels and structurally-rejected entries are transparent, an entry
  failing only its stored bytes' crc is not, and my reader implements exactly that
  and accepts my slab layer.
- **`[R-CNT-21]`'s partial-total bound** is genuinely an upper bound (§4 above).
- **Record reserved flag bits 2–15** are not one of §10.1's four growth vehicles,
  so a modified record may zero them without losing anything a later minor version
  could have meant — unlike the trailer's ignore-lane bits, which `[R-CNT-08]`
  requires an updater to copy forward. The asymmetry is correct.
- **`[R-LIF-02]`'s "in order" over steps 1–3** is unobservable (the step-4 barrier
  makes them durable together), a mild tension with §2.1's Note about not
  constraining technique. Not a defect: no byte or verdict turns on it.
- **Compaction leaves slack** when a layer declares alignment (962 bytes in my
  compacted output). Permitted and correct; §20.5's figure just doesn't draw it.
- **`tarn.created` under Appendix G**: a clock-stamped key defeats reproducibility
  and item 9 pins the serializer, not the content. I classify document content as
  caller input, so this is legitimate and outside the profile — but an implementer
  should be told to take it from the caller.

## 9. Confidence

I would implement a conforming creator, appender, updater and compactor from this
document alone, and I did — three files, read back by an independent reader that
re-derives everything. Every constant, every worked example and every piece of
arithmetic I could check reproduced exactly, and the two hardest parts to get
right from prose — the packed inline payload of §7.4 and the index/segment/CRC
chain of §15 — are worked in the document to the byte.

The one place the document sent me somewhere I would have had to correct myself is
writer-02's shrink clause; the one place it left a genuine choice unresolved is
writer-05; and the reproducible-writer profile has one open degree of freedom
(writer-03). None of the six findings changes a byte a conforming implementation
may emit or a verdict it must return, and I have said so for each rather than
rounding upward.
