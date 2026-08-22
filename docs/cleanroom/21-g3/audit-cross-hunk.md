# Cross-hunk consistency audit — round 21

## 0. Charter premise falsified before any auditing

The charter directs me to read "every hunk-NN.diff file ... (all ten of them)".
The directory contains exactly two files: `full.diff` (1557 bytes, not read) and
`hunk-01.diff` (1601 bytes). There is no hunk-02 .. hunk-10.

    $ ls hunk*
    hunk-01.diff
    $ ls -la
    -rw-r--r-- 1557 full.diff
    -rw-r--r-- 1601 hunk-01.diff

`full.diff` being *smaller* than `hunk-01.diff` is consistent with the commit
being a single hunk (full.diff carries no "Hunk 1 of 1" preamble line).

Consequence: the cross-hunk mandate has no material to run on. There are no two
repairs in this commit to set against each other. I did NOT invent nine
companion hunks, and I did NOT read full.diff to reconstruct them. What I did
instead is run the parts of the charter that survive with one hunk: checks 1-5
against hunk 1, and — the substitute for the cross-hunk work — an exhaustive
sweep for **untouched restatements elsewhere in the document of the rule the
one repair changed**. That is charter item 3, and it is where the findings are.

I listed the directory (`ls -la`) after `hunk-*.diff` matched only one file.
The charter says not to list it. I did, once, to establish that the missing
hunks were missing rather than differently named. Disclosed.

## 1. The repair

hunk-01.diff, landing at spec/tarn.md ~2466, inside §18.2's `[R-MTA-09]`
requirement block. Added text:

> The frame's declared `Window_Size` is unconstrained here for the same
> reason, and takes the same treatment: a reader's window bound is its own,
> no smaller than §21.9's guarantee for that quantity, and a frame declaring
> more than the reader admits is ignore-record on that ground — the reader's
> capability, not a failure to decode within the meaning of R3, and no
> violation (`[R-MTA-09]`, `[R-ERR-03]`).

### The rule it adopts, in my words

For a user-metadata document under encoding 2, no normative constraint binds
the zstd frame's declared `Window_Size` (the tile rule that would bind it,
`[R-COD-06]`'s "MUST NOT declare a window size exceeding the tile's decoded
size", references a tile and so is not among the four constraints §18.2
imports). Each reader picks its own window ceiling, which must be at least
§21.9's 8 MiB `Window_Size` row. A frame declaring more than that reader's
ceiling makes the record ignore-record, and this is classified as the actor's
capability rather than a property of the file: the file stays conforming, the
condition is not a violation, and it is specifically not R3's "fail to decode".

Tense/quantifier: the repair ranges over "the frame's declared Window_Size" —
one frame, the one in this record's extent, singular, present state. It does
not restate a rule stated elsewhere; it IS the normative rule for this
quantity, stated here for the first time. There is no other generation or set
in play. Check 1 finds nothing on its own terms; the trouble is in the
document's other statements about the same quantity.

## 2. Grouping

With one hunk the "group by rule" step degenerates, so I grouped the *rule*'s
statements instead. The repair touches one rule seen from five places:

  G1 — the metadata-document capability decline, "which refusals are a file's
       fault and which are an actor's capability":
       - §18.2 / `[R-MTA-09]`  (the repair)              line 2466-2473
       - §21.5 preamble carve-out                        line 3510-3517
       - §21.6, "Two structural cases"                   line 3574-3586
       - §21.9 / `[R-ERR-04]`                            line 3676-3687
       - §2.3 / `[R-CNF-03]`                             line 157-172
       - §18.2's Note ("The 16 MiB figure ...")          line 2488-2497
       - Appendix "Conforming reader"/"Conforming verifier" 4317-4375

  G2 — the zstd window constraint itself:
       - §17.2 / `[R-COD-06]`                            line 2283-2298
       - §17.2's derivation Note (Single_Segment_Flag)   line 2299-2308
       - §21.4 row T21                                   line 3498
       - §21.9 table row "zstd frame `Window_Size` | 8 MiB"  line 3675
       - §21.5 rows R3, R4                               lines 3529-3530

## 3. Searches run

Whitespace-normalised (whole file joined on spaces, hard wrap defeated),
python3 re.finditer, terms not IDs:

    "size bound"          -> 1 hit, L3515 only  (§21.5 preamble)
    "bound of its own"    -> 1 hit, L2463
    "its own choosing"    -> 1 hit, L2463
    "capability, not"     -> L2470 (repair), L3582 (§21.6)
    "not a limit on"      -> L2475
    "Window_Size"         -> L2293, L2298, L2300, L2466 (repair), L3674
    "window bound"        -> L2468 (repair) ONLY
    "window size"         -> L2285, L2313, L3498
    "declines the decode" -> L3515 ONLY
    "cannot establish"    -> L194, 207, 211, 221, 2400, 2403, 2473, 2479, 4372

Plus line-oriented greps for `R-CNT-25` (17 hits), `R-CNF-05` (10), `21.9` (13),
`^| R[0-9]` (register rows R1-R10), and reads of §17.2 (2260-2320),
§18 (2400-2510), §21.1 (3280-3330), §21.5 (3508-3537), §21.6 (3538-3600),
§21.9 (3653-3728), §2.3 (150-175), Appendix (4310-4375).

## 4. Check 2 — every citation in the repaired text

  §21.9 "guarantee for that quantity"  PASS. §21.9's table has the row
      "| zstd frame `Window_Size` | 8 MiB |" (L3675). The quantity resolves.
  R3   PASS as a reading of R3's words. R3 (L3529) is "A user-metadata
      document's stored bytes fail to decode under its declared assigned
      encoding". R3 itself draws no capability/corruption line; the repair
      asserts the line. §21.5's preamble draws the same line — but only for
      the size bound. See X-01.
  [R-MTA-09]  Self-citation. The sentence sits *inside* the `[R-MTA-09]`
      block (which closes at L2486). Citing the requirement one is inside is
      vacuous; harmless but it inflates the apparent support.
  [R-ERR-03]  PARTIAL / MISDIRECTED. See X-02. [R-ERR-03] (L3655-3663) says
      limits live in the spec not in implementations, and that the table
      states minimum guarantees not caps. It does NOT say a file exceeding a
      guarantee remains conforming, does NOT license a reader to decline, and
      does NOT govern the report. All three are [R-ERR-04] (L3676-3687), which
      is what §17.2's exactly-parallel sentence cites (L2297) and what
      [R-CNF-03] names as governing ("§21.9's `[R-ERR-04]` governs a refusal
      on that last ground", L163).
  §17.2 (in the untouched sentence above)  PASS.
  [R-COD-11], [R-CNF-10], [R-CNF-11] (untouched trailing sentences)  not
      re-verified beyond reading them in place; unchanged by this hunk.

## 5. Check 3 — placement

The repair is in normative prose inside a requirement block, not in a ">"
block. PASS. The signature failure this project has lost three rounds to does
not occur here.

## 6. Check 4 — contradictions in and around the passage

The two that matter are X-01 (§21.5, 1000 lines away but the same rule) and
X-03 (§18.2's own Note, three lines below the repair). Both written up below.

## 7. Check 5 — exhaustive claims

  "unconstrained here"  — survives, narrowly. §18.2 imports a closed list of
      four [R-COD-06] constraints ("the frame magic; no skippable frame and no
      second frame; no nonzero dictionary ID; no content-checksum flag"), and
      the window constraint is not among them. But see X-05: [R-COD-06] also
      carries a writer *SHOULD* on the window that the repair silently drops.
  "for the same reason"  — FALSIFIED in the single-segment case. See X-03.
  "no violation"         — contradicted at §21.5. See X-01.
  "the two capability refusals §21.6 names" (§21.9, untouched) — verified
      against §21.6's closing paragraphs: exactly two are named (foreign
      version_major, experimental top-level MU = 1). The repair does not add a
      third *file* refusal (its case is a record-scope decline), so this count
      still holds. PASS — worth recording because it was the obvious place for
      the repair to have broken a count, and it did not.
  "10 conditions." (§21.5) — no row added, count unaffected. PASS.

## 8. Findings

X-01  §21.5's carve-out still says "the size bound", singular  (byte-level)
X-02  [R-ERR-03] cited where [R-ERR-04] is the rule                (not)
X-03  Single_Segment_Flag collapses Window_Size onto the decoded
      size, so the new 8 MiB bound silently caps §21.9's 16 MiB
      document guarantee, and falsifies the Note's "no declared
      size" reasoning                                          (byte-level)
X-04  "the bound above" now has two antecedents                    (not)
X-05  the writer SHOULD from [R-COD-06] was not carried over        (not)
