# Round 16 — adversarial verification of the round's own verdict

Run after triage returned zero byte-level. Two agents were instructed only to
refute the downgrades; two hunted fresh byte-level defects in the changed
sections. Spec-only access. Both refutations succeeded.


## Refutation target: shrink — **DOWNGRADE_REFUTED**

**Disclosure.** I read only /Users/robertkleffner/Documents/GitHub/tarn/spec/tarn.md, via Read on §3.1 (279-358), §5.2 slack (640-665), §7.2-7.4 (900-1000), §9.2/[R-LIF-02] (1165-1205), §11.2-11.4 (1493-1552), §13.1-13.3 (1690-1750), §14.2 (1815-1880), §14.5 (1946-1978), §20.1-20.3 in full (2845-3013), §21.4 register rows T1-T7 (3421-3434), §21.7 [R-ERR-01] (3540-3578), and the conformance definitions at 170-220. I ran grep for R-SER-05, R-CNF-05, R-CNT-17, "supersed", "A creator", "generation 1", and the section-heading index. No git, no docs/, no ADRs, no conformance/, no web.

Method: I first tested whether a layer-extent shrink can alter any §14-fixed item other than padding. It cannot — §14.2's table derives decoded size and every sample offset from P = ∏Tᵢ and the channel element sizes only, and §11.3/§3.1 make every tile the same logical shape, so a change to Eᵢ moves only the padding-position set. That confirmed the triage's implicit premise for the reporter's own counterexample: a carried-forward stored tile that gains padding either already holds fill (explicitly carved out at 2959-2961, permitted under both readings) or fires T4 (3431: verifier, certification) and the file is nonconforming, so [R-CNF-05] bars it both ways. On that narrow construction the triage was right.

I then attacked ground (c) from the other side: instead of looking for a shrink that damages a tile without a T4, I looked for a commit in the divergence class whose damaged tile is not stored in the new generation, so no tile-scope row has anything to fire on. §20.3's own tense sentence (2951-2954) keeps such a commit inside the bar while §13.3, §14.5 and [R-CNT-21] keep the resulting file clean. §21.7 then confirmed the class exists by naming it directly. I checked the escape routes: a creator is generation 1 only (2852), a compactor rewrites under a new file_id (2857-2858), [R-LIF-01] freezes the committed prefix, and the two-commit route (unstore first, shrink second) yields a different generation number and two extra index regions and directories, so it is a different byte sequence. I also checked that nothing else independently bars the construction: step 4 expressly contemplates "entries for tiles that become unstored written as the sentinel" (2934-2935) and "Extents this commit supersedes become slack" inside the shrink paragraph itself (2996-2997); I took a layer with no slab declaration so [R-SLB-01]/[R-SLB-04] are inert; and I scaled the construction so the "SHOULD instead produce a new file" advice at 2990-2993 does not bite.

The downgrade rests decisively on ground (c): the resulting file carries a T4 violation, so [R-CNF-05] bars it under both readings and the emittable set does not move. That is true of the counterexample the reporter chose, and false of the class the defective sentence governs. The spec itself says so.

THE CONSTRUCTION. Rank 1, tile extent 10, no slab declared, extent 10,000,005 — grid ⌈10000005/10⌉ = 1,000,001, all tiles stored in generation N. One commit does two things: shrink the extent to 9,999,995, and write tile 999,999's index entry as the sentinel. Grid falls to ⌈9999995/10⌉ = 1,000,000, so tile 1,000,000 de-addresses — the permission's stated trigger fires. Tile 999,999 covers x = 9,999,990..9,999,999; every one of those positions was real at E = 10,000,005 and x = 9,999,995..9,999,999 are padding at E = 9,999,995, so the shrink alters, for a tile the layer stores in the generation this commit supersedes, "the set of padding positions (§11.3) and the content [R-SER-05] fixes there" — and its carried-forward bytes there hold ordinary sample data, not fill, so the carve-out at 2959-2961 does not apply.

WHY THE FILE IS CONFORMING. In generation N+1 tile 999,999 is not stored. §3.1: "A tile is stored in a generation if and only if that generation's tile-index entry for it is not the sentinel", and "Superseded payload bytes from earlier generations do not make a tile stored." T4 is a tile-scope row about a padding position in a decoded tile image; an unstored tile has no decoded image, so nothing fires. §13.3 makes the addressed-but-unstored tile read as fill. Its old bytes are now slack, and [R-CNT-21]/[R-CNT-03] put slack content beyond every conformance requirement: "no conformance requirement rides on slack content either way." Entry_count is 1,000,000 per [R-CNT-17]. The 999,999 surviving stored tiles are byte-identical and untouched. The file is conforming.

WHY THE TWO READINGS DIVERGE ON IT. Restrictive: the first limb fires for tile 999,999 — it is stored and the shrink leaves it addressed — routing to the general prohibition, whose tense sentence forecloses the obvious dodge in as many words: "a commit does not escape this by unstoring in the same breath." Barred. Permissive: the second limb's trigger fires, and here its stated premise is not merely arguably satisfied but literally true — the new state stores neither affected tile, so "nothing is altered for a tile the new state stores," and even the trailing description "every surviving stored tile is untouched" holds exactly. A writer reasoning from that sentence concludes permitted. This is the sharpest possible form of the reporter's finding: the sentence reasons over the new generation's stored set while the bar it must not override is quantified over the prior generation's, and the two sets come apart precisely when the damaged tile is unstored or superseded.

THE SPEC CONFIRMS THE CLASS. §21.7 [R-ERR-01] names it: "a commit that supersedes every tile it would have damaged leaves the live state clean, so the bar is unwitnessed there for the same reason [R-LIF-01] is." Unwitnessed, not inapplicable. §21.7 is therefore an explicit acknowledgment that §20.3 step 4's bar has a live sub-class in which a conforming writer is forbidden to emit a file that a verifier would certify. That is exactly the shape the byte-level test asks for, and it is fatal to ground (c), whose whole force was that no such sub-class exists.

NO ALTERNATE ROUTE. The disputed bytes are generation N+1 over a frozen generation-N prefix under the same file_id. A creator "emits a complete file in one commit, generation 1". A compactor "rewrites a file whole under a new identity", so its file_id differs. Doing it in two commits — unstore at N+1, shrink at N+2, at which point tile 999,999 is no longer a prior-generation stored tile and the bar does not reach it — produces a different byte sequence: a different generation counter in the trailer, plus an extra index region, directory, CRC, pad and trailer. So under the restrictive reading no conforming writer can produce the disputed sequence at all, and under the permissive reading one can.

Applying the project's criterion in its own terms: the disputed file is conforming, and only one reading permits an actor to produce it. The emittable set moves. Byte-level.

Grounds (a) and (b) survive as arguments about which reading is correct — the first limb does fire, and the general prohibition is unconditional and per-tile — and I think they are right that the restrictive reading is the better one. But they were never byte-level arguments; all three passes graded the finding real, which concedes the permissive reading is available on the text. Ground (c) was the only thing carrying the downgrade, and it does not carry it.

One honest caveat, stated because it cuts the other way rather than mine: the reporter's own counterexample, with tile 1 carried forward and non-fill bytes left in the new padding, genuinely is not byte-level for exactly the reason all three passes gave. The finding is byte-level in scope, not in the instance as written. Whoever repairs §20.3 step 4 should also fix the counterexample in the finding record, or the next reviewer will re-derive the same downgrade from the same too-small example.

**Decisive quotes.**

DECISIVE — §21.7, [R-ERR-01], lines 3564-3573. The spec names the exact class in which the bar applies to a commit whose output is a clean file:

  3564  §20.3 step 4's bar on a declaration change is witnessed only where
  3565  the affected tiles remain stored *and* the change reaches a byte §14
  3566  structurally constrains — a padding position, a pad bit, or a boolean
  3567  byte — where §21.4's content rows fire; a change that reaches the
  3568  decoded size or the codec instead is witnessed by T3 or T14, which
  3569  read the index entry rather than the decoded image; and a
  3570  commit that supersedes every tile it would have damaged leaves the
  3571  live state clean, so the bar is unwitnessed there for the same
  3572  reason `[R-LIF-01]` is: it is a property of the prior generation,
  3573  which §9.7 does not reconstruct;

"witnessed only where the affected tiles remain stored" is the refutation of ground (c) in the spec's own words: where they do not remain stored, no row fires, the file is conforming, and the bar still binds the writer.

THE BAR AND ITS PRIOR-GENERATION QUANTIFIER — §20.3 step 4, lines 2944-2954:

  2944     an appender's. A commit MUST NOT change a
  2945     layer's declarations in a way that alters, for any tile that layer
  2946     stores **in the generation this commit supersedes**, what §14
  2947     fixes for its stored bytes or how they decode —
  2948     the set of padding positions (§11.3) and the content
  2949     `[R-SER-05]` fixes there, the decoded size, the byte offset of any
  2950     sample within the decoded tile image, or the codec and filter that
  2951     produced the stored bytes. The tense is the prior generation's (§3.1 defines *stored* against a generation), so a commit does not
  2952     escape this by unstoring in the same breath: superseding every
  2953     tile of a layer and re-declaring it are one operation, and this
  2954     bars it.

THE DISPUTED PERMISSION — §20.3 step 4, lines 2981-2989. Note that its premise is quantified over the NEW state's stored set:

  2981     An extent MAY also **shrink**. Where the shrink leaves a stored
  2982  tile addressed it is the case above — barred wherever it alters
  2983  what §14 fixes for that tile — but where it drops a tile out of the
  2984  addressed set entirely (§11.2's grid count falls), nothing is
  2985  altered for a tile the new state stores, and the commit is
  2986  permitted: the de-addressed tiles' extents become slack
  2987  (`[R-CNT-21]`), `[R-CNT-17]` obliges the smaller entry_count and
  2988  so a re-emitted index region, and every surviving stored tile is
  2989  untouched.

WHY THE UNSTORED TILE MAKES THE FILE CLEAN — §3.1, lines 309-314:

  309  - **addressed tile / stored tile** — every tile of a layer is
  310    *addressed*. A tile is *stored in a generation* if and only if that
  311    generation's tile-index entry for it is not the sentinel (§15);
  312    unqualified *stored* means stored in the live generation. Superseded
  313    payload bytes from earlier generations do not make a tile stored.
  314    An addressed tile that is not stored reads as fill (§13).

— and the old bytes, now slack, carry no content obligation, §5.2 [R-CNT-03], lines 657-661:

  657  Writers SHOULD zero the gaps they create — the run before an aligned
  658  tile or slab run, and the pre-trailer pad. A writer that does not
  659  leaves bytes indistinguishable from stale data and forfeits byte
  660  reproducibility (Appendix G); no conformance requirement rides on
  661  slack content either way.

T4 CANNOT FIRE ON AN UNSTORED TILE — §21.4, line 3431 (the row is about a padding position in a decoded tile image; a sentinel entry has none):

  3431  | T4 | A padding position does not encode, for each channel it carries, that channel's recorded fill value | ... | verifier | certification | `[R-SER-05]` |

NO ALTERNATE EMITTER FOR THE SAME BYTES — §20.1, lines 2852-2858:

  2852  - **creator** — emits a complete file in one commit, generation 1:
  2853    the minimal conforming writer.
  2854  - **appender** — extends an existing file by commits (§9.2):
  2855    adding layers or records, superseding tiles, growing extents,
  2856    amending metadata.
  2857  - **compactor** — rewrites a file whole under a new identity
  2858    (§20.5), reclaiming slack.

AND THE RULE THE DOWNGRADE LEANED ON, WHICH DOES NOT REACH A CONFORMING FILE — line 180:

  180  - **Conforming writer.** A writer MUST emit only conforming files.
  181    `[R-CNF-05]`

SUPPORTING, that a shrink can alter nothing but the padding set (so the divergence class is exactly the padding one) — §14.2, lines 1827-1830, where decoded size and every offset derive from P and the element sizes, never from Eᵢ:

  1827  | Layout | Decoded size | Offset of value k |
  1828  |---|---|---|
  1829  | planar, numeric channel c | P · Bᶜ | k · Bᶜ |
  1830  | interleaved | P · Q | (k div C) · Q + F_{k mod C} |


## Refutation target: overflow — **DOWNGRADE_REFUTED**

**Disclosure.** I read only /Users/robertkleffner/Documents/GitHub/tarn/spec/tarn.md, via grep/sed line ranges (no docs/, ADRs, conformance/, git, or web). Specifically: §2.1 conformance definitions (lines 155-215, R-CNF-01 at 104-106, R-CNF-03/04 at 157-179, R-CNF-05 at 180-181); §4.2 R-ENC-03/R-ENC-04/R-ENC-05 (lines 385-406); §7.4 layer-record field table (lines 1014-1040, including entry_count and crc_of_crc_array rows); §11.1 R-GEO-01/R-GEO-02 (lines 1455-1490); §11.2 R-GEO-03 grid arithmetic (lines 1495-1520); §12.1 element-size table (uint16 = 2); §14.1 R-SER-01/R-SER-06, §14.2 R-SER-02 with the P·Q and P·Bᶜ table (lines 1815-1836), §14.3 R-SER-03, R-SER-07 (lines 1911-1918), §14.4 R-SER-09; §17 codec-4 text R-COD-07 and its addressed-tiles note (lines 2310-2331); §20.3's growth paragraph (lines 2960-3000); §21.1 register semantics (lines 3229-3300); register rows F3, L1, L2, L22, L27, L30, L32, L44/T12 (lines 3320-3440); §21.6 non-violations table (lines 3481-3530); §21.9 R-ERR-03/R-ERR-04 limits (lines 3583-3640). I then built a witness layer by hand with actual declared values and checked it row by row against every layer-scope register row that could plausibly bite it (L1 domain, L22 index-length formula, L27 crc_of_crc_array, L32 geometry floors, L44 lz4 cap, §21.9 guarantees) to see whether anything other than the disputed rule bars it. No commands beyond grep/sed reads; no files written.

The "not byte-level" half of the downgrade does not survive a concrete witness; the "PARTIAL" half I do not contest. Full argument is in the decisive_quotes and disclosure fields plus this summary: witness layer W (rank 2; dim y E=0, T=2^62; dim x E=100, T=1; one uint16 channel; interleaved; codec 1; entry_count=0, index slot (0,0), crc_of_crc_array=0) puts every field in domain and every undisputed derived quantity under the ceiling — P = 2^62 <= 2^63-1, N = 0, N*P = 0, C*N = 0 — while the sole over-ceiling quantity in the whole file is the §14.2 decoded size P*Q = P*B^v = 2^63, over by exactly one. Reading A: validity error at layer scope, reject-layer, verifier says nonconforming, R-CNF-05 bars emission. Reading B: R-GEO-02's "Readers MUST accept such a layer" applies, verifier certifies, a writer may emit it. The project's separator fails here because the only register row W could carry is L2, whose governing rule is the disputed R-ENC-04 itself, and §21.1 line 3250 makes the rule govern where row and rule diverge — so L2 is not an independent bar, unlike the unrelated rows (L32, L22) that disposed of earlier findings. The only text that closes the question is the §17 note at 2328, which R-CNF-01 line 104 declares non-normative, so it cannot make W nonconforming. A third consequence the passes missed: §21.9 puts the readings on opposite sides of its own diagnostic rule — under B, W "remains conforming" and any refusal "MUST be reported as a resource limit and not as a validity error"; under A the same reader must report a validity error, which the spec says "send a user to opposite remedies". Residual: reading A is clearly better-supported (R-SER-07's "function of the layer's declarations alone", R-GEO-03 checking P in an empty layer, L2's unquantified instance list, §20.3 line 2976, and the note), which justifies PARTIAL — but dominance of one reading is not the byte-level test.

**Decisive quotes.**

L398-402 (R-ENC-04, the disputed rule; note the parenthetical omits byte lengths): "MUST treat any quantity this specification defines / as a sum or product of integers obtained from a file (offsets plus / lengths, grid counts, tile counts, sample-position counts, ordinals) / whose mathematical value would exceed 2⁶³ − 1 as a validity error at / the owning scope, and MUST NOT act on a wrapped or truncated value."

L1915-1916 (R-SER-02, the only hook that brings P·Q and P·Bᶜ under it, seated in per-tile language): "These products and / sums are declaration-derived quantities under `[R-ENC-04]`."

L1915-1917 (R-SER-07): "Every decoded size, and the / value count V, is a declaration-derived quantity under / `[R-ENC-04]`."

L104-106 (R-CNF-01 — this is what disqualifies the one sentence that closes the question): "All text in this document is normative except: §1 (Introduction); any text / labeled *Note*, *Example*, or *Rationale*; and appendices identified as / non-normative."

L2328-2330 (the §17 *Note* that decides it, and is non-normative for that reason): "`[R-ENC-04]`'s overflow rule carries no such quantifier — it binds / any sum or product a file yields — so P·Q and P·Bᶜ are checked in / an empty layer even though this cap is not."

L3249-3250 (§21.1 — why register row L2 is not an independent bar, which is what breaks the separator): "but each row *restates* its governing rule, and where a / row and the rule it cites diverge, **the rule governs**."

L3367 (row L2 itself; its Governing rule cell is the disputed rule): "| L2 | A declaration-derived sum or product of a layer exceeds 2^63 - 1 although every contributing field is in domain | ... P·Q (which dominates V = P·C); P·Bᶜ; ... | reader | layer access | `[R-ENC-04]` (R-GEO-03, R-CNT-13, R-SER-02, R-SER-07) |"

L1467-1468 (R-GEO-01 — the witness's tile extents are expressly permitted): "A tile extent MAY exceed its dimension's extent (where / 0 < Eᵢ < Tᵢ the grid is then a single padded tile along that axis; / at Eᵢ = 0 the grid count is 0 and the layer addresses no tile, §11.2)."

L1473-1476 (R-GEO-02 — the permissive reading's accept obligation): "A dimension with extent 0 is valid: its grid count is 0, the layer has / zero addressed tiles, its tile index has zero entries, and its reference / array is empty. Readers MUST accept such a layer, and a read of any / region of it returns no samples."

L180-181 (R-CNF-05 — bars only *nonconforming* files, which under reading B W is not): "A writer MUST emit only conforming files. / `[R-CNF-05]`"

L3613-3619 (§21.9 R-ERR-04 — the two readings mandate mutually exclusive diagnostics for W): "A file exceeding any of these remains conforming, and a reader MAY / decline it ... a refusal / on resource grounds MUST be reported as a resource limit and not as / a validity error: the two send a user to opposite remedies"

L2322-2325 (§17's contrast case, showing the spec knew it had to state an addressed-tiles quantifier where it wanted one): "The cap is quantified over the layer's *addressed* tiles, / so a layer that addresses none — any dimension extent 0 / (`[R-GEO-02]`, §21.6) — satisfies it whatever its tile shape / declares, and codec 4 is conforming there."


## Hunt: append

**Disclosure.** Scope and method. I read only /Users/robertkleffner/Documents/GitHub/tarn/spec/tarn.md (no docs/, ADRs, conformance/, git, or web), working from §20.3 step 4 and §11.1 outward to the rules they depend on: §3.1 (stored/addressed), §5.2 + [R-CNT-21] (slack), §9.1–9.3, §11.2–11.4, §12.1–12.3, §13, §14.1–14.5, §17.2–17.3, §19.3, §20.1–20.4, and the register rows §21.2–21.6 and §21.9. For each candidate I built a concrete generation-g file, a concrete commit, and checked the resulting generation-(g+1) file against every register row that could reach it (L21, L22, L27, L44, T3, T4, T14, [R-SER-05], [R-CNT-02]/[R-CNT-21]) before asking whether the two readings differ.

Two findings survived. Both are conflicts inside §20.3 step 4's shrink paragraph against the general declaration bar three sentences above it, and in both the disputed file is conforming, so [R-CNF-05] does not collapse the two readings.

Candidates I discarded, so the absence is deliberate rather than unexamined:
- Growth of a layer whose stored edge tiles carry padding. The general bar names "the set of padding positions (§11.3)" and a growth shrinks that set, but the growth permission is an express MAY whose stated reason is exactly this case ("a position that becomes real held that channel's fill and fill is a legal sample value"), and the escape clause reaches it. One-sided; not a finding.
- The growth proviso ("provided the grown geometry stays within every bound the layer's own declarations impose"). Where a growth breaks a bound (L44, [R-ENC-04]) the resulting file carries a layer-scope register-row violation, so [R-CNF-05] bars it under a permissive reading too. Not byte-level.
- Re-declaring a channel's type at equal element size (e.g. float32 → uint32) under the bar. Textually one-sided once §14's "decode" is read as payload → decoded tile image and §12.3's [R-TYP-04] ("A sample value is its bit pattern") is applied: nothing §14 fixes changes, and the bar's own stated purpose ("Where a change does reach them it makes each stored tile it reaches nonconforming") is not engaged. A surprising permission, not an ambiguity — I judged it a design consequence and left it out rather than pad the list.
- Re-declaring uint8 → bool on an interleaved layer holding a byte outside {0x00, 0x01}: the resulting file exhibits T2, so [R-CNF-05] bars it under both readings. Not byte-level.
- Dimension-order permutation (transpose by directory edit): caught by the bar's lead-in and by "leaves every one of those tiles' stored bytes meaning exactly what they meant". Not a finding.

Confidence: finding 1 is a direct textual contradiction between two sentences about the same operation, and I regard it as solid. Finding 2 rests on a quantifier-domain divergence ("in the generation this commit supersedes" vs "any tile the new state still stores") where each reading has explicit textual support; the "it does not license one either" clause pulls toward the restrictive reading but its worked-out illustration reaches only tiles that remain stored, so the shrink-to-empty case is left open. I did not audit sections outside the assigned areas for further instances of the same tense divergence.


### A shrink that de-addresses tiles and creates padding whose stored bytes already hold fill is expressly permitted by the bar's escape clause and flatly barred by the shrink paragraph  (byte-level: YES)

**Location.** §20.3, step 4 — the shrink permission, against the general declaration bar in the same step (spec/tarn.md, the paragraph beginning "An extent MAY also **shrink**" and the sentence beginning "The test is the effect on such a tile")

The general bar in step 4 states an escape in so many words: a change is not barred where it produces "a new padding position whose stored byte already holds the fill `[R-SER-05]` fixes". The shrink paragraph opens by adopting that same bar whole ("the bar above is the whole of the test"), then states a flat prohibition with no such qualifier: a shrink that de-addresses tiles "while turning real positions into padding of a tile that remains stored is barred on that second count, whatever it does to the first."

Construction. Generation g: layer `img`, rank 2, dimensions (y: E=8, T=4) and (x: E=8, T=4); interleaved; one channel `v`, uint8, fill 0x00; codec 1, filter 1, linearization 1, A = 0, S = 0. G = (2,2), N = 4, entry_count = 4, index extent_length = 4·20 + 4 = 84, P = 16, decoded size 16, all four tiles stored at 16 bytes each. In tile (0,1) the twelve in-tile positions with x in {5,6,7} hold 0x00 — the caller's data is zero there, which is ordinary, not contrived.

The commit: E_y 8 → 4 and E_x 8 → 5. New G = (1,2), N = 2, entry_count = 2, extent_length = 2·20 + 4 = 44. Tiles (1,0) and (1,1) fall out of the addressed set and their payload extents become slack (`[R-CNT-21]`). Tile (0,1) survives, its bytes untouched, and now carries twelve padding positions — each already holding 0x00, the channel's fill.

Reading A (the escape clause): permitted. Nothing §14 fixes is altered in effect — decoded size is still 16, every value's offset is unchanged, codec and filter are unchanged, and each new padding position's stored byte already holds the fill `[R-SER-05]` fixes.

Reading B (the flat clause): barred, because the commit de-addresses some tiles while turning real positions into padding of a tile that remains stored, "whatever it does to the first".

What makes the flat clause read as a slip rather than a policy: the identical padding change is permitted under both readings when it de-addresses nothing. Shrink E_x 8 → 5 alone leaves G_x = ⌈5/4⌉ = 2, drops no tile, and creates exactly the same twelve padding positions in the same surviving tile — the flat clause's antecedent is not met, so only the escape clause governs and the commit stands. On reading B, composing that permitted change with a de-addressing the same paragraph says "never bars a commit on its own" produces a barred commit.

> "a change that leaves every one of those tiles' stored bytes meaning exactly what they meant — a filter whose mandated stride makes it the identity (`[R-COD-10]`), or a new padding position whose stored byte already holds the fill `[R-SER-05]` fixes — is not what this bars." … "An extent MAY also **shrink**, and the bar above is the whole of the test: a shrink is permitted exactly where it alters nothing §14 fixes for any tile the new state still stores. Dropping a tile out of the addressed set entirely (§11.2's grid count falls) is not itself an alteration and never bars a commit on its own — but it does not license one either, so a shrink that de-addresses some tiles while turning real positions into padding of a tile that remains stored is barred on that second count, whatever it does to the first."

*Byte-level rationale:* Apply the conforming-file distinction to the generation-(g+1) file the permissive reading lets an appender produce. It carries no register-row violation: entry_count 2 equals N = 1·2 (L21 clean); extent_length 44 equals 2·20 + ⌈2/2¹⁶⌉·4 (L22 clean); each surviving stored tile's length 16 equals its decoded size P·Q = 16·1 under codec 1 (T14, T3 clean); every padding position of tile (0,1) encodes the channel's recorded fill 0x00, so `[R-SER-05]` holds and T4 is clean; the de-addressed tiles' extents and the superseded index region are slack, whose content `[R-CNT-21]` leaves unconstrained. The file is therefore conforming, and `[R-CNF-05]` ("A writer MUST emit only conforming files") does not bar it under either reading — the emittable set is not held fixed by that rule. Nor is there another route to those bytes: a creator writes generation 1 only (`[R-WRT-02]`, `[R-LIF-02]`) and a compactor rewrites under a fresh file_id at generation 1 (§20.5), so a generation-(g+1) file bearing this file_id, these slack regions, and this smaller index region is producible only by an appender performing exactly this commit. Whether any conforming implementation may emit that byte sequence turns entirely on which of the two sentences governs. Byte-level.


### A single commit that shrinks a layer's extent to 0 and re-declares its tile extents is barred by the bar's prior-generation tense and permitted by the shrink paragraph's new-state quantifier  (byte-level: YES)

**Location.** §20.3, step 4 — the general declaration bar's tense against the shrink paragraph's quantifier and the empty-layer permission (spec/tarn.md, "The tense is the prior generation's …" vs "any tile the new state still stores" and "A layer that stores no tile MAY be re-declared freely"); corroborated by §11.1's Rationale

The general bar quantifies over tiles "that layer stores **in the generation this commit supersedes**", and says so twice over: "The tense is the prior generation's … a commit does not escape this by unstoring in the same breath". The shrink paragraph, claiming to adopt that bar unchanged, restates it with the opposite quantifier — "any tile **the new state still stores**" — and the same step grants that "A layer that stores no tile MAY be re-declared freely", with no tense attached. A shrink to zero extent is exactly where the two domains come apart, because de-addressing removes tiles from the new state's stored set without superseding them.

Construction. Generation g: layer `staging`, rank 1, dimension (i: E=1024, T=256); interleaved; one channel `v`, float64 (B = Q = 8); codec 1, filter 1. G = (4), N = 4, entry_count = 4, P = 256, decoded size 2048, all four tiles stored.

The commit: set E_i = 0 and, in the same commit, T_i = 512. The four payload extents and the old index region become slack; entry_count becomes 0, the index extent slot becomes (0, 0), and crc_of_crc_array is 0.

Reading A (prior-generation tense): barred. Changing T from 256 to 512 alters the decoded size — 2048 → 4096 — for tiles the superseded generation stored, which the bar lists expressly; and the shrink paragraph's own "it does not license one either" says de-addressing supplies no escape. The caller must write a new layer or a fresh file (`[R-LIF-01]`, §20.5).

Reading B (new-state quantifier): permitted. "[A] shrink is permitted exactly where it alters nothing §14 fixes for any tile the new state still stores" — a biconditional; the new state stores no tile, so the condition holds vacuously. The empty-layer permission points the same way if read in the new state's tense, and §11.1's Rationale chains the two steps together in that order: a shrink is "permitted where it drops tiles out of the addressed set, whose extents then become slack. A layer that stores nothing may be re-declared freely." (§11.1's Rationale is non-normative and defers — "§20.3 states normatively, and governs" — so I rest the finding on §20.3's own two sentences and cite §11.1 only as corroboration that the permissive chain is the one a reader assembles.)

The anti-escape clause does not close this. It names one mechanism — "superseding every tile of a layer and re-declaring it are one operation" — and superseding is not what happens here: §3.1 makes a tile stored iff its entry is not the sentinel, and a de-addressed tile has no entry at all. Its worked illustration likewise reaches only "a tile that remains stored", of which there are none.

The disputed set is exactly the one-commit combination. Shrinking to E = 0 alone is permitted under both readings, and a later commit at generation g+2 re-declaring T is permitted under both, since by then the superseded generation stored nothing — but that two-commit route yields a different byte sequence, carrying an extra directory, pad and trailer and a higher generation counter.

A sharper variant of the same disagreement, if it helps size the stakes: keep codec 4 and re-declare T_i = 2²⁸, so P·Q = 2³¹ exceeds `[R-COD-07]`'s 0x7E000000 cap. §17.2's note blesses the result — "a layer that addresses none … satisfies it whatever its tile shape declares, and codec 4 is conforming there" — so reading B lets an appender leave a conforming live file whose lz4 declaration no future growth may realize, while reading A forbids the commit outright.

> "The tense is the prior generation's (§3.1 defines *stored* against a generation), so a commit does not escape this by unstoring in the same breath: superseding every tile of a layer and re-declaring it are one operation, and this bars it." … "A layer that stores no tile MAY be re-declared freely, which is what schema-first creation needs (§11.1)" … "a shrink is permitted exactly where it alters nothing §14 fixes for any tile the new state still stores." … §11.1 Rationale: "a shrink is barred wherever it alters what §14 fixes for a tile the new state still stores, and permitted where it drops tiles out of the addressed set, whose extents then become slack. A layer that stores nothing may be re-declared freely."

*Byte-level rationale:* The generation-(g+1) file the permissive reading yields is conforming, so `[R-CNF-05]` does not bar it under both readings and the emittable set genuinely moves. Checked row by row: a dimension with extent 0 is valid and the layer addresses no tile (`[R-GEO-02]`, §21.6); entry_count 0 with an index extent slot of (0, 0) is the combination L22 requires, the nonzero-slot-with-entry_count-0 and (0,0)-with-entry_count>0 cases being the violations; crc_of_crc_array is 0, so L27 is clean; no stored tile exists, so no tile-scope row (T3, T4, T14) can be exhibited; the orphaned payload extents and the superseded index region are slack, whose content `[R-CNT-21]` leaves unconstrained and which only compaction reclaims; and in the lz4 variant L44 is clean because `[R-COD-07]`'s cap is quantified over addressed tiles, which §17.2's note states expressly. Nothing in the resulting bytes is a register-row violation — the disagreement is purely about whether an appender is permitted to reach them in one commit. And the bytes are reachable no other way: a creator emits generation 1 (`[R-WRT-02]`), a compactor rewrites under a fresh file_id at generation 1 (§20.5), and the permitted two-commit route lands at generation g+2 with an extra directory, pad and trailer, a different byte sequence. Byte-level.


## Hunt: compact

**Disclosure.** Method: read only /Users/robertkleffner/Documents/GitHub/tarn/spec/tarn.md (§2.3–2.5, §4, §5, §6, §7, §8, §9, §12–§17, §19, §20, §21, Appendix G). Built two concrete artifacts on paper and checked every claim the target sections make against them: (a) a compaction of a two-entry, one-layer file, and (b) a full reproducible-writer output (front block at [0,16), one stored tile, index region, directory, pad, trailer, F = 448) walked field by field against Appendix G items 1–10.

Checked and found clean, so not filed: §21.8's totals — I counted the register mechanically (21.2 = 36 rows, 21.3 = 49, 21.4 = 26, 21.5 = 10 → 121 rows; semicolon-counted instance cells, "—" as one → 58 + 116 + 57 + 44 = 275), which matches §21.8's "121 conditions over 275 instances" and every per-subsection count. §21.1's specialization list (F1 of F6/F8, F35 of F36, L24 of L25) holds against the tables, and taking the narrower row's detector is the stricter reading in each pair, so no reader obligation moves. Appendix G item 6's "all equal fill" is pinned to byte equality by [R-TYP-04] ("Wherever this specification treats two sample or fill values as the same value, it means their encoded bytes are identical"), so a NaN fill does not open a store-vs-sentinel fork; item 2's hash input and its "last eight bytes in output order ... read little-endian" are circularity-free and byte-determinate; item 3's placement rule leaves my worked output with exactly one gap (the pre-trailer pad), zeroed.

Deliberately not filed as findings, disclosed here instead:
- Appendix G item 2's "Any other fixed nonzero value is substituted in the measure-zero case that they are all zero" is a genuinely unclosed degree of freedom in a profile whose stated job is closing them — two profile writers sharing a named hash would emit different file_id bytes — but no construction is available (it needs a 2^-64 digest), so it fails the prompt's concrete-construction bar.
- §21.7's second list ("A second set of obligations is omitted from the register because a single file exhibits no witness of their violation") names [R-LIF-01], [R-LIF-03], [R-GEO-06]/[R-SER-01], [R-CNT-13], [R-CNT-18], §20.3 step 4 and [R-ENC-06], but not [R-WRT-06]'s fresh-file_id/generation-1 or [R-WRT-07]'s reference-array equality, which are witnessless in exactly the same way. That is a documentation-completeness gap against §21.1's "§21.7 the account, by class, of what fails it"; no byte sequence changes hands either way, so it is not byte-level and I did not pad the list with it.
- §21.7's "a change that reaches the decoded size or the codec instead is witnessed by T3 or T14" is under-inclusive for a codec change (1→3 is witnessed by T17, 1→2 by T24/T25), but naming fewer rows does not change any detection obligation.


### A carried-forward structurally-invalid index entry has two different, equally licensed output offsets  (byte-level: YES)

**Location.** §20.5, the index-region regeneration parenthesis (paragraph tagged `[R-WRT-07]`)

§20.5 tells a compactor two contradictory things about the same eight bytes. "Carried forward as it stands" means the entry's 20 bytes are reproduced; "its offset re-pointed like any other" means the offset field is rewritten to where the addressed bytes now live. For an entry §15.3 classifies reject-tile on a structural ground there is nothing to re-point to: [R-IDX-03] says such an entry "contributes no stored extent" to the verifier rows and "none to `[R-LIF-08]`'s coverage walk, so any bytes it nominally addressed that no other claimant claims fall to slack". The two readings diverge in bytes whenever the entry's offset aliases a structure that does move.

Construction. Input: one layer `a`, rank 1, extent 64, tile extent 32, one uint8 interleaved channel, codec 1, filter 1, A = 0, S = 0, so entry_count = 2 and the decoded tile size is 32. Entry 0 is a stored tile at offset 4096, length 32, crc C0. Entry 1 is offset 4096, length 0, crc 0 — §15.3's "length = 0 (non-sentinel)" row, a *structural* reject-tile (register row T10). The index region is 2·20 + 4 = 44 bytes at 8192. The coverage walk claims the front block, [4096, 4128), the index region, the directory and the trailer; entry 1 claims nothing, so no overlap row fires and the file's only violation is T10. [R-WRT-09]'s depth — "the open (§19.1), each retained layer's record (§19.3) and full index chain (`[R-IDX-04]`), and each relocated extent's checksum, including every stored tile's entry crc" — passes, and §20.5 says in terms that this entry "is not one `[R-WRT-06]` obliges a compactor to refuse". So the compactor proceeds.

Output: tile 0 relocated to [16, 48), index region at [48, 92), directory at 92, F = 256. Entry 0 is offset 16, length 32, crc C0 ("entry offsets new; entry lengths, entry crcs ... unchanged"). Entry 1 is either `00 10 00 00 00 00 00 00` (offset 4096, "as it stands") or `10 00 00 00 00 00 00 00` (offset 16, "re-pointed like any other" — the bytes at 4096 moved to 16). That is 8 differing bytes at index-region byte 20, a differing segment CRC at region byte 40, a differing crc_of_crc_array in the layer record, and a differing directory CRC. Both outputs still trip T10, so "a violation latent in a structure it carries forward verbatim travels into its output" is satisfied either way and nothing else in §20.5, §15.3 or §16.2 separates them — L41 explicitly treats such an entry as transparent to run continuity, so even a slab declaration does not pin it.

> an entry §15.3 classifies reject-tile on a structural ground is carried forward as it stands, its offset re-pointed like any other — `[R-WRT-09]`'s checks reach the index chain and each stored tile's entry crc, not an entry's own value domain, so such an entry is not one `[R-WRT-06]` obliges a compactor to refuse

*Byte-level rationale:* Applying the conforming-file distinction explicitly: the disputed output is NOT a conforming file — it carries register row T10 at tile scope under both readings — which normally means [R-CNF-05] bars every conforming writer from emitting it under both readings and the emittable set does not move. That premise fails here, and this is the documented exception. [R-CNF-05] binds the *writer* class; a compactor is the updater class under [R-CNF-06] ("MUST satisfy every writer requirement for the bytes it produces"), and §20.1/§20.5 expressly license a conforming compactor to emit this nonconforming output: "a violation latent in a structure it carries forward verbatim travels into its output (`[R-WRT-01]`)", with §20.5 stating outright that this entry is not one it must refuse. So both byte sequences are emittable by a conforming actor, and resolving the sentence forbids one of them. The move is real in the global sense too: a length-0 index entry is a byte pattern no creator may ever emit ([R-CNF-05]), so this compactor licence is the only thing that puts either sequence in the emittable set, and only one of the two survives resolution.


### A compactor that detects a violation in a droppable record: refuse outright, or drop the record and emit a clean file?  (byte-level: YES)

**Location.** §20.5, the refusal sentence (paragraph tagged `[R-WRT-06]`), read against §20.4's MU = 0, PE = 0 row

The clause "a record §20.4 does let it drop is no exception" reads two ways, and the two give a conforming compactor opposite instructions.

Construction. Input: front block; one clean layer `a` with one stored tile and its index region; one top-level record of type 0x0003 — the reserved range of §10.2 — with flags = 0 (MU = 0, PE = 0), inline_length 4, extent slot (0, 0); directory; pad; trailer at generation 3, file_id X. The file's only violation is F36 ("A top-level record carries a type value from the reserved range 0x0003-0x7FFF ... emitting one is a violation whatever its MU bit"), whose Detector is *verifier* at *certification*. F36 is outside [R-WRT-09]'s depth, so a compactor need not look — but a verifier-grade one does, and has now "detected" it. §20.4's table, which applies because the compactor does not implement an unassigned type, says of MU = 0 / PE = 0: "Retain byte-identical, or drop it — its extent becoming slack. ... A compactor may drop it whenever it rewrites the file." §21.6 confirms a reserved-range MU = 0 record is "read the same way" as an experimental one, i.e. "Ignored, and preserved or dropped per its PE bit".

Reading A — "no exception" closes only the *keep-it* option: the compactor drops the record, and its output (front block; tile at 16; index region; a directory holding the layer record alone; pad; fresh file_id Y; generation 1) carries no violation at all and is a conforming file.
Reading B — "no exception" forecloses dropping as a cure, so the detection obliges refusal and no output exists for this input.

The trailing clause pulls both ways: "dropping being available only where that table licenses it" is either the ground for reading A (the table does license it here) or the reason reading B gives for treating the drop licence as a preservation rule and not a repair power. Nothing else in §20.4, §20.5 or §21.6 addresses a *detected* violation in a droppable record.

> MUST NOT emit a file carrying a violation it has detected: it can neither re-emit the structure corrected (`[R-WRT-05]`), nor keep it and call the output clean — and a record §20.4 does let it drop is no exception, dropping being available only where that table licenses it.

*Byte-level rationale:* Applying the conforming-file distinction explicitly: the disputed file is the compacted output, and it is conforming — dropping the record removes F36 and leaves no register-row violation anywhere in it, so [R-CNF-05] bars nobody from emitting it and the "barred under both readings" branch does not apply. Only reading A permits the actor to produce it; under reading B a conforming compactor must refuse and those bytes never exist. By the stated criterion — conforming disputed file, produced under one reading only — the emittable set moves. One honest caveat on the strength of that: unlike the first finding, the same byte sequence is independently emittable by a creator building the file from scratch, so a scorer who reads "emittable set" as the global set of byte sequences rather than as what this actor may produce from this input would rate this lower than byte-level. What is unambiguously at stake either way is whether a compactor produces a file or refuses.
