# SPDX-License-Identifier: Apache-2.0
"""§21.5 — ignored records. 11 rows, 40 instances, outcome ignore-record.

Every row here is a user-metadata record whose *document* cannot be read
(R1–R10), or an unknown record type a reader is told to skip (R11). The outcome
class is what makes these vectors different from every other section of the
register: the record is skipped **as though absent** and decoding of stored data
is unaffected (§2.4, `[R-CNT-25]`). So each vector's real claim is a pair —
the metadata a reader must not serve, and the layer it must still read — and
every vector here sets ``serves=["ok"]``. A file that also failed to read `ok`
would be evidence for some other row.

Each row names its instances as *alternatives × containers*: a condition can sit
in the top-level user-metadata record or in a layer's user-metadata sub-record
(§7.4, §18.1), and the register counts those separately because their detection
points differ — open versus layer access for R1 and R11, and for the rest the
extent-use tier that only exists once a reader reaches for the document
(§19.2). One instance, one file.

Two structural facts about the `meta` seed shape everything below.

*The sub-record half.* The seed's user-metadata record is top-level: it is the
second record of the directory's sequence, after the layer record. §7.4 places a
layer's sub-records at the **end of the layer record's inline payload**, and
§7.2 fixes a record's span as its 24-byte header plus inline_length. So the same
25 bytes become a sub-record by widening the layer record's inline_length to
swallow them — the directory sequence then holds one record, the layer, whose
inline parses as the fixed fields followed by exactly one complete sub-record
with no residue, which is what `[R-CNT-18]` demands. No byte moves; containment
is the only thing that changes. That is `_AS_SUBRECORD`.

*The 23-byte document.* A recipe may only overwrite a field, never grow one, so
every document here is exactly 23 bytes: the seed's extent is 27, of which
§8.1's terminal CRC-32C claims the last 4. Under encoding 1 the document is
stored verbatim and JSON's insignificant whitespace pads it out. Under encoding
2 all 23 bytes are the RFC 8878 frame, which is tight enough that the frames
are built here rather than written as literals — see `_frame`. Where a row is
unreachable inside that budget it is in SKIPPED, with the arithmetic.
"""
import struct
import sys

from tarn_vectors import SEEDS, Vector, Patch  # noqa: F401
from tarn_build import crc32c

u16 = lambda v: struct.pack("<H", v)
u32 = lambda v: struct.pack("<I", v)

# `verify()` looks up the seed's layer names to walk its index chains, and its
# table names only the two seeds the vertical slice used. Registering `meta`
# here rather than editing the shared module keeps concurrent authors out of
# each other's way; setdefault so that a sibling doing the same neither wins nor
# loses. Both module objects are updated because the driver runs as `__main__`
# and the `from tarn_vectors import ...` above binds a second, independent copy
# of the same file — `verify()` reads the one in `__main__`.
for _m in (sys.modules.get("__main__"), sys.modules.get("tarn_vectors")):
    if isinstance(getattr(_m, "LAYERS", None), dict):
        _m.LAYERS.setdefault("meta", ["ok"])

_BLOB, _LAYOUT = SEEDS["meta"]()


def _field(nm: str) -> bytes:
    """The seed's own bytes for a named field — recipes address fields by name
    even when what they need is *most of* the field back unchanged."""
    off, w = _LAYOUT[nm]
    return _BLOB[off:off + w]


# -- turning the top-level record into a layer sub-record -------------------
_LAYER_REC = _field("layer[ok].record")
_SUB_SPAN = len(_field("record[0x0002].header")) + len(_field("record[0x0002].inline"))
_INLINE_LEN = len(_LAYER_REC) - 24            # §7.2: header is 24 B, then inline

#: §7.2's header lays inline_length at header offset 4 as a u32. The layout map
#: names `flags`, `extent_offset` and `extent_length` inside a record header but
#: not `inline_length`, so this splices it — the one place in this module that
#: counts bytes rather than naming a field.
_AS_SUBRECORD = Patch(
    "layer[ok].record",
    _LAYER_REC[:4] + u32(_INLINE_LEN + _SUB_SPAN) + _LAYER_REC[8:],
    note="layer inline_length widened to contain the user-metadata record: the "
         "same 25 bytes, now a layer sub-record (§7.4)")

_META_HDR = _field("record[0x0002].header")


def _retype(ty: int) -> Patch:
    """Rewrite the user-metadata record's type, keeping its flags and slots."""
    return Patch("record[0x0002].header", u16(ty) + _META_HDR[2:],
                 note=f"record type {ty:#06x}")


# -- documents ---------------------------------------------------------------
DOC_LEN = 27 - 4          # the seed's extent, less §8.1's terminal CRC


def _ext(stored: bytes) -> Patch:
    """An extent carrying `stored` under a correct terminal CRC (§8.1).

    Padding is the caller's: JSON whitespace for encoding 1, frame bytes for
    encoding 2. A short document would mean patching extent_length too, and
    every byte it freed would become slack a verifier then reports (§21.6).
    """
    assert len(stored) == DOC_LEN, f"{len(stored)} B, need {DOC_LEN}"
    return Patch("record[0x0002].extent", stored + u32(crc32c(stored)))


def _json(doc: bytes) -> Patch:
    """A verbatim (encoding 1) document, padded to width with JSON whitespace —
    RFC 8259's `ws` around the top-level value, which changes no reading."""
    return _ext(doc + b" " * (DOC_LEN - len(doc)))


ENC = {1: Patch("record[0x0002].inline", b"\x01"),
       2: Patch("record[0x0002].inline", b"\x02")}


# -- RFC 8878 frames, for the encoding-2 rows --------------------------------
ZMAGIC = b"\x28\xb5\x2f\xfd"


def _blockhdr(size: int, btype: int, last: bool) -> bytes:
    """3-byte block header: bit 0 last, bits 1–2 type, bits 3–23 size."""
    return struct.pack("<I", (size << 3) | (btype << 1) | int(last))[:3]


def _frame(content: bytes, magic: bytes = ZMAGIC, dict_id: int | None = None,
           checksum: bool = False) -> bytes:
    """One single-segment frame holding `content` in a raw block.

    Frame_Header_Descriptor bit 5 is Single_Segment, so there is no window
    descriptor and the content-size field is one byte; bit 2 is the
    content-checksum flag and bits 0–1 the dictionary-ID flag — the two knobs
    §18.2 forbids and R4 exercises.
    """
    fhd = 0x20 | (0x04 if checksum else 0) | (0x01 if dict_id is not None else 0)
    out = magic + bytes([fhd])
    if dict_id is not None:
        out += bytes([dict_id])
    out += bytes([len(content)]) + _blockhdr(len(content), 0, True) + content
    if checksum:
        out += u32(_xxh64(content) & 0xFFFFFFFF)
    return out


def _skippable(payload: bytes = b"") -> bytes:
    return u32(0x184D2A50) + u32(len(payload)) + payload


_P = (0x9E3779B185EBCA87, 0xC2B2AE3D27D4EB4F, 0x165667B19E3779F9,
      0x85EBCA77C2B2AE63, 0x27D4EB2F165667C5)
_M64 = (1 << 64) - 1


def _xxh64(data: bytes) -> int:
    """XXH64, for the one frame that carries RFC 8878's content checksum.

    A frame whose checksum field held the wrong value would fail to decode, and
    the vector would then evidence R3 as well as R4 — the frame must be sound in
    every way except the flag the row names.
    """
    rotl = lambda x, r: ((x << r) | (x >> (64 - r))) & _M64
    rnd = lambda a, i: (rotl((a + i * _P[1]) & _M64, 31) * _P[0]) & _M64
    n, i = len(data), 0
    if n >= 32:
        v = [(_P[0] + _P[1]) & _M64, _P[1], 0, (-_P[0]) & _M64]
        while i + 32 <= n:
            for k in range(4):
                v[k] = rnd(v[k], struct.unpack_from("<Q", data, i)[0]); i += 8
        h = (rotl(v[0], 1) + rotl(v[1], 7) + rotl(v[2], 12) + rotl(v[3], 18)) & _M64
        for k in range(4):
            h = (((h ^ rnd(0, v[k])) * _P[0]) + _P[3]) & _M64
    else:
        h = _P[4]
    h = (h + n) & _M64
    while i + 8 <= n:
        h = (rotl(h ^ rnd(0, struct.unpack_from("<Q", data, i)[0]), 27) * _P[0]
             + _P[3]) & _M64
        i += 8
    if i + 4 <= n:
        h = (rotl(h ^ (struct.unpack_from("<I", data, i)[0] * _P[0]) & _M64, 23)
             * _P[1] + _P[2]) & _M64
        i += 4
    while i < n:
        h = (rotl(h ^ (data[i] * _P[4]) & _M64, 11) * _P[0]) & _M64
        i += 1
    h ^= h >> 33; h = (h * _P[1]) & _M64
    h ^= h >> 29; h = (h * _P[2]) & _M64
    return h ^ (h >> 32)


def _pad_json(width: int) -> bytes:
    """`{"a":1}` widened to `width` bytes with trailing JSON whitespace."""
    return b'{"a":1}' + b" " * (width - 7)


# The frames, each exactly DOC_LEN bytes so that the extent's terminal CRC lands
# where §8.1 puts it. Verified against a reference decoder: the four that are
# meant to decode do, and produce the document written beside them.
F_UNDECODABLE = (ZMAGIC + b"\x20" + bytes([14]) + _blockhdr(14, 2, True)
                 + b"\xff" * 14)                       # compressed block, garbage
F_NO_MAGIC = _frame(_pad_json(14), magic=b"\x00\x00\x00\x00")
F_SKIPPABLE = _skippable() + _frame(b"{}" + b" " * 4)
F_TWO_FRAMES = _frame(b"{}") + _frame(b"   ")
F_DICT_ID = _frame(_pad_json(13), dict_id=7)
F_CHECKSUM = _frame(_pad_json(10), checksum=True)

# R10's key must exceed 255 bytes, which no 23-byte verbatim document can hold;
# encoding 2 is the only way to reach the row. The key runs as a single RLE
# block, the braces and the value as raw blocks either side, and the whole frame
# comes to exactly DOC_LEN. Frame_Content_Size is two bytes here (descriptor
# bits 7–6 = 01, stored value = size − 256) because the document is 262 bytes.
_BIG_DOC = b'{"' + b"a" * 256 + b'":1}'
F_LONG_KEY = (ZMAGIC + b"\x60" + struct.pack("<H", len(_BIG_DOC) - 256)
              + _blockhdr(2, 0, False) + b'{"'
              + _blockhdr(256, 1, False) + b"a"
              + _blockhdr(4, 0, True) + b'":1}')

for _n, _f in (("undecodable", F_UNDECODABLE), ("no magic", F_NO_MAGIC),
               ("skippable", F_SKIPPABLE), ("two frames", F_TWO_FRAMES),
               ("dict id", F_DICT_ID), ("checksum", F_CHECKSUM),
               ("long key", F_LONG_KEY)):
    assert len(_f) == DOC_LEN, (_n, len(_f))


# -- expectations ------------------------------------------------------------
TOP = {"kind": "record", "container": "file", "record_type": "0x0002"}
SUB = {"kind": "record", "container": "layer", "layer": "ok",
       "record_type": "0x0002"}
NOT_TOP = ["metadata:file"]
NOT_SUB = ["metadata:layer:ok"]


def _v(vid, title, *, sub, row, rule, detected, patches, conforming=False,
       scope=None, must_not_serve=None):
    """One ignore-record vector.

    Every patch here lands in the directory or in the record's extent. The
    directory carries a CRC over its whole record sequence and the trailer a CRC
    over itself, so any directory-resident patch repairs both; the extent sits
    outside the directory and under no covering checksum but its own terminal
    one, which `_ext` recomputes.
    """
    ps = list(patches)
    if sub:
        ps = [_AS_SUBRECORD] + ps
    needs_dir = any(p.field != "record[0x0002].extent" for p in ps)
    return Vector(
        vid, "meta", title, conforming,
        patches=ps,
        repair=["directory.crc", "trailer.crc"] if needs_dir else [],
        row=row, rule=rule, outcome="ignore-record",
        scope=scope or (SUB if sub else TOP),
        detected=detected,
        must_not_serve=must_not_serve or (NOT_SUB if sub else NOT_TOP),
        # The record is skipped as though absent: the layer, its index and its
        # tile are untouched, so the whole file still reads (§2.4, §21.5).
        serves=["ok"])


VECTORS = [
    # -- R1: an unassigned document encoding ---------------------------------
    # §10.2 partitions the metadata-encoding space: 1 and 2 assigned, 3–0x7F
    # reserved, ≥ 0x80 experimental, 0 invalid everywhere. Detection is at open
    # for the top-level record and at layer access for the sub-record, because
    # the encoding byte is the record's inline payload — resident in the
    # directory, needing no extent fetch (§19.2).
    _v("TV-0500", "user-metadata encoding 0, top-level record",
       sub=False, row="R1", rule="R-CNT-25", detected="open",
       patches=[Patch("record[0x0002].inline", b"\x00",
                      note="§18.2: 0 is invalid in every identifier space")]),
    _v("TV-0501", "user-metadata encoding 0, layer sub-record",
       sub=True, row="R1", rule="R-CNT-25", detected="layer access",
       patches=[Patch("record[0x0002].inline", b"\x00")]),
    _v("TV-0502", "user-metadata encoding 3 (reserved), top-level record",
       sub=False, row="R1", rule="R-CNT-25", detected="open",
       patches=[Patch("record[0x0002].inline", b"\x03",
                      note="reserved range 3–0x7F, §10.2")]),
    _v("TV-0503", "user-metadata encoding 3 (reserved), layer sub-record",
       sub=True, row="R1", rule="R-CNT-25", detected="layer access",
       patches=[Patch("record[0x0002].inline", b"\x03")]),
    # The experimental instances are conforming *files*: §10.3's prohibition on
    # emitting an experimental value is conduct, and `[R-CNF-02]` says conduct
    # binds the actor while the predicate binds the bytes — the same reading
    # §7.3 states outright for an experimental record type. The reader outcome
    # is unchanged; only the `conforming` axis differs, which §24 makes
    # independent of the outcome axis. See the findings note on R1.
    _v("TV-0504", "user-metadata encoding 0x80 (experimental), top-level record",
       sub=False, row="R1", rule="R-CNT-25", detected="open", conforming=True,
       patches=[Patch("record[0x0002].inline", b"\x80",
                      note="experimental range ≥ 0x80, §10.2/§10.3")]),
    _v("TV-0505", "user-metadata encoding 0x80 (experimental), layer sub-record",
       sub=True, row="R1", rule="R-CNT-25", detected="layer access", conforming=True,
       patches=[Patch("record[0x0002].inline", b"\x80")]),

    # -- R2: the extent's terminal CRC does not cover its bytes ---------------
    # The document itself is sound; only §8.1's trailing 4 bytes are wrong, so a
    # reader that skips the CRC would read the record and betray the row.
    _v("TV-0506", "user-metadata extent CRC mismatch, top-level extent",
       sub=False, row="R2", rule="R-CNT-20", detected="extent use",
       patches=[ENC[1],
                Patch("record[0x0002].extent",
                      _pad_json(DOC_LEN) + u32(crc32c(_pad_json(DOC_LEN)) ^ 0xFFFFFFFF),
                      note="correct document, complemented CRC")]),
    _v("TV-0507", "user-metadata extent CRC mismatch, layer sub-record extent",
       sub=True, row="R2", rule="R-CNT-20", detected="extent use",
       patches=[ENC[1],
                Patch("record[0x0002].extent",
                      _pad_json(DOC_LEN) + u32(crc32c(_pad_json(DOC_LEN)) ^ 0xFFFFFFFF))]),

    # -- R3: stored bytes fail to decode under the declared encoding ----------
    # Only reachable under encoding 2: encoding 1 stores the document verbatim,
    # so "fails to decode" has no meaning there — every byte string decodes to
    # itself. The frame satisfies every §18.2 constraint (magic present, one
    # frame, no skippable, dictionary ID 0, no content-checksum flag) so that
    # the vector cannot be mistaken for an R4 instance; what fails is the block,
    # which declares itself compressed and carries garbage.
    _v("TV-0508", "zstd document that fails to decode, top-level extent",
       sub=False, row="R3", rule="R-CNT-25", detected="extent use",
       patches=[ENC[2], _ext(F_UNDECODABLE)]),
    _v("TV-0509", "zstd document that fails to decode, layer sub-record extent",
       sub=True, row="R3", rule="R-CNT-25", detected="extent use",
       patches=[ENC[2], _ext(F_UNDECODABLE)]),

    # -- R4: §18.2's frame constraints, carried over from [R-COD-06] ----------
    # Five alternatives × two containers. Four of the five decode fine under a
    # reference decoder, which is the row's point: the constraint is broken
    # whether or not the bytes decode, so a reader that only tries decoding
    # passes four of these ten by accident.
    _v("TV-0510", "zstd document missing the frame magic, top-level extent",
       sub=False, row="R4", rule="R-MTA-09", detected="extent use",
       patches=[ENC[2], _ext(F_NO_MAGIC)]),
    _v("TV-0511", "zstd document missing the frame magic, layer sub-record extent",
       sub=True, row="R4", rule="R-MTA-09", detected="extent use",
       patches=[ENC[2], _ext(F_NO_MAGIC)]),
    _v("TV-0512", "zstd document preceded by a skippable frame, top-level extent",
       sub=False, row="R4", rule="R-MTA-09", detected="extent use",
       patches=[ENC[2], _ext(F_SKIPPABLE)]),
    _v("TV-0513", "zstd document preceded by a skippable frame, layer sub-record extent",
       sub=True, row="R4", rule="R-MTA-09", detected="extent use",
       patches=[ENC[2], _ext(F_SKIPPABLE)]),
    _v("TV-0514", "zstd document carrying a second frame, top-level extent",
       sub=False, row="R4", rule="R-MTA-09", detected="extent use",
       patches=[ENC[2], _ext(F_TWO_FRAMES)]),
    _v("TV-0515", "zstd document carrying a second frame, layer sub-record extent",
       sub=True, row="R4", rule="R-MTA-09", detected="extent use",
       patches=[ENC[2], _ext(F_TWO_FRAMES)]),
    _v("TV-0516", "zstd document with a nonzero dictionary ID, top-level extent",
       sub=False, row="R4", rule="R-MTA-09", detected="extent use",
       patches=[ENC[2], _ext(F_DICT_ID)]),
    _v("TV-0517", "zstd document with a nonzero dictionary ID, layer sub-record extent",
       sub=True, row="R4", rule="R-MTA-09", detected="extent use",
       patches=[ENC[2], _ext(F_DICT_ID)]),
    _v("TV-0518", "zstd document with the content-checksum flag set, top-level extent",
       sub=False, row="R4", rule="R-MTA-09", detected="extent use",
       patches=[ENC[2], _ext(F_CHECKSUM)]),
    _v("TV-0519", "zstd document with the content-checksum flag set, layer sub-record extent",
       sub=True, row="R4", rule="R-MTA-09", detected="extent use",
       patches=[ENC[2], _ext(F_CHECKSUM)]),

    # -- R5: ill-formed UTF-8 in a string value -------------------------------
    # A lone 0xFF starts no UTF-8 sequence, so the document is not UTF-8 text at
    # all — `[R-ENC-11]`'s condition, quarantined into ignore-record by
    # `[R-CNT-25]` rather than taking the record's containing scope.
    _v("TV-0520", "string value containing ill-formed UTF-8, top-level document",
       sub=False, row="R5", rule="R-CNT-25", detected="extent use",
       patches=[ENC[1], _json(b'{"a":"\xff"}')]),
    _v("TV-0521", "string value containing ill-formed UTF-8, layer sub-record document",
       sub=True, row="R5", rule="R-CNT-25", detected="extent use",
       patches=[ENC[1], _json(b'{"a":"\xff"}')]),

    # -- R6: keys that break §4.6's name rules --------------------------------
    _v("TV-0522", "empty key, top-level document",
       sub=False, row="R6", rule="R-CNT-25", detected="extent use",
       patches=[ENC[1], _json(b'{"":1}')]),
    _v("TV-0523", "empty key, layer sub-record document",
       sub=True, row="R6", rule="R-CNT-25", detected="extent use",
       patches=[ENC[1], _json(b'{"":1}')]),
    # Written as an escape, so the JSON source is well-formed and the violation
    # is in the *decoded* key: §18.2 resolves escapes before applying §4.6.
    _v("TV-0524", "key containing U+0001, top-level document",
       sub=False, row="R6", rule="R-CNT-25", detected="extent use",
       patches=[ENC[1], _json(b'{"a\\u0001":1}')]),
    _v("TV-0525", "key containing U+0001, layer sub-record document",
       sub=True, row="R6", rule="R-CNT-25", detected="extent use",
       patches=[ENC[1], _json(b'{"a\\u0001":1}')]),

    # -- R7: not a JSON object, or marked ------------------------------------
    _v("TV-0526", "document that is not well-formed JSON, top-level document",
       sub=False, row="R7", rule="R-MTA-04", detected="extent use",
       patches=[ENC[1], _json(b'{"a":}')]),
    _v("TV-0527", "document that is not well-formed JSON, layer sub-record document",
       sub=True, row="R7", rule="R-MTA-04", detected="extent use",
       patches=[ENC[1], _json(b'{"a":}')]),
    # Well-formed JSON whose top-level value is an array: the parse succeeds and
    # the document is still unreadable, which is why this is its own instance.
    _v("TV-0528", "top-level value is not an object, top-level document",
       sub=False, row="R7", rule="R-MTA-04", detected="extent use",
       patches=[ENC[1], _json(b'[1,2]')]),
    _v("TV-0529", "top-level value is not an object, layer sub-record document",
       sub=True, row="R7", rule="R-MTA-04", detected="extent use",
       patches=[ENC[1], _json(b'[1,2]')]),
    # A UTF-8-encoded U+FEFF ahead of an otherwise sound object: §18.2 says the
    # encoding carries no byte-order mark, so a reader that strips it silently
    # accepts a document this text calls unreadable.
    _v("TV-0530", "leading U+FEFF, top-level document",
       sub=False, row="R7", rule="R-MTA-04", detected="extent use",
       patches=[ENC[1], _json(b'\xef\xbb\xbf{"a":1}')]),
    _v("TV-0531", "leading U+FEFF, layer sub-record document",
       sub=True, row="R7", rule="R-MTA-04", detected="extent use",
       patches=[ENC[1], _json(b'\xef\xbb\xbf{"a":1}')]),

    # -- R8: a non-finite number ---------------------------------------------
    # §18.2 names `1e400` as the ordinary case: RFC 8259 admits the token, and
    # its binary64 interpretation overflows to infinity. The bare `NaN` and
    # `Infinity` tokens are the same row and the same instance — a document
    # carrying one is not well-formed JSON either, so no two files could differ
    # on the predicate alone (§21.1's distinguishability test).
    _v("TV-0532", "number whose binary64 value is not finite, top-level document",
       sub=False, row="R8", rule="R-MTA-04", detected="extent use",
       patches=[ENC[1], _json(b'{"a":1e400}')]),
    _v("TV-0533", "number whose binary64 value is not finite, layer sub-record document",
       sub=True, row="R8", rule="R-MTA-04", detected="extent use",
       patches=[ENC[1], _json(b'{"a":1e400}')]),

    # -- R9: duplicate keys, identity being the decoded string ----------------
    # The register's own example: `"a"` and `"a"` differ in source bytes
    # and are one key. A reader comparing raw source bytes accepts this.
    _v("TV-0534", "two members with the same decoded key, top-level document",
       sub=False, row="R9", rule="R-MTA-04", detected="extent use",
       patches=[ENC[1], _json(b'{"a":1,"\\u0061":2}')]),
    _v("TV-0535", "two members with the same decoded key, layer sub-record document",
       sub=True, row="R9", rule="R-MTA-04", detected="extent use",
       patches=[ENC[1], _json(b'{"a":1,"\\u0061":2}')]),

    # -- R10: a key longer than 255 bytes ------------------------------------
    # 256 bytes, one over §4.6's bound. Encoding 2 is not a choice here: a
    # verbatim document has 23 bytes to work with. The frame runs the key as a
    # single RLE block and comes to exactly those 23 bytes.
    _v("TV-0536", "key of 256 bytes, top-level document",
       sub=False, row="R10", rule="R-MTA-04", detected="extent use",
       patches=[ENC[2], _ext(F_LONG_KEY)]),
    _v("TV-0537", "key of 256 bytes, layer sub-record document",
       sub=True, row="R10", rule="R-MTA-04", detected="extent use",
       patches=[ENC[2], _ext(F_LONG_KEY)]),

    # -- R11: an unknown record type with MU = 0 ------------------------------
    # Type 0x8001 is experimental (§10.2), so the bytes are conforming
    # (`[R-CNF-02]`) and the record's extent is content this specification does
    # not constrain. Flags stay as the seed wrote them — MU = 0, PE = 1 — which
    # is the whole condition: at file scope `[R-CNT-15]` makes MU = 0 an ignore,
    # and at layer scope `[R-CNT-18]` says the same in its own words. A
    # *reserved*-range type would have been the nonconforming variant, but the
    # register gives R11 no instance for it. See the findings note.
    _v("TV-0538", "unknown record type 0x8001 with MU = 0, top-level record",
       sub=False, row="R11", rule="R-CNT-15", detected="open", conforming=True,
       scope={"kind": "record", "container": "file", "record_type": "0x8001"},
       must_not_serve=["record:file:0x8001"],
       patches=[_retype(0x8001)]),
    _v("TV-0539", "unknown record type 0x8001 with MU = 0, layer sub-record",
       sub=True, row="R11", rule="R-CNT-15", detected="layer access", conforming=True,
       scope={"kind": "record", "container": "layer", "layer": "ok",
              "record_type": "0x8001"},
       must_not_serve=["record:layer:ok:0x8001"],
       patches=[_retype(0x8001)]),
]

#: Rows of §21.5 with no vector here, and why. Empty: all 11 rows and all 40
#: instances are constructible from the `meta` seed. Kept so that a later
#: reviewer can tell an empty gap list from a missing one.
SKIPPED: dict[str, str] = {}
