# Reader-implementer walk — edition A — transcript

## Disclosure

**Access.** I read exactly one file, byte-for-byte, start to end, in nine
sequential chunks via `cat -n` / `sed -n` over the Bash tool:
`/Users/robertkleffner/Documents/GitHub/tarn-first-draft/scratch/cleanroom/editions/a/tarn.md`
(5,004 lines, 303,815 bytes). I did not list any directory other than my own
scratch directory and the output directory (to `mkdir -p` them; I did not
read their contents). I did not open `AGENTS.md`, any ADR, any other copy of
this specification, `PLAN.md`, `OPEN-QUESTIONS.md`, `conformance/`,
`spec/registry.json`, git history, or any web resource. Every grep I ran
against the one file was a re-find of a passage I had already read in full
(used only to pin exact line numbers for citation, and to catch and correct
several citation errors of my own during a review pass — recorded honestly
below rather than silently); every one of those greps returned at least one
hit, so none of my conclusions rest on an unconfirmed zero. All arithmetic
and CRC verification below was done by local Python scripts reading no
files, written to my own scratch directory
(`/private/tmp/claude-501/-Users-robertkleffner-Documents-GitHub-tarn-first-draft/fidelity-5/scratch/walk-reader-a/`),
which held no files from a prior attempt when I began (I `mkdir -p`'d it and
`ls -la`'d it first; it was empty).

**Context I did not ask for, and disregarded as evidence.** Before this task
began, my context already contained: a `CLAUDE.md` pointer to an
`AGENTS.md` I did not open; a user memory file (`MEMORY.md`) listing many
entries about this project's harness, prior rounds, and prior findings
(e.g. "TARN harness vs charter", "TARN repair prose vs rules",
"TARN post-G3 readable-edition process"); a git-status block naming the
current branch (`readable`) and five recent commit subjects about a
"Readable" rewrite of §§14–17; and a model/environment identity block. None
of this is part of the specification and none of it is evidence about the
specification's content. I did not let any of it shape which passages I
read, what I searched for, or how I resolved any ambiguity below — every
finding and every probe answer is sourced only from the one file named
above, and I cite line numbers from it throughout (re-verified by grep
during a review pass; see the note above).

**The relayed "user request."** A line above the computed task relayed the
literal text "Go" as the message that launched this round. Per the brief,
this is the launcher's message to the orchestrator, carried out before I
was spawned; it is not a task for me and does not widen the access rule. I
disclose that it appeared and do nothing else with it.

**Path check.** The file I was told to read was exactly where the brief
said it would be, named `tarn.md`, inside `scratch/cleanroom/editions/a/`.
I note only that this is edition "a" of a multi-edition cleanroom; I draw
no inference from the path about what any other edition says.

**Wrapping.** The document is hard-wrapped prose with blockquotes using
`> ` continuation. I did not rely on line-oriented grep for any
multi-line phrase during the actual reading; I read every line of the file
directly (via `cat -n` and `sed -n`), so no search-miss risk applies to
anything I report below. The only greps I ran were short, single-line
fragments used purely to re-locate passages for citation.

---

## Part 1 — The open algorithm (container reader, no sample decode)

Source: §19.1 (heading at line 2938, through line 2994), §6.4 (heading at
line 925), §6.2 (heading at line 830).

A conforming reader's open is exactly four steps, consuming **only the
trailer and the directory** — no extent slot's content, no tile index, no
payload (line 2989–2991: "its I/O is §6.4's request accounting … at any
layer count and file size").

1. **End of file.** Obtain the transport-authoritative file size F
   (`[R-CNT-10]`). An F below 128 is immediately a validity error at file
   scope — F5/`[R-CNT-27]` — "decided from F alone and needing no other
   byte of the file" (line 2942–2944).
2. **Trailer.** Fetch `[F-64, F)` and validate, in §6.2's fixed order
   (line 863: "A reader MUST validate, in order"): magic → trailer CRC →
   version gate → the remaining field gates (flags, dir_offset,
   dir_length, dir_offset+dir_length ≤ F-64, file_id, reserved bytes).
   This trailer is the session's immutable snapshot (§9.5,
   `[R-LIF-05]`) — no later step re-reads the file's end (line 2957–2961).
3. **Directory.** Fetch `[dir_offset, dir_offset+dir_length)` and verify
   the directory's terminal CRC-32C over the preceding `dir_length-4`
   bytes **before any other use of the region** (`[R-CNT-11]`, defined at
   line 977; invoked again at line 2962–2963).
4. **Record walk.** Parse the record sequence (§7.2 framing), apply the
   MUST_UNDERSTAND gate for unknown top-level types, per-type
   multiplicity, extent-slot validity for non-layer records, the
   top-level user-metadata framing checks, and build the layer-name
   table, checking each name for uniqueness over raw bytes
   (`[R-ENC-13]`, `[R-ENC-15]`) — all decidable from the resident bytes
   and F (line 2965–2982).

For a **remote** transport that discloses a range response's complete
length (as R1 stipulates), steps 1 and 2 collapse into **one request**:
the suffix fetch for the trailer also discloses F (§6.4, line 927–935,
"The baseline remote open is two requests, each with an exact target…(1)
fetch the final 64 bytes — a suffix range, whose response also carries
the transport-authoritative file size F … so that §19.1's first two steps
cost one request between them"). Step 3 is the second and only other
request the open needs. §6.4's baseline accounting (line 925–941) names
these exact two targets:

- Request 1: `[F-64, F)` — 64 bytes — validates end-of-file and the
  trailer in one response.
- Request 2: `[dir_offset, dir_offset+dir_length)` — `dir_length` bytes —
  validates the directory.

A reader MAY instead speculatively fetch a larger suffix window and use
containment to skip request 2 if the window happens to contain the
directory (line 936–941); that is an optimization, not part of the
baseline two-request accounting R1 asks me to state.

**What bounds request 2.** `dir_offset` and `dir_length` are both trailer
fields, covered by the trailer's own terminal CRC-32C at bytes [60,64)
over bytes [0,60) (§8.1's coverage map, line 1250: "Trailer | trailer
bytes [60, 64) | trailer bytes [0, 60)"). `[R-ENC-05]` (line 485–487)
forbids a reader from allocating, seeking, or issuing I/O on the strength
of a field before the checksum covering it verifies, and `[R-ENC-10]`
(line 527–531) is the general form of that rule for "acting on" any
field. So request 2's range is bounded by `dir_offset` and `dir_length`,
and both are usable only *after* the trailer CRC (and the rest of §6.2's
ordered gates, line 863 onward) have verified — which is exactly request
1's response. Independently, `[R-CNT-06]` (§6.2, lines 849–862) also
bounds `dir_offset ≥ 16` and `dir_offset + dir_length ≤ F-64` as part of
that same ordered validation, so by the time request 2 is issued its
range is known to lie inside `[16, F-64)`.

## Part 2 — Validation timing (§19.2, heading at line 2995, body through 3037)

Four tiers, each the *latest* a violation may be detected, never the
earliest (`[R-CNF-12]` always licenses earlier rejection, line 3019–3021:
"A reader MAY detect any violation earlier"):

- **at open:** front block (if resident), trailer, directory region +
  record walk, layer-name namespace (lines 3003–3006).
- **at first access to a layer:** full validation of that layer's record
  (§19.3) before any use of its declarations (lines 3007–3009).
- **at use of a tile:** index-chain, payload, decode checks (§19.4),
  before any sample of that tile is returned (lines 3010–3011).
- **at use of a record's extent:** that extent's CRC and the content
  rules its encoding attaches, before anything it holds is returned
  (lines 3012–3016).

Failure always takes the *violated rule's own* outcome and scope, even
though the *detection point* can be later — e.g. an index-chain failure
is layer scope (`[R-IDX-04]`) even though it is only detected at tile use
(line 3018–3019). A violation in a layer never accessed imposes no
detection obligation at all (line 3021–3023: "a violating record in a
layer never accessed leaves every other layer's reads conforming") — this
is the one place the document explicitly licenses a reader to simply
never find out.

## Part 3 — Layer access (§19.3, heading at line 3038, body through 3062)

First access to a layer requires full validation of its record before
any of its declarations are used: extent-slot validity, the whole §7.4
constraint set (layout/codec/filter/index_encoding/linearization/type
value sets, A/S mutual exclusion), exact parse and sub-record framing,
name rules, the u64 domain and the `2⁶³-1` ceiling on every derived
quantity (`[R-ENC-04]`), the codec-4 (lz4) cap, the geometry floor and
its arithmetic, and the index cross-checks computable without I/O
(`entry_count` vs. geometry, `extent_length` vs. the index-encoding-1
formula). All of it is decidable from the resident directory and F —
**"layer access performs no fetch"** (line 3060).

## Part 4 — Tile-read algorithm (§19.4, heading at line 3063)

Eight steps, each step's failure taking the cited rule's own outcome:

1. Domain check (coordinate inside extents, or region intersected).
2. Compute tile/in-tile/spatial/disk ordinals (`[R-GEO-06]`).
3. Index chain: verify `crc_of_crc_array` over the fetched CRC array and
   the segment CRC over the fetched segment containing the entry
   (`[R-IDX-04]`) — both fetches parallelizable, both cacheable.
4. Classify the entry per §15.3 (`[R-IDX-03]`): sentinel short-circuits
   to fill with no payload I/O; malformed rejects the tile.
5. Fetch `[offset, offset+length)`, verify entry CRC before decoding.
6. Decode: codec, then filter inverse; result length must equal decoded
   size exactly (`[R-SER-07]`).
7. Extract requested values by §14's offset arithmetic; never return
   padding positions.
8. Return bit patterns unaltered (the one resolved exception being
   `[R-SER-08]`'s nonconforming interleaved-bool byte).

---

## Part 5 — Worked example 1: the 128-byte minimal file, with real offsets (Appendix A, heading at line 4548)

I re-derived every checksum in this example from the stated bytes, by
local computation (CRC-32C, reflected in/out, init/final `0xFFFFFFFF`,
polynomial `0x1EDC6F41`, implemented directly — no library — and first
validated against the document's own check vector at §4.5, lines
517–522):

```
CRC32C('123456789')      = 0xe3069283   (spec states 0xE3069283)  MATCH
CRC32C(b'')               = 0x00000000  (spec states 0x00000000)  MATCH
```

Then the file itself (hex dump at lines 4555–4558; field table at lines
4561–4576). Bytes [64,124) of the trailer (first 60 bytes, exactly as the
hex dump gives them) hashed to:

```
CRC32C(trailer[0,60))     = 0x402f157e  (spec states 0x402F157E)  MATCH
```

Open-path walk against this exact file, as a remote reader (F=128, R1's
scenario but with a concrete F):

1. Request 1: `[64, 128)` (64 bytes). Response also discloses F=128
   (transport-authoritative). F ≥ 128: passes `[R-CNT-27]`.
2. Validate trailer in order: magic `8A 4E 52 41 54 0D 0A 1A` at [64,72)
   — matches; CRC at [124,128) = `7E 15 2F 40` little-endian =
   `0x402F157E` — matches my computed value; version_major=1 (implemented);
   flags=0 (no incompat, no ignore bit); dir_offset=16 (≥16, OK);
   dir_length=4 (≥4, OK; 16+4=20 ≤ 128-64=64, OK); committed_file_length=128
   (=F, multiple of 64, OK); file_id=`0x0123456789ABCDEF` (≠0, OK);
   reserved [112,124) zero, OK.
3. Request 2: `[16, 20)` (4 bytes) — the directory region. It is a
   zero-record sequence (0 bytes) plus its CRC over those 0 bytes:
   `00 00 00 00` = `0x00000000`, which is exactly the CRC-32C-of-zero-bytes
   check vector I reproduced above. Matches.
4. Record walk: zero records. Layer table: empty. §21.6 (line 4304)
   records this as a defined, conforming non-violation: "The file
   contains zero layers | A conforming file: a directory carrying no
   layer record is a conforming generation …"

Total requests: 2. Total bytes fetched: 64 + 4 = 68 (out of a 128-byte
file) — the open never touches the 44-byte pre-trailer pad at [20,64).
A local reader additionally verifies [0,16) by equality (`[R-CNT-04]`);
a remote reader whose suffix window does not reach offset 0 may defer
that check — exactly the distinction the document draws at lines
4583–4590, which I independently re-derive here rather than merely
quote.

## Part 6 — Worked example 2: a stored layer, tile-read with real offsets (§7.4's `sst` example, lines 1184–1227, plus §11.2/§11.4/§14.2/§15.4 arithmetic)

I re-derived the two checksums the `sst` example states, from the raw
bytes it specifies (80 bytes of 4 sentinel entries, `FF×16 00×4`
repeated four times, then the CRC-32C of the resulting 4-byte
segment-CRC array):

```
segment CRC over 80 bytes (4 sentinel entries)  = 0x80a34955  MATCH (spec: 0x80A34955)
crc_of_crc_array over that 4-byte array         = 0xc4ee982e  MATCH (spec: 0xC4EE982E)
```

For a *stored* (non-sparse) worked tile-read, I built the R7 scenario by
hand (shown in full under Probe R7 below) and independently re-derived
the document's own two fully-worked arithmetic examples to cross-check my
formula use before trusting it on R7:

- §11.4's example (grid (4,8), tile (1,2) → s=10; in-tile position
  (44,188) → ordinal 44·256+188 = **11,452**; planar channel 2 at that
  spatial ordinal → disk ordinal 2·32+10 = **74**) — I recomputed both
  products by hand and both match.
- §15.4's 1,000,000-entry example: segments = `ceil(1000000/65536)` = 16
  (15 full + 1 of 16,960); index region = `1000000×20 + 16×4` =
  **20,000,064** bytes; entry 999,999 → segment `999999 // 65536` = 15,
  segment-relative index 999999-983040 = 16,959, segment-relative byte
  `16959×20` = **339,180**. All four numbers match the document's stated
  figures exactly.
- §14.2's example (channels `a` uint8, `b` uint16 interleaved, tile
  extents (2,3)): Q=1+2=3, decoded size=6×3=**18**; ordinal
  `1·3+2=5`; byte range `[5·3, 5·3+3) = [15,18)` — matches "bytes [15,
  18)" (line 2102). Planar `b`: 12-byte plane, ordinal 5 → bytes
  `[5·2,5·2+2) = [10,12)` — matches "bytes 10–11". With `t` float32 + `m`
  bool: Q=5, decoded size 30; ordinal 5 → `[25,30)`, `m` at byte
  `25+4=29` — matches exactly. (General form, line 2107–2109: "channel
  c's value at in-tile ordinal u sits at byte u · Q + Fᶜ".)

Having cross-checked the formulas against four independently-verifiable
worked numbers the document itself provides (all four matched), I used
the same formulas, unmodified, for Probe R7's new scenario below.

---

## Part 7 — Seven degradation walks, end to end

### D1. Unknown top-level record type, MU=1 (reject-file) vs. the same type as a layer sub-record, MU=1 (reject-layer)

A top-level record of type `0x1234` (inside the reserved range
`0x0003-0x7FFF`, §10.2 table, line 1607) with flags bit 0 (MU) = 1.
- At open, step 4: `[R-CNT-15]` (line 1087): "An unknown record type at
  file scope: MU = 1 → reject-file." No scope narrower than the whole
  file is available — the type is unknown, so its extent cannot even be
  skipped safely without risking the no-embedded-offsets assumption (the
  rule that makes safe relocation/skipping possible at all, §7.2 line
  1054: "the extent slot is its only sanctioned reference to bytes
  outside the record sequence"); the reader rejects the file outright.
- This specific instance is **also independently a file-conformance
  violation**: emitting a reserved-range type at all is a violation
  whatever its MU bit (`[R-CNT-15]`, register row **F36**, line 3899:
  "A top-level record carries a type value from the reserved range
  0x0003-0x7FFF, which this specification has not assigned; emitting one
  is a violation whatever its MU bit" — detector *verifier*). So an
  ordinary reader's outcome (reject-file) and a verifier's finding
  (nonconforming, via F36) agree on the file being unusable, by two
  independent routes.
- The identical type value, same MU=1, placed as a **sub-record of a
  layer record** instead: `[R-CNT-18]` (line 1177): "an unknown
  sub-record type with MU = 1 is reject-layer, and where the file is
  otherwise conforming a reader MUST NOT reject the file for it."
  Register rows **L24**/**L25** (lines 3937–3938). This is the exact
  divergence Probe R8 asks for, and I answer it there with the same
  citations.
- If instead the type had been in the **experimental** range (≥0x8000)
  with MU=1 at top level: `[R-CNT-15]`'s reader outcome is unchanged
  (reject-file), but §21.6's closing paragraph (lines 4074–4090)
  explicitly says the **file itself is still conforming** — this is one
  of the two named "conforming files a reader nevertheless refuses." The
  byte-level consequence: a verifier reports this file as conforming (no
  register row fires — F35/F36 require the *reserved* range, not
  experimental); an ordinary reader rejects the whole file anyway, purely
  on a capability ground, and the document says the diagnostic "ought to
  distinguish the two" (line 4089) without making that a MUST.

### D2. Unknown/unimplemented codec, core-assigned (zstd, codec 3) — see also Probe R3

Codec value 3 is *assigned* and *core* (`[R-COD-03]`, `[R-CNF-03]`): every
conforming reader MUST implement it. A reader that does not is, by the
text's own words, "not a conforming reader… even if it reads all other
conforming files correctly" (line 192–195, quoted verbatim). This is the
one degradation walk where the register has **no row to land on**: L43
covers an *invalid* codec value (0, reserved, experimental) — not this
case, where the value is perfectly valid and the file perfectly
conforming. I write this up as Finding **readera-01** below; the short
version is: the document defines, in detail, what a conforming
**verifier** does when it cannot execute a codec (§17.4, `[R-COD-11]`,
lines 2634–2646), but it never extends any parallel courtesy to an
ordinary **reader** in the same position — such software is simply
outside every conformance class the document defines, and nothing says
whether it may still serve other layers or list this layer's
declarations.

### D3. Unrecognized flag — two contrasting sub-cases

**D3a (accepted): ignore-lane bit set**, e.g. flags = `0x00010000` (bit
16). `[R-CNT-08]` (line 900–901): "MUST ignore all bits in the ignore
lane (bits 16–31)." §21.6 (line 4049): "An ignore-lane flag bit (16–31)
is set | Ignored; the file is conforming." The reader proceeds exactly
as if flags were 0; no scope is affected.

**D3b (rejected): incompat-lane bit set** — this is Probe R2 exactly
(flags = `0x00000004`, bit 2). Answered in full under R2 below; outcome
reject-file, register row F19, and — unlike D3a — the file is **not**
conforming (F19 is a numbered file-scope violation, §21.2; contrast
§21.6's two *conforming*-file-the-reader-refuses cases, neither of which
is F19).

### D4. Truncated tail (no valid trailer at the physical end of file)

A reader opens a file whose final 64 bytes do not pass `[R-CNT-06]`'s
gates (e.g. the magic bytes are garbage, or they match but the trailer
CRC does not). `[R-LIF-05]` (§9.5): "a reader that finds no valid
trailer in the final 64 bytes MUST report the file torn or invalid and
MUST NOT scan backward." This is the default read path; **only** a
dedicated recovery tool (§9.6, explicitly headed "(not a reader
behavior)") is permitted to probe backward for an earlier commit. An
ordinary conforming reader's outcome here is reject-file via whichever
of F6/F8/F14/F17 the specific corruption trips (the register rows for
the magic, CRC, and length-vs-transport checks respectively); it never
recovers silently and never guesses at an earlier generation.

### D5. Checksum mismatch at tile scope (stored-tile CRC)

A tile's index entry is well-formed (passes §15.3's structural tests)
and its segment/crc_of_crc_array chain verifies, but the stored bytes at
`[offset, offset+length)` do not match the entry's `crc` field. This is
**T1** (register, line 3974): outcome reject-tile, detector *reader*,
detected at tile use, governed by `[R-CNT-20]`. `[R-IDX-03]`'s own
prose (§15.3, lines 2259–2270) is explicit that this is the *one* case
where a malformed-looking situation is **not** treated as a malformed
entry: "An entry whose only defect is that its stored bytes fail its crc
is well-formed: the defect lies in the bytes it addresses, not in the
entry" — so it still counts in run-continuity (§16.2) and in the
coverage walk (§9.7), unlike the six *structural* §15.3 rows. Scope: only
this one tile; every other tile of the layer, including ordinal
neighbors in the same slab run, is unaffected (§2.4's reject-tile
definition, line 310).

### D6. A limit exceeded (resource ground, not corruption)

A layer declares `entry_count = 2^40`. This is within the u64 domain
(`[R-ENC-03]`, ≤2⁶³-1) and, if `extent_length` is set consistently per
`[R-CNT-17]`'s formula (`entry_count×20 + ⌈entry_count/2¹⁶⌉×4`), the file
is **fully conforming** — but it exceeds §21.9's minimum guarantee of
2³² addressed tiles per layer (table at line 4177: "addressed tiles per
layer (entry_count) | 2³²"). `[R-ERR-04]` (lines 4197–4211): the file
"remains conforming, and a reader MAY decline it: at the whole file, or
at the narrowest scope whose stated or derived quantities exceed what it
can serve" — here, the layer. The refusal **MUST be reported as a
resource limit and not as a validity error** (surrounding text, line
4211 area): "a reader that reports 'too large' as 'corrupt' invites the
deletion of intact data." Unlike D2's codec case, this degradation path
**is** fully specified: the reader stays conforming while declining (it
is not disqualified the way a missing-core-codec reader is), it may
still serve every other layer, and it must use the "resource limit"
vocabulary, not reject-layer's ordinary corruption framing (even though
the *mechanism* of declining looks, from outside, like a reject-layer).

### D7. A format major the reader does not implement

`version_major = 2`, reader implements only major 1. `[R-CNT-07]` (§6.3):
reject-file on capability grounds, with a SHOULD that the diagnostic
read as "format major N; this reader supports major 1" rather than
"corrupt" or "not a TARN file" — because the file "can be perfectly
conforming under that major" (§21.6, line 4076–4078). Four conditions
still **reach** such a file regardless (`[R-CNF-13]`, §2.3, with the
worked derivation at the start of §21.2, lines 3855–3858: "Deriving it
there yields F8, F14, F6 and both of F1's instances — each asserting an
invariant `[R-CNT-24]` fixes in every major — and no other row"): the
front-block equality check (F1's front-block instance), the
trailer-magic instance of F1/F8, and the trailer CRC (F14) — because
`[R-CNT-24]` (line 891 onward) fixes exactly those invariants (trailer
magic, major/minor position, the final CRC, and the front block) across
every major, permanently. Every *other* register row is inert against
this file — "it is not assessed against a file declaring another major,
no violation of it is established there" (§2.3). So a reader here does
two things in order: it still validates the four reaching conditions
(and rejects on *those* grounds, citing the specific condition, if any
fails) and only then, if they all pass, falls through to the distinct
capability-ground rejection `[R-CNT-07]` asks for.

---

## Part 7.5 — Probe derivations (full working; answers restated in probe_answers)

**R1.** Scenario: 4,096-byte file, remote transport, ranged requests,
responses disclose complete length. Per Part 1 above: two requests.
- Request 1: `[4032, 4096)` (64 bytes) — the suffix range for the
  trailer; its response also discloses F=4096 (transport-authoritative),
  satisfying step 1 and feeding step 2 in one round trip (§6.4, line
  927–935; §19.1, line 2958–2959).
- Request 2: `[dir_offset, dir_offset+dir_length)` — `dir_length` bytes —
  issued only after the trailer (request 1) has fully passed §6.2's
  ordered gates, since `dir_offset`/`dir_length` are trailer fields
  covered by the trailer CRC (§8.1 map, line 1250) and `[R-ENC-05]`/
  `[R-ENC-10]` (lines 485–487, 527–531) forbid acting on an unverified
  field.
- Total bytes fetched: `64 + dir_length` (dir_length is not fixed by the
  scenario, so the total is expressed in terms of it; the file's 4,096
  total is not itself a bound on dir_length beyond `dir_offset+dir_length
  ≤ F-64 = 4032`, per `[R-CNT-06]`).
- The field that bounds request 2 before it is read: **`dir_offset` and
  `dir_length`**, both trailer fields, both gated by the trailer CRC
  (verified in request 1's response) before being used to form request 2's
  range — this is exactly `[R-ENC-05]`'s "MUST NOT allocate, seek, or
  issue I/O based on any integer obtained from a file before the checksum
  covering it has been verified."

**R2.** flags = `0x00000004` = bit 2 set, bit 2 ∈ [0,15] = the incompat
lane. `[R-CNT-08]` (line 900): "a reader MUST reject-file on any set
bit it does not implement in the incompat lane"; this text defines none,
so every incompat bit is unimplemented. Register row **F19** (line
3882): outcome reject-file, detector reader, detected at open, governing
rule `[R-CNT-08]`. **Is the file conforming?** No. F19 is a numbered
row inside §21.2's "35 conditions" of file-scope *violations* (line
3855: outcome reject-file for the whole table) — contrast §21.6's two
named exceptions, "conforming files a reader nevertheless refuses" (an
unimplemented major, and an experimental-range top-level MU=1 type,
lines 4074–4090), neither of which is F19 and both of which the
document is careful to say are *not* register rows (line 4086: "Neither
is a register row … the register enumerates file-conformance
violations"). F19, being a register row, is therefore an actual
file-conformance violation: this file is not conforming, independent of
any particular reader's capability.

**R3.** Codec 3 (zstd) is core and assigned (`[R-COD-03]`, §17.2:
"all four are core — a conforming reader MUST implement every one of
them"). A reader lacking zstd is, by `[R-CNF-03]` (lines 192–195), **not
a conforming reader at all** — this is not a "which outcome class
applies to the layer" question with a clean register answer, because the
register (§21) enumerates file-conformance violations, and nothing is
wrong with this file: it is fully conforming. The document defines the
parallel situation for a **verifier** in full (§17.4, `[R-COD-11]`,
lines 2634–2646): it "cannot establish that layer's conformance and MUST
NOT certify the file," which is "not a finding that the file is
nonconforming" and yields *cannot establish* only if no other violation
was found. No equivalent text binds an ordinary **reader**. I answer
this probe honestly as underdetermined (see Finding readera-01): the
document does not say whether such a reader may still serve the file's
other layers or list this layer's declarations; my best-supported
reading, by analogy to `[R-ERR-04]`'s narrowest-scope resource-decline
pattern (lines 4197–4200: decline "at the narrowest scope … be that a
layer, a tile, … or the file itself") and to §17.4's verifier treatment,
is that it *may* reasonably confine the damage to the layer and keep
serving the rest — but this is analogy, not a stated rule, and the
document gives no basis to call a different, stricter implementation
nonconforming either (since, per `[R-CNF-03]`, it was never a conforming
reader to begin with, whatever it does next).

**R4.** Entry: `extent_offset = 0xFFFF_FFFF_FFFF_FFFF` (sentinel),
`extent_length ≠` sentinel. §15.3's table (line 2280): "offset = S ∧
length ≠ S, or offset ≠ S ∧ length = S | *structural*: reject-tile."
Register row **T7** (line 3980): "A tile-index entry sets exactly one of
offset and length to the sentinel value … | reader | tile use |
`[R-IDX-03]`." Outcome class: reject-tile. Scope: the tile (the owning
scope of an individual index entry and its stored tile, per §15.1 lines
2215–2216). This is one of the six *structural* rows `[R-IDX-03]` names
(lines 2264–2268): the entry's own 20 bytes yield no usable extent, so
it contributes no stored extent to the coverage walk, to run-continuity
(§16.2), or to the verifier rows — any bytes it nominally addressed fall
to slack if no other claimant claims them (§5.2, §9.7).

**R5.** Directory CRC mismatch. `[R-CNT-11]` (line 977–978): "A reader
MUST verify that CRC before any other use of the region (mismatch:
reject-file)." Register row **F20** (line 3883). Outcome: reject-file.
What may the reader still serve? **Nothing.** §2.4's table (line 310):
"reject-file: The file is not usable; failure is reported for the whole
file. A reader MUST NOT rely on any structure in it." Because the
directory is unverified, the reader cannot even obtain the layer table
(§19.1 step 4 depends on the directory CRC having already passed at
step 3) — there is no layer name, no layer declaration, nothing to list
or serve. The chain of trust (§8.2, line 1259: "trailer → directory →
…") stops at the second link.

**R6.** File is exactly 96 bytes (F=96). §5.1 (line 652–656,
`[R-CNT-27]`): "No conforming file is shorter than 128 bytes … A reader
MUST treat a shorter file as a validity error at file scope." §19.1
step 1 (line 2942–2944) is explicit this is decided "from F alone and
needing no other byte of the file." Register row **F5** (line 3869,
Instances column: "F (physical file size); committed_file_length").
Outcome: reject-file. The single field/fact: F itself (96 < 128),
obtained from the transport (or local filesystem) before any byte of the
file is read.

**R7.** Dimensions declared in order (y, x): E_y=12,T_y=5 then E_x=9,
T_x=4; channels (a uint16, b uint8), interleaved. Sample (y=6,x=5).
- Grid counts: G_y=⌈12/5⌉=3, G_x=⌈9/4⌉=3 (§11.2).
- Tile coords: t_y=6 div 5=1, t_x=5 div 4=1. In-tile position: u_y=6
  mod 5=1, u_x=5 mod 4=1 (§11.4).
- Spatial tile ordinal (row-major, last-declared dim x fastest):
  s = t_y·G_x + t_x = 1·3+1 = **4** (§11.4's formula, with d=2, dims in
  order y then x).
- Interleaved layer ⇒ disk tile ordinal = s = **4** (§11.4: "s for an
  interleaved layer").
- In-tile sample ordinal, same row-major formula over tile extents:
  k = u_y·T_x + u_x = 1·4+1 = **5**.
- Sample stride Q = B_a+B_b = 2+1 = **3** (uint16=2 bytes, uint8=1 byte).
- Channel b's in-sample offset F_b = B_a = **2** (sum of element sizes of
  channels before b, i.e. just `a`).
- Byte offset of channel b's value at in-tile ordinal k, by §14.2's
  worked-example form "channel c's value at in-tile ordinal u sits at
  byte u·Q + F_c" (line 2107–2109): **5·3 + 2 = 17**.
- Sanity: tile P = T_y·T_x = 5·4 = 20 positions; decoded size = P·Q =
  20·3 = 60 bytes; offset 17 and the 2-byte value [17,19) fall well
  inside [0,60). k=5 < P=20. Consistent.

**Answer: disk ordinal 4; channel b's value begins at byte offset 17**
within the decoded tile image.

**R8.** Top-level record, unimplemented type, MU=1. `[R-CNT-15]` (line
1087): "MU = 1 → reject-file." If the type value is in the *reserved*
range this is also, independently, a file-conformance violation (F35 at
open if MU=1 and reserved-range, line 3898; and F36 at certification,
line 3899, whatever the MU bit); if the type value is *experimental*,
§21.6 (lines 4074–4090) says the reader still rejects on this same
capability ground but the **file remains conforming** (one of the two
named "conforming files a reader nevertheless refuses"). Either way, the
**outcome class is reject-file** for the top-level record.

**Does it differ for a sub-record of the same type inside a layer
record?** **Yes.** `[R-CNT-18]` (line 1177): "an unknown sub-record type
with MU = 1 is reject-layer, and where the file is otherwise conforming
a reader MUST NOT reject the file for it." Register rows L24 (reader,
layer access) and L25 (verifier, certification; reserved-range emission
only) at lines 3937–3938. §21.6's closing paragraph is explicit about
exactly this asymmetry (line 4080–4082): "the same type as a layer
sub-record is reject-layer and never a ground to refuse the file
(`[R-CNT-18]`), so only the top-level case is a file a reader refuses."
So: top-level MU=1 unknown type ⇒ whole file unusable; the identical type
value, as a layer sub-record, MU=1 ⇒ only that one layer is unusable,
every other layer and the file as a whole remain servable.

---

## Part 8 — Findings

### readera-01 — AMBIGUITY: no defined reader-side degradation for a core-assigned codec/filter the reader does not implement

**Location.** §2.3 (`[R-CNF-03]`, lines 192–195) vs. §17.4
(`[R-COD-11]`, lines 2634–2646) vs. the layer-scope register (§21.3,
no row).

**The gap.** `[R-CNF-03]` is unambiguous that a reader lacking a core
codec (lines 192–195: "software that declines to support a core codec …
is not a conforming reader, even if it reads all other conforming files
correctly") is disqualified outright. For a **verifier** in the parallel
position, §17.4 spells out a full protocol: it "cannot establish that
layer's conformance and MUST NOT certify the file," this is "not a
finding that the file is nonconforming," and it "fixes the file's
verdict as *cannot establish* only where the verifier established no
violation elsewhere." No analogous text exists for an ordinary reader.
The register (§21.3) has a row for an *invalid* codec value (L43, line
3956) but, correctly, none for *this* condition, since the codec value
here is valid and the file is conforming — there is no file-conformance
violation to register at all; the gap is about reader behavior, not
file conformance.

**Byte-level test.** Does resolving it change which bytes a conforming
implementation may emit or must accept/reject? For the disqualified
reader itself, no — it is already outside every conformance class the
document defines, so nothing in the document binds its bytes one way or
the other. But the document's silence here is a genuine failure to
determine behavior for the realistic case of a reader that implements
*almost* everything: it has **zero textual basis** for deciding whether
it may serve requests against other layers (and the text's own
analogous resource-decline pattern — `[R-ERR-04]`, licensing a decline
"at the narrowest scope … be that a layer, a tile, [or] … the file
itself" — would suggest "yes, decline just this layer," but that pattern
is stated only for limits exceeded, never extended by cross-reference to
a missing core codec). Two independently-built readers facing the exact
same file could reasonably diverge: one treats the whole file as
unusable (since it has disqualified itself from being a reader of
*anything*, on no stated authority to scope its own failure), the other
serves every layer but this one (reasoning by analogy from `[R-ERR-04]`
and from §17.4). The document never says which is right. I mark this
`byte_level: true` because it determines whether a (non-conforming, but
otherwise functioning) implementation's bytes for *other layers* are
served or withheld — a real behavioral fork, not merely a classification
question.

### readera-02 — OBSERVATION: the trailer's "incompat lane" (flags bits 0–15) is permanently unpopulatable under this specification's own closed extension-vehicle list

**Location.** §6.2's trailer layout table (line 840: "bits 0–15
(incompat lane) all zero, a set bit being reject-file (F19)"), §6.3
(lines 900–920), §10.1 (heading at line 1580, vehicle list and
`[R-EXT-01]` at lines 1588–1594), register row F19 (line 3882).

**The observation.** §10.1 states this format "grows through exactly
four vehicles" and lists them; vehicle 3 is, verbatim, "New ignore-lane
flag bits in the trailer (§6.3)" (line 1588) — **not** "new flag bits,"
and not anything naming the incompat lane. `[R-EXT-01]` (lines
1591–1594) then closes the list: "Nothing else extends this format … a
new fixed field … or a reinterpreted assigned value is a new format
major version … never a minor revision." Every mention of the incompat
lane I found (five total: lines 840, 901, 917, 3882, plus the Appendix B
summary) describes it only ever as currently all-zero and a set bit as
always-reject — never as something any minor-version vehicle can
populate. Given `[R-CNT-24]` (line 891 onward) separately guarantees
that a *future major version* "MAY redefine only the remaining 48
trailer bytes" (which already includes the flags field in full)
independent of any incompat/ignore split, a future major does not need
these specific 16 bits pre-reserved either — it can redefine the whole
48-byte remainder, flags included, however it likes. The practical
upshot: for the entire life of format major 1, across every minor
version this text or any successor minor-version text could define, bits
0–15 of the trailer flags are asserted to be always zero, and the
document gives no named mechanism — ever — by which that would change
within major 1.

**Byte-level test.** This does **not** change what bytes a conforming
reader built from this text accepts or rejects today: F19 is unambiguous
and total (any incompat bit set is reject-file, full stop), so I mark
this `byte_level: false`. What is unresolved is design intent/document
self-consistency: naming 16 specific bits "incompat lane" (as distinct
from calling them simply "reserved," the way the 12 trailer bytes at
offset 48 are) implies a purpose — signaling a forward-incompatible
minor-version feature to old readers, the standard reason formats carve
out such a lane — that this document's own closed four-vehicle list
(`[R-EXT-01]`) never actually permits any minor version to exercise.
