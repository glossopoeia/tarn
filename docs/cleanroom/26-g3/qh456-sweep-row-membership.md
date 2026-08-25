# Sweep: which §21.2 file-scope rows reach a file declaring a major other than 1

## 0. Disclosure

Files read: exactly one — `/Users/robertkleffner/Documents/GitHub/tarn/spec/tarn.md`
(4495 lines). No docs/, no ADRs, no conformance/, no registry.json, no git, no web.

Commands run (all read only that file, or are pure computation):
- `wc -l spec/tarn.md` → `4495`
- `grep -n "R-CNT-24" spec/tarn.md`
- `sed -n '740,830p'`, `sed -n '3380,3520p'`, `sed -n '130,175p'`, `sed -n '700,745p'`,
  `sed -n '1440,1490p'`, `sed -n '2810,2835p'`, `sed -n '3330,3382p'`,
  `sed -n '3612,3626p'`, `sed -n '3640,3666p'`, `sed -n '2718,2732p'`
- `grep -n "geometry" spec/tarn.md`
- `grep -n "R-CNF-02" spec/tarn.md`
- `grep -n "subject" spec/tarn.md`
- `grep -n "^#### 21\." spec/tarn.md`
- two Python passes over the file that (a) join all lines into one whitespace-tolerant
  string, (b) strip `*`, `` ` ``, `_` so markdown emphasis cannot hide a phrase, and
  (c) regex-search with every literal space replaced by `\s+`, so a phrase spanning a
  hard wrap still matches. Line numbers are recovered from a per-character index map.

Context I did not ask for appeared in my runtime before I began: a project instruction
file, an index of the maintainer's memory notes, an environment block naming the branch
and recent commit subjects, and an MCP server instruction block. I disregarded all of it
as evidence and do not repeat its contents. Nothing below rests on it.

## 1. The paragraph under examination — verbatim

§21.2, lines 3432–3446:

> Outcome: reject-file. 36 conditions. A file declaring a format major
> other than 1 is neither conforming nor nonconforming under this text
> (§2.3, `[R-CNF-02]`), and the rows below whose subject is that
> file's *geometry* do not reach it: §6.2 puts the version gate ahead
> of every check but the trailer magic and the trailer CRC, so such a
> file is refused on capability grounds first. Four rows are outside
> that reasoning and do reach it, because their subject is a field
> fixed across every major (`[R-CNT-24]`): F8 and F1's trailer-magic
> instance, F14's trailer CRC — the two checks §6.2 places before the
> gate — and F6 with F1's front-block instance, which `[R-CNT-04]`
> places before other processing for a reader that already holds those
> bytes, one that would have to fetch them being free to defer or omit
> the check. F18 is not an exception but a case
> outside the premise: version_major = 0 declares no major at all and
> is permanently invalid in every one (§21.6).

(Not a blockquote in the source — it is body prose of §21.2 and therefore normative
text, not `[R-CNF-01]` non-normative matter. I quote it indented only for legibility.)

Two properties are offered:
- EXCUSING: "whose subject is that file's *geometry*" → does not reach.
- EXCEPTING: "their subject is a field fixed across every major (`[R-CNT-24]`)" → reaches.

## 2. [R-CNT-24] — exactly which fields it fixes

§6.3, lines 800–807, verbatim:

> In every format major version, permanently: the final 64 bytes of a
> file contain the trailer magic at F − 64, version_major and
> version_minor at F − 56, and a CRC-32C at F − 4 covering bytes
> [F − 64, F − 4); and the front signature block (§6.1) is constant. A
> future major MAY redefine only the remaining 48 trailer bytes and MUST
> NOT grow the trailer; additional space comes from structures placed
> before it. The format-major-1 trailer has zero slack: every byte is
> assigned. `[R-CNT-24]`

So the fixed set is exactly four items:
  (a) trailer magic at F−64  → trailer offsets [0,8)
  (b) version_major and version_minor at F−56 → trailer offsets [8,12)
  (c) CRC-32C at F−4 covering [F−64, F−4) → trailer offsets [60,64), covering [0,60)
  (d) the front signature block (§6.1), bytes [0,16), "is constant"

Arithmetic check that "the remaining 48 trailer bytes" is trailer offsets [12,60):
8 (magic) + 4 (version pair) + 48 + 4 (CRC) = 64. 60 − 12 = 48. Exact.
Therefore NOT fixed, and expressly redefinable by a future major: `flags` (12),
`generation` (16), `dir_offset` (24), `dir_length` (32), `committed_file_length` (40),
`file_id` (48), `reserved` (56). Cross-check against §6.2's trailer table, lines
744–756, which assigns exactly those seven fields to offsets 12…59.

Note on (d): the whole 16-byte front block is fixed, not just its magic half —
"the front signature block (§6.1) is constant", and §6.1's table (lines 701–704) gives
both halves: magic `89 54 41 52 4E 0D 0A 1A` at [0,8) and zero at [8,16).

## 3. What "geometry" means in this document

`grep -n "geometry" spec/tarn.md` — all 19 hits:

```
91:layer validation resolves into Part II's value sets and geometry
1045:geometry-derived addressed-tile count, is a validity error at layer
1445:bit-exact and every geometry identical; sample types, geometry,
1472:The owning scope (§2.4) of a layer's geometry and linearization fields
1931:function of the layer's declarations alone — geometry, layout, and
2823:geometry floor and its arithmetic (`[R-GEO-01]`–`[R-GEO-03]`),
3007:   (a geometry change renumbers ordinals wherever `[R-GEO-06]`
3043:   value — provided the grown geometry stays within every bound the
3049:   a growth is permitted exactly where the geometry it produces
3050:   satisfies every rule that geometry is subject to.
3151:> freely, subject to every rule its new geometry is subject to, which
3435:file's *geometry* do not reach it: §6.2 puts the version gate ahead
3514:| L21 | entry_count does not equal the geometry-derived addressed-tile count ...
3525:| L32 | A layer geometry field whose floor is 1 is 0 | rank d; channel count C; tile extent Tᵢ ...
3847:(§14.2, §14.3), so a reader allocates from geometry and never from
3983:dimension, and channel names; declared geometry; the write footprint
4255:structural field, which is why fill values, geometry, and codecs are not keys.
```

Every hit except line 3435 attaches "geometry" to a **layer**:
- §11.1 is titled "Geometry and its validity floor" (line 1470).
- Line 1472: "The owning scope (§2.4) of a layer's geometry and linearization fields / is the layer."
- §11.1 [R-GEO-01], lines 1475–1481, names the geometry fields: "A layer has rank d ≥ 1;
  each of its d dimensions has a name (§4.6), an extent Eᵢ ≥ 0, and a tile extent Tᵢ ≥ 1;
  and the layer has at least one channel."
- §21.3 L32, line 3525: "A layer geometry field whose floor is 1 is 0 | rank d; channel
  count C; tile extent Tᵢ".

Whitespace-normalised, emphasis-stripped searches (a failed line-grep would prove
nothing, so these were run over the joined text):

```
PAT: file's geometry      count 1   → line 3435 only (the paragraph itself)
PAT: geometry of the file count 0
PAT: file geometry        count 0
PAT: byte geometry        count 0
PAT: physical geometry    count 0
PAT: geometry field       count 1   → line 3525, "A layer geometry field"
```

**Derivation.** The phrase "that file's geometry" occurs exactly once in the document —
inside the sentence being examined. The document supplies no definition of a *file's*
geometry, and its only established sense of "geometry" is a layer's rank, dimension
extents, tile extents and channel count, which §11.1 assigns to layer scope (line 1472)
and which §21.3 (layer scope), not §21.2, registers. Under the document's own usage,
**no §21.2 file-scope row has "that file's geometry" as its subject.** The excusing
property therefore selects the empty set.

"Subject" is not a term of art here either: `grep -n "subject"` returns 13 hits, and all
but lines 3434 and 3438 are the ordinary "X is §N's subject" idiom (e.g. line 2330,
line 3632). I read a row's subject as the field or structure its Condition/Instances
cells range over, per §21.1 line 3356 "each row is one malformed condition".

## 4. The ordering premise the paragraph actually leans on

§6.2 [R-CNT-06], lines 773–782:

> A reader MUST validate, in order: the trailer magic; the trailer CRC;
> the version gate (§6.3) — only these touch fields whose positions are
> fixed across all majors (`[R-CNT-24]`) — and then, those gates passed,
> MUST validate all of the following before acting on the fields
> involved: the flag gates (§6.3); committed_file_length equals the file
> size ...  Any failure is reject-file.

§19.1 step 2, lines 2725–2729: "Fetch bytes [F − 64, F) and validate them in / §6.2's
fixed order — magic, trailer CRC, version gate, then the / remaining field gates".

§6.1 [R-CNT-04], lines 717–727: a reader with [0,16) resident "MUST verify the full block
by byte / equality before other processing"; one that would have to fetch them "MAY defer
or omit the check".

§2.3 [R-CNF-02], lines 141–145: "It is always conformance to a stated format major
version. This / document defines format major 1, and a file declaring another major / is
neither conforming nor nonconforming under it: a reader refuses / such a file on
capability grounds (§6.3, `[R-CNT-07]`), and that / refusal is not a finding about its
bytes."

So the *reasoning* after the colon is an ordering argument — a check placed after the
version gate never runs on such a file — and the checks placed before the gate are
exactly trailer magic, trailer CRC, and (for a resident reader) the front block. That
reasoning is sound and it selects F1/F6/F8/F14. But the *property the sentence names*
for the excused rows is "geometry", which is not that property and holds of no row.

## 5. Row-by-row derivation, F1…F36

Classification test applied to each row:
- GEOMETRY  = its subject is that file's geometry (per §3: nothing qualifies)
- FIXED-FIELD = its subject is one of §2's four [R-CNT-24] items
- NEITHER / BOTH otherwise.

| # | Subject (from the row's Condition + Instances cells) | Class | Why |
|---|---|---|---|
| F1 | the two signature constants: front block bytes [0,8); trailer magic at F−64 | FIXED-FIELD | both instances are [R-CNT-24] items (d) and (a) |
| F2 | u64 value domain of dir_offset, dir_length, committed_file_length, generation, record extent_offset/extent_length | NEITHER | all six live in trailer [12,60) or in directory records; none fixed; not layer geometry |
| F3 | wrapping sums dir_offset+dir_length, record extent_offset+extent_length | NEITHER | same fields as F2 |
| F4 | byte-identical layer-record name fields in the live directory | NEITHER | directory content; not fixed; not geometry |
| F5 | 128-byte minimum file size — F and committed_file_length | NEITHER | committed_file_length is at trailer offset 40 (redefinable); F is not a field. [R-CNT-27]'s floor is a major-1 rule |
| F6 | the 16-byte front signature block: magic [0,8); reserved [8,16) | FIXED-FIELD | [R-CNT-24] item (d), "the front signature block (§6.1) is constant" |
| F7 | a structure occupying the pre-trailer gap | NEITHER | gap geometry is a major-1 layout rule ([R-CNT-05]); not a fixed field |
| F8 | the 8 bytes at F−64 vs the trailer magic constant | FIXED-FIELD | [R-CNT-24] item (a) |
| F9 | dir_offset < 16 | NEITHER | trailer offset 24, inside the redefinable 48 |
| F10 | dir_offset + dir_length > F − 64 | NEITHER | both fields inside the redefinable 48 |
| F11 | generation = 0 | NEITHER | trailer offset 16, redefinable |
| F12 | file_id = 0 | NEITHER | trailer offset 48, redefinable |
| F13 | committed_file_length not a multiple of 64 | NEITHER | trailer offset 40, redefinable |
| F14 | u32 at trailer offset 60 vs CRC-32C of [0,60) | FIXED-FIELD | [R-CNT-24] item (c) exactly: offset 60 = F−4, [0,60) = [F−64, F−4) |
| F15 | the 4 reserved bytes at trailer offset 56 | NEITHER | [56,60) is inside "the remaining 48 trailer bytes" a future major MAY redefine. Its Governing-rule cell reads `[R-CNT-06]` (R-CNT-24), but §21.1 lines 3362–3364 make a parenthesised id "a further rule the condition reads", not a claim that the field is fixed — and R-CNT-24's own sentence puts [56,60) on the redefinable side |
| F16 | dir_length < 4 | NEITHER | trailer offset 32, redefinable |
| F17 | committed_file_length vs transport-authoritative size | NEITHER | trailer offset 40, redefinable |
| F18 | version_major = 0 | FIXED-FIELD | version_major sits at F−56, [R-CNT-24] item (b). §21.6 lines 3661–3662 independently: "version_major = 0, permanently invalid in / every format major version (F18, `[R-CNT-07]`)" |
| F19 | flags incompat lane, bits 0–15 | NEITHER | flags at trailer offset 12, first byte of the redefinable 48 |
| F20 | directory-region terminal CRC-32C | NEITHER | the region is located by dir_offset/dir_length, both redefinable |
| F21 | user-metadata record's extent slot (0,0) | NEITHER | directory record field |
| F22 | user-metadata record's extent_length < 5 | NEITHER | directory record field |
| F23 | user-metadata record's inline_length ≠ 1 | NEITHER | directory record field |
| F24 | top-level record type field = 0x0000 | NEITHER | directory record field |
| F25 | record flags MU = 1 with PE = 0 | NEITHER | directory record field |
| F26 | record reserved flag bits 2–15 | NEITHER | directory record field |
| F27 | file-scope user-metadata document object-member key order | NEITHER | document payload; not fixed, not geometry |
| F28 | registered type's stored MU/PE vs the §7.3 registry | NEITHER | directory record field |
| F29 | record header / inline payload overrunning the record sequence | NEITHER | directory record framing |
| F30 | record extent slot with exactly one half zero | NEITHER | directory record field |
| F31 | record extent_offset in 1–15, pointing into the front block | NEITHER | the front block's extent is fixed, but the row's subject is the record's extent_offset, a directory field |
| F32 | record extent_offset + extent_length > F − 64 | NEITHER | directory record fields |
| F33 | one byte claimed by two structures not of the same layer | NEITHER | live-state layout; not a fixed field |
| F34 | two or more user-metadata records in the directory | NEITHER | directory record multiplicity |
| F35 | reserved-range type 0x0003–0x7FFF with MU = 1 | NEITHER | directory record field |
| F36 | reserved-range type value 0x0003–0x7FFF | NEITHER | directory record field |

Tally: FIXED-FIELD = 5 (F1, F6, F8, F14, F18). GEOMETRY = 0. BOTH = 0.
**NEITHER = 31**: F2, F3, F4, F5, F7, F9, F10, F11, F12, F13, F15, F16, F17, F19, F20,
F21, F22, F23, F24, F25, F26, F27, F28, F29, F30, F31, F32, F33, F34, F35, F36.
5 + 31 = 36. ✓ (matches §21.2 line 3432 "36 conditions")

## 6. Comparison with the paragraph's own list of four

The paragraph names F8, F1's trailer-magic instance, F14, F6, and F1's front-block
instance — i.e. rows {F1, F6, F8, F14}. My derivation of the EXCEPTING property yields
{F1, F6, F8, F14, F18}: version_major is one of the fields [R-CNT-24] fixes, so F18
satisfies the stated property. The paragraph reaches the same *outcome* for F18 (it
reaches such a file) by a different and independently sound route — that a file with
version_major = 0 declares no major at all and so is not "a file declaring a format
major other than 1" in the first place. So the four-row list is not wrong about which
rows reach; it is under-inclusive as a list of rows satisfying the property it states.
No row outside {F1, F6, F8, F14, F18} satisfies the excepting property.

## 7. The gap

31 of the 36 rows satisfy neither offered property. For them the paragraph decides
nothing on its own terms: the excusing property ("subject is that file's geometry")
holds of zero rows under the document's only sense of "geometry" (§3), so it excuses
nobody, and the excepting property holds of five.

What the paragraph's *reasoning* would have decided, had the property matched it:
"§6.2 puts the version gate ahead of every check but the trailer magic and the trailer
CRC" — i.e. a check ordered after the version gate never runs. [R-CNT-06] (line 773)
states that ordering for **a reader**. Seven of the 31 carry Detector = *verifier* and
Detected = *certification*: F7, F25, F26, F27, F28, F33, F36. A normalised search for
"verifier" within 40 characters of "major" returns **zero hits** anywhere in the
document; nor is there any statement that a verifier applies the version gate first, or
declines to certify a file of another major. So even reconstructing the ordering
argument in place of the mismatched word leaves those seven undecided.

I searched for, and did not find: any definition of a file's geometry; any list of which
§21.2 rows survive a foreign major; any statement of verifier behaviour on a foreign
major. Those absences are well-searched, not merely undiscovered.

## 8. What I am supplying rather than deriving (not findings)

A charitable reading in which "that file's geometry" means the file's *byte layout*
(sizes, offsets, alignment) would move roughly F2, F3, F5, F7, F9, F10, F13, F16, F17,
F29, F30, F31, F32, F33 into GEOMETRY — about 14 rows — and would still leave about 17
in NEITHER (F4, F11, F12, F15, F19, F20, F21, F22, F23, F24, F25, F26, F27, F28, F34,
F35, F36), since a record's type value, a flag bit, a file_id, a generation counter and a
metadata document's key order are not layout under any reading. The document does not
license this reading; I state it only to show the count stays large either way.
