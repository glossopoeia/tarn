# Cross-hunk consistency audit — round 19

## 0. Scope note (disclosed)

The charter says "every hunk-NN.diff file ... (all ten of them)". **Only three
exist.** Each file self-labels: "Hunk 1 of 3", "Hunk 2 of 3", "Hunk 3 of 3".
I did not read full.diff. I did not read docs/, PLAN.md, OPEN-QUESTIONS.md,
AGENTS.md, README.md, conformance/, registry.json, or git history.

Command run (this is also the only directory listing I did, via a glob, before
I had read the access rule's "do not list" line; disclosed):
    ls -la .../r19audit/hunk-*.diff      -> 3 files
    for i in 01..10; cat hunk-$i.diff    -> 01,02,03 succeed; 04-10 ENOENT

## 1. The three repairs, and the rule each adopts

### Hunk 1 — §20.5, line ~3168 ([R-WRT-06])
Adopts three rules about a compactor's output trailer:
 (a) MUST copy the input's unknown ignore-lane flag bits forward, displacing
     §6.3's "writer creating a file under this text MUST write flags = 0".
 (b) Where any such bit is set: output version_minor SHOULD be >= input's.
 (c) Where none is set: version_minor "follows [R-CNT-26], as it does for an
     appender (§20.3 step 6)".
 (d) "Neither has a witness in the output alone (§21.7)."
Pre-repair the rule was unconditional and indicative: "carries the greater of
[R-CNT-26]'s floor and the input's version_minor."

### Hunk 2 — §21.7, line ~3614 ([R-ERR-01])
Adds to §21.7's second list (obligations omitted from the register for want of
a single-file witness): "§20.5's floor on a compacted file's version_minor
([R-WRT-06]) is unwitnessed for that same reason, the output carrying no
record of its input's minor".

### Hunk 3 — §23.1, line ~3817 ([R-PRV-01])
 (a) Enumerates: "A commit removes sample data two ways — superseding it, and
     a shrink that de-addresses tiles (§20.3 step 4) — and a dropped ancillary
     record's extent (§20.4) goes the same way; no commit removes a layer."
 (b) Widens the MUST NOT from "a commit that supersedes data" to "any commit
     that makes sample data unreachable".

## 2. Grouping by rule, not by section

GROUP A — the compacted output's trailer fields (hunks 1 + 2).
  Both speak to the same object: what §20.5 obliges about flags and
  version_minor in the output trailer, and whether those obligations are
  register-visible. This is the only pair written to interlock, and it is
  where the same-commit inconsistency sits.

GROUP B — what a commit does to reachability of stored bytes (hunk 3 alone,
  but touching §20.3 step 4, §20.4's drop table, §5.2/[R-CNT-21], §23.2, and
  §20.5's closing Note).

GROUP C — restatement surfaces neither hunk touched: §6.3 [R-CNT-08],
  §20.3 step 6, §21.6's rows, Appendix G items 2 and 8, §20.5's Note.

## 3. Citations opened and verdicts

| Cited in | Target | Verdict |
|---|---|---|
| H1 | §6.3 "flags = 0 §6.3 requires of a file created under this text" | PASS — [R-CNT-08] line 809: "a writer creating a file under this text MUST write flags = 0" |
| H1 | [R-CNT-08] | PASS — line 812-815 already says a compactor "carries the input's unknown ignore-lane bits into its output trailer rather than writing flags = 0 (§20.5, [R-WRT-06])" |
| H1 | [R-CNT-26] ("misstating it to tooling as [R-CNT-26] describes") | **FAIL** — [R-CNT-26] line 823: "a *higher* minor than needed ... misstates the file's feature floor to tooling". Opposite direction. It names no harm from a minor that is too low. |
| H1 | [R-CNT-26] ("version_minor follows [R-CNT-26]") | PASS as a pointer, AMBIGUOUS in effect — see F-02 |
| H1 | §20.3 step 6 | PASS textually — line 3025-26: "unknown ignore-lane flag bits copied forward ([R-CNT-08]), and version_minor per [R-CNT-26]". But the appender's [R-CNT-26] clause reads "the prior trailer's minor", which a generation-1 output has none of. |
| H1 | §21.7 ("Neither has a witness") | **FAIL** — §21.7 names one of the two/three candidate obligations |
| H2 | [R-WRT-06] | PASS — the §20.5 paragraph carrying the floor closes `[R-WRT-06]` |
| H2 | §9.7 / [R-LIF-01] | PASS (unchanged context) |
| H3 | §9.1 | PASS — append-only, "committed-prefix immutability" |
| H3 | §20.3 step 4 (shrink de-addresses) | PASS — line 2993-3006: "Dropping a tile out of the addressed set (§11.2's grid count falls) ... its extent becomes slack"; "Where a shrink is permitted the de-addressed tiles' extents become slack ([R-CNT-21])" |
| H3 | §20.4 (dropped ancillary record) | PASS with a widening — §20.4's table licenses the drop for MU=0/PE=0; the repair dropped the word "unknown" from "unknown ancillary record", which extends it to implemented-but-unregistered PE=0 types. §20.4's opening ("Persistence governs every record type; only the authoritative source of the flags differs") supports the widening, so I do not file it. |
| H3 | [R-CNT-21] | PASS — line 631: "everything an earlier commit superseded" is slack |
| H3 | §9.6 | PASS — "probe backward at 64-aligned offsets o for the trailer magic" |
| H3 | "no commit removes a layer at all" | PASS — §20.4 line 3126 "No commit therefore removes a layer record"; table: "an appender never removes one" |

## 4. Normative placement

All three repairs land in unindented prose, not in ">" blocks. Verified by
reading spec/tarn.md at 3160-3190, 3610-3628, 3821-3836 — no line in any
repaired hunk begins with ">". No repair is stranded in a Rationale.

Counter-direction check (repair edited normative text, restatement left
standing) — this is where the finds are. See §5.

## 5. Searches run

    grep -n "R-CNT-08\|R-CNT-26\|R-CNT-21\|R-PRV-01\|R-LIF-01\|R-LIF-03\|R-WRT-06" spec/tarn.md
    grep -n "version_minor" spec/tarn.md
        -> 532, 744, 793, 798, 820, 3026, 3177, 3181, 3539, 3621, 3998,
           4242, 4270
    grep -n "unstored\|becomes unstored\|supersede" spec/tarn.md
        -> 2941-42 distinguishes "stores or supersedes" from "become unstored"
        -> 3849 §23.2: "a tile unstored by a later commit leaves its earlier
           payload in the file as slack (§23.1)"
    grep -n "erasure\|erase\|deletion\|Deletion" spec/tarn.md
        -> 3264 §20.5 Note (blockquote): "logical deletion supersedes bytes"
    grep -n "ancillary" spec/tarn.md   -> 230, 938, 1441, 3826
    grep -n "R-CNF-11" spec/tarn.md
    grep -n "^#### 21\." spec/tarn.md
Short fragments used deliberately (hard wrap): "version_minor", "unstored",
"ancillary", "erasure", "supersede". No conclusion below rests on a grep
that could not have matched.

## 6. Group A — the two repairs that disagree

Hunk 1 closes: "Neither has a witness in the output alone (§21.7)."
Hunk 2 puts into §21.7, in the same commit, exactly ONE item.

Three obligations sit in the four sentences before "Neither":
  (i)  the MUST to copy unknown ignore-lane bits forward;
  (ii) the bit-set branch's version_minor floor;
  (iii) the none-set branch's deference to [R-CNT-26].
"Neither" is a two-place word. It cannot range over three. Whichever two it
means, §21.7 carries only (ii). Under the natural reading (the two immediately
preceding branches, ii and iii), §21.7 is missing (iii); under the reading that
pairs the flags MUST with the floor, §21.7 is missing (i). Either way the
citation is unsupported for one member.

Independently: (i) is the item that most clearly BELONGS in §21.7's second
list — a MUST-level writer obligation with no single-file witness, the exact
class §21.7 collects ([R-LIF-01], [R-LIF-03]'s generation sequence,
[R-GEO-06]/[R-SER-01], [R-CNT-13], [R-CNT-18], §20.3 step 4's bar, [R-ENC-06]
are all MUST-level). It is absent. (ii) is a SHOULD — the first advisory item
in that list — and §21.1 frames §21.7 as "the account, by class, of what
fails" the *detectability* gate over "detectable file-conformance
violation[s]". A SHOULD violation is not a file-conformance violation and
needs no such excuse; listing it implies the contrary.

Quantifier mismatch inside the pair: hunk 2 writes "§20.5's floor on a
compacted file's version_minor" flat, no condition. Hunk 1's floor exists
only "[w]here any such bit is set". The unconditional form is precisely the
PRE-repair rule ("the greater of [R-CNT-26]'s floor and the input's
version_minor") that hunk 1 replaced. A reader of §21.7 alone reconstructs the
old rule.

## 7. Group A — the "as it does for an appender" fork

  Reading A: a compactor is a creator, so [R-CNT-26]'s writer clause applies —
    "the lowest version_minor that defines every feature present in the file",
    i.e. 0 for a file expressible under this text. The input's minor is
    irrelevant.
  Reading B: a compactor takes the appender clause — "the maximum of that
    floor and the prior trailer's minor" — with the input as the prior
    trailer. Then version_minor >= input's ALWAYS, the bit-set branch is
    vacuous, and the repair changed nothing.
§20.3 step 6 is the appender's step; the appender's own file has a prior
trailer. A compacted output is generation 1 under a fresh file_id and has
none. So Reading A is almost certainly intended and the clause "as it does for
an appender (§20.3 step 6)" is the thing that licenses Reading B.

Byte test: version_minor lives at [74,76) of the trailer (Appendix A line
3998). Two implementations compacting an input with minor 3 and no unknown
ignore-lane bit emit 00 00 (A) and 03 00 (B). But [R-CNT-26] is a SHOULD,
[R-CNT-07] forbids rejecting on version_minor, and §21.6 row 3539 accepts a
higher minor outright. Both files conform under both readings; the emittable
set does not move. NOT byte-level — but it forks Appendix G item 8.

## 8. Group C — Appendix G item 8

  "8. **`version_minor` at the floor** [R-CNT-26] states, and `flags` = 0."
Hunk 1 makes copying the input's unknown ignore-lane bits a MUST. A compactor
adopting the profile on such an input cannot write flags = 0. And under the
bit-set branch its minor SHOULD exceed the floor. Item 2 of the same appendix
already carves the compactor out on exactly this pattern:
  "This is a creator's rule: a compactor adopting the profile takes
   [R-WRT-06]'s fresh draw instead"
Item 8 has no carve-out. Appendix G's preamble says "It adds no requirement to
any actor", so the §20.5 MUST governs and no byte moves — but the profile is
the one place an implementer goes for byte-exactness, and it now tells a
compactor to violate a MUST.

## 9. Group B — the "two ways" count

§23.1 repaired: "A commit removes sample data two ways — superseding it, and a
shrink that de-addresses tiles (§20.3 step 4)".

Falsifier, two paragraphs later, in §23.2, citing §23.1:
  "a sentinel entry (§15.2) marks each **addressed** tile not stored in the
   live generation — a tile unstored by a later commit leaves its earlier
   payload in the file as slack (§23.1)"
An addressed tile turned to the sentinel is NOT de-addressed (entry_count does
not fall; §11.2's grid count does not fall), and §20.3 step 4 keeps the two
apart in its own vocabulary:
  "entries for tiles this commit stores **or supersedes** written to their new
   state, entries for tiles that **become unstored** written as the sentinel"
So on the narrow sense of "supersede" that hunk 3's own contrast with shrink
forces, there are THREE mechanisms and §23.1 names two.
On the broad sense §5.2 uses — "everything an earlier commit superseded" is
slack — the shrink and the sentinel-unstore are both sub-cases of superseding
and there is ONE. No reading of the document yields exactly two.

The widened MUST NOT is fine on its own ("any commit that makes sample data
unreachable") and does cover the sentinel case. The defect is that the closed
count immediately before it invites a reader to take the two-item list as the
extension of "makes sample data unreachable" and exclude the third.

## 10. Group B — unswept restatement

§20.5's closing Note, line 3264-3266, a ">" block:
  "> **Note.** Compaction is the only true removal: logical deletion
   > supersedes bytes but leaves them in the file as slack ([R-CNT-21]) — a
   > privacy consideration (§23)."
This is the pre-repair framing — supersession as what logical deletion is —
pointing at the very section hunk 3 rewrote. Non-normative, so no force, but
unswept.

## 11. Checks that passed

- Hunk 1's (a) does not collide with §6.3: [R-CNT-08] already deferred to
  §20.5/[R-WRT-06] for the compactor case. Elevating "carries" to "MUST copy"
  in the governing section is the right direction.
- Hunk 1's placement does not collide with §20.4's MU=1 bar three lines below
  it, nor with §21.6's "an ignore-lane flag bit is set | Ignored; the file is
  conforming" row.
- Hunk 3's "no commit removes a layer at all" agrees with §20.4 line 3126 and
  the drop table's "an appender never removes one".
- Hunk 3's second paragraph ("Compaction ... is the only operation that
  removes slack ... the input persists, unmodified") agrees with hunk 1's
  fresh-file_id / generation-1 requirement.
- No repair introduced or contradicted a register row; [R-WRT-06] appears in
  no row of §21.2-§21.5 (grep confirms 3186, 3203, 3214, 3621, 3867, 4180).
- §21.7's second list is not framed as closed, so adding to it is legal in
  form; the objections are to what was and was not added.
