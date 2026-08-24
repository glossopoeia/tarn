# Refute-only pass — group G3 (open-vs-closed), finding X-07

## 0. Disclosure

Read, in full:
- /private/tmp/.../r23audit/refute/finding-X-07.md
- /private/tmp/.../r23audit/hunk-01.diff, hunk-02.diff, hunk-03.diff
- /Users/robertkleffner/Documents/GitHub/tarn/spec/tarn.md (portions listed below)

Nothing else. No docs/, no ADRs, no conformance/, no registry.json, no git
history, no full.diff, no other hunk file, no directory listing, no web.

**Unrequested context that appeared before I began.** My runtime preloaded: a
project instruction pointer (CLAUDE.md -> AGENTS.md), an index of the
maintainer's memory notes, and a git-status block carrying five recent commit
*subject lines*. Two of those subjects name §18.2's carry-over and the
content-size/R4 routing — i.e. exactly this group's subject matter, and one of
them asserts a conclusion about the very question I was asked to test. I did
not open any of those files and did not use the subjects as evidence. Every
conclusion below is re-derived from spec/tarn.md line ranges I quote. I flag
this because a disclosed breach is usable and a silent one is not.

## 1. Spec passages read (by line range)

| Lines | What |
|---|---|
| 2255–2310 | codec 3 / `[R-COD-06]` and its two Notes |
| 2269–2296 | `[R-COD-06]` proper — read twice, second time whitespace-normalised |
| 2440–2530 | §18.2 encoding-2 passage, through `[R-MTA-09]` and past it |
| 3297–3375 | §21.1 in full |
| 3374–3553 | the register tables (mechanical count) |
| 3505–3514 | T13, T17–T22 |
| 3520–3546 | §21.5 preamble + R1–R4 |
| 3608–3668 | §21.7 and §21.8 |
| 3985–4005 | `[R-VEC-03]` and its Note |

## 2. Greps run, verbatim

```
$ grep -n '^#### 21\.' spec/tarn.md
3297:#### 21.1 How to read the register
3374:#### 21.2 File-scope violations
3429:#### 21.3 Layer-scope violations
3486:#### 21.4 Tile-scope violations
3520:#### 21.5 Ignored records
3554:#### 21.6 Conditions that are not violations
3608:#### 21.7 What no check detects
3662:#### 21.8 Conformance vector coverage
3669:#### 21.9 Implementation limits

$ grep -n 'R-COD-06' spec/tarn.md
2296 (rule text) 2458, 2486 (§18.2) 3505 (T13) 3509 T17 3510 T18 3511 T19
3512 T20 3513 T21 3514 T22 3546 (R4) 3614 (§21.7) 3777

$ grep -n 'R-MTA-09' spec/tarn.md
203, 2501, 3531, 3546

$ grep -n 'Codec 3 — zstd' spec/tarn.md
2269
```

So `[R-COD-06]` spans exactly 2269–2296. That bound matters: the "open" set is
the whole of a 28-line rule minus two named members, and I could therefore
enumerate it exhaustively rather than argue about it.

Whitespace-normalised keyword sweep over 2269–2296 (the document is hard-wrapped,
so a line grep would have missed clauses spanning a break):

```
$ sed -n '2269,2297p' spec/tarn.md | tr '\n' ' ' | fold -w 100 | grep -n 'MUST\|SHOULD\|MAY'
... MUST begin with the compressed-frame magic ...
... MUST treat a payload whose first four bytes are not that magic, or that contains a skippable frame ...
... Writers MUST NOT compress a tile using a dictionary — whether or not the header discloses one ...
... MUST NOT emit a nonzero dictionary ID; a reader MUST treat a frame carrying a nonzero dictionary ...
... MUST NOT set the frame's content-checksum flag ... and MUST NOT declare a window size exceeding the tile's decoded size ...
... The frame content-size field MAY be present; when present it MUST equal the tile's decoded size, a reader MUST treat a mismatch ...
... a reader MUST NOT allocate or size any buffer from it ...
... Writers SHOULD keep the declared window within §21.9's 8 MiB ...
```

That is the complete normative inventory of `[R-COD-06]`: nine clauses.

## 3. Mechanical arithmetic (hunk 3's claim)

```
$ awk 'NR>=3374 && NR<=3553' spec/tarn.md | grep -E '^\| (F|L|T|R)[0-9]+ \|' | wc -l
121
$ python3  (semicolon count + 1 per Instances cell; a cell reading — counts 1)
R1 4  R2 2  R3 2  R4 16  R5 8  R6 4  R7 6  R8 2  R9 2  R10 2
TOTAL 277
```

121 rows, 277 instances, R4 = 16. §21.8's "121 conditions over 277 instances"
is arithmetically correct as the document now stands, and §21.5's "10
conditions." matches R1–R10. Hunk 3's recomputation is right.

## 4. The construction the charter asked for

The charter's test: *name one constraint that could be added to the open set
and that yields a file condition the closed enumeration does not carry.*

A finding only moves bytes if there is a file that one reading rejects and the
other accepts. So I built the difference set explicitly.

Reading A (open): a user-metadata encoding-2 extent is bound by **every**
`[R-COD-06]` frame constraint, save the two carve-outs.
Reading B (closed): bound only by the seven items §18.2 names, plus §18.2's
own two replacements.

Difference set = {`[R-COD-06]` clauses} − {two carve-outs} − {§18.2's list}:

| `[R-COD-06]` clause (2269–2296) | Disposition under §18.2 (2456–2487) |
|---|---|
| exactly one RFC 8878 frame | §18.2 states it itself ("exactly one RFC 8878 compressed frame occupying the extent's bytes before its terminal CRC") |
| frame magic | named: "the frame magic" |
| no skippable frame anywhere | named |
| no second frame | named |
| no dictionary use, disclosed or not | named — newly, in hunk 1 |
| no nonzero dictionary ID | named |
| no content-checksum flag | named |
| window ≤ tile decoded size | **carve-out 2** ("what it states about the frame's declared `Window_Size`"), replaced below |
| content-size = tile decoded size | **carve-out 1** ("what it states against a tile's declared decoded size"), replaced by "MUST equal the byte length of the decoded document" |
| reader MUST NOT size a buffer from content-size | named: "the bar on sizing any buffer from a length the frame itself declares" |
| SHOULD keep window ≤ 8 MiB | carve-out 2; and a SHOULD is not a violation in any case |

**The difference set is empty.** There is no clause in `[R-COD-06]` that
reading A applies and reading B does not. So no file exists that the two
readings sort differently, and no writer's emittable set differs between them.
The word "open" here is doing no work on any byte.

Independent cross-check I ran that the verifier's brief did not use in this
form: the tile-scope mirror. §21.4 registers the same rule's detectable
conditions as T17 (magic), T18 (second frame; skippable frame — 2 instances),
T19 (nonzero DID), T20 (content-checksum flag), T21 (window cap), T22
(content-size ≠, six instances over three layouts × two directions). Take that
set, remove T21 and T22 (the two carve-outs), add back §18.2's own two
replacements (content-size vs the *decoded document length*, two directions;
and the frame occupying the extent's bytes before the terminal CRC → "bytes
remaining after the frame"), and you get exactly R4's eight alternatives. Over
§18.1's two containers — top-level extent and layer sub-record extent — that is
16. The register agrees with itself from two directions. If R4 were short an
alternative, T17–T22 would have to be short one too, and it is not.

### Constructions I tried and that failed to move the set

1. **RFC 8878 well-formedness as an unlisted carried constraint.** Frame with
   `Frame_Header_Descriptor` reserved bit = 1. Not "a Zstandard compressed
   frame as defined by RFC 8878". Does one reading reject and the other
   accept? No — under both it is at worst R3 ("stored bytes fail to decode")
   and at best R4, and §18.2:2501 fixes the outcome for the whole section:
   "Any violation here is ignore-record, never the tile-scope outcome §17.2
   assigns." Same outcome either way; no reader's verdict moves.
2. **Undisclosed dictionary use, newly carried over by hunk 1.** This *is* a
   real widening of the writer's obligation relative to the old text ("the
   frame constraints of `[R-COD-06]` that do not reference a tile" — and
   "Writers MUST NOT compress a *tile* using a dictionary" does reference a
   tile). But it is a widening the current text states determinately, and it is
   *named* in §18.2's list, so readings A and B agree on it. It is also
   undetectable by construction, so no reader verdict turns on it; §21.7:3612–3615
   accounts for it generically — "an undisclosed compression dictionary
   (`[R-COD-06]`)" — with no tile qualifier, so §18.2's import of it needs no
   new §21.7 entry either. R4's *condition* nominally ranges over it while its
   cell does not enumerate it; that is exactly what §21.1 licenses, since
   register completeness is scoped to *detectable* violations.
3. **Zero-length / sub-4-byte frame region.** Falls to "missing frame magic";
   not a distinguishable extra alternative, and identical under both readings.
4. **Skippable frame placed before the compressed frame.** Fires both "missing
   frame magic" and "a skippable frame"; both are registered instances.
   Overlap, not a gap.
5. **Bytes before the frame.** = missing magic at offset 0. Covered.
6. **The buffer-sizing bar as a carve-out instead of a carry-over.** Even if an
   implementer read it as part of "what it states against a tile's declared
   decoded size" and dropped it, it constrains reader memory conduct, not file
   content. No byte, no verdict.
7. **Actor sweep.** §18.2 addresses writer, reader and verifier. R4's Detector
   is *reader* / *extent use*; the verifier paragraph at 2487–2500 governs
   declines and routes them to `[R-CNF-11]`, and §21.5's preamble (3529–3532)
   confirms a decline "on the size bound or on the frame's declared window"
   is "that actor's capability and not a fact about the file". No actor reaches
   the structure on terms the openness makes indeterminate.
8. **The register as the lever.** Could R4's cell or §21.8's total control a
   verdict? No. §21.1:3315–3317 — "each row *restates* its governing rule, and
   where a row and the rule it cites diverge, **the rule governs**." The
   register cannot decide any file. And [R-VEC-03]/§21.8 bind the *corpus*, not
   any file: "A missing vector is a gap in the corpus and never a licence to
   skip the check it would have exercised." A corpus gap is not an
   accept/reject verdict on bytes.

### The prospective form of the finding

The auditor's own closing sentence is "The defect is prospective." Suppose
someone later adds a tenth clause to `[R-COD-06]`. Then §18.2 carries it
automatically (that is what "named here or not" buys), R4's cell is short an
alternative, and §21.8's 277 is stale. Does that move bytes at that future
moment? No: §21.1:3309–3313 pre-classifies it — "Its **completeness is
normative** — a *detectable* file-conformance violation this specification
names and the register omits is a defect in this document" — and §21.1:3315–3317
decides the interim in favour of the rule. So even in the prospective case the
reader's verdict follows the rule, not the cell. The document, read alone, does
tell a reader that the scenario is a declared document defect rather than a
silent conformance change. That is the sentence the auditor quoted a fragment
of.

I also checked the auditor's premise as stated — "An open condition cannot have
an instance cell that §21.1's arithmetic derives or validates" — against
§21.1's own words: "Instances within a cell are separated by semicolons, and a
cell reading — is one instance; the count is therefore mechanical once the cell
is written" (3356–3358). The count is taken *from the cell*. And §21.1:3341–3343
licenses a whole family as one instance ("T24's *any codec*"). T13 and T25 are
in-register precedents for unbounded conditions with finite cells. The premise
fails on the document's text.

## 5. Verdict

DOWNGRADE_STANDS. Not byte-level, and — separately — not a live defect, because
the difference set between the open and closed readings is empty and the
register's authority is expressly subordinate to the rule.

One honest residual, reported as observation and not as a surviving finding:
§21.8's "277" is a hand-maintained integer inside a normative sentence bearing
`[R-ERR-02]`. Nothing in the document *derives* it; §21.1 only says the count is
mechanical once the cells are written. That is a maintenance hazard for the
document's editors, not an ambiguity for an implementer, and it predates all
three hunks. It does not change which bytes anyone may emit or must reject.
