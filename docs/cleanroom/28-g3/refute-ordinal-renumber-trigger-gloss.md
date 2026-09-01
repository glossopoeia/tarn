# Refute pass — R28 finding: "§20.3 step 4 glosses ordinal renumbering as triggered by a geometry change"

## Disclosure

Read exactly one file: `/Users/robertkleffner/Documents/GitHub/tarn-first-draft/spec/tarn.md`,
via `sed -n` and `awk`/`grep` over that file only. No docs/, no conformance/, no registry.json,
no git, no web. Ran one local Python script,
`priv-ordinal-renumber-trigger-gloss/ord_crc_probe.py`, which reads no files (CRC-32C arithmetic
only, validated against §4.5's `"123456789"` -> 0xE3069283 check vector and the zero-byte 0).
Scratch files confined to `.../r28-refute/priv-ordinal-renumber-trigger-gloss/`.

Unrequested context appeared before I began: a project-instruction block, a user-identity/date
block, an environment block naming the repo/branch and recent commit subject lines, an MCP-server
instruction block, and a skills listing. None of it is the specification; I disregarded all of it
and did not use any of it as evidence.

## Sections opened

§2.1 (via §21.1's cross-reference discipline), §2.3 [R-CNF-02]/[R-CNF-03]/[R-CNF-04]/[R-CNF-05]/
[R-CNF-06]/[R-CNF-11]/[R-CNF-13], §2.4 (opening), §3.1, §3.2 [R-MDL-01]/[R-MDL-02], §3.3,
§4.5 [R-ENC-09]/[R-ENC-10], §4.6 [R-ENC-11]–[R-ENC-15], §4.7 [R-ENC-16], §7.4 [R-CNT-23]/
[R-CNT-16]/[R-CNT-17]/[R-CNT-18] and its worked-record Example, §9.1 [R-LIF-01], §9.2 [R-LIF-02],
§11.1 [R-GEO-01]/[R-GEO-02] and its Rationale, §11.2 [R-GEO-03], §11.4 [R-GEO-05]/[R-GEO-06] and
its Example, §12.1 [R-TYP-01]/[R-TYP-02], §14.1 [R-SER-01]/[R-SER-06], §14.2 [R-SER-02]/[R-SER-08],
§15.1 [R-IDX-01], §15.2 [R-IDX-02], §15.3 [R-IDX-03], §15.4 [R-IDX-04]/[R-IDX-05],
§19.4 [R-RDR-04] and its two Notes, §20.1 [R-WRT-01], §20.2 [R-WRT-02], §20.3 [R-WRT-03]/
[R-WRT-04] in full (steps 1-6, the bar, the shrink paragraph, the cost Note, and the
"three shapes a commit takes" Example), §20.4 [R-WRT-05]/[R-WRT-08] and its table and Rationale,
§20.5 [R-WRT-07]/[R-WRT-09] and its Example, §21.1 [R-ERR-02] (row-vs-rule discipline),
§21.6, §21.7 [R-ERR-01], plus targeted greps for "channel", "re-declar", "declared order",
"reference array", "unique" across the whole file.

## Verdict

BYTE_LEVEL_ESTABLISHED.

## The two readings

§20.3 step 4, inside "An appender MUST, in order:":

> every other entry byte-identical at its **disk-ordinal position**
> (a geometry change renumbers ordinals wherever `[R-GEO-06]` moves them)

Reading A (the reporter's and all three triage passes'): a carried-forward entry belongs to a
*named* channel; when that channel's declared index changes, [R-GEO-06] moves the entry.

Reading B: a carried-forward entry belongs to the tile (c, s) — c the channel *index*, s the
spatial ordinal — and [R-GEO-06]'s c·N + s is a function of c, s and N alone. A channel-set edit
that leaves the grid alone leaves N alone, so no entry moves. The parenthetical is then exactly
right and complete: ordinals renumber iff N moves, i.e. on a geometry change.

Reading B is not a misreading nobody would hold. Four rules individuate a planar tile's channel
positionally and none by name across generations:

- [R-GEO-06]: "**c · N + s** for a planar layer (§14), where c is the channel's index (§3.1)".
- §3.1: "a channel's **index** is its 0-based position in that order".
- [R-SER-01]: "the tile with disk ordinal c · N + s (§11.4) carries exactly the values of channel c".
- [R-IDX-01]: "The entry for the tile with disk ordinal k (§11.4) is the k-th entry, at region
  byte 20·k"; §19.4 step 2 computes "c · N + s per requested channel c planar".

And the identity the growth case itself uses is (c, s): to renumber on growth you decompose
position k of the old region as (k div N_old, k mod N_old) and re-lay it at c·N_new + s. Under
that same identity a channel-set edit moves nothing. Nothing in the document ever ties a channel's
identity across generations to its name. §20.3's own Example (c) sanctions a directory-only
channel-declaration edit ("changing a channel's fill value on a layer with no padding position and
no pad bit ... Only the directory is re-emitted"), and step 4 itself says "A layer whose record
alone changes keeps its extent slot, pointing at the existing region".

So the sentence under audit is the only guidance a writer has on when to recompute ordinals, and
it supports B on its face while four careful readers this round took A.

## Construction 1 — the swap commit (both outputs conforming; emitted bytes differ)

Prior generation G_n. One planar layer L:
layout 2 (planar), linearization 1, codec 1 (none), filter 1 (none), A = 0, S = 0, A_slab = 0,
rank d = 1, dimension `x` with E = 2, T = 1, channel count C = 2:
channel `a` uint8 (type 6, B = 1) fill 0x00, channel `b` uint8 fill 0xFF.

Arithmetic: G_x = ceil(2/1) = 2, N = 2, P = prod T = 1. Addressed-tile count = C·N = 4, so
entry_count = 4 and, under index_encoding 1, extent_length = 4·20 + ceil(4/2^16)·4 = 84
([R-CNT-17]). E = 2 = 2·T, so the grid covers the extent exactly: **no padding position**, so
[R-SER-05]/T4 and T5 are vacuous and the two channels' differing fills are unreachable. Planar
numeric decoded size = P·B = 1 byte per tile; both channels have B = 1, so every tile's decoded
size is 1 whichever channel it carries. Codec 1 requires stored length = decoded size.

Disk ordinals ([R-GEO-06]): a -> 0, 1; b -> 2, 3.
All four tiles stored, one byte each, at offsets 16, 17, 18, 19 (>= 16, so [R-IDX-03]'s
front-block row is clear), holding 0x11, 0x22, 0x33, 0x44. Index region R at offset 20, length 84.

Entries (offset u64 LE, length u64 LE, crc u32 LE), CRC-32C per [R-ENC-09]:

    e0  10 00 00 00 00 00 00 00  01 00 00 00 00 00 00 00  3d 17 48 b0   crc(0x11)=0xB048173D
    e1  11 00 00 00 00 00 00 00  01 00 00 00 00 00 00 00  78 ad fb 93   crc(0x22)=0x93FBAD78
    e2  12 00 00 00 00 00 00 00  01 00 00 00 00 00 00 00  14 e9 ce 71   crc(0x33)=0x71CEE914
    e3  13 00 00 00 00 00 00 00  01 00 00 00 00 00 00 00  f2 d9 9c d4   crc(0x44)=0xD49CD9F2

G_n's region: [e0 e1 e2 e3] then the one segment CRC.
  segment CRC over the 80 entry bytes = 0x42ED63A5, stored `a5 63 ed 42`
  crc_of_crc_array = CRC-32C over those 4 bytes = 0xBCA93E21, stored `21 3e a9 bc`

**The commit K**, stated wholly in the format's own vocabulary and identical under both readings:
emit the next generation whose layer record for L carries channel entries in the order [b, a]
instead of [a, b]. Store no tile, supersede no tile, add/drop no record, change no dimension,
extent, tile extent, layout, codec, filter, alignment or slab.

K is permitted under both readings. §20.3's bar asks whether the declaration change alters, for a
tile L stores in the superseded generation, "the set of padding positions (§11.3) and the content
`[R-SER-05]` fixes there, the decoded size, the byte offset of any sample within the decoded tile
image, or the codec and filter". There are no padding positions; every tile's decoded size is
P·B = 1 either way; a planar tile's sample offset is k·B = k either way; codec and filter are
layer fields and unchanged. Nothing fires under name-identity or under index-identity.

**Reading A output (File A).** The entries for channel `b` (now index 0) take ordinals 0 and 1;
channel `a`'s (now index 1) take 2 and 3. So the index content changes, the region is re-emitted
in full at a new placement ([R-LIF-01]), and the layer record's extent slot is re-pointed:

    region at F: [e2 e3 e0 e1] + segment CRC
      first 20 bytes at offset F:  12 00 00 00 00 00 00 00 01 00 00 00 00 00 00 00 14 e9 ce 71
      segment CRC = 0x8391B634, stored `34 b6 91 83`
      crc_of_crc_array = 0x807683CB, stored `cb 83 76 80`
    L's extent slot = (F, 84); old R at (20, 84) becomes slack ([R-CNT-21])
    committed_file_length = F + 84 + |dir| + 4 + pad + 64

**Reading B output (File B).** No entry moved, so the index content did not change: step 4's
"A layer whose record alone changes keeps its extent slot, pointing at the existing region"
applies, and this is Example (c)'s shape — only the directory is re-emitted:

    nothing appended at F but the directory
    L's extent slot = (20, 84), unchanged; crc_of_crc_array = 0xBCA93E21, unchanged
    committed_file_length = F + |dir| + 4 + pad + 64

**Where they differ, in bytes.**
1. At offset F: File A holds `12 00 00 00 00 00 00 00` (e2's offset field); File B holds the first
   byte of the new directory's first record header.
2. Inside the directory, in the same field of the same record: L's crc_of_crc_array is
   `cb 83 76 80` in File A and `21 3e a9 bc` in File B.
3. L's extent-slot offset field: F in File A, 20 in File B.
4. committed_file_length differs by 84 plus the pad delta (84 mod 64 != 0, so the pads differ too).

**Both files are conforming.** entry_count 4 = C·N and extent_length 84 in both ([R-CNT-17]);
every entry well-formed under §15.3 (offsets >= 16, lengths nonzero, extents below F - 64, crcs
matching their unmoved payload bytes); segment CRC and crc_of_crc_array consistent in both
([R-IDX-04]); every stored tile's decoded payload length is exactly the decoded size 1
([R-SER-07]); no padding position, so §14.5 and [R-SER-05] have nothing to check; no slab or
alignment declaration. A conforming reader MUST accept both ([R-CNF-03]).

**And each reading bars the other's file.** Under A, File B leaves e0 at ordinal 0 where A
requires e2 — "every other entry byte-identical at its **disk-ordinal position**" is violated.
Under B, File A puts e2 at ordinal 0 where B requires e0 — the same clause violated. Neither file
is reachable from G_n by commit K under the other reading. The reference arrays differ: at x = 0
File A's sample tuple is (channel 0 = 0x33, channel 1 = 0x11); File B's is (0x11, 0x33).

## Construction 2 — the same edit with unequal element sizes (a MUST NOT / MAY fork)

Same layer, but channel `a` uint8 (B = 1) and channel `b` uint16 (type 7, B = 2). Then a's tiles
have decoded size 1 and b's 2. G_n stores e0, e1 (length 1) at ordinals 0, 1 and e2, e3
(length 2) at ordinals 2, 3.

Commit K' = swap the channel entries to [b, a].

- Under reading A the bar tests b's tiles (decoded size P·B_b = 2, unchanged) and a's tiles
  (P·B_a = 1, unchanged): permitted, and the appender emits the region [e2 e3 e0 e1], which is a
  conforming file — position 0 now expects decoded size 2 and e2's tile is 2 bytes.
- Under reading B the declaration change alters, for the prior-generation stored tile at ordinal 0,
  its decoded size (P·1 -> P·2). That is one of the four effects the bar names, so
  "A commit MUST NOT change a layer's declarations in a way that alters ..." forbids K' outright;
  the operation is "a new layer, or a whole-file rewrite under a fresh file_id".

So a conforming file — File A' — is one that reading A permits this appender to produce and
reading B forbids it to produce at all. That is the discriminator's own shape: the disputed file is
conforming, and only one reading permits an actor to produce it.

## Why the three downgrades do not hold

- "The parenthetical states a case, not a closed trigger set; the governing clause admits one
  reading." The governing clause admits one reading only once you have fixed what individuates an
  entry across the commit. Reading B satisfies it literally: the entry at position k is the entry
  for tile (k div N, k mod N), it is byte-identical, and [R-GEO-06] over the new declarations puts
  that tile back at k because c, s and N are all unchanged. The clause does not decide the
  question; the parenthetical is the only text that speaks to it, and it says "a geometry change".
- "§21.7 fixes that the ordinal mappings are satisfied whatever values a tile carries, so
  conformance is identical under both readings." §21.7 is an account of *detection*, and its own
  subject is obligations that bind while lacking a witness — it names "§20.3 step 4's bar on a
  declaration change" as one. Undetectable is not permitted. [R-CNF-06] binds an updater to
  "every writer requirement for the bytes it produces", and step 4 is inside "An appender MUST, in
  order". §21.7 is what makes both files *conforming*, which is what the construction needs; it
  says nothing about which one the appender is obliged to emit.
- "What separates the two files is the caller's intended reference array, which the format does not
  adjudicate." Not here. Commit K is stated entirely in format vocabulary — a specific new channel
  entry list, no tile stored or superseded. No external intent is consulted to see that one reading
  appends an 84-byte index region and re-points an extent slot and the other appends neither.
- "[R-CNF-05]'s second sentence licenses divergence." Per the standing discriminator it licenses
  divergence within what the rules leave open. If the rules leave this open, that openness is the
  byte-level ambiguity; if they close it toward B, the reporter's repair moves the bytes. The only
  branch that is not byte-level is "the text unambiguously means A", and [R-GEO-06], [R-SER-01],
  [R-IDX-01], §19.4 step 2 and the parenthetical itself all cut the other way.
- §21.1's row-vs-rule tiebreak is not in play: no register row is involved, and §21.1's
  completeness clause expressly does not reach §21.7.

## Constructions tried and killed

1. Planar channel *count* growth, new channel appended last (C: 1 -> 2, geometry fixed). Killed:
   c·N + s is independent of C, so ordinal c·N+s is unchanged for every pre-existing tile under
   both readings and the new channel's N sentinels land at N..2N-1 either way. Identical files.
2. Interleaved layer, channel reorder. Killed by §20.3's bar under both readings: [R-SER-02] makes
   F_c = sum of B_j over j < c, so a reorder with unequal element sizes moves "the byte offset of
   any sample within the decoded tile image" for every stored tile, and the commit is barred.
   With equal element sizes F_c still moves for any C >= 2 with distinct channels... and where all
   B are equal the offsets coincide, but an interleaved tile carries every channel, so the entry
   never moves at all (interleaved disk ordinal is s, with no c term). No fork either way.
3. Planar swap with unequal element sizes, asking for a *reader* fork. Killed as byte-level in the
   naive form: reading B's file would put a 1-byte tile at an ordinal expecting decoded size 2,
   which is an [R-SER-07] violation (T3/T14), so [R-CNF-05] bars that file under both readings —
   exactly the shape the project's discriminator rejects. Survives only in the re-cast form of
   Construction 2, where reading B bars the *commit* rather than emitting a bad file.
4. Planar swap where the two channels differ in fill and the layer *has* a padding position.
   Killed: reading B's file then holds the wrong channel's fill at a padding position, T4 fires,
   [R-SER-05] is violated, and [R-CNF-05] bars the file under both readings. This is why
   Construction 1 uses E = 2, T = 1 (grid covers the extent exactly, no padding position), which
   lets the fills differ freely and still leaves both files conforming.
5. Channel removal from the front of a planar layer (C: 3 -> 2). Not killed, but weaker than
   Construction 1 and I set it aside: under reading B two of the six prior entries have no position
   in a 4-entry region at all, so reading B is under-determined rather than cleanly opposed, and an
   argument from an under-determined reading is the shape that has failed here before.
6. Compaction path (§20.5) rather than append. Killed: [R-WRT-07] — "The output's reference arrays
   MUST equal the live generation's bit for bit ([R-MDL-02]): compaction changes where bytes live,
   never what a layer denotes" — and a compactor changes no declaration, so no ordinal question
   arises.
7. Degenerate layer with a zero extent (entry_count 0, extent slot (0,0)). Killed: no entries
   exist to place, and §11.1's "A layer that stores no tile ... MAY be re-declared freely" makes
   the whole channel-set question moot there.
8. One-tile layer (N = 1, C = 2, planar). Not killed — it is Construction 1 shrunk, with ordinals
   0 and 1 swapping — but the 2x2 version above gives a longer region and a cleaner CRC contrast,
   so I report that one.
9. §20.4's record-drop path (MU = 0, PE = 0 sub-record dropped rather than modified). Killed: a
   tile-index entry is no record §20.4's table licenses dropping (§20.5's text says so in terms),
   and dropping a record does not touch ordinals.
