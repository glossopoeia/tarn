# The readable edition — edit log

ADR-0133, decision 3: a restatement of a rule may be removed where the rule's
statement remains and the removal is logged with the ADR that added it; a
normative sentence is reworded only one at a time and its ID listed in
`conformance/tools/reworded-ids.txt`. This log is where the edits to edition B
(the `readable` branch's `spec/tarn.md`) are recorded, one entry per commit,
newest first. Edition A is `spec/tarn.md` at tag `edition-a` (`81e2ad2`).

Each entry carries: the date and commit; the sections touched; what was cut,
merged, moved or reworded, in a sentence each; every restatement removed, with
the location where the rule still stands and the ADR that added the
restatement where `git log -S` finds it; every reworded requirement ID; the
soft items `tarn_inventory.py` reported and what each was; and any question
that had to go to the maintainer.

## Ready for calibration 2

Stretches the maintainer has declared reworded, in which the next seed set is
planted (`fidelity-seed.py`, every seed with `statement_count` 1): none yet.

## Entries

*(none yet; edition B equals edition A)*
