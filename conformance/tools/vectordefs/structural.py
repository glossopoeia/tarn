# SPDX-License-Identifier: Apache-2.0
"""Structural gaps: file length and placement, slabs, and the multi-structure
instances the single-tile seeds could not reach.

Three capabilities this module is built on, none of which the earlier rounds
had:

  * **`truncate:N` / `append:HEX`.** These change the *physical* file length
    without touching `committed_file_length`, which is the only way to build a
    file shorter than 128 bytes (F5), a file whose committed length is not
    64-aligned while still equalling the physical size (F13), and a file with
    bytes past a completed commit (F40). Every one of those rows was recorded
    as a tooling skip.
  * **`register_seed`.** A vectordef may contribute the file shape its rows
    need. Two are registered below: a layer with three packed tiles under a
    slab declaration (L41, L44, L2's N·P), and a layer carrying a §7.4
    sub-record (F33, L1).
  * **`Layer(sub_records=[...])`.** The sub-record instances of F33 and L1 name
    a container no seed carried.

Two ordering notes recur.

**§19.2 is the masking test, and simultaneity is not masking.** Several rows
here sit inside §6.2's *unordered* gate list — "MUST validate all of the
following" — where two gates read the same field. A vector whose file trips two
of those gates evidences neither more nor less than the reader's verdict, which
is identical for both (reject-file, file scope, at open). Where that happens it
is declared in the vector's `scope` under `co_violates`, never hidden.

**Slack is what makes several of these constructions legal.** Sentinelling an
index entry turns its former payload into slack, which `[R-CNT-21]` leaves
unconstrained; that is the mechanism behind both L44 instances, and it is
exactly what a commit that supersedes a tile leaves behind.
"""
import struct

from tarn_build import (Channel, Layer, Record, TRAILER_MAGIC,
                        build_with_layout, crc32c)
from tarn_vectors import Vector, Patch, SEEDS, register_seed

u8 = lambda v: struct.pack("<B", v)
u16 = lambda v: struct.pack("<H", v)
u32 = lambda v: struct.pack("<I", v)
u64 = lambda v: struct.pack("<Q", v)

BIT63 = 1 << 63                                   # first value outside §4.2
SENTINEL = b"\xff" * 16 + b"\x00" * 4             # §15.2
FILE_ID = 0x0123456789ABCDEF                      # tarn_build's default

REPAIR_DIR = ["directory.crc", "trailer.crc"]


def _ok_layer():
    """The intact sibling `[R-VEC-04]` requires, identical in every seed here
    to the one `pair` carries, so its recorded content is the same file over."""
    return Layer("ok", extents=(2, 3), tile_extents=(2, 3),
                 channels=[Channel("t", 12)],
                 tiles=[struct.pack("<6I", 0x3F800000, 0x80000000, 0x7FC00001,
                                    0xC0000000, 0x00000000, 0x7F800000)])


# --------------------------------------------------------------------------
# Seed `slabrun` — a slab-declared layer with three stored tiles.
#
# §16.2: interleaved, so the single block [0, N) holds run 0 = [0, 3) at
# S = 3. The builder packs a layer's tiles in ordinal order, and the slab
# layer is declared first so its tiles begin at offset 16: with A_slab = 16
# the run's first stored tile is aligned and its interior is packed, which is
# every invariant `[R-SLB-03]` states. The seed is therefore conforming, and
# each vector below breaks exactly one of the two invariants.
#
# Ordinals 1 and 2 carry byte-identical payloads. That is load-bearing for
# TV-0912: swapping their index entries changes byte *placement* without
# changing the layer's decoded content, so the file still records what every
# layer serves.
# --------------------------------------------------------------------------

_TILE_A = bytes([0x0A, 0x0B, 0x0C, 0x0D])
_TILE_B = bytes([0x1A, 0x1B, 0x1C, 0x1D])


def seed_slabrun():
    slab = Layer("slab", extents=(3, 4), tile_extents=(1, 4),
                 channels=[Channel("v", 6, b"\x00")],
                 slab=3, slab_alignment=16,
                 tiles=[_TILE_A, _TILE_B, _TILE_B])
    return build_with_layout([slab, _ok_layer()])


register_seed("slabrun", seed_slabrun, layers=["slab", "ok"])
_SLAB_BLOB, _SLAB = seed_slabrun()
_SLAB_TILE_OFF = [struct.unpack("<Q", _SLAB_BLOB[slice(
    _SLAB[f"layer[slab].entry[{k}].offset"][0],
    _SLAB[f"layer[slab].entry[{k}].offset"][0] + 8)])[0] for k in range(3)]
assert _SLAB_TILE_OFF == [16, 20, 24], _SLAB_TILE_OFF


# --------------------------------------------------------------------------
# Seed `subrec` — a layer record carrying a §7.4 sub-record.
#
# The sub-record's type is from the experimental range with MU = 0: §21.6
# makes such a record a defined ignore (`[R-CNT-15]`, `[R-EXT-03]`; TV-0636
# ships the top-level form as a conforming file), so the seed stays
# conforming and no reader ever reads the extent. A *user-metadata*
# sub-record would drag §18's document rules onto whatever bytes TV-0906
# redirects the extent at — R2/R3/R7, a second defect at extent use — which
# is the same reason f_rows.py's redirected top-level extents use an
# experimental type.
# --------------------------------------------------------------------------

def seed_subrec():
    host = Layer("host", extents=(2, 2), tile_extents=(2, 2),
                 channels=[Channel("v", 6, b"\x00")],
                 tiles=[bytes([1, 2, 3, 4])],
                 sub_records=[Record(0x8001, inline=b"", extent=b"\xA5" * 8)])
    return build_with_layout([_ok_layer(), host])


register_seed("subrec", seed_subrec, layers=["ok", "host"])
_SUB_BLOB, _SUB = seed_subrec()
_OK_TILE_OFF, _OK_TILE_LEN = 16, 24               # layer `ok`'s stored tile
assert _SUB["layer[host].sub[0].extent_offset"][1] == 8
assert struct.unpack("<Q", _SUB_BLOB[slice(
    _SUB["layer[ok].entry[0].offset"][0],
    _SUB["layer[ok].entry[0].offset"][0] + 8)])[0] == _OK_TILE_OFF


# --------------------------------------------------------------------------
# F13's replacement trailer, and F40's post-commit residue.
# --------------------------------------------------------------------------

_MIN_BLOB, _MIN = SEEDS["minimal"]()
assert len(_MIN_BLOB) == 128


def _trailer(dir_offset: int, dir_length: int, cfl: int, generation: int = 1,
             file_id: int = FILE_ID) -> bytes:
    """§6.2's 64 bytes, CRC included — a whole trailer written by `append:`
    rather than patched in place, because the defect is *where it sits*."""
    body = (TRAILER_MAGIC + struct.pack("<HHI", 1, 0, 0) + u64(generation)
            + u64(dir_offset) + u64(dir_length) + u64(cfl) + u64(file_id)
            + b"\x00" * 4)
    return body + u32(crc32c(body))


#: 8 bytes of pad plus a trailer, appended to the 128-byte minimal file: the
#: live trailer then begins at 136 and the file ends at 200.
_F15_APPEND = bytes(8) + _trailer(16, 4, 200)
assert len(_MIN_BLOB) + len(_F15_APPEND) == 200 and 200 % 64 == 8

#: F40's residue: 64 bytes of a payload write that a torn commit left behind.
#: Not zeros — zeros would be indistinguishable from a pre-trailer pad, and
#: the row is about bytes a writer actually wrote.
_F40_RESIDUE = bytes(range(64))
assert _F40_RESIDUE[:8] != TRAILER_MAGIC


# --------------------------------------------------------------------------
# The `meta` seed's top-level record header, rebuilt field by field.
# --------------------------------------------------------------------------

_META_BLOB, _META = SEEDS["meta"]()
_M_HDR = _META["record[0x0002].header"][0]
_M_TY, _M_FL, _M_IL, _M_EO, _M_EL = struct.unpack(
    "<HHIQQ", _META_BLOB[_M_HDR:_M_HDR + 24])


def _hdr(ty, flags, il=_M_IL, eo=_M_EO, el=_M_EL) -> bytes:
    return struct.pack("<HHIQQ", ty, flags, il, eo, el)


# --------------------------------------------------------------------------
# L32's channel-count instance: layer `bad` of `pair` rebuilt with C = 0.
#
# Setting the field alone frees the 6 bytes of the one channel entry, and
# §7.4's exact parse then finds 6 bytes of residue before index_encoding —
# an independent `[R-CNT-18]` defect at the same scope and tier (L23). The
# rebuild spends those 6 bytes on a *dimension name*, which no rule
# constrains beyond §4.6, so the record's length and the offset of every
# trailing field are unchanged and C = 0 is the only violation left.
# --------------------------------------------------------------------------

_PAIR_BLOB, _PAIR = SEEDS["pair"]()
_BAD_OFF, _BAD_LEN = _PAIR["layer[bad].record"]
_BAD_IDX_OFF, _BAD_IDX_LEN = _PAIR["layer[bad].index_region"]
_BAD_CRC_ARR = bytes(_PAIR_BLOB[slice(
    _PAIR["layer[bad].crc_of_crc_array"][0],
    _PAIR["layer[bad].crc_of_crc_array"][0] + 4)])


def _bad_c0() -> bytes:
    nm = lambda s: u8(len(s)) + s
    inline = (nm(b"bad") + u8(1) + u16(1) + u16(1) + u16(1)
              + u64(0) + u64(0) + u64(0) + u8(2) + u16(0)      # rank 2, C = 0
              + nm(b"y" * 7) + u64(2) + u64(2)                 # +6 bytes of name
              + nm(b"x") + u64(2) + u64(2)
              + u8(1) + u64(1) + _BAD_CRC_ARR)
    rec = struct.pack("<HHIQQ", 1, 0b11, len(inline),
                      _BAD_IDX_OFF, _BAD_IDX_LEN) + inline
    assert len(rec) == _BAD_LEN, f"{len(rec)} vs {_BAD_LEN}"
    return rec


# --------------------------------------------------------------------------

FILE = {"kind": "file"}


def _slab_vec(vid, title, patches, row, generation=None, serves=("ok",),
              instance=None):
    """A verifier-detected reject-layer against seed `slabrun`'s slab layer.

    §16.1/§16.2 place both slab invariants outside the reader's obligations —
    offsets are explicit, so placement is reader-invisible — so the file is
    served in full and it is certification the vector constrains.
    """
    scope = {"kind": "layer", "name": "slab"}
    if instance:
        scope["instance"] = instance
    if generation is not None:
        patches = list(patches) + [Patch("trailer.generation", u64(generation),
                                         "the commit this row ranges over")]
        scope["co_violates"] = [
            ("L41" if instance == "S" else "L42") +
            " — unavoidable: [R-SLB-04]'s 'the invariants were not "
            "re-established' *is* [R-SLB-03]'s invariant failing, and "
            "[R-LIF-08] confines a verifier to the live state. See "
            "SPEC_FINDINGS['L44']."]
    return Vector(vid, "slabrun", title, False, patches=list(patches),
                  repair=["index:slab"] + REPAIR_DIR,
                  row=row, rule="R-SLB-03" if row == "L41" else "R-SLB-04",
                  outcome="reject-layer", scope=scope,
                  detector="verifier", detected="certification",
                  must_not_serve=[], serves=list(serves))


VECTORS = [

    # ==================================================================
    # F5 `[R-CNT-27]` — below the 128-byte minimum. Two instances, and
    # they are two *fields*: the physical size, and the declared one.
    # ==================================================================
    # Instance 1. `truncate:` cuts the physical file to 64 bytes, leaving
    # the front block, the 4-byte directory and 44 bytes of the pad.
    # Nothing else in §21.2 can be reached in this file and nothing masks
    # it: §19.1 step 1 obtains F before step 2 fetches any trailer, and
    # [R-CNT-27]'s predicate is decidable from F alone. The trailer's
    # committed_file_length of 128 no longer describes the file (F17) and
    # the 64 bytes at [F-64, F) are not a trailer (F8) — but both of
    # those are steps this file is too short to have.
    Vector("TV-0900", "minimal",
           "F5 physical file size 64, below the 128-byte minimum "
           "(instance: F, the physical file size)", False,
           repair=["truncate:64"],
           breaks_checksums=["file.minimum_length"],
           row="F5", rule="R-CNT-27", outcome="reject-file",
           scope=dict(FILE, instance="F (physical file size)",
                      note="F17 and F8 are true of these bytes but "
                           "unreachable: §19.1 obtains F at step 1 and "
                           "fetches a trailer at step 2, and this file has no "
                           "step 2"),
           detected="open", must_not_serve=["file"]),

    # Instance 2. The file is 128 bytes and its trailer is intact; the
    # declared committed_file_length is 64. This instance has no isolable
    # witness — see SPEC_FINDINGS['F5'] — because [R-CNT-06] also
    # requires committed_file_length = F, so any value below 128 in a file
    # of at least 128 bytes trips F17 as well. Both gates sit in §6.2's
    # single unordered list, both take reject-file at open at file scope,
    # so the reader's verdict is the same under either reading.
    Vector("TV-0901", "minimal",
           "F5 trailer committed_file_length 64, below the 128-byte minimum "
           "(instance: committed_file_length)", False,
           patches=[Patch("trailer.committed_file_length", u64(64))],
           repair=["trailer.crc"],
           breaks_checksums=["trailer.gates"],
           row="F5", rule="R-CNT-27", outcome="reject-file",
           scope=dict(FILE, instance="committed_file_length",
                      co_violates=["F17 — committed_file_length ≠ F, "
                                   "unavoidable for this instance"]),
           detected="open", must_not_serve=["file"]),

    # ==================================================================
    # F13 `[R-CNT-06]` — committed_file_length not a multiple of 64.
    # ==================================================================
    # Built so that F17 stays clean, which is what the previous round
    # thought impossible: `append:` writes 8 bytes of pad and a complete
    # trailer, so the physical file is 200 bytes, the live trailer begins
    # at 136, and committed_file_length = 200 = F exactly. 200 mod 64 = 8.
    # The superseded trailer at [64, 128) is zeroed first: left in place
    # it would be a structure between the live directory's end and the
    # live trailer, which is F7. Everything the live trailer names — the
    # front block at [0, 16), the directory at [16, 20) — is untouched
    # and verifies, so the 64-alignment gate is the file's only defect.
    Vector("TV-0902", "minimal",
           "F13 committed_file_length 200, equal to the physical size but "
           "not a multiple of 64: the trailer begins at 136", False,
           patches=[Patch("trailer", bytes(64),
                          "the superseded trailer is zeroed into slack, so no "
                          "structure lies in the pre-trailer gap (F7)")],
           repair=["append:" + _F15_APPEND.hex()],
           breaks_checksums=["trailer.gates"],
           row="F13", rule="R-CNT-06", outcome="reject-file",
           scope=dict(FILE, instance="committed_file_length"),
           detected="open", must_not_serve=["file"]),

    # ==================================================================
    # F40 `[R-LIF-05]` — bytes past a completed commit, never truncated.
    # ==================================================================
    # The commit at [0, 448) is byte-perfect: §9.6's deliberate scan finds
    # its trailer at 384 and truncating to 448 restores the file exactly.
    # That is the whole point of the row — the default read path is
    # trailer-at-end-or-fail, and a reader that recovers this file by
    # scanning backward is the nonconforming party. The residue is 64
    # bytes of a payload write, so the tail read at [448, 512) carries no
    # trailer magic.
    Vector("TV-0903", "pair",
           "F40 64 bytes of a torn append past a completed commit: the tail "
           "read at [F-64, F) is payload residue, not a trailer", False,
           repair=["append:" + _F40_RESIDUE.hex()],
           breaks_checksums=["trailer.crc", "trailer.gates"],
           row="F40", rule="R-LIF-05", outcome="reject-file",
           scope=dict(FILE, instance="physical file bytes beyond "
                                     "committed_file_length",
                      note="the committed state at [0, 448) is intact and "
                           "recoverable by §9.6; a reader MUST NOT scan back "
                           "to it. F17 is true of these bytes and unreachable: "
                           "§6.2 validates the magic before any field gate, "
                           "and the tail carries none"),
           detected="open", must_not_serve=["file"]),

    # ==================================================================
    # F25 `[R-CNT-12]` — a non-layer top-level record at MU = 1, PE = 0.
    # ==================================================================
    # The previous round recorded this unreachable. It is reachable, and
    # the reason the skip gave is the reason to build it *here*: on type
    # 0x0002 the combination differs from §7.3's registry in both bits, so
    # the file also carries F28. Both rows are verifier-detected at
    # certification, both are file scope, and [R-CNT-22] has the reader
    # apply the registry's fixed semantics regardless — so no reader-tier
    # check fires at all and nothing is masked. The alternative the skip
    # preferred, an unassigned type, is strictly worse: MU = 1 there is
    # F35, which a reader rejects at open, ahead of certification.
    Vector("TV-0904", "meta",
           "F25 the user-metadata record carries MUST_UNDERSTAND = 1 with "
           "PRESERVE_ON_EDIT = 0", False,
           patches=[Patch("record[0x0002].header", _hdr(0x0002, 0b01),
                          "MU = 1, PE = 0")],
           repair=REPAIR_DIR,
           row="F25", rule="R-CNT-12", outcome="reject-file",
           scope=dict(FILE, co_violates=[
               "F28 (flags bit 0) — §7.3 fixes MU = 0 for type 0x0002",
               "F28 (flags bit 1) — §7.3 fixes PE = 1 for type 0x0002"]),
           detector="verifier", detected="certification",
           must_not_serve=[], serves=["ok"]),

    # ==================================================================
    # F36 `[R-CNT-15]` — a reserved-range type value at file scope.
    # ==================================================================
    # Type 0x0003, the first value of §10.2's reserved range, with MU = 0
    # so F35 (reserved range *with* MU = 1, reader, open) is absent and
    # the reader's behavior is §21.6's defined ignore. 0x0003 is not a
    # type §7.3 registers, so F28 does not apply either; the record's
    # extent slot and inline_length are the seed's own, valid and unread.
    # The violation is the emission, and only a verifier sees it.
    Vector("TV-0905", "meta",
           "F36 top-level record of reserved type 0x0003 with MU = 0", False,
           patches=[Patch("record[0x0002].header", _hdr(0x0003, 0b10))],
           repair=REPAIR_DIR,
           row="F36", rule="R-CNT-15", outcome="reject-file",
           scope=FILE,
           detector="verifier", detected="certification",
           must_not_serve=[], serves=["ok"]),

    # ==================================================================
    # F35 `[R-CNT-15]` — a reserved-range type value with MU = 1.
    # ==================================================================
    # As TV-0905 but with MU set, which is what moves detection from the
    # verifier to the reader at open and the outcome to a refusal of the
    # whole file. The reserved range is what F35 names; an experimental
    # type with MU = 1 is §21.6's second exception instead — a conforming
    # file a reader refuses — and TV-0152 carries that case.
    Vector("TV-0910", "meta",
           "F35 top-level record of reserved type 0x0003 with MU = 1", False,
           patches=[Patch("record[0x0002].header", _hdr(0x0003, 0b11))],
           repair=REPAIR_DIR,
           row="F35", rule="R-CNT-15", outcome="reject-file",
           scope=FILE, detected="open",
           must_not_serve=["file"]),

    # ==================================================================
    # F33 `[R-CNT-13]` — the sub-record-extent instance of the
    # double-claim row, the last of its seven the corpus can reach.
    # ==================================================================
    # Layer `host`'s sub-record extent is redirected onto layer `ok`'s
    # stored tile: two structures of two different layers claiming the
    # same 24 bytes. Same-layer overlap would be L18 instead, which is
    # why the sub-record sits on `host` and the tile on `ok`. Every
    # reader-tier gate on the slot passes — offset ≥ 16, both halves
    # nonzero, offset + length ≤ F − 64 — and the sub-record's type is
    # ignored, so nothing reads the extent. The seed's original 8-byte
    # extent becomes slack.
    Vector("TV-0906", "subrec",
           "F33 layer `host`'s sub-record extent covers layer `ok`'s stored "
           "tile (instance: sub-record extents)", False,
           patches=[Patch("layer[host].sub[0].extent_offset", u64(_OK_TILE_OFF)),
                    Patch("layer[host].sub[0].extent_length", u64(_OK_TILE_LEN))],
           repair=REPAIR_DIR,
           row="F33", rule="R-CNT-13", outcome="reject-file",
           scope=dict(FILE, instance="sub-record extents"),
           detector="verifier", detected="certification",
           must_not_serve=[], serves=["ok", "host"]),

    # ==================================================================
    # L1 `[R-ENC-03]` — the sub-record halves of the u64-domain row.
    # ==================================================================
    # The row's Instances cell reads "extent_offset; extent_length (layer
    # record and sub-record slots)": four instances, of which l_rows_a.py
    # builds neither of the sub-record pair (no seed carried one) and
    # neither of the layer-record pair (checksum_report dereferences a
    # layer's extent slot before gating its domain and raises). The
    # sub-record slot is not dereferenced by anything, so both of these
    # build.
    #
    # Each file also fails a later check that reads the same field — L17's
    # bound, L2's sum — but reaching either means *acting on* a value §4.2
    # puts outside the domain, which [R-ENC-05] forbids before validation.
    # The domain gate is the first check a conforming reader can perform.
    Vector("TV-0907", "subrec",
           "L1 layer `host` sub-record extent_offset = 2^63 "
           "(instance: extent_offset, sub-record slot)", False,
           patches=[Patch("layer[host].sub[0].extent_offset", u64(BIT63))],
           repair=REPAIR_DIR,
           row="L1", rule="R-ENC-03", outcome="reject-layer",
           scope={"kind": "layer", "name": "host",
                  "instance": "extent_offset (sub-record slot)"},
           detected="layer access",
           must_not_serve=["layer:host"], serves=["ok"]),
    Vector("TV-0908", "subrec",
           "L1 layer `host` sub-record extent_length = 2^63 "
           "(instance: extent_length, sub-record slot)", False,
           patches=[Patch("layer[host].sub[0].extent_length", u64(BIT63))],
           repair=REPAIR_DIR,
           row="L1", rule="R-ENC-03", outcome="reject-layer",
           scope={"kind": "layer", "name": "host",
                  "instance": "extent_length (sub-record slot)"},
           detected="layer access",
           must_not_serve=["layer:host"], serves=["ok"]),

    # ==================================================================
    # L2 `[R-ENC-04]` — the two remaining declaration-derived products.
    # ==================================================================
    # N·P. l_rows_a.py could not reach it: N ≥ 2 needs a layer with two or
    # more addressed tiles, and `pair` gives its damage layer one. Seed
    # `slabrun` gives three. T₁ = 2^62 with E₁ = 4 keeps the second grid
    # count at 1, so N stays 3 and entry_count still matches it (L21
    # clean) and the index region is still 3 × 20 + 4 bytes (L22 clean).
    # Every other product stays in domain: P = 2^62, P·Q = 2^62 at Q = 1,
    # C·N = 3, V = P·C = 2^62. Only N·P = 3·2^62 leaves it.
    #
    # The slab declaration is untouched and its invariants still hold —
    # the tiles did not move — so no verifier row rides along.
    Vector("TV-0909", "slabrun",
           "L2 layer `slab` T₁ = 2^62 with N = 3: N·P = 3·2^62 (instance: N·P)",
           False,
           patches=[Patch("layer[slab].dim[1].tile_extent", u64(1 << 62))],
           repair=REPAIR_DIR,
           row="L2", rule="R-ENC-04", outcome="reject-layer",
           scope={"kind": "layer", "name": "slab", "instance": "N·P"},
           detected="layer access",
           must_not_serve=["layer:slab"], serves=["ok"]),

    # (No vector for L2's V = P·C: see SKIPPED. A planar seed was built
    # for it and then discarded — §14.1 gives a *planar* tile's sequence
    # V = P, and only an interleaved one V = P·C, so the planar escape the
    # earlier skip reason imagined does not exist.)

    # ==================================================================
    # L32 `[R-GEO-01]` — the geometry floor's channel-count instance.
    # ==================================================================
    # See _bad_c0() above for why this is a whole-record patch. The tile
    # is sentinelled because Q is the sum over zero channels, so the
    # decoded size collapses to 0 and a stored tile would carry T14; a
    # sentinel entry is §21.6's defined "addressed but not stored" and
    # its former payload becomes slack. entry_count stays 1, which is
    # what the unchanged geometry derives, so L21 and L22 stay clean.
    Vector("TV-0911", "pair",
           "L32 layer `bad` declares channel count C = 0 (instance: channel "
           "count C)", False,
           patches=[Patch("layer[bad].entry[0]", SENTINEL,
                          "Q = 0 with C = 0, so no stored tile can have the "
                          "right decoded size"),
                    Patch("layer[bad].record", _bad_c0(),
                          "C = 0; the freed 6 bytes go to dimension 0's name, "
                          "so §7.4's parse still ends exactly at "
                          "index_encoding")],
           repair=["index:bad"] + REPAIR_DIR,
           row="L32", rule="R-GEO-01", outcome="reject-layer",
           scope={"kind": "layer", "name": "bad", "instance": "channel count C"},
           detected="layer access",
           must_not_serve=["layer:bad"], serves=["ok"]),

    # ==================================================================
    # L41 `[R-SLB-03]` — a stored tile inside a run not packed against
    # the previous stored tile.
    # ==================================================================
    # The row names three alternatives — gap, overlap, out-of-ordinal
    # placement — in a cell that counts one instance. This is the third:
    # entries 1 and 2 exchange offsets, so ordinal 1 sits at 24 where the
    # run requires 20, and ordinal 2 at 20, before the previous stored tile. The
    # two payloads are byte-identical, so both entry CRCs still verify
    # against the bytes they now address and the layer's decoded content
    # is unchanged — which is why this file still records what layer
    # `slab` serves. Run 0's first stored tile is still ordinal 0 at 16,
    # a multiple of A_slab = 16, so L42 stays clean.
    _slab_vec("TV-0912",
              "L41 layer `slab` run 0: ordinals 1 and 2 exchange offsets, so "
              "ordinal 1 begins 4 bytes past the previous stored tile's end",
              [Patch("layer[slab].entry[1].offset", u64(24)),
               Patch("layer[slab].entry[2].offset", u64(20))],
              "L41", serves=("ok", "slab")),

    # ADR-0076 enumerated the row's three named alternatives; TV-0912
    # above is out-of-ordinal placement. The gap: unstore the run's
    # middle tile. Sentinels are transparent to [R-SLB-03], so the run's
    # stored sequence is ordinal 0 ending at 20 and ordinal 2 at 24 —
    # four unclaimed bytes inside the run. The freed bytes fall to slack
    # and no other row fires (a sentinel is §21.6's defined behavior);
    # run 0 still starts at 16 = A_slab, so L42 stays clean. Ordinal 1
    # now reads as fill, so `serves` names `ok` alone.
    _slab_vec("TV-0932",
              "L41 layer `slab` run 0: ordinal 1 unstored, so ordinal 2 at "
              "24 begins 4 bytes past the previous stored tile's end at 20",
              [Patch("layer[slab].entry[1]", SENTINEL)],
              "L41", serves=("ok",)),

    # The overlap: ordinal 2's offset moved to 20 — ordinal 1's extent,
    # whose payload is byte-identical, so the entry's crc verifies over
    # the bytes it now addresses and the layer's decoded content is
    # unchanged. The run is not packed (offset 20 where the previous
    # stored tile ends at 24), and the same bytes co-satisfy the
    # intra-layer overlap row, inherently: an in-run overlap between
    # stored tiles is an overlap between two structures of one layer.
    # Outcomes agree (reject-layer), the T17/T18 precedent.
    _slab_vec("TV-0933",
              "L41 layer `slab` run 0: ordinal 2's offset is 20, inside "
              "ordinal 1's extent — the run overlaps where it should pack",
              [Patch("layer[slab].entry[2].offset", u64(20))],
              "L41", serves=("ok", "slab")),

    # ==================================================================
    # L44 `[R-SLB-04]` — a slab declaration carried across a commit that
    # changed an affected run. Two instances: the run length S, and the
    # slab alignment A_slab.
    # ==================================================================
    # Both files are generation 2 — the trailer's generation field is the
    # only in-file evidence a commit happened, since a verifier walks the
    # live state alone (§9.7, [R-LIF-08]) and the superseded generation is
    # slack no reader interprets. Both supersede one tile of run 0 by
    # sentinelling its entry, which is what a commit that drops a tile
    # leaves: the tile is addressed, not stored, its former payload is
    # slack ([R-CNT-21]), and the declaration was carried forward
    # unchanged instead of being re-established or cleared.
    #
    # Instance S: ordinal 1 goes. Ordinals 0 and 2 remain at 16 and 24,
    # and sentinels are transparent to run continuity, so the run is
    # required to be packed at 16 → 20 and is not. The run's first stored
    # tile is still 16-aligned, so the A_slab half of the invariant holds
    # and this file isolates the S half.
    _slab_vec("TV-0913",
              "L44 generation 2 carries S = 3 forward after superseding "
              "ordinal 1: run 0 is no longer packed (instance: S)",
              [Patch("layer[slab].entry[1]", SENTINEL,
                     "the commit dropped ordinal 1; its 4 bytes are slack")],
              "L44", generation=2, instance="S"),

    # Instance A_slab: ordinal 0 goes, so run 0's first *stored* tile
    # becomes ordinal 1 at offset 20, and 20 mod 16 = 4. Ordinals 1 and 2
    # are still packed at 20 → 24, so the contiguity half of the
    # invariant holds and this file isolates the alignment half.
    _slab_vec("TV-0914",
              "L44 generation 2 carries A_slab = 16 forward after superseding "
              "ordinal 0: run 0's first stored tile is at 20 (instance: A_slab)",
              [Patch("layer[slab].entry[0]", SENTINEL,
                     "the commit dropped ordinal 0; its 4 bytes are slack")],
              "L44", generation=2, instance="A_slab"),
]


#: Rows and instances of this assignment already carrying a vector elsewhere.
#: §21.8 asks for at least one vector per instance; a second construction
#: under a second id would put two files in the corpus claiming one row.
COVERED_ELSEWHERE = {
    "L42": "TV-0297 (vectordefs/l_rows_b.py) — seed `pair`'s layer `bad` "
           "declares S = 1 and A_slab = 512 over a stored tile at offset 64. "
           "Verified: 64 mod 512 = 64, the run holds exactly one stored tile "
           "so L41's packing rule has no second tile to relate, and both "
           "declarations are legal. The row is closed.",
}


#: Instances this module leaves open. Every reason below was re-derived
#: against the seeds and the harness as they now stand, not carried forward.
SKIPPED = {
    "F33:trailer": (
        "unreachable, and re-verified against the sub-record slot the new "
        "seed adds. A structure overlapping the live trailer must extend past "
        "F − 64, and every claimant is gated there by a reader rule that "
        "fires strictly before certification: the directory by [R-CNT-06] "
        "(F10), a top-level record extent by [R-CNT-13] (F32), a layer "
        "record's *or sub-record's* extent by [R-CNT-13] (L17), a tile-index "
        "entry by [R-IDX-03] (T9). Nothing else can claim a byte."),
    "F33:front signature block": (
        "unreachable, mirror image, and likewise re-verified for sub-records: "
        "a claimant needs an offset below 16, and every offset is gated at "
        "≥ 16 before certification — dir_offset by [R-CNT-06] (F9), record "
        "and layer and sub-record extents by [R-CNT-13] (F31, L16), "
        "tile-index entries by [R-IDX-03] (T8)."),

    "L1:extent_offset (layer record slot)": (
        "harness. Confirmed still true with the seeds this module adds: "
        "checksum_report follows a layer record's extent slot without gating "
        "§4.2's domain first — the thing [R-ENC-05] forbids a reader to do — "
        "so it computes the segment-CRC array's position from an offset of "
        "2^63 and raises struct.error before any vector can be emitted. The "
        "file is well defined; the fix is a domain gate in checksum_report "
        "ahead of its index walk, in a file this module must not touch."),
    "L1:extent_length (layer record slot)": (
        "harness, same failure by the other half: the declared region size "
        "drives an entry count, and the walk reads past the end of the blob."),
    "L2:extent_offset + extent_length": (
        "harness. Either half large enough to overflow the sum triggers one "
        "of the two failures above."),
    "L2:V = P·C": (
        "not a distinguishable file — and the reason l_rows_a.py gave is not "
        "the reason. §14.1 defines V = P·C for the *interleaved* sequence "
        "only; a planar tile's sequence has V = P, so the planar route to "
        "this instance does not exist at all and a multi-tile seed does not "
        "open it. Within interleaved, Q = Σ Bᶜ over the channels and every "
        "Bᶜ ≥ 1, so Q ≥ C and P·Q ≥ P·C: no file makes P·C exceed 2^63 − 1 "
        "without P·Q exceeding it too, and P·Q is a separate instance of the "
        "same row (TV-0207). Recorded as a finding, not a gap."),
    "L2:max disk ordinal (C−1)·N + (N−1)": (
        "not a distinguishable file, and a finding rather than a gap: the "
        "expression is identically C·N − 1, so it exceeds 2^63 − 1 exactly "
        "when C·N does. TV-0206 is that file. §21.1's own rule — where a "
        "condition is a single predicate over several fields, no two files "
        "could differ — applies here to two *expressions* of one quantity."),
}


#: Places where the specification, not the corpus, looks wrong. Each was
#: reached by trying to build the vector and failing for a reason that is
#: about the text.
SPEC_FINDINGS = {
    "F5": ("SUPERSEDED — the corpus now covers this row; the reason below "
     "was true before register_seed, Layer(sub_records=...) and the "
     "truncate/append verbs existed. " 
        "F5's committed_file_length instance has no isolable witness. "
        "[R-CNT-06] requires committed_file_length = F, so a declared length "
        "below 128 in a file of at least 128 bytes always carries F17, and a "
        "declared length below 128 that equals F puts the file itself below "
        "128 — which is the other instance. TV-0901 ships the first form. "
        "Either the row should name one instance, or §21.1's Instances "
        "convention should say what to do with a field whose value another "
        "row pins to a second field."),
    "L44": (
        "L44 has no manifestation a verifier can distinguish from L41 or "
        "L42. [R-SLB-04]'s condition is 'the invariants were not "
        "re-established', and those invariants are exactly [R-SLB-03]'s — "
        "so every L44 file is an L41 or L42 file. [R-LIF-08] then confines a "
        "verifier to the live state, and §9.3 keeps no record of what a "
        "commit changed, so the generation counter is the only in-file trace "
        "of the history the row ranges over. TV-0913 and TV-0914 carry "
        "generation 2 for that reason and declare the co-violation. The row "
        "is a genuine writer obligation; what it is not is an independently "
        "detectable file condition, and the register's Detector column says "
        "'verifier' as though it were."),
    "L2": ("SUPERSEDED — the corpus now covers this row; the reason below "
     "was true before register_seed, Layer(sub_records=...) and the "
     "truncate/append verbs existed. " 
        "Two of L2's ten instances name a quantity no file can make overflow "
        "alone: max disk ordinal (C−1)·N + (N−1) is identically C·N − 1, and "
        "V = P·C is bounded above by P·Q since Q = Σ Bᶜ ≥ C. §21.1 already "
        "says that where a condition is a single predicate over several "
        "fields the fields are not instances; the same ought to be said of "
        "several *expressions* of one quantity, and the row's instance count "
        "should be 8 rather than 10."),
    "F25": ("SUPERSEDED — the corpus now covers this row; the reason below "
     "was true before register_seed, Layer(sub_records=...) and the "
     "truncate/append verbs existed. " 
        "F25 is reachable only in company. On the one registered non-layer "
        "type, MU = 1/PE = 0 differs from §7.3's registry in both bits and so "
        "is also F28 twice; on any unassigned type MU = 1 is F35 at open. "
        "TV-0904 takes the first, where every co-violating row shares F25's "
        "detector, detection point and scope. Worth stating in §21.2 rather "
        "than leaving each corpus author to rediscover."),
}
