# Triage pass: correctness lens — transcript

## Disclosure

- Runtime/environment note: the computed task text that invoked this run embedded the
  full text of all 67 input findings (ids, quotes, reasoning) directly in my context
  before I began any work. That material is disclosed here as *data supplied to me*,
  not as evidence I independently gathered. I did not treat any quote in the task text
  as authoritative; every quotation used below to decide a grade was re-fetched by me,
  in this session, directly from the two edition files on disk (paths below), via
  normalized substring search, and is separately shown in this transcript.
- Access actually used: I read only
  `/Users/robertkleffner/Documents/GitHub/tarn-first-draft/scratch/cleanroom/editions/a/tarn.md`
  and `.../editions/b/tarn.md`. I did not read any transcript-*.md file from the fidelity
  run's `out/` directory — the 67 findings' own stated quotes and reasoning (supplied in
  my task text) were sufficient to locate every passage in the two editions directly, and
  cross-checking those two edition files against each other is what the correctness lens
  asks for. I did not list any directory. I ran no command that reads any file outside the
  two permitted editions.
- Method: both files were copied verbatim into this scratch directory in two forms:
  `norm_{a,b}.txt` (blockquote `> ` markers stripped, line breaks kept) and
  `collapsed_{a,b}.txt` (all whitespace collapsed to single spaces, so a hard-wrapped
  sentence can be found as one contiguous substring). All searches below are against the
  collapsed files, via a small `search.py` helper that reports the surrounding ~200
  characters of context on each side of a match, plus a `NOT FOUND` report proving a zero
  when relevant. Scratch files written, all under
  `/private/tmp/claude-501/-Users-robertkleffner-Documents-GitHub-tarn-first-draft/fidelity-1/scratch/triage/`:
  `norm_a.txt`, `norm_b.txt`, `collapsed_a.txt`, `collapsed_b.txt`, `search.py`.

## Grouping and re-judging

Groups are listed with the ids they absorb, the passages checked in both editions (with
context), and the verdict. Full quotations appear in the structured output's
`location_a`/`location_b` and the group record; here I record the raw search evidence.

### G1 — ignore-lane "MUST NOT clear them" clause dropped (§6.3, R-CNT-08)
ids: cmp-reader-01, cmp-writer-06, cmp-verifier-06, swab-01, adv-05

A (collapsed, offset 48064): "...An updater MUST copy forward unknown ignore-lane bits
of its input file, MUST NOT clear them, and MUST NOT set any other: no writer under this
text originates an ignore-lane bit..."
B (same offset): "...An updater MUST copy forward unknown ignore-lane bits of its input
file, MUST NOT set any other: no writer under this text originates an ignore-lane bit..."
→ confirmed: the middle clause is gone in B.

But §6.2's trailer flags-field table row (offset 44050, IDENTICAL in both editions):
"...bits 16–31 (ignore lane) 0 from a creator, carried forward unchanged by every updater
(appender and rewriter alike), a set bit ignored (§6.3)". "Carried forward unchanged"
already forbids clearing a set bit — clearing it is not carrying it forward unchanged.
This sentence is untouched between editions and independently states the same obligation
§6.3's deleted clause stated. No implementation satisfying "copy forward"/"carried forward
unchanged" could clear a bit and still conform.
→ Verdict: EQUIVALENT. Not byte-level.

### G2 — appender step-2 "save where §20.4 licenses the drop" carve-out dropped
ids: cmp-reader-02, cmp-writer-02, cmp-verifier-03, swab-02, swba-01, adv-01

A (offset 168676): "...it MUST NOT repair the defect — [R-LIF-01] freezes the committed
prefix — and MUST NOT drop the record save where §20.4 licenses the drop."
B (offset 168651): "...it MUST NOT repair the defect — [R-LIF-01] freezes the committed
prefix — and MUST NOT drop the record."
→ confirmed: carve-out gone in B.

§20.4 (offset 185205/185133, IDENTICAL in both): "...so an appender MAY drop the record
in any commit it is otherwise free to make... and a rewriter MAY drop it in any rewrite."
This is an explicit, unqualified MAY-drop licence for the same actor (appender) and record
class (PE=0), stated later in the same section chain (§20.3→§20.4), with nothing in B's
step 2 signalling that its "MUST NOT drop" is anything but absolute. Unlike the ignore-lane
case, "MUST NOT drop X" does NOT entail "except where later licensed" — dropping the
carve-out is not a logical redundancy, it removes an actual exception, leaving B's step 2
in direct textual conflict with §20.4's MAY. An appender built strictly and literally from
B's step-2 instruction (an ordered algorithm step, "MUST, in order") has a real basis to
retain a record A's text (and B's own §20.4) would drop.
→ Verdict: LOSS, BYTE-LEVEL.

### G3 — worked example "32·20+4 = 664" (should be 644)
ids: cmp-reader-03, cmp-writer-05, cmp-verifier-04, swab-03, swba-02, adv-02, writerb-01

A (offset 179176): "...the layer's full new index region (32 · 20 + 4 = 644 bytes — one
entry re-pointed, 31 byte-identical)..."
B (offset 179116): "...the layer's full new index region (32 · 20 + 4 = 664 bytes — one
entry re-pointed, 31 byte-identical)..."
→ confirmed: A is arithmetically correct (32×20+4=644); B states 664, which is wrong.

The general formula, [R-CNT-16]'s clause "extent_length MUST equal entry_count × 20 +
⌈entry_count / 2¹⁶⌉ × 4" (offset 62201/62176) is byte-identical, unchanged, and correct in
both editions. §2.1's [R-CNF-01] (offset ~107, identical in both) makes any text "labeled
*Note*, *Example*, or *Rationale*" non-normative, and this passage is inside a "**Example.**"
block. An implementation built from either edition's actual normative sizing rule computes
644 for this scenario; only a human trusting the Example's own stated total, not the rule,
would be misled, and only in B.
→ Verdict: LOSS (B states an incorrect worked figure where A states the correct one — this
is a real, edition-specific content difference), but NOT byte-level: no conforming
implementation's emitted bytes or accept/reject verdict depends on this Example's own
printed total, since the governing formula is unchanged, correct, and normative in both
editions, and this passage is explicitly excluded from normative force in both editions.
Severity: content, not byte-level — several of the input findings (adv-02, swba-02)
over-claimed a byte-level effect via a hypothetical "conformance-vector author" who ignores
the normative formula; that is a claim about human error building fixtures, not about what
two correctly-built implementations of A vs B would each emit or accept, which is what the
byte-level test asks.

### G4 — MU=1 persistence-table row: "reaches only... unimplemented" flipped to "reaches every type, implemented or not"
ids: cmp-reader-04, cmp-writer-03, cmp-verifier-01, swab-04, swba-03, adv-03

A (offset 183855): "...Its MU = 1 row reaches only a type the updater does not implement —
...— so for an implemented type only the PE bit bites:"
B (offset 183795): "...Its MU = 1 row reaches every type, implemented or not —
...— so for an implemented type only the PE bit bites:"
→ confirmed. The trailing clause "so for an implemented type only the PE bit bites" is
verified byte-identical in both editions (offset 184102/184030) — so B's own sentence
states a premise ("reaches every type, implemented or not") that directly contradicts its
own unchanged conclusion ("for an implemented type only the PE bit bites" presupposes the
MU=1 row does NOT reach implemented types). A is internally consistent; B is not.
→ Verdict: LOSS, BYTE-LEVEL. An updater built from B's literal premise could treat an
implemented type's MU=1-flagged record as bound by the MU=1 row's "MUST NOT modify the
scope" obligation (refusing an edit A's/B's-own-conclusion-clause would permit under the PE
bit alone) — a genuine accept/reject divergence outside the two walk probes' tested
scenarios (both of which stipulate an unimplemented type, the one case both readings agree
on).

### G5 — "one sub-record blocks the drop" sentence deleted from the layer-drop paragraph
ids: cmp-reader-05, cmp-writer-01, cmp-verifier-02, swab-05, adv-06

A (offset 185688, extending into 185712): "...so a dropped layer's sub-records and their
extents go with it whatever their PE bits. One sub-record blocks the drop, a sub-record of
a type the updater does not implement with MU = 1, the drop being a modification of the
scope it governs (the table's first row). A commit never removes a user-metadata record..."
B (offset 185616): "...so a dropped layer's sub-records and their extents go with it
whatever their PE bits. A commit never removes a user-metadata record from a scope it
keeps..."
→ confirmed: the sentence is entirely absent from B.

But the table row it cites — "the table's first row" — is present, unchanged, in BOTH
editions, a few sentences earlier in the very same paragraph flow (offset 184295/184223):
"MU = 1 | Retain byte-identical. The updater MUST NOT modify the scope the record governs.
At layer scope an unknown critical record blocks modification of that layer, its drop
included, leaving other layers editable ([R-CNT-18])." A's own deleted sentence explicitly
names this as its source ("(the table's first row)"), i.e. A's text itself treats the
deleted sentence as a restatement/application of the general rule, not new content. The
"whatever their PE bits" sentence immediately before the gap talks only about PE, not MU,
so B is not left asserting anything that contradicts the MU=1 row — it is simply silent at
this specific point about the MU dimension, and the table row that answers it sits directly
above, in the same section, in the same edition.
→ Verdict: EQUIVALENT (the specific illustrative sentence is gone, but the general rule it
draws from — and cites by name — survives unchanged in B; the sentence of B that carries
what A's deleted sentence says is the unchanged MU=1 table row quoted above). This is a
closer call than G1: B's local paragraph reads more permissively taken in isolation, so I
flag it in the recommended action as a clarity regression worth restoring even though no
implementation-level divergence follows.

### G6 — register row F19's Instances cell: "flags bits 0-15" → "flags bits 0-7"
ids: cmp-reader-06, cmp-writer-04, cmp-verifier-05, swab-06, adv-04, readerb-02

A (offset 208398): "| F19 | Any bit of the flags incompat lane (bits 0-15) is set;
this text defines no flag bits, so every such bit is unimplemented | flags bits 0-15 |
reader | open | [R-CNT-08] |"
B (offset 208148): same Condition text, "...| flags bits 0-7 | reader | open |
[R-CNT-08] |"
→ confirmed: only the Instances cell narrows; F19's own Condition cell is untouched and
identical in both (bits 0-15), matching §6.2's table row and §6.3's prose (also confirmed
byte-identical above and separately at offset 47480: "a reader MUST reject-file on any set
bit it does not implement in the incompat lane (bits 0–15)").

§21.1's own precedence rule is present, unchanged, in both editions (offset 199800/199550):
"...each row *restates* its governing rule, and where a row and the rule it cites diverge,
**the rule governs**." F19's governing rule is [R-CNT-08], unqualified across bits 0-15 in
both editions' §6.3 prose. So a reader built correctly and completely from either edition
(i.e. applying §21.1's own stated precedence, not just mechanically reading one cell of one
register row) rejects a file with any incompat-lane bit 0-15 set, including bit 10,
regardless of edition.
→ Verdict: LOSS (an edition-specific defect: B's register row is self-inconsistent and its
own stated Instances/coverage-vector promise for F19 no longer covers bits 8-15, a genuine
content difference from A), but NOT byte-level — adv-04's constructed-file argument assumes
a verifier that reads the Instances cell only and ignores §21.1's explicit precedence
clause and §6.3's own prose; that is an incompletely-built implementation of B, not "an
implementation built from B alone" in the sense the byte-level test asks (which is the
totality of B's normative text, including §21.1's tie-breaker). Severity: content (register
internal-consistency / corpus-coverage defect), matching cmp-reader-06's and readerb-02's
own conclusion; swab-06's and adv-04's byte-level claims are downgraded.

### G7 — writera-01's zero-copy drop-and-recreate ambiguity (shared, unchanged text)
ids: writera-01, cmp-writer-07

Both: "...a commit MAY drop the layer (§20.4) and add a new one under its name and other
declarations, the new layer being new whatever bytes its entries address, the dropped
layer's former extents included, §5.2's partition being over the new state alone." —
confirmed byte-identical at offset 173282 (A) / 173222 (B).
→ Verdict: EQUIVALENT. The ambiguity, if real, is present equally in both editions; it is
not a divergence between them, so it is not gradable as a LOSS or ADDITION between A and B.

### G8 — writera-02's cross-layer slab-recheck ambiguity (shared, unchanged text)
ids: writera-02, cmp-writer-08

Both: "Structures the commit neither modifies nor relies on impose no further obligation.
[R-WRT-03]" — confirmed byte-identical at offset 167481 (A) / 167456 (B).
→ Verdict: EQUIVALENT, same reasoning as G7.

### G9 — verifiera-01 + verifiera-02 (single-edition observations, confirmed present in B too)
ids: verifiera-01, verifiera-02, cmp-verifier-13

verifiera-01's §2.3 cannot-establish text ("Cannot establish is not a finding that the file
is nonconforming, and a verifier MUST NOT certify a file it reports that way...") is
byte-identical in both editions (confirmed at offset 11963, both). verifiera-02's §21.1
"this list is not offered as closed" is byte-identical in both (confirmed at offset
200537, both).
→ Verdict: EQUIVALENT. Both are genuine properties of the specification's design, but they
are present, identically, in edition B as well as A — not something A decides that B
doesn't, so they are not a fidelity divergence.

### G10 — verifierb-01 + verifierb-02 (single-edition observations, confirmed present in A too)
ids: verifierb-01, verifierb-02, cmp-verifier-14

verifierb-01's §5.2/§9.7 coverage-walk partial-trigger list, and verifierb-02's §20.3
step-4/§9.7 fixed-declaration-bar-undetectability text, are both confirmed byte-identical
in both editions (offsets 82612/38263 region, and 171892/168676 region respectively).
→ Verdict: EQUIVALENT, same reasoning as G9.

### G11 — readera-01 / readerb-01: no outcome class for a reader lacking a core codec
ids: readera-01, readerb-01

§17.4/R-COD-11's "cannot execute a layer's codec or filter" text and §2.3's R-CNF-03 "is
not a conforming reader" text are both confirmed byte-identical between editions (offsets
9369 and 136939/136914). Both walker-a and walker-b raise essentially the same observation
about the same, unchanged text.
→ Verdict: EQUIVALENT. Whatever gap exists, it exists identically in both editions; it is
not a fidelity divergence between A and B.

### G12–G17 — cmp-verifier-07 through cmp-verifier-12 (V1–V6 confirmations)
ids: cmp-verifier-07 (G12), cmp-verifier-08 (G13), cmp-verifier-09 (G14),
cmp-verifier-10 (G15), cmp-verifier-11 (G16), cmp-verifier-12 (G17)

Spot-verified V1 (§2.3 verdict vocabulary, "MUST NOT certify a file it reports that way",
offset 11963, identical) and V2 (§21.2 F35/F36 rows, offset 212083/211832, identical). V3
rests on the same unchanged R-CNT-17 formula verified for G3. V4 rests on the same §17.4
text verified for G11. V5 rests on the same §20.3 step-4 / §9.7 text verified for G10. V6
rests on §7.2's [R-CNT-12] MU=1/PE=0 combination rule, part of the same persistence-table
region already spot-checked as unchanged around G4/G5's citations.
→ Verdict for each: EQUIVALENT. Each is a same-text, same-conclusion confirmation across
two independent walks; not a fidelity divergence.

### G18 — quiza-06: layer empty + refill + fill-value-change in one commit
id: quiza-quiza-06

Both takers' cited passages are confirmed byte-identical between editions: the "does not
earn an empty layer's freedom" sentence (offset 172903/172843) and the "the change is a new
layer, or a rewrite" sentence (offset 171892/171832). Since the text is identical, the
takers' differing answers cannot be an edition difference. Reading the shared text: "...a
commit MAY drop the layer (§20.4) and add a new one under its name and other declarations"
is stated within §20.3 (the append procedure) discussion — i.e. drop-and-recreate under the
same name, with fresh declarations including a fresh fill value, is achievable by an
ordinary appender commit. The taker who concluded "not a valid appender commit; requires
... a whole-file rewrite" over-reads the text; the taker who concluded "requires declaring a
new layer" (achievable via that same commit) matches it.
→ Verdict: REPORTER_ERROR — the two editions say the same thing; one taker misread it.

### G19 — quiza-09: entry_count / index-region size arithmetic
id: quiza-quiza-09

Both takers give the identical numeric answer (210000, 4200016) with high confidence and
the same reasoning. The cited formula text, "Under index_encoding 1, extent_length MUST
equal entry_count × 20 + ⌈entry_count / 2¹⁶⌉ × 4", is confirmed byte-identical in both
editions (offset 62201/62176) — one taker's citation simply dropped the "Under
index_encoding 1," lead-in when excerpting, which is a citation-length artifact, not a text
difference.
→ Verdict: EQUIVALENT. No misread occurred and no edition difference exists; this was a
false positive of the mechanical diff that flagged the slate.

### G20 — quiza-13: rewriter's two dispositions on a structural reject-tile entry
id: quiza-quiza-13

Both takers quote the identical sentence verbatim ("[R-WRT-06] then leaves it two
disposals... drop the layer... or refuse.") and reach the same substantive conclusion
(dropping reclaims slack; refusing does not). No edition difference and no misread.
→ Verdict: EQUIVALENT.

### G21–G26, G28–G31 — quizb items with converging answers on identical text
ids: quizb-quizb-01 (G21), -02 (G22), -03 (G23), -05 (G24), -06 (G25), -07 (G26),
-09 (G28), -10 (G29), -12 (G30), -15 (G31)

For each, I located the cited passage in both editions and confirmed byte-identical text:
- 01: "MUST NOT declare this codec for a layer any of whose addressed tiles' decoded size
  exceeds 0x7E000000 bytes ... and a reader MUST treat such a declaration as a validity
  error at layer scope" — identical in both (offset 132631/132606); the "FROM A" quote in
  the finding was simply truncated before this clause, which is present in A too.
- 02: "A reader that would have to issue a further range request to obtain those bytes MAY
  defer or omit the check" — identical (offset 42673, both).
- 03: "Under index_encoding 1, extent_length MUST equal entry_count × 20 + ⌈entry_count /
  2¹⁶⌉ × 4" — identical (same as G19).
- 05: fill-byte/padding rule (§14.5, §4.1 little-endian) — cited identically by both takers,
  same numeric answer (21 padding positions, EF BE).
- 06: "in a planar layer exactly the entry's channel reads as fill there, and a single
  sample can mix decoded and fill channels" — quoted identically by both takers.
- 07: "for a packed boolean plane s = 1 and the filter is the identity" — quoted identically.
- 09: "Such an entry contributes no stored extent to the *verifier* rows... and none to
  [R-LIF-08]'s coverage walk" — identical (offset 117242/117217).
- 10: planar channel-list insertion-in-middle rule — quoted identically by both takers.
- 12: "A reader MUST validate, in order: the trailer magic; the trailer CRC; the version
  gate (§6.3)..." — identical (offset 45394, both).
- 15: "One space carries no experimental range: channel layout..." — quoted identically by
  both takers.
→ Verdict for each: EQUIVALENT. In every case the underlying text is identical between
editions and the two takers' final answers converge; the "answers differ" flag was a
mechanical artifact of differing citation length/paraphrase, not a substantive divergence.

### G27 — quizb-08: coverage-walk verdict/slack-total when a tile decode is declined on resource grounds
id: quizb-quizb-08

Both takers' passages are confirmed byte-identical between editions (offset 82612/38263-
region: "Where the walk does not complete — a scope-level rejection blocks enumeration, the
verifier declines a LAYER on resource grounds and so never enumerates its claimants
([R-ERR-04]), or it stops at the first violation ([R-CNF-11]) — the sum is reported as
partial..."), AND, critically, a further clause a few hundred characters earlier in the same
paragraph, also confirmed byte-identical in both editions (offset 38415/40645-region):
"...a tile's or a document's decode declined leaves the walk complete, that claimant being
enumerated from its index entry or extent slot." This explicitly distinguishes a *layer*
decline (→ partial) from a *tile's* (or document's) decode decline (→ walk stays complete).
The probe specifies "a layer whose stored-tile decode it declines" — i.e. a tile-level
decode decline — which the text says leaves the walk complete, not partial.
→ Verdict: REPORTER_ERROR. Both editions state the tile/layer distinction identically; the
taker who answered "partial" (slate A) missed this clause; the taker who answered "complete"
(slate B) applied it correctly. This is not an edition difference.

## Coverage check

All 67 input ids are assigned to exactly one of the 31 groups above (6+8+14+6+3+6+3+3+4+3+11
member counts sum to 67, verified against G1–G31's member lists; cross-checked against the
original 67-id list with no id repeated and none omitted).
