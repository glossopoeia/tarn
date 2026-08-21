# Round 18 repair audit — Appendix G (hunks 8 and 9)

Auditor working transcript. Written to be checkable, not readable.

## 0. Access disclosure

Read, in full or in part:

- `/private/tmp/.../round18-audit/hunk-08.diff` (my charter hunk)
- `/private/tmp/.../round18-audit/hunk-09.diff` (my charter hunk)
- `/Users/robertkleffner/Documents/GitHub/tarn/spec/tarn.md` — lines 555–674
  (§5.1, §5.2), 725–834 (§6.2, §6.3, §6.4 opening), 880–998 (§7.1 tail, §7.2,
  §7.3), 1000–1044 (§7.4), 1155–1256 (§9.1–§9.4), 2100–2170 (§16, §16.1,
  §16.2), 2872–2893 (§20.2), 3160–3209 (§20.5 / `[R-WRT-06]`), 3215–3239
  (§20.5 blockquote), 4080–4328 (Appendices D tail, E, F, G, H).

Not read: `docs/`, `PLAN.md`, `OPEN-QUESTIONS.md`, `AGENTS.md`, `README.md`,
`conformance/`, `spec/registry.json`, git history, git diff, the web,
`full.diff`, any other hunk file. I did not list the audit directory.

Commands run (all against the spec only):

```
grep -n "file_id" spec/tarn.md | head -80
grep -n "R-WRT-06\|R-CNT-14\|R-CNT-03\|R-SLB-05" spec/tarn.md
grep -n -i "little-endian\|little endian" spec/tarn.md | head -30
grep -n "tile-index region\|tile index region\|tile-index" spec/tarn.md | head -60
grep -n "record extent" spec/tarn.md
grep -n "0x0000000000000001\|Appendix G\|reproducib" spec/tarn.md
grep -n "#### 16" spec/tarn.md ; sed -n '2100,2170p' spec/tarn.md
```

plus two whitespace-normalising python scans (the document is hard-wrapped, so
line greps miss wrapped phrases):

```
python3 -c "import re; t=open('spec/tarn.md').read(); n=re.sub(r'\s+',' ',t); ..."
  patterns: 'fixed nonzero', 'any other fixed', 'measure-zero',
            'last eight bytes', 'substituted', 'remaining record',
            'ascending record order', 'disk-ordinal order', 'high-entropy',
            'fresh draw'
  patterns: 'The first structure begins at', 'forces a gap',
            'No declared alignment and no slab', 'One generation',
            'offset mod A = 0', 'fixed declared values'
```

Exact outputs of the two normalised scans are reproduced inline below where
they carry a conclusion.

## 1. Where the hunks land

Both land inside `### Appendix G — Reproducible-writer profile
(non-normative)`, spec lines 4128–4254. Hunk 8 is in numbered item 2
(`file_id` derivation), spec lines 4148–4169. Hunk 9 is in numbered item 3
(total emission order), spec lines 4170–4202.

Note on check 3 (does the repair sit in normative text): the whole appendix is
headed *non-normative*, and neither hunk is inside a `>` blockquote — the
numbered items are plain list text. So the usual `[R-CNF-01]` blockquote trap
does not apply here in either direction: the profile carries no BCP-14 force by
design ("It adds no requirement to any actor: a writer ignoring it is fully
conforming"), and the repair sits exactly where the rest of the profile sits.
Check 3 therefore passes for both hunks in the only sense available. The
standard I applied instead is the charter's: *any freedom at all is a failure*,
because the profile's entire claim is byte-identity.

## 2. Hunk 8 — the `file_id` fallback constant

### 2.1 The rule the repair adopts, in my words

A profile-adopting **creator** computes a named cryptographic hash at a named
version over `bytes[0, F−64) || trailer[0,60) with the 8 bytes at trailer
offset 48 set to zero`. It takes the last eight bytes the hash emits, decodes
them little-endian to a u64, and that u64 is `file_id`. If those eight bytes
are all zero — the only way the derivation can produce a value `§6.2` forbids —
`file_id` is instead the u64 value 1. A compactor does not use this rule at
all; it draws a fresh random id.

### 2.2 Check 1 — tense and quantifier

Generation: the rule speaks about the file being created — the *new* state, and
only its first and only commit (item 4 pins one generation). "This is a
creator's rule" makes the actor explicit and item 4 makes the generation
explicit. It does not restate a rule stated elsewhere in another tense; there
is no prior-state / new-state confusion available, because there is no prior
state. Quantifier: the fallback ranges over one file's one digest, singular,
triggered by a stated property of that digest. No set-valued quantifier is in
play. **Pass.**

The one quantifier worth naming: "the measure-zero case that **they** are all
zero". Antecedent chain: "the digest's last eight bytes in output order — the
eight a named hash emits last, read little-endian; naming the end rather than
calling **them** the *low* bytes is deliberate, that word being read as …".
"they" = those eight bytes. The alternative antecedent (the u64 identifier) is
not plural. And the two coincide: the eight bytes are all zero iff the
little-endian decode is 0. So the trigger is a test a writer can perform, with
no reading under which it selects a different set of files. **Pass.**

### 2.3 Check 2 — citations

- **"§6.2 forbids `file_id` = 0"** — opened §6.2 (spec 735–778). Table row:
  `| 48 | 8 | u64 | file_id | structural | ≠ 0 |`. Validation prose: "…
  1 ≤ generation ≤ 2⁶³ − 1; file_id ≠ 0; reserved bytes zero. Any failure is
  reject-file." **Passes**, exactly as claimed, and `≠ 0` is the *only*
  constraint §6.2 puts on the field — I checked the whole row and the whole
  ordered-validation sentence. That matters for check 5 below: the repair's
  implicit claim that zero is the only value needing a fallback is true.
- **"`[R-WRT-06]`'s fresh draw"** — opened spec 3160–3182. "It MUST mint a
  fresh file_id for the output — a new draw under §9.3's randomness advice, not
  merely a value compared against the input's — and generation 1". **Passes**;
  "fresh draw" is the requirement's own word-for-word content.
- **"§9.3's advice"** — opened §9.3 (spec 1220–1232). "the file_id chosen at
  creation (nonzero; the creating writer SHOULD draw it from a
  cryptographically random source — a predictable or reused file_id lets two
  distinct files collide in the (file_id, range)-keyed caches this rule
  licenses, serving bytes from the wrong file)". **Passes as a citation** (§9.3
  does state advice about file_id entropy); see F-03 for the substantive
  problem with what the appendix claims about it.
- **"`[R-LIF-03]`"** is not cited in the hunk; §9.3's requirement id is
  `[R-LIF-03]`, and the appendix cites "§9.3" by section, which resolves.
- **`[R-ENC-01]`** is not cited but is load-bearing (see 2.4). Opened spec 376:
  "… little-endian. `[R-ENC-01]` There is no byte-order mark and no big-endian
  …", and 385: "unsigned little-endian integers of 1, 2, 4, and 8 bytes. All
  file …". **Passes** — the u64 encoding of the constant is fixed globally.

### 2.4 The charter's three specific questions for hunk 8

**Width.** `0x0000000000000001` is written with 16 hex digits = 64 bits, and
lands in a field §6.2 types `u64`. No freedom.

**Byte order as it lands in the field.** Not stated locally; fixed globally by
`[R-ENC-01]` (all multi-byte fields little-endian; no BOM, no big-endian).
Field bytes are therefore `01 00 00 00 00 00 00 00` at file offset F−16.
I considered a rival reading — that `0x0000000000000001` names a *substitute
byte string* `00 00 … 01` which the preceding clause's "read little-endian"
then decodes to `0x0100000000000000`, giving field bytes `00 00 … 01`. I
rejected it: the sentence says "The **value**", the thing it substitutes for is
"the identifier" (a u64), and the parenthetical it justifies itself with is
about the *value* `file_id` = 0. A byte string is not called a value anywhere
in this document. I record the rival reading because the charter asked about
byte order and because the adjacent sentence does teach a byte-string→value
conversion, but I do not think it survives contact with the words, and I am not
reporting it. Consistency note in the repair's favour: because the primary path
is "digest tail decoded LE" and the field is re-encoded LE, the field bytes
equal the digest tail verbatim — no double swap.

**Trigger, and reachability.** Trigger = "they are all zero" = the eight
last-emitted digest bytes are all zero. Performable by inspection of the digest
before the trailer is written. Reachable: probability 2⁻⁶⁴ for a well-behaved
hash, not zero. ("measure-zero" is loose — the set has measure 2⁻⁶⁴, not 0 —
but that word is unchanged context, not the repair, and it is in a
non-normative appendix; not reported.)

**No circularity.** Checked, because a fallback is worthless if the primary
path cannot be evaluated. The hash input is `[0, F−64)` plus `trailer[0,60)`
with `file_id` zeroed. The trailer CRC lives at trailer offset 60 and is
therefore *outside* the hash input, so CRC → file_id → CRC has no cycle.
(The looser earlier phrasing in the same sentence, "together with the trailer's
other fields", would include the CRC and would be circular; the em-dash
restatement "the trailer's first 60 bytes" is the precise one and the only
satisfiable one. Unchanged context, resolvable by necessity, not reported.)

**Is the constant otherwise safe?** Grepped `file_id` document-wide (output
above). No rule reserves the value 1, and no other constraint on the field
exists. Example file at spec 3985 uses `0x0123456789ABCDEF`. No collision with
the repair's choice.

### 2.5 Check 4 — contradiction in the same passage, including untouched text

I read all of item 2 (spec 4148–4169) and both neighbours.

Two collisions found, both between the repair and untouched text of the same
numbered item:

1. **"a compactor adopting the profile takes `[R-WRT-06]`'s fresh draw
   instead"** (spec 4160–4163). The repair's purpose is to remove the last
   freedom from `file_id` under the profile. Three lines later the same item
   hands one class of profile adopter a 64-bit random draw — total freedom,
   exercised on every compaction, not on 2⁻⁶⁴ of them. Two compactors adopting
   the profile, given the same input, emit files differing at `[F−16, F−8)`.
   The appendix's opening sentence — "Applications that need byte-identical
   output … can adopt this profile, which closes the degrees of freedom this
   format deliberately leaves open" — is not qualified for this case, and the
   appendix's own convention *is* to qualify: item 1 says "Byte-identity across
   *implementations* is therefore unattainable for codecs 2–4", and item 4 says
   "Appending is reproducible only in the weaker sense that the appended bytes
   are." Item 2 says nothing of the kind. → **F-02.**

   I checked whether a compacted file is even in the profile's scope. Item 4
   requires "One generation, so that the file is the output of a single
   commit"; §20.5/`[R-WRT-06]` gives the compactor's output "generation 1", and
   §20.2 `[R-WRT-02]` routes a creator (which a compactor writing a new file
   is) through `[R-LIF-02]`'s creation path. So yes: a compacted file can
   satisfy every other item of the profile. The gap is real, not vacuous.

2. **"Deterministic, and high-entropy — satisfying §9.3's advice rather than
   contradicting it, which a counter would not."** (spec 4164–4165, untouched.)
   The repair now prescribes, for the fallback branch, the value
   `0x0000000000000001` — the first value a counter emits. In that branch the
   rule is deterministic but minimum-entropy, is not a draw, and is *shared by
   every profile file that hits it*, which is precisely the "predictable or
   reused file_id" hazard §9.3 names ("lets two distinct files collide in the
   (file_id, range)-keyed caches …, serving bytes from the wrong file").
   Confirmed against the restatement at spec 3842–3849: "The `file_id` (§9.3)
   is a stable 64-bit identifier that persists across every generation of a
   file - high-entropy only when its writer follows §9.3's randomness advice".
   → **F-03.** I note honestly that round 16's text ("Any other fixed nonzero
   value") had the same property; what the repair changed is that the profile
   now *mandates* the counter value rather than leaving the adopter free to
   pick one that is not, so the sentence reads worse after the repair than
   before. A fallback that preserved the claim was available at the same cost
   (e.g. the digest's *first* eight bytes, or the digest of the digest).

Collisions I looked for and did **not** find: no MAY in item 2 that a MUST
elsewhere forbids; no carve-out narrowing the derivation; nothing in §9.3,
§6.2, §20.2 or `[R-WRT-06]` that the derived-id rule causes an actor to
violate (the derived value satisfies `≠ 0` on both branches, and §9.3's
randomness statement is a SHOULD that the profile is entitled to depart from).

### 2.6 Check 5 — exhaustive claims in the repaired text

Words promising completeness in or adjacent to the repair:

- **"the measure-zero case"** — implies the fallback is the *only* case needing
  handling. Tried to falsify: §6.2 constrains `file_id` only by `≠ 0` (checked
  the table row and the ordered-validation list). No other value is barred, so
  the single carve-out is exhaustive. **Holds.**
- **"Deterministic, and high-entropy"** — falsified on the fallback branch.
  → F-03.
- **"This is a creator's rule"** — implies the actor partition
  {creator, compactor} is complete for this item. Updaters/appenders are
  excluded by item 4 ("One generation"), so the partition holds within the
  profile. **Holds.**
- **"the eight a named hash emits last"** — presupposes the named hash emits at
  least eight bytes; true of every cryptographic hash, and "a named function at
  a named version" is the profile's standard pinning idiom (same shape as item
  1 and item 9). **Holds.**

### 2.7 Sweep — does anything still describe the old behaviour?

Normalised scan for `fixed nonzero` and `any other fixed`: **zero hits
document-wide.** The old wording is gone and was not restated anywhere.
Normalised scan for `substituted` and `measure-zero`: one hit each, both the
repaired sentence. No unswept restatement for hunk 8.

## 3. Hunk 9 — "any **remaining** record extents"

### 3.1 The rule the repair adopts, in my words

In the profile's emission order, the phase that emits record extents in
ascending record order emits only those record extents not already emitted by
the per-layer phase — i.e. every record extent except the layer records' own
extents, which are the tile-index regions and were emitted immediately after
each layer's stored tiles.

### 3.2 Is a tile-index region a record extent? (the fact the repair turns on)

Yes, and normatively:

- `[R-CNT-02]` (§5.2, spec 624–628): "Every byte of the live committed state
  belongs to exactly one of: the front signature block; or a **structure** — a
  stored-tile extent, **a record extent (the bytes any record's extent slot
  references, whatever the record's type, §7.2)**, the directory, or the
  trailer."
- `[R-CNT-23]`/§7.4 (spec 1002): "A layer record's extent slot addresses the
  layer's tile-index region (§15); a layer with zero addressed tiles has extent
  (0, 0)."
- Corroborated non-normatively at §20.5 (spec 3225–3226): "every record extent
  but a relocated tile-index region — **itself a record extent (§5.2)**".

So under round 16's wording, "then any record extents in ascending record
order — all of them after every layer's tiles and index region" demanded that
each index region be emitted after itself. That is the defect the repair fixes,
and it fixes it. **The repair does what it claims.**

Terminology check, because the document uses "record extents" two ways. The
*contrastive* usage — index regions listed alongside record extents as if
disjoint — appears at §5.1 (spec 563), `[R-LIF-02]` step 2 (spec 1167–1169),
`[R-WRT-02]` (spec 2879–2880), and §21 rows F7, F33, L18 (spec 3361, 3387,
3416, which also list "sub-record extents" separately again). Under that
reading "remaining" is a harmless no-op; under `[R-CNT-02]`'s inclusive
reading it excludes the index regions. **The emitted set is identical under
both readings** (= all record extents other than layer records'), so the repair
does not fork on the document's own terminological wobble. Good property; I
checked it deliberately.

### 3.3 Check — is the order still total? Concrete file, emitted.

Configuration: layers `a` and `b`; `a` has 2 addressed, stored tiles (disk
ordinals 0, 1) and index region `Ia`; `b` has 1 stored tile and index region
`Ib`; one top-level user-metadata record `M` with extent `Em`; layer `a`
carries a user-metadata sub-record `Sa` with extent `Es`; no declared
alignment, no slab (item 5, first branch); one generation (item 4).

Emission per item 3:

```
[0,16)   front signature block            (§5.2: not a structure)
16       a: stored tile, disk ordinal 0   ("its stored tiles in disk-ordinal order")
         a: stored tile, disk ordinal 1
         Ia                                ("then its tile-index region")
         b: stored tile, disk ordinal 0
         Ib
         Em    remaining record extents, ascending record order:
               type order puts 0x0001 (a, b) first — excluded as already
               emitted — then 0x0002 (M).  ("top-level records first")
         Es    ("then, within each layer record, its sub-records")
         directory                          ("then the directory")
         pre-trailer pad to the next 64 boundary, every byte zero
[F-64,F) trailer                            (§6.2)
```

Every extent the file can contain is placed by exactly one clause:

| extent kind | placed by | count |
|---|---|---|
| stored-tile extents | per-layer, disk-ordinal order | once |
| layer-record extents (= tile-index regions) | "then its tile-index region" | once |
| top-level non-layer record extents | "any remaining record extents" | once |
| sub-record extents (any layer) | "any remaining …" + "within each layer record, its sub-records" | once |
| directory | "then the directory" | once |
| trailer | §6.2 + the pad clause | once |

Edge cases walked: a layer with zero addressed tiles has extent (0,0) —
`[R-CNT-23]` — so it contributes no bytes to either clause; a layer whose
entries are all sentinel has an index region but no stored tiles, still placed;
a record of an unknown/experimental type is ordered by the stated key (masked
header, inline payload, extent contents) without type knowledge, so it is
placed too. Sentinel entries occupy no bytes (`[R-SLB-03]`), so they cannot
create an unplaced extent.

Ordering coherence I checked and found sound: type 0 is invalid (§7.2), so
0x0001 is the lowest legal record type, so "ascending record order" would put
the layer records *first* anyway — the per-layer phase places their extents in
exactly the relative order the general rule would, tied by layer name as §7.3's
key specifies. The repair therefore removes a contradiction without creating a
mismatch between extent order and directory order.

Tie-break claim re-verified (untouched text): "Two records this key does not
separate are byte-identical in type, flags, lengths, payload and extent
content; emitting them in either order yields the same file". True — swapping
two such records swaps which extent offset each header carries, and since the
records are otherwise byte-identical the directory byte sequence is unchanged.
`[R-CNT-13]` forbids the two extents overlapping, so they are distinct byte
ranges of equal length and equal content; swapping them changes no byte.

### 3.4 Check 1 — tense and quantifier for hunk 9

"remaining" is a quantifier restriction over a set, so this is the check that
matters. Generation: item 4 pins one generation, so there is no
superseded-state/new-state ambiguity — every extent under discussion belongs to
the single committed state the file is. Set: "any remaining record extents"
ranges over record extents of the file being emitted, minus those the clause
already emitted. It does not silently become "the layer's record extents" or
"every layer's record extents". The matching normative rule it adopts is
`[R-CNT-14]` ("Record semantics MUST NOT depend on record order: readers MUST
NOT infer meaning from the position of a record within the sequence") — quoted
from spec 955–962 — which the appendix cites correctly as leaving order free
for the profile to fix. **Pass.**

### 3.5 Check 2 — citations in and around hunk 9

- **`[R-CNT-14]` "leaves order free"** — opened spec 955–962. It states record
  semantics MUST NOT depend on order and fixes multiplicity per type; it does
  not constrain order. **Passes.**
- **`[R-CNT-03]`'s advice, taken as a requirement here** — opened spec 660–664:
  "Writers SHOULD zero the gaps they create … A writer that does not … forfeits
  byte reproducibility (Appendix G)". **Passes**, and the cross-reference back
  to Appendix G is live.
- **`[R-SLB-05]`** (cited in the appendix's closing paragraph for gap extent) —
  opened spec 2110–2119: placement freedom over ordering and relative position.
  **Passes.**
- **`[R-LIF-02]` step 2** (cited as what leaves structure placement free) —
  opened spec 1166–1178: "(2) append new stored-tile payloads and tile-index
  regions …, and any new record extents …, **in any order** satisfying §5.2's
  coverage classes". **Passes.**
- **§5.2 "counts [the front signature block] as no structure"** — opened spec
  624–628: the partition lists the front block as an alternative *to* a
  structure. **Passes.**
- **§6.2's 64-byte trailer alignment** — opened spec 737–738: "The trailer
  occupies the final 64 bytes of the file, beginning at a 64-aligned offset".
  **Passes.**

### 3.6 Check 4 — contradiction in the same passage, including untouched text

I read all of item 3 (spec 4170–4202) and items 4 and 5 that follow.

Found: the placement sentence of the same item is unconditional about the first
structure while item 5 permits declared alignment.

> "The first structure begins at 16, directly after the front signature block,
> which §5.2 counts as no structure; each later structure begins where the
> previous one ended, save where alignment forces a gap — a declared A or
> A_slab, or §6.2's 64-byte trailer alignment, the pre-trailer pad included …"
> (spec 4195–4200)

> "5. **No declared alignment and no slab**, or fixed declared values …"
> (spec 4206)

> `[R-SLB-01]`, §16.1 (spec 2121–2131): "A layer MAY declare alignment A (§7.4):
> a power of two with 512 ≤ A ≤ 2⁶² … When declared: every stored tile's offset
> satisfies offset mod A = 0. … A verifier MUST check the invariant (violation:
> reject-layer, §15.3)"

Item 3's own order makes the first structure the lowest-named layer's
disk-ordinal-0 stored tile whenever that layer stores any tile. If that layer
declares A (item 5's second branch explicitly permits it, and item 3's own
exception clause names "a declared A or A_slab", so the profile plainly
contemplates it), then `16 mod A ≠ 0` for every legal A (A ≥ 512), and the two
sentences cannot both be satisfied. The "save where alignment forces a gap"
exception is attached grammatically to "each **later** structure begins where
the previous one ended", not to the first. Same bite for a slab with
A_slab > 16. → **F-01.**

This is untouched text, and hunk 9 did not cause it. I report it because the
charter's hunk-9 instruction is to "walk the whole ordering rule and confirm
every extent … is placed by exactly one clause, **in a determinate position**",
and this is where the position determination fails. It is the same numbered
item the repair landed in.

Related freedom I considered and am not reporting: "save where alignment forces
a gap" does not say "the smallest such gap". I read "forces" as carrying
minimality — a larger gap is not forced — and a writer inserting a larger one
is not following the sentence. Determinate enough; noted for the record.

Collisions I looked for in item 3 and did **not** find: no sentence that was
true only under "any record extents" and is false under "any remaining record
extents" (I re-read every sentence of item 3 for this); the clause "all of them
after every layer's tiles and index region, not interleaved with them" remains
true and non-vacuous under the new set; "so that record placement and record
order are pinned together" remains true, since the directory sequence still
includes the layer records and their relative order still matches the order
their index regions were emitted in.

### 3.7 Check 5 — exhaustive claims in hunk 9's text

- **"A total emission order"** — tried to falsify with the table and the worked
  file in 3.3. Every extent is placed exactly once. The claim holds *as an
  order*; it is the *positions* that fail under a declared alignment (F-01),
  which is a different sentence.
- **"all of them after every layer's tiles and index region"** — holds; the
  per-layer phase completes for every layer before the remaining-extents phase
  starts.
- **"every other type by the record's header with extent_offset masked to
  zero"** — "every other type" is exhaustive over types ≠ 0x0001. §7.3 assigns
  only 0x0001 and 0x0002 in major 1, plus §10's registry and experimental
  ranges; the key is computable for all of them without type knowledge (header,
  inline payload, extent contents), so the claim carries.
- **"Every other component is a function of content alone"** — checked against
  the header field list at §7.2 (spec 904–910): type, flags, inline_length,
  extent_offset, extent_length. With extent_offset masked, the survivors are
  all content-determined. **Holds.**

### 3.8 Sweep — restatements hunk 9 should have swept

Normalised scan for `remaining record`: exactly one hit, the repaired sentence.
Line grep for `record extent` gave the full list at §5.1/563, §5.2/625,
§7.2/947, §9.2/1168, §16 table/2057, §20.2/2880, §20.5/3225, and §21 rows
3356/3357/3361/3387/3399/3400/3413–3416/3506–3508.

The two places that state the same enumeration are `[R-LIF-02]` step 2 (spec
1167–1169) and `[R-WRT-02]` §20.2 (spec 2879–2880): "each layer's stored tiles,
tile-index region, and any record extents, **in any order** satisfying §5.2's
coverage classes". Both explicitly leave the order free, so the double-mention
of index regions is harmless there — nothing is over-determined and "remaining"
would add nothing. **No sweep was required; none is missing.** I checked this
deliberately because "a rule changed in one place and left standing in another"
is this project's most common defect shape.

Also checked: the appendix's closing paragraph (spec 4239–4254) names "record
and sub-record order, which `[R-CNT-14]` leaves free" and "gap *extent*, which
placement freedom (`[R-SLB-05]`) leaves open" — neither restates the emission
order in a way the repair would have had to update. §5.2's `[R-CNT-03]` and the
two blockquote mentions of Appendix G at spec 1859 and 2262 refer to byte
reproducibility generally, not to the emission order.

## 4. Verdicts

- Hunk 8 **does what it claims**: the fallback is now a single, fully specified
  u64, its bytes fixed by `[R-ENC-01]`, its trigger a performable test, its
  citation to §6.2 exact, and no residue of the old wording anywhere. Two
  defects survive in the passage around it: F-02 (a whole class of profile
  adopter still gets an unpinned, undisclosed random `file_id`) and F-03 (an
  adjacent claim the newly-chosen constant falsifies).
- Hunk 9 **does what it claims, and cleanly**: the double-placement of
  tile-index regions is gone, the emission order is total, the emitted set is
  the same under both of the document's readings of "record extents", and no
  restatement needed sweeping. One defect surfaced by the required walk of the
  same numbered item: F-01, the unconditional "first structure begins at 16"
  against item 5's permitted declared alignment.

## 5. Byte-level assessment

Appendix G is non-normative and binds no actor, so no finding here changes what
a *conforming* implementation may emit or must accept — the emittable set of
conforming files does not move for any of F-01, F-02, F-03. I say that plainly
rather than inflating. The forks are within the profile, which is where they
matter:

- F-01: reading A (exception applies only to later structures) makes a
  profile writer with A = 4096 put its first tile at offset 16, which
  `[R-SLB-01]` makes a reject-layer violation — a **nonconforming** file, so
  `[R-CNF-05]` bars every conforming writer from emitting it under both
  readings. The disputed file is not conforming: **not byte-level.**
- F-02: two profile-adopting compactors emit conforming files differing at
  `[F−16, F−8)`. Both files are conforming and both readings permit both, so
  the conforming set does not move: **not byte-level**, but the profile's
  central claim fails for compactors.
- F-03: changes no implementation behaviour at all: **not byte-level.**
