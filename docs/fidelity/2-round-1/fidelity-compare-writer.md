# writer comparator transcript — TARN fidelity round, fidelity-3

## 0. Disclosure (mandatory, read first)

**Harness "user request" line.** Before my computed task text arrived, the
harness relayed a separately voiced line: "Set the constant to
claude-sonnet-5, preflight with --models, then launch." This reads as
launcher/meta-level instruction (configuring and starting the very round that
spawned this session), not as a task for me, the already-launched
writer-comparator, to perform. I have not treated it as an instruction to do
anything beyond the computed brief below, and have not run any preflight,
edited any constant, or launched anything. I note its presence per the
disclosure obligation and do not act on it.

**Context that arrived unasked.** My context already contained CLAUDE.md's
pointer to AGENTS.md (not read), the user's MEMORY.md index (a list of titled
notes about this same TARN project — not read as files, only the titles were
visible), and git-status/environment blocks naming the current branch
("readable") and recent commit subjects. None of this is the specification
and none of it is evidence about its content; I have not opened any of the
referenced memory files, AGENTS.md, docs/, or any other path outside the
ACCESS RULE.

**Files read, exactly:**
1. `/Users/robertkleffner/Documents/GitHub/tarn-first-draft/scratch/cleanroom/editions/a/tarn.md` (edition A, 4,981 lines)
2. `/Users/robertkleffner/Documents/GitHub/tarn-first-draft/spec/tarn.md` (edition B, 4,847 lines)
3. `/private/tmp/claude-501/-Users-robertkleffner-Documents-GitHub-tarn-first-draft/fidelity-3/out/transcript-writer-a.md` (walk from A, 502 lines)
4. `/private/tmp/claude-501/-Users-robertkleffner-Documents-GitHub-tarn-first-draft/fidelity-3/out/transcript-writer-b.md` (walk from B, 476 lines)

I did not list any directory other than my own scratch directory (confirmed
empty before I wrote to it) and the directory holding the two transcript
files (whose contents, not listing, I needed — I opened each by its exact
given name via the Read tool, no `ls`). I ran `diff -u` between the two
edition files (local computation reading only files 1 and 2 above, no other
file) to localize every textual difference between the editions, then
`grep -n` against files 1 and 2 for specific requirement IDs and phrases to
confirm or refute each candidate the diff raised. Every grep below is
reported with its hit count; where a count is 0 I give the control search
that proves grep itself was working (hard-wrap note below).

**Hard-wrap check.** Both files contain ordinary prose paragraphs (not
blockquote-reflowed) up to ~80 columns and table rows up to 1,608 columns; I
did not find them reflowed under a "> " blockquote prefix at the specific
passages I quote below (I checked each passage's raw lines directly with
Read, not only grep). Where I searched by phrase, I used fragments short
enough to sit inside one visual line of the surrounding prose, and where a
grep returned 0 I re-ran it as a substring search for a shorter, known-present
fragment of the same sentence to confirm the pattern itself was not the
problem (e.g., control `grep -c "trailer magic"` returned 9 in A and 8 in B,
proving ordinary substring grep does find real hits in both files).

## 1. Method

1. `diff -u` the two edition files in full (1,529 lines of unified diff,
   `/private/tmp/.../scratch/compare-writer/full.diff`). This is the ground
   truth for "what differs between A and B, anywhere in either file" and
   lets me locate every hunk's corresponding section instead of reading
   ~10,000 lines of near-identical prose twice.
2. Extract the `@@` hunk header list: 24 hunks, concentrated almost entirely
   between A-lines 9 and ~1270 (Part 0: Preliminaries, §1–§4; and Part I:
   §5 Anatomy, §6 Front block/Trailer, §7 Directory/Records, §8 Integrity),
   plus six small, isolated single- or few-line hunks later (at A-lines
   1793, 2636, 4074 [a genuinely new paragraph], 4332, 4399, 4585) that are
   either a cross-reference renumbering (§7.1 → §7.3, after content moved)
   or trivial copy-edits.
3. Cross-reference this hunk map against every probe's cited sections:
   - W1 cites §5.1, §6.1, §6.2, Appendix A — **inside** the edited zone.
   - W2–W11 cite §7.2, §9.2/9.4–9.6, §12.1, §20.1–20.5, §21.2–21.7 —
     **outside** the edited zone (confirmed: no diff hunk touches §9 at
     all; none touches §12.1, §20.x, or §21.2–21.5/21.7; the one hunk
     touching §21.6 is the new paragraph discussed in cmp-writer-02).
4. For every hunk inside the edited zone, read both sides of the diff as
   full sentences (not just the changed tokens) and classify: wording-only
   readability edit (no quantifier, modal verb, or cited rule-ID changed),
   content relocated (same substance, different section), or substantive
   change (a figure, a condition, or a modal obligation actually changed).
5. For every section a probe cites outside the edited zone, grep the
   governing requirement ID in both files and diff the surrounding
   paragraph directly (via Read) to confirm byte-for-byte identity where the
   hunk map predicts none, rather than trusting the prediction alone.
6. Read both walk transcripts in full, and for every sentence either walker
   attributes to its edition, located that sentence in both editions (not
   just the one the walker read) to check whether the two texts actually
   agree where the walkers' answers agree, and actually disagree where
   their answers disagree.

## 2. Section-by-section findings inside the edited zone (§1–§8)

I read every one of the 24 diff hunks in context (full paragraphs, not
diff fragments). All but one are wording-only: shorter sentences, fewer
em-dash-delimited asides, parenthetical citations moved inline, cross-
reference renumbering after content moved. None of them:
- changes a byte offset, field width, or numeric constant (checked
  specifically for §5.1's 128-byte floor, §6.1's front-block layout table,
  §6.2's trailer layout table and field list, §6.3's flag/version rules,
  §6.4's two-request accounting, §7.2's record-framing rules and
  multiplicity rules, §7.3's flag table, §7.4's layer-record field table,
  §8.1's coverage-map exceptions and chain-of-trust order);
- changes a modal verb (MUST/MUST NOT/SHOULD/MAY) on any requirement I
  could match between the two sides of a hunk;
- drops a named exception, carve-out or worked numeral — **with one
  exception**, detailed as cmp-writer-02 below, which is additive (a new
  paragraph) rather than a drop, and is not itself a LOSS once the rest of
  the document is read (see finding).

One piece of content (the "Metadata compression exists only at record
granularity… quarantined …" paragraph, `[R-CNT-25]`) moved from the end of
§7.1 (A) to the end of §7.2 (B), word-for-word (I diffed the two paragraphs
directly: A lines 979–1005 against B lines 944–971; identical content,
reordered sentences in two places, no clause dropped). This is EQUIVALENT:
it changes no byte-level or verdict-level outcome; I did not write it up as
a numbered finding because it decides nothing differently, but I record it
here since the charter asks for every rule/exception found migrating.

## 3. Findings

### cmp-writer-01 — REPORTER_ERROR, W6, §20.3 step 4 + §21.7 (identical text in A and B)

Both editions state, at §20.3 step 4 (A lines ~3305–3319; B's corresponding
unmoved text — this passage is outside the edited zone, confirmed
byte-identical by direct `grep -n` for `T2, T4` in both files, each
returning exactly one hit, same sentence):

> "...with every checksum in §8 certifying the result and, but for a stored
> tile's decoded size, a padding position or pad bit, or a boolean byte the
> register witnesses (T3, T14, T21, T22, T4, T5, T2) and a decode that fails
> outright, or a codec's framing check that precedes it, under a changed
> codec or filter (T17, T24, T25), no check any actor owes able to see it
> (§21.7)."

T4 is §14.5's padding-content rule: a layer's padding positions must equal
its declared fill. Read plainly, this sentence says the "no check can see
it" conclusion for a disallowed fill-change commit holds **only where none
of the named exceptions apply** — and T4 is named. So where the layer **has**
at least one padding position (some dimension's extent not an exact
multiple of its tile extent), a forbidden fill-only change **is** witnessed:
the already-stored padding bytes were encoded under the old fill and no
longer match the newly-declared one, which T4 catches. Only a layer with
**zero** padding positions escapes every check.

Writer-a's answer (from edition A) states exactly this conditional, traces
it to T4 by name, and marks it `[underdetermined]` pending the padding
fact — a careful, text-faithful reading.

Writer-b's answer (from edition B) states, unconditionally: "...a fill-only
change is in fact unwitnessed — no check any actor owes able to see it,"
and finding writerb-04 repeats the same unconditional claim, citing the very
same T-number list ("padding positions, pad bits, boolean bytes — T2, T4,
T5, T14, T21, T22, T3...") and then asserting "A fill change alone is not in
that named list" — which is simply false of a layer that has padding: T4
*is* on that list, and T4 is exactly the padding-position check that a
fill-only change (on a layer with padding) breaks. Writer-b quotes the
sentence that defeats its own "unwitnessed" conclusion without noticing the
defeat.

Because the cited passage is byte-identical in both editions (confirmed:
`grep -n "T3, T14, T21, T22, T4, T5, T2"` returns exactly one hit in A and
one in B, same sentence, same T-numbers, same parenthetical), this is not a
fidelity difference between A and B — it is writer-b misreading a text that
decides the question, the text being the same text writer-a read correctly.

- **Byte-level test (either edition):** yes, this matters. A verifier built
  from writer-b's stated rule ("fill-only changes are never detectable")
  would skip the T4 padding-content check specifically for a layer whose
  fill was changed by a forbidden direct commit, and so would certify as
  conforming a file that a verifier correctly implementing T4 would reject
  at layer scope (a padding-position byte no longer equal to the newly
  declared fill). A verifier built from writer-a's stated rule implements
  the conditional correctly and would not make this error.

### cmp-writer-02 — OBSERVATION (bordering AMBIGUITY), §2.3 + §21.6, genuine A/B textual difference

This is the one place my diff of the edited zone turned up content in B
with no counterpart anywhere in A (not relocated — new prose), outside the
one EQUIVALENT relocation noted in §2 above.

**A** states the "cannot establish" verdict's grounds inline, in §2.3's
Conforming-verifier bullet, and immediately appends a disclaiming sentence
right there:

> "...or *cannot establish* — the last where some requirement is one it is
> unable to check on a capability or resource ground, as when the file names
> a format major version it does not implement, when a record carries
> MUST_UNDERSTAND = 1 with a type it does not implement (§21.6), when it
> cannot execute a codec or filter (`[R-COD-11]`), when it declines a
> layer's or a tile's decode on resource grounds and so cannot check §14's
> decoded-content obligations (`[R-ERR-04]`, `[R-SER-05]`, `[R-SER-08]`), or
> when it declines to decode a user-metadata document (`[R-MTA-09]`). **A
> user-metadata document under an experimental-range encoding — one this
> specification does not assign and a conforming file can carry (§21.6) —
> is not such a ground: no content rule attaches there, so nothing is left
> unchecked, and certification is unaffected (`[R-MTA-10]`); encoding 0 and
> a reserved value are violations (§21.5, R1).**"

**B** shortens the §2.3 bullet to a forward pointer: "...or *cannot
establish*, the last where some requirement is one it is unable to check on
a capability or resource ground (§21.6 names the grounds)." — dropping the
disclaiming sentence from this location — and instead adds a **new**
paragraph at the very end of §21.6 (confirmed absent from A by `grep -n
"cannot establish"` and `grep -n "R-CNF-11"`: A has no occurrence between
its §21.6 closing paragraph and §21.7's heading; B has one, the new text):

> "A verifier is unable to check a requirement on a capability or resource
> ground, and so reports *cannot establish* (`[R-CNF-11]`), as when the file
> names a format major version it does not implement, a record carries
> MUST_UNDERSTAND = 1 with a type it does not implement, it cannot execute a
> codec or filter (`[R-COD-11]`, §17.4), it declines a layer's or a tile's
> decode on resource grounds and so cannot check §14's decoded-content
> obligations (`[R-ERR-04]`, `[R-SER-05]`, `[R-SER-08]`), or it declines to
> decode a user-metadata document (`[R-MTA-09]`)."

This new paragraph restates the same five grounds as A's inline list, but
**without** A's adjacent disclaimer that an experimental-range user-metadata
encoding is *not* such a ground. Taken alone, a reader of this one paragraph
could misread "declines to decode a user-metadata document (`[R-MTA-09]`)"
as covering the experimental-range case too, and wrongly report *cannot
establish* for a file that both editions actually require to be certified
*conforming*.

I checked whether the disclaimer is lost outright: it is not. Both §21.5's
own prose ("...except at an experimental-range encoding, where no document
rule attaches and §21.6 records the defined non-violation [`R-MTA-10`]...")
and §21.6's Conditions-that-are-not-violations table row ("A user-metadata
record declares an experimental-range (≥ 0x80) document encoding | Ignored
(ignore-record); the file is conforming...") are byte-identical in both
editions (outside the edited zone; confirmed by direct read of both files
at the respective lines). So the rule is fully determinate in B's complete
text — it is just no longer co-located with the "cannot establish" grounds
list the way A deliberately places it, and B's new paragraph, read by
itself, omits the one disclaimer most relevant to the ground it itself
names last.

- **Kind:** not a LOSS (the rule survives, unchanged, elsewhere in B) and
  not an ADDITION (B decides nothing A left open — every grounds the new
  paragraph names already has its own citation to an unchanged rule). I
  record it as an OBSERVATION because it is a real difference in what a
  reader gets from reading *only* the passage that states the "cannot
  establish" grounds, and because the specification's own authors evidently
  judged the adjacency worth stating deliberately in A (the disclaiming
  sentence is explicitly placed right after the list it qualifies, not left
  to a cross-reference).
- **Byte-level test:** no divergence for an implementer who reads either
  edition in full; a possible divergence for an implementer who reads only
  the single paragraph enumerating "cannot establish" grounds without
  following its own citations into §21.5/§21.6's tables.

### cmp-writer-03 — OBSERVATION, §2.3, shared ambiguity, unequal walker diligence

Writer-b's finding writerb-01 flags a genuine tension: §2.3's "Conforming
updater" bullet says an updater works "without necessarily understanding
all of its content," while the adjacent "Conforming verifier" bullet says
"Verifiers and updaters are readers of the files they process and inherit
every reader obligation" — and `[R-CNF-03]`'s no-subset-profiles rule
(binding "conforming reader[s]") would, read literally through that
inheritance sentence, require full codec/sample-type coverage of an
updater too, in tension with the understanding exemption.

I confirmed, directly, that **both** sentences are byte-identical in A and
B (A's "Conforming updater" bullet: "...without necessarily understanding
all of its content... Its tiers, the appender and the rewriter, are
§20.1's..."; B's: same words, reordered clause only — no substantive
change; A's "Conforming verifier" bullet's "Verifiers and updaters are
readers of the files they process and inherit every reader obligation" is
untouched by the diff in both). So this ambiguity belongs to **both**
editions equally — it is not a fidelity difference. What differs is walker
diligence: writer-a's own transcript explicitly considered and rejected
this exact scenario ("Whether a rewriter facing a sample-type it cannot
decode 'cannot be a conforming updater at all' — rejected: §2.3 and §3.3's
Note explicitly define 'conforming updater' as not necessarily
understanding the file's content...") without engaging the specific
"inherit every reader obligation" sentence that creates the tension
writer-b names; writer-b's transcript quotes that sentence directly and
treats the tension as live and unresolved (writerb-01, writerb-03).

- **Kind:** OBSERVATION, not LOSS/ADDITION (edition-neutral: the shared
  text is genuinely ambiguous on this point in both A and B). Not a
  REPORTER_ERROR either, strictly: writer-a's ultimate W8 answer (carrying
  the layer forward, checksum-only, is permitted) is the same conclusion
  writer-b reaches by probe's end, so no probe answer is wrong — only
  writer-a's confidence in rejecting the ambiguity is less supported by the
  text it quotes than writer-b's parallel discussion.
- **Byte-level test:** none between editions (identical text); within either
  edition alone, the ambiguity could in principle license two different
  conformance verdicts for a rewriter that has not implemented one of the
  thirteen core sample types, depending on which of the two bulleted
  sentences a given implementation treats as controlling — a defect of A
  (and, unchanged, of B), not a divergence between them.

## 4. Where the probes agreed and I found no divergence worth reporting

For W1–W5, W7, W9, W10, and (modulo cmp-writer-01) W6, and (modulo
cmp-writer-03) W8, and W11, I read the cited passages directly in both
editions at the location each walker gave and found them byte-identical or
differing only in confirmed-cosmetic ways (shorter sentences, inline vs.
footnoted citations, no changed modal verb, figure, or named exception).
Specifically checked byte-identical, by direct grep of a governing
requirement ID plus a Read of the surrounding paragraph in both files:
`[R-WRT-04]`/`[R-WRT-05]` and the 644-byte worked example (W2); `[R-CNT-15]`,
`[R-WRT-06]` (W3); the MU=0/PE=0 row's "drop-only commit" licence (W4);
`[R-CNT-08]`, `[R-WRT-01]`, §20.1's creator/rewriter split (W5); the §20.4
drop-licensing paragraph and its sub-record veto sentence (W9, W10); the
§20.4 opening paragraph's "only the PE bit bites" sentence and `[R-CNT-12]`
(W11); §9.2's commit protocol and §9.4–9.6's recovery procedure (W7); and
Appendix A's byte table plus §6.1/§6.2's layout tables (W1). None of these
diff; the two walkers' agreement on these probes reflects identical source
text, not coincidence — I checked rather than assumed it per charter item 2.

## 5. What I did not find

I looked for, and did not find: any numeric constant (byte offset, CRC
value, field width, the 128-byte floor, the 644-byte index-region figure,
the 64-byte trailer size) that differs between the editions anywhere the
diff touches; any modal-verb flip (MUST vs. SHOULD vs. MAY) on a
requirement I could align across a hunk; any dropped exception or carve-out
other than the one discussed as cmp-writer-02 (and that one survives
elsewhere, so is not a true drop); and any divergence at all in the text
underlying W1 through W11 beyond cmp-writer-01's identical-text reporter
error and cmp-writer-03's identical-text shared ambiguity. The fidelity
round's substantive editorial work so far (confirmed by the diff's hunk
map) covers Part 0 and §5–§8 only; §9 through §24 and the Appendices are
untouched prose in this edition pair, with the single exception of the new
§21.6 paragraph (cmp-writer-02) and a handful of §7.1→§7.3 cross-reference
renumbers following the one content relocation noted in §2.
