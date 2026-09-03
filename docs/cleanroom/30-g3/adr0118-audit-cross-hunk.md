# Cross-hunk consistency audit — working transcript (round 30)

## Disclosure (running)
Read: spec/tarn.md in full (lines 1-4739, via Read in chunks), hunk-01.diff .. hunk-21.diff
(each by explicit path; directory not listed; full.diff not read).
Context placed before I began, NOT used as evidence: project CLAUDE.md pointer (AGENTS.md not opened),
an auto-memory index naming four TARN notes (not opened), a git-status block naming five recent
commit subjects. All disregarded.

## Grouping by rule touched (my own, from the text)

A. The detectability test (unwitnessed / detectable): h12 (§21.1 restatement), h17 (§21.7 definition),
   h18 (§21.7 R-ENC-06 paragraph), and h1 (§2.4: verifier duty "runs to MUST-level conditions, which §21
   inventories") which leans on what §21 inventories.
B. version_major = 0 / F18: h14 (§21.2 preamble), h15 (F18 row), h16 (§21.6 prose). Three places, one condition.
C. The §14 bar and its carve-out (growth / shrink): h7 (the list, step 4), h8 (growth + carve-out),
   h9 (shrink no-witness), h3 (§11.1 Rationale block — the labelled earlier account); later subsection
   accounts: §20.3 Example (c), §23.1 R-PRV-01 (untouched).
D. Slab declaration upkeep: h4 (R-SLB-04) — siblings §20.3 step 4 closing sentence, §16.2 Notes, §20.5 R-WRT-07.
E. Compaction: h10 (version_minor witness), h11 (which index regions are regenerated) — sibling §20.5 Example.
F. Parse at fixed widths: h6 (§19.3 cites R-ENC-06), h18 (§21.7 discusses R-ENC-06) — the stated rule R-ENC-06 §4.2 untouched.
G. User-metadata verifier decline: h5 (R-MTA-09 "either bound above") — sibling §21.5 preamble, R-CNF-11.
H. §21.9: h19 (decline scope wording), h20 (chosen limits count) — sibling §18.2 Note (decline at whole file).
I. Recovery report: h2 (R-LIF-06).
J. The one resolved byte: h13 (§21.1 → R-TYP-04) — siblings §12.3, §19.4 step 8, Appendix H.
K. Appendix G item 5 filter identity: h21.

Hunk-header verification: every hunk's "nearest preceding heading" matched the body I read at the stated lines
(h1 §2.4 line 324; h2 §9.6 1441; h3 §11.1 1638; h4 §16.2 2320; h5 §18.2 2662; h6 §19.3 2953; h7-9 §20.3
3152/3222/3261; h10-11 §20.5 3479/3491; h12-13 §21.1 3588/3653; h14-15 §21.2 3664/3685; h16 §21.6 3888;
h17-18 §21.7 3915/3948; h19-20 §21.9 3998/4043; h21 App. G 4601). No mismatch.

## Sweeps
== SWEEP [permanently invalid] hits=0
== SWEEP [invalid in every] hits=1
   line~1538: …536⟩ | metadata encoding (§18.2) | u8 | 1, 2 | 3–0x7F | ≥ 0x80 | ⟨1537⟩ ⟨1538⟩ Value 0 is invalid in every space above. Two spaces carry no ⟨1539⟩ experimental range: channel layout, whose `u8` fi…
== SWEEP [every format major version] hits=3
   line~249: …1 when, and ⟨248⟩ only when, the invariant it violates is one `[R-CNT-24]` fixes in ⟨249⟩ every format major version. Reach is per condition because a single ⟨250⟩ requirement can state several: `[R-CNT-06]…
   line~761: …⟨759⟩ #### 6.1 Front signature block ⟨760⟩ ⟨761⟩ Bytes [0, 16) of every file, constant in every format major version: ⟨762⟩ ⟨763⟩ | Offset | Size | Value | Class | ⟨764⟩ |---|---|---|---| ⟨765⟩ | 0 | 8 | `8…
   line~862: …60⟩ all feature gating is structural (records, enums, flags). `[R-CNT-07]` ⟨861⟩ ⟨862⟩ In every format major version, permanently: the final 64 bytes of a ⟨863⟩ file contain the trailer magic at F − 64, ver…
== SWEEP [declares no major] hits=3
   line~3664: …her row. F18 is not an exception but a case outside the ⟨3664⟩ premise: version_major = 0 declares no major at all, so `[R-CNF-13]`'s ⟨3665⟩ premise is unmet and `[R-CNT-07]` governs (§21.6). ⟨3666…
   line~3685: …en | `[R-CNT-06]` (R-LIF-04, R-CNT-10) | ⟨3685⟩ | F18 | Trailer version_major is 0, which declares no major at all | version_major | reader | open | `[R-CNT-07]` | ⟨3686⟩ | F19 | Any bit of the fla…
   line~3888: …ase is the neighbouring condition ⟨3888⟩ that *is* a violation — version_major = 0, which declares no major at ⟨3889⟩ all (F18, `[R-CNT-07]`), and a *reserved*-range ⟨3890⟩ type, whose emission `[R…
== SWEEP [sole resolved] hits=1
   line~4691: …fill for a rejected tile (§2.4); returns sample bit patterns unaltered ⟨4691⟩ (§3.2), the sole resolved byte being a nonconforming interleaved ⟨4692⟩ boolean it chooses to return rather than re…
== SWEEP [resolved byte] hits=1
   line~4691: …for a rejected tile (§2.4); returns sample bit patterns unaltered ⟨4691⟩ (§3.2), the sole resolved byte being a nonconforming interleaved ⟨4692⟩ boolean it chooses to return rather than reject …
== SWEEP [one byte a reader resolves] hits=1
   line~3654: …lue rather than serving it through, which is why ⟨3654⟩ `[R-TYP-04]` (§12.3) makes it the one byte a reader resolves rather ⟨3655⟩ than serves through. ⟨3656⟩ ⟨3657⟩ #### 21.2 File-scope violations ⟨3658⟩ ⟨…
== SWEEP [Two do not] hits=0
== SWEEP [Some do not] hits=1
   line~4043: …42⟩ domain, and the rest from arithmetic over structures a generation ⟨4043⟩ cannot omit. Some do not: the 512 floor on A is a number chosen ⟨4044⟩ here, fixed at the legacy sector size (§16.…
== SWEEP [relocated tile-index region] hits=1
   line~3536: …Every stored tile's bytes survive byte-for-byte, as does every ⟨3536⟩ record extent but a relocated tile-index region — itself a record ⟨3537⟩ extent (§5.2), and the one kind this operation regenerates rathe…
== SWEEP [relocated index region] hits=1
   line~3540: …d. The ⟨3539⟩ reference arrays are identical; extent slots are re-pointed and ⟨3540⟩ each relocated index region is regenerated — the ′ marks ⟨3541⟩ (`[R-WRT-07]`). Placement is what changes, which is w…
== SWEEP [any of whose stored extents] hits=0
== SWEEP [declarations exceed] hits=0
== SWEEP [stated or derived] hits=1
   line~3998: … reader MAY ⟨3997⟩ decline it — at the whole file, or at the narrowest scope whose ⟨3998⟩ stated or derived quantities exceed what it can serve, a layer or a ⟨3999⟩ tile. Software that declines **o…
== SWEEP [narrower scope] hits=1
   line~2685: …4]` does ⟨2684⟩ so at the whole file, a document having no declared size and so no ⟨2685⟩ narrower scope whose declarations that rule can measure. A refusal ⟨2686⟩ on that ground is reported as …
== SWEEP [same check] hits=1
   line~3590: …3589⟩ specification obliges a reader or a verifier to perform, not ⟨3590⟩ necessarily the same check for each ⟨3591⟩ — but each row *restates* its governing rule, and where a ⟨3592⟩ row and …
== SWEEP [witness in the output] hits=1
   line~3479: …es. Otherwise version_minor follows `[R-CNT-26]`'s ⟨3479⟩ floor. Neither obligation has a witness in the output alone, save ⟨3480⟩ that where the output carries no later-minor feature the compactor ⟨34…
== SWEEP [slab-declared] hits=1
   line~2321: …rtition, the byte placement of any run, or the slab ⟨2321⟩ declaration itself, of a layer slab-declared in either the ⟨2322⟩ superseded or the new generation, MUST either ⟨2323⟩ re-establish th…
== SWEEP [last zero grid] hits=0
== SWEEP [only remaining] hits=1
   line~1638: … moves them (§20.3, `[R-WRT-04]`) — ⟨1638⟩ the growth that raises a zero-extent layer's **only remaining** ⟨1639⟩ zero grid count included. ⟨1640⟩ ⟨1641⟩ #### 11.2 Grid arithmetic ⟨1642⟩ ⟨1643⟩ …
== SWEEP [either bound] hits=1
   line~2662: …he declared size it does not. A **verifier** that declines to decode a document on ⟨2662⟩ either bound above cannot establish that document's conformance and MUST NOT certify ⟨2663⟩ the file, …
== SWEEP [the bound above] hits=1
   line~2631: …-size exception holds because a document has no declared ⟨2630⟩ size, ⟨2631⟩ which is why the bound above is the reader's own and not the ⟨2632⟩ file's. The frame's declared `Window_Size` is unco…
== SWEEP [of any sample within] hits=0
== SWEEP [of any value within] hits=0
== SWEEP [inventories] hits=1
   line~325: …o ⟨324⟩ check every file-level requirement runs to MUST-level conditions, ⟨325⟩ which §21 inventories, and a SHOULD deviation is reported where the ⟨326⟩ verifier observes it and not hunted f…
== SWEEP [MUST-level] hits=2
   line~321: …iation from a SHOULD is not a violation for this ⟨321⟩ purpose: §21's register enumerates MUST-level conditions only, and a ⟨322⟩ verifier reports a SHOULD deviation as an advisory that does…
   line~324: …r owes no search for one: §2.3's duty to ⟨324⟩ check every file-level requirement runs to MUST-level conditions, ⟨325⟩ which §21 inventories, and a SHOULD deviation is reported where the ⟨32…
== SWEEP [field widths] hits=1
   line~3945: … requirement that states ⟨3945⟩ **no condition a file can exhibit**. `[R-ENC-06]`'s fixed field widths are not a state a file ⟨3946⟩ can be in — the parse is always at the widths this specific…
== SWEEP [every tile it touches] hits=0
== SWEEP [does not fix] hits=2
   line~4585: …such gap is zero — `[R-CNT-03]`'s advice, taken as a requirement ⟨4585⟩ here: order alone does not fix bytes while the space between ⟨4586⟩ structures is free in either extent or content. ⟨458…
   line~4602: …it changes ⟨4601⟩ the stored bytes of any tile whose decoded image the permutation ⟨4602⟩ does not fix, and a fixed image is no evidence of which filter ⟨4603⟩ produced it. **Fixed declared ti…
== SWEEP [how many it rejected] hits=1
   line~1441: … tool continues the probe past it, and MUST report the ⟨1441⟩ candidate it settled on and how many it rejected, or, where no ⟨1442⟩ candidate survived re-verification, that none did and how many it ⟨1…
== SWEEP [carve-out] hits=3
   line~3223: …s, that ⟨3222⟩ channel's fill (§14.5), and fill is a legal sample value. The bar's ⟨3223⟩ carve-out does not reach a growth: it covers a position whose ⟨3224⟩ stored byte already holds the …
   line~3226: …⟩ to be padding, so this is an exception the permission states ⟨3226⟩ rather than one the carve-out supplies. It holds provided the ⟨3227⟩ grown geometry stays within every bound the ⟨3228⟩…
   line~3254: … ⟨3253⟩ it. What counts as such an alteration is the §14 bar and nothing ⟨3254⟩ else, its carve-out included — a new padding position whose stored ⟨3255⟩ byte already holds the fill `[R-SER…
== SWEEP [no witness] hits=1
   line~3262: … falls on a tile the new state no ⟨3262⟩ longer stores is precisely where the §14 bar has no witness, the ⟨3263⟩ live state being clean, which is why the rule is stated here and ⟨3264⟩ not l…
== SWEEP [ceases to be padding] hits=0
== SWEEP [the slab declaration itself] hits=0
== SWEEP [pad bits] hits=11
   line~2039: …he last value (bit positions ⟨2039⟩ P mod 8 through 7, when P mod 8 ≠ 0) are the tile's **pad bits**; ⟨2040⟩ their content is fixed by `[R-SER-05]` and they never encode ⟨2041⟩ values. Eve…
   line~2046: …riters (§14.5), never a reader's ⟨2044⟩ decode path. `[R-SER-03]` ⟨2045⟩ ⟨2046⟩ **Note.** Pad bits are not padding positions (§11.3). A padding ⟨2047⟩ position is a whole sample position o…
   line~2048: …ion is a whole sample position outside the layer's extents, ⟨2048⟩ arising in any layout; pad bits are a packed plane's final-byte ⟨2049⟩ unused high bits, arising only when P is not a mul…
   line~2050: …only when P is not a multiple of 8. A ⟨2050⟩ plane can have many padding positions and no pad bits — §14.5 ⟨2051⟩ gives both their content. ⟨2052⟩ ⟨2053⟩ **Example.** A planar bool tile, t…
   line~2056: …5` (bits 0–7 = values 0–7), byte 1 carries values 8–9 in bits ⟨2056⟩ 0–1 (`0x01`) and six pad bits. With the channel's fill false the ⟨2057⟩ tile decodes as `55 01`; with fill true, `55 FD…
   line~2057: …ith the channel's fill false the ⟨2057⟩ tile decodes as `55 01`; with fill true, `55 FD` (pad bits 2–7 ⟨2058⟩ set). ⟨2059⟩ ⟨2060⟩ Whichever of §14.2 or §14.3 defines a tile's decoded size,…
   line~2087: …ose planar. At P = 1 the two are the same length and ⟨2087⟩ `[R-SER-05]` fixes the planar pad bits to the channel's fill, so ⟨2088⟩ the images coincide exactly when that fill is false. ⟨20…
   line~3152: …or its stored bytes or how they decode — ⟨3152⟩ the set of padding positions (§11.3), the pad bits `[R-SER-03]` ⟨3153⟩ gives a packed planar bool plane, and the content `[R-SER-05]` ⟨3154⟩…
   line~3905: …8]` narrow this only where content is structurally ⟨3905⟩ constrained: padding positions, pad bits, and boolean bytes. ⟨3906⟩ Nothing here authenticates, either (§4.5). None of these is a …
   line~4696: …⟨4695⟩ fill for every channel (`[R-TYP-06]`, §13.1); fill-encodes edge ⟨4696⟩ padding and pad bits (`[R-SER-05]`, §14.5); emits interleaved boolean ⟨4697⟩ values as only 0x00 or 0x01 (`[R-…
   line~4728: …lignment and slab invariants (§16); decoded-content obligations — ⟨4728⟩ padding samples, pad bits and interleaved boolean bytes (§14.5, §14.3, ⟨4729⟩ §14.2); ⟨4730⟩ user-metadata member o…
== SWEEP [precisely where] hits=1
   line~3262: …s not one. A shrink whose damage falls on a tile the new state no ⟨3262⟩ longer stores is precisely where the §14 bar has no witness, the ⟨3263⟩ live state being clean, which is why the rule is s…
== SWEEP [checkable against] hits=1
   line~3481: … later-minor feature the compactor ⟨3481⟩ does not implement, its stored version_minor is checkable against ⟨3482⟩ the floor `[R-CNT-26]` states. ⟨3483⟩ A compactor MUST refuse to compact a file ca…
== SWEEP [declares no major at all] hits=2
   line~3664: …her row. F18 is not an exception but a case outside the ⟨3664⟩ premise: version_major = 0 declares no major at all, so `[R-CNF-13]`'s ⟨3665⟩ premise is unmet and `[R-CNT-07]` governs (§21.6). ⟨3666⟩ ⟨3667…
   line~3685: …en | `[R-CNT-06]` (R-LIF-04, R-CNT-10) | ⟨3685⟩ | F18 | Trailer version_major is 0, which declares no major at all | version_major | reader | open | `[R-CNT-07]` | ⟨3686⟩ | F19 | Any bit of the flags inco…
== SWEEP [no major] hits=4
   line~278: …64, F − 4). F5 does not reach although its subject is the ⟨278⟩ physical file size, which no major can redefine: the 128-byte floor ⟨279⟩ it asserts is derived from a directory of at least…
   line~3664: …F18 is not an exception but a case outside the ⟨3664⟩ premise: version_major = 0 declares no major at all, so `[R-CNF-13]`'s ⟨3665⟩ premise is unmet and `[R-CNT-07]` governs (§21.6). ⟨3666…
   line~3685: …CNT-06]` (R-LIF-04, R-CNT-10) | ⟨3685⟩ | F18 | Trailer version_major is 0, which declares no major at all | version_major | reader | open | `[R-CNT-07]` | ⟨3686⟩ | F19 | Any bit of the fla…
   line~3888: …e neighbouring condition ⟨3888⟩ that *is* a violation — version_major = 0, which declares no major at ⟨3889⟩ all (F18, `[R-CNT-07]`), and a *reserved*-range ⟨3890⟩ type, whose emission `[R…
== SWEEP [which need not be the same] hits=1
   line~3916: … file exhibiting it is separated from every ⟨3916⟩ file that does not by some such check, which need not be the same ⟨3917⟩ check for every one of them. The two are stated over the ⟨3918⟩ same subject, and …
== SWEEP [not necessarily the same] hits=0
## Sweeps, rerun on a marker-free normalisation (phrases spanning a wrap now match)
== SWEEP [permanently invalid] hits=0
== SWEEP [invalid in every format] hits=0
== SWEEP [permanently invalid in every] hits=0
== SWEEP [Two do not] hits=0
== SWEEP [any of whose stored extents] hits=1
   line 3491: …record per §20.4, except that relocation re-points extent slots, regenerates each tile-index region any of whose stored extents the output relocates (entry offsets new; entry lengths, entry crcs, and sentinel entries unchanged;…
== SWEEP [each relocated tile-index region] hits=0
== SWEEP [declarations exceed] hits=0
== SWEEP [whose declarations] hits=1
   line 2685: …`[R-ERR-04]` does so at the whole file, a document having no declared size and so no narrower scope whose declarations that rule can measure. A refusal on that ground is reported as a resource limit, not as corruption.…
== SWEEP [last zero grid] hits=0
== SWEEP [only remaining zero] hits=0
== SWEEP [of any sample within] hits=0
== SWEEP [of any value within] hits=1
   line 3154: …ed planar bool plane, and the content `[R-SER-05]` fixes at both, the decoded size, the byte offset of any value within the decoded tile image, the sample type each value in the image is read under, or the codec and fil…
== SWEEP [every tile it touches] hits=0
== SWEEP [whose decoded image the permutation] hits=1
   line 4601: …s a single group, n = L/s being 1 (`[R-COD-10]`); elsewhere it changes the stored bytes of any tile whose decoded image the permutation does not fix, and a fixed image is no evidence of which filter produced it. **Fixed declared tile e…
== SWEEP [ceases to be padding] hits=1
   line 3224: …each a growth: it covers a position whose stored byte already holds the fill it keeps, not one that ceases to be padding, so this is an exception the permission states rather than one the carve-out supplies. It holds pro…
== SWEEP [the slab declaration itself] hits=1
   line 2320: …ater whose commit changes the stored-tile set, the run partition, the byte placement of any run, or the slab declaration itself, of a layer slab-declared in either the superseded or the new generation, MUST either re-establish …
== SWEEP [not necessarily the same] hits=1
   line 3589: …very file that does not by some check this specification obliges a reader or a verifier to perform, not necessarily the same check for each — but each row *restates* its governing rule, and where a row and the rule it cites …
== SWEEP [need not be the same] hits=1
   line 3916: … where some file exhibiting it is separated from every file that does not by some such check, which need not be the same check for every one of them. The two are stated over the same subject, and each quantifier is the o…
== SWEEP [sole resolved byte] hits=1
   line 4691: …nd never returns fill for a rejected tile (§2.4); returns sample bit patterns unaltered (§3.2), the sole resolved byte being a nonconforming interleaved boolean it chooses to return rather than reject (`[R-SER-08]`, §1…
== SWEEP [calls it the sole] hits=0
== SWEEP [Neither obligation has a witness] hits=1
   line 3479: …rror of the overstatement `[R-CNT-26]` names. Otherwise version_minor follows `[R-CNT-26]`'s floor. Neither obligation has a witness in the output alone, save that where the output carries no later-minor feature the compactor does n…
== SWEEP [the two capability refusals] hits=1
   line 4000: …und** a file whose every quantity lies within the table is not a conforming reader (`[R-CNF-03]`) — the two capability refusals §21.6 names, a foreign format major and an unimplemented MU = 1 type, are not this ground — the gua…
== SWEEP [capability refusal] hits=1
   line 4001: …file whose every quantity lies within the table is not a conforming reader (`[R-CNF-03]`) — the two capability refusals §21.6 names, a foreign format major and an unimplemented MU = 1 type, are not this ground — the gu…
== SWEEP [conforming files a reader nevertheless refuses] hits=1
   line 3872: …nd it is unchanged: neither is a reason for a reader to reject anything. Two structural cases are **conforming files a reader nevertheless refuses**. The first is **version_major naming a major this reader does not implement**: the reader rejects…
== SWEEP [MUST-level conditions, which] hits=1
   line 324: …ation. A verifier owes no search for one: §2.3's duty to check every file-level requirement runs to MUST-level conditions, which §21 inventories, and a SHOULD deviation is reported where the verifier observes it and not hunted f…
== SWEEP [the MUST-level conditions §21] hits=0
== SWEEP [separated by such a check] hits=0
== SWEEP [separated from every file that does not] hits=2
   line 3588: …s and §21.7 states the test for: a condition is detectable exactly where some file exhibiting it is separated from every file that does not by some check this specification obliges a reader or a verifier to perform, not necessarily the sam…
   line 3915: … a verifier to perform. It is **detectable** in the contrary case: where some file exhibiting it is separated from every file that does not by some such check, which need not be the same check for every one of them. The two are stated over…
== SWEEP [no condition a file can exhibit] hits=2
   line 2628: …e (§21.7) — while the bar on sizing a buffer binds a reader rather than the document, and so states no condition a file can exhibit at all. The decoded-size exception holds because a document has no declared size, which is why the …
   line 3945: …iolation this document names. Distinguish an unwitnessed condition from a requirement that states **no condition a file can exhibit**. `[R-ENC-06]`'s fixed field widths are not a state a file can be in — the parse is always at the …
== SWEEP [wherever the shifted value] hits=1
   line 3948: …tten at any other yields different values at them, caught by the rows for the fields that hold them wherever the shifted value is one those rows reject. Nothing is omitted from the register on its account, there being no condi…
== SWEEP [declares no major] hits=3
   line 3664: …major — and no other row. F18 is not an exception but a case outside the premise: version_major = 0 declares no major at all, so `[R-CNF-13]`'s premise is unmet and `[R-CNT-07]` governs (§21.6). | # | Condition | Inst…
   line 3685: …ger | reader | open | `[R-CNT-06]` (R-LIF-04, R-CNT-10) | | F18 | Trailer version_major is 0, which declares no major at all | version_major | reader | open | `[R-CNT-07]` | | F19 | Any bit of the flags incompat lane …
   line 3888: …istered in each case is the neighbouring condition that *is* a violation — version_major = 0, which declares no major at all (F18, `[R-CNT-07]`), and a *reserved*-range type, whose emission `[R-CNT-15]` does make a vi…
== SWEEP [0 invalid] hits=7
   line 809: … 41 54 0D 0A 1A` (`\x8A`, "NRAT", CR, LF, ctrl-Z) | | 8 | 2 | u16 | version_major | structural | 1 (0 invalid; others: §6.3) | | 10 | 2 | u16 | version_minor | descriptive | any (see §6.3) | | 12 | 4 | u32 | f…
   line 947: … in its extent — never inline — and declares the document's encoding in its own inline payload (u8: 0 invalid, 1 = none, 2 = zstd; §18). An extent of (0, 0) on a user-metadata record, or one whose extent_lengt…
   line 972: …nline payload: | Offset | Size | Type | Field | Class | |---|---|---|---|---| | 0 | 2 | u16 | type (0 invalid) | structural | | 2 | 2 | u16 | flags: bit 0 MUST_UNDERSTAND, bit 1 PRESERVE_ON_EDIT, bits 2–15 res…
   line 1077: …n + bytes | §4.6 name rules; unique per `[R-ENC-15]` | | layout | u8 | 1 = interleaved, 2 = planar (0 invalid; others reserved); semantics §14 | | linearization | u16 | §11.4 | | codec | u16 | §17 (0 invalid) …
   line 1079: … (0 invalid; others reserved); semantics §14 | | linearization | u16 | §11.4 | | codec | u16 | §17 (0 invalid) | | filter | u16 | 1 = none, 2 = byte-shuffle (0 invalid; others per §17) | | alignment A | u64 | …
   line 1080: …tion | u16 | §11.4 | | codec | u16 | §17 (0 invalid) | | filter | u16 | 1 = none, 2 = byte-shuffle (0 invalid; others per §17) | | alignment A | u64 | 0 = none declared; else a power of two, 512 ≤ A ≤ 2⁶² (§16…
   line 1087: …s) · extent u64 · tile extent u64 | §11.1 | | C channel entries | name (u8 len + bytes) · type u16 (0 invalid) · fill (u8 len + bytes) | type per §12; fill length equals the type's element size (`[R-CNT-23]`),…
== SWEEP [version_major is 0] hits=2
   line 853: …ver silent, per §9.2's barrier note. #### 6.3 Version and flag gates A reader MUST reject-file when version_major is 0 (invalid) or is a major it does not implement, and the diagnostic for an unimplemented major SHOULD…
   line 3685: …_length, physical file longer | reader | open | `[R-CNT-06]` (R-LIF-04, R-CNT-10) | | F18 | Trailer version_major is 0, which declares no major at all | version_major | reader | open | `[R-CNT-07]` | | F19 | Any bit of…
== SWEEP [meaning exactly what they meant] hits=1
   line 3164: …arises rather than standing on its own: a change that leaves every one of those tiles' stored bytes meaning exactly what they meant — a filter whose mandated stride makes it the identity (`[R-COD-10]`), or a new padding position wh…
== SWEEP [new padding position whose stored byte already holds the fill] hits=3
   line 1622: …its extent becomes slack, a tile the superseded generation did not store carries none either, and a new padding position whose stored byte already holds the fill alters nothing. One shrink can do several of these at once. A layer that stored no tile in the gene…
   line 3166: …exactly what they meant — a filter whose mandated stride makes it the identity (`[R-COD-10]`), or a new padding position whose stored byte already holds the fill `[R-SER-05]` fixes — is not what this bars. A channel's declared **sample type** is such a declarat…
   line 3254: …s it. What counts as such an alteration is the §14 bar and nothing else, its carve-out included — a new padding position whose stored byte already holds the fill `[R-SER-05]` fixes is not one, so a shrink producing only those is permitted here exactly as it is …
== SWEEP [the set of padding positions] hits=1
   line 3152: …n the generation this commit supersedes**, what §14 fixes for its stored bytes or how they decode — the set of padding positions (§11.3), the pad bits `[R-SER-03]` gives a packed planar bool plane, and the content `[R-SER-05]` f…
== SWEEP [byte offset of any] hits=1
   line 3154: …gives a packed planar bool plane, and the content `[R-SER-05]` fixes at both, the decoded size, the byte offset of any value within the decoded tile image, the sample type each value in the image is read under, or the …
== SWEEP [re-establish the invariants] hits=1
   line 2323: …ration itself, of a layer slab-declared in either the superseded or the new generation, MUST either re-establish the invariants for every such run — or clear the declaration in the new generation; carrying a stale declaration f…
== SWEEP [stale declaration] hits=2
   line 2324: …lish the invariants for every such run — or clear the declaration in the new generation; carrying a stale declaration forward is a validity error at layer scope, detected as the invariant failures of `[R-SLB-03]` are:…
   line 2328: …3]` are: by a verifier. `[R-SLB-04]` **Note.** Because this rule's detection *is* `[R-SLB-03]`'s, a stale declaration carries no register row of its own: every file exhibiting one exhibits a run whose tiles are unpack…
== SWEEP [regenerates each] hits=1
   line 3491: … is unchanged — and every retained record per §20.4, except that relocation re-points extent slots, regenerates each tile-index region any of whose stored extents the output relocates (entry offsets new; entry length…
== SWEEP [is regenerated] hits=1
   line 3540: …ed. The reference arrays are identical; extent slots are re-pointed and each relocated index region is regenerated — the ′ marks (`[R-WRT-07]`). Placement is what changes, which is why the output is a different fil…
== SWEEP [regenerated region] hits=1
   line 3496: …ent CRCs recomputed over the entries as re-emitted), and updates the layer-record fields covering a regenerated region (crc_of_crc_array). Regenerating a region means classifying every entry in it: a sentinel is re-emi…
== SWEEP [settled on] hits=1
   line 1441: …s was not a commit state, so the tool continues the probe past it, and MUST report the candidate it settled on and how many it rejected, or, where no candidate survived re-verification, that none did and how ma…
== SWEEP [decoded-size bound] hits=0
== SWEEP [on the size bound] hits=1
   line 3815: …the defined non-violation (`[R-MTA-10]`), and except where a reader or verifier declines the decode on the size bound or on the frame's declared window, which `[R-MTA-09]` makes that actor's capability and not a fact …
== SWEEP [at the whole file] hits=2
   line 2684: …cord for that record; a reader that instead declines on resource grounds under `[R-ERR-04]` does so at the whole file, a document having no declared size and so no narrower scope whose declarations that rule can measu…
   line 3997: …very layer carries. A file exceeding any of these remains conforming, and a reader MAY decline it — at the whole file, or at the narrowest scope whose stated or derived quantities exceed what it can serve, a layer or …
== SWEEP [relocating a live index region] hits=1
   line 3146: … slot, pointing at the existing region, as does a layer the commit leaves untouched (`[R-WRT-05]`); relocating a live index region is compaction's operation (§20.5, `[R-WRT-07]`), not an appender's. A commit MUST NOT change a laye…
== SWEEP [never relocates a live index region] hits=1
   line 676: …rst time; a later commit changing B's stored-tile set would re-emit it at a new placement. A commit never relocates a live index region otherwise; that is compaction's operation (§20.5, `[R-WRT-07]`). This is what tail-anchored discove…
== SWEEP [turns real positions into padding] hits=1
   line 4167: …ntry becomes the sentinel (§15.2), and a shrink that either drops tiles out of the addressed set or turns real positions into padding (§20.3 step 4) all do it, and a record's extent goes the same way whether a commit drops the record…
== SWEEP [no pad bit] hits=2
   line 2050: … high bits, arising only when P is not a multiple of 8. A plane can have many padding positions and no pad bits — §14.5 gives both their content. **Example.** A planar bool tile, tile extents (2, 5), P = 10, va…
   line 3342: …ming a layer, or changing a channel's fill value where that channel carries no padding position and no pad bit in any tile the layer stores in the generation the commit supersedes. Only the directory is re-emit…
== SWEEP [carries no padding position] hits=1
   line 3342: …learing a slab declaration, renaming a layer, or changing a channel's fill value where that channel carries no padding position and no pad bit in any tile the layer stores in the generation the commit supersedes. Only the direc…
## Derived numbers
rows per family: {'F': 35, 'L': 49, 'T': 26, 'R': 10} total 120
instances (semicolon count, — = 1): 277
stated preamble counts:
3659:Outcome: reject-file. 35 conditions. Which rows reach a file declaring
3955:Every row of §21.2 through §21.5 — 120 conditions over 277

## 'stated' usage near §21.9 and elsewhere (for h19)
159:  It is always conformance to a stated format major version. This
1654:> **Note.** The stated form of the ceiling division avoids the idiom
2611:is stated over a document's decoded size, which a verbatim
3917:check for every one of them. The two are stated over the
3968:below states **minimum guarantees**, not caps: a conforming reader

## R-ENC-03 scope vs A/A_slab (for h20): L1 instances and A rows
3718:| L1 | A u64 offset, length, extent, or count field of a layer record holds a value above 2^63 - 1 | layer record extent_offset; layer record extent_length; sub-record extent_offset; sub-record extent_length; dimension extent Eᵢ; tile extent Tᵢ; entry
3746:| L29 | Layer record declares S ≠ 0 with an A_slab that is not a power of two in 1 … 2^62 (A_slab = 0 included) | A_slab = 0; A_slab not a power of two; A_slab above 2^62 | reader | layer access | `[R-CNT-23]` (R-SLB-02) |
3756:| L39 | Layer record declares a nonzero alignment A that is not a power of two in 512 … 2^62 | A not a power of two; A below 512; A above 2^62 | reader | layer access | `[R-SLB-01]` (R-CNT-23) |

## Per-hunk: rule adopted, and the eight checks (condensed)

h1 §2.4 R-CNF-12 (normative prose). Rule: a verifier's duty runs to all MUST-level conditions; SHOULD deviations are
 advisories reported only when observed. Old text was restrictive ("the MUST-level conditions §21 inventories") which
 limited the duty to the register — the defect. New text is non-restrictive: "MUST-level conditions, which §21
 inventories" asserts §21 inventories MUST-level conditions. §21.1 (h12): register enumerates every *detectable*
 violation; §21.7 (h17): "An unwitnessed condition is not one, so that clause requires no row for it". §21.7 also
 says it decides "without appeal to a list". So §21 does not inventory unwitnessed MUST-level conditions
 (R-COD-06 undisclosed dictionary, R-COD-10 mis-stride). => FINDING X-01 (OVERCLAIM, cross-hunk with h12/h17).
 Citations: §2.3 (line 209-211 "checks every file-level requirement") PASS; §21 PASS. Force: normative PASS.
 Not byte-level (duty over unwitnessed conditions is vacuous: §21.7 "no file-level witness exists to check").

h2 §9.6 R-LIF-06. Rule: recovery tool must report settled candidate + reject count, or none + count. Self-contained;
 no restatement elsewhere ("how many it rejected" 1 hit). Citations n/a. Siblings of the report: nothing else the
 rule needs. PASS.

h3 §11.1 **Rationale** block (non-normative by label — I checked the opening words "> **Rationale.**"). "last" -> "only
 remaining" zero grid count. Consistent with R-COD-07 Note (escape ends when every extent nonzero) and step 4's
 re-emission rule (normative, untouched). Citations R-CNT-17, R-GEO-06, §20.3, R-WRT-04 PASS. Not exhaustive
 ("included"). PASS.

h4 §16.2 R-SLB-04 (normative). Rule: any commit that changes stored-tile set, run partition, run placement, OR the
 declaration itself, of a layer slab-declared in EITHER generation, must re-establish invariants or clear the
 declaration. Tense now explicit. "every such run" -> runs of the new generation; R-SLB-03 binds every run anyway so
 no byte-level slack. Siblings: §20.3 step 4 closing ("a slab declaration is re-established or cleared") PASS; §16.2
 Note (no register row of its own) PASS; per-tile alignment sibling handled in step 4 (R-SLB-01) PASS. Compactor is
 not a "commit" but R-WRT-07 + R-SLB-03 bind it directly — pre-existing, consistent. PASS.

h5 §18.2 R-MTA-09 (normative). "either bound above" — exactly two bounds stated above (decoded-size bound line 2607-2609,
 window bound line 2634-2635); §21.5 preamble names the same two PASS; R-CNF-11 covers "declines to decode" PASS.
 Analogy R-COD-11: repair verb "cannot establish ... MUST NOT certify" = cited rule's verb, ranges document vs layer,
 both a scope's conformance — sound. PASS.

h6 §19.3 R-RDR-03 (normative). "the field widths at which §4 fixes the parse ([R-ENC-06]) and the u64 value domain of
 §4.2 ([R-ENC-03])". Agrees with §21.7 (h18): parse is at fixed widths; values then checked. R-ENC-06 §4.2 untouched
 and still says a structure at another width "is invalid at its owning scope" — a condition-shaped clause that §21.7
 says states no condition; pre-existing, not created by these hunks, no observable effect. PASS (see rejected).

h7 §20.3 step 4 (normative). List extended: pad bits (R-SER-03) + content R-SER-05 fixes at both; "sample"->"value"
 matches §14.2's table "Offset of value k". Example (c) (non-normative) already counted pad bits; §11.1 Rationale
 says only "what §14 fixes" — consistent. Structure siblings: layout, tile extents, channel count/order, type, fill,
 codec, filter — all reachable through decoded size / offsets / content / type / codec-filter. PASS.

h8 §20.3 step 4 (normative). Claims the carve-out (line 3162-3168) does not reach a growth; growth is an exception
 the permission states. The carve-out's own text states a general test ("leaves ... stored bytes meaning exactly
 what they meant") plus two examples; whether a fill byte that becomes a sample "means what it meant" is
 interpretive, and both readings permit the growth. Anaphors after insertion: "It holds" -> the permission/exception
 (same referent either way); "is another" -> another bound (unchanged). L44 / R-COD-07 quantifier ("addressed") PASS.
 Rejected as a finding.

h9 §20.3 step 4 (normative). "A shrink whose damage falls on a tile the new state no longer stores is precisely where
 the §14 bar has no witness". Falsifiable outside shrinks (re-type + unstore, line 3160-3162; filter change on a
 stored tile with no padding); within shrinks it holds (damage on a still-stored tile is T4's). Sentence is scoped
 to shrinks. Rejected.

h10 §20.5 R-WRT-06 (normative). Carve-out: "where the output carries no later-minor feature the compactor does not
 implement, its stored version_minor is checkable against the floor". Actor unnamed; condition is a fact about the
 compactor's implementation set, not the output; a checker needs to implement every feature the output carries.
 => FINDING X-02. SHOULD-level both sides -> not byte-level. App. G item 8 (non-normative) restates same structure.

h11 §20.5 R-WRT-07 (normative). Regeneration keyed on relocated STORED EXTENTS (tile payloads), no longer on relocated
 REGIONS — correct, since entries carry tile offsets. §20.5 Example (non-normative) still says "a relocated
 tile-index region ... the one kind this operation regenerates" and "each relocated index region is regenerated".
 => FINDING X-06 (UNSWEPT_RESTATEMENT, non-normative). Not byte-level: a region copied while its tiles moved would
 point at wrong offsets, nonconforming under both readings (R-CNF-05/06).

h12 §21.1 (normative). Detectable := ∃f exhibiting ∀g not exhibiting ∃k obliged check separating f,g. Matches h17
 word-for-quantifier ("some check ... not necessarily the same check for each" / "some such check, which need not
 be the same check for every one of them"). Citations R-CNF-07, §21.7 PASS. Anaphor "the same exception stated
 above" -> "except where a rule assigns one expressly" (unchanged). PASS.

h13 §21.1 (normative). Now cites R-TYP-04 (§12.3) — which does say "the one case where a reader resolves a byte to a
 value rather than passing it through ... [R-SER-08] states it" PASS. Appendix H still: "the sole resolved byte ...
 ([R-SER-08], §14.2)" — same claim, same citation the repair abandoned. => FINDING X-07 (non-normative).

h14/h15/h16 §21.2 preamble / F18 row / §21.6 (all normative). All three say "declares no major at all" verbatim.
 "permanently invalid" 0 hits (control: "declares no major" 3). R-CNF-13 premise ("declaring a format major other
 than 1") unmet by a file declaring no major PASS; R-CNT-07 "version_major is 0 (invalid)" PASS; §6.2 table
 "1 (0 invalid…)" PASS. R-CNF-02 "always conformance to a stated format major version" — a no-major file is not
 "declaring another major", so it is assessed under major 1 and F18 records it; coherent. PASS.

h17 §21.7 R-ERR-01 (normative). Unwitnessed ∀f∃g∀k¬sep; detectable ∃f∀g∃k sep — exact duals PASS. "which need not
 be the same check for every one of them": "them" has two candidate antecedents — the files that do not exhibit
 it (intended, gives the dual) or "a reader or a verifier" inherited through "such check". The next sentence
 ("each quantifier is the other's dual") forces the intended one. => FINDING X-03 (ANAPHOR, low).
 "its absence is not the defect that clause names" -> §21.1's completeness clause (h12) PASS.

h18 §21.7 R-ERR-01 (normative). Qualifier concedes a mis-width structure is caught only "wherever the shifted value is
 one those rows reject" — i.e. sometimes not. That is the shape §21.7 gives R-COD-10's mis-stride (caught only
 where padding/bool bytes break, T26; "undetectable" otherwise) and classifies UNWITNESSED, while R-ENC-06 stays
 "no condition a file can exhibit". => FINDING X-05 (LOCAL_CONTRADICTION in classification; no obligation differs:
 both yield no row). Citation R-ENC-06 PASS.

h19 §21.9 R-ERR-04 (normative). "stated or derived quantities": the document uses "stated over" for what a TABLE ROW
 ranges over (line 2611 "§21.9's row is stated over a document's decoded size"; 3917). Under that reading a layer
 sub-record's oversized document is a "stated quantity" at layer scope and the narrowest scope is the layer; the
 §18.2 Note (line 2683-2685) says such a decline is "at the whole file ... no narrower scope whose declarations that
 rule can measure" — wording that still tracks the OLD "declarations". Under the declared/derived reading the two
 agree. => FINDING X-04 (NEW_AMBIGUITY). Not byte-level (MAY decline; file conforming either way).
 "the two capability refusals §21.6 names" — §21.6 names exactly two PASS.

h20 §21.9 R-ERR-05 (normative). "Two do not" 0 hits; "Some do not" 1. Items now three (512 floor; 2⁶² ceilings +
 power-of-two shape; 255 key cap) — "Some" carries it. A/A_slab sit outside R-ENC-03's domain (L1 instances exclude
 them; L29/L39 register "above 2^62" under R-CNT-23/R-SLB-01), so the 2⁶² ceiling is chosen, not forced. PASS
 (see rejected: "u64 domain" vocabulary vs h6).

h21 Appendix G item 5 (non-normative by heading). Identity iff s=1 or n=1: i·n+j = j·s+i ∀i<s,j<n ⇔ (n=1 ∨ s=1) —
 verified. "changes the stored bytes of any tile whose decoded image the permutation does not fix" — true under
 every lossless codec (distinct filtered images cannot share stored bytes). PASS.

## Cross-hunk pairs the charter named (my identification)
- three places, one condition: h14/h15/h16 (version_major = 0) — agree verbatim.
- definition + restatement both edited: h17 (§21.7) + h12 (§21.1) — agree quantifier for quantifier; h1 leans on
  what §21 inventories and overclaims (X-01).
- parse rule stated + cited: R-ENC-06 (§4.2, untouched) cited by h6 (§19.3) and discussed by h18 (§21.7) — h6/h18
  agree; h18's qualifier vs §21.7's own R-COD-10 classification (X-05).
- list extended in a numbered step: h7 (+h8/h9), with the labelled earlier block §11.1 Rationale (h3) and later
  accounts §20.3 Example (c) and §23.1 R-PRV-01 — all agree.

## Findings (7): X-01 h1 OVERCLAIM; X-02 h10 TENSE_QUANTIFIER(actor); X-03 h17 ANAPHOR; X-04 h19 NEW_AMBIGUITY;
   X-05 h18 LOCAL_CONTRADICTION; X-06 h11 UNSWEPT_RESTATEMENT; X-07 h13 UNSWEPT_RESTATEMENT. None byte-level.

## Rejected candidates
- h9 "precisely where": holds within its stated subject (shrinks); counterexamples are non-shrinks.
- h8 carve-out reach: interpretive; both readings permit the growth; no obligation differs.
- h20 "the u64 domain" vs h6 "the u64 value domain of §4.2 ([R-ENC-03])": claim true under either reading since
  A/A_slab are outside R-ENC-03 (L1, L29, L39).
- §21.7 gloss "ask whether a breach can be made to leave behind a file no obliged check separates ..." reads ∃f
  where the definition has ∀f; untouched, non-definitional ("That is the whole of the test" names the paragraph
  above as the test), and its innermost-k placement now agrees with h17.
- R-ENC-06's own "is invalid at its owning scope" vs §21.7 "no condition": pre-existing, no observable effect.
- h11 "(entry offsets new; ...)" when only some stored extents moved: next paragraph's "re-pointed to where its
  stored extent now lies" covers unchanged offsets.
