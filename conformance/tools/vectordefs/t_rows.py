# SPDX-License-Identifier: Apache-2.0
"""§21.4 — tile-scope violations (outcome reject-tile). 26 rows, 45 instances.

Every vector here damages seed `pair`'s layer `bad` and leaves layer `ok`
untouched, so each file carries the intact sibling [R-VEC-04] requires: without
it a vector cannot distinguish a reader that scopes its refusal to the tile from
one that rejects the whole file, which [R-CNF-12] permits.

Two levers reach tile scope from a recipe that can only patch named structure
fields:

  * the index entry — offset, length, crc — which is where §15.3's whole
    classification table lives (T6 … T12), and
  * the layer's *declarations*, which decide what the already-stored four bytes
    `01 02 03 04` are supposed to mean. Re-declaring geometry, layout, channel
    type, or codec makes those fixed bytes wrong in a chosen way, which is how
    T2 … T5, T14, T17 and T25 are reached without writing a payload byte.

The second lever is load-bearing because the seed layout map names no tile
payload: `layer[bad].entry[0]` is addressable, the four bytes it points at are
not. That is what forces most of the codec rows into SKIPPED below.
"""
import struct

from tarn_vectors import Vector, Patch

u16 = lambda v: struct.pack("<H", v)
u32 = lambda v: struct.pack("<I", v)
u64 = lambda v: struct.pack("<Q", v)

SENTINEL_HALF = b"\xff" * 8            # §15.2

# Common shapes. Damage is always layer `bad`, disk ordinal 0.
TILE = {"kind": "tile", "layer": "bad", "disk_ordinal": 0}
REPAIR_RECORD = ["directory.crc", "trailer.crc"]
# §15.4's chain: a patched entry changes its segment's bytes, so the segment CRC
# and then crc_of_crc_array must be recomputed. crc_of_crc_array sits in the
# layer record, so the repair propagates into the directory and the trailer.
REPAIR_ENTRY = ["index:bad", "directory.crc", "trailer.crc"]
WELLFORMED = ["entry:bad[0].wellformed"]


def _reader(vid, title, patches, repair, row, rule, breaks=()):
    """A reader-detected reject-tile: refuses tile bad:0, still serves `ok`."""
    return Vector(vid, "pair", title, False, patches=patches, repair=repair,
                  breaks_checksums=list(breaks),
                  row=row, rule=rule, outcome="reject-tile", scope=TILE,
                  detector="reader", detected="tile use",
                  must_not_serve=["tile:bad:0"], serves=["ok"])


def _verifier(vid, title, patches, row, rule):
    """A verifier-detected reject-tile.

    §19.2 places these outside the reader tiers: a reader carries no obligation
    to screen decoded content, so it MAY serve the tile and both layers. The
    file is still nonconforming, and a verifier MUST NOT certify it — the same
    shape TV-0009 uses for the layer-scope reserved-flag rows.
    """
    return Vector(vid, "pair", title, False, patches=patches,
                  repair=REPAIR_RECORD,
                  row=row, rule=rule, outcome="reject-tile", scope=TILE,
                  detector="verifier", detected="certification",
                  must_not_serve=[], serves=["ok", "bad"])


VECTORS = [
    # -- T2 -----------------------------------------------------------------
    # Layer `bad` interleaved, one channel, tile bytes 01 02 03 04. Re-declaring
    # the channel bool makes each byte a bool value: 0x01 is legal, 0x02 0x03
    # 0x04 are not. Fill stays 0x00 (a legal bool fill, so [R-TYP-07] is not
    # tripped) and its length prefix still matches bool's element size 1, so
    # L31 is not tripped either. E == T here, so the tile has no padding
    # positions and T4 cannot co-fire.
    _verifier("TV-0400",
              "layer `bad` redeclared bool: interleaved value bytes 02, 03, 04 "
              "are neither 0x00 nor 0x01",
              [Patch("layer[bad].chan[0].type", u16(1), "bool")],
              "T2", "R-SER-08"),

    # -- T3, six instances --------------------------------------------------
    # Under codec 1 the stored bytes are the decoded image, so a decoded-size
    # mismatch is produced by re-declaring geometry rather than by editing the
    # payload. Every instance keeps grid = 1 in both dimensions so entry_count
    # still equals the addressed-tile count (L22 stays clean), and keeps E == T
    # so no padding position exists to co-violate §14.5.
    _reader("TV-0401",
            "T3 interleaved P·Q, payload longer: `bad` declares tile extents "
            "(1,2) so decoded size is 2, stored length 4",
            [Patch("layer[bad].dim[0].extent", u64(1)),
             Patch("layer[bad].dim[0].tile_extent", u64(1))],
            REPAIR_RECORD, "T3", "R-SER-07"),
    _reader("TV-0402",
            "T3 interleaved P·Q, payload shorter: `bad` declares tile extents "
            "(2,3) so decoded size is 6, stored length 4",
            [Patch("layer[bad].dim[1].extent", u64(3)),
             Patch("layer[bad].dim[1].tile_extent", u64(3))],
            REPAIR_RECORD, "T3", "R-SER-07"),
    _reader("TV-0403",
            "T3 planar numeric P·Bᶜ, payload longer: `bad` planar, tile extents "
            "(1,2), uint8 plane decodes to 2 bytes, stored length 4",
            [Patch("layer[bad].layout", b"\x02", "planar"),
             Patch("layer[bad].dim[0].extent", u64(1)),
             Patch("layer[bad].dim[0].tile_extent", u64(1))],
            REPAIR_RECORD, "T3", "R-SER-07"),
    _reader("TV-0404",
            "T3 planar numeric P·Bᶜ, payload shorter: `bad` planar, tile extents "
            "(2,3), uint8 plane decodes to 6 bytes, stored length 4",
            [Patch("layer[bad].layout", b"\x02", "planar"),
             Patch("layer[bad].dim[1].extent", u64(3)),
             Patch("layer[bad].dim[1].tile_extent", u64(3))],
            REPAIR_RECORD, "T3", "R-SER-07"),
    _reader("TV-0405",
            "T3 packed planar bool ⌈P/8⌉, payload longer: `bad` planar bool, "
            "P = 8 packs to 1 byte, stored length 4",
            [Patch("layer[bad].layout", b"\x02", "planar"),
             Patch("layer[bad].chan[0].type", u16(1), "bool"),
             Patch("layer[bad].dim[1].extent", u64(4)),
             Patch("layer[bad].dim[1].tile_extent", u64(4))],
            REPAIR_RECORD, "T3", "R-SER-07"),
    _reader("TV-0406",
            "T3 packed planar bool ⌈P/8⌉, payload shorter: `bad` planar bool, "
            "P = 34 packs to 5 bytes, stored length 4",
            [Patch("layer[bad].layout", b"\x02", "planar"),
             Patch("layer[bad].chan[0].type", u16(1), "bool"),
             Patch("layer[bad].dim[1].extent", u64(17)),
             Patch("layer[bad].dim[1].tile_extent", u64(17))],
            REPAIR_RECORD, "T3", "R-SER-07"),

    # -- T4, three of four instances ----------------------------------------
    # Shrinking the extents to (1,1) under unchanged tile extents (2,2) turns
    # in-tile ordinals 1, 2, 3 into padding positions. Their stored bytes are
    # 02, 03, 04; the channel's recorded fill is 0x00. Decoded size is unchanged
    # (P is a function of the tile extents alone), so T3 cannot co-fire.
    _verifier("TV-0407",
              "T4 interleaved numeric fill bytes: `bad` extents (1,1), padding "
              "ordinals 1-3 hold 02 03 04, fill is 0x00",
              [Patch("layer[bad].dim[0].extent", u64(1)),
               Patch("layer[bad].dim[1].extent", u64(1))],
              "T4", "R-SER-05"),
    _verifier("TV-0408",
              "T4 planar numeric plane fill bytes: `bad` planar, extents (1,1), "
              "padding ordinals 1-3 hold 02 03 04, fill is 0x00",
              [Patch("layer[bad].layout", b"\x02", "planar"),
               Patch("layer[bad].dim[0].extent", u64(1)),
               Patch("layer[bad].dim[1].extent", u64(1))],
              "T4", "R-SER-05"),
    # Packed plane, P = 32 (tile extents 4x8) so ⌈P/8⌉ = 4 matches the stored
    # length and T3 stays clean, and P mod 8 = 0 so the plane has no pad bits
    # and T5 cannot co-fire. §14.3 packs LSB-first: the set bits of
    # 01 02 03 04 are values 0, 9, 16, 17 and 26. Extents (2,2) make values
    # 0, 1, 8, 9 real, so 16, 17 and 26 are padding positions carrying a set
    # bit where the fill bit is 0.
    _verifier("TV-0409",
              "T4 packed planar bool plane fill bit: `bad` planar bool, tile "
              "extents (4,8), padding values 16, 17, 26 carry set bits",
              [Patch("layer[bad].layout", b"\x02", "planar"),
               Patch("layer[bad].chan[0].type", u16(1), "bool"),
               Patch("layer[bad].dim[0].tile_extent", u64(4)),
               Patch("layer[bad].dim[1].tile_extent", u64(8))],
              "T4", "R-SER-05"),

    # -- T5 -----------------------------------------------------------------
    # P = 25 (tile extents 5x5): ⌈25/8⌉ = 4 still matches the stored length, and
    # P mod 8 = 1 puts the pad bits at bit positions 25-31. Extents (4,5) make
    # values 0-19 real, so the set bits at 0, 9, 16 and 17 are all real values
    # and the padding positions 20-24 are all clear — T4 stays clean. The set
    # bit at 26 is a pad bit, and the channel's fill bit is 0.
    _verifier("TV-0410",
              "T5 pad bit is not the fill bit: `bad` planar bool, P = 25, the "
              "set bit at position 26 lies in the final byte's pad bits",
              [Patch("layer[bad].layout", b"\x02", "planar"),
               Patch("layer[bad].chan[0].type", u16(1), "bool"),
               Patch("layer[bad].dim[0].extent", u64(4)),
               Patch("layer[bad].dim[0].tile_extent", u64(5)),
               Patch("layer[bad].dim[1].extent", u64(5)),
               Patch("layer[bad].dim[1].tile_extent", u64(5))],
              "T5", "R-SER-05"),

    # -- T6 -----------------------------------------------------------------
    # Both halves all-ones with crc = 1: §15.3's second row. The four payload
    # bytes the entry used to address become slack, which [R-CNT-21] leaves
    # unconstrained. checksum_report skips sentinel entries, so this vector
    # breaks nothing it must declare.
    _reader("TV-0411",
            "T6 sentinel entry with crc ≠ 0: `bad` entry 0 is FF×16 with crc 1",
            [Patch("layer[bad].entry[0].offset", SENTINEL_HALF),
             Patch("layer[bad].entry[0].length", SENTINEL_HALF),
             Patch("layer[bad].entry[0].crc", u32(1))],
            REPAIR_ENTRY, "T6", "R-IDX-03"),

    # A note covering TV-0413, TV-0417 and TV-0418, the three vectors that put
    # an out-of-domain value in the entry's *length*: such a length also differs
    # from the tile's decoded size, which under codec 1 is [R-COD-04]'s subject
    # (T14). It cannot be avoided — a length above 2⁶³ can equal no decoded size
    # a sane geometry produces — and it does not mislead: §19.4 classifies the
    # entry at step 4 and only decodes at step 6, and both readings return the
    # same outcome, scope and detection point (reject-tile, tile, tile use).

    # -- T7, two instances --------------------------------------------------
    # §15.3's third row fires before its value-domain rows, and §15.2 exempts
    # the sentinel value from [R-ENC-03]/[R-ENC-04] outright, so the all-ones
    # half does not also make this a T11 or T12 vector.
    _reader("TV-0412",
            "T7 offset is the sentinel, length is not: `bad` entry 0 offset "
            "FF×8, length 4",
            [Patch("layer[bad].entry[0].offset", SENTINEL_HALF)],
            REPAIR_ENTRY, "T7", "R-IDX-03", WELLFORMED),
    _reader("TV-0413",
            "T7 length is the sentinel, offset is not: `bad` entry 0 offset 64, "
            "length FF×8",
            [Patch("layer[bad].entry[0].length", SENTINEL_HALF)],
            REPAIR_ENTRY, "T7", "R-IDX-03", WELLFORMED),

    # -- T8 -----------------------------------------------------------------
    # NOTE: this condition cannot be isolated. Every offset below 16 addresses
    # bytes of the front signature block, so the entry's declared extent always
    # overlaps a structure outside its own layer — F37, [R-CNT-13]. That
    # co-violation is inherent to the row's text, not to this construction, and
    # it does not mask: F37's detector is the verifier at certification, which
    # §19.2 places outside the reader tiers entirely, while §15.3 classifies
    # this entry reject-tile at tile use. Reported as a register finding.
    _reader("TV-0414",
            "T8 non-sentinel entry offset 8, inside the front signature block",
            [Patch("layer[bad].entry[0].offset", u64(8))],
            REPAIR_ENTRY, "T8", "R-IDX-03", WELLFORMED),

    # -- T9 -----------------------------------------------------------------
    # An offset far past the committed file length rather than one straddling
    # F-64: the extent ends past F-64 as the row requires, but claims no live
    # byte, so unlike T8 this instance carries no overlap. offset + length stays
    # under 2^63 - 1 so T12 does not co-fire.
    _reader("TV-0415",
            "T9 non-sentinel entry extent ends past F − 64: offset "
            "0x7FFFFFFFFFFFFF00, length 4",
            [Patch("layer[bad].entry[0].offset", u64(0x7FFFFFFFFFFFFF00))],
            REPAIR_ENTRY, "T9", "R-IDX-03", WELLFORMED),

    # -- T11, two instances -------------------------------------------------
    # Bit 63 set and the value distinct from the all-ones sentinel. §15.3 orders
    # the value-domain row above the sum row, so T12 does not fire first.
    _reader("TV-0416",
            "T11 offset exceeds 2⁶³ − 1: `bad` entry 0 offset 0x8000000000000000",
            [Patch("layer[bad].entry[0].offset", u64(1 << 63))],
            REPAIR_ENTRY, "T11", "R-IDX-03", WELLFORMED),
    _reader("TV-0417",
            "T11 length exceeds 2⁶³ − 1: `bad` entry 0 length 0x8000000000000000",
            [Patch("layer[bad].entry[0].length", u64(1 << 63))],
            REPAIR_ENTRY, "T11", "R-IDX-03", WELLFORMED),

    # -- T12 ----------------------------------------------------------------
    _reader("TV-0418",
            "T12 offset + length exceeds 2⁶³ − 1 with each field in domain: "
            "both 0x4000000000000000",
            [Patch("layer[bad].entry[0].offset", u64(1 << 62)),
             Patch("layer[bad].entry[0].length", u64(1 << 62))],
            REPAIR_ENTRY, "T12", "R-IDX-03", WELLFORMED),

    # -- T14 ----------------------------------------------------------------
    # Codec stays 1, so [R-COD-04]'s equality binds: tile extents (3,2) give
    # decoded size 6 against the entry's length 4. E == T, so no padding
    # position exists and T4 stays clean.
    _reader("TV-0419",
            "T14 codec 1 with entry length 4 against decoded size 6 (`bad` tile "
            "extents (3,2))",
            [Patch("layer[bad].dim[0].extent", u64(3)),
             Patch("layer[bad].dim[0].tile_extent", u64(3))],
            REPAIR_RECORD, "T14", "R-COD-04"),

    # -- T17 ----------------------------------------------------------------
    # Declaring codec 3 over the stored bytes 01 02 03 04, which are not the
    # compressed-frame magic 28 B5 2F FD. A reader that skips the magic check
    # and hands the bytes to a decoder reaches T25 instead — same outcome, same
    # scope, same detection point, so the vector cannot be read as evidence for
    # a different verdict.
    _reader("TV-0420",
            "T17 codec 3 and the stored bytes do not begin with 28 B5 2F FD",
            [Patch("layer[bad].codec", u16(3), "zstd")],
            REPAIR_RECORD, "T17", "R-COD-06"),

    # -- T25, one of three instances ----------------------------------------
    # Declaring codec 4 over 01 02 03 04 read as one raw LZ4 block: token 0x01
    # is zero literals and match length 5, and the next two bytes are the match
    # offset 0x0302 = 770 — a match reaching 770 bytes before an output that has
    # produced nothing. That is T25's lz4 instance verbatim.
    _reader("TV-0421",
            "T25 lz4 block whose match offset 770 reaches past produced output "
            "(codec 4 declared over 01 02 03 04)",
            [Patch("layer[bad].codec", u16(4), "lz4")],
            REPAIR_RECORD, "T25", "R-COD-08"),
]


#: Rows of §21.4 already carrying a vector elsewhere in the corpus. Not gaps:
#: §21.8 asks for at least one vector per row, and duplicating a construction
#: under a second id would put two byte-identical files in the corpus.
COVERED_ELSEWHERE = {
    "T1":  "TV-0008 (vectordefs/slice.py) — entry crc patched away from the "
           "stored bytes.",
    "T10": "TV-0007 (vectordefs/slice.py) — non-sentinel entry with length 0.",
}


#: An honest gap beats a vector that lies. Each entry names what the corpus
#: would need in order to close it.
SKIPPED = {
    "T4 [interleaved bool fill byte]":
        "Not isolable in this seed. Under codec 1 an interleaved bool tile of "
        "the damageable layer must have P·Q = 4, so all four stored bytes "
        "01 02 03 04 occupy sample positions, and 02/03/04 are illegal bool "
        "bytes wherever they land. Any placement that makes one of them a "
        "padding position (T4) simultaneously violates [R-SER-08] (T2), and "
        "any placement that avoids [R-SER-08] leaves no non-fill padding byte. "
        "Needs a seed whose damageable tile carries only 0x00/0x01 bytes.",

    "T13 [deflate stream carrying a previous tile's history window]":
        "Needs a crafted DEFLATE stream in the tile payload. The seed layout "
        "map names no payload bytes, and no seed declares codec 2, so the "
        "stream cannot be placed. zlib(wbits=-15) is available; the blocker is "
        "placement, not generation.",
    "T13 [lz4 block whose match offset reaches before its own output start]":
        "Constructible — TV-0421 is exactly this file — but its condition is "
        "textually the same as T25's lz4 instance, which TV-0421 already "
        "claims. Shipping the same bytes twice under two rows would assert a "
        "distinction the register does not support. Reported as a register "
        "finding: T13's lz4 instance and T25's lz4 instance name one condition.",

    "T15 [zlib RFC 1950 wrapper]": "Needs a real zlib stream in the payload; "
        "payload bytes are unaddressable and no seed declares codec 2.",
    "T15 [gzip RFC 1952 member]": "Same: needs a real gzip member in the payload.",
    "T16": "Needs two concatenated DEFLATE streams in the payload.",
    "T18 [a second concatenated compressed frame]":
        "Needs two real zstd frames in the payload.",
    "T18 [a skippable frame before the frame]": "Needs real zstd frames in the payload.",
    "T18 [a skippable frame after the frame]": "Needs real zstd frames in the payload.",
    "T18 [a skippable frame between two frames]": "Needs real zstd frames in the payload.",
    "T19": "Needs a real zstd frame header carrying a nonzero Dictionary_ID.",
    "T20": "Needs a real zstd frame header with Content_Checksum_flag set.",
    "T21": "Needs a real zstd frame header declaring an oversized Window_Size.",
    "T22": "Needs a real zstd frame header with a Frame_Content_Size field.",
    "T23": "Needs the LZ4 frame magic 04 22 4D 18 and a frame body in the payload.",
    "T24": "Needs a well-formed stream, frame, or block plus trailing bytes in "
           "the payload; under codec 1 the row has no subject, since "
           "[R-COD-04] governs length there instead.",
    "T25 [deflate block type 3 / invalid Huffman table]":
        "Needs a first payload byte of 0x07 (BFINAL = 1, BTYPE = 11); the "
        "stored bytes are fixed at 01 02 03 04.",
    "T25 [corrupt zstd block header]":
        "Needs the zstd frame magic followed by a corrupt block header; a "
        "payload lacking the magic is T17, which TV-0420 already claims.",

    "T26 [planar numeric: channel element size]":
        "Not expressible in this seed. The damageable layer's only channel is "
        "uint8, so the mandated shuffle stride is 1 and the filter is the "
        "identity — the file cannot distinguish a reader that applies the "
        "inverse from one that ignores it, which is the only thing a filter "
        "vector tests. The channel's type cannot be widened either: the fill "
        "field is two bytes (prefix + one byte) and a recipe cannot grow it, so "
        "any wider type trips L31 instead. Needs a seed whose non-`ok` layer "
        "carries a multi-byte channel.",
    "T26 [interleaved: sample stride Q]":
        "Same: Q = 1 for the damageable layer, so the mandated shuffle is the "
        "identity.",
    "T26 [packed planar bool: identity s = 1]":
        "The mandated stride here IS the identity, so a file declaring filter 2 "
        "over a wrongly-shuffled plane is byte-for-byte a T4 or T5 file with "
        "the filter field changed, and no verifier can attribute the break to "
        "the stride (§21.7 says so outright). Skipped rather than shipped as a "
        "vector claiming a verdict nothing can distinguish.",
}
