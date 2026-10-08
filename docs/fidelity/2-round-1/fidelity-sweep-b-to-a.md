# Sweep transcript: B → A completeness (addition check)

Role: completeness sweeper, reading from edition B (`spec/tarn.md`) into
edition A (`scratch/cleanroom/editions/a/tarn.md`). Question asked of every
item B decides: does edition A say this too (anywhere), or has B decided
something A leaves open / never draws?

Scratch dir: `/private/tmp/claude-501/-Users-robertkleffner-Documents-GitHub-tarn-first-draft/fidelity-3/scratch/sweep-b-to-a/`
Working files written there:
- `a/s1.md` … `a/s24.md`, `a/sapp.md` — edition A split by section, by line
  range taken from a heading grep of A.
- `b/s1.md` … `b/s24.md`, `b/sapp.md` — edition B split the same way. §2 and
  §3 were re-extracted by hand after discovering B physically orders them
  3-then-2 while keeping their canonical numbers (see §3 note below).

## Method

1. Grepped both files for `^### ` / `^## ` headings to get line ranges per
   section, confirmed both editions share the same 24-section + 8-appendix
   numbering.
2. `diff -q` every section pair to find which sections differ at all.
   Result: §1–§8 differ (these are the sections the "Readable:" commits have
   touched so far, per `git log`); §12, §18, §21, §22, §23 and the appendices
   differ by a few lines each (cross-reference renumbering); §9, §10, §11,
   §13, §14, §15, §16, §17, §19, §20, §24 are byte-identical to A — not yet
   rewritten, so no addition risk there at all.
3. For every section that differs, read A and B side by side (`diff` on
   `fold -w 100` text so hard-wrap doesn't produce spurious line diffs).
4. For every hunk, asked: is the content in B present anywhere in A (same
   section or moved to another), or is it new? Verified every suspect
   "pure addition" hunk (diff hunks of the form `NNaNN,NN`, i.e. lines only
   on the B side) by grepping A for a short, distinctive fragment of the
   added text — never trusting the hunk shape alone, since reordering within
   a section produces the same `a`-hunk shape as a real insertion.

## Section-by-section notes

**§1 Introduction.** B is shorter throughout (drops A's "four questions"
framing, the exact "two range requests" figure in favor of "a small fixed
number", several cross-refs). Everything B states is a subset of what A
states; the four extension vehicles B names explicitly in §1 prose
("new record types, new enum values in reserved ranges, new ignore-lane flag
bits, and new standardized user-metadata keys") are also in A, both in §1's
own list (A lines 500–502: "four vehicles: new record types (§7), new enum
values in ranges this specification reserves, new ignore-lane flag bits
(§6), and new standardized user-metadata keys (§18)") and spelled out again
in A §10 (lines 1572–1573). No addition.

**§2 Conformance.** Checked by splitting B correctly — B's physical file
order is §1, §3, §2, §4 (Terminology appears before Conformance in the
file, confirmed at B lines 16/60/146/342), but each section keeps its
canonical number, so B's "§2" is still "Conformance" and corresponds to A's
§2. This reordering changes nothing about content; re-extracted the correct
line ranges (`b/s2.md` = B lines 146–341, `b/s3.md` = B lines 60–145) before
comparing. Control search confirms the swap is cosmetic: grepped B for
"declares no major at all" (a condition from A's §2.3 that B's abbreviated
§2.3 omits) and found it relocated to B's §21 (line 3697, and register row
F18 at line 3718) rather than dropped. Every bullet and paragraph B states
in §2 is a shortened version of a corresponding A passage; three Note
blocks A carries (the F14/F5/F15 reach-test note; the bit-numbering note in
§4; the "Reject prescribes scope not UI" note) are absent from B, but that
is A having more than B, not the reverse, and so outside this sweep's
question. No addition found in §2.

**§3 Terminology.** B's term list reorders four entries (front signature
block, generation, trailer, directory) to the front of the list; same
definitions appear later in A's list (A lines 46–60). B's "fill value" entry
drops the word "per-channel" ("the value that a channel's samples take...")
relative to A's "the per-channel value that a channel's samples take...";
the channel-scoping is unchanged since both sentences still key the value to
"a channel's samples", so this is wording, not a scope change. B's "tile"
entry adds an explicit defined verb, "a tile *carries* a channel when its
payload holds that channel's samples at the cell's positions" — searched A
for this usage pattern and found "tile carrying that channel" / "tile
carries" used pervasively already (A lines 380, 390, 419, 422, 1780, 1950,
2009, 2013, 2166, 2316, 3958, 4025); B is naming a usage A already relies on
throughout, not deciding something new. B also drops A's §3.3 Note on
Part I/Part II independence entirely (a loss in the other direction, not
examined further here). No addition found in §3.

**§4 Encoding Conventions.** B's "three exceptions" framing for integer
widths states the same three fields A lists (inline_length u32; name length
prefix u8; fill length prefix u8). B's rule on declaration-derived sums
("Some quantities are not stored but computed...") restates A's list of the
same five quantity kinds (offset+length, grid count, tile count,
sample-position count, ordinal) without adding a sixth. B's checksum
paragraph in §4.5 is a condensed version of A's — same three exceptions
(front block, terminal fields, unassigned-record extent), same "interior
checksum fields... covered by exactly one further checksum" clause. No
addition found in §4.

**§5 File Anatomy and Byte Coverage.** Both editions state the same claims
about which regions a commit appends, slack, coverage of the live committed
state, and the verifier's slack-total obligation (full total / partial
total / no total at all, and when each applies). B restructures the
slack-total paragraph into shorter paragraphs but the content (walk
completeness, what counts as complete, partial-total bound, which scope
stopped the walk) is unchanged. No addition found in §5.

**§6 Front Signature Block and Trailer.** Local/remote reader and residency
definitions match (B states "residency" as its own clause rather than
folding it into the local/remote distinction, but defines it identically).
Pre-trailer pad, version-gate ordering, flags rule (incompat/ignore lane,
writer-under-this-text writes flags=0, updater copy-forward of unknown
ignore-lane bits), version_minor SHOULD rule, and the two-request remote
open protocol (suffix fetch of final 64 bytes / dir fetch) all match
clause-for-clause once reworded into shorter sentences. Checked specifically
whether B's explicit "An appender SHOULD emit the maximum..." (written as
its own sentence) adds a new SHOULD-level obligation beyond A's elliptical
"...and an appender the maximum of that floor and the prior trailer's
minor" (same sentence, verb elided) — same obligation, no addition. No
addition found in §6.

**§7 Metadata Directory and Records.** B relocates the "Metadata compression
exists only at record granularity... User metadata is quarantined..."
passage from early in §7 (where A states it, A lines 13–40) down next to
§7.4 (B lines 944–968); confirmed by direct comparison that the moved text
preserves every clause (extent-length-≥-5 rule, encoding values 0/1/2,
quarantine scope, the `[R-MTA-05]`/F27/L48 carve-out, the resource-decline
exception). Extent-slot, overlap, multiplicity, and unknown-record-type
rules all match A once de-compressed back to full sentences. No addition
found in §7.

**§8 Integrity.** B's checksum-coverage-map paragraph spells out the three
exceptions as separate sentences instead of a parenthetical list; same three
exceptions, same "interior checksum fields... covered by exactly one further
checksum" clause, same five-link chain-of-trust list and outcome mapping.
No addition found in §8.

**§9–§11, §13–§17, §19–§20, §24.** `diff -q` shows these are byte-identical
between the two files; not yet touched by the readable rewrite. Zero
addition risk — nothing to sweep.

**§12 Channels and Sample Types.** One-line rewording only: "order is
load-bearing (§3.1, §11.4)" → "order fixes each channel's index (§3.1,
§11.4)" — same claim (the declared channel order determines each channel's
index), restated. No addition.

**§18 User Metadata.** One-line cross-reference fix only: "(§7.1)" →
"(§7.3)", tracking the §7 passage's move described above. No addition.

**§21 Error-Handling Register and Limits.** The only non-trivial diff is a
paragraph on when a verifier reports *cannot establish* (format major not
implemented; MU=1 unknown type; can't execute codec/filter; resource
decline on layer/tile decode; declines to decode user-metadata document).
Grepped A and found this exact list already stated in A §2.3's "Conforming
verifier" bullet (A lines 126–140, same five grounds, same citations
`[R-COD-11]`, `[R-ERR-04]`, `[R-SER-05]`, `[R-SER-08]`, `[R-MTA-09]`). B's
§2.3 now just says "(§21.6 names the grounds)" and the detail moved here.
Relocation, not addition.

**§22 Security Considerations, §23 Privacy Considerations.** Each has one
cross-reference fix only ("(§7.1)" → "(§7.3)"), same move as §18's. No
addition.

**Appendices.** One line differs: the limits table's "User-metadata extent
minimum" row cites "§7.1" in A and "§7.3" in B — the same cross-reference
fix, tracking the real relocation of the extent-length-≥-5 rule. No
addition.

## Control searches (proving the zeros)

- Confirmed grep works on these hard-wrapped files by first searching a
  phrase known present verbatim in both: `"every requirement names the
  actor it binds"` (§2.1's Note) — 1 hit in each file, same text,
  establishing the grep/line-wrap approach is not silently missing matches.
- For every "pure addition" diff hunk (3 found, in §3, §7, and §21), ran a
  distinctive-fragment grep against the *other* candidate location in A
  before concluding "moved" rather than "new": `"front signature block.*
  constant 16 bytes"` (§3, found at A's later terminology-list position),
  `"Metadata compression exists only at record granularity"` (§7, found at
  A lines 13–40), `"it cannot execute a codec or filter"` (§21, found at A's
  §2.3 verifier bullet, lines ~126–140). All three resolved to "present in A,
  relocated," not "absent from A."
- For the dropped "per-channel" word in §3's fill-value entry, grepped A for
  the same sentence's channel-scoping language to confirm no scope widening:
  both editions key the fill value to "a channel's samples," so the dropped
  adjective changes no decided boundary.

## Coverage statement

All 24 sections and all 8 appendices were read and compared (§9–§11,
§13–§17, §19–§20 and §24 needed only the `diff -q` identity check, since
they are untouched). I did not run short; every section is accounted for
above. No item was found that edition B decides and edition A does not —
every content difference traced to abbreviation, relocation within the
document, or a cross-reference renumbering that tracks a real relocation.
No LOSS, ADDITION, or CONTRADICTION findings are reported from this sweep;
the few EQUIVALENT observations above (the §2/§3 physical reordering, the
§7 paragraph move, the §2.3→§21.6 verifier-grounds move) are recorded for
the maintainer's visibility but need no fix.
