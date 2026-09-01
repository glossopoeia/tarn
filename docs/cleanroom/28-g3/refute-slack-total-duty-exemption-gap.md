# Refute-only verification: [R-CNT-21] duty/exemption gap (§5.2 vs §9.7)

## Disclosure

Read exactly one file: `/Users/robertkleffner/Documents/GitHub/tarn-first-draft/spec/tarn.md`,
via `sed -n` and `grep -n` through the Bash tool. No other file was opened, no
directory listed, no git command, no web access. Local computation: none needed
beyond arithmetic done in-head (recorded below). Scratch dir created at
.../r28-refute/priv-slack-total-duty-exemption-gap/ but no scratch file was
required.

Unrequested context appeared in my prompt before I began: a project-instruction
block, a user-identity/date block, and an environment block naming the repository,
branch and recent commit subject lines. I disregarded all of it as evidence and do
not repeat its contents. It played no part in the verdict.

## Passages opened

- §2.1 [R-CNF-01] (normative-language / non-normative labels), lines ~96-106
- §2.3 [R-CNF-02] (file conformance is a predicate on bytes; conduct rules bind the
  actor, not the bytes), lines ~160-175
- §2.3 [R-CNF-03]/[R-CNF-04] (reader duties), [R-CNF-05] (writer emits only
  conforming files), [R-CNF-06], [R-CNF-11] (three verdicts; established violation
  takes priority; per-requirement reports constrain the report and not the verdict),
  lines ~176-242
- §2.4 [R-CNF-12] (SHOULD deviation is not a violation; register is MUST-level only),
  lines ~310-325
- §5.1 commit/slack figure, lines ~629-680
- §5.2 [R-CNT-02], [R-CNT-21], [R-CNT-03] and both Notes, lines 686-755 (the disputed text)
- §6.2 [R-CNT-05], [R-CNT-06] (trailer layout, ordered validation, pre-trailer pad),
  lines 800-845
- §6.3 [R-CNT-07], [R-CNT-24], flag lanes, lines 846-880
- §9.7 [R-LIF-08] + its Note (coverage walk; partial totals), lines 1440-1490
- §15.3 [R-IDX-03] (structural reject-tile entries fall to slack), lines 2158-2180
- §16 [R-SLB-05], §16.1 alignment slack, lines 2240-2262
- §18.2 [R-MTA-05], [R-MTA-10] ("as it reports the slack total"), lines ~90-130 of
  that section (file lines 2690-2740)
- §18.4 [R-MTA-07], [R-MTA-08] (standardized keys — checked for a slack key), lines 2756-2805
- §20.3 step 4 / [R-WRT-04] (shrink, de-addressed extents become slack), lines 3160-3210
- §20.4 record-drop table row (MU=0, PE=0), line 3306
- §20.5 [R-WRT-09] + compaction Notes, lines 3341-3484
- §21.1 [R-ERR-02] preamble (how to read the register; detector/detection columns),
  lines 3485-3570
- §21.2 file-scope rows: F17, F18, F19, **F20**, F21-F23, F25-F28, **F29**, F30-F33, F36
- §21.5 R1-R10 (checked for a report-duty row), lines 3700-3740
- §21.6 Conditions that are not violations — including the slack row, line 3763 —
  and the two "conforming files a reader nevertheless refuses", lines 3745-3800
- §21.7 [R-ERR-01] (obligations omitted from the register for want of a witness),
  lines 3805-3878
- §21.8 vector coverage, line 3880
- §22.2 [R-SEC-02], §22.3 [R-SEC-03] + [R-SEC-04] residues, lines 3995-4048
- §23.1 deletion-is-not-erasure, lines 4085-4110
- Appendix (conforming-actor summary) definitions of conforming reader/writer/updater/
  verifier, lines 4595-4648
- Appendix worked byte map, line 4278 (F=128 file: pad [20,64) = 44 bytes of slack)

## What the two readings actually are

Disputed sentence pair, §5.2 [R-CNT-21], lines 699-706:

> "A reader MUST NOT interpret it (§9.5); a verifier that reaches a live state MUST
> report the total number of slack bytes, since that number is what tells an operator
> to compact. Where §6.2's ordered validation rejects the file before a live trailer
> is established there is no F and no live state to walk, so the total is not owed at
> all: the verifier reports the trailer failure and nothing about slack, which is not
> a partial total but the absence of one."

The reporter's gap: F20 (directory-region CRC mismatch) and F29 (record-sequence
framing failure) sit after a validated trailer, so the exemption's antecedent is
false; and (on the reporter's premise) no live state is "reached", so the duty's
antecedent is false too. Reading (1): nothing about slack is reported. Reading (2):
a partial total is owed under the third clause.

The wording asymmetry is real. §9.7 [R-LIF-08] closes it from the other side —
"Where the walk does not complete — a scope-level rejection blocks enumeration, or
the verifier stops at the first violation (`[R-CNF-11]`) — the sum is reported as
partial" — and §5.2's own definition of the live committed state ends
"together with the live directory and the live trailer", unconditionally. But
whether the cross-read succeeds is not what I was asked. I was asked whether the
fork moves bytes.

## Construction attempts

### A. The reporter's own case, made concrete (F20)

Take the appendix's worked file and corrupt one field. F = 128.

    [0, 16)    front signature block
    [16, 20)   directory region, dir_length = 4 (empty directory, CRC only)
    [20, 64)   pre-trailer pad, 44 bytes
    [64, 128)  trailer; committed_file_length = 128, dir_offset = 16, dir_length = 4

Now flip one bit in the 4 directory-CRC bytes at [16, 20). Every §6.2 gate still
passes: trailer magic, trailer CRC, version gate, flag gates,
committed_file_length = 128 = file size and 128 mod 64 = 0, dir_offset 16 >= 16,
dir_length 4 >= 4, 16 + 4 = 20 <= 128 - 64 = 64, file_id != 0, reserved zero.
So a live trailer *is* established and the exemption does not fire. F20 fires.

Verifier V1 (reading 1) reports: verdict *nonconforming*, ground F20/[R-CNT-11],
nothing about slack.
Verifier V2 (reading 2) reports: verdict *nonconforming*, ground F20/[R-CNT-11],
plus a partial slack total naming the directory CRC as what stopped the walk:
F less the enumerated claimants = 128 - (16 + 64 + 4) = 44, or 128 - (16 + 64) = 48
if the CRC-failed directory region is held not to have been enumerated. (That
128-vs-44-vs-48 sub-ambiguity lives entirely inside reading (2) and is another
report-line divergence, not a byte one.)

Verdicts: identical. Bytes of the file: identical — the file is a fixed byte string
in both hands. Emittable set: F20 is a register row, so [R-CNF-05] ("A writer MUST
emit only conforming files") bars every conforming writer from producing this file
under *both* readings. This is exactly the shape the brief names as not byte-level:
the disputed file is itself nonconforming, so the emittable set does not move.

Killed by: §21.2's heading "Outcome: reject-file" over the row F20, together with
[R-CNF-11] — "An established violation takes priority: a verifier that has
established any violation reports *nonconforming*, however many requirements it was
unable to check."

### B. F29 instead of F20 (framing failure rather than checksum)

F29: "A top-level record's 24-byte header or its inline payload extends past the end
of the directory's record sequence (dir_offset + dir_length - 4), or bytes remain
after the last complete record"; detector reader, detected at open, governing rule
[R-CNT-12]. Same file-scope row, same reject-file outcome. Identical to A.

Killed by: the same two sentences.

### C. The reporter's second case — F33 overlap between two non-layer structures

F33 is detector *verifier*, detected at *certification*, file scope. Here the walk
itself establishes the violation. Both readings agree the duty triggers (trailer
and directory both parse, so a live state is reached on anybody's reading), and
§5.2's third clause covers the incomplete enumeration. Even granting the reporter's
premise that "no usable live state" results, [R-CNT-02] settles the verdict without
reference to the report: "a file whose live state does not partition this way is not
a conforming file."

Killed by: [R-CNT-02]'s final clause.

### D. Compaction path rather than append path

If the disputed reading changed a compactor's obligations, it would move emitted
bytes. It does not. [R-WRT-09] fixes a compactor's verification depth by *reliance*:
"it relies structurally on every structure it copies, so it MUST verify each link of
the chain — the open (§19.1), each retained layer's record (§19.3) and full index
chain (`[R-IDX-04]`), and each relocated extent's checksum, including every stored
tile's entry crc — before emitting that structure's bytes." No slack total appears in
that list. And on an F20/F29 input the compactor, being a reader, must reject-file at
open under both readings and emits nothing at all. The only slack-facing statement on
this path is §20.5's Note that the total "is what tells an operator when to run this"
— an operator's decision, and a Note, which [R-CNF-01] makes non-normative.

Killed by: [R-WRT-09]'s enumerated chain, which omits the total.

### E. Degenerate file — zero layers, empty directory, minimum length

F = 128 as in A but with a correct directory CRC. §21.6: "The file contains zero
layers | A conforming file with an empty directory | `[R-CNT-14]` (R-CNT-02)". The
walk completes trivially; the total is exact (44); the duty's trigger is satisfied on
every reading and the exemption is inert. No fork.

Killed by: §9.7's walk completing, which puts the case outside both disputed clauses.

### F. Shrink / dropped-record path (bytes de-addressed rather than modified)

§20.3 step 4: "Where a shrink is permitted the de-addressed tiles' extents become
slack (`[R-CNT-21]`)". §20.4's MU=0/PE=0 row: an appender may drop the record, "its
extent becoming slack". In both, slack is a *consequence* of what the writer emitted,
never an input to it, and the resulting file's walk completes, so the total is exact.
I looked specifically for a writer duty keyed to a slack quantity and found only
[R-CNT-03], a SHOULD ("Writers SHOULD zero the gaps they create"), which [R-CNF-12]
places outside the register, and [R-CNT-05]'s over-long pre-trailer gap, which
[R-CNF-02] expressly names as one of the two writer obligations whose violation is
*not* a file-conformance violation.

Killed by: [R-CNT-21] itself — "no conformance requirement applies to it".

### G. A conforming file the verifier refuses — experimental top-level type, MU = 1

§21.6 makes this "a conforming file a reader nevertheless refuses": [R-CNT-15]
obliges rejection, [R-CNF-02] keeps the file conforming. Verdict is *cannot
establish* on either reading ([R-CNF-11] lists the MU=1 unimplemented type as such a
ground and forbids certifying), and a live trailer plus a parsed directory means the
exemption never fires. I chose this case because it is the one place where a
*conforming* file meets an incomplete walk — the shape the brief says moves the set.
It still does not: the file's conformance is fixed by its bytes, and only a report
line varies.

Killed by: [R-CNF-02] — "conduct rules bind the actor, the predicate binds the bytes."

### H. Is the verifier's report itself governed bytes anywhere?

Searched for a certificate/report byte format and for a standardized user-metadata
key carrying a slack figure. §18.4 registers six keys — `tarn.title`,
`tarn.description`, `tarn.created`, `tarn.creator`, `tarn.axes`, `tarn.stats` — and
none of them is a slack count; all six are OPTIONAL and advisory, and [R-MTA-07]
says "Neither placement nor value shape bears on validity". "Certificate" appears
only figuratively ([R-MTA-10], [R-SEC-04]). No report format is specified in bytes.

Killed by: §18.4's closed list and [R-MTA-02]'s bar on metadata affecting decoding.

### I. Is there a register row a missing or extra slack line could fire?

§21.1: the register "enumerates every detectable file-conformance *violation* this
specification names", and "Its **completeness is normative**". Slack appears in
§21.6, the table of "Conditions that are **not** violations": "Bytes the live state
does not claim ... | Slack: unconstrained content, no conformance requirement,
counted and reported by a verifier — as a partial total — an upper bound naming what
stopped the walk — where its walk did not complete". And §21.7 [R-ERR-01] catalogues
what is omitted from the register for want of a witness; the verifier's report duties
are not there because they were never candidates — they bind the actor.

Killed by: §21.6's row, which classifies slack as a non-violation.

### J. Does the phrase's ambiguity leak into a byte-binding rule elsewhere?

Checked every occurrence of "live state" (lines 692, 695, 700, 703, 713, 736, 737,
747, 752, 1442, 3183, 3606, 3610, 3645, 3763, 4095, 4104, 4379). The only *rule
trigger* forms are [R-CNT-02]'s partition (unconditional, and its definition of the
live committed state expressly includes the directory and trailer), F33's and L18's
overlap rows, and the disputed [R-CNT-21] sentence. §22.3's [R-SEC-03] cites the
total but its operative clause is a SHOULD ("a pipeline ... SHOULD verify rather than
merely read"). §22.3's [R-SEC-04] volunteers the point outright: corruption confined
to slack "is caught only by the slack total changing (§9.7) — which is why a writer
that zeroes its gaps (`[R-CNT-03]`) makes its own files easier to reason about, **not
because conformance turns on it**."

Killed by: [R-SEC-04]'s own closing clause.

## Verdict

NOT_BYTE_LEVEL. Every construction terminates in the same place: the object the two
readings disagree about is a line in a verifier's report, and this document has three
independent sentences saying a report line is not a fact about bytes —
[R-CNF-02] ("file conformance — a pure predicate on bytes"; conduct binds the actor),
[R-CNF-11] ("that per-requirement report constrains the report and not the verdict"),
and §5.2's own Note ("A partial total (`[R-CNT-21]`) reports what one verifier's
incomplete walk left unclaimed, which is a fact about that run and not about the
file's live state"). The disputed files (F20, F29, F33) each carry a register-row
violation, so [R-CNF-05] bars every conforming writer from emitting them under both
readings, and [R-CNF-11] fixes *nonconforming* under both. The defect is real and
editorial-to-design; it does not fork the emittable set or any accept/reject verdict.
