# Refute-only pass — G4 (r4-decode-clause)

## Disclosure

Read: the four briefs finding-A-01.md, finding-A-02.md, finding-X-01.md,
finding-X-02.md; hunk-01.diff; hunk-02.diff; and spec/tarn.md.
Did NOT read: full.diff, any other hunk file, docs/, conformance/, registry.json,
git history, the web. Did not list the r23audit directory.

Unrequested context appeared before I began: a project instruction file pointing
at AGENTS.md, and an index of the maintainer's memory notes naming things like a
"gate board", a "corpus build list" and prior-round workflow lore. I did not open
AGENTS.md or any memory file and drew no conclusion from the index. Disclosed as
required.

## Spec regions read (by sed/grep, absolute line ranges)

- 130–270 (§2.3 conformance classes: [R-CNF-02]…[R-CNF-12]; §2.4 outcome table)
- 2255–2300 ([R-COD-06], codec 3 zstd, incl. the tile content-size sentence)
- 2440–2520 (§18.2, the whole [R-MTA-09] passage plus its trailing Note)
- 3290–3380 (§21.1, How to read the register)
- 3486–3519 (§21.4 tile rows, incl. T22)
- 3520–3552 (§21.5 preamble + all ten R rows)
- 3600–3700 (§21.6 tail, §21.7, §21.8, §21.9 head + limits table)
- 3925–4012 (§24, [R-VEC-01]…[R-VEC-04])

## Greps run, verbatim

    grep -n "R-CNF-05\]\|R-CNF-04\]\|R-CNF-12\]\|R-CNF-07\]\|R-CNF-11\]" spec/tarn.md
    grep -n "^#### 21\." spec/tarn.md
    grep -n "21.8\|conformance corpus\|one vector per instance" spec/tarn.md
    grep -n "Frame_Content_Size\|content_size\|Content_Size" spec/tarn.md
    tr '\n' ' ' < spec/tarn.md | grep -o '.\{90\}whether or not.\{90\}'
    tr '\n' ' ' < spec/tarn.md | grep -o '.\{120\}content.size.\{120\}'

The last two were run on a whitespace-flattened copy precisely because the file is
hard-wrapped; the line-oriented greps above are for bracketed tags only, which
never wrap.

### "whether or not" — every occurrence in the document (flattened)

1. §? "(a rejected layer's claimants are not enumerated, whether or not the
   rejection impeded reading them"
2. blockquote: "a shrink is barred wherever it alters what §14 fixes for such a
   tile — whether or not the new state still stores it"
3. [R-COD-06]: "Writers MUST NOT compress a tile using a dictionary — whether or
   not the header discloses one"
4. "over the raw name bytes whether or not each name is itself well-formed"
5. "a shrink that turns real positions into padding of a tile stored there is
   barred whether or not the new state still stores it"
6. "every record it retains and does not logically modify, whether or not it
   implements the record's type"
7. R4 (the disputed clause)
8. §21.9: "an addressed tile has one whether or not its index entry is the
   sentinel"

In all seven non-disputed uses the consequent genuinely holds in BOTH branches of
the "whether or not" variable. That is the document's own idiom, and it fixes the
reading of the disputed conjunct: "the constraint is broken whether or not they
decode to the length it declares" asserts breach in the matching branch too.
So the clause is FALSE as written, not merely loose. A-01 and X-02 are right
about the text.

### "content-size" — every occurrence (flattened)

Only four sites: [R-COD-06]'s tile rule (2288-ish), the [R-COD-06] Note about
Window_Size derivation, §18.2's [R-MTA-09] sentence, and R4's cell (condition +
four instances). `Frame_Content_Size` appears once, at line 3514, T22.
Nothing anywhere else forbids the field's presence. So no rescue sentence exists,
and no second statement of the constraint exists that could fork independently.

## Instance-count arithmetic (independent, mine)

Script over lines 3374–3553 (§21.2 through §21.5), counting semicolon-separated
instances in column 3, "—" counted as 1:

    rows 121 instances 277

§21.8 line 3663: "121 conditions over 277 instances". Exact match. R4 = 16
instances (8 alternatives × 2 containers). The row was integrated cleanly; the
count is not a residue.

Corroborating: R4's four content-size instances are larger/smaller × two
containers. §21.1 lines ~3344–3352: "Where the condition compares two
**magnitudes** either of which can be the greater — a *differs from* or *does not
equal* — the two directions are likewise enumerated". A presence test would have
produced two instances naming presence. The cell is mechanically the signature of
a mismatch test. T22 (line 3514), the same rule's tile-side row, has the identical
larger/smaller shape (6 instances = 3 layouts × 2 directions) under the clean
condition text "is present but does not equal the tile's decoded size".

## Are the four findings two defects?

Yes — two, not four.

- **Defect 1 (A-01 ≡ X-02).** The appended conjunct "and — for the content-size
  field — whether or not they decode to the length it declares" asserts breach in
  the branch where the field equals the decoded length, i.e. registers a case
  [R-MTA-09] declares conforming.
- **Defect 2 (A-02 ≡ X-01).** The pre-existing blanket "unlike R3, the constraint
  is broken whether or not the bytes decode" now ranges over the content-size
  constraint, whose comparand exists only on a successful decode; §18.2 confines
  the R4 content-size case to "the bytes decode".

A-01 and X-02 are the same defect stated twice. A-02 and X-01 are the same defect
stated twice. Both defects are REAL as descriptions of the text.

## The shared premise I was sent to attack

All four downgrades rest on §21.1 lines 3313–3315: "each row *restates* its
governing rule, and where a row and the rule it cites diverge, **the rule
governs**." That is one sentence carrying four verdicts, which is exactly the
shape this pass exists to distrust. So I did not assume it and instead enumerated
constructions.

## Constructions built

### Construction A — the plain matching-FCS file (defect 1, writer)

Top-level user-metadata record, encoding 2, one zstd frame, `Frame_Content_Size`
present and equal to the decoded document's byte length, everything else clean.
Under [R-MTA-09] this file is CONFORMING ("it MAY be present"). This is the
charter's "set moves" signature: the disputed file is conforming.

- Reading M (rule): writer MAY emit the FCS field. File conforming.
- Reading R (row literal): FCS present ⇒ R4 fires ⇒ [R-CNF-05] bars every
  conforming writer from emitting it. Writer X emits an FCS-bearing frame header,
  writer Y clears the flag. **Different bytes.**

So the fork is genuinely available in principle. What closes it:

1. The Condition cell's own operative predicate delegates, inside the cell: "A
   user-metadata document stored under encoding 2 breaks one of the frame
   constraints **§18.2 states** or carries over from `[R-COD-06]`". The condition
   proper ends at the em-dash/semicolon. "**the** constraint is broken" is a
   definite singular anaphor whose only available antecedent is "one of the frame
   constraints" the head clause has already stipulated the document *breaks*. A
   presuppositional gloss cannot enlarge the extension of the predicate it
   glosses, and an implementer building from the row is sent to §18.2 by the row.
2. §21.1's tiebreak, above. R4's Governing rule cell names `[R-MTA-09]` first —
   and I confirmed the §18.2 passage closes with the tag `[R-MTA-09]` at line
   2502, so the diverging sentence is inside the cited rule.
3. [R-CNF-02] line 139: file conformance is "a pure predicate on bytes"
   determined by "every file-level requirement of this specification", and
   §21.1 says a row *restates* rather than states. The row is not a source of
   requirements.
4. The Instances arithmetic above, which testifies that the row's author wrote a
   mismatch condition.

Four independent closers, two of them inside the disputed cell itself. Both
readings converge. **Emittable set does not move.**

### Construction B — matching-FCS, verifier (defect 1, other actor)

Same file, verifier with a 32 MiB bound. Under R it reports *nonconforming*; under
M it certifies. Same four closers. No fork.

### Construction C — reader that must serve vs. ignore (defect 1, reader)

[R-CNF-04] line 171: "A reader MUST detect every violation the error register
(§21) assigns to the reader as its detector". This routes the reader's duty
*through the register* — the one place where the row could plausibly outrank the
prose. But §21.1 is part of the register's own reading instructions and hands the
decision to the rule. No fork.

### Construction D — the charter's "leave the damaged structure out of the live
state" move, applied to defect 2

The downgraders' premise for defect 2 is "the file is nonconforming under R3
anyway, and R3/R4 share the ignore-record outcome, so nothing moves". I attacked it
by hunting for a case where the bytes do not decode and yet the file is
CONFORMING, so that R3 has nothing to fire on and only the disputed clause bites.
§18.2 supplies exactly two such carve-outs, and I built both:

**D1 — the size-bound decline.** Document decodes to 20 MiB; reader's bound is the
§21.9 minimum, 16 MiB. §18.2 (normative body, not the Note): "a document exceeding
that bound is ignore-record like any other it cannot read."

**D2 — the window decline.** Frame declares `Window_Size` = 64 MiB, above §21.9's
8 MiB guarantee row; FCS present and correct; document decodes to 20 MiB. §18.2:
"a frame declaring more than the reader admits is ignore-record on that ground —
the reader's capability, not a failure to decode within the meaning of R3, and no
violation: **the file exceeds a §21.9 guarantee and so remains conforming** while
the reader MAY decline it (`[R-ERR-04]`)."

D2 is the best construction I found: a conforming file, bytes that (for this
actor) do not decode, FCS present. Under reading R the reader must record an R4
violation and a verifier must report *nonconforming*; under M the reader records a
capability decline and the verifier reports *cannot establish*. That is a real
accept/reject fork — if reading R is available.

It is not. Two sentences OTHER than the §21.1 tiebreak close D2:

- §21.5 preamble, lines 3526–3531: "every way its document can be unreadable takes
  this outcome … **except where a reader or verifier declines the decode on the
  size bound or on the frame's declared window, which `[R-MTA-09]` makes that
  actor's capability and not a fact about the file.**" This is a section-head
  carve-out that reaches R4 directly, without any row/rule arbitration.
- §18.2: "the decline is not a finding that the file is nonconforming and a
  verifier **MUST NOT** report it as one."

So the single construction in which the disputed clause could touch a conforming
file is foreclosed by normative text that is not the premise the downgraders
leaned on. This is the load-bearing result of this pass: the downgrade survives an
attack it was not built to survive.

### Construction E — updater / [R-CNF-06]

An updater carrying a metadata record forward verbatim (§20.4) must "satisfy every
writer requirement for the bytes it produces" ([R-CNF-06] line 189). Under R it
would have to rewrite or drop an FCS-bearing frame it is otherwise obliged to
preserve. Same closers as Construction A. No fork.

### Construction F — the corpus (are vector bytes the moving set?)

§21.8 [R-ERR-02]: "one vector per instance". §21.1: "the count is therefore
mechanical once the cell is written." The cell is written with four content-size
instances, all mismatches, all presupposing a decoded length. No builder is asked
for a matching-FCS vector or a non-decoding-FCS vector under either reading. And
[R-VEC-01] line ~3940: "where a vector's recorded expectation and this
specification disagree, this specification governs and the vector is corrected."
No fork in vector bytes.

### Construction G — a genuinely non-decoding frame with FCS present (defect 2)

FCS = 100, decode dies at byte 50. Under M: R3 only. Under R: R3 and R4. Both are
§21.5 rows, both ignore-record, and the file is nonconforming under both — the
charter's own signature for "not byte-level". Dual registration is a reporting
question. §21.1's specialization list ("F1 of F6 and of F8, F35 of F36, L24 of
L25") does not cover the pair, which is A-02's residue, but §18.2's "**the bytes
decode**, and what is wrong is what the header said about them" settles the
attribution and no byte moves either way.

## Constructions that failed to move anything, briefly

- Reader with a bound below the document's size, matching FCS: ignore-record under
  both readings (violation under R, capability decline under M — same observable
  at the record, and the verifier prong is closed by §18.2's MUST NOT).
- "The row is the rule" (§21.1, Instances paragraph, line ~3332) as a precedence
  claim outranking the tiebreak: it is scoped to corpus construction in the same
  sentence ("each instance is one file") and the tiebreak is stated two paragraphs
  earlier in the same subsection. Not available.
- Missing R4 instance for [R-COD-06]'s "no dictionary use, disclosed or not" (the
  carry-over list §18.2 now writes): checked and dismissed. §21.1's completeness
  is over *detectable* violations, and [R-COD-06] says in terms that "Dictionary
  use the header does not disclose is not detectable by inspection", with §21.7
  ([R-ERR-01]) carrying the account. No instance is owed.
- Whether [R-COD-06]'s content-size rule is carried over unchanged (which would
  demand a document's FCS equal "the tile's decoded size"): §18.2's "save two:
  what it states against a tile's declared decoded size" covers it, and §18.2
  states the replacement directly. No contradiction.

## Conclusion

Both defects are real defects in the text. Neither is byte-level. The clause is a
false gloss sitting on a correct condition, a correct Instances cell, and a
correctly cited governing rule, and every route from the false gloss to a byte is
cut — twice for defect 1 inside the cell itself, and twice for defect 2 by §21.5's
preamble and §18.2's MUST NOT, independently of §21.1's tiebreak.

The document is not missing a sentence of reasoning here: the reasoning that
answers both findings is on the page (§21.1's tiebreak, the Condition cell's own
delegating head clause, §21.5's decline carve-out, [R-MTA-09]'s "the bytes
decode"). What the document is missing is nothing; what it *has* that it should
not is the clause itself. The in-place fix is T22's formulation, already used one
subsection earlier: "…unlike R3, the constraint is broken whether or not the bytes
decode; the content-size constraint instead presupposes a decode, and is broken
where the field is present but does not equal the decoded length."

Verdict: DOWNGRADE_STANDS.
