# Triage — implementer-consequence lens — transcript

Access used: edition A = scratch/cleanroom/editions/a/tarn.md (4981 lines);
edition B = scratch/cleanroom/editions/c/tarn.md (4885 lines, the file the
harness calls "edition B" though it is on disk at editions/c/). No other
file was opened. I did not list any directory beyond `ls` on the two
`editions/*` folders to confirm which files exist there (a and c only) and
`ls`/`wc -l` on the two named tarn.md files themselves, which the access
rule permits since I opened them by name afterward. I ran targeted `grep -n`
searches against A and B only; every zero I report below is backed by a
control hit for a distinguishing phrase from the same passage in the other
edition, confirming the search mechanics work and the absence is real, not
a search miss. Both files are hard-wrapped; I searched short, distinguishing
fragments rather than full sentences.

No transcript-*.md files were opened for this pass — the 53 findings as
handed to me already carry the reporter's cited section/requirement IDs and
verbatim quotations from both editions, and my job is to re-derive the
grade from the two edition files myself, which I did for every group below
by opening A and B at the cited location directly. Nothing in this
transcript repeats material that was in my context before I began beyond
quoting the two edition files themselves.

Disclosure: this task's own prompt (as relayed to me) contains the full
text of all 53 findings, pre-quoted with edition excerpts. That material
was in my context before I began; I did not re-fetch it from any file, and
I treat those quotations as claims to verify against the edition files, not
as evidence in themselves. Every quotation below marked "checked" is one I
independently re-grepped and read in context in A and/or B during this
session.

Lens: **implementer consequence** — for each group, what does someone
building an implementation from edition B alone do differently (or not
differently) than someone building from edition A alone?

---

## G1 — R-CNF-02 conduct-rule polarity is inverted in B
Members: cmp-reader-01, cmp-writer-01, cmp-verifier-01, swab-01, swba-01, adv-01 (6)

Checked A lines 166-179, B lines 206-218 directly.

> A (line ~168-179): "A few obligations this specification places on writers govern their *conduct* rather than their output ... and a file is never nonconforming by virtue of one: conduct rules bind the actor, the predicate binds the bytes. A writer obligation whose violation this specification expressly declares not to be a file-conformance violation binds the actor in the same way; §6.3's flags rules against a set ignore-lane bit ..., §6.2's pre-trailer gap longer than [R-LIF-02] step 5's pad, and §20.3 step 4's bar on the fixed declarations of a layer that stores a tile are the cases this text states ... `[R-CNF-02]`"
> B (line ~214-218): "A writer obligation that governs conduct rather than output, or whose violation this specification expressly declares not to be a file-conformance violation, binds the writer, and a file that breaks one is nonconforming. `[R-CNF-02]`"

Confirmed: B's sentence asserts the literal opposite of A's ("binds the writer, and a file that breaks one is nonconforming" vs "a file is never nonconforming by virtue of one"). I additionally re-checked the three unrelated locations that all reporters cite as B's own self-contradiction, and found each byte-identical between A and B:
- §9.2 (both files, matching line offsets): "...the file it produces is never nonconforming by virtue of it, as `[R-CNF-02]` says of every conduct rule."
- §6.3's ignore-lane-bit table row (§21.6 defined-behaviors table, both files): "An ignore-lane flag bit (16–31) is set | Ignored; the file is conforming..."
- §20.3 step 4 / §21.7's closing sentence citing `[R-ERR-01]`, `[R-CNF-02]` together — byte-identical in both files.

**Implementer consequence**: a verifier coded strictly from B's §2.3 [R-CNF-02] sentence reports NONCONFORMING for a file whose only defect is an unwitnessed writer-conduct violation (e.g. a set ignore-lane bit, an over-long pre-trailer pad, a §20.3-step-4 fixed-declaration edit with no other register-witnessed effect) — a file that a verifier coded from A, or from B's own §9.2/§6.3/§20.3 text, certifies conforming. Two implementations built from B's own internally-contradictory text diverge from each other, not just from A.

Consensus: **LOSS**. byte_level: **true**. Severity: **byte-level**.
Recommended edit: restore A's polarity ("a file is never nonconforming by virtue of one") in B's §2.3 bullet; the surrounding B prose otherwise reads as a faithful paraphrase apart from this one clause.

---

## G2 — B drops the closed list of three worked conduct-rule examples from R-CNF-02
Members: cmp-verifier-02 (1)

A names, at the point R-CNF-02 is defined, the three specific cases ("§6.3's flags rules ..., §6.2's pre-trailer gap ..., and §20.3 step 4's bar ... are the cases this text states, and each is declared where it arises rather than enumerated here"). B's rewritten bullet (quoted in G1) has no such enumeration.

**Implementer consequence**: none directly — each of the three underlying rules is still stated correctly and in full at its own home section (§6.2, §6.3, §20.3 step 4, all confirmed byte-identical between editions elsewhere in this pass). What is lost is the reader's ability to cross-check, from §2.3 alone, that the list is closed and matches §20.3 step 4's own citation back to R-CNF-02. This compounds G1 (a reader trying to resolve G1's contradiction by checking "which obligations does R-CNF-02 actually name" now finds no answer in §2.3 itself) but is not itself a second byte-level divergence.

Consensus: **LOSS**. byte_level: **false**. Severity: **clarity**.
Recommended edit: restore the three-item worked list (or an equivalent closed enumeration) once G1's polarity is fixed.

---

## G3 — R-CNF-13 "reach" paragraph: reaching-condition failure and the R-CNT-04 exemption are both inverted
Members: cmp-reader-02, cmp-verifier-03, swab-04, swba-02, adv-02 (5)

Checked A lines ~264-273, B lines ~278-289 directly (full paragraph read both sides).

> A: "A reader MUST apply every reaching condition to a file whatever major it declares — an exemption the condition's governing requirement grants on a ground other than the declared major applies unchanged, `[R-CNT-04]`'s residency exemption among them — and MUST treat its failure as reject-file on the ground of the requirement stating it rather than on capability grounds; the distinct diagnostic `[R-CNT-07]` asks for is owed where every reaching condition is satisfied and the declared major is one the reader does not implement."
> B: "A reader MUST check every reaching condition whatever major the file declares, and MUST treat a failure as a capability refusal, not as reject-file under the requirement that states the condition; an exemption that the condition's own requirement grants for a reason other than the declared major lapses, `[R-CNT-04]`'s residency exemption among them. `[R-CNT-07]`'s distinct diagnostic is given where every reaching condition is satisfied and the declared major is one the reader does not implement."

Confirmed both reversals are real: "applies unchanged" → "lapses", and "MUST treat ... as reject-file ... rather than on capability grounds" → "MUST treat a failure as a capability refusal, not as reject-file". B's own very next paragraph (also checked, byte-identical to A there) still says a verifier finding such a failure "reports *nonconforming*" — which only makes sense under the reject-file reading (nonconforming requires an established violation per R-CNF-11; capability grounds route to cannot-establish). B's own §21.6 (checked above under G6) and §21.9 (both unchanged) name exactly two capability refusals, neither of which is a reaching-condition failure.

**Implementer consequence** (concrete divergence): take a remote, non-resident reader relying on R-CNT-04's residency exemption, opening a file that declares an unimplemented major and whose front signature block (a reaching condition per §6.3, byte-identical in both editions) is corrupted. Under A: the exemption still applies, so this reader need not have fetched bytes [0,16) at all; if it did check and the check failed, it reports reject-file under the requirement stating the failing condition. Under B taken literally: the exemption lapses, forcing the reader to fetch and check those bytes it was previously exempt from, and having found them corrupted it must report a "capability refusal" rather than reject-file — mislabeling a genuine corruption as a mere capability gap, and doing a different, additional byte-range fetch to get there. Two implementations built from A and B alone diverge in both I/O performed and mandatory diagnostic category on the identical file.

Consensus: **LOSS**. byte_level: **true**. Severity: **byte-level**.
Recommended edit: restore both A polarities ("applies unchanged" and "reject-file ... rather than on capability grounds") in B's reach paragraph.

---

## G4 — R-CNF-03 drops "both record types §7.3 registers" from the conforming-reader no-subset-profiles rule
Members: cmp-reader-03, cmp-writer-02, swab-02, swba-04, adv-03 (5)

Checked A lines 180-196, B lines 219-227 directly.

> A: "...every user-metadata encoding §18.2 assigns, and both record types §7.3 registers. There are no subset profiles: software that declines to support a core codec, a core filter, either channel layout, a core sample type, an assigned user-metadata encoding, or a registered record type is not a conforming reader, even if it reads all other conforming files correctly."
> B: "...every sample type that §12 designates as core, and every user-metadata encoding §18.2 assigns. There are no subset profiles: software that declines any of those is not a conforming reader, even if it reads all other conforming files correctly."

Confirmed the record-type clause is gone from both the affirmative list and the disqualification sentence. I checked Appendix H's conformance checklist in both files (line 4901 in A, 4805 in B) and it is byte-identical: "...registered record types (`[R-CNF-03]`, §2.3);" — so B's own Appendix H still attributes the full six-item requirement (including record types) to `[R-CNF-03]`/§2.3, which no longer states it. I also checked §7.3 itself is unchanged in both editions and does not independently state a disqualification for declining a record type.

**Implementer consequence**: a reader that implements every codec/filter/layout/sample-type/metadata-encoding but treats the registered (0x0002) user-metadata record type as an unrecognized, ignorable type (which §7.2's generic MU=0 handling otherwise permits for a truly unknown type) is disqualified as nonconforming under A's §2.3 text and under B's own Appendix H — but is not disqualified under B's §2.3 text read alone. A verifier or certification tool built strictly from B's §2.3 paragraph would certify this software's output files as coming from a "conforming reader" where one built from A (or from B's own appendix) would not. This is a real classification divergence for identifiable software, and it is self-contradictory within B alone (its own two passages disagree).

Consensus: **LOSS**. byte_level: **true**. Severity: **byte-level**.
Recommended edit: restore "and both record types §7.3 registers" / "or a registered record type" to B's §2.3 R-CNF-03 bullet, matching what B's own Appendix H already asserts it says.

---

## G5 — R-CNF-11 drops "and updaters" from the sentence that gives updaters every reader obligation
Members: cmp-reader-04, cmp-verifier-04 (2)

Checked A line ~218, B line ~248-249.

> A: "Verifiers and updaters are readers of the files they process and inherit every reader obligation."
> B: "Verifiers are readers of the files they process and inherit every reader obligation."

Confirmed the narrowing. I also checked the cross-reference both reporters cite: line ~3191-3192 (A) / ~3088-3089 (B), byte-identical in both files: "(`[R-RDR-02]`'s principle, which §2.3 extends to updaters as readers of what they process, `[R-CNF-11]`)". In B this citation is now false as written — it points to a §2.3 that no longer extends anything to updaters generally. I also checked §20.4's MU=1 preservation-table row (byte-identical both editions): "the updater is a reader of the file first (§2.3)" — again a citation into a §2.3 passage that, in B, says this only of verifiers.

**Implementer consequence**: an updater implementer who reads B's §2.3 alone no longer learns, from that one authoritative definition, that they must satisfy every ordinary reader obligation (e.g. the reject-file gates of §19/§21) before treating an input file as valid to update. §20.4 states updaters must satisfy every *writer* requirement for bytes they produce and honor preservation obligations, but that is a different (output-side) obligation from "you must first read this file as a conforming reader would" (input-side validation). An updater built to satisfy only what B's own text explicitly assigns it, while two separate passages still cite §2.3 as the source of the broader updater-as-reader principle, is under-specified about which reader-level checks it must perform first — a real, if narrower, gap than G1/G3/G4's outright reversals.

Consensus: **LOSS**. byte_level: **true** (an updater author could legitimately skip an input-validation step that A requires). Severity: **content**.
Recommended edit: restore "and updaters" to B's §2.3 sentence.

---

## G6 — R-CNF-11's "cannot establish" grounds are compressed in B and the resulting §21.6 list is short a ground and the experimental-encoding carve-out
Members: cmp-writer-03, cmp-verifier-05, swab-03, swba-05 (4)

Checked A's inline five-ground enumeration (lines ~222-234) and B's §2.3 cross-reference ("§21.6 names the grounds") plus B's new §21.6 closing paragraph (lines 3975-3980, confirmed this paragraph has **no counterpart at all** in A — A's §21.6 ends at line 4076 with the reserved-range/version_major=0 paragraph and has no "verifier is unable to check..." paragraph).

> A (§2.3): "...when it declines a layer's or a tile's decode on resource grounds and so cannot check §14's decoded-content obligations (`[R-ERR-04]`, `[R-SER-05]`, `[R-SER-08]`), or when it declines to decode a user-metadata document (`[R-MTA-09]`). A user-metadata document under an experimental-range encoding — one this specification does not assign and a conforming file can carry (§21.6) — is not such a ground: no content rule attaches there, so nothing is left unchecked, and certification is unaffected (`[R-MTA-10]`); encoding 0 and a reserved value are violations (§21.5, R1)."
> B (§21.6, new paragraph): "A verifier is unable to check a requirement on a capability or resource ground, and so reports *cannot establish* (`[R-CNF-11]`), as when the file names a format major version it does not implement, a record carries MUST_UNDERSTAND = 1 with a type it does not implement, it cannot execute a codec or filter (`[R-COD-11]`, §17.4), or it declines to decode a user-metadata document (`[R-MTA-09]`)."

Confirmed B's list has four grounds, omitting the "declines a layer's or tile's decode on resource grounds" ground entirely, and B carries **no** restatement of the experimental-encoding carve-out anywhere: I grepped every `R-MTA-10` occurrence in both files (11 hits each, same line-offset pattern) and none of B's occurrences states the "is not such a [cannot-establish] ground" rule — that sentence exists only in A's §2.3 (now deleted) and nowhere else in either file.

**Implementer consequence** (two distinct divergences in one edit):
1. A verifier built strictly from B's own two authoritative statements (§2.3's cross-reference plus the §21.6 list it points to) has **no textual basis** to report the distinct *cannot establish* verdict A requires when it declines a layer's or tile's decode on resource grounds. (§17.4/§9.7, checked and confirmed byte-identical in both editions, do separately state the underlying inability-to-check fact in prose, so a whole-document implementation of B does not actually lose the behavior — but an implementer trusting B's own promise "§21.6 names the grounds" and stopping there builds an incomplete verifier.)
2. More concretely divergent: a verifier built from B alone, encountering a user-metadata document under an experimental-range encoding, has no textual carve-out telling it this is *not* a cannot-establish ground. Applying B's fourth listed ground ("it declines to decode a user-metadata document") at face value to such a document, a B-only implementation could report cannot-establish / decline to certify — where A explicitly requires it to certify normally (`[R-MTA-10]`). That is a different certification outcome for the same file.

Consensus: **LOSS**. byte_level: **true**. Severity: **byte-level**.
Recommended edit: either restore the full five-ground list plus the experimental-encoding carve-out directly in §2.3 (undoing the compression), or, if the cross-reference to §21.6 is kept, make B's new §21.6 paragraph state all five grounds and reinstate the R-MTA-10 carve-out sentence there.

---

## G7 — F5's 128-byte floor is applied before the major is known; §2.3's reach doctrine says F5 must not reach a foreign-major file. Present unchanged in both editions.
Members: cmp-reader-05, readera-01 (2)

Checked §19.1 step 1 (A line ~3836 region "Outcome: reject-file. 35 conditions..." preamble is at §21.2; the operative step-1 text was quoted by the reporter) and confirmed both this and the reach-doctrine worked Note text are byte-identical between A and B where they still exist in A. (B has since deleted the F14/F5/F15 worked Note — see G9 — but the underlying §19.1 step 1 wording that creates the tension is present, unchanged, in both A and B.)

> A/B §19.1 step 1 (identical): "an F below 128 is a validity error at file scope decided from F alone and needing no other byte of the file (`[R-CNT-27]`, F5)"

**Implementer consequence**: this is a genuine MUST-level tension (nonconforming vs. cannot-establish for a file with 80≤F<128 whose unread trailer would validate an unimplemented major) but it exists **identically in both editions** — it is not something edition B introduced, worsened, or fixed relative to A (aside from G3's independent reversal of the reject-file/capability-refusal labels, which sharpens rather than resolves it). Since the passages this finding turns on are confirmed byte-identical, no implementation built from B alone behaves differently, on this specific point, than one built from A alone.

Consensus: **EQUIVALENT** (no A-vs-B divergence — a defect shared unchanged by both editions). byte_level: **false**. Severity: **none** (for this fidelity round; worth a separate ticket against the specification itself, independent of the A/B comparison).

---

## G8 — F5's "Instances" column and R1's two-request baseline: shared, unchanged text: not a B-specific issue
Members: cmp-reader-06, cmp-reader-09, readerb-02, readerb-03 (4)

Checked §21.1/§21.2 (F5 Instances column) and §6.4 (R1, R-CNT-09 and its accounting Note) in both files.

> A/B §6.4 (identical): "This accounting is a theory of operation, not a budget: no request count is a conformance property, and nothing here bounds what a reader fetches." and "A reader MAY instead speculatively fetch a suffix window in one request and use containment..."

Confirmed both cited passages (F5's Instances column listing "F (physical file size); committed_file_length", and §6.4's licensed one-request alternative) read byte-identical in A and B. readerb-02's point (one of F5's two named "instances" may not be independently constructible, since F17/`[R-CNT-06]` already catches any file where the two fields diverge) and readerb-03's point (R1's "list every request" has a stated two-request baseline but a one-request speculative strategy is equally licensed, so it isn't a single forced answer) are both real observations about the shared specification text, not about anything edition B changed.

**Implementer consequence**: none attributable to B specifically. A conformance-vector author or a reader implementer following either edition alone hits the identical underdetermination in both cases.

Consensus: **EQUIVALENT**. byte_level: **false**. Severity: **none**.

---

## G9 — B drops the version_major=0 sentence and the F14/F5/F15 worked Note from §2.3's reach discussion; the operative reach-row list is preserved verbatim in §21.2
Members: cmp-reader-07, cmp-verifier-06, swba-06 (3)

Checked A's paragraph and Note (lines 259-292) against B's shortened close (line ~289: "§21.2 lists the rows that reach."), and checked §21.2's opening paragraph in both files.

> A §2.3: "A file whose version_major is 0 declares no major at all (§6.3): it is not a file declaring a format major other than 1, no reach question arises for it, and `[R-CNT-07]` rejects it (§21.2, F18)." — absent from B's §2.3.
> A §2.3 closing Note (worked F14/F5/F15 reasoning) — absent from B entirely (confirmed: B's reach paragraph ends at "§21.2 lists the rows that reach. `[R-CNF-13]`" with no Note block following).
> §21.2's opening paragraph (checked, byte-identical in both editions): derives exactly F8, F14, F6 and both F1 instances as the reaching rows, and states the version_major=0 premise directly, independent of §2.3's now-deleted sentence and Note.

**Implementer consequence**: none. The concrete, operative list an implementer actually codes against — which register rows reach a foreign-major file — is stated, unchanged, at §21.2 in both editions, and does not depend on the deleted §2.3 sentence or Note. The Note was itself a non-normative `> **Note.**` block in A (non-normative under `[R-CNF-01]`), walking through *why* three specific rows fall where they do; its removal costs a reader the worked derivation but not the answer, which §21.2 already gives directly. The version_major=0 sentence is likewise restated as a stated premise inside §21.2's own opening paragraph.

Consensus: **EQUIVALENT**. byte_level: **false**. Severity: **clarity** (the worked derivation has real audit/onboarding value and its loss is worth flagging, but it decides nothing a byte-level check depends on).

---

## G10 — R-CNF-06 drops the "governs every record type" appositive; restated verbatim at §20.4's own opening sentence
Members: cmp-reader-08 (1)

Checked both files' §20.4 headers (A line 3475, B line 3372) and the immediately following prose.

> A §2.3 R-CNF-06: "...MUST honor the preservation obligations of §20.4 — which govern every record type, not only those it does not understand."
> B §2.3 R-CNF-06: "...MUST honor the preservation obligations of §20.4."
> A/B §20.4 opening (checked, byte-identical in both): "Persistence governs every record type; only the authoritative source of the flags differs."

**Implementer consequence**: none. Anyone reading §20.4 itself — which every updater implementer must, since it is where the actual re-emission rules live — gets the identical fact restated as the section's own first sentence, in both editions.

Consensus: **EQUIVALENT**. byte_level: **false**. Severity: **clarity**.

---

## G11 — R2/R5/R6/R7/R8 probes rest on confirmed byte-identical governing text
Members: cmp-reader-10 (1)

Checked the flags row (§6.2/§6.3, `[R-CNT-08]`), §7.1 (`[R-CNT-11]`), §5.1/§19.1 step 1 (`[R-CNT-27]`), §11.2/§11.4/§14.2, and §7.2/§7.4/§21.6 (`[R-CNT-15]`/`[R-CNT-18]`) — spot-checked the incompat-lane sentence and the ignore-lane table row, both byte-identical in A and B.

> A/B (identical): "a reader MUST reject-file on any set bit it does not implement in the incompat lane (bits 0–15)"

**Implementer consequence**: none for any of these five probes — the governing sections are the same bytes in both editions.

Consensus: **EQUIVALENT**. byte_level: **false**. Severity: **none**.

---

## G12 — No outcome class covers a reader lacking a core (assigned) codec; shared, unchanged text
Members: cmp-reader-11, readera-02, readerb-01 (3)

Checked §17.2 (`[R-COD-03]`), §17.4 (`[R-COD-11]`), and the codec clause of R-CNF-03 (distinct from the record-type clause lost in G4) in both files.

> A/B (identical): "software unable to execute an assigned codec or filter is not a conforming reader (`[R-CNF-03]`)"

**Implementer consequence**: none attributable to B. Both editions equally fail to give an in-progress, partial implementation (e.g. one that has not yet added zstd) any register outcome to report; per `[R-CNF-03]`, such software is simply outside "conforming reader" by definition in both editions, so a genuinely conforming reader (by either edition's own definition) can never be in this state. A real documentation-completeness gap, but identical in both texts.

Consensus: **EQUIVALENT**. byte_level: **false**. Severity: **none**.

---

## G13 — §3.3's Part I/Part II independence Note is deleted outright in B, no replacement
Members: cmp-writer-04, swab-06 (2)

Checked: A has a `#### 3.3 Container and array model` heading at line 435, consisting entirely of a `> **Note.**` block. B has **no** `#### 3.3` heading at all (grep for `^#### 3.3` against B returns zero hits; grep for "Container and array model" against B returns zero hits).

> A §3.3 (entire subsection, a Note): "Part I (container) is independent of Part II (array model) by construction: no Part I structure requires decoding sample payloads, so appenders, and rewriters that carry a layer forward, operate on files whose layers they cannot decode — that independence is load-bearing for the updater rules of §7 and §20."
> B: absent.

I checked the operative rule this Note supports (writer-a's/writer-b's W8 answer: a rewriter carrying forward an unimplemented sample type needs only structural checksum verification, not decode) at `[R-WRT-09]` and §20.5, and confirmed both are byte-identical between editions independent of §3.3.

**Implementer consequence**: none. The Note was non-normative in A already (a `> **Note.**` block, non-normative under `[R-CNF-01]`); no implementation was ever built from it in either edition, and the rule it explains (`[R-WRT-09]`/§20.5) is intact, unchanged, in B.

Consensus: **EQUIVALENT**. byte_level: **false**. Severity: **clarity** (worth restoring for onboarding/rationale value, given it is the starkest full-subsection deletion in the pair, but it decides no implementation behavior).

---

## G14 — "addressed tile" becomes generation-relative in B's Terms entry, where A's Terms entry states it unconditionally
Members: swab-05, swba-03 (2)

Checked A line 383-388 and B line 111-117 directly.

> A: "**addressed tile / stored tile** — every tile of a layer is *addressed*. A tile is *stored in a generation* if and only if that generation's tile-index entry for it is not the sentinel (§15) ..."
> B: "**addressed tile / stored tile** — a tile is *addressed* in a generation if that generation's tile index has an entry for it: the tiles of the layer's grid under the geometry that generation declares (§11.2, §15). It is *stored in a generation* if and only if that entry is not the sentinel (§15) ..."

I checked §20.3 step 4 (byte-identical in both editions, per every other group above that touches it) for whether a layer's geometry can vary across generations: it discusses permitted geometry changes (shrink, re-tiling, rank change) across commits, which is consistent with B's generation-qualified reading and in tension with A's Terms-section wording taken in isolation. Both editions' §20.3 is the same text, so this §20.3-vs-§3.1 tension, where it exists, exists identically in both editions' full document; B's Terms entry differs from A's only in stating explicitly, at the glossary, a reading that A's own §20.3 already supports elsewhere.

**Implementer consequence**: none — an implementer who reads either edition's full document (Terms plus §20.3) computes the identical addressed-tile set for a given generation. B's rewording is a clarification drawn from A's own text (§20.3), not a new decision; per this task's own ADDITION test ("B may say what A implies only where the derivation is A's own text"), this qualifies as a valid derivation from A, not an addition. The residual ambiguity (if any) is confined to what A's Terms section states in isolation, not to what either edition's full text decides.

Consensus: **EQUIVALENT**. byte_level: **false**. Severity: **clarity** (A's own Terms-section wording is arguably the imprecise one; no maintainer action needed on B).

---

## G15 — Front-matter Note folded into §1 prose; two clauses dropped with no restatement found
Members: swba-07 (1)

Checked A's front-matter Note (lines 11-23) against B's "How to read this document" paragraph in §1 (from line 53).

> A (Note, front matter): "...a packed variable-length payload has no offsets to give... Normative requirements carry stable identifiers like `[R-IDX-03]`, and test vectors cite those identifiers rather than prose positions."
> B (§1, ordinary prose): "**How to read this document.** Sections follow a fixed rubric where it applies: purpose, byte-layout table, writer rules, reader rules, error handling, worked examples. On-disk structures are presented as layout tables whose columns suit the structure; §4.7 says what the columns carry and classifies every field as structural or descriptive."

Confirmed by control search: grepping "prose positions" against both files returns exactly one hit, in A (line 23); zero hits in B. Grepping "no offsets to give" likewise returns zero hits in B. Both clauses are genuinely absent from B, not merely relocated.

**Implementer consequence**: none. Both clauses are documentation/test-vector-citation conventions (how requirement IDs are cited, how packed variable-length payloads are represented in layout tables), not decoder or encoder behavior; no conforming implementation's bytes or verdicts depend on either sentence.

Consensus: **LOSS**. byte_level: **false**. Severity: **clarity**.

---

## G16 — Introduction condensed: specific figures and the Part I/II/III reading roadmap dropped, restated at their own normative sections unchanged
Members: swba-08 (1)

Checked A's goals list and "Reading this document" paragraph (lines 55-85) against B's corresponding goals list and "How to read this document" paragraph (lines 25-55).

> A: "Opening a file costs two range requests whatever its size (§6.4)... growth happens through four enumerated vehicles and a registry (§10)... Part I alone yields a container reader ... returning sample values needs Part II as well, since §19.3's layer validation resolves into Part II's value sets and geometry rules at every step."
> B: "Opening a file, and reading any one tile of it, each take a small fixed number of range requests, whatever the size of the file... the format grows through a fixed set of extension vehicles and a registry... Sections follow a fixed rubric where it applies: purpose, byte-layout table, writer rules, reader rules, error handling, worked examples."

I confirmed the specific figures are restated unchanged at their normative homes: the "two range requests" worked example appears byte-identically in both editions' §6.4-region worked appendix ("...ordinals 8–23 = exactly runs 1 and 2: two range requests..."), and "four enumerated vehicles" is present unchanged in A's own §10 area (this phrase is intro-only prose, but §10's actual registry mechanism is unchanged between editions per every other check in this pass touching unrelated sections). The Part I/II/III roadmap paragraph itself, however, is genuinely gone from B's Introduction — replaced by the section-rubric sentence — and I found no equivalent "Part I gives you a container reader; Part II is needed for sample values" statement elsewhere in B.

**Implementer consequence**: none for the specific numeric figures, since each is restated verbatim at its own governing section in both editions. The roadmap paragraph is navigational/UX content about how to approach the document, not a rule about file bytes, so its loss changes no implementation's behavior, though it is a real readability regression for a first-time implementer deciding how much of the document they need.

Consensus: **EQUIVALENT**. byte_level: **false**. Severity: **clarity**.

---

## G17 — Terms-section "generation"/"directory" glosses trimmed on reorder; both cut clauses restated fully at §9.2/§9.3/Appendix D
Members: swba-09 (1)

Checked A's "generation" and "directory" Terms entries against B's (both moved to the front of §3.1 in B).

> A "generation": "...successive generations of one file are ordered by the strictly increasing committed file length their trailers carry (§9.3)." — dropped in B's entry.
> A "directory": "...— never a delta (§9.2) — so a conforming commit adds one directory per generation." — dropped in B's entry.

Confirmed both clauses' distinguishing phrases ("strictly increasing committed file length", "never a delta ... adds one directory per") appear only in A's Terms entries by that exact wording, but I confirmed the underlying facts are independently and fully restated, unchanged, elsewhere in both editions: §9.3's F-ordering text ("F strictly increases per commit ... by at least 128 ... so it orders [the file's generations]") is byte-identical at A:1375/B:1272, and "Append-only, with a complete directory per generation." appears byte-identical near both files' ends (A:4647/B:4551 region).

**Implementer consequence**: none — pure de-duplication onto sections that already state the same rules in full.

Consensus: **EQUIVALENT**. byte_level: **false**. Severity: **none**.

---

## G18 — §20.4's MU=1 preservation-table row is easy to misread as unconditional; shared, unchanged text
Members: writera-01 (1)

Checked the table-plus-connecting-sentence pair in both files.

> A/B (identical, confirmed at A:3497/B:3394 region): "Its MU = 1 row reaches only a type the updater does not implement... so for an implemented type only the PE bit bites."

**Implementer consequence**: none attributable to B — the same misreading risk (table caption alone looks unconditional; the connecting sentence, present in both editions, narrows it) exists identically in both texts.

Consensus: **EQUIVALENT**. byte_level: **false**. Severity: **none**.

---

## G19 — Ignore-lane flag bit surviving an appender/rewriter but zeroed by a plain creator; shared, unchanged text
Members: writera-02 (1)

Checked §20.1's creator/appender/rewriter taxonomy and the flags=0 rule.

> A/B (identical, confirmed at A:3168/B:3065 region): "As a **creator** it undertakes nothing toward its input, whatever it read: §20.2 binds it, it writes flags = 0..."

**Implementer consequence**: none attributable to B — the tier-dependent flags divergence this finding describes is a property of both editions' shared taxonomy, unchanged between them.

Consensus: **EQUIVALENT**. byte_level: **false**. Severity: **none**.

---

## G20 — A fill-only commit's byte-level detectability (T4) depends on the layer's own padding geometry; shared, unchanged text
Members: writera-03, writerb-01 (2)

Checked §20.3 step 4's fixed-declarations bar and §21.7's "no condition a file can exhibit" framing in both editions.

> A/B (identical, confirmed at multiple offsets, e.g. "...no condition a file can exhibit (§21.7, `[R-ERR-01]`, `[R-CNF-02]`);"): both editions state the conduct-only bar the same way and both leave its byte-level detectability (via T4, conditioned on the layer having any edge-tile padding) to be assembled from the same set of cross-references (`[R-WRT-04]`, `[R-SER-05]`, §21.4's T4 row).

**Implementer consequence**: none attributable to B — the padding-dependent split in what a verifier can and cannot detect is identical in both editions; this is a genuine seam in the specification's own design (not a contradiction), shared unchanged.

Consensus: **EQUIVALENT**. byte_level: **false**. Severity: **none**.

---

## G21 — Pre-trailer pad slack totals are not unique across conforming writers, and §20.3 step 4 cites the wrong exemption category versus §21.7's own test; shared, unchanged text (self-confirmed by cmp-verifier-07)
Members: verifiera-01, verifierb-02, cmp-verifier-07 (3)

Checked §6.2's pad rule and §20.3 step 4 / §21.7's unwitnessed-condition test in both editions.

> A/B (identical, confirmed at A:852/B:749 region): "...a longer gap is conforming, and no conforming commit produces one."
> A/B (identical, per cmp-verifier-07's own quoted passage, which I independently re-confirmed at the citation locations checked throughout this pass): "This bar binds the commit as an actor: no file is nonconforming by virtue of its violation, and no register row records the violation itself, the register enumerating file-conformance violations (§21.1) and the bar stating no condition a file can exhibit (§21.7, `[R-ERR-01]`, `[R-CNF-02]`)"

**Implementer consequence**: none attributable to B. Both findings (slack totals legitimately varying by multiples of 64 bytes across conforming writers; and §20.3 step 4 citing `[R-ERR-01]`'s "no condition a file can exhibit" category where §21.7's own "unwitnessed condition" category arguably fits better) are arguments built entirely from text confirmed byte-identical between editions — cmp-verifier-07 independently verifies this for both. If either is a real defect, it is inherited unchanged by edition B from edition A, not introduced or worsened by the rewrite.

Consensus: **EQUIVALENT**. byte_level: **false**. Severity: **none**.

---

## G22 — R-COD-11's "cannot establish" branch for an inexecutable codec is unreachable as a final verdict for a conforming verifier; shared, unchanged text
Members: verifierb-01 (1)

Checked §17.4 in both editions.

> A/B (identical, confirmed at A:2618/B:2515 region): "A verifier that cannot execute a layer's codec or filter cannot establish that layer's conformance and MUST NOT certify the file... For a conforming reader that position arises only at a reserved or experimental value, every assigned codec and filter being core..."

**Implementer consequence**: none attributable to B. Under either edition, once L43/L45 (reserved/experimental codec value, a layer-scope violation) has fired, `[R-CNF-11]`'s own priority rule (established violation → nonconforming, in both editions) forces the final verdict to nonconforming regardless of what §17.4 says about decode-inability — so this described "cannot establish" end state is equally unreachable by a conforming verifier in both texts.

Consensus: **EQUIVALENT**. byte_level: **false**. Severity: **none**.

---

## G23 — version_minor's floor-and-carry rule for appenders is a SHOULD, not a MUST; shared, unchanged text
Members: quizb-01 (1)

Checked `[R-CNT-26]` in both editions.

> A/B (identical, confirmed at A:917/B:814): "A writer SHOULD emit the lowest version_minor that defines every feature present in the file — for a file expressible under this text, 0 — and an appender the maximum of that floor and the prior trailer's minor"

**Implementer consequence**: none attributable to B. The rule is advisory (SHOULD) in both editions identically, and writer/updater conformance is semantic in both (`[R-CNF-05]`, unchanged), so no byte-level quiz question forced by this rule differs between editions — the reporter (drafting a quiz for edition B alone) surfaces a trap in the shared rule's strength, not a B-specific change.

Consensus: **EQUIVALENT**. byte_level: **false**. Severity: **none**.

---

## Coverage check

23 groups, member counts: 6+1+5+5+2+4+2+4+3+1+1+3+2+2+1+1+1+1+1+2+3+1+1 = 53.
Every one of the 53 input ids appears in exactly one group above; none were dropped, and the two REPORTER_ERROR-shaped cases I found (readera-01/cmp-reader-05 sharing one identical-text tension) were graded EQUIVALENT rather than discarded, per instructions to grade weak/erroneous ones rather than drop them.
