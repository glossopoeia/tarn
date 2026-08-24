# Cross-hunk consistency audit — r23

## 0. Disclosure

Read: /Users/robertkleffner/Documents/GitHub/tarn/spec/tarn.md (many ranges, listed below);
hunk-01.diff, hunk-02.diff, hunk-03.diff, hunk-04.diff in the r23audit scratchpad.
Did NOT read: full.diff, docs/, PLAN.md, OPEN-QUESTIONS.md, AGENTS.md, README.md,
conformance/, spec/registry.json, git history, the web. Did not list the r23audit dir
(globbed hunk-*.diff only).

Unrequested context appeared before I began: a project instruction file pointing at
AGENTS.md, and an index of the maintainer's auto-memory naming several memory documents
(one of which names an ADR number and a round number). I did not open any of it and did
not use it. Nothing in this audit is derived from it.

Spec ranges read: 138-215, 640-665, 878-900, 1499-1526, 1900-1930, 2212-2360 (via
2260-2350), 2400-2530, 2560-2590, 3290-3375, 3520-3600, 3600-3670, 3655-3730, 3960-4030.

## 1. Commands run

    wc -l spec/tarn.md            -> 4404
    grep -n "R-COD-06|R-COD-07|R-MTA-09|R-MTA-10|R-SER-07|R-ERR-02|R-ERR-04|R-CNF-05|R-CNF-12"
    grep -n "R-CNF-03|R-CNF-10|R-CNF-11"
    grep -n "^#### 21\." / "^#### 17\." / "^### 11\." / "^### 24\."
    grep -n "User metadata is quarantined"
    # hard-wrap-safe search: flatten newlines first
    tr '\n' ' ' < spec/tarn.md | tr -s ' ' > flat.txt
    grep -o ".\{80\}<PHRASE>.\{100\}" flat.txt      for PHRASE in:
      "256 MiB" "16 MiB" "8 MiB" "per-instance" "actually contains" "minimum guarantee"
      "addressed tiles" "content-size" "Frame_Content_Size" "content size" "Window_Size"
      "window size" "encoding 2" "user-metadata document" "metadata document"
      "one RFC 8878" "ignore-record"
    # instance arithmetic
    awk 'NR>=3374 && NR<3554' spec/tarn.md | grep -E '^\| [FLTR][0-9]+ \|' | awk -F'|' ...
      -> ROWS=121 INSTANCES=277   (R4 = 16)

## 2. Grouping (by rule, not by section)

GROUP A — "where does a user-metadata encoding-2 frame-header defect land, and what is
the set of constraints such a frame must satisfy?"  Hunks 1 and 2.
  H1 (§18.2/R-MTA-09) restates the carry-over set from [R-COD-06] as open-ended-minus-two,
  and re-routes a content-size mismatch from R3 to R4.
  H2 (§21.5 R4) receives that routing: new clause + 4 new instances.
  Third party never touched: [R-CNT-25] (§7.1), the §21.5 preamble, §21.7, T21/T22.

GROUP B — "how many corpus files does the register demand?"  Hunks 2 and 3.
  H2 adds 4 instances; H3 moves the §21.8 total 273 -> 277. Also reaches R-VEC-03 (§24).

GROUP C — "what does a §21.9 limits row range over?"  Hunks 4 and 1.
  H4 (§21.9) splits the three per-instance rows into two quantifiers.
  H1 leans on two of those rows by name ("§21.9's user-metadata guarantee", "§21.9's
  guarantee for that quantity" = the Window_Size row). H1's licence to decline is measured
  against H4's quantifiers.
  Third party never touched: [R-CNF-03]'s "none of whose values exceeds", R-ERR-04's
  scope list, R-COD-06's Window_Size Note and its writer SHOULD, R-COD-07 + its Note.

Section numbers do NOT group these: H1 is §18.2, H2 is §21.5, H3 is §21.8, H4 is §21.9,
but H1+H2 are one rule and H1+H4 are another, and H2+H3 are an arithmetic pair.

## 3. Rule each repair adopts (in my words)

H1: For an encoding-2 user-metadata document, the frame must satisfy every constraint
[R-COD-06] places on a frame — the list being open, not closed — except the two families
§18.2 replaces (tile-declared-decoded-size, and Window_Size). The decoded size and the
window are the reader's own bounds, floored by §21.9. The content-size field, if present,
must equal the decoded document's byte length; a mismatch is an R4 frame-constraint
violation, not an R3 decode failure.

H2: R4's condition covers the content-size mismatch, in both directions, in both
containers, and R4's constraints bite independently of whether the bytes decode.

H3: The corpus build list is 121 conditions over 277 instances.

H4: "decoded size of one tile" is quantified over a layer's ADDRESSED tiles (stored or
not), because decoded size is declaration-derived; the other two per-instance rows are
quantified over stored objects, which cannot exist unstored.

## 4. Within-group agreement

A: the routing agrees (both send content-size to R4) — the coordination succeeded.
   The disagreements are in the surrounding words: see X-01, X-02, X-03, X-05, X-06.
B: verified mechanically. R4 went 12 -> 16 instances; 273 + 4 = 277; my own count of
   §21.2-§21.5 gives ROWS=121, INSTANCES=277 exactly. H3 PASSES.
C: agree on the two rows H1 uses. The failure is what H1 stripped: see X-04, X-08.

## 5. Check 7 — analogy verbs, side by side

(a) H4 vs [R-COD-07]:
    H4:        "ranges over a layer's **addressed** tiles, stored or not"
    R-COD-07:  "for a layer any of whose addressed tiles' decoded size exceeds 0x7E000000"
    R-COD-07 Note: "The cap is quantified over the layer's *addressed* tiles"
    Same set. PASSES. (This is the round-22 defect and it is genuinely fixed.)
    Sub-warrant: "a tile's decoded size is a function of the layer's declarations alone
    ([R-SER-07])" vs R-SER-07 "decoded size is a function of the layer's declarations
    alone — geometry, layout, and channel types". Verbatim match. PASSES.
    Tested per member: planar layers address C*N tiles each with its own plane size
    (P*B^c or ceil(P/8)) — L44's instance cell enumerates exactly those. PASSES.

(b) H1 vs [R-COD-06] on content-size:
    H1:        "when present it MUST equal **the byte length of the decoded document**"
    R-COD-06:  "when present it MUST equal **the tile's decoded size**"
    R-COD-06 calls its neighbours "both being header-checkable"; the tile's decoded size
    is declaration-derived (R-SER-07), so the tile comparison needs no decode. The
    document comparison needs a full decode. DIFFERENT QUANTIFIERS -> X-03.
    H1 is honest about the transposition in one clause ("the quantity a document does
    have, its decoded length, in place of the declared size it does not") and then
    contradicts it in the next ("keeps the condition checkable from the bytes alone").
    The two halves point opposite ways — the round-22 shape, recurring.

(c) H1 vs [R-COD-06] on the Window_Size treatment:
    H1:        "The frame's declared `Window_Size` is unconstrained here"
    R-COD-06:  "MUST NOT declare a window size exceeding the tile's decoded size" +
               "Writers SHOULD keep the declared window within §21.9's 8 MiB
                `Window_Size` guarantee even for a larger tile"
    R-COD-06 Note: "with Single_Segment_Flag set there is no Window_Descriptor and
               Window_Size is the frame content size"
    §18.2 pins the content size and declares the window unconstrained; for a
    Single_Segment frame those are the same number. -> X-04.

(d) H1 "exactly as `[R-COD-11]` requires of a codec it cannot execute" (unchanged text):
    R-COD-11 (§17.4): "a verifier ... cannot establish that layer's conformance and MUST
    NOT certify the file". H1: "cannot establish that document's conformance and MUST NOT
    certify the file". PASSES.

## 6. Check 2 — citations, all of them

  [R-COD-06] (§17.2, l.2269-2296)  — states magic / one-frame / dict-ID / checksum-flag /
      window<=decoded / FCS==decoded / no buffer-sizing / writer SHOULD 8 MiB.  H1's
      "save two" carve-out overlaps itself (the Window_Size cap IS stated against the
      tile's declared decoded size) — see X-05 note. Otherwise resolves.
  [R-COD-07] (l.2323-2326) — as quoted above. PASSES for H4.
  [R-COD-11] (l.2396-2413) — PASSES.
  [R-SER-07] (l.1916-1923) — PASSES for H4.
  [R-CNF-02] (l.138-157) — "File conformance is a pure predicate on bytes: it does not
      depend on any reader, writer, or environment." Supports "does not turn on a
      decoder's tolerance". Does NOT support "checkable from the bytes alone":
      checkability is a separate axis this document keeps separate (§21.1 "detectability
      being the gate [R-CNF-07] already applies"; §21.7 "What no check detects"). PARTIAL
      -> X-03.
  [R-CNF-03] (l.158-172) — "MUST accept every conforming file ... none of whose values
      exceeds the minimum guarantees of §21's limits table". Load-bearing for X-04.
  [R-CNF-10] (l.278), [R-CNF-11] (l.193-223) — resolve as H1 claims. PASS.
  [R-ERR-04] (§21.9 closing) — "A file exceeding any of these remains conforming, and a
      reader MAY decline it — at the whole file, or at the narrowest scope whose
      declarations exceed what it can serve, a layer or a tile." No record scope -> X-08.
  [R-MTA-03] / [R-MTA-10] (l.2560-2580) — "The document rules of this section — the frame
      constraints of encoding 2, ..." is a *set reference*, so H1's widening of the set
      survives it. PASSES, no sweep needed. (Checked because it is the one other place
      that names "the frame constraints of encoding 2".)
  [R-CNT-25] (§7.1, l.886-898) — enumerates the ignore-record grounds as four ways the
      document "can be unreadable". Does not cover H1's new class -> X-06.
  §21.9 (cited by H1 twice) — the two rows exist and read as H1 says. PASSES.
  §17.2 (cited by H1's closing "never the tile-scope outcome §17.2 assigns") — §17.2 is
      "Codecs", which is where the tile-scope outcomes live. PASSES.
  §11.2 (cited by H4 for "A layer addressing no tile") — §11.2 is "Grid arithmetic",
      which defines the addressed-tile count (N, or C*N) but does not itself state that a
      layer may address none; that is §21.6 / [R-GEO-02] (l.79613 flat: "A dimension with
      extent 0 is valid: ... the layer has zero addressed tiles"). R-COD-07's own Note
      cites "[R-GEO-02], §21.6" for the identical proposition. WEAK BUT DEFENSIBLE —
      §11.2 is where the count is defined and the count is what goes to zero. Not
      reported as a finding; noted.
  §21.6 (cited in the untouched sentence "the two capability refusals §21.6 names") —
      §21.6's closing paragraph names exactly two ("Two structural cases are conforming
      files a reader nevertheless refuses"), and [R-CNF-03] independently says "§21.6's
      closing paragraph names the other two". PASSES — the count is right, and H1's new
      capability decline for documents lives in §21.5, not §21.6, so it does not falsify
      "the two".

## 7. Check 3 — does each repair sit in normative text?

H1: §18.2 body, requirement tag [R-MTA-09] at the end of the paragraph. NORMATIVE. The
    adjacent "> **Note.** The 16 MiB figure ..." block is non-normative and the repair
    did not hide anything in it. PASSES.
H2, H3: register rows / §21.8, both normative (§21.1 makes the register's completeness
    normative). PASSES.
H4: §21.9 body, [R-ERR-03]/[R-ERR-04]. NORMATIVE. PASSES.
No repair landed in a ">" block. No repair edited a ">" block while leaving a stale
normative statement.

## 8. Check 5 — exhaustive claims

H1 "every frame constraint ... named here or not, save two"  -> the two overlap; see X-05.
H1 "named for convenience, not as a closed list"             -> collides with H2/H3; X-07.
H2 "whether or not the bytes decode"                         -> X-01.
H2 "whether or not they decode to the length it declares"    -> X-02.
H4 "neither of which exists except as stored bytes"          -> true for both.
H4 "The first five rows range over declarations, which every file and every layer
    carries"                                                 -> survives charitably (a
    zero-layer file carries no layer declarations, but then the layer rows range over
    nothing, which is the intended reading). Minor blur: H4 itself establishes that the
    tile row is ALSO declaration-derived, so "declarations" no longer names the contrast.
    Noted, not reported.
H3 "121 conditions over 277 instances"                       -> VERIFIED MECHANICALLY.
§21.9 "the two capability refusals §21.6 names"              -> VERIFIED, still two.
§21.5 "10 conditions"                                        -> R1..R10, still ten.

## 9. Check 6 — the structure, member by member

Structure H1 governs: the RFC 8878 frame header of an encoding-2 user-metadata document.

  magic                    pinned (carried over)              R4 instance
  skippable/second frame   pinned                             R4 instance
  trailing bytes           pinned by §18.2's own words        R4 instance
  Dictionary_ID            pinned                             R4 instance
  dictionary use undisclosed  pinned by H1's new words        NO instance, undetectable (X-05)
  Content_Checksum_flag    pinned                             R4 instance
  Frame_Content_Size       pinned to decoded length           R4 instance (new)
  Window_Descriptor/Window_Size   EXPRESSLY UNPINNED, and the tile rule's writer SHOULD
                           is carved out with it                       -> X-04
  Single_Segment_Flag      UNPINNED — and it is the flag that makes Window_Size equal
                           Frame_Content_Size, i.e. makes the pinned member determine the
                           unpinned one                                -> X-04
  reader buffer-sizing bar carried over, but it is not a frame member  -> X-05
  block sizes, reserved bit  left to RFC 8878. Acceptable.

The sibling H1 left unconstrained is the window, and it is not merely unconstrained: the
repair actively strips the one writer SHOULD that the identical tile rule carries.

## 10. Check 4 — the whole passage, including untouched text

§18.2, untouched closing: "Any violation here is ignore-record, never the tile-scope
outcome §17.2 assigns." This is what saves X-06 from being fatal — it grants the outcome
that [R-CNT-25]'s enumeration no longer reaches.

§21.5 preamble, three lines above H2's edit, untouched: "every way its document can be
unreadable takes this outcome ... as a violation in the rows below". H2's four new
instances are not ways the document is unreadable. -> X-06.

§21.9, immediately below H4, untouched: R-ERR-04's scope list "a layer or a tile" now
sits under a paragraph that has just been sharpened to say two of the three per-instance
rows are individuated per user-metadata document / per frame — neither of which is a
layer or a tile. -> X-08.

§21.1, untouched, governs both edits: "where a row and the rule it cites diverge, the
rule governs" (bounds X-02's damage), and the instance arithmetic — "Where the condition
compares two **magnitudes** either of which can be the greater — a *differs from* or a
*does not equal* — the two directions are likewise enumerated". H2's 2 directions x 2
containers = 4 is EXACTLY what §21.1 prescribes, and matches T22's method (3 layouts x 2
directions = 6). H2's instance arithmetic PASSES.

## 11. Byte-level verdicts

None of the four repairs moves the emittable byte set. The whole R3->R4 re-routing is
verdict-neutral: R3 and R4 are both §21.5 rows, both ignore-record, both violations, so
the file is nonconforming and the record is skipped under either routing. What moves is
which row a verifier names, which vector the corpus builds, and (X-01) whether a reader
that declined the decode owes a detection it cannot perform.

X-04's disputed file (12 MiB single-segment encoding-2 document, Window_Size 12 MiB) IS
conforming, but no reading forces a reader to accept it: [R-CNF-03]'s duty lapses on
"none of whose values exceeds", and 12 MiB exceeds the 8 MiB Window_Size row. So the
guarantee is nullified rather than forked. Not byte-level. Reported anyway because it is
a check-6 finding, not a contradiction finding.
