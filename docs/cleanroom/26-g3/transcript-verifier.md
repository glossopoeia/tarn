# Round 26 — Verifier implementer, working transcript

## 0. Disclosure and method

I read exactly one file: `/Users/robertkleffner/Documents/GitHub/tarn/spec/tarn.md`,
in five `Read` calls covering lines 1–4484 (the file is 4484 lines; the brief
said 4485). I ran `grep`/`python3` against that file only, plus local
computation that reads no file (CRC-32C tables, integer arithmetic, and a
synthetic TARN file I generated myself into my own scratch directory). I did
not open `docs/`, `PLAN.md`, `OPEN-QUESTIONS.md`, `AGENTS.md`, `README.md`,
`conformance/`, `spec/registry.json`, or any git history. I did not list the
output directory.

The file was where the brief said it would be.

**Context I did not ask for.** My runtime placed a `CLAUDE.md` pointer and an
index of the maintainer's private memory files in my context before I began —
an index listing titles such as a naming constraint on published rationale, a
working cadence, and a note about spec edits needing propagation checks. I did
not open any of those files and I did not act on their contents; I name them
here only because the brief requires disclosure that such material appeared. I
also received the standing MCP/skill listings, which are irrelevant here.

**Tools I actually ran.** Five `Read` calls on `spec/tarn.md`; three `grep`
invocations against that file; five Python programs, all in
`/private/tmp/.../scratchpad/work/`:

- `crc.py` — CRC-32C implementation and the four stated checksum constants
- `appA.py` — Appendix A's 128-byte hexdump, decoded and re-checksummed
- `build.py` — construction of a complete conforming file of my own design
- `verify.py` — a verifier implementing §19.1/§9.7/§15.3/§16/§14.5 over it
- `slab.py` — slab run-continuity and alignment over hand-built entry arrays

Everything below is what those runs and my reading produced.

---

## 1. Checksum constants — every one I could compute, and the ones I could not

CRC-32C as §4.5 fixes it: Castagnoli polynomial 0x1EDC6F41, reflected in and
out, init 0xFFFFFFFF, final XOR 0xFFFFFFFF. Implemented as a reflected table
with the mirrored polynomial 0x82F63B78.

**Reproduced (5 of 5 computable):**

| Constant | Stated where | Stated value | I computed |
|---|---|---|---|
| CRC-32C(`"123456789"`) | §4.5, App. B | `0xE3069283` | `0xE3069283` ✓ |
| CRC-32C(zero bytes) | §4.5, App. B | `0x00000000` | `0x00000000` ✓ |
| CRC of 4 sentinel entries (80 B) | §7.4 example | `0x80A34955`, stored `55 49 A3 80` | `0x80A34955` ✓ |
| `crc_of_crc_array` over those 4 bytes | §7.4 example | `0xC4EE982E` | `0xC4EE982E` ✓ |
| CRC of a **full** all-sentinel segment (2¹⁶ entries, 1,310,720 B) | §15.4, App. B | `0xEECB3BB2` | `0xEECB3BB2` ✓ |
| Appendix A trailer CRC over trailer[0,60) | App. A | `0xE00938D2`, stored `D2 38 09 E0` | `0xE00938D2` ✓ |

Appendix A's whole 128-byte file decodes exactly as annotated: front magic,
8 zero bytes, directory `00 00 00 00` at [16,20) (CRC-32C of zero bytes),
44 zero pad bytes, then the trailer with version_major 1, version_minor 0,
flags 0, generation 1, dir_offset 16, dir_length 4, committed_file_length 128,
file_id 0x0123456789ABCDEF, reserved zero, CRC 0xE00938D2. `F mod 64 = 0`,
`dir_offset + dir_length = 20 ≤ F − 64 = 64`. Conforming.

**Could not reproduce locally:** none of this specification's own checksum
constants. Two constants belong to external formats and I did not attempt
them: the zstd frame magic `28 B5 2F FD` (§17.2 — a constant of RFC 8878, not
of this document) and the LZ4 frame magic `04 22 4D 18` (§21.4 T23, likewise).
I also did not exercise codecs 2–4 or filter 2 against real encoders; my worked
file uses codec 1 and filter 1 so that every byte is checkable by hand. That is
a limit of my walk, not a gap I found in the document.

**Verdict on §4.5's coverage claim.** I walked the checksum accounting
independently. §4.5 says every field of every structure is covered by exactly
one checksum, excepting (a) the front block, (b) "the terminal checksum fields
of §8.1's map — the trailer, directory-region, and user-metadata checksum
fields", and (c) the extent of an unassigned record type. I derived the
terminal set myself from §8.1's map: a checksum field is terminal iff no other
checksum covers it. Trailer CRC lies at [60,64) and the trailer CRC covers
[0,60) — terminal. Directory CRC is the region's final 4 bytes and covers the
preceding bytes — terminal. User-metadata extent CRC is the extent's final 4
bytes — terminal. The interior ones: each segment CRC array is covered by
`crc_of_crc_array`; each entry's `crc` field lies in the entry array and is
covered by its segment CRC; `crc_of_crc_array` lies in the layer record's
inline payload and is covered by the directory CRC. Three terminal, three
interior. §4.5's closed count of three is **correct**, and its interior list of
three is **correct**. This is one of the closed counts the brief warned about
and it survives derivation from the rule rather than from the prose.

---

## 2. The certification procedure, as an ordered algorithm

This is what I implemented in `verify.py`. Each step names its input, its
verdict contribution, and what happens when it cannot be run.

**Verdict vocabulary.** Three verdicts (§2.3, `[R-CNF-11]`): *conforming*,
*nonconforming*, *cannot establish*. Plus two report-only labels that are
explicitly **not** verdicts: *unexamined* (a scope skipped by a verifier that
elected to stop at the first violation) and the per-requirement
*unable-to-check* report. `[R-CNF-12]` adds a third report-only category: a
SHOULD deviation, reported as an advisory, never barring certification, and
never hunted for.

**Priority rule, which I encoded as the top of my reporting logic:** an
established violation beats everything. `[R-CNF-11]`: "a verifier that has
established any violation reports *nonconforming*, however many requirements it
was unable to check, and *cannot establish* is available only to a traversal
that established no violation." So *cannot establish* is reachable only from a
clean traversal. My implementation therefore computes the violation list first
and consults the unable-to-check list only when it is empty.

### Ordered algorithm

0. **Front signature block.** Input: bytes [0,16). `[R-CNT-04]` obliges byte
   equality "before other processing" for a reader that holds those bytes
   resident, and lets one that would have to fetch them defer or omit. §2.3
   removes the exemption for a verifier ("including those ordinary readers are
   exempted from"), and F6's own condition cell says so: "a verifier holds no
   such exemption (§2.3)". So step 0 is unconditional for me. Failure: F6
   (with F1 as the byte-reversed specialization), reject-file. Note this
   precedes the version gate, which is why §21.2's preamble lists F6/F1's
   front-block instance among the four rows that reach a foreign-major file.

1. **File length.** F = the transport-authoritative size (`[R-CNT-10]`). Below
   128 → F5.

2. **Trailer, in §6.2's fixed order.** magic (F8/F1) → trailer CRC over [0,60)
   (F14) → version gate (F18 for 0; a major I do not implement is not a
   finding — see below). These three and only these touch fields fixed across
   all majors (`[R-CNT-24]`).

3. **Remaining trailer gates**, validated together, not ordered among
   themselves: `committed_file_length` = F (F17) and 64-multiple (F13),
   `dir_offset ≥ 16` (F9), `dir_length ≥ 4` (F16), `dir_offset + dir_length ≤
   F − 64` (F10), `1 ≤ generation ≤ 2⁶³−1` (F11), `file_id ≠ 0` (F12),
   reserved zero (F15), incompat-lane flags (F19). §24 is explicit that a file
   failing two of these attributes to neither alone.

4. **Directory CRC** over `dir_length − 4` bytes (F20). Claim the region.

5. **Record walk** (§7.2 framing): complete records, no residue (F29); type 0
   (F24); multiplicity (F34); extent-slot validity for non-layer top-level
   records (F30/F31/F32); user-metadata framing (F21/F22/F23); reserved-range
   types (F35/F36); flag bits (F25/F26/F28). Build the layer-name namespace
   over raw bytes, uniqueness decided first and over the name fields obtainable
   within each record's `inline_length` (F4, §19.1 step 4).

6. **Per layer** (§19.3's set, plus everything else §21.3 registers): the §7.4
   constraint set (L27–L36, L39, L43, L45), geometry floor (L32), names
   (L3–L9), sub-record framing (L10–L14, L19, L23–L26), value domains and
   derived products (L1, L2), index cross-checks (L21, L22), mutual exclusion
   (L20). All decidable without I/O beyond the directory and F.

7. **Index chain**, per layer: `crc_of_crc_array` over the segment CRC array
   (L37) → each segment CRC over its entries (L38). Note this is a *layer*-scope
   failure although §19.2 places its detection point at tile use.

8. **Entry classification** (§15.3): six *structural* rows (T6, T7, T10, T8,
   T11, T12/T9) plus the crc row (T1) plus three *verifier* rows.

9. **Placement invariants** (verifier rows): per-tile alignment (L40), slab run
   continuity (L41) and run-head alignment (L42).

10. **Decode every stored tile.** §9.7: "A verifier decodes every stored tile,
    whatever content obligations §14 places on the layer: §21.4's codec rows
    are file-conformance violations, and a verifier MUST NOT certify past a
    violation it has not looked for." Codec-1 length equality (T14) is checkable
    before any fetch. Then the entry crc (T1), the decode (T25), exact
    consumption (T24), exact decoded length (T3), and the codec-specific header
    rows (T15–T23).

11. **Decoded content.** Padding positions (T4), packed-plane pad bits (T5),
    interleaved bool bytes at real positions (T2). A wrong filter stride (T26)
    has no procedure of its own: T2's or T4's check is what detects it.

12. **User-metadata extents.** Terminal CRC (R2), decode (R3), frame
    constraints under encoding 2 (R4), document rules (R5–R10), member ordering
    (F27/L48).

13. **Overlap and coverage.** §9.7's walk: disjointness (L18 intra-layer, F33
    otherwise), each claimant within [16, F−64), each verifying against the
    checksum §8.1's map states, and the slack total.

14. **Pre-trailer gap.** F7: no structure between the directory's end and the
    trailer. This is a separate check from the walk — a stored-tile extent in
    that gap passes the [16, F−64) bound and overlaps nothing, so **only** F7
    catches it. I nearly missed this writing `verify.py`; the register carries
    it and the walk does not.

15. **Report.**

### When each verdict is available

- **conforming** — the traversal established no violation and every requirement
  §21.2–§21.5 inventories was checkable. §2.4 scopes the duty: "§2.3's duty to
  check every file-level requirement runs to the MUST-level conditions §21
  inventories." That makes the 121 register rows the verifier's checklist, and
  it is why I could implement a verifier as a row-by-row program at all.
- **nonconforming** — any violation established, at any scope. Reject-tile and
  reject-layer are violations of the *file*: §2.4, "A file is conforming only
  if it satisfies every requirement at every scope: the outcome classes
  describe the blast radius of a violation for readers, never degrees of file
  conformance."
- **cannot establish** — no violation established, and at least one requirement
  unable to be checked on a capability or resource ground.

### What bars certification, enumerated

1. Any established violation (§2.4, `[R-CNF-12]`).
2. Inability to execute a layer's codec or filter (`[R-COD-11]`).
3. Declining a layer's or a tile's decode on resource grounds
   (`[R-ERR-04]`, and so `[R-SER-05]`/`[R-SER-08]` unchecked).
4. Declining to decode a user-metadata document on the verifier's own size or
   window bound (`[R-MTA-09]`).
5. A record with MU = 1 of a type the verifier does not implement (§21.6).
6. A format major the verifier does not implement (§2.3).

**What does *not* bar certification**, which took me three passes to get right:

- A user-metadata record under an **unassigned** encoding. `[R-MTA-10]`: "no
  content rule attaches to the extent's bytes … A verifier meeting such a
  record in an otherwise conforming file has no requirement it is unable to
  check — the record is not among `[R-CNF-11]`'s cannot-establish grounds, and
  certification is unaffected." But it **must be named**: owning scope,
  encoding value, stored extent length. Note the asymmetry with encoding 0 and
  the reserved range 3–0x7F, which R1 keeps as violations: "what `[R-MTA-10]`
  withdraws is the document's content rules, never the encoding byte's own
  value set."
- A SHOULD deviation (`[R-CNF-12]`) — advisory, and not searched for.
- A pre-trailer gap longer than `[R-LIF-02]` step 5's pad. §6.2: "a longer gap
  is conforming, and no conforming commit produces one," and `[R-CNF-02]` lists
  it as one of the two conduct-not-bytes cases. My verifier must **not** flag
  it. This is a trap: a naive implementation checking "the pad is < 64 bytes"
  would reject conforming files.
- A set ignore-lane flag bit (§6.3, §21.6).
- An unrecognized `tarn.` key, or a standardized key out of scope or of the
  wrong shape (`[R-MTA-06]`, `[R-MTA-07]`, §21.6).

**Ground 2 is vacuous for a conforming verifier**, and the document says so
itself. §17.4: "For a conforming reader that position arises only at a reserved
or experimental value, every assigned codec and filter being core: it rejects
the layer." A reserved/experimental codec value is L43 — a *violation*, which
takes priority. So the "cannot execute a codec" branch of `[R-COD-11]` binds
software that is not a conforming reader. I checked whether that creates a
divergence and concluded it does not: an implementer following both §2.3 and
§17.4 reaches the same verdict either way. Not reported.

### What the verifier reports when a check cannot be run

`[R-CNF-11]`: "A verifier MUST report each requirement it was unable to check
on a capability or resource ground, naming the requirement and the ground,
whichever of the three verdicts it reports; that per-requirement report
constrains the report and not the verdict." So the per-requirement report is
owed even on a *nonconforming* verdict and even on a *conforming* one — the
last case being empty by construction. `[R-MTA-09]` adds that a verifier
declining a document SHOULD report the bound it applied and the stored extent
length it declined.

---

## 3. The coverage walk on a concrete file

### 3.1 The file I built

`build.py` emits a 640-byte file. One layer:

- name `sst`, rank 1, dimension `x` with E = 100, T = 32 → G = ⌈100/32⌉ = 4,
  N = 4, P = 32
- interleaved, C = 1, channel `temp`, type 12 (float32), fill `00 00 C0 7F`
  (quiet NaN 0x7FC00000) — §12.3's channel entry byte for byte
- codec 1 (none), filter 1 (none), A = 0, S = 0, A_slab = 0
- `entry_count` = 4, index `extent_length` = 4 × 20 + ⌈4/2¹⁶⌉ × 4 = **84**
- `inline_length` = 81 (name 4 + nine scalars 34 + dimension entry 18 +
  channel entry 12 + trailing fixed 13), matching §7.4's worked example exactly
- tiles at disk ordinals 0 and 3 stored; ordinals 1 and 2 sentinel
- decoded size = P · Q = 32 × 4 = **128** bytes per tile
- ordinal 3 is the **edge tile**: it covers x ∈ [96,128), real positions
  96–99 (in-tile ordinals 0–3) and **28 padding positions** (ordinals 4–31),
  each of which I wrote as the fill bytes `00 00 C0 7F` per `[R-SER-05]`

Plus one file-scope user-metadata record: encoding 1, document
`{"tarn.title":"sst demo"}` (25 bytes) + terminal CRC = extent_length 29.

Segment CRC over the 80-byte entry array: `0x4477609B`.
`crc_of_crc_array` = CRC-32C of those 4 bytes = `0x023135B6`.

Byte map:

```
[0,16)      front signature block
[16,144)    stored tile, disk ordinal 0      128 B
[144,272)   stored tile, disk ordinal 3      128 B
[272,356)   tile-index region                 84 B
[356,385)   user-metadata extent              29 B
[385,519)   directory region                 134 B
[519,576)   pre-trailer pad                   57 B   (slack)
[576,640)   trailer                           64 B
```

`dir_offset + dir_length = 519 ≤ F − 64 = 576` ✓. 519 rounds up to 576, which
is `[R-LIF-02]` step 5's next 64-byte boundary ✓. F = 640, `640 mod 64 = 0` ✓.

### 3.2 The partition and the slack total

§5.2 `[R-CNT-02]` puts every byte of the live committed state in exactly one
of: the front signature block, or a **structure** — a stored-tile extent, a
record extent, the directory, or the trailer. §9.7 `[R-LIF-08]` names the
claimants the walk reaches: the directory itself, each record's extent, and the
stored extent of each non-sentinel index entry, plus the front block and the
live trailer as members of the live state.

Two things I had to get right and did not, at first:

1. **The tile-index region is not a second claimant.** §9.7: "A layer record's
   extent slot addresses that layer's tile-index region (§7.4), so the region
   enters the walk once, as that record's extent, and is not a second claimant
   beside it." My first draft claimed it twice and reported 84 bytes of
   negative slack.
2. **A record is not a claimant of its own.** Its header and inline payload lie
   inside the directory region, which claims them. §9.7 says this explicitly.

Arithmetic:

```
front             16
tile ord 0       128
tile ord 3       128
index region      84
user-meta extent  29
directory        134
trailer           64
                ----
claimed          583
F                640
slack             57      = exactly the pre-trailer pad
```

`verify.py` produced: `claimed 583, slack 57`, violations `[]`, unchecked `[]`
→ **conforming**. The claim list it printed was disjoint and ordered:

```
front       [0,16)     tile sst#0 [16,144)   tile sst#3 [144,272)
index:sst   [272,356)  rec-extent [356,385)  directory  [385,519)
trailer     [576,640)
```

### 3.3 Which bytes are certified, which are counted, and whether any is neither

**Certified** (covered by a checksum §8.1's map states, or by equality):
[0,16) by equality; the two tile extents by their entries' `crc` fields; the
index region's entries by their segment CRC and that array by
`crc_of_crc_array`; the user-metadata extent by its terminal 4 bytes; the
directory by its terminal 4 bytes; the trailer by its own CRC. In this file
that is all 583 claimed bytes.

**Counted but unconstrained:** the 57 slack bytes. §5.2: "Slack has no internal
structure this specification defines, its content is unconstrained, and no
conformance requirement applies to it."

**Neither?** No. §5.2's Note settles it: "The live committed state is *defined*
as the front block plus what a complete coverage walk reaches, and `[R-LIF-08]`
makes every byte that walk misses slack — so 'belongs to no class' describes
nothing, and a register row for it would be a row no file could exhibit." And
bytes past F cannot exist, because F17 makes `committed_file_length ≠` the
transport size a reject-file.

But there are **two classes inside the live state that are claimed and counted
yet not content-certified**, and a verifier's report should distinguish them:

- The extent of a record of an **unassigned type**: covered by no checksum at
  all (§4.5, §8.1's last row, `[R-SEC-04]`). A certificate covers these bytes
  without any integrity check.
- The extent of a user-metadata record under an **unassigned encoding**:
  CRC-covered, but no content rule attaches (`[R-MTA-10]`, `[R-SEC-04]`).

Only the second carries a naming duty (`[R-MTA-10]`: "bytes a certificate
covers without inspecting are counted and named, never silent"). The first,
which is strictly weaker — not even checksummed — carries none. I looked hard
at whether that asymmetry is a defect and concluded it is a stated design
choice: §22.3 names both residues in one paragraph and defends neither, and
`[R-WRT-05]`/`[R-WRT-08]` explain why an updater cannot surface the damage.
Not reported.

### 3.4 A walk that does not complete

I mutated tile ordinal 3's entry offset from 144 to 200, so its extent
[200,328) overlaps the layer's own index region [272,356). That is an
intra-layer overlap: `[R-CNT-13]` and §15.3's verifier row make it
**reject-layer**, register row **L18**.

§5.2 then governs the total: "a rejected layer's claimants are not enumerated
… and where the rejection is one the walk itself established, L18's overlap or
L40 through L42's placement among them, the claimants it had already enumerated
are discarded with the layer, since the total is a claim about a live state one
of whose layers is not usable."

So the layer's three claimants — 128 + 128 + 84 = 340 bytes — are discarded.
Enumerated: front 16 + user-meta 29 + directory 134 + trailer 64 = **243**.

```
partial total = F − 243 = 640 − 243 = 397
```

397 is reported as **partial**, with the scope that stopped the walk named
("layer `sst`, L18"). The file's true slack is still 57, so 397 is a genuine
upper bound, "tightening to the exact total when the walk completes." Verdict:
**nonconforming** (a violation was established), not *cannot establish*.

I also checked the second incompleteness route: a verifier electing under
`[R-CNF-11]` to stop at the first violation. Then the same partial rule
applies, plus every unvisited scope is reported *unexamined* — which §2.3 is
careful to say "is not a finding that the scope is clean."

And the degenerate route: §5.2's carve-out. "Where §6.2's ordered validation
rejects the file before a live trailer is established there is no F and no live
state to walk, so the total is not owed at all … which is not a partial total
but the absence of one." A verifier stopping at F8 or F14 reports the trailer
failure and says nothing about slack.

---

## 4. Extent overlap, alignment, and slab invariants on adversarial layouts

### 4.1 Overlap

I enumerated the outcome for every pair of colliding structure kinds:

| Colliding structures | Outcome | Row |
|---|---|---|
| two stored extents of one layer | reject-layer | L18 |
| a stored extent vs. its own layer's index region | reject-layer | L18 |
| a stored extent vs. its own layer's sub-record extent | reject-layer | L18 |
| a layer's index region vs. its own sub-record extent | reject-layer | L18 |
| any layer structure vs. another layer's | reject-file | F33 |
| any layer structure vs. the directory or a top-level record extent | reject-file | F33 |
| two non-layer structures | reject-file | F33 |
| any claimant vs. the front block | caught by the **bounds** rows, not F33 | F31/L16/T8, and F30/L15 for a (0, N) slot |
| any claimant vs. the trailer | caught by the bounds rows | F32/L17/T9/F10 |

F33's condition cell states the front-block/trailer carve-out explicitly,
including the half-zero subtlety: "a record extent slot of (0, N) with N
nonzero reaches the block through its zero offset and is theirs rather than
F31's or L16's." I checked that the arithmetic actually forces this: every
claimant is bounded below by `offset ≥ 16` and above by
`offset + length ≤ F − 64`, so no well-formed claimant can reach either.
This is tight.

One consequence a verifier implementer must not miss: **§15.3's structurally
invalid entries contribute no extent to the overlap check.** "Such an entry
contributes no stored extent to the *verifier* rows, which bind over
well-formed entries' extents only … and none to `[R-LIF-08]`'s coverage walk,
so any bytes it nominally addressed that no other claimant claims fall to
slack." So an entry with `offset = 10, length = 20` — which nominally reaches
the front block — is T8 (reject-tile) and is then invisible to the overlap
check. Conversely, "An entry whose only defect is that its stored bytes fail
its crc is well-formed: the defect lies in the bytes it addresses, not in the
entry, so its extent stands and it keeps its place in the *verifier* rows, in
run continuity, and in the coverage walk." I encoded exactly this split.

Also: a **structural** reject-tile does not make the walk incomplete (§9.7's
closing sentence), so the slack total stays exact even though the verdict is
nonconforming. A **layer**-scope rejection does make it incomplete. That
asymmetry is stated and I found no case where it fails.

### 4.2 Slab and alignment — worked adversarially

Layout I used (`slab.py`): **planar**, rank 1, E = 10, T = 5 → G = 2, N = 2;
C = 2 uint8 channels → `entry_count` = C · N = 4. Disk ordinals group
channel-major (`[R-GEO-06]`): ordinals 0,1 are channel 0; 2,3 are channel 1.
S = 2, A_slab = 16. Per `[R-SLB-02]`, runs partition **each channel block
independently** — [0,2) and [2,4) — and "runs never span channel blocks."
Decoded size per plane = P · B = 5 × 1 = 5 bytes, codec 1.

| # | Entry offsets (len 5 each) | Expected | `slab.py` |
|---|---|---|---|
| a | 16, 21, 32, 37 | legal | OK ✓ |
| b | 16, **22**, 32, 37 | L41 gap (expected 21) | L41 at k=1 ✓ |
| c | 16, 21, **33**, 38 | L42 (33 mod 16 ≠ 0) | L42 at k=2 ✓ |
| d | 16, **sentinel**, 32, 37 | legal — sentinels transparent | OK ✓ |
| e | 16, **offset 10** (T8, structural), 32, 37 | legal — structural entries transparent | OK ✓ |
| f | 16, 21 with **wrong crc**, 32, 37 | legal for packing — its offset and length stand | OK ✓ |
| g | **sentinel**, 21, 32, 37 | L42 — ordinal 1 is now the run's *first stored tile*, 21 mod 16 ≠ 0 | L42 at k=1 ✓ |

Case (g) is the one worth calling out. Unstoring the **head** of a run promotes
the next stored tile to "the run's first stored tile", and its offset must then
satisfy `offset mod A_slab = 0`. A writer that unstores a run head and leaves
the rest where they lie produces an L42. That is precisely the mechanism
`[R-SLB-04]` exists for, and §16.2's Note claims it is what makes the stale
declaration reachable at all: "every file exhibiting one exhibits a run whose
tiles are unpacked or whose first stored tile is misaligned, which §21.3
registers." I tried to falsify that claim — a commit that changes the
stored-tile set, run partition, or byte placement of a slab layer while leaving
both invariants intact — and could not find one that leaves the declaration
functionally stale. Cases (d)/(g) and the middle-unstore case (which breaks
packing, since sentinels are transparent rather than hole-preserving) both fire.
The Note survives.

`[R-SLB-03]`'s decidability claim also survives: "this invariant stays
decidable from the index entries alone, given the committed file length §15.3
already requires to classify any entry." Classifying an entry as sentinel /
structural / stored needs only its 20 bytes and F; the packing relation needs
only offsets and lengths. My implementation touches no payload byte.

**Per-tile alignment** (`[R-SLB-01]`, L40): quantified over "every stored
tile's offset" of the layer, in the live generation. §20.3 step 4 makes the
tense explicit for an appender — "every one the new state keeps, not only those
this commit adds" — which is the quantifier trap this shape usually hides in,
and it is closed. `[R-CNT-16]` bars declaring both A ≠ 0 and S ≠ 0 (L20), so
the two never interact.

Edge cases I checked and found defined: S > N (one short run per block,
`[R-SLB-02]`: "the final run of a block can cover fewer than S ordinals");
a run with no stored tiles ("imposes nothing"); A_slab = 1 ("contiguity-only");
a zero-tile layer that nonetheless declares a slab (nothing ties S to
`entry_count`; every run is empty and vacuous).

---

## 5. Decoded-content obligations

### 5.1 What must be decoded

Every stored tile, unconditionally, subject only to a resource decline. §9.7 is
categorical: "A verifier decodes every stored tile, whatever content
obligations §14 places on the layer." The reason is that §21.4's codec rows
(T24, T25, T3, T17–T22) are file-conformance violations that no other check
reaches, and "a verifier MUST NOT certify past a violation it has not looked
for." So even a planar float64 layer with no padding position and no bool
channel — where §14.5 and `[R-SER-08]` ask nothing — still gets every tile
decoded.

### 5.2 What it is compared against

- decoded byte length **exactly** the declared decoded size, and never a size
  read from the payload (`[R-SER-07]`, T3). Decoded size is
  `P·Q` interleaved; `P·Bᶜ` planar numeric; `⌈P/8⌉` planar bool.
- codec 1: `entry.length` = decoded size, checkable pre-fetch (`[R-COD-04]`, T14)
- every padding position = that channel's recorded fill (`[R-SER-05]`, T4)
- every pad bit of a packed plane = the plane's channel's fill bit (T5)
- interleaved bool bytes at **real** positions ∈ {0x00, 0x01} (T2)
- filter 2 inverted at the **mandated** stride only (`[R-COD-10]`, T26)

I verified the T2/T4 division of labour. `[R-SER-08]` is quantified over *every*
interleaved bool value, real and padding. T2's cell says "the same byte at a
padding position is T4's, the two rows together covering `[R-SER-08]`". That
holds: at a padding position the byte must equal the recorded fill byte, and
`[R-TYP-07]` constrains a bool fill byte to 0x00 or 0x01, so any byte violating
`[R-SER-08]` there also violates T4. No `[R-SER-08]` witness escapes the pair.

**Worked packed-plane check.** Planar bool, tile extents (2,5), P = 10, layer
extents (2,3), fill = true (0x01). Grid (1,1); in-tile ordinal `u = u₀·5 + u₁`;
padding where `u₁ ≥ 3`, i.e. ordinals 3, 4, 8, 9. Real values at 0,1,2,5,6,7 =
1,0,1,0,1,0. Decoded size ⌈10/8⌉ = 2.

- byte 0, LSB-first: bits 0..7 = ord 0..7 = 1,0,1,**1**,**1**,0,1,0 = `0x5D`
- byte 1: bit 0 = ord 8 = **1**, bit 1 = ord 9 = **1**, bits 2–7 are pad bits
  (P mod 8 = 2) and must all be the fill bit 1 → `0xFF`

Image `5D FF`. This is the §14.3 example's mechanism at a tile that has *both*
padding positions and pad bits, which the §14.3 Note is careful to separate:
"A plane can have many padding positions and no pad bits — §14.5 gives both
their content."

**Worked edge tile from my own file.** Ordinal 3 covers x ∈ [96,128) with
E = 100, so ordinals 0–3 are real and 4–31 are padding. Decoded image = 4
float32 samples followed by 28 copies of `00 00 C0 7F`. `verify.py` walks each
in-tile ordinal, reconstructs its coordinate as `tᵢ·Tᵢ + uᵢ`, tests it against
Eᵢ, and compares the fill bytes at offset `u·Q + Fᶜ`. It passed. A single byte
flipped in the padding region produced a T4.

### 5.3 What it is permitted to skip

Almost nothing. Concretely: a SHOULD deviation (`[R-CNF-12]` — "A verifier owes
no search for one"); the content of a user-metadata document under an
unassigned encoding (`[R-MTA-10]` — no rule attaches, so nothing is skipped);
the content of an unassigned record type's extent (§7.2 makes it opaque; §8.1
gives it no checksum); slack (§5.2). Everything else is owed, and a decline is
a resource ground that forfeits certification rather than a skip.

Note the trap in the other direction: `[R-COD-06]`'s undisclosed-dictionary
prohibition and `[R-CNT-13]`'s no-embedded-offsets prohibition for MU = 0
records have **no file-level witness**, and §21.7 is explicit that these are
*not* requirements a verifier is unable to check within `[R-CNF-11]`'s meaning:
"no file-level witness exists to check, so nothing about the file is left
undetermined and the verdict is unaffected." A verifier must **not** report
them as unable-to-check, or every file would come back *cannot establish*.

---

## 6. Multi-generation trace

Same layer as §3.1. All four states verified.

**Generation 1 — creation.** As built. F₁ = 640, claimed 583, slack 57 (the pad
alone). Trailer: generation 1, fresh nonzero file_id, flags 0, version_minor 0.
Creation path per `[R-LIF-02]`: front block, then steps 2–6 beginning at offset
16, **both** barriers (§20.2 is emphatic: "steps 4–6 — both barriers, not
one"). Verdict: **conforming**.

**Generation 2 — append (store tile ordinal 1).** Writing begins at exactly
F₁ = 640. The layer's stored-tile set changed, so its **whole** tile-index
region is re-emitted at a new placement (`[R-WRT-04]` step 4).

```
[640,768)    new tile ordinal 1      128
[768,852)    index region ′           84
[852,986)    directory₂              134
[986,1024)   pad                      38   (986 → 1024)
[1024,1088)  trailer₂                 64
F₂ = 1088, 1088 mod 64 = 0 ✓
```

claimed = 16 (front) + 128 (t0) + 128 (t3) + 128 (t1) + 84 (index ′) + 29 (um)
+ 134 (dir₂) + 64 (tr₂) = **711**
slack = 1088 − 711 = **377**

I computed this three ways and made them agree, because my first hand pass got
it wrong: I had carried a 44-byte placeholder for the user-metadata extent from
an earlier draft, before I fixed the document to 25 bytes + a 4-byte CRC = 29.

*By subtraction from the claim list*: 1088 − 711 = 377.

*By enumerating the unclaimed runs directly*: [272,356) = 84 (index₁),
[385,640) = 255 (dir₁ 134 + pad₁ 57 + trailer₁ 64, now one contiguous run),
[986,1024) = 38 (pad₂). 84 + 255 + 38 = **377** ✓.

*By accumulation from generation 1*: 57 (slack₁) + 84 (index₁) + 134 (dir₁) +
64 (trailer₁) + 38 (pad₂) = **377** ✓. pad₁'s 57 bytes were *already* slack at
generation 1 and must not be added again — that double-count is the other way
this arithmetic goes wrong.

**Generation 3 — update (supersede tile ordinal 0's bytes).**

```
[1088,1216)  tile ordinal 0 ′        128
[1216,1300)  index region ″           84
[1300,1434)  directory₃              134
[1434,1472)  pad                      38
[1472,1536)  trailer₃                 64
F₃ = 1536 ✓
```

claimed = 16 + 128 + 128 + 128 + 84 + 29 + 134 + 64 = **711** (unchanged — the
live state is the same size)
slack = 1536 − 711 = **825**
Accumulation check: 377 + 128 (superseded tile 0) + 84 (index′) + 134 (dir₂) +
64 (trailer₂) + 38 (pad₃) = **825** ✓. The two agree.

This is §20.3's Note in miniature: "A commit's cost is dominated by its index,
not its data." Here 84 bytes of index and 236 bytes of directory/trailer
overhead accompany a 128-byte data change.

**Generation 4 — compaction.** A whole-file rewrite under a **fresh** file_id
(`[R-WRT-06]`: "a new draw under §9.3's randomness advice, not merely a value
compared against the input's") at **generation 1**, following `[R-LIF-02]`'s
**creation** path (§20.5 is explicit that a compaction is a whole-file rewrite
"fixes what the output *is*, not which rules govern the writing of it").

```
[0,16)     front
[16,144)   tile ord 0
[144,272)  tile ord 1
[272,400)  tile ord 3
[400,484)  index region (regenerated)
[484,513)  user-metadata extent (copied verbatim)
[513,647)  directory
[647,704)  pad                 57
[704,768)  trailer
F₄ = 768 ✓
```

claimed = 711, slack = 768 − 711 = **57** — the pre-trailer pad and nothing
else. Slack fell from 825 to 57; the file fell from 1536 to 768.

What changed and what did not, per `[R-WRT-07]`: every stored tile's bytes
verbatim and every index entry's `crc` unchanged; entry **offsets** new;
sentinel entries re-emitted unchanged (ordinal 2 stays `FF ×16 00 ×4`); segment
CRCs recomputed over the entries as re-emitted; `crc_of_crc_array` updated —
the one layer-record field §20.5 names, and I confirmed by enumeration that it
is the only one: `extent_offset` is re-pointed by the relocation rule,
`extent_length` and `entry_count` are unchanged. The output's reference arrays
must equal the input's bit for bit.

Two compaction refusal paths I traced, because a verifier is often the tool
that explains them: an entry §15.3 classifies reject-tile on a structural
ground gives the compactor nothing to re-point at, so "regenerating the region
cannot proceed without meeting it", and `[R-WRT-06]` obliges refusal — no drop
is available because "a tile-index entry being no record §20.4's table licenses
dropping." And a stored tile failing its entry crc is caught by `[R-WRT-09]`'s
obligation to verify each relocated extent's checksum before emitting it.

**Verdict at each generation: conforming, conforming, conforming, conforming.**
The interesting number is not the verdict but the slack total, which is exactly
what §5.2 says it is for: "since that number is what tells an operator to
compact."

---

## 7. Findings

### verifier-01 — AMBIGUITY — `[R-ENC-04]`'s overflow quantifier does not say whether the unnamed geometry product Gᵢ · Tᵢ is in scope, and a zero-extent layer makes the two readings disagree about accepting a file

**Location:** §4.2 `[R-ENC-04]`; §11.2 `[R-GEO-03]`; §11.3 `[R-GEO-04]`;
§17.2's Note on `[R-COD-07]`; §21.3 row L2.

**The text complained about**, §4.2:

> A reader — including any updater or verifier, which are readers of the
> files they process — MUST treat any quantity this specification defines
> as a sum or product of integers obtained from a file (offsets plus
> lengths, grid counts, tile counts, sample-position counts, ordinals)
> whose mathematical value would exceed 2⁶³ − 1 as a validity error at
> the owning scope, and MUST NOT act on a wrapped or truncated value.
> `[R-ENC-04]`

and §11.3:

> Where Gᵢ · Tᵢ > Eᵢ, the tiles at the high edge of dimension i contain
> **padding positions**

and §17.2's Note:

> `[R-ENC-04]`'s overflow rule carries no such quantifier — it binds
> any sum or product a file yields — so P·Q and P·Bᶜ are checked in
> an empty layer even though this cap is not.

**The two readings.**

*Reading A (narrow).* "any quantity this specification defines" means the
quantities the document actually names and defines: §11.2's grid count Gᵢ,
spatial-tile count N, sample-position count per tile P, addressed-tile count,
total sample-position count N·P; §14.2's decoded sizes and offsets; §7.4's
index-region length; offset-plus-length sums. `Gᵢ · Tᵢ` is an expression
appearing inside a comparison in §11.3, not a named quantity, and it is absent
from §4.2's own parenthetical gloss ("offsets plus lengths, grid counts, tile
counts, sample-position counts, ordinals"). It is also absent from L2's
instance cell, which otherwise enumerates the derived products exhaustively.

*Reading B (broad).* §11.2 says "These products, like all geometry arithmetic,
are subject to `[R-ENC-04]`", and §17.2's Note says the rule "binds any sum or
product a file yields". `Gᵢ · Tᵢ` is geometry arithmetic and is a product a
file yields, so it is bound, and a layer whose `Gᵢ · Tᵢ` exceeds 2⁶³ − 1 is a
validity error at layer scope.

**Why the readings usually agree, and where they do not.** When every extent is
nonzero, `N · P = ∏(Gⱼ · Tⱼ)` and every factor is ≥ 1, so `N · P ≥ Gᵢ · Tᵢ`
for every i. Any `Gᵢ · Tᵢ` overflow therefore implies an `N · P` overflow,
which L2 already registers. The readings diverge **only when some dimension has
extent 0**, because then N = 0 and `N · P = 0` regardless of how large another
axis's `Gᵢ · Tᵢ` is.

**The concrete file.** Rank 2. Dimension `a`: E₀ = 0, T₀ = 1 → G₀ = 0.
Dimension `b`: E₁ = 2⁶³ − 1 = 9223372036854775807, T₁ = 2 → G₁ = 2⁶² =
4611686018427387904. One uint8 channel, interleaved, codec 1, filter 1, no
alignment or slab.

I computed every quantity L2's instance cell names, and every quantity §19.3
sends a reader to check:

```
N = 0            P = 2            N·P = 0          C·N = 0
P·Q = 2          P·Bᶜ = 2         entry_count = 0  region length = 0
extent sums = 0  rank 2 ≤ 32      C = 1 ≤ 4096
G₁ · T₁ = 9223372036854775808  =  2⁶³  =  (2⁶³ − 1) + 1
```

Every listed quantity is in domain. `G₁ · T₁` exceeds 2⁶³ − 1 by exactly 1.
The layer is otherwise flawless: `[R-GEO-02]` says "A dimension with extent 0
is valid … Readers MUST accept such a layer"; L21 is satisfied
(`entry_count = N = 0`); L22 is satisfied (slot (0,0), extent_length 0); L27 is
satisfied (`crc_of_crc_array` = 0); `[R-COD-07]`'s lz4 cap does not apply
(codec 1); §21.9's decoded-tile row does not bind ("A layer addressing no tile
(§11.2) therefore has no tile whose decoded size the table bounds").

The whole file is **256 bytes**: layer-record `inline_length` 91, record 115,
`dir_length` 119 at `dir_offset` 16 ending at 135, pad [135,192) = 57 bytes,
trailer [192,256).

**Which I picked, and why.** I implemented Reading A, because L2's instance
cell is the closest thing the document gives to an enumeration of the bound
quantities and it omits `Gᵢ · Tᵢ`, and because §4.2's own parenthetical does
not name it. But I do not think A is safe: §11.2's "like all geometry
arithmetic" and §17.2's "any sum or product a file yields" are both broader
than A, and §17.2's Note is exactly where an implementer would look for the
empty-layer rule — it names P·Q and P·Bᶜ and stops, which invites the reader
to ask what else is in the list.

**What an implementer does wrong without it.** Under A, a verifier certifies
the 256-byte file and a conforming reader must accept the layer (returning no
samples). Under B, the same verifier reports *nonconforming* with a reject-layer
finding, and a conforming writer must not emit the file. Two implementations
built from this document alone disagree about whether to accept a concrete,
constructible file.

**Byte-level: yes.** Two competent implementations reading this text disagree
about the accept/reject verdict on the 256-byte file above — implementation A
accepts the layer and the file, implementation B rejects the layer and reports
the file nonconforming — and correspondingly `[R-CNF-05]` permits a conforming
writer to emit it under A and forbids it under B.

**Cheapest repairs I can see** (offered as evidence the finding is actionable,
not as a demand): either add `Gᵢ · Tᵢ` to L2's instance cell and say so in
§11.3, which picks B and costs one instance against §21.8's count of 277; or
say in §11.3 that the comparison `Gᵢ · Tᵢ > Eᵢ` is evaluated only for a layer
that addresses a tile, which picks A and leaves the counts alone.

---

### verifier-02 — AMBIGUITY — the partial slack total is defined by a formula that contradicts the property stated in the same sentence whenever enumerated claimants overlap

**Location:** §5.2 `[R-CNT-21]`; §9.7 `[R-LIF-08]`; §21.2 row F33.

**The text complained about**, §5.2:

> A partial total is F less the bytes claimed by the claimants the walk
> did enumerate — an upper bound on the file's true slack, never an
> under-count — and a verifier reporting one MUST say which scope or
> violation stopped the walk.

**The two readings.**

*Reading A (sum).* "F less the bytes claimed" = `F − Σ(length of each
enumerated claimant)`. This is what an implementer writes first, because the
walk accumulates lengths as it goes; it is what I wrote in `verify.py` before I
reread the sentence.

*Reading B (union).* "the bytes claimed by the claimants" names a *set* of
bytes, so the total is `F − |union of the enumerated claimants' ranges|`.

**Where they diverge.** They agree on any file whose enumerated claimants are
disjoint — which is every conforming file, and every file whose only overlap is
one §5.2 already discards. They diverge exactly when the walk enumerates two
overlapping claimants and does **not** discard them. §5.2's discard clause is
written for layer-scope rejections the walk itself established: "where the
rejection is one the walk itself established, L18's overlap or L40 through L42's
placement among them, the claimants it had already enumerated are discarded
with the layer." **F33 is not such a rejection** — it is reject-*file*, and no
discard clause reaches it — so on an F33 file both colliding claimants stay
enumerated.

**Concrete demonstration.** Take my §3.1 file and add one top-level record of an
unassigned experimental type with MU = 0 whose extent slot is (16, 512),
overlapping the two tiles, the index region, the user-metadata extent and the
directory. That is F33 (a layer structure against another scope's structure),
reject-file. F grows to 704 to accommodate the extra 24-byte record header.
Enumerated claimants sum to 16 + 128 + 128 + 84 + 29 + 512 + 158 + 64 = 1119.

```
Reading A:  partial total = 704 − 1119 = −415
Reading B:  partial total = 704 − |union| ≥ 0, and ≥ the true slack
```

Reading A yields a **negative** count of slack bytes, and in milder cases an
under-count — which the same sentence forbids in so many words ("never an
under-count").

**Which I picked, and why.** Reading B. It is the only one under which the
sentence's second half is true, and it is provably an upper bound: the
enumerated claimant set is a subset of the full one, so the union of the
enumerated set is a subset of the union of the full set, so `F − |enumerated
union| ≥ F − |full union| =` the true slack. Reading A has no such property.

**What an implementer does wrong without it.** Writes `F - sum(lengths)`,
which is the natural accumulator, and emits a negative or under-counted slack
figure on exactly the class of file — one with an overlap — where an operator
most wants a trustworthy number. §5.2 makes the total a MUST-report, so two
verifiers can be obliged to report and can report different numbers for the
same file.

**Byte-level: no.** The verdict is *nonconforming* under both readings; only
the reported slack figure differs. Nothing in the emittable set moves and no
accept/reject verdict changes.

---

### verifier-03 — AMBIGUITY — "last" in §11.1's Rationale carries the document's positional house sense, under which the sentence it closes is false

**Location:** §11.1, the Rationale block following `[R-GEO-02]`.

**The text complained about:**

> Growth that changes entry_count changes extent_length with it
> (`[R-CNT-17]`), so the layer's whole tile-index region is re-emitted and
> disk ordinals renumber wherever `[R-GEO-06]` moves them (§20.3,
> `[R-WRT-04]`) — the growth that raises a zero-extent layer's **last**
> zero grid count included.

**The two readings.**

*Reading A (positional).* "last" = last-declared. This is the house sense
everywhere else in the document. I censused every occurrence of the bare word:
§11.4 "the **last**-declared dimension varies fastest"; §16.2's Note "a run is
a band along the **last**-declared dimension"; §11.2's Example "the **last** row
of tiles is padded"; §14.3 "beyond the **last** value"; §15.4's Example "the
**last** covering 16,960 entries"; §21.9 "The **last** three rows"; §7.2/F29
"after the **last** complete record"; §9.4/§9.6 "the **last** committed state";
Appendix G item 2 "the digest's **last** eight bytes in output order". Ten of
eleven other uses are positional or ordinal; only §2.3's "the **last** where
some requirement…" and §21.6's "that **last** ground" are the
most-recently-mentioned sense. Under Reading A the phrase means "the growth
that raises the grid count of the last-declared dimension among those that are
zero."

*Reading B (final remaining).* "last" = the last one still at zero, so that
raising it takes N from 0 to positive.

**Which I picked, and why.** Reading B, because Reading A makes the sentence
false. Under A, raising the last-declared zero grid count while another
dimension's grid count remains 0 leaves `N = ∏Gᵢ = 0` and therefore leaves
`entry_count` unchanged — which is the *opposite* class from the one the
sentence says it belongs to ("Growth that changes entry_count …"). Only under B
does the appended clause hold, since eliminating the final zero factor is
exactly what moves N off 0. The immediately preceding sentence sets the
contrast up — "a growth raising one grid count ⌈Eᵢ / Tᵢ⌉ (§11.2) while another
stays 0 among them, the product holding at 0" — so context resolves it for a
reader who does the arithmetic.

**What an implementer does wrong without it.** Nothing on disk. An updater
author who takes Reading A concludes that raising the last-declared zero extent
always forces an index re-emission and may re-emit a zero-length region — which
`[R-CNT-17]` and `[R-CNT-23]` then make a violation (L22 with a nonzero slot at
`entry_count` = 0, or L27). But the same author reading §20.3 step 4 directly
gets the right rule, and this passage is a Rationale block, which `[R-CNF-01]`
places outside normative text.

I report it because the brief's shape 7 is exactly this — a bolded ordinary
English word whose sense the reader supplies — and because Appendix G item 2
shows the document already treats this class of ambiguity as worth spending
words on ("naming the end rather than calling them the *low* bytes is
deliberate, that word being read as a position by some and as an arithmetic
magnitude by others"). A two-word repair, "last **remaining** zero grid count",
closes it.

**Byte-level: no.** `[R-CNF-01]` puts Rationale outside normative text, the
normative rule (§20.3 step 4 and `[R-CNT-17]`) is unaffected, and both readings
of the Rationale leave the same files emittable.

---

## 8. Things I checked and did not report

Recorded so the next round does not re-walk them.

**Closed counts, all derived from the rule rather than the prose, all correct.**
§21.8's "121 conditions over 277 instances": I parsed §21.2–§21.5
mechanically under §21.1's stated rule ("Instances within a cell are separated
by semicolons, and a cell reading — is one instance") and got exactly 121 rows
and 277 instances, split F 36 / L 49 / T 26 / R 10 — matching each subsection's
own stated count. §4.5's three terminal and three interior checksum fields:
derived independently from §8.1's map, correct. §2.3's five conformance
classes; §10.1's four extension vehicles; §12.1's thirteen sample types and
twelve numeric types; §15.3's "Six rows are marked *structural*" (I counted
six, and confirmed the six exhaust the malformations decidable from an entry's
20 bytes plus F); §22.3's "Four residues"; §21.7's four compaction-trailer
obligations; §21.2's "Four rows are outside that reasoning" (F8, F1, F14, F6);
§20.5's "one row for each of the other seven spaces §10.2 tabulates (L31, L33,
L34, L36, L43, L45, R1)" — I mapped each row to its space and all seven land.

**Register mechanics.** Every one of the 20 verifier-detected rows carries
Detected = *certification*; every reader-detected row carries one of §19.2's
four tiers (R1 carries two, correctly, being top-level or sub-record). No row
carries a detector outside {reader, verifier}. Appendix H's verifier checklist
accounts for all 20 (T26 via T2/T4, as T26's own cell says).

**§16.2's Note that a stale slab declaration needs no register row.** I tried
to construct a file with a functionally stale declaration and no L41/L42, and
failed; the sentinel-transparency rule is what forces the violation whenever a
commit unstores or relocates within a run.

**`[R-ENC-04]`'s coverage of other unnamed products.** Partial products
`∏_{j>i} Gⱼ` and `∏_{j>i} Tⱼ` are bounded by N and P; `Q = Σ Bᵢ` and
`Fᶜ = Σ_{j<c} Bⱼ` are bounded by 65535 × 8; `⌈P/8⌉ ≤ P`; `20·k` is bounded by
the region length; `(s+1)·2¹⁶` is bounded by `entry_count + 2¹⁶ − 1`, and an
`entry_count` large enough to overflow it overflows the region-length formula
first (L2). `Gᵢ · Tᵢ` is the only unnamed product that escapes, and it is
verifier-01.

**T14 against T3 and T24 under codec 1.** A codec-1 tile whose entry length
differs from the decoded size satisfies more than one row. All three are
reject-tile / reader / tile use, so no verdict forks; §24 `[R-VEC-02]` already
governs multi-row attribution in the corpus ("the entry records every row the
file exercises and says which it was built for"), and §21.1's specialization
list is introduced with "Some rows are…", not as closed.

**`[R-COD-11]`'s cannot-establish branch is vacuous for a conforming verifier**
— §17.4 says so itself, and the violation-priority rule makes the verdict the
same either way. Not a divergence.

**The reporting asymmetry between an unassigned metadata encoding (MUST be
named, `[R-MTA-10]`) and an unassigned record type's extent (no naming duty,
and not even checksummed, §8.1 / `[R-SEC-04]`).** §22.3 states both residues in
one paragraph and defends the design; nothing is ambiguous, only asymmetric.

**§18.2's "the bound above"** in `[R-MTA-09]`'s verifier sentence is ambiguous
between the decoded-size bound and the frame's declared window, but §21.5's
preamble names both grounds and §2.3's list is generic, so the verdict is the
same under either. Not a fork.

**Degenerate files I built or specified and found defined:** the 128-byte
minimum (Appendix A, re-checksummed); a 192-byte file with one empty layer
(the smallest file that can carry a layer at all, since a minimal layer record
is 97 bytes and forces `dir_offset + dir_length ≥ 117`); `entry_count` at
exactly 65,536 (one full segment, `[R-IDX-05]`'s constant licensed by the
"final or not" clause) and at 65,537 (two segments, the second partial, its CRC
"MUST be computed"); a layer with `entry_count` = 0 that nonetheless declares a
slab (vacuous, every run empty); codec 4 on a layer addressing no tile
(conforming per §17.2's Note); a stored-tile extent in the pre-trailer gap
(F7 only — the coverage walk does not catch it); two layer records sharing one
extent slot (F33, since the regions coincide exactly).

**§9.6's recovery probe.** For a verifier it is diagnosis, not a finding: "no
verdict turns on the probe". I confirmed the three rows §9.6 names for a file
whose final 64 bytes are not a valid trailer — F8 (magic), F14 (trailer CRC),
F17 (the length cross-check) — are the right three, and that the probe's start
point ("the largest 64-aligned offset o with o + 64 ≤ the physical file
length") and continuation rule are unambiguous.

---

## 9. Confidence

**Medium-high.** I built a conforming file from the document alone, wrote a
verifier from the document alone, and the two agreed on the first run after I
fixed two of my own errors (double-claiming the index region, and mis-summing
the multi-generation slack). Every checksum constant the document states and
that I could compute locally reproduced. The register is complete enough to
serve as the verifier's literal checklist, which is a strong property and one
§2.4 states deliberately.

The one place where I think a fresh implementer could build something that
disagrees with another fresh implementer about bytes on disk is verifier-01, and
it is confined to a layer that has a zero-extent dimension *and* another axis
whose grid times tile extent lands within one of 2⁶³. That is a file nobody
would write on purpose, which is where the brief said to look.
