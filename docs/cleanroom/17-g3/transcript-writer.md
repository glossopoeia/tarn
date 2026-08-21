# Cleanroom round 17 — Writer/updater implementer transcript

**Access disclosure.** I read exactly one file: `/Users/robertkleffner/Documents/GitHub/tarn/spec/tarn.md`,
all 4,317 lines, in five `Read` calls plus two `grep` runs against the same file
(`grep -n "riters\? \(MUST\|SHOULD\|MAY\|SHALL\)\|A writer\b\|An updater\|..."` and
`grep -n "conduct"`). I opened no ADR, no `PLAN.md`, no `AGENTS.md`, no `conformance/`
artefact, no `spec/registry.json`, no git history. I ran no web search or fetch.
I ran four local Python scripts I wrote myself, reading no repository file except
that one via the grep/read path above; they live in a scratch directory I created
(`…/scratchpad/wtmp/`) and they read only their own outputs. I did not read or list
the round17 output directory.

---

## 0. How I worked

I implemented a creator, an appender, and (on paper) a compactor. Every number
below I computed rather than copied. Where the document told me what to do I say
so; where I had to choose I say what I chose and on what authority; where I could
not decide I stopped and wrote a finding.

Before building anything I checked the document's own published constants, because
a writer that gets the checksum wrong gets every structure wrong:

```
CRC-32C("123456789")                  -> 0xe3069283   §4.5 check vector      ✓
CRC-32C(<zero bytes>)                 -> 0x00000000   §4.5 check vector      ✓
CRC-32C(2^16 sentinel entries)        -> 0xeecb3bb2   §15.4 / Appendix B     ✓
CRC-32C(4 sentinel entries, 80 bytes) -> 0x80a34955   §7.4 worked example    ✓
CRC-32C(that 4-byte array)            -> 0xc4ee982e   §7.4 worked example    ✓
CRC-32C(Appendix A trailer[0,60))     -> 0xe00938d2   Appendix A             ✓
```

`[R-IDX-05]`'s licence to emit `0xEECB3BB2` for a full all-sentinel segment
"without computing it" is a byte-level licence — a wrong constant would fork the
bytes between a writer that takes the shortcut and one that does not. It is right.
So is §7.4's whole 81-byte layer-record example: I rebuilt it field by field and
got 4 + 34 + 18 + 12 + 13 = 81 with no residue, and both CRCs.

I also re-derived every worked example in §11.2, §11.4, §14.2, §14.3, §14.5,
§15.4, §16.2 and §17.3. All of them are correct, including the byte-shuffle
example (`00 00 00 00 00 00 80 00 40 3F 40 40` for 1.0/2.0/3.0 float32 at s=4,
n=3) and the packed-plane example (`55 01` with fill false, `55 FD` with fill
true). And I re-derived §21.8's arithmetic mechanically from the register tables:
**121 rows over 273 instances**, matching `[R-ERR-02]` exactly
(F 36/58, L 49/116, T 26/55, R 10/44).

That is a lot of arithmetic that is right. The findings below are not about
arithmetic.

---

## 1. Creation: a file, end to end

### 1.1 What I decided to build

Two layers plus a file-scope user-metadata record. Nothing exotic, but enough to
exercise both layouts, a packed boolean plane, an edge tile with padding, a
sentinel, and an extent-bearing ancillary.

- **Layer `mask`** — planar (`layout = 2`), rank 1, dimension `i` with E=10,
  T=8. G = ⌈10/8⌉ = 2, N = 2, C = 1, so the addressed-tile count is C·N = 2
  (`[R-GEO-03]`). One bool channel `m`, fill `0x00`. Codec 1, filter 1, no
  alignment, no slab. P = ∏Tᵢ = 8, so each plane's decoded size is ⌈P/8⌉ = 1 byte
  (`[R-SER-03]`). Tile 1 covers positions 8–15; 8 and 9 are real, 10–15 are
  padding positions, and `[R-SER-05]` fixes them to the fill bit 0. P mod 8 = 0,
  so there are no *pad bits* — §14.3's Note is worth having read, because I first
  reached for the pad-bit rule when the padding-position rule was the one that
  applied.
- **Layer `sst`** — interleaved (`layout = 1`), rank 2, dimensions `y`, `x` each
  E=4, T=2. G = (2,2), N = 4, addressed-tile count N = 4. Channels `temp`
  (float32, fill `0x7FC00000` — §12.3's exact twelve bytes) and `flag` (uint8,
  fill `0x00`). Q = 4 + 1 = 5, P = 4, decoded size P·Q = 20. G·T = E on both
  axes, so no padding positions. Disk ordinals 0 and 3 stored; 1 and 2 sentinel.
- **One top-level user-metadata record**, encoding 1 (none), document
  `{"tarn.creator":"tarnwrite/0.1","tarn.title":"demo"}`, 52 bytes, plus its
  terminal CRC-32C = 56-byte extent. Keys are sorted ascending by UTF-8 bytes
  (`"tarn.c…" < "tarn.t…"`) per `[R-MTA-05]`.

### 1.2 Decisions the document fixed for me

| Decision | Fixed by |
|---|---|
| Bytes [0,16) = `89 54 41 52 4E 0D 0A 1A` + eight zero bytes | §6.1, no discretion |
| Writing begins at offset 16 on creation | `[R-LIF-02]` creation path |
| Layer record flags = `0x0003` (MU=1, PE=1); user-metadata flags = `0x0002` | §7.3 table + `[R-CNT-22]` |
| Index region = entry_count × 20 then ⌈entry_count/2¹⁶⌉ × 4, contiguous, no padding | `[R-IDX-01]` |
| Layer extent_length = entry_count × 20 + ⌈entry_count/2¹⁶⌉ × 4 | `[R-CNT-17]` |
| Sentinel = `FF ×16 00 ×4` | `[R-IDX-02]` |
| Codec 1 ⇒ entry length **equals** decoded size | `[R-COD-04]` |
| Padding positions carry fill | `[R-SER-05]` |
| Directory last, nothing between its end and the trailer | `[R-CNT-05]` |
| Pad to the next 64-byte boundary, then the trailer | `[R-LIF-02]` step 5 |
| `generation = 1`, `flags = 0`, reserved bytes zero, `file_id ≠ 0` | `[R-CNT-06]`, `[R-CNT-08]` |
| Both barriers, steps 4 **and** 6 | `[R-LIF-02]`, restated by `[R-WRT-02]` |

### 1.3 Decisions the document left to me

`[R-SLB-05]` is explicit that placement and ordering are free, and `[R-CNT-14]`
that record order carries no meaning. So I had to choose:

1. **Emission order of structures.** I adopted Appendix G item 3's total order to
   test it: layers in ascending layer-name byte order (`mask` = `6D 61 73 6B`
   before `sst` = `73 73 74`), each layer's stored tiles in disk-ordinal order,
   then its tile-index region; then non-layer record extents in record order;
   then the directory.
2. **Record order in the directory.** Appendix G item 3 again: by type, so the
   two `0x0001` records (by layer name) then the `0x0002` record.
3. **Gap content.** Zeroed, per `[R-CNT-03]`'s advice (a SHOULD; Appendix G item
   3 makes it a requirement).
4. **`file_id`.** I picked a fixed nonzero 64-bit value. `[R-LIF-03]` only
   SHOULDs a cryptographic source.
5. **`version_minor` = 0.** `[R-CNT-26]`'s floor, a SHOULD.
6. **Whether to store tiles 1 and 2 of `sst`.** Nothing obliges either way;
   sentinels are what `[R-TYP-08]` defines them as. Appendix G item 6 would force
   the sentinel for an all-fill tile; I stored data in 0 and 3.

### 1.4 The bytes

```
  [    0,    16)  len   16  front signature block
  [   16,    17)  len    1  mask tile, disk ordinal 0   (0xFF: eight true)
  [   17,    18)  len    1  mask tile, disk ordinal 1   (0x01: true,false + 6 padding = fill 0)
  [   18,    62)  len   44  mask tile-index region      (2×20 + 4)
  [   62,    82)  len   20  sst tile, disk ordinal 0
  [   82,   102)  len   20  sst tile, disk ordinal 3
  [  102,   186)  len   84  sst tile-index region       (4×20 + 4)
  [  186,   242)  len   56  user-metadata extent        (52-byte doc + CRC)
  [  242,   503)  len  261  directory region            (100 + 132 + 25 + 4)
  [  503,   512)  len    9  pre-trailer pad  -- SLACK
  [  512,   576)  len   64  trailer
                            F = 576, F mod 64 = 0
```

`mask` inline_length = 76, `sst` inline_length = 108, user-metadata
inline_length = 1. Directory = (24+76) + (24+108) + (24+1) + 4 = 261.
`dir_offset` = 242 ≥ 16 ✓, `dir_length` = 261 ≥ 4 ✓,
`dir_offset + dir_length` = 503 ≤ F − 64 = 512 ✓.
§6.4's SHOULD: 261 + 9 + 64 = 334 ≤ 65,536 ✓.

The head of the file, verbatim:

```
0000  89 54 41 52 4e 0d 0a 1a 00 00 00 00 00 00 00 00
0010  ff 01 10 00 00 00 00 00 00 00 01 00 00 00 00 00
0020  00 00 00 00 00 ff 11 00 00 00 00 00 00 00 01 00
0030  00 00 00 00 00 00 52 d0 16 a0 94 15 67 26 00 00
```

Byte 0x10 is `mask`'s first tile — a one-byte stored extent at offset 16, the
lowest offset `[R-IDX-03]` admits. Bytes 0x12–0x39 are `mask`'s two index
entries; the entry at 0x12 reads offset 16, length 1, crc `0x94A016D0`. Bytes
0x3A–0x3D are the single segment CRC, and `0x1526…` — no, the segment CRC is
`52 d0 16 a0`… I had to recheck this: the region is entries *then* the CRC array,
so bytes [18,58) are the two entries and [58,62) the one segment CRC. The layout
table in §15.1 is unambiguous about that and I had it right in code; I mis-read my
own hexdump the first time, which is a fact about me and not about the document.

And the trailer:

```
0200  8a 4e 52 41 54 0d 0a 1a 01 00 00 00 00 00 00 00
0210  01 00 00 00 00 00 00 00 f2 00 00 00 00 00 00 00
0220  05 01 00 00 00 00 00 00 40 02 00 00 00 00 00 00
0230  81 06 d5 b3 e2 17 4a 9c 00 00 00 00 ac b5 14 f8
```

magic; version_major 1; version_minor 0; flags 0; generation 1; dir_offset
0xF2 = 242; dir_length 0x105 = 261; committed_file_length 0x240 = 576; file_id;
four reserved zeros; trailer CRC `0xF814B5AC` over [0,60).

I then ran §19.1's four-step open and §9.7's coverage walk against my own output
as an independent reader. It opens, every checksum verifies, the claimants are
pairwise disjoint and all inside [16, F−64), and the slack total is **9** — the
pre-trailer pad, exactly as §5.1's 128-byte example predicts its own 44.

**Nothing in creation forced me to guess.** The one place I had to read twice was
§14.3 versus §14.5 (pad bits versus padding positions), and §14.3's Note is there
precisely for that; it did its job.

---

## 2. The append procedure

### 2.1 Commit 2 — add a layer

New layer `zed`: interleaved, rank 1, dimension `k` with E=3, T=4. G = ⌈3/4⌉ = 1
(§11.1 explicitly blesses T > E), N = 1, entry_count = 1. One uint16 channel `v`,
fill `0xFFFF`. P = 4, Q = 2, decoded size 8. Positions 0–2 real, position 3 is a
padding position and carries `FF FF` per `[R-SER-05]`.

`[R-LIF-02]`, in order:

1. Begin at exactly F = 576. (`[R-LIF-04]` first: validate the trailer at the
   physical end; it validates, so F = 576 and the physical length equals it, so
   no truncation is owed.)
2. `zed` tile → [576, 584); `zed` index region → [584, 608).
3. New **complete** directory at 608, length 361: the `mask`, `sst` and
   user-metadata records re-emitted **byte-identically** — header, inline payload
   and extent slot (`[R-WRT-05]`) — plus the new `zed` record. `mask`'s slot still
   reads (18, 44) and `sst`'s still (102, 84): §20.3 step 4 is explicit that a
   layer the commit does not touch keeps its extent slot pointing where it always
   pointed, and that relocating a live index region "is compaction's operation …
   not an appender's".
4. **Barrier.**
5. Pad 55 bytes to 1024, trailer at 1024, generation 2, same file_id,
   committed_file_length 1088.
6. **Barrier.**

Appended: 512 bytes. Slack after: 389 = 9 (gen-1 pad) + 261 (gen-1 directory) +
64 (gen-1 trailer) + 55 (gen-2 pad). The commit's slack cost is sized by the
file's *layer count*, never by any layer's data — §20.3's figure (a) says exactly
this and it is what I measured.

### 2.2 Commit 3 — supersede one stored tile

Supersede `sst` disk ordinal 3. §20.3 step 4: the layer's whole tile-index region
is re-emitted — entry 0 byte-identical at its disk-ordinal position, entries 1
and 2 still the sentinel, entry 3 re-pointed — necessarily at a new placement,
because `[R-LIF-01]` freezes the old one.

```
  new payload      [1088, 1108)   20 bytes
  new index region [1108, 1192)   84 bytes  (the whole region for one changed entry)
  new directory    [1192, 1553)  361 bytes
  pad              [1553, 1600)   47 bytes
  trailer          [1600, 1664)   64 bytes
```

Slack after: 965. The old payload (20) and the old index region (84) joined it,
along with gen-2's directory, pad and trailer. §20.3's Note — "a commit's cost is
dominated by its index, not its data" — is visible even at this toy scale: 84
bytes of index for 20 bytes of data.

**The thing to notice, because §3 turns on it:** superseding one tile changed the
`sst` layer record in two places. Its extent_offset went 102 → 1108, and its
`crc_of_crc_array` changed because the segment CRC over the re-emitted entries
changed. Header *and* inline payload both differ from generation 2's, byte for
byte. Under `[R-WRT-05]` that record is "a record it modifies", i.e. new output.

### 2.3 Write order, durability, and the commit point

The commit point is **step 6**: the moment the new trailer is durable. Before it,
the previous generation is the live one and is byte-intact. What must be durable
before what:

- everything in steps 1–3 (payloads, index regions, record extents, the complete
  directory and its CRC) must be durable **before** the trailer is written —
  that is step 4's barrier;
- the trailer must then be durable — step 6's barrier.

`[R-WRT-02]` says "both barriers, not one", and the reason is visible in §9.2's
crash figure: with only the second barrier, a reordering store could land the
trailer while the directory it addresses is still in flight, and the file would
be *silently* wrong rather than loudly torn. §9.2's Note prices the weaker case
honestly: "safety degrades from 'torn commits are invisible' to 'torn commits are
detected'".

One ordering trap the document states but buries: if the physical file is longer
than F (residue from an abandoned attempt) and the writer takes `[R-LIF-04]`'s
*overwrite* branch rather than its *truncate-first* branch, the truncation to the
new committed_file_length must happen "no later than step 6" — i.e. **before**
the trailer becomes durable, not after. Get that backwards and every reader sees
F17 (committed_file_length ≠ transport size) on a file whose commit actually
completed. I took the truncate-first branch; it is strictly simpler and the
document permits it.

### 2.4 Appending to a file whose records I do not all understand

Here is the whole flag surface. §7.2 defines the field as `bit 0
MUST_UNDERSTAND, bit 1 PRESERVE_ON_EDIT, bits 2–15 reserved`. The obligations
split three ways by *whose* flags govern (§20.4: "Persistence governs every
record type; only the authoritative source of the flags differs").

**Case A — a type §7.3 registers (0x0001 layer, 0x0002 user metadata).**
The registry's fixed flags govern, "rather than the stored ones"
(`[R-CNT-22]`, §20.4). Both registered types are PE = 1, so **neither can ever be
dropped**, at either scope. That holds for all four stored bit patterns:

| stored MU/PE on a registered type | what my updater does |
|---|---|
| 1/1 (layer, correct) | re-emit byte-identically unless logically modified |
| 0/1 (user metadata, correct) | same |
| any other combination | *still* re-emit byte-identically, wrong bits and all |

The last row is the interesting one and the document is unambiguous about it.
`[R-CNT-22]` makes a stored-flag mismatch a **verifier**-detected violation
(F28/L49); `[R-WRT-05]` obliges byte-identical re-emission of any retained record;
and §20.3 step 2 says outright that against a structure it carries forward the
appender "MUST NOT repair the defect" and "MUST NOT drop the record". So my
updater propagates a nonconforming flag byte into a new generation, deliberately,
and — §20.3 step 2 again — "SHOULD report it". I flagged nothing here; it is
coherent and it is the right answer.

**Case B — a type the updater implements that this specification does not
register.** "the definition it implements the type from supplies the flags, and
the stored bits never do". Note the hazard this creates, which the document
accepts elsewhere: §10.3 says experimental values carry **no** collision
protection, so an updater implementing experimental type `0x8001` with a private
PE = 0 semantics may drop a record that a *different* experiment wrote with PE = 1
semantics — and §20.4 explicitly disqualifies the one signal (the stored PE bit)
that would have preserved it. That is a legitimate, licensed divergence, not a
defect; I record it in the catalogue in §6 rather than as a finding.

**Case C — a type the updater does not implement.** Stored flags are
authoritative, and `[R-CNT-12]` folds MU = 1/PE = 0 into PE = 1:

| stored | top-level record | layer sub-record |
|---|---|---|
| **MU=1, PE=1** | Retain byte-identical. **No commit is available at all**: `[R-CNT-15]` makes an unimplemented top-level MU = 1 record reject-file, and the updater is a reader first. Compaction barred on the same ground (`[R-WRT-06]`). | Retain byte-identical. That layer is unmodifiable (reject-layer, `[R-CNT-18]`); **other layers stay editable**. |
| **MU=1, PE=0** | Read as PE = 1 (`[R-CNT-12]`). Identical to the row above. Also a verifier violation, F25. | Same; L46. |
| **MU=0, PE=1** | Retain byte-identical, extent content unmodified. May not be relocated by an appender at all — `[R-WRT-08]` allows relocation only "under §20.5". | Same. |
| **MU=0, PE=0** | Retain byte-identical, **or** drop under §20.4's conditional. **This is where I could not decide — see finding writer-01.** | Same, same problem. |
| **reserved bits 2–15 set** | Readers MUST ignore (`[R-CNT-12]`); verifier violation F26/L47; updater re-emits byte-identically, carrying the violation forward. | L47. |

The MU=1 top-level case deserves one more sentence, because it is the harshest
thing in the document and it is stated cleanly: §21.6 records that an
*experimental*-range record type carrying MU = 1 makes a **conforming** file that
every reader must nonetheless reject. Such a file can never be appended to and
can never be compacted, by anyone who does not implement that private type. That
is a deliberate design consequence, not a defect.

I also checked the *timing* of these detections against `[R-WRT-03]`. A top-level
unknown MU = 1 record is established at the open (§19.1 step 4). A layer
sub-record's is not — `[R-WRT-03]` requires §19.3 layer validation only "for every
layer whose record, index, or extents the commit modifies", which is exactly the
set for which the MU = 1 block matters. That composes correctly.

One equivocation I had to reason past. §20.3 step 2 exculpates the appender for
"a violation latent in a structure it **neither modifies nor relies on**" — but
`[R-WRT-03]` says re-emission "relies on every directory byte", which would put
every re-emitted record in the *relied-on* set and pull the exculpation out from
under it. §20.3 patches this by fiat in the same sentence ("which is as true of an
index entry copied to its disk-ordinal position as of a record re-emitted
byte-identically"), and the intent is unmistakable, so I did not file it. But the
word "rely" is carrying two senses — verification depth in `[R-WRT-03]`, authorship
in `[R-WRT-01]` — and I had to read the passage three times to be sure which one
applied.

---

## 3. Finding writer-01 — §20.4's drop rule contradicts itself on a constructible commit

**Kind:** CONTRADICTION. **Location:** §20.4, `[R-WRT-05]`'s table, the MU = 0 /
PE = 0 row. **Byte-level: yes.**

The row, quoted in the two parts that conflict:

> An appender may drop it only in a commit that *independently* changes the scope
> the record attaches to: for a layer sub-record, that layer's record, the entry
> set of its index, or which of its tiles are stored; for a top-level record, the
> file's layer set — which a commit changes by adding or removing a layer and
> equally by **modifying any layer's record** — or another *non-layer* top-level
> record.

> Superseding a stored tile's bytes is not such a change for either kind — it
> re-places that layer's index region (§20.3, `[R-WRT-04]`) without altering the
> scope any record attaches to — so **a commit whose only change is a supersede
> MUST retain the record**.

A supersede-only commit *does* modify that layer's record, necessarily, and I
built one to be sure. In my commit 3 the `sst` layer record's extent_offset went
**102 → 1108** and its `crc_of_crc_array` changed with the segment CRC. That is
not a matter of degree: `[R-LIF-01]` freezes the old index region where it lies,
so the re-emitted region *must* land at a new placement, so the extent slot *must*
change, so under `[R-WRT-05]` the layer record is "a record it modifies". The
inline payload changes too, because the segment CRC over the re-emitted entries
changes.

So the first clause and the second clause disagree about the same commit:

- **Reading 1 (the first clause, read literally).** Modifying any layer's record
  counts as changing the file's layer set. A supersede modifies a layer's record.
  Therefore an appender **may drop** a top-level MU = 0 / PE = 0 record in a
  supersede-only commit. And symmetrically for a layer sub-record, whose
  qualifying list opens with "that layer's record".
- **Reading 2 (the second clause).** A supersede-only commit **MUST retain** the
  record.

I picked reading 2, because it is the more specific sentence and it is the one
with a stated rationale. But reading 1 is not a strained reading; it is what the
words say, and the parenthetical was clearly written to *widen* what counts. An
implementer who takes the widening at face value and an implementer who takes the
carve-out at face value produce **different files** from the same input:

- retain → directory of 361 bytes, extent intact;
- drop → directory 28 bytes shorter (a 24-byte header plus a 4-byte inline
  payload, for the ancillary I modelled), its 24-byte extent turned to slack, and
  therefore a different `dir_offset`, a different pad length, a different
  `committed_file_length`, and a different trailer CRC.

Two entirely different byte sequences, both claiming to be the same commit of the
same file. One of the two updaters is not a conforming updater under
`[R-CNF-06]`, and the document does not say which.

The narrowest repair I can see is to say what "modifying any layer's record" means
— presumably a change to the layer's *declarations*, as distinct from the
mechanical re-pointing of an extent slot and the recomputation of
`crc_of_crc_array` that §20.3 step 4 forces on every supersede. §20.3 step 4 already
draws that distinction in its own vocabulary ("A layer whose record alone changes
keeps its extent slot"), so the vocabulary exists; §20.4 just does not use it.

---

## 4. Finding writer-02 — §20.5 tells a compactor to emit what §20.5 forbids it to emit

**Kind:** CONTRADICTION. **Location:** §20.5, `[R-WRT-06]` against `[R-WRT-07]`.
**Byte-level: yes.**

`[R-WRT-06]`:

> A compactor MUST refuse to compact when any check `[R-WRT-09]` obliges fails,
> and MUST NOT emit a file carrying a violation it has detected: it can neither
> re-emit the structure corrected (`[R-WRT-05]`), nor keep it and call the output
> clean. Dropping is the one disposal that answers, and only where §20.4's table
> licenses it … Where the table does not license a drop the compactor MUST refuse.

`[R-WRT-07]`, on regenerating a relocated tile-index region:

> an entry §15.3 classifies reject-tile on a *structural* ground is reproduced
> with its offset and length exactly as they stand, there being no live extent for
> a re-pointing to target — `[R-IDX-03]` gives such an entry no stored extent and
> no claimant in the coverage walk — and the violation travels with it into the
> output (`[R-WRT-01]`); `[R-WRT-09]`'s checks reach the index chain and each
> stored tile's entry crc, not an entry's own value domain, so such an entry is
> not one `[R-WRT-06]` obliges a compactor to refuse

Take an input file whose layer `A` has one index entry with `offset = 5`,
`length = 20`, `crc` nonzero — §15.3 row "offset < 16 (non-sentinel)", *structural*,
reject-tile, register row T8. §20.4 licenses no drop for it (it is not a record at
all). So the two rules give opposite instructions, and which one bites turns on
whether the compactor "has detected" the violation.

**It has, necessarily.** The carve-out's premise is that `[R-WRT-09]` does not
oblige an entry's-value-domain check. But `[R-WRT-09]` *does* oblige "each
relocated extent's checksum, including every stored tile's entry crc" — that is
§19.4 step 5 — and §19.4 step 5 is reached only through step 4, which is
`[R-IDX-03]`'s classification. The compactor cannot know which entries have a crc
to verify without classifying every entry, and it cannot obey `[R-WRT-07]`'s own
instruction — reproduce *this* class of entry verbatim, re-point *that* class —
without naming the class. `[R-WRT-07]` asks the compactor to make exactly the
determination whose absence is the carve-out's justification.

Note also that the two escape routes both lead back to refusal. If the compactor
declines to classify and treats the entry as a live extent, it tries to verify a
crc over bytes at [5, 25) — inside the front signature block — and that check
fails, which trips `[R-WRT-06]`'s *first* limb ("MUST refuse to compact when any
check `[R-WRT-09]` obliges fails"). If it does classify, it has detected, and the
*second* limb bites. The carve-out disposes of the first limb only.

The fork, named concretely: **compactor A** reads `[R-WRT-06]` and refuses,
emitting no output and reporting the input as nonconforming. **Compactor B** reads
`[R-WRT-07]` and emits a compacted file in which entry k reads `offset = 5,
length = 20` verbatim beside relocated siblings. Whether B's output bytes may be
emitted by a conforming updater at all is what the document does not settle. I
implemented A, because a tool that knowingly writes a file it has just diagnosed
as damaged is the worse failure mode — but I could not defend that choice from the
text, only from taste.

(Two things this finding is *not*. It is not about an entry whose only defect is a
failed stored-bytes crc: §15.3 and `[R-WRT-07]` are both explicit that such an
entry is well-formed, keeps its extent, and gets relocated normally, and
`[R-WRT-09]`'s crc obligation *does* reach it, so `[R-WRT-06]` limb 1 makes the
compactor refuse — which is coherent, if severe: one bad tile makes a whole file
uncompactable. And it is not about a *sentinel*, which is reproduced unchanged and
carries no violation.)

---

## 5. Finding writer-03 — §11.1 states §20.3's shrink bar in the opposite tense

**Kind:** CONTRADICTION. **Location:** §11.1's Rationale against §20.3 step 4
(`[R-WRT-04]`). **Byte-level: no.**

§11.1:

> §20.3 states normatively, and governs, what a commit may do to a layer that
> already stores tiles: a shrink is barred wherever it alters what §14 fixes for
> **a tile the new state still stores**, and permitted where it drops tiles out of
> the addressed set, whose extents then become slack. A layer that **stores
> nothing** may be re-declared freely.

§20.3 step 4, twice over, in the other tense:

> a shrink is permitted exactly where it alters nothing §14 fixes for any tile the
> layer stores **in the generation this commit supersedes**. … Unstoring that tile
> in the same commit does not rescue it either, and for the same reason: the
> quantifier is the superseded generation's, so a shrink that turns real positions
> into padding of a tile stored there is barred **whether or not the new state
> still stores it**.

> A layer that stores no tile **in the generation this commit supersedes** MAY be
> re-declared freely … the tense is the bar's, so a commit does not earn this
> permission by emptying the layer as it re-declares it

These quantify over different sets, and the difference is exactly the case §20.3
went out of its way to close. Concretely: a rank-1 layer, E = 5, T = 8, one
uint16 channel with fill `0xABCD`, one stored tile whose positions 3 and 4 hold
real data. A commit shrinks E to 3 *and* writes that tile's index entry to the
sentinel. §20.3: barred — positions 3 and 4 become padding of a tile stored in the
superseded generation, `[R-SER-05]` fixes their content to fill, and the stored
bytes do not hold fill; unstoring in the same breath does not rescue it. §11.1:
permitted — the new state stores nothing, and "a layer that stores nothing may be
re-declared freely".

I resolved it in §20.3's favour, on two independent grounds: §2.1 makes any text
"labeled … *Rationale*" non-normative, and the passage itself says §20.3 "states
normatively, and governs". So the bytes are not forked — and in any case §21.7
records that this is precisely the case with no witness ("a commit that supersedes
every tile it would have damaged leaves the live state clean, so the bar is
unwitnessed there"), so no verifier verdict turns on it either.

I report it anyway because §11.1's Rationale is where a writer implementing
schema-first growth will actually look — it is the passage that explains the
feature — and it currently teaches the reading §20.3 spent two sentences
forbidding. Both halves are in the wrong tense, not just one.

---

## 6. Finding writer-04 — §21.7's account, by class, has no class for the durability barriers

**Kind:** OBSERVATION. **Location:** §21.7 (`[R-ERR-01]`) against §21.1 and
`[R-LIF-02]`. **Byte-level: no.**

§21.1 makes §21.7 do real work:

> Its **completeness is normative** — a *detectable* file-conformance violation
> this specification names and the register omits is a defect in this document,
> detectability being the gate `[R-CNF-07]` already applies and **§21.7 the
> account, by class, of what fails it**

And §21.7's second paragraph is that account for obligations rather than for
content:

> A second set of obligations is omitted from the register because a single file
> exhibits no witness of their violation. Committed-prefix immutability and the
> generation sequence (`[R-LIF-01]`, `[R-LIF-03]`) are properties of a file's
> history, which §9.7 does not reconstruct; the ordinal mappings of `[R-GEO-06]`
> and `[R-SER-01]` …; `[R-CNT-13]`'s prohibition on an MU = 0 record encoding file
> offsets in its own payload …; `[R-CNT-18]`'s prohibition on a sub-record
> containing records …; §20.3 step 4's bar on a declaration change …; and
> `[R-ENC-06]`'s fixed field widths …

`[R-LIF-02]`'s two barriers — step 4's and step 6's, which `[R-WRT-02]` calls out
as "both barriers, not one", and which are as MUST-level as anything in §9 — fit
that paragraph's stated criterion perfectly and appear in none of its classes.
They are not a property of the file's *history*: no sequence of committed states
witnesses whether `fdatasync` was called, because the two files a barrier
distinguishes are byte-identical. They are not content incorrectness. They are not
an ordinal mapping, an opaque payload, an unparsed payload, or a field width.

This is the one writer obligation I implemented that the document nowhere accounts
for as unwitnessed, and the omission is load-bearing in a small way: a reader of
§21.7 trying to enumerate what a corpus cannot test will conclude that barriers
are testable, or will not think of them at all. The fix is a clause, not a rule
change — the class is "obligations over the write process rather than over any
committed state", and `[R-LIF-02]` steps 4 and 6 are its members. (I checked the
neighbours: `[R-LIF-04]`'s truncate obligation *is* accounted for, by §9.5's Note
pointing at F17; `[R-LIF-07]` is a SHOULD and out of scope by `[R-CNF-12]`.)

---

## 7. Finding writer-05 — §21.5's preamble over-claims: not every unreadable document is a violation or an experimental encoding

**Kind:** CONTRADICTION. **Location:** §21.5's preamble against §18.2
(`[R-MTA-09]`) and its Note. **Byte-level: no.**

§21.5:

> User metadata is quarantined (`[R-CNT-25]`): every way its document can be
> unreadable takes this outcome, whatever the containing scope — as a violation in
> the rows below, except at an experimental-range encoding, where no document rule
> attaches and §21.6 records the defined non-violation (`[R-MTA-10]`).

One "except" is listed. There is a second, defined a hundred lines earlier in
§18.2:

> a reader instead decodes with a bound of its own choosing, no smaller than
> §21.9's user-metadata guarantee, and **a document exceeding that bound is
> ignore-record like any other it cannot read**

and its Note settles the conformance question the other way from §21.5:

> A file whose document decodes to more than the guarantee stays conforming …
> A reader that proceeds takes ignore-record for that record

So a 20 MiB user-metadata document under encoding 2 is unreadable to a reader
holding §21.9's 16 MiB floor, takes ignore-record, is registered by no row of
§21.5, and is **not a violation** — while carrying an encoding this specification
assigns, so §21.5's stated exception does not reach it. `[R-MTA-09]` confirms this
from the verifier side: a verifier declining on that bound "cannot establish" and
"MUST NOT report it as" a finding that the file is nonconforming.

Nothing forks, because §21.1's tie-break ("where a row and the rule it cites
diverge, the rule governs") and §18.2's explicit text both settle it, and §21.9's
figure is a minimum guarantee rather than a cap. But the sentence is a normative
completeness claim in the register, and it is false as written. It cost me a pass
through §18.2 and §21.6 to convince myself the register was not missing a row.

---

## 8. Finding writer-06 — Appendix G item 2 leaves a degree of freedom open in the item whose job is closing them

**Kind:** OBSERVATION. **Location:** Appendix G item 2. **Byte-level: no.**

> Any other fixed nonzero value is substituted in the measure-zero case that they
> are all zero (§6.2 forbids `file_id` = 0).

"Any other fixed nonzero value" fixes nothing across implementations. Two writers
both adopting the reproducible-writer profile, handed identical input, produce
different `file_id`s — and therefore different trailers and different trailer CRCs
— whenever the derived digest's last eight bytes are all zero. Every other item in
the appendix names its value or names its producer; this one says "pick one",
which is the shape of the freedom the appendix exists to remove.

It is measure-zero (2⁻⁶⁴), the appendix is non-normative, and conformance turns on
none of it. I report it only because the charter asks me to work the profile item
by item and say what it leaves open, and this is the single item I could falsify
against its own stated purpose. Naming a constant — `0x0000000000000001`, say —
closes it in six words.

---

## 9. Slack, by shape of commit

| Commit shape | What becomes slack | Who counts it | What it may contain |
|---|---|---|---|
| **Append (new layer)** | the prior generation's directory, its pre-trailer pad, and its trailer; plus the new commit's own pad and any alignment gaps it opened. Measured on my file: 261 + 9 + 64 + 55 = 389. | a verifier, and it **MUST** report the total (§5.2, `[R-CNT-21]`); a reader never counts and MUST NOT interpret it | anything at all — "no conformance requirement applies to it". Writers SHOULD zero (`[R-CNT-03]`); Appendix G item 3 makes that a requirement |
| **Supersede a tile** | as above, **plus** the superseded payload and the layer's *entire* prior index region. Measured: +20 payload, +84 index. §20.3's Note prices this at ~20 MB of index for a one-sample edit on a 10⁶-tile layer | same | same |
| **In-place update** | does not exist. `[R-LIF-01]`: "every conforming mutation of a file is either a commit (§9.2) or a whole-file rewrite under a new file_id" | — | — |
| **Directory-only commit** (clear a slab, rename a layer, change a fill on a layer with no padding position and no pad bit) | only the prior directory, pad and trailer. §20.3's figure (c) | same | same |
| **Whole-file rewrite** (fresh file_id) | nothing inside the new file but its own gaps and pad. The **old file persists untouched** (`[R-PRV-02]`) until something outside this format deletes it | same, on the new file | same |
| **Compaction** | nothing carried: "A compactor's output contains only the structures reachable from the input's live trailer … so slack is never carried". Output slack = the alignment gaps its own declared invariants force, plus its pre-trailer pad | same | same |
| **Abandoned partial write** | **none, and this is the subtle one.** The residue past F is not slack — slack is defined against a *live committed state*, and a torn file has none. §5.2: "Where §6.2's ordered validation rejects the file before a live trailer is established there is no F and no live state to walk, so the total is not owed at all … which is not a partial total but the absence of one" | nobody. The verifier reports the trailer failure and says nothing about slack | unconstrained, and `[R-LIF-05]` forbids a reader to scan it |

Two further points the document is careful about and I had to get right in the
walk. First, a *partial* total (`[R-CNT-21]`) is F minus what the walk did claim —
an **upper bound**, never an under-count — and the verifier must say which scope
or violation stopped it. Second, when a layer is rejected, the claimants already
enumerated inside it are **discarded**, not kept: "the total is a claim about a
live state one of whose layers is not usable". My coverage walk implements both.

---

## 10. Torn-write recovery: five crash points

I take "the next reader" to mean a conforming reader on the default path
(`[R-LIF-05]`), "the next updater" an appender at `[R-WRT-04]` step 1, and
"conforming in the meantime" to be the pure byte predicate of `[R-CNF-02]`.

**(1) Crash inside step 2** (payloads/index regions), no barrier taken. Physical
length > F; trailₙ intact at [F−64, F) but no longer at the file's end.
*Reader:* takes the transport-authoritative size as F′ (`[R-CNT-10]`), fetches
[F′−64, F′), which is payload. Magic mismatch → F8 → reject-file, reported as
torn. It MUST NOT scan backward. In the freak case where payload mimics a magic,
the trailer CRC (F14) or committed_file_length against the transport size (F17)
catches it; §6.2's Note walks the last mile to the directory CRC.
*Updater:* `[R-LIF-04]` — trailer validation at the physical end fails, so the
file is torn, "the writer MUST NOT append", and recovery is "the deliberate
recovery operation of §9.6 — never an implicit step of opening for append".
*Conforming?* **No** (F8/F17). But the last committed state is byte-intact and
truncating to it restores the file exactly — §9.2's figure calls this "a window in
which the old state is *recoverable*" rather than readable, and that is the whole
return on never modifying a committed byte.

**(2) Crash after the directory is written, before step 4's barrier.** Reader and
updater see (1) exactly. Some of steps 1–3's bytes may not be durable, but nothing
references them, because the only thing that could — a trailer — was never
written. This is why step 4 comes where it does.

**(3) Crash inside step 5**, pad written, trailer partial. The final 64 bytes
straddle pad and trailer, so offset 0 of that window holds pad bytes, not the
magic → F8. Torn, recoverable to trailₙ. Same for the updater.

**(4) Crash between step 5's write and step 6's barrier.** Two post-reboot
outcomes, both safe. Either the trailer is durable — in which case generation
n+1 is live and everything it addresses was made durable by step 4, so the state
is consistent — or it is not, and the file reads as (3). There is no third
outcome, and that is precisely what the second barrier buys: the commit point is
atomic *with respect to observers*, not with respect to the storage stack.

**(5) Crash on the `[R-LIF-04]` overwrite branch, after the trailer is durable but
before the truncation.** A *valid* trailer exists, and the file is still refused:
committed_file_length ≠ physical size → F17. §9.5's Note is exactly on point —
"Residue past a completed commit carries no register row of its own … What the
residue violates is `[R-LIF-04]`'s writer obligation to truncate or overwrite, and
the state a reader can observe is already named." Recovery per §9.6 probes back
to the trailer, confirms committed_file_length = o + 64, and truncates.
*Conforming in the meantime?* **No.** This is the one crash point where a
correctly-ordered writer never lands, which is the argument for taking
`[R-LIF-04]`'s truncate-*first* branch instead.

**Bonus, (6): crash during compaction.** The output is a separate artefact, and
`[R-LIF-01]` guarantees the input was never touched. The partial output is torn
by (1)–(3); the input is untouched and conforming. Nothing is lost.

I found no gap here. §9.2, §9.4, §9.5, §9.6 and §20.3 step 1 compose cleanly, and
§9.6's two normative cautions — re-verify recovery output as a whole file, and
rollback is undetectable in-format — are both the right cautions.

One thing I checked and found *not* to be a hole. Deliberate rollback past a
committed generation would break `[R-LIF-03]`'s "(file_id, range) caches never
invalidate" contract, since a later commit would then write different bytes at the
same ranges under the same file_id. But that operation is not a conforming
mutation at all: it removes bytes inside [0, F) of a file that *has* a live
trailer, which `[R-LIF-01]` forbids outright, and §9.6 licenses truncation only to
"the nearest-to-end valid candidate". Recovery from a genuinely torn file removes
only bytes past a state that was never committed, so no cache can hold them under
a valid generation. The contract holds.

---

## 11. Byte-divergence catalogue

Given identical input arrays and identical stated options — I take the tiling,
layout, codec, filter, channel declarations and metadata *content* to be stated
options, per Appendix G item 2's own gloss that "two files carrying the same arrays
can legitimately differ in tiling, layout, and codec" — here is every way two
conforming writers may diverge that I found while building, and what the
reproducible-writer material does to each.

| # | Degree of freedom | Licensed by | Closed by Appendix G? |
|---|---|---|---|
| 1 | Placement of every structure; scattering, gaps, ordering | `[R-SLB-05]`, `[R-LIF-02]` step 2 "in any order" | **Yes**, item 3's total order, anchored at offset 16 with contiguity |
| 2 | Content of every gap and of the pre-trailer pad | `[R-CNT-03]` (a SHOULD), §5.2 "its content is unconstrained" | **Yes**, item 3 makes zeroing a requirement, naming the pad explicitly |
| 3 | Record order in the directory | `[R-CNT-14]` "Record semantics MUST NOT depend on record order" | **Yes**, item 3: by type, then layer name for 0x0001, then a content-derived key |
| 4 | Sub-record order inside a layer record | `[R-CNT-14]`, `[R-CNT-18]` | **Yes**, item 3, same key, and pinned *together with* extent placement |
| 5 | `file_id` | `[R-LIF-03]` states only a SHOULD | **Yes**, item 2's derivation — except in the all-zero-digest case, **finding writer-06** |
| 6 | Compressed-stream bytes for codecs 2–4 | `[R-CNF-05]`; §17.2's Note on RFC 1951's unspecified final-byte high bits | **Yes** by pinning the producer (item 1), which is the honest answer: byte-identity across *implementations* is unattainable and item 1 says so |
| 7 | Whether to store an all-fill tile or spell it as the sentinel | nothing requires either; `[R-TYP-08]` defines only what a sentinel means | **Yes**, item 6 |
| 8 | The fill a writer records when its caller chooses none | `[R-TYP-10]`, a SHOULD | **Yes**, item 7 — and item 7 correctly notes this reaches *further* than eight bytes of layer record, because item 6 makes storedness depend on fill |
| 9 | `version_minor`, `flags` | `[R-CNT-26]`, a SHOULD | **Yes**, item 8 |
| 10 | Declared alignment A / slab S / A_slab, when the caller states none | §16 leaves the choice open | **Yes**, item 5 |
| 11 | Filter value | `[R-COD-09]` permits 1 or 2 freely | **Yes**, item 5's second half |
| 12 | Name normalization form | `[R-ENC-14]`, a SHOULD; `[R-ENC-13]` makes NFC and NFD *different names* | **Yes**, item 10 — and it correctly notes the divergence reaches `inline_length` and `dir_length`, not just the name bytes |
| 13 | JSON serialization of the metadata document | `[R-MTA-05]` sorts members but "does not make two writers' output identical" | **Yes**, item 9, by pinning the JSON writer and the zstd producer |
| 14 | Number of generations / whether to checkpoint | §9 constrains none of it; `[R-LIF-07]` is a SHOULD | **Yes**, item 4, by restricting the profile to one commit |
| 15 | Whether an updater implements a private type, hence whether a PE = 0 experimental record survives a commit | §20.4 ("the definition it implements the type from supplies the flags, and the stored bits never do") crossed with §10.3's "no collision protection" | **Not closed, and not closeable.** Legitimate: the divergence is keyed to an implementation property, not to the file. Worth an implementer's attention because §20.4 *overrides* the stored PE bit, which is the only in-file signal that would have preserved the record |
| 16 | Whether an appender drops a top-level or sub-record MU = 0 / PE = 0 record in a supersede-only commit | **unclassifiable** — §20.4 says both permitted and forbidden | **finding writer-01.** Appendix G does not reach it (item 4 excludes appends) |
| 17 | Whether a compactor emits at all, given a structurally malformed index entry | **unclassifiable** — `[R-WRT-06]` says refuse, `[R-WRT-07]` says emit | **finding writer-02.** Appendix G does not reach compaction (item 2 explicitly hands a compactor back to `[R-WRT-06]`'s fresh draw) |
| 18 | Content of an auto-generated `tarn.created` (§18.4, "an RFC 3339 `date-time`") | §18.4 registers the key; no item forbids emitting it | **Not closed**, but I classify it as *legitimate*: the document's content is a stated option, and a writer that synthesizes a timestamp has changed the input. Item 9 pins the serializer, not the author. Not filed |

**Claims in the material I tried to falsify and could not:**

- Item 3's ordering key is genuinely non-circular. It masks `extent_offset` to
  zero precisely because the order is what fixes it, and every other component
  (type, flags, lengths, inline payload, extent contents) is a function of content
  alone. Its own closing sentence — that two records the key does not separate are
  byte-identical in everything that matters, so either order yields the same file
  — is correct.
- Item 3's placement rule composes with declared alignment: an aligned layer's
  first tile lands at the next multiple of A, the gap is zeroed, and the layer's
  index region (not being a tile) packs immediately after its last tile.
  Deterministic. Same for a slab's per-run A_slab, including the "a run with no
  stored tiles imposes nothing" case.
- §17.2's Note claims item 1 closes the DEFLATE tail-bit freedom "by pinning the
  encoder". True for any deterministic encoder, and item 1 pins thread count
  precisely because multithreading is where determinism is lost.
- Item 2's derivation is well defined and non-circular: the digest input is
  [0, F−64) followed by trailer bytes [0,60) with the `file_id` field zeroed, so
  it excludes both the identifier being derived and the CRC computed after it.
  "The digest's last eight bytes in output order … read little-endian" is
  unambiguous, and the appendix says why it avoids the word "low".

**One claim I would soften rather than call a finding.** Item 4's aside —
"Appending is reproducible only in the weaker sense that the appended bytes are" —
is not supported by any item, because item 3's sweep ("for each layer …") and its
anchor ("The first structure begins at 16") are written for a whole-file emission
and the profile excludes multi-generation files by construction. The aside is
informal and non-normative; adapting item 3 to the appended subset is the obvious
reading and it *is* deterministic. I record it here rather than filing it.

---

## 12. What I could not determine, summarized

Two questions stopped me outright and I could not answer either from the text:

1. May an appender drop an MU = 0 / PE = 0 record it does not implement, in a
   commit whose only change is superseding a stored tile's bytes? §20.4 says both
   yes and no, and the two answers produce different files. **writer-01.**
2. Must a compactor refuse a file carrying a structurally malformed tile-index
   entry, or reproduce the entry and emit? §20.5 says both, in adjacent
   paragraphs. **writer-02.**

Everything else in the creator, the appender, the slack accounting, the crash
analysis and the divergence catalogue I could resolve from the document alone,
usually on the first reading and always by the second. The register's arithmetic
is right, every published constant is right, and every worked example I re-derived
is right.
