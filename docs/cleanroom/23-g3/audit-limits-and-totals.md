# Repair audit — hunks 3 and 4 (§21.8 total; §21.9 limits-table quantifier)

Auditor working transcript. Written for someone who wants to re-run every step.

---

## 0. Disclosure

**Read:**
- `/private/tmp/.../r23audit/hunk-03.diff` (my charter)
- `/private/tmp/.../r23audit/hunk-04.diff` (my charter)
- `/Users/robertkleffner/Documents/GitHub/tarn/spec/tarn.md` — read in pieces:
  lines 44–53, 116–140, 150–215, 271–280, 618–695, 868–900, 1000–1060,
  1465–1540, 1742–1790, 1821–1890, 1900–1930, 2011–2032, 2255–2300, 2300–2360,
  2437–2530, 3295–3380, 3374–3554 (all four register tables, via a saved dump),
  3520–3556, 3554–3608, 3560–3740, 3731–3760, 3932–4016, 4155–4180, 4333–4404.

**Ran (all against `spec/tarn.md` only, plus local arithmetic on extracted rows):**
- `grep -n '^#\{2,\} ' spec/tarn.md` — section index.
- `grep -n '273\|277\|121 \|conditions over\|instance' spec/tarn.md`
- `grep -n 'R-COD-07\|R-SER-07\|R-ERR-03\|R-ERR-04\|R-ERR-05\|R-CNF-03' spec/tarn.md`
- `grep -n 'R-MTA-09\|R-MTA-10\|R-MTA-03' spec/tarn.md`
- `grep -n 'actually contains\|per-instance\|minimum guarantee\|256 MiB\|16 MiB\|8 MiB\|4096\|65,536\|2³²' spec/tarn.md`
- `grep -n 'guarantee' spec/tarn.md`
- Row extraction + instance arithmetic (see §1 below), writing only to my own
  scratchpad (`rows.txt`, `inst.txt`).

**Did NOT read:** `full.diff`, hunks 1 and 2, `docs/`, `PLAN.md`,
`OPEN-QUESTIONS.md`, `AGENTS.md`, `README.md`, `conformance/`,
`spec/registry.json`, git history, the web. I did not list the r23audit
directory (I opened the two files my charter named by exact path).

**Context I did not ask for — disclosed breach.** Before I began, my runtime
placed in context: (a) the project `CLAUDE.md` pointer, (b) an index of the
maintainer's private memory files with one-line summaries, and (c) a git status
block including the subject lines of the five most recent commits. Item (c) is
material: two of those subject lines describe, in outline, the very repairs in
hunks 3 and 4 — one naming the arithmetic change behind the count, one naming
the §21.9 quantifier split. I did not treat any of it as evidence. Everything I
assert below was established from `spec/tarn.md` alone: the instance total is a
mechanical recount I ran myself over the extracted table cells, and every
quantifier comparison quotes the rule text I opened. Where the pre-placed
material could have suggested a conclusion (e.g. "the tile row is quantified
over addressed tiles"), I checked it against `[R-COD-07]`'s and `[R-SER-07]`'s
actual words rather than accepting it. But it appeared, I read it, and this
audit is not cleanroom on that axis.

---

## 1. Hunk 3 — §21.8, "121 conditions over 273 instances" → "277 instances"

### 1.0 The rule the repair adopts

An implementation-facing restatement: the conformance corpus (§24) must contain,
for **every** row of §21.2–§21.5, at least one vector per **instance** the row's
Instances cell enumerates, each vector's expected outcome being that row's
outcome. The repaired numbers are a *claim about the rest of the document*:
that those four tables presently hold 121 rows and that their Instances cells
presently enumerate 277 instances. Nothing about which bytes are legal turns on
the numerals; what turns on them is whether the sentence is a true census.

### 1.1 The count — what I counted and how

§21.1 states the counting rule I applied, verbatim:

> "Instances within a cell are separated by semicolons, and a cell reading — is
> one instance; the count is therefore mechanical once the cell is written."

So: rows = data rows of the four register tables; instances = semicolon-split
parts of column 3, with `—` counting 1.

Extraction (§21.2 begins at line 3374, §21.6 at 3554):

```
awk 'NR>=3374 && NR<3554' spec/tarn.md | grep '^| ' | grep -v '^| # ' > rows.txt
awk -F'|' '{print NF}' rows.txt | sort | uniq -c
   121 8
```

Every row splits into exactly 8 pipe-delimited fields, i.e. the 6 columns are
uniform and no cell contains a stray `|`. Field 4 is Instances.

```
awk -F'|' '{id=$2;gsub(/^ +| +$/,"",id); inst=$4;gsub(/^ +| +$/,"",inst);
            n=split(inst,a,";"); printf "%s\t%d\t%s\n",id,n,inst}' rows.txt \
 | awk -F'\t' '{s+=$2} END {print "TOTAL INSTANCES:",s,"ROWS:",NR}'
TOTAL INSTANCES: 277 ROWS: 121
```

Per family:

```
F rows=36 instances=58
L rows=49 instances=116
T rows=26 instances=55
R rows=10 instances=48
```

36 + 49 + 26 + 10 = **121**. 58 + 116 + 55 + 48 = **277**.

Cross-check against the counts the four subsections state in their own prose:
- §21.2 line 3376: "Outcome: reject-file. **36 conditions**." ✓ (F rows = 36)
- §21.3 line 3432: "**49 conditions**." ✓ (L rows = 49)
- §21.4 line 3489: "**26 conditions**." ✓ (T rows = 26)
- §21.5 line 3539: "**10 conditions**." ✓ (R rows = 10)

I checked the four tables are the only tables in the range: `grep '^| # '`
returned exactly four header rows, so no fifth table sneaked into the span, and
no register row lives outside a table.

I also hand-inspected every Instances cell (`inst.txt`) for semicolons used as
punctuation rather than as separators, since that would inflate the mechanical
count. The suspicious cells:
- `L2` — contains parenthetical asides ("which dominates the max disk ordinal
  (C−1)·N + (N−1)") but no semicolon inside them: 9 parts, 9 instances.
- `T15` — parentheticals with commas only: 2 parts.
- `T26` — uses colons inside parts and semicolons between: 3 parts, and §21.1's
  layout axis rule ("the layout formulas are materially different shapes and the
  cell enumerates them") says 3 is right.
- `F1` — has a semicolon in the *Condition* cell, which is column 2 and not
  counted.
No cell miscounts. **277 is correct as the document now stands.**

Because the delta is +4 and `R4` is the cell whose arithmetic is most fragile, I
audited it independently. `R4` = 16 instances = 8 alternatives × 2 containers
(top-level extent / layer sub-record extent). The 8 alternatives are: missing
frame magic; skippable frame; second frame; nonzero dictionary ID;
content-checksum flag set; bytes remaining after the frame; content-size
declared **larger** than the decoded length; content-size declared **smaller**.
Two directions for the content-size mismatch is exactly what §21.1 prescribes:

> "Where the condition compares two **magnitudes** either of which can be the
> greater — a *differs from* or *does not equal* — the two directions are
> likewise enumerated."

and §18.2 states the constraint as an equality ("when present it MUST equal the
byte length of the decoded document"), i.e. a not-equal in either direction. So
2 directions, not 1. I then walked `[R-COD-06]`'s frame constraints (lines
2270–2296) against R4's enumeration to check the alternative list is closed:
magic ✓, skippable ✓, second frame ✓, dictionary ID ✓, content-checksum ✓;
`[R-COD-06]`'s window-size and declared-decoded-size constraints are the two
§18.2 expressly *replaces* ("save two: what it states against a tile's declared
decoded size, and what it states about the frame's declared `Window_Size`"), so
they correctly do not appear; the "MUST NOT allocate from the declared length"
clause is a reader obligation, not a file condition; and §18.2's own
"occupying the extent's bytes before its terminal CRC" is R4's "bytes remaining
after the frame". List is closed at 8. R4 = 16 stands.

### 1.2 Check 1 — tense and quantifier

Generation: the sentence speaks about the document's present tables, not a prior
state. There is no prior/new-state axis here; the census is of the text.

Set: "**Every row** of §21.2 through §21.5" and "**one vector per instance**".
The rule it restates is §24's `[R-VEC-03]` (line 3990):

> "every register row has at least one vector for each instance it names"

Repair: "has at least one conformance vector (§24) whose expected outcome is
that row's outcome, and one vector per instance."
`[R-VEC-03]`: "every register row has at least one vector for each instance".
Same set (register rows), same granularity (per instance), same floor ("at
least one"). ✓ The upstream definition of *instance* is §21.1's ("the row is the
rule, and each instance is one file"), which is what I counted. ✓

The one wording gap I noticed — §21.8's bare "one vector per instance" against
§24's "at least one vector for each instance" — is in text the hunk did not
touch, is naturally read as a floor given the same sentence's leading "at least
one", and §21.1 makes the rule govern over a restatement anyway. Not reported.

### 1.3 Check 2 — citations

| Citation in repaired text | Opened | Verdict |
|---|---|---|
| §21.2 | line 3374, "File-scope violations", 36 rows | ✓ is a register subsection |
| §21.5 | line 3520, "Ignored records", 10 rows | ✓ is the last register subsection |
| §21.2 **through** §21.5 as the register's span | §21.1 line 3299: "The register — §21.2 through §21.5 (`[R-ERR-02]`)" | ✓ identical span |
| §24 | line 3932, "Conformance Test Vectors" | ✓ is the corpus section; `[R-VEC-03]` there states the matching coverage duty |
| `[R-ERR-02]` | the identifier closing §21.8's paragraph; §21.1 cites the same id for the register's extent | ✓ consistent; the repaired paragraph **is** part of `[R-ERR-02]` |

All five resolve and say what the sentence needs them to say.

### 1.4 Check 3 — does the repair sit in normative text

Line 3664 is plain prose in §21.8, no leading `>`. The paragraph terminates in
`[R-ERR-02]`. The restatement in §24 (`[R-VEC-03]`, line 3985ff) is likewise
plain prose. Neither statement of the coverage rule lives only in a blockquote.
✓ No `[R-CNF-01]` failure.

### 1.5 Check 4 — contradiction in the same passage, including untouched text

I read §21.1 (3297–3372) in full, §21.7 (3608–3660), §21.8, and §21.9's opening.
Looking specifically for a carve-out the new number collides with:

§21.1 contains the carve-out, and it *supports* the repair rather than
colliding with it:

> "The subsections after §21.5 are not part of the register and carry no rows:
> neither this completeness clause nor the instance arithmetic below reaches
> §21.6's defined non-violations, §21.7's account of what no check detects, or
> §21.9's limits."

I verified §21.6 mechanically cannot contribute: its table is three columns
(`|---|---|---|` at line 3560), i.e. it has no Instances column at all, and 16
lines beginning `|` including header and separator. So the 277 could not have
been meant to include it. ✓

§21.7 is prose with no rows. ✓ §21.9's table is a guarantees table, not a
register table, and carries no Instances column. ✓

No sentence in §21.8's neighbourhood was written to be true only under 273. I
grepped the whole document for `273` — zero hits outside nothing; and for `277`
— exactly one hit, line 3664. No stale duplicate of the old total survives
anywhere (Appendix B line 4100 restates the §21.9 limits, not the register
census; Appendix E's changelog carries no counts; Appendix H carries no counts).

### 1.6 Check 5 — exhaustive claims

Words promising completeness in the repaired sentence: "**Every** row",
"**121** conditions", "**277** instances", "**one** vector per instance".

- "Every row of §21.2 through §21.5" — falsification attempt: is there a
  register row outside those four tables, or a table row the sentence's span
  misses? No: `grep '^| # '` over 3374–3554 finds exactly four table headers,
  and §21.1 fixes the register's span at §21.2–§21.5. ✓
- "121" — recounted: 36+49+26+10 = 121. ✓
- "277" — recounted mechanically under §21.1's own rule: 277. ✓
- "one vector per instance" — matches `[R-VEC-03]`. ✓

Both directions of the coverage claim hold: everything it says is covered
(121 rows, all four subsections) and nothing it wrongly omits (§21.6/§21.7/§21.9
are excluded by §21.1's explicit clause, and §24's *additional* corpus duties —
sentinels, boundary values, `[R-ERR-05]`'s hard limits, §21.9's guarantees —
are stated in §24 and never claimed by §21.8).

### 1.7 Check 6 — what the repair leaves unconstrained

Structure governed: the census sentence over the four register tables. Its
carriable quantities are (a) the row count, (b) the instance count, (c) the
per-row outcome match, (d) the per-instance vector floor. All four are named and
all four check out. The per-subsection counts (36/49/26/10) are stated
separately in §21.2–§21.5 and are the sibling quantities most likely to go stale
when a row is added; I verified all four are still consistent with the tables
and with the new total. Nothing in this structure is left unpinned.

### 1.8 Check 7 — analogy

The repaired text contains no "exactly as / the same way / following / likewise"
construction. Its only warrant-by-pointer is the parenthetical "(§24)", which is
a cross-reference, not an analogy. Check 7 has no subject here. For
completeness I compared the two governing verbs anyway:
§21.8 "**has** at least one conformance vector … and one vector per instance"
vs §24 `[R-VEC-03]` "every register row **has** at least one vector for each
instance it names". Same verb, same set. ✓

### Hunk 3 verdict

Clean. No finding. The total is arithmetically correct against the document as
it now stands, the citations resolve, the text is normative, the claim holds in
both directions, and no stale copy of the old total survives.

---

## 2. Hunk 4 — §21.9, the per-instance paragraph after the limits table

### 2.0 The rule the repair adopts

For each of the eight rows of the minimum-guarantee table, the paragraph fixes
*what set the row's quantity is instantiated over*, which in turn fixes when a
file "exceeds" a row and therefore when `[R-CNF-03]`'s duty to accept lapses:

- Rows 1–5 (rank d, C, entry_count, layers per file, dir_length): one quantity
  per file or per layer, always present, so there is never an "absent" case.
- Row 6 (decoded size of one tile): one quantity per **addressed** tile of a
  layer, whether or not that tile is stored. A layer that addresses no tile has
  no instance; a layer all of whose entries are sentinels *does* have instances.
- Rows 7–8 (decoded metadata-document size, zstd `Window_Size`): one quantity
  per document / per compressed frame the file contains as stored bytes. No
  stored instance, no quantity.

What it makes true of an implementation: a reader may decline a file whose
all-sentinel layer *declares* a 512 MiB decoded tile size, and may **not**
decline (on the guarantee ground) a zero-extent layer that declares the same,
and may not decline a file that stores no oversized metadata document however
large its declarations would allow one to be.

### 2.1 The partition, row by row — counted

The table (lines 3682–3690) has exactly **8** rows:

| # | Row | Paragraph puts it | Correct? |
|---|---|---|---|
| 1 | rank d of a layer — 32 | declarations | ✓ §7.4: `rank d`, `u8`, `≥ 1`, a fixed field of every layer record |
| 2 | channels per layer, C — 4096 | declarations | ✓ §7.4: `channel count C`, `u16`, `≥ 1`, fixed field |
| 3 | addressed tiles per layer (entry_count) — 2³² | declarations | ✓ **this is the "zero rather than absent" row** — see below |
| 4 | layers per file — 65,536 | declarations | ✓ derived from the live directory's record sequence; a file with zero layers has the value 0 (§21.6: "The file contains zero layers \| A conforming file with an empty directory") |
| 5 | size of the directory region, dir_length — 16 MiB | declarations | ✓ trailer field, every file carries one |
| 6 | decoded size of one tile — 256 MiB | per-instance, over **addressed** tiles | ✓ see §2.2 |
| 7 | decoded size of one user-metadata document — 16 MiB | per-instance, over documents contained | ✓ §7.1: "Each user-metadata record carries its document in its extent — never inline"; a document exists only as stored bytes |
| 8 | zstd frame `Window_Size` — 8 MiB | per-instance, over frames contained | ✓ a frame header field; exists only in stored bytes (a sentinel tile has no frame) |

5 + 3 = 8. The partition is exhaustive and disjoint, and the paragraph's
"last three" / "first five" line up with the table's physical order. ✓

**The zero-rather-than-absent row.** `entry_count` (row 3) is the count that is
zero rather than absent: §7.4 lists `entry_count | u64 | equals the addressed-tile
count`, an unconditional fixed field, and §11.1 says "at Eᵢ = 0 the grid count is
0 and the layer addresses no tile". So an empty layer still *declares*
entry_count = 0. The paragraph puts it on the declarations side, which is right —
had it been placed with the per-instance rows, the "a file containing no
instance of a kind does not exceed that row" carve-out would have been offered
for a quantity that is never absent, which would be harmless but wrong; had
row 3's quantity been treated as absent in an empty layer, the row would have
gone unreachable for exactly the files §21.6 registers as conforming. Correctly
placed. (Row 4, "layers per file", is the same shape at file scope and is
likewise on the declarations side, correctly.)

**Is any row's side genuinely arguable?** Row 4 is the closest call: "layers per
file" is not a *named field* anywhere — there is no layer-count field in the
trailer or the directory header — so calling it a "declaration" stretches the
word slightly. But the property the paragraph needs is that the quantity exists
for every file (0 when there are no layers) and is derivable without reading
payload bytes, which holds: the count comes from parsing the live directory's
record sequence, and §14.2 already licenses "declaration-derived quantities" for
things computed rather than stored. Not a defect; noted and dismissed.

Row 8 is the second-closest call, because "compressed frames" is broader than
"zstd frames" — codec 2 is a raw DEFLATE *stream* and codec 4 an LZ4 *block*,
neither of which has a `Window_Size`. The row label itself says "zstd frame
`Window_Size`", so the intersection is exact and no reader is misled. Noted and
dismissed.

### 2.2 Check 7 — the analogy, verb against verb (the check for this hunk)

The paragraph justifies itself by pointing at another rule exactly once, and
that pointer covers exactly **one** row. I checked which rows the analogy
sentence covers before comparing verbs, because the defect this check exists for
was one analogy stretched across several differently-individuated rows.

**Sentence A (covers row 6 only):**
> "*Decoded size of one tile* ranges over a layer's **addressed** tiles, stored
> or not, exactly as `[R-COD-07]`'s cap is"

| | governing words |
|---|---|
| repair | "**ranges over a layer's addressed tiles, stored or not**" |
| `[R-COD-07]` (line 2321) | "Writers MUST NOT declare this codec for **a layer any of whose addressed tiles' decoded size exceeds** 0x7E000000 bytes … and a reader MUST treat such a declaration as a validity error at layer scope, checkable from declarations alone." |

Same set: *a layer's addressed tiles*, in both. Same quantity: *decoded size of
a tile*, in both. Same indifference to storage: `[R-COD-07]` is "checkable from
declarations alone", and its Note (line 2331) confirms the empty-layer half —
"The cap is quantified over the layer's *addressed* tiles, so a layer that
addresses none — any dimension extent 0 (`[R-GEO-02]`, §21.6) — satisfies it
whatever its tile shape declares". The analogy **passes**, and both halves of the
repair's sentence point the same way, which is what the previous wording failed
at.

I also checked the per-layer *unit* matches, since a mismatch there would be
invisible: in a planar layer `[R-COD-07]` says "each channel's plane carries its
own decoded size (§14.2, §14.3), and the largest governs", and §11.2 makes the
addressed-tile count `C · N` for planar — one addressed tile *is* one plane. So
"decoded size of one tile" over addressed tiles individuates per plane in planar
layers under both the repair and `[R-COD-07]`. ✓ (Corroborated by T3/T14's
instance cells, which enumerate "planar numeric P·Bᶜ" as a distinct shape.)

**Sentence B (covers row 6's second half):**
> "a tile's decoded size is a function of the layer's declarations alone
> (`[R-SER-07]`), so an addressed tile has one whether or not its index entry is
> the sentinel."

| | governing words |
|---|---|
| repair | "a tile's decoded size **is a function of the layer's declarations alone**" |
| `[R-SER-07]` (line 1917) | "decoded size **is a function of the layer's declarations alone** — geometry, layout, and channel types — never of payload content" |

Verbatim match on the borrowed clause. ✓ I checked the one way this could still
fail: `[R-SER-07]`'s *own* obligation ("a reader MUST treat a decoded payload
whose byte length is not exactly that decoded size as a validity error at tile
scope") ranges over **stored** tiles only — a sentinel tile has no decoded
payload. So the repair borrows a definitional clause from a rule whose
obligation is narrower than the repair's set. That is legitimate here, because
the derivation itself is stated independently of storage in §14.2 `[R-SER-02]`
("the decoded size" = P·Bᶜ or P·Q, from P, Bᶜ, Q, all declared), and the repair
borrows only the derivation, not the obligation. ✓ Passes, but this is the seam
worth naming: the warrant's obligation and the repair's set do not coincide.

**No analogy for rows 7 and 8.** "The other two range over the user-metadata
documents and compressed frames a file actually contains, neither of which
exists except as stored bytes" cites nothing and argues from nothing. So the
one-sentence-many-rows shape that survived the previous round is gone: the
analogy now carries exactly one row. ✓ That is the substance of the repair and
it lands.

### 2.3 Check 1 — tense and quantifier

*Which generation?* This is where I found the residue. The repair pinned the
generation axis for row 6 and left it open for rows 7 and 8.

Row 6 is safe: "a layer's addressed tiles" — a *layer* is a live-directory
record, so the tiles are the live state's addressed tiles, and "stored or not"
disposes of the stored/unstored axis explicitly.

Rows 7–8 say "the user-metadata documents and compressed frames a file
**actually contains**, neither of which exists except as **stored bytes**". §5.2
`[R-CNT-02]` defines the competing readings and makes them non-trivially
different:

> "Every byte the live state does not claim is **slack**: alignment and slab
> gaps, the pre-trailer pad, and **everything an earlier commit superseded**.
> Slack has no internal structure this specification defines, its content is
> unconstrained, and no conformance requirement applies to it."

A file that has been appended to several times physically contains superseded
user-metadata extents and superseded codec-3 tile payloads. Those are stored
bytes. Under a physical reading, a 100 MiB superseded metadata document makes
the file exceed row 7, `[R-CNF-03]`'s acceptance duty lapses for the *whole
file*, and a reader may decline it. Under the live-state reading it does not.
The paragraph — whose entire job is to state individuation precisely, and which
went to the trouble of writing "stored or not" for row 6 — never says "live" for
rows 7–8, and the gloss it adds ("exists … as stored bytes") is the phrase that
most invites the physical reading, since slack is stored bytes.

I then looked for the rule that closes it and found one: §5.2 also says a reader
"MUST NOT interpret" slack, so no conforming actor may measure a superseded
frame's `Window_Size` or a superseded document's decoded length in the first
place, and a verifier inherits every reader obligation (§2.3). Two competent
implementations therefore converge. So this is an unpinned quantifier, not a
fork — reported as **B-01**, byte_level false.

*Which set?* "a layer's addressed tiles" (row 6) vs "the … documents and …
frames a file actually contains" (rows 7–8) vs "declarations, which every file
and every layer carries" (rows 1–5). Three sets, three rows-groups, each stated.
The one place the sets blur is the summary sentence — see §2.6 below (**B-02**).

### 2.4 Check 2 — citations

| Citation in repaired text | Opened | Verdict |
|---|---|---|
| `[R-COD-07]` | line 2316–2327 (§17.2, Codec 4 — lz4) | ✓ Its cap is quantified over "a layer any of whose **addressed** tiles' decoded size exceeds 0x7E000000", exactly as the repair claims. Its Note independently states the empty-layer consequence. |
| `[R-SER-07]` | line 1917–1923 (§14.3 tail) | ✓ States verbatim "decoded size is a function of the layer's declarations alone". |
| §11.2 (for "A layer addressing no tile") | line 1499–1511 | ✓ Defines the addressed-tile count as N (interleaved) / C·N (planar) from Gᵢ = ⌈Eᵢ/Tᵢ⌉, so Eᵢ = 0 ⇒ 0 addressed tiles. §11.1 cross-references it the same way: "at Eᵢ = 0 the grid count is 0 and the layer addresses no tile, §11.2". |
| `[R-CNF-03]` (in the untouched next paragraph) | line 157–172 | ✓ "A reader MUST accept every conforming file … none of whose values exceeds the minimum guarantees of §21's limits table (§21.9's `[R-ERR-04]` governs a refusal on that last ground)". Consistent with §21.9's "a file whose every quantity lies within the table". |
| §21.6 (for "the two capability refusals", untouched) | line 3583–3607 | ✓ §21.6's closing passage names exactly two: "**version_major naming a major this reader does not implement**" and "an **experimental-range top-level record type carrying MU = 1**". Two, not three. `[R-CNF-03]` itself says "§21.6's closing paragraph names the other two". ✓ |

All resolve. None "almost" says the claimed thing.

### 2.5 Check 3 — does the repair sit in normative text

Lines 3692–3706 carry no `>` prefix (`sed -n '3692,3712p' … | grep '^>'` returned
nothing). The paragraph sits between the table (which closes `[R-ERR-03]`'s
material) and the decline paragraph that terminates in `[R-ERR-04]`, so under
this document's convention — the identifier trailing the normative block it
labels (§2.2) — the paragraph is part of `[R-ERR-04]`. It is normative prose. ✓

Grepped the distinctive terms of the rule rather than its id
(`per-instance`, `actually contains`, `minimum guarantee`, `256 MiB`, `8 MiB`,
`guarantee`) across the whole document. Hits: line 3692/3700 (the repair
itself); §2.3 line 162 and §2.5 line 276 (both restate the acceptance duty
without any individuation claim, so nothing to sweep); §17.2 line 2293
(`[R-COD-06]`, see below); §18.2 lines 2469/2473/2476 (`[R-MTA-09]`) and the
blockquoted Note at 2503; §24 line 3993; Appendix B line 4100 (the values
restated, no quantifiers); Appendix H line 4352. **No competing statement of the
individuation rule exists in a blockquote-only position, and no normative
restatement elsewhere still says the old thing.** In particular §18.2's Note is
non-normative but agrees with the repair rather than contradicting it:
"a document having no declared size and so no narrower scope whose declarations
that rule can measure". ✓

### 2.6 Check 4 — contradiction in the same passage, including untouched text

I read §21.9 end to end (3669–3755): opening paragraph + `[R-ERR-03]`, the
table, the repaired paragraph, the decline paragraph + `[R-ERR-04]`, the
"where the numbers come from" Note, and the hard-limits paragraph + `[R-ERR-05]`.

**(a) The decline sentence, untouched, immediately below the repair.**

> "A file exceeding any of these remains conforming, and a reader MAY decline
> it — at the whole file, or at the narrowest scope whose **declarations**
> exceed what it can serve, a layer or a tile."

Set against the repair three lines above:

> "The other two range over the user-metadata documents and compressed frames a
> file actually contains, **neither of which exists except as stored bytes**."

The repair now asserts categorically that rows 7 and 8 are *not* declarations.
The decline sentence conditions the narrow-scope option on "declarations
exceed". For row 7 this is benign and is expressly reconciled in §18.2 (the
decline "does so at the whole file"). For **row 8 it collides with a normative
rule elsewhere**: `[R-COD-06]`, line 2293 —

> "Writers SHOULD keep the declared window within §21.9's 8 MiB `Window_Size`
> guarantee even for a larger tile; a wider window is conforming and merely
> permits a conforming reader to **decline the tile or the layer** on resource
> grounds (`[R-ERR-04]`)."

`[R-COD-06]` grants, under `[R-ERR-04]`'s own name, a tile- or layer-scope
decline on a quantity that `[R-ERR-04]`'s sentence can only reach through
"declarations", and the repaired paragraph now states flatly that this quantity
is not a declaration. Reported as **B-03**. It is not byte-level: both sentences
are permissions (MAY), and once *any* quantity of the file exceeds the table,
`[R-CNF-03]`'s acceptance duty has already lapsed for the whole file, so no
accept/reject verdict turns on the scope granularity. I record it because it is
precisely the "sentence written to be true only under the old wording" shape
the charter asks about, and because the repair's new categorical clause is what
makes it bite; the fix is one word in `[R-ERR-04]` ("declarations" →
"quantities", or an explicit third scope).

**(b) A carve-out the repair's new breadth collides with — checked, none found.**
The repair *widens* row 6 relative to the old text (from tiles a file contains
to tiles a layer addresses). The obvious collision candidate is `[R-GEO-02]`
line 1478: "Readers MUST accept such a layer" (a dimension with extent 0). The
repair does **not** collide with it, and is in fact drafted around it: a
zero-extent layer addresses no tile, so row 6 has no instance there and
`[R-CNF-03]`'s acceptance duty still runs. Had the repair put row 6 on the
declarations side, a reader could have declined a zero-extent layer with a large
declared tile shape and `[R-GEO-02]`'s MUST would have been violated. Checked
and clean. ✓

I also checked the widened case for a colliding MUST: an all-sentinel layer with
large declared tiles now *does* exceed row 6, so a reader MAY decline it.
`[R-TYP-08]` ("a reader **that returns** any of the tile's sample positions …
MUST return … fill") is conditional on returning, so it does not force service.
`[R-TYP-09]`/`[R-CNF-09]` bar returning fill for a *rejected* tile, which is a
different outcome from a resource decline. No collision. ✓

**(c) Did the widening overshoot?** I asked whether "addressed" is materially
right for a *reader-resource* floor, or whether the repair simply chose the
half of the old sentence that matched `[R-COD-07]`. It is materially right:
§13.3 `[R-TYP-08]` obliges a reader that serves an unstored tile's positions to
produce that channel's fill "at every such position", i.e. to materialize
decoded-size worth of output for a tile it never decodes. So the guarantee binds
the same buffer whether the tile is stored or sentinel. Not an overshoot. ✓

**(d) The hard-limits paragraph, same subsection, 40 lines below.** It restates
`[R-COD-07]` as "a layer declaring codec 4 at decoded tile size at most
`0x7E000000` (`[R-COD-07]`)" — with no "addressed tiles" quantifier, while the
repair three-quarters of a page above leans on precisely that quantifier. I
considered reporting this as an unswept restatement and decided against it: the
same subsection opens by disclaiming exactly this, "The hard limits it restates
are a finding aid rather than an inventory — each is normative where the
structure forcing it is defined", and §21.1's rule-governs principle applies.
Pre-existing, expressly disclaimed, and unchanged by the repair. Not reported.

### 2.7 Check 5 — exhaustive claims

Every completeness word in the repaired paragraph, with a falsification attempt:

- "**The last three** rows" — table has 8 rows (counted at 3683–3690); last
  three = rows 6, 7, 8. ✓
- "**The first five** rows" — rows 1–5; 5 + 3 = 8, no row unassigned, none
  double-assigned. ✓
- "declarations, which **every** file and **every** layer carries" — §7.4's
  field table makes `rank d`, `channel count C`, `entry_count` unconditional
  fixed fields of every layer record; §6.2's trailer makes `dir_length`
  unconditional; the layer count is derivable from every file's directory,
  including the zero-layer file §21.6 registers as conforming. ✓
- "a function of the layer's declarations **alone**" — matches `[R-SER-07]`
  word for word. ✓
- "whether or not its index entry is **the sentinel**" — §15.2 `[R-IDX-02]`
  makes sentinel/non-sentinel the exhaustive binary for an entry in a conforming
  file (malformed entries are §15.3 rejects, not a third state). ✓
- "**neither** of which exists except as stored bytes" — for documents, §7.1:
  "Each user-metadata record carries its document in its extent — **never
  inline**", so there is no declaration-derived document. For frames, a frame is
  a stored byte sequence by construction (§17.2, §18.2). ✓
- "**Either way** a file containing no instance of a kind does not exceed that
  row" — see **B-02**; the claim is true under the paragraph's own definition
  of *instance*, but "containing" is the wrong verb for row 6's set.
- "a file containing no instance of a kind does not exceed that row, **whatever
  its declarations would derive**" — true for rows 7 and 8. For row 6 it is only
  true in the layer-addresses-nothing case, which the preceding sentence has
  just carved out. ✓ under the intended reading.

### 2.8 Check 6 — what this structure still leaves unconstrained

Structure: the §21.9 minimum-guarantee table — eight rows, each a
(quantity, floor) pair, plus the individuation of each quantity, plus the scope
at which a decline on each may be taken.

| Row | quantity fixed? | individuation fixed? | decline scope fixed? |
|---|---|---|---|
| 1 rank d | ✓ §7.4 | ✓ per layer | ✓ layer |
| 2 C | ✓ §7.4 | ✓ per layer | ✓ layer |
| 3 entry_count | ✓ §7.4, `[R-CNT-17]` | ✓ per layer, 0 when empty | ✓ layer |
| 4 layers per file | ✓ live directory | ✓ per file | ✓ file |
| 5 dir_length | ✓ §6.2 trailer | ✓ per file | ✓ file |
| 6 decoded tile size | ✓ §14.2 `[R-SER-02]` | ✓ **addressed tiles, stored or not** | ✓ tile / layer |
| 7 document decoded size | ✓ §18.2 | ~ per contained document — **generation axis unstated** (B-01) | ✓ whole file (§18.2) |
| 8 zstd `Window_Size` | ✓ §17.2/§18.2 | ~ per contained frame — **generation axis unstated** (B-01) | ✗ **`[R-ERR-04]` reaches it only through "declarations"** (B-03) |

The repair pinned row 6's quantifier on both axes it could vary on (addressed
vs stored; which layer). Its two neighbours in the same "last three" group were
pinned on the stored/derived axis and left unpinned on the
live-state/superseded axis — the same header, the sibling quantity, invisible to
a check that only reads the words about row 6. That is B-01, and it is the shape
this check exists for. Row 8's decline scope is B-03.

One further sibling I checked and cleared: rows 7 and 8 are themselves
individuated differently from each other (documents vs frames), and the
paragraph's "The other two range over the user-metadata documents and compressed
frames" pairs them in table order, so each gets its own set rather than a shared
one. ✓ And row 8's set correctly spans both frame populations — codec-3 tile
payloads and encoding-2 metadata documents — since both are "compressed frames
a file contains"; `[R-COD-06]` and `[R-MTA-09]` govern them respectively and
neither contradicts the paragraph's set. ✓

### 2.9 Does the repair make any register row unreachable, or any stated total wrong?

No. §21.9 carries no register rows (§21.1: "The subsections after §21.5 are not
part of the register and carry no rows"), the repair touches no Instances cell,
and §21.8's 121/277 is unaffected — I recounted after reading the repair, and
the counts come from §21.2–§21.5 only. The only totals in §21.9 are the eight
table values, unchanged, and Appendix B line 4100 restates all eight identically
("rank 32 · C 4096 · entry_count 2³² · 65,536 layers · 16 MiB directory region ·
256 MiB decoded tile · 16 MiB metadata document · 8 MiB zstd window"). ✓

### Hunk 4 verdict

The core repair is sound and lands: the analogy now carries one row, the two
halves of that sentence point the same way, and the partition is exhaustive and
correct including the zero-rather-than-absent row. Three residual findings:
B-01 (generation axis unpinned for rows 7–8), B-02 (the summary sentence's verb),
B-03 (the untouched decline sentence's "declarations" against row 8 and
`[R-COD-06]`). None is byte-level.

---

## 3. Byte-level determinations

| Finding | Disputed file conforming? | Do two competent implementations differ on bytes or on an accept/reject verdict? |
|---|---|---|
| B-01 | Yes — a file carrying a superseded oversized metadata document or codec-3 payload in slack is conforming (§5.2: slack "content is unconstrained, and no conformance requirement applies to it") | **No.** §5.2 also says "A reader MUST NOT interpret it (§9.5)", and a verifier inherits every reader obligation (§2.3). Neither actor may lawfully measure the slack instance, so both readings converge on the live-state answer. |
| B-02 | Yes — a layer that addresses tiles, stores none, and declares a >256 MiB decoded tile size is conforming | **No.** Read alone, the summary sentence would fork the must-accept verdict (MUST accept under "contains = stored" vs MAY decline under "addressed"). But "stored or not" appears explicitly two sentences earlier and "A layer addressing no tile … therefore has no tile whose decoded size the table bounds" states the carve-out precisely; a competent implementation reading the paragraph cannot land on the other side. |
| B-03 | Yes — a file with a codec-3 tile whose frame declares a >8 MiB window is conforming (`[R-COD-06]`: "a wider window is conforming") | **No.** Both texts state permissions (MAY), and once any quantity exceeds the table `[R-CNF-03]`'s acceptance duty has lapsed for the whole file, so a reader that declines at tile scope and one that declines the whole file are both conforming under either reading. |

---

## 4. Summary of checks run

**Hunk 3:** checks 1–7 all run, all pass. Count independently verified twice
(per-family and total), against §21.1's own mechanical counting rule, and
cross-checked against the four per-subsection prose counts. No finding.

**Hunk 4:** checks 1–7 all run. Checks 2, 3, 5 pass outright. Check 7 — the
designated check — passes, with both verb pairs quoted. Check 1 yields B-01.
Check 4 yields B-03. Check 6 yields B-01 (and re-derives B-03). The
"new ambiguity" heading yields B-02.
