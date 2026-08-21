# Maintainer's independent pass over ADR-0083's repairs

Written before reading any auditor's return. Three hunks, `2f54d8d..62d0310`.

## Citations checked, all passing

- §20.5's "in place of the flags = 0 §6.3 requires of a file created under
  this text" — §6.3 reads "a writer creating a file under this text MUST write
  flags = 0", carried by `[R-CNT-08]`. **Passes**, and it closes the circular
  deferral: §6.3 had stated the compactor's carve-out without a modal while
  pointing at §20.5, and §20.5 had done the same pointing back.
- "misstating it to tooling as `[R-CNT-26]` describes" — `[R-CNT-26]` reads
  "misstates the file's feature floor to tooling". **Passes**, verbatim.
- "as it does for an appender (§20.3 step 6)" — step 6 reads "version_minor
  per `[R-CNT-26]`". **Passes.**
- §23.1's "a shrink that de-addresses tiles (§20.3 step 4)" — step 4 states the
  shrink permission and uses *de-addressed* for exactly this. **Passes.**

## Finding — my own repair, unswept half

§20.5 now closes: "**Neither** has a witness in the output alone (§21.7)."
That is a claim about **both** obligations — the ignore-lane carry-forward
MUST and the `version_minor` SHOULD.

§21.7 records **only one of them**: "§20.5's floor on a compacted file's
version_minor (`[R-WRT-06]`) is unwitnessed … the output carrying no record of
its input's minor."

So §20.5 cites §21.7 for a claim §21.7 half-supports — a citation pointing
somewhere it only partly reaches, which is check 2 of the audit's own five,
failed by the commit that added the check's newest subject.

**The substance is right, which is why it is worth fixing rather than
retracting.** A verifier sees the output's `flags` and never the input's, so a
compactor that cleared an ignore-lane bit produces a file no verifier can
distinguish from a legitimate one. Both obligations genuinely lack a witness;
§21.7 should say so for both.

Repair: extend the §21.7 entry to name both — the bits it MUST carry forward
and the floor its minor SHOULD take — and the reason, the output carrying no
record of its input's flags or minor.

Held until the audit returns rather than applied mid-flight, so the auditors'
line references stay valid.

## Noted, not filed

§23.1's enumeration now reads "superseding it, and a shrink that de-addresses
tiles … and a dropped ancillary record's extent goes the same way". Round 18's
writer walk observed that "an unknown ancillary record's drop" understated
§20.4, which also lets an updater drop a record of a type it *does* implement
but this specification does not register. The repair dropped the word
"unknown", which covers that — deliberately, and worth confirming an auditor
agrees the enumeration is now complete.
