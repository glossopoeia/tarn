# Round 30 — Writer implementer transcript

## 0. Disclosure

I read exactly one file: `/Users/robertkleffner/Documents/GitHub/tarn-first-draft/spec/tarn.md`,
in full (4,743 lines / 47,313 words by `wc`), via `sed -n` in chunks. One `sed`
call (lines 3600–4000) overflowed the tool's output limit and the harness saved
the overflow to a tool-results file; I did **not** open that file and re-read
the range from the spec in two smaller chunks instead. I ran `grep`/`awk` only
over `spec/tarn.md`. I opened no ADR, no `docs/`, no `conformance/`, no
`PLAN.md`, `AGENTS.md`, `README.md`, `OPEN-QUESTIONS.md`, no `registry.json`,
no git history, no web.

Unrequested context: my runtime placed a project-instruction pointer
(`CLAUDE.md` → `AGENTS.md`) and an index of four auto-memory note titles in my
context before I began. I did not open any of them and did not act on them; I
name here only that they appeared. Their titles concern harness paths, a gate
word list, preflight checks and where repair defects live — nothing I used.

Files I wrote, all under
`/private/tmp/claude-501/-Users-robertkleffner-Documents-GitHub-tarn-first-draft/r30-round/scratch/writer/`:
`crc32c_writer.py` (CRC-32C, bit-serial, verified against the document's check
vectors), `build_writer.py` (emits `gen1.tarn` and `gen2.tarn`), `gen1.tarn`,
`gen2.tarn`. Plus this transcript at the output path named in the brief.

## 1. Constants I re-derived before trusting anything

All from my own CRC-32C (reflected 0x1EDC6F41, init/xor 0xFFFFFFFF):

| Quantity | Mine | Document |
|---|---|---|
| CRC("123456789") | 0xE3069283 | 0xE3069283 (§4.5) |
| CRC(empty) | 0x00000000 | 0x00000000 (§4.5) |
| CRC of four sentinel entries (80 bytes) | 0x80A34955 | 0x80A34955 (§7.4 example) |
| crc_of_crc_array over that 4-byte array | 0xC4EE982E | 0xC4EE982E (§7.4 example) |
| CRC of 2¹⁶ sentinel entries | 0xEECB3BB2 | 0xEECB3BB2 (§15.4, [R-IDX-05]) |
| Appendix A trailer CRC | 0x402F157E | 0x402F157E |

Arithmetic in the document's examples, re-derived by hand: §7.4 payload 4+34+18+12+13 = 81 ✓,
slot length 4·20+⌈4/2¹⁶⌉·4 = 84 ✓; §11.2 G=(4,8), N=32, P=65,536 ✓; §11.4
(300,700)→t=(1,2), u=(44,188), s=10, in-tile 11,452, planar c=2 → 74, entry bytes
[1480,1500) ✓; §14.2 Q=3, 18 bytes, ordinal 5 at [15,18); planar b 12 bytes, ordinal
5 at 10–11; float32+bool Q=5, 30 bytes, [25,30) ✓; §14.3 `55 01` / `55 FD` ✓; §14.5
32 bytes, 15 padding positions ✓; §15.4 1,000,000 entries → 16 segments (15 full +
16,960), 64-byte array, region 20,000,064, tile 999,999 at segment-relative
20·16,959 = 339,180, segment 15 at [19,660,800, 20,000,000) ✓; §17.3 shuffle
`00 00 00 00 00 00 80 00 40 3F 40 40` ✓; §20.3 example 32·20+4 = 644 ✓; §9.2 note
F+68 → next multiple of 64 = F+128 ✓; §21.9 note 2³² entries → 256 KiB CRC array,
2³⁶ → 4 MiB ✓; §21.1 "[R-CNT-06] states nine": rows F8, F9, F10, F12, F13, F14,
F15, F16, F17 = 9, of which magic and CRC reach = 2, other seven ✓; §4.6
`température` 12/13 bytes ✓; §12.3 12-byte channel entry ✓.

Register counts by `awk` over the table rows (a cell reading `—` counted as one
instance, others split on `;`, per §21.1's stated arithmetic):
F 35 rows / 56 instances; L 49 / 116; T 26 / 55; R 10 / 50; **total 120 rows,
277 instances** — both equal to §21.8's figures and to the per-section counts in
§21.2 (35), §21.3 (49), §21.4 (26), §21.5 (10). F11 is struck, so F1–F36 gives 35 ✓.

## 2. Creation byte layout — `gen1.tarn`, 448 bytes

**Input.** One layer `img`: dimensions `y` (extent 5, tile 4), `x` (extent 5,
tile 4); interleaved; channels `a` uint8 fill 0x00 and `b` uint16 fill 0xABCD;
codec 1, filter 1, no alignment, no slab. Grid 2×2 (§11.2: ⌈5/4⌉ = 2 each),
N = 4, P = 16, Q = 1+2 = 3, decoded size P·Q = 48 (§14.2). I store tiles at
disk ordinals 0 (all real) and 3 (edge tile (1,1): one real position (4,4) and
15 padding positions), and leave ordinals 1 and 2 as sentinels. Plus one
top-level user-metadata record, encoding 1, document `{"tarn.title":"t"}`.

**Emission order I chose** (the document fixes only: front block first, then
structures in any order satisfying §5.2, then directory, pad, trailer —
[R-LIF-02], [R-CNT-05], [R-WRT-02]):

| Range | Bytes | Structure | Who fixed it |
|---|---|---|---|
| [0,16) | 16 | front signature block `89 54 41 52 4E 0D 0A 1A` + 8 zero | document (§6.1) |
| [16,64) | 48 | tile ordinal 0, decoded image verbatim (codec 1) | placement mine ([R-SLB-05]); content fixed (§14.2) |
| [64,112) | 48 | tile ordinal 3; padding positions carry `00` and `CD AB` | content fixed by [R-SER-05] |
| [112,196) | 84 | index region: 4×20 entries + one segment CRC | length fixed by [R-CNT-17]; placement mine |
| [196,218) | 22 | metadata extent: 18 doc bytes + CRC 0xFF5DC00B | placement mine; framing §7.1/§8.1 |
| [218,371) | 153 | directory: layer record (24+100) + metadata record (24+1) + CRC 0x30C2F860 | record order mine ([R-CNT-14]) |
| [371,384) | 13 | pre-trailer pad, zeroed | extent fixed by [R-LIF-02] step 5; content SHOULD ([R-CNT-03]) |
| [384,448) | 64 | trailer, F = 448, file_id 0x0123456789ABCDEF, CRC 0xAC2A06EC | document (§6.2); file_id mine (SHOULD random, §9.3) |

Index entries (offset, length, crc): (16, 48, 0x894E01C2); sentinel; sentinel;
(64, 48, 0x60D33F3C). Segment CRC 0x9EFE0168; crc_of_crc_array 0xE9700EF7.
Layer record inline payload is 100 bytes: name 4 + nine scalars 34 + 2 dimension
entries 36 + channel entries 6+7 + trailing 13. Record flags: layer MU=1,PE=1
(`03 00`), metadata MU=0,PE=1 (`02 00`) — fixed by §7.3/[R-CNT-22].

Decisions the document left to me, and what I did: structure order (tiles, index,
metadata extent, directory), record order in the directory (layer first),
gap content (zeroed), file_id (a constant here; a real writer draws it randomly —
SHOULD), version_minor (0 — SHOULD, [R-CNT-26]), whether to store or sentinel an
all-fill tile (no rule; §13's note), fill defaults (caller-chosen here).
Nothing I needed was missing: every field width, every CRC coverage, every
sentinel byte and every constraint on the padding content was stated.

Coverage check (§9.7): claimants 16+48+48+84+22+153+64 = 435; F − 435 = 13 =
the pad. Live state partitions with no overlap; slack total 13.

A degenerate variant I also worked on paper: a layer with `x` extent 0 →
G = 0, N = 0, entry_count 0, extent slot (0,0), crc_of_crc_array 0 — all fixed
([R-CNT-17], [R-CNT-23], §15.4 example). With codec 4 and P·Q = 2⁴⁰ declared it is
still conforming (the [R-COD-07] note), while P·Q > 2⁶³−1 is L2 even though no
tile is addressed — the note says so explicitly.

## 3. The append procedure — `gen2.tarn`, 832 bytes

**Add layer `msk`**: rank 1, `x` extent 3 tile 3, planar, one bool channel `m`
fill 0x00. N = 1, C = 1, entry_count 1, P = 3, packed plane ⌈3/8⌉ = 1 byte;
values T,F,T → bits 0 and 2 → `05`, pad bits 3–7 = fill bit 0 ([R-SER-03],
[R-SER-05]).

Steps, in the order §20.3 [R-WRT-04] gives them, applied to `gen1.tarn`:

1. Establish F: validate the trailer at physical [384,448) in §6.2's order → F = 448.
2. Open (§19.1): directory CRC verifies, record walk builds the namespace {`img`}.
3. Validate what the commit touches ([R-WRT-03]): the trailer and full directory
   (re-emission relies on every byte); `img` is neither modified nor relied on, so
   its §19.3 validation and index chain are not owed.
4. Write at exactly 448: `msk` tile [448,449); `msk` index region [449,473)
   (entry (448, 1, crc) + one segment CRC).
5. Re-emit the directory: `img`'s record and the metadata record **byte-identical**
   including their extent slots ([R-WRT-05]) — `img` still addresses [112,196) —
   then the new `msk` record (24+75). Directory [473,725), 252 bytes with CRC.
6. Commit: barrier; pad 43 zero bytes [725,768); trailer [768,832) with F = 832,
   same file_id, flags = 0 (no unknown ignore-lane bits to copy), version_minor
   0 = max(floor 0, prior 0); barrier.

832 − 448 = 384 ≥ 128 ✓ ([R-LIF-02]). Claimed bytes: 16+48+48+84+22+1+24+252+64 =
559; slack = 273 = old directory 153 + old pad 13 + old trailer 64 + new pad 43.
A verifier reports 273.

**Durability order and commit point.** Steps 1–3 of [R-LIF-02] (payloads, index,
directory+CRC) must be durable (step 4 barrier) before the pad and trailer are
written (step 5); the trailer must be made durable (step 6). The commit point is
the moment a valid trailer occupies the final 64 bytes of the physical file; a
reader that finds it there takes it as its snapshot (§9.5). The barrier steps
bind conduct, not bytes (§9.2 paragraph after the steps): a file committed
without them can be byte-identical to one committed with them.

### 3a. Appending to a file whose records I do not all understand

Every combination the document defines, walked for a top-level record and for a
layer sub-record of a type my updater does not implement. Authority for the
flags: the stored bits ([R-CNT-15], §20.4 second paragraph).

| Stored flags | Top-level, unknown type | Layer sub-record, unknown type |
|---|---|---|
| MU=1, PE=1 | I am a reader first: [R-CNT-15] → reject-file. **No commit at all.** A compactor refuses ([R-WRT-06] last sentence, §20.4 table). | [R-CNT-18] → reject-layer for that layer; other layers stay editable. I MUST re-emit that layer record byte-identically and MUST NOT modify that layer. A compactor refuses the whole file (§20.4 table: "At either scope"). |
| MU=1, PE=0 | Read as PE=1 ([R-CNT-12]) → identical to the row above. (Verifier records F25.) | Read as PE=1 → identical to the row above. (Verifier records L46.) |
| MU=0, PE=1 | Ignore for reading; retain byte-identical, extent content unmodified. May not relocate (that is §20.5's). | Same, inside the layer record's sub-record sequence, which I re-emit byte-identically within the layer record. |
| MU=0, PE=0 | Retain byte-identical, **or** drop it — only in a commit that independently changes the file's layer set (adding `msk` is such a change), any layer record's content, or another non-layer top-level record. So in this very commit I MAY drop it and SHOULD report the loss. A commit whose only effect is the drop MUST retain it. | Drop only in a commit that independently changes that layer's record, the entry set of its index, or which tiles are stored. Adding `msk` touches `img` not at all, so an `img` sub-record with PE=0 MUST be retained in this commit. |

Reserved-range types (0x0003–0x7FFF) behave for me exactly as unknown types by
their MU bit; their emission is a verifier-detected violation (F36/L25) that I
carry forward — I SHOULD report a violation I carry forward (§20.3 step 2), but
detection of a verifier-row is not owed of me. Experimental-range types are
conforming files (§21.6) and take the same MU handling.

Registered types I implement: the flags come from §7.3, never from the stored
bits. The layer record's stored MU/PE bits are irrelevant to how I treat it; if
they differ from the registry, that is L49, a verifier's row, and I re-emit the
record byte-identically unless I modify the layer. I may modify a top-level
user-metadata record (re-point its slot at a new extent) because implementing a
type confers understanding; I may never drop it (PE=1). No commit removes a
layer record (§20.4 paragraph after the table).

Unknown incompat-lane trailer bit: reject-file before touching anything
([R-CNT-08]). Unknown ignore-lane bits: copied forward, never cleared.

## 4. Slack, per commit shape

- **Append (any of §20.3's three shapes).** Slack gained = the superseded
  directory + its pad + its trailer (always; ≥ 4+0+64 bytes), plus every
  superseded tile payload, plus each re-emitted index region's old copy, plus each
  superseded record extent (editing user metadata is shape (b), not (c)), plus
  the new commit's own alignment/slab gaps and pre-trailer pad. All within [0, F).
  Counted by a verifier whose walk completes ([R-CNT-21]); content unconstrained;
  a reader MUST NOT interpret it. My gen2: 273 bytes as itemised above.
- **In-place update.** Not a shape the format has: [R-LIF-01] freezes [0, F).
  No byte becomes slack because no such commit exists. A writer that overwrites a
  committed byte has produced a different file, not a generation.
- **Rewrite / compaction (§20.5).** The output carries only the live state (less
  records §20.4 lets a compactor drop): its slack is only the gaps its own
  alignment/slab declarations force and its pre-trailer pad. The input persists
  unchanged; its slack is not "reclaimed" in place but abandoned with the input.
- **Shrink** (a commit shape §20.3 permits): the de-addressed tiles' extents become
  slack; the old index region becomes slack; surviving tiles are untouched.
- **Abandoned partial write.** Bytes past F are *not* slack — slack is a property
  of the live state within [0, F). They are residue that [R-LIF-04] obliges the next
  writer to truncate or overwrite; no verifier counts them because, while they are
  the file's tail, the file has no valid trailer at its end and so no F and no
  live state (§5.2: "the verifier reports the trailer failure and nothing about
  slack").

## 5. Torn-write recovery — six crash points on the gen2 append

Physical lengths below refer to my layout (old F = 448; new F = 832).

| Crash | Physical tail | Next reader | Next updater | Conforming meanwhile? |
|---|---|---|---|---|
| C1 during step 2 (after `msk` tile only; length 449) | tile byte | [R-LIF-05]: no valid trailer in the final 64 bytes (the file is 449 bytes; bytes [385,449) start inside trail₁) → report torn; MUST NOT scan back (F8/F14/F17 on the bytes handed over, §9.6) | §9.4: trailer validation fails → MUST NOT append. Recovery (§9.6): probe from the largest 64-aligned o with o+64 ≤ 449 → o = 384: magic ✓ CRC ✓ committed_file_length 448 = o+64 ✓ → candidate → whole-file re-verify [0,448) ✓ → truncate to 448 | No: fails [R-CNT-06] on the bytes handed over |
| C2 mid-directory (length 600) | directory bytes | same | probe 512 (dir₂ bytes, no magic), 448 (tile/index bytes), 384 ✓ → truncate to 448 | No |
| C3 after step-4 barrier, before trailer (length 768: pad written) | zeros | same | probe 704 (dir₂ tail + zeros), … , 384 ✓ | No |
| C4 trailer half-written (length 800) | 32 bytes of trailer | same — the magic is at 768 but 768+64 > 800, so no trailer fits | probe starts at 704 (largest o with o+64 ≤ 800), finds 384 ✓ | No |
| C5 trailer fully written, power lost before step-6 barrier | after restart: either the whole 832 or some prefix | if 832 bytes survive, a complete conforming generation; else one of C1–C4 | either appends normally or recovers as above | Yes if the trailer survived — nothing distinguishes it from a barriered commit |
| C6 writer **omitted** the step-4 barrier; trailer durable, directory bytes lost (say zeroed) | valid trail₂ at [768,832) | §6.2 gates pass, F = 832; directory CRC fails → **reject-file** (F20), never silent | §9.4 succeeds (trailer valid), then §20.3 step 2's open establishes reject-file → every commit barred. Recovery: candidate at 768 passes the three probe tests, fails whole-file re-verification → "was not a commit state", continue → 384 ✓; the tool MUST report the candidate it settled on and that it rejected one | No (F20); the writer violated [R-LIF-02] step 4 — a conduct violation, and the file's nonconformity is F20's, not the barrier's |

The overwrite-instead-of-truncate path ([R-LIF-04]): with residue to 800 and F
re-established at 448, an updater may write from 448 and must truncate to the
new committed length no later than step 6. If the new commit is shorter than the
residue (say it ends at 640) and the crash comes after the trailer at [576,640)
but before the truncation, the physical tail is old residue → torn for readers;
the probe finds o = 576 (magic ✓, CRC ✓, committed_file_length 640 = o+64 ✓),
re-verifies [0,640) ✓ and truncates to 640 — recovering the *new* commit. The
document's rules handled every case I built; none needed a guess.

## 6. Byte-divergence catalogue vs Appendix G

Given identical input arrays and identical stated options (I take "stated
options" to include the declared codec, filter value, tile extents, layout,
fills, names, dimension/channel order and metadata content), two conforming
writers may legitimately differ in:

| # | Degree of freedom | Which rule leaves it open | Appendix G closes it? |
|---|---|---|---|
| 1 | Compressed stream bytes for codecs 2–4 (block choices, deflate final-byte unused bits, zstd FCS presence / single-segment vs window descriptor, window size ≤ decoded size) | RFC 1951/8878/LZ4 constrain decoders; §17.2's note on deflate unused bits | Item 1: pins implementation, version and settings. Closed by pinning, not by rule — and item 1 says so honestly. |
| 2 | file_id | §9.3 SHOULD random | Item 2: derived hash; substitution for zero; creator's rule only. Closed for a creator. |
| 3 | Placement of every structure; gap *extent* | [R-SLB-05], [R-LIF-02] step 2 "any order" | Item 3: total order, contiguous, first structure at 16 (or first admissible position), gaps only where A/A_slab/64-alignment force them. Closed. |
| 4 | Gap *content* (alignment gaps, slab gaps, pre-trailer pad) | [R-CNT-03] SHOULD | Item 3: every gap byte zero, "taken as a requirement here". Closed. |
| 5 | Record order in the directory; sub-record order in a layer record | [R-CNT-14] | Item 3: by type, then by layer name / masked-header key; record placement and record order pinned together. Closed. |
| 6 | Number of generations | §9 nowhere constrains | Item 4: one generation. Closed. |
| 7 | Alignment / slab declarations | §16 MAY | Item 5: none or fixed. Closed. |
| 8 | Filter value | §17.3 writer's choice | Item 5: fixed. Item 5's claim that the filter is the identity "exactly where" s = 1 or n = 1 is **correct**: the map j·s+i → i·n+j is the identity iff j(s−1) = i(n−1) for all i<s, j<n; with s,n ≥ 2 take i=1, j=0 → n = 1, contradiction. Closed. |
| 9 | Tile extents; layout | §11.3 note, §14.1 | Item 5: fixed. Closed. |
| 10 | Store vs sentinel for an all-fill tile | no rule (§13 note) | Item 6: sentinel. Closed; and padding being fill by [R-SER-05], "all samples equal fill" reads the same whether or not one counts padding. |
| 11 | Fill recorded when the caller chooses none | [R-TYP-10] SHOULD | Item 7: zero. Closed. |
| 12 | version_minor; flags | [R-CNT-26] SHOULD; [R-CNT-08] MUST flags = 0 for a creator | Item 8. Closed for a creator; a compactor differs by design (§20.5). |
| 13 | JSON serialization bytes (whitespace, escapes, number formatting); storage encoding; zstd frame parameters for encoding 2 | §18.2 note; [R-MTA-05] pins member order only | Item 9: named JSON writer, fixed encoding, named zstd implementation. Closed by pinning. |
| 14 | Name normalization | [R-ENC-14] SHOULD | Item 10: NFC. Closed. |
| 15 | Which all-sentinel full segments use the constant | [R-IDX-05] MAY | Not a divergence: the constant equals the computed value. |
| 16 | Two byte-identical unknown-type records' relative order | item 3's key does not separate them | Item 3 argues either order yields the same file; I checked: swapping two records identical in masked header, payload and extent content moves neither bytes nor slots' *values* (each slot takes the extent placed in its own position), so the claim holds. |
| 17 | **Order of two layer names / two keys of unequal length** (lexicographic with a proper prefix first, versus length-first) | "ascending layer-name byte order" (item 3); "ascending order of their keys' UTF-8 bytes" ([R-MTA-05]) | **Not stated.** The document defines name/key *equality* as raw bytes (§4.6, §18.2) and nowhere defines the *order* of unequal-length byte strings. See finding writer-01. |
| 18 | Whether tiles with an identical payload share one extent | [R-CNT-13], §15.3: no overlap | Not open: each stored tile has its own extent. |
| 19 | Linearization | only value 1 | Not open. |
| 20 | Pre-trailer pad extent | [R-LIF-02] step 5 pads to the *next* boundary; [R-CNT-05]: a longer gap is conforming but "no conforming commit produces one" | Not open for a conforming writer; item 3 restates it. |

Claims in the reproducible-writer material I tested and could not falsify:
item 1's "byte-identity across implementations is unattainable for codecs 2–4"
(true — the references constrain decoders); item 2's substitution and
"deterministic and high-entropy"; item 3's first-structure-at-16 rule against a
first layer with A = 4096 whose first structure is a tile (goes to 4096, gap
zeroed) versus one whose tiles are all sentinel (index region goes to 16 — A
constrains tiles only, [R-SLB-01]); item 5's "exactly where" (above); item 6's
per-plane reading for planar layers; item 8's compactor caveats against §20.5
(consistent); the closing paragraph's list, which declares itself open ("names
what they are for, not how many there are"). One claim in the closing paragraph
contradicts item 8 — finding writer-02.

## 7. The changed surface, passage by passage

- **Front-matter block.** Labelled *Note* → non-normative by [R-CNF-01]. Its
  content (rubric, structural/descriptive classes) is restated normatively in
  §4.7 [R-ENC-16]; I compared the two: the Note's four-part definition of
  structural matches §4.7's word for word.
- **§2.3 [R-CNF-02].** Two categories of actor-binding rules; the second is
  given as a closed list of two cases. §9.2's barrier steps are declared with the
  second category's defining sentence. See writer-03 (observation; no consequence
  because both categories bind identically).
- **§2.3 [R-CNF-03].** The acceptance-duty exclusion ranges over any unimplemented
  MU = 1 record, sub-records included, while §21.6 confines the file-refusal to the
  top-level case and [R-CNT-18] forbids rejecting the file for a sub-record. Not a
  fork: [R-CNT-18]'s MUST NOT decides the reader's verdict. Rejected candidate.
- **§2.3 [R-CNF-13] and the Note.** F14 reaches, F5 and F15 do not — I re-derived
  the F5 argument (128 = 16 + 4 + 64-alignment) and the F15 one (bytes [48,60) are
  inside the 48 redefinable bytes) — consistent with §21.2's preamble list.
- **§2.4.** Table rows consistent with §19.2 and §20.4; [R-CNF-12]'s "a verifier
  owes no search for one" consistent with Appendix H (which lists no SHOULD hunt).
- **§9.2.** Steps 4 and 6 declared conduct; "the file it produces is not
  nonconforming on that account". Neighbours checked: §20.2 "both barriers, not
  one"; §20.5 "the barriers of steps 4 and 6 — both, not one — are owed here";
  Appendix H writer "including both barriers". All still oblige the barriers.
  Creation path "steps 2–6" is right (step 1 needs a prior F).
- **§9.6.** Probe start "largest 64-aligned o with o + 64 ≤ physical length"
  matches my C4 case (magic present at 768 but excluded). Reporting obligation
  stated. The passage stays coherent with [R-LIF-05].
- **§11.1 Rationale.** Non-normative; it restates §20.3's two bars. Compared
  quantifier by quantifier with §20.3 step 4: tense ("in the generation a commit
  supersedes") ✓, shrink permitted where nothing §14 fixes is altered ✓, growth
  exception ✓, re-typing barred where tiles carrying the channel are stored ✓,
  planar ordinal bar ✓, entry_count-preserving growth touching the directory
  alone ✓ (growth never changes P, offsets or decoded size, and the growth
  exception covers the padding-set change). One generalisation the Rationale
  states more broadly than §20.3 does: "a tile dropped out of the addressed set
  carries no §14 obligation" without §20.3's parenthetical "(§11.2's grid count
  falls)". See the channel-removal candidate in §9 below.
- **§16.2 [R-SLB-03]/[R-SLB-04].** Transparency of sentinels and structural
  entries, non-transparency of crc-failing entries: matches §15.3 [R-IDX-03] and
  L41's parenthetical word for word. [R-SLB-04]'s trigger list covers superseding a
  tile in a packed run ("the byte placement of any run") and a renumbering growth
  ("the disk ordinal of any tile the new state stores"); the clear-the-declaration
  escape always exists, so no commit is left without a conforming path.
- **§18.2.** The writer-facing constraints for encoding 2 are consistent with R4's
  sixteen instances; window unconstrained (SHOULD ≤ 8 MiB); FCS optional but equal
  to decoded length when present; single-segment framing of a >8 MiB document
  correctly routed to [R-ERR-04]. Nothing a writer needs is missing.
- **§19.3.** Adds the user-metadata sub-record framing rules at layer access;
  R1's sub-record instance is at layer access too but not in §19.3's enumeration —
  §19's preamble says the enumerations are not the inventory, the register is.
  Rejected candidate.
- **§20.3.** Walked above. Tense is uniform ("in the generation this commit
  supersedes", 4 hits). Growth exception, shrink test, carve-out, rescue question
  and the planar ordinal bar are each stated once and restated consistently in
  shape (c) and §11.1.
- **§20.5.** Regeneration paragraph: a structural entry met while regenerating
  obliges refusal; a region with no relocated stored extent is copied and the
  compactor "goes looking" no further. Consistent with [R-WRT-09] and with the
  appender's contrary carry-forward rule (different tools, different depths).
  The seven-space row list (L31, L33, L34, L36, L43, L45, R1) matches §10.2's eight
  spaces less record type ✓.
- **§21.1, §21.2, §21.5, §21.6, §21.7, §21.9.** Counts verified (above).
  Specialisation pairs checked: F1⊂F6/F8, F35⊂F36, L24⊂L25, F21⊂F22, L10⊂L11 all
  hold. §21.9's "last three rows"/"first five rows" match the table's eight rows.
- **Appendix G.** Item by item above; writer-01 and writer-02.
- **Appendix H.** Each checklist entry traced to its cited rule; the verifier
  entry's F1/F6 note matches F6's "a verifier holds no such exemption".

## 8. Findings

### writer-01 — AMBIGUITY — §18.2 [R-MTA-05]; §21.2 F27; §21.3 L48; Appendix G item 3

Quotation (§18.2): "Writers MUST serialize object members, at every nesting
depth, in ascending order of their keys' UTF-8 bytes."
Quotation (Appendix G item 3): "For each layer in ascending layer-name byte
order".

The document defines *equality* of names and keys as raw-byte identity (§4.6
[R-ENC-13], §18.2) but nowhere defines the *order* of two byte strings of
unequal length. Two orders are in use in the world: lexicographic (memcmp-style,
a proper prefix sorts first; `"ab"` < `"b"` because 0x61 < 0x62) and
length-first/shortlex (`"b"` < `"ab"`). For F27/L48 the two disagree on a
document such as `{"ab":1,"b":2}`: lexicographic says sorted (conforming),
length-first says unsorted (F27, nonconforming). For Appendix G the same choice
decides the placement of every structure of two layers named `ab` and `b`.

Reading I picked: lexicographic with a proper prefix first — the phrase names an
order "of their bytes", and that is the universal meaning of ordering byte
sequences; Appendix G's own key for other record types says "compared
lexicographically". I grade this **not byte-level**: I do not believe a competent
implementer reads length-first from this text. I record it because the fork,
though improbable, is a verifier *verdict* (F27/L48), because the document's own
standard for pinning such words is high (item 2 disambiguates "low" versus
"last" bytes for exactly this kind of reason), and because the profile inherits
whatever answer §18.2 gets. One clause — "compared lexicographically" or "a
proper prefix orders first" — closes it.

### writer-02 — CONTRADICTION — Appendix G item 8 vs Appendix G closing paragraph (non-normative)

Quotation (item 8): "The version_minor floor binds a compactor too, save where
its output carries a feature it does not implement, when §20.5's floor governs
instead (`[R-WRT-06]`)."
Quotation (closing paragraph): "`version_minor` at its floor, which `[R-CNT-26]`
states as a SHOULD — item 8's creator's rule, not a compactor's (§20.5)".

Item 8 says the floor binds a compactor (with one exception); the closing
paragraph says the floor is a creator's rule and not a compactor's. Both cannot
be true. The shape is the one the brief names — a repair made in one place with a
neighbour left standing: item 8's compactor sentence reads as recently added, and
the closing paragraph's gloss still describes the item before that sentence.
Consequence: none for bytes. Appendix G is non-normative, and the normative
§20.5 [R-WRT-06] ("Otherwise version_minor follows `[R-CNT-26]`'s floor") gives a
compactor the same answer item 8 does. An adopter reading only the closing
paragraph would think a profile compactor is free of the floor; one reading
item 8 would not. Not byte-level. Wording is for human disposition; I do not
propose one.

### writer-03 — OBSERVATION — §2.3 [R-CNF-02] vs §9.2 (paragraph after [R-LIF-02])

Quotation (§2.3): "A writer obligation whose violation this specification
expressly declares not to be a file-conformance violation binds the actor in the
same way; §6.3's flags = 0 against a set ignore-lane bit and §6.2's pre-trailer
gap longer than `[R-LIF-02]` step 5's pad are the cases this text states, and
each is declared where it arises rather than enumerated here."
Quotation (§9.2): "Steps 4 and 6 bind a writer's **conduct** rather than its
output, and are declared so here on the model `[R-CNF-02]` states … A writer
that omits a barrier violates this requirement, and the file it produces is not
nonconforming on that account."

[R-CNF-02] presents the second category as a closed list of two ("are the cases
this text states"). §9.2 declares the barrier steps with that category's defining
sentence — a violation expressly declared not to make the file nonconforming — so
by the document's own definition there are three such cases, unless the barriers
are meant as the first category (pure conduct), which §9.2 also says. The
classification is undecidable from the text; the consequence is nil, because
[R-CNF-02] makes both categories bind the actor "in the same way". Not byte-level.
Shape 5 (closed count) in the freshest text, recorded so the count is checked
rather than assumed.

## 9. Rejected candidates (opened and closed)

1. **Removing the last channel of a planar layer whose tiles are stored.** The
   §14 bar quantifies over tiles stored in the superseded generation; §20.3's
   shrink paragraph exempts "Dropping a tile out of the addressed set (§11.2's
   grid count falls)". Read restrictively the parenthetical would leave channel
   removal barred. Closed by the sentence's stated ground — "a tile the new state
   does not address carries no §14 obligation and its extent becomes slack" — which
   is general, by §11.1's Rationale stating it without the parenthetical, and by
   the planar bar's own example "removing the last, re-indexes nothing and moves
   no ordinal at all", which would be pointless if the operation were barred
   anyway. I judge the restrictive reading not competent. Interleaved removal is
   unambiguously barred (Q and every offset change).
2. **An appender relocating an unchanged index region.** §20.3 step 4 "keeps its
   extent slot … relocating a live index region is compaction's operation, not an
   appender's" carries no keyword. Closed by the document's practice (§21.7 calls
   keyword-less [R-CNT-13] a prohibition) and by the §5.1 example saying the same;
   and any appender can re-store one tile and lawfully re-emit anyway, so no file
   is reachable under one reading only.
3. **[R-CNF-03]'s exclusion over sub-record MU = 1.** Closed by [R-CNT-18]:
   "where the file is otherwise conforming a reader MUST NOT reject the file for
   it".
4. **§19.3 omits R1's sub-record instance.** Closed by §19's preamble: "Those
   enumerations are not the complete inventory … §21's register is."
5. **Partial slack total an "upper bound" when enumerated claimants overlap.**
   Closed by reading "the bytes claimed" as a set (a byte claimed twice is one
   byte) and by [R-CNT-21]'s discard of a rejected layer's claimants.
6. **§14 bar over a tile whose entry is structurally malformed** (stored by §3.1's
   definition, extent-less by [R-IDX-03]). Any file produced either way carries
   the carried-forward T-row, so it is nonconforming under both readings and the
   emittable set does not move.
7. **[R-CNT-03]'s gap list looks closed** ("the run before an aligned tile or
   slab run, and the pre-trailer pad") while scattered placement creates other
   gaps. A SHOULD with no conformance consequence; closed by [R-CNF-12].
8. **Appendix G item 3's "either order yields the same file"** — verified true
   (§6, row 16).
9. **§16.2 "every such run"** in [R-SLB-04] — which runs? Closed by [R-SLB-03]
   binding every run of the layer regardless, and [R-CNF-05].

## 10. Where I found nothing, and what would have found something

Creation: I emitted a real file and re-verified every CRC, every length and the
coverage partition; a missing width, coverage or constant would have shown as an
assertion failure or an unfixed choice. Append: I applied each of [R-WRT-04]'s
six steps to real offsets and checked the ≥ 128 increase and the slack sum. Flag
walk: all four stored-flag combinations at both scopes against §20.4's table and
[R-CNT-12]/[R-CNT-15]/[R-CNT-18]; a combination the table did not decide would
have appeared as an empty cell. Torn writes: six crash points, each run through
[R-LIF-05], [R-LIF-04], and §9.6's probe with the actual 64-aligned offsets. The
divergence catalogue: twenty degrees of freedom enumerated from the rules that
leave them open, each matched to an item or to a rule that closes it; the one
unmatched (row 17) is writer-01. Register: counts recomputed mechanically.
Confidence that the writer/updater path is clean at byte level: high; the two
textual defects I found are non-normative or consequence-free.
