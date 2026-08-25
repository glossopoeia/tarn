# Advocate for Reading B — working transcript

Access: only /Users/robertkleffner/Documents/GitHub/tarn/spec/tarn.md, via sed/grep/tr.
Unrequested context appeared (project instruction file + an index of maintainer
memory-note titles). Disregarded; not used as evidence. Disclosed.

## 1. Quotation check

§20.3 step 4, spec lines 2994-3001 (the bar):

  "A commit MUST NOT change a layer's declarations in a way that alters, for
  any tile that layer stores **in the generation this commit supersedes**,
  what §14 fixes for its stored bytes or how they decode — the set of padding
  positions (§11.3) and the content `[R-SER-05]` fixes there, the decoded
  size, the byte offset of any sample within the decoded tile image, or the
  codec and filter that produced the stored bytes."

Sentence A, lines 3005-3011 — charter's rendering is accurate; it drops only
the citation "(`[R-COD-10]`)" after "the identity". No substantive misquote.

Sentence B, lines 3041-3045 — accurate.

## 2. The construction, made concrete

Rank-1 layer L, dim x, E=6, T=4. Grid = ceil(6/4) = 2. One uint16 channel,
fill 0x0000. Interleaved, codec 1, filter 1. Tile 1 covers x 4..7: real {4,5},
padding {6,7}. Stored (gen 1), decoded size 8 bytes:
  x=4 sample 0x1234 -> 34 12 ; x=5 sample = 0x0000 -> 00 00 ; pad -> 00 00 00 00

Commit: E 6 -> 5. New grid = ceil(5/4) = 2 — UNCHANGED. Both tiles still
addressed, tile 1 still stored. Tile 1's real set falls to {4}; x=5 becomes
padding. §14.5 demands fill at x=5; the byte there is already 00 00.
Zero bytes of T change. entry_count stays 2. No index re-emission is even
owed (step 4 re-emits only where the stored-tile set or index content changes;
[R-GEO-06] renumbers nothing, the grid count being unchanged).

So under Reading A this is a **directory-only commit** — §20.3's Example (c)
shape: only the layer record's extent field changes.

## 3. Sites that state or restate the rule

(a) The bar itself (3005): list includes "the set of padding positions
    (§11.3)" as a distinct item from "the content [R-SER-05] fixes there".
(b) Sentence A (3005-3011) — the ONLY site supporting Reading A.
(c) Shrink paragraph opener (3033-3036): "a shrink is permitted exactly where
    it alters nothing §14 fixes for any tile the layer stores in the
    generation this commit supersedes." Formulated as ALTERATION, not as
    byte-meaning.
(d) Sentence B (3041-3045) — flat, on point, with a stated reason.
(e) §20.3 consequence sentence (3048-3051): "Where a shrink is permitted the
    de-addressed tiles' extents become slack ([R-CNT-21]), [R-CNT-17] obliges
    the smaller entry_count and so a re-emitted index region, and every
    surviving stored tile is untouched."  -> every permitted shrink has
    de-addressed tiles, a SMALLER entry_count, and a re-emitted index. The
    disputed commit has none of the three. B.
(f) §11.1 Rationale (blockquote, non-normative, lines 1484-1490): "§20.3
    states normatively, and governs, ... a shrink is barred wherever it alters
    what §14 fixes for such a tile — whether or not the new state still stores
    it — and permitted where it **only** drops tiles out of the addressed set,
    whose extents then become slack." No carve-out. B.
(g) §23.1 [R-PRV-01], NORMATIVE (3931-3937): "A commit removes sample data two
    ways — superseding it, and a shrink that de-addresses tiles (§20.3 step
    4) ... In each case the bytes remain in the file as slack." Under Reading A
    there is a third way, and in it the bytes remain live inside an addressed
    stored tile rather than becoming slack. B (corroborating weight: the
    removed sample is always fill-valued under A, so the privacy stake is
    small; the enumeration is still short by one).
(h) §20.3 Example (c) blockquote (3117-3128): enumerates directory-confined
    commits — slab clear, rename, fill change on a layer with no padding
    position and no pad bit. A shrink is not among them. Weak, non-normative.
(i) §21.7 (3693-3700): "§20.3 step 4's bar on a declaration change is
    witnessed only where the affected tiles remain stored, and then only for
    part of what it bars. A change reaching a byte §14 structurally constrains
    — a padding position, a pad bit, or a boolean byte — fires §21.4's content
    rows." Its witness-walk covers the bar's items 2,3,4,5 but never treats
    item 1 (the padding SET) separately. This is the one site that reads
    better under A.

Tally: one site for A (b), plus (i) leaning A. Four for B (d,e,f,g), plus (c)
and (h) leaning B — and, decisively, (b)'s own general standard.

## 4. The internal contradiction inside Sentence A

Sentence A's test: "leaves every one of those tiles' stored bytes meaning
exactly what they meant."

Example 1 (identity filter) satisfies it perfectly. §17.3 [R-COD-10]: "for a
packed boolean plane s = 1 and the filter is the identity." Filter 1 -> 2 on
such a layer changes no decoded byte, no padding position, no size, no offset.
Nothing observable changes.

Example 2 fails it. What the byte at x=5 means, before and after:
  BEFORE — §3.2 [R-MDL-01]: the reference array's element at coordinate 5 is
    "the one decoded from that tile"; [R-MDL-02]: "a conforming reader that
    reads any portion of a layer MUST return exactly the corresponding portion
    of the reference array, bit-for-bit."
  AFTER  — [R-MDL-01]: "Sample positions that exist only as edge-tile padding
    (§11.3) have coordinates outside the layer's extents and are not part of
    the reference array." §11.3 [R-GEO-04]: "a reader MUST NOT return padding
    positions as samples." §19.4 step 7: "padding positions are never
    returned." §14.5: "A conforming reader never returns this content."
    §19.4 step 1: a point request at x=5 now "fails as a request".

MUST return -> MUST NOT return. That is a change in what the stored byte
means, on the document's own definitions, of the largest kind short of a value
change. Sentence A's second example is therefore not an instance of Sentence
A's own standard. The standard is what Sentence A announces as governing
("The test is the effect on such a tile"); the em-dash pair is illustration.
Where illustration contradicts the announced test, the test governs — and the
test, so applied, agrees with Sentence B and with (e), (f), (g).

## 5. The growth clause as corroboration

3022-3024: "an extent MAY **grow**, since a position that becomes real held
that channel's fill and fill is a legal sample value". Growth on a stored edge
tile shrinks the padding set — a change to bar-item 1 with every byte already
carrying a legal value. The drafter granted it EXPRESSLY and justified it by
the byte's value. That express grant is needed only because the bar otherwise
reaches a real/padding reclassification whose bytes already conform. Shrink
received an express grant too — but only for the de-addressing case (e),(f).

## 6. Register

No row fires on the disputed commit under either reading. T4 tests padding
content against recorded fill — satisfied. T5 pad bits — n/a. T3/T14 decoded
size — unchanged. T2 bool bytes — n/a. Codec/filter rows — unchanged. L21
entry_count vs geometry-derived count — 2 = 2. L22 extent_length formula —
unchanged. §21.6 contains no entry licensing this commit.

§21.1's tie-breaker ("where a row and the rule it cites diverge, the rule
governs") is about rows vs rules and does not reach two normative prose
sentences. §2.1/§2.2 supply no precedence rule between them either. So the
dispute is decided by weight of text, not by a conflict clause.

§21.7 on a witness here: this is a case where the affected tile REMAINS
stored, so §21.7's "leaves the live state clean" clause (which is about
unstoring) does not cover it. It falls instead under §21.7's concession that
the bar is witnessed "only for part of what it bars." Cost to Reading B: under
B, §21.7's claim that a change reaching a padding position "fires §21.4's
content rows" over-claims for this construction. That is an inaccuracy in a
catalogue of witnesses that has already disclaimed completeness of witnessing;
it carries no MUST and imposes no obligation.

## 7. What an implementer emits

Reading B (bar governs). The appender MUST NOT commit. Step 4: "Such a change
is a new layer, or a whole-file rewrite under a fresh file_id ([R-LIF-01],
§20.5)." So it emits either
  (i) gen 2, same file_id, TWO layers: L unchanged at E=6 (record and tiles
      carried forward byte-identically) and a new L' at E=5 with freshly
      written tiles and its own index region; or
  (ii) a whole-file rewrite: fresh file_id, generation 1.

Reading A (carve-out governs). The appender commits shape (c): at F it writes
only the re-emitted directory (the layer record with extent 6->5, every other
record byte-identical), the directory CRC, barrier, pad, and a 64-byte trailer
with generation 2 and the same file_id. No tile byte, no index byte appended.
Slack = old directory + pad + trailer.

Divergence is at the byte level and at the reader level. A read of the whole
layer returns 5 samples under A's file; under B's file (i) L returns 6 and L'
returns 5. A conformance vector for this commit has no single expected byte
stream across the two readings.

## 8. Verdict

READING_B_GOVERNS. Sentence A's second em-dash example is the defect: it
contradicts the standard in its own sentence, it is the only site in the
document that supports the permission, and four other sites — one of them a
normative requirement outside §20 ([R-PRV-01]) and one of them §20.3's own
statement of what a permitted shrink costs — describe the permitted-shrink
class as the de-addressing class alone.

The repair the panel should recommend is to strike "or a new padding position
whose stored byte already holds the fill [R-SER-05] fixes" from Sentence A,
leaving the identity-filter example, which is a true instance of the test.
