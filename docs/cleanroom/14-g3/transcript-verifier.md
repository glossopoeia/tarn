# Cleanroom round 14 — Verifier implementer — working transcript

## 0. Disclosure and method

I read exactly one file: `/Users/robertkleffner/Documents/GitHub/tarn/spec/tarn.md`,
in full (4,168 lines), in five `Read` calls. I opened no other file in the
repository — no `docs/`, no ADRs, no `PLAN.md`, `AGENTS.md`, `README.md`,
`OPEN-QUESTIONS.md`, no `conformance/`, no `spec/registry.json`. I ran no
`git` command, no web search, no web fetch, and I did not list the repository's
directories.

I ran `grep`/`rg`-equivalent Python over that one file (to extract the §21
register tables mechanically) and a good deal of local Python that reads no
project file: a CRC-32C implementation, a TARN file *builder*, and a TARN
*verifier* written from the document. All of it lives under my own scratchpad.

**One disclosure I owe.** The session scratchpad root is shared with other
agents in this round, and two of my early scratch filenames (`crc.py`,
`build.py`) collided with files another agent had written there. My imports
silently picked up their versions twice, and their `print` output appeared in
my terminal: two CRC hex values, and one hex dump of a §7.4 layer-record
payload with the caption `inline_length 81 expect 81`. That is the document's
own §7.4 example, whose bytes I had already derived independently from the
field table before the collision, and I did not open, read, or list anything in
that directory. On noticing, I moved all my work under a private `v14/`
subdirectory with a `v14_` filename prefix, rebuilt every artifact from
scratch, and re-derived every number below from my own code. I did not read
any other agent's transcript and did not list the round-14 output directory.

My charter is the **verifier** — the tool that certifies a file rather than
reads it. What follows is the actual construction, in the order I did it.

---

## 1. First pass: reproduce every constant the document states

Before trusting anything I wrote, I checked the checksum machinery against the
document's own published values. The document fixes CRC-32C by parameters
(§4.5, `[R-ENC-09]`): Castagnoli polynomial `0x1EDC6F41`, reflected input and
output, init `0xFFFFFFFF`, final XOR `0xFFFFFFFF`, stored little-endian. I
implemented it from those parameters (reflected table driver, reflected
polynomial `0x82F63B78`) and confirmed the reflection independently:
`reflect32(0x1EDC6F41) = 0x82F63B78`.

**Reproduced (7 checksum constants / 1 parameter derivation):**

| Where | Constant | Reproduced |
|---|---|---|
| §4.5 check vector | `CRC-32C("123456789") = 0xE3069283` | yes |
| §4.5 check vector | `CRC-32C(∅) = 0x00000000` | yes |
| §7.4 example | segment CRC over 4 sentinel entries (80 bytes) `= 0x80A34955`, stored `55 49 A3 80` | yes |
| §7.4 example | `crc_of_crc_array = 0xC4EE982E` over that 4-byte array | yes |
| §15.4 / App. B | CRC of a full all-sentinel segment (2¹⁶ entries) `= 0xEECB3BB2` | yes |
| App. A | trailer CRC `0xE00938D2` over trailer bytes [0, 60) | yes |
| App. A | directory CRC `0x00000000` (empty record sequence) | yes |
| §4.5 | reflected polynomial from `0x1EDC6F41` | yes |

**Reproduced (non-checksum worked examples):**

- §12.1 bfloat16: `1.0` → `0x3F80` (high 16 bits of binary32 `0x3F800000`),
  stored `80 3F`.
- §14.2: interleaved `(2,3)`, `a` uint8 + `b` uint16 → `Q = 3`, decoded size 18,
  in-tile ordinal 5 at bytes [15, 18); planar `b` plane 12 bytes, ordinal 5 at
  [10, 12); `t` float32 + `m` bool → `Q = 5`, size 30, ordinal 5 at [25, 30).
- §14.3: planar bool `P = 10`, alternating → `55 01` with fill false, `55 FD`
  with fill true (pad bits 2–7 carrying the fill bit).
- §14.5: extents (5,5), tile extents (4,4), edge tile (1,1) → 1 real position,
  15 padding, 32 decoded bytes for one uint16 channel.
- §11.4: grid (4,8); tile (1,2) → `s = 10`; in-tile (44,188) → ordinal 11,452;
  planar `c = 2` → disk ordinal 74.
- §15.4: `entry_count = 1,000,000` → 16 segments, 64-byte CRC array, region
  20,000,064 bytes; `k = 999,999` in segment 15 at segment-relative byte
  339,180; segment 15 at region bytes [19,660,800, 20,000,000); entry 74 at
  [1,480, 1,500).
- §17.3: shuffle of float32 `1.0, 2.0, 3.0` →
  `00 00 00 00 00 00 80 00 40 3F 40 40`.
- §20.3: 32-tile interleaved index region = `32·20 + 4 = 644`.
- §21.9's Note: 2³² entries → 256 KiB CRC array; 2³⁶ → 4 MiB. §24's claim that a
  2³² -entry vector is not constructible: `2³² · 20 = 80 GiB` of entries.
- §7.4's whole worked layer-record payload: I rebuilt it from the field table
  alone (packing name, the nine scalars, the dimension entry, the channel
  entry, and the three trailing fixed fields) and got **81 bytes byte-identical
  to the document's hex dump**, with the extent length `4·20 + ⌈4/2¹⁶⌉·4 = 84`
  matching `[R-CNT-17]`.

**Could not reproduce locally:** anything defined by an external format —
the LZ4 block-format interoperability bound `0x7E000000` (§17.2, Appendix F
pins the revision), the RFC 1951 / RFC 8878 / LZ4 stream and frame structures,
and RFC 8878's `Window_Descriptor` floor of 1 KiB that §17.2's Note relies on.
I executed no codec. My verifier implements **codec 1 (none) and filter 1/2
only**, so rows T15–T25 are reasoned about below rather than exercised. That is
a limit of my construction, not a finding about the document.

Nothing in the document's stated arithmetic failed. That matters for
calibration: the parts of this document that can be checked mechanically are
clean, so the findings below are all at the level of *what the text obliges*,
never *what the text computes*.

---

## 2. The certification procedure, as an ordered algorithm

I built this from §2.3 (`[R-CNF-11]`), §19.1–§19.4, §9.7 (`[R-LIF-08]`), §5.2,
§8, §15–§17 and the §21 register, cross-checked against Appendix H's verifier
checklist (non-normative; §2.3 is the authority).

### 2.0 Verdict vocabulary and the priority rule

Three verdicts, and three report-level annotations that are **not** verdicts:

- **conforming** — available only to a traversal that established no violation
  *and* was unable to check nothing. §9.7 makes this explicit from the other
  side: "a verifier MUST NOT certify past a violation it has not looked for."
- **nonconforming** — mandatory the moment any violation is established.
  §2.3: "An established violation takes priority: a verifier that has
  established any violation reports *nonconforming*, however many requirements
  it was unable to check."
- **cannot establish** — available *only* where no violation was established
  and at least one requirement is unable to be checked on a capability or
  resource ground.

Annotations, which constrain the report and not the verdict:

- **unexamined** — every scope a first-violation-stop verifier skipped.
  Explicitly "neither a verdict nor *cannot establish*".
- **unable-to-check line** — one per requirement, naming the requirement and
  the ground, reported *whichever verdict* is returned.
- **advisory** — a SHOULD deviation. `[R-CNF-12]`: "a verifier reports a SHOULD
  deviation as an advisory that does not bar certification." §21's register
  "enumerates MUST-level conditions only."
- **slack total** — mandatory (`[R-CNT-21]`), exact or partial. Section 3.
- **ignored-record line** — mandatory for each user-metadata record ignored
  under an unassigned encoding, naming owning scope, encoding value and stored
  extent length (`[R-MTA-10]`).

The five *cannot-establish* grounds §2.3 names ("as when", so illustrative, not
closed):

1. format major the verifier does not implement (`[R-CNT-07]`);
2. a record with MU = 1 of a type it does not implement (§21.6);
3. a codec or filter it cannot execute (`[R-COD-11]`);
4. a layer's or a tile's decode declined on resource grounds, so §14's
   decoded-content obligations go unchecked (`[R-ERR-04]`, `[R-SER-05]`,
   `[R-SER-08]`);
5. a user-metadata document it declines to decode (`[R-MTA-09]`).

Explicitly **not** a ground: a user-metadata document under an encoding this
specification does not assign — "no content rule attaches there, so nothing is
left unchecked, and certification is unaffected" (`[R-MTA-10]`, §21.6). I found
this fully closed: §17.4's closing sentence, §18.2's `[R-MTA-09]` ("The decline
presupposes an encoding this specification assigns"), §21.5's preamble and
§21.6's row all agree, and §21.5's preamble draws the line I would otherwise
have had to guess at: encoding **0 and the reserved range are still violations**
(R1) because "what `[R-MTA-10]` withdraws is the document's content rules,
never the encoding byte's own value set."

Note on ground 3: for a *conforming* verifier it is effectively unreachable.
Every assigned codec and filter is core, so the only way to meet an unexecutable
one is a reserved or experimental value — which is itself L43/L45, hence
*nonconforming* by the priority rule. §17.4 says exactly this. I implemented
the branch anyway; it is dead code in a conforming verifier.

### 2.1 The ordered algorithm

**Phase 1 — file preliminaries.** Input: the byte sequence and the
transport-authoritative size (`[R-CNT-10]`).

1. Size < 128 → **F5**, reject-file. (See finding `verifier-03` for the one
   corner this leaves open.)
2. Front signature block [0, 16) by byte equality. A verifier holds it
   resident by construction, so `[R-CNT-04]`'s deferral licence never applies
   to it — §2.3's "checks every file-level requirement — including those
   ordinary readers are exempted from" is the authority, and F6's own condition
   cell says "a verifier holds no such exemption (§2.3)". Mismatch → **F6**
   (or **F1** where the constant is byte-reversed; §21.1 makes F1 the narrower
   row).
3. Trailer at [F−64, F), in §6.2's **fixed order**, which is load-bearing:
   magic (**F8**/**F1**) → trailer CRC (**F14**) → version gate. §6.2 says only
   these three "touch fields whose positions are fixed across all majors
   (`[R-CNT-24]`)". So a magic or CRC failure is establishable even on a file
   declaring a foreign major; nothing after the version gate is.
4. Version gate: `version_major = 0` → **F18** (permanently invalid in every
   major). Unimplemented major → **cannot establish**, no finding about the
   bytes (§2.3).
5. Flags: any incompat-lane bit → **F19**. Ignore-lane bits set → *not* a
   violation; §2.3 names this as one of exactly two writer-conduct rules whose
   breach never touches file conformance.
6. Remaining field gates (`[R-CNT-06]`): F17, F13, F9, F16, F10, F11, F12, F15,
   F2, F3.
7. Directory region CRC (**F20**), then parse (`[R-CNT-11]`).

**Phase 2 — top-level record walk** (§19.1 step 4). Framing/residue (**F29**),
type 0 (**F24**), reserved-range type (**F36**, and **F35** when MU = 1),
experimental type with MU = 1 and unimplemented → cannot-establish line,
reserved flag bits (**F26**), MU = 1 with PE = 0 (**F25**), registered-type
stored-flag mismatch (**F28**), multiplicity (**F34**), extent slot
(**F30/F31/F32**), user-metadata framing (**F21/F22/F23**), and the layer-name
namespace (**F4**). §19.1 step 4 settles two things I would otherwise have
guessed at: uniqueness is decided **first**, over raw bytes, "whether or not
each name is itself well-formed"; and a layer record whose name field does not
fit inside its `inline_length` "contributes no name to the namespace" and is
instead layer scope.

**Phase 3 — per layer** (§19.3, `[R-RDR-03]`), all decidable from the resident
directory and F, with no fetch: L1–L9, L10–L17, L19–L23, L26–L36, L39, L43–L45.

**Phase 4 — per layer index.** Fetch the region; `crc_of_crc_array` (**L37**),
then each segment CRC (**L38**) — §15.4's dependency order. Then classify every
entry per §15.3 (**T6–T12**), then codec-1 length equality (**T14**), which
§17.2 notes is "checkable from the entry and the layer record alone, before any
payload fetch."

**Phase 5 — per stored tile.** Fetch, verify the entry crc (**T1**), decode
(**T17–T25**, **T3**), then the decoded-content obligations (**T2**, **T4**,
**T5**; T26 is recorded by T2/T4).

**Phase 6 — whole-file structural.** Pre-trailer gap (**F7**), overlap
(**F33**, **L18**), alignment (**L40**), slab (**L41**, **L42**), and the
coverage partition and slack total.

**Phase 7 — record extents.** Terminal CRC (**R2**), encoding value (**R1**),
decode (**R3**), frame constraints (**R4**), document rules (**R5–R10**),
member ordering (**F27**, **L48**).

**Phase 8 — verdict**, by the priority rule.

I implemented Phases 1–6 and the structural half of 7 in ~330 lines of Python
and ran it against everything below.

---

## 3. The coverage walk

### 3.1 The partition, and whether a byte can be neither

`[R-CNT-02]` puts every byte of the live committed state in exactly one class:
the front block, or a structure (a stored-tile extent, a record extent "whatever
the record's type", the directory, the trailer). `[R-CNT-21]` makes every other
byte slack.

So the answer to "can a byte be neither?" is **no**, and the document says why
in §5.2's Note: the live state "is *defined* as the front block plus what a
complete coverage walk reaches, and `[R-LIF-08]` makes every byte that walk
misses slack — so 'belongs to no class' describes nothing, and a register row
for it would be a row no file could exhibit." That is why §21.2 has an overlap
row (F33) and no coverage-hole row. I checked that the register really does
lack one, and it does.

Two claimant questions §9.7 settles that I would otherwise have had to guess:

- a **record is not a claimant of its own header and inline payload** — those
  lie inside the directory region, "so reaching a record through the directory
  is traversal, not a second claim on those bytes";
- a **layer record's extent slot addresses the tile-index region**, so the
  region "enters the walk once, as that record's extent, and is not a second
  claimant beside it."

Both matter arithmetically: without the first, every file double-counts its
directory; without the second, every layer double-counts its index.

Certified bytes = the claimants. Counted-but-unconstrained = slack, whose
"content is unconstrained, and no conformance requirement applies to it."
Two claimant classes are *certified but uninspected*: the front block (checked
by equality, covered by no checksum) and the extent of a record of an
unassigned type (§8.1's last row, "none — the bytes are opaque"). §22.3 names
the second as a stated residue, which is why `[R-MTA-10]`'s report line exists
for its user-metadata cousin.

### 3.2 A concrete file, built and walked

I built a real file rather than describing one. **Layer `a`**: interleaved,
rank 1, dim `x` E = 8 T = 4 → `G = 2`, `N = 2`, `P = 4`; one uint8 channel `v`,
fill `0x00`; codec 1, filter 1, no alignment, no slab. Decoded size `P·Q = 4`,
so under codec 1 every stored length is 4 (`[R-COD-04]`). `entry_count = 2`,
index region `2·20 + ⌈2/2¹⁶⌉·4 = 44` bytes. Layer-record inline payload 73
bytes; record 97; directory 101.

Generation 1 layout, all offsets computed by the builder:

```
[0,16)     front signature block            16
[16,20)    stored tile 0 of layer 'a'        4
[20,24)    stored tile 1 of layer 'a'        4
[24,68)    tile-index region of layer 'a'   44
[68,169)   directory region                101
[169,192)  pre-trailer pad                  23   <- slack
[192,256)  live trailer                     64
```

`F = 256`, a multiple of 64; `dir_offset + dir_length = 169 ≤ F − 64 = 192`.
Claimed = 16 + 4 + 4 + 44 + 101 + 64 = **233**. Slack = 256 − 233 = **23**, and
23 is exactly the pre-trailer pad. My verifier returns `conforming`, slack 23,
exact.

I ran the same walk on the document's **Appendix A** file, transcribed from its
hex dump: claimants front 16 + directory 4 + trailer 64 = 84, F = 128,
slack = **44** — precisely §5.1's "44 bytes of slack, zeroed by advice."
Verdict `conforming`. That the document's own smallest file and my
independently-built file both partition exactly is the strongest evidence I have
that §5.2/§9.7 are implementable as written.

I also walked a **zero-extent layer** (E = 0 → `G = 0`, `N = 0`, addressed
tiles 0, `entry_count = 0`, extent slot (0,0), `crc_of_crc_array = 0`):
`conforming`, no index claimant, slack = the pad. §17.2's Note settles the one
thing that could have gone wrong here — the codec-4 cap is quantified over
*addressed* tiles and so is vacuous, while "`[R-ENC-04]`'s overflow rule carries
no such quantifier … so P·Q and P·Bᶜ are checked in an empty layer even though
this cap is not." I implemented it that way.

### 3.3 A walk that does not complete

I rebuilt generation 3 with layer `b` carrying two channels named `p` (an
`[R-ENC-15]` duplicate → **L9**, reject-layer) and everything else untouched.

`[R-CNT-21]`: "a scope-level rejection ends that scope's enumeration (a rejected
layer's claimants are not enumerated, whether or not the rejection impeded
reading them)". Layer `b`'s claimants are its four stored extents (4+4+1+1 = 10)
and its 84-byte index region = 94 bytes. So:

```
intact G3:   F = 960, claimed = 430, slack = 530   (exact)
b rejected:  F = 960, claimed = 336, slack = 624   (PARTIAL, stopped by layer 'b')
```

624 ≥ 530 — an upper bound, "never an under-count", as `[R-CNT-21]` requires,
and the verifier names the scope that stopped the walk. The clause "whether or
not the rejection impeded reading them" is doing real work here: `b`'s index
region is perfectly readable, and the rule still drops it.

That worked. Pushing on it is where I found something (§8, finding
`verifier-02`).

---

## 4. Extent overlap, alignment and slab, on adversarial layouts

I built each of these as a real file and ran the verifier.

### 4.1 Overlap

`[R-CNT-13]` gives three outcomes, and I checked they partition the cases
exhaustively: intra-layer → reject-layer; across layers or touching another
scope's structures → reject-file; two structures neither of which belongs to a
layer → reject-file. Enumerating the structure kinds (front, trailer,
directory, layer-owned tiles/index/sub-record extents, non-layer top-level
extents), every pair falls in exactly one. F33's condition cell restates the
last two, and adds the boundary carve-out I would otherwise have had to
reason out myself: "a claimant reaching the front signature block or the live
trailer is instead caught by the bounds rows F9/F10, F31/F32, L16/L17 and
T8/T9, each at its own tier."

| Adversarial layout | Verifier |
|---|---|
| layer `a`'s tile 1 declared at 60, inside `a`'s own index region [24,68) | **L18** reject-layer (+ T1) |
| layer `a`'s tile 1 at 212, inside layer `b`'s index region [208,232) | **F33** reject-file |
| layer `a`'s tile 1 at 100, inside the directory region [68,169) | **F33** reject-file |
| layer `a`'s tile 1 at 180, inside the pre-trailer gap [169,192) | **F7** reject-file |

The third case is the one the register's phrase "a layer structure against
another scope's structure" covers, and it does. The fourth is `[R-CNT-05]`'s
verifier obligation; note it is *not* caught by §9.7's `[16, F−64)` bound, since
the gap lies inside that interval — F7 is the only thing that catches it.

### 4.2 Alignment

Layer with `A = 512`, tiles at 512 and 1028 → **L40**, reject-layer, and the
slack total goes partial. A question §16.1 does not answer directly: are
entries §15.3 classifies reject-tile on a *structural* ground transparent to the
alignment invariant, as §16.2 says they are to run continuity? §15.3 answers it
generally — such an entry "contributes no stored extent to the *verifier* rows,
which bind over well-formed entries' extents only" — and §15.3's table makes
"alignment or slab invariant violated (§16)" one of those verifier rows. So
yes, and the `[R-SLB-03]` parenthetical is an example rather than the rule. I
implemented it that way and confirmed the third structural row (offset < 16)
drops the entry from both L40 and the coverage walk.

### 4.3 Slab

Planar layer, `C = 2` uint8 channels, dim E = 12 T = 4 → `G = 3`, `N = 3`,
addressed 6, `P = 4`, decoded size 4. `S = 2`, `A_slab = 512`.

`[R-SLB-02]` partitions by **channel block**, not across the whole ordinal
space: blocks [0,3) and [3,6); runs [0,2), [2,3) | [3,5), [5,6). Each block's
final run covers fewer than S ordinals, as the rule allows.

| Layout | Verifier |
|---|---|
| 0@512, 1@516, 2@1024, 3 = sentinel, 4@1536, 5@2048 | **conforming** |
| tile 1 at 517 | **L41** (gap inside run [0,2)) |
| tile 2 at 1020 | **L42** (run [2,3) first stored tile not 512-aligned) |
| tiles 2@1024 and 3@1028 packed — a writer treating [2,4) as one run | **L42** on run [3,5) |
| tile 3 sentinel, tile 4@1540 | **L42** — the constraint is on the first **stored** tile |

The fourth row is the discriminating case for "runs never span channel blocks",
and the document decides it cleanly. The fifth is §16.2's example
("If ordinal 10 is a sentinel, run 1's stored tiles are 8, 9, 11…15") and it
matches.

**§16.2's transparency rules — the sharp test.** §16.2 says sentinels and
structurally-rejected entries are transparent to run continuity, while "An entry
whose only defect is that its stored bytes fail its crc is not transparent — its
offset and length stand, and the packing relation reads them as it does any
other stored tile's — so this invariant stays decidable from index bytes alone."
I built the three files that separate these, with `S = 3` so one run covers
tiles 0, 1, 2:

| File | Verifier |
|---|---|
| 0@512, 1@516, 2@520 packed; **tile 1's stored bytes corrupted** | **T1 only** — packing still reads entry 1's offset/length and holds |
| 0@512, 1 = length 0 (**structural**), 2@516 | **T10 only** — the run closes over entry 1, and packing 0→2 holds |
| 0@512, 1 = length 0, 2@520 | **T10 + L41** — the run does *not* close over the byte gap |

That is exactly the behaviour §16.2 describes, and the claim that follows from
it — decidable from index bytes alone, with no payload fetch — is true: none of
the three needed a tile read to settle the packing. This repair is sound, and
its twin in §15.3 covers the alignment and overlap rows as well.

---

## 5. Checksum obligations — is every live structure covered?

I enumerated the live-state structure kinds against §8.1's map:

| Live structure | Covering checksum | Verified how |
|---|---|---|
| front signature block | **none** | byte equality (§6.1) |
| trailer | trailer [60,64) over [0,60) | comparison; covered by nothing further |
| directory region | final 4 bytes over `dir_length − 4` | comparison; covered by nothing further |
| tile-index region — entry array | per-segment CRC array | comparison |
| tile-index region — segment CRC array | layer record's `crc_of_crc_array` | comparison; and the array is itself comparison-verified |
| stored tile | its index entry's `crc` field | comparison |
| user-metadata extent | final 4 bytes over the preceding bytes, "exactly as stored, before decoding" | comparison |
| extent of an unassigned-type record | **none** — opaque | not verified |

So: **every live structure is covered by exactly one checksum except two, both
of which the document names explicitly** — the front block (§4.5, checked by
equality) and an unassigned-type record's extent (§8.1's last row, §22.3's
second stated residue). Every *field* is covered exactly once, which is the
form §4.5 and `[R-CNT-19]` actually assert: the entry `crc` field is covered by
its segment CRC, the segment CRC array by `crc_of_crc_array`, and
`crc_of_crc_array` by the directory CRC, because it lives in the layer record's
inline payload inside the directory region. I traced that chain on my built
file and it closes.

The three "interior" checksum fields §4.5 names (segment CRC arrays, entry
`crc` fields, `crc_of_crc_array`) are each both comparison-verified and covered
by one further checksum; the three "terminal" ones (trailer, directory,
user-metadata) are comparison-verified and covered by nothing. I found no
fourth terminal checksum and no uncovered field.

One phrasing wobble, not a defect: §9.7 says the walk checks "that each
verifies against the checksum covering it" (singular), but the tile-index
region as a *claimant* is covered by two — segment CRCs for the entries,
`crc_of_crc_array` for the array. §8.1's map resolves it per field, and §15.4
gives the dependency order, so a verifier is never in doubt about what to do;
only the singular is loose.

---

## 6. Decoded-content obligations

**What must be decoded.** Every stored tile, without exception: §9.7 says "A
verifier decodes every stored tile, whatever content obligations §14 places on
the layer: §21.4's codec rows are file-conformance violations, and a verifier
MUST NOT certify past a violation it has not looked for." So there is no layer
shape that lets a verifier skip decode — not a layer with no bool channel and
no padding position, because T3/T17–T25 still apply, and not a codec-1 layer,
because T1 still requires fetching and checksumming the bytes.

**What it must compare against:**

- decoded length **exactly** the declaration-derived decoded size — `P·Q`
  interleaved, `P·Bᶜ` planar numeric, `⌈P/8⌉` packed planar bool
  (`[R-SER-07]`, T3); never a size read from the payload (`[R-COD-06]` bars
  allocating from the zstd content-size field);
- every padding position, per channel it carries, against that channel's
  recorded fill — fill bytes for numeric, the fill byte for interleaved bool,
  the fill bit in a packed plane (`[R-SER-05]`, T4);
- every pad bit of a packed plane with `P mod 8 ≠ 0` against the fill bit (T5);
- every interleaved bool byte at a **real** position ∈ {0x00, 0x01}
  (`[R-SER-08]`, T2);
- the codec's own header/frame constraints (T17–T22) and exact consumption
  (T24, T25).

T2's condition cell carries the partition I would otherwise have had to invent:
"the same byte at a padding position is T4's, the two rows together covering
`[R-SER-08]`." So a padding bool byte of `0x02` against fill `0x00` is recorded
as T4, not T2. It is still a violation either way, so the verdict does not turn
on it.

I implemented T2/T4/T5 over a planar bool plane with both padding positions and
pad bits (layer `b` below: E = 5, T = 4, so ordinal 3's positions y = 5,6,7 are
padding *and* bits 4–7 are pad bits) and confirmed the two mechanisms are
distinguishable and never conflict — both demand the same fill bit, so §14.3's
Note ("Pad bits are not padding positions") is a clarification rather than a
choice.

**What it is permitted to skip.** Sample values at real, non-bool positions:
nothing constrains them, and §21.7 says so in terms — "this format detects
*corruption of structure*, not *incorrectness of content*", and none of these
"is a requirement a verifier is *unable to check* within the meaning of
`[R-CNF-11]`: no file-level witness exists to check, so nothing about the file
is left undetermined and the verdict is unaffected." That sentence is what
keeps a wrong-data file at *conforming* rather than *cannot establish*, and it
is the single most load-bearing sentence in §21.7 for a verifier. Likewise a
mis-strided filter where no structural constraint catches it (T26's own
parenthetical), an undisclosed zstd dictionary (`[R-COD-06]`), and SHOULD
deviations.

**What it may decline.** A tile's or a layer's decode on resource grounds
(`[R-ERR-04]`) → cannot establish, reported per requirement. A user-metadata
document above its own bound, which must be no smaller than §21.9's 16 MiB
(`[R-MTA-09]`) → cannot establish, and the verifier "SHOULD report the bound it
applied and the stored length of the extent it declined." I note that the same
conforming file can therefore be *conforming* to a verifier with a 32 MiB bound
and *cannot establish* to one at 16 MiB. That is intended — `[R-MTA-09]` says
"the bound is that verifier's capability and not a limit on validity
(`[R-CNF-10]`)" — so it is not a defect, but it is worth an implementer's
attention because it means the verdict is not purely a function of the bytes.

---

## 7. The multi-generation trace

Four states, all built and verified by the same program. Layer `a` as in §3.2.
**Layer `b`**: planar, rank 1, dim `y` E = 5 T = 4 → `G = 2`, `N = 2`, `P = 4`;
channels `p` uint8 (fill `0x00`) and `q` bool (fill `0x00`); addressed tiles
`C·N = 4`, disk ordinals channel-major (`[R-GEO-06]`): 0,1 = `p`, 2,3 = `q`.
Decoded sizes 4, 4, 1, 1 — the planar bool planes pack to `⌈4/8⌉ = 1` byte
(§14.3). Tile 1 of `p` covers y = 4..7: y = 4 real, y = 5,6,7 padding, so its
bytes are `09 00 00 00` with the three fill bytes `[R-SER-05]` fixes. Tile 3 of
`q` is the byte `0x01`: bit 0 = the real value at y = 4, bits 1–3 the padding
positions carrying the fill bit, bits 4–7 the pad bits carrying it too.

| Step | Operation | F | claimed | slack | verdict |
|---|---|---|---|---|---|
| G1 | **create** layer `a`, 2 tiles, generation 1 | 256 | 233 | **23** | conforming |
| G2 | **append**: add layer `b` — `a` untouched, its record carried forward byte-identically with its extent slot unchanged (`[R-WRT-05]`) | 640 | 430 | **210** | conforming |
| G3 | **update**: supersede `a`'s tile 1; `a`'s whole index region re-emitted at a new placement, entry 0 byte-identical (`[R-WRT-04]`) | 960 | 430 | **530** | conforming |
| G4 | **compact**: fresh `file_id`, generation 1, live structures only | 448 | 430 | **18** | conforming |

Each slack figure decomposes exactly:

- G2's 210 = G1's directory 101 + G1's pad 23 + G1's trailer 64 + G2's pad 22.
- G3's 530 = 188 (G1's dir+pad+trailer) + 290 (G2's) + 4 (`a`'s superseded
  tile 1) + 44 (`a`'s superseded index region) + 4 (G3's pad). This is §20.3's
  Note made concrete: a one-tile edit costs the whole index region, and the
  index dominates.
- G4's 18 = the pre-trailer pad alone. Compaction reclaimed 530 − 18 = **512**
  bytes, and the claimed total is unchanged at 430 across G3 and G4, which is
  `[R-WRT-07]`'s "compaction changes where bytes live, never what a layer
  denotes" as an arithmetic identity.

`[R-WRT-07]`'s regeneration rule checks out on the compacted output: entry
offsets are new, entry lengths and crcs are unchanged, sentinels unchanged,
segment CRCs recomputed, and each layer record's `crc_of_crc_array` updated —
which in turn changes the layer records, hence the directory, hence the trailer.
I confirmed the reference arrays are bit-identical by decoding both G3 and G4
and comparing every stored tile's decoded image.

My compacted layout also happens to satisfy Appendix G item 3's total emission
order (layers in ascending name byte order, each layer's tiles in disk-ordinal
order then its index region, then the directory, with every gap zeroed), which
is a useful cross-check that the non-normative profile is actually achievable
under §5.2's placement rules. `file_id` I drew fresh rather than deriving, as
Appendix G item 2 requires of a compactor: "a compactor adopting the profile
takes `[R-WRT-06]`'s fresh draw instead, since a derived value is not a draw."

I then re-ran G3 with a defect in layer `b` — see §3.3 — to get the
incomplete-walk figure of 624.

---

## 8. Findings

Three. All are report-level or corpus-level; **none is byte-level**, and §8.4
explains why I am confident that is a real result rather than a default.

---

### verifier-01 — CONTRADICTION — §21.1's instance axes are not applied to F17, L21, L22 and L30

**Location:** §21.1 (instance arithmetic); §21.2 row F17; §21.3 rows L21, L22,
L30. Requirements: `[R-ERR-02]`, `[R-VEC-03]`.

**Quotation.** §21.1 states the axis rule unconditionally:

> Two axes recur often enough to be stated rather than judged each time. Where
> the quantity a condition derives varies by layout, the layout formulas are
> materially different shapes and the cell enumerates them. Where the condition
> compares two quantities and either can be the greater — a *differs from* or
> *does not equal* — the two directions are likewise enumerated; where its own
> text bounds the comparison in one direction — an *exceeds*, a *larger than* —
> there is one.

Four rows do not follow it. The clearest is L21, which is short under **either**
reading of the axis rule, because it applies the layout axis and not the
direction axis:

> | L21 | entry_count does not equal the geometry-derived addressed-tile count (N interleaved, C·N planar) | interleaved N; planar C·N | reader | layer access | `[R-CNT-17]` (R-CNT-20) |

Two instances, where "does not equal" × two layout formulas gives four. The
other three:

> | L30 | A channel entry's fill length prefix differs from the element size of the channel's declared type | — | reader | layer access | `[R-CNT-23]` (R-TYP-06) |

> | F17 | Trailer committed_file_length does not equal the transport-authoritative file size (physical file not truncated or extended to it) | committed_file_length | reader | open | `[R-CNT-06]` (R-LIF-04, R-CNT-10) |

> | L22 | Under index_encoding 1, extent_length ≠ entry_count × 20 + ⌈entry_count/2¹⁶⌉ × 4 — including slot (0,0) with entry_count > 0, or a nonzero slot with entry_count = 0 | extent_length against the formula; slot (0,0) with entry_count > 0; a nonzero slot with entry_count = 0 | reader | layer access | `[R-CNT-17]` (R-ENC-07, R-CNT-20) |

**Detail.** The contrast is with the tile-scope rows, which do apply the axis:
T3 ("is not exactly") → *payload longer* / *payload shorter* × three layouts =
6; T14 ("differs from") → *length longer* / *length shorter* × 3 = 6; T22
("does not equal") → *declared larger* / *declared smaller* × 3 = 6. And the
one-direction half of the axis is applied correctly too: T21 ("larger than")
and L44 ("exceeds") each get 3, one per layout formula. So the axis rule is
live and is being used — just not in §21.2 and §21.3.

The permitted readings are: (a) the direction axis is unconditional, in which
case F17, L21, L22 and L30 are all short; (b) the direction axis only multiplies
the layout axis, in which case L21 is still short. I take (a), because the
sentence conditions the direction axis on nothing but "either can be the
greater", and because each of the four really does name two distinguishable
files. L30 is the sharpest: a fill length prefix *shorter* than the element size
and one *longer* are not near-duplicates — the prefix determines where the next
field begins (§4.7: "A variable-length field's value includes its length prefix,
so a name is structural: it determines where the field after it begins"), so the
two directions shift the remainder of the inline payload in opposite directions
and typically produce different secondary rows. F17's own condition text names
both directions — "physical file not truncated **or** extended to it" — and
§21.1's primary criterion already counts "one of several alternatives the
condition text states" as an instance, so F17 is short even before the axis
rule is reached. The two F17 directions are also the two distinct real-world
states the document discusses separately: a truncated file is §9.4's torn
commit, an extended one is §9.5's Note on residue past a completed commit.

**What an implementer does wrong without it.** Nothing, as an implementer of a
reader, writer or verifier — which is why this is not byte-level. What goes
wrong is the corpus: §21.8 asserts "121 conditions over 268 instances" and
`[R-VEC-03]` obliges "at least one vector for each instance it names". I
extracted all four register tables mechanically and counted cells by
semicolon-separated members: 121 rows, 268 instances — the stated total is
internally consistent with the cells as written. Applying the axis rule adds
1 (F17) + 2 (L21) + 1 (L22) + 1 (L30) = **5**, taking the corpus to 273 files
and §21.8's figure to 273. The five missing vectors are exactly the ones that
would catch an implementation that handles `entry_count` too large but not too
small, or a fill prefix too long but not too short.

**Byte-level: no.** §21.1 already fixes which text governs when a row and its
rule diverge, and the Instances column governs nothing an implementation does —
it is the corpus build list. No emitted byte and no accept/reject verdict
changes on the resolution; only the number of vectors built.

---

### verifier-02 — AMBIGUITY — the mandatory slack total is undetermined when the layer that is rejected is rejected *by* the coverage walk

**Location:** §5.2 `[R-CNT-21]`; §9.7 `[R-LIF-08]`; §21.3 rows L18, L40, L41,
L42, L48; §2.4.

**Quotation.** §5.2:

> Where the walk of §9.7 does not enumerate every region's claimants — whether
> because a scope-level rejection ends that scope's enumeration (a rejected
> layer's claimants are not enumerated, whether or not the rejection impeded
> reading them), or because the verifier elected under `[R-CNF-11]` to stop at
> the first violation — the verifier MUST report the total as partial. A partial
> total is F less the bytes claimed by the claimants the walk did enumerate — an
> upper bound on the file's true slack, never an under-count — and a verifier
> reporting one MUST say which scope or violation stopped the walk.

**Detail.** For a layer rejected on a ground the verifier reaches *before* the
walk — a bad value set, a duplicate channel name, a failed segment CRC — this
is unambiguous and I implemented it: drop the layer's claimants, report partial,
name the layer. My G3 file gives 624 against a true 530, an upper bound as
required.

The ambiguity is the class of reject-**layer** rows whose *detector is the
verifier and whose detection is the walk itself*: L18 (intra-layer overlap),
L40 (alignment), L41 and L42 (slab), and L48 (member ordering, detected at
extent use, after the walk). To detect any of them the verifier must already
have enumerated that layer's claimants. §5.2 then says a rejected layer's
claimants are not enumerated. The rule that produces the finding is contradicted
by the finding.

Three behaviours are defensible on the text, and I built a file that separates
them: layer `a`, two stored tiles, the second declared at offset 60 which lies
inside `a`'s own index region [24, 68) — an L18 and nothing else structurally
novel. Claimants: `[0,16)`, `[16,20)`, `[24,68)`, `[60,64)`, `[68,169)`,
`[192,256)`; F = 256.

| Behaviour | Reported total |
|---|---|
| keep the layer, sum claimant lengths: F − 233 | **23**, marked exact |
| keep the layer, take the union of claimants: F − 229 | **27**, marked exact |
| drop the rejected layer: F − (16 + 101 + 64) | **75**, marked partial |

The first is **refuted** by the text, and that is worth stating because it is
the natural implementation: with an overlap present, summing claimant lengths
double-counts the overlapping bytes, so F − Σ *under-counts* the true unclaimed
byte count (23 against 27), and `[R-CNT-21]` says a partial total is "never an
under-count". So a verifier must compute the total over the *union* of
claimants, not the sum. I had written the sum, and only found this by
constructing the overlap case; the document does determine it, but only by
chaining "never an under-count" back onto the formula.

The second and third both satisfy every stated property, and the document does
not choose between them. Reading A: the gating condition is "Where the walk …
does not enumerate every region's claimants" — the walk *did* enumerate them
(it had to), so no partial arises, and the total is the exact 27. Reading B:
"a rejected layer's claimants are not enumerated" is categorical, and the
qualifier "whether or not the rejection impeded reading them" was written
precisely to defeat the objection that the layer was readable — so drop them and
report 75, partial.

**I picked B**, because the qualifier only has work to do under B, and because
§22.3 gives the partial marking its purpose: "a verifier that stopped early
reports it only as partial (`[R-CNT-21]`), so the distinguishing figure comes
from a walk that completes." A total computed across a layer whose structures
are known to overlap is not a figure an operator should act on. But B has a real
cost the document does not acknowledge: for a 256-byte file whose only defect is
a four-byte overlap, the mandatory slack line goes from 27 to 75, and the number
§22.3 calls "the number that distinguishes a working file from a padded one"
becomes nearly useless on exactly the files an operator most wants it for.

A smaller sibling of the same gap: when the walk enumerates **no** claimant at
all — the trailer CRC fails (F14), so `committed_file_length` is not a value the
verifier may act on (`[R-ENC-05]`) — `[R-CNT-21]`'s "F less the bytes claimed"
has no F to work with. The obligation to report a total is unconditional; the
formula is not evaluable. I read §5.2's framing ("Coverage is a property of the
live committed state") as meaning the obligation does not attach where no live
state has been established, and reported the violation with every scope marked
*unexamined* and no total. A verifier substituting the physical size would
report `F_phys − 16` instead. The same file, two different mandatory report
lines.

**What an implementer does wrong without it.** Two conforming verifiers print
different mandatory numbers for the same bytes — 27/exact against 75/partial —
and a third prints 23, which the text forbids. Since `[R-CNT-21]`'s total is a
MUST on the verifier's report, they cannot both be conforming verifiers, but the
text does not say which is not.

**Byte-level: no.** Both readings report *nonconforming* for the file above, and
neither changes which bytes a writer may emit. The divergence is confined to a
mandatory report field. I considered whether dropping a rejected layer's
claimants could suppress a violation another verifier would find — it can (an
overlap between a rejected layer's tile and another layer's tile goes undetected
under B) — but the file is already established nonconforming by the rejection
that caused the drop, so no verdict changes.

---

### verifier-03 — OBSERVATION — whether §21's rows apply at all to a file declaring a format major the verifier does not implement

**Location:** §2.3 `[R-CNF-02]`; §5.1 `[R-CNT-27]`; §6.2 `[R-CNT-06]`; §21.2
rows F5, F13, F9, F10, F16; §19.1 step 1.

**Quotation.** §5.1 states the 128-byte floor with no version qualifier and with
a flat reader MUST:

> No conforming file is shorter than 128 bytes: the front signature block, a
> directory of at least 4 bytes at an offset of at least 16, and the 64-byte
> trailer at a 64-aligned offset cannot be satisfied in fewer. A reader MUST
> treat a shorter file as a validity error at file scope. `[R-CNT-27]`

§2.3 states the opposite conclusion for a foreign-major file, categorically:

> It is always conformance to a stated format major version. This document
> defines format major 1, and a file declaring another major is neither
> conforming nor nonconforming under it: a reader refuses such a file on
> capability grounds (§6.3, `[R-CNT-07]`), and that refusal is not a finding
> about its bytes.

**Detail.** Consider a 96-byte file whose final 64 bytes carry a valid trailer
magic and a verifying trailer CRC, with `version_major = 2`. §6.2's ordered
validation is explicit that only three checks precede the version gate — "the
trailer magic; the trailer CRC; the version gate (§6.3) — only these touch
fields whose positions are fixed across all majors (`[R-CNT-24]`)" — and
`[R-CNT-27]` is not among them, nor does §19.1 place it relative to them; step 1
merely obtains F.

Two readings. (a) `[R-CNT-27]`'s MUST is unqualified and F5's detector is
*reader* at *open*, so F5 fires and the verdict is **nonconforming**. (b) §2.3
bars any finding about a foreign-major file's bytes, so the verdict is **cannot
establish**, and F5 — like every other row in §21.2 that depends on major-1
trailer semantics (F9, F10, F13, F16) — simply does not apply.

I picked (b). §2.3's sentence is categorical and directly on point, and §21.1
scopes the register to "file-conformance violations", a status §2.3 says a
foreign-major file does not have. What makes this expensive rather than open is
that nothing in §5.1, §19.1 or §21.2 points at §2.3: the register presents F5,
F9, F10, F13 and F16 as flat conditions, and the only rows that flag their
cross-major standing flag it in the *other* direction — F18 ("a permanently
invalid major in every format major version"), and F1/F6 on the front block,
which §6.1 does make constant in every major. An implementer working from
§19.1's step order and `[R-CNT-27]`'s flat MUST will get (a), and will report a
possibly-perfect major-2 file as nonconforming — the exact outcome §6.3's
diagnostic advice ("a reader that reports an unimplemented major as corruption
misleads users into discarding files that current software reads") exists to
prevent.

The scenario is not contrived: `[R-CNT-24]` fixes only the trailer's size and
the position of its magic, version fields and CRC across majors, and §6.2's
64-alignment requirement is a major-1 statement, so a 96-byte major-2 file is
exactly the sort of thing a future major could define.

**What an implementer does wrong without it.** It reports *nonconforming* where
the document requires *cannot establish*, on a file it has no standing to
judge — and, worse, does so for a whole class of trailer-geometry rows, not just
F5.

**Byte-level: no.** What already decides it is §2.3's "a file declaring another
major is neither conforming nor nonconforming under it", which is categorical
and leaves a competent implementation no second reading once it has been found.
Both readings also leave a *reader*'s accept/reject unchanged — the file is
refused either way, under `[R-CNT-07]` — so no byte sequence changes status;
only the verifier's three-valued verdict label does, and only for an
implementation that never reaches §2.3.

---

### 8.4 What I looked at and did not report

For calibration, the places I stopped, worked through, and concluded the
document had decided it — each of which I would have reported had it not:

- Whether an experimental-range **sub-record** with MU = 1 that the verifier
  does not implement is a cannot-establish ground. §21.6's closing paragraph
  frames the case at file scope only, citing `[R-CNT-15]`, while `[R-CNT-18]`
  governs sub-records at layer scope. Resolved by §9.7's "MUST NOT certify past
  a violation it has not looked for": the alternative would have the verifier
  certify a file whose layer it could not check.
- Whether a reject-**tile** on a decode ground (T3, T24, T25) makes the walk
  incomplete. §9.7 carves out only the *structural* entry rows, which invites
  the inference that other tile rejections do end enumeration; §15.3 closes it —
  a crc-failing or decode-failing entry "keeps its place … in the coverage
  walk". Two sentences, but determined.
- Whether structurally-rejected entries are transparent to the **alignment**
  invariant as well as to slab run continuity. §16.1 does not say; §15.3's
  general clause ("contributes no stored extent to the *verifier* rows") does,
  and its table makes alignment one of those rows.
- `[R-SLB-03]`'s "each stored tile's offset equals the previous stored tile's
  offset plus its length" and L41's "plus that tile's length" — the pronoun is
  loose in both, but "contiguous and packed in ordinal order" plus §16.2's
  worked example pin it to `offset_k = offset_{k−1} + length_{k−1}`.
- Whether the pre-trailer pad's *length* is constrained. §6.2 and §2.3 both
  say a longer gap is conforming and name it as one of exactly two
  writer-conduct rules; §21.1 removes any completeness obligation on §21.6, so
  the absence of a dedicated non-violation row is not a gap.
- Whether an ignored record's extent is still a claimant. `[R-CNT-02]`'s "the
  bytes any record's extent slot references, **whatever the record's type**"
  settles it; I built the case and confirmed the extent is counted and
  uninspected.
- §21.9's compressed restatement "a layer declaring codec 4 at decoded tile size
  at most `0x7E000000`", which drops `[R-COD-07]`'s "any of whose **addressed**
  tiles" quantifier and would bar codec 4 on a zero-extent layer. §21.9's own
  preamble defers ("each is normative where the structure forcing it is
  defined"), and §17.2's Note confirms the quantified reading, so there is no
  fork.
- §24's claim that recording the row label together with the requirement
  identifier is "what survives a renumbering". Since one identifier maps to many
  rows (`[R-CNT-12]` alone governs F24, F25, F26, F29, L13, L14, L46, L47), the
  pair does not in fact disambiguate after a strike. It is an overstatement in a
  corpus-manifest rule, not a decidable defect, and I judged reporting it
  padding.

I also want to be explicit about the limit of my coverage: I implemented and
exercised codec 1 and both filters. Rows T15–T25 — the deflate, zstd and lz4
constraints — I read and reasoned about but did not execute, so if a defect
lives in §17.2's frame rules I would not have found it. §17.2's Note on the
zstd `Window_Size` derivations and sub-1 KiB tiles is the one place there I
would have wanted to run a real encoder; the Note's conclusion ("no conforming
file turns on which derivation a reader implements") follows from the two
premises it states, and I could not check the second premise against RFC 8878
under the access rule.
