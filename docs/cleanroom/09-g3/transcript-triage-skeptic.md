# Round 9 triage — skeptic lens — working transcript

## 0. What I read and ran

Read in full or in the cited ranges, from `/Users/robertkleffner/Documents/GitHub/tarn/spec/tarn.md`:

- front matter + "How to read this document" (lines 1–91)
- §2 Conformance in full (92–268), including §2.3's five classes and §2.4's outcome table
- §4 Encoding conventions in full (359–525), incl. §4.6 names and §4.7 field taxonomy
- §5 File anatomy and byte coverage in full (526–649)
- §6 Front block / trailer / version gates / remote accounting (650–824)
- §7 Directory and records in full (825–1024)
- §8 Integrity (1025–1067)
- §9 Lifecycle in full (1068–1271), incl. §9.7 coverage verification
- §10 Extension points (1272–1361)
- §13 Fill and sparse tiles (1584–1679)
- §14.2's `[R-SER-08]` block (1730–1760)
- §15 Tile index in full (1876–2000)
- §16 Slabs and alignment (2001–2100)
- §17.1–§17.2 (2101–2204)
- §18.1–§18.2 (2300–2419)
- §19 Reading in full (2494–2704)
- §20 Writing and updating in full (2705–2980)
- §21 in full (2981–3347)
- §23 Privacy (3449–3508)
- §24 Conformance test vectors (3509–3583)
- Appendices A, B, C, D, E, F, G, H (3588–3892 to the end of what §21/§24 reference)

Read from `.../round9/`: `transcript-diagrams.md` only (to recover the content of the
`diagrams-01` placeholder — see §1 below).

Ran one script: a mechanical recount of §21.2–§21.5's Instances cells
(cell `—` = 1 instance, otherwise semicolon-separated items). Result:
**125 conditions, 253 instances** — F 60, L 103, T 46, R 44 — which matches
§21.8's stated "125 conditions over 253 instances" exactly as the cells are
written. That number is load-bearing for three findings.

Not read (per the access rules): `docs/`, `PLAN.md`, `AGENTS.md`,
`conformance/`, `spec/registry.json`, git history, the web.

## 1. An input-integrity problem I must disclose first

`diagrams-01` arrived as a **placeholder**: Location `x`, title `y`, body `z`,
quote `q`, byte-level rationale `r`. There is no content in it to evaluate.

I read `transcript-diagrams.md` (permitted) and found that the diagrams pass
actually produced **eight** findings, `diagrams-01` through `diagrams-08`:

- `diagrams-01` = "Appendix G promises to close gap *content* and no item does"
- `diagrams-02` = "L47, L48 and L50 do not apply §21.1's own instance arithmetic; §21.8's 253 is short by 4"
- `diagrams-03` = Appendix H's verifier checklist drops the pad-bit obligation
- `diagrams-04` = Appendix H's reader checklist states the acceptance duty wider than §2.3
- `diagrams-05` = §4.7's Note promises a worked example the layer record's inline payload lacks
- `diagrams-06` = §19.1 step 4 cites `[R-ENC-12]` where `[R-ENC-13]` is the rule
- `diagrams-07` = §20.4's preservation table carries no requirement identifier
- `diagrams-08` = Appendix B omits one of `[R-ERR-05]`'s hard limits

Only `diagrams-01` reached this triage input, and it reached it stripped.
Seven of that pass's findings were never presented to me and are therefore
**not** in my output; `diagrams-02` duplicates the register-03/adversary-02
group and `diagrams-07` is adjacent to register-08, so at least two of the
seven would have been consolidations rather than new defects — but
`diagrams-03` through `diagrams-06` and `diagrams-08` are unrepresented here
entirely. This is the same class of failure the round-6/7 post-mortems
recorded. **The reconciler should treat the diagrams pass as not having been
triaged.**

Because the transcript identifies `diagrams-01` unambiguously as the Appendix G
gap-content defect, and because dropping an id is not permitted, I placed
`diagrams-01` in the gap-content group rather than in a null group. That is a
judgement made from the transcript, not from the input text I was handed.

## 2. Method

Default: the finding is wrong and the document decides it somewhere the
reporter did not look. For each, I hunted for the foreclosing sentence and
quoted it. Where I could not find one, I said so and graded accordingly.
Every downgrade of a self-flagged byte-level finding carries a quotation.

## 3. Grouping decisions

29 groups over 41 ids. The consolidations:

- **appendix-g-gap-content**: reader-01, writer-02, quiz-01, diagrams-01. All
  four are "the closing paragraph names gap *content* as one of four things
  the items add, and no item adds it; the pre-trailer pad is unavoidable."
  writer-02 carries a secondary claim (the §18.2 `encoding` field is not
  pinned either) which belongs to the *undercount* defect; I record it there
  rather than splitting the id.
- **appendix-g-file-id-hash**: reader-02, writer-04, verifier-05. Identical:
  item 2 names no hash function, no digest→u64 reduction, no exact byte
  string, no zero-digest fallback.
- **appendix-g-four-things-undercount**: verifier-06, register-09. Identical:
  items 6, 8 and item 3's top-level record order each close a freedom that is
  neither mandatory nor among the four. Opposite direction from the
  gap-content defect, different repair, so a separate group.
- **f1-version-major-instance**: reader-03, register-01, adversary-01. Same
  defect from three angles. reader-03 additionally attacks F1's *generation*
  instance; that sub-claim is refuted inside the group (see §4.5).
- **field-taxonomy**: reader-05, writer-08, quiz-02. All three raise the same
  pair (empty informative class; name fields' class underdetermined).
- **sec-21-7-witnessless-list**: writer-06, register-05. Both are "§21.7's
  second paragraph under-enumerates against the role §21.1 assigns it";
  different examples, same sentence, same repair.
- **instance-count-container-split**: register-03, adversary-02. Identical
  arithmetic, identical 253→257.
- quiz-03 is *not* grouped with the above: it attacks different cells (F32,
  L16, L23) in the opposite direction (over-enumeration against §21.1's
  single-predicate exclusion) and needs a different repair.

## 4. The judgements, with the text that decides them

### 4.1 Appendix G — the whole cluster (groups 1–4, 10 ids)

Every Appendix G finding is downgraded on one sentence, and all nine
reporters had already conceded it:

> "### Appendix G — Reproducible-writer profile (non-normative)" … "It adds
> no requirement to any actor: a writer ignoring it is fully conforming"

with §2.1: "All text in this document is normative except: §1 (Introduction);
any text labeled *Note*, *Example*, or *Rationale*; and appendices identified
as non-normative. `[R-CNF-01]`"

So no byte a conforming implementation may emit, and no file it must accept or
reject, turns on any of it. §5.2 independently settles the pad: "Slack has no
internal structure this specification defines, its content is unconstrained,
and no conformance requirement applies to it."

**But the defects themselves are real, and I verified each rather than
accepting the account:**

- *Gap content.* I read items 1–9. Item 3 closes gap **extent** and concedes
  the content question in the same breath ("order alone does not fix bytes
  while the space between structures is free"); item 5 removes the
  alignment-forced gaps; nothing addresses the bytes. The pad is unavoidable:
  item 3 fixes contiguity from offset 16, so the directory's end offset is
  determined by content, and `[R-LIF-02]` step 5 pads to the next 64-byte
  boundary. Appendix A's own 128-byte file carries a 44-byte pad at [20,64).
  Under item 2 the pad feeds the `file_id`. **Confirmed.**
- *file_id hash.* Item 2 names "a cryptographic hash" and nothing else, while
  items 1 and 9 both close their freedom by naming an implementation at a
  version. The sharpest internal contradiction is item 1's own boundary
  claim — "codec 1 is reproducible by anyone" — which is false while item 2's
  hash is unpinned. `[R-CNT-06]` requires `file_id ≠ 0` and item 2 has no
  fallback. **Confirmed.**
- *"Four things" undercount.* I checked each claimed extra freedom against the
  core text. Item 6: nothing in `[R-IDX-02]`/`[R-TYP-08]` requires an all-fill
  tile to be unstored — I read §13 in full — so storing one is conforming and
  item 6 closes a real freedom. Item 8: `[R-CNT-26]` is "A writer SHOULD emit
  the lowest version_minor…", the same category as `[R-TYP-10]`, which *is*
  one of the four. Item 3's top-level record order: `[R-CNT-14]` leaves both
  record and sub-record order free; the closing paragraph names only
  sub-record order. writer-02's `encoding`-field point lands here too: §18.2's
  1-or-2 choice is not pinned and is not among the four. **Confirmed, and at
  least four short, not three.**
- *Item 3's emission order.* Reading (a) leaves two layers' type-0x0002
  sub-record extents unordered against each other, because "ascending record
  order" is defined as "by type, and within type 0x0001 by layer name" and
  sub-record order is defined only *within* one layer record. Reading (b)
  puts "then the directory" inside the per-layer loop, which is impossible.
  Additionally "their order of creation" is not a function of the input at
  all, and in format major 1 it is vacuous: `[R-CNT-14]` permits at most one
  user-metadata sub-record per layer and no other sub-record type exists.
  **Confirmed.**

### 4.2 §4.7 field taxonomy (group 7: reader-05, writer-08, quiz-02)

I checked every Class cell in the document (§6.1, §6.2, §7.2, §15.1, §18.2):
structural ×19, structural (reserved) ×1, semantic ×2 (`generation`,
`file_id`). No cell reads *informative*. The word occurs three times, all
inside the definitions. **The class is empty; confirmed.**

Downgrade quotes. The taxonomy has exactly one operative clause, and it binds
only the empty class:

> "A field classified informative MUST NOT affect how any byte is located or
> decoded, and a reader MUST NOT alter decoding based on it; each informative
> field's definition states what a reader does when it contradicts the data it
> describes. `[R-ENC-16]`"

And the delegation the reporters call underdetermined is **inside a Note**,
which §2.1 excepts from normativity:

> "> **Note.** Layout tables for fixed-layout structures give, per field: …
> its table omits the offset and class columns, and each field's class follows
> from the definitions above."

So no normative requirement obliges anyone to derive a class for a name field,
and no rule anywhere keys off the class. reader-05's extra claim that
`generation` and `file_id` are mis-classed does not survive either: the glosses
they measure against ("affects what decoded values mean") live in §1's *How to
read this document* note, which §2.1 makes non-normative, and §4.7 itself
supplies no definitions at all. Not byte-level. Editorial.

### 4.3 Updater dropping a layer record (group 8: writer-01, self-flagged byte-level)

Tried hard to kill and succeeded. §20.4 decides it in terms:

> "Persistence governs every record type; only the authoritative source of the
> flags differs. For a type §7.3 registers, the registry's fixed flags govern
> rather than the stored ones (`[R-CNT-22]`) — both registered types carry
> PE = 1, so neither can be dropped, and implementing a record's type confers
> understanding of it, not permission to drop it."

The claimed contradiction with §2.3 does not exist. `[R-CNF-06]` reads: "An
updater MUST satisfy every writer requirement for the bytes it produces, and
**additionally** MUST honor the preservation obligations of Part I for records
it does not understand." That is an additive floor; it grants no permission,
and "and additionally MUST Y" is not "and nothing else". §20.4 imposes more,
and both hold.

The claimed mislocation also fails: §7.2 `[R-CNT-12]` ("never silently
deletable") and §7.3's registry fixing PE = 1 are Part I, so "the preservation
obligations of Part I" is accurate.

Appendix H's "respects unknown records' MU and PE bits (§20.4)" does side with
the narrower phrasing, but Appendix H is non-normative and disclaims itself:
"each entry's authority is the requirement or section cited, never this
summary."

**Not byte-level** — there is no fork; the text resolves it. What survives is
a design question the maintainer should confirm deliberately: as written, no
defined operation removes a layer from a TARN file, ever, including
compaction (§20.5 drops only "any record §20.4 lets it drop"). §23.1's "a
commit that removes data removes only its *reachability*" and §20.4's
rationale ("differ exactly by those modified, added, or dropped") both read as
if deletion were available; they are satisfiable by tile supersession and
MU=0/PE=0 drops, but a reader of those two sentences will expect otherwise.
Graded PARTIAL / design-decision.

### 4.4 Front-block residency (group 6: reader-04) — the closest call in the set

This is the group I came nearest to upholding as byte-level, and I want the
reconciler to see why.

The fork the reporter constructs is real in shape: given a file whose byte 0
is 0x88, an mmap reader rejects and a pread-only local reader serves, and
"must reject" is exactly the byte-level test's vocabulary. `[R-CNT-04]`'s own
example list names "a local file" as a residency case, which is the reading
that obliges the pread reader.

Three sentences decide it against that reading, and all three are in the
requirement itself or in its register row:

> "That distinction governs the request accounting of §6.4 and nothing else;
> the obligation over the front block turns on residency instead, because a
> transport can be classified either way at the margin while residency is
> decidable at any reader's own open path."

> "The test is residency, not transport, so an implementation decides it at
> its own open path without having to classify the network underneath it."

> §21.2 F8: "the obligation binds a reader holding those bytes resident, and a
> reader that would have to fetch them MAY defer or omit the check"

The first sentence is decisive: the local/remote axis — where "a local file"
lives as a category — is expressly confined to §6.4 and excluded from this
obligation. So "a local file" in the residency list is drafting residue from
the axis the paragraph above it just abandoned.

Second downgrade ground: the fork only ever appears on a **nonconforming**
file. §2.4 `[R-CNF-12]`: "For a nonconforming file no acceptance obligation
exists — a reader MAY reject it upon detecting any violation." On every
conforming file both readers behave identically. So no conforming byte
sequence changes its treatment.

Not byte-level — **but the two-word edit should be made anyway**, and I would
not defend the current wording to an implementer.

### 4.5 F1's version_major instance (group 5: reader-03, register-01, adversary-01 — two self-flagged byte-level)

The other group I tried hardest to kill, and here the *defect* survives while
the *byte-level flag* does not.

Verified: `version_major` is a u16 whose only invalid value is 0, and 0 is a
byte-swap fixed point (`00 00` either way). Big-endian 1 is `00 01`, read as
256. So the only distinguishable file the instance can produce declares a
major this document does not define.

Three texts converge, and the decisive one is §2.3:

> "This document defines format major 1, and a file declaring another major is
> neither conforming nor nonconforming under it: a reader refuses such a file
> on capability grounds (§6.3, `[R-CNT-07]`), and **that refusal is not a
> finding about its bytes**. `[R-CNF-02]`"

> §21.6: "Neither is a register row: the register enumerates file-conformance
> violations (§21.1), and a file this document declines to judge is not one.
> What is registered in each case is the neighbouring condition that *is* a
> violation — version_major = 0 … (F20, `[R-CNT-07]`)"

> §21.1: "each row *restates* its governing rule, and where a row and the rule
> it cites diverge, **the rule governs**."

adversary-01 argues the tiebreak cannot reach F1 because both texts cite
`[R-CNT-07]`. It reaches it: F1 places a capability refusal in a table of
file-scope *violations*, and `[R-CNT-07]` as glossed by `[R-CNF-02]` makes it
not one, so row and cited rule diverge and the rule governs.

Why the byte-level flag fails. Both reporters concede the reader half does not
fork (both reject on the version gate). On the verifier half, §2.3 says
"*cannot establish* is available only to a traversal that **established** no
violation" — and F1's condition is "a multi-byte field is **stored
big-endian**", which cannot be established from `00 01`, because those bytes
are byte-identical to a conforming major-256 declaration. A verifier that
reports *nonconforming* here has not established F1's condition; it has
established `version_major ≠ 1`, which is a different proposition and the one
§2.3 says is not a finding about the bytes. And under either label,
`[R-CNF-11]` bars certification: "a verifier MUST NOT certify a file it
reports that way." No byte sequence's accept/reject status moves.

**reader-03's second half is refuted separately.** It claims F1's *generation*
instance has no witness because a big-endian g ≤ 127 stays inside
`[R-CNT-06]`'s range. F1's own condition text forecloses it: "detectable only
through that field's own value or range gate" — the vector builder picks a
value that trips. Generation 0x80 written big-endian reads 2⁶³, above
`[R-CNT-06]`'s `1 ≤ generation ≤ 2⁶³ − 1`. adversary-01 says exactly this and
is right. So the repair touches `version_major` only.

Graded CONFIRMED / register-bookkeeping. Repair: strike "trailer
version_major" from F1's Instances cell. Note the arithmetic interaction with
group 20: that removal is −1 and the container split is +4, so the corrected
total is **256**, not 252 and not 257.

### 4.6 Instance arithmetic (group 20: register-03, adversary-02; and group 29: quiz-03)

Verified mechanically (script above): the cells as written total 253 across
125 rows, matching §21.8.

**Group 20 is confirmed.** Every other "A layer record's or sub-record's …"
row splits the two containers — L1 (8 instances), L16 (4), L17 (2), L18 (2) —
while L47 (1), L48 (1) and L50 (2) collapse them. L50's file-scope twin F30
enumerates the two flag bits as two alternatives in one container; L50 has the
same two alternatives in two containers and states 2 where §21.1's own worked
sentence gives 4:

> "An instance names a field the condition ranges over, a container it can
> occur in, one of several alternatives the condition text states, or any
> combination of the three — a condition applying to two alternatives in two
> containers has four."

The T24 carve-out ("a family without the condition changing shape") cannot
rescue them without also collapsing L16/L17/L18, which would move the total
the other way. +4 → 257 as written; 256 after group 5's −1.

Not byte-level, on §21.1's own framing: "The **Instances** column enumerates
what a conformance corpus builds for that row (§21.8): **the row is the
rule**, and each instance is one file." The condition, detector, detection
point, outcome and governing rule are unchanged; the four missing files are
already violations under the same row.

**Group 29 (quiz-03) is refuted.** I checked its three cells against §21.1's
exclusion. F32's condition text spells out its two alternatives — "(offset 0
with length != 0, or offset != 0 with length 0)" — and L23's spells out three
— "including slot (0,0) with entry_count > 0, or a nonzero slot with
entry_count = 0". §21.1 counts alternatives explicitly: "one of several
alternatives the condition text states". So the field names in those cells are
labels for stated alternatives, not the excluded case, and L16's four are two
alternatives × two containers, consistent with F32's two. quiz-03 itself
picked this reading. Nothing needs changing beyond an optional rephrase.

### 4.7 The rest, briefly, with the deciding sentence

- **register-02** (§21.3/§21.4 headers assert reader obligations for 13
  verifier-detected rows): confirmed, and §21.1 already states the corrective
  — "For a row whose Detector is *verifier*, the outcome names the scope at
  which the damage is recorded, **not an obligation on any reader**: the
  governing rule states what a reader does, and for several such rows it
  obliges the reader to serve the structure unchanged (`[R-SER-08]`,
  `[R-CNT-22]`)." Verified `[R-SER-08]`: "A reader that neither detects the
  violation nor rejects the tile, and returns the value, MUST report 0x00 as
  false and every other byte as true." So the header gloss and §24's
  `[R-VEC-04]` ("the scope no reader is permitted to serve") are both
  inaccurate for those rows. Not byte-level: `[R-SER-08]` permits serving and
  `[R-CNF-12]` permits rejecting, so both readers are conforming today.
  The reporter's addendum is right too: §21.1's parenthetical omits
  `[R-MTA-05]`, which does the same job for F29/L49.
- **register-04** (no L- or T-scope endianness row): confirmed as a
  completeness gap against §21.1's normative completeness clause. The *outcome*
  question the reporter raises is already decided — §21.1: "Conditions attach
  to the finest structure they damage, and the outcome follows from that
  scope, never from the severity of the corruption" — so a big-endian Eᵢ is
  layer scope, and the check that actually fires is L22 or L2 at layer scope.
  Register-bookkeeping, not byte-level.
- **register-06** (R1 cites `[R-CNT-25]`, not `[R-EXT-03]`): confirmed as an
  incomplete citation. The outcome is not open — §21.5's preamble: "Every row
  here is a violation all the same: the outcome bounds a reader's blast radius
  and never makes the file conforming (`[R-CNF-12]`); §21.6 lists the
  ignore-record conditions that are not violations." Editorial.
- **register-07** (255-byte name cap justified by a u8 prefix that keys lack):
  partial. The mismatch is real, but §21.9 is faithfully restating §4.6, whose
  own bullet already says "at most 255 bytes of UTF-8 (so every name's length
  prefix is a single byte)" over a definition that includes "user-metadata
  keys". So the parenthetical to fix is §4.6's as much as §21.9's, and it is a
  rationale, not a limit. Editorial.
- **register-08** (§21.1 carries no identifier): partial. §2.1 makes §21.1
  normative regardless. §2.2's rule is about "normative requirements", and
  §2.1's Note says "every requirement names the actor it binds (writer,
  reader, updater, verifier, or file)" — §21.1's clauses name no actor; they
  are reading rules for the document, made binding on implementations through
  `[R-CNF-04]` and `[R-CNF-11]`. Citability gap, not a §2.2 violation.
- **register-05 + writer-06** (§21.7's account is incomplete): confirmed as
  editorial. §7.4's Note already supplies the answer for `[R-CNT-18]` ("in
  format major 1 it has no reader-detectable witness, and so no register row")
  and §16.2's Note for `[R-SLB-04]`, which shows the class is handled case by
  case rather than in §21.7. §21.1's "by class" hedge is what keeps this short
  of contradiction. Nothing byte-level: none of the omitted obligations has a
  single-file witness, so §21.1's completeness clause is untouched.
- **verifier-04** (§21.9's hard-limit list omits the zstd window cap and the
  ≥5 extent floor): confirmed. Both are stated unambiguously where they live —
  `[R-COD-06]`: "MUST NOT declare a window size exceeding the tile's decoded
  size; a reader MUST treat either as a validity error at tile scope" — and
  registered (T21, F24, L12), so no implementation that reads the document
  rejects different bytes. Editorial.
- **writer-05** (256 MiB tile vs 8 MiB window under codec 3): partial. The
  join is stated in the requirement a codec-3 writer reads, not left to be
  discovered: "Writers SHOULD keep the declared window within §21.9's 8 MiB
  `Window_Size` guarantee even for a larger tile; a wider window is conforming
  and merely permits a conforming reader to decline the tile or the layer on
  resource grounds (`[R-ERR-04]`)." A §21.9 cross-reference would help; the
  "disproportionately expensive to decide" framing overstates.
- **writer-07** (`[R-WRT-07]` keys regeneration on the region, not the tiles):
  confirmed as a wording defect. The output question is already decided —
  `[R-WRT-07]`'s own closing sentence, "The output's reference arrays MUST
  equal the live generation's bit for bit (`[R-MDL-02]`)", plus `[R-CNF-05]`
  and T1/T9 — so no two *conforming* outputs differ. One-word repair.
- **writer-09** (`[R-SLB-04]`'s trigger omits sentinel→stored): confirmed as
  editorial. `[R-SLB-03]` binds the live state unconditionally — "When
  declared, for every run: the run's stored tiles are contiguous and packed in
  ordinal order … A verifier MUST check these invariants" — and `[R-CNF-05]`
  obliges the writer to emit only conforming files, so the file's validity is
  decided whatever the trigger list says.
- **writer-10** (appender relocation bar carries no keyword): partial. The
  sentence sits inside a step of a procedure the requirement opens with "An
  appender MUST, in order:", and the MUST distributes over the step's content
  exactly as it does over "writing begins at exactly F" in the same step. The
  §5.1 twin the reporter cites is inside an `> **Example.**` block, which §2.1
  makes non-normative, so it adds nothing either way.
- **verifier-01** (compactor: verbatim copy vs conforming output vs latent
  violations): confirmed, and the one place I could not find a disposing
  sentence for the *actor* question. The lean is clear — `[R-CNF-04]`: "a
  violation whose assigned detector is the verifier imposes no reader
  obligation (§19.2, `[R-RDR-02]`)", and §20.1: "certifying the whole file is
  a verifier's office (§9.7)" — but `[R-WRT-06]`'s flat "emits a new
  conforming file" and `[R-CNF-05]` are unqualified, and `[R-WRT-09]` does
  empty §20.1's "neither modify nor rely on" escape for this actor. Not
  byte-level: the output is nonconforming under both readings and
  `[R-WRT-07]` fixes its bytes verbatim. Design-decision.
- **verifier-02** ("the regions the verifier did walk" is undefined):
  confirmed. "Region" is used elsewhere only for the directory region and the
  tile-index region, both claimants rather than walk units, and §9.7 repeats
  the term without defining it. Two verifiers hand an operator different
  mandatory numbers. Not byte-level, on §5.2's own Note: "A partial total
  (`[R-CNT-21]`) reports what one verifier's incomplete walk left unclaimed,
  **which is a fact about that run and not about the file's live state**."
  Design-decision.
- **verifier-03** (traverse past a capability-ground reject-file?): partial.
  The verdict is decided — §2.3: "An established violation takes priority: a
  verifier that has established any violation reports *nonconforming*,
  **however many requirements it was unable to check**", and the class
  definition obliges the look: "A reader that additionally checks every
  file-level requirement — including those ordinary readers are exempted
  from". What remains is that §2.4's reject-file row ("A reader MUST NOT rely
  on any structure in it") is unqualified for verifiers. Editorial.
- **adversary-03** (T14 reads on sentinels): refuted as an ambiguity, confirmed
  as a wording slip. §21.6's table is decisive: "An index entry is the
  sentinel | The tile is addressed but not stored; every sample position it
  carries reads as the channel's fill", under a preamble reading "These are
  defined behaviors, not errors. A reader that treats any of them as a failure
  is the nonconforming party." Plus `[R-IDX-02]` ("not offsets or lengths"),
  §19.4 step 4 ("A valid sentinel short-circuits steps 5 and 6"), and
  `[R-COD-04]`'s own premise ("The stored bytes are the filtered image
  verbatim"), which a sentinel lacks. The slip is real: T8–T12 all say
  "non-sentinel" and T14 does not.
- **adversary-04** (compactor with a failing metadata extent CRC): confirmed as
  an unstated-but-derivable conclusion. The reporter's own verdict is right —
  it converges on refusal, so no conforming implementation diverges. Editorial.
- **adversary-05** (ignore-record "skipped as though absent" vs the coverage
  walk): refuted. §5.2 decides it in the definition itself: "a **structure** —
  a stored-tile extent, a record extent (the bytes any record's extent slot
  references, **whatever the record's type**, §7.2), the directory, or the
  trailer", and §9.7's walk enumerates "each record's extent" with no
  exception. §2.4's own text disclaims the misreading: "the outcome classes
  describe the blast radius of a violation for readers, never degrees of file
  conformance". The reporter agrees the text does not permit the error.
- **adversary-06** (binary64 finiteness boundary): refuted as an
  indeterminacy. The predicate is pinned to binary64 by the rule's own words —
  "A document is unreadable if it contains a number whose **binary64
  interpretation** is not finite" — so "MAY use a wider representation" does
  not move it, and §2.3's "File conformance is a pure predicate on bytes: it
  does not depend on any reader" confirms. Appendix F carries IEEE 754-2019
  normatively. What is left is implementation cost, which the reporter says
  plainly.
- **quiz-04** (over-long pre-trailer pad): refuted. `[R-CNF-02]`'s closing
  clause is a generalisation with an illustration, not a closed list: "A
  writer obligation whose violation this specification expressly declares not
  to be a file-conformance violation — §6.3's flags = 0 against a set
  ignore-lane bit — binds the actor in the same way." `[R-CNT-05]` makes
  exactly such a declaration: "a longer gap is conforming, and no conforming
  commit produces one." The reporter reached the same answer.

## 5. Byte-level count: 0

That is an uncomfortable number to report after round 8's two survivors, and I
want to be explicit that it is not an anchoring artifact. The two groups I
worked hardest to uphold were **f1-version-major-instance** (2 of 3 reporters
flagged it byte-level) and **front-block-residency-local-file** (nobody
flagged it, and I think it is the strongest candidate in the set). Both fail
on quoted text: the first because `[R-CNF-02]` says the refusal "is not a
finding about its bytes" and `[R-CNF-11]` bars certification under either
label; the second because the requirement states its own test twice and
excludes the transport axis by name, and because the divergence only ever
appears on a nonconforming file, where `[R-CNF-12]` leaves no acceptance
obligation for anyone.

writer-01 was the third candidate and dies on §20.4's "neither can be
dropped", which is as explicit as the document gets.

Three groups carry substantive, non-editorial consequence and should not be
filed with the editorial tail: **f1-version-major-instance** and
**instance-count-container-split** (register bookkeeping, and they interact
arithmetically — corrected total 256), and **verifier-01**,
**verifier-02**, **writer-01** (design decisions the maintainer must make
rather than edits an editor can apply).

## 6. Coverage

41 input ids in, 41 out, 29 groups, no id in two groups, no id dropped.
Counted twice by hand and once against the input list. The one thing I could
*not* evaluate is `diagrams-01` as supplied — see §1.
