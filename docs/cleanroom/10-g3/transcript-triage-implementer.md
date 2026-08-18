# Round 10 triage — implementer-consequence lens

## What I read

- `/Users/robertkleffner/Documents/GitHub/tarn/spec/tarn.md` in full (3919 lines),
  by section: front matter, §1–§10, §11–§18 (§16, §18 in full; §11–§15, §17 by
  targeted read), §19–§24, §21.1–§21.9 including all 121 register rows, Appendices
  A, B (head), G, H.
- No round-9/10 reporter transcripts were opened. Every quotation below was
  verified against the spec text directly, not against a reporter's excerpt.
- I did not read docs/, PLAN.md, AGENTS.md, conformance/, spec/registry.json,
  git history, or the web.
- One arithmetic check run by hand (no tooling): register-01's `78 9C` claim.
  0x78 → BFINAL=0, BTYPE=(0x78>>1)&3=0b00 (stored); LEN=0x009C=156,
  NLEN=0xFF63=~156; trailing `01 00 00 FF FF` = final empty stored block.
  zlib test: CM=8, CINFO=7, FDICT=0, 0x789C = 31 × 996. Both readings check out —
  the byte string is simultaneously a valid zlib header and a valid raw DEFLATE
  stream. The reporter's arithmetic is correct.

## Grouping (union-find over shared defect, not shared section)

| group | ids |
|---|---|
| front-block-residency-gloss | reader-01 |
| compaction-vs-declared-layout | reader-02, quiz-02 |
| appg-item3-emission-order | reader-03, writer-07, quiz-05 |
| appg-item2-file-id-hash | reader-04, diagrams-02, quiz-06 |
| appg-gap-zeroing-pre-trailer-pad | writer-02, verifier-04 |
| appg-metadata-encoding-unpinned | writer-03 |
| appg-closing-undercounts | diagrams-01, adversary-07 |
| mta07-cites-217-wrongly | reader-05 |
| preservation-summary-omits-sub-record | reader-06 |
| index-regen-trigger | reader-07 |
| pe0-drop-caveat-attachment | writer-01, quiz-01 |
| field-taxonomy-not-exhaustive | writer-04, diagrams-03, adversary-03, quiz-04 |
| implemented-unregistered-flag-authority | writer-05, adversary-02 |
| appender-duty-on-detected-violation | writer-06 |
| region-undefined-partial-slack | verifier-01, adversary-01 |
| experimental-metadata-encoding-verdict | verifier-02 |
| enc06-no-row-no-account | verifier-03, diagrams-07, adversary-06 |
| checklists-cite-prose | diagrams-04 |
| preservation-table-unlabelled | diagrams-05 |
| section-211-unlabelled | adversary-05 |
| limits-collection-incomplete | diagrams-06, register-03 |
| verdict-vs-outcome-vocabulary | register-02 |
| t15-no-procedure | register-01 |
| l22-instances-cell | register-04 |
| row-labels-unstable | adversary-04 |
| no-record-byte-example | diagrams-08 |
| vec04-verifier-rows | quiz-03 |
| overlong-pre-trailer-gap | quiz-07 |

Merge notes:
- writer-04 / diagrams-03 / adversary-03 / quiz-04 chain transitively: writer-04
  and diagrams-03 both attack generation/file_id's "semantic" label; diagrams-03
  and adversary-03 both additionally attack the name fields; adversary-03 and
  quiz-04 both attack the name fields. One defect: §4.7's trichotomy is not the
  exhaustive partition it claims to be.
- diagrams-05 (§20.4's table has no identifier) and adversary-05 (§21.1 has no
  identifier) are NOT merged. Two different passages, two different repairs.
- writer-02/verifier-04 (gap *content*) and reader-03/writer-07/quiz-05
  (emission *order*) both live in Appendix G item 3 and are NOT merged: they are
  independent gaps with independent repairs.

## Byte-level judgements

Reporters flagged 7 findings byte-level, spread over 6 groups. I uphold 2 groups
(reader-01; writer-01+quiz-01) and downgrade 4, each with the deciding sentence.

### Upheld: front-block-residency-gloss (reader-01)

[R-CNT-04] classifies the same reader twice, in adjacent sentences.

Sentence 1 (residency gloss): "A reader whose open leaves bytes [0, 16)
**resident** — a local file, a memory mapping, a speculative suffix window that
reached offset 0, or any transport already holding them — ... MUST verify the
full block by byte equality before other processing".
Sentence 2 (escape): "A reader that would have to issue a further range request
to obtain those bytes MAY defer or omit the check".
Sentence 3 (disclaimer): "The test is residency, not transport".

§6.1's own definition makes "range" a local term too: "A **local reader** is one
whose transport serves any byte range at no per-range round trip". So a
pread-only local open, which never touches [0, 16), satisfies sentence 2's
condition literally and satisfies sentence 1's gloss by enumeration. Sentence 3
disclaims transport classification while sentence 1's list leads with a
transport. §21.1's row-versus-rule tie-break cannot reach it: the divergence is
inside the rule.

Implementation consequence, both sides concretely:
- Reader A (local pread-only, reads the gloss): preads [0,16), compares, and
  returns reject-file on a file whose byte 0 is 0x88 and which is otherwise
  conforming. Serves nothing.
- Reader B (local pread-only, reads sentences 2–3): never fetches [0,16),
  validates the trailer, walks the directory, serves every sample of every layer.
Same byte sequence, opposite verdicts, each citing normative text. F6's two
conformance vectors (magic bytes [0,8); reserved bytes [8,16)) expect
reject-file, so the corpus cannot be built without the decision. Byte-level.

### Upheld: pe0-drop-caveat-attachment (writer-01, quiz-01)

The sentence: "An appender may drop it only in a commit that *independently*
changes the scope the record attaches to: for a layer sub-record, that layer's
record, index, or stored tiles; for a top-level record, the file's layer set or
another *non-layer* top-level record — a commit that only supersedes a layer's
tiles is not such a change, though it re-places that layer's index region".

Grammatically I think reading B (whole-sentence qualifier) is better supported:
"such a change" is anaphoric to the head criterion before the colon, and the very
next sentence reuses the phrase the same way — "Dropping the record is not itself
such a change". Under B the concession clause does real work: it forestalls the
argument that re-placing the index region, which IS one of the three sub-record
triggers, counts.

But that is my inference, not the document's statement, and the concession's
only referent ("that layer's index region") lives in the branch reading A
attaches it to — which is precisely why two independent reporters both picked A.
No other passage in §20, §7, or §2.4 speaks to it, and §20.4's obligations carry
no register row, so no corpus vector catches a divergence.

Implementation consequence: input file whose layer `sst` carries an unknown
experimental sub-record (type 0x8001, MU=0, PE=0, inline_length 0, extent (E,n));
commit supersedes one `sst` tile. Appender A emits generation g+1 with the
sub-record dropped: `sst`'s layer record shorter by 24 + inline bytes, dir_length
different, directory CRC different, trailer CRC different, extent (E,n) fallen
to slack. Appender B emits it retained byte-identically. Both outputs are
conforming *files*; exactly one actor is a conforming updater and the text does
not say which. Byte-level.

### Downgraded: compaction-vs-declared-layout (quiz-02, reader-02)

Deciding text, all inside §20.5 and §21.3:
- [R-WRT-06]: "Given a conforming input the output is a conforming file."
  (unconditional, two sentences before the placement grant)
- L40: "Alignment A declared and a stored tile's index-entry offset is not a
  multiple of A | — | verifier | certification | [R-SLB-01]"; L41, L42 likewise.
- [R-WRT-07]'s "except that" list is exhaustive over what may differ from
  byte-identical re-emission and names only extent slots, regenerated index
  regions, and crc_of_crc_array — not A, S, or A_slab. So the "clear the
  declaration" escape is closed too, and [R-SLB-04]'s escape binds only "a writer
  or updater whose commit supersedes a stored tile in, or grows the extents of" a
  layer, which a whole-file rewrite is neither.

So the conforming-compactor output set is already determined: honour the
invariants, re-emit S/A_slab/A unchanged. quiz-02's Compactor B emits a
nonconforming file and is therefore not a conforming compactor. Nothing forks.
The defect is that §20.5 states the grant with a §5.2 bound only, while both
sibling subsections cite §16 explicitly (§20.2: "every declared layout invariant
(`[R-SLB-01]`, `[R-SLB-03]`)"; §20.3 step 4: "an aligned layer's new tiles satisfy
its invariant or the declaration is cleared"). Editorial, one clause.

### Downgraded: implemented-unregistered-flag-authority (adversary-02, writer-05)

Deciding text: [R-CNT-22] — "Stored flag bits are authoritative only for record
types the consuming tool does not implement." adversary-02 concedes this is "the
sharper sentence" and picked against it. The preservation table's own preamble
scopes it: "For a type the updater does not implement, the stored flags are
authoritative ... and carry these obligations:" — the drop permission lives
inside that table, so it is not available for a type the updater does implement.
Outside the table the unconditional default stands: [R-WRT-05], "an updater MUST
re-emit byte-identically — header, inline payload, and extent slot — every record
it retains and does not logically modify, whether or not it implements the
record's type", with no permission to drop granted anywhere else. Retention is
determined. Real gap in §20.4's enumeration; no fork in bytes.

### Downgraded: experimental-metadata-encoding-verdict (verifier-02)

Deciding text: [R-MTA-03] — "An encoding a reader does not implement is therefore
one this specification does not assign, and is ignore-record (`[R-CNT-25]`)."
That fixes the outcome at ignore-record, not cannot-establish. §21.6's row agrees:
"Ignored (ignore-record); the file is conforming."

[R-MTA-09]'s cannot-establish sentence is scoped by its own paragraph to the
resource-bound decline: "the bound is that verifier's capability and not a limit
on validity (`[R-CNF-10]`)" and "the verifier SHOULD report the bound it applied
and the stored length of the extent it declined" — both presuppose a bound the
verifier chose and applied. A verifier meeting encoding 0x80 applies no bound and
declines nothing; it has nothing to decode. The exact parallel is settled for the
codec space in the same terms by [R-COD-11]: "For a conforming reader that
position arises only at a reserved or experimental value ... it rejects the
layer". Verdict: certify. PARTIAL — the residual is that §2.3's illustrative list
names "when it declines to decode a user-metadata document ([R-MTA-09])" without
carrying [R-MTA-09]'s scoping with it.

### Downgraded: t15-no-procedure (register-01)

Two deciding sentences.
- §21.1, on the Instances column: "The **Instances** column enumerates what a
  conformance corpus builds for that row (§21.8): the row is the rule, and each
  instance is one file." — and the same paragraph names T15 by name as an
  example: "one whose members give the condition materially different shapes
  enumerates them (T15, T25)." So T15's "zlib RFC 1950 (CMF/FLG header ...)" cell
  is two corpus files, not a header sniff. Reading (B) has no textual basis.
- [R-CNF-03]: "A reader MUST accept every conforming file of a format major
  version it implements". The `78 9C 00 63 FF <156 bytes> 01 00 00 FF FF` tile is
  conforming under [R-COD-05]; a reader rejecting it is not a conforming reader.

The reporter's arithmetic is right and its own conclusion (reading A) is right.
The defect is real but is bookkeeping: T13 and T26 carry the annotation "the check
that detects it is T25's, and this row records the cause rather than a procedure
of its own"; T15 and T16 do not. Add it.

## Remaining downgrades of non-flagged findings — deciding quotations

- appg-* (five groups): "It adds no requirement to any actor: a writer ignoring
  it is fully conforming." Appendix G is labelled non-normative in its heading.
  Every ordering, hash, and gap fill it leaves open yields a conforming file
  (§5.2: "Slack has no internal structure this specification defines, its content
  is unconstrained"; [R-CNT-14]: "Record semantics MUST NOT depend on record
  order"; §6.2 trailer table: file_id valid values "≠ 0"). The profile's own
  byte-identity claim fails; the conformance predicate does not move.
- mta07-cites-217-wrongly: [R-MTA-05] is unambiguous and independent — "unsorted
  members do not make a document unreadable: the file is nonconforming, a
  verifier MUST report it, and readers process the document unchanged" — carried
  by F27, L48 and Appendix H. §18.4's sentence is a rationale clause for a
  different rule.
- preservation-summary-omits-sub-record: "both registered types carry PE = 1, so
  neither can be dropped, and implementing a record's type confers understanding
  of it, not permission to drop it", with §7.3's Scope cell "file when top-level;
  layer as sub-record". Appendix H disclaims itself: "each entry's authority is
  the requirement or section cited, never this summary."
- index-regen-trigger: "The output's reference arrays MUST equal the live
  generation's bit for bit (`[R-MDL-02]`): compaction changes where bytes live,
  never what a layer denotes."
- field-taxonomy-not-exhaustive: the class's sole operative consequence is
  "a reader MUST NOT alter decoding based on it", which holds vacuously for
  generation, file_id, reserved bytes and names under every candidate class; and
  §6.2's Valid-values column carries the gates (generation "1 ≤ generation ≤
  2⁶³ − 1", file_id "≠ 0") independently of the Class column, with rows F11/F12.
- appender-duty-on-detected-violation: [R-CNF-12] — "a reader MAY reject it upon
  detecting any violation, including violations whose assigned detector is the
  verifier" (MAY, not MUST); [R-WRT-01] — "certifying the whole file is a
  verifier's office (§9.7)"; §2.3 — "conduct rules bind the actor, the predicate
  binds the bytes". When the commit proceeds its bytes are fixed by [R-WRT-05].
  Real residual: "rely" is used in two senses across [R-WRT-01] ("neither modify
  nor rely on") and [R-WRT-03] ("re-emission relies on every directory byte"),
  which is what makes the escape clause read as unavailable.
- region-undefined-partial-slack: [R-CNF-11] — "that per-requirement report
  constrains the report and not the verdict"; §5.2's Note — "A partial total
  (`[R-CNT-21]`) reports what one verifier's incomplete walk left unclaimed,
  which is a fact about that run and not about the file's live state." Every
  partial-total case has an established violation, so [R-CNF-11]'s "An
  established violation takes priority" already fixes the verdict.
- enc06-no-row-no-account: §21.7 — "no file-level witness exists to check, so
  nothing about the file is left undetermined and the verdict is unaffected."
  I independently confirmed undetectability: a trailer emitted with version_major
  as u32 lays down `01 00 00 00` and a spec-width parse reads version_major=1 from
  [8,10) and version_minor=0 from [10,12), with every later field shifted into the
  gates of [R-CNT-06] — a different row, never [R-ENC-06].
- limits-collection-incomplete: [R-GEO-01] — "Writers MUST NOT emit a layer with
  rank 0, any tile extent 0, or channel count 0; a reader MUST treat any of these
  as a validity error at layer scope", carried by L32; [R-CNT-25]'s ≥5 rule
  carried by F22/L11; [R-MTA-03]'s inline_length=1 carried by F23/L12.
  I confirmed [R-ERR-05] does list floors (S ≥ 1, A_slab ≥ 1, dir_length ≥ 4,
  dir_offset ≥ 16, F ≥ 128), so the omissions are not out of scope by kind.
- verdict-vs-outcome-vocabulary: [R-VEC-02] states the manifest schema correctly
  ("the outcome class (§2.4), the scope, and the §21 register row it exercises"),
  and [R-VEC-01] makes the corpus derivative.
- l22-instances-cell: [R-CNT-17] states the equality unambiguously; L22's outcome,
  detector and tier are right.
- row-labels-unstable: [R-VEC-01] — "where a vector's recorded expectation and
  this specification disagree, this specification governs and the vector is
  corrected."
- no-record-byte-example: [R-CNT-18] — "fields are packed in table order with no
  alignment or padding between them" plus §7.2's and §7.4's tables admit one
  parse.
- vec04-verifier-rows: §21.1 — "For a row whose Detector is *verifier*, the
  outcome names the scope at which the damage is recorded, not an obligation on
  any reader". Verified present in §21.1's Instances paragraph; the twelve rows
  quiz-03 names (L18, L40–L42, L46–L49, T2, T4, T5, T26) all carry Detector
  verifier in §21.3/§21.4.
- overlong-pre-trailer-gap: §6.2 — "a longer gap is conforming, and no conforming
  commit produces one." Decided in one sentence; §2.3's second conduct category
  ("A writer obligation whose violation this specification expressly declares not
  to be a file-conformance violation") covers it, its example list merely does not
  name it.
- checklists-cite-prose / preservation-table-unlabelled / section-211-unlabelled:
  all three are traceability defects in text whose content is fully stated.
  §2.4 reaches the preservation table by prose position — "§20.4's table states
  the cases: its MU = 1 and MU = 0 / PE = 1 rows" — so the rule is findable;
  §21.1's tie-break "where a row and the rule it cites diverge, **the rule
  governs**" is fully stated whether or not it is citable.

## Coverage

44 input ids; 28 groups; union of member_ids = the input list exactly, no
duplicates. I counted by hand twice (group sizes 1,2,3,3,2,1,2,1,1,1,2,4,2,1,2,
1,3,1,1,1,2,1,1,1,1,1,1,1 = 44). No finding was left unevaluated.
