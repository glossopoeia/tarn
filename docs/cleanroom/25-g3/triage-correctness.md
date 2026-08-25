# Triage pass — correctness lens — five recovered verifier findings, round 25

## Access log
Read exactly two files: the recovered findings at the path the brief named
(present exactly there), and /Users/robertkleffner/Documents/GitHub/tarn/spec/tarn.md.
All spec access via `sed -n` / `grep -n` on that one path. No docs/, no
conformance/, no registry.json, no git, no web.

Context material that appeared unbidden: a project-instruction file whose body is
a pointer to another file, an index of the maintainer's memory notes with titles,
the user's email, the date. None consulted for substance; noted in disclosure.

---

## verifier-01 — partial slack total at file scope

Passages read: §5.2 [R-CNT-02]/[R-CNT-21]/[R-CNT-03] + both Notes; §9.7
[R-LIF-08] + Note; §6.2 [R-CNT-05]/[R-CNT-06]; §7.1 [R-CNT-11]; §4.5
[R-ENC-10]; §19.1 steps 1-4; §21.2 rows F7, F20, F33; §21.6 slack row; §22.3
[R-SEC-03]/[R-SEC-04].

The reporter's factual premises check out:
- The layer carve-out is genuinely layer-scoped. Its text: "a rejected layer's
  claimants are not enumerated ... the claimants it had already enumerated are
  discarded with the layer, since the total is a claim about a live state one of
  whose layers is not usable". Subject: layer, throughout.
- F20 does not fall under §5.2's excusal. That excusal is "Where §6.2's ordered
  validation rejects the file before a live trailer is established". The
  directory CRC is §19.1 step 3, after a validated trailer. So a total is owed.

Where the reporter overreaches: the document *does* fix the value, by a general
definitional sentence that is not scoped to layers — "A partial total is F less
the bytes claimed by the claimants the walk did enumerate". §9.7 orders
enumeration before checksum verification ("reaches the claimants ... It checks
that these occupy disjoint byte ranges, that each lies within [16, F-64), and
that each verifies against the checksum covering it"), so front block, directory
and trailer are enumerated claimants in the F20 instance. Reading A (387) is what
the text says. Reading B requires importing the layer discard clause to file
scope by analogy — the very extension the reporter itself declines. Reading C
("only the failing claimant is discarded") has no textual hook at all.

Nor does the second instance divide. Partiality's trigger is "Where the walk of
§9.7 does not enumerate every region's claimants"; the F33 variant enumerates
every claimant (overlap detection requires it), so the label is *exact*, and
§9.7's restatement agrees: partial applies where "a scope-level rejection blocks
enumeration, or the verifier stops at the first violation". A rejection
established *after* full enumeration blocked nothing.

Note also that the reporter's own guardrail does not discriminate: 576 and 387
are both upper bounds and neither under-counts, so "never an under-count" cannot
be used to pick A over B. The definitional sentence is what picks A.

Verdict: PARTIAL. Real gap: no explicit file-scope sentence, so the analogy is
available to a careless reader. Not real: "the document does not fix its value".
Severity editorial; a one-clause addition to [R-CNT-21] ("a file-scope rejection
discards nothing already enumerated") closes it.

Byte-level: no. §5.2 — "no conformance requirement applies to it". The F20 file
is reject-file under every reading; the F33 variant is nonconforming under every
reading; [R-CNF-05] bars emission of both. What moves is a reported number and a
label, and no reader's accept/reject follows it.

---

## verifier-02 — §21.2's stated reason does not cover F5

Passages read: §21.2 opening paragraph and rows F5, F6, F1, F8, F13, F14, F18;
§5.1 [R-CNT-27]; §6.2 [R-CNT-06] ordering clause; §6.3 [R-CNT-07]/[R-CNT-24];
§19.1 step 1; §19.2 [R-RDR-02]; §2.3 [R-CNF-02]/[R-CNF-11]; §21.6 closing
paragraphs.

Confirmed. §6.2's ordered list is closed and enumerated: "the trailer magic; the
trailer CRC; the version gate (§6.3) ... and then, those gates passed, MUST
validate all of the following ... the flag gates; committed_file_length equals
the file size ... and is a multiple of 64; dir_offset >= 16; dir_length >= 4;
dir_offset + dir_length <= F - 64; 1 <= generation <= 2^63 - 1; file_id != 0;
reserved bytes zero." The 128-byte minimum is not in it. It lives in §5.1, and
§19.1 step 1 obtains F before the trailer is fetched, so F5's "F (physical file
size)" instance is establishable before the version gate is ever reached. So
§21.2's "§6.2 puts the version gate ahead of every check but the trailer magic
and the trailer CRC" is an overstatement — it is ahead of every check §6.2
lists.

Refinement the reporter did not make: F5 has two instances, "F (physical file
size); committed_file_length". The stated reason does hold for the
committed_file_length instance (a trailer field, gated by §6.2's order) and fails
only for the physical-size instance. The defect is therefore half of one row, not
a whole one.

The correct outcome is nonetheless the reporter's. [R-CNF-02]: "a file declaring
another major is neither conforming nor nonconforming under it" — the
*nonconforming* verdict is unavailable whatever the verifier noticed first, so
§2.3's "An established violation takes priority" has no violation to prioritise.
And §21.2's own exception criterion ("their subject is a field fixed across every
major") independently excludes F5, since dir_offset >= 16, dir_length >= 4 and
the 64-alignment all sit in the 48 trailer bytes [R-CNT-24] lets a future major
redefine. Two independent routes to *cannot establish*; only the ordering
rationale is loose.

Verdict: CONFIRMED, severity editorial. Fix: in §21.2, replace the ordering
clause with the fixed-across-majors criterion the same paragraph already states,
or add "and [R-CNT-27], though decidable from F alone, has a major-1 subject".

Byte-level: no. §2.3 — "a verifier MUST NOT certify a file it reports that way"
holds for cannot-establish, and the file is refused reject-file under
[R-CNT-07] either way. No conforming writer under this text emits version_major
= 7 at all (§6.2's Valid values cell: "1 (0 invalid; others: §6.3)"). Emittable
set fixed.

---

## verifier-03 — no reporting obligation for an unassigned-type record's extent

Passages read: §8.1 [R-CNT-19] and its map row; §4.5 [R-ENC-10]'s parallel
sentence; §7.2 [R-CNT-12]/[R-CNT-13]/[R-CNT-15]; §7.3; §18.2 [R-MTA-10];
§21.5 preamble; §21.6 experimental-type row and experimental-encoding row;
§20.4 [R-WRT-05]/[R-WRT-08]; §22.3 [R-SEC-03]/[R-SEC-04]; grep for every
"MUST report"/"SHOULD report" in the document.

The narrow factual claim survives: grep finds no rule obliging any actor to
report the extent of a record of an unassigned type. [R-MTA-10] alone carries
"MUST report each record it ignored on this ground, naming the owning scope, the
encoding value, and the stored extent length". §21.5's "Readers SHOULD report the
loss" is scoped to user-metadata rows. §21.6's experimental-type row says only
"Ignored, and preserved or dropped per its PE bit". And such a file is indeed
conforming.

The characterisation does not survive. §22.3 states **four** residues, not one
class of two, and it does not give the two extents the same reason. The
unassigned-type extent is likened to *slack*: "covered by no checksum either
(§8.1), so corruption inside it is equally invisible", defended by "[R-WRT-05]
carries such an extent forward unread, and [R-WRT-08] bars re-encoding it, so
nothing an updater does would surface the damage" — a why-it-is-harmless
argument, with no reporting claim attached. The certificate-covers-uninspected-
bytes reason belongs to the metadata residue only, and §22.3 immediately ties it
to the rule that creates the obligation. So the alleged internal inconsistency —
same class, same reason, different obligation — is not in the text.

Two further corrections. The extent is not wholly uninspected: §5.2 makes it a
claimant ("a record extent (the bytes any record's extent slot references,
whatever the record's type, §7.2)"), so §9.7 checks its disjointness, its bounds,
and counts it as claimed rather than slack. And the reporter concedes the point:
"I am supplying the obligation, not reading it."

Verdict: PARTIAL. The asymmetry is real and arguably worth closing; the defect as
*described* (a stated equivalence the document then breaks) is a misreading.
Severity design-decision — adding a report line is a new normative obligation on
verifiers, an ADR call, not an editorial correction.

Byte-level: no. §22.3 itself: "an operator who wants no such bytes rejects on
that report line, **a policy above conformance**". Both verifiers certify the
same file; report content only.

---

## verifier-04 — [R-COD-11]'s cannot-establish branch is dead for a conforming verifier

Passages read: §17.4 [R-COD-11] in full; §17.2 [R-COD-03]; §17.3 [R-COD-09];
§2.3 [R-CNF-03]/[R-CNF-11] ground list; §21.3 rows L43, L45; §2.4 [R-CNF-12];
§21.9 reference to [R-ERR-04].

Confirmed on every link. Codecs 1-4 and filters 1-2 are core ("all four are
**core** — a conforming reader MUST implement every one of them"; "both are
**core**"). §2.3 makes verifiers readers: "Verifiers and updaters are readers of
the files they process and inherit every reader obligation." §17.4 itself closes
the branch: "For a conforming reader that position arises only at a reserved or
experimental value ... it rejects the layer ([R-COD-03], [R-COD-09])". L43 and
L45 register exactly those values, detector *reader*, at layer access. So a
violation is established, and §2.3's "An established violation takes priority"
forces *nonconforming*. The ground §2.3 lists as "when it cannot execute a codec
or filter ([R-COD-11])" is unreachable by any conforming verifier.

I checked the escape routes. A later minor assigning codec 5 does not help: under
this text 5-0x7FFF are reserved and [R-COD-03] makes them a layer-scope validity
error regardless. A resource decline is a different rule with a different
citation ([R-ERR-04], [R-SER-05], [R-SER-08]), separately listed in §2.3. The
other four §2.3 grounds are reachable (unimplemented major via [R-CNF-02];
top-level MU = 1 experimental type via §21.6's "conforming files a reader
nevertheless refuses"; resource decline; [R-MTA-09] decline).

Mitigating: §2.3 introduces the list with "as when", and §17.4's third and fourth
sentences state the closure explicitly. The document decides; it just buries the
decision two sentences past the sentence an implementer stops at.

Verdict: CONFIRMED, severity editorial. Fix: mark the ground in §2.3 as
reachable only outside a conforming verifier, or fold §17.4's fourth sentence
forward.

Byte-level: no. §2.3 — "a verifier MUST NOT certify a file it reports that way"
— so *cannot establish* and *nonconforming* both withhold certification, and the
reader outcome is reject-layer under both. The file carries an L43 violation, so
[R-CNF-05] bars every conforming writer from emitting it under either reading.

---

## verifier-05 — §21.7's second paragraph reads as a closed list

Passages read: §21.1 completeness clause; §21.7 both paragraphs in full; §9.2
[R-LIF-02] steps 4 and 6 and the barrier Note; §20.4 [R-WRT-05], the MU = 0 /
PE = 0 drop row, [R-WRT-08]; §18.2's contrasting phrase.

The four named omissions are real and all sit inside the paragraph's stated class
("a single file exhibits no witness of their violation"):
- [R-LIF-02] steps 4 and 6 exist verbatim as durability barriers; no byte
  witnesses them.
- [R-WRT-05]'s "MUST re-emit byte-identically ... every record it retains" needs
  the prior generation, and its Rationale says "the records of adjacent
  generations differ".
- [R-WRT-08]'s bar on re-encoding an unimplemented type, same reason.
- §20.4's drop rule ("An appender MUST NOT drop it except in a commit that
  *independently* changes the scope the record attaches to") compares two
  generations' record multisets.

And the paragraph carries no non-exhaustiveness marker, closing on "and
[R-ENC-06]'s fixed field widths". The document elsewhere knows the move — §18.2
writes "named for convenience, not as a closed list" — which makes its absence
here a real editorial asymmetry.

Against escalation: §21.1 says the account is "by class" in so many words, and
§21.1's completeness clause is scoped to "a *detectable* file-conformance
violation", which none of the four is. So the audit the reporter fears is
answered by the governing sentence, and the reporter resolved it that way itself.

Verdict: CONFIRMED, severity editorial. One clause ("among them" / "not a closed
list") closes it.

Byte-level: no. §21.7 — "nothing about the file is left undetermined and the
verdict is unaffected". No row moves, no verdict moves, no byte moves.

---

## Tally
Byte-level: 0 of 5. Consensus: 3 CONFIRMED (02, 04, 05), 2 PARTIAL (01, 03).
No finding's byte-level grade departs from the reporter's own; two findings'
*descriptions* do not survive (01's "the document does not fix its value",
03's "§22.3 puts both extents in the same residue class and gives the same
reason").
