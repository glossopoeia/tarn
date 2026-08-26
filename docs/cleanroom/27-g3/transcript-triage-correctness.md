# Round 27 triage — correctness lens — working transcript

## What I read

Only `/Users/robertkleffner/Documents/GitHub/tarn/spec/tarn.md`, in these
ranges (via `sed -n`, absolute path, no directory listings anywhere):
heading index; §2 (94–340); §3.2 (400–430); §4.6 (536–582); §5.2 (681–755);
§6.3 (849–895); §7.1–7.3 (930–1045); §8 (1178–1222); §9.7 (1389–1440);
§10 (1440–1530); §11 (1531–1662); §13.3 (1817–1866); §14 (1864–2060);
§17 (2288–2495); §18.2 (2516–2690); §19 (2755–2975); §20 (2971–3411);
§21 (3411–3800); §21.9 (3796–3884); §22 (3884–3995); §24 excerpt
(4098–4115); Appendix G (4335–4478).

I opened **no** walk transcript and **no** other triage pass's notes. I ran
no `ls` on any round-27 directory; the only directory I created is my own
output directory. I read no `docs/`, `PLAN.md`, `AGENTS.md`, `conformance/`,
`registry.json`, git history, or web.

Every input finding was evaluated. No gaps.

---

## Grouping

16 groups over 23 ids.

| group | members |
|---|---|
| sec02-allocation-scope | reader-01, writer-01, verifier-01, quiz-01 |
| appendix-g5-shuffle-universal | writer-04, diagrams-02, adversary-01 |
| appendix-g10-nfd-length-universal | reader-03, diagrams-03 |
| specialization-list-omits-f21-f22 | register-01, quiz-03 |
| bool-layout-note-degenerate-p | reader-02 |
| appender-flags-origination | writer-02 |
| pe0-drop-adding-a-record | writer-03 |
| mta10-uninspected-bytes-aphorism | verifier-02 |
| mta10-report-scope | adversary-03 |
| wrt06-same-ground-antecedent | diagrams-01 |
| sentinel-row-drops-qualifiers | diagrams-04 |
| r3-r4-overlap | register-02 |
| f21-inline-gloss | register-03 |
| tile-outcome-header-drops-qualifier | register-04 |
| append-bar-omits-channel-offset | quiz-02 |
| appendix-g3-leading-gap | adversary-02 |

---

## 1. sec02-allocation-scope (reader-01, writer-01, verifier-01, quiz-01)

Four reporters, one defect. Two self-flagged byte-level (writer-01,
verifier-01), two did not (reader-01, quiz-01).

**Verified against the text.** §22.2 reads, in one paragraph:

> Decoded tile size is a function of the layer's declarations alone
> (§14.2, §14.3), so a reader allocates from geometry and never from a
> length embedded in a payload … A reader MUST NOT size an allocation,
> fetch, or index walk in proportion to a declared magnitude it has not
> corroborated against the file's actual length … `[R-SEC-02]`

Both sentences are inside `[R-SEC-02]`. Quotations are accurate and in
context. §17.2's closing Note does say "no bound relates a stored length
to its decoded size in either direction". §14.3 `[R-SER-07]` does say
"readers allocate from those declarations, not from stored data". §19.4
step 6 obliges the decode. The witnesses (writer-01's 190.7 MiB tile in a
<512-byte file; verifier-01's 2^28 = exactly 256 MiB tile in a 1,280-byte
file) are both arithmetically sound and both lie inside every §21.9 row.

So the reporters' premise — that the closing MUST NOT, read literally,
reaches the decode buffer — is **correct**. The defect is real: the
sentence's scope is unbounded on its face and it sits in the same
requirement whose opening licenses exactly the allocation it would forbid.

**Byte-level: downgraded. The premise my downgrade rests on**, stated so it
can be attacked: that the "reject" branch of the alleged fork is not open
to a *conforming* reader, because `[R-CNF-03]` states an unqualified duty
to accept and enumerates the only three refusal grounds, none of which is
`[R-SEC-02]`:

> A reader MUST accept every conforming file of a format major version it
> implements, carrying no record of a type it does not implement with
> MUST_UNDERSTAND = 1 … and none of whose values exceeds the minimum
> guarantees of §21's limits table (§21.9's `[R-ERR-04]` governs a refusal
> on that last ground; §21.6's closing paragraph names the other two)

and `[R-ERR-04]`:

> Software that declines **on that ground** a file whose every quantity
> lies within the table is not a conforming reader (`[R-CNF-03]`)

and, decisively, because the literal reading cannot be reached by applying
`[R-SEC-02]` *as a requirement* — the requirement's own first property is
that "a reader allocates from geometry". A rule cannot be the specific
authority for forbidding what its own opening sentence states as the
format's defense. §22.1 `[R-SEC-01]` says the same at the threat-model
level: "a conforming reader derives what it allocates and fetches from
*declarations it has verified*".

Under the literal reading no reader is conforming at all (accept → breach
of `[R-SEC-02]`; decline → breach of `[R-CNF-03]`). An empty conformance
class is an internal inconsistency, not two defensible verdicts. So
resolving this does not change which byte sequences a conforming
implementation must accept or reject: it must accept, both before and
after the repair. The emittable set is untouched — no writer rule is in
play.

**Attack surface on that premise, honestly stated:** the document states no
precedence rule between two conflicting MUSTs. Someone could argue
`[R-SEC-02]` is the later, more specific security rule and that
`[R-CNF-03]`'s acceptance duty is implicitly qualified by it; on that view
the fork is live and this is byte-level. My answer is the one above — the
"more specific rule" is `[R-SEC-02]`, and `[R-SEC-02]` says a reader
allocates from geometry. This is the group I would re-check first if the
maintainer disagrees anywhere.

**Repair.** Bound the MUST NOT to magnitudes that determine how many of
the file's own bytes a reader fetches, walks, or buffers (offsets,
lengths, extents, entry counts), and exempt the decoded tile size by name,
citing `[R-SER-07]` and §21.9's per-tile guarantee as what bounds it
instead.

---

## 2. appendix-g5-shuffle-universal (writer-04, diagrams-02, adversary-01)

Same sentence, same false universal, three different counterexamples. One
defect.

`[R-COD-10]`: filtered image places byte i of group j at offset i·n + j.
At s = 2, n = 2, L = 4 this is the transposition of offsets 1 and 2,
fixing 0 and 3. Therefore **every** decoded image with byte 1 = byte 2 is a
fixed point.

- writer-04: one uint16 channel, P = 2 → Q = 2, L = 4; values 0x0100,
  0x0001 → `00 01 01 00`. Fixed. Verified.
- diagrams-02: two uint8 channels, P = 2 → Q = 2, L = 4; samples
  (AA,BB),(BB,CC) → `AA BB BB CC`. Fixed. Verified.
- adversary-01: byte-uniform image `00 00 00 00`, fill 0x0001 so item 6's
  sentinel rule does not remove the tile. Fixed. Verified.

All three also correctly verify the *first* half of the sentence (identity
iff s = 1 or n = 1). The trailing clause "elsewhere it changes the stored
bytes of every tile it touches" is false.

**Byte-level: no.** `[R-CNF-01]`: "All text in this document is normative
except: §1 (Introduction); any text labeled *Note*, *Example*, or
*Rationale*; and appendices identified as non-normative." Appendix G's
heading reads "(non-normative)" and its own preamble says "It adds no
requirement to any actor: a writer ignoring it is fully conforming."
`[R-COD-10]`, which is normative, fixes the permutation exactly and is
untouched. Item 5's prescription (pin the filter value) survives intact.

**Repair.** "…elsewhere it changes the stored bytes of every tile whose
decoded image the permutation does not fix", or drop the clause.

---

## 3. appendix-g10-nfd-length-universal (reader-03, diagrams-03)

Item 10: "A caller-supplied decomposed name is a different name under
`[R-ENC-13]` and a different length — §4.6's `température` is 12 bytes in
NFC and 13 in NFD — so a writer that does not normalize emits a different
layer record, a different `inline_length`, and a different `dir_length`."

The `température` figure checks out against §4.6's Example (12 vs 13).
The general claim does not.

- reader-03's class: an ASCII base letter (1 byte) plus one combining mark
  in U+0300–U+036F (2 bytes) composing to a precomposed character in
  U+0800–U+FFFF (3 bytes). Spot-checked U+1E00: NFD `41 CC A5` (3 bytes),
  NFC `E1 B8 80` (3 bytes) — different bytes, equal length. The class is
  real; I did not re-run the 155 count and do not rely on it.
- diagrams-03's class: canonical reordering alone. `a`+U+0301+U+0327 =
  `61 CC 81 CC A7` (5 bytes); NFC reorders by combining class to
  `61 CC A7 CC 81` (5 bytes), no composition available. Different bytes,
  equal length. Correct — canonical reordering is length-preserving by
  construction.

Both hit the same sentence and the same false universal. One group. The
first consequence ("a different layer record") is true and is what carries
item 10's advice; the length claim and the two consequences hung off it
are false.

**Byte-level: no.** Same `[R-CNF-01]` exemption as group 2; and
`[R-ENC-13]` already decides name identity by raw bytes, so no file's
conformance turns on the length claim.

**Repair.** Replace "a different length" with "a different byte string",
keep the `température` figure as one case, and drop or qualify the
`inline_length`/`dir_length` consequences.

---

## 4. bool-layout-note-degenerate-p (reader-02)

§14.4's Note: "A single-channel bool layer does not — ⌈P/8⌉ packed bytes
planar versus P bytes interleaved".

`[R-GEO-01]` requires only Tᵢ ≥ 1, so rank 1 with T = (1) gives P = 1 and
⌈1/8⌉ = 1 = P. With fill false, `[R-SER-05]` forces the seven pad bits to
0, so the planar byte is 0x00/0x01 — byte-identical to the interleaved
byte (§14.2). With fill true they are 0xFE/0xFF vs 0x00/0x01, so the claim
is silently fill-dependent. P = 1 is the only P where the Note's own
formula degenerates. Verified; reporter is right on every step.

**Byte-level: no.** `[R-CNF-01]` exempts "any text labeled *Note*", and
§14.2 `[R-SER-02]` and §14.3 `[R-SER-03]` fix every byte of both images
independently of what the Note says about them.

**Repair.** "…does not, wherever ⌈P/8⌉ ≠ P", or add "for P > 1".

---

## 5. appender-flags-origination (writer-02) — self-flagged byte-level

Verified: `[R-CNT-08]`'s MUST is scoped — "a writer creating a file under
this text MUST write flags = 0" — and §20.1 defines *creator* as the tier
that "emits a complete file in one commit, generation 1", *appender* as
one that "extends an existing file by commits". The compactor carve-out
("A compactor, though its output is a new file…") shows the drafters read
"creating a file" as producing a new file. Appendix G item 8 confirms:
"The `flags` half is a creator's rule". The appender's only stated flags
obligation is copy-forward and no-clear. §10.2 expressly excludes the flag
lanes from the numeric identifier spaces, so §10.3's experimental-value
prohibition does not reach them either. §20.3 step 6's enumeration is not
exhaustive of trailer fields (it omits dir_offset, dir_length,
committed_file_length, CRC), which weakens reading (2).

So the gap is real: nothing in the text bars an appender from originating
an ignore-lane bit.

**Byte-level: no.** The premise: this is a writer-conduct obligation the
document itself declassifies. `[R-CNF-02]`:

> A writer obligation whose violation this specification expressly
> declares not to be a file-conformance violation binds the actor in the
> same way; §6.3's flags = 0 against a set ignore-lane bit and §6.2's
> pre-trailer gap longer than `[R-LIF-02]` step 5's pad are the cases this
> text states

and §21.6: "An ignore-lane flag bit (16–31) is set | Ignored; the file is
conforming". `[R-CNT-08]` also obliges every reader to "ignore all bits in
the ignore lane". So the disputed trailer is a conforming file under both
readings and no reader's or verifier's verdict moves. What moves is only
whether one appender's conduct is conforming — the exact category
`[R-CNF-02]` names for this very rule.

**Repair (a maintainer decision).** State the flags obligation over every
writer producing a trailer under this text — no bit originates here — with
copy-forward as the stated addition for updaters and compactors.

---

## 6. pe0-drop-adding-a-record (writer-03) — self-flagged byte-level

Verified: §20.4's MU = 0 / PE = 0 cell licenses a drop only "in a commit
that *independently* changes the scope the record attaches to: … for a
top-level record, the file's layer set, any layer record's content, or
another *non-layer* top-level record." It then resolves two cases
expressly — "A commit changes the layer set by adding a layer" and
"Dropping the record, or dropping another record in the same commit, is
not itself such a change" — and leaves *adding* a top-level non-layer
record unresolved. The asymmetry the reporter noticed (a set in item 1, an
individual record in item 3) is on the page.

One textual lever the reporter did not use, which leans toward reading (1):
the express exclusion of "dropping another record in the same commit" is
only necessary if changes to the non-layer top-level record *population*
are the kind of thing that could qualify. That is an implicature, not a
statement, so the gap stands.

**Byte-level: no.** The premise: the disputed byte sequence is a
conforming file under both readings, and the obligation forked is an
updater-conduct one with no file-level witness. `[R-CNF-02]`: "File
conformance is a pure predicate on bytes: it does not depend on any
reader, writer, or environment." §21.7 `[R-ERR-01]`: "A second set of
obligations is omitted from the register because a single file exhibits no
witness of their violation" — and the register carries no row for an
improper drop, its detection requiring the prior generation, "which §9.7
does not reconstruct". No reader or verifier verdict moves.

**Attack surface:** if the maintainer reads "which byte sequences a
conforming implementation may emit" as reaching updater-conduct
obligations (under (2) no conforming appender may emit that generation
from that input; under (1) one may), this group flips to byte-level. It is
the second-strongest candidate in the batch after group 1, and the one I
would re-check if the gate's reading of "may emit" is the broad one.

**Repair (a maintainer decision).** Say expressly whether adding a
non-layer top-level record counts, as the rule already does for adding a
layer.

---

## 7. mta10-uninspected-bytes-aphorism (verifier-02)

Headline claim checked and it holds. §8.1's map: "| Extent of a record of
a type this specification has not assigned | none — the bytes are opaque
(§7.2) | — |". §5.2 `[R-CNT-02]` makes such an extent a *structure* ("a
record extent (the bytes any record's extent slot references, whatever the
record's type, §7.2)"), so it never enters the slack total `[R-CNT-21]`
obliges a verifier to report. §9.7 `[R-LIF-08]` has the walk check each
claimant "against the checksum covering it, **where §8.1's map states
one**" — so nothing verifies it — and requires no report naming individual
claimants. §21.6 makes a file carrying an MU = 0 experimental-range record
conforming. §22.3 `[R-SEC-04]` concedes the exposure in terms. So the
class exists: certified by nothing, counted by nothing, named by nothing.
`[R-MTA-10]`'s closing aphorism — "bytes a certificate covers without
inspecting are counted and named, never silent" — is therefore false as a
general statement.

Where the reporter is weaker: its reading (1), a *general duty* extracted
from the aphorism, is not available. The MUST is expressly scoped — "it
MUST report each record it ignored **on this ground**" — and the aphorism
is a declarative colon-clause, not a MUST. The reporter itself chose
reading (2). So the defect is the over-general justification, not a live
fork in verifier duty. Graded CONFIRMED on the headline; the two-reading
framing is not what is wrong.

**Byte-level: no.** Verifier report content only; certification is
expressly unaffected ("the record is not among `[R-CNF-11]`'s
cannot-establish grounds, and certification is unaffected").

**Repair.** Either bound the aphorism to the metadata case it justifies,
or add the report duty for an unassigned-type record extent that §22.3
already describes as the strictly worse-covered class.

---

## 8. mta10-report-scope (adversary-03)

Verified. `[R-MTA-10]`'s paragraph opens "Under an unassigned encoding",
and §21.5's preamble confirms the term's breadth: "Encoding 0 and a
reserved-range value are unassigned too, and R1 registers both as
violations: what `[R-MTA-10]` withdraws is the document's content rules,
never the encoding byte's own value set". §22.3 `[R-SEC-04]` states the
report duty over "an unassigned encoding". §21.6's row states it only on
the experimental row. The MUST's own subject is qualified "in an otherwise
conforming file", which is doing real work since an encoding-0 record is
itself R1. Both readings are genuinely on the page.

**Byte-level: no.** §2.3 `[R-CNF-11]`: "that per-requirement report
constrains the report and not the verdict". R1 already fixes the verdict
as nonconforming for encoding 0 / reserved, and `[R-MTA-03]` plus
`[R-CNT-25]` already fix the reader outcome as ignore-record. No writer
output changes.

**Repair.** Say which encodings the report duty ranges over — most simply,
"each record it ignored for an encoding this specification does not
assign", and align §21.6 and Appendix H with it.

---

## 9. wrt06-same-ground-antecedent (diagrams-01)

Verified on both halves. The cell's "Compaction is barred on the same
ground (`[R-WRT-06]`)" follows two consecutive file-scope anaphors, so
reading (i) is the natural English. And the reporter's secondary point is
right: `[R-WRT-06]`'s stated ground is *not* reject-file —

> A compactor MUST refuse to compact a file carrying any record whose type
> it does not implement with MU = 1: such a type can define references
> this specification does not (§7.2), so its bytes cannot be safely
> relocated.

The reachability argument also checks out: §21.6 says "the same type as a
layer sub-record is reject-layer and never a ground to refuse the file
(`[R-CNT-18]`)", so a conforming file can carry an experimental MU = 1
layer sub-record.

**Byte-level: no.** The sentence quoted immediately above — "**any**
record" — decides the question, in the section that owns the operation and
in the very rule the cell cites; §20.5 reinforces it ("an MU = 1 type the
compactor does not implement never reaches this step (`[R-WRT-06]`)"). Two
implementations that follow the citation agree.

**Repair.** Rewrite the cell's last sentence to name its own ground:
"A compactor MUST refuse to compact a file carrying such a record at
either scope, because its type may define references this specification
does not (`[R-WRT-06]`)."

---

## 10. sentinel-row-drops-qualifiers (diagrams-04)

Verified. `[R-TYP-08]` is doubly qualified — "a reader that returns any of
the tile's sample positions **inside the layer's extents** MUST return,
**for each channel the tile carries**, that channel's fill value at every
such position" — and §21.6's row compresses that to "every sample position
it carries reads as **the channel's** fill". Both qualifications are gone.
`[R-GEO-04]` ("a reader MUST NOT return padding positions as samples") and
`[R-MDL-01]` are inconsistent with the literal cell, and §19.4 step 4
states the per-channel form correctly.

**Byte-level: no.** §21.1 decides it in advance, twice: "where a row and
the rule it cites diverge, **the rule governs**", extended in the same
paragraph — "§21.6's entries restate their governing rules on the same
terms a row does, and where such an entry and the rule it cites diverge,
the rule governs there too."

**Repair.** "every sample position it carries **that lies inside the
layer's extents** reads as **the fill of each channel the tile carries**".

---

## 11. specialization-list-omits-f21-f22 (register-01, quiz-03)

Same defect: §21.1's specialization clause names F1/F6, F1/F8, F35/F36,
L24/L25 and omits F21 ⊂ F22 and L10 ⊂ L11.

Verified: F21 is "carries extent slot (0, 0)"; a (0,0) slot has
extent_length 0, and F22 is "extent_length is less than 5". Every F21 file
is an F22 file. `[R-CNT-25]` does not separate them either: "An extent of
(0, 0) on a user-metadata record, or one whose extent_length is less than
5 … is a validity error at its containing scope" — the second disjunct
carries no nonzero qualifier, and the neighbouring F31 shows the document
writes the qualifier when it means it ("A non-layer top-level record's
**nonzero** extent slot…"). L10/L11 are the same pair verbatim at layer
scope. register-01's reading (a) is the right one.

quiz-03's extra pair is **wrong as stated**: F30 ("exactly one half zero")
and F22 ("extent_length < 5") are not in a containment relation — a
user-metadata record with offset ≠ 0 and length 3 exhibits F22 and not
F30; one with offset 0 and length 7 exhibits F30 and not F22. §21.1's
clause resolves *specializations*, so it would not apply to that pair even
if named. register-01 gets this right where quiz-03 does not: it records
F30/F31 and L15/L16 as "partial overlaps rather than containments, so
§21.1's clause would not resolve them even if it named them."

**Byte-level: no.** F21 and F22 carry the same outcome, detector and
detection point; a file exhibiting either is nonconforming under both
readings, so `[R-CNF-05]` bars every conforming writer from it either way
and no reader's verdict differs. The cost is row attribution under
`[R-VEC-02]` (whose "where a condition cannot be isolated" escape I read
in §24) and a verifier's diagnostic.

**Repair.** Add F21 of F22 and L10 of L11 to §21.1's list, or state the
clause as a general rule rather than an enumeration. Do not add
quiz-03's F30/F22 pair.

---

## 12. r3-r4-overlap (register-02)

Verified. R3: "A user-metadata document's stored bytes fail to decode
under its declared assigned encoding" — its carve-outs are experimental
encodings (to §21.6) and encoding 0 / reserved (to R1); nothing carves out
R4. R4's separating clause: "unlike R3, a constraint of this row is broken
by what the frame declares rather than by whether the bytes decode, so a
reader that only tries decoding establishes none of them". R4's instance
list begins "missing frame magic, top-level extent" and includes "a
nonzero dictionary ID". For missing magic there is no frame, so nothing
"the frame declares" is broken, and a decode attempt fails; for a nonzero
dictionary ID a decoder without the dictionary errors. So the stated
ground is false for two of R4's own instances, and those instances satisfy
R3 verbatim. §18.2's separating sentence has the same problem: "the bytes
decode, and what is wrong is what the header said about them" is true only
of the content-size mismatch, the checksum flag, and (for a tolerant
decoder) a second or skippable frame.

R3 and R4 overlap; neither contains the other (R4's content-size instance
decodes cleanly), so §21.1's specialization clause cannot resolve it.

**Byte-level: no.** Both rows are violations with outcome ignore-record;
under either attribution `[R-CNF-05]` bars the file and every conforming
reader skips the record. Only the row a verifier names and a manifest
records moves.

**Repair.** Carve R4 out of R3 explicitly (as R3 already carves out
experimental, 0 and reserved encodings), and restate R4's ground as
"checkable from the extent's bytes without relying on a decoder's
tolerance" rather than "not by whether the bytes decode".

---

## 13. f21-inline-gloss (register-03)

Verified. §7.1 `[R-CNT-25]`: "Each user-metadata record carries its
document in its extent — **never inline** — and declares the document's
encoding in its own inline payload (u8 …)". §18.2 `[R-MTA-03]`: "A
user-metadata record's inline payload is exactly one byte", and
inline_length ≠ 1 is F23. So a record with slot (0, 0) and a conforming
one-byte payload has its document nowhere; it cannot place it inline, and
a record that tried would be F23, not F21. F21's trailing clause
"placing its document inline" describes a state no file can exhibit. L10,
the identical condition at layer scope, carries no such clause.

**Byte-level: no.** §21.1: "where a row and the rule it cites diverge, the
rule governs"; a (0,0) slot on a user-metadata record is reject-file under
every reading.

**Repair.** Delete the clause, matching L10's wording.

---

## 14. tile-outcome-header-drops-qualifier (register-04)

Verified. §21.4's header states reject-tile as "that tile's read reports
failure, and never returns fill in place of data (`[R-CNF-09]`)", while
`[R-CNF-09]` is qualified: "from a scope this specification rejects **and
whose rejection this reader is obliged to detect** (`[R-RDR-02]`)". T2,
T4, T5 and T26 carry Detector *verifier*, so no reader is obliged to
detect them, and for T2 `[R-SER-08]` positively tells such a reader what
to return.

Where the finding overstates: it says the header "forbid[s] exactly the
behavior `[R-SER-08]` mandates", which is true only under a reading §21.1
forecloses in advance, and names `[R-SER-08]` by name while doing so:

> For a row whose Detector is *verifier*, the outcome names the scope at
> which the damage is recorded, not an obligation on any reader: the
> governing rule states what a reader does … `[R-SER-08]` is the one rule
> that goes the other way: it resolves a nonconforming interleaved boolean
> byte to a value rather than serving it through

**Byte-level: no**, on that quotation. The dropped qualifier is a real
imprecision in a restatement; it is not a live fork.

**Repair.** Add "for a reader obliged to detect the violation" to §21.4's
header, or cross-reference §21.1's verifier-row paragraph from it.

---

## 15. append-bar-omits-channel-offset (quiz-02) — graded PARTIAL

The observation is accurate: §20.3 step 4's enumeration names "the byte
offset of any **sample** within the decoded tile image" and never Fᶜ, the
in-sample offset §14.2 defines. I checked the witness: reordering two
interleaved channels of equal element size with byte-identical recorded
fills moves no listed item — padding positions unchanged, `[R-SER-05]`
content unchanged (equal fill bytes, equal sizes), P·Q unchanged, sample
offsets (k div C)·Q unchanged, codec and filter unchanged — while Fᶜ, and
so what every stored tile decodes to, changes.

But the claimed *ambiguity* is refuted by the passage's own words:

> The test is the effect on such a tile, and the list names where that
> effect arises rather than standing on its own

and by `[R-SER-01]`, which fixes "value k of the sequence is channel
(k mod C)'s value at in-tile ordinal k div C". §14 therefore does fix how
those stored bytes decode, and the general test bars the commit. The
reporter concedes as much ("the two readings are not both defensible on
the text as a whole"). So: the enumeration is under-inclusive (real,
worth fixing); the passage is not ambiguous. PARTIAL.

**Byte-level: no**, on the quotation above.

**Repair.** Add "the byte offset of any channel's value within the decoded
tile image" to the list, or name §14.1's value sequence in it.

---

## 16. appendix-g3-leading-gap (adversary-02) — graded PARTIAL

The reachability half is right: with item 3's emission order the first
structure is the first layer's first stored tile, and a declared A ≥ 512
(§16.1's floor) or A_slab > 16 leaves a nonempty run [16, first_offset)
that can be thousands of bytes.

The ambiguity half does not survive. Item 3's own citation resolves it:
"every byte of every such gap is zero — `[R-CNT-03]`'s advice, **taken as
a requirement here**", and `[R-CNT-03]` reads:

> Writers SHOULD zero the gaps they create — **the run before an aligned
> tile or slab run**, and the pre-trailer pad.

The leading run *is* the run before an aligned tile. Taking that advice as
a requirement therefore covers it, and reading (b) — interior gaps only —
loses. The closing gloss "the space between structures is free" is the
rationale for the requirement, not its scope limit. So: a real wording
weakness that a reader must follow a citation to settle, not an open
degree of freedom. PARTIAL.

**Byte-level: no.** Appendix G is non-normative (`[R-CNF-01]`), and
`[R-CNT-21]` puts slack content outside every conformance requirement, so
both readings produce conforming files every reader and verifier treats
identically.

**Repair.** Name the leading run explicitly: "the run from 16 to the first
structure, every alignment-forced gap between structures, and the
pre-trailer pad are all zero."

---

## Byte-level tally

0 of 16 groups. Four inputs were self-flagged byte-level (writer-01,
writer-02, writer-03, verifier-01); each downgrade is carried by a
quotation above, and for groups 1, 5 and 6 I have stated the premise the
downgrade rests on and named the attack on it.
