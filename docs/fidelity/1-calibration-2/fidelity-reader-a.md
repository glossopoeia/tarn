# Reader-implementer walk — edition A — transcript

## Disclosure

**What I read.** Exactly one file:
`/Users/robertkleffner/Documents/GitHub/tarn-first-draft/scratch/cleanroom/editions/a/tarn.md`
(4,981 lines). I read it in full, sequentially, via seven `Read` calls
(offsets 1, 700, 1400, 2100, 2800, 3500, 3899, 4297, 4576, 4854, 4883 —
the tool's 25k-token cap forced the split). I did not open any other
copy of this specification, did not list any directory other than my
own scratch directory, and did not read PLAN.md, OPEN-QUESTIONS.md,
AGENTS.md, README.md, CONTRIBUTING.md, any ADR, any file under
`conformance/`, or `spec/registry.json`.

**What I ran.** `mkdir -p` and one empty `ls` on my own scratch
directory (confirmed empty at start — no previous attempt's files were
there); one `wc -l` and one failed `cat -A` (wrong flag, no output) on
the target file itself, both harmless; and three local Python
computations (a hand-rolled CRC-32C, using no file I/O) to check the
document's own worked-example checksums and the §11.4 arithmetic
against my own re-derivation. No other files were read, no network
access was made, no other directories were listed.

**Context I did not ask for.** Before this task began, my context
contained a project instruction file pointing at another file, a
user-memory index of prior-round notes about this same project, and a
git-status block naming recent commit subjects. None of it is part of
the specification and none of it is evidence about the specification;
I did not open the file the project instructions pointed to, did not
open any memory note, and did not let any commit subject inform a
reading of edition A. I disregarded all of it, per the brief's
instruction, and note only that it appeared, without repeating its
contents.

**Path check.** The file I was told to read was exactly where the
brief said it was; no discrepancy to report.

**Scratch directory.** I did not end up needing working files beyond
this transcript and the two inline Python snippets (run directly via
Bash, not saved to disk), so `/private/tmp/claude-501/.../fidelity-2/scratch/walk-reader-a/`
was created but left empty.

---

## Part 1 — The open path (cold start, byte by byte)

### Local reader

Per §6.1/`[R-CNT-04]`, a reader whose open leaves bytes `[0,16)`
resident (a local file read whole, a memory mapping) MUST verify the
16-byte front signature block by byte equality before other
processing (mismatch: reject-file). A reader that would have to issue
a further range request for those bytes MAY defer or omit the check.

### Remote reader — the exact ranges (§6.4, `[R-CNT-09]`, `[R-CNT-10]`; consolidated at §19.1)

The baseline is **two requests**, each with an exact target:

1. **Suffix range for the final 64 bytes** — `[F-64, F)`. The
   transport's response to this range request also discloses the
   complete resource length where the transport supports it
   (`[R-CNT-10]`), so this one request supplies both the
   transport-authoritative F (§19.1 step 1) and the trailer bytes
   (§19.1 step 2). Validate, **in this fixed order** (§6.2, echoed at
   §19.1 step 2): trailer magic → trailer CRC → version gate (§6.3) —
   "only these touch fields whose positions are fixed across all
   majors" — then, all three passed, the remaining field gates as a
   set: flags; `committed_file_length` = transport size and multiple
   of 64; `dir_offset` ≥ 16; `dir_length` ≥ 4;
   `dir_offset + dir_length` ≤ F − 64; `file_id` ≠ 0; reserved bytes
   zero. Any failure: reject-file (§6.2, `[R-CNT-06]`).
2. **`[dir_offset, dir_offset + dir_length)`** — the directory region.
   Verify its final 4 bytes (CRC-32C over the preceding
   `dir_length − 4` bytes) before any other use of the region
   (`[R-CNT-11]`), then parse records (§7.1, §7.2).

"These steps are ordered by dependency, not by I/O... steps 1 and 2
cost one request between them" (§19.1 step 1). A reader MAY instead
speculatively fetch a suffix window in one request and use
containment to skip request 2 (`[R-CNT-09]`); that is documented as an
alternative to, not a replacement of, the two-request baseline the
probes ask about.

Field bounding request 2: **`dir_offset` and `dir_length`**, both
trailer fields obtained and validated in request 1 — the request
cannot be formed, let alone issued, until the trailer CRC has
verified the bytes it comes from (`[R-ENC-10]`: "verify the checksum
covering a field before acting on that field") and until
`[R-CNT-06]`'s own-field gates on `dir_offset`/`dir_length`/their sum
have passed. Total bytes fetched before the directory record sequence
is available to parse: **64 + `dir_length`** — the second number is
whatever that file's own trailer states; the prompt's "4,096-byte
file" does not by itself fix `dir_length`, only F.

### Appendix A worked example, re-verified

I hand-computed CRC-32C (Castagnoli, reflected in/out, init/final XOR
`0xFFFFFFFF`) and reproduced the document's own check vector before
trusting my implementation:

```
CRC32C("123456789")            = 0xE3069283   ✓ matches §4.5's vector
CRC32C("")                     = 0x00000000   ✓ matches §4.5's vector
```

Then, over the 60 trailer bytes of Appendix A's 128-byte minimal file
(magic `8A 4E 52 41 54 0D 0A 1A`; `version_major=1`, `version_minor=0`;
`flags=0`; `dir_offset=16`; `dir_length=4`; `committed_file_length=128`;
`file_id=0x0123456789ABCDEF`; 12 zero reserved bytes):

```
CRC32C(trailer[0:60]) = 0x402F157E → bytes 7E 15 2F 40
```

This matches the document's stated trailer CRC exactly (line: "trailer
CRC-32C = 0x402F157E, over trailer bytes [0, 60)"). The document's own
worked numbers check out.

I also re-verified §7.4's layer-record example (rank-1 layer `sst`,
4 addressed tiles, all sentinel):

```
entry array = (FF×16 00×4) repeated 4 times   (80 bytes)
CRC32C(entry array)          = 0x80A34955   ✓ matches "segment CRC ... 0x80A34955"
CRC32C(that CRC, 4 bytes LE) = 0xC4EE982E   ✓ matches "crc_of_crc_array ... 0xC4EE982E"
CRC32C(65536 sentinel entries)= 0xEECB3BB2  ✓ matches [R-IDX-05]'s stated constant
```

All three of the document's own numeric claims are correct.

---

## Part 2 — Validation timing by tier (§19.2)

Four tiers, each with its own detection deadline, "no later than the
reader's first reliance on the structure that carries it":

- **At open:** front signature block (if resident, `[R-CNT-04]`), the
  trailer (§6.2–6.3), the directory region + record walk (§7.1–7.2),
  and the layer-name namespace (`[R-ENC-15]`) — all decidable from the
  trailer + directory bytes and F alone, no extent fetched.
- **At first access to a layer:** the *full* validation of that
  layer's record — extent slot, the entire §7.4 constraint set, exact
  parse, sub-record walk/multiplicity, name rules, u64 domain, every
  value-set field (layout/linearization/codec/filter/type/
  index_encoding), fill constraints, the lz4 cap, geometry floor and
  arithmetic up to the 2⁶³−1 ceiling, and the index cross-checks that
  need no I/O (`entry_count` vs. geometry, `extent_length` vs. the
  index-size formula) — §19.3, `[R-RDR-03]`. Still no fetch: "layer
  access performs no fetch."
- **At use of a tile:** the index-chain (`crc_of_crc_array`, segment
  CRC), the entry classification (§15.3), the payload fetch + entry
  CRC, decode, and the exact-decoded-size check — §19.4 steps 3–6.
- **At use of a record's extent:** that extent's own CRC and whatever
  content rules attach at its encoding — before anything the extent
  holds is returned.

"A reader MAY detect any violation earlier... it MUST NOT return data
whose governing structure has not passed the validation this rule
requires at its tier" (`[R-RDR-02]`).

---

## Part 3 — Layer access and the tile-read algorithm

**Layer access** (§19.3, `[R-RDR-03]`): first access to a layer must
be preceded by full record validation as above; failure takes each
cited rule's own scope (in every case here, layer scope, since
duplicate-*layer*-name is checked earlier, at open).

**Tile read** (§19.4, `[R-RDR-04]`), 8 steps, each citing its own
outcome:

1. Domain — point request: `0 ≤ xᵢ < Eᵢ` or the request simply fails
   (no verdict on the file); region request — intersect with extents.
2. Ordinals — tile coords, in-tile ordinal, spatial ordinal `s`, disk
   ordinal (`[R-GEO-06]`).
3. Index chain — verify `crc_of_crc_array` and the covering segment
   CRC (`[R-IDX-04]`) → **reject-layer** on failure.
4. Entry — classify per §15.3 (`[R-IDX-03]`); sentinel short-circuits
   to fill; malformed → **reject-tile**.
5. Payload — fetch `[offset, offset+length)`, verify entry `crc`
   before decoding (`[R-CNT-20]`).
6. Decode — codec then filter inverse (§17.1); exact decoded size
   (`[R-SER-07]`) or **reject-tile** (`[R-COD-08]`).
7. Extract — §14 offset arithmetic; never return padding
   (`[R-GEO-04]`).
8. Return — bit patterns unaltered (`[R-MDL-02]`, `[R-TYP-04]`), the
   one resolved exception being a nonconforming interleaved bool byte
   (`[R-SER-08]`).

---

## Part 4 — Five (plus) degradation walks, end to end

### D1 — Unrecognized flag: trailer `flags = 0x00000004`

`0x00000004` = bit 2 set. Bit numbering: bit 0 = LSB (`[R-ENC-08]`).
Bits 0–15 are the **incompat lane** (§6.2's trailer layout table row
for `flags`: "bits 0–15 (incompat lane) all zero, a set bit being
reject-file (F19)"). Bit 2 is inside that lane. §6.3/`[R-CNT-08]`: "a
reader MUST reject-file on any set bit it does not implement in the
incompat lane... In this specification's text no flag bits are
defined... so every such bit is unimplemented." Register row **F19**
(§21.2), governing rule `[R-CNT-08]`, detector reader, detected at
open. → **This is answered in probe R2.**

### D2 — Unknown/unsupported codec: codec value 3 (zstd) not implemented by the reader

Codec 3 is one of the four values `[R-COD-03]` assigns, and "all four
are **core** — a conforming reader MUST implement every one of them
(`[R-CNF-03]`)." §17.4/`[R-COD-11]` is explicit: "For a conforming
reader that position [cannot execute] arises only at a reserved or
experimental value, every assigned codec and filter being core: it
rejects the layer... software unable to execute an assigned codec or
filter is not a conforming reader." → **Answered in probe R3**, with
the finding this raises noted below.

### D3 — Unrecognized/reserved flag combination at record level

A non-layer top-level record with `MU=1, PE=0` (a combination "no
writer emits") is a **verifier**-detected condition (F25,
`[R-CNT-12]`) — a reader applies fixed semantics (treats it as
`PE=1`) regardless; it never blocks a reader. A genuinely *unknown
top-level record type* is D-covered separately in **probe R8**.

### D4 — Truncated tail / torn file

Default read path (§9.5, `[R-LIF-05]`): "trailer-at-end-or-fail: a
reader that finds no valid trailer in the final 64 bytes MUST report
the file torn or invalid and MUST NOT scan backward." This is
distinct from recovery (§9.6), which is "never a reader behavior" on
the default path — only recovery tools/verifiers probe backward, and
even then must re-verify the whole file before trusting the result
(the trailer-mimicking-payload caution, `[R-LIF-06]`).

### D5 — Checksum mismatch: directory CRC

§7.1/`[R-CNT-11]`: "A reader MUST verify that CRC before any other use
of the region (mismatch: reject-file)." Register row **F20**
(§21.2). → **Answered in probe R5.**

### D6 — Limit exceeded: `entry_count` above §21.9's 2³² guarantee

§21.9/`[R-ERR-04]`: the guarantee table states **minimums**, not caps;
a file exceeding one "remains conforming, and a reader MAY decline it"
— at the narrowest scope whose derived quantities exceed what it can
serve — reported "as a resource limit and not as a validity error."
This is categorically different from every other walk here: it is not
a violation, the file stays conforming, and the outcome is a licensed
capability decline, not a register row.

### D7 — Format major the reader does not implement

§6.3/`[R-CNT-07]`: "A reader MUST reject-file when version_major is 0
(invalid) or is a major it does not implement, and the diagnostic for
an unimplemented major SHOULD be distinct from both 'not a TARN file'
and 'corrupt.'" §2.3/`[R-CNF-13]` governs which register rows (if any)
"reach" such a file at all: only F8 (trailer magic), F14 (trailer
CRC), F6 (front block), and both instances of F1 (byte-reversed
signature) reach a file declaring another major, because those alone
assert invariants `[R-CNT-24]` fixes in every major. §21.6's closing
paragraph: this is one of exactly two "conforming file a reader
nevertheless refuses" cases (the other being an experimental-range
top-level record with `MU=1`) — the file "can be perfectly
conforming under that major," and the refusal is "not a finding about
its bytes." This walk is also where I found this transcript's primary
finding — see below.

---

## Part 5 — Worked example: R7's arithmetic, checked

Interleaved layer, dimensions declared in order **y** (extent 12,
tile extent 5), then **x** (extent 9, tile extent 4); channels
declared in order **a** (uint16, size 2), then **b** (uint8, size 1).
Sample requested at `(y=6, x=5)`.

Grid counts (§11.2, `Gᵢ = ⌈Eᵢ/Tᵢ⌉`):
```
G_y = ceil(12/5) = 3
G_x = ceil(9/4)  = 3
```
Tile coordinates and in-tile position (§11.4):
```
t_y = 6 div 5 = 1,  u_y = 6 mod 5 = 1
t_x = 5 div 4 = 1,  u_x = 5 mod 4 = 1
```
In-tile ordinal (row-major, last-declared dimension fastest,
`Σᵢ uᵢ·∏_{j>i}Tⱼ`, d=2 so this is `u_y·T_x + u_x`):
```
in-tile ordinal = 1*4 + 1 = 5
```
Spatial tile ordinal (`s = Σᵢ tᵢ·∏_{j>i}Gⱼ = t_y·G_x + t_x`):
```
s = 1*3 + 1 = 4
```
Disk tile ordinal (`[R-GEO-06]`): for an **interleaved** layer, disk
ordinal = `s` (no `c·N+s` term — that applies to planar only):
```
disk ordinal = 4
```
Byte offset of channel `b`'s value at in-tile ordinal `u=5`
(§14.2 table + worked-example restatement "channel c's value at
in-tile ordinal u sits at byte u·Q + Fᶜ"):
```
Q  = B_a + B_b = 2 + 1 = 3           (sample stride)
F_b = B_a = 2                        (b is channel index 1; sum of element
                                       sizes of channels before it)
offset = u*Q + F_b = 5*3 + 2 = 17
```
**Disk ordinal = 4; channel b's value begins at byte 17 of the
decoded tile image.**

(Note on the probe's own wording: the document reserves the terms
*extent_offset*/*extent_length* for a record's extent slot, §7.2; a
tile-index entry's own fields are named plainly `offset` and `length`,
§15.1. I have answered using the tile-index entry's actual fields
throughout, since that is unambiguously what R4 and R7 are asking
about.)

---

## Part 6 — Findings

See `findings` in the structured result for the full text; summarized
here:

1. **CONTRADICTION** between §19.1 step 1 (the open algorithm's literal,
   major-agnostic instruction to reject any file below 128 bytes
   "decided from F alone and needing no other byte of the file," cited
   to F5/`[R-CNT-27]`, *before* the trailer — and hence `version_major`
   — has been read) and §2.3/`[R-CNF-13]`'s reach doctrine, reinforced
   by its own worked Note, that F5 explicitly **does not reach** a
   file declaring a format major other than 1 ("F5 does not reach
   although its subject is the physical file size... those are format
   major 1's"). The reach doctrine's general rule requires that a
   non-reaching condition "is not assessed against a file declaring
   another major" — which is only decidable *after* the major is
   known, i.e. after reading trailer bytes the file may be too short
   to need reading to fail step 1. For a file with, say, 80 ≤ F < 128
   whose trailer nonetheless validates magic/CRC/version-gate for an
   unimplemented major ≠ {0,1}, the two passages prescribe different
   dispositions for the *same bytes*: §19.1 says reject on F5 without
   ever consulting the trailer; §2.3 says F5 must not be established
   against this file, and the only applicable ground is the capability
   refusal of `[R-CNT-07]`. This is not merely a labeling nicety: a
   **verifier** built to §2.3's own vocabulary MUST report *nonconforming*
   once it establishes a violation, and MUST NOT report *cannot
   establish* in that case (§2.3, `[R-CNF-11]`) — but *cannot establish*
   is exactly the verdict `[R-CNF-11]`'s own text names for "the file
   names a format major version it does not implement." Whether this
   file's verdict is *nonconforming* (F5 established) or *cannot
   establish* (F5 does not reach, only the major is unresolvable) is
   undetermined by the document as stated, and the two verdicts are
   themselves defined to be mutually exclusive and load-bearing
   (`[R-CNF-11]`: "a verifier MUST NOT certify a file it reports that
   way," "an established violation takes priority"). Byte-level test:
   yes — it decides a verifier's MUST-level verdict (nonconforming vs.
   cannot-establish) and a reader's diagnostic ground (which §6.3
   itself insists SHOULD be distinguishable to the user) for one and
   the same input.

2. **OBSERVATION** on the shape of the conformance vocabulary: the
   document names exactly two licensed cases of "a conforming reader
   refuses an otherwise-conforming file" (§21.6's closing paragraph:
   an unimplemented format major, `[R-CNT-07]`; and an
   experimental-range top-level record carrying `MU=1`, `[R-CNT-15]`)
   and is explicit that a reader's inability to execute an *assigned/
   core* codec, filter, sample type, channel layout, user-metadata
   encoding, or registered record type is not a third such case at
   all — it is simply disqualifying: "software unable to execute an
   assigned codec or filter is not a conforming reader" (`[R-COD-11]`,
   `[R-CNF-03]`). Probe R3's literal premise ("the reader does not
   implement zstd") therefore describes software the document declines
   to characterize at all — no register row, no outcome class, and no
   guidance on what such (non-conforming, but very likely to exist in
   practice) software should do when it meets a zstd-coded layer. This
   is a real gap in what an *implementer* — as opposed to a finished
   conforming reader — is told to do while it is still missing a
   codec; the document's answer is, deliberately, that the question is
   out of scope until the codec is implemented. Byte-level test: no —
   a fully conforming implementation, by construction, never reaches
   this state, so it changes nothing about what a conforming
   implementation emits or accepts/rejects. Flagged as an observation
   about documentation completeness for implementers mid-build, not as
   a defect reachable by any conforming reader.

No other AMBIGUITY/CONTRADICTION was found that meets the byte-level
test after the full single-file read described above; several
apparent candidates I opened and closed:

- Whether the *order* among §6.2's second group of trailer-field
  checks (flags, `committed_file_length`, `dir_offset`, `dir_length`,
  their sum, `file_id`, reserved bytes) matters: closed — every one of
  these failures maps to the same outcome (reject-file) and the same
  detector/tier (reader/open), so no two conforming implementations
  can diverge in accept/reject or in bytes served by choosing a
  different order among them.
- Whether the sentinel value `2⁶⁴−1` being outside the declared
  `0..2⁶³−1` field domain (`[R-ENC-03]`) creates a domain conflict:
  closed — `[R-IDX-02]` explicitly carves sentinel entries out of both
  the domain rule and the sum-overflow rule by name.
- Whether §21.2's `[R-CNT-06]` "nine conditions" claim is internally
  accurate: checked by recount (magic, trailer CRC,
  `committed_file_length=F`, multiple-of-64, `dir_offset≥16`,
  `dir_length≥4`, the sum bound, `file_id≠0`, reserved-zero) — exactly
  nine; closed, no defect.
- Whether the front-signature-block-plus-trailer invariants alone
  (both asserted to hold "in every format major version" by
  `[R-CNT-24]`/§6.1) force the 128-byte floor for *every* major,
  which would make the §2.3 Note's "F5 does not reach" claim itself
  wrong: closed on rereading `[R-CNT-24]` precisely — it does **not**
  list "F is a multiple of 64" among the facts fixed for every major
  (only that the trailer is the file's final 64 bytes, with three
  named fields at three named fixed offsets, and that the front block
  is constant); so a hypothetical future major could place a
  64-byte trailer immediately after the 16-byte front block with no
  64-alignment padding, at F=80, which is indeed a state F5's
  128-byte-from-64-alignment argument does not reach. This closes the
  question of whether the Note is self-contradictory; it does **not**
  close finding 1 above, which is about the procedural clash between
  §19.1 and §2.3, not about whether the Note's own arithmetic is
  right.
