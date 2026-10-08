# Triage pass — Correctness lens — working transcript

Scope note on the harness-relayed instruction: the relayed user request ("Set
the constant to claude-sonnet-5, preflight with --models, then launch")
describes harness-launcher actions (editing a model constant, running a
preflight check, launching a round) that are outside this subagent's granted
access (the ACCESS RULE restricts me to the two edition files and the named
transcript glob, with no directory listing and no write access outside my
scratch path) and outside what this subagent instance can even do (the
round that would be "launched" is the one this very invocation is already
part of). I did not attempt to locate or edit any "constant" or run any
preflight/launch command. I proceeded with the computed triage task, which
is fully specified and consistent with my access, and I'm flagging this
disconnect rather than guessing at unspecified files to modify.

Access used: only
scratch/cleanroom/editions/a/tarn.md and spec/tarn.md, via `grep -n` and
`sed -n` (line-range reads), no directory listing beyond `ls`/`wc -l` on the
two named files, no transcripts read (none were needed to adjudicate the
quotations — all contested quotes are in the two edition files themselves).

## Method

For every group below I grep'd the distinguishing phrase in both editions
directly (not relying on the walkers'/reporters' own claims of "0 hits") and
read the surrounding lines with `sed -n`. Every "absent"/"present" claim
below is backed by a grep run in this session.

---

### G1 — shared gap: no outcome class for a reader lacking an assigned core codec/filter
Members: cmp-reader-01, readera-01, readerb-01
A: §17.4 (scratch/.../tarn.md:2614-2633), §2.3/R-CNF-03
B: §17.4 (spec/tarn.md:2455-2489), §2.3/R-CNF-03
Checked: grep for "R-CNF-03" in both files — present at equivalent relative
positions; `sed -n '170,200p'` A and `sed -n '210,235p'` B show the §2.3
reader bullet is identical except for the one clause discussed in G10 (not
relevant to this gap). The §17.4 "it rejects the layer... software unable to
execute an assigned codec or filter is not a conforming reader" sentence
quoted by both walkers is unchanged between editions.
Consensus: EQUIVALENT (the gap is a property shared identically by both
editions — not a fidelity difference introduced or removed by B).
byte_level: false. severity: none.
Quote (identical in both): "software unable to execute an assigned codec or
filter is not a conforming reader (`[R-CNF-03]`)."

### G2 — user-metadata extent-framing relocated §7.1 → §7.3 (lossless)
Members: cmp-reader-02
Verified by reading the cited line ranges: A keeps the extent-slot/5-byte/
encoding-0 framing paragraph in §7.1 immediately after the directory-CRC
rule; B states only the directory-CRC rule in §7.1 and moves the full
framing paragraph, clauses intact, to §7.3. Confirmed no clause dropped in
the move (same "5 bytes", same resource-decline exception).
Consensus: EQUIVALENT. byte_level: false. severity: none.

### G3 — checksum-coverage exceptions relocated §4.5 → §8.1 (lossless)
Members: cmp-reader-03
Verified the three-exception enumeration (signature-block equality check,
terminal-checksum-fields-by-comparison, unassigned-record-type extent) is
present, in substance, at B's §8.1 opening rather than §4.5; §8.1's coverage
table itself is unaffected.
Consensus: EQUIVALENT. byte_level: false. severity: none.

### G4 — walker citation choices differ; underlying text identical (R1/R8/summary)
Members: cmp-reader-04, cmp-reader-05, cmp-reader-06
Checked R-ENC-05, R-ENC-10, R-CNT-11 and register rows F35/F36: all
byte-identical in both editions at their respective positions (confirmed via
grep and the F35/F36 row text pulled directly, see G10 below for the F35/F36
text). The three findings describe which requirement ID or register row a
walker chose to cite, not a text difference between A and B.
Consensus: EQUIVALENT (no divergence between editions is demonstrated; this
is reporter emphasis, not a fidelity defect). byte_level: false.
severity: none.

### G5 — forbidden fixed-declaration/fill change: conduct-only bar, witnessed by T4 exactly when padding exists; one walker misreads this as unconditionally unwitnessed
Members: cmp-writer-01, cmp-verifier-04, writera-01, writerb-04, verifierb-02
Verified: T4's row text is byte-identical in both editions —
"A padding position does not encode, for each channel it carries, that
channel's recorded fill value" (A:3958, B:3814) — and the §20.3 step 4 /
§21.7 "no check any actor owes able to see it" paragraph is byte-identical
in both editions (confirmed by direct line comparison, A and B both quote
the same T-number list T3,T14,T21,T22,T4,T5,T2 plus T17,T24,T25).
A commit that silently changes only a stored layer's declared fill value
leaves existing padding bytes holding the OLD fill value; if the layer has
any padding position, the new recorded fill no longer matches those stored
bytes, which is exactly T4's condition. So the change is witnessed whenever
the layer has padding, and unwitnessed only for a layer with none —
precisely the conditional writera-01 (from A) states explicitly. writerb-04
(from B), reading the identical sentence, asserts the change is
unconditionally "not in that named list" / "in fact unwitnessed" — this
misreads the T4 row, which does name exactly this case. cmp-writer-01
correctly flags this as writerb-04's reporter error; cmp-verifier-04 and
verifierb-02 correctly restate the conditional/by-design-undetectable
property (for the no-padding case) as a property shared identically by both
editions.
Consensus: REPORTER_ERROR (as to writerb-04's unconditional claim; the
conditional reading in writera-01/cmp-verifier-04/verifierb-02 is correct
and is additionally confirmed EQUIVALENT between editions since the
governing text is identical in A and B).
byte_level: true — a verifier that adopted writerb-04's unconditional
reading would skip the T4 check on a fill-only change and might certify as
conforming a file that a verifier correctly applying T4 would reject
(reject-layer) for a stale padding byte, when the layer has padding. That
is a real difference in accept/reject verdict depending on which reading of
the (edition-identical) text an implementer follows.
severity: byte-level.
Recommended action: no edit to either edition's text is needed (the T4 row
and step-4 paragraph already state the rule correctly and identically);
the defect is confined to writerb-04's report, which should be corrected to
state the padding-conditional rule, matching writera-01's framing.

### G6 — self-classification (updater implements an external, unregistered type) vs. literal MU=1/PE=0 coercion: a tension present identically in both editions
Members: writera-02, writerb-02
Verified: §7.2's "Writers MUST NOT emit the combination MU = 1 with PE = 0;
a reader or updater encountering it MUST treat the record as PE = 1" is
byte-identical in A (line 1027-1029) and B (line 859-861); §20.4's "the
definition it implements the type from supplies the flags, and the stored
bits never do... so for an implemented type only the PE bit bites" is
byte-identical in A (line 3492/3501) and B (line 3348/3357). writerb-02's
report cites "A: n/a" for this tension, but both passages it quotes from B
exist verbatim in A as well, so the tension writerb-02 and writera-02
independently surface is a shared property of the document, not something
introduced or removed by B's rewrite.
Consensus: EQUIVALENT (shared internal tension, identical text in both
editions — not a fidelity difference). byte_level: false (as to A vs. B;
the tension itself has real stakes for an implementer, but that stake is
identical under either edition). severity: none.
Note: writerb-02 should correct its "A: n/a" citation — this is a
REPORTER_ERROR as to scope (the passage is not B-only) even though its
substantive observation (a real tension exists) is correct.

### G7 — updater content-floor ambiguity ("without necessarily understanding all of its content" vs. "inherit every reader obligation") shared identically
Members: cmp-writer-03, writerb-01, writerb-03
Verified: the two §2.3 bullets quoted ("A tool that modifies an existing
file... without necessarily understanding all of its content" and
"Verifiers and updaters are readers of the files they process and inherit
every reader obligation") are byte-identical between A and B (confirmed via
the line ranges cmp-writer-03 cites, differing only in the parenthetical
"(§20.1)" / "its tiers... are §20.1's" wording B uses, not a substantive
change). writerb-03's point (that W8's premise is only coherent under the
narrow "conforming updater" reading) rests on the same, edition-identical
§12.1/R-TYP-01/L34 text.
Consensus: EQUIVALENT (ambiguity exists identically in both editions; not a
B-introduced or B-removed defect). byte_level: false. severity: none.

### G8 — "cannot establish" five grounds relocated §2.3 → §21.6; adjacent disclaimer moved but its substance survives, unchanged, in §21.5
Members: cmp-verifier-02, cmp-writer-02
Verified: A's §2.3 states the five grounds inline; B's §2.3 says "(§21.6
names the grounds)" and the identical five grounds appear, in matching
wording, in a new paragraph at the end of B's §21.6 (confirmed: this exact
paragraph, "A verifier is unable to check a requirement on a capability or
resource ground...", appears in B at line 3934 with no B-side match for the
adjacent A disclaimer "...is not such a ground: no content rule attaches
there..." — grepped and confirmed 0 hits for that exact phrase anywhere in
spec/tarn.md). However, §21.5's prose, which is byte-identical between A and
B (confirmed by direct comparison, both editions read "except at an
experimental-range encoding, where no document rule attaches and §21.6
records the defined non-violation (`[R-MTA-10]`)... Encoding 0 and a
reserved-range value are unassigned too, and R1 registers both as
violations"), states the same substantive disclaimer in both editions. So
the disclaimer's *content* is not lost, only its local adjacency to the
newly-relocated grounds list in §21.6.
Consensus: EQUIVALENT (the grounds list and the disclaiming rule are both
fully present, in substance, in both editions; only location/adjacency
changed). byte_level: false. severity: clarity (a reader who stops at the
new, local §21.6 paragraph in B without following to §21.5 loses the
immediately-adjacent cross-reference that A supplied at the same point;
worth a one-line forward-pointer, not a correctness fix).

### G9 — no explicit sixth "cannot-establish" ground for a file-scope resource decline — gap present identically in both editions
Members: verifiera-01, cmp-verifier-03
Verified: §21.9 is byte-identical between editions (diffed the full
section with `diff`, zero output = identical) and the five-grounds list's
content is identical per G8. The R-ERR-04/§21.9 licence to decline "at the
whole file... before the directory can even be parsed" is present,
unchanged, in both editions, and is not named as an explicit sixth ground
in either edition's version of the five-grounds list.
Consensus: EQUIVALENT (shared gap, not a fidelity difference). byte_level:
false (as to A vs. B — both texts leave the same case equally unstated).
severity: none (for fidelity purposes; this is a drafting gap in the shared
original, out of scope for a B-vs-A fidelity verdict).

### G10 — A's R-CNF-03 bullet states an unimplemented top-level MU=1 type in a conforming file is "necessarily" experimental-range; B drops the clause
Members: cmp-verifier-01, swab-04, verifierb-01
Verified by grep: `necessarily from the experimental` → 1 hit in A (line
183, inside the conforming-reader bullet), 0 hits in B. Read A lines
179-193 and B lines 219-227: A's bullet reads "...carrying no top-level
record of a type it does not implement with MUST_UNDERSTAND = 1 — in a
conforming file such a type is necessarily from the experimental range,
since a reserved-range type carrying MU = 1 is itself a violation — and
none of whose values..."; B's corresponding bullet reads "...carrying no
top-level record of a type it does not implement with MUST_UNDERSTAND = 1
and none of whose values exceeds the minimum guarantees..." with the
derivation clause simply absent, and no restatement found anywhere in B.
I then checked whether this clause is operationally necessary: it is not.
§21.6's closing paragraph "Two structural cases are conforming files a
reader nevertheless refuses... The second is an experimental-range
top-level record type carrying MU = 1... [R-CNT-15] obliges the reader to
reject, and [R-CNF-02] makes the file conforming all the same" is
byte-identical in both editions (A:4057-4063, B:3912-3918, confirmed by
direct comparison), as are the F35/F36 register rows (byte-identical,
confirmed). A real implementation classifies any concrete record by
checking its stored type value against the fixed numeric boundaries
(reserved 0x0003-0x7FFF vs. experimental ≥0x8000, stated identically in
both editions) — it never needs the dropped "necessarily" aside to do so.
The aside is a logical shortcut for a human reader reasoning about an
*incompletely specified* scenario (a probe that withholds the actual type
value, as verifierb-01's own probe does); for any actual file with actual
bytes, both editions' unchanged register material yields the identical
verdict with or without the aside. verifierb-01's own citation also
mis-scopes the §21.6 paragraph as B-only ("A: n/a") when it is in fact
byte-identical in A too.
Consensus: LOSS (A states a derivation B omits and does not restate
anywhere; this is a genuine documentation/reasoning-chain loss — B's own
in-house walk, verifierb-01, demonstrably failed to make this derivation
unaided and reported the fact pattern as unresolved where A's walk did not).
byte_level: false — downgraded from the two reporters' BYTE-LEVEL grade.
Rationale for the downgrade: the byte-level test asks whether "an
implementation built from B alone emit[s] different bytes, or reach[es] a
different accept/reject verdict on SOME FILE" than one built from A alone.
For any concrete file, the type value is a fixed, already-known-to-the-
implementation quantity, and both editions' numeric-range rules and
register rows (F35/F36, §21.6's closing paragraph) are byte-identical, so
both editions compel the identical verdict on that file. The "ambiguity" is
an artifact of stating the probe scenario in English without pinning down
the type's actual range — not a property of any concrete file's bytes.
This matches swab-04's own (correct) conclusion, even though swab-04 filed
it as a low-materiality OBSERVATION rather than fully working the
byte-level test through; cmp-verifier-01 and verifierb-01 overstate the
byte-level stakes by conflating "a verifier's report, given an
underspecified hypothetical, states a settled vs. hedged answer" with "a
verifier, given actual bytes, emits a different verdict."
severity: content (a real loss of explanatory/derivational text that
should be restored for clarity and to spare readers — and B's own walker —
the re-derivation, but it does not, on the facts developed above, change
any conforming/nonconforming verdict for a concrete file).
Recommended action: restore the dropped clause to B's conforming-reader
bullet ("...with MUST_UNDERSTAND = 1 — in a conforming file such a type is
necessarily from the experimental range, since a reserved-range type
carrying MU = 1 is itself a violation — and none of whose values...").

### G11 — closed-list/completeness claim over writer-conduct-only carve-outs dropped from R-CNF-02 bullet
Members: cmp-verifier-05
Verified: A's first §2.3 bullet (ending `[R-CNF-02]`) names three specific
instances (set ignore-lane bit, pre-trailer gap longer than the minimum
pad, §20.3 step 4's fixed-declaration bar) and frames them as "the cases
this text states" — read in context at A:170-179. B's corresponding
sentence (B:215-219) states only "A writer obligation that governs conduct
rather than output, or whose violation this specification expressly
declares not to be a file-conformance violation, binds the writer and
never makes a file nonconforming," with no enumeration and no completeness
claim. I confirmed each of the three named instances is independently
recoverable at its own local section in B (the ignore-lane rule, the
pre-trailer-pad rule, and the §20.3 step 4 bar verified identical under
G5), so only the explicit closed-list/completeness assertion is lost, not
the individual rules.
Consensus: LOSS. byte_level: false (no single instance's rule changes; the
loss is the assurance, stated once in A at the definition point, that
these three are the *only* such carve-outs in the document — a reader of
only §2.3 in B cannot tell whether other, unenumerated instances exist).
severity: content.
Recommended action: restore A's closing enumeration-plus-completeness
clause to B's R-CNF-02 bullet, or add an equivalent "these are the cases
this text states" forward-pointer.

### G12 — §2.3 updater-bullet's "which govern every record type" aside dropped; redundant with §20.4's own opening
Members: cmp-verifier-06
Verified: §20.4's opening sentence, "Persistence governs every record
type; only the authoritative source of the flags differs," is
byte-identical in A (line 3483) and B (line 3339). A's §2.3 updater bullet
previews this with an added clause B drops; the clause's content is fully
and identically restated at §20.4's own point of definition in both
editions.
Consensus: EQUIVALENT. byte_level: false. severity: none.

### G13 — minor prose consolidations (ignore-lane statement, pre-trailer-pad statement, unexamined/per-requirement wording)
Members: cmp-verifier-07
Verified by reading the cited A/B passages side by side (quoted in the
finding) — each pair states the identical rule under different sentence
boundaries; no clause present in one and absent from the other.
Consensus: EQUIVALENT. byte_level: false. severity: none.

### G14 — Part I / Part II architectural-independence claim dropped (stated twice in A, nowhere in B)
Members: swab-01, adv-01, adv-02
Verified: `load-bearing for the updater rules` / `independent of Part` →
1 hit each in A (line 437, 441; §3.3's Note), 0 hits in B. `yields a
container reader` → 1 hit in A (line 89; §1's "Reading this document"
paragraph), 0 hits in B. B has no §3.3 heading at all (confirmed: A's line
range 435-443 has no counterpart section in B), and B's rewritten
Introduction's closing paragraph covers a different topic (the document's
own writing rubric) with no counterpart sentence. The underlying operative
permission (an updater may carry forward a layer it cannot decode) is
established independently and identically by §20's writer-tier rules in
both editions, which neither statement's removal touches.
Consensus: LOSS (both statements are things A states that B does not state
anywhere, and the test explicitly reaches "a definition... that A states
and B does not"; this is architectural/design-invariant guidance, not an
operative rule). byte_level: false — no requirement ID or register row in
either edition cites §3.3 or the dropped Introduction sentence, and §20's
actually-operative rules are byte-identical between editions, so no
implementation's required bytes or verdicts depend on this claim.
severity: clarity (useful design guidance for an implementer deciding what
a container-only tool may safely do; its loss is a documentation quality
regression, not a decided-content regression).

### G15 — preserve-verbatim/ignore-record orthogonality bridge sentence dropped
Members: swab-02
Verified: `orthogonal to reader outcomes` → 1 hit in A (line 303, in §2.4's
ordinary normative prose, not inside a Note), 0 hits in B. Both rules the
sentence bridges (§21.5's ignore-record outcome, §20.4's preserve-verbatim
obligation) are, per other groups' verification above, byte-identical
between editions, so each rule is independently intact in B; only the
explicit cross-rule bridge sentence disappears with no restatement found.
Consensus: LOSS. byte_level: false (both bridged rules are individually
unchanged and correctly statable from either edition alone; what is lost is
the sentence heading off the natural misreading that a reader-ignored
record is one any tool, updater included, may drop).
severity: clarity.

### G16 — "reject" = scope of unusability, not UI, Note dropped
Members: swab-03
Verified: `prescribes the scope of unusability` → 1 hit in A (line 339,
§2.4's trailing Note), 0 hits in B. Control search for "implementation
technique" in B confirms the phrase survives only at the unrelated,
already-present §2.1 Note on requirement-phrasing discipline (present
identically in both editions), not attached to "reject."
Consensus: LOSS. byte_level: false (the Note is explicitly about reporting
mechanism, which by the document's own framework never determines bytes
emitted or verdicts reached).
severity: clarity.

### G17 — worked three-row illustration of the format-major "reach" test (F14/F5/F15) dropped
Members: swab-05
Verified: `three rows show why the distinction` → 1 hit in A (line 284,
§2.3's trailing Note), 0 hits in B. The rule the Note illustrates (R-CNF-13)
and the register rows it walks (F14, F5, F15) are unaffected by its
removal — the Note only explains *why* each row does or does not "reach" a
non-major-1 file, it does not itself assert a new constraint.
Consensus: LOSS — the fidelity test explicitly names "a worked figure... that
A states and B does not" as a LOSS category, and this is exactly that: a
concrete worked figure dropped with no restatement anywhere in B.
byte_level: false (the rule and the per-row determinations it illustrates
are stated, and presumably unchanged, in the register table itself, which
is outside this access-limited pass's remit to re-verify but is not
disputed by any other finding).
severity: content (higher than a bare clarity note, because it is a named,
worked figure the charter singles out, even though no byte or verdict
changes).
Recommended action: restore the Note (or an equivalent worked illustration)
to B's §2.3, since it materially helps an implementer apply R-CNF-13 to
new/future-major fields correctly even though no current-file verdict
depends on it.

### G18 — "addressed tile" glossary definition reworded to be explicitly generation-relative
Members: adv-03
Verified: A's definition ("every tile of a layer is *addressed*", no
generation qualifier) vs. B's ("a tile is *addressed* in a generation if
that generation's tile index has an entry for it: the tiles of the layer's
grid under the geometry that generation declares"). Neither edition
attaches a requirement ID to this glossary bullet. The operative rules that
determine which tiles exist for a given generation (§11.2 grid arithmetic,
§15 tile index, §20.3's append growth clause) are byte-identical between
editions per adv-03's own check (not independently re-verified in this pass
beyond spot-checking §21.9/§20.4/§7.2 elsewhere, which were all confirmed
identical, consistent with this claim).
Consensus: EQUIVALENT (B's wording resolves a latent imprecision in A's
unconditional phrasing — a clarification, not a decided-content change,
since the operative geometry/growth rules are unchanged and identical).
byte_level: false. severity: clarity (noted as a positive clarity change in
B, not a defect).

---

## Coverage check

35 input ids, 18 groups, every id assigned to exactly one group (verified by
listing all group member_ids and confirming the sorted concatenation equals
the sorted input list with no duplicates and no omissions).
