# Round 28 — Writer implementer walk

## 0. Disclosure

I read exactly one file: `/Users/robertkleffner/Documents/GitHub/tarn-first-draft/spec/tarn.md`,
which was where the brief said it would be (4,648 lines; the brief said 4,649 — off by one,
consistent with counting a trailing newline, and not worth more than this sentence).

I ran `grep`/`rg`/`sed`/`wc` against that file only, and Python that reads no files
(a CRC-32C implementation and a register-table parser fed from that one file).

I read no ADRs, no `docs/`, no `PLAN.md`, no `AGENTS.md`, no `conformance/`, no
`spec/registry.json`, no git history. I listed no directories. I did not read the output
directory. I ran no web search or fetch.

**Context I did not ask for.** Before I began, my runtime placed in my context: a
`claudeMd` block quoting `/Users/robertkleffner/Documents/GitHub/tarn-first-draft/CLAUDE.md`
(a one-line pointer to `AGENTS.md`), a `gitStatus` block naming the current branch and the
subject lines of five recent commits, the user's email, and today's date. The commit
subjects name prior-round artifacts and one prior-round outcome. **I disregarded all of it**
and did not follow any of the leads in those subject lines; I record its appearance here
because the brief requires it, not its contents. Nothing in my findings below came from it.
I also had a large set of tool and skill descriptions in context, none of which bears on TARN.

---

## 1. What I set out to do

Implement, on paper and concretely, a conforming **writer and updater**: a byte-layout walk
in emission order, an append procedure, the record-flag matrix, slack accounting per commit
shape, torn-write recovery at four-plus crash points, and a byte-divergence catalogue checked
against Appendix G item by item.

I read the whole document once end to end before writing a byte, because the brief's warning
that the survivor is often in untouched text has been true four rounds out of the last ten.

---

## 2. Reading the trailer change

The brief said a structural field was removed from a fixed-size structure, that the following
fields moved, that the structure's size did not change, that the freed bytes were not
reclaimed, and that a quantity the removed field supplied is now carried by a different
field on a newly stated property of that field.

From the text alone I can see what that was without being told. §6.2's trailer is:

| off | size | field |
|---|---|---|
| 0 | 8 | trailer magic |
| 8 | 2 | version_major |
| 10 | 2 | version_minor |
| 12 | 4 | flags |
| 16 | 8 | dir_offset |
| 24 | 8 | dir_length |
| 32 | 8 | committed_file_length |
| 40 | 8 | file_id |
| 48 | 12 | reserved (zero) |
| 60 | 4 | trailer CRC |

Offsets chain exactly: 0+8=8, +2=10, +2=12, +4=16, +8=24, +8=32, +8=40, +8=48, +12=60,
+4=64. No gap, no overlap, 64 total. §6.3 says "The format-major-1 trailer has zero slack:
every byte is assigned" — true of this table.

The reserved field is now **12** bytes where a 4-byte reserved field is what the other fields
would leave; that is the "bytes the removal freed were not reclaimed" the brief describes.
The removed field was a generation counter, and the quantity it supplied is now carried by
`committed_file_length` under the newly stated property that it **strictly increases per
commit within one file_id, by at least 128** (§3.1, [R-LIF-02], [R-LIF-03]).

This is the single highest-value place to look for stale offsets and widths, so I swept it
first.

### 2.1 Offset/width sweep over the trailer

`grep -n "trailer offset\|offset 48\|offset 40\|offset 32\|F − 56\|F - 56\|F − 4"` → 5 hits,
all consistent:

- §6.3 [R-CNT-24]: "trailer magic at F − 64, version_major and version_minor at F − 56, and a
  CRC-32C at F − 4 covering bytes [F − 64, F − 4)". Trailer offset 8 = F−64+8 = F−56 ✓.
- [R-CNT-24]: "A future major MAY redefine only the remaining **48** trailer bytes." Fixed
  bytes are [0,8) ∪ [8,12) ∪ [60,64) = 16; 64 − 16 = 48 ✓. The redefinable span is [12,60).
- §2.3's Note: "F15 does not reach ... the trailer bytes it requires be zero are inside the
  48 that rule lets a future major redefine." F15's bytes are [48,60) ⊂ [12,60) ✓.
- §21.2 F14: "The u32 at trailer offset 60" ✓.
- §21.2 F15: "The **12** reserved bytes at trailer offset 48 ... | trailer reserved [48,60)" ✓.

`grep -n "48\b\|reserved bytes\|12 bytes\|zero slack"` → 13 hits after filtering; every
trailer-relevant one agrees with the table. Appendix A's annotation row reads
"[112, 124) | zero | trailer reserved, 12 bytes, zero" ✓.

I found **no stale trailer offset or width anywhere in the document.**

### 2.2 The "nine conditions" cross-check — a strong signal that the removal was propagated

[R-CNF-13] (§2.3) says: "`[R-CNT-06]` states nine, of which the trailer magic and the trailer
CRC assert invariants `[R-CNT-24]` fixes and the other seven do not."

I derived the nine from [R-CNT-06]'s own text rather than trusting the count:

1. trailer magic
2. trailer CRC
3. committed_file_length equals the file size
4. committed_file_length is a multiple of 64
5. dir_offset ≥ 16
6. dir_length ≥ 4
7. dir_offset + dir_length ≤ F − 64
8. file_id ≠ 0
9. reserved bytes zero

Nine exactly — and the version gate and flag gates, which [R-CNT-06] cites but does not
state, are correctly excluded. The register rows governed by [R-CNT-06] are F8, F14, F17,
F13, F9, F16, F10, F12, F15 — nine rows, one per condition.

**This is the number that would have been ten had the generation field survived with a
validity condition of its own.** It is nine. The removal reached this passage.

Similarly F11 is struck with an explicit Note ("A row label is retired on the model §2.2
states for a withdrawn requirement identifier"), and §21.2's stated count of 35 conditions
matches F1–F36 minus F11 = 35 (verified mechanically, §7 below).

### 2.3 The re-pointed sentences (brief's shape 10)

I censused every sentence that now names the committed file length where a counter used to
carry the ordering, and asked of each which property of its subject makes it true.

`grep -n "committed file length\|committed_file_length"` → 30 hits. The load-bearing ones:

- **§3.1**: "No field numbers generations; successive generations of one file are ordered by
  the strictly increasing committed file length their trailers carry (§9.3)."
- **[R-LIF-02]**: "A commit's committed_file_length is strictly greater than the prior
  trailer's, by at least 128, so the committed file length orders a file's generations."
- **[R-LIF-03]**: "Within one file_id, F strictly increases per commit — by at least 128 —
  so it orders that file's generations and **identifies each of them**."

The identity claim is the one that could have failed. It rests on "no two commits of one
file share a committed file length", which needs the strict increase, which §9.2's second
Note derives rather than asserts. I checked that derivation line by line:

> "Step 1 begins writing at exactly the prior F, and [R-LIF-01] holds every byte below it
> immutable, so this commit's directory lies at dir_offset ≥ the prior F; the Note above
> forbids reusing an earlier generation's, so there is such a directory; and [R-CNT-06]
> requires dir_length ≥ 4 and dir_offset + dir_length ≤ the new F − 64. The new F is
> therefore at least the prior F plus 68, and since [R-CNT-06] makes every committed file
> length a multiple of 64, at least the prior F plus 128."

- dir_offset ≥ F_prior (step 1 + [R-LIF-01] + §9.2's first Note forbidding reuse) ✓
- F_new − 64 ≥ dir_offset + dir_length ≥ F_prior + 4, so F_new ≥ F_prior + 68 ✓
- F_prior ≡ 0 (mod 64), F_new ≡ 0 (mod 64), F_new ≥ F_prior + 68 ⟹ F_new ≥ F_prior + 128 ✓
  (F_prior + 64 is excluded because it is below 68.)

The bound is **tight**: the smallest legal commit on an empty file is directory (4 bytes at
F) + pad to the next 64 boundary + trailer. From F = 128: dir_offset = 128, dir_length = 4,
dir end 132, pad to 192, trailer [192,256), F_new = 256 = 128 + 128. Exactly 128.

The three exposures I looked for, and where the document already closes each:

1. **Creation.** §9.2: "There being no prior committed file length, the strict increase above
   binds from the second commit onward." Closed.
2. **Rollback** (truncate to an earlier commit and re-append, presenting an already-seen F
   over different bytes). §9.3's third Note names it as "the rollback case §9.6 names as
   needing out-of-band state", and §9.6 adds the sharper observation that "A signed committed
   file length is not among them — the value is exactly what the re-append reproduces."
   Closed and disclosed.
3. **The ceiling.** §9.3's second Note: F ≤ 2⁶³ − 1 ([R-ENC-03]) and F ≡ 0 (mod 64)
   ([R-CNT-06]), so the reachable ceiling is 2⁶³ − 64. I checked: 2⁶³ = 64 · 2⁵⁷, so
   2⁶³ − 64 is a multiple of 64, and it is the largest one ≤ 2⁶³ − 1 ✓. "each commit adds at
   least 128 bytes, so a file there admits no further commit" ✓.

A fourth, which I raised and closed against the text: the identity claim is true of files
produced by a **conforming writer**, not of every conforming file — nothing in the file
predicate forbids a live trailer whose dir_offset points below every prior F, since
[R-CNT-06] asks only dir_offset ≥ 16 and dir_offset + dir_length ≤ F − 64. §9.3's third
Note says so outright: "The contract above also assumes a conforming writer." Closed.

Also checked as re-pointed sentences: §20.4's Rationale ("two trailers of one file_id are
ordered by committed_file_length without being counted"), §22.5's detached-signature claim
("pinned to the file_id its trailer names and to that F"), §23.2 ("No field carries a count
of the commits"), Appendix D ("no counter in the trailer numbering the commits"), §21.7 ("the
strict growth of `committed_file_length` across the commits of one file_id"). Each is true of
F, and §22.5's is true for the right reason — it signs the **prefix** [0,F), not the value F,
which is precisely the distinction §9.6 draws when it rejects a signed length as rollback
detection.

**Verdict on the trailer change: I found nothing wrong with it.**

---

## 3. Creation byte layout — a file built end to end

I built a small non-trivial file and gave every offset, saying for each whether the document
fixed it or left it to me.

Schema: one layer `sst`, rank 1, dimension `x` with E=100, T=32; one channel `temp`,
float32, fill quiet NaN 0x7FC00000; interleaved; linearization 1; codec 1 (none); filter 1
(none); A = 0; S = 0; A_slab = 0. Grid count G = ⌈100/32⌉ = 4 (§11.2), N = 4, entry_count = 4
(interleaved, [R-CNT-17]). Tiles 0 and 1 stored, tiles 2 and 3 sentinel.

Decoded size per tile: P = ∏Tᵢ = 32, Q = ΣBᵢ = 4, so P·Q = 128 bytes ([R-SER-02]). Codec 1,
so each stored extent is exactly 128 bytes ([R-COD-04]).

| range | bytes | what | fixed by |
|---|---|---|---|
| [0, 16) | 16 | front signature block `89 54 41 52 4E 0D 0A 1A` + 8 zero | **document** (§6.1) |
| [16, 144) | 128 | tile 0 payload | **mine** — placement free ([R-SLB-05]); only offset ≥ 16 is fixed (§15.3) |
| [144, 272) | 128 | tile 1 payload | **mine** |
| [272, 356) | 84 | tile-index region: 4×20 entry array + 1×4 segment CRC array | **mine** (placement); size **fixed** ([R-CNT-17]: 4·20 + ⌈4/2¹⁶⌉·4 = 84) |
| [356, 465) | 109 | directory: one layer record (24-byte header + 81-byte inline) + 4-byte CRC | order **fixed** (must be last structure, [R-CNT-05]); position **mine** |
| [465, 512) | 47 | pre-trailer pad | length **fixed** by [R-LIF-02] step 5 (pad to next 64 boundary); content **mine**, SHOULD be zero ([R-CNT-03]) |
| [512, 576) | 64 | trailer, committed_file_length = 576 | **fixed** (§6.2) |

F = 576, 576 mod 64 = 0 ✓. dir_offset + dir_length = 465 ≤ F − 64 = 512 ✓.
dir_offset = 356 ≥ 16 ✓. dir_length = 109 ≥ 4 ✓.

**The inline payload is 81 bytes**, which I derived independently before comparing against
§7.4's worked example:

```
 0  03 73 73 74                name: u8 len 3 + "sst"          → 4
 4  01                         layout 1 = interleaved          → 1
 5  01 00                      linearization 1                 → 2
 7  01 00                      codec 1 = none                  → 2
 9  01 00                      filter 1 = none                 → 2
11  00 ×8                      alignment A = 0                 → 8
19  00 ×8                      slab S = 0                      → 8
27  00 ×8                      A_slab = 0 (forced, [R-CNT-23])  → 8
35  01                         rank d = 1                      → 1
36  01 00                      channel count C = 1             → 2
38  01 78                      dim name: u8 len 1 + "x"        → 2
40  64 00 …                    extent 100                      → 8
48  20 00 …                    tile extent 32                  → 8
56  04 74 65 6D 70 0C 00       channel "temp", type 12         → 7
63  04 00 00 C0 7F             fill: u8 len 4 + 0x7FC00000     → 5
68  01                         index_encoding 1                → 1
69  04 00 …                    entry_count = 4                 → 8
77  ?? ?? ?? ??                crc_of_crc_array                → 4
```

4 + 34 + 18 + 12 + 13 = 81. §7.4's example asserts exactly this decomposition ("Name and the
nine scalars from layout through channel count occupy 4 + 34 bytes, the dimension entry 18,
the channel entry 12, and the trailing fixed fields 13 — 81 exactly"). The nine scalars are
layout, linearization, codec, filter, A, S, A_slab, d, C — nine, summing 1+2+2+2+8+8+8+1+2 =
34 ✓. Every number checks.

Record framing: type 0x0001, flags MU=1 PE=1 (§7.3, fixed by registry), inline_length = 81,
extent slot = (272, 84). Header 24 + inline 81 = 105; + 4 CRC = dir_length 109 ✓.

**Things the document left to me, enumerated:**

- the byte position of every stored tile and of the index region ([R-SLB-05]);
- the order in which I write them within step 2 ([R-LIF-02] step 2, "in any order");
- whether to store or sentinel a tile whose samples all equal fill (no rule; Appendix G item 6
  pins it for the profile);
- the content of every gap and of the pre-trailer pad ([R-CNT-03] is a SHOULD);
- `file_id`, any nonzero value (§9.3's randomness is a SHOULD);
- record order in the directory ([R-CNT-14]: "Record semantics MUST NOT depend on record order");
- tile extents, layout, codec, filter, alignment, slab (§7.4 value sets constrain, do not choose).

**Things the document fixed that I might have got wrong:**

- the pad goes *after* the directory CRC and *before* the trailer, and nothing else may lie
  between the directory's end and the trailer ([R-CNT-05], F7);
- both barriers, not one ([R-LIF-02] steps 4 and 6, restated twice in §20.2 and §20.5 —
  "both barriers, not one");
- on creation the front block is written first and its durability is covered by those same
  barriers (§9.2 says so explicitly, which I checked for because a creator that fsyncs only
  the tail would otherwise be conforming by omission);
- `A_slab` MUST be 0 when S = 0 ([R-CNT-23], L28), which is easy to write as 1;
- `crc_of_crc_array` MUST be 0 when entry_count = 0 ([R-CNT-23], L27);
- extent slot MUST be (0,0) when entry_count = 0 ([R-CNT-17], L22's fourth instance).

### 3.1 The degenerate creation — Appendix A, checked byte by byte

The brief said two of the changed passages are a byte-level worked example and its annotation
table. Appendix A is that pair, so I recomputed all of it rather than reading it.

I implemented CRC-32C from §4.5's parameters (Castagnoli reflected, init 0xFFFFFFFF, final
XOR 0xFFFFFFFF) and verified against §4.5's own check vector first:

```
CRC-32C("123456789") = 0xE3069283   ← matches §4.5
CRC-32C("")          = 0x00000000   ← matches §4.5
```

Then I reconstructed the trailer from the **field table**, not from the dump, and CRC'd it:

```
8a 4e 52 41 54 0d 0a 1a  01 00  00 00  00 00 00 00
10 00 00 00 00 00 00 00  04 00 00 00 00 00 00 00
80 00 00 00 00 00 00 00  ef cd ab 89 67 45 23 01
00 00 00 00 00 00 00 00  00 00 00 00
                                       (60 bytes)
CRC-32C = 0x402F157E → stored little-endian: 7E 15 2F 40
```

Appendix A's dump row `0070` ends `... 7E 15 2F 40`, and its annotation row says
"[124, 128) | `7E 15 2F 40` | trailer CRC-32C = 0x402F157E". **Match.**

Every other annotation row checks against the dump:
- [0,8) magic ✓, [8,16) zero ✓
- [16,20) `00 00 00 00` = CRC-32C of zero bytes ✓ (a 4-byte directory region holding only its
  own terminal CRC, dir_length = 4 = the [R-CNT-06] floor)
- [20,64) 44 zero bytes ✓ (16 + 4 + 44 + 64 = 128, matching §5.1's example's "44 bytes of slack")
- [72,74) `01 00` version_major = 1 ✓; [74,76) `00 00` minor 0 ✓; [76,80) flags 0 ✓
- [80,88) 16 ✓; [88,96) 4 ✓; [96,104) 128 ✓; [104,112) file_id 0x0123456789ABCDEF ✓
  (`EF CD AB 89 67 45 23 01` little-endian ✓)
- [112,124) 12 zero bytes ✓ — **the width that would be wrong if the removal had not been
  propagated here**

Appendix A's prose claims also check:
- "A remote reader opens this file in §6.4's two requests: the final 64 bytes ...; then
  [16, 20)" ✓.
- "a window of the whole file" is what reaches offset 0 on a 128-byte file ✓.
- "112 bytes covering [16, 128) contains the directory" — a 112-byte suffix of a 128-byte
  file is exactly [16,128), and it contains [16,20) ✓, while leaving [0,16) non-resident so
  [R-CNT-04]'s residency test lets the front-block check be omitted ✓.
- "§19.1's four-step open" — §19.1 has exactly four numbered steps ✓.

**Appendix A is correct, and correct specifically at the field that moved.**

I also recomputed §7.4's example CRCs, which are the other byte-level constants a creator
must reproduce:

```
4 sentinel entries (FF×16 00×4 repeated 4×, 80 bytes): CRC-32C = 0x80A34955 → 55 49 A3 80
CRC-32C over that 4-byte array                       :            0xC4EE982E → 2E 98 EE C4
```

§7.4 states `0x80A34955` / `55 49 A3 80` and `0xC4EE982E` / `2E 98 EE C4`. **Match.**

And §15.4's all-sentinel full-segment constant:

```
CRC-32C(65536 × "FF×16 00×4") = 0xEECB3BB2
```

§15.4 and Appendix B both state `0xEECB3BB2`. **Match.** (This is the one constant a sparse
writer is licensed to emit without computing, [R-IDX-05], so a wrong value here would have
been a direct byte-level fork; it is right.)

---

## 4. The append procedure

### 4.1 Order, durability, commit point

From [R-LIF-02] and §20.3 ([R-WRT-04]), the order I would actually emit bytes in:

1. **Establish F** by validating the trailer in the final 64 bytes of the *physical* file
   ([R-LIF-04], §20.3 step 1). If that fails, stop — recovery is a separate, deliberate
   operation (§9.6) and never an implicit step of opening for append.
2. **Open** as a reader (§19.1): trailer, directory, record walk, layer-name namespace.
   §20.3 step 2 fixes the blast radius of what the open finds: "reject-file bars every
   commit, and reject-layer bars a commit that modifies that layer." The open establishes no
   tile-scope violation because it fetches no extent.
3. **Validate what the commit touches** ([R-WRT-03]): the trailer and the *full* directory
   always — "re-emission (§20.4) relies on every directory byte" — plus §19.3's layer
   validation for every layer whose record, index, or extents this commit modifies, plus the
   §19.4 index chain for every segment whose entries this commit reuses.
4. **Write payloads and index regions**, beginning at exactly F.
5. **Re-emit the complete directory** and its CRC.
6. **Barrier** (steps 1–3 durable).
7. **Pad** to the next 64 boundary, then the **trailer**.
8. **Barrier** (trailer durable).

The **commit point** is step 8: until the full valid trailer is at the physical end and
durable, a reader on the default path sees a file whose final 64 bytes are not a trailer and
reports it torn ([R-LIF-05]). The document never says "the commit point is X" in those words,
but it is forced: [R-LIF-05] fixes the read path at trailer-at-end-or-fail and [R-CNT-06]
requires committed_file_length to equal the transport-authoritative size, so no intermediate
state is openable. §9.5's Note confirms the operational consequence ("A file being appended
to is not guaranteed remotely openable until its commit completes").

One thing I had to reason out rather than read: **during a commit the file is nonconforming.**
[R-CNT-01] makes the file size of a conforming file equal F, and mid-commit the physical size
exceeds F_old while the bytes at the physical end are not a trailer, so F8/F14/F17 fire. This
is derivable and §5.2 confirms the corollary ("Where §6.2's ordered validation rejects the
file before a live trailer is established there is no F and no live state to walk"), so I did
not raise it.

A second thing I had to resolve: §20.3 step 1 says an appender resuming from re-verified
recovery output "takes F from that output, then truncates to F or overwrites from it per
[R-LIF-04] — in which case F, never the physical end, anchors every step below." If the
appender takes the *overwrite* branch and then performs step 2's §19.1 open, the open's
F17 check would compare committed_file_length against a physical size that is still larger.
The sentence "F, never the physical end, anchors every step below" is what makes step 2
coherent, and it only does work if read as substituting F for the transport size in that
check. I adopted that reading; it is the only one under which the step-2 open can succeed at
all on that branch, and the clause is otherwise idle. Worth noting that the case is correctly
scoped: §9.4 establishes F "directly" only by validating the trailer at the physical end,
which forces committed_file_length = physical size, so "physical file longer than F" can only
arise out of recovery.

### 4.2 The three shapes of a commit, with the slack they produce

§20.3's own figure gives three shapes; I worked each against my file above (F = 576).

**(a) A new layer B.** Appends B's tiles, B's index region, a new directory carrying A's
record byte-identically (extent slot and all, so it still addresses A's original index at
[272,356)), pad, trailer.
Slack created: the old directory [356,465), the old pad [465,512), the old trailer [512,576)
— 220 bytes, sized by the file's layer count, never by any layer's data.

**(b) Superseding a stored tile of A.** Appends the new payload, A's **whole** index region
(84 bytes here — one entry re-pointed, three byte-identical), the new directory, pad, trailer.
Slack created: the superseded payload (128 bytes), the old index region (84), the old
directory + pad + trailer (220). §20.3's Note quantifies the general case correctly:
"editing one sample of a 10⁶-tile layer appends about 20 MB of index" — and 10⁶·20 + 64 =
20,000,064, so "about 20 MB" ✓.

**(c) A change confined to the directory** — clearing a slab declaration, renaming a layer,
or changing a channel's fill on a layer with no padding position and no pad bit. Only the
directory, pad and trailer are re-emitted; slack is the old directory + pad + trailer alone.

I checked shape (c)'s carve-out arithmetic against my own layer: E=100, T=32, so
E mod T = 4 ≠ 0 and the last tile *has* padding positions. So a fill change on my `sst` layer
is **not** an appender's operation once any tile is stored — exactly what §20.3 says
("A fill change on a layer that **stores** a tile carrying either is not an appender's
operation at all"). A layer with E = 128, T = 32 would have no padding position and the fill
change would be shape (c). The rule is decidable and I could decide it.

**In-place update** is not a shape: [R-LIF-01] makes every conforming mutation a commit or a
whole-file rewrite. The only bytes an updater may overwrite are those beyond F, and those are
never part of any committed state ([R-LIF-04]).

**Compaction.** Slack in the *output* is only the output's own pre-trailer pad plus whatever
gaps the compactor's placement leaves; the input's slack is not carried (§20.5). The input
file persists unmodified until something outside the format deletes it ([R-PRV-02]).

**Abandoned partial write.** The bytes past F are *not* slack of any live state: §5.2 says
that where §6.2's ordered validation rejects the file before a live trailer is established,
"there is no F and no live state to walk, so the total is not owed at all". They are residue,
and [R-LIF-04] obliges the next writer to truncate to F or overwrite from it and truncate no
later than step 6. §9.5's Note closes the loop on what a reader sees ("Residue past a
completed commit carries no register row of its own").

**Who counts slack.** A verifier, and only where its walk completes ([R-CNT-21], §9.7). Where
the walk does not complete the total is reported as *partial* — "F less the bytes claimed by
the claimants the walk did enumerate", an upper bound. I checked that this is an upper bound
and not an under-count: discarding claimants can only raise F − claimed ✓. And I checked it
against Appendix A's file: 128 − 16 (front) − 4 (directory) − 64 (trailer) = 44, which is
§5.1's stated "44 bytes of slack" ✓.

**What slack may contain.** Anything: "Slack has no internal structure this specification
defines, its content is unconstrained, and no conformance requirement applies to it"
([R-CNT-21]). Writers SHOULD zero the gaps they create ([R-CNT-03]) and forfeit byte
reproducibility if they do not. The one thing slack may **not** contain is a live structure
between the directory's end and the trailer (F7, [R-CNT-05]) — and a longer-than-minimal
pre-trailer gap is conforming though no conforming commit produces one, which §2.3
[R-CNF-02] names as one of exactly two express conduct carve-outs.

I derived that pair myself rather than trusting the count. [R-CNF-02] separates (i) rules that
govern *conduct rather than output* — "where a value is published, or which registry version
a writer targets (§10.3, §18.3)" — from (ii) writer obligations over output whose violation
is expressly not a file-conformance violation, of which it says the two cases are §6.3's
flags = 0 against a set ignore-lane bit and §6.2's over-long pre-trailer gap. I hunted for a
third in class (ii) and the best candidate was [R-MTA-06]'s "writers MUST NOT emit a `tarn.`-
prefixed key this specification's registry does not define at the version they target",
whose file §21.6 declares conforming. That is §18.3 — already named in class (i), and
correctly so, since the violation turns on which registry version the writer targeted and
not on the bytes. The enumeration holds.

### 4.3 The record-flag matrix

The brief asked me to walk every combination the document defines and say what my updater may
do. §7.2 defines bit 0 = MUST_UNDERSTAND, bit 1 = PRESERVE_ON_EDIT, bits 2–15 reserved.
§20.4 splits by *whose* flags are authoritative first, which is the axis I would have missed.

**Axis 1 — where the flags come from ([R-WRT-08]'s paragraph):**

- type §7.3 registers (0x0001 layer, 0x0002 user metadata): the **registry's** fixed flags
  govern, not the stored ones ([R-CNT-22]). Both are MU=1/PE=1 and MU=0/PE=1 respectively, so
  neither can ever be dropped. A stored bit differing from the registry is F28/L49 —
  verifier-detected, and the reader processes the record under the fixed semantics anyway.
- type the updater implements but this specification does not register: "the definition it
  implements the type from supplies the flags, and the stored bits never do".
- type the updater does **not** implement: stored flags authoritative, and MU=1/PE=0 is read
  as PE=1 ([R-CNT-12], "never silently deletable").

**Axis 2 — the four flag combinations, for an unimplemented type:**

| MU | PE | top-level | layer sub-record |
|---|---|---|---|
| 1 | 1 | **No commit is available at all.** [R-CNT-15] makes an unimplemented top-level MU=1 record reject-file, and the updater is a reader first (§2.3). A compactor MUST refuse ([R-WRT-06]: such a type "can define references this specification does not"). | Retain byte-identical; MUST NOT modify **that layer** ([R-CNT-18] makes it reject-layer, and "where the file is otherwise conforming a reader MUST NOT reject the file for it"). Other layers stay editable. A compactor MUST still refuse the whole file. |
| 1 | 0 | Not emittable ([R-CNT-12]); read as PE=1, so as above. Verifier-detected as F25. | As above. Verifier-detected as L46. |
| 0 | 1 | Retain byte-identical, extent content unmodified. | Same. |
| 0 | 0 | Retain byte-identical, **or drop** — extent becoming slack — but only in a commit that *independently* changes the file's layer set, any layer record's content, or another non-layer top-level record. A compactor MAY drop it whenever it rewrites. | Same, with the scope-changing triggers being that layer's record, the entry set of its index, or which of its tiles are stored. |

Reserved bits 2–15: writers MUST emit zero, readers MUST ignore, verifiers treat any set bit
as F26/L47.

I stress-tested the MU=0/PE=0 independence condition against the commit shapes above and it
holds together. Shape (b) is explicitly blessed: "Superseding a stored tile's bytes re-places
that layer's index region, moving its extent slot and so modifying that layer's record, which
is such a change". Shape (a) changes the layer set. Shape (c) changes a layer record's content.
And the anti-bootstrap clause is there: "Dropping the record, or dropping another record in
the same commit, is not itself such a change, so a commit whose only effect would be the drop
MUST retain it."

One reading I probed and could not turn into a finding: does "changes ... another *non-layer*
top-level record" cover **adding** a new one? "Changes the layer set" is glossed as including
addition ("A commit changes the layer set by adding a layer"), but the third object is a
record rather than a set, and "changes a record" reads as modifying an existing one. I settled
on the narrow reading (adding a record does not license the drop) because the gloss on the
first object is what would have been needed on the third had addition been meant, and because
[R-CNT-14] caps top-level user-metadata records at one so the interesting case is thin.

### 4.4 Appending to a file whose records I do not all understand

Concretely: my updater implements 0x0001 and 0x0002 and nothing else, and the file carries an
unknown top-level type 0x8123 with MU=0/PE=1 and an unknown sub-record type 0x9000 with
MU=0/PE=0 on layer A.

- I re-emit 0x8123's header, inline payload and extent slot **byte-identically** ([R-WRT-05]),
  leaving its extent where it lies. I MUST NOT re-encode it and MUST NOT relocate its extent —
  [R-WRT-08] permits relocation "only ... under §20.5", which is compaction's operation, not an
  appender's.
- The 0x9000 sub-record I may drop only if this commit independently changes layer A's record,
  its index entry set, or its stored-tile set. If I supersede a tile of A, I may; if the
  commit only adds layer B, I may not.
- If the same unknown top-level type carried MU=1 I could not commit at all, and if the
  sub-record carried MU=1 I could commit to every layer but A.
- Its extent is covered by **no checksum** (§8.1's last row), so corruption inside it is
  invisible to me and to any verifier — §22.4 [R-SEC-04] states this residue rather than
  defending it, and notes that byte-identical re-emission "carries such an extent forward
  unread, and [R-WRT-08] bars re-encoding it, so nothing an updater does would surface the
  damage."
- If the type were from the **reserved** range (0x0003–0x7FFF) rather than experimental, the
  file is nonconforming (F36/L25, verifier-detected) but I read it under the same MU rule, and
  §20.3 step 2 tells me exactly what to do: carry it forward, do not repair it, and SHOULD
  report it — "a caller that is not told cannot know the file it extended was already damaged."

The one place I had to reason and the document met me: an appender that meets a **malformed
index entry** while re-emitting a region does not repair it to a sentinel. §20.3 step 2 says
it "is carried forward byte-identically at its disk-ordinal position under step 4", and gives
the reason — "Reproducing a structure's bytes unchanged is not authoring them."

---

## 5. Torn-write recovery — four crash points

**Crash A: during step 4 (payloads/index), before the directory.**
Physical file = F_old + k, tail is payload bytes. Next reader: the 8 bytes at
physical_size − 64 are not the trailer magic → F8 → reject-file, reported torn ([R-LIF-05],
which forbids scanning backward). Next updater: §20.3 step 1 fails, so no append; §9.6's
deliberate probe finds trail_n at F_old − 64 (64-aligned, since F_old ≡ 0 mod 64), requires
its CRC to verify and its committed_file_length to equal o + 64, and truncating to F_old
restores the file exactly. Conforming in the meantime? **No** — F17/F8 both fail.

**Crash B: after the directory is written, before the step-4 barrier.**
Indistinguishable from A to a reader; the difference is only that the barrier had not ordered
the writes, so an arbitrary subset of [F_old, F_new) may be present. §9.2's third Note is the
right frame: "Where barriers are weaker than assumed, safety degrades from 'torn commits are
invisible' to 'torn commits are detected'."

**Crash C: mid-trailer (step 7 partially durable).**
The physical end may now be a 64-aligned position holding a partial trailer. Magic may match
(it is written first) but the CRC over [0,60) will not → F14 → reject-file. Recovery as in A.
This is the case that makes the trailer CRC load-bearing rather than decorative, and it is
also why [R-CNT-24] pins the CRC's position across majors.

**Crash D: after the trailer is durable but before truncation, on [R-LIF-04]'s
overwrite-without-truncate branch.**
Physical size > F_new, so the bytes at physical_size − 64 are stale residue → the trailer
gates fail → reject-file. §9.5's Note names exactly this and assigns the fault correctly:
"What the residue violates is [R-LIF-04]'s writer obligation to truncate or overwrite, and
the state a reader can observe is already named." The recovery probe finds the *new* trailer
at F_new − 64 and truncating there yields the committed new generation — so unlike A–C, the
recoverable state here is the new one, not the old.

**Crash E (the one I added): after step 8, during a subsequent unrelated write.**
Not a torn commit; the file is conforming and the new generation is live.

In every case, what makes recovery possible rather than merely detectable is that trail_n and
everything it reaches are byte-intact — §9.2's Example puts it exactly right: "The window is
not one in which the old state is *readable* — it is one in which the old state is
*recoverable*."

Two normative cautions I would build into the recovery tool, both from [R-LIF-06]: re-verify
the truncated output **as a whole file** before trusting it, because a tile payload can
deliberately mimic a trailer; and accept that truncation to an earlier commit boundary is
indistinguishable in-format from that earlier version — "no field of this format supplies"
rollback detection, and a *signed committed file length* is explicitly not a substitute since
"the value is exactly what the re-append reproduces." Also: the probe must continue past a
candidate whose whole-file re-verification fails, and the tool MUST report which candidate it
settled on and how many it rejected.

---

## 6. Byte-divergence catalogue, checked against Appendix G

Given identical input arrays and identical stated options, here is every way I can make two
conforming writers diverge, and whether the reproducible-writer profile closes it.

| # | Degree of freedom | Where the format leaves it open | Closed by |
|---|---|---|---|
| 1 | Compressed-stream bytes for a given codec (block/match/table choices; deflate's up to seven unused final-byte high bits, §17.2's Note) | [R-CNF-05]; RFC 1951/8878 constrain decoders, not encoders | **item 1** (pin implementation + version + settings, thread count included) |
| 2 | `file_id` | §9.3: any nonzero value; randomness is a SHOULD | **item 2** (hash of [0, F−64) ‖ trailer[0,60) with file_id zeroed; last eight digest bytes, LE; 1 substituted if all zero) |
| 3 | Placement of every structure, and the *extent* of every gap | [R-SLB-05], [R-LIF-02] step 2 | **item 3** (total emission order, contiguous from 16) |
| 4 | Content of every gap and of the pre-trailer pad | [R-CNT-03] is a SHOULD | **item 3** ("every byte of every such gap is zero — [R-CNT-03]'s advice, taken as a requirement here") |
| 5 | Record and sub-record order in the directory | [R-CNT-14] ("Record semantics MUST NOT depend on record order") | **item 3**'s sort key |
| 6 | Number of commits | §9 constrains it nowhere | **item 4** (one generation) |
| 7 | Declared alignment A / slab S, A_slab | §16 leaves them to the writer | **item 5** |
| 8 | Filter value (1 vs 2) | §17.3 leaves the choice to the writer | **item 5** |
| 9 | Whether an all-fill tile is stored or sentinel | no rule requires either | **item 6** |
| 10 | The fill a writer records when the caller chooses none | [R-TYP-10] is a SHOULD | **item 7** |
| 11 | `version_minor` (any value ≥ the floor) and ignore-lane `flags` bits | [R-CNT-26] is a SHOULD; [R-WRT-06] for a compactor | **item 8** |
| 12 | User-metadata JSON serialization (number formatting, whitespace) and its zstd framing | [R-MTA-05] sorts members but "does not make two writers' output identical" | **item 9** |
| 13 | Name normalization (NFC vs NFD) | [R-ENC-14] is a SHOULD | **item 10** |
| 14 | **Channel layout** (interleaved vs planar) | §7.4 value set; §14.4's Note confirms both are valid for the same content | **not pinned by any item** |
| 15 | **Tile extents** T₀…T_{d−1} | §11.3's Note: "Tile extents are a writer's choice, and this specification imposes none" | **not pinned by any item** |
| 16 | Dimension declaration order and channel declaration order | §3.1: "the declared order is load-bearing", but nothing fixes which order a writer picks for given data | **not pinned by any item** |

Non-divergences I checked and confirmed are *not* freedoms, because a careless catalogue
would list them:

- The segment CRC of an all-sentinel full segment: [R-IDX-05] lets a writer emit `0xEECB3BB2`
  "without computing it", but the constant **equals** the computed value (I verified it), so
  there is no fork. And the rule is careful the other way: "Equality with the constant
  licenses nothing for readers."
- `entry_count`, `extent_length`, `crc_of_crc_array`, `inline_length`: all determined
  ([R-CNT-17], [R-CNT-23], §7.4's exact-parse rule).
- Extent slot for entry_count = 0: forced to (0,0) (L22's third and fourth instances).
- Trailer reserved bytes and record reserved flag bits: forced to zero.
- `linearization` and `index_encoding`: only value 1 is emittable.
- Codec 1 stored length: forced to the decoded size ([R-COD-04]).

I also verified two of Appendix G's own load-bearing claims rather than accepting them:

- **Item 5's identity condition.** "The filter is the identity exactly where its permutation
  is — where the stride is 1 ... and equally where the decoded image is a single group,
  n = L/s being 1." [R-COD-10] maps byte *i* of group *j* from offset j·s + i to offset
  i·n + j. Identity requires j·s + i = i·n + j for all i < s, j < n. Taking i = 0, j = 1 gives
  s = 1; taking s > 1 and n = 1 gives j = 0 always, so the map is i ↦ i. So identity holds
  **iff** s = 1 or n = 1. "Exactly where" is exactly right.
- **Item 3's tie-break soundness.** Ordering non-layer records by "the record's header with
  extent_offset masked to zero, then its inline payload, then the contents of its extent"
  is well founded precisely because extent_offset is the one component the order itself
  fixes — "a key containing it would depend on its own result". And the claim that two
  records the key does not separate are byte-identical in everything but extent_offset
  follows, since the key covers type, flags, inline_length, extent_length, the payload and
  the extent contents. Correct.
- **Item 10's example.** `température` is 12 bytes in NFC (`é` = C3 A9) and 13 in NFD
  (`e` + CC 81), and a name differing only by canonical reordering has the same length in
  both forms. Correct, and it matches §4.6's own example byte for byte.

Rows 14–16 are what I could not close, and they are the subject of finding **writer-01**.
They are not "divergences I cannot classify" — each is plainly *legitimate* under [R-CNF-05]
and §7.4 — but the profile that claims to close what the format leaves open does not close
them, while closing the filter on an argument that applies to all three verbatim.

---

## 7. Sweeps I ran mechanically

### 7.1 Register self-consistency

I parsed every row of §21.2–§21.5 out of the file and counted instances by §21.1's own stated
rule ("Instances within a cell are separated by semicolons, and a cell reading — is one
instance; the count is therefore mechanical once the cell is written").

```
F rows 35   instances  56
L rows 49   instances 116
T rows 26   instances  55
R rows 10   instances  48
TOTAL 120   instances 275
```

- §21.2 claims "35 conditions" ✓ (F1–F36 minus the struck F11).
- §21.3 claims "49 conditions" ✓ (L1–L49).
- §21.4 claims "26 conditions" ✓ (T1–T26).
- §21.5 claims "10 conditions" ✓ (R1–R10).
- §21.8 [R-ERR-02] claims "120 conditions over **275** instances" ✓ — **exact match on both.**

I spot-checked the instance convention against a dozen cells: L37 and F14 are checksum
comparisons and take one instance each ("A comparison with no magnitude ordering enumerates no
direction"); T3, T14 and T22 take 3 layout formulas × 2 directions = 6 each; T21 and L44 are
one-directional *exceeds* comparisons and take 3 each; F5 takes 2 because a file can have
physical size < 128 with committed_file_length ≥ 128 or the converse. All consistent.

### 7.2 Requirement identifier density

I extracted every `[R-XXX-NN]` and every bare `R-XXX-NN` parenthetical citation. Every prefix
is dense from 1 to its maximum with no gaps: CNF 1–13, CNT 1–27, COD 1–11, ENC 1–16
(plus the illustrative `[R-ENC-100]` in §2.2), ERR 1–5, EXT 1–5, GEO 1–6, IDX 1–5, LIF 1–8,
MDL 1–2, MTA 1–10, PRV 1–5, RDR 1–4, SEC 1–7, SER 1–9, SLB 1–5, TYP 1–10, VEC 1–4, WRT 1–9.
`[R-SER-04]` appears only in §14.4's withdrawal Note, which is correct under §2.2 ("a
withdrawn requirement leaves its identifier permanently retired"), and `[R-SER-09]` occupies
the next free number rather than reusing 04.

### 7.3 The SHOULD discipline

§2.1's Note claims "every SHOULD states the consequence of deviation". I grepped all 24
SHOULD/SHOULD NOT occurrences outside §22–§24 and checked each. Every one states a
consequence: [R-ENC-14] "risks visually identical but byte-distinct names coexisting";
[R-CNT-03] "leaves bytes indistinguishable from stale data and forfeits byte reproducibility";
[R-CNT-09] "merely costs the second request"; [R-CNT-10] "remote open fails outright on such
transports"; [R-CNT-26] "misstates the file's feature floor to tooling"; [R-LIF-03] "lets two
distinct files collide in the (file_id, range)-keyed caches"; [R-LIF-07] "recoverable only by
scanning back across its entire length"; [R-TYP-10] "read back as a value consumers of the
conventional zero default will not expect"; [R-COD-06] "merely permits a conforming reader to
decline"; §20.3's "produce a new file" SHOULD is paid for by "slack that is not data the
caller chose to discard is paid for and never read"; §20.3 step 2's report SHOULD by "a caller
that is not told cannot know the file it extended was already damaged"; [R-WRT-06]'s minor
floor by "a lower minor understates the file's feature floor to tooling". **No bare SHOULD.**

### 7.4 Worked arithmetic elsewhere in the document

I recomputed every numeric example a writer would copy. All correct:

- §11.2: G = (4, 8), N = 32, P = 65,536; ⌈1000/256⌉ = 4.
- §11.4: tile (1,0) → 8; (300,700) → tile (1,2), s = 10, in-tile (44,188), ordinal
  44·256 + 188 = 11,452; planar channel 2 → 2·32 + 10 = 74.
- §14.2: Q = 3, decoded 18, ordinal 5 at [15,18); planar b-plane 12 bytes, ordinal 5 at 10–11;
  float32+bool Q = 5, decoded 30, ordinal 5 at [25,30).
- §14.3: P = 10 alternating → `55 01` with fill false, `55 FD` with fill true (pad bits 2–7).
- §14.5: extents (5,5), tiles (4,4) → grid 2×2, edge tile (1,1) has 1 real and 15 padding
  positions, 32 bytes, values 1–15 each `CD AB`.
- §15.4: entry_count 1,000,000 → 16 segments (15 full + 16,960), 64-byte CRC array, region
  20,000,064 bytes; k = 999,999 at segment-relative 339,180; CRC array at
  [20,000,000, 20,000,064); segment 15 at [19,660,800, 20,000,000) = 339,200 bytes ≈ 339 KB;
  a full segment is 65,536·20 = 1,310,720 = 1.25 MiB.
- §16.2: N = 32, S = 8 → runs [0,8), [8,16), [16,24), [24,32); rows 1–2 are ordinals 8–23.
- §17.3: the three-float32 shuffle. I applied i·n + j by hand and got
  `00 00 00 00 00 00 80 00 40 3F 40 40`, matching the stated result byte for byte.
- §20.3: 32·20 + 4 = 644.
- §21.9's Note: 2³²/2¹⁶ · 4 = 2¹⁸ = 256 KiB; 2³⁶/2¹⁶ · 4 = 2²² = 4 MiB.
- §9.3's ceiling: 2⁶³ − 64 is the largest multiple of 64 at or below 2⁶³ − 1.
- §14.4's P = 1 claim: planar byte = value bit | (fill ? 0xFE : 0), interleaved byte = value;
  they coincide iff fill is false. Correct.
- §12.3 / §7.4: the twelve-byte `temp` channel entry appears identically in both places.

### 7.5 Degenerate legal cases I built (brief's shape 8)

- **Zero layers.** Appendix A's 128-byte file. Directory is 4 bytes of CRC over zero bytes.
- **A dimension with extent 0.** N = 0, entry_count = 0, extent slot (0,0),
  crc_of_crc_array = 0, no index region at all. [R-GEO-02] and §15.4's closing Example agree.
  I checked that such a layer escapes [R-COD-07]'s lz4 cap (§17.2's Note says so, and says
  "The escape ends exactly when the layer's addressed-tile count rises above 0") while
  [R-ENC-04]'s ceiling still binds P·Q and P·Bᶜ. Both are right, and L44 and L2 register them
  separately.
- **entry_count = 1.** Index region 20 + 4 = 24 bytes; one segment; the "partial segment's CRC
  MUST be computed" branch of [R-IDX-05].
- **P = 1, single bool channel.** Both layouts one byte; §14.4's coincidence condition.
- **A tile made entirely of padding.** Cannot exist: t_i < G_i = ⌈E_i/T_i⌉ implies
  t_i·T_i < E_i, so every addressed tile has at least one real position. I checked this
  because [R-SER-05] and §13.3 would interact strangely otherwise; they do not.
- **Minimum commit.** From F = 128, the smallest next F is 256 — the [R-LIF-02] bound is tight,
  not merely sound.

### 7.6 Writer-side invariants under committed-prefix immutability

A consequence I worked out and then found the document had already handled: a **slab-declared
layer cannot grow contiguously by appending**, because [R-SLB-03] requires each stored tile's
offset to equal the previous stored tile's offset plus its length, while [R-LIF-01] and
[R-LIF-02] step 1 force every new byte to land at or above F. So an appender adding a stored
tile to a run that already has stored tiles must either re-emit the entire run above F
(stranding the originals as slack) or clear the declaration. [R-SLB-04] states exactly that
disjunction — "MUST either re-establish the invariants for every such run — or clear the
declaration in the new generation" — and §20.3 pairs it with the SHOULD to write a new file
where a commit "would strand a large share of a layer's stored bytes".

I also checked the two quantifier holes I expected in [R-SLB-04]:
- A commit that **newly declares** a slab on a layer that never had one is outside
  [R-SLB-04]'s antecedent ("a slab-declared layer"), but [R-SLB-03] is a live-state invariant
  that catches it as L41/L42 regardless. Closed.
- A commit that changes only **A_slab** triggers none of [R-SLB-04]'s three conditions, but
  again [R-SLB-03] catches a misaligned first stored tile as L42. Closed.

And the alignment analogue in §20.3 step 4 is quantified explicitly and correctly: "an aligned
layer's stored tiles — **every one the new state keeps, not only those this commit adds** —
satisfy its invariant or the declaration is cleared."

---

## 8. Suspicions I opened and closed

Recorded because a lane that finds little should be able to say what it did that would have
found something.

1. **Does F actually identify a generation?** Closed by §9.3's third Note, which discloses
   both the reused-file_id collision and the truncate-and-re-append case.
2. **Is §9.2's derivation of the 128-byte minimum increase sound?** Recomputed; sound and
   tight. Closed.
3. **Does the recovery probe still work without a counter?** §9.6's "nearest-to-end valid
   candidate" is equivalent to "largest F", since the probe requires
   committed_file_length = o + 64. Closed.
4. **Is `[R-CNT-06]`'s "nine" still nine?** Derived independently; yes. Closed. (This is the
   count that would have been wrong if the removal had been half-propagated.)
5. **Is Appendix A's trailer CRC still right at the new field offsets?** Recomputed
   0x402F157E from the field table. Closed.
6. **§6.2's Note: "A payload byte-string that mimics a trailer ... is caught at the directory
   CRC (§7.1) — detection is never silent."** I built the counterexample: a crafted mimic at
   the exact physical end whose dir_offset/dir_length address the *previous* generation's
   still-intact directory would pass the directory CRC too, and would present as a conforming
   file reading that earlier generation. But §21.6's row and [R-LIF-06]'s second caution
   already carve exactly this out ("which catches any mimic that is not itself a consistent
   generation; §9.6's second caution covers the rest"), and the resulting state is benign —
   the reader gets a correct earlier generation, not corruption. The Note is loose, not wrong
   about the case it is glossing. Not reported.
7. **Do [R-LIF-02]'s durability barriers appear in §21.7's account of what no check detects?**
   They do not, by name. §21.7's second class is "obligations ... [where] a single file
   exhibits no witness of their violation", which the barriers plainly join, and §21.1 calls
   §21.7 "the account, **by class**" rather than an inventory. §20.2, §20.5 and Appendix H all
   state the barrier obligation ("both barriers, not one") so it is not lost. Not reported.
8. **Does the §20.4 table carry a requirement identifier?** It sits between [R-WRT-05] and
   [R-WRT-08] and is always cited by section ("§20.4's table", "the preservation obligations
   of §20.4"), never by identifier. [R-CNF-01] makes it normative regardless and [R-CNF-06]
   anchors it to §20.4 as a whole. Cosmetic; not reported.
9. **Is §21.6's "The file contains zero layers | A conforming file with an empty directory"
   over-narrow?** A file with zero layers may still carry a top-level user-metadata record, so
   its directory is not empty. But [R-CNT-14] itself says "zero is valid: an empty directory is
   a conforming generation", meaning zero *layer records* is valid and the empty directory is
   the extreme case. Reading it as a biconditional is uncharitable. Not reported.
10. **May an appender relocate a live index region?** No — §20.3 step 4 is explicit
    ("relocating a live index region is compaction's operation ..., not an appender's"), and
    [R-WRT-08] confines relocation of an unimplemented record's extent to §20.5. Closed.
11. **Is §20.3's "the bar above is the whole of the test" for a shrink missing the proviso the
    growth clause carries?** The growth clause adds "provided the grown geometry stays within
    every bound the layer's own declarations impose, [R-COD-07]'s lz4 decoded-size cap among
    them"; the shrink clause has no such proviso. I looked for a rule a shrink could newly
    violate. A shrink lowers Eᵢ, hence Gᵢ, hence N and entry_count; it changes no Tᵢ, so no
    decoded size, so no lz4 cap and no [R-ENC-04] product grows; [R-CNT-17] is discharged by
    the re-emitted index the same paragraph already requires; [R-SLB-04] covers the changed run
    partition; kept tiles keep their offsets so [R-SLB-01] is untouched; and a shrink to
    entry_count = 0 relaxes rather than tightens. The asymmetry is correct: growth can create
    violations and shrink cannot. Closed.
12. **May a planar layer with stored tiles gain or reorder channels?** Yes — nothing §14 fixes
    for an existing tile changes (its decoded size is P·Bᶜ for its own channel, its padding
    content is its own channel's fill), so §20.3 step 4's bar does not reach it. This is what
    led to finding **writer-03**.
13. **Does §14.4's "single-channel numeric layer produces byte-identical tile images under
    either layout" survive the index too?** Yes: for C = 1 the planar disk ordinal c·N + s
    reduces to s, entry_count is N either way, and the byte-shuffle stride is B⁰ = Q either
    way. The whole file coincides, not just the tile images. Closed, and it confirms the
    §20.3 bar correctly permits a C = 1 numeric layout flip.
14. **Are the bytes past F in an abandoned partial write "slack"?** §5.2 answers directly —
    with no live trailer "the total is not owed at all" — so the question does not arise for a
    verifier, and [R-LIF-04] tells the next writer what to do with them. Closed.
15. **Do §21.1's "strict specialization" pairs hold?** I checked all six. F21 ⊂ F22 (a (0,0)
    slot has extent_length 0 < 5) ✓; L10 ⊂ L11 ✓; F35 ⊂ F36 ✓; L24 ⊂ L25 ✓; F1's front
    instance ⊂ F6's magic instance ✓; F1's trailer instance ⊂ F8 ✓. Closed.
16. **Does §21.2's reach derivation hold?** [R-CNT-24] fixes four invariants: magic at F−64,
    versions at F−56, CRC at F−4 over [F−64,F−4), and the constant front block. The rows
    asserting only those are F8, F14, F6, and both F1 instances — and no other, since F13's
    64-alignment, F17's length cross-check, F15's reserved bytes and F5's 128-byte floor each
    rest on format-major-1 material. The Note's three worked cases (F14 reaches, F5 does not,
    F15 does not) are each right. Closed.
17. **Is §8.1's "every field covered by exactly one checksum" true after the change?** The
    trailer's CRC covers [0,60), which is every trailer field including the widened reserved
    span. Closed.

---

## 9. Findings

### writer-01 — AMBIGUITY

**Location.** Appendix G (non-normative), preamble and items 2 and 5.

**Quotation.**

> "Applications that need byte-identical output — content-addressed storage, reproducible
> builds — can adopt this profile, which closes the degrees of freedom this format
> deliberately leaves open."

and, from item 2:

> "this format fixes no canonical serialization of logical content, and two files carrying the
> same arrays can legitimately differ in tiling, layout, and codec."

and, from item 5:

> "**A fixed filter value** likewise: §17.3 leaves the choice to the writer, and no content
> implies it, so two writers agreeing on everything else still disagree on bytes without it
> pinned."

**The problem.** Item 5 pins the filter value with an argument in three parts — §17.3 leaves
the choice to the writer; no content implies it; unpinned, two otherwise-agreeing writers
diverge. Every clause of that argument is true, word for word, of **channel layout** (§7.4's
`layout` field; §14.4's Note confirms interleaved and planar tile images differ for any bool
channel and for any multi-channel layer) and of **tile extents** (§11.3's Note: "Tile extents
are a writer's choice, and this specification imposes none"), and of **dimension and channel
declaration order** (§3.1: "the declared order is load-bearing"). None of the ten items pins
any of them, and the closing paragraph's enumeration of "what is not [already mandatory]"
does not name them either. Meanwhile item 2 concedes that tiling and layout "legitimately
differ" — in the same breath as codec, which item 1 does pin.

**Permitted readings.**

- **(A) "the same input" includes the full layer schema** — layout, tiling, dimension order,
  channel order, fill, names, and codec ID. Then the profile is complete, but item 5's filter
  clause is redundant, since the filter is a `u16` field of the same layer record supplied by
  the same caller; and item 1's pinning of the *codec choice* is likewise redundant.
- **(B) "the same input" is the logical arrays** (item 2's own framing: "two files carrying
  the same arrays"). Then item 5 is doing necessary work, item 1's codec clause is doing
  necessary work — and the profile is incomplete, because two writers each satisfying all ten
  items can still emit different files by choosing planar over interleaved, or 256×256 tiles
  over 512×512.

**Which I picked, and why.** (B), because it is the reading under which items 1, 5, 6 and 7
each do work rather than restating a caller's supplied option, and because item 2 states it
in those words. Under (B) the preamble's claim that the profile "closes the degrees of freedom
this format deliberately leaves open" is false of at least three such freedoms.

**What an implementer does wrong without it.** Two vendors each certify their writer as
profile-conformant and get different bytes for the same arrays, which defeats the profile's
only purpose — and defeats it in a way the appendix's own refutation model ("conformance to
the profile can be refuted cheaply but confirmed only by reproducing the file") cannot
diagnose, since neither writer has violated a numbered item.

**Byte-level: no.** Appendix G is non-normative and says so twice, and adds "no requirement to
any actor: a writer ignoring it is fully conforming". Both readings leave every file
conforming under [R-CNF-05], so the emittable set does not move. This is a defect in a profile
an implementer will build to, not in what the format admits.

---

### writer-02 — OBSERVATION

**Location.** §20.1, [R-WRT-01], the writer-tier list.

**Quotation.**

> "**appender** — extends an existing file by commits (§9.2): adding layers or records,
> superseding tiles, growing extents, amending metadata."

**The problem.** This is normative text (§20.1 carries no *Note*, *Example* or *Rationale*
label, so [R-CNF-01] makes it normative), and it is the definition an implementer reads to
learn what tier they are building. Its enumeration omits at least three operations that
§20.3 and §20.4 spend paragraphs permitting to an appender, all of them in the same commit:

- **shrinking an extent.** §20.3 devotes two full paragraphs to it: "An extent MAY also
  **shrink**, and the bar above is the whole of the test, **in the bar's own tense** ... Where
  a shrink is permitted the de-addressed tiles' extents become slack ([R-CNT-21]),
  [R-CNT-17] obliges the smaller entry_count and so a re-emitted index region, and every
  surviving stored tile is untouched."
- **unstoring a tile.** §20.3 step 4: "entries for tiles that become unstored written as the
  sentinel"; §23.1 names it as a distinct operation from superseding — "superseding a stored
  tile's payload, unstoring a tile so its entry becomes the sentinel ... and a shrink that
  either drops tiles out of the addressed set or turns real positions into padding".
- **dropping an MU = 0 / PE = 0 record.** §20.4's table: "Retain byte-identical, or drop it —
  its extent becoming slack. An appender MUST NOT drop it except in a commit that
  *independently* changes the scope the record attaches to."

The pairing is what makes the omission conspicuous rather than merely brief: the list names
"growing extents" and not shrinking them, and names "superseding tiles" and not unstoring
them, in each case taking one half of a pair the governing section treats symmetrically.

**Which reading I picked.** That the list is illustrative and the defining clause is "extends
an existing file by commits (§9.2)", so §20.3 and §20.4 govern and an appender may shrink,
unstore and drop. The alternative — reading the list as constitutive of the tier, so that a
tool doing any of the three is not an appender — would put §20.1 in direct conflict with
§20.3's own permissions, which is not a reading the document can have meant.

**What an implementer does wrong without it.** They ship an appender that refuses to shrink an
extent or unstore a tile, and route those callers to a whole-file rewrite — paying a full copy
for an operation §20.3 explicitly permits in place, and one §20.3 itself says is cheaper as a
commit except "wherever a commit would strand a large share of a layer's stored bytes".

**Byte-level: no.** Under both readings the files an appender may emit are the same set —
§20.3's permissions are the operative text and they are unambiguous. The cost is a tool that
declines work it could have done, not a fork in bytes or verdicts.

**Expense of deciding:** low to read, but it requires cross-reading three sections to
establish that the §20.1 list is not exhaustive, which is why I file it as an OBSERVATION
rather than an ambiguity.

---

### writer-03 — OBSERVATION

**Location.** §20.3 step 4, [R-WRT-04] — the parenthetical on disk-ordinal renumbering.

**Quotation.**

> "... and every other entry byte-identical at its disk-ordinal position (a geometry change
> renumbers ordinals wherever `[R-GEO-06]` moves them)."

**The problem.** The governing clause is right: an entry is re-emitted at *its* disk-ordinal
position, computed under the new declarations. The parenthetical names **a geometry change**
as the trigger, and §11.1's Rationale repeats the pairing ("the layer's whole tile-index
region is re-emitted and disk ordinals renumber wherever `[R-GEO-06]` moves them") in the same
geometry-growth context. But [R-GEO-06] defines the planar disk ordinal as

> "**c · N + s** for a planar layer (§14), where c is the channel's index (§3.1) —
> channel-major grouping"

so the ordinal moves whenever **c** moves — that is, whenever a commit adds, removes, or
reorders a planar layer's channel declarations — with no change to any dimension, extent or
tile extent. §3.1 makes c positional: "a channel's **index** is its 0-based position in that
order, and the order is load-bearing".

And §20.3's own bar permits exactly that commit on a layer that already stores tiles. The bar
prohibits only a declaration change that alters, for a prior-generation stored tile, "the set
of padding positions ... and the content [R-SER-05] fixes there, the decoded size, the byte
offset of any sample within the decoded tile image, or the codec and filter that produced the
stored bytes." For a **planar** layer none of those moves when channels are reordered or
appended: each tile still carries one channel, its decoded size is still P·Bᶜ for *its own*
channel, and its padding content is still *its own* channel's fill. (For an interleaved layer
the same change moves Fᶜ = Σ_{j<c} Bⱼ, so the bar catches it — which is why the gap is planar-
specific and easy to miss.)

**Permitted readings.** Only one, of the *rule*: entries go at their new disk-ordinal
positions whatever moved them. The parenthetical is an under-inclusive gloss, not a competing
rule. I file this because the gloss is the only place the document tells a writer *when* to
recompute ordinals, and a writer that takes it as the trigger set will leave a planar layer's
entries in place across a channel-set change.

**What an implementer does wrong without it.** Two outcomes, and the second is the bad one.
If the reordered channels have different recorded fills and the layer has any padding
position, leaving entries in place makes each affected tile's padding hold the wrong channel's
fill and T4 fires — a verifier catches it, and [R-CNF-05] bars the writer, so nothing escapes.
If the fills coincide, nothing catches it: §21.7 says "the ordinal mappings of `[R-GEO-06]`
and `[R-SER-01]` are satisfied by a structurally valid tile whatever values it carries", so
the file is **conforming** and silently denotes a different reference array — every channel's
data attributed to the wrong channel. That is the format's own named undetectable class, and
this gloss is what steers a writer into it.

**Byte-level: no.** The rule "byte-identical at its **disk-ordinal position**" admits one
reading, so two competent implementations following the rule agree; the divergence comes from
following the parenthetical instead of the rule, which is an error rather than a permitted
reading. Where the mistake produces a detectably nonconforming file (differing fills) both
readings bar it under [R-CNF-05]; where it does not, the two files differ but the caller's
intent — not the format — is what distinguishes them.

**Suggested repair, for triage.** Replace "a geometry change renumbers ordinals" with a
trigger set that names the channel index: e.g. "a change to the grid counts or, in a planar
layer, to the channel set or its declared order renumbers ordinals wherever `[R-GEO-06]` moves
them".

---

## 10. Confidence

**High** that a writer, updater and compactor can be built from this document alone. Every
constant I would have to reproduce byte-for-byte — the front block, the trailer magic, the
sentinel, the all-sentinel segment CRC, Appendix A's trailer CRC, §7.4's two index CRCs, the
CRC-32C parameters and check vector — I recomputed and matched. Every count the document
states about itself — 35/49/26/10 register rows, 120 conditions, 275 instances,
[R-CNT-06]'s nine conditions, [R-CNT-24]'s 48 redefinable bytes, the trailer's 64 with zero
slack, the 128-byte floor and the 128-byte minimum commit increase — I derived independently
and matched.

The trailer change in particular is clean. I went looking for the four failure modes the brief
named — a stale offset or width, a worked example whose arithmetic no longer follows, a rule
that silently depended on the removed field, and a claim true of the old quantity and merely
plausible of the new — and found none. The nine-conditions count in [R-CNF-13], the twelve
reserved bytes in F15 and in Appendix A's annotation, and the derivation of the 128-byte
increase in §9.2's second Note are three independent places where a half-propagated removal
would have shown, and all three are correct.

What I am least sure of is the boundary between §20.3's declaration-change bar and the
operations it silently permits — adding or reordering a planar layer's channels being the
case I found. The bar is stated as an effect test rather than a whitelist ("The test is the
effect on such a tile, and the list names where that effect arises rather than standing on its
own"), which is the right shape, but it means the set of permitted commits is only discoverable
by working the effect test against each candidate, and the one place the document tells a
writer what changes force an index renumbering names a narrower trigger than [R-GEO-06] does.
That is writer-03, and it is the finding I would most want a second reader on.
