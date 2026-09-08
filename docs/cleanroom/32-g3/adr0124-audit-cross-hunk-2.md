# Cross-hunk auditor 2 — operation-grouped audit of the §20.3 step 4 rewrite

## Disclosure

Context contamination noted: before I did any work, my system prompt/context
already contained a CLAUDE.md pointer (AGENTS.md), a user MEMORY.md index with
entries titled things like "TARN harness spec path", "TARN lineage gate word
list", "TARN repair prose vs rules", "TARN harness vs charter", "TARN repair
list vs diff", "Shell gates need explicit exit checks", "TARN subagents on
Opus", and a git status block showing recent commit subjects ("Cleanroom round
31: charter", "The pre-round-31 audit: sixteen defects...", "ADR-0122:...",
"ADR-0121:...", "ADR-0120:..."). None of this was requested by me. I did not
open any of the referenced memory files, did not read AGENTS.md, and did not
use any of these commit subjects or memory titles as evidence about the
document. I disregarded all of it and worked only from the two permitted
sources below. I also received mid-session system-reminders about a date
change and about MCP tool availability; these are not spec content either and
were ignored for analysis purposes.

**What I read:**
- `/Users/robertkleffner/Documents/GitHub/tarn-first-draft/spec/tarn.md` (full
  file exists at the path the brief named; read via `sed -n` ranges covering:
  1083–1230 (§7.4 field table + example), 1600–1735 (§11.1–§11.4), 1895–1955
  (§13.3), 2320–2350 (§16.2 R-SLB-03/04), 2995–3015 (§13 read algorithm
  R-GEO-06 use), 3071–3480 (§20.2 through §20.5), 3396–3480 (§20.5
  compaction), 3539, 3866–3905 (§21.7), 4136–4172 (§23.1), 4670–4720
  (Appendix H).
- All 7 files in
  `/private/tmp/claude-501/-Users-robertkleffner-Documents-GitHub-tarn-first-draft/r32-audit2/case/`:
  `hunk-01.diff` through `hunk-07.diff` (NOT `full.diff` — never opened it,
  never listed the directory beyond the one `ls` needed to confirm the seven
  files existed).

**What I ran:** only `sed -n` (line-range reads) and `grep -n` against
`spec/tarn.md`, plus `cat` on my own seven hunk files. No other files, no git
history, no docs/, no conformance/, no web.

**Verification that spec/tarn.md already has the hunks applied:** each hunk's
banner line count (`@@ -oldstart,oldcount +newstart,newcount @@`) matches the
banner's own "lands in spec/tarn.md at lines X-Y (current file)" claim to
within header-context slop, and I independently confirmed this by reading the
named current-file line ranges and finding the hunk's "+" (new) lines verbatim
there. I did this for all 7 hunks (see below) — spec/tarn.md is post-repair
text throughout.

## Method

I organized by writer *operation*, per my charter, working the central
rewrite (hunk-03, §20.3 step 4) against every operation the old bar/carve-out
regime named, then checked hunks 01/02/04/05/06/07 as restatements or
consequences of that same rule, running the 8 checks against each.

## The new closed-list rule (hunk-03), read in full

Read at spec/tarn.md:3157-3246 (post-patch). Full text reproduced/quoted in my
findings below. Structure:

- Step 4 opening (unchanged by this round): every layer whose *stored-tile
  set or index content* changes gets its whole tile-index region
  re-emitted; "a growth renumbers ordinals wherever [R-GEO-06] moves them,
  and nothing else this step permits moves one."
- **New paragraph 1 (the closed list):** "A layer that stores a tile in the
  generation this commit supersedes keeps its declarations, with these
  exceptions and no other: its name, and its dimension and channel names,
  MAY change; an extent MAY grow; a planar layer's channel list MAY be
  extended at its end, or shortened from its end; and a slab or alignment
  declaration is re-established or cleared... Every other declaration is
  fixed... : the layout, the linearization and the index encoding, the codec
  and the filter, the rank and the dimension order, every tile extent, every
  channel's type and fill, an interleaved layer's channel list, and the
  position of every planar channel but the last. A commit MUST NOT change
  one of these... **The two lists partition §7.4's fields, the derived ones
  aside — entry_count, crc_of_crc_array and the extent slot follow the
  commit.** ... A layer that stores no tile in the generation this commit
  supersedes MAY be re-declared freely..."
- **New paragraph 2 (the principle):** "The line is drawn where a stored
  tile's meaning is fixed... **The permitted changes touch none of that:** a
  name enters no map; a grown extent adds positions that held their
  channel's fill...; an appended planar channel adds tiles at ordinals after
  every existing one...; a channel removed from the end takes only its own
  tiles out of the addressed set... What the line gives up is stated rather
  than carved around: a shrink, a fill change, a re-type, a re-tiling, a
  change of layout, codec or filter, and a channel inserted or removed
  anywhere but the end are rewrites..."
- **New paragraph 3 (mechanics):** growth bounds (L44, R-ENC-04); "A channel
  removed from the end leaves its stored tiles' extents as slack (§5.2), and
  [R-CNT-17] obliges the smaller entry_count and so a re-emitted index
  region; a writer SHOULD instead produce a new file wherever a commit would
  strand a large share of a layer's stored bytes — and always where it
  would re-emit every one of them, which duplicates the layer rather than
  dropping part of it."

## Operations worked to bytes

**(1) Renaming a layer.** Permitted-list item 1. Directory-only per shape (c)
(§20.3's example, hunk-04 context, spec:3313-3316): "clearing a slab
declaration, renaming a layer, or dropping a PE = 0 record... Only the
directory is re-emitted." Using the §7.4 worked example (spec:1157-1177, the
81-byte `sst` layer record): renaming `sst` (3 bytes) to e.g. `lake` (4
bytes) changes only the `name` field's length-prefixed bytes at inline-payload
offset 0 (03 73 73 74 → 04 6C 61 6B 65), shifting every subsequent field's
absolute position within the record by +1 byte but not touching
`entry_count`, `crc_of_crc_array`, the extent slot's value, or one byte of
the tile-index region or stored tile payload at offset 61 elsewhere in the
file. Only the directory region and its terminal CRC (§8.1's "final 4 bytes
of the region" covering it) are new bytes on disk; the trailer's
`committed_file_length` grows only by the directory's size delta. Consistent
with hunk-01's Rationale restatement and hunk-07's Appendix-H restatement.
No defect found in this operation as such.

**(2) Growing an extent with entry_count unchanged (product held at 0).**
Governed by the closed list's "an extent MAY grow" plus §11.1's own
(non-normative) Rationale gloss at spec:1648-1656: "Growth that leaves
entry_count unchanged touches the directory alone — a growth raising one
grid count ⌈Eᵢ/Tᵢ⌉ ... while another stays 0 among them, the product holding
at 0." Bytes: only the changed dimension's `extent Eᵢ` u64 field inside the
layer record's dimension-entry array moves (8 bytes), which is inside the
inline payload and hence forces a directory re-emission (record length
possibly unchanged, extent value changed) but the layer's `entry_count`
stays 0 and the tile-index region (which for `entry_count=0` is the 0-length
entry array + its 4-byte segment-CRC-array `crc_of_crc_array`, at extent
slot (0,0) per L21/L22's constant) is untouched, so the extent slot's value
is untouched too. This matches step 4's general trigger ("index content"
moves only when stored-tile set or entry_count changes) and is NOT drawn in
the "three shapes" figure (§20.3, spec:3274-3324) as its own labeled case —
but that figure is inside a block headed "**Example — the three shapes...**"
(Example label, non-normative per R-CNF-01) and does not itself claim to be
exhaustive of every directory-only sub-case, so the omission there is not a
defect of this round's hunks (the figure's shape-(c) enumeration already
omitted this case before this round's edits — I checked the old shape-(c)
text in hunk-04's diff and it likewise never named a bare growth). Not
flagged.

**(3) Removing a planar layer's last channel.** Worked using the §7.4
example's channel-entry shape (`temp`: name+type u16+fill, 12 bytes) as a
stand-in for a 2-channel planar layer (`a`,`b`), N spatial tiles each.
Removing `b`: channel count C: 2→1, one 12-ish-byte channel entry removed
from the inline payload (directory changes), `entry_count`: C·N → 1·N
(shrinks), the tile-index region is *fully* re-emitted at a new placement
(extent slot changes) per step 4's opening clause, `b`'s N tile extents
become slack (§5.2, R-CNT-21), and per hunk-03's own text "a tile the new
state does not address carries no obligation" — `a`'s N tiles keep their
disk ordinals (c·N+s with c=0 unchanged) and are byte-identical at their old
disk positions inside the *new* index region (their entries are copied,
not moved, into the re-emitted region — the region moves as a whole but the
individual entries for surviving tiles are unchanged content at
disk-ordinal position, matching the general "every other entry
byte-identical at its disk-ordinal position" rule). This is the
operation hunk-05 and hunk-06 use as the sole remaining "operation that
takes tiles out of the addressed set." See Y-03 below for a defect in the
guidance sentence that follows this mechanic.

**(4) Shrinking an extent.** Confirmed, by exhaustive grep, that this
operation is **no longer permitted in place at all** under the rewritten
step 4 — a substantive change from the pre-repair rule, and one I traced
for internal consistency:
```
grep -n "shrin" tarn.md
1636:   (byte range that hunk-01 replaced — not a live hit, see below)
3217:   gives up is stated rather than carved around: a shrink, a fill
4157:   padding, a shrink being a rewrite (§20.3 step 4), so the bytes a
```
Only two live hits in the whole 4729-line document, both agreeing: a shrink
is now a rewrite (hunk-03's paragraph 2, and hunk-06's §23.1 rewrite). I
also grepped `L21`/`L22`/`entry_count.*smaller` and the whole document for
any remaining "grid count fall[s]" / "de-addressed" / "addressed set"
language that might still describe shrink as legal (spec:3708-3709,
1627-1655, 3215, 4146, 4588) — every hit is either the shrink-is-a-rewrite
statement, the channel-removal mechanic, or generic register-row text about
`entry_count` mismatches (a reader-side validity check, unaffected by
whether shrink is a legal *writer* operation). No stray restatement of the
old "a shrink is permitted where it doesn't touch a §14-protected tile"
carve-out survives anywhere. This operation is consistently and completely
swept across all seven hunks. Not itself a defect — but see Y-03, which
is a leftover clause written for shrink's "strand 100%" case that the
channel-removal-only regime can no longer reach.

## Findings

### Y-01 — the partition claim is false: sub-records are a §7.4 field in neither list (byte-level)

Rule the repair asserts: "A layer that stores a tile in the generation this
commit supersedes keeps its declarations, with these exceptions and no
other: [5-item list]... Every other declaration is fixed... [11-item list].
A commit MUST NOT change one of these... **The two lists partition §7.4's
fields, the derived ones aside — entry_count, crc_of_crc_array and the
extent slot follow the commit.**"

I read §7.4's field table in full (spec:1089-1106) and checked every row
against the two lists plus the three-item "derived" bucket:

| §7.4 field | Where it lands |
|---|---|
| name | permitted (name MAY change) |
| layout | fixed |
| linearization | fixed |
| codec | fixed |
| filter | fixed |
| alignment A | permitted (slab/alignment) |
| slab S | permitted |
| slab alignment A_slab | permitted |
| rank d | fixed |
| channel count C | fixed (interleaved) / permitted via end-extend-shorten (planar) |
| d dimension entries (name/extent/tile extent) | name permitted, extent permitted-to-grow, tile extent fixed |
| C channel entries (name/type/fill) | name permitted, type+fill fixed |
| index_encoding | fixed |
| entry_count | derived-aside |
| crc_of_crc_array | derived-aside |
| **sub-records** | **neither list, not in the derived-aside bucket** |

`sub-records` is literally the last row of §7.4's own table: "| sub-records |
zero or more records (§7.2 framing) to the end of the inline payload | layer
scope by containment |" (spec:1106). I grepped the entire replaced step-4
text (spec:3157-3250) for "sub-record" and got zero hits — confirmed with a
positive control (grepping "sub-record" over the whole document returns 40+
hits elsewhere, so the search mechanism works; the zero is specific to step
4's own text). The claim "the two lists partition §7.4's fields" is
therefore false on the document's own terms: one of §7.4's own enumerated
fields is not placed by either list and is not one of the three named
derived fields.

This is not a cosmetic gap. The opening sentence's closure — "keeps its
declarations, with these exceptions and no other" — reads as barring any
change not in the 5-item permitted list, which would include sub-record
changes (e.g., a writer wanting to attach a fresh user-metadata sub-record,
or drop one under the PE=0 licence discussed elsewhere, to a layer that
already stores tiles). But the operative prohibition sentence — "Every
other declaration is fixed... : [11-item list]... A commit MUST NOT change
**one of these**" — grammatically binds only the 11 named items, and
sub-records is not one of them, so the MUST NOT does not textually reach it
either. The two sentences disagree about whether a sub-record change to a
populated layer is (a) implicitly barred by the closure of sentence 1, or
(b) simply unaddressed and therefore free, since it is "one of these" in
neither enumerated list.

Hunk-07 (Appendix H, "Conforming updater") treats the closed list as
already fully closed with no third option: "changes a layer that stores a
tile only as §20.3 step 4 permits — its names, a grown extent, a planar
channel at the end, a slab or alignment declaration — and makes any other
change to it as a new layer or a whole-file rewrite (§20.3)." This confirms
the *intent* was a fully closed, two-way partition — which makes the
missing sub-records row a defect in step 4's own enumeration rather than a
deliberately-left-open third category.

Byte-level test: is the disputed file conforming? Consider a commit that
adds one new user-metadata sub-record to a layer record that already stores
tiles, changing nothing else about that layer (no growth, no rename, no
channel-list change). Under reading (a) this commit is barred — the writer
must emit it as "a new layer, or a whole-file rewrite under a fresh
file_id" (hunk-03's own words), producing a very different byte sequence
(new file_id, whole-file rewrite bytes, or a duplicate layer object) from
what it would emit under reading (b), where the commit is a normal
directory-only (or, if the sub-record extent is new, shape-(b)-style)
append that keeps the same file_id and the same layer identity. Two
competent implementations, reading only this text, can and do disagree
about whether the resulting file is a conforming append vs. a conformance
violation requiring a rewrite — the emittable/acceptable byte set moves
depending on which reading is taken. This is byte-level.

### Y-02 — the principle paragraph's "touch none of that" claim covers only 3 of the 4 permitted-change categories (not byte-level)

Rule the paragraph asserts: "The line is drawn where a stored tile's
meaning is fixed. The fixed declarations are the ones §14 reads a stored
tile under... and the ones §11.4 assigns its ordinal and its values'
coordinates by... **The permitted changes touch none of that**: a name
enters no map; a grown extent adds positions that held their channel's
fill...; an appended planar channel adds tiles at ordinals after every
existing one...; a channel removed from the end takes only its own tiles
out of the addressed set..."

The permitted list this paragraph is glossing (the paragraph immediately
above it) names four categories of exception: (i) names, (ii) extent
growth, (iii) planar channel list extended/shortened at the end, and (iv) a
slab or alignment declaration re-established or cleared. The four
"touches none of that" examples given map to (i), (ii), and the two
directions of (iii) — but **(iv), the slab/alignment exception, is never
mentioned** in this paragraph at all. The blanket sentence "The permitted
changes touch none of that" is stated over the *whole* permitted list (it
says "the permitted changes," not "these three"), so on its own terms it
overclaims: it asserts, without argument, that a slab/alignment change also
doesn't touch a stored tile's §14 meaning or §11.4 coordinate — which is
true (slab/alignment govern on-disk *placement*, not sample meaning or
coordinates) but is asserted, not shown, unlike the other three categories
which each get their own one-clause proof. A reader working through "why
these four and not a fifth" (per my charter) gets an answer for three of
the four and has to supply the fourth's argument themselves.

This sits in plain step-4 body text, not inside a Note/Example/Rationale
block, so it is normative-labeled text under R-CNF-01 — but its function is
purely explanatory: the actual grant of permission for slab/alignment
changes lives in the closed list one paragraph above (and in R-SLB-04's own
independent rule for re-establishing or clearing the declaration), so this
paragraph's incompleteness doesn't itself change what bytes a conforming
writer may emit — the permission already stands on the closed list's own
words. Not byte-level: this is a documentation/overclaim defect (an
OVERCLAIM under my check 5 — the word "The permitted changes" claims
coverage of all of them and delivers three), not a conformance fork.

### Y-03 — the "always where it would re-emit every one of them" clause was carried from shrink's context into channel-removal's, where its trigger is now unreachable (not byte-level, PLAUSIBLE)

Rule the sentence asserts (spec:3232-3236, paragraph 3 of the rewrite): "A
channel removed from the end leaves its stored tiles' extents as slack
(§5.2), and [R-CNT-17] obliges the smaller entry_count and so a re-emitted
index region; a writer SHOULD instead produce a new file wherever a commit
would strand a large share of a layer's stored bytes — **and always where
it would re-emit every one of them**, which duplicates the layer rather
than dropping part of it."

I checked this sentence's ancestry: hunk-03's diff shows this exact clause
("A writer SHOULD instead produce a new file wherever a commit would strand
a large share of a layer's stored bytes — and always where it would
re-emit every one of them, which duplicates the layer rather than dropping
part of it.") appearing **verbatim** in the deleted (old) text too, there
attached to *shrink* rather than to channel removal. In the old
shrink-governed passage, the degenerate case this "always" clause reaches
is a shrink that de-addresses literally every stored tile of the layer —
reachable, since a shrink can take a dimension's extent to 0, forcing the
grid count and hence N to 0 and stranding 100% of the layer's stored bytes
at once.

Under the rewrite, shrink is no longer a legal in-place operation at all
(Y-checked above), and the only surviving way to strand tiles without a
rewrite is "removing a planar layer's last channel." But R-GEO-01
(spec:1621, "Writers MUST NOT emit a layer with... channel count 0")
requires channel count ≥ 1 always, so a channel-list-shortening commit can
never remove every channel — at least one channel, and therefore at least
that channel's own N tiles (if it stores any), always survives such a
commit. The 100%-of-the-layer's-stored-bytes degenerate case this clause
was written for is therefore **structurally unreachable** in its new home:
there is no channel-removal commit for which "it would re-emit every one of
[the layer's stored bytes]" can be true, since removing a channel never
"re-emits" any stored payload bytes at all (surviving channels' tiles are
untouched at their old disk positions per the same paragraph's own words —
"a tile the new state does not address carries no obligation" — and the
removed channel's tiles are stranded as slack, not re-emitted). The clause
was carried over from the deleted text without being re-derived for the
operation it now describes.

Byte-level test: this is advisory (SHOULD) prose with no register row or
MUST attached to it — it recommends when a writer *should* choose a
whole-file rewrite over an in-place channel removal, but does not itself
gate whether a file is conforming. Resolving the ambiguity (dropping the
clause, or rewriting it in channel-removal's own terms) changes no byte a
conforming writer MUST or MUST NOT emit, and no verifier accept/reject
verdict. Not byte-level. I flag it PLAUSIBLE rather than CONFIRMED because
the clause is dense enough ("re-emit every one of them") that I cannot
fully rule out a reading under which "them" denotes index entries rather
than stored bytes — under that reading the clause is trivially always true
for any channel removal (since the whole index region is always re-emitted
whenever entry_count changes, per step 4's opening clause) rather than
unreachable, which is a different but also defective reading (a
vacuously-true "always" that does no discriminating work). Either reading
leaves the clause broken; I could not fully resolve which was intended
without material outside my access.

## Checks run against each hunk (summary)

- **Hunk-01** (§11.1 Rationale): sits inside a `> **Rationale.**` block —
  confirmed non-normative per R-CNF-01, correctly so (it restates, doesn't
  originate, the rule). Its restatement ("its extents may grow... a planar
  layer's channel list may be extended or shortened at its end; its names,
  and its slab and alignment declarations, may change; and every other
  declaration is fixed...") is a faithful compression of hunk-03's closed
  list; no contradiction found. No anaphor issues — the paragraph's
  following sentence ("Growth that leaves entry_count unchanged...") begins
  a new topic sentence, not a pronoun, so the hunk-01 edit doesn't change
  what anything downstream resolves to.
- **Hunk-02** (§13.3, `> **Note — sparse writing.**` block, non-normative):
  claim "changes a layer's stored-tile set or its entry_count — the only
  way its index content moves under the changes §20.3 permits" checked by
  exhaustive case analysis against hunk-03's ordinal-renumbering rule
  (R-GEO-06): since every dimension-extent growth is monotonic (shrink
  barred) and each dimension's grid count Gᵢ can only stay level or rise,
  any growth that moves an existing tile's ordinal necessarily raises N
  (hence entry_count, for both layouts) — I could not construct a
  counterexample where ordinals move without entry_count changing. Holds.
- **Hunk-03**: see Y-01, Y-02, Y-03 above; also confirmed no NESTED_DASH
  instances (single em-dash pairs throughout, none nested).
- **Hunk-04** (§20.3 shape (c)): citations resolve — "step 4" and the
  layer-record fixed-declaration list checked against hunk-03's own text,
  consistent; the removed fine-grained fill-value carve-out ("a channel
  that carries no padding position...") is now correctly absent, matching
  the closed list's blanket bar on fill changes (no orphaned reference to
  the deleted carve-out found anywhere else — grepped "carries no padding
  position" and "pad bit in any tile" — zero hits post-patch).
- **Hunk-05/Hunk-06** (§23.1): traced the "every case" / "not offered as
  closed" claims — hold given shrink's removal (see operation (4) above and
  Y-03). The "the list of operations above" back-reference in hunk-06
  resolves, both before and after hunk-05's edit, to the same sentence
  (superseding/unstoring/channel-removal/record-drop-or-supersede) one
  paragraph up — no anaphor drift, since hunk-05 changed that list's
  *content* but not its *position* relative to hunk-06's back-reference.
- **Hunk-07** (Appendix H): restatement checked word-for-word against
  hunk-03's closed list; consistent (see Y-01's discussion of how it
  presupposes a fully-closed two-way partition).

## Rejected candidates

1. Considered flagging the closed list's move from a **channel-level** bar
   on re-typing (old text: free to re-type a channel "of a layer that
   stores nothing, or a planar channel none of whose own tiles are stored")
   to a **layer-level** bar (any tile stored anywhere in the layer freezes
   every channel's type) as a defect. Dropped: the principle paragraph
   explicitly and self-consciously gives this up ("a re-type... [is a]
   rewrite... even where a particular file would survive [it] in place,
   because deciding which files would is the edge this list exists to
   remove") — this is the stated design intent of the closed-list rewrite,
   not an unintended side effect.
2. Considered flagging the loss of the old filter-identity-shuffle carve-out
   (R-COD-10, permitting a filter change when the mandated stride makes it
   the identity) the same way. Dropped for the same reason — explicitly
   named as a given-up case in the same sentence ("a change of layout,
   codec or filter... are rewrites even where a particular file would
   survive them in place").
3. Considered whether hunk-02's dropped "or which ordinal an entry sits at"
   trigger silently narrowed the re-emission requirement. Verified by case
   analysis (see above) that it doesn't — ordinal moves are a strict subset
   of entry_count changes under the growth-only regime. Dropped.
4. Scanned for NESTED_DASH across all seven hunks' new text specifically
   (not the whole document) — found none; every em-dash pair in the
   inserted text is a single unnested pair.

## Confidence / what an empty-findings result would have needed

Not applicable — findings were produced. For completeness: had I found
nothing, the check that would most likely have caught something anyway is
the §7.4 partition-versus-two-lists cross-check (Y-01's method), because
that is the one check-6-style structural sweep ("list every field/quantity
the structure carries, ask whether each is decided") that a purely
sentence-level read of hunk-03 cannot substitute for.
