# SPDX-License-Identifier: Apache-2.0
"""§21.3 rows L26–L52 — the layer record's declaration constraints.

Every vector damages the `pair` seed's `bad` layer and leaves `ok`
untouched, so each reject-layer file carries the intact sibling
[R-VEC-04] requires: without it the file cannot distinguish a reader
that scopes its refusal from one that rejects the whole file, which
[R-CNF-12] permits.

Two habits run through the file and are worth stating once.

*Sentinelling.* §19.3 lists the layer-access validations as a set, not
a sequence, so a file carrying two layer-scope defects evidences
neither row: a reader may report either. Many declaration defects
would drag a second, tile-scope defect in with them — changing a
channel's type changes the tile's decoded size, so codec 1's equality
([R-COD-04]) breaks; declaring an alignment makes the seed's stored
tile misaligned ([R-SLB-01]); declaring bool makes the seed's tile
bytes illegal ([R-SER-08]). Where that happens the vector replaces
`bad`'s single index entry with the sentinel (§15.2). An unstored
tile has no decoded bytes to contradict, and §16.2 says in as many
words that a run with no stored tiles imposes nothing. The tile's
former bytes become slack, which no requirement constrains
([R-CNT-21]).

*Carving.* L34's rank instance shortens the payload's parse: §7.4
requires the payload to parse exactly, the trailing fixed fields
landing on its end with no residue, so dropping the dimension entries
leaves bytes over — an independent [R-CNT-18] violation at the same
scope and tier, which would make the file evidence for neither row.
That vector therefore rewrites the freed span so the parse still
lands exactly. `carve` spreads one byte string across consecutive
named fields, taking every width from the seed's own layout map, so
the rewrite names fields and never offsets. L34's channel-count
instance needs the same treatment and cannot get it; SKIPPED says why.
"""
import struct

from tarn_build import crc32c
from tarn_vectors import SEEDS, Patch, Vector

u8 = lambda v: struct.pack("<B", v)
u16 = lambda v: struct.pack("<H", v)
u32 = lambda v: struct.pack("<I", v)
u64 = lambda v: struct.pack("<Q", v)

_BLOB, _LAY = SEEDS["pair"]()


def _field(f: str) -> bytes:
    """The seed's own bytes for a named field."""
    o, w = _LAY[f]
    return _BLOB[o:o + w]


def carve(fields: list[str], data: bytes, note: str = "") -> list[Patch]:
    """Spread `data` across consecutive named fields, by their widths.

    The fields must be adjacent and in payload order; the widths come
    from the seed layout, so the split is not a restatement of any
    offset. A length mismatch raises at import rather than producing a
    file whose payload no longer parses exactly.
    """
    out, i = [], 0
    for f in fields:
        w = _LAY[f][1]
        out.append(Patch(f, data[i:i + w], note))
        i += w
    if i != len(data):
        raise ValueError(f"carve: fields hold {i} B, data is {len(data)} B")
    return out


#: §15.2's sentinel: the tile is addressed but not stored.
SENTINEL = [
    Patch("layer[bad].entry[0].offset", b"\xff" * 8, "§15.2 sentinel"),
    Patch("layer[bad].entry[0].length", b"\xff" * 8, "§15.2 sentinel"),
    Patch("layer[bad].entry[0].crc", None, "§15.2: a sentinel's crc is 0"),
]
#: sentinelling rewrites an index entry, so §15.4's chain repairs first
REPAIR_IDX = ["index:bad", "directory.crc", "trailer.crc"]
REPAIR_DIR = ["directory.crc", "trailer.crc"]

#: The variable-length span of `bad`'s payload — d dimension entries
#: then C channel entries, between channel_count and index_encoding —
#: is addressable in two runs, not one: the layout map names every
#: dimension entry's extent and tile extent but not its *name* field,
#: so each dimension name (2 bytes here: prefix 0x01 and one letter)
#: is a fixed island a recipe cannot write. Any rewrite of the span
#: must therefore parse those islands as they stand.
SPAN_A = ["layer[bad].dim[0].extent", "layer[bad].dim[0].tile_extent"]
SPAN_B = ["layer[bad].dim[1].extent", "layer[bad].dim[1].tile_extent",
          "layer[bad].chan[0].name", "layer[bad].chan[0].type",
          "layer[bad].chan[0].fill"]

# Facts the vectors below rely on, asserted against the seed rather
# than assumed, so a seed change fails loudly instead of silently
# retargeting a row.
_REGION = _field("layer[bad].index_region")
_ENTRY, _SEGS = _REGION[:20], _REGION[20:]
_TILE_OFF = struct.unpack("<Q", _field("layer[bad].entry[0].offset"))[0]
_COCA = struct.unpack("<I", _field("layer[bad].crc_of_crc_array"))[0]
assert struct.unpack("<Q", _field("layer[bad].entry_count"))[0] == 1
assert len(_REGION) == 24 and len(_SEGS) == 4      # 1 entry, 1 segment CRC
assert _TILE_OFF % 512 != 0                        # L42 / L44 depend on it
assert _COCA ^ 0x5A5A5A5A != 0                     # L39's wrong value is wrong

VECTORS = [
    # -- L29 · entry_count = 0 with a nonzero crc_of_crc_array ------------
    # §7.4 fixes crc_of_crc_array at 0 when entry_count is 0. Reaching
    # entry_count = 0 legitimately needs the geometry to derive 0 addressed
    # tiles (else L22) and the extent slot to be (0, 0) (else L23), so the
    # vector empties one dimension — §21.6 records extent 0 as a valid,
    # empty layer — and clears the slot. The index region and the tile it
    # addressed become slack ([R-CNT-21]).
    Vector("TV-0270", "pair",
           "layer `bad` has entry_count 0 with a nonzero crc_of_crc_array", False,
           patches=[Patch("layer[bad].dim[0].extent", u64(0),
                          "E₀ = 0 ⇒ N = 0 addressed tiles (§21.6, valid)"),
                    Patch("layer[bad].entry_count", u64(0),
                          "matches the derived count, so L22 stays clean"),
                    Patch("layer[bad].extent_offset", u64(0),
                          "slot (0,0) is what entry_count 0 requires (L23)"),
                    Patch("layer[bad].extent_length", u64(0)),
                    Patch("layer[bad].crc_of_crc_array", u32(0xC0FFEE01),
                          "the defect: nonzero where §7.4 fixes 0")],
           repair=REPAIR_DIR,
           row="L29", rule="R-CNT-23", outcome="reject-layer",
           scope={"kind": "layer", "name": "bad"}, detected="layer access",
           must_not_serve=["layer:bad"], serves=["ok"]),

    # -- L30 · S = 0 with a nonzero A_slab --------------------------------
    # A_slab is a legal value in itself (4096 is a power of two in
    # 1 … 2^62): the sole defect is that it is declared with no slab.
    Vector("TV-0271", "pair",
           "layer `bad` declares slab alignment 4096 with slab S = 0", False,
           patches=[Patch("layer[bad].slab_alignment", u64(4096),
                          "§7.4: A_slab is 0 when S is 0")],
           repair=REPAIR_DIR,
           row="L30", rule="R-CNT-23", outcome="reject-layer",
           scope={"kind": "layer", "name": "bad"}, detected="layer access",
           must_not_serve=["layer:bad"], serves=["ok"]),

    # -- L31 · S ≠ 0 with an A_slab outside the power-of-two domain -------
    # Three files, one per alternative the condition states. Each declares
    # S = 1, so §16.2's run invariants would bind — the seed's stored tile
    # sits at an offset no such A_slab divides — and each therefore
    # sentinels the tile: "A run with no stored tiles imposes nothing".
    Vector("TV-0272", "pair",
           "layer `bad` declares S = 1 with A_slab 0 (the included case)", False,
           patches=SENTINEL + [Patch("layer[bad].slab", u64(1))],
           repair=REPAIR_IDX,
           row="L31", rule="R-CNT-23", outcome="reject-layer",
           scope={"kind": "layer", "name": "bad"}, detected="layer access",
           must_not_serve=["layer:bad"], serves=["ok"]),
    Vector("TV-0273", "pair",
           "layer `bad` declares S = 1 with A_slab 3, not a power of two", False,
           patches=SENTINEL + [Patch("layer[bad].slab", u64(1)),
                               Patch("layer[bad].slab_alignment", u64(3))],
           repair=REPAIR_IDX,
           row="L31", rule="R-CNT-23", outcome="reject-layer",
           scope={"kind": "layer", "name": "bad"}, detected="layer access",
           must_not_serve=["layer:bad"], serves=["ok"]),
    Vector("TV-0274", "pair",
           "layer `bad` declares S = 1 with A_slab 2^63, above the 2^62 ceiling",
           False,
           patches=SENTINEL + [Patch("layer[bad].slab", u64(1)),
                               Patch("layer[bad].slab_alignment", u64(1 << 63),
                                     "a power of two, but out of domain")],
           repair=REPAIR_IDX,
           row="L31", rule="R-CNT-23", outcome="reject-layer",
           scope={"kind": "layer", "name": "bad"}, detected="layer access",
           must_not_serve=["layer:bad"], serves=["ok"]),

    # -- L32 · fill length prefix ≠ the type's element size ---------------
    # A single predicate over two fields (§21.1: one instance), so either
    # field may carry the change; retyping the channel keeps §7.4's framing
    # intact, where editing the prefix would shift every following field
    # and test [R-CNT-18] instead. uint64's element size is 8, the fill
    # prefix stays 1. The tile is sentinelled because retyping also
    # changes the decoded size, which codec 1 ties to the entry's length.
    Vector("TV-0275", "pair",
           "layer `bad` channel `v` is uint64 with a 1-byte fill", False,
           patches=SENTINEL + [Patch("layer[bad].chan[0].type", u16(9),
                                     "uint64: element size 8, fill prefix 1")],
           repair=REPAIR_IDX,
           row="L32", rule="R-CNT-23", outcome="reject-layer",
           scope={"kind": "layer", "name": "bad"}, detected="layer access",
           must_not_serve=["layer:bad"], serves=["ok"]),

    # -- L33 · index_encoding other than 1 --------------------------------
    # Value 0 is TV-0005; these are the two remaining alternatives §7.4
    # names. [R-CNT-17]'s extent_length identity is stated "under
    # index_encoding 1", so an invalid encoding drags no L23 with it.
    Vector("TV-0276", "pair",
           "layer `bad` declares index_encoding 2 (reserved 2–0x7F)", False,
           patches=[Patch("layer[bad].index_encoding", u8(2))],
           repair=REPAIR_DIR,
           row="L33", rule="R-CNT-23", outcome="reject-layer",
           scope={"kind": "layer", "name": "bad"}, detected="layer access",
           must_not_serve=["layer:bad"], serves=["ok"]),
    Vector("TV-0277", "pair",
           "layer `bad` declares index_encoding 0x80 (experimental ≥ 0x80)", False,
           patches=[Patch("layer[bad].index_encoding", u8(0x80))],
           repair=REPAIR_DIR,
           row="L33", rule="R-CNT-23", outcome="reject-layer",
           scope={"kind": "layer", "name": "bad"}, detected="layer access",
           must_not_serve=["layer:bad"], serves=["ok"]),

    # -- L34 · a geometry field whose floor is 1 is 0 ---------------------
    # Three instances. T₀ = 0 needs nothing but the byte: the grid count
    # ⌈E₀/T₀⌉ stops being derivable, so [R-CNT-17]'s cross-check cannot be
    # evaluated, let alone violated. The tile is sentinelled because the
    # decoded size P·Q collapses to 0 with it.
    Vector("TV-0278", "pair",
           "layer `bad` has tile extent T₀ = 0 (instance: tile extent Tᵢ)", False,
           patches=SENTINEL + [Patch("layer[bad].dim[0].tile_extent", u64(0))],
           repair=REPAIR_IDX,
           row="L34", rule="R-GEO-01", outcome="reject-layer",
           scope={"kind": "layer", "name": "bad"}, detected="layer access",
           must_not_serve=["layer:bad"], serves=["ok"]),
    # rank 0 erases the dimension entries, so the span must re-parse as
    # channel entries alone, landing exactly on index_encoding. The two
    # dimension names survive as unwritable islands, so the rewrite reads
    # them as channel names: the first island (01 79) becomes channel
    # "y"'s name, the second (01 78) channel "x"'s, and C rises to 4 to
    # tile the remaining bytes with entries whose fill lengths match their
    # types. entry_count stays 1, which is what d = 0 derives (§11.2's
    # empty product is 1), and extent_length stays right for it.
    # The tile is sentinelled: Q is now 1+4+8+4 = 17.
    #
    #   [island "y"] type fill │ "cccc" entry │ [island "x"] type fill │
    #   "ddd" entry │ — ending exactly where index_encoding begins.
    Vector("TV-0279", "pair",
           "layer `bad` declares rank d = 0 (instance: rank d)", False,
           patches=SENTINEL + [Patch("layer[bad].rank", u8(0)),
                               Patch("layer[bad].channel_count", u16(4))]
           + carve(SPAN_A,
                   u16(6) + u8(1) + bytes(1)                # ch "y": uint8
                   + u8(4) + b"cccc" + u16(8) + u8(4) + bytes(4),   # uint32
                   "d = 0 ⇒ the span re-parses as channel entries")
           + carve(SPAN_B,
                   u16(9) + u8(8) + bytes(8)                # ch "x": uint64
                   + u8(3) + b"ddd" + u16(12) + u8(4) + bytes(4),   # float32
                   "…continued past the second dimension-name island"),
           repair=REPAIR_IDX,
           row="L34", rule="R-GEO-01", outcome="reject-layer",
           scope={"kind": "layer", "name": "bad"}, detected="layer access",
           must_not_serve=["layer:bad"], serves=["ok"]),
    # (No TV-0280: L34's channel-count instance is in SKIPPED below.)

    # -- L35 · linearization other than 1 ---------------------------------
    # Value 2 (reserved 2–3) is TV-0006; these are the other three
    # alternatives [R-GEO-05] names.
    Vector("TV-0281", "pair",
           "layer `bad` declares linearization 0 (invalid)", False,
           patches=[Patch("layer[bad].linearization", u16(0))],
           repair=REPAIR_DIR,
           row="L35", rule="R-GEO-05", outcome="reject-layer",
           scope={"kind": "layer", "name": "bad"}, detected="layer access",
           must_not_serve=["layer:bad"], serves=["ok"]),
    Vector("TV-0282", "pair",
           "layer `bad` declares linearization 4 (reserved 4–0x7FFF)", False,
           patches=[Patch("layer[bad].linearization", u16(4))],
           repair=REPAIR_DIR,
           row="L35", rule="R-GEO-05", outcome="reject-layer",
           scope={"kind": "layer", "name": "bad"}, detected="layer access",
           must_not_serve=["layer:bad"], serves=["ok"]),
    Vector("TV-0283", "pair",
           "layer `bad` declares linearization 0x8000 (experimental)", False,
           patches=[Patch("layer[bad].linearization", u16(0x8000))],
           repair=REPAIR_DIR,
           row="L35", rule="R-GEO-05", outcome="reject-layer",
           scope={"kind": "layer", "name": "bad"}, detected="layer access",
           must_not_serve=["layer:bad"], serves=["ok"]),

    # -- L36 · channel type outside 1 … 13 --------------------------------
    # Four alternatives. An unassigned type has no element size, so
    # neither L32's fill cross-check nor the tile's decoded size can be
    # evaluated: the stored tile stays, contradicting nothing.
    Vector("TV-0284", "pair",
           "layer `bad` channel `v` declares type 0 (invalid)", False,
           patches=[Patch("layer[bad].chan[0].type", u16(0))],
           repair=REPAIR_DIR,
           row="L36", rule="R-TYP-03", outcome="reject-layer",
           scope={"kind": "layer", "name": "bad"}, detected="layer access",
           must_not_serve=["layer:bad"], serves=["ok"]),
    Vector("TV-0285", "pair",
           "layer `bad` channel `v` declares type 14 (reserved 14–19)", False,
           patches=[Patch("layer[bad].chan[0].type", u16(14))],
           repair=REPAIR_DIR,
           row="L36", rule="R-TYP-03", outcome="reject-layer",
           scope={"kind": "layer", "name": "bad"}, detected="layer access",
           must_not_serve=["layer:bad"], serves=["ok"]),
    Vector("TV-0286", "pair",
           "layer `bad` channel `v` declares type 20 (reserved 20–0x7FFF)", False,
           patches=[Patch("layer[bad].chan[0].type", u16(20))],
           repair=REPAIR_DIR,
           row="L36", rule="R-TYP-03", outcome="reject-layer",
           scope={"kind": "layer", "name": "bad"}, detected="layer access",
           must_not_serve=["layer:bad"], serves=["ok"]),
    Vector("TV-0287", "pair",
           "layer `bad` channel `v` declares type 0x8000 (experimental)", False,
           patches=[Patch("layer[bad].chan[0].type", u16(0x8000))],
           repair=REPAIR_DIR,
           row="L36", rule="R-TYP-03", outcome="reject-layer",
           scope={"kind": "layer", "name": "bad"}, detected="layer access",
           must_not_serve=["layer:bad"], serves=["ok"]),

    # -- L37 · a bool channel's fill byte is neither 0x00 nor 0x01 --------
    # bool's element size is 1, so the fill prefix stays correct and L32
    # is untouched. The tile is sentinelled: an interleaved bool channel
    # constrains every value byte to 0x00/0x01 ([R-SER-08]), which the
    # seed's payload 01 02 03 04 would break.
    Vector("TV-0288", "pair",
           "layer `bad` channel `v` is bool with fill byte 0x02", False,
           patches=SENTINEL + [Patch("layer[bad].chan[0].type", u16(1), "bool"),
                               Patch("layer[bad].chan[0].fill", u8(1) + b"\x02",
                                     "§13.2 admits only 0x00 and 0x01")],
           repair=REPAIR_IDX,
           row="L37", rule="R-TYP-07", outcome="reject-layer",
           scope={"kind": "layer", "name": "bad"}, detected="layer access",
           must_not_serve=["layer:bad"], serves=["ok"]),

    # -- L38 · layout other than 1 or 2 -----------------------------------
    # Two alternatives. With the layout undecided neither the addressed-
    # tile count (N or C·N) nor the decoded size is derivable, so no
    # second row can be asserted against the file.
    Vector("TV-0289", "pair",
           "layer `bad` declares layout 0 (invalid)", False,
           patches=[Patch("layer[bad].layout", u8(0))],
           repair=REPAIR_DIR,
           row="L38", rule="R-SER-06", outcome="reject-layer",
           scope={"kind": "layer", "name": "bad"}, detected="layer access",
           must_not_serve=["layer:bad"], serves=["ok"]),
    Vector("TV-0290", "pair",
           "layer `bad` declares layout 3 (reserved 3–255)", False,
           patches=[Patch("layer[bad].layout", u8(3))],
           repair=REPAIR_DIR,
           row="L38", rule="R-SER-06", outcome="reject-layer",
           scope={"kind": "layer", "name": "bad"}, detected="layer access",
           must_not_serve=["layer:bad"], serves=["ok"]),

    # -- L39 · crc_of_crc_array ≠ CRC over the segment-CRC array ----------
    # Repairing the directory and trailer but NOT the index chain is the
    # whole point: `index:bad` would recompute exactly the field the
    # vector is corrupting. Detected at tile use, not layer access, and
    # still reject-layer (§19.2, [R-IDX-04]).
    # NOTE: checksum_report models the segment CRCs, the entries and the
    # stored-tile CRCs, but not crc_of_crc_array, so this vector cannot
    # declare the checksum it breaks — see the summary.
    Vector("TV-0291", "pair",
           "layer `bad` crc_of_crc_array does not cover its segment-CRC array",
           False,
           patches=[Patch("layer[bad].crc_of_crc_array",
                          u32(_COCA ^ 0x5A5A5A5A),
                          "the array is untouched; only its CRC is wrong")],
           repair=REPAIR_DIR,
           row="L39", rule="R-IDX-04", outcome="reject-layer",
           scope={"kind": "layer", "name": "bad"}, detected="tile use",
           must_not_serve=["layer:bad"], serves=["ok"]),

    # -- L40 · a segment CRC ≠ CRC over that segment's entry bytes --------
    # The index region is rewritten whole — its 20 entry bytes verbatim,
    # its one segment CRC flipped — and crc_of_crc_array is recomputed
    # over the flipped array by hand, so the chain's outer link still
    # verifies and only the inner one fails. Rewriting the region by name
    # is the only way to reach the segment-CRC array, which the layout map
    # does not name separately.
    Vector("TV-0292", "pair",
           "layer `bad` segment 0's CRC does not cover its entry bytes", False,
           patches=[Patch("layer[bad].index_region",
                          _ENTRY + u32(struct.unpack("<I", _SEGS)[0]
                                       ^ 0x5A5A5A5A),
                          "entries verbatim, segment CRC flipped"),
                    Patch("layer[bad].crc_of_crc_array",
                          u32(crc32c(u32(struct.unpack("<I", _SEGS)[0]
                                         ^ 0x5A5A5A5A))),
                          "recomputed, so L39 stays intact")],
           repair=REPAIR_DIR,
           breaks_checksums=["index:bad.segment_crcs"],
           row="L40", rule="R-IDX-04", outcome="reject-layer",
           scope={"kind": "layer", "name": "bad"}, detected="tile use",
           must_not_serve=["layer:bad"], serves=["ok"]),

    # -- L41 · a nonzero alignment A outside its power-of-two domain ------
    # Three alternatives: not a power of two, a power of two below the
    # 512 floor, and one above the 2^62 ceiling. Each sentinels the tile,
    # since a declared A also binds every stored tile's offset (L42) and
    # the seed's tile is at an offset none of these divides.
    Vector("TV-0293", "pair",
           "layer `bad` declares alignment 1000, not a power of two", False,
           patches=SENTINEL + [Patch("layer[bad].alignment", u64(1000))],
           repair=REPAIR_IDX,
           row="L41", rule="R-SLB-01", outcome="reject-layer",
           scope={"kind": "layer", "name": "bad"}, detected="layer access",
           must_not_serve=["layer:bad"], serves=["ok"]),
    Vector("TV-0294", "pair",
           "layer `bad` declares alignment 256, below the 512 floor", False,
           patches=SENTINEL + [Patch("layer[bad].alignment", u64(256))],
           repair=REPAIR_IDX,
           row="L41", rule="R-SLB-01", outcome="reject-layer",
           scope={"kind": "layer", "name": "bad"}, detected="layer access",
           must_not_serve=["layer:bad"], serves=["ok"]),
    Vector("TV-0295", "pair",
           "layer `bad` declares alignment 2^63, above the 2^62 ceiling", False,
           patches=SENTINEL + [Patch("layer[bad].alignment", u64(1 << 63))],
           repair=REPAIR_IDX,
           row="L41", rule="R-SLB-01", outcome="reject-layer",
           scope={"kind": "layer", "name": "bad"}, detected="layer access",
           must_not_serve=["layer:bad"], serves=["ok"]),

    # -- L42 · a stored tile's offset is not a multiple of A --------------
    # A = 512 is a legal declaration, so the declaration rows stay clean
    # and only the placement is wrong. Verifier-detected: a reader serves
    # the layer unchanged, which is why the file must still serve `bad`.
    Vector("TV-0296", "pair",
           "layer `bad` declares alignment 512; its stored tile is unaligned",
           False,
           patches=[Patch("layer[bad].alignment", u64(512),
                          "legal A; the seed's tile offset is not a multiple")],
           repair=REPAIR_DIR,
           row="L42", rule="R-SLB-01", outcome="reject-layer",
           scope={"kind": "layer", "name": "bad"},
           detector="verifier", detected="certification",
           must_not_serve=[], serves=["ok", "bad"]),

    # -- L44 · a slab run's first stored tile is not A_slab-aligned -------
    # S = 1 and A_slab = 512 are both legal, and with one addressed tile
    # the run holds exactly one stored tile: L43's packing rule has no
    # second tile to relate, so only the run's first-offset rule fails.
    Vector("TV-0297", "pair",
           "layer `bad` declares S = 1, A_slab 512; run 0 starts unaligned",
           False,
           patches=[Patch("layer[bad].slab", u64(1)),
                    Patch("layer[bad].slab_alignment", u64(512))],
           repair=REPAIR_DIR,
           row="L44", rule="R-SLB-03", outcome="reject-layer",
           scope={"kind": "layer", "name": "bad"},
           detector="verifier", detected="certification",
           must_not_serve=[], serves=["ok", "bad"]),

    # -- L46 · codec other than 1 … 4 -------------------------------------
    # Three alternatives. [R-COD-04]'s length equality is codec 1's alone,
    # so the seed's 4-byte stored tile contradicts nothing under an
    # invalid codec, and no stream is ever attempted.
    Vector("TV-0298", "pair", "layer `bad` declares codec 0 (invalid)", False,
           patches=[Patch("layer[bad].codec", u16(0))],
           repair=REPAIR_DIR,
           row="L46", rule="R-COD-03", outcome="reject-layer",
           scope={"kind": "layer", "name": "bad"}, detected="layer access",
           must_not_serve=["layer:bad"], serves=["ok"]),
    Vector("TV-0299", "pair",
           "layer `bad` declares codec 5 (reserved 5–0x7FFF)", False,
           patches=[Patch("layer[bad].codec", u16(5))],
           repair=REPAIR_DIR,
           row="L46", rule="R-COD-03", outcome="reject-layer",
           scope={"kind": "layer", "name": "bad"}, detected="layer access",
           must_not_serve=["layer:bad"], serves=["ok"]),
    Vector("TV-0300", "pair",
           "layer `bad` declares codec 0x8000 (experimental)", False,
           patches=[Patch("layer[bad].codec", u16(0x8000))],
           repair=REPAIR_DIR,
           row="L46", rule="R-COD-03", outcome="reject-layer",
           scope={"kind": "layer", "name": "bad"}, detected="layer access",
           must_not_serve=["layer:bad"], serves=["ok"]),

    # -- L47 · codec 4 above the lz4 decoded-size bound -------------------
    # T₀ = 0x3F000001 with T₁ = 2 puts the decoded size P·Q at
    # 0x7E000002 — two bytes past [R-COD-07]'s 0x7E000000 — while the grid
    # stays 1 × 1, so entry_count = 1 still matches. Sentinelled: no LZ4
    # block is claimed for a tile this size.
    # NOTE: every witness of this row necessarily declares a tile far
    # above §21.9's 256 MiB acceptance floor, so a reader may decline it
    # as a resource limit ([R-ERR-04]) instead of as invalid — see the
    # summary.
    Vector("TV-0301", "pair",
           "layer `bad` declares codec 4 with decoded size 0x7E000002", False,
           patches=SENTINEL + [Patch("layer[bad].codec", u16(4), "lz4"),
                               Patch("layer[bad].dim[0].tile_extent",
                                     u64(0x3F000001),
                                     "P·Q = 0x7E000002 > 0x7E000000")],
           repair=REPAIR_IDX,
           row="L47", rule="R-COD-07", outcome="reject-layer",
           scope={"kind": "layer", "name": "bad"}, detected="layer access",
           must_not_serve=["layer:bad"], serves=["ok"]),

    # -- L48 · filter other than 1 or 2 -----------------------------------
    Vector("TV-0302", "pair", "layer `bad` declares filter 0 (invalid)", False,
           patches=[Patch("layer[bad].filter", u16(0))],
           repair=REPAIR_DIR,
           row="L48", rule="R-COD-09", outcome="reject-layer",
           scope={"kind": "layer", "name": "bad"}, detected="layer access",
           must_not_serve=["layer:bad"], serves=["ok"]),
    Vector("TV-0303", "pair",
           "layer `bad` declares filter 3 (reserved 3–0x7FFF)", False,
           patches=[Patch("layer[bad].filter", u16(3))],
           repair=REPAIR_DIR,
           row="L48", rule="R-COD-09", outcome="reject-layer",
           scope={"kind": "layer", "name": "bad"}, detected="layer access",
           must_not_serve=["layer:bad"], serves=["ok"]),
    Vector("TV-0304", "pair",
           "layer `bad` declares filter 0x8000 (experimental)", False,
           patches=[Patch("layer[bad].filter", u16(0x8000))],
           repair=REPAIR_DIR,
           row="L48", rule="R-COD-09", outcome="reject-layer",
           scope={"kind": "layer", "name": "bad"}, detected="layer access",
           must_not_serve=["layer:bad"], serves=["ok"]),

    # -- L50 · a reserved flag bit of a layer record is set ---------------
    # Bit 2 is TV-0009; this is the top of the reserved lane. MU and PE
    # keep §7.3's fixed 1/1, so neither L49 nor L52 rides along.
    Vector("TV-0305", "pair",
           "layer `bad` reserved flag bit 15 set (the lane's top bit)", False,
           patches=[Patch("layer[bad].flags", u16(0b11 | (1 << 15)))],
           repair=REPAIR_DIR,
           row="L50", rule="R-CNT-12", outcome="reject-layer",
           scope={"kind": "layer", "name": "bad"},
           detector="verifier", detected="certification",
           must_not_serve=[], serves=["ok", "bad"]),

    # -- L52 · a stored flag bit differs from §7.3's registry -------------
    # Instance: layer record flags. §7.3 fixes type 0x0001 at MU = 1,
    # PE = 1; this file stores MU = 0, PE = 1. Clearing MU rather than PE
    # is deliberate: MU = 1 with PE = 0 would also be L49's condition,
    # and the file would evidence two rows.
    Vector("TV-0306", "pair",
           "layer `bad` stores MU = 0 where the registry fixes MU = 1 "
           "(instance: layer record flags)", False,
           patches=[Patch("layer[bad].flags", u16(0b10),
                          "§7.3 fixes 0x0001 at MU = 1, PE = 1")],
           repair=REPAIR_DIR,
           row="L52", rule="R-CNT-22", outcome="reject-layer",
           scope={"kind": "layer", "name": "bad"},
           detector="verifier", detected="certification",
           must_not_serve=[], serves=["ok", "bad"]),
]


SKIPPED = {
    "L26": "Needs a sub-record of an unassigned type with MU = 1 inside the "
           "layer record's inline payload. A recipe patch replaces a named "
           "field with bytes of the same width; it cannot lengthen the "
           "payload, and no seed carries a layer sub-record. Reachable only "
           "by adding a seed whose layer record has one.",
    "L28": "Needs a type 0x0001 record nested as a sub-record — same reason "
           "as L26: no seed carries a sub-record and patches cannot add one.",
    "L34 (channel count C)": "The rank and tile-extent instances are "
           "TV-0279 and TV-0278. C = 0 has no isolable file in this seed: it "
           "frees the 6-byte channel entry, and §7.4's exact parse then "
           "demands the freed bytes be absorbed by the dimension entries — "
           "whose name fields the layout map does not address (their length "
           "prefixes are fixed at 1), so no arrangement of d dimension "
           "entries spans the freed width. Every alternative leaves residue "
           "or a truncated sub-record, an independent [R-CNT-18] defect at "
           "the same scope and tier. A seed whose layer carries longer "
           "dimension names, or a layout map that named them, would carry it.",
    "L43": "Needs two stored tiles inside one slab run so the second's "
           "offset can miss the first's end. Every layer of the `pair` seed "
           "addresses one tile, and raising entry_count would break both "
           "[R-CNT-17] cross-checks (geometry-derived count, and "
           "extent_length = entry_count × 20 + ⌈entry_count/2¹⁶⌉ × 4) — two "
           "further layer-scope defects. A seed with a multi-tile layer "
           "would carry it.",
    "L45": "The condition ranges over a sequence of generations: a commit "
           "changed an affected run and carried the declaration forward "
           "without re-establishing the invariants. A single committed "
           "generation cannot exhibit it distinguishably from L43/L44 — the "
           "superseded generation is slack, which no reader interprets "
           "([R-CNT-21], §9.5). See the summary: the row may have no "
           "single-file witness at all.",
    "L49": "Not isolable in format major 1. MU = 1 with PE = 0 on a layer "
           "record is simultaneously L52, since §7.3 fixes type 0x0001 at "
           "MU = 1, PE = 1; on a user-metadata sub-record it is likewise "
           "L52 (0x0002 is fixed at MU = 0, PE = 1); and on a sub-record of "
           "an unassigned type, MU = 1 is L26. No file can carry this "
           "condition alone. See the summary.",
    "L51": "Needs a user-metadata sub-record of a layer record whose "
           "document has unsorted object members. No seed carries a layer "
           "sub-record, and patches cannot add one (as L26).",
}

#: Rows this module covers in part only.
PARTIAL = {
    "L52": "The `layer record flags` instance is TV-0306. The `sub-record "
           "flags` instance needs a layer sub-record, which no seed carries "
           "and no patch can add.",
}
