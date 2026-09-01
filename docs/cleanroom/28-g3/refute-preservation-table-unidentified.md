# Refute-only verification — §20.4 preservation table carries no identifier; §21.6 cites [R-WRT-08]

## Disclosure

Files read: `/Users/robertkleffner/Documents/GitHub/tarn-first-draft/spec/tarn.md` only.
Commands run: `wc -l`, `mkdir -p` (private scratch dir), `sed -n` on line ranges of that
file, `grep -n` on that file, one `awk`/`cut` pipeline over `sed` output of that file. No
git, no directory listing, no web, no other file, no computation over any other input.
Scratch dir created: `.../r28-refute/priv-preservation-table-unidentified/` (nothing was
ultimately written into it; no scratch script was needed).

Unrequested context appeared before I began: a project-instruction block, a user-identity
block, a current-date block, an environment block naming the repository, branch and recent
commit subject lines, an MCP-server instructions block, and a deferred-tool/skill listing.
None of it is the specification; I disregarded all of it and quote none of it.

## Sections opened

§2.1, §2.2, §2.3, §2.4, §2.5, §7.2 (`[R-CNT-13]`/`[R-CNT-14]`/`[R-CNT-15]` region), §7.3
(`[R-CNT-22]`), §20.1, §20.2, §20.3 (full, including step 2 and step 6's `[R-WRT-04]`),
§20.4 (full), §20.5 (full), §21.1, §21.5, §21.6, §21.7, §21.8, §24 (`[R-VEC-01]`–
`[R-VEC-04]`), §22.3's residues paragraph, §23.1's opening.

## Anchors verified in the file

- 3288 `[R-WRT-05]` closes the re-emission paragraph.
- 3290–3300 the persistence paragraph, no identifier.
- 3302–3306 the table, plain markdown, no blockquote marker, no *Note*/*Example*/
  *Rationale* label, no identifier.
- 3308–3316 the "No commit therefore removes a layer record" paragraph, no identifier.
- 3322 `[R-WRT-08]` closes the re-encode/relocate paragraph.
- 3760 §21.6's row: `| A record type this specification has not assigned, from the
  experimental range (≥ 0x8000, §10.2), carries MU = 0 | Ignored, and preserved or dropped
  per its PE bit; ... | `[R-CNT-15]`, `[R-WRT-08]` |`

Both halves of the finding are true as stated. The question is only whether they fork bytes.

## Constructions attempted

### C1 — the drop-only commit (the appender path)

File: front block; zero layers; one top-level record of experimental type 0x8001, MU = 0,
PE = 0, 8-byte inline payload; directory; pad; trailer. Appender A and appender B both
receive "remove record 0x8001 and change nothing else."

- Under §20.4's table: "Dropping the record, or dropping another record in the same commit,
  is not itself such a change, so a commit whose only effect would be the drop MUST retain
  it." A emits a new directory still carrying the 24-or-so bytes of record 0x8001.
- The hoped-for B: reads §2.2 ("Normative requirements carry identifiers…"), concludes the
  unidentified table states no requirement, drops the record, and emits a directory shorter
  by the record's framed length. Both output files are conforming — a directory with or
  without an unassigned experimental record breaks no register row — so `[R-CNF-05]` does
  not bar either, and the fork would be byte-level.

**Killed by four separate identified requirements that reach the table by section
reference, so B's reading is not permitted:**

- `[R-WRT-01]` (§20.1): "An appender and a compactor satisfy every writer requirement for
  the bytes they produce **and the preservation obligations of §20.4 for what they carry
  forward** (`[R-CNF-06]`)."
- `[R-CNF-06]` (§2.3): an updater "MUST satisfy every writer requirement for the bytes it
  produces, and additionally MUST honor the preservation obligations of §20.4 — which
  govern every record type, not only those it does not understand."
- `[R-CNT-15]` (§7.2), which is the very rule §21.6's row cites first: "Updater obligations
  for unknown records are §20's subject."
- `[R-CNF-01]` (§2.1): the table is not §1, not labeled *Note*/*Example*/*Rationale*, not
  an appendix, therefore normative.

So even the identifier-first implementer §2.2 encourages lands on the table: `[R-CNT-15]`
sends them to §20, `[R-CNF-06]` and `[R-WRT-01]` name §20.4 in a MUST. The table binds
under reading (i) and reading (ii) alike, with identical content. Nothing moves.

### C2 — §21.6's row read as a standing permission that overrides §20.4's conditions

Same file. B instead reasons: §21.6's table is normative text ([R-CNF-01]), it is not
labeled, and it says such a record is "preserved or dropped per its PE bit" with no
condition attached; PE = 0, therefore drop, drop-only commit permitted.

**Killed on three grounds.**

1. §21.1: "§21.6's entries restate their governing rules on the same terms a row does, and
   where such an entry and the rule it cites diverge, the rule governs there too." An entry
   is a restatement, not an independent grant.
2. §21.6's own preamble scopes the table to readers: "These are defined behaviors, not
   errors. A reader that treats any of them as a failure is the nonconforming party." The
   Defined-behavior cell's operative word for the reader is *Ignored*; "preserved or
   dropped per its PE bit" names which disposition the PE bit selects, not that the
   selection is unconditional.
3. The cell carries no BCP 14 keyword at all. Per §2.1 it grants no MAY, and a keyword-less
   restatement cannot displace `[R-CNF-06]`'s and `[R-WRT-01]`'s explicit MUSTs. (I did not
   rest on "no keyword ⇒ no force" — I rested on the entry being a restatement whose
   governing rules §21.1 makes controlling.)

Note also that the entry does not actually conflict with the table: the table agrees that
PE = 1 → preserved and PE = 0 → droppable, and adds when an appender may exercise it. A
summary that omits a condition is not a grant of an unconditional one.

### C3 — "modify" in [R-WRT-08] read to include "remove" (the compaction path)

Under reading (i) the table is *outside* [R-WRT-08], so [R-WRT-08]'s sentence stands alone:
"An updater MUST NOT re-encode a record whose type it does not implement, and MUST NOT
modify one except by relocating its extent and re-pointing its slot under §20.5." If
removal counts as modification, compactor C2 must carry every unimplemented-type record
forward, while compactor C1, reading the table, "MAY drop it whenever it rewrites the file."
Two compacted files of the same input, differing by the record's bytes and by every
downstream offset — a real byte fork if the reading were permitted.

**Killed by §20.5's own identified text, which contemplates the drop for exactly this class
and would be self-contradictory under C3's reading:**

- "A compactor's output contains only the structures reachable from the input's live
  trailer — the live committed state (§7.2), less any record §20.4 lets it drop" (`[R-WRT-06]`).
- "Dropping is the one disposal that answers, and only where §20.4's table licenses it: a
  record dropped is not in the output… Where the table does not license a drop the
  compactor MUST refuse."
- "…no drop is available, a tile-index entry being no record §20.4's table licenses
  dropping."

The specification also keeps the verbs distinct: §20.4's opening speaks of a record "it
retains and does not logically modify", the table's PE = 0 row of "Retain byte-identical,
or drop it", and §20.4's Rationale of a directory differing "exactly by the records
modified, added, or dropped" — three verbs, drop listed apart from modify. C3's reading
would make the table's third row and §20.5's drop machinery dead letters.

### C4 — reading (ii) changes what [R-WRT-08] covers

If the table sits under [R-WRT-08], does the MU = 1 row's "Retain byte-identical" acquire
[R-WRT-08]'s relocate-and-re-point carve-out that it lacks under reading (i)?

**Killed twice.** §2.4's preserve-verbatim row already states the carve-out for both
preserved rows — "the bytes are carried forward unmodified (relocated only as Part I
permits)" — so it is present under reading (i) too. And relocation is compaction's
operation only (§20.3 step 4: "relocating a live index region is compaction's operation
(§20.5, `[R-WRT-07]`), not an appender's"), while `[R-WRT-06]` independently states "A
compactor MUST refuse to compact a file carrying any record whose type it does not
implement with MU = 1." The case never arises under either reading.

### C5 — the degenerate compaction (zero layers, one experimental PE = 0 record)

Compactor may drop or retain. Both readings permit both. This is `[R-CNF-05]`'s second
sentence operating *within* what the rules leave open — "two conforming writers given
identical input MAY produce different conforming files" — not a divergence between
readings. Nothing moves.

### C6 — a reserved-range MU = 0 record (the nonconforming-input case)

§21.6's row extends to reserved-range types ("read the same way, but emitting one is a
violation (F36, L25)"). A compactor detecting F36 must not emit a file carrying it; §20.5
resolves this by the table's licence, PE = 0 droppable / PE = 1 refuse. Both readings give
the same disposition because both reach the table through §20.5's section reference.
Nothing moves.

### C7 — the conformance corpus (the reporter's own residual cost)

`[R-VEC-02]` requires "for each structure the file damages, the outcome class (§2.4), the
scope, and the §21 register row it exercises together with that row's governing requirement
identifier." The identifier duty is attached to a register row. §20.4's obligations carry
no register row (§21.1: the register is §21.2–§21.5, and "The subsections after §21.5 are
not part of the register and carry no rows"), and a vector exercising a licensed drop
damages no structure. So no vector needs an identifier it cannot supply, and the corpus's
files do not differ under the two readings. Nothing moves.

### C8 — does the register's normative completeness force a row, and so a fork?

§21.1's completeness runs to "every detectable file-conformance violation this
specification names." A drop-only commit's output is a conforming file; the restriction is
an obligation on the actor across two generations, of the same family as `[R-LIF-01]`'s
committed-prefix immutability that §21.7 places outside the register. Either way, no row
exists under either reading, so the register cannot fork them.

## Verdict

NOT_BYTE_LEVEL. Under every reading the text permits, §20.4's table binds updaters with the
same content, and §21.6's misdirected citation is resolved by §21.1's divergence clause. No
appender or compactor emits a byte it could not emit under the other reading, and no reader
or verifier reaches a different accept/reject verdict. The cost is traceability, as the
reporter said.
