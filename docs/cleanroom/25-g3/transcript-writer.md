# Round 25 — Writer/updater cleanroom walk (transcript of record)

## 0. Access and disclosure

I read exactly one specification file: `/Users/robertkleffner/Documents/GitHub/tarn/spec/tarn.md`
(4,477 lines), in full, in five sequential `Read` calls. I opened no ADR, no
`PLAN.md`, no `AGENTS.md`, no conformance corpus, no `spec/registry.json`, and
no git history. All arithmetic below was done in Python that reads no project
file.

Two disclosures, both about my *runtime*, not about the specification:

1. **Unrequested context.** My runtime placed material in context before I
   began: a project instruction file pointing at `AGENTS.md`, and an index of
   the maintainer's memory notes with titles naming ongoing concerns of this
   project. I did not open any of it and I have not used it. I am naming that
   it appeared, not repeating its contents.

2. **A shared scratchpad, and a file collision.** I wrote a CRC-32C helper to
   `<scratchpad>/crc.py` and ran it successfully. On my *next* invocation the
   same import printed output I had never written — another agent had
   overwritten `crc.py` between my two calls. To establish what had happened I
   ran `ls -la` on the scratchpad **root** (not on `round25/`). That listing
   showed the scratchpad is shared across many rounds and several concurrent
   agents: it contains directories and JSON files whose *names* reference other
   rounds and other roles. **I read none of their contents**, and I stopped
   looking the moment I understood the collision. Filenames alone are a small
   leak and I disclose it rather than hide it. I then moved all my work into a
   private subdirectory (`wr25-priv-8817/`) and used a uniquely-named module.

3. **Paths.** `spec/tarn.md` was exactly where the brief said it would be. The
   only path surprise is item 2.

## 1. Method

I did not summarise. I built a real file, byte by byte, with a Python emitter;
then wrote an independent verifier that re-parses those bytes from scratch and
checks every invariant I could derive from the document; then walked the append,
the flag matrix, slack, four torn-write points, compaction, and the divergence
catalogue. Every constant and worked example the document states, I recomputed.

### 1.1 The document's own arithmetic, recomputed

All of these check out exactly:

| Claim | Section | Recomputed |
|---|---|---|
| CRC-32C("123456789") = 0xE3069283 | §4.5 | 0xe3069283 |
| CRC-32C(zero bytes) = 0x00000000 | §4.5 | 0x0 |
| CRC of 4 sentinel entries (80 B) = 0x80A34955 | §7.4 example | 0x80a34955 |
| crc_of_crc_array of that = 0xC4EE982E | §7.4 example | 0xc4ee982e |
| CRC of a full all-sentinel segment = 0xEECB3BB2 | §15.4 | 0xeecb3bb2 |
| Appendix A trailer CRC = 0xE00938D2, stored `D2 38 09 E0` | App. A | 0xe00938d2 |
| §7.4's layer payload is 81 bytes; extent 4·20+⌈4/2¹⁶⌉·4 = 84 | §7.4 | 81, 84 |
| §11.2/§11.4: G=(4,8), N=32, P=65536, (300,700)→s=10, u-ord 11452, planar c=2 → 74 | §11.4 | all match |
| §15.4: ec=1e6 → 16 segments, region 20,000,064; tile 999,999 at seg-rel 339,180; segment 15 at [19,660,800, 20,000,000) | §15.4 | all match |
| §14.2: interleaved (a:u8,b:u16), P=6, Q=3, size 18, ordinal 5 → bytes [15,18); planar b → bytes 10–11; (t:f32,m:bool) Q=5, size 30, ordinal 5 → [25,30) | §14.2 | all match |
| §14.3: P=10 alternating → `55 01` (fill false) / `55 FD` (fill true) | §14.3 | match |
| §14.5: (5,5)/(4,4) edge tile (1,1) → 1 real + 15 padding, 32 bytes, values 1–15 = `CD AB` | §14.5 | match |
| §17.3: shuffle of 1.0,2.0,3.0 → `00 00 00 00 00 00 80 00 40 3F 40 40` | §17.3 | match |
| §19.4 note: for N ≥ 2¹⁶ planar per-channel entries fall in distinct segments | §19.4 | true (ordinal delta N ≥ 2¹⁶ ⇒ segment index differs) |
| §21.9 note: 2³² tiles → 256 KiB CRC array; 2³⁶ → 4 MiB | §21.9 | 2¹⁶·4 = 256 KiB; 2²⁰·4 = 4 MiB |
| §21.8: 121 conditions over 277 instances | §21.8 | 121 rows (F36/L49/T26/R10); semicolon count = 277 (F 58, L 116, T 55, R 48) |
| §21.2/3/4/5 stated counts 36/49/26/10 | §21.2–5 | 36/49/26/10 |
| §20.5's "one row for each of the other seven spaces" | §20.5 | §10.2 tabulates 8 spaces; record type → F36/L25; the other 7 → L36, L33, L34, L43, L45, L31, R1 — exactly the list given |

I found no arithmetic error anywhere in the document.

## 2. Creation: a file built end to end

### 2.1 What I chose to build

Two layers plus a file-scope user-metadata record, chosen to exercise the
corners a minimal file does not: an interleaved float32 layer with a stored
*edge* tile (so §14.5's padding rule bites) and a sentinel; and a **planar**
layer mixing a **packed bool plane** with a numeric plane, carrying a **slab
declaration** so that §16.2's run invariants bite.

* Layer `sst` — rank 1, dim `x`: E=100, T=32. Interleaved, one channel `temp`
  (float32, fill 0x7FC00000). codec 1, filter 1, A=0, S=0.
  G=⌈100/32⌉=4, N=4, P=32, Q=4, decoded size P·Q = **128 bytes**.
  entry_count = N = 4; extent_length = 4·20 + ⌈4/2¹⁶⌉·4 = **84**.
  Stored: tiles 0, 2, 3. Tile 1 is the **sentinel**. Tile 3 is the edge tile:
  x∈[96,128), real 96–99, **28 padding positions**, each carrying the recorded
  fill bytes `00 00 C0 7F` (`[R-SER-05]`).
* Layer `mask` — rank 2, dims `y`,`x`: E=(5,5), T=(4,4). **Planar**, two
  channels: `m` (bool, fill 0x00) and `v` (uint16, fill 0xABCD). codec 1,
  filter 1, A=0, **S=2, A_slab=64**.
  G=(2,2), N=4, P=16, C=2 → entry_count = C·N = **8**; extent_length =
  8·20 + 4 = **164**.
  Channel 0 (`m`) is a packed bool plane: decoded size ⌈16/8⌉ = **2 bytes**;
  P mod 8 = 0, so **no pad bits**. Channel 1 (`v`) is planar numeric:
  P·Bᶜ = 16·2 = **32 bytes**.
  Disk ordinals (`[R-GEO-06]`, channel-major): `m` → 0..3, `v` → 4..7.
  Stored: 0, 1, 3, 4, 5, 6, 7. Ordinal 2 is the sentinel.
* One top-level user-metadata record, encoding 1 (none), document
  `{"tarn.creator":"round25-writer/1.0","tarn.title":"demo"}` — 56 bytes,
  members sorted by key UTF-8 bytes (`tarn.c` < `tarn.t`, `[R-MTA-05]`), plus
  the 4-byte terminal CRC-32C = **61-byte extent** (≥ 5, `[R-CNT-25]`).

### 2.2 The emitted byte layout

```
offset   len  structure                                       fixed by
------------------------------------------------------------------------------
     0    16  front signature block                            §6.1  (fixed)
    16   128  sst stored tile, disk ordinal 0                   me
   144   128  sst stored tile, disk ordinal 2                   me
   272   128  sst stored tile, disk ordinal 3 (edge, 28 pad)    me
   400    84  sst tile-index region (4×20 entries + 1 seg CRC)  me
   484    28  SLACK (alignment run-up)                          me
   512     2  mask ordinal 0  (m, s=0)   run [0,2) starts here  A_slab=64
   514     2  mask ordinal 1  (m, s=1)   packed after ord 0     [R-SLB-03]
   516    60  SLACK                                             me
   576     2  mask ordinal 3  (m, s=3)   run [2,4) first stored A_slab=64
   578    62  SLACK                                             me
   640    32  mask ordinal 4  (v, s=0)   run [4,6) first stored A_slab=64
   672    32  mask ordinal 5  (v, s=1)   packed                 [R-SLB-03]
   704    32  mask ordinal 6  (v, s=2)   run [6,8) first stored A_slab=64
   736    32  mask ordinal 7  (v, s=3)   packed                 [R-SLB-03]
   768   164  mask tile-index region (8×20 + 1 seg CRC)         me
   932    61  file-scope user-metadata extent (56 doc + 4 CRC)  me
   993   259  directory region (3 records + 4-byte CRC)         §6.2 last struct
  1252    28  SLACK — the pre-trailer pad                       [R-LIF-02] step 5
  1280    64  trailer                                           §6.2 (F−64)
------------------------------------------------------------------------------
F = 1344, F mod 64 = 0. Claimed by the live state: 1166 bytes. Slack: 178.
1166 + 178 = 1344 exactly — the §5.2 partition closes.
```

Trailer fields: magic; version_major = 1; version_minor = 0 (`[R-CNT-26]`'s
floor); flags = 0 (`[R-CNT-08]` — a creator under this text **MUST**);
generation = 1; dir_offset = 993; dir_length = 259; committed_file_length =
1344; file_id = 0x5A17C0FFEE00D1CE (nonzero, drawn arbitrarily —
`[R-LIF-03]` only *SHOULD*s a CSPRNG); reserved = 4 zero bytes; CRC over [0,60).

Records, in the directory, in the order I chose (order carries no meaning,
`[R-CNT-14]`): `sst` layer (type 0x0001, flags 0x0003 = MU 1 / PE 1 — **fixed**
by §7.3, not my choice), `mask` layer (same), user metadata (type 0x0002, flags
0x0002 = MU 0 / PE 1 — **fixed**).

`sst`'s inline payload is **81 bytes** — byte-for-byte the length §7.4's worked
example gives, which is a useful independent check of my field packing, since I
built the layer to match it. Its `crc_of_crc_array` differs from the example's
(0x222C7129 vs 0xC4EE982E) because my index is not all-sentinel.

### 2.3 Which of those decisions the document fixed, and which it left to me

**Fixed by the document (no writer freedom):**
front-block bytes (§6.1); trailer magic, field order, widths and reserved zeros
(§6.2, `[R-ENC-06]`); trailer at F−64 with F mod 64 = 0; directory as the last
structure with nothing between its end and the trailer (`[R-CNT-05]`); the pad
running to the *next* 64-byte boundary, and **zero-length when the directory
already ends on one** — §6.2 resolves the otherwise-ambiguous "next" explicitly
("a writer that ends its directory on a 64-byte boundary leaves none");
generation = 1 and flags = 0 for a creator; every derived quantity
(entry_count, extent_length, decoded sizes, every CRC); registry-fixed record
flags (§7.3); the sentinel's 20 bytes; padding content = fill (`[R-SER-05]`);
pad-bit content = fill bit; bool bytes ∈ {0x00, 0x01}; in-tile row-major order
for every linearization; disk-ordinal order of index entries; the packed-bool
LSB-first bit assignment.

**Left to me:**
which tiles to store at all (I could equally have stored `sst` tile 1, an
all-fill tile — nothing but Appendix G item 6 forbids it); every offset and
therefore every gap (`[R-SLB-05]`); the order of structures; the order of
records in the directory; file_id; version_minor (a SHOULD); the tiling; the
layout; the codec and filter; the fill values; whether to declare A or S at
all; the JSON serialization; the slack content (a SHOULD to zero — I zeroed).

**One thing I want to be explicit about:** nothing in the document requires the
first structure to sit at offset 16. `[R-LIF-02]`'s creation path says the
writer "perform[s] steps 2–6, writing beginning at offset 16", which fixes
where *writing* starts, not where the first *structure* lands; a creator that
leaves 4 KiB of slack at [16, 4096) and starts there emits a conforming file.
Appendix G item 3 pins it for the reproducible profile and only there. I chose
16 and recorded the choice as mine.

### 2.4 Independent verification of the emitted bytes

I threw away the emitter's state and re-parsed the file from bytes. The
verifier reproduces §19.1's open, §19.3's layer validation, §15.3's entry
classification, §15.4's two-level CRC chain, `[R-COD-04]`'s codec-1 length
equality, §14.5's padding-content check over every padding position of every
stored tile in both layouts, §14.3's pad-bit check, §16.2's slab run invariants,
and §9.7's coverage walk. Result: every check passes; 16 claimants, no overlap,
178 bytes slack, claims + slack = F.

Slab check, spelled out because it is the part of §16 a writer actually has to
plan around. Blocks are per channel for a planar layer (`[R-SLB-02]`): `m` is
[0,4), `v` is [4,8). With S = 2 that is four runs: [0,2), [2,4), [4,6), [6,8).
- run [0,2): first stored is ordinal 0 at 512; 512 mod 64 = 0 ✓; ordinal 1 at
  512 + 2 = 514 ✓ (packed).
- run [2,4): ordinal 2 is a **sentinel and therefore transparent**
  (`[R-SLB-03]`), so the run's first stored tile is ordinal 3 at 576;
  576 mod 64 = 0 ✓. Note this is a run whose *first ordinal* is not stored —
  the alignment obligation attaches to the first **stored** tile, not to
  block_start + r·S.
- run [4,6): 640 (aligned), 672 = 640 + 32 ✓.
- run [6,8): 704 (704 = 11·64, aligned), 736 = 704 + 32 ✓.

The 28 + 60 + 62 = 150 bytes of intra-layer slack are the price of A_slab = 64
on 2-byte tiles. Nothing in §16 discourages that; §16's opening says a writer
that scatters "wastes space rather than violating a rule".

## 3. The append procedure

### 3.1 Commit 2 on the file above: add a layer and supersede a tile

`[R-WRT-04]`'s six steps, executed against g1 (F = 1344, gen 1):

1. **Establish F.** Validate the trailer in the final 64 physical bytes
   (`[R-LIF-04]`). Magic → CRC → version gate → the remaining field gates
   (§6.2's order). F = 1344. On failure I **must not append**; recovery (§9.6)
   is a separate deliberate operation, never an implicit part of opening for
   append.
2. **Open** (§19.1): trailer, directory CRC, record walk, layer-name namespace.
   Two requests' worth of I/O regardless of layer count (`[R-RDR-01]`).
3. **Validate what the commit touches** (`[R-WRT-03]`): the trailer and the
   **full** directory always — re-emission relies on every directory byte —
   plus §19.3's full layer validation for `sst` (whose index I am re-emitting),
   plus the §19.4 index chain (crc_of_crc_array + the covering segment CRC) for
   every segment whose entries I reuse. `mask` I neither modify nor rely on, so
   I owe it nothing.
4. **Write payloads and indexes**, beginning at exactly F = 1344:
   * new `sst` tile-0 payload at [1344, 1472);
   * `sst`'s **whole** index region re-emitted at [1472, 1556) — 84 bytes,
     one entry re-pointed, one sentinel and two entries **byte-identical at
     their disk-ordinal positions**;
   * the new layer `grad`'s tiles and index region after that.
   `mask` keeps its extent slot pointing at 768: a layer the commit does not
   touch does not move (`[R-WRT-05]`), and relocating a live index region is
   compaction's operation, not an appender's.
5. **Re-emit the directory** — complete, never a delta (§9.2) — followed by its
   CRC.
6. **Commit**: barrier; pad to the next 64-byte boundary; trailer with
   generation 2, the **same** file_id, unknown ignore-lane bits copied forward
   (`[R-CNT-08]`), version_minor = max(floor, prior) (`[R-CNT-26]`); barrier.

**Durability order and the commit point.** Steps 1–3's bytes must be durable
before the trailer is written (step 4 of `[R-LIF-02]`), and the trailer durable
after (step 6). Both barriers are owed — §20.2 says so for a creator
("both barriers, not one") and §20.5 repeats it for a compactor. The commit
point is not "the trailer bytes are written": it is "the trailer bytes are at
the physical end of the file **and** the physical length equals the trailer's
committed_file_length". That matters on the `[R-LIF-04]` overwrite path, where a
writer that overwrote from F into a physically longer file must also truncate
"no later than step 6"; a crash between writing the new trailer and truncating
leaves stale bytes past the new F, which a reader meets as a failed
committed_file_length check (F17) and reports as torn. The document places the
truncation inside step 6's durability boundary, so this is determinate.

**Cost, spelled out.** Superseding one `sst` tile costs 128 payload bytes plus
the entire 84-byte index region plus the entire directory plus pad plus trailer.
§20.3's note quantifies the general case (≈20 MB of index to edit one sample of
a 10⁶-tile layer). What the note does *not* say, and what I had to derive, is
the **slab** amplifier: `[R-SLB-04]` obliges a commit that changes the stored-tile
set, run partition, or byte placement of any run to re-establish `[R-SLB-03]`'s
invariants **for every such run**. Superseding `mask` ordinal 4 therefore forces
re-emission of ordinal 5 as well — the whole run — because ordinal 5 cannot move
(`[R-LIF-01]`) and the run must stay packed. Worse, growing a **planar**
slab-declared layer across a grid boundary changes N, which moves every channel
block start [c·N,(c+1)·N) and so re-partitions every run of every channel c ≥ 1;
that forces re-emission of every stored tile of those channels, or clearing the
declaration. Both consequences follow rigorously from `[R-SLB-02]` +
`[R-SLB-04]`; neither is stated as a cost anywhere, and a writer that does not
derive it will emit nonconforming files.

### 3.2 The record-flag matrix, walked exhaustively

§7.2 defines exactly two flag bits — bit 0 MUST_UNDERSTAND, bit 1
PRESERVE_ON_EDIT — plus reserved bits 2–15 (writers MUST emit zero; readers
MUST ignore; a verifier treats nonzero as a violation at the record's governing
scope: F26/L47). That is four (MU, PE) combinations, and §20.4's authority for
the flag values has three sources. The full matrix my updater implements:

| Record | Flags source | MU | PE | What my updater is permitted to do |
|---|---|---|---|---|
| type 0x0001 (layer) | §7.3 registry, **not** the stored bits | 1 | 1 | Re-emit byte-identically if unmodified; modify freely if it modifies the layer. Never drop: no commit removes a layer record. A *stored* bit differing from the registry is F28/L49 — a verifier violation that changes no reader or updater behavior. |
| type 0x0002 (user metadata) | §7.3 registry | 0 | 1 | Re-emit byte-identically, extent content unmodified; or modify it, in which case a **new** extent is appended and the old becomes slack (§20.3 shape (c)). Never drop. |
| unimplemented, top level | stored bits | 1 | 1 | **No commit at all.** `[R-CNT-15]` makes it reject-file; the updater is a reader first. Compaction likewise barred (`[R-WRT-06]`). |
| unimplemented, top level | stored bits | 1 | 0 | Identical to the row above: `[R-CNT-12]` obliges a reader or updater to read this combination **as PE = 1**. (The combination is itself F25 — verifier-detected.) |
| unimplemented, top level | stored bits | 0 | 1 | Retain byte-identical, extent content unmodified. An appender may not even relocate the extent — `[R-WRT-05]` requires the extent **slot** to be byte-identical too; relocation is `[R-WRT-08]`/§20.5's operation. |
| unimplemented, top level | stored bits | 0 | 0 | Retain byte-identical, **or** drop it (extent → slack) — but only in a commit that independently changes the file's layer set, any layer record's content, or another non-layer top-level record. See finding **writer-03**. |
| unimplemented, layer sub-record | stored bits | 1 | 1 or 0 | Retain byte-identical; **that layer** becomes unmodifiable. Every other layer stays editable, and the file is not rejected (`[R-CNT-18]`). |
| unimplemented, layer sub-record | stored bits | 0 | 1 | Retain byte-identical, extent unmodified. |
| unimplemented, layer sub-record | stored bits | 0 | 0 | Retain, or drop in a commit that independently changes that layer's record, its index entry set, or which of its tiles are stored. |
| implemented, unregistered type | the definition the updater implements it from | any | any | Same obligations, flags taken from that definition and never from the stored bits. `[R-CNF-06]` extends §20.4 to "every record type, not only those it does not understand". |
| reserved-range type (0x0003–0x7FFF) | stored bits | — | — | Read exactly as an unknown type; the file is nonconforming (F36/L25) but that is **verifier**-detected, so my appender is not obliged to notice and may commit. It SHOULD report what it carried forward (§20.3 step 2). |

Two consequences worth stating because they surprised me while writing the
updater:

* A single unimplemented top-level MU = 1 record makes the file permanently
  un-appendable and un-compactable by that tool. There is no partial mode.
* A malformed **index entry** an appender meets while re-emitting a region is
  carried forward **byte-identically at its disk-ordinal position**, explicitly
  "not repaired to a sentinel" (§20.3 step 2) — whereas a **compactor** meeting
  the same entry MUST refuse, because regenerating the region requires
  re-pointing every non-sentinel entry and `[R-IDX-03]` gives a structurally
  invalid entry no extent to re-point (§20.5). The asymmetry is deliberate and
  stated in both places; I implemented it as stated.

### 3.3 Entry renumbering on a geometry change

Step 4 says entries not otherwise touched are "byte-identical at [their]
disk-ordinal position (a geometry change renumbers ordinals wherever
`[R-GEO-06]` moves them)". This is not a copy; it is a permutation. Worked:
a planar C = 2 layer, E = (4,6), T = (2,2), G = (2,3), N = 6, entry_count = 12.
Shrink E to (4,4): G = (2,2), N = 4, entry_count = 8. Spatial ordinal
s = t_y·G_x + t_x, so tile (1,0) moves from s = 3 to s = 2 and tile (1,1) from
4 to 3; tiles (0,2) and (1,2) leave the addressed set entirely and their extents
become slack; and every channel-1 entry moves from c·6+s to c·4+s. My updater
therefore rebuilds the region from a (channel, tile-coordinate) → entry map, not
from the old ordinal order. The document determines this completely; it just
does not say it in one place.

## 4. Slack, by shape of commit

| Shape | Bytes that become slack | Who counts them | What they may contain |
|---|---|---|---|
| **Creation** | Alignment/slab run-up gaps and the pre-trailer pad only. In my file: 150 + 28 = 178. | A verifier that reaches a live state MUST report the total (§5.2, §9.7). Readers never. | Unconstrained. Writers SHOULD zero (`[R-CNT-03]`); nothing rides on it. §22.3 states plainly that corruption confined to slack is invisible to reader and verifier alike. |
| **Append** | The previous generation's directory, pad and trailer, always; plus every superseded stored-tile extent; plus the whole previous tile-index region of every layer whose stored-tile set or index content changed; plus any dropped record's extent; plus the new commit's own gaps and pad. | Same. | Same. |
| **In-place update** | Does not exist. `[R-LIF-01]` admits exactly two mutations: a commit, or a whole-file rewrite under a new file_id. There is no conforming operation that edits a committed byte, so the question has no third answer. | — | — |
| **Rewrite (a new file under a fresh file_id)** | Nothing carries over: the old file persists untouched until something outside this specification deletes it (`[R-PRV-02]`). The new file has creation-shaped slack. | Same. | Same. |
| **Compaction** | The *output* carries no superseded bytes, but it is not slack-free: it still has its pre-trailer pad, and it must still honour any declared A or A_slab, so a compacted `mask` still pays 150 bytes of run-up. §20.5's "so slack is never carried" is a claim about *carrying*, and its own figure shows a `pad`. | Same. | Same. |
| **Abandoned partial write** | **None of it is slack.** Bytes past F are not part of any live state; the byte sequence is simply not a conforming file — its final 64 bytes are not a trailer, so `[R-CNT-06]` fails (F8/F14/F17). §5.2 is explicit that where §6.2's ordered validation rejects before a live trailer is established "there is no F and no live state to walk, so the total is not owed at all". | Nobody. The verifier reports the trailer failure "and nothing about slack, which is not a partial total but the absence of one". | Unconstrained but irrelevant; `[R-LIF-04]` obliges the next writer to truncate or overwrite. |

Two further slack facts a writer needs and that took reading to establish:

* **Bytes may never be shared.** `[R-CNT-13]`: "Extents are owned exactly
  once ... no two extent slots and no two structures overlap." So a writer with
  two byte-identical tiles, or two records with identical extent content, MUST
  store both copies. De-duplication is forbidden, not merely unusual. This is a
  real cost and it is unambiguous.
* **A verifier's slack total may be partial.** Where a scope-level rejection
  ends enumeration, or the verifier stopped at the first violation, the total is
  reported as partial and is an **upper bound** — and where the walk itself
  established the rejection (L18, L40–L42), the claimants it had already
  enumerated for that layer are *discarded*, which is what keeps it an upper
  bound rather than an under-count.

## 5. Torn-write recovery: four crash points

Let commit 2 write payload [1344,1472), index [1472,1556), directory
[1556,1815), pad [1815,1856), trailer [1856,1920), F' = 1920.

| # | Crash at | What the next reader sees | What the next updater does | Conforming meanwhile? |
|---|---|---|---|---|
| 1 | Mid-payload, physical length 1400 | Final 64 bytes = [1336,1400): not 64-aligned to a trailer, magic fails (F8). Reports torn; **MUST NOT scan backward** (`[R-LIF-05]`). | Trailer validation fails at step 1 → no append. Recovery (§9.6) probes 64-aligned offsets from the largest o with o+64 ≤ 1400, i.e. 1336, 1280 → hits the gen-1 trailer at 1280 (CRC ✓, committed_file_length = 1344 = 1280+64 ✓). Truncate to 1344, **re-verify the output as a whole file**, then append. | No. |
| 2 | After step 4's barrier (payload+index+directory durable), before the trailer, length 1815 | Final 64 bytes are directory/pad bytes: magic fails. Torn. | Identical to #1: recovery lands on 1280, truncates to 1344. The complete, CRC-valid directory at [1556,1815) is discarded — nothing points at it. | No. |
| 3 | Mid-trailer, length 1856+k, 0 < k < 64 | Largest o with o+64 ≤ 1856+k is 1792 (since k < 64), which is inside the directory/pad: magic fails. Torn. | Recovery walks 1792 → … → 1280. Same outcome. | No. |
| 4 | Trailer written and durable; the overwrite-path truncation not yet done, so physical length > 1920 | Depends on the residue. If the tail is not a valid trailer: torn. If a stale 64-aligned tail *is* a syntactically valid trailer, it will almost certainly fail committed_file_length against the transport size (F17) — and if by construction it does not, §6.2's Note says such a mimic "is caught at the directory CRC". | Same: no append until recovery. §9.5's Note names exactly this state: what the residue violates is `[R-LIF-04]`, and the observable state is already registered. | No. |

In none of the four is the file conforming in the meantime, and the document is
unambiguous about that: §5.1 requires the file size of a conforming file to
equal the live trailer's committed file length, and there is no live trailer.
The recovered file *is* conforming — that is the whole return on never modifying
a committed byte. Two normative cautions bind my recovery tool: re-verify the
output as a whole file before trusting it (a payload can mimic a trailer), and
report both the candidate settled on and how many were rejected.

## 6. Compaction

Compacting g1: output = the live committed state less any record §20.4 licenses
dropping, at a **fresh** file_id (a new draw under §9.3's randomness advice —
§20.5 is explicit that a value merely *compared against* the input's is not
enough) and generation 1, following `[R-LIF-02]`'s **creation** path with both
barriers and the step-5 pad, exactly as §20.2 obliges a creator. I checked the
analogy word for word: §20.2 says "the barrier, the pad, the generation-1
trailer with a fresh nonzero file_id ... and the barrier that makes the trailer
durable (`[R-LIF-02]` steps 4–6 — both barriers, not one)"; §20.5 says "The pad
of step 5 and the barriers of steps 4 and 6 — both, not one — are owed here as
they are of a creator." The analogy holds.

Content preserved, placement not: every stored tile's bytes verbatim, every
index entry's crc unchanged, sentinels unchanged; entry **offsets** new;
segment CRCs recomputed over the entries as re-emitted; the layer record's
crc_of_crc_array updated and its extent slot re-pointed. `[R-WRT-09]` fixes the
verification depth: the open, each retained layer's record and full index chain,
and each relocated extent's checksum including every stored tile's entry crc,
**before** emitting that structure's bytes.

Refusal grounds I implemented: any `[R-WRT-09]` check failing; any record of an
unimplemented type with MU = 1; any structurally invalid index entry met while
regenerating a region (no extent to re-point, and a tile-index entry is not a
record §20.4 licenses dropping); any detected violation the table does not let
it drop.

What compaction does **not** reclaim: the pre-trailer pad, and every gap a
declared A or A_slab forces. Compacting my `mask` layer still costs 150 bytes of
64-alignment run-up, because §20.5 places the compactor's placement freedom
inside "every declared layout invariant permits (`[R-SLB-01]`, `[R-SLB-03]`)".
§20.5's "so slack is never carried" is true as written — carried, not created —
and its own figure shows a `pad`.

## 7. Byte-divergence catalogue

Two conforming writers, identical input arrays, identical stated options. Every
legitimate divergence I could construct, and what Appendix G does with it.

| # | Degree of freedom | Governing text | Appendix G |
|---|---|---|---|
| 1 | Placement of every structure; relative order of tiles, index regions and record extents | `[R-SLB-05]`, `[R-LIF-02]` step 2 | **Closed** — item 3's total emission order |
| 2 | Extent of gaps between structures | `[R-SLB-05]` | **Closed** — item 3 (contiguous save forced alignment) |
| 3 | Content of gaps and of the pre-trailer pad | `[R-CNT-03]` (SHOULD) | **Closed** — item 3 ("every byte of every such gap is zero — `[R-CNT-03]`'s advice, taken as a requirement here") |
| 4 | `file_id` | §9.3 (SHOULD random) | **Closed** — item 2's derived hash, with the all-zero substitution |
| 5 | Record order in the directory | `[R-CNT-14]` | **Closed** — item 3's type/name/header key |
| 6 | Sub-record order within a layer record | `[R-CNT-14]` | **Closed** — item 3, explicitly |
| 7 | Encoder output under codecs 2–4 | §17.2's Note; `[R-CNF-05]` | **Closed by pinning** — item 1 (level, strategy, thread count) |
| 8 | The unused high bits of a raw DEFLATE stream's final byte | §17.2's Note, which says this specification "constrains them nowhere" | **Closed** — item 1, and the Note says so |
| 9 | Presence/absence of a zstd Frame_Content_Size field | `[R-COD-06]` ("MAY be present") | **Closed** — item 1 (encoder settings) |
| 10 | Declared zstd `Window_Size` | `[R-COD-06]` (SHOULD ≤ 8 MiB) | **Closed** — item 1 |
| 11 | Whether an all-fill tile is stored or sentinel | nothing requires the sentinel | **Closed** — item 6 |
| 12 | Fill recorded when the caller chooses none | `[R-TYP-10]` (SHOULD) | **Closed** — item 7, which correctly notes it reaches item 6 as well |
| 13 | `version_minor` | `[R-CNT-26]` (SHOULD) | **Closed** — item 8 (creator); admitted open for compactors |
| 14 | Trailer `flags` | `[R-CNT-08]` (MUST 0 for a creator) | Already fixed for a creator; item 8 restates and carves out the compactor |
| 15 | Number of generations | §9 constrains none | **Closed** — item 4 |
| 16 | Declared A / S / A_slab | §16 leaves to the writer | **Closed** — item 5 |
| 17 | Declared filter | §17.3 leaves to the writer | **Closed** — item 5 |
| 18 | JSON serialization of user metadata (number formatting, escaping, whitespace) | `[R-MTA-05]` sorts members but §18.2's Note concedes no cross-writer identity | **Closed by pinning** — item 9 |
| 19 | Unicode normalization of names | `[R-ENC-14]` (SHOULD NFC) | **Closed** — item 10 |
| 20 | **Tile extents Tᵢ** | §11.3's Note: "Tile extents are a writer's choice, and this specification imposes none" | **Left open** — see finding **writer-04** |
| 21 | **Channel layout (interleaved vs planar)** | §7.4/§14.1 leave it to the writer; §14.4's Note says a single-channel bool layer's tile images differ between layouts and "both forms are valid" | **Left open** — see finding **writer-04** |

Divergences I looked for and found **forbidden**, not legitimate:

* **De-duplicating identical extents or identical stored tiles.** Forbidden by
  `[R-CNT-13]`: "Extents are owned exactly once ... no two extent slots and no
  two structures overlap." Two writers cannot differ here because only one
  behaviour is legal.
* **Emitting the all-sentinel segment constant without computing it.**
  `[R-IDX-05]` permits it, but the constant *is* the computed value, so no byte
  divergence exists.
* **Reusing an earlier generation's superseded bytes as a new structure.** Legal
  for an appender (nothing forbids pointing a new extent at bytes that already
  exist as slack; `[R-LIF-01]` bars *modifying* committed bytes, not referencing
  them), but unreachable under the profile, which is one generation (item 4).
* **Emitting an in-tile bool byte other than 0x00/0x01, padding content other
  than fill, or a pad bit other than the fill bit.** All forbidden; there is one
  legal encoding per value.
* **Linearization, index_encoding.** One legal value each; no freedom.

Appendix G's internal claims that I tested and could **not** falsify:

* Item 2's `file_id` derivation is not circular: F, the directory, and all
  trailer fields other than `file_id` are fixed by items 3–8 without reference
  to `file_id`, and the trailer CRC is computed after the identifier is written
  in.
* Item 3's tie-break key genuinely terminates. Masking `extent_offset` is
  necessary (the order fixes it, so a key containing it would depend on its own
  result), and every other component — type, flags, `inline_length`,
  `extent_length`, inline payload, extent contents — is content-derived. Two
  records the key does not separate are byte-identical apart from
  `extent_offset`, and swapping their positions swaps two identical extents and
  two otherwise-identical headers, so the file is the same. The claim holds.
* Item 3's list of things that force a gap (a declared A, a declared A_slab,
  §6.2's 64-byte trailer alignment including the pad) is complete: I could
  construct no other forced gap under the profile's contiguity rule. In
  particular `dir_offset ≥ 16` and `extent_offset ≥ 16` force nothing, because
  the first structure already starts at 16.
* Item 6's "all-fill tile" is well defined in every layout, including a packed
  bool plane whose pad bits are fill bits by `[R-SER-05]`.

## 8. Places I had to guess, and the findings that came out of them

### writer-01 — AMBIGUITY. §20.3 step 4's list of what a declaration change may not alter names padding positions but not pad bits or interleaved boolean bytes

§20.3 step 4:

> A commit MUST NOT change a layer's declarations in a way that alters, for any
> tile that layer stores **in the generation this commit supersedes**, what §14
> fixes for its stored bytes or how they decode — the set of padding positions
> (§11.3) and the content `[R-SER-05]` fixes there, the decoded size, the byte
> offset of any sample within the decoded tile image, or the codec and filter
> that produced the stored bytes.

§14 places exactly three structural content obligations on a stored tile's
bytes: padding-position content and **pad-bit** content (`[R-SER-05]`, §14.5),
and interleaved **boolean byte** values (`[R-SER-08]`, §14.2). The list names
the first. It does not name pad bits, and §14.3 is emphatic that they are a
different thing:

> **Note.** Pad bits are not padding positions (§11.3).

It does not name boolean bytes either. Yet §20.3's own Example (c) asserts the
bar reaches pad bits —

> A fill change on a layer that **stores** a tile carrying either is not an
> appender's operation at all (step 4): it would invalidate every stored tile it
> reaches.

("either" = a padding position or a pad bit) — and §21.7 asserts it reaches all
three:

> A change reaching a byte §14 structurally constrains — a padding position, a
> pad bit, or a boolean byte — fires §21.4's content rows.

**Permitted readings.** (a) The bulleted list is the test, so a change that
alters only pad bits or only boolean-byte validity is not barred. (b) The list
is illustrative and the operative test is the lead clause "what §14 fixes for
its stored bytes", so all three are barred; the paragraph's own gloss supports
this — "the list names where that effect arises rather than standing on its own".

**Which I picked, and why.** (b). §21.7 and Example (c) both presuppose it, and
(a) would leave `[R-SER-05]`'s pad-bit half and `[R-SER-08]` outside the bar
even though both are §14 obligations on the same bytes.

**Concrete case that made me guess.** A planar bool layer, one channel, T=(3,4)
so P = 12, decoded size ⌈12/8⌉ = 2, E=(3,4) so **no padding positions at all**
and pad bits at bits 4–7 of byte 1. A commit changes the channel's fill from
0x00 to 0x01. Every list item is unchanged: the (empty) set of padding
positions, the content `[R-SER-05]` fixes *there* (vacuous), the decoded size
(2), sample byte offsets, the codec and filter. Under (a) the commit is
permitted; under (b) it is barred. The same shape arises for uint8 → bool on an
interleaved channel, where both types have element size 1 so Q, the decoded
size, and every sample offset are unchanged.

**What an implementer does wrong without it.** Emits the commit. Where the
affected tiles stay stored the result is caught anyway (T5, or T2), so the
implementer's file is nonconforming and the emittable set does not move. Where
the same commit **unstores** those tiles, §20.3 says the bar still applies ("the
quantifier is the superseded generation's"), §21.7 says there is then no witness
— and the output is a conforming file either way. So the cost of the ambiguity
is an updater that believes itself conforming and is not.

**Byte-level: no.** Both readings agree on which *files* conform: where the
tiles remain stored, `[R-SER-05]`/`[R-SER-08]` independently make the file
nonconforming; where they are unstored, the output is conforming under both.
The divergence is in whether the *updater* is conforming, not in the emittable
set.

### writer-02 — OBSERVATION. §11.1's Rationale over-generalises about grid counts and entry_count

§11.1:

> Growth that leaves every grid count ⌈Eᵢ / Tᵢ⌉ (§11.2) unchanged touches the
> directory alone; growth that raises one changes entry_count and with it
> extent_length (`[R-CNT-17]`), so the layer's whole tile-index region is
> re-emitted and disk ordinals renumber wherever `[R-GEO-06]` moves them (§20.3,
> `[R-WRT-04]`) — the first growth of a zero-extent layer included.

The second clause is false for a layer with **two or more** zero extents, which
§11.1 itself makes legal ("A dimension with extent 0 is valid"). Take rank 2,
E = (0, 0), T = (4, 4). Then G = (0, 0), N = ∏Gᵢ = 0, entry_count = 0 (or C·0 =
0 planar), extent slot (0, 0), crc_of_crc_array = 0. Grow E₀ to 4: G becomes
(1, 0). A grid count has risen — and N is still 1·0 = 0, entry_count is still 0,
extent_length is still 0, and there is **no tile-index region to re-emit**. The
trailing clause aggravates it by asserting that "the first growth of a
zero-extent layer" is always such a case; here it is not.

**What an implementer does wrong without it.** Nothing byte-visible, which is
why I grade this low: `[R-CNT-17]`, `[R-CNT-23]` and L22 independently force
entry_count = 0 → extent slot (0, 0) → extent_length 0 → crc_of_crc_array 0, and
an implementer computes entry_count from geometry regardless. What it costs is a
reader of §11.1 who plans an appender around "raising a grid count ⇒ re-emit the
index region" and finds the branch unreachable and the invariant false.

**Byte-level: no.** The text is a Rationale (§2.1 makes it non-normative) and
the normative rules decide every byte it touches.

### writer-03 — AMBIGUITY. §20.4: may adding a top-level record license dropping an MU = 0 / PE = 0 one?

§20.4's MU = 0, PE = 0 row:

> An appender MUST NOT drop it except in a commit that *independently* changes
> the scope the record attaches to: for a layer sub-record, that layer's record,
> the entry set of its index, or which of its tiles are stored; for a top-level
> record, the file's layer set, any layer record's content, or another
> *non-layer* top-level record. A commit changes the layer set by adding a
> layer; an appender never removes one

The colon-list must be the operative definition, not a gloss: the lead phrase
"changes the scope the record attaches to" is, for a top-level record, "changes
the file", which every commit does — and the row's closing sentence forecloses
that reading ("a commit whose only effect would be the drop MUST retain it").

Now the case my updater hit: **a commit that adds a file-scope user-metadata
record where there was none, and drops an unknown MU = 0 / PE = 0 top-level
record.**

**Permitted readings.** (a) The third item means the *set* of non-layer
top-level records, so adding one is a change to it and the drop is licensed —
by parallel with the first item, which the very next sentence glosses as
including addition ("A commit changes the layer set by adding a layer").
(b) Literally, "another *non-layer* top-level record" names an existing record
and adding a new one changes no such record, so nothing in the list is
satisfied and the appender MUST retain.

The asymmetry that produces the ambiguity is that the *sub-record* branch names
a **container** — "that layer's record" — which adding a sub-record plainly
changes, while the top-level branch names a **record** rather than a set, and
the only addition the row glosses is the layer one.

**Which I picked, and why.** (a). The rule's stated purpose is to stop a drop
from being a commit's only effect, and adding a record is an independent effect;
reading (b) would also mean an appender could never drop such a record in a
commit whose other work was purely additive at file scope, which sits oddly
beside the layer gloss. I implemented (a) and recorded the guess.

**What an implementer does wrong without it.** It emits a different directory —
one record fewer or one record more — for the same requested operation, and one
of the two implementations is a nonconforming updater under `[R-CNF-06]`, which
extends §20.4's preservation obligations to "every record type".

**Byte-level: no.** Both directories are conforming files: an unassigned-type
MU = 0 record is conforming whether present or absent (§21.6), and the same
file is emittable by a creator or a compactor in either case
("A compactor MAY drop it whenever it rewrites the file"). No reader's
accept/reject verdict moves.

### writer-04 — OBSERVATION. Appendix G pins four of the six writer-choice knobs in a layer record and leaves two

Appendix G's preamble:

> Applications that need byte-identical output — content-addressed storage,
> reproducible builds — can adopt this profile, which closes the degrees of
> freedom this format deliberately leaves open.

Item 5 closes three of them, with an argument that transfers verbatim to two it
does not close:

> **No declared alignment and no slab**, or fixed declared values — both change
> placement and neither is implied by content. **A fixed filter value**
> likewise: §17.3 leaves the choice to the writer, it changes the stored bytes
> of every tile it touches, and no content implies it, so two writers agreeing
> on everything else still disagree on bytes without it pinned.

Item 1 closes the codec. Nothing in items 1–10 closes **tile extents** or
**channel layout**, and §11.3 says of the first exactly what item 5 says of the
filter:

> **Note.** Tile extents are a writer's choice, and this specification imposes
> none.

Both change the stored bytes of every tile, both change the layer record, and
neither is implied by content — item 2's own rationale concedes it: "two files
carrying the same arrays can legitimately differ in tiling, layout, and codec",
after which the profile pins the codec and neither of the other two. Two
implementations adopting the whole profile, handed the same array, can pick
T = (256, 256) and T = (512, 512), or interleaved and planar for a
single-channel bool layer (§14.4's Note: "⌈P/8⌉ packed bytes planar versus P
bytes interleaved — and both forms are valid"), and emit entirely different
files while conforming to every numbered item.

**What an implementer does wrong without it.** An adopter building
content-addressed storage on two independent profile implementations gets
non-matching digests and no item to point at. The remedy is one sentence in
item 5.

**Byte-level: no.** Appendix G is non-normative and "adds no requirement to any
actor"; nothing about which files conform moves.

## 9. What I could not determine, and did not report as findings

Recorded here for completeness, each because I decided it was resolvable and did
not want to pad the list:

* **`[R-SLB-03]`'s "its length".** "each stored tile's offset equals the
  previous stored tile's offset plus its length" — "its" could bind to either
  tile. §16.2's example disambiguates ("run 1's stored tiles are 8, 9, 11…15,
  packed with no gap where 10 would have been"), and L41's parenthetical
  ("gap, overlap, or out-of-ordinal placement") confirms it. Resolvable.
* **Whether an appender may gratuitously relocate an untouched layer's live
  index region.** §20.3 says "relocating a live index region is compaction's
  operation (§20.5, `[R-WRT-07]`), not an appender's" — a clause carrying no
  BCP 14 keyword. Whichever way it reads, both outputs are conforming files, so
  I implemented the prohibition and moved on.
* **The storage barriers of `[R-LIF-02]` steps 4 and 6.** These are MUST-level
  writer obligations with no witness in any single file, and they appear neither
  in §2.3's closed pair of expressly-declared-conduct rules nor in §21.7's list
  of unwitnessed obligations. Since §21.7 makes no completeness claim of its own
  and §21.1's normative completeness runs only to *detectable file-conformance
  violations*, this is not an omission against any stated claim.
* **`[R-WRT-09]`'s "each relocated extent's checksum".** A compactor that places
  a structure at the offset it already had has not relocated it, so the
  quantifier leaves its checksum unverified. `[R-WRT-01]` already says latent
  violations travel into a compactor's output, so the model absorbs it.
* **§20.4's table header reads "Stored flags" while the section says persistence
  "governs every record type".** Applying the MU = 1 row to a type the updater
  *does* implement would forbid modifying it, contradicting `[R-WRT-07]`'s
  "a compactor implementing one relocates whatever that registration defines".
  The sentence that introduces the table scopes it to types the updater does not
  implement, so I read it that way.
* **§20.5's "so slack is never carried" beside a figure that shows a `pad`.**
  Carried ≠ created; the compacted output's pad and its A_slab run-up are slack
  it creates, which the sentence does not deny.

## 10. Verdict on the charter

The document sufficed to build a non-trivial file byte for byte, to append to
it, to walk all four flag combinations against three flag-authority sources, to
account for every slack byte under five commit shapes, to recover from four
crash points, and to compact — with four places where I had to choose a reading,
none of which moves a byte of a conforming file or a reader's verdict. Every
constant and worked example in the document recomputes correctly, and the §21
register is internally consistent under both a mechanical instance count (277,
as claimed) and a from-the-rule derivation of the rows a writer relies on
(F2, F3, F5, F7, F33, L1, L2, L21, L22, L30, L44, T3, T14, T21, T22, R4).
