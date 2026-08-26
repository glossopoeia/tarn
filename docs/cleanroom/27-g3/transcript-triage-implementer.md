# Round 27 triage — implementer-consequence lens — working transcript

## Access disclosure

Read only `/Users/robertkleffner/Documents/GitHub/tarn/spec/tarn.md`, in these
slices (via `sed -n`/`grep -n`, no directory listing, no other file opened):

- `wc -l` (4549 lines), `grep -n "^## \|^### "` for the section index
- §2 (lines 94–340): conformance classes, outcome classes, §2.5 limits
- §4.6 (552–585): name rules, `température` Example
- §5.2 (640–754): byte coverage, slack
- §6 (754–930): front block, trailer, version/flag gates, remote open
- §7.1 (940–1030): record framing, `[R-CNT-25]`, `[R-CNT-13]`, `[R-CNT-14]`
- §8 (1178–1225): coverage map, verification obligations
- §11.3 (1600–1625): `[R-GEO-04]` padding, §11.4 linearization
- §11.1 (1536–1548): `[R-GEO-01]`
- §13 (1795–1830): fill constraints, `[R-TYP-08]`
- §14 (1864–2060): whole section
- §17 (2288–2500): whole section
- §18.2 (2515–2700): `[R-MTA-03]`, `[R-MTA-09]`, `[R-MTA-04]`, `[R-MTA-05]`, `[R-MTA-10]`
- §20 (2971–3411): whole section
- §21 (3411–3884): §21.1, §21.2 rows, §21.3 head rows, §21.4, §21.5, §21.6, §21.7, §21.8, §21.9
- §22 (3880–3960): §22.1–§22.3
- Appendix G (4335–4480), Appendix H excerpt (4538–4548)

I did **not** read any walk transcript, any other triage pass's notes, `docs/`,
`PLAN.md`, `AGENTS.md`, `conformance/`, `spec/registry.json`, git history, or the
web. I did not list any directory (I created my own output directory with
`mkdir -p`, which enumerates nothing). CLAUDE.md/AGENTS.md content was injected
into my context by the harness as a system reminder before I began; I did not
open those files.

## Grouping

23 ids → 16 groups. Union of member_ids = the 23 input ids, no duplicates,
counted by hand twice (4+3+2+1+1+1+1+1+1+2+1+1+1+1+1+1 = 23).

| group | members | why one defect |
|---|---|---|
| sec02-decode-buffer-allocation | reader-01, writer-01, verifier-01, quiz-01 | all four quote the same two sentences of `[R-SEC-02]` and pose the same scope question about "a declared magnitude" |
| appg5-filter-fixes-some-images | writer-04, diagrams-02, adversary-01 | three distinct 4-byte counterexamples to the *same* trailing universal in Appendix G item 5 |
| appg10-nfd-equal-length | reader-03, diagrams-03 | same clause ("a different length"), two families of equal-length non-NFC names |
| specialization-list-omits-usermeta-rows | register-01, quiz-03 | same §21.1 sentence, same F21⊂F22 / L10⊂L11 containment; quiz-03 adds F30⊂F22, which is the same bookkeeping defect |

Singletons: reader-02, writer-02, writer-03, verifier-02, diagrams-01,
diagrams-04, register-02, register-03, register-04, adversary-02, adversary-03,
quiz-02.

## Group 1 — `[R-SEC-02]` vs the decode buffer (4 members, 2 byte-level flags)

Text verified verbatim at spec lines 3897–3911. Both sentences are in one
requirement. §17.2's closing Note verified: "For the compressing codecs (2–4),
no bound relates a stored length to its decoded size in either direction".
`[R-SER-07]` verified: "readers allocate from those declarations, not from
stored data." The contradiction the reporters describe is **real**; I confirm
it.

writer-01 and verifier-01 flag byte-level on the claim that the literal reading
forces a decline, so two conforming readers reach opposite accept/reject
verdicts on one conforming file. **I tested that premise rather than inheriting
it, and it fails twice over.**

**Leg 1 — literal `[R-SEC-02]` does not force a decline.** The MUST NOT is on
*sizing an allocation in proportion to* an uncorroborated declared magnitude. A
reader that decodes into a buffer it grows as output arrives, capped by
`[R-COD-08]`'s "the stored bytes MUST decode to exactly the decoded size — no
more, no fewer", never sizes an allocation from the declared magnitude and still
accepts the file and returns every sample. That is a standard streaming zstd/lz4
decode, not a contrivance. So under reading B the reader still accepts; only its
malloc pattern changes — and §2.1's phrasing-discipline Note says requirements
here "constrain bytes and observable behavior, never implementation technique".
Both reporters' witness files are served identically under both readings.

**Leg 2 — even if it did force a decline, the decline is foreclosed.** §2.5
`[R-CNF-10]`: "Readers MAY enforce resource limits, but MUST accept any
conforming file within the minimum guarantees stated in §21's limits table."
That sentence is unqualified — it does not turn on the *ground* of the refusal,
so the "[R-ERR-04] says 'on that ground'" escape hatch a literal reader might
reach for does not exist. `[R-CNF-03]` says the same: "A reader MUST accept
every conforming file … none of whose values exceeds the minimum guarantees".
So no reading of `[R-SEC-02]` licenses rejecting verifier-01's 1,280-byte file
or writer-01's 512-byte file. The accept/reject verdict a *conforming* reader
must reach is identical under both readings; the emittable set is untouched
because `[R-SEC-02]` binds readers only and imposes nothing on any writer.

Where writer-01/verifier-01 are right and reader-01/quiz-01 understate: the
implementer consequence is severe and not merely prose. §22.2 is exactly the
section a security engineer reads before writing the anti-decompression-bomb
guard, and the guard the last sentence invites — refuse an allocation
disproportionate to file length — makes an otherwise-correct reader
**nonconforming** on ordinary compressed files, discoverable only by
cross-reading §14.3, §17.2, §21.9 and §2.5. That is a maintainer decision owed,
not an editorial tidy. Severity design-decision, byte-level false.

Downgrade quotations of record: `[R-CNF-10]` above; `[R-COD-08]`'s exact-size
rule (leg 1's cap).

## Group 2 — Appendix G item 5's trailing universal

Text verified at 4425–4430. `[R-COD-10]` verified at 2470–2481: byte *i* of
group *j* goes to offset `i·n + j`.

I re-derived all three counterexamples rather than trusting them.

- adversary-01: interleaved, one uint16 channel, P=2 ⇒ Q=2, L=4, s=2, n=2.
  All-zero image `00 00 00 00` is a fixed point of any permutation. Fill 0x0001
  ⇒ item 6 stores the tile. Valid.
- diagrams-02: two uint8 channels, P=2, Q=2, L=4. Image `AA BB BB CC`.
  Offsets: g0b0→0, g1b0→1, g0b1→2, g1b1→3 ⇒ `AA BB BB CC`. Valid.
- writer-04: one uint16 channel, image `00 01 01 00` ⇒ `00 01 01 00`. Valid.

At s=n=2 the permutation transposes offsets 1 and 2 and fixes 0 and 3, so every
image with byte1 = byte2 is fixed. The universal is false.

Byte-level: no. `[R-CNF-01]`: "All text in this document is normative except: §1
(Introduction); any text labeled *Note*, *Example*, or *Rationale*; and
appendices identified as non-normative." Appendix G's heading carries
"(non-normative)" and its own opening says "It adds no requirement to any actor:
a writer ignoring it is fully conforming." Item 5's actual prescription (pin the
filter value) is untouched; `[R-COD-10]` fixes the permutation normatively.
Editorial.

Implementer consequence, stated plainly: a profile-conformance checker built on
the universal would flag "filter 2 declared, stored bytes unchanged" as a
violation and reject reproducible files. That is a real cost to a profile
adopter — but no TARN file's conformance and no reader's verdict moves.

## Group 3 — Appendix G item 10's "a different length"

Text verified at 4453–4458; §4.6's Example verified at 576–581.

Both counterexamples re-derived:
- reader-03: U+1E00 NFD = `41 CC A5` (3 bytes), NFC = `E1 B8 80` (3 bytes).
  Equal length, different bytes. The Latin Extended Additional class is large.
- diagrams-03: `a` + U+0301 (ccc 230) + U+0327 (ccc 202) = `61 CC 81 CC A7`;
  canonical reordering gives `61 CC A7 CC 81`; no precomposed a-with-cedilla
  exists, so no composition shortens it. 5 bytes either way.

Both are correct, and canonical reordering *never* changes UTF-8 length, so
diagrams-03's shape is a whole family. Item 10's first consequence ("a different
layer record") is true and is the one that carries the advice under
`[R-ENC-13]`'s raw-byte identity; the length claim and the two consequences hung
off it are false.

Byte-level: no, on `[R-CNF-01]` plus `[R-ENC-13]`, which decides name identity by
raw bytes so both forms are conforming names regardless. Editorial.

Implementer consequence: an adopter's reproducibility check that compares
`inline_length`/`dir_length` concludes two files match when their layer names
differ byte-for-byte — reintroducing the exact hazard §4.6's Example exists to
close. Worth fixing, still not a byte fork.

## Group 4 — §14.4's Note on single-channel bool layouts (reader-02)

`[R-GEO-01]` verified: "A layer has rank d ≥ 1 … a tile extent Tᵢ ≥ 1". So
rank 1 with T=(1) gives P=1 and ⌈1/8⌉ = 1 = P. `[R-SER-05]` verified: "Every pad
bit (§14.3) MUST carry the plane's channel's fill bit." With fill false the
planar byte is 0x00/0x01 and the interleaved byte is 0x00/0x01 — identical. With
fill true they differ (0xFE/0xFF vs 0x00/0x01), so the Note is silently
fill-dependent. P=1 is the only counterexample; 2..8 all differ in length.

Byte-level: no. The text is labeled **Note** and `[R-CNF-01]` exempts it; §14.2
and §14.3 fix every byte of both images independently. Editorial.

Implementer consequence: nothing in a reader breaks. A test suite or
layout-detection heuristic resting on "the two layouts always differ for bool"
breaks on the degenerate layer. Inert for readers, live for test authors.

## Group 5 — an appender originating an ignore-lane flag bit (writer-02) — BYTE-LEVEL

`[R-CNT-08]` verified verbatim at 875–888: "a writer **creating a file** under
this text MUST write flags = 0 … A compactor, **though its output is a new
file**, carries the input's unknown ignore-lane bits into its output trailer
rather than writing flags = 0 … An updater MUST copy forward unknown ignore-lane
bits of the file it modifies and MUST NOT clear them".

§20.1 defines the tiers: creator "emits a complete file in one commit"; appender
"extends an existing file by commits". The compactor clause shows the drafters
read "creating a file" as producing a new file and thought the compactor needed
an express exception on that account. An appender's output is not a new file. So
the flags = 0 MUST does not on its face bind an appender, and the appender's only
stated flags duty is copy-forward, which an appender that copies forward *and*
adds a bit has discharged.

§20.3 step 6 is the counterweight: "trailer with generation one greater, the same
file_id, unknown ignore-lane flag bits copied forward (`[R-CNT-08]`), and
version_minor per `[R-CNT-26]`". Read exhaustively it fixes flags to the input's.
The text nowhere says the enumeration is exhaustive, and §21.6 makes the result
conforming either way: "An ignore-lane flag bit (16–31) is set | Ignored; the file
is conforming".

**Why I keep the byte-level flag.** Two appenders built from this text, given the
same input, may emit trailers differing at offset 12 (flags u32) and consequently
at offset 60 (trailer CRC). Under reading (2) that byte sequence is unreachable by
any conforming actor under this text — creators MUST write 0, compactors and
updaters may only carry forward, so flags = 0 is a permanent invariant of the
lineage. Under reading (1) it is reachable, and `[R-CNT-08]`'s copy-forward duty
then obliges every downstream updater and compactor to propagate a meaningless bit
forever. That is a change in which byte sequences a conforming implementation may
emit — the first clause of the byte-level test.

**The premise my flag rests on, stated for attack.** §2.3 `[R-CNF-02]` classes
"§6.3's flags = 0 against a set ignore-lane bit" among obligations that "govern
their conduct rather than their output", and says "a file is never nonconforming
by virtue of one". If one reads the byte-level test as ranging only over the
*conforming-file predicate*, this group drops to design-decision, because the file
is conforming under both readings. I read the test as written — "which byte
sequences a conforming implementation may emit" — and a conforming appender's
permitted output differs between the readings, so I flag it. Someone who thinks
`[R-CNF-02]` narrows the test to file conformance should attack me here.

Implementer consequence, concretely: a vendor wanting an out-of-band marker has no
experimental sub-range in the flags lane (unlike record types, §10.2). Reading (1)
hands it one, reachable only on append, and §21.6 promises the file stays
conforming. Reading (2) closes it. Two vendors will not build the same thing.

Repair: state the flags obligation over every writer producing a trailer under this
text — no bit originates here — with copy-forward as the stated addition for
updaters and compactors.

## Group 6 — dropping a PE = 0 record in a commit that *adds* a record (writer-03) — BYTE-LEVEL

Row verified verbatim at 3245. The relevant clauses: "except in a commit that
*independently* changes the scope the record attaches to: … for a top-level record,
the file's layer set, any layer record's content, or another *non-layer* top-level
record. A commit changes the layer set by adding a layer … Dropping the record, or
dropping another record in the same commit, is not itself such a change".

The rule resolves the addition question for **layers** ("adding a layer" counts) and
resolves **dropping** ("not itself such a change"). It says nothing about adding a
top-level non-layer record. Reading (1) reads the third item as a set, parallel to
the first; reading (2) reads it as an individual record that must have existed before
and after. Both survive the words, and I searched §20.4, §20.5, §21.6 and §21.7 for a
resolver and found none — §21.7 confirms the opposite, listing this class of updater
obligation among those a single file exhibits no witness of.

**Why byte-level.** Given input file I and the instruction "add a file-scope
user-metadata record and drop this MU=0/PE=0 record", updater A (reading 1) emits X;
updater B (reading 2) must retain the record and emits X′. X is a *conforming file*
— but it is producible from I only by an appender in one commit, and only reading (1)
permits that. A creator emits generation 1 under a fresh file_id; a compactor emits a
different sequence entirely; a two-commit route yields generation n+2, not X. So under
reading (2) X is emittable by no conforming implementation and under reading (1) it is.
The directories differ by one 24-byte header plus inline payload, so the files differ
at trailer offset 32 (dir_length), offset 40 (committed_file_length), and in F.

**The premise, stated for attack.** Same as group 5: I take "which byte sequences a
conforming implementation may emit" to range over writer conduct, not only over the
conforming-file predicate. File conformance is a pure predicate on bytes (§2.3) and X
satisfies it either way; if the test is read as ranging over that predicate alone, this
drops to design-decision.

Implementer consequence, both sides concretely: team A honors the caller's "remove this
application record" in a commit that is doing plenty of other work, and the record's
extent becomes slack. Team B refuses, silently retaining application state its owner
asked to delete — in a product where deletion is a compliance operation, that is the
expensive branch. Neither can be told it is wrong by any verifier, since both outputs
are conforming files.

Repair: say explicitly whether adding a non-layer top-level record counts, as the rule
already does for adding a layer.

## Group 7 — `[R-MTA-10]`'s "counted and named, never silent" (verifier-02)

§8.1's map verified: "| Extent of a record of a type this specification has not
assigned | none — the bytes are opaque (§7.2) | — |". `[R-CNT-02]` verified: a record
extent is "the bytes any record's extent slot references, **whatever the record's
type**, §7.2" — so such bytes are a structure, not slack, and never enter `[R-CNT-21]`'s
slack total. §21.6 makes an experimental-range MU=0 record conforming. So the class the
reporter names is real and is certified while covered by no checksum and named by no
report. §22.3 concedes the exposure: "corruption inside it is equally invisible".

Byte-level: no, and the reporter is right about that. The operative MUST is expressly
scoped: "it MUST report each record it ignored **on this ground**" — the ground being an
unassigned *document encoding*, two sentences earlier. So reading (1) (a general duty
reaching unassigned record types) is not sustainable, and the defect is confined to the
trailing gloss, which is a false universal. Verdict, reader outcome and emittable bytes
are identical under both readings; only a report line moves. Editorial.

Implementer consequence: two verifiers emit different certificates for one conforming
file, and §22.3 tells an operator to build reject policy on that report line. Real
operator cost; no byte fork.

## Group 8 — "Compaction is barred on the same ground" (diagrams-01)

Cell verified at 3244. `[R-WRT-06]` verified at 3320–3322: "A compactor MUST refuse to
compact a file carrying **any record** whose type it does not implement with MU = 1:
such a type can define references this specification does not (§7.2), so its bytes
cannot be safely relocated."

The anaphor complaint is right — the sentence sits after two consecutive anaphors that
both point at the file-scope case, and the layer-scope sentence three clauses earlier
ends "leaving other layers editable". The reporter's second point is also right: "the
same ground" misdescribes `[R-WRT-06]`'s ground under either reading, which is unsafe
relocation of undeclared references, not reject-file.

Byte-level: no. The cell cites the rule, §21.1 says "where a row and the rule it cites
diverge, **the rule governs**", and `[R-WRT-06]` says "any record" without a scope
qualifier; §20.5 reinforces it ("an MU = 1 type the compactor does not implement never
reaches this step"). The document decides it in the section that owns the operation.
Editorial.

Implementer consequence: an implementer who stops at the table compacts a file carrying a
layer-scope unimplemented MU=1 sub-record — §21.6 says expressly that such a file is
conforming — and relocates an extent whose type may carry references it cannot see.
That output is barred by `[R-WRT-06]`, so the compactor is nonconforming, not the format
ambiguous.

## Group 9 — §21.6's sentinel row (diagrams-04)

`[R-TYP-08]` verified at 1819–1827: qualified to "sample positions **inside the layer's
extents**" and "for **each channel** the tile carries". §21.6's cell says "every sample
position it carries reads as **the channel's** fill". `[R-GEO-04]` verified: "a reader
MUST NOT return padding positions as samples." Both of the reporter's separating cases
check out against §14.5's own worked geometry (extents (5,5), tiles (4,4), edge tile with
1 real and 15 padding positions) and §13.3's three-channel Example.

Byte-level: no, and §21.1 says so twice, in advance: "where a row and the rule it cites
diverge, **the rule governs**" and, for §21.6 specifically, "§21.6's entries restate
their governing rules on the same terms a row does, and where such an entry and the rule
it cites diverge, the rule governs there too." Editorial.

Implementer consequence: a reader built from the table alone returns 16 samples where the
reference array holds 1. That is a genuine wrong-behavior path — but the document names
the precedence rule before the table, so the divergence is implementer error, not format
ambiguity.

## Group 10 — §21.1's specialization list omits the user-metadata extent rows (register-01, quiz-03)

F21, F22, F30, F31, L10, L11, L15 all verified verbatim. F21's slot (0,0) has
extent_length 0 < 5, so every F21 file is an F22 file; L10/L11 identical at layer scope;
quiz-03's F30 case (nonzero offset, zero length) likewise exhibits F22. §7.1's governing
text verified: "An extent of (0, 0) on a user-metadata record, **or** one whose
extent_length is less than 5 … is a validity error at its containing scope" — the second
disjunct carries no nonzero qualifier, so register-01's reading (a) is right and F22's
wording is not what is wrong.

Byte-level: no. Both rows are reject-file, same detector, same detection point, so no
reader or verifier verdict moves and `[R-CNF-05]` bars every conforming writer from
emitting such a file under either attribution.

I part company with register-01 on one point: §21.1's operative sentence is general, not
list-bound — "**a file exhibiting a specialization** is recorded against the narrower
row, whose detector and detection point are the ones that apply" — with "Some rows are
strict specializations of others" introducing three illustrations. So attribution *is*
resolved; what is missing is the naming that would let a corpus builder see the
obligation at the row. That is register bookkeeping: §21.8 requires "one vector per
instance", and F22's and L11's single instance is isolable only as extent_length in 1–4
with a nonzero offset, which no cell says.

Severity register-bookkeeping.

## Group 11 — R3/R4 overlap (register-02)

R3 and R4 verified verbatim at 3655–3656; §18.2's separating sentence verified at
2582–2586: "A mismatch is one of the frame constraints R4 registers, not a failure to
decode under R3: **the bytes decode**, and what is wrong is what the header said about
them."

The reporter is right on the headline. That separating criterion is stated for the
content-size mismatch and holds there; it does not hold for R4's first enumerated
instance (missing frame magic) or for the nonzero dictionary ID, where the bytes do *not*
decode and a reader that only tries decoding *does* establish a failure. R4's own clause
("a reader that only tries decoding establishes none of them") is therefore false for two
of its eight condition families, and the same file satisfies R3 verbatim.

Byte-level: no. All of §21.5 takes ignore-record, both rows are violations, `[R-CNT-25]`'s
quarantine fixes the reader outcome identically, and `[R-CNF-05]` bars the file either way.

Where I part company: attribution is not left open. §21.1's narrower-row rule applies —
for a magic-less encoding-2 extent, R4 is the strict specialization of R3 and is the row
recorded. What is defective is the *justification* R4 gives for the split, and the corpus
consequence (§21.8's "one vector per instance" for R4's magic-less instance cannot avoid
also exercising R3, so `[R-VEC-02]`'s non-isolable escape is what applies).

Severity register-bookkeeping.

## Group 12 — F21's "placing its document inline" (register-03)

§7.1 verified: a user-metadata record "carries its document in its extent — **never
inline** — and declares the document's encoding in its own inline payload (u8 …)".
`[R-MTA-03]` verified: "A user-metadata record's inline payload is exactly one byte", and
inline_length ≠ 1 is F23. So a slot of (0,0) with a conforming payload places the document
nowhere; the gloss describes an unrepresentable state, and a record that tried would be
F23, not F21. L10 carries the correct wording with no such clause.

Byte-level: no — §21.1's "the rule governs", and the record is reject-file under every
reading. Editorial.

## Group 13 — §21.4's outcome header (register-04)

Header verified: "Outcome: reject-tile — that tile's read reports failure, and never
returns fill in place of data (`[R-CNF-09]`)." `[R-CNF-09]` verified, and it is qualified:
"A reader MUST NOT return data as valid from a scope this specification rejects **and
whose rejection this reader is obliged to detect** (`[R-RDR-02]`)". T2, T4, T5 and T26 all
carry Detector *verifier* — confirmed by reading the rows. `[R-SER-08]` goes further for
T2: "A reader that neither detects the violation nor rejects the tile, and returns the
value, MUST report 0x00 as false and every other byte as true."

Byte-level: no. §21.1 states the resolution expressly: "For a row whose Detector is
*verifier*, the outcome names the scope at which the damage is recorded, not an obligation
on any reader: the governing rule states what a reader does" — and it names `[R-SER-08]`
by identifier as the one rule that resolves a byte rather than serving it through.
Editorial.

Implementer consequence: an implementer reading §21.4's header as governing its own rows
builds a reader that fails the read of a tile carrying an interleaved 0x02, where
`[R-SER-08]` licenses returning it as true. Both behaviors were already available to a
conforming reader via `[R-CNF-12]` on a nonconforming file, so nothing forks.

## Group 14 — Appendix G item 3's leading gap (adversary-02)

Sentence verified at 4405–4416. The reporter's reading (b) turns on "such gap" taking the
later-structure clause as antecedent and on the closing gloss's "between structures".

I grade this PARTIAL, because the item resolves it by citation and the reporter did not
run that step. Item 3 says the requirement is "`[R-CNT-03]`'s advice, **taken as a
requirement here**", and `[R-CNT-03]` verified reads: "Writers SHOULD zero the gaps they
create — **the run before an aligned tile or slab run**, and the pre-trailer pad." The
leading run [16, first_offset) exists precisely because the first structure is an aligned
tile or slab run, so it is the run `[R-CNT-03]` names, and importing that advice imports
it. The wording is loose; the profile's requirement is not open.

Byte-level: no, and not close. `[R-CNF-01]` exempts the appendix; `[R-CNT-21]` verified:
slack's "content is unconstrained, and no conformance requirement applies to it". Every
conforming reader and verifier treats both outputs identically. Editorial.

## Group 15 — `[R-MTA-10]`'s report scope (adversary-03)

`[R-MTA-10]` verified at 2668–2683. The subject two sentences up is "an encoding this
specification does not assign", which by `[R-MTA-03]` (verified) covers encoding 0, the
reserved range 3–0x7F **and** the experimental range ≥ 0x80. §22.3 verified: it says
"unassigned", not "experimental". §21.6's row and Appendix H (verified at 4543–4544:
"encoding 0 and the reserved range stay violations (R1)") state the duty only for the
experimental case. §21.5's preamble verified: "Encoding 0 and a reserved-range value are
unassigned too, and R1 registers both as violations: what `[R-MTA-10]` withdraws is the
document's content rules, never the encoding byte's own value set."

So the scope really is left open — "in an otherwise conforming file" can be read as "the
file is conforming apart from this record", which admits encoding 0. The reporter is right
that the two neighbourhoods disagree.

Byte-level: no. R1 makes the verdict *nonconforming* either way, `[R-MTA-03]` plus
`[R-CNT-25]` fix the reader outcome as ignore-record either way, and §2.3 decides the rest:
"that per-requirement report constrains the report and not the verdict". Editorial.

Implementer consequence: two conformance harnesses disagree about whether a report is
complete, and an operator following §22.3's recommended reject-on-that-line policy never
sees encoding-0 records enumerated. Report content only.

## Group 16 — §20.3 step 4's enumeration (quiz-02)

Bar verified at 3097–3106. I re-derived the reporter's case: reordering two interleaved
channels of equal element size with byte-identical fills leaves the padding position set
unchanged, `[R-SER-05]`'s content there unchanged, P·Q unchanged, every *sample*'s offset
(k div C)·Q unchanged, and codec and filter unchanged. What moves is Fᶜ, which §14.2
defines and the list does not name. So the enumeration genuinely misses it.

Byte-level: no. The paragraph subordinates its own list: "The test is the effect on such a
tile, and **the list names where that effect arises rather than standing on its own**", and
§14.1 `[R-SER-01]` fixes that "value k of the sequence is channel (k mod C)'s value at
in-tile ordinal k div C" — so the reordering alters how the superseded generation's stored
bytes decode and the general test bars it. §21.7 independently confirms the drafters have
this exact class in view: "a change … moving a sample's byte offset within the decoded
image without changing that image's length, is witnessed on the same terms T26 states".
Editorial.

Implementer consequence: an implementer taking the five items as the operative test emits
a commit no conforming updater may make, and every stored tile of the superseded generation
then decodes with two channels swapped — silent, and (per §21.7) unwitnessed where the
swapped channels' fills agree. The repair is one clause: name the byte offset of any
*channel's value*, or cite §14.1's value sequence.

## Byte-level tally

2 of 16 groups: appender-may-originate-flag-bit (writer-02),
pe0-drop-licensed-by-record-addition (writer-03).

Downgraded despite a reporter's byte-level flag: group 1 only (writer-01,
verifier-01), on `[R-CNF-10]` plus `[R-COD-08]`, with the leg-1 premise test
recorded above.

## Coverage check

all_input_ids_seen, counted against the brief's list of 23: reader-01, reader-02,
reader-03, writer-01, writer-02, writer-03, writer-04, verifier-01, verifier-02,
diagrams-01, diagrams-02, diagrams-03, diagrams-04, register-01, register-02,
register-03, register-04, adversary-01, adversary-02, adversary-03, quiz-01,
quiz-02, quiz-03. Union of member_ids across the 16 groups = the same 23, each
exactly once. No id dropped, none duplicated. No finding left unevaluated.
