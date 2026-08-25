# Refutation attempt — verifier-01 (AMBIGUITY), round 25

**Target of attack:** the *not byte-level* grade, which is the finding's own
self-grade.

**Verdict: GRADE_STANDS.** Not byte-level.

---

## Access disclosure

Read: `/Users/robertkleffner/Documents/GitHub/tarn/spec/tarn.md` (via `sed`/`grep`
only) and the finding file the brief named,
`.../round25/recovered/verifier-findings.md`, which was at the stated path.
Nothing else was read: no `docs/`, no ADRs, no `conformance/`, no
`spec/registry.json`, no git history, no directory listings, no web.

Unrequested context appeared in my prompt before I began: a project
instruction pointer, an index of the maintainer's private memory notes, and a
git status block carrying recent commit subject lines. One of those subject
lines is topically adjacent to §20.5 compaction, which is a passage this
finding touches. I disregarded all of it and verified every §20.5/§20.3 point
below from the specification's own text. No conclusion here rests on it.

---

## What the grade rests on, and whether it survives

The walk graded it not byte-level because "only a report changes". Three
attacks were run against that.

### Attack 1 — is there a *verdict* divergence, not a reporting one?

The disputed situations are, in both instances, situations in which the
verifier has **established a violation**:

- Instance 1: F20, the directory region's terminal CRC (§21.2 row F20,
  `[R-CNT-11]`, detector **reader**, tier **open**).
- Instance 2: F33, cross-scope claimant overlap (`[R-CNT-13]`, detector
  verifier, tier certification).

§2.3 then forecloses the only verdict divergence available:

> "An established violation takes priority: a verifier that has established
> any violation reports *nonconforming*, however many requirements it was
> unable to check, and *cannot establish* is available only to a traversal
> that established no violation. `[R-CNF-11]`"

So both readings yield *nonconforming* on both instances. `[R-CNF-11]`'s
cannot-establish grounds are closed and enumerated in §2.3 — unimplemented
major, MU = 1 unimplemented type, `[R-COD-11]`, `[R-ERR-04]`/`[R-SER-05]`/
`[R-SER-08]`, `[R-MTA-09]` — every one a *capability or resource* ground.
Uncertainty about the value or label of a diagnostic quantity is not among
them, and could not be: a violation is established regardless.

I then tried to construct a partial total **without** an established
violation, which is the only shape in which the exact/partial label could
touch a verdict. §9.7 names exactly two triggers for an incomplete walk:

> "Where the walk does not complete — a scope-level rejection blocks
> enumeration, or the verifier stops at the first violation (`[R-CNF-11]`) —
> the sum is reported as partial"

Both presuppose a violation. §9.7 further closes the one near-miss itself:
an entry `[R-IDX-03]` classifies reject-tile on a structural ground "does not
make the walk incomplete". A resource decline under `[R-ERR-04]` does not
block *enumeration* (enumeration is structural — tile-index entries, extent
slots — not decode), and even if a verifier treated it as a layer-scope
rejection, that is layer scope, which `[R-CNT-21]` addresses explicitly and
which is not the disputed gap. Verdict would be *cannot establish* under
every reading in any case.

**No verdict diverges.** Attack fails.

### Attack 2 — is the disputed file itself conforming?

This is the brief's discriminator, and it is decisive. Both instances carry a
register-row violation, so both files are nonconforming, so `[R-CNF-05]`
("A writer MUST emit only conforming files") bars every conforming writer from
emitting either under **all three** candidate readings. The emittable set does
not move by a byte.

On the acceptance side, `[R-CNF-12]`:

> "For a nonconforming file no acceptance obligation exists — a reader MAY
> reject it upon detecting any violation, including violations whose assigned
> detector is the verifier."

The MAY is identical under every reading. Instance 1's F20 is reader-detected
reject-file, so readers must reject under both readings; instance 2's F33 is
verifier-detected, so no reader is obliged either way. Nothing moves.

(Worth flagging to the parent: the walk's own phrase "both readers reject the
file" is imprecise for instance 2 — a conforming reader has no obligation to
detect F33 at all (`[R-CNF-04]`, `[R-RDR-02]`); it only *may* reject. The
sub-premise is sloppy; the conclusion survives it, because the file is
nonconforming under both readings and no acceptance obligation exists either
way.)

### Attack 3 — the second instance's exact/partial label, which the finding
itself calls normative

This was the most promising line, because `[R-CNT-21]` does speak of the label
in normative terms ("It is not the file's slack total but a bound on it"). So I
traced every consumer of the total in the document. There are three, and
every one of them is (a) expressly conditioned on a **completed** walk and
(b) SHOULD-level or operator policy:

- §22.3 `[R-SEC-03]`: "a verifier that stopped early reports it only as
  partial (`[R-CNT-21]`), **so the distinguishing figure comes from a walk
  that completes**." The security-relevant signal is defined to be the
  completed-walk figure; the disputed partial totals are excluded by the very
  sentence the finding cites for their importance. The surrounding obligation
  is "a pipeline … SHOULD verify rather than merely read".
- §20.3's Note: "Writers doing many small updates SHOULD batch them into one
  commit, and compact (§20.5) when slack grows — **a verifier whose walk
  completes reports its total** (§9.7)." Same restriction, and a SHOULD.
- §16 `[R-SLB-05]`: "the verifier's slack total, **where its walk completes**,
  is what surfaces the waste", immediately after "A writer that scatters
  structures wastes space rather than violating a rule."

`[R-CNF-12]` puts SHOULD deviation outside the register entirely ("§21's
register enumerates MUST-level conditions only, and a verifier reports a
SHOULD deviation as an advisory that does not bar certification"), and
`[R-CNF-05]` gates emission on file conformance. Per the brief's second
discriminator, a dispute reaching only SHOULD-level and policy consumers
cannot move the emittable set. Compaction is in any case a permission a writer
holds regardless of the number, and a compacted file is conforming either way.

I also checked that the total is never a stored quantity: §5.2 gives slack no
structure, no record type carries it, and no certificate is an in-format
artifact. Nothing about the disputed number is ever serialized.

**Attack 3 not only fails, it strengthens the grade** beyond the walk's own
reasoning: the walk defended the grade on "only a report changes", but §22.3
and §20.3 — the two passages the finding invokes to argue the number matters —
each disclaim the partial figure by name.

---

## What decides it

1. §2.3 `[R-CNF-11]`: "An established violation takes priority … *cannot
   establish* is available only to a traversal that established no violation."
   Both instances have an established violation; no verdict can diverge.
2. §9.7 `[R-LIF-08]`: the only two triggers for a partial total are a
   scope-level rejection and a `[R-CNF-11]` early stop — both entail a
   violation, so no *conforming* file ever carries a disputed total.
3. §2.3 `[R-CNF-05]` + `[R-CNF-12]`: both disputed files are nonconforming, so
   no conforming writer may emit either under any reading, and no acceptance
   obligation exists for either under any reading.
4. §22.3 `[R-SEC-03]`: "the distinguishing figure comes from a walk that
   completes" — the disputed partial figure is excluded from the security
   signal by the cited rule itself.

The ambiguity is real and worth fixing — the document genuinely does not fix
what survives into a partial total at *file* scope, and three defensible
values follow. But resolving it changes no byte sequence a conforming
implementation may emit, must accept, or must reject, and no verdict. The
grade stands.
