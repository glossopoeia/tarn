# Repair audit — case-adr0106, hunks 1–7

> *Editorial substitution for the repository's vocabulary gate: an ordinary-English
> use of a gate word has been replaced with an exact synonym. The substitution is
> recorded here and changes no finding, quotation or verdict.*

Working transcript. Written as I went; not a summary.

---

## 0. Disclosure

Read:

- `/private/tmp/claude-501/-Users-robertkleffner-Documents-GitHub-tarn/95161ceb-f057-4b49-92d8-298403d066a9/scratchpad/case-adr0106/hunk-01.diff` … `hunk-07.diff` (my seven, and only those).
- `/Users/robertkleffner/Documents/GitHub/tarn/spec/tarn.md`, at these ranges:
  lines 96–116 (§2.1), 130–300 (§2.2–§2.4), 340–380 (§3.1), 421–600 (§4.2–§4.7),
  778–910 (§6.2–§6.4), 943–1160 (§7.2–§7.4), 1513–1600 (§11.1–§11.3),
  1795–1845 (§13.3), 1876–2000 (§14.2–§14.4), 2040–2120 (§15.1–§15.3),
  2268–2475 (§17), 3040–3100 (§20.3), 3391–3530 (§21.1–§21.3 head),
  3519–3576 (§21.3 grep), 3576–3700 (§21.4–§21.6), 3698–3870 (§21.7–§21.9),
  4315–4460 (Appendix G).

Ran (exact commands in §1 below): `wc -l`, `sed -n`, `grep -n`, `awk` over
`spec/tarn.md` only.

Did NOT read: `full.diff`, other auditors' hunk files, `docs/`, `PLAN.md`,
`OPEN-QUESTIONS.md`, `AGENTS.md`, `README.md`, `conformance/`,
`spec/registry.json`, git history/log/diff, the web. Did not list the case
directory.

**Unbidden context that appeared before I began, disclosed as a breach:**

1. A project-instruction pointer (`CLAUDE.md` → `AGENTS.md`) and an index of
   the maintainer's auto-memory files, several of whose one-line descriptions
   concern this project's cleanroom cadence and spec-edit propagation.
2. A runtime environment block containing `git status` and **five recent commit
   subject lines**, several of which name ADR numbers and, in one line each,
   the subject matter of recent decisions — including subject matter that
   overlaps hunks 1, 6 and 7.

Item 2 is the serious one: it is git log, which the access rule forbids. I did
not fetch it; it was placed in my context by the harness. I have not repeated
its contents here and I did not use it to steer any check. Every finding below
is reconstructed from the specification text and the hunk files, and I have
given the derivation for each so the reader can check that no step depends on
those lines. The one place it could have mattered is my treatment of hunk 1's
"reach is per condition" framing and hunk 7's filter argument; in both cases I
derived the rule from `[R-CNT-24]`, `[R-COD-10]` and §21.1 directly and then
cross-checked, and the finding I report on hunk 1 (A-01) is a defect the commit
lines do not mention.

---

## 1. Commands run, verbatim

```
$ wc -l spec/tarn.md
    4529 spec/tarn.md

$ grep -n "^#\{2,5\} " spec/tarn.md            # section map, 200 lines, used for navigation

$ grep -n '`\[R-CNT-06\]`' spec/tarn.md
232, 806, 822, 1284, 1345, 2767, 3482(F1), 3489(F8), 3490(F9), 3491(F10),
3492(F11), 3493(F12), 3494(F13), 3495(F14), 3496(F15), 3497(F16), 3498(F17), 3854

$ grep -n -i "declaration-derived\|designat" spec/tarn.md
167, 168, 441, 445, 447, 819, 976, 1086, 1561, 1896, 1977, 2393, 3088, 3527, 3884, 3885

$ grep -n "R-ENC-04" spec/tarn.md
449, 820, 976, 1087, 1562, 1896, 1978, 2073, 2092, 2392, 2865, 3087,
3484(F3), 3527(L2), 3594(T12), 3885

$ grep -n -i "vacuous\|satisfi[e]*s these\|ranges over" spec/tarn.md
3429, 3434, 3800          # "vacuously" now occurs NOWHERE in the document

$ grep -n "sentinel" spec/tarn.md              # 60 hits, read in full

$ grep -n "identity" spec/tarn.md
2431, 2612, 2632, 2966, 3068, 3249, 3254, 3608(T26), 3641(R9), 4333, 4399, 4422

$ grep -n -i "reach" spec/tarn.md              # 50 hits, read in full
  ... 144, 146  <-- [R-CNF-02], "requirements that reach it" / "a reaching requirement"
  ... 229, 231, 237, 240  <-- [R-CNF-13], the repair
  ... 253, 256, 260  <-- the Note under [R-CNF-13]
  ... 3472  <-- §21.2 preamble

$ awk 'NR>=3480 && NR<=3520 && /^\| F/' spec/tarn.md | wc -l
      36                                        # §21.2 "36 conditions" confirmed
```

Note on hard wrap: every phrase I searched for was chosen short enough not to
wrap (`R-ENC-04`, `designat`, `vacuous`, `identity`, `reach`, `sentinel`). The
one grep whose failure I rely on is `vacuous`, a single unhyphenated word that
cannot span a line break; its zero hits are therefore load-bearing and sound.

Note on `[R-CNF-01]`: the charter's gloss says text inside a `>` blockquote is
non-normative. The document's own rule is narrower — "any text labeled *Note*,
*Example*, or *Rationale*" (line 105–107). §15.1's region-layout display block
is a `>` block but carries no such label, so by the letter of `[R-CNF-01]` it is
normative. I used the document's rule, not the gloss, and flag the difference
because it affected one placement question (hunk 4, §6 below).

---

## 2. Hunk 1 — [R-CNF-13], §2.3, lines 224–252

Heading check: nearest preceding heading is line 134, "2.3 Conformance
classes". Matches the body. No mismatch.

### 2.1 The rule the repair adopts

An implementation must decide, **for each individual malformed condition** —
one register row, not one requirement — whether that condition is asserted
against a file declaring a major other than 1. A condition qualifies exactly
when the invariant it violates is one `[R-CNT-24]` fixes permanently. A reader
must run the qualifying checks on a foreign-major file and reject on that
requirement's own ground; if all of them pass it owes `[R-CNT-07]`'s distinct
capability diagnostic instead. Non-qualifying conditions are not assessed there
at all, so a foreign-major file is not nonconforming by any of them.

The practical bite: a requirement can be **split**. `[R-CNT-06]` is applied in
part (magic, CRC) and not in part (dir_offset, dir_length, generation, file_id,
reserved, committed_file_length) against a major-2 file.

### 2.2 Check 1 — tense and quantifier

Generation: not applicable, no prior/new state here.

Set: the repair ranges over "a **condition** this specification names — one
malformed state, as §21.1 individuates them, and not the requirement that
defines it". The old text ranged over "a requirement of this specification".
That is the whole point of the repair and it is the right direction: under the
old wording "the invariant **its condition** violates" was singular and had no
referent for a requirement stating ten conditions.

Is the repair the normative rule or a restatement? It **is** the normative rule
— `[R-CNF-13]` is the definition of reach. Nothing else defines it. Which makes
check 1's second question the sharp one: does every other place that uses the
predicate use the same quantifier? See §2.5 below. **It does not.**

Sub-quantifier: "as §21.1 individuates them". §21.1 line 3395–3397: "The
register — §21.2 through §21.5 — enumerates every **detectable**
file-conformance violation this specification names: each row is one malformed
condition". So §21.1 individuates only *detectable* violations. `[R-CNF-13]`
ranges over "a condition this specification names", which is wider — §21.7
names conditions with no row (`[R-LIF-01]` immutability, `[R-CNT-18]` nesting,
`[R-COD-06]`'s undisclosed dictionary, `[R-GEO-06]`'s ordinal mapping). For
those, §21.1 supplies no individuation. I chased the consequence: reach governs
(a) what a reader MUST apply and (b) what a §21 row records. Both are empty for
an undetectable condition — there is no check to apply and no row to record it.
So the mismatch is real but inert. **Not raised as a finding.**

### 2.3 Check 2 — citations

- `§21.1` — "one malformed state, as §21.1 individuates them ... and not the
  requirement that defines it". §21.1: "each row is one malformed condition ...
  and the requirement that **defines** it". The repair echoes §21.1's own noun
  phrase exactly. **PASS.**
- `[R-CNT-06]` "states ten". Counted the rows whose Governing-rule cell names
  `[R-CNT-06]` **first** (§21.1: "A Governing rule cell names that requirement
  first; any identifiers following it in parentheses are the further rules the
  condition reads"): F8, F9, F10, F11, F12, F13, F14, F15, F16, F17 = **ten**.
  Cross-checked against `[R-CNT-06]`'s own prose (§6.2 line 813–822): magic;
  CRC; version gate (cross-ref, → F18/`[R-CNT-07]`); flag gates (cross-ref, →
  F19/`[R-CNT-08]`); cfl = F; cfl mod 64 = 0; dir_offset ≥ 16; dir_length ≥ 4;
  dir_offset + dir_length ≤ F − 64; 1 ≤ generation ≤ 2⁶³ − 1; file_id ≠ 0;
  reserved zero. Discounting the two cross-references, ten. **PASS.**
  (Ambiguity noted and resolved: `[R-CNT-06]`'s text also states
  generation ≤ 2⁶³ − 1, whose governing rule is `[R-ENC-03]` (F2's *generation*
  instance), and — **after hunk 2** — the dir-sum overflow, whose governing rule
  is `[R-ENC-04]` (F3's first instance). Under a literal "states" that would be
  twelve. The register's own governing-rule convention gives ten, and both extra
  conditions are non-reaching anyway, so "the other eight" is undisturbed on
  either count. Recorded, not raised.)
- "the trailer magic and the trailer CRC assert invariants `[R-CNT-24]` fixes".
  `[R-CNT-24]` (§6.3 line 843–850): "In every format major version,
  permanently: the final 64 bytes of a file contain the trailer magic at
  F − 64, version_major and version_minor at F − 56, and a CRC-32C at F − 4
  covering bytes [F − 64, F − 4); and the front signature block (§6.1) is
  constant." F8 is the magic at F − 64 **PASS**. F14 is "The u32 at trailer
  offset 60 does not equal the CRC-32C of trailer bytes [0,60)" — offset 60 is
  F − 4, bytes [0,60) is [F − 64, F − 4) **PASS**.
- "`[R-CNT-07]` asks for" a distinct diagnostic. `[R-CNT-07]`: "the diagnostic
  for an unimplemented major **SHOULD** be distinct from both 'not a TARN file'
  and 'corrupt'". "asks for" is a fair rendering of SHOULD; "is owed" is a shade
  strong for a SHOULD but is carried over verbatim from the pre-repair text and
  is not this repair's doing. **PASS (with the note).**
- "`[R-CNT-24]` fixes in every format major version" against `[R-CNT-24]`'s "In
  every format major version, permanently". **PASS.**

### 2.4 Check 3 — normative placement

Lines 224–252 are plain paragraph text carrying `[R-CNF-13]`. Not labeled Note,
Example or Rationale. **Normative. PASS.** The Note that follows (lines 254–264,
labeled **Note**) is non-normative and carries the F14/F5/F15 worked
derivations; the *normative* carrier of "which rows reach" is §21.2's preamble,
which survives hunk 6. So no rule lives only in a Note here.

### 2.5 Check 4 — contradiction in the same passage, including untouched text

I read §2.3 top to bottom, lines 134–263. **`[R-CNF-02]`, the first bullet of
the same subsection, still quantifies reach over requirements** (lines 143–147):

> "a file declaring another major is neither conforming nor nonconforming under
> it save as to the **requirements that reach it** (`[R-CNF-13]`): a reader
> refuses such a file on capability grounds (§6.3, `[R-CNT-07]`), and that
> refusal is not a finding about its bytes, while the failure of **a reaching
> requirement** is."

against the repaired `[R-CNF-13]`:

> "A **condition** this specification names — one malformed state, as §21.1
> individuates them, **and not the requirement that defines it** — **reaches** a
> file declaring a format major other than 1 when, and only when …"

`[R-CNF-02]` is normative (a bulleted class definition, not a Note), it cites
`[R-CNF-13]` as its authority, and it uses "reach" as a predicate of
requirements — the predicate `[R-CNF-13]` was rewritten to abolish. After the
repair, `[R-CNF-13]` defines no such predicate, so `[R-CNF-02]`'s term is
undefined by its own citation.

I worked all three readings an implementer can take:

(a) Read "requirement" as loose for "condition". Correct behaviour, requires
    ignoring the word the sentence uses.
(b) Lift condition-reach to requirements existentially — a requirement reaches
    if **any** of its conditions does. Then `[R-CNT-06]` reaches, and by
    `[R-CNF-02]` a foreign-major file is nonconforming as to it — all ten
    conditions, not two. A major-2 file with a good magic, a good trailer CRC
    and `file_id = 0` is then **nonconforming** (F12), where reading (a) makes
    it an unjudged file refused on capability grounds with `[R-CNT-07]`'s
    distinct diagnostic owed.
(c) Lift it universally — a requirement reaches if **all** of its conditions do.
    Then `[R-CNT-06]` does not reach at all (eight of ten do not), so F8 and F14
    are **not** applied to a foreign-major file. That flatly contradicts §21.2's
    preamble, which lists F8 and F14 as reaching.

(c) is self-refuting, which is evidence this is a defect and not harmless
legacy phrasing. (b) is not: it is a coherent reading of a normative sentence
that produces a different verifier verdict on a concrete file. **Raised: A-01.**

Other contradiction candidates I looked for in §2.3 and found not to be ones:

- `[R-CNF-13]`'s "A reader MUST apply every reaching condition … whatever major
  it declares" against F6's and F1's carve-out ("the obligation binds a reader
  holding those bytes resident, and a reader that would have to fetch them MAY
  defer or omit the check (`[R-CNT-04]`)"). A MUST against a MAY-omit, and F6
  is one of the four reaching rows. But the MUST is about *applicability across
  majors*, not about suspending the check's own residency precondition, and the
  identical tension existed word-for-word in the pre-repair text ("every
  reaching **requirement**"). Not introduced here. Not raised.
- `[R-CNF-11]`'s "*cannot establish*" list against `[R-CNF-13]`'s "A verifier
  that establishes such a failure reports *nonconforming*". `[R-CNF-11]` already
  says "An established violation takes priority: a verifier that has established
  any violation reports *nonconforming*, however many requirements it was unable
  to check". Consistent. **PASS.**
- F6's "a verifier holds no such exemption (§2.3)" against `[R-CNF-11]`'s "checks
  every file-level requirement — including those ordinary readers are exempted
  from". Consistent. **PASS.**

### 2.6 Check 5 — exhaustive claims

Flagged every completeness word in the inserted text:

1. "when, and only when" — an iff. Tested below in §3 by deriving the whole of
   §21.2 against it. Holds.
2. "states ten" / "the other eight" — verified above. Holds.
3. "A reader MUST apply **every** reaching condition" — the four rows are F1,
   F6, F8, F14, all reader/open. Holds.
4. "**Every other** condition this specification names **is one of a structure
   this text defines for format major 1 alone**." Tried to falsify. Two
   falsifiers, one of them supplied by the document's own adjacent Note:
   - **F5.** The Note directly under the repair says: "F5 does not reach
     although **its subject is the physical file size, which no major can
     redefine**". A structure no major can redefine is not "a structure this
     text defines for format major 1 alone". What is major-1's about F5 is the
     *128-byte floor* — the invariant — not the structure.
   - **F18.** version_major sits at F − 56 in every major by `[R-CNT-24]`, and
     §21.6/§21.2 call the value 0 "permanently invalid in **every** format major
     version". F18's structure is fixed in every major, not defined for major 1
     alone.
   The rule's *test* (sentence 1) is stated over **invariants**; the complement
   (sentence 4) is asserted over **structures**. The Note exists specifically to
   insist that "the test is the invariant a condition violates, not the fields it
   reads" — and the closing sentence of the rule it annotates does the opposite.
   **Raised: A-03.**
5. "no §21 row restating it records such a file" — a universal over rows. I
   derived all 36 F rows (§3) and it holds.

### 2.7 Check 6 — what is left unconstrained

Structure the repair governs: the set of conditions §21 names, considered
against a foreign-major file. Members and whether a rule fixes each:

| member | fixed by |
|---|---|
| the four reaching conditions F1, F6, F8, F14 | `[R-CNF-13]` sentence 3 + §21.2 preamble |
| the other 32 §21.2 conditions | `[R-CNF-13]` sentence 4 (not assessed) |
| §21.3/§21.4/§21.5 conditions | same sentence; and unreachable in practice, a foreign-major file never reaching layer access |
| F18 / version_major = 0 | outside the premise — §21.2 preamble states this; `[R-CNF-13]` does not, and its sentence-4 gloss is false of F18 (A-03) |
| §21.6's defined non-violations | not conditions; `[R-CNF-13]` sentence 4 sweeps them harmlessly |
| conditions with no row (§21.7) | not individuated by §21.1; inert, see §2.2 |
| the reader's *diagnostic* obligation when all four pass | `[R-CNT-07]`, cited |
| the verifier's *verdict* when one fails | `[R-CNF-13]` sentence 3, "*nonconforming*" |
| the verifier's verdict when all four pass | `[R-CNF-11]`, "*cannot establish*" |

No member is unpinned by the repair's own terms. The unpinned thing is one
level up: the *predicate itself*, used at a different arity in `[R-CNF-02]`
(A-01).

### 2.8 Check 7 — argument by analogy

The repair's only warrant-by-pointer is "as §21.1 individuates them".

| | governing verb | ranges over |
|---|---|---|
| repair | "A **condition** this specification **names**" | conditions the specification names |
| `[R-CNT-06]` example | "`[R-CNT-06]` **states** ten" | conditions a requirement states |
| §21.1 | "**enumerates** every **detectable** file-conformance violation this specification **names**: each row **is** one malformed condition" | detectable violations |

"names" against "names" matches; "condition" against "row" matches by §21.1's
identification. The mismatch is "conditions the specification names" against
"**detectable** … violations this specification names" — §21.1's set is a proper
subset. Tested member by member against the §21.7 residue (immutability, ordinal
mappings, nesting, undisclosed dictionary): each is inert under reach, as
derived in §2.2. **Analogy reported, does not bite.**

"`[R-CNT-06]` states ten" is one sentence carrying the analogy for **ten**
members, so I tested each separately: F8 and F14 assert `[R-CNT-24]`-fixed
invariants; F9, F10, F11, F12, F13, F15, F16, F17 assert bounds on fields at
trailer offsets 12–60, which `[R-CNT-24]` expressly lets a future major
redefine ("A future major MAY redefine only the remaining 48 trailer bytes":
64 − 8 magic − 4 version − 4 CRC = 48, i.e. offsets 12 through 60). F15's
reserved bytes at [56,60) lie inside that 48, which is why the Note singles it
out. Each of the ten checks out individually.

---

## 3. Hunk 6 — §21.2 preamble, lines 3470–3479 (a deletion)

Heading check: nearest preceding heading is line 3470, "21.2 File-scope
violations". Matches. No mismatch.

### 3.1 What was deleted

`- and where this restatement and that rule diverge, the rule governs (§21.1).`

(plus the reflow that inserted "condition by condition" and split the sentence.)

### 3.2 The rule the repair adopts

Reach is settled row by row from `[R-CNF-13]`, and §21.2's preamble reports the
result rather than asserting it as an independent rule. The named result is F8,
F14, F6 and F1 (both instances) and nothing else, with F18 excluded not by the
test but by the premise.

### 3.3 What the deleted words carried — and does anything still carry it

Two things.

**(i) The characterisation "this restatement."** §21.1 says "each **row**
*restates* its governing rule", and separately extends the idea to §21.6: "§21.6's
entries restate their governing rules on the same terms a row does". A
subsection *preamble* is neither. So after the deletion nothing in the document
says §21.2's preamble is a restatement of anything.

**(ii) The precedence "the rule governs".** §21.1's precedence clause is stated
twice and both times expressly scoped:

> "where a **row** and the rule it cites diverge, **the rule governs**"
> "where such an **entry** [§21.6's] and the rule it cites diverge, the rule
> governs there too"

Neither covers a preamble. The document went to the trouble of extending
precedence to §21.6's non-row entries and did **not** extend it to preambles,
and hunk 6 removed the local sentence that had been doing that job. So §21.2's
preamble is now the one restating passage in §21 with no precedence rule over
it — while being normative text (not a Note) that makes an exhaustive claim
("and no other row").

Compare the pattern elsewhere: §21.9 subordinates itself explicitly — "The hard
limits it restates are a finding aid rather than an inventory — each is
normative where the structure forcing it is defined." §21.2's preamble now has
no such clause.

**Raised: A-02.** But see next: I could not make the gap bite today, because I
derived the enumeration and it is correct. So A-02 is a latent-precedence gap,
not a live divergence, and I mark it non-byte-level on that ground.

### 3.4 Deriving reach for all 36 F rows, to test "and no other row"

`[R-CNT-24]` fixes, in every major: (i) trailer magic at F − 64; (ii)
version_major and version_minor at F − 56; (iii) CRC-32C at F − 4 over
[F − 64, F − 4); (iv) the front signature block constant; (v) the trailer is 64
bytes and does not grow.

| row | invariant it asserts | `[R-CNT-24]`-fixed? |
|---|---|---|
| F1 | a signature constant stored byte-reversed — front block [0,8) and trailer magic | yes, (iv) and (i) — **reaches** |
| F2 | u64 field ≤ 2⁶³ − 1 (dir_offset, dir_length, cfl, generation, record extents) | no |
| F3 | a u64 offset+length sum does not wrap | no |
| F4 | layer names unique | no |
| F5 | F ≥ 128 | no — see below |
| F6 | front signature block byte-identical to the constant | yes, (iv) — **reaches** |
| F7 | nothing between directory end and trailer | no |
| F8 | trailer magic at F − 64 | yes, (i) — **reaches** |
| F9 | dir_offset ≥ 16 | no (offset 24, redefinable) |
| F10 | dir_offset + dir_length ≤ F − 64 | no |
| F11 | generation ≥ 1 | no (offset 16) |
| F12 | file_id ≠ 0 | no (offset 48) |
| F13 | cfl multiple of 64 | no |
| F14 | u32 at trailer 60 = CRC-32C of [0,60) | yes, (iii) — **reaches** |
| F15 | trailer [56,60) zero | no — inside the redefinable 48 |
| F16 | dir_length ≥ 4 | no |
| F17 | cfl = transport size | no |
| F18 | version_major ≠ 0 | premise excluded (declares no major) |
| F19 | incompat lane clear | no (flags at offset 12) |
| F20 | directory CRC | no |
| F21–F36 | directory/record/user-metadata structure | no, all major-1 structures |

F5 needed care because the Note pre-empts the objection and I wanted to test the
Note rather than take it. The reach premise is "a file **declaring** a format
major other than 1", which presupposes a readable version_major at F − 56, hence
F ≥ 64. For 64 ≤ F < 128 the file can carry a valid magic at F − 64 and a valid
CRC at F − 4 — no `[R-CNT-24]` invariant is broken — while F5 fires. So F5's
invariant is not one `[R-CNT-24]` fixes. The Note is right. Likewise a file with
F = 100 breaks F13 and F5 and no fixed invariant.

**Result: exactly F1, F6, F8, F14.** The preamble's list is correct, including
"both of F1's instances" (front block [0,8) is fixed by (iv), trailer magic by
(i)) and "no other row". **No live divergence.**

### 3.5 Check 1 — quantifier

"Which **rows** reach" against `[R-CNF-13]`'s "A **condition** … reaches".
§21.1: "each row is one malformed condition". Same set. **PASS.**

"condition by condition" is the new phrase and matches `[R-CNF-13]`'s new arity
exactly. **PASS** — this is the half of the repair that lands.

One granularity wobble, recorded and not raised: the same sentence decides
reach "condition by condition" and then reports "both of F1's **instances**".
Instances are not conditions (§21.1: "The **Instances** column enumerates what a
conformance corpus builds for that row"), so `[R-CNF-13]` yields no
instance-level verdict. It is harmless because both of F1's instances assert
fixed invariants, so "F1 reaches" entails both; and the same sentence names F6
at row granularity, so the mixed granularity is stylistic. If either of F1's
instances had asserted a non-fixed invariant this sentence would have had no
rule to appeal to — worth a maintainer's eye, but not a defect today.

### 3.6 Check 2 — citations

- `[R-CNF-13]` (§2.3) "decides which rows reach" — yes, it is the definition.
  **PASS.**
- `[R-CNT-24]` "fixes in every major" — verified in §2.3 above. **PASS.**
- §21.6, cited for "version_major = 0 … is permanently invalid in every one".
  §21.6's closing text: "version_major = 0, **permanently invalid in every
  format major version** (F18, `[R-CNT-07]`)". **PASS**, near-verbatim.
- F18's row: "Trailer version_major is 0, a permanently invalid major in every
  format major version | `[R-CNT-07]`". **PASS.**
- "36 conditions": `awk` count = 36 rows F1–F36. **PASS.**

### 3.7 Check 3 — normative placement

Preamble prose, no Note/Example/Rationale label. Normative. **PASS.** Which is
precisely why A-02 matters: an unsubordinated normative enumeration.

### 3.8 Check 4 — contradiction in the passage

Read §21.1 entire (3393–3468) and §21.2's preamble and all 36 rows.

- §21.1's specialization sentence: "Some rows are strict specializations of
  others — F1 of F6 and of F8, F35 of F36, L24 of L25". F1 of F6 and of F8 is
  exactly the F1/F6/F8 trio the preamble names as reaching, and the preamble
  names all three rather than only the narrower one — correct, since reach is a
  property of each condition, not a recording rule. No contradiction.
- I checked whether the designation hunks create a new unlisted specialization
  (F3's dir instance ⊂ F10, F3's record instance ⊂ F32, since a sum above
  2⁶³ − 1 necessarily exceeds F − 64 for any F ≤ 2⁶³ − 1). The F3/F32 pair
  predates all seven hunks (§7.2 already made "an overflowing sum" a validity
  error before hunk 3), so §21.1's list was already illustrative — its opening
  word is "**Some**", and its operative clause ("a file exhibiting a
  specialization is recorded against the narrower row") is general. Not a
  defect, and not this repair's. **Not raised.**
- No carve-out, MUST/MAY collision, or old-wording-only sentence found in the
  preamble or §21.1.

### 3.9 Check 5 — exhaustive claims

"and no other row" — falsification attempted row by row in §3.4. Holds.
"36 conditions" — verified. Holds.
"F18 is not an exception but a case outside the premise" — verified against
§21.6 and `[R-CNT-07]`. Holds.

### 3.10 Check 6 — what is left unconstrained

Structure: §21.2's preamble as a whole. Its members: the outcome class
(reject-file — stated), the condition count (36 — stated and verified), the
reach enumeration (stated and verified), F18's status (stated), and — formerly —
the precedence of the enumeration against `[R-CNF-13]` (**no longer stated by
anything**). That last is A-02. Nothing else in the preamble is unpinned.

### 3.11 Check 7 — analogy

The preamble justifies itself by pointing at `[R-CNF-13]`: "is decided by
`[R-CNF-13]` (§2.3), condition by condition. **Deriving** it there **yields** …".

| | governing verb | ranges over |
|---|---|---|
| preamble | "Which rows **reach**" / "Deriving it there **yields**" | §21.2's rows |
| `[R-CNF-13]` | "A condition … **reaches** … when, and only when, the invariant it **violates** is one `[R-CNT-24]` **fixes**" | conditions the spec names |

Rows ↔ conditions by §21.1. Same set, same verb ("reach"/"reaches"). **PASS.**
Tested separately against each of the five items the one sentence carries (F8,
F14, F6, F1-front-block, F1-trailer-magic): each is a condition or an instance
of one whose asserted invariant is `[R-CNT-24]`-fixed. All five hold.

---

## 4. Hunk 2 — [R-CNT-06], §6.2, lines 816–823

Heading check: nearest preceding heading line 778, "6.2 Trailer". Matches.

### 4.1 The rule the repair adopts

`dir_offset + dir_length` is a quantity a reader is obliged to **form** and to
check against 2⁶³ − 1 before using it, rather than an expression written only
inside a comparison. Concretely: a trailer with dir_offset = 2⁶³ − 1 and
dir_length = 2⁶³ − 1 is reject-file on the overflow itself, and a reader must
not evaluate the wrapped sum.

This matters because `[R-ENC-04]` says so in terms: "A designation is express,
made by the section that defines the quantity; **an expression this
specification writes only inside a comparison, and names nowhere, is not a
designated quantity and no reader is obliged to form it.**" Before this hunk,
§6.2 wrote `dir_offset + dir_length ≤ F − 64` and named the sum nowhere. F3's
first instance therefore had no obligation behind it. The repair is substantive
and correct.

### 4.2 Checks 1, 2, 5, 7

- **Quantifier.** "that sum" — antecedent is `dir_offset + dir_length`, the only
  sum in the clause (F − 64 is a difference). Singular, one quantity, one
  trailer. Matches F3's instance cell verbatim: "dir_offset + dir_length".
  **PASS.**
- **Citation `[R-ENC-04]`.** Read at line 438–448. It designates "a
  declaration-derived sum or product of integers obtained from a file (offsets
  plus lengths, grid counts, tile counts, sample-position counts, ordinals)" —
  "offsets plus lengths" is this case exactly. Consequence "a validity error at
  the owning scope"; §6.2 says "The owning scope of the front signature block
  and the trailer is the file" and "Any failure is reject-file"; F3's outcome is
  reject-file. All three agree. **PASS.**
- **Exhaustive claims.** None added. No "every", "only", "the two", count, or
  closed list in the inserted words.
- **Analogy.** "**under** `[R-ENC-04]`" is a pointer, not an analogy — no
  "exactly as", "the same way", "likewise". Verbs compared anyway: repair "that
  sum **being** a declaration-derived quantity"; `[R-ENC-04]` "any quantity this
  specification **designates** a declaration-derived sum or product". Same noun
  phrase, and "being … under X" is the document's established designation idiom
  (§11.2 "These products **are** declaration-derived quantities under
  `[R-ENC-04]`"; §14.2 "These products and sums **are** declaration-derived
  quantities under `[R-ENC-04]`"; §14.3 "**is** a declaration-derived quantity
  under `[R-ENC-04]`"). Same form, same set. **PASS.**

### 4.3 Check 3 — normative placement

Inside `[R-CNT-06]`'s body paragraph at §6.2. Not a Note. **PASS.** Also checked
that no Note elsewhere already carried this and was left standing: `grep -n
"declaration-derived"` gives 819 (this hunk), 976 (hunk 3), 1086 (hunk 4), 1561,
1896, 1977, 3884 — none of which is a Note-labelled block except 3884–3885
(§22.2 security prose, plain text: "Every declaration-derived sum and product
`[R-ENC-04]` designates is overflow-checked before use") which is a general
claim now made *more* true by these three hunks, not less. **PASS.**

### 4.4 Check 4 — contradiction

Read §6.2 entire (778–828) and §6.3 (829–870).

- `[R-CNT-06]`'s ordering clause ("A reader MUST validate, **in order**: the
  trailer magic; the trailer CRC; the version gate … and then, those gates
  passed, MUST validate all of the following **before acting on the fields
  involved**"). `[R-ENC-05]` bars allocating/seeking on an integer before its
  covering checksum verifies; the trailer CRC is validated second. The
  designation adds a check inside the post-gate list, so it inherits the
  ordering. No collision. **PASS.**
- `[R-CNT-05]`'s parenthetical "(readers check neither, their check being the
  **dir-bounds rule** of `[R-CNT-06]`)" — still true; the designation is part of
  the dir-bounds rule. **PASS.**
- No carve-out, no MAY, nothing written to be true only under the old wording.

### 4.5 Check 6 — what else in this structure is unconstrained

Structure: the 64-byte trailer, every quantity it carries, from §6.2's layout
table.

| field | pinned by |
|---|---|
| trailer magic [0,8) | F8 / `[R-CNT-06]`; F1 for the reversed form |
| version_major | F18 (=0), `[R-CNT-07]` gate |
| version_minor | `[R-CNT-07]` ("MUST NOT reject a file for its version_minor"), `[R-CNT-26]` SHOULD |
| flags | F19 (incompat lane), `[R-CNT-08]` (ignore lane) |
| generation | F11 (≥1), F2 (≤2⁶³−1 via `[R-ENC-03]`) |
| dir_offset | F9 (≥16), F2 |
| dir_length | F16 (≥4), F2 |
| **dir_offset + dir_length** | F10 (≤ F−64), **F3 — pinned by this hunk** |
| committed_file_length | F13 (mult of 64), F17 (= F), F2 |
| file_id | F12 (≠0) |
| reserved [56,60) | F15 |
| trailer CRC [60,64) | F14 |

Every quantity the trailer carries is fixed by some rule, and the sum this hunk
designates was the only unpinned one. **No sibling left unpinned.** This is the
check that caught the compressed-frame defect the charter describes, and here it
comes back clean.

---

## 5. Hunk 3 — [R-CNT-13], §7.2, lines 972–980

Heading check: nearest preceding heading line 943, "7.2 Record framing".
Matches.

### 5.1 The rule the repair adopts

`extent_offset + extent_length` on **any** record's extent slot is a quantity a
reader must form and bound at 2⁶³ − 1, with the error taken at the scope the
record governs.

### 5.2 Checks

- **Quantifier.** The sentence's subject is "The **extent slot**
  (extent_offset, extent_length)" of a record, and the sentence itself
  distributes the outcome across record kinds: "the layer for a layer record and
  for sub-records, the file for other top-level records". So the designation
  covers three of the register's enumerated quantities at once:
  - F3 instance 2 — "non-layer top-level record extent_offset + extent_length"
  - L2 instance 1 — "layer record extent_offset + extent_length"
  - L2 instance 2 — "sub-record extent_offset + extent_length"
  All three match the row cells word for word. **PASS.**
- **Citation `[R-ENC-04]`.** "offsets plus lengths" again. Outcome: `[R-ENC-04]`
  says "at the owning scope"; §7.2 says "at the scope the record governs
  (§7.3)". Cross-checked the two are the same mapping: §7.4 "The owning scope of
  a layer record's inline payload is the layer"; §15.1 "The owning scope of a
  layer's tile index is the layer"; §7.2 assigns file scope to non-layer
  top-level records. F3 = reject-file, L2 = reject-layer. Agree. **PASS.**
- **Placement.** `[R-CNT-13]` body paragraph, not a Note. **PASS.**
- **Exhaustive claims.** None added.
- **Analogy.** Same "being a declaration-derived quantity under `[R-ENC-04]`"
  idiom as hunk 2. Verbs: "is a declaration-derived quantity" vs `[R-ENC-04]`'s
  "designates a declaration-derived sum". Same set. **PASS.** Tested separately
  against each of the three row-instances above — all three are "an offset plus
  a length taken from the file", the exact category `[R-ENC-04]` names. All
  three hold.
- **Contradiction.** Read `[R-CNT-13]` entire, and §7.3, §7.4. The sentence
  already said "or an **overflowing sum** … is a validity error", so this hunk
  adds the `[R-ENC-04]` hook rather than a new condition; it cannot collide with
  the surrounding bounds clauses because it is the same condition they already
  named. `[R-CNT-13]`'s later overlap clauses (F33, F7) are about a different
  predicate. **PASS.**
- **What else is unconstrained** (structure = the extent slot):

  | slot state | pinned by |
  |---|---|
  | (0, 0) | licensed: "means no extent" |
  | exactly one half zero | F30 / L15 |
  | extent_offset in 1–15 | F31 / L16 |
  | offset or length > 2⁶³ − 1 | F2 / L1 (`[R-ENC-03]`) |
  | **offset + length > 2⁶³ − 1** | **F3 / L2 — this hunk** |
  | offset + length > F − 64 | F32 / L17 |
  | overlap with another structure | F7, F33 |

  Nothing left open.

**Assessment.** This hunk is confirmatory rather than substantive — §7.2 already
made the overflowing sum a validity error in its own right, so no reader
obligation changes. It makes F3's and L2's parenthetical `[R-ENC-04]` citation
resolve. Correct, sound, no defect found.

---

## 6. Hunk 4 — [R-CNT-17], §7.4, lines 1083–1090

Heading check: nearest preceding heading line 1046, "7.4 The layer record".
Matches.

### 6.1 The rule the repair adopts

`entry_count × 20 + ⌈entry_count / 2¹⁶⌉ × 4` — the index region's size — is a
quantity a reader must form and bound at 2⁶³ − 1, at layer scope. Before, it was
written only inside the equality `extent_length MUST equal …` and named nowhere,
so by `[R-ENC-04]`'s own express-designation clause **no reader was obliged to
form it**, and L2's last instance had nothing behind it. Substantive repair.

### 6.2 Checks

- **Quantifier.** "that expression" — antecedent is the whole sum. L2's cell:
  "entry_count × 20 + ⌈entry_count/2¹⁶⌉ × 4". Character-for-character the same
  expression. **PASS.**
- **Citation `[R-ENC-04]`.** "grid counts, tile counts" is the closest category
  named; the general clause is "a declaration-derived sum or product of integers
  obtained from a file", which this is (entry_count comes from the layer
  record). Outcome at owning scope = layer (§7.4: "The owning scope of a layer
  record's inline payload is the layer"); L2's outcome is reject-layer at layer
  access. **PASS.**
- **Placement.** `[R-CNT-17]` body, not a Note. **PASS.** I checked whether
  §15.1 rather than §7.4 is "the section that defines the quantity" — §15.1
  writes the two terms separately inside an unlabeled `>` display block (which
  is normative under `[R-CNF-01]`'s label test, see §1), but the **sum** as a
  single named quantity is written only in `[R-CNT-17]`. So §7.4 is the defining
  section and the designation is correctly placed. **PASS.**
- **Exhaustive claims.** None added. (The pre-existing "(and 0 when entry_count
  is 0)" is redundant — the formula already yields 0 at entry_count = 0 — but
  harmless and untouched.)
- **Analogy.** Same designation idiom. Verbs: "that expression **being** a
  declaration-derived quantity" vs `[R-ENC-04]` "any quantity this specification
  **designates** a declaration-derived sum or product". Same set — one
  expression, one layer, one quantity. **PASS.**
- **Contradiction.** Read §7.4 entire including the worked example. The example
  computes "4 × 20 + ⌈4 / 2¹⁶⌉ × 4 = 84" — consistent, and it is labeled
  **Example** so non-normative anyway. `[R-CNT-23]`'s constraint table and
  `[R-CNT-16]` do not touch this quantity. No collision found.

### 6.3 Check 6 — the sweep, and this is the one the charter asked about

L2's cell enumerates **nine** quantities. For each, is there an express
designation?

| L2 instance | designated where |
|---|---|
| layer record extent_offset + extent_length | §7.2, `[R-CNT-13]` — **hunk 3** |
| sub-record extent_offset + extent_length | §7.2, `[R-CNT-13]` — **hunk 3** |
| N = ∏⌈Eᵢ/Tᵢ⌉ | §11.2, `[R-GEO-03]` line 1561 |
| P = ∏Tᵢ | §11.2, `[R-GEO-03]` |
| N·P | §11.2, `[R-GEO-03]` ("total sample-position count is N · P") |
| C·N | §11.2, `[R-GEO-03]` ("addressed-tile count … C · N for a planar layer") |
| P·Q (dominating V = P·C) | §14.2, `[R-SER-02]` line 1896; V by §14.3 `[R-SER-07]` line 1977 |
| P·Bᶜ | §14.2, `[R-SER-02]` |
| entry_count × 20 + ⌈entry_count/2¹⁶⌉ × 4 | §7.4, `[R-CNT-17]` — **hunk 4** |

All nine now designated. **Hunk 4 closes the last gap in L2.** The parenthetical
"(which dominates the max disk ordinal (C−1)·N + (N−1))" and "(which dominates
V = P·C)" are handled by domination, so the dominated quantities need no
separate designation.

Sub-terms of hunk 4's expression: `entry_count × 20` and
`⌈entry_count / 2¹⁶⌉ × 4` are each dominated by the sum, so designating the sum
is sufficient — if either overflows, so does the sum. No sibling left unpinned.

F3's two instances: both designated (hunks 2 and 3). T12 ("A non-sentinel
tile-index entry's offset + length exceeds 2⁶³ − 1", governing rule
`[R-IDX-03]` with `[R-ENC-04]` parenthetical) — checked, and it is covered by
§15.2's "`[R-ENC-03]`'s value-domain rule and `[R-ENC-04]`'s **sum rule** apply
to the fields of non-sentinel entries only" plus §15.3's table row "offset +
length overflows … *structural*: reject-tile", which imposes the reader
obligation directly. Not a gap.

**So the three designation hunks together sweep every `[R-ENC-04]`-governed row
in the register: F3 (both instances), L2 (all nine), T12 (already covered).**
Clean.

---

## 7. Hunk 5 — §17 preamble, lines 2269–2275 (a deletion)

Heading check: nearest preceding heading line 2268, "17. Codecs and Filters".
Matches.

### 7.1 What was deleted

> "Every rule in this section ranges over **stored** tiles — a tile whose index
> entry is the sentinel is not stored (§3.1, `[R-IDX-02]`), carries no payload
> under any codec, and satisfies these rules vacuously."

### 7.2 The rule the repair adopts

Each rule in §17 carries its own quantifier; the section imposes none globally.
An implementation reads "stored tile" where §17 says stored tile and "addressed
tile" where §17 says addressed tile, and does not lift a section-wide "stored"
over the top of `[R-COD-07]`.

### 7.3 What the deleted words carried, and whether it still stands

Three claims. Taken one at a time:

**(a) "Every rule in this section ranges over stored tiles."** This was
**false**, and its falseness was the reason to delete it. `[R-COD-07]` says:
"Writers MUST NOT declare this codec for a layer **any of whose addressed
tiles'** decoded size exceeds 0x7E000000 bytes". L44 restates it: "Codec 4 (lz4)
declared on a layer **any of whose addressed tiles'** decoded size exceeds
0x7E000000". And `[R-COD-07]`'s Note (non-normative but explicit): "The cap is
quantified over the layer's ***addressed*** tiles, so a layer that addresses
none … satisfies it whatever its tile shape declares". §21.9 also leans on it:
"*Decoded size of one tile* ranges over a layer's **addressed** tiles, stored or
not, **exactly as `[R-COD-07]`'s cap is**". A section preamble asserting that
every rule ranges over *stored* tiles collided with all four. The deletion
removes a live contradiction. **Good repair.**

**(b) "a tile whose index entry is the sentinel is not stored".** Still carried,
and carried more strongly, by §3.1's definition (line 352–354): "A tile is
*stored in a generation* **if and only if** that generation's tile-index entry
for it is not the sentinel (§15)". An iff. Also §13.3 and §21.6's row ("An index
entry is the sentinel | The tile is addressed but not stored"). **Nothing
lost.**

**(c) "carries no payload under any codec, and satisfies these rules
vacuously."** `grep -i vacuous` now returns **zero hits document-wide**. So the
explicit vacuous-satisfaction licence is gone. I then went rule by rule through
§17 asking whether any rule could now be read as biting an unstored tile:

| rule | its own quantifier | unstored tile? |
|---|---|---|
| `[R-COD-01]` | "A **stored tile's** bytes are produced …" | excluded by its own words |
| `[R-COD-02]` | "**Every stored tile** is independently decodable …" | excluded |
| `[R-COD-03]` | layer's codec field value | not tile-ranged |
| `[R-COD-04]` | "A **non-sentinel** index entry's length … MUST equal" | excluded, and in bold |
| `[R-COD-05]` | "The **stored bytes** are exactly one DEFLATE stream" | excluded |
| `[R-COD-06]` | "The **stored bytes** are exactly one … frame"; dictionary/window/content-size all predicated on a frame existing | excluded |
| `[R-COD-07]` | "any of whose **addressed** tiles" | deliberately includes unstored — and this is the one (a) contradicted |
| `[R-COD-08]` | "the **stored bytes** MUST decode to exactly the decoded size" | excluded |
| `[R-COD-09]` | layer's filter field value | not tile-ranged |
| `[R-COD-10]` | describes the transform; "A writer that **filters** with any other stride violates this rule" | a writer filters only what it stores |
| `[R-COD-11]` | verifier/layer | not tile-ranged |

Every rule carries its own quantifier and none of them bites an unstored tile.
Cross-checked the register: T13, T14, T17–T22, T24, T25 all say "stored tile",
"stored bytes", "the frame", or "non-sentinel index entry"; T26 says "Filter 2
**applied**"; L44 says "addressed". No row depends on the deleted licence.

**Nothing the deleted sentence carried is now uncarried.** No finding.

### 7.4 Checks 1–7 for hunk 5

- **1 Quantifier.** The repair removes a quantifier rather than restating one.
  Post-deletion the section-level quantifiers are exactly the per-rule ones
  tabulated above, and they now agree with §21.9's "addressed … exactly as
  `[R-COD-07]`'s cap is". **PASS.**
- **2 Citations.** The deletion removes citations (§3.1, `[R-IDX-02]`) rather
  than adding any. Both cited passages still stand and still say what the
  deleted sentence claimed (§7.3(b)). **PASS.**
- **3 Placement.** What remains ("The owning scope of a layer's codec and filter
  declarations is the layer; the owning scope of one **stored tile's** payload
  under them is the tile (§2.4)") is normative and still assigns an owning scope
  to every structure §17 defines, as `[R-CNF-08]` requires. **PASS.**
- **4 Contradiction.** The deletion *resolves* one (with `[R-COD-07]`, L44,
  §21.9). I looked for a new one and found none.
- **5 Exhaustive claims.** The deletion removes the exhaustive claim ("Every rule
  in this section"). Nothing exhaustive remains in the preamble.
- **6 Unconstrained siblings.** Structure = §17's declared objects: the codec
  declaration (scoped: layer), the filter declaration (scoped: layer), a stored
  tile's payload (scoped: tile). All three scoped. An unstored tile has no
  payload, so there is no fourth member wanting a scope. **PASS.**
- **7 Analogy.** None in the surviving text.

---

## 8. Hunk 7 — Appendix G item 5, lines 4394–4406

Heading check: nearest preceding heading line 4315, "Appendix G —
Reproducible-writer profile (non-normative)". Matches.

### 8.1 The rule the repair asserts

Filter 2 (byte-shuffle) is the identity transform exactly in two cases — stride
s = 1, or n = L/s = 1 — and in every other case it changes the bytes of every
tile it is applied to. An adopter of the profile must pin the filter value
regardless.

### 8.2 Verifying the property against `[R-COD-10]`, at every case that rule names

`[R-COD-10]`: "The shuffle stride s is the channel's element size for a planar
tile and the sample stride Q for an interleaved tile (§14.2); for a packed
boolean plane s = 1 and the filter is the identity. The decoded image's length L
is divisible by s in every case (§14). Viewing the image as **n = L/s**
consecutive groups of s bytes, the filtered image places **byte i of group j at
offset i · n + j** … the inverse restores byte i · n + j to offset **j · s + i**."

Identity iff i·n + j = j·s + i for all 0 ≤ i < s, 0 ≤ j < n.

- s = 1 ⇒ i ≡ 0 ⇒ new offset = j, old offset = j·1 + 0 = j. **Identity.**
- n = 1 ⇒ j ≡ 0 ⇒ new offset = i·1 = i, old offset = 0·s + i = i. **Identity.**
- s ≥ 2 and n ≥ 2: take i = 1, j = 0. New offset = n ≥ 2; old offset = 1.
  n ≠ 1, so the byte moves. **Not the identity.**

So "the identity **exactly** where … s = 1 … and equally where … n = 1" is
**correct and exhaustive**. The "exactly"/"and equally" completeness claim
survives falsification.

Per case `[R-COD-10]` names:
- **planar numeric**: s = Bᶜ, L = P·Bᶜ, so n = P. Identity iff Bᶜ = 1 (uint8 /
  int8) or P = 1.
- **interleaved**: s = Q, L = P·Q, so n = P. Identity iff Q = 1 (a single 1-byte
  channel) or P = 1.
- **packed boolean plane**: s = 1 by fiat, always the identity — the case
  `[R-COD-10]` states outright. ✓

Is n = 1 reachable by a legal geometry? `[R-GEO-01]`: "each of its d dimensions
has … a tile extent **Tᵢ ≥ 1**". So P = ∏Tᵢ = 1 whenever every tile extent is 1.
A rank-1 layer, T₀ = 1, E₀ = 5, one float32 planar channel: P = 1, s = 4, L = 4,
n = 1 — filter 2 is the identity, and the **old** text ("it changes the stored
bytes of any tile whose shuffle stride exceeds 1") was flatly wrong there. The
repair fixes a real defect. Confirmed.

### 8.3 Falsifying "elsewhere it changes the stored bytes of every tile it touches"

Degenerate geometry does not falsify it (I tried: rank 1, T₀ = 2, no help).
Degenerate **content** does.

Planar layer, rank 1, T₀ = 2, E₀ = 2, one uint16 channel, fill 0, codec 1.
P = 2, s = Bᶜ = 2, L = 4, n = 2 — so s ≥ 2 and n ≥ 2, squarely in "elsewhere".
Values 0x0100 and 0x0001, little-endian: decoded image = `00 01 01 00`.
Groups g₀ = (00,01), g₁ = (01,00). Filtered, at offset i·n + j = i·2 + j:

```
i=0,j=0 : 00 -> 0        i=0,j=1 : 01 -> 1
i=1,j=0 : 01 -> 2        i=1,j=1 : 00 -> 3
filtered = 00 01 01 00   ==   decoded
```

Byte-identical. The tile is not all-fill (fill = 0, values 256 and 1), so
Appendix G item 6 does not sentinel it away. So there is a legal, stored,
non-degenerate-geometry tile in the "elsewhere" region whose stored bytes the
filter does **not** change. "every tile it touches" is falsified.
**Raised: A-04.**

The profile's argument does not need the universal — item 5's operative
justification is the sentence before it ("two writers agreeing on everything
else still disagree on bytes without it pinned"), which is true unconditionally
because the filter **value** is a u16 field in the layer record and differs
whatever the transform does. So this is an overclaim in a supporting clause, not
a broken argument. Marked non-byte-level: Appendix G is non-normative by its
heading and by `[R-CNF-01]`, and adds no obligation ("It adds no requirement to
any actor").

### 8.4 Checks 1–7 for hunk 7

- **1 Quantifier.** "the filter is the identity" ranges over the transform, not
  over a tile; "it changes the stored bytes of every tile it touches" ranges
  over tiles. Two different ranges in one sentence, joined by "elsewhere" — the
  first is a property of (s, n), the second a claim about tiles. That switch is
  where A-04 lives. **FLAGGED.**
- **2 Citation `[R-COD-10]`.** Verified symbol by symbol above: `n = L/s` is
  `[R-COD-10]`'s own notation, "the stride is 1, as for a packed boolean plane"
  is `[R-COD-10]`'s own sentence. §17.3 "leaves the choice to the writer" —
  `[R-COD-09]` assigns filter values 1 and 2, both core, writers MUST NOT emit
  another; so the choice between 1 and 2 is indeed the writer's. **PASS.**
- **3 Placement.** Non-normative appendix, by design; the profile is opt-in and
  adds no requirement. Not a case of a rule hiding in a Note, because the repair
  states a derived *property*, not an obligation. But see A-05: the property's
  **stride-only** earlier form is still standing in *normative* text at §20.3.
- **4 Contradiction in the passage.** Read Appendix G entire (4315–4457).
  - The clause "two writers agreeing on everything else still disagree on bytes
    without it pinned" against "The filter is the identity … where the stride is
    1" — I initially read these as contradictory (if the transform is the
    identity, do the writers disagree?). They are not: the layer record's
    `filter` u16 differs whatever the transform does, so the file's bytes differ
    regardless. No contradiction. The repair's restructuring moved the identity
    carve-out *after* the "so" conclusion, which makes the conclusion read
    unqualified — but the conclusion happens to be true unqualified. Noted, not
    raised.
  - The closing paragraph's list of "what is not [already mandatory]" does not
    name the filter value. Pre-existing, and disclaimed in place: "Read the
    numbered items as the list; this paragraph names what they are for, not how
    many there are." Not raised.
- **5 Exhaustive claims.** Three: "exactly where" (holds, §8.2), "and equally"
  (holds), "**every** tile it touches" (falsified, §8.3 — A-04). Also "as for a
  packed boolean plane" is exemplary, not a closed list; s = 1 also arises for a
  planar uint8/int8 channel and an interleaved single-1-byte-channel layer, and
  "where the stride is 1" covers all of them, so no overclaim there.
- **6 Unconstrained siblings.** Structure = item 5's degrees of freedom:
  declared alignment A (named), slab S (named), slab alignment A_slab
  (constrained to 0 when S = 0 by `[R-CNT-23]`, and pinned with S otherwise),
  filter value (named). Codec is item 1, linearization is content-implied
  (§11.4 governs), layout is caller input. I could not find a placement- or
  byte-affecting layer-record declaration item 5 leaves free. **PASS.**
- **7 Analogy.** "The filter is the identity **exactly where its permutation
  is**" — the warrant is `[R-COD-10]`.

  | | governing verb | ranges over |
  |---|---|---|
  | repair | "The filter **is** the identity exactly where its permutation **is**" | (s, n) pairs |
  | `[R-COD-10]` | "for a packed boolean plane s = 1 and the filter **is** the identity"; "the filtered image **places** byte i of group j at offset i · n + j" | the decoded image of a tile being filtered |

  Same verb "is"; the repair's n is `[R-COD-10]`'s n, defined in the same
  sentence that defines the placement. The analogy carries **two** members (the
  s = 1 case and the n = 1 case); tested separately in §8.2, both hold. **PASS.**

### 8.5 The restatement the repair did not sweep

`grep -n identity` gave line 3068, inside §20.3's step-4 declaration bar
(normative text, `[R-WRT-04]`'s procedure):

> "a change that leaves every one of those tiles' stored bytes meaning exactly
> what they meant — **a filter whose mandated stride makes it the identity**
> (`[R-COD-10]`), or a new padding position whose stored byte already holds the
> fill `[R-SER-05]` fixes — is not what this bars."

That is the pre-repair formulation of exactly the property hunk 7 corrected:
identity attributed to the **stride** alone. The n = 1 case — a layer all of
whose tile extents are 1, where s ≥ 2 and the filter is nonetheless the identity
— is an equally good instance of "stored bytes meaning exactly what they meant"
and the sentence does not name it. So the corrected statement of the property
now sits in a **non-normative appendix** while its narrower earlier form stands
in **normative** text. That is the shape the charter names as this project's
most common defect. **Raised: A-05.**

Mitigations I weighed before deciding severity, and which drive the
non-byte-level call: §20.3's own sentence makes the *effect* the test and
declares the list illustrative — "The test is the effect on such a tile, and the
list names where that effect arises rather than standing on its own". A reader
who follows the stated test reaches the right answer for the n = 1 case. So two
competent implementations following §20.3 as written converge; the risk is
mis-reading the example as the test.

---

## 9. Cross-hunk interactions I checked

1. **Hunk 2 against hunk 1's "states ten".** Hunk 2 inserts into `[R-CNT-06]`'s
   body a designation whose condition (F3's dir instance) is governed by
   `[R-ENC-04]`, not `[R-CNT-06]`. Under the register's governing-rule
   convention (§21.1: the Governing rule cell "names that requirement first")
   the count stays ten. Under a naive "conditions the requirement's text
   mentions" it would be eleven or twelve (the generation upper bound is a
   pre-existing instance of the same). Either way the substantive claim — only
   the magic and the CRC reach — is unchanged, since neither extra condition
   asserts a `[R-CNT-24]`-fixed invariant. Recorded, not raised.
2. **Hunk 1 against hunk 6.** Both move reach to per-condition; they agree.
   Verified §21.2's derivation against `[R-CNF-13]`'s test for all 36 rows
   (§3.4). They agree exactly. The residual is that the *only remaining*
   requirement-level use of "reach" is in `[R-CNF-02]`, which neither hunk
   touched (A-01), and that §21.2's enumeration is now unsubordinated (A-02).
3. **Hunks 2/3/4 as a sweep.** Together they close every `[R-ENC-04]`-governed
   register instance (§6.3 table). Verified complete.
4. **Hunk 5 against hunk 7.** Hunk 5 removes §17's section-wide "stored"
   quantifier; hunk 7's "every tile it touches" is a tile-level claim that does
   not depend on it. No interaction.

---

## 10. Findings

- **A-01** — hunk 1 — UNSWEPT_RESTATEMENT — `[R-CNF-02]`, §2.3 lines 143–147,
  still quantifies reach over *requirements* and cites `[R-CNF-13]` for it.
  **Byte-level: yes** (verifier verdict fork on a foreign-major file).
- **A-02** — hunk 6 — OVERSHOT — the deleted precedence sentence was the only
  statement subordinating §21.2's preamble to `[R-CNF-13]`; §21.1's precedence
  clause is expressly limited to rows and to §21.6's entries. Byte-level: no
  (derivation verified correct, so no live divergence).
- **A-03** — hunk 1 — OVERCLAIM — "Every other condition … is one of a structure
  this text defines for format major 1 alone" is falsified by F5 and F18, and
  states the complement over *structures* where the rule's test is over
  *invariants*. Byte-level: no.
- **A-04** — hunk 7 — OVERCLAIM — "elsewhere it changes the stored bytes of
  every tile it touches" is falsified by a shuffle-invariant tile image.
  Byte-level: no (non-normative appendix).
- **A-05** — hunk 7 — UNSWEPT_RESTATEMENT — §20.3's "a filter whose mandated
  stride makes it the identity" carries the pre-repair, stride-only form of the
  property hunk 7 corrected, in normative text. Byte-level: no.

Hunks 2, 3, 4 and 5: seven checks run, no findings.
