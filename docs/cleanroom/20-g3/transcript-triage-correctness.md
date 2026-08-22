# Round 20 triage — correctness lens — working transcript

## Access disclosure

Read: `spec/tarn.md` in full (sed chunks covering lines 1–4369). No walk
transcripts opened. No `transcript-triage-*.md` opened, and the round20
directory was listed once by `ls` before I had read the prohibition on
listing it — the listing showed nine transcript filenames and three
`.py` helper files; the three triage files were **not** present in that
listing (they had not been written yet), and I opened none of them. No
`docs/`, `PLAN.md`, `AGENTS.md`, `conformance/`, `registry.json`, git
history, or web.

Mechanical checks run:

- `grep -n "logically modif"` → exactly one hit, line 3105, inside
  `[R-WRT-05]`. Confirms writer-01's "occurs exactly once and is nowhere
  defined".
- `grep -n "Window_Size\|window size\|declared window"` → §17.2 (tile
  rule, twice + two Notes), T21, and §21.9's table row. **No sentence
  anywhere connects a user-metadata frame's window to the §21.9 row.**
- `grep -n "resource ground\|resource limit\|on resource"` → §2.3 (×3),
  §2.5, §17.2 line 2295, §18.2's Note lines 2488/2491, `[R-ERR-04]` line
  3677. The only normative sentence putting a *metadata* decode decline
  on resource grounds is `[R-MTA-09]`'s, and it is written around the
  **size** bound; line 2488's is a *Note* and is also size-bound-scoped.
- Register instance arithmetic, counted mechanically off the tables:
  **121 rows / 273 instances** (F 36/58, L 49/116, T 26/55, R 10/44),
  matching §21.8 exactly. L14 = 3 instances, R7 = 6, F29 = 3. This
  confirms diagrams-01's arithmetic: the published 273 is reachable only
  by trusting the Instances cells.

---

## Grouping decisions

Two merges, on the "one distinct defect" rule, forced by the fact that an
input id cannot be split across groups:

- **diagrams-01 + register-01.** register-01 reports R7 only; diagrams-01
  reports L14 and R7 as one defect of the same shape against the same
  §21.1 rule. Since diagrams-01 cannot be split, R7 travels with L14.
- **register-02 + adversary-03.** adversary-03's whole subject ("the
  §20.4 preservation table carries MUST-level obligations under no
  identifier") is register-02's *first* guessed thing, reached from the
  other side. Same defect, same repair (mint an identifier). register-02
  carries two further defects in the same §21.6 entry, which ride along
  in the group and are named separately in the recommended action.
- **register-03 + quiz-02.** Same sentence, same miscount.
- **reader-01 + quiz-01.** Same sentence, same two readings, same
  resolution.

Everything else stands alone. adversary-01 and adversary-02 both sit on
`[R-MTA-09]` but are distinct defects (classification of a window
decline; the keyword-free floor on the size bound) and are not merged.

---

## Per-group verification notes

### 1. cnf03-scope-blind-carveout (reader-01, quiz-01)

Text checked verbatim:

- §2.3 `[R-CNF-03]`: "A reader MUST accept every conforming file of a
  format major version it implements, carrying no record of a type it
  does not implement with MUST_UNDERSTAND = 1 … (§21.9's `[R-ERR-04]`
  governs a refusal on that last ground; §21.6's closing paragraph names
  the other two)". Accurate; no scope qualifier on "record".
- §7.4 `[R-CNT-18]`: "an unknown sub-record type with MU = 1 is
  reject-layer, and where the file is otherwise conforming a reader MUST
  NOT reject the file for it". Accurate, all-caps.
- §21.6 closing: "the same type as a layer sub-record is reject-layer and
  never a ground to refuse the file (`[R-CNT-18]`), so only the top-level
  case is a file a reader refuses". Accurate.

**Downgrade quotation:** `[R-CNT-18]`'s "a reader MUST NOT reject the
file for it". §2.3 withholds an acceptance duty; it grants no permission
to reject, and `[R-CNF-12]`'s licence reaches only nonconforming files
("For a nonconforming file no acceptance obligation exists"). So the
reader that refuses is nonconforming under a capitalised MUST NOT, and
no accept/reject verdict on any byte sequence is open.

**Correction to reader-01:** its claim that Appendix H "reproduces it as
the summary" is false. Appendix H's conforming-reader entry reads
"accepts every conforming file within §21.9's minimum guarantees and
reports any resource refusal as a limit rather than as corruption
(`[R-ERR-04]`)" — it omits the MU = 1 carve-out entirely, so it is if
anything *stricter*, not scope-blind. One leg of reader-01's harm story
is wrong; the §2.3 leg stands and decides the group.

### 2. channel-selection-undefined (reader-02)

Checked: §19.4's opening defines a point request as "a single
coordinate" and a region request as "a rectangular range of coordinates,
one interval per dimension" — channels appear nowhere. Step 2 ("per
requested channel c planar"), step 7 ("each requested value"), step 8
("a planar layer's several channels") and the closing note
("Channel-subset reads verify only the segments they touch") all use a
channel selection the vocabulary never defines. Accurate, and all four
mentions are planar-side, as reported.

`[R-TYP-08]`'s "for each channel the tile carries" and step 4's "each
carried channel's, in declared order, in an interleaved layer" are quoted
correctly.

**Downgrade quotation:** §14.1 `[R-SER-01]` fixes the stored value
sequence for an interleaved tile — "the tile at spatial ordinal s carries
all C channels at the tile's P positions, sample-major" — with no
reference to any request, and §14.2's byte layout likewise. Nothing a
writer may emit moves, and both readings accept the file. The divergence
is in the arity of an API return. `[R-VEC-02]` records "the decoded
content a reader is to return from every scope it can read", which is a
scope's full content and not a per-request projection, so no vector can
separate the readings either.

Real, and it needs a maintainer decision (does the request vocabulary
admit channel selection, and what does an interleaved sentinel return
under one?). Not bytes.

### 3. ser08-returned-bool-representation (reader-03) — PARTIAL

`[R-SER-08]` quoted correctly. But reader-03's framing — that step 8
"frames returns as bit patterns" and so pulls against `[R-SER-08]` — is
defeated by step 8's own parenthetical, which the reporter quotes only
in part. Step 8 in full: "Return the requested values' bit patterns
unaltered (`[R-MDL-02]`, `[R-TYP-04]`) — **for every byte a conforming
file can carry, the whole of this step** (`[R-SER-08]` fixes what a
reader returns for the one byte a conforming file cannot)." Step 8
expressly withdraws itself for exactly this byte. So the "pass 0x37
through, per step 8's own framing" horn does not exist.

Also: reader-03's second hop leans on `[R-MDL-02]`, but §3.2 opens
"Each layer of **a conforming file** denotes exactly one reference
array" — the case arises only in a nonconforming file, so the reference
array supplies nothing here. The reporter reached the right answer
(0x01) by an argument weaker than claimed; the answer is better carried
by §14.2's "a bool value … as a single byte, 0x00 = false, 0x01 = true"
plus §13.2's Rationale refusing the 255-encodings-of-true convention.

**Downgrade quotation:** `[R-SER-08]`'s own writer half — "Writers MUST
NOT emit any byte other than 0x00 or 0x01 as an interleaved bool value"
— and "A reader is not obligated to screen decoded content, and a reader
that does not detect the violation is not thereby nonconforming".
Emittable set fixed; accept/reject unmoved.

### 4. appender-index-relocation (writer-01)

§20.3 step 4's clause quoted accurately and carries no BCP 14 keyword.
`[R-WRT-05]`'s "does not logically modify" verified as the document's
only occurrence of the phrase, undefined. `[R-WRT-07]`'s "except that
relocation re-points extent slots" verified. The §5.1 Example's parallel
sentence ("A commit never relocates a live index region otherwise") is
inside an *Example* and so non-normative — which strengthens rather than
weakens the finding, since the clause's only normative statement is the
keyword-free one.

One correction to the reporter's premise: §2.1 says the *keywords* bind
only in all caps; it does not say keyword-free text has no force, and
`[R-CNF-01]` makes all text normative. So the clause is normative
declarative text of uncertain operative content — which is the defect,
not "no force at all".

**Downgrade quotation:** §2.3 `[R-CNF-02]` — "a file is never
nonconforming by virtue of one [a conduct rule]" — and the relocated
output is byte-indistinguishable from a freshly emitted one, so no file
moves in or out of the conforming set. A creator may emit either
placement. Conduct, not bytes.

### 5. step2-must-not-drop-vs-204 (writer-02)

§20.3 step 2 quoted accurately. §20.4's MU = 0 / PE = 0 row quoted
accurately, including "A commit changes the layer set by adding a layer".
The tension is real: read as an independent prohibition, step 2 bars a
drop §20.4 licenses; read as a pointer, the "(§20.4)" citation leaves the
licence intact. Both are permitted by the words — the "carries forward"
subject makes reading B available, and reading A is available because
reading B makes the second conjunct vacuous (one cannot drop a record
one carries forward).

**Wrinkle the reporter did not price:** F26's detector is *verifier* and
its outcome is reject-file. Step 2's own first sentence says "A violation
the open establishes bars the commits its outcome bars and no others:
reject-file bars every commit". An appender that *establishes* F26 is
barred from committing at all, drop or no drop. The reporter's scenario
survives only because §21.1 says of a verifier-detected row that its
outcome "names the scope at which the damage is recorded, not an
obligation on any reader", so the appender-as-reader may proceed. Worth
recording, but it does not defeat the finding: the collision between
"MUST NOT drop the record (§20.4)" and §20.4's licence stands
independently of any defect being present.

**Downgrade quotation:** §2.3 `[R-CNF-02]`, "File conformance is a pure
predicate on bytes: it does not depend on any reader, writer, or
environment." Whichever reading an appender takes, the two outputs are
different files each of whose conformance is decided by the same
predicate; no fixed byte sequence changes verdict.

### 6. appendix-g-unpinned-tiling-layout (writer-03)

Verified: item 5's three-part test quoted correctly. §11.3's Note —
"Tile extents are a writer's choice, and this specification imposes
none" — accurate. `[R-SER-06]` leaves layout free; §14.4's Note gives
"⌈P/8⌉ packed bytes planar versus P bytes interleaved". Items 1–10 read
in full: neither tile extents, nor layout, nor dimension order, nor
channel order is pinned anywhere, and the closing paragraph's
enumeration omits them too. The appendix's opening claim to close "the
degrees of freedom this format deliberately leaves open" is therefore
not delivered on its own item-5 test. Reporter's counter to its own
reading A (item 2's rationale groups codec with tiling and layout, yet
item 1 pins the codec) is sound.

**Downgrade quotation:** Appendix G's own second sentence — "It adds no
requirement to any actor: a writer ignoring it is fully conforming" —
plus §2.1's exception for "appendices identified as non-normative".

### 7. cnt21-relief-scope (verifier-01)

Verified: `[R-CNT-21]`'s relief is worded "Where **§6.2's ordered
validation** rejects the file before a live trailer is established".
`[R-CNT-06]`'s ordered list contains no 128-byte-minimum check, and
`[R-CNT-27]` sits in §5.1 with no placement; `[R-CNT-04]` sits in §6.1
with "before other processing". §21.2's preamble names F6 individually
as outside §6.2's ordering, so the document is elsewhere careful about
exactly this — the reporter's strongest point, and it checks out. F5's
Detected cell is "open", verified.

Reading (b) is strained but available: the partial-total trigger reads
"Where the walk of §9.7 does not enumerate every region's claimants —
… or because the verifier elected under `[R-CNF-11]` to stop at the
first violation — the verifier MUST report the total as partial", and a
stop at F6 satisfies that clause on its face. Against it: "A partial
total is F less the bytes claimed", and there is no F.

**Downgrade quotation:** §5.2's own Note — "A partial total
(`[R-CNT-21]`) reports what one verifier's incomplete walk left
unclaimed, which is a fact about **that run** and not about the file's
live state." The slack figure is a property of the verifier's traversal,
not of the bytes; and both readings return *nonconforming*. §2.3's
framing of the per-requirement channel — "that per-requirement report
constrains the report and not the verdict" — is the same shape.

### 8. unassigned-type-extent-not-named (verifier-02)

Verified: §22.3 `[R-SEC-04]` states four residues, two of which are
uninspected extents, and states the naming remedy only for the
user-metadata one. `[R-MTA-10]`'s MUST verified verbatim. §8.1's map row
"Extent of a record of a type this specification has not assigned | none
— the bytes are opaque (§7.2) | —" verified. §9.7's walk reaches "each
record's extent" and §5.2 names "a record extent (the bytes any record's
extent slot references, whatever the record's type)" — so those bytes are
claimants and are not in the slack total, as reported. Appendix H's
verifier checklist names the `[R-MTA-10]` report and no counterpart.
Everything the reporter asserts is true of the document.

Minor: the reporter says `[R-SEC-04]` "sets the two uninspected residues
side by side"; there are four residues in that paragraph, two of them
uninspected extents. Immaterial.

**Downgrade quotation:** §8.1 `[R-CNT-19]`'s exception for "the extent of
a record of a type this specification has not assigned, in which this
specification defines no fields (§4.7) and whose bytes it leaves opaque
(§7.2)" — no rule attaches under either reading, so no byte's status
moves. The gap is in what a certificate can say, which §21.7 treats as
"no file-level witness exists to check, so nothing about the file is
left undetermined".

### 9. instances-beyond-condition-l14-r7 (diagrams-01, register-01)

§21.1's instance rule quoted accurately by both. L14's Condition/Instances
mismatch verified: Condition states two alternatives, Instances names
three, the third being "trailing residue", which `[R-CNT-18]` states as
its own condition ("any overrun, truncation, or **residue** is a validity
error at layer scope") and which F29 — the file-scope twin — puts *in*
its Condition cell ("or bytes remain after the last complete record").
R7 verified the same way against `[R-MTA-04]`'s first bullet, which
states the BOM as a restriction distinct from well-formedness.

I ran the arithmetic myself rather than trusting diagrams-01: 121 rows
and 273 instances, matching §21.8 exactly. Dropping L14's residue and
R7's two BOM instances would give 270. So the Instances cells are the
ones the published figure rests on, and the resolution both reporters
picked (Condition cells are short) is the only one consistent with
§21.8.

register-01's RFC 8259 argument is sound and adds the reason the first
alternative does not subsume the third.

**Downgrade quotation:** §21.1 — "each row *restates* its governing rule,
and where a row and the rule it cites diverge, **the rule governs**."
`[R-CNT-18]` and `[R-MTA-04]` both state the omitted alternative
normatively, so every implementation reaches the same disposition. The
cost is corpus construction only.

### 10. appendix-a-local-reader-phrasing (diagrams-02) — PARTIAL

The reporter quotes Appendix A as "A local reader additionally verifies
bytes [0, 16) by equality first, which `[R-CNT-04]` requires of any
reader holding them" and stops there. The sentence continues: "— **as a
remote reader does too whenever its speculative suffix window reaches
offset 0**, which on this 128-byte file means a window of the whole
file." And the next sentence: "A shorter window can still spare the
second request: 112 bytes covering [16, 128) contains the directory, so
§6.4's containment test applies, **while bytes [0, 16) stay non-resident,
so §6.1 leaves the front-block check to the reader**."

So Appendix A states the residency test three times in three consecutive
sentences and explicitly extends the obligation to a remote reader and
withdraws it from a non-resident window. The reporter's headline — that
Appendix A "ties the front-block equality check to a 'local reader', the
test §6.1 expressly rejects" — and its claim that "Appendix A is the only
place that attaches it to transport class" do not survive the full
sentence. Its own reading (b) ("locality is itself the trigger") is not
permitted by the words, because the words that follow rule it out.

What remains is a mild prose infelicity: the sentence *leads* with the
transport class, and a local reader that preads only the trailer and
directory does not hold [0, 16). That is worth a reword and nothing more.
The claimed harm — a verifier author granting a remote verifier an
exemption — requires ignoring the rest of the same sentence.

**Downgrade quotation:** the appendix heading, "Appendix A — An annotated
minimal file (non-normative)", with §2.1's exception; plus the sentence's
own "which `[R-CNT-04]` requires of any reader holding them — as a remote
reader does too".

### 11. sec47-note-mis-states-columns (diagrams-03)

Both claims verified. §7.4's table is `| Field | Type | Constraint |` —
against §4.7's six-item list it omits offset, **size**, and class, where
the Note says "omits the offset and class columns". §6.2, §15.1 and
§18.2 all carry Size and Type as distinct columns, so the omission of
Size is a real third omission and not a merger. §6.1's table is
`| Offset | Size | Value | Class |`, matching the Note's "a Value column
replaces type and range".

§7.2's five Field cells are exactly as reported: `type (0 invalid)`;
`flags: bit 0 MUST_UNDERSTAND, bit 1 PRESERVE_ON_EDIT, bits 2–15
reserved`; `inline_length`; `extent_offset`; `extent_length`. Only the
first carries a range; the flags cell carries a bit decomposition, not a
range; the three length/offset fields carry none, their ranges living in
`[R-CNT-13]`. So "folds each field's range into its Field cell" is
inaccurate for at least three of five.

**Downgrade quotation:** §2.1 `[R-CNF-01]` — "All text in this document
is normative except: §1 (Introduction); any text labeled *Note*,
*Example*, or *Rationale*". The passage is a *Note*, and every size §7.4
omits is fixed by its Type cell while every range §7.2 omits is fixed by
`[R-CNT-12]`/`[R-CNT-13]`.

### 12. s204-table-unlabelled-and-216-miscite (register-02, adversary-03)

Verified in the source: §20.4 runs paragraph → `[R-WRT-05]`; then
"Persistence governs every record type … carry these obligations:", the
three-row table, and "No commit therefore removes a layer record…", none
carrying an identifier; then a paragraph ending `[R-WRT-08]` whose own
sentence is "An updater MUST NOT re-encode a record whose type it does
not implement, and MUST NOT modify one except by relocating its extent
and re-pointing its slot under §20.5" — nothing about preservation or
dropping. The table's cells carry capitalised MUST NOT / MUST / MAY /
SHOULD, verified verbatim.

§21.6's fifth entry cites "`[R-CNT-15]`, `[R-WRT-08]`", verified. Every
other citation of the table is by section: §2.4's preserve-verbatim row
("§20.4's table states the cases"), `[R-CNF-06]` ("the preservation
obligations of §20.4"), Appendix H. So §21.6 is indeed the only site
pinning an identifier, and it pins one whose sentence is about something
else.

register-02's second point verified: §20.4 says "For a type the updater
implements that this specification does not register, the definition it
implements the type from supplies the flags, and the stored bits never
do", where §21.6's entry says only "preserved or dropped per its PE bit".
Third point is weaker than the reporter allows: L25's own Governing-rule
cell is "`[R-CNT-15]` (R-CNT-18)", so the register's own convention
already treats `[R-CNT-15]` as governing the sub-record row.

**Downgrade quotation:** §21.1 — "§21.6's entries restate their governing
rules on the same terms a row does, and where such an entry and the rule
it cites diverge, **the rule governs there too**." §20.4 governs, so an
updater implementing an experimental type takes its disposition from the
definition it implements. And a record retained byte-identically and a
record dropped are each conforming outputs, so no accept/reject verdict
on any fixed byte sequence moves. adversary-03 concedes the same:
"the obligations bind either way".

### 13. s217-compacted-trailer-count (register-03, quiz-02)

§21.7's sentence quoted accurately by both. `[R-WRT-06]` places four
things on the output trailer: fresh file_id ("a new draw … not merely a
value compared against the input's"), generation 1, carried ignore-lane
bits, version_minor floor. §20.5's own answering sentence, "Neither
obligation has a witness in the output alone (§21.7)", follows the
version_minor sentence and so agrees with §21.7's pair — the two sites
agree with each other and undercount §20.5's own list, exactly as
register-03 says.

quiz-02's claim that "generation 1 is witnessed in the output alone" is
imprecise: a verifier reads generation 5 but has no way to know the file
was a compaction output, so generation 1 is no more witnessed *as a
compaction obligation* than the file_id is. register-03 gets this right
and notes `[R-LIF-03]`'s generation sequence, which §21.7 does name,
absorbs it. The shared core — the fresh file_id belongs in the
inventory and is not there — is right in both.

**Downgrade quotation:** §21.1 — "neither this completeness clause nor
the instance arithmetic below reaches … §21.7's account of what no check
detects." §21.7 owes no exhaustiveness, no register row is missing, and
the obligations are unwitnessed under either reading.

### 14. f5-outside-212-preamble-reasoning (register-04)

Verified: §21.2's preamble justifies the exclusion by §6.2's ordering
and names four exceptions (F8, F1 trailer-magic, F14, F6 with F1's
front-block instance), naming F6's `[R-CNT-04]` placement expressly.
`[R-CNT-06]`'s ordered list contains no 128-byte check; `[R-CNT-27]` is
in §5.1 with no stated placement; §19.1 never mentions it though step 1
already has F in hand. F5's Detected cell is "open". All accurate.

The scenario is constructible (e.g. a 120-byte file carrying the correct
front block, a valid trailer magic and CRC at [56,120), and
version_major = 2: F6 passes, F5 is available, the version gate is
foreign).

**Downgrade quotation:** §2.3 `[R-CNF-02]` — "a file declaring another
major is neither conforming nor nonconforming under it: a reader refuses
such a file on capability grounds (§6.3, `[R-CNT-07]`), and that refusal
is not a finding about its bytes." Reading (a)'s *nonconforming* verdict
is foreclosed outright, so the verdict does not fork; a reader refuses
under both readings. What is wrong is the preamble's *reasoning*, which
does not cover F5 and does not name it as it names F6. The reporter
reaches the same place.

### 15. metadata-zstd-window-r3-or-capability (adversary-01) — UPHELD BYTE-LEVEL

Checked the construction. §18.2 `[R-MTA-09]`: "The constraints §17.2
states against a tile's declared decoded size do not apply, because a
document has no declared size" — `[R-COD-06]`'s window rule is stated as
"MUST NOT declare a window size exceeding the tile's decoded size", so it
is withdrawn and a metadata frame's Window_Size is unconstrained.
Verified by grep that **no** sentence anywhere ties a metadata frame's
window to §21.9's row.

The file: 15-byte extent `28 B5 2F FD | 00 | A0 | 11 00 00 | 7B 7D |
B1 19 64 52` — magic, FHD 0x00, Window_Descriptor 0xA0 (exponent 20 →
windowLog 30 → 1 GiB), one last raw block of 2 bytes carrying `{}`, then
the terminal CRC. 0x68 gives exponent 13 → windowLog 23 → 8 MiB. Record
type 0x0002 with flags 0x0002 = MU 0 / PE 1, matching §7.3; inline_length
1; extent (16, 15) with 16 ≥ 16 and 31 ≤ F − 64; dir at 31 length 29 with
60 ≤ 64; F = 128. Every gate I can check from the document passes, and
the decoded document `{}` satisfies all four of `[R-MTA-04]`'s
restrictions. The file is conforming.

The two paths, both from normative text:

- **Toward R3.** §21.5's preamble: "every way its document can be
  unreadable takes this outcome, whatever the containing scope — as a
  violation in the rows below, except at an experimental-range encoding
  … **and except where a reader or verifier declines the decode on the
  size bound**, which `[R-MTA-09]` makes that actor's capability and not
  a fact about the file." Two exceptions, closed list; a window decline
  is neither. `[R-CNT-25]` lists "a decode failure" among the ways a
  document is unreadable. R3's condition then reads on it, and §2.3's
  "An established violation takes priority" forces *nonconforming*.
- **Toward capability.** §21.9's row is "zstd frame `Window_Size` | 8
  MiB" — unqualified, where its neighbours say "of one tile" and "of one
  user-metadata document" — so 1 GiB is a quantity exceeding a guarantee,
  `[R-CNF-03]`'s acceptance duty does not reach the file, and
  `[R-ERR-04]` says "a refusal on resource grounds MUST be reported as a
  resource limit and not as a validity error".

**Why I did not downgrade.** The instruction is to quote *the sentence*
that decides it. `[R-ERR-04]` is the only candidate, and it does not
decide this case on its face: it never mentions a document or a record,
and its own scope clause names the narrowest available scopes as "a
layer or a tile", which is precisely the enumeration a metadata record
falls outside. Reaching it requires three inferences (the §21.9 row is
not tile-scoped → the ground is objectively "resource" → the rule reaches
a verifier's verdict and not only its wording). That is an argument, not
a quotation.

Against that, the document twice restates the same carve-out at two
different breadths: §2.3's cannot-establish list says "when it declines
to decode a user-metadata document (`[R-MTA-09]`)" — unqualified, and
introduced by an illustrative "as when" — while §21.5's preamble says
"declines the decode **on the size bound**". Two normative restatements
of one carve-out that differ in scope is itself the ambiguity. And
`[R-MTA-09]`'s verifier sentence is written tightly around "the bound
above", i.e. the document-size bound.

Decisive comparison: for a **tile**, §17.2 says in terms that "a wider
window is conforming and merely permits a conforming reader to decline
the tile or the layer on resource grounds (`[R-ERR-04]`)". The metadata
side has no such sentence, and `[R-MTA-09]` is the section that would
carry it. The presence of the sentence on one side and its absence on
the other is evidence the case was not decided, not evidence it was
decided the same way.

So: one fixed 128-byte conforming file, one byte apart from its twin at
offset 0x15, and two verifiers each with a text-anchored path to opposite
verdicts — *nonconforming* and *conforming*. That is an accept/reject
fork on a fixed byte sequence, and `[R-VEC-02]` makes the corpus
expectation unstateable, which that rule names as its own test for a
finding against this document. Byte-level upheld. A false positive costs
one re-read; this one is worth it.

Secondary, and real: `[R-COD-06]`'s "Writers SHOULD keep the declared
window within §21.9's 8 MiB `Window_Size` guarantee" is scoped to tiles
and `[R-MTA-09]` withdraws §17.2's constraints, so nothing steers a
writer's metadata window. Stock zstd at high levels will produce them.

### 16. mta09-decode-bound-floor-keywordless (adversary-02)

Verified: `[R-MTA-09]`'s "a reader instead decodes with a bound of its
own choosing, no smaller than §21.9's user-metadata guarantee" carries no
capitalised keyword, and it is the only place the 16 MiB row is imposed
on reader behaviour. §2.5 `[R-CNF-10]`/`[R-ERR-03]`'s MUST is "accept",
which ignore-record satisfies — `[R-CNT-25]`'s quarantine defines
ignore-record as leaving "decoding of all stored data unaffected", so the
reader accepts the file and serves every sample. §21.9's own "Software
that declines **on that ground** a file whose every quantity lies within
the table is not a conforming reader" is a sentence the reporter did not
quote, but it does not reach the case either: a reader taking
ignore-record has not declined the file.

Correction to the reporter's premise: §2.1 restricts the *keywords* to
all-caps interpretation; it does not strip force from keyword-free text,
and `[R-CNF-01]` makes all text normative. So reading (a) is the better
one and the defect is a phrasing-discipline lapse against §2.1's own
Note ("every requirement names the actor it binds").

**Downgrade quotation:** `[R-CNT-25]` — ignore-record means "The record
is skipped as though absent. Decoding of all stored data is unaffected."
Under both readings the reader accepts the file and serves every sample,
and §2.3 makes *cannot establish* "not a finding that the file is
nonconforming". What forks is which implementations count as conforming,
never what any implementation does to any byte sequence.

---

## Coverage

20 input ids, 16 groups, union of member_ids = the input list, no
duplicates, counted by hand against the id list in the charter:
reader-01, reader-02, reader-03, writer-01, writer-02, writer-03,
verifier-01, verifier-02, diagrams-01, diagrams-02, diagrams-03,
register-01, register-02, register-03, register-04, adversary-01,
adversary-02, adversary-03, quiz-01, quiz-02. No id was skipped and no
finding went unevaluated.
