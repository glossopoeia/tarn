# Triage pass — implementer-consequence lens

## Disclosures (mandatory, before any grading)

1. A relayed "user request" (the single word "Go") appeared above the computed
   brief for this run. Per the brief's own instructions, this is the message
   that launched the round at the orchestrator level, carried out before this
   pass was spawned; it is not a task for this pass, needs no reconciliation
   with the brief, and does not widen the brief's access rule. No action was
   taken on it.
2. Before this pass began, the runtime had already placed into context: the
   project's CLAUDE.md pointer (to AGENTS.md, not opened — out of the access
   rule's scope), a block of the user's cross-session auto-memory notes about
   this same TARN harness project, a git-status snapshot, and a commit-message
   attribution template. None of that material was read as part of this
   triage, none of it is evidence for any finding below, and none of its
   content is repeated here beyond this one acknowledgment.
3. Working file for this pass: this transcript, at
   `/private/tmp/claude-501/-Users-robertkleffner-Documents-GitHub-tarn-first-draft/fidelity-4/scratch/triage/transcript-triage-implementer.md`.
   Only edition A (`scratch/cleanroom/editions/a/tarn.md`) and edition B
   (`spec/tarn.md`) were opened by name for verification, by `sed`/`grep`
   line-range and phrase extraction. No directory was listed. No other file
   (docs/, PLAN.md, OPEN-QUESTIONS.md, AGENTS.md, README.md, conformance/,
   spec/registry.json, git history, the web) was read. The 38 findings and
   their quotations were taken only from the computed task text itself, not
   independently re-opened as transcript files (the walks' full transcripts
   were available under `fidelity-4/out/transcript-*.md` but were not needed
   to re-derive any grade below; every grade rests on my own re-reading of A
   and B at the cited sections).

## Method

For every one of the 38 input ids I re-read both editions at the section(s)
the finding cites, using targeted `grep -n` and `sed -n` extraction (never a
directory listing), confirming or correcting each quotation against the live
file text. Both files are hard-wrapped; several of my own first greps for a
multi-word phrase returned zero hits only because the phrase broke across a
line (" row\nrecords", "nothing toward its\ninput"); each such zero was
re-checked by searching a shorter fragment before being trusted, per the
brief's warning.

I deduplicated by underlying difference (or underlying shared defect), not by
report. Several of the 38 reports are independent rediscoveries of the exact
same textual fact (a comparator and a lone walker citing the same passage;
two lone walkers on opposite editions finding the same unaddressed gap because
the gap is edition-invariant). `cmp-verifier-04` is a compound comparator
finding that itself asserts two unrelated equivalences (the codec-incapable
verifier-classification question, and the "unwitnessed" cross-generation
question); I have filed its one id under the group whose title it leads with
(verifier classification), and cross-referenced its second half under the
unwitnessed group without double-counting its id.

## Groups

### G1 — reader outcome-class gap for a core-but-unimplemented codec/filter
Members: cmp-reader-01, readera-01, readerb-01
Consensus: EQUIVALENT (edition-invariant; no A-vs-B difference exists to grade)
Severity: none (as a fidelity defect of B; it is a real pre-existing spec gap in *both* editions, flagged for the maintainer separately from the fidelity question)
Byte-level: false

Checked passages: A/B §2.3 conforming-reader bullet (`R-CNF-03`), A/B §17.4
`R-COD-11`, A/B §21.9 `R-ERR-04` citations, A/B §21.6 closing paragraph. I
diffed §17.4 in full (A lines 2614–2630 vs B lines 2458–2474): byte-identical
in substance. The §2.3 conforming-reader bullet's core sentence ("There are no
subset profiles... not a conforming reader, even if it reads all other
conforming files correctly. `[R-CNF-03]`") is identical in both (A ~192–196, B
~225–229). §17.4's own narrowing sentence ("For a conforming reader that
position arises only at a reserved or experimental value... software unable
to execute an assigned codec or filter is not a conforming reader") is
word-for-word identical in both editions.

> A (§17.4): "For a conforming reader that position arises only at a reserved
> or experimental value, every assigned codec and filter being core: it
> rejects the layer (`[R-COD-03]`, `[R-COD-09]`); software unable to execute
> an assigned codec or filter is not a conforming reader (`[R-CNF-03]`)."
> B (§17.4): identical, verified byte-for-byte over the full paragraph.

Implementer consequence: the gap is real — software missing a core codec such
as zstd is, by R-CNF-03's own terms, outside the "conforming reader" class
altogether, and neither edition's register (§21.6, §21.9) assigns that
software's behavior an outcome class. Three implementations (whole-file
refusal, layer-only refusal, garbage/fill passthrough for that layer) are all
equally "consistent" with either edition's silence. But since the controlling
text is byte-identical between A and B, this is not a fidelity gap — nothing
a builder working from B alone would do differently than a builder working
from A alone. It is the same open question inherited unchanged. Recommended
action: outside this round's scope (B did not introduce or repair it); worth a
separate maintainer ticket to assign this case a register row or an explicit
outcome class in the next revision of the *shared* text.

### G2 — verifier classification ambiguity for codec/filter incapacity
Members: cmp-verifier-04, verifiera-01, verifierb-01
Consensus: EQUIVALENT (edition-invariant)
Severity: none (as a fidelity defect; a real shared spec ambiguity, noted for the maintainer)
Byte-level: false

Checked: A/B §2.3 (`R-CNF-03`, `R-CNF-11`), A/B §17.4 (`R-COD-11`). Same
passages as G1, read for the different question: whether software that lacks
a core codec can still be a "conforming verifier" issuing valid cannot-establish
verdicts for other files. `R-CNF-03`'s "no subset profiles... not a
conforming reader" sentence and `R-COD-11`'s cannot-establish sentence are
each identical in both editions (confirmed above), so the tension between a
class-level absolute bar and a file-by-file capability carve-out is present,
unresolved, in A exactly as in B.

> A (§17.4): "A verifier that cannot execute a layer's codec or filter cannot
> establish that layer's conformance and MUST NOT certify the file."
> B (§17.4): identical.

Implementer consequence: two implementations built from either edition alone
can diverge on whether a verifier lacking lz4 may certify other files at all —
but that divergence is possible from A alone just as much as from B alone;
there is no edition-attributable byte or verdict difference. Recommended
action: maintainer ticket on the shared text, not a fidelity fix to B.

(cmp-verifier-04's second half — the "unwitnessed" cross-generation
observation — is covered under G3 below; its content is folded into this
id's single group placement per the dedup note above, but the substantive
claim is addressed at G3, not re-argued here.)

### G3 — §20.3's fixed-declaration conduct bar has no independent file-conformance witness (fill-value case and the general "unwitnessed" framing)
Members: cmp-writer-01, writera-01, writerb-02, verifierb-02
Consensus: EQUIVALENT / OBSERVATION (edition-invariant shared fact, not a fidelity difference)
Severity: none
Byte-level: false (as an A-vs-B question); true as a same-edition implementer trap, but that is not what this round grades

Checked: A/B §20.3 step 4's "stored a tile... (a fill value, a type, a tile
extent)... is not an appender's operation at all" passage (A lines
3447–3453, B lines 3250–3256) — byte-identical modulo an em-dash/parenthesis
and em-dash/semicolon punctuation substitution. Also A/B's "no file is
nonconforming by virtue of its violation, and no register row records the
violation itself" sentence (A line ~3277, B line ~3092) — identical (my first
grep for "no register row records" returned zero for B only because the
phrase wraps across a line break there; a second, shorter search confirmed
it). Also the symptomatic-row parenthetical "(T3, T14, T21, T22, T4, T5, T2)"
and "(T17, T24, T25)" — identical lists, identical order, in both editions.
Also §21.7's "unwitnessed" definition — present, substantively identical, in
both editions (A ~4096–4127, B ~3896–3927).

> A/B (§20.3): "This bar binds the commit as an actor: no file is
> nonconforming by virtue of its violation, and no register row records the
> violation itself, the register enumerating file-conformance violations
> (§21.1) and the bar stating no condition a file can exhibit (§21.7,
> `[R-ERR-01]`, `[R-CNF-02]`)."

Implementer consequence: for a layer whose stored tiles have no edge padding
(extent an exact multiple of tile extent), a fill-value-only commit that
violates the §20.3 conduct bar leaves a file that passes every stated §21
check (T4 has nothing to examine without a padding position) and that a
conforming verifier may certify. This is a real, concrete, byte-level fact
about the one format — but it is the same fact in A as in B, stated with the
same witness list and the same conduct/predicate split in both. No builder
working from B alone emits, accepts, or certifies a different byte or file
than one working from A alone. Recommended action: none for fidelity; this is
an implementer-facing trap in the shared design, not a translation defect.

### G4 — worked Note on the format-major "reach" test (F14/F5/F15) dropped
Members: swab-01
Consensus: LOSS
Severity: content (explanatory; no byte consequence)
Byte-level: false

Checked: A §2.3 closing Note (A lines ~285–293) — present; grepped B for "F14
reaches" and "does not reach": zero hits — confirmed absent from B entirely.
Checked A/B §21.2's governing sentence ("yields F8, F14, F6 and both of F1's
instances... and no other row") — byte-identical in both (A ~3838, B ~3630).

> A (§2.3 Note): "§21.2's F14 reaches although the bytes it checksums include
> fields a future major may redefine... F5 does not reach although its
> subject is the physical file size... F15 does not reach although its
> Governing rule cell cites `[R-CNT-24]`..."
> B: absent (confirmed by direct search; zero hits for any of the three
> row-ids in this context).

Implementer consequence: none. The register-row list that actually decides
which conditions reach a foreign format major is unchanged and identical in
both editions; the dropped Note only walks a reader through *why* F14, F5 and
F15 land where they do. A verifier built from B alone derives the identical
reach/no-reach verdict for every row from the unchanged list alone.
Recommended action: a maintainer may want the worked contrast restored for
readability, but it is not required for conformance.

### G5 — Note that "reject" names a scope of unusability, not a UI requirement, dropped
Members: swab-02, adv-02, swba-02
Consensus: LOSS
Severity: none (the dropped text was itself a Note, non-normative under `[R-CNF-01]` even in A)
Byte-level: false

Checked: A §2.4 closing Note (confirmed present, immediately before §2.5, A
line ~340). Grepped B for "not user interface" and "prescribes the scope":
zero hits in B — confirmed fully absent, no restatement anywhere.

> A (§2.4, Note): "'Reject' prescribes the scope of unusability, not user
> interface: how failure is reported is implementation technique."
> B: absent.

Implementer consequence: none whatsoever that a byte or verdict test can
register. The dropped sentence was already excluded from this document's
normative text in edition A by `[R-CNF-01]` (Note/Example/Rationale blocks are
non-normative); its disappearance from B cannot turn a non-normative sentence
into a missing *rule*, because it was never one. Recommended action: none
required; restoring it is a pure readability nicety.

### G6 — sentence pair on non-violation ignore-record vocabulary and preserve-verbatim's orthogonality to reader outcomes, dropped
Members: swab-03, adv-01, swba-01, cmp-reader-04
Consensus: LOSS
Severity: content (not byte-level — see rationale)
Byte-level: false

Checked: A §2.4, immediately after the `[R-CNF-07]` outcome-vocabulary
sentence (A lines ~299–303) — present. B's §2.4 at the identical point goes
straight from the `[R-CNF-07]` citation into the outcome table (B lines
~298–299) — both sentences confirmed absent. Checked B §20.4's preservation
table (B lines ~3277–3311): the table's obligations are keyed purely to the
record's own stored MU/PE flags (`[R-CNT-22]`, `[R-CNT-12]`), never to
whatever a *reader* separately decided to do with the record, and this table
is unchanged in substance between editions. Checked §21.6's own usage of
"Ignored" for non-violation rows (e.g. the experimental-range metadata-
encoding row): present identically in both.

> A (§2.4): "The same vocabulary is used for defined conditions that are not
> violations (an unknown ancillary record is *ignored*, not rejected).
> **preserve-verbatim** names an updater obligation, orthogonal to reader
> outcomes: a record a reader ignores can still be one an updater preserves."
> B: absent — §2.4 ends at "...reject-tile, or ignore-record. `[R-CNF-07]`"
> and proceeds directly to the outcome table.

Implementer consequence (re-judging swba-01's stronger byte-level claim
against the other three reporters' non-byte-level LOSS): swba-01 argues an
updater built from B alone, lacking this explicit bridge sentence, "risks
treating a reader-ignored record as safe to drop rather than preserve." I
checked this directly: §20.4's table is self-contained — it states the
updater's preservation obligation keyed to the record's own MU/PE bits, with
no dependency on, or even a forward reference to, §2.4's reader-outcome
vocabulary. An implementer who read only §20.4 (which every updater
implementation must read to know what to do with any record, regardless of
what §2.4 says) gets the complete, correct rule in both editions equally.
swba-01's risk scenario requires an implementer to derive updater behavior
from §2.4 while skipping the unchanged, controlling §20.4 table outright —
not a reading failure this fidelity defect itself causes. I side with
swab-03/adv-01/cmp-reader-04: this is a real content loss (an explanatory
bridge connecting two already-complete, already-unchanged rules) but not
byte-level. Recommended action: restore the bridge sentence for readability;
not required for correctness.

### G7 — entire §3.3 subsection (Part I/Part II independence) dropped
Members: swab-04, adv-03
Consensus: LOSS
Severity: none (the dropped text is itself a Note, non-normative under `[R-CNF-01]`)
Byte-level: false

Checked: A has `#### 3.3 Container and array model` (A line 435), a one-
paragraph Note. B has no `3.3` at all — B's §3 heading list is `3.1 Terms`
(B line 62), `3.2 The reference array` (B line 125), then `2.2`/`2.3` (B's
reordering places §2 after §3). Grepped B for "Container and array model" and
"independent of Part II": zero hits in either case — confirmed, no
restatement anywhere in B, including inside the §7 and §20 passages the Note
itself calls load-bearing for.

> A (§3.3, Note): "Part I (container) is independent of Part II (array model)
> by construction: no Part I structure requires decoding sample payloads, so
> appenders, and rewriters that carry a layer forward, operate on files whose
> layers they cannot decode — that independence is load-bearing for the
> updater rules of §7 and §20."
> B: absent.

Implementer consequence: none. Every specific rule this Note explains (an
appender copying an unrecognized record's extent without decoding it; a
rewriter relocating a tile index without decoding tile payloads) is
independently and completely stated with its own MUST/MUST NOT language in
§7.2 and §20.1–§20.5, confirmed unchanged between editions elsewhere in this
pass (G3, G19). The dropped text is architectural commentary justifying why
those already-complete rules can coexist, not an additional constraint on
bytes. Recommended action: a maintainer concerned with onboarding new
implementers may want this restored somewhere in B's Part II front matter;
not required for conformance.

### G8 — Note distinguishing general bit-numbering from §14's boolean-sample mapping, dropped
Members: swab-05
Consensus: LOSS
Severity: none (Note, non-normative)
Byte-level: false

Checked: A §4.4 closing Note (A lines 509–510) — present. Grepped B for "bit
numbering in flags" and "mapping of boolean": zero hits — confirmed absent.
Confirmed `[R-ENC-08]` (the rule this Note annotates) is not cited anywhere
else that depends on this specific pointer, in either edition.

> A (§4.4, Note): "This rule fixes bit numbering in flags and packed fields
> generally; the mapping of boolean *samples* to bits is defined in §14."
> B: absent.

Implementer consequence: none. §14.3's packed-boolean-plane bit-k-of-byte-
k-div-8 mapping is stated completely and independently in both editions; the
dropped Note was a cross-reference between two already-separate,
already-complete rules, not a rule itself. Recommended action: none required.

### G9 — second half of the §4.7 Field taxonomy Note dropped
Members: swab-06
Consensus: LOSS
Severity: content/clarity (no byte consequence)
Byte-level: false

Checked: A §4.7 closing Note's second half (A lines 622–627) — present.
Grepped B for "A name is structural", "worked numeric example", "paired
conformance vector", "appear once in Appendix B": zero hits for all four —
confirmed none restated anywhere in B. Confirmed the F4/L9 duplicate-layer-
name violation rows are registered, identically worded, in §21.2 of both
editions regardless of whether §4.7 separately calls names "structural".

> A (§4.7, Note, second half): "A name is structural: a duplicate is a
> validity error at file or layer scope (`[R-ENC-15]`, F4, L9)... Every
> non-obvious encoding is followed by a worked numeric example, and every
> sentinel or overloaded encoding additionally has a paired conformance
> vector. All named constants appear once in Appendix B."
> B: absent.

Implementer consequence: none. The one operative claim buried in this half
(duplicate names are a validity error) is independently and identically
registered at F4/L9 in both editions' §21.2; the rest are claims about the
document's own authoring conventions (worked examples exist; constants are
listed once in an appendix), not requirements on an implementation's bytes.
Recommended action: none required for conformance; a style note for the
maintainer only.

### G10 — §1 Introduction's "Part I alone yields a container reader" claim dropped
Members: swab-07
Consensus: LOSS
Severity: none (§1 is itself excluded from normative text by `[R-CNF-01]` in both editions)
Byte-level: false

Checked: A §1 closing paragraph (A line 89) — present. Grepped B for "Part I
alone yields" and "container reader": zero hits — confirmed absent, and B's
replacement "How to read this document" paragraph covers a different topic
(the document's own rubric and field classification) with no restatement of
the capability-split claim anywhere.

> A (§1): "Part I alone yields a container reader — one that opens files,
> walks the directory, and lists layers without decoding a sample; returning
> sample values needs Part II as well, since §19.3's layer validation
> resolves into Part II's value sets and geometry rules at every step."
> B: absent.

Implementer consequence: none. §1 is non-normative in both editions
(`[R-CNF-01]`); the claim is an orientation remark summarizing §19.1–§19.4's
actual algorithms, which are unchanged between editions. Recommended action:
none required; an onboarding nicety only.

### G11 — front-matter clause on test vectors citing requirement identifiers, dropped when folded into §1
Members: swab-08
Consensus: LOSS
Severity: none
Byte-level: false

Checked: A's pre-§1 front-matter Note (A line 22) — present. Grepped B
("cite those identifiers", "test vectors cite"): zero hits — confirmed
absent. Checked B §2.2 ("Identifiers are stable: they are never renumbered or
reused..." — B lines 168–175): states the general stable-identifier rule,
differently worded but matching in substance. Checked B §24's vector-manifest
format (B lines 4243–4253): each manifest entry is explicitly required to
record, for each damaged structure, "the §21 register row it exercises
together with that row's governing requirement identifier" — confirming the
operative mechanism this dropped sentence described is itself unchanged and
still mandatory in B.

> A (front matter): "Normative requirements carry stable identifiers like
> `[R-IDX-03]`, and test vectors cite those identifiers rather than prose
> positions."
> B: absent (§2.2 keeps the general stable-id rule; §24 keeps the manifest
> requirement to record the governing identifier — the specific sentence
> connecting the two is what is missing).

Implementer consequence: none. §24's manifest format, unchanged, already
forces every conformance vector to key off the requirement identifier rather
than a prose position; its absence from the introduction changes nothing a
vector-manifest author or consumer does. Recommended action: none required.

### G12 — glossary "addressed tile" definition: layer-wide (A) vs generation-relative (B)
Members: swba-03
Consensus: EQUIVALENT
Severity: clarity (B's phrasing is more precise, not differently normative)
Byte-level: false

Checked: A §3.1 Terms (A line 383): "every tile of a layer is *addressed*."
B §3.1 Terms (B line 112): "a tile is *addressed* in a generation if that
generation's tile index has an entry for it: the tiles of the layer's grid
under the geometry that generation declares (§11.2, §15)." Both confirmed
verbatim. Checked that neither glossary entry carries its own requirement ID
(none attaches to either sentence); the operative content — which positions
belong to a layer's grid at a given generation, and that extent MAY grow but
MUST NOT shrink across generations — lives in §11.1, §11.2, §15 and §20.3,
and I confirmed those sections' governing sentences are otherwise unchanged
between editions throughout this pass (the §20.3 extent-growth rule was
checked directly in G3; §15's tile-index entry layout was checked directly in
G18).

Implementer consequence: none. The glossary entry is informal prose with no
requirement ID of its own; whichever wording a reader takes from §3.1, the
actual addressed-tile logic a builder implements comes from §11.1/§11.2/§15/
§20.3, which decide the question identically in A and B. B's phrasing more
precisely anticipates the cross-generation growth case the normative sections
already govern, but it does not decide anything A's normative sections leave
open — A's informal "every tile... is addressed" was always read, in context,
against whichever generation's grid is current. Recommended action: none
required for conformance; worth adopting A's old wording's simplicity is not
worth the loss of B's precision, so no change recommended either way.

### G13 — verifier-a's V2 answer misattributes both F35 and F36 as independently firing
Members: cmp-verifier-01
Consensus: REPORTER_ERROR
Severity: none
Byte-level: false

Checked: A/B §21.1's specialization-list sentence (A line ~3771, B line
~3566): "...F35 of F36, L24 of L25, F21 of F22 and L10 of L11 stand in that
relation... the file is recorded against the narrower row, whose detector and
detection point are the ones that apply." Confirmed byte-identical in both
editions.

> A/B (§21.1): "Some rows are strict specializations of others: where every
> file exhibiting one row's condition... necessarily exhibits another's, the
> file is recorded against the narrower row... F35 of F36, L24 of L25, F21 of
> F22 and L10 of L11 stand in that relation."

Implementer consequence: none either way for accept/reject bytes — a
reserved-range top-level record carrying MU=1 is rejected either way the
register attribution goes. But as a register-row-attribution question this
rule is stated identically in A and in B, and resolves it to F35 alone, not
"both fire." Verifier-a's own V2 answer (reported inside this round, not an
A-vs-B difference) misreads a rule stated identically in the edition
verifier-a itself worked from; verifier-b's V2 answer applies the same rule
correctly to B. This is a reporter (walker) misreading, not an edition
difference. Recommended action: none for either edition's text.

### G14 — R-CNF-02's three inline conduct-rule examples and cross-reference sentence dropped from §2.3, each example independently restated at its own section
Members: cmp-verifier-02
Consensus: EQUIVALENT
Severity: clarity (no byte consequence)
Byte-level: false

Checked: A §2.3's `R-CNF-02` bullet (A lines 166–179) — carries the full
illustrative list and the "declared where it arises rather than enumerated
here" cross-reference. B's `R-CNF-02` bullet (B lines 202–210) — states only
the general rule, no illustrative list, no cross-reference sentence (grepped
B for "declared where it arises": zero hits). Checked each of the three named
examples at its own section in B: §6.3's ignore-lane-bit sentence ("A set
ignore-lane bit is nevertheless not a file-conformance violation", B line
~768) — present; §6.2's pre-trailer-gap sentence ("a longer gap is
conforming, though no conforming commit produces one", B line ~717) —
present; §20.3 step 4's fixed-declaration bar — present and confirmed
byte-identical in substance to A in G3 above. Checked the identical three
examples exist at A's own §6.2/§6.3/§20.3 sections too (not only inside the
§2.3 aggregating list): A §6.3 line ~902 ("a set ignore-lane bit is not a
file-conformance violation"), A §6.2 line ~845 ("a longer gap is conforming,
and no conforming commit produces one").

> A (§2.3, R-CNF-02): "§6.3's flags rules against a set ignore-lane bit...,
> §6.2's pre-trailer gap longer than `[R-LIF-02]` step 5's pad, and §20.3 step
> 4's bar on the fixed declarations of a layer that stores a tile are the
> cases this text states, and each is declared where it arises rather than
> enumerated here."
> B (§2.3, R-CNF-02): the general rule only, no illustrative list.

Implementer consequence: none. All three named conduct rules are present,
substantively unchanged (the "and"/"though" wording difference at §6.2 is
stylistic only), at their own sections in B; an implementer who follows the
rules where they actually bind (§6.2, §6.3, §20.3) rather than through the
§2.3 summary gets the identical behavior either edition. The loss is confined
to an expository aggregating list and a cross-reference sentence, not to any
rule content. Recommended action: none required for conformance.

### G15 — verifier's "cannot establish" grounds list relocated §2.3 → §21.6 closing paragraph
Members: cmp-reader-03, cmp-writer-05, cmp-verifier-03
Consensus: EQUIVALENT
Severity: clarity
Byte-level: false

Checked: A §2.3's conforming-verifier bullet (A lines 215–230) inlines the
full five-ground list for *cannot establish*. B's §2.3 (B lines 247–266)
abbreviates to "(§21.6 names the grounds)"; B's §21.6 closing paragraph (B
lines 3869–3876) restates the identical five grounds (unimplemented format
major; unimplemented MU=1 top-level type; unexecutable codec/filter, now
additionally cross-referencing §17.4; resource-declined layer/tile decode;
declined user-metadata decode), with the identical requirement-ID citations
(`[R-COD-11]`, `[R-ERR-04]`, `[R-SER-05]`, `[R-SER-08]`, `[R-MTA-09]`).

> A (§2.3): "...the last where some requirement is one it is unable to check
> on a capability or resource ground, as when the file names a format major
> version it does not implement, when a record carries MUST_UNDERSTAND = 1
> with a type it does not implement (§21.6), when it cannot execute a codec
> or filter (`[R-COD-11]`)... or when it declines to decode a user-metadata
> document (`[R-MTA-09]`)."
> B (§21.6 closing paragraph): "A verifier is unable to check a requirement
> on a capability or resource ground, and so reports *cannot establish*
> (`[R-CNF-11]`), as when the file names a format major version it does not
> implement, a record carries MUST_UNDERSTAND = 1 with a type it does not
> implement, it cannot execute a codec or filter (`[R-COD-11]`, §17.4)... or
> it declines to decode a user-metadata document (`[R-MTA-09]`)."

Implementer consequence: none. Every ground and every citation is present in
both editions; only the section housing them, and the depth of indirection
(§2.3 inline vs. §2.3-pointer-to-§21.6), differs. A verifier built from B
alone recognizes exactly the same five grounds as one built from A alone.
Recommended action: none required.

### G16 — user-metadata quarantine paragraph relocated §7.1 → §7.3
Members: cmp-writer-06
Consensus: EQUIVALENT
Severity: clarity
Byte-level: false

Checked: A §7.1 (A lines 978–1004) carries the full metadata-compression and
quarantine paragraph. B §7.1 (B lines 829–837) is reduced to a two-sentence
stub about the directory region's own CRC; B §7.3 (B lines 940–970) carries
the metadata-compression sentence and the full quarantine paragraph, reworded
but preserving every obligation: extent-slot validity (`(0,0)` or
`extent_length < 5`), encoding values, ignore-record/SHOULD-report, the
`[R-CNF-08]` owning-scope override, and the resource-decline carve-out
(`[R-MTA-09]`, `[R-ERR-04]`).

> A (§7.1): "User metadata is quarantined: each way a user-metadata record's
> document can be unreadable once its framing has been read... is
> ignore-record with a SHOULD-report, notwithstanding the owning-scope
> mapping of `[R-CNF-08]`."
> B (§7.3): "User metadata is quarantined. Once a user-metadata record's
> framing has been read, each way its document can be unreadable is
> ignore-record with a SHOULD-report... The quarantine overrides the
> owning-scope mapping of `[R-CNF-08]`..."

Implementer consequence: none. Every obligation is present, in substance, in
both editions; only the section number housing it differs (§7.1 vs §7.3).
Recommended action: none required.

### G17 — rewriter ignore-lane-bit restatement at §6.3 dropped, rule survives once at §20.5
Members: cmp-writer-04
Consensus: EQUIVALENT
Severity: clarity
Byte-level: false

Checked: A §6.3 (A lines 906–908) includes, immediately before the general
updater sentence, "A rewriter, though its output is a new file, carries the
input's unknown ignore-lane bits into its output trailer rather than writing
flags = 0, and sets no other (§20.5, `[R-WRT-06]`)." B §6.3 (B lines 766–771)
goes directly from the ignore-lane-bit-is-not-a-violation sentence to "An
updater MUST copy forward unknown ignore-lane bits of its input file..." —
confirmed no separate rewriter sentence appears. Confirmed §20.5's own
`[R-WRT-06]`-adjacent text (checked under G3/G7 sweeps) is unchanged and
identical in both editions, and is the place a builder actually needs to
consult to implement a rewriter's trailer-flags behavior.

> A (§6.3): "A rewriter, though its output is a new file, carries the input's
> unknown ignore-lane bits into its output trailer rather than writing
> flags = 0, and sets no other (§20.5, `[R-WRT-06]`)."
> B (§6.3): absent (consolidated to §20.5 alone, identically worded there in
> both editions).

Implementer consequence: none. §20.5 states the rule, unchanged, in both
editions, and is the section a rewriter implementation must read regardless
of whether §6.3 also repeats it. Recommended action: none required.

### G18 — §15.1's tile-index region-layout blockquote is the document's one unlabeled (hence fully normative) blockquote, in both editions equally
Members: cmp-writer-03, writerb-03
Consensus: EQUIVALENT
Severity: none (as a fidelity question — the risk is real but edition-invariant)
Byte-level: false (A-vs-B); the underlying implementer risk is byte-level but shared

Checked: A/B §15.1 (A line ~2209, B line ~2065): "...with no padding anywhere
inside the region." — confirmed byte-identical, both unlabeled (no "Note",
"Example", or "Rationale" tag precedes either), in the identical structural
position ahead of the entry-layout table.

> A/B (§15.1): "[ entry array: entry_count × 20 bytes ] [ segment CRC array:
> ⌈entry_count / 2¹⁶⌉ × 4 bytes ]\n\nwith no padding anywhere inside the
> region."

Implementer consequence: real but shared. Under `[R-CNF-01]`, an unlabeled
blockquote is fully normative; this is the one place in the document stating
the tile-index region's internal byte ordering (entry array immediately
followed by segment-CRC array, no padding), which `[R-CNT-17]`'s
extent_length formula and `[R-IDX-01]`'s per-entry offset rule both silently
presuppose. A builder who applies a "blockquote = aside" heuristic instead of
checking the label could place the segment-CRC array first, or insert
padding, and disagree with a correct implementation — but this risk is
identical whether that builder worked from A or from B, since the passage is
byte-identical and identically unlabeled in both. Recommended action: none
required as a fidelity fix; worth flagging to the maintainer as a standing
clarity risk in the shared text (e.g. an explicit "no Note/Example/Rationale
label — fully normative" callout), independent of this round.

### G19 — a creator that decodes-and-re-emits an existing file writes flags=0, unlike an appender/rewriter; identical in both editions
Members: cmp-writer-02, writerb-01
Consensus: EQUIVALENT
Severity: content/clarity (a real, determinate rule — not an ambiguity — but edition-invariant)
Byte-level: false (A-vs-B); the rule itself is a real, determinate byte-level fact about the format, shared by both editions

Checked: A §20.1 (A lines 3168–3171, confirmed after accounting for a
mid-sentence line wrap that made my first phrase search return a false
zero): "As a **creator** it undertakes nothing toward its input, whatever it
read: §20.2 binds it, it writes flags = 0, and it answers for every byte of
its output (`[R-CNF-05]`), bytes it copied from another file included." B
§20.1 (B line ~2987): confirmed identical.

> A/B (§20.1): "As a creator it undertakes nothing toward its input, whatever
> it read: §20.2 binds it, it writes flags = 0, and it answers for every
> byte of its output (`[R-CNF-05]`), bytes it copied from another file
> included."

Implementer consequence: real and determinate, not an open question — a tool
that decodes a TARN file and writes a logically equivalent new file (rather
than appending under the same file_id, or rewriting under §20.5's fresh-
file_id procedure with its ignore-lane-copy-forward obligation) is a
*creator* under this sentence, and MUST write flags = 0, silently losing any
feature signalled only by a later-minor ignore-lane bit it decoded. This is a
genuine, citable, byte-level fact about which trailer bytes such a tool must
emit — but it is the identical fact in A as in B, resolved by identical text
in both. No builder working from B alone reaches a different flags-field
byte than one working from A alone. Recommended action: none required for
fidelity; worth flagging to the maintainer as a trap for tool authors,
independent of this round, since it is easy to miss that reading an existing
file demotes a tool to "creator" tier rather than "appender."

### G20 — B drops A's aside deriving that an unimplemented MU=1 top-level type in a conforming file must be experimental-range
Members: cmp-reader-02
Consensus: EQUIVALENT
Severity: clarity
Byte-level: false

Checked: A §2.3 conforming-reader bullet (A lines 180–184): "...carrying no
top-level record of a type it does not implement with MUST_UNDERSTAND = 1 —
in a conforming file such a type is necessarily from the experimental range,
since a reserved-range type carrying MU = 1 is itself a violation — and
none of whose values exceeds..." B's corresponding sentence (B lines 219–221)
omits the dashed aside entirely, going straight from "...MUST_UNDERSTAND = 1
and none of whose values exceeds..." Checked §21.6's register row F36 in
both editions: "emitting one is a violation whatever its MU bit" —
confirmed present identically in both, which is the independent rule from
which B's reader can still derive the same fact (a conforming file's
unimplemented-type MU=1 record cannot be reserved-range) without the aside.

> A (§2.3): "...in a conforming file such a type is necessarily from the
> experimental range, since a reserved-range type carrying MU = 1 is itself
> a violation..."
> B: absent — the sentence skips directly from the MU=1 clause to the
> §21.9-limits clause.

Implementer consequence: none. The fact the aside derives is independently
and completely fixed by §21.6's F36 row (reserved-range emission with any MU
bit is itself a violation) in both editions; the aside only walked the
reader through the inference, it did not supply the only route to it.
Recommended action: none required.

### G21 — probe R4's field names (extent_offset/extent_length) do not match the document's tile-index-entry field names (offset/length)
Members: readera-02
Consensus: REPORTER_ERROR
Severity: none
Byte-level: false

Checked: A §15.1's tile-index entry layout table ("offset" / "length" / crc,
A §15.1 table) versus A §7.2's record-framing table, which is where
"extent_offset" / "extent_length" actually name fields (A lines 1007–1018,
confirmed: these are the generic 24-byte record header's extent-slot fields,
a different structure at a different scope, never tested against an
all-ones sentinel anywhere in the text).

Implementer consequence: none — this is not a text defect of either edition;
it is a naming mismatch in the probe's own wording against the document's
actual (and internally consistent) terminology. Read charitably by
substituting the entry's correct field names, the condition maps cleanly
onto register row T7, with no indeterminacy in the source text. I classify it
REPORTER_ERROR in the sense the fidelity test uses the term: no divergence
between the editions is implicated, and the only "error" is in how a probe
(not either edition's own prose) named a field. Recommended action: none for
either edition's text.

## Coverage check

All 38 input ids are listed in exactly one group above. Counted by hand
against the group member lists: G1(3) + G2(3) + G3(4) + G4(1) + G5(3) + G6(4)
+ G7(2) + G8(1) + G9(1) + G10(1) + G11(1) + G12(1) + G13(1) + G14(1) + G15(3)
+ G16(1) + G17(1) + G18(2) + G19(2) + G20(1) + G21(1) = 38.
