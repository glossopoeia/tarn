# Advocate A1 — working transcript

## Access
Read only /Users/robertkleffner/Documents/GitHub/tarn/spec/tarn.md (sed/grep).
Unsolicited context appeared before I began (project instruction pointer + an
index of maintainer memory files naming prior findings/cadence). Not read
beyond the auto-inserted reminder; not used.

## Quote verification
- Sentence A, lines 3005-3011. Charter's rendering drops the citation
  "(`[R-COD-10]`)" after "makes it the identity". No other difference.
  The dropped citation *helps* Reading A: it makes the first example
  declaration-determined, which matters to the counter-argument below.
- Sentence B, lines 3041-3045. Verbatim modulo hard-wrap.

## The bar's own head (2994-3001)
"A commit MUST NOT change a layer's declarations in a way that **alters**, for
any tile that layer stores in the generation this commit supersedes, what §14
fixes for its stored bytes or how they decode — the set of padding positions
(§11.3) and the content [R-SER-05] fixes there, the decoded size, ..."

Head = "alters what §14 fixes for its stored bytes". Em-dash list = appositive.
Sentence A says exactly that: the list "names where that effect arises rather
than standing on its own".

## The shrink paragraph incorporates the bar whole (3033-3036)
"An extent MAY also **shrink**, and the bar above is the whole of the test,
**in the bar's own tense**: a shrink is permitted exactly where it alters
nothing §14 fixes for any tile the layer stores in the generation this commit
supersedes."

- "the bar above is the whole of the test" — Sentence A is part of the bar
  above. So the shrink paragraph cannot add a bar beyond it.
- "**in the bar's own tense**" (bolded) names the one thing the paragraph
  adjusts: the quantifier. Not the alteration predicate.
- The paragraph's three following sentences are all quantifier sentences:
  de-addressing does not rescue; unstoring does not rescue "for the same
  reason: the quantifier is the superseded generation's".

Sentence B's stated *reason* is the quantifier. Its operative content is
"whether or not the new state still stores it". Its subject is imported by
"and for the same reason" from the prior sentence's "a commit that **damages**
a prior-generation stored tile". So: a *damaging* shrink.

## Sentence B's own cross-reference confines it
3045-3047: "§21.7 records the consequence — that this is precisely where the
bar has no witness, **the live state being clean**".
§21.7's matching text (3706-3708): "a commit that supersedes every tile it
would have damaged leaves the live state clean".
"The live state being clean" is true only where the tile is unstored. In the
construction T remains stored, so Sentence B's consequence-clause does not
describe it. If Sentence B stated a rule reaching retained tiles, its own
cross-reference would be false for that half.

## §21.7 is a second NORMATIVE site, and it is reach-based
3685-3689: "§20.3 step 4's bar on a declaration change is witnessed only where
the affected tiles remain stored, and then only for part of what it bars. A
change **reaching a byte** §14 structurally constrains — a padding position, a
pad bit, or a boolean byte — fires §21.4's content rows."
Then "A change reaching the decoded size...", "reaching the codec...",
"reaching the filter...". The whole taxonomy of the bar is stated in *reach*,
and its padding item is a *byte*, not a position set. §20.3 3011-3012 uses the
same word: "Where a change does reach them".

Under Reading A the taxonomy closes exactly: every barred padding change is one
where the required byte differs from the byte present, and that always fires T4.
Under Reading B the padding class splits — some barred changes fire T4, some
(ours) fire nothing — and §21.7 asserts the whole class is witnessed. §21.7 is
normative (no blockquote) and carries [R-ERR-01]. §21.1 leans on it: register
completeness is normative with "§21.7 the account, by class, of what fails it".
Reading B makes a normative sentence false.

## Register check
- T4 (3541): "A padding position does not encode ... that channel's recorded
  fill value" — the new padding byte DOES hold fill. Does not fire.
- T2/T5: bool only. T3/T14: decoded size unchanged (derived from tile extents,
  not layer extents). T26: no filter change.
- §21.6 row 2 ("A requested coordinate lies outside the layer's extents") is
  the only thing that changes for a reader: x=5 now fails as a request.
- No row fires under either reading. Under Reading A that is correct (no
  violation). Under Reading B it is an unregistered, unaccounted violation.

## Other restatement sites
- §11.1 Rationale, 1486-1490 (non-normative, and it says §20.3 "governs"):
  "a shrink is barred wherever it **alters what §14 fixes** for such a tile —
  whether or not the new state still stores it". Alteration-based, with the
  unstoring clause attached as a modifier on the alteration test — the exact
  grammar Reading A gives Sentence B.
- §20.3 shape-(c) Example, 3120-3127 (non-normative): a fill change "on a layer
  with no padding position and no pad bit" is a directory-only commit; on a
  layer that stores a tile carrying either it "would invalidate every stored
  tile **it reaches**". Reach again.
- The grow permission, 3022-3024: growth is allowed "since a position that
  becomes real held that channel's fill and fill is a legal sample value" —
  the justification is byte-effect, not declaration-shape. Same principle.
- §23.1, §20.5: no restatement of the bar.
- No general precedence rule for two normative prose sentences exists.
  §21.1's "the rule governs" is row-vs-rule (3358) and §21.6-entry-vs-rule
  (3372) only. Neither reaches this.

## Perverse consequence of Reading B
Layer: rank 1, x extent 6, tile extent 3 → grid 2. T = tile 1, covers x=3,4,5.
- Shrink 6→3: T leaves the addressed set entirely. Permitted (3036-3039,
  "Dropping a tile out of the addressed set ... is not itself such an
  alteration"). Three real positions discarded.
- Shrink 6→5: T retained, x=5 becomes fill-valued padding. Reading B: barred.
  One real position discarded.
Reading B bars the smaller discard and permits the larger, with no byte
difference to justify it, against 3051-3052: "Discarding data is the caller's
operation and this specification does not bar it."

## Build the file
One uint16 channel, fill 0xABCD, interleaved, codec 1, filter 1. T's decoded
size 6 bytes; x=3,4 carry data; x=5 already holds CD AB.

Reading A emits: nothing changes in the stored-tile set or index content, so
no index region is re-emitted and the layer keeps its extent slot
([R-WRT-05]). Appended = new directory (layer record identical but for extent
6→5) + directory CRC + barrier + pad + 64-byte trailer at generation 2, same
file_id. Slack = old directory, pad, trailer. Shape (c). Verifier certifies:
T4 passes at x=5, T3/T14 pass, every tile byte untouched.

Reading B emits: refusal. To honor the caller — a new layer L' at extent 5
with every tile copied (both payloads again, a fresh 44-byte index region,
directory carrying both records), stranding L's data live-but-unwanted; or,
per 3052-3056's SHOULD and [R-LIF-01], a whole-file rewrite at a fresh file_id
and generation 1. Different length, different file_id, different generation.

byte_level divergence: yes.

## Strongest counter and why it loses
See structured output.
