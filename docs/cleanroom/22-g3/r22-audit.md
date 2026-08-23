# Round 22 repair audit — hunks 01 and 02

## 0. Disclosure

Read, in full or in the ranges named:

- `/private/tmp/.../r22audit/hunk-01.diff` (whole file)
- `/private/tmp/.../r22audit/hunk-02.diff` (whole file)
- `/Users/robertkleffner/Documents/GitHub/tarn/spec/tarn.md` — ranges
  140–200 (§2.3 conformance definitions), 400–410 (`[R-ENC-04]`/`[R-ENC-05]`),
  1016–1045 (layer record inline payload table, `[R-CNT-23]`, `[R-CNT-17]`),
  1499–1530 (§11.2, §11.3 opening), 2235–2360 (§17.2 entire),
  2380–2530 (§17.4 + §18.1 + §18.2 through the JSON restrictions — the
  passage hunk 1 lands in), 3289–3372 (§21.1 entire), 3530–3560 (§21.5
  rows R1–R10 + §21.6 opening), 3600–3760 (§21.7 through §21.9 including
  the passage hunk 2 lands in), 3760–3800 (§22.2), 3965–4000 (`[R-VEC-03]`,
  `[R-VEC-04]`).

Ran: `grep`/`sed` and two `python3` heredocs over `spec/tarn.md` only
(whitespace-flattened substring searches to defeat the hard wrap, and a
mechanical instance count of the §21.2–§21.5 register). Both scripts read
`spec/tarn.md` and nothing else. Exact outputs reproduced below.

Did NOT read: `full.diff`, any other hunk file, `docs/`, `PLAN.md`,
`OPEN-QUESTIONS.md`, `AGENTS.md`, `README.md`, `conformance/`,
`spec/registry.json`, git history/log/diff, the web. Did not list the
r22audit directory.

**Unrequested context.** My runtime placed material in context before I
began: a project instruction file pointer (`CLAUDE.md` → `AGENTS.md`), an
index of the maintainer's memory notes with several titled entries, a
task list from prior sessions, an MCP server instruction block, and a
skills listing. I did not open any of the files those indexes name, and I
have not used their contents as evidence. Naming that they appeared, per
the charter; not repeating their contents.

---

## 1. Hunk 1 — §18.2, `[R-MTA-09]`, at spec/tarn.md:2467

### 1.1 The rule the repair adopts, in my own words

For a user-metadata document stored under encoding 2 (zstd), the
compressed frame's `Frame_Content_Size` field is optional; if a writer
includes it, its value must be the number of bytes the document decodes
to. A frame whose FCS field is present and unequal to the decoded byte
length is a *violation* of this specification — not a reader-capability
matter — and the outcome is the ignore-record outcome register row R3
carries. Consequently: `[R-CNF-05]` bars a conforming writer from
emitting such a file, and `[R-CNF-04]` obliges a conforming reader to
detect it at extent use and quarantine the record.

That is a genuine change to the emittable byte set. Before the repair,
§18.2 said "The constraints §17.2 states against a tile's declared
decoded size do not apply, because a document has no declared size", and
nothing else touched the FCS field, so an FCS carrying any value at all
was conforming. After the repair a whole family of previously-conforming
files is barred. So the repair is byte-level in its intent, which is
fine; my job is whether it does what it claims where it landed.

### 1.2 The passage as it now stands (spec/tarn.md 2455–2495)

```
Encoding 1 stores the document verbatim. Encoding 2 stores it as
exactly one RFC 8878 compressed frame occupying the extent's bytes
before its terminal CRC, under the frame constraints of
`[R-COD-06]` that do not reference a tile: the frame magic; no
skippable frame and no second frame; no nonzero dictionary ID; no
content-checksum flag. The constraints §17.2 states against a
tile's declared decoded size do not apply, because a document has
no declared size — a reader instead decodes with a bound of its
own choosing, no smaller than §21.9's user-metadata guarantee, and
a document exceeding that bound is ignore-record like any other it
cannot read. The frame's declared `Window_Size` is unconstrained
here for the same reason, and takes the same treatment: a reader's
window bound is its own, no smaller than §21.9's guarantee for that
quantity, and a frame declaring more than the reader admits is
ignore-record on that ground — the reader's capability, not a
failure to decode within the meaning of R3, and no violation: the
file exceeds a §21.9 guarantee and so remains conforming while the
reader MAY decline it (`[R-ERR-04]`). The frame's content-size field
is the one header quantity that is *not* left to the reader: it MAY
be present, and when present it MUST equal the byte length of the
decoded document. A mismatch is a failure to decode within the
meaning of R3, so that R3's condition stays checkable from the bytes
alone rather than turning on a decoder's tolerance (`[R-CNF-02]`) —
the tile rule of `[R-COD-06]` transposed to the quantity a document
does have, its decoded length, in place of the declared size it does
not. A **verifier** that declines to decode a document on
the bound above ... `[R-MTA-09]`
```

### 1.3 Check 3 — does the repair sit in normative text?

Yes. The paragraph is plain prose, no leading `>`, and the requirement
tag `[R-MTA-09]` trails it ("Any violation here is ignore-record, never
the tile-scope outcome §17.2 assigns. `[R-MTA-09]`", line 2494). The
following `> **Note.** The 16 MiB figure ...` block is non-normative and
the repair did not edit it.

Grep for the distinctive terms, whitespace-flattened so the hard wrap
cannot hide a hit:

```
=== "content-size"
   ... both being header-checkable. The frame content-size field MAY be
       present; when present it MUST equal the tile's decoded size, a
       reader MUST t...                                     [§17.2, R-COD-06]
   ... reader MAY decline it (`[R-ERR-04]`). The frame's content-size field
       is the one header quantity that is *not* left to the reader...
                                                            [§18.2, the repair]
=== "Frame_Content_Size"
   ... | T22 | Codec 3 (zstd) and the frame's Frame_Content_Size field is
       present but does not equal the tile's decoded size | ...
=== "byte length of the decoded"
   ... it MAY be present, and when present it MUST equal the byte length of
       the decoded document. ...                            [one hit only]
```

So the document-side FCS rule is stated exactly once, in normative text.
Check 3 **passes**. No stale `>`-block restatement of the old "the FCS is
unconstrained for a document" position survives — the two "no declared
size" hits are about the *declared decoded size*, not the FCS, and the
repair is careful to say it is transposing "in place of the declared size
it does not [have]", so those two sentences are not falsified. I looked
for that contradiction specifically and did not find it.

### 1.4 Check 2 — citations

**`[R-COD-06]` (§17.2, lines 2270–2299).** The tile sentence is:

> "The frame content-size field MAY be present; when present it MUST
> equal the tile's decoded size, a reader MUST treat a mismatch as a
> validity error at tile scope, and a reader MUST NOT allocate or size
> any buffer from it — the decoded size comes from the layer's
> declarations alone (§14, `[R-SER-07]`)."

The repair claims to be "the tile rule of `[R-COD-06]` transposed".
Verdict: **resolves, but the transposition is partial** — see §1.7 and
§1.8 below. Modality is preserved (MAY present / MUST equal). Actor is
preserved by derivation, not by statement: the tile rule names the reader
("a reader MUST treat a mismatch as a validity error at tile scope"), the
document rule names none, and the reader obligation arrives only through
R3's Detector cell plus `[R-CNF-04]`. Detectability is *not* preserved:
the tile comparison is against a declaration and is checkable before any
payload fetch; the document comparison is against a quantity that exists
only after a complete decode. The anti-allocation half of the tile rule
is dropped outright.

**R3 (§21.5, line 3536).** Condition cell, verbatim:

> "A user-metadata document's stored bytes fail to decode under its
> declared assigned encoding — under an experimental-range one this
> specification defines no decoding and §21.6 governs (`[R-MTA-10]`);
> encoding 0 and a reserved value are unassigned too and R1 registers
> both" | Instances: "top-level extent; layer sub-record extent" |
> reader | extent use | `[R-CNT-25]`

Verdict: **does not say what the repair claims it says.** A frame whose
FCS is wrong but whose blocks decode cleanly does not have stored bytes
that "fail to decode"; it has stored bytes that decode perfectly to a
length the header lied about. The repair does not amend R3; it asserts a
reading of it from `[R-MTA-09]`. §21.1's tiebreak — "where a row and the
rule it cites diverge, **the rule governs**" — does not help, because R3
cites `[R-CNT-25]`, not `[R-MTA-09]`. See finding A-01.

**R4 (§21.5, line 3540).** Condition cell, verbatim:

> "A user-metadata document stored under encoding 2 breaks one of the
> frame constraints §18.2 states or carries over from `[R-COD-06]` — the
> single frame occupying the extent's bytes before its terminal CRC
> included; unlike R3, the constraint is broken whether or not the bytes
> decode" | 12 instances | reader | extent use | `[R-MTA-09]` (R-COD-06,
> R-CNT-25)

Verdict: **the repair puts the mismatch inside R4's condition text while
routing it to R3.** "when present it MUST equal the byte length of the
decoded document" is a frame constraint §18.2 states. R4's governing rule
is `[R-MTA-09]` — the very requirement the repair was written into. See
finding A-01.

**`[R-CNF-02]` (§2.3, lines 133–156).** "Conforming file ... conformance
is a property of bytes: it does not depend on any reader, writer, or
environment." Verdict: **resolves.** The repair's use is sound as a
statement about *file conformance*: pinning the FCS means whether the
file is conforming no longer depends on whether a given zstd decoder
happens to police the FCS field. It does not, however, support the
stronger reading of "checkable from the bytes alone" as "checkable by
every conforming reader" — see finding A-05.

**`[R-ERR-04]`, `[R-COD-11]`, `[R-CNF-10]`, `[R-CNF-11]`** appear in the
surrounding untouched sentences; I read each (§21.9 line 3692ff, §17.4
line 2396ff, §2.3 line 130ff, §2.3 line 195ff) and none is disturbed by
the repair.

### 1.5 Check 1 — tense and quantifier

Generation: not in play; §18.2 speaks about the file's live state and the
repair does not introduce a prior/new-state distinction.

Set: the repair ranges over "the frame's content-size field" — singular,
over the one frame a document extent may hold. §18.2 has already fixed
that there is exactly one frame per document extent, and a file may hold
one file-scope document and one per layer, so the rule ranges over every
such frame the file carries. That matches the tile rule's quantifier
("the frame content-size field", per tile). No quantifier drift.

Modality: MAY/MUST, matching `[R-COD-06]`. No drift.

The one referent shift is deliberate and stated: from "the tile's
*declared* decoded size" to "the byte length of the *decoded* document".
The repair announces it. It is the source of the detectability change
(A-05) but it is not a silent substitution.

### 1.6 Check 4 — contradiction in the passage, including untouched text

I read the whole of §18.2 down to the end of the JSON restrictions, plus
the two `>` Notes. What I checked and what I found:

- "The constraints §17.2 states against a tile's **declared** decoded
  size do not apply, because a document has no declared size." Not
  contradicted: the repair's constraint is against the decoded length,
  not against a declared size, and the repair says so explicitly. I
  considered filing this and decided against it — the wording threads it.
- "> ... a document having no declared size and so no narrower scope
  whose declarations that rule can measure." Non-normative Note. Still
  true on the same reading. Not filed.
- "Any violation here is ignore-record, never the tile-scope outcome
  §17.2 assigns." Consistent with the repair (R3's outcome is
  ignore-record via `[R-CNT-25]`).
- `[R-MTA-02]`: "A reader MUST NOT let any part of a user-metadata
  **document** affect how a byte is located, decoded, or returned." The
  FCS field is part of the *frame header*, not the document, so this does
  not reach it. Relevant to A-04, not a contradiction.
- The live collision is with the register, not with §18.2 prose: A-01.

### 1.7 Check 5 — exhaustive claims

"**the one** header quantity that is *not* left to the reader" is a
count, and the same paragraph falsifies it twenty lines earlier: "under
the frame constraints of `[R-COD-06]` that do not reference a tile: **the
frame magic**; no skippable frame and no second frame; **no nonzero
dictionary ID**; **no content-checksum flag**." Magic_Number,
Dictionary_ID and the descriptor's Content_Checksum_flag are all frame
*header* quantities, all fixed by this specification, all not left to the
reader, and all registered against R4. The sentence is wrong as written.
Finding A-02.

"the tile rule of `[R-COD-06]` transposed" — a completeness word by
implication ("the tile rule", as if singular and wholly carried). The
tile rule has three clauses; two are carried and one (the anti-allocation
clause) is dropped. Finding A-04.

### 1.8 Check 6 — the structure, enumerated

Structure: the RFC 8878 compressed frame carrying a user-metadata
document under encoding 2, as §18.2 governs it. Every quantity the frame
header can carry, and what fixes it:

| Header quantity | What fixes it |
|---|---|
| `Magic_Number` (4 B) | §18.2 "the frame magic", carried from `[R-COD-06]`; R4 |
| descriptor: `Frame_Content_Size_flag` / `FCS_Field_Size` | the repair — presence optional |
| descriptor: `Single_Segment_flag` | **nothing states a rule.** It selects which of RFC 8878's two `Window_Size` derivations applies (§17.2's Note states both). See A-03 below for the consequence the repair creates here |
| descriptor: `Unused_bit` | nothing here; covered only by the umbrella "exactly one RFC 8878 compressed frame". Free encoder choice, `[R-CNF-05]` class — the same status §17.2's Note gives DEFLATE's final-byte high bits, except that no Note says so for zstd |
| descriptor: `Reserved_bit` | nothing here; same umbrella. A frame with it set is not an RFC 8878 frame, so it lands in R3 or R4 by derivation, and §18.2's carry-over list — which is written as a closed list — never names it |
| descriptor: `Content_Checksum_flag` | §18.2 "no content-checksum flag"; R4 |
| descriptor: `Dictionary_ID_flag` | via "no nonzero dictionary ID"; R4 (a present-but-zero ID stays legal, as for tiles) |
| `Window_Descriptor` → `Window_Size` | deliberately left to the reader, stated in the sentence before the repair; not a violation |
| `Dictionary_ID` (0–4 B) | §18.2 "no nonzero dictionary ID"; R4 |
| `Frame_Content_Size` (0–8 B) | **the repair** |
| trailing `Content_Checksum` | excluded by the flag rule |
| bytes after the frame | §18.2 "occupying the extent's bytes before its terminal CRC"; R4 |
| extent terminal CRC | R2, `[R-CNT-20]` |

Two things fall out of this table that the repair did not see.

**(a) The single-segment interaction.** §17.2's Note states the mechanism
in the document's own words: "with Single_Segment_Flag set there is no
Window_Descriptor and Window_Size is the frame content size, which this
requirement already obliges to equal the decoded size". For a *tile*,
§17.2 then reassures that "no conforming file turns on which derivation a
reader implements", and adds a writer SHOULD: "Writers SHOULD keep the
declared window within §21.9's 8 MiB `Window_Size` guarantee even for a
larger tile."

The repair transposes the FCS equality to documents and transposes
neither of those. The consequence is arithmetic: after the repair, a
single-segment document frame's `Window_Size` **is** the decoded document
length. §21.9 guarantees a reader accepts a 16 MiB document but only an
8 MiB window, and `[R-ERR-03]` says of the whole table "a writer MAY rely
on that". A writer that relies on the 16 MiB document row and emits a
12 MiB document as a single-segment frame has produced a file with a
value above the `Window_Size` guarantee, so `[R-CNF-03]`'s acceptance
duty does not run to it and §18.2's own sentence lets a reader
ignore-record it. The document guarantee is effectively 8 MiB for
single-segment frames, and nothing tells the writer. Finding A-03.

**(b) The allocation clause.** Finding A-04.

The remaining ungoverned members (`Unused_bit`, `Reserved_bit`,
`Single_Segment_flag` as such) I judged to be adequately covered by the
"exactly one RFC 8878 compressed frame" umbrella and did **not** file as
defects. I note them here so the enumeration is complete rather than
selective; the closure wording that papers over them is A-02.

### 1.9 The register arithmetic

Script (reads `spec/tarn.md` only), counting rows and semicolon-separated
instances in §21.2–§21.5:

```
rows: 121 instances: 273
21.2 rows 36 instances 58
21.3 rows 49 instances 116
21.4 rows 26 instances 55
21.5 rows 10 instances 44
```

This matches §21.8 exactly — "121 conditions over 273 instances" — which
proves the repair added no instance anywhere. Compare T22, the tile row
for exactly this condition: 6 instances (three layouts × two directions,
"declared larger" / "declared smaller"), because §21.1 mandates it:
"Where the condition compares two **magnitudes** either of which can be
the greater — a *differs from* or *does not equal* — the two directions
are likewise enumerated." R3 has 2 instances, R4 has 12, and neither
enumerates a direction of an FCS comparison. `[R-VEC-03]`: "every
register row has at least one vector for each instance it names."
Finding A-06.

---

## 2. Hunk 2 — §21.9, at spec/tarn.md:3684

### 2.1 The rule the repair adopts, in my own words

§21.9's eight-row guarantee table does not mean the same thing row by
row. For the last three rows — one tile's decoded size, one document's
decoded size, one zstd frame's `Window_Size` — the quantity exists only
where a corresponding object exists in the file, so a file with no tiles
(or no documents, or no compressed frames) cannot exceed that row no
matter what its declarations would derive. For the first five rows the
quantity is a declaration and always exists, so those rows always bite.

### 2.2 The table, counted

Ten `|`-lines between 3670 and 3692 = 1 header + 1 separator + **8 data
rows**. "The last three" + "The first five" = 8. The arithmetic of the
partition is correct.

Row by row, against the side the paragraph puts it on:

1. **rank d of a layer** — declared `u8` in the layer record inline
   payload (line 1016). Declaration side. Present in every layer; absent
   in a file with zero layers (a conforming state, §21.6, `[R-CNT-14]`).
2. **channels per layer, C** — declared `u16` (line 1017). Same.
3. **addressed tiles per layer (entry_count)** — declared `u64` (line
   1021): "equals the addressed-tile count (§11.2, `[R-CNT-17]`)". This
   is the charter's "count that is zero rather than absent": a layer
   addressing no tile carries `entry_count = 0` as a present field —
   `[R-CNT-17]` even legislates the `entry_count = 0` case, and
   `[R-CNT-23]` requires `crc_of_crc_array = 0` there. The paragraph puts
   it on the declaration side. **Correct.**
4. **layers per file** — there is no declared layer count. I grepped:
   `dir_length` is a trailer field (line 748), and nothing named
   `layer_count` exists. The layer count is obtained by parsing the
   directory's record sequence — i.e. it ranges over the layers a file
   *actually contains*, which is the paragraph's own definition of
   per-instance. Put on the declaration side, with the stated ground
   "declarations, which every file and every layer carries". Finding
   A-08 (harmless in outcome — 0 ≤ 65,536 either way — but the ground is
   false, and the paragraph is nothing *but* a statement of ground).
5. **dir_length** — trailer field, line 748. Declaration side, present in
   every file. **Correct and the only unarguable member of the five.**
6. **decoded size of one tile** — the genuinely arguable row. See A-07.
7. **decoded size of one user-metadata document** — instance side.
   Correct: §18.2 states a document has no declared size. (Cross-hunk
   note: hunk 1 now pins the FCS to the decoded length, so an
   FCS-carrying frame does expose the quantity in its header. §18.2's
   Note still says the decline is at the whole file "a document having no
   declared size and so no narrower scope whose declarations that rule
   can measure" — non-normative, and still defensible, so I did not file
   it.)
8. **zstd frame `Window_Size`** — instance side. Correct: the window
   lives in payload bytes, never in a declaration.

So the "one row whose side is genuinely arguable" is row 6, and the
"count that is zero rather than absent" (row 3) is placed correctly.

### 2.3 Check 4 — the two sentences after the table

The sentence immediately following, untouched by the repair:

> "A file exceeding any of these remains conforming, and a reader MAY
> decline it — at the whole file, or at the narrowest scope whose
> **declarations** exceed what it can serve, a layer or a tile. Software
> that declines **on that ground** a file whose every quantity lies
> within the table is not a conforming reader (`[R-CNF-03]`)..."

Take an empty layer: any dimension extent Eᵢ = 0, so Gᵢ = ⌈0/Tᵢ⌉ = 0 and
N = ∏Gᵢ = 0 (§11.2), a conforming state (§21.6, `[R-GEO-02]`). Give it
tile extents (8192, 16384) and a 4-byte sample type, so the
declaration-derived decoded tile size P·Q = 512 MiB. That product is
computed and range-checked in an empty layer — L2 lists "P·Q" and "P·Bᶜ"
among the layer-access overflow checks, and §17.2's Note says so in
terms: "`[R-ENC-04]`'s overflow rule carries no such quantifier ... so
P·Q and P·Bᶜ are checked in an empty layer even though this cap is not."

Under the untouched sentence, that layer's *declarations* exceed what a
256 MiB reader can serve, and the reader MAY decline at layer scope.
Under the new paragraph, the file "contain[s] none of a kind", so it does
not exceed row 6 "whatever its declarations would derive", every quantity
lies within the table, and a reader that declines on that ground "is not
a conforming reader (`[R-CNF-03]`)". The same reader is licensed by one
sentence and branded nonconforming by the next. Finding A-07 — and this
one moves verdicts on a real file, so I mark it byte-level.

`[R-CNF-10]` restates the duty ("MUST accept any conforming file within
the minimum guarantees stated in §21's limits table") and `[R-CNF-03]`
phrases it as "none of whose **values** exceeds the minimum guarantees" —
a derived 512 MiB tile size is a value the file has, computed at layer
access. Both restatements read against the new paragraph, not with it.

### 2.4 Check 2 — citations in the new paragraph

**§11.2** — cited for "a layer addressing no tile (§11.2)". §11.2 defines
Gᵢ = ⌈Eᵢ/Tᵢ⌉, N = ∏Gᵢ, and the addressed-tile count as N or C·N. It
never states that a layer may address none; the empty-layer *rule* is
`[R-GEO-02]` and §21.6, which is what §17.2's Note cites for the same
proposition ("a layer that addresses none — any dimension extent 0
(`[R-GEO-02]`, §21.6)"). Verdict: **resolves, weakly** — the arithmetic
supports the inference, but the repair cites the arithmetic where the
document elsewhere cites the rule.

**`[R-COD-07]`** — cited for "exactly as `[R-COD-07]`'s cap is quantified
over a layer's *addressed* tiles". The normative text at line 2325 reads
"Writers MUST NOT declare this codec for a layer any of whose **addressed
tiles'** decoded size exceeds 0x7E000000 bytes". Verdict: **resolves** —
and importantly the word "addressed" is in the normative sentence, not
only in the Note. But see A-09: the *inference* the repair draws — that a
layer addressing none is therefore unbounded — is drawn from the `>`
Note, and that same Note states the opposite convention for the sibling
rule over the identical quantity.

**`[R-CNF-03]`, §21.6** appear in the untouched sentences; read, and
§21.6's table does list exactly two capability refusals plus the other
non-violation entries, so the untouched "the two capability refusals
§21.6 names" is not disturbed by this repair.

### 2.5 Check 5 — exhaustive claims in the new paragraph

- "**The last three** rows" / "**The first five**" — 3 + 5 = 8 = the
  table's data rows. **Passes.**
- "declarations, which **every** file and **every** layer carries" —
  fails for "layers per file" (no such declaration exists) and is
  vacuously inapplicable for rows 1–3 in a zero-layer file, which is the
  same "contains none of a kind" vacuity the paragraph reserves for the
  last three. Finding A-08.
- "**whatever** its declarations would derive" — this is the strong
  clause and it is what collides with the untouched sentence. A-07.

### 2.6 Does the paragraph make a register row unreachable or a total wrong?

No. §21.1 says in terms: "The subsections after §21.5 are not part of the
register and carry no rows: neither this completeness clause nor the
instance arithmetic below reaches §21.6's defined non-violations, §21.7's
account of what no check detects, or §21.9's limits." §21.9's rows are
guarantees, not validity conditions, so no §21.2–§21.5 row depends on
them; my count above confirms 121/273 unchanged. Appendix B's summary
line ("Reader minimum guarantees | rank 32 · C 4096 · entry_count 2³² ·
65,536 layers · 16 MiB directory region · 256 MiB decoded tile · 16 MiB
metadata document · 8 MiB zstd window | §21.9") restates only the
numbers, carries no quantifier, and needs no sweep. `[R-VEC-03]`'s
sentence about exercising §21.9's guarantees is likewise unaffected.

### 2.7 Check 3 — normative placement

The new paragraph is plain prose, no `>`. It carries no requirement tag
of its own and sits between `[R-ERR-03]`'s tag (which trails the sentence
above the table) and `[R-ERR-04]`'s. By this document's trailing-tag
convention it is `[R-ERR-04]` text, which is where it belongs
substantively. The table itself already floats the same way, so this is a
pre-existing convention and not a defect of the repair. **Passes.**

---

## 3. Findings

A-01 hunk 1 LOCAL_CONTRADICTION — R3/R4 routing dilemma.
A-02 hunk 1 OVERCLAIM — "the one header quantity that is not left to the reader".
A-03 hunk 1 UNDERSHOT — single-segment frames make the 16 MiB document guarantee unrelyable above 8 MiB.
A-04 hunk 1 UNDERSHOT — the anti-allocation half of `[R-COD-06]` was not transposed.
A-05 hunk 1 NEW_AMBIGUITY — the new condition is detectable only by a reader whose bound is large enough to finish, against `[R-CNF-04]`'s flat detection duty.
A-06 hunk 1 UNSWEPT_RESTATEMENT — no register instance anywhere; 121/273 verified unchanged.
A-07 hunk 2 LOCAL_CONTRADICTION — the per-instance quantifier for the tile row against the untouched "narrowest scope whose declarations exceed" sentence. **Byte-level.**
A-08 hunk 2 OVERCLAIM — "declarations, which every file and every layer carries" is false for the layers-per-file row.
A-09 hunk 2 NEW_AMBIGUITY — the `[R-COD-07]` parallel does not hold in both directions.

Checks run and passed with nothing to report: check 3 (normative
placement) on both hunks; check 1 (tense and quantifier) on both hunks;
`[R-CNF-02]` and `[R-COD-07]` citations resolve.
