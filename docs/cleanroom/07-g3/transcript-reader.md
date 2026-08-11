# Cleanroom round 7 — reader walk

**Access disclosure.** spec/tarn.md only

## Walk summary

I implemented the reader on paper end to end. §19.1's open: obtain transport-authoritative F ([R-CNT-10], never committed_file_length); fetch [F−64, F) and validate in §6.2's fixed order (magic → trailer CRC → version gate → flags, size, dir bounds, generation, file_id, reserved); fetch [dir_offset, dir_offset+dir_length) and verify the terminal CRC over dir_length−4 bytes before parsing; walk records under §7.2 framing, apply MU/multiplicity/extent-slot rules, and build the layer table with the duplicate-name test over raw name bytes. §19.2's tiers and §19.3's layer validation are self-consistent and require no I/O; §19.4's tile read (CRC array → segment → entry → payload → decode → extract) chains cleanly against §8.2 and never acts on an unverified integer.

Byte-exact cold remote open, exact-range reader, suffix-range transport: 0 layers = 2 requests, 64 + 4 = 68 bytes (Appendix A's file); 1 minimal layer (1-byte names, d=1, C=1 uint8) = record 24+73 = 97, dir_length 101, so 2 requests, 165 bytes; 600 such layers = dir_length 58,204, 2 requests, 58,268 bytes — and 1 request for a 64 KiB-suffix speculator, since 58,204+pad+64 < 65,536. At §21.9's own ~200 B/layer model 600 layers give dir_length ≈ 120,004 (2 requests, 120,068 bytes) and defeat speculation. No suffix-range support adds a size probe (3 requests). The front block never adds a request. One cold tile costs three ranges: whole segment-CRC array (4·⌈n/2¹⁶⌉ B), one segment (≤1.25 MiB), payload.

I traced Appendix A and verified computationally: CRC-32C("123456789") = 0xE3069283, CRC-32C(∅) = 0, the trailer CRC over its 60 bytes = 0xE00938D2 (`D2 38 09 E0`), and the full all-sentinel segment constant = 0xEECB3BB2. All correct. I also recounted §21: 39+50+26+10 = 125 conditions and 61+100+45+36 = 242 named instances, exactly matching §21.8.

Places I had to guess: (1) whether the open's record walk includes [R-CNT-25]/[R-MTA-03] framing checks (RD-01); (2) whether a suffix-speculating remote reader must verify the front block (RD-05); (3) what a region read returns when a layer-scope failure fires mid-request (RD-06); (4) whether an oversized user-metadata document may cost the whole file (RD-07); (5) whether a layer record too truncated to yield a name participates in the open's duplicate-name namespace — I excluded it and rejected only that layer; (6) well-formedness of a region request's intervals (empty/inverted) is undefined — I treated it as caller-API, returning no samples. Minor: §6.1 places a MUST on a "content sniffer", which is not one of §2.3's five conformance classes.

## Findings (8)

### RD-01 — AMBIGUITY  · reporter flags BYTE-LEVEL

**Location.** §19.1 step 4 and §19.3; §19.2's tier bullets; §21.2 rows F24/F25/F26; §21.3 rows L5/L11/L12/L13; [R-RDR-01], [R-RDR-03], [R-CNF-04], [R-CNT-25], [R-MTA-03]

§19 declares itself the consolidation of the reader's normative path, but its per-tier enumerations omit reader-assigned register rows due at those tiers — notably the user-metadata framing checks ([R-CNT-25]'s (0,0)/extent_length<5 and [R-MTA-03]'s inline_length=1), which the register places at open with outcome reject-file, and [R-ENC-11]'s UTF-8 check on dimension/channel names at layer access. It is unclear whether §19's lists are exhaustive statements of each tier's obligations or illustrative.

> This section consolidates the reader's normative path: the open algorithm, the validation-timing rule, layer access, and the tile-read algorithm.

> 4. **Record walk.** Parse the record sequence under §7.2's framing (`[R-CNT-12]`), applying the MUST_UNDERSTAND gate for unknown top-level types (`[R-CNT-15]`), the per-type multiplicity rules (`[R-CNT-14]`), and the extent-slot validity rules for non-layer top-level records (`[R-CNT-13]`) — all decidable from the resident bytes and F — and build the layer table

> - **at open:** the front signature block, for a reader holding it (`[R-CNT-04]`), the trailer, the directory region and its record walk, and the layer-name namespace (§19.1's steps);

> | F24 | A top-level user-metadata record (type 0x0002) carries extent slot (0, 0), placing its document inline | — | reader | open | `[R-CNT-25]` |

> The **extent slot** (extent_offset, extent_length): (0, 0) means no extent.

> A reader MUST detect the violations enumerated in the error register (§21) and apply the outcome class this specification assigns to each

**Permitted readings.**

1. §19.1's step-4 list and §19.3's list are the complete open- and layer-access-tier obligations; the register's Detected column merely names the tier at which a reader that performs a check would perform it, so a reader that never relies on a user-metadata record never detects F24/F25/F26 and serves the file's layers normally.
2. The register plus [R-CNF-04] governs: a reader MUST detect F24/F25/F26 at open and reject the whole file, and MUST detect L5/L11/L12/L13 at layer access; §19.1 and §19.3 are incomplete restatements.

**Picked.** The second: [R-CNF-04] obliges readers to detect register violations and §21.1 calls the Detector/Detected columns the actor obliged and the point due, so a reader must reject a file whose top-level user-metadata record carries extent (0,0). §19.1 and §19.3 are then under-inclusive relative to what they claim to consolidate.

**Rationale.** The two readings differ on whether a reader that does not consume user metadata must nonetheless refuse an entire file. §19.1's enumerated checks are all satisfied by such a file — (0,0) is expressly legal under [R-CNT-13], the only extent-slot rule §19.1 cites — so an implementer building from §19 alone opens and serves it, while an implementer building from §21.2 rejects it at file scope.

**Byte-level?** yes — Concrete file: front block, one layer record with one stored tile, and one top-level type-0x0002 record with extent slot (0,0), inline_length 1, encoding 1; trailer and all CRCs correct. Reader A (register + [R-CNF-04]) MUST reject-file and serve nothing. Reader B (§19.1's enumerated open) validates every check §19 names, opens, and returns the layer's decoded samples. The same byte sequence is must-reject under one reading and servable under the other.

### RD-07 — AMBIGUITY  · reporter flags BYTE-LEVEL

**Location.** §18.2 [R-MTA-09]; §21.9 [R-ERR-04]; §2.3 [R-CNF-03]; §17.2 [R-COD-06] (the resolved analogue)

For a conforming file whose user-metadata document exceeds the reader's decode bound, [R-MTA-09] assigns the outcome ignore-record, while [R-ERR-04] permits a reader to decline any file exceeding a §21.9 guarantee 'at the whole file' and lists no record-level scope. It is undecided whether a reader may refuse a conforming file over an oversized metadata document.

> a reader instead decodes with a bound of its own choosing, no smaller than §21.9's user-metadata guarantee, and a document exceeding that bound is ignore-record like any other it cannot read.

> A file exceeding any of these remains conforming, and a reader MAY decline it — at the whole file, or at the narrowest scope whose declarations exceed what it can serve, a layer or a tile.

> Writers SHOULD keep the declared window within §21.9's 8 MiB `Window_Size` guarantee even for a larger tile; a wider window is conforming and merely permits a conforming reader to decline the tile or the layer on resource grounds (`[R-ERR-04]`).

> A reader MUST accept every conforming file of a format major version it implements, carrying no record of a type it does not implement with MUST_UNDERSTAND = 1, and none of whose values exceeds the minimum guarantees of §21's limits table

**Permitted readings.**

1. [R-MTA-09] is the specific rule and fixes the outcome: ignore-record. The reader ignores the record, reads everything else, and reports the loss; refusing the file is not permitted, since the file is conforming and its only out-of-guarantee quantity has an assigned outcome.
2. [R-ERR-04] governs all §21.9 quantities uniformly. Because a document is neither a layer nor a tile, the only scope available is the whole file, so a reader MAY decline the entire conforming file, reporting a resource limit; §2.3's acceptance obligation is lifted for any file whose values exceed the guarantees.
3. A hybrid: the reader must ignore-record for the document itself but MAY additionally decline the file, so both behaviors are conforming and the divergence is licensed rather than defective.

**Picked.** The first. [R-MTA-09] names the exact condition and assigns an outcome class, and §2.4 makes outcome classes the blast radius of a condition; [R-ERR-04]'s scope list ('a layer or a tile') was drafted for declaration-derived magnitudes, which a document has none of.

**Rationale.** §17.2 explicitly resolves the identical tension for the zstd window guarantee by naming which scopes a reader may decline; §18.2 does not, and its assigned outcome (ignore-record) points the opposite way from [R-ERR-04]'s whole-file option. Nothing in the document reconciles them.

**Byte-level?** yes — Concrete file: a fully conforming file with two readable layers and one top-level user-metadata record whose encoding-1 document is 20 MiB (extent 20 MiB + 4). A reader at the minimum permitted bound of 16 MiB. Under reading 1 it MUST accept the file and return both layers' samples, ignoring the record. Under reading 2 it MAY refuse the file entirely as a resource limit. This is a disagreement about whether a *conforming* byte sequence must be accepted — the one class where [R-CNF-12]'s licence to reject nonconforming files does not paper over the difference.

### RD-03 — OBSERVATION

**Location.** §18.4 [R-MTA-07]; §21.1 (completeness clause); §21.5; §21.6's closing paragraph; §21.8 [R-ERR-02]

[R-MTA-07] names a detectable, verifier-assigned violation — a standardized `tarn.` key emitted outside the scopes §18.4's table lists — and expressly says the file is nonconforming and a verifier detects it, but no row of §21.2–§21.5 registers it, and §21.6 does not list it as a non-violation either. §21.1 declares the register's completeness normative, which makes the omission a defect in this document.

> A file carrying a standardized key outside its listed scope is nonconforming, and a verifier detects it (`[R-CNF-11]`); no reader's behavior turns on the violation, since a reader ignores the key either way. `[R-MTA-07]`

> Its **completeness is normative** — a *detectable* violation this specification names and the register omits is a defect in this document, detectability being the gate `[R-CNF-07]` already applies and §21.7 the inventory of what fails it

> Two conditions that once sat in this table are violations and are registered above: a user-metadata document whose object members are unsorted (`[R-MTA-05]`), and a registered record type whose stored MU or PE bit differs from §7.3's registry (`[R-CNT-22]`). Both make the file nonconforming while leaving every reader behavior unchanged — readers process the document and apply the type's fixed semantics — so both carry detector *verifier*

**Rationale.** The omitted condition is structurally identical to F30/L49 and F31/L50 — verifier-detected, reader-behavior-unchanged, file nonconforming — and the specification expressly moved two such conditions out of §21.6 and into the register for exactly that reason. A third of the same class remains unregistered, so §21.8's 125 conditions / 242 instances and [R-ERR-02]'s corpus obligation carry no vector for it. A related, smaller uncertainty rides along: §18.4's Value column ('a reader MUST ignore ... [a key] whose value does not match the shape its row gives') attaches no writer MUST, so it is unclear whether a wrong-shaped standardized key is a violation at all. Deciding this required auditing every MUST-level obligation in §§4–24 against 125 register rows, which is why it is filed as an observation rather than an ambiguity.

**Byte-level?** no — No implementation behavior turns on the omission. [R-MTA-07] itself already fixes both sides: a reader ignores the key either way, and a verifier must report the file nonconforming on the strength of the rule, since §21.1 makes the rule govern where a row and its rule diverge — and here there is no row at all to diverge from. No byte sequence changes classification; only the corpus loses a vector.

### RD-02 — AMBIGUITY

**Location.** §2.3 [R-CNF-04]; §6.2 [R-CNT-05]; §19.2 [R-RDR-02]; §21.1; §14.2 [R-SER-08]

[R-CNF-04] states flatly that a reader MUST detect the violations enumerated in the error register and apply each assigned outcome. Roughly twenty register rows carry Detector = verifier, and three other passages say those impose no reader obligation — including §6.2, which says in terms that readers do not check the condition F9 registers.

> A reader MUST detect the violations enumerated in the error register (§21) and apply the outcome class this specification assigns to each; a reader MUST NOT heuristically repair a violating structure or infer values this specification does not define. `[R-CNF-04]`

> A verifier MUST treat a structure in that gap as a validity error at file scope, and counts the rest as slack; writers zero it by the advice of `[R-CNT-03]` (readers check neither, their check being the dir-bounds rule of `[R-CNT-06]`). `[R-CNT-05]`

> A reader MUST detect each violation whose detection this specification obliges readers to make — a violation whose assigned detector is the verifier (§2.4, `[R-CNF-12]`) imposes no reader obligation

> For a row whose Detector is *verifier*, the outcome names the scope at which the damage is recorded, not an obligation on any reader: the governing rule states what a reader does, and for several such rows it obliges the reader to serve the structure unchanged (`[R-SER-08]`, `[R-CNT-22]`).

> A reader is not obligated to screen decoded content, and a reader that does not detect the violation is not thereby nonconforming

**Permitted readings.**

1. [R-CNF-04] is literal: a conforming reader must detect every register row, verifier rows included, so it must detect a structure in the pre-trailer pad (F9), extent overlap (F36/L19), alignment and slab invariants (L41–L43), padding-content and bool-byte violations (T2/T4/T5), and reject at the stated scope.
2. [R-CNF-04] delegates to the register's own Detector column, obliging a reader only for rows whose Detector is *reader*; verifier rows record the scope at which damage is attributed and bind only verifiers.

**Picked.** The second. §19.2, §21.1 and §6.2 all say so explicitly, and [R-SER-08] would otherwise be self-contradictory — it tells a reader that does not screen decoded content that it is nonetheless conforming, and fixes what such a reader returns for a byte the literal reading would oblige it to reject.

**Rationale.** The requirement most implementers will read first — the conforming-reader bullet in §2.3 — states an obligation three later passages contradict. The resolution is unambiguous once all four are read, but [R-CNF-04]'s own text carries no qualifier, and it is cited from the register rows themselves (L35).

**Byte-level?** no — Every file exhibiting a verifier-detected condition is nonconforming, and [R-CNF-12] already permits any reader to reject a nonconforming file 'upon detecting any violation, including violations whose assigned detector is the verifier'. So both readings leave the same set of files rejectable and the same set servable; what differs is only whether a non-detecting reader is itself a conforming reader. No byte sequence changes its must-accept/must-reject status. The one place returned bytes could differ — a nonconforming interleaved bool byte — is already covered by [R-SER-08]'s conditional ('A reader that neither detects the violation nor rejects the tile ... MUST report 0x00 as false and every other byte as true'), which mandates nothing of a reader that does reject.

### RD-06 — AMBIGUITY

**Location.** §19.4 step 8 [R-RDR-04]; §19.2 [R-RDR-02]; §2.4's reject-layer row; §15.4 [R-IDX-04]

§19.4 step 8 fixes what a multi-entry request returns when individual entries are rejected at tile scope, but not when step 3 raises a layer-scope failure part-way through a region. §2.4 makes reject-layer prospective — it 'does not retroactively invalidate content already returned' — which leaves the answer turning on whether a reader has handed earlier tiles to its caller, an implementation-technique distinction §2.4's own note says is not a conformance question.

> Where the request covered several entries — a region, or a planar layer's several channels — each rejected entry's failure is bounded to the positions that entry carries (§2.4): the reader MAY return the validating entries' values together with a per-entry report of the failed ones, or fail the request as a whole, but MUST NOT stand fill in for a rejected tile's positions (`[R-CNF-09]`).

> Failure at any point takes the violated rule's own outcome and scope — in particular, index-chain failures take layer scope (`[R-IDX-04]`) although their detection point is tile use.

> The outcome is prospective: it bars further service from the layer, and does not retroactively invalidate content already returned under §19.2's validation timing (`[R-RDR-02]`).

> any mismatch or cross-check failure (`[R-CNT-17]`) is reject-layer

**Permitted readings.**

1. The whole request fails: a layer-scope rejection is not an entry-bounded failure, so nothing further may be served from the layer and any samples not yet delivered are 'further service' the reader must withhold.
2. The request returns the tiles whose segments verified before the failing one, because reject-layer is prospective and those samples were computed under a validation that passed; only tiles after the detection point are barred.
3. The reader may choose either, by analogy to step 8's explicit choice for tile-scope failures ('MAY return the validating entries' values ... or fail the request as a whole'), extended to layer scope.

**Picked.** The first. §2.4 bars further service from a rejected layer, and 'already returned' most defensibly means delivered to the caller before detection — which, within a single request that detects before delivering anything, is nothing. A reader that streams tile by tile may keep what it already emitted.

**Rationale.** A ten-tile region read whose fifth tile's segment CRC fails is the ordinary case, and the specification's own worked path (§19.4) never reaches it: step 8 speaks only of 'each rejected entry', which is tile-scope language. Two readers disagree about whether the caller receives four tiles of valid samples or an error.

**Byte-level?** no — A layer-scope failure at step 3 means a segment CRC or crc_of_crc_array mismatch, which only a corrupt — hence nonconforming — file exhibits. For such a file [R-CNF-12] already lets any reader reject everything, so neither reading enlarges or shrinks the set of byte sequences a reader must accept or reject; the divergence is confined to how much of a doomed request a reader may fulfil. No conforming file can exercise the condition, so no two implementations can disagree about the bytes of a conforming file.

### RD-05 — AMBIGUITY

**Location.** §19.1 step 1 [R-RDR-01]; §6.1 [R-CNT-04]; §21.2 rows F2 and F8; Appendix A's closing paragraph

§19.1 step 1 conditions the front-block obligation on holding bytes [0,16) 'once this step completes' — that is, at the moment F is obtained, before any fetch — and releases a reader that 'would have to fetch them'. §6.1 instead makes the test residency across the whole open and names a speculative suffix window that reached offset 0 as a resident case. A remote reader that speculates a 64 KiB suffix on a small file is released by the first and bound by the second.

> A reader holding bytes [0, 16) once this step completes MUST verify the front signature block by byte equality before other processing (mismatch: reject-file); one that would have to fetch them MAY defer or omit the check (`[R-CNT-04]`).

> A reader whose open leaves bytes [0, 16) **resident** — a local file, a memory mapping, a speculative suffix window that reached offset 0, or any transport already holding them — and a content sniffer MUST verify the full block by byte equality before other processing, and MUST treat any mismatch as reject-file.

> A reader that would have to issue a further range request to obtain those bytes MAY defer or omit the check

> A local reader additionally verifies bytes [0, 16) by equality first, which `[R-CNT-04]` requires of any reader holding them — as a remote reader does too whenever it speculates a suffix window, since this file is 128 bytes and any such window reaches offset 0.

**Permitted readings.**

1. The obligation is evaluated at the end of §19.1 step 1: a remote reader holds nothing then and 'would have to fetch' the front block, so it may omit the check outright, whatever its later fetches deliver.
2. The obligation is evaluated over the whole open, per §6.1: any reader whose open leaves [0,16) resident — including one whose speculative suffix window reached offset 0 — must verify the block by equality before other processing, and only a reader that would need a *further* range request may defer or omit.

**Picked.** The second. §6.1 names the speculative-suffix case explicitly and says the test 'is residency, not transport', and Appendix A applies it that way to the 128-byte file. §19.1's 'once this step completes' is a narrower restatement of a rule it cites rather than an independent licence.

**Rationale.** The two passages evaluate the same counterfactual at different times, and the reader they disagree about — a suffix speculator on a file small enough that the window reaches offset 0 — is the exact case §6.4 recommends and Appendix A walks. An implementer working from §19.1 alone omits a check §6.1 makes mandatory.

**Byte-level?** no — The candidate divergence is a file whose bytes [8,16) are nonzero (F8's reserved-bytes instance) with everything else valid: reading 1 lets a speculating reader serve it, reading 2 obliges reject-file. But reading 1 is not a permitted reading of the document as a whole — §6.1 names 'a speculative suffix window that reached offset 0' among the resident cases, and such a reader issues no further range request, so the release clause cannot reach it. With only one permitted reading, no two conforming implementations can disagree about these bytes; the defect is that §19.1, which claims to consolidate the reader's path, states the test in a form that inverts the answer when read alone.

### RD-04 — CONTRADICTION

**Location.** §2.3 (conforming-reader bullet, [R-CNF-03]); §21.6's closing paragraph; §21.9 [R-ERR-04]

§2.3 asserts that §21.6's closing paragraph names the two exceptions to a reader's acceptance obligation, but the two cases §21.6 actually names are not the two §2.3 states, and neither passage counts the resource-limit refusal [R-ERR-04] permits.

> A reader MUST accept every conforming file of a format major version it implements, carrying no record of a type it does not implement with MUST_UNDERSTAND = 1, and none of whose values exceeds the minimum guarantees of §21's limits table (§21.6's closing paragraph names those two exceptions), and MUST handle every codec and filter that §17 designates as core

> Two distinct cases are **conforming files a reader nevertheless refuses**. The first is **version_major naming a major this reader does not implement**: the reader rejects the file (`[R-CNT-07]`), but the file can be perfectly conforming under that major. The second is an **experimental-range record type carrying MU = 1** (§10.2, §10.3)

> A file exceeding any of these remains conforming, and a reader MAY decline it — at the whole file, or at the narrowest scope whose declarations exceed what it can serve, a layer or a tile.

**Rationale.** §2.3's two carve-outs are (a) a record of an unimplemented type with MU = 1 and (b) values exceeding §21.9's minimum guarantees, with the major handled by the leading clause. §21.6's two cases are (a) an unimplemented major and (b) an experimental-range type with MU = 1 — a strict subset of §2.3's first carve-out — and say nothing about the limits table. So the cross-reference is false on its face under either alignment, and the true count of ways a conforming file may be refused is three, not two: unimplemented major, unimplemented MU = 1 type, and a §21.9 quantity a reader declines on resource grounds.

**Byte-level?** no — Each of the three refusal grounds is independently and unambiguously established elsewhere — the major by [R-CNT-07], the MU = 1 unknown type by [R-CNT-15], the resource decline by [R-ERR-04] and [R-CNF-10] — so no reader's accept/reject behavior turns on repairing the miscount. The defect is a false statement about the document's own content, not an underdetermined rule; a reader relying on §2.3's parenthetical to conclude it MUST accept an over-guarantee file is corrected by [R-ERR-04] two sections later. (RD-07 is where an over-guarantee file does produce a genuine byte-level divergence, and it turns on a different pair of rules.)

### RD-08 — OBSERVATION

**Location.** §21.7 [R-ERR-01]; §21.1 (the clause designating §21.7); §20.4 [R-WRT-05]; §20.5 [R-WRT-06], [R-WRT-07]

§21.1 designates §21.7 as 'the inventory' of obligations that fail the detectability gate and therefore carry no register row, but §21.7's second paragraph names only [R-LIF-01], [R-LIF-03], [R-GEO-06], [R-SER-01] and [R-CNT-13]'s no-embedded-offsets rule, while several other MUST-level obligations likewise have no witness in a single file.

> Its **completeness is normative** ... detectability being the gate `[R-CNF-07]` already applies and §21.7 the inventory of what fails it

> A second set of obligations is omitted from the register because a single file exhibits no witness of their violation. Committed-prefix immutability and the generation sequence (`[R-LIF-01]`, `[R-LIF-03]`) are properties of a file's history, which §9.7 does not reconstruct; the ordinal mappings of `[R-GEO-06]` and `[R-SER-01]` are satisfied by a structurally valid tile whatever values it carries; and `[R-CNT-13]`'s prohibition on an MU = 0 record encoding file offsets in its own payload is opaque by construction. `[R-ERR-01]`

> In the new complete directory, an updater MUST re-emit byte-identically — header, inline payload, and extent slot — every record it retains and does not logically modify

> It MUST mint a fresh file_id for the output — a new draw under §9.3's randomness advice, not merely a value compared against the input's

**Rationale.** [R-WRT-05]'s byte-identical re-emission, [R-WRT-06]'s fresh file_id, [R-WRT-07]'s reference-array equality between input and output, and [R-LIF-02]'s durability barriers are all MUST-level and all unwitnessed by any single file; whether each is already absorbed by §21.7's 'properties of a file's history' clause, or is a further omission from an inventory §21.1 calls complete, is decidable — but only by auditing every MUST in §§4–24 against §21's 125 rows and §21.7's five named requirements, which is why this is filed as an observation. Deciding it either confirms the inventory or produces a list of clauses to add. Note that [R-SLB-04] shows the drafting pattern for the answer: §16.2's note explicitly says it 'carries no register row of its own' and names the rows that catch it instead.

**Byte-level?** no — Every requirement at issue binds a writer, updater or compactor across two states of a file, and by construction no single byte sequence exhibits or fails to exhibit any of them. A reader's and a verifier's treatment of any given file is identical under every resolution: the file is walked, checksummed, and served or refused on the strength of the rows that do exist. Nothing a conforming implementation may emit, must accept, or must reject changes.
