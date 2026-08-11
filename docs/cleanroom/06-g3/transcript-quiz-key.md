# Cleanroom round 6 — quiz answer key

I read **only** `/Users/robertkleffner/Documents/GitHub/tarn/spec/tarn.md`. No docs/, no conformance/, no registry.json, no git history, no web. The one script I ran parsed that same file's §21 tables and nothing else.

---

# QUIZ ANSWER KEY

## 1. Can a byte of the live committed state be claimed by no coverage class?

**No — and it is unfalsifiable rather than merely false.**

§5.2 defines the live committed state *extensionally*: "the front signature block, and every structure reachable from the live trailer through the live directory's records, extent slots, and tile-index entries, together with the live directory and the live trailer." §9.7 `[R-LIF-08]` enumerates the same walk operationally (directory → records → each record's extent → each layer's tile-index region and its non-sentinel entries) and closes it: "Bytes the walk does not reach are slack."

So membership in the live state *is* membership in one of `[R-CNT-02]`'s classes (the tile-index region is reached as the layer record's *record extent*, §7.4). A byte outside the union is not an uncovered live byte; it is slack by definition. §5.2's own Note says so: "'belongs to no class' describes nothing, and a register row for it would be a row no file could exhibit."

Uniquely determined. Consequence worth stating: of `[R-CNT-02]`'s two halves only **disjointness** is testable, and that is what §9.7 has a verifier check (`[R-CNT-02]`, `[R-LIF-08]`, register row F36/L19).

## 2. Interleaved bool value byte = 0x7F at a real sample position

- **Conforming? No.** `[R-SER-08]`: "Writers MUST NOT emit any byte other than 0x00 or 0x01 as an interleaved bool value. Any other byte makes the file nonconforming."
- **A reader that returns the value reports `true`.** `[R-SER-08]`: "MUST report 0x00 as false and every other byte as true." A reader is not obliged to screen decoded content and is not nonconforming for missing it; if it *does* detect it, `[R-CNF-12]` licenses refusal (at tile scope or wider, the file being nonconforming). §19.4 step 8 and Appendix H both name this as the sole byte a reader resolves rather than passes through.
- **A verifier** treats it as a validity error at **tile scope** → reject-tile, at **certification**, and MUST NOT certify the file (`[R-CNF-12]`; §17.4 `[R-COD-11]` if it cannot run the codec at all). Register row **T2** (§21.4), detector *verifier*, governing rule `[R-SER-08]`.

Note the position qualifier is load-bearing: at a *padding* position the governing rule is `[R-SER-05]`/row T4 (the byte must be the fill byte), not `[R-SER-08]`.

> **AMBIGUITY — §14.2 `[R-SER-08]`.** The rule fixes the *logical value reported* ("report … as true"), not the *bytes returned*. For a byte-oriented API two readings are permitted: (a) return the stored byte `0x7F` and label it true — consistent with `[R-MDL-02]`'s bit-pattern pass-through; (b) return a normalized `0x01`. `[R-MDL-02]` cannot arbitrate because the reference array is undefined at a byte a conforming file cannot carry. I picked (a) for the byte and *true* for the value, since `[R-TYP-04]`'s no-alteration rule is the document's default and `[R-SER-08]` overrides only the interpretation. Either reading answers the question the same way at the value level.

## 3. Remote open of Appendix A's 128-byte file, baseline strategy

**Two round trips**, per `[R-CNT-09]`:

1. Suffix range for the final 64 bytes = **[64, 128)** (`Range: bytes=-64`). Validate per §6.2/§6.3 in the fixed order.
2. **[dir_offset, dir_offset + dir_length) = [16, 20)**; verify its terminal CRC-32C — here `00 00 00 00`, the CRC of zero bytes (§7.1, §4.5).

**File size**: from the range response itself — `[R-CNT-10]` requires a *transport-authoritative* size ("the complete length of a range response"), and explicitly forbids substituting the trailer's `committed_file_length`. §6.4 states this is why "steps 1 and 2 cost one request between them" (§19.1 step 1).

The front signature block is **not** fetched: `[R-CNT-04]` lets a remote reader defer or omit that check, and §6.4 says the two-request accounting excludes it. Appendix A restates exactly this.

> **OBSERVATION — §6.4 `[R-CNT-10]`.** "Two" holds only on a transport with suffix-range support. On one without, the SHOULD fallback ("a size probe plus an absolute range") makes the baseline **three** requests, and a reader that omits the fallback fails the open outright. The answer is unique once suffix ranges are assumed, which "baseline" implies but does not say.

## 4. Instances cell reads a single em dash; condition text states three alternatives

**One instance.** §21.1: "Instances within a cell are separated by semicolons, and **a cell reading — is one instance; the count is therefore mechanical**." The consequences follow mechanically: `[R-ERR-02]` requires one vector for that row (the "one vector per instance" clause bites only on *a row naming instances*), and `[R-VEC-03]` inherits that.

I verified the mechanical rule is the one the document itself uses: applying it to §21.2–§21.5 yields exactly **125 rows / 244 instances**, the numbers §21.8 states.

> **AMBIGUITY — §21.1, the two definitions of "instance".** The constitutive sentence — "An instance names a field the condition ranges over, a container it can occur in, **one of several alternatives the condition text states**, or any combination" — makes such a row have **three** instances. The bookkeeping sentence makes it have **one**. Both are in the same paragraph, both are normative prose, and §21.1's tie-breaker ("where a row and the rule it cites diverge, the rule governs") resolves *row vs. governing rule*, not *Instances cell vs. Condition cell*. Permitted readings: (a) 1 — the cell is authoritative, the count is mechanical, and the row is *defective* under §21.1's own definition of instance (the corpus will under-cover it by two files); (b) 3 — the condition's structure is authoritative and the em dash is a drafting error. I picked **(a)**, because §21.1 says the count is mechanical in so many words and because the §21.8 totals are computed that way. But the document does not state which sentence governs when they disagree, and under (a) it provides no way to flag the row as defective — the em dash is indistinguishable from a correct single-predicate row.

## 5. Two layers A and B; a commit appends layer C

**Structures that become slack — exactly three, all from the prior generation:**

1. the prior generation's **directory region** (record sequence + its terminal CRC),
2. the prior generation's **pre-trailer pad**,
3. the prior generation's **trailer** (64 bytes).

Nothing of A or B: `[R-WRT-05]` requires their records re-emitted byte-identically, extent slot and all, so A's and B's stored-tile extents, tile-index regions, and sub-record extents stay reachable from the new live trailer and remain live state (§5.2, `[R-CNT-02]`). §20.3's Example (a) draws precisely this case: "The slack is the old directory, pad and trailer — sized by the file's *layer count*, never by any layer's data."

Two additions for completeness (bytes that *are* slack after the commit without having been live before): any alignment/slab gap the commit leaves around C's new structures, and the **new** pre-trailer pad (§6.2 `[R-CNT-05]`, §5.2 `[R-CNT-21]`). Under `[R-LIF-08]` a verifier sums all of it into one slack total.

## 6. Slab-declared layer, a tile superseded, declaration carried forward stale

`[R-SLB-04]` states the obligation — re-establish the invariants for every affected run **or** clear the declaration — and then hands off detection: "carrying a stale declaration forward is a validity error at layer scope, **detected as the invariant failures of `[R-SLB-03]` are: by a verifier**." Its Note is explicit that the rule has no register row of its own.

**What the verifier detects**, at **certification**, outcome **reject-layer**:

- **L42** (§21.3) — inside the affected run, a stored tile's offset ≠ the previous stored tile's offset plus that tile's length. Superseding forces the new payload to be appended at F (`[R-LIF-01]`, `[R-LIF-02]` step 1), so the run's packing breaks. Governing rule `[R-SLB-03]` (via `[R-IDX-03]`).
- **L43** — if the superseded tile was the run's *first* stored tile, its new offset must still satisfy `offset mod A_slab = 0`; otherwise this row fires as well or instead.

And `[R-CNF-12]`: a verifier certifies only violation-free files, so it MUST NOT certify.

> **OBSERVATION — §16.2 `[R-SLB-04]` vs. its own Note.** `[R-SLB-04]` calls the stale declaration itself "a validity error at layer scope", but its detection is reduced entirely to `[R-SLB-03]`'s invariants. There is a residual case where the two disagree: a run whose only stored tile is the superseded one, re-landed at an `A_slab`-aligned offset, satisfies packing trivially and alignment by luck — the writer never re-established anything, yet no `[R-SLB-03]` row fires and the bytes are conformant. Under `[R-CNF-02]` ("conduct rules bind the actor, the predicate binds the bytes") such a file is conforming, so the Note's "every file exhibiting one exhibits a run whose tiles are unpacked or whose first stored tile is misaligned" is not quite true — but nothing observable turns on it. Decidable, disproportionately expensive to legislate; reported, not treated as blocking.

## 7. Layer sub-record of type 0x0003 with MU = 0

- **Conforming? No.** 0x0003 is in the record-type **reserved** range 0x0003–0x7FFF (§10.2 `[R-EXT-02]`). `[R-CNT-15]`: "one from the reserved range is a value this specification has not assigned — emitting it is a violation." §10.3 `[R-EXT-03]` reiterates that a reserved value MUST NOT be emitted at all.
- **Reader: ignore-record.** The MU rule applies unchanged (`[R-CNT-15]`: "Readers of both apply the MU rule above unchanged"; `[R-CNT-18]`: "an unknown sub-record type with MU = 1 is reject-layer — never reject-file — and with MU = 0 is ignore-record"). The sub-record is skipped as though absent (§2.4); the layer stays readable and decoding of its tiles is unaffected. The reader has *no* obligation to notice the reserved-range violation — but `[R-CNF-12]` permits it to refuse the nonconforming file if it does.
- **Verifier: reject-layer at certification.** `[R-CNT-15]`: "a verifier MUST treat a reserved-range record type as a validity error at the record's governing scope"; the governing scope of a sub-record is the layer (`[R-CNT-18]`, `[R-CNT-13]`). Register row **L26** (§21.3), detector *verifier*, rule `[R-CNT-15]` (via `[R-CNT-18]`). It MUST NOT certify.
- Side note (not asked): the updater obligation follows the *stored* PE bit under §20.4 `[R-WRT-08]` — retain byte-identical if PE = 1; droppable only under the MU = 0 / PE = 0 row's conditions.

Uniquely determined.

## 8. Entry with offset = length = 0xFFFF_FFFF_FFFF_FFFF, crc = 0x00000001

**The read of that tile reports failure — reject-tile. No fill, no data.**

§15.3's table, row 2: "offset = S ∧ length = S ∧ **crc ≠ 0** | reject-tile" (`[R-IDX-03]`). The entry is *not* a valid sentinel: §15.2 `[R-IDX-02]` defines the sentinel as the exact 20 bytes `FF ×16 00 ×4`.

Therefore `[R-TYP-09]` bars fill: "Fill is produced by exactly one condition: a sentinel entry read from a verified index chain… A reader MUST NOT return fill for a tile whose entry is malformed (§15.3)" — reinforced by `[R-CNF-09]` ("a read of a rejected tile MUST NOT silently return fill"). Detection is the **reader**'s, at **tile use** (§19.2, §19.4 step 4). Register row **T6** (§21.4). Every other tile of the layer, and every other layer, is unaffected (§2.4).

## 9. Physical length is 64 bytes greater than committed_file_length

**Reject-file, at §19.1 step 2 (the trailer validation), under `[R-CNT-06]`.**

A reader anchors on the *physical* end: §6.2 and `[R-LIF-05]` — "a reader that finds no valid trailer in the final 64 bytes MUST report the file torn or invalid and **MUST NOT scan backward**." §9.4 `[R-LIF-04]` is the writer's side: the residue exists because a prior writer failed to truncate to F or overwrite from it; recovery (§9.6 `[R-LIF-06]`) is a deliberate, separate operation and never an implicit reader or append step.

Which gate fires depends on what the trailing 64 bytes hold, and §6.2 fixes the order (magic → trailer CRC → version gate → remaining field gates):

- If the last 64 bytes are a valid trailer declaring `committed_file_length` = physical − 64, the magic, CRC and version gates pass and the failure is the **`committed_file_length` = transport-authoritative size** gate (`[R-CNT-06]`, `[R-CNT-10]`) — register row **F19**.
- If they are arbitrary residue, the failure is earlier: the magic (**F10**) or the trailer CRC (**F16**), same rule, same step, same outcome.

§9.5's Note confirms both land here and that residue gets no register row of its own: "A reader meets it as a trailer that fails its gates — the magic, the CRC, or committed_file_length against the transport size, each of which §21.2 already registers."

> **AMBIGUITY (in the question, resolved by the text).** "the trailer's committed_file_length" underdetermines *which* trailer — the one at the physical end, or the committed one 64 bytes earlier that a reader is forbidden to look for. Both readings converge on reject-file at open; they differ only in which of F10/F16/F19 fires. I report both.

## 10. Codec 3 tile whose frame header sets Content_Checksum_flag

- **Scope rejected: the tile — reject-tile.**
- **Actor: the reader** (not the verifier).
- **Detection point: tile use** (§19.2's third tier; §19.4 step 6, and in fact checkable from the frame header before decode).

`[R-COD-06]`: "Writers MUST NOT set the frame's content-checksum flag — the entry's crc already serves that role — and MUST NOT declare a window size exceeding the tile's decoded size; **a reader MUST treat either as a validity error at tile scope, both being header-checkable**." Register row **T20** (§21.4), detector *reader*, detected *tile use*.

Contrast worth recording: the identical constraint on a *user-metadata* zstd frame is **ignore-record**, not tile scope — §18.2 `[R-MTA-09]` ("Any violation here is ignore-record, never the tile-scope outcome §17.2 assigns"), register row **R4** (§21.5).

## 11. Planar bool plane, P = 10, fill = true, ten values all false

**`00 FC`**

- Decoded size = ⌈P/8⌉ = ⌈10/8⌉ = **2 bytes** (§14.3 `[R-SER-03]`).
- Value k occupies bit k mod 8 of byte k div 8, LSB-first, 0 = false (§14.3, §4.4 `[R-ENC-08]`). Values 0–7 false → byte 0 = `0x00`. Values 8–9 false → bits 0–1 of byte 1 = 0.
- Pad bits are bit positions P mod 8 = **2 through 7** of the final byte, and `[R-SER-05]` (§14.5): "Every pad bit MUST carry the plane's channel's fill bit." Fill is true → bits 2–7 set → byte 1 = `0b1111_1100` = **`0xFC`**.

This is §14.3's worked example with the values changed: there, alternating values with fill true give `55 FD` (= `0x01 | 0xFC`); here the value region contributes 0, giving `0x00 | 0xFC`.

Determined uniquely, on the reading that all ten positions are real sample positions. (If any were padding positions, `[R-SER-05]` would force them to the fill *bit* — true — contradicting the premise that all ten values are false; the question's "the tile's ten values are all false" forecloses that.)

## 12. Planar, rank 2, extents (4,4), tile extents (2,2), channels u:uint16 then v:float32

- G = (⌈4/2⌉, ⌈4/2⌉) = (2, 2); N = ∏Gᵢ = **4**; P = ∏Tᵢ = **4**; C = 2 (§11.2 `[R-GEO-03]`).
- Spatial tile ordinal of (1, 0) under linearization 1: s = Σᵢ tᵢ·∏_{j>i} Gⱼ = 1·G₁ + 0·1 = 1·2 + 0 = **2** (§11.4 `[R-GEO-06]`).
- v is the second-declared channel, so its index is c = **1** (§3.1: 0-based position in declared order).
- **Disk tile ordinal = c·N + s = 1·4 + 2 = 6.** (`[R-GEO-06]`, channel-major grouping; §15.1 `[R-IDX-01]` puts its 20-byte entry at region byte 120.)
- **Decoded size = P · Bᶜ = 4 · 4 = 16 bytes** (§14.2 `[R-SER-02]`, planar numeric channel; float32 element size 4 per §12.1 `[R-TYP-01]`).

Channel u's element size never enters either figure — planar planes are sized per channel.

## 13. A reject-layer vector must also contain an intact sibling

`[R-VEC-04]` (§24): every vector whose recorded outcome is reject-layer or reject-tile "is built inside a file that also carries an **intact sibling** — another layer, or another tile of the same layer — **whose decoded content the manifest records**." So the vector's expectation is a *pair*: the scope no reader may serve, and the content a reader that serves anything at all owes. (`[R-VEC-02]` independently requires the manifest to record the decoded content of every readable scope, plus the outcome class, the scope, and the §21 row exercised.)

**Why the specification requires it:** without the sibling, the vector cannot distinguish a reader that *scopes* its refusal from one that rejects the file entire — because `[R-CNF-12]` licenses whole-file rejection for any nonconforming file, and every vector built from §21's register is nonconforming. Such a corpus "would demonstrate only that a violation was detected, which is the weaker of the two claims §24 makes." §24's closing Note adds that a recorded outcome is the *narrowest* scope a reader may refuse, not the only one, so the sibling is the only thing that makes scoping observable.

> **AMBIGUITY — §24 `[R-VEC-04]`.** The sibling clause is one flat disjunction — "another layer, or another tile of the same layer" — applied to both outcomes at once. Read literally it permits a **reject-layer** vector to satisfy the obligation with another tile *of the rejected layer*, which cannot serve the stated purpose: that tile sits inside the unusable scope (§2.4, reject-layer: "The affected layer's data and metadata are not usable"), so no reader owes its content and the vector discriminates nothing. Permitted readings: (a) the disjuncts pair with the outcomes — another layer for reject-layer, another tile for reject-tile; (b) either disjunct for either outcome. I picked **(a)**: only it satisfies the rule's own justification clause. The text states the disjunction, not the pairing.

## 14. float32 fill 0x7FC00001, unstored addressed tile

- **Bytes returned: `01 00 C0 7F`** — the fill value's four bytes exactly as recorded in the channel entry, little-endian (`[R-ENC-01]`, §7.4/§13.1 `[R-TYP-06]`), at every requested sample position of that tile that lies inside the layer's extents (§13.3 `[R-TYP-08]`; §19.4 step 4, which short-circuits payload I/O entirely).
- **May it substitute 0x7FC00000? No.** Three independent bars:
  - `[R-TYP-04]` (§12.3): "NaN payloads are preserved — never quieted, canonicalized, or collapsed."
  - `[R-TYP-06]` (§13.1): a reader "MUST take a channel's fill from its channel entry, MUST NOT substitute a type-derived default or any other value, and MUST return fill bit-exactly as recorded."
  - `[R-MDL-02]` (§3.2): the returned portion of the reference array must be bit-for-bit exact, floating-point payloads included.
  
  §12.3's own example names this bit pattern: "A fill of `0x7FC00001` — a NaN carrying a payload — is equally valid and round-trips bit-exactly." `[R-TYP-05]` makes every bit pattern of the element size a valid fill.

Two preconditions the answer rides on, both stated: the entry must be a **valid sentinel** read from a **verified** index chain (`[R-TYP-09]`, §15.4 `[R-IDX-04]`) — a malformed entry or a failed CRC rejects instead, and fill is never a failure fallback (`[R-CNF-09]`); and padding positions are never returned regardless (`[R-GEO-04]`).

## 15. Directory region ends at offset 235

- **Smallest conforming `committed_file_length` F = 320.**
- **The trailer begins at F − 64 = 256.**

Two constraints bind, both from §6.2's field table and `[R-CNT-06]`:
1. `dir_offset + dir_length ≤ F − 64` → 235 ≤ F − 64 → **F ≥ 299**.
2. `committed_file_length` is **a multiple of 64** (§6.2's valid-values column; §5.1 `[R-CNT-01]`: "F is a multiple of 64"; equivalently the trailer begins at a 64-aligned offset).

The least multiple of 64 that is ≥ 299 is 320 (256 < 299 fails constraint 1). F = 320 also clears the 128-byte floor of `[R-CNT-27]`.

Bytes **[235, 256)** — 21 bytes — are the **pre-trailer pad**: slack under §5.2 `[R-CNT-21]`, zeroed by the advice of `[R-CNT-03]`, and `[R-CNT-05]` requires that no structure occupy them (a verifier-detected file-scope error if one does, row F9). Robust to the off-by-one reading of "ends at 235" (last byte at 235 → F ≥ 300 → still 320).

---

# FINDINGS SUMMARY

| # | Class | Location | Substance |
|---|---|---|---|
| 1 | AMBIGUITY | §21.1 (Q4) | Two normative sentences define "instance" incompatibly — the mechanical em-dash rule (1) vs. "one of several alternatives the condition text states" (3). No tie-breaker: §21.1's row-vs-rule clause addresses a different conflict. Picked the mechanical rule; it is what §21.8's own totals (125 rows / 244 instances, which I reproduced) are computed with. Under it a row can be defective and indistinguishable from a correct one, under-covering the corpus (`[R-ERR-02]`, `[R-VEC-03]`). |
| 2 | AMBIGUITY | §24 `[R-VEC-04]` (Q13) | "another layer, or another tile of the same layer" is a flat disjunction over both reject-layer and reject-tile. Literally it lets a reject-layer vector use a sibling tile *inside* the rejected layer, which defeats the rule's stated purpose. Picked the outcome-paired reading. |
| 3 | AMBIGUITY | §14.2 `[R-SER-08]` (Q2) | Fixes the logical value reported for a nonconforming bool byte, not the byte a byte-oriented API returns; `[R-MDL-02]` cannot arbitrate because no reference-array value exists there. Picked pass-through + logical *true*. |
| 4 | OBSERVATION | §16.2 `[R-SLB-04]` vs. its Note (Q6) | A stale slab declaration is called a validity error, yet its detection is wholly reduced to `[R-SLB-03]`. A run whose sole stored tile is the superseded one, re-landed `A_slab`-aligned, breaks no invariant — so the Note's "every file exhibiting one exhibits…" is not exactly true, though `[R-CNF-02]` makes such a file conforming and nothing observable turns on it. |
| 5 | OBSERVATION | §6.4 `[R-CNT-10]` (Q3) | The "baseline" two-request open is two only on suffix-range-capable transports; the SHOULD fallback makes it three elsewhere. §6.4 names the baseline without stating that precondition. |
| 6 | OBSERVATION | §6.2 / §9.4 / §9.5 (Q9) | Which of F10 / F16 / F19 fires for trailing residue depends on residue content, not on the file's declared state. The document anticipates this (§9.5's Note) and outcome and detection step are invariant, so this is a note for corpus construction rather than a defect. |

No CONTRADICTIONs found. No unresolvable forward references into reserved values or sections were encountered: every reserved range (§10.2 `[R-EXT-02]`) resolves to a stated outcome at the value set that owns it, and the two withdrawn/retired identifiers (`[R-SER-04]`, §14.4) and deleted register row (§5.2's Note) are each disclosed in place.