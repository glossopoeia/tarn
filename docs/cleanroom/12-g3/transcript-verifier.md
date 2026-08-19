# Cleanroom round 12 — Verifier implementer, working transcript

## 0. Disclosure

I read exactly one file: `/Users/robertkleffner/Documents/GitHub/tarn/spec/tarn.md`,
in full (3,982 lines), in five `Read` calls. I opened no ADR, no `PLAN.md`, no
`AGENTS.md`, no `conformance/`, no `spec/registry.json`, no git history, no web
resource. I ran `grep`/`rg` and Python against that file and against scratch
files I created myself.

One incident to disclose, because it touches the isolation rule. The session
scratchpad `…/scratchpad/round12/` is shared with at least one other agent
working this round. My first `crc.py`, `build.py` and `verify.py` were
overwritten by files of the same names written by that other agent, and when my
`import crc` failed I ran `ls -la` and `head -20 crc.py` to find out why. That
`head` showed me ~20 lines of another agent's CRC implementation plus the
opening of the Appendix A hex dump — content I had already computed
independently myself, and containing no specification text or conclusion I did
not already hold. I did not read any of the other files in that directory
(several are transcripts and workflow files whose names I saw in the `ls`
listing: `transcript-quiz-answers.md`, `transcript-quiz-key.md`,
`transcript-quiz-author.md`, `wf-round12.js`, `reconcile.py`, and others). I
immediately moved all my work into a private subdirectory `vwork/` and re-did
the clobbered files from my own source. Everything below was produced in
`vwork/` from the specification alone.

Programs written and run (all in `vwork/`): `tcrc.py` (CRC-32C),
`tbuild.py` (file writer), `tverify.py` (the verifier), `tappend.py` +
`trace.py` (appender and four-generation trace), `tadv.py` / `tadv2.py`
(adversarial layouts), `tids.py` / `tdef.py` / `reg.py` (register and
cross-reference arithmetic).

---

## 1. What I built

A conforming verifier per §2.3 `[R-CNF-11]`, exercised against files I wrote
myself with a conforming writer I also built from the document. Not a sketch:
`tverify.py` parses real bytes, verifies every checksum, walks coverage, checks
overlap/alignment/slab, decodes tiles, validates user-metadata documents, and
emits one of the three verdicts with a slack total and an unchecked-requirement
list.

The document sufficed. I found no place where I could not proceed. I found
three places where I had to reason across sections to reach an answer the
document does decide, or where it does not decide something it arguably should;
those are §7.

---

## 2. The certification procedure, as an ordered algorithm

The order is not free. It is pinned by four things: §6.2 `[R-CNT-06]`'s explicit
validation order for the trailer; §8.2 `[R-CNT-20]`'s chain of trust
(trailer → directory → crc_of_crc_array → segment CRC array → index segment →
index entry → stored tile); §4.5 `[R-ENC-10]` (verify the checksum covering a
field before acting on the field); and §4.2 `[R-ENC-05]` (allocate, seek or
fetch on no integer whose covering checksum is unverified). §19.1/§19.3/§19.4
give the reader path a verifier inherits.

Verdict vocabulary, from §2.3 `[R-CNF-11]`, is a strict three-way partition:

| state of the traversal | verdict |
|---|---|
| any violation established | **nonconforming** ("An established violation takes priority") |
| no violation, some requirement unchecked on a capability or resource ground | **cannot establish** |
| no violation, nothing unchecked | **conforming** |

Two report channels sit beside the verdict and never change it: the
per-requirement *unable to check* report (mandatory, "whichever of the three
verdicts it reports"), and *unexamined* for a verifier that exercised
`[R-CNF-11]`'s licence to stop at the first violation. Note that *unexamined*
can only ever accompany *nonconforming*: the licence is to stop "at the first
violation it finds", so a stopped traversal has established one.

What bars certification: any established violation at any scope (§2.4
`[R-CNF-12]`, "a verifier certifies only violation-free files"); and any
*cannot establish* ground — §2.3 names five, and §17.4 `[R-COD-11]` and §18.2
`[R-MTA-09]` each independently say "MUST NOT certify the file". A SHOULD
deviation does not bar certification; §2.4 says so in terms, and it is reported
as an advisory.

### The algorithm as implemented

```
 0. F = physical size. F < 128            -> F5 (R-CNT-27), stop.
 1. bytes [0,16) == front constant        -> F6/F1 (R-CNT-04).
      A verifier necessarily holds these: it must account for every byte of
      [0,F). R-CNT-04's "MAY defer or omit" is a *reader* exemption, and §2.3
      binds a verifier to "every file-level requirement — including those
      ordinary readers are exempted from". So the check is mandatory here.
 2. trailer, in R-CNT-06's stated order:
      magic (F8) -> trailer CRC (F14) -> version gate (F18; major != 1 ->
      CANNOT ESTABLISH, since R-CNT-24 leaves the other 48 bytes redefinable)
      -> flag gates (F19) -> field gates (F17,F13,F9,F16,F10,F11,F12,F15)
      + the domain/overflow rows the register supplies and §6.2's list does
        not restate (F2, F3) — §19's preamble says the register, not §19's
        enumerations, is the inventory.
 3. directory region CRC (F20). Claim [dir_offset, dir_offset+dir_length).
 4. record walk (F29,F24), per-type multiplicity (F34), extent slots
      (F30,F31,F32), user-metadata framing (F21,F22,F23), flag bits
      (F25,F26,F28), reserved-range types (F35,F36).
 5. per layer: R-RDR-03's full layer-record validation (L1..L36,L39,L43..L47,
      L49), all decidable from the resident directory and F — no fetch.
 6. per layer: index chain — crc_of_crc_array (L37) then each segment CRC
      (L38) — before touching any entry byte (R-ENC-05).
 7. per entry: §15.3 classification (T6..T12).
 8. verifier-only layout invariants: alignment (L40), slab packing (L41),
      slab first-tile alignment (L42).
 9. per stored tile: fetch [offset,offset+length), verify entry crc (T1),
      decode (T3,T14,T17..T25), inverse filter, check decoded content
      (T2,T4,T5,T26).
10. per user-metadata extent: terminal CRC (R2), decode (R3,R4), document
      content rules (R5..R10), member sort order (F27/L48).
11. coverage walk (§9.7): disjointness (F33/L18), containment in [16,F-64),
      slack total, and the pre-trailer-gap check (F7).
12. verdict.
```

Steps 11's pieces are necessarily interleaved with 5–9 in a real
implementation, because the claimant list is only obtainable once each layer's
index chain has verified. The document forces that: §9.7 says the walk reaches
claimants "through its records and their sub-records", and `[R-ENC-05]` forbids
acting on an entry before its covering checksum verifies.

**What the verifier reports when a check cannot be run.** §2.3: "A verifier
MUST report each requirement it was unable to check on a capability or
resource ground, naming the requirement and the ground". §18.2 adds a SHOULD:
report the decode bound applied and the stored length of the extent declined.
§21.9 `[R-ERR-04]` adds that the refusal "MUST be reported as a resource limit
and not as a validity error". My implementation carries an `unchecked` list of
`(requirement, ground, detail)` triples and prints it under every verdict.

I exercised all three verdicts:

```
codec not executable       : CANNOT_ESTABLISH | unchecked: ['R-COD-11']
metadata over decode bound : CANNOT_ESTABLISH | unchecked: ['R-MTA-09']
version_major = 2          : CANNOT_ESTABLISH | unchecked: ['R-CNT-07']
T4 violation + unchecked   : NONCONFORMING    | violations: ['T4']
                             ... and it still reports unchecked: ['R-MTA-09']
```

The last line is §2.3's priority rule working: the violation fixes the verdict,
and the unchecked requirement is still reported beside it.

---

## 3. The coverage walk, on a file of my own construction

I wrote a conforming file byte for byte (`tbuild.py`). Its shape:

* **Layer `a`** — interleaved, linearization 1, codec 1, filter 1, **alignment
  A = 512**, rank 2, dims `y`(E=4,T=2) `x`(E=4,T=2) → G=(2,2), N=4, P=4;
  channels `v` uint8 fill `00`, `w` uint16 fill `CD AB`. Q = 3, decoded size
  P·Q = 12. entry_count = 4 (interleaved ⇒ N). Index region = 4·20 + ⌈4/2¹⁶⌉·4
  = **84** bytes, matching `[R-CNT-17]`. Tiles 0,1,3 stored; tile 2 sentinel.
  Extents divide evenly, so this layer has **no padding positions**.
  One user-metadata sub-record.
* **Layer `b`** — planar, codec 1, filter 1, **slab S = 2, A_slab = 1**, rank 1,
  dim `t`(E=5,T=2) → G=3, N=3, P=2; channels `m` bool fill `01`, `n` float32
  fill `00000000`. Addressed = C·N = **6**; disk ordinals 0–2 are `m`'s planes,
  3–5 are `n`'s (channel-major, `[R-GEO-06]`). Decoded sizes: ⌈2/8⌉ = 1 byte
  for a bool plane, 2·4 = 8 for a float32 plane. Index region = 6·20 + 4 =
  **124**. All six stored. G·T = 6 > E = 5, so tile ordinal 2 of each channel
  block carries **one padding position** — and `[R-SER-05]` fixes its content
  to fill. For the bool plane that means in-tile ordinal 1's bit = the fill bit
  (1), and pad bits 2–7 = 1 as well, giving byte `FF`; for the float32 plane it
  means bytes `00 00 00 00`.
* One file-scope user-metadata record.

### The partition and the slack total

```
claimant                   offset   length  gap before
front                           0       16       0
tile a#0                      512       12     496
tile a#1                     1024       12     500
tile a#3                     1536       12     500
tile b#0                     2048        1     500
tile b#1                     2049        1       0
tile b#2                     2050        1       0
tile b#3                     2051        8       0
tile b#4                     2059        8       0
tile b#5                     2067        8       0
index a                      2080       84       5
index b                      2164      124       0
top UM extent                2288       63       0
sub extent (layer a)         2351       28       0
directory                    2379      282       0
trailer                      2688       64      27   <- pre-trailer pad
```

F = 2752. Union of claimed ranges = **724**. Slack = 2752 − 724 = **2028**,
which is 496 + 500 + 500 + 500 (the four alignment gaps A = 512 forces) + 5
(my chosen gap before layer a's index) + 27 (the pre-trailer pad). Verdict:
**CONFORMING**, slack total exact.

**Which bytes are certified.** The 724 bytes of the live committed state: the
front block by equality (§6.1); the trailer by its own CRC; the directory by
its terminal CRC; each index region by its segment CRC array under
crc_of_crc_array; each stored tile by its entry's crc; each user-metadata
extent by its terminal CRC. That is §8.1's map exhausted.

**Which bytes are counted but unconstrained.** The 2028 slack bytes. §5.2:
"Slack has no internal structure this specification defines, its content is
unconstrained, and no conformance requirement applies to it."

**Can a byte be neither?** No, and the document says why rather than leaving me
to infer it. §5.2's note: "The live committed state is *defined* as the front
block plus what a complete coverage walk reaches, and `[R-LIF-08]` makes every
byte that walk misses slack — so 'belongs to no class' describes nothing, and a
register row for it would be a row no file could exhibit." My arithmetic bears
that out: union(claimants) + slack = F identically, on every file I built.

One implementation note the text does decide but which a careless implementer
would get wrong: the total is F less the **union** of the claimed ranges, not F
less their **sum**. §5.2 says "Every byte the live state does not claim is
slack" and "F less the bytes claimed by" — both set-valued. My first pass summed
lengths, which under-counts slack whenever two claimants overlap; I corrected it.

### A walk that does not complete

I corrupted layer `a`'s `crc_of_crc_array` (only that field; every other
checksum recomputed so the file is otherwise sound). Result:

```
L37 crc_of_crc_array corrupt : NONCONFORMING  slack=2064  PARTIAL
                               (stopped: layer a index CRC array)
```

The verifier cannot act on layer `a`'s entries (`[R-ENC-05]`), so it enumerates
no tile extent for that layer. Three tiles × 12 bytes = 36 bytes leave the
claimant list, and the reported total rises 2028 → **2064**. That is exactly
`[R-CNT-21]`'s promised behaviour: "an upper bound on the file's true slack,
never an under-count", tightening "to the exact total when the walk completes".
The verifier reports which scope stopped it, as the same rule requires. Layer
`a`'s index *region* stays a claimant — it is reached as the layer record's
extent, independently of whether its contents verify.

Contrast a **structural** reject-tile. I forced layer `a`'s entry 1 to
offset 8 / length 12 (T8, offset < 16):

```
T8 entry offset<16 : NONCONFORMING  slack=2040  exact
```

Slack rises by exactly the 12 bytes that entry nominally addressed, and the
walk is still reported **complete**. That is §9.7's closing sentence and §15.3's
preamble working together — "the walk passes over it, and the bytes it
nominally addresses fall to slack", with §15.3 supplying the qualifier §9.7
elides ("any bytes it nominally addressed *that no other claimant claims*").
The two cases produce visibly different reports for superficially similar
damage, and the document distinguishes them correctly.

---

## 4. Extent overlap, alignment, and slab invariants on adversarial layouts

All built as real files with every downstream checksum recomputed, so that only
the targeted invariant is broken.

| adversarial layout | verdict | row | slack |
|---|---|---|---|
| two entries of layer `a` alias one extent (bytes untouched) | NONCONFORMING | **L18** reject-layer | 2040 exact |
| layer `a` entry claims layer `b`'s tile bytes | NONCONFORMING | **F33** reject-file | 2040 exact |
| layer `a` tile 3 at offset 1540, A = 512 | NONCONFORMING | **L40** reject-layer | 2028 exact |
| layer `b` run 0 unpacked (ord 0 @2048 len 1, ord 1 @2060) | NONCONFORMING | **L41** reject-layer | 2029 exact |
| layer `b` A_slab = 4096, run 0 first tile @2048 | NONCONFORMING | **L42** reject-layer | 2028 exact |

**Overlap scope** is decided by "belong to the same layer". `[R-CNT-13]`:
intra-layer overlap → reject-layer; "any overlap across layers or touching
another scope's structures" → reject-file. §15.3's two verifier rows and
F33/L18 restate it consistently. I checked the awkward case — two *file*-scope
structures overlapping each other (say two unknown-type record extents). It is
neither "intra-layer" nor "across layers", and the other is not "another
scope's" structure. F33's own condition covers it ("do not belong to the same
layer" is satisfied vacuously), and independently §2.4 `[R-CNF-08]` maps a
file-scope structure's validity error to reject-file, and `[R-CNT-02]` makes any
non-partition a file-level failure. Same answer three ways; no fork.

**Alignment.** `[R-SLB-01]`: "every stored tile's offset satisfies
offset mod A = 0". The quantifier is over *stored* tiles, so sentinels are out
by definition, and entries §15.3 classifies reject-tile on a structural ground
are out because §15.3's preamble says such an entry "contributes no stored
extent to the *verifier* rows, which bind over well-formed entries' extents
only" — the alignment row being one of them. An entry whose only defect is a
failed payload crc is explicitly *in*. My implementation follows exactly that,
and the rule is stated once and inherited by both §16 invariants rather than
restated (and possibly diverging) in each.

**Slabs.** `[R-SLB-02]` partitions each block of disk ordinals independently —
`[0,N)` interleaved, `[c·N,(c+1)·N)` per channel planar — with run r starting at
`block_start + r·S`. For layer `b` (planar, C = 2, N = 3, S = 2) that is:
block 0 → runs `[0,2)`, `[2,3)`; block 1 → runs `[3,5)`, `[5,6)`. My conforming
placement is 2048,2049 | 2050 | 2051,2059 | 2067 — packed inside each run,
free between runs, every run's first stored tile at a multiple of A_slab = 1.
`[R-SLB-03]`'s transparency rules matter and are stated: sentinels and
structural reject-tile entries close over, a crc-failing entry does not — "so
this invariant stays decidable from index bytes alone", which is what lets a
verifier check it without fetching payloads.

Two things I confirmed are decidable and are: (i) a run with no stored tiles
imposes nothing; (ii) the final run of a block may cover fewer than S ordinals.
Both are stated in `[R-SLB-02]`/`[R-SLB-03]`.

---

## 5. Checksum obligations

**Coverage.** §8.1's map, cross-checked against §4.5's prose, is complete and
consistent. Every field of every structure is covered by exactly one checksum,
with exactly three classes of exception, all named:

1. the front signature block — equality instead (§6.1);
2. the three **terminal** checksum fields — the trailer CRC, the directory
   region's final 4 bytes, and a user-metadata extent's final 4 bytes — which
   are comparison-verified and covered by nothing further;
3. the extent of a record of a type this specification has not assigned —
   covered by nothing at all, which §22.3 `[R-SEC-04]` then names as a stated
   residue rather than a defence.

The three **interior** checksum fields — each segment CRC array, each index
entry's crc, each layer record's crc_of_crc_array — are both
comparison-verified and covered by exactly one further checksum, and §4.5 says
so explicitly. I traced each: entry crcs live inside the entry array, covered
by their segment CRC; the segment CRC array is covered by crc_of_crc_array;
crc_of_crc_array lives in the layer record's inline payload, covered by the
directory CRC; the directory CRC is terminal. No cycle, no gap.

So the answer to "is every live structure covered by a checksum" is **no, and
the exceptions are enumerated and deliberate** — which is the right answer for a
verifier to have, because it tells it where its certification is silent.

**Constants I reproduced locally.** All of them that are computable:

| constant | spec | computed |
|---|---|---|
| CRC-32C(`"123456789"`) | `0xE3069283` | `0xE3069283` ✓ |
| CRC-32C(zero bytes) | `0x00000000` | `0x00000000` ✓ |
| CRC of a full all-sentinel segment (2¹⁶ entries, 1,310,720 bytes) | `0xEECB3BB2` | `0xEECB3BB2` ✓ |
| Appendix A trailer CRC over [0,60) | `0xE00938D2` | `0xE00938D2` ✓ |
| Appendix A directory region (CRC of zero record bytes) | `0x00000000` | `0x00000000` ✓ |

I additionally reconstructed Appendix A's whole 128-byte file from its hex dump
and decoded every trailer field against the annotation table: magic,
version_major 1, version_minor 0, flags 0, generation 1, dir_offset 16,
dir_length 4, committed_file_length 128, file_id `0x0123456789ABCDEF`, reserved
zero. All match. The reflected polynomial `0x82F63B78` reproducing the check
vector confirms the whole parameter set of `[R-ENC-09]` (Castagnoli, reflected
in and out, init and final XOR `0xFFFFFFFF`, stored little-endian).

**Constants I could not reproduce**, because they are external pins rather than
computations: the zstd compressed-frame magic `28 B5 2F FD` (RFC 8878), the lz4
decoded-size cap `0x7E000000` (the LZ4 Block Format's interoperability bound),
and the CRC-32C polynomial `0x1EDC6F41` itself as a *cited* RFC 3720 value —
though its reflection reproducing the check vector is strong local evidence the
citation is right.

**Every other worked number in the document also reproduces.** I checked them
all mechanically because a stale example is the cheapest kind of defect to
carry: §11.2's grids; §11.4's ordinals (s = 10, in-tile 11,452, planar disk 74);
§12.1's bfloat16 (1.0 → `0x3F80` → bytes `80 3F`; `0x7FC0` ↔ binary32
`0x7FC00000`); §12.3's twelve-byte channel entry
`04 74 65 6D 70 0C 00 04 00 00 C0 7F`; §4.6's `température` at 12 NFC bytes;
§14.2's 18/30-byte tiles and byte ranges [15,18), [10,12), [25,30); §14.3's
packed plane `55 01` / `55 FD` (I recomputed both fill cases bit by bit);
§14.5's 32-byte edge tile with 15 padding positions; §15.4's 1,000,000-entry
layer (16 segments, last covering 16,960, region 20,000,064, tile 999,999 at
segment-relative 339,180, array at [20,000,000, 20,000,064), segment 15 at
[19,660,800, 20,000,000), full segment 1.25 MiB); §15.4's planar example (disk
74 at region bytes [1,480, 1,500), channel 3 = ordinals 96–127); §17.3's shuffle
(`00 00 80 3F 00 00 00 40 00 00 40 40` → `00 00 00 00 00 00 80 00 40 3F 40 40`);
§20.3's 644-byte index; §21.9's note (2³² tiles → 256 KiB array, 2³⁶ → 4 MiB);
and §5.1/`[R-CNT-27]`'s 128-byte floor (front 16 + dir ≥ 4 at ≥ 16 ⇒ F − 64 ≥ 20
⇒ F ≥ 84, and F ≡ 0 mod 64 ⇒ F ≥ 128).

Zero discrepancies.

---

## 6. Decoded-content obligations

**What a verifier must decode.** Every stored tile of every layer, and every
user-metadata document. Not because one passage says so, but because §2.4
`[R-CNF-12]` says "A file is conforming only if it satisfies every requirement
at every scope" and "a verifier certifies only violation-free files", and §2.3
defines the class as one that "additionally checks every file-level requirement
— including those ordinary readers are exempted from". The tile-scope rows that
only a decode can settle are T3, T14, T17–T25 (all reader-detected) plus T2, T4,
T5, T26 (verifier-detected). A verifier cannot certify without establishing
their absence.

**What it must compare against.** Only declaration-derived quantities. The
decoded size is P·Q interleaved, P·Bᶜ for a planar numeric plane, ⌈P/8⌉ for a
packed planar bool plane (§14.2, §14.3), and `[R-SER-07]` insists it is "a
function of the layer's declarations alone — geometry, layout, and channel types
— never of payload content". Padding content compares against the channel's
**recorded** fill bytes (§13.1 `[R-TYP-06]`: authoritative, no type-derived
default), including the fill *bit* for a packed plane and every pad bit
(`[R-SER-05]`). Interleaved bool value bytes compare against {`0x00`,`0x01`}
(`[R-SER-08]`). A zstd frame's Frame_Content_Size, where present, compares
against the decoded size — and `[R-COD-06]` separately forbids sizing any buffer
from it.

**What it is permitted to skip.** Three things, each stated:

1. §21.7 `[R-ERR-01]`'s undetectables — wrong sample values, an undisclosed
   compression dictionary, a mis-strided filter whose resulting image happens to
   break no structural constraint. §21.7 forecloses the natural misreading:
   "None of these is a requirement a verifier is *unable to check* within the
   meaning of `[R-CNF-11]`: no file-level witness exists to check, so nothing
   about the file is left undetermined and the verdict is unaffected." So these
   do **not** push the verdict to *cannot establish*. That is exactly the
   distinction an implementer needs and would otherwise get wrong.
2. SHOULD deviations — reported as advisories, §2.4 `[R-CNF-12]`.
3. Decodes it declines on capability or resource grounds — but skipping these
   costs certification, not nothing: verdict becomes *cannot establish*
   (§17.4, §18.2, §21.9).

Where there is genuinely nothing to check, there is nothing to decode: a layer
with codec 1 needs no decode step at all (`[R-COD-04]`/T14 is checkable from the
entry and the layer record "before any payload fetch"), and a tile with no
padding position and no interleaved bool channel imposes no §14 content
obligation. My layer `a` is exactly that case, and my verifier does no content
work on it beyond the CRC and the length equality.

**User-metadata documents.** A verifier must decode and fully validate every
one: JSON well-formedness, top-level object, no BOM, finite numbers, no
duplicate keys under *decoded*-string identity, well-formed UTF-8 including
after `\uXXXX` escape resolution, key rules folded from §4.6 (non-empty, ≤ 255
bytes, no U+0000–U+001F) — R5 through R10 — **and** member sort order, which is
F27/L48 and is *not* quarantined, because unsorted members leave the document
readable. That last distinction is the sharp one and §18.2 states it plainly:
"unsorted members do not make a document unreadable: the file is nonconforming,
a verifier MUST report it, and readers process the document unchanged."

I checked whether an *ignored* record's extent still counts as a claimant, since
§2.4 says ignore-record means "skipped as though absent" — which would move a
conforming file's bytes into slack. It does count: §5.2 defines a record extent
as "the bytes any record's extent slot references, **whatever the record's
type**", §9.7 says "each record's extent" with no exclusion, and §8.1 has a map
row for an unassigned type's extent. "As though absent" governs the reader's
data path, not coverage — §5.2's note ("Coverage is checked by verifiers, never
by readers") settles it. Determined, and I nearly reported it before finding the
"whatever the record's type" clause.

---

## 7. Multi-generation trace

Written, appended to twice, compacted; verified after each step.

**Gen 1 — creation** (`[R-WRT-02]`/`[R-LIF-02]` creation path: front block;
tiles, index regions, record extents in any order satisfying §5.2; directory
and its CRC; barrier; pad; generation-1 trailer with a fresh nonzero file_id;
barrier).

**Gen 2 — append: store layer `a`'s tile 2.** Writing begins at exactly F =
2752. The layer declares A = 512, so the new tile goes at 3072 (192 bytes of new
slack). Layer `a`'s tile-index region is re-emitted **in full** — all 4 entries
plus the segment CRC array, 84 bytes — "necessarily at a new placement", with
one entry re-pointed and three byte-identical at their disk-ordinal positions,
per `[R-WRT-04]` step 4. Layer `a`'s record is modified (new extent slot, new
crc_of_crc_array); layer `b`'s record and the user-metadata record are re-emitted
**byte-identically**, header, inline payload and extent slot, per `[R-WRT-05]`.
The old index region and the old directory/pad/trailer become slack.

**Gen 3 — append: replace the file-scope user-metadata document.** §20.3's
example (c) is explicit that this is *not* the directory-only shape: "its
document lives in an extent (`[R-CNT-25]`), so a new extent is appended and the
old one becomes slack, as in (b)". So: new extent appended, the user-metadata
record's extent slot re-pointed, the two layer records re-emitted byte-identically.

**Gen 4 — compaction** (`[R-WRT-06]`/`[R-WRT-07]`): fresh file_id, generation 1,
every stored tile's bytes verbatim with its entry crc unchanged, each relocated
index region regenerated (offsets new; lengths, crcs and sentinels unchanged;
segment CRCs recomputed; crc_of_crc_array updated), extent slots re-pointed,
sub-record extents relocated. Layer `a`'s alignment and layer `b`'s slab
invariants re-established by the compactor as a writer of new bytes
(`[R-CNF-06]`, `[R-WRT-01]`).

```
gen  F      claimed  slack  %slack  verdict
 1   2752    724     2028   73.7%   CONFORMING
 2   3520    736     2784   79.1%   CONFORMING
 3   3968    772     3196   80.5%   CONFORMING
 4   2816    772     2044   72.6%   CONFORMING   (file_id changed, generation 1)
```

The trace demonstrates the properties the document claims for it. Claimed bytes
grow monotonically by exactly what each commit adds (724 → +12 tile → 736 →
+36 net metadata → 772) while slack grows faster; compaction leaves **claimed
unchanged at 772** and drops F from 3968 to 2816. §20.5's "The output's
reference arrays MUST equal the live generation's bit for bit" holds by
construction, since every tile's bytes and crc are copied.

The compacted file still carries 2044 bytes of slack. That is not a
contradiction of §20.5's "slack is never carried": the input's slack is gone,
and the output's is newly created by layer `a`'s own A = 512 declaration, which
§16.1 says leaves slack that "writers SHOULD zero and no conformance
requirement constrains". A verifier reporting 72.6% slack on a freshly compacted
file is reporting the cost of the alignment declaration, which is the right
thing for it to surface.

---

## 8. The register's own arithmetic

Because past rounds found defects in the register, I checked it mechanically
rather than by reading.

* Row counts: §21.2 = 36, §21.3 = 49, §21.4 = 26, §21.5 = 10. Total **121**.
  §21.8 claims "121 conditions over 248 instances".
* Instance counts under §21.1's stated mechanical rule (semicolon-separated;
  a cell reading `—` is one): F 53, L 106, T 45, R 44 = **248**. Exact match.
* Detectors: 101 reader, 20 verifier. All 20 verifier rows trace to a governing
  rule that does assign detection to the verifier, at the scope the row records:
  F7/`[R-CNT-05]`, F25/F26/L46/L47/`[R-CNT-12]`, F27/L48/`[R-MTA-05]`,
  F28/L49/`[R-CNT-22]`, F33/L18/`[R-CNT-13]`, F36/L25/`[R-CNT-15]`,
  L40/`[R-SLB-01]`, L41/L42/`[R-SLB-03]`, T2/`[R-SER-08]`, T4/T5/`[R-SER-05]`,
  T26/`[R-COD-10]`. No divergence found.
* Requirement identifiers: 160 distinct IDs across 19 prefixes, all 19 declared
  in §2.2. No prefix used but undeclared. No gaps in any prefix's numbering
  except ENC 17–99, which is just the `[R-ENC-100]` illustration in §2.2.
  `[R-SER-04]` appears once, in its own withdrawal note — correct per §2.2.
  **Every ID has a definition site**, and **no register row cites a rule that
  does not exist.**
* Appendix H's verifier checklist maps onto exactly the 20 verifier rows, with
  T26 correctly absent because T26's own text says its detection is T2's or T4's.

I also swept for detectable file-conformance violations the register might omit,
since §21.1 makes completeness normative. Every verifier check I implemented
lands on a row; every requirement whose violation has no row is either accounted
for in §21.7, or has an explicit no-row note (§7.4's nesting note, §16.2's stale
slab note, §5.2's "belongs to no class" note). I found no omission.

---

## 9. Places I had to guess, and findings

Three. None of them changes which bytes a conforming implementation may emit or
must accept or reject, and I say so for each rather than inflating them. I
considered and rejected several louder candidates (recorded in §10 below).

---

### verifier-01 — AMBIGUITY

**A reject-layer that does not itself impede enumeration leaves the walk's
completeness undecided, so two verifiers report different slack totals for the
same file.**

*Location:* §9.7 `[R-LIF-08]`, §5.2 `[R-CNT-21]`, §2.4.

*Quoted, §9.7:*

> Where the walk does not complete — a scope-level rejection blocks enumeration,
> or the verifier stops at the first violation (`[R-CNF-11]`) — the sum is
> reported as partial, and `[R-CNT-21]` governs what such a total counts and
> what the verifier reports beside it.

*and §5.2:*

> Where the walk of §9.7 does not enumerate every region's claimants — whether
> because a scope-level rejection stops it, or because the verifier elected
> under `[R-CNF-11]` to stop at the first violation — the verifier MUST report
> the total as partial.

The trigger is factual — did the walk enumerate every claimant — but the two
causes offered as gloss include "a scope-level rejection", without saying
whether a reject-layer *must* end enumeration of that layer.

Take L35: a bool channel's fill byte is `0x02`. Outcome reject-layer, detector
reader, detected at layer access. The defect is in a channel declaration and
does not impede the index chain at all.

* **Reading A.** Reject-layer is a scope-level rejection, and §2.4 says the
  outcome "bars further service from the layer". A verifier stops enumerating
  that layer's claimants and reports a **partial** total, naming the layer.
* **Reading B.** The trigger is whether the walk enumerated every claimant, and
  this one can. §2.4's outcome vocabulary is expressly a *reader* outcome
  ("Every detectable file-conformance violation … is assigned exactly one
  **reader outcome**"), and §21.1 adds that for a verifier the outcome "names
  the scope at which the damage is recorded, not an obligation on any reader".
  A verifier's own accounting is not "service", so it continues and reports an
  **exact** total.

I picked **B**, and implemented it: my verifier sets `partial` only when it
genuinely cannot enumerate — the index chain failed (L37/L38), or the layer
record would not parse. Reason: §2.4's vocabulary is scoped to readers by its
own words, and the operative trigger in both `[R-CNT-21]` and `[R-LIF-08]` is
the factual one.

*What an implementer does wrong without it.* Reports a needlessly loose bound.
§22.3 makes that consequential in terms: "a verifier that stopped early reports
it only as partial (`[R-CNT-21]`), so the distinguishing figure comes from a
walk that completes" — the slack total is the number that "distinguishes a
working file from a padded one" and tells an operator when to compact. Under
reading A, a single bad fill byte in one layer degrades the whole file's slack
figure to a bound; under B it does not.

*Byte-level:* **no**. Every file that exhibits the condition is nonconforming
under both readings — a reject-layer condition is a violation, so both verifiers
report *nonconforming*. Only the exactness of a reported number differs. No
reader or writer behaviour and no accept/reject verdict changes.

---

### verifier-02 — AMBIGUITY

**Appendix G's reproducible-writer profile fixes no order between two top-level
records of the same unassigned type, so two profile-conforming writers can emit
different bytes for the same input — the one thing the profile exists to
prevent.**

*Location:* Appendix G, item 3.

*Quoted:*

> Records are ordered by type, and within type 0x0001 by layer name; a layer
> record's sub-records are ordered by type, and within a type by their encoded
> bytes compared lexicographically — an order a reader can derive, which a
> creation order is not — record order carries no meaning (`[R-CNT-14]`), so it
> is otherwise free to vary, as is structure placement (`[R-LIF-02]` step 2).

Two top-level records of the same unassigned type are permissible: §7.2
`[R-CNT-14]` states multiplicity rules "per type — in format major 1: any number
of layer records …; at most one file-scope user-metadata record …; and at most
one user-metadata sub-record per layer record", and says nothing about unknown
types. §21.6 makes an experimental-range MU = 0 record a **conforming**
condition. So a file may carry two type-`0x8001` top-level records, each with an
extent.

Item 3 orders records "by type", tie-breaks type `0x0001` by layer name, and
gives a byte-lexicographic tie-break **only for a layer record's sub-records**.
Two top-level records sharing an unassigned type therefore tie with no
tie-break, and item 3's *placement* clause ("then any record extents in
ascending record order") inherits the tie, so both the directory bytes and the
extents' byte positions are undetermined.

* **Reading A.** The first clause states the general rule for all records and
  the second specialises sub-records; the lexicographic tie-break is available
  only to sub-records. Top-level ties are open.
* **Reading B.** The sub-record clause states a principle to be applied by
  analogy to top-level ties. This is a stretch — the sentence is a conjunction
  of two parallel statements about two different populations, not a general rule
  plus an instance.

I picked **A** and note the gap. The obvious fix is to extend the byte-
lexicographic tie-break to top-level records within a type.

*What an implementer does wrong without it.* Builds a profile-conforming writer
whose output is not byte-reproducible against another profile-conforming writer
— which defeats the profile's stated purpose ("Applications that need
byte-identical output — content-addressed storage, reproducible builds"). The
gap is squarely inside the profile's own ambition: it closes every other degree
of freedom deliberately, and even flags derivability as the criterion ("an order
a reader can derive, which a creation order is not").

*Byte-level:* **no**. Appendix G is non-normative and states "It adds no
requirement to any actor: a writer ignoring it is fully conforming". Both
orderings produce conforming files; no verifier verdict and no reader behaviour
differs. The divergence is between two implementations of an optional profile,
not between two conforming implementations of the format.

---

### verifier-03 — OBSERVATION

**That a verifier must decode every stored tile — the single largest cost in
building one — is decidable but is not stated in either section an implementer
would consult for it.**

*Location:* §17.4 `[R-COD-11]`, §9.7 `[R-LIF-08]`, resolved by §2.3 `[R-CNF-11]`
and §2.4 `[R-CNF-12]`.

*Quoted, §17.4 — the section titled "Certification under codecs":*

> The decoded-content obligations of §14 (`[R-SER-05]`, `[R-SER-08]`) require
> decoding. A verifier that cannot execute a layer's codec or filter cannot
> establish that layer's conformance and MUST NOT certify the file.

*and §9.7 — the section that says what a verifier's walk does:*

> It checks that these occupy disjoint byte ranges, that each lies within
> [16, F − 64), and that each verifies against the checksum covering it, where
> §8.1's map states one (§8.1).

§17.4 frames decoding as required *by §14's content obligations*. §9.7's walk
stops at checksums. Neither says the verifier must decode a tile in a layer that
has no padding position and no interleaved bool channel — where §14 imposes
nothing. But T3, T14, T17–T25 are file-conformance violations detectable only by
decoding (trailing bytes after a zstd frame, a malformed deflate stream, a
nonzero Dictionary_ID, a declared window above the decoded size), and the only
thing that obliges a verifier to establish their absence is the chain §2.3
("checks every file-level requirement — including those ordinary readers are
exempted from") plus §2.4 ("A file is conforming only if it satisfies every
requirement at every scope … a verifier certifies only violation-free files").
Those rows carry detector *reader*, and a reader's obligation is bounded by
§19.2's first-reliance rule — a reader that never reads a tile owes nothing —
so the reader-side chain does not reach a verifier that issues no read request.

Appendix H's verifier checklist reinforces the narrow impression by listing only
"decoded-content obligations — padding samples and interleaved boolean bytes
(§14.5, §14.2)" under the verifier-specific checks, though it does open with
"every reader obligation".

I resolved it in favour of full decoding and implemented that: the verifier
fetches, CRC-checks and decodes every stored tile of every layer. The
counter-reading — decode only where §14 bites — would let a verifier certify a
file carrying a T24 violation, which §2.4 flatly forbids, so the counter-reading
is not tenable once §2.4 is brought to bear.

*What an implementer does wrong without it.* Under-builds the verifier and
certifies files with malformed codec streams; or, reading §17.4 the other way,
over-reports *cannot establish* on layers whose content obligations are empty.
Both are avoidable with one clause in §9.7 or §17.4 saying that a verifier
decodes every stored tile.

*Byte-level:* **no**. §2.3 and §2.4 together do decide it; the cost is in
assembling four sections, not in a genuine fork. Two competent implementations
that read §2.4 will agree on every verdict.

---

## 10. Candidates I examined and rejected

Recorded so the reasoning can be checked rather than repeated.

* **A pre-trailer pad longer than 63 bytes.** `[R-LIF-02]` step 5 says a commit
  "pads to the next 64-byte boundary", so a 200-byte pad looked like a possible
  verdict fork. §6.2 resolves it in terms — "a longer gap is conforming, and no
  conforming commit produces one" — putting it in `[R-CNF-02]`'s class of writer
  obligations expressly declared not to be file-conformance violations. §21.1's
  normative completeness clause independently confirms it: a long pad is
  detectable and has no register row, so it must not be a violation. Also
  resolved: "pads to the next 64-byte boundary" when already aligned means zero
  bytes, since §6.2 says "a writer that ends its directory on a 64-byte boundary
  leaves none".
* **An appender re-emitting an index region that contains a malformed entry.**
  §20.3 step 2 commands the carry-forward ("not repaired to a sentinel"), while
  `[R-CNF-05]` says a writer emits only conforming files. Not a contradiction:
  §2.3 and §20.1 `[R-WRT-01]` deliberately bind an appender to "every writer
  requirement for the bytes it produces" rather than to `[R-CNF-05]`'s whole-file
  predicate, and §20.1 gives creators the whole-file duty and appenders/
  compactors the narrower one in adjacent sentences. Carefully done.
* **An ignored record's extent falling out of the coverage walk.** §2.4's
  ignore-record row says "skipped as though absent", which would make a
  *conforming* file's slack total implementation-dependent (§21.6 makes an
  experimental MU = 0 record conforming). Resolved by §5.2's "whatever the
  record's type" and §8.1's map row for an unassigned type's extent.
* **Two file-scope structures overlapping each other.** `[R-CNT-13]`'s dichotomy
  (intra-layer vs across-layers-or-another-scope) does not literally name the
  case, but F33's condition, `[R-CNF-08]`'s scope mapping, and `[R-CNT-02]`'s
  partition rule all deliver reject-file. No fork.
* **T23 (an LZ4 frame stored where a block is required) lacking the "this row
  records the cause" disclaimer** that its siblings T13, T15, T16 and T26 carry.
  I checked whether it is independently detectable: as a raw block, the frame
  magic's first byte `0x04` is a token meaning 0 literals and an 8-byte match,
  whose 2-byte offset `0x4D22` reaches past zero produced bytes, so the block
  decoder always fails. Detection is real, reject-tile either way, whether a
  reader checks the magic explicitly or just runs the decoder. Cosmetic at most.
* **`version_minor` under §4.7's new "or verifier" clause.** A verifier may
  report a `[R-CNT-26]` deviation as an advisory, which sounds like something a
  verifier does with the file's bytes. But §4.7's four-way enumeration — "where
  a byte lies, how it decodes, what a decoded value is, or whether the file,
  layer or tile is accepted at all" — bounds the test, and an advisory is none
  of those. `version_minor` stays descriptive and §4.7's claim that it is the
  only descriptive field survives the edit.
* **A commit that shrinks a dimension extent**, turning a previously-real
  position into a padding position whose stored byte is not fill. §20.3 step 4
  enumerates "tiles this commit stores or supersedes", "tiles that become
  unstored", "entries new to this generation (added tiles, grown extents)", and
  "every other entry byte-identical" — no case covers a shrink, so a writer
  following step 4 literally leaves a T4 violation. But the file-level rule
  (`[R-SER-05]`) is unambiguous and a verifier's verdict is determined, so this
  is writer guidance that could be more complete rather than a defect a verifier
  can be forked by. §20.3's example (c) shows the authors handled the analogous
  fill-change case explicitly.

## 11. Bottom line

I built a verifier end to end from this document and it certified files I built
from the same document, across creation, two appends and a compaction, and it
correctly refused ten adversarial layouts at the right scope with the right
register row. Every locally computable constant and every worked example in the
document reproduces exactly. The register's self-declared arithmetic (121
conditions, 248 instances) is exact, every requirement identifier resolves, and
no register row cites a rule that does not exist. The three findings above are
the only places I had to decide something the text left to me, and none of them
forks the bytes.
