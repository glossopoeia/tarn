# Round 35 — triage pass: SKEPTIC

## Disclosure

Read only `/Users/robertkleffner/Documents/GitHub/tarn-first-draft/spec/tarn.md`,
by targeted `sed`/`grep` ranges. Sections opened in full or in part:
§2.3, §2.4 (head), §4.5, §4.7, §5.2, §6.1–§6.4, §7.1 tail ([R-CNT-25]),
§8.1, §8.2, §10.2–§10.4, §11.1–§11.3, §13.1–§13.2, §14.1, §14.4–§14.5,
§15.1–§15.3 (head), §16, §17.1–§17.4, §19.1–§19.3, §20.1–§20.5,
§21.1, §21.3 (selected rows), §21.4 (whole table), §21.5, §21.6, §21.7,
§21.8, §21.9, §22.3, §24 (head), Appendix G, Appendix H (head).
Row-level greps for F1–F17, L2, L18, L21, L23, L26, L31, L37, L38, L40–L42,
L48, F27, R1, R2.

I read NO walk transcript, NO other triage pass's notes, and ran NO directory
listing anywhere under the round's output tree. I did not open `docs/`,
`PLAN.md`, `AGENTS.md`, `conformance/`, `spec/registry.json`, git history or
the web. The only non-spec files I touched are this transcript and the
`wc -l`/`grep` of the spec itself.

No input finding was left unevaluated.

## The one uphold — [R-WRT-09] (verifier-02 + adversary-04)

Text:

> A compactor's verification depth follows reliance over everything it carries
> (`[R-WRT-03]`): it relies structurally on every structure it copies, so it
> MUST verify each link of the chain — the open (§19.1), each retained layer's
> record (§19.3) and full index chain (`[R-IDX-04]`), and each relocated
> extent's checksum, including every stored tile's entry crc — before emitting
> that structure's bytes. `[R-WRT-09]`

I tried to kill this group four ways and failed on the one that matters.

**Kill attempt 1 — "each link of the chain" is a defined term (§8.2) that
excludes a user-metadata extent's CRC.** §8.2: "The chain of trust is strictly
ordered: trailer → directory → (per layer) crc_of_crc_array → segment CRC
array → index segment → index entry → stored tile." A user-metadata extent's
CRC is not a link. FAILS: the em-dash list itself already reaches outside that
chain — "the open (§19.1)" and "each retained layer's record (§19.3)" are not
links of §8.2's chain either, and "each relocated extent's checksum" reaches a
user-metadata extent when it moves. So "the chain" here is not §8.2's closed
term; the apposition is the content.

**Kill attempt 2 — §19.2's extent tier forecloses it.** "at use of a record's
extent: that extent's CRC and the content rules of the document it carries …
before anything the extent holds is returned". A compactor returns nothing, so
no reader-tier obligation fires. FAILS as a foreclosure: §19.2 fixes the
*latest* point for violations a reader is obliged to detect; [R-WRT-09] is an
additional compactor obligation stated on top of the reader tiers, and §20.5
keys refusal to "any check `[R-WRT-09]` obliges", not to §19.2's tiers.

**Kill attempt 3 — [R-MTA-02] denies structural reliance on a document.**
Real, but it denies reliance on the *document*, not on the *extent*: the rule's
premise is quantified over "every structure it copies", and a record extent is
a structure ([R-CNT-02] names "a record extent … whatever the record's type").

**Kill attempt 4 — the disputed output is nonconforming anyway, so
[R-CNF-05] bars it under both readings** (verifier-02's own argument). This is
the one I most wanted to succeed, and the document refutes it in terms.
[R-WRT-01]: "An appender and a compactor satisfy every writer requirement for
the bytes they produce and the preservation obligations of §20.4 for what they
carry forward (`[R-CNF-06]`) — a violation latent in a structure they carry
forward unmodified travels with it, seen or unseen". §20.5 repeats it: "a
violation latent in a structure it carries forward verbatim travels into its
output (`[R-WRT-01]`)". So [R-CNF-05]'s "A writer MUST emit only conforming
files" is expressly *not* the rule for a compactor's carried-forward bytes;
verifier-02's downgrade rests on a premise the document contradicts.

With attempt 4 gone the fork is live and it is in the bytes:

- Input I: front [0,16); a top-level user-metadata extent at [16,116) whose
  terminal 4 bytes do not match CRC-32C of the preceding bytes (R2, PE = 1 so
  §20.4 licenses no drop); layer A's one stored tile [116,216); A's index
  region [216,300); directory; pad; trailer. No interior slack.
- Placement is the compactor's to choose (§20.5: "placement being the
  compactor's to choose"; "it is free to place structures anywhere §5.2
  admits"), so a placement that relocates nothing is available.
- Reading (E) — enumeration operative: no check reaches the unmoved extent;
  nothing is detected; §20.5's bar bites only on "a violation it has detected";
  the compactor emits O.
- Reading (P) — premise operative: the extent is a structure it copies, so it
  relies on it, so it verifies; the CRC fails; "A compactor MUST refuse to
  compact when any check `[R-WRT-09]` obliges fails". O is never written.

O is emittable by a conforming implementation under (E) and by none under (P).
No creator can emit O ([R-CNF-05], O being nonconforming) and no appender can
(fresh file_id, no slack). That is the byte-level test met.

**The sentence I looked for and did not find:** any sentence saying, in terms,
that a compactor owes no checksum verification on a structure it copies without
moving — or, equivalently, that the premise clause is justification rather than
obligation. [R-WRT-07]'s restatement closes the tile half only ("That
`[R-WRT-09]`'s checks reach the index chain and each stored tile's entry crc
rather than an entry's own value domain bounds how far a compactor goes
looking"), dropping the "relocated" qualifier for tiles and saying nothing
about non-tile extents. §20.5's figure commentary settles only which index
regions are regenerated.

**Premise my uphold rests on, stated for attack:** that a compaction leaving
every structure at its input offset is available — i.e. that "relocated" has a
non-empty complement in a real compaction. If some rule forces every structure
to move (I found none; §20.5 says the opposite), the fork collapses. Second
premise: that a user-metadata record with PE = 1 cannot be dropped, so the
compactor's only disposals are refuse or carry.

**Repair:** decide it in the rule. Either quantify the obligation over
everything copied — "each copied extent's checksum, whether or not the output
relocates it" — or narrow the premise to match the enumeration ("it relies
structurally on every structure whose bytes the output's own offsets depend on")
and say expressly that an unmoved non-tile extent's checksum is not owed.

## Groups where the document decides it (downgrades, with the deciding text)

**quiz-01 — REFUTED.** The reporter says the resolution "has to be supplied by
the reader from a clause two sentences earlier". It is in the *same sentence*:
"A layer that stores a tile **in the generation this commit supersedes** keeps
its declarations, with these exceptions and no other: its name … MAY change; a
dimension extent MAY grow …; a planar layer's channel list MAY be extended …;
and a slab or alignment declaration MAY be declared, changed or cleared as this
step provides below." "keeps its declarations" is the head of the colon-list of
which the fifth member is the last item. Keeping is the stated baseline;
reading (B) is foreclosed by the clause introducing the list it misreads.

**quiz-04 — REFUTED.** Two deciding texts. §21.9: "*Decoded size of one tile*
ranges over a layer's **addressed** tiles" — the quantity is a tile's, so
[R-ERR-04]'s own quantifier ("the narrowest scope whose stated or derived
quantities exceed what it can serve") picks the tile. And even granting (B),
[R-ERR-04] adds "It MAY also decline at any scope that contains the narrowest
one", so the two readings license exactly the same set of behaviours. Nothing
turns on it.

**quiz-03 — PARTIAL (verifier half refuted).** The gloss is definitional, and
the sentence says so: "determines anything a conforming reader or verifier does
with the bytes it reads — where a byte lies, how it decodes, what a decoded
value is, or whether the file, layer or tile is accepted at all, **which is the
sense `[R-CNT-07]`, `[R-MTA-02]` and `[R-SEC-06]` already use**." A [R-CNF-12]
advisory on a [R-CNT-26] SHOULD is none of the four. What survives is the
reporter's second, smaller point: "each class being what the one before it is
not" names nothing for **structural**, the first of the two classes.

**writer-01 — PARTIAL (reading 1 refuted).** The asymmetry the reporter leans
on runs the other way. The same sentence glosses the generic word with the two
specifics: "save where alignment forces a gap — a declared A or A_slab, or
§6.2's 64-byte trailer alignment". "Alignment" is used in this sentence as the
genus of which A and A_slab are the species, so the earlier "a declared
alignment" covers A_slab and no L42 file is instructed. The non-tile half
survives: [R-SLB-01] binds "every stored tile's offset" and [R-SLB-03] "the
first stored tile's offset", so neither constrains a leading tile-index region,
and item 3's "admits no structure at 16" has no truth value there.

**writer-03 — PARTIAL.** Class 1's own words assign the case: "entries for
tiles this commit stores or supersedes written to their new state". A tile
going sentinel → stored is a tile this commit stores, so it is class 1 and
"added tiles" cannot mean it without contradiction. A wording wart, not a
straddle.

**register-04 — PARTIAL.** The circularity is looser than reported. [R-CNF-13]'s
criterion is stated before the pointer — "one malformed state, as §21.1
individuates them" — and §21.1 supplies row-independent principles: "Conditions
attach to the finest structure they damage", the strict-specialization rule, and
the Instances rules ("An instance names a field the condition ranges over, a
container it can occur in, one of several alternatives the condition text
states"). And §21.7's illustration is derivable from the requirement rather than
the rows: §6.2's ordered list, minus the version gate ([R-CNT-07]) and the flag
gates ([R-CNT-08]), states exactly nine — magic, trailer CRC,
committed_file_length = file size, its multiple of 64, dir_offset ≥ 16,
dir_length ≥ 4, dir_offset + dir_length ≤ F − 64, file_id ≠ 0, reserved zero.
So the completeness clause is not vacuous. The three-hop wording still deserves
one substantive sentence.

**register-02 — PARTIAL.** §21.1 defines the parenthetical convention for "A
Governing rule cell", and says of §21.6 that its subsections "are not part of
the register and carry no rows". §21.6's column is headed "Rule", not
"Governing rule". "where such an entry and the rule it cites diverge, the rule
governs there too" reads distributively over the cited rules — for whichever
cited rule the gloss diverges from, that rule wins — which answers both the
"no referent" and the "first-named picks the wrong rule" complaints. What
survives is that exactly one entry (zero layers) uses the register's
parenthetical form while fourteen use comma lists; normalize.

**register-01 — PARTIAL.** [R-CNT-25]'s trigger list is genuinely four items
and several R4 instances leave the document readable — §21.5 itself concedes
"several, the content-size field among them, are broken by what the frame
declares while the bytes decode". But the same §21.1 sentence names
"`[R-MTA-09]` for the frame constraints R4 registers", and §21.5's preamble
carries the outcome for the whole section. Nothing is left undetermined.

## Non-byte-level downgrades, deciding quotes

- **reader-01 / verifier-01 (T17).** The defect is real — T17's Detector is
  *reader*, Detected *tile use*, Governing rule [R-COD-06], with no "the check
  that detects it is T24's or T25's" routing (contrast T15, T16, T23), so a
  reader detects a 1→3 re-declaration at T17, not at T24 or T25. Not byte-level
  on the step's own words: "This bar binds the commit as an actor: no file is
  nonconforming by virtue of its violation, and no register row records the
  violation itself". T17 is a row every conforming reader applies whether or not
  the sentence lists it.
- **verifier-03.** Real: §17 owns the codec and the filter — "A stored tile's
  bytes are produced from its decoded tile image (§14) by two per-tile stages"
  — and the gloss names only §14, §11.4 and §15. Decided by the operative list
  two paragraphs above: "the layout, the linearization and the index encoding,
  **the codec and the filter**, the rank and the dimension order…".
- **reader-02.** Real: [R-CNT-06] hangs the parenthetical "(for a remote reader,
  the size reported by its transport)" on the classification and [R-CNT-10]
  hangs four MUSTs on it, so "and nothing else" overshoots. Not byte-level:
  [R-CNT-06] requires of every reader that committed_file_length "equals the
  file size … Any failure is reject-file"; comparing the field against itself
  performs no such check under either label, so F17 stays reader-detected for
  both.
- **writer-04.** Real: [R-CNT-02] — "belongs to exactly one of: the front
  signature block; **or** a structure". Not byte-level: §9.7 names the walk's
  claimants — "the directory itself, each record's extent, and the stored extent
  of each non-sentinel tile-index entry" — and the slack total follows from
  that, not from §22.3's wording. Note the document is already two-voiced:
  §8.1's table heads its first column "Structure" with "Front signature block"
  as its first row.
- **writer-02, adversary-01, writer-01.** Appendix G opens "It adds no
  requirement to any actor: a writer ignoring it is fully conforming."
- **register-03.** §21.1: "where a row and the rule it cites diverge, **the
  rule governs**." Verified the inconsistency by hand: L2 cites (R-GEO-03,
  R-CNT-13, R-SER-02, R-SER-07) while L21, whose condition reads
  [R-GEO-03]'s addressed-tile count in terms, cites only (R-CNT-20); F27 and
  L48 cite (R-CNF-05) though [R-CNT-25] is what places their scope, naming them
  by label; F14 cites R-ENC-09 while F20, L37 and L38 cite R-ENC-10 and R2
  cites neither.
- **register-05.** Verified verbatim: "…rather than serving it through, which is
  why `[R-TYP-04]` (§12.3) makes it the one case where a reader resolves a byte
  to a sample value rather than serving it through". A true tautology.
- **register-06.** Verified: §15.1's only mention is "Under index_encoding 1
  (the only encoding this format major version defines, §7.4)" — no set, no
  reserved range, no outcome — while §14.1 does state the layout set via
  [R-SER-06] and §17.2/§17.3 state theirs. §7.4's row states the whole set and
  L31's cell cites §7.4 correctly.
- **adversary-02.** Verified: the flag lanes are absent from §10.2's eight-row
  table, which the preceding sentence introduces as "The spaces … collected
  here", while the closing sentence calls them a space. §6.3 states the lane
  rules directly, so nothing operational moves.
- **adversary-03.** Real under §21.1's own test: "One instance is one
  *distinguishable* file … because no two files could differ" — here two files
  plainly differ, and differ in detection tier and in effect on F4. Not
  byte-level: §19.1 step 4 states the behaviour normatively and [R-VEC-01] makes
  the corpus derivative — "where a vector's recorded expectation and this
  specification disagree, this specification governs". Repair changes §21.8's
  277 to 278.
- **adversary-05.** Real over-assertion; [R-CNT-10] provides for it and §6.4's
  Note says "no request count is a conformance property".
- **adversary-06.** Real terminological split (§4.7 Note puts the prefix inside
  the value; §13.1 puts it in "§7.4's framing"). Decided for every operative
  purpose by [R-ENC-16]: "In format major 1 `version_minor` is the only
  descriptive field, and every other field this specification defines is
  structural."
- **quiz-02.** The block's own opening defers: "§20.3 states normatively, and
  governs, what a commit may do to a layer that already stored tiles". And
  because the restatement drops "with these exceptions and no other", it states
  permissions without closure, so a kept declaration is not prohibited by it —
  the gap is an under-statement, not a trap.

## Groups I tried hardest to kill and failed

1. [R-WRT-09] (verifier-02 + adversary-04) — failed, and upgraded to byte-level.
2. reader-01/verifier-01's T17 omission — failed to refute the defect (T17 is
   genuinely a reader-owed check outside T24/T25); succeeded only on byte-level.
3. register-03's parenthetical inconsistency — failed; the four disagreements
   are verifiable row by row.
4. register-06's §15.1 pointer — failed; §15.1 really states no value set.
