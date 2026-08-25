# Round 24 — Verifier implementer — working transcript

Charter: implement, on paper but concretely, a **conforming verifier** — the tool
that certifies a file rather than reads it.

Access: I read exactly one file, `/Users/robertkleffner/Documents/GitHub/tarn/spec/tarn.md`,
in five `Read` calls covering lines 1–4445. I ran local Python (CRC arithmetic, file
construction, a verifier) and two `grep`s against that same file. I opened no ADR, no
`conformance/` artifact, no `registry.json`, no git history, and did not list the
round-24 output directory.

**Contamination to disclose.** Material appeared in my context before I began: a
project instruction file pointing at `AGENTS.md`, and an index of the maintainer's
auto-memory naming several memory files (one of whose titles mentions §21.9). I did
not open any of them and did not act on their contents. Separately and more seriously:
partway through the run a scratch file I had written (`.../scratchpad/work/crc.py`) was
**overwritten by another process** writing into the shared scratchpad — the replacement
was a different agent's CRC helper, and it printed expected-value assertions. I caught
this because my verifier run emitted output my code does not produce. I did not read
that file's source beyond the five lines I dumped to establish provenance. All
arithmetic reported below was then **re-derived from scratch** in a uniquely named
private directory (`scratchpad/vfr-iso-9271/`) using a CRC implementation I wrote from
§4.5's parameters alone, and every constant reproduced identically to my pre-clobber
run. The clobber affected only the `verify.py` run's stray stdout, not any conclusion.

---

## 1. The certification procedure, as an ordered algorithm

I derived this from §2.3 (`[R-CNF-11]`), §2.4 (`[R-CNF-12]`), §6.1–§6.2, §7.1–§7.2,
§8.2, §9.7, §17.4, §18.2, §19.1–§19.4, §21.1 and Appendix H, then implemented it.

**Verdict vocabulary** (§2.3): *conforming*, *nonconforming*, *cannot establish*.
Three further report channels, none of which is a verdict:

| channel | rule | trigger |
|---|---|---|
| per-requirement *unable to check* | `[R-CNF-11]` | any requirement not checkable on a **capability or resource** ground; owed "whichever of the three verdicts it reports" |
| *unexamined* scope | `[R-CNF-11]` | only for a verifier that elects to stop at the first violation |
| slack total (or **partial** total) | `[R-CNT-21]`, `[R-LIF-08]` | any traversal that reaches a live state |
| ignored-record report | `[R-MTA-10]` | a user-metadata record under an encoding this text does not assign |
| advisory | `[R-CNF-12]` | a SHOULD deviation the verifier *observes*; never hunted for |
| resource-limit report | `[R-ERR-04]` | any refusal on §21.9 grounds, reported as a limit and never as corruption |

**Verdict logic**, resolved from §2.3: an established violation wins over everything
(*nonconforming*, "however many requirements it was unable to check"); *cannot
establish* is available "only to a traversal that established no violation"; and
*conforming* requires both no violation **and** nothing left unchecked, because
`[R-COD-11]` and `[R-MTA-09]` each say the inability "MUST NOT certify the file" and
§2.3 says "a verifier MUST NOT certify a file it reports that way". So:

```
if any established violation      -> NONCONFORMING
elif any unchecked requirement    -> CANNOT ESTABLISH
else                              -> CONFORMING
```

I checked that *conforming* + *unable-to-check* is unreachable: every resource decline
I could construct leaves at least T3/T24/T25 unchecked for a tile, or the §18.2 document
rules unchecked for a document. §2.3's "whichever of the three verdicts it reports" is
therefore over-general but harmless.

**Ordered algorithm.** Steps are ordered by dependency, and two of the orderings are
normatively fixed rather than derived:

0. **Front signature block, by byte equality, first.** `[R-CNT-04]` says a reader
   holding [0,16) resident "MUST verify the full block by byte equality **before other
   processing**". §2.3 gives the verifier no residency exemption; F6's condition says so
   ("a verifier holds no such exemption (§2.3)") and Appendix H repeats it. So a verifier
   makes those bytes resident and checks them before anything else. Rows: F6, F1's
   front-block instance. Mismatch → reject-file.
1. **Minimum length**, `[R-CNT-27]` → F5.
2. **Trailer, in §6.2's fixed order**: magic (F8, F1's trailer-magic instance) → trailer
   CRC (F14) → version gate (F18; foreign major → *cannot establish*, §2.3). Only these
   three touch fields `[R-CNT-24]` fixes across majors, which is exactly §21.2's
   preamble's claim, and I checked it: `flags` sits at trailer offset 12, inside the 48
   bytes a future major MAY redefine, so F19 correctly is **not** among the four rows that
   reach a foreign-major file.
3. **Remaining trailer gates as a set** (`[R-CNT-06]`): F19, F17, F13, F9, F16, F10, F11,
   F12, F15, plus F2/F3 for the u64 domain. §6.2 validates them together and `[R-VEC-02]`
   admits that a file failing two "attributes to neither alone".
4. **Directory region CRC** before any other use (`[R-CNT-11]`) → F20.
5. **Top-level record walk** (`[R-CNT-12]`/`-13`/`-14`/`-15`, `[R-MTA-03]`) → F24, F25,
   F26, F28, F29, F30–F36, F21–F23, F4.
6. **Per layer**, §19.3's full validation (`[R-RDR-03]`) → the L-rows; then the index
   chain (`[R-IDX-04]`, L37/L38); then §15.3 entry classification (T6–T12); then the
   §16 invariants (L40, L41, L42).
7. **Decode every stored tile.** §9.7 is categorical: "A verifier decodes every stored
   tile, whatever content obligations §14 places on the layer: §21.4's codec rows are
   file-conformance violations, and a verifier MUST NOT certify past a violation it has
   not looked for." → T1, T3, T14, T17–T25, then the content rows T2, T4, T5, T26.
8. **Every user-metadata document** (§18.2) → R1–R10, or a decline → *cannot establish*.
9. **Coverage walk**, §9.7 → F7, F33, L18, and the slack total.

**What the verifier reports when a check cannot be run.** §2.3 gives an open list
("as when …") of capability/resource grounds: a foreign format major; an MU = 1 record of
an unimplemented type; a codec or filter it cannot execute (`[R-COD-11]`); a layer's or
tile's decode declined on resource grounds (`[R-ERR-04]`, `[R-SER-05]`, `[R-SER-08]`);
a user-metadata document it declines to decode (`[R-MTA-09]`). Expressly *not* such a
ground: a document under an encoding this text does not assign, because "no content rule
attaches there, so nothing is left unchecked" (`[R-MTA-10]`, §17.4's closing sentence).

I note that `[R-COD-11]`'s ground is nearly unreachable for a *conforming* verifier:
`[R-CNF-03]` makes all four codecs and both filters core, so a verifier that cannot
execute one is not a conforming reader, and §17.4 says so — "For a conforming reader
that position arises only at a reserved or experimental value … it rejects the layer".
The reachable neighbour is the resource path: a zstd frame declaring a window above what
the verifier supports (§21.9 floor 8 MiB) → decline the tile → *cannot establish*.

---

## 2. Checksum obligations — what I could reproduce

§4.5 fixes CRC-32C (poly 0x1EDC6F41, reflected in/out, init 0xFFFFFFFF, final XOR
0xFFFFFFFF, stored little-endian). I implemented it from those parameters alone
(reflected table 0x82F63B78) and recomputed **every constant this document states that
is locally computable**:

| constant | §  | spec value | I computed | ✓ |
|---|---|---|---|---|
| CRC-32C(`"123456789"`) | §4.5, App. B | `0xE3069283` (`83 92 06 E3`) | `0xE3069283` | ✓ |
| CRC-32C(zero bytes) | §4.5, §7.1, App. A | `0x00000000` | `0x00000000` | ✓ |
| CRC of 4 sentinel entries (80 B) | §7.4 example | `0x80A34955`, stored `55 49 A3 80` | `0x80A34955` | ✓ |
| crc_of_crc_array over `55 49 A3 80` | §7.4 example | `0xC4EE982E`, stored `2E 98 EE C4` | `0xC4EE982E` | ✓ |
| CRC of a **full** all-sentinel segment (2¹⁶ entries) | §15.4, App. B | `0xEECB3BB2` | `0xEECB3BB2` | ✓ |
| Appendix A trailer CRC over [0,60) | App. A | `0xE00938D2`, stored `D2 38 09 E0` | `0xE00938D2` | ✓ |

Six for six. I could **not** reproduce anything requiring an external codec
(no deflate/zstd/lz4 stream constants are stated, so nothing was owed), and no other
numeric constant in the document is a checksum.

I also rebuilt §7.4's worked layer-record payload byte for byte. Every annotated offset
matched, the payload came out at **81 bytes** with no residue (name 4 + nine scalars 34 +
dimension entry 18 + channel entry 12 + trailing fixed 13 = 81), §12.3's channel entry
came out as the stated twelve bytes `04 74 65 6D 70 0C 00 04 00 00 C0 7F`, and
`[R-CNT-17]`'s arithmetic gave extent_length = 4·20 + ⌈4/2¹⁶⌉·4 = **84**, as stated.
Appendix A's 128-byte file decoded field-for-field to the stated table.

**Is every live structure covered by a checksum?** No — and the document says so, in
three consistent places. §5.2's live-state classes are: front block; stored-tile extent;
record extent; directory; trailer. §8.1's map covers all of them **except** "Extent of a
record of a type this specification has not assigned | none — the bytes are opaque
(§7.2)". §4.5 restates it and §22.3 names it as a residue. Because an experimental-range
MU = 0 record is a *conforming* file (§21.6), a conforming file can carry live bytes
under no checksum at all. I confirmed §4.5's interior/terminal taxonomy closes: the three
terminal fields (trailer CRC, directory CRC, user-metadata extent CRC) are covered by
nothing; the three interior fields (segment CRC array ← crc_of_crc_array; entry crc ←
its segment CRC; crc_of_crc_array ← directory CRC) are each comparison-verified **and**
covered exactly once. That closure is what lets the coverage walk act on index offsets:
every integer the walk consumes is under a link the walk has already verified, so
`[R-ENC-05]` is satisfied without a special rule.

That residue is where finding **verifier-03** lands.

---

## 3. The coverage walk on a concrete file

I built a two-layer file from scratch (`gen1.tarn`, F = 2176) rather than reasoning
abstractly, so the arithmetic is checkable.

- **Layer A** — interleaved, rank 2, extents (5,5), tile extents (4,4) → G = (2,2),
  N = 4, P = 16. One `uint16` channel `v`, fill `0xABCD`. Codec 1, filter 1,
  **alignment A = 512**. Decoded size P·Q = 32. Tiles 0, 1, 3 stored; tile 2 sentinel.
  This is §14.5's worked geometry: tile (1,1) has one real position and fifteen padding
  positions, each of which I fill-encoded as `CD AB`.
- **Layer B** — planar, rank 1, extent 10, tile extent 5 → N = 2, P = 5. Two channels,
  `m` (bool, fill `0x01`) and `t` (float32, fill `+0.0`) → entry_count = C·N = 4, disk
  ordinals channel-major. Bool planes are ⌈5/8⌉ = 1 byte with **three pad bits**, which
  `[R-SER-05]` fixes to the fill bit (so `0xE0`-masked high bits set). Float planes are
  20 bytes. **Slab S = 2, A_slab = 16**, so runs are [0,2) in channel block 0 and [2,4)
  in channel block 1.
- One file-scope user-metadata record, encoding 1, document `{"tarn.title":"demo"}`
  (21 bytes) + terminal CRC = 25-byte extent.

The claimant set §9.7 names — the directory, each record's extent (the tile-index
regions enter here, once, as their layer records' extents and "not a second claimant
beside it"), each non-sentinel well-formed entry's stored extent, plus the front block
and the live trailer, which §9.7 claims explicitly:

```
claimant                  start      len      end  gap before
front block                   0       16       16        0
A tile 0                    512       32      544      496   <- alignment gap
A tile 1                   1024       32     1056      480   <- alignment gap
A tile 3                   1536       32     1568      480   <- alignment gap
A index region             1568       84     1652        0
B tile 0                   1664        1     1665       12   <- A_slab gap
B tile 1                   1665        1     1666        0   <- packed
B tile 2                   1680       20     1700       14   <- A_slab gap
B tile 3                   1700       20     1720        0   <- packed
B index region             1720       84     1804        0
user-metadata extent       1804       25     1829        0
directory                  1829      251     2080        0
live trailer               2112       64     2176       32   <- pre-trailer pad
                                    -----
                             claimed  662
```

**Slack total = F − claimed = 2176 − 662 = 1514 bytes.** Verdict: **CONFORMING**.

**Which bytes are certified, which are counted-but-unconstrained, and can a byte be
neither?** The 662 claimed bytes are certified: each lies within [16, F−64) (the front
block and trailer excepted, which the [16,F−64) bound keeps disjoint from), no two
overlap, and each verifies against the checksum §8.1's map states for it — with the one
exception in §2 above. The 1514 slack bytes are counted and unconstrained: §5.2 says
"Slack has no internal structure this specification defines, its content is
unconstrained, and no conformance requirement applies to it."

No byte can be neither, and the document settles this rather than leaving it to me.
§5.2's Note: the live committed state is *defined* as the front block plus what a
complete walk reaches, and `[R-LIF-08]` makes every byte that walk misses slack — "so
'belongs to no class' describes nothing, and a register row for it would be a row no
file could exhibit." Of `[R-CNT-02]`'s two halves only disjointness is testable, and
that is what F33/L18 register.

**One arithmetic trap worth recording.** §5.2 says a partial total is "F less **the
bytes claimed by** the claimants the walk did enumerate — an upper bound on the file's
true slack, **never an under-count**." The obvious implementation, F − Σ(lengths),
*under-counts* whenever two claimants overlap, because the shared bytes are counted
twice on the claimed side. I built the case: a file where layer B's index region
[1648,1732) overlaps other claimants gives F − Σlen = 1694 but F − |union| = 1736. The
text's wording ("the bytes claimed by") and §9.7's ("the verifier sums *them*", them
being the unreached bytes) both mean the union, so this is determinate — but it is a
trap, and I implemented the union.

### 3b. A walk that does not complete

§5.2 gives two ways: a scope-level rejection ends that scope's enumeration, or the
verifier elects under `[R-CNF-11]` to stop at the first violation. I exercised the first.

Damaging layer B's segment CRC array (L38, reject-layer) makes the verifier discard
layer B's claimants — §5.2 is explicit that this holds "whether or not the rejection
impeded reading them", and that where the walk itself established the rejection (L18,
L40–L42) "the claimants it had already enumerated are discarded with the layer, since
the total is a claim about a live state one of whose layers is not usable". Layer B's
claimants total 1 + 1 + 20 + 20 + 84 = 126 bytes:

```
claimed 662 − 126 = 536
PARTIAL slack total = 2176 − 536 = 1640 bytes   (upper bound; true slack 1514)
walk stopped by: layer-scope rejection in layer 'B'  (L38)
verdict: NONCONFORMING
```

That is the shape §5.2 demands: a partial total, an upper bound, never an under-count,
naming the scope that stopped the walk.

**The case that does *not* make the walk incomplete.** I gave layer A's entry 1 a length
of 0 — T10, a *structural* reject-tile row. §9.7: "An entry `[R-IDX-03]` classifies
reject-tile on a *structural* ground does not make the walk incomplete: the walk passes
over it, and the bytes it nominally addressed fall to slack (§15.3)." My verifier
produced exactly that — claimed 630 (= 662 − 32), **complete** slack total 1546, verdict
nonconforming. A complete total on a nonconforming file is a coherent combination and
the text supports it; nothing about a tile-scope violation ends enumeration.

**Where the total is not owed at all.** §5.2 exempts one case: "Where §6.2's ordered
validation rejects the file before a live trailer is established there is no F and no
live state to walk, so the total is not owed at all". I tested F8 and F14 against this
and my verifier reports the trailer failure and nothing about slack. I could **not**
resolve the same question for F5 and for F6/F1's front-block instance, which also reject
before a live trailer but whose governing rules are `[R-CNT-27]` (§5.1) and `[R-CNT-04]`
(§6.1), not §6.2's ordered validation. That is finding **verifier-01**.

---

## 4. Extent overlap, alignment, and slab invariants on adversarial layouts

I ran a mutation battery against `gen1.tarn`. Reporting the ones that isolate cleanly.

**Alignment (`[R-SLB-01]`, L40).** Layer A declares A = 512. Moving tile 1 from 1024 to
1028 gives `1028 mod 512 = 4 ≠ 0` → L40, reject-layer, detector verifier, at
certification. Readers are not obliged: "offsets are always explicit, so alignment is
reader-invisible."

The quantifier question I had to settle: does L40 range over *every* non-sentinel entry
or only well-formed ones? `[R-IDX-03]`'s preamble settles it — an entry classified
reject-tile on a structural ground "contributes no stored extent to the *verifier* rows,
which bind over well-formed entries' extents only". My T10 case confirms: entry 1 with
length 0 is exempt from the alignment check, not a second violation. Conversely, an
entry whose *only* defect is that its stored bytes fail its crc "is well-formed: the
defect lies in the bytes it addresses, not in the entry, so its extent stands and it
keeps its place in the *verifier* rows, in run continuity, and in the coverage walk."
I implemented both and my verifier's T1 cases leave the extent claimed.

**Slab (`[R-SLB-03]`, L41/L42).** Layer B declares S = 2, A_slab = 16, planar, so runs
are per channel block: [0,2) and [2,4), never spanning blocks. Moving ordinal 3 from
1700 to 1704 breaks packing — the invariant is "each stored tile's offset equals the
previous stored tile's offset plus **its** length", 1680 + 20 = 1700 ≠ 1704 → L41.
Starting channel block 1's run at 1682 breaks `offset mod A_slab = 0` → L42.

§16.2 makes a claim I checked rather than assumed: "this invariant stays decidable from
the index entries alone, given the committed file length §15.3 already requires to
classify any entry." It holds, and the reason is subtle and correct — you need to know
which entries are *transparent* (sentinels, and structurally-reject-tile entries), and
both are decidable from an entry's own 20 bytes plus F. A crc-failing entry is not
transparent, so you never need to know whether its crc failed: it participates either
way. My implementation needs no payload fetch to evaluate L41/L42.

Degenerate slab cases I checked against the text: S > N is fine ("the final run of a
block can cover fewer than S ordinals"); a run with no stored tiles "imposes nothing";
sentinels close over ("If ordinal 10 is a sentinel, run 1's stored tiles are 8, 9,
11…15, packed with no gap where 10 would have been" — §16.2's own example); N = 0 gives
empty blocks and no runs.

A degenerate alignment case with a real consequence: A = 2⁶² is legal
(`[R-SLB-01]`: power of two, 512 ≤ A ≤ 2⁶²), but a stored tile's offset must be ≥ 16 and
a multiple of A, so the only admissible offset is 2⁶², and a *second* stored tile would
need 2⁶³, outside `[R-ENC-03]`'s domain. So a conforming file can store **at most one
tile** in a layer declaring A = 2⁶². Nothing is broken; T11 or L40 catches any attempt.

**Overlap (`[R-CNT-13]`, F33/L18).** The rule's trichotomy is intra-layer → reject-layer;
"any overlap across layers or touching another scope's structures" → reject-file; "any
overlap between two structures neither of which belongs to a layer" → reject-file. I
enumerated the cases a verifier meets and found the trichotomy exhaustive: tile×tile of
one layer, tile×own index region, tile×own sub-record extent (all L18); tile×other
layer's anything, tile×directory, tile×file-scope record extent (all F33); directory×
top-level extent, two top-level extents (F33). F33's condition also claims that a
claimant reaching the front block or the live trailer "is instead caught by the bounds
rows F9/F10, F31/F32, L16/L17 and T8/T9, each at its own tier" — I checked this and it
holds: every claimant class has a lower bound ≥ 16 and an upper bound ≤ F−64 registered
at its own tier, so no claimant can reach either end, which is also why §9.7's
"[16, F−64)" bound suffices to keep them disjoint.

**Pre-trailer gap (`[R-CNT-05]`, F7).** I moved the user-metadata extent past the
directory's end → F7, reject-file, verifier, certification. I also built the *conforming*
neighbour: a file with a 1952-byte pre-trailer gap (far longer than `[R-LIF-02]` step 5's
pad-to-64) and nothing in it. §6.2 is explicit: "a longer gap is conforming, and no
conforming commit produces one", and `[R-CNF-02]` names this as one of exactly two
declared conduct-not-bytes cases. My verifier certifies it — slack 3434 of F = 4096 —
which is the right answer and a nice illustration that the slack total is a *waste*
signal, not a validity signal.

---

## 5. Decoded-content obligations

**What a verifier must decode.** Every stored tile, unconditionally (§9.7). Every
user-metadata document under an assigned encoding (§18.2), or decline and lose
certification.

**What it must compare against.** Only what §14 structurally constrains, which §21.7
enumerates as "padding positions, pad bits, and boolean bytes" — and I checked that
enumeration is complete against §14: `[R-SER-05]` fixes padding positions and pad bits;
`[R-SER-08]` fixes interleaved bool bytes; `[R-SER-03]` expressly frees the value region
of a packed plane ("Every bit pattern of the value region decodes to a value sequence");
`[R-TYP-05]` frees every numeric bit pattern. So the tile checks are:

- T3 — decoded length is exactly the declaration-derived decoded size;
- T14 — under codec 1, the entry's length equals it (checkable before any fetch);
- T24/T25 — the decode consumes the extent exactly and does not fail;
- T4 — every padding position encodes, per channel it carries, that channel's fill;
- T5 — every pad bit carries the plane's fill bit;
- T2 — every interleaved bool byte at a **real** position is `0x00` or `0x01`.

T2 and T4 partition `[R-SER-08]`'s subject cleanly ("the same byte at a padding position
is T4's, the two rows together covering `[R-SER-08]`"), and I verified the partition is
exhaustive: at a padding position the byte must equal the fill byte, and L35 already
constrains a bool fill to `0x00`/`0x01`, so no interleaved bool byte escapes both rows.

I exercised T4 by zeroing one padding position of layer A's corner tile (which should
hold `CD AB`) and T5 by clearing the three pad bits of layer B's bool plane 0 (fill is
true, so all three must be set). Both fired at tile scope.

**What it is permitted to skip.** Three things and no more: (a) a decode declined on
resource grounds, which costs certification (`[R-ERR-04]`, §2.3); (b) the interior of a
layer it has rejected, which §5.2 turns into a partial total rather than a licence; (c)
the *content* of a user-metadata document under an unassigned encoding — `[R-MTA-10]` is
emphatic that this is not a decline and not a cannot-establish ground, because "no
content rule attaches to the extent's bytes". It must still check that record's framing,
extent slot, encoding-byte value set and terminal CRC, and it must **name the record** in
its report. It may **not** skip a tile decode for a layer with no padding positions and
no bool channels: §9.7 forecloses that shortcut explicitly.

**`[R-SER-08]`'s odd position.** §21.1 flags it as "the one rule that goes the other way:
it resolves a nonconforming interleaved boolean byte to a value rather than serving it
through". As a verifier I never exercise that path — I record T2 — but I noted that a
verifier is also a reader, and if it chooses to return the value rather than reject the
tile it owes "0x00 as false and every other byte as true". The two roles do not conflict:
the resolution rule "neither makes the byte conforming nor relieves the verifier".

**Filter.** I implemented byte-shuffle from `[R-COD-10]` and checked its stride rule
against §14: s = Q interleaved, s = element size for a planar numeric plane, s = 1 (and
therefore the identity) for a packed bool plane, and "The decoded image's length L is
divisible by s in every case" holds for all three (P·Q by Q; P·B by B; anything by 1).
I reproduced §17.3's worked example: `00 00 80 3F 00 00 00 40 00 00 40 40` with s=4,
n=3 shuffles to `00 00 00 00 00 00 80 00 40 3F 40 40`. T26 is verifier-detected and
witnessed only where the mis-strided image breaks padding content or bool bytes — which
is §21.7's subject, below.

---

## 6. Multi-generation trace

Four generations, each verified end to end. Every step asserted byte-identity of the
prior committed prefix before verifying.

**Gen 1 — creation.** `[R-LIF-02]`'s creation path: front block, then structures from
offset 16, then the complete directory and its CRC, then the barriers/pad/trailer with
generation 1 and a nonzero file_id. F = 2176, claimed 662.
→ **CONFORMING**, slack **1514**.

**Gen 2 — append a new layer C** (§20.3's shape (a)). Writing begins at exactly
F = 2176 (`[R-LIF-02]` step 1). Layer C: interleaved rank 1, E = 4, T = 2 → N = 2, one
`int8` channel, both tiles stored, index region 2·20 + 4 = 44 bytes. A, B and the
user-metadata record are re-emitted **byte-identically, extent slots and all**
(`[R-WRT-05]`), so layer A's record still addresses A's original index region — "a layer
the commit does not touch keeps its extent slot pointing where it always pointed".
F = 2688, claimed 807. Prefix [0,2176) byte-identical: **OK**.
→ **CONFORMING**, slack **1881**. The 367-byte increase is exactly dir₁ + pad₁ + trail₁,
which §20.3's shape-(a) figure says is "sized by the file's *layer count*, never by any
layer's data".

**Gen 3 — supersede layer A's tile 1** (shape (b)). The new payload had to be placed at
a 512-aligned offset, because §20.3 step 4 requires that "an aligned layer's stored tiles
— **every one the new state keeps, not only those this commit adds** — satisfy its
invariant or the declaration is cleared". Layer A's **whole** index region is re-emitted
at a new placement (`[R-WRT-04]`): one entry re-pointed, one sentinel and two entries
byte-identical at their disk-ordinal positions. F = 3648, claimed 807 (unchanged — one
tile in, one tile out; the old tile and the old 84-byte index region became slack).
Prefix [0,2688) byte-identical: **OK**.
→ **CONFORMING**, slack **2841**.

I checked the step-4 bar was not tripped: nothing in layer A's declarations changed, so
nothing §14 fixes for a tile stored in the superseded generation moved.

**Gen 4 — compaction** (§20.5). I implemented `[R-WRT-06]`/`[R-WRT-07]`/`[R-WRT-09]`:

- verified each link before emitting that structure's bytes — the open, each retained
  layer's record, the full index chain, and **every stored tile's entry crc**
  (`[R-WRT-09]`); my implementation asserts the crc rather than trusting it, since
  `[R-WRT-06]` says a compactor "MUST refuse to compact when any check `[R-WRT-09]`
  obliges fails";
- classified **every** entry while regenerating each region, per §20.5's paragraph on
  regeneration: a sentinel re-emitted unchanged, every other entry re-pointed. I checked
  the claim that a structurally-reject-tile entry "is neither — `[R-IDX-03]` gives it no
  stored extent for a re-pointing to target — so regenerating the region cannot proceed
  without meeting it", and it is right: my loop has no third branch, and no drop is
  available "a tile-index entry being no record §20.4's table licenses dropping". A
  compactor fed my T10 file must refuse;
- preserved every stored tile's bytes verbatim and every index entry's crc; recomputed
  segment CRCs over the entries as re-emitted; updated each layer record's
  `crc_of_crc_array`; re-pointed extent slots. I confirmed the licence to touch a layer
  record is exactly those two fields — which means a compactor may **not** clear a slab
  declaration under `[R-SLB-04]`'s "re-establish or clear" alternative, and must
  re-establish. Mine does: layer A's tiles stayed 512-aligned and layer B's runs stayed
  packed and 16-aligned;
- minted a fresh file_id and generation 1, and carried the input's (empty) ignore-lane
  bits forward.

Output F = **2304**, claimed 807, verdict **CONFORMING**, slack **1497**. Compaction
reclaimed 1344 bytes and the file shrank by exactly that.

**The residual 1497 bytes of slack is the interesting number.** Compaction does not drive
slack to zero and cannot: layer A declares A = 512, and §5.2 counts alignment gaps as
slack. So "the verifier's slack total … is what tells an operator to compact" (§5.2,
§22.3) is a noisy signal for any file with a declared alignment — the floor is set by the
declaration, not by history. Nothing in the document is wrong here (§16.1 says the gaps
"are slack (§5.2), which writers SHOULD zero and no conformance requirement constrains"),
but a verifier that reports only a raw total invites a pointless compaction. I would
report the total *and* the largest gap distribution; the document neither requires nor
forbids that.

Generational summary:

| gen | operation | F | claimed | slack | verdict |
|---|---|---|---|---|---|
| 1 | create | 2176 | 662 | 1514 | conforming |
| 2 | append layer C | 2688 | 807 | 1881 | conforming |
| 3 | supersede A tile 1 | 3648 | 807 | 2841 | conforming |
| 4 | compact (new file_id, gen 1) | 2304 | 807 | **1497** | conforming |

---

## 7. Register bookkeeping I checked mechanically

§21.8 claims "121 conditions over 277 instances". I parsed §21.2–§21.5's tables and
counted instances by §21.1's stated rule ("Instances within a cell are separated by
semicolons, and a cell reading — is one instance"):

```
F rows 36  instances  58
L rows 49  instances 116
T rows 26  instances  55
R rows 10  instances  48
TOTAL 121  instances 277
```

Exact. §21.2's stated "36 conditions", §21.3's "49", §21.4's "26" and §21.5's "10" all
match their tables.

I also checked §21.1's two stated instance axes against the rows that use them and found
no exception: layout-derived quantities enumerate their formulas (T3, T14, T21, T22, L44
— three formulas each); "differs from"/"does not equal" enumerates two directions
(F17, L21, L22, L30, T3, T14, T22); "exceeds"/"larger than" enumerates one (T21, L44);
a checksum-against-computed or byte-against-constant comparison enumerates no direction
(F14, F20, L37, L38, T1); a nonzero test is not a comparison (L20's *A ≠ 0 and S ≠ 0*
reads "—", one instance).

§20.5's parenthetical arithmetic also checks out: "§10.1's four vehicles", two of which
§21.6 makes conforming (ignore-lane bits, unrecognized `tarn.` keys), the other two
reaching a compactor "only as values this text still registers as reserved-range
violations — F36 and L25 for a record type, and one row for each of the other seven
spaces §10.2 tabulates (L31, L33, L34, L36, L43, L45, R1)". §10.2 tabulates eight
spaces; record type takes F36/L25; the remaining seven map one-to-one onto L36 (channel
layout), L33 (linearization), L34 (sample type), L43 (codec), L45 (filter), L31 (index
encoding), R1 (metadata encoding). Seven for seven.

R4's sixteen instances also reconcile with §18.2's carry-over list: eight frame
conditions (missing magic; skippable frame; second frame; nonzero dictionary ID;
content-checksum flag; bytes after the frame; content-size larger; content-size smaller)
× two containers (top-level extent, layer sub-record extent) = 16, and §18.2's two
expressly *unregistered* carry-overs (undisclosed dictionary use, the buffer-sizing bar)
are absent, as its text says they should be.

**Register completeness.** I walked every `[R-…]` identifier that binds a file's bytes and
tried to find a detectable file-conformance violation with no row. I found none. The
places where I expected a hole and did not find one: §7.4's full constraint table
(L27–L36, L39, L43, L45, L30, L34, L35, L1, L2, L21, L22 cover every field); §6.2's
eleven trailer fields (F8–F19 plus F2/F3); §10.3's reserved ranges (eight spaces, eight
rows); §4.6's three name rules across four namespaces (L5–L8, R6, R10, and the 255-byte
cap being forced by a `u8` prefix wherever one exists); and §8.1's six checksum links
(F14, F20, L37, L38, T1, R2).

---

## 8. Where I had to guess

Fifteen decisions had to be made to implement. Twelve of them the document settled,
sometimes only after re-reading:

- claimant set and the front-block/trailer's membership in it — §9.7, settled;
- whether a crc-failing entry keeps its extent in the walk — §9.7, settled;
- whether a structural reject-tile entry makes the walk incomplete — §9.7, settled (no);
- whether the walk uses the union or the sum of claim lengths — §5.2/§9.7, settled
  (union), but a trap;
- whether a rejected layer's already-enumerated claimants are discarded — §5.2, settled;
- front-block check ordering for a verifier — `[R-CNT-04]` + §2.3 + F6, settled;
- L40's quantifier over well-formed entries only — `[R-IDX-03]`, settled;
- whether L41/L42 need payload access — §16.2, settled (no);
- whether a compactor may clear a slab declaration — `[R-WRT-07]`'s closed list, settled
  (no);
- whether a compactor must classify every entry — §20.5, settled;
- whether a verifier may skip a tile decode on a layer with no content obligations —
  §9.7, settled (no);
- whether an unassigned metadata encoding is a cannot-establish ground — `[R-MTA-10]`,
  settled (no).

Three I could not settle from the text. They are the findings.

I also record two pieces of prose that are loose but that other text closes, so I am not
reporting them: §18.2's "A **verifier** that declines to decode a document on **the bound
above**" — the antecedent is ambiguous between the size bound (introduced two paragraphs
earlier and already once called "the bound above") and the frame's declared `Window_Size`
(introduced one paragraph earlier), but §21.5's preamble and §2.3's ground list both
treat the two grounds alike, so the verdict is the same either way; and §2.3's "whichever
of the three verdicts it reports" attached to the unable-to-check report duty, which
admits a *conforming*-plus-unable combination I could not construct.

---

# Findings

## verifier-01 — AMBIGUITY

**A verifier that stops at F5 or at the front-block instance of F1/F6 is under a MUST to
report a partial slack total it has no F to compute.**

Location: §5.2, `[R-CNT-21]`; with §5.1 `[R-CNT-27]` (F5), §6.1 `[R-CNT-04]` (F6),
§21.2's preamble, and §2.3 `[R-CNF-11]`.

Quotation, §5.2:

> a verifier that reaches a live state MUST report the total number of slack bytes,
> since that number is what tells an operator to compact. Where §6.2's ordered
> validation rejects the file before a live trailer is established there is no F and no
> live state to walk, so the total is not owed at all: the verifier reports the trailer
> failure and nothing about slack, which is not a partial total but the absence of one.
> Where the walk of §9.7 does not enumerate every region's claimants — whether because a
> scope-level rejection ends that scope's enumeration … or because the verifier elected
> under `[R-CNF-11]` to stop at the first violation — the verifier MUST report the total
> as partial.

The exemption is scoped by **citation** to "§6.2's ordered validation" but by **reason**
to "before a live trailer is established". Two register rows are reject-file, are
established before a live trailer, and are *not* §6.2's ordered validation:

- **F5** — "File size is below the 128-byte minimum", governing rule `[R-CNT-27]` (§5.1).
  A 100-byte file has no trailer to validate.
- **F6, and F1's front-block instance** — governing rule `[R-CNT-04]` (§6.1). §21.2's own
  preamble places this check ahead of §6.2's gates: "F6 with F1's front-block instance,
  which `[R-CNT-04]` places before other processing"; §2.3 and Appendix H remove the
  residency exemption for a verifier, so a verifier necessarily reaches this check first.

A verifier that elects under `[R-CNF-11]` to stop at the first violation and stops at one
of these has "elected … to stop at the first violation", which is the second limb of the
partial-total trigger. That limb's MUST therefore fires, and its object — "A partial
total is **F** less the bytes claimed by the claimants the walk did enumerate" — is
undefined, because F is the *live trailer's* committed file length and no trailer has
been validated. (The physical size is not F: §6.2 and `[R-CNT-10]` make F the trailer's
declared value, checked against the transport size.)

Permitted readings, both defensible:

1. **Purposive.** The exemption's stated reason ("there is no F and no live state to
   walk") governs, so it reaches every rejection before a live trailer, F5 and F6
   included; the verifier reports the failure and nothing about slack. This is what I
   implemented, and it is the only reading under which the MUST is dischargeable.
2. **Literal.** The exemption names §6.2 and only §6.2; F5 and F6 fall to the partial-
   total limb, and the verifier owes a partial total. Under this reading the only
   discharge is to keep walking past the violation (which `[R-CNF-11]` permits but does
   not require) so that a trailer is validated and F obtained — which makes a MUST on a
   verifier's *report* silently constrain whether it may stop early.

I picked (1). An implementer who picks (2) either emits an uncomputable field or is
forced not to stop early at exactly the two violations where stopping is cheapest.

Byte-level: **no.** Neither the emittable set nor any reader's accept/reject verdict
moves; the file is reject-file under both readings and the verdict is *nonconforming*
under both. What differs is one line of the verifier's report.

## verifier-02 — AMBIGUITY

**The verifier's verdict on a conforming file carrying an experimental-range MU = 1
*layer sub-record* of a type it does not implement is not stated, and §2.3's citation
points at text that expressly excludes that case.**

Location: §2.3 `[R-CNF-11]`; §21.6's closing paragraphs; §7.4 `[R-CNT-18]`; §5.2
`[R-CNT-21]`; §5.2 `[R-CNT-02]`.

Quotation, §2.3:

> A verifier reports one of three verdicts: *conforming*, *nonconforming*, or *cannot
> establish* — the last where some requirement is one it is unable to check on a
> capability or resource ground, as when the file names a format major version it does
> not implement, when a record carries MUST_UNDERSTAND = 1 with a type it does not
> implement (§21.6), when it cannot execute a codec or filter …

and §21.6, the text that clause cites:

> The second is an **experimental-range top-level record type carrying MU = 1** (§10.2,
> §10.3): `[R-CNT-15]` obliges the reader to reject, and `[R-CNF-02]` makes the file
> conforming all the same. The qualifier is load-bearing — the same type as a layer
> sub-record is reject-layer and never a ground to refuse the file (`[R-CNT-18]`), so
> only the top-level case is a file a reader refuses

The cited passage settles the *top-level* case and expressly distinguishes the
sub-record case, without saying what a verifier reports for it. The sub-record case is a
**conforming** file (`[R-CNT-18]`: "where the file is otherwise conforming a reader MUST
NOT reject the file for it"), so the verifier establishes no violation and the choice is
between *conforming* and *cannot establish*.

Permitted readings:

1. **Conforming.** The verifier established no violation. The unknown type is
   experimental, so this specification defines no requirement over it (§10.3), and
   §21.6's "never a ground to refuse the file" reads as: nothing here bars anything.
   Certify, reporting the rejected layer.
2. **Cannot establish.** `[R-CNT-18]` obliges the verifier — a reader — to reject the
   layer. §5.2 then says "a rejected layer's claimants are not enumerated, **whether or
   not the rejection impeded reading them**", so the coverage walk is incomplete and the
   slack total is partial. `[R-CNT-02]`'s partition is a file-level requirement, and §2.3
   defines a verifier as one that "checks every file-level requirement"; it has not
   checked that requirement for that layer, on a capability ground. Hence *cannot
   establish*, plus a per-requirement unable-to-check report under `[R-CNF-11]`.

I picked (2), because reading (1) would have a verifier certify a file while reporting a
**partial** coverage total, and §5.2 is explicit that a partial total "is not the file's
slack total but a bound on it" — a certificate resting on a bound is not the certificate
§2.3 defines. But the chain that forces (2) runs `[R-CNT-18]` → reject-layer → §5.2 →
incomplete walk → `[R-CNT-02]` unchecked → §2.3, none of which the document assembles,
while §2.3's one-line ground list cites the very passage that carves the case out.

An implementer who picks (1) certifies conforming files that an implementer picking (2)
refuses to certify — a divergence over the same bytes, on a MUST-governed output, for a
file whose *conformance* the document has already settled.

Byte-level: **no.** The bytes are conforming and stay conforming under both readings, and
every reader's obligation is fixed (`[R-CNT-18]`: accept the file, reject the layer).
Only the certificate differs, and a certificate is not an emit-or-accept decision.

## verifier-03 — OBSERVATION

**The one live-state region this specification leaves under no checksum at all — the
extent of a record of a type it has not assigned — carries no verifier reporting duty,
although the strictly better-protected sibling residue does.**

Location: §8.1 `[R-CNT-19]`'s map; §4.5; §18.2 `[R-MTA-10]`; §22.3 `[R-SEC-04]`;
Appendix H's verifier checklist.

Quotation, §8.1's map:

> | Extent of a record of a type this specification has not assigned | none — the bytes
> are opaque (§7.2) | — |

and §22.3, which places this residue beside the user-metadata one and reasons about both:

> The extent of a record of a type this specification has not assigned is covered by no
> checksum either (§8.1), so corruption inside it is equally invisible: §20.4's
> byte-identical re-emission (`[R-WRT-05]`) carries such an extent forward unread, and
> `[R-WRT-08]` bars re-encoding it, so nothing an updater does would surface the damage.
> … And the extent of a user-metadata record under an unassigned encoding is covered by
> its terminal CRC but constrained by no content rule (`[R-MTA-10]`): the CRC detects
> corruption and authenticates nothing (§4.5), so a certificate covers those bytes
> uninspected — which is why `[R-MTA-10]` makes the verifier's report name each such
> record, and an operator who wants no such bytes rejects on that report line, a policy
> above conformance.

`[R-MTA-10]` states the duty for the metadata case: the verifier "MUST report each record
it ignored on this ground, naming the owning scope, the encoding value, and the stored
extent length, as it reports the slack total (`[R-CNT-21]`): **bytes a certificate covers
without inspecting are counted and named, never silent**."

That principle applies *a fortiori* to the unassigned-record-type extent, which is the
harder case on every axis §22.3 itself names: it is covered by **no** checksum where the
metadata extent has one, it is carried forward unread by every updater, and — because an
experimental-range MU = 0 record is a conforming file (§21.6, `[R-CNT-15]`) — a verifier
must certify a file containing arbitrarily many such extents, of arbitrary size, without
inspecting or even checksumming a byte. My coverage walk claims those bytes (§9.7 checks
each claimant "against the checksum covering it, **where §8.1's map states one**"), so
they are neither certified nor counted as slack: they are certified-by-silence. Yet no
rule requires the verifier to name them, and Appendix H's verifier checklist lists the
`[R-MTA-10]` report line and not this one.

Two implementers therefore produce different certificates over identical bytes: one names
each opaque extent with its type, scope and stored length; the other says nothing, and an
operator running "a policy above conformance" has no report line to reject on for the
residue §22.3 calls the more invisible of the two.

I built the case to be sure it is reachable: a conforming file with one experimental-type
(≥ 0x8000) MU = 0 record whose extent is 1 MiB of arbitrary bytes. It verifies, it
certifies, and 1 MiB of the certificate's coverage is uninspected and unchecksummed.

The reason I grade this OBSERVATION rather than AMBIGUITY is that it is decidable from
the text — no reporting duty is stated, so none exists — and the cost of deciding it is
that a reader must notice an asymmetry §22.3 sets up and then declines to complete. The
finding is that the asymmetry looks like an omission rather than a decision, and no text
records it as a decision.

Byte-level: **no.** Nothing about which byte sequences may be emitted or must be accepted
changes; the file is conforming and every reader's and verifier's verdict is unaffected.
Only the content of the certificate differs.
