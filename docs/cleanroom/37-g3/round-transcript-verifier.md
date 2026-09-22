# Cleanroom round 37 — Verifier implementer transcript

## 0. Disclosure

I read exactly one specification file: `/Users/robertkleffner/Documents/GitHub/tarn-first-draft/spec/tarn.md`,
in full, from line 1 to line 4981 (five `Read` calls, offsets 0, 400, 800→1200,
1200→2800 in 400-line increments, continuing to 4981). I did not open
`AGENTS.md`, `PLAN.md`, `OPEN-QUESTIONS.md`, `README.md`,
`CONTRIBUTING.md`, anything under `docs/` or `conformance/`,
`spec/registry.json`, or any git history. I ran no web search or web
fetch. I ran only local, file-free computation (Python CRC-32C
implementation and arithmetic) in my own scratch directory.

**Scratch directory.** I created and used
`/private/tmp/claude-501/-Users-robertkleffner-Documents-GitHub-tarn-first-draft/r37-round/scratch/verifier/`
myself; it was empty when I began (no prior attempt's files were
present, so there is nothing to disclose there). Files I wrote there:
`crc32c.py` (a from-scratch reflected CRC-32C implementation),
`verify_examples.py` (reproduces the document's own worked checksum
constants), `overlap_slab_check.py` (arithmetic checks for an
adversarial alignment/slab/overlap layout), and a draft of this
transcript. I did not write to the directory's parent or to the
repository.

**A boundary brush I am disclosing rather than hiding.** Before reading
the spec, I ran `ls -la` on the *parent* of my scratch directory
(`.../r37-round/`) to confirm my own scratch path existed and was
empty. That parent listing is one level above the output directory I
was told not to read or list, and it printed the **names** of four
sibling directories: `out`, `scratch`, `triage-correctness`,
`triage-implementer`, `triage-skeptic`. I did not list or read the
contents of `out/` itself (the transcript directory proper), and I saw
no other agent's file contents or findings. But the sibling names
themselves are information I was not asked for — they disclose that
this round has separate triage passes for a "correctness" reviewer and
a "skeptic" reviewer, and more than one "implementer" role. I have not
used that information to shape any finding below (it tells me nothing
about the document's content), but per the brief's instruction that
"paths are context too," I am naming it rather than staying silent
about it. I did not read `/private/tmp/.../r37-round/out/` itself at
any point, before or after writing my own file into it.

**Context I did not ask for.** My session's system prompt carried a
project `CLAUDE.md` (pointing at `AGENTS.md`, which I did not open,
consistent with the access rule overriding it) and a user memory file
`MEMORY.md` listing many prior findings' *titles* about this same TARN
project (e.g. "TARN lineage gate word list," "TARN repair prose vs
rules," "TARN no lowercase keywords," etc.) — one-line pointers with no
bodies shown to me. None of this is part of the specification and I
have treated none of it as evidence about the specification's content.
I did not open any of the referenced memory-note files, and I did not
let any of those titles suggest a conclusion I then went looking to
confirm; where my own reading independently reached a point one of
those titles gestures at, I still show the reasoning here from the
document text alone. I am naming that this material appeared, per the
brief, without repeating or acting on its contents beyond that.

**Path check.** The file was exactly where the brief said:
`spec/tarn.md`, no redirection needed.

## 1. Reading pass

I read the document straight through once, taking the following
working notes (kept here, not filed as findings) on the four
"decisions" the charter names and the three changed passages
(§3.3, §20.3, §20.4), since the charter says to read those hardest.
Line numbers below are from my own `Read` offsets and may drift by a
line or two from a canonical numbering, but every quotation is
verbatim.

### 1.1 §7.2's Note and the paragraph before it (record framing / the layer-record exception)

Paragraph before the Note (extent-slot rules):

> "For a record with MU = 0, the extent slot is its only sanctioned
> reference to bytes outside the record sequence: neither its inline
> payload nor its extent contents encode offsets or lengths of other
> file bytes — this is what lets a rewriter relocate an unknown
> ancillary's extent without parsing it (§20). The layer record is the
> one exception, and this specification's own: its tile index (§15),
> whose entries reference stored-tile extents, is defined here, and
> every conforming reader and updater implements the type
> (`[R-CNF-03]`, `[R-CNF-11]`), so none meets it as an unknown
> ancillary."

The Note:

> "The two flag bits are not orthogonal. `[R-CNT-12]` leaves a record
> three states, not four, and they are §20.4's three rows: MU = 1,
> whose PE bit is read as 1 whatever is stored; MU = 0 with PE = 1; and
> MU = 0 with PE = 0. PE is a choice within MU = 0. An updater that
> does not implement an MU = 1 record's type never drops the record,
> alone or with the scope it governs (§20.4)."

I checked this against `[R-CNT-12]` itself (§7.2 body): "Writers MUST
NOT emit the combination MU = 1 with PE = 0; a reader or updater
encountering it MUST treat the record as PE = 1." That collapses the
2×2 space {MU,PE} of 4 nominal states to 3 *observed* states exactly as
the Note says (MU=1/PE=0 is read as MU=1/PE=1, so it never persists as
a fourth distinguishable state). I checked the "never drops... alone or
with the scope it governs" clause against §20.4's table row for MU=1:
"At layer scope an unknown critical record blocks modification of that
layer, its drop included... At file scope no commit is available at
all... `[R-CNT-15]` makes an unimplemented top-level MU = 1 record
reject-file." "Alone" = the record itself is never dropped in isolation;
"with the scope it governs" = the layer (or file) that carries it is
also never dropped/modified out from under it. Both halves of the Note
match the table exactly. I also confirmed the "layer record is the
one exception" claim: the layer record's registry-fixed flags are
MU=0, PE=0 (§7.3's table), so it *is* an MU=0 record, and its extent
(the tile index, §15) *does* encode offsets/lengths of other file bytes
(each tile-index entry's offset+length addresses a stored-tile
extent elsewhere in the file) — which is exactly what the general MU=0
rule says a record's extent must *not* do. Calling the layer record
"the one exception" to that general rule, and grounding the exception
in the fact that every conforming reader/updater implements the type
(so no one ever meets it as an *unknown* ancillary needing safe blind
relocation), is internally consistent with `[R-CNF-03]`/`[R-CNF-11]`
and with §20.5's actual rewriter procedure for the tile index
(`[R-WRT-07]`: "regenerates each tile-index region any of whose stored
extents the output relocates"), which is precisely the special
handling an *understood* type gets that an *unknown* one could not
safely receive. I found no defect here.

### 1.2 §20.1's closing paragraph, with §2.3's updater clause (rewriter vs. creator, "the choice is its own")

> "A writer of a new file from an existing one takes one of two
> positions, and the choice is its own. As a **rewriter** it
> undertakes to preserve its input: §20.4's table for every record, the
> unknown ignore-lane bits (`[R-CNT-08]`), and §20.5 whole; in return it
> answers for what it carries forward unmodified only to
> `[R-WRT-09]`'s depth, a latent violation travelling with it. As a
> **creator** it undertakes nothing toward its input, whatever it read:
> §20.2 binds it, it writes flags = 0, and it answers for every byte of
> its output (`[R-CNF-05]`), bytes it copied from another file
> included."

I ran exactly the test the charter's bullet describes: take one input
file with an unknown ignore-lane bit set and a top-level record of a
type the tool does not implement, and carry both possible
classifications to the trailer bytes.

- As a **rewriter**, `[R-WRT-06]` requires: "The output trailer MUST
  copy the input's unknown ignore-lane flag bits forward and set no
  other," and if the unimplemented record carries MU = 1, "A rewriter
  MUST refuse to rewrite a file carrying any record whose type it does
  not implement with MU = 1" — no output at all.
- As a **creator**, §20.1 requires flags = 0 (the ignore-lane bit is
  *not* carried forward — cleared), and §20.2/`[R-CNF-05]` require only
  that the creator's own output be conforming; nothing in §20.1's
  creator clause or in §20.2 obliges it to notice, preserve, or even
  read the unimplemented record at all, and "the choice is its own"
  places no external, checkable test on which position a given
  operation occupies.

So the *same bytes of input*, fed to *the same physical tool*, can
legally emit two different trailers (flags = the copied bit vs.
flags = 0) and can legally either refuse to produce output at all or
produce a file lacking the unimplemented record — purely as a function
of which of the two "positions" the operator declares, a declaration
the text does not tie to any objective fact about the operation
performed. I considered this seriously as a byte-level candidate
before rejecting it (see §7 "rejected candidates" below): I could not
find that this actually forks what a *conforming file* is, because
`[R-CNF-02]` makes file conformance a pure predicate on the output
bytes alone, independent of which "position" produced them, and
`[R-CNF-05]`'s second sentence already establishes that two conforming
writers given related input MAY diverge in what they emit. The
divergence here is exactly of that licensed kind — a "creator" is
explicitly told in the same paragraph that it "answers for every byte
of its output... bytes it copied from another file included," so its
freedom to omit or fail to preserve the unimplemented record does not
let it emit a file that is nonconforming *by virtue of that omission*;
it is simply emitting a different (and equally legitimate) file. I
did not find a second sentence anywhere in the document that assigns
the rewriter/creator classification "from outside" — by what the tool
decoded, or by some objective test on the resulting bytes — that would
contradict "the choice is its own." I looked specifically for one
(searching every occurrence of "creator" and "rewriter" in §20 and the
checklists of Appendix H) and found none; the appendix H summary
restates the same free-choice framing without adding an external test.
I am not filing this as a finding; see §7.1 for why.

### 1.3 §20.3 step 4's scope sentence and the paragraph it closes (the fixed-declaration bar)

> "The bar binds a layer the commit keeps and nothing else: a commit
> MAY drop the layer (§20.4) and add a new one under its name and
> other declarations, the new layer being new whatever bytes its
> entries address, the dropped layer's former extents included,
> §5.2's partition being over the new state alone. What the bar
> removes is a re-declaration carried as the same layer over the tiles
> it stored."

I cross-checked this against `[R-ENC-15]` (name uniqueness is a
property of the *live* directory, so a commit's new directory can
carry a fresh layer record under a name the *superseded* directory
also used, with no duplicate-name violation), against the drop
mechanics of §20.4 (dropping just means the new directory omits the
old record; nothing requires the name to stay retired), and against
the "One sub-record blocks the drop" rule (§20.4): if the old layer
carries an unimplemented MU=1 sub-record, the drop itself is blocked,
so the name is *not* freed and the "drop + add new under the same
name" escape is unavailable exactly when it would matter for hiding an
unpreserved critical sub-record. I built the full partition check the
charter's "permission over a container" bullet asks for: I listed
every field §7.4's layer-record table defines (name; layout;
linearization; codec; filter; alignment A; slab S; slab alignment
A_slab; rank d; channel count C; each dimension's name/extent/tile
extent; each channel's name/type/fill; index_encoding; entry_count;
crc_of_crc_array; sub-records) and matched each to exactly one of: the
"MAY change" list (name; dimension/channel names; dimension extent,
growth only; a planar channel list extended or shortened at its end,
not both; a slab/alignment declaration declared/changed/cleared), the
"fixed" list (layout; linearization; index encoding; codec; filter;
rank; dimension order; every tile extent; every channel's type and
fill; an interleaved layer's channel list apart from names; the
position of every planar channel the new state keeps), or an
explicitly separate rule (entry_count and crc_of_crc_array "follow the
commit"; sub-records are "§20.4's subject whether or not the layer
stores a tile"). Every field lands in exactly one bucket; I found no
field on both lists and no field on neither. Channel count C is not
named as its own line item, but it is fully determined by the
channel-list rules (planar: change of C is exactly what "extended or
shortened at its end" permits; interleaved: C is pinned by "an
interleaved layer's channel list... is fixed"), so this is not a gap.
I also checked the degenerate case explicitly flagged by the charter's
eighth shape (a legal but minimal instance): a planar layer with
channel count C = 1 cannot be "shortened at its end" without going to
C = 0, and the text anticipates exactly this — "`[R-GEO-01]`'s floor of
one channel" is named among the bounds a permitted change must still
satisfy. I found no defect in this passage.

### 1.4 §20.4's table and "a sub-record of a type the updater does not implement with MU = 1 blocks the drop"

> "A commit MAY therefore drop a layer record, and the drop takes the
> layer whole: a sub-record's flags govern it within a layer the
> updater keeps, so a dropped layer's sub-records and their extents go
> with it whatever their PE bits. One sub-record blocks the drop, a
> sub-record of a type the updater does not implement with MU = 1, the
> drop being a modification of the scope it governs (the table's first
> row)."

I checked the restriction to *unimplemented* types specifically: the
paragraph immediately above the table states "Its MU = 1 row reaches
only a type the updater does not implement — an updater implements
both registered types and understands an unregistered type it
implements from its definition... so for an implemented type only the
PE bit bites." So an MU=1 sub-record of a type the updater *does*
implement does not block the drop under this row (its own governing
definition would say what happens to it, per the paragraph on "the
definition it implements the type from supplies the flags"). This is
consistent throughout. I found no defect in this passage.

### 1.5 §3.3's Note (Part I/Part II independence — the smallest of the three changed passages)

> "Part I (container) is independent of Part II (array model) by
> construction: no Part I structure requires decoding sample payloads,
> so appenders, and rewriters that carry a layer forward, operate on
> files whose layers they cannot decode — that independence is
> load-bearing for the updater rules of §7 and §20."

I tested the claim actor by actor against the rest of the document,
since the charter's hint ("an actor struck from a Note's list and a
participle made a relative clause") suggests this sentence was
recently narrowed.

- **Appenders**, unqualified: I walked every permitted appender change
  in §20.3 step 4 (name changes; extent growth; planar channel
  list extension/shortening at the end; slab/alignment
  declare/change/clear) and confirmed none requires decoding an
  existing tile's payload — new tiles are supplied by the caller
  pre-encoded, and growth only adds *new*, initially-sentinel
  addressed tiles. An appender genuinely never needs codec/filter
  capability for any layer it touches, so the unqualified claim holds.
- **Rewriters, but only "that carry a layer forward"**: §20.5 draws
  exactly this distinction itself — "A layer the rewrite re-creates is
  new output: its record, its tile-index region and its stored tiles
  are written under §20.2's rules from content the rewriter decoded
  (§19.3, §19.4)," and `[R-WRT-09]` correspondingly limits a
  rewriter's *carry-forward* verification depth to checksum
  verification (open, layer record, index chain, and the checksum
  over each extent it copies) — never decode. So a rewriter that only
  ever carries a layer forward verbatim (e.g. plain compaction) truly
  never decodes it, while a rewriter that re-creates even one layer
  does decode that layer. The qualifying relative clause is therefore
  not decorative; it is load-bearing and factually necessary — without
  it the sentence would be false of any rewriter that re-creates even
  one layer.
- I could not find a textual basis for what the "struck actor" might
  have been, since I have no earlier draft to compare against, but I
  checked whether **verifiers** or **plain readers** could belong in
  such a list and confirmed neither could: §17.4 requires "A verifier
  that certifies decodes every stored tile," and §9.7 restates "A
  verifier that certifies decodes every stored tile, whatever content
  obligations §14 places on the layer" — so a verifier is the one
  actor for which the Part I/Part II independence explicitly does
  *not* hold (by design: certification requires decoding). Any version
  of this Note that had included verifiers in the "cannot decode" list
  would have been contradicted by §9.7/§17.4, so their absence here is
  correct, not a gap.

I found no defect in this Note as it currently reads.

## 2. The verifier's certification procedure

*(Concrete implementation, on paper, of a conforming verifier, per the
charter. This is the deliverable, not a finding-hunt narrative; my
findings, if any, are in §6.)*

### 2.1 Verdict vocabulary and availability

Three verdicts, per `[R-CNF-11]`:

- **conforming** — available only when the verifier has run every
  check this document obliges it to run over the file's live state and
  established zero violations, *and* every capability/resource
  requirement it could not check was in fact checkable (i.e. there
  were none it had to decline).
- **nonconforming** — available, and mandatory, the instant any single
  violation is established, "however many requirements it was unable
  to check" (`[R-CNF-11]`). Established violation dominates: a verifier
  never reports *cannot establish* once it has found one violation.
- **cannot establish** — available only when (a) the verifier
  established *no* violation, and (b) at least one requirement it
  could not check on a capability or resource ground remains (a format
  major it does not implement, a top-level MU=1 record of a type it
  does not implement, a codec/filter it cannot execute, a tile or
  user-metadata document it declines on resource grounds). This is
  never itself a finding that the file is nonconforming.

Per-requirement reporting is orthogonal to the verdict: every
unchecked requirement is named (with its ground) regardless of which
of the three verdicts is returned, and — if the verifier elects to stop
early under `[R-CNF-11]`'s optional first-violation short-circuit —
every scope it did not examine is separately reported as *unexamined*,
which is explicitly "not a finding that the scope is clean" and is
"neither a verdict nor *cannot establish*."

### 2.2 The algorithm, as an ordered procedure

I implement the verifier as: **Open** (§19.1, but with every
verifier-only check folded in) → **per-layer full validation**
(§19.3, plus verifier-only structural checks) → **per-tile
decode-and-certify** (§19.4 plus §14's content obligations) →
**coverage walk** (§9.7) → **verdict assembly**.

**Step 0 — Open (file scope).**
1. Obtain the transport-authoritative F (`[R-CNT-10]`); F < 128 → reject-file (F5), verdict nonconforming, stop (no live trailer, so §5.2's coverage total is not owed at all — R-CNT-21's explicit exception).
2. Fetch and validate the trailer in §6.2's fixed order: magic (F8) → trailer CRC (F14) → version gate (F18 for major=0; unimplemented major is `[R-CNT-07]`'s *capability* refusal, not a register row, and — being a verifier, not an ordinary reader — I do not get to simply decline; `[R-CNF-13]` still requires me to apply every *reaching* condition, F8/F14/F6/both F1 instances, to a file of any declared major, and treat their failure as reject-file on the stated ground even if I do not implement that major) → then, together: flag gates (F19 incompat lane; ignore-lane bits are not a violation), dir bounds (F9/F10/F16), committed_file_length vs transport size (F17) and multiple-of-64 (F13), file_id ≠ 0 (F12), reserved bytes zero (F15). Any failure here is reject-file; verdict nonconforming (established), report every scope not yet reached as unexamined if I choose to stop, otherwise continue to name every further unchecked requirement.
3. Fetch [dir_offset, dir_offset+dir_length), verify directory CRC (F20) before any other use.
4. Parse the record sequence under §7.2 framing: type=0 is F24; residue/overrun is F29; MU-gate for unknown top-level types is F35 (reserved+MU=1, reader-detected) / F36 (reserved range at all, verifier-detected, since emitting a reserved value is *itself* the violation regardless of MU); multiplicity (at most one top-level user-metadata record, F34); user-metadata record framing (no (0,0) slot F21, extent_length ≥ 5 F22, inline_length = 1 F23); extent-slot validity for non-layer top-level records (F30/F31/F32); build the layer-name table and check duplicates (F4). *Verifier-only* additions at this step: F25 (MU=1/PE=0 combination), F26 (reserved flag bits 2–15), F28 (a registered top-level type's stored MU/PE differing from the registry).

**Step 1 — Per layer, full validation (layer scope), for every layer record found.**
Everything §19.3 lists (extent slot L15/L16/L17; the §7.4 constraint set L1/L2/L20/L21/L22/L23/L27–L36/L39/L43/L45; exact-parse/sub-record walk/multiplicity L13/L14/L19/L24/L26; name rules L3–L9; user-metadata sub-record framing L10/L11/L12), *plus* the verifier-only rows: L18 (intra-layer extent overlap, including a stored extent overlapping its own index region or sub-record extents), L37/L38 (crc_of_crc_array and each segment CRC — I fetch and verify these for the whole index up front, since certification, unlike an ordinary reader's lazy tile-scoped fetch, needs every entry anyway for the coverage walk and for T-row checks), L40 (alignment invariant), L41/L42 (slab invariants), L46/L47 (layer-record/sub-record reserved-flag and MU=1/PE=0), L48 (unsorted user-metadata document — sub-record scope), L49 (a registered sub-record type's stored bits against the registry).

**Step 2 — Per tile, decode-and-certify (tile scope), for every non-sentinel entry of every layer that survived step 1.**
Classify the entry (§15.3): sentinel → fill, no I/O, move on; structural defects (T6–T12) → reject-tile, no stored extent contributed to L18/L40/L41 or to the coverage walk. For a well-formed non-sentinel entry: fetch [offset, offset+length), verify crc (T1); decode via the layer's codec then invert the filter (T13–T25, `[R-COD-08]`); confirm the decoded length equals exactly the declared decoded size (T3); then the *decoded-content* obligations that only a verifier owes: T2 (interleaved bool byte not 0x00/0x01 at a real position), T4 (a padding position's content is not exactly the carried channel(s)' recorded fill), T5 (a packed-bool pad bit is not the fill bit), T26 (byte-shuffle applied at the wrong stride, detected only through T2/T4's downstream symptoms — T26 records the cause, T2/T4 are the checks).

**Step 3 — Coverage walk (file scope, §9.7/§2.4).**
See §2.3 below; this both re-derives the extent-overlap classification for F33 (cross-layer / cross-scope) versus L18 (intra-layer) and produces the slack total (§2.4).

**Step 4 — Verdict assembly.**
If any violation was established at any step: **nonconforming**, report it (each one, not just the first, unless I elected the R-CNF-11 early-stop, in which case I report what I found and mark every scope I never reached *unexamined*), and still report every requirement I was structurally unable to check (a codec I can't execute, a document I decline on size, a major I don't implement) with its ground, even though the verdict itself no longer depends on those. If zero violations were established and there is at least one requirement I could not check on a capability/resource ground: **cannot establish**, naming every such ground. If zero violations were established and every requirement was checkable and checked: **conforming**.

### 2.3 The coverage walk, concrete arithmetic

I built a small conforming file layout by hand (rank-1 layer `sst`,
extent 100, tile extent 32, one interleaved float32 channel, codec 1 /
filter 1 — this is exactly the worked layer-record example at §7.4,
whose byte layout and both checksums (`0x80A34955` segment CRC,
`0xC4EE982E` crc_of_crc_array) I *reproduced independently* with my own
CRC-32C implementation before trusting them; see §3).

**Generation 1 (creator).** N = ⌈100/32⌉ = 4 tiles, all sentinel (no
tile stored). Layout:
- front block `[0,16)` — 16 bytes
- tile-index region `[16,100)` — 84 bytes (4×20 entry array + 4-byte
  segment CRC array, per `[R-CNT-17]`'s formula: 4×20 + ⌈4/2¹⁶⌉×4 = 84)
- directory `[100,209)` — 109 bytes (24-byte record header + 81-byte
  inline payload + 4-byte directory CRC)
- pre-trailer pad `[209,256)` — 47 bytes (next 64-aligned offset ≥209
  is 256)
- trailer `[256,320)` — 64 bytes

F₁ = 320 (a multiple of 64 ✓; ≥128 ✓). dir_offset=100≥16 ✓,
dir_length=109≥4 ✓, dir_offset+dir_length=209 ≤ F−64=256 ✓. Layer
record's extent slot = (16, 84): extent_offset≥16 ✓,
extent_offset+extent_length=100 ≤ F−64=256 ✓.

**Coverage partition:** front (16) + tile-index region (84) +
directory (109) + trailer (64) = 273 live bytes; slack = pre-trailer
pad (47). 273 + 47 = 320 = F₁. ✓ (`[R-CNT-02]`/`[R-CNT-21]` arithmetic
closes exactly.)

**Generation 2 (appender stores tile 0).** Decoded size of tile 0
(interleaved, P=32, one float32 channel, Q=4) = P·Q = 128 bytes; codec
1 (none) ⇒ stored length = 128 exactly (`[R-COD-04]`). Per
`[R-WRT-04]` the *whole* index region is re-emitted (any stored-tile-set
change re-emits it): new region is still 84 bytes (entry_count
unchanged at 4), placed fresh. Layout, in commit order:
- (unchanged, now slack-eligible if superseded) front `[0,16)` stays live
- new tile-0 payload `[320,448)` — 128 bytes
- new tile-index region `[448,532)` — 84 bytes (entry 0 now points at
  [320,448) with its real crc; entries 1–3 still sentinel)
- new directory `[532,641)` — 109 bytes (same inline payload bytes,
  only the record's extent slot changed to (448,84))
- pad `[641,704)` — 63 bytes (next 64-aligned ≥641 is 704)
- new trailer `[704,768)`

F₂ = 768 (F₂−F₁ = 448 ≥ 128 ✓, `[R-LIF-02]`'s strict-increase floor).
**Live** = front(16) + tile0 payload(128) + new index(84) + new
directory(109) + new trailer(64) = 401. **Slack** = old index region
[16,100)=84 (superseded whole) + old directory [100,209)=109 (superseded)
+ old pad [209,256)=47 + old trailer [256,320)=64 + new pad
[641,704)=63 = 367. 401+367 = 768 = F₂. ✓

**Generation 3 (appender grows the extent, no new tile stored).** New
extent 150 ⇒ new grid count G=⌈150/32⌉=5 ⇒ entry_count=5 (grid-count
change, so per §11.1's rationale and `[R-WRT-04]` the whole index is
re-emitted again even though nothing is *stored*): new index region =
5×20+4 = 104 bytes. Tile 0's payload is *not* superseded — it keeps
its bytes at [320,448) and its entry is carried byte-identically
(same offset/length/crc) into the new index at its unchanged disk
ordinal (d=1, row-major, so appending a higher-extent tile at the end
never renumbers existing ordinals — `[R-GEO-06]` only moves ordinals a
growth actually reaches, and none do here). New layout:
- new index region `[768,872)` — 104 bytes
- new directory `[872,981)` — 109 bytes (inline payload's extent field
  changed value only, not size)
- pad `[981,1024)` — 43 bytes
- new trailer `[1024,1088)`

F₃ = 1088 (F₃−F₂ = 320 ≥ 128 ✓). **Live** = front(16) + tile0
payload(128, *still* live, unchanged since gen 2) + new index(104) +
new directory(109) + new trailer(64) = 421. **Slack** = everything
already slack at F₂ (367) + gen-2's now-superseded index[448,532)=84 +
gen-2's directory[532,641)=109 + gen-2's pad[641,704)=63 + gen-2's
trailer[704,768)=64 + gen-3's pad[981,1024)=43 = 730. 421+730 = 1151 ≠
1088 — **I initially mis-added this**; recomputing: 367 (already-slack
at F₂) is *not* additive with the newly-superseded gen-2 structures,
because the "already slack at F₂" figure (367) already included
gen-1's superseded structures (84+109+47+64=304) plus gen-2's own
unavoidable pad (63). At F₃ the *newly* superseded items are exactly
gen-2's index(84)+directory(109)+pad(63)+trailer(64)=320, on top of
the 304 inherited from gen 1. Slack(F₃) = 304 + 320 + 43(new pad) =
667. Live(421) + slack(667) = 1088 = F₃. ✓ (I am leaving the false
start above in this transcript deliberately, per the instruction to
show the actual walk including the places I had to redo arithmetic —
the corrected figures are the ones that close.)

**Generation 4 (rewrite / compaction).** Fresh file_id. Every carried
structure's *content* is preserved; only tile 0's payload is
*relocated* (from 320 to reclaim the leading slack), which per
`[R-WRT-07]` forces regeneration of the index region it belongs to
(entry offsets change; entry lengths/crcs/sentinels unchanged; segment
CRC recomputed over the re-emitted entries). Layout:
- front `[0,16)`
- tile0 payload `[16,144)` — 128 bytes (content and crc unchanged, only
  offset moved)
- regenerated index region `[144,248)` — 104 bytes (entry 0 now
  (offset=16,length=128,crc=unchanged); entries 1–4 sentinel, unchanged)
- new directory `[248,357)` — 109 bytes
- pad `[357,384)` — 27 bytes (unavoidable — this is *not* reclaimable
  slack, it is the ordinary creation-path pad every generation has;
  §20.5 says a rewrite carries "no slack" meaning no *reclaimable*
  slack, not that a directory-to-trailer pad can be avoided when the
  directory does not happen to end on a 64-byte boundary)
- trailer `[384,448)`

F₄(output) = 448. Live = 16+128+104+109+64 = 421; slack = 27 (the
unavoidable pad only). 421+27 = 448. ✓ Compare to gen-3's total slack
of 667 bytes reclaimed to 27 bytes — this is the number `[R-CNT-21]`
says "tells an operator to compact," and it matches the document's own
description of what compaction buys.

### 2.4 A walk that does not complete

Take generation 2 above (F₂=768) but suppose the file also has a
second layer, `mask` (planar, bool, extents matching `sst`), whose
tile-index region I have *not yet reached* when I discover, mid-walk
on `sst`, that `sst`'s stored-tile extent [320,448) overlaps a
sub-record extent I placed (hypothetically) at [400,460) — an
intra-layer overlap (`[R-CNT-13]`, L18, verifier-detected). Per
`[R-CNT-21]`: "where the rejection is one the walk itself
established... the claimants it had already enumerated are discarded
with the layer" — so `sst`'s already-enumerated claimants (front,
`sst`'s index region, `sst`'s tile-0 payload) are *removed* from the
running live-bytes tally, `sst` is rejected whole, and — if I have not
yet started `mask`'s walk — `mask`'s claimants were never enumerated
either. The verifier must then report the slack total as **partial**:
an *upper bound* on true slack (never an under-count), naming L18 on
layer `sst` as the reason the walk did not complete, and explicitly
not attempting to net out `mask`'s bytes at all (I have no figure for
them, only the fact that they are unaccounted). Concretely: reportable
figure = F₂ − (bytes I am still willing to call claimed) = F₂ − (only
the directory and the live trailer, which are always reachable from
the trailer directly and are not part of the discarded layer) = 768 −
(109+64) = 595, reported as "≥ 595 bytes of slack, partial: walk
stopped on L18 in layer `sst`; layer `mask` unexamined." This is
deliberately a *loose* bound (I threw away figures I actually had, for
`sst`'s pre-violation claimants, because the rule requires discarding
a rejected layer's already-enumerated claimants entirely, not just the
overlapping bytes) — which is exactly the "upper bound, never an
under-count" property `[R-CNT-21]` requires, and it is why the note
under `[R-CNT-21]` calls a partial total "a fact about that run and not
about the file's live state."

I separately confirmed the *other* way a walk can be incomplete that
does **not** report partial: a tile whose only defect is a failed
stored-bytes CRC (T1) is "well-formed" under `[R-IDX-03]` and *keeps
its place* in the coverage walk (its extent is still claimed) even
though the tile itself is rejected and nonconforming — so a file
riddled with T1 failures but no *structural* (§15.3 "*structural*") or
scope-level failures still yields a **complete** walk and an exact
(non-partial) slack total, alongside a **nonconforming** verdict. This
is the distinction the document's own worked note in §5.2 draws between
"an entry `[R-IDX-03]` classifies reject-tile on a structural ground"
(walk still complete, bytes fall to slack) and a scope-level rejection
established by the walk itself (walk incomplete, partial total). I
built both cases above to make sure I had the distinction right rather
than asserting it from the prose alone.

### 2.5 Extent overlap / alignment / slab, adversarial layouts (computed, not abstract)

I ran three concrete adversarial constructions (script
`overlap_slab_check.py` in my scratch directory; no file bytes, pure
offset arithmetic):

1. **Alignment.** Declared A = 512. Tile 0 at offset 512 (512 mod 512
   = 0, aligned). Tile 1 at offset 612 (612 mod 512 = 100 ≠ 0). A
   verifier MUST flag this as reject-layer under `[R-SLB-01]` (L39/L40)
   — confirmed arithmetically that 612 is not a multiple of 512.
2. **Slab packing.** Declared S = 2, A_slab = 4096, run 0 = ordinals
   [0,2). Tile 0 at offset 4096 (aligned), length 200. Tile 1 placed
   (adversarially) at offset 4346 instead of the required
   4096+200=4296 — a 50-byte gap. `[R-SLB-03]` (L41) requires "each
   stored tile's offset equals the previous stored tile's offset plus
   that previous tile's length"; 4346 ≠ 4296, confirmed by
   computation, so this is reject-layer.
3. **Intra-layer extent overlap.** Tile A at [1000,1100), tile B at
   [1050,1150); interval intersection is nonempty ([1050,1100)),
   confirmed by computation. Under `[R-CNT-13]`/`[R-IDX-03]` this is
   L18 (reject-layer) because both extents belong to the same layer;
   had tile B instead belonged to a *different* layer at the same
   offsets, `[R-CNT-13]` routes it to **F33 (reject-file)** instead —
   I checked this scope-switch explicitly against F33's own text,
   which lists "a claimant reaching the front signature block or the
   live trailer is instead caught by the bounds rows," and separately
   confirms cross-layer overlap is file-scope while intra-layer
   overlap is layer-scope. This is a real, sharp scope boundary a
   verifier must implement correctly (same byte-level fact pattern,
   different outcome class, purely as a function of which layer(s) own
   the two extents) — I checked it here because it is exactly the kind
   of thing shape #2 ("one quantity named where two are in play") asks
   for, but found the text draws the line clearly and does not leave
   the two cases ambiguous.

## 3. Checksum obligations

§8.1's coverage map is exhaustive over seven rows; I checked each
structure this document defines is covered by exactly one of them
(front block: equality only; trailer: its own CRC; directory: its own
terminal CRC; tile-index region: per-segment CRC, itself covered by
crc_of_crc_array; stored tile: its entry's crc; user-metadata extent:
its own terminal CRC; an unassigned record type's extent: no checksum
at all, by design, since this document defines no fields there to
protect). I found no structure this document defines that is *not*
named in this map.

I independently **reproduced** every checksum constant the document
states that is computable without a physical file, using my own
from-scratch CRC-32C (reflected, poly 0x82F63B78 applied bit-by-bit,
init 0xFFFFFFFF, final XOR 0xFFFFFFFF — i.e. the textbook reflected
CRC-32C, not a table-driven or borrowed implementation):

| Constant | Document states | I computed | Match |
|---|---|---|---|
| CRC-32C("123456789") | `0xE3069283` | `0xe3069283` | ✓ |
| CRC-32C(zero bytes) | `0x00000000` | `0x0` | ✓ |
| CRC-32C(2¹⁶ sentinel entries) | `0xEECB3BB2` | `0xeecb3bb2` | ✓ |
| Appendix A minimal-file trailer CRC | `0x402F157E` | `0x402f157e` | ✓ (over the exact 60 trailer bytes the appendix's hex dump gives) |
| §7.4 example — index segment CRC (4 sentinel entries) | `0x80A34955` | `0x80a34955` | ✓ |
| §7.4 example — crc_of_crc_array | `0xC4EE982E` | `0xc4ee982e` | ✓ |

All six reproduced exactly. I could not independently reproduce any
checksum that depends on a *physical file's* payload bytes I do not
have (there are none stated as bare hex in the document beyond these
six — the deflate/zstd/lz4 worked examples give shuffled byte patterns
and float bit patterns, not additional CRC constants), so there is
nothing else in this category to check; I say so explicitly rather
than silently skipping it, per the evidence requirements.

**Which structures are covered by which checksum, and is every live
structure covered by one?** Yes: front block (equality), stored-tile
payload (entry crc → segment CRC → crc_of_crc_array → nothing further,
terminal), directory (its own terminal CRC), trailer (its own terminal
CRC), user-metadata extent (its own terminal CRC), and the *only*
uncovered live bytes by design are an unassigned record type's extent
(§8.1's own stated exception) and slack (which is not a "structure" at
all under `[R-CNT-02]`'s partition, so §8.1's "every field of every
structure" claim is not violated by slack going uncovered — I checked
this is not a gap: slack is explicitly outside the coverage map's
universe of discourse, per §5.2/§9.7's repeated statement that slack
"has no internal structure this specification defines").

## 4. Decoded-content obligations

A verifier that certifies **must** decode every stored tile
(§9.7, §17.4) — this is what distinguishes verifier obligations from
ordinary reader obligations, which only decode tiles a request
actually touches. Concretely the verifier must, per tile: apply the
codec then invert the filter (§17.1), confirm the decoded length is
exactly the declared decoded size (`[R-SER-07]`, T3), and then check
the content obligations that are otherwise invisible to any reader
(since a conforming reader "never returns padding positions" and so
"is not obligated to check" — `[R-SER-05]`): every padding position
equals its channel's recorded fill (T4), every packed-bool pad bit
equals the fill bit (T5), and every interleaved-bool value byte at a
*real* position is exactly 0x00 or 0x01 (T2). A verifier is
**permitted** to skip exactly two categories, and only by declining
certification rather than by silently passing: (a) a codec/filter it
cannot execute (`[R-COD-11]`) — for a *conforming reader* this can only
arise at a reserved/experimental value since all four codecs and both
filters are core and mandatory, but a verifier implementation that
happens not to implement, say, zstd, would have to report *cannot
establish* rather than certify any file with a zstd-coded layer; (b) a
user-metadata document it declines to decode on a size or window bound
(`[R-MTA-09]`), which is the verifier's own declared capability, not a
finding about the file. Neither decline is itself a violation.

I checked one subtlety here against shape #9 ("a rule whose object is
defined so precisely that it excludes its own exceptions"): §21.9's
lz4 tile-size cap (`[R-COD-07]`, L44) is "quantified over the layer's
*addressed* tiles," and an *empty* layer (any dimension extent 0)
addresses none, so it trivially satisfies the cap regardless of its
declared tile shape — the document states this explicitly ("the escape
ends exactly when the layer's addressed-tile count rises above 0"),
and I confirmed this is the *only* place codec 4's cap and the general
`[R-ENC-04]` overflow rule diverge in their quantifier (the overflow
rule binds every declaration-derived product "whether or not the layer
addresses a tile"). This is stated correctly and consistently in both
places I found it discussed (§17.2's Note and §20.3 step 4's bounds
paragraph), so I am not filing it, but it is exactly the kind of
quantifier-mismatch shape #1/#9 exist to catch and I want to record
that I looked and it holds up.

## 5. Multi-generation trace with certification at each step

Using the four generations built in §2.3:

- **Gen 1 (create).** Layer `sst`, 4 addressed tiles, all sentinel.
  Coverage partitions exactly (§2.3). Every checksum I can compute
  locally verifies (trivially — the index array is 4 sentinel entries,
  segment CRC = CRC-32C of `FF×16 00×4` repeated 4 times, which I also
  computed independently and matches the document's worked §7.4
  example exactly). No stored tile to decode. **Verdict: conforming.**
- **Gen 2 (append: store tile 0).** New index region re-emitted whole;
  tile 0's stored bytes (128 bytes, codec 1/none) match their entry's
  crc, decoded length equals P·Q=128 exactly. Extent 100, tile extent
  32: tile 3 (positions 96–127) has 4 real positions (96–99) and 28
  padding positions (100–127); tile 0 (positions 0–31) has no padding.
  For tile 0 specifically there is no padding to check; had I stored
  tile 3 instead I would additionally verify all 28 padding positions'
  4-byte float fields equal the channel's recorded fill exactly (T4).
  Coverage partitions exactly (§2.3, F₂=768 closes). **Verdict:
  conforming**, assuming the caller supplied a genuinely valid 128-byte
  encoded tile.
- **Gen 3 (update: grow extent 100→150, no new tile stored).** Whole
  index re-emitted (grid count changed 4→5); tile 0's entry carried
  byte-identically at its unchanged disk ordinal; new tile 4 addressed
  as sentinel. Coverage partitions exactly (§2.3, corrected
  arithmetic, F₃=1088). **Verdict: conforming.**
- **Gen 4 (compact/rewrite, fresh file_id).** Tile 0's payload
  relocated with content and crc preserved bit-for-bit; index region
  regenerated (offset field only); reference array of the carried
  layer is required to equal the live generation's bit-for-bit
  (`[R-MDL-02]`, `[R-WRT-07]`) — trivially true here since I performed
  no re-encoding, only relocation. Fresh file_id (I used Y ≠ the
  original X). Slack collapses from 667 bytes (gen 3) to the
  unavoidable 27-byte pad. **Verdict: conforming**, and this is the
  generation whose slack total (27, vs. 667 a moment before) is the
  number `[R-CNT-21]`/Appendix D's rationale say motivates running a
  compaction in the first place — I now have that number from an
  actual construction rather than from the prose alone.

At every step the two axes the document insists are independent held
apart cleanly in my construction: file conformance (a pure predicate
on the bytes I built) never depended on which tier of writer produced
them, and the reader-outcome/verifier-outcome distinction (T1 keeps a
tile's extent in the walk even on failure; L18/F33 discard a layer's
or the walk's claimants entirely) produced different, correctly-scoped
consequences from superficially similar byte patterns.

## 6. Findings

**None survive to be filed.** I found zero AMBIGUITY, CONTRADICTION,
or OBSERVATION findings I am confident meet the taxonomy's bar after
the review documented above. Section 7 records what I opened and
closed instead, since an empty list without that record is not a
clean result.

## 7. Rejected candidates

**7.1 — "Two positions... the choice is its own" as a byte-level fork
(§20.1).** Worked in full in §1.2 above. Closed because: (a)
`[R-CNF-02]` makes file conformance a pure predicate on output bytes,
independent of which position produced them; (b) `[R-CNF-05]`'s
already-licensed writer divergence ("two conforming writers given
identical input MAY produce different conforming files") covers
exactly this divergence — a creator's flags=0 output and a rewriter's
flags-carried-forward output are two different, both-conforming files,
not two different verdicts on one file; (c) I could not find any
sentence that assigns the classification "from outside" (by what the
tool decoded, or by an objective test on its output) that would
contradict "the choice is its own" and thereby create a genuine
CONTRADICTION — I searched specifically for one and found none. What
remains is a real, and slightly startling, design fact (a tool can
sidestep `[R-WRT-06]`'s mandatory refusal-to-rewrite by declaring
itself a creator instead of a rewriter, even while copying bytes from
the very file that would have triggered the refusal), but it is
explicit in the text rather than ambiguous or self-contradictory, and
its consequence is a writer-conduct question (per `[R-CNF-02]`'s
conduct/predicate split), not a fork in what bytes a conforming
implementation may emit or a reader/verifier must accept or reject —
the "loophole" produces a *different conforming file*, not a disputed
verdict on the *same* file. I am not confident enough that this
crosses into CONTRADICTION or AMBIGUITY territory to file it, and file
it here instead so the reasoning is visible rather than silently
dropped.

**7.2 — §3.3's Note missing "verifiers" from any implicit list.**
Considered and closed in §1.5: verifiers are correctly *excluded* from
the "cannot decode" claim (they must decode everything to certify,
§17.4/§9.7), so their absence is required, not a gap.

**7.3 — Channel count C as an unlisted field in §20.3 step 4's fixed/
permitted partition.** Considered and closed in §1.3: C is not named
as an independent line item, but is fully and unambiguously determined
by the channel-list rules for both layouts, so there is no field left
ungoverned.

**7.4 — A commit reducing a layer's addressed-tile count to zero after
it has already stored tiles.** Considered while checking §20.3 step
4's "A layer the new state leaves addressing no tile has no region to
re-emit" sentence. Closed by arithmetic: extents can only grow (never
shrink) and channel count has a floor of 1, so N (interleaved) or C·N
(planar) can never be driven from positive back to zero by any
*permitted* appender change once positive; the sentence in question
therefore only ever applies to a layer that was already at zero
addressed tiles (i.e. one being "freely re-declared," not one subject
to the fixed-declaration bar), which is the only case the text's
surrounding context actually needs it for.

**7.5 — Rewriter relocating an MU=1-record-of-an-implemented-type's
internal references (§20.5, "No other record payload carries a file
offset").** Considered whether an MU=1 type the rewriter *does*
implement, if it carries internal offsets a hypothetical future
registration might define, is adequately covered. Closed: the text
explicitly handles exactly this — "An MU = 1 type it *does* implement
is the remaining case, and §7.2 admits it... so a rewriter implementing
one relocates whatever that registration defines, on the same terms as
the tile index" — this is a forward-looking hook (registration is
required to specify how, per `[R-EXT-04]`), not a gap in the current
text, since format major 1 registers no such type today (only the
layer record itself carries this property, and §20.5 already gives it
its own regeneration procedure).

## 8. Evidence

**sweeps_run.** (1) Full sequential read of spec/tarn.md, all 4981
lines, in five passes. (2) `grep -n "exactly as\|the same way\|likewise\|for the same reason"` over the document → 20 hits, each read in
context (§1's list above covers the ones inside the four flagged
decision passages; the rest are unrelated cross-references I checked
briefly and found unremarkable — e.g. §21.6's "exactly as it does for
an unrecognized key" pairing `tarn.axes`/`tarn.stats` placement rules,
which restate the same non-violation twice consistently). (3) A
field-by-field partition check of every §7.4 layer-record field
against §20.3 step 4's "MAY change" / "fixed" lists → every field
placed in exactly one bucket, zero gaps, zero double-assignments. (4)
Independent CRC-32C re-derivation of all six checksum constants the
document states as bare hex (check vector ×2, full-sentinel-segment
constant, Appendix A trailer CRC, §7.4 worked-example segment CRC and
crc_of_crc_array) → six of six matched. (5) Hand-built four-generation
file trace (create/append/update/compact) with full byte-offset
bookkeeping and coverage-partition arithmetic at each generation,
including one arithmetic error I made and caught by re-deriving instead
of accepting a total that didn't close (§2.3, generation 3). (6) A
constructed "walk that does not complete" scenario, worked through
`[R-CNT-21]`'s partial-total rule to a concrete reported figure. (7)
Three concrete adversarial layouts (misaligned tile, slab packing gap,
intra-layer extent overlap) checked arithmetically against
`[R-SLB-01]`/`[R-SLB-03]`/`[R-CNT-13]`. (8) Cross-check of §10.2's
numeric-identifier-space table and Appendix C's registry snapshot
against every space's defining section (§7.3, §12.1/§12.2, §17.2,
§17.3, §14.1, §11.4, §7.4, §18.2) → all matched exactly, no divergence
found. (9) Targeted re-reads of all four "decisions" the charter names
(§20.4's table/drop paragraph, §7.2's Note/preceding paragraph, §20.1's
closing paragraph with §2.3's updater clause, §20.3 step 4's scope
sentence/closing paragraph) plus the three literally-changed passages
(§3.3, §20.3, §20.4) against every cross-referenced rule each one
cites, following each `[R-...]` citation back to its defining section
at least once.

**derived_numbers.** CRC-32C("123456789") computed `0xe3069283` vs.
document's `0xE3069283` (match). CRC-32C(∅) computed `0x0` vs.
`0x00000000` (match). CRC-32C(2¹⁶×sentinel) computed `0xeecb3bb2` vs.
`0xEECB3BB2` (match). Appendix A trailer CRC computed `0x402f157e` vs.
`0x402F157E` (match). §7.4 example segment CRC computed `0x80a34955`
vs. `0x80A34955` (match). §7.4 example crc_of_crc_array computed
`0xc4ee982e` vs. `0xC4EE982E` (match). Layer-record inline-payload
size: computed 4+34 (fixed scalars) + 18 (one dimension entry) + 12
(one channel entry) + 13 (trailing fixed fields) = 81 bytes, vs.
document's stated 81 (match). Index-region size via `[R-CNT-17]`'s
formula at entry_count=4: 4×20+⌈4/2¹⁶⌉×4 = 84, vs. document's implicit
84 (80-byte entry array + 4-byte segment CRC array, match). My own
four-generation file: F₁=320, F₂=768 (ΔF=448≥128 ✓), F₃=1088
(ΔF=320≥128 ✓, after correcting one addition error), F₄=448 (fresh
file_id, ΔF is not meaningfully comparable across a rewrite since it's
a different file_id/history). Coverage-partition sums closed exactly
(live+slack=F) at every one of the four generations once corrected.
Slack at gen 3 (667 bytes) vs. slack at gen 4 post-compaction (27
bytes, the unavoidable pad only) — a 640-byte reclaim on a toy file,
illustrating the "index region for the whole layer re-emitted on every
tile edit" cost the document's own §20.3 Note describes qualitatively.

**rejected_candidates.** Five, detailed in §7 above with the sentence
or arithmetic fact that closed each: (7.1) the rewriter/creator
"choice" as a byte fork, closed by `[R-CNF-02]`'s pure-bytes predicate
plus `[R-CNF-05]`'s licensed-divergence sentence and the absence of any
externally-assigning sentence to contradict "the choice is its own";
(7.2) verifiers missing from §3.3's Note, closed by §17.4/§9.7's
explicit decode-everything requirement for certification; (7.3)
channel count C unlisted in §20.3 step 4's partition, closed by its
full determination via the channel-list rules; (7.4) addressed-tile
count reduced to zero after tiles are stored, closed by the
monotonicity of extent growth and the channel-count floor; (7.5) an
implemented MU=1 type's internal references under rewriting, closed by
the explicit forward-looking clause covering exactly that case.

**confidence_empty.** For the certification-procedure and
decoded-content-obligation portions of my charter, "found little" does
not apply — I built a concrete, runnable-on-paper algorithm and traced
it over four real generations plus one incomplete-walk scenario and
three adversarial layouts, so there is a positive result to show
throughout §2–§5, not an absence. Where I found *zero findings*
(§6) rather than little evidence, what would have found something: a
genuine textual gap in the §20.3 step 4 permitted/fixed partition would
have shown up as a §7.4 field landing in neither list or in both (my
sweep #3 checked every field individually and found none); a genuine
inconsistency in §7.2's Note vs. its governing rule `[R-CNT-12]` or
§20.4's table would have shown up as the three-states-not-four claim
failing to match the table's three actual rows (I matched them
one-for-one); a genuine checksum-constant error would have shown up as
my from-scratch CRC-32C disagreeing with any of the six stated hex
constants (all six matched); a genuine coverage-arithmetic error in the
document's own worked examples would have shown up as my hand
partition sums failing to close to F at any generation (all four
closed, one only after I caught and corrected my own transcription
error, which I left visible in §2.3 rather than silently fixing). None
of these checks came back empty of effort; they came back negative for
defects, which is a different thing and is why I am reporting zero
findings rather than reporting nothing.
