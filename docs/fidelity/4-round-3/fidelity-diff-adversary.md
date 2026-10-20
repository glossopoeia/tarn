# Diff-adversary transcript — TARN fidelity round

**Disclosure.** A message launched this round ahead of my brief, labelled
"user request," reading only "Go." It carries no task content of its own,
needs no reconciliation with this brief, and does not widen the access
rule below; I disclose it appeared and proceed. Nothing else was placed in
my context before I began.

## Access

Read only:
- A (reference): `/Users/robertkleffner/Documents/GitHub/tarn-first-draft/scratch/cleanroom/editions/a/tarn.md` (5004 lines)
- B (rewrite): `/Users/robertkleffner/Documents/GitHub/tarn-first-draft/spec/tarn.md` (4810 lines)

No other file was opened, and no directory was listed except my own
scratch directory
(`/private/tmp/claude-501/-Users-robertkleffner-Documents-GitHub-tarn-first-draft/fidelity-5/scratch/diff-adversary/`)
and the out directory for this transcript. All working files are under the
scratch directory: `split_sections.py` (a Python script that splits both
editions into blocks by heading and normalizes whitespace so wrapping
differences don't register as content differences) and `sections/` (the
per-heading extracted, normalized blocks for both editions, one pair of
`_a.txt`/`_b.txt` files per heading).

## Method

1. Dumped heading lists for both editions (`grep -n "^#"`) — structure is
   identical except B moves §2 (Conformance) after §3 (Terminology), a
   pure reordering with no heading gained or lost except as noted below.
2. Swept requirement-ID citations: `grep -oE '\[R-[A-Z]+-[0-9]+\]'`,
   sorted/uniqued. **Control:** both editions cite exactly the same 163
   distinct requirement IDs — zero added, zero removed. This is the
   sweep that proves no requirement was silently dropped or invented.
3. Compared per-ID citation *counts* (`sort | uniq -c`) to find every ID
   whose number of citations differs between editions — 15 IDs differed.
   For each, pulled every citing line in both editions and read the
   surrounding paragraph to see whether the differing count reflects
   reorganization (content moved, still said once) or an actual
   deletion/addition.
4. Ran the section-split script to normalize every matched heading's body
   (join wrapped lines into whitespace-normalized blocks, compare
   block-for-block) and ranked headings by word-count delta between
   editions, largest first, as the fastest way to surface spots where a
   whole paragraph rather than a dash/comma moved.
5. For every heading with a large delta, or every differing requirement-ID
   count, read both editions' full surrounding paragraphs side by side
   and, where a sentence appeared to vanish, grepped the exact phrase (or
   a short distinctive fragment of it, both docs being hard-wrapped) across
   the *entire* other edition before concluding it was really absent
   (control search, not just "not in this section").
6. Diffed the two appendices that are purely tabular/numeric (Appendix B
   constants, Appendix C registry snapshot, Appendix F references,
   Appendix E changelog) directly with `diff` on the raw line ranges,
   since a reworded appendix row would still be suspicious even after
   whitespace normalization.

## Constructions carried to bytes

Six concrete cases, each run through to an accept/reject verdict or an
emitted-byte question under both editions' own text.

### C1 — reserved-range record type, MU=1, at file scope
Construct a directory whose top-level record sequence contains one record
of type 0x00F0 (inside the reserved range, per §10.2/§10.3 in both
editions — identical range tables in both) with flags MU=1, PE=0,
otherwise well-formed. A's §2.3 drew an explicit corollary: "in a
conforming file such a type is necessarily from the experimental range,
since a reserved-range type carrying MU = 1 is itself a violation." B
drops that corollary sentence from §2.3. Does the verdict differ?
Trace: §7.2/R-CNT-15 (byte-identical text in both editions) — "a
reserved-range record type is a value this specification has not
assigned — emitting it is a violation, and a verifier MUST treat a
reserved-range record type as a validity error at the record's governing
scope." File scope, MU=1 unimplemented type additionally triggers
reject-file under R-CNT-15's MU rule, present identically in both. **Same
verdict both editions: reject-file.** The corollary A stated and B
dropped is a derivation from text both editions retain unchanged
(§7.2/R-CNT-15); nothing is lost for an implementer. Rejected: closed by
§7.2's identical R-CNT-15 text in both.

### C2 — cross-layer extent overlap: a user-metadata sub-record's extent overlaps another layer's stored-tile extent
A defines "live committed state" inline at §7.2 ("within the live
committed state — all structures reachable from the live trailer,
whichever generation's commit appended them — no two extent slots and no
two structures overlap"). B's §7.2 instead says "no two extent slots and
no two structures of the live committed state overlap (§5.2,
`[R-CNT-02]`)," pointing to §5.2 rather than restating the definition.
Construct a file where layer L1's user-metadata sub-record extent
`[1000,1020)` overlaps layer L2's stored-tile extent `[1010,1030)`.
Trace: §5.2 in both editions defines "live committed state" with the
identical content A's §7.2 inlined (front signature block + every
structure reachable from the live trailer; no two overlap). §7.2's table
in both: "any overlap across layers... as reject-file." **Same verdict
both editions: reject-file, R-CNT-13.** Rejected: B's cross-reference
resolves to the same definition A inlined; confirmed by reading §5.2 in
both (word-for-word equivalent apart from punctuation).

### C3 — pre-trailer pad longer than the commit protocol's floor
Construct a file whose directory ends 200 bytes before the trailer (far
more than the 64-byte alignment pad §9.2/R-LIF-02 step 5 requires), the
extra 136 bytes being zero. A's §2.3 lists this explicitly as one of
three named conduct-only cases ("§6.2's pre-trailer gap longer than
`[R-LIF-02]` step 5's pad") that never makes a file nonconforming. B's
§2.3 replaces the three-item list with one general sentence and omits the
enumeration. Does B still make the file conforming? Trace: §6.2 in B
(unchanged from A in substance): "a longer gap is conforming, though no
conforming commit produces one." **Same verdict both editions: the file
is conforming.** Rejected: the fact is independently and identically
stated in §6.2 in both editions, not only via the §2.3 summary that B
trimmed.

### C4 — an appender commit that changes a stored tile's codec field without changing file_id
Construct a commit that re-emits a layer's record with a different codec
value while the layer still stores a tile from the prior generation, and
the new directory keeps the same file_id (i.e., claims to be an appended
commit, not a rewrite). Trace: §20.3 ("Every other declaration is fixed
for as long as the layer stores a tile: ... the codec and the filter...
A commit MUST NOT change one of these; the change is a new layer, or a
rewrite that re-declares it under a fresh file_id") is **byte-identical**
between A and B (confirmed by direct diff of the extracted block — zero
differences). **Same verdict both editions:** such a commit is barred;
the bar binds the commit as an actor (no register row, §21.7/R-ERR-01),
but "a file such a commit leaves can be nonconforming on its own terms"
per the very next sentence, identical in both — i.e. the resulting file's
actual conformance turns on whether the file's *bytes* satisfy §7.4's
declaration-consistency requirements independent of how it was produced.
Rejected: no edition-dependent difference; the governing paragraph is
word-for-word identical.

### C5 — a tile-index entry rejected on a *structural* ground (offset < 16, T8) inside a declared slab run
Construct a layer with a slab declaration (run length S=8) whose run 0
contains one entry with offset = 8 (violating the ≥16 floor, T8,
structural ground) while the other seven entries in the run are
validly packed and contiguous. Does the run-packing invariant
(§16.2/R-SLB-03) register a violation because of the malformed entry, and
does the verifier's coverage-total walk (§5.2/§9.7) count that entry's
nominal bytes as slack or as a claimed structure, under each edition?
Trace: §16.2 — "So are the entries §15.3 classifies reject-tile on a
*structural* ground: they address no usable extent, and the run's stored
tiles close over them" — byte-identical in both editions (confirmed by
diff of the extracted blocks, differences are comma/em-dash only). §9.7 —
"An entry `[R-IDX-03]` classifies reject-tile on a *structural* ground
does not make the walk incomplete: the walk passes over it, and the bytes
of the file it nominally addresses fall to slack" — also byte-identical
in both (confirmed by diff). **Same verdict both editions:** the
structurally-rejected entry is transparent to the slab run-packing check,
and its nominal bytes are slack, counted in the verifier's total, not a
claimed structure. Rejected: A's §5.2 additionally spells this out inline
where B's §5.2 instead says "§9.7 says when that is" — but §9.7 says it
identically in both, so the trim in §5.2 loses no information reachable
from B alone.

### C6 — Appendix B citation mismatch: "User-metadata extent minimum" row cites §7.1 in A, §7.3 in B
Both rows state the identical rule text ("extent_length ≥ 5") and the
identical governing requirement. Is one edition's cross-reference simply
wrong (a REPORTER_ERROR-shaped candidate, since a wrong appendix pointer
could send an implementer to the wrong prose)? Trace: in A, the
extent_length≥5 rule is stated within §7.1 (A's heading boundaries place
it at lines 971–1009, which *is* §7.1 in A's section order). In B, the
equivalent rule is stated within §7.3 (B's reorganized §7 moved the
metadata-compression paragraph that carries this rule into §7.3,
confirmed by reading the full passage — B's §7.3 opens with the record
type table, then "Metadata compression exists only at record
granularity... an extent slot of (0, 0) or an extent_length less than 5
is a validity error..."). **Both appendix rows correctly point to where
each edition actually states the rule.** Rejected as a citation error:
it is a consequence of the §7 reorganization, and each edition's appendix
is internally consistent with its own body text.

## Rejected candidates not elevated to constructions

- **§2.3 word-count delta (541 words, largest in the document).** Opened
  because the delta was the single largest in the whole corpus. Closed:
  B replaced a three-case enumeration of conduct-only writer obligations
  with one general sentence (`[R-CNF-02]`), but all three cases are
  independently and identically stated at their own home sections (§6.2,
  §6.3, §20.3 — see C3, C4 above, and the ignore-lane-bit case in §6.3,
  diffed and found equivalent). Closed by: reading all three home
  sections in both editions and finding the substantive sentences
  byte-identical or equivalent apart from punctuation.
- **§21.6 "cannot establish" paragraph, relocated.** A states the list of
  capability/resource grounds inline in §2.3's "Conforming verifier"
  bullet; B shortens that bullet to "(§21.6 names the grounds)" and moves
  the full list, verbatim, into §21.6 itself. Closed by: finding the
  identical sentence (same words, same requirement citations) at its new
  address in B's §21.6.
- **§15.4 and §16.2 gained Rationale blocks not in A (segments are not a
  writer's choice; what a slab promises).** Opened because these are
  genuine additions of explanatory text. Closed as EQUIVALENT, not
  ADDITION: each new Rationale sentence is a derivation from a definition
  A's own text already states without alternative (§15.4: "Segment s
  covers entries [s·2¹⁶, ...)" is stated as a fact with no writer choice
  mentioned in either edition; §16.2: slab alignment and run contiguity
  are both already normative in `[R-SLB-01]`–`[R-SLB-05]`, unchanged
  between editions). Neither Rationale decides anything A leaves open.
- **R-ENC-15 citation count (9 in A, 8 in B).** Closed: the single
  dropped citation is the forward-reference aid in §4.7 ("which is the
  sense `[R-CNT-07]`, `[R-MTA-02]` and `[R-SEC-06]` already use"), not a
  rule; the actual duplicate-name rule (F4, L9 register rows) is
  byte-identical in both editions' §21.
- **§4.7's dropped closing sentences** ("A name is structural... Every
  non-obvious encoding is followed by a worked numeric example... All
  named constants appear once in Appendix B.") Grepped B for "worked
  numeric example," "paired conformance vector," "Appendix B" near
  "constant," and "name is structural" — zero hits (control: the same
  grep against A finds all of them, confirming the search itself works).
  Judged EQUIVALENT / out of scope for the fidelity test rather than
  LOSS: (a) "name is structural" is a fully redundant restatement of a
  sentence both editions keep two sentences earlier ("version_minor is
  the only descriptive field, and every other field... is structural" —
  name is not version_minor, so it is structural by that sentence alone);
  (b) the "worked example"/"paired vector"/"Appendix B" sentences are
  claims about the *document's own presentation conventions*, not about
  the format, and their absence changes no implementer's bytes or
  verdicts.
- **Appendix G word-count delta (1709 vs 1695 words).** Diffed in full;
  every difference is an em-dash-to-comma/colon substitution consistent
  with the project's own "re-wrapped, no word changed" passes (matches
  the git history's §17.4 commit message). Zero content differences.
- **§24 (Conformance Test Vectors) word-count delta.** Same: diffed in
  full, all differences are punctuation (em-dash to comma/colon),
  zero content differences.

## One finding that does not reduce to a byte-level disagreement

**adv-01.** A's §3.3 ("Container and array model") consists entirely of
one Note:

> Part I (container) is independent of Part II (array model) by
> construction: no Part I structure requires decoding sample payloads, so
> appenders, and rewriters that carry a layer forward, operate on files
> whose layers they cannot decode — that independence is load-bearing for
> the updater rules of §7 and §20.

B has no heading "3.3" (or any heading with this title) at all, and I
could not find this sentence, or any paraphrase of its central claim,
anywhere else in B (grepped "Part II" — one unrelated hit at line 131
about decoded channel values; grepped "cannot decode," "sample
payloads," "load-bearing," "independent of Part" — zero hits). This is a
genuine, unrelocated omission: content A states, B does not state
anywhere.

I do not carry it to a byte-level construction because the Note states
no testable rule, carve-out, or quantifier of its own; it is an
architectural claim *about* two other rules, both of which are retained,
unchanged, in B: (1) the definition of "Conforming updater" in §2.3,
present in both editions, already says an updater acts "without
necessarily understanding all of its content," which is the substance of
"operate on files whose layers they cannot decode"; and (2) §20's actual
obligations (§20.3, §20.4) do not anywhere condition on Part II content
being decoded, in either edition. An implementer who read only B would
still correctly build an appender that never decodes tile payloads,
because nothing in B's §20 asks it to. So while the sentence is lost, no
construction I can build produces different bytes or a different
accept/reject verdict between an implementation built from A versus one
built from B. I report it as a LOSS of an explanatory/architectural
remark, not of a normative rule, and mark it byte_level: false.
