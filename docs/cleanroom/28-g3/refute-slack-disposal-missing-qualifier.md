# Refute pass — §9.7's slack disposal drops §15.3's "that no other claimant claims"

Verdict: **NOT_BYTE_LEVEL**

## Disclosure

Read exactly one file: `/Users/robertkleffner/Documents/GitHub/tarn-first-draft/spec/tarn.md`.
Ran only `sed -n` / `wc -l` / `grep -n` against that file, plus `mkdir` for my private
scratch dir. No git, no directory listings, no other file, no network. Wrote this
transcript and nothing else; my private scratch dir
(`.../r28-refute/priv-slack-disposal-missing-qualifier/`) ended up unused — every
computation here is arithmetic small enough to do inline.

Context I did not ask for appeared before I began: a project-instruction block pointing at
an AGENTS.md, a user-email line, a date line, an environment block naming the repo, the
branch and five recent commit subject lines, an MCP-server instruction block, and a
skills listing. I did not read any file it names and I treat none of it as evidence about
the specification. I disclose it here without repeating its contents.

## The disputed sentence (line 1477-1480, §9.7, `[R-LIF-08]`)

> An entry `[R-IDX-03]` classifies reject-tile on a *structural* ground does not make the
> walk incomplete: the walk passes over it, and the bytes it nominally addresses fall to
> slack (§15.3).

versus §15.3 `[R-IDX-03]` (line ~2168-2171):

> Such an entry contributes no stored extent to the *verifier* rows ... and none to
> `[R-LIF-08]`'s coverage walk, so any bytes it nominally addressed **that no other
> claimant claims** fall to slack.

The defect is real: the qualifier is dropped, and three structural rows reach claimed or
nonexistent bytes (offset < 16 → front block; offset+length > F − 64 → live trailer;
sentinel-mismatch rows carrying offset 2⁶⁴ − 1 → bytes outside the file).

## The gate that closes the writer side

§15.3's six *structural* rows are register rows T6, T7, T8, T9, T10, T11, T12 (§21.4).
§21.1: the register "enumerates every detectable file-conformance violation this
specification names." §2.4 `[R-CNF-12]`: "A file is conforming only if it satisfies every
requirement at every scope: the outcome classes describe the blast radius of a violation
for readers, never degrees of file conformance." §2.3 `[R-CNF-05]`: "A writer MUST emit
only conforming files."

§9.7's disputed sentence is scoped, by its own words, to entries `[R-IDX-03]` classifies
reject-tile on a structural ground. Every such entry is a T6-T12 violation. Therefore
**no conforming file exhibits the disputed sentence at all**, and the emittable set is
identical under both readings — the second sentence of `[R-CNF-05]` licenses divergence
within what the rules leave open, and emitting a T8 entry is not left open.

## The three texts that decide the disposal itself

1. §5.2 `[R-CNT-21]`, the defining rule, stated as a complement:
   "Every byte the live state does not claim is **slack**."
   A byte the live state claims is therefore not slack, whatever §9.7's gloss says.
2. §9.7 itself, two sentences earlier, in the same complement form:
   "Bytes the walk does not reach are slack: the verifier sums them and reports the total."
   And, three sentences earlier: "The front signature block at [0, 16) and the live trailer
   at [F − 64, F) are claimed by the walk as well, being members of the live committed
   state (`[R-CNT-02]`)."
3. §21.6's register entry, whose Condition column is itself the complement definition:
   "Bytes the live state does not claim — alignment gaps, the pre-trailer pad, superseded
   structures | Slack: unconstrained content, no conformance requirement, counted and
   reported by a verifier ... | `[R-CNT-21]`". §21.1: "§21.6's entries restate their
   governing rules on the same terms a row does, and where such an entry and the rule it
   cites diverge, the rule governs there too."

Even §5.2's *partial* total is complement-shaped: "A partial total is F less the bytes
claimed by the claimants the walk did enumerate."

## Constructions tried

**C1 — Writer emits a file exploiting the literal reading.** Layer with one stored tile
whose entry is offset 8, length 8 (nominal extent [8,16)); writer argues the bytes are
"slack", "content is unconstrained", so it may put payload in the front block's reserved
half. Killed by: T8 is a register row → the file is nonconforming → `[R-CNF-05]` bars it
under both readings. Also §6.1: "Bytes [0, 16) of every file, constant in every format
major version".

**C2 — Verdict escalation: reject-tile vs reject-file.** Argue the literal reading makes
[8,16) belong to two classes, tripping `[R-CNT-02]`'s "belongs to exactly one of" → F33 →
reject-file, where §15.3's reading yields only reject-tile. Killed twice over. (a) Slack is
not one of `[R-CNT-02]`'s classes — the classes are "the front signature block; or a
**structure**" — so "front block and also slack" is not two of the enumerated classes;
§5.2's Note: "'belongs to no class' describes nothing ... What remains, and what a verifier
actually checks, is that no two claimants overlap." (b) A structural entry is not a
claimant under either reading — §9.7: "contributes no stored extent to the walk"; §15.3:
"contributes no stored extent to the *verifier* rows". (c) F33's own text routes the case
away: "a claimant reaching the front signature block or the live trailer is instead caught
by the bounds rows F9/F10, F30/F31/F32, L15/L16/L17 and **T8/T9**, each at its own tier".
The register has already assigned the outcome, at reject-tile, for both readings.

**C3 — Compaction path.** Compactor reading §20.5's "so slack is never carried" together
with the literal §9.7 concludes the front block or the trailer is slack and omits it, or
places output bytes differently. Killed by `[R-WRT-07]`: "An entry §15.3 classifies
reject-tile on a structural ground is neither ... so regenerating the region cannot proceed
without meeting it, and the violation is thereafter one the compactor has detected.
`[R-WRT-06]` then obliges refusal ... no drop is available, a tile-index entry being no
record §20.4's table licenses dropping." The compactor emits **nothing** under either
reading. Independently, §5.2 defines the live committed state as including the front block
by name, and §6.1 fixes bytes [0,16) of every file.

**C4 — Appender reuses "slack".** If [8,16) is slack under the literal reading, and slack's
"content is unconstrained, and no conformance requirement applies to it", may an updater
overwrite it in a later commit — bytes one reading permits and the other forbids? Killed by
§9.1 `[R-LIF-01]`: "Bytes in [0, F) — F being the live trailer's committed file length —
are immutable: a writer MUST NOT modify them." Immutability is stated over the committed
prefix and never consults the slack classification. §9.2 step (1) likewise begins writing
"at exactly F".

**C5 — Verifier skips a check because the bytes are "slack".** §9.7: slack bytes' "content
is not its concern" → a verifier under the literal reading does not check [8,16) against
the front-block constant → certifies where the other reading rejects on F6. Killed by: F6's
check is a *reader* row detected at **open** under `[R-CNT-04]`/§6.1, not a product of the
coverage walk; §2.3 defines a verifier as "A reader that additionally checks every
file-level requirement". And the file carries T8 regardless, so §2.4 applies: "For a
nonconforming file no acceptance obligation exists."

**C6 — Trailer variant (T9).** Entry with offset+length reaching [F−64, F); argue the
literal reading makes the trailer slack, so the trailer CRC need not verify. Killed by
§8.2's strictly ordered chain "trailer → directory → ..." and by F8/F14/F17, all detected
at open before any walk. And the file carries T9 either way.

**C7 — Sentinel-mismatch rows (T6/T7), offset = 2⁶⁴ − 1.** Under the literal reading the
"nominally addressed" bytes do not exist, so the additive slack sum can exceed F or
overflow: e.g. F = 128, one T7 entry with offset = 2⁶⁴ − 1, length = 4096 → additive total
= (128 − claimed) + 4096 > F, versus the complement total ≤ 128. The numbers genuinely
differ. But the number is a **report**: `[R-CNT-21]` — "a verifier that reaches a live
state MUST report the total number of slack bytes"; §21.6 registers slack as a defined
non-violation; `[R-CNF-11]`'s verdict vocabulary is *conforming* / *nonconforming* /
*cannot establish*, and this file is *nonconforming* on T7 under both readings. No byte of
any file changes and no verdict changes.

**C8 — Does the figure ever escape into emitted bytes?** Searched every occurrence of
"slack" in the document (43 hits). §6.2's trailer defines no slack field ("The
format-major-1 trailer has zero slack: every byte is" — describing its own reserved
bytes, not a counter). §18.4's standardized keys are `tarn.title`, `tarn.description`,
`tarn.created`, `tarn.creator`, `tarn.axes`, `tarn.stats`, each "OPTIONAL and advisory".
§24's manifest records identifier, conformance, decoded content, outcome class, scope and
register row — no slack figure. §22.3's "caught only by the slack total changing" is a
stated security residue, not a requirement on bytes. Nothing writes the figure into a file.

**C9 — The reporter's own slab layout, pushed for a scope change.** Run's second tile given
offset 8 (T8): does the divergence change §16.2's packing verdict, which is reject-*layer*
and so a wider scope than reject-tile? Killed by §16.2 stating the transparency itself,
with no dependence on §9.7: "So are the entries §15.3 classifies reject-tile on a
*structural* ground: they address no usable extent, and the run's stored tiles close over
them." Identical under both readings.

**C10 — Degenerate files.** The 128-byte minimum file (zero layers, empty directory) and a
layer with entry_count = 0 ("At entry_count = 0 there is no region at all") contain no
index entry, so the disputed sentence has no subject. A one-tile layer whose single entry
is the sentinel likewise: the sentinel row is *valid*, not structural.

**C11 — Complete vs partial total.** Could the divergence flip a walk from complete to
partial, which `[R-CNT-21]` makes a MUST-report distinction? No: §9.7's same sentence says
a structural entry "does not make the walk incomplete" under both readings, and §5.2's
partial total is itself the complement of enumerated claimants.

**C12 — BCP 14 angle.** The disputed sentence carries no all-capitals keyword ("fall to
slack"). I did **not** rest on that: §2.1 binds keywords only in capitals, but a clause
with no keyword can still carry force (`[R-CNT-13]` is the project's own counterexample).
The sentence is normative text under `[R-CNF-01]` — it is not labeled Note, Example or
Rationale — and I treated it as normative throughout. It loses to §5.2 on substance, not
on keyword count.

## Conclusion

The finding is a genuine editorial defect: §9.7's restatement is wrong as written, and one
of the three passages it contradicts (§5.2) is a definition, not a gloss. But the set of
files that can exhibit it is exactly the set carrying a T6-T12 register row, which is
nonconforming under both readings; `[R-CNF-05]` bars every conforming writer from emitting
one, `[R-WRT-06]`/`[R-WRT-07]` make a compactor refuse one, and the outcome for a reader is
reject-tile under both readings because F33 hands the front-block and trailer cases to
T8/T9 by name. What moves is one figure on a verifier's report line, which `[R-CNT-21]`
makes a report and §21.6 makes a non-violation. Not byte-level.
