# Triage pass — correctness lens — cleanroom round 35

## What I read

`/Users/robertkleffner/Documents/GitHub/tarn-first-draft/spec/tarn.md` only, in
sections: heading map; §2.1–§2.5; §3.1–§3.2; §4.5, §4.6 (partial), §4.7; §5.2;
§6.1–§6.4; §7.1 ([R-CNT-25]), §7.4 ([R-CNT-16], [R-CNT-17], [R-CNT-23]); §8.1,
§8.2; §9.7; §10.2–§10.4; §11.1–§11.3; §12.3; §13.1–§13.3 (partial); §14 intro,
§14.1, §14.4; §15.1–§15.4; §16, §16.1, §16.2; §17.1, §17.2 (partial); §18.2
(partial); §19.1–§19.4 (partial); §20.1–§20.5; §21.1–§21.9; §22.3; Appendix G.

I did NOT open any walk transcript, any quiz transcript, any other triage
pass's notes, `docs/`, `PLAN.md`, `AGENTS.md`, `conformance/`,
`spec/registry.json`, git history, or the web. I ran no directory listing of
the round's output directory; every file I touched I named directly. The only
shell commands were `wc -l`, `grep -n`, `sed -n` against `spec/tarn.md`, plus
the `mkdir`/`cat` that wrote this file.

## Grouping

23 groups over 25 ids. Two groups have two members each:

- `t17-omitted-from-changed-codec-witnesses` = {reader-01, verifier-01}: same
  sentence, same omitted row, same argument.
- `compactor-copies-vs-relocated` = {verifier-02, adversary-04}: same sentence,
  same premise/enumeration mismatch. verifier-02 frames it as tiles + non-tile;
  adversary-04 shows the tile half is closed by [R-WRT-07]'s restatement and
  builds the non-tile construction. One defect, one repair.

quiz-01 and quiz-02 touch the same subject (the "kept" disposition of a slab
declaration) but different text with different repairs (§20.3 step 4's fifth
member vs §11.1's Rationale), so they are separate groups.
verifier-03 is the sentence immediately before the reader-01/verifier-01
sentence but a different defect (which sections are said to own the fixed
declarations), so it is its own group.

## Findings checked against the text

### 1. T17 (reader-01, verifier-01) — CONFIRMED, not byte-level

Quotation verified verbatim at §20.3 step 4. §21.4 verified: T17 is
"Codec 3 (zstd) and the stored bytes do not begin with the compressed-frame
magic 28 B5 2F FD | — | reader | tile use | `[R-COD-06]`". T15, T16, T23 and
T13 all carry "the check that detects it is T24's or T25's" in their condition
cells; T17, T18, T19, T20 carry no such routing. The first parenthetical is in
fact exhaustive: grepping the tile rows, the decoded-size witnesses are exactly
T3, T14, T21, T22, and T4/T5/T2 are exactly the padding-position, pad-bit and
interleaved-bool rows. So the reporters' reading (a) is the natural one and the
sentence understates its own witnesses.

Byte-level: no. Two decisive sentences.
(i) §20.3 step 4: "This bar binds the commit as an actor: no file is
nonconforming by virtue of its violation, and no register row records the
violation itself, the register enumerating file-conformance violations (§21.1)
and the bar stating no condition a file can exhibit".
(ii) [R-CNF-04]: "A reader MUST detect every violation the error register (§21)
assigns to the reader as its detector" — T17's detection comes from the
register, not from this parenthetical.
Premise of my downgrade, stated for attack: no rule anywhere makes any actor's
obligation turn on this parenthetical; it enumerates witnesses for an argument.
I checked the two candidate routes — [R-CNF-04] (register-driven) and §19.2
(tier-driven) — and neither passes through §20.3 step 4's list.

### 2. verifier-03 — CONFIRMED, not byte-level

Verified: §14 opens "This section defines the **decoded tile image**: the byte
sequence a stored tile's payload decodes to under §17's codec pipeline" — so
§14 does not own the codec or the filter; §17.1 does ("A stored tile's bytes
are produced from its decoded tile image (§14) by two per-tile stages"). The
gloss's three sections (§14, §11.4, §15) therefore miss codec and filter.

Byte-level: no. The operative list two paragraphs earlier decides it: "Every
other declaration is fixed for as long as the layer stores a tile: the layout,
the linearization and the index encoding, **the codec and the filter**, the
rank and the dimension order, ...". A gloss narrower than the rule it glosses
creates no permission; the next clause ("a changed codec or filter") confirms
the intent. Distinguish this from group 8: there the two formulations sit in one
sentence with no operative/explanatory hierarchy between them.

### 3. reader-02 — CONFIRMED, not byte-level

Verified: §6.1 says "That distinction governs the request accounting of §6.4
and nothing else". [R-CNT-06] (§6.2) uses it: "committed_file_length equals the
file size (for a remote reader, the size reported by its transport)".
[R-CNT-10] (§6.4) hangs four MUSTs and a SHOULD on "a remote reader", none of
which is a request count. So "and nothing else" is false as to [R-CNT-06],
which is not even in §6.4.

Byte-level: no. [R-CNT-06]'s check is unconditional over every reader —
"committed_file_length equals the file size" — so no reader may compare the
field against itself whatever it calls its transport; F17 is reader-detected at
open for both classifications. Reporter's own rationale is right.

### 4. writer-01 — CONFIRMED, not byte-level

Verified [R-SLB-01] binds "every stored tile's offset satisfies offset mod
A = 0"; [R-SLB-03] binds "the run's stored tiles" and "the first stored tile's
offset satisfies offset mod A_slab = 0". Neither reaches a non-tile structure.

On the A-vs-A_slab reading: the same sentence's later clause uses "alignment"
generically and glosses it — "save where alignment forces a gap — a declared A
or A_slab, or §6.2's 64-byte trailer alignment" — which favours reading 2. But
elsewhere in the same appendix "declared alignment" contrasts with "slab"
(item 5: "**No declared alignment and no slab**"; closing paragraph: "a declared
alignment and slab"), so reading 1 is available on the appendix's own usage.
That is enough for a naming fix.

On the second half: I do not think the words fork. Where the first structure is
a tile-index region, a declared A or A_slab does not bar it from offset 16
(neither rule speaks about it), so the declaration "admits" a structure at 16
and the first branch applies — determinate. The residue is that "where a
declared alignment admits no structure at 16" is loose about which structures a
declaration reaches. Same clause, same repair, so one group.

Byte-level: no. Appendix G's own opening: "It adds no requirement to any actor:
a writer ignoring it is fully conforming." Reading 1's output violates
[R-SLB-03] and is barred for a creator by [R-CNF-05]'s "A writer MUST emit only
conforming files" under both readings.

### 5. writer-02 — PARTIAL, not byte-level

Both cited facts check out: [R-GEO-03] gives "N for an interleaved layer and
C · N for a planar layer", equal at C = 1; §14.4's Note says "A single-channel
numeric layer produces byte-identical tile images under either layout."

But the item's claim is "Without both pinned, two writers agreeing on everything
above still disagree on bytes", and that claim stays TRUE at C = 1 numeric —
the layer record's own layout field holds 1 or 2. So the reason is not "false";
it is non-discriminating in that case and the justification omits the residual
mechanism. PARTIAL: real defect is an incomplete justification, not a
contradiction.

Byte-level: no. [R-SER-06]: "1 = interleaved and 2 = planar are the only values
this specification defines and the only values a writer MAY emit" — both
conforming; Appendix G is non-normative.

### 6. writer-03 — REFUTED

§3.1 decides it: "**addressed tile / stored tile** — every tile of a layer is
*addressed*." So "added tiles" means tiles added to the layer, i.e. newly
addressed tiles, and "grown extents, an appended channel" are the two ways that
happens — precisely the reporter's reading 2, and the only reading the
document's own vocabulary supports. A tile that goes sentinel→stored is not an
"added tile"; it existed and was addressed, and [R-IDX-01] ("The entry for the
tile with disk ordinal k is the k-th entry") already gave it an entry. Reading 1
is available only to a reader who takes "added" to mean "newly stored", which
the terminology section forecloses. No partition break.

Residue: the flat comma list would read better with a colon. Optional.

### 7. writer-04 — CONFIRMED, not byte-level

Verified both sides. [R-CNT-02]: "belongs to exactly one of: the front signature
block; or a **structure** — a stored-tile extent, a record extent ..., the
directory, or the trailer." §22.3: "every byte a reader can reach belongs to one
named structure." §8.1's table heads its first column "Structure" and its first
row is "Front signature block", so the document does use the word both ways.
Real terminological inconsistency, at the one place the partition has its
special case, in unlabelled normative text.

Byte-level: no. §9.7 names the walk's claimants directly: "The front signature
block at [0, 16) and the live trailer at [F − 64, F) are claimed by the walk as
well, being members of the live committed state (`[R-CNT-02]`)". Nothing turns
on the word.

### 8. verifier-02 + adversary-04 — CONFIRMED, **BYTE-LEVEL** (upgraded)

Both reporters self-flagged non-byte-level. I uphold the defect and upgrade it.

The sentence, verified: "A compactor's verification depth follows reliance over
everything it carries (`[R-WRT-03]`): it relies structurally on every structure
it copies, so it MUST verify each link of the chain — the open (§19.1), each
retained layer's record (§19.3) and full index chain (`[R-IDX-04]`), and each
relocated extent's checksum, including every stored tile's entry crc — before
emitting that structure's bytes."

The two quantifications differ and §20.5 itself says the difference is live:
"In this placement A's stored extents happen not to move, so A's index is copied
and only its slot re-pointed". So "relocated" means moved.

*Why verifier-02's downgrade fails.* It rests on "[R-CNF-05]'s first sentence,
'A writer MUST emit only conforming files', bars every conforming writer from
emitting it under both readings". The document says the opposite for a
compactor. §20.1 [R-WRT-01]: "A creator emits only conforming files
(`[R-CNF-05]`). An appender and a compactor satisfy every writer requirement
for the bytes they produce and the preservation obligations of §20.4 for what
they carry forward (`[R-CNF-06]`) ... — a violation latent in a structure they
carry forward unmodified travels with it, seen or unseen". §20.5 repeats it:
"a violation latent in a structure it carries forward verbatim travels into its
output (`[R-WRT-01]`)", and its conformance claim is conditional — "Given a
conforming input the output is a conforming file." So a conforming compactor
may emit a nonconforming output; the disputed file's own nonconformance does
not settle the question, which is what adversary-04's reason (1) also assumes.

*Why the fork reaches bytes.* §20.5: "A compactor MUST refuse to compact when
any check `[R-WRT-09]` obliges fails, and MUST NOT emit a file carrying a
violation it has detected". Take adversary-04's input I (a top-level
user-metadata extent whose terminal CRC does not match, everything else clean,
compactor chooses a placement that moves nothing). Under (E) that extent's CRC
is not a check [R-WRT-09] obliges, the compactor never looks, and it lawfully
emits O. Under (P) the check is obliged, it fails, and the compactor MUST
refuse. O is in the emittable set under one reading and not the other. That is
the byte-level test as stated.

*Routes that would collapse the fork, checked and rejected.*
- [R-CNF-11] makes updaters readers, but §19.2 puts R2's detection "at use of a
  record's extent: that extent's CRC ... before anything the extent holds is
  returned", and adds "Structures a request never relies on impose no detection
  obligation beyond the open steps." A compactor copying opaque bytes returns
  nothing the extent holds.
- §8.2's chain of trust ("trailer → directory → (per layer) crc_of_crc_array →
  segment CRC array → index segment → index entry → stored tile") does not
  contain a user-metadata extent's CRC — but neither does it contain the
  "relocated extent's checksum" the enumeration adds, so it does not adjudicate.
- [R-WRT-07]'s restatement closes the tile half only: "That `[R-WRT-09]`'s
  checks reach the index chain and each stored tile's entry crc rather than an
  entry's own value domain bounds how far a compactor goes looking" — note it
  drops "relocated" for tiles and is silent on record extents.
- The trailing clause "before emitting **that structure's** bytes" has no closer
  antecedent than "every structure it copies", which pulls the timing (and so
  the obligation) back to the premise's quantifier. That is what keeps (P) live
  against the grammar argument for (E).

*Sentence I looked for and did not find*: any sentence saying either that a
compactor's [R-WRT-09] duty reaches every extent it copies, or that it is
exempt on one it does not relocate. Three formulations exist (premise,
enumeration, [R-WRT-07]'s restatement) and no two agree.

### 9. register-01 — CONFIRMED, not byte-level

Verified [R-CNT-25]'s quarantine trigger is a closed four-item list: "each way a
user-metadata record's document can be unreadable once its framing has been read
— a failed extent CRC, an unimplemented or invalid encoding, a decode failure,
or content violating the document's own rules". Verified R4's condition cell:
"several, the content-size field among them, are broken by what the frame
declares while the bytes decode". So several R4 instances meet none of the four,
and §21.1's "as `[R-CNT-25]`'s quarantine does for every §21.5 row" over-reaches
— which is why the same sentence names [R-MTA-09] for R4.

Byte-level: no. The outcome is fixed twice over: §21.5's heading "Outcome:
ignore-record", and [R-MTA-09]'s "Any violation here is ignore-record, never the
tile-scope outcome §17.2 assigns."

### 10. register-02 — PARTIAL, not byte-level

Counted the §21.6 Rule column myself: 15 entries — 8 cite a single rule, 6 give
a flat comma list, 1 (zero layers) uses the register's parenthetical form
"`[R-CNT-14]` (R-CNT-02)". The reporter's "Fourteen entries give an
undifferentiated comma list" is a miscount; his own parenthetical shows 6.

His two "first-named picks the wrong rule" examples do not survive checking.
§19.4 step 1 derives the request failure from the very rule he says is silent:
"a coordinate outside the extents addresses nothing in the reference array
(`[R-MDL-01]`) — the request fails as a request, with no verdict on the file."
And [R-IDX-02] does state the fill behaviour, not only the bytes: "A sentinel
tile contributes fill to the reference array (§3.2, §13)."

Residual real defect: §21.1 extends governance in the singular — "where such an
entry and the rule it cites diverge, the rule governs there too" — over cells
that cite up to four rules, and the parenthetical convention is used in exactly
one of the fifteen. PARTIAL.

Byte-level: no. Every cited rule is normative in its own section and unchanged;
§21.6 entries are defined non-violations.

### 11. register-03 — CONFIRMED, not byte-level

All four claims verified against the rows:
1. L2 cell "`[R-ENC-04]` (R-GEO-03, R-CNT-13, R-SER-02, R-SER-07)"; its last
   instance is "entry_count × 20 + ⌈entry_count/2¹⁶⌉ × 4"; the rule designating
   that expression is [R-CNT-17]: "Under index_encoding 1, extent_length MUST
   equal entry_count × 20 + ⌈entry_count / 2¹⁶⌉ × 4 (and 0 when entry_count is
   0), **that expression being a declaration-derived quantity under
   `[R-ENC-04]`**". Uncited.
2. L21's condition names "the geometry-derived addressed-tile count (N
   interleaved, C·N planar)", which is [R-GEO-03]'s; cell is "`[R-CNT-17]`
   (R-CNT-20)". Uncited — while L2 cites R-GEO-03 for the same quantities.
3. F27 and L48 both read "`[R-MTA-05]` (R-CNF-05)"; [R-CNT-25] names them for
   scope: "where a rule outside this quarantine records a document's defect at
   the file or the layer (`[R-MTA-05]`, F27, L48), the verifier records it
   there". Uncited.
4. F14 (R-CNT-20, R-ENC-09); F20, L37, L38, T1 (… R-ENC-10); R2 (R-CNT-25) —
   neither. Verified row by row.

Byte-level: no. §21.1: "each row *restates* its governing rule, and where a row
and the rule it cites diverge, **the rule governs**."

### 12. register-04 — PARTIAL, not byte-level

The chain is as described: §21.7 "as `[R-CNF-13]` individuates them";
[R-CNF-13] "one malformed state, as §21.1 individuates them"; §21.1 "each row
is one malformed condition". And §21.7 does close the parallel hazard for
detectability in terms: "The instrument is the checks this specification
obliges an actor to perform, and deliberately not the register's own rows — a
test keyed to the rows would make §21.1's completeness clause vacuous".

But the circle is not closed the way the reporter says: [R-CNF-13] supplies a
substantive criterion of its own — "one malformed state" — and §21.1's "each row
is one malformed condition" reads as its application to the rows that exist
rather than as the definition. PARTIAL: the real defect is that no individuation
guidance is stated for a condition with no row, which is conspicuous beside
§21.7's explicit anti-circularity move for the sibling question.

Byte-level: no. Reach under [R-CNF-13] is settled by enumeration where it
matters — §2.3 "`[R-CNT-06]` states nine" and §21.2 "Deriving it there yields
F8, F14, F6 and both of F1's instances ... and no other row" — and a reader's
duties come from the requirements and the rows that exist.

### 13. register-05 — CONFIRMED, not byte-level

The repetition is verbatim: "...it resolves a nonconforming interleaved boolean
byte to a sample value rather than serving it through, which is why
`[R-TYP-04]` (§12.3) makes it the one case where a reader resolves a byte to a
sample value rather than serving it through". The "which is why" derives the
claim from itself.

Byte-level: no. [R-TYP-04] states it independently: "the one case where a
reader resolves a byte to a value rather than passing it through arises only in
a nonconforming file, and `[R-SER-08]` states it."

### 14. register-06 — CONFIRMED, not byte-level

Verified [R-EXT-03]: "a validity error at the owning scope for the value sets of
§11.4, §12.2, §14.1, §15.1, §17.2, and §17.3", and [R-RDR-03]: "the value sets
of §11.4, §12.2, §14.1, §15.1, §17.2, and §17.3". §15.1's only mention of the
field points elsewhere: "Under index_encoding 1 (the only encoding this format
major version defines, §7.4)" — no set, no reserved range, no outcome. L31's own
cell is "`[R-CNT-23]` (§7.4)". §10.2's row hedges: "index encoding (§7.4,
§15.1)".

Byte-level: no. §7.4 states the set and L31 enumerates the three alternatives
("index_encoding 0; reserved 2-0x7F; experimental >= 0x80"), so the verdict on
any value is unchanged.

### 15. adversary-01 — CONFIRMED, not byte-level

Checked the closing paragraph item by item against the numbered items. Item 5
pins four freedoms; only the first (alignment/slab) appears in the inventory.
Absent: the fixed filter value (§17.3), fixed declared tile extents (§11.3),
fixed layout (§14.1). Every other numbered item is represented.

The hedge mitigates but does not cover: "Read the numbered items as the list;
this paragraph names what they are for, not how many there are" disclaims the
count, and the paragraph's own construction ("the list is not short: <kind>,
which <rule> leaves open; ...") is an enumeration of kinds, three of which are
missing.

Byte-level: no. Appendix G "adds no requirement to any actor", and [R-CNF-05]:
"two conforming writers given identical input MAY produce different conforming
files."

### 16. adversary-02 — CONFIRMED, not byte-level

Verified both sentences of [R-EXT-02] and the table between them. The table is
introduced as "The spaces, defined in the sections that own them and collected
here" and has eight rows, none of them the flag lanes; the closing sentence
nevertheless calls the flag lanes a space, and they are not partitioned into
assigned/reserved/experimental ("which §6.3 partitions instead"). I also
re-derived §20.5's "the other seven spaces §10.2 tabulates (L31, L33, L34, L36,
L43, L45, R1)": eight table rows minus record type = seven. So the table is the
operative inventory, as the reporter says.

Byte-level: no. §6.3 [R-CNT-08] states the lane rules directly: "a reader MUST
reject-file on any set bit it does not implement in the incompat lane (bits
0–15), and MUST ignore all bits in the ignore lane (bits 16–31)."

### 17. adversary-03 — CONFIRMED, not byte-level

Verified L23's two cells and §19.1 step 4's distinct consequence: "a layer
record whose name field does not lie entirely within that record's
inline_length yields no name field to compare, so it contributes no name to the
namespace and is instead a validity error at layer scope (`[R-CNT-18]`)". So
the name case is detected at open, changes what F4 ranges over, and sits inside
the instance "leading fixed fields (name … C)" alongside cases detected at layer
access. §21.1's own test: "One instance is one *distinguishable* file ... because
no two files could differ" — here two files plainly differ. R1's compound
Detected cell does match its instance enumeration; L23's does not.

Byte-level: no. §19.1 step 4 and [R-CNT-18] state the behaviour normatively;
the Instances column governs corpus obligations, and [R-VEC-01] settles the
direction of authority. Bookkeeping consequence: §21.8's "120 conditions over
277 instances" would move.

### 18. adversary-05 — PARTIAL, not byte-level

Both assertions verified verbatim ([R-CNT-09] "a suffix range, whose response
also carries the transport-authoritative file size F (`[R-CNT-10]`)"; §19.1
step 1 "a remote reader's suffix range for step 2 carries F in its own
response"). [R-CNT-10] does provide for the case where it does not.

But "unconditionally" over-states the framing. [R-CNT-09] says "The **baseline**
remote open is two requests"; §19.1 step 1 prefaces the clause with "These steps
are ordered by dependency, not by I/O"; and the Note says "This accounting is a
theory of operation, not a budget". PARTIAL: the real defect is the missing
cross-reference to the case [R-CNT-10] handles (a range response that does not
disclose the complete length), which §6.4's fallback sentence does not cover —
it addresses "transports without suffix-range support", a different failure.

Byte-level: no. [R-CNT-10]: "a reader that cannot obtain one MUST probe
separately or fail the open, and MUST NOT substitute the trailer's
committed_file_length for the transport size."

### 19. adversary-06 — CONFIRMED, not byte-level

Both quotations verified. §4.7's Note: "A variable-length field's value includes
its length prefix, so a name is structural: it determines where the field after
it begins." §13.1: "it never affects how any byte is located or decoded; the
field's length prefix is §7.4's framing". The second sentence is only true of
the fill field if the prefix is *not* part of the value — the opposite
assignment. Real inconsistency in the use of "value".

Byte-level: no. [R-ENC-16] fixes the taxonomy outcome regardless: "In format
major 1 `version_minor` is the only descriptive field, and every other field
this specification defines is structural." Where the prefix is read and what it
must hold is fixed by §7.4's framing and [R-CNT-23]'s cross-check.

### 20. quiz-01 — REFUTED

The sentence that decides it is the one introducing the list, in the same
paragraph: "A layer that stores a tile **in the generation this commit
supersedes** keeps its declarations, with these exceptions and no other".
Keeping is the stated default; the closed list enumerates departures from it, so
"kept" cannot be a member of it and its absence is not a gap. Reading (B) —
that a commit leaving a declaration untouched does something the enumeration
does not license — requires reading the exceptions list as a list of everything
a commit may do, which the opening clause forecloses. The delegated clause's
"declared, changed or kept ... or is cleared" is doing different work: it names
which declarations owe their invariants over the new state, and a kept
declaration owes them exactly as a declared or changed one does.

### 21. quiz-02 — PARTIAL

Verified §11.1's Rationale drops the "keeps its declarations" default. But a
commit that keeps a declaration needs no permission, so the restatement's
silence about it is not a gap in permissions. The sharper residue is the
catch-all: "each subject to every rule the declarations it **produces** are
under" reaches only declarations the commit produces, so [R-SLB-04]'s duty on a
*kept* slab declaration across a commit that changes the stored-tile set —
"MUST either re-establish the invariants for every such run — or clear the
declaration in the new generation" — is not reflected. PARTIAL.

Not byte-level: [R-CNF-01] exempts "any text labeled *Note*, *Example*, or
*Rationale*", and the block itself says "§20.3 states normatively, and governs".

### 22. quiz-03 — PARTIAL

The version_minor claim is refuted by the sentence's own closing clause. The
test is glossed and the gloss is declared definitional: "determines anything a
conforming reader or verifier does with the bytes it reads — where a byte lies,
how it decodes, what a decoded value is, or whether the file, layer or tile is
accepted at all, **which is the sense `[R-CNT-07]`, `[R-MTA-02]` and
`[R-SEC-06]` already use**." An advisory line is none of the four, and
[R-CNF-12] puts it outside acceptance in terms: "a verifier reports a SHOULD
deviation as an advisory that does not bar certification. A verifier owes no
search for one". So the widening to "or verifier" does not reach version_minor
and the closing sentence stands.

The reporter's second point is right and is what survives: "each class being
what the one before it is not" names nothing for the first of two classes —
structural is defined positively and only descriptive is defined as the
complement. PARTIAL on that residue.

Not byte-level: [R-CNT-07] "A reader MUST NOT reject a file for its
version_minor".

### 23. quiz-04 — REFUTED

Two sentences decide it. §21.9: "The last three rows are **per-instance** ...
*Decoded size of one tile* ranges over a layer's **addressed** tiles, stored or
not" — the quantity is a tile's, and [R-ERR-04]'s own list of scopes includes
"a tile". Reading (B) substitutes "declarations" for the rule's "stated or
derived quantities". (In a planar layer the tiles of different channels have
different decoded sizes, so the layer is not even a uniform unit here.)

And the distinction is inconsequential in any case: "It MAY also decline at any
scope that contains the narrowest one, as `[R-COD-06]` provides for a frame's
window and `[R-CNF-11]` presupposes." A reader declining the layer is licensed
under reading (A) too, so no behaviour is barred either way and no file moves
between the accepted and rejected sets.

## Coverage

25 input ids, 23 groups, each id in exactly one group, counted by hand:
reader-01, reader-02 (2); writer-01..04 (4); verifier-01..03 (3);
register-01..06 (6); adversary-01..06 (6); quiz-01..04 (4) = 25.
Two groups carry two members; 21 carry one. 21 + 2 + 2 = 25.

Byte-level upheld: 1 (`compactor-copies-vs-relocated`).
