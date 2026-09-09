# Round 33 — Register hunter — working transcript

Charter: §21, the error-handling register, audited against the rules it restates
and against itself.

## 0. Access, disclosure, and method

I read exactly one file: `/Users/robertkleffner/Documents/GitHub/tarn-first-draft/spec/tarn.md`.
It was where the brief said it would be. I opened no ADR, no findings file, no
conformance directory, no registry, no git history. I ran no web tool.

**Context I did not ask for.** Before I began, my runtime placed a project
instruction file (CLAUDE.md pointing at AGENTS.md) and an index of the
maintainer's persistent memory notes into my context. The memory index carries
titles that name this project's harness, its lineage gate, its repair
methodology and its prior failure modes. None of it is part of the
specification and I have not used any of it as evidence, nor let a title steer
where I looked; I record its appearance because the brief requires it. My
charter (§21) was set by the brief, not by that material.

Scratch files I wrote, all under
`/private/tmp/claude-501/.../r33-round/scratch/register/`:

- `count_inst.py` — parses the four register tables out of the document and
  counts rows and semicolon-separated instances per row.
- `crc_reg.py` — a from-scratch CRC-32C (Castagnoli, reflected, init/final
  0xFFFFFFFF) used to re-derive the document's stated checksum constants.

I wrote nothing to the repository and nothing to the output directory except
this transcript. I did not list or read the output directory.

**Wrapping.** Every phrase search I ran was run over a whitespace-normalised
copy of the document built in Python (newlines and any leading `> ` collapsed
to a single space), so a phrase spanning a hard wrap or a blockquote marker
still matches. Where I report a zero I say what positive control I ran beside
it.

---

## 1. First pass: reading §21.1's own rules before anything else

§21.1 is the section that governs the rest of §21, so I read it first and held
everything else to it. Its load-bearing claims, extracted:

1. The register is §21.2–§21.5 and "enumerates every detectable
   file-conformance violation this specification names".
2. Each row's outcome is "the outcome class its scope determines (§2.4) — except
   where a rule assigns one expressly, as `[R-CNT-25]`'s quarantine does for
   every §21.5 row, whatever the containing scope".
3. The Governing rule cell "names that requirement first; any identifiers
   following it in parentheses are the further rules the condition reads".
4. Completeness is normative; detectability is §21.7's test.
5. "each row *restates* its governing rule, and where a row and the rule it
   cites diverge, **the rule governs**."
6. Strict specializations: the file is recorded against the narrower row,
   "whose detector and detection point are the ones that apply". Named pairs:
   F1's front-block instance of F6, F1's trailer-magic instance of F8, F35 of
   F36, L24 of L25, F21 of F22, L10 of L11. Explicitly not a closed list.
7. §21.6–§21.9 are outside the register; §21.6's entries get the same
   rule-governs tiebreak.
8. The Instances arithmetic: alternatives × containers; layout-varying derived
   quantities enumerate the layout formulas; a two-magnitude comparison
   enumerates two directions and a one-directional bound enumerates one; a
   comparison with no magnitude ordering (checksum vs computed, byte pattern vs
   constant) enumerates none; a nonzero test is not a comparison; semicolons
   separate; a cell reading `—` is one instance.
9. Detection points are §19.2's four reader tiers plus *certification*.
10. For verifier rows the outcome "names the scope at which the damage is
    recorded, not an obligation on any reader".

Two of these I checked against their sources immediately.

**(9) against §19.2.** §19.2's four bullets are "at open", "at first access to a
layer", "at use of a tile", "at use of a record's extent". §21.1 renders them
"open, layer access, tile use, extent use". Agrees. I then tallied the actual
Detected cells (script `count_inst.py`, extended): `layer access` 34, `open` 31,
`tile use` 24, `certification` 20, `extent use` 9, plus two compound cells (L23,
R1). No cell carries a value outside that vocabulary. The Detector column takes
exactly two values: `reader` 100, `verifier` 20. The 20 `verifier` rows and the
20 `certification` rows are the same 20 rows (F7, F25, F26, F27, F28, F33, F36,
L18, L25, L40, L41, L42, L46, L47, L48, L49, T2, T4, T5, T26) — no verifier row
is given a reader tier and no reader row is given *certification*.

**(10) against §2.4.** §2.4 defines four reader outcomes — reject-file,
reject-layer, reject-tile, ignore-record — plus preserve-verbatim, which it
expressly calls an updater obligation "orthogonal to reader outcomes". The four
subsection headers of §21.2–§21.5 use exactly the four reader outcomes, one
each. So the outcome vocabulary is closed, every defined reader value is
reachable, and preserve-verbatim's absence from the register is not a gap
because it is not a reader outcome. That closes the "outcome vocabulary" half of
my charter in both directions.

---

## 2. The counting — recounted by hand and by script

I derived the counts myself before reading the document's totals in anger.

Script `count_inst.py` extracts every table line matching `^\|\s*([FLTR]\d+)\s*\|`,
splits on `|`, and counts semicolon-separated non-empty instance fragments,
treating a cell of `—` as 1 — which is exactly §21.1's stated arithmetic ("the
count is therefore mechanical once the cell is written").

Rows per subsection:

| Subsection | rows found | document states |
|---|---|---|
| §21.2 | 35 (F1–F36 with F11 struck) | 35 conditions |
| §21.3 | 49 (L1–L49) | 49 conditions |
| §21.4 | 26 (T1–T26) | 26 conditions |
| §21.5 | 10 (R1–R10) | 10 conditions |
| total | **120** | §21.8: 120 conditions |

Instances per subsection (my derivation): F 56, L 116, T 55, R 50 = **277**.
§21.8 states 277. Both totals reproduce exactly. The F11 gap is accounted for by
the Note under §21.2 ("Row label F11 is struck ... retired on the model §2.2
states"), which is consistent with §24's `[R-VEC-02]` ("a row label is never
renumbered and never reused").

I then spot-audited the instance arithmetic against §21.1's own rules rather
than trusting the total:

- Two-direction magnitude comparisons: L30 (fill prefix *differs from* element
  size) 2; L21 (entry_count *does not equal*) 2 layouts × 2 = 4; L22 2 + 2
  extras = 4; T3, T14, T22 each 3 layouts × 2 = 6; F17 2; F23/L12 2. All obey
  the rule.
- One-directional bounds: F5 ("below"), F9 ("less than 16"), F16 ("less than
  4"), L44 ("exceeds"), T21 ("larger than") — one direction each. Correct.
- No-ordering comparisons: F8 and F1 (byte pattern vs constant), F14, F20, L37,
  L38, T1 (stored checksum vs computed) — no direction enumerated. Correct.
- Nonzero value tests: L20 ("both A ≠ 0 and S ≠ 0"), L27, L28 — 1 each, exactly
  as §21.1's "an *A ≠ 0*, an *S ≠ 0*" clause says. Correct.
- Single predicate over several fields: F25 (MU/PE combination) 1; F3 and L2
  (sums against a bound) count sums not fields. Correct.
- Family without a shape change: T24 ("any codec") 1; F19 ("flags bits 0-15") 1;
  F26 and L47 ("flags bits 2-15"). Correct.
- Layout-varying derived quantities: T3, T14, T21, T22, L44 enumerate the three
  layout formulas (P·Q, P·Bᶜ, ⌈P/8⌉). Correct.
- R4: six frame-constraint shapes + the two directions of the content-size
  comparison = 8, × 2 containers = 16. Reproduces the cell exactly.
- R5: 2 alternatives × 2 locations (key/string value) × 2 containers = 8.
  Reproduces.
- R6 + R10 between them cover all three of §4.6's name rules folded onto keys
  (non-empty, ≤255 bytes, no U+0000–U+001F) — R6 the first and third, R10 the
  second.

No cell contains a semicolon that is not a separator (I checked the ones with
internal punctuation: L2's parentheticals, L23's field lists, L41). So the
mechanical count is safe.

**Derived numbers checked outside the register.** Using `crc_reg.py`:

| Quantity | I computed | document states |
|---|---|---|
| CRC-32C("123456789") | 0xE3069283 | 0xE3069283 (§4.5) |
| CRC-32C(zero bytes) | 0x00000000 | 0x00000000 (§4.5) |
| CRC-32C of 2¹⁶ sentinel entries | 0xEECB3BB2 | 0xEECB3BB2 (§15.4, L38, App. B) |
| CRC-32C of 4 sentinel entries (80 B) | 0x80A34955, stored `55 49 A3 80` | same (§7.4 example) |
| crc_of_crc_array over that 4-byte array | 0xC4EE982E | same (§7.4 example) |

L38's row text ("the all-sentinel constant 0xEECB3BB2 never substitutes for
comparison") therefore quotes a constant that is correct, and its restriction to
*full* segments matches `[R-IDX-05]`'s "a partial segment's CRC MUST be
computed".

**§21.9's Note arithmetic, checked.** "2³² addressed tiles is the point where the
segment-CRC array ... is still 256 KiB — it reaches 4 MiB at 2³⁶". Array size is
⌈entry_count/2¹⁶⌉ × 4. At 2³²: 2¹⁶ segments × 4 = 2¹⁸ B = 256 KiB ✔. At 2³⁶:
2²⁰ × 4 = 4 MiB ✔. "65,536 layers is roughly a 12.5 MiB directory": 12.5 MiB /
65,536 = exactly 200 bytes per record, which is a plausible "small layer record"
(24-byte header + ~176 payload) ✔, and the 16 MiB dir_length row is that budget
rounded up ✔. "256 MiB is an order of magnitude above the tile sizes §11.3
describes as ordinary" — §11.3's Note gives "roughly 1 to 16 MiB", so 256 MiB is
16× the top of that range; "an order of magnitude" is loose but not wrong.

---

## 3. Row-versus-rule agreement, row by row

I opened each governing rule and compared wording, outcome, scope and detector.
What follows records the comparisons that mattered; the ones that matched
exactly I list in compressed form.

### 3.1 File scope (§21.2)

`[R-CNT-06]` states, in §6.2, exactly nine conditions: trailer magic; trailer
CRC; committed_file_length = file size; committed_file_length a multiple of 64;
dir_offset ≥ 16; dir_length ≥ 4; dir_offset + dir_length ≤ F − 64; file_id ≠ 0;
reserved bytes zero. The register carries F8, F14, F17, F13, F9, F16, F10, F12,
F15 — nine rows, one per condition, in bijection. §2.3 independently asserts
"`[R-CNT-06]` states nine". Agrees.

The rest of §21.2 maps: `[R-ENC-02]`→F1, `[R-CNT-04]`→F6, `[R-CNT-07]`→F18,
`[R-CNT-08]`→F19, `[R-CNT-11]`→F20, `[R-CNT-27]`→F5, `[R-CNT-05]`→F7,
`[R-CNT-13]`→F30/F31/F32/F33, `[R-CNT-12]`→F24/F25/F26/F29,
`[R-CNT-14]`→F34, `[R-CNT-15]`→F35/F36, `[R-CNT-25]`→F21/F22,
`[R-MTA-03]`→F23, `[R-MTA-05]`→F27, `[R-CNT-22]`→F28, `[R-ENC-03]`→F2,
`[R-ENC-04]`→F3, `[R-ENC-15]`→F4. That is 35 rows, and I could not construct a
file-scope MUST-level condition without a row (see §4 below for the sweep).

Boundary wording, checked one by one because this is where an off-by-one hides:

- F32 "extent_offset + extent_length exceeds F - 64" vs `[R-CNT-13]`'s "an
  extent extending past F − 64". A sum exactly equal to F − 64 ends at the last
  byte before the trailer and is legal under both. Agrees, and matches L17
  ("> F - 64"), T9 ("ends past F − 64") and F10 ("exceeds F - 64") against
  §6.2's "dir_offset + dir_length ≤ F − 64".
- F31 "extent_offset in 1-15" vs `[R-CNT-13]`'s "an extent_offset < 16": offset
  0 is the (0,0)/half-zero case, which F21 and F30 own. F33's own text confirms
  this partition explicitly ("a record extent slot of (0, N) with N nonzero
  reaches the block through its zero offset and is theirs rather than F31's").
  Agrees.
- F9 "less than 16" vs §6.2's "dir_offset ≥ 16". Agrees.
- F5 "below the 128-byte minimum" vs `[R-CNT-27]`. See finding register-06.

**The `[R-CNF-13]` reach derivation in §21.2's header.** The header claims the
reaching rows are "F8, F14, F6 and both of F1's instances ... and no other row".
I re-derived this from `[R-CNT-24]`, which fixes, in every major: (a) the trailer
magic at F − 64; (b) version_major and version_minor at F − 56; (c) a CRC-32C at
F − 4 over [F − 64, F − 4); (d) the constancy of the front signature block; (e) a
48-byte redefinable remainder and no growth. Rows asserting (a): F8 and F1's
trailer-magic instance. Asserting (c): F14. Asserting (d): F6 and F1's
front-block instance. (b) is a position invariant no row asserts — F18 asserts a
*value* constraint on version_major, which the header correctly treats as
outside `[R-CNF-13]`'s premise rather than as an exception. (e) is asserted by no
row. Every other file-scope row reads a field inside the redefinable 48 bytes
(F2's committed_file_length, F13, F15, F17, F19, F12, F9, F10, F16) or a
format-major-1 structure (F5, F7, F20–F36). So "and no other row" holds. §2.3's
Note independently works three of these (F14 reaches, F5 does not, F15 does
not); all three agree with my derivation.

### 3.2 Layer scope (§21.3)

49 rows. I mapped each to its rule and found nothing missing and nothing extra.
The comparisons worth recording:

- **L1's field list.** `[R-ENC-03]` bounds "every offset, length, extent, and
  count ... entry counts and slab run lengths included". L1 enumerates layer
  record and sub-record extent_offset/extent_length, Eᵢ, Tᵢ, entry_count, and S
  — eight. It does **not** list alignment A or slab alignment A_slab, and I
  initially took that for a gap. It is not: A and A_slab are neither offsets,
  lengths, extents nor counts, and a value above 2⁶³ − 1 in either is caught by
  L39 ("A above 2^62") and L29 ("A_slab above 2^62"), because both must be
  powers of two within those ceilings. The document is internally consistent
  about this in a third place: §21.9's hard-limit paragraph says the 2⁶²
  ceilings "are chosen here too rather than consequences of the u64 domain",
  which is only true if `[R-ENC-03]` does not already bind them. Three passages
  agree; suspicion closed.
- **L2's dominance claims.** L2 lists nine derived quantities and justifies two
  omissions inline: "planar C·N (which dominates the max disk ordinal
  (C−1)·N + (N−1))" — true, since C·N ≥ C·N − 1 — and "interleaved P·Q (which
  dominates V = P·C)" — true, since Q = ΣBᵢ ≥ C when every element size is ≥ 1,
  which §12.1 guarantees. The packed-planar decoded size ⌈P/8⌉ ≤ P is dominated
  by P; Q itself is at most 8 × 65,535 and cannot overflow; the in-tile ordinal
  is < P and the spatial ordinal < N. So the list is complete for the quantities
  §14.2/§11.2/§7.4 designate. Suspicion closed.
- **L23's four regions** are exactly `[R-CNT-18]`'s four ("the fixed fields, the
  d dimension entries, the C channel entries, and the trailing fixed fields").
  Its split detection cell — "open (the name field, §19.1 step 4); layer access
  (every other field and entry)" — matches §19.1 step 4 verbatim in substance
  ("a layer record whose name field does not lie entirely within that record's
  inline_length ... is instead a validity error at layer scope (`[R-CNT-18]`)").
- **L27 vs L37.** With entry_count = 0 the segment-CRC array is empty and its
  CRC-32C is 0x00000000 (I computed this), so `[R-CNT-23]`'s "0 when
  entry_count = 0" is not an arbitrary constant but the value L37's own check
  would produce. The two rows do not conflict, and L27's earlier detection point
  (layer access, no I/O) is the one §19.3 licenses.
- **L15/L16/L17** restate `[R-CNT-13]`'s three slot faults at layer scope; F30/
  F31/F32 restate the same three at file scope for non-layer top-level records.
  The partition — "non-layer top-level" vs "layer record or sub-record" — is
  exactly `[R-CNT-13]`'s "the layer for a layer record and for sub-records, the
  file for other top-level records", and the same partition is used for the flag
  rows (F25/F26 vs L46/L47) and the registry-flag rows (F28 vs L49). Consistent
  across all three pairs.
- **L46/L47/L49's placement at layer scope** turns on `[R-CNT-13]`'s reading of
  §7.3, not on §7.3's own Scope column, which says of the layer record "file
  (container for layer scope)". I read that as a tension and then closed it:
  `[R-CNT-13]` states flatly "the layer for a layer record", adds "a malformed
  slot on a layer record is therefore reject-layer, consistent with
  `[R-CNT-17]`", and §7.3's parenthetical says "container for layer scope". The
  register follows `[R-CNT-13]`. Not a finding.
- **L26** cites "(§7.3 registry table)" where §21.1 says parentheticals hold
  "identifiers ... the further rules the condition reads". L31 likewise cites
  "(§15.1)". A section reference is not an identifier. I considered filing this
  and did not: §21.1's sentence is about how to read identifiers when they
  appear, not a prohibition on section pointers, and no reading of the row moves.
- **§16.2's `[R-SLB-04]`** (a stale slab declaration carried forward) carries a
  Note saying it has no register row because every file exhibiting it exhibits
  an L41 or L42 failure. I tested the claim: if the invariants happen to hold in
  the new generation, the writer has "re-established" them and there is nothing
  to detect; if they do not, L41 or L42 fires. The claim holds.
- **§7.4's nesting Note** likewise claims no row for depth-beyond-two nesting,
  because detecting it requires parsing an opaque payload as records — except
  for the layer record, whose appearance as a sub-record is L26. L26 exists.
  Claim holds.

### 3.3 Tile scope (§21.4)

§15.3's classification table has eleven rows. Mapping: sentinel-with-crc≠0 → T6;
exactly-one-sentinel → T7; length 0 → T10; offset < 16 → T8; offset or length
> 2⁶³ − 1 → T11; overflow or > F − 64 → T12 and T9; stored bytes fail crc → T1;
intra-layer overlap → L18; cross-scope overlap → F33; alignment/slab → L40–L42.
Nothing in §15.3 lacks a row. §15.3 also says "Six rows are marked *structural*";
I counted the *structural* markers in the table: six. Agrees.

Codec rows against §17.2: `[R-COD-04]`→T14, `[R-COD-05]`→T15/T16,
`[R-COD-06]`→T17 (magic), T18 (skippable/second frame), T19 (dictionary ID), T20
(content-checksum flag), T21 (window > decoded size), T22 (content-size ≠
decoded size), `[R-COD-07]`→T23 and L44, `[R-COD-08]`→T24/T25 and (via
`[R-SER-07]`) T3, `[R-COD-02]`→T13, `[R-COD-10]`→T26. Six of `[R-COD-06]`'s
constraints, six rows; the seventh — undisclosed dictionary use — the rule itself
declares undetectable ("not detectable by inspection ... the same undetectable
class as any other writer that emits wrong bytes"), so §21.1's completeness
clause requires no row, and §21.7's test agrees. Correct.

T2's carve-out ("the same byte at a padding position is T4's, the two rows
together covering `[R-SER-08]`") is sound: an interleaved bool padding byte other
than the recorded fill breaks `[R-SER-05]`, and L35 guarantees the recorded fill
byte is itself 0x00 or 0x01, so T4 catches every out-of-range padding byte.

### 3.4 Ignored records (§21.5)

`[R-CNT-25]`'s four named ways a document can be unreadable map to R2 (extent
CRC), R1 (invalid/unimplemented encoding), R3 (decode failure), R5–R10 (content
rules). R4 is the extra: the frame constraints §18.2 carries over from
`[R-COD-06]`. That extra is where finding register-02 lives.

§18.2's carried-over list is "the frame magic; no skippable frame and no second
frame; no dictionary use, disclosed or not, and no nonzero dictionary ID; no
content-checksum flag; and the bar on sizing any buffer from a length the frame
itself declares", plus this section's own content-size pin, plus "exactly one
... frame occupying the extent's bytes before its terminal CRC". Two are
excluded by §18.2 itself ("R4 registers neither"): undisclosed dictionary use
(unwitnessed) and the buffer-sizing bar (states no file condition). What is left
is six shapes, and R4 enumerates six shapes × 2 containers, plus the
content-size comparison's two directions × 2 containers = 16. Reproduces.

---

## 4. Completeness sweeps — both directions

### 4.1 Is there a condition without a row?

Sweep 1: normalised search for `validity error` — 52 hits. I walked all 52 with
three lines of context each. Each one either resolves to a register row (the
mapping in §3 above), or is a definition of the phrase itself (`[R-CNF-08]`), or
is one of the four the document expressly excuses:

- `[R-ENC-06]` fixed field widths — §21.7: "not a state a file can be in".
- `[R-CNT-18]`'s nesting-depth prohibition — §7.4's Note: no reader-detectable
  witness.
- `[R-SLB-04]`'s stale slab declaration — §16.2's Note: detection *is*
  `[R-SLB-03]`'s.
- `[R-CNT-02]`'s "belongs to no coverage class" — §5.2's Note: "a register row
  for it would be a row no file could exhibit".
- `[R-LIF-04]`'s residue past a completed commit — §9.5's Note: a reader meets it
  as F8/F14/F17.

Sweep 2: `MUST NOT emit` — 18 hits, all walked. Each is either paired with a
reader clause that a row restates, or is a conduct rule `[R-CNF-02]` places
outside file conformance (§10.3's publication bar, §18.3's registry-version bar),
or is `[R-ENC-01]`'s big-endian bar, which — like `[R-ENC-06]` — states no
condition a file can exhibit except at the signature constants, where F1 exists.

Sweep 3: `is a violation` (5), `makes the file nonconforming` (3),
`not a conforming file` (1), `is invalid` (12) — all walked, all resolve to rows
already found or to §21.6 non-violations.

Sweep 4: §22 and §23 (security, privacy) for MUST-level obligations — six hits,
every one a constraint on a *consumer's* behaviour (allocation sizing, name
display, path interpretation, metadata influence, erasure claims), none a
condition a file exhibits. No missing rows there.

Positive control for the sweeps: I ran the same normalised search for a phrase I
knew was present in the §21.5 preamble — `quarantine does for every` — and for
`each way a user-metadata record's document can be unreadable`, both of which
span hard wraps in the raw file. Both returned 1. So a zero from this
instrument would have been a real zero.

### 4.2 Does any row register a non-violation?

I took §21.6's fifteen entries and checked each against the register for a
collision: sentinel entry (T6 registers only crc≠0); coordinate outside extents
(no row); dimension extent 0 (L32 covers rank, C and Tᵢ, never Eᵢ); zero layers
(no row); experimental record type with MU = 0 (F35/F36/L24/L25 are all
reserved-range only); ignore-lane flag bit (F19 is the incompat lane only);
higher version_minor (F18 is version_major only); slack (F7 registers a
*structure* in the gap, not the gap); bool/numeric mix (no row); experimental
metadata encoding (R1 covers 0 and 3–0x7F only); unrecognized `tarn.` key (no
row); misplaced standardized key (no row); document size or window over the
reader's bound (R4's instance list contains neither); trailer mimic in a payload
(no row); compressing codec decoded ≠ stored length (T14 is codec 1 only). No
collision anywhere.

I also checked the twenty verifier rows for the opposite failure — a row whose
rule does not actually make the condition a violation. Each rule says so
expressly: `[R-CNT-05]` ("A verifier MUST treat a structure in that gap as a
validity error at file scope"), `[R-CNT-12]` ("Both writer violations make the
file nonconforming"), `[R-CNT-22]` ("makes the file nonconforming"),
`[R-MTA-05]` ("the file is nonconforming, a verifier MUST report it"),
`[R-CNT-13]`, `[R-CNT-15]`, `[R-SLB-01]`, `[R-SLB-03]`, `[R-SER-05]`,
`[R-SER-08]` ("Any other byte makes the file nonconforming"), `[R-COD-10]`.
All twenty stand.

---

## 5. Every cross-reference to a row

I extracted every occurrence of `\b[FLTR][0-9]{1,2}\b` in the document (regex
over the raw file, then de-duplicated by line) and resolved each by hand. The
citing sites outside the tables are: §2.3 ×5 (F18; F14/F5/F15 in the Note; R1),
§5.2 (L18, L40–L42), §6.2's trailer table (F19), §7.1 (F27, L48), §7.4's Note
(§21.3 by section), §9.5's Note (§21.2 by section), §9.6 (F8, F14, F17), §16.2's
Note (§21.3 by section), §17.2's Note (T24), §18.2 ×5 (R1, R3 ×2, R4 ×3), §20.3
(T2/T3/T4/T5/T14/T21/T22, T24/T25, L44), §20.5 (F36/L25 and L31/L33/L34/L36/
L43/L45/R1), §21.1 (F1/F6/F8/F35/F36/L24/L25/F21/F22/L10/L11/F27/L48/T24/T15/
T25), §21.2's header (F8/F14/F6/F1/F18), §21.6 (F36/L25, F18, F35/F36/L24/L25),
Appendix H (F1/F6, F7, F36/L25, R1).

Every one resolves to a row that says what the citing text claims. The two I
worked hardest:

- §20.5's "one row for each of the other seven spaces §10.2 tabulates (L31, L33,
  L34, L36, L43, L45, R1)". §10.2 tabulates eight spaces; minus record type,
  seven remain: index encoding (L31), linearization (L33), sample type (L34),
  channel layout (L36), codec (L43), filter (L45), metadata encoding (R1). Seven
  rows, seven spaces, correctly matched — and each of those rows does in fact
  register its space's reserved range.
- §5.2's "L18's overlap or L40 through L42's placement". L40 is per-tile
  alignment, L41 run packing, L42 run first-tile alignment — all three are
  placement invariants and all three are verifier rows, which is what §5.2 needs
  ("the rejection is one the walk itself established"). Correct.

I also checked §2.3's `[R-CNF-11]` pointer "(§21.6)" for the
MU = 1-unimplemented-type cannot-establish ground. §21.6's closing paragraph
discusses only the *top-level* case, while `[R-CNF-11]` writes "a record" without
that qualifier. I opened this as a candidate and closed it: `[R-CNF-11]` is about
certification, not refusal, and a sub-record whose type the verifier cannot
implement genuinely leaves a requirement unchecked, so the unqualified form is
correct for its own purpose. §21.9, by contrast, does carry the qualifier ("an
unimplemented top-level MU = 1 type"), matching §21.6. Not a finding.

---

## 6. Limits — §21.9 against every other statement of a limit

**Minimum guarantees.** Eight rows. Cross-checked against: §2.3 `[R-CNF-03]`
("none of whose values exceeds the minimum guarantees of §21's limits table"),
§2.5 `[R-CNF-10]` ("the table is §21.9"), §17.2 `[R-COD-06]` ("§21.9's 8 MiB
`Window_Size` guarantee"), §18.2 (the 16 MiB document row, twice), §21.6's
resource-decline entry, §24 `[R-VEC-03]`, and Appendix B's summary row, which
lists all eight values and matches all eight. No divergence anywhere.

The per-instance paragraph divides the eight into five declaration-ranged rows
and three per-instance rows. Five + three = eight ✔. "The other two range over
the user-metadata documents and compressed frames a file actually contains" — I
checked whether the `Window_Size` row is thereby confined to document frames,
which would leave a tile's zstd frame unbounded; it is not, "compressed frames"
is unqualified and `[R-COD-06]` independently ties tile frames to the same row.

The degenerate case the paragraph turns on: "A layer addressing no tile (§11.2)
therefore has no tile whose decoded size the table bounds." I built the case —
a layer with E₀ = 0, huge Tᵢ, codec 4 — and confirmed it is consistent with
`[R-COD-07]`'s own Note, which says the cap "is quantified over the layer's
*addressed* tiles, so a layer that addresses none ... satisfies it whatever its
tile shape declares", while adding that `[R-ENC-04]`'s ceiling "carries no such
quantifier". The register agrees: L44's condition reads "any of whose addressed
tiles' decoded size exceeds", vacuously false at zero addressed tiles, while L2
lists the decoded-size products unconditionally. The empty-layer case is handled
identically in three places. Suspicion closed.

**Hard limits.** §21.9 disclaims completeness ("a finding aid rather than an
inventory"), so an omission is not a defect; I checked the ten it does state
against their defining sections anyway. Names ≤255 bytes ↔ `[R-ENC-12]` ✔;
user-metadata key ≤255 ↔ §18.2's fourth restriction ✔ (and R10 registers it);
rank ≤255 and C ≤65,535 ↔ §7.4's u8/u16 ✔; codec 4 cap 0x7E000000 with "the
largest channel plane governing in a planar layer" ↔ `[R-COD-07]` word for word
✔; every offset/length/extent/count ≤ 2⁶³ − 1 ↔ `[R-ENC-03]` ✔; A a power of two
512…2⁶² ↔ §16.1 and §7.4 ✔; A_slab a power of two 1…2⁶² ↔ §7.4 (§16.2 gives only
the floor) ✔; S 1…2⁶³ − 1 ↔ §7.4 ✔; directory ≥4 bytes at offset ≥16 ↔ §6.2 ✔;
128-byte file floor ↔ §5.1 ✔. Appendix B restates all of these and matches all
of them. No limit is claimed here that its defining section states differently.

---

## 7. The specialization rule, tested

§21.1 names six specialization relations and says the list is open. I verified
all six and then hunted for one it would break on — specifically for a pair
whose two rows carry *different outcomes*, since §21.1 says only that the
narrower row's "detector and detection point are the ones that apply" and is
silent about the outcome.

Verified: F1's front-block instance ⊂ F6 (a reversed magic is not byte-identical
to the constant, and the constant is not a palindrome — `89 54 41 52 4E 0D 0A 1A`
reversed is `1A 0A 0D 4E 52 41 54 89`); F1's trailer-magic instance ⊂ F8; F35 ⊂
F36; L24 ⊂ L25; F21 ⊂ F22 (a slot of (0,0) has extent_length 0 < 5); L10 ⊂ L11.
In every pair the two rows share an outcome, so the silence costs nothing there.

I then looked for a cross-outcome pair. Candidates tried and rejected: T7 vs T11
(T11 excludes the all-ones value, so they partition rather than nest); F5 vs F10
(F5 with F = 100 does not force F10); F13 vs F17 (a 100-byte file with
committed_file_length 100 exhibits F13 alone); L27 vs L37 (at entry_count = 0
there is no index region for L37 to check, so L27 is the row rather than a
specialization, and both are reject-layer anyway); R1 vs R2 (independent, both
ignore-record). I could not construct a specialization pair spanning two
outcomes, so I am not filing the silence as a defect — but I record that I
looked for one, because that is the shape §21.1's sentence would fail on.

---

## 8. Findings

### register-01 — CONTRADICTION — §21.6, closing paragraph

> "The second is an **experimental-range top-level record type carrying MU = 1**
> (§10.2, §10.3): `[R-CNT-15]` obliges the reader to reject, and `[R-CNF-02]`
> makes the file conforming all the same. ... Neither is a register row: the
> register enumerates file-conformance violations (§21.1), and a file this
> document declines to judge is not one."

The paragraph introduces two structural cases and then gives one reason why
neither is a register row. That reason — "a file this document declines to
judge" — is the *first* case's property. §2.3 `[R-CNF-13]` supplies it: a file
declaring a foreign major "is neither conforming nor nonconforming under it save
as to the conditions that reach it". But the same paragraph says of the second
case, three lines earlier, that "`[R-CNF-02]` makes the file conforming all the
same". A file this document declares conforming is not a file it declines to
judge; it is a file it has judged. The relative clause modifies "a file", so it
is offered as a description of both cases, and it is false of one of them.

The conclusion survives by another route — the register enumerates violations,
the second file carries none, so no row — but the reason the document gives does
not reach the case it is offered for, and a reader who takes it at face value
learns that an experimental-range top-level MU = 1 record leaves the file
unjudged rather than conforming, which is the opposite of what `[R-CNF-02]` and
the preceding sentence say.

Permitted readings: (a) the clause describes only the foreign-major case and the
second case is left without a stated reason; (b) the clause describes both, and
the second case's file is "declined judgement", contradicting the sentence above
it. I take (a) as the intended reading, because (b) contradicts a flat statement
in the same paragraph and two rules outside it. What an implementer does wrong
without the correction: reports "cannot establish" or refuses to characterise
such a file, where §2.3 and §21.6 both require it to be certified conforming
once the verifier's own capability question is separated out.

**Byte-level: no.** Both readings agree that no register row exists and that a
reader rejects the file on capability grounds. The file's conformance is settled
independently by `[R-CNF-02]` and by §2.3's `[R-CNF-03]` clause. Nothing an
implementation emits or accepts moves.

### register-02 — AMBIGUITY — §21.1 first paragraph, against §7.1 `[R-CNT-25]` and §18.2 `[R-MTA-09]`, reaching R4

§21.1:

> "each row is one malformed condition, with the outcome class its scope
> determines (§2.4) — except where a rule assigns one expressly, as
> `[R-CNT-25]`'s quarantine does for every §21.5 row, whatever the containing
> scope"

The quarantine `[R-CNT-25]` states is keyed to unreadability:

> "each way a user-metadata record's document can be unreadable once its framing
> has been read — a failed extent CRC, an unimplemented or invalid encoding, a
> decode failure, or content violating the document's own rules (ill-formed
> UTF-8 included, `[R-ENC-11]`) — is ignore-record with a SHOULD-report"

R4 registers frame constraints that leave the document readable. §18.2 says so
in its own words:

> "several, the content-size field among them, are broken by what the frame
> declares while the bytes decode"

and, of the content-size mismatch specifically, "the bytes decode, and what is
wrong is what the header said about them". A document whose bytes decode is not
one of `[R-CNT-25]`'s four ways of being unreadable, and the governing predicate
of the quarantine — "can be unreadable" — is not met. So §21.1's claim that the
quarantine assigns the outcome "for every §21.5 row" over-reaches at least R4's
content-size and content-checksum-flag instances, and possibly its
bytes-remaining instance.

Permitted readings: (a) `[R-CNT-25]`'s four-item list is illustrative and
"unreadable" is to be read as "not to be served", so the quarantine does reach
R4; (b) the quarantine is bounded by its own predicate, R4's outcome rests
instead on `[R-MTA-09]`'s "Any violation here is ignore-record, never the
tile-scope outcome §17.2 assigns", and §21.1's "as `[R-CNT-25]`'s quarantine
does for every §21.5 row" is simply wrong about one row. I take (b): §18.2
volunteers that the bytes decode, and §21.1's own exception clause is general
("except where a rule assigns one expressly"), with `[R-CNT-25]` given as an
instance of it rather than as the only one, so nothing depends on the
over-reach except the accuracy of the sentence.

What an implementer does wrong without it: nothing to the bytes, but a
conformance-tool author who takes §21.1 literally will look to `[R-CNT-25]` for
R4's authority, fail to find the condition there, and either drop R4 or route
it to the record's containing scope. The document already answers the question
in `[R-MTA-09]` and in §21.5's own header; the defect is that §21.1 points at
the wrong rule for it.

**Byte-level: no.** Under both readings R4's outcome is ignore-record, stated
twice more (the §21.5 header and `[R-MTA-09]`), and the disputed file is
nonconforming under both, so `[R-CNF-05]` bars every conforming writer from
emitting it either way. Reaching the scope-determined default would take
overriding both of those statements as well, which no competent reading does.

### register-03 — AMBIGUITY — §21.2 F33 and §21.3 L18, against §21.1's Instances rule and §21.8

F33's Instances cell: "stored-tile extents; tile-index regions; record extents;
sub-record extents; directory region" (5).
L18's Instances cell: "stored-tile extents; tile-index region; layer sub-record
extents" (3).

Both conditions are relations between **two** claimants — F33: "A byte of the
live committed state is claimed by two structures that do not belong to the same
layer"; L18: "Two structures of one and the same layer claim overlapping bytes".
The cells name one claimant kind per instance. §21.1 says an instance names "a
field the condition ranges over, a container it can occur in, one of several
alternatives the condition text states, or any combination of the three", and
that "One instance is one *distinguishable* file". Neither clause says which of
the two claimants an instance names, and for a symmetric relation the question
is unavoidable: a stored-tile extent overlapping its own layer's tile-index
region is named equally well by L18's first instance and by its second.

This matters because §21.8 and §24 `[R-VEC-03]` promise a vector per instance:
"every register row has at least one vector for each instance it names". A
corpus builder must decide whether L18's three vectors are (tile ∩ tile),
(tile ∩ index), (tile ∩ sub-record) — leaving (index ∩ sub-record) untested — or
some other selection of three from the six unordered pairs the three kinds admit.
Two builders reading this text will build different corpora and both will
satisfy §21.8's letter.

F33 carries a second layer of the same problem: its condition text states three
alternatives explicitly ("across two layers, a layer structure against another
scope's structure, or two structures neither of which belongs to a layer"), and
§21.1 says a cell enumerates "the condition's own alternatives and containers"
and that "a condition applying to two alternatives in two containers has four".
Applied to F33 that arithmetic does not yield 5. I read the three-way clause as
an exhaustive gloss of "do not belong to the same layer" rather than a menu, and
so do not press the count itself; but the pairing question remains open under
either reading.

Permitted readings I can defend: (a) each instance names one *side* of the
relation and the other side is the builder's choice; (b) each instance names the
kind of the claimant that is *out of place*, which is meaningless for an
overlap since neither is; (c) the cells are shorthand for "one vector per kind,
paired however the builder likes". I picked (a) because it is the only one under
which the counts 5 and 3 come out as written and the total 277 reproduces.

What an implementer does wrong without it: nothing to a reader or writer; a
corpus that under-tests one or more overlap pairings, which §21.8 says "is a gap
in the corpus, not a licence to skip the check".

**Byte-level: no.** The rows' conditions, outcomes, detectors and detection
points are all unambiguous; only the corpus construction is under-determined,
and `[R-VEC-01]` already makes the corpus derivative of the specification.

### register-04 — OBSERVATION — §21.5, R10's Governing rule cell

R10: "A user-metadata document key is longer than 255 bytes | top-level
document; layer sub-record document | reader | extent use | `[R-MTA-04]`
(R-ENC-12)".

§21.1 says the parenthetical identifiers "are the further rules the condition
reads". R10's four sibling rows under the same governing rule all read
`[R-CNT-25]` and all cite it: R6 `[R-MTA-04]` (R-CNT-25, R-ENC-12), R7
`[R-MTA-04]` (R-CNT-25), R8 `[R-MTA-04]` (R-CNT-25), R9 `[R-MTA-04]`
(R-CNT-25). R10 does not. The asymmetry is sharpest against R6, which is the
other half of the same folding of §4.6's name rules onto keys — R6 takes
"non-empty" and "free of U+0000–U+001F", R10 takes "at most 255 bytes" — and
which cites both `[R-CNT-25]` and `[R-ENC-12]` where R10 cites only the latter.

R10's outcome is ignore-record and it sits in §21.5, so it does read
`[R-CNT-25]` exactly as R6–R9 do; the citation is simply missing. §21.1 asserts
that `[R-CNT-25]`'s quarantine assigns the outcome "for every §21.5 row", which
makes the omission a self-inconsistency in the table rather than a mere
tidiness point: a tool that harvests governing-rule cells to check §21.1's
claim will find one row that does not cite the rule §21.1 says governs it.

**Byte-level: no.** The outcome is fixed by the subsection header and by
§21.1's own sentence; nothing about any file's treatment changes.

### register-05 — OBSERVATION — §21.1 through §21.6 carry no requirement identifier

§2.2: "Normative requirements carry identifiers of the form
`[R-<PREFIX>-<NN>]`."

§21.1 is normative under `[R-CNF-01]` — it is not §1, carries no *Note*,
*Example* or *Rationale* label, and is not in a non-normative appendix — and it
states requirements that nothing else in the document states:

> "each row *restates* its governing rule, and where a row and the rule it
> cites diverge, **the rule governs**"

together with "Its **completeness is normative**", the specialization rule ("the
file is recorded against the narrower row, whose detector and detection point
are the ones that apply"), the whole Instances arithmetic, and the extension of
the rule-governs tiebreak to §21.6. None of these carries an identifier. The
only identifier §21.1 cites for itself is `[R-ERR-02]`, in the parenthetical
after "§21.2 through §21.5"; but `[R-ERR-02]` is defined in §21.8 and its text
is entirely about conformance-vector coverage ("Every row ... has at least one
conformance vector ... A row without a vector is a gap in the corpus"). It
presupposes the register; it does not establish it, its completeness, or its
tiebreak. The same is true of the header paragraphs of §21.2 (which derives the
`[R-CNF-13]` reach set), §21.3, §21.4, §21.5 (which states the quarantine's
reach over the subsection) and §21.6 (whose closing two paragraphs decide the
status of four distinct cases). The first `ERR` identifier in §21 appears at the
end of §21.7.

The register's *binding force* is not in doubt — `[R-CNF-04]` binds readers to
it and `[R-CNF-07]` assigns the outcomes — so this does not leave any file's
treatment open. What it leaves open is citability: §24 `[R-VEC-02]` requires a
vector to record "the §21 register row it exercises together with that row's
governing requirement identifier", and there is no identifier for the rules that
decide, for instance, which of two overlapping rows a vector is built for.

I note against myself that §2.2's own sentence carries no identifier either, so
the document does not apply the convention to every normative sentence; the
reason I file this anyway is that §21.1's rules are decision procedures other
sections defer to, not descriptions.

**Byte-level: no.** No rule's content changes; only its addressability.

### register-06 — OBSERVATION — §21.2, F5's second instance against `[R-CNT-27]`

F5: "File size is below the 128-byte minimum, so the front block, directory,
pre-trailer pad and trailer cannot all fit | F (physical file size);
committed_file_length | reader | open | `[R-CNT-27]` (R-CNT-01, R-CNT-06)".

`[R-CNT-27]`, in §5.1, is stated over the file's length alone:

> "No conforming file is shorter than 128 bytes: the front signature block, a
> directory of at least 4 bytes at an offset of at least 16, and the 64-byte
> trailer at a 64-aligned offset cannot be satisfied in fewer. A reader MUST
> treat a shorter file as a validity error at file scope."

The second instance names committed_file_length, which `[R-CNT-27]` does not
mention. A file of 192 physical bytes whose trailer declares
committed_file_length = 64 is not "a shorter file" and does not violate
`[R-CNT-27]`; what it violates is `[R-CNT-06]`'s "committed_file_length equals
the file size", which is F17, and `[R-CNT-01]`'s "The file size of a conforming
file equals the live trailer's committed file length F". §21.1 says "where a row
and the rule it cites diverge, **the rule governs**", and the rule the cell
names first is `[R-CNT-27]`.

Two readings. (a) "File size" in F5 means F, and §5.1 defines F as the live
trailer's committed file length, so both instances are readings of the same
quantity and `[R-CNT-27]` reaches both — this requires reading F as the declared
length, which §5.1 and §9.1 support but §19.1 step 1 and §6.4 contradict, both
calling F "the transport-authoritative file size". (b) The two instances are two
different quantities, and only the first is `[R-CNT-27]`'s; the second is a
violation only through the parenthetical rules, which §21.1 characterises as
"the further rules the condition reads" rather than as governing. I take (b),
because the cell would not name two instances if they were the same quantity.

What an implementer does wrong without it: little, since any file exhibiting the
second instance also fails F17 or F13, and both are reject-file at open. A
corpus builder constructing the second instance under `[R-CNT-27]` will produce
a file that exercises F17 as well and must record both, which §24 `[R-VEC-02]`
already provides for ("the entry records every row the file exercises and says
which it was built for").

**Byte-level: no.** Every file exhibiting either instance is reject-file at open
under one row or another; the emittable set and the accept/reject verdict are
the same under both readings.

---

## 9. Suspicions opened and closed

Recorded because a clean lane has to show it looked.

1. **L1 omits alignment A and A_slab from `[R-ENC-03]`'s field list.** Closed by
   L39 and L29, which bound both at 2⁶², and by §21.9's statement that those
   ceilings are "chosen here too rather than consequences of the u64 domain" —
   which is only coherent if A is outside `[R-ENC-03]`. Three passages agree.
2. **F2 names "count" with no file-scope count instance.** Closed: the row
   restates `[R-ENC-03]`'s categories, and naming a category with no instance in
   a given scope is not a divergence about any file.
3. **F19 registers "any bit of the incompat lane" although `[R-CNT-08]` keys the
   outcome to "any set bit it does not implement".** Closed: §10.1's four growth
   vehicles admit only *ignore*-lane bits, so under format major 1 no reader
   implements any incompat bit, and F19's gloss ("this text defines no flag bits,
   so every such bit is unimplemented") is exactly right.
4. **§7.3's Scope column calls the layer record's scope "file", while
   `[R-CNT-13]` says a layer record governs the layer.** Closed by §7.3's own
   parenthetical ("container for layer scope") and by `[R-CNT-13]`'s explicit
   "a malformed slot on a layer record is therefore reject-layer". The register
   follows `[R-CNT-13]` uniformly across L15–L17, L46, L47 and L49.
5. **R8 enumerates "bare token" as one instance where `[R-MTA-04]` names three
   (`NaN`, `Infinity`, `-Infinity`).** Closed by §21.1's "a row whose check
   ranges over a family without the condition changing shape states that range
   as a single instance" — the three tokens fail the same check the same way.
6. **T23 asserts that an LZ4 frame in place of a raw block is caught by T25.**
   Not independently checkable from this document, and the document asserts it;
   I record it as an assertion I could not verify rather than a defect, since
   §21.7's test would in principle decide it.
7. **§2.3 `[R-CNF-11]` cites "(§21.6)" for the MU = 1 cannot-establish ground
   without §21.6's "top-level" qualifier.** Closed: certification and refusal are
   different questions, and §21.9 uses the qualifier where refusal is the
   subject.
8. **An experimental-range sub-record type with MU = 1 has no §21.6 entry.**
   Closed: its defined behaviour is reject-layer, so §21.6's preamble ("A reader
   that treats any of them as a validity failure is the nonconforming party")
   would be false of it; §21.6's closing paragraph states its treatment in prose
   instead, and `[R-CNT-18]` states it normatively.
9. **§21.6's slack entry omits `[R-CNT-21]`'s "not owed at all" case.** Closed:
   in that case §6.2's ordered validation has already rejected the file, so no
   §21.6 condition arises.
10. **Is there a specialization pair spanning two outcomes, which §21.1's
    sentence would not resolve?** Searched (see §7); none found.
11. **`[R-ENC-01]`'s big-endian prohibition is not classified by §21.7.**
    Closed: §21.7 explicitly disclaims being a list ("That is the whole of the
    test, and it decides any condition put to it without appeal to a list"), and
    the endianness bar is the same shape as `[R-ENC-06]`, which §21.7 does work.
12. **§21.7's duality claim.** I checked it formally. Unwitnessed: ∀f exhibiting
    C, ∃g not exhibiting C, no obliged check separates f from g. Detectable: ∃f
    exhibiting C, ∀g not exhibiting C, some obliged check separates them. The
    second is the negation of the first. §21.1's one-sentence restatement of
    detectability matches §21.7's, including the "not necessarily the same check
    for each such file" quantifier order. Sound; not a finding.

## 10. Confidence

High on the counting and on row-versus-rule agreement, which I checked
exhaustively and mechanically. High on the cross-references, which I enumerated
by regex and resolved individually. Medium on completeness in the
"missing row" direction: my sweeps were phrase-based over a normalised copy with
positive controls, and they found every excusal the document itself makes, but a
condition stated without any of the phrases I searched would have escaped them.
Medium on the limits comparison, since two of §21.9's Note's justifications
(the RFC 8878 window recommendation, and what "stock encoder settings" do) rest
on an external document I am not permitted to open.

None of the six findings is byte-level, and I say so on each. The register's
central anti-fork device — "where a row and the rule it cites diverge, the rule
governs" — held everywhere I pushed on it: every divergence I found is a
divergence in the register's *own* prose about itself (§21.1's attribution,
§21.6's reasoning, a missing citation, an under-determined corpus instruction),
not between a row and a rule that could leave two implementations disagreeing
about bytes.
