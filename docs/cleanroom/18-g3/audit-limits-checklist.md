# Round 18 repair audit — hunks 7 and 10

Auditor scope: hunk-07.diff (§21.9 limits, `[R-ERR-04]`) and hunk-10.diff
(Appendix H verifier checklist, decoded-content item).

## 0. Disclosure — what I read and ran

Files opened:

- `/private/tmp/.../round18-audit/hunk-07.diff`
- `/private/tmp/.../round18-audit/hunk-10.diff`
- `/Users/robertkleffner/Documents/GitHub/tarn/spec/tarn.md` — read in these
  windows: 95–118 (§2.1 `[R-CNF-01]`), 128–163 and 160–199 (§2.2/§2.3
  `[R-CNF-02]`, `[R-CNF-03]`, `[R-CNF-11]`), 215–232 (§2.4 head), 268–283
  (§2.5 `[R-CNF-10]`), 785–824 (§6.3 `[R-CNT-07]`, `[R-CNT-08]`,
  `[R-CNT-24]`, `[R-CNT-26]`), 955–1014 (§7.2 `[R-CNT-14]`, `[R-CNT-15]`;
  §7.3 `[R-CNT-22]`; §7.4 head), 1040–1061 (`[R-CNT-17]`, `[R-CNT-18]`),
  1387–1430 (§10.2 `[R-EXT-02]`, §10.3 `[R-EXT-03]`), 1836–1864 (§14.2
  `[R-SER-02]`, `[R-SER-08]`), 1885–1934 (§14.3 `[R-SER-03]`, `[R-SER-07]`;
  §14.4 `[R-SER-09]`), 1950–2009 (§14.5 `[R-SER-05]`; §15.1 head),
  2228–2247 (§17.2 `[R-COD-03]`), 2350–2379 (§17.3 `[R-COD-09]`,
  byte-shuffle), 2396–2425 (§17.4 `[R-COD-11]`), 2440–2489 (§18.2
  `[R-MTA-03]`, `[R-MTA-09]` + its Note), 3337–3364 (§21.2 head, F1–F10),
  3392–3448 via grep (§21.3 L-rows), 3449–3482 (§21.4 all T-rows),
  3483–3515 (§21.5 head, R1–R10), 3516–3570 (§21.6 whole), 3580–3620
  (§21.7 tail, §21.8), 3621–3696 (§21.9 whole, incl. the repaired
  paragraph, its Note and `[R-ERR-05]`), 4240–4290 (Appendix H head,
  file/reader/writer bullets), 4270–4328 (updater + verifier bullets).

Commands run (all against spec/tarn.md only):

- `grep -n "^#### 21\.\|^#### 22\.\|^### 21\|^### 22" spec/tarn.md`
- `grep -n "R-CNT-15\|R-CNF-03\|R-CNT-07" spec/tarn.md`
- `grep -n "incompat" spec/tarn.md`
- `grep -n "R-CNT-18" spec/tarn.md`
- `grep -n "^#### 6\.\|^### 6\.\|^#### 10\.\|^### 10\." spec/tarn.md`
- `grep -n "^#### 14\.\|^### 14\." spec/tarn.md` + `sed -n '3449,3483p'`
- `grep -n "R-SER-08\|R-SER-05\|R-SER-03" spec/tarn.md`
- `grep -n "R-MTA-05\|R-CNT-22" spec/tarn.md`
- `grep -n "R-CNF-10\|R-ERR-03" spec/tarn.md` + `sed -n '215,232p'`
- `grep -n "overlap" spec/tarn.md` + slab/alignment grep over §21.3
- `grep -n "R-CNF-01" spec/tarn.md` + `sed -n '95,118p'`
- Two python3 passes that joined all lines into one whitespace-normalised
  string and printed ±130/160 chars of context around each occurrence of:
  `minimum guarantee`, `guarantees of`, `within the table`,
  `not a conforming reader`, `conforming reader MUST accept`, `declines`,
  `on that ground`, `capability refusal`, `capability ground`, `pad bit`,
  `decoded-content`, `reject-layer — never`, `two capability`.
  (Whole-document normalisation, so hard wraps could not hide a match.)

Nothing else was read. I did not open `full.diff`, other hunk files, docs/,
conformance/, registry.json, PLAN.md, OPEN-QUESTIONS.md, AGENTS.md, README,
or git history. I did not list the audit directory. No web access.

---

## 1. HUNK 7 — §21.9, `[R-ERR-04]` (spec line 3644–3654)

### 1.0 The rule the repair adopts, in my own words

Before: *any* refusal of a file all of whose quantities sit inside §21.9's
table makes the software a non-conforming reader.

After: refusing such a file **because the reader cannot serve its
declarations** (the resource/capacity ground of the preceding sentence)
makes the software a non-conforming reader. Refusing it because the reader
lacks a *capability* — it does not implement the file's format major, or it
does not implement a record type carried with MU = 1 — does not. The
minimum-guarantee floor is therefore a floor on resource capacity only,
not a bar on capability-driven rejection.

### 1.1 Check 1 — tense and quantifier

- Generation: the passage is about a single file presented to a reader, not
  about a commit's prior/new state. No generation ambiguity is available
  here and the repair introduces none.
- Set: "**a** file whose **every** quantity lies within the table" —
  unchanged from round 16 (both `-` and `+` lines carry it). The universal
  runs over the table's rows applied to the file's declarations; the
  existential over files. Matches `[R-CNF-03]`'s "every conforming file …
  none of whose values exceeds the minimum guarantees".
- "the two capability refusals §21.6 names" — a definite, counted
  enumeration. Checked in §1.5 below.
- The normative rule being restated is `[R-CNF-03]` (spec 157–171):

  > "A reader MUST accept every conforming file of a format major version
  > it implements, carrying no record of a type it does not implement with
  > MUST_UNDERSTAND = 1 — in a conforming file such a type is necessarily
  > from the experimental range, since a reserved-range type carrying
  > MU = 1 is itself a violation — and none of whose values exceeds the
  > minimum guarantees of §21's limits table (§21.9's `[R-ERR-04]` governs
  > a refusal on that last ground; §21.6's closing paragraph names the
  > other two) …"

  The repair's quantifier and carve-out match `[R-CNF-03]` exactly,
  including the "the other two" count. **PASS.** The repair is a
  restatement, and it now agrees with its source; before the repair it did
  not.

- One antecedent question I chased: does "**on that ground**" have a
  non-vacuous antecedent? The preceding sentence ends "…at the narrowest
  scope whose declarations **exceed what it can serve**, a layer or a
  tile." "What it can serve" is the reader's capacity, so "that ground" =
  *declarations exceeding what this reader can serve*, which a within-table
  file can perfectly well trigger for a small reader. The alternative
  reading ("the ground that the file exceeds the table") would make the
  sentence vacuous, but it is not the nearer antecedent and the following
  sentence's "Either way, a refusal on resource grounds…" confirms the
  capacity reading. Not a defect; recorded because I looked.

### 1.2 Check 2 — citations resolve

| Citation in repaired text | Opened at | Verdict |
|---|---|---|
| `[R-CNF-03]` | spec 157–171 | **PASS.** States the acceptance duty with three conditions (major implemented; no unimplemented MU = 1 record; within the guarantees) and the "not a conforming reader" consequence. It also itself points at §21.6's closing paragraph for "the other two". The repair's use is exact. |
| §21.6 (for the two refusals) | spec 3549–3565 | **PASS on count.** "Two structural cases are **conforming files a reader nevertheless refuses**. The first is **version_major naming a major this reader does not implement**… The second is an **experimental-range record type carrying MU = 1**…" |
| §21.6 → "a foreign format major" | 3550–3552 | **PASS.** Accurate paraphrase; §2.3 (143–145) uses the same framing ("a reader refuses such a file on capability grounds"). |
| §21.6 → "an unimplemented MU = 1 type" | 3552–3557 | **PASS, with a note.** §21.6 says *experimental-range* MU = 1; the repair says *unimplemented* MU = 1. These are not the same set: §21.6's own phrasing is the loose one (an experimental type a reader *does* implement privately produces no refusal at all — `[R-CNT-15]` keys on "unknown"), and the repair's is the tighter one, matching `[R-CNT-15]` ("An unknown record type at file scope: MU = 1 → reject-file") and `[R-CNF-03]` ("a type it does not implement with MU = 1"). Not a defect; the repair is more accurate than the section it cites. |
| `[R-ERR-04]` (the tag the paragraph carries) | 3654 | **PASS.** The paragraph is the requirement, not a restatement of another one, for the resource-report half. |

Citations checked and **not** appearing in the repaired text but load-bearing
for it, all opened: `[R-CNT-07]` (6.3, 787–794) — yes, MUST reject-file on an
unimplemented major; `[R-CNT-15]` (7.2, 964–973) — yes, MU = 1 unknown at file
scope → reject-file, and the experimental-range file stays conforming;
`[R-CNF-02]` (2.3, 146–156) — yes, conduct rules bind the actor, not the bytes.

### 1.3 Check 3 — the repair sits in normative text

`[R-CNF-01]` (spec 105–106): "All text in this document is normative except:
§1 (Introduction); any text labeled *Note*, *Example*, or *Rationale*; and
appendices identified as non-normative."

Lines 3644–3654 carry no ">" prefix and are not labelled Note/Example/
Rationale; the paragraph ends `[R-ERR-04]`. §21.6's closing paragraph
(3549–3565) is likewise unquoted prose. **PASS** — the repair landed in
normative text, and the source it now agrees with (`[R-CNF-03]`) is
normative too.

### 1.4 Check 4 — contradiction in the same passage, including untouched text

I read the whole of §21.9 (3621–3694): opening paragraph `[R-ERR-03]`, the
table, the repaired paragraph, the Note, and `[R-ERR-05]`'s hard-limits
paragraph.

**FOUND — `[R-ERR-03]`, four lines above the repair, spec 3628–3631:**

> "The table below states **minimum guarantees**, not caps: a conforming
> reader MUST accept any conforming file whose quantities lie within these
> bounds, and a writer MAY rely on that. `[R-ERR-03]`"

This is normative (no ">", carries an ID) and it is the *unqualified* form
of exactly the duty the repair just qualified. Take the file §21.6 itself
describes: a conforming format-major-1 file carrying a top-level
experimental-range record with MU = 1, every quantity inside the table.
- `[R-ERR-03]` says a conforming reader **MUST accept** it.
- `[R-CNT-15]` says the reader's outcome is **reject-file**.
- The repaired `[R-ERR-04]` sentence says that refusal is *not* the ground
  that costs conformance — i.e. the reader stays conforming while refusing.
- §21.6 says the file "can be perfectly conforming" and "`[R-CNF-02]` makes
  the file conforming all the same".

So §21.9 now contains, four lines apart, a MUST to accept and a licence to
refuse the same file. The repair carved the exception into the weaker,
restating sentence and left the MUST-bearing sentence that introduces the
very table standing in the old, over-broad form. This is the project's
signature failure mode (rule changed in one place, left standing in
another) occurring *inside the repaired subsection*. Filed as **E-01**.

Nothing else in §21.9 collides: the Note (3656–3671) is about where the
numbers came from; `[R-ERR-05]` (3673–3694) is about hard limits, a
disjoint category, and says "a file violating one is invalid, not merely
large" — consistent.

I also checked the §21.9 opening sentence "Every limit affecting which
files are valid, or which files a conforming reader accepts, lives in this
specification and never only in an implementation (`[R-CNF-10]`)". A
reader's *capability* (which majors, which record types) is not a "limit"
in that sense — §21.6 calls it "a reader's capability, not a defect in the
bytes" — so no collision.

### 1.5 Check 5 — exhaustive claims

Completeness words in the repaired text: "**every** quantity", "**the
two** capability refusals".

(a) "every quantity" — unchanged by the repair, and bounded by "lies within
the table", a closed 8-row table. Cannot be falsified.

(b) "the two capability refusals §21.6 names" — I enumerated §21.6 in full
(3516–3565): 13 table rows, then two closing paragraphs. The table rows are
defined non-violations, none of them a refusal (the closest, an
experimental-range **MU = 0** record, is *ignored*, not refused). The
paragraph at 3538–3547 is about two conditions that moved *out* of the
table into the register — also not refusals. The paragraph at 3549–3565
names exactly two refusals. **The count is right.**

Candidates for a third that I tried and rejected:

1. **An unknown incompat-lane flag bit** (§6.3 `[R-CNT-08]`, "a reader MUST
   reject-file on any set bit it does not implement in the incompat lane"),
   which spec line 3121 explicitly calls "the same treatment §6.3 gives an
   unknown incompat-lane bit". **Rejected as a third case**: F19 in §21.2
   registers it — "Any bit of the flags incompat lane (bits 0-15) is set;
   this text defines no flag bits, so every such bit is unimplemented …
   reader | open | `[R-CNT-08]`" — so under this text such a file is
   *nonconforming*, not "a conforming file a reader nevertheless refuses".
   §21.6's premise does not reach it.
2. **A codec or filter the reader cannot execute.** Rejected: §17.4
   `[R-COD-11]` (2402–2407) says "For a conforming reader that position
   arises only at a reserved or experimental value, every assigned codec
   and filter being core: it rejects the layer … software unable to execute
   an assigned codec or filter is not a conforming reader (`[R-CNF-03]`)."
   A reserved/experimental codec or filter value is a validity error at
   layer scope (`[R-COD-03]`, `[R-COD-09]`), so the file is not conforming.
3. **An unassigned user-metadata document encoding.** Rejected: it is
   ignore-record, never a refusal (§18.2 `[R-MTA-03]`, `[R-MTA-10]`,
   §21.6 row, §17.4's closing sentence).
4. **An unimplemented MU = 1 *sub-record* at layer scope.** *Not* rejected
   — see below.

On (4): `[R-CNT-18]` (spec 1050–1054): "an unknown sub-record type with
MU = 1 is **reject-layer — never reject-file** — and with MU = 0 is
ignore-record", and `[R-EXT-03]` (1424–1426) routes experimental values to
"the MU-bit outcome of `[R-CNT-15]` at file scope and `[R-CNT-18]` for
layer sub-records". A conforming file (experimental range ⇒ `[R-CNF-02]`
keeps it conforming) can therefore have one of its layers refused by a
conforming reader purely on capability. That is a third capability refusal
of (part of) a conforming file, and §21.6 does not name it.

Does it falsify "the two capability refusals §21.6 names"? Strictly no:
the claim is *de dicto* about §21.6, §21.6 names two, and §21.6's own
premise is whole-file ("conforming **files** a reader nevertheless
refuses"). But the repaired sentence sits one clause after a sentence that
explicitly extends declining to "a layer or a tile", and it drops the scope
word: it says "capability refusals", not "whole-file capability refusals".
Read in that neighbourhood, "the two" reads as the complete inventory of
non-resource refusals, and it is not. Filed as **E-03**, low severity, with
the one-word repair.

### 1.6 Restatements the repair should have swept

Whole-document search for the acceptance duty (python normalised pass on
`minimum guarantee`, `conforming reader MUST accept`, `within the table`,
`not a conforming reader`). Five statements exist:

| Site | Text | Carve-out present? |
|---|---|---|
| §2.3 `[R-CNF-03]`, 157–164 | "MUST accept every conforming file **of a format major version it implements, carrying no record of a type it does not implement with MU = 1**, and none of whose values exceeds…" | **Yes** — the authority |
| §2.5 `[R-CNF-10]`, 273–278 | "Readers MAY enforce resource limits, but MUST accept any conforming file within the minimum guarantees stated in §21's limits table" | **No** |
| §21.9 `[R-ERR-03]`, 3628–3631 | "a conforming reader MUST accept any conforming file whose quantities lie within these bounds" | **No** |
| §21.9 `[R-ERR-04]`, 3646–3650 | the repaired sentence | **Yes** — new |
| Appendix H reader bullet, 4274–4276 | "accepts every conforming file within §21.9's minimum guarantees and reports any resource refusal as a limit rather than as corruption (`[R-ERR-04]`)" | **No** |

The repair swept one of the four non-authoritative sites. `[R-ERR-03]` is
E-01 (same subsection). `[R-CNF-10]` and the Appendix H reader bullet are
E-02. `[R-CNF-10]` is the milder of the two because "Readers MAY enforce
resource limits, **but** MUST accept…" ties the MUST to the resource
clause by the conjunction; the Appendix H bullet has no such tie and is the
checklist an implementer audits against — and it cites `[R-ERR-04]`, the
very requirement that now says the opposite thing about capability
refusals. Appendix H is non-normative by `[R-CNF-01]` and disclaims its own
authority ("each entry's authority is the requirement or section cited,
never this summary"), which is why E-02 is not byte-level.

Note for E-02's Appendix H half: the *foreign-major* case escapes it,
because §2.3 (141–145) makes a foreign-major file "neither conforming nor
nonconforming under" this text, so it is not "a conforming file". Only the
MU = 1 case bites. I checked this rather than assuming it.

### 1.7 Overshoot / undershoot / new ambiguity for hunk 7

- Overshoot: none. The carve-out is exactly `[R-CNF-03]`'s two conditions.
- Undershoot: yes, in the sweep sense — E-01/E-02.
- New ambiguity: the "on that ground" antecedent was checked in §1.1 and
  resolves; the scope-free word "capability refusals" is E-03.

---

## 2. HUNK 10 — Appendix H, conforming verifier bullet (spec line 4315–4317)

### 2.0 The rule the repair adopts, in my own words

A conforming verifier's decoded-content checks are three, not two: it must
check padding-position content, **packed-plane pad bits**, and interleaved
boolean value bytes. Pad bits were missing from the summary; the repair
adds them and adds §14.3 to the parenthetical section list.

### 2.1 Check 1 — tense and quantifier

No generation language. The list is an enumeration inside a non-normative
summary of a class's obligations; the quantifier that matters is
completeness of the enumeration, handled under check 5. The normative rule
being summarised is `[R-SER-05]` (§14.5, 1957–1961): "**Every pad bit**
(§14.3) MUST carry the plane's channel's fill bit. A conforming reader
never returns this content (`[R-GEO-04]`) and is not obligated to check it;
**a verifier MUST check it**, and a violation is a validity error at tile
scope." The universal ("every pad bit") and the actor (verifier) match.
**PASS.**

### 2.2 Check 2 — citations resolve

| Citation | Opened at | Verdict |
|---|---|---|
| §14.5 | 1950–1961 | **PASS.** States both the padding-position obligation and the pad-bit obligation, both as `[R-SER-05]`, and both explicitly as verifier MUSTs. |
| §14.2 | 1842–1853 | **PASS.** `[R-SER-08]`: "Writers MUST NOT emit any byte other than 0x00 or 0x01 as an interleaved bool value… its assigned detector is the verifier, for which it is a validity error at tile scope." |
| §14.3 (newly added) | 1885–1898 | **FAIL, mildly.** §14.3 *defines* pad bits — "The final byte's high bits beyond the last value … are the tile's **pad bits**; **their content is fixed by `[R-SER-05]`** and they never encode values" — and then disclaims any reader/verifier check: "decoding a packed plane never fails over its content; padding-position content binds writers (§14.5), never a reader's decode path. `[R-SER-03]`". §14.3 states no obligation; it forwards to §14.5. The list's three items map positionally onto its three sections (padding samples→§14.5, pad bits→§14.3, boolean bytes→§14.2), so the pad-bit obligation is anchored to the section that does not state it. Filed as **E-04**. |

Corroborating: every other place in the document that enumerates this same
trio anchors pad bits to §14.5/`[R-SER-05]`, never to §14.3 —
- §17.4 (2396–2397): "The decoded-content obligations of §14 (`[R-SER-05]`,
  `[R-SER-08]`)";
- §2.3 (200–202): "§14's decoded-content obligations (`[R-ERR-04]`,
  `[R-SER-05]`, `[R-SER-08]`)";
- §21.7 (3575–3577): "The obligations of §14.5 and `[R-SER-08]` narrow this
  only where content is structurally constrained: padding positions, pad
  bits, and boolean bytes";
- Appendix H **writer** bullet (4283–4284): "fill-encodes edge padding and
  pad bits (`[R-SER-05]`, §14.5)".

The repaired verifier bullet is now the only site in the document that
sends a reader to §14.3 for the pad-bit obligation, and it is two bullets
below a writer bullet that sends them to §14.5 for the same obligation.

### 2.3 Check 3 — the repair sits in normative text

Appendix H is headed "Appendix H — Conformance checklists (non-normative)"
and `[R-CNF-01]` excludes "appendices identified as non-normative". So the
repair is in non-normative text — but that is **correct here**, because
this repair is not creating a rule: the rule (`[R-SER-05]`, §14.5) already
covers pad bits normatively and was already correct. The defect being
repaired was a summary that was short by one item. **PASS** — and the
mirror failure ("the repair edited a summary while the normative statement
elsewhere still says the old thing") does not apply: §14.5 already said the
new thing.

### 2.4 Check 4 — contradiction in the same passage

I read the whole verifier bullet (4302–4327) and its neighbours (file,
reader, writer, updater bullets, 4262–4300), and resolved every other item
in the verifier list:

| Item | Resolves? |
|---|---|
| live-state coverage partition + slack total, "reported as partial — an upper bound, naming the scope or violation that stopped the walk" (§9.7, `[R-CNT-21]`) | Yes — matches §21.6's slack row verbatim in substance (3530). |
| extent overlap (§7.2) | Yes — spec 945–952: verifier MUST treat intra-layer overlap as reject-layer, overlap outside the layer as reject-file; L18 in §21.3, detector verifier. |
| record flag bits: reserved bits, MU = 1 with PE = 0, registered type's stored bits vs §7.3 (`[R-CNT-12]`, `[R-CNT-22]`) | Yes — §7.3 (985–998), rows F28/L49. |
| front signature block by byte equality, which `[R-CNT-04]` lets a non-resident reader defer and §2.3 does not (F1, F6) | Yes — F1 and F6 (3355, 3360) say exactly that, and §21.2's head paragraph (3344–3349) repeats it. |
| no structure between live directory end and live trailer (`[R-CNT-05]`, F7) | Yes — F7 (3361), detector verifier. |
| reserved-range record or sub-record type value, **whatever its MU bit** (`[R-CNT-15]`, F36, L25) | Yes — F36 and L25 (3390, 3423) both say "whatever its MU bit". |
| alignment and slab invariants (§16) | Yes — L41, L42 verifier/certification (3439–3440); L20/L28/L29/L39 reader-detected, covered by "every reader obligation". |
| user-metadata member ordering (`[R-MTA-05]`, §18.2) | Yes — F27 (3381) and L48 (3446), detector verifier. |
| experimental-range metadata encoding is no bar and is reported: owning scope, encoding value, stored extent length (`[R-MTA-10]`); encoding 0 and reserved stay violations (R1) | Yes — §21.5 head (3490–3497) and R1 (3505). |
| *nonconforming* vs *cannot establish*; report unchecked requirements and unexamined scopes (`[R-CNF-11]`) | Yes — §2.3 (193–223). |

No stale neighbour found in the verifier bullet. No carve-out or MAY in the
passage collides with the new item; the writer bullet two above states the
writer side of the same obligation and agrees on substance.

One term mismatch, **pre-existing** (present on the `-` line too, so not
introduced by this repair): the list says "padding **samples**" where §11.3,
§14.5, T4 and §21.7 all say "padding **positions**", and §14.3's Note
(1900–1905) exists specifically to keep "padding position" and "pad bit"
apart. Not filed as its own finding — it is not the repair's doing and it
introduces no ambiguity an implementer can act wrongly on — but it is worth
folding into E-04's edit while that line is open.

### 2.5 Check 5 — exhaustive claims / is the list still short by one?

The item is an enumeration presented as closed ("decoded-content
obligations — X, Y and Z"). I enumerated every decoded-content obligation
the document places on a verifier, from three independent directions:

1. **From §21.4's rows** (read in full, T1–T26). Verifier-detected rows
   about decoded content: **T2** (interleaved bool value byte at a real
   position, `[R-SER-08]`), **T4** (padding position content, `[R-SER-05]`),
   **T5** (packed-plane final-byte pad bits, `[R-SER-05]`). **T26**
   (mis-strided filter) is verifier-detected but explicitly has no check of
   its own: "the check that detects it is T2's or T4's, and this row
   records the cause rather than a procedure of its own". Every other
   verifier row in §21.4 — none — and all remaining rows are reader-detected
   (covered by the bullet's opening "every reader obligation, plus…").
   Count: **3**.
2. **From the sections cited.** §14.5 → 2 obligations (padding positions,
   pad bits), both verifier MUSTs; §14.2 → 1 (`[R-SER-08]`); §14.3 → 0 (it
   defers; `[R-SER-07]`'s decoded-length rule at its tail is a *reader*
   obligation, T3, and is about length not content). Count: **3**.
3. **From the document's own enumerations.** §21.7 (3589–3591): "except
   where §14 constrains a byte's content — **a padding position, a pad bit,
   or an interleaved boolean** — and a mis-ordered image is then witnessed
   by T2, T4 or T5"; §21.7 again (3575–3577): "padding positions, pad bits,
   and boolean bytes"; §20.3-related text (3598–3600): "a padding position,
   a pad bit, or a boolean byte". Count: **3**, three times.

The repaired list has exactly those three. **The list is now complete; it
is not short by one.** Two adjacent things a reader might expect and that
are *not* missing because they are listed separately or are reader-side:
user-metadata member ordering (its own item, F27/L48) and the
decoded-payload length rule `[R-SER-07]`/T3 (reader-detected).

No other completeness word appears in the repaired text.

### 2.6 Overshoot / undershoot / new ambiguity for hunk 10

- Undershoot: none — the list is complete at three.
- Overshoot: none — no obligation was added that the document does not
  place on a verifier.
- New ambiguity: the §14.3 anchor, E-04.

---

## 3. Byte-level test, per finding

The discriminating question: is the disputed file itself conforming, and
does a reading fork the bytes a writer may emit or the verdict a reader
must give?

- **E-01.** The disputed file — a conforming major-1 file with a top-level
  experimental-range record carrying MU = 1, all quantities within the
  table — *is* conforming: §21.6 says so ("`[R-CNF-02]` makes the file
  conforming all the same"), no register row fires ("Neither is a register
  row"), and §10.3's bar on publishing experimental values is conduct-only,
  so `[R-CNF-05]` does not bar a writer from emitting it. So the emittable
  set does not move. The *verdict* is what the two sentences disagree
  about — accept (`[R-ERR-03]`) vs reject (`[R-CNT-15]`) — but `[R-CNT-15]`
  is a specific, unambiguous MUST and `[R-CNF-03]` carves the case out
  explicitly, so a competent reader rejects under both readings. What
  actually forks is a *conformance-test verdict about the reader*: a suite
  built from `[R-ERR-03]` would fail a correct reader. Not byte-level.
- **E-02.** Same file, same reasoning; and the Appendix H half is
  non-normative and self-disclaiming. Not byte-level.
- **E-03.** The layer-scope case: a conforming file with an
  experimental-range MU = 1 *sub-record*. `[R-CNT-18]`'s "reject-layer —
  never reject-file" is a flat MUST-equivalent outcome assignment; no
  reading of §21.9 licenses suppressing it. Not byte-level.
- **E-04.** A citation anchor in a non-normative appendix; `[R-SER-05]`
  governs the verifier's check under every reading. Not byte-level.

## 4. Verdict

Both repairs do the thing they claim, in normative-vs-summary terms that
are correct for their sites, and hunk 10's enumeration is genuinely
complete. The failure is a sweep failure around hunk 7: the exception the
repair carved into `[R-ERR-04]` was not carried to the three other places
the same duty is stated, one of which (`[R-ERR-03]`) is a normative MUST
four lines above the repair in the same subsection.
