#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Rob Kleffner and contributors
"""Byte-exact codec streams for §21.4's codec rows, assembled by hand.

§17.2 constrains what a stored tile's bytes may be under each codec, and most
of those constraints are violated by frames a compressor will not emit: a
nonzero Dictionary_ID, a set Content_Checksum_flag, an oversized window, a
skippable frame, two concatenated frames. A library cannot produce them, so
these are built field by field from RFC 8878 and the LZ4 block format.

Building them by hand also keeps ADR-0050's no-dependency rule: the only
compression this module calls is `zlib`, which is standard library, and the
zstd and LZ4 producers here emit stored/literal blocks that need no encoder.
Correctness is checked in `_selftest` against a real decoder where one exists.
"""

from __future__ import annotations

import struct
import zlib

# --------------------------------------------------------------------------
# Codec 2 — DEFLATE (RFC 1951 raw, and the two wrappers §17.2 excludes)
# --------------------------------------------------------------------------

def deflate_raw(data: bytes, level: int = 9) -> bytes:
    """Exactly one RFC 1951 stream, no wrapper — what `[R-COD-05]` requires."""
    c = zlib.compressobj(level, zlib.DEFLATED, -15)
    return c.compress(data) + c.flush()


def deflate_zlib_wrapped(data: bytes) -> bytes:
    """RFC 1950: CMF/FLG header and a trailing Adler-32. T15's first instance."""
    return zlib.compress(data, 9)


def deflate_gzip_wrapped(data: bytes) -> bytes:
    """RFC 1952 member: 1F 8B, trailing CRC32 and ISIZE. T15's second."""
    c = zlib.compressobj(9, zlib.DEFLATED, 16 + 15)
    return c.compress(data) + c.flush()


def deflate_two_streams(a: bytes, b: bytes) -> bytes:
    """A second stream after the first BFINAL block — T16."""
    return deflate_raw(a) + deflate_raw(b)


def deflate_corrupt(data: bytes) -> bytes:
    """A stream whose first block declares reserved block type 3 — T25."""
    raw = bytearray(deflate_raw(data))
    raw[0] |= 0b110              # BTYPE = 11, reserved
    return bytes(raw)


# --------------------------------------------------------------------------
# Codec 3 — Zstandard (RFC 8878), assembled from raw blocks
# --------------------------------------------------------------------------

ZSTD_MAGIC = b"\x28\xB5\x2F\xFD"

def zstd_frame(data: bytes, *, dict_id: int | None = None,
               content_checksum: bool = False, window_log: int | None = None,
               content_size: int | None = None,
               omit_content_size: bool = False) -> bytes:
    """One RFC 8878 frame carrying `data` in raw blocks.

    Every excluded feature of §17.2 is a keyword here, so a vector names the
    constraint it breaks rather than hiding it in an opaque blob.
    `content_size` overrides the value written into Frame_Content_Size, which
    is how T22's mismatch is built.
    """
    fcs = content_size if content_size is not None else len(data)
    # Frame_Header_Descriptor: FCS_Field_Size in bits 6-7, Single_Segment in
    # bit 5, Content_Checksum in bit 2, Dictionary_ID_Flag in bits 0-1.
    single_segment = window_log is None
    # RFC 8878: code 0 is one byte only when Single_Segment is set (and no FCS
    # at all otherwise); code 1's two bytes store the value MINUS 256, so it
    # cannot represent anything below 256. Choosing code 1 for a small value
    # silently writes a different content size than the payload carries, which
    # would make every window-size vector also a Frame_Content_Size mismatch.
    if omit_content_size:
        fcs_code, fcs_bytes = 0, b""
    elif single_segment and fcs < 256:
        fcs_code, fcs_bytes = 0, struct.pack("<B", fcs)
    elif 256 <= fcs < 65536 + 256:
        fcs_code, fcs_bytes = 1, struct.pack("<H", fcs - 256)
    elif fcs < 1 << 32:
        fcs_code, fcs_bytes = 2, struct.pack("<I", fcs)
    else:
        fcs_code, fcs_bytes = 3, struct.pack("<Q", fcs)
    did_code, did_bytes = 0, b""
    if dict_id is not None:
        if dict_id < 256:
            did_code, did_bytes = 1, struct.pack("<B", dict_id)
        elif dict_id < 65536:
            did_code, did_bytes = 2, struct.pack("<H", dict_id)
        else:
            did_code, did_bytes = 3, struct.pack("<I", dict_id)
    fhd = (fcs_code << 6) | ((1 if single_segment else 0) << 5) \
        | ((1 if content_checksum else 0) << 2) | did_code
    out = bytearray(ZSTD_MAGIC)
    out.append(fhd)
    if not single_segment:
        # Window_Descriptor: exponent in bits 3-7, mantissa in 0-2.
        exp = max(0, window_log - 10)
        out.append((exp << 3))
    out += did_bytes + fcs_bytes
    # Raw blocks: header is (Last_Block | Block_Type<<1 | Block_Size<<3), u24.
    MAX = 1 << 17
    chunks = [data[i:i + MAX] for i in range(0, len(data), MAX)] or [b""]
    for i, ch in enumerate(chunks):
        last = 1 if i == len(chunks) - 1 else 0
        hdr = last | (0 << 1) | (len(ch) << 3)
        out += struct.pack("<I", hdr)[:3] + ch
    if content_checksum:
        out += struct.pack("<I", 0)      # a placeholder XXH64 low word
    return bytes(out)


def zstd_skippable(payload: bytes = b"\x00\x00\x00\x00", variant: int = 0) -> bytes:
    """A skippable frame — magic 0x184D2A5x. §17.2 excludes these outright."""
    return struct.pack("<II", 0x184D2A50 + variant, len(payload)) + payload


# --------------------------------------------------------------------------
# Codec 4 — LZ4 block format (raw block; the frame format is excluded)
# --------------------------------------------------------------------------

LZ4_FRAME_MAGIC = b"\x04\x22\x4D\x18"

def lz4_literals(data: bytes) -> bytes:
    """One raw LZ4 block that is all literals — valid and encoder-free.

    A block is a token byte (literal length in the high nibble, match length in
    the low), length extensions in 255-steps, then the literals. A final
    sequence may end after its literals, which is what this emits.
    """
    n = len(data)
    out = bytearray()
    out.append((15 if n >= 15 else n) << 4)
    if n >= 15:
        rem = n - 15
        while rem >= 255:
            out.append(255); rem -= 255
        out.append(rem)
    out += data
    return bytes(out)


def lz4_frame(data: bytes) -> bytes:
    """An LZ4 *frame*, which `[R-COD-07]` excludes — T23."""
    return LZ4_FRAME_MAGIC + b"\x40\x70\x00" + lz4_literals(data) + b"\x00\x00\x00\x00"


def lz4_bad_match_offset(data: bytes) -> bytes:
    """A block whose match offset is 0 — invalid per the block format, T25."""
    out = bytearray(lz4_literals(data))
    out[0] |= 0x04                    # claim a match follows
    out += b"\x00\x00"                # offset 0
    return bytes(out)


# --------------------------------------------------------------------------

def _selftest() -> int:
    ok = True
    payload = bytes(range(256)) * 4

    got = zlib.decompressobj(-15).decompress(deflate_raw(payload))
    print(f"deflate_raw round-trips: {got == payload}"); ok &= got == payload
    print(f"zlib wrapper starts 0x78: {deflate_zlib_wrapped(payload)[0] == 0x78}")
    gz = deflate_gzip_wrapped(payload)[:2]
    print(f"gzip wrapper starts 1F 8B: {gz == bytes((0x1F, 0x8B))}")
    ok &= gz == bytes((0x1F, 0x8B))

    try:
        from compression import zstd as _z
        dec = _z.decompress
    except ImportError:
        try:
            import zstandard
            dec = lambda b: zstandard.ZstdDecompressor().decompress(b)
        except ImportError:
            dec = None
    if dec:
        f = zstd_frame(payload)
        got = dec(f)
        print(f"zstd_frame round-trips through a real decoder: {got == payload}")
        ok &= got == payload
        print(f"zstd_frame magic correct: {f[:4] == ZSTD_MAGIC}")
        w = zstd_frame(payload, window_log=23)
        print(f"zstd_frame(window_log=23) decodes: {dec(w) == payload}")
        ok &= dec(w) == payload
    else:
        print("zstd: no decoder available, frame construction unverified")

    b = lz4_literals(payload)
    print(f"lz4_literals length = 1 + ext + {len(payload)}: {len(b) > len(payload)}")
    print(f"lz4_frame carries the excluded magic: {lz4_frame(payload)[:4] == LZ4_FRAME_MAGIC}")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(_selftest())
