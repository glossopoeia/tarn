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
            if el:
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
                "row": v.row, "rule": v.rule, "outcome": v.outcome,
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
