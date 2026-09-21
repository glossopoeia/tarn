# Register hunter — cleanroom round 36 — transcript

## Setup and access discipline

I created my scratch directory at
`/private/tmp/claude-501/-Users-robertkleffner-Documents-GitHub-tarn-first-draft/r36-round/scratch/register/`
before doing anything else. It was empty when I created it — no prior attempt's files were
present, so there is nothing to disclose there.

I read exactly one file for the substance of this audit:
`/Users/robertkleffner/Documents/GitHub/tarn-first-draft/spec/tarn.md`, in full (via several
`Read` calls covering every line, 1–4981), plus targeted `grep`/`rg`-style greps against that
same file for cross-reference sweeps. I did not open `AGENTS.md`, any ADR, `PLAN.md`,
`OPEN-QUESTIONS.md`, `spec/registry.json`, `conformance/`, or any git history. I did not list
any directory other than my own scratch directory, and I did not read the shared output
directory that other agents are writing to.

**Context I did not ask for.** Before my first turn, the harness placed a project-instruction
pointer (`CLAUDE.md` → "See AGENTS.md") and a list of the user's auto-memory note titles
(`MEMORY.md`, titles only — e.g. "TARN harness spec path", "TARN repair prose vs rules", "TARN
class lines are undertakings") into my context, along with git-status/log lines showing recent
commit subjects for this repository. I did not open `AGENTS.md` or any memory note body, and I
did not treat any of this material as evidence about the specification's content. Two of the
memory titles ("TARN repair list vs diff", "TARN closed-list exceptions compose") are suggestive
of exactly the kind of check my charter already asks for, but I did not use them to decide where
a defect *is* — only ordinary charter-driven suspicion generation, immediately checked against
the document itself. The git-log commit subjects shown to me (e.g. "Cleanroom round 36: charter,
re-cut over the scoped second audit") are consistent with the round narrative in my brief but I
did not read the diffs they name and did not use them as evidence either. I'm disclosing this
per the brief's instruction; I did not act on any of it.

The one file was exactly where the brief said it would be; no path substitution was needed.

I ran only local, no-file-access computation: Python one-liners/scripts for arithmetic and for
mechanically recounting the register's own tables, and greps against `tarn.md`. One script
(`recount_instances.py`, saved under my scratch directory) is disclosed below with its output.

## Charter

Audit §21 (the error-handling register, §21.1–§21.9) against the rules it restates and against
itself: row-vs-rule agreement, completeness in both directions, every cross-reference to a
register row from elsewhere in the document, the counting (conditions and instances), the
outcome vocabulary, and the limits material.

## Reading §21 itself first (§21.1's own governing rules)

I read §21.1 (lines 3735–3832) closely, since it states the register's own arithmetic and
scope before I hold the rest of §21 to it. Key rules I extracted and later checked every row
against:

- The register is exactly §21.2–§21.5. Completeness is normative for it: every detectable
  file-conformance violation must have a row, and only detectable ones need one (§21.7 states
  the detectability test).
- Each row *restates* its governing rule; where they diverge, the rule governs. Governing-rule
  cells' *parenthetical* citations are explicitly declared "a finding aid and not the whole of
  them" — i.e. non-exhaustive by the document's own admission. This mattered later (see
  "Rejected candidates").
- Specialization: where every file exhibiting row A's condition necessarily exhibits row B's,
  the file is recorded against the narrower row A. The document names six such pairs: F1's
  front-block instance of F6, F1's trailer-magic instance of F8, F35 of F36, L24 of L25, F21 of
  F22, L10 of L11 — and says the list "is not offered as closed."
- The Instances column's counting convention: separated by semicolons; "—" is one instance; a
  layout-varying quantity is enumerated per layout (materially different shapes); a
  not-equal/differs-from comparison is enumerated in both directions, a one-directional bound
  (exceeds/larger than) is not; a nonzero-value test or a checksum/constant equality test is not
  a "magnitude comparison" and is not doubled.
- Detector *verifier* rows still carry the outcome that names *the scope at which the damage is
  recorded*, not an obligation on any reader — several such rows in fact oblige a reader to
  serve the flawed structure through unchanged (R-CNT-22's F28/L49, R-MTA-05's F27/L48,
  R-CNT-12's reserved-flag rows F26/L47). R-SER-08 is called out as "the one rule that goes the
  other way," resolving a byte to a returned value rather than serving it through, and
  R-CNT-12's MU=1/PE=0-read-as-PE=1 (F25/L46) resolves a flag.

I verified every one of these claims against the rest of the document (below) rather than
taking them on faith, since §21.1 is itself part of the "freshest text" this round names.

## Row-versus-rule agreement

I read every section §2–§20, §22–§24 that a §21 row's Governing rule cell cites (primary or
parenthetical), end to end, and checked each row's condition, instances, detector, detection
point, and outcome against the current text of that rule. This is the bulk of the work; I do
not reproduce every match here, only what is worth recording.

Everything I checked agreed, including subtle cases I expected to trip on:

- **F30/F31/F32 vs L15/L16/L17 vs F3/L2, and R-CNT-13's disjunction.** R-CNT-13's extent-slot
  rule (§7.2) is a disjunction of four conditions: either-half-zero, offset in [1,16), extent
  past F−64, and an overflowing offset+length sum. §21.1's own note explains that a slot of
  (0, N) with N≠0 is *not* F31's "offset 1–15" case — it belongs to F30 (half-zero) because
  offset=0 is caught there first. I checked this is mathematically exact: F30's condition
  (exactly one half zero) and F31's ("nonzero extent slot" with offset in 1–15) are disjoint by
  construction, and F32 (extent past F−64) and F3 (overflowing sum) round out the remaining two
  disjuncts. Same pattern for L15/L16/L17/L2 at layer scope. No gap, no double-count.
- **F21 of F22, L10 of L11 (specialization).** F21/L10's condition is extent slot exactly
  (0, 0); F22/L11's is extent_length < 5. Since (0,0) implies extent_length = 0 < 5, F21 ⊆ F22
  and L10 ⊆ L11 exactly as claimed — I checked the arithmetic, not just the prose.
- **F35 of F36, L24 of L25 (specialization).** F35/L24 (reserved-range type + MU=1, reader-
  detected) is a proper subset of F36/L25 (reserved-range type regardless of MU, verifier-
  detected). Checked against R-CNT-15/R-CNT-18's text; holds.
- **T6/T7/T8/T9/T10/T11/T12 vs §15.3's entry-state table.** §15.3 states seven "structural"
  entry-outcome rows (sentinel-mismatch three ways, length=0, offset<16, domain overflow,
  offset+length overflow-or-past-F−64) plus "stored bytes fail crc" (non-structural), plus two
  *verifier* rows (overlap, alignment/slab). I matched every one of the nine reader-facing rows
  to T1/T6/T7/T8/T9/T10/T11/T12 one-to-one (T9 and T12 are the two sub-cases of the last
  structural row — arithmetic overflow vs. the F−64 bound — correctly split into two rows since
  they are separately triggerable), and the two verifier rows to L18 (overlap) and
  L40/L41/L42 (alignment/slab). No gap.
- **R4's sixteen instances vs §18.2's carried-over zstd frame constraints for user metadata.**
  §18.2 explicitly carries over the frame magic, no-skippable/no-second-frame, no (disclosed)
  dictionary ID, no content-checksum flag, and the content-size-must-equal-decoded-length rule,
  and explicitly *excludes* the tile-specific decoded-size and Window_Size constraints
  (replacing them with the reader's-own-capability treatment, which is not a violation and
  correctly does *not* appear in R4). I enumerated R4's 16 instances (8 conditions × top-level/
  sub-record) and matched every one to this list, and confirmed the two named exclusions
  (undisclosed dictionary use; the buffer-sizing bar) are correctly *absent* from R4, per
  §18.2's own explanation of why they fall outside the register on two different grounds
  (unwitnessed vs. binds-a-reader-not-a-document).
- **T13/T15/T16/T18/T23's self-referential "detected by" language.** Several tile rows say
  their own condition has no detection procedure of its own and is caught by T24 or T25
  instead. I checked this claim is actually true given the codec definitions in §17.2 (a
  cross-tile dependency, a wrapper format, a second stream, an LZ4 frame instead of a block all
  either fail to decode as the declared codec or leave trailing bytes) rather than just
  accepting the row's self-description.
- **T2 and T4 "the two rows together covering R-SER-08."** T2 covers real (non-padding)
  positions; T4 (governed by R-SER-05, padding content generally) covers padding positions
  including the interleaved-bool-fill-byte instance. I checked whether T4's "does not encode
  fill value" condition really subsumes every R-SER-08 violation at a padding position: since
  fill for a bool channel is itself constrained to {0x00, 0x01} (L35/R-TYP-07), any byte at a
  padding position that is neither 0x00 nor 0x01 automatically differs from fill, so it's always
  inside T4's condition too. The claim holds (T4's condition is a proper superset there, which
  is consistent with T4 being the row of record under the specialization principle even though
  T4's own Governing-rule cell cites only R-SER-05).
- **§20.3's fixed-declaration bar and its witnessed exceptions.** The Note/rationale under
  §11.1 and the long paragraph in §20.3 step 4 both list which register rows are the *only*
  witnesses that could catch a commit that silently changed a layer's fixed declarations
  (decoded-size/padding/pad-bit/bool-byte rows T3, T14, T21, T22, T4, T5, T2, and framing/decode
  rows T17, T24, T25 for a changed codec/filter). I checked each cited row is in fact about one
  of those two families (size-vs-declaration, or framing/decode-failure) and that the omitted
  wrapper-detection rows (T15, T16, T23) are correctly omitted since their own text says their
  detection is *via* T24/T25 rather than an independent procedure — so citing T17 (zstd's magic
  check, which is a genuine independent framing check) but not T15/T16/T23 is deliberate, not an
  oversight.
- **§10.2's eight numeric-identifier spaces vs. the seven-plus-one reserved-range rows named at
  line 3616–3618** (record type F36/L25, and "one row for each of the other seven": index
  encoding L31, linearization L33, sample type L34, codec L43, filter L45, channel layout L36,
  metadata encoding R1). I checked each of the eight spaces in §10.2's table against exactly one
  cited row and found the correspondence exact, including that L36 ("layout... 0 or reserved
  3–255") is the *channel layout* space (§14.1), not a different field.

## Completeness sweep

**Direction 1 — is every detectable violation registered?** I read §21.7's detectability test
closely (a condition is detectable iff some file exhibiting it is separated from every file that
doesn't by some check this specification obliges a reader or verifier to perform) and walked
every normative MUST/MUST NOT in §4–§20, §22–§24 asking whether it states a file-exhibitable
condition, and if so whether it has a row. I did not find one that lacked a row. Two checks
worth naming specifically since the brief calls out exactly this kind of gap:

- **The unlabelled blockquote.** The brief warns that at least one blockquote in this document
  carries no *Note*/*Example*/*Rationale* label and is therefore normative under R-CNF-01's own
  wording (the exemption is by label, not by the `>` marker). I swept the whole document
  programmatically for blockquote runs whose first line is not `> **Note`/`> **Example`/
  `> **Rationale`, and found exactly one: line 2206, the physical-layout diagram of the tile-
  index region in §15.1 (`[ entry array: entry_count × 20 bytes ] [ segment CRC array: ... ]`).
  This is indeed unlabelled and normative — but it states only the *layout* that L22's formula
  already tests in full (extent_length must equal entry_count×20 + ⌈entry_count/2¹⁶⌉×4); any
  padding or reordering that violated the diagram would already fail L22's arithmetic. I found
  no additional, separately-registrable condition hiding in it.
- **§10.1's four extension vehicles vs. the register.** New record types (§7.3) — covered by
  F24/F34/F35/F36/L13/L19/L24/L25/L26. New reserved-range values (§10.2) — covered as tabulated
  above. New ignore-lane flag bits (§6.3) — explicitly a defined non-violation (§21.6, R-CNT-08).
  New standardized user-metadata keys (§18.4) — explicitly a defined non-violation (§21.6,
  R-MTA-06/R-MTA-07). All four vehicles are accounted for.

**Direction 2 — does every row register an actual violation?** I checked this by confirming
every row's governing rule text actually states a MUST/MUST NOT (or "is a validity error")
matching the row's condition, rather than a SHOULD or a non-normative gloss. All 120 rows
passed. I also specifically re-checked the two rows that moved out of §21.6 into the register in
recent history per the document's own note at lines 4041–4053 (F27/L48 unsorted user-metadata
members, and F28/L49 registered-type flag mismatches) — both are correctly still present as
violations, both correctly carry detector *verifier*, and the document's own explanatory note
about why they belong in the register (they make the file nonconforming while leaving reader
behavior unchanged) matches R-MTA-05's and R-CNT-22's text exactly.

## Cross-references to register rows from elsewhere in the document

I grepped the whole document for tokens matching `F\d+`, `L\d+`, `T\d+`, `R\d+` and manually
inspected every hit outside §21 itself (lines 234, 260, 285–292, 623, 738, 838, 998, 1473, 2481,
2690, 2705, 2723, 2725, 2826, 2929, 3316, 3318, 3346, 3616–3618, 4695–4697, 4965–4968, 4977 — 28
distinct citing spots). Every one resolves to a row that actually says what the citing text
claims:

- §2.3's Note (285–292): F14 reaches every format major, F5 and F15 do not — checked against
  R-CNT-24's four fixed invariants; correct in both directions.
- §21.2's own opening paragraph (3836–3842): "F8, F14, F6 and both of F1's instances... and no
  other row" reach every major. I independently derived this from R-CNT-24's four fixed
  invariants (trailer magic, version-field position, trailer CRC scope, front-block constancy)
  and got the same four rows (F1 counted once, both its instances narrow F6 and F8
  respectively). F18 is correctly excluded (its own text explains why: version_major=0 declares
  no major at all, so the "declares a major other than 1" premise is unmet — it isn't an
  exception, the reach question doesn't arise for it).
- §4.7's Note (623): "a duplicate is a validity error at file or layer scope (F4, L9)" — F4 is
  the file-scope (layer name) duplicate, L9 the layer-scope (dimension/channel name) duplicate.
  Correct pairing.
- §9.6 (1473): "F8, F14 and F17 — the magic, the trailer CRC and the length cross-check" —
  matches exactly.
- §17.2's Note (2481): T24 for "a whole byte after the final DEFLATE bit trails the stream" —
  T24 is exactly the general trailing-bytes rule. Correct.
- §18.2 (2690, 2705, 2723, 2725, 2826): R3/R4/R1 routing — checked above under R4.
- §20.3 step 4 (3316, 3318, 3346): the witnessed-exceptions lists (T3/T14/T21/T22/T4/T5/T2, and
  T17/T24/T25) and L44's lz4 cap citation — checked above.
- §20.5 (3616–3618): the eight-numeric-space accounting — checked above.
- Appendix F (4695, 4697): T15 cited for the RFC 1950/1952 wrapper rows codec 2 excludes —
  matches T15's condition exactly.
- Appendix H (4965, 4967–4968, 4977): F1/F6 (front block, verifier always checks), F7 (pre-
  trailer gap), F36/L25 (reserved-range type), R1 (encoding 0/reserved) — all match their rows.

I found no citation that points at the wrong row or mischaracterizes what a row says.

## The counting

I recounted §21.2–§21.5's conditions and instances by hand against §21.1's own stated
arithmetic (see rules extracted above), then re-verified mechanically with a script
(`recount_instances.py`, saved to my scratch directory; reproduced in full below) that parses
the four register tables directly out of `tarn.md` and applies the same convention
(semicolon-separated, "—" = 1).

```python
import re

with open('/Users/robertkleffner/Documents/GitHub/tarn-first-draft/spec/tarn.md', encoding='utf-8') as f:
    lines = f.readlines()

sections = {
    'F (21.2 file-scope)': (3846, 3880),
    'L (21.3 layer-scope)': (3895, 3943),
    'T (21.4 tile-scope)': (3955, 3980),
    'R (21.5 ignored records)': (4005, 4014),
}

total_all = 0
for name, (start, end) in sections.items():
    total = 0
    count = 0
    for ln in range(start, end+1):
        line = lines[ln-1]
        if not line.startswith('|'):
            continue
        cols = line.split('|')
        if len(cols) < 4:
            continue
        rowid = cols[1].strip()
        instances = cols[3].strip()
        if rowid in ('#', '---') or set(rowid) == {'-'}:
            continue
        n = 1 if instances in ('—', '-') else instances.count(';') + 1
        total += n
        count += 1
    print(f'{name}: rows={count} instances={total}')
    total_all += total

print('grand total instances =', total_all)
```

Output:

```
F (21.2 file-scope): rows=35 instances=56
L (21.3 layer-scope): rows=49 instances=116
T (21.4 tile-scope): rows=26 instances=55
R (21.5 ignored records): rows=10 instances=50
grand total instances = 277
```

Per-subsection condition counts match the stated totals exactly: §21.2 states "35 conditions"
(I count F1–F36 minus the struck F11 = 35); §21.3 "49 conditions" (L1–L49, none struck); §21.4
"26 conditions" (T1–T26); §21.5 "10 conditions" (R1–R10). Total 120 conditions matches §21.8's
"120 conditions over 277 instances," and my instance total (277) matches exactly, both by hand
and by script, using §21.1's own stated convention (layout-varying quantities enumerated per
layout; not-equal/differs-from comparisons doubled for direction; one-directional bounds,
nonzero-value tests, and equality-against-a-constant/checksum tests not doubled). I spot-checked
roughly forty individual cells against this convention (documented inline above and in my
row-by-row pass) and found every one applied consistently — including the subtle cases (L20,
L27, L28, T6 as nonzero-value tests correctly counted as 1; T21 as a one-directional "larger
than" correctly counted as 1 per layout rather than 2; F17/L21/L22/T3/T22/R4's content-size
clause as not-equal comparisons correctly doubled).

I also independently derived several of the numeric examples in §21.9's Note and cross-checked
them arithmetically rather than trusting the prose:

- 2³² addressed tiles ⇒ segment CRC array = ⌈2³²/2¹⁶⌉×4 = 2¹⁶×4 = 2¹⁸ = 262,144 bytes = 256 KiB.
  Matches the Note's "still 256 KiB."
- 2³⁶ addressed tiles ⇒ ⌈2³⁶/2¹⁶⌉×4 = 2²⁰×4 = 2²² = 4,194,304 bytes = 4 MiB. Matches "reaches
  4 MiB at 2³⁶."
- §15.4's worked example (entry_count = 1,000,000): 1,000,000/65,536 = 15.26 ⇒ 15 full segments
  (983,040 entries) + one partial segment of 16,960 entries = 16 segments total, matching the
  text exactly; index region = 1,000,000×20 + 16×4 = 20,000,000 + 64 = 20,000,064 bytes, matching
  exactly; tile 999,999's position in segment 15 = (999,999 − 983,040)×20 = 16,959×20 = 339,180,
  matching exactly; segment 15's byte range [19,660,800, 20,000,000) (983,040×20 = 19,660,800),
  matching exactly; full-segment size 65,536×20 = 1,310,720 bytes = 1.25 MiB exactly, matching
  "1.25 MiB."
- 0x7E000000 (codec 4's per-tile decoded-size cap, L44/R-COD-07) = 2,113,929,216 bytes ≈ 1.97 GiB,
  comfortably above the 256 MiB minimum-guarantee row, so the two limits don't conflict (a
  reader's guaranteed floor for tile size is well under lz4's hard ceiling).

I found no arithmetic error anywhere I checked, and no discrepancy between any stated total and
my recount.

## Outcome vocabulary

§21.2/§21.3/§21.4/§21.5's section headers each declare one outcome (reject-file/reject-layer/
reject-tile/ignore-record respectively) and every row within a section carries that section's
declared outcome uniformly — including the verifier-detected rows (T2/T4/T5/T26 are still
reject-tile in outcome even though no ordinary reader is obliged to act; F27/F28/L46-L49 are
still reject-file/reject-layer in outcome for the same reason). §21.1 explicitly and correctly
flags that a verifier-detected row's "outcome" names the scope of nonconformance rather than an
action any reader takes — I checked this against R-CNT-22, R-MTA-05, and R-CNT-12's actual text
and it holds precisely (§2.4's outcome-class table's own wording, "the file is nonconforming...
readers process the document unchanged," matches).

`preserve-verbatim` — the fifth outcome value defined in §2.4 — is correctly *never* used as a
register-row outcome (§2.4 itself states it is "orthogonal to reader outcomes," an updater
obligation, not a violation outcome), and it is reachable in practice via §20.4's table (its
MU=1 and MU=0/PE=1 rows). All five outcome values are therefore both correctly scoped and
reachable.

## Limits

I cross-checked every entry in §21.9's minimum-guarantees table and hard-limits paragraph
against the section that defines the underlying quantity, in both directions (a limit stated
elsewhere and missing from §21.9; a limit in §21.9 stated differently from its defining
section):

- rank ≤ 255, channel count ≤ 65,535 — matches §7.4's u8/u16 field widths exactly.
- alignment A: power of two, 512 ≤ A ≤ 2⁶² — matches §16.1/R-SLB-01 and §7.4's field table
  exactly (word for word: "a power of two with 512 ≤ A ≤ 2⁶²").
- slab alignment A_slab: power of two, 1 ≤ A_slab ≤ 2⁶² — matches §16.2/§7.4 exactly.
- slab run length S: 1 ≤ S ≤ 2⁶³ − 1 — matches §7.4's field table exactly.
- codec 4 per-tile decoded-size cap 0x7E000000, largest channel plane governing in a planar
  layer — matches R-COD-07 word for word.
- every offset/length/extent/count ≤ 2⁶³ − 1 — matches R-ENC-03 exactly.
- name/key ≤ 255 bytes — matches §4.6 (u8 length prefix) and §18.2's folding of §4.6 onto keys.
- directory ≥ 4 bytes at offset ≥ 16; file ≥ 128 bytes — matches §6.2/R-CNT-06 and §5.1/
  R-CNT-27 exactly.
- the eight minimum-guarantee rows (rank 32, channels 4096, entry_count 2³², layers 65,536,
  dir_length 16 MiB, tile decoded size 256 MiB, user-metadata document 16 MiB, zstd
  `Window_Size` 8 MiB) are each cross-referenced from their using section (§17.2/R-COD-06 and
  §18.2 both cite the same 8 MiB Window_Size guarantee; §18.2 cites the same 16 MiB document
  guarantee) with no numeric mismatch anywhere I found.

I found no limit stated in §21.9 that conflicts with its defining section, and no limit stated
elsewhere in the document that §21.9 omits (the only two "limit-shaped" statements I could find
outside §21.9 that are not restated there — the 2⁶³−64 ceiling on committed_file_length derived
in a §9.3 Note, and the informal "workable range... 1 to 16 MiB of decoded tile" in §11.3's Note
— are both explicitly non-normative/advisory in their own text, not hard or minimum-guarantee
limits, so their absence from §21.9 is correct rather than a gap).

## Rejected candidates

I opened and closed several suspicions that did not survive scrutiny; recording them since a
clean lane should show it looked:

1. **L2 does not parenthetically cite R-CNT-17**, even though one of its named instances
   ("entry_count × 20 + ⌈entry_count/2¹⁶⌉ × 4") is the exact formula R-CNT-17 designates as a
   declaration-derived quantity in §7.4. I initially flagged this as a missing citation. Closed:
   §21.1 explicitly states that a Governing-rule cell's parenthetical citations are "a finding
   aid and not the whole of them" — i.e. declared non-exhaustive by the document's own text — so
   an omitted secondary citation is not itself a defect. (L22, which registers the *value* of
   this same formula, does correctly cite R-CNT-17 as its primary governing rule.)
2. **T4's governing-rule cell cites only R-SER-05**, not R-SER-08, even though T2's condition
   text says "the two rows together cover R-SER-08." I checked whether this makes T2's claim
   false. Closed: it doesn't — every padding-position byte that violates R-SER-08 (∉{0x00,0x01})
   also violates T4's broader "≠ fill" condition, since fill is itself constrained to {0x00,
   0x01} (L35/R-TYP-07), so T4 does fully subsume the padding-position half of R-SER-08 even
   though its own Governing-rule cell doesn't name R-SER-08 (same non-exhaustive-citation
   principle as above).
3. **L1's condition text says "a u64... field of a layer record"** but its own Instances column
   includes "sub-record extent_offset; sub-record extent_length" — fields of a nested
   sub-record, not the layer record's own inline payload. I considered flagging this as a scope/
   quantifier mismatch (shape #1). Closed as not byte-level and not worth filing: the Instances
   column's own explicit enumeration removes any real ambiguity about what the row covers, the
   row's Detector/Detected (reader/layer access) and outcome (reject-layer) are unambiguous and
   correct for both kinds of field, and no two implementations could disagree about which bytes
   this row reaches or what happens to them — it reads as loose shorthand ("of a layer["'s
   structures]") rather than a genuine fork.
4. **The unlabelled blockquote at line 2206** (§15.1's tile-index-region diagram) — checked
   above under "Completeness sweep." Confirmed genuinely unlabelled and normative, but it
   introduces no separately-registrable condition beyond what L22 already tests in full.
5. **Whether §21.2's "F8, F14, F6 and both of F1's instances... and no other row" omits a
   distinct row for the version-field *position*** (R-CNT-24 also fixes that version_major/
   version_minor sit at F−56 in every major). Closed: this is not an exhibitable condition under
   §21.7's own test — the position is fixed by how the format is parsed, not by anything a
   corrupt file could independently vary, so no row is owed for it (matches R-ERR-01's
   fixed-field-width principle).

## Conclusion

Every row I checked restates its governing rule correctly; the register's own completeness,
specialization, and instance-counting claims about itself all check out on independent
recount; every cross-reference into the register from elsewhere in the document resolves to the
row it claims to; the outcome vocabulary is used consistently and every value is reachable; and
the limits material agrees with every other statement of a limit in the document, in both
directions, everywhere I could check it. I did not find a confirmed defect within my charter.
