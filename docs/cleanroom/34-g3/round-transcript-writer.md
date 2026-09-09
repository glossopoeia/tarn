# Round 34 — Writer implementer — working transcript

## 0. Access, disclosure, and two things that were not where the brief said

I read exactly one file of the repository: `/Users/robertkleffner/Documents/GitHub/tarn-first-draft/spec/tarn.md`,
in full, in four `Read` calls. I opened no ADR, no `docs/`, no `conformance/`,
no `spec/registry.json`, no `PLAN.md`, `AGENTS.md`, `README.md`. I ran no
`git` command, no web search, no web fetch. I listed no repository directory.

Two disclosures.

**(1) Context I did not ask for.** Before my first tool call, my runtime placed
a project-instruction pointer and an index of the maintainer's auto-memory notes
into my context. The index consisted of titles of TARN-related notes — several of
them plainly about this round's machinery and about where this project's defects
have historically lived. I did not open any of them and I have not repeated their
contents here. I have deliberately not let any of them steer a search: every
suspicion below is traceable to a passage of `spec/tarn.md` I quote, and where a
line of thought could have been suggested by that index I re-derived it from the
document and say so. One of those titles bore on a shape I would in any case have
been told to check by the brief itself (the brief's shape 5), so its appearance
changed nothing about where I looked; I record it because an undisclosed breach
poisons the round and a disclosed one is usable.

**(2) The scratch directory was not empty.** The brief says
"Your scratch directory is `.../r34-round/scratch/writer/` and it is yours alone.
Create it yourself." I ran `mkdir -p` on it and then listed it. It already
contained, timestamped 08:01–08:16 (my session began at ~08:40):

```
appA.py  countreg.py  crc32c_tools.py  emit_gen1.py  emit_gen2.py
gen1.tarn  nsearch.py  sec74.py
```

These are exactly the working files a Writer-lane agent would produce — a CRC
tool, an Appendix-A checker, a register counter, two generation emitters, a
normalised-search tool, a §7.4 layout script, and an emitted `.tarn`. I did not
read any of them, did not execute any of them, and did not overwrite them. This
is precisely the cross-contamination the brief describes ("one agent's script was
silently replaced by another's between two calls"), and reading them would have
put another run's derived numbers into my context. I created
`.../scratch/writer/w34-rk/` and worked only there, with `w34_`-prefixed
filenames. Files I wrote, all under `w34-rk/`:

`w34_flat.txt`, `w34_map.json`, `w34_search.py`, `w34_crc.py`,
`w34_checkdoc.py`, `w34_emit.py`, `w34_verify.py`, `w34_gen2.py`, `w34_count.py`,
`w34_gen1.tarn`, `w34_gen2.tarn`. (I also wrote `flat.txt` into the parent
`writer/` directory on my first call, before I had listed it and discovered it was
occupied; that file did not exist beforehand and I overwrote nothing.)

I take the directory's prior contents to mean either that this lane has been run
before against this same path, or that another lane is pointed at it. Either way
the brief's promise that the directory is mine alone did not hold, and a reader of
this round should know it.

## 1. Instrument checks before any conclusion

The document is hard-wrapped and blockquotes carry `> `. A line-oriented grep
misses most multi-word phrases. So I built a normalised flat text: strip a leading
`>` marker per line, collapse whitespace, join, keeping a char-offset→line map
(`w34_flat.txt` / `w34_map.json`, 284,550 chars). Every search below runs over
that. Every search set includes at least one **positive control** — a phrase I
know is in the passage — and one **negative control** (`zzqqxx`, 0 hits). No
conclusion below rests on a zero that was not paired with a control.

CRC-32C implementation checked against the document's own three constants
(§4.5, §15.4, Appendix B) before any use:

```
CRC32C("123456789")                 = 0xE3069283   doc: 0xE3069283   OK
CRC32C(<zero bytes>)                = 0x00000000   doc: 0x00000000   OK
CRC32C(2^16 sentinel entries)       = 0xEECB3BB2   doc: 0xEECB3BB2   OK
```

Then against the document's worked examples:

```
Appendix A trailer CRC over [0,60) = 0x402F157E   doc: 0x402F157E   OK
§7.4 4-sentinel entry array CRC    = 0x80A34955   doc: 0x80A34955   OK
§7.4 crc_of_crc_array              = 0xC4EE982E   doc: 0xC4EE982E   OK
§7.4 layer payload length          = 81 bytes     doc: 81           OK
   field offsets 0,4,5,7,9,11,19,27,35,36,38,56,68,69,77 — all match the example
   4 + 34 + 18 + 12 + 13 = 81                                       OK
```

So the instrument is sound and §7.4's example is internally exact.

## 2. Creation: a byte-layout walk

I built a two-layer file end to end (`w34_emit.py` → `w34_gen1.tarn`), then wrote
an *independent* verifier (`w34_verify.py`) that re-derives every quantity from
the bytes and re-runs §6.2, §7.1, §7.2, §7.4, §11.2, §14.2/§14.3, §15.1/§15.3/§15.4,
§16.1/§16.2, §17.2, §5.2 and §9.7.

**Design.**
- layer `grid`: interleaved, rank 2, dims `y`(E=5,T=4), `x`(E=5,T=4). G=(2,2),
  N=4, P=16. Channels `a` uint8 fill `07`, `b` uint16 fill `ABCD`. Q=1+2=3,
  decoded size P·Q = 48. codec 1, filter 1. **alignment A = 512.**
- layer `mask`: planar, rank 1, dim `x`(E=10,T=8). G=2, N=2, P=8. Channel `m`
  bool fill `00`. C=1, entry_count = C·N = 2. Packed plane, decoded size
  ⌈8/8⌉ = 1. codec 1, filter 1. **slab S = 2, A_slab = 1.**
- one file-scope user-metadata record, encoding 1, document
  `{"tarn.creator":"w34-rk 1.0","tarn.title":"demo"}` (49 bytes) + 4-byte CRC.

**Emitted layout (generation 1, F = 2560).**

```
[0,16)        front signature block          89 54 41 52 4E 0D 0A 1A + 8×00   §6.1 FIXED
[16,69)       user-metadata extent (53 B)    doc 49 B + terminal CRC-32C 4 B  §7.1/§8.1
[69,70)       mask tile ordinal 0            byte 0x55                        §14.3
[70,71)       mask tile ordinal 1            byte 0x01                        §14.3
[71,512)      slack (441 B)                  gap forced by A=512              §5.2
[512,560)     grid tile s=0  (48 B)          512 mod 512 = 0                  §16.1
[560,1024)    slack (464 B)
[1024,1072)   grid tile s=1
[1072,1536)   slack (464 B)
[1536,1584)   grid tile s=2
[1584,2048)   slack (464 B)
[2048,2096)   grid tile s=3
[2096,2180)   grid tile-index region (84 B)  4×20 + ⌈4/2^16⌉×4 = 84           §15.1/[R-CNT-17]
[2180,2224)   mask tile-index region (44 B)  2×20 + 4 = 44
[2224,2478)   directory region (254 B)       3 records + 4-byte CRC           §7.1
[2478,2496)   pre-trailer pad (18 B)         to the next 64-boundary          [R-LIF-02] step 5
[2496,2560)   trailer                        F = 2560, 2560 mod 64 = 0        §6.2
```

Directory: layer record `grid` (type 0x0001, flags 3 = MU 1|PE 1, inline 101,
extent (2096,84)); layer record `mask` (inline 76, extent (2180,44));
user-metadata record (type 0x0002, flags 2 = MU 0|PE 1, inline 1 = `01`,
extent (16,53)).

Independent verification: **12 claimants, 709 bytes claimed, 1851 bytes slack,
no overlap, every checksum verifies, every codec-1 length equals its decoded
size, every aligned offset is 512-aligned, the slab run is packed.**

### 2.1 Every decision, and whether the document fixed it

| Decision | Fixed by | Free? |
|---|---|---|
| bytes [0,16) | §6.1, "Writers MUST emit exactly these 16 bytes" | fixed |
| first structure at 16 | [R-CNT-13] extent_offset ≥ 16; §15.3 tile offset ≥ 16 | floor fixed, position free ([R-SLB-05]) |
| order of tiles / index / extents | §9.2 step 2 "in any order satisfying §5.2's coverage classes" | **free** |
| aligned tile offsets 512/1024/1536/2048 | [R-SLB-01] offset mod A = 0 | multiples free, congruence fixed |
| index region need not be A-aligned | [R-SLB-01] quantifies over "every **stored tile's** offset" only | fixed (unconstrained) |
| slab run packing 69→70 | [R-SLB-03] "each stored tile's offset equals the previous stored tile's offset plus that previous tile's length" | fixed |
| A_slab = 1 → first-tile alignment vacuous | §16.2, "With A_slab = 1 a slab is contiguity-only" | fixed |
| directory last | [R-CNT-05] "no structure lies between its end and the trailer" | fixed |
| pad length 18 | [R-LIF-02] step 5 "to the next 64-byte boundary"; [R-CNT-05] "a writer that ends its directory on a 64-byte boundary leaves none" | fixed |
| F = 2560 | §6.2 F mod 64 = 0; pad + 64 | fixed once dir end is fixed |
| gap **content** (1851 B) | [R-CNT-03] SHOULD zero; [R-CNT-21] "its content is unconstrained" | **free** |
| file_id | §6.2 ≠ 0; [R-LIF-03] SHOULD be random | **free** |
| version_minor = 0 | [R-CNT-26] SHOULD "the lowest ... that defines every feature present" | **free** (SHOULD) |
| flags = 0 | §6.3 "a writer creating a file under this text MUST write flags = 0" | fixed |
| edge padding content | [R-SER-05] fill at every padding position | fixed |
| pad bits | mask tile 1: P=8, P mod 8 = 0, so **no pad bits**; §14.3's Note distinguishes them from padding positions | fixed |
| entry_count, extent_length, crc_of_crc_array | [R-CNT-17], [R-CNT-23] | derived |
| record order in the directory | [R-CNT-14] "Record semantics MUST NOT depend on record order" | **free** |
| which tiles to store | free where the tile is all-fill; forced otherwise (§3.2's reference array) | **free** for all-fill |

Nothing in creation left me guessing. The one place I had to read twice was
§9.7's claim that the tile-index region "enters the walk once, as that record's
extent, and is not a second claimant beside it" — my first verifier double-counted
it and tripped its own overlap check. The document had already anticipated exactly
that error; the sentence is doing real work.

## 3. The append procedure

### 3.1 A concrete second generation

`w34_gen2.py` → `w34_gen2.tarn`. Commit 2 does three things at once, which is
the interesting case: it **supersedes** one `grid` tile, it **grows** `mask`'s
extent 10 → 20 (G 2→3, N 2→3, entry_count 2→3), and it therefore has to deal
with a slab whose run partition changes.

Order followed, per §20.3 step-by-step:

1. **Establish F.** Validate the trailer in the final 64 bytes ([R-LIF-04]).
   F = 2560. Physical length = 2560, so neither truncate nor overwrite applies.
2. **Open** (§19.1, four steps). Appender is a reader here.
3. **Validate what the commit touches** ([R-WRT-03]): trailer + full directory
   always (re-emission relies on every directory byte), plus §19.3 layer
   validation for `grid` and `mask`, plus the §19.4 index chain for every segment
   whose entries the commit reuses. Both layers have one segment each.
4. **Write payloads and indexes**, beginning at exactly F = 2560:

```
[2560,2608)  grid tile s=1, new content   2560 mod 512 = 0            [R-SLB-01]
[2608,2609)  mask tile ordinal 0, re-emitted   \
[2609,2610)  mask tile ordinal 1, re-emitted    > run 0 = ordinals [0,2), packed
[2610,2611)  mask tile ordinal 2, new           > run 1 = ordinal [2,3)
[2611,2695)  grid index region, re-emitted in full (84 B)
[2695,2759)  mask index region, re-emitted in full (3×20 + 4 = 64 B)
[2759,3013)  directory (254 B)
[3013,3072)  pre-trailer pad (59 B)
[3072,3136)  trailer, F = 3136
```

   F grew by 576. The commit's minimum growth is 128 ([R-LIF-02]); §9.2's Note
   derives it (prior F + 4 + 64 = +68, rounded up to a multiple of 64 = +128).
   I re-derived it: correct.
5. **Re-emit the directory** per §20.4. The user-metadata record is re-emitted
   **byte-identically**, header, inline payload and extent slot ([R-WRT-05]),
   still pointing at (16,53) — the extent is not re-appended because the
   document is not modified.
6. **Commit**: barrier; pad; trailer with the *same* file_id, cfl = 3136,
   ignore-lane bits copied forward (none set), version_minor per [R-CNT-26];
   barrier.

Independent verification of gen 2: **13 claimants, 730 bytes claimed, 2406 bytes
slack.** Cross-check of the slack arithmetic: 1851 (gen 1) + 496 superseded
(old grid tile 48 + old mask tiles 2 + old grid index 84 + old mask index 44 +
old directory 254 + old trailer 64) + 59 (new pad) = 2406. Exact.

### 3.2 Two things the append forced me to notice

**(a) A grown extent turns padding positions into real positions.** `mask` tile 1
covered x = 8..15; under E = 10 the positions x = 10..15 were padding and
[R-SER-05] forced them to the fill bit (false). Under E = 20 those same stored
bits are now *real samples* reading false. The document says this in terms:
"a grown extent adds positions that held their channel's fill (§14.5), and fill
is a legal sample value" (§20.3). So the writer either accepts fill there or
supersedes the tile. I superseded it. This is stated, not left open.

**(b) Growing a slab-declared layer can make the invariant unsatisfiable in
place.** With C = 1 my run 0 stayed [0,2) and its frozen offsets 69,70 still
packed, so I could have left it. To probe the general case I worked the
arithmetic for S = 3, C = 2, N: 2 → 3. Old block [0,2) is one run; new block
[0,3) is one run [0,3). Ordinal 2's tile must sit at `offset(1) + length(1)` —
a byte position inside the committed prefix, which [R-LIF-01] freezes. So the
writer must either sentinel ordinal 2, or supersede the whole run at appended
offsets, or clear the declaration. The document gives exactly those:
[R-SLB-04]'s "MUST either re-establish the invariants for every such run — or
clear the declaration in the new generation", and §20.3's "has its invariants
re-established over every run the new state keeps, or is cleared". Determined.

I checked [R-SLB-04]'s trigger list against every permitted change of §20.3
step 4 and it is complete over conforming inputs (see §7.3 below).

### 3.3 Adding to a file whose records I do not all understand

Walking every flag combination the document defines, crossed with the three
authority sources §20.4 names and with the two scopes.

Authority for the flags ([R-WRT-05]/§20.4, "only the authoritative source of the
flags differs"):
- type §7.3 registers → the **registry's fixed** flags govern ([R-CNT-22]);
- unregistered type the updater **implements** → the definition it implements
  the type from supplies them, "and the stored bits never do";
- type the updater does **not** implement → the **stored** flags are
  authoritative, with MU=1/PE=0 read as PE=1 ([R-CNT-12]).

| Governing MU / PE | Top-level record | Layer sub-record |
|---|---|---|
| MU=1, PE=1, **type I implement** (0x0001 layer; 0x0002 is MU=0) | §20.4's MU=1 row does **not** reach it: "Its MU = 1 row reaches only a type the updater does not implement ... so for an implemented type only the PE bit bites." I may modify the layer as §20.3 step 4 permits. PE=1 → I may **never drop** it. | same |
| MU=1, PE=1, **type I do not implement** | Retain byte-identical; **no commit is available at all** — [R-CNT-15] makes it reject-file and I am a reader first (§2.3). A compactor MUST refuse ([R-WRT-06]). | Retain byte-identical; **modification of that layer is blocked**, other layers stay editable ([R-CNT-18]). I may still re-emit the layer record byte-identically as part of a commit touching another layer — that is [R-WRT-05], not modification. |
| MU=1, PE=0 **stored** | Never legal to emit ([R-CNT-12]); as a reader/updater I **MUST treat it as PE=1**, so it collapses into the row above. A verifier records F25 / L46. | same, L46 |
| MU=0, PE=1 (0x0002 user metadata; any ancillary so registered) | Retain byte-identical, **extent content unmodified**. Editing the document is a *modification*: I append a new extent and re-point the slot, the old extent becoming slack (§20.3 shape (b), §23.1). | same, L19 caps it at one per layer |
| MU=0, PE=0 | Retain byte-identical, **or drop it — its extent becoming slack**. "an updater MAY drop the record in any commit it is otherwise free to make — one whose only effect is the drop included". I SHOULD report the loss. | same |
| reserved-range type (0x0003–0x7FFF), any MU | I read it under the MU rule unchanged; a verifier records F36 (F35 when MU=1) / L25 (L24). I do **not** repair it; it travels with the file ([R-WRT-01]). | L25 / L24 |
| experimental-range type (≥0x8000), MU=0 | Conforming file (§21.6); ignored; preserved or dropped per PE. | same |
| experimental-range type, MU=1 | Conforming file a reader **refuses** (§21.6's closing paragraph) → no commit. | reject-layer only; the file is not refused ([R-CNT-18]). |

Also binding on me throughout: [R-WRT-08], "An updater MUST NOT re-encode a
record whose type it does not implement, and MUST NOT modify one except by
relocating its extent and re-pointing its slot under §20.5"; and §20.3 step 2,
"a malformed index entry an appender meets while re-emitting a region is carried
forward byte-identically at its disk-ordinal position under step 4, not repaired
to a sentinel."

**Write order, durability, commit point.** [R-LIF-02]: (1) begin at exactly F;
(2) payloads, index regions, record extents, in any order; (3) complete
directory + its CRC; (4) **barrier**; (5) pad + trailer; (6) **barrier**. The
commit point is the trailer of step 5 becoming visible; steps 4 and 6 bind
conduct, not bytes ("a file committed without one can be byte-identical to a file
committed with it"). Both barriers, not one — §20.2 and §20.5 each say so
explicitly.

## 4. Slack, by commit shape

| Shape | Bytes that become slack | Counted by | Content |
|---|---|---|---|
| **Append (new layer)** | the superseded directory, pad and trailer only — "sized by the file's *layer count*, never by any layer's data" (§20.3 (a)); plus any alignment/placement gap the new structures leave | a verifier, "MUST report the total number of slack bytes" ([R-CNT-21]) | unconstrained; writers SHOULD zero ([R-CNT-03]) |
| **Append (tiles added / superseded)** | the layer's **whole** prior index region, every superseded payload, the prior directory/pad/trailer, plus new gaps. My gen 2: 496 bytes | verifier | unconstrained |
| **In-place update** | does not exist. [R-LIF-01] freezes [0,F); every "in-place" edit is an append. Editing user metadata appends a new extent and strands the old (§23.1, §20.3 (c)) | verifier | unconstrained |
| **Directory-only commit** | prior directory, pad, trailer; plus any extent owned by a dropped PE=0 record | verifier | unconstrained |
| **Whole-file rewrite (not compaction)** | none in the new file beyond its own pad/gaps; the *input* survives untouched ([R-PRV-02]) | verifier of each file separately | unconstrained |
| **Compaction** | none carried: "A compactor's output contains only the structures reachable from the input's live trailer ... so slack is never carried." The output still has its own pre-trailer pad and any gap a declared A/A_slab forces | verifier | unconstrained |
| **Abandoned partial write** | **no bytes become slack.** Slack is a property of the live committed state; where §6.2's ordered validation rejects before a live trailer is established "there is no F and no live state to walk, so the total is not owed at all" (§5.2). The residue makes the file nonconforming (F17), and [R-LIF-04] obliges the next writer to truncate to F or overwrite from it | nobody — the verifier "reports the trailer failure and nothing about slack, which is not a partial total but the absence of one" | n/a |

Partial totals: where the walk does not complete (scope-level rejection, a layer
declined on resource grounds, or a stop at the first violation under [R-CNF-11]),
the verifier reports "F less the bytes claimed by the claimants the walk did
enumerate — an upper bound ... never an under-count" and MUST say what stopped
it. A tile's or document's *decode* declined leaves the walk complete. An entry
[R-IDX-03] classifies reject-tile on a **structural** ground also leaves it
complete, "for the opposite reason: it contributes no claimant". Both cases are
stated in §5.2 and again in §9.7 and agree.

## 5. Torn-write recovery — five crash points

**P1 — crash inside step 2** (payloads written, no directory). Physical > F.
Next reader: the final 64 bytes are not a valid trailer, so §6.2's magic/CRC/length
gates fail (F8, F14, F17); [R-LIF-05] forbids scanning backward, so the reader
"MUST report the file torn or invalid". Next updater: [R-LIF-04] — validation
fails, "the writer MUST NOT append"; §9.6 recovery is a separate, deliberate
operation. Conforming in the meantime? **No** — F17.

**P2 — crash after step 3, before step 5** (directory written, no trailer).
Identical observable state to P1. §9.2's figure draws exactly this row.

**P3 — crash mid-trailer.** The final 64 bytes exist but are torn: F8 (magic)
or F14 (CRC) or F17 (length). Same handling. §6.2's Note covers the nasty
sub-case where a *payload* mimics a trailer at exact physical end: "it is caught
at the directory CRC (§7.1)".

**P4 — crash after step 5, before step 6.** If the trailer bytes reached stable
storage, the file is complete and conforming and the commit stands. If they did
not, the state is P2. §9.2's Note prices the difference: "Where barriers are
weaker than assumed, safety degrades from 'torn commits are invisible' to 'torn
commits are detected'."

**P5 — the [R-LIF-04] overwrite-and-truncate path, crash before truncation,
new F' < stale physical length.** The physical tail holds stale bytes from the
abandoned longer file. Reader: torn. Recovery: §9.6's probe starts "at the
largest 64-aligned offset o with o + 64 ≤ the physical file length" and demands
`committed_file_length = o + 64` plus a verifying CRC, then whole-file
re-verification; it lands on the new trailer at F' − 64 and truncating to F'
recovers the completed commit. The tool MUST report "the candidate it settled on
and how many candidates it rejected".

Nothing here left me guessing. The one place where I had to reason rather than
read is that a *valid* trailer at the physical end of a file whose step-4 barrier
never ran can commit a state whose earlier bytes never flushed — the document
answers with §8's chain (the directory CRC catches it) rather than with a rule,
which is the right answer but is a Note rather than a requirement.

## 6. Byte-divergence catalogue

Two conforming writers, identical input arrays, identical stated options. I found
these degrees of freedom, and checked each against Appendix G item by item.

| # | Divergence | Document's licence | Appendix G |
|---|---|---|---|
| 1 | tile extents | §11.3 "Tile extents are a writer's choice, and this specification imposes none" | item 5 closes |
| 2 | layout interleaved/planar | §14.1 leaves it to the writer | item 5 closes |
| 3 | codec choice | [R-COD-03] any of 1–4 | item 1 closes |
| 4 | encoder output for a given codec | [R-CNF-05]; §17.2's Note on deflate's unused final-byte bits | item 1 closes (by pinning implementation, version, level, strategy, thread count) |
| 5 | filter choice | [R-COD-09] 1 or 2 | item 5 closes |
| 6 | alignment / slab declared at all, and their values | §16 leaves it to the writer | item 5 closes |
| 7 | placement order of structures | [R-SLB-05] "MAY occupy any non-overlapping byte positions, in any order" | item 3 closes |
| 8 | gap **extent** | [R-SLB-05] | item 3 closes ("each later structure begins where the previous one ended, save where alignment forces a gap") |
| 9 | gap **content** | [R-CNT-03] SHOULD; [R-CNT-21] unconstrained | item 3 closes ("every byte of every such gap is zero") |
| 10 | record order in the directory | [R-CNT-14] | item 3 closes |
| 11 | sub-record order | [R-CNT-14] | item 3 closes |
| 12 | file_id | §6.2 ≠ 0; [R-LIF-03] SHOULD random | item 2 closes **for a creator**; explicitly open for a compactor |
| 13 | version_minor | [R-CNT-26] SHOULD | item 8 closes for a creator; §20.5's carried-feature floor leaves a range for a compactor, which item 8 concedes |
| 14 | trailer flags | §6.3 MUST 0 for a creator; copy-forward for updater/compactor | item 8 closes |
| 15 | which all-fill tiles are stored | no rule requires the sentinel | item 6 closes |
| 16 | fill recorded when the caller chooses none | [R-TYP-10] SHOULD all-zero | item 7 closes |
| 17 | user-metadata JSON serialisation (number formatting, escaping) | [R-MTA-05] sorts keys but "does not make two writers' output identical" | item 9 closes |
| 18 | name normalisation NFC/NFD | [R-ENC-14] SHOULD | item 10 closes |
| 19 | number of generations | §9 nowhere constrains | item 4 closes |
| 20 | segment CRC for a full all-sentinel segment | [R-IDX-05] MAY emit the constant "without computing it" | **no divergence**: the constant *is* the computed value (I verified 0xEECB3BB2) |
| 21 | zstd Frame_Content_Size present or absent | [R-COD-06] "MAY be present" | item 1 closes (an encoder setting) |
| 22 | pre-trailer pad length | [R-LIF-02] step 5 + [R-CNT-05] | **not a freedom**: determined |
| 23 | which index regions a compactor regenerates | [R-WRT-07] "any of whose stored extents the output relocates" | determined once item 3 fixes placement |
| 24 | **whether a compactor drops a MU=0 / PE=0 record** | §20.4: "a compactor MAY drop it whenever it rewrites the file" | **NOT CLOSED — see finding writer-01** |

I checked the arithmetic in Appendix G item 5's identity claim, since it is the
one falsifiable piece of mathematics in the profile. The byte-shuffle sends byte
`i` of group `j` to `i·n + j`; the inverse sends `i·n + j` to `j·s + i`. Identity
requires `i·n + j = j·s + i` for all `i < s`, `j < n`. Setting `i=1, j=0` forces
`n = 1` whenever `s ≥ 2`; setting `i=0, j=1` forces `s = 1` whenever `n ≥ 2`. So
identity holds **exactly** when `s = 1` or `n = 1`, which is what item 5 says
("where the stride is 1 ... and equally where the decoded image is a single
group, n = L/s being 1"). Correct, and the "exactly" is earned.

I also verified §17.3's shuffle example byte for byte:
`00 00 80 3F 00 00 00 40 00 00 40 40` (s=4, n=3) shuffles to
`00 00 00 00 00 00 80 00 40 3F 40 40`. Matches.

Item 2's claim that a derived file_id "re-derived ... on an already-compact input
would reproduce the input's own file_id" is sound: under item 3 the output's
[0, F−64) and the trailer's other fields would be byte-identical to the input's,
so the hash input is identical — and [R-WRT-06] demands "a new draw ... not merely
a value compared against the input's". Correct.

Item 4's claim that "what refutes it is §9.6's backward probe finding a superseded
trailer" is sound given §9.1's committed-prefix immutability, modulo the mimic
case §21.6 and §9.6's second caution already name.

**A divergence I opened and closed:** `tarn.created` (§18.4, "an RFC 3339
`date-time`") is writer-generated, not input, so two runs of one writer diverge.
I decided this is *not* a divergence "given identical input" — the document's
own framing makes the metadata document part of the input, and item 9 pins the
serializer, not the content. Not filed.

## 7. Findings

### writer-01 — CONTRADICTION — Appendix G item 8 says a compactor's output is reproducible "only modulo its trailer"; §20.4 lets it drop a PE=0 record, which is not a trailer difference, and no profile item pins the choice

**Location:** Appendix G item 8; §20.4's flag table, the MU = 0 / PE = 0 row;
§20.5 first paragraph.

Appendix G item 8 says:

> A compactor's output is therefore reproducible only modulo its trailer:
> `[R-WRT-06]`'s fresh file_id is no function of content, and this item's floor
> turns on which features the compactor implements. An adopter needing
> byte-identity across compactors pins the compactor, as items 1 and 9 pin their
> producers.

§20.4's table says:

> Retain byte-identical, or drop it — its extent becoming slack. The licence is
> the bit's own: whoever fixed PE = 0 for the record, the writer that stored it
> or the definition that governs it, declined preservation across edits, so an
> updater MAY drop the record in any commit it is otherwise free to make — one
> whose only effect is the drop included — and a compactor MAY drop it whenever
> it rewrites the file.

and §20.5 confirms the output is "the live committed state (§7.2), **less any
record §20.4 lets it drop**".

Two compactors, given one conforming input carrying a MU = 0 / PE = 0 record and
both adopting the whole profile, may legitimately produce outputs that differ in
the **directory** — one record present, one absent — and therefore in
`dir_length`, in every offset downstream of the dropped record's extent, in the
directory CRC, in `committed_file_length` and in `F`. That is not a difference
"modulo the trailer"; the trailer differs only as a consequence.

I searched Appendix G for any coverage of this. Normalised search over the
appendix: `drop` → **0 hits**; `preserv` → **0 hits**; positive control
`compactor` → 8 hits, `record` → 25 hits, `modulo` → 1 hit. So the zero is a
real zero, not a wrap artefact. None of the ten items, and none of the closing
paragraph's enumeration ("gap *content* ... gap *extent* ... record and
sub-record order ... the fill a writer records ... the sentinel for every
all-fill tile ... a single generation ... the absence or fixing of a declared
alignment and slab ... `version_minor` at its floor ... a derived `file_id` ...
NFC-normalized names ... and the producer pinning of items 1 and 9") mentions
record retention or the PE bit.

The divergence is sharpened by §20.5's other clause: "A compactor ... MUST NOT
emit a file carrying a violation it has detected ... Dropping is the one disposal
that answers". Whether a compactor *has detected* a violation depends on how far
past [R-WRT-09]'s floor it looks, which is a per-implementation property — so
even the *forced* drops are not a function of the input alone.

**What an implementer does wrong without it:** builds a content-addressed store
on the profile, compacts, and finds the digest changes when the compactor is
swapped — having been told by item 8 that only the trailer could move. The fix
is a profile item ("retain every record the input carries; drop none") or a
correction of item 8's scope; I picked the reading that item 8 is simply
overstated, because §20.4's licence is unambiguous and normative and item 8 is
not.

**Byte-level:** no. Appendix G is identified non-normative and "adds no
requirement to any actor: a writer ignoring it is fully conforming". Both
outputs are conforming under the normative text. But it is a non-normative
passage that disagrees with the normative text it glosses, and it still tells an
implementer what to build.

### writer-02 — AMBIGUITY — §20.3 step 4 puts its own bar in §21.7's "no condition a file can exhibit" class, but a TARN file physically retains the superseded generation, which makes the bar *unwitnessed* instead

**Location:** §20.3 step 4; §21.7, [R-ERR-01]; §2.3, [R-CNF-02].

§20.3 step 4 says of the fixed-declaration bar:

> This bar binds the commit as an actor: no file is nonconforming by virtue of
> its violation, and no register row records the violation itself, the register
> enumerating file-conformance violations (§21.1) and the bar stating no
> condition a file can exhibit (§21.7, `[R-ERR-01]`, `[R-CNF-02]`); a file such
> a commit leaves can be nonconforming on its own terms, as the paragraph below
> sets out.

§21.7 draws the two classes apart deliberately:

> A condition this specification names is **unwitnessed** where, for every file
> exhibiting it, some file that does not exhibit it cannot be told apart from it
> by any check this specification obliges a reader or a verifier to perform.

> Distinguish an unwitnessed condition from a requirement that states **no
> condition a file can exhibit**. `[R-ENC-06]`'s fixed field widths are not a
> state a file can be in — the parse is always at the widths this specification
> fixes, and a structure written at any other yields different values at them —
> a different file, conforming or not on its own terms.

The two readings I can defend:

**(a) no condition a file can exhibit** — the bar's subject is an *event*
("a commit changed X"), and the live committed state carries no record of the
superseded generation's declarations, so no predicate over the live state
expresses it.

**(b) unwitnessed** — a physical TARN file *does* carry the superseded
generation. §9.1 makes committed bytes immutable; §9.6's probe finds the
superseded trailer; §23.2 says the "shape of its own history" is "recoverable by
probing backward for the superseded trailers that committed-prefix immutability
keeps in place". So the predicate "layer L declares X in the live generation and
declared Y ≠ X, with a tile stored, in the generation this trailer supersedes" is
evaluable on the bytes. It is simply read by no check any obliged actor performs
— §9.7's walk is live-state-only, and §9.6's probe is "not a reader behavior"
and, for a verifier, "diagnosis ... not a finding about the file it was given".
That is §21.7's definition of *unwitnessed*, word for word.

I worked a concrete witness. Take an interleaved layer, C = 1, uint8 channel,
extents divisible by tile extents (no padding positions). Generation 1 stores
tiles. Generation 2 flips `layout` 1 → 2. For C = 1 numeric the decoded image is
byte-identical under both layouts (§14.4's Note), `entry_count` is N either way
(N interleaved, C·N = 1·N planar), and the disk ordinal is s either way
(c·N + s with c = 0). Generation 2's file is fully conforming and denotes the same
reference array; the bar is violated and nothing in the live state shows it.
Yet generation 1's directory and trailer sit in the slack, byte-intact, declaring
`layout` 1 with a non-sentinel index — and §20.3's own re-emission clause means
generation 2 *kept the same extent slot*, so the index generation 1 stored under
is still live and still non-sentinel. §9.6's probe recovers the pair. So the
condition is exhibited, and exhibited legibly; it is unwitnessed, not absent.

I picked **(b)**. §21.7's own worked case for class (a) — [R-ENC-06] — turns on
an argument that does not transfer: the parse is *always* at the fixed widths, so
there is no alternative state. §18.2's use of the same class also does not
transfer for the same reason it works there: "the bar on sizing a buffer binds a
reader rather than the document, and so states no condition a file can exhibit at
all" — a rule binding a *reader* genuinely says nothing about any file. §20.3's
bar binds a writer and is about the file's declarations.

**What an implementer does wrong without it:** §21.7 says its test "decides any
condition put to it without appeal to a list", and §21.1's completeness clause
turns on that test. A worked example that files an unwitnessed condition under
the no-condition class mis-calibrates the instrument: applied consistently, any
condition whose witness lies in slack could be re-labelled "no condition a file
can exhibit", which collapses the distinction §21.7 exists to draw and would make
§21.1's completeness clause easier to satisfy than it should be. The verdict for
this particular rule does not move, because §2.3's [R-CNF-02] independently and
expressly declares it a conduct rule — that ground is sufficient on its own — but
the §21.7 citation is doing work it cannot do.

Secondary, and smaller: §21.7's paragraph on class (a) names only [R-ENC-06]
("Nothing is omitted from the register on its account"). It neither says its list
is open nor names §20.3's bar or §18.2's reader-bound rule, both of which now
claim membership. Normalised search for `no condition a file can exhibit` → 3
hits (§18.2 L2674, §20.3 L3236, §21.7 L4013); positive control
`unwitnessed` → 5 hits. So the class is invoked twice from outside the section
that defines it and enumerated nowhere.

**Byte-level:** no. [R-CNF-02] decides the conformance question either way, and
neither class needs a register row, so the emittable set and the accept/reject
verdict are unchanged under both readings.

### writer-03 — OBSERVATION — §20.3 step 4 restates the slab obligation over a *kept* declaration unconditionally, while [R-SLB-04], the rule it cites, fires only on five named triggers

**Location:** §20.3 step 4, closing sentence; §16.2, [R-SLB-04].

§20.3 step 4 says:

> Extents this commit supersedes become slack (`[R-CNT-21]`); a slab declaration
> declared, changed or kept has its invariants re-established over every run the
> new state keeps, or is cleared (`[R-SLB-04]`), and an aligned layer's stored
> tiles — every one the new state keeps, not only those this commit adds —
> satisfy its invariant or the declaration is cleared (`[R-SLB-01]`,
> `[R-CNF-05]`).

[R-SLB-04] says:

> A writer or updater whose commit changes the stored-tile set, the run
> partition, the byte placement of any run, the disk ordinal of any tile the new
> state stores, or the slab declaration itself, of a layer slab-declared in
> either the superseded or the new generation, MUST either re-establish the
> invariants for every such run — or clear the declaration in the new generation

The restatement's third verb, **kept**, has no trigger condition attached: read
as written, *any* commit — a rename-only commit, a commit that touches a
different layer entirely and re-emits this layer record byte-identically —
must re-establish this layer's slab invariants over every run or clear the
declaration. [R-SLB-04] fires on five named changes, none of which a rename-only
commit makes.

Note the asymmetry within the same sentence: the **alignment** half is stated at
exactly the right breadth because it is grounded in the invariant and in
[R-CNF-05] — "an aligned layer's stored tiles — every one the new state keeps,
not only those this commit adds — satisfy its invariant" — which is true
unconditionally of any file declaring A. The slab half is grounded in [R-SLB-04],
a *writer* rule with a trigger list, but is stated as broadly as the alignment
half.

I checked whether the divergence can bite on a **conforming** input. It cannot.
The slab invariants are a function of (i) the run partition, (ii) A_slab,
(iii) the stored tiles' offsets and lengths, and (iv) which tiles are stored;
[R-SLB-04]'s five triggers cover all four exhaustively (I walked every permitted
change of §20.3 step 4 against them — name change, extent growth, planar channel
list extended, planar channel list shortened, and each of the four
slab/alignment verbs including the exclusive alignment↔slab switch — and every
one that can disturb an invariant is on the trigger list). So on a conforming
input the broad reading is satisfied vacuously, and nothing moves.

The divergence bites only on a **nonconforming** input that already carries L41
or L42. There the two readings disagree about whether a rename-only commit owes a
slab check-and-fix — a check §19.3's layer validation does not include (L41/L42
carry detector *verifier*), so [R-WRT-03]'s reliance-depth does not require the
appender to have looked, while the broad reading of §20.3 obliges it to act on
what it has not checked. Deciding this costs an implementer a walk of
[R-SLB-04]'s trigger list against every permitted change and a determination that
the disputed file is already nonconforming — which is why I file it as an
observation rather than an ambiguity.

**Byte-level:** no. The disputed file carries a register-row violation (L41 or
L42) under both readings, so [R-CNF-05] bars every conforming writer from
emitting it either way, and the emittable set does not move. This is the exact
discriminator the brief names.

### writer-04 — AMBIGUITY — §20.3 step 4's "where a field is on both sides" names a dimension extent, which appears on the permitted list only

**Location:** §20.3 step 4.

The passage sets up two lists and then makes a claim about their intersection:

> A layer that stores a tile **in the generation this commit supersedes** keeps
> its declarations, with these exceptions and no other: its name, and its
> dimension and channel names, MAY change; an extent MAY grow, and MUST NOT
> shrink; a planar layer's channel list MAY be extended at its end or shortened
> from its end, but not both in one commit; and a slab or alignment declaration
> MAY be declared, changed, re-established or cleared as this step provides
> below.

> Every other declaration is fixed for as long as the layer stores a tile: the
> layout, the linearization and the index encoding, the codec and the filter, the
> rank and the dimension order, every tile extent, every channel's type and fill,
> an interleaved layer's channel list (its names aside), and the position of
> every planar channel the new state keeps.

> Between them the two lists reach every declaration field of §7.4, and where a
> field is on both sides — a dimension extent, a planar layer's channel list, an
> interleaved layer's channel list — the permitted side states the whole of what
> a commit MAY do to it

I verified the completeness claim field by field against §7.4's table — name,
layout, linearization, codec, filter, A, S, A_slab, rank d, channel count C, the
d dimension entries (name / extent / tile extent), the C channel entries (name /
type / fill), index_encoding, entry_count, crc_of_crc_array, sub-records. Every
one is reached. The claim holds.

The "both sides" enumeration does not. Two of the three named fields are
genuinely on both lists: a planar layer's channel list (permitted: extended or
shortened at its end; fixed: "the position of every planar channel the new state
keeps"), and an interleaved layer's channel list (permitted: its channel names;
fixed: "an interleaved layer's channel list (its names aside)"). A **dimension
extent** is on the permitted list only — the fixed list names "every tile
extent", which is a different field, and its opening words are "Every *other*
declaration", which excludes anything the permitted list already names.

Two readings:

**(a)** "both sides" = the two lists just stated. Then the sentence is wrong
about a dimension extent, and a reader who trusts it will hunt the fixed list for
dimension extents, fail, and have to decide whether the completeness claim in the
same sentence survives.

**(b)** "both sides" = the permitted and the *barred*, where "an extent MAY grow,
and MUST NOT shrink" is itself a permission and a bar in one clause — and indeed
"a shrink" heads the give-up list later in the step ("What the line gives up is
stated rather than carved around: a shrink, a fill change, a re-type, ...").
Then the sentence is right.

I picked **(b)**, because the sentence's conclusion — "the permitted side states
the whole of what a commit MAY do to it" — is true of a dimension extent under
either reading, and because the give-up list gives (b) a real referent. But (a)
is the natural reading of "the two lists ... both sides" in the same sentence,
and the two are not the same relation.

**What an implementer does wrong without it:** nothing, in the bytes. The cost is
a reader of the closed list spending time reconciling an illustration with the
lists it illustrates, in the one paragraph of this document where the closed list
is the whole point.

**Byte-level:** no. Under both readings a commit may grow an extent and may not
shrink one, and the fixed list's membership is unchanged.

## 8. What I checked and found clean

- **Every worked number in the document.** §7.4's 81-byte layer payload and its
  three CRCs; Appendix A's 128-byte file and its trailer CRC; §11.2's
  G=(4,8)/N=32/P=65536; §11.4's ordinals 0, 1, 8, s=10, in-tile 11,452, planar 74;
  §14.2's Q=3/size 18/bytes [15,18), planar 12/bytes 10–11, Q=5/size 30/[25,30);
  §14.3's `55 01` and `55 FD`; §14.5's 32-byte edge tile with 15 × `CD AB`;
  §15.4's 16 segments / 16,960 / 20,000,064 / 339,180 / [19,660,800, 20,000,000) /
  1.25 MiB, and 74 → [1,480, 1,500) with entries 96–127; §16.2's four runs;
  §17.3's shuffle; §20.3's 32·20 + 4 = 644; §9.2's +68 → +128 derivation;
  §21.9's 256 KiB at 2³² and 4 MiB at 2³⁶; §12.1's bfloat16 `0x3F80`; §4.6's
  12-byte NFC `température`. **All correct.**
- **The register's own counts.** Mechanically parsed every `| Fn |`/`| Ln |`/
  `| Tn |`/`| Rn |` row and counted instances by §21.1's stated rule
  ("Instances within a cell are separated by semicolons, and a cell reading — is
  one instance"): **35 + 49 + 26 + 10 = 120 conditions over 277 instances.**
  §21.2 says 35, §21.3 says 49, §21.4 says 26, §21.5 says 10, §21.8 says
  "120 conditions over 277 instances". Exact.
- **§20.5's arithmetic about the four extension vehicles.** "the two of §10.1's
  four vehicles §21.6 makes conforming" = ignore-lane bit + unrecognised `tarn.`
  key; "one row for each of the other seven spaces §10.2 tabulates (L31, L33,
  L34, L36, L43, L45, R1)" — §10.2 tabulates eight spaces, minus record type
  leaves seven, and the seven cited rows map one-to-one onto index encoding,
  linearization, sample type, layout, codec, filter, metadata encoding. Correct.
- **§2.3's closed list of conduct cases.** Searched for every express declaration
  that a writer obligation's violation is not a file-conformance violation:
  `not a file-conformance violation` → 1 hit (§6.3);
  `nonconforming by virtue` → 3 (§2.3, §9.2, §20.3);
  `conduct, not the bytes` / `conduct rather than the bytes` → 2 (§7.2, §21.6,
  both §10.3's publication bar, which §2.3 already places in its *first*
  category). The three cases §2.3 names — §6.3's flags rules, §6.2's pre-trailer
  gap, §20.3 step 4's bar — are the complete set. Clean.
- **§4.7's partition claim** that `version_minor` is the only descriptive field.
  I tested the trailer reserved bytes (F15 → acceptance → structural), the
  ignore-lane flag bits (classification is per field, and `flags`' incompat lane
  decides acceptance), record reserved flag bits (F26/L47 → verifier acceptance
  → structural), and a registered type's stored MU/PE (F28/L49). The partition
  holds.
- **[R-SLB-04]'s trigger list against every permitted change** of §20.3 step 4,
  including the exclusive alignment↔slab switch composed in one commit
  ("A commit MAY make several of these changes at once"). Complete over
  conforming inputs.
- **The four verbs across all four sites.** Normalised search
  `slab or alignment declaration` → 4 hits (§11.1's Rationale L1663, §20.3
  step 4 L3216, §20.3's safety paragraph L3279, Appendix H L4798) and
  `declared, changed` → 4 (L1663, L3217, L3320, L4799). §11.1's Rationale and
  Appendix H both carry all four verbs and both carry the channel-list exception.
  The one three-verb list, §20.3's closing "declared, changed or kept", is a
  different list — it is about *invariants*, and its `kept` is the below-clause
  counterpart of the permitted list's `re-established` (a declaration carried at
  the same value whose invariants must be re-established, which is exactly
  [R-SLB-04]'s "re-establish the invariants"). The four transitions —
  none→some, some→another, some→same, some→none — each have a verb, and the fifth
  (the exclusive switch) is reached by composition. **No missing verb.**
- **The re-emission clause's entry partition.** Tiles this commit stores or
  supersedes / tiles that become unstored / entries new to this generation /
  every other entry byte-identical at its disk-ordinal position — plus tiles that
  cease to be addressed, which correctly have no entry at all. Complete. And
  "a growth renumbers ordinals wherever [R-GEO-06] moves them, and nothing else
  this step permits moves one" is true: I checked each permitted change, and only
  an extent growth (through N) moves a retained ordinal.
- **"whether or not entry_count changes with it"** in the channel-shortening
  clause. This looked like dead text until I found the composition that exhibits
  it: shorten C 4→3 while growing N 3→4 leaves entry_count = C·N = 12 unchanged
  and extent_length unchanged, while the index content changes and every retained
  ordinal moves. The clause is doing real work.
- **Degenerate legal cases.** Zero-extent dimension (N = 0, entry_count = 0,
  extent slot (0,0), crc_of_crc_array = 0, and codec 4 conforming because
  [R-COD-07]'s cap is quantified over addressed tiles); a slab-declared layer
  with no addressed tiles (runs impose nothing); an aligned layer with no stored
  tiles (invariant vacuous); A_slab = 1 (L42 unexhibitable for that layer);
  P = 1 packed bool plane (7 pad bits, all forced to the fill bit); the smallest
  conforming file (128 bytes, verified against Appendix A byte for byte); the
  smallest legal commit (+128, derived independently).
- **[R-CNT-05]'s consequence for a writer** — the directory must be the last
  structure. My emitter honours it; F7 registers the violation.
- **[R-LIF-04]'s two options** produce identical bytes: truncate-then-append and
  overwrite-then-truncate both end at physical length = the new F with the same
  content.

## 9. Confidence

High on creation, append and slack: I emitted two generations, verified them with
independently written code, and every quantity the document states that I could
recompute, I recomputed and matched. High on the divergence catalogue: I
enumerated 24 degrees of freedom and traced each to a licensing rule and to a
profile item, and the one that is not closed (writer-01) is closed by a searched
zero with controls, not by an impression. Medium on torn-write recovery: I walked
five crash points and the document answered all five, but the answer at P4 leans
on a Note rather than a requirement, and I would want a second reader on that.

No finding here is byte-level, and I say so of each. I looked hardest at the
place the round points to — the four verbs of the slab/alignment member, the
transitions they must span, the clause they delegate to, and the three
restatements — and I could not make a fork out of it: the verbs cover the four
transitions, the fifth is reached by the composition sentence, the delegated
clause provides for each, and both the Rationale and the checklist carry all four
with the channel-list exception intact. What I did find in that paragraph is
smaller and is filed honestly as such.
