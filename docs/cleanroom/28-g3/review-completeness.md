# Round 28 completeness review — working transcript

## Disclosure

I read only `/Users/robertkleffner/Documents/GitHub/tarn-first-draft/spec/tarn.md`
(4,648 lines), via `cat -n` and `sed -n` over that one file, plus local
Python arithmetic (a from-scratch CRC-32C implementation, no file I/O) to
check the Appendix A worked example. I did not open any ADR, PLAN.md,
AGENTS.md, registry.json, or any other file, did not run git log/diff, and
did not list any directory other than creating my own scratch folder.

Before starting, my context window already contained an environment block
naming this repo, its branch, and recent commit subjects (including one
reading "the generation counter is removed, the trailer reordered, a struck
row label retired" and another "ADR-0112: seven defects in ADR-0111's own
text"). Per instructions I am disregarding this as evidence about the
specification and not treating it as license to skip verification — but I
note that the charter's own hint ("a recent change removed a structural
field from a fixed-size structure...") independently pointed me to the same
area (the trailer / §9.3 generations), which I verified from the document
text itself (the phrase "No field numbers generations" at line ~395, the
struck row label F11 at §21.2's closing note, the 64-byte trailer layout
table at §6.2), not from the commit-subject text.

## Sections opened

- §1 Introduction (pillars, "no generation-attribution machinery")
- §2.1–2.2 (normative language, `[R-CNF-01]`, requirement-identifier stability)
- §3.1 terms (generation, trailer, directory) — lines ~340–400
- §4.2 Integer types and domains (`[R-ENC-03]`, `[R-ENC-04]`)
- §4.5 checksum coverage table (§8.1)
- §5.1–5.2 tail-anchored discovery, byte coverage (`[R-CNT-02]`, `[R-CNT-21]`, `[R-CNT-03]`)
- §6.1–6.4 front signature block, trailer layout, version/flag gates, remote-open accounting
  (`[R-CNT-04]`, `[R-CNT-05]`, `[R-CNT-06]`, `[R-CNT-24]`, `[R-CNT-08]`, `[R-CNT-26]`, `[R-CNT-09]`, `[R-CNT-10]`)
- §7.2 record framing / multiplicity (`[R-CNT-13]`, `[R-CNT-14]`)
- §8.2 verification chain and outcomes (`[R-CNT-20]`)
- §9.1–9.6 lifecycle (commit protocol `[R-LIF-02]`, generations/file_id/caching `[R-LIF-03]`,
  recovery `[R-LIF-04]`/`[R-LIF-05]`)
- §10.3 experimental range
- §11.1–11.4 geometry, grid arithmetic, linearization/disk ordinal (`[R-GEO-01..06]`)
- §18.2 user-metadata frame constraints / `[R-MTA-10]` (encoding-attaches-document-rules text)
- §20.1, 20.3, 20.4, 20.5 (appender, commit steps, preservation, compaction —
  `[R-WRT-01]`, `[R-WRT-04]`, `[R-WRT-05]`, `[R-WRT-06]`, `[R-WRT-07]`)
- §21.1 "How to read the register" (register-vs-rule precedence)
- §21.2 File-scope violations table (F1–F36, struck F11 note)
- §21.4 Tile-use table (T13–T26)
- §21.5 Ignored records (R1–R10, the experimental-encoding exception paragraph)
- §21.6 Conditions that are not violations (zero-layers row, experimental-encoding row)
- §19.1–19.2 open algorithm and validation timing (`[R-RDR-01]`, `[R-RDR-02]`)
- §22.4/23.2/23.3 privacy (`[R-PRV-03]`, `[R-PRV-04]`, file_id linkage)
- Appendix A annotated minimal file (full byte table + CRC verification)

## Constructions tried

1. **Trailer field removal (direction b, the flagged recent change).**
   Hypothesis: the removed generation-counter field left some sentence
   true of the old field but only "plausible" of its replacement (file_id
   or committed_file_length F). Traced every place file_id and F are used
   to order/identify/cache generations (§9.3, §9.2's Notes, §20.5,
   §23.2/23.3). Every claim I found is explicitly and carefully hedged:
   "F counts bytes, not commits... how many commits a file has undergone
   is not recoverable... no field records it" (§9.3 Note); file_id's
   uniqueness is stated only as writer SHOULD-advice with an explicit
   discussion of the collision case it doesn't prevent (§9.3's second
   Note); §23.2 states file_id is "high-entropy only when its writer
   follows §9.3's randomness advice, which [R-LIF-03] states as a SHOULD"
   — no false strong claim survives. Cross-checked the trailer byte
   layout (offsets 0,8,10,12,16,24,32,40,48,60 summing to 64) against the
   Appendix A hex dump and independently recomputed the worked example's
   CRC-32C over trailer bytes [64,124) in Python from scratch: result
   0x402f157e / bytes 7e 15 2f 40, matching the document exactly. Also
   checked `[R-CNT-24]`'s "permanent across every major" claim (magic at
   F-64, version fields at F-56, CRC at F-4 over [F-64,F-4), 48 bytes
   free for future majors) against the current field table: 8+2+2=12,
   +4(CRC)=16 bytes permanently fixed, 64-16=48 — arithmetic matches
   exactly. Found the struck-row note (F11) is handled exactly as
   `[R-VEC-02]`/§2.2 prescribes (permanently retired, gap left in the
   table, no renumbering). **No divergence found: this area was already
   settled to be self-consistent.**

2. **Roster item 13 (§21.5 experimental-encoding exception vs. R2/CRC).**
   Checked whether "except at an experimental-range encoding, where no
   document rule attaches" could be read to also excuse R2 (the extent's
   terminal CRC check). Found the governing rule `[R-MTA-10]` explicitly
   lists the terminal CRC as one of the structural checks that still
   apply "alone" at an unassigned/experimental encoding ("file conformance
   ... is decided by the structural checks that precede the document
   alone: the record's framing and extent slot ..., the encoding byte's
   own value set ..., and the extent's terminal CRC"). That forecloses
   the ambiguity: R2 is not a "document rule" and R-MTA-10 says so in so
   many words. Killed by R-MTA-10's own explicit enumeration.

3. **Roster item 15 (compaction index-region regeneration keyed to region
   relocation, not tile relocation).** Tried to construct a compactor that
   relocates a layer's stored tiles but leaves the tile-index region's own
   file offset unchanged, to see if the parenthetical's phrasing would let
   it skip regenerating entries. Found the surrounding text's actual MUST
   clause is independent of the parenthetical: "regenerates each relocated
   tile-index region (entry offsets new; ...)" is itself embedded in a
   sentence governed by the general obligation that a compactor "preserves
   no placement" and updates whatever it relocates; and separately, the
   general index-entry correctness requirement (an index entry's offset
   must equal the tile's actual byte position, checked by T1's CRC/
   decode path) forces correct entries regardless of how this specific
   clause phrases its trigger. Killed by the more fundamental structural
   requirement that entries must correctly address their tiles.

4. **Roster item 7 (§20.3 step 4 renumbering gloss vs. planar channel-set
   changes).** Tried to construct a writer that follows the parenthetical
   literally ("a geometry change renumbers ordinals...") and therefore
   fails to move entries when only a planar layer's channel set (not its
   geometry) changes. Found (a) the operative MUST text is "every other
   entry byte-identical at its disk-ordinal position" — a self-correcting
   formulation that doesn't require identifying *why* an ordinal moved,
   only where it currently sits under `[R-GEO-06]`'s live formula; and (b)
   any legal channel-set change on a layer that still has tiles whose
   decode meaning would be disturbed is independently barred by the
   general "MUST NOT alter what §14 fixes for a stored tile" rule earlier
   in the same step, so the only legal channel-set edits are on layers
   with zero stored tiles in the superseded generation, where there is no
   real data whose disk-ordinal position matters. Killed by the operative
   clause's self-sufficiency plus the prior bar's scope.

5. **Roster item 16 (L23 Detected = "layer access" vs. §19.1 step 4/§19.2
   placing the name-fits determination at open).** Confirmed the tension
   is real for the "name" instance of L23 (§19.1 step 4 explicitly performs
   the inline_length-overrun check on the name field while building the
   open-time layer-name namespace, and §19.2 lists "the layer-name
   namespace" as an at-open obligation). But `§21.1`'s own governing
   sentence — "where such an entry and the rule it cites diverge, the rule
   governs there too" — already resolves any register-table-vs-rule
   conflict in the rule's favor: a reader that mis-times detection to
   satisfy L23's label while violating `[R-RDR-01]`/`[R-RDR-02]`'s actual
   at-open obligation is nonconforming under the rule regardless of what
   the table's "Detected" cell says. No second conforming reading survives
   once §21.1's precedence sentence is applied. Killed by §21.1.

6. **Roster item 2 (§21.6 zero-layers row: "an empty directory").**
   Checked whether "zero layers" could license other directory content
   while the row's answer wrongly narrows it to "an empty directory."
   Confirmed `[R-CNT-14]` (the cited rule) is correctly the rule that both
   permits zero layer records *and* separately bounds user-metadata
   record multiplicity — so the citation is right; only the row's answer
   text ("an empty directory") is inaccurate against a file with zero
   layer records but a file-scope user-metadata record present. This is a
   commentary/gloss inaccuracy in a table that adds no independent
   normative force (the actual permission is `[R-CNT-14]`'s own sentence,
   already correct) — does not move the emittable set.

7. **Roster item 14 (grid product zero factor).** Confirmed `[R-GEO-03]`'s
   overflow check binds the *mathematical value* of the declaration-derived
   product (N = ∏Gᵢ, etc.), not any particular evaluation order's
   intermediate result. A zero factor makes the true mathematical value of
   the whole product 0 regardless of which partial products an
   implementation forms along the way, so there is no accept/reject
   divergence between two conforming readers — only an implementation
   detail about how to multiply without spurious intermediate overflow,
   which is not something the spec's normative text (a predicate over a
   mathematical value) actually turns on. Consistent with this item's own
   skeptic-triage outcome (REFUTED/none).

8. Spot-checked items 4, 6, 9, 11, 12, 17, 18 against their governing rules
   (`[R-CNF-01]`, `[R-WRT-01]`, `[R-CNT-21]`, `[R-ERR-01]`, `[R-CNT-25]`'s
   register rows, §2.1's Note) without finding any point where the
   disputed text is itself the operative constraint on bytes — in each
   case a more fundamental rule elsewhere in the document (not the
   disputed sentence) is what a reader/writer must actually satisfy, and
   that rule is unambiguous. No new construction pursued to full byte
   detail for these given the effort budget; flagged as lower-priority
   because their roster descriptions are about labeling/citation/coverage
   of an itemized list (register bookkeeping), not about a rule's own
   truth-condition.

## Conclusion

No construction produced two conforming implementations that diverge on
emitted bytes or on an accept/reject verdict for the same file. Every
candidate collapsed once the actual governing MUST-clause (as opposed to
a parenthetical gloss, a register-table cell, or a non-normative aside)
was traced to its source. The recently-changed trailer/generation-counter
area, which the charter specifically flagged as this cycle's likely
failure mode, turned out on inspection to have been written with unusually
careful hedging (explicit "no field records the commit count" language,
explicit SHOULD-only uniqueness advice with its own collision discussion)
— it reads like an area that has already been through the kind of scrutiny
this exercise is for.

Verdict: NOT_BYTE_LEVEL.
