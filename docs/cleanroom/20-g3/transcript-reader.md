# Round 20 — Reader implementer, working transcript

## 0. Disclosure

I read exactly one file: `/Users/robertkleffner/Documents/GitHub/tarn/spec/tarn.md`,
in six `sed -n` passes covering lines 1–4369. I opened no other file in the
repository — no `docs/`, no `conformance/`, no `spec/registry.json`, no
`PLAN.md`, `AGENTS.md`, `README.md`. I ran no `git` command and did no web
access. I ran local Python that reads no project file: a CRC-32C implementation
I wrote from §4.5's parameters, a builder that synthesises a TARN file from the
document's rules, a reader that implements §19 from the document, and two
scripts that parse §21's register tables out of the spec text I had already
read (`grep`/`re` over that one file, which the brief permits).

**Context I did not ask for.** My runtime placed material in context before I
began: a project instruction file pointing at `AGENTS.md`, a memory index with
several one-line entries naming this project's cadence and prior findings, and
a task list. I did not open `AGENTS.md` or any memory file. One memory index
line contained what looked like a numeric fact about §21; I deliberately
re-derived that number mechanically from the register tables in the spec rather
than relying on it, and I say so at §7 below. Nothing else from that material
entered my reasoning, and no finding below originates in it.

## 1. Method

I wrote a reader in the order I would actually write the code: transport →
trailer → directory → record walk → layer table → layer validation → index
chain → entry classification → payload → codec → filter inverse → extract →
return. Every time the document did not tell me what to do I stopped and wrote
it down. I then built a file from scratch under the document's rules and ran
the reader over it, and mutated that file eleven ways to trace the degradation
walks end to end.

## 2. Constants and checksums I could check

I implemented CRC-32C from §4.5 alone (reflected, poly 0x82F63B78 reflected
form of 0x1EDC6F41, init 0xFFFFFFFF, final XOR 0xFFFFFFFF, stored LE) and
checked it against §4.5's own check vector before using it for anything:

```
CRC-32C("123456789") = 0xE3069283   (spec: 0xE3069283, bytes 83 92 06 E3)  OK
CRC-32C(zero bytes)  = 0x00000000   (spec: 0x00000000)                     OK
```

Then every stated constant and offset I could verify:

| Claim | Section | Result |
|---|---|---|
| Appendix A trailer CRC = 0xE00938D2 over trailer[0,60) | App. A | **matches** |
| Appendix A field decode (gen 1, dir 16/4, F=128, file_id 0x0123456789ABCDEF) | App. A | **matches every annotation row** |
| Empty directory = 4 bytes holding CRC of zero bytes = 0x00000000 | §5.1, §7.1 | **matches** |
| §7.4 example: CRC over 4 sentinel entries (80 bytes) = 0x80A34955, stored `55 49 A3 80` | §7.4 | **matches** |
| §7.4 example: crc_of_crc_array = 0xC4EE982E | §7.4 | **matches** |
| §7.4 example: inline payload is 81 bytes, every listed offset | §7.4 | **matches at every one of the 13 annotated offsets** |
| §7.4 example: 4 + 34 + 18 + 12 + 13 = 81 | §7.4 | **matches** (name 4; nine scalars 1+2+2+2+8+8+8+1+2 = 34; dim 18; chan 12; trailing 13) |
| §7.4 example: extent_length 4·20 + ⌈4/2¹⁶⌉·4 = 84 | §7.4 | **matches** |
| CRC of a full all-sentinel segment (2¹⁶ entries) = 0xEECB3BB2 | §15.4, App. B | **matches** |
| §15.4 example: 16 segments, 15 full + 16,960; array 64 B; region 20,000,064 B; k=999,999 at segment-relative byte 339,180; array at [20,000,000, 20,000,064); segment 15 at [19,660,800, 20,000,000); full segment 1.25 MiB | §15.4 | **all match** |
| §15.4 example: planar C=4 N=32, channel 2 at s=10 → disk ordinal 74, entry [1,480, 1,500); channel 3 = entries 96–127 | §15.4 | **all match** |
| §11.2/§11.4 example: G=(4,8), N=32, P=65,536; (300,700) → tile (1,2), s=10, u=(44,188), in-tile ordinal 11,452; planar c=2 → 74 | §11.2, §11.4 | **all match** |
| §14.2 example: Q=3, size 18, ordinal 5 at [15,18); planar b = 12 B, ordinal 5 at 10–11; float32+bool Q=5, size 30, [25,30) | §14.2 | **all match** |
| §14.3 example: alternating planar bool P=10 → `55 01` (fill false), `55 FD` (fill true) | §14.3 | **matches** |
| §14.5 example: (5,5)/(4,4) → grid 2×2, edge tile 1 real + 15 padding, 32 B, values 1–15 = `CD AB` | §14.5 | **matches** |
| §17.3 example: shuffle of 1.0/2.0/3.0 float32 → `00 00 00 00 00 00 80 00 40 3F 40 40` | §17.3 | **matches** (I computed it from the i·n+j rule, not by copying) |
| §20.3 example: 32·20 + 4 = 644 | §20.3 | **matches** |
| §21.9 note: 2³² entries → 256 KiB CRC array; 2³⁶ → 4 MiB | §21.9 | **matches** |
| §4.6 example: `température` NFC 12 B / NFD 13 B, with the stated hex | §4.6 | **matches** |
| §12.3 example: `temp` float32 entry = 12 bytes as listed | §12.3 | **matches** |
| bfloat16 1.0 = 0x3F80 = high half of binary32 0x3F800000 | §12.1 | **matches** |
| §5.1: 128-byte floor derivable (16 + ≥4 ⇒ F−64 ≥ 20 ⇒ F ≥ 84, F ≡ 0 mod 64 ⇒ F ≥ 128) | §5.1 | **derivation checks** |

I found **no wrong constant, offset or checksum** in the document. Every
arithmetic claim I could reduce to numbers reproduced exactly.

## 3. The open path, byte-exact

Steps as I coded them, with what bounds each range *before* I have read it.

**Request 1 — the trailer.** A suffix range for the final 64 bytes. Nothing in
the file bounds it; it is a suffix, and per `[R-CNT-10]` the response's own
complete-length figure is the transport-authoritative F. §19.1's steps 1 and 2
therefore cost one request between them (§6.4). If the transport answers 200
rather than 206, `[R-CNT-10]` obliges me to abort or accept the full body
deliberately, never to take the body prefix as the range.

Validation in §6.2's stated order — and the order matters, because only the
first three touch fields whose positions §6.3 fixes across every format major:

1. trailer magic `8A 4E 52 41 54 0D 0A 1A` at F−64 (F8; F1's trailer-magic
   instance for the byte-reversed case)
2. CRC-32C over trailer[0,60) against the u32 at [60,64) (F14)
3. version gate: `version_major == 0` → F18; `!= 1` → capability refusal,
   diagnostic distinct from "not a TARN file" and from "corrupt" (§6.3's SHOULD)

then, those passed, all of: incompat lane (bits 0–15) any set → F19; ignore
lane (16–31) ignored entirely; `committed_file_length == F` (F17) and
`F mod 64 == 0` (F13); `dir_offset ≥ 16` (F9); `dir_length ≥ 4` (F16);
`dir_offset + dir_length ≤ F − 64` (F10); `1 ≤ generation ≤ 2⁶³−1` (F11/F2);
`file_id != 0` (F12); reserved [56,60) zero (F15); plus `[R-ENC-03]`'s domain
on dir_offset/dir_length/committed_file_length (F2) and `[R-ENC-04]` on their
sum (F3), and `[R-CNT-27]`'s 128-byte floor (F5).

I noticed and checked one thing here: **`file_id` is deliberately not subject
to the 2⁶³−1 domain.** `[R-ENC-03]` binds "every offset, length, extent, and
count"; F2's instance list omits `file_id`; §21.9's hard-limit paragraph omits
it. That is load-bearing for Appendix G item 2, which derives `file_id` from
the last eight bytes of a digest — a value that will exceed 2⁶³−1 half the
time. Consistent.

**Request 2 — the directory.** `[dir_offset, dir_offset + dir_length)`, bounded
before I fetch by dir_offset ≥ 16 and dir_offset + dir_length ≤ F − 64, both
read from a CRC-verified trailer, so `[R-ENC-05]`'s "no I/O on an unverified
integer" holds. dir_length ≥ 4 guarantees the terminal CRC exists. §21.9
guarantees me at least 16 MiB here; above that I may decline as a resource
limit, reported as a limit and never as corruption (`[R-ERR-04]`).

Verify CRC-32C over dir[0, dir_length−4) against dir[dir_length−4, dir_length)
before any other use (F20), then walk the record sequence, which is exactly
dir[0, dir_length−4).

**Cold remote open cost.** Two requests, **64 + dir_length bytes**. For
Appendix A's minimal file that is 64 + 4 = **68 bytes in 2 requests**, and the
front block is never fetched, so `[R-CNT-04]` lets me omit its equality check —
which Appendix A's own prose confirms. For the file I built below,
**192 bytes in 2 requests**. The alternative is one speculative suffix window
(§6.4's containment test); writers are advised to keep dir_length + pad + 64
inside 65,536 so a 64 KiB window suffices.

**Record walk.** 24-byte header, then inline_length bytes. Type 0 → F24. Header
or payload past the sequence end, or residue → F29. Unknown type: MU=1 →
reject-file, MU=0 → ignore (see finding reader-01 for where that obligation
comes from). Multiplicity: a second top-level user-metadata record → F34.
Extent slots of non-layer top-level records → F30/F31/F32. Top-level
user-metadata framing: slot ≠ (0,0) (F21), extent_length ≥ 5 (F22),
inline_length == 1 (F23), encoding byte in {1,2} else ignore-record (R1) or, at
≥ 0x80, ignore-record and no violation (§21.6). Layer records contribute only
their **name** at this tier.

The layer-name namespace rule is unusually well drafted and I want to record
that I tested it, because it is the kind of thing that forks readers: §19.1
step 4 decides uniqueness **first**, over raw bytes, before any name is
validated, so two layers with byte-identical *ill-formed* names are F4
(reject-file), not two independent reject-layers; and a layer record whose name
field does not fit inside its own inline_length "contributes no name to the
namespace", so it can never be half of a duplicate. F4's Instances cell carries
the same qualifier ("both obtainable within their records' inline_length").
Determined, and I implemented it exactly.

I also confirmed mechanically that **every reader-detected file-scope row is
Detected = open** (29 of 29), so a reader never discovers a file-scope violation
after it has begun serving data — there is no retroactivity problem at file
scope. The only reader-detected layer-scope rows at *tile use* are L37 and L38,
the two index-chain CRCs, and §19.4 step 8 makes that bar explicitly
prospective.

## 4. Validation timing by tier

- **At open** — front block *if resident* (`[R-CNT-04]`; a reader that would
  have to issue a further range for [0,16) MAY omit it, a verifier may not);
  trailer; directory region and record walk; layer-name namespace; the
  top-level user-metadata framing rules and R1's encoding value.
- **At first access to a layer** — the whole of §19.3, and it performs **no
  I/O**: I verified this in code, the request counter did not move across
  `access()`.
- **At use of a tile** — index chain (L37, L38), entry classification (T6–T12),
  payload CRC (T1), decode (T3, T14–T25).
- **At use of a record's extent** — that extent's CRC (R2) and the document
  content rules §18.2 attaches at its encoding (R3–R10).
- **Never obliged** — everything whose Detector is *verifier*: F7, F25–F28,
  F33, F36; L18, L25, L40–L42, L46–L49; T2, T4, T5, T26. A reader that detects
  one MAY reject under `[R-CNF-12]`, and for `[R-CNT-22]` and `[R-MTA-05]` the
  governing rule positively obliges it to serve the structure unchanged.
- **What becomes a verdict when** — a reader's verdict is per-scope and
  immediate. A verifier's is *nonconforming* the moment it establishes any
  violation; *cannot establish* only for a traversal that established none, on
  a capability or resource ground (foreign major, unimplemented MU=1 type,
  un-executable codec/filter, declined decode); and each unchecked requirement
  and unexamined scope is reported beside the verdict without changing it.

§19's preamble is what makes these tier lists safe to implement from: "Those
enumerations are not the complete inventory of what a reader detects at that
tier: §21's register is". Without that sentence R1's detection at open would be
unreachable from §19.1's step 4, which does not mention the encoding byte's
value set. I checked that no row's *Detected* cell disagrees with its rule's
own tier statement where the rule makes one.

## 5. The worked example I built

I built a file from the document alone, then read it back with the reader.

Layer `sst`: rank 2, dims `y` (E=2, T=2) and `x` (E=3, T=3), interleaved,
channels `a` (uint8, fill 0x00) and `b` (uint16, fill 0xFFFF), linearization 1,
codec 1 (none), filter 2 (byte-shuffle), no alignment, no slab.

Derived, per §11.2/§14.2: G = (1,1); N = 1; P = 6; Q = 1 + 2 = 3; F = (0, 1);
decoded size P·Q = 18; addressed-tile count = N = 1; entry_count = 1;
nseg = ⌈1/2¹⁶⌉ = 1; index region length = 1·20 + 1·4 = 24. Grid·T = (2,3) = E,
so **no padding positions** — I deliberately took that case first, then checked
§14.5's own example separately for the padded one.

Decoded tile image (sample-major, a then b, LE):
```
0a e8 03  0b e9 03  0c ea 03  0d eb 03  0e ec 03  0f ed 03
```
Byte-shuffle at s = Q = 3, n = L/s = 6, byte i of group j to offset i·n + j:
```
0a 0b 0c 0d 0e 0f  e8 e9 ea eb ec ed  03 03 03 03 03 03
```
Codec 1, so those 18 bytes are the stored bytes, and `[R-COD-04]`'s equality
(length == decoded size) holds — checkable before any payload fetch, which is
what my reader does.

Placement: front [0,16); tile [16,34); index region [34,58) (entry array
[34,54), segment CRC array [54,58)); directory [58,186); pre-trailer pad
[186,192) = 6 bytes of slack, exactly `[R-LIF-02]` step 5's pad to the next
64-boundary; trailer [192,256). F = 256, a multiple of 64. The directory is the
last structure, as `[R-CNT-05]` requires.

Values: tile crc 0x69BF86A0; segment CRC 0x27973047; crc_of_crc_array
0x213B027C; layer-record inline_length 100; dir_length 128; trailer CRC
0xB226FC93.

Reader output:

```
OPEN: F=256 gen=1 dir=[58,186) file_id=0x123456789abcdef
  requests: [suffix 64, (58,186)]  bytes: 192
  layers: ['sst']
LAYER ACCESS: no I/O -> True
  d=2 C=2 G=[1,1] N=1 P=6 Q=3 addressed=1 dsizes=[18]
  read (0,0)  a=0a  b=e803      (ordinal 0  -> a=10,   b=1000)
  read (1,2)  a=0f  b=ed03      (ordinal 5  -> a=15,   b=1005)
  read (0,2)  a=0c  b=ea03      (ordinal 2  -> a=12,   b=1002)
  read (2,0)  -> request-failed: coordinate outside extents
TILE READ I/O (uncached): 3 requests, 42 bytes
  ranges: (54,58) CRC array | (34,54) segment 0 | (16,34) payload
```

**Cold tile cost**, then: the layer's whole segment-CRC array
(⌈EC/2¹⁶⌉·4 bytes), the one segment covering the entry
(min(2¹⁶, EC − s·2¹⁶)·20 bytes, never more than 1.25 MiB), and the tile's own
extent. Here 4 + 20 + 18 = **42 bytes in 3 requests**, the first two of which
`[R-IDX-04]` lets me issue in parallel, both bounded from the layer record
alone. §15.4's note lets me cache each verified range under committed-prefix
immutability, so the repeated reads above cost nothing after the first.

Reverse ordinal check by hand for (1,2): t = (1 div 2, 2 div 3) = (0,0) → s = 0;
u = (1 mod 2, 2 mod 3) = (1,2) → in-tile ordinal 1·3 + 2 = 5; interleaved, so
value k = 5·C + c; byte offset u·Q + F_c = 5·3 + 0 = 15 for `a`, 16–17 for `b`.
The decoded image's bytes 15..17 are `0f ed 03` — a = 15, b = 0x03ed = 1005.
Matches what the reader returned.

## 6. Degradation walks

Eleven mutations, run through the reader:

| Mutation | Outcome | Still served |
|---|---|---|
| `version_major = 2` | capability refusal at open, distinct diagnostic (§6.3) | nothing; file conforming under major 2, not judged here |
| incompat-lane bit 3 set | reject-file, F19, at open | nothing |
| ignore-lane bit 20 set | **ignored**; file conforming (§21.6) | everything |
| `version_minor = 9` | **accepted**; minors never gate (`[R-CNT-07]`) | everything |
| tile payload byte flipped | reject-**tile**, T1, at tile use | every other tile, every other layer, the file |
| index entry byte flipped | reject-**layer**, L38 (segment CRC), at tile use — *prospective*, so values already returned stand | every other layer; nothing further from this one |
| reserved codec / reserved layout value | reject-**layer** at layer access (my mutation offsets landed on the alignment field, so the run shows L39; the blast radius is the point and it is right) | every other layer |
| physical file truncated by 8 bytes | reject-file at open — the last 64 bytes are not a trailer, magic fails (F8); `[R-LIF-05]` forbids me to scan backward | nothing |
| 8 residue bytes appended | identical: F8. §9.5's note is exactly right that a reader cannot tell residue from corruption and is not asked to | nothing |
| unknown top-level type 0x9000, MU = 1 | reject-file | nothing |
| unknown top-level type 0x9000, MU = 0 | **ignore-record**, SHOULD-report emitted | everything |

Three more I traced on paper rather than in code because they need a codec I
did not implement:

- **Unknown codec value** (reserved 5–0x7FFF or experimental ≥ 0x8000):
  reject-layer at layer access, L43. Crucially this is *not* "cannot execute a
  codec" — §17.4 is explicit that for a conforming reader that position arises
  only at a reserved or experimental value, since all four assigned codecs are
  core; software that cannot run an assigned codec is simply not a conforming
  reader. A verifier that cannot run one reports *cannot establish*.
- **Limit exceeded**: `[R-ERR-04]` lets me decline at the whole file, or at the
  narrowest scope whose *declarations* exceed what I can serve — a layer or a
  tile — and obliges me to report it as a resource limit, never as a validity
  error. A user-metadata document has no declared size, so §18.2's note pins
  its decline to the whole file.
- **User-metadata extent CRC failure**: ignore-record (R2) whatever the
  containing scope, under `[R-CNT-25]`'s quarantine, with a SHOULD-report. The
  structural data it annotates is untouched. But a malformed *slot* on such a
  record precedes the quarantine and is reject-file / reject-layer (F21, F22,
  L10, L11) — a distinction I had to read three times and which §18.1 states
  plainly.

## 7. Register audit

I extracted §21.2–§21.5's tables mechanically and counted, because §21.1 makes
the register's completeness normative and §21.8 states a figure:

```
rows: 121   instances: 273
F: 36 rows / 58 instances      (§21.2 states 36 conditions)
L: 49 rows / 116 instances     (§21.3 states 49)
T: 26 rows / 55 instances      (§21.4 states 26)
R: 10 rows / 44 instances      (§21.5 states 10)
```

121 rows over 273 instances, matching §21.8's "121 conditions over 273
instances" and every per-subsection count. I counted a cell reading `—` as one
instance and otherwise split on semicolons, which is §21.1's own stated
mechanical rule ("the count is therefore mechanical once the cell is written").

Spot-checks of outcome and detector against the governing rules found no
divergence. §15.3's preamble says "Six rows are marked *structural*"; I counted
six. L2's dominance claims check out: C·N > (C−1)·N + (N−1) = CN − 1, and
P·Q ≥ P·C because Q = ΣBᵢ with every Bᵢ ≥ 1. §10.2's eight numeric spaces are
each partitioned identically in their defining sections, and §10.3's
enumeration of where each lands covers all eight.

## 8. Findings

### reader-01 — OBSERVATION — §2.3's acceptance-duty carve-out for an unimplemented MU = 1 record is unqualified as to scope, where §21.6 and §7.4 confine whole-file refusal to top-level records

> "A reader MUST accept every conforming file of a format major version it
> implements, carrying no record of a type it does not implement with
> MUST_UNDERSTAND = 1 — in a conforming file such a type is necessarily from
> the experimental range, since a reserved-range type carrying MU = 1 is itself
> a violation — and none of whose values exceeds the minimum guarantees of
> §21's limits table (§21.9's `[R-ERR-04]` governs a refusal on that last
> ground; §21.6's closing paragraph names the other two)" — §2.3, `[R-CNF-03]`

against

> "The qualifier is load-bearing — the same type as a layer sub-record is
> reject-layer and never a ground to refuse the file (`[R-CNT-18]`), so only
> the top-level case is a file a reader refuses" — §21.6, closing paragraph

and

> "an unknown sub-record type with MU = 1 is reject-layer, and where the file
> is otherwise conforming a reader MUST NOT reject the file for it" — §7.4,
> `[R-CNT-18]`

Take a conforming file: layer A is clean, layer B carries an experimental-range
sub-record (type ≥ 0x8000) with MU = 1, PE = 1. §2.3's acceptance duty runs
only to conforming files "carrying no record of a type it does not implement
with MUST_UNDERSTAND = 1", and this file carries one — at layer scope, but §2.3
does not say top-level. So the acceptance duty, read on its own, does not reach
this file, and an implementer building the conforming-reader checklist from
§2.3 concludes it may refuse the whole thing.

That conclusion is wrong, and the document does decide it, but only through a
move that is easy to miss: **§2.3 withholds an obligation to accept; it does
not grant a permission to reject.** The only general permission to reject is
`[R-CNF-12]`, and that runs to *nonconforming* files. This file is conforming.
And `[R-CNT-18]` supplies an all-caps MUST NOT against refusing it. So the
reader must serve layer A, and the reader that refuses the file is
nonconforming.

Three readings are on the table and I want to name them: (i) §2.3's carve-out
is literal and scope-blind, so refusal is permitted — defeated by the absence
of any permission and by `[R-CNT-18]`'s MUST NOT; (ii) §2.3's carve-out should
be read as carrying §21.6's top-level qualifier, which its own parenthetical
pointer ("§21.6's closing paragraph names the other two") invites — this is the
reading I took; (iii) §2.3's carve-out is literal *and* `[R-CNT-18]` narrows it
back, which reaches the same behaviour by a longer route. (ii) and (iii) agree
on every byte. I implemented (ii): my reader rejects the file only for a
*top-level* unimplemented MU = 1 record, and rejects the layer for a
sub-record one.

What an implementer does wrong without this: builds the acceptance predicate
from §2.3's checklist — which Appendix H reproduces as the conforming-reader
summary — and refuses conforming files over a sub-record it does not
understand, discarding every other layer in them. The fix that would close it
is a scope qualifier on §2.3's clause, not a new rule.

**Byte-level: no.** The verdict on the byte sequence is settled — `[R-CNT-18]`'s
"a reader MUST NOT reject the file for it" is an all-caps prohibition and §2.3
supplies no counter-permission, so a reader that refuses the file is
nonconforming under a rule that names the actor and the outcome. Nothing here
changes the emittable set either: the file's conformance is decided by
`[R-CNF-02]` and is not in dispute. The cost is entirely to the implementer who
reads §2.3 or Appendix H without following the pointer.

### reader-02 — AMBIGUITY — §19.4 never defines channel selection as part of a request, and `[R-TYP-08]`'s MUST then over-delivers on an interleaved sentinel tile

> "A **point request** names a single coordinate (§3.1); a **region request**
> names a rectangular range of coordinates, one interval per dimension, and a
> range whose every interval holds a single position is a region request." —
> §19.4, `[R-RDR-04]`

> "A valid sentinel short-circuits steps 5 and 6 for that entry: every
> requested sample position of its tile reads as fill — the entry's channel's
> recorded fill in a planar layer; each carried channel's, in declared order,
> in an interleaved layer — bit-exactly and with no payload I/O" — §19.4 step 4

> "a reader that returns any of the tile's sample positions inside the layer's
> extents MUST return, for each channel the tile carries, that channel's fill
> value at every such position" — §13.3, `[R-TYP-08]`

The request vocabulary is defined over **coordinates only**. Channels never
enter it. Yet step 2 says "the disk ordinal of each needed tile — s
interleaved; c · N + s **per requested channel** c planar", step 7 says "Locate
each **requested value**", step 8 speaks of "a planar layer's several
channels", and the closing note says "Channel-subset reads verify only the
segments they touch". So channel selection is used four times in the algorithm
and defined nowhere in the request grammar, and every mention of it is on the
planar side.

For a **planar** layer this is harmless: a channel subset is a subset of
entries, and step 4's "the entry's channel's recorded fill" is per entry.

For an **interleaved** layer it is not. One tile carries every channel, so
"requested channel" cannot mean "which entry"; it can only mean "which values
to hand back". Three readings:

(a) **Interleaved layers admit no channel subsetting.** Every read returns the
full sample. Then §19.4 step 4 and `[R-TYP-08]` are exactly right as written,
and the algorithm is consistent — but §14.2's closing sentence ("channel c's
value at in-tile ordinal u sits at byte u · Q + Fᶜ") exists to support an
operation the document then never sanctions, and every real implementation will
offer it.

(b) **Subsetting is allowed and `[R-TYP-08]` is literal**, so a one-channel
request against a stored interleaved tile returns one value (step 7: "each
requested value") while the same request against a *sentinel* tile returns all
C fill values, because the MUST is quantified over "each channel the tile
carries". That is an incoherent API — the sparse path returns strictly more
than the dense path — but it is what the words say.

(c) **Subsetting is allowed and `[R-TYP-08]` fixes which channels *read as*
fill, not what the reader hands back**, so the caller's request bounds the
return in both the stored and the sentinel case.

I picked **(c)**, on `[R-MDL-02]`: "a conforming reader that reads any portion
of a layer MUST return exactly the corresponding portion of the reference
array". A channel-subset read is a portion; the corresponding portion is those
channels' values; and reading (b) returns more than the corresponding portion.
`[R-TYP-08]`'s "for each channel the tile carries" then reads as the
interleaved/planar contrast §3.2 draws — one tile's channels are stored or fill
*together* in interleaved, independently in planar — rather than as an
enumeration of the return value.

What an implementer does wrong without this: writes (b) and ships a reader
whose sparse and dense paths disagree about arity, or writes (a) and is unable
to serve a single-channel query on an interleaved layer without dragging the
whole sample through its API. Two implementations of (b) and (c) handed the
same conforming file and the same one-channel query return different numbers of
values.

**Byte-level: no.** The divergence is in what a reader returns to its caller
from a *conforming* file, not in which byte sequences may be emitted and not in
any accept/reject verdict — both readings accept the file and neither rejects
any scope. It does not reach the corpus either: `[R-VEC-02]` records "the
decoded content a reader is to return from every scope it can read", which is
the full content of the scope, not a per-request projection, so no vector
distinguishes (b) from (c).

### reader-03 — OBSERVATION — `[R-SER-08]` fixes the *value* a reader reports for a nonconforming interleaved boolean byte but not the *byte*, while §19.4 calls it the thing that "fixes what a reader returns"

> "A reader that neither detects the violation nor rejects the tile, and
> returns the value, MUST report 0x00 as false and every other byte as true."
> — §14.2, `[R-SER-08]`

> "**Return.** Return the requested values' bit patterns unaltered
> (`[R-MDL-02]`, `[R-TYP-04]`) — for every byte a conforming file can carry,
> the whole of this step (`[R-SER-08]` fixes what a reader returns for the one
> byte a conforming file cannot)." — §19.4 step 8

§19.4 step 8 says samples are returned as **bit patterns**, and names
`[R-SER-08]` as what fixes the return for the one byte a conforming file cannot
carry. `[R-SER-08]` fixes a *truth value*, not a bit pattern. Handed the stored
byte 0x37 in an interleaved bool channel, a reader that declines to reject the
tile must "report it as true" — and two implementations can do that two ways:
hand back 0x37 (a bit pattern, per step 8's framing, which the caller then
interprets), or hand back 0x01 (the sole encoding of true).

I resolved it to **0x01**, and the resolution is available but takes three
hops. First, `[R-TYP-06]`: an unstored bool channel returns its recorded fill
*byte*, which `[R-TYP-07]` constrains to 0x00 or 0x01 — so the returned
representation of a bool sample in this format is a byte in {0x00, 0x01}.
Second, `[R-MDL-02]`: the same reference array must come back from an
interleaved and a planar encoding of the same logical content, and in a packed
plane (§14.3) the only thing recoverable is a bit — so the returned
representation cannot be layout-dependent, and cannot be an arbitrary byte.
Third, §13.2's Rationale explicitly refuses the "any nonzero byte is true"
convention that passing 0x37 through would require of the caller — though that
is a Rationale and §2.1 makes it non-normative, so it corroborates rather than
decides.

What an implementer does wrong without this: passes the stored byte through and
believes it has complied with both step 8 ("bit patterns unaltered") and
`[R-SER-08]` ("report as true"), producing a reader whose bool channel can hand
a caller 254 distinct values. §14.2's own Rationale says the point of the rule
is that "two readers handed the same malformed tile could disagree about a
sample and both be conforming, which is the divergence this document exists to
prevent" — and at the level of the returned byte, that is still the state the
text leaves.

**Byte-level: no.** It arises only in a nonconforming file, it does not touch
the emittable set (`[R-SER-08]`'s writer-side prohibition is unambiguous:
0x00 or 0x01 and nothing else), and it does not change any accept/reject
verdict — T2's detector is the verifier and the reader is expressly under no
obligation to screen the content. It reaches the corpus only through
`[R-VEC-02]`'s "decoded content a reader is to return", where a T2 vector's
manifest entry would have to write down one of the two.

## 9. Things I checked and did *not* find defective

Recording these so the next round does not re-walk them.

- **The chain of trust is airtight for `[R-ENC-05]`.** Every fetch my reader
  issues is bounded by an integer already covered by a verified checksum: the
  trailer suffix by nothing (a suffix), the directory by the CRC-verified
  trailer, the index region and its segments by the directory-CRC-verified
  layer record, and each payload by the segment-CRC-verified entry. I could not
  construct a path that allocates or seeks on an unverified value.
- **§6.2's ordered validation and §6.3's cross-major invariants agree.** The
  three checks §6.2 puts before the version gate (magic, CRC) plus
  `[R-CNT-04]`'s front block are exactly the four rows §21.2's preamble says
  reach a foreign-major file, and §6.3's permanent layout (magic at F−64,
  versions at F−56, CRC at F−4 over [F−64, F−4)) is what makes them safe there.
- **`[R-CNT-15]`'s keyword-less arrow** ("An unknown record type at file scope:
  MU = 1 → reject-file; MU = 0 → ignore-record") worried me under §2.1's
  all-caps rule, since the experimental-range MU = 1 case is expressly *not* a
  register row and so cannot borrow `[R-CNF-04]`'s MUST. It is backed: §2.4's
  outcome table defines reject-file as "A reader MUST NOT rely on any structure
  in it", and §2.4 states that the same vocabulary governs defined conditions
  that are not violations. Two hops, but sound.
- **The "otherwise conforming" clause in `[R-CNT-18]`** is self-resolving. Read
  as "conforming apart from this very condition", it would collide inside one
  sentence with its own second half ("on a nonconforming file `[R-CNF-12]`'s
  licence ... is untouched") for a reserved-range MU = 1 sub-record (L24). Only
  the reading "the file is conforming" makes the sentence consistent, which is
  the experimental-range case, which is what §21.6 independently says.
- **§16's slab and alignment invariants** are stated declaratively without
  keywords but carry force through "A verifier MUST check the invariant
  (violation: reject-layer)" plus `[R-WRT-02]`'s binding on creators; L40–L42
  register them. Run continuity closes correctly over sentinels and over
  structurally-rejected entries but not over an entry whose only defect is its
  payload CRC — I checked that §15.3, §16.2 and L41 all say the same thing.
- **zstd's window rule composes with RFC 8878.** For a tile below 1 KiB decoded
  the Window_Descriptor cannot express a small enough window, so only a
  single-segment frame is encodable — §17.2's note says exactly this, and both
  of §14.2's worked decoded sizes (18 and 30) and §14.3's (2) fall there.
- **`[R-COD-10]`'s divisibility claim** ("L is divisible by s in every case")
  holds in all three cases: planar numeric L = P·Bᶜ with s = Bᶜ; interleaved
  L = P·Q with s = Q; packed bool s = 1.
- **Coverage classes are complete.** A layer's tile-index region is a *record*
  extent (the layer record's), so it enters §9.7's walk once and is not a
  second claimant — which is the only way §5.2's partition closes. Prior
  generations' trailers, directories and pads are slack.
- **Three near-synonyms for scope** — "owning" (defined in §2.4), "governing"
  (defined inside `[R-CNT-13]`: "the layer for a layer record and for
  sub-records, the file for other top-level records"), and "containing" (§7.1,
  §18.1) — coincide in every case I could construct, and the register's F/L
  row split confirms each one. §7.3's Scope cell for the layer record reads
  "file (container for layer scope)", and the parenthetical is what keeps it
  from contradicting `[R-CNT-13]`.
- **§15.1 does not state the index-encoding value set** although §10.3 and
  §19.3 both cite "§15.1" for it; the set is stated unambiguously in §7.4's
  table and in §10.2's, and §15.1 points back to §7.4. A loose pointer, not a
  gap, and no implementer can be led to a wrong value by it. Not raised as a
  finding.

## 10. Confidence

I would ship a reader from this document. Every byte I needed to fetch, every
check I needed to run, every outcome and its blast radius, and every constant I
could compute were determined. The three items above are where I had to choose,
and none of them changes a byte on disk or an accept/reject verdict.
