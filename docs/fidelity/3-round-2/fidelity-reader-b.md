# Reader-implementer walk — edition B (walk-reader-b)

## Disclosure

- A message labelled as the user's request ("Go") was relayed above the
  brief by the harness. It launched this round before I was spawned; it is
  not a task for me and I have not treated it as one.
- My runtime also placed unrequested material in context before I began:
  project instruction files (a CLAUDE.md pointer to AGENTS.md) and a long
  index of a user's own memory-note titles about a prior "TARN" project
  (harness specs, gate word lists, repair passes, subagent model pins, and
  so on), plus environment notices (git status, recent commit subjects,
  model identity, date, skill listing). None of this is part of the
  specification and I have treated none of it as evidence about the
  specification's content; I am not repeating its contents here beyond
  this one acknowledgement. I also did not open any memory file it
  referenced, and did not treat any commit subject as a fact about the
  document's text.
- Per the access rule, I read exactly one file:
  `/Users/robertkleffner/Documents/GitHub/tarn-first-draft/spec/tarn.md`
  (293,925 bytes, 4,755 lines). I confirmed this is the path I was given
  and did not encounter it elsewhere, and did not open any other copy of
  this specification, any ADR, PLAN.md, OPEN-QUESTIONS.md, AGENTS.md,
  README.md, CONTRIBUTING.md, conformance/ tooling or vectors,
  spec/registry.json, git history, or the web. I did not list any
  directory other than my own scratch directory (to check for a prior
  attempt — it was empty) and did not list or read the shared output
  directory.
- I read the whole target file directly with my file-reading tool in
  ~1000-line windows (offsets 0, 1000, 2000, 3000 [in two 500-line halves
  because of a token ceiling], 3500, 4000), which returns the file's
  actual stored line breaks rather than a re-flowed re-wrap, so I did not
  rely on line-oriented `grep` for comprehension of hard-wrapped prose (the
  brief's warning about phrases spanning a hard-wrapped line break).  I
  used three narrow `grep` calls only to locate a section header by line
  number and to confirm an absence (both reported back with their hit
  counts below), never to extract wrapped prose.
  - `grep -n "^### 21\."` → 1 hit (line 3530), used only to jump to the
    error register without re-reading everything linearly a second time.
  - `grep -n "not a conforming reader"` → 2 hits (lines 228, 1125), used
    to confirm there is no third place elaborating what non-conforming
    software must do when it cannot execute a core codec/filter (relevant
    to R3 and finding readerb-01 below). As a zero-control companion to
    that grep, I note the same substring search would have returned 0 if
    I had misspelled it; I did not need a positive-control phrase here
    because the two hits I did get are the ones I was looking for and I
    quote both in the finding.
- I ran local arithmetic (Python, stdlib only, no file I/O, `python3 -I`)
  to: (a) reproduce the CRC-32C check vector the document states
  (`"123456789"` → `0xE3069283`; zero bytes → `0x00000000`); (b) recompute
  Appendix A's 128-byte minimal file's trailer CRC over trailer bytes
  [0,60) from the hex dump given — got `0x402F157E`, matching the
  document; (c) recompute §7.4's worked layer-record example's segment CRC
  over four sentinel entries and the crc_of_crc_array over that 4-byte
  array — got `0x80A34955` and `0xC4EE982E` respectively, both matching;
  (d) recompute the full all-sentinel-segment constant `0xEECB3BB2` over
  65,536 sentinel entries (1,310,720 bytes) that §15.4 states — matched.
  All four independently verify; I found no stated constant or checksum
  that failed to reproduce.
- My scratch directory
  `/private/tmp/claude-501/-Users-robertkleffner-Documents-GitHub-tarn-first-draft/fidelity-4/scratch/walk-reader-b/`
  was empty when I started (no prior attempt's files were there). I wrote
  `arithmetic.txt`, `crc_check.py`, `crc_check2.py`, `crc_check3.py` there.

---

## 1. The open path — every byte fetched from a cold start, in order

Governing text: §19.1 (`[R-RDR-01]`), §6.4 (`[R-CNT-09]`, `[R-CNT-10]`),
§6.2 (`[R-CNT-06]`), §6.1 (`[R-CNT-04]`).

For a **remote** reader whose transport supports ranged requests and
discloses each response's complete length:

1. **Request 1 — suffix range for the final 64 bytes.** Byte range
   `[F-64, F)` is wanted, but F is not yet known with certainty before this
   fetch; the reader issues a suffix range ("last 64 bytes") or, having
   obtained F from a prior probe, an absolute range. Because the transport
   discloses the response's complete length, this single response also
   carries the transport-authoritative F (§6.4: "where the transport
   discloses a range response's complete length, that response also
   carries the transport-authoritative file size F, so §19.1's first two
   steps cost one request between them"). The reader validates, **in this
   fixed order** (`[R-CNT-06]`, restated at §19.1 step 2): trailer magic →
   trailer CRC → version gate (§6.3) → the remaining field gates (flags,
   committed_file_length = F and multiple of 64, dir_offset ≥ 16,
   dir_length ≥ 4, dir_offset + dir_length ≤ F − 64, file_id ≠ 0, reserved
   bytes zero).
   - **What bounds the second range before it is read:** the trailer's
     own `dir_offset` and `dir_length` fields, *after* they have passed
     every gate just listed — in particular `dir_offset ≥ 16`,
     `dir_length ≥ 4`, and `dir_offset + dir_length ≤ F − 64`
     (`[R-CNT-06]`). A reader MUST NOT issue request 2 from an
     unvalidated trailer (`[R-ENC-05]`, `[R-ENC-10]`: "A reader MUST NOT
     allocate, seek, or issue I/O based on any integer obtained from a
     file before the checksum covering it has been verified").
2. **Request 2 — the directory region**, byte range
   `[dir_offset, dir_offset + dir_length)`. The reader verifies the
   region's final 4 bytes (a CRC-32C over the preceding `dir_length − 4`
   bytes) **before any other use of the region** (`[R-CNT-11]`), then
   parses the record sequence (§7.2) and builds the layer-name table
   (§19.1 step 4), checking name well-formedness/length/control-code
   rules and layer-name uniqueness as it goes (`[R-ENC-11]`,
   `[R-ENC-12]`, `[R-ENC-15]`).

Total requests before the trailer and directory are both validated: **2**.
Total bytes fetched: **64 + dir_length** (the trailer's 64 bytes, plus
exactly the directory region; no tile index, no record extent, no tile
payload is touched — "the open... consumes the trailer and directory
only, no extent slot's content, no tile index, no payload", `[R-RDR-01]`).
If the file's front 16 bytes happen to be resident from this fetch pattern
(they are not, under the two ranges above; they would be only if the
reader separately holds them, e.g. a whole-file read or a suffix window
reaching offset 0), a third check — byte-equality of the front signature
block — is also owed before other processing (`[R-CNT-04]`), but it costs
no additional *request* here since it is not fetched by either of the two
ranges above; absent residency, this reader may defer or omit that check
entirely (§6.1, §19.1 step 1).

If the transport does **not** disclose a range response's complete
length, `[R-CNT-10]` governs instead: the reader spends a third request
to probe the size separately, or fails the open outright if it cannot.
The probe's premise in R1 ("reports each response's complete length")
places us in the two-request case above.

A **local** reader (memory-mapped or whole-file) obtains F without any
request at all and typically holds bytes [0, 16) resident, so it performs
the front-block equality check unconditionally before other processing.

## 2. Validation timing by tier (§19.2, `[R-RDR-02]`)

| Tier | What must be fully valid before reliance | Cited rules |
|---|---|---|
| open | front block (if resident), trailer, directory region + record walk, layer-name namespace | `[R-CNT-04]`, `[R-CNT-06]`–`[R-CNT-08]`, `[R-CNT-11]`–`[R-CNT-15]`, `[R-ENC-12]`/`[R-ENC-15]` |
| first access to a layer | full layer-record validation: extent slot, §7.4 constraint set, exact parse, sub-record walk/multiplicity, name rules, u64 domain, every enumerated value set, fill constraints, codec cap, geometry floor/arithmetic, 2⁶³−1 ceilings, index cross-checks — all decidable without I/O | `[R-RDR-03]` and its full citation list |
| use of a tile | index-chain (crc_of_crc_array, segment CRC), entry classification, payload CRC, decode | `[R-IDX-04]`, `[R-IDX-03]`, `[R-CNT-20]`, `[R-COD-08]`/`[R-SER-07]` |
| use of a record's extent | that extent's CRC and the content rules its encoding attaches | `[R-MTA-10]`, §18.2 |

This is the *latest* permitted point, not a mandated point: a reader MAY
detect earlier, never later, and MUST NOT return data whose governing
structure has not yet passed its tier's validation (`[R-RDR-02]`). Failure
always takes the *violated rule's own* outcome/scope, even though
detection is deferred — e.g. an index-chain failure discovered at tile use
is still layer scope (`[R-IDX-04]`), and already-returned values from
before the failure stand (the bar is prospective, §2.4).

## 3. Layer access (§19.3, `[R-RDR-03]`)

First access to a layer (any use of its declarations beyond the name
already parsed at open) requires, with **no additional fetch** (everything
is already resident from the directory fetched at open): extent-slot
validity; the whole §7.4 constraint set (layout/codec/filter/index_encoding/
channel-type value sets, A_slab-with-S=0, fill length vs. element size,
crc_of_crc_array-with-entry_count=0); exact inline-payload parse with
sub-record walk and multiplicity; dimension/channel name rules;
u64 domain and the 2⁶³−1 designated-sum/product ceiling (rank/channel/
dimension/entry fields, N, P, N·P, C·N, P·Q, etc.); per-type fill
constraints; the lz4 decoded-size cap; the geometry floor (d≥1, every
Tᵢ≥1, C≥1); and the index-region arithmetic cross-check
(`extent_length = entry_count×20 + ⌈entry_count/2¹⁶⌉×4` and
`entry_count` = the geometry-derived addressed-tile count). Any failure
takes its own cited rule's scope — overwhelmingly layer scope, since §7.4's
whole constraint set is `[R-CNT-23]`'s.

## 4. The tile-read algorithm, decoded samples (§19.4, `[R-RDR-04]`)

1. **Domain** — clip to [0, Eᵢ) per dimension; out-of-extent is a request
   failure, not a file verdict (`[R-MDL-01]`, `[R-GEO-02]`).
2. **Ordinals** — tile coordinates, in-tile ordinal, spatial ordinal s,
   disk ordinal (s interleaved; c·N+s planar) (`[R-GEO-06]`).
3. **Index chain** — verify crc_of_crc_array over the fetched CRC array
   and the segment CRC over the fetched segment containing the needed
   entry/entries; parallelizable, cacheable (`[R-IDX-04]`).
4. **Entry** — classify per §15.3 (`[R-IDX-03]`); a valid sentinel
   short-circuits to fill with no payload I/O; a malformed entry rejects
   the tile, never silently filling (`[R-CNF-09]`, `[R-TYP-09]`).
5. **Payload** — fetch [offset, offset+length); verify the entry's crc
   over the stored bytes before decoding (`[R-CNT-20]`).
6. **Decode** — codec, then filter inverse; exact decoded-size match
   required (`[R-COD-08]`, `[R-SER-07]`).
7. **Extract** — locate requested values by §14's offset arithmetic;
   never return padding positions (`[R-GEO-04]`).
8. **Return** — bit patterns unaltered (`[R-MDL-02]`, `[R-TYP-04]`), with
   `[R-SER-08]`'s narrow exception for a nonconforming interleaved bool
   byte that a reader chooses to pass through anyway. A request spanning
   several entries bounds each rejected tile's failure to that tile's
   positions; a layer-scope failure (index chain) bars the rest of the
   request and all further service from the layer, prospectively
   (`[R-RDR-04]`).

---

## 5. Seven degradation walks, end to end

### D1 — Unknown top-level record type
A top-level record's `type` is not 0x0001 or 0x0002, and is from the
**reserved** range (0x0003–0x7FFF). At open (record walk, step 4): the
reader reads the record's MU bit. **MU = 1** → reject-file
(`[R-CNT-15]`: "A record at file scope whose type the reader does not
implement is governed by its stored MU bit: MU = 1 is reject-file...").
**MU = 0** → ignore-record; the record is skipped as though absent, and
whether it survives the next commit follows its PE bit (§20.4's table);
the rest of the open proceeds and every layer is servable. Emitting a
reserved-range type at all is itself a (verifier-detected) violation (F36)
whatever its MU bit; a type from the **experimental** range (≥0x8000) with
MU=0 is not a violation at all (§21.6), and with MU=1 is "a conforming
file a reader nevertheless refuses" (§21.6) — the reader still rejects the
file by the same MU rule, but no register row records the bytes as
nonconforming.

### D2 — Unknown/unimplemented codec
See probe R3 and finding readerb-01 below: this is the one degradation
walk the document does not fully close, because every assigned codec
value (1–4) is **core** and mandatory, so "unimplemented assigned codec"
is a state only non-conforming software can be in.
- If the layer's codec field itself is a **reserved or experimental**
  value (5–0x7FFF, or ≥0x8000): at layer access, this is a plain value-set
  violation, reject-layer (`[R-COD-03]`, register row L43), checkable
  without any I/O. The reader MAY still list the layer's name (it was
  already in the open's layer table) and MUST still serve every other
  layer (§2.4's reject-layer meaning).
- If the codec field is a **valid, assigned, core** value (e.g. 3 = zstd)
  that *this particular reader's software* does not implement: the
  software is "not a conforming reader" (`[R-CNF-03]`, `[R-COD-11]`) and
  the document states no further behavioral obligation for it — see
  readerb-01.

### D3 — Unrecognized/unimplemented flag bit
Two distinct mechanisms, by lane (§6.3, `[R-CNT-08]`):
- **Incompat lane (bits 0–15):** this text defines none, so *any* set bit
  there is unimplemented by every reader built from this text → reject-file
  (register row F19), unconditionally, for every bit position, under every
  minor version of major 1 (§10.1 lists only four growth vehicles, and new
  incompat-lane bits are not one of them).
- **Ignore lane (bits 16–31):** any set bit here is ignored outright; the
  file is conforming (§21.6); an updater copies such bits forward unchanged
  and never originates one under this text.

### D4 — Truncated tail
Physical file shorter than the trailer's `committed_file_length` (a
classic truncation): at open step 2, `committed_file_length` fails to
equal the transport-authoritative size → reject-file (register row F17,
`[R-CNT-06]`). Nothing is served; per §9.5/`[R-LIF-05]` the reader MUST NOT
scan backward on the default path looking for an earlier valid trailer —
that is a deliberate, separate recovery operation (§9.6), never an
implicit part of opening for read.

### D5 — Checksum mismatch
Walked at the directory: the final 4 bytes of the directory region do not
equal the CRC-32C of the preceding `dir_length − 4` bytes. Detected at
open, **before any other use of the region** (`[R-CNT-11]`) → reject-file
(register row F20). Nothing in the file is usable; no layer table is even
built. (Contrast a *tile*-scope checksum mismatch, T1: only that one tile's
read fails; all other tiles of the same layer, and all other layers, are
unaffected.)

### D6 — Limit exceeded
A user-metadata document's decoded size, or its zstd frame's declared
`Window_Size`, exceeds the *reader's own* bound (itself no smaller than
§21.9's 16 MiB / 8 MiB guarantees). Outcome: ignore-record **on resource
grounds**, reported as a resource limit and never as corruption
(`[R-MTA-09]`, `[R-ERR-04]`); the file remains conforming, and the reader
MAY instead decline any containing scope up to the whole file. This is the
clearest instance of §21.9's "minimum guarantee, not a cap" design: a
reader that refuses a within-guarantee file on this ground is itself not
conforming (`[R-CNF-03]`).

### D7 — Format major the reader does not implement
`version_major` is validated second among the three fixed-position gates
at open (magic, trailer CRC, version gate — in that order, `[R-CNT-06]`).
`version_major = 0` is outright invalid and triggers reject-file
regardless of any reader's capability (register row F18, `[R-CNT-07]`).
Any other value the reader does not implement is a **capability refusal**,
not a finding about the bytes: the reader rejects the file
(`[R-CNT-07]`), with a diagnostic the spec SHOULDs be distinct from both
"not a TARN file" and "corrupt," but the file can be perfectly conforming
under that major (§21.6, `[R-CNF-13]`). Only the four reach-conditions that
`[R-CNT-24]` fixes across every major (both of F1's instances, F6, F8,
F14) are checked at all against such a file; every other row's check does
not apply to it.

---

## 6. Worked examples, with real offsets

### 6a. The 128-byte minimal file (Appendix A)

```
0000  89 54 41 52 4E 0D 0A 1A  00 00 00 00 00 00 00 00
0010  00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00
0020  00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00
0030  00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00
0040  8A 4E 52 41 54 0D 0A 1A  01 00 00 00 00 00 00 00
0050  10 00 00 00 00 00 00 00  04 00 00 00 00 00 00 00
0060  80 00 00 00 00 00 00 00  EF CD AB 89 67 45 23 01
0070  00 00 00 00 00 00 00 00  00 00 00 00 7E 15 2F 40
```

- `[0,16)` front signature + 8 zero bytes.
- `[16,20)` directory region: 0 record bytes + CRC-32C(empty) =
  `00 00 00 00`. **Checked**: CRC-32C of zero bytes is `0x00000000`
  per the check vector — confirmed independently (scratch `crc_check.py`).
- `[20,64)` 44-byte pre-trailer pad, slack, zeroed by advice.
- `[64,72)` trailer magic.
- `[72,74)` version_major = 1 (`01 00`).
- `[74,76)` version_minor = 0.
- `[76,80)` flags = 0.
- `[80,88)` dir_offset = 16 (`10 00 00 00 00 00 00 00`).
- `[88,96)` dir_length = 4.
- `[96,104)` committed_file_length = 128 = F (`80 00 ...` = 0x80 = 128).
- `[104,112)` file_id = `EF CD AB 89 67 45 23 01` LE = 0x0123456789ABCDEF.
- `[112,124)` reserved, 12 zero bytes.
- `[124,128)` trailer CRC = `7E 15 2F 40` LE = **0x402F157E**.

**Checked independently**: I recomputed CRC-32C over trailer bytes
`[0,60)` (i.e. file bytes `[64,124)`) in Python (stdlib-only, no file
access, `python3 -I`) and got `0x402F157E` — an exact match (scratch
`crc_check.py`).

Remote open of this exact file, per §1 above: request 1 = suffix 64 bytes
`[64,128)`, which (since F=128) **also contains** `[16,20)` — so by the
containment test of `[R-CNT-09]` a 64-byte suffix already holding the
directory can save request 2 entirely for this particular tiny file, as
the document itself notes ("A shorter window can still spare the second
request: 112 bytes covering [16, 128) contains the directory"). A reader
not speculating gets 2 requests: `[64,128)` then `[16,20)`, 68 bytes
total.

### 6b. The §7.4 rank-1 `sst` layer record

Dimension `x` (extent 100, tile extent 32), one interleaved float32
channel `temp`, codec/filter = none, no alignment/slab, 81-byte inline
payload exactly as the document lays out byte-by-byte. Grid count
G = ⌈100/32⌉ = 4, so entry_count = 4; with no tile stored, the whole
20×4 = 80-byte entry array is four copies of the sentinel
`FF×16 00×4`.

**Checked independently** (scratch `crc_check2.py`): CRC-32C over those 80
sentinel bytes is `0x80A34955` (document's stated value), and
CRC-32C over that 4-byte array (`55 49 A3 80` as stored) is
`0xC4EE982E` (document's `crc_of_crc_array`) — both match exactly.

**Checked independently** (scratch `crc_check3.py`): the full
all-sentinel-segment constant the document states for `[R-IDX-05]`,
`0xEECB3BB2`, computed over 65,536 (2¹⁶) sentinel entries
(1,310,720 bytes), reproduces exactly.

### 6c. R7's tile-read arithmetic (own construction, see §7 R7 below)

Interleaved layer, dimensions declared `y` (E=12, T=5) then `x` (E=9,
T=4); channels `a` (uint16) then `b` (uint8). Sample (y=6, x=5):

- Grid: Gy = ⌈12/5⌉ = 3, Gx = ⌈9/4⌉ = 3.
- Tile coords: t_y = 6 div 5 = 1, u_y = 6 mod 5 = 1;
  t_x = 5 div 4 = 1, u_x = 5 mod 4 = 1.
- Spatial ordinal s = t_y·Gx + t_x·1 = 1·3 + 1 = **4**. Interleaved, so
  disk ordinal = s = **4**.
- In-tile ordinal u = u_y·Tx + u_x·1 = 1·4 + 1 = **5**.
- Sample stride Q = size(a) + size(b) = 2 + 1 = 3. Channel `b`'s
  in-sample offset F_b = size(a) = 2.
- Byte offset of `b`'s value at ordinal u: u·Q + F_b = 5·3 + 2 = **17**.
- Sanity bound: decoded tile size = P·Q where P = Ty·Tx = 5·4 = 20, so
  60 bytes total; offset 17 (1 byte, uint8) fits well inside [0,60).

---

## 7. Probe answers

### R1
Two requests before trailer and directory are both validated (given a
transport that reports each range response's complete length, per
`[R-CNT-09]`):
1. Suffix range for the final 64 bytes, `[F-64, F)` (here, since the file
   is exactly 4,096 bytes, `[4032, 4096)`). This response's complete
   length also supplies the transport-authoritative F, so steps "end of
   file" and "trailer" cost this one request (§6.4, §19.1 step 1).
2. `[dir_offset, dir_offset + dir_length)`, read from the now-validated
   trailer.
Total bytes fetched: 64 + dir_length.
**Which field bounds the second range before it is read:** `dir_offset`
and `dir_length`, taken from the trailer **only after** that trailer has
passed the fixed-order gates of `[R-CNT-06]` (magic → CRC → version →
the remaining field gates, including `dir_offset ≥ 16`, `dir_length ≥ 4`,
and `dir_offset + dir_length ≤ F − 64`); `[R-ENC-05]`/`[R-ENC-10]`
forbid issuing request 2 from an unverified value. Citations: §6.4
(`[R-CNT-09]`, `[R-CNT-10]`), §19.1 steps 1–3 (`[R-RDR-01]`), §6.2
(`[R-CNT-06]`), §4.2 (`[R-ENC-05]`). No disagreement found among these —
they describe the same two-step path from complementary angles (byte
accounting in §6.4, ordering obligation in §6.2/§19.1).

### R2
Outcome class: **reject-file** (register row F19, `[R-CNT-08]`: "a reader
MUST reject-file on any set bit it does not implement in the incompat
lane (bits 0–15)... This specification's text defines no flag bits, so a
writer creating a file under this text MUST write flags = 0"). Bit 2
(0x00000004) is in the incompat lane (bits 0–15), and this text implements
none of them, so every reader built from this text treats it as
unimplemented. **The file is not conforming**: §10.1 lists exactly four
format-growth vehicles and new incompat-lane bits are not one of them
(only new ignore-lane bits are, vehicle 3), so no minor version of major 1
ever assigns bit 2 a meaning; a writer setting it violates
`[R-CNT-08]`/`[R-CNF-05]` outright. I checked §6.3, §10.1, and §21.6 for
any passage that might make an incompat-lane bit a defined, conforming
extension point (the way an ignore-lane bit is) and found none; no
disagreement among the passages that bear on this act.

### R3
Outcome class for the layer: depends on which case obtains, and the
document does not fully determine the reader's behavior in one of them —
see finding readerb-01.
- If codec 3 is validly declared (it is: 3 is an assigned, core value,
  §10.2's table) and the **reader implements zstd**: no violation at
  all; the layer decodes normally.
- If the reader does **not** implement zstd (the probe's premise): per
  `[R-CNF-03]` ("A reader MUST... handle every codec and filter that §17
  designates as core... There are no subset profiles: software that
  declines any of those is not a conforming reader, even if it reads all
  other conforming files correctly") and `[R-COD-11]` ("software unable to
  execute an assigned codec or filter is not a conforming reader"), such
  software is **categorically not a conforming reader**. The document
  assigns no register row and no outcome class to what *this* software
  then does with the layer — reject-layer, reject-file, and silent
  misbehavior are all equally undiscussed for this case (`[R-COD-11]`
  only fixes the *conforming*-reader case, where it "arises only at a
  reserved or experimental value," and there the outcome is reject-layer
  under `[R-COD-03]`/`[R-COD-09]`, not this one).
- Whether such software "may still serve other layers" and "may still
  list this layer's declarations": not stated for this software by this
  document at all (see readerb-01); if it instead encountered the
  layer-scope mechanism that *does* exist for an invalid codec value
  (`[R-COD-03]`, register row L43), the answer there is clearly yes to
  both (§2.4's definition of reject-layer: "A reader MAY still list the
  file's layers, including the rejected one's name," and "all other
  layers are unaffected" — the layer table was already built at open from
  resident, already-CRC-verified directory bytes, so listing names costs
  nothing further).

### R4
Outcome class: **reject-tile**, structural ground (register row **T7**,
`[R-IDX-03]`: "A tile-index entry sets exactly one of offset and length
to the sentinel value" — the row explicitly enumerates both directions,
"offset; length"). Scope: **tile** — only this one tile's read fails;
neighboring tiles of the same layer and all other layers are unaffected
(§2.4). Being a *structural* classification (one of the six §15.3 rows
`[R-IDX-03]` marks *structural*), the entry "contributes no stored extent"
to a verifier's coverage walk or to slab run-continuity checks — the
bytes it nominally addressed fall to slack if no other claimant claims
them (§9.7, `[R-SLB-03]`). I checked §15.3's full table (the sentinel row,
this row, the length=0 row, the offset<16 row, the domain-overflow rows,
the sum-overflow row, the crc-only-failure row, and the three verifier
rows) for any other condition matching "exactly one field at the
sentinel": only this row matches; no disagreement.

### R5
Outcome class: **reject-file** (register row F20, `[R-CNT-11]`: "A reader
MUST verify that CRC before any other use of the region (mismatch:
reject-file), then parse records"). What the reader may still serve: **
nothing**. Reject-file means "the file is not usable; failure is reported
for the whole file. A reader MUST NOT rely on any structure in it" (§2.4).
Because the directory CRC gate precedes the record walk entirely, the
reader has not yet built a layer table, so there is not even a layer name
to report — contrast this with a *tile's* checksum mismatch (T1), where
every other tile and layer remains fully servable, or with a record whose
flags are merely malformed after the directory itself is intact.

### R6
A reader concludes the file is invalid — **reject-file**, register row
**F5** — from **F (the physical/transport-reported file size) alone**,
needing no other byte: "File size is below the 128-byte minimum... decided
from F alone and needing no other byte of the file" (row F5's own
Instances cell), governed by `[R-CNT-27]`: "No conforming file is shorter
than 128 bytes... A reader MUST treat a shorter file as a validity error
at file scope." 96 < 128, so this is immediate at open step 1 ("end of
file"), before any attempt to fetch or validate a trailer. (Separately,
96 is also not a multiple of 64, which `[R-CNT-06]` would otherwise also
condemn once a trailer were read — but the document is explicit that F6's
determination needs none of that: the 128-byte floor alone decides it.)

### R7
Disk ordinal of the tile holding (y=6, x=5): **4**. Byte offset within
the decoded tile image at which channel `b`'s value begins: **17**. Full
arithmetic in §6c above, built from `[R-GEO-06]` (ordinals),
`[R-SER-01]`/`[R-SER-02]` (value sequence and byte-offset formula). I
found no second passage stating a different ordinal formula to compare
against; §11.4's own worked example (grid (4,8), tile (1,2) → s=10) uses
the identical `t_i · ∏_{j>i} G_j` form I applied, which I used to sanity
check my own instantiation before trusting it for a different grid shape.

### R8
Top-level record, unimplemented type, MU=1: **reject-file**
(`[R-CNT-15]`: "A record at file scope whose type the reader does not
implement is governed by its stored MU bit: MU = 1 is reject-file..."). A
**sub-record** of the same (unimplemented) type inside a layer record,
MU=1: **reject-layer**, confined to that one layer, and the document is
explicit that this differs from the top-level case and that the rest of
the file is unaffected: `[R-CNT-18]`: "An unknown sub-record type with
MU = 1 is reject-layer, and where the file is otherwise conforming a
reader MUST NOT reject the file for it." §20.4's table restates the same
split for updaters ("At layer scope an unknown critical record blocks
modification of that layer, its drop included, leaving other layers
editable... At file scope no commit is available at all"). Both passages
agree; the scope difference (file vs. layer) is the entire point of the
rule and is stated the same way in both places I found it.

---

## 8. Findings

See structured findings `readerb-01` (AMBIGUITY) in the tool result. No
second finding survived scrutiny at a confidence I would stand behind for
this round; I looked for, and rejected, three further suspicions, recorded
in the structured result's `rejected_candidates` field.
