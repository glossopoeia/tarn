# Round 20 triage — skeptic pass — working transcript

## Access disclosure

Read: `spec/tarn.md` in full (all 4369 lines, in chunks: 1–400, 400–900,
900–1400, 1400–1900, 1900–2400, 2400–2950, 2950–3200, 3232–3400,
3400–3560, 3560–3720, 3757–3830, 3897–3990, 3984–4040, 4158–4300,
4298–4369). Ran two mechanical checks over it (below). Read **no**
transcript at all — not the six walk transcripts, not the quiz
transcripts, and certainly no `transcript-triage-*.md`. I did not list
the round20 directory. Every quotation below is from `spec/tarn.md`.

## Mechanical checks run

1. **Register instance arithmetic** (decides diagrams-01 / register-01).
   Parsed every row of §21.2–§21.5 from the Instances cell, counting a
   cell reading `—` as one instance and otherwise counting
   semicolon-separated items:

   ```
   conditions: 121   instances: 273
   F 36 rows / 58 instances;  L 49 / 116;  T 26 / 55;  R 10 / 44
   L14 = 3 instances;  R7 = 6 instances
   ```

   §21.8 publishes "121 conditions over 273 instances". The published
   figure is therefore reachable **only** by trusting the Instances
   cells. diagrams-01's recomputation is correct and its reading (a) is
   the one the document's own total requires.

2. **`grep -n "logically modif"`** → one hit, line 3105, inside
   `[R-WRT-05]`. The phrase is used once and defined nowhere.
   writer-01's premise checks out.

3. `grep -n "requested channel"` → line 2790 only (§19.4 step 2);
   `Channel-subset` → line 2839 (closing note). §19.4's request
   vocabulary ("A **point request** names a single coordinate (§3.1); a
   **region request** names a rectangular range of coordinates, one
   interval per dimension") mentions no channel. reader-02's premise
   checks out.

4. `grep -n "MUST accept at least"` → line 3659, §21.9's table **column
   header**. This is the sentence adversary-02 says does not exist.

---

## Groups, and the sentence I hunted for in each

### 1. `carve-out-scope` — reader-01 + quiz-01

Same defect from two reporters: §2.3 `[R-CNF-03]`'s acceptance carve-out
is written over "record" with no scope qualifier, so read alone it
appears to release a reader from any duty toward a conforming file whose
*sub-record* is an unimplemented experimental MU = 1 type.

Tried to kill it: I looked for a scope qualifier in §2.3 itself. There is
none — the words are "carrying no record of a type it does not implement
with MUST_UNDERSTAND = 1". The defect is real.

Tried to make it byte-level: could a reader lawfully refuse the file?
No, twice over.

- §7.4 `[R-CNT-18]`: "an unknown sub-record type with MU = 1 is
  reject-layer, and where the file is otherwise conforming a reader MUST
  NOT reject the file for it".
- §21.6 closing: "the same type as a layer sub-record is reject-layer and
  never a ground to refuse the file (`[R-CNT-18]`), so only the top-level
  case is a file a reader refuses".
- The only general licence to reject runs to nonconforming files:
  `[R-CNF-12]` "For a nonconforming file no acceptance obligation
  exists — a reader MAY reject it upon detecting any violation".

Withholding a duty is not granting a permission, and §2.1 gives an
absence no force. Both reporters got this right. **Byte-level: no.
Editorial.** Repair: one qualifier — "no *top-level* record".

### 2. `channel-selection-undefined` — reader-02

§19.4 defines requests over coordinates only, then uses "requested
channel" four times. Tried to find the definition: it is not in §19.4,
not in §3.1's *channel* entry, not in `[R-RDR-04]`. Absence confirmed by
grep. The defect is real.

Deciding sentence for the substance (reading (c), not (b)): §3.2
`[R-MDL-02]` — "a conforming reader that reads any portion of a layer
MUST return **exactly** the corresponding portion of the reference
array". A one-channel request against an interleaved sentinel tile that
returns C fill values returns more than the corresponding portion.
Reading (b) is foreclosed.

Byte-level: no. Nothing about accept/reject; nothing about emitted
bytes; §14.1/§14.2 fix the stored value sequence without reference to
any request; and `[R-VEC-02]` records "the decoded content a reader is
to return from every scope it can read" — a scope's full content, not a
per-request projection, so no vector separates the readings.
**Editorial.**

### 3. `bool-return-byte` — reader-03

Reporter: `[R-SER-08]` fixes a truth value, not a returned byte.

Tried hard to kill it, and mostly succeeded on the framing, not on the
residue. The reporter's "step 8 frames returns as bit patterns" is
answered by step 8's own parenthetical: "Return the requested values'
bit patterns unaltered … — for every byte **a conforming file can
carry**, the whole of this step (`[R-SER-08]` fixes what a reader
returns for the one byte a conforming file cannot)." Step 8 expressly
excepts the malformed byte from "unaltered".

Two further sentences the reporter did not reach, which decide the
residue outright:

- §21.1: "`[R-SER-08]` is the one rule that goes the other way: it
  **resolves** a nonconforming interleaved boolean byte to a value
  **rather than serving it through**".
- Appendix H: "the sole resolved byte being a nonconforming interleaved
  boolean it chooses to return rather than reject".
- §12.3 `[R-TYP-04]`: "the one case where a reader resolves a byte to a
  value rather than passing it through arises only in a nonconforming
  file, and `[R-SER-08]` states it."

"Rather than serving it through" rules out handing back 0x37, and §14.2
gives true exactly one encoding ("a bool value … as a single byte,
0x00 = false, 0x01 = true"). So 0x01 it is.

Byte-level: no. Writer side is an unambiguous MUST NOT ("Writers MUST
NOT emit any byte other than 0x00 or 0x01 as an interleaved bool
value"), the detector is the verifier, and the reader "is not obligated
to screen decoded content". **Editorial**, and arguably nothing needs
doing at all; at most a parenthetical "(0x01)" in `[R-SER-08]`.
Graded **CONFIRMED** because the reporter reaches the right answer and
the residue is real, though smaller than the title implies.

### 4. `appender-relocation` — writer-01

Two halves, both verified against the text:

- The clause "relocating a live index region is compaction's operation
  (§20.5, `[R-WRT-07]`), not an appender's" carries no BCP 14 keyword,
  and §2.1 binds them "when, and only when, they appear in all
  capitals".
- "logically modify" occurs exactly once (grep) and is undefined.

Tried to kill it with `[R-WRT-05]`: "an updater MUST re-emit
byte-identically — header, inline payload, **and extent slot** — every
record it retains and does not logically modify". That closes the
untouched-layer case with an all-caps MUST. It does **not** close the
case the reporter actually raises — a layer record the commit *does*
modify (rename, fill change on a tile-less layer, clearing a slab
declaration, all three named in §20.3's shape (c)). For that case I
searched §20.3, §20.4, §20.5, §9.1, §5.2 and found nothing with a
keyword. Absence confirmed. Nor is the obligation listed in §21.7's
inventory of unwitnessed obligations — I read that list line by line.

Byte-level: **no**, and here is the premise, stated so it can be
attacked. *A relocated live index region is byte-indistinguishable in
the output from a freshly emitted one, so a verifier handed either
output alone reaches the same verdict under either reading; and
`[R-CNF-02]` makes file conformance "a pure predicate on bytes: it does
not depend on any reader, writer, or environment", so no file's
conformance can turn on which operation produced it.* What forks is
which of two conforming outputs a conforming appender may produce, which
`[R-CNF-05]` already licenses in general: "two conforming writers given
identical input MAY produce different conforming files." Attack this by
producing a single-file witness of the relocation; I could not.

**Design-decision** — the maintainer must choose: give the clause a MUST
NOT and add it to §21.7, or delete it and say an appender that modifies
a layer record MAY re-place that layer's index region. Either way
"logically modify" needs a definition, since `[R-WRT-05]`'s MUST is
keyed on it.

### 5. `step2-drop-prohibition` — writer-02

§20.3 step 2's "MUST NOT drop the record (§20.4)" against §20.4's
conditional licence. Verified both texts verbatim.

Tried to kill it and found the parallel that decides it — §20.5, on a
compactor meeting a detected violation: "it can neither re-emit the
structure corrected (`[R-WRT-05]`), nor keep it and call the output
clean. **Dropping is the one disposal that answers, and only where
§20.4's table licenses it.**" Plus `[R-CNF-06]`: an updater "MUST honor
the preservation obligations of §20.4", making §20.4 the authority; plus
§2.4's preserve-verbatim row, which names only "its MU = 1 and MU = 0 /
PE = 1 rows", leaving MU = 0 / PE = 0 outside preserve-verbatim
entirely. Reading B is the only coherent one, so the divergence is
smaller than an ambiguity — but step 2's words are genuinely unqualified
and a careful implementer can land on Reading A.

Byte-level: no. Premise: *the two outputs are two different byte
sequences, and each one's verdict is fixed by its own bytes under either
reading — the retained-defect output is nonconforming either way (F26
fires on it), the dropped output is conforming either way. Nothing makes
one fixed sequence's verdict depend on the reading.* §20.1
`[R-WRT-01]`: "a violation latent in a structure they neither modify nor
rely on travels with it, and certifying the whole file is a verifier's
office." **Editorial**: "…and MUST NOT drop the record except as §20.4
licenses."

### 6. `appendix-g-unpinned-declarations` — writer-03

Verified: §11.3 Note — "Tile extents are a writer's choice, and this
specification imposes none"; `[R-SER-06]` leaves layout to the writer;
§14.4 Note — "⌈P/8⌉ packed bytes planar versus P bytes interleaved".
Both satisfy item 5's own three-part test, and neither appears in items
1–10 or the closing paragraph. Read all ten items to confirm.

Tried to kill it with the reporter's own Reading A — that tiling and
layout are caller input, not writer freedom. **The refutation is inside
item 5 itself**: the same item pins "No declared alignment and no slab,
or fixed declared values" and "A fixed filter value". Alignment, slab
and filter are *layer-record declaration fields*, exactly like layout and
tile extents. A profile that pins three declaration fields and leaves two
others free cannot be resting on "declarations are input". So Reading A
fails and the list is incomplete by its own test.

Byte-level: **no**, flatly. Appendix G is "non-normative" per §2.1's
exception, and says of itself "It adds no requirement to any actor: a
writer ignoring it is fully conforming." **Editorial**: add tile
extents, layout, and declaration order to item 5, or state at the head
of the appendix that the profile takes the layer's declarations as given.

### 7. `partial-total-relief-scope` — verifier-01

Verified: `[R-CNT-21]`'s relief names "§6.2's ordered validation";
`[R-CNT-06]`'s ordered list does **not** contain the 128-byte minimum or
the front-block equality check; §21.2's preamble itself distinguishes F6
as placed by `[R-CNT-04]` "before other processing" — so the document
knows F6 is outside §6.2 and the relief still cites only §6.2.

Tried to kill it. Two sentences do most of the work but not all:

- `[R-CNT-21]` first sentence: "a verifier **that reaches a live state**
  MUST report the total number of slack bytes". The reporting duty is
  conditioned on reaching a live state; a stop at F6 or F5 never reaches
  one, so no duty attaches for the partial rule to modify.
- The definition itself: "A partial total is **F less the bytes claimed**
  by the claimants the walk did enumerate" — with no validated trailer
  there is no F, so the definition yields nothing.
- §9.7: the walk runs "From the live trailer".

That is enough to make reading (a) the right answer, but it is not
enough to make the *citation* right: the relief's stated trigger is a
section that does not contain either check. The defect survives as an
imprecision. Byte-level: no — both readings hold the file nonconforming,
and §2.3 says of the sibling report channels that they "constrain the
report and not the verdict". **Editorial**: extend the relief from
"§6.2's ordered validation" to any rejection established before a live
trailer, naming `[R-CNT-04]` and `[R-CNT-27]`.

### 8. `unassigned-type-extent-not-named` — verifier-02

Verified `[R-SEC-04]` sets both residues side by side and states the
naming remedy only for the metadata one; verified `[R-MTA-10]`'s MUST
("it MUST report each record it ignored on this ground, naming the
owning scope, the encoding value, and the stored extent length");
verified §8.1's map gives an unassigned-type extent no checksum and §7.2
leaves it opaque; searched §2.3, §9.7, `[R-CNF-11]`, §21.7 and Appendix
H for a parallel duty and found none. Absence confirmed — which, per my
instructions, is the strongest evidence for the finding.

The reporter's reading (a) is right on the keywords: §2.3's report duty
runs to requirements "it was unable to check on a capability or resource
ground", and no requirement attaches to those bytes at all. So there is
no MUST, and no ambiguity — the gap is in what the certificate can say.
Byte-level: no. **Design-decision**: either add a parallel report duty
(cheap, and §22.3's stated operator policy depends on it), or say
expressly that none is owed.

### 9. `condition-cells-under-state` — diagrams-01 + register-01

Grouped: both report Instances cells enumerating an alternative the
Condition cell does not state, against §21.1's instance rule.
diagrams-01 reports L14 and R7; register-01 reports R7 alone. One
defect, one repair shape.

Verified L14 (Condition states 2 alternatives, Instances names 3,
including "trailing residue"), R7 (Condition states 2, Instances names
3 × 2 containers = 6, including "leading U+FEFF"), and §21.1's rule
("one of several alternatives **the condition text states**"). Verified
that F29 — L14's file-scope twin — gets it right: "or bytes remain after
the last complete record". Verified `[R-CNT-18]` states residue
separately and `[R-MTA-04]` states the BOM separately, so neither third
alternative is subsumed.

Tried to kill it with §21.1's "where a row and the rule it cites diverge,
the rule governs" — that decides the *reader behaviour* (residue →
reject-layer, BOM → ignore-record) but not the *instance arithmetic*,
which §21.1 makes "mechanical once the cell is written". My own count
(121/273) matches §21.8 exactly, so the Instances cells are the ones the
published total rests on and the Condition cells are the defective half.
Byte-level: no — quoted rule above. **Register-bookkeeping**: extend
L14's and R7's Condition cells.

Note a small arithmetic slip in diagrams-01: a builder working from the
Condition cells finishes **three** short of 273 (1 for L14, 2 for R7),
not four.

### 10. `appendix-a-local-reader` — diagrams-02

**REFUTED**, and by the sentence the reporter truncated. Appendix A
reads, in full:

> "A local reader additionally verifies bytes [0, 16) by equality first,
> which `[R-CNT-04]` requires of **any reader holding them** — as a
> remote reader does too whenever its speculative suffix window reaches
> offset 0, which on this 128-byte file means a window of the whole
> file. A shorter window can still spare the second request: 112 bytes
> covering [16, 128) contains the directory, so §6.4's containment test
> applies, **while bytes [0, 16) stay non-resident, so §6.1 leaves the
> front-block check to the reader**."

The passage does not attach the obligation to transport class. It names
locality as an instance, states the residency test in the same sentence's
relative clause, extends it to a remote reader whose window reaches 0,
and then works the case of a resident-directory / non-resident-front-block
reader. That is §6.1's rule stated correctly and applied three ways. The
reporter's reading (a) is not a charitable rescue; it is what the text
says. Byte-level: no (also non-normative per §2.1). **Severity: none.**

### 11. `note-4-7-miscounts-columns` — diagrams-03

Verified §7.4's table columns: Field | Type | Constraint — so measured
against the Note's six-item list it omits offset, **size**, and class,
where the Note says "the offset and class columns". Verified §7.2's five
Field cells: two of five carry a range, and the extent slot's range lives
in `[R-CNT-13]`'s prose, where the Note says "§7.2 folds **each** field's
range into its Field cell". Verified the Note's third claim *is* right:
§6.1's table is Offset | Size | Value | Class, so "a Value column
replaces type and range" holds.

Tried to kill it with the Note's own hedges — "each table giving the
columns its structure needs", and the six-item list being scoped to
"Layout tables for **fixed-layout** structures", which §7.4's packed
payload is not. Those excuse the *tables*; they do not make the Note's
two specific claims about those tables accurate. Byte-level: no — §2.1
excepts "any text labeled *Note*", and every size §7.4 omits is
recoverable from its Type cell while every range §7.2 omits is stated in
the following requirement. **Editorial.**

### 12. `sec-21-6-experimental-entry` — register-02

Verified the entry, verified `[R-WRT-08]`'s own sentence ("An updater
MUST NOT re-encode a record whose type it does not implement, and MUST
NOT modify one except by relocating its extent and re-pointing its slot
under §20.5" — nothing about preserving or dropping), verified §20.4's
qualifier the entry drops ("For a type the updater implements that this
specification does not register, the definition it implements the type
from supplies the flags, and **the stored bits never do**"), and verified
that L25's own Governing-rule cell cites `[R-CNT-15] (R-CNT-18)` while
the §21.6 entry cites `[R-CNT-15]`, `[R-WRT-08]` only.

Tried to kill it with §21.1: "§21.6's entries restate their governing
rules on the same terms a row does, and where such an entry and the rule
it cites diverge, **the rule governs there too**." That forecloses the
byte question completely — an updater that follows §20.4 rather than the
entry takes the flags from the definition it implements the type from.
But it does not excuse the entry: §21.1 puts §21.6's entries under the
register's discipline precisely so they can be audited against their
rules, and this one diverges from its rule on the qualifier that decides
the case.

Byte-level: no — and note that both dispositions produce conforming
outputs (a record retained byte-identically, and a record dropped with
its extent becoming slack), so nothing moves in or out of the conforming
set either. **Register-bookkeeping**: restore the not-implemented
qualifier and cite `[R-CNT-18]` alongside `[R-CNT-15]` for the L25 half.

The entry's identifier pin is the same root as adversary-03 and is
graded there.

### 13. `sec-21-7-trailer-obligation-count` — register-03 + quiz-02

Same defect, two reporters. Verified `[R-WRT-06]` places four things on
a compacted output's trailer — fresh file_id ("a new draw under §9.3's
randomness advice, not merely a value compared against the input's"),
generation 1, carried ignore-lane bits, version_minor floor — and that
§21.7 says "§20.5's **two** obligations on a compacted file's trailer".
Verified §20.5's answering sentence, "Neither obligation has a witness in
the output alone (§21.7)", sits immediately after the version_minor
sentence and so refers to the same pair — the two sites agree with each
other and disagree with §20.5's own list.

Tried to kill it: the fresh draw genuinely has no output-alone witness
(a file_id is a value, and the rule binds the draw), and generation 1 has
none *as a compaction obligation* — an output at generation 5 is visibly
generation 5, but nothing in it says it was a compaction — though §21.7
already names `[R-LIF-03]`'s generation sequence, which absorbs it. So
the definite description is genuinely short.

Byte-level: no. §21.1: "neither this completeness clause nor the
instance arithmetic below reaches … §21.7's account of what no check
detects" — so an omission from §21.7 is not a missing register row, and
under either reading the obligations have no witness. **Editorial**:
drop the numeral, or add the fresh file_id.

### 14. `f5-preamble-justification` — register-04

Verified: `[R-CNT-06]`'s ordered list contains no 128-byte minimum;
`[R-CNT-27]` in §5.1 states the check with no placement; §19.1 step 1
obtains F but never mentions the check; F5's Detected cell is "open";
§21.2's preamble names F6 as an exception by `[R-CNT-04]`'s placement
and does not name F5.

Tried to kill it and half succeeded. The preamble's *conclusion* about
F5 is right for a reason the preamble also states — "Four rows are
outside that reasoning and do reach it, because their subject is **a
field fixed across every major** (`[R-CNT-24]`)". The 128-byte minimum
is not such a field, so F5 correctly does not reach a foreign-major
file. And §2.3 forecloses the verdict outright: "a file declaring another
major **is neither conforming nor nonconforming under it** … and that
refusal is not a finding about its bytes." A verifier may not print
*nonconforming*, whatever its check order.

What survives is exactly what the reporter says: the *stated* mechanism
("§6.2 puts the version gate ahead of every check but…") does not cover
a check that is not in §6.2 at all, and F5 is not named as F6 is.

Byte-level: no — §2.3's sentence decides the verdict, and I also checked
reachability: 64 ≤ F < 128 with F mod 64 = 0 admits only F = 64, where
dir_offset ≥ 16 and dir_offset + dir_length ≤ F − 64 = 0 cannot both
hold, so some other row fires in every case. **Register-bookkeeping**.

### 15. `metadata-zstd-window` — adversary-01  *(the one I fought hardest)*

The only self-flagged byte-level finding. I tried to sustain it and could
not, and I am recording the premise of the downgrade in full because
this is exactly the shape round 16 got wrong.

Verified the construction is available: `[R-MTA-09]` withdraws §17.2's
window constraint ("The constraints §17.2 states against a tile's
declared decoded size do not apply, because a document has no declared
size") and carries over only four constraints — "the frame magic; no
skippable frame and no second frame; no nonzero dictionary ID; no
content-checksum flag". §17.2's writer SHOULD on the window is scoped to
tiles ("even for a larger tile"). So a metadata frame may declare any
Window_Size, and no writer guidance steers it. That half of the finding
is **confirmed**, and it is the substantive half.

Verified the reporter's Reading (a) has real textual pull: §21.5's
preamble says "every way its document can be unreadable takes this
outcome … as a violation in the rows below, except at an
experimental-range encoding … and except where a reader or verifier
declines the decode **on the size bound**" — and the size bound is the
16 MiB decoded-document bound, not the window. `[R-CNT-25]` likewise
lists "a decode failure" flatly.

Four sentences kill it anyway, and the reporter quoted none of them:

1. §21.9 `[R-ERR-04]`: "**A file exceeding any of these remains
   conforming**, and a reader MAY decline it". "These" is the minimum-
   guarantee table, whose rows include "zstd frame `Window_Size` | 8
   MiB", unqualified as to tile or document. The 1 GiB-window file is
   conforming, full stop.
2. §21.9 `[R-ERR-04]`: "a refusal on resource grounds **MUST be reported
   as a resource limit and not as a validity error**: … a reader that
   reports 'too large' as 'corrupt' invites the deletion of intact data."
   R3 is a validity error. Verifier A is forbidden from reporting it.
3. §2.3 `[R-CNF-02]`: "File conformance is a **pure predicate on bytes**:
   it does not depend on any reader, writer, or environment." §21.1 makes
   the register an enumeration of file-conformance violations. So R3's
   "fail to decode" cannot mean "fail to decode *in this reader*"; it
   must be a property of the bytes, which these bytes do not have.
4. §2.3's cannot-establish list names "when it declines to decode a
   user-metadata document (`[R-MTA-09]`)" — without restricting it to
   the size bound.

And the tile side draws the identical line explicitly, which is the
structural analogy: §17.2, "a wider window is conforming and merely
permits a conforming reader to decline the tile or the layer on resource
grounds (`[R-ERR-04]`)" — T25 ("malformed stream that fails to decode")
and a too-wide window are separate things there, and R3 is T25's
counterpart.

**Premise of the downgrade, stated for attack:** *§21.9's Window_Size row
reaches a zstd frame carried in a user-metadata extent and not only one
carried in a tile.* If that is wrong — if the Window_Size guarantee is
tile-only — then the adversary's file exceeds no guarantee, `[R-ERR-04]`'s
resource-limit sentence never engages, and the R3 question reopens as a
genuine byte-level fork. I checked three things against it: the table row
carries no qualifier; `[R-MTA-09]` itself sends a metadata reader to
§21.9 for its bound; and `[R-CNF-03]` reads the table file-wide, "none of
whose **values** exceeds the minimum guarantees". I am satisfied, but a
maintainer who reads the row as tile-only should overturn this to
byte-level.

Graded **PARTIAL**: the writer-side gap and the under-inclusive exception
list in §21.5's preamble are real; the claim that the verdict is
undetermined is not. **Design-decision**, because the repair has a
maintainer choice in it: mirror §17.2's sentence into `[R-MTA-09]` ("a
wider window is conforming and merely permits a reader or verifier to
decline on resource grounds"), widen §21.5's preamble's second exception
from "the size bound" to any resource ground, and decide whether to add
a writer SHOULD steering metadata frame windows to 8 MiB. Worth doing
precisely because the natural implementation — map the decoder's error
return to R3 — gets it wrong.

### 16. `metadata-bound-floor-keyword` — adversary-02

**REFUTED.** The reporter says the 16 MiB floor "carries no BCP 14
keyword", searched `[R-MTA-09]` and `[R-ERR-03]`'s prose sentence, and
concluded that only "accept" is capitalised. The capitalised sentence
they want is the **column header of §21.9's own table** (line 3659):

> | Quantity | **A conforming reader MUST accept at least** |
> | … | … |
> | decoded size of one user-metadata document | 16 MiB |

That is an all-caps MUST reaching exactly the behaviour: a reader must
accept at least a 16 MiB decoded user-metadata document. A reader with a
1 KiB bound has not. `[R-ERR-04]` says the same again in prose — "the
guarantees are the floor, not a suggestion" — and §2.5 `[R-CNF-10]`
forbids a limit that "affects … which files a conforming reader accepts"
to live "only in an implementation".

The reporter's chosen reading (a) is right; the premise that no
capitalised sentence supplies it is wrong. Byte-level: no, and the
reporter agrees. **Severity: none.** Optional nicety only: `[R-MTA-09]`
could read "a bound of its own choosing, which MUST be no smaller than
§21.9's user-metadata guarantee" — but nothing is undetermined without it.

### 17. `sec-20-4-table-identifier` — adversary-03

Verified the block sits between `[R-WRT-05]` and `[R-WRT-08]` with no
marker of its own, and verified the cells carry live keywords ("The
updater MUST NOT modify the scope the record governs"; "An appender MUST
NOT drop it except in a commit that *independently* changes the scope…";
"a commit whose only effect would be the drop MUST retain it"; "A
compactor MAY drop it whenever it rewrites the file"; "SHOULD report the
loss").

Tried to kill it, and it partly dies. The reporter rejects the
"`[R-WRT-08]` covers the run" reading on the ground that `[R-WRT-08]`'s
own final sentence is about re-encoding and relocation. That test is not
the document's: identifiers here routinely terminate multi-paragraph runs
whose final sentence is not the whole requirement — `[R-WRT-04]` closes
six numbered steps with "barrier; pad; trailer with generation one
greater…"; `[R-CNF-11]`, `[R-CNT-21]` and `[R-LIF-08]` do the same. And
§21.6's fifth entry positively asserts the reading, citing `[R-WRT-08]`
for "preserved or dropped per its PE bit".

So a citation handle exists; what is missing is any statement of where
the block begins. §2.2 gives no placement rule at all, which is the real
gap. Byte-level: no — the obligations bind either way (capitalised
keywords under `[R-CNF-01]`, plus `[R-CNF-06]`'s "MUST honor the
preservation obligations of §20.4" and §2.4's preserve-verbatim row).
Graded **PARTIAL**. **Design-decision**, because §2.2 makes minting an
identifier a one-way door: either declare that `[R-WRT-08]`'s block
begins at "Persistence governs every record type" (cheapest, and what
§21.6 already assumes), or mint one for the table.

---

## Coverage check

20 input ids; 17 groups. Union of member_ids, sorted, against the input
list, checked by hand item by item:

adversary-01(15), adversary-02(16), adversary-03(17), diagrams-01(9),
diagrams-02(10), diagrams-03(11), quiz-01(1), quiz-02(13),
reader-01(1), reader-02(2), reader-03(3), register-01(9),
register-02(12), register-03(13), register-04(14), verifier-01(7),
verifier-02(8), writer-01(4), writer-02(5), writer-03(6).

20 ids, each in exactly one group. Merged groups: {reader-01, quiz-01},
{diagrams-01, register-01}, {register-03, quiz-02}. All others singleton.

## Byte-level tally

**Zero** groups graded byte-level. The reporters flagged one
(adversary-01); I downgraded it with the premise stated above and four
quotations. Groups I tried hardest to kill and failed: verifier-02
(no parallel naming duty — searched six places, absence confirmed),
writer-01 (no keyword and no witness — searched §20.3/§20.4/§20.5/§21.7),
and the substantive half of adversary-01 (no writer guidance on a
metadata frame's window — confirmed by reading `[R-MTA-09]`'s carry-over
list). Groups I killed: diagrams-02 (refuted by the sentence the reporter
truncated) and adversary-02 (refuted by §21.9's table column header).
