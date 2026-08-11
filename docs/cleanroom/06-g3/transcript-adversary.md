# Cleanroom round 6 — adversary

Protocol: ADR-0034. Access rule: `spec/tarn.md` only.

## Walk

ACCESS DISCLOSURE
==================
I read only /Users/robertkleffner/Documents/GitHub/tarn/spec/tarn.md (all 3475 lines). I ran two
throwaway Python scripts in my scratchpad: one that recomputes CRC-32C constants, and one that
parses the §21 register tables *out of that same file* to count rows and instances. No ADR, no
PLAN.md, no AGENTS.md/README, no conformance/, no registry.json, no git history, no web. No breach.

============================================================
PART 1 — IMPLEMENTATION WALK (container, then array model)
============================================================

I implemented the reader on paper, in the order §19.1 dictates, and stopped at each point where I
had to make a choice the text did not force.

OPEN. Obtain F (§19.1 step 1, `[R-CNT-10]`). Local reader: compare [0,16) to
`89 54 41 52 4E 0D 0A 1A` + 8 zeros (`[R-CNT-04]`). Fetch [F-64,F). Validate in §6.2's stated order:
magic, then CRC-32C over [0,60), then the version gate (§6.3) — and only those three touch offsets
`[R-CNT-24]` pins across majors, which is what makes the order implementable rather than merely
prescribed. Then the unordered second group (`[R-CNT-06]`): flags, committed_file_length == F and
64-aligned, dir_offset >= 16, dir_length >= 4, dir_offset+dir_length <= F-64, generation >= 1,
file_id != 0, reserved zero. `[R-ENC-10]`'s "acting on" carve-out ("comparing a field against a
constant for validation is not acting on it") is precisely the clause that keeps the mandated order
from contradicting the verify-before-use rule. Fetch the directory, verify its terminal CRC over
dir_length-4 bytes (`[R-CNT-11]`), parse records (`[R-CNT-12]`), apply MU gating (`[R-CNT-15]`),
multiplicity (`[R-CNT-14]`), non-layer extent slots (`[R-CNT-13]`), layer names (`[R-ENC-12]`,
`[R-ENC-15]`). Every one of these is decidable from resident bytes plus F, as `[R-RDR-01]` claims.
I could implement the open with no further questions.

LAYER ACCESS. §19.3's `[R-RDR-03]` enumerates the full §7.4 constraint set. I walked the inline
payload byte by byte: name, layout, linearization, codec, filter, A, S, A_slab, d, C, d dimension
entries, C channel entries, index_encoding, entry_count, crc_of_crc_array, sub-records. Packed, no
padding, exact parse or reject-layer (`[R-CNT-18]`). The fill field's length is cross-checked
against the type's element size (`[R-CNT-23]`), which is what lets the payload parse without type
knowledge and validate with it — a genuinely well-designed hinge. `[R-CNT-16]` (A and S mutually
exclusive) and `[R-CNT-17]` (extent_length == entry_count*20 + ceil(entry_count/2^16)*4, and
entry_count == geometry-derived count) close the index cross-checks with no I/O.

TILE READ. Ordinals per `[R-GEO-06]` (spatial s = sum t_i * prod_{j>i} G_j; disk ordinal s
interleaved, c*N+s planar). Index chain: crc_of_crc_array over the segment CRC array, then the
segment CRC over the segment holding entry k (`[R-IDX-04]`). Entry classification per §15.3's
table. Sentinel short-circuits to fill (`[R-TYP-08]`), never to error, and a malformed entry never
short-circuits to fill (`[R-TYP-09]`, `[R-CNF-09]`). Payload fetch, entry crc, codec, inverse
filter, exact decoded size (`[R-SER-07]`), extract by §14.2/§14.3 arithmetic, return bit patterns
(`[R-MDL-02]`, `[R-TYP-04]`).

ARITHMETIC AUDIT. I recomputed every worked example: §11.2's grids (4,8); §11.4's ordinals
(s=10, in-tile 11452, planar disk 74); §14.2's three interleaved/planar layouts (Q=3 -> 18 bytes,
offset [15,18); Q=5 -> 30 bytes, offset [25,30)); §14.3's packed plane (0x55 0x01, and 0x55 0xFD
with fill true); §14.5's edge tile (1 real position, 15 padding, 32 bytes); §15.4's 1,000,000-entry
layer (16 segments, array at [20000000,20000064), segment 15 at [19660800,20000000), 1.25 MiB
maximum full segment); §17.3's shuffle (00 00 00 00 00 00 80 00 40 3F 40 40); §12.3's 12-byte
channel entry; §4.6's NFC/NFD byte counts; §20.3's 644-byte index region; §21.9's note (256 KiB at
2^32 entries, 4 MiB at 2^36). All correct.

CONSTANT AUDIT (computed). CRC-32C("123456789") = 0xE3069283 — matches §4.5. CRC-32C of zero bytes
= 0x00000000 — matches. CRC-32C of a full segment of 65,536 sentinel entries = 0xEECB3BB2 — matches
`[R-IDX-05]` and Appendix B. Appendix A's trailer CRC over bytes [0,60) = 0xE00938D2, stored
`D2 38 09 E0` — matches the hex dump. The one constant I did not verify (the all-sentinel segment
CRC) is the one most likely to be transcribed wrong, and it is right.

REGISTER SELF-COUNT (computed from the tables in the file). §21.2 = 39 rows, §21.3 = 50, §21.4 =
26, §21.5 = 10; total 125, matching each subsection heading and `[R-ERR-02]`'s "125 conditions".
Counting instances by `[R-ERR-02]`'s own stated rule (semicolon-separated; a cell reading "—" is
one instance) gives 61 + 100 + 45 + 38 = 244, matching "244 named instances" exactly. Requirement
identifiers: 19 prefixes used, 19 declared in §2.2, no unused prefix; no numeric gaps in any prefix
(the apparent R-ENC gap is only §2.2's own `[R-ENC-100]` illustration, and withdrawn `[R-SER-04]`
is present as a retirement note, per §2.2's rule).

============================================================
PART 2 — ADVERSARIAL ATTACK LOG
============================================================
Every attack I tried, with the citation that refutes it or the finding it produced.

--- The central attack: divergent SAMPLE VALUES on a CONFORMING file. REFUTED. ---
A1. Two readers returning different values at one coordinate. The reference array is uniquely
    determined: `[R-MDL-01]` fixes it from declarations plus storedness, `[R-MDL-02]` forbids any
    alteration, `[R-GEO-06]` fixes ordinals, `[R-SER-01]` fixes the value sequence, `[R-SER-02]`
    and `[R-SER-03]` fix byte offsets and the packed form, `[R-SER-07]` fixes length exactly,
    `[R-COD-08]` fixes decode exactness, `[R-COD-02]` forbids cross-tile state, `[R-TYP-04]` makes
    values bit patterns, `[R-TYP-06]` makes fill authoritative and forbids type-derived defaults,
    `[R-TYP-08]` fixes fill delivery, `[R-GEO-04]` forbids returning padding. I found no gap.
A2. The one byte whose interpretation is a reader's choice — a non-{0x00,0x01} interleaved bool —
    is closed by `[R-SER-08]`, which defines the charitable path *and* states it cannot arise in a
    conforming file. This is the document's strongest single move.
A3. Fill vs. padding confusion. REFUTED: `[R-SER-05]` makes padding carry fill, so even a reader
    that forgets to clip observes a defined value; §13.3's note separates the mechanisms.
A4. A tile all of whose positions are padding (so `[R-SER-05]` and `[R-GEO-04]` fight over it).
    REFUTED arithmetically: t_i <= G_i - 1 and (G_i - 1)*T_i < E_i, so every tile has at least one
    real position along every axis; when E_i = 0 there are no tiles at all (`[R-GEO-02]`).
A5. NaN quieting / -0.0 collapse. REFUTED: `[R-TYP-04]`, `[R-TYP-05]`.

--- Structures that touch, abut, or nest. REFUTED. ---
A6. Zero-length structure abutting another (the classic half-open-interval divergence). REFUTED:
    no zero-length structure can exist. dir_length >= 4 (`[R-CNT-06]`); a non-sentinel entry with
    length 0 is reject-tile (§15.3); a user-metadata extent below 5 bytes is a validity error
    (`[R-CNT-25]`); (0,0) means "no extent", not "zero-length extent" (`[R-CNT-13]`); a zero-entry
    index region is (0,0) and not a structure at all (§7.4, `[R-CNT-17]`).
A7. Extent ending exactly at F-64. REFUTED as an error: the predicate everywhere is "> F - 64"
    (`[R-CNT-06]`, `[R-CNT-13]`, §15.3, L18, T9), so abutting the trailer is legal. The prose gloss
    "would touch the live trailer" in §15.3 is looser than its own predicate but the predicate is
    explicit and wins.
A8. A stored tile nested inside its own layer's index region -> reject-layer; inside another
    layer's or another scope's structure -> reject-file. REFUTED as underdetermined:
    `[R-CNT-13]` and §15.3's last three rows partition this exhaustively, and §15.3's carve-out
    ("an entry these rows classify reject-tile contributes no stored extent to the *verifier* rows")
    forecloses the double-classification I was hunting for — an entry at offset 10 is reject-tile
    (T8) and does *not* additionally become a front-block overlap.
A9. A live structure after the live directory. REFUTED: `[R-CNT-05]` makes it a file-scope error
    (F9), so the directory is necessarily last among live structures, not merely by convention.
A10. Directory overlapping the front block. REFUTED: dir_offset >= 16.
A11. Two index entries of the same layer pointing at one payload (aliasing). REFUTED as a
     conformance question by `[R-CNT-13]` (intra-layer overlap, reject-layer); acknowledged as
     reader-invisible by §22.3, which says so in terms.

--- Order of validation: can an earlier check hide a later one? MOSTLY REFUTED. ---
A12. Bad magic hiding a bad CRC hiding a bad version. REFUTED at the level that matters: §6.2
     orders them but assigns all three the same outcome, reject-file. The residue is only which
     §21 row gets attributed, which matters to `[R-VEC-02]`'s manifest and to nothing else
     (Finding 13).
A13. A reject-layer condition hiding a reject-file condition in the same layer (e.g. index_encoding
     = 2 makes the index region uninterpretable, so a cross-layer stored-extent overlap can never be
     found). Not refuted for the *slack total* (Finding 9), but refuted for the verdict: the file is
     nonconforming either way, and `[R-CNF-12]` plus `[R-VEC-04]`'s note license the narrower or
     wider refusal alike.
A14. A layer-scope failure at *open* (L4/L6/L7 put layer-record-name checks at open, outcome
     reject-layer) hiding the file-scope duplicate-name check. Produces Finding 12.
A15. Detection tier skew: a reader detects at its tier, a verifier at certification, so a reader can
     serve bytes from a file the specification rejects. REFUTED as a defect by `[R-RDR-02]`'s
     explicit "a violation whose assigned detector is the verifier ... imposes no reader
     obligation", though `[R-CNF-09]`'s own text is unconditional (Finding 8).

--- Codec/filter declarations vs. decoded content. ONE HIT. ---
A16. Codec 1 with a stored length != decoded size. REFUTED: `[R-COD-04]`, pre-fetch checkable.
A17. Filter 2 at the wrong stride. REFUTED as underdetermined: `[R-COD-10]` fixes s per layout, and
     §21.7 honestly states the residue is undetectable.
A18. Filter 2 over a packed bool plane, where L = ceil(P/8) need not divide by an element size.
     REFUTED: `[R-COD-10]` makes s = 1 and the filter the identity there, and its "L is divisible
     by s in every case" holds for all three cases (P*B/B, P*Q/Q, ceil(P/8)/1).
A19. Concatenated / skippable zstd frames, dictionary IDs, content-checksum flag, oversized window,
     mismatched Frame_Content_Size. REFUTED: `[R-COD-06]` names all five, and the note about
     whole-buffer decoders tolerating concatenation is the right warning.
A20. DEFLATE stream ending mid-byte with nonzero residual bits. NOT REFUTED — Finding 3. This is my
     strongest byte-level construction.
A21. zstd on a tile below 1 KiB decoded, where RFC 8878's minimum windowLog collides with
     `[R-COD-06]`'s window ceiling. Decidable, but only by going to the external RFC — Finding 10.
A22. LZ4 frame instead of block; lz4 at decoded size above 0x7E000000. REFUTED: `[R-COD-07]`, T23.
     Boundary check: "exceeds" means 0x7E000000 exactly is legal, consistent with `[R-ERR-05]`'s
     "at most".

--- Things the document declares unconstrained. ---
A23. Slack content. REFUTED as an attack surface for readers (`[R-CNT-21]` forbids interpreting it;
     `[R-LIF-05]` forbids scanning backward). But the *slack total*, which `[R-CNT-21]` makes a
     mandatory verifier output, is defined twice and incompatibly — Finding 4.
A24. Pre-trailer pad size unbounded, so a 1 GiB pad holding a planted 64-aligned trailer whose
     committed_file_length equals its own offset+64, with a valid directory behind it. A recovery
     scan (§9.6) lands on it before the real prior trailer, and re-verification passes because the
     planted state is genuinely conforming. PARTIALLY REFUTED: §9.6's own second caution (rollback
     detection needs out-of-band state) covers it, but §22.3's `[R-SEC-04]` presents re-verification
     as the mimic defense, which does not cover this variant — Finding 11.
A25. Record order (`[R-CNT-14]`), structure placement (`[R-SLB-05]`), version_minor, ignore-lane
     bits. REFUTED: each is unconstrained *and* explicitly non-load-bearing, with `[R-CNT-08]` even
     stating that an ignore-lane bit does not make the file nonconforming — which is the exact
     pattern §18.2's encoding space fails to follow (Finding 1).
A26. Multiplicity of *unknown* record types is unstated. `[R-CNT-14]`'s "multiplicity rules are per
     type" plus the enumeration for major 1 implies unlimited. Weak; not reported.

--- Enumerations, sentinels, degenerate geometry. REFUTED. ---
A27. Zeroed index region read as all-sparse. REFUTED: §15.2's all-ones sentinel makes 0/0 loudly
     invalid, and §15.3 gives the row.
A28. All-0xFF index region (erased flash). REFUTED: a sentinel's crc must be 0, so T6 catches it.
A29. Sentinel values colliding with `[R-ENC-03]`'s domain and `[R-ENC-04]`'s sum rule. REFUTED:
     `[R-IDX-02]` carves sentinels out explicitly, and §15.3's per-entry outcomes are stated to
     govern "notwithstanding the general owning-scope mapping".
A30. Zero-extent dimension: N = 0, entry_count = 0, extent (0,0), crc_of_crc_array = 0,
     ceil(0/2^16) = 0. REFUTED — every rule lines up (`[R-GEO-02]`, `[R-CNT-17]`, `[R-CNT-23]`).
A31. entry_count = 65536 exactly (one full segment, 4-byte array). REFUTED: arithmetic is exact.
A32. A_slab = 1 (a power of two), S > N (one short run), a run with no stored tiles, sentinels
     inside a run. REFUTED: `[R-SLB-02]`/`[R-SLB-03]` state all four.
A33. S != 0 with A_slab = 0. REFUTED: L30 and `[R-CNT-23]` both name it.

--- Conformance-class boundaries. FOUR HITS. ---
A34. Experimental metadata encoding: conforming bytes or a violation? NOT REFUTED — Finding 1.
A35. Dimension name colliding with a channel name in the same layer. NOT REFUTED — Finding 2.
A36. `[R-CNF-03]`'s unqualified "MUST accept every conforming file" against `[R-CNT-07]` and
     `[R-CNT-15]`. NOT REFUTED in `[R-CNF-03]`'s own text — Finding 5.
A37. What a verifier reports for a conforming file it must reject as a reader. NOT REFUTED —
     Finding 6.
A38. Metadata decode bound as a certification variable. NOT REFUTED, but stated — Finding 7.
A39. §9.6's "generation enumeration for coverage verification (§5.2)" against §9.7's live-state-only
     walk and "nothing here enumerates prior commits". NOT REFUTED — Finding 15.
A40. `[R-LIF-03]`'s "increasing by exactly 1 per commit" has no register row and no assigned
     detector, yet §9.6 supplies the mechanism to detect it. Folded into Finding 15.
A41. "Conformance is defined for four classes" followed by five. Finding 14.
A42. T2's "real (non-padding) sample position" narrowing `[R-SER-08]`, which has no such
     restriction. §21.1's "the rule governs" decides it and both paths land on tile scope —
     REFUTED as a divergence, reported as Finding 16 for the register's own accuracy.
A43. Point vs. region request for a single coordinate. NOT REFUTED — Finding 17.

============================================================
PART 3 — THE FILES I CONSTRUCTED
============================================================
Four files. Each is a concrete artifact two conforming implementations can judge differently, and
for each I name the two implementations and the citation each stands on.

FILE A — experimental metadata encoding.
  128+ byte file, one top-level record: type 0x0002, MU=0, PE=1, inline_length 1, encoding byte
  0x80, extent (offset >= 16, length >= 5) holding opaque bytes plus a correct terminal CRC-32C.
  Verifier V1 certifies it CONFORMING, citing `[R-CNF-02]` ("conduct rules bind the actor, the
  predicate binds the bytes"), `[R-EXT-03]` (for §18.2's space, "ignore-record under the quarantine,
  never a scope-level rejection"), and §21.6's ruling that an experimental *record type* is a
  conforming file for exactly this reason.
  Verifier V2 declines, citing §21.5's R1 — whose Instances cell names "experimental >= 0x80" —
  together with §21.1's "The register below enumerates every violation this specification names" and
  its normative completeness.
  Both readers ignore the record, so no reader-visible divergence. The certification verdict differs.

FILE B — dimension name equal to channel name.
  One layer, rank 1, dimension named "x" (extent 4, tile extent 4), one channel named "x" (uint8,
  fill 0x00), interleaved, linearization 1, codec 1, filter 1, entry_count 1, one stored 4-byte tile.
  Verifier V1 certifies, reading `[R-ENC-15]`'s "dimension names and channel names within their
  layer" as two namespaces, and pointing at L10 ("two dimension entries, *or* two channel entries").
  Verifier V2 rejects the layer, reading the same clause as one namespace — and citing §21.1's own
  instruction that "where a row and the rule it cites diverge, the rule governs", which strips L10
  of tiebreaking authority.
  Reader-visible: V1 returns the four samples; V2 serves nothing from the layer.

FILE C — DEFLATE stream with nonzero residual bits in its final byte.
  One layer, codec 2, one stored tile whose single BFINAL block's last bit falls at bit 3 of the
  final stored byte, with bits 4-7 set to 1.
  Reader R1 accepts: `[R-COD-08]` forbids "trailing *bytes* past the stream", and T24's condition is
  "*bytes* remain in the stored extent after the stream ... ends". No byte remains; the final byte is
  consumed. Every stock inflate binding reports it consumed.
  Reader R2 rejects the tile: `[R-COD-08]` also says "the decode MUST consume the stored bytes
  exactly", and under a bit-granular reading of "exactly" the stream did not consume the byte.
  Reader-visible: R1 returns sample values, R2 reports tile failure. Byte-level.

FILE D — Appendix A's own 128-byte minimal file.
  Verifier V1 reports 44 slack bytes (the pre-trailer pad), following §5.2's definition: slack is
  "every byte the live state does not claim", and the live committed state expressly includes "the
  front signature block ... together with the live directory and the live trailer".
  Verifier V2 reports 124 slack bytes, following §9.7's `[R-LIF-08]`: the walk it enumerates reaches
  "the live directory and its records, each record's extent, and each layer's tile-index region
  together with that region's non-sentinel entries" — the front block and the trailer are not in
  that list — and "Bytes the walk does not reach are slack: the verifier sums them and reports the
  total". §5.2's own Note endorses V2 ("`[R-LIF-08]` makes every byte the walk misses slack").
  `[R-CNT-21]` makes this a MUST-report output, so two conforming verifiers emit different mandated
  numbers for the specification's own worked example.
  Internal evidence that §9.7's list is exhaustive rather than elliptical: the same sentence requires
  each walked structure to lie "within [16, F - 64)", which the trailer and front block cannot.

WHAT I COULD NOT BUILD
  A conforming file whose sample values two conforming readers can return differently. Attacks
  A1-A5, A16-A19, A22, A27-A33 all die on the citations listed. Every residual divergence on a
  conforming file is about *whether* data is served, never *what* — and each of those is licensed in
  terms: resource limits (`[R-ERR-03]`, `[R-ERR-04]`), an unimplemented major (`[R-CNT-07]`,
  §21.6), an experimental record type with MU=1 (`[R-CNT-15]`, §21.6), and the metadata decode
  bound (`[R-MTA-09]`). That is a real result and the document earned it.

## Findings

### AMBIGUITY — §21.5 register row R1 (Instances cell) against §21.6 closing text, `[R-CNF-02]`, `[R-EXT-03]`, and `[R-CNT-08]`

Byte-level: True

Whether a file carrying an experimental-range (>= 0x80) user-metadata encoding byte is a conforming file is decided oppositely in two normative places. §21.6 rules for the parallel case: an experimental-range *record type* with MU = 1 is not a register row because "`[R-CNF-02]` makes the file conforming all the same, since the prohibition on publishing experimental values binds a writer's conduct and not the bytes", and it contrasts this with "a *reserved*-range type, whose emission `[R-CNT-15]` does make a violation". `[R-EXT-03]` states the reader consequence for §18.2's space as "ignore-record under the quarantine (`[R-CNT-25]`), never a scope-level rejection" — a treatment, not a verdict on the bytes. `[R-CNT-08]` sets the same precedent explicitly for a third space: "a set ignore-lane bit is not a file-conformance violation". Yet §21.5's row R1 registers "experimental >= 0x80, top-level record" and "experimental >= 0x80, layer sub-record" as two of its six instances, and §21.1 declares that the register "enumerates every violation this specification names" with normative completeness. §10.3's single prohibition ("Writers MUST NOT emit files carrying an experimental value in released software or published data") governs both spaces identically, so no distinguishing rule exists. Consequence: File A in my walk is certified conforming by one verifier and declined by another, both correctly applying the text. Note the reserved range (3-0x7F) is unaffected — under §21.6's own distinction it is a genuine violation, so only two of R1's six instances are in dispute, which is itself evidence the row was written without the record-type precedent in view.

**Readings.** Reading 1 (conduct-binds-the-actor): the file is conforming; the reader ignores the record; R1's two experimental instances are miscategorised and belong in §21.6's non-violation table alongside the ignore-lane bit and the experimental record type. Reading 2 (register-is-complete): the file is nonconforming; §21.1's normative completeness means anything listed as a row is a violation the specification names. I picked Reading 1, because §21.6 addresses the identical question for record types by name and decides it, because `[R-CNT-08]` decides it the same way for flag bits, and because `[R-CNF-02]` is a definitional rule about the conformance predicate while §21.1 is a rule about the register's coverage — a rule about bytes outranks a rule about a table. But Reading 2 is squarely available, and §21.1's "where a row and the rule it cites diverge, the rule governs" does not help, because R1 cites `[R-CNT-25]`, which fixes the outcome (ignore-record) and says nothing about file conformance.

### AMBIGUITY — §4.6 `[R-ENC-15]`, first sentence; register row L10

Byte-level: True

`[R-ENC-15]` reads: "Names are unique within their scope: layer names within a file, dimension names and channel names within their layer." The phrase "dimension names and channel names within their layer" does not say whether the layer carries one namespace shared by both kinds of name or two independent ones. The enforcement sentence inherits the ambiguity verbatim: "a duplicate dimension or channel name is a layer-scope error (reject-layer)". Nothing else in §7.4, §11.1, or §12 disambiguates — §7.4's layout table cites `[R-ENC-15]` for both entry kinds without separating them, and §3.1 defines dimension and channel independently without stating a namespace relation. The only tiebreaker anywhere is register row L10 ("Two dimension entries, *or* two channel entries, of one layer carry byte-identical name fields"), and §21.1 explicitly strips rows of authority: "where a row and the rule it cites diverge, the rule governs". Consequence: File B in my walk — one layer, dimension "x", channel "x" — is certified by one verifier and reject-layer for another, and the divergence is reader-visible, not merely a certification verdict: one implementation returns the layer's samples and the other refuses the layer entirely.

**Readings.** Reading 1 (two namespaces): dimensions are unique among dimensions, channels among channels; a dimension and a channel may share a name. Reading 2 (one namespace): the layer's dimension names and channel names are drawn from a single set and may not collide. I picked Reading 1 — it is what L10 spells out, it is what §3.1's separate definitions of dimension and channel suggest, and a shared namespace would be a surprising constraint to impose in passing without a rationale, which this document supplies for every other non-obvious rule. But the sentence as written supports Reading 2 with equal force, and the fix is one clause ('dimension names among a layer's dimensions, channel names among its channels').

### AMBIGUITY — §17.2 `[R-COD-08]`; §21.4 register row T24; §17.2 `[R-COD-05]` and row T16

Byte-level: True

`[R-COD-08]` states two things about exactness in one sentence: "the decode MUST consume the stored bytes exactly, with no trailing bytes past the stream, frame, or block". For codecs 3 and 4 the unit of the underlying format is the byte, so the two clauses coincide. For codec 2 they do not: RFC 1951 is bit-granular, and a DEFLATE stream's final BFINAL block routinely ends part-way through its last byte, leaving 1-7 bits whose content RFC 1951 does not constrain. `[R-COD-05]` ("exactly one DEFLATE compressed data stream") does not reach them either, and row T16's condition ("a second stream begins after the BFINAL block") is stated in stream terms that a few stray bits neither satisfy nor clearly escape. Row T24 phrases the check purely in bytes ("bytes remain in the stored extent after the stream, frame, or block ends"), which points one way; `[R-COD-08]`'s own "consume the stored bytes exactly" points the other. Nothing anywhere requires the residual bits to be zero, and nothing declares them unconstrained — the specification is otherwise scrupulous about doing one or the other (compare §5.2 on slack, §14.3 on pad bits, §6.2 on the pre-trailer pad, all of which state the answer explicitly). Consequence: File C in my walk is accepted by one conforming reader and reject-tile for another, and they return different things for the same coordinate of the same file. This also silently costs Appendix G a degree of freedom it does not list: two encoders that agree on every block and table decision can still differ in those trailing bits, so item 1's 'named implementation at a named version with fixed settings' is doing more work than it appears to.

**Readings.** Reading 1 (byte-granular): 'consume the stored bytes exactly' means no whole byte is left over; the final byte is consumed because the stream ends inside it, and its residual bits are unconstrained like any other bits the format does not name. Reading 2 (bit-granular): 'exactly' means the stream's extent is the extent, so bits after BFINAL are residue and the tile is invalid under `[R-COD-08]`. I picked Reading 1 — T24 is written in bytes, `[R-COD-08]`'s own qualifier is 'no trailing *bytes*', and every stock inflate binding reports the final byte consumed, so Reading 2 would make conformance turn on a quantity most implementations cannot observe without a bit-level decoder. The document should say so in one clause: the unused high bits of a DEFLATE stream's final byte are unconstrained (or MUST be zero), and either choice is fine as long as it is made.

### CONTRADICTION — §5.2 `[R-CNT-21]` and its defining paragraph, against §9.7 `[R-LIF-08]`; §5.2's own trailing Note takes §9.7's side

Byte-level: False

The slack total is a mandatory verifier output that is defined twice, incompatibly, with an 80-byte difference on every file. §5.2: "Coverage is a property of the **live committed state** — the front signature block, and every structure reachable from the live trailer through the live directory's records, extent slots, and tile-index entries, together with the live directory and the live trailer." and "Every byte the live state does not claim is **slack**" and "a verifier MUST report the total number of slack bytes". Under that definition the 16-byte front block and the 64-byte trailer are claimed and are not slack. §9.7 `[R-LIF-08]`: "From the live trailer it enumerates the live directory and its records, each record's extent, and each layer's tile-index region together with that region's non-sentinel entries; it checks that these occupy disjoint byte ranges, that each lies within [16, F − 64) ... Bytes the walk does not reach are slack: the verifier sums them and reports the total." That enumeration omits the front block and the trailer, so under §9.7 they are slack. The list is exhaustive rather than elliptical by its own internal evidence: it requires every walked structure to lie within [16, F − 64), which the trailer at [F−64, F) and the front block at [0, 16) cannot. §5.2's own trailing Note then endorses the §9.7 reading against §5.2's definition: "`[R-LIF-08]` makes every byte the walk misses slack". On Appendix A's 128-byte file the two answers are 44 and 124. The fix is one clause in §9.7 adding the front block and the trailer to the walk, or excluding them from the sum.

**Readings.** Reading 1 (§5.2's definition governs): slack excludes the front block and the trailer; §9.7's walk list is an incomplete restatement. Reading 2 (§9.7's procedure governs, as §5.2's Note says): the walk's reach defines slack, so the 80 bytes count. I picked Reading 1 — §5.2 is where slack is defined and where the reporting obligation lives, and calling the trailer 'slack' contradicts §5.2's enumeration of coverage classes, which lists the trailer as a structure. But §5.2's Note explicitly hands the definition to `[R-LIF-08]`, which makes Reading 2 the one a careful implementer following cross-references arrives at.

### CONTRADICTION — §2.3 `[R-CNF-03]` against §6.3 `[R-CNT-07]` and §7.2 `[R-CNT-15]`; §21.6 states the resolution but does not amend `[R-CNF-03]`

Byte-level: False

`[R-CNF-03]`: "A reader MUST accept every conforming file none of whose values exceeds the minimum guarantees of §21's limits table" — one qualifier, resource limits, and no other. `[R-CNT-07]`: "A reader MUST reject-file when version_major is 0 (invalid) or is a major it does not implement". `[R-CNT-15]`: "An unknown record type at file scope: MU = 1 → reject-file", which applies unchanged to the experimental range. §21.6 identifies exactly these two cases: "Two distinct cases are **conforming files a reader nevertheless refuses**. The first is **version_major naming a major this reader does not implement**: the reader rejects the file (`[R-CNT-07]`), but the file can be perfectly conforming under that major. The second is an **experimental-range record type carrying MU = 1**". So a major-1 reader handed a conforming major-2 file whose values are within §21.9's guarantees is under a MUST to accept and a MUST to reject. §21.6 resolves the direction, so this is a soft contradiction — but `[R-CNF-03]` is the sentence implementers read first and it carries a false absolute. The repair is mechanical: qualify `[R-CNF-03]` with 'of a format major version it implements, and carrying no record type it does not implement with MU = 1'.

**Readings.** Both citations are quoted above; §21.6 fixes the resolution in favor of `[R-CNT-07]` and `[R-CNT-15]`. The defect is that `[R-CNF-03]` carries no cross-reference to §21.6, so a reader auditing itself against §2.3 alone concludes it is nonconforming for obeying `[R-CNT-07]`.

### AMBIGUITY — §2.3 `[R-CNF-11]` and the `[R-CNF-02]` bullet, against §2.4's reject-file row and §21.6's 'conforming files a reader nevertheless refuses'

Byte-level: False

The verifier's verdict space is not defined for the case §21.6 names. `[R-CNF-11]` makes a verifier "a reader that additionally checks every file-level requirement ... and certifies conformance", and "Verifiers and updaters are readers of the files they process and inherit every reader obligation." §2.4's outcome table says reject-file means "The file is not usable ... A reader MUST NOT rely on any structure in it." Now hand a verifier a conforming file carrying an experimental-range record type with MU = 1 (or a conforming file of a major it does not implement). As a reader it MUST reject-file and MUST NOT rely on any structure in the file — so it cannot check anything and cannot certify. As a verifier it is looking at a file the specification declares conforming (`[R-CNF-02]`, §21.6). A second verifier that happens to implement that private-use type does not reject and certifies. The specification defines a third verdict — 'cannot establish conformance, MUST NOT certify' — in exactly two places (`[R-COD-11]` for an unexecutable codec, `[R-MTA-09]` for an undecodable document) and never generalises it, so it is unclear whether the first verifier reports 'nonconforming', 'unusable', or 'cannot establish'. The two outputs send an operator to opposite conclusions about the file, exactly as `[R-ERR-04]` argues for resource limits. Generalising `[R-COD-11]`'s 'cannot establish ... MUST NOT certify' into §2.3 as the verifier's third verdict, and naming §21.6's two cases as instances of it, would close this.

**Readings.** Reading 1: the verifier reports 'cannot establish conformance' and declines, by analogy to `[R-COD-11]`/`[R-MTA-09]`. Reading 2: the verifier reports the file nonconforming, since reject-file is the outcome it must apply and §2.4 gives it no other. Reading 3: the verifier certifies conforming and separately reports that it cannot read the file, since `[R-CNF-02]` makes conformance a pure predicate on bytes that the verifier can evaluate for every requirement except the one it lacks capability for. I picked Reading 1 as the only one consistent with both `[R-CNF-02]` and §2.4's prohibition on relying on any structure, but the text does not say it.

### OBSERVATION — §18.2 `[R-MTA-09]`, in conjunction with §21.9's 16 MiB user-metadata guarantee and `[R-MTA-05]`/rows F30, L49

Byte-level: False

`[R-MTA-09]` makes the certification verdict for a class of conforming files depend on a verifier's freely chosen resource bound: "a reader instead decodes with a bound of its own choosing, no smaller than §21.9's user-metadata guarantee ... A **verifier** that declines to decode a document cannot establish its conformance and MUST NOT certify the file". Take a conforming file whose user-metadata document decodes to 100 MiB with correctly sorted members. A verifier with a 1 GiB bound certifies it; a verifier with the minimum 16 MiB bound MUST NOT certify it. Both are conforming verifiers, both correct. The mirror case is worse: if that same 100 MiB document has unsorted members, it is nonconforming under `[R-MTA-05]` (rows F30/L49), and only a verifier that happens to have chosen a large bound can ever say so. This is decidable and the text is internally consistent — it is an OBSERVATION rather than a defect because the cost falls entirely on interpretation: the specification's claim that file conformance is 'a pure predicate on bytes' (`[R-CNF-02]`) is true, but for these files no bounded verifier can evaluate the predicate, and the document never says which quantity a verifier should report. Deciding a given file requires knowing a verifier's private configuration, which is precisely the class of thing §2.5/`[R-CNF-10]` says must never determine validity: "Every limit that affects which files are valid or which files a conforming reader accepts lives in this specification, never only in an implementation."

### AMBIGUITY — §2.4 `[R-CNF-09]` against §19.2 `[R-RDR-02]` and §7.2 `[R-CNT-13]`

Byte-level: False

`[R-CNF-09]` is written without condition: "A reader MUST NOT return data as valid from a scope this specification rejects". Several rejections are assigned to the verifier alone and are explicitly beyond a reader's reach — `[R-CNT-13]` says so in terms: "readers are not obligated to detect overlap, which requires whole-directory knowledge", and the corresponding register row F36 (a stored-tile extent overlapping another scope's structure) is reject-file. So a reader handed a file whose tile payload overlaps the directory region will fetch those bytes, find the entry crc matches, and return them as samples — returning data as valid from a scope the specification rejects. Constructing this is trivial: place a 4-byte stored tile at exactly dir_offset with a matching crc. §19.2's `[R-RDR-02]` supplies the reconciliation — "a violation whose assigned detector is the verifier (§2.4, `[R-CNF-12]`) imposes no reader obligation" — and §22.3 confirms it ("a reader that skips them is still conforming"). So the text does refute the attack, but only from a rule two sections away; `[R-CNF-09]` should carry the qualifier itself ('a scope this specification rejects and this reader is obliged to detect'), since it is the rule an implementer cites when deciding what to do on detection.

**Readings.** Reading 1 (literal): the reader is nonconforming for returning the samples, whether or not it could have known. Reading 2 (`[R-RDR-02]`-qualified): the obligation attaches only to rejections whose detection the reader owes. I picked Reading 2 — `[R-RDR-02]` is explicit, §22.3 confirms the reader/verifier gap is deliberate, and Reading 1 would make conformance depend on a check the specification elsewhere says readers need not perform.

### OBSERVATION — §9.7 `[R-LIF-08]` and §5.2 `[R-CNT-21]`, where a layer-scope rejection blocks the coverage walk

Byte-level: False

`[R-CNT-21]` makes reporting the slack total unconditional ("a verifier MUST report the total number of slack bytes"), and §9.7 defines the total as what the walk does not reach. But the walk can be blocked. A layer declaring index_encoding = 2 is reject-layer (`[R-CNT-23]`, row L32), and its tile-index region cannot be parsed — index entry layout is per encoding (`[R-ENC-07]`: "for structures whose size is a function of a declared encoding (the tile index), the fixed size is per encoding"), so the verifier cannot enumerate that layer's non-sentinel entries and cannot know which bytes its stored tiles claim. Those bytes therefore land in the slack total, and a verifier that parses the region as raw-segmented anyway gets a different total. The same arises wherever a layer-scope rejection precedes entry enumeration (a failed crc_of_crc_array, row L38; a failed segment CRC, row L39; an entry_count cross-check failure, rows L22/L23). This is decidable but expensive to decide, because deciding it means settling what the slack total means for a file that is already nonconforming — plausibly nothing, in which case the honest rule is that the total is reported only for files the walk completes on, and `[R-CNT-21]`'s MUST should say so.

### OBSERVATION — §17.2 `[R-COD-06]`, the window-size and Frame_Content_Size sentences, against Appendix F's RFC 8878

Byte-level: True

`[R-COD-06]` says writers "MUST NOT declare a window size exceeding the tile's decoded size" and, separately, that "The frame content-size field MAY be present". Under RFC 8878 the smallest Window_Size expressible in a Window_Descriptor byte is 1 KiB (windowLog = 10 + Exponent), and the descriptor is absent only when Single_Segment_Flag is set — in which case the frame MUST carry Frame_Content_Size and Window_Size equals it. So for any tile whose decoded size is below 1024 bytes, the only conforming zstd encoding is a single-segment frame, and Frame_Content_Size is not optional at all but mandatory (and, by the same requirement's later clause, must equal the decoded size). Small tiles are not exotic: §14.2's own worked example has an 18-byte decoded tile, and §14.3's has 2 bytes. The interaction is fully decidable, but only by cross-reading RFC 8878's frame-header rules against two clauses of `[R-COD-06]` that sit four sentences apart, and an implementer who does not do that will either emit nonconforming small-tile zstd files or reject conforming ones. One sentence of note text ('for a tile whose decoded size is below 1 KiB, Single_Segment_Flag is forced, and Frame_Content_Size with it') would retire this — the document does exactly this kind of derivation-sparing elsewhere, e.g. §11.2's note on the ceiling-division idiom.

### OBSERVATION — §22.3 `[R-SEC-04]` against §9.6 `[R-LIF-06]`'s two cautions

Byte-level: False

`[R-SEC-04]` states the trailer-mimic risk and names one mitigation: "a payload can contain a byte string that mimics a trailer; recovery tooling that scans backward can land on one, which is why recovery output is re-verified as a whole file before being trusted (`[R-LIF-06]`) before any use." Re-verification does not mitigate the strong form of the attack. Nothing bounds the pre-trailer pad — `[R-CNT-05]`: "this specification bounds neither their number nor their content" — so an attacker can place, inside a large pad or inside any slack run, a complete and internally consistent generation: a 64-aligned trailer whose CRC verifies, whose committed_file_length equals its own offset + 64, and whose dir_offset/dir_length address a directory the attacker also planted. §9.6's scan finds it first ("The nearest-to-end valid candidate is the last committed state"), truncation produces a file that is fully conforming, and re-verifying it whole therefore passes. The genuine answer is §9.6's *second* caution — "truncation of a file to an earlier commit boundary is indistinguishable in-format from that earlier version — rollback detection requires out-of-band state" — which covers a planted state as well as a genuine earlier one. So the document contains the right answer; the defect is that `[R-SEC-04]` attributes the defense to the first caution, which does not carry it. §21.6's row for this condition ("A payload contains a byte string that mimics a trailer | Inert: nothing enumerates slack, and a recovery tool re-verifies its output whole") repeats the same misattribution.

### OBSERVATION — §19.4 `[R-RDR-04]` step 1, against §21.6's row on out-of-extent coordinates

Byte-level: False

Step 1 assigns two different behaviors on the basis of a distinction it never defines: "For a point request, verify 0 ≤ xᵢ < Eᵢ for every dimension; a coordinate outside the extents addresses nothing in the reference array (`[R-MDL-01]`) — the request fails as a request, with no verdict on the file. A region request covers the region's intersection with the extents: a region wholly outside them ... succeeds and returns no samples". A request for a single coordinate is describable both ways — as a point, or as a 1×1×…×1 region — and no rule says which. So a reader offering one read entry point can, for the same out-of-extent coordinate on the same conforming file, either fail the request or succeed with zero samples, and both are defensible. §21.6's row ("A requested coordinate lies outside the layer's extents | The request fails as a request ... a region request returns the intersection, empty if disjoint") restates the split without resolving it. This is API surface rather than bytes, which is why it is an OBSERVATION — but it is the one place the document lets an observable behavior on a conforming file turn on an undefined term, and it is decidable only by fiat ('a request naming a single coordinate is a point request').

### OBSERVATION — §24 `[R-VEC-02]`, against §6.2 `[R-CNT-06]`'s mandated validation order

Byte-level: False

`[R-VEC-02]` requires each manifest entry to record, "for each structure the file damages, the outcome class (§2.4), the scope, and the §21 register row it exercises". Register-row attribution is not always determined. §6.2 orders the first three trailer checks (magic, CRC, version gate) but leaves the remaining eight unordered — "MUST validate all of the following" — and every one of the eleven is reject-file (rows F10, F16, F20/F21, F11-F19, F22). A file damaged in two of them therefore has no single row it 'exercises': one conforming reader reports F10, another F16, and §21.1's 'conditions attach to the finest structure they damage' does not discriminate, because both attach to the trailer. The same holds across the ordered prefix, where an earlier check deliberately hides later ones. This costs nothing in outcome — every path lands on reject-file — and it is decidable by construction discipline (build each vector to exhibit exactly one row), which is presumably the intent. Worth stating because `[R-VEC-02]` phrases it as a property recorded *of the file* rather than a constraint *on how the file is built*, and the latter is what makes it well defined.

### CONTRADICTION — §2.3, opening sentence, against the five bullets that follow it and Appendix H

Byte-level: False

§2.3 states "Conformance is defined for four classes." Five classes follow, each with its own requirement identifier: **Conforming TARN file** (`[R-CNF-02]`), **Conforming reader** (`[R-CNF-03]`, `[R-CNF-04]`), **Conforming writer** (`[R-CNF-05]`), **Conforming updater** (`[R-CNF-06]`), **Conforming verifier** (`[R-CNF-11]`). Appendix H confirms five, giving a checklist for each. §2.1 makes all of §2.3 normative (the exclusions are §1, labeled Notes/Examples/Rationales, and appendices identified as non-normative), so this is a normative miscount rather than a typo in prose. It is editorial and decides nothing, but it sits in the section the document's own §1 tells readers to read first ("§2 fixes the conformance vocabulary every later section uses, and is worth reading first").

### CONTRADICTION — §9.6 `[R-LIF-06]`, final sentence of the first paragraph, against §9.7 `[R-LIF-08]` and its Note

Byte-level: False

§9.6 assigns generation enumeration to coverage verification: "Generation enumeration for coverage verification (§5.2) is the same probe continued to offset 0." §9.7 defines coverage verification as live-state-only and denies any such enumeration: "A verifier checking `[R-CNT-02]`'s partition walks the live state only", and its Note: "Nothing here enumerates prior commits. A verifier certifies what a reader can reach and counts what it cannot, which is decidable from the live trailer in one pass and does not depend on reconstructing the file's history". Both are normative. Two conforming verifiers therefore do different work: one continues the §9.6 probe to offset 0 and inspects every prior trailer, the other never leaves the live state. A related gap sharpens it. `[R-LIF-03]` requires "generation g ≥ 1, increasing by exactly 1 per commit", which is a constraint on trailer bytes, not merely on conduct — yet it has no register row, no assigned detector, and no stated outcome, and §21.7's inventory of what no check detects covers only content incorrectness, not this. The §9.6 probe is exactly the mechanism that would find a violation of it (gen 1 at offset 128, gen 5 at the end, with nothing in between), so a verifier following §9.6 can observe a violation the specification never tells it what to do with, while a verifier following §9.7 cannot observe it at all. Since prior generations' bytes are slack and "no conformance requirement applies to it" (`[R-CNT-21]`), the intended answer is almost certainly that §9.6's clause is vestigial and should be struck — but the text as written licenses both behaviors and leaves `[R-LIF-03]`'s increment obligation unassigned.

### OBSERVATION — §21.4 register row T2, against §14.2 `[R-SER-08]` and §14.5 `[R-SER-05]`

Byte-level: False

Row T2 narrows the rule it cites. `[R-SER-08]` is unqualified: "Writers MUST NOT emit any byte other than 0x00 or 0x01 as an interleaved bool value." T2 restricts the condition to real positions: "In an interleaved tile, a bool channel's single value byte at a **real (non-padding)** sample position is neither 0x00 nor 0x01". Padding positions are not exempt from `[R-SER-08]` — §11.3 says "Padding positions are serialized like any other position" — so a padding bool byte of 0x02 violates `[R-SER-08]` while falling outside T2. It is caught anyway by `[R-SER-05]`/row T4 (padding must carry the recorded fill, which for a bool channel is constrained to 0x00 or 0x01 by `[R-TYP-07]`), and both rows are tile scope, so no outcome diverges and no file is judged differently. Reported only because §21.1 makes register completeness normative — "a violation this specification names and the register omits is a defect in this document" — and T2's qualifier means the register does not, on its face, cover every instance of the rule it restates. Deleting the parenthetical would make T2 coextensive with `[R-SER-08]` at no cost.


## Verdict
This document is the tightest format specification I have audited, and the adversary's central objective fails against it. I could not construct a conforming file whose sample values two conforming readers could return differently, and I do not believe one exists: `[R-MDL-01]`/`[R-MDL-02]`, `[R-GEO-06]`, `[R-SER-01]`-`[R-SER-03]`, `[R-SER-07]`, `[R-COD-02]`, `[R-COD-08]`, `[R-TYP-04]`, `[R-TYP-06]`, `[R-TYP-08]` and `[R-GEO-04]` between them fix the reference array uniquely from declarations plus stored bytes, and the one byte whose interpretation could have been a reader's choice is closed by `[R-SER-08]`, which defines the charitable path and proves it unreachable in a conforming file. Every remaining divergence I found on a conforming file is about WHETHER data is served, never WHAT, and each is licensed in terms (`[R-ERR-03]`/`[R-ERR-04]`, `[R-CNT-07]`, `[R-CNT-15]`, `[R-MTA-09]`). The classic traps are all pre-closed: no zero-length structure can exist, so no abutting-interval ambiguity arises; sentinels are carved out of the domain and sum rules by `[R-IDX-02]`; a reject-tile entry is explicitly barred from feeding the verifier-only overlap rows; the all-padding tile is unreachable by grid arithmetic; and `[R-ENC-10]`'s "comparing against a constant is not acting on it" is exactly the clause needed to keep §6.2's mandated order from contradicting verify-before-use. I also recomputed all three checksum constants (0xE3069283, 0xEECB3BB2, and Appendix A's 0xE00938D2/`D2 38 09 E0`) and every worked example, and machine-counted the register: 125 rows and 244 instances, matching `[R-ERR-02]` exactly. Nothing is off.

But the objective does not fail completely. I constructed four files that two conforming implementations judge differently, and three of them turn on the conformance predicate itself rather than on licensed capability. FILE A (a user-metadata encoding byte of 0x80) is conforming under `[R-CNF-02]`/`[R-EXT-03]` and §21.6's own ruling for the identical record-type case, and nonconforming under register row R1 — the document decides the same question two ways in two spaces governed by one §10.3 prohibition, and `[R-CNT-08]` shows it deciding it a third time, correctly, for flag bits. FILE B (a dimension and a channel both named "x") turns on whether `[R-ENC-15]`'s "dimension names and channel names within their layer" is one namespace or two; row L10 answers, but §21.1 explicitly denies rows that authority, and this divergence is reader-visible, not merely a certification verdict. FILE C (a DEFLATE stream whose final byte carries residual bits after BFINAL) turns on whether `[R-COD-08]`'s "consume the stored bytes exactly" is byte-granular or bit-granular; the document is scrupulous everywhere else about either constraining or explicitly releasing such bits, and here does neither. FILE D is the specification's own Appendix A file, for which §5.2 and §9.7 mandate slack totals of 44 and 124 — a required verifier output defined twice, with §5.2's own Note taking §9.7's side against §5.2's definition.

The pattern under the three substantive findings is the same and worth naming: each is a place where the document made a hard call correctly in one location and then failed to propagate it to a structurally identical case. §21.6 solves the conduct-versus-bytes problem for record types and `[R-CNT-08]` solves it for flag bits, but §21.5's R1 was written without either in view. `[R-CNF-03]` states an absolute that §21.6 later carves twice without amending it. §9.7's walk restates §5.2's coverage classes and drops two of them. None of these is a design flaw; all four are one-clause repairs. My priority order for a next pass: Finding 1 (experimental metadata encoding — a genuine split in the conformance predicate), Finding 2 (name namespace — the only reader-visible split), Finding 3 (deflate tail bits — the only byte-level accept/reject split), Finding 4 (slack total — a mandated output defined twice), then Findings 5, 6 and 15, which are cheap and which a fresh implementer will hit while reading §2.3 first, exactly as §1 instructs.