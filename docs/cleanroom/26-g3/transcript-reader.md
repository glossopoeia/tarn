# Cleanroom round 26 — Reader implementer transcript

## 0. Disclosure

I read exactly one file: `/Users/robertkleffner/Documents/GitHub/tarn/spec/tarn.md`
(4,484 lines). It was where the brief said it would be. I opened no other file in
the repository — no `docs/`, no `PLAN.md`, no `OPEN-QUESTIONS.md`, no
`conformance/`, no `spec/registry.json`, no ADRs, no git history commands.

Two pieces of context arrived before I began, which I did not ask for and did not
act on as evidence:

1. A project-instruction preamble (`CLAUDE.md` → `AGENTS.md` pointer) and an index
   of the maintainer's memory notes, listing note titles about working cadence,
   naming constraints, and prior workflow failures. I did not open any of them and
   I have used none of their content.
2. **The environment block printed the repository's five most recent commit
   subject lines.** Two of them name specific sections and the shape of a repair.
   This is material the access rule plainly intends me not to have, and I am
   naming it rather than pretending otherwise. Its effect on my walk: it
   corroborated two suspicions the charter's hint list had already pointed me at
   (§11.1 and §16.2). I did not use it to *settle* anything — every finding below
   is argued from the document's own text and I have quoted that text. But I
   cannot claim the walk was clean of it, so I am disclosing it as a breach of
   the round's independence, not as a footnote.

Computation I ran: local Python only, reading no project file. A CRC-32C
implementation (used to check the document's stated constants), a mechanical
instance-count over the §21 register tables extracted from the one file I am
permitted to read, and a builder + independent reader for a synthetic TARN file
I constructed myself from the document. No web access, no other tooling.

---

## 1. What I built

I implemented, on paper and then in Python, a conforming reader: the open path,
validation timing by tier, layer access, the tile-read algorithm, and the
degradation walks. I then built a complete conforming file from the document
alone and read it back with the reader. Everything below is the actual walk.

---

## 2. Preliminaries — the constants I could check

§4.5 fixes CRC-32C (Castagnoli 0x1EDC6F41, reflected in/out, init 0xFFFFFFFF,
final XOR 0xFFFFFFFF, stored little-endian) and gives a check vector. I
implemented it and reproduced every stated constant in the document:

| Constant | Document | Computed |
|---|---|---|
| CRC-32C("123456789") (§4.5) | 0xE3069283 | 0xe3069283 |
| CRC-32C(zero bytes) (§4.5) | 0x00000000 | 0x0 |
| Appendix A trailer CRC over [0,60) | 0xE00938D2 | 0xe00938d2 |
| §7.4 example: CRC of 4 sentinel entries (80 bytes) | 0x80A34955 | 0x80a34955 |
| §7.4 example: crc_of_crc_array over `55 49 A3 80` | 0xC4EE982E | 0xc4ee982e |
| §15.4 / Appendix B: CRC of a full 2^16-sentinel segment | 0xEECB3BB2 | 0xeecb3bb2 |

All six check. I also re-derived, by hand, every worked numeric example I could:

- §11.2: (1024,2048)/(256,256) → G=(4,8), N=32, P=65536. With E_y=1000, G_y=4. ✓
- §11.4: (300,700) → tile (1,2), s = 1·8+2 = 10; in-tile (44,188), ordinal
  44·256+188 = 11,452; planar C=4 channel 2 → 2·32+10 = 74. ✓
- §14.2: interleaved (2,3), a:uint8 b:uint16 → Q=3, 18 bytes, ordinal 5 at
  [15,18). Planar b: 12 bytes, ordinal 5 at 10–11. t:float32 m:bool → Q=5,
  30 bytes, ordinal 5 at [25,30), m at byte 29. ✓
- §14.3: planar bool (2,5), P=10, alternating → `55 01` (fill false) / `55 FD`
  (fill true, pad bits 2–7 set). ✓
- §14.5: (5,5)/(4,4), edge tile (1,1): 1 real + 15 padding, uint16 fill 0xABCD,
  32 bytes. ✓
- §15.4: entry_count 1,000,000 → 16 segments (15 full + 16,960), 64-byte CRC
  array, region 20,000,064 bytes; k=999,999 in segment 15 at segment-relative
  byte 20·16,959 = 339,180; CRC array at [20,000,000, 20,000,064); segment 15 at
  [19,660,800, 20,000,000). Full segment = 65,536·20 = 1,310,720 = 1.25 MiB. ✓
- §15.4: planar C=4 N=32, channel 2 at s=10 → ordinal 74, region bytes
  [1,480, 1,500); channel 3's tiles are ordinals 96–127. ✓
- §17.3: three float32 1.0/2.0/3.0, s=4 n=3, shuffled to
  `00 00 00 00 00 00 80 00 40 3F 40 40`. I recomputed byte-by-byte from
  "byte i of group j at offset i·n+j". ✓
- §20.3: 32-tile index region = 32·20 + 4 = 644. ✓
- §21.9 note: 2^32 tiles → 2^16 segments × 4 = 256 KiB; 2^36 → 4 MiB. ✓
- §5.1 / Appendix A: 16 + 4 + 44 + 64 = 128. ✓

I found no stated constant, offset or checksum in this document to be wrong.
That is a meaningful negative result and I record it as one.

---

## 3. The open path, byte-exact

### 3.1 Cold remote open

§19.1 gives four steps; §6.4 gives the accounting. Implementing it literally:

**Request 1** — a suffix range `bytes=-64`. 64 bytes. Its response carries the
transport-authoritative file size F (`[R-CNT-10]`: "a full-response content
length, the complete length of a range response, or a size probe"), which is why
§19.1's steps 1 and 2 "cost one request between them". Nothing bounds this range
before I have read it except the constant 64 — that is the whole point of
tail-anchoring.

Validation on those 64 bytes, in §6.2's *mandated* order:

1. trailer magic `8A 4E 52 41 54 0D 0A 1A` at [F−64, F−56)  → F8/F1
2. trailer CRC: u32 at [F−4, F) == CRC-32C over [F−64, F−4) → F14
3. version gate: version_major == 1 (0 invalid → F18; other → capability refusal)
4. then, and only then: flag gates (incompat lane bits 0–15 must be clear →
   F19), committed_file_length == transport size and ≡ 0 mod 64 (F17, F13),
   dir_offset ≥ 16 (F9), dir_length ≥ 4 (F16), dir_offset + dir_length ≤ F − 64
   (F10), 1 ≤ generation ≤ 2^63−1 (F11), file_id ≠ 0 (F12), reserved [56,60)
   zero (F15). Also `[R-ENC-03]`/`[R-ENC-04]`: each u64 ≤ 2^63−1 (F2) and the
   sum non-wrapping (F3).

The ordering matters and is a MUST, which is what makes §21.2's preamble true:
only the magic, the CRC and the front block precede the version gate, so a file
declaring a foreign major is refused on capability grounds before its geometry is
ever judged. I checked the preamble's arithmetic: it names **four rows** as
reaching such a file — F8, F1's trailer-magic instance, F14, and F6 with F1's
front-block instance — and those are exactly the checks §6.2 and `[R-CNT-04]`
place ahead of the gate. F18 is correctly excluded as "outside the premise".

I also checked the case the preamble does *not* name: F5 (file below 128 bytes).
A 96-byte file declaring version_major = 2 has a readable magic at F−64 = 32 and
a readable CRC at F−4 = 92, so the reader reaches the version gate and refuses on
capability grounds — F5 never fires, consistent with the preamble. A file shorter
than 64 bytes has no trailer at all and is F5. That hangs together.

**Request 2** — `bytes=dir_offset–(dir_offset+dir_length−1)`. dir_length bytes.
What bounds it before I read it: dir_offset ≥ 16, dir_length ≥ 4, and
dir_offset + dir_length ≤ F − 64, all read from a CRC-verified trailer, so
`[R-ENC-05]` is satisfied. §21.9 obliges me to accept dir_length up to 16 MiB.

**Total cold remote open: 2 requests, 64 + dir_length bytes.** For Appendix A's
128-byte file that is 2 requests and 68 bytes — 64 at [64,128) and 4 at [16,20).
Appendix A states exactly this and it is right.

**The front block is not in that accounting.** `[R-CNT-04]` turns the obligation
on *residency*, not transport: a reader whose open leaves [0,16) resident MUST
verify the 16 bytes by equality before other processing; one that would have to
issue a further range request MAY defer or omit it. So the minimal remote open
never touches offset 0. I note in passing that this means two conforming readers
can disagree about accept/reject on a file whose front block is corrupt (the
speculating one rejects, the exact-range one serves) — but the file is
nonconforming, `[R-CNF-12]` licenses either, and the divergence is designed and
stated. Not a defect.

A reader that speculates a suffix window instead: one request, and containment
decides whether request 2 is needed. §6.4's writer SHOULD — dir_length + pad + 64
within 65,536 — is exactly F − dir_offset ≤ 65,536, i.e. the condition under
which a 64 KiB suffix captures both. I checked that identity.

Appendix A's closing paragraph adds a case I verified: a 112-byte window covering
[16,128) contains the directory (so request 2 is spared) while leaving [0,16)
non-resident (so the front check is optional). Correct on this file.

`[R-CNT-10]`'s 200-response rule is a real trap and is stated: a range request
answered with the whole body must be aborted or accepted deliberately, never
treated as the requested range prefix. My reader does the former.

### 3.2 Record walk (step 4)

Verify the directory CRC (last 4 bytes over the preceding dir_length − 4) before
any other use — F20. Then parse [dir_offset, dir_offset + dir_length − 4) as
zero or more 24-byte headers each followed by inline_length bytes, with no
residue (F29). Per record: type ≠ 0 (F24); unknown top-level type gated by MU
(`[R-CNT-15]`: MU=1 → reject-file, MU=0 → ignore-record); multiplicity
(`[R-CNT-14]`: at most one top-level user-metadata record → F34); extent-slot
validity for **non-layer** top-level records only (F30/F31/F32); and for a
top-level user-metadata record the three framing checks §19.1 enumerates —
no (0,0) slot (F21), extent_length ≥ 5 (F22), inline_length exactly 1 (F23).

Layer records' extent slots are *not* checked here; they are layer-access work
(L15/L16/L17), which is why the open's cost is independent of layer count.

The layer-name namespace is built here. §19.1 is unusually careful about it and I
tested my reading against the register: uniqueness is decided **first**, over raw
bytes, whether or not each name is well-formed, so two byte-identical ill-formed
names are F4 (reject-file) rather than two L3/L5/L6 (reject-layer) findings. F4's
condition text carries the matching qualifier — "both obtainable within their
records' inline_length" — and a layer record whose name field overruns
inline_length contributes no name and is instead reject-layer (L23's leading-
fixed-fields instance). This is a place where an implementer could easily diverge
and the document closes it. Good.

I noticed that §19.1 step 4 cites only `[R-ENC-12]` for the name check while L3's
governing rule is `[R-ENC-11]` (well-formed UTF-8) and §19.3 cites both for
dimension and channel names. §19's own preamble covers this ("A row this section
does not restate is due at its own tier all the same"), so it is not a gap.

---

## 4. Validation timing by tier

The four tiers of §19.2, and what my reader does at each:

**At open** — front block (if resident), trailer, directory region and its record
walk, the layer-name namespace. Also, per §19's preamble and the register's
*Detected* column: L3, L5, L6 (layer record name validity) and R1's top-level
instance (a user-metadata record's encoding byte, which is inline and therefore
resident). §19.1 does not restate R1 and does not need to.

**At first access to a layer** — §19.3's full validation of the layer record. I
implemented the whole list: slot validity, the §7.4 constraint set, exact parse
and sub-record walk, sub-record multiplicity, dimension/channel name rules, the
user-metadata sub-record framing trio, fixed widths and the u64 domain, the value
sets of §11.4/§12.2/§14.1/§15.1/§17.2/§17.3, the bool fill constraint, the lz4
declaration cap, the geometry floor and its arithmetic, the 2^63−1 ceiling on
every derived product, and the two index cross-checks that need no I/O
(`[R-CNT-17]`: entry_count against the geometry-derived addressed count, and
extent_length against entry_count × 20 + ⌈entry_count/2^16⌉ × 4). "layer access
performs no fetch" is true — I confirmed every one of these is decidable from
the resident directory plus F.

**At use of a tile** — the index chain (crc_of_crc_array, then the segment CRC),
entry classification, payload CRC, decode, size.

**At use of a record's extent** — that extent's CRC (R2) and the document content
rules §18.2 attaches at the encoding (R3–R10). No earlier, because the open
fetches no extent.

**What a reader is permitted never to check.** I derived this by taking every
register row whose Detector is *verifier*: F7, F25, F26, F27, F28, F33, F36,
L18, L25, L40, L41, L42, L46, L47, L48, L49, T2, T4, T5, T26. In prose: the
pre-trailer gap's emptiness, extent overlap and the coverage partition, record
flag hygiene (reserved bits, MU=1/PE=0, a registered type's stored bits),
reserved-range type values, alignment and slab invariants, decoded-content
obligations (padding positions, pad bits, interleaved boolean bytes), filter
stride, and user-metadata member ordering. Plus the front block when not
resident (`[R-CNT-04]`) and the slack total. That list is consistent everywhere
I cross-checked it: §5.2's Note ("Coverage is checked by verifiers, never by
readers"), §16.1/§16.2 ("readers are not obligated to"), §14.5 ("not obligated
to check it"), §14.2's `[R-SER-08]`, §6.2's `[R-CNT-05]` ("readers check
neither"), and Appendix H's verifier checklist.

**What becomes a verdict when.** `[R-CNF-11]` gives a verifier three verdicts.
An established violation wins over any number of unchecked requirements; *cannot
establish* is available only to a traversal that established none; *unexamined*
constrains the report and not the verdict. The cannot-establish grounds are
enumerated with "as when", i.e. openly: foreign major, an unimplemented MU=1
type, an unexecutable codec/filter, a declined decode on resource grounds, a
declined user-metadata decode. An unassigned metadata encoding is expressly *not*
such a ground (`[R-MTA-10]`) — no content rule attaches, so nothing is left
unchecked, and the verifier certifies while naming the record. I found this
consistent between §2.3, §17.4, §18.2, §21.5's preamble, §21.6 and Appendix H.

---

## 5. Layer access and the tile-read algorithm

### 5.1 From layer record to geometry

Parse the inline payload in §7.4's table order, packed, no padding. I wrote the
parser and ran it against my own file (below). Derived quantities:

- G_i = ⌈E_i/T_i⌉, stated as E_i/T_i + (1 if E_i mod T_i ≠ 0) to avoid the
  (E+T−1)/T idiom whose intermediate sum can leave the declared domain. I used
  the stated form.
- N = ∏G_i, P = ∏T_i, addressed-tile count = N (interleaved) or C·N (planar),
  total sample positions N·P.
- Q = Σ B_i (sample stride), F_c = Σ_{j<c} B_j.
- Decoded size: interleaved P·Q; planar numeric P·B^c; planar bool ⌈P/8⌉.

Every one of these is subject to `[R-ENC-04]`'s 2^63−1 ceiling, and L2's instance
list is the enumeration a reader needs. I derived the members independently and
compared: layer/sub-record extent sums, N, P, N·P, C·N (which dominates the max
disk ordinal (C−1)·N + (N−1) = C·N − 1), P·Q (which dominates V = P·C, since
Q ≥ C), P·B^c, and the index extent_length formula. That is complete — every
other derived quantity in the document (G_i ≤ E_i, the in-tile ordinal < P, the
spatial ordinal < N, ⌈P/8⌉ ≤ P, the segment count inside the formula, F_c ≤ Q) is
dominated by a listed one. L2's cell is right.

### 5.2 Index chain

Region = [extent_offset, extent_offset + extent_length), laid out as
entry_count × 20 bytes of entries followed by ⌈entry_count/2^16⌉ × 4 bytes of
segment CRCs, no padding anywhere. Entry k at region byte 20k. Segment s covers
[s·2^16, min((s+1)·2^16, entry_count)).

To read tile k a cold remote reader issues **three** requests: the CRC array
(⌈entry_count/2^16⌉ × 4 bytes), the segment containing k (at most 1.25 MiB), and
the payload (length bytes). §1's pillar and §19.4 agree, and §15.4's worked
example gives the numbers. The array is the only term that grows with the layer,
which is what §21.9's 2^32 tile-count guarantee is sized against (256 KiB array).

Verification order is forced: crc_of_crc_array (covered by the directory CRC) over
the array, then the segment CRC (covered by the array) over the segment, then the
entry's crc over the payload. `[R-ENC-05]` forbids issuing the payload fetch
before the entry's bytes are covered — so the segment CRC must verify first. My
reader does this and I confirmed the chain in §8.2 is exactly it.

### 5.3 Entry classification

§15.3's eleven rows. I checked the table is exhaustive and mutually consistent,
and that it maps one-to-one onto §21.4:

| §15.3 row | §21.4 |
|---|---|
| sentinel (S,S,0) | not a violation (§21.6) |
| S,S,crc≠0 | T6 |
| exactly one of offset/length = S | T7 |
| length = 0 non-sentinel | T10 |
| offset < 16 non-sentinel | T8 |
| offset or length > 2^63−1 non-sentinel | T11 |
| sum overflows / > F−64 | T12 / T9 |
| stored bytes fail crc | T1 |
| intra-layer overlap | L18 |
| cross-scope overlap | F33 |
| alignment or slab invariant | L40 / L41 / L42 |

`[R-IDX-03]` says "Six rows are marked *structural*" — I counted six. Three are
marked *verifier* — I counted three. Eleven rows total. The counts hold.

The structural/well-formed distinction is load-bearing and I tested it three
ways. A structurally-bad entry (a) contributes no stored extent to the verifier
rows, (b) is transparent to slab run continuity, and (c) contributes nothing to
`[R-LIF-08]`'s coverage walk, so the bytes it nominally addressed fall to slack.
An entry whose *only* defect is a failed payload crc is well-formed: its extent
stands in all three. That is coherent, and it is what makes `[R-SLB-03]`'s
invariant decidable from index entries plus F without fetching a payload — a
claim I checked and believe.

### 5.4 Decode and extract

Codec, then the filter's inverse. Byte-shuffle's inverse restores byte i·n+j to
offset j·s+i, with s = B^c (planar numeric), Q (interleaved), 1 and identity
(packed bool plane); L is divisible by s in every case, which I verified for all
three layouts. Then `[R-SER-07]`: the decoded length must equal the
declaration-derived decoded size exactly, and I allocate from the declarations,
never from the payload or an embedded size field.

Extraction: channel c's value at in-tile ordinal u sits at u·Q + F_c
(interleaved) or u·B^c (planar numeric) or bit u mod 8 of byte u div 8 (packed
bool). Padding positions are never returned.

---

## 6. The worked example — I built a file and read it back

Appendix A's 128-byte file checks out (§2 above). To exercise more of the format
I built my own from the document alone: the §7.4 example layer as a complete
file.

Layer `sst`, rank 1, dimension `x` with E=100 T=32, interleaved, one float32
channel `temp` with fill 0x7FC00000, codec 1, filter 1, no alignment, no slab,
no sub-records. All four tiles stored, each carrying float32(x) at real
positions and the fill at padding positions.

Derived: G = ⌈100/32⌉ = 4, N = 4, P = 32, C = 1, Q = 4, decoded size P·Q = 128,
entry_count = 4, index extent_length = 4·20 + ⌈4/65536⌉·4 = 84.

The inline payload came out to **81 bytes** — matching §7.4's example exactly,
including its field-by-field byte offsets (name 0–3, layout 4, linearization 5–6,
codec 7–8, filter 9–10, A 11–18, S 19–26, A_slab 27–34, rank 35, C 36–37,
dimension entry 38–55, channel entry 56–67, index_encoding 68, entry_count
69–76, crc_of_crc_array 77–80). §7.4's own accounting — 4 + 34 + 18 + 12 + 13 =
81 — is right, and the "nine scalars from layout through channel count" are
indeed 34 bytes.

Layout of my file:

```
[0,16)      front signature block
[16,144)    tile 0 payload   (128 bytes)
[144,272)   tile 1
[272,400)   tile 2
[400,528)   tile 3           (positions 100..127 = 28 padding positions, all fill)
[528,612)   tile-index region (4 entries × 20 + one 4-byte segment CRC = 84)
[612,721)   directory region  (24-byte header + 81 inline + 4 CRC = 109)
[721,768)   pre-trailer pad   (47 bytes, slack)
[768,832)   trailer
F = 832, 832 mod 64 = 0, dir_offset + dir_length = 721 ≤ F − 64 = 768
```

I then ran an independent reader over the bytes, following §19.1 and §19.4 step
by step, and it:

- verified the front block by equality (bytes resident, local whole-file read);
- validated the trailer in §6.2's order and every field gate;
- verified the directory CRC and walked one layer record;
- performed §19.3's layer validation, including `[R-CNT-17]`'s two cross-checks
  (entry_count == N == 4; extent_length == 84);
- for x = 0, 1, 31, 32, 96, 99: verified crc_of_crc_array, then the single
  segment CRC, classified the entry, verified the payload crc, checked
  `[R-COD-04]`'s codec-1 length equality and `[R-SER-07]`'s decoded size, and
  returned the correct float32 bit patterns (`00000000`, `0000803f`, `0000f841`,
  `00000042`, `0000c042`, `0000c642`);
- failed x = 100 and x = −1 as *requests*, with no verdict on the file
  (`[R-MDL-01]`, §21.6's second row);
- confirmed tile 3's 28 padding positions all hold the recorded fill
  (`[R-SER-05]`);
- computed the coverage partition: claimed = 16 + 4·128 + 84 + 109 + 64 = 785,
  F = 832, **slack = 47** — exactly the pre-trailer pad, which is what
  `[R-CNT-21]` says a verifier reports.

The document was sufficient to build and read this file with no guesswork
anywhere on the happy path. That is the strongest positive result of this walk.

---

## 7. Degradation walks

Seven traced end to end.

**(1) Unknown record type, top-level, MU = 1.** Reader reaches it at open in
step 4. `[R-CNT-15]`: reject-file. If the type is from the experimental range,
the file is *conforming* and the reader refuses it anyway — §21.6 names this as
one of exactly two "conforming files a reader nevertheless refuses", and the
diagnostic ought to distinguish capability from corruption. If from the reserved
range, the emission is itself a violation: F35 (reader) for the MU=1 case and
F36 (verifier) for any MU bit. Nothing is served from the file.

**(2) Unknown sub-record type, MU = 1.** Detected at layer access. Reject-layer,
and — the qualifier is load-bearing — "where the file is otherwise conforming a
reader MUST NOT reject the file for it". So the caller still gets every other
layer, and may still be told this layer's *name* (§2.4's reject-layer row).
Register rows L24/L25 for the reserved-range case. With MU = 0 it is
ignore-record and the layer is fully readable.

**(3) Unknown codec.** codec = 5 (reserved) → L43, reject-layer at layer access,
before any fetch. The layer's name remains listable; every other layer is
unaffected; nothing of this layer's data may be returned, and fill is never a
fallback (`[R-CNF-09]`). A reader that *cannot execute* an assigned codec is not
a conforming reader at all (`[R-CNF-03]`, `[R-COD-11]`), so this branch only ever
fires on reserved/experimental values. For a verifier the parallel case is
*cannot establish*, not *nonconforming*.

**(4) Truncated / torn tail.** §9.5's default path is trailer-at-end-or-fail and
the reader MUST NOT scan backward. I enumerated what a torn tail can look like
and checked §9.6's claim that only three rows can fire:

- tail is arbitrary payload → magic fails → **F8**;
- tail is a partially written trailer → magic passes, CRC fails → **F14**;
- tail is an intact older trailer with residue beyond it → magic and CRC pass,
  committed_file_length ≠ transport size → **F17**.

Because magic + CRC passing means the 60 covered bytes are a genuine trailer,
version_major and the 64-alignment cannot then be wrong, so nothing else can
fire first. §9.6's "(§21.2 rows F8, F14 and F17)" is exhaustive. I checked it.
§9.5's Note on residue is right too: the reader cannot tell residue from
corruption and is not asked to; what residue violates is `[R-LIF-04]`'s *writer*
obligation. Recovery is a separate deliberate operation, probing 64-aligned
offsets o for the magic and requiring CRC + committed_file_length = o + 64, with
the output re-verified whole.

**(5) Checksum mismatch, per scope.** trailer → reject-file (F14); directory →
reject-file (F20); crc_of_crc_array → reject-layer (L37); a segment CRC →
reject-layer (L38); a stored tile's crc → reject-tile (T1); a user-metadata
extent's CRC → ignore-record with a SHOULD-report (R2). I traced the last one:
the quarantine holds "notwithstanding the owning-scope mapping of `[R-CNF-08]`",
so a corrupt *file-scope* metadata document still costs only that record. What
the caller still gets: everything except the lost document.

**(6) Limit exceeded.** §21.9's eight rows are *minimum guarantees*, not caps. A
file above one of them stays conforming; the reader MAY decline it, at the whole
file or at the narrowest scope whose declarations exceed what it can serve, and
MUST report the refusal as a resource limit and not as corruption. Software that
declines *on that ground* a file entirely within the table is not a conforming
reader. The last three rows are per-instance; the first five range over
declarations. I checked the individuation prose against the rows and it is
coherent — in particular that a layer addressing no tile has no tile whose
decoded size the table bounds, which matches `[R-COD-07]`'s quantifier.

**(7) Format major it does not implement.** Reject-file on capability grounds at
step 2, before any other gate but magic and CRC; the diagnostic SHOULD be
distinct from "not a TARN file" and from "corrupt". The file is neither
conforming nor nonconforming under this text, so a verifier reports *cannot
establish*. Nothing is served.

Two more I traced because they are the interesting ones for a reader that wants
to serve as much as it can:

**Sentinel entry.** Not a violation. Short-circuits payload I/O entirely: every
requested position of that tile reads as fill — each carried channel's, in
declared order, interleaved; exactly the entry's channel, planar. `[R-TYP-09]`
is the guard I implemented: fill is produced by *exactly one* condition, a
sentinel read from a verified chain. Never for a malformed entry, never for a
failed CRC.

**Partial failure inside one request.** §19.4 step 8: tile-scope failures are
bounded to the positions the failing entry carries, and the reader may return the
good entries' values with a per-entry report, or fail the request whole, but MUST
NOT stand fill in for the rejected positions. A layer-scope failure inside the
same request (step 3's index chain) bars the rest of the request and all further
service from the layer — prospectively, so values already returned stand.

---

## 8. Audits I ran that produced nothing

I record these because a negative result from a mechanical check is worth as much
as a finding.

**Register arithmetic.** I extracted every row of §21.2–§21.5 mechanically and
counted rows and instances by §21.1's stated rule (semicolon-separated; a cell
reading "—" is one instance). Result: F = 36 rows / 58 instances, L = 49 / 116,
T = 26 / 55, R = 10 / 48. Totals **121 conditions over 277 instances** — exactly
what §21.8 states. Every subsection's own count (36, 49, 26, 10) matches its row
count.

**Instance cells against the rules they restate.** I re-derived the members for
every cell where the rule gives an independent enumeration, and compared:

- L32 against `[R-GEO-01]`'s three floors (rank, tile extent, channel count) — 3. ✓
- L23 against `[R-CNT-18]`'s four payload groups — 4. ✓
- L2 (above) — 9, complete. ✓
- L1's eight u64 fields; A and A_slab are correctly absent, their out-of-domain
  values being caught by L39's "above 2^62" and L29's instances. ✓
- The value-set rows against §10.2's partition table, including the two places
  the document splits a reserved range into two bands (linearization 2–3 vs
  4–0x7FFF → L33 = 4; sample type 14–19 vs 20–0x7FFF → L34 = 4) and the one
  space with no experimental range at all (layout → L36 = 2). ✓
- The layout-formula axis: three formulas everywhere a decoded size is compared
  (T3, T14, T21, T22, L44), doubled where the comparison is a "differs from"
  (T3, T14, T22 → 6) and single where its own text bounds the direction (T21,
  L44 → 3). Consistent with §21.1's stated axes. ✓
- R4 against §18.2's carried-over frame constraints: magic, skippable frame,
  second frame, dictionary ID, content-checksum flag, trailing bytes,
  content-size in two directions = 8, × 2 containers = 16. The two constraints
  §18.2 says carry no witness (undisclosed dictionary use, the buffer-sizing bar)
  are correctly absent, and Window_Size is correctly absent because §18.2
  replaces it. ✓
- R5–R10 against `[R-MTA-04]`'s four restrictions. ✓

**Register completeness.** I worked down my own list of detectable malformations
— roughly forty — and found a row for each. I looked specifically for a
file-scope condition with no row (the trailer's file_id has no upper bound, and
correctly appears in no F2 instance; version_minor is descriptive and gates
nothing) and for a layer-scope condition with no row (a stale slab declaration
is expressly rowless because its detection *is* L41/L42's, and §16.2 says so).
I found no omission.

**§8.1's coverage claim.** "Every field of every structure is covered by exactly
one checksum" — I walked it: front block (equality), trailer (self), directory
(self), index entries (segment CRCs), segment CRC array (crc_of_crc_array, itself
under the directory CRC), stored tiles (entry crc), user-metadata extents (self),
and the one hole the map declares — the extent of an unassigned record type. The
claim holds.

**Analogy audit.** I put the governing verbs side by side for every "exactly as",
"the same way", "for the same reason", "on the same terms", "likewise" and "as it
does" in the document (18 sites). All sound. The two I expected to break did not:
§21.9's "*Decoded size of one tile* ranges over a layer's addressed tiles …
exactly as `[R-COD-07]`'s cap is" is a true match, and §18.2's "exactly as
`[R-COD-11]` requires of a codec it cannot execute" transposes correctly.

**Closed-list audit.** `[R-CNF-02]`'s "are the cases this text states" (two:
§6.3's flags = 0 against an ignore-lane bit, §6.2's over-long pre-trailer gap) —
I hunted for a third writer obligation whose violation the document *expressly*
declares not to be a file-conformance violation and found none; §10.3 and §18.3
belong to the sentence's first category (conduct, not output), and §20.5's four
trailer obligations and `[R-COD-06]`'s undisclosed dictionary belong to §21.7's
no-witness category, not this one. §23.1's operation list is expressly open
("the list of operations above is not offered as closed"). §2.3's
cannot-establish grounds are expressly open ("as when"). §21.7's two sets are
not presented as closed. `[R-CNF-11]`'s three verdicts are exhaustive by
construction.

**The one genuinely reachable degenerate file I could think of that the document
might not cover**: a layer whose only dimension has extent 0 under codec 4 with a
tile shape whose decoded size exceeds the lz4 cap. §17.2's Note answers it
directly and correctly — the cap is quantified over *addressed* tiles, the layer
addresses none, and codec 4 is conforming there. I verified the supporting claim
that the escape ends exactly when every dimension's extent is nonzero: the
addressed count is N or C·N with C ≥ 1 and N = ∏⌈E_i/T_i⌉, so it is positive iff
every E_i is. And I verified the Note's contrast — `[R-ENC-04]` carries no such
quantifier, so P·Q and P·B^c *are* checked in an empty layer, which is right
because P = ∏T_i with every T_i ≥ 1 exists regardless of the extents.

---

## 9. Findings

Three. None of them is byte-level, and I say so for each rather than reaching.

---

### reader-01 — CONTRADICTION — §13.3's sparse-writing Note states the index re-emission trigger more narrowly than `[R-WRT-04]` does

**Location.** §13.3, closing Note (the "Note — sparse writing" block); against
§20.3 step 4 `[R-WRT-04]`, and §5.1's second Example.

**Quotation** (§13.3):

> **Note — sparse writing.** A writer creates a sparse layer by
> emitting sentinel entries: no payload bytes, and for a full
> segment of sentinels even the segment CRC is a known constant
> (`[R-IDX-05]`). Declare-then-fill workflows append tiles as data
> arrives, generation by generation (§9); each commit that changes
> a layer's stored-tile set, or that grows its extents so that
> entry_count changes, re-emits that layer's whole tile-index region
> (§11.1, §20.3, `[R-WRT-04]`).

The rule it cites, §20.3 step 4 (`[R-WRT-04]`):

> Every layer whose stored-tile set or index content this commit changes has
> its tile-index region re-emitted in full

and §5.1's Example, in the same words:

> A commit that changes a layer's stored-tile set or index
> content re-emits that layer's whole tile-index region as well, at a
> new placement (§20.3, `[R-WRT-04]`).

**Detail.** The normative trigger has two disjuncts: *stored-tile set* and *index
content*. The Note replaces the second with a strictly narrower one — "grows its
extents so that entry_count changes" — and there are three commits the document
permits that satisfy the rule's second disjunct without satisfying the Note's:

1. **A supersede-only commit.** The same tiles remain stored; only their extents
   move. §20.4 settles that this is not a change to which tiles are stored — it
   reasons separately that "Superseding a stored tile's bytes re-places that
   layer's index region (§20.3, `[R-WRT-04]`), moving its extent slot (§7.4) and
   so modifying that layer's record", i.e. it reaches the re-emission obligation
   through *index content*, not through the stored-tile set. §20.3's own
   step 4 likewise distinguishes "tiles this commit stores or supersedes". A
   writer built from the Note appends the new payload, leaves the index alone,
   and silently strands the edit: the old payload is immutable and still
   addressed, so the file stays conforming and the caller's write is lost.

2. **A shrink that changes entry_count.** The Note says "grows". §20.3 step 4
   states the shrink case explicitly — "`[R-CNT-17]` obliges the smaller
   entry_count and so a re-emitted index region" — and a writer that follows the
   Note instead emits extent_length ≠ entry_count × 20 + ⌈entry_count/2^16⌉ × 4,
   which is L22, reject-layer.

3. **A commit that renumbers disk ordinals with entry_count unchanged.** §20.3
   step 4 permits an extent to grow and permits an extent to shrink, and nothing
   bars doing both to one layer in one commit (§11.1: "One shrink can do several
   of these at once"). Take a rank-2 layer with T = (1,1) and E = (2,3), so
   G = (2,3) and entry_count = 6; commit E = (3,2), so G = (3,2) and entry_count
   is still 6. extent_length is unchanged, entry_count is unchanged, and the set
   of stored tiles can be unchanged — but under `[R-GEO-06]`'s s = Σ t_i·∏_{j>i}G_j
   every surviving tile's disk ordinal moves (tile (1,0) goes from ordinal 3 to
   ordinal 2). §20.3 step 4 covers this in its parenthesis — "a geometry change
   renumbers ordinals wherever `[R-GEO-06]` moves them" — and the Note's
   condition never fires. A writer built from the Note leaves entries at ordinals
   that now denote different tiles, and §21.7 says that has no witness: the file
   is structurally conforming and every sample it returns is wrong.

I picked the normative reading — "stored-tile set or index content" — because
§21.1's principle for a divergence between a restatement and its rule ("the rule
governs") applies a fortiori to a Note, and because `[R-CNF-01]` puts Notes
outside normative text. The finding is the disagreement itself: this Note is the
only place in the document that states the trigger without "index content", and
it is the place a writer implementing sparse layers will read.

**Byte-level: no.** `[R-CNF-01]` puts the Note outside normative text and
`[R-WRT-04]` decides the question, so no conforming implementation may read the
Note as the rule. Two competent implementations that both read `[R-WRT-04]` agree
on every byte. What the defect costs is an implementer who builds from the
gloss: case 1 loses a caller's write silently, case 2 produces a reject-layer
file, case 3 produces a conforming file with a wrong reference array that §21.7
confirms nothing will catch.

---

### reader-02 — AMBIGUITY — "last zero grid count" in §11.1 has two readings, and the document's own house sense of *last* is the one under which the sentence is false

**Location.** §11.1, the Rationale block following `[R-GEO-02]`.

**Quotation:**

> Growth that changes entry_count changes extent_length with it (`[R-CNT-17]`), so the
> layer's whole tile-index region is re-emitted and disk ordinals
> renumber wherever `[R-GEO-06]` moves them (§20.3, `[R-WRT-04]`) —
> the growth that raises a zero-extent layer's **last** zero grid
> count included.

**Detail.** Two readings are defensible.

*Reading A — positional.* "last" indexes the declared dimension order: the zero
grid count belonging to the highest-indexed dimension that has one. Under this
reading the sentence is **false**. Raising that dimension's grid count while an
earlier dimension still has G_i = 0 leaves N = ∏G_i at 0, so entry_count does not
change, extent_length does not change, and no index region is re-emitted — the
case the *previous* sentence describes ("touches the directory alone"), not this
one.

*Reading B — the final remaining one.* "last" means the last zero grid count
still standing, so that raising it takes N from 0 to positive. Under this reading
the sentence is true: entry_count goes from 0 to a positive number, extent_length
goes from 0 to entry_count × 20 + ⌈entry_count/2^16⌉ × 4, and the layer emits an
index region for the first time.

I picked B, on context: the immediately preceding clause sets up the multi-zero
case ("a growth raising one grid count ⌈E_i / T_i⌉ (§11.2) while another stays 0
among them, the product holding at 0"), so "last" is being contrasted against
"one … while another stays 0". The bolding also signals that the word is
load-bearing.

But the census cuts the other way, which is why I am reporting it. Every other
occurrence of *last* in this document is positional — last in an ordering, not
last-remaining:

- §3.1 "The last two are separate namespaces"
- §5.1 "pre-trailer pad, and trailer last, in that order"
- §5.1 "the structures that must change on every commit are the last ones in the file"
- §9.4 / §9.6 "the last committed state" (which §9.6 defines positionally: "The nearest-to-end valid candidate")
- §11.2 "the last row of tiles is padded"
- §11.4 "**the last-declared dimension** varies fastest"
- §14.3 "the last value"
- §15.4 "the last covering 16,960 entries"
- §16.2 "a band along the **last-declared dimension**"
- §21.2 F29 "bytes remain after the last complete record"
- §21.9 "The last three rows are per-instance"
- Appendix G "the digest's **last eight bytes in output order**"

Two of those are the phrase *last-declared dimension*, applied to exactly the
object a grid count is indexed by. A fresh implementer who has read §11.4 and
§16.2 arrives at "last zero grid count" with the positional sense primed, and the
document supplies no other use of *last* to correct it. The fix an implementer
needs is one word — "the growth that raises a zero-extent layer's *final
remaining* zero grid count", or "the last of its zero grid counts to be raised".

**Byte-level: no.** The passage is inside a Rationale block, which `[R-CNF-01]`
places outside normative text, and the normative rule it glosses (§20.3 step 4)
keys re-emission on "stored-tile set or index content", not on this sentence. No
byte and no verdict turns on which reading is taken.

---

### reader-03 — OBSERVATION — §16.1's per-tile alignment invariant is stated over "every stored tile" without the transparency carve-out §16.2 spells out for slabs, and resolving it costs a three-rule chain

**Location.** §16.1 `[R-SLB-01]`; §21.3 row L40; against §3.1's definition of
*stored* and §15.3 `[R-IDX-03]`.

**Quotation** (§16.1):

> When declared:
> every stored tile's offset satisfies offset mod A = 0. … A verifier MUST check the invariant
> (violation: reject-layer, §15.3); readers are not obligated to —
> offsets are always explicit, so alignment is reader-invisible.

and L40:

> | L40 | Alignment A declared and a stored tile's index-entry offset is not a multiple of A | — | verifier | certification | `[R-SLB-01]` (R-IDX-03) |

**Detail.** §3.1 defines the term the invariant ranges over: "A tile is *stored in
a generation* if and only if that generation's tile-index entry for it is not the
sentinel". An entry that §15.3 classifies reject-tile on a *structural* ground —
say offset = 100, length = 0, in a layer declaring A = 4096 — is not the
sentinel, so its tile is *stored*, so the literal invariant tests its offset and
L40 fires at layer scope.

The document's other invariant over the same objects says the opposite for such
entries, and says it in its own text. §16.2 `[R-SLB-03]`:

> Sentinel tiles are transparent to run continuity: they
> occupy no bytes and do not break packing. So are the entries §15.3
> classifies reject-tile on a *structural* ground: they address no
> usable extent, and the run's stored tiles close over them.

§16.1 carries no parallel sentence. What actually settles it is one clause two
sections away, in `[R-IDX-03]`:

> Such an
> entry contributes no stored extent to the *verifier* rows, which bind
> over well-formed entries' extents only — `[R-SLB-03]`'s run
> continuity closes over it as it does over a sentinel — and none to
> `[R-LIF-08]`'s coverage walk

§15.3's *verifier* rows are three: the two overlap rows and "alignment or slab
invariant violated (§16)". So the exclusion reaches the alignment invariant as
well as the slab one — an entry with no usable extent contributes no stored tile
to L40, and the layer is not condemned for it. That is the reading I picked, and
I believe it is the right one: the parenthetical names `[R-SLB-03]` only as an
illustration, while "the *verifier* rows" is the operative quantifier.

What it costs to reach that reading is the observation. An implementer has to
(a) notice that §3.1 makes a structurally-malformed entry's tile *stored*,
(b) notice that §16.1's invariant therefore literally reaches it, (c) find
`[R-IDX-03]`'s "verifier rows" clause in §15.3 rather than in §16, and (d) work
out that §15.3's alignment/slab row is one of those three. The parallel
transparency sentence that §16.2 supplies for slabs would answer it in place, and
its absence from §16.1 is what makes the chain necessary. The stakes are not
nothing: the two readings differ by reject-tile against reject-layer for exactly
the same twenty bytes, which is the scope a conformance vector would have to
record under `[R-VEC-02]`.

**Byte-level: no.** L40's detector is *verifier*, so no reader obligation turns on
it; a conforming reader rejects that tile under §15.3's structural row on either
reading and serves the rest of the layer on either reading. A verifier reports
*nonconforming* on either reading — the entry is already a violation (T10). What
differs is only the scope the verifier records against, and `[R-IDX-03]` decides
that. No emittable byte sequence and no accept/reject verdict moves.

---

## 10. Confidence

**High** that an implementation built from this document alone would
interoperate. I built a file and read it back with no guesswork on the happy
path, every stated constant and worked example verified, the register's
arithmetic is internally exact (121 rows / 277 instances), and the seven
degradation walks each terminated in a defined outcome at a defined scope with a
defined detection point. The three findings above are all glosses and
cross-reference cost; none of them forks the bytes, and I looked hard for one
that does.

The places I would want a second pair of eyes: the compound-commit case in
reader-01 (I convinced myself the normative text covers it, but only by the
parenthesis in §20.3 step 4), and whether reader-03's chain is as expensive for
someone who reads §15 before §16 as it was for me, who read them in order.
