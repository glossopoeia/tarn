# Cleanroom round 35 — Adversary transcript

## 0. Disclosure and setup

I read exactly one file: `/Users/robertkleffner/Documents/GitHub/tarn-first-draft/spec/tarn.md`.
It was at the path the brief named. I read it end to end in eight `sed -n` slices
(lines 1–420, 420–900, 900–1400, 1400–1900, 1900–2420, 2420–2960, 3000–3300,
3300–3620, 3630–3800, 3800–3920, 3920–4180, 4180–4450, 4450–4864), plus two
targeted re-reads (4692–4715, 4757–4775) to get quotations exact. Two slices
overflowed the tool's output cap and were persisted to a tool-results file by the
harness; I did not read those persisted files — I re-issued narrower slices
instead.

I opened no other file. No ADR, no `docs/`, no `PLAN.md`, no `conformance/`, no
`spec/registry.json`, no git history, no web. I listed exactly one directory: my
own scratch directory, to confirm it was empty before I began. It was empty — no
previous attempt's files were present.

**Context I did not ask for.** Material was placed in my context before I began:
a project instruction file pointer (`CLAUDE.md` → `AGENTS.md`) and an index of
the maintainer's memory notes with titles referring to this project's harness,
gates, repair practice and round structure; also a git status snapshot with
recent commit subject lines. None of it is the specification. I disregarded all
of it and reached no conclusion from it. I name that it appeared without
repeating its contents. The git subject lines in particular name prior rounds'
outcomes; I did not use them to aim, and every conclusion below is derived from
`spec/tarn.md` and from arithmetic I ran myself.

**Files I wrote**, all inside
`/private/tmp/claude-501/.../r35-round/scratch/adversary/`:

- `norm.txt` — a whitespace-normalised, blockquote-marker-stripped copy of the
  spec, built so that phrase searches survive the hard wrap.
- `posmap.json` — normalised-offset → original-line map for the above.
- `s.py` — the search driver (regex over `norm.txt`, prints hit count and
  context with an approximate line number).
- `crc.py` — a CRC-32C implementation (Castagnoli, reflected, init/xor
  0xFFFFFFFF) plus the document's own check vectors.
- `count.py` — a register-row and instance counter over §21.2–§21.5.

I ran no file that I did not write in this session.

## 1. Method, and why my zeros are worth something

The brief warns that the document is hard-wrapped and that a line-oriented grep
will report a false zero. I built `norm.txt` first and validated the instrument
before trusting any zero. Control test:

```
python3 s.py "the register enumerating file-conformance violations"  -> HITS=1 (line ~3238)
python3 s.py "no check any actor owes able to see it"                -> HITS=1 (line ~3270)
python3 s.py "Slack has no internal structure this specification defines" -> HITS=1 (line ~711)

grep -c "the register enumerating file-conformance violations" spec/tarn.md -> 0
grep -c "no check any actor owes able to see it"               spec/tarn.md -> 0
```

Plain grep misses all three; my instrument finds all three. Every "hits = 0"
below was produced by the validated instrument.

## 2. Arithmetic: I re-derived every number the document states that I could

This is the cheapest way to find out whether the document is careless, and the
answer is that it is not. I implemented CRC-32C from the parameters §4.5 states
(polynomial 0x1EDC6F41 → reflected 0x82F63B78, reflected in/out, init
0xFFFFFFFF, final XOR 0xFFFFFFFF) and reproduced every checksum in the document:

| Quantity | I computed | Document states |
|---|---|---|
| CRC-32C(`"123456789"`) | 0xE3069283 | 0xE3069283 (§4.5) |
| CRC-32C(zero bytes) | 0x00000000 | 0x00000000 (§4.5) |
| CRC-32C(4 sentinel entries, 80 bytes) | 0x80A34955 | 0x80A34955 (§7.4 Example) |
| CRC-32C of that 4-byte CRC array | 0xC4EE982E | 0xC4EE982E (§7.4 Example) |
| CRC-32C(2¹⁶ sentinel entries) | 0xEECB3BB2 | 0xEECB3BB2 (§15.4, App. B) |
| Appendix A trailer CRC over [0,60) | 0x402F157E | 0x402F157E (App. A) |

I rebuilt Appendix A's trailer field by field from §6.2's layout to get that last
one, which means §6.2's offsets, the field widths, and Appendix A's hex dump all
agree.

Other derivations, all matching:

- §7.4's Example layer record: 4 (name) + 34 (nine scalars: layout 1,
  linearization 2, codec 2, filter 2, A 8, S 8, A_slab 8, rank 1, C 2) + 18
  (dimension entry) + 12 (channel entry) + 13 (index_encoding 1, entry_count 8,
  crc_of_crc_array 4) = **81**, exactly as stated, with no residue, so the
  sub-record sequence is empty. Extent length 4·20 + ⌈4/2¹⁶⌉·4 = **84** ✓.
- §11.2/§11.4 Example: G = (4,8), N = 32, P = 65,536; (300,700) → tile (1,2),
  s = 10, in-tile (44,188) → 44·256+188 = **11,452**; planar c=2 → 2·32+10 =
  **74** ✓.
- §14.2 Example: interleaved (2,3), P=6, uint8+uint16 → Q=3, decoded 18, ordinal
  5 at bytes [15,18) ✓; planar `b` plane 12 bytes, ordinal 5 at [10,12) ✓;
  float32+bool → Q=5, decoded 30, ordinal 5 at [25,30) ✓.
- §14.3 Example: P=10 alternating from true → byte 0 = 0x55, byte 1 = 0x01 with
  six pad bits; fill true → 0xFD ✓.
- §14.5 Example: extents (5,5), tiles (4,4) → grid 2×2; edge tile (1,1) has one
  real position (4,4) and **15** padding; 16 uint16 values = 32 bytes ✓.
- §15.4 Example: entry_count 1,000,000 → 16 segments (15 full, last 16,960),
  64-byte CRC array, region 20,000,064 bytes; tile 999,999 at segment-relative
  byte 339,180; segment 15 = [19,660,800, 20,000,000) ≈ 339 KB; one full segment
  = 1,310,720 = 1.25 MiB ✓. Second Example: disk ordinal 74 → region bytes
  [1,480, 1,500); channel 3 unstored → entries 96–127 ✓.
- §17.3 Example: I applied the shuffle `byte i of group j → offset i·n+j` to
  `00 00 80 3F 00 00 00 40 00 00 40 40` (s=4, n=3) and got
  `00 00 00 00 00 00 80 00 40 3F 40 40` ✓.
- §20.3 Example: 32-tile interleaved index region = 32·20 + 4 = **644** ✓.
- §9.3 Note: largest multiple of 64 ≤ 2⁶³−1 is 2⁶³−64 ✓.
- §21.9 Note: ⌈2³²/2¹⁶⌉·4 = 262,144 = **256 KiB**; ⌈2³⁶/2¹⁶⌉·4 = **4 MiB**;
  12.5 MiB / 65,536 = 200 bytes per layer record, consistent with "the small
  layer records that figure assumed" ✓.
- §4.6 Example: `température` NFC = 12 bytes, the exact byte string given; NFD =
  13 ✓.
- §13.3 Rationale's "a zeroed index region … is loudly invalid": I checked that
  CRC-32C(4 zero bytes) = 0x48674BC7 ≠ 0, so a zeroed region with
  crc_of_crc_array = 0 fails L37 at layer scope, and CRC-32C(20 zero bytes) =
  0xBCC5563E ≠ 0. The claim holds at the scope claimed.

Nothing in the document's arithmetic is wrong. I therefore stopped looking there.

## 3. Mechanical audit of the register (§21.1–§21.5, §21.8)

§21.2, §21.4, §21.8 and §21.1 are all on the changed surface and §21.8 states a
closed count, so I derived it.

`count.py` parses every row of the form `| F<n> |`, `| L<n> |`, `| T<n> |`,
`| R<n> |` and counts semicolon-separated instances (a cell reading `—` counting
as one, per §21.1's "a cell reading — is one instance"):

```
F: 35 rows, labels 1..36, missing=[11], instances=56
L: 49 rows, labels 1..49, missing=[],   instances=116
T: 26 rows, labels 1..26, missing=[],   instances=55
R: 10 rows, labels 1..10, missing=[],   instances=50
TOTAL 120 rows, 277 instances
```

§21.2 says 35, §21.3 says 49, §21.4 says 26, §21.5 says 10; §21.8 says "120
conditions over 277 instances". Exact match, and the F11 gap the Note declares is
the only gap.

I then audited the instance counts against §21.1's two stated conventions, row by
row, because the conventions themselves are on the changed surface:

- **Layout axis.** T3, T14, T22 each carry 3 layout formulas × 2 magnitude
  directions = 6 ✓. T21 and L44 are one-directional ("larger than", "exceeds") ×
  3 formulas = 3 ✓. L21 is 2 formulas (N, C·N) × 2 directions = 4 ✓. T4's 4 is
  the layout × type cross (interleaved numeric / interleaved bool / planar
  numeric / packed planar bool) with no direction, an equality against a recorded
  value ✓. T26's 3 is the same cross minus interleaved-bool, since the stride is
  what varies ✓. L2 correctly omits ⌈P/8⌉, which can never exceed 2⁶³−1 given
  P ≤ 2⁶³−1.
- **Magnitude axis.** Every "differs from"/"does not equal" row carries two
  directions (F17, F23, L12, L21, L22, L30, T3, T14, T22); every "exceeds"/
  "below"/"less than"/"larger than" row carries one (F2, F3, F5, F9, F10, F16,
  L1, L44, T9, T11, T12, T21); every checksum-vs-computed and pattern-vs-constant
  row carries none (F1, F6, F8, F14, F20, L37, L38, T1, R2) ✓; and the nonzero
  value tests (L20 "A ≠ 0 and S ≠ 0", L27, L28) are single instances ✓.
- **Value-set cells.** L31 (3), L33 (4), L34 (4), L36 (2), L43 (3), L45 (3), R1
  (2 alternatives × 2 containers) each reproduce exactly the partition their
  owning section states (§7.4/§15.1, §11.4, §12.2, §14.1, §17.2, §17.3, §18.2),
  and §10.2's collected table agrees with all seven.
- **Container axis.** F-rows carry one container, L-rows two (layer record /
  sub-record), R-rows two (top-level / sub-record), consistently: L15 = 2×2,
  L16/L17 = 2, L46/L47 = 2, L49 = 2×2, R5 = 2×2×2 = 8, R7 = 3×2 = 6, R4 =
  8 constraints × 2 = 16 ✓.

**Result: the register is internally consistent with its own conventions. I found
no miscount and no missing instance.** I record this as a clean lane rather than a
finding, and I say exactly what I did that would have found one.

I also derived §21.2's reach claim rather than accepting it. [R-CNT-24] fixes,
across all majors: the trailer magic at F−64, version_major/minor at F−56, a
CRC-32C at F−4 over [F−64,F−4), and the constancy of the front block. The
conditions asserting only those invariants are F8 (magic), F14 (trailer CRC), F6
(front block) and both of F1's instances — and no other row, because every other
F-row reads either a field inside the 48 redefinable trailer bytes (F2, F3, F12,
F13, F15, F17, F19 …) or a major-1 structure (F20 onward). §21.2's derivation is
correct, and its treatment of F18 as outside the premise matches [R-CNF-13].

I checked §21.1's strict-specialisation list pairwise. F1's front-block instance
⊂ F6 (the reversed constant is not the constant); F1's trailer-magic instance ⊂
F8; F35 ⊂ F36; L24 ⊂ L25; F21 ⊂ F22 (extent_length 0 < 5); L10 ⊂ L11. All six
hold. I looked for a pair the list misses and found only overlaps that §21.1
expressly excludes: T10 (length 0) and T14 (codec 1 length mismatch) are each
reachable without the other, so they overlap rather than specialise.

## 4. The changed surface, read hard

### 4.1 §20.3 step 4 — the closed list of permitted changes

This is where the brief points hardest, so I enumerated the transitions myself
before reading the member.

Search: `python3 s.py "declared, changed" 220` → **4 hits**. Three sites carry
"declared, changed or cleared" (§11.1's Rationale at ~1665, §20.3 step 4 at
~3222, Appendix H at ~4825) and one carries "declared, changed or **kept** … or
is cleared" (§20.3's delegated obligation clause at ~3324).

Transitions a slab or alignment declaration can make across a commit, and the
verb that names each:

| Transition | Named by |
|---|---|
| none → some | "declared" |
| some → another value | "changed" |
| some → the same value | **not a member — and does not need to be**: the governing clause is "A layer that stores a tile in the generation this commit supersedes **keeps its declarations**, with these exceptions and no other". Keeping is the base case, not an exception. |
| some → none | "cleared" |
| none → none | the same base case |
| exclusive switch A≠0 ↔ S≠0 in one commit | "cleared" applied to one declaration plus "declared" applied to the other, composed under "A commit MAY make several of these changes at once, an extension and a shortening of one channel list excepted" — the exception is channel-list-only, so the pair composes. |

So I could not find a transition nothing names. I then went after the second and
third shapes the brief describes.

**A delegated clause naming a disposition the member does not.** The member ends
"as this step provides below", and the clause below reads:

> on a layer this commit modifies, a slab declaration declared, changed or kept
> has its invariants satisfied over every run of the new state, the runs this
> commit adds included, or is cleared (`[R-SLB-03]`, `[R-SLB-04]`, `[R-CNF-05]`),
> and an aligned layer's stored tiles, every one the new state holds and those
> this commit adds included, satisfy its invariant or the declaration is cleared
> (`[R-SLB-01]`, `[R-CNF-05]`).

The clause names "kept", which the member does not. I asked whether that is a
gap and concluded it is not, in either direction:

- *Obligation side.* Keeping a slab declaration does need the obligation — a
  commit that grows an extent repartitions the runs and can break packing without
  touching the declaration — and the clause supplies it. If the clause omitted
  "kept", that would be the defect. It does not omit it.
- *Permission side.* Keeping needs no permission beyond "keeps its declarations".

**Quantifier comparison against the cited rules.** I put the clause beside each
rule it grounds itself in:

- [R-SLB-04] binds "A writer or updater whose commit changes the stored-tile set,
  the run partition, the byte placement of any run, the disk ordinal of any tile
  the new state stores, or the slab declaration itself, of a layer slab-declared
  in either the superseded or the new generation". Every member of that trigger
  set entails modifying the layer, so §20.3's "on a layer this commit modifies"
  is a superset. It is a strict superset — a commit that merely renames a
  slab-declared layer whose runs were already broken is reached by §20.3 and not
  by [R-SLB-04] — but the extra reach is licensed by [R-SLB-03] + [R-CNF-05],
  which the clause also cites, since [R-SLB-03]'s invariant is a standing
  file-level one and [R-WRT-05] makes a modified record new output. No gap.
- [R-SLB-01] binds "every stored tile's offset" unconditionally. §20.3's
  alignment half is quantified over "an aligned layer's stored tiles, every one
  the new state holds", which reaches a *changed* A — the case a static reading
  of [R-SLB-01] alone might be thought to miss. It is the narrower statement, but
  [R-SLB-01] stands behind it, so nothing escapes.
- I checked the appositives "the runs this commit adds included" and "those this
  commit adds included". Both are subsets of the universals they qualify
  ("every run of the new state", "every one the new state holds"), so they are
  redundant emphasis. They carry the fingerprints of a repair (shape 11), so I
  asked what the rewrite opened: nothing I could find — the universal already
  covered the appositive in both halves.

**The partition claim.** "Between them the two lists reach every declaration
field of §7.4." I walked §7.4's table: name (permitted), layout, linearization,
codec, filter (fixed), A, S (permitted), A_slab (permitted, as part of "a slab …
declaration"), rank d (fixed via "the rank and the dimension order"), channel
count C (reached only *through* the channel lists — permitted for planar, fixed
for interleaved), dimension name (permitted), extent (permitted, grow only), tile
extent (fixed), channel name (permitted), type and fill (fixed), index_encoding
(fixed), entry_count / crc_of_crc_array / extent slot ("follow the commit"),
sub-records (§20.4's). C is the only field reached indirectly, and the indirect
route is exact. The claim holds.

**The "bar names its own category" sentence.** §20.3 says the bar on the fixed
declarations states "no condition a file can exhibit" (§21.7's second category),
not merely an unwitnessed one. I tested this by trying to build a pair of files
that differ in whether the condition obtains. Take file X = generation 1 (layer
L, fill 0, one tile stored) followed by generation 2 (L re-declared with fill 1).
Now ask whether a creator could emit the identical byte sequence in one commit.
It could: gen 1's directory, pad and trailer lie in the interior as slack; slack
content is unconstrained ([R-CNT-21]) and gap *extent* is free ([R-SLB-05]); a
mimic in slack is inert (§21.6). So the same bytes arise from a conforming
creation, and "a commit changed a fixed declaration" is not a property of the
bytes at all. The document's category assignment is right, and it is the stronger
of the two.

**The witness list.** "…but for a stored tile's decoded size, a padding position
or pad bit, or a boolean byte the register witnesses (T3, T14, T21, T22, T4, T5,
T2) and a decode that fails outright under a changed codec or filter (T24, T25),
no check any actor owes able to see it." I walked each fixed declaration: a
changed tile extent, rank, layout or channel type moves the decoded size (T3,
T14, T21, T22); a changed fill breaks padding (T4, T5); a bool appearing or
moving gives T2; a changed codec or filter gives T24/T25 or wrong content. A
changed linearization or index encoding cannot occur in an otherwise-conforming
file, only value 1 being legal for each. A permuted dimension order in an exactly
tiled layer, and a permutation of two same-typed same-filled planar channels, are
both genuinely invisible — which is what the sentence claims. L44 and L2 are not
missing from the list: they read the *new* declarations alone and see no change.

I could not break §20.3 step 4. I record it as attacked and standing.

### 4.2 §15.2 and §15.3 — the sentinel and entry validity

I treated §15.3's table as a partition claim (shape 5) and looked for the entry
state on neither side and the one on both.

- offset=S ∧ length=S ∧ crc=0 → valid sentinel. crc≠0 → row 2. Exactly one
  field at S → row 3 (and §15.2 says so expressly: "an entry with exactly one
  field at the sentinel value is §15.3's own row before either rule reads it").
- Row 6 excludes S ("neither field being S"), so offset=S with length=2⁶³ falls
  to row 3, not row 6. Row 7 requires "each field alone being in domain", so a
  double-S entry cannot reach it. No entry state reaches two rows with different
  outcomes; the overlapping pairs (offset 0 ∧ length 0 hits rows 4 and 5) agree.
- A well-formed non-sentinel entry has no row, which is correct — the table
  classifies malformed states plus the valid sentinel.
- "Six rows are marked *structural*" — I counted rows 2,3,4,5,6,7 = 6 ✓.

I then tested the structural-entry consequences against the three rules that read
them. An entry with offset 10 (< 16) nominally addresses bytes of the front
block; it contributes no stored extent, so [R-LIF-08]'s walk never sees the
overlap and F33 does not fire — and F33's own cell says exactly that ("a claimant
reaching the front signature block or the live trailer is instead caught by the
bounds rows … and T8/T9, each at its own tier"). An entry whose only defect is
its stored bytes' crc keeps its extent in the walk, the verifier rows and run
continuity, which is what keeps [R-SLB-03] decidable from the entries alone plus
F. I constructed the case where a structural entry's nominal offset lies inside a
sibling's extent and confirmed no L18 is owed. This all coheres.

### 4.3 §18.2 — the metadata frame

Longest and most-repaired passage on the surface, so I read it against
[R-COD-06] clause by clause.

[R-COD-06] states seven things about a zstd frame. §18.2 saves two ("what it
states against a tile's declared decoded size, and what it states about the
frame's declared `Window_Size`") and replaces both; it carries over five by name
and says two of those five fall outside the register (undisclosed dictionary use,
unwitnessed; the buffer-sizing bar, which binds a reader and states no condition
a file can exhibit). R4's sixteen instances are exactly the remaining eight
checkable constraints × two containers: magic, skippable frame, second frame,
nonzero dictionary ID, content-checksum flag, trailing bytes, content-size larger,
content-size smaller. Nothing is missing and nothing is double-counted.

I probed the composition of §21.9's two guarantees. A 9 MiB document framed with
Single_Segment_Flag has Window_Size = 9 MiB, within the 16 MiB document
guarantee but above the 8 MiB window guarantee, so it falls outside [R-CNF-03]'s
acceptance duty even though its decoded size does not. The document says exactly
this, and adds the sentence that closes the obvious misreading: "§21.9's
user-metadata row bounds a document's decoded size; it does not relieve the frame
carrying it of the `Window_Size` row."

I then tested the antecedent of "a document larger than **that guarantee**,
framed that way, exceeds a §21.9 row". The nearest guarantee is the 8 MiB
Window_Size one; a reader supplying the 16 MiB one instead gets a claim that is
still true, only less tight. So the loose anaphor forks nothing, and the next
sentence disambiguates. Rejected.

Attempted fork: two verifiers with different window bounds (8 MiB and 16 MiB)
over a 9 MiB single-segment document. Verifier A reports *cannot establish*;
verifier B certifies. Not the charter's fork: *cannot establish* is a third
verdict the document defines, expressly turned on the verifier's capability
([R-CNF-11], §18.2's "the bound is that verifier's capability and not a limit on
validity"), and A does not reject.

### 4.4 §21.6 and §21.9 — conditions that are not violations, and the limits

I checked each §21.6 row against its cited rule and found no divergence. The two
"conforming files a reader nevertheless refuses" are consistent with
[R-CNF-03]'s qualifier and with §21.9's "the two capability refusals §21.6's
closing paragraph names … are not this ground".

I attacked §21.9's per-instance individuation with degenerate layers. A layer
with E = (0,) and T = (2⁴⁰,) addresses no tile, so [R-COD-07]'s lz4 cap is
satisfied whatever its declarations would derive — §17.2's Note blesses this
expressly, and adds the discriminator that [R-ENC-04]'s overflow rule *does*
apply in an empty layer because it "carries no such quantifier". I verified the
two designations are layout-keyed: §14.2's table designates P·Q for interleaved
and P·Bᶜ for planar-numeric, and says so ("a planar layer has no P · Q to form"),
while §14.3/[R-SER-07] designate ⌈P/8⌉ for a packed bool plane. L2's instance
list matches, including its dominance notes (P·Q ≥ P·C because Q = ΣBᵢ ≥ C;
C·N > (C−1)·N + (N−1)).

I then ran the fetch-bomb attack: a conforming file with a 1 TB stored tile
extent whose decoded size is 1 KiB. §21.9's table bounds no stored length
(searches for "stored length", "stored size", "length of the stored",
"stored extent's length" returned 4/0/0/0 hits, none of them a bound), so
[R-CNF-03] and [R-CNF-10] oblige a conforming reader to accept it and §19.4 step
5 obliges the fetch. I looked for a sentence that would let a reader decline and
found instead the sentence that closes the attack: §22.2's Note claims only that
"a reader that validates both before fetching cannot be induced to read more than
**the file contains**" — which is true, and is the honest bound. The attacker
pays a terabyte for a terabyte. Rejected as a defect.

### 4.5 §22.3 — the four residues

I counted the residues (slack; an unassigned type's extent; a trailer mimic in a
payload; an experimental-encoding user-metadata extent) and got four, matching
"Four residues are stated rather than defended". I checked §8.1's coverage map
against §4.5's list of exceptions and confirmed the interior checksums close:
each segment CRC array is covered by crc_of_crc_array; each entry crc by its
segment CRC; crc_of_crc_array by the directory CRC; each stored tile by its entry
crc. Only the three terminal fields, the front block and an unassigned type's
extent are uncovered, exactly as §4.5 enumerates.

### 4.6 §19.1 step 4, §19.3, §19.4

I tested the layer-name namespace rule with two layers whose name fields are both
the single byte `00`. Uniqueness is decided first and over raw bytes "whether or
not each name is itself well-formed … even when neither name is valid", so F4
fires and the file is reject-file rather than the layer being reject-layer. That
is odd but expressly decided, and it survives both readings of "well-formed"
(UTF-8 sense or name-validity sense), because an empty field is well-formed UTF-8
either way. Not a fork.

I checked §19's enumerations against the register and found the shield: "Those
enumerations are not the complete inventory of what a reader detects at that
tier: §21's register is … A row this section does not restate is due at its own
tier all the same." That forecloses the whole family of "§19.3 forgets to cite
[R-ENC-11]" attacks. I abandoned them.

### 4.7 The compactor (§20.5), attacked at length

This is off the named surface, and the brief notes that several rounds found
their survivor in untouched text, so I spent real time here.

Construction. Input I: front [0,16); a top-level user-metadata extent at
[16,116); layer A's stored tile at [116,216); A's index region at [216,300); the
directory; pad; trailer. I has no interior slack. The user-metadata extent's
terminal CRC does not match its preceding bytes — I is nonconforming on row R2,
and nothing else. A compactor opens I ([R-RDR-01] — the open "consumes the
trailer and directory only … no extent slot's content"), validates A's record
(§19.3) and index chain ([R-IDX-04]), verifies A's stored tile's entry crc, and
chooses a placement that leaves every structure at its input offset. Nothing is
relocated. It mints a fresh file_id and writes output O.

Compactor **X** reads [R-WRT-09]'s enumeration — "each **relocated** extent's
checksum, including every stored tile's entry crc" — as the operative obligation,
and [R-WRT-07]'s vocabulary makes "relocated" mean "moved", since its Example
says "In this placement A's stored extents happen not to move". The
user-metadata extent did not move, so X does not verify it, detects nothing, and
emits O. §20.5 bars only emitting "a violation **it has detected**", and
[R-WRT-01] expressly lets "a violation latent in a structure it carries forward
verbatim travel into its output".

Compactor **Y** reads the same sentence's leading clause — "it relies structurally
on **every structure it copies**, so it MUST verify each link of the chain" — as
the obligation. Y verifies the extent's terminal CRC, it fails, a check
[R-WRT-09] obliges has failed, and §20.5's "A compactor MUST refuse to compact
when any check [R-WRT-09] obliges fails" makes Y refuse. O never exists.

I then looked for the sentence that closes it, on the "read the paragraph above"
discipline. Two things cut:

1. [R-WRT-07]'s closing sentence restates the depth as "each stored tile's entry
   crc" — **unqualified** — which closes the *tile* half of the ambiguity in
   Y's favour. It says nothing about a non-tile extent.
2. The sentence's own grammar: "so it MUST verify [list]" makes the list the
   obligation and the reliance principle its justification. On that parse X is
   right, and Y's extra check is supererogatory but not forbidden.

Reading 2 leaves the divergence in place as *licensed*: X and Y are both
conforming and O exists in one world and not the other, because §20.5 keys the
bar to detection. That is a deliberate design, not an ambiguity. Reading the
leading clause as operative instead makes X nonconforming.

Two further reasons I graded this **below** byte-level rather than at it. First,
O carries a register-row violation (R2), so the disputed file is not itself
conforming, which is the discriminator the calibration names. Second, §8.2's
"chain of trust" is enumerated as trailer → directory → crc_of_crc_array →
segment CRC array → index segment → index entry → stored tile; a user-metadata
extent's CRC is not a link in it, so "each link of the chain" does not reach it
under either reading, and the reliance principle is separately blunted by
[R-MTA-02], which forbids the compactor to rely structurally on a document at
all. I file it as an ambiguity because two competent implementations plainly
land differently on what [R-WRT-09] obliges, and I grade it honestly. Triage may
disagree with my downgrade; the construction above is what it should be tested
against.

### 4.8 Attacks I built and closed

Recorded in full in the structured `rejected_candidates` field. The ones that
took longest were the empty-layer lz4 escape, the fetch bomb, the planar-bool
return encoding, the pre-trailer gap longer than step 5's pad, and the
experimental-range MU = 1 sub-record.

## 5. Findings

### adversary-01 — Appendix G's closing inventory omits three of item 5's four pins

**Kind:** OBSERVATION. **Location:** Appendix G, item 5 and the closing paragraph.

The closing paragraph presents itself as the inventory of freedoms the profile
closes:

> The items above add what is not, and the list is not short: gap *content*,
> which `[R-CNT-03]` only advises; gap *extent*, which placement freedom
> (`[R-SLB-05]`) leaves open; record and sub-record order, which `[R-CNT-14]`
> leaves free; the fill a writer records when its caller chooses none
> (`[R-TYP-10]`, a SHOULD); the sentinel for every all-fill tile, which no rule
> requires; a single generation, which §9 nowhere constrains; the absence or
> fixing of a declared alignment and slab, which §16 leaves to the writer;
> `version_minor` at its floor, which `[R-CNT-26]` states as a SHOULD — item 8,
> binding creator and compactor alike save §20.5's carried-feature case, its
> `flags` half a creator's rule alone; a derived `file_id`, where §9.3 states
> only advice; NFC-normalized names, which `[R-ENC-14]` states as a SHOULD; and
> the producer pinning of items 1 and 9.

Item 5 pins four things, each with the same shape — a degree of freedom a
normative section expressly leaves to the writer — and the paragraph names one:
"the absence or fixing of a declared alignment and slab, which §16 leaves to the
writer". It does not name **a fixed filter value** ("§17.3 leaves the choice to
the writer"), **fixed declared tile extents** ("§11.3 states that tile extents
are a writer's choice and that this specification imposes none"), or **a fixed
layout** ("§14.1 leaves the layout to the writer"). Every other numbered item is
represented, several of them twice (item 3 contributes gap content, gap extent
and record order; item 8 contributes both halves).

The closing hedge — "Read the numbered items as the list; this paragraph names
what they are for, not how many there are" — disclaims the *count*, and I weigh
that against the finding. It does not disclaim naming three whole kinds of
freedom; the paragraph's own construction ("the list is not short: …") is an
enumeration of kinds, not a count.

Cost to an implementer: an adopter who reads the closing paragraph as the
inventory of what the profile must pin — a natural reading, since it is the only
place the items are stated as *freedoms* against the rules that leave them open —
pins alignment, slab, gaps, order, fill, sentinels, generations, minor, file_id
and names, and leaves the filter, the tile extents and the layout unpinned. Two
such writers agreeing on everything else still emit different bytes, which is
precisely the failure item 5 exists to prevent and which item 5's own text
spells out ("the tile extents fix every tile's shape and with it the grid count,
while the layout fixes how many tile-index entries the layer addresses").

Non-normative (Appendix G is identified as non-normative), and no rule turns on
it, so it cannot move the emittable set.

### adversary-02 — [R-EXT-02] states a universal its own next sentence contradicts

**Kind:** CONTRADICTION. **Location:** §10.2, [R-EXT-02].

First citation:

> Every numeric identifier space is partitioned identically: values this
> specification assigns; a **reserved** range only this specification assigns
> from; and an **experimental** range for private use.

Second citation, four sentences later in the same requirement:

> Value 0 is invalid in every space above. Two spaces carry no experimental
> range: channel layout, whose `u8` field is too narrow to spare one — 3 through
> 255 stay reserved to this specification — and the trailer's flag lanes, which
> §6.3 partitions instead.

The universal says every space carries all three parts; the second sentence names
two that do not. For channel layout this reads as a permitted emptiness (the
experimental part is empty), which strains "partitioned identically" but survives.
For the trailer's flag lanes it does not survive: they are not partitioned into
assigned / reserved / experimental at all — "§6.3 partitions instead", into an
incompat lane and an ignore lane — and they are not among the eight spaces the
table between the two sentences collects ("The spaces, defined in the sections
that own them and collected here"). So the sentence calls a "space" something the
requirement's own inventory excludes and its own opening universal cannot
describe.

Nothing operational turns on it: no reader, writer, updater or verifier behaviour
depends on whether the flag lanes are a numeric identifier space, and §6.3 states
their rules directly. The cost is that a reader who takes the opening universal
at face value must then decide, unaided, which of the two sentences governs when
counting the spaces — for instance in reading §20.5's "one row for each of the
other seven spaces §10.2 tabulates", which resolves to the table's eight minus
record type and therefore silently uses the table, not the "two spaces" sentence,
as the inventory. (I verified that count: the seven rows §20.5 lists — L31, L33,
L34, L36, L43, L45, R1 — are exactly the seven non-record-type spaces the table
carries, and each does register a reserved-range violation.)

### adversary-03 — L23's Detected cell splits at a boundary its Instances cell does not

**Kind:** OBSERVATION. **Location:** §21.3, L23; §19.1 step 4; §21.8
[R-ERR-02]; §24 [R-VEC-03].

L23 reads:

> | L23 | A declared region of the layer record's inline payload does not lie
> entirely within inline_length (overrun or truncation) | leading fixed fields
> (name … C); d dimension entries; C channel entries; trailing fixed fields
> (index_encoding, entry_count, crc_of_crc_array) | reader | open (the name
> field, §19.1 step 4); layer access (every other field and entry) |
> `[R-CNT-18]` |

The Detected cell distinguishes the name field from every other field of the
same instance. §19.1 step 4 gives that case a consequence no other L23 case has:

> a layer record whose name field does not lie entirely within that record's
> inline_length yields no name field to compare, so it contributes no name to the
> namespace and is instead a validity error at layer scope (`[R-CNT-18]`).

So the name-truncation file is behaviourally distinct from, say, a
codec-field-truncation file: it is detected at a different tier and it changes
what F4 ranges over. But the Instances cell folds both into one instance,
"leading fixed fields (name … C)". §21.8 requires "at least one vector per
instance" and §24 [R-VEC-03] repeats it, so a corpus can discharge L23 in full
with four vectors none of which is the open-tier name case — leaving the one L23
behaviour that interacts with another row (F4's namespace) unexercised.

The asymmetry is visible against R1, the only other row with a compound Detected
cell: R1 reads "open (top-level); layer access (sub-record)", and R1's Instances
cell *does* enumerate the two containers, so its four instances match its two
detection points. L23's do not.

Whether this is a defect turns on §21.1's own rule, which cuts both ways. "An
instance names a field the condition ranges over, a container it can occur in,
one of several alternatives the condition text states, or any combination of the
three" supports enumerating by region, as L23 does. But "One instance is one
*distinguishable* file: where a condition is a single predicate over several
fields … the fields it reads are not instances, **because no two files could
differ**" gives the reason fields collapse — and here two files plainly can
differ, and differ in tier and in downstream effect. I state both readings; I
picked the second, because the row's own Detected cell concedes the distinction.

Cost to an implementer: none directly — §19.1 step 4 states the behaviour
normatively. The cost falls on the corpus, which is the instrument the document
offers for catching an implementer who missed it.

### adversary-04 — [R-WRT-09]'s stated principle reaches further than its enumeration, and the difference decides whether a compactor must refuse

**Kind:** AMBIGUITY. **Location:** §20.5, [R-WRT-09]; §20.5's first paragraph;
[R-WRT-07]'s closing sentence.

> A compactor's verification depth follows reliance over everything it carries
> (`[R-WRT-03]`): it relies structurally on every structure it copies, so it MUST
> verify each link of the chain — the open (§19.1), each retained layer's record
> (§19.3) and full index chain (`[R-IDX-04]`), and each relocated extent's
> checksum, including every stored tile's entry crc — before emitting that
> structure's bytes.

Two readings, both defensible:

- **(E)** The em-dash list is the obligation; "it relies structurally on every
  structure it copies" is the justification for choosing that list. Then a
  compactor owes a checksum verification only for an extent it *relocates* —
  "relocate" meaning "move", the sense [R-WRT-07] fixes when its Example says "In
  this placement A's stored extents happen not to move".
- **(P)** The principle is the obligation and the list illustrates it. Then a
  compactor owes verification of every structure it copies, relocated or not.

The tile half of the difference is closed by [R-WRT-07]'s restatement, which
names the depth without the qualifier: "That `[R-WRT-09]`'s checks reach the
index chain and **each stored tile's entry crc** rather than an entry's own value
domain bounds how far a compactor goes looking". The non-tile half is not closed
anywhere I could find.

Concrete construction (built in §4.7 above): input I is conforming except that a
top-level user-metadata extent's terminal CRC does not match (row R2), and the
compactor's chosen placement leaves that extent at its input offset. Under (E)
the compactor never verifies it, detects nothing, and emits output O — permitted,
because §20.5 bars only emitting "a violation **it has detected**" and
[R-WRT-01] expressly lets a latent violation "travel into its output". Under (P)
the compactor verifies it, the check fails, and §20.5's "A compactor MUST refuse
to compact when any check `[R-WRT-09]` obliges fails" makes it refuse. O exists
on disk under one reading and not the other.

What an implementer does wrong without this resolved: a compactor built to (E)
launders a corrupt user-metadata extent into a fresh file_id with a clean-looking
trailer, and reports success; a compactor built to (P) refuses files its peer
compacts. A pipeline that runs both sees non-deterministic refusals.

I graded this **not** byte-level, for two reasons I want on the record because
they are contestable. O carries a register-row violation, so the disputed file is
not itself conforming — the discriminator the calibration names. And §8.2's chain
of trust, which "each link of the chain" refers to, is enumerated as trailer →
directory → crc_of_crc_array → segment CRC array → index segment → index entry →
stored tile; a user-metadata extent's CRC is not a link in it, and [R-MTA-02]
independently forbids a compactor to rely structurally on a document, so the
reliance principle is blunted exactly where the enumeration is silent. Reading (E)
is therefore the better one, and under (E) the divergence between a compactor
that looks and one that does not is licensed rather than ambiguous. If triage
reads the leading clause as operative, this is byte-level and the two
implementations are the ones named above.

### adversary-05 — §6.4 and §19.1 assert as fact what [R-CNT-10] provides against

**Kind:** OBSERVATION. **Location:** §6.4, [R-CNT-09]; §19.1 step 1,
[R-RDR-01]; §6.4, [R-CNT-10].

§6.4:

> The baseline remote open is two requests, each with an exact target: (1) fetch
> the final 64 bytes — a suffix range, whose response also carries the
> transport-authoritative file size F (`[R-CNT-10]`), so that §19.1's first two
> steps cost one request between them

§19.1 step 1 repeats it: "a remote reader's suffix range for step 2 carries F in
its own response, so steps 1 and 2 cost one request between them (§6.4)".

Both state unconditionally that a suffix-range response carries the
transport-authoritative size. [R-CNT-10], two paragraphs below the first,
provides for the case where it does not:

> The size a remote reader compares against committed_file_length MUST be
> transport-authoritative (a full-response content length, the complete length of
> a range response, or a size probe); a reader that cannot obtain one MUST probe
> separately or fail the open, and MUST NOT substitute the trailer's
> committed_file_length for the transport size.

A transport that serves suffix ranges without disclosing the complete length — an
HTTP 206 whose `Content-Range` gives `*` as the complete length is the ordinary
case — satisfies neither of §6.4's and §19.1's assertions, and [R-CNT-10] then
obliges a third request or an aborted open. §6.4's own fallback sentence covers a
different case, transports "without suffix-range support", not this one.

Nothing turns on it for conformance: [R-CNT-09] carries no keyword over the
request count, §6.4's Note says "no request count is a conformance property", and
[R-CNT-10] carries the MUSTs. The cost is to an implementer who sizes an open
path from §19.1's step list and finds a transport where step 1 and step 2 do not
in fact collapse — and, more sharply, to a reader that takes §19.1's assertion as
licence to skip the size probe, which [R-CNT-10] forbids in terms.

### adversary-06 — §4.7's Note and §13.1 classify a length prefix on opposite sides of the same field

**Kind:** OBSERVATION. **Location:** §4.7 Note; §13.1, closing paragraph.

§4.7's Note:

> A variable-length field's value includes its length prefix, so a name is
> structural: it determines where the field after it begins.

§13.1, of the fill field — which is a variable-length field with a length prefix,
exactly like a name:

> The fill value is structural (§4.7): it fixes what unstored samples read as,
> and a verifier's acceptance of a tile turns on it, since `[R-SER-05]` fixes
> every padding position's content to it — though **it never affects how any byte
> is located or decoded**; the field's length prefix is §7.4's framing,
> cross-checked against the element size (`[R-CNT-23]`).

Under §4.7's Note the fill field's *value* includes its length prefix, and that
prefix determines where `index_encoding` begins — so the fill's value does affect
where a byte lies. §13.1 says it never does, and rescues itself only by
attributing the prefix to "§7.4's framing" rather than to the value — which is
the opposite of the assignment §4.7's Note makes.

Nothing operational turns on it: both passages conclude that the field is
structural, and they reach it by different routes. Two readings of "value" for a
length-prefixed field are in play — prefix included (§4.7) and prefix excluded
(§13.1) — and I picked §4.7's for the taxonomy question and §13.1's for the
locating question, which is what each passage is actually doing. An implementer
reading §13.1's "never affects how any byte is located" as a statement about the
whole field would mis-parse a layer record if it also believed the prefix could
be recomputed from the type rather than read; [R-CNT-23]'s cross-check catches
that, so the cost is confined to the reasoning and not to the parse.

I note that §4.7's Note reaches for the prefix argument at all when a name is
already structural by the shorter route: [R-ENC-15] makes a duplicate name a
validity error at file scope (F4) and at layer scope (L9), which is "whether the
file, layer or tile is accepted at all" — the third limb of §4.7's own definition.

## 6. Ranking of surviving attacks by how plausibly a real implementation lands on each side

1. **adversary-04** (compactor verification depth). Both sides are what a real
   compactor would naturally do: verify what you move, or verify what you write.
   The construction is small and reachable with an ordinary placement.
2. **adversary-01** (Appendix G inventory). An adopter reading the closing
   paragraph as the checklist ships a non-reproducible writer. Non-normative, but
   the profile exists to be implemented from.
3. **adversary-05** (suffix-range size assertion). Plausible on real HTTP
   deployments; harmless for conformance, costly for an open path.
4. **adversary-03** (L23 instance vs detection point). Falls on the corpus, not
   on an implementation, but the corpus is the instrument.
5. **adversary-02**, **adversary-06**. Wording, no operational side.

## 7. Byte-level verdict

**No byte-level flag.** Every attack I built that reached concrete bytes was
either foreclosed by a sentence I quote above, or landed on a file that is
nonconforming under both readings. The closest thing I have is adversary-04, and
I graded it down on the discriminator the calibration states and on §8.2's
enumeration of the chain; I have set out the construction so that the downgrade
can be checked rather than taken.
