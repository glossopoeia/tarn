## 1. Checks a conforming verifier owes that a reader does not

`[R-CNF-11]` defines the class as "checks every file-level requirement — including those ordinary readers are exempted from." The exemptions are enumerable:

| # | Verifier-only check | Rule | Register row | Decidable from the bytes alone? |
|---|---|---|---|---|
| 1 | Live-state coverage partition | `[R-CNT-02]`, `[R-LIF-08]` | F8/F9 | Yes — one walk from the live trailer. Boundary wording issue, §5.2 vs §9.7 (Obs 1) |
| 2 | Slack total (MUST report) | `[R-CNT-21]`, `[R-LIF-08]` | §21.6 row | Yes, same caveat |
| 3 | No structure in the directory→trailer gap | `[R-CNT-05]` | F10/F11 | Yes (falls out of 1). The paired "fewer than 64 bytes" clause has no outcome and no row (Obs 4) |
| 4 | Intra-layer extent overlap → reject-layer | `[R-CNT-13]`, `[R-IDX-03]` | L17 | Yes |
| 5 | Cross-scope extent overlap → reject-file | `[R-CNT-13]`, `[R-IDX-03]` | F34/F35 | Yes |
| 6 | Reserved record flag bits 2–15 nonzero | `[R-CNT-12]` | F29, L48 | Yes |
| 7 | Record MU = 1 with PE = 0 | `[R-CNT-12]` | F28, L47 | Yes; overlaps `[R-CNT-22]` for registered types (Obs 3) |
| 8 | Reserved-range record type emitted | `[R-CNT-15]` | **none** | Yes — but the register omits it (Obs 2) |
| 9 | Registered type's stored MU/PE ≠ §7.3 (SHOULD report) | `[R-CNT-22]` | §21.6 row | Yes |
| 10 | Per-tile alignment: offset mod A = 0 | `[R-SLB-01]` | L39 | Yes |
| 11 | Slab run contiguity/packing | `[R-SLB-03]` | L41 | Yes |
| 12 | Slab run first-tile A_slab alignment | `[R-SLB-03]` | L42 | Yes |
| 13 | Stale slab declaration carried forward | `[R-SLB-04]` | L43 | **No as phrased** — names the prior commit, which §9.7 does not enumerate. Only manifests as 11/12 |
| 14 | Padding positions carry fill | `[R-SER-05]` | T4 | Yes, but requires decoding every stored edge tile |
| 15 | Pad bits carry the fill bit | `[R-SER-05]`, `[R-SER-03]` | T5 | Yes, with decode |
| 16 | Interleaved bool bytes ∈ {0x00, 0x01} | `[R-SER-08]` | T2 | Yes, with decode |
| 17 | Filter applied at a wrong stride | `[R-COD-10]` | T26 | Only where 14–16 catch it; otherwise undetectable *by construction* (§21.7) |
| 18 | Unsorted user-metadata members (MUST report) | `[R-MTA-05]` | §21.6 row | Yes |
| 19 | Document decode; MUST NOT certify if it cannot | `[R-MTA-09]`, `[R-COD-11]` | — | Capability, not bytes (see Obs 5) |
| 20 | Front block by equality even on a remote transport | `[R-CNT-04]` + `[R-CNF-11]` | F2 (partly) | Yes |
| 21 | Every reader-tier check applied to *every* layer, record, extent and stored tile — not only those a request touches | `[R-CNF-11]`, `[R-RDR-02]` | all reader rows | Yes; this is the largest real cost (full decode of every tile, per `[R-COD-08]`/`[R-SER-07]`) |

## 2. Figures a verifier reports

| Figure | How computed | Must two verifiers agree? |
|---|---|---|
| **Slack total** (`[R-CNT-21]`) | F − 16 (front block) − \|directory\| − 64 (trailer) − Σ live structure sizes (record extents, tile-index regions, non-sentinel stored extents) | Yes, once §5.2's live-state definition is preferred to §9.7's literal walk (Obs 1). Deterministic otherwise — every term is a declared length |
| **Certification verdict** | "violation-free at every scope" (§2.4, `[R-CNF-12]`) | Yes, except for the three conditions the document calls nonconforming but files outside the register (Obs 2, Contradiction 2) |
| **Outcome class + scope + row per damaged structure** (the recording model of `[R-VEC-02]`) | §21 row, overridden by its governing rule where they diverge (§21.1) | Only for verifiers that apply §21.1's precedence sentence; L47 vs the §21.6 flag-mismatch row is where it bites (Obs 3) |
| **Register self-counts** — "37/47/26 conditions", "120 conditions over 214 named instances" (§21.2–§21.5, `[R-ERR-02]`) | §21.1 declares the instance count mechanical (semicolon split; "—" = 1) | My mechanical count is **213**, not 214 (Obs 6) |

## 3. Verifier obligations stated in more than one section

| Obligation | Statements | Agree? |
|---|---|---|
| Coverage + slack | §5.2 `[R-CNT-21]` + Note; §9.7 `[R-LIF-08]`; F8/F9; §22.3 `[R-SEC-03]`; App. H | Substance yes; §9.7's walk omits the front block and trailer from what it "reaches" (Obs 1) |
| Generation enumeration | §9.6 `[R-LIF-06]` ("the same probe continued to offset 0") vs §9.7 `[R-LIF-08]` ("walks the live state only") | **No** — Contradiction 1 |
| Extent overlap | §7.2 `[R-CNT-13]`; §15.3 `[R-IDX-03]` rows; L17/F34/F35; App. H | Yes, including the reject-layer / reject-file split |
| Alignment & slab | §16.1, §16.2; §15.3's "*verifier*: reject-layer" row; L39/L41/L42/L43; App. H | Yes |
| Decoded content | §14.2 `[R-SER-08]`; §14.5 `[R-SER-05]`; §17.3 `[R-COD-10]`; §17.4 `[R-COD-11]`; T2/T4/T5/T26; App. H | Yes |
| Record flags | §7.2 `[R-CNT-12]` (MUST, scope outcome) vs §7.3 `[R-CNT-22]` (SHOULD report) vs §21.6's row | Reconcilable but not stated as such (Obs 3) |
| Reserved-range values | §7.2 `[R-CNT-15]` vs §10.3 `[R-EXT-03]` vs R10/§21.6 | Rule and register diverge; §21.1 resolves (Obs 2) |
| Metadata | §7.1 `[R-CNT-25]`; §18.2 `[R-MTA-09]`, `[R-MTA-05]`; §21.5; §21.6 | Obs 5, Contradiction 2 |
| App. H's verifier checklist | §2.3, §5.2, §7.2, §16, §14 | Omits `[R-CNT-12]`, `[R-CNT-15]`, `[R-MTA-09]`, `[R-MTA-05]`; non-normative, so an incompleteness not a conflict |

## 4. Worked trace — two commits, tile superseded, MU = 0/PE = 0 record dropped

Layer `a`: interleaved, d = 1 (`x`, E = 4, T = 2 → G = 2, N = 2), C = 1 (`v`, uint8, fill 0x00), codec 1, filter 1, A = S = A_slab = 0, linearization 1, index_encoding 1, entry_count 2. Decoded size P·Q = 2 (`[R-SER-02]`), so each entry length is 2 (`[R-COD-04]`); G·T = E, so no padding positions — T4/T5 vacuous. Layer-record inline payload = 73 bytes → record 97 bytes; index region = 2×20 + 1×4 = 44 (`[R-CNT-17]`). Gen 1 also carries a top-level record of type 0x8001 (experimental, conforming per `[R-CNT-15]`), flags 0x0000, inline 0, extent (64, 8). CRC arithmetic is routine throughout.

**Generation 1**, F₁ = 320: front [0,16); tile0 [16,18); tile1 [18,20); index [20,64); ancillary extent [64,72); directory [72,197) = 97 + 24 + 4; pad [197,256) = 59 slack; trailer [256,320).

**Generation 2** — supersede tile 1, drop the ancillary. Writing begins at exactly F₁ (`[R-LIF-02]` step 1); the whole index region is re-emitted with entry 0 byte-identical (`[R-WRT-04]` step 4); the layer record is *modified* output (extent slot and crc_of_crc_array change), so `[R-WRT-05]`'s byte-identity does not bind it. F₂ = 576.

| Range | Bytes | Class at gen 2 |
|---|---|---|
| [0,16) | 16 | front signature block — live (§5.2) |
| [16,18) | 2 | tile 0 payload, **appended by gen 1, still live** (`[R-CNT-13]`) |
| [18,20) | 2 | superseded tile 1 → slack |
| [20,64) | 44 | superseded index region → slack |
| [64,72) | 8 | dropped record's extent → slack (`[R-WRT-08]`) |
| [72,197) | 125 | gen-1 directory → slack |
| [197,256) | 59 | gen-1 pre-trailer pad → slack |
| [256,320) | 64 | gen-1 trailer → slack |
| [320,322) | 2 | new tile 1 payload — live |
| [322,366) | 44 | new index region — live |
| [366,467) | 101 | live directory (layer record only) |
| [467,512) | 45 | pre-trailer pad → slack (gap < 64, `[R-CNT-05]`) |
| [512,576) | 64 | live trailer, generation 2 |

Live = 229 bytes; **slack total = 347** (60% of the file) — the figure `[R-CNT-21]` obliges. Note what the verifier *cannot* see: nothing in gen 2 records that a record was dropped, and its extent is indistinguishable from any other slack — which is exactly §5.2's rationale.

## 5. What a verifier cannot establish

- **Content correctness** — wrong samples, an undisclosed zstd dictionary (`[R-COD-06]`), a mis-strided filter with no structural constraint (`[R-COD-10]`): stated at `[R-ERR-01]`.
- **Authenticity** — every checksum is recomputable by whoever modified the bytes (`[R-SEC-07]`, §4.5).
- **Anything about earlier generations.** §9.7 walks the live state only and §5.2 makes everything else unconstrained slack, so these are unfalsifiable from one file: generation increments by exactly 1 (`[R-LIF-03]`), committed-prefix immutability (`[R-LIF-01]`), byte-identical re-emission (`[R-WRT-05]`), the appender's version_minor floor (`[R-CNT-26]`), the slab-staleness condition as phrased (`[R-SLB-04]`), and whether a MU = 0/PE = 0 drop was licensed (`[R-WRT-08]`).
- **Writer conduct** (`[R-CNF-02]`): experimental values in released data (§10.3), registry version targeted (§18.3), file_id randomness (§9.3), commit barriers (`[R-LIF-02]`), a compactor's fresh draw (`[R-WRT-06]`).
- **Slack content** — no checksum covers it (§8.1); corruption inside it is invisible to reader and verifier alike (`[R-SEC-04]`).
- **Rollback** — truncation to an earlier commit boundary is in-format indistinguishable (`[R-LIF-06]`).
- **Field widths** where total size is preserved (`[R-ENC-06]`, rows F5/L3) — width is not a property of bytes (Obs 7).

## Findings

### BYTE-LEVEL AMBIGUITY
None.

### CONTRADICTION
**C1 — generation enumeration.** §9.6 `[R-LIF-06]`: "Generation enumeration for coverage verification (§5.2) is the same probe continued to offset 0." §9.7 `[R-LIF-08]`: "A verifier checking `[R-CNT-02]`'s partition walks the live state only," with the Note "Nothing here enumerates prior commits." Both are normative and cannot both describe the verifier's coverage procedure. Consequence is procedural only — under §5.2 prior structures are slack either way, so the slack total and the verdict are unaffected — which is why I do not rank it byte-level.

**C2 — violations with no outcome class.** §2.4 `[R-CNF-07]`: "Every detectable violation named by this specification is assigned exactly one reader outcome." §21.6 is headed "Conditions that are **not** violations … defined behaviors, not errors," yet two of its rows state the opposite of their own heading: unsorted metadata members — "The file is nonconforming, but the document is readable" (`[R-MTA-05]`) — and a registered type's stored MU/PE mismatch — "The file is nonconforming, but readers apply the type's fixed semantics" (`[R-CNT-22]`). Both are detectable violations carrying none of the four outcomes, and neither appears in §21.2–§21.5, whose completeness §21.1 declares normative.

### OBSERVATION
1. **Slack's two definitions.** §5.2 puts the front signature block, live directory and live trailer *inside* the live committed state, so they are not slack; §9.7 says "Bytes the walk does not reach are slack" and its enumeration lists neither the front block nor the trailer. On Appendix A's 128-byte file this reads 44 vs 60 (or 124). Searched: §5.2's coverage sentence, §9.7, §21.6's slack row, App. B. Resolved by §5.1's example ("44 bytes of slack") plus §5.2's own list — but §5.1's example is non-normative (§2.1), so the resolution rests on §5.2 alone. §9.7 should name the front block and trailer.
2. **Reserved-range record type has no register row.** `[R-CNT-15]` gives the verifier a MUST ("a validity error at the record's governing scope") for a reserved-range type; §21.2/§21.5 carry only F36 (MU = 1, reader) and R10 (MU = 0, ignore-record, reader), and §21.6 plus App. H gloss "unknown MU = 0" as conforming without the reserved/experimental split. A verifier reading only the register certifies a file with a type-0x0003 MU = 0 record; one reading `[R-CNT-15]` rejects it. §21.1's precedence sentence resolves this — and §21.1 itself makes the omission "a defect in this document."
3. **Two verifier rules for one byte pattern.** A layer record with flags = 0x0001 is both L47 (`[R-CNT-12]`, verifier MUST, reject-layer) and the §21.6 `[R-CNT-22]` row (verifier SHOULD report, readers process the record). Reconcilable — MUST subsumes SHOULD — but the reported outcome class differs, which `[R-VEC-02]` requires a vector to record.
4. **`[R-CNT-05]`'s size clause is unenforced.** "the gap is slack, fewer than 64 bytes" sits under a writer MUST, but the only verifier obligation stated is "a structure in that gap," and no register row covers an oversized gap. §5.2 and §21.6 say slack carries no conformance requirement, so a 900-byte pre-trailer gap is best read as conforming waste (`[R-SLB-05]`).
5. **Conforming files no verifier can certify.** `[R-CNF-02]` makes §10.3's experimental prohibition conduct, so a user-metadata record declaring encoding ≥ 0x80 is conforming and ignore-record (`[R-EXT-03]`); `[R-MTA-09]` nevertheless says a verifier that cannot decode a document "MUST NOT certify the file." Coherent, but worth stating outright. Separately, `[R-COD-11]` cites "the rule of §9.7(d)" — §9.7 has no lettered clauses; the reference is dangling.
6. **Register bookkeeping.** F8/F9, F10/F11 and F34/F35 are verbatim duplicates; L40 is absent with no note (contrast §14.4's explicit retirement of `[R-SER-04]`). My mechanical instance count under §21.1's stated rule is 213, not §21.8's 214.
7. **F5/L3 are not predicates on bytes.** `[R-ENC-06]`'s "fields at any other width" is detectable only through the consequential gate failures of other rows (a u32 version_major with value 1 is byte-identical to a conforming trailer). Assigning them detector = reader at open, and requiring a vector per instance (`[R-ERR-02]`, `[R-VEC-03]`), asks the corpus for a file `[R-VEC-02]` says cannot be expressed.
8. **The MU = 0/PE = 0 drop licence is self-referential.** `[R-WRT-08]` permits an appender to drop such a record "only in a commit that modifies the scope the record attaches to," while the MU = 1 row defines file-scope modification as "adding, removing, or reordering top-level records" and excludes a commit that only changes a layer's tiles. The drop itself is a removal, so the condition either self-licenses (vacuous) or requires an independent file-scope change. No verifier can adjudicate it — §4's trace shows the dropped record leaves no live trace.

## Verdict
BYTE-LEVEL AMBIGUITIES: 0
CONFIDENCE: medium
