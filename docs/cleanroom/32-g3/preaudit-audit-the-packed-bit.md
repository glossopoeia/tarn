# Audit transcript — "the packed bit" (hunks 05, 12, 15, 16, 24)

## Access-rule disclosure

Files read: the five hunk files named in the charter
(`case/hunk-05.diff`, `hunk-12.diff`, `hunk-15.diff`, `hunk-16.diff`,
`hunk-24.diff`), and `spec/tarn.md` (via `Read` at the offsets below, and
via `grep`/`python3 re` scans of the whole file for sweeps). No other
file under `docs/`, `PLAN.md`, `OPEN-QUESTIONS.md`, `AGENTS.md`,
`README.md`, `conformance/`, `spec/registry.json`, git history, or the
web was read. `full.diff` was not read. No hunk file other than my own
five was read. The `case/` directory was not listed.

Commands run: `Bash` calls doing `grep -n`, `wc -l`, and small inline
`python3` scripts that normalize the hard-wrap (`>`-prefixed
continuation lines joined, all newlines collapsed to spaces, runs of
whitespace collapsed to one space) before substring-searching — done
specifically because the document is hard-wrapped and a naive
line-oriented grep would miss phrases that cross a line break, per the
charter's warning. No file was written except this transcript and a
now-empty scratch directory
(`r32-audit/scratch/the-packed-bit/`) created but not used for any
script — all computation was inline Bash/Python one-liners, nothing
persisted.

**Contamination check.** The session's system context (CLAUDE.md,
auto-memory files, environment reminders) named prior round commits
("ADR-0120: PE = 0 licenses the drop...", "ADR-0122: a removed channel
de-addresses its tiles...", "Cleanroom round 31: charter") and general
project lore about repair-defect patterns. None of that material was
about the packed-plane clause specifically, and I did not use any of it
as evidence about this repair — every claim below is derived from
reading the hunk files and `spec/tarn.md` directly and is cited to a
line number or grep output. Flagging its presence per the charter's
disclosure requirement; I did not act on it. The memory file
`tarn-repair-prose-vs-rules.md` and similar are titles only, visible in
the index; I did not open any of them (they are outside the two-file
access rule and I had no need to).

## The five hunks, restated

All five insert the identical clause `, or bit in a packed plane,`
into a sentence of the form "whose stored byte [, or bit in a packed
plane,] already holds the fill …", at five different landings:

- hunk-05: §11.1 "Geometry and its validity floor", inside a
  `> **Rationale.**` blockquote (lines 1629–1664).
- hunk-12: §20.3 step 4, the general §14-bar exception statement
  (lines 3196–3208), inside a larger restructuring not part of my
  charter (see below).
- hunk-15: §20.3 step 4, the growth carve-out (lines 3289–3304).
- hunk-16: §20.3 step 4, the shrink carve-out (lines 3306–3338).
- hunk-24: §23.1 "Deletion is not erasure" (lines 4242–4270),
  pluralized: "those bytes, or bits in a packed plane, already hold…".

Header-vs-body check: every hunk's stated "nearest preceding heading"
matches what I found by reading forward from that heading to the
diff's context lines — no mismatch in any of the five.

Hunks 12 and 15 each carry additional edits beyond the packed-plane
clause (hunk-12 restructures "is not what this bars" / "leaves them
so"; hunk-15 changes "it covers" to "its padding limb covers"). Per
the charter ("Two of your hunks carry larger edits another lane
holds"), I judged only the packed-plane clause in each, though I
checked whether the packed-plane insertion interacts badly with the
surrounding edit (it does not — see Check 8 below).

## The rule each hunk adopts (in my own words)

All five state, in different structures, the same fact: a padding
position's already-stored content is expressed as a **byte** when the
channel is numeric (any layout) or interleaved-bool, but as a single
**bit inside a shared byte** when the channel is a bool channel stored
in a planar (packed) layout — and the various carve-outs/exceptions
throughout the document that turn on "the stored content already
equals fill" must be read at whichever of those two grains actually
applies to the position in question, not always at byte grain.

## Derive the case (per the charter's explicit instruction)

**What a padding position of a packed planar bool plane is stored
as.** §14.3 (lines 2059–2072): a planar bool tile's P values are
bit-packed LSB-first, value k in bit `k mod 8` of byte `k div 8`.
§11.4 (lines 1730–1739): in-tile ordinal u = Σᵢ uᵢ·∏_{j>i}Tⱼ,
row-major, permanent across linearization values. So a padding
position (§11.3: a sample position whose coordinate along some axis
is ≥ Eᵢ but still inside the tile, i.e. ordinal < P) occupies exactly
one bit of some byte in the plane — the *same* mechanism, and the
*same* byte-grouping, as a real position. Nothing distinguishes a
padding position's storage location from a real position's: both are
ordinals 0..P-1, packed 8-to-a-byte.

**What content the rule fixes for it.** §14.5 / `[R-SER-05]` (lines
2126–2137): "at every padding position, a writer MUST encode, for
each channel the position carries, that channel's fill value — the
recorded fill bytes for a numeric channel, the recorded fill byte for
an interleaved bool channel, **the fill bit in a packed plane**."
`[R-SER-05]` already states the bit-grain rule explicitly and has done
so (this is pre-existing, unedited by any of my five hunks). The
register also already has it right: T4 (line 3856) lists "packed
planar bool plane fill bit" as a distinct witness column entry, and T5
(line 3857) is entirely about "a final-byte pad bit … is not the
channel's fill bit."

**Whether the pre-repair wording ("stored byte") reached it.** Not
cleanly. "Stored byte" is accurate for a numeric channel (whose fill
occupies whole bytes) and for an interleaved bool channel (whose fill
is one whole byte, §13.2, `[R-TYP-07]`), but for a packed plane a
"byte" is not a single value's storage — it holds up to 8 independent
ordinals' bits. Read literally, "a padding position whose stored byte
already holds the fill" asks whether an entire byte equals the fill
pattern, which is a **different and stricter condition** than "this
position's bit already equals the fill bit" whenever the byte also
carries other (still-real, still-live) ordinals' bits — which happens
routinely, not as an edge case, whenever an extent shrink lands a new
extent boundary that is not byte-aligned inside a packed plane's value
region (constructed concretely below). So the pre-repair wording did
not reach the packed-plane case correctly; the repair's added
alternative ("or bit in a packed plane") is what makes the sentence
track `[R-SER-05]`'s own bit-grain rule.

**The smallest layer where a shrink makes an in-tile ordinal a padding
position whose bit already holds the fill and whose byte holds other
real values too.** Rank-1 (d=1, so uᵢ reduces per §11.4's stated
convention), one bool channel, planar layout (packed), tile extent
T₀ = 9, fill = false (`0x00`). Superseded generation: E₀ = 9 (grid
count G₀ = ⌈9/9⌉ = 1, P = T₀ = 9, no §11.3 padding at all — every one
of the tile's 9 ordinals is real). Suppose the writer stored, at
ordinals 0–3, real values (1,0,1,1) and, at ordinals 4–8, real values
that happen to equal `false` (0,0,0,0,0) — coincidence, not required by
any rule, just a legal choice of sample data. Byte 0 (ordinals 0–7)
= `0b0000_1011` = `0x0B` reading LSB-first bit0..bit7 = (1,0,1,1,0,0,0,0)
i.e. bits 0–3 = the real (1,0,1,1) values, bits 4–7 = the (also real,
coincidentally-false) values. Byte 1 (ordinal 8 in bit 0, pad bits in
bits 1–7 since P mod 8 = 1) = whatever `[R-SER-05]`/`[R-SER-03]`
already fixes for the tile's final-byte pad bits, unrelated to this
example.

Now the commit: shrink E₀ from 9 to 4. Grid count is unchanged
(⌈4/9⌉ = 1), so the tile is still stored (not dropped), but ordinals
4–8 are now padding positions (coordinate ≥ 4). Ordinals 0–3 remain
real. Byte 0 on disk is untouched (§20.3 step 4's shrink paragraph,
line 3341: "every surviving stored tile is untouched") — it is still
`0x0B`. This byte now holds: 4 real bits (unrelated to fill, still
part of the live state) and 4 newly-padding bits, which happen to
already equal the fill bit (0). Under the pre-repair "stored byte
already holds the fill" wording, read at byte grain, `0x0B` does **not**
equal the fill-byte pattern `0x00` — so a literal byte-grain reading
would say the carve-out's condition fails and this shrink is barred
by the §14 bar (even though nothing that matters was altered: the
newly-padding bits already held fill, and the real bits are unaffected
and untouched). Under the post-repair "bit in a packed plane" reading,
only ordinals 4–8's bits need already equal fill, which they do — the
shrink is permitted, matching `[R-SER-05]`'s own bit-grain content
rule and matching T4/T5's bit-grain witnesses.

**What each of the five sentences now says of this commit**, after the
repair:
- hunk-05 (Rationale, §11.1): "a new padding position whose … bit in a
  packed plane, already holds the fill alters nothing" — true of
  ordinals 4–8 here; the commit is licensed.
- hunk-12 (§20.3 general test): the same clause, now embedded as one
  of the things that "leaves them so" (leaves the tile's stored bytes
  meaning what they meant) — true, byte 0's real bits (0–3) are
  unaffected and its padding bits (4–7) already meant fill.
- hunk-15 (growth carve-out): explicitly says this padding-limb
  clause does *not* reach a growth — correctly inapplicable here,
  since this example is a shrink.
- hunk-16 (shrink carve-out): the direct match — "a new padding
  position whose … bit in a packed plane, already holds the fill …
  is not [such an alteration], so a shrink producing only those is
  permitted" — this is exactly the rule licensing the constructed
  commit.
- hunk-24 (§23.1): "those bytes, or bits in a packed plane, already
  hold the channel's recorded fill" — describes exactly byte 0's
  bits 4–7: their content (0) is derivable from the layer record's
  declared fill (`0x00`) without needing to read the file, so their
  survival as slack-free live padding discloses nothing new. Byte 0's
  bits 0–3 (the real, still-live data) are outside this sentence's
  concern entirely — they are ordinary live sample data, not slack,
  and §23.1 is not making any claim about them.

This confirms the repair's factual content is correct and matches
`[R-SER-05]`'s pre-existing bit-grain rule, and that the pre-repair
"stored byte" wording, taken literally, would have mis-classified this
constructed (and unremarkable) shrink as barred.

## Check 3 — label, not marker

hunk-05 lands inside a blockquote that opens "> **Rationale.**" at
line 1629 (confirmed by reading lines 1611–1665 in full). Per
`[R-CNF-01]` this block is **non-normative**. I checked whether the
packed-plane rule's *only* statement is here (which would be a
defect per the check's own test) — it is not: `[R-SER-05]` at §14.5
(line 2126, an ordinary unlabeled paragraph, normative) already states
"the fill bit in a packed plane" explicitly, and hunks 12/15/16 land
inside §20.3 step 4's numbered "An appender MUST, in order: … 4. …"
list (line 3133), which carries no blockquote marker at all and is
squarely normative. So hunk-05's Rationale copy is exactly what §11.1
already declares itself to be at lines 1629–1632 ("§20.3 states
normatively, and governs, what a commit may do…") — a non-normative
gloss of a rule stated normatively elsewhere. Not a defect.

hunks 12, 15, 16 land in the unlabeled, ">"-free numbered step 4 —
normative, confirmed by reading lines 3133–3364 in full (no blockquote
markers anywhere in step 4's body; the two blockquotes that follow,
at lines 3366 and 3374, are a "> **Note.**" and a "> **Example.**"
that come *after* step 4 ends, not inside it).

hunk-24 lands in §23.1's main prose (lines 4244–4270), also
unlabeled/normative, immediately preceding the `[R-PRV-01]` citation
at line 4270 that the paragraph builds up to.

## Check 2 — citations

- `[R-SER-05]` (cited by hunk-12, hunk-16, hunk-24, and referenced by
  content in hunk-05 and hunk-15 without the bracket): opened at
  §14.5, lines 2126–2137. States exactly what all five sentences
  claim of it — "at every padding position, a writer MUST encode …
  the fill bit in a packed plane" — and assigns the check to a
  verifier ("a verifier MUST check it"), consistent with T4/T5's
  outcome column ("verifier", "certification"). PASS for all five
  citing/depending sites.
- `[R-SER-03]` (named alongside, in §14.3 line 2072 and echoed in the
  §20.3 general test at line 3189): opened at §14.3, lines 2059–2072.
  Governs pad bits (not padding positions) — correctly kept distinct
  from the padding-position content rule throughout; none of my five
  hunks conflate the two. PASS.
- `[R-GEO-04]` (§11.3, line 1701, cited in the passage hunk-05 sits
  in): "a reader MUST NOT return padding positions as samples" —
  consistent with hunk-24's framing that a reader never surfaces this
  content directly. PASS.
- Section cross-references: "§20.3 step 4" in hunk-24 — verified step
  4 is indeed the numbered item containing the shrink/growth carve-outs
  (line 3166 onward, "4. **Write payloads and indexes**"). PASS.
  "§14.5" in the Note at line 2154 and elsewhere — verified it is the
  section that states padding content (not pad bits) — PASS.

## Sweeps

All sweeps below normalize the hard wrap first (join `>`-prefixed
continuation lines and all newlines into single spaces, collapse
whitespace) before substring search, per the charter's warning, and
each is followed by a control search proving the normalization
actually works (a phrase from the same passage that *is* known to be
present).

1. `grep -c "already holds the fill"` after normalization → **4**
   hits, all four are hunk-05/12/15/16's landing sentences (verified
   by printing 60-char context around each). Control: searching
   normalized text for "the fill" alone (deliberately generic, known
   to hit many places) returns dozens of hits, proving the
   normalization pass is not itself silently returning zero for
   everything — the 4-count is a real, non-trivial result.
2. `grep -c "hold the fill"`, `"holds fill"`, `"hold fill"` (the
   grammatical near-misses of the same phrase, in case a variant
   wording of the same restatement existed elsewhere) → **0, 0, 0**.
   No missed restatement of this specific clause under any of these
   variant forms.
3. `grep -c "bit in a packed plane"` (singular, un-prefixed by "or")
   → **5** hits: hunks 05/12/15/16 (4) plus the pre-existing §14.5
   phrase "the fill bit in a packed plane" (1, confirmed by printing
   context — it is not one of my five hunks, it predates this round's
   repair and is the normative rule the repair is bringing the other
   sites into line with).
4. `grep -c "bits in a packed plane"` (plural) → **1** hit: hunk-24,
   confirmed by context. No other plural restatement missed.
5. `grep -c "already hold the channel"` → **1** hit: hunk-24 itself.
   No duplicate plural restatement elsewhere.
6. Register-row sweep: `grep -n "^| T" tarn.md | grep -i
   "fill\|padding\|pad bit"` → T2, T4, T5, T26 (lines 3854, 3856,
   3857, 3878). Read all four in full. T4's witness column already
   separately lists "packed planar bool plane fill bit" as distinct
   from "planar numeric plane fill bytes" — the register was already
   bit-grain-correct before this round, nothing to sweep there. T5 is
   specifically about pad bits (not padding positions), correctly
   distinct. T26 mentions "packed planar bool: identity s = 1" for an
   unrelated reason (filter stride), no fill-content claim to sweep.
7. `grep -n "^| R\|^| L"` filtered for shrink/padding/fill → L30, L35
   (lines 3822, 3827), both about fill-field *validity* (is the
   recorded fill byte itself 0x00/0x01), not about padding-position
   content — nothing to sweep.
8. §21.7 ("What no check detects", lines 3971–4026) and Appendix H
   (lines 4756–4831): both read in full. §21.7 line 3983 uses the
   generic enumeration "padding positions, pad bits, and boolean
   bytes" (no "stored byte…already holds fill" claim to be
   byte/bit-imprecise about). Appendix H line 4785 says "fill-encodes
   edge padding and pad bits" — same generic, non-byte-specific
   phrasing. Neither needed the sweep.
9. Additional stray site found by the "stored byte" sweep (79
   contexts scanned programmatically, filtered to the ones mentioning
   fill/padding): one non-hunk hit at lines 1944–1947 ("The padding
   positions of stored edge tiles (§11.3) are a different mechanism —
   their stored byte content is §14's subject"). Read in context
   (lines 1930–1952): this is a `> **Note.**` block that defers to
   §14 generically rather than restating the fill-equality claim
   itself — it makes no "already holds the fill" assertion of its own
   to be imprecise about, so it needed no edit and got none. Correctly
   left alone.

Net: the packed-plane clause appears in exactly the 5 places the
charter names, in exactly the phrasing the charter names, and no
sixth restatement was left behind unswept.

## Check 1 — tense and quantifier

All five instances use "already holds the fill" — present-tense,
referring to the state *before* the commit under discussion. This
matches the tense convention §20.3 step 4 states explicitly for
itself at lines 3197–3198: "The tense is the prior generation's (§3.1
defines *stored* against a generation)." The packed-plane insertion
does not touch tense or quantifier at all — it inserts a parallel noun
phrase ("bit in a packed plane") alongside the existing "stored byte,"
governed by the same "already holds" verb, same tense, same implicit
quantifier (a specific commit's specific padding position, not "every"
or "any"). Checked against `[R-SER-05]`'s own tense — §14.5's
statement is a standing writer obligation on every padding position
in every generation ("at every padding position, a writer MUST
encode…"), and the §20.3 carve-out's "already holds" is squarely an
instance of that same standing rule evaluated at the moment just
before the commit. Quantifiers match. PASS for all five.

## Check 4 — contradiction in the same passage

Read each hunk's full enclosing structure (§11.1's whole Rationale
block; all of §20.3 step 4, lines 3133–3364; all of §23.1, lines
4242–4270).

- No MUST elsewhere in §20.3 step 4 is loosened by the packed-plane
  addition — the addition only clarifies which storage grain the
  existing "already holds the fill" test applies at; it does not
  change who must do what.
- The growth carve-out (hunk-15) explicitly disclaims reaching a
  growth ("The bar's carve-out does not reach a growth: its padding
  limb covers a position whose … already holds the fill it keeps, not
  one that ceases to be padding") — checked this against the
  preceding sentence's growth permission ("an extent MAY grow, since a
  position that becomes real held … that channel's fill … and fill is
  a legal sample value") and found no collision: the growth permission
  is stated as its own exception to the §14 bar, not as an instance of
  the padding-content carve-out, and the carve-out's disclaimer is
  consistent with that, both before and after the packed-plane
  insertion.
- Checked the "exactly as it is there" callback at line 3330 (part of
  hunk-16's landing) against the earlier general statement it
  points back to (hunk-12's landing, line ~3207): both now carry the
  *identical* "or bit in a packed plane" clause, so the "exactly as
  it is there" claim remains true after the repair — had only one of
  the two picked up the insertion, this specific cross-reference
  would have gone false without any diff showing it (a live risk this
  audit specifically checked for and did not find realized).
- No carve-out three sentences later narrows what the packed-plane
  insertion widens: I read forward and backward from every landing and
  found no such collision.

## Check 5 — exhaustive claims

- hunk-24's "Those two cases are exhaustive because the bytes either
  travel out of the live state or stay in the structure that carried
  them" (unchanged by the repair, but re-checked against the
  packed-plane addition): the bit-level padding case is not a third
  case, it is a finer-grained instance of the second case ("stay in
  the structure that carried them") — the dichotomy is still binary
  and still exhaustive after the repair. Not falsified.
- The two-term disjunction itself ("stored byte, or bit in a packed
  plane") is implicitly exhaustive over the ways a padding position's
  content is stored: verified against §14.5's own three-way
  enumeration ("recorded fill bytes for a numeric channel, … fill
  byte for an interleaved bool channel, … fill bit in a packed
  plane") and against `[R-SER-09]`'s "every combination of layout and
  channel types is defined" (§14.4, line 2099) — there is no fourth
  layout/type combination the two-term disjunction fails to cover;
  "stored byte" is the generic term covering both of §14.5's
  byte-grain sub-cases (numeric multi-byte, interleaved-bool
  single-byte), consistent with how "byte"/"bytes" is used generically
  elsewhere in the document (e.g. "stored bytes" at line 3203) rather
  than as a literal "exactly one byte" claim. Not falsified.

## Check 6 — what else is left unconstrained

Named structure: a packed planar bool tile's byte array (⌈P/8⌉ bytes,
holding up to 8 independent per-ordinal value bits per byte, plus
possibly leftover pad bits in the final byte). Enumerated every
quantity/flag this structure carries and checked each is governed by
something:
- per-ordinal value bit (real or padding) — governed by §14.3's
  packing rule for its position, and by `[R-SER-05]` for a padding
  ordinal's required content. Covered.
- final-byte leftover pad bits (only when P mod 8 ≠ 0) — governed by
  `[R-SER-03]`/`[R-SER-05]` together, and separately witnessed by T5.
  Not touched by any of my five hunks and not in need of touching —
  a shrink of the layer's *extent* does not change P (P is a function
  of the *tile* extents only, §11.2), so pad-bit count and position
  are invariant under exactly the class of commit these carve-outs
  discuss. Covered, and correctly untouched.
- decoded tile byte length ⌈P/8⌉ — governed by `[R-SER-07]` (§14.4,
  line 2088), unrelated to and unaffected by the packed-plane clause.
  Covered elsewhere, not this repair's concern.
- disk ordinal of the tile itself (which byte-array this is) —
  governed by `[R-GEO-06]` and the surrounding "disk ordinal move"
  bar (§20.3 step 4, lines 3248–3283), a wholly separate limb of the
  same step, unaffected by and not needing the packed-plane clause.

No sibling quantity of this structure was left ungoverned by the
repair; the repair's scope (padding-position content grain) does not
overlap the other governed quantities, and I found no case of "one
quantity pinned, its sibling left open" of the shape the charter warns
about for this check.

## Check 7 — analogy comparisons

No hunk among my five states its rule by pointing at another rule as
warrant ("exactly as", "the same way", "as X is", "on the model",
etc.) *for the packed-plane clause itself*. The one nearby "exactly as
it is there" (line 3330, part of hunk-16's landing) is a
same-document callback between two instances of the *same* carve-out
(general statement vs. shrink-specific statement), not an analogy to
a differently-quantified rule — I checked it under Check 4 above
(cross-consistency) rather than here, since both "here" and "there"
range over the identical set (padding positions whose already-stored
content matches fill) after the repair, with no quantifier mismatch of
the "contains" vs. "addressed" shape the check warns about. Governing
verb on both sides: "already holds the fill" / "already holds the
fill" — identical, not merely analogous. No Check-7 finding.

## Check 8 — effect on surrounding sentences (insertions)

For each of the five insertions, read forward to the end of its
enclosing subsection and listed every back-reference:

- hunk-05: next sentence "One commit can do several of these at
  once." — "these" resolves to the list of prior clauses (tile
  dropped from addressed set; tile the superseded generation didn't
  store; new padding position with byte/bit already fill) both before
  and after the insertion — the insertion sits *inside* one list item,
  not between list items, so it cannot change which items "these"
  ranges over. Unaffected.
- hunk-12: "leaves them so" — "them" resolves to "those tiles' stored
  bytes" (established earlier in the same sentence, before the
  restructuring's dash-clause and before the packed-plane insertion).
  Checked whether the intervening restructured clause ("the value each
  denotes, at the coordinate it denotes it") introduces a competing
  plural antecedent — it does not (both nouns in it, "the value" and
  "the coordinate," are singular). "Them" still resolves correctly.
  Next sentence ("A channel's declared **sample type** is such a
  declaration…") — "such a declaration" resolves to the declarations
  discussed in the §14-bar list generally, unaffected by the
  packed-plane insertion three clauses earlier.
- hunk-15: "the fill it keeps" — "it" resolves to "a position" (the
  subject of the same relative clause, immediately preceding);
  unaffected by inserting "or bit in a packed plane" between "stored
  byte" and "already holds," since that insertion sits before "it"
  appears and does not introduce a new candidate antecedent noun
  ("plane" is not picked up by "it," which is singular and reads
  naturally as "position"). Next sentence ("It holds provided the
  grown geometry stays…") — "It" resolves to "this is an exception the
  permission states," i.e. the growth permission, unaffected.
- hunk-16: "so a shrink producing only those is permitted here exactly
  as it is there" — "those" resolves to "[padding positions] whose
  stored byte, or bit in a packed plane, already holds the fill" —
  the insertion *is* part of what "those" now ranges over, which is
  the intended widening (both byte- and bit-grain padding positions),
  not an accidental one. "Here"/"there" checked under Check 4 above.
  Next sentence ("The bar beside the §14 bar does not reach a shrink
  either…") — "The bar beside the §14 bar" resolves to the ordinal-move
  bar introduced earlier in step 4 (line 3248), unaffected by this
  insertion three sentences earlier.
- hunk-24: "Those two cases are exhaustive…" and "the bytes either
  travel out of the live state or stay in the structure that carried
  them" — both resolve to the A/B dichotomy stated at the top of the
  paragraph (lines 4255, 4259), established well before the insertion
  and not renumbered or reworded by it. Unaffected.

Also checked the reverse direction (does the inserted text itself use
a back-reference reaching further than the reader will look): no —
"or bit in a packed plane" is a bare noun phrase, introduces no
pronoun, and neither the singular nor plural variant relies on
anything preceding it beyond "stored byte"/"those bytes" in the same
clause.

No anaphor was found to have silently re-resolved as a result of any
of the five insertions.

## NESTED_DASH

Checked every sentence containing the packed-plane clause for an
em-dash pair nested inside another em-dash-delimited clause. None of
the five insertions itself introduces an em-dash. hunk-12's landing
(part of the larger, out-of-charter restructuring) does contain one
em-dash pair — "— the value each denotes, at the coordinate it denotes
it —" — but it is not nested inside a second, outer em-dash pair (the
sentence's outer boundary is a colon on one side and "and…leaves them
so" with no dash on the other), so it does not meet this check's
trigger, and in any case that clause is outside my charter (another
lane's edit). No NESTED_DASH finding among my five hunks.

## Rejected candidates

1. *Suspected ambiguity in "whose stored byte, or bit in a packed
   plane, already holds the fill" as offering an updater a free choice
   between checking a byte or a bit for the same position.* Closed:
   §14.3/§14.4 (`[R-SER-09]`) make layout+type per channel fixed and
   mutually exclusive — packing is exclusive to planar bool
   (`[R-SER-03]`, line 2065), so which of the two disjuncts applies to
   any given padding position is determined by the channel's
   declaration, not chosen by the reader/updater. Not a defect.
2. *Suspected conflation between "bit in a packed plane" (my five
   hunks' phrase) and the defined term "pad bit" (§14.3, a different,
   P-independent concept — the final byte's leftover high bits).*
   Closed by re-reading the `> **Note.**` at lines 2074–2079, which
   states the distinction explicitly ("Pad bits are not padding
   positions"), and by checking that none of my five hunks use the
   term "pad bit" for this clause — they consistently say "bit in a
   packed plane," which is deliberately not the defined term. Not a
   defect.
3. *Suspected byte-level fork surviving the repair* (i.e., that the
   repair itself, not just the prior wording, might still leave the
   byte/bit distinction ambiguous). Closed by the "Derive the case"
   construction above: under the post-repair wording the constructed
   shrink (byte 0 = `0x0B`, bits 0–3 real, bits 4–7 newly-padding and
   already fill) is unambiguously permitted, matching `[R-SER-05]` and
   T4/T5. The fork I was able to construct exists only in the
   *pre-repair* wording (a real defect that predates this round, now
   fixed by this repair) — see "Derived numbers" below for the
   byte-level analysis of that pre-repair ambiguity.
4. *Suspected inconsistency between hunk-24's "the bytes either travel
   out of the live state or stay in the structure that carried them"
   (unedited, still says "bytes" only, not "bytes or bits") and the
   new bit-grain precision two sentences earlier.* Closed: this later
   sentence is a structural claim about *where* removed content goes
   (out of the live state vs. staying in its structure), using "bytes"
   as the generic term for "the underlying storage," not a
   byte-vs-bit content claim — it does not need the "or bits" gloss
   any more than "readable by anyone with the bytes and a hex editor"
   (line 4257, also unedited, also generic) does. Not a defect.
5. *Suspected NESTED_DASH inside hunk-12's landing.* Closed above
   (one em-dash pair, not nested in a second, and out of charter
   scope regardless).

## Byte-level assessment

For hunks 12, 15, 16 (normative, inside §20.3 step 4's MUST-governed
appender procedure): **not byte-level as a defect in the repaired
text**, because the repaired text is what removes a genuine byte-level
ambiguity rather than creating one. I verified this is a real,
constructible fork (see "Derive the case" and "Derived numbers"): the
*pre-repair* wording, read strictly at byte grain, would classify the
constructed shrink (byte `0x0B`, mixed real/padding-fill bits) as
barred by the §14 bar, while the same wording read loosely (or the
post-repair wording, read either way) classifies it as permitted —
two competent implementations could reach different accept/reject
verdicts on the identical candidate file under the old text. The
repair resolves that fork in the direction that matches the
already-normative `[R-SER-05]` and the already-existing T4/T5 register
rows, so the *current* (post-repair) text no longer forks — this is a
correction, not a new defect, and I found no residual fork in the
repaired wording itself.

For hunk-05 (Rationale, non-normative) and hunk-24 (§23.1, explanatory
prose feeding into but not itself the `[R-PRV-01]` MUST): not
byte-level, by the checklist's own governing-clause rule — neither
sentence gates what bytes a conforming writer may emit or a conforming
reader/verifier must accept/reject; hunk-05 is disclaimed non-normative
by §11.1's own text, and hunk-24's clause is explanatory scaffolding
for why misrepresenting a shrink as erasure would be misleading, with
the actual MUST NOT stated separately at line 4270's `[R-PRV-01]`,
unaffected by this insertion's wording either way.

## Derived numbers

- Count of "already holds the fill" occurrences (normalized text):
  computed = 4; matches the count of singular-form hunks (05, 12, 15,
  16) exactly, confirming no fifth singular site and no dropped one.
- Count of "bit in a packed plane" (singular) occurrences: computed
  = 5; expected = 4 (my hunks) + 1 (pre-existing §14.5 occurrence,
  "the fill bit in a packed plane") = 5. Matches.
- Count of "bits in a packed plane" (plural) occurrences: computed
  = 1; expected = 1 (hunk-24 only, no pre-existing plural form
  anywhere else). Matches.
- P for the constructed example: T₀ = 9 (rank 1) ⇒ P = ∏Tᵢ = 9,
  ⌈P/8⌉ = 2 bytes, pad-bit count = 8 − (P mod 8) = 8 − 1 = 7 (bits
  1–7 of byte 1), consistent with §14.3's stated formula. Byte 0's
  bit layout for values (1,0,1,1,0,0,0,0) LSB-first at bits 0–7:
  bit0=1,bit1=0,bit2=1,bit3=1,bit4=0,bit5=0,bit6=0,bit7=0 →
  binary `00001011` → hex `0x0B`, confirmed by hand (bit0 is the
  least-significant bit per "value k occupies bit k mod 8", so the
  byte value is Σ bit_i·2^i = 1·1 + 0·2 + 1·4 + 1·8 = 13 = 0x0D).
  **Correction on manual re-check:** 1+4+8 = 13 = `0x0D`, not `0x0B` as
  first written above in the derivation section. This does not change
  the argument (any byte value ≠ the all-zero fill pattern `0x00`
  makes the same point), but I flag the arithmetic slip here rather
  than silently fixing the earlier prose, per the disclosure
  requirement — the derivation's *conclusion* (the byte is not the
  fill pattern even though the relevant bits are) is unaffected by
  which of `0x0B`/`0x0D` is the correct value; I made an arithmetic
  error in the walking-prose version above and am recording the
  corrected computation here.

## Confidence / empty-findings note

I found no confirmed defect in the packed-plane clause across its five
landings, or in its interaction with the surrounding unedited text. To
back that verdict: I (a) constructed a concrete minimal counter-example
layer and traced it through all five sentences by hand rather than
just reading the words on the page; (b) ran and controlled eight
distinct sweeps for a sixth, unswept restatement site, including the
error register, §21.7, and Appendix H, all read in full rather than
grepped-and-trusted; (c) checked the one "exactly as it is there"
cross-reference between two of the five landings word-for-word rather
than assuming consistency; (d) checked every back-reference in the
subsections the five insertions land in, in both directions; (e)
verified `[R-SER-05]`, `[R-SER-03]`, `[R-GEO-04]`, and the "§20.3 step
4" cross-reference each by opening and reading the cited text, not by
trusting the citation's plausibility. What I did not, and could not,
check under this charter's access rule: whether the *other* edits
riding along in hunks 12 and 15 (the restructuring outside my charter)
are themselves defective — another lane holds that; I only checked
that the packed-plane clause's insertion into that restructured text
does not itself break under the restructuring, which it does not.
