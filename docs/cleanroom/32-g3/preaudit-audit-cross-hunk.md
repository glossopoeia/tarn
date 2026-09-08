# Cross-hunk consistency audit — round 32 (eighth view)

## Disclosure

Read: `spec/tarn.md` (whole file, in slices) and all 25 `hunk-NN.diff` files in
`/private/tmp/.../r32-audit/case/`. Did NOT read `full.diff`, did not list the case
directory beyond the `hunk-*.diff` glob, did not open `docs/`, `PLAN.md`,
`OPEN-QUESTIONS.md`, `AGENTS.md`, `README.md`, `conformance/`, `spec/registry.json`,
git history, or the web.

Context I did not ask for DID appear before I began: a project instruction file
(CLAUDE.md pointing at AGENTS.md — I did not open AGENTS.md), an index of the
maintainer's auto-memory notes with TARN-specific titles, and an environment block
naming the five most recent commit subjects (which name ADR numbers and resolved
question ids). I disregarded all of it; no finding below rests on it. I note that the
brief's stated hunk directory and the spec path were both exactly where the brief said.

Working files written: only this transcript, under `.../r32-audit/out/`, plus nothing in
`.../scratch/cross-hunk/` (all computation was inline `python3 - <<EOF` heredocs, no
script files persisted). No file in the repository was modified.

Tooling: every search below was run through one normaliser that strips a leading `> `
from each line, joins lines with a space, and collapses runs of whitespace — so
hard-wrapped and blockquoted phrases match. Every zero reported has a control search in
the same passage that returned nonzero.

## Grouping (derived from the text, not from headers)

- **G1 — the §14 bar and the bar beside it (§20.3 step 4, §11.1):** h11 (subject clause
  + list), h12 (carve-out/gloss), h13 (new tile-extents/dimension-order paragraph +
  renumbering gloss), h14 (anaphor made explicit), h15 (growth), h16 (shrink), h10
  (renumbering parenthetical), h5 (§11.1 **Rationale.** block restating the case).
- **G2 — stored byte widened to bit-in-a-packed-plane:** h5, h12, h15, h16 (four in step
  4/§11.1) + h24 (§23.1 privacy claim). Five sites; sweep verified complete.
- **G3 — occasions for a renumbering, one widened to two:** h10 (parenthetical) + h13
  (gloss two paragraphs below), with h6 (§13.3 **Note — sparse writing.**) as the
  re-emission restatement.
- **G4 — the "top-level" qualifier:** h1 (§2.3 conforming reader) + h21 (§21.9), against
  §21.6's closing paragraph which already carried it; h20's `[R-CNT-18]` addition sits
  beside it.
- **G5 — resource declines and partial totals:** h21 (R-ERR-04 restructured + scoped) +
  h2 (§5.2) + h4 (§9.7), against §18.2's prose (L2713), §21.6's document row (L3935),
  `[R-COD-06]`, `[R-CNF-11]`, and Appendix H's verifier line.
- **G6 — R-SER-08's "one byte":** h7 (§14.2) + h8 (§19.4 step 8) + h19 (§21.1), against
  §12.3's `[R-TYP-04]` and Appendix H's reader line.
- **G7 — flags:** h3 (trailer row) + h25 (Appendix H writer/updater lines), against
  `[R-CNT-08]` and §2.3's conduct-rule list.
- **G8 — preservation/authorship:** h9 (§20.3 step 2) + h17 (shape (c) drop) + h18
  (§20.4 governing-flags table), against `[R-WRT-01]`, `[R-WRT-03]`, §20.5.
- **G9 — standalone:** h22 (lz4 cap), h23 (§22.3 restructure — the next-day sentence),
  h20 (§21.6 rows).

## Force test applied (label, not marker)

Per `[R-CNF-01]` I read the opening words of every block a hunk landed in:
- h5 → `> **Rationale.**` — **non-normative**. Restatement only; normative twin is
  §20.3 step 4 (h11/h13), which says the same. OK.
- h6 → `> **Note — sparse writing.**` — **non-normative**.
- h17 → `> **Example — the three shapes a commit takes.**` — **non-normative**.
- h25 → Appendix H, heading says "(non-normative)". **Non-normative**.
- h3 → plain table in §6.2, no label, **normative**.
- h18 → plain table in §20.4, no label, **normative**.
- h20 → plain table in §21.6, no label, **normative**.
- h1, h2, h4, h7–h16, h19, h21–h24 → running prose, **normative**.
No repair's only statement of a rule sits in a labelled block: every labelled-block
repair has a normative twin that was edited in the same commit. Check 3 passes.

## Searches run (verbatim, with counts)

```
already holds the fill        -> 4   (L1642, L3207, L3293, L3328)
already hold the fill         -> 0   [control: "already holds the fill" -> 4]
bit in a packed plane         -> 5   (L1642, L2132, L3207, L3293, L3328)
bits in a packed plane        -> 1   (L4263)
padding position whose        -> 3   (L1641, L3206, L3327)
becomes padding               -> 0   [control: "ceases to be padding" -> 1 (L3294)]
turns real positions into padding    -> 1 (L4248)
turning real positions into padding  -> 1 (L4259)
[R-COD-06]                    -> 15
[R-CNF-11]                    -> 12
[R-ERR-04]                    -> 12
[R-CNT-18]                    -> 10
[R-TYP-04]                    -> 5
[R-CNT-14]                    -> 9
narrowest                     -> 5   (L2713, L3935, L4072, L4076, L4399)
serving it through            -> 2   (L3728, L3730)
serves through                -> 0   [control: "serving it through" -> 2]
the one byte                  -> 0   [control: "sole resolved byte" -> 1 (L4779)]
one byte a conforming file    -> 0   [control: "sole resolved byte" -> 1]
sole resolved byte            -> 1   (L4779, Appendix H)
Either way                    -> 2   (L4067, L4082)
empty directory               -> 4   (L650, L1037, L3926, L4420)
zero layers                   -> 1   (L3926)
the two capability refusals   -> 1   (L4078)
top-level MU = 1              -> 3   (L3464, L4080, L4804)
top-level record of a type    -> 2   (L179, L3770)
carries forward unmodified    -> 1   (L3157)
carries forward verbatim      -> 1   (L3508)
neither modify nor rely       -> 1   (L3102, [R-WRT-01])
neither modifies nor relies   -> 1   (L3130, [R-WRT-03])
```

## Citations opened and verdict

| Cited in | Citation | Verdict |
|---|---|---|
| h21 | `[R-COD-06]` "provides for a frame's window" | **PASS** — L2473: "permits a conforming reader to decline **the tile or the layer** on resource grounds". The layer is a containing scope. |
| h21 | `[R-CNF-11]` "presupposes" | **PASS** — L222: "when it declines **a layer's or a tile's** decode on resource grounds". |
| h21 | `[R-CNF-03]` | **PASS** — §2.3's conforming-reader duty. |
| h21 | "§21.6's closing paragraph names … the two capability refusals" | **PASS** — §21.6 closing names exactly two, and already qualifies the second as **top-level**. Count verified: two, no more. |
| h1 | §21.9's `[R-ERR-04]`; §21.6's closing paragraph "names the other two" | **PASS** on both. |
| h20 | `[R-CNT-18]` on the experimental MU=0 row | **PASS** — L1138 ends "with MU = 0 it is ignore-record", which is exactly the layer-scope half the row needed. |
| h20 | `[R-CNT-14]` on the zero-layers row | **PARTIAL** — R-CNT-14 licenses "any number of layer records (zero is valid)", so the row's wider claim follows; but R-CNT-14's own gloss still says only "an empty directory is a conforming generation". See X-07. |
| h22 | `[R-COD-07]` | **PASS** — L2503 word for word: "any of whose addressed tiles' decoded size exceeds 0x7E000000 … in a planar layer each channel's plane carries its own decoded size … and the largest governs". L44 agrees. |
| h11 | §11.4 / `[R-GEO-06]` for "the coordinate" | **PASS as to existence** — §11.4 is `[R-GEO-06]`'s home and does fix the coordinate↔value mapping. But it also fixes the disk ordinal; see X-01, X-10, X-14. |
| h13 | `[R-GEO-06]` "what fix the coordinate each stored value denotes" | **PASS** — §11.4's tile-coordinate and in-tile-ordinal clauses. |
| h9 | `[R-WRT-01]`, §20.1 | **FAIL** — quantifier mismatch, see X-09. |
| h9 | `[R-WRT-03]`'s depth | **PASS** — R-WRT-03 covers the full directory and the §19.4 index chain for reused segments; both examples fall inside it. |
| h12 | `[R-COD-10]`, `[R-SER-05]` | **PASS** — R-SER-05 (L2126ff) fixes padding-position content to the channel's fill, "the fill bit in a packed plane"; T4/T5 register both. |
| h24 | "§20.3 step 4 permits that shrink only where those bytes … hold the channel's recorded fill" | **PASS** — L3306ff: "A shrink is permitted exactly where it alters nothing §14 fixes for any tile the layer stores in the generation this commit supersedes", plus the carve-out at L3327. |
| h3 | F19 | **PASS** — F19 reads "Any bit of the flags incompat lane (bits 0-15) is set; this text defines no flag bits, so every such bit is unimplemented". |
| h25 | `[R-CNT-08]`, §6.3 | **PASS for the words quoted, FAIL as stated** — R-CNT-08 expressly excepts the compactor. See X-05. |
| h8/h19 | `[R-TYP-04]` (§12.3) | **PASS** — §12.3 already says "the one **case** where a reader resolves a byte", which is what h19 adopted. |
| h2/h4 | `[R-ERR-04]`, `[R-CNF-11]`, `[R-CNT-21]` | **PASS** — both restatements are word-for-word compatible with each other and with §5.2's governing clause. |
| h17 | "§20.4 licenses the drop" | **PASS** — §20.4's MU=0/PE=0 row: "an updater MAY drop the record in any commit it is otherwise free to make — one whose only effect is the drop included". |
| h23 | `[R-LIF-06]` | **PASS** — §21.6's mimic row agrees. |

## Derived numbers

The charter names counts in two places I could check mechanically:
- h21's "the two capability refusals §21.6's closing paragraph names" — §21.6's closing
  paragraph contains exactly two "The first is … The second is …" cases. Count = 2. Matches.
- h8/h19's abandoned "the one byte": an interleaved bool byte a conforming file cannot
  carry has 2^8 − 2 = **254** values, so the singular was wrong; both repairs correctly
  stopped counting. Appendix H's "the sole resolved byte" still counts. See X-06.
- h22's `0x7E000000` = 2,113,929,216 bytes; §21.9's tile guarantee 256 MiB =
  268,435,456. The hard cap is ~7.9× the guarantee, so the two rows do not collide.
- §11.4 disk ordinal c·N + s: with N = 2 and channels (a,b), a is at 0,1 and b at 2,3;
  appending c adds 4,5 and moves nothing; exchanging a and b moves all four. The
  document's own worked example agrees, so the ordinal bar's arithmetic is sound.

## Findings (detail in the structured return)

X-01 h11+h13   "no listed quantity moves" vs the coordinate now being a listed quantity
X-02 h13       "the geometry changes this step permits" overclaims against free re-declaration
X-03 h21       untouched "Either way" now under-counts three options
X-04 h21       widened decline scope not swept into §18.2 (L2713) and §21.6's row (L3935)
X-05 h25       writer "writes flags = 0 on creation" vs R-CNT-08's express compactor exception
X-06 h8+h19    Appendix H's "the sole resolved byte" left standing in the abandoned form
X-07 h20       R-CNT-14's own "an empty directory" gloss left unswept
X-08 h6        "a growth, a shrink or a channel removal that changes entry_count" — attachment
X-09 h9        "carries forward unmodified" vs R-WRT-01's "neither modifies nor relies on"
X-10 h11       coordinate limb needs a cross-generation tile-identity criterion never stated
X-11 h12       carve-out's general test still one value per stored byte in a packed plane
X-12 h11       three em-dashes, a pair nested in a dash-opened clause
X-13 h10+h13   the ordinal bar's ground made circular by the widened renumbering occasion
X-14 h11+h13   the untouched ground argues non-reach on bytes alone
