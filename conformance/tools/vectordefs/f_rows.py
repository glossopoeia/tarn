# SPDX-License-Identifier: Apache-2.0
"""§21.2 — file-scope violations, outcome reject-file.

40 rows over 64 named instances. One vector per instance, except where the
instance cannot be built as a *distinguishable* file; those are listed in
SKIPPED with the reason, per ADR-0046's rule that an honest gap beats a
vector that lies.

Two recurring facts about this section shape the recipes below.

**The trailer is one covering CRC.** Every trailer-field mutation repairs
`trailer.crc`, or the reader stops at [R-CNT-06]'s CRC step and the vector
evidences F14 instead of the row it names. Several trailer mutations then
fail §6.2's field gates on purpose — those declare `trailer.gates`.

**Record-header fields are not separately addressable.** The builder's
layout map names a top-level record's 24-byte header as one field, so a
recipe rewrites the whole header with `_hdr()` and changes one value in it.
The header sits inside the directory, so the repair chain is
`directory.crc` then `trailer.crc`.
"""
import struct
import sys

from tarn_build import FRONT, TRAILER_MAGIC, crc32c
from tarn_vectors import SEEDS, Patch, Vector

u16 = lambda v: struct.pack("<H", v)
u32 = lambda v: struct.pack("<I", v)
u64 = lambda v: struct.pack("<Q", v)

# `verify()` needs the layer-name list for each seed it checks. tarn_vectors
# ships LAYERS for `minimal` and `pair` only; `meta` is the only seed carrying
# a non-layer top-level record, which sixteen of this section's instances are
# about. Registering the mapping here is additive and idempotent — the seed
# has exactly one layer, named `ok`. The proper home is LAYERS itself.
#
# The registration has to be written twice over. `load_vectors()` execs this
# module, and the `from tarn_vectors import ...` above resolves to a *second*
# module object whenever the tool is run as a script, because the running
# instance is then named `__main__` and `tarn_vectors` is not yet in
# sys.modules. Mutating the imported copy's LAYERS therefore leaves the
# dictionary `verify()` actually reads untouched. Fixing this in tarn_vectors
# — a LAYERS.get(seed) default, or exposing a register_seed() — would let
# every vectordef module drop this block.
for _mod in ("tarn_vectors", "__main__"):
    _tbl = getattr(sys.modules.get(_mod), "LAYERS", None)
    if isinstance(_tbl, dict) and "minimal" in _tbl:
        _tbl.setdefault("meta", ["ok"])

_PAIR_BLOB, _PAIR = SEEDS["pair"]()
_META_BLOB, _META = SEEDS["meta"]()


def _hdr(ty, flags, il, eo, el):
    """§7.2's 24-byte top-level record header, at the widths §7.2 fixes."""
    return struct.pack("<HHIQQ", ty, flags, il, eo, el)


def _doc(text: str, width: int) -> bytes:
    """A user-metadata extent: a JSON document padded with insignificant
    whitespace to `width` - 4 bytes, then §8.1's terminal CRC-32C."""
    b = text.encode("utf-8").ljust(width - 4)
    assert len(b) == width - 4, text
    return b + u32(crc32c(b))


# The seed's own extent bytes, so a recipe that changes only the header can
# leave the document alone: (extent_offset, extent_length) = (64, 27).
_M_EO, _M_EL = _META["record[0x0002].extent"]

# §10.2: record types >= 0x8000 are the experimental range. Vectors that need
# a top-level record with no content rules of its own use one: a *registered*
# type would drag §18's document rules in as a second defect, and a
# *reserved*-range type is itself a [R-CNT-15] violation a verifier must
# report. [R-CNF-02] settles that the bytes stay conforming: §10.3's
# prohibition binds a writer's conduct, not the file.
_EXPERIMENTAL = 0x8001


# --------------------------------------------------------------------------
# F4 — two layer records with byte-identical name fields.
#
# The name field is a length prefix plus its bytes, so `ok` occupies 3 bytes
# and `bad` occupies 4: no fixed-width patch can make them equal on its own.
# Rebuilding layer `bad`'s whole record trades the byte back — rename the
# layer to `ok` (-1) and its first dimension `y` to `yy` (+1) — so the record
# length, the inline_length, the geometry, the extent slot and every checksum
# below the directory are untouched, and the only changed fact is the one the
# row names.
# --------------------------------------------------------------------------
def _dup_layer_name_record() -> bytes:
    o, w = _PAIR["layer[bad].record"]
    rec = bytearray(_PAIR_BLOB[o:o + w])
    n_off, n_w = _PAIR["layer[bad].name"]
    cc_off, cc_w = _PAIR["layer[bad].channel_count"]
    e_off, _ = _PAIR["layer[bad].dim[0].extent"]
    d_off, d_w = cc_off + cc_w, e_off - (cc_off + cc_w)
    rec[d_off - o:d_off - o + d_w] = b"\x02yy"      # later splice first
    rec[n_off - o:n_off - o + n_w] = b"\x02ok"
    assert len(rec) == w, len(rec)
    return bytes(rec)


# --------------------------------------------------------------------------
# F23 — a top-level user-metadata record whose inline_length is not 1.
#
# That record is last in the sequence, so changing its inline_length alone
# leaves a residue or an overrun at the sequence end — [R-CNT-12]'s framing
# rule, register row F29, detected at the same open step. To carry only
# F23 the directory is rebuilt so the byte comes from somewhere else: the
# layer is renamed `ok` -> `o`, which is a conforming name, and the freed
# byte goes to the metadata record's inline payload.
# --------------------------------------------------------------------------
def _meta_dir_inline_len_2() -> bytes:
    d0, dl = _META["directory"]
    d = bytearray(_META_BLOB[d0:d0 + dl])
    hdr_off, _ = _META["record[0x0002].header"]
    inl_off, inl_w = _META["record[0x0002].inline"]
    nm_off, nm_w = _META["layer[ok].name"]
    lay_off, _ = _META["layer[ok].record"]
    d[inl_off - d0:inl_off - d0 + inl_w] = b"\x01\x00"          # encoding + 1
    d[hdr_off - d0 + 4:hdr_off - d0 + 8] = u32(2)               # inline_length
    d[nm_off - d0:nm_off - d0 + nm_w] = b"\x01o"                # -1 byte
    old = struct.unpack("<I", d[lay_off - d0 + 4:lay_off - d0 + 8])[0]
    d[lay_off - d0 + 4:lay_off - d0 + 8] = u32(old - 1)
    assert len(d) == dl, len(d)
    return bytes(d)


# --------------------------------------------------------------------------
# F34 — two user-metadata records in one top-level sequence.
#
# The seed carries one. A second needs an extent of its own that no other
# structure claims and whose bytes are a readable document, or the file
# carries an R2/R7 defect as well. The directory is rebuilt as exactly two
# metadata records; dir_length shrinks to match and the stale tail is zeroed,
# so the bytes past the new directory are slack ([R-CNT-21]) and not a
# structure in the pre-trailer gap ([R-CNT-05], row F7). The seed's layer
# record goes with it — a file with zero layers is conforming ([R-CNT-14]) —
# which frees its tile-index region to hold the second document.
# --------------------------------------------------------------------------
_F38_DOC_OFF, _F38_DOC_LEN = _META["layer[ok].index_region"]
_F38_SEQ = (_hdr(0x0002, 0b10, 1, _M_EO, _M_EL) + b"\x01"
            + _hdr(0x0002, 0b10, 1, _F38_DOC_OFF, _F38_DOC_LEN) + b"\x01")
_F38_DIRLEN = len(_F38_SEQ) + 4


def _f38_directory() -> bytes:
    _, dl = _META["directory"]
    return (_F38_SEQ + u32(crc32c(_F38_SEQ))).ljust(dl, b"\x00")


# --------------------------------------------------------------------------
# F7 / F33 — relocating a structure. The tile payload moved onto is written
# nowhere, so the entry's crc field is recomputed over the bytes already
# there; the entry is otherwise well-formed and both index checksums repair.
# --------------------------------------------------------------------------
def _entry(offset: int, length: int, blob: bytes) -> bytes:
    return u64(offset) + u64(length) + u32(crc32c(blob[offset:offset + length]))


_T = len(_PAIR_BLOB) - 64                       # pair: F - 64 = 384


VECTORS = [
    # Seed `meta` rather than `minimal`: reversing 128 sets bit 63 and the
    # file would carry F2 as well, while reversing this seed's 320 lands on
    # 0x4001000000000000 — in [R-ENC-03]'s domain and still a multiple of 64,
    # generation's only gates are >= 1 (§6.2) and <= 2^63 - 1 ([R-ENC-03]),
    # so a byte-reversed generation is detectable only when the true value's
    # low byte sets bit 63 on reversal. 128 is the smallest such value.

    # ------------------------------------------------------------------
    # F1 [R-ENC-02] — a signature constant stored byte-reversed.
    # ------------------------------------------------------------------
    Vector("TV-0105", "minimal",
           "F1 front signature block bytes [0,8) byte-reversed", False,
           patches=[Patch("front", FRONT[:8][::-1] + bytes(8))],
           row="F1", rule="R-ENC-02", outcome="reject-file",
           scope={"kind": "file"}, detected="open", must_not_serve=["file"]),
    Vector("TV-0106", "minimal", "F1 trailer magic at F-64 byte-reversed", False,
           patches=[Patch("trailer.magic", TRAILER_MAGIC[::-1])],
           repair=["trailer.crc"],
           row="F1", rule="R-ENC-02", outcome="reject-file",
           scope={"kind": "file"}, detected="open", must_not_serve=["file"]),

    # ------------------------------------------------------------------
    # F2 [R-ENC-03] — a u64 offset or length above 2^63 - 1. §4.2 orders the
    # field-domain check ahead of the sum check, so these are F2 and not F3
    # even where the sum also exceeds the domain. The committed_file_length
    # instance stays a multiple of 64, which is all that can be held constant:
    # no value above 2^63 - 1 can equal F, so F17's "= F" gate necessarily
    # fails too, and that is a property of the row rather than of the vector.
    # ------------------------------------------------------------------
    Vector("TV-0107", "minimal", "F2 dir_offset has bit 63 set", False,
           patches=[Patch("trailer.dir_offset", u64(0x8000000000000010))],
           repair=["trailer.crc"],
           breaks_checksums=["trailer.gates"],
           row="F2", rule="R-ENC-03", outcome="reject-file",
           scope={"kind": "file"}, detected="open", must_not_serve=["file"]),
    Vector("TV-0108", "minimal", "F2 dir_length has bit 63 set", False,
           patches=[Patch("trailer.dir_length", u64(0x8000000000000004))],
           repair=["trailer.crc"],
           breaks_checksums=["trailer.gates"],
           row="F2", rule="R-ENC-03", outcome="reject-file",
           scope={"kind": "file"}, detected="open", must_not_serve=["file"]),
    Vector("TV-0109", "minimal",
           "F2 committed_file_length has bit 63 set", False,
           patches=[Patch("trailer.committed_file_length",
                          u64(0x8000000000000080))],
           repair=["trailer.crc"],
           breaks_checksums=["trailer.gates"],
           row="F2", rule="R-ENC-03", outcome="reject-file",
           scope={"kind": "file"}, detected="open", must_not_serve=["file"]),
    Vector("TV-0110", "meta",
           "F2 non-layer top-level record extent_offset has bit 63 set", False,
           patches=[Patch("record[0x0002].header",
                          _hdr(0x0002, 0b10, 1, 0x8000000000000040, _M_EL))],
           repair=["directory.crc", "trailer.crc"],
           row="F2", rule="R-ENC-03", outcome="reject-file",
           scope={"kind": "file"}, detected="open", must_not_serve=["file"]),
    Vector("TV-0111", "meta",
           "F2 non-layer top-level record extent_length has bit 63 set", False,
           patches=[Patch("record[0x0002].header",
                          _hdr(0x0002, 0b10, 1, _M_EO, 0x800000000000001B))],
           repair=["directory.crc", "trailer.crc"],
           row="F2", rule="R-ENC-03", outcome="reject-file",
           scope={"kind": "file"}, detected="open", must_not_serve=["file"]),

    # ------------------------------------------------------------------
    # F3 [R-ENC-04] — each field in domain, the sum out of it. One vector per
    # instance: §21.1 counts the sum as one predicate, so the two fields it
    # reads are not separate instances.
    # ------------------------------------------------------------------
    Vector("TV-0112", "minimal",
           "F3 dir_offset + dir_length exceeds 2^63 - 1, both fields in domain",
           False,
           patches=[Patch("trailer.dir_offset", u64(0x7FFFFFFFFFFFFFF0)),
                    Patch("trailer.dir_length", u64(0x20))],
           repair=["trailer.crc"],
           breaks_checksums=["trailer.gates"],
           row="F3", rule="R-ENC-04", outcome="reject-file",
           scope={"kind": "file"}, detected="open", must_not_serve=["file"]),
    Vector("TV-0113", "meta", "F3 non-layer top-level record extent_offset + "
           "extent_length exceeds 2^63 - 1, both fields in domain", False,
           patches=[Patch("record[0x0002].header",
                          _hdr(0x0002, 0b10, 1, 0x7FFFFFFFFFFFFFF0, 0x20))],
           repair=["directory.crc", "trailer.crc"],
           row="F3", rule="R-ENC-04", outcome="reject-file",
           scope={"kind": "file"}, detected="open", must_not_serve=["file"]),

    # ------------------------------------------------------------------
    # F4 [R-ENC-15] — duplicate layer names, compared as raw bytes.
    # ------------------------------------------------------------------
    Vector("TV-0116", "pair",
           "F4 both layer records carry the name field `ok`", False,
           patches=[Patch("layer[bad].record", _dup_layer_name_record(),
                          note="renamed ok; its dimension y renamed yy so the "
                               "record length and inline_length are unchanged")],
           repair=["directory.crc", "trailer.crc"],
           row="F4", rule="R-ENC-15", outcome="reject-file",
           scope={"kind": "file"}, detected="open", must_not_serve=["file"]),

    # ------------------------------------------------------------------
    # F6 [R-CNT-04] — the front signature block is not byte-identical to the
    # constant. Distinct from F1: these are corruptions, not reversals.
    # ------------------------------------------------------------------
    Vector("TV-0117", "minimal",
           "F6 front signature magic bytes [0,8): final byte 1A -> 1B", False,
           patches=[Patch("front", FRONT[:7] + b"\x1b" + bytes(8))],
           row="F6", rule="R-CNT-04", outcome="reject-file",
           scope={"kind": "file"}, detected="open", must_not_serve=["file"]),
    Vector("TV-0118", "minimal",
           "F6 front signature reserved bytes [8,16) are not zero", False,
           patches=[Patch("front", FRONT[:8] + bytes(7) + b"\x01")],
           row="F6", rule="R-CNT-04", outcome="reject-file",
           scope={"kind": "file"}, detected="open", must_not_serve=["file"]),

    # ------------------------------------------------------------------
    # F7 [R-CNT-05] — a structure between the live directory's end and the
    # live trailer. Layer `bad`'s stored tile is relocated into the
    # pre-trailer pad, ending exactly at F - 64 so no offset gate fires; its
    # entry crc is recomputed over the zero bytes now standing there, so the
    # index chain and the tile check both still verify and the only fact the
    # file carries is where the extent sits. Readers are unaffected — their
    # check is the dir-bounds rule, per §6.2 — so this is the verifier's.
    # ------------------------------------------------------------------
    Vector("TV-0119", "pair", "F7 layer `bad`'s stored tile extent lies in "
           "the pre-trailer pad", False,
           patches=[Patch("layer[bad].entry[0]", _entry(_T - 4, 4, _PAIR_BLOB))],
           repair=["index:bad", "directory.crc", "trailer.crc"],
           row="F7", rule="R-CNT-05", outcome="reject-file",
           scope={"kind": "file"},
           detector="verifier", detected="certification",
           must_not_serve=[], serves=["ok"]),

    # ------------------------------------------------------------------
    # F8-F19 [R-CNT-06]/[R-CNT-07]/[R-CNT-08] — §6.2's trailer gates.
    # ------------------------------------------------------------------
    Vector("TV-0120", "minimal", "F8 the 8 bytes at F-64 are all zero", False,
           patches=[Patch("trailer.magic")],
           repair=["trailer.crc"],
           row="F8", rule="R-CNT-06", outcome="reject-file",
           scope={"kind": "file"}, detected="open", must_not_serve=["file"]),
    Vector("TV-0121", "minimal", "F9 dir_offset = 8, inside the front block",
           False,
           patches=[Patch("trailer.dir_offset", u64(8))],
           repair=["trailer.crc"],
           breaks_checksums=["trailer.gates"],
           row="F9", rule="R-CNT-06", outcome="reject-file",
           scope={"kind": "file"}, detected="open", must_not_serve=["file"]),
    Vector("TV-0122", "pair", "F10 dir_offset + dir_length = F - 63, one byte "
           "into the live trailer", False,
           patches=[Patch("trailer.dir_length", u64(293))],
           repair=["trailer.crc"],
           breaks_checksums=["trailer.gates"],
           row="F10", rule="R-CNT-06", outcome="reject-file",
           scope={"kind": "file"}, detected="open", must_not_serve=["file"]),
    # F2's generation instance; F11 covers a
    # generation of 0; neither puts the field above §4.2's domain. ADR-0058
    # added the ceiling to `[R-CNT-06]`'s gate list, but no row registers the
    # ceiling separately, so this is F2's.
    Vector("TV-0930", "minimal", "F2 generation has bit 63 set", False,
           patches=[Patch("trailer.generation", u64(0x8000000000000001))],
           repair=["trailer.crc"],
           row="F2", rule="R-ENC-03", outcome="reject-file",
           scope={"kind": "file"}, detected="open", must_not_serve=["file"]),
    Vector("TV-0123", "minimal", "F11 generation = 0", False,
           patches=[Patch("trailer.generation")],
           repair=["trailer.crc"],
           row="F11", rule="R-CNT-06", outcome="reject-file",
           scope={"kind": "file"}, detected="open", must_not_serve=["file"]),
    Vector("TV-0124", "minimal", "F12 file_id = 0", False,
           patches=[Patch("trailer.file_id")],
           repair=["trailer.crc"],
           row="F12", rule="R-CNT-06", outcome="reject-file",
           scope={"kind": "file"}, detected="open", must_not_serve=["file"]),
    # trailer.crc is the one trailer field with no repair: breaking it is the
    # point, and §6.2 puts its check ahead of every field gate.
    Vector("TV-0125", "minimal",
           "F14 the u32 at trailer offset 60 is not the CRC of [0,60)", False,
           patches=[Patch("trailer.crc")],
           breaks_checksums=["trailer.crc"],
           row="F14", rule="R-CNT-06", outcome="reject-file",
           scope={"kind": "file"}, detected="open", must_not_serve=["file"]),
    Vector("TV-0126", "minimal",
           "F15 the 4 reserved bytes at trailer offset 56 are not zero", False,
           patches=[Patch("trailer.reserved", b"\x01\x00\x00\x00")],
           repair=["trailer.crc"],
           row="F15", rule="R-CNT-06", outcome="reject-file",
           scope={"kind": "file"}, detected="open", must_not_serve=["file"]),
    Vector("TV-0127", "minimal",
           "F16 dir_length = 3, below the terminal CRC's 4 bytes", False,
           patches=[Patch("trailer.dir_length", u64(3))],
           repair=["trailer.crc"],
           breaks_checksums=["trailer.gates"],
           row="F16", rule="R-CNT-06", outcome="reject-file",
           scope={"kind": "file"}, detected="open", must_not_serve=["file"]),
    # 192 keeps committed_file_length a multiple of 64 and above the 128-byte
    # floor, so F17 is the only condition the file carries (not F13, not F5).
    Vector("TV-0128", "minimal",
           "F17 committed_file_length = 192 in a 128-byte file", False,
           patches=[Patch("trailer.committed_file_length", u64(192))],
           repair=["trailer.crc"],
           breaks_checksums=["trailer.gates"],
           row="F17", rule="R-CNT-06", outcome="reject-file",
           scope={"kind": "file"}, detected="open", must_not_serve=["file"]),
    Vector("TV-0129", "minimal", "F18 version_major = 0", False,
           patches=[Patch("trailer.version_major")],
           repair=["trailer.crc"],
           row="F18", rule="R-CNT-07", outcome="reject-file",
           scope={"kind": "file"}, detected="open", must_not_serve=["file"]),
    Vector("TV-0131", "minimal",
           "F19 flags bit 0 set, an unimplemented incompat-lane bit", False,
           patches=[Patch("trailer.flags", u32(1))],
           repair=["trailer.crc"],
           row="F19", rule="R-CNT-08", outcome="reject-file",
           scope={"kind": "file"}, detected="open", must_not_serve=["file"]),

    # ------------------------------------------------------------------
    # F20 [R-CNT-11] — the directory region's terminal CRC. No repair: the
    # trailer CRC covers only trailer bytes [0,60), so nothing above it moves.
    # The seed is `pair` because `minimal`'s record sequence is empty and its
    # directory CRC is the CRC of zero bytes, 0x00000000 — zeroing that field
    # would change no byte.
    # ------------------------------------------------------------------
    Vector("TV-0132", "pair", "F20 the directory region's final 4 bytes are "
           "not the CRC of the record sequence", False,
           patches=[Patch("directory.crc", b"\xde\xad\xbe\xef")],
           breaks_checksums=["directory.crc"],
           row="F20", rule="R-CNT-11", outcome="reject-file",
           scope={"kind": "file"}, detected="open", must_not_serve=["file"]),

    # ------------------------------------------------------------------
    # F21-F23 [R-CNT-25]/[R-MTA-03] — the user-metadata record's own framing,
    # which precedes the document and so is not under §18.1's quarantine.
    # ------------------------------------------------------------------
    Vector("TV-0133", "meta", "F21 top-level user-metadata record carries "
           "extent slot (0, 0)", False,
           patches=[Patch("record[0x0002].header", _hdr(0x0002, 0b10, 1, 0, 0))],
           repair=["directory.crc", "trailer.crc"],
           row="F21", rule="R-CNT-25", outcome="reject-file",
           scope={"kind": "file"}, detected="open", must_not_serve=["file"]),
    Vector("TV-0134", "meta", "F22 top-level user-metadata record's "
           "extent_length is 4, below the terminal CRC's own size", False,
           patches=[Patch("record[0x0002].header",
                          _hdr(0x0002, 0b10, 1, _M_EO, 4))],
           repair=["directory.crc", "trailer.crc"],
           row="F22", rule="R-CNT-25", outcome="reject-file",
           scope={"kind": "file"}, detected="open", must_not_serve=["file"]),
    Vector("TV-0135", "meta", "F23 top-level user-metadata record's "
           "inline_length is 2", False,
           patches=[Patch("directory", _meta_dir_inline_len_2(),
                          note="the extra inline byte comes from renaming the "
                               "layer ok -> o, so the sequence still parses "
                               "with no residue and F29 stays out of the file")],
           repair=["directory.crc", "trailer.crc"],
           row="F23", rule="R-MTA-03", outcome="reject-file",
           scope={"kind": "file"}, detected="open", must_not_serve=["file"]),

    # ------------------------------------------------------------------
    # F24-F28 — top-level record type and flags.
    # ------------------------------------------------------------------
    Vector("TV-0136", "meta", "F24 top-level record type = 0x0000", False,
           patches=[Patch("record[0x0002].header",
                          _hdr(0x0000, 0b10, 1, _M_EO, _M_EL))],
           repair=["directory.crc", "trailer.crc"],
           row="F24", rule="R-CNT-12", outcome="reject-file",
           scope={"kind": "file"}, detected="open", must_not_serve=["file"]),
    # MU and PE keep the registry's values, so §7.3's row F28 stays out.
    Vector("TV-0137", "meta", "F26 non-layer top-level record has reserved "
           "flag bit 2 set", False,
           patches=[Patch("record[0x0002].header",
                          _hdr(0x0002, 0b110, 1, _M_EO, _M_EL))],
           repair=["directory.crc", "trailer.crc"],
           row="F26", rule="R-CNT-12", outcome="reject-file",
           scope={"kind": "file"},
           detector="verifier", detected="certification",
           must_not_serve=[], serves=["ok"]),
    Vector("TV-0138", "meta", "F27 top-level user-metadata document's members "
           "are not in ascending key order", False,
           patches=[Patch("record[0x0002].extent",
                          _doc('{"b":1,"a":2}', _M_EL),
                          note="padded with insignificant whitespace to the "
                               "seed's extent length, terminal CRC recomputed")],
           row="F27", rule="R-MTA-05", outcome="reject-file",
           scope={"kind": "file"},
           detector="verifier", detected="certification",
           must_not_serve=[], serves=["ok"]),
    Vector("TV-0139", "meta", "F28 registered type 0x0002 stores MU = 1 where "
           "§7.3 fixes MU = 0 (flags bit 0)", False,
           patches=[Patch("record[0x0002].header",
                          _hdr(0x0002, 0b11, 1, _M_EO, _M_EL))],
           repair=["directory.crc", "trailer.crc"],
           row="F28", rule="R-CNT-22", outcome="reject-file",
           scope={"kind": "file"},
           detector="verifier", detected="certification",
           must_not_serve=[], serves=["ok"]),
    Vector("TV-0140", "meta", "F28 registered type 0x0002 stores PE = 0 where "
           "§7.3 fixes PE = 1 (flags bit 1)", False,
           patches=[Patch("record[0x0002].header",
                          _hdr(0x0002, 0b00, 1, _M_EO, _M_EL))],
           repair=["directory.crc", "trailer.crc"],
           row="F28", rule="R-CNT-22", outcome="reject-file",
           scope={"kind": "file"},
           detector="verifier", detected="certification",
           must_not_serve=[], serves=["ok"]),

    # ------------------------------------------------------------------
    # F29 [R-CNT-12] — a record that does not fit its containing sequence.
    # Both instances inflate a layer record's inline_length, which is the only
    # framing field a fixed-width patch can reach. The inflated payload also
    # leaves the *layer* record unparsable, a layer-scope condition (§21.3
    # L23) — but §19.2 puts the directory's record walk at open, strictly
    # before any layer access, so the file is rejected on F29 first.
    # ------------------------------------------------------------------
    Vector("TV-0141", "pair", "F29 the next record's 24-byte header extends "
           "past the end of the record sequence", False,
           patches=[Patch("layer[ok].record",
                          _PAIR_BLOB[slice(_PAIR["layer[ok].record"][0],
                                           _PAIR["layer[ok].record"][0] + 4)]
                          + u32(204)
                          + _PAIR_BLOB[_PAIR["layer[ok].record"][0] + 8:
                                       sum(_PAIR["layer[ok].record"])],
                          note="inline_length 95 -> 204, so the following "
                               "header would start 8 bytes before the "
                               "sequence end")],
           repair=["directory.crc", "trailer.crc"],
           row="F29", rule="R-CNT-12", outcome="reject-file",
           scope={"kind": "file"}, detected="open", must_not_serve=["file"]),
    # F29's third instance: bytes remaining after the last complete record.
    # The meta seed's record sequence runs 91..235 and record[0x0002] is
    # last, so declaring inline_length 0 ends the walk at 234 and leaves the
    # one byte at 234 over — too few for a 24-byte header, so it is residue
    # and not a further record. The type moves to §10.2's experimental range
    # with MU = 0, whose payload is opaque, because inline_length 0 on a
    # user-metadata record would be F23 instead ([R-MTA-03]); §21.6 makes
    # that type a defined ignore, so the record contributes no second defect.
    Vector("TV-0931", "meta",
           "F29 one byte remains after the last complete record", False,
           patches=[Patch("record[0x0002].header",
                          _hdr(_EXPERIMENTAL, 0b10, 0, _M_EO, _M_EL))],
           repair=["directory.crc", "trailer.crc"],
           row="F29", rule="R-CNT-12", outcome="reject-file",
           scope={"kind": "file"}, detected="open", must_not_serve=["file"]),
    Vector("TV-0142", "pair", "F29 the last record's inline payload extends "
           "past the end of the record sequence", False,
           patches=[Patch("layer[bad].record",
                          _PAIR_BLOB[slice(_PAIR["layer[bad].record"][0],
                                           _PAIR["layer[bad].record"][0] + 4)]
                          + u32(120)
                          + _PAIR_BLOB[_PAIR["layer[bad].record"][0] + 8:
                                       sum(_PAIR["layer[bad].record"])],
                          note="inline_length 93 -> 120; the header still fits")],
           repair=["directory.crc", "trailer.crc"],
           row="F29", rule="R-CNT-12", outcome="reject-file",
           scope={"kind": "file"}, detected="open", must_not_serve=["file"]),

    # ------------------------------------------------------------------
    # F30-F32 [R-CNT-13] — the extent slot of a non-layer top-level record.
    # ------------------------------------------------------------------
    Vector("TV-0143", "meta", "F30 non-layer top-level record extent slot "
           "(0, 27): offset zero, length nonzero", False,
           patches=[Patch("record[0x0002].header",
                          _hdr(0x0002, 0b10, 1, 0, _M_EL))],
           repair=["directory.crc", "trailer.crc"],
           row="F30", rule="R-CNT-13", outcome="reject-file",
           scope={"kind": "file"}, detected="open", must_not_serve=["file"]),
    # An extent_length of 0 on a *user-metadata* record would also be F22
    # (< 5), so this instance uses an experimental-range record type, for
    # which §18 states no length floor.
    Vector("TV-0144", "meta", "F30 non-layer top-level record extent slot "
           "(64, 0): offset nonzero, length zero", False,
           patches=[Patch("record[0x0002].header",
                          _hdr(_EXPERIMENTAL, 0b10, 1, _M_EO, 0))],
           repair=["directory.crc", "trailer.crc"],
           row="F30", rule="R-CNT-13", outcome="reject-file",
           scope={"kind": "file"}, detected="open", must_not_serve=["file"]),
    # Any extent_offset in 1-15 necessarily overlaps the front signature
    # block, which is F33's condition at verifier scope. §19.2 reaches this
    # one first: the record walk runs at open, certification is outside the
    # reader tiers entirely, so the reader's verdict is F31's.
    Vector("TV-0145", "meta", "F31 non-layer top-level record extent_offset = "
           "8, inside the front signature block", False,
           patches=[Patch("record[0x0002].header",
                          _hdr(0x0002, 0b10, 1, 8, 8))],
           repair=["directory.crc", "trailer.crc"],
           row="F31", rule="R-CNT-13", outcome="reject-file",
           scope={"kind": "file"}, detected="open", must_not_serve=["file"]),
    # Placed after the directory so the extent crosses nothing but the
    # pre-trailer pad and the trailer's first 3 bytes.
    Vector("TV-0146", "meta", "F32 non-layer top-level record extent ends 3 "
           "bytes into the live trailer", False,
           patches=[Patch("record[0x0002].header",
                          _hdr(0x0002, 0b10, 1, 239, 20))],
           repair=["directory.crc", "trailer.crc"],
           row="F32", rule="R-CNT-13", outcome="reject-file",
           scope={"kind": "file"}, detected="open", must_not_serve=["file"]),

    # ------------------------------------------------------------------
    # F33 [R-CNT-13] — one byte claimed by two structures that do not belong
    # to the same layer. Five of the seven named instances are built; the
    # other two are in SKIPPED, both because every offset gate already
    # forbids the bytes they would need.
    #
    # Vectors that need a record extent pointed at another scope's structure
    # use an experimental-range type: under type 0x0002 the bytes landed on
    # would also have to satisfy §18's document rules, and failing them is
    # R2/R3/R7 — a second, ignore-record defect at extent use.
    # ------------------------------------------------------------------
    Vector("TV-0147", "pair", "F33 stored-tile extents: layer `bad`'s tile 0 "
           "extent lies inside layer `ok`'s stored tile", False,
           patches=[Patch("layer[bad].entry[0]", _entry(16, 4, _PAIR_BLOB))],
           repair=["index:bad", "directory.crc", "trailer.crc"],
           row="F33", rule="R-CNT-13", outcome="reject-file",
           scope={"kind": "file"},
           detector="verifier", detected="certification",
           must_not_serve=[], serves=["ok"]),
    Vector("TV-0148", "meta", "F33 tile-index regions: a top-level record's "
           "extent covers layer `ok`'s tile-index region", False,
           patches=[Patch("record[0x0002].header",
                          _hdr(_EXPERIMENTAL, 0b10, 1,
                               *_META["layer[ok].index_region"]))],
           repair=["directory.crc", "trailer.crc"],
           row="F33", rule="R-CNT-13", outcome="reject-file",
           scope={"kind": "file"},
           detector="verifier", detected="certification",
           must_not_serve=[], serves=["ok"]),
    Vector("TV-0149", "meta", "F33 record extents: a top-level record's extent "
           "covers layer `ok`'s stored tile", False,
           patches=[Patch("record[0x0002].header",
                          _hdr(_EXPERIMENTAL, 0b10, 1, 16, 24))],
           repair=["directory.crc", "trailer.crc"],
           row="F33", rule="R-CNT-13", outcome="reject-file",
           scope={"kind": "file"},
           detector="verifier", detected="certification",
           must_not_serve=[], serves=["ok"]),
    Vector("TV-0150", "meta", "F33 directory region: a top-level record's "
           "extent covers the first 20 bytes of the directory", False,
           patches=[Patch("record[0x0002].header",
                          _hdr(_EXPERIMENTAL, 0b10, 1,
                               _META["directory"][0], 20))],
           repair=["directory.crc", "trailer.crc"],
           row="F33", rule="R-CNT-13", outcome="reject-file",
           scope={"kind": "file"},
           detector="verifier", detected="certification",
           must_not_serve=[], serves=["ok"]),

    # ------------------------------------------------------------------
    # F34 [R-CNT-14] — two user-metadata records at file scope. Both records
    # are otherwise flawless: inline_length 1, encoding 1, a well-formed
    # sorted document under a correct terminal CRC, and disjoint extents. The
    # directory shrinks to hold exactly the two, so dir_length moves with it
    # and the stale tail is zeroed into slack.
    # ------------------------------------------------------------------
    Vector("TV-0151", "meta", "F34 the record sequence carries two "
           "user-metadata records (type 0x0002)", False,
           patches=[Patch("layer[ok].index_region", _doc('{"a":1}',
                                                         _F38_DOC_LEN),
                          note="the second record's document, written over "
                               "the now-unreferenced tile-index region"),
                    Patch("directory", _f38_directory(),
                          note="two 0x0002 records and their CRC; the tail is "
                               "zeroed and becomes slack"),
                    Patch("trailer.dir_length", u64(_F38_DIRLEN))],
           repair=["trailer.crc"],
           row="F34", rule="R-CNT-14", outcome="reject-file",
           scope={"kind": "file"}, detected="open", must_not_serve=["file"]),

    # ------------------------------------------------------------------
    # F35 [R-CNT-15] — an unassigned type with MU = 1. PE stays 1, so
    # [R-CNT-12]'s MU=1/PE=0 combination (row F25) is not also present, and
    # the type is from the experimental range rather than the reserved one so
    # that [R-CNT-15]'s reserved-range verifier error is not either.
    # ------------------------------------------------------------------
    # §21.6's second exception, not F35. F35 is scoped to the *reserved*
    # range (0x0003-0x7FFF); 0x8001 is experimental (§10.2), and for an
    # experimental type with MU = 1 `[R-CNT-15]` obliges the reader to
    # reject while `[R-CNF-02]` leaves the bytes conforming — §10.3's
    # prohibition binds a writer's conduct, not the file. So this vector
    # names no register row and asserts the refusal of a valid file.
    # TV-0813 is its layer-scope twin. TV-0910 covers F35 proper.
    Vector("TV-0152", "meta", "a conforming file a reader must refuse: "
           "top-level record of experimental type 0x8001 with "
           "MUST_UNDERSTAND = 1", True,
           patches=[Patch("record[0x0002].header",
                          _hdr(_EXPERIMENTAL, 0b11, 1, _M_EO, _M_EL))],
           repair=["directory.crc", "trailer.crc"],
           must_not_serve=["file"]),
]


#: Instances of §21.2 this module does not build, and why. Keys are
#: `row` or `row:instance`. Three kinds of gap appear here, and they are not
#: equivalent: a *tooling* gap is a limit of the recipe format, an
#: *unreachable* gap is a condition §19.2 places behind an earlier check, and
#: a *vacuous* gap is a row whose condition no file can satisfy.
SKIPPED = {
    "F5": ("SUPERSEDED — the corpus now covers this row; the reason below "
     "was true before register_seed, Layer(sub_records=...) and the "
     "truncate/append verbs existed. " 
        "tooling, and unreachable for one instance. Both instances need a "
        "file below 128 bytes: recipes patch fixed-width fields and cannot "
        "change a file's length, and the builder's floor is 128. The "
        "committed_file_length instance is additionally unreachable in any "
        "file: [R-CNT-01] makes every conforming F a multiple of 64 and F17 "
        "requires committed_file_length = F, so a committed_file_length "
        "below 128 always co-violates F17 unless F is itself below 128, "
        "which is the other instance."),
    # (The row this entry was written against — "a byte of the live committed
    # state claimed by no coverage class" — was found vacuous and DELETED from
    # §21.2 by ADR-0056. §5.2 defines the live committed state as exactly what
    # the coverage classes cover, so no byte could ever exhibit it. Nothing to
    # skip: the row no longer exists.)
    "F13": ("SUPERSEDED — the corpus now covers this row; the reason below "
     "was true before register_seed, Layer(sub_records=...) and the "
     "truncate/append verbs existed. " 
        "unreachable with this builder, and co-violating in general. A "
        "committed_file_length that is not a multiple of 64 must still equal "
        "the physical file size (F17), so the file itself must end at a "
        "non-64-aligned offset. The builder pads every file to a multiple of "
        "64 and recipes cannot change a file's length; setting the field "
        "alone would carry F17 as well, at the same validation step."),
    "F25": ("SUPERSEDED — the corpus now covers this row; the reason below "
     "was true before register_seed, Layer(sub_records=...) and the "
     "truncate/append verbs existed. " 
        "unreachable. MU = 1 with PE = 0 on a *non-layer top-level* record "
        "requires a non-layer type, and format major 1 offers only two "
        "kinds. On the one registered non-layer type, 0x0002, §7.3 fixes "
        "MU = 0 and PE = 1, so the combination differs from the registry in "
        "both bits and the file also carries F28 — twice. On any unassigned "
        "type, MU = 1 is F35, which a reader rejects at open, ahead of "
        "certification. No file carries F25 alone."),
    "F33:trailer": (
        "unreachable. A structure overlapping the live trailer must extend "
        "past F - 64, which every offset gate already forbids at open: "
        "[R-CNT-06] for the directory (F10), [R-CNT-13] for a record or "
        "layer extent (F32, L17), [R-IDX-03] for a tile-index entry (T9). "
        "Every such file is rejected before certification, on the row that "
        "owns the gate."),
    "F33:front signature block": (
        "unreachable, for the mirror reason. Overlapping the front block "
        "needs a byte below offset 16, and every claimant's offset is gated "
        "at >= 16 before certification: dir_offset by [R-CNT-06] (F9), "
        "record and layer extents by [R-CNT-13] (F31, L16), tile-index "
        "entries by [R-IDX-03] (T8)."),
    "F33:sub-record extents": (
        "tooling. The builder emits no layer sub-records, and introducing "
        "one costs 24 bytes of layer-record inline payload that a "
        "fixed-width recipe has nowhere to take from — every field in the "
        "payload that could shrink is a name, and names shrink by at most a "
        "byte or two. A seed carrying a layer sub-record would close this."),
    "F35:flags bit 0": (
        "not a distinguishable file. F35's condition is the conjunction "
        "'unassigned type AND MU = 1', and §21.1 states that where a "
        "condition is a single predicate over several fields the fields it "
        "reads are not instances, because no two files could differ. The "
        "row's Instances cell reads 'type; flags bit 0' — two fields of one "
        "predicate — so it should count one, not two. TV-0152 is that one "
        "file."),
    "F40": (
        "tooling. The row's distinguishing fact is a physical file longer "
        "than committed_file_length, with the stale tail read in place of "
        "the trailer. Recipes cannot lengthen a file, and without the extra "
        "bytes the condition collapses into whichever trailer row the tail's "
        "content trips (F8, F14). A recipe verb that appends bytes after "
        "the trailer, or a seed carrying post-commit residue, would close "
        "this and F5 together."),
}
