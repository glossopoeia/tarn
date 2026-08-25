# Triage pass — implementer lens — round 25 recovered findings

## Access

Read: `/Users/robertkleffner/Documents/GitHub/tarn/spec/tarn.md` (whole file, via
`sed -n` ranges and `grep`), and the brief's own input file
`.../round25/recovered/verifier-findings.md`. Nothing else. No docs/, no
PLAN.md, no conformance/, no registry.json, no git, no web. I did not list or
read the output directory.

Contamination disclosed: before I began, the runtime placed a project
CLAUDE.md pointer and an index of the maintainer's auto-memory files in my
context. I did not open any of them and did not use them; naming that they
appeared, not their contents.

## verifier-01 — partial slack total after a file-scope rejection

Passages opened: §5.2 `[R-CNT-21]` (spec lines ~628–666), §9.7 `[R-LIF-08]`
(~1321–1368), §6.2 `[R-CNT-06]` (~772–782), §7.1 `[R-CNT-11]`, §4.5
`[R-ENC-10]`, §21.2 rows F7/F20/F33, §21.3 rows L18/L40–L42, §21.6's slack row,
§22.3 `[R-SEC-04]`.

Quote verified verbatim. The structure of `[R-CNT-21]` is:

1. general duty — "a verifier that reaches a live state MUST report the total
   number of slack bytes";
2. one express excusal — "Where §6.2's ordered validation rejects the file
   before a live trailer is established … the total is not owed at all";
3. the partial trigger — "Where the walk of §9.7 does not enumerate every
   region's claimants … the verifier MUST report the total as partial";
4. the value — "A partial total is F less the bytes claimed by the claimants
   the walk did enumerate".

I confirm the gap. §6.2's ordered list (magic; CRC; version gate; then flag
gates, committed_file_length, dir_offset, dir_length, dir bounds, generation,
file_id, reserved) does **not** contain the directory CRC, so an F20 file has a
live trailer established and F known — the excusal in (2) does not fire and a
total is owed. The elaboration of "a scope-level rejection ends that scope's
enumeration" is written entirely inside a parenthetical about layers: "a
rejected **layer's** claimants are not enumerated … discarded **with the
layer**, since the total is a claim about a live state one of whose **layers**
is not usable". Nothing states the file-scope case.

Both readings the walk gives are textually anchored:

- **A (387).** Clause (4) is a flat definition. §9.7 names "the directory
  itself" as a claimant, and says the front block and live trailer "are claimed
  by the walk as well, being members of the live committed state" —
  unconditionally, not contingent on reading the directory. dir_offset and
  dir_length are covered by the trailer CRC, which verified, so `[R-ENC-10]`
  does not bar using them. Enumerated = 16 + dir_length + 64.
- **B (F).** The generic sentence is "a scope-level rejection ends **that
  scope's** enumeration", and the parenthetical's first clause reads as an
  instance of it: *a rejected X's claimants are not enumerated, whether or not
  the rejection impeded reading them*. Substituting file for layer discards
  everything, and the stated rationale generalises the same way (here the whole
  live state is unusable). Note also that the discard clause's **trigger** —
  "where the rejection is one the walk itself established" — does fit F20, since
  §9.7 makes checksum verification part of the walk; only its **consequence**
  ("with the layer") fails to transfer.
- **C (496)** has no textual anchor; I would not expect an implementer to reach it.

A/B is a live 1.5× divergence on a number §22.3 makes security-relevant ("the
number that distinguishes a working file from a padded one"). Two implementers
would plausibly split.

The second instance is a distinct and, to me, sharper gap. F33 and F7 are
file-scope rejections a verifier can only establish **after** enumerating every
claimant. The discard clause names "L18's overlap or L40 through L42's
placement" — the layer-scope walk-established rows — and conspicuously not F33
or F7. Under clause (3) the walk did enumerate every claimant, so the total is
not partial; "tightening to the exact total when the walk completes" says
*exact*. Under a generalised reading of (2)/B it is partial and equals F. So the
divergence is in the **label** as well as the value, and the label is normative
("It is not the file's slack total but a bound on it").

**Byte-level: no.** Both disputed files are nonconforming — F20 is reject-file
under `[R-CNT-11]`, F33 reject-file under `[R-CNT-13]`. `[R-CNF-05]` ("A writer
MUST emit only conforming files") bars every conforming writer from emitting
either under both readings, so the emittable set does not move; readers
reject-file either way; and a verifier reports *nonconforming* either way, so no
certification flips. A partial total can only arise where a rejection or an
early stop occurred, which entails a violation, so this quantity never decides a
conforming file's fate.

**Verdict: CONFIRMED, design-decision.** Real underdetermination of a normative
MUST-report quantity; needs a sentence, not a byte change.

## verifier-02 — §21.2's ordering justification vs F5

Passages opened: §21.2 opening paragraph (~3414–3428), §5.1 `[R-CNT-27]`
(~571–575), §6.2 `[R-CNT-06]`, §6.3 `[R-CNT-07]`/`[R-CNT-24]`, §2.3
`[R-CNF-02]`, §19.2 `[R-RDR-02]`, row F5.

Both quotes verified. The factual core of the finding is right:

- §6.2's ordered list does not contain the 128-byte floor. `[R-CNT-27]` lives in
  §5.1 and its F-instance is decidable from the physical size alone.
- §19.2 does license earlier detection: "A reader MAY detect any violation
  earlier (`[R-CNF-12]`)".
- §21.2 applies exactly this ordering test to F6, citing `[R-CNT-04]`'s "before
  other processing", and does not run it for F5.

But the finding overstates the consequence. §21.2 does not leave the ordering
clause as the operative test; two sentences later it gives a closed list and a
criterion: "**Four rows** are outside that reasoning and do reach it, because
their subject is a field fixed across every major (`[R-CNT-24]`): F8 and F1's
trailer-magic instance, F14's trailer CRC … and F6 with F1's front-block
instance." F5 is not in the list, and its subject is not a fixed field —
dir_offset ≥ 16, dir_length ≥ 4 and the 64-alignment all sit in the 48 trailer
bytes `[R-CNT-24]` lets a future major redefine. And `[R-CNF-02]` settles the
verdict independently: "a file declaring another major is neither conforming nor
nonconforming under it". So the *nonconforming* verdict is simply unavailable,
however early the verifier noticed the 96-byte floor. I verified the walk's
construct is buildable (F=96, front [0,16), trailer [32,96), dir_offset in
16..28) — it just doesn't produce the divergence claimed.

So what is left is an over-broad justificatory clause: true of §6.2's own list,
not true as a general statement about every check in the document, and used to
carry rows that §6.2 never orders. Worth fixing; not a verdict hazard.

**Byte-level: no.** Reject-file under both readings, and no writer emits a
major-7 file under this text at all.

**Verdict: PARTIAL, editorial.**

## verifier-03 — reporting asymmetry between two §22.3 residues

Passages opened: §8.1 `[R-CNT-19]` map (~1113–1131), §22.3 `[R-SEC-04]`
(~3851–3893), §18.2 `[R-MTA-10]` (~2586–2601), §21.6's experimental-type row,
§7.2 `[R-CNT-15]`, §2.3's verifier duties.

Both quotes verified. I ran `grep -n "MUST report\|SHOULD report"` over the whole
file: the only report obligations that could bear here are `[R-CNT-21]`'s slack
total, `[R-CNF-11]`'s unable-to-check and *unexamined* lines, `[R-MTA-09]`'s
SHOULD, §21.5's readers-SHOULD-report, and `[R-MTA-10]`'s "MUST report each
record it ignored on this ground, naming the owning scope, the encoding value,
and the stored extent length". **Nothing names the extent of a record of an
unassigned type.** The asymmetry is real and I confirm it.

I also confirm the reachability claim: §21.6 registers "A record type this
specification has not assigned, from the experimental range (≥ 0x8000, §10.2),
carries MU = 0 → Ignored" as a *defined non-violation*, and `[R-CNF-02]` makes
§10.3's publication ban bind conduct, not bytes. So a conforming file can carry
an arbitrary, unchecksummed, unconstrained record extent that a certificate
covers with no report line. `[R-CNF-11]`'s unable-to-check duty does not reach
it either: there is no requirement left unchecked, exactly as `[R-MTA-10]` says
for its own case.

One correction to the finding's framing. §22.3 does not give the two residues
"the same reason". The unassigned-type residue is argued from *no checksum*
("corruption inside it is equally invisible"); the metadata residue is argued
from *a CRC that authenticates nothing* ("a certificate covers those bytes
uninspected"). They are adjacent, not identical. The operator-policy sentence
the finding leans on is attached to the metadata case only. Extending
`[R-MTA-10]`'s report line to unassigned types is a spec addition the maintainer
should decide on, not a misreading being corrected — and the walk says as much:
"I am supplying the obligation, not reading it."

**Byte-level: no.** §8.1's row leaves those bytes opaque and no rule constrains
them, so the emittable set is identical under both readings and both verifiers
certify the same file.

**Verdict: CONFIRMED, design-decision.**

## verifier-04 — the dead cannot-establish branch of `[R-COD-11]`

Passages opened: §17.4 (~2399–2416), §2.3 `[R-CNF-03]`/`[R-CNF-11]`
(~150–224), §17.2 `[R-COD-03]`, §17.3 `[R-COD-09]`, §21.3 rows L43/L45, §17.2's
window-size SHOULD, §21.9's `[R-ERR-04]` citation.

Quotes verified. Chain checked end to end:

- Codecs 1–4 and filters 1–2 are core; `[R-CNF-03]`: "software that declines to
  support a core codec … is not a conforming reader".
- §2.3: "Verifiers and updaters are readers of the files they process and
  inherit every reader obligation."
- §17.4 sentence 4: "For a conforming reader that position arises only at a
  reserved or experimental value … it rejects the layer (`[R-COD-03]`,
  `[R-COD-09]`)".
- L43 and L45 both carry **Detector: reader, Detected: layer access** — so the
  bad value is an *established* violation, not merely a refusal.
- `[R-CNF-11]`: "An established violation takes priority: a verifier that has
  established any violation reports *nonconforming*."

So the cannot-establish branch of `[R-COD-11]` is unreachable by any conforming
verifier, and §2.3 lists it beside four grounds I checked and found reachable
(unimplemented major; experimental top-level type with MU = 1 per §21.6;
`[R-ERR-04]` resource declines; `[R-MTA-09]` metadata declines). The walk's
identification of §17.2's wider-window SHOULD as the *reachable* codec-adjacent
ground — "a wider window is conforming and merely permits a conforming reader to
decline the tile or the layer on resource grounds (`[R-ERR-04]`)" — is correct
and is a different rule.

This is decided by the text; the defect is that §2.3's list presents a dead
ground without the narrowing, and §17.4 places the narrowing in a sentence that
reads as an aside. Cheap fix: a cross-reference.

**Byte-level: no.** Reject-layer under both readings, and the file is
nonconforming under both, so neither the emittable set nor certification moves.

**Verdict: CONFIRMED, editorial.**

## verifier-05 — §21.7's second-paragraph enumeration

Passages opened: §21.7 `[R-ERR-01]` (~3650–3719), §21.1's completeness clause
(~3345–3352), §9.2 `[R-LIF-02]` steps 4/6, §20.2 `[R-WRT-02]` ("both barriers,
not one"), §20.4 `[R-WRT-05]`, `[R-WRT-08]` and the MU=0/PE=0 drop row, §20.5.

Quotes verified. I checked the four alleged omissions against the paragraph's
own class ("obligations … omitted from the register because a single file
exhibits no witness of their violation") and against the enumeration's actual
members ( `[R-LIF-01]`, `[R-LIF-03]`, `[R-GEO-06]`/`[R-SER-01]`, `[R-CNT-13]`'s
no-embedded-offsets, `[R-CNT-18]`'s nesting bar, §20.3 step 4, §20.5's four
`[R-WRT-06]` obligations, `[R-ENC-06]` ):

- `[R-WRT-05]` byte-identical re-emission — **confirmed absent**, and squarely
  in the class: its own Rationale says "the records of *adjacent generations*
  differ exactly by those modified, added, or dropped", i.e. two files.
- `[R-WRT-08]` no re-encoding of an unimplemented type — **confirmed absent**,
  same ground.
- §20.4's MU=0/PE=0 drop rule ("An appender MUST NOT drop it except in a commit
  that *independently* changes the scope the record attaches to") — **confirmed
  absent**; it compares two generations' record multisets.
- `[R-LIF-02]` steps 4/6 barriers — **absent, but weaker as an omission**: a
  storage barrier is arguably §2.3's *conduct* class ("govern their conduct
  rather than their output"), not a candidate for the register at all, so it may
  be excluded one level up.

Three of four stand, so the enumeration is genuinely non-exhaustive of the class
it names, and the closing "and" reads as closing a list. Against that:
§21.1 — the very clause the finding invokes — says §21.7 is "the account, **by
class**, of what fails it", which licenses the walk's own resolution ("the class
governs; the enumeration is illustrative"). Cost is wasted audit effort and a
spurious defect report, no more.

**Byte-level: no.** §21.7 itself decides it: "no file-level witness exists to
check, so nothing about the file is left undetermined and the verdict is
unaffected."

**Verdict: CONFIRMED, editorial.** Fix is one hedge word ("among them") or three
added members.

## Summary

Byte-level count: 0 of 5. I agree with every one of the walk's own byte-level
grades. Where I part from the walk is on severity/consensus for verifier-02:
§21.2's closed four-row list and `[R-CNF-02]` both give the right verdict, so
"yields the wrong verdict" overstates it. The one finding I would put at the top
of the maintainer's queue is verifier-01 — it is the only one where I would have
had to guess, and where I believe another implementer would have guessed
differently.
