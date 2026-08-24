# Round 23 triage — SKEPTIC pass, working transcript

## Access disclosure

Read in full: `/Users/robertkleffner/Documents/GitHub/tarn/spec/tarn.md` (all 4426 lines,
in eleven `sed` windows plus targeted greps).

Read NO walk transcript. Read NO `transcript-triage-*.md`; I did `ls` the round23
directory once in my first tool call, before I had internalised the prohibition on
listing it, and saw the filenames only — `calc.py`, `count.py`, and the nine walk/quiz
transcripts. No `transcript-triage-*` file existed at that moment and I opened nothing.
I did not use `calc.py` or `count.py`; I wrote my own counter (`mycount.py`, in the
scratchpad root, not in round23/).

Ran: `zstd` (homebrew, /opt/homebrew/bin/zstd) against four hand-assembled RFC 8878
frames I built with python3; a python instance-counter over §21.2–§21.5's tables.

Read nothing from `docs/`, `PLAN.md`, `AGENTS.md`, `conformance/`, `registry.json`,
git history, or the web.

## Method

Lens is skeptic: for each finding I hunted for the sentence that forecloses it before
crediting it. Where I found one I quote it. Where I looked and could not find one I say
so explicitly — that absence is the strongest evidence for the finding.

Two mechanical checks I ran rather than reasoned about:

**(1) Instance arithmetic.** Independent counter over §21.2–§21.5 applying §21.1's rules
(semicolons separate; an em-dash cell is one):

    21.2: 36 rows,  58 instances
    21.3: 49 rows, 116 instances
    21.4: 26 rows,  55 instances
    21.5: 10 rows,  48 instances
    TOTAL 121 rows, 277 instances

§21.8's "121 conditions over 277 instances" is exactly right. quiz-02's per-subsection
breakdown is right to the number. Its incidental figure is not: em-dash cells number
**40**, not 42, so a counter that scored them zero would land 40 low, not 42.

**(2) zstd Frame_Content_Size behaviour** (adversary-01 Reading C / reader-03).
Hand-assembled frames carrying the 18-byte document `{"tarn.title":"x"}`:

    honest  28b52ffd20129100007b227461726e2e7469746c65223a2278227d   → decodes, rc=0
    liar2 (Window_Descriptor, FCS = 512 MiB) → "Decoding error (36) : Data corruption detected"
    liar3 (FCS = 100)                        → "Decoding error (36) : Data corruption detected"
    liar4 (FCS = 5)                          → "Decoding error (36) : Data corruption detected"

So the reference decoder refuses an FCS mismatch **in both directions**. §18.2's "the
bytes decode, and what is wrong is what the header said about them" is false for it, and
R4's "a reader that only tries decoding establishes none of them" is false for the
content-size instance specifically. This is the one place a reporter's empirical claim
survived independent reproduction, and it kills the routing's stated justification.

**(3) adversary-03's second construction, made concrete.** A ten-byte single-segment
zstd frame decoding to exactly ten bytes:

    28b52ffd200a53000041  →  "AAAAAAAAAA"  (10 bytes)

magic present (T17 silent), one frame (T18), Dictionary_ID 0 (T19), no content checksum
(T20), Window_Size = FCS = 10 = decoded size so no window overrun (T21) and no FCS
mismatch (T22), consumes the extent exactly (T24), decodes cleanly (T25), decoded length
= decoded size (T3). A layer whose decoded size is 10, storing this byte string under
codec 1, re-declared to codec 3 by a later commit, is undetected by every row §21.7
names. adversary-03's claim is not merely arguable; it is constructible, and I built it.

## Grouping

Nineteen ids, seventeen groups. Two merges:

- `reader-01` + `adversary-04`: both say §21.9 bounds a decoded size and a window but no
  row bounds the stored length a reader must fetch and CRC, and both invoke [R-ERR-04]'s
  "declines on that ground" as removing the escape. adversary-04's second theme (the
  rows are never composed) is a sub-claim of the same complaint about §21.9's coverage.
- `reader-03` + `adversary-01`: both attack §18.2's content-size sentence and its R4
  routing; adversary-01's Reading C *is* reader-03's finding, reached empirically.

Three findings sit in one §21.7 sentence and I deliberately did **not** merge them,
because they have three different repairs and three different verdicts: quiz-01 (the
"only where" conjunct), diagrams-01 (the enumeration omits the filter and the
sample-byte-offset item), adversary-03 (the codec clause's positive witness claim is
false). diagrams-01 independently raises quiz-01's point as a "smaller point"; the
reconciler should treat those two as corroborating even though they are separate groups.

---

## Group-by-group

### 1. unbounded-stored-extent-length — reader-01, adversary-04 — PARTIAL, not byte-level

Facts verified. §21.9's table has eight rows; none names a stored extent's length. §15.3
bounds it only by `length ≥ 1` and `offset + length ≤ F − 64`. §19.4 step 5 obliges the
whole-extent fetch and CRC before decode. §17.2's closing Note does end "Resource limits
are §21's subject." All true.

The ambiguity claim is what I killed. Both reporters offer a reading under which a reader
may cap. It cannot, and two rules say so:

> "Readers MAY enforce resource limits, but MUST accept any conforming file within the
> minimum guarantees stated in §21's limits table" — `[R-CNF-10]`

> "A reader MUST accept every conforming file of a format major version it implements …
> and none of whose values exceeds the minimum guarantees of §21's limits table" — `[R-CNF-03]`

A file whose stored tile extent is multi-gigabyte but whose eight table quantities are all
inside the table **is** a conforming file within the guarantees. MUST accept. [R-ERR-04]'s
narrower "on that ground" clause grants nothing; it only names which declines are
nonconforming. So [R-CNF-10]'s MAY is exhausted by files that *do* exceed a row, and reader-01's
reading (ii) has no footing. reader-01 picked (i) and (i) is simply what the text says.

The metadata half is decided the same way, and additionally by [R-CNT-25]'s closed
enumeration — "a failed extent CRC, an unimplemented or invalid encoding, a decode
failure, or content violating the document's own rules" — which does not include a
too-large stored extent; §18.2's only decline routes are the decoded-size bound and the
declared window.

adversary-04's composition worry I also weakened, with the document's own answer:

> "the index is the cheapest hostile amplifier: entry_count is one `u64`, and
> `[R-CNT-17]`'s cross-check ties it to the region's declared length while `[R-CNT-13]`
> ties that length to the file's actual size — a reader that validates both before
> fetching cannot be induced to read more than the file contains." — §22.2 Note

Every one of the 2.8 × 10¹⁴ index entries adversary-04 fears occupies twenty real bytes,
so the file carrying them is ~5.6 PB. The coverage walk is linear in F, not in the
declarations. The composition is self-limiting.

What survives is a design position, not an ambiguity: this specification obliges a
conforming reader to fetch and checksum an arbitrarily large single extent, and §17.2
sends an implementer to §21 for a bound that is not there.

**Byte-level: no**, on the premise that "within the minimum guarantees stated in §21's
limits table" is satisfied by a file all of whose *table-named* quantities lie within the
table. Anyone attacking the downgrade must argue a file can fall outside the guarantees on
a quantity the table does not state — which would leave the phrase referring to nothing.
Note for the gate: **a repair here would be byte-affecting.** Adding a §21.9 row for a
stored extent's length moves files out of the must-accept set. The current text is
unambiguous; the fix is not free.

### 2. metadata-content-size-routing — reader-03, adversary-01 — CONFIRMED, not byte-level

This is the group I tried hardest to refute and could not.

I searched §18.2, §17.2, §21.5 and Appendix F's neighbourhood for a sentence saying how a
reader obtains the decoded length without a successful decode, or licensing an
FCS-ignoring decode mode. There is none. The section states the constraint in the
writer's voice ("when present it MUST equal the byte length of the decoded document") and
supplies the reader's obligation only through R4 plus [R-CNF-04] — which is exactly the
pairing §2.1's Note promises never to leave open:

> "every writer-side prohibition is paired with an explicit reader-side clause stating
> what a reader does with a violating file"

And the justification the section gives is falsified by the reference decoder, three times
over (see check (2) above):

> "A mismatch is one of the frame constraints R4 registers, not a failure to decode under
> R3: the bytes decode, and what is wrong is what the header said about them. Routing it
> to R4 keeps the condition checkable from the bytes alone rather than turning on a
> decoder's tolerance (`[R-CNF-02]`)"

It turns on a decoder's tolerance precisely. reader-03's disanalogy is also correct on its
own terms: [R-COD-06]'s tile comparand is declaration-derived and header-checkable; a
document has no declared size — §18.2 says so itself ("a document has no declared size") —
so the comparand is obtainable only by decoding.

Where I *did* refute a reporter: adversary-01's Reading B verdict split does not survive.
A verifier whose one-shot decode fails has not established that the document exceeds its
bound; §18.2's decline is available only where "a document exceeding that bound"
is the case, and this 18-byte document does not exceed any bound. Nor may the verifier
infer the document's size from the frame's claim — [R-CNF-04]: "A reader MUST NOT …
infer values this specification does not define", reinforced by the carried-over "bar on
sizing any buffer from a length the frame itself declares". So the honest Reading-B
verifier records a decode failure → R3 → **nonconforming**, the same verdict Reading A
reaches by R4. The split collapses.

**Byte-level: no.** R3 and R4 carry the identical detector (reader), tier (extent use) and
outcome (ignore-record), and §21.5 fixes that both make the file nonconforming: "Every row
here is a violation all the same". No served byte, no accept/reject, no verdict moves.
What moves is which row a report and a manifest name — and four of R4's sixteen instances
would migrate to R3, leaving §21.8's 277 unchanged (16→12, 2→6).

### 3. json-nesting-depth-unbounded — adversary-02 — PARTIAL, DOWNGRADED from byte-level

The only self-flagged byte-level finding, so I state my premise plainly for attack.

Confirmed facts: RFC 8259 §9 permits depth limits; §18.2 pins four other RFC 8259
freedoms and says nothing about depth; §21.9's table has no depth row; [R-ERR-05]'s
hard-limit list has none; [R-CNT-25]'s enumeration of unreadability does not reach it. The
1.14 MiB, 200,000-deep document is a conforming file. All true.

The reporter's dilemma — "ship a formally nonconforming verifier or map its parser's error
onto R7 and call a conforming file nonconforming" — is what I refuted, on three sentences.

*The R7 route is barred.* R7's condition is "A decoded user-metadata document is not
well-formed JSON, or its top-level value is not an object". A 200,000-deep object **is**
well-formed JSON: RFC 8259's grammar has no depth bound, and §9's latitude is about
implementations, not about what a JSON text is. Reporting it under R7 is inferring a value
the specification does not define — [R-CNF-04] bars that in terms.

*The reader is not obliged to touch the document at all.*

> "Structures a request never relies on impose no detection obligation beyond the open
> steps: a violating record in a layer never accessed leaves every other layer's reads
> conforming." — `[R-RDR-02]`

and §19.2's tier for this material is "at use of a record's extent … no earlier, since the
open fetches no extent". I grepped for any obligation to surface a metadata document to a
caller: the only `MUST return` obligations in the document are [R-MDL-02]'s reference-array
rule and [R-TYP-06]'s fill. There is none for metadata. A depth-limited reader accepts the
file, serves every sample bit-exactly, and never uses the extent. Fully conforming.

*The verifier's cannot-establish route is licensed.* §2.3 states the ground generally and
introduces its list with "as when", not "exactly when": "*cannot establish* — the last
where some requirement is one it is unable to check on a capability or resource ground, as
when …". A stack-bounded parser is unable to check [R-MTA-04] on a resource ground.

*And the resulting verdict variation is already a designed property of this document,
not an ambiguity.* Two conforming verifiers already give different verdicts on identical
conforming bytes, by design, in at least two places:

> "A verifier that cannot execute a layer's codec or filter cannot establish that layer's
> conformance and MUST NOT certify the file. That inability is not a finding that the file
> is nonconforming" — `[R-COD-11]`

> "the bound is that verifier's capability and not a limit on validity (`[R-CNF-10]`), so
> the decline is not a finding that the file is nonconforming" — `[R-MTA-09]`

**My premise, stated for attack:** "must accept or reject" means a reader's
file/layer/tile/record outcome and a verifier's *nonconforming* finding — not the
certify-versus-cannot-establish distinction. If a reconciler treats that distinction as a
byte fork, then [R-COD-11] and [R-MTA-09] make this specification byte-level ambiguous by
construction, which cannot be the intended reading of the gate. The file's conformance is
determinate (conforming) and every conforming reader accepts it.

What survives, and it is worth a maintainer's decision: §18.2 anchors the reader's *size*
bound and *window* bound to §21.9 floors ("no smaller than §21.9's user-metadata
guarantee", "no smaller than §21.9's guarantee for that quantity") and anchors the parse
depth to nothing. A writer relying on §21.9 has no depth floor to rely on. As with group 1,
**a repair here would be byte-affecting**: a §21.9 depth row would move deep documents out
of the must-accept set.

### 4. compactor-not-bound-to-commit-protocol — writer-01 — CONFIRMED, not byte-level

Grep verified: `[R-LIF-02]` is cited at lines 154, 567, 759, 1180, 1239, 1253, 2921, 2929,
2977, 3065, 3066, 4282. §20.5 (lines ~3160–3260) is not among them, and the words
"barrier", "durable" and "fsync" do not occur anywhere in §20.5. The reporter's grep holds.
The asymmetry is real: §20.2 binds "A creator" to [R-LIF-02]'s creation path "steps 4–6 —
both barriers, not one", §20.3 step 6 binds the appender to "steps 4–6", §20.5 binds the
compactor to nothing procedural.

The byte half is closed by the document, twice, in terms:

> "bounds their number only through step 5 of the commit protocol, which pads to the next
> 64-byte boundary (`[R-LIF-02]`) — **a longer gap is conforming**, and no conforming
> commit produces one." — `[R-CNT-05]`

> "A writer obligation whose violation this specification expressly declares not to be a
> file-conformance violation binds the actor in the same way; §6.3's flags = 0 against a
> set ignore-lane bit and **§6.2's pre-trailer gap longer than `[R-LIF-02]` step 5's pad**
> are the cases this text states" — `[R-CNF-02]`

So writer-01's "single row of my byte-divergence catalogue I could classify as neither
legitimate nor forbidden" is in fact expressly classified: conduct, not bytes. The
reporter reached this itself and graded honestly.

What is left is durability, and there the silence is real and I found nothing to close it.
Appendix G item 3 does cover the pad ("§6.2's 64-byte trailer alignment, the pre-trailer
pad included") but Appendix G is headed "(non-normative)" and says "It adds no requirement
to any actor". A one-clause repair in §20.5, the shape §6.3 already writes for flags.

### 5. min-file-size-unordered-vs-version-gate — verifier-01 — PARTIAL, not byte-level

The observation is right: [R-CNT-27] appears in neither half of [R-CNT-06]'s ordered list
nor in §19.1's four steps. I checked both.

The verdict is not open, and the reporter quotes the sentence that closes it while calling
it open:

> "the rows below whose subject is that file's *geometry* do not reach it: §6.2 puts the
> version gate ahead of every check but the trailer magic and the trailer CRC, so such a
> file is refused on capability grounds first. Four rows are outside that reasoning and do
> reach it … F8 and F1's trailer-magic instance, F14's trailer CRC … and F6 with F1's
> front-block instance" — §21.2 preamble, normative under [R-CNF-01]

F5's subject is the file's geometry and F5 is not one of the four. Reading (B). And §2.3
independently forbids the (A) verdict for any actor:

> "a file declaring another major is neither conforming nor nonconforming under it: a
> reader refuses such a file on capability grounds (§6.3, `[R-CNT-07]`), and that refusal
> is not a finding about its bytes." — `[R-CNF-02]`

I checked the reporter's 96-byte construction: F = 96 is not a multiple of 64, but F13 is
a post-gate check so it does not fire under (B) either; the construction does isolate the
question as claimed. Under (B) the verifier reports cannot establish and makes no finding.
Determinate. Byte-level: no — both readings refuse the file, and [R-CNT-07] independently
obliges reject-file.

### 6. unassigned-type-extent-not-reported — verifier-02 — CONFIRMED, not byte-level

I hunted for a naming duty and found none. [R-CNT-21]'s duty is the *slack* total and
those bytes are not slack — [R-CNT-02] names "a record extent (the bytes any record's
extent slot references, whatever the record's type)" as a claimant class, and §9.7's walk
reaches them as claimants. [R-MTA-10]'s duty is scoped to its own subject. §22.3 states the
residue and states no report. §8.1's map gives the extent no checksum at all.

So the asymmetry the reporter names is real: the *weaker* uninspected population (no
checksum) gets no report line while the stronger one (terminal CRC) gets a MUST-report
under a stated principle — "bytes a certificate covers without inspecting are counted and
named, never silent".

Byte-level: no, and [R-CNF-11] says why a report duty cannot be: "that per-requirement
report constrains the report and not the verdict".

### 7. s217-only-where-scoping — quiz-01 — CONFIRMED, not byte-level

Straightforwardly true: "witnessed only where … the change reaches a byte §14 structurally
constrains" followed two clauses later by "a change that reaches the decoded size instead
is witnessed by T3 or T14" is a literal contradiction if "only" scopes both conjuncts.
Reading (a) — "only" governs the remain-stored conjunct — is the one on which every clause
is true, and the sentence's own closing presumes it: "a commit that supersedes every tile
it would have damaged leaves the live state clean, so the bar is unwitnessed there".

Byte-level: no. §21.7 assigns no obligation, and §20.3 step 4's MUST NOT binds the writer
identically under every reading.

### 8. s217-filter-and-offset-omitted — diagrams-01 — PARTIAL, not byte-level

The omission is real and I verified the unwitnessedness. §20.3 step 4 bars four things;
§21.7 accounts for the padding set, the decoded size, and the codec. The filter and "the
byte offset of any sample within the decoded tile image" are not named. And the filter case
genuinely has no witness: §17.3 fixes "Length is unchanged" and "The decoded image's length
L is divisible by s in every case", so a filter 1→2 re-declaration on a layer with no
padding position, no pad bit and no bool channel moves no structurally constrained byte —
T2, T3, T4, T5, T14 and T26 are all silent.

Where I refuted the reporter: its framing rests on §21.1 making §21.7 normatively
complete. §21.1 says the opposite, in the same paragraph diagrams-01 quotes from:

> "The subsections after §21.5 are not part of the register and carry no rows: **neither
> this completeness clause nor the instance arithmetic below reaches** §21.6's defined
> non-violations, **§21.7's account of what no check detects**, or §21.9's limits."

So an incomplete §21.7 is a documentation defect, not a violation of the register's
normative completeness. Byte-level: no — §21.7 is descriptive and §20.3's bar decides the
writer's conduct in both readings.

### 9. s217-codec-witness-overclaimed — adversary-03 — CONFIRMED, not byte-level

Both clauses fail, and I built the harder of the two constructions (check (3) above): a
ten-byte single-segment zstd frame decoding to exactly ten bytes silences T3, T17, T18,
T19, T20, T21, T22, T24 and T25 after a codec 1 → 3 re-declaration. The T14 direction is
easier still — raw DEFLATE of tuned input landing exactly on D. I looked for a qualifier
elsewhere in §21.7 or §20.3 that would rescue the unconditional claim and found none.

Byte-level: no — in exactly the cases where the claim fails, the violation is undetectable
by construction, and §21.1's carve-out (quoted in group 8) means the shortfall is not a
register-completeness violation. The repair is a qualifier on one clause.

### 10. vec04-sibling-scope-vs-rationale — diagrams-02 — CONFIRMED, not byte-level

Verified. The requirement enumerates reject-layer and reject-tile; the rationale reaches
"every vector built from §21's register", and §21.5 states in terms that its rows are
violations and their files nonconforming ("Every row here is a violation all the same").
The reachable gap is real: R1's top-level instances against a zero-layer file
(conforming per §21.6's "The file contains zero layers") leave a scoping reader and a
file-rejecting reader observationally identical.

I looked for a sentence narrowing the rationale or extending the requirement and found
none; [R-VEC-03]'s coverage clause adds no sibling duty. Half of R1's instances carry a
layer by construction (the sub-record ones) but nothing obliges that layer's content to be
recorded, so the gap stands for the top-level instances.

Byte-level: no — "where a vector's recorded expectation and this specification disagree,
this specification governs and the vector is corrected" ([R-VEC-01]). The cost is the
corpus's discriminating power.

### 11. s47-note-overstates-s72-ranges — diagrams-03 — CONFIRMED, not byte-level

Verified against §7.2's table: five fields, ranges folded into two Field cells (`type (0
invalid)`; the flags bit assignment with `bits 2–15 reserved`), three bare. The ranges are
stated normatively nearby — [R-CNT-12] for inline_length, [R-CNT-13] for the extent slot,
[R-ENC-03] for the u64 domain.

The killing sentence for byte-level is the label on the defective text itself:

> "All text in this document is normative except: §1 (Introduction); any text labeled
> *Note*, *Example*, or *Rationale*" — `[R-CNF-01]`

§4.7's claim sits inside a block headed "> **Note.**". A charitable reading is available
and worth recording — the clause may be explaining why §7.2's table has no "Valid values"
column rather than promising a range per field — but the literal claim is not delivered.

### 12. r8-instance-undercount — register-01 — CONFIRMED, register-bookkeeping

§21.1's collapse licence is conditioned on shape: "a row whose check ranges over a family
**without the condition changing shape** states that range as a single instance (T24's
*any codec*), and one whose members give the condition materially different shapes
enumerates them (T15, T25)."

The shapes do differ. `1e400` needs a decimal→binary64 conversion and an overflow test;
`NaN` / `Infinity` / `-Infinity` are tokens RFC 8259's grammar does not admit, which
§18.2 itself flags as reaching this check only through a lenient parser ("which RFC 8259
does not admit and some parsers accept regardless") — a strict parser meets them at R7, not
R8. That gap is wider than T15's zlib-versus-gzip, which the register does enumerate. The
three bare tokens collapse to one alternative among themselves, so the arithmetic is 2 × 2
= 4 and §21.8 becomes 279.

One correction to the reporter: R2, R3, R9 and R10 also carry two instances, so R8 is not
"the only row that does not multiply" — it is the only row whose *rule text is
disjunctive* and whose cell does not. The substance is unaffected.

Byte-level: no — [R-MTA-04]'s own disjunction binds either way and both forms take
ignore-record.

### 13. r6-governing-rule-inconsistent — register-02 — PARTIAL, register-bookkeeping

The inconsistency is real: two clauses of [R-MTA-04]'s fourth bullet produce R6 (governing
`[R-CNT-25]` (R-ENC-12)) and R10 (governing `[R-MTA-04]` (R-ENC-12)), and [R-VEC-02] makes
the (row, identifier) pair a vector's durable identity, so two vectors from one sentence
carry permanently different identifiers.

But the reporter's central argument rests on a selective quote and does not survive. It
says "[R-ENC-12] expressly excludes document keys from its own scope". It does not:

> "**Names** — the strings that identify layers, dimensions, channels, **and
> user-metadata keys** — satisfy three further constraints. Writers MUST NOT emit a name
> that violates any of them; a reader MUST treat such a name as a validity error at the
> owning scope — except for a key inside a user-metadata document, where `[R-CNT-25]`'s
> quarantine governs and the outcome is ignore-record." — `[R-ENC-12]`

The exception is to the *outcome*, not to the constraints, and the constraints are
expressly stated over user-metadata keys. [R-ENC-12] is in R6's parentheses, so §21.1's
tie-break does **not** resolve to nothing: it resolves to [R-ENC-12], which says non-empty
and C0-free in so many words. The defect is cosmetic consistency across R6 and R10, not a
dangling tie-break.

### 14. compaction-parenthetical-row-list — register-03 — PARTIAL, editorial

Verified: §10.2 tabulates eight identifier spaces, seven of them vehicle 2's, and the
register carries a reserved-range row for each (L31, L33, L34, L36, L43, L45, R1). The
parenthetical names one.

The reporter says it tried and failed to find a reading that makes the list complete, and
its attempt fails for a reason it did not notice: it conflates *detection* with *obliged
refusal*. The six layer rows are reject-layer, so §19.3's validation fails and [R-WRT-06]
bites — "A compactor MUST refuse to compact when any check `[R-WRT-09]` obliges fails" —
whereas R1's outcome is ignore-record, which does not fail the open. There is also a
principled selection available on the input side: the only two identifier spaces where an
unassigned value can appear in a *conforming* file are record type (experimental, MU = 0)
and metadata encoding (experimental ≥ 0x80), both of which §21.6 records as
non-violations; in the other six spaces any unassigned value is an immediate reject-layer.
Those two spaces are exactly F36/L25 and R1.

I could not make that principle airtight — a reserved-range metadata encoding is a
violation the compactor would also detect, so R1's own presence is not fully earned
either — so the citation is at best under-explained. Nothing normative turns on it: the
sentence's operative content is an ignore-lane MUST and a version_minor SHOULD.

### 15. s218-instance-total-unverifiable — quiz-02 — CONFIRMED, editorial

I reproduced the count independently and it is right (see check (1)). The finding is a
presentation request — per-subsection subtotals — and I agree the aggregate is expensive
to falsify locally. Its incidental em-dash figure is wrong: 40, not 42.

Byte-level: no; [R-VEC-01] makes the corpus derivative.

### 16. s219-first-five-rows-quantifier — quiz-03 — REFUTED, editorial at most

"The first five rows range over declarations, which every file and every layer carries" is
an ordinary relative clause, quantified over the layers a file has. Reading (b) — that it
asserts at least one instance always exists — is not a reading a relative clause supports,
and two sentences foreclose the conclusion it is said to license:

> "Either way a file containing no instance of a kind does not exceed that row, whatever
> its declarations would derive." — §21.9, the sentence immediately preceding

> "The file contains zero layers | A conforming file with an empty directory" — §21.6

The reporter concedes the stakes ("a row with no instance cannot be exceeded on any
reading"). Nothing to repair beyond an optional half-clause.

### 17. s217-compactor-trailer-obligations — reader-02 — PARTIAL, editorial

The count is right: [R-WRT-06] places four obligations on the output trailer (fresh
file_id "a new draw under §9.3's randomness advice", generation 1, ignore-lane carry-
forward, version_minor floor), all four unwitnessed in the output alone, and §21.7 names
two and calls them "§20.5's two obligations on a compacted file's trailer".

The reporter's question — "is a compacted file that reuses its input's file_id
nonconforming?" — is not unanswered. §2.3 answers it in its first sentence:

> "File conformance is a pure predicate on bytes: it does not depend on any reader,
> writer, or environment." — `[R-CNF-02]`

A generation-7 output carrying its input's file_id is byte-indistinguishable from an
ordinary seventh generation of that file, so the file is conforming and the compactor,
having violated a MUST, is a nonconforming writer. That is determinate, and it is the same
answer §2.3's conduct paragraph gives for its two named cases without needing §20.5 to opt
in. What is left is that §21.7 undercounts, and §21.1's carve-out (group 8) means the
undercount is not a register-completeness violation. Byte-level: no.

---

## Summary

Seventeen groups, **zero byte-level**. I am aware that is the shape the calibration warns
against, so: the two candidates were group 3 (the only self-flagged one) and group 2 (the
one with reproduced empirical support). I have stated group 3's downgrade premise
explicitly for attack, and group 2 is downgraded on the flat identity of R3's and R4's
detector, tier, outcome and conformance consequence, which is checkable in one line of the
register.

Groups I tried hardest to kill and failed: **2** (searched §18.2, §17.2, §21.5 and §2.1's
phrasing Note for a reader-side clause or an FCS-tolerant decode licence — none exists,
and the reference decoder falsifies the stated rationale), **6** (searched [R-CNT-21],
[R-MTA-10], §22.3 and §9.7 for any duty to name an unassigned-type extent — none exists),
**9** (constructed the counterexample rather than arguing about it), and **10** (searched
for anything narrowing [R-VEC-04]'s rationale or widening its scope — nothing).

Groups where I found the deciding sentence the reporter did not look for: **1** and **3**
([R-CNF-10] / [R-CNF-03] / [R-RDR-02]), **4** ([R-CNF-02]'s express conduct carve-out),
**5** (§21.2's preamble and §2.3), **8**, **9**, **17** (§21.1's carve-out on §21.7),
**13** (§4.6's "and user-metadata keys"), **14** ([R-WRT-06]'s refusal trigger), **16**
(§21.9's own no-instance sentence).
