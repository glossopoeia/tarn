#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Rob Kleffner and contributors
"""Construct conforming TARN files from explicit declarations.

This emits bytes; it never reads a TARN file and makes no judgement about one.
Everything it writes follows the specification's own rules, cited per field, so
that a file it produces is evidence about the specification rather than about
this code. Its acceptance test is Appendix A: `python3 tarn_build.py --selftest`
must reproduce the specification's printed hex dump byte for byte, and must
reproduce §4.5's CRC check vectors.

Scope is fixed by ADR-0050 as extended by ADR-0052.
"""

from __future__ import annotations

import struct
import sys
from dataclasses import dataclass, field

# --------------------------------------------------------------------------
# §4.5 — CRC-32C, polynomial 0x1EDC6F41, reflected in and out, init and final
# XOR 0xFFFFFFFF, stored little-endian.
# --------------------------------------------------------------------------

_T = []
for _i in range(256):
    _c = _i
    for _ in range(8):
        _c = (_c >> 1) ^ (0x82F63B78 if _c & 1 else 0)
    _T.append(_c)


def crc32c(data: bytes, crc: int = 0xFFFFFFFF) -> int:
    t = _T
    for b in data:
        crc = t[(crc ^ b) & 0xFF] ^ (crc >> 8)
    return crc ^ 0xFFFFFFFF


def _crc_stream(chunks) -> int:
    crc = 0xFFFFFFFF
    t = _T
    for chunk in chunks:
        for b in chunk:
            crc = t[(crc ^ b) & 0xFF] ^ (crc >> 8)
    return crc ^ 0xFFFFFFFF


u8 = lambda v: struct.pack("<B", v)
u16 = lambda v: struct.pack("<H", v)
u32 = lambda v: struct.pack("<I", v)
u64 = lambda v: struct.pack("<Q", v)


def name(s: str) -> bytes:
    """§4.6 — a u8 length prefix and that many bytes of UTF-8."""
    b = s.encode("utf-8")
    if not 1 <= len(b) <= 255:
        raise ValueError(f"name must be 1..255 bytes, got {len(b)}")
    return u8(len(b)) + b


FRONT = b"\x89TARN\r\n\x1a" + b"\x00" * 8          # §6.1
TRAILER_MAGIC = b"\x8aNRAT\r\n\x1a"                # §6.2
SENTINEL = b"\xff" * 16 + b"\x00" * 4              # §15.2

ELEMENT_SIZE = {1: 1, 2: 1, 3: 2, 4: 4, 5: 8, 6: 1, 7: 2, 8: 4, 9: 8,
                10: 2, 11: 2, 12: 4, 13: 8}       # §12.1


@dataclass
class Channel:
    name: str
    type: int = 6                                  # uint8
    fill: bytes | None = None

    def encoded(self) -> bytes:
        size = ELEMENT_SIZE[self.type]
        f = self.fill if self.fill is not None else b"\x00" * size
        if len(f) != size:
            raise ValueError(f"fill for type {self.type} must be {size} bytes")
        return name(self.name) + u16(self.type) + u8(len(f)) + f


@dataclass
class Layer:
    name: str
    extents: tuple[int, ...] = (4, 4)
    tile_extents: tuple[int, ...] = (2, 2)
    dim_names: tuple[str, ...] = ("y", "x")
    channels: list[Channel] = field(default_factory=lambda: [Channel("v")])
    layout: int = 1                                # 1 interleaved, 2 planar
    linearization: int = 1
    codec: int = 1                                 # 1 none
    filter: int = 1                                # 1 none
    alignment: int = 0
    slab: int = 0
    slab_alignment: int = 0
    #: one entry per addressed tile, in disk-ordinal order; None = sentinel
    tiles: list[bytes | None] | None = None
    #: §7.4's trailing sub-record sequence, layer scope by containment
    sub_records: list = field(default_factory=list)

    # -- §11.2 grid arithmetic ---------------------------------------------
    @property
    def grid(self) -> tuple[int, ...]:
        return tuple(-(-e // t) for e, t in zip(self.extents, self.tile_extents))

    @property
    def N(self) -> int:
        n = 1
        for g in self.grid:
            n *= g
        return n

    @property
    def P(self) -> int:
        p = 1
        for t in self.tile_extents:
            p *= t
        return p

    @property
    def entry_count(self) -> int:
        """§11.2 — N interleaved, C·N planar."""
        return self.N if self.layout == 1 else len(self.channels) * self.N

    def decoded_size(self, disk_ordinal: int) -> int:
        """§14.2 / §14.3."""
        if self.layout == 1:
            Q = sum(ELEMENT_SIZE[c.type] for c in self.channels)
            return self.P * Q
        c = self.channels[disk_ordinal // self.N]
        return -(-self.P // 8) if c.type == 1 else self.P * ELEMENT_SIZE[c.type]

    def resolved_tiles(self) -> list[bytes | None]:
        if self.tiles is not None:
            if len(self.tiles) != self.entry_count:
                raise ValueError(
                    f"layer {self.name!r}: {len(self.tiles)} tiles for "
                    f"entry_count {self.entry_count}")
            return self.tiles
        return [bytes(self.decoded_size(k)) for k in range(self.entry_count)]


@dataclass
class Record:
    """A non-layer top-level record (§7.2)."""
    type: int
    inline: bytes = b""
    extent: bytes | None = None
    flags: int = 0b10                              # MU = 0, PE = 1


def build_with_layout(layers: list[Layer], records: list[Record] | None = None,
                      file_id: int = 0x0123456789ABCDEF, generation: int = 1,
                      version_minor: int = 0) -> tuple[bytes, dict]:
    """`build`, plus a map naming where every field landed.

    Vector recipes address fields by name — `trailer.dir_offset`,
    `layer[bad].index_encoding` — so that a mutation stays readable and stays
    correct when an unrelated declaration changes the file's geometry. Raw
    offsets in a recipe would be a restatement site of exactly the kind
    ADR-0049 came out of.
    """
    blob = build(layers, records, file_id, generation, version_minor)
    F = len(blob)
    t = F - 64
    layout: dict[str, tuple[int, int]] = {
        "front": (0, 16),
        "trailer": (t, 64),
        "trailer.magic": (t, 8),
        "trailer.version_major": (t + 8, 2),
        "trailer.version_minor": (t + 10, 2),
        "trailer.flags": (t + 12, 4),
        "trailer.generation": (t + 16, 8),
        "trailer.dir_offset": (t + 24, 8),
        "trailer.dir_length": (t + 32, 8),
        "trailer.committed_file_length": (t + 40, 8),
        "trailer.file_id": (t + 48, 8),
        "trailer.reserved": (t + 56, 4),
        "trailer.crc": (t + 60, 4),
    }
    d0, dl = struct.unpack("<QQ", blob[t + 24:t + 40])
    layout["directory"] = (d0, dl)
    layout["directory.crc"] = (d0 + dl - 4, 4)

    # Walk the record sequence to name each layer's fields.
    p = d0
    end = d0 + dl - 4
    li = 0
    while p < end:
        ty, fl, il, eo, el = struct.unpack("<HHIQQ", blob[p:p + 24])
        if ty == 1:
            nm = layers[li].name
            q = p + 24
            layout[f"layer[{nm}].record"] = (p, 24 + il)
            layout[f"layer[{nm}].flags"] = (p + 2, 2)
            layout[f"layer[{nm}].extent_offset"] = (p + 8, 8)
            layout[f"layer[{nm}].extent_length"] = (p + 16, 8)
            layout[f"layer[{nm}].index_region"] = (eo, el)
            n = blob[q]
            layout[f"layer[{nm}].name"] = (q, 1 + n)
            layout[f"layer[{nm}].name_len"] = (q, 1)
            layout[f"layer[{nm}].name_bytes"] = (q + 1, n)
            q += 1 + n
            for f, w in (("layout", 1), ("linearization", 2), ("codec", 2),
                         ("filter", 2), ("alignment", 8), ("slab", 8),
                         ("slab_alignment", 8), ("rank", 1), ("channel_count", 2)):
                layout[f"layer[{nm}].{f}"] = (q, w); q += w
            for di in range(len(layers[li].extents)):
                n = blob[q]
                layout[f"layer[{nm}].dim[{di}].name"] = (q, 1 + n)
                layout[f"layer[{nm}].dim[{di}].name_len"] = (q, 1)
                layout[f"layer[{nm}].dim[{di}].name_bytes"] = (q + 1, n)
                q += 1 + n
                layout[f"layer[{nm}].dim[{di}].extent"] = (q, 8); q += 8
                layout[f"layer[{nm}].dim[{di}].tile_extent"] = (q, 8); q += 8
            for ci in range(len(layers[li].channels)):
                n = blob[q]
                layout[f"layer[{nm}].chan[{ci}].name"] = (q, 1 + n)
                layout[f"layer[{nm}].chan[{ci}].name_len"] = (q, 1)
                layout[f"layer[{nm}].chan[{ci}].name_bytes"] = (q + 1, n)
                q += 1 + n
                layout[f"layer[{nm}].chan[{ci}].type"] = (q, 2); q += 2
                n = blob[q]; layout[f"layer[{nm}].chan[{ci}].fill"] = (q, 1 + n); q += 1 + n
            layout[f"layer[{nm}].index_encoding"] = (q, 1); q += 1
            layout[f"layer[{nm}].entry_count"] = (q, 8); q += 8
            layout[f"layer[{nm}].crc_of_crc_array"] = (q, 4); q += 4
            si = 0
            while q + 24 <= p + 24 + il:
                sty, sfl, sil, seo, sel = struct.unpack("<HHIQQ", blob[q:q + 24])
                layout[f"layer[{nm}].sub[{si}].header"] = (q, 24)
                layout[f"layer[{nm}].sub[{si}].type"] = (q, 2)
                layout[f"layer[{nm}].sub[{si}].flags"] = (q + 2, 2)
                layout[f"layer[{nm}].sub[{si}].inline_length"] = (q + 4, 4)
                layout[f"layer[{nm}].sub[{si}].extent_offset"] = (q + 8, 8)
                layout[f"layer[{nm}].sub[{si}].extent_length"] = (q + 16, 8)
                if sil:
                    layout[f"layer[{nm}].sub[{si}].inline"] = (q + 24, sil)
                if sel:
                    layout[f"layer[{nm}].sub[{si}].extent"] = (seo, sel)
                q += 24 + sil; si += 1
            # index entries, in disk-ordinal order
            for k in range(layers[li].entry_count):
                layout[f"layer[{nm}].entry[{k}]"] = (eo + 20 * k, 20)
                layout[f"layer[{nm}].entry[{k}].offset"] = (eo + 20 * k, 8)
                layout[f"layer[{nm}].entry[{k}].length"] = (eo + 20 * k + 8, 8)
                layout[f"layer[{nm}].entry[{k}].crc"] = (eo + 20 * k + 16, 4)
            li += 1
        else:
            layout[f"record[{ty:#06x}].header"] = (p, 24)
            layout[f"record[{ty:#06x}].inline"] = (p + 24, il)
            if el:
                layout[f"record[{ty:#06x}].extent"] = (eo, el)
        p += 24 + il
    return blob, layout


def build(layers: list[Layer], records: list[Record] | None = None,
          file_id: int = 0x0123456789ABCDEF, generation: int = 1,
          version_minor: int = 0) -> bytes:
    """Emit one complete generation, per §9.2's ordering.

    Front block, then payloads and index regions, then record extents, then the
    directory, then the pre-trailer pad, then the trailer.
    """
    records = records or []
    out = bytearray(FRONT)
    layer_index_slot: list[tuple[int, int]] = []
    layer_entries: list[bytes] = []

    for layer in layers:
        tiles = layer.resolved_tiles()
        entries = bytearray()
        for payload in tiles:
            if payload is None:
                entries += SENTINEL
                continue
            offset = len(out)
            out += payload
            entries += u64(offset) + u64(len(payload)) + u32(crc32c(payload))
        # §15.1 — entry array then the segment CRC array, contiguous, no padding
        seg_crcs = b"".join(
            u32(crc32c(bytes(entries[s * 65536 * 20:min((s + 1) * 65536,
                                                        layer.entry_count) * 20])))
            for s in range(-(-layer.entry_count // 65536)))
        region = bytes(entries) + seg_crcs
        if layer.entry_count == 0:
            layer_index_slot.append((0, 0))
            layer_entries.append(b"")
        else:
            layer_index_slot.append((len(out), len(region)))
            out += region
            layer_entries.append(seg_crcs)

    sub_slots: dict[int, tuple[int, int]] = {}
    for layer in layers:
        for sub in layer.sub_records:
            if sub.extent is None:
                sub_slots[id(sub)] = (0, 0)
            else:
                sub_slots[id(sub)] = (len(out), len(sub.extent))
                out += sub.extent

    record_slots: list[tuple[int, int]] = []
    for rec in records:
        if rec.extent is None:
            record_slots.append((0, 0))
        else:
            record_slots.append((len(out), len(rec.extent)))
            out += rec.extent

    # -- the directory (§7.1, §7.2, §7.4) ----------------------------------
    seq = bytearray()
    for layer, (off, ln), seg in zip(layers, layer_index_slot, layer_entries):
        inline = (
            name(layer.name) + u8(layer.layout) + u16(layer.linearization)
            + u16(layer.codec) + u16(layer.filter)
            + u64(layer.alignment) + u64(layer.slab) + u64(layer.slab_alignment)
            + u8(len(layer.extents)) + u16(len(layer.channels))
        )
        for dn, e, t in zip(layer.dim_names, layer.extents, layer.tile_extents):
            inline += name(dn) + u64(e) + u64(t)
        for ch in layer.channels:
            inline += ch.encoded()
        inline += (u8(1) + u64(layer.entry_count)
                   + u32(crc32c(seg) if layer.entry_count else 0))
        for sub in layer.sub_records:
            inline += (u16(sub.type) + u16(sub.flags) + u32(len(sub.inline))
                       + u64(sub_slots[id(sub)][0]) + u64(sub_slots[id(sub)][1])
                       + sub.inline)
        seq += u16(1) + u16(0b11) + u32(len(inline)) + u64(off) + u64(ln) + inline
    for rec, (off, ln) in zip(records, record_slots):
        seq += (u16(rec.type) + u16(rec.flags) + u32(len(rec.inline))
                + u64(off) + u64(ln) + rec.inline)

    dir_offset = len(out)
    directory = bytes(seq) + u32(crc32c(bytes(seq)))
    out += directory
    dir_length = len(directory)

    # §6.2 — the trailer occupies the final 64 bytes, at a 64-aligned offset.
    end = len(out)
    F = ((end + 63) // 64 + 1) * 64
    out += b"\x00" * (F - 64 - end)                # pre-trailer pad, zeroed by advice

    trailer = (TRAILER_MAGIC + struct.pack("<HHI", 1, version_minor, 0)
               + u64(generation) + u64(dir_offset) + u64(dir_length) + u64(F)
               + u64(file_id) + b"\x00" * 4)
    out += trailer + u32(crc32c(trailer))
    assert len(out) == F, (len(out), F)
    return bytes(out)


def minimal() -> bytes:
    """Appendix A's file: no layers, no records."""
    return build([], [])


# --------------------------------------------------------------------------

def _selftest() -> int:
    ok = True
    v = crc32c(b"123456789")
    print(f"CRC-32C('123456789') = 0x{v:08X}  expect 0xE3069283  "
          f"{'ok' if v == 0xE3069283 else 'FAIL'}")
    ok &= v == 0xE3069283
    v = crc32c(b"")
    print(f"CRC-32C('')          = 0x{v:08X}  expect 0x00000000  "
          f"{'ok' if v == 0 else 'FAIL'}")
    ok &= v == 0
    v = _crc_stream([SENTINEL] * 65536)
    print(f"CRC-32C(full sentinel segment) = 0x{v:08X}  expect 0xEECB3BB2  "
          f"{'ok' if v == 0xEECB3BB2 else 'FAIL'}")
    ok &= v == 0xEECB3BB2

    import re
    from pathlib import Path
    spec = None
    for parent in Path(__file__).resolve().parents:
        if (parent / "spec" / "tarn.md").exists():
            spec = (parent / "spec" / "tarn.md").read_text()
            break
    built = minimal()
    if spec:
        dump = re.search(r"```\n(0000  89 54.*?)\n```", spec, re.S).group(1)
        printed = bytes.fromhex("".join(re.findall(
            r"[0-9A-Fa-f]{2}", re.sub(r"^\w{4}  ", "", dump, flags=re.M))))
        same = printed == built
        print(f"Appendix A rebuild: {len(built)} bytes, "
              f"{'byte-identical to the printed dump' if same else 'DIFFERS'}")
        ok &= same
    else:
        print("Appendix A rebuild: spec/tarn.md not found, skipped")
    return 0 if ok else 1


if __name__ == "__main__":
    if "--selftest" in sys.argv:
        raise SystemExit(_selftest())
    sys.stdout.buffer.write(minimal())
