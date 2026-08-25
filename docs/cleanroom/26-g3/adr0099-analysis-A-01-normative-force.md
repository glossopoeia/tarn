# Refute pass on A-01 — lens: normative force

## Disclosure
Read: spec/tarn.md (sed/awk/grep only), case/case-A-01.md, hunk-01.diff, hunk-02.diff. Nothing else.
Unrequested context appeared before I began (a project instruction file and an index of maintainer memory notes). Not opened, not used.

## Prefix verification
awk NR 2334-2344 substr($0,1,2): 2334|[] 2335..2343 all |[> ] 2344|[]
=> the disputed §17.2 Note is entirely inside a blockquote.
awk NR 3025-3040 substr($0,1,3): 3025..3038 all "   " (no ">") => §20.3 growth passage is normative prose.

## Greps
grep -n "escape": 1423, 2338, 2567, 2613, 3010, 3034, 3593, 3902
grep -n "durab": 1174, 1180, 1183, 1458, 2339, 2936
grep -n "addressed tiles|addresses none|addresses tiles": 1003,1480,2328,2336,2339,3035,3060,3525,3609,3748,3781,3846
grep -n "0x7E000000": 2329, 3525, 3804, 4176
Whitespace-normalised: tr '\n' ' ' | grep -o -E '.{160}grow[a-z]* .{0,10}extent.{160}' => 5 hits, all either the §17.2 Note, a blockquote hunks 1/2 already corrected, or correct normative prose (§20.3 2996 under the antecedent "whose stored-tile set or index content this commit changes"; §2.3 actor list).
=> The false durability claim exists in exactly ONE place, and that place is a blockquote.

## Constructions tried
1. Normative sentence carrying the Note's rule? None. Chain: [R-COD-07] "any of whose addressed tiles"; [R-GEO-02] per-dimension "its grid count is 0, the layer has zero addressed tiles" (directly decisive for E=(100000,100,0) without the product argument); [R-GEO-03]; L44 and §21.6 preserve "addressed tiles" verbatim so §21.1's tiebreak is never reached.
2. Actor enumeration (reader, writer, updater, verifier, creator, appender, compactor). Verifier/updater inherit reader obligations => same quantifier. Appender governed by §20.3 line 3037 "a growth is permitted exactly where the geometry it produces satisfies every rule that geometry is subject to" => permits. NOTE: the verifier's ground (3) ("Implementation B is unconstructible") IS overreach — an appender holds both generations and can ask whether E_0 left 0. But its governing text is normative and correct, so the overreach costs nothing.
3. Does the Note gain force by any route? [R-CNF-01] excepts "any text labeled Note, Example, or Rationale"; the label is "**Note.**" (bold not italic, same form as every other §17.2 blockquote). The Note assigns no requirement id. No normative sentence incorporates it. §21.8 corpus instances come from rows, not Notes, so no corpus file's bytes move.
4. The reporter's disputed file: G=(391,1,0), N=0, decoded tile size 16,777,216*4 = 0x4000000 << 0x7E000000. Conforming; every conforming implementation accepts. B rejects only by following a blockquote against five normative statements. Writer side also does not move: §20.3's growth is a MAY, so a writer that declines or clears codec 4 violates no MUST NOT and stays conforming.

## Adjacent observation (recorded, NOT used to refute)
§21.9 lines 3797-3804, normative, ends [R-ERR-05]: "Some limits are instead **hard**: a file violating one is invalid, not merely large. They are stated where the structures forcing them are defined — ... a layer declaring codec 4 at decoded tile size at most `0x7E000000` (`[R-COD-07]`)". This restatement drops the "addressed" quantifier, and §21.1 explicitly does NOT extend its "the rule governs" tiebreak to §21.9 (it names §21.6 only). Set aside because (a) "They are stated where the structures forcing them are defined" defers to the cited rule, and (b) it says nothing about growth or durability and, for the reporter's actual file (67 MB), it agrees with [R-COD-07]. Grading A-01 byte-level on this would be grading a different finding.

## Where the verifier is wrong
Ground (4) is factually wrong and it is the only ground attacking the finding's reality. Hunk 1's minus side carried BOTH the carve-out AND a contradicting trailing clause "— the first growth of a zero-extent layer included." The repair's substance is the deletion of exactly that clause, replaced by "the growth that raises a zero-extent layer's **last** zero grid count included." §17.2's Note states the deleted proposition in other words. UNSWEPT_RESTATEMENT is apt; the finding is real as text.
Ground (1) is true but narrower than presented (§20.3 governs commit permission, not reader acceptance; [R-COD-07]+[R-GEO-02] carry the reader side).
Ground (2) is correct and independently sufficient for byte-level. I could not break it.

## Verdict
Real as text: YES. Byte-level: NO. The byte-level downgrade stands.
