# Round 23 triage — correctness lens — working transcript

## What I read

- `/Users/robertkleffner/Documents/GitHub/tarn/spec/tarn.md`, in full for the
  sections at issue: §2 (94–279), §4.6–4.7 (473–550), §5 (553–690), §6 (691–865),
  §7.1–7.4 (866–1014), §8 (1111–1153), §9.1–9.5 (1154–1275), §10 (1370–1458),
  §17.2–17.4 (2246–2414), §18 (2415–2671), §19 (2676–2891), §20 (2892–3314),
  §21 in full (3315–3778), §22.3 (3820–3856), §24 (3954–4036), Appendix F
  (4200–4214).
- No `transcript-*.md` opened. I did `ls` the round23 directory once (before
  reading the prohibition carefully); the listing showed nine filenames plus
  `calc.py`/`count.py` and **no** `transcript-triage-*` file was present in it.
  I opened none of them. Disclosed.
- No `docs/`, `PLAN.md`, `AGENTS.md`, `conformance/`, `registry.json`, git
  history, or web.

## Tools I ran

1. **Instance counter** over §21.2–§21.5 rows (semicolon split; `—` = 1):
   F 58 / L 116 / T 55 / R 48 = **277** over 36+49+26+10 = **121**.
   §21.8's stated figure is exactly right. Also confirms register-01's
   arithmetic (R8 at 4 would give 279) and refutes its sub-claim that R8 is the
   only §21.5 row that does not multiply — R2, R3, R9, R10 are all 1×2 = 2.
2. **zstd reference decoder probe** for reader-03 / adversary-01. Hand-built
   two 35-byte frames `28 b5 2f fd | c0 | 00 | <FCS,u64le> | 91 00 00 | <18
   bytes>` carrying `{"tarn.title":"x"}`, FCS = 18 and FCS = 512 MiB.
   - FCS = 18 → decodes, rc 0.
   - FCS = 512 MiB → `liar.zst : Decoding error (36) : Data corruption
     detected`, rc 1.
   So §18.2's "the bytes decode" is **false for the reference decoder**. The
   reporters' suspicion is confirmed empirically, not just argued.

## The quotation that governs three of the §21.7 findings

§21.1, lines 3343–3347:

> The subsections after §21.5 are not part of the register and carry no rows:
> neither this completeness clause nor the instance arithmetic below reaches
> §21.6's defined non-violations, §21.7's account of what no check detects, or
> §21.9's limits.

So an **omission** from §21.7's enumeration is not a breach of the register's
normative completeness. A **false positive claim** in §21.7 (adversary-03) is
still a defect, because it is normative text that is untrue; an omission
(diagrams-01, reader-02) is weaker than the reporters present it.

## Group-by-group

### G1 no-stored-length-bound (reader-01 + adversary-04)
Same defect: §21.9 states no guarantee for any *stored* (on-disk) quantity, and
composes no rows, while §19.4 step 5 and [R-CNT-20] oblige a whole-extent fetch
and CRC before decode. Verified: §21.9's table has 8 rows, none over a stored
length; [R-ERR-05]'s hard limits stop at 2⁶³−1. §17.2's "Resource limits are
§21's subject" is inside a **Note** (non-normative), which reader-01 states
correctly. §18.2 does floor the decoded-size and window bounds at §21.9 rows and
says nothing about the extent's stored length while treating that length as
reportable ("the stored length of the extent it declined") — accurate.
Downgrade quote (§21.9, [R-ERR-04]):
> Software that declines **on that ground** a file whose every quantity lies
> within the table is not a conforming reader (`[R-CNF-03]`)
Only quantities the table names can "lie within the table", so a file with a
multi-gigabyte stored extent has every such quantity within it and a
resource-grounded decline makes the software nonconforming. That is
determinate — reader-01 says so itself for the tile half. The metadata half's
second reading only moves whether a quarantined record's content is surfaced,
and [R-MTA-02] forbids any part of a document from affecting how a byte is
located, decoded or returned. Premise of the downgrade, stated for attack: an
implementation's *inability* to meet a determinate duty is not an ambiguity
about bytes. Severity design-decision.

### G2 compactor-trailer-obligations (reader-02)
[R-WRT-06] carries four trailer obligations (fresh file_id; generation 1;
ignore-lane carry-forward; version_minor floor). §21.7 names two and §20.5's own
"Neither obligation has a witness in the output alone" names the same two.
§2.3's conduct bucket names only §6.3's flags = 0 and §6.2's long pre-trailer
gap, and §20.5 never opts in. So the accusation is factually right. But per
§21.1's 3343–3347 the completeness clause does not reach §21.7, so this is an
incomplete account rather than a normative gap. Nothing checkable from one file
under either classification. Editorial.

### G3 content-size-comparand (reader-03 + adversary-01)
Same sentence, same defect from two angles. Verified reader-03's asymmetry:
[R-COD-06] for a tile compares FCS against a size "the layer's declarations
alone" give — genuinely header-checkable — while §18.2 pins the document field
to "the byte length of the decoded document", obtainable only by decoding. And
the reference decoder refuses the frame (probe above), so "the bytes decode" is
not safe. CONFIRMED.
What is overstated: adversary-01's forked-verdict consequence. Reading B (a
pre-decode decline on the declared size) is foreclosed — the actual document is
18 bytes, so no §21.9 row is exceeded, and [R-ERR-04]'s sentence quoted in G1
makes such a decline nonconformance. Reading C's R3-instead-of-R4 costs nothing
operative: R3 and R4 share detector (reader), tier (extent use), outcome
(ignore-record), and the file is nonconforming under both, the mismatch being a
MUST:
> when present it MUST equal the byte length of the decoded document
and §2.3: "File conformance is a pure predicate on bytes: it does not depend on
any reader". [R-VEC-02] already handles a file exercising two rows ("the entry
records every row the file exercises and says which it was built for").
Repair: soften the rationale and say expressly that a decoder refusing the frame
on the mismatch has established the same violation, recorded against R4 — i.e.
add the R3/R4 pair to §21.1's specialization list. Editorial.

### G4 compactor-write-procedure (writer-01)
Verified by grep: [R-LIF-02] is cited at 154, 567, 759, 1180, 1239, 1253, 2921,
2929, 2977, 3065, 3066, 4282 — §20.5 is not among them. §9.1 does contrast a
commit with "a whole-file rewrite under a new file_id (compaction, §20)", and
§9.2's procedure binds "a writer performing a commit". So reading B is real, and
the durability half is a genuine hole. The *bytes* half is not:
> bounds their number only through step 5 of the commit protocol, which pads to
> the next 64-byte boundary (`[R-LIF-02]`) — a longer gap is conforming, and no
> conforming commit produces one.
and §2.3:
> §6.3's flags = 0 against a set ignore-lane bit and §6.2's pre-trailer gap
> longer than `[R-LIF-02]` step 5's pad are the cases this text states
Both outputs are conforming files; F13's 64-multiple still binds. Design-decision.

### G5 128-byte-floor-ordering (verifier-01)
Checked §6.2's [R-CNT-06] enumeration: magic, CRC, version gate, then eight
field gates — [R-CNT-27] is in neither half, and §19.1's four steps do not carry
it. So §21.2's supporting clause has a hole. But the preamble's *operative*
clause is not the ordering claim:
> the rows below whose subject is that file's *geometry* do not reach it
F5's subject ("File size is below the 128-byte minimum") is geometry, and F5 is
not among the four named exceptions (F1, F6, F8, F14, all fixed-across-majors
fields per [R-CNT-24]). So the verdict is decided: F5 does not reach a
foreign-major file, and the reporter's own reading (B) is what the text says.
The finding is right about the justification and wrong that the verdict is open.
PARTIAL. Both readings reject/refuse anyway; [R-CNT-07] is reject-file
independently. Register-bookkeeping.

### G6 unassigned-type-extent-unnamed (verifier-02)
Verified §8.1's last row, §22.3's four residues, [R-MTA-10]'s naming duty, and
[R-CNT-02]'s "a record extent (the bytes any record's extent slot references,
whatever the record's type)" — so those bytes are live state, excluded from the
slack total, covered by no checksum, and no rule obliges a report line. Every
step of the reporter's chain checks out. The text decides it (no duty exists),
so this is a design gap in the certificate's contract, not an ambiguity.
Design-decision.

### G7 filter-dropped-from-§21.7 (diagrams-01)
§20.3 step 4 bars four things "the set of padding positions (§11.3) and the
content `[R-SER-05]` fixes there, the decoded size, the byte offset of any
sample within the decoded tile image, or the codec and filter". §21.7 names the
codec and not the filter — true. The worked witness holds: [R-COD-10] makes
filter 2 total and length-preserving ("The decoded image's length L is divisible
by s in every case"), Q = 4 defeats §20.3's identity escape, and T26 needs a
structural byte to break. So a filter-only re-declaration is genuinely
unwitnessed.
Where the finding overstates: §21.7 paragraph 1 already names the class —
> a mis-strided filter (`[R-COD-10]`), an undisclosed compression dictionary
> ..., or simply wrong data
and §21.1 asks §21.7 for an account **by class**, which paragraph 1 supplies;
[R-COD-10] itself routes the case there ("otherwise the consequence is wrong
sample content — undetectable by construction (§21.7)"). Plus 3343–3347: the
completeness clause does not reach §21.7. PARTIAL. Editorial. Non-byte-level
because §20.3's bar is a MUST that binds the writer whatever §21.7 says.
(diagrams-01's secondary point is quiz-01's; I grouped by primary claim and
cross-reference it.)

### G8 vector-sibling-scope (diagrams-02)
Checked [R-VEC-04]: the requirement enumerates reject-layer and reject-tile; the
rationale's premise is "every vector built from §21's register is
nonconforming", which reaches §21.5's ten ignore-record rows, and §21.5's
preamble confirms they are violations. The zero-layer R1 file is legal
(§21.6: "The file contains zero layers | A conforming file with an empty
directory") and against it ignore-record and reject-file are observationally
identical under [R-VEC-02]'s recorded content. Real gap. Not byte-level:
[R-VEC-01] makes the corpus derivative, and reader behaviour for an R-row file
is fixed by [R-CNT-25] and [R-CNF-12]. Design-decision (widening a normative
requirement).

### G9 §4.7-note-overstates (diagrams-03)
Verified §7.2's table: five fields; `type (0 invalid)` and the flags cell carry
ranges; `inline_length`, `extent_offset`, `extent_length` are bare. The Note's
"each field's range" is not delivered. The defective text is a Note, and
[R-CNF-01]: "All text in this document is normative except: §1 ...; any text
labeled *Note*, *Example*, or *Rationale*". [R-CNT-12]/[R-CNT-13] state the
ranges within two paragraphs. CONFIRMED, editorial.

### G10 R8-instance-collapse (register-01)
The row cell is "top-level document; layer sub-record document" = 2, and
[R-MTA-04] does state the two forms disjunctively (`1e400` overflow vs the bare
tokens). §21.1's licence is conditioned on shape:
> a row whose check ranges over a family without the condition changing shape
> states that range as a single instance (T24's *any codec*), and one whose
> members give the condition materially different shapes enumerates them (T15,
> T25)
Sibling practice (R5's ill-formed bytes vs unpaired-surrogate escape; R7's three
alternatives) enumerates exactly this kind of "different way of exhibiting". So
the coverage consequence is real: nothing obliges a `1e400` vector, and §18.2
calls that "the ordinary case". Counter-consideration recorded: the row's own
"in any form" is the collapse idiom, and §21.1 makes the count mechanical once
the cell is written — so the decision is whether the *condition text* should
have enumerated. Sub-claim corrected: R8 is **not** the only §21.5 row that
fails to multiply — R2, R3, R9, R10 are all 1×2. CONFIRMED on the substance;
register-bookkeeping; 279 if enumerated.

### G11 R6-governing-rule (register-02)
The R6/R10 asymmetry is real: both come from [R-MTA-04]'s fourth bullet and R6
cites `[R-CNT-25]` (R-ENC-12) while R10 cites `[R-MTA-04]` (R-ENC-12), so
[R-VEC-02]'s durable (row, identifier) pair differs for two rows from one
sentence.
But the finding's load-bearing premise is **false**. It claims "[R-ENC-12]
expressly excludes document keys from its own scope". §4.6 says the opposite:
> **Names** — the strings that identify layers, dimensions, channels, and
> user-metadata keys — satisfy three further constraints.
[R-ENC-12]'s carve-out is about the **outcome** only — "a reader MUST treat such
a name as a validity error at the owning scope — except for a key inside a
user-metadata document, where `[R-CNT-25]`'s quarantine governs and the outcome
is ignore-record". So R6's parenthetical R-ENC-12 *is* the requirement that
defines the condition, and §21.1's tie-break does not resolve to nothing.
PARTIAL. Register-bookkeeping.

### G12 vehicle-2-citation (register-03)
§10.1's four vehicles and §10.2's eight-row table check out. Reserved-range rows:
record type F35/F36/L24/L25; layout L36; linearization L33; sample type L34;
codec L43; filter L45; index encoding L31; metadata encoding R1. §20.5's
"(F36, L25, R1)" names the record-type pair plus one of the other seven spaces.
§21.6's closing "(F35, F36, L24, L25)" does use the same bare-list construction
exhaustively, so the reporter's worry about an exhaustive reading is fair. The
sentence is a finding aid inside a SHOULD's rationale and each row registers its
space independently ([R-EXT-03] fixes the reader outcome). Editorial.

### G13 json-nesting-depth (adversary-02) — the only self-flagged byte-level
Tested every premise of the example. `{"a":` ×200,000 + `1` + `}` ×200,000:
well-formed RFC 8259 (the grammar sets no depth), top-level object, no BOM, one
finite number, no duplicate key *within any one object*, single-member objects
so [R-MTA-05] is trivially satisfied, keys 1 byte. 1.14 MiB < 16 MiB. Every
§21.9 quantity within the table. So the file is conforming — the reporter is
right about that.
Verified [R-CNT-25]'s unreadability list: "a failed extent CRC, an unimplemented
or invalid encoding, a decode failure, or content violating the document's own
rules". Depth is none of them, so reading (ii) has no route to ignore-record
either. And two sentences decide it against the depth-limited implementation:
> Every limit that affects which files are valid or which files a conforming
> reader accepts lives in this specification, never only in an implementation.
> ([R-CNF-10], §2.5)
> Software that declines **on that ground** a file whose every quantity lies
> within the table is not a conforming reader (`[R-CNF-03]`) ([R-ERR-04])
So RFC 8259 §9's licence does not ride in, and Verifier A is simply not
conforming. Two *conforming* implementations do not diverge on these bytes.
The reporter's R7 mapping is an implementation error, not a permitted reading —
a deep document *is* well-formed JSON.
Premise of my downgrade, stated so it can be attacked: I treat "a conforming
implementation must accept this file, and a real recursive-descent parser
cannot" as an implementability gap, not as an ambiguity about bytes; and I read
a certify/cannot-establish split as a report-level split, since §2.3 says
"*Cannot establish* is not a finding that the file is nonconforming" and the
file's status is fixed by the byte predicate either way. If a reconciler holds
that certify-vs-cannot-establish *is* an accept/reject split, this becomes
byte-level; the reporter records the same reservation. The gap is real and worth
a §21.9 row. Design-decision.

### G14 codec-witness-claims-fail (adversary-03)
Both constructions check out. codec 2 → codec 1 with stored length already equal
to D: T14's condition is "length differs from the tile's decoded size" and it
does not; T3 compares the decoded payload's length, which under codec 1 is the
stored bytes' length = D; T24 has no decode to under-consume. codec 1 → codec 3
where the image bytes happen to be a valid frame decoding to D with window ≤ D
and FCS absent-or-D: T17–T25 all silent. So §21.7's unconditional "is witnessed
by" is false in constructible cases. This is a false claim in normative text —
stronger than the omissions in G2/G7, and not saved by 3343–3347. CONFIRMED.
Not byte-level: in exactly those cases the violation is undetectable, and
§21.1's completeness runs to a "*detectable* file-conformance violation".
Repair is a qualifier. Editorial.
(Their side-checks on [R-ENC-06], [R-CNT-18] and T2/[R-TYP-07] are also right.)

### G15 only-where-quantifier (quiz-01)
The sentence as written: "witnessed only where the affected tiles remain stored
*and* the change reaches a byte §14 structurally constrains ...; a change that
reaches the decoded size instead is witnessed by T3 or T14". Under an exclusive
reading of both conjuncts the later clauses contradict the first. Reading (a) —
"only" scoping the remain-stored conjunct — is the sole self-consistent one, and
the closing clause about a commit that supersedes every damaged tile presumes
it. CONFIRMED. Editorial; §20.3's MUST binds the writer regardless, and every
named row keeps its detector and outcome.

### G16 277-is-expensive-to-check (quiz-02)
I re-derived it mechanically: 58 + 116 + 55 + 48 = 277 over 36 + 49 + 26 + 10 =
121. Correct. §21.2–§21.5 do each state their condition count and none states an
instance subtotal, so the observation is accurate. No defect in the document;
the proposal (per-subsection instance subtotals) is an ergonomics improvement.
Editorial, no correction required.

### G17 first-five-rows-quantification (quiz-03)
"The first five rows range over declarations, which every file and every layer
carries." Read distributively — every file carries the file-level declarations,
every layer the layer-level ones — the sentence is true, and a zero-layer file
simply has no layer. That is the reporter's own reading (c)/(a). Reading (b)
(asserting at least one instance) requires taking a statement about *carriers*
as a statement about *existence*. Zero layers is conforming ([R-CNT-14], §21.6),
so the phrasing is loose, but nothing turns on it: "The table below states
**minimum guarantees**, not caps" and a row with no instance is exceeded on no
reading. PARTIAL, editorial.

## Coverage

19 input ids, 17 groups, union equals the input exactly, no id in two groups.
Counted twice by hand:
reader-01(G1) reader-02(G2) reader-03(G3) writer-01(G4) verifier-01(G5)
verifier-02(G6) diagrams-01(G7) diagrams-02(G8) diagrams-03(G9) register-01(G10)
register-02(G11) register-03(G12) adversary-01(G3) adversary-02(G13)
adversary-03(G14) adversary-04(G1) quiz-01(G15) quiz-02(G16) quiz-03(G17) = 19.

Byte-level survivors: 0. The two closest calls are G13 (adversary-02) and G1;
both are stated above with the premise the downgrade rests on.
