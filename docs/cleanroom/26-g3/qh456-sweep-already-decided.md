# Sweep: what the TARN document already decides about a file declaring a format major other than 1

Working transcript. Line numbers are physical line numbers in
`/Users/robertkleffner/Documents/GitHub/tarn/spec/tarn.md` (4495 lines, 273042 bytes).

---

## 0. Disclosure

**Files read:** exactly one — `/Users/robertkleffner/Documents/GitHub/tarn/spec/tarn.md`.
Nothing under `docs/`, `conformance/`, no `PLAN.md`, `OPEN-QUESTIONS.md`, `AGENTS.md`,
`README.md`, `spec/registry.json`, no git history, no web.

**Commands run** (all read only that file or ran pure computation):

- `wc -l` / `wc -c` on the spec.
- `grep -n "^#\{1,4\} "` — heading index.
- `grep -n -i "major"` — the primary term sweep.
- `grep -n -i` for: `foreign`, `capability`, `cannot establish`, `verdict`,
  `unimplemented`, `version gate`, `version_major`, `not implement`,
  `does not implement`, `certif`, `reader first`, `another major`, `other major`,
  `later major`, `future major`, `every major`, `per major`, `same major`, `majors`,
  `cross-major`, `forward`, `version_minor`, `version` (with already-seen lines filtered out).
- A Python pass that collapsed all whitespace across the whole file into a single
  normalised string with a byte→line map, then searched that string for phrases that
  can wrap across the hard wrap: `major other than`, `a major it`, `refuses`, `refusal`,
  `capability ground`, `declares no major`, `not implement`, `implements`, `implemented`,
  `this reader supports`, `neither conforming nor`. This is the search that guarantees a
  wrapped phrase could have been found; the absences reported below rest on it, not on
  the line-oriented greps.
- `sed -n` reads of: §1 (28–93), §2 entire (94–279), §4.3 (418–429), §4.7 excerpt
  (530–538), §6 entire (695–868), §7.4 closing note (1100–1112), §8.2 (1137–1157),
  §9.6 (1292–1324), §9.7 (1326–1375), §10.1 tail (1385–1392), §11.4 excerpt (1553–1567),
  §17.4 (2415–2432), §19.1–§19.3 head (2710–2810), §20.2 + §20.3 step 6 (2938–2955,
  3085–3100), §21.1–§21.2 (3351–3500), §21.5–§21.9 (3578–3830), §24 (4022–4103),
  Appendix E (4255–4267), Appendix H (4424–4495).

**Unrequested context.** Material appeared in my context before I began: a project
instruction file, an index of the maintainer's notes, an environment block naming the
branch and recent commit subjects, and tool/skill listings from the runtime. None of it
is part of the specification and none of it is evidence about the specification. I
disregarded all of it and do not repeat its contents; nothing below derives from it.

---

## 1. Passages found, in document order

### §2.3, "Conforming TARN file", lines 138–156 — `[R-CNF-02]`

> ```
> 138  - **Conforming TARN file.** A byte sequence satisfying every file-level
> 139    requirement of this specification. File conformance is a pure predicate
> 140    on bytes: it does not depend on any reader, writer, or environment.
> 141    It is always conformance to a stated format major version. This
> 142    document defines format major 1, and a file declaring another major
> 143    is neither conforming nor nonconforming under it: a reader refuses
> 144    such a file on capability grounds (§6.3, `[R-CNT-07]`), and that
> 145    refusal is not a finding about its bytes.
> ```

Normative (§2.3 is body text, not a `>` block, not §1, not an appendix — per `[R-CNF-01]`
at line 104–106). Fixes: (a) conformance is *relative to a declared major*; (b) this text
defines major 1 only; (c) a foreign-major file is **neither conforming nor nonconforming
under this text**; (d) the reader's refusal is a *capability* refusal, not a byte finding.
Leaves open: what a verifier's *verdict* is (this bullet speaks only of the file predicate
and the reader's refusal); what happens if the same file also breaks a rule this text
says is fixed across all majors.

### §2.3, "Conforming reader", lines 157–164 — `[R-CNF-03]`

> ```
> 157  - **Conforming reader.** A reader MUST accept every conforming file of
> 158    a format major version it implements, carrying no record of a type
> 159    it does not implement with MUST_UNDERSTAND = 1 ...
> 163    limits table (§21.9's `[R-ERR-04]` governs a refusal on that last
> 164    ground; §21.6's closing paragraph names the other two),
> ```

Normative. Fixes: the reader's *acceptance* obligation is scoped to majors the reader
implements, so a foreign-major file is outside it entirely — declining it costs a reader
nothing on `[R-CNF-03]`. Also fixes the cross-reference: §21.6's closing paragraph is the
place this document treats the foreign-major refusal, and §21.9's `[R-ERR-04]` is *not*.

### §2.3, "Conforming verifier", lines 189–223 — `[R-CNF-11]` — **the verdict passage**

> ```
> 189  - **Conforming verifier.** A reader that additionally checks every
> 190    file-level requirement — including those ordinary readers are
> 191    exempted from — and certifies conformance. Verifiers and updaters are
> 192    readers of the files they process and inherit every reader
> 193    obligation. A verifier reports one of three verdicts: *conforming*,
> 194    *nonconforming*, or *cannot establish* — the last where some
> 195    requirement is one it is unable to check on a capability or
> 196    resource ground, as when the file names a
> 197    format major version it does not implement, when a record carries
> 198    MUST_UNDERSTAND = 1 with a type it does not implement (§21.6), when
> 199    it cannot execute a codec or filter (`[R-COD-11]`), when it
> 200    declines a layer's or a tile's decode on resource grounds and so
> 201    cannot check §14's decoded-content obligations (`[R-ERR-04]`,
> 202    `[R-SER-05]`, `[R-SER-08]`), or when it declines to decode a
> 203    user-metadata document (`[R-MTA-09]`). ...
> 207    *Cannot establish* is not a finding that the file is nonconforming,
> 208    and a verifier MUST NOT certify a file it reports that way. An
> 209    established violation takes priority: a verifier that has
> 210    established any violation reports *nonconforming*, however many
> 211    requirements it was unable to check, and *cannot establish* is
> 212    available only to a traversal that established no violation. A
> 213    verifier MUST report each requirement it was unable to check on a
> 214    capability or resource ground, naming the requirement and the
> 215    ground, whichever of the three
> 216    verdicts it reports; ...
> 218    A verifier MAY stop at the first violation it finds; one that does
> 219    MUST report each scope it did not examine as *unexamined*, ...
> 223    `[R-CNF-11]`
> ```

Normative. **This is the passage that answers the verdict question**, and it answers it by
name: "as when the file names a format major version it does not implement" is listed
first among the *cannot establish* grounds. See derivations §2 below.

### §2.4, lines 227–266 — `[R-CNF-07]`, `[R-CNF-12]`

Nothing here names a major. Two clauses bear on the derivation:

> ```
> 254  A file is conforming only if it satisfies every requirement at every
> 255  scope: ... and a verifier
> 257  certifies only violation-free files.
> ```

Relevant only as the general certification bar.

### §4.3, lines 420–426 — `[R-ENC-07]`

> ```
> 420  Structures this specification defines with a fixed size have exactly
> 421  that size in every conforming file of a given format major version; for
> ...
> 423  index), the fixed size is per encoding. A reader that encounters a known
> 424  structure at any other size MUST treat it as a validity error at the
> 425  structure's owning scope; an unexpected size is never evidence of a
> 426  newer format version. `[R-ENC-07]`
> ```

Normative. Fixes: fixed sizes are *per major*, and an off-size structure is never to be
read as forward-compatibility slack. Bears on foreign majors only negatively — a major-1
reader never infers a newer major from a size.

### §4.7, lines 536–537 — `[R-ENC-16]`

> ```
> 536  format major 1 `version_minor` is the only descriptive field, and
> 537  every other field this specification defines is structural.
> ```

Normative. `version_major` is therefore **structural** — its value determines whether the
file is accepted at all. (Line 530–531 states the sense: "…is accepted at all, which is
the sense `[R-CNT-07]`, `[R-MTA-02]` and `[R-SEC-06]` already use.")

### §6.2 trailer table, line 747

> ```
> 747  | 8 | 2 | u16 | version_major | structural | 1 (0 invalid; others: §6.3) |
> ```

Normative table cell. Fixes: the only valid value under this text is 1; 0 is invalid;
everything else is deferred to §6.3.

### §6.2 ordering, lines 773–782 — `[R-CNT-06]`

> ```
> 773  A reader MUST validate, in order: the trailer magic; the trailer CRC;
> 774  the version gate (§6.3) — only these touch fields whose positions are
> 775  fixed across all majors (`[R-CNT-24]`) — and then, those gates passed,
> 776  MUST validate all of the following before acting on the fields
> 777  involved: the flag gates (§6.3); committed_file_length equals the file
> 778  size ... reserved
> 781  bytes zero. Any failure is reject-file. The owning scope of the front
> 782  signature block and the trailer is the file. `[R-CNT-06]`
> ```

Normative, and load-bearing. Fixes the **ordering**: magic → trailer CRC → version gate →
everything else. It fixes exactly three checks as safe on a file of unknown major, and
says so in its own parenthesis. Every other trailer field gate is behind the version gate,
so on a foreign-major file none of them ever runs.

### §6.3, lines 791–798 — `[R-CNT-07]` — **the reader-side decision**

> ```
> 791  A reader MUST reject-file when version_major is 0 (invalid) or is a
> 792  major it does not implement, and the diagnostic for an unimplemented
> 793  major SHOULD be distinct from both "not a TARN file" and "corrupt"
> 794  (e.g. "TARN format major N; this reader supports major 1") — a reader
> 795  that reports an unimplemented major as corruption misleads users into
> 796  discarding files that current software reads. A reader MUST NOT reject
> 797  a file for its version_minor: minor releases are additive-only, and
> 798  all feature gating is structural (records, enums, flags). `[R-CNT-07]`
> ```

Normative. Fixes: **reader outcome = reject-file, MUST**; the diagnostic **SHOULD** be a
third category distinct from "not a TARN file" and from "corrupt", with the consequence of
deviation stated (users discard intact files). Note the rule's subject is "a major it does
not implement" — it is reader-relative, not "a major other than 1".

Leaves open: nothing at MUST level forbids reporting the refusal as a validity error — the
distinctness requirement is a SHOULD. (`[R-ERR-04]`'s MUST at line 3786–3790 is expressly
about *resource* grounds and expressly excludes this one; see below.)

### §6.3, lines 800–807 — `[R-CNT-24]` — **what is fixed across every major**

> ```
> 800  In every format major version, permanently: the final 64 bytes of a
> 801  file contain the trailer magic at F − 64, version_major and
> 802  version_minor at F − 56, and a CRC-32C at F − 4 covering bytes
> 803  [F − 64, F − 4); and the front signature block (§6.1) is constant. A
> 804  future major MAY redefine only the remaining 48 trailer bytes and MUST
> 805  NOT grow the trailer; additional space comes from structures placed
> 806  before it. The format-major-1 trailer has zero slack: every byte is
> 807  assigned. `[R-CNT-24]`
> ```

Normative, and it is the only rule in the document that binds *files of other majors*.
Fixes, for a file of any major: trailer is the final 64 bytes; magic at F−64;
version_major/version_minor at F−56; CRC-32C at F−4 over [F−64, F−4); front block
[0,16) constant. Fixes for future majors: MAY redefine only trailer bytes [16,64);
MUST NOT grow the trailer.

This is what makes the foreign-major *diagnosis* possible at all: a major-1 reader can
read a major-N file's declared major, and can verify its magic and its trailer CRC, and
this rule is why.

### §6.1, lines 699 and 717–727 — `[R-CNT-04]`

> ```
> 699  Bytes [0, 16) of every file, constant in every format major version:
> ```
> ```
> 717  A reader whose open leaves bytes
> 718  [0, 16) **resident** ... MUST verify the full block by byte
> 720  equality before other processing, and MUST treat any mismatch as
> 721  reject-file. A reader that would have to issue a further range request
> 722  to obtain those bytes MAY defer or omit the check ...
> ```

Normative. Line 699 restates the cross-major constancy of the front block. The residency
test decides whether the front-block check runs *before* the trailer path at all.

### §6.4 / §19.1 — the open path

§19.1 step 2, lines 2725–2729:

> ```
> 2725  2. **Trailer.** Fetch bytes [F − 64, F) and validate them in
> 2726     §6.2's fixed order — magic, trailer CRC, version gate, then the
> 2727     remaining field gates (`[R-CNT-06]`, `[R-CNT-07]`,
> 2728     `[R-CNT-08]`). ...
> ```

Normative. Places the version gate at **open**, in step 2, after magic and CRC and before
the directory fetch (step 3). So on a foreign-major file the open terminates in step 2:
the directory is never fetched, no record walk happens, no layer table is built.

§19.2, lines 2771–2774, places the trailer at the "at open" tier. Consistent.

### §9.6, lines 1294–1305 — `[R-LIF-06]` (recovery scan)

> ```
> 1295  offsets o for the trailer magic; on a match, require the trailer CRC
> 1296  to verify and committed_file_length = o + 64. ...
> 1301  `[R-LIF-08]`), and no verdict turns on the probe: a file whose final
> 1302  64 bytes are not a valid trailer fails `[R-CNT-06]`'s gates on the
> 1303  bytes handed over (§21.2 rows F8, F14 and F17 — the magic, the
> 1304  trailer CRC and the length cross-check), ...
> ```

Normative, but says nothing about majors. Noted here because the probe's third predicate
is `committed_file_length` — a field at trailer offset 40, i.e. inside the 48 bytes
`[R-CNT-24]` lets a future major redefine. The recovery scan is therefore a major-1
procedure. The document does not say so, and does not say what a recovery tool does with
a candidate whose magic and CRC verify but whose declared major is not 1. **Undecided.**

### §10.1, lines 1388–1392 — `[R-EXT-01]`

> ```
> 1388  Nothing else extends this format. A new fixed field, a widened
> 1389  structure, a changed field width, or a reinterpreted assigned value
> 1390  is a new format major version (`[R-CNT-24]`) — never a minor
> 1391  revision, and never an implementation's private convention.
> 1392  `[R-EXT-01]`
> ```

Normative. Fixes what *causes* a new major to exist. Says nothing about how a file
declaring one is handled.

### §11.4, lines 1556–1567 — `[R-GEO-05]`

> ```
> 1556  ... in-tile
> 1557  sample order is row-major for every linearization value, in every
> 1558  version of this format. Field values: 0 is invalid; **1 = row-major** —
> ...
> 1566  experimental range, which no conforming writer of format major
> 1567  version 1 emits. `[R-GEO-05]`
> ```

Normative. One further cross-major invariant ("in every version of this format": in-tile
sample order is row-major). Nothing about handling a foreign-major file.

### §15.1, line 2004 — `[R-IDX-01]` context

> ```
> 2004  index_encoding 1 (the only encoding this format major version defines,
> ```

Normative, scoping only. Not about foreign-major handling.

### §17.4, lines 2417–2432 — `[R-COD-11]` (structural parallel)

> ```
> 2418  `[R-SER-08]`) require decoding. A verifier that cannot execute a
> 2419  layer's codec or filter cannot establish that layer's conformance
> 2420  and MUST NOT certify the file. That inability is not a finding that
> 2421  the file is nonconforming, and it fixes the file's verdict as
> 2422  *cannot establish* only where the verifier established no violation
> 2423  elsewhere (`[R-CNF-11]`). ...
> ```

Normative. Not about majors, but it is the document's one *worked* instance of the
cannot-establish machinery, and its shape is exactly what §2.3 applies to the foreign-major
case: "*cannot establish* only where the verifier established no violation elsewhere".
It is the model for the derivation in §2 below. §18.2 line 2527 and 2533 do the same for
an over-large user-metadata document ("it fixes the file's verdict as *cannot establish*").

Note by contrast: for the foreign-major case **no rule of the same shape exists**. There is
no sentence anywhere reading "a foreign major fixes the file's verdict as *cannot
establish*" — the only statement is `[R-CNF-11]`'s enumeration of grounds at lines 196–197.
Confirmed by the normalised search for `cannot establish` (5 hits: 194, 207, 211, 221, plus
2419/2422 and 2527/2533) — none of the §17.4/§18.2-style sentences mentions a major.

### §21.1, lines 3355–3385 — `[R-ERR-02]` framing

> ```
> 3355  The register — §21.2 through §21.5 (`[R-ERR-02]`) — enumerates
> 3356  every detectable file-conformance violation this specification names: each row is one
> ...
> 3365  ... Its **completeness is normative** — a
> 3366  *detectable* file-conformance violation this specification names and
> 3367  the register omits is a defect in this document ...
> 3370  ... but each row *restates* its governing rule, and where a
> 3371  row and the rule it cites diverge, **the rule governs**.
> ...
> 3379  point are the ones that apply. The subsections after §21.5 are not
> 3380  part of the register and carry no rows: neither this completeness
> 3381  clause nor the instance arithmetic below reaches §21.6's defined
> 3382  non-violations, ...
> 3383  §21.6's entries restate their governing rules on
> 3384  the same terms a row does, and where such an entry and the rule it
> 3385  cites diverge, the rule governs there too.
> ```

Normative. Fixes: the register's subject is *file-conformance violations*; §21.6 is not
part of the register; §21.6's entries are restatements subordinate to their governing rules.

### §21.2 opening paragraph, lines 3432–3446 — **the passage under examination**

> ```
> 3432  Outcome: reject-file. 36 conditions. A file declaring a format major
> 3433  other than 1 is neither conforming nor nonconforming under this text
> 3434  (§2.3, `[R-CNF-02]`), and the rows below whose subject is that
> 3435  file's *geometry* do not reach it: §6.2 puts the version gate ahead
> 3436  of every check but the trailer magic and the trailer CRC, so such a
> 3437  file is refused on capability grounds first. Four rows are outside
> 3438  that reasoning and do reach it, because their subject is a field
> 3439  fixed across every major (`[R-CNT-24]`): F8 and F1's trailer-magic
> 3440  instance, F14's trailer CRC — the two checks §6.2 places before the
> 3441  gate — and F6 with F1's front-block instance, which `[R-CNT-04]`
> 3442  places before other processing for a reader that already holds those
> 3443  bytes, one that would have to fetch them being free to defer or omit
> 3444  the check. F18 is not an exception but a case
> 3445  outside the premise: version_major = 0 declares no major at all and
> 3446  is permanently invalid in every one (§21.6).
> ```

Normative (register prose, not a `>` block). Fixes:

1. Restates §2.3: foreign-major file is neither conforming nor nonconforming under this text.
2. Most of §21.2's 36 rows **do not reach** such a file, on an ordering argument: the version
   gate precedes them.
3. **Four rows do reach it** — F1 (both instances, split across the two clauses), F6, F8, F14
   — because their subject is a field `[R-CNT-24]` fixes across every major.
4. F18 (version_major = 0) is outside the premise entirely: 0 declares no major.

The rows named (lines 3450, 3455, 3457, 3463):

> ```
> 3450  | F1 | A signature constant is stored byte-reversed ... | front signature block bytes [0,8); trailer magic at F-64 | reader | open | `[R-ENC-02]` (R-CNT-04, R-CNT-06) |
> 3455  | F6 | The 16-byte front signature block is not byte-identical to the constant; the obligation binds a reader holding those bytes resident, and a reader that would have to fetch them MAY defer or omit the check (`[R-CNT-04]`); a verifier holds no such exemption (§2.3) | magic bytes [0,8); reserved bytes [8,16) | reader | open | `[R-CNT-04]` |
> 3457  | F8 | The 8 bytes at F-64 are not exactly the trailer magic 8A 4E 52 41 54 0D 0A 1A | trailer magic | reader | open | `[R-CNT-06]` |
> 3463  | F14 | The u32 at trailer offset 60 does not equal the CRC-32C of trailer bytes [0,60) | trailer CRC | reader | open | `[R-CNT-06]` (R-CNT-20, R-ENC-09) |
> 3467  | F18 | Trailer version_major is 0, a permanently invalid major in every format major version | version_major | reader | open | `[R-CNT-07]` |
> ```

### §21.6 closing prose, lines 3645–3664 — **the second decisive passage**

> ```
> 3645  Two structural cases are **conforming files a reader nevertheless
> 3646  refuses**. The first is **version_major naming a major this reader
> 3647  does not implement**: the reader rejects the file (`[R-CNT-07]`), but
> 3648  the file can be perfectly conforming under that major. The second is
> 3649  an **experimental-range top-level record type carrying MU = 1**
> 3650  (§10.2, §10.3): `[R-CNT-15]` obliges the reader to reject, and
> 3651  `[R-CNF-02]` makes the file conforming all the same. ...
> 3656  ... In both the outcome records a reader's capability, not a defect
> 3657  in the bytes, and the diagnostic ought to distinguish the two.
> 3658  Neither is a register row: the register enumerates file-conformance
> 3659  violations (§21.1), and a file this document declines to judge is not
> 3660  one. What is registered in each case is the neighbouring condition
> 3661  that *is* a violation — version_major = 0, permanently invalid in
> 3662  every format major version (F18, `[R-CNT-07]`), and a *reserved*-range
> 3663  type, whose emission `[R-CNT-15]` does make a violation (F35, F36,
> 3664  L24, L25).
> ```

Normative prose (not a `>` block, not inside §21.6's table). §2.3 line 164 points here by
name. Fixes: the foreign-major case is a *conforming file a reader refuses*; the refusal
records reader capability, not a byte defect; it is **not a register row** and never will
be; the registered neighbour is F18. Note the last clause of line 3657, "the diagnostic
ought to distinguish the two" — keyword-free, and reading as advice; `[R-CNT-07]`'s
SHOULD at line 792–794 is the binding form.

Note also §21.6's *table* has no foreign-major row. Its nearest row (line 3625) is:

> ```
> 3625  | version_minor is higher than this text defines | Accepted; minors never gate | `[R-CNT-07]` |
> ```

### §21.9, lines 3780–3790 — `[R-ERR-04]`

> ```
> 3780  A file exceeding any of these remains conforming, and a reader MAY
> 3781  decline it — at the whole file, or at the narrowest scope whose
> 3782  declarations exceed what it can serve, a layer or a tile. Software that declines **on that ground** a file whose every quantity lies
> 3783  within the table is not a conforming reader (`[R-CNF-03]`) — the two
> 3784  capability refusals §21.6 names, a foreign format major and an
> 3785  unimplemented MU = 1 type, are not this ground — the
> 3786  guarantees are the floor, not a suggestion. Either way, a refusal
> 3787  on resource grounds MUST be reported as a resource limit and not as
> 3788  a validity error: the two send a user to opposite remedies, and a
> 3789  reader that reports "too large" as "corrupt" invites the deletion
> 3790  of intact data. `[R-ERR-04]`
> ```

Normative. Fixes two things by exclusion: (a) declining a foreign-major file is **not** a
`[R-CNF-03]` failure — it is not "that ground"; (b) the MUST at line 3786–3788 about
reporting is scoped to **resource** grounds, and the foreign major is expressly a
*capability* refusal, so that MUST does not reach it. The only reporting obligation for
the foreign-major refusal is `[R-CNT-07]`'s SHOULD.

Also note line 3784 uses the term **"a foreign format major"** — the only occurrence of
"foreign" in that sense in the document (the other two, lines 379 and 3450, are
"foreign-endian").

### §24, lines 4037–4046 and 4079–4082 — `[R-VEC-02]`, `[R-VEC-03]`

> ```
> 4037  Each vector is one file plus a manifest entry recording, at minimum:
> 4038  its identifier; whether the file is **conforming**; the decoded
> ...
> 4042  file damages, the outcome class (§2.4), the scope, and the §21
> 4043  register row it exercises together with that row's governing
> 4044  requirement identifier ...
> ```
> ```
> 4079  Coverage is the corpus's own obligation, inherited from
> 4080  `[R-ERR-02]`: every register row has at least one vector for each
> 4081  instance it names, and every sentinel, every boundary value, and every
> 4082  hard limit of `[R-ERR-05]` has one at its stated bound.
> ```

Normative. Fixes: the corpus's coverage obligation runs to register rows, boundary values,
sentinels and `[R-ERR-05]`'s hard limits. Since the foreign-major case is expressly not a
register row (§21.6 line 3658), **no vector is owed for it**. And the manifest's
conformance field is a binary ("whether the file is conforming") that a foreign-major file
fits neither side of. §24 does not address this. **Undecided.**

### Appendix H, lines 4470–4495 (non-normative)

> ```
> 4491  ... reports *nonconforming*
> 4492  whenever it has established a violation, reserving *cannot
> 4493  establish* for a traversal that established none; and reports each
> 4494  requirement it was unable to check on a capability or resource
> 4495  ground, and each scope it did not examine (`[R-CNF-11]`).
> ```

Non-normative by its own heading ("Conformance checklists (non-normative)") and by
line 4427–4428: "each entry's authority is the requirement or section cited, never this
summary". It restates `[R-CNF-11]`'s priority clause and does **not** mention majors.

### Appendix A, line 4133; Appendix E, lines 4261, 4265–4266 (non-normative)

> ```
> 4133  | [72, 74) | `01 00` | version_major = 1 |
> ```
> ```
> 4261  | 1.0 (draft) | unreleased | First complete draft of format major version 1. |
> 4265  Minor versions are additive only (§6.3); a change that is not additive
> 4266  is a new format major version.
> ```

Both appendices are labelled non-normative in their headings. Nothing new.

---

## 2. Derivations

### D1 — The verdict for a foreign-major file that exhibits no establishable violation

Premises, all verbatim above:

1. §2.3 / `[R-CNF-11]`, lines 193–197: "A verifier reports one of three verdicts:
   *conforming*, *nonconforming*, or *cannot establish* — the last where some requirement
   is one it is unable to check on a capability or resource ground, **as when the file names
   a format major version it does not implement**".
2. §2.3 / `[R-CNF-11]`, lines 207–212: "*Cannot establish* is not a finding that the file is
   nonconforming, and a verifier MUST NOT certify a file it reports that way. An established
   violation takes priority: … *cannot establish* is available only to a traversal that
   established no violation."
3. §2.3, lines 191–193: "Verifiers and updaters are readers of the files they process and
   inherit every reader obligation."
4. §6.3 / `[R-CNT-07]`, line 791: reader MUST reject-file on a major it does not implement.

Derivation. Premise 1 places the foreign-major case squarely inside the enumerated grounds
for *cannot establish* — it is named, not inferred. *Conforming* is excluded twice over:
by §2.3 line 143 (such a file is not conforming under this text) and by premise 2's
"MUST NOT certify a file it reports that way". *Nonconforming* is excluded so long as the
traversal established no violation, since §2.3 line 145 says the refusal "is not a finding
about its bytes" and premise 2 says *cannot establish* "is not a finding that the file is
nonconforming". Hence: **verdict = *cannot establish***, and separately, as a reader outcome
under premises 3–4, **reject-file**. The two are different registers of the vocabulary
(§2.4's outcome classes are reader outcomes; §2.3's three verdicts are verifier verdicts)
and the document keeps them apart, so there is no conflict between "rejects the file" and
"reports cannot establish".

This derivation is what §2.3's own cross-reference at line 164 anticipates
("§21.6's closing paragraph names the other two"), and it matches the worked shape
`[R-COD-11]` uses at §17.4 line 2421–2423 for an unexecutable codec.

**So the answer to the question that matters most is: yes, `[R-CNF-11]` already decides it,
by naming the case.**

### D2 — The verdict is *not* decided for a foreign-major file that also breaks F1/F6/F8/F14

Premises:

1. §21.2, lines 3432–3434: "A file declaring a format major other than 1 is neither
   conforming nor nonconforming under this text (§2.3, `[R-CNF-02]`)".
2. §21.2, lines 3437–3444: "Four rows are outside that reasoning and **do reach it**, because
   their subject is a field fixed across every major (`[R-CNT-24]`): F8 and F1's trailer-magic
   instance, F14's trailer CRC … and F6 with F1's front-block instance".
3. §21.1, lines 3355–3356: the register "enumerates every detectable **file-conformance
   violation** this specification names: each row is one malformed condition".
4. §2.3 / `[R-CNF-11]`, lines 208–212: "An established violation takes priority: a verifier
   that has established any violation reports *nonconforming*, however many requirements it
   was unable to check".

Derivation. Take a file declaring major 2 whose 8 bytes at F−64 are not the trailer magic.
By premise 2 that file is reached by F8. By premise 3 an F8 row is a file-conformance
violation. A verifier checks the magic first (§6.2 line 773) and therefore *establishes*
it — before the version gate ever runs. By premise 4 the verifier then reports
***nonconforming***. But premise 1 says the same file "is neither conforming nor
nonconforming under this text".

These two conclusions cannot both hold. The document therefore yields **no single answer**
for the intersection: foreign major *and* a violation of one of the four cross-major rows.
Either

- "reach it" at line 3437 means only that the *reader's reject-file outcome* fires at that
  check rather than at the gate — in which case no conformance finding is available, premise 1
  survives, and `[R-CNF-11]`'s priority clause must be read as not triggered because nothing
  was "established" in the conformance sense; or
- "reach it" means the row's condition is exhibited by the file as a violation — in which case
  premise 1's "neither conforming nor nonconforming" is false of that file, and the verdict is
  *nonconforming*.

The document does not say which. §21.1's tie-break ("where a row and the rule it cites
diverge, the rule governs", line 3370–3371) does not resolve it, because the divergence here
is between §21.2's own opening paragraph and `[R-CNF-11]`/`[R-CNF-02]`, not between a row and
its governing rule. **This is an undecided question I searched for specifically.** Searches:
normalised whole-document search for `major other than`, `neither conforming nor`,
`a major it`, `capability ground`, `refuses`, `refusal` (all hits reproduced in §1 above);
line search for `major` (28 hits, all read). No passage anywhere states what verdict follows
when a cross-major check fails on a foreign-major file.

### D3 — A writer under this text may not emit a foreign major (stated only by derivation)

Premises: §6.2 line 747, valid values "1 (0 invalid; others: §6.3)"; §2.3 lines 141–143,
"This document defines format major 1, and a file declaring another major is neither
conforming nor nonconforming under it"; §2.3 line 180, `[R-CNF-05]`: "A writer MUST emit only
conforming files."

Derivation. A file declaring major 2 is not a *conforming file* under this text (it is not
conforming under it; premise 2). A writer bound by this text MUST emit only conforming files
(premise 3). Therefore a writer bound by this text MUST NOT emit version_major ≠ 1.

Note what is *absent*: there is no keyword-bearing writer rule on `version_major` anywhere,
of the kind §6.1 line 706 gives the front block ("Writers MUST emit exactly these 16 bytes")
or `[R-GEO-05]` line 1560 gives linearization ("writers MUST NOT emit any other value").
Searched: `grep -n -i version_major` returns lines 747, 791, 801, 3445, 3467, 3646, 3661, 4133
— none is a writer rule. §20.2 (`[R-WRT-02]`, lines 2940–2953) enumerates the creation path
and never mentions version_major; §20.3 step 6 (line 3089–3093) enumerates what the commit
trailer carries — generation, file_id, ignore-lane bits, version_minor — and does not mention
version_major either. The obligation exists only as the derivation above.

### D4 — Detection point and I/O consequence

From §19.1 step 2 (lines 2725–2729) with §6.2's order (line 773): the version gate fires at
**open**, in the trailer step, after magic and trailer CRC, before every other trailer field
gate and before the directory fetch of step 3. Therefore, on a foreign-major file: no
directory is fetched, no record walk runs, no layer-name namespace is built, no extent is
touched. The refusal costs at most the front block plus 64 bytes. This is stated, and it is
also why §21.2's ordering argument works.

### D5 — §9.7's coverage walk cannot run on a foreign-major file

§9.7 / `[R-LIF-08]`, lines 1328–1331: "From the live trailer it reads the live directory and,
through its records and their sub-records, reaches the claimants `[R-CNT-02]` names". The
directory is located by `dir_offset`/`dir_length` at trailer offsets 24 and 32 — inside the
48 bytes `[R-CNT-24]` (line 804) permits a future major to redefine. So a major-1 verifier
has no defined way to start the walk on a foreign-major file. The document does not say what
the verifier reports for the slack total in that case; `[R-CNT-21]`'s "partial" machinery
(lines 1356–1360, 3626) is written for a walk that started and stopped, not for one that
never began. **Undecided.**

---

## 3. Searched-for absences (each backed by a search that could have succeeded)

All searches below were run over the whitespace-normalised whole document, so a phrase
spanning the hard wrap could have matched.

| Question | Searched | Result |
|---|---|---|
| Is there a §21.6 *table row* for a foreign major? | read §21.6's table, lines 3617–3632 | No. The case is in the closing prose, lines 3645–3664. |
| Is there a register row for a foreign major? | §21.2 rows read in full (3450–3485); §21.6 line 3658 states it explicitly | No, and never will be — line 3658–3660. |
| Is a conformance vector owed for one? | §21.8 (`[R-ERR-02]`, 3739–3742), §24 (`[R-VEC-02]`/`[R-VEC-03]`, 4037–4089) | No obligation. And §24's manifest binary "whether the file is conforming" has no third state. Undecided. |
| Does anything oblige a *writer* to emit version_major = 1 with a keyword? | `version_major` (8 hits), §20.2, §20.3 step 6 | No. Derivation D3 only. |
| Does anything say what an **updater** or **compactor** does with a foreign-major file? | `reader first` (1 hit, line 821, about incompat flag bits); §20.3 (2919–3165), §20.4 (3166–3215), §20.5 (3216–3350) skimmed for `major` — 0 hits in that range from the `major` grep | Nothing states it directly. Derivable only through §2.3 line 191–192 ("updaters are … readers … and inherit every reader obligation") plus `[R-CNT-07]`: the updater rejects at open and no commit is available. The document draws that inference explicitly for the *MU = 1* twin (line 3188) and for incompat flag bits (line 820–822), and **not** for the foreign major. |
| Does anything say what a **recovery tool** does with a foreign-major candidate? | §9.6 read in full (1292–1324); `major` grep has 0 hits in 1292–1324 | Nothing. Undecided (see §1, §9.6 note). |
| Is there a MUST-level rule on how the foreign-major refusal is *reported*? | `[R-CNT-07]` (791–798), `[R-ERR-04]` (3780–3790), §21.6 line 3657 | Only a SHOULD (`[R-CNT-07]`) and a keyword-free "ought" (line 3657). `[R-ERR-04]`'s MUST expressly excludes this ground. |
| Does anything address a verifier that **does** implement the declared foreign major? | `implements` (7 hits: 158, 2322, 3171, 3179, 3180, 4388, 4440), `a major it` (1 hit, 791), `does not implement` (17 hits, all read) | Nothing. `[R-CNT-07]` and `[R-CNF-11]` are both phrased reader-relatively ("a major it does not implement"); §2.3 line 141 says conformance "is always conformance to a stated format major version". A verifier that implements major 2 is verifying against major 2's text, which this document does not have. Out of scope by construction, and the document never says so. |
| Does anything say what `[R-CNF-11]`'s "MUST report each requirement it was unable to check, naming the requirement and the ground" (lines 213–215) amounts to for a foreign-major file? | lines 189–223 read in full; no elaboration elsewhere (`unable to check` appears at 195, 210, 213, 3680, 4494) | Nothing. On a foreign-major file the set is *every major-1 file-level requirement*, and the document gives no bulk form for that report. Undecided. |

---

## 4. Summary of what is decided vs. owed

**Decided, normatively:**

- Conformance is major-relative; this text defines major 1 (§2.3, 141–142).
- A foreign-major file is neither conforming nor nonconforming under this text (§2.3, 142–145;
  §21.2, 3432–3434).
- Reader outcome: reject-file, MUST (`[R-CNT-07]`, 791).
- Diagnostic: SHOULD be distinct from "not a TARN file" and from "corrupt" (`[R-CNT-07]`, 792–796).
- The refusal is a *capability* refusal, not a byte finding (§2.3 144–145; §21.6 3656–3657;
  `[R-ERR-04]` 3783–3785).
- Declining such a file is not a `[R-CNF-03]` failure (`[R-ERR-04]`, 3782–3785); the reader's
  acceptance duty is scoped to majors it implements (§2.3, 157–158).
- Detection point: at open, in §6.2's order, after magic and trailer CRC, before every other
  trailer gate and before the directory fetch (`[R-CNT-06]` 773–775; §19.1 step 2, 2725–2729).
- What is readable in such a file at all: trailer at F−64, magic, version fields at F−56,
  CRC at F−4 over [F−64, F−4), front block [0,16) — and nothing else (`[R-CNT-24]`, 800–807;
  `[R-CNT-04]`/line 699).
- Never a register row; the registered neighbour is F18, version_major = 0 (§21.6, 3658–3662).
- **Verifier verdict, when no violation is established: *cannot establish*** — named directly
  at `[R-CNF-11]` lines 196–197, with *conforming* barred by line 208 and by §2.3 line 143.

**Owed (searched for, not found):**

- The verdict when a foreign-major file *also* fails one of the four cross-major rows
  F1/F6/F8/F14 — §21.2's "do reach it" and its own "neither conforming nor nonconforming"
  give incompatible answers (D2).
- Whether §21.2's blanket term for the non-reaching rows — "the rows below whose subject is
  that file's *geometry*" (3434–3435) — actually covers all 31 of them. F19 (flags lane), F23
  (inline_length), F27 (metadata member ordering), F34 (record multiplicity) are not
  *geometry* in any ordinary sense. The ordering argument at 3435–3437 is sound for them (the
  version gate precedes every one), but the label the paragraph uses does not describe them.
- Whether the corpus manifest's binary conformance field can express such a file (§24, 4038).
- Updater/compactor behaviour, stated for the MU = 1 twin (3188) and the incompat-flag twin
  (820–822) but not for this case.
- Recovery-scan behaviour on a foreign-major candidate (§9.6).
- What §9.7's coverage walk and slack total report when the walk cannot start (D5).
- How `[R-CNF-11]`'s per-requirement "unable to check" report is to be given when the set is
  every requirement in the document (213–215).
- Anything at all about a verifier that *does* implement the declared major.
- A keyword-bearing writer rule fixing version_major = 1 (derivable, D3, but never stated).
