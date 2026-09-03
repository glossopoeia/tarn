# Cleanroom round 30 — Adversary transcript

## 0. Access and disclosure

Read: `/Users/robertkleffner/Documents/GitHub/tarn-first-draft/spec/tarn.md`, whole, in
`sed -n` windows of 250–450 lines (two windows overflowed the tool's output cap and were
re-read in smaller windows; I did not open the persisted tool-result files the runtime
wrote for the overflowing windows — those are copies of the same spec text and I re-read
the ranges directly instead). Nothing else in the repository was opened, listed, or
searched. No git commands, no web.

Files I wrote, all under
`/private/tmp/claude-501/-Users-robertkleffner-Documents-GitHub-tarn-first-draft/r30-round/scratch/adversary/`:

- `adv_crc_check.py` — CRC-32C implementation; reproduces the document's check vector,
  the all-sentinel segment constant, the §7.4 example's two CRCs, Appendix A's trailer CRC,
  and re-derives the 81-byte layer-record payload.
- `adv_instances.py` — counts register rows and instances from the four §21 tables.
- `adv_variants.py` — builds the concrete files cited below and computes their trailer CRCs.

Plus this transcript at the named output path. I did not read or list the output directory.

**Unrequested context.** My runtime placed material in context before I began: a project
instruction file pointer (CLAUDE.md → AGENTS.md) and an index of four auto-memory notes
with one-line titles about this project's harness, a gate word list, a preflight check, and
where repair defects "actually live". I did not open any of them and did not act on their
titles. I name their appearance here as the brief asks; nothing in my findings derives from
them. The prompt itself also named the nineteen changed passages; I treated that as
where-to-look only.

## 1. Reading order and method

1. Full linear read, §1 → Appendix H.
2. Re-read of the nineteen named passages with the eleven shapes in hand, and of every
   passage that restates each (register rows, §21.6 entries, Appendix H checklist lines,
   §11.1's Rationale against §20.3, §5.1's Example against §20.3/§20.5).
3. Numeric re-derivation of every figure I could compute (§5 below).
4. Constructive attacks: for each, a concrete file, the reader and verifier verdicts under
   every reading I could defend, and the sentence that closes it (§4 below).
5. Findings (§6).

Search hygiene: the document is hard-wrapped and blockquotes wrap with `> `. I ran every
phrase search twice — line-oriented `grep -c`, and a whitespace-normalised search over the
whole text with `\n> ` folded — and only rested on a zero where a control phrase from the
same passage returned nonzero. Example of why: `cannot establish` returns 6 by line grep and
8 normalised; `another non-layer top-level record` returns 0 normalised because the source
is `another *non-layer* top-level record` (the line grep with the asterisks returns 1).

## 2. Sweeps run (pattern → hits)

Line-oriented (`grep -c`): `neither detects` 1 · `exactly as` 14 · `the same way` 4 ·
`likewise` 5 · `for the same reason` 2 · `cannot establish` 6 · `relocated extent` 1 ·
`every stored tile` 3 · `removing the last` 1 · `another \*non-layer\*` 1 · `independently`
4 · `whole-file re-verification` 3 · `re-verified` 5 · `conduct` 6 · `longer gap` 1 · `no
conforming commit` 1 · `stored in a generation` 1 · `in the generation this commit
supersedes` 3 · `addressed tiles` 10 · `Window_Size` 9 · `Single_Segment` 2 · `first
stored` 4 · `A run with no stored` 1.

Whitespace-normalised (blockquote `> ` folded): `cannot establish` 8 · `neither detects the
violation nor rejects the tile` 1 · `removing the last, re-indexes nothing` 1 · `another
non-layer top-level record` 0 (control with asterisks: 1) · `a commit whose only effect would
be the drop` 1 · `each relocated extent's checksum, including every stored tile's entry crc`
1 · `regenerates each tile-index region any of whose stored extents the output relocates` 1 ·
`re-verified as a whole file` 2 · `whole-file re-verification` 3 · `no conforming commit
produces one` 1 · `Dropping a tile out of the addressed set` 1 · `carries no §14 obligation`
2 · `a filter whose mandated stride makes it the identity` 1 · `n = L/s being 1` 1 · `MUST
refuse to compact when any check` 1 · `preserves no placement` 1 · `it relies structurally on
every structure it copies` 1 · `changes the layer set by adding a layer` 1 · `detects and
does not` 0 (no control needed — the point of that search was that the document has no such
clause; see finding 01) · `the first stored tile's offset satisfies offset mod A_slab` 1.

Analogy census (shape 3): every `exactly as` / `the same way` / `likewise` / `for the same
reason` / `on the same terms` line was listed (26 lines) and the two governing verbs read
side by side. None disagreed; the pairs are recorded in §4 where they mattered.

## 3. Derived numbers, against the document

| Quantity | Derived | Document |
|---|---|---|
| CRC-32C("123456789") | 0xE3069283 | 0xE3069283 (§4.5) |
| CRC-32C(empty) | 0x00000000 | 0x00000000 (§4.5) |
| CRC of 2¹⁶ sentinel entries | 0xEECB3BB2 | 0xEECB3BB2 (§15.4) |
| §7.4 example segment CRC over 80 sentinel bytes | 0x80A34955 | 0x80A34955 |
| §7.4 example crc_of_crc_array | 0xC4EE982E | 0xC4EE982E |
| §7.4 example payload length | 81 (4+34+18+12+13) | 81 |
| §7.4 example extent length | 4·20 + ⌈4/2¹⁶⌉·4 = 84 | 84 |
| Appendix A trailer CRC over [0,60) | 0x402F157E | 0x402F157E |
| Register rows F/L/T/R | 35/49/26/10 = 120 | 35/49/26/10, 120 (§21.8) |
| Register instances (`;`+1 per cell, `—`=1) | 56+116+55+50 = 277 | 277 (§21.8) |
| [R-CNT-06] conditions (rows citing it as governing) | F8 F9 F10 F12 F13 F14 F15 F16 F17 = 9 | "nine" (§2.3) |
| …of which [R-CNT-24]-fixed | F8, F14 = 2; other 7 | "the other seven" (§2.3) |
| §21.2 reaching rows | F8, F14, F6, F1×2 | same (§21.2 preamble) |
| §15.4 example: segments for 10⁶ entries | 16 (15 full, last 16,960) | same |
| §15.4 example: CRC array / region | 64 B / 20,000,064 B | same |
| §15.4 example: entry 999,999 segment-relative byte | 20·16,959 = 339,180 | same |
| §15.4 example: segment 15 range | [19,660,800, 20,000,000) | same |
| §11.4 example: tile of (300,700), s, in-tile ordinal, planar ch.2 | (1,2), 10, 11,452, 74 | same |
| §14.2 example: Q, decoded size, sample bytes | 3, 18, [15,18); planar b 12 B, [10,12); Q=5, 30, [25,30) | same |
| §14.3 example bytes | `55 01` / `55 FD` | same |
| §14.5 example: padding positions, decoded size | 15, 32 | same |
| §20.3 example index region | 32·20+4 = 644 | 644 |
| §9.2 Note: minimum commit growth | prior F + 68 → next multiple of 64 = +128 | +128 |
| §9.3 Note: F ceiling | 2⁶³ − 64 | 2⁶³ − 64 |
| §21.9 Note: CRC array at 2³² / 2³⁶ entries | 256 KiB / 4 MiB | same |
| §21.9 Note: 65,536 layers at ~200 B/record | 12.5 MiB | "roughly 12.5 MiB" |
| [R-CNT-27] floor | dir [16,20), trailer at 64 → 128 | 128 |
| §20.5 [R-WRT-06] "other seven spaces" rows | L31 L33 L34 L36 L43 L45 R1 = 7 of §10.2's 8 spaces | same |
| §15.3 structural rows | 6 | "Six rows" |

Every figure the document states that I could recompute, I recomputed, and every one
matched.

## 4. The attacks

Notation: F = committed file length. Variant files were built by `adv_variants.py`; the
front block is `89 54 41 52 4E 0D 0A 1A` + 8 zero bytes; trailer CRCs below are computed.

### A1. Degenerate minimal files

**(a)** 128 bytes: front [0,16); slack [16,60) zero; directory [60,64) = `00 00 00 00` (zero
records + CRC of nothing); trailer at 64 with dir_offset = 60, dir_length = 4,
committed_file_length = 128, file_id 0x0123456789ABCDEF, trailer CRC `34 A2 CC FA`.
Reader: [R-CNT-06] gates all pass (60 ≥ 16, 4 ≥ 4, 64 ≤ 64). Verifier: coverage walk claims
front, directory, trailer; slack 44. **Conforming under every reading.** Closing text:
`[R-CNT-06]` "dir_offset ≥ 16; dir_length ≥ 4; dir_offset + dir_length ≤ F − 64".

**(b)** 192 bytes: front; directory [16,20); 108 zero bytes; trailer at 128 with
dir_offset 16, dir_length 4, F = 192, trailer CRC `D6 B1 A0 57`. The pre-trailer gap is
108 bytes — longer than step 5's pad (44). Reader: accepts. Verifier: F7 needs "a
structure" in the gap; none → certifies, slack 108. Two verifiers cannot differ: §6.2
`[R-CNT-05]` "a longer gap is conforming, and no conforming commit produces one", and §2.3
`[R-CNF-02]` names this exact case as an actor-binding, non-file rule. The writer that made
it violated `[R-LIF-02]` step 5 while emitting a conforming file; no verdict forks.
**Foreclosed.**

**(c)** Reference single-layer file: index region [16,100) (four sentinels + segment CRC
`55 49 A3 80`), directory [100,209) (24-byte header type 1 flags 3 inline 81 extent (16,84),
the §7.4 payload, CRC), pad 47, trailer at 256, F = 320, trailer CRC `4E 17 0E EA`. Conforming.

**(d)** Same content, index region *after* the directory: directory [16,125), index
[125,209), pad 47, F = 320, trailer CRC `61 B8 C6 20`. Reader: accepts (the dir-bounds rule
holds). Verifier: F7 — "A structure occupies bytes between the live directory's end and the
live trailer" — reject-file. Seam is by design (F7 detector verifier). **Foreclosed** by
`[R-CNT-05]` "A verifier MUST treat a structure in that gap as a validity error at file
scope … (readers check neither, their check being the dir-bounds rule of `[R-CNT-06]`)".

A structure that only *partially* lies in the gap overlaps the directory (F33) or crosses
F − 64 (F10/F32/L17/T9); there is no third case, so "in that gap" needs no boundary rule.

### A2. Overlap taxonomy (verifier-only rows)

Constructions: two layers whose records carry the same extent slot (16, 84) → F33 "across
two layers"; one layer with two non-sentinel entries at the same extent → L18; an entry
whose extent lies inside the directory region → F33 ("a layer structure against another
scope's structure"; directory region is a listed F33 instance); an entry inside the layer's
own index region → L18; a sub-record extent inside another layer's tile → F33; a top-level
user-metadata extent overlapping the directory → F33 ("two structures neither of which
belongs to a layer"). I could not build an overlap the three-way rule of `[R-CNT-13]` does
not classify. Readers accept all of these (crc can be made to match); verifiers reject
them; both verdicts are the document's. **Foreclosed.**

An entry with offset in [16, F−64) pointing at *intact superseded bytes* from an earlier
generation (a previously superseded payload still byte-intact under `[R-LIF-01]`) is a
valid stored tile: it overlaps nothing live and its crc verifies. Reader and verifier both
accept. Not a fork — a curiosity: an appender can "un-supersede" by re-pointing.

### A3. Index-entry boundary values

Non-sentinel entry with offset = 16, length = 1: valid (T8 is `< 16`). Offset + length =
F − 64 exactly: valid by `[R-IDX-03]` (T9 is `> F − 64`) — but then it sits after the
directory or overlaps it, so F7/F33 (verifier). offset = S, length = 5, crc = 0: T7; T11 is
worded "the value being distinct from the all-ones sentinel", so T7 and T11 are disjoint, no
double-recording question. Offset = 2⁶³, length = 1: T11. Offset = 2⁶³ − 1, length = 1: T12
(sum 2⁶³). Length 0: T10. All reader-detected reject-tile; verifier records nonconforming.
crc = 0 on a *stored* tile whose true CRC-32C is 0: valid — the sentinel test needs offset =
length = S. **Foreclosed** by the table of §15.3 read row by row.

### A4. Empty layer under codec 4 and under overflow

Layer d = 1, E = 0, T = 2⁶², one uint8 channel, codec 4: P·B = 2⁶² ≤ 2⁶³ − 1; addressed
tiles 0; `[R-COD-07]`'s cap is quantified over addressed tiles → conforming; L44 restates
the same quantifier ("any of whose addressed tiles"). Same layer with d = 2, T = (2⁶², 2⁶²):
P = 2¹²⁴ → L2 even though the layer is empty — §17.2's Note says exactly this ("P·Q and
P·Bᶜ are checked in an empty layer even though this cap is not"), and §21.9's per-instance
paragraph says the *guarantee* row does not bind an empty layer, which is a different
quantity. No verdict forks. **Foreclosed.**

### A5. Reserved / experimental values in every space and position

Codec 5, filter 3, layout 3, linearization 2, sample type 14, index_encoding 2, each →
reader reject-layer at layer access (L43/L45/L36/L33/L34/L31), verifier nonconforming.
Experimental values (≥ 0x8000 etc.) → same rows, same outcomes. Metadata encoding: 0 and
3–0x7F → R1 (violation, ignore-record); ≥ 0x80 → §21.6 non-violation, ignore-record,
verifier certifies and reports. Record types: reserved with MU = 1 → F35 (reader,
reject-file, strict specialization of F36); reserved with MU = 0 → F36 (verifier);
experimental with MU = 1, PE = 1 → conforming file a reader refuses (§21.6), verifier
*cannot establish* (§2.3 names it); experimental MU = 1 with PE = 0 → F25 (verifier
violation) — so that file is nonconforming, and the reader still rejects it; experimental
MU = 0 with reserved bit 2 set → F26. Same set as sub-records → L24/L25/L46/L47, and the
experimental MU = 1 sub-record is reject-layer with `[R-CNT-18]` forbidding a file
rejection on a conforming file. Every cell decided. **Foreclosed.**

One residue is finding 03 below: the *codec-inability* "cannot establish" ground of §2.3 has
no file that reaches it under this text.

### A6. User-metadata boundary files

**(e)** Top-level record: header type 2, flags PE, inline 1, extent (16, 6); inline byte
`01`; extent = `7B 7D` + CRC; directory [22,51); F = 128. Conforming; smallest file with a
readable document.

**(f)** Extent length 5 (the floor): one document byte `7B` + CRC `67 AC 6C BA`. Under
encoding 1: `{` is not well-formed JSON → R7, a violation → reader ignore-record, verifier
nonconforming. Under encoding 2: no frame magic → R4, violation. Under encoding 0x80: no
document rule attaches (`[R-MTA-10]`) → conforming; verifier certifies and reports scope,
encoding value, stored length. The same five bytes are conforming or not by the encoding
byte alone, and every reading agrees. **Foreclosed.**

Verbatim document of 20 MiB (encoding 1): reader with a 16 MiB bound → ignore-record on
capability; verifier with that bound → *cannot establish*; verifier with a 32 MiB bound →
certifies. Two verifiers differ, but §2.3 and `[R-MTA-09]` make this a declared resource
ground, and *cannot establish* is not a rejection. Not a defect.

10 MiB document under encoding 2 with Single_Segment_Flag: RFC 8878 makes Window_Size the
content size → 10 MiB > 8 MiB row → reader MAY ignore-record; §18.2 says this in terms
("a document larger than that guarantee, framed that way, exceeds a §21.9 row"). Same
document framed with a Window_Descriptor ≤ 8 MiB: within every row. **Foreclosed.**

### A7. Trailer and version-gate boundaries

F = 64 with dir (16, 4): the sum rule fails and F5 fails — both reject-file. Major-2 file
100 bytes long: `[R-CNT-06]`'s order is magic → CRC → version gate, and `[R-CNF-13]` says
F5 does not reach and is "not assessed"; reader refuses on capability, verifier *cannot
establish*. Major-2 file with a byte-reversed front block, resident: F1/F6 reach →
reject-file, verifier *nonconforming* — `[R-CNF-13]` says so explicitly. file_id with bit 63
set: not an offset/length/count, valid. version_minor 0xFFFF: valid (§21.6). Ignore-lane
bit set: conforming; compactor and appender carry it. **Foreclosed.**

### A8. Slabs and alignment with defective entries

S = 4, A_slab = 4096, N = 8. Run 0 entries: ordinal 0 = entry whose stored bytes fail crc
(offset 4096, len 100); ordinal 1 = structural defect (offset S, length 7); ordinal 2 =
stored at 4196; ordinal 3 = sentinel. `[R-SLB-03]`: the crc-failed entry is "not
transparent — its offset and length stand", so it is the run's first stored tile (4096 mod
4096 = 0 ✓) and ordinal 2 must sit at 4096 + 100 = 4196 ✓ — the structural entry is
transparent. L41/L42 both satisfied; T1 and T7 recorded. A run with no stored tiles imposes
nothing. Every combination I built had one classification. **Foreclosed** by the rewritten
§16.2 paragraph, whose three sentences on sentinel / structural / crc-failed entries are
restated word-for-word in L41's condition cell.

### A9. Updater conduct over conforming outputs (the discriminator's live zone)

The brief's discriminating question makes an *actor-permission* ambiguity byte-level when
the disputed output is a conforming file. I therefore spent most of the constructive effort
on §20.3–§20.5, where every rule is a MUST over an operation whose output is conforming
either way.

**A9.1 Supersede every stored tile and re-declare the codec in one commit.** Text: "a commit
does not escape this by unstoring in the same breath: superseding every tile of a layer and
re-declaring it are one operation, and this bars it." Unambiguous, unwitnessed by
construction, remedy stated ("a new layer, or a whole-file rewrite"). A decision, not a
fork. **Foreclosed.**

**A9.2 Remove the last channel of a planar layer whose last channel stores tiles.** Ordinal
bar: "Appending a channel, or removing the last, re-indexes nothing and moves no ordinal at
all" — not barred there. §14 bar: the removed channel's tiles leave the addressed set;
"a tile the new state does not address carries no §14 obligation and its extent becomes
slack" (stated for a shrink, parenthetically tied to a grid-count fall, but the principle is
the tense's own: nothing §14 fixes for an unaddressed tile exists to alter). Permitted. I
could construct the counter-reading only by treating the parenthetical "(§11.2's grid count
falls)" as restrictive, which the sentence's own structure does not support. **Foreclosed**,
with a note that the principle is stated once, at the shrink, and applied here by
inference.

**A9.3 Appender re-emits an *unchanged* index region at a new placement** (e.g. layer B's
region rewritten identically while superseding a tile in layer A). Output conforming.
Text: "A layer whose record alone changes keeps its extent slot, pointing at the existing
region, as does a layer the commit leaves untouched (`[R-WRT-05]`); relocating a live index
region is compaction's operation (§20.5, `[R-WRT-07]`), not an appender's." For an untouched
layer `[R-WRT-05]`'s MUST (byte-identical slot) settles it; for a record that changes for
another reason, the keyword-less clause settles it under the document's own practice
(`[R-CNT-13]`, `[R-SER-01]` carry no keyword and bind). **Foreclosed**, low residual.

**A9.4 Drop a PE = 0 record in a commit whose only other effect is adding a new top-level
record.** This is finding 02. Construction and both readings there.

**A9.5 Shrink turning real positions into padding.** Permitted iff the stored bytes already
hold the fill (writer must inspect stored bytes — a decision the text makes plainly: "the
§14 bar is the whole of the test of what a shrink alters"). Shrink dropping the edge tile
entirely: permitted. Shrink of a non-last dimension renumbering ordinals: permitted, index
re-emitted (index content changes). **Foreclosed.**

**A9.6 Fill change on a channel with stored tiles.** Barred where any stored tile carrying
the channel has a padding position or pad bit (the §14 bar lists "the content `[R-SER-05]`
fixes at both"); permitted otherwise (shape (c)). **Foreclosed.**

**A9.7 Compactor meets a PE = 0 record with a malformed slot (F30).** "MUST refuse to
compact when any check `[R-WRT-09]` obliges fails" — the open is a `[R-WRT-09]` check and
F30 fails it, and F30 is reject-file, under which "A reader MUST NOT rely on any structure
in it". The drop-disposal sentence answers the *second* prohibition (a detected violation
the compactor is not obliged to find, e.g. F26 on a PE = 0 record). Refuse. **Foreclosed.**

**A9.8 Compactor and `[R-WRT-09]`'s "each relocated extent's checksum, including every
stored tile's entry crc".** Whether an extent the compactor places at its input offset is
"relocated" is answered by the preceding clause "it relies structurally on every structure
it copies": every structure in the output was copied, so every stored tile's crc is checked.
**Foreclosed.**

### A10. Reader-side seams on nonconforming tiles

T2/T4 (interleaved bool byte 0x02): reader serves, verifier rejects; by design. The one
open sentence is finding 01 — what a reader that *detects* the byte, elects not to reject,
and serves, must return.

### A11. Recovery-tool candidate selection (§9.6)

Construction: file with a valid generation n at [0, 4096); commit n+1 appends a tile
payload that embeds, at a 64-aligned position, a byte string that is a valid trailer T'
(magic, CRC, committed_file_length = o' + 64) whose dir_offset addresses bytes inside the
same payload that parse as a valid one-layer directory with a verifying CRC, whose layer
record's extent slot addresses an index region (also inside the payload) whose CRC chain
verifies, and whose single non-sentinel entry addresses bytes whose crc does *not* match.
Commit n+1's real trailer is then torn off. A recovery tool probes backward and meets T'
first. "Whole-file re-verification (§8)" of [0, o'+64): a tool that verifies trailer,
directory, and index chains passes T' and settles there; a tool that also decodes/verifies
every stored tile fails it and continues to trailer n. Two tools recover different files.
The text: "recovery output MUST be re-verified as a whole file (§8) before being trusted",
and §21.6: "which catches any mimic that is not itself a consistent generation". "As a whole
file" and "consistent generation" both read most naturally as *every* checksum in §8.1's
map, and §8.2's chain ends at "stored tile". I closed this as a rejected candidate rather than
a finding: the natural reading is full verification, recovery tools are not a conformance
class of §2.3, and the case requires an adversarial payload the document already concedes
is undetectable when made fully consistent. Recorded in `rejected_candidates`.

### A12. Analogy pairs (shape 3), read verb for verb

- §7.3 `[R-CNT-22]` "exactly as they do for `[R-CNT-12]`'s reserved-flag and MU = 1 /
  PE = 0 violations, whose detection this specification likewise assigns to the verifier":
  F25/F26/L46/L47 and F28/L49 all carry detector *verifier* ✓.
- §18.2 "exactly as `[R-COD-06]` has it for a tile (§21.7)" — undisclosed dictionary
  unwitnessed in both ✓; "exactly as `[R-COD-11]` requires of a codec it cannot execute" —
  both MUST NOT certify ✓.
- §18.3 "exactly as they define ignore-lane flag bits (§6.3)" — both conforming, both §21.6
  rows ✓.
- §20.3 "permitted here exactly as it is there" (shrink carve-out) — same carve-out sentence
  in both places ✓.
- §21.9 "exactly as `[R-COD-07]`'s cap is" — both over addressed tiles ✓ (L44 agrees).
- §24 "exactly as §2.2 makes the identifier permanent" — both never reused ✓.
- §16.2 "as it does over a sentinel" / "as it does any other stored tile's" — L41 restates
  both ✓.

### A13. Universals against degenerate members (shape 8)

- "Every tile of a layer has the same logical shape" — P = 1 tile: fine.
- "Decoded output is never empty — §14's decoded sizes are at least 1 byte" — planar bool
  P = 1: ⌈1/8⌉ = 1 ✓; smallest interleaved: 1·1 = 1 ✓.
- "for N ≥ 2¹⁶ they are guaranteed to fall in different segments" — N·20 ≥ 2¹⁶·20 = one
  segment ✓.
- `[R-COD-10]` "L is divisible by s in every case" — checked all three layouts ✓.
- "A run with no stored tiles imposes nothing" — S > N gives one short run; N = 0 gives
  none ✓.
- `[R-SER-05]` "Every pad bit MUST carry the plane's channel's fill bit" — P mod 8 = 0
  gives none ✓ (T5 states the condition).
- §21.9 "A layer addressing no tile therefore has no tile whose decoded size the table
  bounds" — consistent with the guarantee being over instances, and with `[R-ENC-04]` still
  binding P·Q there (§17.2 Note) ✓.

### A14. Closed counts (shape 5)

35/49/26/10 rows; 277 instances; nine `[R-CNT-06]` conditions; seven "other" spaces; six
structural rows; §21.1's six strict-specialization pairs (F1⊂F6, F1⊂F8, F35⊂F36, L24⊂L25,
F21⊂F22, L10⊂L11 — each checked: every file exhibiting the narrower row exhibits the wider,
and the list says it is not closed). §2.3's "the cases this text states" for non-file
writer obligations names two (flags = 0; longer gap). A third express declaration exists —
§9.2 "the file it produces is not nonconforming on that account" for the barriers — but §9.2
files it under the *conduct* category of `[R-CNF-02]`'s first sentence, whose examples are
given with a dash, not a count. Either way the actor is bound and the file conforms;
recorded as a rejected candidate.

## 5. Findings

### adversary-01 — AMBIGUITY — §14.2, `[R-SER-08]` — non-byte-level

Quotation: "A reader is not obligated to screen decoded content, and a reader that does not
detect the violation is not thereby nonconforming; `[R-CNF-12]` governs a reader that does
detect it. A reader that neither detects the violation nor rejects the tile, and returns the
value, MUST report 0x00 as false and every other byte as true."

Construction: interleaved layer, channels `t` (float32) and `m` (bool), tile with byte 0x02
at a real position's `m` slot; every checksum correct. Three readers: R1 does not screen
and serves — bound by the sentence, returns true. R2 screens, detects, and rejects the tile
(`[R-CNF-12]`'s MAY). R3 screens, detects, elects *not* to reject (the MAY is not a MUST),
and serves the value. R3 satisfies neither antecedent: it detected. The document fixes R3's
return nowhere. Reading (i): the MUST is purposive and R3 returns true like R1 — the
Rationale says "leaving the return value undefined bought nothing: two readers handed the
same malformed tile could disagree about a sample and both be conforming, which is the
divergence this document exists to prevent". Reading (ii): the antecedent is exact and R3
is unconstrained. I pick (i) as intended, but the sentence as written admits (ii).

Byte-level: no. The file is nonconforming under both readings; no emission and no
accept/reject verdict moves; only a sample value returned by a reader that has already
established the defect. Cost: exactly the divergence the Rationale names, on the one path
the rule's own antecedent excludes.

### adversary-02 — AMBIGUITY — §20.4, `[R-WRT-08]` table, MU = 0 / PE = 0 row — byte-level, low plausibility

Quotation: "An appender MUST NOT drop it except in a commit that *independently* changes
the scope the record attaches to: for a layer sub-record, that layer's record, the entry set
of its index, or which of its tiles are stored; for a top-level record, the file's layer
set, any layer record's content, or another *non-layer* top-level record. A commit changes
the layer set by adding a layer; an appender never removes one (`[R-CNT-22]`, §7.3)."

Construction: generation 1 holds layer A (untouched throughout) and a top-level record X of
experimental type 0x8001, stored flags MU = 0, PE = 0, extent (o, ℓ). Commit 2 adds a new
top-level user-metadata record M (type 0x0002, extent appended at F₁) and re-emits the
directory. Appender P also drops X; appender Q retains X byte-identically. Both outputs are
conforming files (X is PE = 0; dropping leaves its extent as slack; M is well-formed).
Reading (i): "changes … another non-layer top-level record" means modifying an existing
record; adding M modifies none, the layer set is unchanged, no layer record changed, so the
commit's other effect is not a licensing change and P violated the MUST NOT. Reading (ii):
the principle is "changes the scope the record attaches to" — the file scope — and the
enumerated list is illustrated by "A commit changes the layer set by adding a layer"; adding
a non-layer record is the parallel change to the file's record set, so P is licensed. The
list is introduced by a colon as the content of "such a change", and the drafters wrote
the adding case out for layers and not for non-layer records, which supports (i); the
purpose (an *independent* rewrite of the scope) supports (ii). I pick (i) as the safer
reading for an implementer and cannot exclude (ii) from the text.

Byte-level: yes, by the brief's discriminating question — the disputed file is conforming
and one reading permits a conforming appender to emit it. Two implementations: P emits a
directory without X's 24-byte header (and leaves X's extent as slack); Q emits it with. Both
outputs are conforming files; the dispute is whether P is a conforming updater.
Plausibility that real implementations land on both sides: low — retaining is always
permitted and is the path a cautious appender takes; the fork requires an appender that
wants to drop and reads (ii).

### adversary-03 — OBSERVATION — §2.3 `[R-CNF-11]`, §17.4 `[R-COD-11]`, §21.3 L43/L45 — non-byte-level

Quotation (§2.3): "*cannot establish* — the last where some requirement is one it is unable
to check on a capability or resource ground, as when … when it cannot execute a codec or
filter (`[R-COD-11]`)". Quotation (§17.4): "A verifier that cannot execute a layer's codec
or filter cannot establish that layer's conformance and MUST NOT certify the file. That
inability is not a finding that the file is nonconforming, and it fixes the file's verdict
as *cannot establish* only where the verifier established no violation elsewhere
(`[R-CNF-11]`). For a conforming reader that position arises only at a reserved or
experimental value, every assigned codec and filter being core: it rejects the layer
(`[R-COD-03]`, `[R-COD-09]`)".

Construction: layer with codec = 5, one stored tile. A conforming verifier implements
codecs 1–4 (core, `[R-CNF-03]`), so the only value it "cannot execute" is one L43 registers
as a violation, reader-detected at layer access. The verifier, being a reader, establishes
L43; `[R-CNF-11]`'s priority clause then fixes *nonconforming*. `[R-COD-11]`'s "That
inability is not a finding that the file is nonconforming … fixes the file's verdict as
cannot establish" therefore never governs a conforming verifier under this text: the
ground §2.3 lists is reachable only by software that lacks a core codec, which is not a
conforming verifier. Decidable — the priority clause decides it — but it takes §2.3's
list, §2.3's priority sentence, `[R-COD-11]` and L43 read together, and an implementer who
follows `[R-COD-11]`'s middle sentence literally emits the wrong verdict word. Neither
verdict certifies, so the emittable set and the certify/refuse line do not move.

## 6. Rejected candidates (opened and closed)

- **Longer pre-trailer gap** (A1b): closed by `[R-CNT-05]` "a longer gap is conforming, and
  no conforming commit produces one" and §2.3's naming of the case.
- **Reserved codec value → cannot establish vs nonconforming**: closed as a verdict-word
  question by the priority clause; retained only as observation 03.
- **Remove last planar channel with stored tiles** (A9.2): closed by "a tile the new state
  does not address carries no §14 obligation" and "removing the last, re-indexes nothing".
- **Appender relocating an unchanged index region** (A9.3): closed by "relocating a live
  index region is compaction's operation (§20.5, `[R-WRT-07]`), not an appender's" plus
  `[R-WRT-05]` for untouched layers.
- **Compactor drop vs refuse on a `[R-WRT-09]` failure** (A9.7): closed by "MUST refuse to
  compact when any check `[R-WRT-09]` obliges fails" read with reject-file's "MUST NOT rely
  on any structure in it".
- **"relocated extent" scope in `[R-WRT-09]`** (A9.8): closed by "it relies structurally on
  every structure it copies".
- **Recovery re-verification depth** (A11): closed, with residual, by "re-verified as a whole
  file (§8)" and §21.6's "consistent generation"; recovery tools are outside §2.3's classes.
- **Major-2 file shorter than 128 bytes**: closed by `[R-CNF-13]` "not assessed against a
  file declaring another major" and §2.3's Note on F5.
- **Structural-defect entry whose nominal bytes lie in the pre-trailer gap**: closed by
  `[R-IDX-03]` "contributes … none to `[R-LIF-08]`'s coverage walk, so any bytes it
  nominally addressed … fall to slack" — no structure, no F7.
- **Layer-name overrun detected at open vs L23's "layer access"**: closed — same outcome,
  earlier detection licensed by `[R-RDR-02]` "A reader MAY detect any violation earlier".
- **§2.3's closed count of two non-file writer obligations vs §9.2's barriers**: closed —
  §9.2 files the barriers under the conduct category, whose examples §2.3 gives with a dash;
  the actor is bound and the file conforms under either filing.
- **Single-segment zstd metadata frame > 8 MiB**: closed by §18.2's own sentence naming the
  case and the remedy ("frames it with a Window_Descriptor instead").
- **Empty layer under codec 4 with a huge tile shape**: closed by `[R-COD-07]`'s addressed-
  tile quantifier, restated in L44 and §21.9.
- **Experimental MU = 1 sub-record and `[R-CNF-03]`'s acceptance duty**: closed —
  `[R-CNT-18]` "where the file is otherwise conforming a reader MUST NOT reject the file for
  it" is the specific rule; the acceptance duty's carve-out does not license rejection.
- **T7 vs T11 double-recording**: closed by T11's "the value being distinct from the
  all-ones sentinel".
- **Entry re-pointed at intact superseded bytes**: not a defect; conforming under all
  readings.
- **§11.1 Rationale vs §20.3**: every claim checked against the normative text and found to
  restate it (listed in A9); the Rationale defers ("§20.3 states normatively, and governs").
- **Front-matter Note (label gained)**: its two claims restate `[R-ENC-16]` and §24; nothing
  normative relied on the block.

## 7. Confidence and what would have found more

The nineteen passages were each read at least three times, once for their own sense, once
against every restatement I could find, once with the eleven shapes. Every numeric claim I
could recompute matched. The seam constructions (A1–A8, A10) all resolved to a single verdict
pair. The live zone was updater conduct over conforming outputs (A9), where I found one
genuinely open permission (02) and closed five others on quoted sentences. If a byte-level
fork survives this round, I expect it in that zone or in a two-commit interaction I did not
build (I built one-commit edits only, plus the two-commit "empty then re-declare" escape,
which the text expressly permits). What I did not do: build a multi-segment index (entry_count
> 2¹⁶) with a defect on the segment boundary, or a planar layer with N ≥ 2¹⁶ to exercise the
"different segments" Note against a partial final segment — both are arithmetic the text
states in one place (§15.4) and I re-derived, so I rate them clean with moderate confidence.
