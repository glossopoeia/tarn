# Cleanroom round 31 — Verifier implementer, working transcript

## 0. Access and disclosure

I read exactly one file: `/Users/robertkleffner/Documents/GitHub/tarn-first-draft/spec/tarn.md`
(4,790 lines), in five `Read` calls covering lines 1–4790 with no gaps. I opened
no ADR, no `docs/`, no `conformance/`, no `registry.json`, no `PLAN.md`, no
`OPEN-QUESTIONS.md`, no git history. I ran no web search and no web fetch. I did
not list the output directory.

The spec was where the brief said it would be.

**Context I did not ask for.** Two things appeared in my context before I began.
(a) A project instruction file (`CLAUDE.md`, redirecting to `AGENTS.md`) — I read
neither target and treated the pointer as nothing. (b) An index of the
maintainer's auto-memory notes, whose entries name this project's harness,
lineage gate, repair process and subagent model. I disregarded all of it; I did
not open any note, and no conclusion below rests on any of it. I disclose that
it appeared, as instructed, without repeating its contents.

Files I wrote, all under
`/private/tmp/claude-501/-Users-robertkleffner-Documents-GitHub-tarn-first-draft/r31-round/scratch/verifier/`:

- `crc.py` — a from-scratch CRC-32C (reflected poly 0x82F63B78, init/final 0xFFFFFFFF)
- `appA.py` — decodes and re-checksums Appendix A's 128-byte hexdump
- `count.py` — mechanical row/instance count over §21.2–§21.5
- `build.py` — builds a concrete generation-1 file and runs the §9.7 walk on it
- `trace.py` — cross-checks the document's worked examples and runs the four-generation trace

and this transcript at the single output path named in the brief.

---

## 1. Method

My charter is the verifier: the certification procedure, the coverage walk and
slack arithmetic, extent/alignment/slab invariants, checksum obligations,
decoded-content obligations, and a multi-generation trace.

I worked in this order:

1. Read the document end to end once, without stopping to judge.
2. Reproduced every checksum constant the document states, locally.
3. Reproduced every worked numeric example I could compute.
4. Counted §21's rows and instances mechanically against §21.8's stated figures.
5. Built a concrete file byte-for-byte and ran the coverage walk on it, then
   ran it again through four generations including a compaction.
6. Went back over the seventeen changed passages and the three decisions the
   brief described, and over the parts of the document my charter touches that
   were in no hunk.

A note on searching, since the brief warned about it and the warning was
warranted. My first phrase sweep searched for `"conduct rather than"` and
returned **0**, which is false: §9.2 contains `bind a writer's **conduct**
rather than its output`. The `**` bold markers, not the hard wrap, defeated it.
I rebuilt the search over a normalised copy (join `\n> ` blockquote
continuations, collapse whitespace, strip `**`, `*` and backticks) and re-ran
the same query against a control phrase I knew was present. Every zero reported
below is from the normalised corpus with a control phrase verified in the same
passage. Raw line-oriented `grep` is not trustworthy on this document and I did
not rest anything on it.

---

## 2. The certification procedure, as an ordered algorithm

Assembled from §2.3 `[R-CNF-11]`, §2.4 `[R-CNF-12]`, §6.2 `[R-CNT-06]`, §19.1–§19.4,
§9.7 `[R-LIF-08]`, §17.4 `[R-COD-11]`, §18.2 `[R-MTA-09]`/`[R-MTA-10]`.

### Verdict vocabulary

Three verdicts, and three report-only annotations that are not verdicts:

| Token | Kind | When |
|---|---|---|
| *conforming* | verdict | no violation established **and** no requirement left unchecked on a capability or resource ground |
| *nonconforming* | verdict | at least one violation established. Takes priority over everything (§2.3) |
| *cannot establish* | verdict | no violation established, but some requirement is uncheckable on a capability or resource ground |
| per-requirement "unable to check" | report | MUST accompany **any** of the three verdicts (§2.3) |
| *unexamined* (per scope) | report | MUST accompany a verdict from a verifier that elected to stop at the first violation |
| slack total, exact or partial | report | §5.2 `[R-CNT-21]` |

The document is careful that *cannot establish* is **mandatory**, not merely
available, once a requirement is uncheckable and no violation was found:
`[R-COD-11]` and `[R-MTA-09]` both say the inability "fixes the file's verdict as
*cannot establish* only where the verifier established no violation elsewhere",
and "fixes" is not "permits". So *conforming* is unreachable while any
capability/resource inability stands. That in turn makes §2.3's "whichever of the
three verdicts it reports" cover a combination — unchecked-requirement report
alongside *conforming* — that cannot arise. Harmless: the obligation is
unconditional, and stating it over all three verdicts costs nothing.

### The algorithm

**Step 0 — size floor.** If the physical file is under 128 bytes: F5,
reject-file, *nonconforming*, and stop (§5.1 `[R-CNT-27]`). No slack total is
owed — there is no live state.

**Step 1 — trailer, in §6.2's fixed order.** Read the final 64 bytes.
Validate, strictly in order: magic (F8); trailer CRC (F14); the version gate
(F18 for major 0; an unimplemented major → §2.3 makes this *cannot establish*,
not *nonconforming*, since `[R-CNT-07]`'s refusal "is not a finding about its
bytes"). Then, those gates passed, all of: flag gates (F19 for any incompat bit);
committed_file_length against the transport-authoritative size and mod 64 (F17,
F13); dir_offset ≥ 16 (F9); dir_length ≥ 4 (F16); dir_offset + dir_length ≤ F − 64
(F10); file_id ≠ 0 (F12); reserved 12 bytes zero (F15). Any failure: reject-file.

Two things a verifier must get right here that a reader need not.

First, a verifier holds **no residency exemption** on the front signature block.
`[R-CNT-04]` lets a reader that would have to issue a further range request defer
or omit the equality check; §2.3's verifier "checks every file-level
requirement — including those ordinary readers are exempted from", and F6's row
says so explicitly ("a verifier holds no such exemption (§2.3)"). So a verifier
fetches [0, 16) whatever its transport, and checks F1's front-block instance and
F6.

Second, on a file declaring a foreign format major, §2.3 `[R-CNF-13]` narrows the
whole procedure to the **reaching** conditions. §21.2's preamble derives them:
F8, F14, F6 and both of F1's instances, "and no other row". If all pass, the
verdict is *cannot establish*; if any fails, *nonconforming* "whatever major the
file declares". I checked the reach derivation myself against `[R-CNT-24]`: the
permanently-fixed trailer bytes are magic [0,8), version_major/minor [8,12), and
the CRC at [60,64) — 16 bytes; the other 48 (offsets [12,60)) are redefinable,
which is why F15 (reserved bytes zero, [48,60)) does not reach and F5 does not
either. The §2.3 Note states exactly this and it is correct.

I paused on one apparent conflict. `[R-CNF-13]` says "an exemption the
condition's governing requirement grants on a ground other than the declared
major applies unchanged, `[R-CNT-04]`'s residency exemption among them", while
§2.3 removes that exemption from verifiers. Two readings: (i) on a foreign-major
file even a verifier may skip the front block; (ii) "applies unchanged" means the
foreign major does not disturb whatever exemption the actor otherwise has, which
for a verifier is none. (ii) is right — "unchanged" is relative to the actor's
ordinary position, and F6's row states the verifier position unconditionally.
Closed.

**Step 2 — directory.** Fetch [dir_offset, dir_offset + dir_length), verify the
terminal CRC before any other use (F20). Parse the record sequence: no residue,
no record overrunning the sequence (F29); type 0 (F24); MU gate for unknown
top-level types (F35 for a reserved-range type with MU=1); multiplicity (F34);
extent-slot validity for non-layer top-level records (F30, F31, F32); the
user-metadata framing rules (F21, F22, F23); the layer-name namespace (F4).

Verifier-only at this tier: reserved flag bits (F26, L47), MU=1/PE=0 (F25, L46),
a registered type's stored MU/PE against §7.3 (F28, L49), and a reserved-range
record or sub-record type value whatever its MU bit (F36, L25).

**Step 3 — per layer.** §19.3's full layer-record validation: L1–L36, L39,
L43–L45. All decidable from the resident directory and F — "layer access
performs no fetch".

**Step 4 — per layer, index chain.** crc_of_crc_array over the segment CRC array
(L37); each segment CRC (L38); then classify every entry per §15.3 (T6–T12).

**Step 5 — per stored tile.** Fetch the extent, verify the entry crc (T1),
decode (T24, T25, T3, T14–T23), then check decoded content: padding positions
(T4), packed-plane pad bits (T5), interleaved bool bytes (T2), and the filter
stride so far as those two witness it (T26).

§9.7 is unambiguous that this is owed on every stored tile, not only on layers
that carry padding or bools: "A verifier decodes every stored tile, whatever
content obligations §14 places on the layer: §21.4's codec rows are
file-conformance violations, and a verifier MUST NOT certify past a violation it
has not looked for."

**Step 6 — record extents.** User-metadata: terminal CRC (R2), encoding value
(R1), frame constraints under encoding 2 (R4), decode (R3), then the decoded
document's own rules (R5–R10) and member ordering (F27, L48). Under an
experimental-range encoding, §18.2 `[R-MTA-10]` attaches **no** content rule; the
record is not a cannot-establish ground, certification is unaffected, and the
verifier MUST report the record naming owning scope, encoding value and stored
extent length. Encoding 0 and the reserved range stay R1 violations.

**Step 7 — the coverage walk (§9.7).** Below.

**Step 8 — pre-trailer gap.** No structure between the directory's end and the
trailer (F7, §6.2 `[R-CNT-05]`).

**Step 9 — verdict.** Violation established anywhere → *nonconforming*.
Otherwise, any requirement uncheckable on a capability or resource ground →
*cannot establish*. Otherwise *conforming*, plus the slack total.

### What bars certification, and what does not

Bars it: any established violation; any capability or resource inability
(`[R-COD-11]` for a codec or filter it cannot execute; `[R-ERR-04]` for a layer
or tile decode declined on resource grounds; `[R-MTA-09]` for a document decode
declined on the size bound or the frame's declared window; an unimplemented
format major; an unimplemented type carrying MU=1).

Does **not** bar it: a SHOULD deviation — §2.4 `[R-CNF-12]` says a verifier
"reports a SHOULD deviation as an advisory that does not bar certification" and
"owes no search for one". A user-metadata record at an experimental-range
encoding — `[R-MTA-10]`, "no requirement it is unable to check". A conforming
file exceeding a §21.9 guarantee that the verifier can nonetheless handle.

I checked Appendix H's verifier checklist against my enumeration of
verifier-detected rows (F7, F25, F26, F27, F28, F33, F36, L18, L25, L40, L41,
L42, L46, L47, L48, L49, T2, T4, T5, T26, plus F1/F6 as a verifier). Every one is
covered; T26 is covered transitively, its own row saying "the check that detects
it is T2's or T4's". The checklist is complete and I found no divergence from the
normative text it summarises.

---

## 3. The coverage walk, with arithmetic

### The partition

§5.2 `[R-CNT-02]`: every byte of the live committed state belongs to exactly one
of **the front signature block**, or a **structure** — a stored-tile extent, a
record extent (whatever the record's type), the directory, or the trailer.
§9.7 adds that the front block at [0,16) and the live trailer at [F−64, F) are
claimed by the walk, and that every other claimant lies in [16, F−64), which is
what keeps them disjoint from those two.

Claimant enumeration, from §9.7:

- the directory region (including its terminal CRC — §7.1 makes the CRC part of
  the region);
- each record's extent, reached through the directory's records **and their
  sub-records**;
- the stored extent of each non-sentinel tile-index entry.

Two exclusions, both stated: a record is **not** a claimant of its own header and
inline payload (those lie inside the directory region, which claims them), and a
layer record's extent **is** that layer's tile-index region, so the region enters
once rather than twice.

Two entry-level rules, from §9.7 and `[R-IDX-03]`: an entry §15.3 classifies
reject-tile on a *structural* ground contributes **no** stored extent (its
nominal bytes fall to slack, and the walk is not thereby incomplete); an entry
whose only defect is that its stored bytes fail its crc **keeps** its extent (it
stays in the overlap check, in slab run continuity, and in the walk).

### Can a byte be neither certified nor counted?

No. §5.2's Note settles it: "The live committed state is *defined* as the front
block plus what a complete coverage walk reaches, and `[R-LIF-08]` makes every
byte that walk misses slack — so 'belongs to no class' describes nothing, and a
register row for it would be a row no file could exhibit." Only disjointness is
testable, and that is what F33/L18 register. I built no case against this and
believe none exists.

The finer three-way split my charter asks for:

- **Certified** (claimed **and** covered by a checksum §8.1 states): stored-tile
  extents (entry crc), tile-index regions (segment CRCs under crc_of_crc_array),
  the directory (its terminal CRC), the trailer (its own CRC), user-metadata
  extents (terminal CRC) — this last **including** one under an
  experimental-range encoding, which §22.3 confirms: "covered by its terminal CRC
  but constrained by no content rule".
- **Claimed but uncovered**: the front signature block (equality, not checksum);
  and the extent of a record of a type this specification has not assigned,
  which §8.1's map "covers by no checksum at all". That second one is a
  certificate covering bytes it has never checked, and §22.3 names it as one of
  its four stated-not-defended residues. It is the only class of live byte a
  clean certificate says nothing about.
- **Counted but unconstrained**: slack.

I chased one thing here and closed it. Does an **ignored** record's extent stay
claimed, or fall to slack? §2.4 says ignore-record means "skipped as though
absent", which read broadly would remove it from the live state and change the
slack total — a report fork between two verifiers. It does not: §5.2 defines a
record extent as "the bytes any record's extent slot references, **whatever the
record's type**"; §2.4's "as though absent" is bounded by its own next sentence
("Decoding of all stored data is unaffected"); and `[R-MTA-10]` closes it
outright — "bytes a certificate covers without inspecting are counted and named,
never silent". Claimed, not slack. Closed.

### Worked arithmetic — a concrete generation

I built a real file rather than an abstract one. Layer `sst`, the §7.4 example's
geometry: rank 1, dimension `x` with E = 100, T = 32; interleaved; one float32
channel `temp`, fill quiet NaN 0x7FC00000; codec 1 (none), filter 1 (none); no
alignment, no slab.

- G = ⌈100/32⌉ = 4, N = 4, entry_count = 4 (interleaved).
- P = ∏Tᵢ = 32, Q = ΣBᵢ = 4, decoded size = P·Q = **128** bytes.
- Under codec 1, `[R-COD-04]` forces each non-sentinel entry's length = 128.
- Index region = 4×20 + ⌈4/2¹⁶⌉×4 = 80 + 4 = **84** bytes (`[R-CNT-17]`).
- Layer inline payload: I laid the fields out in §7.4's table order and got
  **81 bytes** — identical to the document's own example, field for field
  (4 name + 34 scalars + 18 dimension entry + 12 channel entry + 13 trailing).
- Record framing: 24 + 81 = 105; directory = 105 + 4 (CRC) = **109** bytes.

Tiles 0 and 2 stored, tiles 1 and 3 sentinel. Placement:

```
[0,   16)   front signature block          16
[16,  144)  stored tile, disk ordinal 0   128
[144, 272)  stored tile, disk ordinal 2   128
[272, 356)  tile-index region              84   (= layer record's extent)
[356, 465)  directory region              109
[465, 512)  pre-trailer pad                47   <- slack
[512, 576)  live trailer                   64
F = 576, F mod 64 = 0
```

Checks: dir_offset 356 ≥ 16; dir_length 109 ≥ 4; 356 + 109 = 465 ≤ F − 64 = 512;
every non-front, non-trailer claimant inside [16, 512); pairwise disjoint
(verified by sorting and comparing adjacent bounds).

Slack total: F − Σ|claimants| = 576 − (16+128+128+84+109+64) = 576 − 529 = **47**,
and the 47 bytes are exactly [465, 512), the pre-trailer pad. Exact total, walk
complete, no violation → *conforming*.

Degenerate check, since §5.1 supplies one: the 128-byte minimal file. Claimants
are [0,16) = 16, the directory [16,20) = 4, the trailer [64,128) = 64; total 84;
slack = 128 − 84 = **44**, which is [20, 64) — precisely the "44 bytes of slack"
§5.1's example states.

### A walk that does not complete

Same file, but make the entry for disk ordinal 2 overlap the tile-index region:
offset 272, length 128 → [272, 400), which straddles the region [272, 356). §15.3
classifies this "a stored extent overlaps its own layer's index region" —
*verifier*, reject-layer, L18.

§5.2 then does three things at once, and I had to read it twice to keep them
apart. (i) The layer is rejected, so its claimants are not enumerated — "whether
or not the rejection impeded reading them". (ii) Because the rejection is one the
walk itself established, "the claimants it had already enumerated are discarded
with the layer". (iii) The total is reported as partial.

Partial total = F less the bytes claimed by the claimants that survive, i.e. the
front block, the directory and the trailer: 576 − (16 + 109 + 64) = **387**. The
true slack of this (nonconforming) file is 47. 387 > 47, so the invariant §5.2
asserts holds: "an upper bound on the file's true slack, never an under-count".
The verifier reports 387 as partial, names the layer as what stopped the walk,
and reports *nonconforming* — the established violation taking priority over
everything, per §2.3.

I checked the never-an-under-count claim for the other stopping mode too. A
verifier electing to stop at the first violation has enumerated a subset of the
claimants, so F minus that subset's **union** is ≥ F minus the full union. It is
an under-count only if one sums lengths instead of taking the union of ranges,
which would require two enumerated claimants to overlap — and that overlap is
itself the violation. So the bound holds under any stopping point.

A degenerate case worth recording, because it cuts the other way. Suppose the
rejected layer is one with a zero-extent dimension: entry_count = 0, extent slot
(0,0), crc_of_crc_array = 0, rejected on L27 for a nonzero crc_of_crc_array. That
layer has **no** claimants. §5.2's obligation keys on the condition "the walk does
not enumerate every region's claimants", which is false here — there were none to
skip. So the total stays exact even though a layer was rejected. The rule is
written on the enumeration and not on the rejection, and that is what makes this
come out right.

---

## 4. Extent overlap, alignment and slab invariants, adversarially

### Overlap

`[R-CNT-13]` gives three outcomes and I checked the partition is exhaustive:
intra-layer overlap → reject-layer (L18); overlap across layers or against
another scope's structures → reject-file (F33); overlap between two structures
neither of which belongs to a layer → reject-file (F33). Cases I put to it:

- two stored extents of one layer → L18;
- a stored extent against its own layer's index region → L18 (the case I used above);
- a stored extent against a layer sub-record's extent → L18;
- a layer's index region against the directory → F33 (layer structure vs another scope's);
- two top-level record extents → F33 (neither belongs to a layer);
- layer A's index region against layer B's stored tile → F33;
- a claimant reaching [0,16) or [F−64, F) → **not** an overlap row: F33's own
  text routes it to the bounds rows F9/F10, F30/F31/F32, L15/L16/L17, T8/T9,
  "each at its own tier". I tried to construct a claimant that reaches the front
  block or trailer without tripping a bounds row and could not: extent_offset ≥ 16
  and extent_offset + extent_length ≤ F − 64 are enforced for record extents
  (`[R-CNT-13]`), stored extents (§15.3), and the directory (`[R-CNT-06]`).
  The routing is exhaustive.

F33's own carve-out about the half-zero rows is right too: a slot (0, N) with N
nonzero has offset 0, so it reaches the front block through its **zero offset**,
and F30/L15 (exactly one half zero) fire before F31/L16 (offset in 1–15).

### Alignment

`[R-SLB-01]`: A a power of two, 512 ≤ A ≤ 2⁶²; when declared, every stored tile's
offset ≡ 0 mod A; verifier-checked, reject-layer (L40). Adversarial layout: A =
4096, the file above with tile 0 at offset 16 → 16 mod 4096 ≠ 0 → L40. To make it
conform, the first structure must start at 4096, which forces [16, 4096) to slack
— 4,080 bytes. Appendix G item 3 anticipates exactly this: "or, where a declared
alignment admits no structure at 16, at the least position above it the
declaration admits".

Which entries does "every stored tile" range over? §15.3's *verifier* rows "bind
over well-formed entries' extents only", and a structurally-rejected entry
contributes none. An entry whose only defect is a failed crc **is** well-formed,
so its offset is still checked for alignment. §16.1 does not restate this, but
§15.3's governing prose does, and L40's Governing rule cell cites `[R-IDX-03]`.
Decidable.

### Slabs

`[R-SLB-02]`: runs partition each contiguous block of disk ordinals
independently — [0, N) interleaved, [c·N, (c+1)·N) per channel planar; run r of a
block starts at block_start + r·S; the final run of a block may be short.

Adversarial layout I worked: planar, C = 2, N = 3, S = 2, A_slab = 512. Blocks
[0,3) and [3,6). Four runs: {0,1}, {2}, {3,4}, {5}. Note that run boundaries fall
**inside** what looks like a uniform stride — ordinal 2 begins a run of its own,
so it must be 512-aligned, and ordinal 3 begins a new block's run 0, so it must
be too. A writer that treated the ordinals as one 6-long sequence with S = 2
would put run boundaries at 0, 2, 4 and misalign ordinal 3. "Runs never span
channel blocks" is the sentence that decides it, and it is explicit.

Transparency, from `[R-SLB-03]`: sentinels are transparent to run continuity; so
are entries §15.3 classifies reject-tile on a *structural* ground ("the run's
stored tiles close over them"); an entry failing **only** its stored bytes' crc is
**not** transparent — "its offset and length stand, and the packing relation reads
them as it does any other stored tile's". This is what keeps the invariant
decidable from the index entries plus F alone, and L41's Instances cell restates
the same three-way split correctly. I checked: `gap; overlap; out-of-ordinal
placement` — three instances, and the row text carries the transparency rules.

Concrete failures I constructed: ordinal 0 at 512 len 100, ordinal 1 at 620 (≠
512+100) → L41 gap; ordinal 2 at 662, 662 mod 512 = 150 → L42; ordinal 1 placed
below ordinal 0 → L41 out-of-ordinal. A run with no stored tiles "imposes
nothing", and a layer with N = 0 has no runs at all — legal, and a slab
declaration on it is vacuous.

`[R-SLB-04]`'s stale-declaration rule has no register row of its own, and §16.2's
Note explains why: every file exhibiting one exhibits L41 or L42. I checked that
claim and it holds — a carried-forward declaration whose runs were not
re-established is by construction a run that is unpacked or whose first stored
tile is misaligned.

`[R-CNT-16]` makes A and S mutually exclusive (L20), so no layout is subject to
both invariants at once.

---

## 5. Checksum obligations

### The map

§8.1's table, checked against §4.5's prose:

| Structure | Checksum | Covers |
|---|---|---|
| front signature block | none — byte equality | — |
| trailer | bytes [60,64) | trailer [0,60) |
| directory region | final 4 bytes | preceding dir_length − 4 |
| tile-index region | segment CRC array, itself under crc_of_crc_array | entries, per segment |
| stored tile | its entry's crc field | the tile's stored bytes |
| user-metadata extent | final 4 bytes | the preceding encoded bytes |
| extent of an unassigned-type record | none | — |

Is every field covered exactly once? I walked it. Entry crc fields are inside
their segment, so the segment CRC covers them. The segment CRC array is covered
by crc_of_crc_array. crc_of_crc_array is a field of the layer record's inline
payload, which lies in the directory region, so the directory CRC covers it. The
directory CRC and the trailer CRC and a user-metadata extent's CRC are terminal —
comparison-verified, covered by nothing further. §4.5 names exactly these three as
terminal and exactly these three as interior (segment CRC array, entry crc,
crc_of_crc_array). The classification is complete and self-consistent.

Is every **live structure** covered by one? All but two, and both are named:
the front block (equality instead), and an unassigned-type record's extent
(nothing). `[R-CNT-17]` forces the index region's length to
entry_count × 20 + ⌈entry_count/2¹⁶⌉ × 4 and §15.1 forbids padding inside it, so
there is no uncovered byte hiding in the region either.

### Constants I reproduced

I implemented CRC-32C from the parameters §4.5 states (Castagnoli 0x1EDC6F41,
reflected in and out, init 0xFFFFFFFF, final XOR 0xFFFFFFFF) — reflected table
polynomial 0x82F63B78 — and computed:

| Constant | Document | Computed | ✓ |
|---|---|---|---|
| CRC-32C(`"123456789"`) | 0xE3069283 | 0xE3069283 | ✓ |
| CRC-32C(zero bytes) | 0x00000000 | 0x00000000 | ✓ |
| §7.4: CRC over 80 bytes = 4 sentinel entries | 0x80A34955, stored `55 49 A3 80` | 0x80A34955 | ✓ |
| §7.4: crc_of_crc_array over `55 49 A3 80` | 0xC4EE982E | 0xC4EE982E | ✓ |
| §15.4: full all-sentinel segment (2¹⁶ entries, 1,310,720 bytes) | 0xEECB3BB2 | 0xEECB3BB2 | ✓ |
| Appendix A: trailer CRC over [0,60) | 0x402F157E, stored `7E 15 2F 40` | 0x402F157E | ✓ |
| Appendix A: directory CRC (zero records) | 0x00000000 | 0x00000000 | ✓ |

**Seven of seven reproduced. None could not be.** I also parsed Appendix A's
hexdump field by field: 128 bytes, magic and 8 zero bytes at [0,16), directory
`00 00 00 00` at [16,20), version_major 1, version_minor 0, flags 0,
dir_offset 16, dir_length 4, committed_file_length 128 (= the file size, mod 64 = 0),
file_id 0x0123456789ABCDEF, 12 zero reserved bytes. It satisfies every §6.2 gate.

A nice degenerate consistency I want to record: §15.4's example says that at
entry_count = 0 "crc_of_crc_array = 0". CRC-32C of zero bytes **is** 0x00000000,
so the required constant is also the correctly computed value over the zero-byte
array. `[R-CNT-23]`'s special case and the general rule agree rather than merely
coexist, and L27 registers the violation of it.

### Other worked examples I reproduced

Not checksums, but the same discipline. All matched the document:

- §12.3 channel entry `04 74 65 6D 70 0C 00 04 00 00 C0 7F` — 12 bytes, and §7.4's
  layer payload reuses it "byte for byte" at offsets 56–67.
- §7.4 payload: 4 + 34 + 18 + 12 + 13 = 81, no residue, so the sub-record sequence
  is empty; extent length 4 × 20 + ⌈4/2¹⁶⌉ × 4 = 84.
- §11.4: spatial ordinals 0, 1, 8; (300, 700) → tile (1,2), s = 10, in-tile
  (44, 188), ordinal 11,452; planar channel 2 → 2·32 + 10 = 74.
- §14.2: Q = 3, decoded 18, ordinal 5 at [15,18); planar `b` plane 12 bytes,
  ordinal 5 at bytes 10–11; float32 + bool interleaved Q = 5, decoded 30, ordinal
  5 at [25,30).
- §14.3: P = 10 alternating → `55 01`; with fill true → `55 FD` (pad bits 2–7 set).
- §14.5: edge tile (1,1) of E = (5,5), T = (4,4): 16 positions, 1 real, 15
  padding, decoded 32 bytes.
- §17.3 byte-shuffle: `00 00 00 00 00 00 80 00 40 3F 40 40`.
- §15.4: entry_count 1,000,000 → 16 segments (15 full, last 16,960), 64-byte CRC
  array, region 20,000,064; k = 999,999 in segment 15 at segment-relative byte
  339,180; array at [20,000,000, 20,000,064); segment 15 at [19,660,800,
  20,000,000); one full segment = 1,310,720 bytes = 1.25 MiB.
- §15.4: planar C = 4, N = 32 → ordinal 74's entry at [1,480, 1,500); channel 3's
  entries are ordinals 96–127.
- §21.9's Note: 2³² addressed tiles → segment CRC array 2¹⁶ × 4 = 262,144 = 256 KiB;
  2³⁶ → 2²⁰ × 4 = 4 MiB.
- §12.1: bfloat16 1.0 = 0x3F80 from binary32 0x3F800000, stored `80 3F`.
- §9.2's second Note: prior F + 4 + 64 = prior F + 68, and the least multiple of
  64 at or above that is prior F + 128. Correct.

### Register counts, mechanically

I parsed §21.2–§21.5's tables and counted rows and semicolon-separated instances
(a cell reading `—` counting as one, per §21.1):

| Table | Rows | Instances | Labels |
|---|---|---|---|
| §21.2 F | 35 | 56 | 1–10, 12–36 (F11 struck) |
| §21.3 L | 49 | 116 | 1–49 |
| §21.4 T | 26 | 55 | 1–26 |
| §21.5 R | 10 | 50 | 1–10 |
| **total** | **120** | **277** | |

§21.2 says 35, §21.3 says 49, §21.4 says 26, §21.5 says 10, and §21.8 says
"120 conditions over 277 instances". **Every figure matches.** F11's gap is
declared struck by the Note that follows §21.2, so the label set is correct too.

---

## 6. Decoded-content obligations

**What a verifier must decode.** Every stored tile (§9.7). Every user-metadata
document under an assigned encoding (§18.2, and §19.2 places the check "at use of
a record's extent").

**What it must compare against.**

- Decoded byte length against the decoded size derived from declarations alone —
  P·Q interleaved, P·Bᶜ planar numeric, ⌈P/8⌉ packed planar bool (T3, `[R-SER-07]`).
  Never from payload content or an embedded frame field.
- Every padding position against the channel's recorded fill (T4, `[R-SER-05]`).
- Every pad bit of a packed planar bool plane against the plane's fill bit
  (T5). §14.3's Note is careful that pad bits and padding positions are different
  mechanisms: "A plane can have many padding positions and no pad bits".
- Every interleaved bool value byte against {0x00, 0x01} — but only at **real**
  positions: T2's row hands the padding-position case to T4, "the two rows
  together covering `[R-SER-08]`". I checked this partition is exhaustive and
  non-overlapping: `[R-TYP-07]` confines a bool fill byte to 0x00 or 0x01, so any
  out-of-range byte at a padding position necessarily violates T4 as well; there
  is no bool byte that violates `[R-SER-08]` at a padding position without
  violating T4. The division is sound.
- Codec-specific frame and stream constraints: T15–T25.

**What it is permitted to skip.** Nothing outright. It may *decline* — a layer's
or a tile's decode on resource grounds (`[R-ERR-04]`), a document's decode on its
size bound or the frame's declared window (`[R-MTA-09]`), a codec or filter it
cannot execute (`[R-COD-11]`) — and each decline costs it certification and must
be reported as an unchecked requirement. It owes no search for SHOULD deviations
(`[R-CNF-12]`). It checks nothing about slack content (§5.2: "no conformance
requirement applies to it"). And at an experimental-range document encoding it
checks nothing about the document — `[R-MTA-10]` — but must name the record.

§21.7 is what keeps this from being a false promise: a mis-strided filter, an
undisclosed compression dictionary, or simply wrong data produces a file "that
every checksum in §8 certifies". §21.7's definition of *unwitnessed* is stated as
the exact dual of *detectable* and I checked the two quantifiers are genuinely
each other's negation — they are, over the same subject (a condition, not a
requirement), with the same instrument (checks this specification obliges an
actor to perform, deliberately not the register's rows).

One case I traced through §17.4 because §2.3 names it as a cannot-establish
ground: a verifier that "cannot execute a layer's codec or filter". For a
**conforming** verifier this ground is empty in practice, and §17.4 says so
itself — every assigned codec and filter is core, so the position "arises only at
a reserved or experimental value", which is L43/L45, a violation, so the verdict
is *nonconforming* by the priority rule rather than *cannot establish*. The rule
is not wrong; it is aimed at software that would not be a conforming reader
either. I record it as read, not as a defect.

---

## 7. Multi-generation trace

Same layer as §3. Interleaved, N = 4, decoded size 128, index region 84,
directory 109. Each commit follows `[R-LIF-02]`: begin at exactly F, append
payloads and re-emitted index regions, then the complete directory and its CRC,
barrier, pad to the next 64-byte boundary, trailer, barrier.

**G1 — creation.** As laid out in §3. F = 576, claimed 529, **slack 47**.
Verdict: *conforming*.

**G2 — store tile 1.** The stored-tile set changed, so §20.3 step 4 re-emits the
layer's whole tile-index region, "necessarily at a new placement". Appended:
tile 1 [576,704); index′ [704,788); dir₂ [788,897); pad [897,960); trailer
[960,1024). F = 1024.

Live claimants: front 16, tile0 [16,144), tile2 [144,272), tile1 [576,704),
index′ [704,788), dir₂ [788,897), trailer [960,1024) = 657 bytes.
**Slack 367** = old index 84 + old dir 109 + old pad 47 + old trailer 64 + new pad 63.
ΔF = 448 ≥ 128 ✓, mod 64 = 0 ✓. Verdict: *conforming*.

**G3 — supersede tile 0.** Appended: tile 0′ [1024,1152); index″ [1152,1236);
dir₃ [1236,1345); pad; trailer [1408,1472). F = 1472. Claimed still 657 (the same
seven structures, relocated); **slack 815** — the previous 367 plus the old tile 0
(128), the old index (84), dir₂ (109), the old pad (63) and the old trailer (64).
Verdict: *conforming*. The verifier's slack total has now grown to 55% of the
file, which is exactly the signal §5.2 says it is for: "what tells an operator to
compact".

**G4 — compaction.** `[R-WRT-06]`/`[R-WRT-07]`: fresh file_id, creation path,
both barriers, every stored tile's bytes verbatim with its entry crc unchanged,
the index region regenerated because its stored extents moved (offsets new;
lengths, crcs and sentinel entries unchanged; segment CRCs recomputed;
crc_of_crc_array updated). Placed in Appendix G's total emission order —
stored tiles in disk-ordinal order, then the index region, then the directory:

```
[0,   16)  front            [400, 484) index′
[16, 144)  tile ordinal 0   [484, 593) directory
[144,272)  tile ordinal 1   [593, 640) pad  <- slack
[272,400)  tile ordinal 2   [640, 704) trailer     F = 704
```

Claimed 657, **slack 47**. Verdict: *conforming*. 815 → 47 reclaimed, and the
reference arrays are bit-identical (`[R-MDL-02]`).

Two things the trace made concrete that the prose only asserts. First, the
commit cost really is dominated by the index: G2 appended 128 bytes of data and
84 + 109 + 63 + 64 = 320 bytes of everything else. Second, the file's slack total
after G3 is not recoverable from the trailer — no field numbers generations
(§9.3's third Note, §20.4's Rationale) — so a verifier's walk is the only way to
learn it, which is why §5.2 makes reporting it a MUST rather than advice.

---

## 8. Findings

### verifier-01 — OBSERVATION

**§20.3 step 4, `[R-WRT-04]`.** The §14 bar's carve-out is stated with two limbs
in the paragraph that defines the bar, and glossed three paragraphs later as
having only one.

The bar's own paragraph:

> The test is the effect on such a tile, and the list names where that effect
> arises rather than standing on its own: a change that leaves every one of those
> tiles' stored bytes meaning exactly what they meant — a filter whose mandated
> stride makes it the identity (`[R-COD-10]`), or a new padding position whose
> stored byte already holds the fill `[R-SER-05]` fixes — is not what this bars.

Two limbs: an identity filter, and a fill-holding new padding position. The
growth permission below it:

> The bar's carve-out does not reach a growth: it covers a position whose stored
> byte already holds the fill it keeps, not one that ceases to be padding, so
> this is an exception the permission states rather than one the carve-out
> supplies.

"it covers X, not Y" describes the carve-out as consisting of the padding limb
alone. The identity-filter limb has vanished from the description. The shrink
paragraph handles the same problem correctly by incorporating the whole
carve-out before giving one instance of it — "What counts as such an alteration
is the §14 bar and nothing else, **its carve-out included** — a new padding
position whose stored byte already holds the fill `[R-SER-05]` fixes is not one"
— which is why I read the growth sentence as the one that was not updated.

**Why I say this does not move the emittable set.** The conclusion the growth
sentence draws is still true: a growth is permitted by the express exception the
permission states, not by the carve-out, and the identity-filter limb has nothing
to say about a growth either way. And the reading that would move bytes — taking
"it covers a position whose stored byte already holds the fill" as the carve-out's
full extent, and so barring a filter-declaration change on a layer that stores
tiles whose permutation is the identity — is defeated by the governing sentence
above it, which states the test in general terms ("a change that leaves every one
of those tiles' stored bytes meaning exactly what they meant") and says in so
many words that "the list names where that effect arises rather than standing on
its own". The general test governs; the two limbs are instances of it. I checked
what the general test admits that neither named limb does: Appendix G item 5
observes that the byte-shuffle permutation is the identity "where the stride is 1
... and equally where the decoded image is a single group, n = L/s being 1", and I
verified the algebra — the map j·s + i ↦ i·n + j is the identity exactly when
s = 1 or n = 1, since i = 1, j = 0 requires n = 1 and i = 0, j = 1 requires s = 1.
The n = 1 case is a layer with every tile extent 1, and it is reached by the
general test but by neither of §20.3's two named limbs. That the general test has
to do that work is the reason the gloss's incompleteness is worth recording.

What an implementer gets wrong without this: an updater author who reads §20.3
top to bottom and takes the growth sentence as the definition of the carve-out
will treat a filter-declaration change on a P = 1 layer with stored tiles as
barred, and will produce a new file where a commit was available. The resulting
file is conforming under either reading, so nothing a reader must accept or
reject changes.

### verifier-02 — AMBIGUITY

**§5.2 `[R-CNT-21]` and §9.7 `[R-LIF-08]`.** Both passages name exactly two
causes for an incomplete coverage walk. A third exists, licensed elsewhere in the
document, and neither passage accounts for it.

§5.2:

> Where the walk of §9.7 does not enumerate every region's claimants — whether
> because a scope-level rejection ends that scope's enumeration ... or because
> the verifier elected under `[R-CNF-11]` to stop at the first violation — the
> verifier MUST report the total as partial.

§9.7 gives the same pair: "Where the walk does not complete — a scope-level
rejection blocks enumeration, or the verifier stops at the first violation
(`[R-CNF-11]`) — the sum is reported as partial".

Both named causes presuppose a violation. But `[R-ERR-04]` lets a reader — and
§2.3 makes a verifier a reader — decline a conforming file "at the whole file, or
at the narrowest scope whose stated or derived quantities exceed what it can
serve: a layer, a tile, or the record carrying a user-metadata document", and
§21.9's guarantees are floors, not caps, so a layer declaring entry_count = 2⁴⁰
is conforming and declinable. A verifier that declines such a layer cannot read
its tile-index region and therefore cannot enumerate its stored extents. No
violation has been established; the verdict is *cannot establish* (§2.3 lists
resource declines among its grounds); and the walk is incomplete for a reason
that is neither a scope-level **rejection** — §21.9 insists a resource refusal
"MUST be reported as a resource limit and not as a validity error" — nor an
election to stop at the first violation.

Two readings. **(a)** The MUST attaches to the head condition ("Where the walk
does not enumerate every region's claimants"), and the "whether because ... or
because ..." clause is an appositive naming the anticipated causes; the verifier
must report the total as partial. **(b)** The "whether because ... or because ..."
clause is the exhaustive set of triggering causes; a resource decline is not among
them, so the obligation does not fire and the verifier may report its total
without the partial marking.

**I picked (a).** Three things decide it for me. §9.7's parallel sentence puts
its em-dash clause after "Where the walk does not complete", which is plainly a
gloss on the head. §21.6's slack row states the obligation on the general
condition alone — "counted and reported by a verifier — as a partial total — an
upper bound naming what stopped the walk — where its walk did not complete" —
naming no causes. And Appendix H does the same: "reported as partial ... where
its walk did not complete". Reading (b) would also license a verifier to publish
a number that is strictly larger than the file's true slack while presenting it
as the exact total, which §5.2 elsewhere treats as the distinguishing property of
a *partial* total and not of an exact one.

What an implementer gets wrong without this: a verifier that declines a large
layer on resource grounds and reports its slack total unmarked tells an operator
that a conforming file contains more waste than it does, which is precisely the
number §22.3 says "distinguishes a working file from a padded one". §5.2's
further requirement that "a verifier reporting one MUST say which scope or
violation stopped the walk" is satisfiable in this case — the scope is the
declined layer — which is a small sign that the general reading was intended and
the enumeration simply was not updated when resource declines were folded into
`[R-CNF-11]`'s cannot-establish grounds.

Not byte-level: both readings produce the same verdict (*cannot establish*) on
the same file, and the divergence is confined to whether one line of the report
carries the word "partial". No byte a writer may emit, and no accept/reject
outcome, turns on it.

---

## 9. Suspicions I opened and closed

Recorded because a clean lane has to show it looked.

1. **Does the identity-filter limb of §20.3's carve-out reach the n = 1 case?**
   I proved the permutation is the identity exactly when s = 1 or n = 1, and the
   phrase "a filter whose mandated stride makes it the identity" names only the
   stride. Closed against a *byte-level* grading by "the list names where that
   effect arises rather than standing on its own", which makes the general test
   the governing one. Retained as the substance of verifier-01.

2. **Is `[R-CNF-02]`'s "are the cases this text states" a closed count that the
   text falsifies?** I enumerated the writer obligations expressly declared not
   to be file-conformance violations: §6.3's flags rules and §6.2's over-long
   pre-trailer gap. §9.2's barriers are the *other* category (conduct leaving no
   trace in the bytes) and say so — "declared so here on the model `[R-CNF-02]`
   states". §10.3's experimental-value bar and §18.3's `tarn.` key bar are also
   that category, and §2.3 names both sections. I found no third member of the
   stated category. Closed by "and each is declared where it arises rather than
   enumerated here".

3. **The four restatements of the new ignore-lane prohibition, word for word.**
   §2.3 ("an updater's or compactor's copy-forward and set-no-other"), §6.3
   (updater: "MUST copy forward ... MUST NOT clear them, and MUST NOT set any
   other"; compactor: "carries the input's unknown ignore-lane bits into its
   output trailer ... and sets no other"), §20.3 step 6 ("copied forward and no
   other set"), §20.5 `[R-WRT-06]` ("MUST copy the input's unknown ignore-lane
   flag bits forward and set no other"), Appendix G item 8 ("carries its input's
   unknown ignore-lane bits forward instead, setting no other"). They agree.
   "Any other" resolves in all five to "any bit other than the input's set
   ignore-lane bits", which correctly also bars an updater from setting an
   incompat bit. Closed.

4. **Are two MUSTs on `flags` jointly unsatisfiable on some input?** I put the
   §6.3 paragraph's four MUSTs against every input I could construct: an input
   with an ignore-lane bit set (updater copies it — no conflict with the creator
   rule, which binds only "a writer creating a file"); an input with an
   incompat-lane bit set (the updater is a reader first and rejects before
   modifying); a compactor, which does create a file and is expressly excepted
   from flags = 0 in both §6.3 and §20.5; a profile-adopting compactor, which
   Appendix G item 8 excepts on the same terms and then admits is "reproducible
   only modulo its trailer". I found no input on which two of them conflict.
   Closed.

5. **Is a set incompat-lane bit a file-conformance violation while a set
   ignore-lane bit is not?** Yes, and the asymmetry is load-bearing rather than
   accidental: §10.1's four growth vehicles include "**New ignore-lane flag
   bits**" and nothing about the incompat lane, so under format major 1 no
   incompat bit can ever be validly set. F19 registers it as reject-file; §21.6
   records the ignore-lane bit as a non-violation. §2.3's qualifier — "§6.3's
   flags rules **against a set ignore-lane bit**" — is what keeps the creator's
   flags = 0 from being mis-classified as wholly conduct. Closed.

6. **Does an ignored record's extent fall to slack?** Closed against, by §5.2's
   "whatever the record's type" and by `[R-MTA-10]`'s "bytes a certificate covers
   without inspecting are counted and named, never silent". Detailed in §3 above.

7. **Does a file-scope rejection end the whole enumeration, so that any
   reject-file condition forces a partial total?** §5.2's parenthetical about
   discarding already-enumerated claimants is stated for a rejected **layer**
   only. For a file-scope violation the obligation still keys on whether the walk
   enumerated the claimants, and a verifier that continues has enumerated them.
   Both behaviours are licensed ("A verifier MAY stop at the first violation"),
   the verdict is *nonconforming* either way, and the report difference is the
   one `[R-CNF-11]` already contemplates. Closed as no defect.

8. **Is the slack total owed after a §6.2 failure that leaves F derivable?**
   §5.2 exempts the case where "§6.2's ordered validation rejects the file before
   a live trailer is established", justifying it as "there is no F". For a failure
   of, say, the reserved-bytes gate, F is arithmetically available — but §6.2
   requires all the second-tier gates to pass "before acting on the fields
   involved", so no field may be acted on and no live state exists. The
   justification is loosely worded; the rule is unambiguous, and the exemption is
   a "not owed", not a prohibition. Closed as not a defect.

9. **Is `[R-COD-11]`'s cannot-establish ground reachable by a conforming
   verifier?** Effectively no, and §17.4 says why itself. Not a defect — the
   priority rule in §2.3 decides the case cleanly. Closed.

10. **Does §20.3's "Example — the three shapes a commit takes" survive the
    widened drop permission?** A commit whose only effect is dropping an
    MU = 0 / PE = 0 record re-emits only the directory and strands the dropped
    record's extent — shape (c) plus a stranded extent, which (c)'s figure does
    not draw and (c)'s contrast with metadata editing does not contemplate. But
    (c)'s own words, "Only the directory is re-emitted", are true of it, and the
    block is a labelled Example and therefore non-normative under `[R-CNF-01]`.
    Too thin to file. Closed.

11. **Does §5.2's illustrative list of slack — "alignment and slab gaps, the
    pre-trailer pad, and everything an earlier commit superseded" — still cover a
    dropped record's extent, which is abandoned rather than superseded?** The head
    definition governs ("Every byte the live state does not claim is slack") and
    §20.4's table says of the drop "its extent becoming slack" in terms. Closed.

12. **Is §21's register complete over the verifier's domain?** I walked every
    requirement identifier in the document and asked which row records it. Every
    detectable one has a row. The ones with no row have a stated reason:
    `[R-SLB-04]` (subsumed by L41/L42, §16.2's Note), `[R-CNT-18]`'s nesting
    prohibition (no reader-detectable witness in major 1, §7.4's Note),
    `[R-ENC-06]` (states no condition a file can exhibit, §21.7),
    `[R-COD-06]`'s undisclosed dictionary and `[R-COD-10]`'s undetectable strides
    (unwitnessed, §21.7), `[R-WRT-05]`'s byte-identical re-emission (§20.4's
    Rationale: the live state names one generation), `[R-LIF-02]` step 3
    (a trailer re-pointed at an earlier directory is byte-indistinguishable from
    a fresh one). Closed with no omission found.

13. **Do §8.1's exceptions leave any live byte uncovered that the document does
    not name?** No — the front block and unassigned-type record extents, both
    named in §4.5, §8.1 and §22.3. Closed.

14. **Does `[R-CNF-13]`'s "residency exemption applies unchanged" restore a
    verifier's front-block exemption on a foreign-major file?** Closed against, by
    §2.3's verifier definition and F6's row. Detailed in §2 above.

15. **Is the partial total genuinely never an under-count?** Proved for both
    stopping modes, given that "bytes claimed" is a union of ranges rather than a
    sum of lengths — and any counterexample to that would itself be the overlap
    violation. Closed.

---

## 10. Confidence

**Medium-high** that an implementation built from this text alone would
interoperate on the verifier path. The certification procedure, the verdict
priority rules, the coverage walk and its partial-total semantics, the checksum
map, the entry classification table and its structural/well-formed split, the
slab run partition, and the decoded-content obligations are all stated to a
degree I could implement without guessing. Every constant, every worked example
and every register count reproduced exactly, which is not a small thing across
seven checksums, sixteen numeric examples and 120 rows over 277 instances.

Where I found little — extent overlap, alignment, slab invariants, checksum
coverage, the multi-generation trace — I did not find little for want of looking:
I built adversarial layouts for each (an extent straddling its own index region;
a first structure at offset 16 under A = 4096; a planar two-channel slab whose
run boundaries fall inside an apparently uniform stride), computed the exact
slack total at four generations, and derived every checksum constant from the
parameters rather than trusting the table. The two findings I do file are both
about report semantics and gloss, not about bytes, and I say so.

