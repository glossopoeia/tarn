# Triage pass — implementer consequence — cleanroom round 35

## What I read

Only `/Users/robertkleffner/Documents/GitHub/tarn-first-draft/spec/tarn.md`, by
`sed -n` over line ranges and by `grep -n`, plus `wc`. I did not open any walk
transcript, did not list any directory under `r35-round/out`, and did not read
`docs/`, `PLAN.md`, `AGENTS.md`, `conformance/`, `spec/registry.json`, git
history or the web.

Ranges read: §2.3–2.5 (152–350), §3.2 (412–442), §4.5 (510–548), §4.7 (594–632),
§5.2 (697–782), §6 (780–960), §7.1 (962–1000), §7.4 (1104–1216), §8 (1216–1260),
§9.7 (1490–1546), §10 (1547–1636), §11.1–11.4 (1640–1730), §12.3 (1849–1878),
§13.1–13.3 (1876–1930), §14.1–14.5 (1984–2015, 2115–2150), §15.1–15.4
(2179–2260), §16 (2303–2410), §18.1–18.2 (2617–2650, 2690–2740), §19 (2889–3110),
§20 (3107–3641), §21 (3643–4145), §22.3 (4180–4230), Appendix G (4609–4780),
plus targeted greps of §21.2/§21.3 rows.

## Grouping

22 groups over the 25 input ids. Three merges:

- `reader-01` + `verifier-01` — both say the second parenthetical of §20.3
  step 4's "no check any actor owes able to see it" sentence, `(T24, T25)`,
  omits T17. Same sentence, same omitted row, same argument from the first
  parenthetical's exactness.
- `verifier-02` + `adversary-04` — both say [R-WRT-09]'s premise ("every
  structure it copies") is wider than its enumeration ("each relocated
  extent's checksum"). adversary-04 additionally builds the divergence.
- `quiz-01` + `quiz-02` — one reporter splitting one claim ("the slab/alignment
  member enumerates three dispositions and does not name *kept*") across its
  normative statement in §20.3 step 4 and its restatement in §11.1's Rationale.
  One coordinated repair fixes both.

`verifier-03` is kept apart from the T17 group: it is a different sentence
(the fixed-declarations gloss) and a different omission (codec and filter,
which §17 owns).

`writer-02` and `adversary-01` both concern Appendix G item 5 but are separate
defects — one attacks item 5's stated justification, the other attacks the
closing paragraph's failure to restate item 5's pins.

`adversary-06` and `quiz-03` both concern §4.7 but are separate defects — the
length prefix's membership in "value" versus the widening of the structural
test to "or verifier".

## The one byte-level uphold: [R-WRT-09]'s quantifier

The sentence, §20.5:

> A compactor's verification depth follows reliance over everything it carries
> (`[R-WRT-03]`): it relies structurally on every structure it copies, so it
> MUST verify each link of the chain — the open (§19.1), each retained layer's
> record (§19.3) and full index chain (`[R-IDX-04]`), and each relocated
> extent's checksum, including every stored tile's entry crc — before emitting
> that structure's bytes. `[R-WRT-09]`

The tile half is closed by [R-WRT-07]'s restatement, which drops the qualifier:
"That `[R-WRT-09]`'s checks reach the index chain and each stored tile's entry
crc rather than an entry's own value domain bounds how far a compactor goes
looking". Layer records are already unqualified in the list. The gap is exactly
a **user-metadata extent the compactor does not move**.

That case is live in the document's own words: "In this placement A's stored
extents happen not to move, so A's index is copied and only its slot
re-pointed; under a placement that moved them it would be regenerated too,
placement being the compactor's to choose."

Nothing else supplies the obligation. §20.5 opens: "its verification depth is
`[R-WRT-09]`'s and reaches no decoded content." §19.2's extent tier is keyed to
returning: "at use of a record's extent: that extent's CRC ... before anything
the extent holds is returned", and [R-RDR-02] adds "Structures a request never
relies on impose no detection obligation beyond the open steps" — a compactor
that copies an extent without reading its document returns nothing it holds.
§8.2's chain of trust does not contain a user-metadata extent CRC either
(trailer → directory → crc_of_crc_array → segment CRC array → index segment →
index entry → stored tile), so "each link of the chain" cannot be read to
supply it; [R-WRT-09]'s own list is what reaches beyond that chain, and its
reach is the disputed word.

### The divergence, both sides

Input I, nonconforming on R2 alone (a top-level user-metadata extent whose
final 4 bytes are not the CRC-32C of the preceding bytes), with slack after
that extent so compaction is worth running.

- **Compactor X** (em-dash list is the obligation) chooses a placement leaving
  the metadata extent at its input offset, moves the tiles, verifies the open,
  the layer records, the index chains, every stored tile's entry crc and every
  *relocated* extent's checksum. Everything it checks passes. It mints a fresh
  file_id and emits **O**.
- **Compactor Y** (reliance premise is the obligation) verifies the copied
  metadata extent's CRC, the check fails, and §20.5's "A compactor MUST refuse
  to compact when any check `[R-WRT-09]` obliges fails" makes it **refuse**.

O is a byte sequence X may emit and Y may not.

### The premise my uphold rests on, stated so it can be attacked

**Premise: a conforming compactor may emit a nonconforming output where the
violation is latent in a structure it carried forward and it detected
nothing.** If that premise is false — if [R-CNF-05]'s "A writer MUST emit only
conforming files" binds a compactor's whole output — then O is barred under
both readings and this drops to editorial. That is exactly the move
`verifier-02` makes. Three sentences say the premise is true:

1. §20.1: "A creator emits only conforming files (`[R-CNF-05]`). An appender
   and a compactor satisfy every writer requirement for the bytes they produce
   ... — a violation latent in a structure they carry forward unmodified
   travels with it, seen or unseen, and certifying the whole file is a
   verifier's office". [R-CNF-05] is attributed to the creator and the other
   rule to the compactor, in one paragraph, deliberately.
2. §20.5: "**Given a conforming input** the output is a conforming file." The
   conditional is idle unless a nonconforming input may yield a nonconforming
   output.
3. §20.5: "MUST NOT emit a file carrying a violation **it has detected**" —
   detection-keyed, not existence-keyed.

**Second premise: reading (P) is genuinely available.** Grammar favours (E) —
"so it MUST verify [list]" is the operative clause. But the premise clause is
stated as the derivation and cites [R-WRT-03], whose own closing sentence is
"Structures the commit neither modifies nor relies on impose no further
obligation" — i.e. structures it *does* rely on do impose one, and [R-WRT-09]
asserts flatly that a compactor "relies structurally on every structure it
copies". And the trailing "before emitting **that structure's** bytes" is
singular and per-structure, reaching everything the compactor emits. Two
reporters found the same ambiguity independently.

I therefore grade this byte-level. It is the only one in the set.

## Downgrades, each with the sentence that decides it

**T17 / `(T24, T25)` (reader-01, verifier-01).** The omission is real: T17 is
[R-COD-06]'s magic check, performed before any decode; a codec re-declared to 3
over raw or deflate bytes fires T17, not T24 (bytes remaining after a stream
that was never recognised) and not T25 (a malformed stream that fails to
decode). Unlike T15, T16 and T23, T17's condition cell carries no "the check
that detects it is T24's or T25's" routing. I checked the first parenthetical
and it is exact: decoded size is exactly T3, T14, T21, T22; T4 is the padding
position; T5 the pad bit; T2 the boolean byte.

Not byte-level. What decides it:

> This bar binds the commit as an actor: no file is nonconforming by virtue of
> its violation, and no register row records the violation itself, the register
> enumerating file-conformance violations (§21.1) and the bar stating no
> condition a file can exhibit (§21.7, `[R-ERR-01]`, `[R-CNF-02]`)

and, for the implementer question specifically, §19's own preamble:

> Those enumerations are not the complete inventory of what a reader detects at
> that tier: §21's register is, and `[R-CNF-04]` binds a reader to every
> register row whose detector is the reader, at the tier that row's *Detected*
> cell names (§21.1). A row this section does not restate is due at its own tier
> all the same, with its governing rule's own outcome.

A reader's check set comes from the register, never from this parenthetical, so
no reader emits, accepts or rejects differently. The document decides it; it is
not merely a matter the ledger asks about.

**Fixed-declarations gloss (verifier-03).** Real: the gloss reaches §14, §11.4
and §15 and not §17. What decides it is the operative list two paragraphs above
in the same step:

> Every other declaration is fixed for as long as the layer stores a tile: the
> layout, the linearization and the index encoding, the codec and the filter,
> the rank and the dimension order, every tile extent, every channel's type and
> fill, an interleaved layer's channel list (its names aside), and the position
> of every planar channel the new state keeps.

plus the very next clause after the gloss, "a decode that fails outright under a
changed codec or filter". §21.1's principle that the rule governs a divergent
restatement applies a fortiori to a gloss inside the same step as the rule.

**§6.1's "and nothing else" (reader-02).** The over-claim is real — [R-CNT-10]
hangs four MUSTs on the classification and [R-CNT-06] uses it in §6.2, outside
§6.4 entirely. What decides the byte question is §19.1 step 1, which imposes
the obligation on **every** reader with no classification predicate:

> **End of file.** Obtain the transport-authoritative file size F
> (`[R-CNT-10]`)

together with [R-CNT-06]'s unconditional "committed_file_length equals the file
size". A reader that substitutes committed_file_length for the transport size
is nonconforming whatever it calls itself, so F17's detection does not move with
the label and no byte sequence changes status.

**Suffix range carries F (adversary-05).** Same decider. §19.1 step 1's
operative sentence cites [R-CNT-10]; the "steps 1 and 2 cost one request between
them" claim is prefaced by "These steps are ordered by dependency, not by I/O",
and §6.4's Note says "no request count is a conformance property, and nothing
here bounds what a reader fetches." [R-CNT-09]'s own sentence carries the
`[R-CNT-10]` citation inline at the exact clause. Over-broad wording, no fork.

**§22.3's structure universal (writer-04).** Real: [R-CNT-02] reads "belongs to
exactly one of: the front signature block; **or** a **structure** — a
stored-tile extent, a record extent ..., the directory, or the trailer." What
decides it is §9.7, which is where the walk is actually specified and which
names the front block by hand:

> The front signature block at [0, 16) and the live trailer at [F − 64, F) are
> claimed by the walk as well, being members of the live committed state
> (`[R-CNT-02]`)

A verifier built from §9.7 gets the claimants and the slack total right either
way.

**Appendix G items 3 and 5, and the closing inventory (writer-01, writer-02,
adversary-01).** All three are inside a body that disclaims normativity:

> It adds no requirement to any actor: a writer ignoring it is fully
> conforming

writer-01's reading 1 would have the profile prescribe a file exhibiting L42;
that file is barred to every conforming writer by [R-SLB-03] under both
readings, so the conforming-emittable set does not move. writer-01's non-tile
half and adversary-01's omissions produce two files that are both conforming and
both already permitted by "two conforming writers given identical input MAY
produce different conforming files" ([R-CNF-05]) and by [R-SLB-05]'s placement
freedom. writer-02's finding is verified against §14.4's Note ("A single-channel
numeric layer produces byte-identical tile images under either layout") and
[R-GEO-03] (N interleaved, C·N planar, equal at C = 1) — both stated mechanisms
are inoperative at C = 1 — but both layout values are conforming under
[R-SER-06]. For adversary-01 I note the hedge is stronger than the reporter
allows: "**Read the numbered items as the list**; this paragraph names what they
are for, not how many there are" tells the reader in terms that the paragraph is
not the list, which is why I grade that one PARTIAL.

**"added tiles" (writer-03).** [R-IDX-01] settles that every addressed tile has
an entry in every generation — "The entry for the tile with disk ordinal k
(§11.4) is the k-th entry, at region byte 20·k" — so a tile going
unstored→stored occupies an entry that already existed. The partition claim is
damaged; the bytes are not: §15 prescribes the same 20 bytes (offset, length,
crc) whichever class routes the entry.

**Register bookkeeping (register-01, -02, -03, adversary-03).** Verified each
against the rows:
- register-01: [R-CNT-25]'s quarantine trigger is closed — "a failed extent
  CRC, an unimplemented or invalid encoding, a decode failure, or content
  violating the document's own rules" — and §18.2 says of R4's content-size
  instance that "the bytes decode, and what is wrong is what the header said
  about them", so the document is readable and none of the four ways is met.
  §21.1's "every §21.5 row" over-reaches. Decided for outcome purposes by
  [R-MTA-09]'s own closing sentence: "Any violation here is ignore-record,
  never the tile-scope outcome §17.2 assigns", and by §21.5's outcome heading.
- register-02: I counted the column myself. Fifteen entries: eight cite a single
  rule, six cite an undifferentiated comma list, exactly one (zero layers) uses
  the register's parenthetical form. The reporter's "fourteen ... comma list" is
  wrong on the count. The reporter's supporting claim that first-named picks a
  rule silent on the behaviour does not hold either: [R-IDX-02] does state
  "A sentinel tile contributes fill to the reference array (§3.2, §13)", and
  §19.4 step 1 cites [R-MDL-01] for exactly "a coordinate outside the extents
  addresses nothing in the reference array". Hence PARTIAL. The convention
  mismatch itself is real.
- register-03: verified all four groups. L2's last instance is
  "entry_count × 20 + ⌈entry_count/2¹⁶⌉ × 4" and [R-CNT-17] is the rule that
  designates it ("that expression being a declaration-derived quantity under
  `[R-ENC-04]`") and is uncited. L21's condition names the geometry-derived
  count [R-GEO-03] defines and cites [R-CNT-17] (R-CNT-20). F27/L48 cite
  [R-MTA-05] (R-CNF-05) while [R-CNT-25] is what places the defect at the
  file or the layer. F14 cites R-ENC-09 (the CRC-32C *definition*) where
  F20/L37/L38/T1 cite R-ENC-10 (the verify-before-acting rule) and R2 cites
  neither. Inconsistent. Decided for verdicts by §21.1's "where a row and the
  rule it cites diverge, **the rule governs**".
- adversary-03: verified L23's cells against R1's. L23 Detected splits inside
  its first instance; R1's four instances match its two detection points. §19.1
  step 4 states the name-truncation consequence normatively ("yields no name
  field to compare, so it contributes no name to the namespace and is instead a
  validity error at layer scope (`[R-CNT-18]`)"), so the cost falls on the
  corpus, and [R-VEC-01]'s "A missing vector is a gap in the corpus and never a
  licence to skip the check it would have exercised" bounds it.

**register-04 (individuation).** The chain is exactly as reported: §21.7 "as
`[R-CNF-13]` individuates them"; [R-CNF-13] "one malformed state, as §21.1
individuates them"; §21.1 "each row is one malformed condition". §21.7 forbids
the same move for detectability in terms — "a test keyed to the rows would make
§21.1's completeness clause vacuous, every omitted condition being undetectable
by construction" — and does not close the parallel hole for individuation. This
is a real gap in the document's self-audit machinery and needs a maintainer's
decision, not a wording tweak. No file's status turns on how conditions are
counted.

**register-05 (tautology).** Verified verbatim: "it resolves a nonconforming
interleaved boolean byte to a sample value rather than serving it through, which
is why `[R-TYP-04]` (§12.3) makes it the one case where a reader resolves a byte
to a sample value rather than serving it through." [R-TYP-04] states the
behaviour itself — "the one case where a reader resolves a byte to a value
rather than passing it through arises only in a nonconforming file, and
`[R-SER-08]` states it" — so nothing a reader returns turns on the gloss.

**register-06 (§15.1 value set).** Verified. §15.1's only mention is "Under
index_encoding 1 (the only encoding this format major version defines, §7.4)",
which points at §7.4; §7.4's row states the whole set and the outcome. Both
[R-EXT-03] and [R-RDR-03] list §15.1 among "the value sets of". §10.2's table
hedges with "index encoding (§7.4, §15.1)". A reader following the wrong pointer
lands one hop from the set and reaches the same layer-scope outcome.

**adversary-02 ([R-EXT-02]).** Verified: the table between the two sentences
collects eight spaces and the flag lanes are not among them; §6.3 partitions
them into an incompat lane and an ignore lane, not into
assigned/reserved/experimental. The downstream count in §20.5 uses the table
("one row for each of the other seven spaces §10.2 tabulates (L31, L33, L34,
L36, L43, L45, R1)"). What decides the byte question is [R-CNT-08], which states
the lane rules directly: "a reader MUST reject-file on any set bit it does not
implement in the incompat lane (bits 0–15), and MUST ignore all bits in the
ignore lane (bits 16–31)."

**adversary-06 and quiz-03 (§4.7).** Both real prose defects. adversary-06: the
§4.7 Note's "A variable-length field's value includes its length prefix" is at
odds with §13.1's "though it never affects how any byte is located or decoded;
the field's length prefix is §7.4's framing". Decided by [R-ENC-16]'s own
closing sentence — "In format major 1 `version_minor` is the only descriptive
field, and every other field this specification defines is structural" — so the
taxonomy question has one answer whichever way the prefix is assigned, and
[R-CNT-23]'s cross-check of the fill prefix against the element size fixes the
parse. quiz-03: the widening to "or verifier" does put [R-CNF-12]'s SHOULD
advisory in reach, but the em-dash gloss reads as definitional ("which is the
sense `[R-CNT-07]`, `[R-MTA-02]` and `[R-SEC-06]` already use"), and [R-CNT-07]
settles the bytes: "A reader MUST NOT reject a file for its version_minor."
The "each class being what the one before it is not" infelicity (structural has
no predecessor) is real and separate but equally inert.

**quiz-04 (narrowest scope).** [R-ERR-04]'s enumeration names both "a layer, a
tile", §21.9's per-instance paragraph says the tile row "ranges over a layer's
**addressed** tiles", and the rule then adds "It MAY also decline at any scope
that contains the narrowest one". Both readings' permitted behaviours are
licensed, and "A file exceeding any of these remains conforming" fixes the
file's status. Contrast §21.6, which names the narrowest scope expressly for a
document ("the narrowest-scope decline `[R-ERR-04]` names for a document") and
does not for a tile — that asymmetry is the actual defect.

**quiz-01 + quiz-02 (kept slab declaration).** The §20.3 member's three verbs
are closed in situ by the clause that introduces the list:

> A layer that stores a tile **in the generation this commit supersedes** keeps
> its declarations, with these exceptions and no other

Keeping is the baseline, not an exception, so the member is complete and reading
(B) is refuted. §20.3's own later clause contemplates keeping —
"a slab declaration declared, changed or kept has its invariants satisfied over
every run of the new state ... or is cleared" — which is where the fourth
disposition comes from. §11.1 carries the label *Rationale*, defers ("§20.3
states normatively, and governs"), and permission is the default absent a bar,
so an updater has nothing to refuse. Real mismatch between two enumerations of
one subject in one step; the consequence the reporter names does not follow.
PARTIAL.

## Coverage

25 input ids, 22 groups, each id in exactly one group. Counted by hand against
the brief's id list: reader-01, reader-02, writer-01, writer-02, writer-03,
writer-04, verifier-01, verifier-02, verifier-03, register-01, register-02,
register-03, register-04, register-05, register-06, adversary-01, adversary-02,
adversary-03, adversary-04, adversary-05, adversary-06, quiz-01, quiz-02,
quiz-03, quiz-04. Group sizes: three groups of 2 (T17, compactor, kept-slab),
nineteen of 1 → 6 + 19 = 25.

## Gap I am declaring

I cannot say whether any group here is *new* relative to earlier rounds' ledger:
I am barred from `docs/`, git history and prior transcripts, so every downgrade
above is stated as "the document decides it" and none as "the ledger already
asks it". If the reconciler needs the novelty axis, it has to come from
elsewhere.
