# Round 11 triage — skeptic pass

## What I read

- `/Users/robertkleffner/Documents/GitHub/tarn/spec/tarn.md` in full (3953 lines, read in
  seven contiguous chunks: 1–120, 120–330, 330–560, 560–830, 830–1120, 1120–1400,
  1400–1700, 1700–2000, 2000–2320, 2320–2650, 2650–2980, 2980–3260, 3200–3480,
  3480–3953). Front matter, §1–§24, Appendices A–H.
- No round-9/11 reporter transcripts were opened. Every quotation below is from
  `spec/tarn.md` as it stands.
- One script run: a mechanical recount of the Instances column of §21.2–§21.5
  (below). No other tooling.
- Not read (per the access rule): docs/, PLAN.md, AGENTS.md, conformance/,
  spec/registry.json, git history, the web.

## Mechanical check run

```
21.2 rows 36 instances 53
21.3 rows 49 instances 106
21.4 rows 26 instances 45
21.5 rows 10 instances 44
total 248
```

Row counts match each subsection's stated count (36/49/26/10 = 121) and the
instance total matches §21.8's "121 conditions over 248 instances". The two
`leading U+FEFF` instances of R7 are inside that 248, and F5's two instances are
too. Both facts are load-bearing below (diagrams-07, register-05).

## Method

Skeptic default: assume the reporter is wrong and hunt for the sentence that
forecloses the finding, in a section the reporter did not cite. Where I found
one, it is quoted. Where I looked and could not find one, I say so explicitly.

---

## 1. fill-taxonomy — reader-01, adversary-01, quiz-04

Three reporters, one defect: §4.7's structural test captures `fill`, contradicting
§4.7's own closing claim that `fill` is the only semantic field.

Text checked. §4.7: "A field is **structural** if its value determines anything a
conforming reader or verifier does with the file's bytes — where a byte lies, how
it decodes, or whether the file, layer or tile is accepted at all... It is
**semantic** if not, but its value determines what decoded values are... In format
major 1 `fill` is the only semantic field."

§14.5: "at every padding position, a writer MUST encode, for each channel the
position carries, that channel's fill value... a verifier MUST check it, and a
violation is a validity error at tile scope."

Tried to kill it three ways and failed:

- "which is the sense `[R-CNT-07]`, `[R-MTA-02]` and `[R-SEC-06]` already use" —
  hoped this narrowed the definition to a reader-side decoding sense. It does not:
  [R-CNT-07] is the version gate, an acceptance gate, and the definition's own
  third disjunct is written as acceptance. No narrowing.
- §13.1's "never how any byte is located or decoded" — this is a *restatement*, and
  §21.1's "where a row and the rule it cites diverge, the rule governs" has no
  analogue here, but §4.7 is where the classes are *defined*, so §13.1 cannot
  narrow §4.7.
- Appendix A / front matter version: "structural (its value affects where a byte
  lies, how it decodes, or whether the file is accepted)" — note "the file", not
  "file, layer or tile". Under the front matter's narrower wording fill escapes.
  But the front matter is the weaker text (and see group 26 on its status), and
  §4.7 carries [R-ENC-16].

So the contradiction is real. adversary-01's ground 3 (§4.7's Note: "A
variable-length field's value includes its length prefix, so a name is
structural") is answered inside §13.1 — "the field's length prefix is §7.4's
framing, cross-checked against the element size" — so ground 3 alone would not
carry; grounds 1 and 2 do.

Byte-level: no. Deciding quotes: the only MUST that keys off the taxonomy is on
the *descriptive* class — "a reader MUST NOT alter decoding based on it" — and
`fill` is not descriptive under either reading. §14.5 states the padding
obligation unconditionally ("a verifier MUST check it") and §21.4's T4/T5 state
their conditions over bytes, so a verifier reaches the same verdict on every file
whichever noun §4.7 attaches.

Severity: design-decision. The repair forks — either narrow the structural test to
a field's direct role in locating/decoding (keeping `fill` semantic, keeping the
class non-empty), or classify `fill` as structural and withdraw the exhaustive
sentence, which leaves the semantic class empty. That is a maintainer's call.

---

## 2. compactor-placement-invariants — reader-02, adversary-04

§20.5 [R-WRT-07]: "it is free to place structures anywhere §5.2 admits", against
§20.2's parallel grant for a creator, which carries "and every declared layout
invariant (`[R-SLB-01]`, `[R-SLB-03]`)".

reader-02 flagged this byte-level. This is the group I tried hardest to kill, and
I killed it — the deciding sentence is two sentences up from the grant, in
[R-WRT-06], and reader-02 quoted it himself without weighing it as a foreclosure:

> "Given a conforming input the output is a conforming file. A compactor
> satisfies every writer requirement for the bytes it produces (`[R-CNF-06]`)"

That is normative declarative text (§2.1's exception list does not reach it), it
is unqualified, and it settles reading (b). Reinforced by [R-CNF-06]: "An updater
MUST satisfy every writer requirement for the bytes it produces", and the
offsets are bytes it produces; and by [R-SLB-03], which is a predicate on the
file's own bytes ("When declared, for every run: the run's stored tiles are
contiguous and packed in ordinal order... offset mod A_slab = 0"). Rows L40/L41/L42
state their conditions over the output file's bytes with no reference to how it
was produced, so no verifier's verdict on any file moves.

I also checked the escape adversary-04 checked, and agree it is closed: [R-SLB-04]
licenses clearing a declaration only on "a commit that supersedes a stored tile
in, or grows the extents of" the layer, which compaction does neither of, and
[R-WRT-07] enumerates the layer-record fields a compactor may touch
(crc_of_crc_array only).

Byte-level: no, on the quotes above. Consensus CONFIRMED — the grant as written is
genuinely missing the qualifier §20.2 states for the neighbouring tier, and the
omission is conspicuous. Severity: editorial (add the §20.2 qualifier verbatim).

---

## 3. compactor-refusal-corrupt-metadata — reader-03

Whether one corrupt user-metadata extent permanently bars compaction.

Checked the chain. §8.1's map: "User-metadata extent | final 4 bytes of the extent |
the preceding bytes". [R-WRT-09]: "each relocated extent's checksum, including
every stored tile's entry crc — before emitting that structure's bytes". So the
check is obliged; reading (c) fails on §8.1.

[R-WRT-06]: "A compactor MUST refuse to compact when any check `[R-WRT-09]`
obliges fails, and MUST NOT emit a file carrying a violation it has detected: it
can neither drop the structure (§20.4, `[R-WRT-07]`), nor re-emit it corrected
(`[R-WRT-05]`)."

The quarantine does not override it. The deciding words are the scope of the
"notwithstanding":

> "is ignore-record with a SHOULD-report, **notwithstanding the owning-scope
> mapping of `[R-CNF-08]`**"

It overrides the scope→outcome mapping, and nothing else. It does not reach an
updater's conduct. And §21.5's header confirms R2 is a violation: "Every row here
is a violation all the same: the outcome bounds a reader's blast radius and never
makes the file conforming (`[R-CNF-12]`)".

So the *ambiguity* claim is refuted: reading (a) is what the text determines. No
byte fork — compactor B's behaviour is not licensed by any reading of the text.

But the determined outcome is undiscussed and surprising: §20.5 and §23.1 both
make compaction the only slack-reclaiming operation and the operator's remedy, and
§7.1 closes with "Application metadata never invalidates the structural data it
annotates" — yet a single corrupt metadata blob makes the file permanently
uncompactable, with no way out ([R-CNT-25] cannot drop it, PE = 1 by registry;
[R-WRT-05] cannot re-emit it corrected). PARTIAL, design-decision.

---

## 4. preservation-either-scope — reader-04, verifier-04, diagrams-05

§20.4's summary sentence names only the file-scope user-metadata record; Appendix
H says "at either scope".

The deciding sentence is the paragraph immediately above the summary, and all
three reporters found it:

> "For a type §7.3 registers, the registry's fixed flags govern rather than the
> stored ones (`[R-CNT-22]`) — both registered types carry PE = 1, so neither can
> be dropped, and implementing a record's type confers understanding of it, not
> permission to drop it."

§7.3 registers type 0x0002 once, with Scope "file when top-level; layer as
sub-record", so the drop bar reaches the sub-record. §20.4's MU = 0 / PE = 1 table
row says "Retain byte-identical, extent content unmodified" without scope
qualification. §2.4's preserve-verbatim row points at those table rows. Appendix H
is substantively correct; §20.4's summary is under-inclusive.

Byte-level: no. Both a dropping and a retaining updater emit a *conforming file* —
version of the directory with or without a sub-record is conforming either way,
and no register row exists for the drop. The quote that decides which one a
conforming updater may emit is the one above. Severity: editorial.

---

## 5. section-21-7-account-closure — reader-05, diagrams-09, register-06

Three reporters, one defect claim: §21.7 ¶2's list of witness-less obligations is
incomplete ([R-LIF-02] step 3, [R-IDX-01], [R-WRT-05], [R-WRT-06]/[R-WRT-07],
[R-CNF-06]).

I confirmed each nominated obligation *is* witness-free (a trailer re-pointed at a
prior generation's directory leaves no field recording which commit wrote which
bytes, and §9.7's Note is explicit: "Nothing here enumerates prior commits"; a
permuted index parses identically).

But the foreclosing words are in §21.1, and only two of the three reporters
weighed them:

> "detectability being the gate `[R-CNF-07]` already applies and §21.7 **the
> account, by class,** of what fails it"

The account is designated *by class*, and every nominated omission falls inside a
class §21.7 already opens: [R-LIF-02] step 3, [R-WRT-05], [R-WRT-06]/[R-WRT-07]
and [R-CNF-06] are all "properties of a file's history, which §9.7 does not
reconstruct"; [R-IDX-01]'s entry order is an ordinal mapping alongside [R-GEO-06]
and [R-SER-01]. So the account is complete at the level §21.1 makes normative, and
register-06 and diagrams-09 both reached that conclusion independently.

PARTIAL: the "incomplete inventory" claim does not hold, but the paragraph's
grammar (a semicolon list joined by "and", each item citing identifiers) reads as
an inventory rather than a taxonomy, and one word ("among them", "for example")
closes the reading the reporters took. Byte-level: no — every obligation at issue
is witness-free under both readings, so no register row, outcome class, verdict or
vector moves. Severity: editorial.

---

## 6. commit-narrowing-extent-padding — reader-06

§20.3 step 4 and the shape-(c) example state the re-emission consequence of a fill
change but not the symmetric consequence of a geometry change that creates padding
positions.

Searched for a foreclosing sentence and did not find one. The nearest candidates
all fail:

- §20.1 [R-WRT-01]: "a violation latent in a structure they neither modify nor rely
  on travels with it" — does not apply, because a narrowing commit *creates* the
  violation rather than carrying one forward.
- §11.1's rationale discusses growth only ("Growth that leaves every grid count
  ⌈Eᵢ / Tᵢ⌉ (§11.2) unchanged touches the directory alone"), which if anything
  reinforces the wrong instinct.
- Nothing in §11 or §20 forbids narrowing an extent; §20.3 step 4 speaks only of
  "grown extents", and [R-SLB-04] only of a commit that "grows the extents".

So the gap is real: the procedure is silent where the file predicate bites.

Byte-level: no, and here the deciding sentence is the predicate itself:

> "at every padding position, a writer MUST encode, for each channel the position
> carries, that channel's fill value... a verifier MUST check it, and a violation
> is a validity error at tile scope."

An edge tile carrying non-fill at a padding position is nonconforming (T4/T5)
whether §20.3 mentions it or not, so two implementations reading §14.5 reach the
same verdict. What is missing is a step in a procedure. CONFIRMED, editorial.

---

## 7. rejected-layer-name-listing — reader-07

§2.4 permits listing a rejected layer's name; L3/L5/L6 are the cases where the name
is what was rejected.

Killed. Two deciding sentences the reporter did not cite:

> **§2.4 Note.** "'Reject' prescribes the scope of unusability, not user
> interface: how failure is reported is implementation technique."

> **§2.1 Note.** "requirements constrain bytes and observable behavior, never
> implementation technique."

What a reader hands a caller for a rejected layer's name is exactly user interface,
which this document declines to constrain by design. The security half is already
covered normatively, and not by a carve-out but by a MUST on the consumer:

> **[R-SEC-05].** "A display surface MUST NOT assume a name is safe for its own
> syntax, and a reader MUST NOT interpret a name as a filesystem path"

REFUTED, severity none. At most an optional cross-reference from §2.4's
reject-layer row to [R-SEC-05].

---

## 8. verifier-front-block-obligation — verifier-01, adversary-06

verifier-01 asks whether a verifier inherits [R-CNT-04]'s deferral; adversary-06
observes that Appendix H never mentions the front block, including in the verifier
entry that exists to enumerate "the checks readers are exempt from". One repair
fixes both, so one group.

The normative question is decided, by the clause adversary-06 quotes:

> "**Conforming verifier.** A reader that additionally checks every file-level
> requirement — **including those ordinary readers are exempted from** — and
> certifies conformance."

"Writers MUST emit exactly these 16 bytes" is a file-level requirement; F6
registers its violation; [R-CNT-04]'s deferral is precisely the exemption ordinary
readers get. Reinforced by §9.7, which claims [0, 16) for the coverage walk ("The
front signature block at [0, 16) and the live trailer at [F − 64, F) are claimed by
the walk as well"), and by [R-CNF-11], which makes *cannot establish* available
only "on a capability or resource ground" — fetching 16 bytes is neither.

PARTIAL: the ambiguity is refuted, the checklist omission is real. Byte-level: no.
Severity: editorial (one clause in Appendix H's verifier entry).

---

## 9. experimental-metadata-encoding-verdict — verifier-02

Verdict for a user-metadata record with an experimental-range (≥ 0x80) encoding:
*conforming* or *cannot establish*?

Decided, and against the reporter's stated worry. §18.2 [R-MTA-09] scopes its
cannot-establish clause narrowly:

> "A **verifier** that declines to decode a document **on the bound above** cannot
> establish that document's conformance"

— "the bound above" being the resource bound of the preceding sentence. An
unassigned encoding is not that. [R-MTA-03] settles what it is instead: "An
encoding a reader does not implement is therefore one this specification does not
assign, and is ignore-record (`[R-CNT-25]`)". And [R-MTA-04]/[R-MTA-05] are
predicated on a decoded document ("The decoded document is a JSON text as defined
by RFC 8259"), which does not exist, so no requirement is left unchecked. §21.6's
row states the outcome directly: "Ignored (ignore-record); the file is conforming".

So the file is *conforming* and the reporter's reading (b) is what the text
determines. PARTIAL: the residue is that §2.3's restatement drops [R-MTA-09]'s
"on the bound above" qualifier, which is what generated the finding. Byte-level:
no. Severity: editorial (restore the qualifier in §2.3).

---

## 10. partial-slack-total-trigger — verifier-03

Does every layer-scope rejection make the coverage walk partial?

Decided by the sentence's own frame and by [R-CNT-21]'s closing words:

> **§9.7.** "**Where the walk does not complete** — a scope-level rejection blocks
> enumeration, or the verifier stops at the first violation (`[R-CNF-11]`) — the
> sum is reported as partial"

The operative test is walk completion; the em-dash pair names two causes of
incompletion. And [R-CNT-21] removes any doubt:

> "It is not the file's slack total but a bound on it, **tightening to the exact
> total when the walk completes**."

The numeric divergence the reporter measured is real but licensed and labelled:
[R-CNF-11]'s "A verifier MAY stop at the first violation it finds; one that does
MUST report each scope it did not examine as *unexamined*", and [R-CNT-21]'s "a
verifier reporting one MUST say which scope or violation stopped the walk". An
operator can tell an exact total from a partial one with its cause named.

REFUTED. Byte-level: no (both readings give NONCONFORMING on the same file).
Severity: editorial — §22.3's "a verifier that stopped early reports it only as
partial" names one of §9.7's two causes and could name both.

---

## 11. appendix-h-pad-bits — verifier-05

Appendix H's verifier entry reads "decoded-content obligations — padding samples
and interleaved boolean bytes (§14.5, §14.2)". T5 (pad bits) is verifier-detected
and is a distinct mechanism by §14.3's own Note ("Pad bits are not padding
positions (§11.3)... A plane can have many padding positions and no pad bits").
Verified against §21.4: T4, T5, T2, T26 are the four verifier-detected
decoded-content rows; the entry names two of the three that need enumerating.

CONFIRMED. Byte-level: no — Appendix H is non-normative and disclaims itself
("each entry's authority is the requirement or section cited, never this
summary"), and [R-SER-05] states the obligation directly: "Every pad bit (§14.3)
MUST carry the plane's channel's fill bit." Severity: editorial.

---

## 12. appendix-g-emission-order — verifier-06, adversary-05

Grouped because verifier-06's gap 2 and adversary-05's gap 1 are the same
construction (a layer-scope user-metadata sub-record's extent against a top-level
user-metadata record's extent, both type 0x0002, no stated relative order).
adversary-05 additionally raises the item-2 hash-function gap; I have folded that
into group 15's repair rather than splitting the id.

Verified both gaps against item 3's text. "Records are ordered by type, and within
type 0x0001 by layer name" — type 0x0002 needs no tiebreak at top level
([R-CNT-14] permits at most one), but an unassigned type has no multiplicity rule
in §7.2/[R-CNT-14] at all, so two records of type 0x8001 have no defined order.
And "then any record extents in ascending record order" is ambiguous as to whether
it sits inside or outside the per-layer loop, and no order is stated across the
top-level/sub-record boundary.

CONFIRMED. Byte-level: no, on the appendix's own disclaimer: "It adds no
requirement to any actor: a writer ignoring it is fully conforming." Every
ordering yields a conforming file. Severity: editorial.

---

## 13. layout-table-columns — diagrams-01

Checked both tables against §4.7's Note. §6.1: `| Offset | Size | Value | Class |`
— four columns, no type, no field name, no valid range. §7.2: `| Offset | Size |
Type | Field | Class |` — five, no valid-range column, with the constraints folded
into Field cells ("type (0 invalid)", "flags: bit 0 MUST_UNDERSTAND..."). §6.2,
§15.1 and §18.2 do deliver all six.

The Note carves out exactly one exception ("its table omits the offset and class
columns"), which under the reporter's reading (b) would be pointless. I agree with
(a). Note also that the front matter promises five columns and §4.7's Note six —
the two promises differ from each other as well as from the tables.

CONFIRMED. Byte-level: no — §4.7's Note is labelled *Note* and so is non-normative
by [R-CNF-01]; §6.1's two rows are unambiguous constants and §7.2's constraints
are all present, only in a different cell. Severity: editorial.

---

## 14. appendix-g-four-things — diagrams-02

"Four things are not [already mandatory]" against nine items.

Verified the reporter's strongest instance: item 6 ("The sentinel for every
all-fill tile, so that a tile whose samples all equal fill is never stored") is
mandated nowhere. [R-TYP-08] makes an unstored tile read as fill; nothing forbids
storing a tile whose decoded values happen to equal fill, and §15.3 admits any
well-formed non-sentinel entry. Item 7's own text concedes item 6 is a separate
freedom ("item 6 stores no tile whose samples all equal fill, so two writers that
default fill differently disagree about which tiles exist"), yet counts only item
7's. Item 2 (§9.3 requires nonzero, advises randomness) and item 8 (promotes
[R-CNT-26]'s SHOULD exactly as item 7 promotes [R-TYP-10]'s) are likewise
uncounted freedoms.

CONFIRMED, undercount of at least three. Byte-level: no — "It adds no requirement
to any actor: a writer ignoring it is fully conforming." Severity: editorial.

---

## 15. appendix-g-file-id-hash — diagrams-03

Item 2: "computed over [0, F − 64) together with the trailer's other fields with
the `file_id` field taken as zero, then written in."

§6.2's table makes the trailer CRC a *field* of the trailer ("| 60 | 4 | u32 |
trailer CRC | structural | CRC-32C over trailer bytes [0, 60) |"), and it covers
file_id at trailer offset 48. So the literal reading is circular. Three
non-circular readings ((a) exclude the CRC field, (b) zero file_id in place and
hash all 64 bytes, (c) zero both) give three different digests. I looked for a
sentence fixing which, and there is none; nor is a hash function named, nor a
digest→64-bit reduction, nor the fallback when the result is 0 (which §6.2 forbids
as a file_id).

CONFIRMED. Byte-level: no — Appendix G is non-normative ("a writer ignoring it is
fully conforming") and §6.2 admits any nonzero file_id, so all three readings
produce conforming files every reader must accept. Severity: editorial.

---

## 16. vec-04-detector-field — diagrams-04

[R-VEC-02]'s per-damaged-structure minimum is "the outcome class (§2.4), the scope,
and the §21 register row it exercises" — no detector. [R-VEC-04] then switches on
"the entry's own scope and **detector** fields (`[R-VEC-02]`)". The "at minimum"
makes [R-VEC-02] a floor, so a corpus *may* carry a detector field, but [R-VEC-04]
requires one and attributes the requirement to a rule that does not state it.

CONFIRMED. Byte-level: no — manifest schema, and §24 makes the corpus derivative:
"where a vector's recorded expectation and this specification disagree, this
specification governs and the vector is corrected." Severity: editorial (add
"detector" to [R-VEC-02]'s list, or have [R-VEC-04] read the detector off the
recorded register row).

---

## 17. appendix-a-local-reader — diagrams-06

"A local reader additionally verifies bytes [0, 16) by equality first, which
`[R-CNT-04]` requires of any reader holding them". Main clause on transport,
subordinate clause on residency.

§6.1 is emphatic that the transport distinction does not govern this:

> "That distinction governs the request accounting of §6.4 and nothing else; the
> obligation over the front block turns on residency instead"

and "The test is residency, not transport". F6's Condition cell restates it
correctly. Appendix A's own subordinate clause carries the right test, and the
appendix is non-normative, so nothing is left open — but the main clause is a
residue of a superseded rule, and §6.1's own definition of a local reader ("one
whose transport serves any byte range at no per-range round trip") admits a local
reader that never holds [0, 16).

CONFIRMED (wording residue). Byte-level: no, on §6.1's "nothing else" sentence and
[R-CNT-04]'s "A reader that would have to issue a further range request to obtain
those bytes MAY defer or omit the check", which make both behaviours conforming by
construction. Severity: editorial.

---

## 18. r7-bom-instances — diagrams-07

R7's Condition states two alternatives over two containers = four; its Instances
cell delivers six, adding "leading U+FEFF". §21.1 fixes what an instance may name:
"a field the condition ranges over, a container it can occur in, **one of several
alternatives the condition text states**, or any combination of the three." The
BOM is not an alternative the condition text states, and §18.2 spells it out
separately ("The top-level value is an object, and the encoding carries no
byte-order mark: a leading U+FEFF makes the document unreadable"), so it is a
distinct alternative rather than a specialization.

My recount settles which side is wrong: the register totals 248 with the two BOM
instances included, matching §21.8 exactly. So the Instances cell is right and the
Condition cell lags. Deleting the instances would break [R-ERR-02]'s arithmetic.

CONFIRMED. Byte-level: no — [R-MTA-04] states the BOM rule normatively and
[R-CNT-25] fixes the outcome. Severity: register-bookkeeping.

---

## 19. index-encoding-defining-section — diagrams-08

Checked §15.1 in full. Its only mention of the field is "Under index_encoding 1
(the only encoding this format major version defines, §7.4)" — it states no value
set and points onward to §7.4, whose table row states the set and points back to
"(§15)". [R-EXT-03], [R-RDR-03], §10.2's cell and L31's Governing rule cell all
name §15.1. For the other five spaces [R-EXT-03] cites (§11.4, §12.2, §14.1,
§17.2, §17.3) the cited section does state the set — verified each.

This matters only for [R-EXT-05]'s tiebreaker: "Where the registry, §10.2's table,
and Appendix C diverge, the section that defines the space governs."

CONFIRMED. Byte-level: no — §7.4, §10.2, Appendix C and L31's three instances all
state 1 assigned / 2–0x7F reserved / ≥ 0x80 experimental, identically. Severity:
editorial.

---

## 20. front-matter-vector-identifiers — diagrams-10

"test vectors cite those identifiers rather than prose positions" vs [R-VEC-02]'s
"the §21 register row it exercises".

Refuted on two grounds the reporter himself identified and then filed anyway.
First, every register row carries a Governing rule cell naming the identifier —
§21.1: "the requirement that defines it" is a column of the register — so citing a
row cites the identifier transitively. Second, [R-VEC-02]'s list is explicitly a
floor ("at minimum"), so nothing bars a manifest from carrying the identifier
too. And the front matter's contrast is with *prose positions*, which row labels
certainly are not.

REFUTED. Byte-level: no. Severity: editorial at most — one word in [R-VEC-02]
("and the requirement it names") would end the question.

---

## 21. serve-unchanged-gloss — register-01

§21.1: "for several such rows it obliges the reader to serve the structure
unchanged (`[R-SER-08]`, `[R-CNT-22]`)".

[R-CNT-22] fits. [R-SER-08] fails both halves, and §14.2 says so imperatively:

> "A reader is not obligated to screen decoded content, and a reader that does not
> detect the violation is not thereby nonconforming; `[R-CNF-12]` governs a reader
> that does detect it. A reader that neither detects the violation nor rejects the
> tile, and returns the value, MUST report 0x00 as false and every other byte as
> true."

So it neither obliges serving (rejection is licensed) nor serving *unchanged*
(0x02 resolves to true). §12.3 calls this "the one case where a reader resolves a
byte to a value rather than passing it through" and Appendix H "the sole resolved
byte". The requirement that actually reads "unchanged" is [R-MTA-05] — "readers
process the document unchanged" — whose rows F27/L48 sit beside F28/L49, and the
parenthetical omits it.

CONFIRMED. Byte-level: no — §21.1 subordinates itself ("where a row and the rule
it cites diverge, the rule governs"), §14.2 states both answers imperatively, and
the byte concerned cannot occur in a conforming file. Severity: editorial (swap
[R-SER-08] for [R-MTA-05] in the parenthetical).

---

## 22. vec-02-cites-21-5 — register-02

[R-VEC-02]: "a conforming file can carry a record a reader ignores (§21.5,
§21.6)". The deciding sentence is inside the cited section itself:

> **§21.5 header.** "Every row here is a violation all the same: the outcome
> bounds a reader's blast radius and never makes the file conforming
> (`[R-CNF-12]`); §21.6 lists the ignore-record conditions that are not
> violations."

So §21.5 cannot support the proposition; only §21.6 can. Appendix H states it
correctly ("§21.6's defined conditions can — an experimental-range MU = 0 record
being conforming"). The reporter's reading (a) — loose citation supplying the
vocabulary — is the charitable one, but the citation is still wrong as it stands.

CONFIRMED (citation defect). Byte-level: no — §21.5's header, [R-CNF-12] ("A file
is conforming only if it satisfies every requirement at every scope") and Appendix
H each decide it identically, and [R-VEC-01] makes the specification govern over
any vector recorded the other way. Severity: editorial.

---

## 23. f33-non-layer-overlap — register-03

Shape (d) — two non-layer structures overlapping, e.g. a top-level record's extent
against the directory region.

Checked. F33's em-dash gloss enumerates only (b) and (c); [R-CNT-13]'s outcome
clause likewise splits "an intra-layer overlap... as reject-layer, and any overlap
across layers or touching another scope's structures as reject-file", which does
not describe two file-scope claimants. But the row's leading clause — "claimed by
two structures that do not belong to the same layer" — is satisfied (vacuously)
by (d), and F33's own Instances cell names "directory region" as a claimant, which
pairs only with (c) and (d). So the register does carry (d); the gloss and
[R-CNT-13]'s outcome dichotomy are what fall short.

CONFIRMED, narrower than reported (the row covers it; the prose does not). Byte-
level: no — [R-CNT-02] is unconditional ("No two of them overlap, and a file whose
live state does not partition this way is not a conforming file") and [R-LIF-08]
obliges disjointness over exactly this claimant set, so both readings converge on
nonconforming/reject-file. Severity: register-bookkeeping.

---

## 24. section-21-6-overbound-document — register-04

§21.5's "§21.6 lists the ignore-record conditions that are not violations" against
[R-MTA-09]'s over-bound document.

The closure claim the reporter tests does not exist. §21.1:

> "The subsections after §21.5 are not part of the register and carry no rows:
> neither this completeness clause nor the instance arithmetic below reaches
> §21.6's defined non-violations"

and §21.6's own header claims only "These are defined behaviors, not errors." So
§21.5's sentence is a signpost, not an assertion of closure, and it is not false.

But the condition is real and is genuinely of §21.6's kind — [R-MTA-09]'s Note:
"A file whose document decodes to more than the guarantee stays conforming... A
reader that proceeds takes ignore-record for that record." A §21.6 row would be an
improvement. PARTIAL. Byte-level: no — [R-MTA-09] states the outcome and
[R-ERR-04] the alternative, and [R-CNF-03]'s acceptance duty already does not run
past §21.9's guarantees. Severity: editorial.

---

## 25. f5-instances-F — register-05

F5's Instances cell reads "F (physical file size); committed_file_length". The
document uses F for the *committed* file length everywhere else — §5.1 ("the live
trailer's committed file length F"), §6.2's table ("committed_file_length ... = F"),
§15.3 ("with F the committed file length"), and F10/F32/L17/T9's F − 64. So the
cell's gloss of F contradicts the document's own definition.

The second instance's attribution is soft: a file whose *declared*
committed_file_length is below 128 also trips F17 (transport size) and F10
(dir_offset + dir_length ≤ F − 64 = 0). [R-VEC-02] already governs that: "the
entry records every row the file exercises and says which it was built for."

CONFIRMED, as a terminology defect in the cell. Byte-level: no — under either
reading the file is nonconforming, reject-file, reader, open. Severity: register-
bookkeeping. Note for the repair: F5 carries 2 of the register's 248 instances, so
collapsing it to one instance requires §21.8's total to become 247. Re-glossing
the cell ("physical file size; declared committed_file_length") costs nothing.

---

## 26. front-matter-normativity — adversary-02, quiz-01

[R-CNF-01]: "All text in this document is normative except: §1 (Introduction); any
text labeled *Note*, *Example*, or *Rationale*; and appendices identified as
non-normative."

The "How to read this document" block sits above §1, is labelled *(non-normative)*,
is not a Note/Example/Rationale, and is not an appendix. Confirmed by inspection:
it is the only such block, and the status paragraph and licence line above §1 are
in the same position. Appendix F ("Normative references") is correctly unmarked, so
the appendix half of the rule is clean.

I looked for a sentence bringing the front matter inside one of the three
exceptions and found none.

CONFIRMED. Byte-level: no. Under the normative reading the block's claims are
about document layout (§4.7 states the taxonomy normatively with [R-ENC-16]) and
corpus citation ([R-VEC-02] states the manifest's contents, and [R-VEC-01] makes
the corpus derivative: "this specification governs and the vector is corrected").
Nothing in the block constrains a byte of any file. Severity: editorial (add
"any text labeled non-normative" or "the front matter" to [R-CNF-01]'s list).

---

## 27. section-21-7-opaque-ground — adversary-03

§21.7 gives "opaque by construction" as the ground for omitting [R-CNT-13]'s
no-embedded-offsets prohibition. §7.3 registers exactly one MU = 0 type — 0x0002,
user metadata — whose extent contents this specification defines down to duplicate-
key identity and number finiteness. So the stated ground is untrue for the only
MU = 0 instance a format-major-1 file can carry.

The conclusion nonetheless stands, on a different ground I found in §18.1:

> **[R-MTA-01].** "Its content is application data: this specification defines its
> encoding, not its meaning."

Meaning being undefined, no verifier can establish that a JSON number is an offset,
so the obligation is still witness-free. And the reader-side guard is elsewhere and
is a MUST: [R-MTA-02], "A reader MUST NOT let any part of a user-metadata document
affect how a byte is located, decoded, or returned."

CONFIRMED, as an imprecise justification rather than a register gap. Byte-level:
no, on [R-MTA-02] and [R-MTA-01] above — no verifier can reach a different verdict
on any concrete file under either reading. Severity: editorial.

---

## 28. trailer-mimic-slack-justification — adversary-07

§21.6's row: "| A payload contains a byte string that mimics a trailer | Inert:
nothing enumerates slack, ... |". §5.2 makes a stored-tile extent a *structure* of
the live committed state, and "Every byte the live state does not claim is
**slack**" — so the condition names a payload and the justification names a
disjoint byte class.

The correct grounds exist and are sound: [R-LIF-05] ("a reader that finds no valid
trailer in the final 64 bytes MUST report the file torn or invalid and MUST NOT
scan backward") and §6.2's Note for the end-of-file placement ("caught at the
directory CRC (§7.1)").

§22.3 makes the same slide in one paragraph but is defensible on a charitable
reading — it opens on the payload case (answered by re-verification) and then
treats a *slack* mimic separately. §21.6's row is the one that mismatches.

CONFIRMED. Byte-level: no — §21.1: "where such an entry and the rule it cites
diverge, the rule governs there too", and [R-LIF-05]/[R-LIF-06] decide every file
identically. Severity: editorial.

---

## 29. mu1-compaction-scope — adversary-08

§20.4's MU = 1 row ends "Compaction is barred on the same ground (`[R-WRT-06]`)"
after the file-scope discussion.

Decided, and by the requirement a compactor author must read:

> **[R-WRT-06].** "A compactor MUST refuse to compact a file carrying **any**
> record whose type it does not implement with MU = 1: such a type can define
> references this specification does not (§7.2), so its bytes cannot be safely
> relocated."

"any record" is categorical and its stated reason applies with full force to a
layer sub-record's extent, which is exactly what compaction relocates. §7.2
confirms the premise: "Records with MU = 1 carry further references only where
this specification or registry review (§10) defines them."

PARTIAL: the ambiguity claim is refuted, but §20.4's sentence reads narrowly by
placement and a three-word fix ("by such a record at either scope") removes the
invitation. Byte-level: no — the reporter's own caveat is answered by the
categorical quote above; no reading licenses compactor A. Severity: editorial.

---

## 30. compactor-version-minor — quiz-02

The one finding self-flagged byte-level that I could not simply dispose of, and the
closest call in this pass.

§20.5 [R-WRT-06]: "The output trailer copies the input's unknown ignore-lane flag
bits forward (`[R-CNT-08]`) and carries the greater of `[R-CNT-26]`'s floor and the
input's version_minor". [R-CNT-26] is a SHOULD binding "a writer" and "an
appender"; §20.1 makes the compactor a third tier.

Arguments each way, both real:

- For MUST: §2.1 makes BCP 14 force keyword-gated ("when, and only when, they
  appear in all capitals"), and the clause carries no keyword, so it cannot be
  read as a SHOULD by inheritance; and §2.1 makes all such text normative. The
  same construction two sentences earlier — "Given a conforming input the output
  is a conforming file" — I relied on as normative in group 2, so I must treat
  declaratives here consistently.
- For SHOULD: the conjoined first clause restates [R-CNT-08]'s MUST, so the
  parallel is "each conjunct at its cited rule's strength", which for the second
  is a SHOULD. And [R-CNT-26]'s floor for a file carrying an unknown ignore-lane
  bit is *not* 0 ("the lowest version_minor that defines every feature present in
  the file" — the parenthetical "for a file expressible under this text, 0" does
  not reach such a file), so §20.5's rule is a computable proxy for [R-CNT-26]'s
  own floor rather than a new obligation.

I could not find a sentence that picks one. So: CONFIRMED as an ambiguity.

Byte-level: no. The deciding quotes:

> **§6.2 table.** "| 10 | 2 | u16 | version_minor | descriptive | any (see §6.3) |"

> **[R-CNT-07].** "A reader MUST NOT reject a file for its version_minor: minor
> releases are additive-only, and all feature gating is structural (records,
> enums, flags)."

> **[R-ENC-16].** "It is **descriptive** if neither — its value determines nothing
> a conforming reader does"

> **[R-CNF-12].** "Deviation from a SHOULD is not a violation for this purpose:
> §21's register enumerates MUST-level conditions only, and a verifier reports a
> SHOULD deviation as an advisory that does not bar certification."

Under both readings both output files are conforming files, every conforming
reader accepts both and returns identical data, and every verifier certifies both
(§21 carries no version_minor row, and could not: §6.2 admits any value). The
fork is confined to whether a particular tool is a conforming *compactor* — the
same category [R-CNF-02] already names for §6.3's flags = 0 obligation, which
"binds the actor" without making any file nonconforming. Two bytes move, and
nothing in the format's conformance predicate or any reader's behaviour moves with
them, by the deliberate design of the one descriptive field the format has.

Severity: design-decision. The maintainer must state the strength — either add
MUST to §20.5's clause, or say it restates [R-CNT-26] at SHOULD strength for the
compactor tier. Recorded as the closest call in this pass.

---

## 31. cross-major-crc-verdict — quiz-03

Verdict for a file declaring an unimplemented major whose trailer CRC fails.

Killed, by the interaction of §6.2's ordering with [R-ENC-10] — which quiz-03
cited for the ordering but did not follow through:

> **[R-ENC-10].** "A reader MUST verify the checksum covering a field before
> acting on that field — where *acting on* means using its value to allocate,
> seek, fetch, or **select behavior**"

> **§6.2 [R-CNT-06].** "A reader MUST validate, in order: the trailer magic; the
> trailer CRC; the version gate (§6.3)"

version_major is covered by the trailer CRC. Once the CRC fails, the reader may
not act on version_major, and the version gate is precisely "selecting behavior"
on it. So there is no trustworthy declaration of another major to invoke §2.3's
exemption; what has been established is F14, a violation, and §2.3 then decides:

> "An established violation takes priority: a verifier that has established any
> violation reports *nonconforming*, however many requirements it was unable to
> check, and *cannot establish* is available only to a traversal that established
> no violation."

Reading (1) is what the text determines; the reporter picked (2). §2.3's "a file
declaring another major" presupposes a declaration the reader is permitted to act
on, which §6.2's ordering exists to establish and [R-CNT-24]'s permanence exists to
make possible across majors.

REFUTED. Byte-level: no — both verdicts are non-certification and a conforming
reader takes reject-file either way. Severity: editorial — a clause in §2.3 noting
that the cross-major exemption presupposes a verified trailer CRC would foreclose
the misreading cheaply.

---

## Groups I tried hardest to kill and failed

- **6 (commit-narrowing-extent-padding).** I went through §20.1's "a violation
  latent in a structure they neither modify nor rely on travels with it", §20.3
  step 2's no-repair rule, §11.1's rationale, and [R-SLB-04], looking for anything
  that either forbids narrowing an extent or states the re-emission duty. Nothing
  does. The absence is the evidence.
- **26 (front-matter-normativity).** I checked every "non-normative" occurrence and
  every appendix heading looking for a rule that reaches the front matter.
  [R-CNF-01]'s list is closed and does not.
- **12/15 (Appendix G).** I read item 3 and item 2 several times looking for an
  implied total order and an implied hash. Neither exists.
- **2 (compactor-placement).** Tried hardest of all, and *succeeded* — see above.
- **30 (compactor version_minor).** Tried hardest to find a strength-fixing
  sentence and failed; the ambiguity stands, but the byte-level flag does not.

## Coverage

41 input ids, 31 groups, each id in exactly one group, no duplicates. Counted
twice by hand and once by listing the member arrays. No finding was dropped for
weakness; the six graded REFUTED are grouped and graded, not omitted.

Byte-level count: 0.
