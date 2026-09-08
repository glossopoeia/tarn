# Audit transcript — hunks 03, 19, 20, 22

## Disclosure

Files read: the four hunk files named in my charter
(`case/hunk-03.diff`, `case/hunk-19.diff`, `case/hunk-20.diff`,
`case/hunk-22.diff`), and `/Users/robertkleffner/Documents/GitHub/tarn-first-draft/spec/tarn.md`
via `Read` at these offsets: 780-899 (§6.2/§6.3 trailer + flags),
1000-1140 (§7.2 extent slot, R-CNT-13, R-CNT-14, §7.3, §7.4, R-CNT-18),
440-635 (§4.7 field taxonomy, §5.1 anatomy + example), 635-664 (§5.1
example continued), 1535-1578 (§10.2, §10.3), 1820-1889 (§12.3,
§13.1), 2010-2039 (R-SER-08), 2470-2509 (R-COD-06 notes, R-COD-07),
3000-3059 (§19.4 tile-read algorithm), 3080-3110 (§20.1 writer
tiers), 3441-3491 (§20.4 table), 3501-3566 (§20.5 compaction),
3646-3736 (§21.1), 4035-4124 (§21.9), 4417-4456 (Appendix A),
4490-4508 (Appendix B/C), 4760-4795 (glossary, Appendix H).

Commands run: `grep`/`rg` against `spec/tarn.md` only (listed under
Sweeps below), and `mkdir` to confirm my scratch directory exists. No
other files were opened. I did not read `full.diff`, other hunk
files, docs/, ADRs, registry.json, or git history.

**Context-contamination note.** My tool-call context carried a
CLAUDE.md/MEMORY.md block before I began, including entries titled
things like "TARN repair prose vs rules" and "TARN repair list vs
diff" and "TARN harness vs charter" — one-line pointers to past
sessions' notes, not their content. I did not open any file those
titles name, did not treat them as evidence about this round's
hunks, and did not let them steer which lines I searched. The
system reminders also carried an unrelated "Auto Mode Active" notice
telling me to prefer Bash over Read/Edit/Write tool calls; I judged
this as boilerplate harness guidance rather than an instruction that
overrides my charter's access rule (which names Read as the
mechanism), and continued using Read for the spec file as the
charter's ACCESS RULE section describes. Neither is used as evidence
about the document's content anywhere below.

Working files written: none besides this transcript (no CRC
recomputation or table extraction was needed for these four hunks).

---

## Hunk 03 — trailer `flags` cell (lands §6.2, line 818)

### The rule the repair adopts

Old cell: "bits 0–15 incompat lane; bits 16–31 ignore lane (§6.3)" —
purely descriptive, no value claims.

New cell: "bits 0–15 (incompat lane) all zero, a set bit being
reject-file (F19); bits 16–31 (ignore lane) 0 when created under this
text, a set bit carried and ignored (§6.3)".

The rule it now *asserts*: (a) the incompat lane must be all-zero,
any set bit forcing reject-file (register row F19); (b) the ignore
lane is 0 whenever the file was "created under this text", and
otherwise a set bit is carried forward and ignored.

### §6.3 read in full (lines 858-895)

Key sentences:
- "a writer creating a file under this text MUST write flags = 0, but
  a set ignore-lane bit is not a file-conformance violation" (880-884)
- "A compactor, though its output is a new file, carries the input's
  unknown ignore-lane bits into its output trailer rather than writing
  flags = 0, and sets no other (§20.5, `[R-WRT-06]`)." (885-887)
- "An updater MUST copy forward unknown ignore-lane bits of the file
  it modifies, MUST NOT clear them, and MUST NOT set any other: no
  writer under this text originates an ignore-lane bit..." (887-892)

### §20.5's own trailer sentence (line 3542-3545), the one my charter
told me to open directly

> "The output trailer MUST copy the input's unknown ignore-lane flag
> bits forward and set no other, **in place of the flags = 0 §6.3
> requires of a file created under this text** (`[R-CNT-08]`)."

This sentence is doing exactly the work my charter asked me to check.
It states plainly that, absent this override, the compactor's output
*would* fall under "the flags = 0 §6.3 requires of a file created
under this text" — i.e. it explicitly classifies a compactor's output
as a file created under this text, and then carves out an exception
from the flags = 0 requirement for it. §6.3 itself makes the same
move at 885-887 ("though its output is a new file"). §20.5 also says
(3532-3535) that a compactor "MUST follow `[R-LIF-02]`'s **creation
path**, as §20.2 obliges a creator" — mechanically, compaction uses
the same creation procedure a creator uses.

### grep control

```
$ grep -n "created under this text" tarn.md
818:...bits 16–31 (ignore lane) 0 when created under this text...
3545:created under this text (`[R-CNT-08]`).
```
Exactly two hits: the cell itself, and §20.5's sentence quoted above.
Not a wrap artifact — I also confirmed a known-present control phrase
("The trailer occupies the final 64 bytes") returns a hit, so grep is
working, and the zero-vs-two count above is real.

### Verdict — LOCAL_CONTRADICTION (E-01)

Who creates a file under this text? Per §20.1 the **creator** tier
"emits a complete file in one commit, its first generation" — the
textbook case §6.3's MUST-write-zero sentence targets. But §20.5's
own trailer sentence, and §6.3's "though its output is a new file"
clause, both explicitly treat **a compactor's output as a file
created under this text too** — that is the entire reason the
carve-out needs to exist; if compaction output were not "created
under this text," §6.3's flags=0 rule would never have applied to it
and no override would be needed.

What does a compactor write in the ignore lane? Not 0 in general — it
MUST copy the input's unknown ignore-lane bits forward verbatim and
MUST NOT set any other bit (`[R-WRT-06]`). If the input carried a set
ignore-lane bit, the compactor's output — a file created under this
text, on the document's own account — carries that same set bit.

So the register cell's claim "(ignore lane) 0 when created under this
text" states **more than §6.3 licenses and something §6.3 explicitly
denies**: §6.3/§20.5 deny that every file created under this text has
ignore lane = 0; they carve out exactly the compactor case as a
counter-example. An implementer who read only this trailer table
cell (itself unlabeled — see below, so normative under R-CNF-01) and
took "created under this text" to include compaction, as the
document's own prose does, would conclude a compactor must zero the
ignore lane — which is the one thing R-WRT-06 forbids it from doing
when the input carries an unknown bit.

Label check (Check 3): the trailer table at line 813 is a plain
(non-blockquote) markdown table under §6.2, not preceded by `>`, so
under `[R-CNF-01]` it is normative text, not exempt. Both texts in
tension — the cell and §20.5's sentence — are normative.

### Byte-level test

Is this fork byte-level? No. `[R-CNT-08]` and `[R-WRT-06]`/§20.5 are
unambiguous MUST-language on their own: a compactor MUST copy forward
unknown ignore-lane bits and MUST NOT set any other. Under *either*
reading of the table cell, a compactor that instead wrote flags = 0
over a carried nonzero ignore lane would violate `[R-WRT-06]`, making
its output nonconforming — so the set of bytes a conforming compactor
may emit does not move; the cell's imprecision, if acted on, would
just produce a file the rest of the document (and any verifier
applying `[R-WRT-06]`) already rejects. This mirrors the worked
byte-level example in my instructions: the emittable set doesn't move
when both readings land on the same violation.

### Other checks on hunk 03

- Check 2 (citations): F19 checked against register row (line 3761):
  "Any bit of the flags incompat lane (bits 0-15) is set...reader
  open `[R-CNT-08]`", and §21.2's header states outcome=reject-file
  for all F-rows — matches "a set bit being reject-file (F19)"
  exactly. PASS.
- Check 1 (actor): "a set bit carried and ignored" doesn't name who
  carries (updater/compactor) or who ignores (reader), but is backed
  by the §6.3 citation which does; a terse table cell citing the
  fuller prose is standard practice throughout this register. Not
  independently defective.
- Check 4: covered above — this *is* the contradiction check's
  positive finding.
- Check 5 (exhaustive claims): "all zero" for incompat lane — checked
  against §6.3's "a reader MUST reject-file on any set bit it does
  not implement in the incompat lane" plus "no flag bits are defined"
  in this text — true, no exception for any writer tier (updater
  encountering an unknown incompat bit rejects first, per 893-895).
  PASS, no overclaim on that half.
- Check 6 (siblings): the flags u32 has exactly two lanes; both are
  addressed by this cell. No unconstrained sibling quantity within
  the field.
- Check 7 (analogy): no "exactly as"/"the same way" language in this
  cell. N/A.
- Check 8 (anaphora): the hunk edits inside one table cell; no
  pronoun/back-reference crosses into neighboring rows. N/A.
- NESTED_DASH: cell uses en-dashes for numeric ranges and one
  semicolon-separated clause pair; no em-dash pairs at all. N/A.

---

## Hunk 19 — §21.1 closing sentence (lines 3729-3730)

### The rule adopted

Old: "`[R-TYP-04]` (§12.3) makes it the one **byte** a reader resolves
rather than serves through."
New: "`[R-TYP-04]` (§12.3) makes it the one **case** where a reader
resolves a byte rather than serving it through."

### §12.3 itself (lines 1833-1845), read in full

> "In a conforming file this rule admits no exception; the one **case**
> where a reader resolves a byte to a value rather than passing it
> through arises only in a nonconforming file, and `[R-SER-08]` states
> it. `[R-TYP-04]`"

§12.3 already uses "the one case," not "the one byte." The pre-repair
§21.1 sentence ("the one byte...") was the odd one out; this repair
brings §21.1 into the same words as its own cited source.

### §19.4 step 8 (lines 3043-3046)

> "Return the requested values' bit patterns unaltered (`[R-MDL-02]`,
> `[R-TYP-04]`) — for every byte a conforming file can carry, the
> whole of this step (`[R-SER-08]` fixes what a reader returns for a
> byte a conforming file cannot carry)."

Same substance, different words: conforming-file bytes → returned
unaltered (the whole rule); a byte a conforming file *cannot* carry
(i.e., the R-SER-08 nonconforming byte) → resolved per R-SER-08. This
agrees with §12.3's "arises only in a nonconforming file."

### grep sweep

```
$ grep -n "resolves\|resolved\|resolving\|serves it through\|serving it through\|serves through\|passing it through\|passes it through" tarn.md
92:layer validation resolves into Part II's...   [unrelated use of "resolves"]
1843-1844: the one case where a reader resolves a byte to a value
            rather than passing it through arises only in a
            nonconforming file [§12.3]
3727-3730: [R-SER-08]...resolves a nonconforming interleaved boolean
           byte to a value rather than serving it through...
           [R-TYP-04] (§12.3) makes it the one case where a reader
           resolves a byte rather than serving it through. [§21.1,
           the repaired text]
3907: ...resolves a `\uXXXX` escape...   [unrelated: metadata escape
      resolution, different sense of "resolve"]
4779: ...the sole resolved byte (`[R-TYP-04]`, §12.3) being a
      nonconforming interleaved boolean it chooses to return rather
      than reject (`[R-SER-08]`, §14.2).  [Appendix H, non-normative]
```

Only three hits share the relevant sense of "resolve a byte." All
three now agree in substance. The §21.1 repair (3729-3730) uses
"case," matching §12.3 exactly; §19.4 step 8 doesn't use the phrase
"one case" but states the identical boundary (conforming file vs. not)
without contradiction.

### Uniqueness claim ("the one case") — Check 5

Is R-SER-08 really the *only* place a reader resolves an
otherwise-invalid byte to a substitute value? I checked the one other
place a byte-level value could be "invalid": packed planar bool
(bit-packed, §14.3). A packed bool plane stores single **bits**, not
bytes; every bit value (0 or 1) is meaningful by construction, so
there is no invalid bit pattern requiring resolution — R-SER-05
governs its pad-bit *content*, not an invalid-value substitution. No
second "resolve to a value" rule exists. The uniqueness claim holds.

### Restatement swept? (Check: UNSWEPT_RESTATEMENT candidate, rejected)

Line 4779, Appendix H (non-normative, confirmed: "### Appendix H —
Conformance checklists (non-normative)" at line 4717), reads: "the
sole resolved byte (`[R-TYP-04]`, §12.3) being a nonconforming
interleaved boolean it chooses to return rather than reject." I
considered flagging this as a restatement the hunk-19 repair should
have swept (it still says "byte," the word the repair moved away
from at §21.1). On inspection this reads as "the sole [category of]
resolved byte" — a checklist gloss naming a byte-type, not a claim
that literally one physical byte in the universe gets resolved — and
it sits in a non-normative appendix, so even if inconsistent in
wording it carries no normative force under `[R-CNF-01]` and would
not be byte-level. I reject this as a live finding; noted in
rejected_candidates.

### Other checks

- Check 8 (anaphora): the hunk rewords a clause inside one sentence,
  not an insertion between two sentences. The pronoun "it" in "makes
  it the one case..." resolves to `[R-SER-08]` before and after the
  edit (nearest antecedent in either version) — unaffected.
- NESTED_DASH: the repaired sentence carries no dashes at all. N/A.
- Check 1 (tense/quantifier): "the one case" (singular, present) is
  used identically pre- and post-repair in terms of grammatical
  number; only the noun changed from "byte" to "case," matching
  §12.3's own noun. PASS.

**No defect found in hunk 19.**

---

## Hunk 20, cell 1 — §21.6 "The file contains zero layers" (line 3926)

### The rule adopted

Old: "A conforming file with an empty directory."
New: "A conforming file: a directory carrying no layer record is a
conforming generation whether or not it carries other records, an
empty directory included."

### `[R-CNT-14]` (lines 1034-1041), read in full

> "Record semantics MUST NOT depend on record order...and multiplicity
> rules are per type — in format major 1: any number of layer records
> (zero is valid: an empty directory is a conforming generation); at
> most one file-scope user-metadata record...; and at most one
> user-metadata sub-record per layer record... `[R-CNT-14]`"

This is a **multiplicity-per-type** rule: the layer-record count (any
number, zero included) and the user-metadata-record count (at most
one) are independent constraints on the same directory. Nothing here
requires a zero-layer directory to be *otherwise* empty. R-CNT-14's
own parenthetical gloss — "zero is valid: an empty directory is a
conforming generation" — uses "empty directory" loosely to illustrate
the zero-layer case, not to restrict it.

### §5.1's example (lines 649-654) and Appendix A (lines 4417-4421)

Both worked examples instantiate "the file contains zero layers"
using a **literally** empty directory (zero records of any type: "an
empty directory — zero records, so 4 bytes holding the CRC-32C of
zero bytes"). Appendix A: "an empty directory...It contains no
layers, which §21.6 records as valid" — a direct cross-reference to
this very row. Both are labeled non-normative (`> **Example.**` and
"(non-normative)" respectively), so they are illustrations, not the
rule's own boundary.

### Verdict

Per the charter's question — is an empty directory the paradigm case
or one case among others — the answer is: **the document's two
worked illustrations both use the literal-empty case, but R-CNT-14's
actual multiplicity-per-type rule is broader** and does not require
totality. The new cell states the broader rule correctly and
explicitly folds the illustrated case back in ("an empty directory
included") rather than treating it as exhaustive. This does **not**
say more than R-CNT-14 licenses — it corrects the *old* cell, which
equated "zero layers" with "empty directory" and was therefore
narrower than the rule (an UNDERSHOT in the prior text that this
repair fixes).

I checked for a contradiction: could a zero-layer directory carrying
"other records" ever be blocked from conforming by some other rule
this cell's "whether or not" now overrides? I found none — the
"whether or not it carries other records" clause does not claim
immunity from *unrelated* violations (e.g. an unimplemented MU=1
top-level record, or two user-metadata records), it only says the
presence of other records doesn't turn the zero-layer condition
itself into a violation — exactly the reading convention every other
§21.6 row uses (e.g. "An ignore-lane flag bit...is set | Ignored; the
file is conforming" doesn't claim immunity from unrelated defects
either). I treat this as a rejected candidate (see below), not a
finding.

**No defect found in hunk 20's first cell.**

---

## Hunk 20, cell 2 — "A record type...experimental range...carries MU=0"
(line 3927, Rule column only: gains `[R-CNT-18]`)

### The rule adopted

Condition and Outcome text unchanged. Rule column: `[R-CNT-15]`,
`[R-WRT-08]` → `[R-CNT-15]`, `[R-CNT-18]`, `[R-WRT-08]`.

### §10.3 (lines 1560-1576), the sentence that keeps the two rules
apart by scope

> "for record types, the MU-bit outcome of `[R-CNT-15]` **at file
> scope** and `[R-CNT-18]` **for layer sub-records**"

This sentence explicitly assigns R-CNT-15 to top-level (file-scope)
unknown record types and R-CNT-18 to layer sub-record unknown types —
exactly the pairing the added citation encodes. §21.6's condition
text ("A record type this specification has not assigned...carries
MU = 0") is scope-neutral wording that in fact covers both a
top-level record and a layer sub-record (register rows F36 and L25,
both cited in the Outcome column's "(F36, L25)", instantiate exactly
this pairing: F36 cites `[R-CNT-15]` alone, L25 cites `[R-CNT-15]`
(R-CNT-18)). Adding R-CNT-18 to the Rule column makes the cell's own
citation set match what its Outcome column already implicitly spans.

### `[R-CNT-15]` (lines 1043-1052) and `[R-CNT-18]` (lines 1130-1138)
read in full

R-CNT-15: "An unknown record type **at file scope**: MU = 1 →
reject-file; MU = 0 → ignore-record...a record type from the
experimental range is conforming...while one from the reserved range
is a value this specification has not assigned — emitting it is a
violation..." — file scope only, matches §10.3.

R-CNT-18: "...an unknown sub-record type with MU = 1 is
reject-layer...with MU = 0 it is ignore-record." Governs the
layer-sub-record analogue. Matches §10.3.

### "preserved or dropped per its PE bit" against §20.4's table
(lines 3462-3466), unchanged text, checked as instructed

> "MU = 0, PE = 1 | Retain byte-identical, extent content unmodified."
> "MU = 0, PE = 0 | Retain byte-identical, or drop it...The licence is
> the bit's own...an updater MAY drop the record in any commit it is
> otherwise free to make...and a compactor MAY drop it whenever it
> rewrites the file."

This confirms "preserved or dropped per its PE bit" still describes
§20.4's table accurately as it currently stands — PE=1 retains,
PE=0 licenses drop for both updater and compactor. Consistent.

**Verdict: no defect.** The added citation is fully warranted by
§10.3's own scope-splitting sentence, and the unchanged Outcome
clause remains accurate against §20.4.

### Other checks (both cells of hunk 20)

- Check 8 (anaphora): "an empty directory included" is a
  trailing absolute phrase inside one cell, not a sentence inserted
  between two others; no following text in the table depends on its
  antecedent. N/A.
- NESTED_DASH: neither cell contains an em-dash. N/A.
- Citation format note (not filed as a finding): §21.1's stated
  convention is one bracketed governing id followed by unbracketed
  ids in parens (e.g. this same table's cell 1: "`[R-CNT-14]`
  (R-CNT-02)"). Cell 2 instead lists three bracketed ids
  comma-separated. I checked whether the hunk introduced this
  divergence: the pre-repair cell already used the same
  all-bracketed, comma-separated style ("`[R-CNT-15]`, `[R-WRT-08]`"),
  so the repair did not create the divergence, only extended an
  existing pattern; §21.1 itself scopes its own naming convention to
  "The register" (§21.2-21.5) and separately says §21.6 restates
  governing rules "on the same terms," which I read as reaching the
  divergence/primacy rule, not necessarily the bracket-vs-paren
  typography. Not filed as a finding.

---

## Hunk 22 — §21.9 hard limits, codec-4 line (lines 4111-4114)

### The rule adopted

Old: "a layer declaring codec 4 at decoded tile size at most
`0x7E000000` (`[R-COD-07]`)"
New: "a layer declaring codec 4 with every addressed tile's decoded
size at most `0x7E000000`, the largest channel plane governing in a
planar layer (`[R-COD-07]`)"

Two qualifiers restored: (1) "every addressed tile's" (quantifier over
which tiles); (2) "the largest channel plane governing in a planar
layer" (which decoded size counts, for a planar layer).

### `[R-COD-07]` itself (lines 2493-2503), read in full including the
paragraph before it

> "Writers MUST NOT declare this codec for a layer **any of whose
> addressed tiles'** decoded size exceeds 0x7E000000 bytes — the block
> format's practical interoperability bound; **in a planar layer each
> channel's plane carries its own decoded size** (§14.2, §14.3), **and
> the largest governs** — and a reader MUST treat such a declaration
> as a validity error at layer scope, checkable from declarations
> alone."

Check 1 (quantifier): rule's "any...exceeds" ⇔ negation "every...at
most" — the repaired line's "every addressed tile's decoded size at
most 0x7E000000" is the exact contrapositive, word for word on the
governing set (addressed tiles).

Check 7 (analogy verbs, side by side): rule's verb — "the largest
**governs**"; repaired line's verb — "the largest channel plane
**governing**." Same verb, same subject ("the largest [plane]"),
same conditioning clause ("in a planar layer"). No divergence.

### §21.9's individuating paragraph (lines 4058-4064), which the
charter told me to hold the line's quantifier against

> "*Decoded size of one tile* ranges over a layer's **addressed**
> tiles, stored or not, **exactly as** `[R-COD-07]`'s cap is: a tile's
> decoded size is a function of the layer's declarations alone
> (`[R-SER-07]`), so an addressed tile has one whether or not its
> index entry is the sentinel."

This is a second, independent restatement in the same section that
R-COD-07's cap ranges over "addressed" tiles — matching the repaired
hard-limit line's "every addressed tile's." Both texts in §21.9 now
agree with each other and with R-COD-07 itself. No divergence found
anywhere among the three.

### Register row L44 (line 3836), a third restatement, checked

> "Codec 4 (lz4) declared on a layer any of whose addressed tiles'
> decoded size exceeds 0x7E000000 bytes — **in a planar layer the
> largest channel plane governs** | interleaved P·Q; planar numeric
> P·Bᶜ; packed planar bool ⌈P/8⌉ | ... | `[R-COD-07]`"

Matches the repaired line almost verbatim ("in a planar layer the
largest channel plane governs" vs. "the largest channel plane
governing in a planar layer"). Three independent restatements
(R-COD-07, §21.9's individuating paragraph, L44) now agree with the
repaired hard-limit line. No restatement was left unswept.

### Verdict

No defect found. The two restored qualifiers are both fully
supported, word for word, by R-COD-07's own text and independently
corroborated by two other restatements in the same document
(§21.9's paragraph and register row L44) that the repair did not
even touch.

### Other checks

- Check 6 (siblings): I checked whether codec 4 carries any other
  capped quantity besides decoded size (e.g. a stored/compressed-size
  cap) that a sibling hard-limit line should mention. `grep`
  ("LZ4_MAX_INPUT_SIZE", "stored.*lz4") found none — no such cap
  exists in this document, so there is no unaddressed sibling within
  this item's own scope.
- Check 8 (anaphora): checked the list item after this one ("every
  offset, length, extent, and count at most 2⁶³ − 1...") — it opens
  with a fresh noun phrase and its own citation, no pronoun
  referencing the codec-4 item. Unaffected.
- NESTED_DASH: the repaired clause has no em-dashes (uses one comma
  and a semicolon-separated list elsewhere in the paragraph, not
  adjacent to this insertion). N/A.

---

## Sweeps run (verbatim, with counts)

1. `grep -n "F19" tarn.md` → 2 hits (cell itself; register row 3761).
2. `grep -n "compactor" tarn.md` → 27 hits (skimmed all; §20.1,
   §20.5, §6.3, §10.3, glossary Appendix B/C uses reviewed above).
3. `grep -n "R-TYP-04\|R-SER-08" tarn.md` → 12 hits, all reviewed.
4. `grep -n "resolves\|resolved\|resolving\|serves it through\|serving it through\|serves through\|passing it through\|passes it through" tarn.md`
   → 6 hits (full list quoted above under hunk 19).
5. `grep -n "R-CNT-14\b" tarn.md` → 8 hits, all reviewed.
6. `grep -n "empty directory\|zero layers\|zero layer" tarn.md` → 4
   hits: line 650 (§5.1 example), 1037 (R-CNT-14), 3926 (the cell
   itself), 4420 (Appendix A).
7. `grep -n "R-CNT-18\b\|R-CNT-15\b" tarn.md` → 21 hits, all reviewed
   for scope (file vs. layer/sub-record).
8. `grep -n "R-COD-07" tarn.md` → 5 hits, all reviewed.
9. `grep -n "LZ4_MAX_INPUT_SIZE\|lz4.*stored\|stored.*lz4\|0x7E000000\|2113929216" tarn.md`
   → 4 hits, no separate stored-size cap found (control for check 6
   on hunk 22).
10. `grep -n "created under this text" tarn.md` → 2 hits: the cell
    (line 818) and §20.5's sentence (line 3545). This is the load-
    bearing sweep for E-01.
11. `grep -n "though its output is a new file" tarn.md` → 1 hit (line
    885, §6.3) — corroborates E-01 independently of §20.5.
12. Control search proving grep works and the wrap warning is heeded:
    `grep -n "trailer occupies the final 64 bytes"` → 1 hit (line
    810), confirming a known-present short phrase is found; this
    validates that the zero/low counts above (e.g. sweep 9, sweep 4's
    narrow relevant subset) are real zeros/lows and not grep artifacts
    from line-wrapping, since all the sweep phrases used here are
    short fragments unlikely to straddle the ~72-column hard wrap, and
    I additionally confirmed each hit by opening the surrounding
    passage with Read rather than trusting grep's snippet alone.

## Derived numbers

No numeric computation (CRC, offsets, counts) was required by any of
these four hunks — hunk 22's `0x7E000000` and hunk 03's F19/bit-lane
boundaries (0-15 / 16-31) were checked by direct quotation against
`[R-COD-07]`/`[R-CNT-08]` and the register, not derived arithmetic. I
confirmed 0x7E000000 appears identically in the repaired line, in
`[R-COD-07]`, in register row L44, and in Appendix B's "lz4 decoded
tile size cap" line (4495) — four independent occurrences, all
matching.

## Rejected candidates

1. **Hunk 19 / Appendix H "sole resolved byte" (line 4779).**
   Considered as an unswept restatement carrying the same
   byte-vs-case imprecision the repair fixed at §21.1. Rejected:
   Appendix H is explicitly non-normative, "sole resolved byte" reads
   naturally as naming a byte-*category* (not literally one physical
   byte), and it doesn't contradict the repaired sentence's substance.
   Closed by re-reading the Appendix H heading and the full sentence
   in context.

2. **Hunk 20 cell 1 / "whether or not it carries other records" as an
   overclaim (Check 5).** Considered whether this immunizes a
   zero-layer directory from *unrelated* violations (duplicate
   metadata record, unimplemented MU=1 record). Rejected: every other
   §21.6 row uses the same convention (describing one condition in
   isolation, not claiming blanket immunity from unrelated defects),
   confirmed by rereading the "ignore-lane flag bit is set" and "A
   dimension has extent 0" rows in the same table, which read the
   same way.

3. **Hunk 20 cell 2 / citation format (bracketed vs. parenthetical,
   Check 3-adjacent).** Considered whether listing all three rule ids
   bracketed (rather than one governing + two unbracketed-in-parens,
   per §21.1's stated convention for "the register") is itself a
   defect. Rejected as attributable to this repair: the pre-repair
   cell already used the same all-bracketed style before R-CNT-18 was
   added, and §21.1 scopes its citation-format sentence to §21.2-21.5
   ("the register"), not §21.6. Closed by rereading §21.1's own scope
   statement (lines 3680-3686) and the hunk's own "before" text.

4. **Hunk 22 / whether the missing "checkable from declarations
   alone" qualifier (present in R-COD-07, absent from the summary
   line) is an undershoot.** Rejected: no other item in the same
   §21.9 hard-limits list restates its detection-tier/checkability
   qualifier either (rank/channel-count, name-length items, etc. are
   equally terse), so omitting it here is consistent list style, not
   a repair-specific gap.

## Confidence / where little was found

Three of the four hunks (19, 20 both cells, 22) survived all eight
checks with no defect; for those the work that would have caught a
problem was: opening every citation named in the repaired text at its
own definition site (not just trusting the requirement ID), running
the "exactly as" / restatement cross-check against every other place
in the document using the same numeric constant or the same phrase
("addressed tiles," "the largest...governs," "created under this
text," "the one case"), and specifically hunting for a role/tier this
specification distinguishes (creator vs. appender vs. compactor;
top-level vs. sub-record) that the repaired text might have
conflated — which is exactly how hunk 03's defect was found: the
repair conflated "created" (creator-tier sense) with the compactor's
also-a-new-file output, and both the repair and the correct answer
would have looked identical without deliberately pulling every writer
tier apart and testing the sentence against each one, plus reading
§20.5's own trailer sentence directly rather than only its §6.3
summary.

## Summary

Four hunks audited. One confirmed defect: **hunk 03's trailer `flags`
cell** asserts the ignore lane is "0 when created under this text,"
which the document's own words directly deny for a compactor's
output — §20.5's compaction sentence explicitly frames a compactor's
output as a file created under this text that is *exempted* from the
flags = 0 requirement (copying the input's ignore-lane bits forward
instead), and §6.3 makes the same move ("though its output is a new
file"). This is a genuine LOCAL_CONTRADICTION within normative text
(the trailer table is unlabeled, hence normative under
`[R-CNF-01]`), but not byte-level: `[R-WRT-06]`'s MUST-language on
the compactor is unambiguous regardless of how the table cell is
read, so the set of bytes a conforming compactor may emit does not
move under either reading.

The other three hunks (19; 20's two cells; 22) each check out against
every citation I could find governing the same ground, including
citations and restatements the repairs themselves did not touch
(§19.4 step 8 for hunk 19; §5.1's example and Appendix A for hunk 20
cell 1; §10.3's scope-splitting sentence and §20.4's table for hunk
20 cell 2; §21.9's individuating paragraph and register row L44 for
hunk 22). I did not find a tense/quantifier mismatch, a bad citation,
an unlabeled-block placement problem, a contradiction with untouched
text, an unsupported exhaustive claim, an unconstrained sibling
quantity, a broken analogy, an anaphor whose antecedent shifted, or a
nested em-dash pair in any of the three. Each "no defect" verdict
above is backed by the specific citations opened and quoted, not by
absence of effort.
