# Downstream audit — case adr0109, hunks 01–08

Role: repair auditor, **outside-the-hunk** charter. Question answered here is not
"are the eight corrections right" but "what elsewhere depended on what those
passages used to say, and what else is wrong in the same way".

## 0. Disclosure

Read in full or in part, by absolute path:

- `/Users/robertkleffner/Documents/GitHub/tarn/spec/tarn.md` — the specification.
  Passages opened: §2.1, §2.2, §2.3, §2.4, §2.5, §3.1, §3.2, §3.3, §4.2, §4.3,
  §4.4 (head), §4.6, §4.7, §5.2, §6.1, §6.2, §6.3, §7.1, §7.2, §7.3, §7.4,
  §11.1, §11.2, §11.3, §11.4 (head), §13 intro, §13.1, §13.2, §13.3, §14 intro,
  §14.1, §14.2, §14.3, §14.4, §14.5, §15.1, §15.2, §15.3, §17.1, §17.2, §17.3,
  §17.4, §18.1, §18.2, §18.3 (head), §19 intro, §19.1, §19.2, §19.3, §19.4,
  §20.4, §20.5, §21.1, §21.2, §21.3, §21.4, §21.5, §21.6, §21.7, §21.8, §21.9,
  §24, Appendix G, Appendix H, plus the heading index of the whole file.
- The eight hunk files
  `/private/tmp/claude-501/-Users-robertkleffner-Documents-GitHub-tarn/47df3e0a-29c9-4ed2-8e1d-01658d3e6d8e/scratchpad/case-adr0109/hunk-0{1..8}.diff`.

Nothing else. I did not open `full.diff`, any other hunk file, `docs/`,
`PLAN.md`, `OPEN-QUESTIONS.md`, `AGENTS.md`, `README.md`, `conformance/`,
`spec/registry.json`, git history, or the web. I did not list the case
directory. `wc -l spec/tarn.md` = 4559.

**Context I did not ask for.** Before I began, my runtime placed in context a
project-instruction pointer (`CLAUDE.md` → `AGENTS.md`) and an index of the
maintainer's personal memory files, several of whose titles name this project's
working cadence, its gate board, and prior classes of finding. I did not open
any of them, and I have disregarded their contents; I am naming their appearance
here because disclosure is mandatory. No conclusion below rests on them — each
finding is anchored to a quotation from `spec/tarn.md` that I reproduce.

Computation run: two Python passes over `spec/tarn.md` (below) that parse the
§21.2–§21.5 register tables and count rows and instances. They read no other
file. Greps run are reproduced verbatim below.

## 1. Header check on the hunk files

Each hunk file warns that its "nearest preceding heading" line is derived
mechanically and should be verified. I verified all eight against the current
file:

| hunk | file says | current file at that line | verdict |
|---|---|---|---|
| 01 | 2000, "14.4 Layout–type validity" | line 2000 `#### 14.4 Layout–type validity` | ok |
| 02 | 3228, "20.4 Re-emission and preservation" | line 3228 `#### 20.4 …` | ok |
| 03 | 3415, "21.1 How to read the register" | line 3415 `#### 21.1 …` | ok |
| 04 | 3496, "21.2 File-scope violations" | line 3496 `#### 21.2 …` | ok |
| 05 | 3602, "21.4 Tile-scope violations" | line 3602 `#### 21.4 …` | ok |
| 06 | 3639, "21.5 Ignored records" | line 3639 `#### 21.5 …` | ok |
| 07 | 3673, "21.6 Conditions that are not violations" | line 3673 `#### 21.6 …` | ok |
| 08 | 4344, "Appendix G — Reproducible-writer profile (non-normative)" | line 4344 | ok |

No mismatch.

## 2. The rule each repair adopts, in my own words

1. **Hunk 01 (§14.4 Note).** Rule adopted: for a single-channel bool layer the
   planar and interleaved decoded tile images differ *only* where ⌈P/8⌉ ≠ P;
   at P = 1 they are the same length and are byte-identical iff the channel's
   fill is false. Sits inside a `> **Note.**` — labelled, therefore
   non-normative under `[R-CNF-01]`. It asserts no obligation, so its lack of
   force is not a defect.
2. **Hunk 02 (§20.4 MU = 1 row).** Rule adopted: for a record of a type the
   updater does not implement carrying MU = 1, a *compactor* must refuse
   whether the record is top-level or a layer sub-record.
3. **Hunk 03 (§21.1).** Rule adopted: "narrower row wins" is no longer a closed
   list of three pairs but a **property** — one row specializes another iff
   every file exhibiting the first necessarily exhibits the second — with five
   pairs given as examples and merely-overlapping rows expressly excluded.
4. **Hunk 04 (F21).** Rule adopted: a top-level user-metadata record with
   extent slot (0, 0) is a violation, full stop; the old gloss "placing its
   document inline" is withdrawn.
5. **Hunk 05 (§21.4 preamble).** Rule adopted: the "never returns fill in place
   of data" duty binds a reader only for a rejection that reader is obliged to
   detect; where a row's detector is *verifier*, no reader is obliged and the
   governing rule says what a reader does.
6. **Hunk 06 (R3/R4).** Rule adopted: where the encoding is 2 and what fails is
   a frame constraint R4 registers, R4 is the row **whether or not the bytes
   also fail to decode**; R4's constraints are checkable from the extent's
   bytes without relying on a decoder's tolerance.
7. **Hunk 07 (§21.6 sentinel entry).** Rule adopted: a sentinel tile's sample
   positions **inside the layer's extents** read, **for each channel the tile
   carries**, as that channel's fill.
8. **Hunk 08 (Appendix G item 10).** Rule adopted: a caller-supplied decomposed
   name is a different name because its **bytes** differ, not because its
   length differs; the consequence stated is a different layer record. The
   consequences "a different `inline_length`" and "a different `dir_length`"
   are withdrawn.

## 3. Check 2 — every citation opened

| where | citation | what I checked | verdict |
|---|---|---|---|
| h01 | `[R-SER-05]` | §14.5: "Every pad bit (§14.3) MUST carry the plane's channel's fill bit." | **passes** |
| h01 | (implicit ⌈P/8⌉) | §14.3 `[R-SER-03]`: "the decoded size is ⌈P/8⌉ bytes"; §14.2: interleaved bool "a single byte, 0x00 = false, 0x01 = true", decoded size P·Q with Q = 1 for one bool channel | **passes** |
| h01 | (implicit P ≥ 1) | §11.1 `[R-GEO-01]`: "each of its d dimensions has … a tile extent Tᵢ ≥ 1"; §11.2: "P = ∏ Tᵢ". So P = 1 is reachable and ⌈P/8⌉ = P holds at P = 1 and nowhere else. | **passes** |
| h02 | `[R-CNT-18]` | §7.4: "an unknown sub-record type with MU = 1 is reject-layer, and where the file is otherwise conforming a reader MUST NOT reject the file for it" — supports "blocks modification of that layer, leaving other layers editable" | **passes** |
| h02 | §2.3 | "Verifiers and updaters are readers of the files they process and inherit every reader obligation" | **passes** |
| h02 | `[R-CNT-15]` | §7.2: "An unknown record type at file scope: MU = 1 → reject-file" | **passes** |
| h02 | §6.3 | `[R-CNT-08]`: "an updater encountering an unknown incompat-lane bit is a reader first, and therefore rejects the file before modifying anything" | **passes** |
| h02 | `[R-WRT-06]` | §20.5: "A compactor MUST refuse to compact a file carrying **any record** whose type it does not implement with MU = 1: such a type can define references this specification does not (§7.2), so its bytes cannot be safely relocated." Quantifier "any record" does reach sub-records (§7.4: "Sub-records are layer-scope records"), so the repair's "either scope" is inside the rule's range. | **passes on quantifier; see finding B-01 on the verb** |
| h02 | §7.2 | "Records with MU = 1 carry further references only where this specification or registry review (§10) defines them" — the repair copies `[R-WRT-06]`'s own gloss of this verbatim | **passes (faithful copy)** |
| h03 | F1 / F6 / F8 | F1 "A signature constant is stored byte-reversed … front signature block bytes [0,8); trailer magic at F-64"; F6 "The 16-byte front signature block is not byte-identical to the constant"; F8 "The 8 bytes at F-64 are not exactly the trailer magic". Byte-reversed ⇒ not byte-identical, both instances. | **passes** |
| h03 | F35 / F36 | F35 reserved-range type **with MU = 1**; F36 reserved-range type "whatever its MU bit". F35 ⊂ F36, F36 reachable at MU = 0. | **passes** |
| h03 | L24 / L25 | same shape at sub-record scope | **passes** |
| h03 | **F21 / F22 (new)** | F21 slot (0, 0) ⇒ extent_length = 0 < 5 ⇒ F22. F22 reachable at extent_length 1–4 with a legal offset. Strict specialization; both rows reader/open. | **passes** |
| h03 | **L10 / L11 (new)** | identical argument; both rows reader/layer access | **passes** |
| h03 | §21.6, §21.7, §21.9 | named as "not part of the register" — confirmed: §21.6 is a table of non-violations, §21.7 `[R-ERR-01]`, §21.9 `[R-ERR-03]`–`[R-ERR-05]`; none carries numbered rows | **passes** |
| h04 | `[R-CNT-25]` | §7.1: "Each user-metadata record carries its document in its extent — **never inline** … An extent of (0, 0) on a user-metadata record … is a validity error at its containing scope." The deleted gloss "placing its document inline" contradicted the governing rule outright. Deleting it is correct. | **passes** |
| h05 | `[R-CNF-09]` | §2.4: "A reader MUST NOT return data as valid from a scope this specification rejects **and whose rejection this reader is obliged to detect** (`[R-RDR-02]`); in particular, a read of a rejected tile MUST NOT silently return fill." The repair restores exactly this qualifier. | **passes** |
| h05 | "Detector is *verifier*" clause | §21.1: "For a row whose Detector is *verifier*, the outcome names the scope at which the damage is recorded, not an obligation on any reader: the governing rule states what a reader does". §21.4's four verifier rows are T2 (`[R-SER-08]`, which does state what a reader returns), T4/T5 (`[R-SER-05]`: "A conforming reader never returns this content … and is not obligated to check it"), T26 (`[R-COD-10]`, which defines the inverse a reader applies). | **passes** |
| h06 | `[R-MTA-10]` | §18.2: under an unassigned encoding "no content rule attaches to the extent's bytes" — supports R3's experimental-range carve-out | **passes** |
| h06 | `[R-COD-06]`, §18.2 | §18.2 `[R-MTA-09]`: "A mismatch is one of the frame constraints R4 registers, not a failure to decode under R3 … Routing it to R4 keeps the condition checkable from the bytes alone rather than turning on a decoder's tolerance". R4's new wording is a faithful restatement. | **passes** |
| h06 | R4 instance list vs §18.2 | §18.2 carries over "the frame magic; no skippable frame and no second frame; no dictionary use, disclosed or not, and no nonzero dictionary ID; no content-checksum flag; and the bar on sizing any buffer" and adds "the single frame occupying the extent's bytes before its terminal CRC" and the content-size pin. §18.2: "Two of those carry no witness a file exhibits, and R4 registers neither". R4's eight distinguishable conditions × two containers = 16 instances. | **passes** |
| h07 | `[R-TYP-08]` | §13.3: "a reader that returns any of the tile's sample positions **inside the layer's extents** MUST return, **for each channel the tile carries**, that channel's fill value at every such position." Word-for-word the two qualifiers the repair adds. | **passes** |
| h07 | `[R-IDX-02]` | §15.2: "A sentinel tile contributes fill to the reference array (§3.2, §13)"; and `[R-MDL-01]` confines the reference array to the extents. | **passes** |
| h08 | `[R-ENC-14]` | §4.6: "Writers SHOULD emit names in Unicode Normalization Form C" | **passes** |
| h08 | `[R-ENC-13]` | §4.6: "Name comparison is raw bytes: two names are the same name if and only if their encoded byte sequences are identical." Supports "because its bytes differ — whether or not its length differs with them". | **passes** |
| h08 | §4.6 `température` | §4.6 Example: 12 bytes NFC, 13 bytes NFD | **passes** |

No citation failed.

## 4. Check 3 — does each repair sit in normative text?

Blockquote inventory. I enumerated every blockquote's first line and filtered
out the labelled ones:

```
$ awk 'BEGIN{inq=0} /^>/{ if(inq==0){start=NR; first=$0; inq=1} next } { if(inq==1){ printf "%d: %s\n", start, first; inq=0 } }' spec/tarn.md | grep -v -i '\*\*Note\|\*\*Example\|\*\*Rationale'
12: > **How to read this document** *(non-normative).* Sections follow a fixed
2073: > [ entry array: entry_count × 20 bytes ] [ segment CRC array:
```

So the one unlabelled — therefore **normative** — blockquote in the document is
§15.1's tile-index region layout at line 2073. None of the eight hunks touches
it, and none of them depends on it.

- Hunk 01 lands in a `> **Note.**` — labelled, no force. It states no rule; it
  is an observation about byte-identity. The normative statements it glosses
  (`[R-SER-03]`'s ⌈P/8⌉, `[R-SER-02]`'s P·Q, `[R-SER-05]`'s pad bits,
  `[R-SER-09]`'s "A reader MUST NOT reject a layer for its combination of
  layout and channel types") are all in plain prose in §14.2/§14.3/§14.4/§14.5
  and none of them says the old thing. No failure-to-land.
- Hunks 02–07 all land in normative prose or normative table cells (§20.4's
  table, §21.1–§21.6). §21.6's table entries are normative by §21.1's own
  statement: "§21.6's entries restate their governing rules on the same terms a
  row does, and where such an entry and the rule it cites diverge, the rule
  governs there too."
- Hunk 08 lands in Appendix G, whose heading reads "(non-normative)". It adopts
  a SHOULD as a profile rule and claims no force; correct as written.

## 5. Check 5 — completeness words, and their falsification attempts

- h01 "**wherever** ⌈P/8⌉ ≠ P", "**exactly when** that fill is false". Tried to
  falsify. ⌈P/8⌉ = P only at P = 1 given Tᵢ ≥ 1 (`[R-GEO-01]`). At P = 1,
  planar image = one byte, bit 0 the value, bits 1–7 the pad bits fixed to the
  fill bit (`[R-SER-05]`, §14.3 "bit positions P mod 8 through 7, when
  P mod 8 ≠ 0"; 1 mod 8 = 1 ≠ 0, so pad bits exist). Interleaved image = one
  byte, 0x00 or 0x01 (§14.2). fill = false → planar 0x00/0x01, coincide.
  fill = true → planar 0xFE/0xFF, differ. The biconditional holds. Not falsified.
- h02 "**At either scope**". Records exist at exactly two scopes — top-level in
  the directory's sequence, and layer sub-records (§7.2/§7.4). There is no
  third. Not falsified.
- h03 "**every** file exhibiting one row's condition necessarily exhibits
  another's"; "the property decides **any** pair"; "this list is **not offered
  as closed**". The escape hatch defuses the closed-list risk. The logic of the
  negation is right: ¬(A⊆B ∨ B⊆A) ≡ each reachable without the other, which is
  what the next sentence says. The residue is that for a merely-overlapping
  pair the property decides the *relation* but not which row records a file
  exhibiting both — F2/F3 is such a pair (see §8 below). I read "decides any
  pair" as scoped to the relation, which the following sentence makes explicit,
  so I do not report the phrase itself.
- h04 no completeness word.
- h05 "**never** returns fill in place of data" — now qualified; "**no** reader
  is obliged to detect" for verifier rows — matches §21.1 verbatim in substance.
  "26 conditions" — counted mechanically, 26 T rows. Not falsified.
- h06 "**one of** the frame constraints R4 registers", "**several**, the
  content-size field among them". Tried to falsify "several": conditions broken
  while the bytes decode are the content-checksum flag, a second frame, a
  skippable frame after the first, bytes remaining after the frame, and the
  content-size mismatch — at least five. "Several" holds.
- h07 "**every** sample position it carries inside the layer's extents",
  "**for each** channel the tile carries" — both copied from `[R-TYP-08]`.
- h08 "**whether or not** its length differs with them"; "**the same length in
  both forms**". Canonical reordering permutes combining marks without adding
  or removing bytes, so length is preserved; and canonical ordering is part of
  NFC, so a reordered name is genuinely non-NFC. Not falsified.

Register counts, checked mechanically:

```
$ python3  # parse the four register tables
rows 121 instances 277
Counter({'L': 49, 'F': 36, 'T': 26, 'R': 10})
Counter({'L': 116, 'F': 58, 'T': 55, 'R': 48})
```

§21.2 "36 conditions", §21.3 "49 conditions", §21.4 "26 conditions", §21.5
"10 conditions", §21.8 "121 conditions over 277 instances" — all agree. No hunk
changed an Instances cell (h04 changed only F21's Condition text; h06 changed
only R3's and R4's Condition text), so no count is disturbed.

## 6. Check 7 — arguments by analogy, verb against verb

- **h02** — "on `[R-WRT-06]`'s own ground".
  - repair's verb: "a compactor **MUST refuse the file**"
  - cited rule's verb: "A compactor **MUST refuse to compact** a file carrying
    any record whose type it does not implement with MU = 1"
  - Sets: "either scope" vs "any record" — the cited rule's range is wider, so
    the analogy does not stretch the quantifier. But the *verbs are not the
    same verb*: "refuse to compact" names declining an operation; "refuse the
    file" is, in this document's vocabulary, the reader outcome reject-file
    (§2.4, §21.6 "a file a reader refuses"). This is the one place where the
    side-by-side comparison fails, and it is finding **B-01**.
- **h05** — "for a rejection the reader is obliged to detect (`[R-CNF-09]`)".
  - repair's verb: "never **returns** fill in place of data, for a rejection
    the reader is **obliged to detect**"
  - cited rule's verb: "A reader **MUST NOT return** data as valid from a scope
    this specification rejects and **whose rejection this reader is obliged to
    detect**"
  - Same set, same modality. **Passes.**
- **h06** — "unlike R3". Contrast, not analogy; and §18.2's own analogy ("the
  tile rule of `[R-COD-06]` transposed to the quantity a document does have,
  its decoded length, in place of the declared size it does not") is unchanged
  text that the repair does not re-use. R4's verb "breaks one of the frame
  constraints §18.2 states or carries over" against §18.2's "under every frame
  constraint `[R-COD-06]` places on a frame, named here or not, save two" —
  same set, with §18.2's two exceptions (declared decoded size; declared
  Window_Size) both replaced in §18.2 and neither registered by R4. **Passes.**
- **h07** — no analogy; a direct restatement of `[R-TYP-08]`, verb "reads …
  as that channel's fill" against "MUST return … that channel's fill value".
  Same set (positions inside the extents; channels the tile carries).
  **Passes.**
- **h08** — "as items 1 and 9 pin their producers" is elsewhere in Appendix G,
  not in this hunk. Item 10 argues from `[R-ENC-13]` directly: repair's verb
  "is a different name … because its bytes differ" against `[R-ENC-13]`'s "two
  names are the same name if and only if their encoded byte sequences are
  identical". Same predicate, contrapositive. **Passes**, and it is the
  correction: the old text reasoned from *length*, which `[R-ENC-13]` never
  mentions.
- **h01, h03, h04** — no analogy sentences.

## 7. Check 6 — what each repair leaves unconstrained

- **h01.** Structure: the decoded tile image of a single-channel bool layer.
  Quantities: P, layout, the channel's fill bit, the filter, the codec. Layout
  is pinned by `[R-SER-06]`; fill by `[R-TYP-07]`/`[R-TYP-06]`; pad bits by
  `[R-SER-05]`; the filter is the identity in both forms here (§17.3: planar
  packed bool s = 1; interleaved single bool channel Q = 1 so s = 1). Nothing
  the note governs is left unpinned.
- **h02.** Structure: a record header's flag pair (MU, PE) plus the record's
  scope. The §20.4 table gives all three stored-flag combinations; the
  repair touches only MU = 1. PE for an MU = 1 record is forced to 1 by
  `[R-CNT-12]` ("MU = 1 with PE = 0 is read as PE = 1"), so the row is complete.
  Compaction is now stated for MU = 1 (refuse) and for MU = 0 / PE = 0 ("A
  compactor MAY drop it whenever it rewrites the file"); the MU = 0 / PE = 1
  row says nothing about compaction, but §20.5 and `[R-WRT-07]` cover it
  ("every retained record per §20.4, except that relocation re-points extent
  slots"). No gap.
- **h03.** Structure: the register's row set. What the property leaves open is
  the *merely-overlapping* case — see §8, F2/F3.
- **h04.** Structure: a top-level user-metadata record. Its quantities: type
  (F24, F34), flags (F25, F26, F28), inline_length (F23), the encoding byte
  (R1 for 0 and reserved; §21.6 for experimental), extent_offset (F31),
  extent_length (F22), the slot as a pair (F21, F30, F32), the extent's
  terminal CRC (R2), and the document (R3–R10). Every quantity is bound by
  some row. No sibling left unpinned.
- **h05.** Structure: §21.4's table. Preamble now covers reader rows and
  verifier rows separately. Complete.
- **h06.** Structure: the RFC 8878 frame header of a user-metadata document
  under encoding 2. Members: magic (R4), Frame_Content_Size_flag /
  Frame_Content_Size (R4, and §18.2 pins it to the decoded length),
  Single_Segment_flag (§18.2 addresses it expressly, "Where the frame sets
  Single_Segment_Flag there is no Window_Descriptor and RFC 8878 makes the
  frame's `Window_Size` its content-size field, which this section pins below
  to the decoded document's byte length"), Content_Checksum_flag (R4),
  Dictionary_ID_flag / Dictionary_ID (R4), Window_Descriptor (deliberately left
  to the reader's own bound, §18.2, §21.9), reserved bit (falls to R3 via
  "fails to decode"), block sequence (R3), bytes after the frame (R4). This is
  the exact shape the charter warns about — a compressed-frame header with one
  quantity pinned and a neighbour unpinned — and I find both the content-size
  and the window addressed, the window deliberately and with a stated reason.
  No sibling left silently unpinned.
- **h07.** Structure: a tile-index entry. Fields: offset, length, crc. The
  sentinel is (S, S, 0); T6 catches (S, S, crc≠0), T7 catches exactly one half
  sentinel. All three fields bound. The behaviour statement now names both the
  positional range and the channel range. Complete.
- **h08.** Structure: the set of "names" (§4.6: layers, dimensions, channels,
  and user-metadata keys). Item 10's stated consequence is "a different layer
  record", which covers layer, dimension and channel names but not a
  user-metadata **key** — a decomposed key yields a different document, not a
  different layer record. The old text was equally layer-record-only ("a
  different layer record, a different `inline_length`, and a different
  `dir_length`"), so the repair neither introduced nor widened this; and item
  10's headline ("Names normalized to Unicode Normalization Form C") plus
  Appendix G's closing summary ("NFC-normalized names, which `[R-ENC-14]`
  states as a SHOULD") do reach keys. Noted, not reported.

## 8. The charter's five named sweeps

### 8a. "Five repairs fix a restatement that dropped a qualifier" — sweep each governing rule

**`[R-CNF-09]` (hunk 05).** Grep:

```
$ grep -n 'R-CNF-09' spec/tarn.md
311:silently return fill. `[R-CNF-09]`
1841:rejection is never satisfied by returning fill (`[R-CNF-09]`).
2927:   fallback (`[R-CNF-09]`).
2947:   in for a rejected tile's positions (`[R-CNF-09]`). That
3606:to detect (`[R-CNF-09]`); where a row's Detector is *verifier* no
```

- line 311 — the rule itself, §2.4, carries the qualifier.
- line 1841 — §13.3 `[R-TYP-09]`: "A reader MUST NOT return fill for a tile
  whose entry is malformed (§15.3), whose index CRC array or segment failed
  verification, or whose stored bytes failed their checksum". Every condition
  it enumerates is reader-detected (T1, T6–T12 all Detector *reader*; L37, L38
  reader). No qualifier needed. **Still correct.**
- line 2927 — §19.4 step 4: "A malformed entry rejects the tile; a rejected
  tile's read reports failure, and fill is never a failure fallback." Same:
  malformed entries are §15.3's reader rows. **Still correct.**
- line 2947 — §19.4 step 8: "MUST NOT stand fill in for a rejected tile's
  positions". Same, about entries the reader itself rejected. **Still correct.**

The unswept restatement is not of `[R-CNF-09]` but of the *outcome gloss* the
repair rewrote. §21.4's preamble and §21.3's preamble are siblings written to
one pattern; only §21.4's now carries the verifier qualifier. §21.3:

> Outcome: reject-layer — the named layer is unusable, every other
> layer unaffected. 49 conditions.

§21.3 has nine verifier rows: L18, L25, L40, L41, L42, L46, L47, L48, L49. For
two of them the governing rule says in terms that the layer stays usable —
L48 "the document stays readable and readers process it unchanged"
(`[R-MTA-05]`: "readers process the document unchanged") and L49 "readers apply
the type's fixed semantics regardless" (`[R-CNT-22]`: "A reader MUST apply a
known type's specified semantics regardless of its stored MU and PE bits"). And
§21.1 names L48 explicitly as such a row. This is finding **B-02**.

The same gloss appears a second time, in §24's Note (line ~4154): "a vector
exercising a reject-layer row expects that layer to be unusable" — two
paragraphs after `[R-VEC-04]` says the opposite for verifier rows: "Where it is
the verifier, no reader is obliged to refuse anything (§21.1), so the pair is
the scope at which a verifier confines its finding … and the content a reader
owes from every scope, **the damaged one included**." Finding **B-03**.

I checked §21.2's and §21.5's preambles for the same shape. §21.2 states only
"Outcome: reject-file. 36 conditions." — no behavioural gloss. §21.5's preamble
does gloss ("the record is skipped as though absent and decoding of stored data
is unaffected"), but every §21.5 row R1–R10 has Detector *reader*, so no
qualifier is owed there. §2.4's own outcome table glosses unqualifiedly too
("**reject-tile** | … a read of that tile reports failure"), but `[R-CNF-09]`
sits three paragraphs below it carrying the qualifier, and §2.4 also states "a
reader MAY reject it upon detecting any violation, including violations whose
assigned detector is the verifier". §21.3 is the outlier.

**`[R-TYP-08]` / `[R-IDX-02]` (hunk 07).** Restatements found by grepping
`fill` across the whole file (74 hits, reviewed individually). The behavioural
ones:

- §3.1 term: "An addressed tile that is not stored reads as fill (§13)." —
  terminology pointer, no obligation. Still correct.
- §3.2 `[R-MDL-01]`: "If the tile carrying that channel at that coordinate is
  stored, the channel's value is the one decoded from that tile …; otherwise it
  is that channel's fill value" and "Sample positions that exist only as
  edge-tile padding (§11.3) have coordinates outside the layer's extents and
  are not part of the reference array." — carries both qualifiers already.
  Still correct.
- §13 intro: "each channel it carries reads as fill at every sample position
  (§13.3)" — carries the channel qualifier, omits "inside the extents". I
  considered reporting this and decided against it: an unstored tile's padding
  positions are outside the extents, are never returned (`[R-GEO-04]`), and
  §14.5 fixes padding content to the same fill anyway, so the wider reading
  states nothing false and licenses nothing. Not a defect.
- §15.2 `[R-IDX-02]`: "A sentinel tile contributes fill to the reference array"
  — the reference array is extent-bounded by `[R-MDL-01]`, so the qualifier is
  carried by reference. Still correct.
- §15.3 table row: "valid sentinel — reads as fill" — a classification cell,
  not a behaviour statement. Still correct.
- §19.4 step 4: "every requested sample position of its tile reads as fill —
  the entry's channel's recorded fill in a planar layer; each carried
  channel's, in declared order, in an interleaved layer". Step 1 has already
  confined the request to the intersection with the extents, and step 7 bars
  returning padding positions. Carries both qualifiers. Still correct.
- Appendix H reader checklist: "never returns padding positions (§11.3) and
  never returns fill for a rejected tile (§2.4)" — non-normative, and correct.

No unswept restatement of `[R-TYP-08]`.

**`[R-CNT-25]` (hunk 04).** Grep for the slot form:

```
$ grep -n '(0, 0)\|(0,0)\|no extent' spec/tarn.md
945: … An extent of (0, 0)
992: The **extent slot** (extent_offset, extent_length): (0, 0) means no
1069: (§15); a layer with zero addressed tiles has extent (0, 0). Its inline
2177: … extent slot (0, 0) and
2510: malformed extent slot on such a record, (0, 0) included, is a
2801: (0, 0) slot, extent_length at least 5, inline_length exactly
2879: sub-record carries — no (0, 0) slot, extent_length at least 5,
3528: | F21 …
3561: | L10 …
3573: | L22 …
```

Every one of these is consistent with the repaired F21 and with §7.1's "never
inline": §7.2 "(0, 0) means no extent"; §18.1 "a malformed extent slot on such
a record, (0, 0) included, is a validity error at the record's containing
scope"; §19.1 step 4 and §19.3 "no (0, 0) slot, extent_length at least 5,
inline_length exactly 1"; §18.2 "A user-metadata record's inline payload is
exactly one byte". The false gloss existed only in F21. **Nothing depended on
it, and the deletion sweeps cleanly.**

**`[R-MTA-09]` (hunk 06)** — see 8c.

**`[R-SER-03]`/`[R-SER-05]` (hunk 01).** The only other passage that compares
the two layouts' bool images is §21.6's row "A layer mixes bool and numeric
channels, in either layout | Defined: planar bool planes pack, interleaved bool
values are single bytes; a reader MUST NOT reject the layer for the
combination" — which makes no byte-identity claim. Appendix G item 5 ("The
filter is the identity exactly where its permutation is — where the stride is
1, as for a packed boolean plane, and equally where the decoded image is a
single group, n = L/s being 1") is consistent with, and independently confirms,
the P = 1 case. No unswept restatement.

### 8b. "A closed list became a property" — sweep for pairs, and for a file recorded against the wider row

I enumerated the places the document names a register row outside a table:

```
$ grep -n -o -E '\b(F|L|T|R)[0-9]{1,2}\b' spec/tarn.md  # filtered to non-table lines
273 F14 | 276 F5 | 280 F15 | 709 L18 L40 L42 | 1366 F14 F17 F8 | 2345 T24
2553 R4 | 2565 R3 | 2583 R3 R4 | 2585 R4 | 3107 L44 | 3320 F36 L25
3322 L31 L33 L34 L36 L43 L45 R1 | 3441 F1 F35 F6 F8 | 3442 F21 F22 F36 L10 L11 L24 L25
3461 T24 | 3463 T15 T25 | 3491 F27 L48 | 3500 F14 F6 F8 | 3501 F1 | 3502 F18
3652 R1 | 3723 F18 | 3724 F35 F36 | 3725 L24 L25 | 3753 T2 T4 T5 | 3763 T3
3764 T14 | 3765 T14 T3 | 3768 T14 T15 T17 T23 T25 | 3773 T26 | 3776 T2 T26 T4
4543 F1 F6 | 4545 F7 | 4546 F36 L25 | 4555 R1
```

Each checked against the property:

- **§21.2 preamble (3500–3502)** — "Deriving it there yields F8, F14, F6 and
  both of F1's instances … and no other row." A list of rows that *reach* a
  foreign-major file, not a recording. A byte-reversed signature in such a file
  is recorded against F1, the narrower row, which is in the list. Correct.
- **§21.6 table (3723–3725 area)** — "a *reserved*-range type is read the same
  way, but emitting one is a violation (F36, L25)". The entry's condition is
  "carries MU = 0", at which F35/L24 do not apply, so F36/L25 are the right
  (and only) rows. **Correct, not a wider-row recording.**
- **§21.6 closing (3724–3725)** — "(F35, F36, L24, L25)" enumerates all four
  registered rows for reserved-range types; not a recording of one file.
- **§20.5 (3320–3322)** — "F36 and L25 for a record type, and one row for each
  of the other seven spaces §10.2 tabulates (L31, L33, L34, L36, L43, L45,
  R1)". Context is a compactor's *output*. `[R-WRT-06]` bars the compactor from
  producing output at all if the input carries an unimplemented MU = 1 record,
  so the reserved-range record that can reach the output carries MU = 0, at
  which F35/L24 do not apply. **Correct, and precise.**
- **§21.7 (3763–3768)** — "A change reaching the decoded size is witnessed by
  T3 or T14 … T14 the entry's declared length, T3 the decoded payload's own."
  T14 ⊂ T3 (under codec 1 the stored bytes are the filtered image verbatim, so
  entry length ≠ decoded size ⇒ decoded length ≠ decoded size). Naming both is
  right — under a compressing codec only T3 fires. Not a wider-row recording.
- **Appendix H (4546)** — "a reserved-range record or sub-record type value,
  whatever its MU bit (`[R-CNT-15]`, F36, L25)" in the *verifier* checklist.
  F36/L25 are the verifier rows and `[R-CNT-15]`'s verifier duty is
  MU-independent; non-normative in any case.
- **§5.2 (709)** and **§9.6 (1366)** and **§20.3 (3107)** — L18/L40/L42 named
  as walk-stopping verifier findings; F8/F14/F17 named as recovery-scan checks;
  L44 named for the codec-4 cap. None is a specialization-pair recording.

I then swept the register for further pairs standing in the relation and asked
whether anything turns on them: T14 ⊂ T3, T17 ⊂ T25, T11 ⊂ T9, T13 ⊂ T25.
In every one of these the two rows share Detector and Detected, so the
property's "whose detector and detection point are the ones that apply" changes
nothing. The register also carves several near-pairs apart deliberately, which
I checked and found sound: T11 excludes the sentinel value ("the value being
distinct from the all-ones sentinel"), T12 and L2 exclude the in-domain-field
case, T4/T5 are separated by §14.3's Note ("Pad bits are not padding
positions"), and T2 routes the padding-position case to T4 in terms ("the same
byte at a padding position is T4's, the two rows together covering
`[R-SER-08]`").

**Nowhere does the document record a file against the wider row.** What the
sweep did turn up is one *merely-overlapping* pair whose two siblings elsewhere
in the register are carved into disjointness and which F3 is not: finding
**B-04**.

### 8c. "Two register cells had their boundary restated" — sweep everything that routes to R3 or R4

Passages that route a condition to R3 or R4, or reason about which applies:

- **§18.2 `[R-MTA-09]`, content-size:** "A mismatch is one of the frame
  constraints R4 registers, not a failure to decode under R3: the bytes decode,
  and what is wrong is what the header said about them." — **still correct**,
  and now consistent in both directions: R3's new clause says R4 wins "whether
  or not the bytes also fail to decode", which is the strictly wider statement
  and does not contradict §18.2's narrower one.
- **§18.2 `[R-MTA-09]`, window:** "a frame declaring more than the reader
  admits is ignore-record on that ground — the reader's capability, not a
  failure to decode within the meaning of R3, and no violation". The window is
  not one of the constraints R4 registers, so R3's new clause does not capture
  it. **Still correct.**
- **§18.2 `[R-MTA-09]`, witnessless constraints:** "Two of those carry no
  witness a file exhibits, and R4 registers neither". Unaffected. **Still
  correct.**
- **§21.5 preamble:** "except where a reader or verifier declines the decode on
  the size bound or on the frame's declared window, which `[R-MTA-09]` makes
  that actor's capability and not a fact about the file". Unaffected. **Still
  correct.**
- **§21.5 preamble, encodings:** "Encoding 0 and a reserved-range value are
  unassigned too, and R1 registers both as violations" — matches R3's retained
  clause. **Still correct.**
- **§2.3 `[R-CNF-11]`:** "when it declines to decode a user-metadata document
  (`[R-MTA-09]`)" — a cannot-establish ground, untouched. **Still correct.**
- **§21.7:** "an undisclosed compression dictionary (`[R-COD-06]`, and
  `[R-MTA-09]` for a user-metadata document …)" — the witnessless case §18.2
  says R4 does not register. **Still correct.**
- **§17.4 `[R-COD-11]`:** "The metadata-encoding space alone differs: an
  unassigned document encoding in a conforming file is not a violation (§21.6)"
  — matches R3's experimental-range carve-out. **Still correct.**

Nothing routes wrongly after the repair. The one thing the repair does not
reach is the tile-side analogue: T22 (zstd Frame_Content_Size present and
unequal to the decoded size) against T25 (malformed stream that fails to
decode) has no tie-break sentence, where R4/R3 now does. Both are reject-tile,
reader, tile use, so nothing operational turns on it, and §21.4 already uses a
different, express convention for its cause-versus-procedure rows (T13, T15,
T16, T23, T26 each say "the check that detects it is T24's or T25's, and this
row records the cause rather than a procedure of its own"). I judged this below
the reporting bar and record it here only so the next reader knows it was
looked at.

### 8d. "An appendix item dropped two consequences" — find anything that relied on either

The dropped consequences: a non-normalizing writer emits "a different
`inline_length`" and "a different `dir_length`". Sweep:

```
$ grep -n -i 'normaliz\|NFC\|NFD\|R-ENC-13\|R-ENC-14' spec/tarn.md
559,560,561,563  §4.6 [R-ENC-13], [R-ENC-14]
576-579          §4.6 Example (température, 12 vs 13 bytes)
2646-2647        §18.3-ish: "two keys differing only in Unicode normalization are distinct keys"
2814             §19.1 step 4: "[R-ENC-13] makes name comparison a byte comparison"
3275-3276        §20.4 Rationale: "a re-serializer that renormalized a name would change the name's identity ([R-ENC-13])"
3511             F4: "comparison is raw bytes, no normalization"
4339             Appendix F: Unicode reference
4463-4468        Appendix G item 10 (the repair)
4482-4483        Appendix G closing summary
```

Every one of these reasons from *bytes* or *identity*, never from *length*:

- §4.6 `[R-ENC-13]` — "two names are the same name if and only if their encoded
  byte sequences are identical". Byte-based. **Still correct.**
- §4.6's Example — asserts 12 vs 13 for `température` specifically, which is
  true; it does not generalise. **Still correct.**
- §18.2's key rule — "Key comparison is raw bytes (`[R-ENC-13]`), so two keys
  differing only in Unicode normalization are distinct keys." Byte-based, and
  it says *normalization*, not *length*. **Still correct** — and, notably,
  correct precisely because it does not use the premise the appendix withdrew.
- §19.1 step 4 — "`[R-ENC-13]` makes name comparison a byte comparison, which
  needs no valid name". Byte-based. **Still correct.**
- §20.4's Rationale — "a re-serializer that renormalized a name would change
  the name's identity (`[R-ENC-13]`)". Identity, not length. **Still correct.**
- F4 — "both obtainable within their records' `inline_length` (comparison is
  raw bytes, no normalization)". `inline_length` appears here only as the bound
  within which a name field must lie, not as a consequence of normalization
  form. **Still correct.**
- Appendix G item 3 — the emission order keys on "ascending layer-name byte
  order" and on "the record's header with extent_offset masked to zero, then
  its inline payload". These would change under a decomposed name, which is a
  *further* consequence the item does not claim; nothing there relies on the
  two that were dropped.
- Appendix G closing summary — "NFC-normalized names, which `[R-ENC-14]` states
  as a SHOULD". No length claim. **Still correct.**

**Nothing anywhere relied on either dropped consequence.** The repair sweeps
cleanly, and it removes a premise that was false in general (canonical
reordering changes bytes without changing length).

### 8e. "One repair asserts an obligation reaches either scope" — check every other statement of that obligation

The obligation: a compactor must refuse a file carrying a record of a type it
does not implement with MU = 1.

```
$ grep -n 'MU = 1\|MUST_UNDERSTAND\|does not implement' spec/tarn.md   # 30 hits, reviewed
```

- **§20.5 `[R-WRT-06]` (3329):** "A compactor MUST refuse to compact a file
  carrying **any record** whose type it does not implement with MU = 1". Scope-
  neutral; reaches both scopes. **Consistent with the repair's "either scope".**
- **§20.5 (3358–3359):** "an MU = 1 type the compactor does not implement never
  reaches this step (`[R-WRT-06]`)". Scope-neutral. **Consistent.**
- **§2.3 `[R-CNF-03]` (177–180):** the reader's acceptance duty is lifted for a
  file "carrying no record of a type it does not implement with
  MUST_UNDERSTAND = 1" — scope-neutral, about readers not compactors.
- **§7.2 `[R-CNT-15]` (1030):** "An unknown record type at file scope: MU = 1 →
  reject-file" — file scope only, and correctly so; it is a *reader* rule.
- **§7.4 `[R-CNT-18]` (1120):** "an unknown sub-record type with MU = 1 is
  reject-layer, and where the file is otherwise conforming a reader MUST NOT
  reject the file for it" — layer scope, and it forbids exactly the words the
  repair now uses. **This is the collision, finding B-01.**
- **§21.6 closing (3708–3717):** "The qualifier is load-bearing — the same type
  as a layer sub-record is reject-layer and **never a ground to refuse the
  file** (`[R-CNT-18]`), so only the top-level case is a file a reader
  refuses". **The collision again, in the document's own emphatic voice.**
- **§21.9 `[R-ERR-04]` (3846):** "the two capability refusals §21.6 names, a
  foreign format major and an unimplemented MU = 1 type, are not this ground" —
  points back at §21.6, i.e. at the top-level-only refusal. Consistent with
  §21.6, and now in tension with the repair on the same terms as B-01.
- **Appendix H updater checklist (4530–4532):** "never modifies a scope governed
  by an unknown critical record, and rejects outright a file carrying an
  unimplemented **top-level** MU = 1 record (`[R-CNT-15]`, §20.4)". This states
  the *reader* rejection, which is genuinely top-level-only, so it is correct as
  written; it simply says nothing about the compactor's refusal. Non-normative,
  and its cited authority is `[R-CNT-15]`. Not reported.

## 9. Check 4 — contradiction inside each repaired passage, including untouched text

- **h01, §14.4 whole subsection.** The normative paragraph ("Every combination
  of layout and channel types is defined … A reader MUST NOT reject a layer for
  its combination of layout and channel types. `[R-SER-09]`"), the withdrawn-
  identifier Note, the repaired Note, and the Rationale. The Rationale says "A
  bool channel is deliberately expressible in both layouts" — the repaired Note
  now says at P = 1 with fill false the two are byte-identical, which the
  Rationale neither needs nor denies. No contradiction. No carve-out collides.
- **h02, §20.4 whole subsection.** Preamble scopes the table to "a type the
  updater does not implement" — the compactor sentence is inside that branch, so
  it does not reach an MU = 1 type the compactor *does* implement, which §20.5
  handles separately ("An MU = 1 type it *does* implement is the remaining case,
  and §7.2 admits it"). The MU = 0 / PE = 0 row's "A compactor MAY drop it
  whenever it rewrites the file" concerns a different record. The paragraph
  below ("No commit therefore removes a layer record … That is not compaction,
  which carries every layer of its input forward") is untouched and unaffected.
  Inside the passage: no contradiction. **Outside it: B-01.**
- **h03, §21.1 whole subsection.** The completeness clause, the "rule governs"
  clause, the finest-structure clause, the instance arithmetic, and the
  verifier-detector paragraph all read the same under the property as under the
  closed list. The property's new escape ("this list is not offered as closed")
  strengthens the completeness clause rather than colliding with it. No
  contradiction.
- **h04, §21.2 whole table and preamble.** F21's neighbours F22, F23, F30, F31,
  F32, F34 are all consistent with the shortened F21; §7.1's "never inline"
  is now the only statement on the point and F21 no longer contradicts it. No
  contradiction; the repair *removes* one.
- **h05, §21.4 whole subsection.** The four verifier rows T2, T4, T5, T26 are
  exactly the rows the new clause is for. T2's own text ("the same byte at a
  padding position is T4's, the two rows together covering `[R-SER-08]`") and
  T26's ("the check that detects it is T2's or T4's") are untouched and remain
  true. No contradiction.
- **h06, §21.5 whole subsection.** The preamble's carve-outs — the
  experimental-range encoding, and the decline "on the size bound or on the
  frame's declared window" — are both outside R4's constraint set, so R3's new
  "R4 is the row" clause does not swallow them. R1's clause about encoding 0
  and reserved values is repeated inside R3 and agrees. No contradiction.
- **h07, §21.6 whole table and both closing paragraphs.** The row below
  ("A requested coordinate lies outside the layer's extents | The request fails
  as a request …") is the complement of the new "inside the layer's extents"
  qualifier and now dovetails with it instead of overlapping. The zero-extent
  row ("zero addressed tiles, an empty index, reads returning no samples") is
  consistent. No contradiction.
- **h08, Appendix G item 10 and the closing summary.** The summary's "NFC-
  normalized names, which `[R-ENC-14]` states as a SHOULD" is unchanged and
  still true. Item 3's ordering rules are unaffected. No contradiction.

## 10. Findings

### B-01 — hunk 02: "a compactor MUST refuse the file" collides with §21.6 and `[R-CNT-18]` at layer scope

Repaired text (§20.4, MU = 1 row):

> At either scope a compactor MUST **refuse the file**, on `[R-WRT-06]`'s own
> ground: such a type can define references this specification does not (§7.2),
> so its bytes cannot be safely relocated.

Untouched text it collides with, §21.6's closing paragraph:

> The qualifier is load-bearing — the same type as a layer sub-record is
> reject-layer and **never a ground to refuse the file** (`[R-CNT-18]`), so only
> the top-level case is a file a reader refuses

and §7.4 `[R-CNT-18]`:

> an unknown sub-record type with MU = 1 is reject-layer, and where the file is
> otherwise conforming a reader **MUST NOT reject the file for it**

and the rule the repair cites as its own warrant, §20.5 `[R-WRT-06]`:

> A compactor MUST **refuse to compact** a file carrying any record whose type
> it does not implement with MU = 1

The substance of the repair is right — `[R-WRT-06]`'s "any record" does reach a
layer sub-record, so a compactor genuinely must decline at either scope. What
is wrong is the verb. "Refuse the file" is this document's phrase for the
reader outcome reject-file (§2.4 "The file is not usable"; §21.6 "a file a
reader refuses"), and the sentence immediately before it in the same cell has
just established a reader-outcome frame: "the updater is a reader of the file
first (§2.3), and `[R-CNT-15]` makes an unimplemented top-level MU = 1 record
reject-file". Read in that frame, the repaired sentence tells a compactor to
take reject-file at layer scope, which `[R-CNT-18]` forbids in terms.

Failure scenario. A conforming file (no register row applies) carries layer `A`
with an experimental-range sub-record type, MU = 1, and layers `B` and `C`.
`[R-CNF-02]` and §21.6 make the file conforming; `[R-CNT-18]` makes the
sub-record reject-layer for `A` only. Compactor **X** reads §20.4's MU = 1 row
and reports the whole file rejected, serving nothing. Compactor **Y** reads
`[R-WRT-06]` and §21.6, declines to compact, takes reject-layer for `A`, and
serves `B` and `C`. Two accept/reject verdicts on one conforming file.

Repair: make the verb match the warrant — "At either scope a compactor MUST
refuse **to compact** the file, on `[R-WRT-06]`'s own ground …" — and, if the
distinction is worth stating, add that the refusal is a refusal of the
operation and not the reader outcome, which at layer scope stays reject-layer
(`[R-CNT-18]`, §21.6).

Byte-level: **yes**, on the verdict half of the test. The disputed file is
conforming, and the two readings give different accept/reject verdicts for it
(reject-file versus reject-layer plus service of the intact layers). It does not
move the emittable set — neither reading lets a writer produce anything new.

### B-02 — hunk 05's sweep missed §21.3, whose preamble makes the very claim §21.4's no longer makes

§21.3, untouched:

> Outcome: reject-layer — the named layer is **unusable**, every other
> layer unaffected. 49 conditions.

§21.4, as repaired:

> Outcome: reject-tile — that tile's read reports failure, and never
> returns fill in place of data, **for a rejection the reader is obliged
> to detect** (`[R-CNF-09]`); **where a row's Detector is *verifier* no
> reader is obliged to detect the condition, and the governing rule
> states what a reader does.** 26 conditions.

§21.1, which supplies the qualifier generally:

> For a row whose Detector is *verifier*, the outcome names the scope at which
> the damage is recorded, not an obligation on any reader: the governing rule
> states what a reader does, and for several such rows it obliges the reader to
> serve the structure unchanged (`[R-CNT-22]` … and `[R-MTA-05]`, whose
> unsorted document readers process as they find it — F27 and **L48**).

§21.3 has nine verifier rows (L18, L25, L40, L41, L42, L46, L47, L48, L49). For
L48 and L49 the layer is emphatically usable: L48's own cell says "the document
stays readable and readers process it unchanged", L49's says "readers apply the
type's fixed semantics regardless", and `[R-MTA-05]` says "readers process the
document unchanged". §21.1 names L48 as one of these rows by number, so this is
not a corner the document overlooked elsewhere — only §21.3's preamble states
it wrong, and it is now the only outcome preamble in §21 that does.

Repair: give §21.3 the sentence §21.4 just received — "Outcome: reject-layer —
the named layer is unusable and every other layer unaffected, for a rejection
the reader is obliged to detect; where a row's Detector is *verifier* no reader
is obliged to detect the condition, and the governing rule states what a reader
does (§21.1). 49 conditions."

Byte-level: **no**. `[R-CNF-12]` already licenses a reader to reject a
nonconforming file on any violation it detects, verifier-assigned ones
included, so a reader that refuses the layer on L48 is licensed either way and
the verdict set does not move.

### B-03 — the same unswept gloss in §24's Note, contradicting `[R-VEC-04]` two paragraphs above

`[R-VEC-04]`, normative:

> Where it is the verifier, no reader is obliged to refuse anything (§21.1), so
> the pair is the scope at which a verifier confines its finding … and the
> content a reader owes from **every scope, the damaged one included**.

§24's Note, immediately after it:

> a vector exercising a reject-layer row expects that layer to be **unusable**,
> and an implementation that instead rejects the whole nonconforming file is
> exercising `[R-CNF-12]`'s licence, not failing the vector.

For the nine verifier rows of §21.3 the Note's expectation is the opposite of
what `[R-VEC-04]` had just fixed. A corpus author reading the Note builds an
L48 or L49 vector whose manifest expects the damaged layer to be unusable; a
conforming reader serves that layer, and the vector fails a conforming
implementation. `[R-VEC-01]` says the specification governs and the vector is
corrected, so no implementation is misjudged in the end — but the Note is where
the corpus author looks.

Repair: qualify the Note — "a vector exercising a reject-layer row **whose
detector is the reader** expects that layer to be unusable" — or delete the
clause and let `[R-VEC-04]` stand alone.

Byte-level: **no**. The Note is labelled *Note* and carries no force under
`[R-CNF-01]`; nothing an implementation does turns on it.

### B-04 — F3 is the one of three sibling `[R-ENC-04]` rows written without the in-domain carve-out, and hunk 03's property cannot decide the pair it creates

F3, untouched:

> A sum of a u64 offset and length taken from the file exceeds 2^63 - 1, so the
> sum wraps

Its two siblings, both carrying the carve-out F3 lacks:

> L2 | A declaration-derived sum or product of a layer exceeds 2⁶³ - 1
> **although every contributing field is in domain**
> T12 | A non-sentinel tile-index entry's offset + length exceeds 2⁶³ − 1
> **although each field alone is in domain**

and the governing rule, §4.2 `[R-ENC-04]`, which carries no such qualifier
itself, leaving the carve-out to the rows.

Consequence. F2 ("A u64 offset, length, or count field holds a value above
2^63 - 1", instances including `dir_offset`) and F3 (instances including
`dir_offset + dir_length`) are not disjoint: a file with `dir_offset` = 2⁶³
exhibits both, because the sum is at least the offset. L2/T12 exclude the
corresponding case in one clause; F3 does not. Under hunk 03's new property
F2 and F3 "merely overlap, each reachable without the other" — F3 is reachable
with both fields in domain, F2 is reachable on `generation` — so they "do not
stand in" the specialization relation and the property, which the repair now
advertises as deciding any pair, supplies no answer for a file exhibiting both.
`[R-VEC-02]` rescues the corpus ("the entry records every row the file
exercises and says which it was built for"), but that clause is for conditions
that *cannot* be isolated, and this one can be, in one word, exactly as its two
siblings already are.

Secondary: "so the sum wraps" is not true as stated. Two values each at most
2⁶³ − 1 sum to at most 2⁶⁴ − 2, which does not wrap a u64; it wraps only in the
signed-64-bit arithmetic §4.2's Rationale has in mind. L2 and T12 do not make
this claim.

Repair: bring F3 into line with its siblings — "A sum of a u64 offset and
length taken from the file exceeds 2⁶³ − 1 although each field alone is in
domain" — and drop "so the sum wraps".

Byte-level: **no**. F2 and F3 are both reject-file, Detector reader, Detected
open, so every reader rejects the file under either attribution and no verdict
or emitted byte moves. What moves is which row a corpus entry names.

## 11. What I checked and did not report

- §13's intro "each channel it carries reads as fill at every sample position" —
  omits "inside the layer's extents"; harmless because such positions are never
  returned (`[R-GEO-04]`) and carry the same fill anyway (§14.5).
- T22 against T25 has no tie-break sentence where R3/R4 now does; both are
  reject-tile / reader / tile use, so nothing turns on it.
- Appendix G item 10's consequence names only "a different layer record" and so
  does not reach a decomposed user-metadata *key*; the old text was equally
  layer-record-only, item 10's headline reaches keys, and Appendix G is
  non-normative.
- Appendix H's updater checklist does not mention the compactor's layer-scope
  refusal; it states the reader rejection (`[R-CNT-15]`), which is correctly
  top-level-only, and it is non-normative.
- §21.1's "the property decides any pair" reads as scoped to the relation, which
  the following sentence makes explicit; I did not report the phrase itself.
- §2.4's outcome table glosses reject-tile and reject-layer unqualifiedly, but
  `[R-CNF-09]` three paragraphs below and the verifier sentence in the same
  subsection carry the qualifier; §2.4 is the definitional home and is
  self-correcting.
