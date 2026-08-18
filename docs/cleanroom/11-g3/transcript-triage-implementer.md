# Round 11 triage — implementer-consequence lens

## What I read

`spec/tarn.md` only (plus one mechanical count over it). Sections read in
full: front matter, §2.1–2.5, §4.5–4.7, §5.1–5.2, §6.1–6.4, §7.1–7.4,
§8.1–8.2, §9.2, §9.7, §10.2–10.4, §11.1–11.2, §12.3, §13.1–13.3,
§14.2–14.5, §15.1–15.2, §16, §18.1–18.3, §19.1–19.2, §20.1–20.5,
§21.1–21.9 (all four register tables), §22.3–22.5, §24, Appendices A, G, H.
I did **not** read the round-9/11 reporter transcripts in the scratchpad,
`docs/`, `PLAN.md`, `AGENTS.md`, `conformance/`, `spec/registry.json`, git
history, or the web. I evaluated all 41 input findings; none was skipped.

One mechanical check run (python over the register tables, no repo state
touched):

```
{'21.2': 53, '21.3': 106, '21.4': 45, '21.5': 44}  total 248
row counts 36 / 49 / 26 / 10 = 121
```
matching §21.8's "121 conditions over 248 instances" — with R7's six
instances (BOM included) counted. That settles diagrams-07 in favour of the
Instances cell and against the Condition cell.

## Method

For each finding I asked the lens question first — *name the wrong thing an
implementation does* — and only then the byte-level test. Where I downgraded
a reporter's byte-level flag I recorded the sentence that decides it.

Working rule I applied consistently to the four compactor-conduct findings
(reader-02/adversary-04, reader-03, adversary-08, quiz-02), because they have
identical shape and must not be graded differently by accident:

> If a sentence in the governing requirement decides which of the two
> candidate outputs a conforming compactor may emit, the finding is a wording
> defect. If no sentence decides it — if the deciding word is the one that is
> missing — the permitted-emission set really does fork and the finding is
> byte-level.

Under that rule three of the four are wording defects and one (quiz-02) is
not.

## Group-by-group

### 1. fill / structural taxonomy — reader-01, adversary-01, quiz-04
Three reporters, one defect. Verified §4.7's text: structural = "determines
anything a conforming reader or verifier does with the file's bytes — where a
byte lies, how it decodes, or **whether the file, layer or tile is accepted at
all**"; and the closing "In format major 1 `fill` is the only semantic field".
[R-SER-05] makes a tile's acceptance a function of the recorded fill (T4, T5,
detector verifier); [R-TYP-07] makes a bool fill byte a layer-scope error
(L35). So the test captures fill and the class is empty. §13.1's gloss
("never how any byte is located or decoded") reproduces only the first two
disjuncts. Adversary-01's third ground (the Note's length-prefix rule) is
answered by §13.1's own "the field's length prefix is §7.4's framing", so I
do not rely on it.
**Byte-level: no.** I grepped every use of "structural" as a class word: the
only normative consequence attached to any class is the *descriptive* one —
§4.7's "a reader MUST NOT alter decoding based on it". [R-MTA-02] and
[R-SEC-06] use "structural" as the opposite of "user metadata", unaffected by
where `fill` lands. T4, T5 and L35 state their conditions over bytes.
Consequence to an implementer: none to a byte; a spec editor auditing field
classes cannot reproduce the document's own count.

### 2. compactor placement vs §16 — reader-02, adversary-04
reader-02 flags byte-level; adversary-04 does not. Checked §20.2 (creator)
states the grant *with* the qualifier — "in any order satisfying §5.2's
coverage classes … and every declared layout invariant (`[R-SLB-01]`,
`[R-SLB-03]`)" — and §20.5 states it without. The expressio-unius hazard is
real and I agree the clause must be repaired.
**Byte-level: no.** Downgrade quotes, both inside [R-WRT-06], the requirement
an implementer of §20.5 is reading: "Given a conforming input the output is a
conforming file." and "A compactor satisfies every writer requirement for the
bytes it produces (`[R-CNF-06]`)"; [R-CNF-06] in turn is "An updater MUST
satisfy every writer requirement for the bytes it produces", and [R-CNF-05]
is "A writer MUST emit only conforming files." A densely-packed output of an
alignment-declared input is not a conforming file — [R-SLB-01] states the
invariant as a property of the file ("When declared: every stored tile's
offset satisfies offset mod A = 0") and L40/L41/L42 register it. So the set
of byte sequences a conforming compactor may emit is the same before and
after the repair; what the omission does is invite a compactor author to emit
something outside that set. I also confirmed the escape hatch is closed:
[R-SLB-04]'s clearing licence is conditioned on a *commit* that supersedes a
tile or grows extents, and [R-WRT-07] enumerates the layer-record fields a
compactor may change (extent slots, regenerated index regions,
crc_of_crc_array) — the declaration is not among them.

### 3. corrupt user-metadata extent bars compaction — reader-03
§8.1's map does state a checksum for a user-metadata extent, so [R-WRT-09]'s
"each relocated extent's checksum" reaches it, so [R-WRT-06]'s refusal fires.
The quarantine's "notwithstanding" in [R-CNT-25] overrides *the owning-scope
mapping of `[R-CNF-08]`* by its own words — it is about which outcome class a
reader applies, not about an updater's conduct. Deciding quote: "A compactor
MUST refuse to compact when any check `[R-WRT-09]` obliges fails, and MUST NOT
emit a file carrying a violation it has detected."
So the question is decided (not an ambiguity) but the *policy* it decides is
worth a maintainer's eye: §20.5 and §23.1 make compaction the only operation
that reclaims slack, so one corrupt metadata blob makes a file permanently
uncompactable, over a condition §7.1 says "never invalidates the structural
data it annotates". PARTIAL.

### 4. "no commit removes … a file-scope user-metadata record" — reader-04, verifier-04, diagrams-05
Same defect from three reporters. The premise sits one paragraph above and is
unqualified — "both registered types carry PE = 1, so neither can be dropped,
and implementing a record's type confers understanding of it, not permission
to drop it" — and §7.3 registers 0x0002 once, scope "file when top-level;
layer as sub-record". Appendix H states it correctly ("at either scope").
**Byte-level: no**, on the quoted premise: the sentence that would license the
drop is contradicted by the sentence above it, so which directory bytes a
conforming updater may emit is already fixed. Note this is the same shape as
quiz-02 and differs exactly in that a deciding sentence exists here.

### 5. §21.7's witness-free account — reader-05, register-06, diagrams-09
Three reporters, one defect, different candidate omissions ([R-LIF-02] step 3;
[R-IDX-01]; [R-WRT-05]/[R-WRT-06]/[R-WRT-07]/[R-CNF-06]). Checked each:
[R-IDX-01] ("The entry for the tile with disk ordinal k is the k-th entry …
entry order is disk-ordinal order") is a definition of the mapping, i.e.
exactly the class §21.7 already names for [R-GEO-06]/[R-SER-01]; [R-LIF-02]
step 3 and the preservation obligations are relations between generations,
i.e. exactly the history class. So under "§21.7 the account, **by class**, of
what fails it" nothing is missing; under the paragraph's closing-"and"
grammar, five identifiers are. Evidence the document's practice is to note
witness-freedom *at the site* rather than only in §21.7: §7.4's Note on the
nesting prohibition — "in format major 1 it has no reader-detectable witness,
and so no register row."
**Byte-level: no** — both readings agree none of these carries a row.

### 6. a commit that narrows an extent — reader-06
Grepped for shrink/narrow/reduce: nothing in the document forbids narrowing a
dimension extent, and §11.1's rationale discusses growth only. [R-SER-05] is
a file predicate ("a verifier MUST check it, and a violation is a validity
error at tile scope", T4/T5), so a narrowing commit that retains its edge
tiles emits a nonconforming file. §20.3 step 4 never says so, while shape (c)
states the symmetric rule for a fill change. **Byte-level: no** — the file
predicate decides which files are conforming and both readings agree; what is
missing is a step in a procedure. But the maintainer has to decide whether
narrowing is permitted at all, which the document nowhere states.

### 7. listing a rejected layer's name — reader-07
L3/L5/L6 reject a layer *because* the name is unusable, all detected at open;
§2.4 then says "A reader MAY still list the file's layers, including the
rejected one's name", and §22.4's [R-SEC-05] screening is precisely what has
failed. Genuinely unstated. **Byte-level: no** — the file's verdict is fixed.

### 8. the front block and the verifier — verifier-01, adversary-06
One defect seen from two places: nothing verifier-facing states the
front-block obligation (Appendix H's verifier list omits it; F6's Condition
cell repeats the deferral), while §6.1 grants deferral to "a reader".
**Byte-level: no.** Deciding quote, §2.3: "**Conforming verifier.** A reader
that additionally checks every file-level requirement — *including those
ordinary readers are exempted from*". [R-CNT-04]'s residency deferral is the
clause's evident referent, and [R-CNF-12] adds "a verifier certifies only
violation-free files". Also §2.3's *cannot establish* is available only "on a
capability or resource ground", which fetching 16 bytes is not. Adversary-06's
secondary point (Appendix H's reader entry drops §2.3's "assigns to the reader
as its detector") travels with this group.

### 9. experimental-range metadata encoding — verifier-02
[R-MTA-09] scopes its cannot-establish clause narrowly — "A **verifier** that
declines to decode a document **on the bound above**" — while §2.3's list
restates it as "when it declines to decode a user-metadata document
(`[R-MTA-09]`)". A verifier genuinely cannot check [R-MTA-05]'s member
ordering for a document under an unassigned encoding, so *cannot establish*
is defensible; §21.6 says "the file is conforming". Two verdicts on identical
bytes. **Byte-level: no** — §2.3: "*Cannot establish* is not a finding that
the file is nonconforming", the reader outcome is ignore-record under
[R-CNT-25] either way, and no writer's bytes move. It is a certificate fork,
which the maintainer should close.

### 10. partial slack total — verifier-03
The reporter's two readings are decided by [R-CNT-21], which states the
criterion as enumeration rather than as rejection: "Where the walk of §9.7
does not enumerate every region's claimants — whether because a scope-level
rejection stops it, or because the verifier elected under `[R-CNF-11]` to stop
at the first violation — the verifier MUST report the total as partial." So a
verifier that enumerated everything reports an exact total whatever the L35
verdict, and one that abandoned the layer reports partial *and must say what
stopped it* — the operator can tell the two numbers apart by their labels.
§9.7's "a scope-level rejection blocks enumeration" is loose wording of that
criterion. PARTIAL, byte-level no.

### 11. Appendix H omits pad bits — verifier-05
Verified: the verifier entry reads "decoded-content obligations — padding
samples and interleaved boolean bytes (§14.5, §14.2)". T5 exists, detector
verifier. Non-normative, cites §14.5 which covers pad bits. Byte-level no.

### 12. Appendix G is not total — verifier-06, adversary-05, diagrams-03
I merged these because they are the same defect stated over three gaps in the
same recipe: (a) no order between top-level record extents and a layer's
sub-record extent, though both are extents the profile emits "in ascending
record order"; (b) no tiebreak between two records of one unassigned type;
(c) item 2's hash names no function, no digest reduction, no serialization of
"the trailer's other fields", no rule for a zero result — and, as diagrams-03
shows, is circular if "the trailer's other fields" is read to include the
trailer CRC, since §6.2 makes that CRC cover trailer bytes [0, 60) which
contain file_id at offset 48. adversary-05's two gaps are (a) and (c);
diagrams-03 is (c) sharpened.
**Byte-level: no.** Appendix G: "It adds no requirement to any actor: a writer
ignoring it is fully conforming", and §6.2's trailer table admits any nonzero
file_id, so every reading produces conforming files.

### 13. Appendix G's "Four things are not" — diagrams-02
Checked item 6 against the core text: nothing in §13.3/[R-TYP-08]/§15.2
requires the sentinel for an all-fill tile, so item 6 closes a freedom the
inventory does not count; item 8's version_minor floor is [R-CNT-26]'s SHOULD
promoted exactly as item 7 promotes [R-TYP-10]'s. The count is wrong.
Byte-level no, same disclaimer quote as group 12.

### 14. layout-table columns — diagrams-01
Verified column headers: §6.1 is `| Offset | Size | Value | Class |`; §7.2 is
`| Offset | Size | Type | Field | Class |`; §6.2, §15.1, §18.2 do deliver all
six. §4.7's Note carves out §7.4 alone. Byte-level no.

### 15. [R-VEC-04]'s detector field — diagrams-04
[R-VEC-02]'s minimum list is "the outcome class (§2.4), the scope, and the §21
register row it exercises" — no detector; [R-VEC-04] reads "the entry's own
scope and detector fields (`[R-VEC-02]`)". Confirmed. Manifest schema only.

### 16. Appendix A "A local reader" — diagrams-06
§6.1 says twice that residency, not transport, governs. Appendix A's main
clause says "local reader"; its own subordinate clause restates residency.
Non-normative. Byte-level no.

### 17. R7's Condition cell — diagrams-07
Settled mechanically (see the count above): the six instances are the ones
§21.8 counts, so the Condition cell should name the BOM alternative that
§18.2's first restriction states. Byte-level no — [R-MTA-04] states the rule.

### 18. index-encoding value set — diagrams-08
§15.1 states no value set (only "Under index_encoding 1 (the only encoding
this format major version defines, §7.4)"); §7.4's table row does state it in
full. [R-EXT-03], [R-RDR-03], §10.2 and L31 all point at §15.1. With
[R-EXT-05] making section-of-definition the tiebreaker, the pointer should be
§7.4. Byte-level no — every statement of the set agrees.

### 19. front matter's vector claim — diagrams-10
"test vectors cite those identifiers" vs [R-VEC-02]'s register row. Kept
separate from group 26 because the repair differs (fix the sentence, or add
the identifier to the manifest) even though both reporters of group 26 cite
this claim as a consequence.

### 20. §21.1's [R-SER-08] gloss — register-01
§21.1: "for several such rows it obliges the reader to serve the structure
unchanged (`[R-SER-08]`, `[R-CNT-22]`)". [R-SER-08] obliges neither half:
"A reader is not obligated to screen decoded content … `[R-CNF-12]` governs a
reader that does detect it" and "A reader that neither detects the violation
nor rejects the tile, and returns the value, MUST report 0x00 as false and
every other byte as true." §12.3 calls it "the one case where a reader
resolves a byte to a value rather than passing it through". Byte-level no —
the imperative sentence governs and the byte cannot occur in a conforming
file.

### 21. [R-VEC-02] cites §21.5 — register-02
§21.5's header: "Every row here is a violation all the same … §21.6 lists the
ignore-record conditions that are not violations." Citing §21.5 for "a
conforming file can carry a record a reader ignores" is wrong. Byte-level no —
[R-CNF-12] and Appendix H each decide it.

### 22. F33 and two file-scope structures — register-03
Constructed the case mentally: a top-level MU=0 experimental record whose
extent overlaps the directory. F31/F32/F7 do not fire. F33's em-dash gloss
names only cross-layer and layer-vs-other-scope; [R-CNT-13]'s operative clause
("any overlap across layers or touching another scope's structures") does not
reach two file-scope structures either. **Byte-level: no**, on §9.7: the walk
enumerates "the live directory and its records and their sub-records, each
record's extent, …" and "It checks that these occupy disjoint byte ranges" —
so the obligation is stated over the full claimant set independently of F33's
prose, and [R-CNT-02] is unconditional. Register bookkeeping, but the leading
clause of F33 should be made to say what [R-CNT-13] cannot.

### 23. §21.5's pointer at §21.6 — register-04
§18.2's over-bound document is a third ignore-record non-violation with no
§21.6 entry. But §21.6 claims no closure ("These are defined behaviors, not
errors") and §21.1 says "neither this completeness clause nor the instance
arithmetic below reaches §21.6's defined non-violations". So §21.5's sentence
is a signpost, not a completeness claim. PARTIAL; adding the row would still
improve the finding aid.

### 24. F5's Instances cell — register-05
The document uses F for the *committed* length everywhere else (§5.1 "the live
trailer's committed file length F"; §6.2 "committed_file_length … = F"), so
"F (physical file size)" is a slip; and a distinguishable second instance
necessarily also trips F17/F10. [R-VEC-02] already anticipates non-isolable
attributions. Register bookkeeping — but note §21.8's mechanical 248 depends
on the cell, so this is a maintainer's call, not a hand-edit.

### 25. "opaque by construction" — adversary-03
§7.3 registers exactly one MU=0 type and §18.2 specifies its contents
completely, so §21.7's stated reason is untrue for the only instance a
format-major-1 file can carry. The honest reason is undecidability.
**Byte-level: no**, on §21.7's own first paragraph: "no file-level witness
exists to check, so nothing about the file is left undetermined and the
verdict is unaffected." Whether [R-CNT-13] reaches a user-metadata document at
all is a scope question the maintainer should answer explicitly.

### 26. the front-matter block — adversary-02, quiz-01
[R-CNF-01]'s list is exhaustive: "§1 (Introduction); any text labeled *Note*,
*Example*, or *Rationale*; and appendices identified as non-normative." The
block precedes §1, is not so labeled, and is not an appendix — and the status
paragraph and licence line above §1 are in the same position. Byte-level no:
nothing in the block constrains a file byte.

### 27. the trailer-mimic row — adversary-07
§21.6's row states its condition over a *payload* and its justification over
*slack*; §5.2 makes a payload a structure of the live state, explicitly not
slack. The sound reasons are [R-LIF-05]'s no-backward-scan and §6.2's Note
("A payload byte-string that mimics a trailer and happens to sit at exact
physical end of file … is caught at the directory CRC"). Byte-level no —
§21.6 carries no rows and §21.1 makes the cited rule govern.

### 28. compaction barred by any MU=1 record — adversary-08
**Byte-level: no.** Deciding quote, in the section a compactor author is
reading: "A compactor MUST refuse to compact a file carrying **any record**
whose type it does not implement with MU = 1: such a type can define
references this specification does not (§7.2), so its bytes cannot be safely
relocated." §7.2's framing makes a sub-record a record. §20.4's "Compaction is
barred on the same ground" reads narrowly only by placement. The failure mode
the reporter describes (relocating an extent whose embedded references still
point at the input's offsets, undetectable because §8.1 gives an unassigned
type's extent no checksum) is real, which is why the cross-reference should be
repaired even though it is not byte-level.

### 29. compactor version_minor — quiz-02 — **byte-level, upheld**
The one finding where my working rule bites the other way. The sentence is:
"The output trailer copies the input's unknown ignore-lane flag bits forward
(`[R-CNT-08]`) and carries the greater of `[R-CNT-26]`'s floor and the input's
version_minor". The first conjunct is mandatory ([R-CNT-08]: "An updater MUST
copy forward unknown ignore-lane bits"); the second cites a SHOULD whose
appender half it restates almost verbatim ([R-CNT-26]: "an appender the
maximum of that floor and the prior trailer's minor"). No keyword, and no
consequence-of-deviation clause of the kind §2.1's Note requires of a SHOULD —
what follows the dash is a rationale for the rule, not a consequence of
deviating, unlike [R-CNT-26]'s own "misstates the file's feature floor to
tooling" and [R-TYP-10]'s "still emits a conforming file, but …".
Concrete fork, on an input whose trailer carries version_minor = 3 and no
unknown ignore-lane bit: compactor A emits `03 00` at [F−54, F−52); compactor
B, following [R-CNT-26]'s primary advice ("the lowest version_minor that
defines every feature present in the file — for a file expressible under this
text, 0"), emits `00 00`. Under the MUST reading B has emitted a file no
conforming compactor may emit; under the SHOULD reading both are within
permission. Nothing else in the document decides it: I checked §6.3, §20.1,
§20.5, §2.3 and Appendix H, and Appendix H does not mention version_minor for
updaters at all.
Why I did not downgrade despite the obligation being witness-free (no verifier
can compare an output against its input, and both outputs are conforming
*files*): the test's first half asks which byte sequences a conforming
implementation may emit, and the permitted-emission set genuinely differs
between the readings. There is no sentence I could quote to close it, because
the closing word is the one that is absent. The repair is one keyword.

### 30. unimplemented major with a failing trailer CRC — quiz-03
REFUTED. §6.2 orders the checks "the trailer magic; the trailer CRC; the
version gate (§6.3)" precisely so the version field is trustworthy when it is
used, and [R-ENC-10] bars acting on a field before the checksum covering it
verifies ("*acting on* means using its value to allocate, seek, fetch, or
**select behavior**"). A file whose trailer CRC fails is therefore not
established as "declaring another major" at all; what is established is F14,
and §2.3's "An established violation takes priority" gives *nonconforming*.
Both candidate verdicts are non-certification and the reader rejects the file
either way, so nothing byte-level rides on it; a clarifying half-sentence in
§2.3 would still help.

## Coverage

41 input ids, 30 groups, each id in exactly one group; counted by hand and
re-summed (3+2+1+3+3+1+1+2+1+1+1+3+1+1+1+1+1+1+1+1+1+1+1+1+1+2+1+1+1+1 = 41).
Byte-level upheld: 1 (quiz-02). Byte-level flags downgraded: 2 (reader-02,
reader-03), each with the deciding sentence quoted above.
