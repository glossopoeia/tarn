# Repair audit — hunks 1 and 2 (enumeration and order)

Auditor working transcript. Verbatim record of what was read, what was run,
and what was concluded. Written to be checkable, not to be skimmed.

## 0. Disclosure

Read, in full or in the ranges named below:

- `/private/tmp/.../r24audit/hunk-01.diff` (my charter hunk)
- `/private/tmp/.../r24audit/hunk-02.diff` (my charter hunk)
- `/Users/robertkleffner/Documents/GitHub/tarn/spec/tarn.md`, ranges:
  94–200 (§2 Conformance), 540–600 (§5.1 anatomy, `[R-CNT-01]`,
  `[R-CNT-27]`), 700–820 (§6.1–§6.3, `[R-CNT-04]`, `[R-CNT-06]`,
  `[R-CNT-07]`, `[R-CNT-08]`, `[R-CNT-24]`), 955–985 (`[R-CNT-14]`,
  `[R-CNT-15]`, §7.3 registry table), 1370–1450 (§10.1–§10.4),
  2609–2670 (§18.3, §18.4), 2691–2760 (§19.1 open algorithm, §19.2),
  3180–3260 (§20.4 tail and §20.5 compaction), 3319–3396 (§21.1),
  3396–3455 (§21.2 preamble + full F table), 3455–3512 (§21.3 full L
  table), 3512–3546 (§21.4 T table), 3546–3580 (§21.5 preamble + R
  table), 3580–3634 (§21.6 table and closing), 3770–3800 (`[R-ERR-05]`),
  4400–4441 (Appendix actor checklist).

Did NOT read: `docs/`, `PLAN.md`, `OPEN-QUESTIONS.md`, `AGENTS.md`,
`README.md`, `conformance/`, `spec/registry.json`, git history, `full.diff`,
any other hunk file, the web. Did not list the r24audit directory.

**Unrequested context appeared before I began.** The runtime placed a
project-instruction pointer and an index of the maintainer's private memory
notes in my context. I did not open any of the files it named, and no
conclusion below derives from it. Naming that it appeared, not its contents,
per the charter.

Commands run (all read-only, against the spec only):

```
wc -l spec/tarn.md                                        -> 4441
sed -n '3180,3260p' spec/tarn.md
grep -n "^#### 10\.\|^### 10\|^#### 21\.\|^### 21" spec/tarn.md
sed -n '1370,1450p' spec/tarn.md
sed -n '3455,3600p' spec/tarn.md
sed -n '3396,3455p' spec/tarn.md
grep -n "R-CNT-27\|R-CNT-01\b\|R-CNT-24\|R-CNT-04" spec/tarn.md
sed -n '540,600p' spec/tarn.md ; sed -n '700,820p' spec/tarn.md
grep -n "128" spec/tarn.md
sed -n '3770,3800p' spec/tarn.md ; grep -n "^#### 2\.3\|^### 2\." spec/tarn.md
sed -n '94,200p' spec/tarn.md
grep -n "^#### 19\.\|^### 19\|^#### 21\.1" spec/tarn.md ; sed -n '3319,3396p'
sed -n '2691,2760p' spec/tarn.md
grep -n -i "capability ground" spec/tarn.md
grep -n -i "four rows\|five rows\|three rows\|two rows" spec/tarn.md
grep -n -i "other than 1 is neither\|neither conforming nor nonconforming\|foreign major\|major it does not implement" spec/tarn.md
grep -n "F36\|L25\|L31\|L33\|L34\|L36\|L43\|L45\|R1\b" spec/tarn.md | grep -v <table lines>
sed -n '3600,3640p' spec/tarn.md ; sed -n '4400,4441p' spec/tarn.md
grep -n "^#### 18\." spec/tarn.md ; sed -n '/^#### 18.3/,/^#### 18.5/p'
awk 'NR>=3205 && NR<=3232 {printf "%d:[%s]\n", NR, substr($0,1,3)}'  (blockquote test)
awk 'NR>=3396 && NR<=3415 {...}'                                     (blockquote test)
grep -n "reserved-range\|reserved range" spec/tarn.md
sed -n '955,985p' spec/tarn.md
```

Hard-wrap note: every grep above used a short fragment that cannot wrap
(`128`, `R-CNT-27`, `F36`, `capability ground`, `reserved-range`) or was a
range read rather than a line match. The two blockquote tests read the first
three characters of each line by `awk`, which cannot be defeated by wrapping.

---

## 1. Hunk 1 — §20.5, the compactor's carry-forward parenthetical

### 1.1 The text as it now stands (spec lines 3219–3227)

> Where the output carries a feature a later minor defines and this
> compactor does not — on a conforming input a carried ignore-lane bit
> (§6.3) or an unrecognized `tarn.` key in a record it never decoded
> (§18.3), the two of §10.1's four vehicles §21.6 makes conforming, the
> other two reaching such a file only as values this text still registers
> as reserved-range violations — **F36 and L25 for a record type, and one
> row for each identifier space §10.2 tabulates (L31, L33, L34, L36, L43,
> L45, R1)** — the output's version_minor SHOULD be at least the input's:
> …

Bolded portion is the repair. Prior text: `(F36, L25, R1)`.

### 1.2 The rule the repair asserts, in my words

For each of the extension vehicles that a *conforming* input cannot carry —
an unassigned record type from the reserved range, and an unassigned value
from the reserved range of any numeric identifier space — this text has a
register row that makes the value a violation. Therefore the only two
vehicles by which a conforming input can hand a compactor a later-minor
feature are the ignore-lane flag bit and the unrecognized `tarn.` key. The
parenthetical is a witness list for that exhaustiveness claim: it names, per
space, the row that does the registering.

The repair itself states no requirement. It is descriptive gloss supporting
the `SHOULD` that follows it. It is nonetheless normative text (see §1.5).

### 1.3 Deriving the correct list before reading theirs

I did this from §10.2 alone before comparing. §10.2's table (spec lines
1397–1406) tabulates **eight** spaces:

| # | Space | Reserved range |
|---|---|---|
| 1 | record type (§7.3) | 0x0003–0x7FFF |
| 2 | channel layout (§14.1) | 3–255 |
| 3 | linearization (§11.4) | 2–0x7FFF |
| 4 | sample type (§12.2) | 14–0x7FFF |
| 5 | codec (§17.2) | 5–0x7FFF |
| 6 | filter (§17.3) | 3–0x7FFF |
| 7 | index encoding (§7.4, §15.1) | 2–0x7F |
| 8 | metadata encoding (§18.2) | 3–0x7F |

Cross-check against §10.3, which enumerates the reader treatments: "a
validity error at the owning scope for the value sets of §11.4, §12.2,
§14.1, §15.1, §17.2, and §17.3" (six) "; for record types, the MU-bit
outcome of `[R-CNT-15]`" (seven) "; and for the metadata-encoding space of
§18.2, ignore-record under the quarantine (`[R-CNT-25]`)" (eight). Eight,
confirmed independently of the table.

The rows I derived, one per space, by reading the §21.3/§21.5 tables:

| Space | Row I derived | Row text checked |
|---|---|---|
| record type, file scope | F36 | "A top-level record carries a type value from the reserved range 0x0003-0x7FFF … whatever its MU bit" |
| record type, sub-record | L25 | same wording, layer sub-record |
| channel layout | L36 | "Layer record's layout is a value other than 1 or 2 — 0 or reserved 3–255" |
| linearization | L33 | "reserved 2–3, reserved 4–0x7FFF" |
| sample type | L34 | "outside 1 … 13 — 0, reserved 14–19, reserved 20–0x7FFF" |
| codec | L43 | "reserved 5–0x7FFF" |
| filter | L45 | "reserved 3–0x7FFF" |
| index encoding | L31 | "reserved 2–0x7F" |
| metadata encoding | R1 | "encoding of 0, or a reserved-range value (3-0x7F)" |

My derived list: **F36, L25 · L31, L33, L34, L36, L43, L45, R1** — nine
rows over eight spaces. The repair's list is the same nine rows. **Substantive
coverage is complete and I found no space left without a row.** The prior
text `(F36, L25, R1)` covered three spaces of eight; the repair genuinely
closes that.

### 1.4 Where the repair still fails — the distributive count

The repair's own sentence structure is:

- "F36 and L25 **for a record type**", then
- "and **one row for each identifier space §10.2 tabulates** (L31, L33, L34,
  L36, L43, L45, **R1**)" — **seven** rows.

Record type **is** one of the identifier spaces §10.2 tabulates: it is the
table's first row, `| record type (§7.3) | u16 | 0x0001, 0x0002 |
0x0003–0x7FFF | ≥ 0x8000 |`. So the literal claim is a bijection between the
eight spaces §10.2 tabulates and the seven rows in the parenthetical, and it
is false by one. The record-type space's rows were spent in the preceding
clause and are not repeated inside the parenthetical.

Why this matters and is not pedantry: the sentence is a *witness list for an
exhaustiveness claim*. A reader auditing it does exactly what I did — count
§10.2's rows, count the parenthetical — and gets 8 against 7. The reader then
either hunts for a missing row that does not exist, or concludes a space is
unregistered and that a conforming input can carry a reserved value after
all, which is the opposite of what the sentence is for. The list is longer
than it was, and it is not thereby correctly quantified. See finding **A-01**.

Repair: "and one row for each of the seven **other** identifier spaces §10.2
tabulates (…)", or move F36/L25 inside the parenthetical and say "one or two
rows for each of the eight identifier spaces §10.2 tabulates (F36 and L25 for
record type; L31, …)".

### 1.5 Check 3 — does the repair sit in normative text?

`awk` on the first three characters of spec lines 3205–3232 returns no line
beginning `>`:

```
3219:[tex]  3220:[def]  3221:[ign]  3222:[nev]  3223:[con]
3224:[tex]  3225:[rec]  3226:[(L3]  3227:[the]
```

Plain prose in §20.5. Per `[R-CNF-01]` ("All text in this document is
normative except: §1; any text labeled *Note*, *Example*, or *Rationale*;
and appendices identified as non-normative") this is normative. The rule it
supports — the version_minor `SHOULD` and `[R-WRT-06]` — is in the same
paragraph. **Check 3 passes.** No sibling statement of the same rule sits
only in a `>` block: `grep -n "reserved-range\|reserved range"` returns hits
at 161, 968, 970, 1420, 1434, 3224, and the table rows — none in a
blockquote.

### 1.6 Check 2 — every citation in the repaired text, opened

| Citation | Verdict |
|---|---|
| §10.2 | **PASS with the caveat of §1.4.** §10.2 is "Numeric identifier spaces" and does tabulate identifier spaces. It tabulates eight, not seven. |
| F36 | **PASS.** Line 3453. Reserved-range top-level type, "whatever its MU bit", verifier/certification, `[R-CNT-15]`. |
| L25 | **PASS.** Line 3486. Same for a layer sub-record, `[R-CNT-15]` (R-CNT-18). |
| L31 | **PASS.** index_encoding value domain, includes "reserved 2-0x7F". |
| L33 | **PASS.** linearization, includes "reserved 2-3, reserved 4-0x7FFF". |
| L34 | **PASS.** channel type, includes "reserved 14-19, reserved 20-0x7FFF". |
| L36 | **PASS.** layout, "0 or reserved 3–255". §10.2 gives channel layout no experimental range; L36 matches. |
| L43 | **PASS.** codec, "reserved 5-0x7FFF". |
| L45 | **PASS.** filter, "reserved 3-0x7FFF". |
| R1 | **PASS.** metadata encoding, "encoding of 0, or a reserved-range value (3-0x7F)". |

Surrounding citations not changed by the repair but load-bearing for the
sentence, checked anyway: §6.3 (`[R-CNT-08]`, ignore-lane bit set is not a
file-conformance violation — PASS); §18.3 (`[R-MTA-06]`, "A file carrying an
unrecognized `tarn.` key is **conforming**" — PASS); §10.1 ("This format
grows through exactly four vehicles (`[R-ENC-07]`)" — PASS, four); §21.6
(names the ignore-lane row and the unrecognized-`tarn.`-key row — PASS).

### 1.7 Check 5 — is any row in the wrong class?

The class asserted is "values this text still registers as reserved-range
violations". Every named row's condition text names a reserved range
explicitly (quoted in §1.3's table). R1 is the one that needed thought: its
outcome is *ignore-record*, not a scope rejection. §21.5's preamble settles
it: "Every row here is a violation all the same: the outcome bounds a
reader's blast radius and never makes the file conforming (`[R-CNF-12]`)",
and line 3559 "Encoding 0 and a reserved-range value are unassigned too, and
R1 registers both as violations". R1 is class-correct. §10.3 independently
routes the metadata-encoding space to ignore-record "never a scope-level
rejection", so R1 is the only row that space could have. **No row is in the
wrong class.**

F35 and L24 are *not* named, and that is right, not an omission: §21.1 says
"F35 of F36, L24 of L25" are strict specializations requiring MU = 1, and
`[R-WRT-06]` two sentences later obliges a compactor to refuse any record of
an unimplemented type carrying MU = 1, so an MU = 1 reserved type never
reaches a compactor's output. §21.6's own MU = 0 row names exactly "(F36,
L25)". Consistent.

### 1.8 Check 4 — contradiction in the passage, including untouched text

Read all of §20.5 from line 3193 to line 3245. Looked for: a carve-out the
wider list now collides with; a MUST the list lets an actor violate; a
sentence true only under `(F36, L25, R1)`. Found none. The three rows the
old text named are a subset of the nine; no sentence anywhere in §20.5
counts them or depends on there being three.

One thing I examined and am **not** reporting: "the two of §10.1's four
vehicles §21.6 makes conforming" is untouched text and is, read at maximum
literalness, contestable — §21.6 also makes conforming an *experimental*-range
record type with MU = 0 and an *experimental*-range metadata encoding, which
are vehicles 1 and 2. But the governing clause is "a feature **a later minor
defines**", and later minors assign from reserved ranges, never experimental
ones (§10.3, §10.4). Scoped that way the count of two is right. Not a defect;
recording that I looked.

### 1.9 Check 6 — what does this structure leave unconstrained?

Structure governed: §10.1's four-vehicle enumeration, and, behind it, the set
of things a conforming input can carry that this compactor does not
implement. Members and their governance:

| Member | Governed? |
|---|---|
| ignore-lane flag bits 16–31 | yes — `[R-CNT-08]`, conforming; §21.6 row |
| incompat-lane flag bits 0–15 | yes — F19, violation. Not an extension vehicle at all under §10.1 (vehicle 3 is ignore-lane only), so a later minor cannot define one. Nothing left open. |
| unrecognized `tarn.` key | yes — `[R-MTA-06]`, §21.6 row |
| standardized key out of scope / wrong value shape | yes — `[R-MTA-07]`, §21.6 row; conforming |
| reserved-range record type | yes — F35/F36/L24/L25 |
| reserved-range value, each of the 7 other spaces | yes — the seven rows above |
| experimental-range record type MU = 0 | yes — §21.6, conforming |
| experimental-range metadata encoding | yes — §21.6/`[R-MTA-10]`, conforming |
| trailer reserved bytes [56,60) | yes — F15 |

No member of the structure is left unpinned. **Check 6 passes for hunk 1.**

### 1.10 Check 7 — argument by analogy

The repaired text contains no "exactly as", "the same way", "as X is",
"following", "likewise", "transposed from". Its only warrant-by-pointing is
"each identifier space **§10.2 tabulates**". Verb comparison, side by side:

- repair's governing verb: "each identifier space §10.2 **tabulates**"
- §10.2's own governing verb: "The spaces, defined in the sections that own
  them and **collected here**" (`[R-EXT-02]`), realised as an eight-row table.

Same verb, same set — §10.2 tabulates/collects exactly eight spaces — and
that is precisely why the seven-item list under-delivers against its own
warrant. The analogy check does not save the count; it is the check that
condemns it. Reported as A-01.

### 1.11 Restatements elsewhere the repair should have swept

`grep -n "F36\|L25\|L31\|L33\|L34\|L36\|L43\|L45\|R1\b"` outside the tables
returns: 3224/3226 (the repair), 3343 (§21.1's specialization note), 3559
(§21.5's R1 note), 3631–3632 (§21.6's closing, "F35, F36, L24, L25"), 4428
(appendix verifier checklist, "F36, L25"), 4437 (appendix, "R1"). Each of
these is a statement about record types or about R1 in its own right and none
of them purports to enumerate the per-space rows. **Nothing to sweep.**

---

## 2. Hunk 2 — §21.2's preamble, F5 added as a fifth exception

### 2.1 The text as it now stands (spec lines 3398–3414)

> Outcome: reject-file. 36 conditions. A file declaring a format major other
> than 1 is neither conforming nor nonconforming under this text (§2.3,
> `[R-CNF-02]`), and the rows below whose subject is that file's *geometry*
> do not reach it: §6.2 puts the version gate ahead of every check but the
> trailer magic and the trailer CRC, so such a file is refused on capability
> grounds first. **Five** rows are outside that reasoning and do reach it.
> **Four have as their subject** a field fixed across every major
> (`[R-CNT-24]`): F8 and F1's trailer-magic instance, F14's trailer CRC —
> the two checks §6.2 places before the gate — and F6 with F1's front-block
> instance, which `[R-CNT-04]` places before other processing. **The fifth
> is F5, `[R-CNT-27]`'s 128-byte floor, which §6.2's order does not name
> because it precedes that order: a file shorter than 128 bytes has no
> trailer to read a magic, a CRC or a version from, so the floor is
> established before any field the gate consults exists.** F18 is not an
> exception but a case outside the premise: version_major = 0 declares no
> major at all and is permanently invalid in every one (§21.6).

Prior text: "Four rows are outside that reasoning and do reach it, because
their subject is a field fixed across every major (`[R-CNT-24]`): …".

### 2.2 The rule the repair asserts, in my words

Take a file whose trailer declares version_major ≠ 1. This text normally
records no verdict about such a file's bytes; it is refused on capability
grounds. The repair asserts that F5 is an exception: if such a file is also
shorter than 128 bytes, this text **does** record a verdict about its bytes —
a file-scope validity error under `[R-CNT-27]` — because the size floor is
decided before the trailer is read at all. For an implementer: a reader
handed a 100-byte file declaring major 2 must report a validity error
(reject-file as *corrupt*), and a verifier must report *nonconforming*, not
*cannot establish*.

### 2.3 Check 3 — placement

`awk` on lines 3396–3415 shows no `>` prefix; this is §21.2's preamble prose,
normative under `[R-CNF-01]`. So the assertion has force. Not a
"repair-landed-in-a-Rationale" failure. **Check 3 passes.**

### 2.4 Go read the rule that states the order

The repair claims an ordering. Two candidates for the rule that states it,
both opened.

`[R-CNT-06]`, §6.2, spec lines 771–782, verbatim:

> A reader MUST validate, in order: the trailer magic; the trailer CRC; the
> version gate (§6.3) — only these touch fields whose positions are fixed
> across all majors (`[R-CNT-24]`) — and then, those gates passed, MUST
> validate all of the following before acting on the fields involved: the
> flag gates (§6.3); committed_file_length equals the file size (for a remote
> reader, the size reported by its transport) and is a multiple of 64;
> dir_offset ≥ 16; dir_length ≥ 4; dir_offset + dir_length ≤ F − 64;
> 1 ≤ generation ≤ 2⁶³ − 1; file_id ≠ 0; reserved bytes zero.

`[R-CNT-27]`, §5.1, spec lines 571–575, verbatim:

> No conforming file is shorter than 128 bytes: the front signature block, a
> directory of at least 4 bytes at an offset of at least 16, and the 64-byte
> trailer at a 64-aligned offset cannot be satisfied in fewer. A reader MUST
> treat a shorter file as a validity error at file scope.

`[R-RDR-01]`, §19.1, the open algorithm, step 1 and step 2:

> 1. **End of file.** Obtain the transport-authoritative file size F
>    (`[R-CNT-10]`). …
> 2. **Trailer.** Fetch bytes [F − 64, F) and validate them in §6.2's fixed
>    order — magic, trailer CRC, version gate, then the remaining field gates …

Findings from the three: §6.2 states an order and **does not name the
128-byte floor** — the repair is right about that half. `[R-CNT-27]` states
**no ordering at all**; it states a floor and a reader duty. §19.1 obtains F
at step 1 and validates the trailer at step 2, but **step 1 does not perform
the floor check**; nothing in the ordered algorithm places it. So **no rule in
this document states the order the repair asserts.** The repair supplies the
ordering itself, on a physical argument. That argument is therefore the whole
of its support, and it has to hold. See §2.5.

Citation verdicts for hunk 2:

| Citation | Verdict |
|---|---|
| `[R-CNT-27]` | **PASS as to the floor, FAIL as to the order.** It is the 128-byte floor. It says nothing about when the check runs. The repair's "which §6.2's order does not name because it precedes that order" cites it for a proposition it does not contain. |
| §6.2 | **PASS.** Its ordered list is magic, CRC, version gate, then the rest; it genuinely does not name the floor. |
| `[R-CNT-24]` | **PASS** (untouched clause). Fixes across majors: trailer magic at F−64, version_major/version_minor at F−56, CRC-32C at F−4 over [F−64, F−4), and the front signature block. Notably it does **not** fix any minimum file size, which is why F5 needed a separate ground. |
| `[R-CNT-04]` | **PASS** (untouched clause). "MUST verify the full block by byte equality before other processing". |
| §21.6 (for F18) | **PASS** (untouched clause). §21.6's closing: "version_major = 0, permanently invalid in every format major version (F18, `[R-CNT-07]`)". |
| F5's row | **PASS.** "File size is below the 128-byte minimum … | F (physical file size); committed_file_length | reader | open | `[R-CNT-27]` (R-CNT-01, R-CNT-06) |" |

### 2.5 Test the physical argument at the boundary

The repair's argument, verbatim: "a file shorter than 128 bytes has no
trailer to read a magic, a CRC or a version from, so the floor is established
before any field the gate consults exists."

The trailer is 64 bytes, not 128. §6.2: "The trailer occupies the final 64
bytes of the file". §19.1 step 2: "Fetch bytes [F − 64, F)". Therefore **any
file with F ≥ 64 has a full 64 bytes at [F−64, F) from which a magic, a CRC
and a version can all be read.** The argument holds only for F < 64. Across
the whole window **64 ≤ F < 128 — sixty-four of the file sizes F5 covers —
the premise is simply false.**

Concrete counterexample, constructed at the boundary:

- F = 100 bytes.
- Bytes [0, 16): the §6.1 front signature block constant, byte-exact. F6 and
  F1's front-block instance therefore pass.
- Bytes [36, 100): a well-formed trailer. Offset 0 of it (file offset 36)
  holds `8A 4E 52 41 54 0D 0A 1A`, so F8 and F1's trailer-magic instance
  pass. Offset 8 (file offset 44) holds version_major = 2. Offset 60 (file
  offset 96) holds a correct CRC-32C over trailer bytes [0,60), so F14
  passes.

Walk it under §6.2's stated order: magic — pass. Trailer CRC — pass. Version
gate — version_major = 2 is a major this reader does not implement, so
`[R-CNT-07]` obliges reject-file, and by §21.2's own words "such a file is
refused on capability grounds first". The floor was never reached. **F5 does
not reach this file**, and it did not fail to reach it for some exotic
reason: it failed for exactly the reason the paragraph's general reasoning
gives, which is what makes F5 not an exception to it.

(F = 64 also lies in the window but is a weaker counterexample: with F = 64
the trailer starts at offset 0, so bytes [0,16) are the trailer's first 16
bytes rather than the front block, and a resident reader trips F6 first. F =
100 avoids that and is the clean case. Note also that a 100-byte file
violates F13's "committed_file_length is a multiple of 64" — but F13 is a
major-1 geometry row §6.2 places *after* the gate, so it does not reach the
file either, and a reader still fetches [F−64, F) to find the magic
regardless of alignment.)

Now the other side of the window. For F < 64 there is genuinely no trailer,
so no major is declared. But then the file is not "a file declaring a format
major other than 1" — the premise of the whole paragraph — it is a file
declaring **no** major. That is precisely the category the paragraph's last
sentence already has a name for: "F18 is not an exception but a case outside
the premise: version_major = 0 declares no major at all". A file too short to
carry a version_major declares no major at all in exactly the same way.

**So F5 is misclassified under both halves of its own range.** For
64 ≤ F < 128 it is *inside* the general reasoning (gate first), not outside
it. For F < 64 it is *outside the premise*, F18's category, not an exception
that reaches a foreign-major file. There is no F at which F5 is what the
repair says it is. Finding **A-02**.

### 2.6 Check 4 — contradiction with untouched text in the same passage

Two collisions, both quotable.

(a) With the paragraph's own first sentence, three lines above the repair:

> "A file declaring a format major other than 1 is neither conforming nor
> nonconforming under this text (§2.3, `[R-CNF-02]`) … so such a file is
> refused on capability grounds first."

against the repair:

> "The fifth is F5 … which §6.2's order does not name because it precedes
> that order".

For the 100-byte major-2 file above, the first sentence says capability
refusal comes first and no verdict is recorded about the bytes; the repair
says F5 reaches the file and records a file-scope validity error about its
bytes. Both are normative prose in the same paragraph.

(b) With `[R-CNF-02]` itself, §2.3:

> "a file declaring another major is neither conforming nor nonconforming
> under it: a reader refuses such a file on capability grounds (§6.3,
> `[R-CNT-07]`), and **that refusal is not a finding about its bytes**."

F5 reaching such a file *is* a finding about its bytes. The repair's ground
would have this text pronounce a validity error on a file over which §2.3
disclaims jurisdiction.

### 2.7 The list's stated common ground, and whether F5 shares it

The old list had one ground: "because their subject is a field fixed across
every major (`[R-CNT-24]`)". F5's subject is not such a field. `[R-CNT-24]`
fixes exactly four things across majors — trailer magic position, the two
version fields' position, the trailer CRC's position and coverage, and the
front signature block — and adds "A future major MAY redefine only the
remaining 48 trailer bytes". A minimum file size is not among them, and could
not be: the 128 floor is derived in `[R-CNT-27]` from *major-1* structure
sizes ("a directory of at least 4 bytes at an offset of at least 16"), which
a future major is free to change.

Credit where due: **the repair noticed this and restructured the sentence to
carry two grounds explicitly** — "Five rows are outside that reasoning …
Four have as their subject a field fixed across every major … The fifth is
F5 …". That is the right shape. The sentence does not silently have two
grounds; it says so. The defect is not the structure, it is that the second
ground does not hold (§2.5).

### 2.8 Check 1 and check 6 — the quantifier, and F5's second instance

The passage's own idiom is **instance-level**, not row-level, and the repair
departs from it. The untouched text is careful: "F1's **trailer-magic
instance**", "F6 with F1's **front-block instance**" — because F1's other
instance and F6's residency exemption behave differently. The repair says
"The fifth is **F5**", naming the whole row.

F5 has two instances. Its Instances cell, verbatim:

> `F (physical file size); committed_file_length`

Take the second. Establishing "committed_file_length is below 128" requires
reading the u64 at **trailer offset 40**. Trailer offset 40 is inside the "48
remaining bytes" `[R-CNT-24]` expressly permits a future major to redefine,
so on a major-2 file there is no committed_file_length field at that offset
to read; and §6.2 places "committed_file_length equals the file size" in the
*after-the-gate* group. Under no reading whatsoever can F5's
committed_file_length instance "precede that order" — it is a trailer field
whose very existence the gate has to establish first.

So even a maintainer who wants to keep the F5 claim on some repaired ground
must scope it to F5's **physical-file-size instance**. As written the
sentence sweeps in an instance that plainly cannot qualify, in a passage that
elsewhere splits rows into instances precisely to avoid this. This is the
"named one quantity where two are in play" shape: the sentence reads as
perfectly correct about the thing it mentions (physical file size) and is
wrong about the sibling it does not mention. Finding **A-03**.

Enumerating the structure the repair governs, per check 6 — the classification
of all 36 §21.2 rows against a foreign-major file:

| Class | Rows | Governed? |
|---|---|---|
| fixed across every major, before the gate | F8, F14, F1 (trailer-magic instance) | yes, named |
| fixed across every major, before other processing | F6, F1 (front-block instance) | yes, named — with `[R-CNT-04]`'s residency exemption, which the row cell carries |
| outside the premise | F18; and, I argue, F5 at F < 64 | F18 named; F5's short-file case not |
| everything else (F2–F4, F7, F9–F13, F15–F17, F19–F36) | after the gate | covered by "Five rows are outside" as a closed count |
| F5, physical-size instance | disputed | see A-02 |
| F5, committed_file_length instance | after the gate, field not fixed across majors | unaddressed — see A-03 |

One thing I checked and am **not** reporting: F15's Governing rule cell cites
`(R-CNT-24)`, so a reader grepping `R-CNT-24` across the F table finds a
fifth row and may wonder why it is not among the exceptions. It correctly is
not — trailer bytes [56,60) are inside the 48 a future major may redefine,
and F15 is checked after the gate. The prose names its rows explicitly rather
than by citation, so there is no ambiguity to report.

### 2.9 Does anything elsewhere depend on the old count?

```
grep -n -i "four rows\|five rows\|three rows\|two rows" spec/tarn.md
2184:> writer's, and it is what makes those two rows reachable at all after a
3403:file is refused on capability grounds first. Five rows are outside
3520:| T2 | … the two rows together covering `[R-SER-08]` |
3729:The last three rows are **per-instance**, and are individuated
3739:that row, whatever its declarations would derive. The first five rows
```

None of 2184, 3520, 3729, 3739 concerns §21.2's exception set. Likewise
`grep -n -i "capability ground"` returns only 144 (§2.3) and 3403 (this
paragraph). **No external dependency on the old count of four.** §21.2's
header count "36 conditions" is unaffected (rows run F1…F36; verified by
reading the table).

### 2.10 Restatement the repair should have swept

§19.1 is this document's only *ordered* reader procedure and its step 1 is
the only place F becomes available. If the maintainer's intent is that the
128-byte floor gates before the trailer read, that intent has to be written
into §19.1 step 1, which today says only "Obtain the transport-authoritative
file size F (`[R-CNT-10]`)" and then hands off to §6.2's fixed order. As
things stand, §21.2's preamble asserts an ordering fact about a check that
appears in no ordered list in the document. An implementer building from
§19.1 — the section that tells them how to open a file — will never run the
floor check before the gate. Finding **A-04**.

### 2.11 Checks that passed for hunk 2

- **Check 5 (exhaustive claims):** "Five rows", "every check but the trailer
  magic and the trailer CRC", "any field the gate consults", "every major".
  "every check but the trailer magic and the trailer CRC" verified against
  `[R-CNT-06]`'s ordered list — correct, the version gate is third and
  everything else follows it. "every major" verified against `[R-CNT-24]`.
  The count "Five" is wrong only because F5 should not be in it (A-02); the
  arithmetic over the four is right (F8, F14, F6, F1 — four rows, five
  instances, exactly as the prose splits them).
- **Check 7 (analogy):** the repaired sentence's only warrant-by-pointing is
  "which §6.2's order does not name because it **precedes** that order".
  Verbs side by side — repair: "**precedes** that order"; `[R-CNT-06]`: "A
  reader MUST **validate, in order**: the trailer magic; the trailer CRC; the
  version gate"; `[R-CNT-27]`: "A reader MUST **treat** a shorter file as a
  validity error at file scope". `[R-CNT-27]` has no ordering verb at all —
  no "before", no "first", no "in order". The repair's "precedes" ranges over
  a sequence that its cited rule does not join. Reported inside A-02; the
  comparison is recorded here as the charter asks, including that it fails.

---

## 3. Verdict

Four findings. Hunk 1's repair is substantively right — every one of §10.2's
eight identifier spaces now has its row named, and I derived the same nine
rows independently before reading theirs — but its distributive phrase
promises a row per tabulated space and delivers seven for eight (A-01).
Hunk 2's repair is structurally the right shape — it names its second ground
openly instead of smuggling it — but the ground itself does not hold: the
physical argument is false across the entire 64 ≤ F < 128 window, and at
F < 64 the file falls into F18's outside-the-premise category rather than
being an exception that reaches a foreign-major file (A-02). It additionally
names a row where the passage's own idiom names instances, sweeping in an
instance that cannot qualify under any reading (A-03), and asserts an
ordering that §19.1 does not carry (A-04).

Byte-level: none of the four. A-01 is descriptive gloss supporting a SHOULD.
A-02's disputed files all declare a major other than 1, so no conforming
writer under this text emits them and every reader rejects them under both
readings — what forks is the *verdict label* a verifier reports
(*nonconforming* vs *cannot establish*, §2.3) and the diagnostic §6.3
prescribes, not the accept/reject bit and not the emittable set. A-03 and
A-04 inherit that. I record the verdict-label fork explicitly so a maintainer
who counts §2.3's three verifier verdicts as an observable can overrule me;
on the charter's stated discriminating question the answer is no.
