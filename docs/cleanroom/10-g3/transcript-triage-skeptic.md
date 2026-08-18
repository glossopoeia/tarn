# Round 10 triage — skeptic lens — working transcript

## What I read

- `/Users/robertkleffner/Documents/GitHub/tarn/spec/tarn.md` in full (3919 lines), read in
  seven passes: front matter + §1–§4 (L1–480), §4.6–§6.4 (L480–760), §7–§9 (L760–1060),
  §9.7–§11 (L1060–1400), §12–§14 (L1400–1700), §14–§17 (L1700–2050), §17–§20 (L2050–2400),
  §20–§21.2 (L2400–3100), §21.3 (persisted to tool-results, then grepped row by row),
  §21.4–§21.6 + §24 (L3158–3610), Appendix A/B (L3609–3700), Appendix G/H (L3781–3919).
- Mechanical checks run:
  - `grep -n "verdict" tarn.md` — 11 hits. Nine are the verifier's three-valued report or
    "no verdict on the file"; L3298 (§21.8) is the sole use identifying a verdict with a
    row's outcome. Confirms register-02's sweep.
  - `grep -n "R-ENC-06" tarn.md` — exactly two hits: L398 (the rule) and L2619 (§19.3's
    reader enumeration). No register cell cites it. Confirms verifier-03 / diagrams-07 /
    adversary-06 mechanically.
  - `grep -n "24 bytes\|record header"` — three hits, all register rows or Appendix B's
    constants table. No hex example of a record header exists. Confirms diagrams-08.
- I did NOT read: `docs/`, `PLAN.md`, `AGENTS.md`, `conformance/`, `spec/registry.json`,
  git history, the web, or the round-9 reporter transcripts. Every judgement below is
  against the document text quoted in the findings and re-verified in the file.

## Grouping principle

One group = one distinct defect (one repair site + one repair). Four Appendix-G groups
stay separate because the repairs are separate items: item 2's hash (4/2/6), item 3's
emission order (3/7/5), item 3's gap-zeroing anaphor (2/4), item 9's encoding coverage (3),
and the closing paragraph's count (1/7). The §20.4 findings split into two genuinely
different defects: the em-dash caveat's attachment (writer-01, quiz-01) and the
flags-authority third cell (writer-05, adversary-02). The §4.7 taxonomy findings collapse
into one: every one of them is the residual class's gloss over-claiming.

## The five groups I tried hardest to kill

### G-supersede-caveat (writer-01, quiz-01) — self-flagged byte-level by both

Two independent reporters read the em-dash clause as attaching to the top-level branch
alone (reading A) and both flagged a byte fork. I spent the most time here.

The deciding text is the *next sentence*, which reuses the same phrase without any branch
restriction:

> Dropping the record is not itself such a change, so a commit whose only effect would be
> the drop MUST retain it.

"such a change" there unambiguously denotes the general criterion stated before the colon
("a commit that *independently* changes the scope the record attaches to"), and it ranges
over records of both kinds. The same phrase two clauses earlier must have the same
antecedent, which makes the tiles-only carve-out global — reading B.

Second decider, internal to the clause: the concession is

> though it re-places that layer's index region

and the word "index" appears in the sub-record branch alone ("that layer's record, index,
or stored tiles"). Under reading A the concession answers an objection nobody would raise
(nobody thinks a moved index region changes *the file's layer set*); under reading B it
answers exactly the objection the sub-record branch invites. A makes the clause inert; B
makes it load-bearing.

Coherence check on B: the sub-record branch keeps all three triggers, because commits that
add tiles, unstore tiles, grow extents, or change the layer record are not commits that
"only supersede" tiles. writer-01's worry that B nullifies two of three terms is
overstated — B carves out one case, it does not empty the branch.

So the text decides for B: an appender may NOT drop a layer's MU=0/PE=0 sub-record in a
supersede-only commit. Both reporters implemented A. Downgraded to non-byte-level, but
this is the group where I am least comfortable and where the cost of my being wrong is
highest (silent loss of application state), so it is called out in `notes`.

### G-compaction-layout (reader-02, quiz-02) — quiz-02 self-flagged byte-level

quiz-02 offers three readings: re-establish the invariants, clear the declaration, or let
placement freedom win with a nonconforming output. Reading (3) dies on

> Given a conforming input the output is a conforming file.

which sits two sentences before the placement grant, in the same requirement, and on
L40/L41/L42 making an unaligned or unpacked declared layer a reject-layer violation.

Reading (2) — clear the declaration — is the one quiz-02 says no sentence excludes. It is
excluded by [R-WRT-07]'s exception list being closed:

> and every retained record per §20.4, **except that** relocation re-points extent slots,
> regenerates each relocated tile-index region (…), and updates the layer-record fields
> covering a regenerated region (crc_of_crc_array).

"per §20.4" routes a retained record through [R-WRT-05]'s byte-identical re-emission, and
the "except that" list enumerates the only permitted departures. A, S and A_slab are not
among them. §20.1 confirms §20.4 binds compactors: "An appender and a compactor satisfy
every writer requirement for the bytes they produce and the preservation obligations of
§20.4 for what they carry forward". quiz-02's own observation that [R-SLB-04]'s
clear-the-declaration escape binds only a *commit* is correct and closes the last door.

So (1) is determined. The defect that remains is real and is reader-02's: the grant is
stated bounded only by §5.2, and §5.2 admits placements §16 forbids, so the sentence
over-grants on its face and both siblings (§20.2, §20.3 step 4) state the obligation their
sibling omits.

### G-flags-authority (writer-05, adversary-02) — adversary-02 self-flagged byte-level

The uncovered cell is real: §20.4's preamble splits {registered} ∪ {not implemented} and
[R-CNT-22]'s "only" shuts the stored-flags door for a type the tool *does* implement. I
looked for the third cell's rule and found it in §21.6, which does not condition on
implementation:

> | A record type this specification has not assigned, from the experimental range
> (≥ 0x8000, §10.2), carries MU = 0 | Ignored, and **preserved or dropped per its PE bit**;
> a *reserved*-range type is read the same way … |

§21.6 is normative (§2.1 excludes only §1, Notes/Examples/Rationales, and non-normative
appendices), and §21.1 says its entries "restate their governing rules on the same terms a
row does". So the stored PE bit governs, and adversary-02's U1 is right. Note also that
retention is always permitted — the MU=0/PE=0 row reads "Retain byte-identical, **or** drop
it" — so only the licence to drop is at stake, and §21.6 grants it.

### G-metadata-encoding-verdict (verifier-02) — self-flagged byte-level

Reading B (cannot establish on an experimental-range metadata encoding) rests on reading
[R-MTA-09]'s "declines to decode" as unconditional. It is not: the sentence's own paragraph
scopes "declines" to the reader's self-chosen resource bound, and the requirement's closing
sentence proves it —

> the verifier SHOULD report **the bound it applied** and the stored length of the extent it
> declined.

A verifier meeting encoding 0x80 applies no bound. [R-CNF-11] also defines the third verdict
as available "where some requirement is one it is **unable to check on a capability or
resource ground**", and §18.2 forecloses the capability ground outright:

> Both assigned encodings are core … An encoding a reader does not implement is therefore one
> this specification does not assign, and is ignore-record (`[R-CNT-25]`).

So the verifier implements everything the specification assigns; the gap is the format's,
not the verifier's, and §21.6's row ("the file is conforming") stands. Verdict: *conforming*.
One clarifying clause in [R-MTA-09] is still worth having, which is why this is PARTIAL and
not REFUTED.

### G-t15-procedure (register-01) — self-flagged byte-level

I checked the arithmetic and it holds: `78 9C` is a valid zlib header (0x789C = 31 × 996,
CM = 8, FDICT clear) and is simultaneously a valid raw-DEFLATE prologue (0x78 → BFINAL = 0,
BTYPE = 00 stored; LEN = 0x009C = 156, NLEN = 0xFF63). So a header-sniffing T15 implementation
does have conforming false positives.

But the text bars that implementation twice. First, §21.1 defines the Instances column as a
corpus-construction column, never a procedure:

> The **Instances** column enumerates what a conformance corpus builds for that row (§21.8)
> … and one whose members give the condition materially different shapes enumerates them
> (T15, T25).

Second, a reader that rejects a conforming tile is nonconforming by [R-CNF-03]: "A reader
MUST accept every conforming file of a format major version it implements". So register-01's
implementation B is not a permitted reading of the register; it is a defective reader. The
residual defect is that T15 and T16 lack the one-clause annotation T13 and T26 carry ("the
check that detects it is T25's, and this row records the cause rather than a procedure of
its own") — a register-bookkeeping repair.

## The one group I refuted outright

**quiz-07** (over-long pre-trailer gap). §6.2 states the answer in terms — "a longer gap is
conforming, and no conforming commit produces one" — and §2.3's conduct-rule account is not
the closed list quiz-07 takes it for; its second sentence is a general clause with §6.3
merely exemplifying it:

> A writer obligation whose violation this specification expressly declares not to be a
> file-conformance violation — §6.3's flags = 0 against a set ignore-lane bit — binds the
> actor in the same way. `[R-CNF-02]`

§6.2 *expressly declares* the longer gap conforming, so the pad case falls inside that clause.
Nothing is missing. Severity: none.

## Downgrade quotes, by group (condensed)

| group | deciding quote |
|---|---|
| front-block-residency | "The test is residency, not transport, so an implementation decides it at its own open path without having to classify the network underneath it." |
| compaction-layout | "Given a conforming input the output is a conforming file." + [R-WRT-07]'s closed "except that" list |
| supersede-caveat | "Dropping the record is not itself such a change…" (same phrase, unrestricted antecedent) |
| flags-authority | §21.6: "Ignored, and preserved or dropped per its PE bit" |
| metadata-encoding-verdict | "the verifier SHOULD report the bound it applied…" + §18.2's core-encodings sentence |
| t15-procedure | §21.1's Instances-column definition + [R-CNF-03]'s acceptance duty |
| appender-refusal | [R-WRT-05] fixes the emitted bytes byte-identically; only whether the commit happens is at stake, and both input and output are nonconforming either way |
| index-regen-trigger | "The output's reference arrays MUST equal the live generation's bit for bit (`[R-MDL-02]`)" |
| subrecord-omission | "both registered types carry PE = 1, so neither can be dropped" |
| partial-slack | [R-CNF-11]: "that per-requirement report constrains the report and not the verdict" |
| every Appendix-G group | "It adds no requirement to any actor: a writer ignoring it is fully conforming." |
| taxonomy groups | the only operative consequence is "a reader MUST NOT alter decoding based on it", true of every candidate field under every reading |
| R-ENC-06 | §21.7: "no file-level witness exists to check, so nothing about the file is left undetermined and the verdict is unaffected." |

## Coverage

44 input ids; 27 groups; union of member_ids = the input list exactly, no duplicates,
counted twice (by hand and by summing group sizes: 1+2+3+3+1+1+1+2+2+1+4+2+1+2+1+3+2+1+2+2+1+1+1+1+1+1+1 = 44).
