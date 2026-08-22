# R20 repair audit — hunks 01, 02, 03

Auditor working transcript. Verbatim record of what was opened, what was
grepped, what the output was, and what was concluded.

## 0. Disclosure

Read, in full or in the ranges named below:

- `/private/tmp/.../r20audit/hunk-01.diff`
- `/private/tmp/.../r20audit/hunk-02.diff`
- `/private/tmp/.../r20audit/hunk-03.diff`
- `/Users/robertkleffner/Documents/GitHub/tarn/spec/tarn.md` — ranges
  96–116, 116–134, 134–225, 225–280, 282–345, 785–830, 940–1000,
  1000–1075, 1368–1435, 2108–2210, 2648–2770, 2876–2895, 3010–3025,
  3096–3150, 3149–3275, 3274–3356, 3406–3415, 3497–3530, 3530–3640,
  3655–3695, 4296–4367.

Did NOT read: `full.diff`, any other hunk file, `docs/`, `PLAN.md`,
`OPEN-QUESTIONS.md`, `AGENTS.md`, `README.md`, `conformance/`,
`spec/registry.json`, git history, the web. Did not list the r20audit
directory. Ran only `wc`, `sed -n`, `grep`, `tr` against `spec/tarn.md`
and the three hunk files.

**Unasked-for context appeared in my context window before I began**: a
project instruction file (CLAUDE.md pointing at AGENTS.md), an index of
the maintainer's memory notes naming this project's cadence and prior
findings, and a task list naming this round. I did not open any of the
files those referred to and did not use their contents as evidence; every
conclusion below is anchored to a quoted passage of `spec/tarn.md`. I
disclose their appearance as the access rule requires.

---

## 1. The three repairs, stated as rules

**Hunk 1** — §7.4, `[R-CNT-18]`, line 1050–1052 of the current file.

Before: `an unknown sub-record type with MU = 1 is reject-layer — never
reject-file — and with MU = 0 is ignore-record.`
After: `an unknown sub-record type with MU = 1 is reject-layer, and a
reader MUST NOT reject the file for it; with MU = 0 it is
ignore-record.`

Rule adopted: for a sub-record of a layer record whose type the reader
does not implement, with MU = 1, the reader is *forbidden* — not merely
unassigned — to reject the whole file; it refuses the containing layer
only. The MU = 0 branch is unchanged in force (ignore-record).

**Hunk 2** — §20.5, `[R-WRT-07]`, line 3192.

Before: `A compactor preserves content but not placement — placement is
not among the things it carries forward, and it is free to place
structures anywhere §5.2 admits and every declared layout invariant
permits (…): every stored tile's bytes verbatim …`
After: `A compactor MUST preserve content, and preserves no placement —
placement is not among the things it carries forward, and it is free to
place structures anywhere §5.2 admits and every declared layout
invariant permits (…): every stored tile's bytes verbatim …`

Rule adopted: content preservation by a compactor is an obligation, and
its extension is the colon list — every stored tile's bytes verbatim,
each index entry's crc unchanged, and every *retained* record per §20.4,
minus the three enumerated relocation exceptions. Placement is not part
of it.

**Hunk 3** — §21.6 closing paragraph, lines 3561–3583.

Adds the qualifier **top-level** to the second of two "conforming files a
reader nevertheless refuses", and adds a sentence saying why the
qualifier matters, asserting that the same type as a layer sub-record is
reject-layer and never a ground to refuse the file (`[R-CNT-18]`).

Rule adopted: a conforming file carrying an experimental-range MU = 1
record is a file the reader refuses **only** when that record is
top-level; in a layer's sub-record sequence the same type costs the
reader that layer and nothing more.

Hunks 1 and 3 are the two halves of one rule, as the charter says: hunk 1
is the normative statement, hunk 3 the §21.6 restatement.

---

## 2. Check 3 first — does each repair sit in normative text?

§2.1 `[R-CNF-01]`, read at lines 105–107:

> All text in this document is normative except: §1 (Introduction); any
> text labeled *Note*, *Example*, or *Rationale*; and appendices
> identified as non-normative.

- Hunk 1 lands at line 1050–1052, mid-paragraph, tagged `[R-CNT-18]` at
  line 1056. No `>` prefix on any line of that paragraph (verified by
  `sed -n '1044,1058p'`). **Normative. PASS.**
- Hunk 2 lands at line 3192. No `>` prefix. The paragraph carries no ID
  of its own; the chain of three paragraphs from 3192 closes at line
  3225 with `` `[R-WRT-07]` ``, so the MUST belongs to `[R-WRT-07]`.
  **Normative. PASS.**
- Hunk 3 lands at 3561–3583, §21.6 prose, no `>` prefix. §21.6 is
  outside the register (§21.1: "The subsections after §21.5 are not part
  of the register and carry no rows") but it is not a Note/Example/
  Rationale, so it is normative text. It is additionally load-bearing by
  incorporation: `[R-CNF-03]` cites "§21.6's closing paragraph" as the
  place that names two of the three grounds on which a conforming reader
  may refuse a conforming file. **Normative. PASS.**

Grep confirming the old hunk-1 phrase is gone and the new one is the
only statement of the sub-record MU rule (whitespace-normalised, since
the file is hard-wrapped):

```
$ tr '\n' ' ' < spec/tarn.md | grep -o "unknown sub-record[^.]\{0,140\}"
unknown sub-record type with MU = 1 is reject-layer, and a reader MUST NOT reject the file for it; with MU = 0 it is ignore-record

$ tr '\n' ' ' < spec/tarn.md | grep -o "never reject-file[^.]\{0,100\}\|ground to refuse[^.]\{0,80\}"
ground to refuse the file (`[R-CNT-18]`), so only the top-level case is a file a reader refuses,
```

"never reject-file" no longer occurs. The repair landed; nothing states
the old rule.

```
$ tr '\n' ' ' < spec/tarn.md | grep -o "MUST NOT reject[^.;]\{0,120\}"
MUST NOT reject a file for its version_minor: …            (R-CNT-07)
MUST NOT reject the file for it                            (R-CNT-18, new)
MUST NOT reject a layer for its combination of layout and channel types  (R-SER-09)
MUST NOT reject the layer for the combination              (§21.6 row, R-SER-09)
```

Note the precedent this establishes: before this repair, every
"MUST NOT reject" in the document attached to a **defined
non-violation** — a version_minor a reader does not know, a bool/numeric
channel mix. The new one is the first that attaches to a condition that
can also be a *violation*. That observation drives finding A-01.

---

## 3. Hunk 1

### 3.1 Tense and quantifier

The rule ranges over "an unknown sub-record type with MU = 1". Two
things to pin down.

*Which set?* "unknown" = a type the consuming reader does not implement.
Confirmed against `[R-CNT-15]` (line 964–973):

> An unknown record type at file scope: MU = 1 → reject-file; MU = 0 →
> ignore-record. … Readers of both apply the MU rule above unchanged.

and against `[R-CNF-03]` (line 157–160): "carrying no record of a type
it does not implement with MUST_UNDERSTAND = 1". So "unknown" is
reader-relative, and the set includes both experimental-range types
(≥ 0x8000) and reserved-range types (0x0003–0x7FFF), since no reader
implements the latter. The register agrees: L24's Governing-rule cell
(line 3436) reads `` `[R-CNT-18]` (R-CNT-15) `` for *A layer record's
sub-record carries a reserved-range type value … with MUST_UNDERSTAND
… set to 1*. **So the new MUST NOT ranges over reserved-range
sub-records too.** Held for §3.4.

*Which generation / which actor?* Neither generation nor tense is at
issue here; the obligation is on "a reader", which is the right actor —
reject-file is a reader outcome (§2.4 `[R-CNF-07]`). PASS on actor.

*Does the quantifier match the rule it restates?* The repair IS the
normative rule; there is no other statement of it (grep above).

### 3.2 Both flag values still covered

Charter's specific worry. Before: one subject, two branches joined by
"and". After: `… with MU = 1 is reject-layer, and a reader MUST NOT
reject the file for it; with MU = 0 it is ignore-record.` Both branches
present, neither re-scoped in force: MU = 1 → reject-layer + the new
prohibition; MU = 0 → ignore-record. **No case dropped.**

But the sentence now reads, at top level:

`Sub-records are layer-scope records; a sub-record MUST NOT itself
contain records (…), and an unknown sub-record type with MU = 1 is
reject-layer, and a reader MUST NOT reject the file for it; with MU = 0
it is ignore-record.`

There are now two semicolons at the same rank in one sentence. The MU =
0 branch is punctuated as a third top-level clause, coordinate with
"Sub-records are layer-scope records", and its subject is the bare
pronoun "it", which must reach back past "the file", "records" and "a
sub-record" to "an unknown sub-record type". Before the repair the MU =
0 branch was an elliptical coordinate of the MU = 1 branch and needed no
pronoun. Recoverable — a file has no MU bit, so the wrong antecedent is
self-defeating — but degraded. Recorded as A-07.

### 3.3 Citations in the repaired sentence

None added. The surrounding sentence cites §7.3 ("A *known* type
appearing where §7.3's table does not scope it") — opened at lines
975–984; the table's Scope column reads `file (container for layer
scope)` for 0x0001 and `file when top-level; layer as sub-record` for
0x0002. The claim holds. **PASS.**

### 3.4 Contradiction in the same passage and elsewhere — A-01

§2.4 `[R-CNF-12]`, lines 253–262, opened in full:

> A file is conforming only if it satisfies every requirement at every
> scope: the outcome classes describe the blast radius of a violation
> for readers, never degrees of file conformance, and a verifier
> certifies only violation-free files. **For a nonconforming file no
> acceptance obligation exists — a reader MAY reject it upon detecting
> any violation, including violations whose assigned detector is the
> verifier.**

§21.3, L24 (line 3436), detector **reader**, detected at **layer
access**, governing rule **`[R-CNT-18]`**:

> | L24 | A layer record's sub-record carries a reserved-range type
> value (0x0003-0x7FFF, §10.2) with MUST_UNDERSTAND (flags bit 0) set to
> 1 | — | reader | layer access | `[R-CNT-18]` (R-CNT-15) |

A file exhibiting L24 is **nonconforming** — L25 makes emitting a
reserved-range value a violation, and §21.1 makes the register
"every detectable file-conformance violation this specification names".
So on that file:

- `[R-CNF-12]` says the reader **MAY** reject the whole file, on the
  strength of a violation it has itself detected;
- the repaired `[R-CNT-18]` says the reader **MUST NOT** reject the file
  for it.

Same actor, same condition, opposite modals. "for it" does not rescue
the MUST NOT: `[R-CNF-12]`'s licence is precisely a licence to reject
*for* the detected violation.

The old wording did not have this problem. "is reject-layer — never
reject-file —" was an *outcome-class assignment*, and `[R-CNF-12]`
expressly sits above outcome classes ("the outcome classes describe the
blast radius of a violation for readers, never degrees of file
conformance"). Turning the assignment into a prohibition on the reader
is what collides.

Note also the asymmetry the repair creates: F35 is the top-level twin of
L24, and there `[R-CNT-15]` and `[R-CNF-12]` agree (reject-file). Only
the sub-record side now carries a MUST NOT that `[R-CNF-12]` overrides
in the other direction. And L24 is not special — every one of §21.3's 49
reject-layer rows is a violation a reader MAY, per `[R-CNF-12]`, treat
as a whole-file refusal. The repair silently exempts one of them.

The case the repair actually needed — an **experimental**-range MU = 1
sub-record — is a *conforming* file (`[R-CNF-02]`: the §10.3 prohibition
"binds a writer's conduct, not the bytes"), so `[R-CNF-12]` grants
nothing there and the MUST NOT binds cleanly. The defect is that the
repair did not stop at that case. **Overshoot into nonconforming
files.** → A-01.

### 3.5 Exhaustive claims

"never" is gone; "MUST NOT" carries no completeness promise beyond the
scope discussed in A-01. Nothing else in the repaired clause promises
completeness. PASS apart from A-01.

### 3.6 Unswept restatements of the hunk-1 rule

```
$ tr '\n' ' ' < spec/tarn.md | grep -o ".\{90\}MU = 1.\{110\}" | grep -in "reject\|refus\|accept\|implement"
```
Ten hits, each opened:

| site | text | verdict |
|---|---|---|
| §7.2 `[R-CNT-15]` l.964 | "An unknown record type **at file scope**" | already position-qualified. PASS |
| §7.4 `[R-CNT-18]` l.1050 | the repair itself | — |
| §10.3 `[R-EXT-03]` l.1424 | "for record types, the MU-bit outcome of `[R-CNT-15]` **at file scope** and `[R-CNT-18]` **for layer sub-records**" | partitions the positions explicitly. PASS, and it is the best statement of the partition in the document |
| §19.1 step 4 l.2673 | "applying the MUST_UNDERSTAND gate for unknown **top-level** types (`[R-CNT-15]`)" | already qualified. PASS |
| §20.4 table, MU = 1 row l.3121 | "At layer scope an unknown critical record blocks modification of that layer, leaving other layers editable (`[R-CNT-18]`). At file scope … `[R-CNT-15]` makes an unimplemented **top-level** MU = 1 record reject-file" | already qualified, and already draws the same layer/file line. PASS |
| §20.5 `[R-WRT-06]` l.3190 | "MUST refuse to compact a file carrying **any** record whose type it does not implement with MU = 1" | unqualified as to position — but refusing to compact is not rejecting the file, and §2.3 makes a compactor a reader first only for reader obligations. No collision with the new MUST NOT. PASS |
| §21.6 closing l.3567 | hunk 3 | — |
| §21.9 `[R-ERR-04]` l.3672 | "the two capability refusals §21.6 names, a foreign format major and an **unimplemented MU = 1 type**" | unswept. → A-03 |
| App. H updater l.4340 | "rejects outright a file carrying an unimplemented **top-level** MU = 1 record" | already qualified, non-normative. PASS |
| §2.3 `[R-CNF-03]` l.157 | "carrying **no record** of a type it does not implement with MUST_UNDERSTAND = 1" | unqualified as to position. → A-02 |

Also checked `MUST_UNDERSTAND` occurrences whole-document
(`tr '\n' ' ' | grep -o ".\{80\}MUST_UNDERSTAND.\{100\}"`, 8 hits):
`[R-CNF-03]`, `[R-CNF-11]`, §7.2's header table, §19.1 step 4, F25, F35,
L24, L46. Of these only `[R-CNF-03]` states a refusal ground without a
position qualifier; `[R-CNF-11]`'s "when a record carries
MUST_UNDERSTAND = 1 with a type it does not implement (§21.6)" is a
*cannot establish* ground for a verifier, which is true at both
positions (the verifier cannot check the record's content rules either
way), so it needs no qualifier — PASS, though its §21.6 pointer now
lands on a paragraph that discusses only the top-level case as a file
refusal.

---

## 4. Hunk 2

### 4.1 Tense and quantifier — the list under the MUST

Read the whole §20.5 (lines 3149–3272) and §20.4 (3099–3148).

The list the MUST now governs: "every stored tile's bytes verbatim —
each index entry's crc is unchanged — and every retained record per
§20.4, except that relocation re-points extent slots, regenerates each
relocated tile-index region (entry offsets new; entry lengths, entry
crcs, and sentinel entries unchanged; segment CRCs recomputed over the
entries as re-emitted), and updates the layer-record fields covering a
regenerated region (crc_of_crc_array)."

*"every stored tile"* — which generation? §3.1 settles it, verbatim:

> **addressed tile / stored tile** — … A tile is *stored in a
> generation* if and only if that generation's tile-index entry for it
> is not the sentinel (§15); **unqualified *stored* means stored in the
> live generation.** Superseded payload bytes from earlier generations
> do not make a tile stored.

So the MUST ranges over the live committed state's tiles, not over
bytes any superseded generation once stored. That matters a great deal
now that this is an obligation, because the same subsection opens with
"A compactor's output contains only the structures reachable from the
input's live trailer … so slack is never carried". Had "stored" ranged
over the input file's history, the new MUST would have obliged the
compactor to carry slack forward and contradicted that opening
sentence. §3.1's definition forecloses it. **PASS — and this is the
check I expected to fail.**

*"every retained record per §20.4"* — "retained" is the word that keeps
the MUST off the records §20.4's MU = 0 / PE = 0 row lets a compactor
drop ("A compactor MAY drop it whenever it rewrites the file"). Checked
against §20.5's opening ("less any record §20.4 lets it drop") and
against §20.4's three-row table. **PASS: the MUST does not collide with
the drop licence.**

*Does "record" reach the record's extent bytes?* `[R-WRT-05]` defines
byte-identical re-emission over "header, inline payload, and extent
slot" — not extent content. But §20.4's MU = 0 / PE = 1 row says
"Retain byte-identical, **extent content unmodified**", and the list
says "per §20.4", which pulls that in. **PASS.**

### 4.2 Does the MUST reach the freedom clause?

Charter's specific worry: "A MUST that accidentally reaches the freedom
clause would forbid the thing the sentence exists to permit."

`A compactor MUST preserve content, and preserves no placement — …, and
it is free to place structures anywhere …`

The second conjunct's verb is the inflected indicative "preserves", not
a bare infinitive, so it cannot share the modal: "MUST preserve … and
preserves …" does not distribute. The freedom clause sits inside the
em-dash aside elaborating *placement*, two conjuncts away from the
modal. **The MUST does not reach the freedom clause. PASS.**

The colon list's distance from its head ("content") is unchanged by the
repair — the em-dash aside was already interposed in the "-" text — so
the repair did not worsen the attachment. PASS.

### 4.3 Exhaustive claims in the repaired text — A-06

Two completeness words, both new or newly strengthened.

**"preserves no placement".** The "-" text said "but not placement",
which reads as *is not obliged to preserve placement*. "preserves no
placement" is a flat universal in normative text (§2.1: all text is
normative unless labelled). Falsification attempt, from §16.2
`[R-SLB-03]`:

> When declared, for every run: the run's stored tiles are contiguous
> and packed in ordinal order — each stored tile's offset equals the
> previous stored tile's offset plus its length — and the first stored
> tile's offset satisfies offset mod A_slab = 0.

The compactor must honour that in its output (the repaired sentence
itself concedes "every declared layout invariant permits"). The
relative byte placement of a slab run's stored tiles is therefore
placement the output reproduces from the input — placement carried
forward. Same for §16.1 `[R-SLB-01]`'s offset mod A = 0. So "no
placement" is falsifiable from the very rules the same clause cites two
lines later. The old "but not placement" did not make the claim.

Second reading hazard: as a normative declarative, "preserves no
placement" can be read as *forbidding* the output from having the
input's placement — which would bar a compactor from emitting an
already-compact input unchanged in layout. The freedom clause ("free to
place structures anywhere §5.2 admits") disambiguates, so I do not
count this as byte-level, but it is a reading the old text did not
admit. → A-06.

**"(crc_of_crc_array)"** — a closed parenthetical, now under a MUST.
Falsification attempt: which layer-record fields cover a regenerated
tile-index region? From §7.4's table: `index_encoding` (unchanged),
`entry_count` (unchanged — the addressed-tile count does not move),
`crc_of_crc_array` (changes, since segment CRCs are recomputed over
new offsets). The extent slot is covered separately by "relocation
re-points extent slots". So the parenthetical is complete. **PASS.**

**"every stored tile's bytes verbatim"**, **"each index entry's crc is
unchanged"**, **"entry lengths, entry crcs, and sentinel entries
unchanged"** — all cross-checked against the following paragraph
("Regenerating a region means classifying every entry in it: a sentinel
is re-emitted unchanged, and every other entry is re-pointed…") and the
non-normative Example ("Every stored tile's bytes survive
byte-for-byte, as does every record extent but a relocated tile-index
region"). Consistent. **PASS.**

### 4.4 Contradiction hunt in the passage the repair landed in

Read §20.5 end to end and §20.3 step 4 and §16.2 `[R-SLB-04]`.

Candidate: `[R-SLB-04]` (line 2170–2176):

> A writer or updater whose commit changes the stored-tile set, the run
> partition, or the byte placement of any run of a slab-declared layer
> MUST either re-establish the invariants for every such run — or clear
> the declaration in the new generation.

A compactor changes byte placement, so it owes one of the two. Clearing
the declaration means writing S = 0 / A_slab = 0 into a layer record —
a layer-record change **not** in hunk 2's now-normative exception list,
so the new MUST forecloses it for compactors. Is that a contradiction?
No: re-establishing is always available to a compactor (it lays the file
out from scratch and the invariant is satisfiable at any run), so the
disjunction is satisfied by the surviving branch. A licence is narrowed,
not violated. **Checked; not reported.**

Candidate: `[R-WRT-09]`'s verification depth does not reach the slab
invariant (L41/L42 are verifier/certification rows), so a compactor can
compact an input whose slab invariant is broken without detecting it —
and must then produce output that satisfies it. Still satisfiable.
**Checked; not reported.**

Candidate: does the new MUST need a §21 register row? §21.1: the
register's completeness runs to "*detectable* file-conformance
violations". A compactor that alters content emits a well-formed file
carrying wrong bytes; §21.7's opening paragraph is exactly that class
("this format detects *corruption of structure*, not *incorrectness of
content*"). Also `[R-WRT-07]` already carried a witnessless MUST before
this repair ("The output's reference arrays MUST equal the live
generation's bit for bit"), and §21.7's second list does not name it
either, so that list is not held out as closed over `[R-WRT-07]`.
**Checked; not reported.**

### 4.5 Citations in the repaired line

- `[R-SLB-01]` — §16.1, "A layer MAY declare alignment A … When
  declared: every stored tile's offset satisfies offset mod A = 0." A
  declared layout invariant that constrains placement. **PASS.**
- `[R-SLB-03]` — §16.2, run contiguity and A_slab alignment. **PASS.**
- §5.2 — "Byte coverage" (heading confirmed at line 618). The clause
  says placement is free "anywhere §5.2 admits". **PASS.**
- §20.4 — "Re-emission and preservation" (heading at 3099), which is
  where retention and dropping are governed. **PASS.**

---

## 5. Hunk 3

### 5.1 Who designates this paragraph as authoritative, and does it still answer them

Grep for `21\.6` gave 20 hits; the three that designate authority:

1. **§2.3 `[R-CNF-03]`, line 157–164** — verbatim:

> - **Conforming reader.** A reader MUST accept every conforming file of
>   a format major version it implements, carrying no record of a type
>   it does not implement with MUST_UNDERSTAND = 1 — in a conforming
>   file such a type is necessarily from the experimental range, since
>   a reserved-range type carrying MU = 1 is itself a violation — and
>   none of whose values exceeds the minimum guarantees of §21's
>   limits table (§21.9's `[R-ERR-04]` governs a refusal on that last
>   ground; **§21.6's closing paragraph names the other two**),

This is the designation. It sends a reader to §21.6 to learn the two
non-resource grounds on which a conforming reader may refuse a
conforming file. Its own exclusion — "carrying **no record** of a type
it does not implement with MU = 1" — is unqualified as to position, and
its aside says such a type is "necessarily from the experimental range",
which is precisely the file hunk 3 now says a reader must not refuse. So
§21.6, as now written, answers a **narrower** question than
`[R-CNF-03]` sends the reader here to learn, and `[R-CNF-03]`'s
MUST-accept obligation still stops short of the file the repaired
`[R-CNT-18]` forbids rejecting. → A-02.

2. **§21.9 `[R-ERR-04]`, line 3670–3673** — "the two capability refusals
   §21.6 names, a foreign format major and an unimplemented MU = 1 type,
   are not this ground". A count claim plus an unqualified apposition,
   both now stale. → A-03.

3. **§2.3 `[R-CNF-11]`, line 198** — a verifier's *cannot establish*
   ground, correct at both positions. **PASS** (noted in §3.6).

### 5.2 The count in the opening sentence

> Two structural cases are **conforming files a reader nevertheless
> refuses**.

After the edit the paragraph still gives exactly two: version_major, and
the experimental-range **top-level** MU = 1 record. The later sentences
that depend on the count — "In both the outcome records a reader's
capability", "Neither is a register row" — still have two referents.
**Count PASS.**

But the paragraph now *names* a third capability refusal in passing (the
sub-record reject-layer). That is what falsifies `[R-ERR-04]`'s "the two
capability refusals §21.6 names". → A-03.

Also checked the closing sentence: "What is registered in each case is
the neighbouring condition that *is* a violation — version_major = 0 …
(F18, `[R-CNT-07]`), and a *reserved*-range type, whose emission
`[R-CNT-15]` does make a violation (F35, F36, L24, L25)." F35/F36 are
the top-level rows, L24/L25 the sub-record rows (opened at lines
3403–3404 and 3436–3437). The four-row citation is correct and, after
the edit, better justified than before, since the paragraph now
discusses both positions. **PASS.**

### 5.3 The added sentence's claim about the other position

> The qualifier is load-bearing — the same type as a layer sub-record is
> reject-layer and never a ground to refuse the file (`[R-CNT-18]`), so
> only the top-level case is a file a reader refuses, since the
> prohibition on publishing experimental values binds a writer's conduct
> and not the bytes.

**Do the two rules partition the positions with nothing in the gap?**
Where can a record appear? §7.3's Scope column: `file (container for
layer scope)` and `file when top-level; layer as sub-record`. §7.4:
"a sub-record MUST NOT itself contain records (nesting depth beyond two
is a validity error at layer scope)". So exactly two positions exist:
top-level in the directory, and sub-record of a layer record.
`[R-CNT-15]` governs the first ("An unknown record type **at file
scope**"), `[R-CNT-18]` the second. §10.3 `[R-EXT-03]` states the
partition outright: "for record types, the MU-bit outcome of
`[R-CNT-15]` at file scope and `[R-CNT-18]` for layer sub-records".
**Nothing falls in the gap. PASS — this is the strongest part of the
repair.**

**Is the claim itself true of the governing rule?** `[R-CNT-18]` says
"an **unknown** sub-record type with MU = 1 is reject-layer". The added
sentence drops "unknown". For a reader that *does* implement the
experimental type — the entire point of an experimental range being
private use — nothing is rejected at all. The first case in the same
paragraph spells the qualifier out ("a major **this reader does not
implement**"); the second and the new third do not. → A-05.

**The trailing "since" clause.** Before the repair the sentence ran
"… and `[R-CNF-02]` makes the file conforming all the same, **since the
prohibition on publishing experimental values binds a writer's conduct
and not the bytes**" — the causal clause explained the *conformance*
claim, and it is the correct explanation of it (`[R-CNF-02]`: "A few
obligations this specification places on writers govern their *conduct*
rather than their output … and a file is never nonconforming by virtue
of one"). The repair broke the sentence at "all the same." and left the
"since" clause dangling off the new claim "only the top-level case is a
file a reader refuses" — which it does not explain, and which it would
prove too much about if it did: the conduct/bytes distinction is equally
true of the top-level case, so as re-attached it argues that the
top-level case is not a file refusal either, contradicting the sentence
two lines above. Meanwhile `[R-CNF-02]`'s conformance claim lost its
stated justification. → A-04.

### 5.4 Citations in hunk 3

| citation | claim made | opened at | verdict |
|---|---|---|---|
| §10.2 | the experimental range for record types | l.1387–1412, table row `record type (§7.3) \| u16 \| 0x0001, 0x0002 \| 0x0003–0x7FFF \| ≥ 0x8000` | **PASS** |
| §10.3 | the prohibition on publishing experimental values | l.1412–1428, "Writers MUST NOT emit files carrying an experimental value in released software or published data" | **PASS** |
| `[R-CNT-07]` | "the reader rejects the file" for an unimplemented major | l.787–794, "A reader MUST reject-file when version_major is 0 (invalid) or is a major it does not implement" | **PASS** |
| `[R-CNT-15]` | "obliges the reader to reject" a top-level experimental MU = 1 | l.964, "An unknown record type at file scope: MU = 1 → reject-file" | **PASS**, modulo the elided "unknown" (A-05) |
| `[R-CNF-02]` | "makes the file conforming all the same" | l.146–156, conduct-vs-bytes | **PASS** |
| `[R-CNT-18]` | "the same type as a layer sub-record is reject-layer and never a ground to refuse the file" | l.1050–1056 | **PASS on "never a ground to refuse the file"** (that is exactly the hunk-1 MUST NOT); **FAIL on the elided "unknown"** (A-05) |
| §21.1 | "the register enumerates file-conformance violations" | l.3276, "enumerates every detectable file-conformance violation this specification names" | **PASS** |

### 5.5 Do hunks 1 and 3 agree with each other?

Yes, and that is the repair's real achievement: hunk 1 supplies the
normative MUST NOT that hunk 3's "never a ground to refuse the file"
restates, so hunk 3 is not a rule stranded in a restatement section.
Both use the same position vocabulary as `[R-EXT-03]`, §19.1 step 4,
§20.4's table and Appendix H. The two disagreements found are (a) the
"unknown" qualifier present in hunk 1 and absent in hunk 3 (A-05), and
(b) the scope of the MUST NOT reaching nonconforming files, which hunk 3
does not need and does not mention (A-01).

---

## 6. Contradictions looked for and NOT found

- Hunk 1 vs §2.4's reject-layer row: "all other layers are unaffected. A
  reader MAY still list the file's layers, including the rejected one's
  name." Consistent with, and weaker than, the new MUST NOT. No
  conflict.
- Hunk 1 vs `[R-WRT-06]` ("MUST refuse to compact a file carrying **any**
  record whose type it does not implement with MU = 1"). Refusal to
  compact is not file rejection; §20.4's MU = 1 row draws the same line
  ("At layer scope an unknown critical record blocks modification of
  that layer, leaving other layers editable"). No conflict.
- Hunk 1 vs §19.2's timing rule: sub-record walk is at layer access
  (§19.3 lists "sub-record walk, and sub-record multiplicity
  (`[R-CNT-18]`, `[R-CNT-14]`)"), consistent with a layer-scoped
  outcome. No conflict.
- Hunk 2 vs §20.5's opening "slack is never carried" — resolved by
  §3.1's definition of *stored*; see 4.1.
- Hunk 2 vs §20.4's drop licence — resolved by "retained"; see 4.1.
- Hunk 2 vs `[R-SLB-04]`'s "or clear the declaration" — a narrowed
  option, not a violated one; see 4.4.
- Hunk 2 vs `[R-WRT-05]`/`[R-WRT-08]` (byte-identical re-emission,
  relocation-only modification) — the three enumerated exceptions match
  `[R-WRT-08]`'s "except by relocating its extent and re-pointing its
  slot under §20.5". No conflict.
- Hunk 3 vs the register rows F35/F36/L24/L25 — the register already
  splits top-level from sub-record for exactly this condition, which is
  independent corroboration that the qualifier hunk 3 adds is the right
  one.
- Hunk 3 vs §21.5's ignore-record framing — the MU = 0 branch is
  untouched at both positions.
- Hunk 3 vs §21.1's "where such an entry and the rule it cites diverge,
  the rule governs there too" — note this tiebreak is stated over
  §21.6's *entries* (its table rows); the closing paragraph is prose,
  not an entry, so the tiebreak may not reach it. This is why A-05 is
  reported rather than waved off.

## 7. Findings

A-01 hunk 1 — new MUST NOT contradicts `[R-CNF-12]`'s MAY on a
      nonconforming file (L24). Byte-level.
A-02 hunk 3 — `[R-CNF-03]`'s unqualified "no record … with
      MUST_UNDERSTAND = 1" not swept to "top-level".
A-03 hunk 3 — `[R-ERR-04]`'s "the two capability refusals §21.6 names,
      … an unimplemented MU = 1 type" not swept.
A-04 hunk 3 — the "since" clause re-parented onto a claim it does not
      justify, stranding `[R-CNF-02]`'s.
A-05 hunk 3 — "the same type as a layer sub-record is reject-layer"
      drops `[R-CNT-18]`'s "unknown".
A-06 hunk 2 — "preserves no placement" is a universal the document
      falsifies via `[R-SLB-01]`/`[R-SLB-03]`.
A-07 hunk 1 — re-punctuation leaves the MU = 0 branch as a third
      top-level clause headed by a far-reaching "it".
