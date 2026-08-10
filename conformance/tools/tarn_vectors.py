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


SEEDS = {"minimal": seed_minimal, "pair": seed_pair}


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

VECTORS = [
    Vector("TV-0001", "minimal", "Appendix A's minimal file", True,
           serves=["file opens; zero layers"]),
    Vector("TV-0002", "pair", "two layers, one float32 tile of edge values", True,
           serves=["ok", "bad"]),

    Vector("TV-0003", "minimal", "trailer magic corrupted", False,
           patches=[Patch("trailer.magic", b"\x8aNRAT\r\n\x1b")],
           repair=["trailer.crc"],
           row="F11", rule="R-CNT-06", outcome="reject-file",
           scope={"kind": "file"}, detected="open",
           must_not_serve=["file"]),
    Vector("TV-0004", "pair", "trailer dir_offset = 15, inside the front block", False,
           patches=[Patch("trailer.dir_offset", u64(15))],
           repair=["trailer.crc"],
           breaks_checksums=["trailer.gates"],   # dir_offset < 16 IS a gate failure
           row="F12", rule="R-CNT-06", outcome="reject-file",
           scope={"kind": "file"}, detected="open",
           must_not_serve=["file"]),

    Vector("TV-0005", "pair", "layer `bad` declares index_encoding 0", False,
           patches=[Patch("layer[bad].index_encoding", b"\x00")],
           repair=["directory.crc", "trailer.crc"],
           row="L32", rule="R-CNT-23", outcome="reject-layer",
           scope={"kind": "layer", "name": "bad"}, detected="layer access",
           must_not_serve=["layer:bad"], serves=["ok"]),
    Vector("TV-0006", "pair", "layer `bad` declares linearization 2 (reserved)", False,
           patches=[Patch("layer[bad].linearization", u16(2))],
           repair=["directory.crc", "trailer.crc"],
           row="L34", rule="R-GEO-05", outcome="reject-layer",
           scope={"kind": "layer", "name": "bad"}, detected="layer access",
           must_not_serve=["layer:bad"], serves=["ok"]),

    Vector("TV-0007", "pair", "layer `bad` entry 0 has length 0", False,
           patches=[Patch("layer[bad].entry[0].length", u64(0))],
           # crc_of_crc_array sits in the layer record, so an index repair
           # propagates into the directory and then the trailer.
           repair=["index:bad", "directory.crc", "trailer.crc"],
           breaks_checksums=["entry:bad[0].wellformed"],
           row="T10", rule="R-IDX-03", outcome="reject-tile",
           scope={"kind": "tile", "layer": "bad", "disk_ordinal": 0},
           detected="tile use",
           must_not_serve=["tile:bad:0"], serves=["ok"]),
    Vector("TV-0008", "pair", "layer `bad` tile 0 fails its entry crc", False,
           patches=[Patch("layer[bad].entry[0].crc", b"\x00\x00\x00\x00")],
           repair=["index:bad", "directory.crc", "trailer.crc"],
           breaks_checksums=["tile:bad[0].crc"],
           row="T1", rule="R-CNT-20", outcome="reject-tile",
           scope={"kind": "tile", "layer": "bad", "disk_ordinal": 0},
           detected="tile use",
           must_not_serve=["tile:bad:0"], serves=["ok"]),

    Vector("TV-0009", "pair", "layer `bad` reserved flag bit 2 set", False,
           patches=[Patch("layer[bad].flags", u16(0b111))],
           repair=["directory.crc", "trailer.crc"],
           row="L49", rule="R-CNT-12", outcome="reject-layer",
           scope={"kind": "layer", "name": "bad"},
           detector="verifier", detected="certification",
           must_not_serve=[], serves=["ok", "bad"]),
]


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
        if "ok" in v.serves:
            e["expect"]["serves"] = [OK_CONTENT]
        out.append(e)
    return {
        "corpus_version": "1.0-rc",
        "license": "CC0-1.0",
        "note": ("Derivative evidence, never a definition of conformance: where a "
                 "recorded expectation and the specification disagree, the "
                 "specification governs and the vector is corrected (§24, ADR-0046)."),
        "vectors": out,
    }


LAYERS = {"minimal": [], "pair": ["ok", "bad"]}


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
    for v in VECTORS:
        (OUT / v.path).write_bytes(built[v.id])
    (OUT / "manifest.json").write_text(json.dumps(m, indent=2) + "\n")
    print(f"wrote {len(VECTORS)} vectors + manifest.json to {OUT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
