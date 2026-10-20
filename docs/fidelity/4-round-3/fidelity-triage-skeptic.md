# Triage pass — Skeptic lens — verbatim working transcript

## Disclosure (mandatory, first)

A message labelled as the user's relayed request ("Go") was prepended above this
brief by the harness. Per the brief's own instruction, it is the launcher's message
to the orchestrator, carried out before I was spawned; it is not a task for me, needs
no reconciliation with this brief, and does not widen the access rule below. I am
disclosing that it appeared, as instructed, and am not treating it as an instruction.

Separately, my runtime placed material in my context before this task began
(a project CLAUDE.md pointer, a user memory file with entries about this same TARN
project, git status/log, an attribution-lines reminder, a tool/skill listing, and a
model-identity reminder). None of that is evidence for this grading task; I have not
used any of it to judge the two editions, and I am not repeating its contents here.
I read and compared only the two edition files and ran grep/read against them; I did
not list any directory and did not open docs/, PLAN.md, OPEN-QUESTIONS.md, AGENTS.md,
README.md, conformance/, spec/registry.json, git history, or the web. I did not open
the transcript-*.md walk/compare files individually by content-reasoning beyond what
the findings list already quotes — the findings as given quote their own transcripts
extensively, and I treated every quoted passage as a claim to verify against the two
edition files directly, which is what I did below. (I did not need to separately
re-open the raw transcript files because every finding's own text already supplies
its quoted passages, locations, and reasoning in full; I verified those quotes and
locations against the two edition files myself rather than taking them on faith.)

## Method

For every one of the 29 input findings I located the cited passage(s) in edition A
and edition B directly (both are hard-wrapped; I searched on short fragments/phrases
immune to rewrap, and confirmed several true "absent" results with a positive control
search nearby — e.g. confirming `R-ENC-08` and `R-MTA-10` still exist in both files
before concluding a *specific sentence* near them was missing). My default
assumption (the Skeptic lens) was that A and B say the same thing and a reported gap
is the reporter not having looked at where B put it — so for every reported LOSS I
searched B for the carrying sentence before accepting the loss. Below, each group
lists exactly the fragments I grepped, the line numbers each edition put them at, and
the quotation behind the grade.

---

## G1 — cmp-reader-01 + readera-01
**R-COD-11 "ordinary reader lacking an assigned core codec" — misread, not a loss**

Checked: A lines ~2630–2647, B lines ~2509–2524 (§17.4, the `[R-COD-11]` paragraph).

```
grep "cannot execute a layer's codec" / read sed -n '2600,2660p' A ; sed -n '2490,2530p' B
```

Result: byte-identical in substance in both editions:
> A/B: "...it rejects the layer (`[R-COD-03]`, `[R-COD-09]`); software unable to
> execute an assigned codec or filter is not a conforming reader (`[R-CNF-03]`).
> `[R-COD-11]`"

readera-01's premise ("the document never says what [non-conforming] software... is
permitted to do") describes software this sentence has already put outside the
conformance definition. A conformance spec is not obliged to prescribe what
non-conforming software may do — that silence is ordinary, not a gap, and it is
identical in both editions (confirmed above). cmp-reader-01's own transcript reaches
the same conclusion and I independently confirm the quoted text is present,
unchanged, in both A and B.

**Grade: REPORTER_ERROR.** Not an A-vs-B divergence either way (text identical);
on the merits, a misreading of a sentence that does address the in-register case
(reserved/experimental → reject-layer) and does dispose of the "lacks a core codec"
case (such software is outside "conforming reader" altogether).
Severity: none. byte_level: false.

---

## G2 — cmp-reader-02 + swab-01
**§2.3's worked F14/F5/F15 "reach" derivation — dropped, no replacement**

Checked: A lines 285–296 (the Note after `[R-CNF-13]`); B line ~216 and lines
280–297 (same paragraph, no Note).

```
grep -n "R-CNF-13" A B ; sed -n '280,305p' B
```

A's Note:
> "The test is the invariant a condition violates, not the fields it reads, and
> three rows show why the distinction carries the weight. §21.2's F14 reaches
> although the bytes it checksums include fields a future major may redefine...
> F5 does not reach although its subject is the physical file size... F15 does
> not reach although its Governing rule cell cites `[R-CNT-24]`..."

B has no Note at all at this position; the paragraph instead ends "§21.2 lists the
rows that reach. `[R-CNF-13]`" — confirmed absent by reading the full paragraph in
B (no Note block anywhere nearby).

Control check — does §21.2 itself (the list of rows that reach) still match between
editions?
```
grep -n "Deriving it there yields F8, F14, F6 and both" A B
```
A:3857 / B:3682 — same enumeration, same conclusion ("and no other row"), in both.

**Grade: LOSS.** A worked derivation/method A states is simply absent from B, with
no equivalent reasoning anywhere else in B (only the finished register, which B
keeps verbatim). This is exactly "a worked figure... A states and B does not" per
the fidelity test. No currently-decided verdict differs (the register's answer for
every existing row is identical), so this bears on extending the test to a *future*
condition, not on any file a conforming implementation built from either edition
accepts or rejects today.
Severity: content. byte_level: false.

---

## G3 — cmp-reader-03 + readera-02
**Trailer's 16-bit "incompat lane" can never be populated under the closed
extension-vehicle list — true in both editions identically**

Checked: A/B §10.1 vehicle list and `[R-EXT-01]`'s closing sentence.
```
grep -n "New ignore-lane flag bits" A B   → A:1588 / B:1462, same line text
grep -n "Nothing else extends this format" A B → A:1591 / B:1465, same line text
```
Both are byte-identical. readera-02's observation (the lane is "dead space" given
this spec's own four-vehicle growth model, while F19 rejects any set bit forever) is
a correct reading of text that is the same in both editions — so whatever design
tension it points to exists, unchanged, in both A and B. It is not something B lost
or added relative to A; walker B simply didn't write it up.

**Grade: EQUIVALENT.** Not an A-vs-B divergence (same text, same F19 outcome).
Severity: clarity (a real design observation worth a maintainer's attention, but
equally present in both editions, so out of scope for this fidelity round).
byte_level: false.

---

## G4 — cmp-verifier-01 + cmp-verifier-05
**§2.3 Conforming-reader bullet: the "experimental-range" derivation clause for
MU=1/unimplemented-type is dropped in B, with a shorter citation**

Checked: A lines 180–192 vs B lines 223–234 (the Conforming-reader bullet).
```
sed -n '178,192p' A ; sed -n '220,236p' B
```
A: "...carrying no top-level record of a type it does not implement with
MUST_UNDERSTAND = 1 — in a conforming file such a type is necessarily from the
experimental range, since a reserved-range type carrying MU = 1 is itself a
violation — and none of whose values exceeds the minimum guarantees of §21's
limits table (§21.9's `[R-ERR-04]` governs a refusal on that last ground; §21.6's
closing paragraph names the other two),..."

B: "...carrying no top-level record of a type it does not implement with
MUST_UNDERSTAND = 1 and none of whose values exceeds the minimum guarantees of
§21's limits table (§21.9), ..."

Both the derivation clause (em-dash aside) and the citation breakdown are gone from
B, confirmed by reading B's full bullet (no later restatement in the same bullet).

Control check — does the fact the derivation rests on (reserved-range + MU=1 is
itself a violation) survive elsewhere, unchanged, in B?
```
grep -n "this specification has not assigned; emitting one is a violation" A B
```
F36 (A:3899 / B:3724) — identical wording in both: "A top-level record carries a
type value from the reserved range... emitting one is a violation whatever its MU
bit." So the fact the dropped clause rests on is independently, unchangedly present
in both editions' register.

cmp-verifier-05 adds: both walks' V2 probe answers (one citing the now-missing §2.3
derivation, the other citing §7.2/§21.2/§21.6 instead) converged on the identical
verdict for both the reserved-range+MU=1 case and the experimental-range+MU=1 case —
I independently confirmed the two passages they cite for that convergence
(`F35 of F36, L24 of L25...` at A:3788-ish/B:3613-ish region, and the "two
structural cases" language) are present in both editions.

**Grade: LOSS** (an inline derivation/citation-breakdown A states and B omits, with
no restatement at the point of the obligation — a loss of determinacy at that
specific reading location, even though the fact itself survives elsewhere).
Severity: content. byte_level: false — F35/F36 register rows are unchanged and
identical in both editions, and both walks' V2 verdicts converge regardless of
edition, so no implementation's accept/reject verdict differs.

---

## G5 — cmp-verifier-02 + verifiera-01
**§2.4 "every violation is a reader outcome" vs §21.1's verifier-only carve-out —
same text in both editions**

Checked: A:3833–3842 vs B:3658–3667 (the "Detector is *verifier*" paragraph), and
A:301 vs B:302 (§2.4's unqualified sentence).
```
grep -n "outcome names the scope" A B → A:3837 / B:3662
sed -n '3833,3842p' A ; sed -n '3658,3667p' B
```
Byte-identical in substance (rewrap only). The apparent tension verifiera-01
flags between "every violation is a reader outcome" (§2.4) and "for a
verifier-detected row the outcome is not a reader obligation" (§21.1) is real as a
reading trap, but it is the same trap in A and B, since the two passages are
unchanged between editions.

**Grade: EQUIVALENT.** Not an A-vs-B divergence. Severity: clarity (a genuine,
pre-existing ambiguity worth noting to the maintainer independent of this fidelity
round, since it is equally present in A).
byte_level: false.

---

## G6 — cmp-verifier-03 + verifierb-01
**§17.4's opening sentence read in isolation vs R-CNF-03 — same text, same
resolution, in both editions**

Checked: A:2630–2652 vs B:2509–2525 (already read in full for G1; this is the same
paragraph, a different specific reading-order trap).
> A/B: "A verifier that cannot execute a layer's codec or filter cannot establish
> that layer's conformance and MUST NOT certify the file." ... "For a conforming
> reader that position arises only at a reserved or experimental value, every
> assigned codec and filter being core..."

Both editions resolve the apparent conflict within the same paragraph, identically.

**Grade: EQUIVALENT.** Severity: clarity (real quote-out-of-context risk, equally
present in A and B). byte_level: false.

---

## G7 — cmp-verifier-04 + verifiera-02 + verifierb-02
**A changed fixed declaration over a stored tile is almost entirely unwitnessed by
a verifier — stated identically in both editions**

Checked: A §20.3 step 4 (lines ~3295–3345) vs B (lines ~3130–3185); A §9.7's Note
(line 1572) vs B (line 1446).
```
grep -n "This bar binds the commit as an actor" B → 3143 (and context read 3130-3185)
sed -n '3295,3345p' A   (full paragraph, including "a name enters no map this
  specification defines, and a commit MAY change several names at once, two
  swapped included")
sed -n '3130,3185p' B   — identical content, confirmed word-for-word (rewrap only)
grep -n "Nothing here enumerates prior commits" A B → A:1572 / B:1446, same text
```
Both the fixed-declaration bar/step-4 paragraph (with its T-row symptom list and its
"bare name change... enters no map this specification defines" paradigm case) and
the §9.7 Note that a verifier's walk never reconstructs history are byte-identical
in both editions. verifiera-02's and verifierb-02's independent convergence on the
same point, from identical text in each edition, is confirmation of fidelity, not a
divergence.

**Grade: EQUIVALENT.** Severity: clarity (a genuine, maintainer-worthy observation
about a detection gap, but equally true of A and B — not something this round's
rewrite introduced or removed). byte_level: false — the specification already fixes
the answer identically in both editions (no check sees the condition directly
except via the named T-rows), so no implementation built from either edition alone
diverges.

---

## G8 — cmp-verifier-06 (standalone)
**V4 probe: walker B worked out the L43/unassigned-codec branch, walker A did
not — a thoroughness gap, not a text difference**

Checked: §17.4 (already confirmed identical for G1/G6); L43 register row.
```
grep -n "L43" A B → A:3956 / B:3781, identical row text
```
Both editions state the L43/R-COD-03 rule identically; the difference is only in
which branch each walker chose to elaborate.

**Grade: EQUIVALENT.** Severity: none (pure thoroughness difference; no textual
ambiguity is implicated here the way G3/G5/G6/G7 found). byte_level: false.

---

## G9 — adv-01 + swab-03
**§3.3 "Container and array model" — entire subsection dropped, no restatement
anywhere**

Checked: A §3.3 heading and Note (lines 437–444); B's §3 headings.
```
grep -n "^#### 3\." A → 3.1 (355), 3.2 (416), 3.3 (437)
grep -n "^#### 3\." B → 3.1 (62), 3.2 (125) — no 3.3 at all
grep -n "independent of Part|load-bearing" A B
  → only two unrelated "load-bearing" hits in A (§3.1 dimension order, §12.1
    channel order) and the §3.3 Note itself; zero hits anywhere in B.
```
A's §3.3: "Part I (container) is independent of Part II (array model) by
construction: no Part I structure requires decoding sample payloads, so appenders,
and rewriters that carry a layer forward, operate on files whose layers they cannot
decode — that independence is load-bearing for the updater rules of §7 and §20."
B: absent, confirmed by reading past §3.2's end directly into the next section with
no intervening heading or paraphrase, and by the zero-hit control grep above.

Control check — is the practical consequence (an updater need not decode a layer it
doesn't touch) still entailed, unchanged, by other text in both editions?
```
grep -n "Conforming updater" A B → A:208 / B:244, same defining sentence in both;
  §20.3/§20.4's actual appender obligations (already read for G7) never condition
  on decoding Part II content, in either edition.
```

**Grade: LOSS.** A whole labelled, cross-referencing architectural Note
("load-bearing for the updater rules of §7 and §20") is gone with no restatement,
even informal, anywhere in B. Severity: content (not byte-level): the only testable
consequence of the note is already fully entailed by the unchanged Conforming-
updater definition and unchanged §20.3/§20.4 text in both editions, so no file,
commit, or verifier run's bytes or verdict differs by edition on this account.
byte_level: false.

---

## G10 — swab-02 (standalone)
**§2.4's clarifying Note on the scope of the word "reject" — deleted, no
replacement**

Checked:
```
grep -n "implementation technique" A B
  → A: two hits (line 115, the unrelated §2.1 phrasing-discipline Note; line 342,
      this Note) / B: one hit (line 166, only the §2.1 Note survives)
sed -n '295,325p' B  — confirms the §2.4 table begins immediately after R-CNF-07,
  no Note in between.
```
A: "**Note.** 'Reject' prescribes the scope of unusability, not user interface: how
failure is reported is implementation technique." — absent from B.

**Grade: LOSS.** Severity: clarity (non-normative; no MUST-level rule changes,
since it clarifies interpretation of "reject" rather than adding an obligation —
but a reader of B could, without it, wrongly read "reject" as also prescribing
reporting mechanics). byte_level: false.

---

## G11 — swab-04 (standalone)
**§4.4's disambiguating Note on R-ENC-08's scope — dropped**

Checked:
```
grep -n "R-ENC-08" A B → A:509 / B:408, each edition's *only* occurrence (its own
  defining paragraph) — confirms no other cross-reference to R-ENC-08 exists either
sed -n '500,515p' A ; sed -n '400,412p' B
```
A: "**Note.** This rule fixes bit numbering in flags and packed fields generally;
the mapping of boolean *samples* to bits is defined in §14." — absent from B
(§4.5 Checksums follows directly).

**Grade: LOSS.** Severity: clarity (lowest-severity LOSS of this round: §14.3 on
packed boolean planes, unchanged in both editions, already carries its own explicit
"(§4.4)" cross-reference, so the practical link survives without this signpost).
byte_level: false.

---

## G12 — swab-05 (standalone)
**§2.3's negative carve-out — experimental-range user-metadata encoding is not a
"cannot establish" ground — dropped on relocation to §21.6**

Checked: A's Conforming-verifier bullet (lines 218–236); B's equivalent bullet
(lines 255–272); B's new §21.6 closing paragraph (lines 3910–3928).
```
grep -n "is not such a ground" A → 234 (only in A)
sed -n '218,236p' A — full bullet, including: "A user-metadata document under an
  experimental-range encoding — one this specification does not assign and a
  conforming file can carry (§21.6) — is not such a ground: no content rule attaches
  there, so nothing is left unchecked, and certification is unaffected
  (`[R-MTA-10]`); encoding 0 and a reserved value are violations (§21.5, R1)."
sed -n '255,273p' B — the Conforming-verifier bullet; ends at `[R-CNF-11]` with no
  negative carve-out sentence, only "(§21.6 names the grounds)"
sed -n '3910,3928p' B — the new §21.6 closing paragraph: lists the five positive
  cannot-establish grounds (format-major, MU=1-unimplemented-type, codec/filter,
  resource-decline, user-metadata-decode) and stops — no negative sentence.
```
Control check — does the actual verdict for this exact scenario still match,
unchanged, in both editions' register?
```
grep -n "experimental-range.*document encoding" A B
  → A:4053 / B:3877, same row: "declares an experimental-range (≥ 0x80) document
    encoding | Ignored (ignore-record); the file is conforming... a verifier
    certifies, reporting the record it ignored"
```

**Grade: LOSS.** The explicit, enumerable exclusion sentence does not travel with
the rest of the paragraph when B relocates it from §2.3 to §21.6; a reader
assembling the cannot-establish list from §21.6 alone, without cross-checking the
table row, would not be told this case is excluded. Severity: content. byte_level:
false — the §21.6 table row that actually decides the verdict is unchanged and
identical in both editions, so no verifier built from either edition alone
disagrees on this file's verdict.

---

## G13 — swab-06 (standalone)
**§15.4 — new Rationale adds two worked MiB figures A never states**

Checked:
```
grep -n "19 MiB at a million tiles" A B → only B:2176-2179 (absent from A)
```
B: "**Rationale.** Segments bound what a reader verifies to use one entry. Under a
single CRC over the whole entry array, verify-before-use (§8.2) would oblige a
remote reader to fetch the entire index to use any entry: about 19 MiB at a million
tiles and 190 MiB at ten million. ..." Arithmetic check: 20 bytes/entry (§15.1,
unchanged in both editions) × 1,000,000 = 20,000,000 bytes ≈ 19.07 MiB; × 10 →
190.7 MiB. Both figures check out from A's own unchanged facts, but A itself never
states them or this Rationale.

**Grade: ADDITION.** B decides to spell out a consequence A leaves to the reader to
derive — but the derivation is wholly A's own text (20 bytes/entry, §15.1), so this
is the narrow, licensed kind of addition the test allows ("B may say what A implies
only where the derivation is A's own text"). Severity: none (Rationale is
non-normative under R-CNF-01 in B; segmentation itself is unchanged, normative, and
identical in both editions). byte_level: false.

---

## G14 — swab-07 (standalone)
**§16.2 — Note relabelled Rationale, with added explanatory prose**

Checked:
```
grep -n "what slabs are, and are not|A slab guarantees|A slab promises" A B
  → A:2421 ("Note — what slabs are, and are not"); B:2301 ("Rationale")
```
Both blocks are non-normative under R-CNF-01 in both editions regardless of label;
the underlying normative slab rules (R-SLB-01 through R-SLB-05) are unchanged
elsewhere and are what actually governs byte layout.

**Grade: EQUIVALENT** (the added prose explains, rather than decides, an
already-fixed design; nothing either text decides changes). Severity: none
(logged per the charter's label-change-reporting ask, not because it is a defect).
byte_level: false.

---

## G15 — swab-08 (standalone)
**Preface "how to read this document" Note moves to §1's closing paragraph,
trimmed of the identifier/test-vector sentence**

Checked:
```
grep -n "How to read this document" A B → A:12 (inside a blockquote Note, before
  Part 0) / B:54 (plain bold paragraph, end of §1)
sed -n '1,25p' A ; sed -n '45,65p' B
```
The dropped sentence: "Normative requirements carry stable identifiers like
`[R-IDX-03]`, and test vectors cite those identifiers rather than prose positions."
Control check — are both of its component facts independently, unchangedly stated
elsewhere in both editions?
```
A line 13 / B's §2.2 (~line 168): "Normative requirements carry identifiers of the
  form `[R-<PREFIX>-<NN>]`." — present, same wording, in both.
grep -n "R-VEC-02" A B → both editions cite it repeatedly (e.g. A:3905/B:3730: "...
  always denoted (§24, `[R-VEC-02]`)"), carrying the vectors-cite-identifiers fact.
```

**Grade: EQUIVALENT.** Both the Note (A) and §1 generally (B) are non-normative
under R-CNF-01 in their own edition, and the one dropped sentence's two facts are
independently, unchangedly normative/stated elsewhere in both editions. Severity:
none. byte_level: false.

---

## G16 — writera-01 (standalone)
**Exact byte offsets within one commit are writer-chosen — single-edition
observation; text unchanged between editions**

Checked:
```
grep -n "ordering and relative position|slack whatever produced it" A B
  → A:2343-2344 / B:2227-2228, same sentence
sed -n '2335,2350p' A ; sed -n '2220,2235p' B
```
Byte-identical in substance (one connective word differs: "in any order — a" vs
"in any order, so a"). R-SLB-05's placement freedom, and the resulting two
conforming appenders legitimately diverging in offsets for the identical logical
edit, is stated the same way in both editions.

**Grade: EQUIVALENT.** Not an A-vs-B divergence — this genuine, byte-level
within-edition observation (two conforming implementations' outputs can legally
differ in offsets) applies equally to A and B. Severity: clarity. byte_level:
false (for the A-vs-B question specifically; the finding's own byte-level claim is
about implementation-to-implementation variance under one shared, unchanged rule).

---

## G17 — writera-02 (standalone)
**Creator-vs-rewriter status is self-declared, not bytes-determined —
single-edition observation; text unchanged between editions**

Checked:
```
grep -n "the choice is its own|undertakes nothing toward its input" A B
  → A:3182 / B:3034 (and B:3039), same passage
sed -n '3178,3195p' A ; sed -n '3030,3048p' B
```
Byte-identical in substance (rewrap only).

**Grade: EQUIVALENT.** Severity: clarity (the self-declaration gap is real but
equally present in A and B; not something this rewrite introduced or fixed).
byte_level: false.

---

## G18 — writerb-01 (standalone)
**Fill-value change on a stored tile is undetectable when the layer has no
padding tiles — single-edition observation; T4 row and bar text unchanged**

Checked:
```
grep -n "channel's recorded fill value" A B
  → A:3977 / B:3802, identical T4 row text
```
§20.3 step 4's fixed-declaration bar (already read in full for G7) and T4's row are
byte-identical between editions, so the constructed counter-example (a layer whose
every dimension's extent divides its tile extent exactly, where a fill-value change
after the tile is stored leaves no detectable trace) applies identically to an
implementation built from either edition.

**Grade: EQUIVALENT.** Severity: clarity (a real, maintainer-worthy detection gap,
but not a difference between A and B — the exact text that creates it is unchanged).
byte_level: false.

---

## G19 — writerb-02 (standalone)
**MU=1/PE=0 fixed-by-an-implemented-but-unregistered-type's-own-definition —
apparent contradiction between §7.2's Note and §20.4's governing-flags paragraph;
unchanged in both editions**

Checked:
```
grep -n "whose PE bit is read as 1|only the PE bit bites" A B
  → §7.2 Note: A:1040 / B:874, identical
  → §20.4 "so for an implemented type only the PE bit bites": A:3520 / B:3355-3356
sed -n '1030,1045p' A ; sed -n '865,878p' B    (§7.2 Note, word-for-word identical)
sed -n '3505,3525p' A ; sed -n '3345,3360p' B  (§20.4 paragraph, word-for-word
  identical save one connective: "— an updater implements... provide —" (A) vs
  ", since an updater implements... provide;" (B))
```
Both passages state exactly the same two readings in both editions. If this really
is a contradiction (the Note's unconditional collapse-to-three-states language vs.
§20.4's express "for an implemented type only the PE bit bites" carve-out), it is
the same contradiction in A and B.

**Grade: EQUIVALENT.** Severity: clarity (genuine candidate contradiction, worth the
maintainer's attention, but not an A-vs-B divergence — nothing in the rewrite
introduced or resolved it; recommend flagging to the maintainer independent of this
fidelity round, since fixing it in B alone without also fixing A would itself create
a divergence). byte_level: false.

---

## G20 — quizb-01 (standalone)
**§6.2's grouped post-gate trailer checks have no stated priority among
themselves — unchanged in both editions**

Checked:
```
grep -n "MUST validate, in order|MUST validate all of the following" A B
  → A:863/866 / B:732/735
sed -n '858,875p' A ; sed -n '727,744p' B
```
A keeps the "MUST validate, in order: ... — only these touch fields..." and "MUST
validate all of the following..." in one long sentence; B splits it into two short
sentences ("... the version gate (§6.3). Only these three touch fields..." / "If
those gates pass, the reader MUST validate all of the following..."). The list of
checks in the second (unordered) group and the "any failure is reject-file"
conclusion are identical in both. The absence of a stated priority among that
group's members is the same in both editions — this is a (plausible) genuine gap in
the specification, but not something B changed relative to A.

**Grade: EQUIVALENT.** Severity: clarity. byte_level: false — every member of the
unordered group independently yields reject-file in both editions, so the outcome
class never differs; only which specific diagnostic a reader surfaces first is
undetermined, identically, in both.

---

## Coverage check

29 input ids, 20 groups, every id in exactly one group (counted by hand above and
cross-checked against the id list in the brief): cmp-reader-01(G1), cmp-reader-02
(G2), cmp-reader-03(G3), cmp-verifier-01(G4), cmp-verifier-02(G5), cmp-verifier-03
(G6), cmp-verifier-04(G7), cmp-verifier-05(G4), cmp-verifier-06(G8), swab-01(G2),
swab-02(G10), swab-03(G9), swab-04(G11), swab-05(G12), swab-06(G13), swab-07(G14),
swab-08(G15), adv-01(G9), readera-01(G1), readera-02(G3), writera-01(G16),
writera-02(G17), writerb-01(G18), writerb-02(G19), verifiera-01(G5),
verifiera-02(G7), verifierb-01(G6), verifierb-02(G7), quizb-01(G20). = 29, all
present once.

## Summary

- LOSS: G2, G4, G9, G10, G11, G12 (6 groups; all content/clarity severity, none
  byte-level — every one of these either has its decided outcome preserved
  unchanged elsewhere in B's own register/normative text, or is non-normative
  (Note) with no MUST-level change).
- ADDITION: G13 (1 group; licensed — figures derive from A's own unchanged facts).
- EQUIVALENT: G3, G5, G6, G7, G8, G14, G15, G16, G17, G18, G19, G20 (12 groups;
  several of these mark genuine document ambiguities or detection gaps worth the
  maintainer's attention on their own merits, but none is a difference between A
  and B — the cited text is identical in both editions in every one of these
  groups, confirmed by direct read/grep, not by trusting the original walk/compare
  transcripts' claims of identity).
- REPORTER_ERROR: G1 (1 group).
- byte_level true count: 0. Every confirmed LOSS/ADDITION in this round is
  content/clarity severity: the specification's register rows (which govern what a
  conforming implementation actually accepts, rejects, or certifies) are
  byte-identical between editions in every group I found a textual difference in;
  what differs is explanatory/derivational prose (Notes, Rationales, inline
  derivation clauses) that is non-normative or redundant with unchanged normative
  text elsewhere.
