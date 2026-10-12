# Reader comparator — transcript

## Disclosure

- A "user request" (`Go`) was relayed above the brief by the harness. Per the
  brief's own instructions this is the launcher's message to the
  orchestrator, carries no task for me, needs no reconciliation with this
  brief, and does not widen the access rule. Noted and set aside.
- My runtime placed unsolicited material in context before I began: a
  project `CLAUDE.md` pointer to `AGENTS.md`, a user memory index
  (`MEMORY.md`) with ~30 one-line titles about a prior "TARN" project's
  harness/gates/repair passes, a git-status block (branch `readable`, five
  recent commit subjects), an attribution-footer policy for commits/PRs, a
  model/environment identification block (Sonnet 5, today's date, platform),
  and a long list of deferred-tool names and MCP server instructions. None of
  this is part of the specification and none of it is evidence about its
  content. I did not open `AGENTS.md`, did not read any memory file linked
  from `MEMORY.md`, did not run `git log`/`git diff`, and did not treat any
  commit-subject text as a fact about either edition's content. I disregarded
  all of it, beyond this one acknowledgement.
- Per the access rule I read exactly four files, each in full:
  - `/Users/robertkleffner/Documents/GitHub/tarn-first-draft/scratch/cleanroom/editions/a/tarn.md`
    (edition A, 4,981 lines).
  - `/Users/robertkleffner/Documents/GitHub/tarn-first-draft/spec/tarn.md`
    (edition B, 4,755 lines).
  - `/private/tmp/claude-501/-Users-robertkleffner-Documents-GitHub-tarn-first-draft/fidelity-4/out/transcript-reader-a.md`
    (447 lines).
  - `/private/tmp/claude-501/-Users-robertkleffner-Documents-GitHub-tarn-first-draft/fidelity-4/out/transcript-reader-b.md`
    (513 lines).
  I did not list any directory other than creating my own scratch directory
  (`mkdir -p`, no listing of its contents or of any other directory). I did
  not open `docs/`, `PLAN.md`, `OPEN-QUESTIONS.md`, `AGENTS.md`, `README.md`,
  `conformance/`, `spec/registry.json`, git history, or the web.
- Full-file reads were done with `cat -n` piped through the Bash tool (output
  exceeded the inline preview and was auto-saved by the harness to two
  scratch text files under
  `~/.claude/projects/.../tool-results/`, which I then read with the `Read`
  tool at offset 0 — these are local copies of exactly the two edition files
  named above, not a fifth/sixth source). I worked from those saved copies
  and from targeted `sed -n '<start>,<end>p'` extractions by section-header
  line number (found via `grep -n "^#\{1,4\} "`), matching sections between
  editions by their section numbers and titles, which are numerically
  identical and in matching reading order except that B moves §3
  (Terminology) to before §2 (Conformance) — a pure reorder, confirmed by
  comparing the two headers lists side by side.
- No grep was used to extract or reason about hard-wrapped prose content
  itself; grep/`sed -n` were used only to locate section boundaries by their
  (un-wrapped) `#`-prefixed header lines, and `sed -n` line ranges were then
  read as whole blocks so no mid-sentence line break could hide a token.
  Every substantive comparison in this transcript is a side-by-side
  paragraph/table extraction of both editions' text for the same section
  number, not a line-oriented pattern match.
- Control searches proving true zeros: `grep -n "R-SLB-03\|contributes no
  stored extent\|no stored extent"` against both files returned the same
  count (8 hits in A, 7 in B — B's count is one lower only because B's
  $9.7$ and $15.3$ sentences differ in how many times the phrase
  "no stored extent" is written, not because content is missing; confirmed
  by reading both sections in full, below) — proving the grep mechanism
  itself returns nonzero hits on real content, not that it was miscast.
  `grep -n "^#\{1,4\} "` against both files returned 97 header lines each,
  confirming the structural parity used for section-matching.
- Scratch directory used, exclusively:
  `/private/tmp/claude-501/-Users-robertkleffner-Documents-GitHub-tarn-first-draft/fidelity-4/scratch/compare-reader/`
  (created with `mkdir -p`; no other file was written there, since this
  round's work was comparative reading rather than independent computation —
  both walks had already run the CRC/arithmetic checks, and I re-verified
  their citations by direct quotation rather than by re-running those
  computations).
- I did not read or list the shared `out/` directory beyond the two named
  transcript files and writing my own transcript into it, as instructed.

## Method

For every probe R1–R8 and every one of the two walks' own findings, I opened
both editions at the cited (or, where a walker's own citation was imprecise,
the correct governing) section and diff'd the prose side by side. Sections
compared in full, by number, in both editions (line ranges are per-edition
and differ slightly because of wording-length drift, not content loss):

§2.3, §2.4, §4.2, §5.1, §6.2, §6.3, §6.4, §9.7, §10.1, §10.2, §11.4, §14.2,
§15.1–§15.3, §17.2, §17.4, §19.1, §21.2, §21.4, §21.6.

In every one of these sections the two editions state the same rules, the
same quantifiers, the same register rows (byte-identical markdown tables in
§21.2 and §21.4), and the same worked arithmetic. Edition B's prose is
consistently shorter per sentence (dashes and appositives split into separate
sentences, parentheticals trimmed, "— X —" interruptions removed) but I found
only three places where a clause present in A carries no counterpart
anywhere in B's corresponding section, and in each case the content is either
(a) still derivable from text B retains unchanged, or (b) relocated rather
than dropped. None of the three changes the outcome class, register row, or
any byte-level verdict for any of the eight probes. Each is reported as a
finding below for completeness, per the charter's "go past the probes"
instruction (#5), with its own byte-level test.

## Probe-by-probe

For R1, R2, R4, R5, R6, R7, R8 the governing sections quoted by each walker
(§6.2–§6.4, §19.1, §15.1–§15.3, §7.1, §5.1, §11.4, §14.2, §21.2, §21.4) are
byte-for-byte equivalent in normative content between editions (verified
above). Both walks reached the same outcome class and the same register row
for every one of these seven probes, from texts that say the same thing. I
read every passage either walker cited and found no case where a cited
passage decided the question differently between editions, and no case where
one walker's text decided it one way while the actual (correctly-read)
passage in that edition said something else (no REPORTER_ERROR). All seven
are **EQUIVALENT**: the surface wording differs (sentence joins, dash removal,
"notwithstanding" → "override", "govern" → stated plainly, light trims of
"SHOULD"/"MAY" supporting clauses) but nothing either edition *decides*
differs, and an implementation built from A alone and one built from B alone
would emit the same bytes and reach the same accept/reject verdict on every
file for every one of these seven probes.

R3 (the zstd / assigned-but-unimplemented-codec case) is the one probe where
both walks independently flagged the *document itself* as underdetermined
(readera-01, readerb-01) rather than disagreeing with each other. I opened
every passage both walks cite for R3 — §2.3 (`[R-CNF-03]`), §17.2
(`[R-COD-03]`), §17.4 (`[R-COD-11]`), §21.6's closing paragraph, §21.9
(`[R-ERR-04]`) and its limits table — in both editions. All five passages are
substantively identical between A and B (§17.2 and §17.4 are word-for-word
except for sentence-boundary punctuation; §2.3 and §21.6 differ only in the
three relocations/trims detailed below, none of which touches the
codec-capability question). The gap both walks found — no register row, no
outcome class, and no behavioral obligation stated for software that is
categorically "not a conforming reader" because it lacks zstd, as distinct
from the fully-specified reserved/experimental-value case (`[R-COD-03]`,
register row L43) — is present, identically, in both editions. This is not a
LOSS introduced by the rewrite and not an ADDITION invented by it: edition B
carried the ambiguity over unchanged. I classify this as **AMBIGUITY, present
in both editions equally** (see cmp-reader-01 below), not as a divergence
between A and B.

## Each walk's own findings, checked against the other edition

- **readera-01 / readerb-01** (the R3 ambiguity): as above — the same gap,
  present in both texts identically. Neither edition resolves it; the
  readable rewrite did not introduce or close this ambiguity. See
  cmp-reader-01.
- **readera-02** (OBSERVATION: probe R4's wording `extent_offset`/
  `extent_length` doesn't match the tile-index entry's own field names
  `offset`/`length`): I confirmed independently that both editions name a
  tile-index entry's two fields `offset` and `length` (§15.1's table, both
  editions, byte-identical) and that `extent_offset`/`extent_length` is both
  editions' name for a *record's* extent slot (§7.2) at a different scope.
  This is a probe-wording artifact common to both editions alike, not a
  textual divergence between them; no finding against either edition.

## Guesses one walker made that the other did not

Reading both transcripts for places where a walker had to re-read, guess, or
range outside its own probe-cited sections (charter #4): reader-a's
transcript explicitly disclaims any such guess for R4 beyond the terminology
note above, and reader-b's transcript explicitly discloses it answered R4 by
reading the entry condition directly against register row T7 with no
alternate candidate considered. Neither walker reported having to go outside
its cited sections for any of R1–R8, and neither transcript records
re-reading a passage because its first reading seemed wrong. I found no case
where one edition forced a guess the other edition's walker avoided; both
walks' citation sets for each probe draw from the same substantive passages
in both editions (confirmed above), so there is no textual basis for one
walker needing to search further than the other.

## Findings

### cmp-reader-01 [AMBIGUITY, present in both editions equally]

**Location A:** §2.3 (`[R-CNF-03]`), §17.4 (`[R-COD-11]`), §21.6 closing
paragraph, §21.9 (`[R-ERR-04]`).
**Location B:** §2.3 (`[R-CNF-03]`), §17.4 (`[R-COD-11]`), §21.6 closing
paragraph, §21.9 (`[R-ERR-04]`) — same sections, same requirement IDs.

Both walks independently found that the document assigns no outcome class,
register row, or behavioral obligation to a reader that is categorically
"not a conforming reader" because it cannot execute an assigned, core codec
or filter (e.g. zstd, codec 3) that a layer validly declares — as distinct
from the fully specified case of a *reserved or experimental* codec value
(reject-layer, register row L43, `[R-COD-03]`). I read every passage either
walk cited in both editions and the wording is identical in substance:
§17.4's `[R-COD-11]` sentence is word-for-word the same in both editions:
"For a conforming reader that position arises only at a reserved or
experimental value, every assigned codec and filter being core: it rejects
the layer (`[R-COD-03]`, `[R-COD-09]`); software unable to execute an
assigned codec or filter is not a conforming reader (`[R-CNF-03]`)." — this
sentence's grammar confines reject-layer to the reserved/experimental case in
both editions equally, and neither edition's §21.6 closing paragraph or
§21.9 limits table contemplates codec/filter capability as a third
"conforming file a reader nevertheless refuses" case or a resource-limit
axis.

**Detail:** this is not a divergence between A and B — the readable rewrite
carried the gap over unrepaired, with its exact textual shape unchanged.

**Quotation A:** "software unable to execute an assigned codec or filter is
not a conforming reader (`[R-CNF-03]`)." (§17.4, `[R-COD-11]`)
**Quotation B:** "software unable to execute an assigned codec or filter is
not a conforming reader" (§17.4, `[R-COD-11]`) — identical text.

**Byte-level test:** an implementation built from A alone and one built from
B alone are equally underdetermined here and can equally diverge from each
other *and from a third implementation of the same edition* (as both walks'
own findings document: refuse-whole-file, reject-layer-only, and
serve-declarations-refuse-tiles are all consistent with either text). The
indeterminacy is edition-invariant, not edition-specific.

### cmp-reader-02 [EQUIVALENT]

**Location A:** §2.3, conforming-reader bullet (`[R-CNF-03]`).
**Location B:** §2.3, conforming-reader bullet (`[R-CNF-03]`), same bullet,
clause absent.

A's bullet reads, in part: "...carrying no top-level record of a type it
does not implement with MUST_UNDERSTAND = 1 — in a conforming file such a
type is necessarily from the experimental range, since a reserved-range
type carrying MU = 1 is itself a violation — and none of whose values
exceeds the minimum guarantees of §21's limits table (§21.9's `[R-ERR-04]`
governs a refusal on that last ground; §21.6's closing paragraph names the
other two)...". B's corresponding sentence reads: "...carrying no top-level
record of a type it does not implement with MUST_UNDERSTAND = 1 and none of
whose values exceeds the minimum guarantees of §21's limits table
(§21.9)...". Both dashed/parenthetical clauses are absent from B.

**Detail:** the first dropped clause states a derived fact (an unimplemented
MU=1 top-level type in a conforming file must be experimental-range, since a
reserved-range type's mere emission is itself a violation under `[R-CNT-15]`
whatever its MU bit). That underlying rule — "emitting one is a violation
whatever its MU bit" — is stated identically in both editions' §21.6 table
(the "record type ... from the experimental range ... carries MU = 0" row:
"a *reserved*-range type is read the same way, but emitting one is a
violation (F36, L25)") and in both editions' register row F36. The fact A's
dropped clause states is therefore still fully derivable from B's own
unchanged text; it was never an independent rule, only an explanatory
inference A spelled out and B left for the reader to draw. The second dropped
clause is pure cross-reference ("which section argues which part") and its
content (the R-ERR-04 ground, and the "other two" cases) is stated in full in
both editions' §21.6 and §21.9, unchanged.

**Quotation A:** "in a conforming file such a type is necessarily from the
experimental range, since a reserved-range type carrying MU = 1 is itself a
violation" (§2.3, `[R-CNF-03]`).
**Quotation B:** absent at this location; the underlying rule it derives from
survives verbatim at §21.6: "a *reserved*-range type is read the same way,
but emitting one is a violation (F36, L25)".

**Byte-level test:** no. Nothing a reader, writer, or verifier does turns on
this sentence; it is an explanatory aside whose premise is independently
fixed by `[R-CNT-15]`/F36 in both editions. An implementation built from B
alone reaches the identical accept/reject verdict as one built from A alone
on every file, because the operative rule (`[R-CNT-15]`'s MU-bit-only
rejection test) is unchanged and does not depend on this aside.

### cmp-reader-03 [EQUIVALENT — reorganization, not loss]

**Location A:** §2.3, conforming-verifier bullet (`[R-CNF-11]`): inline list
of the five grounds on which a verifier reports *cannot establish*.
**Location B:** §21.6, new closing paragraph (after the "two structural
cases" paragraph): the same five grounds, restated, with §2.3 now reading
"...the last where some requirement is one it is unable to check on a
capability or resource ground (§21.6 names the grounds)."

**Detail:** A states the five *cannot-establish* grounds (unimplemented
format major; MU=1 record of an unimplemented type; cannot execute a codec
or filter; declines a layer's/tile's decode on resource grounds; declines to
decode a user-metadata document) inline inside §2.3's verifier bullet. B
moves this same five-item list, word for word on each item, to a new
standalone paragraph at the end of §21.6, and shortens the §2.3 bullet to a
pointer. I confirmed by direct comparison that B's §21.6 paragraph enumerates
the identical five grounds with the identical citations
(`[R-COD-11]`/§17.4, `[R-ERR-04]`/`[R-SER-05]`/`[R-SER-08]`, `[R-MTA-09]`)
that A's §2.3 bullet lists.

**Quotation A:** "...as when the file names a format major version it does
not implement, when a record carries MUST_UNDERSTAND = 1 with a type it does
not implement (§21.6), when it cannot execute a codec or filter
(`[R-COD-11]`), when it declines a layer's or a tile's decode on resource
grounds and so cannot check §14's decoded-content obligations
(`[R-ERR-04]`, `[R-SER-05]`, `[R-SER-08]`), or when it declines to decode a
user-metadata document (`[R-MTA-09]`)." (§2.3, `[R-CNF-11]`)
**Quotation B:** "A verifier is unable to check a requirement on a
capability or resource ground, and so reports *cannot establish*
(`[R-CNF-11]`), as when the file names a format major version it does not
implement, a record carries MUST_UNDERSTAND = 1 with a type it does not
implement, it cannot execute a codec or filter (`[R-COD-11]`, §17.4), it
declines a layer's or a tile's decode on resource grounds and so cannot
check §14's decoded-content obligations (`[R-ERR-04]`, `[R-SER-05]`,
`[R-SER-08]`), or it declines to decode a user-metadata document
(`[R-MTA-09]`)." (§21.6)

**Byte-level test:** no. The content relocated, not lost; every ground, every
citation, and every requirement ID is present in both editions, so no
implementer's behavior differs.

### cmp-reader-04 [EQUIVALENT — minor trim]

**Location A:** §2.4, opening paragraph, final two sentences.
**Location B:** §2.4, opening paragraph, sentences absent.

A's §2.4 opens: "Every detectable file-conformance violation named by this
specification is assigned exactly one **reader outcome**: reject-file,
reject-layer, reject-tile, or ignore-record. `[R-CNF-07]` The same
vocabulary is used for defined conditions that are not violations (an
unknown ancillary record is *ignored*, not rejected). **preserve-verbatim**
names an updater obligation, orthogonal to reader outcomes: a record a
reader ignores can still be one an updater preserves." before the outcome
table. B's §2.4 goes straight from the `[R-CNF-07]` sentence to the table,
omitting both the "same vocabulary... not rejected" sentence and the
"preserve-verbatim... orthogonal to reader outcomes" sentence.

**Detail:** this is the one trim I found whose dropped content is not
restated anywhere else, word for word, in B — it is the most substantive of
the three. However: (1) the **preserve-verbatim** row itself, with its own
operative definition ("Binds updaters: the bytes are carried forward
unmodified... §20.4's table states the cases: its MU = 1 and MU = 0 / PE = 1
rows"), is present unchanged in B's table immediately following, so the
*rule* preserve-verbatim names is not lost, only this one summary sentence
calling it "orthogonal to reader outcomes." (2) The point that "ignore-record"
vocabulary is reused for non-violations is illustrated, not stated as a
general principle, by B's own §21.6 table, which does use the literal phrase
"Ignore-record" for two conditions explicitly listed as non-violations (the
experimental-range document-encoding row, and the resource-decline row) —
so the usage pattern A's dropped sentence named explicitly is still
observable (by example rather than by rule-statement) in B. Neither dropped
sentence states a requirement with its own ID; both are explanatory.

**Quotation A:** "The same vocabulary is used for defined conditions that
are not violations (an unknown ancillary record is *ignored*, not
rejected). **preserve-verbatim** names an updater obligation, orthogonal to
reader outcomes: a record a reader ignores can still be one an updater
preserves." (§2.4)
**Quotation B:** absent; the table's preserve-verbatim row survives
unchanged.

**Byte-level test:** no. No requirement ID attaches to either dropped
sentence, and the operative preserve-verbatim rule (table row, and §20.4's
own treatment, unaffected) is unchanged. An implementer reading only B
still has the preserve-verbatim definition and can still observe
"ignore-record" applied to §21.6's non-violation rows directly; nothing
about what bytes a conforming updater or reader produces turns on these two
summary sentences. I flag it because it is the one case in this round where
an explanatory generalization, rather than a pure cross-reference or a
derivable corollary, was dropped outright rather than relocated — worth the
maintainer's attention as a readability regression even though it clears the
byte-level bar for EQUIVALENT.

## Sections read past the probes with no divergence found

§4.2 (integer domains — A's "entry counts and slab run lengths included"
example-list is trimmed in B but the general term "count" it exemplifies is
unchanged and the `[R-ENC-03]`/`[R-ENC-04]` rules are identical); §5.1 (the
128-byte floor, `[R-CNT-27]`, byte-identical); §9.7 (coverage verification,
`[R-SLB-03]`/`[R-IDX-03]` interaction, byte-identical in substance); §10.1
(the four growth vehicles, `[R-EXT-01]`, byte-identical); §10.2 (identifier
space table, byte-identical); §15.1–§15.3 (tile-index layout, sentinel, and
the full entry-validity table including register row T7, byte-identical);
§21.2 and §21.4 (the file-scope and tile-scope register tables, byte-
identical markdown tables, confirmed row by row for F1–F36 and T1–T26).

## Evidence

(See the structured `evidence` object for the required
sweeps/derivations/rejected-candidates/confidence-empty summary.)
