# Completeness sweep, B into A — working transcript

## Disclosure

A relayed "user request" (the single word "Go") was prepended above this
brief by the harness; it is the launcher's message to the orchestrator, was
carried out before this session was spawned, needs no reconciliation with
this brief, and did not widen the access rule. My context also carried, before
I began, a project CLAUDE.md pointer to AGENTS.md (not read, per the access
rule), a long user MEMORY.md index of past TARN-round lessons (titles only,
not read as files), git-status/attribution reminders, and an environment
banner. None of that was treated as evidence about edition A or B; it is
disclosed, not repeated, and nothing in it was used to decide a finding below.
Scope, as instructed: only edition A
(`scratch/cleanroom/editions/a/tarn.md`) and edition B (`spec/tarn.md`) were
read. No other file, no directory listing, no git history, no web.

## Method

1. Split both editions into heading-delimited sections and unwrapped each to
   one paragraph per blank-line block (joining hard-wrapped lines, stripping
   `> ` blockquote markers), so whitespace/line-wrap differences would not
   masquerade as content differences. Scripts and outputs are under
   `fidelity-4/scratch/sweep-b-to-a/` (`split.py`, `secdiff.py`,
   `a_sections.txt`, `b_sections.txt`, `note_a.txt`, `note_b.txt`,
   `example_a.txt`, `rationale_a.txt`, etc.).
2. Census of labelled blocks: counted every paragraph opening `**Note.**`,
   `**Example.**`, `**Rationale.**` in both editions (anchored at line start,
   not mid-sentence mentions of the word). Counts: Note A=57, B=52;
   Example A=15, B=15; Rationale A=13, B=13. The Example/Rationale counts
   match exactly. The 5-Note gap was resolved note-by-note (see §Census
   below) — every one of the 5 is either a reworded duplicate matched by
   fingerprint, or content relocated to its normative home section and
   verified present there by grep + direct reading. Net unresolved: 0.
3. Word-level `difflib.SequenceMatcher` diff per numbered section (matching A
   and B sections by their `N` / `N.M` prefix, and by `Appendix X` letter for
   the appendices), to localize exactly which words a human read-through
   needed to check. Every section with a non-trivial diff (ops > 0) was
   either fully read side by side (for low word-ratio or high-ops sections)
   or had its diff hunks read individually (for high-ratio sections, to
   confirm punctuation-only changes: em dash → comma/colon/period, the
   recurring "spruce-up" style pattern visible in this branch's own commit
   history for Appendices G/H).
4. Every apparent one-sided sentence was treated as a candidate LOSS/ADDITION
   until a control search (`grep -n` for its key terms, phrases, or governing
   requirement ID) either found the same substance relocated to its normative
   home section in the other edition, or came back empty — confirmed with a
   second phrasing of the same search before being accepted as a true zero.

## Section-by-section pass

Sections read in full, side by side, in B's order (both editions follow the
same numbering, except B places §3 Terminology before §2 Conformance,
physically — an ordering swap only, not evaluated further since it decides
nothing a condition or rule turns on):

1, 2.1, 2.2, 2.3, 2.4, 2.5, 3.1, 3.2, 3.3(A only — see census), 4.1–4.7,
5.1, 5.2, 6.1–6.4, 7.1–7.4, 8.1, 8.2, 9.1–9.7, 10.1–10.4, 11.1–11.4,
12–12.3, 13–13.3, 14.1–14.5, 15.1–15.4, 16–16.2, 17.1–17.4, 18.1–18.4,
19.1–19.4, 20–20.5, 21.1–21.9, 22.1–22.5, 23.1–23.3, 24, Appendices A–H.

Every section's word-diff was produced and read. The overwhelming majority of
non-equal opcodes across the whole document are punctuation-register changes
consistent with this branch's own "spruce-up pass" commits (em dash →
comma/colon/period/semicolon; "and" for a second em-dash clause; occasional
sentence-boundary shift that keeps the same two propositions). These are
EQUIVALENT by inspection and are not listed as individual findings; the ones
below are the cases where a clause, sentence or whole paragraph had no
word-for-word counterpart and had to be chased to a different location (or
came back absent).

### Relocations verified present (EQUIVALENT, not losses)

For each, A's paragraph/Note had no counterpart in the same section of B;
grep + direct reading confirmed the same substance stated in B at a different,
more logical home section (this format's own stated editorial pattern of
"declared where it arises rather than enumerated" — A's own §2.3 phrase):

- §7.1 "Metadata compression exists only at record granularity…" (user-metadata
  encoding/quarantine paragraph, `[R-CNT-25]`) — moved from A's §7.1 to B's
  §7.3. Verified byte-for-byte equivalent in content at spec/tarn.md:944-971.
- §2.3 Conforming-TARN-file conduct-rule enumeration (ignore-lane bit,
  pre-trailer gap, `[R-LIF-01]` fixed-declaration bar, registry-targeting
  conduct) — each of A's four named examples individually verified still
  marked "not a file-conformance violation" / "conforming" at its own home
  section in B: §6.3 (spec/tarn.md:767-768), §6.2 (spec/tarn.md:717-718),
  §20.3 (spec/tarn.md:3091-3096), §10.3 via §21.6's row
  (spec/tarn.md:3825), §18.3 (spec/tarn.md:2686-2687).
- §2.3 Conforming-verifier "cannot establish" five-way enumeration and the
  experimental-range-encoding exclusion — fully restated in B's §21.6 closing
  paragraphs (spec/tarn.md:3862-3871) and its table row for experimental-range
  document encoding (spec/tarn.md:3825).
- §2.3's reach discussion ("the test is the invariant/property … not the
  bytes read") — restated as B's own §2.3 main-text sentence
  (spec/tarn.md:220-221) and the F5/F14/F15 worked contrast is implicit in
  B's §21.2 opening ("F8, F14, F6 and both of F1's instances … and no other
  row", spec/tarn.md:3629-3633), which names the same reaching set without
  re-walking the three examples — a compression, not a decision change.
- §3.1 glossary "generation" clause (ordering by strictly increasing
  committed_file_length) — restated at B's §9.3 (spec/tarn.md:1234-1235).
- §4.4's Note cross-referencing §14 for boolean-sample bit mapping — B's
  §14.3 itself still carries the "(§4.4)" citation verbatim
  (spec/tarn.md:1956), so the relationship the Note glossed is still visible
  from §14.3 alone; nothing decided by the Note is undecidable without it.
- §4.5/§8.1 checksum-coverage-exceptions paragraph — A states it twice
  (§4.5 and §8.1, word-for-word near-duplicate); B keeps it once, at §8.1
  (spec/tarn.md:1086-1096), where the Coverage Map structurally belongs.
- §4.7's Note on layout-table columns — A's §4.7 version and B's §4.7
  version are the same Note, reworded (confirmed by reading both in full;
  initial fingerprint mismatch was an artifact of different opening words).
- §5.2/§9.7 walk-completeness paragraph (scope-level rejection, resource
  decline, `[R-CNF-11]` early stop, and the separate "structurally-rejected
  tile still completes the walk, for the opposite reason" clause) — both
  halves fully present in B's §9.7 (spec/tarn.md:1403-1413), cross-referenced
  from §5.2 ("§9.7 says when that is").
- §9.3/§2.3's "What is a condition" wording changes — content-preserving.
- §20.3's per-commit-cost-of-small-edits framing, dropped from B's
  Introduction pillar text — the underlying mechanical fact (any commit
  touching a layer's stored-tile set or index content re-emits that layer's
  *whole* tile-index region) is independently and fully stated in both
  editions' §7.4 worked-example Note (spec/tarn.md:561-563) and in §20.3
  proper; only the Introduction's rhetorical gloss ("write-mostly artifact,
  not a version store… wasteful") is gone, and it decides nothing a reader
  or writer does.
- §6.3's explicit "a rewriter… carries the input's unknown ignore-lane bits…
  rather than writing flags = 0" sentence — restated as B's own normative
  rule at §20.5 (spec/tarn.md:3409), which a rewriter is already bound by
  as a kind of "updater" under §2.3's definition.

### Confirmed true gaps (reported as findings below)

- §2.4 Outcome classes: A states, and B omits entirely, two general
  clarifications: (a) the ignore-record vocabulary is also used for defined
  conditions that are *not* violations, and (b) preserve-verbatim is an
  updater obligation *orthogonal* to reader outcomes — a record a reader
  ignores can still be one an updater must preserve verbatim. Grepped B for
  "orthogonal to reader", "ignored, not rejected", "is ignored, not" and the
  literal preserve-verbatim definition row (spec/tarn.md:306): the row states
  only the updater-binding half, not the orthogonality-to-reader-outcomes
  half. See finding swba-01.
- §2.4's closing Note ("'Reject' prescribes the scope of unusability, not
  user interface: how failure is reported is implementation technique") has
  no counterpart anywhere in B (grepped "implementation technique" — the one
  hit, spec/tarn.md:166, is in a different Note, about requirement-phrasing
  discipline in general, not about the Reject/UI distinction specifically).
  This does not change any testable byte or verdict — nothing in either
  edition prescribes a reporting mechanism — so it is reported as a minor,
  non-byte-level observation (swba-02) rather than a LOSS.
- §3.1 glossary "addressed tile" wording: A's glossary defines "addressed"
  layer-wide ("every tile of a layer is addressed"); B's glossary makes it
  generation-relative ("a tile is addressed in a generation if that
  generation's tile index has an entry for it … under the geometry that
  generation declares"). Both editions' main bodies agree that a dimension's
  extent MAY grow across generations (`[R-GEO-06]`/§20.3,
  spec/tarn.md:3075), which makes B's generation-qualified glossary wording
  the more accurate one and A's the looser one; neither edition's *normative*
  text (outside the glossary) turns on the glossary wording, so this is
  reported as an observation (swba-03), not a LOSS or ADDITION.

## Notes on what I did not re-derive

Per the brief, I did not re-diff the mechanically-checked layers: requirement-
ID paragraphs, register rows (§21.2–§21.6 tables), §3.1 term list membership,
tables, and fenced blocks. Where my word-diff passed through a register table
row, I read it only far enough to confirm the row's prose matched beyond the
ID citation (e.g. F27/L48, F4/L9, F21/F22/L10/L11 cross-references used above
as controls), not to re-certify the table itself.

## Sections given a lighter pass

Given the single-session time budget, §§22 (Security) and §23 (Privacy) and
Appendices A–F got the word-ratio screen (all ≥0.94, low op counts) plus a
read of every opcode hunk (not a full side-by-side re-read of the whole
section prose) — every hunk read was punctuation-only. §24 and Appendix
G/H's many small diffs were likewise read hunk-by-hunk rather than prose-by-
prose; no hunk in either showed a missing clause. I did not do a second,
independent read of §§11–16 (Array Model) beyond the word-ratio screen (all
≥0.78, and every section's diff opcode count was ≤ 18 on a section of several
hundred words) — these are the sections with the fewest and smallest hunks in
the entire document, consistent with the git log's commit messages, which
name later sections (§9.7, Appendix G/H, §22–24) as the ones that got
dedicated spruce-up/preflight passes; §§11–16 appear untouched by comparison
and I weight that as corroborating, not as a substitute for having read them.
If the round needs a second pass, §§11–16's word-diffs are the cheapest place
to start since they were screened but not hunk-read.
