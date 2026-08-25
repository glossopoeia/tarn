# Five findings recovered from a walk whose structured return was lost

These are the complete findings of one implementer walk in cleanroom round 25.
The walk completed and wrote this transcript; its structured return failed and
the findings never reached the round's triage passes. They are reproduced here
verbatim, exactly as the walk wrote them, including its own byte-level grades.

**The walk's own grades are not evidence.** Every other finding in this round
was judged by three independent passes; these five were judged by none. Your
job is to supply that judgement.

---

### verifier-01 — AMBIGUITY

**Where.** §5.2 `[R-CNT-21]`; §9.7 `[R-LIF-08]`.

**Quoted.**

> "Where the walk of §9.7 does not enumerate every region's claimants —
> whether because a scope-level rejection ends that scope's enumeration (a
> rejected layer's claimants are not enumerated, whether or not the
> rejection impeded reading them — and where the rejection is one the walk
> itself established, L18's overlap or L40 through L42's placement among
> them, the claimants it had already enumerated are discarded with the
> layer, since the total is a claim about a live state one of whose layers
> is not usable), or because the verifier elected under `[R-CNF-11]` to
> stop at the first violation — the verifier MUST report the total as
> partial. A partial total is F less the bytes claimed by the claimants
> the walk did enumerate"

**The problem.** Every clause that says *which claimants survive into a
partial total* is written about a **layer**. Nothing says what survives
when the rejection is at **file** scope. But file-scope rejections that
occur after a live trailer is established are common — F20 (directory CRC),
F33 (cross-scope overlap), F7 (a structure in the pre-trailer gap) — and
§5.2's excusal from reporting a total at all is expressly narrow: it
covers only the case where "§6.2's ordered validation rejects the file
before a live trailer is established". So a total is owed, and the
document does not fix its value.

**Worked instance.** My §3.3 file, F = 576, with the directory's terminal
CRC corrupted (F20, reject-file, detected at open). `[R-ENC-10]` bars
acting on any record field, so nothing past the directory can be
enumerated. Three defensible partial totals:

- **A.** Front block (16), directory (109) and trailer (64) were
  enumerated before the failure — §9.7 enumerates claimants and *then*
  checks "that each verifies against the checksum covering it" — so
  partial = 576 − 189 = **387**.
- **B.** A file-scope rejection ends the file's enumeration exactly as a
  layer-scope one ends a layer's, and by the stated rationale ("the total
  is a claim about a live state one of whose layers is not usable" — here
  the whole live state is unusable) everything is discarded, so
  partial = **576**.
- **C.** Only the claimant whose checksum failed is discarded, front and
  trailer standing, so partial = 576 − 80 = **496**.

A second instance separates the readings differently: variant B of §4.1
(a stored tile at [360, 460) inside the directory, F33). Here the walk
*did* enumerate every claimant — overlap detection requires that — so
"tightening to the exact total when the walk completes" argues the total is
**exact**, 576 − |union| = 576 − 401 = **175**; while "a scope-level
rejection ends that scope's enumeration" argues it is partial, and B gives
576. So the readings differ not only in value but in the *label* the
verifier attaches, which is itself normative ("It is not the file's slack
total but a bound on it").

**Which I picked.** A, and *partial*. Rationale: §9.7's ordering makes
enumeration precede checksum verification, so the claimants reached were
enumerated; the discard clause is written for layers and I declined to
extend a rule the document scoped; and labelling it partial is the safe
side of "an upper bound on the file's true slack, never an under-count".
I also report which row stopped the walk, which `[R-CNT-21]` requires.

**Cost to an implementer without this.** Two conforming verifiers hand an
operator different slack figures for the same file — 387 versus 576 versus
496 — and one of them says "exact" where the other says "partial". §22.3
makes that number a security-relevant signal ("the number that
distinguishes a working file from a padded one"), and §20.3's note makes
it the compaction trigger. A number two tools disagree about by a factor of
1.5 is not a signal.

**Byte-level?** No. It changes a reported diagnostic quantity and its
label. Both verifiers report *nonconforming*, both readers reject the
file, and no writer's output changes.

---

### verifier-02 — OBSERVATION

**Where.** §21.2, opening paragraph; §5.1 `[R-CNT-27]`; §2.3 `[R-CNF-02]`.

**Quoted.**

> "A file declaring a format major other than 1 is neither conforming nor
> nonconforming under this text (§2.3, `[R-CNF-02]`), and the rows below
> whose subject is that file's *geometry* do not reach it: §6.2 puts the
> version gate ahead of every check but the trailer magic and the trailer
> CRC, so such a file is refused on capability grounds first."

and, from §5.1:

> "A reader MUST treat a shorter file as a validity error at file scope.
> `[R-CNT-27]`"

**The problem.** The justification offered — that the version gate comes
ahead of everything but the magic and the CRC — is not true of
`[R-CNT-27]`. §6.2's ordered list is "the trailer magic; the trailer CRC;
the version gate … and then, those gates passed, … the flag gates;
committed_file_length equals the file size …". The 128-byte minimum is not
in that list; it lives in §5.1, it is decidable from F alone with no
trailer at all, and §19.2 expressly licenses earlier detection ("A reader
MAY detect any violation earlier"). §21.2 handles the parallel case
correctly for F6 by citing `[R-CNT-04]`'s "before other processing" — and
then does not apply the same test to F5.

**Constructible instance.** A 96-byte file: a correct 16-byte front block,
a trailer at [32, 96) with correct magic and correct CRC, and
`version_major = 7`. Verifier A checks `[R-CNT-27]` at open (it is F5's
Detected tier), establishes a registered violation, and by §2.3's "An
established violation takes priority" reports **nonconforming**. Verifier B
follows §6.2's order, fails the version gate, and reports **cannot
establish**.

**Which I picked.** Cannot establish. `[R-CNF-02]` settles it independently
of check order — "a file declaring another major is neither conforming nor
nonconforming under it" makes the *nonconforming* verdict unavailable
whatever the verifier noticed — and §21.2's actual criterion ("their
subject is a field fixed across every major") gives the same answer, since
the 128-byte floor derives from `dir_offset ≥ 16`, `dir_length ≥ 4` and
64-alignment, all of which live in the 48 trailer bytes `[R-CNT-24]` lets a
future major redefine.

**Cost to an implementer without this.** They must reconstruct a
three-passage argument to place one check in the order, and the passage
that looks like it is telling them the answer tells them a false thing.
Reading §21.2's stated reason literally and applying it to F5 yields the
wrong verdict. It is decidable — hence OBSERVATION rather than AMBIGUITY —
but expensive to decide.

**Byte-level?** No. The reader-level outcome is reject-file under either
reading, so no byte sequence changes hands differently; only the verifier's
verdict label and the diagnostic (§6.3's SHOULD asks it to be distinct from
"corrupt") are at stake, and `[R-CNF-02]` decides even that.

---

### verifier-03 — OBSERVATION

**Where.** §8.1 `[R-CNT-19]`; §22.3 `[R-SEC-04]`; §18.2 `[R-MTA-10]`.

**Quoted.** §8.1's map row:

> "| Extent of a record of a type this specification has not assigned |
> none — the bytes are opaque (§7.2) | — |"

and §22.3, treating it and the metadata case as one residue class:

> "The extent of a record of a type this specification has not assigned is
> covered by no checksum either (§8.1), so corruption inside it is equally
> invisible … And the extent of a user-metadata record under an unassigned
> encoding is covered by its terminal CRC but constrained by no content
> rule (`[R-MTA-10]`): the CRC detects corruption and authenticates
> nothing (§4.5), so a certificate covers those bytes uninspected — which
> is why `[R-MTA-10]` makes the verifier's report name each such record,
> and an operator who wants no such bytes rejects on that report line, a
> policy above conformance."

**The problem.** §22.3 puts both extents in the same residue class and
gives the same reason — a certificate covers bytes nobody inspected — but
only one of them carries a reporting obligation. `[R-MTA-10]` says the
verifier "MUST report each record it ignored on this ground, naming the
owning scope, the encoding value, and the stored extent length … bytes a
certificate covers without inspecting are counted and named, never
silent." No rule anywhere says the same of the extent of a record of an
unassigned type — and that one is *worse*, being covered by no checksum at
all, so its corruption is invisible to reader and verifier alike, exactly
as slack's is.

An experimental-range MU = 0 record is a **conforming** file's furniture
(§21.6's row), so this is not an edge case reachable only through
violations: a verifier certifies such a file, and the certificate silently
covers an arbitrary, unchecksummed, unconstrained extent.

**Which I picked.** I report it: owning scope, record type value, extent
offset and length, and the fact that no checksum covers it. §22.3's
"policy above conformance" sentence describes the operator control that
`[R-MTA-10]` creates, and an operator who wants that control needs the
same line for both classes. But I am supplying the obligation, not reading
it.

**Cost to an implementer without this.** Two verifiers' certificates
differ in what they disclose about the same conforming file. One names the
uninspected bytes and one does not, and the operator policy §22.3
describes — "rejects on that report line" — works against unassigned
*encodings* and silently fails against unassigned *types*.

**Byte-level?** No. Report content on a file both verifiers certify.

---

### verifier-04 — OBSERVATION

**Where.** §17.4 `[R-COD-11]`; §2.3 `[R-CNF-11]`; §21.3 L43, L45.

**Quoted.** §17.4, second and fourth sentences:

> "A verifier that cannot execute a layer's codec or filter cannot
> establish that layer's conformance and MUST NOT certify the file. That
> inability is not a finding that the file is nonconforming, and it fixes
> the file's verdict as *cannot establish* only where the verifier
> established no violation elsewhere (`[R-CNF-11]`). For a conforming
> reader that position arises only at a reserved or experimental value,
> every assigned codec and filter being core: it rejects the layer
> (`[R-COD-03]`, `[R-COD-09]`); software unable to execute an assigned
> codec or filter is not a conforming reader (`[R-CNF-03]`)."

and §2.3's ground list, which cites it:

> "when it cannot execute a codec or filter (`[R-COD-11]`)"

**The problem.** Put the two halves side by side, which is what the
brief's "argument by analogy" test asks. Codecs 1–4 and filters 1–2 are all
core, and `[R-CNF-03]` makes software that cannot execute one **not a
conforming reader**, hence not a conforming verifier (§2.3: "Verifiers and
updaters are readers of the files they process and inherit every reader
obligation"). So the only value at which a *conforming* verifier meets a
codec it cannot execute is a reserved or experimental one — and that value
is itself a violation (L43 for codec, L45 for filter, `[R-COD-03]` /
`[R-COD-09]`, reject-layer, detector reader). §2.3 then forces
**nonconforming**, because "An established violation takes priority".

The cannot-establish branch of `[R-COD-11]`'s second sentence is therefore
unreachable by any conforming verifier, and §2.3 lists it as a live ground
beside four that are reachable. §17.4's fourth sentence is what closes it,
and it reads as an aside rather than as the sentence that empties the
second.

**Which I picked.** A reserved or experimental codec/filter value yields
**nonconforming**, not cannot-establish; I implemented no
codec-capability cannot-establish path at all. The reachable
codec-adjacent cannot-establish ground is the *resource* one — §17.2's
"a wider window is conforming and merely permits a conforming reader to
decline the tile or the layer on resource grounds (`[R-ERR-04]`)" — which
is a different rule with a different citation.

**Cost to an implementer without this.** An implementer who reads §2.3's
ground list and §17.4's second sentence, and stops there, reports *cannot
establish* for a file carrying codec 7. That file is nonconforming and the
verifier must say so. It is a verdict error on a constructible file,
reachable by a plausible reading path, and it is fixed only by the fourth
sentence of the same paragraph.

**Byte-level?** No — the text does decide it, and the reader outcome
(reject-layer) is the same either way. But the verdict divergence is real
for a careless implementation, which is why I report it rather than
letting the dead branch pass.

---

### verifier-05 — OBSERVATION

**Where.** §21.7 `[R-ERR-01]`, second paragraph; §21.1's completeness
clause.

**Quoted.**

> "A second set of obligations is omitted from the register because a
> single file exhibits no witness of their violation. Committed-prefix
> immutability and the generation sequence (`[R-LIF-01]`, `[R-LIF-03]`)
> are properties of a file's history, which §9.7 does not reconstruct; the
> ordinal mappings of `[R-GEO-06]` and `[R-SER-01]` … ; `[R-CNT-13]`'s
> prohibition on an MU = 0 record encoding file offsets in its own payload
> is opaque by construction; `[R-CNT-18]`'s prohibition on a sub-record
> containing records … ; §20.3 step 4's bar on a declaration change … ;
> §20.5's four obligations on a compacted file's trailer … ; and
> `[R-ENC-06]`'s fixed field widths are not a state a file can be in"

**The problem.** This is an enumeration with a closing "and", and §21.1
leans on it: "Its **completeness is normative** — a *detectable*
file-conformance violation this specification names and the register omits
is a defect in this document, detectability being the gate `[R-CNF-07]`
already applies **and §21.7 the account, by class, of what fails it**."
So §21.7 is the document's own inventory of what falls outside the
register, and a reader auditing the register's completeness works the list
backwards: anything not here should be detectable and should have a row.

I derived the members from the rule the list is about — writer obligations
this specification states whose violation a single file cannot witness —
and found at least four that are not named:

- **`[R-LIF-02]` steps 4 and 6, the durability barriers.** No file
  exhibits whether `fdatasync` was called. §20.2 and §20.5 both stress
  them ("both barriers, not one"), and §9.2's own Note concedes only that
  weak barriers degrade detection, not that a missing barrier leaves a
  witness.
- **`[R-WRT-05]`'s byte-identical re-emission.** Detecting a re-encoded
  record requires the prior generation's directory, which §9.7 does not
  reconstruct. Its Rationale even says "byte-identity makes preservation
  testable — the records of adjacent generations differ exactly by those
  modified, added, or dropped" — *adjacent generations*, i.e. two files.
- **`[R-WRT-08]`'s bar on re-encoding an unimplemented record type**, for
  the same reason.
- **§20.4's drop rules** ("An appender MUST NOT drop it except in a commit
  that *independently* changes the scope the record attaches to"), which
  compare two generations' record multisets.

All four fall inside the *class* the paragraph names, so a reader who
treats "by class" as governing is fine. A reader who treats the
enumeration as closed — which the closing "and" invites, and which §21.1's
normative completeness makes worth doing — concludes these four must be
detectable, looks for their rows, finds none, and reports a register
defect that is not one.

**Which I picked.** The class governs; the enumeration is illustrative. I
implemented no checks for any of the four and reported nothing about them,
consistent with §21.7's "nothing about the file is left undetermined and
the verdict is unaffected".

**Cost to an implementer without this.** Wasted audit effort, and a
spurious defect report against §21.1's completeness claim. No verdict
changes.

**Byte-level?** No. Nothing here reaches bytes, verdicts, or the register's
rows; it reaches whether an implementer trusts the register's completeness
clause.

---

