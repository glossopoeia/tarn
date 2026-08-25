# §21.2 preamble — testing the "subject property" candidate for reach

Working transcript. Verbatim, in order of work.

## 0. Disclosure

**Files read:** exactly one — `/Users/robertkleffner/Documents/GitHub/tarn/spec/tarn.md`.
No docs/, no ADRs, no conformance/, no registry.json, no git history, no web.

**Commands run** (all read only that one file, or nothing):

1. `wc -l -c spec/tarn.md` → 4495 lines, 273042 bytes.
2. `grep -n "^#" spec/tarn.md | head -200` — section index.
3. `sed -n '3351,3500p'` — §21.1, §21.2 preamble, the full F-table, head of §21.3.
4. `sed -n '557,700p'` — §5.1, §5.2, head of §6.
5. `sed -n '695,870p'` — §6.1, §6.2, §6.3, §6.4.
6. `sed -n '94,280p'` — §2.1–§2.5.
7. `python3` heredoc: read the file, `re.sub(r'\s+',' ',t)` to defeat the hard wrap,
   then searched the flattened text for the short fragments `foreign`, `other major`,
   `another major`, `major it does not`, `R-CNT-24`, `128-byte`, `128 bytes`,
   `unimplemented major`, `capability ground`, printing ±220 chars of context.
   Every fragment is short enough that no line break can split it.
8. `python3` heredoc, same flattening, fragment `geometry` — to check whether
   "that file's *geometry*" in the current preamble is a defined term.
9. `sed -n '2763,2810p;3612,3670p'` — §19.2, §21.6.
10. `sed -n '3430,3448p' | cat -n` — the exact preamble text to be replaced.

**Unrequested context.** My runtime placed material in context before I began:
a project instruction file pointing at another file, an index of the maintainer's
personal memory notes with their one-line summaries, an environment block naming
the working directory / branch / recent commit subjects and a git status, and a
list of available tools and skills. None of it is the specification and none of
it is evidence about the specification. I disregarded all of it; nothing in this
transcript or in the verdict derives from it, and I do not repeat its contents.

## 1. The text under examination (verbatim, spec/tarn.md lines 3432–3446)

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

Two independent defects, before the candidate is even applied:

- **"Four rows"** is a closed count in normative prose — a claim about the
  whole register, checkable only against the rows someone has thought of.
- **"that file's *geometry*"** is not this document's term. Every other use of
  *geometry* in the specification is the layer model's (rank d, extents Eᵢ, tile
  extents Tᵢ, addressed-tile count N) — §11.1 is titled "Geometry and its
  validity floor", `[R-CNT-17]` speaks of "the geometry-derived addressed-tile
  count", L21 and L32 are geometry rows, §7.3's registry test is "every geometry
  identical". No file-scope structure is called geometry anywhere else. So the
  italicised coinage names the complement of the four listed rows and nothing
  more: it is the list again, wearing a word.

## 2. The candidate

> a row reaches a file declaring a foreign major exactly where its condition can
> be established without consulting any field a future major may redefine.

## 3. The ground truth the candidate must reproduce

`[R-CNT-24]` (§6.3), verbatim:

> In every format major version, permanently: the final 64 bytes of a file
> contain the trailer magic at F − 64, version_major and version_minor at
> F − 56, and a CRC-32C at F − 4 covering bytes [F − 64, F − 4); and the front
> signature block (§6.1) is constant. A future major MAY redefine only the
> remaining 48 trailer bytes and MUST NOT grow the trailer; additional space
> comes from structures placed before it. The format-major-1 trailer has zero
> slack: every byte is assigned.

Fixed in every major: front block [0, 16); trailer magic [F−64, F−56);
version_major and version_minor [F−56, F−52); terminal CRC-32C [F−4, F) over
[F−64, F−4); and the trailer's 64-byte size (MUST NOT grow).

Redefinable: trailer bytes [F−52, F−4) — i.e. trailer offsets 12–60: `flags`,
`generation`, `dir_offset`, `dir_length`, `committed_file_length`, `file_id`,
`reserved` — and, transitively, every structure those fields reach and every
quantity this text derives from them.

Corroborating order, §6.2 `[R-CNT-06]`: "A reader MUST validate, in order: the
trailer magic; the trailer CRC; the version gate (§6.3) — only these touch
fields whose positions are fixed across all majors (`[R-CNT-24]`)".
And `[R-CNT-04]` (§6.1) puts the front-block equality check "before other
processing" for a reader holding [0, 16) resident — that check is *not* in
§6.2's ordered list at all, which is why the current preamble needs two
separate justifications for its four rows.

## 4. Applying the candidate to all 36 file-scope rows

Column *fields consulted* lists what the row's condition reads as a field.
"C" = candidate's answer. "R" = the answer the rest of the document requires
(from §6.2's ordering, `[R-CNT-24]`, `[R-CNF-02]`).

| # | Subject / fields the condition consults | fixed in every major? | C | R | agree |
|---|---|---|---|---|---|
| F1 | front block bytes [0,8); trailer magic at F−64 | yes, both (`[R-CNT-24]`) | reaches | reaches | ✓ |
| F2 | dir_offset; dir_length; committed_file_length; generation; record extent_offset/extent_length | no — all in the redefinable 48, or reached through them | no | no | ✓ |
| F3 | dir_offset + dir_length; record extent_offset + extent_length | no | no | no | ✓ |
| F4 | layer record name fields, via the live directory | no (dir_offset/dir_length) | no | no | ✓ |
| F5 | **F, the physical file size**; committed_file_length | **the F instance consults no field at all** | **reaches** | **does not reach** | ✗ **BREAKS** |
| F6 | front block bytes [0,16) | yes | reaches | reaches | ✓ |
| F7 | structures between directory end and trailer | no (dir_offset, dir_length, extents) | no | no | ✓ |
| F8 | trailer magic at F−64 | yes | reaches | reaches | ✓ |
| F9 | dir_offset | no | no | no | ✓ |
| F10 | dir_offset + dir_length against F − 64 | no | no | no | ✓ |
| F11 | generation | no | no | no | ✓ |
| F12 | file_id | no | no | no | ✓ |
| F13 | committed_file_length mod 64 | no | no | no | ✓ |
| F14 | the u32 at trailer offset 60 (= F−4) vs CRC-32C of trailer [0,60) (= [F−64, F−4)) | yes — the CRC and its coverage are fixed; the covered *bytes* include redefinable ones but are consumed as CRC input, not read as fields | reaches | reaches | ✓ |
| F15 | trailer reserved [56,60) | no — squarely inside the 48 bytes a future major MAY redefine | no | no | ✓ |
| F16 | dir_length | no | no | no | ✓ |
| F17 | committed_file_length vs transport-authoritative size | no (committed_file_length) | no | no | ✓ |
| F18 | version_major = 0 | position fixed; the value rule is `[R-CNT-07]`'s | vacuous | outside the premise | ✓ (see §6 below) |
| F19 | flags bits 0–15 | no | no | no | ✓ |
| F20 | directory region CRC over dir_length − 4 bytes | no | no | no | ✓ |
| F21 | user-metadata record extent slot (0,0) | no | no | no | ✓ |
| F22 | user-metadata record extent_length < 5 | no | no | no | ✓ |
| F23 | user-metadata record inline_length ≠ 1 | no | no | no | ✓ |
| F24 | top-level record type = 0x0000 | no | no | no | ✓ |
| F25 | record flags MU=1 with PE=0 | no | no | no | ✓ |
| F26 | record reserved flag bits 2–15 | no | no | no | ✓ |
| F27 | user-metadata document member ordering | no | no | no | ✓ |
| F28 | stored MU/PE vs §7.3 registry | no | no | no | ✓ |
| F29 | record header / inline_length / trailing residue vs dir_offset + dir_length − 4 | no | no | no | ✓ |
| F30 | record extent slot half-zero | no | no | no | ✓ |
| F31 | record extent_offset in 1–15 | no | no | no | ✓ |
| F32 | record extent_offset + extent_length vs F − 64 | no | no | no | ✓ |
| F33 | coverage walk: tile extents, index regions, record extents, sub-record extents, directory | no | no | no | ✓ |
| F34 | two type-0x0002 records in the directory | no | no | no | ✓ |
| F35 | reserved-range type with MU = 1 | no | no | no | ✓ |
| F36 | reserved-range type value | no | no | no | ✓ |

Result: 35 of 36 agree. **F5 breaks it.**

## 5. The break, in full

F5's row, verbatim from the table:

> | F5 | File size is below the 128-byte minimum, so the front block, directory,
> pre-trailer pad and trailer cannot all fit | F (physical file size);
> committed_file_length | reader | open | `[R-CNT-27]` (R-CNT-01, R-CNT-06) |

F5 is the one row whose subject is a **physical property of the file rather than
a declared field**. Its first instance ranges over *F, the physical file size*.
A physical file size is not a field, so no future major can redefine it, so the
candidate's test is satisfied vacuously and the candidate says **F5 reaches a
file declaring a foreign major**.

That answer contradicts the document in two places.

**(a) §6.2's ordering.** `[R-CNT-06]` puts the version gate third, after only the
trailer magic and the trailer CRC. F5's check is not among them (its detection
point is *open*, and its governing rule `[R-CNT-27]` is a §5.1 rule, not one of
the two §6.2 orders ahead of the gate). A 100-byte file declaring major 7 is
refused at the gate on capability grounds before the 128-byte floor is ever
tested — and 100 bytes is enough to carry every byte `[R-CNT-24]` fixes: the
front block at [0,16), the trailer at [36,100) with magic at F−64 = 36,
version_major at F−56 = 44, CRC at F−4 = 96. There is nothing incoherent about
such a file; this text simply declines to judge it.

**(b) `[R-CNF-02]` / `[R-CNT-27]`.** The 128-byte floor is not a universal fact
about TARN files. `[R-CNT-27]` derives it, verbatim (§5.1):

> No conforming file is shorter than 128 bytes: the front signature block, a
> directory of at least 4 bytes at an offset of at least 16, and the 64-byte
> trailer at a 64-aligned offset cannot be satisfied in fewer.

Of its three ingredients, only the front block and the trailer's 64-byte size
are fixed by `[R-CNT-24]`. "A directory of at least 4 bytes at an offset of at
least 16" is `dir_length` and `dir_offset` — trailer offsets 24 and 32, inside
the 48 bytes a future major MAY redefine. "At a 64-aligned offset" is
`committed_file_length` being a multiple of 64 — trailer offset 40, likewise
redefinable. §21.9 records the floor among the limits that follow "from
arithmetic over structures a generation cannot omit" — a generation of *this*
major. A future major with no directory region, or with a different alignment,
has a different floor. So F5 asserts an invariant of format major 1 alone, and
recording it against a foreign-major file would be exactly the "finding about
its bytes" that `[R-CNF-02]` says the refusal is not.

**The candidate cannot be rescued by re-reading "consulting a field".** There are
only two readings, and each gets one of F5/F14 wrong:

- *Narrow* — a field is consulted when its value is read and interpreted as that
  field. Then F14 reaches (it consumes trailer bytes [0,60) as CRC input, never
  interpreting `dir_offset` or `flags` as fields) — correct. And F5 reaches,
  because F is not a field at all — **wrong**.
- *Broad* — a condition consults a field when its truth depends on a fact about
  that field. Then F5 is excluded, because the 128 floor depends on
  `dir_offset ≥ 16`, `dir_length ≥ 4` and 64-alignment — correct. And F14 is
  excluded too, because whether the stored u32 equals the CRC depends on the
  byte values at trailer offsets 12–56, which are `flags`, `generation`,
  `dir_offset`, `dir_length`, `committed_file_length`, `file_id` and `reserved` —
  **wrong**, and wrong about one of the only two checks §6.2 itself places
  before the gate.

No third reading separates them: any reading that admits F14 admits F5, and any
reading that excludes F5 excludes F14. The candidate does not decide membership
for an arbitrary row.

## 6. Attempts to break it further (both failed to add a second defeater)

- **F18.** `version_major` sits at F−56, a position `[R-CNT-24]` fixes, so the
  candidate would seem to admit F18. Not a contradiction: a file with
  version_major = 0 declares no major at all, so it is not a file declaring a
  foreign major and the quantifier never ranges over it. §21.6 says so directly:
  version_major = 0 is "permanently invalid in every format major version".
  A domain clarification, not an exception — keep the sentence.
- **F15.** Its Governing rule cell is `` `[R-CNT-06]` (R-CNT-24) `` — the only
  non-reaching row that cites `[R-CNT-24]` at all. A reader skimming for the
  citation would misclassify it. But `[R-CNT-24]` is cited there for the
  opposite reason: the trailer's zero slack is why major 1 requires those four
  bytes zero, and those same bytes are inside the 48 a future major MAY
  redefine. F15 does not reach, under the candidate and under the repair alike.
- **F33, F31, F9, F5** all *mention* the front signature block or the live
  trailer in their condition text. None of them tests a `[R-CNT-24]` invariant;
  each tests a bound on a redefinable field (or, for F5, a derived floor).
  Mentioning a fixed structure is not asserting an invariant over it.

## 7. The repair

The candidate's instinct is right — reach is a property of the row's subject and
needs no reference to detection order — but it points at the wrong property.
"Which fields does the condition read" is a proxy. The thing itself is:

> **A row reaches a file declaring a foreign major exactly where the condition
> it states violates an invariant `[R-CNT-24]` fixes in every format major
> version.**

Total, and decidable against any candidate row, including one nobody has written:
read `[R-CNT-24]`, ask whether the invariant this condition negates is among the
ones it makes permanent. It is stated existentially ("violates *an* invariant"),
so a condition negating both a permanent invariant and a major-1-only one still
reaches — correctly, since the permanent one is establishable on its own.

Re-run over the 36: F1, F6, F8, F14 reach (front block; front block; trailer
magic; the terminal CRC and its fixed coverage). F18 is outside the premise. The
other 31 assert invariants of major 1 alone. Same dispositions the current
preamble reaches by listing four rows — obtained from a property instead.

Checks on the repair:

- **F5** — the invariant it violates is "F ≥ 128", which `[R-CNT-24]` does not
  fix. Does not reach. Correct.
- **F14** — the invariant is "a CRC-32C at F − 4 covering bytes [F−64, F−4)",
  which `[R-CNT-24]` fixes in those words. Reaches. Correct. The redefinable
  bytes it consumes are CRC input, not invariants it asserts anything about.
- **F15** — the invariant is "trailer reserved [56,60) zero", which is precisely
  what `[R-CNT-24]` licenses a future major to redefine. Does not reach.
- **A row nobody has written**, e.g. "the file is shorter than 64 bytes, so the
  fixed trailer cannot exist": the invariant is "the final 64 bytes contain the
  trailer magic at F − 64", fixed → reaches. Or "the trailer does not begin at a
  64-aligned offset": the alignment invariant is §6.2's, not `[R-CNT-24]`'s →
  does not reach. Both decided, neither in anyone's list.
- **Instance granularity.** The current preamble already reasons per instance
  ("F1's trailer-magic instance", "F1's front-block instance"). Under the repair
  F1's two instances agree, so no split arises among the 36 — but F5 shows that
  a row's instances *can* differ in subject, so the property must be stated as
  applying to the instance where they do. That is granularity, not an exception.
- **Detection order** is nowhere in the normative sentence. It belongs in a
  Rationale, and it corroborates: the checks §6.2 places before the gate are
  exactly the trailer-magic and terminal-CRC invariants, and `[R-CNT-04]` places
  the front-block check before other processing. Note that order alone would
  *under*-generate — §6.2's ordered list does not contain the front-block check
  at all, which is why the current preamble needs two justifications for one
  set of rows. The property needs one.
- **Actor and outcome.** "Reach" needs operational content, and §2.3 supplies it
  without invention: `[R-CNF-11]` gives a verifier *cannot establish* "when the
  file names a format major version it does not implement", and immediately adds
  "An established violation takes priority: a verifier that has established any
  violation reports *nonconforming*". A reaching row is establishable precisely
  because the invariant belongs to the file's own major too — so the verdict is
  under the major the file declares, and `[R-CNF-02]`'s "neither conforming nor
  nonconforming **under it**" (this text) is untouched. The reader clause is
  `[R-CNT-07]`'s: the refusal on capability grounds stands either way, and which
  ground is reported is a diagnostic question `[R-CNT-07]` already governs.

## 8. Verdict

WORKABLE_WITH_CHANGES. The approach — reach as a subject property, no detection
order — survives. The candidate's wording does not: **F5 defeats it**, in its
"F (physical file size)" instance, and no reading of "consulting a field"
excludes F5 without also excluding F14. Anchoring the property on the invariants
`[R-CNT-24]` makes permanent, rather than on the fields a condition reads,
decides all 36 rows correctly, decides rows nobody has written, and drops the
closed count of four.
