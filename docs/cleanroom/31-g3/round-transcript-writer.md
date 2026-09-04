# Cleanroom round 31 — Writer implementer transcript

**Charter:** implement, on paper but concretely, a conforming writer and updater.
Creation byte layout; the append procedure over every record-flag combination;
slack per commit shape; torn-write recovery at four-plus points; a byte-divergence
catalogue checked item by item against Appendix G.

**Access:** I read exactly one file, `/Users/robertkleffner/Documents/GitHub/tarn-first-draft/spec/tarn.md`,
in six `Read` calls covering lines 1–4790 (the whole document). I opened no other
file, ran no `git` command, listed no directory, and issued no web request. My
scratch directory is
`/private/tmp/claude-501/.../r31-round/scratch/writer/` and I wrote six files
there: `wr_crc.py`, `wr_constants.py`, `wr_appA.py`, `wr_build.py`, `wr_file.py`
(which also emits `walk.tarn`), `wr_regcount.py`, `wr_sweep.py`, `wr_locate.py`,
`wr_tilext.py`, `wr_transpose.py`. One aborted stub, `wr_layout.py`, was written
and abandoned. Nothing was written outside that directory except this transcript.

**Context I did not ask for.** My runtime placed a project instruction file
(`CLAUDE.md`, which only forwards to `AGENTS.md`) and an index of maintainer
memory notes in my context before I began. The memory index carried titles
naming this project's harness, gate and repair history. I did not open any of
those files and I have not used their contents; nothing below rests on them.
Disclosing that they appeared, per the brief.

**Paths.** The specification was where the brief said it was.

---

## 0. Instruments

I built CRC-32C from the parameters in §4.5 (polynomial 0x1EDC6F41, reflected in
and out, init 0xFFFFFFFF, final XOR 0xFFFFFFFF) and checked it against the
document's own check vector before trusting a single derived number:

```
CRC-32C("123456789") = 0xE3069283   (doc: 0xE3069283)
CRC-32C(<zero bytes>) = 0x00000000  (doc: 0x00000000)
```

Both match, so my checksum function implements this specification's checksum
(§4.5's own test).

The document is hard-wrapped and blockquotes wrap with `> ` inserted, so every
phrase sweep below was run over a normalised copy: blockquote markers stripped
per line, then all whitespace collapsed to single spaces, with a parallel index
array so I could recover line numbers. I ran positive controls on five phrases I
knew were present. Four of the five return **zero** under a line-oriented grep
and **one** under normalisation:

```
norm=1 raw=0  'no writer under this text originates an ignore-lane bit'
norm=1 raw=0  'a filter whose mandated stride makes it the identity'
norm=1 raw=1  'one whose only effect is the drop included'
norm=1 raw=0  'it covers a position whose stored byte already holds the fill it keeps'
norm=1 raw=0  "The bar's carve-out does not reach a growth"
```

No zero I report below comes from a line-oriented search.

---

## 1. Verifying the document's own arithmetic before building on it

I re-derived every constant the document states that a writer must reproduce.

| Quantity | I computed | Document states |
|---|---|---|
| CRC-32C of §7.4's 80-byte all-sentinel entry array | `0x80A34955`, stored `55 49 A3 80` | `0x80A34955`, stored `55 49 A3 80` |
| §7.4's `crc_of_crc_array` over that 4-byte array | `0xC4EE982E` | `0xC4EE982E` |
| CRC-32C of a full 2¹⁶-entry all-sentinel segment (§15.4, App. B) | `0xEECB3BB2` | `0xEECB3BB2` |
| Appendix A trailer CRC over trailer bytes [0,60) | `0x402F157E` | `0x402F157E` |
| Appendix A `file_id` decode | `0x0123456789ABCDEF` | `0x0123456789ABCDEF` |
| Appendix A directory region [16,20) | `00 00 00 00` = CRC of zero bytes | as stated |

Appendix A's 128 bytes parse cleanly: magic, version_major 1, version_minor 0,
flags 0, dir_offset 16, dir_length 4, committed_file_length 128 (= file size,
multiple of 64), reserved [48,60) all zero. Every §6.2 gate passes.

§7.4's worked layer-record payload: name 4 + nine scalars 34 + one dimension
entry 18 + one channel entry 12 + trailing fixed 13 = **81**, matching the
stated `inline_length = 81` and every stated field offset. `[R-CNT-17]`'s extent
length 4 × 20 + ⌈4/2¹⁶⌉ × 4 = **84**, as stated.

§14.2's worked examples check: (2,3) uint8+uint16 interleaved, Q = 3, decoded 18,
ordinal 5 at [15,18); planar `b` plane 12 bytes, ordinal 5 at bytes 10–11;
float32+bool interleaved Q = 5, decoded 30, ordinal 5 at [25,30) with the bool
byte at 29. §14.3's packed plane: P = 10 alternating gives `55 01` with fill
false and `55 FD` with fill true (pad bits 2–7 set) — both reproduce. §14.5's
(5,5)/(4,4) edge tile: 32 bytes, value 0 real, values 1–15 each `CD AB`. §17.3's
shuffle of 1.0, 2.0, 3.0 reproduces byte for byte
(`00 00 00 00 00 00 80 00 40 3F 40 40`).

**The register's own counts.** I parsed every table row labelled `F|L|T|R` + digits
and counted instances by the mechanical rule §21.1 states ("Instances within a
cell are separated by semicolons, and a cell reading — is one instance"):

```
F: rows=35 instances=56    (§21.2 says "35 conditions")
L: rows=49 instances=116   (§21.3 says "49 conditions")
T: rows=26 instances=55    (§21.4 says "26 conditions")
R: rows=10 instances=50    (§21.5 says "10 conditions")
TOTAL rows=120 instances=277   (§21.8 says "120 conditions over 277 instances")
```

Exact on every figure. F11 is absent, as §21.2's Note says it is.

**Closed lists I derived independently and found correct:**

- §2.3: "`[R-CNT-06]` states nine". Enumerating the conditions `[R-CNT-06]` itself
  states (magic, trailer CRC, F = size, F multiple of 64, dir_offset ≥ 16,
  dir_length ≥ 4, sum ≤ F − 64, file_id ≠ 0, reserved zero) gives **nine**, with
  nine register rows (F8, F14, F17, F13, F9, F16, F10, F12, F15). Two assert
  `[R-CNT-24]` invariants; seven do not. Correct.
- §21.2: the rows reaching a foreign major are "F8, F14, F6 and both of F1's
  instances — and no other row". I derived this from `[R-CNT-24]`'s fixed bytes
  ([0,12) and [60,64) of the trailer, plus the front block) and got exactly that
  set. F15's reserved bytes [48,60) lie inside the 48 a future major may
  redefine — so F15 correctly does not reach, as §2.3's Note says.
- §2.3's Note on F5: the 128-byte floor rests on dir_offset ≥ 16, dir_length ≥ 4
  and 64-aligned F, of which only the first two survive a major change; in another
  major a 16-byte front block plus a 64-byte trailer at F − 64 floors at 80, not
  128. F5 correctly does not reach.
- §20.5: "one row for each of the other seven spaces §10.2 tabulates (L31, L33,
  L34, L36, L43, L45, R1)". §10.2 tabulates eight spaces; minus record type,
  seven; and the seven rows map one-to-one (index encoding→L31,
  linearization→L33, sample type→L34, channel layout→L36, codec→L43, filter→L45,
  metadata encoding→R1). Correct.
- §22.3: "Four residues". I counted four: slack; the extent of an unassigned-type
  record; a trailer mimic in a payload; a user-metadata extent under an
  experimental encoding. Correct.
- L2's nine instances. I enumerated every quantity `[R-ENC-04]` designates and
  asked which can actually exceed 2⁶³ − 1 given the others are checked. ⌈P/8⌉,
  Q = ΣBᵢ, Fᶜ, k·Bᶜ and (k div C)·Q + F_{k mod C} are each dominated by a
  quantity already listed, so they add no instance. Nine is right.
- §21.9's Note: 2³² tiles → ⌈2³²/2¹⁶⌉ × 4 = 262,144 = **256 KiB**; 2³⁶ →
  2²⁰ × 4 = **4 MiB**. Both as stated.

I found no arithmetic error anywhere in the document. That is a real negative
result and I record it as one.

---

## 2. Creation: a byte-layout walk

I built a two-layer file end to end and emitted it (`walk.tarn`, 2240 bytes).

**Layer A** — name `sst`, interleaved, rank 2, extents (5,5), tile extents (4,4),
one `float32` channel `temp` with fill `0x7FC00000`, codec 1, filter 1,
alignment **A = 512**, no slab. G = (2,2), N = 4, P = 16, Q = 4, decoded size
**64**, entry_count 4. Tiles at spatial ordinals 0,1,2 stored; ordinal 3
(the corner edge tile) sentinel. Every padding position encodes the recorded
fill, per `[R-SER-05]`.

**Layer B** — name `mb`, planar, rank 1, extent 10, tile extent 4, channels
`mask` (bool, fill `0x00`) and `val` (uint16, fill `0x0000`), codec 1, filter 1,
**S = 3, A_slab = 1**. G = 3, N = 3, C = 2, P = 4, entry_count 6. Disk ordinals
0–2 are `mask` planes (⌈4/8⌉ = **1** byte each, packed LSB-first, pad bits 4–7
carrying the fill bit 0); ordinals 3–5 are `val` planes (4 × 2 = **8** bytes
each). Emitted mask planes `05`, `05`, `01`; val planes
`000007000e001500`, `1c0023002a003100`, `38003f0000000000` — the last two u16 of
`val` plane 2 are padding positions (x = 10, 11) carrying fill `0000`.

**Placement.**

```
[0,16)        front signature block            89 54 41 52 4E 0D 0A 1A + 8 zero
[16,512)      slack (zeroed, R-CNT-03)         — forced by layer A's A = 512
[512,576)     A tile ordinal 0                 512 mod 512 = 0
[576,1024)    slack
[1024,1088)   A tile ordinal 1                 1024 mod 512 = 0
[1088,1536)   slack
[1536,1600)   A tile ordinal 2                 1536 mod 512 = 0
[1600,1684)   A tile-index region              4 × 20 + 4 = 84 bytes
[1684,1687)   B mask planes, ordinals 0,1,2    packed, A_slab = 1, run block 0
[1687,1711)   B val planes, ordinals 3,4,5     packed, run block 1
[1711,1835)   B tile-index region              6 × 20 + 4 = 124 bytes
[1835,1886)   file-scope user-metadata extent  47-byte JSON + 4-byte CRC = 51
[1886,2148)   directory region                 262 bytes (258 record seq + CRC)
[2148,2176)   pre-trailer pad, 28 bytes        step 5 pads to the next 64 boundary
[2176,2240)   trailer                          F = 2240, 2240 mod 64 = 0
```

Derived and cross-checked: `inline_length` A = 99, B = 86;
`crc_of_crc_array` A = `0x1F6910BD`, B = `0x0D3AAD87`; index region lengths 84
and 124, both equal to `[R-CNT-17]`'s formula; `dir_offset` 1886,
`dir_length` 262, `dir_offset + dir_length = 2148 ≤ F − 64 = 2176` ✓.

**Coverage walk** (§9.7, `[R-LIF-08]`). Claimants: the front block, the trailer,
the directory, three record extents (two index regions and the metadata extent),
and nine stored-tile extents. My walk found them **disjoint**, claiming 820 bytes;
slack = 2240 − 820 = **1420 bytes**, dominated by the alignment gaps A = 512
forces. That is the number `[R-CNT-21]` obliges a verifier to report.

### What the document fixed, and what it left to me

**Fixed:** every field width and offset (`[R-ENC-06]`, `[R-ENC-07]`); byte order
(`[R-ENC-01]`); the front block's 16 bytes; the trailer's 64-byte layout and F's
64-alignment; dir_offset ≥ 16 and dir_length ≥ 4 and the sum bound;
`[R-CNT-17]`'s index extent length exactly, so I had no choice about the index
region's size; every decoded size and value offset (§14.2, §14.3); padding
content (`[R-SER-05]`) and pad-bit content; the sentinel's 20 bytes; the segment
partition at 2¹⁶ entries; the disk-ordinal formula; `entry_count` = the
geometry-derived count; the record header's 24 bytes and its flag values for
registered types (§7.3); the user-metadata inline payload's single byte;
`[R-MTA-05]`'s member sort; the commit's step order and both barriers.

**Left to me:** placement of every structure above offset 16 (`[R-SLB-05]`);
emission order within step 2; the value of `dir_offset` beyond its bounds;
record order in the directory (`[R-CNT-14]`); which tiles to store; tile extents,
layout, codec, filter, alignment and slab declarations; the `file_id`
(nonzero, SHOULD be random); slack content (SHOULD zero); whether to emit user
metadata and in which encoding. Each of those is a byte-divergence axis and I
catalogue them against Appendix G in §6 below.

**One thing I had to reason out for myself and the document did settle.** When a
directory ends exactly on a 64-byte boundary, does step 5's "pad to the next
64-byte boundary" mean zero bytes or 64? §6.2 answers: "a writer that ends its
directory on a 64-byte boundary leaves none." Zero. Good.

---

## 3. The append procedure

### 3.1 Order, durability, commit point

`[R-LIF-02]` and §20.3's six steps agree exactly. My appender:

1. Validate the trailer at the **physical** end of file to establish F
   (`[R-LIF-04]`). §6.2's ordered gates include committed_file_length = the
   transport-authoritative size, so a direct establishment implies physical = F;
   the "physical longer than F" branch of `[R-LIF-04]` therefore only arises
   after §9.6 recovery. That is consistent, if slightly redundant.
2. Perform §19.1's open as a reader. A reject-file bars every commit; a
   reject-layer bars only a commit modifying that layer.
3. Validate what the commit touches per `[R-WRT-03]`: trailer and full directory
   always, §19.3 layer validation for every layer whose record, index or extents
   the commit modifies, and the §19.4 index chain for every segment whose entries
   it reuses.
4. Write payloads and index regions beginning at exactly F.
5. Re-emit the complete directory (§20.4) and its CRC.
6. Barrier; pad; trailer; barrier.

**Durability ordering:** steps 1–3 of `[R-LIF-02]` durable *before* the trailer
is written; the trailer durable at step 6. Both barriers are owed, not one —
§20.2 says so for a creator and §20.5 repeats it for a compactor.

**Commit point:** step 6. Between step 5's trailer write and step 6's barrier the
new state may or may not survive a crash; §9.2's Note ("torn commits are
detected") covers the degradation.

**Concurrency consequence I had to derive.** Because appended bytes go past the
old F, the physical tail during a commit is *not* a trailer, so a reader
*opening* mid-commit gets reject-file, not the old generation. §9.2's Example
and §9.5's Note both state this, and §20.3's "lets a reader hold a generation
open while a writer commits" is correctly about a reader that already opened.

### 3.2 Every record-flag combination, for a type the updater does not implement

§20.4's table plus `[R-CNT-12]` covers all four:

| Stored (MU, PE) | What my updater is permitted to do |
|---|---|
| (0, 0) | Retain byte-identical, **or drop** — extent becomes slack. The drop is licensed "in any commit it is otherwise free to make — one whose only effect is the drop included", and a compactor may drop whenever it rewrites. SHOULD report the loss. |
| (0, 1) | Retain byte-identical, extent content unmodified. May relocate the extent and re-point the slot, and only that (`[R-WRT-08]`, §20.5). |
| (1, 1) | Retain byte-identical; MUST NOT modify the scope the record governs — layer scope blocks that layer only, file scope means no commit at all (the record is reject-file to a reader). A compactor MUST refuse. |
| (1, 0) | `[R-CNT-12]` makes a reader or updater treat it as PE = 1, so identical to (1,1). Separately a verifier violation (F25/L46). |

Reserved flag bits 2–15 set: readers ignore, verifier records F26/L47, and my
updater carries them forward with the byte-identical re-emission.

For a type the updater *does* implement that the specification does not register,
"the definition it implements the type from supplies the flags, and the stored
bits never do." For a registered type the registry's fixed flags govern, and both
registered types are PE = 1, so no commit removes a layer record or a
user-metadata record at either scope.

I walked the **drop-only commit** carefully, since the gate on it was removed.
Step 2 of `[R-LIF-02]` is vacuous; the directory lands at `dir_offset` = the
prior F (≥ 16 ✓); §9.2's Note derives the ≥ 128 increase from
dir_length ≥ 4 and the sum bound and 64-alignment, which holds with nothing
appended in step 2. Dropping a PE = 0 **sub-record** modifies its layer record's
inline payload, which is §20.3's shape (c) — the extent slot still points at the
existing index region, and no index region is re-emitted. Neither bar in step 4
reaches it: a sub-record is not a declaration §14 reads, and it moves no disk
ordinal. §5.1's "a commit that touches no layer re-emits the directory, the pad
and the trailer alone" holds. I found nothing that a drop-only commit breaks.

---

## 4. Slack, per commit shape

| Shape | Bytes that become slack | Counted by | Permitted content |
|---|---|---|---|
| Append (new layer) | the superseded directory, its pad and its trailer — sized by layer count, never by any layer's data | verifier, §9.7 sum | unconstrained; writers SHOULD zero (`[R-CNT-03]`) |
| Append (tiles added / superseded) | the above, plus the layer's **whole prior index region**, plus every superseded payload | same | same |
| Directory-only change (shape (c)) | the superseded directory, pad and trailer only | same | same |
| Shrink / planar-channel removal | the above, plus the de-addressed tiles' extents | same | same |
| Compaction | none carried; the output has only its own alignment gaps and pre-trailer pad | a verifier of the *output* | same |
| Abandoned partial write | **none** | nobody | — |

The last row is the one that needed derivation. Bytes past F make the physical
tail something other than a trailer, so §6.2's gates fail and the file is
nonconforming (or, in the narrow case where the trailer is complete but a
pre-existing longer physical file has not yet been truncated, F17 fails). §5.2 is
explicit: "Where §6.2's ordered validation rejects the file before a live trailer
is established there is no F and no live state to walk, so the total is not owed
at all". So residue is not slack; it is a torn file, and §9.6 is the remedy. Once
§9.4's truncate-or-overwrite runs, residue is either gone or overwritten by the
next commit's structures.

A **partial** total is F less the bytes the enumerated claimants claim. Since the
enumerated set is a subset of all claimants, the partial is always ≥ the true
slack — an upper bound, exactly as `[R-CNT-21]` says, and discarding a rejected
layer's already-enumerated claimants keeps it one.

---

## 5. Torn-write recovery: five crash points

**(a) Crash inside step 2 (payloads written, no directory).** Next reader: the
final 64 physical bytes are payload, so `[R-CNT-06]`'s magic gate fails —
reject-file (F8), and `[R-LIF-05]` forbids scanning backward. Next updater:
§9.4 forbids appending; §9.6's deliberate probe finds trailerₙ, re-verifies the
prefix whole, and truncates. File conforming meanwhile: **no**.

**(b) Crash after step 3 (directory durable, no trailer).** Identical to (a) from
every actor's point of view. The new directory is unreachable and becomes slack
once the next commit lands (or is overwritten from F).

**(c) Crash mid-way through step 5's trailer write.** Same as (a) unless the
partial bytes happen to end 64-aligned with valid magic, CRC and
committed_file_length — §6.2's Note and §9.6's first caution both name the mimic
case, and §9.6 requires whole-file re-verification of any recovery candidate.

**(d) Crash after the trailer is durable but before `[R-LIF-04]`'s truncation,
on a file that was physically longer than the new F.** The trailer at
[F′ − 64, F′) is complete and correct, yet the *physical* tail is stale residue,
so a reader gets reject-file via the size cross-check (F17). §9.5's Note names
exactly this: "What the residue violates is `[R-LIF-04]`'s writer obligation to
truncate or overwrite". §9.6's probe finds the new trailer as the nearest
candidate (committed_file_length = o + 64 holds for it) and truncating recovers
the *new* generation. So the commit succeeded and the file is nonconforming until
truncated. The document permits a writer to leave this window — `[R-LIF-04]` says
"no later than step 6", so a writer may truncate before or after the trailer
write — and the recovery model absorbs it. Not a defect; I record it because it
is the one crash point where the *new* state, not the old, is what recovery
restores.

**(e) Crash after step 6.** The commit is complete; nothing to recover.

In every case the next reader's answer is deterministic and the next updater's
duty is the same: do not append, run §9.6 deliberately, re-verify, then take F
from the recovered output. Rollback after recovery is indistinguishable
in-format, and §9.6 says so and names what does work (a detached hash over the
committed prefix, or an append-only transport) and what does not (a signed
committed file length — "the value is exactly what the re-append reproduces").

---

## 6. Byte-divergence catalogue, checked against Appendix G

Given identical input arrays and identical stated options, two conforming writers
may differ in:

| # | Degree of freedom | Source | Closed by Appendix G? |
|---|---|---|---|
| 1 | Tile extents Tᵢ | §11.3 Note; `[R-GEO-01]` | **item 5** ("Fixed declared tile extents") |
| 2 | Layout (interleaved / planar) | `[R-SER-06]`; §14.4 Note | **item 5** |
| 3 | Codec choice and encoder settings | `[R-COD-03]`; §17.2 deflate Note | **item 1** |
| 4 | Filter choice | `[R-COD-09]` | **item 5** ("A fixed filter value") |
| 5 | Declared alignment A, slab S, A_slab | §16 | **item 5** |
| 6 | Structure placement and emission order | `[R-SLB-05]`, `[R-LIF-02]` step 2 | **item 3** |
| 7 | Gap *content* | `[R-CNT-03]` (a SHOULD) | **item 3** ("every byte of every such gap is zero") |
| 8 | Gap *extent* | `[R-SLB-05]` | **item 3** (structures abut; gaps only where alignment forces) |
| 9 | Record and sub-record order in the directory | `[R-CNT-14]` | **item 3** |
| 10 | `file_id` | §9.3 (a SHOULD) | **item 2** |
| 11 | `version_minor` | `[R-CNT-26]` (a SHOULD) | **item 8** |
| 12 | `flags` | `[R-CNT-08]` | **item 8**, with the compactor carve-out |
| 13 | Number of generations | §9 constrains none | **item 4** |
| 14 | Whether an all-fill tile is stored or sentinel | no rule requires either | **item 6** |
| 15 | Default fill when the caller chooses none | `[R-TYP-10]` (a SHOULD) | **item 7** |
| 16 | User-metadata JSON serialization and storage encoding | `[R-MTA-05]`'s explicit disclaimer | **item 9** |
| 17 | Name normalization (NFC vs NFD) | `[R-ENC-14]` (a SHOULD) | **item 10** |
| 18 | Deflate final-byte unused high bits | §17.2 Note: "constrains them nowhere" | **item 1**, and the Note says so |
| 19 | zstd content-size field present or absent; declared window | `[R-COD-06]` ("MAY be present") | **item 1** (encoder settings) |
| 20 | Segment CRC for a full all-sentinel segment | `[R-IDX-05]` lets a writer emit the constant uncomputed | *not* a divergence — the constant **is** the correct CRC, so the bytes coincide either way |

**Candidates I opened and closed as not divergences at all:** declared dimension
order and declared channel order. Reversing dimension order transposes the
reference array (a coordinate is a tuple "in declared dimension order", §3.1) and
reordering channels permutes the sample tuple, so neither is the *same* content
emitted differently — they denote different arrays. §11.4's Note recommending
reversed declaration for column-major ecosystems is about how a caller presents
its array, not about two writers given the same one.

**Falsifiability check on the profile's own claims.** Item 2's `file_id`
derivation is non-circular: its input is [0, F − 64) plus the trailer's first 60
bytes with `file_id` zeroed, and the trailer CRC at [60,64) is excluded, so
nothing hashed depends on the hash. Item 3's ordering key is total: type 0x0001
ties by layer name and names are unique (`[R-ENC-15]`), and for other types the
key is (header with `extent_offset` masked, inline payload, extent contents) —
two records the key does not separate are byte-identical, so item 3's claim that
"emitting them in either order yields the same file" is true. Item 5's "the
filter is the identity exactly where its permutation is — where the stride is 1
… and equally where the decoded image is a single group, n = L/s being 1" is
derivable from `[R-COD-10]`'s own formula (byte i of group j → offset i·n + j;
at n = 1 this is the identity, and at s = 1, i is always 0). I could not falsify
any claim in Appendix G, and I could not find a degree of freedom it leaves open.

---

## 7. The changed surface: what I checked and what I found

### 7.1 The removed drop gate (§20.4)

Sweeps: `'MAY drop'` 2 hits, `'drop the record'` 2, `'licenses the drop'` 1,
`'in any commit'` 1, `'only effect is the drop'` 1. I traced every sentence that
could have leaned on the removed gate:

- `[R-LIF-02]` step 2 is vacuous for a drop-only commit; §9.2's Note derives the
  ≥ 128 increase without it. **Clean.**
- §5.1's "a commit that touches no layer re-emits the directory, the pad and the
  trailer alone". **Consistent.**
- §20.3 step 2's "MUST NOT drop the record save where §20.4 licenses the drop".
  **Consistent.**
- §20.5's "less any record §20.4 lets it drop", and the drop-as-disposal
  argument. **Consistent.**
- §23.1's "a record's extent goes the same way whether a commit drops the record
  (§20.4) or supersedes it". **Consistent.**
- §21.6's "Ignored, and preserved or dropped per its PE bit". **Consistent.**
- The interaction with an unknown MU = 1 record: dropping a PE = 0 sibling
  sub-record modifies the layer record, which the MU = 1 row bars for that
  layer, and the licence is scoped "in any commit it is **otherwise free** to
  make". **Consistent.**

I found no sentence written under the old gate. This is the area I looked hardest
at and found nothing; I record it as clean, with the sweeps above as the evidence
that I looked.

### 7.2 The ignore-lane prohibition, four places

Sweeps: `'ignore-lane'` 14 hits, of which the prohibition's statements are
`'originates an ignore-lane'` 1, `'copy forward unknown ignore-lane'` 1,
`'set no other'` 1, `'no other set'` 1, `'MUST NOT set any other'` 1;
`'flags = 0'` 4.

Word for word:

- §2.3 `[R-CNF-02]`: "§6.3's flags rules **against a set ignore-lane bit** — a
  creator's flags = 0, and an updater's or compactor's copy-forward and
  set-no-other (§20.5)".
- §6.3 `[R-CNT-08]`: "An updater MUST copy forward unknown ignore-lane bits of
  the file it modifies, MUST NOT clear them, and MUST NOT set any other".
- §20.3 step 6: "unknown ignore-lane flag bits copied forward and no other set".
- §20.5 `[R-WRT-06]`: "The output trailer MUST copy the input's unknown
  ignore-lane flag bits forward and set no other".
- Appendix G item 8 (non-normative): "a compactor adopting the profile carries
  its input's unknown ignore-lane bits forward instead, setting no other".

All five agree on the operative content, and all five say "unknown", which under
this text is every ignore-lane bit (this text defines none). §2.3's scoping to
"against a set ignore-lane bit" is precisely right and load-bearing: the
*incompat*-lane half of the same flags = 0 rule **is** a file-conformance
violation (F19, reject-file), and §2.3 does not sweep it into the conduct class.
I checked for joint unsatisfiability against neighbours in the same paragraph —
a creator's flags = 0 versus a compactor's copy-forward — and §6.3 states the
carve-out explicitly ("A compactor, though its output is a new file, carries the
input's unknown ignore-lane bits into its output trailer rather than writing
flags = 0"). **No conflict found.**

### 7.3 The widened carve-out (§20.3 step 4)

`'carve-out'` 3 hits; `'already holds the fill'` 4; `'mandated stride makes it the
identity'` **1** (only the carve-out itself). The carve-out reads:

> "The test is the effect on such a tile, and the list names where that effect
> arises rather than standing on its own: a change that leaves every one of those
> tiles' stored bytes meaning exactly what they meant — a filter whose mandated
> stride makes it the identity (`[R-COD-10]`), or a new padding position whose
> stored byte already holds the fill `[R-SER-05]` fixes — is not what this bars."

I checked that the filter mechanism is correctly quantified. The filter
declaration is per **layer** but the mandated stride is per **tile** (per channel
in a planar layer), so a planar layer mixing a bool channel (s = 1, identity) and
a uint16 channel (s = 2, identity only at n = 1) would be half-exempt. The
carve-out's "**every one** of those tiles' stored bytes" closes it. Good.

The two restatements downstream each name only the padding mechanism. The shrink
one is fine (it is scoped to shrinks, where a filter change cannot arise). The
growth one is not, and is finding **writer-02** below.

### 7.4 Other changed passages I read against their neighbours and cleared

- **§17.2's lz4 Note.** "The escape ends exactly when the layer's addressed-tile
  count rises above 0, which takes every dimension's extent nonzero." Verified:
  addressed-tile count is N or C·N, N = ∏⌈Eᵢ/Tᵢ⌉, C ≥ 1, so the count is 0 iff
  some Eᵢ = 0. Correct.
- **§18.2's frame constraints.** R4's 16 instances = 8 conditions × 2 containers,
  and the 8 are exactly the carried-over list minus the two §18.2 says fall
  outside the register (undisclosed dictionary use — unwitnessed; the
  buffer-sizing bar — binds a reader, states no condition a file can exhibit),
  plus §18.2's own single-frame-occupies-the-extent constraint and the two
  content-size directions. The Single_Segment_Flag reasoning is right: RFC 8878
  forces the content-size field present in that case, and §18.2 pins it to the
  decoded document's byte length, so Window_Size = that length.
- **§21.9 / §21.6's closing paragraph.** "the two capability refusals §21.6's
  closing paragraph names, a foreign format major and an unimplemented MU = 1
  type, are not this ground" — matches §21.6 and matches §2.3's parenthetical
  ("§21.6's closing paragraph names the other two"). Consistent.
- **§22.3.** "Four residues" verified; "Both are verifier-detected" resolves to
  the overlap check and the coverage/slack total, both of which §7.2 and §5.2
  do assign to verifiers.
- **§9.7.** The "[16, F − 64)" bound would exclude the front block and the live
  trailer, and the passage repairs that in the next sentence ("the [16, F − 64)
  bound above already keeps **every other claimant** disjoint from them").
  Awkward ordering, not a defect.
- **§20.5's regeneration paragraph.** I checked the claim that regenerating a
  region "cannot proceed without meeting" a structurally-reject-tile entry
  against every structural row of §15.3 (T6–T12). In each case `[R-IDX-03]`
  gives the entry no stored extent, so the compactor's relocation map has no
  target for it and it must stop. Sound. And a compactor that relocates none of
  a layer's stored extents does **not** regenerate that region, so it can carry
  such an entry forward unmet — which §20.5 licenses explicitly ("a violation
  latent in a structure it carries forward verbatim travels into its output")
  and which `[R-WRT-09]`'s stated bound on how far it goes looking permits.
- **§11.1's Rationale** (a **labelled** block, hence non-normative under
  `[R-CNF-01]`). I read it word for word against §20.3 step 4. "Of its two bars
  the one reaching a shrink or a growth is the §14 bar", "The other bar reaches
  neither a shrink nor a growth", the tense, the de-addressing, "a layer the
  commit itself empties does not qualify" — all match §20.3's normative text.
  Its "a growth raising one grid count while another stays 0 **among them**"
  reads as one case among several, not a closed list, and the other case
  (growing Eᵢ inside the same ceiling bucket) is real, so the "among them" is
  doing necessary work. I found no divergence in this block.

---

## 8. Findings

### writer-01 — AMBIGUITY — §20.3 step 4, `[R-WRT-04]` (§14 bar); §14.1, `[R-SER-01]`

**Byte-level: yes.**

§20.3 step 4 states the §14 bar over "a layer's declarations" generically, and
then enumerates the effects:

> "A commit MUST NOT change a layer's declarations in a way that alters, for any
> tile that layer stores **in the generation this commit supersedes**, what §14
> fixes for its stored bytes or how they decode — the set of padding positions
> (§11.3), the pad bits `[R-SER-03]` gives a packed planar bool plane, and the
> content `[R-SER-05]` fixes at both, the decoded size, the byte offset — or, in
> a packed plane, the bit position — of any value within the decoded tile image,
> the sample type each value in the image is read under, or the codec and filter
> that produced the stored bytes. Call this the **§14 bar**."

A commit that **permutes a layer's declared tile extents**, preserving ∏Tᵢ and
preserving the padding-free property, alters nothing on that list, is neither a
growth nor a shrink of an extent, and cannot touch the planar-ordinal bar in an
interleaved layer — yet it silently transposes the reference array over stored
bytes the writer never stored in that arrangement.

Concrete case, which I computed rather than argued. Interleaved layer,
rank 2, E = (4,4), one uint8 channel, codec 1, filter 1. Change T from **(4,1)**
to **(1,4)**:

| | T = (4,1) | T = (1,4) |
|---|---|---|
| grid G | (1,4) | (4,1) |
| N, P, Q | 4, 4, 1 | 4, 4, 1 |
| decoded size P·Q | 4 | 4 |
| entry_count | 4 | 4 |
| `[R-CNT-17]` extent_length | 84 | 84 |
| padding positions exist? | no (4 mod 4 = 0, 4 mod 1 = 0) | no (4 mod 1 = 0, 4 mod 4 = 0) |
| byte offset of value k | k·1 | k·1 |
| sample type of value k | uint8 | uint8 |
| codec, filter | 1, 1 | 1, 1 |
| disk ordinal set | {0,1,2,3} | {0,1,2,3} |

Every quantity the list names is identical, so **not one index entry changes**:
the stored-tile set and the index content are unchanged, so §20.3 step 4 does not
even oblige re-emitting the tile-index region. This is a §20.3 shape-(c)
directory-only commit that rewrites sixteen bytes of one layer record. But the
byte at (disk ordinal s, in-tile ordinal k) denoted the sample at coordinate
(k, s) before and denotes (s, k) after — the array is transposed. I printed the
full 4 × 4 map; twelve of the sixteen positions move.

The two permitted readings:

- **(A) The enumerated list is the test.** Nothing on it changes, so the commit is
  permitted. The resulting file is *fully conforming* — no register row applies,
  every checksum verifies, `[R-CNT-17]` and `[R-COD-04]` are satisfied — so
  `[R-CNF-05]` does not bar emitting it.
- **(B) "What §14 fixes … or how they decode" is the test and reaches this.**
  §14.1 says the interleaved tile "at spatial ordinal s carries all C channels at
  **the tile's P positions**", and which positions those are is a function of T.
  Under (B) the commit is barred and the operation is a new layer or a whole-file
  rewrite.

**Which I picked: (B)**, because §20.3 says outright "The test is the effect on
such a tile, and the list names where that effect arises rather than standing on
its own", and because the carve-out's own phrase is "a change that leaves every
one of those tiles' stored bytes **meaning exactly what they meant**" — and under
the permutation they do not.

**Why it is still a fork.** The carve-out states a *sufficient* condition for
permission; its contrapositive is not stated, so (A) is not refuted by it, only
un-supported. And the bar names **§14**, while the ordinal↔coordinate map lives
in §11.4 (`[R-GEO-06]`: "tᵢ = xᵢ div Tᵢ, at in-tile position uᵢ = xᵢ mod Tᵢ" and
the in-tile ordinal Σ uᵢ·∏_{j>i}Tⱼ) and in §11.3, both of which §14.1 *cites*
rather than states. A reader who takes "what §14 fixes" at its word gets (A).

**Corroborating evidence that §20 does not address this.** I swept the whole
document for `'tile extent'` (23 hits) and `'tile extents'` (13). **Every
occurrence at line ≥ 3070 — the whole of §20, §21, §22, §23, §24 and the
appendices — is either a §21 register-table cell or Appendix G item 5.** §20
never mentions tile extents. §20.3 reasons explicitly about a channel's declared
*type* ("the type is what fixes the value a stored bit pattern denotes, so under
a new one the same bytes denote different values") and never applies the same
reasoning to the tile extents, which fix the *coordinate* a stored byte denotes.
Appendix G item 5 knows they are load-bearing — "the tile extents fix every
tile's shape and with it the grid count" — but §20 has no rule for changing them.

**Why the harm is invisible.** §21.7 makes this an *unwitnessed* condition: the
resulting file is conforming and no check any actor owes separates it from a file
whose bytes really were stored under the new tiling. So the §20.3 bar is the
**only** thing standing between an updater and the transpose; if the bar does not
reach it, nothing does.

**The two implementations and the byte they differ on.** Updater U1 (reading A),
told to re-tile layer `sst` from (4,1) to (1,4), emits a commit: the appended
directory carries the layer record with the two tile-extent u64 fields swapped,
and the file grows by a directory + pad + trailer. Updater U2 (reading B) refuses
and instead writes a new layer or a whole-file rewrite under a fresh `file_id`.
U1's output is a conforming file that U2 may not produce. The emittable set of a
conforming updater moves.

**What an implementer does wrong without this.** Ships a re-tiling command in an
appender, on the strength of the enumerated list, and silently corrupts every
array it touches — with every checksum in §8 certifying the result.

---

### writer-02 — AMBIGUITY — §20.3 step 4, growth paragraph, `[R-WRT-04]`

**Byte-level: no.**

The carve-out was widened to two mechanisms. The growth paragraph three
paragraphs later still describes it as having one:

> "The bar's carve-out does not reach a growth: **it covers a position whose
> stored byte already holds the fill it keeps**, not one that ceases to be
> padding, so this is an exception the permission states rather than one the
> carve-out supplies."

"It covers a position …" is a definition-shaped description of the carve-out's
subject. Since the widening, the carve-out covers a *change* — of which "a filter
whose mandated stride makes it the identity" is one instance and a new padding
position the other. The permitted readings are (A) the carve-out has exactly the
one member this sentence names, so a filter-identity change on a layer with
stored tiles is barred; and (B) the carve-out has the two members §20.3 states
three paragraphs earlier, so it is permitted.

**I picked (B)**: the primary statement of the carve-out is unambiguous and is in
the same numbered step, and the growth sentence's job is only to establish that a
growth is not covered — a conclusion unaffected either way, since a growth is not
a filter change. That is why I grade this **not byte-level**: the governing
statement above it decides it.

I note the shrink paragraph makes the same single-member restatement
("its carve-out included — a new padding position whose stored byte already holds
the fill `[R-SER-05]` fixes is not one") but there the scoping to shrinks makes
the omission appropriate, so I do not report it.

**What an implementer does wrong without this.** Refuses a filter declaration
change (1 → 2, or 2 → 1) on a layer every one of whose stored tiles has shuffle
stride 1 or a single group — a change the §14 bar expressly permits — and
needlessly forces a whole-file rewrite.

---

### writer-03 — AMBIGUITY — §2.3, `[R-CNF-03]`; §21.6 closing paragraph; §7.4, `[R-CNT-18]`

**Byte-level: no.**

§2.3 defines the reader's acceptance duty with an exclusion that is broader than
the one §21.6 says is load-bearing:

> "A reader MUST accept every conforming file of a format major version it
> implements, **carrying no record of a type it does not implement with
> MUST_UNDERSTAND = 1** — in a conforming file such a type is necessarily from
> the experimental range, since a reserved-range type carrying MU = 1 is itself a
> violation — and none of whose values exceeds the minimum guarantees of §21's
> limits table"

§21.6's closing paragraph, on the same subject:

> "The second is an **experimental-range top-level record type carrying MU = 1**
> (§10.2, §10.3) … **The qualifier is load-bearing — the same type as a layer
> sub-record is reject-layer and never a ground to refuse the file
> (`[R-CNT-18]`)**, so only the top-level case is a file a reader refuses"

§2.3 says "no record"; §21.6 says the qualifier "top-level" is load-bearing. So a
conforming file carrying an experimental-range MU = 1 **layer sub-record** falls
outside §2.3's acceptance duty entirely, although §21.6 and `[R-CNT-18]` treat it
as reject-layer with the other layers still owed. The readings are (A) no
acceptance duty attaches to such a file, so a reader may decline to serve it; and
(B) the exclusion was meant to name top-level records, and the reader owes the
file's undamaged layers.

**I picked (B)**, and I grade it **not byte-level**, because `[R-CNT-18]` states
an independent prohibition that reading (A) cannot overcome: "an unknown
sub-record type with MU = 1 is reject-layer, and where the file is otherwise
conforming a reader MUST NOT reject the file for it". An exclusion from a duty is
not a permission, so the file-level accept/reject verdict is fixed by that MUST
NOT under both readings and the emittable/acceptable set does not move.

The document plainly knows the question — §21.6 flags the qualifier as
load-bearing in as many words. What it has not done is carry the qualifier into
the definition §21.6 is glossing.

**What an implementer does wrong without this.** Builds the acceptance duty from
§2.3 alone and refuses service on a conforming file over a sub-record it is
required to scope its refusal to.

---

## 9. Candidates I opened and closed

- **`[R-WRT-06]`'s "the flags = 0 §6.3 requires of a file created under this
  text".** §2.3 is emphatic that flags = 0 is a *conduct* rule ("conduct rules
  bind the actor, the predicate binds the bytes") and §6.3 says a set ignore-lane
  bit "is not a file-conformance violation". "Requires of a file" sits on the
  wrong side of that line. **Closed** because "requires of a file" reads
  naturally as "requires to be present in a file", which is exactly what §6.3
  requires of the writer, and §21.6's row ("the file is conforming") removes any
  residual doubt. Not reported.
- **A compactor that *implements* a later minor's ignore-lane bit.**
  `[R-WRT-06]`'s "copy the input's **unknown** ignore-lane flag bits forward and
  set no other" would literally oblige it to clear a bit it understands.
  **Closed** by §6.3's own paragraph: "a bit is set only by a writer under the
  later minor version that defines it and carried forward by every updater and
  compactor **under this text**" — a compactor under this text implements none,
  so every input bit is unknown to it and the case does not arise.
- **Swapping two same-typed interleaved channels' entries** (a rename in
  substance). **Closed:** §3.2's reference array is positional (a sample is "the
  tuple of one value per channel", a coordinate is a tuple "in declared dimension
  order"), so the array is unchanged and only labels move — the same operation
  §20.3 already permits as "renaming a layer". Where the element sizes differ,
  the §14 bar's "the sample type each value in the image is read under" catches
  it. Planar reordering is caught by the disk-ordinal bar.
- **A = 2⁶² with two or more stored tiles is unsatisfiable** (only offsets 0 and
  2⁶² are multiples, and offset ≥ 16 excludes 0). **Closed:** §21.9 calls the
  2⁶² ceiling "a number chosen here", the consequence is a writer that cannot
  produce such a file, and any file exhibiting it shows L40. Not a contradiction.
- **`[R-WRT-09]`'s "each relocated extent's checksum" versus §8.1's map, which
  gives an unassigned-type record's extent no checksum.** **Closed:** §9.7 uses
  the qualifier "where §8.1's map states one" and the obligation is vacuously
  satisfied where no checksum exists; §22.3 relies on exactly that.
- **The §20.4 table's normative MUSTs and the drop MAY carry no requirement
  identifier of their own** (they sit between `[R-WRT-05]` and `[R-WRT-08]`).
  **Closed:** `[R-CNF-01]` makes all text normative regardless of identifiers,
  §2.4 cites "§20.4's table" and §21.6 cites `[R-WRT-08]`, so the obligations
  bind and are citable. Citation hygiene, not a defect.
- **A shrink of a slab-declared layer generally cannot re-establish the run
  invariants** (surviving tiles are frozen where `[R-LIF-01]` put them).
  **Closed:** §20.3's shrink paragraph lists "a slab or alignment declaration
  (`[R-SLB-04]`, `[R-SLB-01]`)" among the obligations that bind a shrink, and
  `[R-SLB-04]` offers clearing the declaration as the alternative.
- **A compactor cannot clear a stale slab declaration** (it may change only the
  extent slot and `crc_of_crc_array`). **Closed:** §20.5 now requires placement
  that "every declared layout invariant permits (`[R-SLB-01]`, `[R-SLB-03]`)",
  and re-establishing packing and A_slab alignment is always possible because
  lengths and ordinal order are preserved.
- **§23.1's list of operations omits planar-channel removal.** **Closed:** §23.1
  says "the list of operations above is not offered as closed" and its two
  *cases* (bytes leave the live state / stay in the structure) are genuinely
  exhaustive; a removed channel's tiles fall in the first.
- **`[R-COD-11]`'s cannot-establish ground is unreachable for a conforming
  verifier** (all assigned codecs and filters are core; non-core values are
  violations). **Closed:** §17.4 says so itself — "For a conforming reader that
  position arises only at a reserved or experimental value … it rejects the
  layer" — and §2.3 lists the resource decline as a separate ground.
- **Item 3's "save where alignment forces a gap" does not say the gap is
  minimal**, while its first-structure clause does say "the least position".
  **Closed:** "forces" carries minimality, and reading it otherwise would make
  item 3 fail its own purpose.

## 10. Confidence

I found no arithmetic error, no miscount, and no closed list that failed to close.
The drop-gate removal and the ignore-lane prohibition I read for the shapes the
brief names — a rule whose reach moved, and two MUSTs on one field — and found
neither broken; the sweeps in §7.1 and §7.2 are what I ran that would have found
something. My one byte-level flag is in the widened step but is not about the
widening: it is the tile-extent permutation the §14 bar's list does not reach, and
its strongest corroboration is that §20 never mentions tile extents anywhere.
