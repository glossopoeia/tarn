# Audit transcript — hunks 08, 09, 10, 11 (§20.3 step 4 and its Example)

## Access / disclosure

Read exactly:
- `/Users/robertkleffner/Documents/GitHub/tarn-first-draft/spec/tarn.md` (via `Read` at offset 3125/280, offset 1085/50, offset 1620/75, offset 1690/60(?), offset 3782/140, offset 3921/50, offset 4040/30, offset 4175/30 — see tool calls below).
- Hunk files `hunk-08.diff`, `hunk-09.diff`, `hunk-10.diff`, `hunk-11.diff` under `.../r33-audit/case/`.

Did NOT read: `full.diff`, other hunk files, docs/, PLAN.md, AGENTS.md, git history, registry.json, or any URL.

**Contamination disclosure.** My context (system reminder / MEMORY.md) contained pre-existing project memory notes with titles like "TARN repair prose vs rules", "TARN repair list vs diff", "no nested em-dash phrases", "TARN permissions, not carve-outs", and git log subjects naming prior rounds' commit messages (e.g. "eighteen defects in the closed list's own wording", "the edit model as a closed list of permissions"). These appeared in the system reminder / gitStatus block before I did any work. I did not open any of the memory files (only titles were visible), and I have not treated any of it as evidence about this round's document — I independently re-derived every finding below directly from the spec text and the hunk diffs. I flag this because the rule requires flagging any such appearance, not because I used it.

Scratch files written: only this transcript. No scratch scripts were needed beyond a short inline Python snippet run via Bash for whitespace-normalized string counts (not saved to a file — run and discarded; its full source and output are quoted verbatim below under "Sweeps run").

## Hunk files as given

```
hunk-08.diff: lands at spec/tarn.md lines 3194-3207 (current file), inside §20.3 step 4's
  declaration paragraph. Header says nearest preceding heading is line 3125 "20.3 The append
  procedure". Verified: reading the live file at that location confirms the surrounding
  text ("An appender MUST, in order: ... 4. Write payloads and indexes ...") matches. No
  discrepancy.

hunk-09.diff: lands at lines 3233-3236, same subsection (the "line is drawn" / witness
  paragraph). Verified against live file — matches, no discrepancy.

hunk-10.diff: lands at lines 3264-3273, the "bounds ... not offered as exhaustive" paragraph
  and the channel-removal sentence. Verified against live file — matches, no discrepancy.

hunk-11.diff: lands at line 3358, inside the ">" Example block, shape (c). Verified against
  live file — matches (line 3357-3358 in the read: "... is re-declared freely, subject to
  every rule its new declarations are subject to, which is the same step's permission —").
  No discrepancy.
```

All four hunk headers agree with their bodies and with the live file. No path or header
mismatch to report.

## The full passage read (spec/tarn.md lines 3125-3404)

I read the whole of §20.3's step 4 (lines 3170-3287), the two Notes/Examples that follow it
(3299-3372), and the boundary into §20.4 (3373-3404), plus the two steps flanking step 4
(steps 3 and 5, lines 3169, 3288-3289) as instructed. Full quotation of the load-bearing
paragraphs is reproduced inline below as each hunk is discussed, rather than repeated here
in full, to keep this transcript navigable; the exact byte ranges I viewed are recorded in
the tool-call log (offset 3125, limit 280).

I also read, because the hunks require it:
- §7.4 (the layer record field table), lines 1090-1134, to get the authoritative field list
  (name, layout, linearization, codec, filter, alignment A, slab S, slab alignment A_slab,
  rank d, channel count C, dimension entries {name, extent, tile extent}, channel entries
  {name, type, fill}, index_encoding, entry_count, crc_of_crc_array, sub-records) and
  R-CNT-16's slab/alignment mutual-exclusivity rule (line 1126-1128).
- §11.1-11.4 (Geometry, grid arithmetic, linearization/R-GEO-06), lines 1620-1749, for the
  Rationale restatement of the append rule (line 1643-1665) and the disk-ordinal formula
  R-GEO-06 gives (line 1727-1740).
- §21.4 (tile-scope violations register), lines 3782-3818, in full, for the T-row texts
  T1-T26.
- §21.6-21.7 (non-violations; what no check detects), lines 3853-3967, in full, for the
  "structurally constrained content" sentence hunk 09 is checked against.
- §21.8 boundary (line 3969) to confirm I read all of §21.7.
- Two more restatement candidates found by grep: line 4048-4069 (hard limits list) and line
  4183-4204 (§23.1 deletion-is-not-erasure, which restates "shortening a planar layer's
  channel list from its end") — read to check for an unswept restatement (see hunk 08
  section below).

## Sweeps run

All exact commands and outputs:

```
$ grep -n "net change|net effect" tarn.md        -> (not run this way; see below, ERE needs -E)
$ grep -n "slab declaration\|alignment declaration\|R-SLB" tarn.md | head -60
  -> 20 hits, incl. line 1127 "per-tile alignment and slab declarations are mutually
     exclusive", line 1650, line 3195, 3246, 3284 (all examined above).

$ grep -n "interleaved layer" tarn.md   -> 11 hits
$ grep -n "planar layer" tarn.md | head -40   -> 16 hits (all examined; list in transcript
     body).

$ grep -n "R-GEO-06\|R-GEO-01\\b" tarn.md
  -> lines 1636, 1663, 1740, 2995, 3023, 3182, 3263, 3763 (8 hits). Opened 1663-1749 (the
     definition + Rationale) and 3182/3263 (the two step-4 uses).

$ awk 'NR==3190,NR==3288' tarn.md | grep -n "list"   -> 9 hits (used for the "the list
     above" anaphor resolution in hunk 10 — see below). Verbatim hits:
     5: "list MAY be extended at its end or shortened from its end, but not"
     9: "and a shortening of one channel list excepted: a commit's net"
     10: "change to a planar layer's channel list is an extension or a"
     16: "an interleaved layer's channel list (its names aside), and the"
     20: "fresh file_id (`[R-LIF-01]`, §20.5). Between them the two lists"
     22: "both sides — a dimension extent, a planar layer's channel list —"
     62: "filter, any change to an interleaved layer's channel list, and a"
     64: "list are rewrites even where a particular file would survive them"
     65: "in place, because deciding which files would is the edge this list"
     78: "changes are permitted is what the list above states. A channel"

$ python3 (inline, via Bash) — whitespace-normalized substring counts over the whole file,
  to guard against the hard-wrap false-zero failure mode the charter warns about:

    import re
    text = open('tarn.md').read()
    norm = re.sub(r'\s+', ' ', text)
    for phrase in ["net change", "replacing the last channel", "two commits or a rewrite",
                   "its names aside", "declarations it produces satisfy every rule"]:
        print(phrase, "->", norm.count(phrase))

  Output:
    net change -> 1
    replacing the last channel -> 1
    two commits or a rewrite -> 1
    its names aside -> 1
    declarations it produces satisfy every rule -> 1

  Control used: each of these phrases is one I had just read verbatim in the live file at
  the hunk's landing line, so a zero would have been diagnostic of a broken search; all
  five came back 1, confirming the normalisation works and that none of these phrases is
  restated (or pre-defined) anywhere else in the document. In particular "net change" is
  used exactly once in the whole spec — nowhere is it given a formal definition — which is
  load-bearing for finding A-01 below.

$ grep -c "^| T[0-9]" tarn.md    -> 26   (control: §21.4's own prose says "26 conditions";
     matches exactly — the table is internally consistent, confirming I have the right,
     complete row set to check hunk 09's witness list against.)

$ sed -n '3190,3360p' tarn.md | grep -n "exactly as\|same way\|on the model\|transposed from\|for the same reason\|likewise\|following \|the model is"
  -> 1 hit: "following the tile" (line 52 of the range, i.e. spec line ~3241) — read in
     context, this is "the re-emission clause above following the tile", not an
     analogy-to-another-rule construction (check 7 target phrase), so no check-7 candidate
     in these hunks.

$ grep -n "T21\|T22" spec section 21.4 (read directly, not grepped separately) — confirmed
  T21 (zstd window > tile decoded size) and T22 (zstd Frame_Content_Size ≠ tile decoded
  size) exist as distinct rows from T3/T14, both "reader"/"tile use", governing rule
  `[R-COD-06]`.
```

## Hunk 08 — the permitted list and its exception

**Text as repaired** (spec lines 3190-3223, my own paraphrase of the rule it adopts first):

> The rule this repair adopts: for a layer that stored a tile in the prior generation, a
> single commit may (a) rename the layer/dimensions/channels, (b) grow (never shrink) an
> extent, (c) either extend a planar channel list at its end or shorten it from its end —
> never both to the *same* list in the same commit — and (d) declare/re-establish/clear a
> slab-or-alignment declaration; several of (a)-(d) may be combined in one commit except
> that a single commit's channel-list delta must net out to a pure extension or a pure
> shortening (not "replace the last channel", which needs two commits or a rewrite).
> Everything else about a layer that stored a tile is frozen.

### Check 1 (tense/quantifier)

The paragraph is explicitly scoped: "A layer that stores a tile **in the generation this
commit supersedes** keeps its declarations..." — this is the PRIOR generation's stored-tile
set, and the whole paragraph (unchanged by this hunk) already fixes that tense; the hunk's
new clauses inherit it correctly (both "an extension and a shortening of one channel list"
and "a commit's net change" are stated as properties of *this* commit relative to that prior
state). No tense drift introduced.

### Check 2 (citations)

No new bracketed requirement IDs are introduced by hunk 08's own diff lines. The nearby
`[R-LIF-01]` citation (context, unchanged) was independently checked in the surrounding read
and is unaffected.

### Check 3 (normative placement)

The whole paragraph is plain, unlabeled prose inside numbered step 4 — not inside a
Note/Example/Rationale block (those begin later, at line 3299). It is normative under
R-CNF-01. Confirmed by re-reading the block boundaries: the nearest preceding ">" block is
the whole document's front matter; there is no ">" marker anywhere near lines 3190-3287.

### Check 4 (local contradiction) — the § 11.1 Rationale restatement

I found and read the restatement at lines 1643-1665 (§11.1, labeled **Rationale.**, hence
non-normative): "a planar layer's channel list may be extended or shortened at its end, one
or the other in a commit". This already states the "one or the other" (not-both) rule *at
the coarse level* — consistent with hunk 08's new "but not both in one commit" wording. It
does **not** restate the "net change" nuance or the "replacing the last channel" case, but
because it is Rationale (non-normative, deliberately a compressed summary) this is not a
sweep failure — it was already coarse before this round's repair and remains coarse and
correct at that grain afterward. Also checked §23.1 (line 4183-4204, "shortening a planar
layer's channel list from its end") and the hard-limits list (line 4048-4069): neither
restates the extend/shorten rule at a level of detail this hunk's edit would invalidate.
**No unswept restatement found for the "not both" / "net change" wording itself.**

However, I did find a **live contradiction candidate one paragraph downstream of the hunk,
in text the hunk did not touch** — see Finding A-02 below (the "on both sides" enumeration).

### Check 5 (exhaustive claims) — run over PAIRS, as the charter specifies

Enumerated permitted-change members: (1) name/dimension-name/channel-name change, (2) extent
growth, (3) channel-list extension at the end, (4) channel-list shortening from the end,
(5) slab-or-alignment declare/re-establish/clear.

For each required pair:

- **Extension + extent growth.** Not the excepted pair (different fields). Mechanism
  paragraph: "an appended planar channel adds tiles at ordinals after every existing one, a
  disk ordinal being c · N + s with N the spatial-tile count" — this correctly uses the
  *post-commit* N, so it composes correctly with a simultaneous growth that changes N.
  Justification ("a name enters no map"-style reasoning doesn't apply here; the relevant
  justification is the disk-ordinal formula itself) remains true of the pair. **Decided,
  consistent.**

- **Shortening + extent growth.** Not the excepted pair. Derived under R-GEO-06 (see hunk 10
  section below, which the charter also drives through this same derivation): shortening
  removes only the top channel's own tiles from the addressed set (its own justification,
  "a channel removed from the end takes only its own tiles out of the addressed set");
  growth's ordinal-renumbering is orthogonal (governs c·N+s for the survivors via N and s,
  not via which channels exist). The two justifications remain independently true when
  composed. **Decided, consistent.**

- **Growth of two different dimension extents at once.** Not the excepted pair (same field
  type, two different dimensions — the base bullet only names "an extent" singular, without
  a per-commit dimension limit). R-GEO-06's formulas (Gᵢ = ⌈Eᵢ/Tᵢ⌉, N = ∏Gᵢ, s = Σᵢ tᵢ·∏_{j>i}Gⱼ)
  are already stated generally over *all* dimensions at once — nothing in the formula or the
  step-4 text restricts it to one dimension growing at a time. **Decided, consistent; no
  defect found.**

- **A rename (name/dimension/channel names) with any other permitted change.** The mechanism
  paragraph's justification for renaming is "a name enters no map" — true regardless of what
  else composes with it, since renaming never touches the addressed-tile set, ordinals, or
  byte layout. **Decided, consistent.**

- **Slab cleared with alignment declared.** R-CNT-16 (line 1126-1128) requires the *final*
  state to have at most one of {A, S} nonzero — clearing S to 0 while setting A to nonzero in
  the same commit satisfies R-CNT-16 in the resulting declarations, and is not the excepted
  pair (different declaration entirely from the channel list). Justification: "a slab or
  alignment declaration governs placement (§16), not a value, its coordinate or its
  padding" — true of the composed pair (still only about placement). **Decided, consistent;
  no defect found.**

- **Extension and shortening of one channel list — the named exception.** This is where I
  found the strongest defect. See **Finding A-01** below.

I also ran the charter's specific sub-questions on the exception's own wording:

- *Does "net change" have a definition?* No — confirmed by the whitespace-normalized sweep
  above: the phrase "net change" occurs exactly once in the whole document, in this hunk's
  own new sentence. It is used but never defined.
- *Does "one channel list" reach an interleaved layer?* No, and correctly so: an interleaved
  layer's channel list is entirely on the fixed side (list structure, "its names aside");
  the extend/shorten permission is stated only for "a planar layer's channel list", so the
  exception (which is phrased "of one [planar] channel list", by cross-reference to the
  sentence's own subject two clauses earlier) does not and should not reach interleaved
  layers. Verified: no defect here.
- *Does "two commits or a rewrite" say which two?* It doesn't name an order (shorten-then-
  extend vs extend-then-shorten), but I could not construct a scenario where order matters:
  each commit independently satisfies the single-item permission and the layer's declared
  state after each commit is independently valid, so under-specifying order is not a defect
  — it's a case where either order is genuinely fine and the text is correctly silent.

### Check 5 continued — the tie-break sentence and "(its names aside)"

- *Tie-break sentence "the permitted side states the whole of what a commit MAY do to it"
  still holds now that the permitted side carries a "not both"?* Yes — the tie-break's job
  is to say that everything the permitted side does NOT license is fixed by default; adding
  "but not both in one commit" to the permitted side only narrows what it licenses, which the
  tie-break's own logic already accommodates (narrower licence, same fallback-to-fixed
  structure). No contradiction.

- *"(its names aside)" against the partition claim's list of fields on both sides, and
  against the permitted list's "channel names"* — this is **Finding A-02**, detailed below.

### Check 6 (unconstrained siblings)

The structure here is the closed permitted/fixed pair over every §7.4 field. I walked every
§7.4 field (line 1096-1113) against the two lists: name (permitted), layout (fixed),
linearization (fixed), codec (fixed), filter (fixed), alignment A / slab S / slab alignment
A_slab (permitted as a pair via the slab-or-alignment bullet), rank d (fixed), channel count
C (implicitly governed via the channel-list bullet for planar, via "(its names aside)" for
interleaved), dimension entries' name (permitted) / extent (permitted, grow-only) / tile
extent (fixed), channel entries' name (permitted) / type (fixed) / fill (fixed),
index_encoding (fixed), entry_count (explicitly "follows the commit" — derived, not itself
independently declared), crc_of_crc_array (same), sub-records ("§20.4's subject... whether or
not the layer stores a tile" — explicitly carved out to a different rule). I did not find a
§7.4 field left ungoverned by either list. No new Finding under check 6 for hunk 08.

### Check 7 (analogy)

No "exactly as / same way / on the model" construction inside hunk 08's new text (confirmed
by the grep above). Not applicable.

### Check 8 (anaphora — text hunk 08 inserted)

Hunk 08 inserts "but not both in one commit" and the whole "an extension and a shortening of
one channel list excepted: ..." clause. Back-references inside the inserted text: "one
channel list" (resolves to "a planar layer's channel list", the subject two clauses earlier
in the *same* sentence — not a long-range anaphor, resolves cleanly). No pronoun or "the X
above" phrase is introduced by this hunk that reaches outside its own sentence. Forward
effect: I checked whether anything *after* the insertion re-resolves — see Finding A-02
(the "Between them..." sentence, which is downstream, unchanged, but now stale given the
new "(its names aside)" upstream of it).

### Findings — hunk 08

**A-01 [OVERCLAIM / UNDERSHOT].** The exception's own gloss — "a commit's net change to a
planar layer's channel list is an extension or a shortening" — decides the *net-zero*
compose case ("replacing the last channel") but does not decide, and on its literal wording
appears to *permit*, an *asymmetric* compose: removing K2 trailing channels and appending K1
new ones in the same commit where K1 ≠ K2. Net change there is nonzero (an extension if
K1>K2, a shortening if K1<K2), so the disjunction "is an extension or a shortening" is
satisfied by the letter of the text, yet the operation still *composes* a removal-run and an
addition-run exactly as "replacing the last channel" does — the very shape the exception
exists to forbid, since the newly appended channels are not "channels that stored a tile in
the generation this commit supersedes" and so their type/fill are NOT fixed by "every
channel's type and fill", letting a writer effectively replace the *type* of channels near
the tail while nominally staying inside a single net-shortening or net-extension label. I
verified the base bullet's plain-language "not both in one commit" would forbid this (it
does not condition on net effect), but the exception's *gloss*, which is the only place the
disjunction is spelled out, contradicts that plain reading by defining the exception in terms
of net effect rather than in terms of "add and remove both occurred". Two competent readers
of the repaired text could reach opposite verdicts on whether such a commit — remove 3
trailing channels, append 5 new ones, all in one commit on a planar layer that previously
stored tiles — is conforming.
- Byte-level: **yes**. Under the permissive (net-effect) reading a writer may legally emit
  such a commit (new channel types unconstrained by any prior generation); under the strict
  (no-compose) reading the same commit is invalid and the writer must split it into two
  commits or a whole-file rewrite. The conforming/nonconforming boundary for this exact file
  shape differs between the two readings, so the emittable/acceptable byte set moves.
- Repair: replace the net-effect gloss with an unconditional one, e.g. "an addition at the
  end and a removal from the end are not both permitted in the same commit, regardless of
  their counts; only a commit whose channel-list delta is purely additions or purely
  removals is a shortening or an extension for the purposes of this list."

**A-02 [UNSWEPT_RESTATEMENT].** The unchanged sentence a few lines below hunk 08's edit —
"Between them the two lists reach every declaration field of §7.4, and where a field is on
both sides — a dimension extent, a planar layer's channel list — the permitted side states
the whole of what a commit MAY do to it" — enumerates the fields split across both lists as
exactly two: a dimension extent and a planar layer's channel list. Hunk 08 itself introduces
a *third* such split field by adding "(its names aside)" to "an interleaved layer's channel
list" in the fixed list: that parenthetical means an interleaved layer's channel list is now
*also* split — its structure/membership fixed, its names permitted (via the separate,
layout-agnostic "its name, and its dimension and channel names, MAY change" bullet). The
"Between them..." sentence was not sled to mention it, so its enumeration now undercounts the
straddling fields by one.
- Byte-level: **no**. The tie-break principle itself ("the permitted side states the whole
  of what a commit MAY do to it") is still true of the omitted third field too (the general
  name-change bullet does state the whole of what may be done to an interleaved layer's
  channel-list names); only the illustrative enumeration is incomplete. No implementation's
  accept/reject verdict turns on this sentence's example list.
- Repair: append ", an interleaved layer's channel list" to the "on both sides" example list,
  or drop the specific examples and just say "and where a field is split between them, the
  permitted side states the whole of what a commit MAY do to it."

## Hunk 09 — the witness parenthetical

**Text as repaired:** "...with every checksum in §8 certifying the result and, but for a
decoded size, a padding position or pad bit, or a boolean byte the register witnesses (T3,
T14, T4, T5, T2), no check any actor owes able to see it (§21.7)."

**The rule this repair adopts:** of all the content a stored tile's bytes could be
misinterpreted as denoting if the fixed declarations were (wrongly) changed, only decoded
size, padding-position content, pad-bit content, and boolean-byte validity are witnessed by
any check a reader or verifier owes — everything else is invisible to every obliged check.

### Check 2 (citations) — every T-row and the §21.7 sentence

- **T2** (line 3793): "In an interleaved tile, a bool channel's single value byte at a real
  (non-padding) sample position is neither 0x00 nor 0x01; the same byte at a padding
  position is T4's, the two rows together covering `[R-SER-08]`." — Matches "a boolean byte"
  exactly, and its own text hands the padding-position half to T4, so T2+T4 jointly and
  exclusively cover R-SER-08. **Verified correct.**
- **T3** (line 3794): "The decoded payload's byte length is not exactly the tile's decoded
  size derived from the layer's declarations" — governing rule `[R-SER-07]`. Matches "a
  decoded size" exactly, codec-agnostic (its Instances column varies only by
  interleaved/planar/packed shape, not by codec). **Verified correct.**
- **T4** (line 3795): "A padding position does not encode, for each channel it carries, that
  channel's recorded fill value" — governing rule `[R-SER-05]`; instances cover interleaved
  numeric, interleaved bool, planar numeric, and packed planar bool. Matches "a padding
  position" exactly and completely (all four shape combinations). **Verified correct — this
  is the row hunk 09 newly adds, and it is the right one.**
- **T5** (line 3796): "In a packed planar bool plane with P mod 8 ≠ 0, a final-byte pad bit
  ... is not the channel's fill bit" — governing rule `[R-SER-05]` (R-SER-03). Matches "pad
  bit" exactly — this is a genuinely distinct concept from T4's "padding position" (T5's pad
  bits are sub-byte packing slack beyond the tile's P sample count; T4's padding positions
  are real grid coordinates ≥ the dimension extent). **Verified correct — the other row
  hunk 09 newly adds, and it is the right one.**
- **T14** (line 3805): "Codec 1 (none) declared and a non-sentinel index entry's length
  differs from the tile's decoded size" — governing rule `[R-COD-04]`. A second, codec-1-
  specific decoded-size witness (pre-decode, on the index entry's length field directly
  rather than post-decode). **Verified as a legitimate decoded-size witness.**
- **§21.7's own sentence** (line 3922-3924): "The obligations of §14.5 and `[R-SER-08]`
  narrow this only where content is structurally constrained: padding positions, pad bits,
  and boolean bytes." This names exactly three categories — padding positions, pad bits,
  boolean bytes — corresponding one-to-one to T4, T5, T2. It does **not** name "decoded
  size" at all, but that is not a contradiction: decoded size (a byte *count*) is *structure*
  under §21.7's own opening framing ("this format detects corruption of structure, not
  incorrectness of content"), not "content" in the sense this sentence is narrowing, so T3
  and T14 sit outside the three-category list on entirely legitimate grounds. **Verified
  consistent, not a defect.**

### Check 5 (exhaustive claim) — is the parenthetical "no more and no fewer"?

Running the charter's specific instruction — "say whether the enumeration is now exactly the
register's witness set for a fixed-declaration change, no more and no fewer" — against all
26 rows of §21.4 (count independently confirmed via `grep -c "^| T[0-9]" tarn.md` = 26,
matching the register's own stated "26 conditions"):

For the three §21.7-named content categories (padding position, pad bit, boolean byte), the
parenthetical's T4/T5/T2 are exactly right — no other row in the table concerns any of these
three. Confirmed exhaustively: I read all 26 rows; the only other rows that mention "fill"
or "padding" language are T4 itself and T26 ("Filter 2 applied at a stride other than the
mandated one... the check that detects it is T2's or T4's" — T26 self-declares it adds no new
detection capability, so it is correctly not separately cited).

For the "decoded size" category, I found two further candidate witnesses the parenthetical
omits:
- **T21** — "Codec 3 (zstd) and the frame declares a window size larger than the tile's
  decoded size" (`[R-COD-06]`).
- **T22** — "Codec 3 (zstd) and the frame's Frame_Content_Size field is present but does not
  equal the tile's decoded size" (`[R-COD-06]`).

Both check the tile's *decoded size as computed from the layer's declarations* against a
value the writer embedded in the stored zstd frame at write time — structurally identical in
kind to what T14 does for codec 1 (a pre-decode, codec-specific decoded-size witness). If a
fixed declaration were (hypothetically) changed after the fact, re-deriving the tile's
decoded size from the new declarations and comparing it against the *unchanged, already-
stored* zstd frame's own Frame_Content_Size/window fields would trip T22 (and, depending on
direction of the size change, T21) exactly as changing codec-1's stored length trips T14.
The parenthetical includes T14 for this reason but omits T21/T22, which sit at the identical
level of specificity for a different codec.

- Byte-level: **no**. T3 alone (codec-agnostic, always fires on any decoded-size mismatch
  regardless of codec) already establishes that "decoded size" is witnessed in every case;
  omitting T21/T22 does not create an actual detection gap or change any accept/reject
  verdict, it only makes the parenthetical's citation list inconsistent in how finely it
  itemizes per-codec redundant witnesses (fine-grained for codec 1 via T14, coarse for codec
  3, absent for codec 2/4 where no analogous pre-decode field exists at all).
- Confidence: moderate — this is a citation-completeness inconsistency, not a substantive
  hole, and it predates this specific hunk (T14 was already present before hunk 09; hunk 09
  only added the T4/T5 pair, which I found fully correct). I report it because the charter
  asks explicitly whether the *current* enumeration is exactly right, "no more and no
  fewer," and by that literal standard it is not — though the inconsistency was not
  introduced by hunk 09 itself.
- Repair: either add ", T21, T22" after T14, or reword to "a decoded size the register
  witnesses at least at T3, T14 (and, for zstd, T21-T22)", or simply drop the specific-row
  citation for decoded size and keep it only for the newly-added padding/pad-bit/bool-byte
  set, which is where hunk 09's own contribution is fully correct and exhaustive.

### Checks 1, 3, 4, 6, 7, 8 for hunk 09

- **Check 1:** the actor is named correctly and consistently — "no check any actor owes able
  to see it" tracks §21.7's own "checks this specification obliges a reader or a verifier to
  perform" (line 3946-3947). Quantifier match confirmed.
- **Check 3:** plain prose, not inside a blockquote (confirmed, same paragraph as hunk 08,
  already checked above). Normative.
- **Check 4:** no contradiction found elsewhere in the passage from adding T4/T5.
- **Check 6:** the structure here is "the set of register rows witnessing a given content
  category" — I named all members (T2, T3, T4, T5, T14, and the T21/T22 candidates above);
  no other member left unconstrained beyond A-03 above.
- **Check 7:** not applicable (no analogy construction in this hunk's text).
- **Check 8:** the hunk inserts "a padding position or pad bit" and ", T4, T5" mid-list; no
  back-reference is created or disturbed (it's a flat parenthetical list, not a referring
  phrase), and nothing after this sentence refers back to "a decoded size... (T3, T14, T2)"
  by name that would need re-resolution.

### Finding — hunk 09

**A-03 [UNDERSHOT].** As detailed above: the "decoded size" portion of the witness
parenthetical (T3, T14) omits T21 and T22, the codec-3 analogs of T14's codec-1-specific
witnessing, while the newly-added padding-position/pad-bit/boolean-byte portion (T4, T5, T2)
is fully correct and exhaustive against §21.4's 26 rows and §21.7's three-category list.
Not byte-level (see rationale above); flagged because the charter's "no more and no fewer"
standard is not met by the sentence as it now reads.

## Hunk 10 — the bounds paragraph's close and the channel-removal sentence

### Part (a): "These bounds are not offered as exhaustive..."

**Before:** "The list is not offered as exhaustive: a change is permitted exactly where the
declarations it produces satisfy every rule they are subject to."

**After:** "These bounds are not offered as exhaustive: a permitted change holds exactly
where the declarations it produces satisfy every rule they are subject to, and which changes
are permitted is what the list above states."

**The rule this repair adopts:** splits what was one test into two: (i) whether an operation
is *of a permitted type at all* is decided solely by the closed list in step 4's earlier
paragraph ("the list above"); (ii) whether the declarations that operation *produces* are
*valid* ("holds") is a separate, open-ended test against every applicable rule, not limited
to the four bounds just cited (R-COD-07, R-ENC-04, R-GEO-01, §4.6/R-ENC-15).

- **Check 8 (anaphor) — "the list above".** Going backward from the insertion point: the
  nearest textual occurrence of the bare word "list" is at spec line ~3253-3255 (hit #64-65
  in my `awk`/`grep` sweep above): "...are rewrites even where a particular file would
  survive them in place, because deciding which files would is the edge **this list** exists
  to remove." That "this list" already refers to the *original* closed permitted-changes
  list from the top of step 4's declaration paragraph (the "with these exceptions and no
  other" list), not to the "gives-up" enumeration it sits inside (a shrink, a fill change, a
  re-type, ...). Because "this list" — the nearest prior occurrence of the word — already
  carries that referent, "the list above" (13 lines later) naturally continues the same
  referent rather than picking up a nearer-but-wrong one. **Resolved correctly: "the list
  above" = the closed enumeration of permitted changes ("with these exceptions and no
  other..."), not the four-bound citation list two sentences earlier (called "these bounds"
  in the very same sentence, so it cannot also be "the list above") and not the "gives-up"
  rewrite enumeration immediately preceding.** No anaphor defect found for this phrase.

- **Check 8 (anaphor) — "under the clause above"** (this appears in part (b), see below, but
  I resolve it here since it's the same check). This phrase is new text (see the diff). Going
  backward, it resolves to step 4's own opening re-emission trigger, line 3172-3174: "Every
  layer whose stored-tile set or index content this commit changes has its tile-index region
  re-emitted in full" — the only sentence in step 4 establishing a general "index content
  changed → full re-emission" rule, and the new sentence deliberately echoes its exact
  phrase "index content" ("...and changes the layer's index content, so the region is
  re-emitted under the clause above"). Despite the ~90-line distance, the shared vocabulary
  makes the antecedent identifiable. **No anaphor defect found.**

- **Check 4/1 — "holds" vs. "is permitted" as two predicates.** I checked whether this
  split is itself new or already established: the paragraph's *own opening sentence*, one
  sentence before the touched text and unchanged by this hunk — "A permitted change **holds**
  provided the declarations and geometry it produces stay within every bound they are
  subject to:" (line 3257) — already uses "holds" in exactly this sense. So the repaired
  sentence's reuse of "holds" is consistent with, not a novel departure from, the paragraph's
  own established vocabulary. **Verified consistent — this is a good repair**, correctly
  separating "which operations are permitted" (closed list) from "when a permitted
  operation's result is valid" (open-ended bound satisfaction), fixing a real pre-existing
  ambiguity in "a change is permitted exactly where declarations satisfy every rule" (which
  could previously be misread as making bound-satisfaction alone sufficient for permission,
  bypassing the closed list). I also confirmed the "not exhaustive" claim is independently
  true and useful: R-CNT-16 (slab/alignment mutual exclusivity, line 1126-1128) is a real
  rule a permitted change's declarations must satisfy that is *not* one of the four named
  bounds — good concrete evidence the "not exhaustive" qualifier is warranted, not decorative.

No finding for part (a); checked and passed.

### Part (b): the channel-removal sentence

**Before:** "A channel removed from the end leaves its stored tiles' extents as slack (§5.2),
and `[R-CNT-17]` obliges the smaller entry_count and so a re-emitted index region;"

**After:** "A channel removed from the end leaves its stored tiles' extents as slack (§5.2)
and changes the layer's index content, so the region is re-emitted under the clause above:
the shortening taken alone lowers entry_count (`[R-CNT-17]`), and one taken with a growth
moves ordinals whether or not the count changes;"

**The rule this repair adopts:** re-emission is now justified generically ("changes the
layer's index content", tying back to step 4's general trigger) rather than solely via
entry_count; and it asserts, as a mechanism claim, that combining a channel-list shortening
with *any* extent growth in the same commit moves (renumbers) ordinals, independent of
whether "the count" changes.

**Deriving the two charter-specified cases from R-GEO-06** (line 1737-1740): "the **disk tile
ordinal** ... is s for an interleaved layer, and **c · N + s** for a planar layer ... where c
is the channel's index" — with N = ∏Gᵢ and s = Σᵢ tᵢ·∏_{j>i}Gⱼ (line 1671, 1727-1736).

- **Case 1 — shortening + a growth that changes NO grid count.** §11.1's Rationale (line
  1657-1659, itself consistent with, and here corroborated by, step 4's own normative text
  at line 3181-3182: "a growth renumbers ordinals wherever `[R-GEO-06]` moves them, and
  nothing else this step permits moves one") states such a growth "moves no entry and adds
  none". Deriving directly from the formula: if no Gᵢ changes, then N (=∏Gᵢ) is unchanged,
  and for every *existing* tile (same tile coordinates tᵢ), s is unchanged (s depends only on
  tᵢ and the Gⱼ's). Shortening removes only the top channel (c = C−1); every *retained*
  channel keeps its own index c unchanged. So for every retained tile, c, N, and s are **all
  three unchanged** — the disk ordinal c·N+s is identical before and after. **No ordinal of
  any surviving entry moves in this case.** entry_count still drops (the removed channel's N
  tiles are gone), so re-emission is still correctly triggered — but not because any ordinal
  moved.
- **Case 2 — shortening + a growth that doubles N.** For any retained channel c ≥ 1, the
  c·N term changes from c·N₀ to c·(2N₀) — a nonzero shift regardless of what happens to s —
  so the disk ordinal necessarily moves for every tile in every channel c ≥ 1. **Ordinals do
  move in this case,** matching step 4's general "a growth renumbers ordinals wherever
  R-GEO-06 moves them" rule (line 3181-3182) for a growth of the kind that changes a grid
  count.

**Result:** the new sentence's claim — "one taken with a growth moves ordinals **whether or
not the count changes**" — is stated as an unconditional property of "a growth" (indefinite,
unqualified, parallel in construction to "the shortening taken alone" in the clause right
before it, which is also unqualified/universal). Case 1 is a direct counterexample: a
shortening combined with a growth that changes no grid count moves *no* ordinal at all. The
claim is true of Case 2 and false of Case 1.

### Findings — hunk 10 part (b)

**A-04 [LOCAL_CONTRADICTION].** "one taken with a growth moves ordinals whether or not the
count changes" contradicts step 4's own already-standing, unchanged, normative sentence at
line 3181-3182 — "a growth renumbers ordinals wherever `[R-GEO-06]` moves them, **and nothing
else this step permits moves one**" — which makes ordinal movement conditional on the
specific growth (via R-GEO-06), not a property that "a growth" (any growth) guarantees. I
derived, from R-GEO-06's own formula, a concrete growth (one that changes no grid count) that
demonstrably moves no ordinal even combined with a shortening, directly falsifying the new
sentence's unconditional wording. The contradicting quotation is line 3181-3182's "and
nothing else this step permits moves one [ordinal]", in the *same* numbered step, both
passages unlabeled normative prose.
- Byte-level: **no**. The actual controlling rule remains the correct, older sentence at
  line 3181-3182 (unchanged by this hunk), which conditions ordinal movement on R-GEO-06
  correctly; the new sentence is explanatory narration justifying re-emission, and
  re-emission is *independently* and correctly justified by the entry_count drop / addressed-
  tile-set change in both derived cases (Case 1 and Case 2 alike), so no accept/reject
  verdict or emittable byte sequence turns on the overclaim. It is nonetheless a false
  factual statement sitting in normative prose.
- Repair: qualify the clause, e.g. "and one taken with a growth that renumbers ordinals (per
  the clause above) moves them whether or not entry_count itself changes" — or drop the
  clause, since re-emission is already fully justified by "changes the layer's index
  content" one clause earlier without needing this sub-claim at all.

I also checked whether "whether or not the count changes" might instead mean *entry_count*
specifically (the nearest count-word, one clause earlier) rather than *grid count*. Under
that reading the sentence would be making a narrower claim ("ordinals move even when
entry_count doesn't"), but Case 1 refutes that reading too: entry_count *does* change in
Case 1 (shortening alone lowers it), and ordinals still do not move — so under either
reading of "the count," the sentence's "moves ordinals" half is false for Case 1. This
strengthens A-04 rather than resolving it.

## Hunk 11 — shape (c), "declarations" for "geometry"

**Before:** "A layer that stored no tile in the generation the commit supersedes is
re-declared freely, subject to every rule its new **geometry** is subject to, which is the
same step's permission — a layer the commit itself empties does not qualify."

**After:** "...subject to every rule its new **declarations** are subject to, which is the
same step's permission..."

**The rule this repair adopts:** aligns the Example's wording with step 4's own empty-layer
permission sentence word for word.

**Check — held against the step's actual wording**, line 3220-3223: "A layer that stores no
tile in the generation this commit supersedes MAY be re-declared freely, subject to every
rule its **new declarations** are subject to, which is what schema-first creation needs
(§11.1)." Comparing word for word: "subject to every rule its new declarations are subject
to" now appears **identically** in both places (modulo the expected MAY/is tense difference,
appropriate since the Example describes a scenario in the indicative rather than restating
the deontic rule). Before the repair, the Example said "geometry" — a strictly narrower term
than "declarations" (geometry conventionally covers rank/dimensions/extents/tile-extents,
not layout, codec, filter, slab/alignment, or channel type/fill) — which would have wrongly
suggested the empty-layer re-declaration freedom applies only to geometric fields, when step
4's own rule (and §11.1's Rationale, "may be re-declared freely, subject to every rule its
new declarations are under") is explicitly about *every* declaration. **This is a correct,
precise fix**, verified against both the immediate governing sentence (line 3220-3223) and
the §11.1 Rationale's earlier, matching phrasing ("subject to every rule its new declarations
are under", line 1655-1656) — the Example is now finally in step with a wording that §11.1's
Rationale already used.

- **Check 8 (anaphor):** nothing after this sentence in shape (c) refers back to "geometry"
  specifically ("Editing user metadata is not this shape: its document lives in an extent
  ..." — no dependency on the word changed). No forward effect.
- **BCP-14 casing:** no MUST/MAY/SHOULD keyword appears in the touched clause. N/A.
- **NESTED_DASH:** the sentence has exactly one em-dash pair ("— a layer the commit itself
  empties does not qualify."), not nested inside another dash-delimited clause. No
  violation.

No finding for hunk 11 — checked and passed on every applicable check.

## Summary of findings

- A-01 (hunk 08, byte-level): the channel-list exception's net-effect gloss fails to forbid
  asymmetric add/remove compositions, only the net-zero "replace" case.
- A-02 (hunk 08, not byte-level): the "on both sides" field enumeration is stale by one
  entry after hunk 08's own "(its names aside)" addition.
- A-03 (hunk 09, not byte-level): the decoded-size witness citation (T3, T14) is
  inconsistent in granularity, omitting T21/T22 (zstd analogs of T14).
- A-04 (hunk 10, not byte-level): "moves ordinals whether or not the count changes" is false
  for a shortening combined with a grid-count-preserving growth, contradicting step 4's own
  earlier, correct, unchanged sentence about when R-GEO-06 renumbers ordinals.
- Hunk 11: no defect found; a correct, verified-word-for-word repair.
- Hunk 10 part (a): no defect found; a correct repair that fixes a genuine pre-existing
  ambiguity (bound-satisfaction alone could previously look sufficient for "permitted").
- Every pair required by the charter's check-5 pass over hunk 08 was individually worked
  through; only the named exception pair itself produced a defect (A-01).
