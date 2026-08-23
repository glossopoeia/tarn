# 0087. A metadata frame's content-size mismatch is an R4 constraint, with four instances

- Status: Accepted (closes the register debt the round-22 pre-round audit recorded)
- Date: 2026-08-21
- Covers: §18.2's content-size routing; R4's condition and instances; §21.8's
  instance total; four new vectors
- Revises: the routing ADR-0085's repair asserted, which sent the mismatch to R3
- Confirm: none

## Context

`Frame_Content_Size` is a **declaration**, not a checksum: a field in the RFC
8878 frame header where the compressor writes how many bytes the frame decodes
to. Nothing verifies it, and whether a decoder notices a false value is a
property of that decoder, not of the bytes.

For a tile, `[R-COD-06]` pins it against an independent source of truth — "when
present it MUST equal the tile's decoded size … and a reader MUST NOT allocate
or size any buffer from it — the decoded size comes from the layer's
declarations alone". §22.2 explains why: allocation runs "from geometry and
never from a length embedded in a payload", which "is this format's
decompression-bomb defense".

A user-metadata document has no declared size, so `[R-MTA-09]` withdrew that
constraint and put nothing in its place. Round 21's adversary showed the
consequence: a frame declaring 999 that decodes to 100 was caught by no rule
but R3, "stored bytes fail to decode" — and whether those bytes "fail to
decode" depended on the decoder, against `[R-CNF-02]`'s "conformance is a
property of bytes: it does not depend on any reader, writer, or environment".

The repair pinned the field to the decoded document's byte length. **It routed
the mismatch to R3, and that was wrong** — the pre-round audit said so four
times, verification refuted it, and reading the row text settles it against
the refutation.

## Decision

**The mismatch is an R4 constraint.** R3's condition is "stored bytes **fail to
decode**", and a frame that decodes cleanly to a length its header misstates
does not fail to decode; what is wrong is what the header said about bytes that
decoded. R4's condition is "breaks one of the frame constraints **§18.2
states**", which this is — §18.2 states it.

R4's trailing clause is extended to match: the constraint is broken "whether or
not the bytes decode, **and — for the content-size field — whether or not they
decode to the length it declares**". R4's purpose was already this, as its own
vector commentary records: "a reader that only tries decoding passes four of
these ten by accident." R4 is the row for constraints a reader must actively
check, which is exactly what a content-size mismatch is.

**Four instances, by §21.1's own criterion.** The mismatch is a magnitude
comparison, so it takes the direction axis — declared larger, declared smaller
— exactly as F23 and L12 do under ADR-0079, across the two placements R4
already carries. §21.8's instance total moves **273 → 277**; the condition count
stays 121, because no row was added.

**Four vectors, landing in this commit**: TV-0957 through TV-0960. They set
Single_Segment, so the content-size field is one byte and RFC 8878 makes
`Window_Size` equal to it — both values stay far under §21.9's 8 MiB guarantee,
so each vector carries the content-size mismatch and nothing else. The block
still declares its true length, so the frame decodes; only the header lies.

## Consequences

**On codec coupling, which the maintainer raised.** This decision adds no new
codec vocabulary: §18.2 says "the frame's content-size field", the same words
`[R-COD-06]` already used, and `Frame_Content_Size` as an identifier still
appears exactly once in the document, in T22's row where it already was. The
document names zstd 19 times, RFC 8878 six, deflate ten; the deepest frame
internals — `Window_Descriptor`, `Single_Segment_Flag` — appear only inside a
non-normative Note.

The concern is nonetheless well aimed, and it is worth stating what bounds the
growth: codec knowledge is admitted **only where a codec's own header can
contradict what TARN declares elsewhere**, and every such rule lives in §17.2
or is carried over from it by explicit reference. A new codec inherits the
frame of §17's structure — declare, constrain what the header may contradict,
register the rows — rather than requiring new machinery. What it does cost is
rows: the eleven codec rows T15–T25 are the standing bill, and a fourth codec
would add its own.

## Precedent

- `[R-COD-06]`'s tile rule, transposed here to the quantity a document has.
- ADR-0079's direction axis, which fixes the instance count at four rather than
  one.
- ADR-0064's instance identity, which is why each vector names its instance in
  the register's own words.
