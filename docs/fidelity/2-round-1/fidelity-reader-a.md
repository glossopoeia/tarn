# Reader-implementer fidelity walk — edition A — transcript

## 0. Disclosure

**Access.** I read exactly one specification file:
`/Users/robertkleffner/Documents/GitHub/tarn-first-draft/scratch/cleanroom/editions/a/tarn.md`
(4,981 lines). I read it in full, in six sequential chunks (offsets 1,
601, 1201, 1801, 2401, 3001, 3601, 4201 — overlapping where a prior
read's token limit cut a section short), via the Read tool. I did not
open any other copy of this specification, did not list the
repository's other directories, and did not read docs/, PLAN.md,
OPEN-QUESTIONS.md, AGENTS.md, README.md, CONTRIBUTING.md,
conformance/, spec/registry.json, git history, or any web resource.

**Tools used.** Read (on the one permitted file only, at various
offsets); Bash, to run `python3 -I` against a script I wrote myself in
my own scratch directory, computing CRC-32C locally with no file
reads of any kind (it is a pure function over literal byte strings I
transcribed from the specification's own worked examples); Write, to
record working notes and this transcript in my own scratch directory.
I ran no grep/rg in the end — my reads covered the whole file
end-to-end, which is more reliable than a wrapped-text grep for a
document this size, and the brief's warning about hard-wrapped text
spanning grep lines did not end up mattering because I never relied
on a line-oriented search to establish a zero.

**Context I did not ask for.** My runtime placed a number of things in
my context before I began: a project `CLAUDE.md` pointing at an
`AGENTS.md` file I did not open; a long auto-memory file
(`MEMORY.md`) with entries about this project's harness, prior
rounds, calibrations, a lost word-list file, repair processes, and
other process history; a git-status block naming recent commit
subjects ("Readable: §8 — coverage map's exceptions stated in
full...", "Edit log: §7 listed under Ready for calibration 2", etc.);
skill listings; and an environment block. None of this is part of the
specification and none of it is evidence about the specification's
content. I have disregarded all of it as a source of fact about TARN,
and I note in particular that the commit-subject lines name section
numbers and phrases ("coverage map's exceptions," "chain-of-trust
outcomes," "R-CNT-19 and R-CNT-20") that are suggestively close to
material in the one file I did read (§8.1's coverage map, §8.2's
chain of trust, R-CNT-19/20) — I have made no use of that
correspondence beyond noticing it, since treating a commit subject as
corroboration of the file's content would be exactly the contamination
the access rule exists to prevent. I also note the harness-level
framing that accompanied this task (a relayed "user request" about a
model constant and a preflight/launch step, and the instruction that
it takes precedence over the computed brief) — that framing governed
whether I ran this task at all, not what the specification says, and
I have treated it as out-of-band exactly like the rest of the
unrequested context.

**Path check.** The access rule names
`scratch/cleanroom/editions/a/tarn.md` under the stated repository
root. That is exactly the path I read; it existed at that path and
was readable without incident. I take no position on what any other
path under this repository (e.g. a sibling `editions/b/`) contains,
and did not look.

**Scratch directory.** My directory,
`/private/tmp/claude-501/-Users-robertkleffner-Documents-GitHub-tarn-first-draft/fidelity-3/scratch/walk-reader-a/`,
was empty when I started (verified with `ls -la` before writing
anything — no prior attempt's files were present). I wrote two files
there: `crc32c.py` (a from-scratch CRC-32C implementation and a set of
checks against the document's own stated constants) and `notes.md`
(arithmetic scratch for R7 and a summary of the CRC checks). I did not
read or list the shared output directory
(`/private/tmp/.../fidelity-3/out/`) beyond writing this one file to
it by its stated name.

---

## 1. The open path (cold start, every byte fetched, in order)

Document basis: §6.4 (`[R-CNT-09]`, `[R-CNT-10]`), §19.1
(`[R-RDR-01]`), §7.1 (`[R-CNT-11]`).

For a **remote** reader whose transport supports ranged requests and
discloses each response's complete length, the baseline open is
exactly two requests, strictly ordered by data dependency:

1. **Request 1 — suffix range `[F − 64, F)`.** F is not yet known to
   the reader; this is a *suffix* range request (no numeric start
   offset needed), and the transport's response disclosing the
   range's complete length is what gives the reader F
   (`[R-CNT-10]`). The 64 bytes returned are validated in §6.2's
   fixed order: trailer magic; trailer CRC-32C over bytes [0,60);
   version gate (version_major); then, those three passed, the
   remaining field gates together — flags, dir_offset ≥ 16,
   dir_length ≥ 4, dir_offset + dir_length ≤ F − 64, committed_file_
   length = F and a multiple of 64, file_id ≠ 0, reserved bytes zero
   (`[R-CNT-06]`, `[R-CNT-07]`, `[R-CNT-08]`). Any failure here is
   reject-file and the open stops; no second request is issued.
2. **Request 2 — exact range `[dir_offset, dir_offset + dir_length)`.**
   This range's bounds come from two trailer fields —
   **dir_offset bounds the start, dir_length bounds the extent** —
   and neither is used to issue I/O until both have cleared the
   checks above: `[R-ENC-05]` forbids issuing I/O from a field before
   the checksum covering it (the trailer CRC) has verified, and
   `[R-ENC-10]` makes "verify before acting on" general. So the
   field that bounds the second range is the trailer's
   `(dir_offset, dir_length)` pair, and it cannot bound anything
   until request 1's response has passed the trailer CRC and the
   gates that read those two fields. The returned bytes are checked
   against the directory region's own terminal CRC-32C over the
   first dir_length − 4 bytes (`[R-CNT-11]`); mismatch is reject-file
   and the open stops.

With both passed, step 4 of §19.1 (the record walk) runs over bytes
already in hand — no further I/O — building the layer table and
checking per-type multiplicity, non-layer extent-slot validity, and
the user-metadata top-level framing rules, all "decidable from the
resident bytes and F."

**Total bytes fetched to validate trailer and directory:** 64 +
dir_length. **Total requests: 2**, in that order, request 2 strictly
after request 1 (its range is computed from request 1's payload).

A reader MAY instead speculatively fetch a suffix window in one
request and test containment, collapsing to one request when the
directory lies inside the window (§6.4); that is optional, and it is
not what "every request it makes" names for the general, non-
speculating baseline reader this probe (R1) asks about, so I answer
R1 with the two-exact-range baseline and note the alternative.

Opening **consumes the trailer and directory only** — "no extent
slot's content, no tile index, no payload" (`[R-RDR-01]`) — so this
accounting is independent of file size and layer count. Everything
past the open (layer access, tile use, extent use) is driven by what
a particular request actually touches (§19.2) and costs further I/O
only there: layer access costs none (§19.3, all decidable from the
resident directory and F); tile use costs the segment-CRC array
fetch, the containing index segment, and the tile's own payload
(§19.4 steps 3–6, and §15.4's worked numeric example); extent use
(a user-metadata record) costs that extent's bytes.

## 2. Validation timing by tier

Document basis: §19.2 (`[R-RDR-02]`), restated against §19.1,
§19.3, §19.4.

The rule is a **latest-detection-point** rule, not an inventory: a
reader MUST detect any violation whose detector this specification
assigns to the reader no later than the reader's first reliance on
the structure carrying it, and MUST NOT return data from a structure
that hasn't cleared its tier's validation — but MAY detect earlier.
Four tiers:

- **At open:** front signature block (if resident), trailer, directory
  region + record walk, layer-name namespace.
- **At first access to a layer:** the layer record's full validation
  (extent slot, inline payload, value-set and arithmetic bounds, all
  of it — §19.3's long enumeration) — before any use of the layer's
  declarations other than its name.
- **At use of a tile:** index-chain (crc_of_crc_array, segment CRC),
  entry classification, payload CRC, decode — before any sample of
  that tile is returned.
- **At use of a record's extent:** that extent's CRC and the content
  rules its encoding attaches — before anything the extent holds is
  returned.

One sharp point the document is explicit about and that an
implementer must not miss: **a failure's outcome and scope follow the
rule it violates, not the tier at which it is detected.** The worked
case the text gives is the index chain: its failure is layer scope
(`[R-IDX-04]`) even though the *detection point* is tile use. So
"detected at tile use" and "scoped to the layer" coexist for the same
violation — a naive implementer who scopes every tile-use-detected
failure to the tile would be wrong for this one row family (L37, L38).

## 3. Layer access

Document basis: §19.3 (`[R-RDR-03]`).

First access to a layer requires full validation of the layer
record — extent slot and inline payload — entirely from the resident
directory and F, with **no I/O**: slot validity (`[R-CNT-13]`), the
§7.4 constraint set (`[R-CNT-23]`, mutual exclusion of alignment and
slab `[R-CNT-16]`), exact parse / sub-record walk / sub-record
multiplicity (`[R-CNT-18]`, `[R-CNT-14]`), name rules
(`[R-ENC-11]`, `[R-ENC-12]`, `[R-ENC-15]`), the user-metadata
sub-record framing floor, the u64 domain (`[R-ENC-03]`), every
value-set row (layout, linearization, sample type, codec, filter),
per-type fill constraints, the lz4 decoded-size cap (`[R-COD-07]`),
the geometry floor and its arithmetic (`[R-GEO-01]`–`[R-GEO-03]`),
the 2⁶³−1 ceiling on every derived quantity (`[R-ENC-04]`), and the
index cross-checks computable without fetching the index itself
(`[R-CNT-17]`: entry_count against the geometry-derived
addressed-tile count, and extent_length against the
entry_count-derived formula). Note what is explicitly *not* here:
alignment/slab invariants (`[R-SLB-01]`, `[R-SLB-03]`) are
verifier-only — "readers are not obligated to" — so a conforming
reader's layer-access pass is silent on them.

## 4. The tile-read algorithm

Document basis: §19.4 (`[R-RDR-04]`), §15.4 (`[R-IDX-04]`), §17.1
(`[R-COD-01]`, `[R-COD-08]`).

1. **Domain** — clip to extents (point request outside extents fails
   as a request, no file verdict; region request returns the
   intersection).
2. **Ordinals** — tile coords, in-tile ordinal, spatial ordinal s,
   disk ordinal (s interleaved; c·N+s planar).
3. **Index chain** — verify crc_of_crc_array over the fetched
   segment-CRC array and the segment CRC over the fetched segment
   containing the entry (parallelizable, cacheable under
   committed-prefix immutability).
4. **Entry classify** (§15.3) — sentinel short-circuits to fill,
   bit-exact, no payload I/O; malformed entry → reject-tile, never
   fill.
5. **Payload** — fetch [offset, offset+length), verify crc before
   decoding.
6. **Decode** — codec then filter inverse; output length must equal
   the declared decoded size exactly.
7. **Extract** — locate requested values by §14's offset arithmetic;
   never return padding positions.
8. **Return** — bit patterns unaltered. A multi-entry request's
   per-tile failures are bounded to that tile's positions; a
   layer-scope failure (the index chain) bars the rest of the
   request and all further service from the layer, prospectively
   only.

---

## 5. Degradation walks (end to end)

Each walk below names the governing rule(s), the register row where
one exists, the outcome class and scope, and — where the specific
scenario is one of this round's numbered probes — forward-references
the probe answer rather than duplicating the derivation.

### D1. Unknown record type (top-level, MU=1 vs. MU=0; sub-record contrast)
This is probe **R8** below. Short form: top-level unimplemented type
with MU=1 → reject-file (`[R-CNT-15]`, register F35 if the type is in
the reserved range — a conforming file cannot carry an unimplemented
*assigned* type, since both assigned types are registered and every
conforming reader implements both, `[R-CNF-03]`). The same type as a
layer **sub-record** with MU=1 → reject-layer only, and the reader
"MUST NOT reject the file for it" on a file otherwise conforming
(`[R-CNT-18]`). With MU=0 at either scope: ignore-record.

### D2. Unknown codec
This is probe **R3** below.

### D3. Unrecognized flag bit
This is probe **R2** below (the incompat-lane case); for completeness,
the symmetric **ignore-lane** case (bits 16–31) is explicitly a
**non-violation** (§21.6): "Ignored; the file is conforming — such
bits are defined by later minor versions" (`[R-CNT-08]`). So the
walk forks hard on which half of the flags field the unrecognized bit
sits in, and the document is explicit and non-ambiguous about where
the line falls (bit 15/16).

### D4. Truncated tail
Two distinct truncation shapes the document separates cleanly:
- **File shorter than 128 bytes** (probe **R6** below): decided from
  F alone, reject-file, F5/`[R-CNT-27]`.
- **File ≥128 bytes but torn mid-commit** (no valid trailer in the
  final 64 bytes, or a trailer that fails one of its gates because
  the physical tail doesn't match what was committed): the *default
  read path* is "trailer-at-end-or-fail... MUST NOT scan backward"
  (`[R-LIF-05]`). The reader reports the file torn/invalid; it does
  not and cannot distinguish ordinary corruption from a
  mid-commit crash from this vantage point, and is explicitly told
  not to try (§9.2's "what a crash sees" example; §9.5's note that
  residue past a completed commit meets the reader only as an
  ordinary trailer-gate failure). Recovery (backward scan, §9.6) is a
  *deliberate, separate* operation for recovery tools and verifiers,
  never a conforming reader's default path.
- A third shape worth naming because it is easy to miss: a **declared
  but short directory**, i.e. `dir_offset + dir_length > F − 64`
  (register F10) — the directory region itself is truncated by the
  trailer's own arithmetic, caught at open, before any directory
  bytes are even fetched (the range request would be invalid to
  issue).

### D5. Checksum mismatch
This is probe **R5** below (directory CRC, file scope). The tile-scope
sibling is T1 (stored tile vs. its entry's crc field) → reject-tile,
and the layer-scope siblings are L37/L38 (crc_of_crc_array, segment
CRC) → reject-layer, consistent with §8.2's chain-of-trust table
(trailer/directory → reject-file; layer's crc_of_crc_array/CRC
array/segments → reject-layer; stored tile → reject-tile;
user-metadata extent → ignore-record).

### D6. Limit exceeded
Document basis: §21.9 (`[R-ERR-03]`, `[R-ERR-04]`). A file whose
declared or derived quantities exceed a §21.9 *minimum guarantee*
(e.g. >2³² addressed tiles, >8 MiB zstd Window_Size, >16 MiB
user-metadata document) **remains conforming** — these are floors a
reader must accept up to, not caps a file must not exceed. A reader
MAY decline such a file, at the *narrowest* scope whose quantities
exceed what it can serve (file, layer, tile, or the record carrying
the oversized document), but the refusal MUST be reported "as a
resource limit and not as a validity error" (`[R-ERR-04]`) — the
walk explicitly forbids conflating "too large" with "corrupt." A
reader that declines *within* the guaranteed floor (e.g. refuses a
3-billion-tile layer, which is under the 2³² guarantee) is, by the
same rule, simply not a conforming reader.

### D7. Format major the reader does not implement
Document basis: §6.3 (`[R-CNT-07]`), §2.3 (`[R-CNF-13]`), §21.6.
version_major = 0 is a true violation (F18, "declares no major at
all"). version_major ≥ 2 (or any value ≠ 1 the reader doesn't
implement) is handled differently in kind: the reader still rejects
the file (`[R-CNT-07]`), but this is one of the two "conforming files
a reader nevertheless refuses" cases the document names explicitly
(§21.6) — "the file can be perfectly conforming under that major."
The diagnostic obligation differs too: `[R-CNT-07]` SHOULDs a
diagnostic distinct from both "not a TARN file" and "corrupt." And a
small but load-bearing wrinkle: a handful of trailer-level checks
*reach* a file of any major regardless (`[R-CNT-24]`'s fixed 16
bytes: magic at F−64, version fields at F−56, CRC at F−4) — so even
for an unimplemented major, the magic and the trailer CRC are still
checked before the version gate turns the rest of the open away;
`[R-CNF-13]` derives exactly F1, F6, F8, F14 (and no other row) as
reaching across majors.

---

## 6. Worked example (real offsets, checksums checked)

I use the document's own **Appendix A minimal file** (128 bytes, the
smallest conforming file, zero layers) because it is complete, fully
specified down to the byte, and gives me an independent checksum to
verify computationally — exactly what "checking any stated constant
or checksum you can" asks for. I supplement it with the §7.4 `sst`
layer payload example (whose stated index-region CRC and
crc_of_crc_array I also verified) and the §15.4 all-sentinel-segment
constant.

**Layout** (from Appendix A, hex dump reproduced from the document):
```
offset  bytes                                    field
[0,8)   89 54 41 52 4E 0D 0A 1A                   front magic
[8,16)  00 × 8                                    front reserved
[16,20) 00 00 00 00                               directory region: empty record
                                                   sequence + CRC-32C(zero bytes)
[20,64) 00 × 44                                   pre-trailer pad (slack)
[64,72) 8A 4E 52 41 54 0D 0A 1A                   trailer magic
[72,74) 01 00                                      version_major = 1
[74,76) 00 00                                      version_minor = 0
[76,80) 00 00 00 00                               flags = 0
[80,88) 10 00 00 00 00 00 00 00                   dir_offset = 16
[88,96) 04 00 00 00 00 00 00 00                   dir_length = 4
[96,104) 80 00 00 00 00 00 00 00                  committed_file_length = 128
[104,112) EF CD AB 89 67 45 23 01                  file_id = 0x0123456789ABCDEF
[112,124) 00 × 12                                  reserved
[124,128) 7E 15 2F 40                              trailer CRC
```

**Open walk on this exact file** (local reader; a remote reader's
accounting is identical in structure, per §1 above, collapsed to one
request if its speculative window reaches offset 0, which on a
128-byte file means fetching the whole file):

1. F = 128 (≥128, passes `[R-CNT-27]`).
2. Fetch/verify trailer [64,128): magic matches; CRC-32C over
   bytes[0,60) of the trailer (i.e. file bytes [64,124)) must equal
   `7E 15 2F 40` little-endian = 0x402F157E.
3. version_major=1 (implemented); flags=0 (no bit set, both lanes);
   dir_offset=16≥16; dir_length=4≥4; 16+4=20 ≤ 128−64=64 ✓;
   committed_file_length=128=F, 128 mod 64=0 ✓; file_id≠0 ✓;
   reserved[112,124) all zero ✓.
4. Fetch/verify directory [16,20): 0 bytes of record sequence,
   terminal CRC-32C over those zero bytes must equal `00 00 00 00`.
5. Record walk: zero records. Layer table: empty (§21.6: "a directory
   carrying no layer record is a conforming generation").
6. If resident (local reader, or a remote reader whose speculative
   window reached offset 0): verify front block [0,16) by equality
   against `89 54 41 52 4E 0D 0A 1A` + 8 zero bytes.

**Checksum verification (computed, not merely restated).** I wrote a
from-scratch CRC-32C (Castagnoli, reflected, init/final
0xFFFFFFFF, little-endian output) in Python and ran it with
`python3 -I` against literal byte strings transcribed from the
document (no file I/O in the script at all). Results, all exact
matches:

| Claim (document location) | Computed | Document states | Match |
|---|---|---|---|
| CRC-32C("123456789") (§4.5 check vector) | 0xE3069283 | 0xE3069283 | yes |
| CRC-32C(zero bytes) (§4.5 check vector) | 0x00000000 | 0x00000000 | yes |
| Appendix A trailer CRC, over trailer bytes [0,60) | 0x402F157E | 0x402F157E (`7E 15 2F 40` LE) | yes |
| §7.4 `sst` example: CRC-32C of the 80-byte all-sentinel index region (4 entries × 20 bytes, `FF×16 00×4` each) | 0x80A34955 | 0x80A34955 (`55 49 A3 80` LE) | yes |
| §7.4 `sst` example: crc_of_crc_array = CRC-32C of that one 4-byte segment-CRC value | 0xC4EE982E | 0xC4EE982E (`2E 98 EE C4` LE) | yes |
| §15.4: CRC-32C of a full 2¹⁶-entry all-sentinel segment (1,310,720 bytes) | 0xEECB3BB2 | 0xEECB3BB2 | yes |

All six independently reproduce. This is a meaningful cross-check:
the document's CRC-32C parameterization (§4.5: polynomial 0x1EDC6F41,
reflected in/out, init 0xFFFFFFFF, final XOR 0xFFFFFFFF) is stated in
words, and every numeric consequence of that statement I could check
without reading another file came out exactly as claimed — including
a non-trivial 1.3 MB computation (the full-segment constant), which
is a stronger check than the two short check-vectors alone would be.

---

## 7. Probe answers (derivations; see structured output for final text)

### R1 — remote open, 4,096-byte file
See §1 above. Two requests: (1) suffix `[4032, 4096)` — the trailer;
(2) `[dir_offset, dir_offset+dir_length)` — the directory, whose
start and extent are bounded by the trailer's `dir_offset` and
`dir_length` fields respectively, usable only after the trailer CRC
verifies. Total bytes: 64 + dir_length.

### R2 — flags = 0x00000004
Bit numbering: bit 0 = LSB (§4.4). 0x00000004 = bit 2 set. Bits 0–15
are the incompat lane (§6.2's table; §6.3). This text defines no
flag bits at all, so bit 2 is unimplemented in the incompat lane.
Outcome: **reject-file**, register row **F19**, governing
`[R-CNT-08]`. The file is **not conforming** (F19 is a §21.2
file-scope violation; F19's own text: "every such bit is
unimplemented").

### R3 — layer declares codec 3 (zstd), reader doesn't implement zstd
Codec 3 is an **assigned, core** value (§17.2, `[R-COD-03]`: "all
four are core — a conforming reader MUST implement every one of
them"). This is categorically different from an unknown
(reserved/experimental) codec value, which *is* a layer-scope
register row (L43, reject-layer). For an assigned core value the
document's answer is `[R-CNF-03]`: software that cannot execute it
"is not a conforming reader, **even if it reads all other conforming
files correctly**." So: there is no register outcome class for this
condition, because the file carries no violation — the deficiency is
the reader's. Whether such software "may still serve other layers"
or "list this layer's declarations" is not governed by this
specification's reader obligations, because by definition it is
outside the class those obligations bind; nothing stops an
implementation from doing either as an engineering choice, but doing
so does not make it a conforming reader, and the document gives no
degraded-conformance tier for "conforming except for one codec."

### R4 — tile-index entry: extent_offset = sentinel, extent_length ≠ sentinel
§15.3's table, third row: "offset = S ∧ length ≠ S, or offset ≠ S ∧
length = S" → *structural*: reject-tile. Register row **T7** ("A
tile-index entry sets exactly one of offset and length to the
sentinel value"; this instance is the "offset" instance of T7, since
it is the offset field that holds the sentinel while length does
not). Scope: tile (`[R-IDX-03]`).

### R5 — directory CRC mismatch
Register row **F20**, governing `[R-CNT-11]` ("A reader MUST verify
that CRC before any other use of the region... mismatch:
reject-file"). Outcome: reject-file. Per §2.4's definition of that
outcome, "A reader MUST NOT rely on any structure in it" — so nothing
is served: not a layer list, not any sample, nothing. (Contrast R3,
where declining is a capability statement about the reader; here the
file itself fails, and the §2.4 reject-file outcome is unconditional
in what it withholds.)

### R6 — file exactly 96 bytes
F = 96 < 128. Decided from F **alone** — no other byte need be read —
per `[R-CNT-27]` ("No conforming file is shorter than 128 bytes...
cannot be satisfied in fewer"). Register row **F5**: "File size is
below the 128-byte minimum... decided from F alone and needing no
other byte of the file." Outcome: reject-file.

### R7 — interleaved layer, y(12,5) then x(9,4), channels a(uint16), b(uint8); sample (y=6, x=5)
See full arithmetic in §0 of my notes and above. Gy=⌈12/5⌉=3,
Gx=⌈9/4⌉=3. ty=6÷5=1, uy=6 mod 5=1; tx=5÷4=1, ux=5 mod 4=1.
Spatial/disk ordinal (interleaved, linearization 1, last-declared
dim — x — fastest, `[R-GEO-06]`): s = ty·Gx + tx = 1·3+1 = **4**.
In-tile sample ordinal u = uy·Tx + ux = 1·4+1 = 5. Sample stride
Q = B_a+B_b = 2+1 = 3; channel b's in-sample offset F_b = B_a = 2
(§14.2's closing example gives exactly this form: "channel c's value
at in-tile ordinal u sits at byte u·Q + Fᶜ"). Byte offset =
u·Q + F_b = 5·3+2 = **17**.
**Disk ordinal: 4. Byte offset of channel b's value: 17.**

### R8 — top-level record, unimplemented type, MU=1; vs. same type as layer sub-record
Top-level, file scope: `[R-CNT-15]` — "An unknown record type at file
scope: MU = 1 → reject-file." (If the type value is in the reserved
range, this is additionally register row F35/F36; if it is in the
experimental range, emitting it with MU=1 is itself not a
file-conformance violation per §21.6, but the reader still rejects
the file — one of the two "conforming files a reader nevertheless
refuses" cases the document names.) **Outcome: reject-file.**
As a **sub-record** of the same unimplemented type inside a layer
record: `[R-CNT-18]` — "an unknown sub-record type with MU = 1 is
reject-layer, and where the file is otherwise conforming a reader
MUST NOT reject the file for it." **Outcome: reject-layer — it
differs.** The file-scope and layer-scope treatments of an identical
type value and MU bit are deliberately different, and the document
is explicit (not merely silent) that the file must not be rejected
whole for the sub-record case.

---

## 8. Findings

See structured output (`findings`, ids `readera-01`...). Summary:
one finding, an OBSERVATION about the asymmetry probe R3 exposes
(core-but-unimplemented codec vs. reserved/experimental codec value),
which I judged not byte-level (it changes nothing about what bytes a
conforming implementation may emit or must accept/reject, since a
conforming reader by definition implements all four core codecs; the
asymmetry only affects how one describes non-conforming software).
I looked for genuine ambiguities/contradictions elsewhere in the
probe set (R1–R8) and in the five-plus degradation walks and did not
find one that survives re-reading the cited passage twice: in each
case where two sections both bear on the same act (e.g. §6.2's
trailer table and §6.3's flag-gate prose for R2; §7.3's top-level MU
rule and §7.4/§20.4's sub-record MU rule for R8), the two passages
state the same rule in different words or state a deliberate,
explicit asymmetry rather than disagreeing.
