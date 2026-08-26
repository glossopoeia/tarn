# Cross-hunk consistency audit — ADR-0106 repair set (7 hunks)

## 0. Disclosure

Read: the seven files `hunk-01.diff` … `hunk-07.diff` in
`/private/tmp/.../case-adr0106/`, and `/Users/robertkleffner/Documents/GitHub/tarn/spec/tarn.md`
(sections read in full: §2.3, §2.4, §2.5, §4.1–§4.7, §5.1, §5.2, §6.1–§6.4,
§7.1–§7.4, §11.2, §11.3, §14.2, §14.3, §15.1–§15.3, §17 entire, §19.1, §19.2,
§21.1–§21.6, §21.9 fragment, Appendix G entire).
Did NOT read: `full.diff`, docs/, PLAN.md, OPEN-QUESTIONS.md, AGENTS.md,
README.md, conformance/, registry.json, git history, the web. Did not list the
case directory beyond globbing `hunk-*.diff`.

Unsolicited context that appeared before I began: a project instruction file
(CLAUDE.md → AGENTS.md pointer) and an index of the maintainer's memory notes
naming several private files. I did not open any of them and drew no conclusion
from their titles. Disclosed, not acted on.

Tools run: `sed -n` ranges over spec/tarn.md, `grep -n`, and three Python
whitespace-normalising searches over the whole file (the document is hard-wrapped,
so every phrase search below was run against `re.sub(r'[ \t]*\n[ \t]*',' ',raw)`).

## 1. Grouping (worked out from the hunk bodies, not from section numbers)

**Group A — "what does *reach* range over": hunks 1 and 6.**
Hunk 1 rewrites `[R-CNF-13]` (§2.3) so that *reach* is a property of a
**condition** (a §21.1 register row) rather than of a **requirement**.
Hunk 6 rewrites §21.2's preamble so the derivation runs "condition by
condition", and **deletes** the clause "where this restatement and that rule
diverge, the rule governs (§21.1)". These two are one repair split across two
sections: hunk 6 is the restatement of hunk 1's rule.

**Group B — "express designation under `[R-ENC-04]`": hunks 2, 3 and 4.**
Three sites where an arithmetic expression previously appeared *only inside a
comparison*, which `[R-ENC-04]` expressly excludes from the overflow duty
("an expression this specification writes only inside a comparison, and names
nowhere, is not a designated quantity and no reader is obliged to form it").
Hunk 2 designates `dir_offset + dir_length` (§6.2, `[R-CNT-06]`); hunk 3
designates `extent_offset + extent_length` (§7.2, `[R-CNT-13]`); hunk 4
designates `entry_count × 20 + ⌈entry_count/2¹⁶⌉ × 4` (§7.4, `[R-CNT-17]`).

**Group C — "what does a §17 rule range over": hunks 5 and 7.**
Hunk 5 **deletes** §17's preamble sentence "Every rule in this section ranges
over **stored** tiles…". Hunk 7 rewrites Appendix G item 5's filter argument,
whose whole subject is the range over which byte-shuffle is a no-op.

Two deletions whose effect is elsewhere: **hunk 5** (effect: `[R-COD-07]`'s
*addressed*-tile quantifier and §21.9's "exactly as `[R-COD-07]`'s cap is" now
stand unchallenged) and **hunk 6** (effect: §21.1's precedence clause is now
the only tie-break, and it does not cover subsection preambles).

## 2. What each repair makes true of an implementation

- **H1.** For a file declaring a major other than 1, a reader/verifier applies
  exactly those *individual malformed conditions* (register rows) whose violated
  invariant is one `[R-CNT-24]` fixes in every major; the requirement that
  states a condition is irrelevant, and one requirement may be partly reaching.
- **H2/H3/H4.** A reader must form these three sums/products and reject on
  mathematical overflow above 2⁶³−1 — an obligation it did not previously have,
  because `[R-ENC-04]` withholds it from undesignated comparison-only expressions.
- **H5.** §17's rules range as their own words say; no blanket stored-tile
  quantifier overrides `[R-COD-07]`'s *addressed*-tile cap.
- **H6.** Exactly four §21.2 rows (F1, F6, F8, F14) apply to a non-major-1 file.
- **H7.** In Appendix G's profile, pinning the filter matters only where the
  byte-shuffle permutation is non-trivial: `s > 1` **and** `n = L/s > 1`.

## 3. Check-by-check results

### Group B (hunks 2, 3, 4) — clean

Register rows citing `[R-ENC-04]`: **F3** (file), **L2** (layer), **T12** (tile).
Every expression those rows name, traced to its defining section:

| expression | designated at | by |
|---|---|---|
| `dir_offset + dir_length` | §6.2 | **hunk 2** ✔ |
| non-layer top-level record `extent_offset + extent_length` | §7.2 | **hunk 3** ✔ |
| layer-record / sub-record `extent_offset + extent_length` | §7.2 | **hunk 3** ✔ |
| `N = ∏⌈Eᵢ/Tᵢ⌉`, `P = ∏Tᵢ`, `N·P`, `C·N` | §11.2 `[R-GEO-03]` | pre-existing ✔ |
| `P·Q`, `P·Bᶜ`, `Q = ΣBᵢ`, `Fᶜ` | §14.2 `[R-SER-02]` | pre-existing ✔ |
| every decoded size, `V` | §14.3 `[R-SER-07]` | pre-existing ✔ |
| `entry_count × 20 + ⌈entry_count/2¹⁶⌉ × 4` | §7.4 | **hunk 4** ✔ |
| non-sentinel entry `offset + length` (T12) | §15.3 states the condition directly ("offset + length overflows … *structural*: reject-tile") and §15.2 scopes `[R-ENC-04]`'s sum rule to non-sentinel entries | no designation needed ✔ |

House phrasing matches the pre-existing designations word for word
("declaration-derived quantit{y,ies} under `[R-ENC-04]`"). Outcomes agree:
hunk 2 → "Any failure is reject-file" and the trailer's owning scope is the
file (F3, file scope); hunk 3 → "at the scope the record governs … the layer
for a layer record and for sub-records, the file for other top-level records"
(L2 layer / F3 file); hunk 4 → "at layer scope" (L2). No overclaim, no bad
citation, no collision inside the passages. Group B is internally consistent
and consistent with Group A and C.

Residual (check 6, reported as X-08): hunk 2 pinned the sum on the left of the
comparison and left **`F − 64`** on the right unpinned. `[R-ENC-04]` reaches
"sum or product", not a difference, and nothing orders `[R-CNT-27]`'s F ≥ 128
test before §6.2's read of "the 8 bytes at F − 64".

### Group A (hunks 1 and 6)

Verified arithmetic in hunk 1: rows whose **Governing rule** cell names
`[R-CNT-06]` first are F8, F9, F10, F11, F12, F13, F14, F15, F16, F17 —
**ten**. Of those, F8 (trailer magic) and F14 (trailer CRC) assert invariants
`[R-CNT-24]` fixes; the other eight do not. ✔ The "ten" only works at
register-row granularity (§6.2's sentence enumerates twelve validations, and
fourteen rows *cite* `[R-CNT-06]` counting parentheticals) — the repair's own
"as §21.1 individuates them" is what licenses it. Good.

Verified hunk 6's list against `[R-CNT-24]`'s four fixed invariants
(magic at F−64; version_major/version_minor at F−56; CRC-32C at F−4 over
[F−64, F−4); front block constant): F8 ✔, F14 ✔, F6 ✔, F1 both instances ✔,
and nothing else in §21.2 asserts one. F5 and F15 excluded, matching the Note.
F10 reads redefinable trailer bytes but asserts a major-1 invariant, so it
correctly does not reach. **The four-row list is right.**

What is *not* right is everything around it — see findings X-01 through X-06.

### Group C (hunks 5 and 7)

Hunk 5 removes a real contradiction: the deleted sentence said "Every rule in
this section ranges over **stored** tiles", while `[R-COD-07]`'s normative text
says "a layer any of whose **addressed** tiles' decoded size exceeds
0x7E000000", §17.2's Note says "The cap is quantified over the layer's
*addressed* tiles", §21.9 says "*Decoded size of one tile* ranges over a
layer's **addressed** tiles, stored or not, exactly as `[R-COD-07]`'s cap is",
and §20.3 says the empty layer "escapes only because that cap is quantified
over addressed tiles". After the deletion all four agree.

Nothing was lost: every §17 rule self-quantifies — `[R-COD-01]` "A stored
tile's bytes", `[R-COD-02]` "Every stored tile", `[R-COD-04]` "A **non-sentinel**
index entry's length", `[R-COD-05]`/`[R-COD-06]`/`[R-COD-07]` "The stored
bytes", `[R-COD-08]` "the stored bytes". The retained preamble still carries
"the owning scope of one **stored** tile's payload under them is the tile".
**Hunk 5 passes every check.**

Hunk 7's mathematics is right. `[R-COD-10]`'s permutation sends byte *i* of
group *j* to offset `i·n + j`; the original offset is `j·s + i`. These agree for
all *i*, *j* iff `s = 1` or `n = 1` (take *i*=0, *j*=1: new 1, old *s*). So
"identity exactly where … the stride is 1 … and equally where … n = L/s being 1"
is exhaustive and correct, and `n = 1 ⇔ P = 1` is reachable (`[R-GEO-01]` floors
tile extents at 1). Two problems remain — X-07 and X-09.

## 4. Check 7 — analogies, verb against verb

| repair | its verb | cited rule's verb | same set? |
|---|---|---|---|
| H1 "one malformed state, **as §21.1 individuates them**" | "condition … reaches" | §21.1 "each row **is** one malformed condition" | rows only. §21.1 expressly disclaims §21.6/§21.7/§21.9 ("carry no rows"), so undetectable conditions get no individuation — harmless, they fall to the catch-all |
| H1 "`[R-CNT-06]` **states** ten" | "states" | §21.1 "A Governing rule cell **names** that requirement first" | ✔ same set (10) |
| H6 "Deriving it there **yields** F8, F14, F6 and **both of F1's instances**" | rows *and* **instances** | `[R-CNF-13]` "A **condition** … reaches"; §21.1 "the row **is** the rule, and each **instance is one file**" | ✘ **different sets** — see X-04 |
| H6 "…and is permanently invalid in every one **(§21.6)**" | "declares **no major at all**" | §21.6 "version_major = 0, permanently invalid in every format major version"; F18 "a permanently invalid **major**" | ✘ §21.6 does not say it — see X-03 |
| H7 "The filter is the identity **exactly where its permutation is** … (`[R-COD-10]`)" | "is the identity" | `[R-COD-10]` "the filtered image **places** byte i of group j at offset i·n + j"; "for a packed boolean plane s = 1 and the filter **is** the identity" | ✔ for filter 2; ✘ unqualified "the filter" also covers filter 1 — see X-09 |
| H2/H3/H4 "a declaration-derived quantity **under `[R-ENC-04]`**" | "is a declaration-derived quantity" | `[R-ENC-04]` "any quantity this specification **designates** a declaration-derived sum or product of integers obtained from a file" | ✔ identical form to §11.2/§14.2/§14.3 |

## 5. Searches run (whitespace-normalised unless noted)

- `grep -n 'R-CNT-24'` → lines 230, 233, 244, 255, 261, 814, 847, 1433, 3475, 3496.
- `grep -n 'declaration-derived'` → 441, 819 (h2), 976 (h3), 1086 (h4), 1561, 1896, 1977, 3527, 3884. Confirms the three hunks are the only new designations and that §11.2/§14.2/§14.3 are the precedents.
- `grep -n 'designat'` → 167, 168, 441, 445, 447, 2393, 3088, 3885. Line 445–447 is `[R-ENC-04]`'s express-designation clause; 2393 and 3088 are `>`-block / §20.3 restatements that the hunks do not disturb.
- normalised search `'reach'` (line-oriented, since "reach" never wraps mid-word) → **144 and 146 are the only surviving requirement-level statements of reach**: "save as to the requirements that reach it (`[R-CNF-13]`)" and "the failure of a reaching requirement is". Both in `[R-CNF-02]`, both normative bullet text, both in §2.3 — the same subsection hunk 1 edits.
- normalised `'declares no major'` → **one hit only**, §21.2's preamble (hunk 6's own text). `'permanently invalid'` → three hits: §21.2 preamble, F18's Condition cell ("a permanently invalid **major** in every format major version"), §21.6's closing paragraph.
- normalised `'the rule governs'` → **two hits only**, both in §21.1: "where a **row** and the rule it cites diverge" and "where such an **entry** [§21.6] and the rule it cites diverge". Neither covers a §21.2 subsection preamble.
- normalised `'ranges over'` / `'range over'` / `'addressed tiles'` / `'stored tiles'` / `'vacuously'` → confirms §17.2 Note, §20.3, §21.9 and L44 all use *addressed*, and that "vacuously" now appears nowhere (hunk 5's deletion was complete).
- normalised existence checks: `'1 = none — the filtered image is the decoded image'` True; `'for a packed boolean plane s = 1 and the filter is the identity'` True; `'A designation is express'` True; `'save as to the requirements that reach it'` True.

## 6. Findings (ids as returned)

X-01 UNSWEPT_RESTATEMENT (h1, h6) — `[R-CNF-02]` still quantifies reach over
requirements, citing the very rule that now disclaims it. **Byte-level.**
X-02 NEW_AMBIGUITY (h1, h6) — hunk 6 deleted the preamble's tie-break; §21.1's
precedence clause covers rows and §21.6 entries only.
X-03 CITATION (h6, h1) — "version_major = 0 declares no major at all (§21.6)"
is not what §21.6 says, and F18's own cell says the opposite. **Byte-level.**
X-04 TENSE_QUANTIFIER (h1, h6) — condition-level rule, instance-level derivation.
X-05 LOCAL_CONTRADICTION (h1, h6) — "MUST apply every reaching condition"
against `[R-CNT-04]`'s residency exemption, which F1 and F6 restate inline.
X-06 OVERCLAIM (h1, h6) — "Every other condition … is one of a structure this
text defines for format major 1 alone" is falsified by F18's version_major.
X-07 OVERCLAIM (h7) — "changes the stored bytes of every tile it touches".
X-08 UNDERSHOT (h2) — `F − 64` left unpinned beside the sum that was pinned.
X-09 NEW_AMBIGUITY (h7) — unqualified "The filter" plus "exactly" sweeps in
filter 1, which §17.3 makes the identity everywhere.

Clean: **hunk 3**, **hunk 4**, **hunk 5** — no finding.
