# Round 25 recovered findings — skeptic triage pass

Access: I read only `/Users/robertkleffner/Documents/GitHub/tarn/spec/tarn.md`
(plus the findings file the brief named). Passages opened, by line range:
94–280 (§2), 362–382 (§3.3, §4.1), 555–700 (§5), 735–830 (§6.2–6.3),
1111–1155 (§8), 1321–1372 (§9.7), 2238–2270 (§17.2), 2399–2420 (§17.4),
2560–2612 (§18.2 `[R-MTA-10]`), 2694–2795 (§19.1–19.2), 3337–3530 (§21.1–21.3),
3562–3660 (§21.5–21.6), 3650–3730 (§21.7–21.8), 3851–3900 (§22.3).
Greps over the same file for `R-MTA-10`, `R-ENC-10`, `MUST report|SHOULD report`,
`^#`. No other file read; no git, no web, no directory listing.

---

## verifier-01 — partial total after a file-scope rejection

**What the reporter claims.** Every clause saying which claimants survive into a
partial total is written about a layer; nothing governs a file-scope rejection;
three defensible values (387 / 576 / 496).

**What the document says.**

1. The general definition is not layer-scoped:
   > "A partial total is F less the bytes claimed by the claimants the walk did
   > enumerate — an upper bound on the file's true slack, never an under-count"

   That sentence fixes the value for *any* partial total. Reading **C** (discard
   only the claimant whose checksum failed) has no warrant at all — the directory
   was enumerated, and nothing licenses un-enumerating one claimant.

2. §9.7 claims the front block and trailer unconditionally, not through the walk
   of the directory:
   > "The front signature block at [0, 16) and the live trailer at [F − 64, F)
   > are claimed by the walk as well, being members of the live committed state"

   That is inconsistent with reading **B** (partial = F, nothing claimed): in the
   F20 instance the trailer has already been validated and F established, so at
   minimum 80 bytes are claimed. B as stated (576) is refuted.

3. §5.2's Note expressly makes a partial total run-dependent:
   > "A partial total (`[R-CNT-21]`) reports what one verifier's incomplete walk
   > left unclaimed, which is a fact about that run and not about the file's live
   > state."

   This defuses the stated cost. Two verifiers reporting different partial
   figures for the same file is the design, not a defect.

4. The label question (exact vs partial) in the F33 instance is decided. §5.2
   triggers *partial* on "the walk of §9.7 does not enumerate every region's
   claimants". Overlap detection requires full enumeration, so the walk
   enumerated everything, and §5.2's own closing clause applies: "tightening to
   the exact total when the walk completes."

**Where the reporter has a real hook.** The clause "a scope-level rejection ends
that scope's enumeration" is glossed only for layers ("a rejected layer's
claimants are not enumerated, whether or not the rejection impeded reading
them"), and the gloss is retroactive while §9.7's phrasing ("a scope-level
rejection *blocks* enumeration") is prospective. Applied to file scope the gloss
would strip already-enumerated claimants. So the wording is loose. But the
loose reading collides with §9.7's unconditional front/trailer claim, and the
general definitional sentence covers the case, so the value is not open in the
way claimed.

**Verdict.** PARTIAL. Real looseness in the discard clause's scope; the claim
that "the document does not fix its value" over-claims, and the operator-facing
cost is licensed by the §5.2 Note. Editorial.

**Byte-level.** No. The F20 instance is a nonconforming file under every reading
(`[R-CNT-11]`, F20, reject-file, reader-detected), so `[R-CNF-05]` bars every
conforming writer from emitting it either way and every reader rejects it either
way. The dispute is over a reported diagnostic quantity that §5.2's Note already
calls a fact about the run.

---

## verifier-02 — §21.2's ordering rationale does not cover F5

**Checked against §6.2.** §6.2's ordered list is exactly:
> "the trailer magic; the trailer CRC; the version gate (§6.3) … and then, those
> gates passed, MUST validate all of the following …: the flag gates (§6.3);
> committed_file_length equals the file size … and is a multiple of 64;
> dir_offset ≥ 16; dir_length ≥ 4; dir_offset + dir_length ≤ F − 64; …"

The 128-byte floor is not in it. It lives in §5.1 `[R-CNT-27]`, its F5 row is
detector *reader*, detected *open*, and §19.1 step 1 obtains F before the trailer
is fetched at all. §19.2 licenses earlier detection: "A reader MAY detect any
violation earlier (`[R-CNF-12]`)." So the reporter is right that §21.2's
colon-clause ("§6.2 puts the version gate ahead of every check but the trailer
magic and the trailer CRC, so such a file is refused on capability grounds
first") does not, on its own terms, dispose of F5. §21.2 already knows this
pattern — it makes F6 an express exception on `[R-CNT-04]`'s "before other
processing" — and does not run the same test on F5.

**But the answer is in the same sentence.** §21.2 opens:
> "A file declaring a format major other than 1 is neither conforming nor
> nonconforming under this text (§2.3, `[R-CNF-02]`)"

and §21.2's actual exception criterion is "their subject is a field fixed across
every major (`[R-CNT-24]`)". `[R-CNT-24]` fixes only the trailer magic,
version_major/minor, the trailing CRC, and the front block; the 128-byte floor
derives from dir_offset, dir_length and 64-alignment, all inside the 48 bytes a
future major MAY redefine. Both routes put F5 with the geometry rows.

**Verdict.** CONFIRMED as an editorial defect: the offered justification is
inaccurate as applied to F5, and the paragraph applies the correct test to F6 but
not to F5. The reporter's "yields the wrong verdict" framing over-states the
cost — `[R-CNF-02]` is cited in the same sentence, and `[R-CNF-11]`'s priority
rule is not needed.

**Byte-level.** No. `[R-CNF-02]`: "a file declaring another major is neither
conforming nor nonconforming under it: a reader refuses such a file on capability
grounds (§6.3, `[R-CNT-07]`), and that refusal is not a finding about its bytes."
The reader outcome is reject-file under both readings; only the verdict label and
the §6.3 diagnostic move, and neither verdict permits certification.

---

## verifier-03 — no reporting obligation for an unassigned-type record's extent

**The asymmetry is real.** `[R-MTA-10]` carries the only per-record report duty in
the document:
> "it MUST report each record it ignored on this ground, naming the owning scope,
> the encoding value, and the stored extent length, as it reports the slack total
> (`[R-CNT-21]`): bytes a certificate covers without inspecting are counted and
> named, never silent."

A grep for `MUST report|SHOULD report` over the whole file returns nothing
comparable for a record of an unassigned type. §21.6's row reads only "Ignored,
and preserved or dropped per its PE bit", and the file is conforming.

**But the reporter's premise is wrong on the text.** §22.3 does not give the two
residues the same reason. For the unassigned *type*:
> "covered by no checksum either (§8.1), so corruption inside it is equally
> invisible: §20.4's byte-identical re-emission (`[R-WRT-05]`) carries such an
> extent forward unread, and `[R-WRT-08]` bars re-encoding it, so nothing an
> updater does would surface the damage."

The residue named there is invisible *corruption*, and it is explicitly closed by
preservation, not by reporting. For the unassigned *encoding* the residue is the
opposite case — the extent *is* checksummed, and the residue is uninspected
*content*: "the CRC detects corruption and authenticates nothing (§4.5), so a
certificate covers those bytes uninspected". §22.3 distinguishes them; it does
not equate them. And §22.3 opens the paragraph "Four residues are stated rather
than defended" — the document declines to defend, and creates no parallel duty.

The reporter concedes the point itself: "I am supplying the obligation, not
reading it."

**Verdict.** PARTIAL. The asymmetry is correctly observed; the characterization
that §22.3 gives one reason for both is not supported; a defect is not
established. This is a design-decision-shaped request for a new obligation.

**Byte-level.** No. Both verifiers certify the same file — §21.6 makes the MU = 0
experimental-type record a defined non-violation — and §22.3 puts the operator
control it describes explicitly outside conformance: "an operator who wants no
such bytes rejects on that report line, a policy above conformance."

---

## verifier-04 — `[R-COD-11]`'s cannot-establish branch is dead for a conforming verifier

**Checked.** `[R-CNF-03]`: "software that declines to support a core codec, a core
filter, either channel layout, a core sample type, or an assigned user-metadata
encoding is not a conforming reader". §17.2 makes codecs 1–4 core and §17.3 makes
filters 1–2 core. L43 and L45 register every other codec/filter value —
0, reserved, and experimental alike — as reject-layer violations. §2.3:
"An established violation takes priority: a verifier that has established any
violation reports *nonconforming*". So a conforming verifier that cannot execute
a codec has necessarily already established L43 or L45, and reports nonconforming.
The branch is vacuous, exactly as reported. §2.3 nonetheless lists it beside four
reachable grounds, without the qualification it supplies for the metadata case
("A user-metadata document under an encoding this specification does not assign is
not such a ground").

**But the document closes it twice**, not once as the reporter implies: §17.4's
fourth sentence and §2.3's own priority rule. So it is decidable from the
paragraph the implementer is already reading, and from §2.3 alone.

**Verdict.** CONFIRMED as an editorial defect — a normative list carrying a
vacuous member. Cost lower than claimed.

**Byte-level.** No. §2.3: "*Cannot establish* is not a finding that the file is
nonconforming, and a verifier MUST NOT certify a file it reports that way."
Both candidate verdicts bar certification, and the reader outcome is reject-layer
under `[R-COD-03]` / `[R-COD-09]` either way. No file's accept/reject moves.

---

## verifier-05 — §21.7's enumeration read as closed

**Refuted by §21.1 directly.** The reporter's own quoted sentence carries the
qualifier: "§21.7 the account, **by class**, of what fails it." And §21.1 says so
again, in terms:
> "The subsections after §21.5 are not part of the register and carry no rows:
> neither this completeness clause nor the instance arithmetic below reaches
> §21.6's defined non-violations, §21.7's account of what no check detects, or
> §21.9's limits."

The normative completeness clause is expressly declared not to reach §21.7. A
reader who treats §21.7's enumeration as closed and audits the register against
it is contradicting the sentence that clause is stated in. The closing "and" of a
prose list is not a competing reading against explicit text.

The four omitted members the reporter names do sit inside the class the paragraph
describes, and §21.7 states the class principle for the nearest analogue itself
("it is a property of the prior generation, which §9.7 does not reconstruct"), so
even the class membership of `[R-WRT-05]`, `[R-WRT-08]` and §20.4's drop rules is
derivable from the text as written.

**Verdict.** REFUTED. Not a defect. The reporter's own resolution ("the class
governs; the enumeration is illustrative") is what §21.1 says twice.

**Byte-level.** No. §21.1: "The subsections after §21.5 are not part of the
register and carry no rows." Nothing here reaches a row, a verdict, or a byte.

---

## Cross-cutting note on the reporter's citations

`verifier-01`'s worked instances are cited as "my §3.3 file, F = 576" and
"variant B of §4.1". §3.3 (Container and array model) is a single non-normative
Note; §4.1 (Byte order) is `[R-ENC-01]` / `[R-ENC-02]`. Neither contains an
example file. These are the walk's own working artifacts named after sections of
its own notes, not specification citations — worth flagging because the finding's
whole worked argument rests on numbers a reader cannot check against the
document.

Byte-level count across all five: 0.
