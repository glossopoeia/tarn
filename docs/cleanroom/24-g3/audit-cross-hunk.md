# Cross-hunk consistency audit — r24, hunks 01-04

## 0. Access disclosure

Read: `/Users/robertkleffner/Documents/GitHub/tarn/spec/tarn.md`; the four files
`hunk-01.diff`, `hunk-02.diff`, `hunk-03.diff`, `hunk-04.diff`. Did NOT read
`full.diff`, docs/, PLAN.md, OPEN-QUESTIONS.md, AGENTS.md, README.md,
conformance/, spec/registry.json, git history, or the web.

**Breach:** I ran `ls -la` on the hunk directory before reading the instruction
not to list it. Output seen: the five filenames and their sizes
(full.diff 15362 B, hunk-01 2304 B, hunk-02 3951 B, hunk-03 6642 B,
hunk-04 3337 B). No content of full.diff was read. Nothing in that listing
informed any conclusion below.

**Unrequested context:** a project instruction file (CLAUDE.md -> AGENTS.md
pointer) and an index of maintainer memory notes were placed in my context
before I began. They name working cadence, prior failure shapes, and a naming
constraint. I did not read the files they index and drew no conclusion from
them; no finding below traces to them.

Commands run: `sed -n` ranges over spec/tarn.md; `grep -n` for `R-VEC-0`,
`R-CNT-27`, `128`, `version_minor. at the floor`; two `python3` heredocs, one
normalising all whitespace in spec/tarn.md before regex search (the document is
hard-wrapped, so line-oriented grep misses wrapped phrases), one counting
register rows and instances mechanically.

## 1. Grouping — by the rule touched, not the section

The four hunks group on three axes, none of which is the section numbering.

**Group A — [R-WRT-06]'s obligations on a compacted file's trailer: hunks 1 and 4.**
Hunk 1 edits the sentence chain in Sec 20.5 that *states* those obligations
(fresh file_id, generation 1, carry the ignore-lane bits, version_minor floor).
Hunk 4 edits Sec 21.7's *restatement* of exactly the same four, in the same
commit. This is the only pair that touches one rule from two places, and it is
where the two-auditor split is structurally blind.

**Group B — closed counts of register rows asserted in running prose:
hunks 1, 2 and 4.** Hunk 1: "one row for each of the other seven spaces Sec 10.2
tabulates (L31, L33, L34, L36, L43, L45, R1)". Hunk 2: "Four rows are outside
that reasoning and do reach it". Hunk 4: "T2, T4 or T5 fires" and "any of the
four was owed". Each is falsifiable against the register.

**Group C — which rule *establishes* a classification, as against what the
classification says: hunks 2 and 3.** Hunk 2 deletes the claim that
[R-CNT-27]'s 128-byte floor "is established before any field the gate consults
exists" (i.e. that F5's rule precedes Sec 6.2's order). Hunk 3 re-grounds R8's
one-instance collapse: no longer "a judgement under Sec 21.1" but
"[R-VEC-02]'s limit". Both move a rule's home rather than its content — the
document's own signature failure mode.

## 2. The rule each repair adopts, in my words

- **H1.** For a compactor's output carrying a later-minor feature it does not
  implement: exactly two of Sec 10.1's four extension vehicles can appear in a
  *conforming* output (a carried ignore-lane bit; an unrecognised `tarn.` key);
  the other two would appear only as reserved-range values, which the register
  refuses — F36/L25 for the record-type space and exactly one row for each of
  the **seven remaining** spaces Sec 10.2 *tabulates*. Previously the parenthetical
  said "each identifier space Sec 10.2 tabulates", which double-counted record
  type (the table has eight rows, and record type is one of them).
- **H2.** Only four Sec 21.2 rows can bite a file declaring a major other than 1,
  and the reason is uniform: their subject is a field [R-CNT-24] fixes across
  every major. F5 (128-byte floor) is no longer among them.
- **H3.** R8's two forms are one instance-axis. The warrant is not Sec 21.1's
  specialisation rule but [R-VEC-02]: the bare-token form is exhibitable only as
  a co-violation of R7, which is a limit on corpus construction.
- **H4.** A filter change (or a sample move that preserves image length) is not
  witness-free: it fires T2, T4 or T5 wherever the resulting image breaks
  Sec 14.5's padding content or [R-SER-08]'s bool bytes, and is unwitnessed
  otherwise. And [R-WRT-06]'s four trailer obligations share one reason for being
  unwitnessed (nothing marks the output as a compaction output); the last two
  (flags, minor) have a second (the output records neither the input's flags nor
  its minor).

## 3. Mechanical counts

    python3: parse every row of Sec 21.2..Sec 21.5, count ';'-separated instances,
             a cell reading '—' = 1
    -> rows: 121  instances: 277
    -> F 36, L 49, T 26, R 10
    -> R-row instances: R1 4, R2 2, R3 2, R4 16, R5 8, R6 4, R7 6, R8 2, R9 2, R10 2

Matches Sec 21.8 ("121 conditions over 277 instances") and each subsection header
(36 / 49 / 26 / 10). The commit changed no Instances cell, so the arithmetic is
untouched by these four hunks. It is *load-bearing* for X-04: repairing R8 to 4
instances moves 277 -> 279.

## 4. Citation ledger

| Citation in repaired text | Hunk | Verdict |
|---|---|---|
| Sec 10.2 "tabulates" eight spaces; "the other seven" | 1 | PASS. Table rows: record type, channel layout, linearization, sample type, codec, filter, index encoding, metadata encoding = 8. Note the verb is exact: Sec 10.2's prose *names* a ninth space ("the trailer's flag lanes, which Sec 6.3 partitions instead") that it does not tabulate. "tabulates" excludes it; "names" or "defines" would not have. |
| L31 / L33 / L34 / L36 / L43 / L45 / R1 map one-to-one onto those seven | 1 | PASS. L31 index_encoding; L33 linearization; L34 sample type; L36 layout(channel layout); L43 codec; L45 filter; R1 metadata encoding (reserved 3-0x7F). Each space has exactly one register row for its reserved range. |
| F36 and L25 "for a record type" | 1 | PASS in context. F35/L24 also register reserved-range types, but only with MU = 1, and Sec 20.5's closing sentence makes a compactor refuse any unimplemented MU = 1 type, so the MU = 1 case cannot reach an output. |
| "the two of Sec 10.1's four vehicles Sec 21.6 makes conforming" | 1 | QUALIFIED FAIL -> X-06. Sec 21.6 also makes vehicle 1 conforming (experimental record type, MU = 0) and a vehicle-2 value conforming (experimental metadata encoding). True only under the sentence's later-minor premise. |
| [R-CNT-24] as "a field fixed across every major" | 2 | PASS. [R-CNT-24] fixes the trailer magic at F-64, version_major/minor at F-56, the CRC at F-4, and the constancy of the front block — covering F8, F1 (both instances), F14, F6. |
| "the two checks Sec 6.2 places before the gate" | 2 | PASS. [R-CNT-06]: "A reader MUST validate, in order: the trailer magic; the trailer CRC; the version gate". |
| [R-CNT-04] "places [the front block] before other processing" | 2 | PASS. Sec 19.1 step 1 and [R-CNT-04] both, for a reader holding [0,16) resident. |
| Sec 21.6 for F18 "permanently invalid in every one" | 2 | PASS. Sec 21.6's closing paragraph names version_major = 0 (F18) exactly so. |
| [R-VEC-02] as the warrant for collapsing R8's instances | 3 | FAIL -> X-04. [R-VEC-02] does address non-isolable conditions, and resolves them the *other* way: "the entry records every row the file exercises and says which it was built for". It licenses building the vector; it removes no instance. |
| Sec 21.1 disclaimed ("rather than a judgement under Sec 21.1") | 3 | Sec 21.1 is the section that *defines* the Instances column and its axes, and states "where a row and the rule it cites diverge, the rule governs". Disclaiming it does not move the column's definition. -> X-04. |
| R7 as the co-violated row | 3 | PASS. Sec 18.1's [R-MTA-04] bullet: bare `NaN`/`Infinity`/`-Infinity` "RFC 8259 does not admit", so R7 ("not well-formed JSON") fires; `1e400` is well-formed JSON and fires R8 alone. |
| "the same terms T26 states for a wrong stride" | 4 | FAIL -> X-03. T26 states "the check that detects it is T2's or T4's". The repair states T2, T4 **or T5**. |
| Sec 14.5 padding content / [R-SER-08] bool bytes | 4 | PASS, and it is what convicts T26: Sec 14.5's [R-SER-05] covers padding positions *and* "Every pad bit (Sec 14.3) MUST carry the plane's channel's fill bit" — the pad-bit half is T5, not T4. [R-COD-10] itself cites "Sec 14.5's padding" whole. |
| Sec 17.3 "both filter values are length-preserving" | 4 | PASS. Filter 1 = none; byte-shuffle: "Length is unchanged." |
| T3 / T14 as length witnesses | 4 | PASS. T3 tests the decoded payload's length, T14 the codec-1 entry's declared length. |
| Sec 20.5's "four obligations ... on a compacted file's trailer" | 4 | PASS as a count of Sec 20.5's trailer obligations: fresh file_id, generation 1, carry ignore-lane bits, version_minor floor. But see X-01 (Sec 20.5 itself says "Neither obligation", i.e. two) and X-02. |
| [R-ENC-06] "fixed field widths are not a state a file can be in" | 4 | PASS. [R-ENC-06]: "No field's width is ever a writer choice ... a structure whose fields appear at any other width is invalid at its owning scope." |

## 5. Check 7 — analogy verbs, side by side

**H4 vs T26.** Repair: "is witnessed on the same terms T26 states for a wrong
stride: where the resulting image breaks Sec 14.5's padding content or
`[R-SER-08]`'s bool bytes, **T2, T4 or T5** fires". T26: "where the resulting
image breaks Sec 14.5's padding content or `[R-SER-08]`'s bool bytes ...; **the
check that detects it is T2's or T4's**". Governing verbs are identical
("breaks ... padding content or bool bytes"); the *witness sets* are not —
three rows against two. The analogy carries one clause over several rows and
fails on the third. Sec 21.7's own untouched earlier sentence already says
"a mis-ordered image is then witnessed by T2, T4 or T5, exactly as a
mis-strided filter is" — so the document now says T5 twice and T26 still says
it does not. Substantively T5 wins: a packed planar bool plane is the one place
T26 enumerates an identity stride ("packed planar bool: identity s = 1"), and a
wrong stride there corrupts final-byte pad bits, which is T5's predicate and
not T4's. -> X-03.

**H1 vs Sec 10.2.** "one row for each of the other seven spaces Sec 10.2 tabulates"
against Sec 10.2's "The spaces, defined in the sections that own them and collected
here" + an eight-row table. Ranges over the same set. PASS.

**H3 vs [R-VEC-02].** Repair's verb: the bare token is "exhibitable only as a
co-violation of R7, **which is [R-VEC-02]'s limit**". [R-VEC-02]'s verb: "where
a condition cannot be isolated ... **the entry records every row the file
exercises and says which it was built for**". Same set (non-isolable
conditions), opposite disposition: [R-VEC-02] builds the vector and records
both rows; the repair drops the instance. FAIL -> X-04.

**H4 vs [R-LIF-01].** "unwitnessed there for the same reason `[R-LIF-01]` is:
it is a property of the prior generation, which Sec 9.7 does not reconstruct".
[R-LIF-01] is indeed history-scoped ("every conforming mutation of a file is
either a commit or a whole-file rewrite under a new file_id"). PASS.

## 6. Check 4 — the passages around each repair

**Sec 20.5, untouched sentence three lines below hunk 1's edit:**
"Otherwise version_minor follows `[R-CNT-26]`'s floor. **Neither obligation has
a witness in the output alone (Sec 21.7).**"
Nearest antecedents are the two version_minor obligations. Under that reading
the sentence is false: [R-CNT-26]'s floor *is* witnessed from the output alone
("for a file expressible under this text, 0" — a checker enumerates the features
present and compares), which is exactly why Sec 21.7 does not list [R-CNT-26]
among the undetectables. Under the other reading ({flags MUST, minor SHOULD})
the sentence is true but counts two where Sec 21.7, as hunk 4 rewrote it, counts
four and asserts a reason all four share. -> X-01.

**Sec 21.2 preamble after hunk 2:** the complement of the four is still labelled
"the rows below whose subject is that file's *geometry*", but F24 (type 0x0000),
F27 (document member ordering), F34 (two metadata records), F15, F19, F25, F26
have no geometric subject at all, and every other use of "geometry" in this
document means a *layer's* geometry (Sec 11.1, L21, L32, Sec 10.4, Sec 23.2). The
operative phrase after the repair is "outside that reasoning", and *that
reasoning* is Sec 6.2's gate order, which reaches all 32 non-excepted rows.
-> X-05. Note also that F18's subject (version_major) *is* a field [R-CNT-24]
fixes across every major, so it satisfies the repair's new "because" criterion
while being excluded from the four; the passage rescues this in its next
sentence ("outside the premise"), so I do not raise it separately.

**Sec 21.5 R8 after hunk 3:** the register's own practice three subsections up
contradicts the collapse. T13, T15, T16, T23 and T26 are all rows that "record
the cause rather than a procedure of its own" — every file exhibiting them
exhibits another row's predicate too — and every one of them enumerates its
alternatives as instances (T13: 2, T15: 2, T26: 3). R8 is the sole row that
suppresses an alternative for non-isolability, and the repair supplies it a
warrant rather than removing the anomaly. -> X-04.

**Sec 21.7 after hunk 4:** Sec 20.5's "It MUST mint a fresh file_id for the output
— a new draw under Sec 9.3's randomness advice, **not merely a value compared
against the input's**" is three lines from hunk 1's edit and is the clause that
falsifies "The last two are unwitnessed twice over". Appendix G item 8 agrees:
"`[R-WRT-06]`'s fresh file_id is no function of content". -> X-02.

## 7. Check 6 — what each repair left open

- **H1 / the output trailer.** Fields: magic, version_major, version_minor,
  flags (incompat lane 0-15 + ignore lane 16-31), generation, dir_offset,
  dir_length, committed_file_length, file_id, reserved [56,60), CRC. Sec 20.5 pins
  file_id, generation, the ignore lane, version_minor. The incompat lane is
  pinned transitively (F19 makes any set incompat bit a violation, so a
  conforming input's lane is 0). Everything else is pinned by [R-CNT-06] /
  Sec 6.2's table. **No sibling left unpinned.**
- **H2 / Sec 21.2's 36 rows against a major != 1 file.** Four classified as
  reaching, F18 classified as outside the premise, F5 moved into an unnamed
  bucket, ~25 rows unclassified by the "geometry" label. -> X-05.
- **H3 / row R8.** The Condition cell now argues instances; it does not say
  which row a `{"a": NaN}` file is *recorded against* in the register, having
  expressly disclaimed Sec 21.1 (whose specialisation rule is the only attribution
  machinery the document has). The three bare tokens are also treated as one
  shape without a stated reason. -> X-07.
- **H4 / Sec 21.7's account of [R-WRT-06].** The clause scopes itself to "a
  compacted file's trailer", leaving Sec 20/[R-WRT-07]'s equally history-dependent
  obligations unnamed anywhere in Sec 21.7: the MU = 1 refusal, "slack is never
  carried" (an output carrying superseded structures is a conforming file), and
  "The output's reference arrays MUST equal the live generation's bit for bit".
  Sec 21.1 calls Sec 21.7 "the account, **by class**, of what fails" detectability.
  -> X-08 (low; the "property of the prior generation" class arguably absorbs
  them).

## 8. Byte-level test

None of X-01..X-08 is byte-level.
- X-03: the disputed file (packed bool plane, wrong stride, corrupt pad bits) is
  nonconforming under both readings, because T5 is an independent Sec 21.4 row a
  verifier checks regardless of T26's cross-reference. Verdicts agree; only the
  row a vector is *attributed to* moves.
- X-04: a bare-token document is ignore-record under both readings. What moves
  is the corpus (whether a bare-token vector exists) and Sec 21.8's total, not any
  accept/reject verdict.
- X-05: a file declaring major != 1 is refused by every conforming reader under
  both readings; the dispute is nonconforming-vs-not-judged, and no conforming
  writer emits such a file under this text in either case ([R-CNF-05]).
- X-01, X-02, X-08: Sec 21.7 is an account of what no check detects; no reader or
  writer behaviour turns on it.
- X-06, X-07: wording.

## 9. Direction of each disagreement

X-01 Sec 20.5 changes (Sec 21.7 is right).
X-02 Sec 21.7 changes (Sec 20.5 and Appendix G are right).
X-03 T26 changes (Sec 21.7, twice, is right).
X-04 R8's Instances cell changes, or Sec 21.1 gains an explicit isolability axis —
     maintainer decision; the repair's warrant is wrong either way.
X-05 Sec 21.2's preamble changes.
X-06 Sec 20.5's parenthetical changes (Sec 21.6 is right).
X-07, X-08 the repaired text changes.
