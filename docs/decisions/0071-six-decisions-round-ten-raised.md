# 0071. Six decisions round ten raised

- Status: Accepted
- Date: 2026-08-17
- Covers: the field taxonomy; the partial slack total; the appender's
  counterpart to §20.5's refusal; §21.9's domain; row-label drift;
  `[R-VEC-04]` and verifier-detected rows
- Confirm: amends ADR-0065's slack clause; trims ADR-0069's §20.5 sentence

## Context

Cleanroom round 10 left six decisions. Working them up found two live corpus
defects as well — vectors that fail a *correct* implementation, which is worse
than a missing vector, because it punishes the conforming reader.

## Decision

**The `structural` class is broadened to the sense the document already uses.**
§4.7's cascade partitioned field effects into locating/decoding and
value-meaning and called everything else "determines nothing", omitting the
effect the format is built from: a value that decides **acceptance**.
`[R-ENC-10]` refutes the old labels in terms — *"comparing a field against a
constant for validation is not acting on it"* — while magics, reserved bytes
and CRCs were all labelled structural. Three normative sentences already read
`structural` broadly: `[R-CNT-07]`'s *"all feature gating is structural"*,
`[R-MTA-02]`'s *"located, decoded, **or returned**"*, and `[R-SEC-06]`. §4.7
was the outlier, not the tables. It now reads: structural if the value
determines anything a reader or verifier does with the file's bytes — where a
byte lies, how it decodes, or whether the file, layer or tile is accepted;
semantic if not, but it determines what decoded values *are*; descriptive if
neither. `generation` and `file_id` move to structural, and §4.7 now states
the counts, which makes the taxonomy self-checking: **`fill` is the only
semantic field and `version_minor` the only descriptive one.** §7.4's Note
closes the names question — a variable-length field's value includes its
length prefix, so a name is structural.

**The partial slack total becomes an upper bound.** `[R-CNT-21]` counted
*"the bytes no claimant claims within the regions the verifier did walk"* —
but §9.7 enumerates claimants, not regions, so "region" had no definition; and
on a worked 896-byte file with 522 bytes of true slack, the only range the
document can prove claimant-free is 12 bytes. A partial total is now **F less
the bytes claimed by the claimants the walk did enumerate**: always
computable, never an under-count, tightening to the exact total when the walk
completes. This **amends ADR-0065**, whose holding — a verifier that stops
early still owes a bounded total — survives with its derivation replaced, and
its error direction knowingly inverted from under- to over-report. The
companion obligation to name the unwalked regions and their byte extent is
dropped: it asked the verifier to size what the stop prevented it from seeing.

**The appender proceeds, and §20.3 says so.** §20.5's refusal rule had no
counterpart. The distinguisher was already in `[R-WRT-05]` and nobody had
quoted it: *"a record it **modifies** is new output under its writer
obligations (`[R-CNF-05]`)"* — so one re-emitted unchanged is not. §20.3 step
2 now states that a violation the open establishes bars the commits its
outcome bars and no others, that the appender may neither repair the defect
(`[R-LIF-01]` freezes the prefix) nor drop the record (§20.4), and that it
SHOULD report what it carried. The alternative would brick files: a 400 GB
generation-47 archive whose layer record stores PE = 0 where §7.3 fixes PE = 1
could never be appended to again, over a bit no reader reads.

Consistency forced a trim: §20.5's third justification, *"nor author bytes it
knows to be nonconforming"*, rested on treating re-emission as authorship, and
is removed. ADR-0069's first clause carries that rule on its own.

**§21.9 is a finding aid, not an inventory.** `[R-ERR-03]` claimed every
validity-affecting limit *"lives here"*; ADR-0067 completed the list once and
it was short again two rounds later, and a literal reading needs about twenty
more entries — at which point §21.9 becomes a second copy of the register.
`[R-ERR-03]` now takes `[R-CNF-10]`'s actual words and says it collects rather
than exhausts. `[R-VEC-03]`'s *"every boundary value"* clause is not scoped to
`[R-ERR-05]` and keeps the corpus obligation intact.

**The corpus gains a second, stable key.** Row labels are positional by
ADR-0049 and have been renumbered twice in five commits. COV-05 catches a
mis-pointed label only when the two rows' Instances text differs — and **50 of
121 rows share the instance `—`**. Replaying both renumberings, 15% of
re-pointings would have been silent; sweeping all 121 possible single-row
strikes gives 620 silent mis-pointings, with only 18 strikes drift-free. It
has already happened twice, at commit `e417dcb` and at TV-0813. **COV-06** now
asserts that a vector's recorded `rule` is the governing rule of the row it
cites. Rule identifiers do not renumber (§2.2), so they are the stable key.
The check was tested by simulating both shapes of drift, including the
`—`-row case COV-05 is blind to, and it names the cause in both.

**`[R-VEC-04]`'s pair is qualified to the rows it fits.** It required every
reject-layer/tile vector to name *"the scope no reader is permitted to
serve"*, which for a verifier-detected row does not exist — §21.1 says such a
row *"names the scope at which the damage is recorded, not an obligation on
any reader"*. This was ADR-0065's un-propagated half: that ADR concluded the
layer remains servable, edited the sibling disjunct, and left the pair clause
standing two lines below its diff. For a verifier-detected row the pair is now
the scope at which a verifier confines its finding — carried by the entry's own
scope and detector fields — and the content a reader owes.

### Two corpus defects, repaired

**Seven vectors would have failed a correct implementation.** TV-0226 and
TV-0950 recorded `must_not_serve` on verifier-detected rows, because
`l_rows_a.py`'s `L()` helper hard-coded it while exposing `detector=` as a
keyword; the same row's third vector, TV-0811, had it right. And TV-0400,
TV-0407, TV-0408, TV-0409 and TV-0410 recorded expected content derived from
the *seed* while their own patches re-declared the layer's geometry, layout or
channel type — TV-0409 patches layout to planar and the channel to bool, and
still recorded `interleaved`/`uint8`. `seed_content()`'s docstring claims it
"cannot drift from the bytes the builder emits", which is true of bytes and
false of declarations.

Both helpers are fixed. The re-declaring vectors now list only the intact
sibling in `serves`: the corpus cannot yet compute a re-declared layer's true
decoded content, and recording content it cannot compute is what caused the
defect. **That is a stated gap, not a claim that the layer is unservable** —
`[R-VEC-04]` as amended asks for the damaged scope's content, and the corpus
owes it. TV-0954 keeps its `must_not_serve`: MU = 1 on an experimental
sub-record type is an independent reader refusal under `[R-CNT-18]`, which
§21.6 says is not a register row, so the entry records a refusal its cited row
does not carry.

## Consequences

Register and corpus unchanged at **121 conditions over 248 instances, 300
vectors**, 100% coverage. One new check, COV-06. Thirteen spec edits.

Priced knowingly. Broadening `structural` leaves the taxonomy with one
descriptive and one semantic field, which reads thin — but that is a true
claim about this format, and it is what the closed type list, the closed codec
menu and the metadata quarantine were for. The upper-bound slack total is
loosest exactly when a stop is most likely: an early stop on a terabyte file
reports close to a terabyte. That is the honest cost of a number that is
always computable, and §22.3 already says the distinguishing figure comes from
a walk that completes. And trimming §20.5's third justification one commit
after ADR-0069 wrote it is the pattern this gate keeps producing; the trim is
right, and it is also evidence that a rule written to fix an over-strong claim
can carry an over-strong clause of its own.

## Precedent

- ADR-0049's decision that row identifiers are positional, whose cost this
  finally mitigates rather than reverses.
- ADR-0065, amended in its slack clause and completed in its `[R-VEC-04]` half.
- ADR-0069's conduct-voice repair of §20.5, extended to §20.3 and trimmed
  where the same reasoning cuts against it.
- `[R-CNF-02]`'s conduct-versus-predicate split, which is why the appender's
  rule needs no register row.
