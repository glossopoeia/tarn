# Cleanroom round 20 — Adversary transcript

## 0. Disclosure

I read exactly one file: `/Users/robertkleffner/Documents/GitHub/tarn/spec/tarn.md`
(4,369 lines, read in full, in seven `sed -n` slices). I ran `grep`/`rg` against
that file only. I ran local Python (a CRC-32C implementation I wrote from the
parameters in §4.5, plus struct packing) and the local `zstd(1)` binary against
byte strings I generated myself — no file of the repository was an input to
either. I wrote scratch files under my own scratchpad
(`.../scratchpad/work/`) and this transcript. I did not read `docs/`,
`conformance/`, `spec/registry.json`, `PLAN.md`, `AGENTS.md`, any ADR, or any
git history, and I did not list the output directory.

**Context I did not ask for.** Before I began, my runtime placed a project
instruction file and an index of the maintainer's private notes into my context.
The index named several topics by title. I did not open any of the files it
named, and I have deliberately not used any of its contents as evidence; nothing
below traces to it. I disclose its appearance because the brief requires it.

## 1. How I worked

The brief told me where the recent edits are (§7.4, §20.5, §21.6) and warned
that the last two rounds found their survivor outside the changed surface. So I
did three passes:

1. **Cold read of the whole document**, front to back, no skipping. (§1 §2 §3 §4
   §5 §6 §7 §8 §9 §10 §11 §12 §13 §14 §15 §16 §17 §18 §19 §20 §21 §22 §23 §24 +
   Appendices A–H.)
2. **Arithmetic verification of every worked example** the document gives, from
   its own primitives. This is the cheapest way to find out whether the document
   is self-consistent enough that a disagreement I find is probably real rather
   than my misreading.
3. **Construction.** I built the byte sequences the charter asks for, ran the
   reader algorithm of §19 against them by hand, and looked for a file two
   conforming implementations must judge differently.

### 1.1 Verifying the document against itself

I implemented CRC-32C from §4.5's parameters alone (reflected polynomial
0x82F63B78, init 0xFFFFFFFF, final XOR 0xFFFFFFFF) and checked the check vector:

```
crc32c("123456789") = 0xE3069283   ✓ §4.5
crc32c(b"")         = 0x00000000   ✓ §4.5
```

Then, without looking at any conformance vector, I rebuilt each structure the
document works out:

**Appendix A, the 128-byte minimal file.** I assembled front block + 4-byte
directory (CRC of zero bytes = 0x00000000) + 44 zero pad + trailer with
`version_major=1, version_minor=0, flags=0, generation=1, dir_offset=16,
dir_length=4, committed_file_length=128, file_id=0x0123456789ABCDEF`. My
computed trailer CRC over bytes [0,60) came out `0xE00938D2`, stored
`D2 38 09 E0` — byte for byte Appendix A's `[124,128)`. The whole 128 bytes
reproduced.

**§7.4's layer record example.** Four sentinel entries (`FF ×16 00 ×4` each,
80 bytes):

```
crc32c(80 sentinel bytes)      = 0x80A34955  ✓ §7.4 ("stored 55 49 A3 80")
crc32c(bytes 55 49 A3 80)      = 0xC4EE982E  ✓ §7.4 crc_of_crc_array
```

and the packed inline payload came to 81 bytes, matching the annotated dump
offset for offset (name at 0, layout at 4, linearization at 5, codec 7,
filter 9, A at 11, S at 19, A_slab at 27, rank 35, C 36, dimension entry 38,
channel entry 56, index_encoding 68, entry_count 69, crc_of_crc_array 77).
`[R-CNT-17]`'s extent length 4 × 20 + ⌈4/2¹⁶⌉ × 4 = 84 ✓.

**Appendix B's all-sentinel constant.**

```
crc32c(65536 sentinel entries) = 0xEECB3BB2  ✓ §15.4 / Appendix B
```

This matters beyond arithmetic: it tells me `[R-IDX-05]`'s "writers MAY emit
this constant … without computing it" is a pure optimisation licence and can
never fork bytes, because the constant *is* the computed value. I had it on my
attack list as an "overloaded encoding" and it is closed by identity.

**§17.3's byte-shuffle example.** Groups `00 00 80 3F | 00 00 00 40 |
00 00 40 40`, s = 4, n = 3; byte *i* of group *j* to offset i·n + j gives
`00 00 00 | 00 00 00 | 80 00 40 | 3F 40 40` — exactly the document's string.

**§14.2, §14.3, §14.5, §11.2, §11.4, §15.4's two examples.** All check. Spot
worked: (300,700) in grid (4,8) with tile extents (256,256) → tile (1,2),
s = 1·8+2 = 10, in-tile (44,188), ordinal 44·256+188 = 11,452 ✓; planar C=4,
channel 2 → 2·32+10 = 74, entry at region bytes [1480,1500) ✓. §15.4's
1,000,000-entry layer: 16 segments (15 full + 16,960), CRC array 64 bytes,
region 20,000,064 bytes, tile 999,999 at segment-relative byte 339,180, segment
15 at [19,660,800, 20,000,000) — all reproduce. §14.5's (5,5)/(4,4) edge tile:
grid 2×2, tile (1,1) has exactly one real position (4,4) and 15 padding, 32
bytes with values 1–15 = `CD AB` ✓. §14.3's packed plane: fill false → `55 01`,
fill true → `55 FD` ✓.

**§21's instance arithmetic.** I extracted the Instances cell of all 121 register
rows and counted by §21.1's own mechanical rule (semicolon-separated; a cell
reading `—` is one):

```
F: 36 rows / 58 instances
L: 49 rows / 111 instances
T: 26 rows /  63 instances
R: 10 rows /  41 instances
   ------------------------
   121 rows / 273 instances   ✓ §21.8 "121 conditions over 273 instances"
```

I also checked the two axis rules §21.1 states — layout-formula splits and
magnitude directions — against the rows that use them (T3, T14, T22 get 6 each;
T21 and L44 get 3 because "larger than"/"exceeds" bounds the comparison in one
direction; L30 and F17 get 2). They hold everywhere I checked.

This is a document that is arithmetically clean. I record that because it moved
my prior: a numeric or example-level disagreement I thought I found would more
likely be my error than the document's. So I spent my remaining effort on the
seams between actors rather than on the numbers.

### 1.2 Building the thing

I wrote a small builder and produced, from the document alone:

- The 128-byte minimum (reproduced Appendix A byte for byte).
- **The smallest conforming file carrying a layer.** Rank 1, dimension `x` with
  extent 0 and tile extent 1, one interleaved bool channel `c` with fill `00`,
  codec 1, filter 1, no alignment, no slab, index_encoding 1. Grid count
  ⌈0/1⌉ = 0 → N = 0 → addressed-tile count 0 → `entry_count = 0`, extent slot
  (0,0), `crc_of_crc_array = 0` (§7.4, `[R-CNT-17]`, `[R-CNT-23]`, L22, L27).
  Inline payload 73 bytes; record 97; dir_length 101; dir [16,117); pad to the
  64-boundary → trailer at 128; F = 192. Every §6.2 gate and every §19.3 check
  passes. Nothing in this construction made me guess.
- The attack file of §3 below.

Where I had to guess is recorded inline in §2 and §3.

## 2. Attacks that failed, and the sentence that forecloses each

The charter asks for this explicitly, so here it is in full. Each entry is an
attack I actually constructed or worked to concrete bytes before killing it.

**A1 — Two structures claiming the same bytes, deduplicated tiles.** Two
index entries of one layer pointing at one identical extent (the obvious
dedup optimisation a writer will reach for). Killed by `[R-CNT-13]`: "Extents
are owned exactly once … a verifier MUST treat an intra-layer overlap … as
reject-layer", and §15.3's row "two stored extents of the same layer overlap".
Identical ranges overlap. Both verifiers reject the layer. No fork.

**A2 — A stored extent overlapping the directory region.** `[R-CNT-13]` again:
"any overlap across layers or touching another scope's structures as
reject-file", and F33 names `directory region` as an instance. Reader doesn't
detect it (§7.2: "readers are not obligated to detect overlap, which requires
whole-directory knowledge"), verifier rejects the file. That is the documented
reader/verifier seam, not a fork between two verifiers.

**A3 — A structure in the pre-trailer gap.** Index region at [40,64) with the
directory at [16,40) and the trailer at [64,128). Every reader gate passes
(dir_offset + dir_length = 40 ≤ F−64; the extent slot 40+24 = 64 ≤ F−64).
`[R-CNT-05]` forecloses the verifier side: "A verifier MUST treat a structure in
that gap as a validity error at file scope, and counts the rest as slack;
writers zero it by the advice of `[R-CNT-03]` (readers check neither, their
check being the dir-bounds rule of `[R-CNT-06]`)." The parenthetical is what
kills it — it names precisely which actor checks what.

**A4 — A pre-trailer gap longer than one 64-byte pad.** Directory at [16,20),
trailer at [192,256), F = 256, 172 bytes of gap. Foreclosed as a *defined
non-violation* by `[R-CNT-05]`: "a longer gap is conforming, and no conforming
commit produces one", cross-referenced by `[R-CNF-02]`'s conduct list. Both
verifiers certify.

**A5 — The dedup of the all-sentinel segment constant.** See §1.1: the constant
equals the computed CRC, so `[R-IDX-05]`'s licence is inert. Additionally
"Equality with the constant licenses nothing for readers: verification is byte
comparison of computed CRCs, never constant matching."

**A6 — A point request vs a one-position region request at the same
out-of-range coordinate.** §19.4 step 1 makes the point request *fail* and the
region request *succeed returning no samples*. I expected this to be the
classic unnoticed fork; §19.4 pre-empts it in the definition: "a range whose
every interval holds a single position is a region request." Deliberate and
stated.

**A7 — Experimental-range record type with MU = 1, as a top-level record and as
a layer sub-record.** Both are conforming files (`[R-CNF-02]`, §10.3's
prohibition binds conduct). Top-level: `[R-CNT-15]` obliges reject-file — a
conforming file a conforming reader refuses, which §21.6's closing paragraph
registers as a defined capability refusal. Sub-record: `[R-CNT-18]`'s
"an unknown sub-record type with MU = 1 is reject-layer, and where the file is
otherwise conforming a reader MUST NOT reject the file for it". I attacked the
apparent gap between that MUST NOT and §2.3's unqualified carve-out ("carrying
no record of a type it does not implement with MUST_UNDERSTAND = 1"), on the
theory that §2.3 licenses a reader to refuse the file. It does not: §2.3's
participial phrase *narrows an acceptance duty*, it grants no permission to
reject, and `[R-CNT-18]`'s explicit MUST NOT then bites. The carve-out is in
fact *necessary* — without it, reject-layer on a conforming file would itself
breach the duty. Closed, and closed correctly.

**A8 — Every combination of the record flag bits in every position.** MU=0/PE=0,
MU=0/PE=1, MU=1/PE=0, MU=1/PE=1 × {reserved range, experimental range,
registered type} × {top-level, sub-record}. Every cell lands on a stated rule:
`[R-CNT-12]` (MU=1/PE=0 read as PE=1; F25, L46), `[R-CNT-15]` (F35 reader /
F36 verifier; L24 / L25), `[R-CNT-22]` (F28, L49), §7.3's fixed flags, §20.4's
table. The reserved-flag-bits case (F26, L47) is verifier-only with the reader
obliged to ignore. No cell is unassigned and no two rows collide.

**A9 — The register contradicting a rule.** I checked the rows I could
independently derive. Where I found looseness — §7.3's Scope column giving the
layer record "file (container for layer scope)" while `[R-CNT-13]` says "the
layer for a layer record" — §21.1 has already decided it ("where a row and the
rule it cites diverge, the rule governs") and the register agrees with the rule
(L46, L47, L49 all sit at layer scope). Per the brief's warning about the
dominant over-claim, I am not reporting this.

**A10 — Boundary values on the index arithmetic.** entry_count = 0 (no region,
slot (0,0), crc 0); = 1; = 65,536 (one full segment, region 1,310,724 bytes);
= 65,537 (two segments, second covering one entry); = 2³² (the §21.9 guarantee —
region 85,899,608,064 bytes, still under 2⁶³−1, CRC array 256 KiB exactly as
§21.9's Note computes). And the value that overflows: a rank-1 layer with
E = T = 1, extent 2⁶³−1, tile extent 1 gives entry_count = 2⁶³−1, whose region
length 20·(2⁶³−1) exceeds the domain — L2 lists exactly that product
("entry_count × 20 + ⌈entry_count/2¹⁶⌉ × 4"), so it is reject-layer. Every
boundary lands on a row.

**A11 — The overflow set.** I enumerated every product a reader must form
(N, P, N·P, C·N, P·Q, P·Bᶜ, V = P·C, the max disk ordinal (C−1)N + (N−1), the
index-region length, Q, Fᶜ, ⌈P/8⌉, the value offset (k div C)·Q + F_{k mod C})
and checked each is either in L2's list or dominated by something that is. L2's
parentheticals are correct: C·N ≥ (C−1)N + (N−1) since C·N − 1 ≥ that, and
P·Q ≥ P·C since Q = ΣBᵢ ≥ C. Nothing escapes `[R-ENC-04]`.

**A12 — The legal monster: extent 2⁶³−1, tile extent 2⁶³−1, one bool channel,
one sentinel tile.** N = 1, P = 2⁶³−1, decoded size 2⁶³−1 — a tile no machine can
hold, in a file of a few hundred bytes. Conforming (codec must not be 4:
`[R-COD-07]`'s cap, L44). A reader may decline the layer under `[R-ERR-04]`
because the declared decoded size exceeds §21.9's 256 MiB guarantee, or may
serve the sentinel as fill at zero cost. Both licensed by the same sentence
("A file exceeding any of these remains conforming, and a reader MAY decline
it — at the whole file, or at the narrowest scope whose declarations exceed
what it can serve, a layer or a tile"). Defined divergence, not a defect.

**A13 — A degenerate empty layer under codec 4.** §17.2's Note is explicit:
"a layer that addresses none — any dimension extent 0 … — satisfies it whatever
its tile shape declares, and codec 4 is conforming there", with the
non-durability of the escape and the contrast to `[R-ENC-04]` (which "carries no
such quantifier") both spelled out, and §20.3 step 4 naming L44 as the bound a
later growth must satisfy. This is the exact "two features each individually
well-specified" interaction the charter names, and it is closed in three places.

**A14 — Compaction over a record the compactor cannot read.** MU=1 unimplemented,
top-level or sub-record: `[R-WRT-06]` "A compactor MUST refuse to compact a file
carrying any record whose type it does not implement with MU = 1". MU=0
unimplemented with an extent covered by no checksum (§8.1's last row):
relocated unread under `[R-WRT-08]`, and `[R-SEC-04]` states the residue rather
than defending it. A structurally-malformed index entry: §20.5 walks it
explicitly — "regenerating the region cannot proceed without meeting it … then
obliges refusal" — and contrasts it with §20.3 step 2's appender, which carries
the same entry forward byte-identically. That asymmetry is stated, not latent.

**A15 — A compactor clearing a slab declaration.** `[R-SLB-04]` offers any
updater "re-establish … or clear the declaration". If a compactor could clear
it, its output would differ from a compactor that re-establishes, on a
conforming input. Foreclosed by `[R-WRT-07]`'s closed exception list: byte-
identical re-emission "except that relocation re-points extent slots,
regenerates each relocated tile-index region …, and updates the layer-record
fields covering a regenerated region (crc_of_crc_array)". Clearing a slab field
is not in the list, and the same sentence says the compactor places structures
where "every declared layout invariant permits". Closed, though only by the
exhaustiveness of a list — the tightest of the closures I found.

**A16 — The tile-side zstd window.** A tile whose frame declares a window above
§21.9's 8 MiB guarantee but not above its own decoded size. Foreclosed by
§17.2's own sentence: "a wider window is conforming and merely permits a
conforming reader to decline the tile or the layer on resource grounds
(`[R-ERR-04]`)", plus §2.3's cannot-establish ground "when it declines a layer's
or a tile's decode on resource grounds". This one is *closed for tiles* — which
is what made me look at whether it is closed for user metadata. It is not. See
§3.

**A17 — The 1e400 fork in user metadata.** Whether a reader using "a wider
representation" (§18.2) may treat a magnitude binary64 cannot hold as finite.
Foreclosed by the next clause pinning the test to the binary64 interpretation:
"A document is unreadable if it contains a number whose **binary64
interpretation** is not finite". The "MAY use a wider representation" governs
precision retention, not the finiteness test.

**A18 — `[R-SER-08]`'s resolved bool byte.** A nonconforming interleaved bool
byte 0x02. `[R-TYP-04]`'s "readers MUST NOT alter a value's encoded bytes" looks
like it should collide with `[R-SER-08]`'s "MUST report … every other byte as
true". `[R-TYP-04]` names the collision and yields: "the one case where a reader
resolves a byte to a value rather than passing it through arises only in a
nonconforming file, and `[R-SER-08]` states it". Closed by construction, and
§21.1 flags T2/T4 as jointly covering the rule.

**A19 — Zero-length and out-of-file structures.** length = 0 non-sentinel (T10),
offset < 16 (T8, F31, L16), extent past F−64 (T9, F32, L17), sum overflow (T12,
F3, L2), one-half-zero slot (F30, L15), extent exactly ending at F−64 (legal —
the rows all test `>`). Every one lands on a row, at the right tier.

**A20 — A file whose 128-byte floor is unreachable.** F = 64 (trailer only):
`[R-CNT-06]`'s dir_offset ≥ 16 and dir_offset + dir_length ≤ F−64 = 0 are jointly
unsatisfiable, so F5 is subsumed by the trailer gates. Consistent, and §21.2's
preamble already reasons about which rows survive a foreign version_major.

**A21 — A user-metadata extent of exactly 5 bytes** (the stated minimum). Under
encoding 1 the document is one byte, which cannot be a JSON object — so the
minimum extent length is reachable only as R7. That is a hard bound with no
conforming instance, but `[R-ERR-05]`/§24 ask for a vector "at its stated bound",
not for a conforming one, and R7 is the row. Not a defect.

**A22 — §20.4's MU = 0 / PE = 0 drop conditions.** I tried to build a commit
whose only effect is a drop (barred: "a commit whose only effect would be the
drop MUST retain it"), a drop justified by another drop (barred: "Dropping the
record, or dropping another record in the same commit, is not itself such a
change"), and a drop justified by a tile supersede (permitted, and the text
walks the chain: supersede → index re-placed → extent slot moves → layer record
modified → that is such a change). All three are decided in the table cell
itself.

**A23 — The `[R-CNF-02]` conduct enumeration.** "§6.3's flags = 0 against a set
ignore-lane bit and §6.2's pre-trailer gap … are the cases this text states."
I tried to falsify it with §10.3's experimental-value prohibition, §18.3's
`tarn.` key rule, and §18.4's standardized-key placement. The first two are
already caught by the *preceding* sentence ("where a value is published, or
which registry version a writer targets (§10.3, §18.3)"); the third is a SHOULD
and outside the register by `[R-CNF-12]`. The enumeration survives.

## 3. The one that survived

### 3.1 The construction

**A conforming file whose user-metadata document is stored under encoding 2 in
a Zstandard frame that declares a Window_Size above §21.9's 8 MiB guarantee.**

§18.2 defines encoding 2 as "exactly one RFC 8878 compressed frame occupying
the extent's bytes before its terminal CRC, under the frame constraints of
`[R-COD-06]` that do not reference a tile: the frame magic; no skippable frame
and no second frame; no nonzero dictionary ID; no content-checksum flag", and
then says:

> The constraints §17.2 states against a tile's declared decoded size do not
> apply, because a document has no declared size — a reader instead decodes with
> a bound of its own choosing, no smaller than §21.9's user-metadata guarantee,
> and a document exceeding that bound is ignore-record like any other it cannot
> read.

§17.2's window rule *is* a constraint against the tile's declared decoded size
("MUST NOT declare a window size exceeding the tile's decoded size"), so it does
not carry over. A metadata frame's declared window is therefore unconstrained by
this specification. Meanwhile §21.9's table guarantees a conforming reader only:

| Quantity | A conforming reader MUST accept at least |
|---|---|
| zstd frame `Window_Size` | 8 MiB |

I hand-built the frame from RFC 8878's header layout rather than from an
encoder, so that the only thing distinguishing my two files is one byte:

```
Frame_Header_Descriptor = 0x00   (no FCS field, Single_Segment_flag = 0,
                                  no content checksum, no dictionary ID)
Window_Descriptor       = 0xA0   (Exponent 20 → windowLog 30, Mantissa 0
                                  → Window_Size = 1 GiB)
Block_Header            = 11 00 00  (last block, raw type, size 2)
Block content           = 7B 7D     ("{}")

frame = 28 B5 2F FD 00 A0 11 00 00 7B 7D            (11 bytes)
extent = frame ++ crc32c(frame)                      (15 bytes)
```

The complete 128-byte file, offsets as built:

```
00000000: 8954 4152 4e0d 0a1a 0000 0000 0000 0000   front block  [0,16)
00000010: 28b5 2ffd 00a0 1100 007b 7db1 1964 5202   UM extent    [16,31)
00000020: 0002 0001 0000 0010 0000 0000 0000 000f   directory    [31,60)
00000030: 0000 0000 0000 0002 9891 4dd5 0000 0000   pad (slack)  [60,64)
00000040: 8a4e 5241 540d 0a1a 0100 0000 0000 0000   trailer      [64,128)
00000050: 0100 0000 0000 0000 1f00 0000 0000 0000
00000060: 1d00 0000 0000 0000 8000 0000 0000 0000
00000070: 8877 6655 4433 2211 0000 0000 b548 7796
```

Reading it as §19.1 requires:

- Front block equals the constant (`[R-CNT-04]`, F1/F6). ✓
- Trailer magic `8A 4E 52 41 54 0D 0A 1A`; trailer CRC over [0,60) verifies;
  version_major = 1; flags = 0; generation = 1; dir_offset = 31 ≥ 16;
  dir_length = 29 ≥ 4; 31 + 29 = 60 ≤ F − 64 = 64; committed_file_length =
  128 = the file size and a multiple of 64; file_id ≠ 0; reserved zero.
  Every gate of `[R-CNT-06]` in §6.2's order. ✓
- Directory CRC over the 25-byte record sequence verifies (`[R-CNT-11]`). ✓
- One record: type 0x0002, flags 0x0002 — MU = 0, PE = 1, exactly the values
  §7.3's registry fixes, so no F28. inline_length = 1 (`[R-MTA-03]`, F23);
  extent slot (16, 15), offset ≥ 16, 16 + 15 = 31 ≤ F − 64, extent_length ≥ 5
  (`[R-CNT-25]`, F21/F22). Multiplicity: one (`[R-CNT-14]`, F34). ✓
- Encoding byte = 2 — an *assigned* encoding, so not §21.6's experimental-range
  non-violation and not R1. ✓
- Coverage (`[R-CNT-02]`, `[R-LIF-08]`): claimants are the front block [0,16),
  the extent [16,31), the directory [31,60), the trailer [64,128). Disjoint;
  the two middle claimants lie inside [16, F−64) = [16,64). Slack total 4 bytes,
  the pre-trailer pad. No structure lies between directory end and trailer
  (`[R-CNT-05]`, F7). ✓
- Extent terminal CRC verifies (`[R-CNT-20]`, R2). ✓
- The frame satisfies every §18.2 encoding-2 constraint: magic present, one
  frame, no skippable frame, dictionary-ID flag 0, content-checksum flag 0, no
  bytes after the frame before the terminal CRC (R4's six conditions). ✓
- The document is `{}` — a JSON object, no BOM, no numbers, no keys, no
  duplicate keys, well-formed UTF-8, and vacuously sorted (`[R-MTA-04]`,
  `[R-MTA-05]`; R5–R10 and F27 all clean). ✓

I also built the byte-identical file with `Window_Descriptor = 0x68`
(Exponent 13 → windowLog 23 → Window_Size = 8 MiB). The two files differ at
five bytes: offset 0x15 (the window descriptor) and the four extent-CRC bytes
that follow from it.

### 3.2 The two verdicts

Both files are conforming under §18.2 as written. I then ran stock `zstd(1)`
against the two frames, because I wanted a real implementation's behaviour
rather than my reading of RFC 8878:

```
$ zstd -d -c meta_window_8mib.zst
{}                                             # exit 0

$ zstd -d -c --long=23 meta_window_1gib.zst    # --long=23 == exactly 8 MiB
meta_window_1gib.zst : Decoding error (36) : Frame requires too much memory
meta_window_1gib.zst : Window size larger than maximum : 1073741824 > 8388608

$ zstd -d -c --memory=1024MB meta_window_1gib.zst
{}                                             # exit 0
```

So: an implementation sitting exactly on §21.9's guaranteed floor reports the
frame as a **decoding error**, and one with a larger allowance decodes it. That
is not a hypothetical; it is the default behaviour of the reference tool.

**Verifier A** implements a zstd decoder at the 8 MiB window §21.9 guarantees —
which is all this specification obliges of it, and which §21.9's own Note calls
"the decoder window support RFC 8878 itself recommends". It attempts the
document, fails, and reads §21.5's register row R3:

> R3 | A user-metadata document's stored bytes fail to decode under its declared
> assigned encoding — under an experimental-range one this specification defines
> no decoding and §21.6 governs (`[R-MTA-10]`); encoding 0 and a reserved value
> are unassigned too and R1 registers both | … | reader | extent use |
> `[R-CNT-25]`

The encoding is assigned (2). The stored bytes failed to decode. Verifier A has
established a violation. §2.3 then forces its hand: "An established violation
takes priority: a verifier that has established any violation reports
*nonconforming*, however many requirements it was unable to check". Verifier A
reports **nonconforming**.

Verifier A's reading is not strained. §21.5's preamble enumerates, exhaustively
and in one sentence, the only two ways a document's unreadability escapes being
a violation:

> every way its document can be unreadable takes this outcome, whatever the
> containing scope — as a violation in the rows below, **except at an
> experimental-range encoding**, where no document rule attaches and §21.6
> records the defined non-violation (`[R-MTA-10]`), and **except where a reader
> or verifier declines the decode on the size bound**, which `[R-MTA-09]` makes
> that actor's capability and not a fact about the file.

Neither exception is a window. And `[R-MTA-09]`'s carve-out is written tightly
around the size bound and nothing else:

> A **verifier** that declines to decode a document **on the bound above**
> cannot establish that document's conformance and MUST NOT certify the file …
> the bound is that verifier's capability and not a limit on validity
> (`[R-CNF-10]`), so the decline is not a finding that the file is nonconforming
> and a verifier MUST NOT report it as one.

"The bound above" is the document-size bound. Verifier A did not decline on it —
it declined on a window. The existence of that explicit carve-out, in a document
this careful, is itself evidence that without one an inability to decode reads
as R3. That is the strongest form of Verifier A's argument.

**Verifier B** implements a 256 MiB window (or simply calls `ZSTD_decompress`
with a large allowance). It decodes `{}`, finds no violation anywhere else in
the 128 bytes, and reports **conforming**. It certifies.

Same 128 bytes. One certificate, one finding of nonconformance. Both defensible.

**Verifier C** is worth naming because it is the third defensible reading and
shows the ambiguity is genuinely three-way. §2.3's cannot-establish list is
introduced with "as when", so it is illustrative rather than closed; Verifier C
therefore books the window failure as a capability ground and reports **cannot
establish**. That verdict is neither A's nor B's, and §2.3 makes it explicitly
"not a finding that the file is nonconforming" — so C will not certify where B
does.

### 3.3 Why the tile side does not have this problem, and the metadata side does

I want to be precise about the asymmetry, because it is what makes this a defect
rather than a place where I simply did not look hard enough.

For a **tile**, three sentences close the loop:

1. §17.2: "Writers SHOULD keep the declared window within §21.9's 8 MiB
   `Window_Size` guarantee even for a larger tile; a wider window is conforming
   and merely permits a conforming reader to decline the tile or the layer on
   resource grounds (`[R-ERR-04]`)."
2. §2.3 lists as a cannot-establish ground "when it declines a layer's or a
   tile's decode on resource grounds and so cannot check §14's decoded-content
   obligations (`[R-ERR-04]`, `[R-SER-05]`, `[R-SER-08]`)".
3. `[R-ERR-04]`: "a refusal on resource grounds MUST be reported as a resource
   limit and not as a validity error".

So a verifier meeting a 200 MiB-window tile has a named door: decline, cannot
establish, do not report nonconforming.

For a **user-metadata document**, sentence 1 has no counterpart — §18.2
explicitly *removes* the window constraint rather than replacing it with a
decline licence. Sentence 2's list names "a layer's or a tile's decode" and, via
`[R-MTA-09]`, the document *size* bound; it does not name a document's frame
parameters. `[R-ERR-04]`'s scope list is "at the whole file, or at the narrowest
scope whose declarations exceed what it can serve, **a layer or a tile**" — a
record is not among them, and `[R-MTA-09]`'s Note explains why for the size case
("a document having no declared size and so no narrower scope whose declarations
that rule can measure") — but a *window* is a declared size, present in the
frame header, so that explanation does not reach it either.

Every door that exists on the tile side is missing or mis-fitted on the metadata
side, and R3 sits behind the gap.

### 3.4 What an implementer does wrong without this resolved

Concretely: a verifier author who wires `ZSTD_decompress` straight through and
maps its error return to R3 — the most natural implementation, and the one the
`zstd -d` transcript above shows the reference tool leading you toward — will
report perfectly good published files as nonconforming, on a byte the writer was
entitled to emit and that this specification nowhere told the writer to avoid.
A writer, correspondingly, has no sentence telling it to keep its metadata
window inside 8 MiB (§17.2's SHOULD is scoped to tiles), so a large-document
writer using a high compression level will emit windows above 8 MiB as a matter
of course.

The reading I would pick, and would expect the project to pick, is the one that
matches the tile side: extend §17.2's SHOULD and the decline licence to encoding
2, and add the window to `[R-MTA-09]`'s capability carve-out and §21.5's
preamble, so that a verifier at the guaranteed floor reports *cannot establish*
and never *nonconforming*. But that is a repair, not a reading the current text
compels, and Verifier A can defend itself from §21.5's preamble as it stands.

### 3.5 Byte-level?

Yes, on the accept/reject half of the test rather than the emission half.
No byte a writer may emit changes — both my files are emittable under either
reading. What changes is a verdict on a fixed byte sequence: Verifier A must
report *nonconforming*, Verifier B certifies *conforming*. §2.3 makes those
verdicts a normatively defined observable of a conforming verifier, and §24
makes them a corpus expectation ("whether the file is **conforming**"). A
conformance vector built from this file cannot be given an expectation without
resolving the question, which is `[R-VEC-02]`'s own test for a finding against
the document: "A vector whose expectation cannot be stated in those terms is
testing something this specification has not defined, which makes it a finding
against this document rather than a vector."

I have graded it byte-level and I am aware of the brief's warning. My check
against that warning: this does not turn on a SHOULD (§17.2's SHOULD is the
sentence that is *missing* here, not the one being disputed); it does not turn
on a §21 row contradicting its rule (R3 and `[R-CNT-25]` agree — the question is
whether R3's antecedent is satisfied); and it is not important-therefore-
byte-level, it is a straight disagreement between two verifiers about whether a
named register row fired.

## 4. Two smaller findings

### 4.1 The metadata decode bound's floor carries no BCP 14 keyword

`[R-MTA-09]`, §18.2:

> a reader instead decodes with a bound of its own choosing, no smaller than
> §21.9's user-metadata guarantee, and a document exceeding that bound is
> ignore-record like any other it cannot read.

"no smaller than §21.9's user-metadata guarantee" is the only place the 16 MiB
floor is imposed on a reader's *decode* behaviour, and it carries no capitalised
keyword. The candidate that would supply one is `[R-ERR-03]`/`[R-CNF-10]`:
"a conforming reader MUST **accept** any conforming file whose quantities lie
within these bounds". But a reader with a 1 KiB metadata bound has not refused
the file — it has taken ignore-record for the record, which is a *defined
outcome* under `[R-CNT-25]`'s quarantine, not a refusal. It accepts the file and
serves every sample. On that reading nothing in the document makes it a
nonconforming reader, and §21.9's 16 MiB row guarantees nothing at all.

Two readings:

- **(a)** The keyword-free clause binds as normative declarative text
  (`[R-CNF-01]` makes all such text normative), so a reader whose bound is below
  16 MiB is not a conforming reader.
- **(b)** Per §2.1, only capitalised keywords carry BCP 14 force; the floor is
  therefore descriptive, and the only binding obligation is `[R-ERR-03]`'s
  "accept", which ignore-record satisfies. Any bound is conforming.

I pick (a), because (b) makes the §21.9 row dead and because every other §21.9
row is enforced through a MUST that clearly reaches the behaviour it guarantees.
But (b) is the reading the project's own stated discriminator produces, and it
is what an implementer optimising memory will reach for.

What it costs: under (b), Verifier D with a 1 KiB bound reports *cannot
establish* on almost every file carrying user metadata, and never certifies one,
while Verifier E at 16 MiB certifies. Under (a), Verifier D is not a conforming
verifier at all. I am **not** grading this byte-level: *cannot establish* is
explicitly "not a finding that the file is nonconforming", no byte changes, and
no accept/reject verdict moves — what moves is which implementations count as
conforming. That is a real cost to an implementer and a real gap in the
guarantee, but it is not the fork §3 is.

### 4.2 §20.4's preservation table carries no requirement identifier

The block running from "Persistence governs every record type; only the
authoritative source of the flags differs." through "That is not compaction,
which carries every layer of its input forward (§20.5)." — which contains the
three-row updater-obligation table and every MU/PE preservation and drop rule —
has no trailing `[R-…]` marker. `[R-WRT-05]` closes the paragraph above it;
`[R-WRT-08]` opens the paragraph below it. The table's cells carry capitalised
keywords of their own ("MUST NOT modify the scope the record governs", "An
appender MUST NOT drop it except…", "a commit whose only effect would be the
drop MUST retain it", "A compactor MAY drop it"), so they bind under §2.1
regardless; and `[R-CNF-06]` gives the block force by reference ("MUST honor the
preservation obligations of §20.4"), as does §2.4's preserve-verbatim row
("§20.4's table states the cases: its MU = 1 and MU = 0 / PE = 1 rows").

But §2.2 and the document's own preamble promise otherwise — "Normative
requirements carry stable identifiers like `[R-IDX-03]`, and test vectors cite
those identifiers rather than prose positions" — and this is the largest block
of MUST-bearing normative text I found with no identifier of its own. Nothing
about the bytes changes; the cost is that an ADR, a vector, or a reviewer who
wants to cite "an appender MUST NOT drop it except in a commit that
independently changes the scope" has only a prose position to cite, which is
precisely what §2.2 exists to avoid. Not byte-level, and I flag it as the
thinnest of my three.

## 5. Confidence and what I could not determine

I could build every file the charter's list names, from this document alone,
without consulting anything else — the minimal file, the minimal file with a
layer, the empty layer, the all-sentinel layer, the metadata-only file — and
where I had to compute (CRCs, grid arithmetic, index-region lengths, shuffle
offsets, zstd frame headers) the document gave me enough to get bytes that
reproduce its own worked examples exactly. That is a strong result for a
document-only artifact and I want it on the record alongside the findings.

The places I had to guess, and did not resolve from the text:

1. **The metadata window question of §3** — I guessed that Verifier B's reading
   is intended, and reported the guess rather than acting on it.
2. **The metadata decode-bound floor of §4.1** — I guessed (a).
3. **The exact ordering inside §19.4 step 6** — whether `[R-SER-07]`'s length
   test applies to the codec's output or to the post-filter image. It cannot
   matter, because the filter preserves length (§17.3: "Length is unchanged")
   and both orders reject the tile, so I did not report it. I record it because
   an implementer will notice it and should be told it is harmless.
4. **Whether a compactor may carry forward a *known* ignore-lane bit** — §6.3
   and §20.5 both bind only "unknown" ones. Under this text no conforming
   implementation knows any ignore-lane bit, so the case is unreachable in
   format major 1 and I did not report it; it becomes live the first time a
   minor version defines one.

Confidence that an implementation built from this text alone would interoperate:
**high**, with the metadata-window verdict as the one place two conformant
verifiers will disagree in the field.
