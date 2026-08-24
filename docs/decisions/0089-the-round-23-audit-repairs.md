# 0089. §18.2's carry-over gets its four missing sentences, and R4's clause stops overclaiming

- Status: Accepted (resolves the round-23 repair audit's five confirmed findings)
- Date: 2026-08-24
- Covers: §18.2's reader bound across both encodings; the carried-over items R4
  does not register; the document-side window SHOULD and the single-segment
  derivation; §21.7's undisclosed-dictionary appositive; `[R-MTA-09]`'s
  content-size clause in R4's Condition cell
- Revises: the trailing clause ADR-0087 gave R4, and three sentences ADR-0088
  wrote into §18.2
- Confirm: none

## Context

The repair audit that precedes round 23 read the whole accumulated diff since
round 22's charter commit — ADR-0086's quantifier fix, ADR-0087's R4 routing,
and ADR-0088's carry-over inversion. Three auditors returned **18 findings**,
independent verification graded 16 REFUTED and 1 PARTIAL, and **no auditor and
no verifier flagged a single finding byte-level.**

A unanimous zero is this project's trigger for the refute phase, not a result:
an earlier audit verified 31 findings with agents told to default to REFUTED,
returned zero byte-level, and a refute pass overturned all four of its
downgrades. Eight refuters ran, one per finding group. **All eight returned
DOWNGRADE_STANDS — the zero holds, and nothing in the accumulated diff forks
the bytes.** Five findings nonetheless survive as real defects in the text,
and three of the eight groups returned a *missing sentence*: a place where the
reasoning that answers a finding exists, but only in a commit message or a
tooling acknowledgement, and never in `spec/tarn.md`. A reader has neither.
That is the defect, and this decision closes it in four places.

The deepest of the five is worth stating in full, because it was not created by
any recent repair and had never been noticed. §21.9 guarantees a conforming
reader **16 MiB** of user-metadata document, and `[R-ERR-03]` expressly says a
writer MAY rely on that. §21.9 separately guarantees **8 MiB** of zstd
`Window_Size`, and that row ranges over the compressed frames a file contains —
a metadata frame among them. For a frame with `Single_Segment_Flag` set, RFC
8878 supplies no Window_Descriptor and the frame's `Window_Size` **is** its
content-size field, which §18.2 pins to the decoded document's byte length. So
a 12 MiB metadata document in the ordinary single-segment framing exceeds the
8 MiB row and forfeits `[R-CNF-03]`'s acceptance duty. The two rows disagree in
practice, and one of them is a guarantee a writer was invited to rely on.

Worse, the single-segment derivation appears in this document **only inside a
Note**, whose own opening clause reads "for a tile this rule they agree". By
`[R-CNF-01]` it carries no force, and by its own words it does not reach §18.2.
A reader of the normative text has never been told that a frame without a
Window_Descriptor has a `Window_Size` at all.

Two measurements bound the choice. Against libzstd, a reader that allocates its
bound and decodes the frame whole accepts a **2 GiB** declared window on an
1800-byte payload even with its ceiling pinned to 8 MiB — the decoder writes
straight into the destination buffer and allocates no window. Feed the same
bytes in chunks and the ceiling is enforced exactly: a 16 MiB frame against an
8 MiB cap fails. **The window guarantee binds a streaming reader and no other.**
And RFC 8878 §3.1.1.1.2 is where the 8 MiB itself comes from: "it's recommended
for decoders to support values of Window_Size up to 8 MB, and for encoders not
to generate frames requiring a Window_Size larger than 8 MB."

## Decision

**§21.9's numbers do not move.** 8 MiB is RFC 8878's own interoperability
figure, adopted; raising it would require of every conforming reader more than
the codec's specification recommends, make a reader built exactly to that
recommendation nonconforming, raise the tile-side floor where nothing needs it,
and couple two rows the table presents as independent. ADR-0039 left "RFC
8878's own decoder-resource guidance" governing and this keeps it there. The
interaction is made **visible and navigable** instead, in normative text.

Five repairs, all in normative prose:

1. **The reader's document bound is stated once, for both encodings.** §18.2
   stated it only inside the encoding-2 paragraph, and ADR-0088 then tied it to
   "the first exception" — an exception to `[R-COD-06]`, which reaches encoding
   2 alone. §21.9's row is encoding-agnostic and a verbatim document can exceed
   it too. The bound now sits with encoding 1's own sentence and governs both;
   the encoding-2 paragraph points at it rather than restating it.

2. **The two carried-over items R4 cannot register are named.** ADR-0088 widened
   the carry-over to include dictionary use "disclosed or not" and the bar on
   sizing a buffer from a frame-declared length. R4 registers breaches of that
   list as **reader-detected file violations**, and neither of those two is a
   state a file exhibits: the first is a writer violation with no witness in the
   extent, the second binds a reader. §21.1 routes R4's arbitration to
   `[R-MTA-09]`, so the widened text governs and the carve-out has to be there.

3. **The document-side window SHOULD, and the single-segment derivation, become
   normative.** `[R-COD-06]` asks a tile's writer to stay within the 8 MiB
   guarantee; §18.2 excepted the window and put nothing in its place, which is
   why ADR-0088's "this section replaces both" was an overclaim. Both are now
   stated for a document, including the consequence: a document larger than the
   guarantee, framed single-segment, forfeits the acceptance duty, so a writer
   needing one frames it with a Window_Descriptor.

4. **§21.7's undisclosed-dictionary appositive reaches a document.** It scoped
   the undetectable class to "wrong sample values", which a document does not
   have. `[R-MTA-09]` now carries the same prohibition, so §21.7 says so.

5. **R4's Condition cell stops asserting a breach that is not one.** ADR-0087
   appended "and — for the content-size field — whether or not they decode to
   the length it declares". The document's own idiom is against it: every other
   occurrence of "whether or not" in this specification has a consequent that
   holds in **both** branches of its variable, so the clause asserts the
   constraint is broken where the field *matches*, which `[R-MTA-09]` declares
   conforming. The blanket "broken whether or not the bytes decode" also came to
   range over a constraint whose comparand exists only on a successful decode.
   The cell now takes **T22's formulation** — present and unequal — which states
   the condition positively and leaves R4's purpose intact: a reader that only
   tries decoding establishes none of these.

## Consequences

The register does not move: 121 conditions, 277 instances, 331 vectors, and R4's
sixteen instances are unchanged, since "declared larger" and "declared smaller"
are exactly *present and unequal* in both directions.

Repair 3 makes explicit a limit on `[R-ERR-03]`'s "a writer MAY rely on that": a
writer relying on the 16 MiB user-metadata row above 8 MiB must choose its
framing. That is the honest cost of keeping the window row at RFC 8878's figure,
and stating it is better than a reader discovering it.

Repairs 1, 2 and 3 close the gap the audit named directly: reasoning that lived
in a commit message and in `propagation-acks.txt` now lives in the document.
The acknowledgement for `R-COD-06 -> R-COD-06` is amended accordingly, since its
stated reason — that the newly carried constraints add no file condition — is
now a sentence a reader can find.

## Precedent

- RFC 8878 §3.1.1.1.2's 8 MB recommendation for decoders and encoders alike,
  which is where §21.9's row came from and why it stays.
- `[R-CNF-01]`, which is why a derivation stated only in a Note could not carry
  the fact §21.9's row turns on.
- T22's formulation, which states the same content-size condition positively for
  a tile and has never been read the way R4's clause could be.
- ADR-0081's repair audit and the refute phase, which found all five of these
  before a fresh-context round did.
