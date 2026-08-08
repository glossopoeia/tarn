## Findings

### BYTE-LEVEL AMBIGUITY

None found in §11–§18. Every path from declarations to returned sample bytes closed under attack: geometry (§11.1–§11.3), the three ordinal formulas (§11.4 `[R-GEO-06]`), element sizes (§12.1), fill (§13), the value sequence and both offset tables (§14.1–§14.2 `[R-SER-01]`/`[R-SER-02]`), packed planes and pad bits (§14.3 `[R-SER-03]`), padding content (§14.5 `[R-SER-05]`), entry layout and the sentinel (§15.1–§15.3), segment boundaries (§15.4), slab/alignment (§16), and the pipeline (§17.1–§17.3). What I searched, and what refuted each candidate, is recorded under OBSERVATION below.

### CONTRADICTION — verifier obligation on padding content (verdict-divergent; outside §11–§18, found while checking §16's "bytes between structures")

- **§22.3 `[R-SEC-04]`, lines 2801–2804 (normative):** "Declared padding is covered by no checksum (§8.1): corruption confined to padding is invisible to a reader and caught only by **a verifier's zero check (`[R-CNT-03]`)**." Reinforced by Appendix H's verifier checklist, line 3218: "the checks readers are exempt from: … **declared-padding content (§5.2)**"; and by §5.1 line 474–475, which still lists "**declared padding**" as a thing lying between the front block and the trailer, though §5.2's coverage classes contain no such class.
- **§5.2 `[R-CNT-03]`, lines 515–519:** "Writers SHOULD zero the gaps they create — the run before an aligned tile or slab run, and the pre-trailer pad. … **no conformance requirement rides on slack content either way**." And `[R-CNT-21]`, lines 505–512: slack's "**content is unconstrained, and no conformance requirement applies to it**"; the verifier's only obligation is to *report the total*. §21.6's slack row and §16.1/§16.2/§14.5's closing note all state the §5.2 position.

Discriminator: a 192-byte file, directory at [16, 20), pre-trailer pad [20, 64) containing `AA` bytes instead of zeros, trailer at [128, 192). Verifier A (§22.3 + Appendix H) runs the zero check, fails it, and does not certify. Verifier B (§5.2 + §21.6) counts 44 slack bytes, reports the total, and certifies the file as conforming. Opposite certification verdicts on identical bytes, from two normative passages.

What I searched: `grep` for "declared padding", "zero check", "SHOULD zero"; §8.1's coverage map (no padding row); the whole of §21.2 and §21.6 for a padding-content register row (none exists — §21.6 lists the pre-trailer pad as slack with "no conformance requirement"). §22.3's clause cites `[R-CNT-03]`, which is the very requirement that denies it. This reads as residue of a retired "declared padding" coverage class that §5.2, §16, and §21 were updated for and §5.1, §22.3, and Appendix H were not.

### OBSERVATION

**1. §21's register omits at least five violations §18 and §7.1 name — against `[R-ERR-02]`'s normative completeness claim.** §21.1: "a violation this specification names and the register omits is a defect in this document." Missing rows:
- `[R-MTA-03]` (§18.2, line 1991): "A record whose inline_length is not 1 is a validity error at the record's containing scope." No F- or L-row.
- §18.2's BOM rule (line 2021): "a leading U+FEFF makes the document unreadable." R6 covers "not well-formed JSON, or top-level value is not an object" — a parser that ignores a BOM per RFC 8259 §8.1 finds a well-formed object, so R6 does not reach it.
- `[R-MTA-07]` (§18.4, line 2099): "A writer MUST NOT emit a standardized key outside the scopes its row lists." No row.
- `[R-MTA-09]` (§18.2, lines 2001–2004): metadata frame constraints. R3 covers only "fail to decode"; a metadata zstd frame that sets the content-checksum flag, or is followed by a second or skippable frame, decodes successfully and has no row.
- `[R-CNT-25]` (§7.1, line 692): a user-metadata record "whose extent_length is less than 5". F26 and L11 cover only slot (0, 0).

These do not diverge implementers — each rule is explicit and §21.1 makes the rule govern — but they undercut §21.8's coverage claim and the corpus obligation of `[R-VEC-03]`.

**2. §21.8's instance count does not reconcile.** Counting mechanically as §21.1 directs (semicolon-separated items per cell; a cell reading "—" is one instance) I get 69 (§21.2) + 81 (§21.3) + 43 (§21.4) + 20 (§21.5) = **213**, against the stated 214. The row count, 37 + 47 + 26 + 10 = 120, does reconcile (§21.3 skips L40, consistent with 47). Medium confidence — a single cell I read differently would close the gap — and outside my assigned range.

**3. §18.2's key rules do not state their depth.** "every key satisfying §4.6's name rules — non-empty, at most 255 bytes, free of U+0000 through U+001F" (line 2044) is unqualified, while §18.3 and §18.4 use "key" to mean a top-level member name. Discriminator: a layer document `{"app.cfg":{"":1}}`. Read at all depths → ignore-record; read at top level only → readable. I judge this resolvable: the duplicate-key bullet explicitly reaches "any one object", the UTF-8 bullet says "throughout", and §21.5's R5 says "A key of a decoded user-metadata document". A careful reader applies the rules at every depth. Reported because §18.3's narrower usage is the only friction I found in §18.

**4. §18.2's 255-byte key bound is measured on the decoded key, not the JSON source.** A 300-byte source key of `\uXXXX` escapes decoding to 50 bytes is conforming. Resolved by the preceding bullet: "Key identity is the *decoded* string, not its JSON source bytes." Worth an explicit half-sentence, since R9 says only "longer than 255 bytes".

**5. §18.2's "MAY use a wider representation" against the binary64 finiteness test.** A reader with decimal128 arithmetic could read `{"a":1e400}` as finite. The test is stated on the binary64 interpretation unconditionally, so a careful reader still declares the document unreadable; the wider representation is licensed only for values that pass. No structural consequence either way (`[R-MTA-02]`).

**6. `[R-COD-07]`'s LZ4 boundary leans entirely on the pinned revision.** The LZ4 Block Format Description states end-of-block restrictions (last sequence literals-only; minimum distance of the last match from block end) that real decoders enforce inconsistently. §17.2 says only "exactly one LZ4 block per the LZ4 Block Format Description … version 1.0; Appendix F pins the exact revision", and §21.4's T25 names only "lz4 match offset 0 or match reaching past produced output". A block violating the end-of-block restrictions that still decodes to exactly the decoded size, consuming exactly `length` bytes, satisfies `[R-COD-08]` under a permissive binding and is rejected under a strict one. I did not report this as byte-level because the document does the one thing available to it — pins the exact revision — and that revision states the restrictions normatively; the divergence is the external format's, not this text's. §17.2's zstd rules by contrast enumerate their frame-level boundary explicitly, which is the stronger treatment.

**7. `[R-COD-07]`'s "a layer whose tiles' decoded size"** is per-tile, not an aggregate over a planar layer's channels — resolved by §21.3's L45 ("per-tile decoded size"). Not a finding.

**8. §21.3's L2 instance list includes `V = P·C` without a layout qualifier**, but §14.1 defines V = P for planar layers, so P·C is not a spec-defined quantity there. A reader that checks the L2 list literally would reject a planar layer where P·C overflows though every defined quantity is in domain (e.g. d = 1, T₀ = E₀ = 2⁶², C = 2 bool channels: P = 2⁶², N = 1, entry_count = 2, planes ⌈P/8⌉ = 2⁵⁹, all in domain, P·C = 2⁶³). Resolved by §21.1 — "where a row and the rule it cites diverge, the rule governs" — and `[R-ENC-04]` binds only quantities the specification defines. Not byte-level.

**9. §15.2's Rationale mis-cites the scope for a zeroed index region.** It says a zeroed region is "loudly invalid (§15.3)", i.e. reject-tile; in fact the CRC chain (`[R-IDX-04]`) fires first with reject-layer. Non-normative text; both outcomes are rejections and `[R-TYP-09]` forbids fill either way.

**10. §15.1 does not state the index_encoding value set** that §10.3 and §19.3 cite it for; the set lives only in §7.4's table. Cross-reference only — the set is complete and unambiguous where it is stated.

**Positive checks (all passed).** I verified numerically: CRC-32C(`"123456789"`) = `0xE3069283` and CRC-32C(∅) = `0x00000000` (§4.5); the all-sentinel full-segment constant `[R-IDX-05]` = **`0xEECB3BB2`** over 65,536 × (`FF`×16 `00`×4) — correct, so a writer taking §15.4's licence produces bytes a computing reader accepts; Appendix A's trailer CRC = `0xE00938D2`. I hand-checked every worked example in my range: §11.2's grids, §11.4's ordinals (s = 10, in-tile 11,452, planar disk 74), §14.2's three interleaved/planar offset cases, §14.3's `55 01` / `55 FD` packed plane, §14.5's 32-byte edge tile, §15.4's segment arithmetic (segment 15 at region bytes [19,660,800, 20,000,000), CRC array [20,000,000, 20,000,064), 1.25 MiB full segment), §15.4's planar entry at [1,480, 1,500) and entries 96–127, §16.2's four-run example, and §17.3's byte-shuffle (`00 00 00 00 00 00 80 00 40 3F 40 40` — exact). All correct.

**My own worked layout**, checked against every rule that constrains it: planar layer, d = 2, dims y(E=3,T=2) and x(E=3,T=2), channels `v`:uint16 fill `0xABCD` and `m`:bool fill `0x01`, layout 2, linearization 1, codec 1, filter 1, A = S = A_slab = 0. G = (2,2), N = 4, P = 4, entry_count = C·N = 8; index extent_length = 8×20 + ⌈8/2¹⁶⌉×4 = **164** (`[R-CNT-17]`); layer-record inline_length = **98** bytes packed in §7.4 table order with no padding (`[R-CNT-18]`); channel-0 planes 8 bytes (P·Bᶜ), channel-1 planes 1 byte (⌈P/8⌉) — so codec 1 forces entry lengths 8 and 1 respectively (`[R-COD-04]`), a per-entry decoded size the reader derives as c = k div N. Edge tiles s = 1, 2 carry 2 padding positions each and s = 3 carries 3; in channel 1's plane those bits plus pad bits 4–7 all carry the fill bit 1 (`[R-SER-05]`, `[R-SER-03]`). Every rule in §11–§17 that touches this file resolved to one answer.

## Verdict
BYTE-LEVEL AMBIGUITIES: 0
CONFIDENCE: high

Note for the caller: the one CONTRADICTION above (§22.3/Appendix H vs. §5.2) is itself verdict-divergent — two verifiers reach opposite certification verdicts on the same bytes — so if contradictions are folded into the byte-level count, the number is 1. It lies outside my assigned §11–§18 range; I surfaced it because §16's slack language is what led me to it.
