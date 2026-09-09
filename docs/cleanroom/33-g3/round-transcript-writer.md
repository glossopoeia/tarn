# Cleanroom round 33 — Writer implementer transcript

Lane: conforming **writer and updater**, implemented on paper against
`spec/tarn.md` alone.

## 0. Disclosure and method

I opened exactly one file: `/Users/robertkleffner/Documents/GitHub/tarn-first-draft/spec/tarn.md`
(4,805 lines, 47,853 words by `wc`). I did not open `docs/`, `PLAN.md`,
`AGENTS.md`, `README.md`, `conformance/`, `spec/registry.json`, or any git
object. I ran no `git log`/`git diff`, no web access, and I did not list the
output directory.

The spec file is where the brief said it would be. No path surprise.

Context I did not ask for **did** appear before I began: a project instruction
file (`CLAUDE.md` pointing at `AGENTS.md`), an index of the maintainer's
auto-memory with a dozen titled entries about this project's harness and about
where its repair defects live, a git status snapshot with recent commit
subjects naming ADR-0124 and a defect count, and an MCP server instruction
block. I read none of the memory entries and opened none of the files they
name. I am naming that this material appeared, per the brief, without
repeating its contents; the commit subjects in particular carry the shape of
the previous round's result and I have deliberately not let them steer where I
looked. Everything below is derived from `spec/tarn.md` and from arithmetic I
ran myself.

Files I wrote, all in my own scratch directory
`/private/tmp/claude-501/-Users-robertkleffner-Documents-GitHub-tarn-first-draft/r33-round/scratch/writer/`:

- `wr_crc.py` — a CRC-32C implementation from §4.5's parameters, plus the
  document's own check vectors.
- `wr_minfile.py` — rebuilds Appendix A's 128-byte file from §6.1/§6.2 alone.
- `wr_build.py` — builds a non-trivial file end to end; emits `gen1.tarn`.
- `wr_append.py` — walks one append commit against `gen1.tarn`.
- `gen1.tarn` — the 768-byte artifact of the creation walk.

I also ran `grep`/`sed`/`tr` sweeps against the spec file (listed in §7 below).
Because the document is hard-wrapped and blockquotes insert `> `, every phrase
sweep I relied on a *zero* from was re-run in a whitespace-normalised form
(`tr '\n' ' ' | sed 's/  */ /g'`), and every sweep was accompanied by a control
search for a phrase I knew was present in the same passage.

---

## 1. Instrument check: the document's own constants

Before trusting any of my own arithmetic I reproduced every checksum constant
the document states. All five matched on the first run:

| Quantity | I computed | Document states | §|
|---|---|---|---|
| CRC-32C(`"123456789"`) | `0xE3069283` | `0xE3069283` | §4.5 |
| CRC-32C(zero bytes) | `0x00000000` | `0x00000000` | §4.5 |
| CRC-32C of 4 sentinel entries (80 bytes) | `0x80A34955` | `0x80A34955` | §7.4 example |
| crc_of_crc_array over that 4-byte array | `0xC4EE982E` | `0xC4EE982E` | §7.4 example |
| CRC-32C of a full 2¹⁶-sentinel segment | `0xEECB3BB2` | `0xEECB3BB2` | §15.4, App. B |

`wr_minfile.py` then rebuilt Appendix A's minimal file from §6.1 and §6.2's
layout tables without consulting the appendix's hex dump, and produced the
appendix's 128 bytes **byte for byte**, trailer CRC `0x402F157E` included. That
is a real confirmation that §6.2's table, §7.1's directory rule and §4.5's
checksum are jointly sufficient to emit a file: a writer that reads only Part I
gets the same bytes the annotated example shows.

I also re-derived §5.1's and §9.2's floor arguments:

- `[R-CNT-27]`: 16 (front block) + 4 (minimum directory) = 20; least
  64-aligned offset ≥ 20 is 64; + 64 (trailer) = **128**. Matches.
- §9.2's second Note: prior F + 68 rounded up to the next multiple of 64 is
  prior F + **128** (since prior F + 64 < prior F + 68). Matches.
- §5.1's example pad: 64 − 20 = **44** bytes of slack. Matches.

---

## 2. Creation: a byte-layout walk

### 2.1 The file I built

One layer plus one file-scope user-metadata record, deliberately exercising a
sentinel in the middle of an index, edge padding in a stored tile, and a
record extent.

- Layer `sst`, rank 1, dimension `x`, E = 100, T = 32 → G = ⌈100/32⌉ = 4,
  N = 4, P = 32.
- Interleaved (`layout` = 1), one channel `temp`, type 12 (float32),
  fill `00 00 C0 7F` (the quiet NaN `0x7FC00000`).
- `linearization` = 1, `codec` = 1 (none), `filter` = 1 (none), A = 0, S = 0,
  A_slab = 0, `index_encoding` = 1.
- Decoded size per tile = P·Q = 32 · 4 = **128 bytes** (`[R-SER-02]`, the
  interleaved row).
- Tiles 0, 1 and 3 stored; tile 2 the sentinel.

Tile 3 covers x ∈ [96, 128); x = 96…99 are real and x = 100…127 are **padding
positions**, each of which I encoded as the channel's fill (`[R-SER-05]`).
That is 28 × 4 = 112 bytes of fill inside a 128-byte tile — the rule bites
hard on a writer and I want it on record that I applied it.

### 2.2 Offsets, and who fixed each one

| Region | Offset | Length | Fixed by the document, or mine? |
|---|---|---|---|
| front signature block | 0 | 16 | **fixed** — §6.1, `[R-CNT-04]` |
| tile 0 payload | 16 | 128 | **mine** — `[R-SLB-05]`; only the floor of 16 is fixed (`[R-IDX-03]`, `[R-CNT-13]`) |
| tile 1 payload | 144 | 128 | **mine** |
| tile 3 payload | 272 | 128 | **mine** |
| tile-index region | 400 | 84 | length **fixed** by `[R-CNT-17]`: 4·20 + ⌈4/2¹⁶⌉·4 = 84; offset mine |
| user-metadata extent | 484 | 24 | length = 20-byte document + 4-byte terminal CRC (§8.1, `[R-CNT-25]`'s ≥ 5 floor); offset mine |
| directory | 508 | 134 | length **fixed** by the record sequence (105 + 25) + 4; offset mine, but §6.2/`[R-CNT-05]` force it to be the last structure |
| pre-trailer pad | 642 | 62 | **fixed** — `[R-LIF-02]` step 5 pads to the next 64-byte boundary |
| trailer | 704 | 64 | **fixed** — §6.2 |

F = **768**, F mod 64 = 0, dir_offset + dir_length = 642 ≤ F − 64 = 704. ✓

Derived values I computed and that no example in the document gives me:
tile CRCs `0xF8118D31`, `0xFDF96FE9`, `0xE1909AA1A`→`0x1909AA1A`; segment CRC
`0x1EE4CDE6`; crc_of_crc_array `0x647EE2B6`; user-metadata extent CRC
`0xA780E8C5`; directory CRC `0xE81B9AD6`; trailer CRC `0x5F309F06`.

**The layer record's inline payload came out at 81 bytes**, which is exactly
the length §7.4's worked example states for the same declarations — an
independent confirmation that I packed the fields in table order with no
padding (`[R-CNT-18]`) and got the field widths right. My payload differs from
the example only in `crc_of_crc_array` (mine reflects three stored tiles).

### 2.3 Ordering and durability, as the document fixes them

`[R-LIF-02]`, creation path (§9.2's third paragraph), with §20.2 restating it:

1. front signature block at 0 — its durability is covered by the barriers of
   steps 4 and 6, stated expressly.
2. payloads, index regions and record extents, **in any order** satisfying
   §5.2's coverage classes and every declared layout invariant. This is the one
   place a creator has real latitude; `[R-SLB-05]` names it.
3. the complete directory, then its CRC.
4. **barrier.**
5. pad to the next 64-byte boundary, then the trailer with a fresh nonzero
   `file_id`.
6. **barrier.**

The commit point is step 6. §20.2 is emphatic that *both* barriers are owed
("`[R-LIF-02]` steps 4–6 — both barriers, not one"), and §9.2's second
paragraph classifies both as conduct rules with no byte trace, so a
barrier-less writer emits a conforming file and violates its own obligation as
an actor. I could implement this without guessing.

Coverage check on my file (`[R-CNT-02]`): the eight claimants partition
[0, 768) with a single 62-byte hole, the pre-trailer pad. Slack total = **62**,
which is what a verifier must report (`[R-CNT-21]`).

### 2.4 What creation did *not* leave open

Things I expected to have to guess and did not have to:

- Whether the front block's second 8 bytes are writer-chosen. They are zero
  (§6.1 table), and F6 registers the reserved half separately from the magic.
- Whether the pad is 0 or 64 bytes when the directory ends on a boundary.
  §6.2 says "a writer that ends its directory on a 64-byte boundary leaves
  none".
- Whether a partial segment may use `[R-IDX-05]`'s constant. It may not:
  "a partial segment's CRC MUST be computed". My 4-entry segment is partial,
  so I computed `0x1EE4CDE6`.
- Whether the layer record's flags come from §7.3's registry or from me.
  `[R-CNT-22]`: from the registry, MU = 1 / PE = 1 → `flags` = 3 for the layer
  record and MU = 0 / PE = 1 → `flags` = 2 for the user-metadata record.

---

## 3. The append procedure

### 3.1 One concrete commit

Against `gen1.tarn` (F = 768) I committed: supersede tile 1's payload, and
grow E from 100 to 130.

The growth changes the grid count (⌈100/32⌉ = 4 → ⌈130/32⌉ = 5), so under
§20.3 step 4 and `[R-CNT-17]` the index content changes, `entry_count`
goes 4 → 5, `extent_length` 84 → 104, and the layer's **whole** tile-index
region is re-emitted at a new placement.

| Region | Offset | Length |
|---|---|---|
| new tile 1 payload | 768 | 128 |
| new index region | 896 | 104 |
| new directory | 1000 | 134 |
| pad | 1134 | 18 |
| trailer₂ | 1152 | 64 |

F₂ = **1216**; F₂ − F₁ = 448 ≥ 128 as `[R-LIF-02]` requires; F₂ mod 64 = 0.
New segment CRC `0x4C03A782`, new crc_of_crc_array `0x83EC33B2`.

Slack after the commit, computed from the live claimants: runs
[144, 272) = 128 (the superseded payload), [400, 484) = 84 (the superseded
index region), [508, 768) = 260 (dir₁ + pad₁ + trailer₁), [1134, 1152) = 18
(the new pad). **Total 490 bytes** — nearly two thirds of the original file,
for a one-tile edit. §20.3's Note and its 20 MB example say exactly this, so
the accounting is the document's own.

The user-metadata record was re-emitted **byte-identically**, extent slot and
all, still pointing at [484, 508) — `[R-WRT-05]`, and §20.3's shape (a) figure.

### 3.2 The growth's effect on already-stored bytes — checked, not assumed

This is where I wanted to catch the document out and could not. Tile 3's
positions x = 100…127 were padding in generation 1 and are **real sample
positions** in generation 2. Their stored bytes are unchanged. Under
`[R-SER-05]` they held the channel's fill, so after the growth they read back
as fill — a legal sample value (`[R-TYP-05]`). §20.3's justification sentence
says precisely this ("a grown extent adds positions that held their channel's
fill (§14.5), and fill is a legal sample value"), and I confirmed it by
construction. The other two cases — a position falling in a previously
unaddressed tile, and one in an addressed-but-sentinel tile — both read fill
too. There is no fourth case: a coordinate ≥ E_old is either padding inside an
addressed tile or in a tile the old grid did not address.

For a packed planar bool plane the same growth argument holds and **pad bits
are untouched**, since pad bits are keyed to P = ∏Tᵢ and tile extents are on
the fixed side. §14.3's Note draws that distinction and it survives the pair.

### 3.3 Every record-flag combination, and what my updater may do

`[R-CNT-12]` defines two flag bits (MU = bit 0, PE = bit 1) and reserves bits
2–15. §20.4 routes them. The authoritative source of the flags is *not* the
stored bits in every case, which is the trap; §20.4's opening paragraph is
explicit.

| Case | Governing flags | What my updater may do |
|---|---|---|
| type 0x0001 (layer), stored flags 3 | registry: MU 1, PE 1 | Re-emit byte-identically if untouched; may modify per §20.3 step 4. Never droppable. |
| type 0x0001, stored flags ≠ 3 (e.g. 1) | registry still governs | Same. The file is nonconforming (L49, verifier) but no reader behaviour changes. If I *modify* the record it is "new output under its writer obligations", so `[R-CNT-22]` obliges me to write flags = 3; if I merely carry it, §20.3 step 2's "reproducing a structure's bytes unchanged is not authoring them" obliges byte-identity. Both directions stated. |
| type 0x0002 (user metadata), any stored flags | registry: MU 0, PE 1 | Retain byte-identical, extent content unmodified. Never droppable at either scope (§20.4's closing paragraph). Editing the document = new extent appended, old one slack. |
| unregistered type I implement | the definition I implement it from | Never the stored bits (`[R-CNT-22]`, §10.3). PE decides droppability. |
| unknown top-level type, MU 1, PE 1 | stored | **No commit at all.** I am a reader first; `[R-CNT-15]` makes it reject-file. |
| unknown top-level type, MU 1, PE 0 | stored, read as PE 1 | Same — `[R-CNT-12]` forbids the combination and forces the PE = 1 reading. |
| unknown top-level type, MU 0, PE 1 | stored | Retain byte-identical, extent unmodified. A compactor may relocate the extent and re-point the slot (`[R-WRT-08]`, `[R-WRT-07]`). |
| unknown top-level type, MU 0, PE 0 | stored | Retain byte-identical **or drop**, its extent becoming slack — in any commit I am otherwise free to make, one whose only effect is the drop included. SHOULD report the loss. |
| unknown **sub-record** type, MU 1 | stored | Reject-layer: that layer is not modifiable, other layers stay editable. The file is not rejected (`[R-CNT-18]`). |
| unknown sub-record, MU 0, PE 1 / PE 0 | stored | As the two top-level MU 0 rows. |
| reserved-range type (0x0003–0x7FFF), MU 1 | stored | reject-file at open (F35). No commit. |
| reserved-range type, MU 0 | stored | Ignore-record for reading; carried forward or dropped by PE. The file is nonconforming (F36) but its detector is the verifier, so I need not notice, and `[R-WRT-01]` lets the violation travel. |
| reserved flag bit 2–15 set | — | Readers MUST ignore; verifier-detected (F26/L47). Carried forward. |

That is the complete lattice and the document decides every cell. The one
place it made me stop and re-read three times was the MU = 1 row's reach:
§20.4 says the row "reaches only a type the updater does not implement",
which is only sound because `[R-CNF-03]` obliges a conforming reader — and an
updater is a reader (§2.3) — to implement **both** registered types. That
chain is spelled out.

### 3.4 Write order, durability, commit point (append)

`[R-WRT-04]`'s six steps, with `[R-WRT-03]` fixing verification depth:

1. Establish F by validating the trailer at the **physical** end (§6.2's
   ordered gates). Failure ⇒ torn ⇒ no append; recovery is a separate,
   deliberate operation (§9.6).
2. Perform §19.1's open. Note the order: F first, then the open. That matters,
   because §6.2's gates alone do not check the directory CRC, so a payload
   byte-string that mimics a trailer at exact end of file passes step 1 and is
   caught by step 2's `[R-CNT-11]`. §6.2's Note says so explicitly. My updater
   therefore never appends to a mimic.
3. Validate what the commit touches: trailer and **full** directory always
   (re-emission relies on every directory byte), §19.3's layer validation for
   every layer whose record, index or extents I modify, and the §19.4 index
   chain for every segment whose entries I reuse.
4. Write payloads and indexes, beginning at exactly F.
5. Re-emit the complete directory + CRC.
6. **barrier**, pad, trailer (same `file_id`, ignore-lane bits copied forward
   and no other set, `version_minor` per `[R-CNT-26]`), **barrier**.

Durability order: everything in steps 4–5 is durable before the trailer is
written; the trailer is durable last. Commit point = the completion of step
6's barrier.

---

## 4. Slack, per commit shape

| Shape | Bytes that become slack | Counted by | Permitted content |
|---|---|---|---|
| **Append (new layer)** | the superseded directory, its pad, and its trailer. Nothing else — §20.3 shape (a). Sized by *layer count*, never by data. | verifier, on a completed walk (`[R-CNT-21]`, §9.7) | unconstrained; writers SHOULD zero only the gaps they create (`[R-CNT-03]`) — a superseded structure is a committed byte the writer MUST NOT touch (`[R-LIF-01]`), so it can never be zeroed |
| **Append (tiles added / superseded)** | the layer's whole prior index region, every superseded payload, plus dir/pad/trailer — shape (b). My worked commit: 128 + 84 + 260 + 18 = 490. | same | same |
| **Directory-only commit** (rename, clear a slab, drop a PE = 0 record) | dir/pad/trailer, plus any dropped record's extent — shape (c). | same | same |
| **Planar channel shortened from the end** | the removed channels' stored-tile extents, in addition to the index region and dir/pad/trailer. §20.3 says so and §23.1 names it as the deletion-is-not-erasure case. | same | same |
| **Alignment / slab gaps** | the run before an aligned tile or a slab run's first stored tile | same | unconstrained; SHOULD be zeroed |
| **Pre-trailer pad** | dir end → next 64-byte boundary | same | unconstrained; SHOULD be zeroed; a *longer* gap is conforming though no conforming commit produces one (§6.2) |
| **Whole-file rewrite / compaction** | **none carried**: the output holds only structures reachable from the input's live trailer, less any record §20.4 licenses dropping (`[R-WRT-06]`) | verifier on the output | alignment gaps and the new pad only |
| **Abandoned partial write** | *no slack total is owed at all.* There is no valid trailer at the physical end, so §6.2's ordered validation rejects before a live trailer is established, "so the total is not owed at all… which is not a partial total but the absence of one" (`[R-CNT-21]`). | nobody | n/a |

Partial totals: a verifier that stops at the first violation, that has a
scope-level rejection block enumeration, or that declines a **layer** on
resource grounds must report the total as partial and say what stopped it. A
declined **tile** or **document** decode does *not* make the walk partial —
the claimant is enumerated from its index entry or extent slot. Nor does an
entry `[R-IDX-03]` classifies reject-tile on a structural ground: it
contributes no claimant, the walk passes over it, and the bytes it nominally
addressed fall to slack. All four of those distinctions are stated; I did not
have to supply any of them.

---

## 5. Torn-write recovery — five crash points

Let generation *n* be committed at F_n, and let the writer be committing *n+1*.

**(A) Crash inside step 4 (payloads/index written, no directory).** Physical
length > F_n. The final 64 bytes are payload. A reader: F8 (trailer magic
mismatch) at open, reject-file, and `[R-LIF-05]` forbids it to scan backward.
The file is **not conforming** in the meantime — `[R-CNT-01]` requires the
file size to equal the live trailer's F. My updater: §9.4 forbids appending;
recovery (§9.6) probes backward at 64-aligned offsets, finds trailer_n
(magic ✓, CRC ✓, committed_file_length = o + 64 ✓ — a candidate), re-verifies
the whole prefix, and truncates to F_n. Everything trailer_n reaches is still
byte-intact, which is the entire return on `[R-LIF-01]`.

**(B) Crash after step 5 (directory written) but before step 6.** Identical
reader-visible state to (A): no trailer at the physical end. Same recovery.

**(C) Crash during step 6's trailer write.** Two sub-cases and both are
covered. If the physical length is short of F_{n+1}, the last 64 bytes are not
trailer-aligned and the magic fails (F8). If the file was pre-extended so the
physical length is F_{n+1} but the trailer's tail is unwritten, the magic
matches and the **trailer CRC** fails (F14). Either way reject-file, and the
backward probe rejects that offset as a non-candidate ("a match satisfying
both is a candidate, and one failing either is not") and continues to
trailer_n.

**(D) Crash after step 6's barrier.** The commit is complete; the reader sees
generation *n+1*. Conforming.

**(E) Crash on the recovery path itself** — after `[R-LIF-04]`'s
"overwrite from F" but before the truncation that must happen "no later than
step 6". The residue past the new committed length leaves the file torn again;
§9.5's Note says exactly this ("Residue past a completed commit carries no
register row of its own… what the residue violates is `[R-LIF-04]`'s writer
obligation to truncate or overwrite, and the state a reader can observe is
already named"). Recoverable to either F_n or F_{n+1}.

Two things I checked and found decided rather than open:

- A recovery tool MUST report the candidate it settled on and how many
  candidates it rejected on re-verification (`[R-LIF-06]`) — so a mimic that
  fooled the probe is at least visible in the report.
- Rollback is **not** detectable in-format, and an expected committed file
  length is expressly not a substitute, because placement is free and slack is
  unconstrained so a re-append can reach any length ≥ the expected one. That
  is stated, with the one thing that does work (a detached hash or an
  append-only transport) named.

---

## 6. Byte-divergence catalogue

Given identical input arrays and identical stated options, here is every way I
can find for two conforming writers to differ, checked item by item against
Appendix G.

| # | Degree of freedom | Rule that opens it | Closed by Appendix G? |
|---|---|---|---|
| 1 | Placement of every structure (order and position) | `[R-SLB-05]`, `[R-LIF-02]` step 2 | **yes**, item 3 (total emission order, contiguous, first structure at 16) |
| 2 | Extent of gaps between structures | same | **yes**, item 3 |
| 3 | Content of gaps and the pre-trailer pad | `[R-CNT-03]` (a SHOULD) | **yes**, item 3 ("every byte of every such gap is zero — `[R-CNT-03]`'s advice, taken as a requirement here") |
| 4 | `file_id` | §9.3 (advice only) | **yes for a creator**, item 2 (derived from a named hash over [0, F−64) plus the trailer's first 60 bytes with `file_id` zeroed). **Expressly not for a compactor** — item 2 and item 8 say so and pin the compactor instead. |
| 5 | Record order in the directory | `[R-CNT-14]` | **yes**, item 3 (ordered by type; 0x0001 ties by layer name; others by masked header, then payload, then extent contents) |
| 6 | Sub-record order | `[R-CNT-14]` via `[R-CNT-18]` | **yes**, item 3 |
| 7 | Encoder output for codecs 2–4 | `[R-CNF-05]`; RFC 1951/8878 constrain decoders, not encoders | **yes** by pinning, item 1 — and item 1 concedes byte-identity *across* implementations is unattainable |
| 8 | The ≤ 7 unused high bits of a raw DEFLATE stream's final byte | §17.2's Note under `[R-COD-05]`: "This specification constrains them nowhere" | **yes**, item 1 — the Note itself points at item 1 |
| 9 | Which codec value | §17.2 | **yes**, item 1 (naming the implementation names the codec) |
| 10 | Which filter value | §17.3 | **yes**, item 5 |
| 11 | Tile extents | §11.3 ("a writer's choice, and this specification imposes none") | **yes**, item 5 |
| 12 | Channel layout | §14.1 | **yes**, item 5 |
| 13 | Whether A / S / A_slab is declared, and at what value | §16 | **yes**, item 5 |
| 14 | Whether an all-fill tile is stored or sentinelled | no rule requires either | **yes**, item 6 |
| 15 | The fill a writer records when the caller chooses none | `[R-TYP-10]` (a SHOULD) | **yes**, item 7 — and item 7 notes it reaches further than 8 bytes, because item 6 makes tile *existence* depend on it |
| 16 | `version_minor` | `[R-CNT-26]` (a SHOULD) | **yes**, item 8, for creator and compactor, with §20.5's carried-feature case named |
| 17 | Ignore-lane `flags` bits | `[R-CNT-08]` for a creator forces 0; a compactor carries the input's forward | **yes**, item 8 |
| 18 | Number of generations | §9 constrains it nowhere | **yes**, item 4 — and item 4 correctly notes no field refutes it, only §9.6's probe |
| 19 | JSON serialization of user metadata (number formatting, escaping, whitespace) | `[R-MTA-05]` sorts members but explicitly does not make two writers agree | **yes**, item 9 |
| 20 | zstd settings for metadata encoding 2 | §18.2 | **yes**, item 9's clause "and, where that encoding is 2, by a named zstd implementation at a named version with fixed settings" |
| 21 | Unicode normalization of names | `[R-ENC-14]` (a SHOULD) | **yes**, item 10 |
| 22 | Presence of a zstd frame's `Frame_Content_Size` field | `[R-COD-06]`: "MAY be present"; §18.2 likewise for a document | **yes**, transitively — item 1 and item 9 pin the producer, and the field's presence is a function of the pinned encoder's settings and API |
| 23 | Segment CRC of a full all-sentinel segment: computed vs `[R-IDX-05]`'s constant | `[R-IDX-05]` MAY | **not a divergence** — the constant *equals* the computed value, so the bytes are identical either way. I verified `0xEECB3BB2` myself. |
| 24 | Pre-trailer pad length | §6.2 admits a longer gap | **not open to a writer** — "no conforming commit produces one"; `[R-LIF-02]` step 5 fixes it |

**I could not find a degree of freedom Appendix G leaves open**, and I looked
hard at the two places where a total order is easiest to under-specify:

- *Alignment interacting with the emission order.* Item 3's "each later
  structure begins where the previous one ended, save where alignment forces a
  gap — a declared A or A_slab, or §6.2's 64-byte trailer alignment" yields a
  unique placement under a declared per-tile A (each stored tile at the least
  multiple of A ≥ the previous end), under a slab (packed within a run,
  A_slab-aligned at each run's first stored tile), and for an index region
  (unaligned, so packed). I walked all three and they are determinate. The
  clause "or, where a declared alignment admits no structure at 16, at the
  least position above it the declaration admits" handles the one boundary,
  a first layer whose first structure is an aligned stored tile.
- *Ties in item 3's record key.* Item 3's claim that two records its key does
  not separate are interchangeable is **true**: such records agree in type,
  flags, lengths, payload and extent content, and because item 3 also fixes
  extent placement in the same order, swapping the pair swaps both the record
  and its extent and yields identical bytes.

Two claims in Appendix G I tried to falsify and could not:

- Item 5's "The filter is the identity exactly where its permutation is —
  where the stride is 1 … and equally where the decoded image is a single
  group, n = L/s being 1". The permutation j·s + i ↦ i·n + j is the identity
  iff s = 1 or n = 1: with i = 0, j = 1 and s, n > 1 it sends offset s to
  offset 1. **"Exactly" is correct.**
- Item 2's hash input is well founded and non-circular: [0, F − 64) followed by
  the trailer's first 60 bytes with `file_id` zeroed. Every one of those bytes
  — `committed_file_length`, `dir_offset`, `dir_length` included — is fixed
  before `file_id` is chosen, and the trailer CRC at [60, 64) is outside the
  input, so it can be computed afterwards.

I also verified `[R-COD-10]`'s premise that the decoded image's length is
divisible by the shuffle stride in every case: planar numeric P·Bᶜ over
s = Bᶜ; interleaved P·Q over s = Q; packed planar bool ⌈P/8⌉ over s = 1.
All three divide.

---

## 7. The closed list, taken in pairs

§20.3 step 4 is the surface the round points at hardest, so I derived the
members from the structure the list governs (§7.4's declaration fields) rather
than from the list's own prose, put each on one side, and then took them
pairwise.

**Members of the permitted side**, as I derive them:
(1) layer, dimension and channel **names**;
(2) a dimension **extent**, growth only;
(3) a planar layer's channel list **extended at its end**;
(4) a planar layer's channel list **shortened from its end**;
(5) a **slab or alignment declaration** — declared, re-established or cleared.

**Fixed side:** layout, linearization, index encoding, codec, filter, rank,
dimension order, every tile extent, every channel's type and fill, an
interleaved layer's channel list save names, and the position of every planar
channel but the last. Plus the three fields that "follow the commit"
(`entry_count`, `crc_of_crc_array`, the extent slot) and sub-records, which
are §20.4's.

I checked the document's own closure claim — "Between them the two lists reach
every declaration field of §7.4" — field by field against §7.4's table. All
sixteen rows are reached: name (1), layout/linearization/codec/filter (fixed),
A / S / A_slab (5), rank (fixed), C (via "channel list"), the three dimension
sub-fields (name → 1, extent → 2, tile extent → fixed), the three channel
sub-fields (name → 1, type and fill → fixed), index_encoding (fixed),
entry_count and crc_of_crc_array ("follow the commit"), sub-records (§20.4).
**The closure claim holds.**

### 7.1 The pairs

| Pair | Does the text decide it? | Does the principle beside the list still reach it? |
|---|---|---|
| 1 × 2 names + growth | yes — "A commit MAY make several of these changes at once" | yes: a name enters no structural map; a grown extent adds positions that held fill |
| 1 × 3, 1 × 4 names + list change | yes | yes. I built the adversarial case: shorten `[a,b,c]` to `[a,b]` while renaming `b` → `c`. A name-level "replacement" results, but positions are the identity ("the dimension order and the channel order being positional and fixed"), old tiles keep their ordinal, type and fill, and nothing is reinterpreted. |
| 1 × 5 | yes | yes |
| 2 × 3 growth + append channel | yes | **yes, and I checked the justification survives the pair.** The sentence "an appended planar channel adds tiles at ordinals after every existing one, a disk ordinal being c·N + s" is stated with an unqualified N. Under a simultaneous growth N moves from N_old to N_new, yet every existing tile still sits below C_old·N_new, so "after every existing one" remains true; the renumbering is separately covered by "a growth renumbers ordinals wherever `[R-GEO-06]` moves them". |
| 2 × 4 growth + shorten | yes | yes — and the text anticipates the exact arithmetic coincidence, saying the region is re-emitted "whether or not entry_count changes with it", which is the C↓ · N↑ case (e.g. C 4→2 with N 3→6 holds entry_count at 12). That is a careful sentence and it is right. |
| 2 × 5 growth + slab/alignment | yes | yes. A growth that changes a grid count changes the run partition, which is one of `[R-SLB-04]`'s five triggers, so re-establishment or clearing is owed. A growth that changes no grid count triggers none of the five and disturbs nothing. |
| 3 × 5, 4 × 5 | yes | yes — channel blocks are `[c·N, (c+1)·N)`, so adding or removing a block adds or removes whole runs and `[R-SLB-04]` fires on "the run partition". |
| **3 × 4** extend + shorten | **excepted expressly** | the exception is the round-32 repair and it reads soundly |
| triples (2 × 3 × 5 etc.) | yes — "several of these changes at once" is general | yes |

The one composition the text forbids is 3 × 4, and I could not find a second
pair that composes into anything the fixed side forbids. Renaming plus a list
change gets closest, and it is defused by the positional-identity clause.

### 7.2 Where the list does break down

The failure is not in a *pair*. It is inside member (5), and it is a
quantifier question about three ordinary English verbs. See finding
**writer-01** below.

---

## 8. Findings

### writer-01 — AMBIGUITY

**§20.3 step 4 (`[R-WRT-04]`).** The closed list's alignment/slab member does
not say whether a commit may change an already-declared A, S or A_slab to a
*different* nonzero value.

Quotation (§20.3, normative; the passage is not labelled Note, Example or
Rationale):

> A layer that stores a tile **in the generation this commit
> supersedes** keeps its declarations, with these exceptions and no
> other: its name, and its dimension and channel names, MAY change;
> an extent MAY grow, and MUST NOT shrink; a planar layer's channel
> list MAY be extended at its end or shortened from its end, but not
> both in one commit; and a slab or alignment declaration MAY be
> declared, re-established or cleared as this step provides below.

and, three sentences later, the same step's statement of what is excluded:

> What the line gives up is stated rather than carved around: a
> shrink, a fill change, a re-type, a re-tiling, a change to the
> dimension order, a change of rank, layout, linearization, index
> encoding, codec or filter, any change to an interleaved layer's
> channel list but a channel's name, a planar channel inserted or
> removed anywhere but the end of the list, and a planar channel list
> both extended and shortened in one commit are rewrites even where a
> particular file would survive them in place, because deciding which
> files would is the edge this list exists to remove.

**The two permitted readings.**

*(R-a) "declared" is any act of writing a nonzero declaration.* A commit that
sets A from 4096 to 512 declares an alignment of 512; the prior generation's
value is irrelevant to whether this commit declares one. The change is
permitted, subject to the step's below-clause ("an aligned layer's stored
tiles — every one the new state keeps, not only those this commit adds —
satisfy its invariant or the declaration is cleared").

*(R-b) The three verbs partition the transitions.* "declared" = none → some,
"re-established" = some → the same some (with its invariants re-satisfied,
which is what `[R-SLB-04]` obliges), "cleared" = some → none. A change of
value is none of the three, so the closing "and no other" of the permitted
list forbids it, and it is a new layer or a whole-file rewrite.

**Why neither reading can be dismissed.**

For (R-a): `[R-SLB-04]` lists "or the slab declaration itself" among the five
things whose change obliges re-establishment, which presupposes that a slab
declaration can change under a commit. And under (R-b) the restriction
forbids nothing substantive, because a writer reaches the same end state in
two commits — clear A in commit *n*, declare A = 512 in commit *n+1* — with
every intermediate file conforming. A rule that a second commit trivially
routes around is unlikely to be the one intended, and §20.3 says its own
purpose is "the edge this list exists to remove", not the creation of one.

For (R-b): the step's own below-clause, which is the text "as this step
provides below" points at, offers only **two** dispositions for a slab —
"a slab declaration is re-established or cleared (`[R-SLB-04]`)" — dropping
"declared" entirely; if "declared" already covered writing any value,
"re-established" would be redundant, and drafting this careful does not
usually carry a redundant verb in a closed list. §20.3's shape-(c) figure
names "clearing a slab declaration" as its directory-only example and does
not name changing one. And the "what the line gives up" sentence is offered
as the statement of exclusions "rather than carved around", so under (R-a) it
is silent about a permitted change while under (R-b) it is silent about a
forbidden one — one of the two lists is incomplete on either reading.
`[R-SLB-04]` cuts less than it appears to: it constrains a change that
happens, it does not grant one, and §20.3 says flatly that "which changes are
permitted is what this step's list of exceptions above states".

**Which I picked, and why.** (R-a), on the two-commit argument: a restriction
that a second commit dissolves cannot be what a list built to remove edges is
for, and alignment is the one declaration §20.3's own reasoning excuses,
since "a slab or alignment declaration governs placement (§16), not a value,
its coordinate or its padding" — the sentence that explains why member (5) is
safe is entirely indifferent to *which* value is declared. But I am picking,
and an implementer reading the closed list as closed will pick the other way.

**What an implementer does wrong without it.** Under (R-b) my updater refuses
"lower this layer's alignment from 4096 to 512" — an operation that is
trivially satisfiable, since every 4096-aligned offset is 512-aligned, so the
new generation's invariant holds over every stored tile the new state keeps
without moving a byte — and instead rewrites the file whole under a fresh
`file_id`, invalidating every `(file_id, range)` cache entry
(`[R-LIF-03]`) and duplicating every stored tile. Under (R-a) it appends a
directory, a pad and a trailer. The two updaters, given the same file and the
same instruction, emit different byte sequences and each believes itself
conforming.

The same question runs over S and A_slab, where it is sharper still: a layer
declaring S = 8 that wants S = 16 with the same A_slab has no in-place path
at all under (R-b), even where every run of the new partition is already
packed and aligned.

Location: §20.3, `[R-WRT-04]` step 4. The same triple of verbs appears
unchanged in §11.1's *Rationale* and in Appendix H's updater checklist, so
neither of those resolves it; a whitespace-normalised sweep for the phrase
found it in exactly those three places plus the below-clause's two-verb form.

**Byte-level: yes.** Two conforming updaters, both handed generation *n* of a
file whose layer `L` declares A = 4096 with every stored tile at a multiple of
4096, and both told to set A to 512. Updater X (reading R-a) appends a commit
whose directory carries `L`'s record with the alignment field holding
`00 02 00 00 00 00 00 00`, followed by a pad and a trailer with the same
`file_id` and F increased by at least 128. Updater Y (reading R-b) will not
emit that commit at all; it emits a whole new file under a fresh `file_id`
carrying none of the input's superseded bytes. The file X emits is a
**conforming file** — the new generation's alignment invariant holds over every
stored tile it keeps (`[R-SLB-01]`, L40), `[R-CNT-16]` is satisfied since S
stays 0, `[R-CNT-23]`'s power-of-two range 512 ≤ A ≤ 2⁶² is satisfied — so
this is not a case where `[R-CNF-05]` bars both readings alike; only one
reading permits an actor to produce it, and the two actors' outputs differ
from the first byte of the new directory onward. This is the same shape as the
composition defect the previous round established here, one level down: not
which pairs of members may be combined, but how far a single member reaches.

### writer-02 — OBSERVATION

**§20.3 step 4 and §2.3 (`[R-CNF-02]`).** The closed list of step 4 is a
writer obligation whose violation this specification never classifies, and
whose violating file is conforming.

Quotation (§20.3):

> A commit MUST NOT change one of
> these; the change is a new layer, or a whole-file rewrite under a
> fresh file_id (`[R-LIF-01]`, §20.5).

and (§2.3, `[R-CNF-02]`):

> A writer obligation whose
> violation this specification expressly declares not to be a
> file-conformance violation binds the actor in the same way; §6.3's
> flags rules against a set ignore-lane bit — a creator's flags = 0,
> and an updater's or compactor's copy-forward and set-no-other
> (§20.5) — and §6.2's pre-trailer gap longer than `[R-LIF-02]` step
> 5's pad are the cases this text states, and each is declared where
> it arises rather than enumerated here.

Every fact about a generation is a fact about the live state alone. A commit
that changes, say, a tile extent on a layer that stored a tile leaves a live
state that is byte-indistinguishable from one a creator could have emitted
lawfully; §9.6's backward probe can reach the superseded trailer, but "no
verdict turns on the probe" and "the earlier state the probe finds is a
different artifact". So the resulting file satisfies file conformance, which
§2.3 makes "a pure predicate on bytes", and `[R-CNF-05]` is not violated.

That leaves step 4's MUST NOT in a category the document never names. It is
not a conduct rule of the §10.3/§18.3 kind (it does constrain bytes). It is
not one of `[R-CNF-02]`'s expressly-declared cases, which the text says are
two and enumerates. It is not an *unwitnessed condition* in §21.7's sense
either, strictly, since §21.7's definition quantifies over "every file
exhibiting it" and no file exhibits a fact about its predecessor; it is nearer
§21.7's other category, "a requirement that states no condition a file can
exhibit", whose only stated instance is `[R-ENC-06]`'s field widths.

I raise this as an OBSERVATION rather than a defect in a rule because nothing
an implementer builds turns on it: under every classification the actor is
bound and no reader or verifier check changes. It is decidable from the text —
each of the three categories is defined — but deciding which one step 4 falls
into costs a reader four cross-references and yields nothing, which is the
OBSERVATION shape. Naming it where step 4 arises, as `[R-CNF-02]` says every
such case is named, would close it in a sentence.

**Byte-level: no.** Under every reading the actor is barred from making the
change and no reader's or verifier's accept/reject verdict moves; the file is
conforming on all of them.

---

## 9. What I looked at and found clean

Recorded because a lane that finds little should be able to say what it did
that would have found something.

- **Creation.** Rebuilt Appendix A byte-for-byte from §6.1/§6.2 alone, and
  built an independent 768-byte file whose layer-record inline payload landed
  on §7.4's stated 81 bytes. Any width, order or padding error in §7.4's table
  would have shown as a length mismatch. None did.
- **The register's own arithmetic.** Parsed §21.2–§21.5 mechanically:
  35 + 49 + 26 + 10 = **120 conditions**, and counting instance cells by the
  rule §21.1 states (semicolon-separated; a cell reading "—" is one instance)
  gives **277 instances**. `[R-ERR-02]` states "120 conditions over 277
  instances". Exact match. Per-subsection: F 35/56, L 49/116, T 26/55,
  R 10/50.
- **`[R-WRT-06]`'s row enumeration.** "one row for each of the other seven
  spaces §10.2 tabulates (L31, L33, L34, L36, L43, L45, R1)" — §10.2 tabulates
  eight spaces, record type plus seven, and the seven named rows are index
  encoding, linearization, sample type, layout, codec, filter and metadata
  encoding. Correct and complete, channel layout's absent experimental range
  included (L36 covers "layout 0; reserved 3-255").
- **`[R-CNF-13]`'s reach derivation.** F8, F14, F6 and both F1 instances assert
  invariants `[R-CNT-24]` fixes; F13 (F a multiple of 64) and F17
  (committed_file_length against the transport size) do not, because
  `[R-CNT-24]` fixes only the magic at F − 64, the version fields at F − 56,
  the CRC at F − 4, and the front block. The stated set is right.
- **§9.6's candidate test** against all five crash points in §5 above; each
  produces a state the register already names.
- **The lattice of record flags** (§3.3's table) — every cell decided.
- **The pair table** (§7.1) — no undecided pair.
- **Appendix G item by item** against 24 degrees of freedom (§6) — none left
  open, and two of its claims independently verified.
- **Cross-checked worked numbers**, all matching: §11.4's ordinals
  (s = 10, in-tile 11,452, planar disk ordinal 74, entry at region bytes
  [1,480, 1,500)); §15.4's million-entry layer (16 segments, 15 full + 16,960,
  64-byte array, 20,000,064-byte region, segment 15 at [19,660,800,
  20,000,000), ~339 KB, a full segment 1.25 MiB); §14.2's decoded sizes
  (18, 12, 30) and offsets ([15,18), 10–11, [25,30)); §14.3's ⌈10/8⌉ = 2 and
  `55 01` / `55 FD`; §14.5's 2 × 2 grid with 1 real and 15 padding positions
  in 32 bytes; §16.2's four runs; §21.9's note (2³² tiles → 256 KiB CRC array,
  2³⁶ → 4 MiB); §4.6's `température` at 12 bytes NFC and 13 NFD; and
  `[R-CNT-17]`'s formula at entry_count 4 → 84 and 5 → 104.

Suspicions I opened and closed:

- **`[R-CNT-22]` vs `[R-WRT-05]` on a modified record.** Does an appender that
  modifies a layer record whose stored PE bit is wrong emit the corrected
  flags or the stored ones? Closed by two sentences: `[R-WRT-05]`'s "a record
  it modifies is new output under its writer obligations", and §20.3 step 2's
  "Reproducing a structure's bytes unchanged is not authoring them", which
  together split the case cleanly between modified and carried-forward.
- **A compactor that modifies a layer record carrying an undetected flag
  violation.** `[R-WRT-07]` enumerates the modifications relocation licenses
  ("re-points extent slots, regenerates each tile-index region…, and updates
  the layer-record fields covering a regenerated region"), so everything else
  falls to §20.4's byte-identity; and §20.5's promise is conditioned —
  "*Given a conforming input* the output is a conforming file".
- **A compactor's duty to refuse turning on its own placement choice** (a
  structurally-malformed index entry is met only if the region is
  regenerated). Closed expressly: "That `[R-WRT-09]`'s checks reach the index
  chain and each stored tile's entry crc rather than an entry's own value
  domain bounds how far a compactor goes looking".
- **"a name enters no map this specification defines"** (§20.3), against
  §18.4's `tarn.stats`, which is "an object keyed by channel name". Closed by
  context and by `[R-MTA-08]`, which already licenses `tarn.stats` to be stale
  after any commit that changes the layer; the sentence's "map" is plainly the
  structural kind §14 and §11.4 read a tile under.
- **`[R-CNT-03]`'s gloss** ("the run before an aligned tile or slab run, and
  the pre-trailer pad") against gaps a scattering writer creates for no
  alignment reason. Even if the gloss is restrictive, `[R-CNT-03]` is a SHOULD
  and `[R-CNF-12]` puts SHOULD deviation outside the register, so nothing
  moves.
- **§18.2's finiteness test.** With roundTiesToEven named, the overflow
  boundary is a single exact threshold (2¹⁰²⁴·(1 − 2⁻⁵⁴)), so two readers
  cannot disagree about which numbers are finite; underflow to zero stays
  readable, which is consistent with the rule as written. The carry-over list
  from `[R-COD-06]` is complete: magic, no skippable/second frame, no
  dictionary and no dictionary ID, no content-checksum flag, and the
  no-sizing-from-a-declared-length bar are exactly `[R-COD-06]`'s constraints
  less the three §18.2 replaces (decoded size, `Window_Size`, and the SHOULD
  about the window).
- **The two-verb below-clause for the alignment.** "an aligned layer's stored
  tiles — every one the new state keeps, not only those this commit adds —
  satisfy its invariant or the declaration is cleared" is agnostic about the
  declared value and therefore does not resolve writer-01 either way.

---

## 10. Sweeps run

All against `spec/tarn.md` only. Every zero-bearing sweep was re-run
whitespace-normalised and paired with a control.

| Sweep | Hits |
|---|---|
| `grep -nE '^\| (F\|L\|T\|R)[0-9]+ \|'` (register rows) | 120 |
| `grep -c "re-established"` (control for the verb sweep) | 4 |
| `grep -n "re-established or cleared"` | 3 (§20.3 list, §20.3 below-clause, App. H) |
| `grep -n "declaration itself"` | 1 (`[R-SLB-04]`, §16.2) |
| normalised `grep -o "declaration MAY be declared, re-established or cleared[^.]*\."` | 1 |
| normalised `grep -o "may be declared, re-established or cleared[^;]*;"` | 1 (§11.1 Rationale) |
| normalised `grep -o "a slab or alignment declaration declared[^—]*—"` | 1 (App. H) |
| `grep -c "and no other"` | 3 |
| `grep -c "keeps its declarations"` | 1 |
| `grep -c "whole of what a commit MAY do"` | 1 |
| `grep -c "gives up is stated"` | 1 |
| normalised `grep -o "What the line gives up is stated rather than carved around:.\{0,700\}"` | 1 |
| normalised `grep -o "keeps its declarations, with these exceptions and no other:.\{0,600\}"` | 1 |

Transcript finding count: **2**.
