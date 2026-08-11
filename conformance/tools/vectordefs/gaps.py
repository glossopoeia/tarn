# SPDX-License-Identifier: Apache-2.0
"""Instances the section modules left uncovered without recording them.

One entry so far: L19's `stored-tile extents` instance. §21.3's L19 names
three — stored-tile extents, the tile-index region, and layer sub-record
extents — and the corpus covered the second and third while no module's
SKIPPED mentioned the first. `[R-VEC-03]` promises a vector per named
instance, so a gap nobody records is a silent breach of the corpus's own
coverage claim rather than an honest limit.
"""
import struct

from tarn_vectors import Patch, Vector, register_seed
from tarn_build import Channel, Layer, build_with_layout

u64 = lambda v: struct.pack("<Q", v)


def _seed_two_tiles():
    """Two stored tiles carrying identical payloads, plus the intact sibling.

    Identical payloads matter: redirecting entry[1] onto entry[0]'s extent
    then leaves both entry CRCs verifying, so the file's only fault is the
    overlap itself and not a checksum the reader would reach first.
    """
    ok = Layer("ok", extents=(2, 3), tile_extents=(2, 3), channels=[Channel("t", 12)],
               tiles=[struct.pack("<6I", 0x3F800000, 0x80000000, 0x7FC00001,
                                  0xC0000000, 0x00000000, 0x7F800000)])
    two = Layer("two", extents=(2, 4), tile_extents=(2, 2),
                channels=[Channel("v", 6)],
                tiles=[bytes([1, 2, 3, 4]), bytes([1, 2, 3, 4])])
    return build_with_layout([ok, two])


_TWO = register_seed("two_tiles", _seed_two_tiles, layers=["ok", "two"])


VECTORS = [
    Vector(
        "TV-0950", _TWO,
        "L19 stored-tile extents: entry[1] redirected onto entry[0]'s extent",
        False,
        # §7.2: "a verifier MUST treat an intra-layer overlap — including a
        # stored extent overlapping its own layer's index region or sub-record
        # extents — as reject-layer". Here two stored extents of one layer
        # claim the same bytes.
        patches=[Patch("layer[two].entry[1].offset", None,
                       note="set to entry[0].offset by the repair below")],
        repair=["index:two", "directory.crc", "trailer.crc"],
        row="L19", rule="R-CNT-13", outcome="reject-layer",
        scope={"kind": "layer", "name": "two",
               "instance": "stored-tile extents"},
        detector="verifier", detected="certification",
        must_not_serve=["layer:two"], serves=["ok"]),
]

# The patch above zeroes entry[1].offset, which would be an offset below 16
# (row T8) rather than an overlap. Point it at entry[0]'s extent instead.
def _fix_offset():
    blob, layout = _seed_two_tiles()
    off0, _ = layout["layer[two].entry[0].offset"]
    return blob[off0:off0 + 8]


VECTORS[0].patches[0].value = _fix_offset()

VECTORS.append(Vector(
    "TV-0951", "pair",
    "L47 layer record flags MU = 1 with PE = 0", False,
    # §7.2: "Writers MUST NOT emit the combination MU = 1 with PE = 0; a
    # reader or updater encountering it MUST treat the record as PE = 1".
    # Type 0x0001's registry-fixed flags are MU = 1, PE = 1 (§7.3), so
    # clearing PE necessarily also makes the stored bits differ from the
    # registry — L50. Both are verifier rows at the same scope and tier, so
    # neither masks the other; the co-violation is declared rather than
    # hidden, since no file can carry L47 on a layer record without it.
    patches=[Patch("layer[bad].flags", struct.pack("<H", 0b01))],
    repair=["directory.crc", "trailer.crc"],
    row="L47", rule="R-CNT-12", outcome="reject-layer",
    scope={"kind": "layer", "name": "bad", "co_violates": ["L50"]},
    detector="verifier", detected="certification",
    must_not_serve=[], serves=["ok"]))


SKIPPED = {
    # Stale key, kept as evidence and re-pointed. This reason was written
    # against the L25 that existed before ADR-0057 deleted three rows and §21
    # renumbered contiguously; today's L25 is the reserved-range row TV-0915
    # covers. The condition described here is the nesting-depth one, which is
    # why the entry is keyed by its rule now rather than by a row number that
    # moves under it — the same drift ADR-0049 forbids relying on.
    "R-CNT-18:nesting": ("unreachable. Detecting nesting beyond two needs a sub-record "
            "whose payload this specification defines as holding records, "
            "and format major 1 registers exactly one such type — 0x0001, "
            "which as a sub-record is its own row (a layer record nested as "
            "a sub-record). An unassigned type's payload is opaque, and "
            "0x0002's is one byte ([R-MTA-03]), so no file can exhibit "
            "nesting without exhibiting a different row instead."),
}
