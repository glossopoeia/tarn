# refute-G8 — unreadable-sweep — working transcript

## Disclosure

Read: the two briefs (finding-A-06.md, finding-X-06.md), hunk-01.diff,
hunk-02.diff, and spec/tarn.md. Nothing else. Did not read full.diff, other
hunk files, docs/, conformance/, registry.json, git history. Did not list the
r23audit directory.

Unbidden context appeared before I began: a project instruction pointer
(CLAUDE.md -> AGENTS.md) and an index of the maintainer's memory notes with
titles referencing this project's cadence and prior-round shapes. I did not
open any of it and drew no conclusion from it. Disclosed, not used.

Commands run: sed reads of spec/tarn.md at the line ranges below; two python3
scripts over spec/tarn.md only (whitespace-normalising grep, and a register
row/instance counter); one line-oriented grep for `R-COD-06` and one for the
CNF identifiers. Exact outputs reproduced below.

## Passages read in full

- spec/tarn.md 145-235  (§2.3 [R-CNF-02]..[R-CNF-11], §2.4 [R-CNF-07])
- spec/tarn.md 870-900  (§7.1, [R-CNT-11], [R-CNT-25])
- spec/tarn.md 2255-2300 (§17.2 codec 3, [R-COD-06] and its Note)
- spec/tarn.md 2400-2520 (§18.1 [R-MTA-01]/[R-MTA-02], §18.2 [R-MTA-03],
  [R-MTA-09] entire, its Note, the four content restrictions)
- spec/tarn.md 2554-2559 ([R-MTA-05])
- spec/tarn.md 3290-3345 (§21.1 entire)
- spec/tarn.md 3516-3554 (§21.5 preamble + all ten rows)
- spec/tarn.md 3554-3640 (§21.6, §21.7)
- spec/tarn.md 3655-3670 (§21.8 [R-ERR-02])

## Grep 1 — hard-wrap check

`grep -n "no dictionary use\|not part of the register\|None of these is a
requirement\|capability or resource ground\|Any violation here is\|every frame
constraint" spec/tarn.md` returned only:

```
214:  capability or resource ground, naming the requirement and the
2280:disclose is not detectable by inspection and need not decode to
2458:before its terminal CRC, under every frame constraint `[R-COD-06]`
2500:`[R-MTA-10]`'s subject, not a decline. Any violation here is
```

i.e. "no dictionary use", "not part of the register", "None of these is a
requirement" all returned NOTHING line-oriented — every one of them spans a
wrap. Confirms the charter's warning. All subsequent searching was done over a
whitespace-normalised join of the file with a char-index -> line map.

## Grep 2 — normalised sweep of the TERMS (not identifiers)

Patterns: `unreadable`, `content-size`, `content size`, `Frame_Content_Size`,
`fail to decode`, `fails to decode`, `failure to decode`, `failure to read`,
`dictionary`, `ignore-record`, `preserve-verbatim`.

Every hit for `unreadable`: L887, L889, L1661, L2516, L2521, L2525, L2536,
L2541, L2557, L3526.
Every hit for `failure to decode`: L2475, L2482 — both inside the repaired
§18.2 paragraph, both current text. **No stale restatement of the old "a
mismatch is a failure to decode within the meaning of R3" survives anywhere
else in the document.** R3's row text (L3545) contains no content-size
reference. The term-level sweep of hunk 1's own change is therefore clean.

Third enumeration of unreadability found that neither brief names: §18.2
L2516, "Four restrictions apply, and a document violating any of them is
unreadable". Consistent with [R-CNT-25]'s fourth ground; not disturbed.

## Local computation — §21.8 arithmetic

Hunk 2 grew R4 from 12 instances to 16. §21.8 [R-ERR-02] (L3663-4) states
"Every row of §21.2 through §21.5 — 121 conditions over 277 instances". I
counted the register myself (python over spec/tarn.md alone; a cell of "—"
counted as one instance, otherwise semicolon-separated):

```
21.2 rows 36 instances 58
21.3 rows 49 instances 116
21.4 rows 26 instances 55
    R1 4  R2 2  R3 2  R4 16  R5 8  R6 4  R7 6  R8 2  R9 2  R10 2
21.5 rows 10 instances 48
TOTAL rows 121 instances 277
```

277 = 277 and 121 = 121, with R4 at 16. §21.5's own "10 conditions." (L3539)
also holds. The repair swept the arithmetic. This closes the most obvious
unswept-restatement candidate in hunk 2's neighbourhood and is evidence the
sweep was done deliberately, not left to chance.

---

## Finding A-06

### The claim under test
§18.2's carry-over newly imports "no dictionary use, disclosed or not" into
user metadata, creating an undetectable violation class; §21.7's account of the
undetectable class speaks only of "wrong sample values", so the class falls
into no account and "the document's stated completeness scheme has a hole".

### Facts confirmed
The widening is real. Hunk 1 shows the replaced text scoped the carry-over to
"the frame constraints of `[R-COD-06]` that do not reference a tile", followed
by a closed colon-list of four. [R-COD-06]'s bar is phrased "Writers MUST NOT
compress **a tile** using a dictionary" (L2276-7) — it references a tile, and
was not in the closed four. It is now carried (L2464). §21.7's illustration
(L3612-4) is indeed sample-scoped.

### Constructions built

**C1 — the verifier verdict route (the strongest one, and neither brief nor
verdict took it).** If the metadata undisclosed-dictionary bar is outside
§21.7's account, then §21.7's closing disclaimer ("None of these is a
requirement a verifier is *unable to check* within the meaning of
`[R-CNF-11]`") does not reach it. A verifier by definition "checks every
file-level requirement". It cannot check this one. If that made it an
unchecked requirement, [R-CNF-11] would force *cannot establish* on **every**
file carrying an encoding-2 user-metadata document, and [R-CNF-11] also says a
verifier MUST NOT certify a file it reports that way. Two verifiers reading
only this document would then differ on an actual accept/reject verdict over
identical bytes. That is byte-level in the charter's sense.

**C1 fails on [R-CNF-11]'s own quantifier.** L204-206: *cannot establish* is
"the last where some requirement is one it is unable to check **on a
capability or resource ground**". L213-215 repeats the qualifier for the
report obligation: "A verifier MUST report each requirement it was unable to
check **on a capability or resource ground**". An undisclosed dictionary is
neither a capability ground nor a resource ground — the verifier is perfectly
capable and there is simply no witness in the file. So even a verifier that
never reads §21.7 reaches *conforming*. Both readings converge; the verdict
does not move, and the per-requirement report does not move either. C1 dead.

**C2 — the writer's emittable set.** Does §21.7's silence license a writer to
compress a metadata document against an undisclosed dictionary? No. The bar is
stated in §18.2 (L2464), not in §21.7. [R-CNF-02]'s conduct carve-out — the
one place a writer obligation is declared not to be a file-conformance
violation — names its cases: "§6.3's flags = 0 against a set ignore-lane bit
and §6.2's pre-trailer gap longer than `[R-LIF-02]` step 5's pad are the cases
this text states" (L152-155). Dictionary use is not among them, and [R-COD-06]
classes it instead as "a writer violation" (L2281). So under both readings
[R-CNF-05] bars the file. Emittable set does not move. C2 dead.

**C3 — the reader's detect obligation.** [R-CNF-04] (L173-6) obliges a reader
to detect "every violation the error register (§21) assigns to the reader as
its detector". R4 carries no instance for it, under either reading, because no
reader can detect it. Both readings: no obligation, no reject. C3 dead.

**C4 — register completeness as an obligation on bytes.** §21.1's completeness
clause is quantified over *detectable* violations, and §21.1 L3323-3327 then
withdraws it from §21.7 entirely: "The subsections after §21.5 are not part of
the register and carry no rows: neither this completeness clause nor the
instance arithmetic below reaches §21.6's defined non-violations, §21.7's
account of what no check detects, or §21.9's limits." Even granting the
auditor that §21.7 under-describes, an implementer who concluded the register
had a hole still could not detect the condition, still could not emit it, and
still would certify. C4 dead.

**C5 — does §18.2 import [R-COD-06]'s undetectability characterisation?**
Strictly it imports "every frame constraint", and a characterisation is not a
constraint. But undetectability here is a fact about zstd frames, not a
stipulation: with Dictionary_ID zero there is no witness, in a metadata extent
exactly as in a tile extent. Any implementer reaches it from the bytes. And
nothing normative hangs on the label — C1 through C4 show every downstream
obligation is fixed by other text. C5 dead.

### Verdict on A-06
Not byte-level. Downgrade stands. The residual is real but inert: §21.7's
appositive illustrates its class with "wrong sample values", narrower than the
class statement one sentence earlier (L3610-2, "this format detects
*corruption of structure*, not *incorrectness of content*"), which does cover a
metadata document. If either text changed it should be §21.7, not §18.2. It
licenses no implementation behaviour either way.

---

## Finding X-06

### The claim under test
The repair created a user-metadata violation that is not a way the document is
unreadable, and left [R-CNT-25] (L888-893) and the §21.5 preamble (L3525-7)
standing as enumerations that now under-describe their class; the ignore-record
grant survives "only because §18.2's untouched closing sentence says 'Any
violation here is ignore-record' — an accident of an unrelated sentence, not
the rule the row cites".

### Premise 1 tested: is the sentence unrelated, and is it not the cited rule?
No, twice. L2500-2501: "Any violation here is ignore-record, never the
tile-scope outcome §17.2 assigns. `[R-MTA-09]`" — that identifier closes the
very §18.2 paragraph that states the content-size MUST (L2477-2482), and R4's
Governing rule cell is `[R-MTA-09]` (R-COD-06, R-CNT-25). It is the cited rule,
and it is the same paragraph. Not a blockquote; [R-CNF-01] not in play.
Premise refuted on the document's own text.

### Premise 2 tested: did the repair CREATE this class?
No — and this is the part I could settle independently of the verdict I was
asked to attack. R4's instance list contains, **untouched by hunk 2**, "the
content-checksum flag set, top-level extent" and "bytes remaining after the
frame, top-level extent". A zstd frame with Content_Checksum_flag set decodes
its content perfectly; the document is readable; it is nonetheless an R4
violation carrying ignore-record. So §21.5 already held rows that are not
unreadability, and [R-MTA-09]'s closing sentence was already what carried them.

Corroboration the briefs did not cite: [R-MTA-05] at L2556-8 — "unsorted
members do not make a document unreadable: the file is nonconforming, a
verifier MUST report it, and readers process the document unchanged." The
document already treats "unreadable" as a narrower defined term than
"user-metadata violation", expressly. (F27/L48 register that one outside
§21.5, so it is not itself a §21.5 counterexample — the content-checksum flag
is.)

### Premise 3 tested: are the two enumerations falsified?
Both are one-directional. [R-CNT-25]: "each way ... can be unreadable ... is
ignore-record" — unreadable => ignore-record. §21.5 preamble: "every way its
document can be unreadable takes this outcome ... as a violation in the rows
below" — same direction. Neither says ignore-record => unreadable. A condition
outside the antecedent leaves them silent, not wrong. The preamble's own next
universal is over rows, not over unreadability: "Every row here is a violation
all the same" (L3536-8) — the authors already hold the two classes apart.

### Constructions built for byte movement

**C6 — the layer sub-record scope escape (the charter's "different actor /
different scope" move).** Suppose an implementer reads [R-CNT-25]'s four
grounds as closed, finds a content-size mismatch outside them, and falls back
on §2.4 owning-scope mapping ([R-CNF-08]). For a **layer sub-record**
user-metadata document that yields reject-layer: reader A returns the layer's
tiles, reader B refuses the whole layer. That is a real accept/reject
divergence on identical bytes — the sharpest construction available here.

**C6 fails on three independent normative supports, any one sufficient.**
(i) [R-MTA-09] L2500-1, unqualified: "Any violation here is ignore-record" —
"here" is §18.2, which is where the content-size MUST is stated.
(ii) §21.5's section-level assignment, L3520-2: "Outcome: ignore-record — the
record is skipped as though absent", governing every row including R4.
(iii) §21.1 L3301-3: rows take "the outcome class its scope determines (§2.4)
— except where a rule assigns one expressly", and [R-MTA-09] assigns expressly.
Also [R-EXT-03] L1429 and [R-ENC-11]/[R-ENC-12] L481/L488 invoke the quarantine
by name as "never a scope-level rejection". C6 dead.

**C7 — slack / superseded (the charter's first suggested move).** Put the
offending user-metadata record outside the live state: logically deleted,
bytes become slack ([R-CNT-21], §21.6 "Slack: unconstrained content, no
conformance requirement"). Then no row fires — but that is true under BOTH the
R3 reading and the R4 reading, identically. The move does not separate the two
readings; it only removes the condition. C7 dead.

**C8 — writer side.** Can either reading let a writer emit a mismatched
content-size field? No. §18.2 L2477-9: "it MAY be present, and when present it
MUST equal the byte length of the decoded document." A MUST on the bytes;
[R-CNF-02] makes the file nonconforming; [R-CNF-05] bars every conforming
writer. Under both R3 and R4 the file is nonconforming and unemittable. The
emittable set does not move. C8 dead.

**C9 — updater / appender.** preserve-verbatim (L241) carries the bytes forward
unmodified regardless of which row classifies them; §20.4's obligations do not
branch on R3-vs-R4. Swept `ignore-record` and `preserve-verbatim` normalised
across the whole file (outputs above) — no rule anywhere conditions an actor's
obligation on whether a user-metadata defect is a *decode failure* as against a
*frame constraint*. C9 dead.

**C10 — lenient decoder.** RFC 8878 decoders need not verify content size.
Under the old text the mismatch was stipulated a decode failure, so a lenient
decoder had to treat it as R3 anyway; under the new text it is R4. Both rows:
detector reader, detected extent use, outcome ignore-record. Identical
behaviour. C10 dead.

### Verdict on X-06
Not byte-level, and its load-bearing factual premises are false on the
document's own text (the sentence is the cited rule and is in the same
paragraph; the not-unreadable class predates the repair). Downgrade stands.

If either text were to change it is [R-CNT-25] and the §21.5 preamble, not
§18.2 — the auditor's proposed direction is right even though the finding is
not. But nothing normative rides on it: the outcome is assigned three times
over and the two sentences are one-directional universals that a non-member
does not falsify.

---

## Overall

Both downgrades stand. No construction I could build separates two conforming
implementations on bytes emitted or on an accept/reject verdict, for either
finding. The document answers both from its own text — §21.1 L3323-7 and
[R-CNF-11] L204-6/L213-5 for A-06; [R-MTA-09] L2500-1, §21.5 L3520-2 and
§21.1 L3301-3 for X-06 — so neither is a case of reasoning that lives only
outside spec/tarn.md. No missing sentence.
