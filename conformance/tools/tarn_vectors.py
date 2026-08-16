#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Rob Kleffner and contributors
"""Build the conformance corpus — gate G5.

Every vector is a seed plus a **recipe**: a named field, a new value, and the
list of checksums to repair afterwards. The repair list is the reason recipes
exist at all. Almost no mutation is one byte, because every field sits under a
covering checksum: editing `trailer.dir_offset` without repairing
`trailer.crc` produces a vector that trips the CRC check instead of the
dir-bounds check, so it silently tests a different register row than the one it
claims. Naming the repairs makes that reviewable.

Both the recipe and the resulting bytes are committed. The bytes so an
implementer needs no tooling; the recipe so a reviewer sees intent and CI can
prove the two still agree.

    python3 tarn_vectors.py --emit    # write conformance/vectors/
    python3 tarn_vectors.py           # list what would be written
"""

from __future__ import annotations

import hashlib
import json
import struct
import sys
from dataclasses import dataclass, field
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from tarn_build import (Channel, Layer, Record, build_with_layout,  # noqa: E402
                        crc32c, minimal)

REPO = Path(__file__).resolve().parents[2]
OUT = REPO / "conformance" / "vectors"


# --------------------------------------------------------------------------
# Seeds
# --------------------------------------------------------------------------

def seed_minimal():
    return build_with_layout([], [])


def seed_pair():
    """Two layers: `ok` carries recorded content, `bad` is the damage target.

    [R-VEC-04] requires every reject-layer and reject-tile vector to sit in a
    file with an intact sibling whose decoded content the manifest records —
    without it a vector cannot tell a reader that scopes its refusal from one
    that rejects the whole file, since [R-CNF-12] permits the latter.
    """
    ok = Layer("ok", extents=(2, 3), tile_extents=(2, 3), channels=[Channel("t", 12)],
               tiles=[struct.pack("<6I", 0x3F800000, 0x80000000, 0x7FC00001,
                                  0xC0000000, 0x00000000, 0x7F800000)])
    bad = Layer("bad", extents=(2, 2), tile_extents=(2, 2), channels=[Channel("v", 6)],
                tiles=[bytes([1, 2, 3, 4])])
    return build_with_layout([ok, bad])


def seed_sparse():
    """A layer whose tiles are mostly unstored: sentinel entries read as fill."""
    ok = Layer("ok", extents=(2, 3), tile_extents=(2, 3), channels=[Channel("t", 12)],
               tiles=[struct.pack("<6I", 0x3F800000, 0x80000000, 0x7FC00001,
                                  0xC0000000, 0x00000000, 0x7F800000)])
    sp = Layer("sparse", extents=(4, 4), tile_extents=(2, 2),
               channels=[Channel("v", 6, b"\x2A")],
               tiles=[bytes([9, 9, 9, 9]), None, None, None])
    return build_with_layout([ok, sp])


def seed_planar():
    """Planar layout, mixed channel types including bool (packed plane)."""
    ok = Layer("ok", extents=(2, 3), tile_extents=(2, 3), channels=[Channel("t", 12)],
               tiles=[struct.pack("<6I", 0x3F800000, 0x80000000, 0x7FC00001,
                                  0xC0000000, 0x00000000, 0x7F800000)])
    pl = Layer("planar", extents=(2, 4), tile_extents=(2, 4), layout=2,
               channels=[Channel("u", 7), Channel("m", 1, b"\x00")],
               tiles=[bytes(16), bytes(1)])       # u: 8 values x 2 B; m: ceil(8/8)
    return build_with_layout([pl, ok])


def seed_meta():
    """A top-level user-metadata record with a zstd-free (encoding 1) document."""
    doc = b'{"tarn.title":"vector"}'
    ext = doc + struct.pack("<I", crc32c(doc))
    ok = Layer("ok", extents=(2, 3), tile_extents=(2, 3), channels=[Channel("t", 12)],
               tiles=[struct.pack("<6I", 0x3F800000, 0x80000000, 0x7FC00001,
                                  0xC0000000, 0x00000000, 0x7F800000)])
    return build_with_layout([ok], [Record(0x0002, inline=b"\x01", extent=ext)])


SEEDS = {"minimal": seed_minimal, "pair": seed_pair, "sparse": seed_sparse,
         "planar": seed_planar, "meta": seed_meta}

def register_seed(name: str, fn, layers: list[str] | None = None) -> str:
    """Let a vectordef module contribute its own seed.

    Modules are exec'd by load_vectors(), so `from tarn_vectors import ...`
    inside one resolves to whichever module object is live — which is
    `__main__` when this file runs as a script. Registering through this
    function rather than mutating SEEDS directly means a module reaches the
    dictionaries apply_recipe() and verify() actually read, whichever that is.
    """
    for mod in (sys.modules.get("tarn_vectors"), sys.modules.get("__main__")):
        if mod is not None and hasattr(mod, "SEEDS"):
            mod.SEEDS[name] = fn
            if layers is not None:
                mod.LAYERS[name] = layers
    return name


_LAYER_CACHE: dict[str, list] = {}


def _seed_layers(seed: str) -> list:
    """The Layer declarations a seed was built from, for content derivation."""
    if seed in _LAYER_CACHE:
        return _LAYER_CACHE[seed]
    import inspect
    fn = SEEDS.get(seed)
    if fn is None:
        return []
    src_layers: list = []
    try:
        # Re-run the seed with build_with_layout captured, so we see its Layers.
        import tarn_build
        real = tarn_build.build_with_layout
        def spy(layers, records=None, **kw):
            src_layers.extend(layers)
            return real(layers, records, **kw)
        tarn_build.build_with_layout = spy
        g = fn.__globals__
        prev = g.get("build_with_layout")
        g["build_with_layout"] = spy
        try:
            fn()
        finally:
            tarn_build.build_with_layout = real
            if prev is not None:
                g["build_with_layout"] = prev
    except Exception:
        src_layers = []
    _LAYER_CACHE[seed] = src_layers
    return src_layers


# --------------------------------------------------------------------------
# Recipes
# --------------------------------------------------------------------------

@dataclass
class Patch:
    field: str                 # a name from the builder's layout map
    value: bytes | None = None  # replacement bytes; None ⇒ zero the field
    note: str = ""


@dataclass
class Vector:
    id: str
    seed: str
    title: str
    conforming: bool
    patches: list[Patch] = field(default_factory=list)
    repair: list[str] = field(default_factory=list)
    row: str | None = None
    #: which of the row's §21 Instances cell entries this vector exercises,
    #: verbatim (ADR-0064). None on a row whose cell reads —.
    instance: str | None = None
    rule: str | None = None
    outcome: str | None = None
    scope: dict | None = None
    detector: str = "reader"
    detected: str | None = None
    serves: list[str] = field(default_factory=list)
    must_not_serve: list[str] = field(default_factory=list)
    #: checksums this vector INTENDS to break. Every other checksum in the
    #: file must still verify, or the vector tests a rule it does not claim.
    breaks_checksums: list[str] = field(default_factory=list)

    @property
    def path(self) -> str:
        d = {"reject-file": "reject-file", "reject-layer": "reject-layer",
             "reject-tile": "reject-tile", "ignore-record": "ignore-record"}
        return f"{d.get(self.outcome, 'conforming')}/{self.id}.tarn"


def apply_recipe(v: Vector) -> bytes:
    blob, layout = SEEDS[v.seed]()
    buf = bytearray(blob)
    for p in v.patches:
        if p.field not in layout:
            raise KeyError(f"{v.id}: no field {p.field!r} in seed {v.seed!r}")
        off, width = layout[p.field]
        val = p.value if p.value is not None else bytes(width)
        if len(val) != width:
            raise ValueError(f"{v.id}: {p.field} is {width} B, patch is {len(val)} B")
        buf[off:off + width] = val
    for what in v.repair:
        if what == "directory.crc":
            d0, dl = layout["directory"]
            buf[d0 + dl - 4:d0 + dl] = struct.pack("<I", crc32c(bytes(buf[d0:d0 + dl - 4])))
        elif what == "trailer.crc":
            t, _ = layout["trailer"]
            buf[t + 60:t + 64] = struct.pack("<I", crc32c(bytes(buf[t:t + 60])))
        elif what.startswith("index:"):
            # §15.4's chain: a patched entry changes its segment's bytes, so the
            # segment CRC and then crc_of_crc_array must be recomputed, or the
            # reader rejects the LAYER at the index chain and never reaches the
            # entry — testing a different row than the vector claims.
            nm = what.split(":", 1)[1]
            eo, el = layout[f"layer[{nm}].index_region"]
            ec = struct.unpack("<Q", bytes(buf[slice(*_span(layout, f"layer[{nm}].entry_count"))]))[0]
            nseg = -(-ec // 65536)
            arr = eo + ec * 20
            for s in range(nseg):
                lo = eo + s * 65536 * 20
                hi = eo + min((s + 1) * 65536, ec) * 20
                buf[arr + 4 * s:arr + 4 * s + 4] = struct.pack("<I", crc32c(bytes(buf[lo:hi])))
            co, cw = layout[f"layer[{nm}].crc_of_crc_array"]
            buf[co:co + cw] = struct.pack("<I", crc32c(bytes(buf[arr:arr + 4 * nseg])))
        elif what.startswith("truncate:"):
            # §9.4/[R-LIF-05]: a physical length below committed_file_length.
            buf = buf[:int(what.split(":", 1)[1])]
        elif what.startswith("append:"):
            # [R-LIF-05]/F40: bytes past a completed commit, never truncated.
            buf += bytes.fromhex(what.split(":", 1)[1])
        else:
            raise KeyError(f"{v.id}: unknown repair {what!r}")
    return bytes(buf)


def _span(layout, key):
    off, w = layout[key]
    return off, off + w


def checksum_report(blob: bytes, layers: list[str]) -> dict[str, bool]:
    """Recompute every checksum the file carries and report which verify.

    This computes CRCs over byte ranges the structures name. It decodes no
    tile, returns no sample, and pronounces no file conforming — ADR-0052's
    line. Its purpose is isolation: a vector must carry the one defect it
    claims and no other, and a mutation that silently breaks a covering
    checksum tests the covering rule instead.
    """
    out: dict[str, bool] = {}
    F = len(blob)
    if F < 128:
        out["file.minimum_length"] = False   # [R-CNT-27]
        return out
    t = F - 64
    out["trailer.crc"] = crc32c(blob[t:t + 60]) == struct.unpack("<I", blob[t + 60:t + 64])[0]
    d0, dl = struct.unpack("<QQ", blob[t + 24:t + 40])
    cfl = struct.unpack("<Q", blob[t + 40:t + 48])[0]
    gates = (d0 >= 16 and dl >= 4 and d0 + dl <= t and cfl == F and cfl % 64 == 0)
    out["trailer.gates"] = gates
    if not gates:
        # §6.2's field gates fail, so a reader rejects at open and never fetches
        # the directory. Reporting a directory CRC here would invent a defect.
        return out
    out["directory.crc"] = (crc32c(blob[d0:d0 + dl - 4])
                            == struct.unpack("<I", blob[d0 + dl - 4:d0 + dl])[0])
    # walk records; for each layer verify its index chain and stored-tile CRCs
    p, end, li = d0, d0 + dl - 4, 0
    while p < end:
        ty, fl, il, eo, el = struct.unpack("<HHIQQ", blob[p:p + 24])
        if ty == 1 and li < len(layers):
            nm = layers[li]; li += 1
            # An extent slot a recipe has pointed outside the file cannot be
            # walked at all. Report the chain as broken rather than raising:
            # the vector declares exactly these breaks, and §19.2 puts the
            # slot's own validity at layer access, ahead of any index read.
            if el and (eo > len(blob) or el > len(blob) or eo + el > len(blob)):
                out[f"index:{nm}.segment_crcs"] = False
                out[f"entry:{nm}[0].wellformed"] = False
            elif el:
                ec = (el - 4 * (-(-((el // 20) if el else 0) // 65536) or 1)) // 20
                # recover entry_count exactly from the region size
                for cand in range(max(0, ec - 2), ec + 3):
                    if cand >= 0 and cand * 20 + -(-cand // 65536) * 4 == el:
                        ec = cand; break
                nseg = -(-ec // 65536)
                arr = eo + ec * 20
                ok = True
                for s in range(nseg):
                    lo, hi = eo + s * 65536 * 20, eo + min((s + 1) * 65536, ec) * 20
                    ok &= crc32c(blob[lo:hi]) == struct.unpack(
                        "<I", blob[arr + 4 * s:arr + 4 * s + 4])[0]
                out[f"index:{nm}.segment_crcs"] = ok
                for k in range(ec):
                    o, ln, c = struct.unpack("<QQI", blob[eo + 20 * k:eo + 20 * k + 20])
                    if o == 0xFFFFFFFFFFFFFFFF and ln == 0xFFFFFFFFFFFFFFFF:
                        continue                      # sentinel: reads as fill
                    wellformed = ln > 0 and o >= 16 and o + ln <= t
                    out[f"entry:{nm}[{k}].wellformed"] = wellformed
                    if wellformed:                    # §15.3 classifies first
                        out[f"tile:{nm}[{k}].crc"] = crc32c(blob[o:o + ln]) == c
        p += 24 + il
    return out


# The decoded content of seed `pair`'s intact layer, as [R-VEC-02] requires:
# floats as hexadecimal bit patterns, so no comparison depends on a formatter.
OK_CONTENT = {
    "layer": "ok",
    "geometry": {"rank": 2, "extents": [2, 3], "tile_extents": [2, 3]},
    "channels": [{"name": "t", "type": "float32", "fill": "0x00000000"}],
    "tiles": [{"disk_ordinal": 0, "stored": True,
               "values": ["0x3F800000", "0x80000000", "0x7FC00001",
                          "0xC0000000", "0x00000000", "0x7F800000"]}],
    "note": "1.0, -0.0, NaN payload 1, -2.0, +0.0, +Inf",
}

u16 = lambda v: struct.pack("<H", v)
u64 = lambda v: struct.pack("<Q", v)

#: Vectors withheld pending a maintainer decision. A vector that names the
#: wrong row is worse than a missing one: it evidences a rule it does not test.
CONTESTED = {
    # Resolved by ADR-0056: the row these claimed was deleted. §21.6 already
    # carried the identical condition as a defined behavior, and [R-CNT-15]
    # agreed with §21.6. TV-0636 ships the same bytes as the conforming vector
    # they always were.
    "TV-0538": ("the register row it claimed no longer exists (ADR-0056); the "
                "condition is §21.6's defined behavior, shipped as TV-0636"),
    "TV-0539": ("as TV-0538, sub-record instance of the deleted row"),
    # Rows whose condition, by the governing rule's own text, cannot be
    # witnessed independently of a neighbouring row. Not construction errors —
    # register findings, quarantined pending a maintainer decision.
    # Resolved by ADR-0057: all three rows were deleted. Each named a cause
    # or a writer obligation rather than a state a reader or verifier can
    # distinguish, and each is now a note beside its rule.
    "TV-0903": ("the row it claimed was deleted (ADR-0057): residue past a "
                "commit is observed as a trailer-gate failure, which §21.2 "
                "already registers"),
    "TV-0913": ("the row it claimed was deleted (ADR-0057); this is a "
                "slab-packing file, which §21.3 registers in its own right"),
    "TV-0914": ("the row it claimed was deleted (ADR-0057); this is a "
                "slab-alignment file, likewise registered"),
    "TV-0401": "superseded by codec_rows' codec-2 T3 vectors, which fire [R-SER-07] and nothing earlier",
    "TV-0402": "superseded by codec_rows' codec-2 T3 vectors, which fire [R-SER-07] and nothing earlier",
    "TV-0403": "superseded by codec_rows' codec-2 T3 vectors, which fire [R-SER-07] and nothing earlier",
    "TV-0404": "superseded by codec_rows' codec-2 T3 vectors, which fire [R-SER-07] and nothing earlier",
    "TV-0405": "superseded by codec_rows' codec-2 T3 vectors, which fire [R-SER-07] and nothing earlier",
    "TV-0406": "superseded by codec_rows' codec-2 T3 vectors, which fire [R-SER-07] and nothing earlier",
}


def load_vectors() -> list["Vector"]:
    """Vector definitions live in `vectordefs/`, one module per register
    section, so they can be authored and reviewed independently. Each module
    exports VECTORS: a list of Vector."""
    import importlib.util
    out = []
    d = Path(__file__).resolve().parent / "vectordefs"
    for mod in sorted(d.glob("*.py")):
        if mod.name.startswith("_"):
            continue
        spec_ = importlib.util.spec_from_file_location(f"vectordefs.{mod.stem}", mod)
        m = importlib.util.module_from_spec(spec_)
        sys.modules[spec_.name] = m
        spec_.loader.exec_module(m)
        out.extend(getattr(m, "VECTORS", []))
    out = [v for v in out if v.id not in CONTESTED]
    seen = {}
    for v in out:
        if v.id in seen:
            raise ValueError(f"duplicate vector id {v.id}")
        seen[v.id] = v
    return sorted(out, key=lambda v: v.id)


VECTORS = []  # populated in main()



_TYPE_NAME = {1: "bool", 2: "int8", 3: "int16", 4: "int32", 5: "int64",
              6: "uint8", 7: "uint16", 8: "uint32", 9: "uint64",
              10: "float16", 11: "bfloat16", 12: "float32", 13: "float64"}


def seed_content(seed: str, layer_name: str) -> dict | None:
    """The decoded content a reader must return for one layer of one seed.

    Derived from the seed's own declarations, so it cannot drift from the bytes
    the builder emits. [R-VEC-02] asks for the content of every scope a reader
    can read, with floating-point values as hexadecimal bit patterns.
    """
    layers = _seed_layers(seed)
    L = next((l for l in layers if l.name == layer_name), None)
    if L is None:
        return None
    from tarn_build import ELEMENT_SIZE
    tiles = []
    for k, payload in enumerate(L.resolved_tiles()):
        if payload is None:
            tiles.append({"disk_ordinal": k, "stored": False,
                          "reads_as": "fill, every position (§13.3)"})
            continue
        if L.layout == 1:
            widths = [ELEMENT_SIZE[c.type] for c in L.channels]
        else:
            widths = [ELEMENT_SIZE[L.channels[k // L.N].type]]
        vals, p, i = [], 0, 0
        while p + widths[i % len(widths)] <= len(payload):
            w = widths[i % len(widths)]
            vals.append("0x" + payload[p:p + w][::-1].hex().upper())
            p += w; i += 1
        tiles.append({"disk_ordinal": k, "stored": True, "values": vals})
    return {
        "layer": L.name,
        "geometry": {"rank": len(L.extents), "extents": list(L.extents),
                     "tile_extents": list(L.tile_extents)},
        "layout": "interleaved" if L.layout == 1 else "planar",
        "channels": [{"name": c.name, "type": _TYPE_NAME.get(c.type, c.type),
                      "fill": "0x" + (c.fill or bytes(ELEMENT_SIZE[c.type]))[::-1].hex().upper()}
                     for c in L.channels],
        "tiles": tiles,
    }


#: Which §21 Instances entry each vector exercises, verbatim (ADR-0064).
#: Derived by reading every vector title against its row's cell, then
#: validated mechanically: COV-05 fails if a string here is not present
#: in the row's cell, so rewording an instance surfaces the vectors that
#: need rechecking instead of silently remapping them.
INSTANCE_OF: dict[str, str] = {
    'TV-0916': 'bytes remaining after the frame, top-level extent',
    'TV-0917': 'bytes remaining after the frame, layer sub-record extent',
    'TV-0918': 'ill-formed source bytes in a key, top-level document',
    'TV-0919': 'ill-formed source bytes in a key, layer sub-record document',
    'TV-0920': 'unpaired-surrogate escape in a key, top-level document',
    'TV-0921': 'unpaired-surrogate escape in a key, layer sub-record document',
    'TV-0922': 'unpaired-surrogate escape in a string value, top-level document',
    'TV-0923': 'unpaired-surrogate escape in a string value, layer sub-record document',
    'TV-0924': 'layer record extent_offset',
    'TV-0925': 'layer record extent_length',
    'TV-0926': 'layer record extent_offset',
    'TV-0927': 'layer record extent_offset + extent_length',
    'TV-0928': 'sub-record extent_offset',
    'TV-0929': 'sub-record flags',
    'TV-0930': 'generation',
    'TV-0931': 'trailing residue',
    'TV-0003': 'trailer magic',
    'TV-0004': 'dir_offset',
    'TV-0005': 'index_encoding 0',
    'TV-0006': 'reserved 2-3',
    'TV-0007': '—',
    'TV-0008': '—',
    'TV-0009': 'layer record flags bits 2-15',
    'TV-0101': 'dir_offset',
    'TV-0102': 'dir_length',
    'TV-0103': 'committed_file_length',
    'TV-0104': 'generation',
    'TV-0105': 'front signature block bytes [0,8)',
    'TV-0106': 'trailer magic at F-64',
    'TV-0107': 'dir_offset',
    'TV-0108': 'dir_length',
    'TV-0109': 'committed_file_length',
    'TV-0110': 'non-layer top-level record extent_offset',
    'TV-0111': 'extent_length',
    'TV-0112': 'dir_offset + dir_length',
    'TV-0113': 'non-layer top-level record extent_offset + extent_length',
    'TV-0114': 'trailer (e.g. version_major and version_minor each written as u32)',
    'TV-0115': 'top-level record header',
    'TV-0116': 'layer record name',
    'TV-0117': 'magic bytes [0,8)',
    'TV-0118': 'reserved bytes [8,16)',
    'TV-0119': '—',
    'TV-0120': 'trailer magic',
    'TV-0121': 'dir_offset',
    'TV-0122': '—',
    'TV-0123': 'generation',
    'TV-0124': 'file_id',
    'TV-0125': 'trailer CRC',
    'TV-0126': 'trailer reserved [56,60)',
    'TV-0127': 'dir_length',
    'TV-0128': 'committed_file_length',
    'TV-0129': 'version_major',
    'TV-0130': 'version_major',
    'TV-0131': 'flags bits 0-15',
    'TV-0132': 'directory region CRC',
    'TV-0133': '—',
    'TV-0134': '—',
    'TV-0135': '—',
    'TV-0136': 'type',
    'TV-0137': 'flags bits 2-15',
    'TV-0138': '—',
    'TV-0139': 'flags bit 0',
    'TV-0140': 'flags bit 1',
    'TV-0141': 'record header',
    'TV-0142': 'inline_length',
    'TV-0143': 'extent_offset',
    'TV-0144': 'extent_length',
    'TV-0145': 'extent_offset',
    'TV-0146': '—',
    'TV-0147': 'stored-tile extents',
    'TV-0148': 'tile-index regions',
    'TV-0149': 'record extents',
    'TV-0150': 'directory region',
    'TV-0151': 'type',
    'TV-0200': 'dimension extent Eᵢ',
    'TV-0201': 'tile extent Tᵢ',
    'TV-0202': 'entry_count',
    'TV-0203': 'slab run length S',
    'TV-0204': 'N = ∏⌈Eᵢ/Tᵢ⌉',
    'TV-0205': 'P = ∏Tᵢ',
    'TV-0206': 'C·N (which dominates the max disk ordinal (C−1)·N + (N−1))',
    'TV-0207': 'P·Q (which dominates V = P·C)',
    'TV-0208': 'P·Bᶜ',
    'TV-0209': 'entry_count × 20 + ⌈entry_count/2¹⁶⌉ × 4',
    'TV-0210': 'any layer-record inline-payload field',
    'TV-0211': '—',
    'TV-0212': 'channel entry name',
    'TV-0213': 'dimension entry name',
    'TV-0214': '—',
    'TV-0215': '—',
    'TV-0216': 'dimension entry name',
    'TV-0217': 'channel entry name',
    'TV-0218': 'dimension entry name',
    'TV-0219': 'channel entry name',
    'TV-0220': 'dimension entry name',
    'TV-0221': 'channel entry name',
    'TV-0222': 'sub-record header',
    'TV-0223': 'layer record extent_length',
    'TV-0224': 'layer record extent slot',
    'TV-0225': 'layer record extent slot',
    'TV-0226': 'tile-index region',
    'TV-0227': '—',
    'TV-0228': '—',
    'TV-0229': 'extent_length',
    'TV-0230': 'extent_offset',
    'TV-0231': 'entry_count',
    'TV-0232': 'leading fixed fields (name … C)',
    'TV-0233': 'd dimension entries',
    'TV-0234': 'C channel entries',
    'TV-0235': 'trailing fixed fields (index_encoding, entry_count, crc_of_crc_array)',
    'TV-0270': '—',
    'TV-0271': '—',
    'TV-0272': 'A_slab = 0',
    'TV-0273': 'A_slab not a power of two',
    'TV-0274': 'A_slab above 2^62',
    'TV-0275': '—',
    'TV-0276': 'reserved 2-0x7F',
    'TV-0277': 'experimental >= 0x80',
    'TV-0278': 'tile extent Tᵢ',
    'TV-0279': 'rank d',
    'TV-0281': 'linearization 0',
    'TV-0282': 'reserved 4-0x7FFF',
    'TV-0283': 'experimental >= 0x8000',
    'TV-0284': 'type 0',
    'TV-0285': 'reserved 14-19',
    'TV-0286': 'reserved 20-0x7FFF',
    'TV-0287': 'experimental >= 0x8000',
    'TV-0288': '—',
    'TV-0289': 'layout 0',
    'TV-0290': 'reserved 3-255',
    'TV-0291': '—',
    'TV-0292': '—',
    'TV-0293': 'A not a power of two',
    'TV-0294': 'A below 512',
    'TV-0295': 'A above 2^62',
    'TV-0296': '—',
    'TV-0297': '—',
    'TV-0298': 'codec 0',
    'TV-0299': 'reserved 5-0x7FFF',
    'TV-0300': 'experimental >= 0x8000',
    'TV-0301': '—',
    'TV-0302': 'filter 0',
    'TV-0303': 'reserved 3-0x7FFF',
    'TV-0304': 'experimental >= 0x8000',
    'TV-0305': 'layer record flags bits 2-15',
    'TV-0306': 'layer record flags',
    'TV-0400': '—',
    'TV-0407': 'interleaved numeric fill bytes',
    'TV-0408': 'planar numeric plane fill bytes',
    'TV-0409': 'packed planar bool plane fill bit',
    'TV-0410': '—',
    'TV-0411': '—',
    'TV-0412': 'offset',
    'TV-0413': 'length',
    'TV-0414': '—',
    'TV-0415': '—',
    'TV-0416': 'offset',
    'TV-0417': 'length',
    'TV-0418': '—',
    'TV-0419': '—',
    'TV-0420': '—',
    'TV-0421': 'lz4 match offset 0 or match reaching past produced output',
    'TV-0500': 'encoding 0, top-level record',
    'TV-0501': 'encoding 0, layer sub-record',
    'TV-0502': 'reserved 3–0x7F, top-level record',
    'TV-0503': 'reserved 3–0x7F, layer sub-record',
    'TV-0506': 'top-level extent',
    'TV-0507': 'layer sub-record extent',
    'TV-0508': 'top-level extent',
    'TV-0509': 'layer sub-record extent',
    'TV-0510': 'missing frame magic, top-level extent',
    'TV-0511': 'missing frame magic, layer sub-record extent',
    'TV-0512': 'a skippable frame, top-level extent',
    'TV-0513': 'a skippable frame, layer sub-record extent',
    'TV-0514': 'a second frame, top-level extent',
    'TV-0515': 'a second frame, layer sub-record extent',
    'TV-0516': 'a nonzero dictionary ID, top-level extent',
    'TV-0517': 'a nonzero dictionary ID, layer sub-record extent',
    'TV-0518': 'the content-checksum flag set, top-level extent',
    'TV-0519': 'the content-checksum flag set, layer sub-record extent',
    'TV-0520': 'ill-formed source bytes in a string value, top-level document',
    'TV-0521': 'ill-formed source bytes in a string value, layer sub-record document',
    'TV-0522': 'empty key, top-level document',
    'TV-0523': 'empty key, layer sub-record document',
    'TV-0524': 'key with a code point in U+0000–U+001F, top-level document',
    'TV-0525': 'key with a code point in U+0000–U+001F, layer sub-record document',
    'TV-0526': 'not well-formed JSON, top-level document',
    'TV-0527': 'not well-formed JSON, layer sub-record document',
    'TV-0528': 'top-level value not an object, top-level document',
    'TV-0529': 'top-level value not an object, layer sub-record document',
    'TV-0530': 'leading U+FEFF, top-level document',
    'TV-0531': 'leading U+FEFF, layer sub-record document',
    'TV-0532': 'top-level document',
    'TV-0533': 'layer sub-record document',
    'TV-0534': 'top-level document',
    'TV-0535': 'layer sub-record document',
    'TV-0536': 'top-level document',
    'TV-0537': 'layer sub-record document',
    'TV-0700': 'interleaved P·Q, payload longer',
    'TV-0701': 'interleaved P·Q, payload shorter',
    'TV-0702': 'planar numeric P·Bᶜ, payload longer',
    'TV-0703': 'planar numeric P·Bᶜ, payload shorter',
    'TV-0704': 'packed planar bool ⌈P/8⌉, payload longer',
    'TV-0705': 'packed planar bool ⌈P/8⌉, payload shorter',
    'TV-0706': 'interleaved bool fill byte',
    'TV-0707': "deflate stream carrying a previous tile's history window",
    'TV-0708': "lz4 block whose match offset reaches back into a previous tile's output",
    'TV-0709': 'zlib RFC 1950 (CMF/FLG header + trailing Adler-32)',
    'TV-0710': 'gzip RFC 1952 member (1F 8B, trailing CRC32+ISIZE)',
    'TV-0711': '—',
    'TV-0712': 'a second concatenated compressed frame',
    'TV-0713': 'a skippable frame before the frame',
    'TV-0714': 'a skippable frame after the frame',
    'TV-0715': 'a skippable frame between two frames',
    'TV-0716': '—',
    'TV-0717': '—',
    'TV-0718': '—',
    'TV-0719': '—',
    'TV-0720': '—',
    'TV-0721': 'any codec',
    'TV-0722': 'deflate block type 3 / invalid Huffman table',
    'TV-0723': 'corrupt zstd block header',
    'TV-0724': 'planar numeric: channel element size',
    'TV-0725': 'interleaved: sample stride Q',
    'TV-0726': 'packed planar bool: identity s = 1',
    'TV-0802': '—',
    'TV-0803': '—',
    'TV-0804': '—',
    'TV-0805': '—',
    'TV-0806': 'trailing residue',
    'TV-0807': 'sub-record inline_length',
    'TV-0808': 'sub-record extent_length',
    'TV-0809': 'sub-record extent slot',
    'TV-0810': 'sub-record extent slot',
    'TV-0811': 'layer sub-record extents',
    'TV-0812': '—',
    'TV-0814': '—',
    'TV-0815': '—',
    'TV-0816': 'sub-record flags bits 2-15',
    'TV-0817': '—',
    'TV-0900': 'F (physical file size)',
    'TV-0901': 'committed_file_length',
    'TV-0902': 'committed_file_length',
    'TV-0904': '—',
    'TV-0905': '—',
    'TV-0910': '—',
    'TV-0915': '—',
    'TV-0906': 'sub-record extents',
    'TV-0907': 'sub-record extent_offset',
    'TV-0908': 'sub-record extent_length',
    'TV-0909': 'N·P',
    'TV-0911': 'channel count C',
    'TV-0912': '—',
    'TV-0950': 'stored-tile extents',
    'TV-0951': 'layer record',
    'TV-0954': 'sub-record',
    'TV-0953': 'tile-index entry',
}

def manifest(built: dict[str, bytes]) -> dict:
    out = []
    for v in VECTORS:
        blob = built[v.id]
        e = {
            "id": v.id, "file": v.path, "title": v.title,
            "sha256": hashlib.sha256(blob).hexdigest(), "size": len(blob),
            "conforming": v.conforming,
            "derivation": {
                "seed": v.seed,
                "patches": [{"field": p.field,
                             "value": (p.value or b"").hex() or "zero"}
                            for p in v.patches],
                "repair": v.repair,
            },
            "expect": {},
        }
        if v.row:
            e["violations"] = [{
                "row": v.row,
                "instance": v.instance or INSTANCE_OF.get(v.id, "—"),
                "rule": v.rule, "outcome": v.outcome,
                "scope": v.scope, "detector": v.detector, "detected": v.detected,
            }]
            e["expect"]["must_not_serve"] = v.must_not_serve
            e["expect"]["may_escalate_to"] = "file"
        served = [seed_content(v.seed, nm) for nm in v.serves]
        served = [c for c in served if c]
        if served:
            e["expect"]["serves"] = served
        elif v.conforming:
            # A conforming file with no layer still asserts something: it opens.
            e["expect"]["serves"] = []
            e["expect"]["opens"] = True
        out.append(e)
    return {
        "corpus_version": "1.0-rc",
        "license": "CC0-1.0",
        "note": ("Derivative evidence, never a definition of conformance: where a "
                 "recorded expectation and the specification disagree, the "
                 "specification governs and the vector is corrected (§24, ADR-0046)."),
        "vectors": out,
    }


LAYERS = {"minimal": [], "pair": ["ok", "bad"], "sparse": ["ok", "sparse"],
          "planar": ["planar", "ok"], "meta": ["ok"]}


def verify(built: dict[str, bytes]) -> list[str]:
    """Each vector must carry exactly the defect it claims.

    Every checksum in the file must verify except those the vector declares it
    breaks. A mutation that silently invalidates a covering checksum makes the
    reader reject at that checksum's rule, so the vector would evidence a row
    it does not name.
    """
    problems = []
    for v in VECTORS:
        rep = checksum_report(built[v.id], LAYERS[v.seed])
        broken = {k for k, ok in rep.items() if not ok}
        want = set(v.breaks_checksums)
        for extra in sorted(broken - want):
            problems.append(
                f"{v.id} ({v.row or 'conforming'}): breaks {extra}, which it does "
                f"not declare — it would test that checksum's rule instead")
        for missing in sorted(want - broken):
            problems.append(f"{v.id}: declares it breaks {missing}, but it verifies")
    return problems


def main() -> int:
    global VECTORS
    VECTORS = load_vectors()
    built = {}
    for v in VECTORS:
        built[v.id] = apply_recipe(v)
    problems = verify(built)
    if problems:
        print("ISOLATION FAILURES\n")
        for p in problems:
            print(f"  ✗ {p}")
        print()
        if "--emit" in sys.argv:
            return 1
    else:
        print("isolation: every vector carries exactly the defect it claims\n")
    m = manifest(built)

    if "--emit" not in sys.argv:
        print(f"{len(VECTORS)} vectors\n")
        for v in VECTORS:
            b = built[v.id]
            tag = "conforming" if v.conforming else f"{v.outcome} [{v.row}]"
            print(f"  {v.id}  {len(b):>6} B  {tag:<22} {v.title}")
        rows = {v.row for v in VECTORS if v.row}
        print(f"\nregister rows covered by this slice: {len(rows)} — {', '.join(sorted(rows))}")
        return 0

    for sub in ("conforming", "reject-file", "reject-layer",
                "reject-tile", "ignore-record"):
        (OUT / sub).mkdir(parents=True, exist_ok=True)
    keep = {v.path for v in VECTORS}
    for stale in sorted(OUT.rglob("*.tarn")):
        if str(stale.relative_to(OUT)) not in keep:
            stale.unlink()
    for v in VECTORS:
        (OUT / v.path).write_bytes(built[v.id])
    (OUT / "manifest.json").write_text(json.dumps(m, indent=2) + "\n")
    print(f"wrote {len(VECTORS)} vectors + manifest.json to {OUT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
