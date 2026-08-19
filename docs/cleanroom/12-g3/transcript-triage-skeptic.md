# Round 12 triage — skeptic pass

## Disclosure of what I read

Read in full or in substantial part, from `/Users/robertkleffner/Documents/GitHub/tarn/spec/tarn.md`
(3982 lines):

- front matter (lines 1–22), §2 (all), §3.1–3.3, §4 (all), §5.1–5.2, §6.1, §6.3
  (`[R-CNT-07]`, `[R-CNT-08]`, `[R-CNT-24]`, `[R-CNT-26]`), §7.1–7.4, §9.1–9.3,
  §9.7, §10.1–10.4, §11.1–11.4, §12.3, §14.3–14.5, §15.1–15.4, §16 (all),
  §17.1–17.4, §18.1–18.4, §19.1–19.4, §20.1–20.5, §21.1, §21.2 (F1–F36),
  §21.3 (L30–L49), §21.4 (T1–T26), §21.5 (R1–R10), §21.6–21.9, §23.1–23.2,
  §24, Appendix A, Appendix B, Appendix C, Appendix G, Appendix H.

Commands run: `wc`, `sed -n`, `grep -n` over the spec only. Greps used to
settle specific claims: `grep -io "shrink|shrunk|reduce the extent"` (zero
hits — confirms writer-02's claim that extent reduction is nowhere addressed);
`grep -nE "^0[0-9a-f]{3} "` (the only hex dump in the document is Appendix A's
128-byte no-layer file — confirms diagrams-09).

I did **not** read: the round-12 reporter transcripts in the scratchpad, `docs/`,
`PLAN.md`, `AGENTS.md`, `conformance/`, `spec/registry.json`, git history, the
web. Every judgement below is against the spec text as quoted in the findings
and verified by me in the file. No input finding was left unevaluated.

## Grouping

34 input ids → 24 groups. Three multi-member groups:

- **appender-carries-malformed-index-entry**: reader-01, writer-01,
  adversary-01, quiz-01. One defect: §20.3 `[R-WRT-04]` step 2 directs an
  appender to write a malformed index entry into a region step 4 forces it to
  re-emit, against `[R-CNF-05]`/`[R-CNF-06]`. adversary-01 differs only in
  supplying a constructed 448-byte file (T10 rather than T8); same rule, same
  collision, same two candidate readings.
- **appendix-g-item3-top-level-record-order**: reader-02, writer-03,
  verifier-02, diagrams-05, adversary-05. Five statements of one defect.
- **appendix-g-item2-file-id-underspecified**: writer-04, diagrams-04,
  adversary-03, quiz-02. Four statements of one defect. writer-08 is *not* in
  this group: it is a different defect (item 2 against `[R-WRT-06]`'s
  fresh-file_id MUST) with a different repair.

Everything else is a singleton.

## The two calls I worked hardest to overturn, and how they came out

### 1. appender-carries-malformed-index-entry (4 reporters, 3 byte-level flags)

This is the round's centre of gravity, so I hunted for the deciding text rather
than reasoning from the collision. Five things decide it, and I list them
because a single one would not have persuaded me.

(a) The paragraph's own subject is *which violations bar a commit*, and it
answers the tile-scope case in the same breath:

> "A violation the open establishes bars the commits its outcome bars and no
> others: reject-file bars every commit, and reject-layer bars a commit that
> modifies that layer. The open establishes no tile-scope violation — it
> consumes the trailer and directory only (`[R-RDR-01]`) — and a malformed
> index entry an appender meets while re-emitting a region is carried forward
> byte-identically at its disk-ordinal position under step 4, not repaired to a
> sentinel."

The reporters read the second sentence as directing what the *entry* looks like
while leaving open whether the commit may proceed. But the sentence sits inside
an enumeration of what bars a commit, and it is the entry for the tile-scope
row of that enumeration. A tile-scope violation does not bar the commit.

(b) The very next clause presupposes the commit happened:

> "An appender that carries a violation forward SHOULD report it, and a caller
> that is not told cannot know the file it extended was already damaged."

"the file it extended" — the extension is done. Under the refuse reading no
file is extended and this SHOULD is dead text.

(c) `[R-CNF-05]` is expressly *not* the appender's obligation. §20.1:

> "A creator emits only conforming files (`[R-CNF-05]`). An appender and a
> compactor satisfy every writer requirement for the bytes they produce and the
> preservation obligations of §20.4 for what they carry forward
> (`[R-CNF-06]`) … and certifying the whole file is a verifier's office (§9.7).
> `[R-WRT-01]`"

Every reporter's reading (b) is built on `[R-CNF-05]` binding the appender to
emit a conforming *file*. `[R-WRT-01]` assigns that requirement to the creator
and hands the appender the narrower one. This is the sentence none of the four
quoted.

(d) §20.5 shows the document saying "refuse" for the compactor and choosing not
to say it for the appender, in adjacent sections, for the same defect class.
Expressio unius; the reporters themselves note the asymmetry and then discount
it.

(e) The drafter *named* `[R-CNF-05]` when reconciling — "re-emitting it
byte-identically is not authorship, since `[R-WRT-05]` makes only *a record it
modifies* new output under `[R-CNF-05]`". The collision was seen and answered.

What survives, and it is real: the answer's *citation* does not reach a
tile-index region. `[R-WRT-05]` governs records ("header, inline payload, and
extent slot"), and a tile-index region is not a record. So the outcome is
determined and the justification is not. That is an editorial/design defect in
the grounding, not a fork in the bytes. Repair: state the non-authorship
doctrine for a re-emitted tile-index region directly, without routing through
`[R-WRT-05]`. Note the maintainer *could* instead choose the compactor rule for
appenders — that choice would change emitted bytes, which is why I grade the
severity design-decision rather than editorial, while holding byte_level false
for the text as it stands.

Corroborating signal, not evidence: all four reporters independently
implemented reading (a). A live fork usually splits its readers.

### 2. writer-02 (a commit that shrinks a dimension extent)

I nearly upheld this one. `grep` confirms "shrink"/"shrunk" appear nowhere, and
`[R-CNF-06]`'s "for the bytes it produces" quantifier plus `[R-WRT-01]`'s
"certifying the whole file is a verifier's office" genuinely appear to license
shape (c) — the untouched edge tiles are not bytes the commit produces.

What kills it is that the commit modifies the layer record, and §20.4 says:

> "a record it modifies is new output under its writer obligations
> (`[R-CNF-05]`). `[R-WRT-05]`"

with `[R-CNF-05]` = "A writer MUST emit only conforming files." So the
whole-file obligation attaches through the modified record — which is exactly
the mechanism §20.3 step 2 has to *disapply* (via "not authorship") in the
malformed-entry case, and here there is no such disapplication: the doctrine is
about a structure "the appender carries forward", and untouched edge tiles are
neither carried forward nor latently defective — `[R-WRT-01]`'s carve-out is
for "a violation latent in a structure they neither modify nor rely on", and
before this commit there was no violation to be latent.

The document's only treatment of the same shape of problem points the same way,
in §20.3's shape taxonomy:

> "A fill change on a layer carrying either additionally requires re-emitting
> the affected stored tiles, whose content `[R-SER-05]` fixes — which makes it
> shape (b)."

(That passage is inside an **Example**, hence non-normative under
`[R-CNF-01]` — so it cannot carry reading (ii) either.)

Conclusion: the gap the reporter found is real and worth a normative sentence —
the document never says an extent may shrink and never states the consequent
obligation, and the same hole reaches a channel-type or channel-set change that
moves Q. But the bytes are decided: only re-emission yields a conforming file
and the updater is on the hook for one. byte_level false; severity
design-decision, because the repair is a maintainer choice (prohibit reduction,
or state the re-emission obligation).

### Third closest call: writer-05 (two MU=0/PE=0 drops licensing each other)

The purest "may emit" shape in the set — both candidate outputs are conforming
files. Decided by two things in the cell itself:

> "An appender may drop it only in a commit that *independently* changes the
> scope the record attaches to … Dropping the record is not itself such a
> change either, so a commit whose only effect would be the drop MUST retain
> it."

Reading (i) needs circular licensing: R1's drop is grounded in R2's, R2's in
R1's, and neither has a ground outside the pair. The italicised *independently*
is precisely the word that forbids that, and "Dropping the record is not itself
such a change" states the class-level fact that a drop is not a qualifying
change. A reading under which a MUST is evaded by performing the forbidden act
twice is not a permitted reading. Still, this is the thinnest decider in my
output and the cheapest repair: add "nor is dropping another such record".

## Per-group notes (singletons)

- **reader-03** — §19.2's bullets assign name parsing to the open explicitly
  ("**at open:** … and the layer-name namespace (§19.1's steps)") and the
  layer-record validation to first access; its rationale states the cost model
  ("its one namespace-wide obligation — parsing each record's name — runs over
  bytes already fetched and CRC-verified"). `[R-RDR-02]` is a latest-detection
  rule ("no later than"). Loose phrase in §19.3, decided by §19.2. Editorial.
- **writer-06** — trigger/scope mismatch in `[R-SLB-04]` verified: storing a
  previously-sentinel tile and unstoring a stored tile both change a run's
  stored-tile set and neither "supersedes a stored tile in, or grows the
  extents of". `[R-SLB-03]`'s invariants bind the file regardless (L41/L42), so
  no byte forks. Confirmed observation.
- **writer-07** — closed by `[R-CNT-22]`'s own quantifier ("Stored flag bits
  are authoritative only for record types the consuming tool does not
  implement") plus §10.3 ("Experimental values are private use … nothing in
  this format distinguishes them") and §10.4's registration requirement ("for a
  record type, its MU and PE assignment with justification"). The seam is a
  wording seam. Editorial.
- **writer-08** — verified: item 4 fixes one generation, a compactor's output
  is generation 1, so a compactor can be a profile writer; item 2 then derives
  the input's own file_id for an already-compact input, which `[R-WRT-06]`
  forbids in terms ("a new draw under §9.3's randomness advice, not merely a
  value compared against the input's"). Decidable (Appendix G non-normative);
  worth a sentence in item 2. Editorial.
- **verifier-01** — the operative trigger is factual in both rules ("Where the
  walk of §9.7 does not enumerate every region's claimants"), and §9.7 supplies
  the proof that a rejection need not stop the walk: "An entry `[R-IDX-03]`
  classifies reject-tile on a *structural* ground does not make the walk
  incomplete: the walk passes over it". The gloss "a scope-level rejection
  blocks enumeration" is what invites reading A. Partial: loose gloss, decided
  trigger. Nothing byte-level — both verifiers report *nonconforming*.
- **verifier-03** — decidable via §2.4 ("A file is conforming only if it
  satisfies every requirement at every scope … a verifier certifies only
  violation-free files") and §2.3 ("checks every file-level requirement —
  including those ordinary readers are exempted from"). The reporter says so
  himself. One clause in §9.7 or §17.4 removes the derivation.
- **diagrams-01** — verified against the tables: §6.1 is Offset|Size|Value|Class
  (no type, no name), §7.2 is Offset|Size|Type|Field|Class (no valid-range
  column). §4.7's note promises six columns; the front matter promises five and
  a different structural definition ("whether the file is accepted" vs "whether
  the file, layer or tile is accepted at all"). Both passages are non-normative.
  Editorial.
- **diagrams-02** — verified: `[R-VEC-02]` requires "the §21 register row it
  exercises"; §2.2's stability promise runs to `[R-…]` identifiers only, and
  §21.1 makes no promise about F/L/T/R numbering. Editorial.
- **diagrams-03** — verified: §7.3 gives 0x0002 one row, MU=0/PE=1, scope "file
  when top-level; layer as sub-record"; the rule says "both registered types
  carry PE = 1, so neither can be dropped"; Appendix H says "at either scope".
  §20.4's summary sentence undercounts. Editorial.
- **diagrams-06** — verified against §3.1 ("A tile is *stored in a generation*
  if and only if that generation's tile-index entry for it is not the sentinel
  … unqualified *stored* means stored in the live generation") and §20.3 step 4
  ("entries for tiles that become unstored written as the sentinel"). §23.2's
  "never stored" is wrong in the direction that matters for a privacy section.
  Editorial.
- **diagrams-07** — the paragraph's own parenthetical ("which carry no such
  prefix") is what undercuts the transitivity rescue; but the rescue is
  available and §21.9 disclaims inventory status. Partial, editorial.
- **diagrams-08** — verified: §20.3 shape (a) is "**(a) A new layer.** Nothing
  existing is rewritten", and §5.1's figure hatches only "the directories, pads
  and trailers of commits 1 and 2". The caption cites the layer-B commit as an
  instance of index re-emission at a new placement, which shape (a) denies.
  Figure defect.
- **diagrams-09** — verified by grep: the document's only hex dump is Appendix
  A's 128-byte layerless file; §12.3's twelve-byte channel entry is the only
  byte-level example of any part of a layer record. The §4.7 note's promise is
  unmet for the format's most intricate encoding. Editorial.
- **diagrams-10** — verified against Appendix B: it carries "Directory
  minimums" but no user-metadata extent floor of 5 (§7.1, F22/L11) and no bool
  byte encodings (§13.2 `[R-TYP-07]`, §14.2 `[R-SER-02]`); Appendix C is
  identifier assignments only. Editorial.
- **register-01** — verified: `[R-COD-07]`'s only reader MUST is the decoded-size
  cap (registered separately as L44); the zstd analogue `[R-COD-06]` *does*
  state the magic check a reader owes (T17). T13/T15/T16/T26 all carry "the
  check that detects it is …"; T23 does not. Register bookkeeping.
- **register-02** — verified from the cells: T3 enumerates six, T14 reads —;
  F33 enumerates five claimant families, F7 reads —. §21.1's criterion is
  applied in both directions. Register bookkeeping; corpus counts only
  (`[R-VEC-01]` makes the corpus derivative).
- **adversary-02** — decided by §2.4's ignore-record row ("The record is skipped
  as though absent") together with §21.6's entry ("A user-metadata record
  declares an experimental-range (≥ 0x80) document encoding | Ignored
  (ignore-record); the file is conforming") and §21.6's preamble ("A reader that
  treats any of them as a failure is the nonconforming party"). `[R-MTA-05]`
  has no subject where the specification defines no decoding, and *cannot
  establish* is for grounds that are "**that verifier's** capability" —
  `[R-MTA-09]` says so of its own bound ("the bound is that verifier's
  capability and not a limit on validity"). An unassigned encoding is no
  verifier's capability limit; no conforming implementation decodes it. Partial;
  a clarifying clause in §18.2 is cheap.
- **adversary-04** — the branch gap is real; `[R-CNT-02]`, `[R-CNF-08]` and F33's
  head clause ("claimed by two structures that do not belong to the same layer")
  all reach it and all give reject-file. No competing outcome exists. Editorial.
- **quiz-03** — §4.7's structural test is its four enumerated senses ("where a
  byte lies, how it decodes, what a decoded value is, or whether the file, layer
  or tile is accepted at all, which is the sense `[R-CNT-07]`, `[R-MTA-02]` and
  `[R-SEC-06]` already use"), and a compactor's copy-forward of version_minor is
  none of them; the descriptive limb speaks of decoding ("a reader MUST NOT
  alter decoding based on it"). Partial, editorial.

## Byte-level tally

0 of 34 findings, 0 of 24 groups. Six input findings carried a byte-level flag
(reader-01, writer-01, writer-02, writer-05, adversary-01, quiz-01); every
downgrade above is quoted. I record honestly that the deciding text is thinnest
for writer-05, then writer-02, then the appender cluster — and that in all three
the repair I recommend is worth making regardless of the grade.
