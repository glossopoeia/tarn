# Cleanroom round 6 — register

Protocol: ADR-0034. Access rule: `spec/tarn.md` only.

## Walk

ACCESS DISCLOSURE: I read /Users/robertkleffner/Documents/GitHub/tarn/spec/tarn.md in full (3475 lines) and nothing else. No docs/, no conformance/, no registry.json, no git history, no ADRs, no web. Every conclusion below is traceable to a quoted line of that file.

================================================================
PASS 0 — MECHANICAL AUDIT OF THE COUNTS (§21.1's own counting rule)
================================================================

§21.1 fixes the counting rule: "Instances within a cell are separated by semicolons, and a cell reading — is one instance; the count is therefore mechanical."

Row counts, against each subsection's stated total:
  §21.2 claims "39 conditions" — rows F1..F39. 39. OK.
  §21.3 claims "50 conditions" — rows L1..L50. 50. OK.
  §21.4 claims "26 conditions" — rows T1..T26. 26. OK.
  §21.5 claims "10 conditions" — rows R1..R10. 10. OK.
  Total 125, matching §21.8's "125 conditions".

Instance counts, cell by cell, applying the semicolon rule literally:
  §21.2: F1=5, F2=2, F3=5, F4=2, F5=2, F6=1, F7=2, F8=2, F9=1, F10..F30=1 each
    except F22=1 ("flags bits 0-15" is one cell) and F29=1, F31=2, F32=2, F33=2,
    F34=1, F35=1, F36=7, F37=1, F38=1, F39=1  → 61.
  §21.3: L1=6, L2=10, L3=1, L4=1, L5=2, L6=1, L7=1, L8=2, L9=2, L10=2, L11=1,
    L12=1, L13=1, L14=1, L15=3, L16=2, L17=2, L18=2, L19=3, L20=1, L21=1, L22=1,
    L23=3, L24=4, L25=1, L26=1, L27=1, L28=1, L29=1, L30=3, L31=1, L32=3, L33=3,
    L34=4, L35=4, L36=1, L37=2, L38=1, L39=1, L40=3, L41=1, L42=1, L43=1, L44=3,
    L45=1, L46=3, L47=1, L48=1, L49=1, L50=2 → 100.
  §21.4: T1=1, T2=1, T3=6, T4=4, T5=1, T6=1, T7=2, T8=1, T9=1, T10=1, T11=2,
    T12=1, T13=2, T14=1, T15=2, T16=1, T17=1, T18=4, T19=1, T20=1, T21=1, T22=1,
    T23=1, T24=1, T25=3, T26=3 → 45.
  §21.5: R1=6, R2=2, R3=2, R4=10, R5=2, R6=4, R7=6, R8=2, R9=2, R10=2 → 38.

  61 + 100 + 45 + 38 = 244, matching §21.8's "244 named instances" exactly.

The arithmetic of §21.1/§21.8 is sound. §21.1's distinguishability clause ("where a
condition is a single predicate over several fields — a sum against a bound, a
combination of two flag bits — the fields it reads are not instances") is also
honored: F28 (MU=1 with PE=0, a two-bit combination) carries "—" = 1, while F31
(MU *or* PE differs — a disjunction) carries 2. F33 and T7 ("exactly one half
zero"/"exactly one field is the sentinel") carry 2, which is right: two
distinguishable files. F4 and L2 give sums their own instances per container,
which is right under "a container it can occur in."

Detection-point vocabulary: §21.1 says the Detected column names "§19.2's reader
tiers — open, layer access, tile use, extent use — or *certification*". Every
Detected cell in all four tables uses exactly those five tokens. No stray values.

================================================================
PASS 1 — EVERY ROW AGAINST THE RULE IT CITES
================================================================

I read each row's governing rule and asked whether the row's condition is what
that rule forbids. The great majority check out; I list only where they do not,
plus the checks that required real work.

§21.2 against §6.2's `[R-CNT-06]` gate list. `[R-CNT-06]` enumerates: magic; trailer
CRC; version gate; flag gates; committed_file_length equals file size and multiple
of 64; dir_offset ≥ 16; dir_length ≥ 4; dir_offset + dir_length ≤ F − 64;
generation ≥ 1; file_id ≠ 0; reserved bytes zero. Mapping: F10 magic, F16 CRC,
F20/F21 version, F22 flags, F19 size equality, F15 multiple-of-64, F11 dir_offset,
F18 dir_length, F12 sum-vs-F−64, F13 generation, F14 file_id, F17 reserved. Every
gate has a row; no row invents a gate. Clean.

§15.3's entry-state table against §21.4. §15.3 has ten rows; T6 (sentinel with
crc≠0), T7 (half-sentinel), T10 (length 0), T8 (offset<16), T11 (>2⁶³−1), T12
(overflowing sum) and T9 (>F−64), T1 (crc mismatch), L19/F36 (overlap, verifier),
L41/L42/L43 (alignment and slab, verifier). Every §15.3 row maps to at least one
register row and no register row overstates §15.3. Clean.

§17.2 codec 3 against T17–T22: magic (T17), one frame / no skippable (T18),
dictionary ID (T19), content-checksum flag (T20), window size (T21), content size
(T22). Exactly the six header-checkable constraints `[R-COD-06]` states. Clean.

`[R-ENC-12]`'s three name constraints. Non-empty → L6/L8/R6; C0 range → L7/L9/R6;
"at most 255 bytes" → R10 for metadata keys only. That asymmetry is correct and
worth recording as a *sound* judgement: a layer/dimension/channel name cannot
exceed 255 bytes because §4.6 makes the prefix a u8 ("so every name's length prefix
is a single byte") and §7.4 fixes it at "u8 len + bytes" — the state is
unrepresentable, so there is nothing to register. A JSON key is not so bounded,
hence R10. Correct.

Divergences found in pass 1:

(a) L25 vs F38 — range scoping. F38 is carefully written: "A top-level record has a
reserved-range type value (0x0003-0x7FFF, §10.2) with MUST_UNDERSTAND (flags bit 0)
set to 1". Its layer-scope twin L25 is not: "A layer record's sub-record sequence
contains a record of an unassigned type with MUST_UNDERSTAND = 1". §7.3 defines
unassigned as "All other type values are unassigned (registry and experimental
ranges: §10)", so L25 covers the experimental range ≥ 0x8000. But §21.6 says of
exactly that case: "`[R-CNT-15]` obliges the reader to reject, and `[R-CNF-02]`
makes the file conforming all the same ... which is why neither is a register row,
while a *reserved*-range type, whose emission `[R-CNT-15]` does make a violation,
is." §10.3 confirms the two containers are treated alike: "for record types, the
MU-bit outcome of `[R-CNT-15]` at file scope and `[R-CNT-18]` for layer
sub-records". So L25 registers as a layer-scope violation a condition the document
elsewhere declares conforming. Reported as a finding.

(b) F8 / F2 detector cell vs `[R-CNT-04]`. F8's Detector is "reader", unqualified.
`[R-CNT-04]` binds only local readers: "A **local reader** ... MUST verify the full
block by byte equality ... A **remote reader** ... MAY defer or omit this check."
§19.2 gets it right — "at open: the front signature block (local readers,
`[R-CNT-04]`)" — the register does not. Same for F2's first instance (front block
bytes byte-reversed). Reported.

(c) T2 vs `[R-SER-08]`. T2 restricts to "a real (non-padding) sample position".
`[R-SER-08]` does not: "Writers MUST NOT emit any byte other than 0x00 or 0x01 as
an interleaved bool value", and §11.3 makes padding positions serialized "like any
other position". The narrowing is a deliberate de-duplication against T4's
"interleaved bool fill byte" instance, and §21.1's tiebreak ("where a row and the
rule it cites diverge, the rule governs") keeps the padding case a violation. It is
still a row that does not restate its rule. Reported as an observation.

(d) F1's "generation" instance is unbuildable. F1's condition is "A multi-byte
field is stored big-endian ... detectable only through that field's own value or
range gate". For generation the only gate is "generation ≥ 1" (`[R-CNT-06]`) plus
the table's "1 ≤ generation ≤ 2⁶³ − 1". A generation g written big-endian has its
low-order byte at the high end; for any g < 2⁵⁶ the byte-reversed u64 has a zero
top byte, hence a value in [1, 2⁵⁶) — inside every gate. No big-endian generation
is detectable by any actor this document defines. Yet `[R-ERR-02]` demands "a row
naming instances has one vector per instance", and `[R-VEC-02]` says "A vector
whose expectation cannot be stated in those terms is testing something this
specification has not defined". Reported.

================================================================
PASS 2 — VIOLATIONS THE DOCUMENT NAMES AND THE REGISTER OMITS
================================================================

I walked §4 through §24 for every MUST / MUST NOT that names a detectable
malformed state, and checked it against the 125 rows.

Fully covered (spot list, not exhaustive): `[R-ENC-01..06]`, `[R-ENC-11..15]`,
`[R-CNT-01]`, `[R-CNT-04..08]`, `[R-CNT-11..18]`, `[R-CNT-22..23]`, `[R-CNT-25]`,
`[R-CNT-27]`, `[R-GEO-01]`, `[R-GEO-03]`, `[R-GEO-05]`, `[R-TYP-03]`, `[R-TYP-06]`
(length), `[R-TYP-07]`, `[R-SER-05..08]`, `[R-IDX-03..05]`, `[R-SLB-01..03]`,
`[R-COD-02..10]`, `[R-MTA-03..05]`, `[R-MTA-09]`, `[R-CNF-05]` derivatives.

Omissions correctly and *explicitly* justified in the text (these are not defects):
  - sub-record nesting beyond two (§7.4 Note: "in format major 1 it has no
    reader-detectable witness, and so no register row");
  - a stale slab declaration (§16.2 Note: "Because this rule's detection *is*
    `[R-SLB-03]`'s, a stale declaration carries no register row of its own");
  - residue past a completed commit (§9.5 Note: "A reader meets it as a trailer
    that fails its gates ... each of which §21.2 already registers");
  - "belongs to no coverage class" (§5.2 Note: "a register row for it would be a
    row no file could exhibit").
This is unusually disciplined and I want it on the record: the document reasons
about its own omissions.

Omissions I judge to be real:

(A) `[R-MTA-07]` — §18.4: "A writer MUST NOT emit a standardized key outside the
scopes its row lists". This is a bytes-binding MUST NOT: the key is in the file. It
is not exempted as conduct — `[R-CNF-02]` names only "§10.3, §18.3" as conduct
rules, and `[R-MTA-07]` lives in §18.4. It is detectable: any reader that parses
the document to ignore the key can see it, and a verifier certainly can. A file
carrying `tarn.created` on a layer, or `tarn.axes` at file scope, is therefore a
nonconforming file with a named violation — and no register row exists in §21.2,
§21.3, §21.5, nor a defined-behavior row in §21.6. Under §21.1 ("a violation this
specification names and the register omits is a defect in this document") that is a
defect by the register's own standard.
  It is worse than a missing row. §18.4 fixes the reader's treatment as "a reader
that finds one malformed MUST ignore that key rather than the document", and §2.4
defines exactly four outcomes — reject-file, reject-layer, reject-tile,
ignore-record. "Ignore the key" is none of them, and `[R-MTA-07]` explicitly
forbids the nearest one. So `[R-CNF-07]`'s "Every detectable violation named by
this specification is assigned exactly one reader outcome" cannot be satisfied for
this violation. The natural repair is an ignore-record row with detector
*verifier*, on the F30/`[R-MTA-05]` precedent, where readers likewise proceed
unchanged.

(B) generation above 2⁶³ − 1. §6.2's layout table gives generation the valid range
"1 ≤ generation ≤ 2⁶³ − 1 (`[R-ENC-03]`)". `[R-ENC-03]` says "a reader MUST treat a
value above 2⁶³ − 1 in any such field as a validity error at the owning scope".
`[R-CNT-06]`'s gate list, however, states only "generation ≥ 1", and the register
covers only generation = 0 (F13) and generation byte-swapped (F1). F3's condition
is scoped to "A u64 offset or length field" — generation is neither. So the
upper-bound violation has no row. Whether it is even a violation turns on whether
generation counts as a "count" under `[R-ENC-03]`'s "every offset, length, extent,
and count"; §6.2's own table asserts it does by citing the requirement. Reported as
a joint omission/ambiguity.

(C) `[R-CNT-13]`'s prohibition on MU = 0 records encoding offsets — "neither its
inline payload nor its extent contents encode offsets or lengths of other file
bytes" — is a MUST-class writer constraint with no register row and no mention in
§21.7's list of undetectable classes ("a mis-strided filter, an undisclosed
compression dictionary, or simply wrong data"). Same for `[R-GEO-06]`'s entry
ordering and `[R-SER-01]`'s value-sequence order: a writer that misorders produces
a file every checksum certifies. These belong either in a row or in §21.7's
enumeration; §21.7 is the register's stated escape hatch and it is under-populated.
Lower severity than (A) — folded into the completeness finding below.

================================================================
PASS 3 — §21.1's COUNTING RULE, AND §21.6 AGAINST §21.2–§21.5
================================================================

Counting rule: verified above, 125/244 exact. One caveat on the claim "the count
is therefore mechanical": the count is mechanical *given the cells*, but the
granularity of the cells is authorial and demonstrably inconsistent. The same zstd
constraint set is enumerated four ways at tile scope (T18: "a second concatenated
compressed frame; a skippable frame before the frame; a skippable frame after the
frame; a skippable frame between two frames") and two ways at metadata scope (R4:
"a skippable frame, top-level extent; a skippable frame, layer sub-record extent"),
though `[R-MTA-9]` carries over the identical constraint. T24 collapses to "any
codec" (1 instance) where T15/T25 enumerate per codec. So 244 is reproducible but
not derivable from the rules.

§21.6 versus the violation tables. Eleven of the twelve §21.6 rows are disjoint
from §21.2–§21.5 and several are explicitly disambiguated against them (the
compressing-codec row against T14: "codec 1's equality is `[R-COD-04]`'s subject").
One row is not disjoint:

  §21.6: "| An unknown record type carries MU = 0 | Ignored, and preserved or
  dropped per its PE bit | `[R-CNT-15]`, `[R-WRT-08]` |", under the preamble
  "These are defined behaviors, not errors."
  F39: "A top-level record carries a type value from the reserved range
  0x0003-0x7FFF, which this specification has not assigned; emitting one is a
  violation whatever its MU bit | — | verifier | certification | `[R-CNT-15]`"
  (L26 is the identical row at layer scope.)

A top-level record of type 0x0003 with MU = 0, PE = 1 satisfies both. §21.6 says it
is not an error; F39 says it is a violation "whatever its MU bit". Appendix H takes
§21.6's side against the register: "no violation row of §21.2–§21.5 applies, though
§21.6's defined conditions can — an unknown MU = 0 record being conforming
(`[R-CNT-15]`)". The document knows the distinction — its own closing paragraph in
§21.6 makes it for the MU = 1 case ("while a *reserved*-range type, whose emission
`[R-CNT-15]` does make a violation, is") — but the table row was never qualified.

Second structural problem found in this pass, cutting across all four tables: each
subsection preamble assigns one outcome to every row it contains, and §2.4 defines
those outcomes as reader obligations. Twelve rows contradict their own preamble.
§21.2 says "Outcome: reject-file" and §2.4 says reject-file means "A reader MUST NOT
rely on any structure in it" — yet F30 reads "the document stays readable and
readers process it unchanged" and `[R-MTA-05]` says "readers process the document
unchanged". §21.3 says "the named layer is unusable" — yet L50 reads "readers apply
the type's fixed semantics regardless". §21.4 says "that tile's read reports
failure" — yet T4/T5's rule `[R-SER-05]` says "A conforming reader never returns
this content ... and is not obligated to check it", and T2's rule `[R-SER-08]` says
"A reader that neither detects the violation nor rejects the tile, and returns the
value, MUST report 0x00 as false and every other byte as true". For these rows the
outcome is a *verifier's certification scope*, not a reader outcome, and the
preambles say otherwise. §21.1's tiebreak resolves it in the rules' favor, but an
implementer reading the table headings first — which is what a register is for —
gets the wrong answer, and for F30 gets an answer that would make a compliant
reader reject a file `[R-MTA-05]` obliges it to read.

Third: R1's instance list mixes classes. "encoding 0" is invalid by `[R-CNT-25]`
("u8: 0 invalid"); "reserved 3–0x7F" is a violation by `[R-EXT-03]` ("a value from
a reserved range MUST NOT be emitted at all"); but "experimental ≥ 0x80" is
governed only by §10.3's conduct prohibition, which `[R-CNF-02]` explicitly names
("§10.3, §18.3") as binding "their *conduct* rather than their output". §18.2
supplies no unconditional writer prohibition for the metadata-encoding space — unlike
§11.4, §12.2, §14.1, §17.2, §17.3, each of which does ("writers MUST NOT emit any
other value"). So a file with metadata encoding 0x80 is conforming and its record is
ignored for reader-capability reasons, which is precisely the class §21.6 keeps out
of the register. R1 puts it in.

Cross-cutting observations recorded but not treated as defects: overlapping rows
(F2 ⊂ F8, F2 ⊂ F10, F38 ⊂ F39, L25 ⊂ L26 for MU=1 reserved types) mean one file
exercises two rows, while `[R-VEC-02]` records "the §21 register row it exercises"
in the singular; F32 lacks the "trailing residue" instance its twin L15 carries,
though `[R-CNT-12]`'s no-residue rule binds both sequences; F36 lists "front
signature block" and "trailer" as overlap participants, neither of which can be
overlapped without independently tripping F34/L17/T8 (offset < 16) or F35/L18/T9
(past F − 64).

One contradiction outside the register that determines what the register may
contain: §9.6 says "Generation enumeration for coverage verification (§5.2) is the
same probe continued to offset 0", while §9.7 says "A verifier checking
`[R-CNT-02]`'s partition walks the live state only" and its Note says "Nothing here
enumerates prior commits." If §9.6 governs, `[R-LIF-03]`'s "increasing by exactly 1
per commit" and `[R-LIF-04]`'s truncation obligation become verifier-detectable and
must be registered; if §9.7 governs, they cannot be and the register is right to
omit them. As written the document says both.

Finally, §21.1's completeness sentence is stronger than the document can support:
"a violation this specification names and the register omits is a defect in this
document", with no detectability qualifier — while §2.4 has one ("Every *detectable*
violation named by this specification is assigned exactly one reader outcome"),
§21.7 catalogues named violations that no check detects, and three separate Notes
justify omitting rows precisely on detectability grounds. Read literally, §21.1
convicts the document of defects it deliberately and correctly incurred.

================================================================
WHAT I DID NOT FIND
================================================================
No row cites a requirement identifier that does not exist. `[R-SER-04]` is cited
nowhere in the register, consistent with §14.4's withdrawal note. No row assigns an
outcome its governing rule contradicts on scope (I checked every reject-layer row
whose damage looks tile-sized: L38/L39 take layer scope because `[R-IDX-04]` says
so, and §19.2 anticipates the surprise). No §21.6 row lacks a rule citation. No
detection point precedes the tier at which the resident bytes exist.

## Findings

### CONTRADICTION — §21.6 row "An unknown record type carries MU = 0" vs §21.2 row F39 and §21.3 row L26; Appendix H "Conforming file"

Byte-level: True

The same file — a top-level record of a reserved type (say 0x0003) with MU = 0, PE = 1 — is classified both ways. §21.6's preamble: "These are defined behaviors, not errors. A reader that treats any of them as a failure is the nonconforming party." Its row: "| An unknown record type carries MU = 0 | Ignored, and preserved or dropped per its PE bit | [R-CNT-15], [R-WRT-08] |". F39 says the opposite: "A top-level record carries a type value from the reserved range 0x0003-0x7FFF, which this specification has not assigned; emitting one is a violation whatever its MU bit | — | verifier | certification | [R-CNT-15]". L26 repeats F39 at layer scope. Appendix H sides with §21.6 against the register: "no violation row of §21.2–§21.5 applies, though §21.6's defined conditions can — an unknown MU = 0 record being conforming ([R-CNT-15])". §21.6's own closing paragraphs draw the reserved/experimental distinction correctly for the MU = 1 case ("while a *reserved*-range type, whose emission [R-CNT-15] does make a violation, is"), so the fix is plainly to qualify the table row to the experimental range. As written, a verifier cannot decide whether to certify the file, and Appendix H's conformance checklist gives an answer F39 forbids.

**Readings.** n/a (contradiction, not ambiguity)

### CONTRADICTION — §21.3 row L25 vs §21.6 closing paragraph, §7.2 [R-CNT-15], §2.3 [R-CNF-02], §10.3 [R-EXT-03]

Byte-level: True

L25 reads "A layer record's sub-record sequence contains a record of an unassigned type with MUST_UNDERSTAND = 1" and registers it as a layer-scope violation. §7.3 defines unassigned as "All other type values are unassigned (registry and experimental ranges: §10)", so L25 covers experimental types ≥ 0x8000. But §21.6 says of that exact condition: "an **experimental-range record type carrying MU = 1** (§10.2, §10.3): [R-CNT-15] obliges the reader to reject, and [R-CNF-02] makes the file conforming all the same, since the prohibition on publishing experimental values binds a writer's conduct and not the bytes ... which is why neither is a register row". §10.3 treats the two containers identically: "for record types, the MU-bit outcome of [R-CNT-15] at file scope and [R-CNT-18] for layer sub-records". The file-scope twin F38 is correctly narrowed — "a reserved-range type value (0x0003-0x7FFF, §10.2) with MUST_UNDERSTAND (flags bit 0) set to 1" — and L25 is not. Consequence: a verifier handed a conforming file with an experimental MU = 1 sub-record must refuse to certify under L25 and must certify under [R-CNF-02].

**Readings.** n/a (contradiction, not ambiguity)

### OBSERVATION — §18.4 [R-MTA-07]; absent from §21.2–§21.6; §2.4 [R-CNF-07]

Byte-level: True

REGISTER OMISSION. [R-MTA-07]: "A writer MUST NOT emit a standardized key outside the scopes its row lists, and a reader MUST ignore a standardized key found outside its listed scope, or whose value does not match the shape its row gives, rather than rejecting the document." This is a bytes-binding MUST NOT — the key is in the file — and it is not exempted as conduct: [R-CNF-02] names only "(§10.3, §18.3)" as conduct rules, and [R-MTA-07] is in §18.4. It is detectable by any reader that parses the document in order to ignore the key, and certainly by a verifier. A file carrying `tarn.created` on a layer is therefore nonconforming with a named violation, and no row of §21.2, §21.3 or §21.5 covers it, nor does §21.6 record it as defined behavior. Under §21.1 ("a violation this specification names and the register omits is a defect in this document") that is a defect by the register's own standard. It also breaks [R-CNF-07]: "Every detectable violation named by this specification is assigned exactly one reader outcome" — the four outcomes are reject-file/reject-layer/reject-tile/ignore-record, and §18.4's defined treatment is "a reader that finds one malformed MUST ignore that key rather than the document", which is none of them and explicitly excludes the nearest. Repair: an ignore-record row with detector *verifier*, on the F30/[R-MTA-05] precedent where reader behavior is likewise unchanged. Costly to decide only in the sense that it forces a decision about whether §18.4's value-shape mismatch (as opposed to scope) is also a writer violation — the MUST NOT covers scope only, while the reader-side clause covers both.

**Readings.** n/a

### CONTRADICTION — §21.2, §21.3, §21.4 subsection preambles vs §2.4's outcome table and rows F28–F31, L47–L50, T2, T4, T5, T26

Byte-level: True

Each table's preamble assigns one outcome to every row it contains, and §2.4 defines those outcomes as reader obligations. Twelve rows contradict their own heading. §21.2: "Outcome: reject-file." §2.4: "**reject-file** | The file is not usable; failure is reported for the whole file. A reader MUST NOT rely on any structure in it." F30's own condition text: "...the document stays readable and readers process it unchanged", and [R-MTA-05]: "unsorted members do not make a document unreadable: the file is nonconforming, a verifier MUST report it, and readers process the document unchanged." §21.3: "Outcome: reject-layer — the named layer is unusable, every other layer unaffected" versus L50: "readers apply the type's fixed semantics regardless". §21.4: "Outcome: reject-tile — that tile's read reports failure" versus [R-SER-05] for T4/T5: "A conforming reader never returns this content ([R-GEO-04]) and is not obligated to check it", and [R-SER-08] for T2: "A reader that neither detects the violation nor rejects the tile, and returns the value, MUST report 0x00 as false and every other byte as true." For these rows the cell means "the scope at which a verifier records the damage", not a reader outcome. §21.1's tiebreak ("where a row and the rule it cites diverge, the rule governs") resolves it, but the table heading is what an implementer reads first, and for F30 it directs a reader to reject a file [R-MTA-05] obliges it to read.

**Readings.** n/a (contradiction, not ambiguity)

### AMBIGUITY — §21.1 completeness sentence vs §2.4 [R-CNF-07], §21.7 [R-ERR-01], §7.4 Note, §16.2 Note, §5.2 Note, §9.5 Note

Byte-level: False

§21.1: "Its **completeness is normative** — a violation this specification names and the register omits is a defect in this document". The sentence carries no detectability qualifier, while §2.4 does — "Every *detectable* violation named by this specification is assigned exactly one reader outcome" — and §21.7 catalogues named violations no check detects ("a mis-strided filter ([R-COD-10]), an undisclosed compression dictionary ([R-COD-06]), or simply wrong data — produces a file that every checksum in §8 certifies"). Four Notes justify omitting rows precisely on detectability grounds (§7.4: "in format major 1 it has no reader-detectable witness, and so no register row"; §16.2; §5.2; §9.5).

**Readings.** Reading 1 (literal): every named violation needs a row, so [R-LIF-01] (modifying a committed byte), [R-LIF-03] (generation increment), [R-GEO-06] (entry ordering), [R-SER-01] (value-sequence order), [R-CNT-13]'s no-embedded-offsets rule for MU = 0 records, and every §21.7 case are all defects in this document. Reading 2 (qualified by §2.4): only *detectable* named violations need rows, and the omissions above are correct. I picked Reading 2 — §2.4 supplies the qualifier, the four Notes act on it, and Reading 1 would convict the document of defects it deliberately and correctly incurred. The sentence should carry the word "detectable", and §21.7 should enumerate the omitted-by-undetectability set (it currently names three of at least six).

### OBSERVATION — §21.2 row F1, instance "generation"; §6.2 [R-CNT-06]; §21.8 [R-ERR-02]; §24 [R-VEC-02]

Byte-level: False

F1's condition is "A multi-byte field is stored big-endian rather than little-endian, detectable only through that field's own value or range gate", and its instances include generation. No big-endian generation is detectable. The only gates are [R-CNT-06]'s "generation ≥ 1" and §6.2's table range "1 ≤ generation ≤ 2⁶³ − 1". Byte-reversing any g < 2⁵⁶ puts a zero in the top byte, yielding a value in [1, 2⁵⁶) — inside every gate — and §9.7 forbids the verifier to reconstruct history that would expose the wrong number ("Nothing here enumerates prior commits"). So this instance names a condition no actor can detect and no vector can carry an expected verdict for, while [R-ERR-02] requires "a row naming instances has one vector per instance" and [R-VEC-02] says "A vector whose expectation cannot be stated in those terms is testing something this specification has not defined, which makes it a finding against this document rather than a vector." The other four F1 instances (version_major, dir_offset, dir_length, committed_file_length) are all detectable; only generation is not.

**Readings.** n/a

### OBSERVATION — §6.2 trailer layout table (generation row) + §4.2 [R-ENC-03]; §21.2 rows F3 and F13

Byte-level: True

REGISTER OMISSION. §6.2's table gives generation the range "1 ≤ generation ≤ 2⁶³ − 1 ([R-ENC-03])", and [R-ENC-03] says "a reader MUST treat a value above 2⁶³ − 1 in any such field as a validity error at the owning scope". The register covers generation = 0 (F13) and byte-swapped generation (F1), but not generation > 2⁶³ − 1: F3's condition is scoped to "A u64 offset or length field", which generation is not, and [R-CNT-06]'s reader gate list stops at "generation ≥ 1". Whether the violation exists at all turns on whether generation is a "count" within [R-ENC-03]'s "every offset, length, extent, and count"; §6.2's table asserts it is by citing the requirement, and §21.9's hard-limits paragraph repeats "every offset, length, extent, and count at most 2⁶³ − 1 ([R-ENC-03])" without mentioning generation either way. Either add the instance to F3 (widening its condition beyond "offset or length") or state in §6.2 that generation's upper bound is enforced only through [R-ENC-03].

**Readings.** Reading A: generation is a count, the upper bound is enforced, and the register omits a reader-detected file-scope violation. Reading B: generation is neither offset, length, extent nor count, [R-ENC-03] does not reach it, the table's citation is decorative, and any nonzero u64 is a valid generation. I picked Reading A — the table's explicit range plus its explicit citation is the strongest signal, and Reading B makes the table's stated upper bound unenforceable text.

### OBSERVATION — §21.5 row R1 instances "experimental ≥ 0x80, top-level record; experimental ≥ 0x80, layer sub-record"; §10.3 [R-EXT-03]; §2.3 [R-CNF-02]; §18.2 [R-MTA-03]; §21.6

Byte-level: True

R1 registers three classes as one violation: encoding 0 (invalid per [R-CNT-25]'s "u8: 0 invalid"), reserved 3–0x7F (a violation per [R-EXT-03]: "a value from a reserved range MUST NOT be emitted at all before this specification assigns it"), and experimental ≥ 0x80. The third is not a violation. §18.2 supplies no unconditional writer prohibition for the metadata-encoding space — unlike §11.4, §12.2, §14.1, §17.2 and §17.3, each of which says writers MUST NOT emit any other value — so the only prohibition reaching it is §10.3's "Writers MUST NOT emit files carrying an experimental value in released software or published data", which [R-CNF-02] classifies as binding "their *conduct* rather than their output ... (§10.3, §18.3)". The file is conforming and the record is ignored for reader-capability reasons ([R-MTA-03]: "An encoding this specification does not assign, or one the reader does not implement, is ignore-record") — exactly the class §21.6 keeps out of the register for record types. Either these two instances belong in §21.6, or §21.6's record-type exclusion is wrong; the document cannot have it both ways.

**Readings.** n/a

### CONTRADICTION — §9.6 [R-LIF-06] vs §9.7 [R-LIF-08] and its Note

Byte-level: True

§9.6: "Generation enumeration for coverage verification (§5.2) is the same probe continued to offset 0." §9.7: "A verifier checking [R-CNT-02]'s partition walks the live state only. From the live trailer it enumerates the live directory and its records ... Bytes the walk does not reach are slack", and its Note: "Nothing here enumerates prior commits. A verifier certifies what a reader can reach and counts what it cannot." One requirement makes backward generation enumeration part of coverage verification; the other says coverage verification does not do it. This is a register question, not only a lifecycle one: if §9.6 governs, [R-LIF-03]'s "increasing by exactly 1 per commit" and [R-LIF-04]'s "after any commit completes, the physical file length equals committed_file_length" become verifier-detectable and require rows, and §9.5's Note ("Residue past a completed commit carries no register row of its own") loses its premise. If §9.7 governs, the register is right to omit them and §9.6's sentence should be struck or relabeled as recovery-tool guidance only.

**Readings.** n/a (contradiction, not ambiguity)

### AMBIGUITY — §7.1 [R-CNT-25] internal; §18.2 [R-MTA-03]; §21.2 rows F24–F26; §21.3 rows L11–L13

Byte-level: True

[R-CNT-25] says both that specific user-metadata framing failures take the containing scope — "an extent of (0, 0) on a user-metadata record, or one whose extent_length is less than 5 ... is a validity error at its containing scope" — and that "*every* way a user-metadata record's document can be unreadable ... is ignore-record with a SHOULD-report, notwithstanding the owning-scope mapping of [R-CNF-08]". With extent (0,0), extent_length 4, or inline_length 2, the document is unreadable, so the second sentence read literally gives ignore-record while the first (and [R-MTA-03] for inline_length: "A record whose inline_length is not 1 is a validity error at the record's containing scope") gives reject-file/reject-layer. The register picks the containing-scope reading (F24, F25, F26; L11, L12, L13).

**Readings.** Reading 1 (literal "every way"): all three are ignore-record, and F24–F26 / L11–L13 are six wrongly-placed rows. Reading 2 (the em-dash list is exhaustive): "every way" is qualified by its own enumeration — "a failed extent CRC, an unimplemented or invalid encoding, a decode failure, or content violating the document's own rules" — none of which is a framing failure, and [R-MTA-02] supplies the principle: "a malformed extent slot on such a record, (0, 0) included, is a validity error at the record's containing scope ..., because that failure precedes the document." I picked Reading 2, matching the register. The word "every" should be dropped or the enumeration marked exhaustive; note that [R-MTA-02] states the precedes-the-document principle for extent slots only, and inline_length ≠ 1 is left to rest on [R-MTA-03] alone.

### OBSERVATION — §21.2 row F8 and F2 (Detector column) vs §6.1 [R-CNT-04] and §19.2

Byte-level: False

F8's Detector cell reads "reader" without qualification, as does F2's for its "front signature block bytes [0,8)" instance. [R-CNT-04] binds only local readers: "A **local reader** — one whose transport serves any byte range at no per-range round trip ... MUST verify the full block by byte equality before other processing and MUST treat any mismatch as reject-file. A **remote reader** ... MAY defer or omit this check". §19.2 states the qualifier correctly — "at open: the front signature block (local readers, [R-CNT-04])" — and §19.1 step 1 repeats it. §21.1 defines the Detector column as "the actor obliged to detect it", so F8 as written obliges an actor [R-CNT-04] exempts. A conformance vector for F8 whose expected verdict is reject-file would fail a conforming remote reader.

**Readings.** n/a

### OBSERVATION — §21.4 row T2 vs §14.2 [R-SER-08]

Byte-level: False

T2 narrows its rule: "In an interleaved tile, a bool channel's single value byte at a real (non-padding) sample position is neither 0x00 nor 0x01". [R-SER-08] carries no such restriction — "Writers MUST NOT emit any byte other than 0x00 or 0x01 as an interleaved bool value" — and §11.3 makes padding positions "serialized like any other position". The narrowing is a sound de-duplication against T4's "interleaved bool fill byte" instance ([R-SER-05] requires the fill byte there, and [R-TYP-07] constrains the fill byte to 0x00/0x01), and §21.1's tiebreak keeps the padding case a violation via the rule. Recorded because §21.1 claims each row restates its governing rule, and this one restates a proper subset.

**Readings.** n/a

### OBSERVATION — §21.1 ("the count is therefore mechanical"); §21.4 rows T18, T24, T3, T15, T25; §21.5 row R4

Byte-level: False

The instance count is reproducible from the cells but the cells' granularity is authorial and inconsistent, so 244 is not derivable from the requirements. The same zstd frame-constraint set is enumerated four ways at tile scope — T18: "a second concatenated compressed frame; a skippable frame before the frame; a skippable frame after the frame; a skippable frame between two frames" — and once at metadata scope, R4: "a skippable frame, top-level extent; a skippable frame, layer sub-record extent", though [R-MTA-09] carries the identical constraint over ("no skippable frame and no second frame"). T24 collapses to "any codec" (1 instance) where T15 and T25 enumerate per codec. T3 crosses two alternatives with three layouts (6) where L45 leaves the same layout axis unenumerated. Under [R-ERR-02] ("a row naming instances has one vector per instance") this decides how many files the corpus must contain, so the inconsistency has a cost; §21.1 should either fix the enumeration axes or drop the claim that the count is mechanical.

**Readings.** n/a

### OBSERVATION — §21.2 row F32 vs §21.3 row L15; §7.2 [R-CNT-12]

Byte-level: False

[R-CNT-12] binds both record sequences identically: "The sequence MUST parse as zero or more complete records with no residue." L15 enumerates three instances — "sub-record header; sub-record inline_length; trailing residue" — while its file-scope twin F32 enumerates two, "record header; inline_length", with no residue instance. A directory whose record sequence ends with, say, 10 stray bytes is arguably reachable through F32's "record header" instance (a 24-byte header starting there would extend past the end), but the register elsewhere pairs file- and layer-scope twins instance-for-instance (F33/L16, F34/L17, F35/L18, F28/L47, F29/L48, F30/L49, F31/L50), and this pair breaks the pattern silently.

**Readings.** n/a

### OBSERVATION — §21.2 rows F2/F8/F10 and F38/F39; §21.3 rows L25/L26; §24 [R-VEC-02]

Byte-level: False

Several rows are strict specializations of others, so one file exercises two rows. F2's instance "front signature block bytes [0,8)" is a special case of F8 ("not byte-identical to the constant"); F2's "trailer magic at F-64" is a special case of F10. F38 (reserved-range type with MU = 1) is a subset of F39 (reserved-range type "whatever its MU bit"); L25 ⊃ L26's MU = 1 case likewise. [R-VEC-02] requires each vector to record "the §21 register row it exercises" in the singular, and [R-ERR-02] requires "at least one conformance vector ... whose expected verdict is that row's outcome" per row — but F38's verdict is reject-file at open by a reader while F39's is a verifier's refusal at certification, for the same bytes. The register should say which row such a file is recorded against, or §24 should permit a vector to cite several.

**Readings.** n/a

### OBSERVATION — §21.2 row F36 instances "trailer" and "front signature block"

Byte-level: False

F36's instance list ends "...; directory region; trailer; front signature block". Neither of the last two can participate in an overlap without the offending structure independently tripping a reader-detected row: any live-state extent overlapping [0, 16) has offset < 16 (F34, L17, T8), and any extent overlapping the final 64 bytes has offset + length > F − 64 (F35, L18, T9). Both instances are therefore buildable only as files that simultaneously exercise a different row with a different detector and detection point, which weakens what a vector at those two instances can demonstrate about verifier-only overlap detection.

**Readings.** n/a

### OBSERVATION — Document header (lines 3–7) and §5.2's second Note

Byte-level: False

Unresolvable references out of the document, against §1's claim that TARN is "implementable from this document alone". The header: "Decisions encoded here are governed by the ADRs in [docs/decisions/](../docs/decisions/README.md)" — a governance claim placing authority outside the text. §5.2's Note reasons about a normative choice by citing a record I am not permitted to read and which is not part of the specification: "a register row for it would be a row no file could exhibit (ADR-0056 deleted one)". §10.4 handles the analogous case correctly for the registry — "Where the registry, §10.2's table, and Appendix C diverge, the section that defines the space governs — the registry is machine-readable convenience, never a second authority" — and the same disclaimer is missing for the ADRs. The §5.2 citation is inside a Note and so non-normative under [R-CNF-01], but it is the only justification offered for an absent register row, which §21.1 makes a normative matter.

**Readings.** n/a


## Verdict
The register is in better shape than I expected: 125 rows and 244 instances count out exactly as §21.1's rule prescribes and as §21.8 claims, every gate in [R-CNT-06] and every row of §15.3's entry-state table has a corresponding row, the detection-point vocabulary is used without a single stray token, and four separate Notes reason explicitly about rows the document deliberately does not carry. Pass 1 found no row citing a nonexistent requirement and no row whose outcome contradicts its rule's scope. But the register is not complete or self-consistent as §21.1 asserts. One violation is genuinely missing: [R-MTA-07]'s prohibition on a standardized metadata key outside its listed scope is a bytes-binding MUST NOT, is detectable, is unregistered, and — worse — its defined reader treatment ("ignore that key rather than the document") is not one of §2.4's four outcome classes, so [R-CNF-07] cannot assign it one. A second is probably missing (generation above 2^63-1, which §6.2's table forbids by citing [R-ENC-03] and no row covers). Two rows are scoped too widely and register conforming files as violations: L25 covers experimental sub-record types that §21.6 and [R-CNF-02] declare conforming, where its file-scope twin F38 is correctly narrowed to the reserved range; R1 does the same for experimental metadata encodings. Pass 3 found the §21.6 collision the role anticipated — the "unknown record type carries MU = 0" row classifies as defined behavior exactly what F39 and L26 classify as a violation, with Appendix H siding against the register — and one systemic problem the role did not: the four table preambles assign reader outcomes, defined by §2.4 as reader obligations, to twelve verifier-only rows whose own rules state that reader behavior is unchanged, so §21.2's heading tells a reader to reject a file [R-MTA-05] obliges it to read. Finally, §21.1's completeness sentence lacks the word "detectable" that §2.4 has and that §21.7 and three Notes depend on; read literally it convicts the document of omissions it correctly made. Seven of the eighteen findings change what a conforming implementation accepts or certifies.