# Working transcript — verdict for a foreign-major file exhibiting a §21.2 row

## 0. Disclosure

Files read: exactly one — `/Users/robertkleffner/Documents/GitHub/tarn/spec/tarn.md`
(4495 lines, 273042 bytes). No other file in the repository was opened, listed, or
searched. No git history, no `docs/`, no `conformance/`, no `spec/registry.json`, no web.

Commands run (all read only that one file, plus one scratch helper I wrote myself):

- `wc -l` / `wc -c` on the spec.
- `grep -n "^#\{1,4\} "` on the spec, to build the section→line map.
- `sed -n '<range>p'` with an `awk` re-numbering filter, to read these ranges verbatim:
  94–280, 439–480, 622–695, 695–870, 1115–1160, 1292–1376, 2695–2835,
  3351–3500, 3612–3745, 4022–4110, 4424–4495.
- A helper `fsearch.py` that I wrote into the scratchpad. It reads only the spec,
  flattens it to a single whitespace-normalised string while keeping a
  character→line-number map, and regex-searches that flat string. This defeats the
  document's hard wrapping, so a phrase spanning a line break is still found.
  Queries run through it: `cannot establish`, `another major`, `other than 1`,
  `does not implement`, `major it does not`, `capability ground`, `capability grounds`,
  `foreign`, `verdict`, `certif(y|ies|ication|icate)`, `establish`, `R-CNT-24`,
  `fixed across every major`, `in every format major`, `F8`, `F14\b`,
  `declines to judge`, `not a TARN file`, `version gate`, `capabilit`, `refus`,
  `major 2`, `version_major`.

Unasked-for context: material appeared in my context before I began — a project
instruction file, an index of the maintainer's memory notes, and an environment block
naming the branch, git status and recent commit subjects. None of it is part of the
specification. I disregarded all of it and do not repeat its contents. Nothing below
derives from it.

Nothing was written to the repository. The only file written is this transcript.

## 1. The passages, verbatim

### §2.1 [R-CNF-01] — what is normative (lines 104–106)

> All text in this document is normative except: §1 (Introduction); any text
> labeled *Note*, *Example*, or *Rationale*; and appendices identified as
> non-normative. `[R-CNF-01]`

Consequence used below: §21.2's opening paragraph (lines 3432–3446) is normative.
It is not a Note/Example/Rationale, not in §1, not in an appendix, and (checked in the
raw `sed` output) not inside a Markdown blockquote. It carries no `[R-…]` identifier,
but §2.2 attaches identifiers to *requirements*, not to every normative sentence.
Appendix H (lines 4424–4495) is headed "(non-normative)" and is therefore evidence of
intent only, never authority.

### §2.3 [R-CNF-02] — the file predicate (lines 138–145)

> - **Conforming TARN file.** A byte sequence satisfying every file-level
>   requirement of this specification. File conformance is a pure predicate
>   on bytes: it does not depend on any reader, writer, or environment.
>   It is always conformance to a stated format major version. This
>   document defines format major 1, and a file declaring another major
>   is neither conforming nor nonconforming under it: a reader refuses
>   such a file on capability grounds (§6.3, `[R-CNT-07]`), and that
>   refusal is not a finding about its bytes.

Note the structure of the sentence: the "neither … nor" clause is glossed, in its own
sentence, by a single stated operational consequence — *a reader refuses such a file on
capability grounds, and that refusal is not a finding about its bytes*. The clause is
placed in the bullet that defines the **predicate**, not in the verifier bullet that
defines the verdicts. "Neither conforming nor nonconforming" is nowhere listed as a
verdict.

### §2.3 [R-CNF-11] — the verifier and its three verdicts (lines 189–223)

> - **Conforming verifier.** A reader that additionally checks every
>   file-level requirement — including those ordinary readers are
>   exempted from — and certifies conformance. Verifiers and updaters are
>   readers of the files they process and inherit every reader
>   obligation. A verifier reports one of three verdicts: *conforming*,
>   *nonconforming*, or *cannot establish* — the last where some
>   requirement is one it is unable to check on a capability or
>   resource ground, as when the file names a
>   format major version it does not implement, when a record carries
>   MUST_UNDERSTAND = 1 with a type it does not implement (§21.6), when
>   it cannot execute a codec or filter (`[R-COD-11]`), when it
>   declines a layer's or a tile's decode on resource grounds and so
>   cannot check §14's decoded-content obligations (`[R-ERR-04]`,
>   `[R-SER-05]`, `[R-SER-08]`), or when it declines to decode a
>   user-metadata document (`[R-MTA-09]`). A user-metadata document
>   under an encoding this specification does not assign is not such
>   a ground: no content rule attaches there, so nothing is left
>   unchecked, and certification is unaffected (`[R-MTA-10]`, §21.6).
>   *Cannot establish* is not a finding that the file is nonconforming,
>   and a verifier MUST NOT certify a file it reports that way. An
>   established violation takes priority: a verifier that has
>   established any violation reports *nonconforming*, however many
>   requirements it was unable to check, and *cannot establish* is
>   available only to a traversal that established no violation. A
>   verifier MUST report each requirement it was unable to check on a
>   capability or resource ground, naming the requirement and the
>   ground, whichever of the three
>   verdicts it reports; that per-requirement report constrains the
>   report and not the verdict, as *unexamined* does below.
>   A verifier MAY stop at the first violation it finds; one that does
>   MUST report each scope it did not examine as *unexamined*, which is
>   not a finding that the scope is clean. *Unexamined* is neither a
>   verdict nor *cannot establish* — it constrains the report, not the
>   verdict.
>   `[R-CNF-11]`

Three things are load-bearing here:
(a) the verdict set is closed at three;
(b) "as when the file names a format major version it does not implement" is the
    document's own leading example of a *cannot establish* ground;
(c) the priority clause is keyword-free but declarative and therefore binding per §2.1's
    convention: "a verifier that has established any violation reports *nonconforming*,
    however many requirements it was unable to check, and *cannot establish* is
    available only to a traversal that established no violation."

### §2.4 [R-CNF-12] — certification bar (lines 254–266, excerpt)

> A file is conforming only if it satisfies every requirement at every
> scope: the outcome classes describe the blast radius of a violation
> for readers, never degrees of file conformance, and a verifier
> certifies only violation-free files.

### §4.5 [R-ENC-10] — check before acting (lines 452–456)

> A reader MUST verify the checksum covering a field before acting on
> that field — where *acting on* means using its value to allocate,
> seek, fetch, or select behavior; comparing a field against a constant
> for validation is not acting on it, and an explicit validation order
> (§6.2) governs where one is stated. `[R-ENC-10]`

### §6.1 [R-CNT-04] — front block (line 699 and 717–727)

> Bytes [0, 16) of every file, constant in every format major version:

> A reader whose open leaves bytes
> [0, 16) **resident** … MUST verify the full block by byte
> equality before other processing, and MUST treat any mismatch as
> reject-file. A reader that would have to issue a further range request
> to obtain those bytes MAY defer or omit the check … `[R-CNT-04]`

### §6.2 [R-CNT-06] — the ordered trailer validation (lines 773–782)

> A reader MUST validate, in order: the trailer magic; the trailer CRC;
> the version gate (§6.3) — only these touch fields whose positions are
> fixed across all majors (`[R-CNT-24]`) — and then, those gates passed,
> MUST validate all of the following before acting on the fields
> involved: the flag gates (§6.3); committed_file_length equals the file
> size … Any failure is reject-file. The owning scope of the front
> signature block and the trailer is the file. `[R-CNT-06]`

Trailer layout row for the magic (line 746) and CRC (line 756):

> | 0 | 8 | bytes | trailer magic | structural | `8A 4E 52 41 54 0D 0A 1A` … |
> | 60 | 4 | u32 | trailer CRC | structural | CRC-32C over trailer bytes [0, 60) |

### §6.3 [R-CNT-07] and [R-CNT-24] (lines 791–807)

> A reader MUST reject-file when version_major is 0 (invalid) or is a
> major it does not implement, and the diagnostic for an unimplemented
> major SHOULD be distinct from both "not a TARN file" and "corrupt" … `[R-CNT-07]`

> In every format major version, permanently: the final 64 bytes of a
> file contain the trailer magic at F − 64, version_major and
> version_minor at F − 56, and a CRC-32C at F − 4 covering bytes
> [F − 64, F − 4); and the front signature block (§6.1) is constant. …
> `[R-CNT-24]`

### §5.2 [R-CNT-21] — what a verifier reports when §6.2 rejects early (lines 638–645)

> A reader MUST NOT interpret it (§9.5); a verifier that
> reaches a live state MUST report the total number of slack bytes,
> since that number is what tells an operator to compact. Where §6.2's
> ordered validation rejects the file before a live trailer is
> established there is no F and no live state to walk, so the total is
> not owed at all: the verifier reports the trailer failure and
> nothing about slack, which is not a partial total but the absence of
> one.

### §9.6 [R-LIF-06] — a bad trailer is a *failure*, not a suspension (lines 1299–1308)

> A recovery tool enumerating a file's commit states continues
> the same probe to offset 0; coverage verification does not (§9.7,
> `[R-LIF-08]`), and no verdict turns on the probe: a file whose final
> 64 bytes are not a valid trailer fails `[R-CNT-06]`'s gates on the
> bytes handed over (§21.2 rows F8, F14 and F17 — the magic, the
> trailer CRC and the length cross-check) …

### §19.1 step 2 (lines 2725–2729)

> 2. **Trailer.** Fetch bytes [F − 64, F) and validate them in
>    §6.2's fixed order — magic, trailer CRC, version gate, then the
>    remaining field gates (`[R-CNT-06]`, `[R-CNT-07]`,
>    `[R-CNT-08]`). …

### §21.1 — what a register row is (lines 3355–3372, 3376–3379, excerpts)

> The register — §21.2 through §21.5 (`[R-ERR-02]`) — enumerates
> every detectable file-conformance violation this specification names: each row is one
> malformed condition, with the outcome class its scope determines
> (§2.4) … the actor obliged to detect it (`[R-CNF-04]`, `[R-CNF-11]`),
> the point by which detection is due (§19.2), and the requirement that
> defines it.

> … each row *restates* its governing rule, and where a
> row and the rule it cites diverge, **the rule governs**.

> Some
> rows are strict specializations of others — F1 of F6 and of F8,
> F35 of F36, L24 of L25 — and a file exhibiting a specialization is
> recorded against the narrower row, whose detector and detection
> point are the ones that apply.

### §21.2 — THE PARAGRAPH UNDER EXAMINATION (lines 3432–3446)

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

Rows named (lines 3450, 3455, 3457, 3463):

> | F1 | A signature constant is stored byte-reversed … | front signature block bytes [0,8); trailer magic at F-64 | reader | open | `[R-ENC-02]` (R-CNT-04, R-CNT-06) |
> | F6 | The 16-byte front signature block is not byte-identical to the constant; … a verifier holds no such exemption (§2.3) | magic bytes [0,8); reserved bytes [8,16) | reader | open | `[R-CNT-04]` |
> | F8 | The 8 bytes at F-64 are not exactly the trailer magic 8A 4E 52 41 54 0D 0A 1A | trailer magic | reader | open | `[R-CNT-06]` |
> | F14 | The u32 at trailer offset 60 does not equal the CRC-32C of trailer bytes [0,60) | trailer CRC | reader | open | `[R-CNT-06]` (R-CNT-20, R-ENC-09) |

Count check: "Four rows" = F1, F6, F8, F14 (F1 contributing two instances). Consistent.
Note that F17 (committed_file_length vs. physical size) is *not* in the four, although
§9.6 groups it with F8 and F14; F17 is a post-gate field gate under §6.2, so it does not
reach a foreign-major file. Internally consistent.

### §21.6 — the two capability refusals (lines 3645–3664)

> Two structural cases are **conforming files a reader nevertheless
> refuses**. The first is **version_major naming a major this reader
> does not implement**: the reader rejects the file (`[R-CNT-07]`), but
> the file can be perfectly conforming under that major. …
> In both the outcome records a reader's capability, not a defect
> in the bytes, and the diagnostic ought to distinguish the two.
> Neither is a register row: the register enumerates file-conformance
> violations (§21.1), and a file this document declines to judge is not
> one.

### Appendix H (non-normative), verifier entry (lines 4477–4494, excerpts)

> the 16-byte front signature block by byte equality, which
> `[R-CNT-04]` lets a reader not holding it resident defer or omit and
> §2.3 does not (F1, F6);

> reports *nonconforming*
> whenever it has established a violation, reserving *cannot
> establish* for a traversal that established none;

## 2. Searches that produced nothing

Normalised-whitespace searches that found **no** passage assigning a verdict word to a
foreign-major file:

- `major 2` — zero hits anywhere in the document.
- `verdict` — 11 hits (lines 193, 216, 217, 221, 222, 1301, 2421, 2533, 2844, 3620,
  3682). None of them is about a foreign major. The three that fix a verdict
  (2421 `[R-COD-11]`, 2533 `[R-MTA-09]`, 4494 Appendix H) all concern codec/metadata
  declines, and all three restate the same priority clause.
- `establish` — every hit inventoried. No hit states what a verifier reports for a
  foreign-major file that also fails a cross-major check.
- `capabilit` / `refus` — the foreign-major case is discussed at lines 143–145, 3437,
  3646–3657 and 3784. All four discuss the **reader's refusal**; none names a verifier
  verdict.

**Well-searched absence #1:** the document never states, in any section, the verdict a
verifier reports for a file declaring a foreign major — neither for the clean case nor
for the case where a cross-major row also fires. The verdict must be derived.

**Well-searched absence #2:** §21.2's paragraph uses the verb "reach" without defining
it. `fsearch.py "reach"` shows no definitional use elsewhere that fixes whether "reaching"
a file means (i) the row's reader outcome applies, or (ii) the file thereby exhibits a
file-conformance violation. The distinction is exactly the hinge of this question and the
document does not settle it by stipulation.

## 3. The cases, traced

### Case A — declares major 2, trailer magic wrong

Step 1. `[R-CNT-06]` fixes the order: "the trailer magic; the trailer CRC; the version
gate (§6.3)". §19.1 step 2 repeats it. The magic check therefore fires **first**, before
the verifier has any licence to act on `version_major`.

Step 2. The magic is wrong → "Any failure is reject-file" (`[R-CNT-06]`). The condition is
§21.2 row F8 ("The 8 bytes at F-64 are not exactly the trailer magic…"), detector
*reader*, detected *open*. If the wrongness is specifically byte-reversal, §21.1's
specialization rule records it against F1's trailer-magic instance instead
("F1 of F6 and of F8"); either way a §21.2 row fires.

Step 3. §21.2's paragraph expressly says this row reaches this file: "Four rows are
outside that reasoning and do reach it, because their subject is a field fixed across
every major (`[R-CNT-24]`): F8 and F1's trailer-magic instance, F14's trailer CRC".

Step 4. §21.1: "The register … enumerates every detectable file-conformance violation
this specification names: each row is one malformed condition". So a file the row reaches
exhibits a file-conformance violation this specification names.

Step 5. `[R-CNF-11]`: "An established violation takes priority: a verifier that has
established any violation reports *nonconforming*, however many requirements it was
unable to check, and *cannot establish* is available only to a traversal that established
no violation."

Step 6. Therefore the traversal has established a violation, *cannot establish* is
withdrawn by its own availability condition, and *nonconforming* is what the clause says
is reported.

Step 7. *Conforming* is independently forbidden: `[R-CNF-12]` — "a verifier certifies only
violation-free files."

Corroboration from a second, independent place: §9.6 `[R-LIF-06]` — "a file whose final
64 bytes are not a valid trailer **fails** `[R-CNT-06]`'s gates on the bytes handed over
(§21.2 rows F8, F14 and F17…)" — the word is *fails*, a finding, and the sentence it sits
in begins "no verdict turns on the probe", presupposing that a verdict exists and is fixed
by the gate failure. And §5.2 `[R-CNT-21]` — "Where §6.2's ordered validation rejects the
file before a live trailer is established … the verifier reports **the trailer failure**"
— again a failure report, not a suspension of judgment.

Corroboration on the ordering point, from R-CNF-02's own gloss: R-CNF-02 explains "neither
conforming nor nonconforming" by exactly one operational consequence — "a reader refuses
such a file on capability grounds (§6.3, `[R-CNT-07]`), and that refusal is not a finding
about its bytes." In Case A the reader does **not** refuse on capability grounds: it never
reaches the version gate. §21.2 says as much — the geometry rows do not reach because
"such a file is refused on capability grounds first", and the four rows are "outside that
reasoning". So R-CNF-02's stated consequence does not cover Case A, and the refusal here
*is* a finding about the bytes.

Corroboration on the substance: the requirement violated is one this document asserts for
**every** major. `[R-CNT-24]`: "In every format major version, permanently: the final 64
bytes of a file contain the trailer magic at F − 64 … and a CRC-32C at F − 4 covering bytes
[F − 64, F − 4); and the front signature block (§6.1) is constant." So the verifier is not
reaching past its competence: it is establishing the breach of a rule that binds major 2
as much as major 1, which is precisely the reason §21.2 gives for the carve-out.

**Case A verdict: nonconforming.** Forced by the priority clause; *conforming* forbidden;
*cannot establish* forbidden by "available only to a traversal that established no
violation".

### Case B — declares major 2, trailer CRC fails

Same trace, one row later. Magic passes; the CRC check is second in `[R-CNT-06]`'s order;
it fails → reject-file; row F14; §21.2 names "F14's trailer CRC" among the four that reach.
Steps 4–7 identical. **Verdict: nonconforming.**

Case B carries an extra, independent argument that the foreign-major premise never
legitimately arises for the verifier. `[R-ENC-10]`: "A reader MUST verify the checksum
covering a field before acting on that field — where *acting on* means using its value to
allocate, seek, fetch, or select behavior … and an explicit validation order (§6.2) governs
where one is stated." `version_major` sits at trailer offset 8, inside the range the
trailer CRC covers (§8.1's map, line 1130: "Trailer | trailer bytes [60, 64) | trailer
bytes [0, 60)"). Applying the version gate is *selecting behavior* on that field's value,
and it is not the excepted "comparing a field against a constant for validation". With the
CRC failed, a conforming verifier may not act on `version_major` at all. So in Case B the
verifier never establishes that the file declares major 2; it establishes only F14. The
foreign-major shield has nothing to attach to.

### Case C (for completeness) — declares major 2, front signature block wrong

`[R-CNT-04]` places the block check "before other processing" for a reader holding
[0, 16) resident, and F6's own Condition cell says "a verifier holds no such exemption
(§2.3)" — confirmed by Appendix H's non-normative summary, "the 16-byte front signature
block by byte equality, which `[R-CNT-04]` lets a reader not holding it resident defer or
omit and §2.3 does not (F1, F6)". §21.2 names "F6 with F1's front-block instance" among
the four. Same trace. **Verdict: nonconforming.**

### Case D (the contrast case) — declares major 2, some *other* §21.2 row's condition

E.g. F11 (generation = 0), F9 (dir_offset < 16), F20 (directory CRC), F34 (two
user-metadata records). §21.2: "the rows below whose subject is that file's *geometry* do
not reach it: §6.2 puts the version gate ahead of every check but the trailer magic and the
trailer CRC, so such a file is refused on capability grounds first." The row does not
reach; no violation is established; the file "names a format major version it does not
implement", which `[R-CNF-11]` gives as its leading *cannot establish* ground; and
`[R-CNF-11]` forbids certifying. **Verdict: cannot establish**, with the version-gate
requirement reported as unchecked under `[R-CNF-11]`'s per-requirement duty.

## 4. The tension, stated exactly, and what survives it

The §21.2 paragraph asserts both halves in one sentence:

  (i) "A file declaring a format major other than 1 is neither conforming nor
      nonconforming under this text (§2.3, `[R-CNF-02]`)"
  (ii) "Four rows are outside that reasoning and do reach it"

If "reach" means *the file thereby exhibits a file-conformance violation* — which is what
§21.1 says a register row **is** — then in Cases A/B/C the verifier reports *nonconforming*
by the priority clause, and (i) is false of exactly those files. If "reach" means only
*the row's detection obligation and reject-file outcome apply to a reader* — a reading the
document nowhere states but nowhere excludes — then no violation is established, (i)
stands, and the verdict is *cannot establish*.

Reading 1 (rows reach as violations → **nonconforming**) is the stronger reading, on four
textual grounds:

- §21.1 defines the register's rows as file-conformance violations; nothing gives "reach"
  a weaker sense.
- §21.2's stated *reason* for the carve-out is substantive, not procedural in the reader's
  interest: "because their subject is a field fixed across every major (`[R-CNT-24]`)".
  A rule holding in every major is one whose breach a major-1 verifier can establish
  without judging major 2. A merely-reader-facing reading makes that reason idle.
- R-CNF-02's "neither" clause is glossed by exactly one consequence — refusal *on
  capability grounds* — and §21.2 tells us that in these four cases the file is not
  refused on capability grounds first.
- `[R-LIF-06]` (line 1303) and `[R-CNT-21]` (lines 640–645) both describe the §6.2 gate
  outcome as a *failure* the verifier *reports*, never as a suspension.

Reading 2 (rows reach only as reader obligations → **cannot establish**) has one textual
ground, but a blunt one: (i) is stated flatly, unqualified, twice — once in `[R-CNF-02]`
and once at the head of the very paragraph that then carves out four rows. And `[R-CNF-02]`
says conformance "is always conformance to a stated format major version", which makes a
bare *nonconforming* verdict on a major-2 file a verdict with no major to attach it to.

What the document does **not** decide, and what a decision is therefore genuinely owed on:
whether "nonconforming" in `[R-CNF-11]`'s priority clause is relativised to the file's
declared major or to the document doing the verifying. Under Reading 1 the verdict word is
forced but its relativisation is unstated: the file is nonconforming *under `[R-CNT-24]`,
i.e. under every major*, which is a claim the verdict vocabulary has no slot for. §2.3's
verdict sentence never mentions a major; §2.3's predicate sentence insists conformance
always names one. That gap is real and searched-for (`verdict`, `establish`, `capabilit`,
`major 2` all run; no passage bridges it).

## 5. What each verdict is: forced / permitted / forbidden

For a foreign-major file exhibiting F1, F6, F8 or F14 (Cases A/B/C):

- *conforming* — **forbidden**, unconditionally and on two independent grounds.
  `[R-CNF-12]`: "a verifier certifies only violation-free files." `[R-CNF-02]`: the file is
  not conforming under this text in any case. No reading rescues it.
- *nonconforming* — **forced under Reading 1**, which I take to be the better-supported
  reading; **not permitted under Reading 2**.
- *cannot establish* — **forbidden under Reading 1** ("available only to a traversal that
  established no violation"); **forced under Reading 2**.

The two readings are exhaustive and mutually exclusive, and *conforming* is out on both.
So the document forces the disjunction {nonconforming, cannot establish} and forbids
*conforming*; within the disjunction it leans hard on *nonconforming* but does not close
the question, because the sentence that would close it asserts both halves at once.

For a foreign-major file exhibiting any other §21.2 row (Case D): the document does force
one answer — *cannot establish*, with certification forbidden. Both readings agree here,
since the row does not reach and no violation is established.

## 6. "Neither conforming nor nonconforming": verdict or predicate?

The document forces the predicate answer. Grounds:

- `[R-CNF-11]` closes the verdict set at three by enumeration: "A verifier reports one of
  three verdicts: *conforming*, *nonconforming*, or *cannot establish*". "Neither…nor" is
  not among them.
- The phrase appears in the **Conforming TARN file** bullet, whose subject sentence is
  "File conformance is a pure predicate on bytes" — a statement about the predicate's
  domain, i.e. that the predicate is undefined (not false) on foreign-major inputs.
- `[R-CNF-11]` is careful to mark what is and is not a verdict elsewhere in the same
  requirement — "*Unexamined* is neither a verdict nor *cannot establish*" — and never
  performs that marking for "neither conforming nor nonconforming", because that phrase is
  not in the verdict register at all.
- §21.6 confirms the predicate framing: "the register enumerates file-conformance
  violations (§21.1), and a file this document declines to judge is not one" — declining
  to judge is a gap in the predicate, not a fourth answer.

Consequence: a verifier facing a foreign-major file cannot *report* "neither"; it must pick
one of three. That is exactly why the question has bite.

## 7. Priority rule

The only rule fixing priority among verdicts is in `[R-CNF-11]`, lines 209–212:
"An established violation takes priority: a verifier that has established any violation
reports *nonconforming*, however many requirements it was unable to check, and *cannot
establish* is available only to a traversal that established no violation."

It is restated identically at §17.4 `[R-COD-11]` (lines 2421–2422), at §18.2 `[R-MTA-09]`
(lines 2533–2534), and non-normatively at Appendix H (lines 4491–4494). Three restatements,
no exception carved anywhere for the foreign-major case. The rule is directional in only
one way: it lets an established violation *override* a cannot-establish ground, never the
reverse. Nothing in the document lets a cannot-establish ground suppress an established
violation. That asymmetry is the single strongest structural argument for Reading 1.

## 8. Derivation summary (Reading 1, the one I take as better supported)

1. `[R-CNT-06]` orders magic → CRC → version gate. (§6.2, lines 773–775)
2. So for Cases A/B the failing check precedes the version gate; the verifier never
   reaches the capability ground. (§6.2; §19.1 step 2, lines 2725–2728)
3. For Case B additionally, `[R-ENC-10]` bars acting on `version_major` before its
   covering CRC verifies. (§4.5, lines 452–456; §8.1 map, line 1130)
4. §21.2 states F1/F6/F8/F14 "do reach" a foreign-major file, on the substantive ground
   that `[R-CNT-24]` fixes their subjects across every major. (lines 3437–3444)
5. §21.1 makes a register row a *detectable file-conformance violation*. (lines 3355–3357)
6. Hence the traversal has *established a violation*.
7. `[R-CNF-11]`'s priority clause then yields *nonconforming* and withdraws *cannot
   establish*. (lines 209–212)
8. `[R-CNF-12]` independently forbids *conforming*. (line 257)

## 9. What I am supplying, not deriving

- The four-way case split (A/B/C/D) is mine; the document does not enumerate cases.
- The label "Reading 1 / Reading 2" and the judgment that Reading 1 is better supported
  are mine. The document does not rank them.
- The observation that Reading 1 leaves *nonconforming* unrelativised to a major, and that
  this is the residue a decision is owed on, is mine — derived from `[R-CNF-02]`'s "It is
  always conformance to a stated format major version" against `[R-CNF-11]`'s
  major-free verdict sentence, but not stated as a problem anywhere in the document.
