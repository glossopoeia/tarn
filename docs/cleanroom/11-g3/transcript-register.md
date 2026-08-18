# Round 11 — Register hunter — working transcript

**Charter:** audit §21, the error-handling register, against the rules it restates and
against itself.

**Disclosure.** I read exactly one file: `/Users/robertkleffner/Documents/GitHub/tarn/spec/tarn.md`
(3,953 lines), in full, in four `Read` passes. I ran `wc -l` and `grep` against that same
file only. I ran three local Python computations that read no files: (1) a mechanical
extraction of the §21.2–§21.5 tables from the text I had already read, to count rows and
semicolon-separated instances; (2) a CRC-32C implementation to check the document's three
stated CRC constants and Appendix A's trailer CRC; (3) hand arithmetic on §11.2/§11.4/§14.2/
§14.5/§15.4/§17.3/§21.9 worked examples. I opened no ADR, no `docs/`, no `conformance/`,
no `spec/registry.json`, no `PLAN.md`, `AGENTS.md`, `README.md` or `OPEN-QUESTIONS.md`, no
git history, and did no web access. I did not list any directory. I wrote this one file and
one scratch Python heredoc (not persisted).

---

## 1. How I worked

I read §21 first, then the whole document front to back, then went back through §21 row by
row. §21.1 is the governing text and I held everything else to it, in particular:

> Its **completeness is normative** — a *detectable* file-conformance violation this
> specification names and the register omits is a defect in this document […] — but each row
> *restates* its governing rule, and where a row and the rule it cites diverge, **the rule
> governs**.

and

> Instances within a cell are separated by semicolons, and a cell reading — is one instance;
> the count is therefore mechanical once the cell is written.

That second sentence is what let me mechanise the counting rather than argue it.

I did four sweeps:

- **A. Row → rule.** For each of the 121 rows, locate the cited requirement, read it, and
  compare the row's condition wording, its outcome class, its detector, and its detection
  point against the rule's own text.
- **B. Rule → row.** Sweep the document for every stated MUST-level condition that makes a
  file nonconforming or that a reader/verifier must detect, and look for its row. Then the
  reverse: look for a row registering something the rules do not make a violation.
- **C. Cross-references.** Every citation of a register row or subsection from outside §21.
- **D. Counting, vocabulary, limits.** Recount conditions and instances per subsection; check
  the outcome vocabulary is closed and every value reachable; check §21.9's limits in both
  directions against the sections that define them.

---

## 2. The counting (sweep D, done first because it is falsifiable)

I extracted the four tables mechanically from lines 3081–3236 by splitting on `|`, taking
column 3 (Instances), and applying §21.1's rule verbatim: `—` counts 1, otherwise count the
semicolon-separated fragments. I checked by eye that no Instances cell contains a semicolon
that is not a separator (the parenthetical asides in L2 — `C·N (which dominates the max disk
ordinal (C−1)·N + (N−1))`, `P·Q (which dominates V = P·C)` — and in L23 —
`trailing fixed fields (index_encoding, entry_count, crc_of_crc_array)` — use commas, not
semicolons, inside their parentheses, so the mechanical split is safe).

| Subsection | Rows | Header claims | Instances |
|---|---|---|---|
| §21.2 file scope | 36 (F1–F36) | "36 conditions" ✓ | 53 |
| §21.3 layer scope | 49 (L1–L49) | "49 conditions" ✓ | 106 |
| §21.4 tile scope | 26 (T1–T26) | "26 conditions" ✓ | 45 |
| §21.5 ignored records | 10 (R1–R10) | "10 conditions" ✓ | 44 |
| **total** | **121** | §21.8: "121 conditions over 248 instances" ✓ | **248** |

53 + 106 + 45 + 44 = 248. **Every stated total reproduces exactly.** This is the one number
I was most expecting to find broken and it is not.

I then spot-audited the instance cells against §21.1's two refinements, which are the parts a
mechanical count cannot police:

- *"where a condition is a single predicate over several fields […] the fields it reads are
  not instances, because no two files could differ."* F25 (`MU = 1 with PE = 0, a combination
  no writer emits`) is `—` = 1 instance — correct, that is the "combination of two flag bits"
  example. F28 (`a stored MU **or** PE bit differing`) is 2 — correct, that is a disjunction,
  two distinguishable files. F3 and L2 name *containers* and *products*, never the individual
  addends. All consistent.
- *"a row whose check ranges over a family without the condition changing shape states that
  range as a single instance (T24's any codec)."* F26/L47 give reserved flag bits 2–15 as one
  instance per container, matching. T15 and T25 enumerate, matching.

Instance counts are also internally consistent across the file/layer mirror pairs:
F30 (2) ↔ L15 (2 alternatives × 2 containers = 4); F31 (1) ↔ L16 (2 containers);
F32 (1) ↔ L17 (2); F25 (1) ↔ L46 (2); F26 (1) ↔ L47 (2); F27 (1) ↔ L48 (1);
F28 (2) ↔ L49 (2 × 2 = 4). Every pair scales by the container count and nothing else.

### Detector and detection-point vocabulary

Every `Detector` cell is `reader` or `verifier`. Every `Detected` cell is one of
`open`, `layer access`, `tile use`, `extent use`, `certification` — the exact vocabulary
§21.1 names ("Detection points name §19.2's reader tiers — open, layer access, tile use,
extent use — or *certification* for the rows a verifier detects"). R1 is the only compound
cell (`open (top-level); layer access (sub-record)`) and it uses the same tier names.
No stray value.

### Outcome vocabulary

§2.4 `[R-CNF-07]` closes the reader-outcome vocabulary at four values plus the orthogonal
updater obligation `preserve-verbatim`. §21.2 = reject-file, §21.3 = reject-layer,
§21.4 = reject-tile, §21.5 = ignore-record: all four defined values are reachable and no row
carries a value outside the vocabulary. `preserve-verbatim` is reachable through §20.4's
table (its MU = 1 and MU = 0 / PE = 1 rows), exactly as §2.4 says. Nothing dangling in
either direction.

### CRC and arithmetic checks (local computation, no files read)

I implemented CRC-32C per §4.5 (reflected, poly 0x1EDC6F41 → reversed 0x82F63B78, init and
final XOR 0xFFFFFFFF) and checked the document's own constants:

- `CRC-32C("123456789")` → `0xE3069283` ✓ (§4.5 check vector)
- `CRC-32C(zero bytes)` → `0x00000000` ✓
- CRC-32C over 65,536 sentinel entries (`FF ×16 00 ×4`, 1,310,720 bytes) → `0xEECB3BB2` ✓
  (§15.4 `[R-IDX-05]`, Appendix B)
- Appendix A's trailer bytes [0,60) as tabulated →
  `8a4e5241540d0a1a 0100 0000 00000000 0100000000000000 1000000000000000 0400000000000000
  8000000000000000 efcdab8967452301 00000000` → CRC `0xE00938D2`, stored `D2 38 09 E0` ✓

Worked-example arithmetic I re-derived by hand and confirmed: §11.2 (G = (4,8), N = 32,
P = 65,536); §11.4 ((300,700) → tile (1,2), s = 10, in-tile ordinal 44·256+188 = 11,452,
planar disk ordinal 2·32+10 = 74); §14.2 (Q = 3 → 18 bytes, ordinal 5 at [15,18); Q = 5 → 30
bytes, ordinal 5 at [25,30)); §14.3 (P = 10, `55 01` / `55 FD`); §14.5 (2×2 grid, 16 values,
32 bytes, `CD AB` ×15); §15.4 (entry_count 1,000,000 → 16 segments, last covering 16,960,
region 20,000,064 bytes, entry 999,999 at segment 15 offset 339,180, array at
[20,000,000, 20,000,064), segment at [19,660,800, 20,000,000), full segment 1.25 MiB);
§15.4 second example (entry 74 at [1480,1500), channel-3 entries 96–127); §17.3's shuffle
(`00 00 00 00 00 00 80 00 40 3F 40 40`). All correct.

§21.9's own note arithmetic: at entry_count = 2³² the segment-CRC array is
(2³²/2¹⁶)·4 = 2¹⁸ = 256 KiB ✓, and at 2³⁶ it is 2²⁰·4 = 2²² = 4 MiB ✓; 65,536 layers at the
"small layer records that figure assumed" is 12.5 MiB at 200 bytes/record ✓, under the
16 MiB directory row ✓. §24's remark that a 2³² -tile vector's "index region alone [runs] to
tens of gigabytes" checks: 2³²·20 + 2¹⁶·4 ≈ 80 GiB ✓.

---

## 3. Sweep A — row versus rule, all 121 rows

I will not narrate every row; I will record where I had to work and what I concluded.

### §21.2 (file scope)

Mapped every one of §6.2 `[R-CNT-06]`'s enumerated gates onto a row: magic → F8; trailer CRC
→ F14; version gate → F18 (0 only; an unimplemented major is §21.6's non-violation, correctly
excluded); flag gates → F19; committed_file_length = file size → F17; multiple of 64 → F13;
dir_offset ≥ 16 → F9; dir_length ≥ 4 → F16; dir_offset + dir_length ≤ F − 64 → F10;
1 ≤ generation → F11 and generation ≤ 2⁶³−1 → F2; file_id ≠ 0 → F12; reserved zero → F15.
Complete, one row per gate, no gate registered twice, no row without a gate.

F2's instance list (`dir_offset; dir_length; committed_file_length; generation;
non-layer top-level record extent_offset; extent_length`) correctly *omits* `file_id`:
`[R-ENC-03]` binds "every offset, length, extent, and count", and a file_id is none of the
four. This is the kind of thing that is easy to get wrong and it is right.

F32 versus `[R-CNT-13]`: the rule says "an extent extending past F − 64"; the row says
"extent_offset + extent_length exceeds F - 64, so the extent touches or passes the live
trailer". These agree at the boundary — a sum of exactly F − 64 leaves the extent ending
where the trailer begins, which the row's "exceeds" admits. L17 and T9 and §15.3's row
("offset + length > F − 64") all use the same strict inequality. Consistent everywhere.

F1's relationship to F6/F8 is exactly as §21.1's specialisation clause states: a byte-reversed
front magic is a case of "not byte-identical to the constant" (F6); a byte-reversed trailer
magic is a case of "not exactly the trailer magic" (F8). F1 also correctly carries
`[R-CNT-04]`'s residency condition into the front-block instance and not into the trailer-magic
instance, which `[R-ENC-02]` alone would not have told a reader.

F33 — see finding **register-03** below.

F5 — see finding **register-05** below.

F27/F28 (and L48/L49): I checked the scope assignment hard, because assigning *reject-file*
to an unsorted user-metadata document looks at first like a violation of §21.1's own
"conditions attach to the finest structure they damage". It is not. §18.1 `[R-MTA-02]` puts
the *quarantine* only on failures to **read** the document, and `[R-MTA-05]` is explicit that
"unsorted members do not make a document unreadable […] readers process the document
unchanged". So the quarantine does not reach it, `[R-CNF-08]`'s owning-scope mapping applies,
and a top-level record's owning scope is the file. Correct as registered, and §21.6's closing
note ("Two conditions that once sat in this table are violations and are registered above")
says so in as many words.

### §21.3 (layer scope)

L1's field list is complete for `[R-ENC-03]`'s four categories and correctly excludes the two
alignment fields (A and A_slab are neither offsets, lengths, extents, nor counts, and their
ranges are L39 and L29's business), and includes slab run length S, which `[R-ENC-03]`
expressly names ("entry counts and slab run lengths included").

L2's nine products: I checked each dominance claim. Max planar disk ordinal is
(C−1)·N + (N−1) = C·N − 1, so C·N dominates ✓. V = P·C and Q = ΣBᵢ ≥ C since every element
size ≥ 1, so P·Q ≥ P·C ✓. ⌈P/8⌉ ≤ P ≤ N·P, dominated ✓. The index-region formula is
`[R-CNT-17]`'s ✓.

L3/L5/L6 carry detection point **open** while L4/L7/L8 carry **layer access**. That split is
right and is load-bearing: §19.1 step 4 obliges the open to parse and check "each layer
record's name […] per §4.6" (which is both `[R-ENC-11]` and `[R-ENC-12]`), while §19.3 puts
"dimension- and channel-name rules" at first layer access. The outcome for L3/L5/L6 is still
reject-layer even though detection is at open, which §19.2's closing rule permits explicitly
("Failure at any point takes the violated rule's own outcome and scope").

F4's condition — "both obtainable within their records' inline_length" — is not decoration:
§19.1 step 4 states exactly that a layer record whose name field overruns its inline_length
"contributes no name to the namespace and is instead a validity error at layer scope
(`[R-CNT-18]`)" — i.e. L23's first instance. The row and the rule agree.

L26's governing cell cites `[R-CNT-18]` (§7.3 registry table), and `[R-CNT-18]` does state it:
"A *known* type appearing where §7.3's table does not scope it — a layer record nested as a
sub-record, say — is a validity error at layer scope". §7.3 scopes 0x0002 to both file and
layer, so 0x0001-as-sub-record is the only reachable case, and L26 is the only row needed.
Checked.

L41's "the previous stored tile's offset plus that tile's length" reads ambiguously in
isolation ("that tile" = previous or current?), but `[R-SLB-03]`'s own wording ("each stored
tile's offset equals the previous stored tile's offset plus its length"), the words
"contiguous and packed in ordinal order", and §16.2's worked example (ordinal 10 a sentinel,
"packed with no gap where 10 would have been") make only the previous-tile reading coherent.
I decided it is determined and did not raise it.

L46/L49 and F25/F28 partially overlap: a layer record with MU = 1, PE = 0 exhibits both L46
and L49's `layer record flags bit 1` instance. §21.1's specialisation list does not name this,
but that list is about rows *wholly* contained in others (F1, F35, L24), and L46 covers
sub-records of unregistered types that L49 cannot reach, so it is not a whole-row
specialisation. `[R-VEC-02]`'s "where a condition cannot be isolated […] the entry records
every row the file exercises and says which it was built for" already governs the corpus side.
Not a defect.

### §21.4 (tile scope)

I mapped §15.3's classification table row by row onto §21.4:

| §15.3 row | Register |
|---|---|
| sentinel valid | §21.6 (non-violation) |
| S/S/crc≠0 | T6 |
| exactly one of offset/length = S | T7 (2 instances) |
| length = 0 non-sentinel | T10 |
| offset < 16 non-sentinel | T8 |
| offset or length > 2⁶³−1 non-sentinel | T11 (2) |
| sum overflows, or sum > F−64 | T12 and T9 |
| stored bytes fail crc | T1 |
| intra-layer overlap | L18 (verifier, reject-layer) |
| extra-layer overlap | F33 (verifier, reject-file) |
| alignment or slab invariant | L40, L41, L42 |

Complete in both directions. §15.3's own claim "Six rows are marked *structural*" also
reproduces: rows 2–7 of its table, six of them.

I checked §17.2's codec rules against T14–T25. Each of `[R-COD-06]`'s six named tile-scope
conditions has a row (T17 magic, T18 exactly-one-frame incl. skippable, T19 dictionary ID,
T20 content-checksum flag, T21 window > decoded size, T22 FCS ≠ decoded size). `[R-COD-04]`
→ T14. `[R-COD-05]` → T15/T16. `[R-COD-07]`'s frame-not-block → T23; its layer-scope size cap
→ L44, whose wording ("in a planar layer the largest channel plane governs") is verbatim the
rule's. `[R-COD-08]` → T24/T25 and T3's size rule via `[R-SER-07]`.

T13, T15, T16 and T26 are "cause" rows that say in their own cells which row's check detects
them (T25's, T24's/T25's, T24's, T2's/T4's respectively). I verified each cause really is
always caught by the named check: a raw DEFLATE stream that assumed a preloaded history
window emits back-references before the start of its own output, which RFC 1951 makes an
error (T25); an LZ4 match offset reaching back into a previous tile's output is "match
reaching past produced output", T25's own instance. T13 correctly omits zstd, because a zstd
frame that carries a *disclosed* dictionary is T19 and one that carries an undisclosed one is
in §21.7's undetectable class, which §17.2 states in as many words.

T2's condition partitions `[R-SER-08]` against T4 at the padding boundary ("the same byte at a
padding position is T4's, the two rows together covering `[R-SER-08]`"), which is right: a
0x02 bool byte at a padding position violates both `[R-SER-08]` and `[R-SER-05]`, and
recording it against T4 follows §21.1's specialisation principle.

### §21.5 (ignored records)

`[R-CNT-25]`'s enumeration of "each way a user-metadata record's document can be unreadable"
maps onto: failed extent CRC → R2; invalid/unimplemented encoding → R1 (with the experimental
range correctly excluded to §21.6); decode failure → R3; content violating the document's own
rules → R5–R10; and `[R-MTA-09]`'s encoding-2 frame constraints → R4. R4's 12 instances are
exactly 6 alternatives (magic; skippable frame; second frame; dictionary ID; content-checksum
flag; trailing bytes) × 2 containers, and §18.2 lists exactly those six ("the frame magic; no
skippable frame and no second frame; no nonzero dictionary ID; no content-checksum flag" plus
"occupying the extent's bytes before its terminal CRC").

R5 covers `[R-MTA-04]`'s "well-formed UTF-8 throughout" for the only two places a JSON text can
carry non-ASCII — keys and string values — and R7 catches an ill-formed byte anywhere else as
"not well-formed JSON". R6 and R10 split §4.6's three name rules folded onto keys
(non-empty + C0 in R6, ≤ 255 bytes in R10). R10's terse wording does not say whether the
255 bytes are the source bytes or the decoded string, but §18.2 settles it twice over — "Key
identity is the *decoded* string, not its JSON source bytes" and "`[R-MTA-05]`'s sort order is
likewise over decoded keys' UTF-8 bytes" — and the U+0000–U+001F rule is only checkable on the
decoded string anyway (a `` escape). Determined; not raised.

§21.5's header claim "Every row here is a violation all the same" survives checking:
encoding 0 is invalid by §7.1/§18.2, a reserved-range encoding is prohibited by `[R-EXT-03]`'s
*unqualified* clause ("a value from a reserved range MUST NOT be emitted at all", which unlike
the experimental clause carries no publication qualifier and so is not one of `[R-CNF-02]`'s
conduct rules), and R2–R10 are all failures of stated requirements. The header's *other*
claim, about §21.6, is finding **register-04**.

---

## 4. Sweep B — completeness in both directions

### Rule → row

I grepped every occurrence of "validity error", "reject-file", "reject-layer", "reject-tile",
"ignore-record" and "nonconforming", plus every "Writers MUST" / "MUST NOT emit" / "MUST
equal", and walked them. Everything that names a MUST-level condition with a single-file
witness has a row. The ones deliberately without a row are each accounted for *somewhere*:

- `[R-SLB-04]` (stale slab declaration) — §16.2's note: every file exhibiting it exhibits an
  L41 or L42 failure. Verified: the invariants are re-established or the declaration cleared,
  so a stale declaration necessarily leaves an unpacked run or a misaligned first stored tile.
- `[R-CNT-18]`'s nesting prohibition — §7.4's note: no reader-detectable witness in major 1,
  because the only payload a reader parses as records is the layer record's, and *that* case
  is L26.
- `[R-LIF-04]`'s truncate-or-overwrite — §9.5's note: the observable state is a trailer that
  fails its gates, already F8/F14/F17.
- `[R-CNT-02]`'s "belongs to no class" half — §5.2's note: `[R-LIF-08]` defines every byte the
  walk misses as slack, so the condition describes nothing and "a register row for it would be
  a row no file could exhibit". I agree; only disjointness is testable, and F33/L18 register it.
- `[R-IDX-05]`'s "a partial segment's CRC MUST be computed" — L38 registers it explicitly
  ("the all-sentinel constant 0xEECB3BB2 never substitutes for comparison").
- `[R-COD-06]`'s undisclosed dictionary and `[R-COD-10]`'s harmless mis-stride — §21.7 ¶1.
- `[R-LIF-01]`, `[R-LIF-03]`, `[R-GEO-06]`, `[R-SER-01]`, `[R-CNT-13]`'s no-embedded-offsets
  clause, `[R-ENC-06]` — §21.7 ¶2. Gaps in that paragraph are finding **register-06**.

I also checked the eight numeric identifier spaces of §10.2 against their rows. Every space's
reserved range is a violation and every space's experimental range is a violation *except*
record type and metadata encoding, exactly as `[R-EXT-03]` and `[R-CNF-02]` prescribe:
L31 (index encoding), L33 (linearization), L34 (sample type), L36 (channel layout — no
experimental range, and the row's two instances reflect that), L43 (codec), L45 (filter) all
include their experimental instance; F35/F36/L24/L25 register only the *reserved* range for
record types, with the experimental range sent to §21.6; R1 registers only encoding 0 and
3–0x7F, with ≥ 0x80 sent to §21.6. Six spaces one way, two the other, and the asymmetry is
stated where it is created. This is the tidiest part of the register.

### Row → rule (does any row register a non-violation?)

I checked every row whose outcome is not obviously a violation. F19 (incompat-lane bit set)
survives: `[R-CNF-02]` carves out *only* "§6.3's flags = 0 against a set **ignore-lane** bit",
and §10.1 makes ignore-lane bits the only flag extension vehicle, so a set incompat bit in a
major-1 file is a writer violation with byte consequences. F27/F28/L46/L47/L48/L49 survive via
`[R-CNT-12]`/`[R-CNT-22]`/`[R-MTA-05]`'s explicit "makes the file nonconforming". T2/T4/T5
survive via `[R-SER-08]`/`[R-SER-05]`. T26 survives only in the qualified form the row states,
which matches `[R-COD-10]`. No row registers a non-violation.

---

## 5. Sweep C — every cross-reference to a row or subsection

| Site | Cites | Resolves? |
|---|---|---|
| §9.6 (line 1226) | "§21.2 rows F8 and F17" for `[R-CNT-06]`'s gates on a torn tail | ✓ F8 magic, F17 committed_file_length vs transport size |
| §17.2 note (2169) | "§21.4, T24" for a trailing byte after DEFLATE's final bit | ✓ T24 is exactly trailing bytes |
| §7.4 note (1033) | "§21.3 registers" a layer record appearing as a sub-record | ✓ L26 |
| §9.5 note (1202) | "each of which §21.2 already registers" (magic, CRC, length) | ✓ F8, F14, F17 |
| §16.2 note (2085) | "which §21.3 registers" (unpacked run / misaligned first tile) | ✓ L41, L42 |
| §17.2 note (2232) | "(`[R-GEO-02]`, §21.6)" for a zero-extent layer | ✓ §21.6 row 3 |
| §17.3 (2284) | "undetectable by construction (§21.7)" | ✓ §21.7 ¶1 |
| §18.4 (2478, 2481) | "(§21.6)" for unrecognised / mis-scoped keys | ✓ §21.6 rows 11–12 |
| §2.3 (157–159) | "§21.9's `[R-ERR-04]` […]; §21.6's closing paragraph names the other two" | ✓ the three refusal grounds partition exactly this way |
| §2.3 (193) | "MUST_UNDERSTAND = 1 with a type it does not implement (§21.6)" | ✓ §21.6 closing ¶, second case |
| §21.6 row 5 (3248) | "(F36, L25)" for reserved-range emission | ✓ |
| §21.6 closing (3284–6) | "(F18 […]) […] (F35, F36, L24, L25)" | ✓ |
| Appendix A (3646) | "which §21.6 records as valid" (zero layers) | ✓ §21.6 row 4 |
| Appendix H (3944–5) | "(`[R-CNT-05]`, F7)" and "(`[R-CNT-15]`, F36, L25)" | ✓ |
| Appendix H (3899) | "no violation row of §21.2–§21.5 applies, though §21.6's defined conditions can" | ✓ and it is the correct statement of the point §24 gets wrong |
| F33 (3116) | "F9/F10, F31/F32, L16/L17 and T8/T9, each at its own tier" | ✓ four claimant classes × two bounds, tiers open/open/layer access/tile use |
| §21.1 (3041–2) | "F1 of F6 and of F8, F35 of F36, L24 of L25" | ✓ all three are whole-row containments |
| §24 `[R-VEC-02]` (3580) | "(§21.5, §21.6)" for "a conforming file can carry a record a reader ignores" | ✗ — **register-02** |
| §21.1 (3076) | "(`[R-SER-08]`, `[R-CNT-22]`)" for "obliges the reader to serve the structure unchanged" | ✗ — **register-01** |

Every row label the document uses outside §21 is F7, F8, F17, F18, F35, F36, L24, L25, T24 —
plus F9/F10/F31/F32/L16/L17/T8/T9/T2/T4/T25 used *inside* §21. All nine external ones resolve
to a row that says what the citing text claims. The two failures above are citations to
requirement IDs and to a subsection rather than to a row label.

---

## 6. Sweep D — limits, both directions

`[R-ERR-03]`'s minimum-guarantee table, row by row, against every other statement:

- rank 32, C 4096, entry_count 2³², layers 65,536, dir 16 MiB, tile 256 MiB, metadata doc
  16 MiB, zstd window 8 MiB. Appendix B's "Reader minimum guarantees" row lists the same eight
  values in the same order ✓. §18.2 ("no smaller than §21.9's user-metadata guarantee", note:
  "The 16 MiB figure") ✓. §17.2 ("§21.9's 8 MiB `Window_Size` guarantee") ✓. §1 ("§21.9's
  tile-count guarantee") and Appendix D ("§21.9's entry_count guarantee") ✓. §24 ("the
  tile-count guarantee is not [constructible]") ✓.
- Consistency against the hard limits: C 4096 ≤ 65,535 (u16) ✓; rank 32 ≤ 255 (u8) ✓.
- The 256 MiB tile guarantee and the 8 MiB window guarantee do not conflict: a conforming file
  with a 256 MiB zstd tile necessarily declares a window > 8 MiB (Single_Segment_Flag makes
  Window_Size = FCS = decoded size; without it a Window_Descriptor can still express 8 MiB
  over a 256 MiB content size), so `[R-CNF-03]`'s acceptance duty simply does not run to it —
  "none of whose values exceeds the minimum guarantees" is a conjunction over all listed
  quantities. I worked this one carefully because it looks like a contradiction and is not.

`[R-ERR-05]`'s hard limits, each against its defining section:

| §21.9 says | Defining section says | Agree? |
|---|---|---|
| name ≤ 255 bytes (`[R-ENC-12]`, u8 prefix) | §4.6 "at most 255 bytes of UTF-8 (so every name's length prefix is a single byte)" | ✓ |
| metadata key ≤ 255 bytes, "which carry no such prefix" | §18.2 "every key satisfying §4.6's name rules — non-empty, at most 255 bytes" | ✓ |
| rank ≤ 255, C ≤ 65,535 (u8/u16) | §7.4 field widths; Appendix B same | ✓ |
| codec 4 at decoded tile ≤ 0x7E000000 | §17.2 `[R-COD-07]` same constant; Appendix B same | ✓ |
| every offset/length/extent/count ≤ 2⁶³−1 | §4.2 `[R-ENC-03]` | ✓ |
| A a power of two, 512 ≤ A ≤ 2⁶² | §7.4 and §16.1 both | ✓ |
| A_slab a power of two, 1 ≤ A_slab ≤ 2⁶² | §7.4 explicitly; §16.2 gives only "a power of two ≥ 1" and defers to §7.4 | ✓ (upper bound only in §7.4/Appendix B, but §16.2 cites §7.4) |
| S with 1 ≤ S ≤ 2⁶³−1 | §7.4; §16.2 "S ≥ 1"; Appendix B same | ✓ |
| directory ≥ 4 bytes at offset ≥ 16 | §6.2 gates; §5.1; Appendix B | ✓ |
| no file shorter than 128 bytes | §5.1 `[R-CNT-27]`; Appendix B | ✓ |

Nothing claimed here is stated differently where it is defined. In the other direction, the
only limits stated elsewhere and absent from §21.9 are guidance rather than validity limits —
§6.4's 65,536-byte discovery window (a writer SHOULD, and Appendix B labels it as such) and
§11.3's 1–16 MiB tile working range ("guidance"). §21.9's opening now says outright that the
section "is a finding aid rather than an inventory — each limit is normative where the
structure forcing it is defined", which licenses exactly that. I checked this claim is not
contradicted anywhere: §2.5 `[R-CNF-10]` says every limit "lives in this specification",
never that it lives in §21.9, and points at §21.9 only for the minimum-guarantee table.
Consistent.

One thing I noticed and decided not to raise: there is no limit anywhere on a *stored* tile's
byte length (only on its decoded size), so a conforming file all of whose listed quantities
are within the guarantees can still oblige a reader to fetch an arbitrarily expanded payload.
§17.2's note is explicit that "no bound relates a stored length to its decoded size in either
direction", and `[R-CNT-13]`/T9 bound it by the file's own length, so nothing is
under-specified — it is a stated design consequence, not a gap.

---

## 7. Findings

### register-01 — CONTRADICTION — §21.1 misstates what `[R-SER-08]` obliges a reader to do

**Location:** §21.1 (closing sentence of the Instances paragraph); §14.2 `[R-SER-08]`;
§12.3 `[R-TYP-04]`; Appendix H.

§21.1 says:

> For a row whose Detector is *verifier*, the outcome names the scope at which the damage is
> recorded, not an obligation on any reader: the governing rule states what a reader does, and
> for several such rows it obliges the reader to serve the structure unchanged
> (`[R-SER-08]`, `[R-CNT-22]`).

`[R-CNT-22]` fits: "A reader MUST apply a known type's specified semantics regardless of its
stored MU and PE bits". `[R-SER-08]` does not fit, on either half of the claim.

It does not oblige the reader to *serve*: §14.2 says "A reader is not obligated to screen
decoded content, and a reader that does not detect the violation is not thereby
nonconforming; `[R-CNF-12]` governs a reader that does detect it" — and `[R-CNF-12]` licenses
rejection ("a reader MAY reject it upon detecting any violation, including violations whose
assigned detector is the verifier").

And it does not oblige the reader to serve the structure *unchanged*: §14.2 continues "A
reader that neither detects the violation nor rejects the tile, and returns the value, MUST
report 0x00 as false and every other byte as true." §12.3 calls this out by name — "the one
case where a reader resolves a byte to a value rather than passing it through arises only in a
nonconforming file, and `[R-SER-08]` states it" — and Appendix H repeats it: "returns sample
bit patterns unaltered (§3.2), the sole resolved byte being a nonconforming interleaved
boolean it chooses to return rather than reject".

The rule that *does* read "serve the structure unchanged" is `[R-MTA-05]` — "readers process
the document unchanged" — and it is the one requirement the parenthetical omits, even though
its rows (F27, L48) are verifier rows sitting right beside F28/L49.

Which governs: §21.1's own clause settles it — "where a row and the rule it cites diverge, the
rule governs", and this sentence explicitly subordinates itself ("the governing rule states
what a reader does"). So `[R-SER-08]` governs and §21.1's gloss is the error.

**Byte-level: no.** Two readings would differ on what a reader returns for a 0x02 interleaved
bool byte — 0x02 verbatim versus `true` — and on whether a reader may reject that tile at all.
But §14.2 states both answers in imperative terms, §12.3 and Appendix H restate the second,
`[R-CNF-12]` independently licenses the rejection, and §21.1 defers to the rule by its own
terms. Four passages against one parenthetical gloss; nothing about bytes on disk or an
accept/reject verdict is left open. The byte in question cannot occur in a conforming file at
all.

### register-02 — CONTRADICTION — §24 cites §21.5 for a claim §21.5 denies

**Location:** §24 `[R-VEC-02]`; §21.5's header.

§24 says:

> The two axes are independent: a conforming file can carry a record a reader ignores
> (§21.5, §21.6), and a nonconforming file can still read correctly outside the scope its
> violation damages.

§21.5's header says the opposite of the §21.5 half:

> Every row here is a violation all the same: the outcome bounds a reader's blast radius and
> never makes the file conforming (`[R-CNF-12]`); §21.6 lists the ignore-record conditions
> that are not violations.

Every §21.5 row makes the file nonconforming. The records a *conforming* file can carry and a
reader ignores are §21.6's two: an unassigned experimental-range record type with MU = 0, and
a user-metadata record declaring an experimental-range document encoding. §21.5 contributes
none of them, and it says so while pointing the reader at §21.6.

Appendix H states the correct version of the same point — "no violation row of §21.2–§21.5
applies, though §21.6's defined conditions can — an experimental-range MU = 0 record being
conforming" — which makes §24's parenthetical the outlier rather than a second reading.

The permitted readings are (a) §24's citation is loose and §21.5 supplies only the
*vocabulary* of ignore-record, or (b) §24 means a conforming file can carry a §21.5 condition.
I picked (a), because (b) is refuted three ways: §21.5's own sentence, `[R-CNF-12]`'s "A file
is conforming only if it satisfies every requirement at every scope", and Appendix H. The
concrete harm of (b) is a corpus entry that records `conforming: true` for a file exercising,
say, R9 (duplicate metadata keys), which `[R-VEC-02]` requires the manifest to record — and a
verifier built to that expectation would report *conforming* for a nonconforming file.

**Byte-level: no.** It could fork a verifier's verdict — verifier A reports *nonconforming*
for a file whose user-metadata document has duplicate keys, verifier B reports *conforming* —
but §21.5's header, `[R-CNF-12]`, and Appendix H each decide it independently and in the same
direction, and `[R-VEC-01]` makes the specification govern over any vector built the other way.

### register-03 — AMBIGUITY — F33's condition does not clearly reach an overlap between two non-layer structures, though its Instances cell names one

**Location:** §21.2 row F33; §7.2 `[R-CNT-13]`; §5.2 `[R-CNT-02]`; §9.7 `[R-LIF-08]`.

F33 reads:

> A byte of the live committed state is claimed by two structures that do not belong to the
> same layer — across two layers, or a layer structure against another scope's structure; a
> claimant reaching the front signature block or the live trailer is instead caught by the
> bounds rows F9/F10, F31/F32, L16/L17 and T8/T9, each at its own tier

Its Instances cell is `stored-tile extents; tile-index regions; record extents; sub-record
extents; directory region`.

Overlaps come in four shapes: (a) two structures of one layer → L18; (b) structures of two
different layers → F33's first gloss case; (c) a layer structure against a non-layer structure
→ F33's second gloss case; (d) **two non-layer structures** — a top-level record's extent
overlapping the directory region, or two top-level records' extents overlapping each other.

Shape (d) is constructible and is caught by no other row. Take a directory at [16, 116) and a
top-level record of an experimental type, MU = 0, whose extent slot is (16, 14): extent_offset
≥ 16 so not F31; the sum is far below F − 64 so not F32; nothing lies after the directory's end
so not F7. The two claimants overlap on [16, 30).

The leading clause of F33 — "two structures that do not belong to the same layer" — covers (d)
vacuously (neither belongs to any layer). The em-dash gloss enumerates only (b) and (c), and
the governing rule `[R-CNT-13]` likewise reaches only "any overlap across layers or touching
another scope's structures" — the directory and a top-level record's extent are both file
scope, so "another scope's" does not describe them either.

Readings: (i) F33's leading clause is the condition and the gloss is illustrative, so (d) is
registered — supported by the Instances cell, which names `directory region` as a claimant and
gives it nothing but (d) and (c) to pair with; (ii) the gloss is the condition, so (d) has no
row, which would be a failure of §21.1's normative completeness. I picked (i), because the
Instances cell would otherwise be enumerating a claimant the condition excludes, and because
`[R-CNT-02]` ("No two of them overlap, and a file whose live state does not partition this way
is not a conforming file") plus `[R-LIF-08]` ("It checks that these occupy disjoint byte
ranges") make (d) a violation a verifier must detect, so the register must carry it somewhere.
An implementer who picks (ii) builds a verifier that reports *conforming* for the file above.

**Byte-level: no.** `[R-CNT-02]` is unconditional and `[R-LIF-08]` obliges the verifier to
check disjointness over exactly this claimant set, so both readings converge on
*nonconforming* / reject-file; only the register's bookkeeping differs. What is at stake is
§21.1's completeness claim and F33's instance count, not a verdict.

### register-04 — OBSERVATION — §21.5's pointer to §21.6 is not exhaustive: an over-bound user-metadata document is an ignore-record non-violation with no §21.6 entry

**Location:** §21.5 header; §21.6 table; §18.2 `[R-MTA-09]` and its note.

§21.5 asserts:

> §21.6 lists the ignore-record conditions that are not violations.

§21.6's table carries exactly two ignore-record non-violations: the experimental-range record
type with MU = 0, and the experimental-range document encoding. But §18.2 defines a third:

> a reader instead decodes with a bound of its own choosing, no smaller than §21.9's
> user-metadata guarantee, and a document exceeding that bound is ignore-record like any other
> it cannot read.

and its note confirms the file stays conforming — "A file whose document decodes to more than
the guarantee stays conforming […] A reader that proceeds takes ignore-record for that record".
So this is an ignore-record condition that is not a violation and §21.6 does not list it.

The reading I picked is that §21.5's sentence is a signpost, not a completeness claim about
§21.6 — §21.6's own header claims only "These are defined behaviors, not errors", never that
the table is closed, and §21.1 says the register's completeness clause "[does not reach]
§21.6's defined non-violations", which cuts the other way too: §21.6 carries no stated
completeness obligation. The alternative reading makes §21.5's sentence false. Either way the
outcome for the over-bound document is fixed by `[R-MTA-09]`.

This is decidable from the text but expensive to decide, because settling it means reading the
whole quarantine chain (§7.1, §18.1, §18.2, §21.5, §21.6) to establish that no §21.6 entry
covers it and that §21.6 makes no closure claim of its own.

**Byte-level: no.** `[R-MTA-09]` states the outcome (ignore-record), `[R-ERR-04]` states the
alternative (decline at whole-file, reported as a resource limit), and `[R-CNF-03]`'s
acceptance duty already does not run to a file exceeding a §21.9 guarantee, so the divergence
between two readers here is licensed by design, not opened by this gap.

### register-05 — OBSERVATION — F5's second instance is not a condition `[R-CNT-27]` states

**Location:** §21.2 row F5; §5.1 `[R-CNT-27]`.

F5:

> File size is below the 128-byte minimum, so the front block, directory, pre-trailer pad and
> trailer cannot all fit | F (physical file size); committed_file_length

`[R-CNT-27]`:

> No conforming file is shorter than 128 bytes: the front signature block, a directory of at
> least 4 bytes at an offset of at least 16, and the 64-byte trailer at a 64-aligned offset
> cannot be satisfied in fewer. A reader MUST treat a shorter file as a validity error at file
> scope.

Two things sit oddly. First, the row glosses `F` as "physical file size", while everywhere
else in the document `F` *is* committed_file_length — §5.1 "the live trailer's committed file
length F", §6.2's table "committed_file_length | = F", §15.3 "with F the committed file
length", and F10/F32/L17/T9 all use `F − 64` in that sense. Second, and consequently, the
second instance registers a case `[R-CNT-27]` does not name: a physical file of, say, 200 bytes
whose trailer declares committed_file_length = 64 is not "a shorter file" in the rule's sense,
and what it violates is `[R-CNT-06]`'s size gate (F17) and, since dir_offset + dir_length must
be ≤ F − 64 = 0, also F10.

Permitted readings: (i) `[R-CNT-27]`'s "file" means the committed state, whose length is
committed_file_length, so the instance is in scope; (ii) it means the artifact the reader was
handed, so the instance belongs to F17/F10. I picked (ii), because the rule's own reader clause
("A reader MUST treat a shorter file as a validity error") has to be actionable before the
trailer is read at all — a 40-byte artifact has no trailer to declare anything — and because
§21.1 makes the rule govern over the row. The practical consequence is small: a corpus vector
built for F5's second instance necessarily also exercises F17 and F10, which `[R-VEC-02]`
already contemplates ("the entry records every row the file exercises and says which it was
built for").

**Byte-level: no.** Both readings make the file nonconforming and reject-file, at the open,
by the reader; only which row it is attributed to moves.

### register-06 — OBSERVATION — §21.7's account of undetectable obligations omits the commit protocol and the updater/compactor obligations

**Location:** §21.7 ¶2 `[R-ERR-01]`; §21.1.

§21.1 makes §21.7 the account of what fails the detectability gate: "detectability being the
gate `[R-CNF-07]` already applies and §21.7 the account, by class, of what fails it". §21.7 ¶2
reads:

> A second set of obligations is omitted from the register because a single file exhibits no
> witness of their violation. Committed-prefix immutability and the generation sequence
> (`[R-LIF-01]`, `[R-LIF-03]`) are properties of a file's history, which §9.7 does not
> reconstruct; the ordinal mappings of `[R-GEO-06]` and `[R-SER-01]` are satisfied by a
> structurally valid tile whatever values it carries; `[R-CNT-13]`'s prohibition on an MU = 0
> record encoding file offsets in its own payload is opaque by construction; and
> `[R-ENC-06]`'s fixed field widths are not a state a file can be in […]

Sweeping the document for MUST-level obligations with no single-file witness turns up four
more that the paragraph does not name: `[R-LIF-02]`'s commit protocol (begin at exactly F,
the two barriers, the ordering of steps 2–5, and its "each commit appends its own complete
directory" note, none of which a single file witnesses); `[R-WRT-05]`'s byte-identical
re-emission, which is decidable only against the previous generation; and `[R-WRT-06]`/
`[R-WRT-07]`'s compaction obligations (fresh file_id, generation 1, and "The output's
reference arrays MUST equal the live generation's bit for bit"), which are relations between
two files.

Readings: (i) the paragraph enumerates *classes* by exemplar, so the omitted four fall under
"properties of a file's history" and nothing is missing; (ii) the paragraph enumerates the set
("A second set of obligations"), and the four are missing. I picked (i), because §21.1's
wording is "the account, **by class**" and because the four do reduce to the history class.
But the paragraph's grammar — a semicolon list joined by "and", each item naming its
requirement IDs — reads as an inventory, and a reader auditing §21.1's completeness clause
against the ERR/LIF/WRT requirement set has nothing in the text that tells them which reading
was intended.

**Byte-level: no.** Nothing here bears on any file's bytes or on any verdict: every obligation
named is one this document already says no single file witnesses, so no verifier's report
changes under either reading. It is a completeness question about §21.7's own prose.

---

## 8. What I could not determine

Nothing in my charter was left undetermined by the document. The two places where I had to
work hardest to reach a determination, and where a hurried implementer could plausibly land
elsewhere, are recorded above as register-03 and register-05. The places I suspected a defect
and found none, and which I want on the record so the next round does not re-plough them:

- The 256 MiB tile guarantee versus the 8 MiB zstd `Window_Size` guarantee — not a conflict,
  because `[R-CNF-03]`'s acceptance duty is a conjunction over all listed quantities.
- F27/L48 taking reject-file/reject-layer rather than ignore-record — correct, because the
  quarantine covers *unreadability* only and `[R-MTA-05]` says the document stays readable.
- §21.6's "Two structural cases are conforming files a reader nevertheless refuses" versus
  `[R-ERR-04]`'s resource decline, which looks like a third — not a conflict, because §2.3
  partitions the three grounds explicitly and §21.6's two are the *structural* ones.
- `[R-SLB-03]`'s "the previous stored tile's offset plus that tile's length" — determined by
  "contiguous and packed in ordinal order" and by §16.2's worked example.
- R10's "longer than 255 bytes" for a metadata key — determined to be the decoded string by
  §18.2's two explicit statements about decoded keys.
- The L46/L49 and F25/F28 partial overlaps not appearing in §21.1's specialisation list —
  correct, that list is about whole-row containment and `[R-VEC-02]` handles the rest.

**Finding count in this transcript: 6.**
