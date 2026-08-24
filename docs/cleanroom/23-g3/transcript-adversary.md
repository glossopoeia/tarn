# Round 23 — Adversary transcript

## 0. Access and disclosure

I read exactly one file: `/Users/robertkleffner/Documents/GitHub/tarn/spec/tarn.md`
(4,426 lines), in seven `sed` slices covering lines 1–4426. I ran no `git`
command, listed no directory, opened no ADR, no `PLAN.md`, no
`OPEN-QUESTIONS.md`, no `conformance/`, no `registry.json`, no web tool.

Material I did not ask for appeared in my context before I began: a project
instruction file pointing at `AGENTS.md`, and an index of the maintainer's
memory notes with six titles. I did not open any of them and I have not used
their contents; I name their appearance here because the brief requires it.
Nothing below is derived from them.

Local computation I ran (reads no spec file beyond the one above): a CRC-32C
implementation in Python, a byte-level TARN writer, an instance-counting script
over the §21 register tables, `zlib` for raw DEFLATE, and the `zstd` CLI on
frames I hand-assembled myself.

## 1. Instrumenting first: does the document's own arithmetic hold?

Before attacking I built the checksum and confirmed it against §4.5's check
vector, because every later byte-level claim rests on it.

> "The CRC-32C of the nine ASCII bytes `"123456789"` ... is `0xE3069283` ...
> The CRC-32C of zero bytes is `0x00000000`."

My implementation (reflected poly 0x82F63B78, init 0xFFFFFFFF, final XOR
0xFFFFFFFF) reproduces both. I then checked every constant the document
derives:

| Claim | Location | Computed | Verdict |
|---|---|---|---|
| trailer CRC of Appendix A's 128-byte file = 0xE00938D2 | Appendix A | 0xe00938d2 | ✓ |
| CRC over 4 sentinel entries (80 bytes) = 0x80A34955 | §7.4 example | 0x80a34955 | ✓ |
| crc_of_crc_array of that = 0xC4EE982E | §7.4 example | 0xc4ee982e | ✓ |
| CRC of a full 2¹⁶-sentinel segment = 0xEECB3BB2 | §15.4, App. B | 0xeecb3bb2 | ✓ |

I also checked the derived arithmetic by hand: §7.4's 81-byte inline payload
(4 + 34 + 18 + 12 + 13 = 81 — I re-derived each term from the field table and
it lands exactly, with no residue, so the sub-record sequence is empty as the
example says); §7.4's extent length 4 × 20 + ⌈4/2¹⁶⌉ × 4 = 84; §15.4's
1,000,000-entry worked example (16 segments, 15 full, last covering
1,000,000 − 983,040 = 16,960; array 64 bytes; region 20,000,064 bytes; entry
999,999 at segment-relative byte 20 × 16,959 = 339,180; segment 15 at
[19,660,800, 20,000,000), i.e. 339,200 bytes); §15.4's planar example
(disk ordinal 2·32 + 10 = 74 → region bytes [1,480, 1,500); channel 3's block
= entries 96–127); §11.2's grid (4, 8) with N = 32, P = 65,536; §11.4's
(300, 700) → tile (1, 2) → s = 10, in-tile (44, 188) → 44·256 + 188 = 11,452;
§14.2's Q = 3 / decoded size 18 / ordinal 5 at bytes [15, 18), and the
float32+bool variant Q = 5 / 30 / [25, 30); §14.3's `55 01` and `55 FD`;
§20.3's 32 · 20 + 4 = 644; §21.9's note (2³²/2¹⁶ × 4 = 256 KiB, 2³⁶ → 4 MiB,
65,536 × 20 = 1.25 MiB per full segment). **Every one holds.** I found no
arithmetic defect anywhere in the document.

## 2. The stated total in §21.8

§21.8 is one of the five changed passages, and it makes a mechanically
checkable claim:

> "Every row of §21.2 through §21.5 — 121 conditions over 277 instances — has
> at least one conformance vector"

§21.1 makes the count mechanical:

> "Instances within a cell are separated by semicolons, and a cell reading —
> is one instance; the count is therefore mechanical once the cell is written."

I extracted every table row matching `^\| [FLTR]\d+ \|` and counted
semicolon-separated instances, treating an em-dash cell as 1.

```
row count 121
total instances 277
per prefix: F=36 rows/58 instances, L=49/116, T=26/55, R=10/48
```

36 + 49 + 26 + 10 = 121 matches §21.2's "36 conditions", §21.3's "49", §21.4's
"26", §21.5's "10". The instance total is 277 exactly. **§21.8's stated total
is correct.** No finding.

I also spot-checked the instance *rules* against three cells the brief's
"quantifier" hint would make me suspicious of. R4's content-size instances are
enumerated in two directions ("declared larger", "declared smaller") — §21.1
requires that, because the constraint is a *does not equal* between two
magnitudes either of which can be the greater. T21's window-size row enumerates
three layout formulas and **no** direction, correctly, because its own text
bounds the comparison in one direction ("larger than"). L28's cell is a single
instance, correctly, because *A_slab ≠ 0* is "a value test and not a comparison
of two quantities at all". The instance arithmetic is being applied
consistently.

## 3. Building the file end to end

I wrote a byte-level writer and built §14.5's worked layer for real: extents
(5, 5), tile extents (4, 4), grid 2 × 2, N = 4, P = 16, interleaved, one uint16
channel with fill `0xABCD`, codec 1, filter 1, tiles 0 and 3 stored, tiles 1
and 2 sentinel. Layout:

```
[0,16)     front signature block
[16,48)    tile ordinal 0 payload      (32 bytes = P·Q = 16·2)
[48,80)    tile ordinal 3 payload      (32 bytes; 1 real position, 15 padding
                                        positions each holding CD AB)
[80,164)   tile-index region           (4 × 20 + ⌈4/2¹⁶⌉ × 4 = 84 bytes)
[164,286)  directory region            (24-byte header + 94-byte inline
                                        payload + 4-byte CRC = 122)
[286,320)  pre-trailer pad             (34 bytes, to the next 64 boundary)
[320,384)  trailer                     F = 384, 384 mod 64 = 0
```

Slack = 384 − 16 − 64 − 122 − 84 − 32 − 32 = 34, which is exactly the
pre-trailer pad — the partition of `[R-CNT-02]` closes. Places I had to make a
call, and what decided each:

- **Layer record flags.** §7.3's table fixes MU = 1, PE = 1 for type 0x0001, so
  the flags word is 0x0003. Decided.
- **Where the index region goes.** `[R-SLB-05]`: "its stored tiles MAY occupy
  any non-overlapping byte positions, in any order". Free — but constrained
  from above by `[R-CNT-05]`, which I discuss in §5 below.
- **Padding content of tile 3.** `[R-SER-05]` fixes it: 15 copies of the fill
  bytes. The document even works this exact tile in §14.5's example.
- **Which byte of the sentinel is which.** `[R-IDX-02]` gives the 20 bytes
  literally (`FF ×16 00 ×4`), so nothing is guessed.
- **`crc_of_crc_array` when there is exactly one segment.** §15.4 says the
  array is the segment CRCs, and §7.4 says crc_of_crc_array is the CRC over
  that array — so it is a CRC over 4 bytes, not over the entries. §7.4's worked
  example confirms this by giving both numbers, and mine reproduce them.

Nothing in the container path required a guess. That is a real result and I
want to record it plainly: I implemented the front block, trailer, directory,
record framing, layer record, tile index, segments, sentinels, fill, padding
and coverage from this document alone, and at no point did I have to invent a
rule.

## 4. Attacks on the container, and what forecloses each

I worked through boundary values and structural collisions. For each, the
sentence that decides it.

**Zero-length and one-past bounds.** A directory of `dir_length = 4` is zero
records plus a CRC (Appendix A). `dir_length = 5` leaves one residue byte →
F29 ("bytes remain after the last complete record"). `dir_offset = 15` → F9.
An extent ending exactly at F − 64 is legal; one byte further → F32/T9/L17
("extent extending past F − 64"). A stored extent at offset 16 is legal;
offset 15 → T8. A non-sentinel entry with `length = 0` → T10, and §17.2's note
supplies the reason the rule is safe ("Decoded output is never empty ... and
none of the codecs above emits zero bytes for a nonempty input"). Foreclosed
throughout.

**The 128-byte floor.** I re-derived it rather than trusting it: dir_offset ≥ 16
and dir_length ≥ 4 force F − 64 ≥ 20, so F ≥ 84; F ≡ 0 (mod 64) forces F ≥ 128.
`[R-CNT-27]` is exactly right.

**The value that overflows the reader's arithmetic.** `[R-ENC-04]` binds "any
quantity this specification defines as a sum or product of integers obtained
from a file", and L2's instance list enumerates nine of them explicitly,
including `C·N (which dominates the max disk ordinal (C−1)·N + (N−1))` and
`P·Q (which dominates V = P·C)`. I checked those two dominance claims by hand:
(C−1)·N + (N−1) = C·N − 1 < C·N ✓, and V = P·C ≤ P·Q since Q = ΣBᵢ ≥ C
(every element size is ≥ 1) ✓. Both hold. The sentinel is carved out of the
domain rule by `[R-IDX-02]` ("`[R-ENC-03]`'s value-domain rule and
`[R-ENC-04]`'s sum rule apply to the fields of non-sentinel entries only"),
and T11's condition text carries the matching qualifier ("the value being
distinct from the all-ones sentinel"), so the two do not collide. Foreclosed.

**Two structures claiming the same bytes.** I tried every pairing I could
construct: two stored tiles of one layer (L18, verifier, reject-layer); a
stored tile against its own layer's index region (L18 — `[R-CNT-13]` names this
case expressly); a stored tile against another layer's anything (F33,
reject-file); a stored tile against the directory (F33, "touching another
scope's structures"); a record extent against the trailer or the front block
(caught earlier and at a different tier by the bounds rows, which F33's own
cell says: "a claimant reaching the front signature block or the live trailer
is instead caught by the bounds rows F9/F10, F31/F32, L16/L17 and T8/T9, each
at its own tier"). The classification is total and the tiering is stated. The
only divergence is reader-vs-verifier, and `[R-CNT-13]` states it outright
("readers are not obligated to detect overlap, which requires whole-directory
knowledge"). Foreclosed.

**A structure that claims bytes outside the file.** F32/T9/L17 all key off
F − 64 rather than F, so nothing can lap the live trailer. §9.7 restates the
same bound for the walk ("each lies within [16, F − 64)"). Consistent.

**The degenerate file.** The smallest conforming file is Appendix A's 128
bytes, and I rebuilt it byte for byte and re-derived its trailer CRC. A
zero-layer file is expressly conforming (§21.6). A zero-extent layer is
expressly conforming (`[R-GEO-02]`). I then pushed on the combination the
document itself flags: a layer with extent 0 declaring **codec 4** with a tile
shape whose decoded size is 2 TiB. §17.2's note answers it directly — the lz4
cap "is quantified over the layer's *addressed* tiles, so a layer that
addresses none ... satisfies it whatever its tile shape declares" — and then
closes the escape I would have tried next: "`[R-ENC-04]`'s overflow rule
carries no such quantifier — it binds any sum or product a file yields — so
P·Q and P·Bᶜ are checked in an empty layer even though this cap is not."
That is precisely the quantifier trap the brief warned me to look for, and it
is already shut, in writing, with the asymmetry called out. Foreclosed.

**A slab or alignment declaration on a layer that addresses nothing.**
`[R-SLB-02]`'s blocks are [0, N) interleaved and [c·N, (c+1)·N) planar; at
N = 0 every block is empty, so no run exists and nothing is checkable. No rule
is left dangling. Foreclosed.

**Slab run continuity across a damaged entry.** This looked like the best
quantifier target in §16 and it is fully closed. `[R-SLB-03]` distinguishes two
kinds of bad entry: entries `[R-IDX-03]` classifies reject-tile on a
*structural* ground "are transparent, and the run's stored tiles close over
them", while "An entry whose only defect is that its stored bytes fail its crc
is not transparent — its offset and length stand". I checked the consequence:
that split is exactly what keeps L41 decidable without reading payloads, and
§16.2 says so ("this invariant stays decidable from the index entries alone,
given the committed file length §15.3 already requires to classify any entry").
L41's own cell repeats both halves. Foreclosed, and tightly.

**A structure after the directory.** `[R-CNT-05]` bars it (F7, verifier,
reject-file) while readers check only `[R-CNT-06]`'s dir bounds — so a reader
accepts a file a verifier rejects. That is a stated reader/verifier seam, not a
fork: the text assigns the detector. I checked whether the commit protocol can
even produce one: `[R-LIF-02]` appends step 2's structures, then step 3's
directory, then step 5's trailer, and every prior generation's structures lie
before that generation's directory, hence before F, hence before the new
directory. So `[R-CNT-05]` is automatically satisfied by any conforming commit.
Consistent.

**The pre-trailer gap.** I tried to make the "conforming file / nonconforming
writer" seam bite: a 1,000-byte pre-trailer pad. §6.2 concedes it ("a longer
gap is conforming, and no conforming commit produces one") and `[R-CNF-02]`
names it as one of exactly two declared conduct-not-bytes cases. Both verifiers
certify. Foreclosed.

## 5. Attacks on the reader/verifier seam

I hunted specifically for a file where two **verifiers** part company, since
reader divergence is licensed wholesale by `[R-CNF-12]` on any nonconforming
file.

**Residency of the front block.** `[R-CNT-04]` lets a non-resident reader
"defer or omit the check", so two readers differ on a file with a bad front
block. But §2.3 gives verifiers no such exemption and Appendix H spells it out
("the 16-byte front signature block by byte equality, which `[R-CNT-04]` lets a
reader not holding it resident defer or omit and §2.3 does not (F1, F6)"), and
F6's own condition cell repeats it. Verifiers agree. Foreclosed.

**Registered-flag mismatch, reserved flag bits, unsorted metadata members.**
All three are reader-invisible and verifier-detected (F27/F28, F26, L47/L48/L49),
and §21.1 explains why the outcome column does not oblige the reader
("for several such rows it obliges the reader to serve the structure
unchanged"). Verifiers agree. Foreclosed.

**Conforming files a reader refuses.** §21.6's closing paragraph enumerates two
and insists on the qualifier: "the same type as a layer sub-record is
reject-layer and never a ground to refuse the file (`[R-CNT-18]`), so only the
top-level case is a file a reader refuses". I then tried the mismatch I thought
I had found: §2.3's acceptance duty is carved out for a file "carrying no
record of a type it does not implement with MUST_UNDERSTAND = 1", unqualified
as to scope, while §7.4 makes sub-records records ("Sub-records are layer-scope
records"). So on a conforming file whose *sub-record* is an experimental MU = 1
type, §2.3's duty appears carved away and a reader could claim licence to
refuse the file. It is foreclosed by `[R-CNT-18]`, in capitals: "an unknown
sub-record type with MU = 1 is reject-layer, and where the file is otherwise
conforming a reader MUST NOT reject the file for it". Absence of a duty to
accept is not permission to reject against an explicit MUST NOT, and §2.3's own
parenthesis routes the reader to §21.6, which restricts the case to top-level.
Loose phrasing, no consequence. Not reported as a finding.

**Verifier decline grounds.** §2.3 lists them and §21.5's preamble extends the
metadata one to two bounds ("declines the decode on the size bound **or on the
frame's declared window**"). Every one of them produces *cannot establish*,
which §2.3 separates sharply from *nonconforming* ("*Cannot establish* is not a
finding that the file is nonconforming"). So the designed divergences are
certify-vs-cannot-establish, and the document says so. That is where I stopped
finding easy targets and started reading §18.2 as a passage.

## 6. §18.2 read as one passage

The brief told me to read this as a whole rather than as a sequence of rules,
so I laid the tile rule and the document rule side by side, verb by verb, as
the "argument by analogy" hint asks.

`[R-COD-06]`, for a tile:

> "The frame content-size field MAY be present; when present it MUST equal the
> tile's decoded size, a reader MUST treat a mismatch as a validity error at
> tile scope, and a reader MUST NOT allocate or size any buffer from it"

§18.2, for a document:

> "The frame's content-size field, unlike the decoded size and the window, is
> *not* left to the reader: it MAY be present, and when present it MUST equal
> the byte length of the decoded document."

The transposition §18.2 announces is exact on the writer side and drops the
reader-side clause. §2.1's Note states the document's own phrasing discipline —
"every writer-side prohibition is paired with an explicit reader-side clause
stating what a reader does with a violating file" — and here the pairing is
supplied instead by R4's Detector cell plus `[R-CNF-04]`. That is derivable,
but it is the only frame constraint in the section whose reader clause lives
only in the register.

I checked the carry-over list for completeness rather than trusting "named for
convenience, not as a closed list". `[R-COD-06]` states: frame magic; no
skippable frame; no more than one frame; no dictionary use; no nonzero
dictionary ID; no content-checksum flag; window ≤ the tile's decoded size;
content-size = the tile's decoded size; no buffer sized from the content-size
field; and a SHOULD on the 8 MiB window. §18.2 excepts "what it states against
a tile's declared decoded size, and what it states about the frame's declared
`Window_Size`", which is two *topics* covering three clauses (the window cap,
the content-size equality, and the window SHOULD), and it replaces both topics.
Everything else is carried, and R4's sixteen instances cover the carried
constraints that have a witness, with the two witness-less ones named and
excluded in the text. **The carry-over is complete.** I could not break it.

Where it does break down is the interaction between the content-size field and
the reader's own bound. §18.2 says:

> "Under either encoding a reader decodes with a bound of its own choosing, no
> smaller than §21.9's user-metadata guarantee, and a document exceeding that
> bound is ignore-record like any other it cannot read; §21.9's row is stated
> over a document's decoded size, which a verbatim document has as surely as a
> compressed one."

and R4 says:

> "unlike R3, a constraint of this row is broken by what the frame declares
> rather than by whether the bytes decode, so a reader that only tries decoding
> establishes none of them"

I built the bytes. A hand-assembled RFC 8878 frame carrying the 18-byte
document `{"tarn.title":"x"}`:

```
honest: 28b52ffd c0 00 1200000000000000 910000 7b227461726e2e7469746c65223a2278227d
liar:   28b52ffd c0 00 0000002000000000 910000 7b227461726e2e7469746c65223a2278227d
         magic  FHD WD  Frame_Content_Size  blk hdr   raw block: the document
```

`FHD = 0xC0` sets FCS_Field_Size = 3 (8-byte content size), Single_Segment = 0,
no checksum, no dictionary; `WD = 0x00` gives Window_Size = 1 KiB, comfortably
inside §21.9's 8 MiB row, so no window decline is available; the block header
`910000` is one final raw block of 18 bytes. The two frames differ only in the
declared content size: 18 versus 512 MiB. Both are 35 bytes.

Reference decoder behavior:

```
$ zstd -d -c honest.zst   →  {"tarn.title":"x"}
$ zstd -d -c liar.zst     →  liar.zst : Decoding error (36) : Data corruption detected
$ zstd -l liar.zst        →  Compressed 35 B   Uncompressed 512 MiB
```

Three things follow. First, R4's premise that "the bytes decode" is false for
the reference implementation: a streaming decoder *fails*, so the condition
presents as R3, not R4, contradicting §18.2's express routing ("A mismatch is
one of the frame constraints R4 registers, **not** a failure to decode under
R3: the bytes decode"). Second, the declared value is readable from the header
alone, which is what the routing wanted. Third — and this is the part that
matters — a reader using a one-shot decompress call with a destination sized to
its own 16 MiB bound never reaches the bytes at all: the declared 512 MiB is
what the API rejects, and the reader has to decide whether that counts as "a
document exceeding that bound". §18.2 pins the reader's bound to the *decoded*
size and bars sizing "any buffer from a length the frame itself declares", but
it never says the declared length may not be *consulted* in deciding whether to
attempt the decode, and §21.9's row is stated over "a document's decoded size"
— which the frame purports to state. I develop this as finding **adversary-01**.

I also checked the Single_Segment interaction, since §18.2 handles it
explicitly and it is the one place two of its quantities coincide:

> "Where the frame sets Single_Segment_Flag there is no Window_Descriptor and
> RFC 8878 makes the frame's `Window_Size` its content-size field, which this
> section pins below to the decoded document's byte length: a document larger
> than that guarantee, framed that way, exceeds a §21.9 row"

I traced it: under Single_Segment, RFC 8878 requires the content-size field to
be present, §18.2 pins it to the decoded length, and Window_Size then equals
that length — so a 12 MiB document framed single-segment declares a 12 MiB
window, exceeding the 8 MiB Window_Size row while sitting inside the 16 MiB
document row. §18.2 anticipates exactly this and says so ("§21.9's
user-metadata row bounds a document's decoded size; it does not relieve the
frame carrying it of the `Window_Size` row"), and tells the writer what to do
("a writer that needs one frames it with a Window_Descriptor instead").
Foreclosed. This is the "one quantity named where two are in play" shape and
the passage handles it.

## 7. The document rules themselves

Having failed to break the frame, I turned to what §18.2 says the decoded bytes
must be:

> "The decoded document is a JSON text as defined by RFC 8259, encoded in
> UTF-8. Four restrictions apply"

The four restrictions pin the top-level type, the BOM, number finiteness,
duplicate keys (over decoded strings), and UTF-8 including escape resolution,
and they fold §4.6's name rules onto keys. §21.9 then names the 255-byte key
cap as one of only two hard limits "chosen here" rather than forced. That is a
careful, closed list — and the care is what made the omission visible.

RFC 8259 §9 expressly licenses an implementation to limit nesting depth. TARN
imports RFC 8259 as the definition of the document and states no depth bound
anywhere: not in §18.2's four restrictions, not in §21.9's guarantee table, not
in §21.9's hard-limit list. Meanwhile `[R-CNF-10]` promises the opposite:

> "Every limit that affects which files are valid or which files a conforming
> reader accepts lives in this specification, never only in an implementation."

and `[R-ERR-03]` repeats it for §21.9. A conforming document nested 200,000
deep — about 1.2 MB, well inside every §21.9 row — must therefore be parsed by
every conforming reader and verifier, and a recursive-descent parser (the
ordinary implementation, and the one RFC 8259 §9 has in mind) cannot. I checked
what outcomes are available to it and found none: `[R-CNT-25]`'s quarantine
enumerates four ways a document "can be unreadable" — "a failed extent CRC, an
unimplemented or invalid encoding, a decode failure, or content violating the
document's own rules" — and depth is none of them; the decode succeeded, the
encoding is assigned, the CRC is fine, and the document satisfies all four of
§18.2's restrictions. §18.2's own decline route is the *size* bound and nothing
else. And `[R-CNF-04]` closes the improvisation: "A reader MUST NOT
heuristically repair a violating structure or infer values this specification
does not define." This is finding **adversary-02**, and it is the one I think
forks a verdict.

I checked the neighbouring RFC 8259 freedoms to see whether the omission is
isolated. Number precision: pinned (`[R-MTA-04]`'s binary64 rule). Duplicate
keys: pinned, including the source-bytes-versus-decoded-string question. BOM:
pinned. Member order: pinned, and §21.1 and F27/L48 route the violation to the
verifier. Whitespace: left free, and Appendix G item 9 acknowledges it by
pinning the JSON writer. Depth is the only one left open, which is why I read
it as an omission rather than a deliberate silence.

## 8. §21.7, read against constructible files

§21.7 is an account of what has no witness, so a claim that a witness *exists*
is the way it can be wrong. The sentence:

> "a change that reaches the codec is witnessed by the rows for the codec now
> declared, which test the stored bytes as a stream of it (T15, T17, T23, T25),
> or by T14 where the new declaration is codec 1"

T14 fires only when "a non-sentinel index entry's length differs from the
tile's decoded size". So the T14 clause holds only where the old codec's
compressed length differs from the decoded size — and a writer can arrange
equality. I checked constructibility with real DEFLATE: for incompressible
input, raw deflate is D + 5·⌈D/65535⌉ bytes; for compressible input it is
below D; so a tile can be tuned to land exactly on D by adjusting how much
redundancy it carries. Re-declare that layer codec 2 → codec 1 and T14 is
silent, the stored bytes are read as a raw filtered image, and the samples are
wrong. Symmetrically, the "rows for the codec now declared" clause fails
whenever the old stored bytes are themselves a valid stream of the new codec —
constructible for codec 1 → codec 3, since under codec 1 the stored bytes are
the tile image and the tile image is arbitrary sample content, so a writer can
simply make the image a valid zstd frame. In both cases the violation is
genuinely undetectable, so the register is still right to omit it; what is
wrong is §21.7 asserting a witness. Finding **adversary-03**.

I did check the other clauses of the same paragraph and they hold. The
`[R-ENC-06]` clause ("not a state a file can be in") is right — a structure
written at a different width simply yields different values at the fixed
widths. The `[R-CNT-18]` nesting clause is right and §7.4's closing Note
supplies the proof (a user-metadata payload is one byte, an unknown type's
payload is opaque, so the layer record is the only payload anyone parses as
records, and its appearance as a sub-record is L26). The `[R-SER-05]`/
`[R-SER-08]` clause is right, and I verified the covering claim in T2's cell —
"the same byte at a padding position is T4's, the two rows together covering
`[R-SER-08]`" — by checking that `[R-TYP-07]` confines a bool fill to 0x00 or
0x01, so *any* padding byte outside {0x00, 0x01} necessarily differs from the
recorded fill and fires T4. The two rows do cover the rule.

## 9. §21.9's guarantees, and what they do not bound

The new paragraph individuates the rows correctly as far as it goes. I checked
the analogy it draws:

> "*Decoded size of one tile* ranges over a layer's **addressed** tiles, stored
> or not, exactly as `[R-COD-07]`'s cap is"

against `[R-COD-07]`'s own words ("for a layer any of whose addressed tiles'
decoded size exceeds 0x7E000000 bytes ... in a planar layer each channel's
plane carries its own decoded size ... and the largest governs"). Both range
over addressed tiles; in a planar layer §3.1 makes each channel-plane a tile in
its own right, so "each addressed tile has one decoded size" and "the largest
governs" agree. L44's three instances match the three formulas. The analogy is
sound — this one survives the side-by-side test.

What I could not resolve is what the table bounds *collectively*. The rows are
per-quantity minimums and compose multiplicatively: 65,536 layers × 2³²
addressed tiles per layer is inside every row and is 2.8 × 10¹⁴ index entries.
§9.7 obliges a verifier to walk all of them —

> "From the live trailer it reads the live directory and, through its records
> and their sub-records, reaches the claimants `[R-CNT-02]` names: the directory
> itself, each record's extent, and the stored extent of each non-sentinel
> tile-index entry ... It checks that these occupy disjoint byte ranges"

— and `[R-ERR-04]` forbids declining a within-table file on resource grounds
("Software that declines **on that ground** a file whose every quantity lies
within the table is not a conforming reader"). §21.9's note justifies the 2³²
row by a *reader's* per-tile working set ("the segment-CRC array a reader
fetches whole before using any entry (§15.4) is still 256 KiB"), which says
nothing about the verifier's whole-file disjointness check that §2.3 and §9.7
make it owe. Nothing bounds a stored tile's *stored* length either — §17.2's
note is explicit that "no bound relates a stored length to its decoded size in
either direction" — so a conforming tile inside the 256 MiB decoded row can
carry a multi-gigabyte stored extent that a reader must fetch and CRC. This is
decidable but disproportionately expensive: finding **adversary-04**.

## 10. Attacks that produced nothing, listed for the record

- Byte-reversed signatures (F1), version_major = 0 (F18), incompat lane bits
  (F19): all registered, all with the ordering §21.2's preamble justifies
  ("§6.2 puts the version gate ahead of every check but the trailer magic and
  the trailer CRC"). The four exceptions it names are exactly the four fields
  `[R-CNT-24]` freezes across majors. Consistent.
- Trailing residue past a completed commit: §9.5's Note declines to give it a
  row and explains why ("A reader meets it as a trailer that fails its gates").
  F17 has both directions as instances.
- A payload mimicking a trailer: §21.6 records it as inert, §9.6 requires
  whole-file re-verification, §22.3 states the residue.
- Every combination of MU/PE on every record type in every position: F25, F26,
  F28, F35, F36, L24, L25, L26, L46, L47, L49, plus §21.6's non-violation rows.
  I could not find a combination without a home.
- Reserved and experimental values in all eight identifier spaces: §10.2's
  table, and L31/L33/L34/L36/L43/L45/R1 plus §21.6's experimental-encoding row.
  Complete.
- Codec 1 with a filter (length unchanged by `[R-COD-10]`, so `[R-COD-04]`'s
  equality survives); byte-shuffle stride on every layout (L divisible by s in
  every case, which I verified for all three formulas); packed bool planes with
  P mod 8 ≠ 0 (T5 and §14.3's worked `55 FD`).
- DEFLATE trailing bytes: I confirmed empirically with `zlib` that a raw
  stream plus one byte leaves `unused_data` non-empty and `eof` true, so T24 is
  detectable exactly as `[R-COD-05]`'s Note claims, and the unconstrained final
  *bits* are genuinely invisible to it.
- Point versus region requests at the same coordinate outside the extents:
  §19.4 step 1 distinguishes them deliberately, and §21.6 records both.

## 11. Findings

### adversary-01 — AMBIGUITY
**§18.2, `[R-MTA-09]`; §21.5, R4; §2.1's phrasing Note**

Quotation:

> "The frame's content-size field, unlike the decoded size and the window, is
> *not* left to the reader: it MAY be present, and when present it MUST equal
> the byte length of the decoded document. A mismatch is one of the frame
> constraints R4 registers, not a failure to decode under R3: the bytes decode,
> and what is wrong is what the header said about them."

Two readings are defensible for a frame declaring a content size far above the
reader's decode bound while decoding to a small document.

*Reading A (the one I picked).* The reader's bound is on the **actual** decoded
size only. The carried-over "bar on sizing any buffer from a length the frame
itself declares" and "unlike the decoded size and the window, [it] is *not*
left to the reader" together forbid treating the declared value as the
document's size, so the reader must attempt a bounded streaming decode, obtain
18 bytes, compare against the declared 512 MiB, and record R4 — a violation,
verdict *nonconforming*.

*Reading B.* §18.2 pins the bound to "a document's decoded size" and adds that
"§21.9's row is stated over a document's decoded size" — which a frame with a
Frame_Content_Size field purports to state. Nothing in the section bars
*consulting* the declared length in deciding whether to attempt the decode;
what is barred is sizing a buffer from it. A reader using a one-shot
`ZSTD_decompress` against a destination sized from its own 16 MiB bound gets
`dstSize_tooSmall` and never sees a byte of output. Under §18.2 that is a
decline "on the bound above": ignore-record for a reader, and for a verifier
"cannot establish that document's conformance and MUST NOT certify the file" —
with §2.3 additionally forbidding it to "report it as one [nonconforming]".

*Reading C, which the text asserts is impossible.* The reference zstd decoder
reports "Data corruption detected" on my `liar.zst`, so for a streaming
implementation the condition is a decode failure and lands in R3, directly
against §18.2's "the bytes decode" and against R4's "a reader that only tries
decoding establishes none of them". R3 and R4 carry the same detector, tier and
outcome, so this reading costs a reader nothing — but it falsifies the stated
rationale for the routing, and a corpus vector built for R4's content-size
instances will be answered with R3 by any streaming implementation.

An implementer who lands on Reading B ships a verifier that is normatively
forbidden to report the violation that Reading A's verifier is normatively
obliged to report, on the same 35 bytes. What fixes it is one sentence saying
whether the frame's declared content size may be consulted before the decode is
attempted, and an explicit reader-side clause for the content-size constraint —
the clause `[R-COD-06]` has for a tile and §2.1's phrasing Note promises for
every writer-side prohibition.

**Byte-level: no.** Every reading routes a reader to ignore-record, so the
document returned and the file's acceptance are identical; no verifier
certifies under any reading. The divergence is between *nonconforming* and
*cannot establish*, which the emittable and acceptable sets do not see.

### adversary-02 — AMBIGUITY
**§18.2, `[R-MTA-04]`; §21.9, `[R-ERR-03]`/`[R-ERR-04]`; §2.5, `[R-CNF-10]`**

Quotation:

> "The decoded document is a JSON text as defined by RFC 8259, encoded in
> UTF-8. Four restrictions apply, and a document violating any of them is
> unreadable"

and

> "Every limit that affects which files are valid or which files a conforming
> reader accepts lives in this specification, never only in an implementation."

RFC 8259 §9 expressly permits an implementation to limit the maximum depth of
nesting. This document imports RFC 8259 as the definition of a user-metadata
document, pins four other RFC 8259 freedoms (top-level type, BOM, number
range, duplicate keys) and pins key length to 255 bytes — but states no bound
on structural nesting depth in §18.2's restrictions, in §21.9's minimum
guarantees, or in `[R-ERR-05]`'s hard-limit list.

Permitted readings. (i) There is no depth limit: every conforming reader and
verifier must parse a document of any depth, so a recursive-descent parser that
gives up is not a conforming reader, and `[R-ERR-04]` says so in terms
("Software that declines **on that ground** a file whose every quantity lies
within the table is not a conforming reader"). (ii) RFC 8259 §9's licence rides
in with the reference, so a depth-limited parser is behaving as its normative
reference permits and the document is one it "cannot read" — ignore-record
under `[R-CNT-25]`.

I picked (i), because `[R-CNF-10]` and `[R-ERR-03]` both say limits do not live
only in implementations, and because §21.9's table is the stated home for every
acceptance floor. But (i) leaves the implementer with no defined outcome:
`[R-CNT-25]`'s quarantine enumerates the ways a document "can be unreadable" —
"a failed extent CRC, an unimplemented or invalid encoding, a decode failure,
or content violating the document's own rules" — and depth is none of them (the
zstd decode succeeded, the encoding is assigned, the CRC verified, and all four
of §18.2's restrictions are satisfied). §18.2's only decline route is the size
bound. `[R-CNF-04]` then bars improvising: "A reader MUST NOT ... infer values
this specification does not define." So a reader that cannot parse a 200,000-
deep, 1.2 MB, in-every-respect-conforming document must either invent an
outcome or claim a ground the section does not give it.

The concrete file: a top-level user-metadata record, encoding 1, extent length
1,200,005, whose document is `{"a":` × 200,000 + `1` + `}` × 200,000. Every
§21.9 quantity is inside the table (one layer or none, 1.14 MiB document
against the 16 MiB row, no zstd frame). The document is well-formed RFC 8259
JSON, a top-level object, no BOM, one finite number, no duplicate keys, valid
UTF-8, one 1-byte key — so no row of §21.5 applies and the file is conforming.

**Byte-level: yes.** Verifier B, built on an iterative/streaming JSON tokenizer
with an explicit heap stack, parses the document, finds no violation, and
reports *conforming* — it certifies these bytes. Verifier A, built on
recursive descent with a depth guard (what RFC 8259 §9 anticipates and what
most JSON libraries ship), cannot parse it and cannot certify: it reports
either *nonconforming* against R7 — "A decoded user-metadata document is not
well-formed JSON" being the only row its parser's error maps to — or *cannot
establish* on a resource ground, which §2.3 permits generally ("unable to check
on a capability or resource ground") but never anchors to a stated limit. The
two disagree on the accept verdict for one concrete byte sequence. I record my
own reservation: the file's *conformance* is determinate under every reading,
and if triage judges that a certify/cannot-establish split is not an accept/
reject split, this drops to non-byte-level. I flag it high because
`[R-CNF-10]` makes an explicit completeness promise that this omission breaks,
and because a §21.9 depth row would move which documents a conforming reader
must accept.

### adversary-03 — OBSERVATION
**§21.7, `[R-ERR-01]`**

Quotation:

> "a change that reaches the codec is witnessed by the rows for the codec now
> declared, which test the stored bytes as a stream of it (T15, T17, T23, T25),
> or by T14 where the new declaration is codec 1"

Both clauses are stated unconditionally and both fail on constructible files.

T14's condition is "Codec 1 (none) declared and a non-sentinel index entry's
length differs from the tile's decoded size". A layer whose stored tiles happen
to compress to exactly their decoded size, re-declared from codec 2 to codec 1
by a commit, exhibits no T14 — the entry lengths already equal the decoded
size. Constructible: raw DEFLATE of incompressible data is D + 5·⌈D/65535⌉
bytes and of compressible data is under D, so the length can be tuned onto D by
adjusting the tile's redundancy. The stored bytes are then read as a raw
filtered image and every sample is wrong, undetected.

The first clause fails the same way for codec 1 → codec 3: under codec 1 the
stored bytes *are* the tile image, and a tile image is arbitrary sample
content, so a writer can make it a valid single zstd frame decoding to exactly
the decoded size — after which T17, T18, T24 and T25 are all silent.

The register is still right to omit these cases, since they are genuinely
undetectable, and §21.1's completeness clause runs only to *detectable*
violations. What is wrong is the account: §21.7 exists to say precisely where a
witness does and does not exist, and here it promises one that a constructed
file does not provide. An implementer building a verifier from §21.7 will
believe §20.3 step 4's codec clause is covered by T14 and T15/T17/T23/T25 and
will not look further; a corpus builder will believe a vector for the codec
clause is constructible in every case.

**Byte-level: no.** In exactly the cases where the claim fails, the violation
is undetectable, so no implementation's accept/reject verdict changes and no
emittable byte sequence moves. Correcting it means adding a qualifier to a
non-normative-in-effect account of coverage.

### adversary-04 — OBSERVATION
**§21.9, `[R-ERR-03]`/`[R-ERR-04]`; §9.7, `[R-LIF-08]`; §2.5, `[R-CNF-10]`**

Quotation:

> "The table below states **minimum guarantees**, not caps: a conforming reader
> MUST accept any conforming file whose quantities lie within these bounds, and
> a writer MAY rely on that."

and

> "It checks that these occupy disjoint byte ranges, that each lies within
> [16, F − 64), and that each verifies against the checksum covering it"

The guarantee rows are individuated per quantity — the new paragraph does that
carefully — but they are never composed, and two sibling quantities of the
structures they bound are unbounded. First, the rows multiply: 65,536 layers
each with 2³² addressed tiles is inside every row and yields ~2.8 × 10¹⁴
tile-index entries, each a claimant §9.7 obliges a verifier to enumerate and
test for disjointness. §21.9's own note justifies the 2³² figure by a
*reader's* per-tile working set — "the segment-CRC array a reader fetches whole
before using any entry (§15.4) is still 256 KiB" — which is a statement about
one tile read, not about the whole-file walk that §2.3 and §9.7 make a verifier
owe on the same file. Second, a stored tile's *stored* length is bounded by
nothing but F: §17.2 states plainly that "no bound relates a stored length to
its decoded size in either direction", so a tile whose decoded size sits inside
the 256 MiB row may carry a multi-gigabyte stored extent that `[R-CNT-20]`
obliges a reader to fetch whole and CRC before decoding. `[R-ERR-04]` then
removes the escape, since every quantity the table names does lie within it:
"Software that declines **on that ground** a file whose every quantity lies
within the table is not a conforming reader."

The condition is decidable — the walk is a finite disjointness test over
explicit extents — and disproportionately expensive, which is what puts this in
OBSERVATION rather than AMBIGUITY. An implementer building a verifier to this
text has no licensed resource ceiling for the coverage walk and no licensed way
to report a decline for a file that is within the table, and will either ship a
verifier that is formally nonconforming or one that cannot terminate on files
the specification says it must accept.

**Byte-level: no.** The text decides the question against the declining
implementation, so two competent implementations do not disagree about what is
required; they disagree about whether to meet it. Nothing moves in the
emittable or acceptable set.

## 12. Honest summary of what I could not determine

I could not construct a file on which two conforming verifiers reach
*conforming* and *nonconforming* respectively by defensible readings of this
text. adversary-02 is the closest — it splits *conforming* from
*cannot establish*/*nonconforming* — and its force depends on whether a
certify/cannot-establish split counts as an accept/reject split. adversary-01
is a genuine ambiguity whose consequences the outcome classes absorb.

Everything else I attacked was already answered, usually in the sentence
immediately after the one that raised the question. The container path in
particular — front block, trailer, directory, record framing, layer record,
index, segments, sentinel, slabs, alignment, coverage — I implemented end to
end from this document with no guesses at all, and every constant and every
worked example I recomputed came out right.
