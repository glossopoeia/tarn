# qh456 — can the foreign-major reach question be answered once in §2.3?

## Disclosure

Files read: exactly one — `/Users/robertkleffner/Documents/GitHub/tarn/spec/tarn.md`.

Commands run (all read only that file or compute over its text):

- `wc -l` / `wc -c` on the spec.
- `grep -n '^#\{1,4\} '` on the spec — section header index.
- `sed -n` on the spec for line ranges 94–280 (§2), 622–870 (§5.2–§6.4),
  2695–2810 (§19.1–§19.2), 3351–3500 (§21.1–§21.3 head), 3544–3620 (§21.4–§21.6),
  3612–3670 (§21.6).
- Three `python3` heredocs that open only `spec/tarn.md`, normalise all
  whitespace to single spaces (`re.sub(r'\s+',' ',t)`) — because the document is
  hard-wrapped and a line-oriented grep would miss any phrase that wraps — and
  print windows around: `stated in the section`, `where it arises`,
  `rather than enumerated`, `belongs with`, `is stated once`, `stated once`,
  `single place`, `one place`, `not restated`, `restat`, `R-CNT-27`,
  `version_major = 0`, `major other than 1`, `another major`, `foreign`,
  `capability grounds`, `§21.2`, `Appendix H`, `§2.3 defines the classes`,
  plus `re.findall(r'R-CNF-\d+')` to enumerate the CNF identifier space.

Nothing else was read: no `docs/`, no ADRs, no `PLAN.md`, `OPEN-QUESTIONS.md`,
`AGENTS.md`, `README.md`, no `conformance/`, no `spec/registry.json`, no git
history, no web.

Unrequested context appeared in my context window before I began: a project
instruction file, an index of the maintainer's notes, and an environment block
naming the branch and recent commit subjects. I disregarded all of it and do not
repeat its contents; none of it is evidence about the specification.

## The text under examination (§21.2, first paragraph, verbatim)

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
> the check. F18 is not an exception but a case outside the premise:
> version_major = 0 declares no major at all and is permanently
> invalid in every one (§21.6).

Shape: a four-item list, plus one item declared "not an exception but a case
outside the premise" — which is an exception with a disclaimer attached. This is
the shape the project's standards name twice ("a closed count in normative prose
is a claim about the whole document"; "a claim patched with an exception is a
list by another name").

## The property the list is standing in for

Candidate A (ordering): *a requirement reaches iff §6.2 orders its check no
later than the version gate.*

Candidate B (fixity): *a requirement reaches iff the field or structure it
constrains is one `[R-CNT-24]` fixes in every format major version.*

§6.2 itself ties the two together, verbatim: "the trailer magic; the trailer
CRC; the version gate (§6.3) — only these touch fields whose positions are fixed
across all majors (`[R-CNT-24]`)". So ordering is *derived from* fixity. I tested
both. Candidate A is under-determined at F5 (below); Candidate B decides every
row. I adopt B and state the ordering as a consequence that also binds future
edits.

`[R-CNT-24]`, verbatim, is the sole owner of the fixed set: "In every format
major version, permanently: the final 64 bytes of a file contain the trailer
magic at F − 64, version_major and version_minor at F − 56, and a CRC-32C at
F − 4 covering bytes [F − 64, F − 4); and the front signature block (§6.1) is
constant. A future major MAY redefine only the remaining 48 trailer bytes…"

## Every row tested against Candidate B

All 36 file-scope rows. "Fixed?" = is the row's subject a field or structure
`[R-CNT-24]` fixes in every format major version.

| Row | Subject | Fixed? | Reaches a foreign-major file |
|---|---|---|---|
| F1 | front block [0,8); trailer magic at F−64 | yes, both | **reaches, both instances** |
| F2 | dir_offset, dir_length, committed_file_length, generation, record extents | no — trailer bytes 12–56, redefinable | no |
| F3 | dir_offset + dir_length; record extent sums | no | no |
| F4 | layer record name fields in the directory | no | no |
| F5 | 128-byte file minimum; committed_file_length | no — floor derived from major 1's own layout | no |
| F6 | 16-byte front signature block | yes | **reaches** |
| F7 | structures in the pre-trailer gap | no | no |
| F8 | trailer magic | yes | **reaches** |
| F9 | dir_offset ≥ 16 | no — offset 24 | no |
| F10 | dir_offset + dir_length ≤ F − 64 | no | no |
| F11 | generation ≠ 0 | no — offset 16 | no |
| F12 | file_id ≠ 0 | no — offset 48 | no |
| F13 | committed_file_length multiple of 64 | no — offset 40 | no |
| F14 | u32 at trailer offset 60 = CRC-32C of [0,60) — i.e. F−4 | yes | **reaches** |
| F15 | reserved bytes [56,60) all zero | **no** — see trap (a) | no |
| F16 | dir_length ≥ 4 | no | no |
| F17 | committed_file_length = transport size | no | no |
| F18 | version_major = 0 | yes — version_major's position is fixed, and 0 is invalid in every major (`[R-CNT-07]`, §21.6) | **reaches** |
| F19 | flags incompat lane bits 0–15 | no — offset 12, redefinable | no |
| F20 | directory region CRC | no | no |
| F21 | user-metadata record extent slot (0,0) | no | no |
| F22 | user-metadata extent_length < 5 | no | no |
| F23 | user-metadata inline_length ≠ 1 | no | no |
| F24 | top-level record type 0x0000 | no | no |
| F25 | MU=1 with PE=0 | no | no |
| F26 | reserved flag bits 2–15 of a record | no | no |
| F27 | file-scope metadata document member order | no | no |
| F28 | registered type's stored MU/PE vs registry | no | no |
| F29 | record header / inline payload bounds, trailing residue | no | no |
| F30 | extent slot with exactly one half zero | no | no |
| F31 | extent_offset in 1–15 | no | no |
| F32 | extent_offset + extent_length > F − 64 | no | no |
| F33 | two structures claiming one byte | no | no |
| F34 | two user-metadata records | no | no |
| F35 | reserved-range type with MU = 1 | no | no |
| F36 | reserved-range type at all | no | no |

Reaching set: **F1, F6, F8, F14, F18** — five rows, six instances.

Spot-checked §21.3 (L1–L49), §21.4 (T1–T26), §21.5 (R1–R10) as classes: every
subject there is a layer record, a dimension/channel entry, a tile-index entry, a
tile payload, or a record extent's document — all structures this document
defines for major 1 alone, none named by `[R-CNT-24]`. So none reaches, and the
property says so without a word being added. §21.2's preamble never said
anything about those three subsections at all; the property closes that silence.

## Text I tried to break the proposal with

**(a) F15 cites `[R-CNT-24]` in its Governing rule cell.** Verbatim:
"| F15 | The 4 reserved bytes at trailer offset 56 are not all zero | … |
`[R-CNT-06]` (R-CNT-24) |". If the property were "the row cites `[R-CNT-24]`",
F15 would reach and the property would be wrong — bytes [56,60) sit inside the
48 a future major MAY redefine. The citation is to `[R-CNT-24]`'s *last*
sentence ("The format-major-1 trailer has zero slack: every byte is assigned"),
not to its fixity clause. Survived, but it forced the wording: the test must be
"a field `[R-CNT-24]` **fixes in every format major version**", never "a field
`[R-CNT-24]` mentions" or "a row citing `[R-CNT-24]`".

**(b) F5's physical-F instance, against Candidate A.** `[R-CNT-27]` is a rule of
its own ("No conforming file is shorter than 128 bytes… A reader MUST treat a
shorter file as a validity error at file scope"); §6.2's ordered list does not
contain it, and §19.1 step 1 obtains F before step 2 touches the trailer. So an
ordering-only property leaves F5 undecided — it is arguably decidable before the
gate. Candidate B decides it cleanly (the 128-byte floor is derived from major
1's own directory placement; a future major's floor could differ), and this is
why the draft states fixity as the test and ordering as its consequence.

**(c) The current text's own bookkeeping.** It says "Four rows … do reach it"
and then lists F8, F1's trailer-magic instance, F14, and "F6 with F1's
front-block instance" — F1 counted across two of the four items, and F18 handled
in a separate sentence. Five rows reach. The count in the prose is already
carrying a fiction to keep the list tidy. A property has no count to keep.

**(d) Does §2.3's own placement discipline forbid a central answer?**
`[R-CNF-02]` says of its writer-conduct carve-outs: "each is declared where it
arises rather than enumerated here." If the relocation moved the *list* into
§2.3, that sentence would indict it directly. It does not indict a property:
the new paragraph enumerates no cases, and the one list it depends on stays in
`[R-CNT-24]`, the rule that owns it. Survived — but it is decisive against a
lift-and-shift of the current text, which is the honest answer to task
question (2): relocating the list buys nothing and lands in the one section that
has written down a rule against doing that.

**(e) Does the relocation drop the residency qualification?** The current
preamble carries "a reader that already holds those bytes, one that would have
to fetch them being free to defer or omit the check". That is `[R-CNT-04]`'s own
text, restated again in F6's Condition cell ("a verifier holds no such
exemption (§2.3)") and again in §19.1 step 1. Nothing is lost; the draft cites
`[R-CNT-04]` rather than restating it a fourth time.

**(f) Verifier verdict ambiguity.** §2.3's verifier bullet gives *cannot
establish* "as when the file names a format major version it does not
implement". A major-2 file with a corrupt front block satisfies that clause and
also exhibits F6. The same bullet already resolves it — "An established
violation takes priority: a verifier that has established any violation reports
*nonconforming*" — but only if F6 is *established* against that file, which is
exactly what the reach rule decides. The draft states the interaction rather
than leaving the reader to compose two bullets.

**(g) Does §21.1's normative completeness break?** "Its **completeness is
normative** — a *detectable* file-conformance violation this specification names
and the register omits is a defect in this document". Completeness is about
which conditions have rows, not about which files a row reaches. Deleting the
preamble removes no row and adds no unregistered condition. Survived.

**(h) Does anything cite §21.2's preamble?** Whitespace-normalised search for
`§21.2` returns five hits: §9.5's note ("each of which §21.2 already
registers"), §9.6 ("§21.2 rows F8, F14 and F17"), §21.1 ("§21.2 through §21.5"),
§21.8 ("Every row of §21.2 through §21.5"), Appendix H ("no violation row of
§21.2–§21.5 applies"). Every one cites rows or the section range. None cites the
preamble. Survived.

**(i) Over-claim check on "not a conforming file under any format major
version".** Supported by `[R-CNT-24]`'s "In every format major version,
permanently", by `[R-ENC-02]`/F1's "never to be adapted as a foreign-endian TARN
file", and for F18 by `[R-CNT-07]` plus §21.6's "version_major = 0, permanently
invalid in every format major version". This document already makes forward
commitments about other majors; the draft makes no new one.

## Task question (1) — is §2.3 the defining section?

Placement discipline actually written down in this document:

- `[R-CNF-08]`, §2.4: "Every structure this specification defines has exactly
  one **owning scope** … stated in the section that defines the structure."
- §21.9: "The hard limits it restates are a finding aid rather than an
  inventory — each is normative where the structure forcing it is defined."
- §21.1: "each row *restates* its governing rule, and where a row and the rule
  it cites diverge, **the rule governs**."
- §20.5: "which is why the rule is stated here and not left to the rows."

The pattern is consistent: a rule lives where its subject is defined; §21 and
§21.9 restate. The reach rule's subject is not a structure — it is *the
applicability of this document's requirements to a file that declares a major
this document does not define*. §2.3 defines exactly that subject, in its first
bullet: "It is always conformance to a stated format major version. This
document defines format major 1, and a file declaring another major is neither
conforming nor nonconforming under it". §21.2 owns rows, not the scoping of
conformance to a declared major — and by §21.1's own logic a preamble deciding
reach is a rule sitting in the restating section, which is backwards. The
competing home is §6.3 with `[R-CNT-24]`, but `[R-CNT-24]` is a rule about
bytes (what a future major may redefine); the reach rule is a rule about
requirements. §2.3 is the defining section; it cites `[R-CNT-24]` for the fixed
set instead of restating it.

## Task question (2) — must rows be named?

No, provided the reach test is the `[R-CNT-24]` property. Naming rows is
required only by the list form, and the list form is what makes the relocation
worthless (and is what `[R-CNF-02]`'s own sentence argues against — trap (d)).
The property names no row, no count, and no instance; it is checkable against
any candidate row, including rows that do not exist yet, and it extends to
§21.3–§21.5 for free.

## Task question (3) — the remainder

Siblings, verbatim:

- §21.3: "Outcome: reject-layer — the named layer is unusable, every other layer
  unaffected. 49 conditions."
- §21.4: "Outcome: reject-tile — that tile's read reports failure, and never
  returns fill in place of data (`[R-CNF-09]`). 26 conditions."

§21.2 reduced to "Outcome: reject-file. 36 conditions." plus a one-clause
pointer is the same shape as both, and §21.4 shows a parenthetical
cross-reference is already idiomatic there. Coherent.

Alternative considered and rejected for churn: put the pointer in §21.1 instead,
since the reach rule governs the whole register rather than §21.2 alone. §21.2
keeps it because §21.2 is where a reader currently looks for the answer.

## Identifier

`re.findall(r'R-CNF-\d+')` over the whole file: R-CNF-01 … R-CNF-12, no gaps,
13 free. §2.2: "numbers above 99 extend naturally … without renumbering" and
"New prefixes are added by ADR when a section needs one" — a new *number* under
an existing prefix needs no new prefix. `[R-CNF-13]` it is. The alternative —
folding the text into `[R-CNF-02]` — was rejected because the rule binds readers
and verifiers as well as fixing the file predicate, and `[R-CNF-02]` is the
"Conforming TARN file" bullet; a trailing paragraph in §2.3 with its own
identifier follows §2.4's precedent of paragraphs after the tabulated material.

## Final draft — §2.3, new paragraph after the five class bullets

> A requirement of this specification reaches a file declaring a format major
> other than 1 when, and only when, the field or structure it constrains is one
> `[R-CNT-24]` fixes in every format major version. This specification places
> the check for every such requirement at or before the version gate: §6.2
> orders them there, and `[R-CNT-04]` places the front signature block's check
> ahead of all processing for a reader holding those bytes resident. A reader
> MUST apply each such requirement to every file whatever major it declares, and
> MUST treat a failure of one as reject-file on that requirement's own ground
> and not on capability grounds — such a failure establishes that the byte
> sequence is not a conforming file under any format major version
> (`[R-CNT-24]`), which is a finding about its bytes — and the distinct
> diagnostic `[R-CNT-07]` asks for is owed where every such requirement is
> satisfied and the declared major is one the reader does not implement. A
> verifier that establishes such a failure reports *nonconforming*, the priority
> rule above applying whatever major the file declares. Every other requirement
> of this specification governs a structure this document defines for format
> major 1 alone: it is not assessed against a file declaring another major, no
> violation of it is established there, and no row of §21 restating it records
> such a file. `[R-CNF-13]`

## Final draft — §21.2, first paragraph, in full

> Outcome: reject-file. 36 conditions. Which of these rows reach a file
> declaring a format major other than 1, and which are not assessed against one,
> follows from `[R-CNF-13]` (§2.3).

## Cost

No row's Condition, Instances, Detector, Detected, or Governing rule cell
changes. 36 file-scope conditions unchanged; §21.8's "121 conditions over 277
instances" unchanged; the vector corpus unchanged. One identifier added,
`[R-CNF-13]`, in a prefix that already exists. §21.2 sheds ~115 words; §2.3
gains ~175. Appendix H is non-normative and needs no edit ("no violation row of
§21.2–§21.5 applies" remains true).

Left open for the maintainer: (i) `[R-CNF-13]` as a new identifier versus
folding into `[R-CNF-02]`; (ii) whether the §21.2 pointer would sit better in
§21.1, which governs the whole register; (iii) whether §6.2's sentence "only
these touch fields whose positions are fixed across all majors (`[R-CNT-24]`)"
should gain a back-reference to `[R-CNF-13]`, which would make the equivalence
navigable from both ends — not required, since neither statement depends on the
other for its force.
