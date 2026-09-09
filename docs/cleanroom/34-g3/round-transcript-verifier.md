# Cleanroom round 34 — Verifier implementer, working transcript

## 0. Access and disclosure

I read exactly one file: `/Users/robertkleffner/Documents/GitHub/tarn-first-draft/spec/tarn.md`
(4,838 lines, 48,163 words as `wc` reports). It was where the brief said it would be.
I opened no ADR, no `docs/`, no `conformance/`, no `spec/registry.json`, no git history,
and made no network access. Every other file I touched I wrote myself, all of them under
my own scratch directory
`/private/tmp/.../r34-round/scratch/verifier/`:

- `crc32c_verifier.py` — a CRC-32C implementation built from §4.5's parameters alone.
- `appendixA_verifier.py` — re-derives Appendix A's 128-byte file.
- `buildfile_verifier.py` — a byte-exact TARN writer (front block, layer record, index region, directory, pad, trailer).
- `verifier_impl.py` — the conforming verifier, written from §19.1/§19.3/§19.4/§9.7/§7.2/§15.3/§16/§14.5.
- `adversarial_verifier.py` — the adversarial slab/alignment/overlap/padding/gap layouts.
- `trace_verifier.py` — the four-generation trace.
- `edge_verifier.py` — the zero-slack and over-long-gap boundary files.
- `walk2_verifier.py` — the incomplete-walk arithmetic and the unchecksummed-extent case.
- `count_rows.py` — mechanical row and instance counts over §21.2–§21.5.
- Binary artefacts `W1.tarn`, `W7.tarn`.

I did not read the output directory.

**Context I did not ask for.** My runtime placed material in my context before I began: a
project instruction file (`CLAUDE.md`, itself a pointer to `AGENTS.md`), an index of the
maintainer's auto-memory notes with titles referring to this project's harness and to
earlier rounds' findings, a git status with recent commit subject lines naming round 33's
result, and a list of available skills and MCP servers. None of it is the specification. I
disregarded all of it: nothing below rests on it, and I did not open any file it named. I
note its appearance here as the brief requires, without repeating its contents.

---

## 1. Instrument check — do I have a working CRC-32C?

Before trusting any arithmetic I built CRC-32C from §4.5's stated parameters only
(Castagnoli polynomial 0x1EDC6F41, reflected input and output, init 0xFFFFFFFF, final XOR
0xFFFFFFFF, stored little-endian u32). The reflection of 0x1EDC6F41 is 0x82F63B78, which is
the table constant I used; I did not take that value from memory of any library, I derived
it by bit-reversing the stated polynomial and then confirmed the whole construction against
the document's own check vector.

| Constant | Document | Computed | |
|---|---|---|---|
| CRC-32C(`"123456789"`) | 0xE3069283, stored `83 92 06 E3` (§4.5) | 0xE3069283, `83 92 06 E3` | ✓ |
| CRC-32C(zero bytes) | 0x00000000 (§4.5) | 0x00000000 | ✓ |
| CRC of a full all-sentinel segment | 0xEECB3BB2 (§15.4, App. B) | 0xEECB3BB2 over 2¹⁶ × 20 = 1,310,720 bytes | ✓ |
| §7.4's 4-sentinel entry array (80 bytes) | 0x80A34955, stored `55 49 A3 80` | 0x80A34955 | ✓ |
| §7.4's `crc_of_crc_array` over that 4-byte array | 0xC4EE982E, stored `2E 98 EE C4` | 0xC4EE982E | ✓ |
| Appendix A trailer CRC over trailer [0,60) | 0x402F157E, stored `7E 15 2F 40` | 0x402F157E | ✓ |
| Appendix A directory CRC over 0 bytes | 0x00000000 | 0x00000000 | ✓ |

Every checksum constant the document states that is computable without an external codec
reproduces. The ones I could **not** reproduce, and why: the zstd frame magic `28 B5 2F FD`
(§17.2) is a frame marker, not a checksum, and pinning it needs RFC 8878; the lz4 decoded-size
cap `0x7E000000` (§17.2) is a bound, not a checksum; and nothing in §8.1's map is a hash
other than CRC-32C, so there is no second algorithm to check.

Appendix A's file also decodes field-for-field: magic `8A 4E 52 41 54 0D 0A 1A`,
version_major 1, version_minor 0, flags 0, dir_offset 16, dir_length 4,
committed_file_length 128 (= 128 mod 64 = 0), file_id 0x0123456789ABCDEF, twelve zero
reserved bytes, and dir_offset + dir_length = 20 ≤ F − 64 = 64. Slack = 128 − (16 + 4 + 64)
= 44, exactly the "44 bytes of slack" §5.1's Example states.

---

## 2. The certification procedure, as an ordered algorithm

I implemented this and ran it. What follows is the algorithm the document determines, with
the verdict vocabulary at each point.

### 2.1 The verdict trichotomy and its decision rule

§2.3 `[R-CNF-11]` gives three verdicts and, read with `[R-CNF-12]`, a total decision rule:

1. **If the traversal established any violation → *nonconforming*.** "An established
   violation takes priority: a verifier that has established any violation reports
   *nonconforming*, however many requirements it was unable to check."
2. **Else, if some requirement is one it was unable to check on a capability or resource
   ground → *cannot establish*.** "*cannot establish* is available only to a traversal that
   established no violation." A verifier MUST NOT certify a file it reports that way.
3. **Else → *conforming*.**

Step 3 is by elimination — the document nowhere states positively "reports *conforming*
when…" — but the elimination is airtight because §2.3 says a verifier "reports one of three
verdicts" and gives necessary conditions for the other two.

Two report obligations sit **beside** the verdict and never move it:

- **Unchecked requirements.** "A verifier MUST report each requirement it was unable to
  check on a capability or resource ground, naming the requirement and the ground,
  whichever of the three verdicts it reports; that per-requirement report constrains the
  report and not the verdict." So a *nonconforming* verdict still carries the
  unable-to-check list.
- **Unexamined scopes.** "A verifier MAY stop at the first violation it finds; one that
  does MUST report each scope it did not examine as *unexamined*, which is not a finding
  that the scope is clean. *Unexamined* is neither a verdict nor *cannot establish*."

Grounds for *cannot establish* that §2.3 names ("as when", so illustrative, not closed):
a format major it does not implement; a record carrying MU = 1 with a type it does not
implement (§21.6); inability to execute a codec or filter (`[R-COD-11]`); a layer's or a
tile's decode declined on resource grounds (`[R-ERR-04]`, `[R-SER-05]`, `[R-SER-08]`); and
a declined user-metadata document decode (`[R-MTA-09]`). §21.9 adds a whole-file resource
decline, which the list does not name but plainly reaches.

One ground is, for a *conforming* verifier, unreachable, and the document says so itself:
`[R-COD-11]`'s codec inability. Every assigned codec and filter is core (§17.2, §17.3), so
"software unable to execute an assigned codec or filter is not a conforming reader
(`[R-CNF-03]`)"; and at a reserved or experimental value the verifier establishes L43 or
L45, which is a violation, so §2.3's priority rule fixes *nonconforming*, not *cannot
establish*. I opened this as a suspicion and closed it: `[R-COD-11]`'s own third sentence
states the vacuity. **Not a finding.**

`[R-CNF-12]` also fixes what a SHOULD deviation does: nothing. "§21's register enumerates
MUST-level conditions only, and a verifier reports a SHOULD deviation as an advisory that
does not bar certification. A verifier owes no search for one." So the whole of §21's
register — 120 rows — plus the verifier-only checks Appendix H lists is the certification
surface, and `[R-CNT-03]`'s zeroed gaps, `[R-TYP-10]`'s zero fill default, `[R-CNT-26]`'s
version_minor floor, `[R-ENC-14]`'s NFC and `[R-CNT-09]`'s 64 KiB discovery window are
advisories the verifier reports where it happens to see them.

### 2.2 The ordered walk

**Step 1 — size.** Obtain the transport-authoritative F (`[R-CNT-10]`). F < 128 is F5,
"decided from F alone and needing no other byte of the file" (§19.1 step 1, `[R-CNT-27]`).
Verdict *nonconforming*; no slack total is owed, because no live trailer was established.

**Step 1b — front signature block.** A verifier holds no `[R-CNT-04]` residency exemption.
§2.3 defines a verifier as one that "additionally checks every file-level requirement —
including those ordinary readers are exempted from", F6's row spells it out ("a verifier
holds no such exemption (§2.3)"), and Appendix H repeats it. So the block is compared for
byte equality before other processing; mismatch is F6 (and, if byte-reversed, F1's
front-block instance, which §21.1 records as the narrower row).

**Step 2 — trailer, in §6.2's fixed order.** magic (F8) → trailer CRC (F14) → version gate
(F18 for version_major 0; an unimplemented major is not a violation) → then, those gates
passed, all of: flag gates (F19); committed_file_length = file size (F17) and a multiple of
64 (F13); dir_offset ≥ 16 (F9); dir_length ≥ 4 (F16); dir_offset + dir_length ≤ F − 64
(F10, a declaration-derived sum under `[R-ENC-04]`); file_id ≠ 0 (F12); reserved bytes zero
(F15). Any failure is reject-file.

The order matters for the foreign-major case. §2.3 `[R-CNF-13]` fixes which conditions
*reach* a file declaring a major other than 1, and §21.2's preamble derives the answer:
F8, F14, F6, and both of F1's instances — and no other row. I re-derived this independently
against `[R-CNT-24]`, which fixes permanently only the trailer magic at F − 64, version_major
and version_minor at F − 56, the CRC-32C at F − 4 over [F − 64, F − 4), and the front
signature block. That leaves the 48 trailer bytes [12, 60) redefinable — so dir_offset (at
trailer offset 16), dir_length (24), committed_file_length (32), file_id (40), flags (12)
and the reserved bytes (48) are all format-major-1's, and F9/F10/F12/F13/F15/F16/F17/F19 do
not reach. F5 does not reach because its 128-byte floor is *derived* from dir_offset ≥ 16,
dir_length ≥ 4 and a 64-aligned F, all of which are major 1's. The derivation is correct,
including §2.3's Note that F14 reaches although it consumes redefinable bytes as CRC input.

So a verifier implementing only major 1, handed a conforming-looking major-2 file: it runs
F6/F1, F8, F14, and then reports *cannot establish*, naming "every format-major-1 structural
requirement" and the ground "format major 2 not implemented". If any reaching condition
fails, it reports *nonconforming* — "whatever major the file declares and whether or not it
implements that major", because the broken invariant is one that major shares.

**Step 3 — directory.** Fetch [dir_offset, dir_offset + dir_length) and verify the terminal
CRC before any other use (F20). A failure here is reject-file **and** ends the record walk,
which is the first place a partial slack total arises: the walk has enumerated the front
block, the directory and the trailer, and nothing else.

**Step 4 — record walk.** §7.2 framing (F29, F24), MU gate for unknown top-level types
(F35, and F36 for the reserved range), multiplicity (F34), extent-slot validity for
non-layer top-level records (F30, F31, F32), and the user-metadata framing rules (F21, F22,
F23). Build the layer-name namespace over raw name bytes — §19.1 step 4 is explicit that
uniqueness is decided first, over raw bytes, "whether or not each name is itself
well-formed", and that a layer record whose name field does not fit its inline_length
contributes no name and is instead L23 at layer scope. F4 is the duplicate.

**Step 5 — per layer, §19.3's full validation** before any use of the layer's declarations:
extent slot, the §7.4 constraint set, exact parse and sub-record walk, name rules, the u64
value domain, the value sets of §11.4/§12.2/§14.1/§15.1/§17.2/§17.3, bool fill, the lz4
declaration cap, the geometry floor and arithmetic, the 2⁶³−1 ceiling on every designated
derived quantity, and the index cross-checks computable without I/O. All decidable from the
resident directory and F: "layer access performs no fetch".

**Step 6 — index chain**, per layer: crc_of_crc_array over the fetched segment-CRC array
(L37), then each segment CRC over its entries (L38). Both reject-layer, "although their
detection point is tile use" (§19.2).

**Step 7 — per entry, §15.3's classification.** Six *structural* rows (T6, T7, T10, T8,
T11, T12/T9) yield no usable extent and contribute no claimant. Everything else that is
non-sentinel contributes its extent as a claimant.

**Step 8 — per stored tile:** entry crc over the stored bytes (T1); codec-1 length equality
(T14); decode (T24, T25, and the codec-specific header rows T17–T23); decoded size (T3);
then the decoded-content obligations T4 (padding positions), T5 (pad bits) and T2
(interleaved bool bytes).

**Step 9 — per user-metadata extent:** terminal CRC (R2), then, at an assigned encoding,
the frame constraints (R4) and the document content rules (R3, R5–R10) and member ordering
(F27 / L48). At an experimental-range encoding, nothing: `[R-MTA-10]` withdraws every
content rule, "certification is unaffected", and the verifier instead **reports** the record
it ignored, naming owning scope, encoding value and stored extent length.

**Step 10 — the certification-tier checks** that no reader owes: F7 (a structure in the
pre-trailer gap), F33 / L18 (overlap), F25/F26/L46/L47 (flag bits), F28/L49 (registered
type's stored bits against §7.3), F36/L25 (reserved-range types), L40/L41/L42 (alignment
and slab), and the coverage partition and slack total.

**What is reported when a check cannot be run.** Three distinct things, and the document
keeps them apart cleanly: an *unchecked requirement* (capability or resource ground; named
with its ground; does not by itself make the file nonconforming; fixes the verdict at
*cannot establish* if nothing was established); an *unexamined scope* (only after electing
to stop early; not a finding that the scope is clean); and a *partial slack total* (§5.2).
`[R-ERR-04]` adds that a resource refusal "MUST be reported as a resource limit and not as
a validity error".

---

## 3. The coverage walk, on a file of my own construction

### 3.1 W1 — a conforming file, built byte-exactly

I built §7.4's worked layer for real: layer `sst`, rank 1, dimension `x` with extent 100 and
tile extent 32, one interleaved float32 channel `temp` with fill 0x7FC00000, codec 1, filter
1, no alignment and no slab. G = ⌈100/32⌉ = 4, so N = 4 and entry_count = 4; P = ∏Tᵢ = 32;
Q = ΣBᵢ = 4; decoded size = P·Q = 128 bytes per tile. My encoder produced an inline payload
of **81 bytes**, which is exactly the figure §7.4's Example states, and my index region came
to 4 × 20 + ⌈4/2¹⁶⌉ × 4 = **84 bytes**, matching `[R-CNT-17]`'s formula and the Example's
"extent slot of length 4 × 20 + ⌈4 / 2¹⁶⌉ × 4 = 84".

All four tiles stored. Tile 3 covers positions 96–127, of which 100–127 are padding
positions (§11.3), each carrying the fill bytes `00 00 C0 7F` per `[R-SER-05]`.

```
front             [0, 16)        16
tile 0            [16, 144)     128   crc 0xF8118D31
tile 1            [144, 272)    128   crc 0xFDF96FE9
tile 2            [272, 400)    128   crc 0x99870149
tile 3            [400, 528)    128   crc 0x1909AA1A
tile-index region [528, 612)     84   (4x20 entries + one 4-byte segment CRC)
directory         [612, 721)    109   (one 105-byte layer record + 4-byte CRC)
pre-trailer pad   [721, 768)     47   -- slack
trailer           [768, 832)     64
F = 832;  832 mod 64 = 0;  dir_offset + dir_length = 721 <= F - 64 = 768
```

**The partition.** Every byte of the live committed state belongs to exactly one of: the
front signature block; a stored-tile extent; a record extent; the directory; the trailer
(`[R-CNT-02]`). Claimants here: front 16 + four stored extents 512 + the tile-index region
84 (which enters "once, as that record's extent" — §9.7 is explicit that a layer record's
extent slot addresses its index region, so the region is not a second claimant beside the
record) + directory 109 + trailer 64 = **785**.

**The slack total.** F − 785 = **47**, which is exactly the pre-trailer pad, and the walk
enumerated every region's claimant, so the total is exact, not partial. Verdict:
***conforming***.

**Which bytes are certified, which counted-but-unconstrained, and whether any byte can be
neither.** Three classes, and the third is the one worth naming:

- **Certified** — covered by a checksum §8.1's map states *and* by content rules: the
  trailer (its own CRC), the directory (its terminal CRC), each index region (segment CRCs
  under crc_of_crc_array), each stored tile (its entry's crc, plus §14.5/§14.3/§14.2's
  content obligations), and each user-metadata extent under an assigned encoding (terminal
  CRC plus §18.2's frame and document rules). The front block is certified by equality, not
  by checksum.
- **Checksummed but content-unconstrained**: a user-metadata extent under an
  experimental-range encoding. `[R-MTA-10]` withdraws every content rule there; `[R-SEC-04]`
  says so in terms — "the CRC detects corruption and authenticates nothing (§4.5), so a
  certificate covers those bytes uninspected — which is why `[R-MTA-10]` makes the
  verifier's report name each such record".
- **Neither checksummed nor content-constrained, yet inside the live state**: the extent of
  a record of a type this specification has not assigned. §8.1's last row states "none —
  the bytes are opaque (§7.2)". So **no**, not every live structure is covered by a
  checksum, and the document says so three times (§4.5, §8.1, `[R-SEC-04]`).

I built that case to be sure it is reachable in a *conforming* file. **W7**: two layers,
layer A carrying an experimental-range sub-record (type 0x8001, MU = 0, PE = 1) whose extent
is 38 bytes of opaque payload. §21.6's table makes an experimental-range MU = 0 record a
defined non-violation; `[R-CNT-18]` gives it ignore-record at layer scope; §9.7's walk
reaches it "through its records and their sub-records" and claims its extent. F = 1600, 14
claimants covering 1,538 bytes, slack 62, walk complete, verdict *conforming* — with 38
bytes of the certified live state covered by no checksum at all.

**Can a byte be neither claimed nor slack?** No, and the document's own Note in §5.2 makes
the argument: "The live committed state is *defined* as the front block plus what a complete
coverage walk reaches, and `[R-LIF-08]` makes every byte that walk misses slack — so
'belongs to no class' describes nothing, and a register row for it would be a row no file
could exhibit." And there are no bytes at or above F in a conforming file: F17 registers
committed_file_length ≠ the transport-authoritative size as reject-file, and `[R-LIF-04]`
requires the physical length to equal committed_file_length after any commit. So
[0, F) partitions into live state ∪ slack, exhaustively, and that is the whole file.

**Boundary cases I built to test the universals** (the brief's shape 8):

- *Slack = 0 is reachable.* I added a top-level user-metadata record with a 27-byte extent
  chosen so that the directory ends exactly on a 64-byte boundary at F − 64: F = 832,
  pre-trailer pad 0, every byte claimed, **slack total 0 (exact)**, verdict *conforming*. A
  verifier that treats "report the total" as "report a positive number" is wrong; 0 is a
  total.
- *The smallest conforming file* (Appendix A, 128 bytes, zero layers, empty directory):
  claimants front 16 + directory 4 + trailer 64 = 84, slack 44, walk complete, *conforming*.
  §21.6 records zero layers as a defined non-violation; §15.4's closing Example records that
  at entry_count = 0 "there is no region at all", extent slot (0, 0), crc_of_crc_array = 0,
  so an empty layer contributes no claimant either.
- *A conforming file no conforming commit produces.* I built a file whose pre-trailer gap is
  192 bytes rather than the 0 that `[R-LIF-02]` step 5's pad would leave. `[R-CNT-05]` says
  flatly "a longer gap is conforming, and no conforming commit produces one", and
  `[R-CNF-02]` lists exactly this as one of three writer obligations whose violation is
  expressly not a file-conformance violation. My verifier certified it, counting all 192
  bytes as slack: verdict *conforming*, slack 192 exact. This is the sharpest illustration
  in my lane of the conduct/predicate split — the file is conforming, and any writer that
  emitted it broke a MUST as an actor.

### 3.2 A walk that does not complete

§5.2's operative criterion is enumeration: "Where the walk of §9.7 does not enumerate every
region's claimants, the verifier MUST report the total as partial", and "A partial total is
F less the bytes claimed by the claimants the walk did enumerate — an upper bound on the
file's true slack, never an under-count", and the verifier "MUST say which scope or
violation stopped the walk".

I ran three incomplete walks.

**(a) A layer rejected, W7 with layer B rejected.** §5.2: "A rejected layer's claimants are
not enumerated, whether or not the rejection impeded reading them". Layer B's claimants are
four stored extents of 128 plus an 84-byte index region = 596 bytes. Enumerated claimants
drop from 1,538 to 942, and the partial total is 1600 − 942 = **658**, against a true slack
of 62. The upper-bound property holds (658 ≥ 62), as `[R-CNT-21]` promises, and the report
must name "layer scope / layer B" as the stopper.

**(b) W3a — alignment A = 512 declared, one stored tile at offset 3080.** L40 fires
(3080 mod 512 = 8). My first implementation reported the total as *exact*; that is wrong,
and re-reading §5.2 corrected me: L40 is named there among the rejections "the walk itself
established", so the layer's claimants — 8 × 128 + 164 = 1,188 bytes — are discarded and the
report becomes a partial total of 3236 + 1188 = **4,424**, naming "layer scope / L40". I
record the error because it is exactly the trap the rule exists to close: a verifier that
keeps the claimants it gathered before rejecting the layer under-reports slack, and §5.2
forbids an under-count.

**(c) The directory CRC fails (F20).** A live trailer *is* established, so the total is
owed, but the record walk never runs. Claimants: front 16 + directory dir_length + trailer
64. Partial total = F − (80 + dir_length), naming "file scope / F20". §5.2's exemption —
"Where §6.2's ordered validation rejects the file before a live trailer is established there
is no F and no live state to walk, so the total is not owed at all" — does **not** reach
this case, and rightly: the trailer validated.

Two cases that explicitly leave the walk **complete**, both of which I exercised:

- *A declined tile decode.* "a tile's or a document's decode declined leaves the walk
  complete, that claimant being enumerated from its index entry or extent slot." I ran W1
  with decoding suppressed: the four stored extents are still claimants (they come from the
  index entries, before any payload work), slack stays 47 exact, and the verdict falls to
  *cannot establish* with `[R-SER-05]` reported unchecked on a resource ground for each tile.
- *A structural-ground entry.* "it contributes no claimant, the walk passes over it, and the
  bytes of the file it nominally addresses fall to slack where no other claimant claims
  them." So a T8 entry (offset < 16) or a T10 entry (length 0) removes a claimant, and the
  slack total goes **up** while the walk stays complete.

Those two are the tile cases §5.2 glosses. There is a third class it does not gloss, and
resolving it took me longer than it should have — see **verifier-02** below.

---

## 4. Extent overlap, alignment, and slab invariants, on adversarial layouts

I did not take these in the abstract; I built files.

### 4.1 Slab — W2, an interleaved layer, E = 256, T = 32, N = 8, S = 4, A_slab = 64

§16.2 `[R-SLB-02]`: "Runs partition each contiguous block of disk ordinals independently:
for an interleaved layer the single block [0, N)". So two runs, [0, 4) and [4, 8). Tile 2 is
a sentinel; every other tile is stored, decoded size 128.

Conforming placement: run 0 = tile 0 @ 64, tile 1 @ 192, tile 3 @ 320 — sentinel 2 is
transparent to run continuity per `[R-SLB-03]` ("Sentinel tiles are transparent to run
continuity: they occupy no bytes and do not break packing"), so tile 3's offset must equal
tile 1's offset plus tile 1's length = 192 + 128 = 320, with no gap where tile 2 "would have
been". This is §16.2's own worked Example, and my file reproduces it. Run 1 = tiles 4–7 at
448, 576, 704, 832; 448 mod 64 = 0. Verdict *conforming*, slack 100 exact.

Then three adversarial variants:

- **A 64-byte gap in run 0** (tile 3 moved to 384): L41 fires with condition "gap".
  In my construction the displacement also collided tile 3's extent with tile 4's, so L18
  fired as well and the total went partial — an unintended but instructive demonstration
  that a placement error and an overlap are separate rows at separate scopes.
- **Run 1's first stored tile at 456** (not 64-aligned): L42 fires, "A slab run's first
  stored tile's offset is not a multiple of A_slab". Note that only the *first* stored tile
  of a run carries the alignment obligation; the interior is fixed by packing.
- I also confirmed by reading that a run with no stored tiles "imposes nothing"
  (`[R-SLB-03]`), and that entries §15.3 classifies reject-tile on a structural ground are
  transparent to run continuity while an entry failing only its stored bytes' crc is not —
  that asymmetry is stated three times (§15.3, §16.2, L41's condition cell) and is
  consistent everywhere.

### 4.2 Alignment — W3, A = 512

`[R-SLB-01]`: "every stored tile's offset satisfies offset mod A = 0". Every stored tile,
not only those a commit adds. My conforming variant placed all eight at multiples of 512
(slack 3,236 — alignment is expensive, which is the point of §5.2's "the verifier's slack
total, where its walk completes, is what surfaces the waste"). Moving one to 3080 raised
L40.

An important scoping point I checked rather than assumed: does L40 range over *every*
non-sentinel entry, including a structurally malformed one whose offset happens not to be
aligned? No. §15.3: such an entry "contributes no stored extent to the *verifier* rows,
which bind over well-formed entries' extents only", and the alignment and slab rows are
among the *verifier* rows in §15.3's table. So a T8 entry with offset 8 does not also
produce L40. That closes cleanly.

`[R-CNT-16]` and L20 make A ≠ 0 with S ≠ 0 a layer-scope error, so the two invariants never
apply together, and my implementation branches on that.

### 4.3 Overlap

`[R-CNT-13]` splits overlap three ways and the walk must too: an *intra*-layer overlap,
"including a stored extent overlapping its own layer's index region or sub-record extents",
is reject-layer (L18); "any overlap across layers or touching another scope's structures" is
reject-file; and "any overlap between two structures neither of which belongs to a layer" is
reject-file (F33). Readers are not obliged to detect any of it: "which requires
whole-directory knowledge".

F33's condition cell resolves the boundary case I would otherwise have had to guess at: a
claimant reaching the front block or the live trailer is caught by the bounds rows
(F9/F10, F30/F31/F32, L15/L16/L17, T8/T9) rather than by the overlap row — "the half-zero
rows F30 and L15 among them, since a record extent slot of (0, N) with N nonzero reaches the
block through its zero offset and is theirs rather than F31's or L16's". I checked each of
those bounds rows exists and reaches the case; they all do.

### 4.4 A structure in the pre-trailer gap — W5

`[R-CNT-05]`: "A verifier MUST treat a structure in that gap as a validity error at file
scope, and counts the rest as slack." I placed a user-metadata record's extent eight bytes
past the directory's end. F7 fires, verdict *nonconforming*. The contrast with §3.1's
192-byte empty gap is the whole content of `[R-CNT-05]`: the gap's *length* is unconstrained
and its *content* is unconstrained, but a claimed structure there is a file-scope violation.

---

## 5. Checksum obligations

**Which structures are covered by which checksum** (§8.1, and I verified every one of them
is actually reachable and checkable in my built files):

| Structure | Checksum | Verified how |
|---|---|---|
| Front signature block | none — byte equality | equality against the 16-byte constant |
| Trailer | trailer [60, 64) over [0, 60) | computed, compared |
| Directory region | final 4 bytes over the preceding dir_length − 4 | computed, compared |
| Tile-index region | segment CRC array (itself under crc_of_crc_array) over entries per segment | two-level: crc_of_crc_array over the array, then each segment CRC over its entries' bytes as stored |
| Stored tile | the crc field of its index entry | computed over [offset, offset + length) |
| User-metadata extent | final 4 bytes over the preceding bytes as stored, before decoding | computed, compared |
| Extent of an unassigned-type record | **none** — opaque | not checkable |

**Is every live structure covered by one?** No, and the exception is exactly the last row.
§4.5 states the whole accounting: every field is covered by exactly one checksum, "excepting
the front signature block (a constant whose check is equality), the terminal checksum fields
of §8.1's map — the trailer, directory-region, and user-metadata checksum fields — which are
verified by comparison and covered by no further checksum, and the extent of a record of a
type this specification has not assigned, which §8.1's map covers by no checksum at all."
The interior checksum fields — segment CRC arrays, entry crc fields, crc_of_crc_array — are
"both comparison-verified and covered by exactly one further checksum". I traced the chain
on W1: entry crc → covered by its segment CRC; segment CRC array → covered by
crc_of_crc_array; crc_of_crc_array → inside the layer record → covered by the directory CRC;
directory CRC → terminal. §8.2's stated chain of trust (trailer → directory → per layer
crc_of_crc_array → segment CRC array → index segment → index entry → stored tile) is exactly
what my implementation walks, in that order.

**Constants reproduced / not reproduced** — see §1 above. All seven computable ones
reproduce; the two I could not check locally (zstd frame magic, lz4 size cap) are not
checksums.

---

## 6. Decoded-content obligations

**What a verifier must decode.** §9.7 is flat about it: "A verifier that certifies decodes
every stored tile, whatever content obligations §14 places on the layer: §21.4's codec rows
are file-conformance violations, and a verifier MUST NOT certify past a violation it has not
looked for; one that declines a tile's decode on resource grounds reports that check unmade
and cannot certify." I read the "whatever content obligations §14 places on the layer" as
answering exactly the question I had: a layer with no padding positions, no pad bits and no
bool channels still gets every tile decoded, because T3, T24 and T25 need the decode
regardless.

It must also decode every user-metadata document under an **assigned** encoding —
`[R-MTA-09]` says a verifier that declines "cannot establish that document's conformance and
MUST NOT certify the file", which only makes sense if decoding is otherwise owed. §19.2's
fourth tier says the same from the reader side: "at use of a record's extent: that extent's
CRC and the content rules of the document it carries — those §18.2 attaches at its encoding".

**What it must compare against.**

- Decoded length against the *declared* decoded size (`[R-SER-07]`): P·Q interleaved,
  P·Bᶜ for a planar numeric channel, ⌈P/8⌉ for a packed planar bool plane — "a function of
  the layer's declarations alone … never of payload content". I re-derived §14.2's worked
  examples and they hold: T = (2, 3), P = 6, channels uint8 + uint16 → Q = 3, decoded size
  18, ordinal 5's sample at bytes [15, 18); planar `b` is 12 bytes with ordinal 5 at 10–11;
  float32 + bool interleaved → Q = 5, decoded size 30, ordinal 5 at [25, 30) with the bool
  as the single byte at 29.
- Padding-position content against the channel's recorded fill (`[R-SER-05]`, T4). I built
  the violation: W1's tile 3 has 28 padding positions; writing `DE AD BE EF` at each raised
  28 T4 findings. §14.5's own Example — extents (5, 5), tile extents (4, 4), the edge tile
  at (1, 1) holding one real position and 15 padding positions, 32 bytes with values 1–15
  each `CD AB` for fill 0xABCD — checks out arithmetically.
- Pad bits against the plane's channel's fill bit (`[R-SER-03]`, `[R-SER-05]`, T5). §14.3's
  Example verifies: P = 10, values alternating true from ordinal 0, byte 0 = 0x55 (bits 0–7
  = 1,0,1,0,1,0,1,0 LSB-first = 0x55), byte 1 = 0x01 with fill false and 0xFD with fill
  true (pad bits 2–7 set = 0xFC, plus bit 0 = 0x01).
- Interleaved bool bytes against {0x00, 0x01} (`[R-SER-08]`, T2) — and only at *real*
  positions; T2's own row splits the padding case off to T4 ("the same byte at a padding
  position is T4's, the two rows together covering `[R-SER-08]`").
- Codec-1 stored length against the decoded size (`[R-COD-04]`, T14), "checkable from the
  entry and the layer record alone, before any payload fetch" — I implemented it there.
- The codec-specific header rows T17–T23, and exact consumption (T24) and well-formedness
  (T25) for every codec.

**What it is permitted to skip.**

- Slack content entirely: "Slack has no internal structure this specification defines, its
  content is unconstrained, and no conformance requirement applies to it" (`[R-CNT-21]`).
  It counts it and reports the number; it does not inspect it.
- The extent of an unassigned-type record: opaque by §7.2 and covered by no checksum.
- The *content* of a user-metadata document under an experimental-range encoding —
  `[R-MTA-10]`, and §9.7 says the walk asks nothing of it: "no rule attaches to its content
  …, so there is no violation there to look for, and what the verifier reports instead is
  that rule's subject." It must still check the record's framing, its extent slot, the
  encoding byte's value set, and the extent's terminal CRC. Encoding 0 and reserved-range
  values stay violations (R1).
- §9.6's backward probe. §9.6 names "Recovery tools and verifiers" as the actors who run it,
  but for a verifier "the probe is diagnosis — which commit state is recoverable — not a
  finding about the file it was given", and "no verdict turns on the probe". §9.7's Note
  seals it: "Nothing here enumerates prior commits." My verifier does not probe.
- A SHOULD deviation is not hunted for (`[R-CNF-12]`).

**What it may decline, at the price of certification.** Anything above §21.9's minimum
guarantees, at "the narrowest scope whose stated or derived quantities exceed what it can
serve" or any scope containing it. Each decline is an unchecked requirement, reported as a
resource limit, and bars *conforming*.

---

## 7. A multi-generation trace

One file_id, three generations, then a compaction. Layer A: rank 1, x extent 100, tile
extent 32, one interleaved float32 channel, fill 0x7FC00000. Layer B the same shape. I
verified after each step with the same implementation.

| Step | Operation | F | Claimed | Slack | Walk | Verdict |
|---|---|---|---|---|---|---|
| G1 | **create** — layer A, four stored tiles | 832 | 780 | 52 | complete | *conforming* |
| G2 | **append** — add layer B, two of four tiles stored | 1,472 | 1,220 | 252 | complete | *conforming* |
| G3 | **update** — supersede A's tile 1 | 1,984 | 1,220 | 764 | complete | *conforming* |
| G4 | **compact** — fresh file_id 0xFEEDFACECAFEBEEF | 1,280 | 1,220 | 60 | complete | *conforming* |

The slack accounting reconciles by hand at every step, which is the test that the coverage
rules are consistent:

- G1 → G2 turns G1's directory (104) + pad (52) + trailer (64) = 220 into slack, and adds
  B's two payloads (256), B's index (84), and a two-record directory (204). 52 + 220 − 20
  (the new pad being 20 rather than 52) … more simply: F − claimed = 1472 − 1220 = 252, and
  252 = 220 (G1's superseded tail) + 32 (G2's own pad). This is §20.3's shape (a): "A's
  record is carried into dir₂ byte-identically, extent slot and all, so it still addresses
  A's original index. The slack is the old directory, pad and trailer — sized by the file's
  *layer count*, never by any layer's data."
- G2 → G3 is shape (b): A's stored-tile set changes, so "that layer's tile-index region
  [is] re-emitted in full — entry_count entries plus the segment CRC array — necessarily at
  a new placement (`[R-LIF-01]`)". The superseded payload (128) and the superseded index
  (84) join the superseded directory tail. Claimed stays at 1,220 because the file's live
  content is unchanged in size; slack rises from 252 to 764. §20.3's Note is exactly right
  that "A commit's cost is dominated by its index, not its data" — the 84-byte index
  re-emission here would be 20 MB at 10⁶ tiles.
- Every commit's F rose by at least 128 (deltas 640 and 512), as `[R-LIF-02]` forces and
  §9.2's second Note derives from `[R-CNT-06]` (dir_length ≥ 4, dir_offset ≥ prior F,
  dir_offset + dir_length ≤ new F − 64, F a multiple of 64 ⇒ at least prior F + 128).
- G4 compaction: output claims the same 1,220 bytes, slack falls to 60 (its own pad alone),
  and F drops from 1,984 to 1,280. I verified `[R-WRT-07]`'s content promise directly: every
  index entry's crc is bit-identical between input and output, so "every stored tile's bytes
  verbatim" holds, and the reference arrays are equal. The output carries a fresh file_id
  ("a new draw under §9.3's randomness advice, not merely a value compared against the
  input's"), and B's index region is regenerated because its stored extents moved while A's
  slot is merely re-pointed — which is §20.5's own Example, and my placement moved both, so
  both were regenerated.

Two things about compaction I read carefully rather than assumed, because they bear on what
a verifier sees:

1. A compactor that *copies* an index region (because none of its stored extents moved) never
   classifies its entries, so a structurally malformed entry travels into the output
   unnoticed. §20.5 says so deliberately: `[R-WRT-09]`'s checks "reach the index chain and
   each stored tile's entry crc rather than an entry's own value domain", and that "bounds
   how far a compactor goes looking, not what it owes on what regenerating the region has
   already put in front of it". A compactor that *regenerates* the region must meet the
   entry, and `[R-WRT-06]` then obliges refusal. Consistent, and certifying the whole file
   remains the verifier's office (§20.1).
2. I suspected `[R-WRT-09]`'s "each relocated extent's checksum, including every stored
   tile's entry crc" of a quantifier defect — is the entry-crc duty universal, or restricted
   to relocated extents? The paragraph it sits in decides it: "A compactor's verification
   depth follows reliance over everything it carries: it relies structurally on **every
   structure it copies**, so it MUST verify each link of the chain". Universal. Closed.

**Verification depth of an updater** (`[R-WRT-03]`), which I also implemented as a check on
my trace: "the trailer and the full directory always — re-emission (§20.4) relies on every
directory byte — plus §19.3's layer validation for every layer whose record, index, or
extents the commit modifies, and the §19.4 index chain for every segment whose entries the
commit reuses." My G3 validated A fully (its index is re-emitted) and B not at all beyond
the directory, which the rule permits.

**The closed list of what a commit may do to a layer that stored a tile** (§20.3 step 4). My
G3 changed nothing declarative, so I read the list rather than exercised it. I enumerated
the transitions a slab-or-alignment declaration can make and matched each to a verb:

| Transition | Verb | Provided for below? |
|---|---|---|
| none → declared | *declared* | yes — "a slab declaration declared, changed or kept has its invariants re-established … or is cleared"; and for alignment, "an aligned layer's stored tiles … satisfy its invariant or the declaration is cleared" |
| declared(v) → declared(v′), v ≠ v′ | *changed* | yes, same clause |
| declared(v) → declared(v), unchanged | *re-established* (the below-clause's "kept") | yes, same clause |
| declared → none | *cleared* | yes — the "or is cleared" branch |
| alignment → slab, or slab → alignment, in one commit | *cleared* + *declared*, composed under "A commit MAY make several of these changes at once"; or a single *change* if "a slab or alignment declaration" is read as one object | yes under either reading; `[R-CNT-16]` forbids only the simultaneous holding of both |

I found no transition unnamed, and no verb naming a transition the below-clause fails to
provide for. The one wording slip is that "re-established" is applied to the *declaration*
in the member list and to the *invariants* in the clause below — but the below-clause's
"kept" occupies the same slot, so the mapping is forced. All three restatements — §11.1's
Rationale, §20.3 step 4 itself, and Appendix H's updater checklist — carry all four verbs; I
grepped for the verb list across the document (normalising blockquote wrapping first) and
got three hits, all four-verb, plus one three-verb hit which is the below-clause and reads
"declared, changed or kept", the fourth case being its "or is cleared" branch. **No finding
here.**

I also checked that the two lists between them reach every declaration field of §7.4: name,
layout, linearization, codec, filter, A, S, A_slab, rank, channel count, each dimension's
name/extent/tile extent, each channel's name/type/fill, index_encoding, entry_count,
crc_of_crc_array, the extent slot and the sub-records. Every one is on the permitted side,
the fixed side, or named as following the commit (entry_count, crc_of_crc_array, extent
slot) or as §20.4's subject (sub-records). Complete.

---

## 8. Sweeps and mechanical checks

I ran the register through a parser rather than reading the counts off the page.

- §21.2 states 35 conditions; the table has 35 rows (F1–F10, F12–F36 — F11 struck, as its
  Note says). §21.3 states 49; 49 rows, L1–L49, no gap. §21.4 states 26; 26 rows. §21.5
  states 10; 10 rows. Total **120**, and §21.8 states "120 conditions".
- I counted instances by §21.1's own mechanical rule (semicolon-separated; a cell reading —
  is one): F 56, L 116, T 55, R 50 → **277**, and §21.8 states "277 instances". This is the
  strongest single piece of evidence I have that these tables were maintained carefully; the
  count is not robust to a single stray semicolon.
- I spot-checked the instance rules on the rows where they bite. L21 (4) = 2 layout formulas
  × 2 directions of a "does not equal". T3, T14, T22 (6 each) = 3 layout formulas × 2
  directions. L44, T21 (3 each) = 3 formulas × 1 direction, the condition text bounding it
  ("exceeds", "larger than"). T24 (1) = "any codec", the family without a change of shape.
  T15, T25 enumerate their materially different members. Every one follows the stated rule.
- L2's nine instances: I derived the designated declaration-derived quantities of a layer
  independently and got the same nine, including the two dominance arguments the cell makes.
  I checked both: C·N − [(C−1)N + (N−1)] = 1 > 0, so C·N dominates the maximum disk ordinal;
  and Q = ΣBᵢ ≥ C because every element size is at least 1, so P·Q dominates V = P·C. And
  ⌈P/8⌉ is correctly *absent*, since it never exceeds P.
- L1's eight instances correctly omit A and A_slab: those are not "offset, length, extent or
  count" fields under `[R-ENC-03]`, and their own rows (L39, L29) already bound them at 2⁶².
- Detector/detection-point consistency: 20 rows carry detector *verifier* (F7, F25, F26,
  F27, F28, F33, F36, L18, L25, L40, L41, L42, L46, L47, L48, L49, T2, T4, T5, T26) and
  every one of them has Detected = *certification*; no reader row carries *certification*;
  every reader row names one of §19.2's four tiers. Zero anomalies.
- `[R-CNT-06]` "states nine" (§2.3): I counted the rows governed by it — F8, F9, F10, F12,
  F13, F14, F15, F16, F17 — nine exactly, of which two (F8 magic, F14 CRC) assert invariants
  `[R-CNT-24]` fixes and seven do not, matching §2.3's "the other seven".
- Requirement-to-row coverage: 162 distinct `R-XXX-NN` identifiers appear in the document
  (one, `R-ENC-100`, is §2.2's illustration of numbering above 99, not a requirement); 67
  are cited by register rows. I walked the 95 uncited ones looking for a detectable
  file-conformance violation with no row, and found none: they are reader/writer/updater
  conduct rules, SHOULDs, non-violations (`[R-SER-09]`, `[R-MTA-10]`), rules whose
  violations are registered under a different governing identifier (`[R-IDX-02]` under
  `[R-IDX-03]`, `[R-COD-01]` under `[R-COD-08]`, `[R-SLB-04]` under `[R-SLB-03]`, whose Note
  says exactly that), unwitnessed conditions (`[R-SER-01]`, `[R-COD-10]`'s undetectable
  half), or requirements stating no condition a file can exhibit (`[R-ENC-06]`,
  `[R-ENC-01]`). §21.1's completeness clause survives the sweep.
- Appendix H's verifier checklist against the 20 verifier rows: it names coverage/slack
  (F33, L18 and §9.7), extent overlap (F33, L18), record flag bits (F25/F26/L46/L47 and
  F28/L49), the front block (F1, F6), the pre-trailer gap (F7), reserved-range types (F36,
  L25), alignment and slab (L40–L42), decoded content (T4, T5, T2), and member ordering
  (F27, L48). The only verifier row it does not name is **T26**, and T26's own row says "the
  check that detects it is T2's or T4's, and this row records the cause rather than a
  procedure of its own" — so the checklist is complete as to *procedures*. Not a finding.
- Worked examples I re-derived and confirmed: §11.2's G = (4, 8), N = 32, P = 65,536, and
  ⌈1000/256⌉ = 4; §11.4's ordinals (tile (1,0) → 8; (300,700) → tile (1,2), s = 10, in-tile
  (44,188) → 44·256 + 188 = 11,452; planar channel 2 → 2·32 + 10 = 74); §15.4's
  entry_count = 1,000,000 → 16 segments (15 full + 16,960), 64-byte CRC array, region
  20,000,064 bytes, entry 999,999 at segment-relative 20 × 16,959 = 339,180, segment 15 at
  [19,660,800, 20,000,000); §15.4's planar example (disk ordinal 74 at region bytes
  [1,480, 1,500); channel 3's entries 96–127); §17.3's byte-shuffle
  (`00 00 00 00 00 00 80 00 40 3F 40 40`, which I reproduced permutation-index by
  permutation-index); §20.3's 32 · 20 + 4 = 644; §21.9's note (2³²/2¹⁶ × 4 = 256 KiB,
  2³⁶/2¹⁶ × 4 = 4 MiB). All correct.
- Phrase sweeps (run over a whitespace-normalised copy with `> ` blockquote markers folded
  away first, per the brief's warning about hard wrapping, and each zero checked against a
  positive control from the same passage): "declared, changed, re-established or cleared" 3;
  "declared, changed or kept" 1; "re-established" 4; "slab or alignment declaration" 4;
  "not a file-conformance violation" 1; "file-conformance violation" 9; "conduct rule" 2;
  "binds the actor" 1; "no condition a file can exhibit" 3; "cannot establish" 8;
  "MUST NOT certify" 4; "unexamined" 3; "partial total" 4; "unable to check" 6;
  "a verifier MUST"/"A verifier MUST" 13; "verifier MUST NOT" 3.

---

## 9. Findings

Two. Both are non-byte-level, and I say why for each. I looked hard for a byte-level fork in
the certification procedure, the coverage walk and the checksum chain and did not find one;
§10 records the suspicions I opened and closed.

### verifier-01 — AMBIGUITY — §4.7, `[R-ENC-16]`: the structural/descriptive definitions quantify over different actor sets, so the partition they claim does not hold

> "Every field this specification defines is classified by what its *value* determines,
> each class being what the one before it is not. A field is **structural** if its value
> determines anything a conforming reader or verifier does with the bytes it reads — where a
> byte lies, how it decodes, what a decoded value is, or whether the file, layer or tile is
> accepted at all … It is **descriptive** if it determines none of those: its value
> determines nothing a conforming reader does, and a reader MUST NOT alter decoding based on
> it".

The structural test ranges over "a conforming reader **or verifier**". The descriptive test
ranges over "a conforming **reader**" alone. The sentence asserts they partition — "each
class being what the one before it is not" — but as written they do not: a field whose value
determines something a verifier does and nothing a reader does satisfies **both** tests.

The witness is not hypothetical. §7.2's record-header table classifies the flags field,
"bits 2–15 reserved", as **structural**. `[R-CNT-12]` says of those bits "writers MUST emit
zero; **readers MUST ignore them**", and then assigns detection to the verifier: "a verifier
MUST treat a nonzero reserved flag bit … as a validity error at the record's governing
scope" (F26, L47, detector *verifier*). So the value of those bits determines nothing a
conforming reader does and determines whether a verifier certifies. Structural by the first
test; descriptive by the second.

Permitted readings, and the one I picked:

- **(a) The actor set for both classes is "reader or verifier."** The descriptive clause's
  "a conforming reader" is elliptical for the phrase just given. Then the classes partition
  and the reserved flag bits are structural, as §7.2's table says. **I picked this.**
- **(b) The actor set differs as written.** Then the classes overlap, and every field whose
  only consequence is a verifier check is in both. §7.2's table would then be asserting one
  of two available answers.

I picked (a) because the following sentence assigns every actual field outright — "In format
major 1 `version_minor` is the only descriptive field, and every other field this
specification defines is structural" — which is only consistent with (a), and because the
descriptive clause's second half ("each descriptive field's definition states what a reader
does when the field contradicts the data it describes") describes a *descriptive-of-something*
field, which reserved bits are not.

What an implementer does wrong without it: not much, which is why I grade this low. Under
(b) they would classify the reserved flag bits, and the layer record's and sub-record's flag
bits, as descriptive — and the only normative consequence of "descriptive" is "a reader MUST
NOT alter decoding based on it", which `[R-CNT-12]` independently requires of exactly those
bits ("readers MUST ignore them"). The classification is presentational (§4.7's Note: layout
tables carry a "taxonomy class" column), so the two readings converge on behaviour. The
defect is that a rule stating a partition does not state one, in a passage on this round's
changed surface.

**Byte-level: no.** Nothing an implementation emits, accepts or rejects turns on the class
label; the label's one normative consequence is separately and identically stated for the
only field where the two readings differ.

### verifier-02 — AMBIGUITY — §5.2 `[R-CNT-21]` and §9.7 `[R-LIF-08]`: the incompleteness test is stipulative at layer scope and factual at tile and file scope, and its tile gloss names only two of the tile cases

> "Where the walk of §9.7 does not enumerate every region's claimants, the verifier MUST
> report the total as partial. **The walk is incomplete where a scope-level rejection ends
> that scope's enumeration**, where the verifier declined a layer on resource grounds
> (`[R-ERR-04]`) and so never enumerated its claimants, or where the verifier elected under
> `[R-CNF-11]` to stop at the first violation; a tile's or a document's decode declined
> leaves the walk complete, that claimant being enumerated from its index entry or extent
> slot. An entry `[R-IDX-03]` classifies reject-tile on a *structural* ground leaves it
> complete too …
> **A rejected layer's claimants are not enumerated, whether or not the rejection impeded
> reading them** …"

"A scope-level rejection" reaches all three scopes — §2.4 defines file, layer and tile — but
the passage then treats them incompatibly, and the passage supplies no test that sorts them.

At **layer** scope the rule is *stipulative*: the claimants go whether or not the rejection
impeded anything, and the counter-factual is spelled out. At **file** scope it cannot be
stipulative: F27 (an unsorted file-scope user-metadata document, detector *verifier*,
detected at certification) rejects the file after the walk has reached every claimant, and
stipulating that a file-scope rejection ends the file's enumeration would leave the partial
total at F, or at F less the front block, directory and trailer — a number that reports
nothing. So at file scope the test must be factual. At **tile** scope the passage glosses
exactly two cases as leaving the walk complete (a declined decode, and a structural-ground
entry) and is silent on the rest.

The rest is not a small class. Every tile-scope row whose entry is well-formed and whose
defect is found after the claimant was enumerated is in it: T1 (payload crc), T2, T3, T4,
T5, T14, T17–T26. Two readings:

- **(a) Factual.** The operative criterion is the first sentence — whether the walk
  enumerated every region's claimant — and the "scope-level rejection" clause is a gloss on
  it. A T4 tile's extent was enumerated from its index entry before any decode; the
  rejection ends nothing; the walk is **complete** and the total exact. **I picked this.**
- **(b) Stipulative, by analogy with the layer rule.** A reject-tile is a scope-level
  rejection, so the tile's claimant is discarded; the walk is **incomplete** and the total
  partial, higher by that tile's length, and the verifier must name the violation that
  stopped it.

I picked (a) on three grounds. First, the first sentence states the criterion in terms of
enumeration and the rest of the paragraph glosses it. Second, the layer rule states its
counter-factual expressly — "whether or not the rejection impeded reading them" — and a
stipulation that needed saying at layer scope would have needed saying at tile scope too;
its absence is the signal. Third, §15.3 settles one member of the class outright — an entry
whose only defect is that its stored bytes fail its crc "keeps its place in the *verifier*
rows, in run continuity, and **in the coverage walk**" — and the reason it gives (the claimant
comes from the entry, not from the payload) transfers verbatim to T4, T3, T14 and the codec
rows, exactly as §5.2's own reason for the declined-decode case does ("that claimant being
enumerated from its index entry or extent slot").

What an implementer does wrong without it: two conforming verifiers handed the same
nonconforming file — say W6, my four-tile layer whose tile 3 carries non-fill padding —
report different slack totals for it. Under (a): 52 bytes, exact. Under (b): 180 bytes,
partial, naming "tile scope / T4". §22.3 makes that number load-bearing — "a verifier
reports the slack total (§9.7), which is the number that distinguishes a working file from a
padded one — a verifier that stopped early reports it only as partial (`[R-CNT-21]`), so the
distinguishing figure comes from a walk that completes" — and §20.3's Note makes it the
operator's signal to compact. An operator reading "partial" where the walk in fact completed
learns nothing about whether to compact.

I would not repair this in the text myself: the passage has been rewritten more than once
(it now carries three incompleteness causes, two tile carve-outs, a layer counter-factual and
an upper-bound claim), and the clean fix is a choice between naming the tile cases and
recasting the gloss around enumeration, which is a human's call.

**Byte-level: no.** The disputed quantity is a line in the verifier's report, not a byte on
disk and not a verdict: the file is *nonconforming* under both readings, since the rejection
that raises the question is itself an established violation. No writer's emittable set moves
and no accept/reject verdict moves.

---

## 10. Suspicions opened and closed

Recorded because a clean lane has to show it looked.

1. **Does a verb in §20.3 step 4's closed list name a transition the below-clause does not
   provide for?** No — the table in §7 above enumerates all five transitions of a
   slab-or-alignment declaration and matches each to a verb and to a clause. Closed by "a
   slab declaration declared, changed or kept has its invariants re-established over every
   run the new state keeps, or is cleared (`[R-SLB-04]`), and an aligned layer's stored tiles
   — every one the new state keeps, not only those this commit adds — satisfy its invariant
   or the declaration is cleared".
2. **Does a restatement of that list still carry three verbs?** No. Three restatements,
   all four verbs. Closed by grep over the whitespace-normalised text.
3. **Does §20.3 step 4's bar name its own category correctly?** It calls itself a rule
   "stating no condition a file can exhibit (§21.7, `[R-ERR-01]`, `[R-CNF-02]`)", and §21.7
   distinguishes that from an *unwitnessed* condition. I suspected mis-classification, since
   a file physically carries its superseded generations until compaction and §9.6's probe can
   find them. Closed: the condition's subject is a *transition between two generations*, not
   a state of one file, which is precisely §21.7's `[R-ENC-06]` move ("a different file,
   conforming or not on its own terms") and §20.3's own echo of it ("a file such a commit
   leaves can be nonconforming on its own terms"). And §2.3 `[R-CNF-02]`'s enumeration of
   express non-violations does now name it: "§20.3 step 4's bar on the fixed declarations of
   a layer that stores a tile are the cases this text states".
4. **Is `[R-CNF-02]`'s three-case list closed against other express non-violations?** I
   swept for "not a file-conformance violation", "binds the writer's conduct", "conforming
   all the same", "never nonconforming", "no file is nonconforming". Everything else falls
   into the *first* category (conduct rules — barriers, published values, targeted registry
   version) or into §21.7's unwitnessed class, neither of which the closed list is about.
   Closed.
5. **Is `[R-COD-11]`'s cannot-establish ground reachable by a conforming verifier?** No, and
   `[R-COD-11]` says so itself. Closed by "software unable to execute an assigned codec or
   filter is not a conforming reader (`[R-CNF-03]`)".
6. **Is `[R-WRT-09]`'s "including every stored tile's entry crc" quantified over relocated
   extents only?** No. Closed by the sentence above it: "it relies structurally on every
   structure it copies, so it MUST verify each link of the chain".
7. **Is a T14 entry (codec 1, length ≠ decoded size) a claimant of the coverage walk?**
   Yes. Closed by §9.7's universal head — "the stored extent of each non-sentinel
   tile-index entry" — whose only exception is the structural class, and by §15.3's "Six
   rows are marked *structural*: they classify an entry whose own 20 bytes yield no usable
   extent", which T14 is not among. (§15.3's justification for the crc case — "the defect
   lies in the bytes it addresses, not in the entry" — does not transfer to T14, whose defect
   is a field of the entry; but the six-row rule is the classifier, not that justification.)
8. **Does L40 fire on a structurally malformed entry that happens to be misaligned?** No.
   Closed by §15.3: such an entry "contributes no stored extent to the *verifier* rows, which
   bind over well-formed entries' extents only", and the alignment and slab rows are
   *verifier* rows in that table.
9. **Is §5.2's exemption from the slack total ("§6.2's ordered validation rejects the file
   before a live trailer is established") narrower than the cases where no live state
   exists — F5, which is checked at §19.1 step 1 and is not part of §6.2's order?** Yes,
   narrower, but harmlessly: the governing sentence is "a verifier that reaches a live state
   MUST report the total", and an F5 rejection reaches none, so the duty never fires. Closed.
10. **Is §2.3's "on both sides — a dimension extent, a planar layer's channel list, an
    interleaved layer's channel list" accurate?** A dimension extent is named in §20.3's
    permitted list and not in its fixed enumeration, so under a "named in both lists" reading
    it is spurious. Closed on the other reading — "both sides" means the field carries both a
    permission and a bar — under which all three named fields fit exactly and no unnamed
    field does. Either way the sentence's own resolution ("the permitted side states the whole
    of what a commit MAY do to it") makes every case decidable.
11. **Is §21.1's list of strict specializations sound?** I checked each pair. F21 ⊂ F22
    (extent slot (0,0) forces extent_length 0 < 5); L10 ⊂ L11 likewise; F35 ⊂ F36 and
    L24 ⊂ L25 (MU = 1 is a case of "whatever its MU bit"); F1's two instances of F6 and F8.
    All five hold, and the list disclaims closure. Closed.
12. **Does §21.6's non-violation table omit a defined non-violation — an over-long
    pre-trailer gap, say?** It does omit that one. Closed by §21.1: "neither this
    completeness clause nor the instance arithmetic below reaches §21.6's defined
    non-violations". §21.6's completeness is not normative.
13. **Does a verifier owe §9.6's backward probe?** No. Closed by "no verdict turns on the
    probe" and "For a verifier the probe is diagnosis … not a finding about the file it was
    given", and by §9.7's Note.
14. **Is §19.1's F5 check ordered before §6.2's, and is that consistent?** Yes; §19.1 step 1
    places it there expressly and §21.2's preamble confirms F5 does not reach a foreign major.
    Closed.
15. **Does the register omit a detectable file-conformance violation?** I walked all 95
    requirement identifiers no row cites. Every one is a conduct rule, a SHOULD, a
    non-violation, an unwitnessed condition, a requirement stating no condition a file can
    exhibit, or a rule whose violations are registered under another governing identifier.
    Closed — this is the sweep I would have expected to surface a completeness defect, and it
    surfaced none.
