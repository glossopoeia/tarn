# SPDX-License-Identifier: Apache-2.0
"""§21.3's sub-record rows — the trailing record sequence of a layer record.

§7.4 ends the layer record's inline payload with "zero or more records (§7.2
framing) ... layer scope by containment". Every row here is a condition on that
sequence, or the sub-record half of a row whose Instances cell names a
layer-record slot and a sub-record slot separately. All of them share one
shape: the file has two layers, `ok` and `sub`; the defect is on `sub`; `ok` is
intact and is what a reader must still serve ([R-VEC-04]).

Four facts govern every recipe below.

**A sub-record's type decides which other rules apply to it.** Only two types
are registered (§7.3): 0x0001 (layer) and 0x0002 (user metadata). A recipe
that needs a sub-record with *no* content rules of its own uses an
experimental-range type (>= 0x8000, §10.2) with MU = 0 — §21.6 makes such a
record a defined ignore, so the file carries no defect but the one the vector
names. A reserved-range type would itself be L25, and 0x0002 would drag §18's
document rules in. This is why L15, L16, L17 and L18 sit on an inert
sub-record while L10, L11 and L12 sit on a user-metadata one: those three rows
*are* §18's rules.

**Registry-fixed flags are not free.** §7.3 fixes MU/PE per registered type,
and L49 makes a stored bit differing from the registry a violation. So the
user-metadata sub-records here carry flags 0b10 (MU = 0, PE = 1) and the
nested layer record carries 0b11, and only reserved bit 2 — which the registry
does not fix — is available to a flags recipe (L47).

**Some shapes cannot be reached by patching.** A recipe overwrites a field at
its stored width; it cannot add a sub-record, lengthen one, or leave a partial
header at the payload's end. Where a row needs such a shape the seed carries
it, built from `Layer`/`Record` through `build_with_layout` and registered with
`register_seed()`. One of those seeds then splices bytes into the layer
record's inline payload, because no declaration produces a payload that ends
mid-record: see `_with_residue`.

**Slack is not a defect.** Several recipes zero or re-point a sub-record's
extent slot, abandoning the bytes the seed wrote for it. §21.6 classes
unclaimed bytes as slack — unconstrained content, no conformance requirement,
counted by a verifier — so the abandoned extent leaves the vector carrying one
defect still.
"""
import struct

from tarn_build import (Channel, Layer, Record, TRAILER_MAGIC,  # noqa: F401
                        build_with_layout, crc32c)
from tarn_vectors import Patch, Vector, register_seed

u16 = lambda v: struct.pack("<H", v)
u32 = lambda v: struct.pack("<I", v)
u64 = lambda v: struct.pack("<Q", v)

#: §10.2 — the experimental range. With MU = 0 such a record is §21.6's
#: "unknown record type carries MU = 0": ignored, and the file conforming.
INERT = 0x8001
#: §10.2 — the reserved range 0x0003-0x7FFF, which this text has not assigned.
RESERVED = 0x0003

_MU, _PE = 0b01, 0b10


def _ok() -> Layer:
    """The intact sibling [R-VEC-04] requires, identical in every seed here."""
    return Layer("ok", extents=(2, 3), tile_extents=(2, 3),
                 channels=[Channel("t", 12)],
                 tiles=[struct.pack("<6I", 0x3F800000, 0x80000000, 0x7FC00001,
                                    0xC0000000, 0x00000000, 0x7F800000)])


def _sub(subs: list) -> Layer:
    """The damage target: a one-tile layer whose record carries `subs`."""
    return Layer("sub", extents=(2, 2), tile_extents=(2, 2),
                 channels=[Channel("v", 6)], tiles=[bytes([7, 7, 7, 7])],
                 sub_records=subs)


def _umeta(doc: bytes) -> bytes:
    """A user-metadata extent: the document, then §8.1's terminal CRC-32C."""
    return doc + u32(crc32c(doc))


#: Members in ascending order of their keys' UTF-8 bytes, as [R-MTA-05] wants.
DOC_SORTED = b'{"a.one":1,"b.two":2}'
#: The same members, same length, out of order — L48's whole condition.
DOC_UNSORTED = b'{"b.two":2,"a.one":1}'
assert len(DOC_SORTED) == len(DOC_UNSORTED)

#: An inert sub-record's extent. It carries no structure: §8.1's coverage map
#: gives a checksum to user-metadata extents only, and [R-CNT-13] forbids an
#: MU = 0 record's extent from encoding offsets, so these bytes mean nothing.
INERT_EXTENT = bytes(range(0x40, 0x60))          # 32 bytes


# --------------------------------------------------------------------------
# Seeds. Each is one file shape a recipe cannot reach from another.
# --------------------------------------------------------------------------

def _seed_umeta():
    return build_with_layout([_ok(), _sub(
        [Record(0x0002, inline=b"\x01", extent=_umeta(DOC_SORTED), flags=_PE)])])


def _seed_umeta_wide():
    """L12: the encoding payload is two bytes, so inline_length is not 1.

    Not reachable by patch: shrinking or growing the stored inline_length
    without moving bytes leaves the sub-record sequence with residue or an
    overrun, which is L14.
    """
    return build_with_layout([_ok(), _sub(
        [Record(0x0002, inline=b"\x01\x00", extent=_umeta(DOC_SORTED),
                flags=_PE)])])


def _seed_umeta_empty():
    """L12's other direction (ADR-0079): inline_length 0, the encoding byte
    absent. Like the wide case this is not reachable by patch — the stored
    length has to match the bytes actually present or the sequence carries
    residue, which is L14."""
    return build_with_layout([_ok(), _sub(
        [Record(0x0002, inline=b"", extent=_umeta(DOC_SORTED),
                flags=_PE)])])


def _seed_umeta_two():
    """L19: two user-metadata sub-records, each valid on its own."""
    return build_with_layout([_ok(), _sub([
        Record(0x0002, inline=b"\x01", extent=_umeta(DOC_SORTED), flags=_PE),
        Record(0x0002, inline=b"\x01", extent=_umeta(DOC_SORTED), flags=_PE),
    ])])


def _seed_inert():
    return build_with_layout([_ok(), _sub(
        [Record(INERT, inline=bytes(8), extent=INERT_EXTENT, flags=_PE)])])


def _seed_nested_layer():
    """L26: a record of type 0x0001 in the sub-record sequence.

    It is emptied of everything a reader might trip over first — inline_length
    0, extent slot (0, 0), the registry's own MU = 1 / PE = 1 — so the type's
    placement is all that is wrong with it.
    """
    return build_with_layout([_ok(), _sub(
        [Record(0x0001, inline=b"", extent=None, flags=_MU | _PE)])])


def _with_residue(subs: list, residue: bytes):
    """Build the two-layer file, then extend layer `sub`'s inline payload by
    `residue` bytes without adding a record to it.

    No declaration produces this: `build` emits complete sub-records, so a
    payload that ends part-way through §7.2's 24-byte header has to be spliced.
    The splice widens the layer record's inline_length and the directory's
    dir_length by the same amount, which keeps the *top-level* sequence parsing
    exactly as before — the residue is inside the layer record, where the row
    puts it, and not after it, which would be F29 at file scope and would mask
    the row. Layer `sub` is emitted last, so nothing after the insertion point
    but the directory CRC, the pre-trailer pad and the trailer moves; all three
    are rebuilt here.
    """
    blob, layout = build_with_layout([_ok(), _sub(subs)])
    rec_off, rec_len = layout["layer[sub].record"]
    d0, dl = layout["directory"]
    ins, delta = rec_off + rec_len, len(residue)
    buf = bytearray(blob)
    buf[ins:ins] = residue
    struct.pack_into("<I", buf, rec_off + 4,
                     struct.unpack_from("<I", buf, rec_off + 4)[0] + delta)
    dl2 = dl + delta
    seq = bytes(buf[d0:d0 + dl2 - 4])
    body = bytes(buf[:d0]) + seq + u32(crc32c(seq))
    F = ((len(body) + 63) // 64 + 1) * 64
    out = bytearray(body + bytes(F - 64 - len(body)))
    tr = (TRAILER_MAGIC + struct.pack("<HHI", 1, 0, 0) + u64(1) + u64(d0)
          + u64(dl2) + u64(F) + u64(0x0123456789ABCDEF) + bytes(4))
    out += tr + u32(crc32c(tr))
    assert len(out) == F, (len(out), F)

    # The layout map, corrected. Only three things sit at or after the splice
    # point: the layer record's own span, the directory's CRC, and the
    # trailer — whose offsets are re-derived from the new F, not shifted,
    # because the pre-trailer pad absorbed part of the growth.
    old_t = len(blob) - 64
    lay = {}
    for k, (o, w) in layout.items():
        if k == "trailer" or k.startswith("trailer."):
            lay[k] = (F - 64 + (o - old_t), w)
        else:
            lay[k] = (o + delta, w) if o >= ins else (o, w)
    lay["layer[sub].record"] = (rec_off, rec_len + delta)
    lay["directory"] = (d0, dl2)
    lay["directory.crc"] = (d0 + dl2 - 4, 4)
    return bytes(out), lay


#: §7.2's header is 24 bytes; 10 of them cannot be parsed as one.
PARTIAL_HEADER = struct.pack("<HHIQQ", INERT, _PE, 0, 0, 0)[:10]


def _seed_residue():
    """L14, instance *trailing residue*: one complete sub-record, then 10
    bytes the sequence cannot parse.

    L14's other truncation instance — *sub-record header*, a payload ending
    part-way through a header with no complete sub-record before it — is
    already TV-0222 in `l_rows_a`, which frees the bytes for it by re-cutting
    layer `bad`'s geometry at constant record width. What that construction
    cannot reach is this file: residue *after* a sub-record the sequence has
    already parsed, which is what distinguishes the two instances at all.
    Whenever fewer than 24 bytes remain the residue is also a truncated
    header, so the distinction rests on that, and on nothing in the bytes
    themselves — see the findings note.
    """
    return _with_residue(
        [Record(INERT, inline=bytes(8), extent=INERT_EXTENT, flags=_PE)],
        PARTIAL_HEADER)


UMETA = register_seed("sub_umeta", _seed_umeta, ["ok", "sub"])
UMETA_WIDE = register_seed("sub_umeta_wide", _seed_umeta_wide, ["ok", "sub"])
UMETA_EMPTY = register_seed("sub_umeta_empty", _seed_umeta_empty, ["ok", "sub"])
UMETA_TWO = register_seed("sub_umeta_two", _seed_umeta_two, ["ok", "sub"])
INERT_SEED = register_seed("sub_inert", _seed_inert, ["ok", "sub"])
NESTED = register_seed("sub_nested_layer", _seed_nested_layer, ["ok", "sub"])
RESIDUE = register_seed("sub_residue", _seed_residue, ["ok", "sub"])

_UM_BLOB, _UM = _seed_umeta()
_IN_BLOB, _IN = _seed_inert()

#: Layer scope, so the repair chain is the layer record's two covering
#: checksums; nothing here touches an index entry.
DIR = ["directory.crc", "trailer.crc"]

_LAYER = {"kind": "layer", "name": "sub"}


def _reject(vid, seed, title, row, rule, patches=(), **kw):
    """A reader-detected layer-scope violation: `sub` unusable, `ok` intact."""
    return Vector(vid, seed, title, kw.pop("conforming", False),
                  patches=list(patches),
                  repair=kw.pop("repair", DIR if patches else []),
                  row=row, rule=rule, outcome="reject-layer", scope=_LAYER,
                  detected="layer access", must_not_serve=["layer:sub"],
                  serves=["ok"], **kw)


def _certify(vid, seed, title, row, rule, patches=(), **kw):
    """A verifier-detected violation: the file is nonconforming, yet every
    reader behavior is unchanged, so both layers are still served."""
    return Vector(vid, seed, title, False, patches=list(patches),
                  repair=kw.pop("repair", DIR if patches else []),
                  row=row, rule=rule,
                  outcome="reject-layer", scope=_LAYER, detector="verifier",
                  detected="certification", must_not_serve=[],
                  serves=["ok", "sub"], **kw)


VECTORS = [
    # ----------------------------------------------------------------------
    # The two conforming baselines. Every recipe below is a patch on one of
    # these two files or a seed that differs from them in one declaration; a
    # corpus that did not ship them would leave a reader unable to tell a
    # rejection caused by the row from one caused by the sub-record's mere
    # presence.
    # ----------------------------------------------------------------------
    Vector("TV-0800", UMETA,
           "layer `sub` carries a conforming user-metadata sub-record", True,
           serves=["ok", "sub"]),
    Vector("TV-0801", INERT_SEED,
           "layer `sub` carries a sub-record of an experimental type with "
           "MU = 0 — §21.6's defined ignore", True,
           serves=["ok", "sub"]),

    # ----------------------------------------------------------------------
    # L10-L12 — §18's rules, which reach a sub-record only when its type is
    # 0x0002. [R-CNT-25] and [R-MTA-03] place all three at the record's
    # containing scope, which §18.1 makes the layer for a sub-record.
    # ----------------------------------------------------------------------
    _reject("TV-0802", UMETA,
            "user-metadata sub-record with extent slot (0, 0)", "L10",
            "R-CNT-25",
            [Patch("layer[sub].sub[0].extent_offset", u64(0),
                   note="§7.1: a user-metadata document is never inline"),
             Patch("layer[sub].sub[0].extent_length", u64(0))]),
    _reject("TV-0803", UMETA,
            "user-metadata sub-record with extent_length 4, one byte short of "
            "a document plus its terminal CRC", "L11", "R-CNT-25",
            [Patch("layer[sub].sub[0].extent_length", u64(4),
                   note="§8.1 claims 4 of the extent's bytes for its CRC, so "
                        "5 is the floor")]),
    _reject("TV-0804", UMETA_WIDE,
            "user-metadata sub-record with inline_length 2 (instance: "
            "inline_length >= 2)", "L12", "R-MTA-03"),
    _reject("TV-0818", UMETA_EMPTY,
            "user-metadata sub-record with inline_length 0, the encoding "
            "byte absent (instance: inline_length 0, the encoding byte "
            "absent)", "L12", "R-MTA-03"),

    # ----------------------------------------------------------------------
    # L13-L14 — §7.2's framing, read before any type's own rules.
    # ----------------------------------------------------------------------
    _reject("TV-0805", UMETA, "sub-record of type 0x0000", "L13", "R-CNT-12",
            [Patch("layer[sub].sub[0].type", u16(0),
                   note="§7.2: type 0 is invalid, never an unknown type")]),
    _reject("TV-0806", RESIDUE,
            "L14 trailing residue: one complete sub-record, then 10 bytes the "
            "sequence cannot parse", "L14", "R-CNT-12"),
    _reject("TV-0807", INERT_SEED,
            "L14 sub-record inline_length: the header parses, its declared "
            "payload runs past the layer record's inline payload", "L14",
            "R-CNT-12",
            [Patch("layer[sub].sub[0].inline_length", u32(64),
                   note="24 + 64 exceeds what the payload has left")]),

    # ----------------------------------------------------------------------
    # L15-L18 — [R-CNT-13]'s extent-slot rules, on the inert sub-record so
    # that no document rule applies to the bytes the slot lands on.
    # ----------------------------------------------------------------------
    _reject("TV-0808", INERT_SEED,
            "sub-record extent slot with extent_length 0 and extent_offset "
            "nonzero", "L15", "R-CNT-13",
            [Patch("layer[sub].sub[0].extent_length", u64(0))]),
    # The mirror half. (0, 0) means no extent, so it is the pairing that is
    # invalid and each zeroed half is its own instance.
    # L2's sum instance ranges over both containers §21.1's arithmetic
    # counts: the layer record's own slot (TV-0927) and a sub-record's.
    # Both halves in domain, their sum 2^63.
    _reject("TV-0952", INERT_SEED,
            "sub-record extent slot (2^62, 2^62): both halves in domain, "
            "their sum 2^63", "L2", "R-ENC-04",
            [Patch("layer[sub].sub[0].extent_offset", u64(1 << 62)),
             Patch("layer[sub].sub[0].extent_length", u64(1 << 62))],
            instance="sub-record extent_offset + extent_length"),
    _reject("TV-0928", INERT_SEED,
            "sub-record extent slot with extent_offset 0 and extent_length "
            "nonzero", "L15", "R-CNT-13",
            [Patch("layer[sub].sub[0].extent_offset", u64(0))]),
    _reject("TV-0809", INERT_SEED,
            "sub-record extent at offset 8, inside the front signature block",
            "L16", "R-CNT-13",
            [Patch("layer[sub].sub[0].extent_offset", u64(8)),
             Patch("layer[sub].sub[0].extent_length", u64(8),
                   note="kept inside [0, 16) so the only structure the extent "
                        "overlaps is the front block, whose F33 instance "
                        "§21.2 already records as unreachable behind this "
                        "very gate")]),
    _reject("TV-0810", INERT_SEED,
            "sub-record extent begins at F - 64, on the live trailer", "L17",
            "R-CNT-13",
            [Patch("layer[sub].sub[0].extent_offset", u64(len(_IN_BLOB) - 64),
                   note="extent_offset + extent_length > F - 64")]),
    _certify("TV-0811", INERT_SEED,
             "sub-record extent covers layer `sub`'s own tile-index region",
             "L18", "R-CNT-13",
             [Patch("layer[sub].sub[0].extent_offset",
                    u64(_IN["layer[sub].index_region"][0])),
              Patch("layer[sub].sub[0].extent_length",
                    u64(_IN["layer[sub].index_region"][1]),
                    note="both structures belong to layer `sub`, so [R-CNT-13] "
                         "makes the overlap reject-layer, not reject-file")]),

    # ----------------------------------------------------------------------
    # L19 — multiplicity, per type, per containing record ([R-CNT-14]).
    # ----------------------------------------------------------------------
    _reject("TV-0812", UMETA_TWO,
            "two user-metadata sub-records on one layer record", "L19",
            "R-CNT-14"),

    # ----------------------------------------------------------------------
    # L24-L26 — what a type value means where §7.3 does not scope it.
    # ----------------------------------------------------------------------
    # An *experimental*-range type, not a reserved one: [R-CNF-02] keeps the
    # bytes conforming (§10.3's prohibition binds the writer, not the file).
    #
    # The claim that this vector "carries L24" was true of the L24 that
    # existed when it was written. ADR-0057 deleted three rows and §21
    # renumbered contiguously, so today's L24 is a different condition —
    # exactly the drift ADR-0049 forbids deriving vector identity from.
    #
    # §21.6's second exception, not L24. L24 is scoped to the *reserved*
    # range (0x0003-0x7FFF) and this seed's sub-record type is
    # experimental (>= 0x8000, see this module's header), so the file is
    # conforming and the refusal is the reader's capability, not a defect
    # in the bytes. The vector therefore names no register row.
    # TV-0152 is its file-scope twin. TV-0915 covers L24 proper.
    Vector("TV-0813", INERT_SEED,
           "a conforming layer a reader must refuse: sub-record of an "
           "experimental type with MU = 1", True,
           patches=[Patch("layer[sub].sub[0].flags", u16(_MU | _PE),
                          note="§10.2's experimental range, so the bytes stay "
                               "conforming while the reader must refuse")],
           repair=DIR,
           must_not_serve=["layer:sub"], serves=["ok"]),

    # L24 proper: the reserved range with MU = 1. Same shape as TV-0814
    # (reserved type, MU = 0, verifier-only) with the MU bit set, which is
    # what moves detection to the reader at layer access.
    Vector("TV-0915", INERT_SEED,
           "L24 sub-record carrying reserved-range type 0x0003 with "
           "MUST_UNDERSTAND = 1", False,
           patches=[Patch("layer[sub].sub[0].type", u16(RESERVED)),
                    Patch("layer[sub].sub[0].flags", u16(_MU | _PE))],
           repair=DIR, row="L24", rule="R-CNT-18", outcome="reject-layer",
           scope=_LAYER, detected="layer access",
           must_not_serve=["layer:sub"], serves=["ok"]),
    # L49's sub-record instance: type 0x0002 is registered at MU = 0, PE = 1
    # (§7.3), so a stored PE = 0 differs from the registry. `[R-CNT-22]`
    # makes that the file's defect while conforming readers still apply the
    # fixed semantics, which is why the detector is the verifier.
    # L49 needs a sub-record of a type §7.3 *registers*. The inert seed's
    # sub-record is type 0x8001 — experimental, which the registry does not
    # reach — so this vector is built on UMETA, whose sub-record is 0x0002
    # at the registry's MU = 0, PE = 1. flags = 0 leaves MU matching and
    # clears PE: the PE bit alone differs.
    _certify("TV-0929", UMETA,
             "sub-record of registered type 0x0002 stores PE = 0 where the "
             "registry fixes PE = 1", "L49", "R-CNT-22",
             [Patch("layer[sub].sub[0].flags", u16(0))],
             instance="sub-record flags bit 1"),
    # The mirror: MU set where the registry fixes MU = 0, PE left matching.
    _certify("TV-0955", UMETA,
             "sub-record of registered type 0x0002 stores MU = 1 where the "
             "registry fixes MU = 0", "L49", "R-CNT-22",
             [Patch("layer[sub].sub[0].flags", u16(0b11))],
             instance="sub-record flags bit 0"),
    # L46's sub-record instance. The inert sub-record's type is unassigned,
    # so §7.3 fixes no flags for it and the MU = 1 / PE = 0 combination is
    # L46 alone -- unlike a layer record, where the registry's MU = 1, PE = 1
    # makes the same combination co-violate L49.
    # L46's sub-record instance. MU = 1 on a type the reader does not
    # implement is reject-layer under [R-CNT-18] — TV-0813 is the conforming
    # twin of the same refusal — so `sub` is refused while `ok` is served.
    Vector("TV-0954", INERT_SEED,
           "sub-record of an unassigned type carries MU = 1 with PE = 0",
           False,
           patches=[Patch("layer[sub].sub[0].flags", u16(0b01))],
           repair=DIR, row="L46", rule="R-CNT-12",
           outcome="reject-layer", scope=_LAYER, detector="verifier",
           detected="certification",
           must_not_serve=["layer:sub"], serves=["ok"]),
    _certify("TV-0814", INERT_SEED,
             "sub-record carrying reserved-range type 0x0003", "L25",
             "R-CNT-15",
             [Patch("layer[sub].sub[0].type", u16(RESERVED),
                    note="MU stays 0, so a reader ignores the record (§21.6) "
                         "and only the emission is the violation")]),
    _reject("TV-0815", NESTED,
            "a record of type 0x0001 in the sub-record sequence", "L26",
            "R-CNT-18"),

    # ----------------------------------------------------------------------
    # L47-L48 — nonconforming files whose every reader behavior is unchanged.
    # ----------------------------------------------------------------------
    _certify("TV-0816", UMETA,
             "sub-record reserved flag bit 2 set", "L47", "R-CNT-12",
             [Patch("layer[sub].sub[0].flags", u16(_PE | 0b100),
                    note="bits 0 and 1 keep §7.3's registered values, so the "
                         "file does not also carry L49")]),
    _certify("TV-0817", UMETA,
             "sub-record user-metadata document with unsorted members", "L48",
             "R-MTA-05",
             [Patch("layer[sub].sub[0].extent", _umeta(DOC_UNSORTED),
                    note="same members, same bytes, descending key order")],
             repair=[]),   # §8.1 covers a user-metadata document with the
                           # extent's own final 4 bytes, which the patch
                           # rewrites; the extent lies outside the directory,
                           # so no other checksum moves.
]


SKIPPED = {
    "L24": (
        "unreachable. Detecting that a sub-record 'itself contains records' "
        "requires knowing that the record's payload holds records, and format "
        "major 1 defines exactly one type whose payload does — 0x0001, whose "
        "inline payload §7.4 ends with a sub-record sequence. Type 0x0002's "
        "payload is one byte ([R-MTA-03]), and for an unassigned type the "
        "payload is opaque: with MU = 0 §21.6 makes the record a defined "
        "ignore no reader looks inside, and with MU = 1 the reader rejects "
        "the layer at L24, before any payload is parsed. So every file "
        "exhibiting L24 is a file whose sub-record has type 0x0001 — which is "
        "L26, detected by the type alone and therefore strictly earlier in "
        "any reader's walk. TV-0816 is that file. L24 has no instance L26 "
        "does not already carry."),
    "L46:sub-record": (
        "unreachable, for the reason §21.2's F25 is unreachable at file "
        "scope. MU = 1 with PE = 0 on a sub-record needs a type: on 0x0002 "
        "§7.3 fixes MU = 0 and PE = 1, so both stored bits differ from the "
        "registry and the file also carries L49; on 0x0001 the type's mere "
        "placement is L26; on any unassigned type MU = 1 is L24, which a "
        "reader detects at layer access, ahead of the certification this row "
        "is detected at. No file carries L46's sub-record half alone. The "
        "layer-record half is unreachable too — §7.3 fixes PE = 1 for type "
        "0x0001, so clearing it is L49 — which is why the row has no vector "
        "in either container."),
}
