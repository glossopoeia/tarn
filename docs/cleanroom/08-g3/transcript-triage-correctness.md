# Round 8 triage — correctness lens — working transcript

## What I read

`spec/tarn.md` in full-relevant-part, by direct Read of these line ranges:
92–271 (§2 conformance), 352–531 (§4 encoding, §5.1), 531–820 (§5.2, §6, §7.1),
820–1019 (§7.2–§7.4, §8.1 head), 1056–1265 (§9), 1290–1350 (§10.2–§10.4),
1571–1600 (§13.1), 1667–1876 (§14, §15.1), 1876–2105 (§15.2–§16, §17.1),
2105–2304 (§17.2–§18.1), 2304–2483 (§18.2–§18.4), 2483–2702 (§19),
2702–2971 (§20), 2971–3318 (§21), 3479–3598 (§24, Appendix A), 3606–3640
(Appendix B), 3729–3842 (Appendices G, H).

Greps run: `^#{1,3} ` (section index); `informative|semantic|structural`;
`preserve-verbatim`; `R-TYP-10`; `non-layer top-level`; counts of
`| verifier |` in the §21.2/§21.3/§21.4 line ranges.

I did **not** read `docs/`, `PLAN.md`, `AGENTS.md`, `conformance/`,
`spec/registry.json`, git history, the web, or any round-8 reporter
transcript. Every claim below was checked against `spec/tarn.md` directly.
I did not run any of the reporters' scripts and did not open `f3.bin` or the
other binaries in `round8/`; where a reporter's arithmetic over a
hand-built file was load-bearing I re-derived it on paper (see §10, §23
below).

## Mechanical checks I performed myself

- Verifier-detected register rows: 7 (§21.2) + 9 (§21.3) + 4 (§21.4) = **20**.
  Appendix H's verifier entry names checks covering F28, F29, F30, F31, F36,
  L19, L41, L42, L43, L47, L48, L49, L50, T2, T4, T5 (+T26 via T2/T4) = 17.
  Missing: **F9, F39, L26**. verifier-05's grep result reproduces.
- `preserve-verbatim`: exactly two hits, lines 216 and 226, both inside §2.4.
  register-06 reproduces.
- Taxonomy-class hits: class labels appear in the layout tables of §6.1, §6.2,
  §7.2, §15.1, §18.2 and in three prose statements (§11.4 line 1422, §12 line
  1470, §13.1 line 1590). §7.4's table header at line 951 is
  `| Field | Type | Constraint |` — no class column. No field anywhere is
  labelled *informative*. diagrams-02 reproduces.
- `non-layer top-level`: 8 hits, all in §21.2 rows (F3, F4, F28, F29, F31,
  F33, F34, F35). This is real evidence for the convention writer-02 relies
  on: the register qualifies "top-level record" when it means to exclude
  layer records.
- §21.8's stated totals: 39+50+26+10 = 125 conditions. 61+102+45+44 = 252.
  Consistent with register-04's count; I did not recount cell-by-cell.

## Grouping decisions

24 groups over 33 ids. Each id appears exactly once; I counted the union
twice (2+1+1+1+1+2+1+2+1+2+1+1+1+1+3+2+1+2+1+1+1+1+2+1 = 33).

Merges, with reasons:

- **reader-01 + diagrams-04** — identical claim about F36's "at open"
  parenthetical against L17/L18/T8/T9.
- **writer-02 + quiz-01** — identical claim about "another top-level record"
  in [R-WRT-08]'s MU=0/PE=0 row. Same two readings, same worked commit.
- **writer-04 + verifier-01** — both about the over-long pre-trailer pad:
  §6.2 says the file is conforming, [R-LIF-02] step 5 makes the commit a MUST
  violation, and no register row exists. writer-04 frames the residue as a
  completeness defect in §21.1/[R-CNF-07]; verifier-01 frames it as a
  verifier's certify-or-refuse choice. One defect, two framings.
- **verifier-02 + diagrams-01** — identical claim about §20.3 example (c)'s
  fill-value change against [R-SER-05]/T4/T5.
- **diagrams-03 + quiz-03 + adversary-04** — all three report Appendix H's
  writer checklist listing [R-CNT-03]'s SHOULD among MUSTs. adversary-04
  additionally carries the reader-checklist omission that diagrams-06 reports
  alone; I placed adversary-04 here because that is its headline and its bulk,
  and cross-noted it in the diagrams-06 group's recommended action.
- **diagrams-05 + register-05** — both against [R-ERR-03]'s "lives here" and
  [R-ERR-05]'s hard-limit enumeration; both name the §16.1 alignment floor as
  the omission and the counterexample to "never a number chosen here".
  register-05 adds a second sub-claim (the 255-byte cap's u8-prefix
  derivation does not hold for JSON metadata keys), kept inside the group.
- **register-01 + adversary-03** — identical claim about F21.
- **adversary-01 + adversary-02** — adversary-02 says so itself ("The defect
  is definitional; its byte-level consequence is reported under
  adversary-01"). Same file, same two clauses ([R-COD-06]'s dictionary
  sentence, [R-COD-10]'s stride sentence), same repair.

Splits I deliberately did *not* make into merges:

- **verifier-05 vs quiz-02.** Both notice that F9 has no home in the text an
  implementer builds a verifier from. But verifier-05's location is
  Appendix H's checklist (and it carries two further, unrelated omissions),
  and quiz-02's is §9.7's check enumeration. Different sections, different
  repairs. Kept separate; cross-noted.
- **verifier-04 vs adversary-01.** Both run the reductio on the broad reading
  of "unable to check". But verifier-04's subject is the clause's scope in
  general (with §21.7's five, [R-CNT-26], [R-WRT-04]/[R-WRT-05] as examples)
  and adversary-01's subject is whether [R-COD-10]/[R-COD-06] are file-level
  requirements at all. The repairs differ (scope the clause vs widen
  [R-CNF-02]'s carve-out). Kept separate.

## Per-group verification notes and downgrade quotations

### 1. F36's "at open" (reader-01, diagrams-04) — CONFIRMED, not byte-level

Checked line 3061 (F36) against lines 3089, 3090 (L17, L18: Detected =
"layer access") and 3138, 3139 (T8, T9: Detected = "tile use"). F11/F12
(3036, 3037) and F34/F35 (3059, 3060) are indeed "open". §21.1 line 3011:
"Detection points name §19.2's reader tiers — open, layer access, tile use,
extent use — or *certification*", so "at open" is a defined term and the
parenthetical is wrong for four of the eight rows cited. §19.1's
[R-RDR-01] confirms the tier could not be open for the index case: the open
"consumes the trailer and directory only — no extent slot's content, no tile
index, no payload".

Downgrade quotation (§19 preamble, lines 2490–2492): "§21's register is, and
`[R-CNF-04]` binds a reader to every register row whose detector is the
reader, **at the tier that row's *Detected* cell names** (§21.1)." Each cited
row's own cell governs that row, so no reader's obligations move. Second
decider, [R-RDR-02] line 2574: "A reader MAY detect any violation earlier".

### 2. §9.7's closing sentence (reader-02) — CONFIRMED, not byte-level

Line 1248–1250: "An entry `[R-IDX-03]` classifies reject-tile does not make
the walk incomplete: the walk passes over it, and the bytes it nominally
addresses fall to slack (§15.3)." The qualifier "on a *structural* ground"
appears only in the opening parenthetical at lines 1228–1231. The reporter's
reading (B) is genuinely available from the closing sentence alone.

Downgrade quotations: §9.7's own opening, line 1228–1231 — "one whose stored
bytes alone fail its crc keeps its extent"; §15.3 line 1921–1925 — "An entry
whose only defect is that its stored bytes fail its crc is well-formed …
its extent stands and it keeps its place in the *verifier* rows, in run
continuity, and in the coverage walk"; §16.2 [R-SLB-03] line 2038–2041 — "An
entry whose only defect is that its stored bytes fail its crc is not
transparent". The reporter's worry that (B) could propagate to L42 is
therefore blocked in §16.2 as well as in §15.3. §5.2's note line 632:
"Coverage is checked by verifiers, never by readers." The only quantity at
risk is a reported slack total.

### 3. [R-ENC-12] and metadata keys (reader-03) — CONFIRMED, not byte-level

Verified [R-ENC-11] (line 457–460) carries the carve-out explicitly and
[R-ENC-12] (line 462–465) does not, while naming user-metadata keys in its
opening clause. The asymmetry is real and one paragraph wide.

Downgrade quotations: [R-CNT-25] line 838–841 — "content violating the
document's own rules (ill-formed UTF-8 included, `[R-ENC-11]`) — is
ignore-record with a SHOULD-report, **notwithstanding the owning-scope
mapping of `[R-CNF-08]`**"; [R-MTA-02] line 2296–2299 — "the outcome of every
failure to read its **document** is ignore-record **whatever the scope**".
Plus §18.2's fourth restriction (lines 2387–2394) folding §4.6's name rules
into the document's own rules, and rows R6 (line 3177) and R10 (line 3181),
both ignore-record at extent use, both citing (R-ENC-12). Four independent
deciders.

### 4. Sub-record extents in the walk (reader-04) — CONFIRMED, not byte-level

§9.7 line 1226: "it enumerates the live directory and its records, each
record's extent". Sub-records are not in the directory's top-level sequence,
so the narrow reading is available.

Downgrade quotations: §5.2 line 584–586 — "a **structure** — a stored-tile
extent, **a record extent (the bytes any record's extent slot references,
whatever the record's type**, §7.2)"; §7.4 line 995 — "Sub-records are
layer-scope records"; §7.2 line 892–894 — "including a stored extent
overlapping its own layer's index region **or sub-record extents**"; L19's
Instances cell (line 3091) — "layer sub-record extents"; F36's (line 3061) —
"sub-record extents". Five deciders. Verifier-only in any case.

### 5. [R-WRT-08] MU = 1 at file scope (writer-01) — CONFIRMED, **byte-level**

This is the one I spent longest on, and I decline to downgrade it.

The row (line 2869) is normative text: "at file scope it blocks any
modification of file-scope structure — adding, removing, or reordering
top-level records — while a commit that only changes a layer's own tiles,
index, or record **remains permitted**." Its preamble (line 2863) scopes it
to "a type the updater does not implement". For a top-level record of such a
type with MU = 1, [R-CNT-15] (line 909) is "MU = 1 → reject-file", §2.4
(line 222) is "A reader MUST NOT rely on any structure in it", §2.3
[R-CNF-11] (line 181) is "Verifiers and updaters are readers of the files
they process and inherit every reader obligation", and §20.3 step 2 (line
2755) is "Perform §19.1's open (`[R-RDR-01]`) — the appender is a reader
here", with §19.1 step 4 (line 2520) applying "the MUST_UNDERSTAND gate for
unknown top-level types (`[R-CNT-15]`)".

I considered and could not adopt the harmonizing reading — that "remains
permitted" is scoped to *this* obligation and other rules may still block —
because it makes the whole file-scope half of the row describe a case that
cannot arise, and because no meta-rule in the document resolves a
normative-vs-normative conflict outside the register (§21.1's "the rule
governs" is scoped to register rows). I have a chain of five passages but no
single sentence that decides it, and the brief is explicit that a downgrade
without a decisive quotation is not a judgement. So: byte-level.

What forks: under (i) a conforming updater emits nothing and the file stays
at generation 1; under (ii) it emits a generation-2 append. The set of byte
sequences a conforming updater may emit differs. I checked writer-01's
redundancy argument against [R-WRT-06] and found it only half-good: the
compactor refusal is *not* redundant for a layer sub-record with MU = 1
(that case is reject-layer, not reject-file), so it adds content under
reading (i) too. That weakens but does not close the finding.

### 6. [R-WRT-08] MU = 0/PE = 0 drop licence (writer-02, quiz-01) — CONFIRMED, **byte-level**

Row text at line 2871: "for a top-level record, the file's layer set or
**another top-level record**". §7.3's table (line 924) scopes type 0x0001 to
"file", so a layer record *is* a top-level record. [R-WRT-04] (line 2763–
2768) makes a tile supersession re-emit the layer's index region "necessarily
at a new placement", which changes the layer record's extent slot — a change
to another top-level record on the literal reading.

I looked for a decider and found the opposite: the register's own convention
is to write "**non-layer** top-level record" (8 occurrences, all §21.2)
precisely when layer records are to be excluded, which makes the unqualified
phrase in §20.4 *include* them. The MU = 1 row's contrasting gloss
("a commit that only changes a layer's own tiles, index, or record") is an
inference across rows about a different obligation and uses different
vocabulary ("modification of file-scope structure"). No sentence decides it,
so no downgrade.

What forks: whether a routine tile commit licenses dropping a PE = 0
ancillary. The two emitted directories differ by 24 bytes plus inline
payload, with different dir_length, pad and committed_file_length.

### 7. Creation path at offset 16 (writer-03) — REFUTED, not byte-level

The sentence (line 1084–1087) does omit step 1 and substitute "beginning at
offset 16". But the reporter's reading (i) — no gap may precede the first
structure — is not a permitted reading.

Decisive quotation, §20.2 [R-WRT-02] lines 2721–2726: "A creator MUST follow
`[R-LIF-02]`'s creation path: the front signature block; each layer's stored
tiles, tile-index region, and any record extents, in any order satisfying
§5.2's coverage classes (`[R-CNT-02]`, `[R-CNT-03]`) and every declared
layout invariant (`[R-SLB-01]`, `[R-SLB-03]`) — **placement is otherwise
free** (`[R-SLB-05]`)."

Corroborating: §5.2 line 590 lists "alignment and slab gaps" as slack;
[R-CNT-02] requires only that claimants partition without overlap, never that
byte 16 be claimed; and §20.3 step 4 line 2758–2760 gives the append analogue
— "writing begins at exactly F; new stored tiles and record extents follow,
each byte classified under §5.2" — which must permit a leading gap, since an
aligned layer with A ≥ 512 could otherwise never be appended to (F is only
64-aligned). Reading (i) would also require a register row that §21 does not
have, which the reporter noticed. The reporter picked the stricter reading
and paid for it; nothing in the document required that.

### 8. Over-long pre-trailer pad (writer-04, verifier-01) — CONFIRMED, not byte-level

Both reporters are right that step 5 is a MUST, that an over-long pad is
byte-visible from the trailer alone, and that no register row exists.

Decisive quotation for the file's status, §6.2 [R-CNT-05] line 706: "**a
longer gap is conforming, and no conforming commit produces one**." That
settles verifier-01's fork outright: a verifier certifies (absent other
violations), and refusal is not available.

Decisive quotation for the actor's status, §2.3 [R-CNF-02] lines 143–146: "A
writer obligation **whose violation this specification expressly declares not
to be a file-conformance violation** — §6.3's flags = 0 against a set
ignore-lane bit — binds the actor in the same way." That clause is a general
test with one illustration, not a closed list, and §6.2 expressly declares.
So writer-04's "unnamed fourth member" is a member of a class the rule
already defines by test, not an exception the rule fails to cover.

What survives, and it is real: [R-CNF-07] (line 212) and §21.1 (line 2974)
both say "detectable violation" unqualified where they mean "detectable
*file-conformance* violation". An over-long pad is a detectable violation of
a named MUST that the register omits by design, which reads as a
counterexample to a normative completeness claim. Editorial, and the repair
is a two-word qualification in each place.

### 9. Appendix G's unclosed freedoms (writer-05) — CONFIRMED, not byte-level

Item 3 (lines 3758–3764) fixes an emission order and explicitly notes that
"structure placement (`[R-LIF-02]` step 2)" is otherwise free — it does not
say sequentially with no gaps. It orders top-level records ("Records are
ordered by type, and within type 0x0001 by layer name") and says nothing
about sub-record order inside a layer record's inline payload, where
[R-CNT-14] makes order meaningless and a layer can carry a user-metadata
sub-record beside unknown ones. The closing paragraph (3782–3785) cites
[R-TYP-06] (fill is *recorded*) and not [R-TYP-10] (line 1596–1599: "a writer
whose caller does not choose a fill SHOULD record all-zero bytes. A writer
that defaults differently still emits a conforming file"). All three gaps are
real, and the third changes the reference array, not just the bytes.

Downgrade quotation, Appendix G opening lines 3735–3736: "It adds no
requirement to any actor: **a writer ignoring it is fully conforming**", and
the appendix heading itself is "(non-normative)". No conforming
implementation's emit set or verdict changes. The repair is a maintainer
decision about what the profile should require, so I graded severity
design-decision rather than editorial.

### 10. §20.3 example (c) (verifier-02, diagrams-01) — CONFIRMED, not byte-level

Line 2835–2837: "**(c) A change confined to the directory** — clearing a slab
declaration, renaming a layer, changing a channel's fill value. Only the
directory is re-emitted." Against [R-SER-05] line 1832–1841: "at every
padding position, a writer MUST encode … that channel's fill value … Every
pad bit (§14.3) MUST carry the plane's channel's fill bit … a verifier MUST
check it, and a violation is a validity error at tile scope." T4 (line 3134)
says "that channel's **recorded** fill value" — the fill recorded in the live
layer record — and conformance is a predicate on the live bytes.

I re-derived both reporters' padding counts independently. verifier-02's file
(extents 3×3, tiles 2×2, interleaved, one uint8 channel, row-major in-tile
ordinal): tile (0,0) no padding; tile (0,1) padding at in-tile ordinals
{1,3}; tile (1,0) at {2,3}; tile (1,1) at {1,2,3}. Seven padding bytes across
three tiles. Correct. diagrams-01's file is §14.5's own worked layer (extents
(5,5), tiles (4,4)): 0, 12, 12, 15 padding positions. Correct. §14.3's plane
with P = 10 does have six pad bits per tile and the example gives both
encodings (`55 01` / `55 FD`), so the packed-bool case needs no edge padding
at all. Both reporters are accurate.

Downgrade quotation, §2.1 line 102–104: "All text in this document is
normative except: §1 (Introduction); **any text labeled *Note*, *Example*, or
*Rationale***". The block is labelled "> **Example — the three shapes a
commit takes.**". [R-SER-05] therefore governs and no conforming
implementation's emit set moves. This is nonetheless the highest-priority
editorial item in the round: the example invites an updater author to build
a `set_fill()` that emits files every verifier condemns tile by tile, on
exactly the layers where fill matters.

### 11. §15.3's slack gloss (verifier-03) — CONFIRMED, not byte-level

Line 1919–1921: "and none to `[R-LIF-08]`'s coverage walk, whose slack total
therefore includes whatever bytes such an entry nominally addresses." I
checked the six structural rows: for the T8 shape the nominal bytes lie
inside [0,16), which §9.7 lines 1238–1240 expressly claim for the walk; for
the T9 shape they run past F − 64 and can run past the physical end; for T11
and T12 the nominal extent is not representable. So the gloss is false as
written in four of the six shapes and trivially true only in the T10 shape.
That is a genuine contradiction with §9.7, not merely a loose paraphrase.

Downgrade quotation, §9.7 line 1242–1243: "**Bytes the walk does not reach
are slack: the verifier sums them and reports the total**, and their content
is not its concern." Slack is defined as the set complement of the walk, so
the arithmetic is settled and reading (i) is not merely different but
impossible. §5.2 line 594–595 makes the slack total a report figure, not a
verdict: "no conformance requirement applies to it … a verifier MUST report
the total number of slack bytes".

### 12. "Unable to check" is unscoped (verifier-04) — PARTIAL, not byte-level

The observation is fair: [R-CNF-11]'s clause carries no scoping and the five
illustrations are introduced with "as when". But the reporter says the scope
is "decidable only by a reductio", and it is not.

Decisive quotation, §2.3 [R-CNF-11] lines 198–202: "A verifier MUST report
each requirement it was unable to check, naming the requirement and the
ground, whichever of the three verdicts it reports; **that per-requirement
report constrains the report and not the verdict**, as *unexamined* does
below." And line 197–198: "*cannot establish* is **available** only to a
traversal that established no violation" — permissive, not mandatory.

So even on the broad reading the verdict does not follow from the report, and
the conforming-verifier class is not emptied. The residual defect is that the
clause's ground is unstated and would read better as "on a capability or
resource ground". I graded PARTIAL because the reporter is right about the
gap and wrong about its consequence.

### 13. Appendix H's verifier checklist (verifier-05) — CONFIRMED, not byte-level

Reproduced the count independently (20 verifier rows; checklist reaches 17).
F9, F39 and L26 are the three missing. Item (1) is the interesting one: a
stored tile placed in the pre-trailer gap is a claimant, is disjoint, lies
within [16, F − 64) and verifies against its own crc, so §9.7's three stated
checks all pass and only [R-CNT-05] fires. Item (2) is straightforwardly
right: the checklist's "record flag bits" line covers F28/F29/F31/L47/L48/L50
but no type-value row, and F38/L25 (the MU = 1 specialisations) are reader
rows, so a checklist-derived verifier accepts a reserved-range MU = 0 record
silently. Item (3) is weaker than the reporter allows: Appendix H's verifier
entry opens "every reader obligation, plus …", and T3/T24/T25 are
reader-assigned, so they are covered by the first clause; what survives is
only that a *reader's* obligation runs at tile use for tiles it reads while a
verifier owes all tiles.

Downgrade quotation, Appendix H lines 3790–3791: "§2.3 defines the classes;
**each entry's authority is the requirement or section cited, never this
summary**", under a heading marked "(non-normative)".

### 14. §7.4's missing class column (diagrams-02) — CONFIRMED, not byte-level

Verified by grep (see mechanical checks). §4.7's note lines 505–510 promises
"Layout tables in this document give, per field: byte offset within the
structure, size, type, name, **taxonomy class**, and valid range" — and
§7.4's table gives neither offset nor class, though it is the table defining
the most fields. [R-ENC-16] line 498–499: "**Every** field this specification
defines is classified structural, semantic, or informative." Fifteen layer
record fields carry no class anywhere (linearization, channel sample type and
fill are classified in prose at §11.4, §12 and §13.1).

Downgrade quotation, [R-ENC-16] lines 499–502: "A field classified
**informative** MUST NOT affect how any byte is located or decoded, and a
reader MUST NOT alter decoding based on it." That prohibition is the only
behaviour the taxonomy attaches, and none of the fifteen is a candidate for
the informative class — each has an explicit normative role in locating or
decoding bytes. So no decode or validation differs.

### 15. Appendix H's writer SHOULD (diagrams-03, quiz-03, adversary-04) — CONFIRMED, not byte-level

I checked each of the eight writer-checklist items against its citation.
Seven are MUST-level; the sixth cites [R-CNT-03], a SHOULD.

Downgrade quotations: §5.2 line 593–594 — "Slack has no internal structure
this specification defines, **its content is unconstrained, and no
conformance requirement applies to it**"; [R-CNT-03] line 610–611 — "**no
conformance requirement rides on slack content either way**"; §21.6's slack
row line 3197 registers it as a defined non-violation. Appendix G line
3782–3783 draws the distinction correctly for the same rule, so two
non-normative appendices give one SHOULD opposite treatments — which is the
sharpest form of the finding and the reason it is worth an edit.

adversary-04's second half (the reader checklist dropping the fifth
[R-CNF-03] clause) is the same defect diagrams-06 reports; noted there.

### 16. §21.9's limits inventory (diagrams-05, register-05) — CONFIRMED, not byte-level

[R-ERR-03] line 3264–3265: "Every limit affecting which files are valid, or
which files a conforming reader accepts, **lives here** (`[R-CNF-10]`)."
[R-ERR-05] lines 3308–3316 enumerates four hard limits and closes "Each is a
consequence of a field's width, an external format, or the value domain —
**never a number chosen here**."

Verified omissions that affect validity: per-tile A, "a power of two with
512 ≤ A ≤ 2⁶²" (§16.1 line 2003–2004; row L40); A_slab, power of two in
1 … 2⁶² (§7.4 line 960, §16.2; row L30); the 128-byte floor ([R-CNT-27] line
532–536; row F7); dir_offset ≥ 16 and dir_length ≥ 4 (§6.2 table; rows F11,
F18). Verified counterexample to the closing generalisation: §16.1's own note
line 2016 — "**512 is the legacy sector floor**" — a number chosen here, not
forced by a field width. Verified Appendix B does carry both alignment rows
while §21.9 does not. Verified register-05's second sub-claim: [R-ERR-05]
attributes the 255-byte cap to "a `u8` length prefix", which holds for §7.4's
length-prefixed names but not for user-metadata keys, which §18.2's fourth
restriction subjects to the same cap and which are JSON strings with no
prefix (row R10).

This is more than editorial because [R-VEC-03] line 3531 binds corpus
construction to the enumeration: "every sentinel, every boundary value, and
**every hard limit of `[R-ERR-05]`** has one at its stated bound." A short
enumeration is a short corpus.

Downgrade quotation, [R-ERR-05] line 3308–3310: "Some limits are instead
**hard**: a file violating one is invalid, not merely large. **They are
stated where the structures forcing them are defined**" — which concedes that
"lives here" means [R-CNF-10]'s "lives in this specification", not "lives in
§21.9". §7.4's constraint column, §16.1 and §16.2 state the alignment bounds
normatively and [R-CNT-23] assigns the outcome, so no emitted or accepted
byte moves.

### 17. Appendix H's reader checklist (diagrams-06) — CONFIRMED, not byte-level

§2.3 [R-CNF-03] lines 155–157 names five: codecs, filters, both layouts,
sample types, "and every user-metadata encoding §18.2 assigns"; the
no-subset sentence names all five again. Appendix H line 3803–3804 names
four.

Downgrade quotation, §18.2 [R-MTA-03] lines 2321–2324: "Both assigned
encodings are core: a conforming reader MUST be able to decode encoding 2,
**whose decoder `[R-COD-11]` already requires of it for codec 3**." Encoding
1 is verbatim storage. So the four listed capabilities entail the fifth and
no implementation differs. Same appendix disclaimer as group 15.

### 18. F21 (register-01, adversary-03) — CONFIRMED, not byte-level

§21.2's heading line 3022: "File-scope violations. Outcome: reject-file. 39
conditions." §21.1 line 2970: "each row is one malformed condition." F21 at
line 3046. §21.6 lines 3224–3228: "In both the outcome records a reader's
capability, not a defect in the bytes … the first is registered as F21,
**whose condition records only the reader's outcome and not a defect in the
bytes**." That is the register contradicting itself by row number.

I checked both consequences the reporters draw. [R-VEC-04] line 3523: "every
vector built from §21's register is nonconforming" — false if F21's vector is
not a nonconforming file. [R-VEC-02] line 3495: each manifest records
"whether the file is **conforming**" — and for a version_major = 2 file this
document supplies no answer, since §6.2's table defers to §6.3, §6.3 treats
an unimplemented major as a reader-capability matter without calling the file
invalid, and §21.6 says it "can be perfectly conforming under that major".
Both consequences hold up.

Downgrade quotations: §21.1 line 2979–2980 — "where a row and the rule it
cites diverge, **the rule governs**"; [R-CNT-07] line 734–735 — "A reader
MUST reject-file when version_major is 0 (invalid) or is a major it does not
implement", which reserves "invalid" for 0 alone and says nothing about file
conformance; §2.3 line 185–186 — cannot establish "as when the file names a
format major version it does not implement". Note also that both candidate
verdicts (*nonconforming* and *cannot establish*) equally bar certification,
so unlike adversary-01's construction there is no divergence at all in what
any implementation does with the bytes — only in the label.

### 19. L24's Detected cell (register-02) — PARTIAL, not byte-level

I could not sustain the contradiction as stated. §19.1 step 4 lines 2531–2535
assigns the open a *namespace-exclusion decision*, not an error report: "a
layer record whose name field does not lie entirely within that record's
inline_length yields no name field to compare, so it **contributes no name to
the namespace** and is instead a validity error at layer scope
(`[R-CNT-18]`)." It states the scope, not the tier. §19.2's tier list item
"the layer-name namespace (§19.1's steps)" is the namespace check (F6,
reject-file), which is at open and unaffected.

Decisive quotations: §19 preamble lines 2490–2492 — "§21's register is, and
`[R-CNF-04]` binds a reader to every register row whose detector is the
reader, **at the tier that row's *Detected* cell names**"; [R-RDR-02] line
2574 — "A reader MAY detect any violation earlier". A reader necessarily
*determines* the overrun at open (it must, to know whether a name is
contributed) but is not obliged to *surface* the layer-scope error until
layer access. That is coherent and implementable, contra the reporter's
"(1) is not implementable".

What survives, and is worth a maintainer's eye: L4, L6 and L7 — three
layer-scope conditions on the same name field — carry Detected = "open",
while L24's name instance carries "layer access". A reader that must parse
the name at open to run L4/L6/L7 has already established L24's name instance.
The asymmetry is bookkeeping, not a contradiction.

### 20. No tile-scope [R-ENC-06] cause row (register-03) — CONFIRMED, not byte-level

Verified: no §21.4 row cites [R-ENC-06]; F5 (line 3030) and L3 (line 3075)
both exist and both describe themselves as recording "the cause rather than a
procedure of its own". §15.1 line 1867–1869 makes the entry's owning scope
the tile, so [R-ENC-06] names a tile-scope condition. The condition is
constructible with the 20-byte entry size preserved (so [R-CNT-17]'s
region-length cross-check does not fire) and is then detectable through
T1/T8/T9/T11/T12 exactly as F5 and L3 concede of themselves. §21.1 line
2974–2976 makes completeness normative. The omission is a real asymmetry
against the register's own practice (T13 and T26 are cause rows too).

Not byte-level: every file exhibiting it is already rejected at the tile on
grounds the document states. Adding the row moves §21.8's totals to 126/253.

### 21. L2's collapsed containers (register-04) — CONFIRMED, not byte-level

Verified L1 (line 3073) enumerates four instances across the two containers,
L16 (3088) four, L17 (3089) and L18 (3090) two each; L2 (3074) gives a single
"extent_offset + extent_length". §21.1 lines 2996–2999 names "a container it
can occur in" as an instance and lines 3007–3011 exclude only the *fields* of
a single predicate. So collapsing the two fields is right and collapsing the
two containers is not: [R-CNT-13] line 879–880 covers "the layer for a layer
record and for sub-records". Two distinguishable files, one vector under
[R-ERR-02].

The reporter's two secondary observations check out (T3's six instances from
a one-equality condition at line 3133; L42's "—" from a three-alternative
condition at line 3114) and are offered as evidence of judgement, not as
defects. Not byte-level: instance counts drive corpus construction only.
Repair moves §21.3 to 103 and the total to 253 — note this composes with
group 20's row, so the maintainer should apply both before restating totals.

### 22. preserve-verbatim never bound (register-06) — CONFIRMED, not byte-level

Two occurrences, both §2.4 (lines 216, 226). §20.4 carries the substance in
prose ("Retain byte-identical" in all three rows; [R-WRT-05] line 2852–2856
"MUST re-emit byte-identically") without ever using the term. §21 correctly
carries no preserve-verbatim rows, since [R-CNF-07] line 212–214 restricts
the register to reader outcomes. Vocabulary hygiene; nothing behavioural
depends on it.

### 23. Conduct-rule carve-out (adversary-01, adversary-02) — PARTIAL, not byte-level

adversary-02's factual half is right. §2.3 [R-CNF-02] lines 139–146 glosses
its carve-out as "where a value is published, or which registry version a
writer targets (§10.3, §18.3)" plus one further named case, and neither
[R-COD-06]'s undisclosed-dictionary prohibition (line 2151–2159) nor
[R-COD-10]'s stride prohibition (line 2253–2258) is either of those. I
verified T26's condition text limits it to the cases with a structural
witness (line 3156) and that adversary-01's f3.bin construction — G = 1 so no
padding positions, two uint16 channels so no bool bytes — leaves T26 unable
to fire. The byte-identity argument is sound: shuffle₂(D) = shuffle₄(D′) for a
D′ that is a perfectly good decoded image, so the bytes carry no witness.

But the conclusion — that file conformance is therefore not a byte predicate,
and that a verifier's verdict forks — does not follow.

Decisive quotation, §2.3 [R-CNF-02] lines 136–139: "**File conformance is a
pure predicate on bytes: it does not depend on any reader, writer, or
environment.**" W1's bytes are uncontroversially conforming; W2's bytes are
identical; conformance does not depend on the writer; therefore W2's file is
conforming. The carve-out enumeration is an illustration of that principle,
not the source of it, and reading a short illustrative list as exhaustive
inverts the logic. Its closing clause states the operative test outright:
"**conduct rules bind the actor, the predicate binds the bytes**."

Second decider, for adversary-01's Reading B specifically, §2.3 [R-CNF-11]
lines 200–202: "**that per-requirement report constrains the report and not
the verdict**." Once the file is conforming, [R-COD-10] is not a file-level
requirement the verifier owes a check on, and even a verifier taking the
broad reading of "unable to check" does not thereby lose the *conforming*
verdict.

What survives: [R-CNF-02]'s illustrative enumeration is under-inclusive and
would be safer as the general rule adversary-02 proposes ("a writer
obligation with no witness in the emitted bytes binds the actor, not the
predicate"), or with §17.2 and §17.3 added to the list. I graded PARTIAL: the
enumeration gap is real; the byte-level consequence is not.

### 24. §9.7's check list omits F9 (quiz-02) — CONFIRMED, not byte-level

§9.7 lines 1234–1238 states three checks: disjointness, the [16, F − 64)
bound, and each claimant's checksum. F9 (line 3034) is a verifier-detected
reject-file row that none of the three catches: a structure in the
pre-trailer gap is a claimant, is disjoint, lies inside [16, F − 64), and
verifies. Deciding it needs exactly the claimant inventory the walk produces,
so the check belongs beside the walk and is stated two sections earlier
instead.

Downgrade quotation, §6.2 [R-CNT-05] line 707–708: "**A verifier MUST treat a
structure in that gap as a validity error at file scope**, and counts the rest
as slack." The obligation is unambiguous where it is stated and §21.1 makes
[R-CNT-05] govern F9, so no two conforming verifiers can defensibly disagree.
The cost is that §9.7 alone is an incomplete build sheet — which is also
verifier-05's item (1), reached from Appendix H rather than from §9.7.

## Honest gaps

- I did not recount §21's 252 instance cells one by one; I checked the
  reporters' subtotals sum to the stated figure and spot-checked the cells
  register-04 names.
- I did not execute any reporter script or open `f3.bin`, `gen*.bin`,
  `worked.tarn`. Where a byte-level claim rested on a built file
  (adversary-01/02, verifier-02, diagrams-01, verifier-03) I re-derived the
  arithmetic on paper from the spec's own formulas and it reproduced in every
  case.
- Group 5 (writer-01) is the judgement I hold with least confidence. The
  harmonizing reading — that "remains permitted" is scoped to §20.4's own
  obligation and leaves [R-CNT-15]'s reject-file intact — is available, and
  on that reading the defect is unreachable text rather than a fork. I kept
  the byte-level flag because I could not produce a single sentence that
  decides it and the brief forbids a downgrade without one. A maintainer
  re-read of §20.4's MU = 1 row against §20.3 step 2 would settle it cheaply.
