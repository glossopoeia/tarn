# Refute-only pass — group G6 (limits-quantifier): B-01, B-02, B-03, X-08

## 0. Disclosure

Read, in this order:
- The four briefs: finding-B-01.md, finding-B-02.md, finding-B-03.md, finding-X-08.md
  (in .../r23audit/refute/).
- hunk-04.diff and hunk-01.diff (my charter's two hunks). Nothing else in
  r23audit/ was opened; I did not list the directory, did not open full.diff,
  and did not open any other hunk or brief.
- spec/tarn.md, by `sed -n` on line ranges and by grep. Ranges opened:
  140–235, 270–282, 305–340, 615–650, 1499–1526, 1905–1930, 2270–2350,
  2410–2520, 3320–3335, 3520–3548, 3556–3572, 3660–3730, 3985–4000,
  4095–4103, 4345–4360.

Ran locally: greps listed verbatim below, plus one whitespace-normalising
pass (`tr '\n' ' ' | tr -s ' '`) into a scratch flat copy of spec/tarn.md,
used because the document is hard-wrapped.

Read nothing under docs/, conformance/, PLAN.md, OPEN-QUESTIONS.md,
AGENTS.md, README.md, spec/registry.json; ran no git command; no web.

**Unrequested context that appeared before I began.** My runtime placed a
project-instruction pointer (CLAUDE.md -> AGENTS.md) and an index of the
maintainer's private memory notes in my context. I did not open AGENTS.md or
any memory file, and I have disregarded the index's contents; none of it
figures in any conclusion below. Naming it here as a disclosed exposure.

## 1. The passage, as it now stands (spec/tarn.md 3692–3707)

Verified by `sed -n '3660,3730p'`:

```
The last three rows are **per-instance**, and are individuated
differently. *Decoded size of one tile* ranges over a layer's
**addressed** tiles, stored or not, exactly as `[R-COD-07]`'s cap is:
a tile's decoded size is a function of the layer's declarations alone
(`[R-SER-07]`), so an addressed tile has one whether or not its index
entry is the sentinel. A layer addressing no tile (§11.2) therefore
has no tile whose decoded size the table bounds. The other two range
over the user-metadata documents and compressed frames a file
actually contains, neither of which exists except as stored bytes.
Either way a file containing no instance of a kind does not exceed
that row, whatever its declarations would derive. The first five rows
range over declarations, which every file and every layer carries.

A file exceeding any of these remains conforming, and a reader MAY
decline it — at the whole file, or at the narrowest scope whose
declarations exceed what it can serve, a layer or a tile.
```

Both hunks are as the diffs describe. Confirmed by `grep -n` that the
quotations in all four briefs are accurate and in place (3692, 3700, 3701,
3705–3706).

## 2. Fixing the byte-level lever before testing anything

§21.9's rows never move a *file's* conformance: line 3705 says outright "A
file exceeding any of these remains conforming". So the only thing this
paragraph can move is the **must-accept** relation, and that is squarely
inside the charter's test ("...or must accept or reject"). Two normative
statements make the paragraph load-bearing for it:

- §2.3 `[R-CNF-03]`, 158–165: "A reader MUST accept every conforming file
  ... and none of whose values exceeds the minimum guarantees of §21's
  limits table".
- §2.5 `[R-CNF-10]`, 272–277: "Readers MAY enforce resource limits, but MUST
  accept any conforming file within the minimum guarantees stated in §21's
  limits table".

So: **the per-instance paragraph decides which values a file has, and
therefore decides which byte sequences every conforming reader is obliged to
accept.** A genuine fork in it *is* byte-level. I did not accept any
verifier's "the file stays conforming, so nothing moves" move — that move is
wrong as stated, and three of the four verdicts lean on it. What follows is
therefore a fork hunt, not a re-reading of the verdicts.

The correct test per finding: is there a **conforming** file F such that one
reading of the paragraph makes some value of F exceed a row (so every reader
may lawfully decline F) and the other does not (so every conforming reader
MUST accept F)?

## 3. Word-by-word quantifier check against each cited warrant

Charter instruction: compare governing verbs word for word, per row, against
the rule cited as warrant. This is the shape that produced last round's
surviving defect, so I did it first.

**Row 6 vs `[R-COD-07]`.** §21.9 claims the tile row is quantified "exactly
as `[R-COD-07]`'s cap is". `[R-COD-07]` normative text, §17.2 line ~2320
(read at 2270–2350, *not* the Note):

> "Writers MUST NOT declare this codec for a layer any of whose **addressed**
> tiles' decoded size exceeds 0x7E000000 bytes"

"any of whose addressed tiles". §21.9: "a layer's **addressed** tiles, stored
or not". **Match.** No quantifier mismatch. (The 2328–2331 Note that the B-02
verifier quoted is a blockquote and carries no force under `[R-CNF-01]` — but
it is not needed, because the normative rule itself carries the quantifier.
I checked this specifically, because "repair written into a Rationale" is the
failure mode named in my charter.)

**Row 6 vs `[R-SER-07]`.** §14.3 line 1917–1922: "decoded size is a function
of the layer's declarations alone — geometry, layout, and channel types —
never of payload content". The paragraph's warrant sentence is exact. Match.

**"A layer addressing no tile (§11.2)".** §11.2 (1499–1510) gives
N = ∏⌈Eᵢ/Tᵢ⌉ and addressed-tile count N (interleaved) or C·N (planar); an
extent of 0 yields 0. §21.6's table (3563) confirms: "A dimension has extent
0 | A valid, empty layer: zero addressed tiles, an empty index". Accurate.

**Planar cross-check.** §3.1 (308–312): in a planar layer a *tile* is "one
cell of the grid for one channel". `[R-COD-07]`: "in a planar layer each
channel's plane carries its own decoded size ... and the largest governs".
Row 6 ("decoded size of one tile") therefore lines up per-plane in a planar
layer under both. Consistent.

**Row 3 vs §11.2.** "addressed tiles per layer (entry_count)" — §11.2 calls
the addressed-tile count "the number of its tile-index entries". Match.

Conclusion: the repair's quantifier claims are all true of the rules they
cite. No mismatch of the kind that survived last round.

## 4. B-01 — do rows 7/8 reach superseded instances in slack?

Construction attempted (the auditor's, made concrete):

> F1: a conforming file, committed several times. Live state carries one
> file-scope user-metadata record whose document decodes to 1 MiB. An earlier
> commit's user-metadata extent, superseded, still physically present,
> decodes to 100 MiB. Every live value is within §21.9.

Reading (a) physical-bytes: F1 has a 100 MiB document value -> exceeds row 7
-> `[R-CNF-03]`'s duty lapses -> any reader may decline F1.
Reading (b) live-state: F1's values are all within -> every conforming reader
MUST accept F1; one that declines is nonconforming.

That fork *would* be byte-level. It is closed by normative text.

§5.2 `[R-CNT-21]`, lines 630–634, read in full:

> "Every byte the live state does not claim is **slack**: alignment and slab
> gaps, the pre-trailer pad, and everything an earlier commit superseded.
> Slack has no internal structure this specification defines, its content is
> unconstrained, and **no conformance requirement applies to it**. A reader
> MUST NOT interpret it (§9.5)"

The decisive clause is "no conformance requirement applies to it", not the
MUST NOT. Row 7 and row 8 are conformance requirements — they are the
antecedent of `[R-CNF-03]`'s and `[R-CNF-10]`'s duties. A requirement that
does not apply to slack cannot take a value from slack. So under the
document's own terms F1 has no 100 MiB document value, and reading (a) is
not available. §21.6's restatement at line 3568 says the same in the register
region itself: "Bytes the live state does not claim — alignment gaps, the
pre-trailer pad, superseded structures | Slack: unconstrained content, **no
conformance requirement** ... `[R-CNT-21]`".

§3.1 corroborates but is narrower than the B-01 verifier claimed. Its
"unqualified *stored* means stored in the live generation. Superseded payload
bytes from earlier generations do not make a tile stored" sits inside the
**addressed tile / stored tile** bullet and governs the predicate *stored* as
applied to a tile. It does not by its own terms govern the phrase "exists as
stored bytes" applied to a document. I record this because the verifier's
argument 1 is weaker than it reads; the closure is §5.2's, not §3.1's.

Escape routes I tried against the closure, and why each fails:

1. *A reader that learns the fact lawfully.* None exists. Locating the
   superseded record requires reading a superseded directory, and §9.5 bars
   the backward scan ("a conforming reader declines the torn file rather than
   scanning backward (§9.5)", found in the flat pass). §9.7's verifier "walks
   the live state only", summing slack without reading it.
2. *A recovery probe.* §9.6 makes the earlier state "a different artifact" —
   a different byte sequence (a prefix), so no fork on F1's bytes.
3. *A reader that declines F1 arbitrarily.* Under (a) it would be conforming,
   under (b) not. But this only re-states the fork; it needs (a) to be
   available, and §5.2 denies it.
4. *The writer side.* `[R-ERR-03]` "a writer MAY rely on that" is a
   permission. Neither reading obliges a writer to compact rather than
   append, so the **emittable** set does not move under either.

Also checked the verifier's argument 2 and found it weaker than stated:
`[R-CNT-14]`'s "at most one file-scope user-metadata record" is scoped to
*the directory*, which §3.1 defines as the live generation's, so reading (a)
would not have made F1 nonconforming. It is a reductio, not a closure. The
closure is §5.2 alone — and §5.2 is enough.

**B-01: does not survive. Not byte-level.**

## 5. B-01, second construction — a live extent whose bytes parse as a frame

The class the auditor was in ("row 8 counts frames physically present")
survives §5.2 only if the bytes are *live*. So:

> F2: conforming file, one file-scope user-metadata record declaring
> encoding 0x85 (experimental range). Its extent's bytes happen to be a
> well-formed zstd frame declaring Window_Size = 64 MiB. The extent is a
> record extent, hence live state (§5.2's partition), not slack.

Does F2 "actually contain" a compressed frame with a 64 MiB window? This is
not what B-01 reported, but it is the same class with §5.2's closure removed,
so I built it. It fails on §21.6's table row (3570):

> "A user-metadata record declares an experimental-range (≥ 0x80) document
> encoding | Ignored (ignore-record); the file is conforming ... **No
> document rule attaches at such an encoding**, so a verifier certifies,
> reporting the record it ignored | `[R-MTA-03]`, `[R-EXT-03]`, `[R-CNF-02]`,
> `[R-MTA-10]`"

Nothing makes those bytes a "compressed frame" in this document's sense:
§18.2 `[R-MTA-03]` makes the record ignore-record, and only encoding 2
("Encoding 2 stores it as exactly one RFC 8878 compressed frame") and codec 3
("The stored bytes are exactly one Zstandard compressed frame") ever
constitute an extent as a frame. Grep on the flat copy for "compressed frame"
returns exactly four sites: §17.2 codec 3, §18.2 encoding 2, register T18,
and §21.9 line 3700. No reader is ever obliged or permitted to decode F2's
extent, so no window guarantee can bind on it. Fork not available.

## 6. B-02 — the summary sentence's "containing"

Disputed file, as the auditor built it:

> F3: one layer, 4,096 addressed tiles, **none** stored (every index entry
> the sentinel), declarations deriving 512 MiB decoded per tile. 512 MiB <
> 0x7E000000 = 2,113,929,216, so no cap is broken; F3 is conforming.

Under "instance = addressed tile", F3 exceeds row 6 and a reader MAY decline
it. Under the summary sentence read with "containing" as physical, F3
contains no tile, does not exceed, and every conforming reader MUST accept
it. That fork is byte-level *if it is genuinely open*. It is not:

- Line 3693–3697 decides F3 by name, twice, in normative prose: "ranges over
  a layer's **addressed** tiles, **stored or not**" and "an addressed tile
  has one **whether or not its index entry is the sentinel**". The sentinel
  escape is closed by name.
- The summary sentence's own noun is "no **instance** of a kind" — "instance"
  is the term the paragraph's first sentence introduces and the next two
  individuate per row. It is not a free-standing word.
- "Either way" and "that row" are anaphors with no referent outside the
  paragraph, so the auditor's "read alone" reading is not a reading a
  reader can actually have.
- The diff refutes the finding's headline claim: the '-' side already read
  "a file **containing** none of a kind does not exceed that row". The verb
  was not replaced and then reverted to; the repair changed "none of a kind"
  to "no instance of a kind", which is strictly tighter.

Correction to the B-02 verifier, recorded because it matters for the record
even though it does not change the grade: its argument 4 is **wrong**. It
asserted that "§21.9 has no rows, generates no instances, and generates no
vectors — the specific downstream author the finding invokes does not
exist", citing §21.1 and §21.8. But §24 `[R-VEC-03]`, line 3992–3994, says:

> "§21.9's minimum guarantees **are exercised where a vector at the bound is
> constructible** — the tile-count guarantee is not ... and is exercised
> instead by a scaled vector spanning several segments with the bound checked
> arithmetically."

So a corpus author *does* build files at §21.9's bounds, and the finding's
harm vector (a vector author working from this paragraph) exists. It still
does not rescue the finding: the author reads the same paragraph, and lines
3693–3697 answer the question outright.

Residue: "the ... frames a file actually contains" (stored sense) sits one
sentence from "a file containing no instance" (generic sense). A lexical
wobble, inherited from the pre-repair text, resolved by the sentence above
it. Not what was reported, and not byte-level.

**B-02: does not survive as reported. Not byte-level.**

## 7. B-03 — is a frame's Window_Size a "declaration"?

The finding needs: "row 8 ranges over frames, not declarations" ⟹ "a frame
declares nothing" ⟹ `[R-ERR-04]`'s narrow-scope clause cannot reach a tile
for row 8, while `[R-COD-06]` grants exactly that.

The first entailment fails on the paragraph's own structure, and row 6 is the
proof: row 6 ranges over *addressed tiles*, not over declarations, yet its
quantity is expressly declaration-derived (`[R-SER-07]`). "Ranges over X" is
a statement about the instance population, not about whether the quantity is
declared. The finding reads the clause as doing work it does not do.

The second entailment fails on the document's vocabulary, in three normative
(non-blockquote) places I verified by opening the lines:

- §17.2 `[R-COD-06]`, ~2285 and 2292–2294: writers "MUST NOT **declare** a
  window size exceeding the tile's decoded size"; "Writers SHOULD keep the
  **declared window** within §21.9's 8 MiB `Window_Size` guarantee".
- §21.4 row T21, line 3513: "Codec 3 (zstd) and the frame **declares** a
  window size larger than the tile's decoded size | ... | reader | **tile
  use** | `[R-COD-06]`". A tile-scope row on this exact quantity.
- §21.5 prose, line 3529–3531 (not a blockquote): "declines the decode on the
  size bound or on **the frame's declared window**".

So "the narrowest scope whose declarations exceed what it can serve, a layer
or a tile" reaches the tile for row 8 on its face.

Byte-level test run anyway, on the file the finding needs:

> F4: 100 layers; one codec-3 tile in layer 7, decoded size 64 MiB (row 6 OK,
> 64 < 256), frame declares Window_Size 32 MiB (> 8 MiB, row 8 exceeded).
> `[R-COD-06]`: "a wider window is conforming". F4 is conforming.

Reader D serves everything and declines just that tile. Is D conforming?
- Under `[R-COD-06]`: yes, expressly.
- Under §21.9 alone, even granting the finding's reading that "declarations"
  cannot reach: `[R-ERR-04]`'s prohibition is "Software that declines **on
  that ground** **a file whose every quantity lies within the table**". F4's
  quantities do not all lie within the table, so D is not caught; and
  `[R-CNF-03]`'s duty does not cover F4 either. D is conforming under both.

I also ran the inverse (a reader declining F4 *whole*, which `[R-COD-06]`'s
"merely permits ... the tile or the layer" might be read to exclude):
`[R-ERR-04]` line 3705 grants "at the whole file" unconditionally for a file
exceeding any row, and `[R-COD-06]` states no MUST NOT. Conforming both ways.

No file's must-accept status moves. **B-03: does not survive. Not
byte-level.** The residue is one loose word ("declarations" where "declared
quantities" would be tighter), which the register itself already glosses.

## 8. X-08 — do the offered scopes cover every per-instance row?

This is the charter's explicit second instruction, so I ran it row by row.

| row | instance | scope offered by 3705–3707 | covered? |
|---|---|---|---|
| 6 decoded tile size | a layer's addressed tile | "a layer or a tile", reachable via declarations (`[R-SER-07]`) | yes |
| 7 document decoded size | a user-metadata document | "at the whole file" | yes — and §18.2's Note gives the same answer with the same reason |
| 8 Window_Size, in a tile | a codec-3 frame | "a tile", per §17.2/T21/§21.5 above | yes |
| 8 Window_Size, in a metadata extent | an encoding-2 frame | "at the whole file"; plus ignore-record at record scope | yes |

The finding's live point is that a user-metadata record is neither a layer
nor a tile. True — and the sentence's first alternative, "at the whole file",
covers it without needing the second. The record-scope outcome is supplied
normatively, not only by a Note:

- §21.5 prose, 3524–3532 (not a blockquote): "every way its document can be
  unreadable takes this outcome, whatever the containing scope — ... and
  except where a reader or verifier declines the decode on the size bound or
  on the frame's declared window, which `[R-MTA-09]` makes that actor's
  capability and not a fact about the file."
- §18.2 `[R-MTA-09]`, 2470–2477: "a frame declaring more than the reader
  admits is **ignore-record** on that ground ... the file exceeds a §21.9
  guarantee and so remains conforming while the reader MAY decline it
  (`[R-ERR-04]`)."

So the auditor's claim that the record-scope outcome rests on a Note is
false; §21.5 and §18.2 carry it in normative prose. I verified both by
opening the lines, precisely because "repair lives in a blockquote" is the
failure mode my charter names.

Byte-level test:

> F5: conforming, one file-scope encoding-2 user-metadata record, frame
> declares Window_Size 32 MiB, document decodes to 1 KiB, all else within.

Three reader behaviours — decode it (bound 64 MiB); ignore-record it and
serve the rest; decline the whole file — are each permitted, the first two by
§18.2, the third by 3705. All three **accept or decline the same bytes
lawfully**, and F5 stays conforming throughout. `[R-CNF-03]`'s duty has
already lapsed (a value exceeds), so nothing forces a unique answer and
nothing forbids any of them. This is a deliberate MAY, and no reading of the
repaired paragraph changes which of the three is available. Not byte-level.

### 8a. X-08's secondary prong — encoding 1 has no stated bound floor

This is the one thing in the group with residue, so I worked it separately.

Hunk 1 puts the reader's bound sentence inside the **encoding-2** paragraph
and, post-repair, ties it explicitly to that structure: "**The first
exception** holds because a document has no declared size — a reader instead
decodes with a bound of its own choosing, **no smaller than §21.9's
user-metadata guarantee**". The "first exception" is an exception to
`[R-COD-06]`, which reaches only encoding 2. Row 7 of §21.9, by contrast, is
encoding-agnostic ("decoded size of one user-metadata document").

So: is there a floor on a reader's bound for an **encoding-1 (verbatim)**
document? Test file:

> F6: conforming, file-scope encoding-1 user-metadata record, document
> 12 MiB verbatim (within row 7's 16 MiB). All other values within.

Reader E has a 4 MiB verbatim bound, ignore-records the document per
`[R-MTA-02]` ("the outcome of **every** failure to read its document is
ignore-record whatever the scope"), and serves the whole file.

Reading (i): the §21.9 guarantee floors the bound for every encoding — E is
nonconforming.
Reading (ii): the floor is stated only for encoding 2 — E is conforming,
because ignore-record is not a rejection and E has therefore *accepted* F6
as `[R-CNF-03]` requires.

The X-08 verifier closed this with "`[R-CNF-03]` at 162-164 ... a reader
whose verbatim-document bound sat below 16 MiB would already be
nonconforming". That inference requires "MUST accept the file" to entail
"MUST decode the document", which the document does not say — and §18.2 shows
the drafters knew the entailment needed stating, because they stated it for
encoding 2. `[R-CNF-03]`'s other hook, "software that declines to support ...
an assigned user-metadata encoding is not a conforming reader", is about
supporting the *encoding*, which E does.

So the prong is real: the answer exists only as reasoning outside the text.
**But it is not byte-level.** E accepts F6; a reader under reading (i)
accepts F6. No file's accept/reject verdict moves, no byte is emitted
differently, and the emittable set is untouched. What differs is only whether
one particular reader carries the label "conforming", and only in a case
where its externally visible file-level verdict is identical. Under the
charter's stated discriminating test that is a miss.

Note also: this prong is **inherited**, not introduced. The '-' side of hunk
1 read "The constraints §17.2 states against a tile's declared decoded size
do not apply, because a document has no declared size — a reader instead
decodes with a bound of its own choosing...", equally inside the encoding-2
paragraph. Hunk 1 did not create the gap; if anything, "The first exception"
makes it slightly more visible.

## 9. Greps run, verbatim

```
$ grep -n "R-COD-07" spec/tarn.md
2326, 2783, 3005, 3479, 3515, 3694, 3741
$ grep -n "R-SER-07\|R-COD-06\|R-MTA-09\|R-ERR-04\|R-ERR-03" spec/tarn.md
163, 201, 203, 1923, 2226, 2292, 2296, 2342, 2458, 2477, 2486, 2501,
2509, 2787, 2832, 3437, 3495, 3505, 3509-3514, 3531, 3546, 3614, 3679,
3715, 3777, 4353
$ grep -n "21\.9" spec/tarn.md
49, 163, 277, 2293, 2468, 2473, 2476, 2503, 3327, 3669, 3992, 4100,
4159, 4352
$ grep -n "per-instance\|actually contains\|no instance of a kind\|narrowest scope\|remains conforming, and a reader MAY\|Superseded payload bytes\|no conformance requirement\|MUST NOT interpret it\|minimum guarantees are exercised" spec/tarn.md
633, 634, 663, 2130, 3568, 3692, 3700, 3701, 3705, 3706, 3993
```

Note on grep hygiene, per the charter's warning: "Superseded payload bytes"
returned **nothing** line-oriented because §3.1 wraps between "Superseded"
and "payload"; and "addressed tiles, stored or not" returned nothing on the
flat copy because of the `**addressed**` emphasis markers. Both were
recovered from the whitespace-normalised copy / by opening the range. No
conclusion below rests on a failed grep.

Flat-copy phrase probes run (each with 60–80 chars of context, output read):
"per-instance", "actually contains", "no instance of a kind",
"minimum guarantee", "MUST accept", "Window_Size", "compressed frame",
"decline", "Superseded payload bytes from earlier generations",
"unqualified *stored* means".

## 10. Bottom line

All four downgrades hold on the byte-level question, but not always for the
reasons given:

- **B-01** — closed, by §5.2's "no conformance requirement applies to it",
  not by §3.1's tile-scoped "stored" definition. The verifier's `[R-CNT-14]`
  argument is a reductio, not a closure.
- **B-02** — closed by lines 3693–3697; its headline claim is contradicted by
  the diff. The verifier's §21.8/vector argument is **wrong** ( `[R-VEC-03]`
  line 3993 does put vectors at §21.9's bounds), but the grade survives.
- **B-03** — closed by §17.2, §21.4 T21 and §21.5, all normative; the
  finding's first entailment is refuted by row 6's own structure.
- **X-08** — main prong closed by "at the whole file" plus §21.5's and
  §18.2's normative ignore-record. Secondary prong (encoding-1 bound floor)
  is a real, small, inherited gap answered only by an inference the document
  does not make — not byte-level.

I built five files (F1–F6) trying to move the emittable or must-accept set
and none of them moved it. Verdict: DOWNGRADE_STANDS.
