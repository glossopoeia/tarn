# Advocate B — working transcript

Access: spec/tarn.md only, via grep/sed/awk. No docs/, no git, no conformance/, no web.

## 0. Quotation check

Sentence A — spec/tarn.md lines 3005–3011, verbatim:

> The test is the effect on such a tile, and the list names where that effect
> arises rather than standing on its own: a change that leaves every one of
> those tiles' stored bytes meaning exactly what they meant — a filter whose
> mandated stride makes it the identity (`[R-COD-10]`), or a new padding
> position whose stored byte already holds the fill `[R-SER-05]` fixes — is not
> what this bars.

The charter's rendering drops the citation `(`[R-COD-10]`)`. Nothing else differs.

Sentence B — lines 3041–3045, verbatim, matches the charter exactly.

Both sit in §20.3 step 4's normative prose (no `>` prefix; §2.1 `[R-CNF-01]`).

## 1. The operative rule, in full (lines 2994–3001)

> A commit MUST NOT change a layer's declarations in a way that alters, for any
> tile that layer stores **in the generation this commit supersedes**, what §14
> fixes for its stored bytes or how they decode — the set of padding positions
> (§11.3) and the content `[R-SER-05]` fixes there, the decoded size, the byte
> offset of any sample within the decoded tile image, or the codec and filter
> that produced the stored bytes.

Four enumerated conjunct-terms. Term 1 is a CONJUNCTION: "the set of padding
positions (§11.3) **and** the content `[R-SER-05]` fixes there."

## 2. The surplusage argument (my strongest)

What can alter "the set of padding positions" of a prior-generation stored tile
WITHOUT also altering a later term?

- tile extent Tᵢ change → alters P and decoded size (term 2). Covered elsewhere.
- rank / dimension order change → alters in-tile byte offsets (term 3).
- layout or channel-set change → alters decoded size (term 2).
- extent Eᵢ **grow** → alters the padding set only. EXPRESSLY PERMITTED, line 3022.
- extent Eᵢ **shrink** → alters the padding set only. THE DISPUTED CASE.

So term 1's only independent application is grow-or-shrink, and grow is carved
out by its own express MAY. If Sentence A's second illustration governs, term 1
of a normative enumeration names nothing at all. Under Reading B it names
exactly one thing, and Sentence B names it back.

## 3. The express-growth argument

Line 3022–3024: "an extent MAY **grow**, since a position that becomes real held
that channel's fill and fill is a legal sample value".

Under Reading A this MAY is dead letter. Growth's newly-real position holds fill,
the stored byte does not change, and by Reading A's own reasoning the byte
"means" what it meant — Sentence A, three lines earlier, would already permit it.
A drafter does not grant an express permission, with its own justification and
its own proviso list (L44, `[R-ENC-04]`), for something the immediately preceding
sentence has just excepted. The express MAY presupposes that a padding-set change
is otherwise barred.

Note also the asymmetry the growth justification relies on: growth RELEASES a
§14 constraint on a byte (constrained-to-fill → free sample). Shrink IMPOSES one
on a tile `[R-LIF-01]` has frozen. That the frozen byte happens to satisfy the
new obligation is accidental; the bar is about what obligation attaches, not
about today's luck.

## 4. Sentence A's own criterion excludes the disputed case

The criterion Sentence A states is "leaves every one of those tiles' stored bytes
**meaning** exactly what they meant." It cannot mean "the bytes are unchanged" —
every commit the bar reaches leaves the bytes unchanged; that is the bar's whole
complaint ("a change that reads like a directory edit", line 3016). So "meaning"
is semantic: what §14 makes of the byte.

- Identity filter: byte is the same sample, at the same in-tile offset, decoding
  the same way. Criterion satisfied.
- Real → padding: the byte stops being a sample and becomes content §14.5
  constrains and `[R-GEO-04]` forbids a reader ever to return. §13.3's Note is
  explicit that these are two different mechanisms. Criterion NOT satisfied.

Reading B does not strike Sentence A. It strikes Sentence A's second
illustration, which contradicts the criterion the same sentence states. Reading A
must instead read Sentence B's flat "is barred" as carrying an unwritten
exception.

## 5. Cross-site propagation — every other site restating the rule

(a) §23.1, line 3932–3934, NORMATIVE prose (no blockquote), `[R-PRV-01]`:

> A commit removes sample data two ways — superseding it, and a shrink that
> de-addresses tiles (§20.3 step 4) — and a dropped ancillary record's extent
> (§20.4) goes the same way

"Two ways", closed enumeration, citing §20.3 step 4, naming the shrink species as
the DE-ADDRESSING one. Under Reading A there is a third way: a shrink that
de-addresses no tile and converts a real position of a surviving stored tile into
padding, making that sample unreachable. §23.1 is then simply wrong. Under
Reading B it is exactly right.

(b) §11.1 Rationale, lines 1484–1490 — NON-NORMATIVE (`>` block, `[R-CNF-01]`),
so no force; evidentiary only:

> §20.3 states normatively, and governs, what a commit may do to a layer that
> already stored tiles in the generation a commit supersedes: a shrink is barred
> wherever it alters what §14 fixes for such a tile — whether or not the new
> state still stores it — and permitted where it **only** drops tiles out of the
> addressed set

Carries Sentence B's distinctive qualifier verbatim; the permission is exclusive
("only drops tiles"); Sentence A's carve-out is absent.

(c) §20.3 line 3048–3051, normative: "Where a shrink is permitted the
de-addressed tiles' extents become slack, `[R-CNT-17]` obliges the smaller
entry_count and so a re-emitted index region, and **every surviving stored tile
is untouched**." The disputed commit de-addresses nothing, lowers no
entry_count, re-emits no index region, and does touch a survivor's
position classification. It has none of the shape the document says a permitted
shrink has.

(d) §20.3 line 3036–3040, normative: dropping a tile out of the addressed set
"neither does it rescue a commit that damages a prior-generation stored tile."
In a shrink, the only thing that can "damage" a survivor is the real→padding
conversion.

(e) §21.7 line 3685–3689, normative: the bar is "witnessed only where the
affected tiles remain stored, and then only for part of what it bars. A change
reaching a byte §14 structurally constrains — a padding position, a pad bit, or
an interleaved boolean — fires §21.4's content rows." §21.7 treats a change
reaching a padding position as within the bar, with no fill-valued carve-out.
Note §21.7 DOES hedge explicitly for the filter/offset family ("where it breaks
neither there is no witness") — so its silence for the padding family is not a
drafting habit. Honest caveat: under Reading B §21.7 is incomplete about
witnesses in the disputed case; under Reading A it is wrong about scope.

**Propagation test.** Sentence B's content appears at four other sites (§11.1,
§21.7, §23.1, and twice more inside §20.3 itself). Sentence A's carve-out appears
nowhere else in the document.

## 6. Sentence A's job in its own paragraph

Sentence A's paragraph is about declaration changes generally — filters, codecs,
decoded size, in-tile offsets. Sentence A's job is to answer "is the list the
test, or is the effect the test?" and it answers: the effect. The identity-filter
illustration is the load-bearing one: it is the case where the list's term "the
codec and filter that produced the stored bytes" provably over-fires. The padding
illustration does not show the list over-firing — it repeals the list's first
term. That is a different act, done in an aside.

Conversely, Sentence B is not shorthand for "unstoring is no escape". A drafter
restating that in shorthand picks an uncontroversial illustration — a filter
change, a codec change. Sentence B picks, as its paradigm of what IS barred, the
exact operation Sentence A had just declared not barred. That is not
abbreviation; it is contradiction.

## 7. Register

No row fires on the disputed commit under EITHER reading. Checked:
- L21 (`[R-CNT-17]`): entry_count must equal N. E 6→5 with T=4 leaves G=2, N=2,
  entry_count 2. Clean.
- L22: extent_length = 2×20 + 1×4 = 44, unchanged. Clean.
- T4 (`[R-SER-05]`): every padding position encodes fill — x=5,6,7 all hold the
  fill byte. Clean.
- T14, T3: length = decoded size = P·Q = 4. Clean.

So the emitted file is a conforming file under both readings; the divergence is
entirely in what the updater is permitted to do. That is consistent with §21.7's
opening: the bar sits in the set of obligations "omitted from the register
because a single file exhibits no witness of their violation."

§21.7 on a witness here: the bar is witnessed "only where the affected tiles
remain stored, and then only for part of what it bars." T remains stored — but
the part reaching it (padding content) is already satisfied, so no witness. This
matches §20.3's own line 3045–3047 ("precisely where the bar has no witness ...
which is why the rule is stated here and not left to the rows") — a sentence
that only makes sense if the rule stated there is one the rows cannot carry,
i.e. Sentence B.

## 8. Tie-break rules in the document

Searched: "diverge", "governs", "takes precedence", "prevails".
- §1 line 8: ADR vs document — inapplicable.
- §21.1 lines 3357–3358 and 3371–3372: register ROW vs rule, and §21.6 entry vs
  rule — the rule governs. No row/entry here, inapplicable.
- §10.2 / Appendix C line 1449–1450, 4168: registry vs section — inapplicable.
- §24 `[R-VEC-01]`: vector vs specification — inapplicable.

The document supplies NO tie-break for two normative prose statements in the same
step. So the tie-break has to be interpretive, and the available ones —
an exception may not nullify the term it excepts from; a term restated at four
sites outweighs a clause restated at none — both run to Reading B.

## 9. The file, concretely

Generation 1. Layer L: rank 1, dim "x" E=6 T=4; one uint8 channel "v", fill 0x00;
interleaved, linearization 1, codec 1, filter 1, index_encoding 1, entry_count 2.
G=2, N=2, P=4, Q=1, decoded size 4.
  Tile 0 (s=0), x∈[0,4): `11 22 33 44`.
  Tile 1 = T (s=1), x∈[4,8): real x=4 = 0x77, real x=5 = 0x00, padding x=6,7 =
  fill 0x00 → `77 00 00 00`.
Index region: 2×20 + 4 = 44 bytes.

Commit: x 6→5. New G = ⌈5/4⌉ = 2 — no tile de-addressed. x=5 becomes padding;
`[R-SER-05]` requires 0x00 there; the byte is already 0x00.

**Reading A emits** (generation 2, appended at F): no payload; NO index region —
L's stored-tile set and index content are unchanged, so line 2986–2992 leaves the
extent slot pointing at the generation-1 region; the new complete directory with
L's dimension extent field 5 in place of 6 and every other record byte-identical
(`[R-WRT-05]`); directory CRC; barrier; pad to 64; trailer gen 2, same file_id,
ignore-lane bits copied (`[R-CNT-08]`), version_minor per `[R-CNT-26]`; barrier.
Appended ≈ |directory| + 4 + pad + 64. New slack: the generation-1 directory,
pad and trailer. This is shape (c) of §20.3's Example — "a change confined to the
directory" — a list that, tellingly, does not include an extent change.

**Reading B emits** nothing: the commit is unavailable. Line 3016–3018 routes the
writer to "a new layer, or a whole-file rewrite under a fresh file_id
(`[R-LIF-01]`, §20.5)" — a compactor output with a fresh nonzero file_id, L
declared E=5, tile 1 re-authored under `[R-CNF-05]` as `77 00 00 00` in a
generation where x=5 was never real. Or the writer takes the shrink the document
does permit: x 6→4. Then G 2→1, entry_count 2→1, index region re-emitted as
1×20+4 = 24 bytes, T's 4-byte payload and the 44-byte index region become slack,
and no surviving stored tile is touched — exactly line 3048–3051.

So two conforming implementations reading only this document emit different
bytes: a directory-sized append versus a refusal-plus-rewrite. Byte-level, yes.

## 10. Honest weakness

Sentence A's clause is precisely engineered — "a new padding position whose
stored byte already holds the fill `[R-SER-05]` fixes" — and can only have been
written with this exact construction in view. And the shrink paragraph opens
"the bar above is the whole of the test", which is an express incorporation of
the bar AS AMENDED, carve-out included. That is Reading A at its strongest and it
is a real argument. My answer is in §2 and §5: "the bar above" includes term 1,
which the disputed commit alters; an illustration in the same paragraph cannot
repeal the term it illustrates and leave it with no application anywhere; and the
clause's precision is a symptom of a late unpropagated insertion, not evidence of
considered scope.

## 11. Verdict

READING_B_GOVERNS. The document contains a genuine contradiction on this fact
pattern, and Sentence A's six-word illustration is the defect — the repair
overreached from the filter case it was written for into the padding case, and
did not propagate to §11.1, §21.7, §23.1, or to §20.3's own closing description
of a permitted shrink.
