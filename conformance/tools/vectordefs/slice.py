# SPDX-License-Identifier: Apache-2.0
"""The vertical slice: one vector per outcome class, both detectors."""
import struct
from tarn_vectors import Vector, Patch, OK_CONTENT

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
           row="F8", rule="R-CNT-06", outcome="reject-file",
           scope={"kind": "file"}, detected="open",
           must_not_serve=["file"]),
    Vector("TV-0004", "pair", "trailer dir_offset = 15, inside the front block", False,
           patches=[Patch("trailer.dir_offset", u64(15))],
           repair=["trailer.crc"],
           breaks_checksums=["trailer.gates"],   # dir_offset < 16 IS a gate failure
           row="F9", rule="R-CNT-06", outcome="reject-file",
           scope={"kind": "file"}, detected="open",
           must_not_serve=["file"]),

    Vector("TV-0005", "pair", "layer `bad` declares index_encoding 0", False,
           patches=[Patch("layer[bad].index_encoding", b"\x00")],
           repair=["directory.crc", "trailer.crc"],
           row="L31", rule="R-CNT-23", outcome="reject-layer",
           scope={"kind": "layer", "name": "bad"}, detected="layer access",
           must_not_serve=["layer:bad"], serves=["ok"]),
    Vector("TV-0006", "pair", "layer `bad` declares linearization 2 (reserved)", False,
           patches=[Patch("layer[bad].linearization", u16(2))],
           repair=["directory.crc", "trailer.crc"],
           row="L33", rule="R-GEO-05", outcome="reject-layer",
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
           row="L47", rule="R-CNT-12", outcome="reject-layer",
           scope={"kind": "layer", "name": "bad"},
           detector="verifier", detected="certification",
           must_not_serve=[], serves=["ok", "bad"]),
]
