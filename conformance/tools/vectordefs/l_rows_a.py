# SPDX-License-Identifier: Apache-2.0
"""§21.3 rows L1–L25: layer-scope violations, outcome reject-layer.

Encoding domains (L1–L3), name rules (L4–L10), sub-record framing
(L11–L15, L20, L25), extent slots (L16–L19), and the declaration
cross-checks that sit between them (L21–L24).

Every vector damages layer `bad` of the `pair` seed and leaves layer `ok`
untouched, so `serves=["ok"]` supplies the intact sibling `[R-VEC-04]`
requires: without it no vector can tell a reader that scopes its refusal
from one that rejects the whole file, which `[R-CNF-12]` permits.

Two construction notes that recur below.

**Whole-record patches.** Most rows here are a single field's value and
patch a single named field. The name rules and the framing rows are not:
a name's length prefix decides where every later field starts, so a vector
for "the name is empty" that patched only the prefix would desynchronize
the whole parse and test `[R-CNT-18]`'s framing instead. Those vectors
patch `layer[bad].record` — still a name, never an offset — rebuilding the
117 bytes from the same field order §7.4 fixes, and compensating the byte
the defect adds or removes in a *dimension name*, which no rule constrains
beyond §4.6. The rebuild asserts its own length at import, so a
miscounted field is a build failure rather than a silent reframing.

**Downstream checksums under a redirected pointer.** A vector that
corrupts `bad`'s extent slot leaves the tile-index region's bytes and
CRCs exactly as built, but `checksum_report` follows the slot and
recomputes over whatever the slot now names. Those entries are declared
in `breaks_checksums` with a note: §19.2 puts the slot's validity at
layer access and the index chain at tile use, so the checksum the report
finds broken sits *after* the row this vector claims, and no conforming
reader reaches it. That is the opposite of masking.
"""
import struct

from tarn_build import crc32c
from tarn_vectors import Vector, Patch, SEEDS

u8 = lambda v: struct.pack("<B", v)
u16 = lambda v: struct.pack("<H", v)
u32 = lambda v: struct.pack("<I", v)
u64 = lambda v: struct.pack("<Q", v)

BIT63 = 1 << 63                      # first value outside §4.2's domain

_BLOB, _MAP = SEEDS["pair"]()


def _seed(field: str) -> bytes:
    """The bytes the seed put in a field, so a rebuild can carry them
    forward instead of restating them (ADR-0049's restatement rule)."""
    o, w = _MAP[field]
    return bytes(_BLOB[o:o + w])


CRC_ARR = _seed("layer[bad].crc_of_crc_array")   # unchanged: region untouched
IDX_OFF, IDX_LEN = _MAP["layer[bad].index_region"]
REC_LEN = _MAP["layer[bad].record"][1]           # 117
INLINE = REC_LEN - 24                            # 93
SENTINEL = b"\xff" * 16 + b"\x00" * 4            # §15.2


# --------------------------------------------------------------------------
# Rebuilding layer `bad`'s record, field by field in §7.4's order.
# --------------------------------------------------------------------------

def _lead(lname=b"\x03bad", layout=1, lin=1, codec=1, filt=1, alignment=0,
          slab=0, slab_alignment=0, rank=2, chan_count=1,
          rank_bytes=None, cc_bytes=None):
    """name … C. `rank_bytes`/`cc_bytes` exist only for L3, which is about
    a field written at a width §7.4 does not fix."""
    return (lname + u8(layout) + u16(lin) + u16(codec) + u16(filt)
            + u64(alignment) + u64(slab) + u64(slab_alignment)
            + (u8(rank) if rank_bytes is None else rank_bytes)
            + (u16(chan_count) if cc_bytes is None else cc_bytes))


def _dim(nm: bytes, extent: int, tile: int) -> bytes:
    return nm + u64(extent) + u64(tile)          # nm carries its length prefix


def _chan(nm: bytes, typ: int, fill: bytes) -> bytes:
    return nm + u16(typ) + u8(len(fill)) + fill


def _tail(entry_count=1, index_encoding=1, crc_arr=CRC_ARR) -> bytes:
    return u8(index_encoding) + u64(entry_count) + crc_arr


def _record(inline: bytes, *, il=INLINE, eo=IDX_OFF, el=IDX_LEN) -> bytes:
    """A layer record: §7.2's 24-byte header, flags MU=1 PE=1 per §7.3."""
    rec = struct.pack("<HHIQQ", 1, 0b11, il, eo, el) + inline
    assert len(rec) == REC_LEN, f"record is {len(rec)} B, must be {REC_LEN}"
    return rec


DIM_Y = _dim(b"\x01y", 2, 2)
DIM_X = _dim(b"\x01x", 2, 2)
CHAN_V = _chan(b"\x01v", 6, b"\x00")             # uint8, fill 0x00


def L(id_, title, row, rule, patches, *, repair=("directory.crc", "trailer.crc"),
      detected="layer access", breaks=(), named=True, detector="reader"):
    """One reject-layer vector against layer `bad`.

    `named=False` is for the four vectors whose defect *is* the name field:
    the layer cannot be identified by a name it does not validly carry, so
    the scope names its ordinal in the directory's record sequence.
    """
    scope = ({"kind": "layer", "name": "bad"} if named
             else {"kind": "layer", "record_ordinal": 1,
                   "note": "the layer's name field is the defect"})
    return Vector(id_, "pair", title, False, patches=list(patches),
                  repair=list(repair), row=row, rule=rule,
                  outcome="reject-layer", scope=scope, detector=detector,
                  detected=detected, must_not_serve=[
                      "layer:bad" if named else "layer:#1"],
                  serves=["ok"], breaks_checksums=list(breaks))


VECTORS = [

    # -- L1 — a u64 field of a layer record above 2^63 - 1 -----------------
    # `[R-ENC-03]`. Four of the row's six named instances; the extent-slot
    # two are in SKIPPED. Each of these files also fails a later check that
    # reads the same field — a grid count from an out-of-domain extent, the
    # index cross-checks from an out-of-domain entry_count — but reaching
    # that check means *acting on* the value, which §4.2 forbids outright
    # and `[R-ENC-05]` forbids before validation. The domain gate is
    # therefore the first check a conforming reader can perform on the
    # field, and the later ones are unreachable, not masked.
    L("TV-0200", "layer `bad` dimension extent E0 = 2^63 (instance: dimension extent Ei)",
      "L1", "R-ENC-03", [Patch("layer[bad].dim[0].extent", u64(BIT63))]),
    L("TV-0201", "layer `bad` tile extent T0 = 2^63 (instance: tile extent Ti)",
      "L1", "R-ENC-03", [Patch("layer[bad].dim[0].tile_extent", u64(BIT63))]),
    L("TV-0202", "layer `bad` entry_count = 2^63 (instance: entry_count)",
      "L1", "R-ENC-03", [Patch("layer[bad].entry_count", u64(BIT63))]),
    # The layer record's own extent slot. Both halves are u64 fields of the
    # layer record, so `[R-ENC-03]`'s domain gate reaches them exactly as it
    # reaches the declaration fields above. The breaks are the same two
    # TV-0224 declares: `checksum_report` recomputes the index chain over
    # whatever bytes the corrupted slot now names, and §19.2 puts the slot's
    # validity at layer access, ahead of either.
    L("TV-0924", "layer `bad` extent_offset = 2^63 "
      "(instance: layer record extent_offset)",
      "L1", "R-ENC-03", [Patch("layer[bad].extent_offset", u64(BIT63))],
      breaks=["index:bad.segment_crcs", "entry:bad[0].wellformed"]),
    L("TV-0925", "layer `bad` extent_length = 2^63 "
      "(instance: layer record extent_length)",
      "L1", "R-ENC-03", [Patch("layer[bad].extent_length", u64(BIT63))],
      breaks=["index:bad.segment_crcs", "entry:bad[0].wellformed"]),
    # S != 0 obliges a power-of-two A_slab in 1 … 2^62 (`[R-CNT-23]`, L30),
    # so A_slab = 1 is set alongside: not a second defect but the value the
    # slab declaration requires, leaving S's domain as the only violation.
    L("TV-0203", "layer `bad` slab run length S = 2^63 (instance: slab run length S)",
      "L1", "R-ENC-03", [Patch("layer[bad].slab", u64(BIT63)),
                         Patch("layer[bad].slab_alignment", u64(1))]),

    # -- L2 — a declaration-derived sum or product above 2^63 - 1 ----------
    # `[R-ENC-04]`, every contributing field in domain. Six of the row's ten
    # instances; the other four are in SKIPPED with the arithmetic that puts
    # them out of reach.
    #
    # N overflows while E and T stay in domain. The reader cannot compare
    # entry_count against N without computing N, so L22 is unreachable here
    # rather than a second defect. P is unchanged at 4, so the stored tile's
    # decoded size still matches its length.
    L("TV-0204", "layer `bad` N = prod ceil(Ei/Ti) = 2^122 (instance: N)",
      "L2", "R-ENC-04", [Patch("layer[bad].dim[0].extent", u64(1 << 62)),
                         Patch("layer[bad].dim[1].extent", u64(1 << 62))]),
    # P = 2^62 * 2 = 2^63, one past the domain, with both grid counts 1 so
    # N = entry_count = 1 and §15.1's region size still checks out.
    L("TV-0205", "layer `bad` P = prod Ti = 2^63, the first value past the domain "
      "(instance: P)",
      "L2", "R-ENC-04", [Patch("layer[bad].dim[0].tile_extent", u64(1 << 62))]),
    # extent_offset + extent_length: both halves in domain at 2^62, their sum
    # 2^63 out of it. The sum is the quantity §7.2 forms to place the extent
    # inside the file, so `[R-ENC-04]` bites before any placement row can —
    # a bound cannot be compared against a sum that has no value.
    L("TV-0927", "layer `bad` extent slot (2^62, 2^62): both halves in domain, "
      "their sum 2^63 (instance: extent_offset + extent_length)",
      "L2", "R-ENC-04",
      [Patch("layer[bad].extent_offset", u64(1 << 62)),
       Patch("layer[bad].extent_length", u64(1 << 62))],
      breaks=["index:bad.segment_crcs", "entry:bad[0].wellformed"]),
    # C·N: planar, C = 4, N = 2^62. Both in domain; their product is not,
    # and it is the addressed-tile count itself, so `[R-CNT-17]`'s
    # comparison is the computation that overflows.
    L("TV-0206", "layer `bad` planar with C=4, N=2^62: C*N = 2^64 (instance: C*N)",
      "L2", "R-ENC-04",
      [Patch("layer[bad].record", _record(
          _lead(layout=2, rank=1, chan_count=4)
          + _dim(b"\x01y", 1 << 62, 1)
          + _chan(b"\x01a", 6, b"\x00") + _chan(b"\x01b", 6, b"\x00")
          + _chan(b"\x01c", 6, b"\x00") + _chan(b"\x01d", 6, b"\x00")
          + _tail()))]),
    # P·Q: interleaved, P = 2^60, one uint64 channel so Q = 8. P and C are
    # in domain and P·C = 2^60 is too — only the interleaved sample stride's
    # product leaves it (§14.2).
    L("TV-0207", "layer `bad` interleaved P=2^60 with Q=8: P*Q = 2^63 (instance: P*Q)",
      "L2", "R-ENC-04",
      [Patch("layer[bad].record", _record(
          _lead(rank=1)
          + _dim(b"\x0c" + b"y" * 12, 2, 1 << 60)
          + _chan(b"\x01v", 9, bytes(8))
          + _tail()))]),
    # P·B^c: the same geometry declared planar, where §14.3 sizes a numeric
    # plane as P·B^c. P·C = 2^60 stays in domain, so this is the plane
    # product alone.
    L("TV-0208", "layer `bad` planar P=2^60 with B^c=8: P*B^c = 2^63 (instance: P*B^c)",
      "L2", "R-ENC-04",
      [Patch("layer[bad].record", _record(
          _lead(layout=2, rank=1)
          + _dim(b"\x0c" + b"y" * 12, 2, 1 << 60)
          + _chan(b"\x01v", 9, bytes(8))
          + _tail()))]),
    # The index region's declared size: entry_count = N = 2^60 exactly, so
    # `[R-CNT-17]`'s count cross-check passes and only its size formula
    # overflows. Geometry is re-cut to keep P = 4, so the stored tile's
    # decoded size is unchanged.
    L("TV-0209", "layer `bad` entry_count = 2^60: entry_count*20 + ceil(/2^16)*4 "
      "overflows (instance: index region size)",
      "L2", "R-ENC-04", [Patch("layer[bad].dim[0].extent", u64(1 << 60)),
                         Patch("layer[bad].dim[0].tile_extent", u64(1)),
                         Patch("layer[bad].dim[1].extent", u64(1)),
                         Patch("layer[bad].dim[1].tile_extent", u64(4)),
                         Patch("layer[bad].entry_count", u64(1 << 60))]),

    # -- L3 — a layer-scope field at a width this specification does not fix
    # `[R-ENC-06]`. Channel count C written as u8 rather than u16, the
    # record's total size held at 117 by one extra byte of dimension name.
    # A width deviation necessarily desynchronizes the parse — that is how
    # it is detectable at all — so a reader takes C as u16 = 0x0201 = 513
    # and is one byte out of step from there, overrunning the payload on
    # the very first dimension name (which reads as 121 bytes long).
    # Outcome and scope are L24's, which is why `[R-ENC-06]` is the rule
    # and L24 is not: the defect is the width, the overrun is its symptom.
    L("TV-0210", "layer `bad` writes channel count C as u8 instead of u16",
      "L3", "R-ENC-06",
      [Patch("layer[bad].record", _record(
          _lead(cc_bytes=u8(1))
          + _dim(b"\x02yy", 2, 2) + DIM_X + CHAN_V + _tail()))]),

    # -- L4, L6, L7 — the layer record's own name -------------------------
    # `[R-ENC-11]`, `[R-ENC-12]`. Detected at open: §19.1 step 4 parses and
    # checks every layer record's name while building the layer table, so
    # these are the layer-scope rows a reader owes before any layer access.
    L("TV-0211", "layer `bad` name is ill-formed UTF-8 (03 62 FF 64)",
      "L4", "R-ENC-11", [Patch("layer[bad].name", b"\x03b\xffd")],
      detected="open", named=False),
    L("TV-0214", "layer `bad` name has length prefix 0 (empty name)",
      "L6", "R-ENC-12",
      [Patch("layer[bad].record", _record(
          _lead(lname=b"\x00")
          + _dim(b"\x04yyyy", 2, 2) + DIM_X + CHAN_V + _tail()))],
      detected="open", named=False),
    L("TV-0215", "layer `bad` name contains U+0001, a code point in U+0000-U+001F",
      "L7", "R-ENC-12", [Patch("layer[bad].name", b"\x03b\x01d")],
      detected="open", named=False),

    # -- L5, L8, L9, L10 — dimension and channel entry names --------------
    # Two instances each, one per entry kind. The channel-name vectors patch
    # `layer[bad].chan[0].name` where the byte count is unchanged; every
    # dimension-name vector rebuilds the record, because the builder's field
    # map names a dimension's extent and tile extent but not its name.
    L("TV-0212", "layer `bad` channel name is ill-formed UTF-8 (instance: channel entry name)",
      "L5", "R-ENC-11", [Patch("layer[bad].chan[0].name", b"\x01\xff")]),
    L("TV-0213", "layer `bad` dimension name is ill-formed UTF-8 "
      "(instance: dimension entry name)",
      "L5", "R-ENC-11",
      [Patch("layer[bad].record", _record(
          _lead() + _dim(b"\x01\xff", 2, 2) + DIM_X + CHAN_V + _tail()))]),

    L("TV-0216", "layer `bad` dimension name has length prefix 0 "
      "(instance: dimension entry name)",
      "L8", "R-ENC-12",
      [Patch("layer[bad].record", _record(
          _lead() + _dim(b"\x00", 2, 2) + _dim(b"\x02xx", 2, 2)
          + CHAN_V + _tail()))]),
    L("TV-0217", "layer `bad` channel name has length prefix 0 "
      "(instance: channel entry name)",
      "L8", "R-ENC-12",
      [Patch("layer[bad].record", _record(
          _lead() + _dim(b"\x02yy", 2, 2) + DIM_X
          + _chan(b"\x00", 6, b"\x00") + _tail()))]),

    L("TV-0218", "layer `bad` dimension name contains U+0001 "
      "(instance: dimension entry name)",
      "L9", "R-ENC-12",
      [Patch("layer[bad].record", _record(
          _lead() + _dim(b"\x01\x01", 2, 2) + DIM_X + CHAN_V + _tail()))]),
    L("TV-0219", "layer `bad` channel name contains U+0001 "
      "(instance: channel entry name)",
      "L9", "R-ENC-12", [Patch("layer[bad].chan[0].name", b"\x01\x01")]),

    # `[R-ENC-15]`: comparison is raw bytes, no normalization (`[R-ENC-13]`).
    L("TV-0220", "layer `bad` declares two dimensions both named `y` "
      "(instance: dimension entry name)",
      "L10", "R-ENC-15",
      [Patch("layer[bad].record", _record(
          _lead() + DIM_Y + _dim(b"\x01y", 2, 2) + CHAN_V + _tail()))]),
    # Two channels needs rank 1 to fit; E0 = T0 = 2 keeps N = entry_count = 1
    # and P·Q = 2·2 = 4, still exactly the stored tile's length.
    L("TV-0221", "layer `bad` declares two channels both named `v` "
      "(instance: channel entry name)",
      "L10", "R-ENC-15",
      [Patch("layer[bad].record", _record(
          _lead(rank=1, chan_count=2)
          + _dim(b"\x0d" + b"y" * 13, 2, 2)
          + CHAN_V + _chan(b"\x01v", 6, b"\x00") + _tail()))]),

    # -- L15 — a sub-record that does not fit the inline payload -----------
    # `[R-CNT-12]` via `[R-CNT-18]`. Instance 1 only: the 24-byte header
    # truncated at the payload end. The record is re-cut to rank 1 with
    # E0 = T0 = 4 — P·Q = 4, the stored tile's length unchanged — freeing
    # 18 bytes, into which a sub-record header begins and stops short.
    L("TV-0222", "layer `bad` sub-record header truncated at the payload end, "
      "18 of 24 bytes (instance: sub-record header)",
      "L15", "R-CNT-12",
      [Patch("layer[bad].record", _record(
          _lead(rank=1) + _dim(b"\x01y", 4, 4) + CHAN_V + _tail()
          + struct.pack("<HHIQ", 0x0002, 0b10, 0, 256) + b"\x18\x00"))]),

    # -- L16, L17, L18 — the layer record's extent slot --------------------
    # `[R-CNT-13]`. One instance each; the sub-record instance of all three
    # is in SKIPPED. A malformed slot on a layer record is reject-layer, not
    # reject-file (§7.2), which is what separates these from F33–F35.
    #
    # Half-zero slot: length 0 with a nonzero offset. The file also fails
    # L23's size formula, unavoidably — the formula's subject is a slot that
    # has already parsed as a slot — so the shape check is the finer
    # description and the one this vector claims.
    L("TV-0223", "layer `bad` extent slot is (68, 0), exactly one half zero "
      "(instance: layer record extent slot)",
      "L16", "R-CNT-13", [Patch("layer[bad].extent_length", u64(0))]),
    # The mirror: offset zero, length nonzero. (0, 0) means no extent
    # (`[R-CNT-13]`), so it is the *pairing* that is invalid, and each half
    # is its own instance because the two files differ.
    L("TV-0926", "layer `bad` extent slot is (0, 24), exactly one half zero "
      "(instance: layer record extent_offset)",
      "L16", "R-CNT-13", [Patch("layer[bad].extent_offset", u64(0))],
      breaks=["index:bad.segment_crcs", "entry:bad[0].wellformed"]),
    # Offset 8 puts the tile index inside the front signature block. The two
    # declared breaks are `checksum_report` recomputing the index chain over
    # the bytes the corrupted slot now names; §19.2 places the slot's
    # validity at layer access and the index chain at tile use, so a
    # conforming reader rejects before reaching either.
    L("TV-0224", "layer `bad` extent_offset = 8, inside the front signature block "
      "(instance: layer record extent slot)",
      "L17", "R-CNT-13", [Patch("layer[bad].extent_offset", u64(8))],
      breaks=["index:bad.segment_crcs", "entry:bad[0].wellformed"]),
    L("TV-0225", "layer `bad` extent 376+24 = 400 reaches past F-64 = 384 "
      "(instance: layer record extent slot)",
      "L18", "R-CNT-13", [Patch("layer[bad].extent_offset", u64(376))],
      breaks=["index:bad.segment_crcs", "entry:bad[0].wellformed"]),

    # -- L19 — two structures of one layer claiming the same bytes ---------
    # `[R-CNT-13]` with §15.3's verifier row. Entry 0 is repointed at the
    # first four bytes of the tile-index region itself: a stored extent
    # overlapping its own layer's index region, which §7.2 makes
    # reject-layer rather than reject-file. The entry's crc is set over
    # those four bytes so the overlap is the only defect — every checksum
    # in the file still verifies, which is exactly why this row needs a
    # verifier and no reader is obliged to detect it.
    L("TV-0226", "layer `bad` stored tile [68,72) overlaps its own tile-index region "
      "(instance: tile-index region)",
      "L19", "R-CNT-13",
      [Patch("layer[bad].entry[0].offset", u64(IDX_OFF)),
       Patch("layer[bad].entry[0].length", u64(4)),
       Patch("layer[bad].entry[0].crc", u32(crc32c(u64(IDX_OFF)[:4])))],
      repair=["index:bad", "directory.crc", "trailer.crc"],
      detector="verifier", detected="certification"),

    # -- L21 — per-tile alignment and a slab both declared -----------------
    # `[R-CNT-16]`, the one row here about a combination rather than a
    # value. Entry 0 is made a sentinel first: `bad`'s stored tile sits at
    # offset 64, which no A >= 512 divides, so any file declaring A over a
    # stored tile would also violate `[R-SLB-01]`'s invariant (L41). With no
    # stored tile the alignment and slab invariants are vacuous and the
    # mutual exclusion is the only thing wrong. A sentinel entry is defined
    # behavior (§21.6), not a second defect.
    L("TV-0227", "layer `bad` declares both A = 512 and S = 1",
      "L21", "R-CNT-16",
      [Patch("layer[bad].entry[0]", SENTINEL),
       Patch("layer[bad].alignment", u64(512)),
       Patch("layer[bad].slab", u64(1)),
       Patch("layer[bad].slab_alignment", u64(1))],
      repair=["index:bad", "directory.crc", "trailer.crc"]),

    # -- L22 — entry_count against the geometry-derived count --------------
    # `[R-CNT-17]`. E1 = 4 over T1 = 2 makes G1 = 2 and N = 2 while
    # entry_count stays 1. L23's size formula reads entry_count, not N, so
    # 1*20 + 4 = 24 still matches the region and this is the count
    # cross-check alone.
    L("TV-0228", "layer `bad` addresses N = 2 tiles but declares entry_count = 1",
      "L22", "R-CNT-17", [Patch("layer[bad].dim[1].extent", u64(4))]),

    # -- L23 — the index region's declared size ----------------------------
    # `[R-CNT-17]`, three files for the three alternatives the row's text
    # states. Each keeps entry_count equal to the geometry-derived count so
    # that L22 is satisfied and only the size relation fails.
    L("TV-0229", "layer `bad` extent_length = 20, not entry_count*20 + 4 = 24 "
      "(instance: extent_length)",
      "L23", "R-CNT-17", [Patch("layer[bad].extent_length", u64(20))]),
    L("TV-0230", "layer `bad` extent slot (0, 0) with entry_count = 1 "
      "(instance: extent_offset)",
      "L23", "R-CNT-17", [Patch("layer[bad].extent_offset", u64(0)),
                          Patch("layer[bad].extent_length", u64(0))]),
    # E0 = 0 makes the layer legitimately empty (`[R-GEO-02]`), so
    # entry_count = 0 is the correct count and crc_of_crc_array = 0 is what
    # `[R-CNT-23]` then requires (L28) — neither is the defect. The defect
    # is the extent slot still claiming a 24-byte region.
    L("TV-0231", "layer `bad` has entry_count = 0 but a nonzero extent slot "
      "(instance: entry_count)",
      "L23", "R-CNT-17", [Patch("layer[bad].dim[0].extent", u64(0)),
                          Patch("layer[bad].entry_count", u64(0)),
                          Patch("layer[bad].crc_of_crc_array", u32(0))]),

    # -- L24 — a declared region outside the inline payload ----------------
    # `[R-CNT-18]`. One file per named region. inline_length stays 93 in all
    # four, so the directory's own record sequence still parses with no
    # residue and the file-scope framing row (F32) stays out of it.
    L("TV-0232", "layer `bad` name declares 200 bytes, past the 93-byte payload "
      "(instance: leading fixed fields)",
      "L24", "R-CNT-18", [Patch("layer[bad].name", b"\xc8bad")], named=False),
    L("TV-0233", "layer `bad` declares rank 3 with room for two dimension entries "
      "(instance: d dimension entries)",
      "L24", "R-CNT-18", [Patch("layer[bad].rank", u8(3))]),
    L("TV-0234", "layer `bad` declares C = 9 with room for one channel entry "
      "(instance: C channel entries)",
      "L24", "R-CNT-18", [Patch("layer[bad].channel_count", u16(9))]),
    # The dimension and channel entries fit exactly; the 13 trailing fixed
    # bytes start at payload byte 85 and need 98.
    L("TV-0235", "layer `bad` trailing fixed fields start at 85 and need 13 of the "
      "remaining 8 bytes (instance: trailing fixed fields)",
      "L24", "R-CNT-18",
      [Patch("layer[bad].record", _record(
          _lead() + DIM_Y + _dim(b"\x06xxxxxx", 2, 2) + CHAN_V
          + _tail()[:8]))]),
]


# --------------------------------------------------------------------------
# Rows and instances this module does not build, and why. An honest gap
# beats a vector that claims a row it cannot reach (§24, ADR-0046: the
# corpus is evidence, and a missing vector is a gap in it, never a licence
# to skip the check — `[R-VEC-03]`).
#
# Keys are register row ids; where only some of a row's instances are
# missing, the key names the instance.
# --------------------------------------------------------------------------

SKIPPED = {
    # ---- no constructible file can carry a well-formed sub-record --------
    # The directory region is 236 bytes of record sequence and cannot grow:
    # dir_offset/dir_length are trailer fields, but the bytes between the
    # index regions and the pre-trailer pad belong to other structures, and
    # the pad is not an addressable field. Layer `ok` must stay intact for
    # [R-VEC-04], costing 119 bytes, so layer `bad` has 117. Its smallest
    # conforming record — a 1-byte name, rank 1, one uint8 channel — is 97
    # bytes, leaving 20. A sub-record's header alone is 24 (§7.2). Every row
    # below therefore needs a seed carrying a layer user-metadata
    # sub-record; the `meta` seed carries a *top-level* one, which is a
    # different container. This is the largest single gap in §21.3's
    # layer-scope coverage and it is a corpus-tooling gap, not a spec one.
    "L11": "user-metadata sub-record with extent slot (0,0): needs a 25-byte "
           "sub-record; the pair seed's layer record has 20 spare bytes and "
           "no seed carries a layer sub-record.",
    "L12": "sub-record extent_length < 5: same 20-byte ceiling.",
    "L13": "sub-record inline_length != 1: same 20-byte ceiling.",
    "L14": "sub-record of type 0x0000: a complete 24-byte header does not "
           "fit in the 20 spare bytes.",
    "L15/sub-record inline_length": "needs a complete 24-byte header plus an "
           "inline_length that overruns; only 20 bytes are available.",
    "L15/trailing residue": "needs a complete sub-record followed by leftover "
           "bytes (>= 25). Separately, this instance is not distinguishable "
           "from L15's truncated-header instance whenever fewer than 24 "
           "bytes remain: the same bytes are both.",
    "L20": "two user-metadata sub-records: needs 50 bytes.",
    "L25": "a sub-record containing a record: needs 48 bytes.",
    "L16/sub-record extent slot": "no sub-record is constructible (see L11).",
    "L17/sub-record extent slot": "no sub-record is constructible (see L11).",
    "L18/sub-record extent slot": "no sub-record is constructible (see L11).",
    "L19/layer sub-record extents": "no sub-record is constructible (see L11).",

    # ---- the builder's checksum_report cannot walk these files -----------
    # checksum_report follows a layer record's extent slot without gating on
    # §4.2's domain — the thing [R-ENC-05] forbids a reader to do — so it
    # reads the segment-CRC array past the end of the blob and raises
    # struct.error ("unpack requires a buffer of 4 bytes"), from an
    # out-of-domain offset and from an out-of-domain length alike. Neither
    # vector can be built while the isolation check runs on every file. The
    # files themselves are well defined; this is a limit of the harness, and
    # the fix is a domain gate in checksum_report ahead of its index walk.
    "L1/extent_offset": "checksum_report dereferences the slot before "
           "checking §4.2's domain and raises struct.error.",
    "L1/extent_length": "checksum_report derives an entry count from the "
           "declared region size and reads the segment-CRC array past the "
           "end of the file; same struct.error.",
    "L2/extent_offset + extent_length": "either half large enough to make "
           "the sum overflow triggers one of the two failures above.",

    # ---- instances that no file can distinguish --------------------------
    # These are findings against the register, not gaps in the tooling.
    "L2/max disk ordinal (C-1)*N + (N-1)": "identically C*N - 1, so it "
           "exceeds 2^63-1 only when C*N does. No file distinguishes it "
           "from the C*N instance (TV-0206); the instance is redundant.",
    "L2/V = P*C": "Q is the sum of the channels' element sizes, so Q >= C "
           "and P*Q >= P*C: any file where P*C overflows has P*Q "
           "overflowing too. Planar avoids Q but makes the addressed-tile "
           "count C*N >= 2, which needs an index region the seed cannot "
           "carry. Not independently realizable.",
    "L2/N*P": "requires N >= 2, hence entry_count >= 2 and an index region "
           "of at least 44 bytes; `pair` gives layer `bad` 24. With N = 1, "
           "N*P is the P instance's file (TV-0205). Constructible on a seed "
           "whose damage layer has two or more addressed tiles.",
}
