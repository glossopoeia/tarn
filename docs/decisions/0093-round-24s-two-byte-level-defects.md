# 0093. A compactor is outside the commit protocol, and the shrink bar has one test

- Status: Accepted (resolves round 24's two byte-level ambiguities)
- Date: 2026-08-24
- Covers: §20.5's writer obligations and the compactor's pad and barriers;
  §20.3 step 4's shrink paragraph
- Revises: nothing; both changes state what was left open
- Confirm: none

## Context

Round 24 returned **two byte-level ambiguities**, both upheld by all three blind
triage passes by membership and not merely by count, and both self-flagged by
their reporters. G3 is not met. This decision answers both.

**The first had been deferred to the ledger.** Round 23's writer walk reported
that §20.5 never binds a compactor to `[R-LIF-02]`; round 23's three passes
graded it *design-decision*, and the disposition sent it to OPEN-QUESTIONS as
Q-A6. Round 24's three passes graded the identical finding **byte-level**. The
text did not change between rounds — the grading did. The lesson is general and
worth stating once: **a design-decision grade is not a finding that something is
not byte-level**, and a deferral cannot make a defect smaller than it is.

The construction is exact. `[R-LIF-02]` is invoked by name for a creator (§20.2)
and for an appender (§20.3 step 6); §20.5 contains no occurrence of
`[R-LIF-02]`, "barrier" or "durable". Compactor P pads to the next 64-byte
boundary and emits F = 4,096; compactor Q aligns its trailer to a 4 KiB device
block and emits F = 8,192 with a 3,452-byte pre-trailer gap. **Both outputs are
conforming** — §2.3 names "§6.2's pre-trailer gap longer than `[R-LIF-02]` step
5's pad" among the writer obligations whose violation is not a file-conformance
violation — so no reader's verdict separates them and the emittable set moves.

**The second was settled by a panel rather than by a repair slot.** Round 24's
adversary showed that §20.3 step 4 carves out "a new padding position whose
stored byte already holds the fill `[R-SER-05]` fixes" as "not what this bars",
then two paragraphs later bars "a shrink that turns real positions into padding
of a tile stored there … whether or not the new state still stores it". Three
repair cycles this week established what happens when a question with two
defensible readings is answered inside a repair slot, so this one was put to six
spec-only agents instead: an **unprimed control** told only the construction and
never that a conflict existed, **two advocates assigned to each reading** and
told to attack the other at its strongest, and a **judge** told that
UNDETERMINED was a real verdict.

The control returned Reading A without being told there was a dispute. Both
B-advocates argued their assigned side and neither conceded. The judge, holding
all five, returned **Reading A**. All six graded the question byte-level.

## Decision

**A compactor is outside `[R-LIF-02]`, and §20.5 says what follows.** That
protocol is stated for a commit, and `[R-LIF-01]` makes a compaction a
whole-file rewrite under a new `file_id` rather than a commit, so neither its
barrier ordering nor its step 5 pad reaches this tier — where §20.2 binds a
creator by name and §20.3 step 6 binds an appender, §20.5 deliberately does not.
Two consequences are now stated as intended rather than left to inference:

- **The output's pre-trailer gap is fixed by nothing.** §6.2 requires the
  trailer to occupy the final 64 bytes and bounds the gap ahead of it only
  through step 5. Two conforming compactors given one input MAY emit outputs of
  different lengths, and the longer gap is conforming — one of the writer
  obligations §2.3 already names as no file-conformance violation.
- **No barrier ordering is owed within the output.** A compaction leaves its
  input intact and writes bytes that are not readable as a TARN file until the
  trailer completing them is present, so there is no committed prefix for a
  barrier to protect and a torn output is an unreadable file rather than a
  damaged one. A compactor SHOULD make its output durable before anything
  discards the input; what discards it is outside this specification.

**The shrink bar has one test, and the shrink paragraph states it.** §20.3 step
4's shrink sentence now says a shrink "that alters what §14 fixes for a tile
stored there is barred whether or not the new state still stores it", and adds
that what counts as such an alteration is the bar above and nothing else, its
carve-out included. The sentence answers the rescue question — whether
de-addressing or unstoring saves a damaging commit — rather than restating the
test.

Three things carried the panel's verdict, and the first is textual rather than a
canon of construction:

1. **The paragraph's own opening is an express biconditional.** "An extent MAY
   also **shrink**, and the bar above is the whole of the test, **in the bar's
   own tense**: a shrink is permitted exactly where it alters nothing §14 fixes
   for any tile the layer stores in the generation this commit supersedes." A
   sentence inside the paragraph that clause governs cannot enlarge what the
   clause declares the whole of. The only premise the disputed sentence gave for
   itself was "the quantifier is the superseded generation's" — a premise about
   *which tiles* are tested, which yields the rider about unstoring and cannot
   yield a conclusion about *what counts as damage*.
2. **The consequence test.** §20.3 states that "where a change does reach them it
   makes each stored tile it reaches nonconforming". After this commit the tile
   satisfies §14 in every particular, §14.5 at the new padding position
   included, so it is conforming; by contrapositive the change does not reach
   it. The barring reading requires a change that is barred, reaches a stored
   tile, and leaves it conforming.
3. **Dead-letter asymmetry.** `[R-SER-02]` derives decoded size and every sample
   offset from the tile extents, the rank, the layout and the channel set —
   never from an extent. A new padding position on a tile whose size and offsets
   are unchanged can therefore arise from an extent shrink and from nothing
   else. Under the barring reading the carve-out has **no instance anywhere in
   the format**, repealed two paragraphs below where it is stated.

## Consequences

The register does not move: 121 conditions, 277 instances, 331 vectors. Q-A6 is
resolved against the reading its own ledger entry favoured.

**The cost of the shrink decision, recorded because the panel's judge named it
as the strongest case against its own verdict.** The bar reads as a rule about
declarations, and this reading makes it turn partly on stored content: the same
directory edit is lawful against one file and unlawful against another that is
byte-identical in structure but differs in what a padding position happens to
hold. A writer must inspect the stored bytes to know whether the shrink is
permitted. That cost is inherent in the carve-out as it was already written —
"whose stored byte already holds the fill" is a content test — and this decision
makes the two passages agree rather than introducing it.

Three propagation acknowledgements recorded. §11.1's Rationale had stated the
qualified test correctly all along; §20.3 now agrees with it word for word.

## Precedent

- `[R-LIF-01]`'s own contrast between a commit and "a whole-file rewrite under a
  new file_id (compaction, §20)", which is why the commit protocol stops short
  of this tier.
- §2.3's list of writer obligations whose violation is not a file-conformance
  violation, which already contained the over-long pre-trailer gap and so
  already anticipated two conforming compactors disagreeing on length.
- §20.3 step 4's "the bar above is the whole of the test", which the panel
  found and which no earlier reading of this contradiction had cited.
