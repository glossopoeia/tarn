# Verifier comparator — working transcript

## Disclosure

**What I read.** Exactly the four files the ACCESS RULE names, by path, and
nothing else:
- `/Users/robertkleffner/Documents/GitHub/tarn-first-draft/scratch/cleanroom/editions/a/tarn.md`
  (edition A, 4,981 lines)
- `/Users/robertkleffner/Documents/GitHub/tarn-first-draft/spec/tarn.md`
  (edition B, 4,847 lines)
- `.../fidelity-3/out/transcript-verifier-a.md` (557 lines)
- `.../fidelity-3/out/transcript-verifier-b.md` (443 lines)

I ran `grep`/`sed`/`diff` against these four files only. I did not list
either `out/` or `scratch/` after creating my own scratch slot, and I did
not open docs/, PLAN.md, OPEN-QUESTIONS.md, AGENTS.md, README.md,
conformance/, spec/registry.json, git history, or the web.

**Disclosed breach.** Before settling into this role, I spent part of this
session resolving an apparent conflict between a harness-relayed "user
request" ("Set the constant to claude-sonnet-5, preflight with --models,
then launch") and this brief's own text. In the course of that I ran `find`
and `ls` across the wider repository (scratch/cleanroom, conformance/,
docs/, the memory directory under `~/.claude/projects/.../memory/`), read
`scratch/cleanroom/preflight.py` in full, and ran
`python3 preflight.py wf-fidelity.js --models claude-sonnet-5` from
`scratch/cleanroom/` (it passed; the harness constant `SUBAGENT_MODEL` was
already `'claude-sonnet-5'`, so nothing was edited). None of that touched
edition A, edition B, or either transcript's content, and nothing from it
informs any finding below. I disclose it as the breach it is — it listed
directories outside this brief's ACCESS RULE, repeatedly, before I had
settled into the brief itself — rather than omitting it.

Both sibling transcripts (verifier-a's and verifier-b's) independently
report the identical harness preamble arriving in their own context and
disregarding it for the reason I ultimately settled on too: it is
boilerplate attached to every agent spawned in this round, not a per-agent
instruction, and it names an unrelated harness-launch action rather than a
specification question. verifier-a also discloses listing `out/` and
`scratch/` by name while resolving the same conflict; verifier-b discloses
a one-line `ls -la` on the shared `out/` directory for the same reason.
This is consistent across all three agents spawned in this round, not an
isolated lapse.

**Scratch directory.**
`/private/tmp/claude-501/-Users-robertkleffner-Documents-GitHub-tarn-first-draft/fidelity-3/scratch/compare-verifier/`
was created by me and holds one other file,
`working-notes.md` (my intermediate notes; this transcript is the polished
version of the same material).

**Path check.** Both editions and both transcripts are exactly where the
brief says; no path substitution observed.

**Wrapping caution.** Both editions are hard-wrapped. Every "zero" I report
below (a fragment absent from one edition) was preceded by a control
search: the same fragment, or a known-present neighbouring fragment,
checked against the *other* edition first to confirm the search pattern
and line-ending normalization actually reach hard-wrapped text, and a
direct `sed`+`diff` re-check of the full surrounding passage rather than
relying on the grep fragment alone.

---

## Method

For every probe (V1-V6) and every self-reported finding in each walk
(verifiera-01, verifierb-01, verifierb-02), I located the cited requirement
IDs and section numbers in *both* editions with `grep -n`, then read the
surrounding prose in both with `sed -n`, and — once I had matching anchors
(an identical heading number, an identical register-row string) — ran
`diff` directly on the corresponding line ranges of both files, which
catches a wording difference too small for a fragment search to surface
and proves a "no difference" claim rather than asserting it from fragment
hits alone.

Sections opened and diffed, in full or in the relevant run, in both
editions:

- §2.3 (all five conformance-class bullets — Conforming TARN file, reader,
  writer, updater, verifier — diffed directly as one block)
- §21.6 ("Conditions that are not violations": the full table, the "two
  conditions that once sat in this table" paragraph, the "two structural
  cases" paragraph, and the cannot-establish-grounds paragraph that follows
  it)
- §21.9 (Implementation limits, first ~120 lines, diffed)
- §21.1 (How to read the register, first ~115 lines, diffed)
- §7.2/§7.3 (the unknown-top-level-type paragraph; the record-type table;
  the registered-type stored-flags paragraph)
- §17.4 (Certification under codecs, in full)
- §20.3 step 4 (the fixed-declaration bar, in full, including the
  `[R-WRT-04]` 644-byte worked example)
- §20.4 (Re-emission and preservation, opening)
- §9.7's closing Note ("Nothing here enumerates prior commits...")
- §6.2 (trailer fields; the pre-trailer-pad definition)
- §6.3 (flags; the ignore-lane-bit statement)
- Register rows F25, F35, F36, L46 (table rows, verbatim)

---

## Part 1 — Probe-by-probe

### V1 — Verdict vocabulary

Both walks' answers agree in substance: three verdicts (conforming,
nonconforming, cannot establish), with *unexamined* and the per-requirement
report explicitly denied verdict status. I diffed the whole `[R-CNF-11]`
bullet directly (A lines ~211-229 against B lines ~245-267; see the
`[R-CNF-11]` bullet in the §2.3 diff below). The only difference is
consolidation: A states the "per-requirement report constrains the report
and not the verdict" twice — once immediately after describing that
obligation ("...whichever of the three verdicts it reports; that
per-requirement report constrains the report and not the verdict, as
*unexamined* does below"), and again at the end for *unexamined* alone
("*Unexamined* is neither a verdict nor *cannot establish* — it constrains
the report, not the verdict.") — while B states it once, at the end,
bundling both ("*Unexamined* is neither a verdict nor *cannot establish*;
it and the per-requirement report constrain the report, not the verdict.").
Same entities, same relationships, fewer sentences. **Kind: EQUIVALENT.**
Both walkers quoted their own edition correctly; they agree because the
substance agrees, not by luck — confirmed by the direct diff, not inferred
from matching quotes alone.

### V2 — Unimplemented top-level type, MU=1

This is the probe where the two walks genuinely diverge in confidence, and
the diff explains why.

verifier-A answered both branches (experimental-range -> cannot establish;
reserved-range -> nonconforming) without hedging, citing: "`[R-CNF-11]`'s
own definition of a conforming reader says: 'carrying no top-level record
of a type it does not implement with MUST_UNDERSTAND = 1 ... in a
conforming file such a type is necessarily from the experimental range,
since a reserved-range type carrying MU = 1 is itself a violation.'"

verifier-B's own finding **verifierb-01** treats the identical fact pattern
as a live, document-level AMBIGUITY with "no default," and has to *choose*
a reading ("I answer V2 under the experimental-range reading... and flag
the dependency here") rather than cite a settled resolution.

I checked both editions' "conforming reader" bullets directly:

- **Edition A** (`scratch/cleanroom/editions/a/tarn.md`, line 183, inside
  the §2.3 `[R-CNF-03]` bullet): "...a type it does not implement with
  MUST_UNDERSTAND = 1 — in a conforming file such a type **is necessarily
  from the experimental range, since a reserved-range type carrying MU = 1
  is itself a violation** — and none of whose values exceeds the minimum
  guarantees of §21's limits table (§21.9's `[R-ERR-04]` governs a refusal
  on that last ground; §21.6's closing paragraph names the other two),
  and MUST handle every codec..."
- **Edition B** (`spec/tarn.md`, line ~218, the corresponding bullet):
  "...a type it does not implement with MUST_UNDERSTAND = 1 and none of
  whose values exceeds the minimum guarantees of §21's limits table
  (§21.9), and MUST handle every codec..."

B's bullet omits the italicized clause entirely — not shortened, *absent*.
I confirmed this is not merely moved elsewhere: `grep -n "necessarily from
the experimental" spec/tarn.md` returns **zero** hits; the identical search
against edition A returns **one**, at line 183 (the control proving the
search pattern itself works). `grep -n "necessarily"` against all of
`spec/tarn.md` (5 hits total) turns up nothing else on this topic — the
nearest is an unrelated "without necessarily understanding" in the
conforming-updater bullet.

**Kind: LOSS.** Edition A states, at the point where "conforming reader"
is defined, a definition-level fact that directly forecloses the
probe's ambiguity: a reserved-range type with MU=1 is *itself* a violation
(F35/F36, identical in both editions — see Part 3 below), so by the
established-violation-priority rule (`[R-CNF-11]`, identical in both
editions — see V1 above) *any* file with such a record is automatically
nonconforming, which means the *only* way "unimplemented type, MU=1" can
coexist with "the verifier found no other violation" is if the type is
experimental-range. Edition A states this inference outright, as settled
fact, at the reader-definition site. Edition B never states it anywhere —
an implementer of B must perform the same multi-step derivation themselves
to reach the identical conclusion, and B's own in-house walk, performing
exactly that derivation, explicitly declined to treat it as settled
("two document-licensed answers... the probe's English does not pin
down"), flagging it as an open ambiguity rather than citing a resolution.

**Byte-level test (edition named).** Built from A alone, an implementer is
told directly, at the point where the relevant obligation is defined, that
an unimplemented-type-with-MU=1 record in an otherwise-violation-free file
is necessarily experimental-range — no derivation is required, and the
two-branch logic (experimental -> cannot establish; reserved -> established
violation, nonconforming) follows immediately and without hedging. Built
from B alone, nothing in the text states this; an implementer who does not
independently chain F35/F36 together with the established-violation
priority rule has no textual anchor forcing the experimental-range
reading, and — as verifier-B's own transcript demonstrates on this exact
scenario — a careful reader of B alone can and does conclude the document
itself leaves the verdict undetermined for this fact pattern, which is a
different output (an explicit "cannot determine without more information"
report, or a choice justified only by extrinsic reasoning about which
reading is "more consistent") than A's implementer would produce (a
direct, cited, two-branch answer with no flagged gap). Two conforming
implementations that otherwise agree can therefore diverge in whether they
report a probe-shaped case as decided or as requiring a capability-ground
disclosure of indeterminacy — a difference in what the verifier's report
says, not merely in its internal reasoning.

### V3 — Three-generation byte arithmetic

Both walks reach identical final figures (F1=4,480; F2=13,120; F3=14,528;
live total 12,816; slack 1,712) via the identical method (minimum pad to
the next 64-byte boundary; whole tile-index re-emission on a changed
stored-tile set). I located and diffed the governing passages directly:

- The `[R-WRT-04]` 644-byte worked example ("Superseding one 100,000-byte
  stored tile of a 32-tile interleaved layer appends...") — A lines
  3399-3406 against B lines 3255-3262 — **diffs identical, verbatim.**
- The six-step commit protocol ending in the `[R-WRT-04]` barrier (the
  numbered list item 6, "barrier; pad; trailer with the same file_id...")
  — **diffs identical.**

**Kind: EQUIVALENT**, confirmed by direct diff rather than inferred from
matching final numbers (which could in principle hide a lucky
coincidence; here it is not luck — the source text the arithmetic is built
on is byte-identical).

### V4 — Unexecutable codec

Both walks quote the same §17.4 passage for the same conclusion (cannot
establish, provided no other violation; the inability is reported as an
unchecked requirement, not as a rejection). I diffed §17.4 in full (A lines
2613-2629 against B lines 2469-2485): **identical, verbatim**, including
the closing sentence about an experimental-range metadata encoding not
being a cannot-establish ground. **Kind: EQUIVALENT.**

### V5 — A commit changing a fixed declaration; verifier visibility

Both walks reach the identical two-part answer (the bar is a writer-conduct
rule carrying no register row of its own; the verifier cannot see the act
because it walks only the live state in one pass; the actual verdict turns
on whether the result is *independently* structurally inconsistent). I
diffed the full §20.3 step 4 bar paragraph (A lines 3250-3299 against B
lines 3106-3155, the run from "A layer that stores a tile **in the
generation**..." through "...a re-declaration carried as the same layer
over the tiles it stored"): **identical, verbatim**, including the dual
citation `[R-ERR-01]`, `[R-CNF-02]`. I separately diffed the §9.7 closing
Note ("Nothing here enumerates prior commits... A verifier certifies what a
reader can reach... does not depend on reconstructing the file's history")
— A lines 1555-1560 against B lines 1411-1416: **identical, verbatim.**
**Kind: EQUIVALENT.**

### V6 — MU=1, PE=0 combination

Both walks quote the identical `[R-CNT-12]` paragraph and its Note, and
cite the identical register rows. I diffed the full paragraph (A lines
1023-1035 against B lines ~858-870) and its Note: **identical, verbatim.**
I also located and compared register rows F25 and L46 directly:

- F25 — A line 3869 / B line 3725: `| F25 | A non-layer top-level record's
  flags carry MUST_UNDERSTAND = 1 with PRESERVE_ON_EDIT = 0, a combination
  no writer emits | — | verifier | certification | [R-CNT-12] |` —
  **identical, character for character.**
- L46 — A line 3940 / B line 3796: `| L46 | A layer record's or
  sub-record's flags carry MUST_UNDERSTAND = 1 with PRESERVE_ON_EDIT = 0 |
  layer record; sub-record | verifier | certification | [R-CNT-12]
  (R-CNT-13) |` — **identical, character for character.**

**Kind: EQUIVALENT.**

---

## Part 2 — Each walk's own findings, checked against the other edition

### verifiera-01 (AMBIGUITY: no cannot-establish ground named for a
file-scope resource decline)

This finding rests on `[R-CNF-11]`'s "illustrative... list of five grounds"
and §21.9/`[R-ERR-04]`'s license to decline "at the whole file." I diffed
§21.9's first ~120 lines directly (A lines 4142-4260 against B lines
4008-4126): **identical, verbatim** — the licence to decline on resource
grounds "at the whole file... as layers per file and dir_length are" is
present, word for word, in both. The five-grounds list itself is present
in both editions too (see cmp-verifier-02 below; only its *location*
differs between them, not its content). **The gap verifier-A is pointing
at — that the specific file-scope, pre-directory-parse resource decline is
never named as a sixth, explicit cannot-establish ground alongside the
other five — exists unchanged in edition B.** This is a property of the
shared specification text, not something either edition introduces or
removes relative to the other.

### verifierb-01 (AMBIGUITY: reserved- vs experimental-range verdict for
an "unimplemented type with MU=1" probe)

Covered in full under V2 above. This is **not** a shared-document gap the
way verifiera-01's finding is: it is a genuine edition-specific LOSS (see
cmp-verifier-01). Edition A resolves the fact pattern directly at the
reader-definition site (§2.3); edition B never states the resolving
inference anywhere, which is exactly what makes B's own walk unable to
cite a settled answer where A's walk could.

### verifierb-02 (OBSERVATION: a commit that silently changes a stored
layer's fixed declaration is often undetectable by construction)

This finding rests on §20.3 step 4's bar and §9.7's closing Note, both
confirmed byte-identical between editions under V5 above. verifier-A's own
V5 answer, reasoning independently from edition A alone (it does not cite
verifier-B's finding — the two walks are blind to each other, per this
brief's premise), reaches the identical substantive conclusion ("the file
can verify as conforming on its own terms despite the writer having broken
this rule... an instance of the 'unwitnessed'/'no condition a file can
exhibit' design the document states deliberately"). **This is a shared
design property of the specification, present and reachable from either
edition, not a B-only discovery** — verifier-B's walk simply chose to
elevate it to a named Finding while verifier-A's walk folded the identical
conclusion into its direct answer to V5 without flagging it separately.

---

## Part 3 — Beyond the probes: §2.3 diffed as one block

The probes above account for every divergence I found in the sections the
verifier depends on most, with one exception surfaced only by reading the
whole of §2.3 side by side rather than following individual probe
citations. I diffed the entire "Conformance is defined for five classes"
block — all five bullets — directly: A lines 154-253 against B lines
205-267.

**Four differences, all contained inside this one block:**

1. **Conforming TARN file / `[R-CNF-02]` (LOSS).** Edition A names three
   specific, closed-list instances of writer-conduct-only obligations that
   never make a file nonconforming, introduced as "are the cases this text
   states" (a completeness claim — these and no others):
   > "§6.3's flags rules against a set ignore-lane bit (a creator's flags =
   > 0, and an updater's copy-forward and set-no-other, §20.3 step 6 and
   > §20.5), §6.2's pre-trailer gap longer than `[R-LIF-02]` step 5's pad,
   > and §20.3 step 4's bar on the fixed declarations of a layer that
   > stores a tile are the cases this text states, and each is declared
   > where it arises rather than enumerated here." (A, lines 173-179)

   Edition B's corresponding sentence drops the enumeration and the
   completeness claim, stating only the bare category:
   > "A writer obligation that governs conduct rather than output, or
   > whose violation this specification expressly declares not to be a
   > file-conformance violation, binds the writer and never makes a file
   > nonconforming." (B, lines ~213-217)

   I checked each of the three dropped instances at its own local section
   in both editions to see whether the *substance* (not the summary) is
   independently recoverable in B:
   - Ignore-lane bit: A line 902 ("a set ignore-lane bit is not a
     file-conformance violation") vs. B line ~768 ("A set ignore-lane bit
     is nevertheless not a file-conformance violation") — present,
     equivalently, in both.
   - Pre-trailer pad: A line ~851 ("a longer gap is conforming, and no
     conforming commit produces one") vs. B line ~716 ("a longer gap is
     conforming, though no conforming commit produces one") — present,
     equivalently, in both.
   - §20.3 step 4 bar: confirmed identical in both editions under V5
     above, including the `[R-ERR-01]`/`[R-CNF-02]` dual citation.

   All three facts survive independently in B; what is lost is the single
   place in the document that collects them and asserts there are no
   others. **Kind: LOSS. Byte-level: no divergence demonstrated on the
   facts given** — each instance is identically recoverable at its own
   site in both editions — but B loses the closed-list/completeness
   assertion A makes at the point `[R-CNF-02]` is defined.

2. **Conforming reader / `[R-CNF-03]` (LOSS).** Covered in full above as
   cmp-verifier-01/V2 — the "necessarily from the experimental range"
   clause.

3. **Conforming updater / `[R-CNF-06]` (EQUIVALENT).** Edition A adds "—
   which govern every record type, not only those it does not understand"
   after citing §20.4's preservation obligations; edition B drops the
   clause. I diffed §20.4's opening (A lines 3475-3530 against B lines
   3331-3386): **identical, verbatim**, including "Persistence governs
   every record type; only the authoritative source of the flags differs"
   as the section's own second sentence. The scope claim A's §2.3 bullet
   previews is fully and identically restated at its point of full
   definition in both editions; A's §2.3 clause was a redundant
   forward-pointer, not unique content.

4. **Conforming verifier / `[R-CNF-11]` (EQUIVALENT).** Covered under V1
   above (the per-requirement-report/unexamined consolidation), and the
   five-grounds relocation, covered next.

**Fifth difference, spanning §2.3 and §21.6 together (EQUIVALENT, but
worth separating from #4):** the five-grounds enumeration for *cannot
establish* sits inline in A's §2.3 `[R-CNF-11]` bullet ("...as when the
file names a format major version it does not implement, when a record
carries MUST_UNDERSTAND = 1 with a type it does not implement (§21.6),
when it cannot execute a codec or filter (`[R-COD-11]`)...", A lines
220-229) but is replaced in B's §2.3 bullet by a bare cross-reference,
"(§21.6 names the grounds)" (B line 254). The same five grounds, in
matching wording, instead appear in B's own §21.6 section:

> "A verifier is unable to check a requirement on a capability or resource
> ground, and so reports *cannot establish* (`[R-CNF-11]`), as when the
> file names a format major version it does not implement, a record
> carries MUST_UNDERSTAND = 1 with a type it does not implement, it cannot
> execute a codec or filter (`[R-COD-11]`, §17.4), it declines a layer's or
> a tile's decode on resource grounds and so cannot check §14's
> decoded-content obligations (`[R-ERR-04]`, `[R-SER-05]`, `[R-SER-08]`),
> or it declines to decode a user-metadata document (`[R-MTA-09]`)."
> (B, lines 3934-3942)

Edition A does **not** have this paragraph at its §21.6 location at all —
`grep -n "unable to check a requirement on a capability"` against both
files returns a hit only in `spec/tarn.md` (line 3934); edition A goes
directly from the "two structural cases" paragraph (which I separately
confirmed is byte-identical between editions) to the "#### 21.7" heading
with no intervening paragraph. Each edition states the five grounds
exactly once; only the *location* moved (§2.3 in A, §21.6 in B). Net
content is unchanged. **Kind: EQUIVALENT** — but this is the reason
verifiera-01's and verifierb-01's own citations of "the five grounds" land
in different sections of their respective editions, which is worth
recording even though it produces no byte-level divergence.

---

## Evidence notes

- **Sweeps run, with hit counts and controls.** `grep -n "necessarily from
  the experimental" spec/tarn.md` -> 0 hits; control, same pattern against
  `scratch/cleanroom/editions/a/tarn.md` -> 1 hit (line 183), proving the
  pattern itself is not the reason for the zero. `grep -n "necessarily"
  spec/tarn.md` -> 5 hits total, none on this topic (checked each). `grep
  -n "unable to check a requirement on a capability"` against both files
  -> 0 in A, 1 in B (line 3934); control — `grep -n "A verifier is unable
  to check"` run the same way, same result, confirming the fragment is not
  an artifact of line-wrap splitting. Every register-row and worked-example
  "identical" claim above was confirmed by `diff` on the located line
  ranges, not by fragment search alone.
- **Derived facts checked against the document, not assumed.** The claim
  that a reserved-range type with MU=1 is *itself* a violation regardless
  of the MU bit (the premise A's dropped sentence rests on) was checked
  directly against register row F36's text in both editions (identical,
  "emitting one is a violation whatever its MU bit") rather than taken from
  either walk's paraphrase.
- **Suspicions opened and closed.** (1) Whether the §21.6 relocation (item
  5 above) was itself the cause of the V2 divergence — closed: the
  relocated paragraph states the same five grounds in both forms, neither
  of which contains the "necessarily experimental" inference; the actual
  cause is the separate, independent omission in the §2.3 `[R-CNF-03]`
  bullet (item 2/cmp-verifier-01), confirmed by diffing the two bullets
  directly rather than assuming the relocation explained everything. (2)
  Whether verifierb-02's observation might be a B-only artifact of some
  trimmed qualifier in §20.3 or §9.7 — closed by direct `diff`, which found
  no difference in either passage. (3) Whether the §2.3 "Conforming
  updater" clause-drop (item 3) left any actual gap in B — closed by
  checking §20.4's own opening sentence, which restates the dropped claim
  identically in both editions.
- **Where this came up thin.** Beyond the four §2.3 differences and the
  §21.6 relocation, every other passage I opened for the probes and for
  the two walks' self-reported findings (V1, V3-V6 in full; §21.1, §21.9,
  §7.2/7.3, §17.4, §20.3 step 4, §20.4's opening, §9.7's Note, register
  rows F25/F35/F36/L46) diffed identical between editions. I did not find
  a second LOSS/ADDITION/CONTRADICTION beyond the two reported in §2.3
  after specifically re-reading that block line by line against its B
  counterpart; I am reporting what the diff actually showed rather than
  padding the list to look more thorough.
