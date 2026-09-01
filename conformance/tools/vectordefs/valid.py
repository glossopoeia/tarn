# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Rob Kleffner and contributors
"""The positive corpus — §24 `[R-VEC-03]`.

`[R-ERR-02]` buys coverage of the register: every way a file can be wrong.
It buys nothing about the files that are *right*. This module is the other
half `[R-VEC-03]` asks for — every sentinel, every boundary value, and every
hard limit of `[R-ERR-05]` at its stated bound — plus a vector for every
row of §21.6, the conditions that are **not** violations, that one file can
distinguish from another (two cannot; SKIPPED says why).

Those last are the only vectors in the corpus a broken reader can fail by
being too strict. An invalid vector catches a reader that serves data it
should have refused; nothing in the register catches a reader that refuses
a conforming file. A reader that rejects an ignore-lane flag bit, an
extent-0 layer, a sentinel index, or an unknown `tarn.` metadata key is the
nonconforming party (§21.6), and only a conforming file whose expectation is
"this reads" can say so.

Every vector here is `conforming=True` and therefore carries no register row:
a row would put a violation in the manifest that the file does not contain.
The governing rule is cited in each vector's title instead, which is what the
manifest records for a conforming file.

Seeds. Most boundaries are declarations the five stock seeds do not make —
rank 255, 65,535 channels, a dimension extent of 2⁶³ − 1 — and a Patch cannot
change a field's width, let alone add dimension entries. So this module
registers its own seeds. It adds keys to SEEDS and LAYERS and edits no file
but this one; every name is `valid_`-prefixed and every registration is a
setdefault, so sibling modules authored concurrently cannot collide with it.
"""

import struct
import sys
import zlib
from compression import zstd

from tarn_vectors import Vector, Patch, SEEDS
from tarn_build import (Channel, Layer, Record, TRAILER_MAGIC,
                        build_with_layout, crc32c)

u16 = lambda v: struct.pack("<H", v)
u32 = lambda v: struct.pack("<I", v)
u64 = lambda v: struct.pack("<Q", v)

MAX63 = (1 << 63) - 1


# --------------------------------------------------------------------------
# Seed registration
# --------------------------------------------------------------------------

def _hosts():
    """Every loaded copy of tarn_vectors.

    The runner executes tarn_vectors.py as `__main__`, so this module's
    `from tarn_vectors import SEEDS` imports it a *second* time and binds the
    second copy's dict. A registration made through that binding is invisible
    to the SEEDS the runner actually indexes. Registering into both copies is
    the whole of the workaround, and it is why every registration below is a
    setdefault: it can run twice.
    """
    out, seen = [], set()
    for nm in ("__main__", "tarn_vectors"):
        mod = sys.modules.get(nm)
        if (mod is not None and id(mod) not in seen
                and hasattr(mod, "SEEDS") and hasattr(mod, "LAYERS")):
            seen.add(id(mod))
            out.append(mod)
    return out


def _reg(name, fn, layers):
    """Register a seed and the layer-name order `verify` needs to walk it."""
    for h in _hosts():
        h.SEEDS.setdefault(name, fn)
        h.LAYERS.setdefault(name, layers)


def _reg_layers(name, layers):
    for h in _hosts():
        h.LAYERS.setdefault(name, layers)


# tarn_vectors.LAYERS ships entries for `minimal` and `pair` only; the three
# other stock seeds have none, so verify() raises KeyError on any vector built
# from them. Supplying them here is additive and idempotent — the names are
# each seed's layers in directory order, which is the order build() emits.
_reg_layers("sparse", ["ok", "sparse"])
_reg_layers("planar", ["planar", "ok"])           # seed_planar builds [pl, ok]
_reg_layers("meta", ["ok"])


def _ok():
    """seed `pair`'s intact layer, byte for byte, so OK_CONTENT applies.

    Recording real decoded content is `[R-VEC-02]`'s minimum, and OK_CONTENT
    is the only content the manifest knows how to state. A seed that carries
    this layer unmodified gets `serves=["ok"]`; one that does not says so.
    """
    return Layer("ok", extents=(2, 3), tile_extents=(2, 3),
                 channels=[Channel("t", 12)],
                 tiles=[struct.pack("<6I", 0x3F800000, 0x80000000, 0x7FC00001,
                                    0xC0000000, 0x00000000, 0x7F800000)])


# -- an all-sentinel layer: the zero declarations, and §15.2's entry --------

def _seed_sparse_all():
    """`sp`'s four addressed tiles are all unstored — the whole index is
    sentinels. It carries A = 0, S = 0, A_slab = 0, the "none declared"
    encoding of all three, and it is the seed the alignment and slab
    boundaries patch: with no stored tile, `[R-SLB-01]`'s and `[R-SLB-03]`'s
    placement invariants hold vacuously, so the declaration is exercised
    without the builder needing to control byte placement."""
    sp = Layer("sp", extents=(4, 4), tile_extents=(2, 2),
               channels=[Channel("v", 6, b"\x2A")], tiles=[None] * 4)
    return build_with_layout([_ok(), sp])


_reg("valid_sparse_all", _seed_sparse_all, ["ok", "sp"])


# -- geometry ---------------------------------------------------------------

def _seed_empty_dim():
    """A layer with a dimension of extent 0: N = 0, entry_count 0, extent
    slot (0, 0), crc_of_crc_array 0 (§7.4, `[R-GEO-02]`). With no tile and no
    index region there is nothing to place before the directory, so this
    also puts dir_offset at its floor of 16 (§6.2) while the directory
    still carries a record — Appendix A's file reaches the same floor with
    an empty one."""
    e = Layer("empty", extents=(0, 4), tile_extents=(2, 2),
              channels=[Channel("v", 6)], tiles=[])
    return build_with_layout([e])


def _seed_big_extent():
    """E₀ = T₀ = 2⁶³ − 1: the u64 domain ceiling of `[R-ENC-03]`, with every
    derived product (N = 1, P = 2⁶³ − 1, N·P, P·Q) exactly at `[R-ENC-04]`'s
    bound rather than over it. The single addressed tile is unstored, which
    is what keeps the file small and what keeps it conforming: a stored tile
    under codec 1 would owe `[R-COD-04]` a length equal to the decoded size."""
    big = Layer("big", extents=(MAX63,), tile_extents=(MAX63,),
                dim_names=("k",), channels=[Channel("v", 6, b"\x00")],
                tiles=[None])
    return build_with_layout([_ok(), big])


def _seed_rank(d, nm):
    dims = tuple(_cname(i, 2) for i in range(d))
    ly = Layer(nm, extents=(1,) * d, tile_extents=(1,) * d, dim_names=dims,
               channels=[Channel("v", 6)], tiles=[b"\x00"])
    return build_with_layout([_ok(), ly])


_ALPHA = bytes(range(0x21, 0x7F)).decode()   # 94 single-byte names, no U+0020


def _cname(i, width):
    """A distinct `width`-byte name per index, base 94 over printable ASCII.

    Names must be unique within their scope (`[R-ENC-15]`) and the two big
    vectors need 255 and 65,535 of them; decimal names would add ~190 KiB of
    committed bytes to the channel-count vector for no coverage.
    """
    out = []
    for _ in range(width):
        out.append(_ALPHA[i % 94])
        i //= 94
    return "".join(out)


def _seed_chan(c, nm, stored):
    """An interleaved layer of `c` uint8 channels: Q = C, P = 1."""
    chans = [Channel(_cname(i, 2 if c <= 8836 else 3), 6) for i in range(c)]
    tiles = [bytes(range(256)) * (c // 256) + bytes(range(c % 256))] if stored \
        else [None]
    ly = Layer(nm, extents=(1,), tile_extents=(1,), dim_names=("k",),
               channels=chans, tiles=tiles)
    return build_with_layout([_ok(), ly])


def _seed_layers64():
    ls = [_ok()] + [Layer(f"l{i:02d}", extents=(1,), tile_extents=(1,),
                          dim_names=("k",), channels=[Channel("v", 6)],
                          tiles=[bytes([i])]) for i in range(64)]
    return build_with_layout(ls)


def _seed_multisegment():
    """entry_count = 65,537: two segments, and the boundary between them.

    §15.4 fixes segment s over entries [s·2¹⁶, min((s+1)·2¹⁶, entry_count)).
    Segment 0 here is full and all sentinels, so its stored CRC is exactly
    `[R-IDX-05]`'s constant 0xEECB3BB2 — the one place the corpus can show
    that the constant is a computed value a writer MAY skip computing, never
    a value a reader matches against. Segment 1 covers one entry, which is
    stored, so its CRC MUST be computed: the partial-segment rule and the
    full-segment shortcut in one file.

    This is `[R-VEC-03]`'s scaled substitute for §21.9's 2³² addressed-tile
    guarantee; the bound itself is in SKIPPED with its arithmetic.
    """
    seg = Layer("seg", extents=(65537,), tile_extents=(1,), dim_names=("k",),
                channels=[Channel("v", 6)], tiles=[None] * 65536 + [b"\x01"])
    return build_with_layout([_ok(), seg])


_reg("valid_empty_dim", _seed_empty_dim, ["empty"])
_reg("valid_big_extent", _seed_big_extent, ["ok", "big"])
_reg("valid_rank32", lambda: _seed_rank(32, "r32"), ["ok", "r32"])
_reg("valid_rank255", lambda: _seed_rank(255, "r255"), ["ok", "r255"])
_reg("valid_chan4096", lambda: _seed_chan(4096, "c4096", True), ["ok", "c4096"])
_reg("valid_chan65535", lambda: _seed_chan(65535, "c65535", False),
     ["ok", "c65535"])
_reg("valid_layers64", _seed_layers64,
     ["ok"] + [f"l{i:02d}" for i in range(64)])
_reg("valid_multisegment", _seed_multisegment, ["ok", "seg"])


# -- names ------------------------------------------------------------------

def _seed_names_max():
    """Every name in the layer at `[R-ERR-05]`'s hard limit of 255 bytes —
    the ceiling a u8 length prefix forces (`[R-ENC-12]`). Layer, dimension,
    and channel names are three separate parses, so one file exercises all
    three at the bound."""
    ly = Layer("a" * 255, extents=(2,), tile_extents=(2,),
               dim_names=("b" * 255,), channels=[Channel("c" * 255, 6)],
               tiles=[b"\x01\x02"])
    return build_with_layout([_ok(), ly])


def _seed_names_edge():
    """The name value-space edges: a 1-byte name (the `[R-ENC-12]` floor),
    U+0020 (the lowest code point the C0 exclusion leaves), U+007F (DEL,
    excluded by no rule), and U+10FFFF (the highest code point there is, four
    bytes of UTF-8). Byte comparison is the only comparison (`[R-ENC-13]`),
    so a reader that normalizes or rejects these fails here."""
    ly = Layer("z", extents=(2,), tile_extents=(2,),
               dim_names=("\u007f\U0010ffff",),
               channels=[Channel(" ", 6)], tiles=[b"\x01\x02"])
    return build_with_layout([_ok(), ly])


_reg("valid_names_max", _seed_names_max, ["ok", "a" * 255])
_reg("valid_names_edge", _seed_names_edge, ["ok", "z"])


# -- types, fills, padding --------------------------------------------------

_EDGE_FILL = {                      # one boundary bit pattern per type
    1: b"\x01",                                     # bool true
    2: b"\x80",                                     # int8 min
    3: b"\x00\x80",                                 # int16 min
    4: b"\xff\xff\xff\x7f",                         # int32 max
    5: b"\x00\x00\x00\x00\x00\x00\x00\x80",         # int64 min
    6: b"\xff",                                     # uint8 max
    7: b"\xff\xff",                                 # uint16 max
    8: b"\x00\x00\x00\x00",                         # uint32 zero
    9: b"\xff\xff\xff\xff\xff\xff\xff\xff",         # uint64 max
    10: b"\x00\x7c",                                # float16 +Inf
    11: b"\xc0\x7f",                                # bfloat16 qNaN
    12: b"\x01\x00\xc0\x7f",                        # float32 NaN, payload 1
    13: b"\x00\x00\x00\x00\x00\x00\x00\x80",        # float64 -0.0
}


def _seed_fills():
    """One channel of every one of §12.1's thirteen types, each fill an edge
    bit pattern — NaN with a payload, −0.0, +Inf, the signed minima, the
    unsigned maxima — and the layer's one addressed tile unstored.

    Fill is returned bit-exactly (`[R-TYP-04]`, `[R-TYP-06]`) and a sentinel
    entry is the one thing that produces it (`[R-TYP-08]`, `[R-TYP-09]`), so
    every sample of this layer is a fill byte pattern a reader must hand back
    unaltered. A reader that quiets a NaN or collapses −0.0 fails here and
    nowhere in the register.
    """
    ch = [Channel(f"f{t:02d}", t, _EDGE_FILL[t]) for t in range(1, 14)]
    ly = Layer("fills", extents=(1,), tile_extents=(1,), dim_names=("k",),
               channels=ch, tiles=[None])
    return build_with_layout([_ok(), ly])


def _seed_types():
    """The same thirteen types, stored: an interleaved sample of every core
    type, in declared channel order, at element size, little-endian
    (`[R-TYP-01]`, `[R-SER-02]`). Q = 47, P = 1, so the tile is one sample
    and its byte offsets are the §14.2 table read straight down."""
    ch = [Channel(f"f{t:02d}", t, _EDGE_FILL[t]) for t in range(1, 14)]
    tile = b"".join(_EDGE_FILL[t] for t in range(1, 14))
    ly = Layer("types", extents=(1,), tile_extents=(1,), dim_names=("k",),
               channels=ch, tiles=[tile])
    return build_with_layout([_ok(), ly])


def _seed_pad():
    """T₀ = T₁ = 4 over extents (2, 2): `[R-GEO-01]` permits a tile extent
    above its dimension's extent, and the grid is then one padded tile. Of
    the 16 sample positions four are real and twelve are padding, and every
    padding position carries the channel's recorded fill (`[R-SER-05]`) —
    the content a verifier checks and a reader never returns
    (`[R-GEO-04]`)."""
    fill = 0x2A
    tile = bytearray([fill] * 16)
    for u0 in range(2):                       # in-tile ordinal u0·T₁ + u1
        for u1 in range(2):
            tile[u0 * 4 + u1] = 1 + u0 * 2 + u1
    ly = Layer("pad", extents=(2, 2), tile_extents=(4, 4),
               channels=[Channel("v", 6, bytes([fill]))], tiles=[bytes(tile)])
    return build_with_layout([_ok(), ly])


def _seed_padbits():
    """A packed planar bool plane with P = 12, so P mod 8 ≠ 0 and the final
    byte carries four pad bits. Value k is true for even k, packed LSB-first
    (`[R-SER-03]`), so byte 0 is 0x55 and byte 1 carries values 8–11 in bits
    0–3 as 0b0101; pad bits 4–7 carry the channel's fill bit, which is 1
    here (`[R-SER-05]`), making byte 1 0xF5 — a plane whose pad bits are
    *not* zero, so a reader or verifier that assumes zero padding is
    caught."""
    ly = Layer("bits", extents=(3, 4), tile_extents=(3, 4), layout=2,
               channels=[Channel("m", 1, b"\x01")],
               tiles=[bytes([0x55, 0xF5])])
    return build_with_layout([_ok(), ly])


def _seed_mixed_inter():
    """An interleaved layer mixing a numeric channel and a bool channel:
    Q = 2, the bool value one byte of 0x00 or 0x01 (`[R-SER-08]`), never
    packed. §21.6 makes the combination defined in either layout and
    `[R-SER-09]` forbids rejecting a layer for it."""
    tile = bytes([7, 1, 8, 0, 9, 1, 10, 0])
    ly = Layer("mix", extents=(2, 2), tile_extents=(2, 2),
               channels=[Channel("u", 6, b"\x00"), Channel("m", 1, b"\x01")],
               tiles=[tile])
    return build_with_layout([_ok(), ly])


_reg("valid_fills", _seed_fills, ["ok", "fills"])
_reg("valid_types", _seed_types, ["ok", "types"])
_reg("valid_pad", _seed_pad, ["ok", "pad"])
_reg("valid_padbits", _seed_padbits, ["ok", "bits"])
_reg("valid_mixed_inter", _seed_mixed_inter, ["ok", "mix"])


# -- codecs and the filter --------------------------------------------------

def _deflate(data, level):
    c = zlib.compressobj(level, zlib.DEFLATED, -15)      # raw RFC 1951
    return c.compress(data) + c.flush()


def _seed_deflate():
    """Codec 2 in both directions. `shrink` stores 64 zero bytes as a raw
    RFC 1951 stream far shorter than the decoded image; `grow` stores 64
    bytes at level 0, whose stored blocks make the payload *longer* than
    what it decodes to. §21.6: under a compressing codec the two lengths
    differ, expected in either direction, and only codec 1 owes equality
    (`[R-COD-04]`, `[R-COD-08]`)."""
    small = bytes(64)
    big = bytes((i * 167 + 13) & 0xFF for i in range(64))
    a = Layer("shrink", extents=(8, 8), tile_extents=(8, 8), codec=2,
              channels=[Channel("v", 6)], tiles=[_deflate(small, 9)])
    b = Layer("grow", extents=(8, 8), tile_extents=(8, 8), codec=2,
              channels=[Channel("v", 6)], tiles=[_deflate(big, 0)])
    return build_with_layout([_ok(), a, b])


def _seed_zstd():
    """Codec 3 at every constraint `[R-COD-06]` states: the frame magic
    28 B5 2F FD, exactly one frame and no skippable frame, dictionary ID 0,
    the content-checksum flag clear, a declared window no larger than the
    64-byte decoded size, and a Frame_Content_Size that is present and equal
    to it. The single-segment frame libzstd emits for a small input sets
    Window_Size = Frame_Content_Size, which is the equality case of the
    window rule — the bound, not an interior value."""
    dec = bytes(64)
    frame = zstd.compress(dec)
    assert frame[:4] == b"\x28\xb5\x2f\xfd" and (frame[4] >> 5) & 1 == 1
    assert (frame[4] >> 2) & 1 == 0 and frame[4] & 3 == 0
    ly = Layer("z", extents=(8, 8), tile_extents=(8, 8), codec=3,
               channels=[Channel("v", 6)], tiles=[frame])
    return build_with_layout([_ok(), ly])


def _shuffle(image, s):
    """§17.3: byte i of group j moves to offset i·n + j, n = L/s."""
    n = len(image) // s
    return bytes(image[j * s + i] for i in range(s) for j in range(n))


def _seed_filter2():
    """Filter 2 at each of the three strides `[R-COD-10]` names: the sample
    stride Q for an interleaved tile, the channel's element size for a
    planar numeric plane, and s = 1 — the identity — for a packed bool
    plane. Length is unchanged by the shuffle, so codec 1's equality
    (`[R-COD-04]`) still holds and the stored bytes are the filtered image
    verbatim (§17.1)."""
    inter = bytes(range(20))                       # P=4, Q=5 (float32+uint8)
    plane = bytes(range(8))                        # P=4, B=2
    a = Layer("sh_i", extents=(2, 2), tile_extents=(2, 2), filter=2,
              channels=[Channel("t", 12), Channel("u", 6)],
              tiles=[_shuffle(inter, 5)])
    b = Layer("sh_p", extents=(2, 2), tile_extents=(2, 2), layout=2, filter=2,
              channels=[Channel("w", 7)], tiles=[_shuffle(plane, 2)])
    c = Layer("sh_b", extents=(2, 4), tile_extents=(2, 4), layout=2, filter=2,
              channels=[Channel("m", 1, b"\x00")], tiles=[b"\xa5"])
    return build_with_layout([_ok(), a, b, c])


def _seed_codec4_bound():
    """Codec 4 declared on a layer whose per-tile decoded size is exactly
    0x7E000000 — `[R-COD-07]`'s hard limit, which forbids *exceeding* it.
    The addressed tile is unstored, so the file that carries the boundary
    declaration is 512 bytes rather than two gigabytes."""
    ly = Layer("lz", extents=(0x7E000000,), tile_extents=(0x7E000000,),
               dim_names=("k",), codec=4, channels=[Channel("v", 6)],
               tiles=[None])
    return build_with_layout([_ok(), ly])


_reg("valid_deflate", _seed_deflate, ["ok", "shrink", "grow"])
_reg("valid_zstd", _seed_zstd, ["ok", "z"])
_reg("valid_filter2", _seed_filter2, ["ok", "sh_i", "sh_p", "sh_b"])
_reg("valid_codec4_bound", _seed_codec4_bound, ["ok", "lz"])


# -- records, metadata, slack ----------------------------------------------

def _seed_meta_zstd():
    """A top-level user-metadata document under encoding 2 (§18.2): one RFC
    8878 frame before the extent's terminal CRC-32C, no skippable frame, no
    second frame, dictionary ID 0, content-checksum flag clear. §18.2 drops
    the window and content-size constraints `[R-COD-06]` states against a
    tile's declared decoded size — a document has none."""
    doc = b'{"tarn.creator":"tarn-vectors 1.0-rc","tarn.title":"zstd"}'
    frame = zstd.compress(doc)
    assert frame[:4] == b"\x28\xb5\x2f\xfd" and (frame[4] >> 2) & 1 == 0
    ext = frame + u32(crc32c(frame))
    return build_with_layout([_ok()], [Record(0x0002, inline=b"\x02",
                                              extent=ext)])


def _seed_no_layers():
    """Zero layers with a non-empty directory (§21.6, `[R-CNT-14]`).
    Appendix A's file is the empty-directory case; this one proves the
    record sequence may carry records while naming no layer at all, which a
    reader that assumes at least one layer record will not survive."""
    doc = b'{"tarn.title":"no layers"}'
    return build_with_layout([], [Record(0x0002, inline=b"\x01",
                                         extent=doc + u32(crc32c(doc)))])


def _seed_slack():
    """`_ok()` alone, with the pre-trailer pad named so a recipe can address
    it. The pad is slack (§5.2, §6.2): under no checksum, of unconstrained
    content, claimed by no coverage class (`[R-CNT-21]`)."""
    blob, layout = build_with_layout([_ok()])
    d0, dl = layout["directory"]
    layout["pretrailer_pad"] = (d0 + dl, len(blob) - 64 - (d0 + dl))
    return blob, layout


def _seed_mimic():
    """A stored tile whose 64 bytes are a byte-perfect trailer image — magic,
    version 1.0, directory bounds, a 64-multiple committed length, a
    nonzero file_id, zero reserved bytes, and a correct CRC-32C over its
    first 60. Nothing enumerates slack and no reader scans for trailers,
    so the lookalike is inert (`[R-LIF-06]`, §21.6); only a recovery tool
    sees it, and §9.6 makes it re-verify its output whole."""
    t = (TRAILER_MAGIC + struct.pack("<HHI", 1, 0, 0) + u64(16)
         + u64(4) + u64(128) + u64(0xDEADBEEFCAFEF00D) + b"\x00" * 12)
    t += u32(crc32c(t))
    assert len(t) == 64
    ly = Layer("mimic", extents=(8, 8), tile_extents=(8, 8),
               channels=[Channel("v", 6)], tiles=[t])
    return build_with_layout([_ok(), ly])


_reg("valid_meta_zstd", _seed_meta_zstd, ["ok"])
_reg("valid_no_layers", _seed_no_layers, [])
_reg("valid_slack", _seed_slack, ["ok"])
_reg("valid_mimic", _seed_mimic, ["ok", "mimic"])

_PAD = _seed_slack()[1]["pretrailer_pad"][1]

# The unknown-record recipes rewrite seed `meta`'s 24-byte record header
# whole, there being no named sub-field for a record's type. Its extent slot
# is read from the seed's own layout rather than written as a literal: a raw
# offset in a recipe is exactly the restatement site the layout map exists to
# remove, and it would silently rot if the seed's geometry ever changed.
_META_EXT = SEEDS["meta"]()[1]["record[0x0002].extent"]


def _rec_header(type_, flags, inline_len, slot):
    return (u16(type_) + u16(flags) + u32(inline_len)
            + u64(slot[0]) + u64(slot[1]))


# A 23-byte document — the width of seed `meta`'s, so it patches in place —
# carrying a `tarn.`-prefixed key this specification does not register.
_UNKNOWN_KEY_DOC = b'{"tarn.nosuchkey":true}'
assert len(_UNKNOWN_KEY_DOC) == 23


# --------------------------------------------------------------------------
# Vectors
# --------------------------------------------------------------------------

VECTORS = [

    # -- §6.2/§6.3: the trailer's value ranges at their ends ---------------
    Vector("TV-0600", "pair",
           "version_minor 0xFFFF, the u16 ceiling — minors never gate "
           "[R-CNT-07] (§21.6)", True,
           patches=[Patch("trailer.version_minor", u16(0xFFFF))],
           repair=["trailer.crc"],
           serves=["ok", "bad"]),
    Vector("TV-0601", "pair",
           "flags bit 16 set, the ignore lane's lowest bit — ignored, file "
           "conforming [R-CNT-08] (§21.6)", True,
           patches=[Patch("trailer.flags", u32(1 << 16))],
           repair=["trailer.crc"],
           serves=["ok", "bad"]),
    Vector("TV-0602", "pair",
           "flags bit 31 set, the ignore lane's highest bit [R-CNT-08]", True,
           patches=[Patch("trailer.flags", u32(1 << 31))],
           repair=["trailer.crc"],
           serves=["ok", "bad"]),
    Vector("TV-0603", "pair",
           "flags 0xFFFF0000, the whole ignore lane set and the incompat "
           "lane clear [R-CNT-08]", True,
           patches=[Patch("trailer.flags", u32(0xFFFF0000))],
           repair=["trailer.crc"],
           serves=["ok", "bad"]),
    Vector("TV-0604", "pair",
           "file_id 0xFFFFFFFFFFFFFFFF, its ceiling as a u64 with no upper "
           "domain limit of its own [R-CNT-06]", True,
           patches=[Patch("trailer.file_id", u64(0xFFFFFFFFFFFFFFFF))],
           repair=["trailer.crc"],
           serves=["ok", "bad"]),
    Vector("TV-0605", "pair",
           "file_id 1, its floor: the smallest value [R-CNT-06] permits",
           True,
           patches=[Patch("trailer.file_id", u64(1))],
           repair=["trailer.crc"],
           serves=["ok", "bad"]),

    # -- §15.2's sentinel, and the zero-means-none declarations ------------
    Vector("TV-0606", "sparse",
           "a sparse layer: one stored tile and three sentinel entries, "
           "reading as fill [R-IDX-02], [R-TYP-08] (§21.6)", True,
           serves=["ok", "sparse: tile 0 stored; tiles 1-3 read as fill 0x2A"]),
    Vector("TV-0607", "valid_sparse_all",
           "an all-sentinel index, with alignment 0, slab 0 and slab "
           "alignment 0 — the 'none declared' encoding of each [R-IDX-02], "
           "[R-SLB-01], [R-SLB-02]", True,
           serves=["ok", "sp: every addressed tile reads as fill 0x2A"]),
    Vector("TV-0608", "valid_sparse_all",
           "alignment 512, the floor of [R-SLB-01]'s power-of-two range",
           True,
           patches=[Patch("layer[sp].alignment", u64(512))],
           repair=["directory.crc", "trailer.crc"],
           serves=["ok"]),
    Vector("TV-0609", "valid_sparse_all",
           "alignment 2^62, the ceiling of [R-SLB-01]'s range", True,
           patches=[Patch("layer[sp].alignment", u64(1 << 62))],
           repair=["directory.crc", "trailer.crc"],
           serves=["ok"]),
    Vector("TV-0610", "valid_sparse_all",
           "slab run length 1 with slab alignment 1 — both floors, and "
           "A_slab = 1 is contiguity-only [R-SLB-02]", True,
           patches=[Patch("layer[sp].slab", u64(1)),
                    Patch("layer[sp].slab_alignment", u64(1))],
           repair=["directory.crc", "trailer.crc"],
           serves=["ok"]),
    Vector("TV-0611", "valid_sparse_all",
           "slab run length 2^63-1 with slab alignment 2^62 — both ceilings "
           "[R-SLB-02], [R-ENC-03]", True,
           patches=[Patch("layer[sp].slab", u64(MAX63)),
                    Patch("layer[sp].slab_alignment", u64(1 << 62))],
           repair=["directory.crc", "trailer.crc"],
           serves=["ok"]),

    # -- §11: geometry at its floor and its ceiling ------------------------
    Vector("TV-0612", "valid_empty_dim",
           "a dimension of extent 0: zero addressed tiles, extent slot "
           "(0,0), crc_of_crc_array 0, and dir_offset at its floor of 16 "
           "[R-GEO-02], [R-CNT-17], [R-CNT-23] (§21.6)", True,
           serves=["empty: a valid layer; every read returns no samples"]),
    Vector("TV-0613", "valid_big_extent",
           "extent and tile extent both 2^63-1, so P and N.P sit exactly on "
           "[R-ENC-04]'s bound [R-ENC-03], [R-GEO-03]", True,
           serves=["ok",
                   "big: one unstored tile; a reader MAY decline the layer "
                   "on resource grounds, but MUST report that as a limit "
                   "and not as invalidity [R-ERR-04]"]),
    Vector("TV-0614", "valid_rank32",
           "rank 32, §21.9's minimum guarantee for rank [R-ERR-03]", True,
           serves=["ok", "r32"]),
    Vector("TV-0615", "valid_rank255",
           "rank 255, the hard limit the u8 rank field forces [R-ERR-05]",
           True,
           serves=["ok", "r255"]),
    Vector("TV-0616", "valid_chan4096",
           "4096 channels, §21.9's minimum guarantee for C [R-ERR-03]", True,
           serves=["ok", "c4096"]),
    Vector("TV-0617", "valid_chan65535",
           "65,535 channels, the hard limit the u16 channel-count field "
           "forces [R-ERR-05]", True,
           serves=["ok",
                   "c65535: one unstored tile, so every sample is 65,535 "
                   "fill bytes"]),
    Vector("TV-0618", "valid_layers64",
           "64 layers in one directory — a scaled exercise of §21.9's "
           "65,536-layer guarantee, whose bound is in SKIPPED [R-ERR-03]",
           True,
           serves=["ok"] + [f"l{i:02d}" for i in range(64)]),
    Vector("TV-0619", "valid_multisegment",
           "entry_count 65,537: a full all-sentinel segment whose CRC is "
           "[R-IDX-05]'s constant 0xEECB3BB2, plus a one-entry partial "
           "segment whose CRC must be computed [R-IDX-04]", True,
           serves=["ok",
                   "seg: tiles 0-65535 read as fill; tile 65536 is stored"]),

    # -- §4.6: names --------------------------------------------------------
    Vector("TV-0620", "valid_names_max",
           "layer, dimension and channel names all exactly 255 bytes — the "
           "hard limit a u8 length prefix forces [R-ERR-05], [R-ENC-12]",
           True, serves=["ok", "a*255"]),
    Vector("TV-0621", "valid_names_edge",
           "names at the code-point edges: 1 byte (the length floor), "
           "U+0020, U+007F, and U+10FFFF [R-ENC-12], [R-ENC-13]", True,
           serves=["ok", "z"]),

    # -- §12, §13, §14: values, fills, padding ------------------------------
    Vector("TV-0622", "valid_fills",
           "one channel of each of the thirteen core types, every fill an "
           "edge bit pattern (NaN payload, -0.0, +Inf, the minima and "
           "maxima), tile unstored so every sample is fill [R-TYP-05], "
           "[R-TYP-06], [R-TYP-08]", True,
           serves=["ok", "fills: every sample position reads each channel's "
                         "recorded fill, bit-exactly"]),
    Vector("TV-0623", "valid_types",
           "one interleaved sample carrying all thirteen core types at "
           "element size, little-endian [R-TYP-01], [R-SER-02]", True,
           serves=["ok", "types"]),
    Vector("TV-0624", "planar",
           "a planar layer mixing a numeric channel and a packed bool plane, "
           "P mod 8 = 0 so the plane has no pad bits [R-SER-09], [R-SER-03] "
           "(§21.6)", True,
           serves=["planar", "ok"]),
    Vector("TV-0625", "planar",
           "bool fill 0x01 — the upper of the two bytes [R-TYP-07] admits",
           True,
           patches=[Patch("layer[planar].chan[1].fill", b"\x01\x01")],
           repair=["directory.crc", "trailer.crc"],
           serves=["ok",
                   "planar: channel m's fill is true; the stored plane has "
                   "no padding position and no pad bit, so no stored byte "
                   "changes with it"]),
    Vector("TV-0626", "valid_padbits",
           "a packed bool plane with P = 12: four pad bits in the final "
           "byte, each carrying the channel's fill bit of 1 [R-SER-03], "
           "[R-SER-05]", True,
           serves=["ok", "bits"]),
    Vector("TV-0627", "valid_mixed_inter",
           "an interleaved layer mixing numeric and bool channels, the bool "
           "value a single byte [R-SER-09], [R-SER-08] (§21.6)", True,
           serves=["ok", "mix"]),
    Vector("TV-0628", "valid_pad",
           "a tile extent above its dimension's extent: one padded tile, "
           "twelve padding positions, each carrying the channel's fill "
           "[R-GEO-01], [R-GEO-04], [R-SER-05]", True,
           serves=["ok", "pad: four samples; the twelve padding positions "
                         "are never returned"]),

    # -- §17: codecs and the filter ----------------------------------------
    Vector("TV-0629", "valid_deflate",
           "codec 2 in both directions: a stored tile shorter than its "
           "decoded image and one longer than it [R-COD-05], [R-COD-08] "
           "(§21.6)", True,
           serves=["ok", "shrink", "grow"]),
    Vector("TV-0630", "valid_zstd",
           "codec 3 at every frame constraint: one frame, no dictionary ID, "
           "no content checksum, window equal to the decoded size, "
           "Frame_Content_Size present and equal [R-COD-06]", True,
           serves=["ok", "z"]),
    Vector("TV-0631", "valid_filter2",
           "filter 2 at each stride [R-COD-10] names: interleaved Q, planar "
           "element size, and the identity for a packed bool plane", True,
           serves=["ok", "sh_i", "sh_p", "sh_b"]),
    Vector("TV-0632", "valid_codec4_bound",
           "codec 4 declared at a decoded tile size of exactly 0x7E000000, "
           "the bound [R-COD-07] forbids exceeding [R-ERR-05]", True,
           serves=["ok", "lz: one unstored tile"]),

    # -- §7, §18: records, metadata, and slack ------------------------------
    Vector("TV-0633", "meta",
           "a top-level user-metadata record: encoding 1, a registered "
           "tarn. key, one object member, extent CRC intact [R-MTA-03], "
           "[R-MTA-04], [R-MTA-07]", True,
           serves=["ok", 'file metadata {"tarn.title":"vector"}']),
    Vector("TV-0634", "meta",
           "a user-metadata document carrying an unrecognized tarn.-prefixed "
           "key — the reader ignores the key, the file is conforming "
           "[R-MTA-06] (§21.6)", True,
           patches=[Patch("record[0x0002].extent",
                          _UNKNOWN_KEY_DOC + u32(crc32c(_UNKNOWN_KEY_DOC)))],
           serves=["ok", "file metadata: the document reads, the unknown "
                         "key is skipped"]),
    Vector("TV-0635", "valid_meta_zstd",
           "a user-metadata document under encoding 2: one RFC 8878 frame, "
           "no dictionary ID, no content checksum [R-MTA-03], [R-MTA-09]",
           True,
           serves=["ok", 'file metadata {"tarn.creator":...,'
                         '"tarn.title":"zstd"}']),
    Vector("TV-0636", "meta",
           "a record of an experimental type with MU = 0 — ignored as though "
           "absent, the file conforming [R-CNT-15], [R-EXT-03] (§21.6)",
           True,
           patches=[Patch("record[0x0002].header",
                          _rec_header(0x8001, 0b10, 1, _META_EXT))],
           repair=["directory.crc", "trailer.crc"],
           serves=["ok", "the unknown record is skipped by the reader; its "
                         "extent stays a claimed structure under §5.2"]),
    Vector("TV-0637", "meta",
           "an unknown record with MU = 0 and extent slot (0,0), the "
           "'no extent' encoding [R-CNT-13], [R-CNT-15] (§21.6)", True,
           patches=[Patch("record[0x0002].header",
                          _rec_header(0x8001, 0b10, 1, (0, 0)))],
           repair=["directory.crc", "trailer.crc"],
           serves=["ok", "the record has no extent; the 27 bytes it used to "
                         "address are slack"]),
    Vector("TV-0638", "valid_no_layers",
           "zero layers with a non-empty directory [R-CNT-14] (§21.6)", True,
           serves=["the file names no layer, so there is no layer content",
                   'file metadata {"tarn.title":"no layers"}']),
    Vector("TV-0639", "valid_slack",
           "a pre-trailer pad of non-zero bytes: slack is unconstrained "
           "content under no checksum [R-CNT-21], [R-CNT-05] (§21.6)", True,
           patches=[Patch("pretrailer_pad", b"\xDE" * _PAD)],
           serves=["ok"]),
    Vector("TV-0640", "valid_mimic",
           "a stored tile whose 64 bytes are a valid-looking trailer — inert, "
           "since nothing enumerates slack [R-LIF-06] (§21.6)", True,
           serves=["ok", "mimic: 64 uint8 samples that happen to spell a "
                         "trailer"]),
]


# --------------------------------------------------------------------------
# Gaps. An honest gap beats a vector that lies.
# --------------------------------------------------------------------------

SKIPPED = {
    # §21.9, the directory-region row ADR-0065 added. Joins the five
    # §21.9 guarantees already skipped below on the same ground: the
    # at-bound file is real but its size makes it unshippable. A 16 MiB
    # directory is about 16.8 MB of vector, roughly four times the whole
    # 4.2 MB corpus, and it exercises no condition a smaller file cannot —
    # exceeding a §21.9 guarantee leaves the file conforming (`[R-ERR-04]`),
    # so there is no register row and no outcome to assert.
    "§21.9/size of the directory region = 16 MiB":
        "An at-bound vector is ~16.8 MB, about 4x the entire corpus, and "
        "asserts nothing a smaller file does not: a file exceeding a §21.9 "
        "guarantee remains conforming (`[R-ERR-04]`), so the row carries no "
        "outcome and no register condition. The guarantee bounds what a "
        "reader may decline, not what a file may contain.",
    # §21.6, row 2.
    "§21.6/coordinate outside the layer's extents":
        "The condition is a property of a *request*, not of a file: the "
        "bytes a reader is handed are identical whether or not anyone asks "
        "for an out-of-range coordinate, so no two conforming files differ "
        "by it and §21.1's 'one distinguishable file' test cannot be met. "
        "[R-VEC-02]'s manifest entry records decoded content per scope and "
        "has no place to state a request, so a vector here would carry an "
        "expectation nothing checks. TV-0628's padded layer is the nearest "
        "reachable case: it makes positions outside the extents exist in "
        "the stored bytes, which [R-GEO-04] forbids returning.",

    # §21.6, row 4 — the empty-directory instance.
    "§21.6/zero layers, empty directory":
        "TV-0001 in slice.py is Appendix A's file, which is exactly this "
        "case; a vector here would be byte-identical to it. TV-0638 "
        "supplies the distinguishable instance instead: zero layers with a "
        "non-empty record sequence.",

    # §21.9 minimum guarantees not constructible at their bound.
    "§21.9/addressed tiles per layer = 2^32":
        "The index region alone is 2^32 x 20 B + 2^16 x 4 B = 85.9 GB of "
        "incompressible entries. Exercised by TV-0619 at 65,537 entries — "
        "two segments, the full/partial segment boundary, and [R-IDX-05]'s "
        "constant — with the bound checked arithmetically, which is the "
        "substitution §24 [R-VEC-03] names for this quantity.",
    "§21.9/layers per file = 65,536":
        "65,536 layer records of ~119 B of inline payload each is a 7.8 MB "
        "directory, and a reader's open fetches the directory whole "
        "([R-RDR-01]), so the vector would be a 7.8 MB file. TV-0618 "
        "exercises the shape at 64 layers.",
    "§21.9/decoded size of one tile = 256 MiB":
        "A stored tile at the bound is a 256 MiB payload; under codec 1 "
        "[R-COD-04] forces the stored length to equal it, and a "
        "compressing codec would test the codec rather than the bound. "
        "TV-0613 declares a decoded size far above the guarantee with an "
        "unstored tile, which exercises [R-ERR-04]'s 'report a resource "
        "refusal as a limit, not as invalidity' but not the guarantee "
        "itself.",
    "§21.9/decoded size of one user-metadata document = 16 MiB":
        "A 16 MiB document; under encoding 1 the extent is 16 MiB of "
        "committed bytes, and under encoding 2 the vector would measure "
        "the compressibility of whatever filler was chosen rather than the "
        "bound.",
    "§21.9/zstd Window_Size = 8 MiB":
        "A frame declaring an 8 MiB window needs 8 MiB of decoded content "
        "to be conforming under [R-COD-06]'s rule that the window not "
        "exceed the tile's decoded size, so the vector is an 8 MiB tile.",

    # [R-ERR-05] hard limits not constructible at their bound.
    "[R-ERR-05]/entry_count = 2^63-1":
        "[R-CNT-17] fixes extent_length at entry_count x 20 + "
        "ceil(entry_count/2^16) x 4, so a conforming file at this bound is "
        "1.8 x 10^20 bytes. No file can carry the count without the region.",
    "[R-ERR-05]/a tile-index offset or length = 2^63-1":
        "[R-IDX-03] requires offset + length <= F - 64 for a non-sentinel "
        "entry, so an entry at the bound needs a file of 2^63 bytes. The "
        "bound is reachable only in the *invalid* direction, which is "
        "T11's and T12's ground, not the positive corpus's. TV-0613 "
        "reaches the same 2^63-1 ceiling through a declared extent, the "
        "one field of the family a small file can hold at its maximum.",

    # Coverage this module wanted and the builder cannot express.
    "§18.1/a layer-scope user-metadata sub-record":
        "A sub-record lives at the end of a layer record's inline payload "
        "and tarn_build emits no sub-records; a Patch cannot add one, since "
        "it cannot change a field's width. Layer-scope metadata therefore "
        "has no positive vector — the top-level instances are TV-0633 "
        "through TV-0635. This is a gap in the builder, not in the format.",
    "§16.1/alignment declared with a stored tile at an aligned offset":
        "TV-0608 and TV-0609 declare A on a layer whose tiles are all "
        "unstored, where [R-SLB-01]'s invariant holds vacuously. A vector "
        "with a stored tile actually at a multiple of A needs the writer to "
        "place payload bytes at a chosen offset, and tarn_build appends "
        "payloads in order with no padding control. The same limit applies "
        "to [R-SLB-03]'s packed slab runs.",
}
