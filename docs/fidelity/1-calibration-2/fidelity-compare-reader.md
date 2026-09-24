# Reader comparator — transcript

## Disclosure

**What I read.** Exactly four files, each opened by the literal path given in
the ACCESS RULE, never by listing a directory:

- `/Users/robertkleffner/Documents/GitHub/tarn-first-draft/scratch/cleanroom/editions/a/tarn.md` (edition A, 4,981 lines)
- `/Users/robertkleffner/Documents/GitHub/tarn-first-draft/scratch/cleanroom/editions/c/tarn.md` (edition B — the ACCESS RULE names this path "edition B of the specification"; the directory happens to be called `c`, which I note only because reader-B's own transcript flagged the same letter mismatch. I did not treat that as license to read any `editions/b/` path, and did not.)
- `/private/tmp/claude-501/-Users-robertkleffner-Documents-GitHub-tarn-first-draft/fidelity-2/out/transcript-reader-a.md`
- `/private/tmp/claude-501/-Users-robertkleffner-Documents-GitHub-tarn-first-draft/fidelity-2/out/transcript-reader-b.md`

I did not list `scratch/cleanroom/editions/`, `.../fidelity-2/out/`, or any other
directory. I did not open docs/, PLAN.md, OPEN-QUESTIONS.md, AGENTS.md,
README.md, conformance/, spec/registry.json, git history, or the web.

**What I ran.** `mkdir -p` on my own scratch directory
(`.../fidelity-2/scratch/compare-reader/`) and on the `out/` directory (creation
only, not a listing — no directory contents were returned or inspected by
that command). `wc -l` on the four files above, to plan `sed`/`diff` ranges.
Every subsequent command was `sed -n '<range>p'`, `diff <(sed ...) <(sed ...)`,
or `grep -n` against the four named files only — no other path was touched,
and no `ls`, `find`, `git`, or network call was made. I did not write any
working file to my scratch directory beyond this transcript; all intermediate
diffs were run inline via process substitution and consumed directly, not
saved to disk, so the scratch directory contains only this transcript's final
copy.

**Wrapping caveat.** Both editions are hard-wrapped prose (~64–72 cols) with
`> ` on blockquote lines. Where I compared passages I pulled matched line
ranges by section-header line number (confirmed identical section order and
numbering via `grep -n "^#### "`/`"^### "` in both files first) and diffed
whole sections rather than short greps, so wrapping could not manufacture a
false zero. Where I did use short `grep -n` fragments to locate a term
(`R-MTA-10`, `R-SER-05`, `R-ERR-04`, `registered record type`, `updaters are
readers`, etc.), each search was run against **both** files with the same
pattern, side by side; a hit in one file and a miss in the other, for a
fragment that also hits correctly-matched surrounding text in the miss file,
rules out wrapping as the cause. I additionally cross-checked every claimed
absence by re-running the same command with a control term I already knew
(from the successful hits in that same file) was present in the immediate
vicinity — e.g. for `R-CNF-03`'s dropped "registered record type" clause, the
same `grep -n "registered record type"` call that returned zero hits in a
window of edition B also returned two hits elsewhere in the *same file*
(lines 3940 and 4805), proving the pattern and the file both work and the
absence at the §2.3 location is real, not a wrapping artifact.

**Whole-section diffs run (byte-identical unless noted).** §3 (Terminology),
§4 (Encoding Conventions), §5 (File Anatomy), §6 (Front Signature Block and
Trailer), §7 (Metadata Directory and Records), §8 (Integrity), §9 (Lifecycle),
§11 (Layers/Dimensions/Tiling), §14 (Tile Serialization), §15 (Tile Index),
§17 (Codecs and Filters), §19 (Reading a TARN File), §20.4 (Re-emission and
preservation), §21.1–§21.5, §21.9. Differences found only in §2.3
(Conformance) and one added paragraph plus one dropped word at the tail of
§3/§11.4/§21.6, detailed below.

**Context I did not ask for.** My context already contained a project
instruction file (`CLAUDE.md` → `AGENTS.md`), a user-memory index of prior-round
note titles about this same TARN project, and a git-status block naming the
current branch (`readable`) and recent commit subjects about a "readable
edition." None of it is the specification and none of it is evidence about
it. I did not open the file the project instructions point to, did not open
any memory note, and did not let any commit subject inform my reading of
either edition — including where a commit subject's wording ("§2.3 — condition
and reach defined in plain words," "reach paragraph cut to its rules, its Note
removed") happens to name the exact passage I independently found altered by
diffing the two files myself. I flag the coincidence and disclose that the
memory titles appeared, without repeating their content or treating them as a
lead; every finding below is derived solely from the diff-and-read work shown
above, and would be identical had that memory index not been in my context.

**Breach in reader-B's transcript.** Reader-B's transcript (which I was
told to read) discloses that it ran `ls -la` on the output directory after
copying its file there, in violation of its own brief, and saw two filenames
belonging to other agents' work (`transcript-quiz-a-on-a.md`,
`transcript-quiz-a-on-b.md`) with no content. I am relaying that disclosure
because it is part of the file I was assigned to read; I did not open either
named file, did not list any directory myself to check, and made no use of
those names in the analysis below.

**Path check.** All four files were exactly where the brief said. No
discrepancy of my own to report.

---

## Part 1 — Whole-document diff: what actually differs between the editions

A line-by-line, section-by-section pass (methodology above) found textual
differences in exactly three places, all inside or pointing at §2.3
("Conformance requirement" / `[R-CNF-02]`, `[R-CNF-03]`, `[R-CNF-06]`,
`[R-CNF-11]`, `[R-CNF-13]`), plus two one-clause rewordings elsewhere that are
paraphrases, not rule changes. Every section a probe cites outside §2.3 —
§4, §5, §6, §7, §9, §11 (bar one clause), §14, §15, §17, §19, §20.4, §21.1–21.5,
§21.9 — is **byte-identical** between the two editions. This matters for
every probe below: where a probe's cited passage is outside §2.3, any
difference between the two walkers' answers cannot be a LOSS or ADDITION
(the text is the same), and must be REPORTER_ERROR, EQUIVALENT phrasing, or a
walker simply noticing something the other one didn't about *shared* text.

### D1 — `[R-CNF-02]` (writer-conduct obligations and file conformance): **reversed**

Edition A:
> A few obligations this specification places on writers govern their
> *conduct* rather than their output... and a file is never nonconforming by
> virtue of one: conduct rules bind the actor, the predicate binds the
> bytes. A writer obligation whose violation this specification expressly
> declares not to be a file-conformance violation binds the actor in the
> same way; §6.3's flags rules against a set ignore-lane bit..., §6.2's
> pre-trailer gap longer than `[R-LIF-02]` step 5's pad, and §20.3 step 4's
> bar on the fixed declarations of a layer that stores a tile are the cases
> this text states...

Edition B:
> A writer obligation that governs conduct rather than output, or whose
> violation this specification expressly declares not to be a
> file-conformance violation, binds the writer, **and a file that breaks
> one is nonconforming.** `[R-CNF-02]`

This is not a paraphrase; it says the opposite thing. A says explicitly a
file is *never* nonconforming for breaking one of these obligations
(conduct-only, or expressly-carved-out); B says a file that breaks one *is*
nonconforming. B's sentence is also internally self-contradictory on its own
terms: it names the obligation as one "whose violation this specification
expressly declares not to be a file-conformance violation" and then declares
the file nonconforming for exactly that violation.

I checked this against the two concrete cases A names, both in
byte-identical §6 text in both editions:
- §6.2 (identical in both): "a longer [pre-trailer] gap is conforming, and
  no conforming commit produces one" — i.e. explicitly **not** a
  file-conformance violation.
- §6.3 (identical in both): "a set ignore-lane bit is not a
  file-conformance violation."

Both editions' §6 say, unchanged, that these are not file-conformance
violations. Edition B's rewritten `[R-CNF-02]` now says a file breaking such
an obligation "is nonconforming" — directly contradicting B's own §6.2 and
§6.3 in the same document.

**Kind: LOSS** (of a stated, load-bearing rule) **and CONTRADICTION** (B is
internally inconsistent). **Byte-level: yes.** A verifier built from B alone,
reading only §2.3, could report *nonconforming* for a file with a longer
pre-trailer gap or a carried-forward ignore-lane bit — exactly the outcome
§6.2/§6.3 (unchanged in B) forbid. A verifier built by reading §6 on its own
would reach the opposite, correct verdict. The document, as edition B states
it, decides this both ways.

### D2 — `[R-CNF-13]` (reach doctrine): failure disposition **reversed**

Edition A: "A reader MUST apply every reaching condition to a file whatever
major it declares... and **MUST treat its failure as reject-file** on the
ground of the requirement stating it **rather than on capability grounds**;
the distinct diagnostic `[R-CNT-07]` asks for is owed where every reaching
condition is satisfied and the declared major is one the reader does not
implement."

Edition B: "A reader MUST check every reaching condition whatever major the
file declares, and **MUST treat a failure as a capability refusal, not as
reject-file** under the requirement that states the condition..."

Again, opposite dispositions for the same class of failure (a reaching
condition — trailer magic, trailer CRC, front block, and `[R-CNT-24]`'s
fixed invariants — failing on a file declaring an unimplemented major).

Checked against §21.2, byte-identical in both editions: its opening
paragraph states "Outcome: reject-file. 35 conditions... Deriving it there
[`[R-CNF-13]`] yields F8, F14, F6 and both of F1's instances... and no other
row," and the table itself assigns F1/F6/F8/F14/F15 Detector = **reader**,
Detected = **open**, under the section header "Outcome: reject-file." Nothing
in the identical §21.2 table calls any of these a "capability refusal" — they
are ordinary reject-file rows like every other row in that table. Edition
B's rewritten `[R-CNF-13]` therefore contradicts edition B's own §21.2.

This directly compounds reader-A's own finding (readera-01, reproduced below)
about the tension between §19.1 step 1 (F5 checked before the major is known)
and the reach doctrine — and shows that tension is not unique to F5 or to
edition A: edition B has introduced a second, sharper self-contradiction on
the *general* rule for every reaching condition, on top of inheriting the
first one unchanged (§19.1 is byte-identical between editions; see readera-01
below).

**Kind: LOSS/CONTRADICTION. Byte-level: yes** — same reasoning as D1: whether
a reaching-condition failure on an unimplemented-major file is reported
*nonconforming* (an established violation, reject-file) or *cannot establish*
(a capability ground) is exactly the MUST-level, mutually-exclusive
distinction `[R-CNF-11]` polices, and the two passages of edition B decide it
oppositely.

### D3 — `[R-CNF-03]` (core-conformance obligations): **"both record types" dropped, breaking a live cross-reference**

Edition A's `[R-CNF-03]` list of what a conforming reader MUST handle
includes, in addition to codecs/filters/layouts/sample types/user-metadata
encodings, "**and both record types §7.3 registers**," and its no-subset-profiles
sentence lists "...an assigned user-metadata encoding, **or a registered
record type** is not a conforming reader..."

Edition B's `[R-CNF-03]` drops both clauses: its MUST-handle list ends at
"every user-metadata encoding §18.2 assigns" (no record-type clause), and its
no-subset-profiles sentence reads "...software that declines any of those is
not a conforming reader..." with no record-type disjunct to decline.

I checked §7.3 itself (byte-identical in both editions): it defines the two
record types and their fixed flags, but never itself states that a
conforming reader must implement both — that obligation lived only in
`[R-CNF-03]`. I then checked Appendix H's conformance checklist, which is
**byte-identical in both editions** and still reads: "implements all four
codecs, both filters, both layouts, all thirteen sample types, both
user-metadata encodings, **and both registered record types**
(`[R-CNF-03]`, §2.3)." Edition B's checklist cites `[R-CNF-03]` as the source
of an obligation that `[R-CNF-03]`'s own text, in edition B, no longer
states.

**Kind: LOSS**, with a broken internal cross-reference as corroborating
evidence that this was dropped rather than intentionally relocated (nothing
else in edition B states it). **Byte-level: yes** — a reader built strictly
from edition B's §2.3, ignorant of user-metadata records entirely, could
consider itself conforming under the letter of B's `[R-CNF-03]`; the same
implementation is disqualified under edition A's `[R-CNF-03]`.

### D4 — `[R-CNF-11]` (verifiers/updaters): "and updaters" dropped, breaking a second live cross-reference

Edition A: "Verifiers **and updaters** are readers of the files they process
and inherit every reader obligation."

Edition B: "Verifiers are readers of the files they process and inherit
every reader obligation." — updaters are silently dropped from the sentence.

Checked against §20.4's step table (byte-identical in both editions), whose
MU=1 row states: "At file scope no commit is available at all: **the updater
is a reader of the file first (§2.3)**, and `[R-CNT-15]` makes an
unimplemented top-level MU = 1 record reject-file..." — this citation back to
§2.3 for the claim "the updater is a reader" is only actually stated in
§2.3's `[R-CNF-11]` in edition A. Edition B keeps the cross-reference but has
dropped the fact it points to.

**Kind: LOSS**, same broken-cross-reference signature as D3. **Byte-level:
marginal but real** — nothing in edition B's §2.3 any longer tells an
implementer that an updater inherits every ordinary reader obligation (only
that a verifier does), even though §20's own rules for updaters depend on
that premise being established at §2.3.

### D5 — `[R-CNF-13]`'s worked Note (F14/F5/F15) and the version_major=0 sentence: dropped, but the underlying rule survives elsewhere — EQUIVALENT

Edition A's §2.3 also contains (a) a sentence carving out version_major=0
("it is not a file declaring a format major other than 1, no reach question
arises for it, and `[R-CNT-07]` rejects it (§21.2, F18)") and (b) a `> Note`
walking through why F14 reaches, F5 doesn't, and F15 doesn't despite citing
`[R-CNT-24]`. Both are absent from edition B's §2.3.

I checked whether the substance survives elsewhere before calling this a
loss. §21.2's opening paragraph — **byte-identical in both editions** —
already states: "F18 is not an exception but a case outside the premise:
version_major = 0 declares no major at all, so `[R-CNF-13]`'s premise is
unmet and `[R-CNT-07]` governs (§21.6)," and separately: "Deriving it there
yields F8, F14, F6 and both of F1's instances... and no other row" (which by
exclusion already tells a reader F5 does not reach, in both editions
equally). The dropped Note itself is explicitly non-normative under
`[R-CNF-01]` (a `>` blockquote), and its content — the *reasoning* for facts
already stated as rules in the identical §21.2 — is not itself a rule.

**Kind: EQUIVALENT** (relocated/deduplicated, not lost — unlike D3/D4, no
live cross-reference elsewhere depends on the missing sentence, and the
missing Note's factual content is independently recoverable from
byte-identical §21.2 text). I list it only to record that I checked it and
closed it, since it is the passage two of my four available source documents'
recent-commit context (disregarded per the brief) happens to also name.

### D6 — `[R-CNF-06]`'s "governs every record type" clause: dropped, restated verbatim elsewhere — EQUIVALENT

Edition A: "...MUST honor the preservation obligations of §20.4 — **which
govern every record type, not only those it does not understand.**"
Edition B drops the appositive.

Checked: §20.4 itself, byte-identical in both editions, opens: "**Persistence
governs every record type**; only the authoritative source of the flags
differs." Substance preserved verbatim at its primary location.
**Kind: EQUIVALENT.**

### D7 — Two one-clause rewordings outside §2 — EQUIVALENT

- §3.1's "addressed tile" definition: A says "every tile of a layer is
  *addressed*"; B says "a tile is *addressed* in a generation if that
  generation's tile index has an entry for it: the tiles of the layer's grid
  under the geometry that generation declares (§11.2, §15)." B is more
  explicit about the generation-relative framing, but I could not construct
  a file where the two definitions license different bytes: §11.2's grid
  geometry is fixed by the layer record for a generation either way, so
  "every tile of a layer" and "every tile under that generation's declared
  geometry" pick out the same set. **EQUIVALENT.**
- §11.4/§3.1's "declared order is load-bearing" → "fixes the sample order on
  disk... tile ordinals follow the same order" / "fixes each channel's
  index": both are restatements of the identical, unchanged §11.4 rule.
  **EQUIVALENT.**

---

## Part 2 — Probes: agreement, and whether the shared text explains it

For every probe both walks answered nearly identically. I verified, for
each, that the section(s) each walker cited are in the byte-identical set
found in Part 1 (§4, §5, §6, §7, §14, §15, §17, §19, §21.2–21.5, §21.9 are
all identical); none of R1, R2, R4, R5, R6, R7, R8's cited passages fall
inside the one changed passage (§2.3). Where the two walks' probe answers
diverge, the divergence traces to something *other* than the fixed text (a
difference in explicitness or completeness of the walker's own account, not
to the text), never to a byte difference between editions.

- **R1** — Both name the same two requests, same offsets, same total-bytes
  formula (`64 + dir_length`), from §6.4 text that is byte-identical in both
  editions, including the Note that "no request count is a conformance
  property." Reader B's structured probe answer is tagged
  `[underdetermined]` and reader B's own finding readerb-03 elevates this
  into an AMBIGUITY; reader A's transcript quotes the same "MAY instead
  speculatively fetch" sentence and the same Note's working-set claim but
  does not tag its own R1 answer underdetermined or raise it as a finding.
  Since §6.4 is identical in both files, this is not a text-driven
  divergence — it is the same ambiguity, present equally in edition A,
  that reader A noticed and used only as color and reader B noticed and
  escalated to a finding. **Kind: EQUIVALENT text; the difference is
  walker thoroughness, not the document.** I agree with readerb-03's
  characterization on the merits (§6.4's Note is explicit that request
  count is not a conformance property), and note it applies to *both*
  editions identically — it is not evidence that edition B is less
  determinate than edition A.
- **R2, R5, R6, R7, R8** — Both walks agree, citing §6.2/§6.3 (R2), §7.1
  (R5), §5.1/§19.1 (R6), §11.2/§11.4/§14.2 (R7), §7.2/§7.4/§21.6 (R8), all
  confirmed byte-identical between editions. No divergence; agreement is
  not luck here, since the source text the two walkers read is literally
  the same bytes. **EQUIVALENT / REPORTER agreement, non-luck.**
- **R3** — Both walks agree the probe's premise ("a reader that does not
  implement zstd") describes software `[R-CNF-03]`/`[R-COD-11]` disqualify
  from being a conforming reader at all, with no L43 (out-of-range codec)
  row applying. §17.2, §17.4, §2.3's codec clause, and §21.3's L43 row are
  all confirmed byte-identical between editions (the §2.3 diff in Part 1 is
  confined to the record-type and reach-doctrine clauses; the codec
  MUST-handle clause and no-subset-profiles codec disjunct are unchanged in
  both editions). **EQUIVALENT.**

---

## Part 3 — Each walk's own findings, checked against the other edition

- **readera-01** (CONTRADICTION, §19.1 step 1 vs §2.3/`[R-CNF-13]`'s reach
  doctrine over F5): §19.1 is byte-identical between editions, and — as
  shown in D5 above — the fact that F5 does not reach is established
  identically in both editions' (unchanged) §21.2 preamble. The tension
  reader A identified — step 1 rejects a sub-128-byte file on F5 grounds
  before the major is ever read, while the reach doctrine says F5 must not
  be established against a file whose (still-unread) major turns out to be
  foreign — is therefore present, unchanged, in edition B as well. Reader B
  did not raise it. Because edition B additionally reverses the general
  reach-condition disposition rule (D2), edition B's version of this
  tension is if anything harder to resolve than edition A's: edition B no
  longer even tells a reader clearly that a *reaching* condition's failure
  (as opposed to F5's non-reaching failure) is ordinary reject-file rather
  than a capability refusal. **This is not a LOSS or ADDITION — the cited
  text is identical — but it is a finding that reader B's silence on it is
  an omission, not evidence the defect is edition-A-specific.**
- **readera-02** / **readerb-01** (OBSERVATION, no outcome class for a
  reader lacking a core/assigned codec): the two walks make the identical
  finding independently, from byte-identical §17.4/§2.3 text. **EQUIVALENT
  — same text, same (correct) finding, no divergence to report.**
- **readerb-02** (OBSERVATION, F5's Instances column claims two instances
  that may not be independently constructible) and **readerb-03** (already
  covered under R1 above): both cite §21.2/§21.1/§19.1/§5.1, all
  byte-identical between editions. The condition readerb-02 describes (that
  a `committed_file_length`-only F5 instance cannot be built without also
  triggering F17) is a property of the shared, unchanged text and applies
  equally to edition A; reader A did not raise it. **Not a fidelity
  difference — the text is identical in both editions — but worth
  recording that it is a real property of *both* editions, not of edition B
  alone**, since a reader of only reader-A's transcript could otherwise
  mistake its absence there for evidence the ambiguity is B-specific.

---

## Part 4 — Sections read side by side beyond the probes

Beyond the diffs in Part 1, I read §2.4 (outcome-class table and its Notes),
§10 (Extension Points and Registry), §12–13 (Channels/Fill), §16
(Slabs/Alignment), §18 (User Metadata), §20.1–20.3, 20.5 (Writer tiers,
creation, append, rewriting), and §22–24 in both editions via the same
whole-section-diff method as Part 1's list, specifically looking for a rule,
exception, quantifier, or figure present in one and not the other. All were
byte-identical. I did not find a difference outside the ones already listed
in Part 1.

---

## Summary of kinds

- D1 (`[R-CNF-02]`): LOSS + CONTRADICTION, byte-level yes — **primary
  finding**.
- D2 (`[R-CNF-13]` disposition): LOSS + CONTRADICTION, byte-level yes —
  **primary finding**.
- D3 (`[R-CNF-03]` record types): LOSS, byte-level yes.
- D4 (`[R-CNF-11]` updaters): LOSS, byte-level marginal/real.
- D5, D6, D7: EQUIVALENT (checked and closed).
- R1/readerb-03: EQUIVALENT text; walker-thoroughness difference only.
- R2, R3, R5, R6, R7, R8: EQUIVALENT / correct agreement on identical text.
- readera-01: applies unchanged to edition B; reader B's silence is an
  omission, not a text difference.
- readera-02/readerb-01: EQUIVALENT, independently confirmed.
- readerb-02: property of shared, unchanged text; applies to edition A too.
