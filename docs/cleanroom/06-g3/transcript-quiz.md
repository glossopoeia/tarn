# Cleanroom round 6 — quiz answers

**Access statement.** I read `/Users/robertkleffner/Documents/GitHub/tarn/spec/tarn.md` and nothing else. The only other command I ran was a `python3` one-liner that re-read that same file to count the §21.2–§21.5 register rows and their Instances cells (result: 125 rows, 244 instances). No docs/, no conformance/, no registry.json, no git history, no web.

---

## Answers

### 1. Can a byte of the live committed state be claimed by no coverage class? — **No.**

Proof from the definitions. §5.2 `[R-CNT-02]` defines the live committed state *extensionally*: "the front signature block, and every structure reachable from the live trailer through the live directory's records, extent slots, and tile-index entries, together with the live directory and the live trailer." Every member of that union is already one of the enumerated classes — the front block; a stored-tile extent (reached through tile-index entries, §15.1 `[R-IDX-01]`); a record extent (§7.2 `[R-CNT-13]`, which for a layer record *is* the tile-index region, §7.4); the directory; the trailer. So membership in the state entails membership in a class.

The converse closure is §9.7 `[R-LIF-08]`: "Bytes the walk does not reach are slack." A byte outside every class is therefore outside the state, not an unclaimed byte inside it. §5.2's own Note states the conclusion: "'belongs to no class' describes nothing, and a register row for it would be a row no file could exhibit."

Consequence: the only testable half of `[R-CNT-02]` is the *exactly one* — disjointness — which is what §9.7 checks and what §21.2 F36 and §21.3 L19 register. There is no register row for an unclaimed byte, correctly.

### 2. Interleaved bool value byte 0x7F at a real sample position

- **Conforming? No.** `[R-SER-08]` (§14.2): "Writers MUST NOT emit any byte other than 0x00 or 0x01 as an interleaved bool value. Any other byte makes the file nonconforming."
- **A reader that returns the value reports `true`.** `[R-SER-08]`: "A reader that neither detects the violation nor rejects the tile, and returns the value, MUST report 0x00 as false and every other byte as true." A reader is *not* obliged to screen decoded content, and one that does not detect this is still conforming; one that *does* detect it may reject under `[R-CNF-12]` (§2.4). This is the one byte §14.2's Note and Appendix H call "the sole resolved byte."
- **A verifier treats it as a validity error at tile scope** → reject-tile, and MUST NOT certify the file (§2.4 `[R-CNF-08]`, `[R-CNF-12]`). Register row **T2** (§21.4): detector *verifier*, detected at *certification*, governing rule `[R-SER-08]`.
- Note the row's qualifier "real (non-padding)": at a padding position the governing rule would instead be `[R-SER-05]` (§14.5), row T4.

### 3. Remote open of Appendix A's 128-byte file, baseline strategy

**Two round trips** (§6.4 `[R-CNT-09]`, §19.1 `[R-RDR-01]`, confirmed by Appendix A's own walkthrough):

1. A **suffix range for the final 64 bytes** — bytes **[64, 128)**. Validated in §6.2's fixed order (magic, trailer CRC, version gate, then the remaining field gates: `[R-CNT-06]`, `[R-CNT-07]`, `[R-CNT-08]`).
2. **[dir_offset, dir_offset + dir_length) = [16, 20)** — the 4-byte empty directory, whose terminal CRC (`0x00000000`, the CRC-32C of zero bytes, §4.5) is verified before any other use (§7.1 `[R-CNT-11]`).

**File size:** F comes from the *same* first response — §6.4 `[R-CNT-09]`: "a suffix range, whose response also carries the transport-authoritative file size F (`[R-CNT-10]`), so that §19.1's first two steps cost one request between them." `[R-CNT-10]` requires it be transport-authoritative (complete length of a range response, a full-response content length, or a separate size probe) and forbids substituting the trailer's own committed_file_length for it.

No third request: a remote reader MAY defer or omit the front-signature-block equality check (§6.1 `[R-CNT-04]`, restated in §19.1 step 1), so bytes [0, 16) are never fetched. (On a transport without suffix-range support the reader SHOULD fall back to a size probe plus an absolute range, `[R-CNT-10]` — that is the fallback path, not the baseline.)

### 4. Register row: Instances cell "—", condition text naming three alternatives → **one instance**

§21.1 states the counting rule mechanically: "Instances within a cell are separated by semicolons, and a cell reading — is one instance; the count is therefore mechanical." The cell, not the condition prose, carries the count. §21.8 `[R-ERR-02]` then owes that row **one** vector ("a row naming instances has one vector per instance"), and §24 `[R-VEC-03]` inherits the same.

L42 (§21.3) is exactly this shape: "gap, overlap, or out-of-ordinal placement" in the condition, "—" in the cell → one instance. I verified the rule reproduces §21.8's published totals exactly: applying "— = 1, otherwise count semicolon-separated items" over §21.2–§21.5 yields **125 rows and 244 instances**, the numbers §21.8 states. That agreement is strong internal evidence the mechanical reading is the intended one. See AMBIGUITY-1 below for the reading I rejected.

### 5. Two layers A and B; a commit appends layer C, touching nothing else

Slack after the commit (§5.2 `[R-CNT-21]`, §20.3's shape (a) diagram, `[R-WRT-05]`):

- **The superseded directory region** of the prior generation (record sequence + its terminal CRC).
- **The superseded trailer** of the prior generation — it was live state under §5.2 ("together with the live directory and the live trailer") and stops being reachable the moment the new trailer commits.

Precisely: those two *become* slack. Two more categories are worth separating rather than merging into the answer:

- **The prior generation's pre-trailer pad** was *already* slack before this commit — §6.2 `[R-CNT-05]`: "Those bytes — the pre-trailer pad — are slack (§5.2)." It stays slack; it does not become slack.
- **The new commit's own pre-trailer pad** is slack from birth, same rule.

Nothing of A or B changes: §20.3 step 4 and `[R-WRT-05]` require A's and B's records be re-emitted byte-identically, extent slot included, so their tiles and tile-index regions remain live where they always were (§5.1's Example makes the same point). Any gap layer C's writer leaves around its own structures is additionally slack under `[R-SLB-05]`/§5.2, but nothing requires one.

### 6. Stale slab declaration carried forward across a commit that supersedes a stored tile

**Governing writer rule:** §16.2 `[R-SLB-04]` — the writer MUST re-establish the invariants for every affected run or clear the declaration; "carrying a stale declaration forward is a validity error at layer scope, detected as the invariant failures of `[R-SLB-03]` are: by a verifier."

**What the verifier detects:** not `[R-SLB-04]` directly — it has no register row of its own (§16.2's Note says so explicitly) — but `[R-SLB-03]`'s invariant failures, via §15.3's row "alignment or slab invariant violated (§16) → *verifier*: reject-layer":

- **L42** (§21.3, `[R-SLB-03]`): inside the affected run, a stored tile's offset ≠ the previous stored tile's offset plus that tile's length. This is the ordinary witness: a commit appends the superseding payload at the file's end (`[R-LIF-01]`, `[R-LIF-02]` step 1), while the run's other stored tiles keep their old offsets, so packing breaks.
- **L43** (§21.3, `[R-SLB-03]`): if the superseded tile was the run's first stored tile, its new offset need not satisfy offset mod A_slab = 0.

**Outcome:** reject-layer; detector *verifier*; detection point *certification*; the verifier MUST NOT certify the file (§2.4 `[R-CNF-12]`). Ordinary readers have no obligation here — `[R-SLB-03]`: "readers are not obligated to, and MAY instead detect contiguity arithmetically from any index segment." See AMBIGUITY-2 for the one configuration where I read this rule as producing no detectable witness.

### 7. Layer sub-record of type 0x0003 with MU = 0

- **Conforming? No.** 0x0003 is in the record-type **reserved** range 0x0003–0x7FFF (§10.2 `[R-EXT-02]` table). `[R-EXT-03]`: "a value from a reserved range MUST NOT be emitted at all before this specification assigns it." `[R-CNT-15]`: "one from the reserved range is a value this specification has not assigned — emitting it is a violation."
- **Reader:** treats it as an unknown sub-record type with MU = 0 → **ignore-record** (§7.4 `[R-CNT-18]`: "an unknown sub-record type with MU = 1 is reject-layer — never reject-file — and with MU = 0 is ignore-record"; `[R-EXT-03]` routes reserved record types to "`[R-CNT-18]` for layer sub-records"). The record is skipped as though absent; the layer is otherwise read normally, and decoding of stored data is unaffected (§2.4's table). The reader has no obligation to detect the reserved-range violation — its assigned detector is the verifier — though `[R-CNF-12]` licenses it to reject on detecting it.
- **Verifier:** `[R-CNT-15]` — "a verifier MUST treat a reserved-range record type as a validity error at the record's governing scope." A sub-record's governing scope is the layer (`[R-CNT-13]`: "the layer for a layer record and for sub-records"; `[R-CNT-18]`: "Sub-records are layer-scope records") → **reject-layer**, and no certification. Register row **L26** (§21.3), detector *verifier*, detected *certification*.

### 8. Index entry: offset = length = 0xFFFF_FFFF_FFFF_FFFF, crc = 0x00000001

**The reader returns nothing for that tile — the read reports failure (reject-tile).**

§15.3 `[R-IDX-03]`, second row of the table: "offset = S ∧ length = S ∧ crc ≠ 0 → reject-tile." The sentinel is the whole 20-byte pattern `FF ×16 00 ×4` (§15.2 `[R-IDX-02]`); a nonzero crc disqualifies it. Register row **T6** (§21.4), detector *reader*, detected at *tile use*.

It **must not** read as fill: `[R-TYP-09]` — "Fill is produced by exactly one condition: a sentinel entry read from a verified index chain... A reader MUST NOT return fill for a tile whose entry is malformed (§15.3)" — reinforced by `[R-CNF-09]`. Blast radius is the tile only: all other tiles of the layer, including neighbors, are unaffected (§2.4's outcome table), and §19.4 step 4 says a rejected tile's read reports failure with fill never a fallback.

### 9. Physical length = committed_file_length + 64

**Outcome: reject-file, at §19.1 step 2 (the trailer gates), under `[R-CNT-06]`.** The reader never scans backward (`[R-LIF-05]`).

Which gate fails depends on what the trailing 64 physical bytes hold, because the reader's tail read lands on the residue, not on the committed trailer:

- If those 64 bytes are not a trailer at all — the ordinary residue case — the failure is the magic gate or the trailer CRC (`[R-CNT-06]`; register rows **F10**, **F16**), and the reader reports the file torn or invalid (`[R-LIF-05]`).
- If they parse as a trailer whose committed_file_length is 64 less than the physical size, the failing gate is "committed_file_length equals the file size (for a remote reader, the size reported by its transport)" (`[R-CNT-06]`, with `[R-CNT-10]` fixing how the size is obtained and forbidding substituting the trailer's own field) — register row **F19**.

§9.5's Note names this case directly: "Residue past a completed commit carries no register row of its own. A reader meets it as a trailer that fails its gates — the magic, the CRC, or committed_file_length against the transport size, each of which §21.2 already registers."

The §9.4 half: the state is a **writer** violation of `[R-LIF-04]`, which requires that after any commit "the physical file length equals committed_file_length, and bytes beyond a committed length never survive into any committed state." A writer meeting this file MUST NOT append (§9.4); recovering the earlier state is §9.6's deliberate scan (`[R-LIF-06]`), never an implicit step of opening for append.

### 10. Codec 3 frame with Content_Checksum_flag set

- **Scope rejected: the tile** — reject-tile.
- **Actor: a reader** (not merely a verifier). §17.2 `[R-COD-06]`: "Writers MUST NOT set the frame's content-checksum flag — the entry's crc already serves that role — and MUST NOT declare a window size exceeding the tile's decoded size; a reader MUST treat either as a validity error at tile scope, both being header-checkable."
- **Detection point: at use of the tile** (§19.2's third tier, "the index-chain, payload, and decode checks (§19.4), before any sample of that tile is returned"). Register row **T20** (§21.4): detector *reader*, detected *tile use*, governing rule `[R-COD-06]`.
- Being header-checkable it can be caught immediately after §19.4 step 5's fetch and crc verification, before decompression; `[R-RDR-02]` fixes only the latest permissible point and licenses earlier detection. Verifiers inherit this reader obligation (`[R-CNF-11]`).

### 11. Planar bool plane, P = 10, fill = true, all ten values false

**`00 FC`** (2 bytes).

- Decoded size = ⌈P/8⌉ = ⌈10/8⌉ = 2 bytes (§14.3 `[R-SER-03]`).
- Values 0–7 occupy bits 0–7 of byte 0, LSB-first, 0 = false → byte 0 = `0x00`.
- Values 8–9 occupy bits 0–1 of byte 1, both false → both clear.
- P mod 8 = 2, so bit positions 2 through 7 of the final byte are **pad bits**, and §14.5 `[R-SER-05]` requires "Every pad bit (§14.3) MUST carry the plane's channel's fill bit" — fill true → 1 → bits 2–7 set = `0xFC`.

This is §14.3's worked example with the values changed: it gives `55 FD` for alternating values with fill true, whose final byte is the same `0xFC` pad mask OR'd with value bit 0. A verifier checks the pad bits; a violation is a validity error at tile scope (`[R-SER-05]`, row **T5**).

Assumption stated: all ten positions are real sample positions. If any of the ten were padding positions (§11.3), `[R-SER-05]` would require the fill bit (1) there, so a tile with ten false values would then be nonconforming at tile scope (row **T4**) and the byte pattern would differ.

### 12. Planar, rank 2, extents (4,4), tile extents (2,2), channels u (uint16), v (float32)

- Grid counts G = (⌈4/2⌉, ⌈4/2⌉) = (2, 2); N = ∏Gᵢ = **4**; P = ∏Tᵢ = **4** (§11.2 `[R-GEO-03]`).
- Spatial tile ordinal of (t₀, t₁) = (1, 0) under linearization 1: s = Σ tᵢ·∏_{j>i} Gⱼ = 1·2 + 0 = **2** (§11.4 `[R-GEO-06]`).
- v is the second declared channel, so its index c = **1** (§3.1: 0-based position in declared order).
- **Disk tile ordinal = c·N + s = 1·4 + 2 = 6** (`[R-GEO-06]`, channel-major grouping). Its index entry sits at region byte 20·6 = 120 (§15.1 `[R-IDX-01]`).
- **Decoded size = P · Bᶜ = 4 × 4 = 16 bytes** (§14.2 `[R-SER-02]`, row "planar, numeric channel c"; float32 element size 4, §12.1). The u channel's planes would be 4 × 2 = 8 bytes each; per-channel sizes differ, which is normal for planar (`[R-SER-09]`).

### 13. A vector whose recorded outcome is reject-layer

Its file must also contain an **intact sibling** whose decoded content the manifest records — §24 `[R-VEC-04]`: "Every vector whose recorded outcome is reject-layer or reject-tile is built inside a file that also carries an intact sibling — another layer, or another tile of the same layer — whose decoded content the manifest records."

For a *reject-layer* vector the sibling must be **another layer**: the damaged layer's data and metadata are entirely unusable (§2.4's outcome table), so no tile of it can serve as the intact sibling. (The rule states the disjunction generically across reject-layer and reject-tile; the "another tile of the same layer" branch is the one that serves reject-tile vectors.)

**Why the specification requires it** — `[R-VEC-04]`'s own reason: "Without the sibling a vector cannot distinguish a reader that scopes its refusal from one that rejects the file entire, because `[R-CNF-12]` permits the latter for any nonconforming file and every vector built from §21's register is nonconforming." The expectation is therefore a pair: the scope no reader is permitted to serve, and the content a reader that serves anything at all owes. A corpus of single-scope vectors "would demonstrate only that a violation was detected, which is the weaker of the two claims §24 makes."

Alongside it, `[R-VEC-02]` requires the manifest entry to record the identifier, whether the file is conforming, the decoded content returnable from every readable scope (floats as hexadecimal bit patterns), and for each damaged structure the outcome class, the scope, and the §21 register row exercised.

### 14. float32 fill 0x7FC00001, unstored addressed tile

**The reader returns the four bytes `01 00 C0 7F`** — the recorded fill, little-endian (§4.1 `[R-ENC-01]`), bit-exactly.

- §13.3 `[R-TYP-08]`: for every addressed tile that is not stored, a reader returning any of the tile's sample positions inside the extents MUST return that channel's fill value at every such position. §19.4 step 4 restates it: a valid sentinel short-circuits payload I/O and yields the recorded fill bit-exactly.
- §13.1 `[R-TYP-06]`: fill is authoritative — the reader "MUST take a channel's fill from its channel entry, MUST NOT substitute a type-derived default or any other value, and MUST return fill bit-exactly as recorded."

**May it substitute 0x7FC00000? No.** §12.3 `[R-TYP-04]`: "NaN payloads are preserved — never quieted, canonicalized, or collapsed." §3.2 `[R-MDL-02]` requires bit-for-bit correspondence to the reference array. §12.3's own example makes the point with this exact value: "A fill of `0x7FC00001` — a NaN carrying a payload — is equally valid and round-trips bit-exactly (§13.1)." `[R-TYP-05]` confirms every bit pattern of the element size is a valid fill.

Two conditions on the answer: the position must lie inside the layer's extents (padding positions are never returned, `[R-GEO-04]`), and the sentinel must have come from a verified index chain — otherwise `[R-TYP-09]`/`[R-CNF-09]` forbid returning fill at all.

### 15. Directory region ends at offset 235

- **Smallest conforming committed_file_length: F = 320.**
- **The trailer begins at offset 256.**

Derivation: §6.2's trailer table requires dir_offset + dir_length ≤ F − 64, so F ≥ 235 + 64 = 299; and committed_file_length must be a multiple of 64 ("= F; multiple of 64", equivalently F mod 64 = 0, §5.1 `[R-CNT-01]`). The least multiple of 64 that is ≥ 299 is 320 (64·4 = 256 < 299 ≤ 320). The trailer occupies the final 64 bytes, [F − 64, F) = **[256, 320)**, at a 64-aligned offset. F = 320 also clears the 128-byte floor (`[R-CNT-27]`).

The bytes [235, 256) — 21 bytes — are the **pre-trailer pad**: slack, which a writer SHOULD zero (`[R-CNT-03]`), whose count is unbounded by this specification, and in which a verifier MUST treat any structure as a file-scope validity error (`[R-CNT-05]`, row **F9**).

---

## Findings

**AMBIGUITY-1 — §21.1, the Instances column: two rules for what an instance is.**
Location: §21.1, paragraph beginning "The **Instances** column enumerates…".
Permitted readings:
(a) *The cell governs, mechanically.* "Instances within a cell are separated by semicolons, and a cell reading — is one instance; the count is therefore mechanical." A row whose condition prose lists three alternatives but whose cell reads — has one instance.
(b) *The condition governs.* The preceding sentence defines an instance as naming "a field the condition ranges over, a container it can occur in, **one of several alternatives the condition text states**, or any combination of the three," which makes such a row a three-instance row whose cell is simply under-filled — i.e. a defect in the row, and `[R-ERR-02]`/`[R-VEC-03]` would then owe three vectors, not one.
Chosen: (a). The sentence that states how the count is *determined* is explicit, calls itself mechanical, and keys on the cell; and applying it over §21.2–§21.5 reproduces §21.8's published "125 conditions over 244 named instances" exactly, which reading (b) would not. Reading (b) is best understood as describing what an author *should* put in the cell, not how a counter reads it.
Live examples of the divergence: **L42** ("gap, overlap, or out-of-ordinal placement", cell —), **T18**'s condition prose vs. its four enumerated instances (enumerated, so no divergence), **F33** (two alternatives in prose, two instances in cell). L42 is the clean case where the two readings disagree.

**AMBIGUITY-2 — §16.2 `[R-SLB-04]`: is the stale-declaration rule a byte predicate or a conduct rule?**
Location: `[R-SLB-04]`, "A writer or updater whose commit supersedes a stored tile in… a slab-declared layer MUST either re-establish the invariants for every affected run… or clear the declaration in the new generation; carrying a stale declaration forward is a validity error at layer scope."
Permitted readings:
(a) *Byte predicate, coextensive with `[R-SLB-03]`.* "Re-established" means the invariants hold in the new generation, so a file violates `[R-SLB-04]` exactly when it violates `[R-SLB-03]`, and §16.2's Note is right that the violation "carries no register row of its own."
(b) *Conduct rule with an independent extension.* "Re-establish" means the writer performed the check. Then a commit that supersedes the only stored tile of a run and happens to place the new payload at an A_slab-aligned offset carries the declaration forward *unre-established* while `[R-SLB-03]`'s invariants still hold — a `[R-SLB-04]` violation with no verifier-detectable witness, which would make §21's normatively-complete register (§21.1) incomplete.
Chosen: (a), because §16.2's Note asserts it outright ("every file exhibiting one exhibits a run whose tiles are unpacked or whose first stored tile is misaligned") and because §2.3 `[R-CNF-02]` says conduct rules bind the actor while the predicate binds the bytes — so a rule phrased as "a validity error at layer scope" is a bytes rule. Under (a) the answer to question 6 is exactly rows L42/L43; under (b) there is a further, undetectable violation the register does not carry.

**AMBIGUITY-3 — §9.7 `[R-LIF-08]` enumerates a layer record's extent twice.**
Location: §9.7: "From the live trailer it enumerates the live directory and its records, **each record's extent**, and **each layer's tile-index region** together with that region's non-sentinel entries; it checks that these occupy disjoint byte ranges."
For a layer record, its extent *is* the tile-index region (§7.4: "A layer record's extent slot addresses the layer's tile-index region"). The two enumerated items therefore denote the same bytes.
Permitted readings: (a) they name one structure, listed twice for emphasis, and it is enumerated once in the disjointness check; (b) they are two claimants, in which case every file containing a layer with a nonempty index fails the disjointness check — a check no conforming file could pass.
Chosen: (a); (b) is absurd and contradicted by §5.2's class list, which names "a record extent (the bytes any record's extent slot references, whatever the record's type, §7.2)" as one class covering both. Worth reporting because a verifier implemented literally from §9.7's sentence — the section a verifier author will implement from — self-reports overlap on the very first layer, and §21.3 L19 ("Two structures of one and the same layer claim overlapping bytes") is the row it would spuriously fire.

**OBSERVATION — question 9's case is decidable only from the residue's bytes.**
Whether the reject-file verdict is charged to the magic gate (F10), the trailer CRC (F16), or the size gate (F19) depends on what the last 64 physical bytes happen to contain, and slack/residue content is unconstrained (§5.2 `[R-CNT-21]`). §9.5's Note anticipates this and declines to register the case; the outcome (reject-file) is invariant across all three, so nothing is undecidable — but a test that pins the *row* for "physical file 64 bytes longer than F" must fix the residue bytes, and a reader cannot distinguish residue from corruption because `[R-LIF-05]` forbids it to scan backward.

**OBSERVATION — §21.8's "244 named instances" is decidable but expensive by hand.**
Confirming `[R-ERR-02]`'s coverage claim means applying §21.1's counting rule to 125 rows across four tables and summing semicolon-separated entries. I confirmed it mechanically (125 / 244, exactly as published). By hand it is an error-prone hour, and any future edit to a Condition or Instances cell silently invalidates both §21.8's stated totals and the per-section counts in §21.2 ("39 conditions"), §21.3 ("50"), §21.4 ("26"), §21.5 ("10"). Nothing in the document is wrong here; the cost of re-deciding it after an edit is the observation.

No contradictions found in the fifteen areas examined. Every question above was answerable from `spec/tarn.md` alone; questions 4, 6, and 9 required choosing among readings, disclosed above.