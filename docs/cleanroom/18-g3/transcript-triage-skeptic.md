# Round 18 triage — skeptic lens — working transcript

## What I read

Only `/Users/robertkleffner/Documents/GitHub/tarn/spec/tarn.md`, in these
chunks (all by absolute path, via `sed -n`):

- §2.1–§2.5 (lines 96–280)
- §3.1 (282–345)
- §5.2 (618–700)
- §6.1–§6.4 (691–830)
- §7.1 (868–900)
- §9.4–§9.7 (1242–1370)
- §15.4 (2061–2108)
- §17.3–§17.4 (2355–2413)
- §18.2 (2435–2570)
- §20–§20.5 (2849–3264)
- §21.1–§21.9 (3264–3705)
- §23.1–§23.2 (3813–3870)
- Appendix G, whole (4138–end of G)
- header index (`grep -n "^#"`)

I read **no** transcript at all — not the six walk transcripts, not the
quiz transcripts, and none of the `transcript-triage-*.md` files. I ran
one `ls` of the round18 directory before I had read the instruction's
"do not list that directory" clause; the listing showed the file names
only, and I opened none of them. Disclosed in `disclosure`.

I did not read docs/, PLAN.md, AGENTS.md, conformance/, registry.json,
git history, or the web.

## Grouping

18 groups over 26 ids. Counted twice; union checked by hand against the
id list in the prompt.

1. `s21-7-only-where-conjunction` — reader-01, verifier-01, diagrams-01, register-03 (4)
2. `compactor-depth-relocated-vs-copied` — reader-02 (1)
3. `lif-04-residue-clause` — writer-01 (1)
4. `appendix-g-item-8-compactor` — writer-02 (1)
5. `one-crc-forecloses-compaction` — writer-03 (1)
6. `index-regeneration-trigger` — writer-04, adversary-02, quiz-03 (3)
7. `prv-01-supersede-scope` — writer-05 (1)
8. `s20-4-table-scope` — writer-06, adversary-01, diagrams-06 (3)
9. `foreign-major-verdict` — verifier-02 (1)
10. `partial-slack-enumeration-boundary` — verifier-03 (1)
11. `s20-4-persistence-block-unidentified` — diagrams-02 (1)
12. `r5-r6-governing-rule-order` — diagrams-03 (1)
13. `r7-bom-condition-vs-instances` — diagrams-04, register-02 (2)
14. `s20-3-note-narrowed` — diagrams-05 (1)
15. `t26-t5-analogy` — register-01 (1)
16. `s21-1-no-identifier` — register-04 (1)
17. `compactor-version-minor-modal` — quiz-01 (1)
18. `dead-cannot-establish-branch` — quiz-02 (1)

4+1+1+1+1+3+1+3+1+1+1+1+2+1+1+1+1+1 = 26.

### Grouping calls worth defending

- **6 vs 2.** writer-04, adversary-02 and quiz-03 all attack the same
  clause of `[R-WRT-07]` — "regenerates each **relocated** tile-index
  region" — and all three consequences (stale entries; undetected
  malformed entry; no input-determined trigger) fall out of the same
  word. One group. reader-02 attacks a *different* sentence
  (`[R-WRT-09]`'s premise/enumeration mismatch) with a different repair,
  so it stays separate even though the same word "relocated" is the
  hinge. If the reconciler prefers one group of four, the substance of
  my grades is unchanged.
- **8.** writer-06 and adversary-01 are plainly one defect. diagrams-06
  approaches the same scope mismatch from §2.4's pointer into the table;
  the repair (say which of the MU = 1 cell's four sentences generalize,
  and point §2.4 at §20.4's prose for the registered types) is one edit.
- **13.** diagrams-04 and register-02 are the same row-internal
  mismatch; they differ only on which half they would repair.
- **15 stays out of group 1** even though both are §21.7 sentences:
  different clause, different claim, different repair.

## Group-by-group: what I tried to kill and how it went

### 1. §21.7 "witnessed only where … *and* …" (reader-01, verifier-01, diagrams-01, register-03)

Kill attempt: find a governing rule making the "only" true. Failed. The
sentence's own continuation names T3/T14 for a decoded-size change and
T15/T17/T23/T25 for a codec change, none of which is "a padding
position, a pad bit, or a boolean byte". Reading (a) is falsified in
place. All four reporters converge on reading (b). CONFIRMED.

Byte-level: no. Deciding sentence, §2.3 `[R-CNF-04]`: "A reader MUST
detect every violation the error register (§21) assigns to the reader as
its detector, and apply the outcome class this specification assigns to
each". T3, T14, T15, T17, T23, T25 are §21.4 rows with detector *reader*
and their own governing rules; §21.1 adds "The subsections after §21.5
are not part of the register and carry no rows". §21.7 assigns nothing,
so no reader's or verifier's behaviour moves under either reading.
Severity editorial.

### 2. reader-02 — `[R-WRT-09]` premise vs enumeration

I tried hard to kill this one and only half-killed it.

The enumeration's own gloss is a universal: "each relocated extent's
checksum, **including every stored tile's entry crc**". "Every stored
tile's" is not restricted by "relocated", so the whole T1 half of the
reporter's worry is decided — a stored tile's entry crc is verified
whether or not that tile moved. That leaves record extents (the R2 case
the reporter actually built: a top-level user-metadata extent at offset
16 that compaction leaves at 16 — realistic, since Appendix G item 3
pins "The first structure begins at 16").

For record extents I could not find the deciding sentence. §20.5's
"a violation latent in a structure it carries forward verbatim travels
into its output (`[R-WRT-01]`) — **its verification depth is
`[R-WRT-09]`'s**" defers to the very sentence in dispute rather than
resolving it.

Byte-level judgement, and the premise it rests on, stated so it can be
attacked: **I downgrade on the premise that a divergence reachable only
from an input that is already nonconforming is not a fork in the
format's bytes** — the document conditions its output promise expressly
("Given a conforming input the output is a conforming file") and
expressly sanctions the other disposition (`[R-WRT-01]`). On a
conforming input every CRC verifies and the readings produce identical
output. If the reconciler rejects that premise, this group *is*
byte-level: under (a) `[R-WRT-06]`'s "MUST refuse to compact when any
check `[R-WRT-09]` obliges fails" forbids emitting a specific,
constructible file that (b) permits, and no drop is available because
both registered types carry PE = 1. Graded design-decision, because the
repair is a choice with a cost (it makes writer-03's uncompactable-file
consequence bite wider).

### 3. writer-01 — `[R-LIF-04]`'s trailing clause

Kill: the clause is introduced by "**so that** after any commit
completes, the physical file length equals committed_file_length, and
bytes beyond a committed length never survive into any committed state".
The "so that" makes the second conjunct a consequence of truncating to
the *new* committed_file_length, under which reading it is simply true.
The reporter reads "a committed length" as universally quantified over
generations, which the framing does not support. PARTIAL.

Byte-level: no, and not for the reporter's reason. Even under reading
(a) — "overwrite all of [F, old physical length)" — a writer that
overwrites those bytes with bytes equal to what was there has complied,
because `[R-CNT-21]` says "Slack has no internal structure this
specification defines, its content is unconstrained, and no conformance
requirement applies to it". So the set of emittable byte sequences is
identical under both readings; only the syscall pattern differs.

### 4. writer-02 — Appendix G item 8

Verified: item 2 carries an explicit compactor carve-out ("This is a
creator's rule: a compactor adopting the profile takes `[R-WRT-06]`'s
fresh draw instead"); item 8 carries none; §6.3 says in terms "A
compactor, though its output is a new file, carries the input's unknown
ignore-lane bits into its output trailer **rather than writing
flags = 0**". Item 8 tells a profile-adopting compactor to write
flags = 0. Real. CONFIRMED.

Byte-level: no. Deciding sentence, Appendix G's own preamble: "It adds
no requirement to any actor: a writer ignoring it is fully conforming",
and `[R-CNF-01]` excludes "appendices identified as non-normative" from
normative text. Nothing a conforming implementation may emit changes.

### 5. writer-03 — one failed CRC forecloses compaction

Chain verified end to end: `[R-WRT-09]` reaches "every stored tile's
entry crc" and the retained records; `[R-WRT-06]` "MUST refuse to
compact when any check `[R-WRT-09]` obliges fails"; §20.5 "Where the
table does not license a drop the compactor MUST refuse"; §20.4 "both
registered types carry PE = 1, so neither can be dropped". So a single
T1 or R2 makes the file permanently uncompactable. CONFIRMED as stated —
the text decides, and what it decides is expensive.

Byte-level: no. The input keeps its verdict; the tool emits nothing.
Graded design-decision: whether to state this consequence out loud (and
whether to offer any escape) is the maintainer's call, not an edit.

### 6. writer-04 + adversary-02 + quiz-03 — regeneration conditioned on relocation

Kill attempt on writer-04's half: succeeded on the bytes. `[R-WRT-07]`'s
own closing MUST — "The output's reference arrays MUST equal the live
generation's bit for bit (`[R-MDL-02]`): compaction changes where bytes
live, never what a layer denotes" — forbids the stale-entry output the
literal reading would produce. So the trigger is under-inclusive as
*wording* but no conforming compactor may act on it.

Kill attempt on adversary-02/quiz-03's half: succeeded, and for a
reason both reporters half-state. The divergence between a compactor
that leaves a region at its input offset and one that moves it is
**licensed, not undetermined**: §2.3 `[R-CNF-05]` — "Writer conformance
is semantic: this specification does not promise canonical bytes, and
two conforming writers given identical input MAY produce different
conforming files" — and §20.5's placement freedom. Both compactors agree
about what the text requires *of them given their own placement choice*.
That is licensed nondeterminism, which is not a byte-level ambiguity.

I checked the premise that a non-relocated structure is reachable at all,
rather than inheriting it: input `front | tiles A | index A | ▓slack▓ |
dir | pad | tr` compacts to `front | tiles A | index A | dir' | pad |
tr'` with nothing before the reclaimed slack moving. Common, not
contrived. Premise holds.

CONFIRMED (the trigger names the wrong event), byte-level no, editorial.
Residue worth a maintainer's note: the malformed-entry refusal duty has
no input-determined trigger, so §21.8's corpus cannot compel it.

### 7. writer-05 — §23.1's "only removal of sample data"

Kill: found. §5.2 uses "superseded" as the general term for every byte an
earlier commit left unclaimed — "Every byte the live state does not claim
is slack: alignment and slab gaps, the pre-trailer pad, and **everything
an earlier commit superseded**" — and §3.1 glosses it the same way
("Superseded payload bytes from earlier generations do not make a tile
stored"). A de-addressed tile's extent is neither a gap nor the pad, so
§5.2's enumeration puts it under "superseded". §20.3's local contrast
between "de-addressed" and "supersedes" is descriptive of the operation,
not a narrowing of the term. So `[R-PRV-01]` reaches shrink-as-delete
and §23.1's "only" survives.

The reporter's *secondary* point does survive: "an unknown ancillary
record's drop (§20.4)" is narrower than §20.4, which lets an updater
drop a PE = 0 record of "a type the updater implements that this
specification does not register". PARTIAL, editorial, not byte-level
(the rule governs how a tool describes an operation to its user).

### 8. writer-06 + adversary-01 + diagrams-06 — §20.4's table scope

Kill of the broad reading: succeeded, twice over. §20.4's lead-in:
"**For a type the updater does not implement**, the stored flags are
authoritative (§7.3, `[R-CNT-15]`; MU = 1 with PE = 0 is read as PE = 1,
`[R-CNT-12]`), and carry these obligations:". The MU = 1 cell's own
prose confirms it — "an **unknown** critical record blocks modification
of that layer", "`[R-CNT-15]` makes an **unimplemented** top-level MU = 1
record reject-file". And §20.3's `[R-WRT-04]` is an explicit, ordered
MUST to modify layers. So no updater may read the cell as barring every
layer edit.

What survives the kill is the residue adversary-01 isolates: an
MU = 1 type the updater *implements* but this specification does not
register. The cell's "Compaction is barred on the same ground
(`[R-WRT-06]`)" points the opposite way from §20.5's "a compactor
implementing one relocates whatever that registration defines, on the
same terms as the tile index" — reconciled only by noticing that
`[R-WRT-06]`'s own text bars "any record whose type it does not
implement with MU = 1". Three sections to see. CONFIRMED as a scoping
defect worth repairing; byte-level no; editorial.

### 9. verifier-02 — foreign major plus a permanently-fixed-field violation

Kill: found, in §21.2's own reason clause. "Four rows are outside that
reasoning and do reach it, **because their subject is a field fixed
across every major (`[R-CNT-24]`)**". A violation of a field fixed
across every major is not a finding *under major 1 in particular*, which
is all §2.3's "neither conforming nor nonconforming **under it**" bars.
So Reading A is the document's, and §2.3's priority sentence then gives
*nonconforming*. §24's boolean is recordable. PARTIAL: the verdict is
decided, but §2.3's blanket sentence carries no pointer to the carve-out
and should get one. Byte-level no — the reporter's own analysis of the
reader path is correct and I confirmed it against §6.2's ordering.

### 10. verifier-03 — partial slack total when a file-scope failure stops the walk

Kill: found, and the reporter did not look at it. §9.7, on which
claimants survive a failure: "an entry `[R-IDX-03]` classifies
reject-tile on a **structural** ground contributes no stored extent to
the walk; **one whose stored bytes alone fail its crc keeps its
extent**." That is the document stating the principle the reporter says
is missing — a checksum failure does not withdraw a claim, a structural
failure does. §9.7 also lists "the directory itself" among the claimants
reached from the live trailer, and separates reaching from verifying
("It checks that these occupy disjoint byte ranges … and that each
verifies against the checksum covering it"). The directory's bounds come
from the trailer, which verified. So reading (i) — 387 in the reporter's
W1 — is the document's, and reading (ii) is foreclosed.

REFUTED. Byte-level no. Optional editorial repair only: lift the
parenthetical's principle into §5.2 so it is not stated solely about
index entries.

### 11. diagrams-02 — §20.4's persistence block carries no identifier

Verified by inspection: `[R-WRT-05]` terminates the first paragraph;
the "Persistence governs every record type" paragraph, the obligation
table, and the "No commit therefore removes a layer record" paragraph
carry no identifier; `[R-WRT-08]` terminates a later, separate paragraph
about re-encoding. §21.6 cites `[R-WRT-08]` for "preserved or dropped
per its PE bit", which `[R-WRT-08]`'s sentence does not state; §22.3
uses the identifier narrowly. Both usages are in the document, and
nothing states an identifier-placement convention. CONFIRMED.

Byte-level: no — "the obligations in §20.4's table are the same words
binding the same actors" under either label, and §21.6 is outside the
register (§21.1: "The subsections after §21.5 are not part of the
register and carry no rows"), so no `[R-VEC-02]` manifest identifier
turns on it. Editorial: mint an identifier for the persistence block and
repoint §21.6.

### 12. diagrams-03 — R5/R6 vs R7–R10 governing-rule order

Checked the cells directly. R5 `[R-CNT-25]` (R-MTA-04, R-ENC-11);
R6 `[R-CNT-25]` (R-ENC-12); R7–R10 `[R-MTA-04]` first. §21.1: a
Governing rule cell names "the requirement that **defines** it" first.

Partial kill on R5: `[R-CNT-25]` does name its subject expressly —
"content violating the document's own rules (**ill-formed UTF-8
included**, `[R-ENC-11]`)" — so R5's order is defensible. No kill on R6:
"empty or contains a code point in U+0000 through U+001F" and R10's
"longer than 255 bytes" are stated by one and the same `[R-MTA-04]`
bullet ("every key satisfying §4.6's name rules — non-empty, at most 255
bytes, free of U+0000 through U+001F"), and the two rows name different
requirements first. CONFIRMED on R6-vs-R10.

Byte-level: no — §21.5's heading fixes the outcome ("Outcome:
ignore-record") and §21.1 makes the rule govern over the row.
register-bookkeeping, because `[R-VEC-02]` records the first identifier.

### 13. diagrams-04 + register-02 — R7's condition vs its instances

Verified against §18.2's first bullet: "A JSON object, unmarked. The
top-level value is an object, and the encoding carries no byte-order
mark: a leading U+FEFF makes the document unreadable." Three
restrictions; R7's Condition restates two; R7's Instances enumerate
three shapes over two containers. §21.1 licenses an instance to name
"one of several alternatives **the condition text states**". It does
not. CONFIRMED.

Byte-level: no — §21.1's "where a row and the rule it cites diverge, the
rule governs", and `[R-MTA-04]` is unambiguous. register-bookkeeping,
because the instance count 6 is load-bearing for §21.8's 273.
Repair the Condition, not the Instances, so the count is unchanged.

### 14. diagrams-05 — §20.3's cost Note

Rule: "Every layer whose stored-tile set **or index content** this
commit changes has its tile-index region re-emitted in full". Note:
"any change to a layer's stored-tile set re-emits that layer's whole
tile-index region". The Note then reasons to "editing one sample", which
supersedes a tile — the stored-tile set is unchanged, the index content
is not. §5.1's caption states the trigger in full, so the narrow form is
isolated. CONFIRMED.

Byte-level: no. `[R-CNF-01]`: "All text in this document is normative
except: §1 (Introduction); **any text labeled *Note*, *Example*, or
*Rationale***". Editorial.

### 15. register-01 — §21.7's "exactly as a mis-strided filter is" vs T26

I checked the arithmetic myself rather than taking it. §17.3: the
filtered image places byte i of group j at offset i·n + j, n = L/s; the
inverse restores byte i·n + j to offset j·s + i. Setting i·n + j = L − 1
over 0 ≤ j < n forces i = s − 1, j = n − 1, whose source offset is
j·s + i = ns − 1 = L − 1. So the last byte is a fixed point at every
stride dividing L, for every s — no simulation needed. A packed planar
bool plane's pad bits live only in that byte (§14.3 per the reporter,
and T5's own text: "a final-byte pad bit (bit positions P mod 8 through
7)"), and the reader's inverse for such a plane is the identity (§17.3:
"for a packed boolean plane s = 1 and the filter is the identity"). So
T5 cannot witness a stride error. T26 is right; §21.7's "exactly as" is
the half to repair.

Partial kill: grammatically the list "T2, T4 or T5" attaches to *a
mis-ordered image* — for which T5 is reachable — and "exactly as a
mis-strided filter is" can be read as a manner analogy rather than a
claim of identical rows. That reading rescues the sentence but is not
the one a corpus builder will take. CONFIRMED with that caveat.

Byte-level: no. T26's own parenthetical ("a wrong stride with no such
structural constraint is undetectable, §21.7") and `[R-COD-10]` decide
the outcome; T26's "packed planar bool: identity s = 1" instance stays
constructible through T4, since a wrong stride moves padding-position
bits even though it fixes the final byte. register-bookkeeping.

### 16. register-04 — §21.1 carries no identifier

Verified: neither §21.1 paragraph terminates in an identifier;
`[R-ERR-02]` is §21.8's; §21.7 has `[R-ERR-01]`, §21.9 `[R-ERR-03]`–`05`.

Partial kill: §2.1's Note states the phrasing discipline as "every
requirement **names the actor it binds** (writer, reader, updater,
verifier, or file)". §21.1's two load-bearing rules — completeness is
normative, and the rule governs over the row — bind no actor; they are
interpretive rules about the document. On that test §2.2's convention
("Normative requirements carry identifiers") does not clearly reach
them. But "Its **completeness is normative**" is hard to square with
"interpretive only". PARTIAL; byte-level no; editorial, and a
maintainer's call.

### 17. quiz-01 — §20.5's compactor `version_minor` clause (the only byte-level flag)

This is the one I worked hardest, in the direction my lens prefers
(kill it) — and I did not manage it cleanly.

The clause: "The output trailer copies the input's unknown ignore-lane
flag bits forward (`[R-CNT-08]`) and carries the greater of
`[R-CNT-26]`'s floor and the input's version_minor". No BCP 14 modal.
Its only cited authority for the floor, `[R-CNT-26]`, is stated wholly
in the SHOULD register: "A writer **SHOULD** emit the lowest
version_minor that defines every feature present in the file — for a
file expressible under this text, 0 — and an appender the maximum of
that floor and the prior trailer's minor".

Kill attempts:

- `[R-CNF-01]` ("All text in this document is normative except…") makes
  the clause normative but does not fix its **strength**; normative text
  can be a SHOULD. Not decisive.
- §2.1's "when, and only when, they appear in all capitals" shows the
  clause is not a lowercase SHOULD. It shows what the clause is not, not
  what it is.
- Precedent: `[R-CNT-24]` is a bare declarative whose violations are
  registered as F8/F14, so the document does treat declaratives as
  binding. Suggestive, not stated.
- Best attempt — coordination. "The output trailer **copies** … **and
  carries** …": one subject, two coordinate verbs, so one modal force.
  "Copies" must be mandatory, because §6.3 relies on exactly this
  construction to displace its own MUST: "a writer creating a file under
  this text MUST write flags = 0 … A compactor, though its output is a
  new file, carries the input's unknown ignore-lane bits into its output
  trailer rather than writing flags = 0 (§20.5, `[R-WRT-06]`)."
  Counter, and why the kill fails: §6.3 states that carve-out **itself**,
  backed by "An updater MUST copy forward unknown ignore-lane bits". So
  §20.5's "copies" restates a MUST that lives elsewhere, while "carries"
  restates nothing mandatory — its only citation is a SHOULD. The
  coordination argument therefore shows the two verbs share a register
  without establishing which register that is.

I could not quote a sentence that fixes the strength, so I did not
downgrade. And the fork is over a **conforming** input, which is the
cleanest shape there is: given a conforming minor-7 input with flags = 0
and every feature expressible under this text, `[R-CNT-26]`'s floor is 0
(version_minor is descriptive, §4.7, not a "feature present in the
file"), so a compactor reading the clause as mandatory emits `07 00` at
trailer offset 10 and one reading it as advisory emits `00 00`, with
four different CRC bytes at trailer offset 60. Both files are
conforming; `[R-CNT-07]` forbids any reader to reject on
version_minor. The fork is entirely in the second half of the test —
which byte sequences a conforming implementation may emit.

Noted for the maintainer: the clause is unconditional while its stated
rationale ("a compactor cannot know which minor version defined an
ignore-lane bit it does not implement") only reaches inputs that carry
unknown ignore-lane bits. Repairing the modal without deciding the scope
leaves a second reading available.

UPHELD byte-level.

### 18. quiz-02 — the dead cannot-establish branch

Verified the collapse. §2.3 lists "when it cannot execute a codec or
filter (`[R-COD-11]`)" among the cannot-establish grounds. §17.4 closes
it: "For a conforming reader that position arises only at a reserved or
experimental value, **every assigned codec and filter being core**: it
rejects the layer (`[R-COD-03]`, `[R-COD-09]`); software unable to
execute an assigned codec or filter is not a conforming reader
(`[R-CNF-03]`)." A reserved/experimental value is L43/L45, an
established violation, and §2.3's priority sentence then forces
*nonconforming*. §2.3 also makes verifiers readers. So the ground has no
instance for a conforming verifier. I checked the near misses — window
size, lz4 decoded-size cap, oversized metadata documents — and each is a
*resource* ground, separately enumerated.

CONFIRMED as an observation. Byte-level: no — the quoted §17.4 sentence
decides every case the branch could name. Editorial.

## Byte-level tally

1 of 26 ids, 1 of 18 groups: quiz-01.

Groups where I record that a reconciler rejecting my stated premise
would reach byte-level instead: group 2 (reader-02). That premise is
written out in `byte_level_rationale`.

## Groups I tried hardest to kill and failed

- **17 (quiz-01)** — four separate attempts, above. Failed.
- **2 (reader-02)** — half-killed by the "including every stored tile's
  entry crc" universal; the record-extent half survives on a premise I
  had to supply myself rather than quote.
- **1 (§21.7)** — nothing to kill; the sentence refutes itself in place.

## Groups I killed

- **10 (verifier-03)** — §9.7's "one whose stored bytes alone fail its
  crc keeps its extent". REFUTED.
- **7 (writer-05)** — §5.2's "everything an earlier commit superseded".
  Main claim refuted; a narrower point survives.
- **3 (writer-01)** — the "so that" framing, plus the
  overwrite-with-identical-bytes observation that collapses the byte
  question outright.
- **9 (verifier-02)** — §21.2's "because their subject is a field fixed
  across every major".
- **8 (§20.4 table)** — the lead-in plus the cell's own "unknown" and
  "unimplemented"; broad reading dead.
- **6 (regeneration trigger)** — `[R-CNF-05]`'s licensed
  nondeterminism, and `[R-WRT-07]`'s reference-array MUST.
