# SPDX-License-Identifier: Apache-2.0
"""§21.4's codec rows — T3, T13, T15–T26, and T4's interleaved bool instance.

Every vector here is a **seed**, not a patch. §17.2's constraints are properties
of a stored tile's *payload* — a wrapper around a DEFLATE stream, a second zstd
frame, a nonzero Dictionary_ID — and a payload cannot be reached by a recipe:
the builder's layout map names index entries and record fields, never the bytes
an entry points at. Patching one would also change its length, which moves every
structure after it. So each vector declares its own two-layer file through
`register_seed`: the intact `ok` layer [R-VEC-04] requires, and a `bad` layer
whose single tile *is* the malformed stream. There is nothing to repair, because
nothing is edited after the build — every CRC in the file is computed over the
bytes the vector means to ship.

Two constraints shape the constructions:

  * **§19.2's order.** ADR-0056 records six vectors that claimed T3 while
    keeping codec 1, where [R-COD-04]'s entry-length equality (T14) is the same
    predicate checked strictly earlier, from the entry alone and before any
    fetch. T3 therefore needs a *compressing* codec, where a stored length and a
    decoded size are legitimately unequal; all six instances below use codec 2,
    whose streams `zlib` produces exactly.
  * **One defect per file.** For the zstd rows this is mostly a matter of
    keeping the frame header otherwise perfect: Frame_Content_Size equal to the
    decoded size, window size equal to it, no dictionary, no checksum. Where a
    register instance *cannot* be built without a second condition — T18's
    "skippable frame before the frame" is a payload whose first four bytes are
    not the frame magic, which is T17 — the co-violation is inherent to the
    row's own text and is noted at the vector. It never misleads: both rows cite
    [R-COD-06], and both carry the same outcome, scope, detector and detection
    point, so no reading of the file yields a different verdict.

The streams come from `codec_streams.py`, which builds §17.2's excluded frame
features field by field because no compressor emits them. Three constructions
that module does not carry are built here: a fixed-Huffman DEFLATE block whose
match distance reaches before its own output start (T13), an LZ4 block with the
same property, and XXH64, so that T20's content-checksum frame carries the
*correct* checksum — a wrong one would make the frame fail to decode and the
vector would evidence T25 instead of the flag it claims.
"""
import struct
import zlib

from tarn_build import Channel, Layer, build_with_layout
from tarn_vectors import Vector, register_seed
from codec_streams import (deflate_corrupt, deflate_gzip_wrapped, deflate_raw,
                           deflate_two_streams, deflate_zlib_wrapped,
                           lz4_frame, zstd_frame, zstd_skippable)

# --------------------------------------------------------------------------
# Seed scaffolding
# --------------------------------------------------------------------------

TILE = {"kind": "tile", "layer": "bad", "disk_ordinal": 0}


def _ok() -> Layer:
    """The intact sibling [R-VEC-04] requires, identical to seed `pair`'s.

    Its decoded content is what a reader that scopes its refusal to the damaged
    tile still owes; without it these vectors could not tell such a reader from
    one that rejects the whole file under [R-CNF-12]'s licence.
    """
    return Layer("ok", extents=(2, 3), tile_extents=(2, 3),
                 channels=[Channel("t", 12)],
                 tiles=[struct.pack("<6I", 0x3F800000, 0x80000000, 0x7FC00001,
                                    0xC0000000, 0x00000000, 0x7F800000)])


def _seed(vid: str, bad: Layer) -> str:
    """Register `ok` + `bad` as a seed of this vector's own, and name it."""
    nm = f"codec:{vid}"

    def fn(_bad=bad):
        return build_with_layout([_ok(), _bad])

    return register_seed(nm, fn, ["ok", "bad"])


def _reader(vid, title, bad, row, rule):
    """A reader-detected reject-tile: tile bad:0 is refused, `ok` still served.

    No patches, no repairs, no broken checksums — the defect is the payload the
    seed builds, and every CRC covering it is computed over exactly those bytes.
    """
    return Vector(vid, _seed(vid, bad), title, False,
                  row=row, rule=rule, outcome="reject-tile", scope=TILE,
                  detector="reader", detected="tile use",
                  must_not_serve=["tile:bad:0"], serves=["ok"])


def _verifier(vid, title, bad, row, rule, serves=("ok",)):
    """A verifier-detected reject-tile.

    §19.2 places these outside the reader tiers: a reader carries no obligation
    to screen decoded content, so it MAY serve the tile and both layers. The
    file is nonconforming all the same, and a verifier MUST NOT certify it.
    """
    return Vector(vid, _seed(vid, bad), title, False,
                  row=row, rule=rule, outcome="reject-tile", scope=TILE,
                  detector="verifier", detected="certification",
                  must_not_serve=[], serves=list(serves))


# --------------------------------------------------------------------------
# Streams codec_streams.py does not carry
# --------------------------------------------------------------------------

class _Bits:
    """RFC 1951 §3.1.1 bit packing: data elements LSB-first, Huffman codes MSB-first."""

    def __init__(self):
        self._out, self._acc, self._n = bytearray(), 0, 0

    def _bit(self, b):
        self._acc |= (b & 1) << self._n
        self._n += 1
        if self._n == 8:
            self._out.append(self._acc)
            self._acc, self._n = 0, 0

    def value(self, v, n):          # a data element: least-significant bit first
        for i in range(n):
            self._bit(v >> i)

    def code(self, v, n):           # a Huffman code: most-significant bit first
        for i in range(n - 1, -1, -1):
            self._bit(v >> i)

    def done(self) -> bytes:
        if self._n:
            self._out.append(self._acc)
        return bytes(self._out)


def deflate_far_back(literal: int = 0x41) -> bytes:
    """One RFC 1951 stream whose match distance reaches before its own output.

    A single BFINAL fixed-Huffman block: one literal, then length symbol 257
    (length 3) with distance symbol 5 (base 7, one extra bit = 0, so distance
    7), then end-of-block. The block would produce 4 bytes if the 7 bytes it
    reaches back for existed — they do not, and they could only come from a
    previous tile's history window, which is exactly [R-COD-02]'s prohibition.
    Literal 0x41 encodes as fixed code 0x30 + 0x41 in 8 bits (RFC 1951 §3.2.6).
    """
    w = _Bits()
    w.value(1, 1)                   # BFINAL = 1
    w.value(1, 2)                   # BTYPE = 01, fixed Huffman
    w.code(0x30 + literal, 8)       # literal
    w.code(1, 7)                    # length symbol 257 -> length 3
    w.code(5, 5)                    # distance symbol 5 -> base 7
    w.value(0, 1)                   # its one extra bit -> distance 7
    w.code(0, 7)                    # symbol 256, end of block
    return w.done()


def lz4_far_back(offset: int = 1000) -> bytes:
    """One raw LZ4 block whose match offset reaches before its own output start.

    20 literals, then a match of length 4 at `offset`, then 8 trailing literals:
    32 bytes of output. The trailing sequence keeps the block format's
    end-of-block restrictions (the last five bytes are literals, and the match
    starts twelve bytes before the end), so the *only* thing wrong with the
    block is that its match reaches 1000 bytes back from an output that has
    produced 20 — data outside the stored extent.
    """
    out = bytearray()
    out.append(0xF0)                       # token: literal length >= 15, match length 4
    out.append(20 - 15)                    # literal-length extension
    out += bytes(range(0x41, 0x41 + 20))
    out += struct.pack("<H", offset)       # match offset, little-endian
    out.append(8 << 4)                     # final sequence: 8 literals, no match
    out += bytes(range(0x61, 0x61 + 8))
    return bytes(out)


_M = (1 << 64) - 1
_P1, _P2, _P3 = 0x9E3779B185EBCA87, 0xC2B2AE3D27D4EB4F, 0x165667B19E3779F9
_P4, _P5 = 0x85EBCA77C2B2AE63, 0x27D4EB2F165667C5


def _rotl(x, r):
    return ((x << r) | (x >> (64 - r))) & _M


def _round(acc, inp):
    return (_rotl((acc + inp * _P2) & _M, 31) * _P1) & _M


def xxh64(d: bytes, seed: int = 0) -> int:
    """XXH64, for T20's frame checksum only.

    zstd's content checksum is the low 32 bits of XXH64 over the decompressed
    content (RFC 8878 §3.1.1). Writing the *correct* value matters: a frame
    carrying a wrong one fails to decode, and the vector would then evidence
    T25 rather than the flag T20 names.
    """
    n, i = len(d), 0
    if n >= 32:
        v1, v2 = (seed + _P1 + _P2) & _M, (seed + _P2) & _M
        v3, v4 = seed & _M, (seed - _P1) & _M
        while i + 32 <= n:
            v1 = _round(v1, int.from_bytes(d[i:i + 8], "little"))
            v2 = _round(v2, int.from_bytes(d[i + 8:i + 16], "little"))
            v3 = _round(v3, int.from_bytes(d[i + 16:i + 24], "little"))
            v4 = _round(v4, int.from_bytes(d[i + 24:i + 32], "little"))
            i += 32
        h = (_rotl(v1, 1) + _rotl(v2, 7) + _rotl(v3, 12) + _rotl(v4, 18)) & _M
        for v in (v1, v2, v3, v4):
            h = ((h ^ _round(0, v)) * _P1 + _P4) & _M
    else:
        h = (seed + _P5) & _M
    h = (h + n) & _M
    while i + 8 <= n:
        h = (_rotl(h ^ _round(0, int.from_bytes(d[i:i + 8], "little")), 27) * _P1 + _P4) & _M
        i += 8
    if i + 4 <= n:
        h = (_rotl(h ^ ((int.from_bytes(d[i:i + 4], "little") * _P1) & _M), 23) * _P2 + _P3) & _M
        i += 4
    while i < n:
        h = (_rotl(h ^ ((d[i] * _P5) & _M), 11) * _P1) & _M
        i += 1
    h ^= h >> 33
    h = (h * _P2) & _M
    h ^= h >> 29
    h = (h * _P3) & _M
    return h ^ (h >> 32)


def zstd_checksummed(data: bytes) -> bytes:
    """A frame with Content_Checksum_flag set and the checksum correct."""
    f = bytearray(zstd_frame(data, content_checksum=True))
    f[-4:] = struct.pack("<I", xxh64(data) & 0xFFFFFFFF)
    return bytes(f)


def zstd_bad_block_type(data: bytes) -> bytes:
    """A well-formed frame header over a block header declaring reserved type 3.

    The magic is present, there is one frame, no dictionary, no checksum, and
    Frame_Content_Size and window both equal the decoded size — so T17, T18,
    T19, T20, T21 and T22 are all clean and the single defect is the block
    header, which is T25's zstd instance.
    """
    f = bytearray(zstd_frame(data))
    off = len(f) - len(data) - 3            # the block header precedes the raw block
    hdr = int.from_bytes(f[off:off + 3], "little")
    f[off:off + 3] = (((hdr & ~0b110) | (3 << 1))).to_bytes(3, "little")
    return bytes(f)


def shuffle(image: bytes, s: int) -> bytes:
    """[R-COD-10]'s byte-shuffle at stride `s`: byte i of group j lands at i·n + j."""
    n = len(image) // s
    return bytes(image[j * s + i] for i in range(s) for j in range(n))


# --------------------------------------------------------------------------
# T3 — the decoded payload's length is not the declared decoded size
# --------------------------------------------------------------------------
# Six instances, all codec 2. Under a compressing codec the stored length and
# the decoded size are unrelated by design ([R-COD-08]'s second Note says so
# outright), so the only thing wrong with these files is what the stream decodes
# TO. Every geometry keeps E == T, so no padding position exists to co-violate
# §14.5, and the packed planar planes keep P mod 8 == 0, so no pad bit exists to
# co-violate T5. The streams are `zlib`'s own output, consumed exactly, so T24
# and T25 are clean.

def _il2(payload):
    """Interleaved, channels uint8 + uint16: Q = 3, P = 4, decoded size 12."""
    return Layer("bad", extents=(2, 2), tile_extents=(2, 2),
                 channels=[Channel("a", 6), Channel("b", 7)],
                 codec=2, tiles=[payload])


def _pl_num(payload):
    """Planar, one float32 channel: P = 4, Bᶜ = 4, decoded size 16."""
    return Layer("bad", extents=(2, 2), tile_extents=(2, 2), layout=2,
                 channels=[Channel("t", 12)], codec=2, tiles=[payload])


def _pl_bool(payload):
    """Planar bool: P = 16, decoded size ⌈16/8⌉ = 2."""
    return Layer("bad", extents=(4, 4), tile_extents=(4, 4), layout=2,
                 channels=[Channel("m", 1, b"\x00")], codec=2, tiles=[payload])


VECTORS = [
    _reader("TV-0700",
            "T3 interleaved P·Q, payload longer: deflate stream decoding to 13 "
            "bytes against decoded size 12",
            _il2(deflate_raw(bytes(13))), "T3", "R-SER-07"),
    _reader("TV-0701",
            "T3 interleaved P·Q, payload shorter: deflate stream decoding to 11 "
            "bytes against decoded size 12",
            _il2(deflate_raw(bytes(11))), "T3", "R-SER-07"),
    _reader("TV-0702",
            "T3 planar numeric P·Bᶜ, payload longer: deflate stream decoding to "
            "17 bytes against decoded size 16",
            _pl_num(deflate_raw(bytes(17))), "T3", "R-SER-07"),
    _reader("TV-0703",
            "T3 planar numeric P·Bᶜ, payload shorter: deflate stream decoding to "
            "15 bytes against decoded size 16",
            _pl_num(deflate_raw(bytes(15))), "T3", "R-SER-07"),
    _reader("TV-0704",
            "T3 packed planar bool ⌈P/8⌉, payload longer: deflate stream decoding "
            "to 3 bytes against decoded size 2",
            _pl_bool(deflate_raw(bytes(3))), "T3", "R-SER-07"),
    _reader("TV-0705",
            "T3 packed planar bool ⌈P/8⌉, payload shorter: deflate stream decoding "
            "to 1 byte against decoded size 2",
            _pl_bool(deflate_raw(bytes(1))), "T3", "R-SER-07"),

    # ----------------------------------------------------------------------
    # T4 — a padding position does not carry its channel's fill value.
    # The instance §21.4 names for the interleaved bool byte, which t_rows.py
    # could not build from seed `pair`: there the damageable tile's four bytes
    # are 01 02 03 04, and 02/03/04 are illegal bool bytes wherever they land,
    # so every placement that created a padding position also violated
    # [R-SER-08]. A seed fixes it. Extents (1,2) under tile extents (2,2) make
    # in-tile ordinals 2 and 3 padding; ordinal 2 carries 0x01 where the
    # channel's recorded fill is 0x00. T2 cannot co-fire twice over: its row is
    # scoped to a *real* sample position, and 0x01 is a legal bool byte anyway.
    # Codec 1, so the entry's length 4 equals the decoded size P·Q = 4 and T14
    # is clean.
    _verifier("TV-0706",
              "T4 interleaved bool fill byte: padding ordinal 2 carries 0x01 "
              "where the channel's fill byte is 0x00",
              Layer("bad", extents=(1, 2), tile_extents=(2, 2),
                    channels=[Channel("m", 1, b"\x00")],
                    tiles=[bytes([0x00, 0x01, 0x01, 0x00])]),
              "T4", "R-SER-05", serves=("ok", "bad")),

    # ----------------------------------------------------------------------
    # T13 — not independently decodable: the decode needs bytes outside the
    # tile's own stored extent. Both instances would decode to exactly the
    # declared decoded size if the history they reach for existed, so T3 has no
    # subject here, and both consume their extent exactly, so T24 is clean.
    _reader("TV-0707",
            "T13 deflate stream carrying a previous tile's history window: "
            "match distance 7 with one byte produced",
            Layer("bad", extents=(2, 2), tile_extents=(2, 2),
                  channels=[Channel("v", 6)], codec=2,
                  tiles=[deflate_far_back()]),
            "T13", "R-COD-02"),
    # Distinct from TV-0421, which claims T25's lz4 instance for the same
    # predicate — see FINDINGS below. That file declares codec 4 over the four
    # bytes 01 02 03 04, a token whose match is the whole block; this one is a
    # structurally complete block, correct in every respect the format states
    # except the reach of its one match.
    _reader("TV-0708",
            "T13 lz4 block whose match offset 1000 reaches before its own output "
            "start (20 bytes produced)",
            Layer("bad", extents=(4, 8), tile_extents=(4, 8),
                  channels=[Channel("v", 6)], codec=4,
                  tiles=[lz4_far_back()]),
            "T13", "R-COD-02"),

    # ----------------------------------------------------------------------
    # T15 — codec 2 with a wrapper instead of a raw RFC 1951 stream. Both
    # wrappers hold a stream that decodes to exactly the decoded size, so the
    # wrapper is the whole defect: strip it and the file conforms.
    # A reader that ignores [R-COD-05] and hands the bytes to a raw inflater
    # reaches [R-COD-08] instead (T25) — the zlib header parses as a stored
    # block with a corrupt LEN/NLEN pair, the gzip header as reserved block
    # type 3. Same outcome, scope, detector and detection point, so no reading
    # of either file yields a different verdict; the distinguishing evidence is
    # the wrapper's own signature, which is what the row names.
    _reader("TV-0709",
            "T15 codec 2 with a zlib RFC 1950 wrapper (CMF/FLG header, trailing "
            "Adler-32)",
            Layer("bad", extents=(2, 2), tile_extents=(2, 2),
                  channels=[Channel("v", 6)], codec=2,
                  tiles=[deflate_zlib_wrapped(bytes(4))]),
            "T15", "R-COD-05"),
    _reader("TV-0710",
            "T15 codec 2 with a gzip RFC 1952 member (1F 8B, trailing CRC32 and "
            "ISIZE)",
            Layer("bad", extents=(2, 2), tile_extents=(2, 2),
                  channels=[Channel("v", 6)], codec=2,
                  tiles=[deflate_gzip_wrapped(bytes(4))]),
            "T15", "R-COD-05"),

    # ----------------------------------------------------------------------
    # T16 — a second DEFLATE stream after the first BFINAL block. The second
    # stream is the empty stream 03 00: a complete RFC 1951 stream (BFINAL = 1,
    # fixed Huffman, end-of-block and nothing else) that produces no output. So
    # the extent decodes to exactly the decoded size under either reading —
    # first stream only, or everything — and T3 stays clean whichever a reader
    # does. What is left is only the second stream, which is the row.
    # T24 is a necessary consequence and not a separate defect: [R-COD-05]'s
    # "exactly one stream" and [R-COD-08]'s "consume the extent exactly" are
    # the same observation for deflate. Reported below.
    _reader("TV-0711",
            "T16 codec 2 with two DEFLATE streams: an empty second stream after "
            "the first BFINAL block",
            Layer("bad", extents=(2, 2), tile_extents=(2, 2),
                  channels=[Channel("v", 6)], codec=2,
                  tiles=[deflate_two_streams(bytes(4), b"")]),
            "T16", "R-COD-05"),
]

# --------------------------------------------------------------------------
# T18 … T25 — codec 3 (zstd) and codec 4 (lz4)
# --------------------------------------------------------------------------
# One shape for every zstd row: interleaved uint8, extents and tile extents
# (2,2), so P = 4, Q = 1 and the decoded size is 4. A conforming frame for that
# tile is `zstd_frame(IMG)`: single-segment, Frame_Content_Size 4, window
# therefore also 4, no dictionary ID, no content checksum. Each vector below
# changes exactly one of those facts, so the header a reader inspects differs
# from the conforming one in one field.

IMG = bytes([0x10, 0x20, 0x30, 0x40])
EMPTY_FRAME = zstd_frame(b"")       # a valid frame producing no output


def _z(payload, codec=3):
    return Layer("bad", extents=(2, 2), tile_extents=(2, 2),
                 channels=[Channel("v", 6)], codec=codec, tiles=[payload])


VECTORS += [
    # -- T18, four instances ------------------------------------------------
    # Each keeps the tile's own frame — the one carrying IMG — exactly
    # conforming, and each concatenation still decodes to exactly the decoded
    # size, so T3 has no subject. That is deliberate: §17.2's Note warns that a
    # whole-buffer zstd decoder tolerating concatenated and skippable frames
    # returns the right bytes for all four of these files. A reader that does
    # not confirm the single frame spans the full extent passes them silently,
    # which is precisely what the row exists to catch.
    _reader("TV-0712",
            "T18 a second concatenated compressed frame (the second produces no "
            "output, so the extent still decodes to 4 bytes)",
            _z(zstd_frame(IMG) + EMPTY_FRAME), "T18", "R-COD-06"),
    # The trailing frame declares Frame_Content_Size 0, which is its own content
    # and not the tile's. T22's subject is the frame carrying the tile — here
    # the first, whose Frame_Content_Size is 4 — since a per-frame constraint
    # presupposes the single frame [R-COD-06] requires.
    _reader("TV-0713",
            "T18 a skippable frame before the frame (magic 0x184D2A50)",
            _z(zstd_skippable() + zstd_frame(IMG)), "T18", "R-COD-06"),
    # Inherent co-violation, not a construction choice: a payload whose first
    # frame is skippable is a payload whose first four bytes are not
    # 28 B5 2F FD, which is T17. Both rows are [R-COD-06], both reject-tile at
    # tile use, so the file evidences the same verdict under either reading —
    # the same shape as t_rows.py's T8 note. Reported below.
    _reader("TV-0714",
            "T18 a skippable frame after the frame",
            _z(zstd_frame(IMG) + zstd_skippable()), "T18", "R-COD-06"),
    _reader("TV-0715",
            "T18 a skippable frame between two frames",
            _z(zstd_frame(IMG) + zstd_skippable() + EMPTY_FRAME),
            "T18", "R-COD-06"),
    # This last instance names two frames in its own text, so the "second
    # concatenated frame" condition is part of the instance rather than a
    # separate defect; both are T18.

    # -- T19 ----------------------------------------------------------------
    # Dictionary_ID_Flag = 1 and a one-byte Dictionary_ID of 1. Everything else
    # in the header is the conforming frame's. A decoder without the dictionary
    # reports a dictionary mismatch rather than decoding — the check the row
    # asks for is on the header field, before any decode.
    _reader("TV-0716",
            "T19 codec 3 and the frame header carries Dictionary_ID 1",
            _z(zstd_frame(IMG, dict_id=1)), "T19", "R-COD-06"),

    # -- T20 ----------------------------------------------------------------
    # Content_Checksum_flag set, and the trailing XXH64 low word *correct*, so
    # the frame decodes cleanly through a real decoder and the flag is the only
    # thing wrong with the file. A placeholder checksum would have made the
    # frame fail to decode, which is T25.
    _reader("TV-0717",
            "T20 codec 3 and the frame header sets Content_Checksum_flag (the "
            "checksum itself is correct)",
            _z(zstd_checksummed(IMG)), "T20", "R-COD-06"),

    # -- T21 ----------------------------------------------------------------
    # Single_Segment_flag cleared and a Window_Descriptor of 0x00: exponent 0,
    # mantissa 0, so Window_Size = 2¹⁰ = 1024 against a decoded size of 4. The
    # Frame_Content_Size field is omitted, which [R-COD-06] permits ("MAY be
    # present"), so T22 has no subject — it must be omitted, because in
    # single-segment mode Window_Size *is* Frame_Content_Size and the two rows
    # could not then be separated.
    _reader("TV-0718",
            "T21 codec 3 and the frame declares Window_Size 1024 against a "
            "decoded size of 4",
            _z(zstd_frame(IMG, window_log=10, omit_content_size=True)),
            "T21", "R-COD-06"),

    # -- T22 ----------------------------------------------------------------
    # Frame_Content_Size 3 against a decoded size of 4. Below rather than above:
    # the frame is single-segment, where Window_Size = Frame_Content_Size, so a
    # value above the decoded size would declare an oversized window and
    # co-violate T21. A value below leaves the window at 3, and [R-COD-06]
    # forbids only a window *exceeding* the decoded size.
    _reader("TV-0719",
            "T22 codec 3 and Frame_Content_Size 3 against a decoded size of 4",
            _z(zstd_frame(IMG, content_size=3)), "T22", "R-COD-06"),

    # ADR-0076: T21's and T22's cells enumerate the decoded-size formulas;
    # the vectors above are the interleaved instances. Same construction
    # discipline: E == T so no padding position exists, the packed plane
    # keeps P mod 8 = 0 so no pad bit exists, and each frame's content
    # decodes to exactly the plane's size, so the frame field named in the
    # title is the file's only fact.
    _reader("TV-0727",
            "T21 codec 3, planar: Window_Size 1024 against a uint8 plane's "
            "decoded size of 4",
            Layer("bad", extents=(2, 2), tile_extents=(2, 2), layout=2,
                  channels=[Channel("v", 6)], codec=3,
                  tiles=[zstd_frame(IMG, window_log=10,
                                    omit_content_size=True)]),
            "T21", "R-COD-06"),
    _reader("TV-0728",
            "T21 codec 3, packed planar bool: Window_Size 1024 against a "
            "plane of ⌈8/8⌉ = 1 byte",
            Layer("bad", extents=(2, 4), tile_extents=(2, 4), layout=2,
                  channels=[Channel("v", 1)], codec=3,
                  tiles=[zstd_frame(b"\xAA", window_log=10,
                                    omit_content_size=True)]),
            "T21", "R-COD-06"),
    _reader("TV-0729",
            "T22 codec 3, planar: Frame_Content_Size 3 against a uint8 "
            "plane's decoded size of 4",
            Layer("bad", extents=(2, 2), tile_extents=(2, 2), layout=2,
                  channels=[Channel("v", 6)], codec=3,
                  tiles=[zstd_frame(IMG, content_size=3)]),
            "T22", "R-COD-06"),
    _reader("TV-0730",
            "T22 codec 3, packed planar bool: Frame_Content_Size 0 against a "
            "plane of ⌈8/8⌉ = 1 byte",
            Layer("bad", extents=(2, 4), tile_extents=(2, 4), layout=2,
                  channels=[Channel("v", 1)], codec=3,
                  tiles=[zstd_frame(b"\xAA", content_size=0)]),
            "T22", "R-COD-06"),

    # ADR-0077 gave T22 the direction axis it shares with T14: the three
    # vectors above declare a Frame_Content_Size BELOW the decoded size,
    # these three declare one ABOVE it. Above needs care — the frames above
    # are single-segment, where Window_Size is Frame_Content_Size, so a
    # larger declared value would also declare an oversized window and
    # co-violate T21. Clearing Single_Segment with an explicit window_log
    # of 10 fixes Window_Size at 1024 ≥ every decoded size here, so only
    # the Frame_Content_Size relation fails.
    _reader("TV-0731",
            "T22 codec 3: Frame_Content_Size 5 against a decoded size of 4",
            _z(zstd_frame(IMG, content_size=5, window_log=10)),
            "T22", "R-COD-06"),
    _reader("TV-0732",
            "T22 codec 3, planar: Frame_Content_Size 5 against a uint8 "
            "plane's decoded size of 4",
            Layer("bad", extents=(2, 2), tile_extents=(2, 2), layout=2,
                  channels=[Channel("v", 6)], codec=3,
                  tiles=[zstd_frame(IMG, content_size=5, window_log=10)]),
            "T22", "R-COD-06"),
    _reader("TV-0733",
            "T22 codec 3, packed planar bool: Frame_Content_Size 2 against a "
            "plane of ⌈8/8⌉ = 1 byte",
            Layer("bad", extents=(2, 4), tile_extents=(2, 4), layout=2,
                  channels=[Channel("v", 1)], codec=3,
                  tiles=[zstd_frame(b"\xAA", content_size=2, window_log=10)]),
            "T22", "R-COD-06"),

    # -- T23 ----------------------------------------------------------------
    _reader("TV-0720",
            "T23 codec 4 and the stored bytes are an LZ4 frame (magic "
            "04 22 4D 18) instead of one raw block",
            _z(lz4_frame(IMG), codec=4), "T23", "R-COD-07"),

    # -- T24 ----------------------------------------------------------------
    # Four zero bytes after a frame that is conforming in every respect. They
    # are not a frame — no compressed-frame magic, no skippable magic — so T18
    # has no subject, and the frame itself decodes to exactly the decoded size,
    # so T3 and T25 have none either. All that is left is that the decode does
    # not consume the entry's length. Codec 3 rather than 2 keeps this file
    # distinct from TV-0711, where the trailing bytes *are* a stream.
    _reader("TV-0721",
            "T24 codec 3 and four bytes remain in the stored extent after the "
            "frame ends",
            _z(zstd_frame(IMG) + bytes(4)), "T24", "R-COD-08"),

    # -- T25, the two instances t_rows.py could not place -------------------
    _reader("TV-0722",
            "T25 deflate stream whose first block declares reserved block "
            "type 3",
            Layer("bad", extents=(2, 2), tile_extents=(2, 2),
                  channels=[Channel("v", 6)], codec=2,
                  tiles=[deflate_corrupt(bytes(4))]),
            "T25", "R-COD-08"),
    _reader("TV-0723",
            "T25 corrupt zstd block header: a conforming frame header over a "
            "block declaring reserved Block_Type 3",
            _z(zstd_bad_block_type(IMG)), "T25", "R-COD-08"),
]

# --------------------------------------------------------------------------
# T26 — filter 2 applied at a stride other than the mandated one
# --------------------------------------------------------------------------
# The row is a *writer's* fault that only becomes observable through content:
# the stored bytes are the byte-shuffle of a conforming decoded image at the
# wrong stride, so applying the inverse at the mandated stride yields an image
# whose padding positions no longer carry their channels' fill values. §21.7 is
# explicit that a wrong stride with no such structural constraint is
# undetectable, and the row says the same in its own text; these three files are
# the detectable cases, one per mandated stride the row names.
#
# Each therefore co-violates T4 by construction — that is what "where the
# resulting image breaks §14.5's padding content" means, and no file can satisfy
# T26's condition without it. The co-violation cannot mislead: T4 and T26 are
# both verifier-detected reject-tile at certification. What distinguishes these
# files from a plain T4 file is that the stored bytes unshuffle at one specific
# wrong stride to an image that conforms in every respect — a relation no other
# row's construction produces.
#
# Codec 1 throughout, so the stored length equals the decoded size and T14 stays
# clean (the shuffle is length-preserving). `serves` names only `ok`: the
# corpus's content deriver reads a tile payload as the decoded image, which is
# what a filter declaration makes it not.

_PL_IMG = bytes([0x01, 0x00, 0x02, 0x00, 0xCD, 0xAB, 0xCD, 0xAB])
_IL_IMG = bytes([0x11, 0x01, 0x00, 0x22, 0x02, 0x00,
                 0x77, 0xCD, 0xAB, 0x77, 0xCD, 0xAB])
_BOOL_IMG = bytes([0xAA, 0xBB, 0xCC, 0xDD, 0x00, 0x00, 0x00, 0x00])

VECTORS += [
    # Planar uint16, fill 0xABCD, extents (1,2) under tile extents (2,2): in-tile
    # ordinals 2 and 3 are padding and carry CD AB in the conforming image.
    # Mandated stride is the channel's element size, 2; the writer used 4. The
    # inverse at stride 2 recovers 01 02 CD CD 00 00 AB AB, whose padding
    # positions read 0x0000 and 0xABAB — neither is the fill.
    _verifier("TV-0724",
              "T26 planar numeric: shuffled at stride 4 where the mandated "
              "stride is the uint16 channel's element size 2",
              Layer("bad", extents=(1, 2), tile_extents=(2, 2), layout=2,
                    channels=[Channel("v", 7, b"\xCD\xAB")], filter=2,
                    tiles=[shuffle(_PL_IMG, 4)]),
              "T26", "R-COD-10"),
    # Interleaved uint8 (fill 0x77) + uint16 (fill 0xABCD): Q = 3, decoded size
    # 12, padding at ordinals 2 and 3. The writer used stride 2; the inverse at
    # the mandated Q = 3 recovers padding samples 02 01 77 and 77 22 AB against
    # the fill sample 77 CD AB.
    _verifier("TV-0725",
              "T26 interleaved: shuffled at stride 2 where the mandated stride "
              "is the sample stride Q = 3",
              Layer("bad", extents=(1, 2), tile_extents=(2, 2),
                    channels=[Channel("a", 6, b"\x77"),
                              Channel("b", 7, b"\xCD\xAB")], filter=2,
                    tiles=[shuffle(_IL_IMG, 2)]),
              "T26", "R-COD-10"),
    # Packed planar bool, tile extents (8,8) so P = 64 and the plane is 8 bytes
    # with no pad bits (T5 cannot co-fire); extents (4,8) make in-tile ordinals
    # 32-63 — the whole second half of the plane — padding, which the fill bit
    # 0 requires to be zero. The mandated stride is 1, the identity, so the
    # decoded image is the stored bytes verbatim; the writer shuffled at stride
    # 2, which moves the real bytes AA BB CC DD to AA CC 00 00 BB DD 00 00 and
    # lands BB DD in the padding half.
    #
    # This instance is why the previous round's skip reason was wrong only in
    # part: a mis-strided shuffle can never disturb a *pad bit*, because the
    # shuffle fixes the image's last byte for every stride (index L−1 maps to
    # itself), and the pad bits live there. Padding *positions* are a different
    # structure (§14.3's Note), they fall wherever the extents end, and the
    # shuffle moves them freely.
    _verifier("TV-0726",
              "T26 packed planar bool: shuffled at stride 2 where the mandated "
              "stride is the identity s = 1",
              Layer("bad", extents=(4, 8), tile_extents=(8, 8), layout=2,
                    channels=[Channel("m", 1, b"\x00")], filter=2,
                    tiles=[shuffle(_BOOL_IMG, 2)]),
              "T26", "R-COD-10"),
]


# --------------------------------------------------------------------------
# Construction checks, run at corpus-build time
# --------------------------------------------------------------------------
# Every claim above that a stream decodes to a stated length, or fails to decode
# for a stated reason, is checked here against `zlib` — the one decoder the
# no-dependency rule (ADR-0050) guarantees is present. The zstd and LZ4
# constructions are verified in codec_streams.py's --selftest, which runs them
# through a real decoder when one is installed.

def _inflate(b):
    return zlib.decompressobj(-15).decompress(b)


assert xxh64(b"") == 0xEF46DB3751D8E999, "XXH64 empty-input check vector"
for _n in (1, 3, 11, 13, 15, 17):
    assert len(_inflate(deflate_raw(bytes(_n)))) == _n
assert _inflate(deflate_two_streams(bytes(4), b"")) == bytes(4), \
    "T16's first stream must decode to exactly the decoded size"
assert deflate_raw(b"") == b"\x03\x00", "T16's second stream is the empty stream"
try:
    _inflate(deflate_far_back())
    raise AssertionError("T13's deflate stream decoded; it must not")
except zlib.error as _e:
    assert "distance too far back" in str(_e), str(_e)
try:
    _inflate(deflate_corrupt(bytes(4)))
    raise AssertionError("T25's deflate stream decoded; it must not")
except zlib.error:
    pass
assert deflate_zlib_wrapped(bytes(4))[0] == 0x78
assert deflate_gzip_wrapped(bytes(4))[:2] == b"\x1f\x8b"
assert zstd_frame(IMG)[:4] == b"\x28\xB5\x2F\xFD" and len(EMPTY_FRAME) == 9
assert lz4_frame(IMG)[:4] == b"\x04\x22\x4D\x18"
assert len(lz4_far_back()) == 33
# The shuffle is length-preserving, and each T26 image differs from its stored
# form — a stride that happened to be the identity would test nothing.
for _img, _s in ((_PL_IMG, 4), (_IL_IMG, 2), (_BOOL_IMG, 2)):
    assert len(shuffle(_img, _s)) == len(_img)
    assert shuffle(_img, _s) != _img


#: Nothing in this assignment was skipped. Recorded because the previous round
#: skipped fifteen of these rows and three of its reasons were false:
#:
#:   * "T13's lz4 instance is textually the same as T25's" — they are separable.
#:     T25's instance names two alternatives, "match offset 0 or match reaching
#:     past produced output"; TV-0708 builds T13 from a structurally complete
#:     block whose only fault is the reach of one match, and TV-0421 keeps T25
#:     for a different file. The overlap is real and is reported below, but it
#:     is between one alternative of one row and another row, not between the
#:     rows entire.
#:   * "T26's packed planar bool instance is undetectable" — true of pad bits,
#:     false of padding positions. See TV-0726.
#:   * "T24 has no subject" — true under codec 1 only, which the row does not
#:     require; TV-0721 builds it under codec 3.
#:
#: The remaining twelve reasons were accurate for a corpus that could only patch
#: named structure fields. register_seed removes that limit.
SKIPPED: dict[str, str] = {}


#: Observations about §21 this module could not resolve from the specification.
#: Recorded here rather than acted on: a vector that renames a row is worse than
#: a finding that names the ambiguity.
FINDINGS = {
    "T13 / T25, lz4":
        "T13's lz4 instance ('a match offset reaching before its own output "
        "start') and one of T25's two lz4 alternatives ('match reaching past "
        "produced output') are the same predicate under two rows, with the same "
        "outcome, scope, detector and detection point. A corpus building both "
        "instances ships two files for one condition. Suggest narrowing T25's "
        "lz4 instance to 'match offset 0', which is the alternative T13 cannot "
        "express — an offset of 0 reaches nothing, inside or outside the extent.",

    "T16 / T24, deflate":
        "For codec 2 the two rows are one observation: any second DEFLATE "
        "stream is also bytes the first decode did not consume, and there is no "
        "file satisfying T16 that does not satisfy T24. T18/T24 do separate for "
        "zstd, because trailing bytes that are not a frame satisfy T24 alone "
        "(TV-0721). Worth a note in T16's row that it is the deflate "
        "specialization of T24, as T14 is codec 1's specialization of T3.",

    "T17 / T18, skippable frame first":
        "T18's instance 'a skippable frame before the frame' cannot be built "
        "without violating T17: a payload beginning with a skippable frame is a "
        "payload whose first four bytes are not the compressed-frame magic. The "
        "instance is worth keeping — it is what catches a decoder that skips "
        "leading skippable frames before checking the magic — but the register "
        "could say that it necessarily co-violates T17, as §21.4 already says "
        "for other unavoidable pairs.",

    "T26 vs T4/T5":
        "Every T26 instance co-violates T4 or T5 by the row's own text, which "
        "scopes the row to strides 'where the resulting image breaks §14.5's "
        "padding content or [R-SER-08]'s bool bytes'. A verifier observes the "
        "broken content and cannot attribute it to the stride; the attribution "
        "rests on the layer declaring filter 2 and on the stored bytes being an "
        "exact wrong-stride shuffle of a conforming image. The register might "
        "say which row such a file evidences.",

    "T26, packed planar bool":
        "The mandated stride for a packed bool plane is 1, so the filter is the "
        "identity and the decoded image equals the stored bytes. A file "
        "exercising this instance is therefore byte-identical to a T4 file with "
        "filter 2 declared instead of 1. It is still worth building — a "
        "verifier that skips padding checks on filtered layers fails it — but "
        "the instance carries no information the filter field does not.",

    "§21.4 T21 and the §21.9 floor":
        "T21 forbids a declared Window_Size exceeding the tile's decoded size, "
        "while §21.9 guarantees a reader accepts Window_Size up to 8 MiB. For "
        "any tile under 8 MiB decoded the first bound is the binding one, so "
        "the guarantee never applies to a conforming file's tile frames. Not a "
        "contradiction, but the 8 MiB row reads as though it constrains tile "
        "decoding when only §18.2's metadata frames can reach it.",
}
